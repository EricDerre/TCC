#!/usr/bin/env python3
# ! Alteração de IA - Revisar: módulo novo (11/11/2026, corrida 27, ficha 67 opção b, decisão 121): a revisão humana às cegas das propostas de edição da medida M2.
# `--gerar` junta as propostas da corrida 27 que passaram nos filtros de hoje com as 20 edições da corrida 20 que a revisão do lote julgou, embaralha com semente fixa e
# grava três coisas: a página (Documentacao/dashboard/revisao-propostas.html, uma proposta por vez, com o verbete de destino, a ficha do caso e os três vereditos da
# revisão do lote: Correta, Parcial, Errada), a planilha às cegas (para quem preferir preencher em Markdown) e a chave, que guarda de qual corrida veio cada item e fica
# fora do que o revisor lê. `--gravar` passa as respostas (lidas do banco da página ou da planilha preenchida) para `revisao_as_cegas.json` na pasta da corrida, que é o
# que `avaliar_fase4.py --analista` lê, e grava a planilha final, já com a origem. `--estado` conta o que tem veredito.
# ! Motivo: a medida M2 da proposta do analista de documentação pede "a mesma revisão humana, às cegas": a parcela correta das duas corridas só se compara se a mesma
# pessoa julgar as duas sem saber de onde veio cada proposta. A revisão do lote da corrida 20 foi feita em planilha; o Eric passou a preferir a página (a sessão de
# revisão e a curadoria das leituras), e por isso há as duas formas, no molde de `sessao_revisao.py` e de `curadoria_leituras.py`. Quem revisa é resposta do Eric: a
# ferramenta não tem nome padrão e recusa gravar sem `--quem`. A cegueira tem um limite, que a leitura declara: o tipo "verbete novo" só existe na corrida 20, e o
# jeito de escrever pode denunciar a origem.
"""Uso:
  python ferramentas/revisao_propostas.py --gerar [--sem-a-corrida-20] [--saida <html>]            gera a página, a planilha às cegas e a chave da origem
  python ferramentas/revisao_propostas.py --gravar respostas.json --quem "<quem revisou>"          grava a revisão lida do banco da página na pasta da corrida
  python ferramentas/revisao_propostas.py --gravar --da-planilha --quem "<quem revisou>"           o mesmo, lendo a planilha às cegas preenchida
  python ferramentas/revisao_propostas.py --estado                                                 quantas propostas têm veredito
"""
from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import os
import random
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
EXP = RAIZ / "Programacao" / "AgenteCore" / "experimentos"
# ! Alteração de IA - Revisar: a ferramenta aponta o harness para `resultados_alvo` antes de importar qualquer módulo dele, sem trocar um valor que já esteja definido.
# ! Motivo: `caminhos.py` lê a variável RESULTADOS_DIR na importação; sem ela, os registros das corridas 20 e 27 seriam procurados na pasta da máquina de desenvolvimento.
os.environ.setdefault("RESULTADOS_DIR", "resultados_alvo")
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(EXP))
import biblioteca as bib
import caminhos
import curadoria_leituras as cl
import executar_bateria
import executar_fase3
import experimento_analista as ea
import portoes_de_edicao as pe

SAIDA = RAIZ / "Documentacao" / "dashboard" / "revisao-propostas.html"
CORRIDA = "fase4_analista"
SEMENTE = 20261111
VEREDITOS = pe.VEREDITOS
CELULA_EM_BRANCO = "(em branco)"
ARQ_PLANILHA = "revisao_as_cegas_planilha.md"      # a planilha que o revisor preenche, sem a origem
ARQ_CHAVE = "revisao_as_cegas_chave.json"          # de qual corrida veio cada item; o revisor não abre este arquivo
ARQ_REVISAO = ea.ARQ_DA_REVISAO                    # o resultado que avaliar_fase4.py --analista lê
ARQ_PLANILHA_FINAL = "revisao_as_cegas.md"         # a planilha depois da revisão, com o veredito e a origem de cada item
NOME_DA_ORIGEM = {"27": "corrida 27", "20": "corrida 20"}
NOME_DA_OPERACAO = {"nota": "nota (uma frase acrescentada ao verbete)", "retificacao": "retificação (aponta um trecho do verbete e dá a frase certa)",
                    "novo_verbete": "verbete novo", "sinal_de_busca": "sinal de busca (palavras-chave e sintomas acrescentados ao verbete, sem texto)"}
# Os critérios são os da revisão do lote da corrida 20 (revisao_do_lote.md), com uma linha a mais para o sinal de busca, que aquela revisão não tinha.
CRITERIOS = {"Correta": "Correta: o que a proposta afirma é verdade sobre o sistema e serve ao diagnóstico da causa do verbete. Vale também quando o verbete já dizia o mesmo; anote isso no comentário.",
             "Parcial": "Parcial: vaga, recomendação sem fato novo, verdade só em parte ou verdade fora de lugar. Vale também para verbete novo que só repete um verbete que já existe.",
             "Errada": "Errada: afirma o que o código não faz, inverte o caso ou põe a causa em outro componente.",
             "sinal": "Num sinal de busca não há frase: julgue os termos. Corretos quando descrevem o que um caso dessa causa mostra; parciais quando são vagos ou servem a várias causas; errados quando são de outra causa."}
_CELULA_RE = re.compile(r"(?<!\\)\|")


# ------------------------------------------------------------------ o que vai para a revisão

def _da_edicao(origem: str, edicao: dict, ficha: str, verbetes: dict[str, dict]) -> dict:
    vid = str(edicao.get("verbete"))
    if edicao.get("operacao") == "novo_verbete":
        novo = edicao.get("novo") or {}
        verbete_texto = (f"(verbete novo, proposto com o título \"{novo.get('titulo') or vid}\", para as causas {', '.join(novo.get('causas') or []) or 'não informadas'}; "
                         "não existe na biblioteca)")
    else:
        verbete_texto = bib.render(verbetes[vid]) if vid in verbetes else "(verbete fora da biblioteca)"
    return {"origem": origem, "caso": str(edicao.get("caso") or ""), "verbete": vid, "operacao": str(edicao.get("operacao")), "texto": edicao.get("texto") or "",
            "trecho": edicao.get("trecho") or "", "palavras_chave": list(edicao.get("palavras_chave_novas") or []), "sintomas": list(edicao.get("sintomas_novos") or []),
            "motivo": edicao.get("motivo") or "", "verbete_texto": verbete_texto, "ficha": ficha}


def itens_da_revisao(registros: list[dict], com_a_corrida_20: bool = True, semente: int = SEMENTE) -> list[dict]:
    """O que vai para a revisão às cegas: as propostas da corrida 27 que passaram nos filtros de hoje (os mesmos que escolheram o que foi revisado na corrida 20) e,
    com `com_a_corrida_20`, as 20 edições que a revisão do lote julgou. Cada item leva o verbete de destino como estava antes do lote e a ficha do caso, que é a mesma
    para as duas corridas. A ordem é embaralhada com semente fixa, e o número do item não diz nada da origem."""
    verbetes = {v["id"]: v for v in bib.carregar(ea.base_da_corrida_20())}
    fichas = {i["caso"]["id"]: ea.ficha_do_caso(i, verbetes) for i in ea.casos_da_corrida_20()}
    itens = [_da_edicao("27", r["edicao"], r.get("ficha") or fichas.get(r["caso"], ""), verbetes) for r in registros if r.get("passa_nos_filtros_de_hoje") and r.get("edicao")]
    if com_a_corrida_20:
        itens += [_da_edicao("20", e, fichas.get(str(e.get("caso")), ""), verbetes) for e in pe.edicoes_do_lote_da_corrida_20()]
    random.Random(semente).shuffle(itens)
    return [{"n": n, "id": f"p{n:02d}", **i} for n, i in enumerate(itens, 1)]


def publico(item: dict) -> dict:
    """O item como o revisor o vê: sem a origem."""
    return {k: v for k, v in item.items() if k != "origem"}


def _esc(texto: str) -> str:
    return str(texto).replace("|", "\\|").replace("\n", " ")


def _texto_ou_termos(i: dict) -> str:
    if i["operacao"] == "sinal_de_busca":
        return "; ".join(x for x in ("palavras-chave: " + ", ".join(i["palavras_chave"]) if i["palavras_chave"] else "", "sintomas: " + ", ".join(i["sintomas"]) if i["sintomas"] else "") if x)
    return i["texto"]


def planilha(itens: list[dict]) -> str:
    """A planilha às cegas: uma linha por proposta, na ordem embaralhada, com a coluna Avaliação em branco e sem nenhuma coluna que diga a origem."""
    linhas = ["<!-- ! Alteração de IA - Revisar: planilha da revisão humana às cegas das propostas de edição, gerada por ferramentas/revisao_propostas.py --gerar; preencher a coluna",
              "     Avaliação (Correta, Parcial ou Errada) e, se quiser, o Comentário. A origem de cada linha fica num arquivo à parte, que o revisor não abre.",
              "     ! Motivo: a medida M2 pede que a mesma pessoa julgue as propostas sem saber de onde veio cada uma; é a outra forma de responder, para quem preferir a planilha à página. -->",
              "", "# Revisão às cegas das propostas de edição", "",
              *(f"- {c}" for c in CRITERIOS.values()), "",
              "| # | Verbete | Operação | Caso | Texto ou termos | Trecho que a retificação corrige | Motivo | Avaliação | Comentário |",
              "|---|---|---|---|---|---|---|---|---|"]
    for i in itens:
        linhas.append("| " + " | ".join([str(i["n"]), f"`{i['verbete']}`", i["operacao"], i["caso"], _esc(_texto_ou_termos(i)), _esc(i["trecho"]), _esc(i["motivo"]), CELULA_EM_BRANCO, ""]) + " |")
    return "\n".join(linhas) + "\n"


def vereditos_da_planilha(texto: str) -> dict[int, tuple[str, str]]:
    """número do item -> (avaliação, comentário), de cada linha da planilha às cegas."""
    saida: dict[int, tuple[str, str]] = {}
    for linha in texto.splitlines():
        if not linha.startswith("| ") or linha.startswith("| # |"):
            continue
        cel = [c.strip() for c in _CELULA_RE.split(linha)[1:-1]]
        if len(cel) != 9 or not cel[0].isdigit():
            continue
        saida[int(cel[0])] = (cel[7], cel[8])
    return saida


# ------------------------------------------------------------------ a página

CORPO = """
<header class="topo">
  <p class="olho">Medida M2 do analista de documentação, revisão humana às cegas</p>
  <h1>Revisão das propostas de edição</h1>
  <nav class="trilho" aria-label="Propostas">
    <ol id="trilho-lista">@@PIPS@@</ol>
    <span id="contagem" class="contagem">0 de @@TOTAL@@ julgadas</span>
  </nav>
</header>
<div id="aviso" class="aviso" role="status" hidden><span id="aviso-texto"></span></div>
<main>
  <section id="inicio" class="bloco">
    <p>São @@TOTAL@@ propostas de acréscimo à documentação que o modelo escreveu. Elas vêm de duas rodadas diferentes e estão embaralhadas: a página não diz de qual rodada veio cada uma, e é para ser assim. Dá para parar a qualquer momento: o que está respondido fica guardado nesta página.</p>
    <ol>
      <li><strong>Leia a proposta</strong>: a operação, o texto (ou os termos, no sinal de busca), o trecho que ela corrige, quando há, e o motivo que o modelo deu.</li>
      <li><strong>Confira</strong> contra o verbete de destino e a ficha do caso, que ficam à direita, e contra o código das cobaias, quando a proposta fala do que o sistema faz.</li>
      <li><strong>Julgue</strong> com um dos três vereditos e, se quiser, deixe um comentário.</li>
    </ol>
    <ul>@@CRITERIOS@@</ul>
    <button type="button" id="comecar" class="primario">Começar pela primeira proposta sem veredito</button>
  </section>
  <section id="item" class="item" hidden>
    <h2 id="item-titulo"></h2>
    <p class="meta">verbete <code id="item-verbete"></code> · caso <code id="item-caso"></code> · <span id="item-marca" class="marca"></span></p>
    <div class="colunas">
      <div>
        <div id="proposta" class="filtros"></div>
        <label for="comentario"><strong>Comentário (opcional)</strong></label>
        <textarea id="comentario" rows="4" spellcheck="true" style="width:100%;box-sizing:border-box"></textarea>
        <div class="acoes">
          <button type="button" id="correta" class="bom">Correta</button>
          <button type="button" id="parcial" class="primario">Parcial</button>
          <button type="button" id="errada">Errada</button>
        </div>
        <p id="mensagem" class="mensagem" role="alert"></p>
        <div class="acoes">
          <button type="button" id="anterior" class="discreto">Anterior</button>
          <button type="button" id="proxima" class="discreto">Próxima sem veredito</button>
        </div>
      </div>
      <div>
        <details open><summary>Verbete de destino (como estava antes das propostas)</summary><pre id="verbete" class="previa" style="white-space:pre-wrap"></pre></details>
        <details open><summary>Ficha do caso que motivou a proposta</summary><pre id="ficha" class="previa" style="white-space:pre-wrap"></pre></details>
      </div>
    </div>
  </section>
  <section id="fim" class="fim" hidden>
    <h2>Todas as propostas têm veredito</h2>
    <p>Avise o Claude: ele lê as respostas do banco desta página e grava a revisão. Para trocar um veredito, clique no número da proposta acima.</p>
    <table><thead><tr><th>Proposta</th><th>Veredito</th><th>Quando</th></tr></thead><tbody id="fim-linhas"></tbody></table>
    <details class="copia"><summary>Copiar as respostas</summary>
      <p class="nota">Serve para quando as respostas não chegam ao banco da página: cole o texto na conversa com o Claude.</p>
      <textarea id="respostas-texto" rows="8" readonly></textarea>
      <div class="acoes"><button type="button" id="copiar">Copiar</button> <span id="copia-status" role="status"></span></div>
    </details>
  </section>
</main>
"""

JS = r"""
(() => {
  "use strict";
  document.documentElement.lang = "pt-BR";
  const ITENS = JSON.parse(document.getElementById("itens").textContent);
  const OPERACOES = JSON.parse(document.getElementById("operacoes").textContent);
  const CHAVE = "revisao_propostas_v1";
  const $ = (id) => document.getElementById(id);
  let banco = null, carregou = false, salvas = {}, atual = -1, gravando = false;
  const local = lerLocal();

  function lerLocal() {
    try { const v = JSON.parse(localStorage.getItem(CHAVE) || "{}"); return {atual: v.atual == null ? -1 : v.atual, rascunhos: v.rascunhos || {}, respostas: v.respostas || {}}; }
    catch (e) { return {atual: -1, rascunhos: {}, respostas: {}}; }
  }
  function guardarLocal() { try { localStorage.setItem(CHAVE, JSON.stringify(local)); } catch (e) {} }
  const resposta = (id) => salvas[id] || local.respostas[id] || null;
  const respondida = (i) => !!resposta(ITENS[i].id);
  function aviso(texto) { $("aviso-texto").textContent = texto || ""; $("aviso").hidden = !texto; }

  function pips() {
    ITENS.forEach((x, i) => {
      const b = $("pip-" + i), r = resposta(x.id);
      b.className = "pip" + (i === atual ? " atual" : "") + (r ? (r.veredito === "Correta" ? " feita" : r.veredito === "Parcial" ? " curada" : " adiada") : "");
      b.title = x.id + (r ? " (" + r.veredito + ")" : "");
    });
    $("contagem").textContent = ITENS.filter((_, i) => respondida(i)).length + " de " + ITENS.length + " julgadas";
  }

  function proximaEmAberto(desde) {
    for (let k = 1; k <= ITENS.length; k++) { const j = (desde + k) % ITENS.length; if (!respondida(j)) return j; }
    return -1;
  }

  function linha(rotulo, valor) {
    const p = document.createElement("p"), s = document.createElement("strong");
    s.textContent = rotulo + " ";
    p.append(s, document.createTextNode(valor));
    return p;
  }

  function mostrar(i) {
    atual = i; local.atual = i; guardarLocal();
    const x = ITENS[i], r = resposta(x.id);
    $("inicio").hidden = true; $("fim").hidden = true; $("item").hidden = false;
    $("item-titulo").textContent = "Proposta " + (i + 1) + " de " + ITENS.length;
    $("item-verbete").textContent = x.verbete;
    $("item-caso").textContent = x.caso;
    const marca = $("item-marca");
    marca.textContent = r ? "julgada: " + r.veredito : "sem veredito";
    marca.className = "marca" + (r ? " feita" : "");
    const blocos = [linha("Operação:", OPERACOES[x.operacao] || x.operacao)];
    if (x.texto) blocos.push(linha("Texto proposto:", x.texto));
    if (x.palavras_chave.length) blocos.push(linha("Palavras-chave novas:", x.palavras_chave.join(", ")));
    if (x.sintomas.length) blocos.push(linha("Sintomas novos:", x.sintomas.join(", ")));
    if (x.trecho) blocos.push(linha("Trecho do verbete que ela corrige:", x.trecho));
    blocos.push(linha("Motivo dado pelo modelo:", x.motivo));
    $("proposta").replaceChildren(...blocos);
    $("verbete").textContent = x.verbete_texto;
    $("ficha").textContent = x.ficha;
    $("comentario").value = local.rascunhos[x.id] != null ? local.rascunhos[x.id] : (r && r.comentario) || "";
    $("mensagem").textContent = "";
    botoes();
    pips();
    window.scrollTo({top: 0});
  }

  function botoes() {
    ["correta", "parcial", "errada"].forEach((id) => { $(id).disabled = gravando; });
    $("anterior").disabled = atual <= 0;
  }

  async function gravar(doc) {
    if (!banco) { local.respostas[doc.id] = doc; guardarLocal(); return "local"; }
    const ref = banco.collection("revisao_propostas").doc(doc.id);
    try { await ref.set(doc); }
    catch (e) {
      if (!e || e.code !== "unavailable") throw e;
      await new Promise((ok) => setTimeout(ok, 500 + Math.random() * 800));
      await ref.set(doc);
    }
    salvas[doc.id] = doc;
    return "banco";
  }

  async function responder(veredito) {
    const x = ITENS[atual];
    const anterior = resposta(x.id);
    const agora = new Date().toISOString();
    const doc = {id: x.id, n: x.n, veredito: veredito, comentario: $("comentario").value.trim(), salvo_em: anterior && anterior.salvo_em ? anterior.salvo_em : agora,
                 editado_em: anterior ? agora : null};
    gravando = true; botoes();
    try {
      const onde = await gravar(doc);
      delete local.rascunhos[x.id]; guardarLocal();
      if (onde === "local") aviso("Sem o banco da página: as respostas ficam só neste navegador. No fim, use Copiar as respostas.");
    } catch (e) {
      $("mensagem").textContent = "Não consegui gravar (" + ((e && e.code) || "erro") + "). Tente de novo.";
      gravando = false; botoes(); return;
    }
    gravando = false;
    pips();
    const j = proximaEmAberto(atual);
    if (j < 0) fim(); else mostrar(j);
  }

  function fim() {
    $("inicio").hidden = true; $("item").hidden = true; $("fim").hidden = false;
    const tb = $("fim-linhas");
    tb.replaceChildren();
    ITENS.forEach((x, i) => {
      const r = resposta(x.id);
      const tr = document.createElement("tr");
      ["Proposta " + (i + 1), r ? r.veredito : "sem veredito", r && r.salvo_em ? r.salvo_em.replace("T", " ").slice(0, 16) : ""].forEach((v) => { const td = document.createElement("td"); td.textContent = v; tr.appendChild(td); });
      const td = document.createElement("td");
      const b = document.createElement("button"); b.type = "button"; b.className = "discreto"; b.textContent = "Trocar"; b.dataset.i = String(i); td.appendChild(b); tr.appendChild(td);
      tb.appendChild(tr);
    });
    $("respostas-texto").value = JSON.stringify(ITENS.map((x) => resposta(x.id)).filter(Boolean), null, 1);
    pips();
    window.scrollTo({top: 0});
  }

  $("comecar").addEventListener("click", () => { const j = proximaEmAberto(-1); if (j < 0) fim(); else mostrar(j); });
  $("correta").addEventListener("click", () => responder("Correta"));
  $("parcial").addEventListener("click", () => responder("Parcial"));
  $("errada").addEventListener("click", () => responder("Errada"));
  $("anterior").addEventListener("click", () => { if (atual > 0) mostrar(atual - 1); });
  $("proxima").addEventListener("click", () => { const j = proximaEmAberto(atual); if (j < 0) fim(); else mostrar(j); });
  $("comentario").addEventListener("input", () => { local.rascunhos[ITENS[atual].id] = $("comentario").value; guardarLocal(); });
  $("trilho-lista").addEventListener("click", (ev) => { const b = ev.target.closest("button[data-i]"); if (b) mostrar(Number(b.dataset.i)); });
  $("fim-linhas").addEventListener("click", (ev) => { const b = ev.target.closest("button[data-i]"); if (b) mostrar(Number(b.dataset.i)); });
  $("copiar").addEventListener("click", () => {
    const t = $("respostas-texto");
    const escolher = () => { t.focus(); t.select(); $("copia-status").textContent = "Selecionei o texto: use Ctrl+C."; };
    if (!navigator.clipboard) { escolher(); return; }
    navigator.clipboard.writeText(t.value).then(() => { $("copia-status").textContent = "Copiado."; }, escolher);
  });

  function semOBanco(motivo) { banco = null; aviso("Sem o banco da página" + (motivo ? " (" + motivo + ")" : "") + ": as respostas ficam só neste navegador. No fim, use Copiar as respostas."); pips(); }

  (async () => {
    pips();
    let db = null;
    try { db = window.claude ? await window.claude.use("db") : null; } catch (e) { db = null; }
    if (!db) { semOBanco(""); return; }
    banco = db;
    const relogio = setTimeout(() => { if (!carregou) aviso("O banco da página ainda não respondeu; o que você gravar fica à espera dele."); }, 10000);
    banco.collection("revisao_propostas").onSnapshot((foto) => {
      const novo = {};
      foto.docs.forEach((d) => { if (d.exists) novo[d.id] = d.data(); });
      salvas = novo;
      if (!foto.metadata.fromCache) { carregou = true; clearTimeout(relogio); aviso(""); }
      pips();
    }, (e) => { clearTimeout(relogio); semOBanco(e && e.code); });
  })();
})();
"""


def pagina(itens: list[dict]) -> str:
    """A página da revisão: os itens em JSON, sem a origem, a folha de estilo da página de curadoria e o script; as respostas ficam no banco da própria página."""
    def seguro(obj) -> str:
        return json.dumps(obj, ensure_ascii=False).replace("<", "\\u003c")

    pips = "".join(f'<li><button type="button" class="pip" id="pip-{i}" data-i="{i}">{i + 1}</button></li>' for i in range(len(itens)))
    criterios = "".join(f"<li>{html.escape(c)}</li>" for c in CRITERIOS.values())
    corpo = CORPO.replace("@@TOTAL@@", str(len(itens))).replace("@@PIPS@@", pips).replace("@@CRITERIOS@@", criterios)
    return ("<title>Revisão das propostas de edição</title>\n"
            '<meta name="claude:viewport-fit-sides" content="cover">\n'
            "<!-- ! Alteração de IA - Revisar: página gerada por ferramentas/revisao_propostas.py --gerar para a revisão humana às cegas das propostas de edição (medida M2 do analista de "
            "documentação, decisão 121).\n"
            "     ! Motivo: a mesma pessoa julga as propostas de duas rodadas sem saber de qual veio cada uma; os textos vêm dos registros das corridas, e as respostas ficam no banco da própria "
            "página até o Claude gravá-las na pasta da corrida. -->\n"
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Source+Serif+4:wght@600&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">\n'
            f"<style>{cl.CSS}</style>\n{corpo}\n"
            f'<script type="application/json" id="itens">{seguro([publico(i) for i in itens])}</script>\n'
            f'<script type="application/json" id="operacoes">{seguro(NOME_DA_OPERACAO)}</script>\n<script>{JS}</script>\n')


# ------------------------------------------------------------------ o resultado

def montar_revisao(itens: list[dict], respostas, quem: str) -> dict:
    """Junta as respostas à chave e devolve o que `experimento_analista.resumir` lê: quem revisou e, para cada item, a origem e o veredito. `respostas` é a lista do banco
    da página (`id`, `veredito`, `comentario`) ou o dicionário da planilha (número -> avaliação e comentário). Item sem resposta fica sem veredito, e a leitura o conta
    como pendente. Para (SystemExit) com veredito fora dos três, com item desconhecido ou sem dizer quem revisou."""
    if not str(quem or "").strip():
        raise SystemExit("falta dizer quem revisou (--quem): a ferramenta não registra a revisão sem isso")
    por_id = {i["id"]: i for i in itens}
    if isinstance(respostas, dict):
        respostas = [{"id": f"p{n:02d}", "veredito": av, "comentario": com} for n, (av, com) in respostas.items() if av != CELULA_EM_BRANCO]
    vistos: dict[str, dict] = {}
    for r in respostas:
        if r.get("id") not in por_id:
            raise SystemExit(f"a resposta {r.get('id')!r} não é de nenhum item desta revisão")
        if r.get("veredito") not in VEREDITOS:
            raise SystemExit(f"veredito {r.get('veredito')!r} no item {r.get('id')}: use um de {', '.join(VEREDITOS)}")
        vistos[r["id"]] = r
    saida = [{"n": i["n"], "id": i["id"], "origem": i["origem"], "caso": i["caso"], "verbete": i["verbete"], "operacao": i["operacao"],
              "veredito": (vistos.get(i["id"]) or {}).get("veredito"), "comentario": (vistos.get(i["id"]) or {}).get("comentario") or ""} for i in itens]
    return {"quem": str(quem).strip(), "gravado_em": dt.datetime.now().isoformat(timespec="seconds"), "itens_na_revisao": len(itens), "respondidas": len(vistos),
            "criterios": CRITERIOS, "itens": saida}


def planilha_final(itens: list[dict], revisao: dict) -> str:
    """A planilha depois da revisão: a mesma ordem, com o veredito, o comentário e, agora sim, a origem de cada item."""
    vistos = {x["id"]: x for x in revisao["itens"]}
    linhas = ["<!-- ! Alteração de IA - Revisar: planilha final da revisão humana às cegas das propostas de edição, gravada por ferramentas/revisao_propostas.py --gravar a partir das",
              "     respostas do revisor; a coluna Origem só aparece aqui, depois da revisão.",
              "     ! Motivo: é o registro legível do que `revisao_as_cegas.json` guarda e do que a leitura da corrida 27 usa para comparar a parcela correta das duas corridas. -->",
              "", "# Revisão às cegas das propostas de edição: resultado", "",
              f"Quem revisou: {revisao['quem']}. Itens: {revisao['itens_na_revisao']}; com veredito: {revisao['respondidas']}.", "",
              "| # | Origem | Verbete | Operação | Caso | Texto ou termos | Motivo | Avaliação | Comentário |", "|---|---|---|---|---|---|---|---|---|"]
    for i in itens:
        v = vistos.get(i["id"]) or {}
        linhas.append("| " + " | ".join([str(i["n"]), NOME_DA_ORIGEM.get(i["origem"], i["origem"]), f"`{i['verbete']}`", i["operacao"], i["caso"], _esc(_texto_ou_termos(i)),
                                         _esc(i["motivo"]), v.get("veredito") or "sem veredito", _esc(v.get("comentario") or "")]) + " |")
    return "\n".join(linhas) + "\n"


def gerar(registros: list[dict], pasta: Path, saida: Path = SAIDA, com_a_corrida_20: bool = True, semente: int = SEMENTE) -> list[Path]:
    """Grava a página, a planilha às cegas e a chave. A chave guarda os itens inteiros, com a origem, para a gravação do resultado não depender de regerar a lista."""
    itens = itens_da_revisao(registros, com_a_corrida_20=com_a_corrida_20, semente=semente)
    pasta.mkdir(parents=True, exist_ok=True)
    saida.write_text(pagina(itens), encoding="utf-8", newline="\n")
    (pasta / ARQ_PLANILHA).write_text(planilha(itens), encoding="utf-8", newline="\n")
    (pasta / ARQ_CHAVE).write_text(json.dumps({"semente": semente, "com_a_corrida_20": com_a_corrida_20, "gerado_em": dt.datetime.now().isoformat(timespec="seconds"), "itens": itens},
                                              ensure_ascii=False, indent=1), encoding="utf-8")
    return [saida, pasta / ARQ_PLANILHA, pasta / ARQ_CHAVE]


def _pasta_da_corrida() -> Path:
    return caminhos.fase3(CORRIDA)["raiz"]


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Revisão humana às cegas das propostas de edição da corrida 27 (medida M2), com as edições da corrida 20 misturadas.")
    ap.add_argument("--gerar", action="store_true", help="gera a página, a planilha às cegas e a chave da origem")
    ap.add_argument("--sem-a-corrida-20", action="store_true", help="com --gerar: só as propostas da corrida 27 (a comparação passa a usar a revisão do lote da corrida 20)")
    ap.add_argument("--saida", type=Path, default=SAIDA, help=f"o HTML gerado (padrão: {SAIDA.relative_to(RAIZ)})")
    ap.add_argument("--gravar", nargs="?", const="", default=None, help="arquivo JSON com as respostas lidas do banco da página (ou sem valor, com --da-planilha)")
    ap.add_argument("--da-planilha", action="store_true", help="com --gravar: lê os vereditos da planilha às cegas preenchida")
    ap.add_argument("--quem", default=None, help="com --gravar: quem revisou, como o Eric disse; obrigatório, sem valor padrão")
    ap.add_argument("--estado", action="store_true", help="quantas propostas têm veredito gravado")
    ap.add_argument("--pasta", type=Path, default=None, help=f"pasta da corrida (padrão: resultados_alvo/{CORRIDA})")
    args = ap.parse_args(argv)
    pasta = args.pasta or _pasta_da_corrida()
    if args.gerar:
        registros = executar_bateria.ler_jsonl(pasta / executar_fase3._slug(ea.MODELO) / ea.NOME_DO_REGISTRO)
        if not registros:
            print(f"sem os registros da corrida 27 em {pasta}: a revisão só é gerada depois de a corrida rodar")
            return 2
        escritos = gerar(registros, pasta, args.saida, com_a_corrida_20=not args.sem_a_corrida_20)
        chave = json.loads((pasta / ARQ_CHAVE).read_text(encoding="utf-8"))
        origens = [i["origem"] for i in chave["itens"]]
        print(f"{len(origens)} itens para revisar: {origens.count('27')} da corrida 27 e {origens.count('20')} da corrida 20; gravados: {', '.join(p.name for p in escritos)}")
        if not origens.count("27"):
            print("nenhuma proposta da corrida 27 passou nos filtros de hoje: não há o que comparar na revisão humana, e a leitura da parcela correta fica sem veredito")
        return 0
    if args.gravar is not None:
        if not str(args.quem or "").strip():
            print("falta --quem: diga quem revisou, como o Eric informou; a ferramenta não grava a revisão sem isso")
            return 2
        arq_chave = pasta / ARQ_CHAVE
        if not arq_chave.exists():
            print(f"sem a chave em {arq_chave}: rode --gerar antes")
            return 2
        itens = json.loads(arq_chave.read_text(encoding="utf-8"))["itens"]
        if args.da_planilha:
            respostas = vereditos_da_planilha((pasta / ARQ_PLANILHA).read_text(encoding="utf-8"))
        elif args.gravar:
            respostas = json.loads(Path(args.gravar).read_text(encoding="utf-8"))
        else:
            print("informe o arquivo das respostas da página ou --da-planilha")
            return 2
        revisao = montar_revisao(itens, respostas, args.quem)
        (pasta / ARQ_REVISAO).write_text(json.dumps(revisao, ensure_ascii=False, indent=1), encoding="utf-8")
        (pasta / ARQ_PLANILHA_FINAL).write_text(planilha_final(itens, revisao), encoding="utf-8", newline="\n")
        print(f"revisão gravada em {ARQ_REVISAO} e {ARQ_PLANILHA_FINAL}: {revisao['respondidas']} de {revisao['itens_na_revisao']} itens com veredito; "
              "rode avaliar_fase4.py --analista de novo para a leitura da parcela correta")
        return 0
    if args.estado:
        revisao = ea.ler_revisao(pasta)
        if not revisao:
            print("a revisão ainda não foi gravada")
            return 0
        print(f"{revisao['respondidas']} de {revisao['itens_na_revisao']} itens com veredito; quem revisou: {revisao['quem']}")
        return 0
    ap.error("informe --gerar, --gravar ou --estado")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
