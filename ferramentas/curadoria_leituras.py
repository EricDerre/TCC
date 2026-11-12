#!/usr/bin/env python3
# ! Alteração de IA - Revisar: módulo novo (10/11/2026, Pós-Fase 4): a página de curadoria das leituras dos verbetes e a aplicação das respostas dela.
# `--gerar` monta Documentacao/dashboard/curadoria-leituras.html com uma leitura por vez: o corpo da leitura num campo editável, a prévia dela, o verbete
# original (o que o modelo lê, só para consulta) e o que os filtros de texto do pacote Q2 acusam naquela leitura (filtros_de_texto.medir e avaliar com
# resultados_alvo/fase4/limiares_texto.json); três respostas por leitura (aprovada como está, editada, adiada), guardadas no banco da própria página.
# `--aplicar respostas.json` passa cada resposta ao arquivo em biblioteca_producao_leitura/: o corpo editado (ou o mesmo), `curado: sim` no cabeçalho e a
# nota na seção Curadoria; recusa leitura já curada (sem --corrigir), corpo que mudou desde a página e resposta sem texto; `--estado` conta o que falta.
# ! Motivo: a curadoria das 39 leituras é do Eric desde o pacote Q1 (07/11/2026) e estava parada, porque abrir 39 arquivos à mão e trocar o cabeçalho é
# moroso; ele pediu uma página ("uma interfacezinha"), como a da sessão de revisão. O gerador de biblioteca_leitura.py nunca regrava um arquivo com
# `curado: sim`, então o que a página aplica fica, e `--check` continua conferindo o cabeçalho contra o verbete.
"""Uso:
  python ferramentas/curadoria_leituras.py --gerar [--saida <html>]                 gera a página da curadoria
  python ferramentas/curadoria_leituras.py --aplicar respostas.json [--corrigir]    aplica as respostas lidas do banco da página aos arquivos
  python ferramentas/curadoria_leituras.py --estado                                 quantas leituras estão curadas e quais faltam
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
EXP = RAIZ / "Programacao" / "AgenteCore" / "experimentos"
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(EXP))
import biblioteca as bib
import biblioteca_leitura as bl
import filtros_de_texto as ft
import painel_topicos as tp

SAIDA = RAIZ / "Documentacao" / "dashboard" / "curadoria-leituras.html"
PASTA_SESSAO = EXP / "resultados_alvo" / "fase4" / "curadoria_leituras"
ESTADOS = ("aprovada", "editada", "adiada")
SECAO_CURADORIA = "## Curadoria"
# ! Alteração de IA - Revisar: (10/11/2026) quem curou e os consertos: QUEM_PADRAO é o que a nota da seção Curadoria diz quando ninguém informa outro autor, e
# ARQ_CONSERTOS_MD é o caminho, a partir da raiz do repositório, da lista dos consertos que a nota e o cabeçalho de cada leitura consertada citam.
# ! Motivo: na curadoria de 10/11/2026 as respostas vieram de um analista e foram coladas pelo Eric, e 26 textos precisaram de consertos do Claude; a nota
# gravada em cada arquivo dizia sempre "pelo Eric", o que não era o que tinha acontecido.
QUEM_PADRAO = "pelo Eric"
ARQ_CONSERTOS_MD = "Programacao/AgenteCore/experimentos/resultados_alvo/fase4/curadoria_leituras/consertos.md"
# O nome de cada métrica dos filtros, para a página dizer o que acusou sem a chave em código.
NOME_DA_METRICA = {"palavras_por_frase_media": "palavras por frase, na média", "palavras_por_frase_max": "palavras na frase mais longa",
                   "preenchimento_razao": "palavras de preenchimento", "repeticao_razao": "repetição interna (trigramas repetidos)", "compressao": "compressão (palavras repetidas)",
                   "termos_sem_expansao_n": "termos técnicos sem o significado na primeira menção", "flesch": "Flesch adaptado (só alarme, abaixo de 50)",
                   "densidade_dominio": "densidade de termos do domínio (só comparação)"}


def separar(texto: str) -> tuple[str, str]:
    """O cabeçalho (do primeiro `---` ao `---` de fechamento, com a quebra de linha) e o corpo; cabeçalho mais corpo recompõem o arquivo."""
    if not texto.startswith("---"):
        raise ValueError("arquivo não começa com '---'")
    fim = texto.find("\n---", 3)
    if fim < 0:
        raise ValueError("cabeçalho sem '---' de fechamento")
    corte = fim + 4
    if texto[corte:corte + 1] == "\n":
        corte += 1
    return texto[:corte], texto[corte:]


def _filtros(corpo: str, limiares: dict) -> tuple[dict, dict]:
    med = ft.medir(corpo)
    av = ft.avaliar(med, limiares)
    chaves = [m["chave"] for m in ft.METRICAS]
    return med, {"aprovado": av["aprovado"], "falhas": [ch for ch, c in av["criterios"].items() if c["passa"] is False], "termos_sem_expansao": av["termos_sem_expansao"],
                 "alarme_flesch": av["alarme_flesch"], "preenchimentos": med["preenchimentos"], "medidas": {ch: med.get(ch) for ch in chaves},
                 "limiares": {ch: (limiares["limiares"].get(ch) or {}).get("valor") for ch in chaves}, "flesch": med.get("flesch")}


def itens(raiz_bib: Path = bl.PASTA_BIBLIOTECA, raiz_leitura: Path = bl.PASTA_LEITURA, limiares: dict | None = None) -> list[dict]:
    """Uma entrada por leitura, em ordem de id: o caminho, o título, se já está curada, o corpo (o que o campo editável mostra) e a sua marca, o corpo
    do verbete original (sem o cabeçalho) e o que os filtros de texto acusam no corpo da leitura."""
    raiz_bib, raiz_leitura = Path(raiz_bib), Path(raiz_leitura)
    limiares = limiares or ft.carregar_limiares(ft.ARQ_LIMIARES)
    verbetes = {v["id"]: v for v in bib.carregar(raiz_bib)}
    saida = []
    for vid, l in sorted(bl.carregar(raiz_leitura).items()):
        texto = (raiz_leitura / l["caminho"]).read_text(encoding="utf-8")
        _, corpo = separar(texto)
        v = verbetes.get(vid)
        verbete_corpo = bib._parse_frontmatter(Path(v["caminho"]).read_text(encoding="utf-8"))[1] if v else ""
        _, filtros = _filtros(corpo, limiares)
        saida.append({"id": vid, "caminho": l["caminho"], "titulo": l["titulo"], "tipo": l.get("tipo") or "", "curado": bool(l["curado"]), "corpo": corpo,
                      "corpo_sha": ft.sha16(corpo), "verbete_corpo": verbete_corpo, "filtros": filtros})
    return saida


CSS = """
:root{--bg:#f6f4ee;--bg2:#fdfcf9;--ink:#1f2328;--ink2:#4c545c;--linha:#d8d3c7;--acento:#2f5d8a;--acento2:#dbe7f3;--bom:#2e7d4f;--meio:#b7791f;--ruim:#b3392b;
--fd:"Source Serif 4",Georgia,serif;--fb:"IBM Plex Sans","Segoe UI",Roboto,Arial,sans-serif;--fm:"IBM Plex Mono",Consolas,monospace}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){color-scheme:dark;--bg:#15181c;--bg2:#1d2126;--ink:#e8e6df;--ink2:#a8adb4;--linha:#333a42;--acento:#7fb0e0;--acento2:#243342;--bom:#5cc48a;--meio:#e0a84a;--ruim:#e46b5c}}
:root[data-theme=dark]{color-scheme:dark;--bg:#15181c;--bg2:#1d2126;--ink:#e8e6df;--ink2:#a8adb4;--linha:#333a42;--acento:#7fb0e0;--acento2:#243342;--bom:#5cc48a;--meio:#e0a84a;--ruim:#e46b5c}
body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 var(--fb)}
.topo{padding:14px 16px 8px;border-bottom:1px solid var(--linha);background:var(--bg2)}
.olho{margin:0;font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:var(--ink2)}
h1{margin:4px 0 8px;font:600 22px/1.25 var(--fd)}
.trilho{display:flex;flex-wrap:wrap;gap:4px;align-items:center}
.trilho ol{display:flex;flex-wrap:wrap;gap:4px;margin:0;padding:0;list-style:none}
.pip{min-width:30px;padding:2px 6px;border:1px solid var(--linha);border-radius:12px;background:var(--bg2);color:var(--ink2);font:12px var(--fm);cursor:pointer}
.pip.atual{outline:2px solid var(--acento)}.pip.feita{background:var(--bom);color:#fff;border-color:var(--bom)}.pip.adiada{background:var(--meio);color:#fff;border-color:var(--meio)}
.pip.curada{background:var(--acento);color:#fff;border-color:var(--acento)}
.contagem{margin-left:8px;font-size:13px;color:var(--ink2)}
.aviso{margin:8px 16px 0;padding:8px 12px;border-left:3px solid var(--meio);background:var(--acento2);border-radius:0 6px 6px 0;font-size:14px}
main{padding:12px 16px 40px;max-width:1500px;margin:0 auto}
.bloco{max-width:820px}
.bloco ol{padding-left:22px}
button{font:inherit;padding:8px 14px;border-radius:8px;border:1px solid var(--linha);background:var(--bg2);color:var(--ink);cursor:pointer}
button.primario{background:var(--acento);color:#fff;border-color:var(--acento)}button.bom{background:var(--bom);color:#fff;border-color:var(--bom)}
button.discreto{background:transparent}button[disabled]{opacity:.45;cursor:not-allowed}
.item h2{margin:6px 0 2px;font:600 20px/1.3 var(--fd)}
.meta{color:var(--ink2);font-size:13px;margin:0 0 8px}.meta code{font:12px var(--fm)}
.marca{display:inline-block;padding:1px 8px;border-radius:10px;font-size:12px;background:var(--acento2);color:var(--ink)}
.marca.feita{background:var(--bom);color:#fff}.marca.adiada{background:var(--meio);color:#fff}.marca.curada{background:var(--acento);color:#fff}
.colunas{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,1fr);gap:16px}
@media (max-width:980px){.colunas{grid-template-columns:1fr}}
textarea#texto{width:100%;box-sizing:border-box;min-height:62vh;padding:10px;border:1px solid var(--linha);border-radius:8px;background:var(--bg2);color:var(--ink);font:13px/1.45 var(--fm);resize:vertical}
.filtros{padding:10px 12px;border:1px solid var(--linha);border-radius:8px;background:var(--bg2);font-size:14px}
.filtros h3,details h3{margin:0 0 6px;font:600 15px var(--fb)}
.filtros ul{margin:4px 0 0;padding-left:20px}.filtros .ok{color:var(--bom)}.filtros .ruim{color:var(--ruim)}
details{margin-top:10px;border:1px solid var(--linha);border-radius:8px;background:var(--bg2);padding:6px 12px}
details summary{cursor:pointer;font-weight:600}
.previa{font-size:14px;max-width:none}.previa h1{font-size:18px}.previa h2{font-size:16px;margin:12px 0 4px}.previa code{font:12px var(--fm);background:var(--acento2);padding:0 3px;border-radius:3px}
.previa table{border-collapse:collapse;font-size:13px}.previa td,.previa th{border:1px solid var(--linha);padding:3px 6px;text-align:left}
.previa blockquote{margin:6px 0;padding:2px 10px;border-left:3px solid var(--linha);color:var(--ink2)}
.acoes{display:flex;flex-wrap:wrap;gap:8px;margin:12px 0}
.mensagem{min-height:1.2em;color:var(--ruim);font-size:14px}
.fim table{border-collapse:collapse;font-size:13px;margin-top:8px}.fim td,.fim th{border:1px solid var(--linha);padding:3px 8px;text-align:left}
.nota{color:var(--ink2);font-size:13px}
.copia textarea{width:100%;box-sizing:border-box;font:12px var(--fm)}
"""

CORPO = """
<header class="topo">
  <p class="olho">Pós-Fase 4, camada de leitura dos verbetes, curadoria</p>
  <h1>Curadoria das leituras dos verbetes</h1>
  <nav class="trilho" aria-label="Leituras">
    <ol id="trilho-lista">@@PIPS@@</ol>
    <span id="contagem" class="contagem">0 de @@TOTAL@@ curadas</span>
  </nav>
</header>
<div id="aviso" class="aviso" role="status" hidden><span id="aviso-texto"></span></div>
<main>
  <section id="inicio" class="bloco">
    <p>São @@TOTAL@@ leituras, uma por verbete da biblioteca de produção, geradas por código a partir do verbete e nunca lidas pelo modelo: é o que o analista lê no relatório e na árvore. Nenhuma foi curada ainda. Dá para parar a qualquer momento: o que está respondido fica guardado nesta página.</p>
    <ol>
      <li><strong>Leia a leitura</strong> no campo à esquerda (é o texto do arquivo, em Markdown; a prévia renderizada e o verbete original ficam à direita, só para consulta).</li>
      <li><strong>Veja o que os filtros acusam</strong>: as oito medidas do pacote Q2 contra os limiares calibrados no corpus deste repositório. Um termo técnico sem o significado na primeira menção é o que mais reprova.</li>
      <li><strong>Responda</strong>: <em>Aprovar como está</em> (o arquivo fica igual, só com <code>curado: sim</code>), <em>Salvar com a mudança</em> (o texto do campo substitui o corpo do arquivo) ou <em>Deixar para depois</em>.</li>
      <li><strong>O Claude aplica</strong> as respostas aos arquivos de <code>biblioteca_producao_leitura/</code> quando você terminar, e remede os filtros.</li>
    </ol>
    <p class="nota">O cabeçalho do arquivo (os campos copiados do verbete) não é editado aqui: ele tem de bater com o verbete, e o <code>--check</code> confere isso.</p>
    <button type="button" id="comecar" class="primario">Começar pela primeira leitura em aberto</button>
  </section>
  <section id="item" class="item" hidden>
    <h2 id="item-titulo"></h2>
    <p class="meta"><code id="item-caminho"></code> · <span id="item-tipo"></span> · <span id="item-marca" class="marca"></span></p>
    <div class="colunas">
      <div>
        <label for="texto"><strong>Leitura (edite aqui, em Markdown)</strong></label>
        <textarea id="texto" spellcheck="true"></textarea>
        <div class="acoes">
          <button type="button" id="aprovar" class="bom">Aprovar como está</button>
          <button type="button" id="salvar" class="primario" disabled>Salvar com a mudança</button>
          <button type="button" id="adiar">Deixar para depois</button>
          <button type="button" id="restaurar" class="discreto" disabled>Voltar ao texto gerado</button>
        </div>
        <p id="mensagem" class="mensagem" role="alert"></p>
        <div class="acoes">
          <button type="button" id="anterior" class="discreto">Anterior</button>
          <button type="button" id="proxima" class="discreto">Próxima em aberto</button>
        </div>
      </div>
      <div>
        <div id="filtros" class="filtros"></div>
        <details open><summary>Prévia da leitura gerada (como estava ao gerar a página)</summary><div id="previa" class="previa"></div></details>
        <details><summary>Verbete original (o que o modelo lê; não muda)</summary><div id="verbete" class="previa"></div></details>
      </div>
    </div>
  </section>
  <section id="fim" class="fim" hidden>
    <h2>Todas as leituras têm resposta</h2>
    <p>Avise o Claude: ele lê as respostas do banco desta página, aplica aos arquivos e remede os filtros. Para corrigir uma resposta, clique no número dela acima.</p>
    <table><thead><tr><th>Leitura</th><th>Resposta</th><th>Quando</th></tr></thead><tbody id="fim-linhas"></tbody></table>
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
  const NOMES = JSON.parse(document.getElementById("nomes").textContent);
  const CHAVE = "curadoria_leituras_v1";
  const $ = (id) => document.getElementById(id);
  let banco = null, semBanco = false, carregou = false, salvas = {}, atual = -1, gravando = false;
  const local = lerLocal();

  function lerLocal() {
    try { const v = JSON.parse(localStorage.getItem(CHAVE) || "{}"); return {atual: v.atual == null ? -1 : v.atual, rascunhos: v.rascunhos || {}, respostas: v.respostas || {}}; }
    catch (e) { return {atual: -1, rascunhos: {}, respostas: {}}; }
  }
  function guardarLocal() { try { localStorage.setItem(CHAVE, JSON.stringify(local)); } catch (e) {} }
  const fmt = (v) => v == null ? "n/d" : (Number.isInteger(v) ? String(v) : String(Math.round(v * 1000) / 1000).replace(".", ","));
  const resposta = (id) => salvas[id] || local.respostas[id] || null;
  const feita = (i) => { const r = resposta(ITENS[i].id); return ITENS[i].curado || (r && (r.estado === "aprovada" || r.estado === "editada")); };
  const respondida = (i) => ITENS[i].curado || !!resposta(ITENS[i].id);
  const estadoDe = (i) => ITENS[i].curado ? "curada" : (resposta(ITENS[i].id) || {}).estado || "";

  function aviso(texto) { $("aviso-texto").textContent = texto || ""; $("aviso").hidden = !texto; }

  function pips() {
    ITENS.forEach((x, i) => {
      const b = $("pip-" + i);
      b.className = "pip" + (i === atual ? " atual" : "") + (ITENS[i].curado ? " curada" : feita(i) ? " feita" : estadoDe(i) === "adiada" ? " adiada" : "");
      b.title = x.id + (estadoDe(i) ? " (" + estadoDe(i) + ")" : "");
    });
    const n = ITENS.filter((_, i) => feita(i)).length;
    $("contagem").textContent = n + " de " + ITENS.length + " curadas" + (ITENS.some((_, i) => estadoDe(i) === "adiada") ? " (" + ITENS.filter((_, i) => estadoDe(i) === "adiada").length + " adiadas)" : "");
  }

  function proximaEmAberto(desde) {
    for (let k = 1; k <= ITENS.length; k++) { const j = (desde + k) % ITENS.length; if (!respondida(j)) return j; }
    for (let k = 1; k <= ITENS.length; k++) { const j = (desde + k) % ITENS.length; if (!feita(j)) return j; }
    return -1;
  }

  function filtrosHtml(f) {
    const ul = document.createElement("ul");
    Object.keys(f.medidas).forEach((ch) => {
      const li = document.createElement("li");
      const lim = f.limiares[ch];
      const ruim = f.falhas.includes(ch);
      li.className = ruim ? "ruim" : (lim == null ? "" : "ok");
      li.textContent = (NOMES[ch] || ch) + ": " + fmt(f.medidas[ch]) + (lim == null ? "" : " (limite " + fmt(lim) + ")") + (ruim ? " reprova" : "");
      ul.appendChild(li);
    });
    const box = document.createElement("div");
    const h = document.createElement("h3");
    h.textContent = f.aprovado ? "Os filtros aprovam esta leitura" : "Os filtros reprovam esta leitura";
    h.className = f.aprovado ? "ok" : "ruim";
    box.appendChild(h);
    if (f.termos_sem_expansao.length) {
      const p = document.createElement("p");
      p.textContent = "Termos sem o significado na primeira menção: " + f.termos_sem_expansao.join(", ") + ". Escreva o significado na primeira vez que o termo aparece, ou troque o termo.";
      box.appendChild(p);
    }
    const pre = Object.keys(f.preenchimentos || {});
    if (pre.length) { const p = document.createElement("p"); p.textContent = "Palavras de preenchimento: " + pre.map((t) => t + " (" + f.preenchimentos[t] + ")").join(", ") + "."; box.appendChild(p); }
    if (f.alarme_flesch) { const p = document.createElement("p"); p.textContent = "Alarme do Flesch (" + fmt(f.flesch) + "): frases longas ou palavras longas; não reprova sozinho."; box.appendChild(p); }
    box.appendChild(ul);
    const nota = document.createElement("p");
    nota.className = "nota";
    nota.textContent = "Medido no texto gerado, ao montar a página; o Claude remede depois de aplicar o que você salvar.";
    box.appendChild(nota);
    return box;
  }

  function mostrar(i) {
    atual = i; local.atual = i; guardarLocal();
    const x = ITENS[i], r = resposta(x.id);
    $("inicio").hidden = true; $("fim").hidden = true; $("item").hidden = false;
    $("item-titulo").textContent = (i + 1) + " de " + ITENS.length + ": " + x.titulo;
    $("item-caminho").textContent = "biblioteca_producao_leitura/" + x.caminho;
    $("item-tipo").textContent = x.tipo || "";
    const marca = $("item-marca");
    const est = estadoDe(i);
    marca.textContent = est === "curada" ? "já curada no arquivo" : est === "aprovada" ? "aprovada como está" : est === "editada" ? "editada e salva" : est === "adiada" ? "deixada para depois" : "sem resposta";
    marca.className = "marca" + (est === "curada" ? " curada" : est === "aprovada" || est === "editada" ? " feita" : est === "adiada" ? " adiada" : "");
    const texto = (r && r.estado === "editada" && r.texto != null) ? r.texto : (local.rascunhos[x.id] != null ? local.rascunhos[x.id] : x.corpo);
    $("texto").value = texto;
    $("filtros").replaceChildren(filtrosHtml(x.filtros));
    $("previa").replaceChildren(document.getElementById("prev-" + i).content.cloneNode(true));
    $("verbete").replaceChildren(document.getElementById("verb-" + i).content.cloneNode(true));
    $("mensagem").textContent = "";
    botoes();
    pips();
    window.scrollTo({top: 0});
  }

  function botoes() {
    const x = ITENS[atual];
    const mudou = $("texto").value !== x.corpo;
    $("salvar").disabled = gravando || !mudou || x.curado;
    $("aprovar").disabled = gravando || x.curado;
    $("adiar").disabled = gravando || x.curado;
    $("restaurar").disabled = !mudou;
    $("anterior").disabled = atual <= 0;
  }

  async function gravar(doc) {
    if (!banco) { local.respostas[doc.id] = doc; guardarLocal(); return "local"; }
    const ref = banco.collection("curadoria").doc(doc.id);
    try { await ref.set(doc); }
    catch (e) {
      if (!e || e.code !== "unavailable") throw e;
      await new Promise((ok) => setTimeout(ok, 500 + Math.random() * 800));
      await ref.set(doc);
    }
    salvas[doc.id] = doc;
    return "banco";
  }

  async function responder(estado) {
    const x = ITENS[atual];
    const valor = $("texto").value;
    if (estado === "editada" && !valor.trim()) { $("mensagem").textContent = "O texto está vazio."; return; }
    const anterior = resposta(x.id);
    const agora = new Date().toISOString();
    const doc = {id: x.id, caminho: x.caminho, estado: estado, corpo_sha: x.corpo_sha, texto: estado === "editada" ? valor : null, editado: estado === "editada",
                 salvo_em: anterior && anterior.salvo_em ? anterior.salvo_em : agora, editado_em: anterior ? agora : null};
    gravando = true; botoes();
    try {
      const onde = await gravar(doc);
      if (estado !== "editada") delete local.rascunhos[x.id]; guardarLocal();
      $("mensagem").textContent = "";
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
      [x.id, x.curado ? "já curada no arquivo" : (r ? r.estado : "sem resposta"), r && r.salvo_em ? r.salvo_em.replace("T", " ").slice(0, 16) : ""].forEach((v) => { const td = document.createElement("td"); td.textContent = v; tr.appendChild(td); });
      const td = document.createElement("td");
      const b = document.createElement("button"); b.type = "button"; b.className = "discreto"; b.textContent = "Corrigir"; b.dataset.i = String(i); td.appendChild(b); tr.appendChild(td);
      tb.appendChild(tr);
    });
    const todas = ITENS.map((x) => resposta(x.id)).filter(Boolean);
    $("respostas-texto").value = JSON.stringify(todas, null, 1);
    pips();
    window.scrollTo({top: 0});
  }

  $("comecar").addEventListener("click", () => { const j = proximaEmAberto(-1); if (j < 0) fim(); else mostrar(j); });
  $("aprovar").addEventListener("click", () => responder("aprovada"));
  $("salvar").addEventListener("click", () => responder("editada"));
  $("adiar").addEventListener("click", () => responder("adiada"));
  $("restaurar").addEventListener("click", () => { $("texto").value = ITENS[atual].corpo; delete local.rascunhos[ITENS[atual].id]; guardarLocal(); botoes(); });
  $("anterior").addEventListener("click", () => { if (atual > 0) mostrar(atual - 1); });
  $("proxima").addEventListener("click", () => { const j = proximaEmAberto(atual); if (j < 0) fim(); else mostrar(j); });
  $("texto").addEventListener("input", () => { const x = ITENS[atual]; if ($("texto").value !== x.corpo) local.rascunhos[x.id] = $("texto").value; else delete local.rascunhos[x.id]; guardarLocal(); botoes(); });
  $("trilho-lista").addEventListener("click", (ev) => { const b = ev.target.closest("button[data-i]"); if (b) mostrar(Number(b.dataset.i)); });
  $("fim-linhas").addEventListener("click", (ev) => { const b = ev.target.closest("button[data-i]"); if (b) mostrar(Number(b.dataset.i)); });
  $("copiar").addEventListener("click", () => {
    const t = $("respostas-texto");
    const escolher = () => { t.focus(); t.select(); $("copia-status").textContent = "Selecionei o texto: use Ctrl+C."; };
    if (!navigator.clipboard) { escolher(); return; }
    navigator.clipboard.writeText(t.value).then(() => { $("copia-status").textContent = "Copiado."; }, escolher);
  });

  function semOBanco(motivo) { banco = null; semBanco = true; aviso("Sem o banco da página" + (motivo ? " (" + motivo + ")" : "") + ": as respostas ficam só neste navegador. No fim, use Copiar as respostas."); pips(); }

  (async () => {
    pips();
    let db = null;
    try { db = window.claude ? await window.claude.use("db") : null; } catch (e) { db = null; }
    if (!db) { semOBanco(""); return; }
    banco = db;
    const relogio = setTimeout(() => { if (!carregou) aviso("O banco da página ainda não respondeu; o que você gravar fica à espera dele."); }, 10000);
    banco.collection("curadoria").onSnapshot((foto) => {
      const novo = {};
      foto.docs.forEach((d) => { if (d.exists) novo[d.id] = d.data(); });
      salvas = novo;
      if (!foto.metadata.fromCache) { carregou = true; clearTimeout(relogio); aviso(""); }
      if (atual >= 0 && !$("item").hidden) { const x = ITENS[atual]; const r = resposta(x.id); if (r && r.estado === "editada" && r.texto != null && local.rascunhos[x.id] == null) $("texto").value = r.texto; botoes(); }
      pips();
    }, (e) => { clearTimeout(relogio); semOBanco(e && e.code); });
  })();
})();
"""


def pagina(itens_: list[dict]) -> str:
    """A página da curadoria: os itens em JSON (sem o verbete), a prévia e o verbete de cada um em templates, a folha de estilo e o script."""
    dados = [{k: v for k, v in x.items() if k != "verbete_corpo"} for x in itens_]
    moldes = []
    for i, x in enumerate(itens_):
        moldes.append(f'<template id="prev-{i}">{tp._relatorio_para_html(x["corpo"])}</template>')
        moldes.append(f'<template id="verb-{i}">{tp._relatorio_para_html(x["verbete_corpo"]) if x["verbete_corpo"] else "<p>Verbete não encontrado na biblioteca.</p>"}</template>')
    pips = "".join(f'<li><button type="button" class="pip" id="pip-{i}" data-i="{i}">{i + 1}</button></li>' for i in range(len(itens_)))
    corpo = CORPO.replace("@@TOTAL@@", str(len(itens_))).replace("@@PIPS@@", pips)
    seguro = lambda obj: json.dumps(obj, ensure_ascii=False).replace("<", "\\u003c")
    return ("<title>Curadoria das leituras dos verbetes</title>\n"
            '<meta name="claude:viewport-fit-sides" content="cover">\n'
            "<!-- ! Alteração de IA - Revisar: página gerada por ferramentas/curadoria_leituras.py --gerar para a curadoria das leituras dos verbetes (Pós-Fase 4, camada de leitura, decisão 103).\n"
            "     ! Motivo: a curadoria é do Eric e ele pediu uma página, como a da sessão de revisão; o texto de cada leitura, a prévia, o verbete original e o que os filtros acusam vêm dos arquivos "
            "do repositório, e as respostas ficam no banco da própria página até o Claude aplicá-las aos arquivos. -->\n"
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Source+Serif+4:wght@600&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">\n'
            f"<style>{CSS}</style>\n{corpo}\n" + "\n".join(moldes) +
            f'\n<script type="application/json" id="itens">{seguro(dados)}</script>\n<script type="application/json" id="nomes">{seguro(NOME_DA_METRICA)}</script>\n<script>{JS}</script>\n')


def _normalizar(texto: str) -> str:
    texto = texto.replace("\r\n", "\n").replace("\r", "\n").rstrip() + "\n"
    return texto


def _anotar_curadoria(corpo: str, nota: str) -> str:
    """Põe a nota na seção Curadoria da leitura: no lugar do texto padrão do gerador, ou no fim da seção quando o Eric já escreveu algo nela."""
    if bl.TEXTO_DA_CURADORIA in corpo:
        return corpo.replace(bl.TEXTO_DA_CURADORIA, nota, 1)
    if SECAO_CURADORIA not in corpo:
        return corpo.rstrip("\n") + f"\n\n{SECAO_CURADORIA}\n\n{nota}\n"
    return corpo.rstrip("\n") + f"\n\n{nota}\n"


# ! Alteração de IA - Revisar: (10/11/2026) `_aplicar_consertos`, `_marcar_consertos` e `render_consertos`, e os parâmetros `consertos` e `quem` de `aplicar`: cada
# conserto troca um trecho que ocorre uma vez só no texto salvo na página (com o motivo obrigatório); o cabeçalho da leitura ganha a tag com os motivos; a nota da
# seção Curadoria diz quem curou e quantos consertos houve; e a lista de todas as trocas, com o antes e o depois, sai em Markdown.
# ! Motivo: o texto que o analista escreveu para 26 leituras trazia frases erradas sobre o projeto (busca vetorial, épocas de treinamento), uma linha colada na
# seguinte, uma mensagem literal da API alterada e termos ainda sem explicação; o Eric escolheu no quadro da sessão aplicar a curadoria com consertos, vendo cada
# troca. Um conserto que não acha o trecho exatamente uma vez não grava nada, para nenhuma troca acontecer no lugar errado.
def _aplicar_consertos(texto: str, lista: list[dict]) -> tuple[str, list[str]]:
    erros = []
    for i, c in enumerate(lista, 1):
        antigo, novo, motivo = c.get("antigo"), c.get("novo"), (c.get("motivo") or "").strip()
        if not antigo or novo is None or not motivo:
            erros.append(f"conserto {i} sem trecho antigo, trecho novo ou motivo")
            continue
        n = texto.count(antigo)
        if n != 1:
            erros.append(f"conserto {i}: o trecho {antigo[:60]!r} " + ("não aparece no texto salvo" if n == 0 else f"aparece {n} vezes no texto salvo"))
            continue
        texto = texto.replace(antigo, novo, 1)
    return texto, erros


def _plural(n: int, um: str, varios: str) -> str:
    return f"{n} {um if n == 1 else varios}"


def _marcar_consertos(cab: str, lista: list[dict], data: str) -> str:
    """Acrescenta ao cabeçalho da leitura, logo depois da tag do gerador, a tag dos consertos com os motivos (sem repetir motivo igual)."""
    motivos = list(dict.fromkeys(c["motivo"].strip().rstrip(".") for c in lista))
    tag = (f"# ! Alteração de IA - Revisar: ({data}) {_plural(len(lista), 'conserto', 'consertos')} do Claude no texto que o analista escreveu na curadoria desta leitura; "
           f"o antes e o depois de cada troca estão em {ARQ_CONSERTOS_MD}.\n# ! Motivo: {'; '.join(motivos)}.\n")
    linhas = cab.split("\n")
    alvo = next((i for i, l in enumerate(linhas) if l.startswith("# ! Motivo:")), 0)
    return "\n".join(linhas[:alvo + 1]) + "\n" + tag + "\n".join(linhas[alvo + 1:])


def render_consertos(consertos: dict[str, list[dict]], hoje: str | None = None) -> str:
    """A lista dos consertos em Markdown: por leitura, cada troca com o motivo, o trecho de antes e o de depois."""
    hoje = hoje or dt.date.today().isoformat()
    data = f"{hoje[8:10]}/{hoje[5:7]}/{hoje[0:4]}"
    total = sum(len(v) for v in consertos.values())
    partes = [("<!-- ! Alteração de IA - Revisar: lista DERIVADA dos consertos do Claude nos textos da curadoria das leituras dos verbetes, gerada por "
               "ferramentas/curadoria_leituras.py --aplicar a partir de consertos.json; não editar à mão."),
              ("     ! Motivo: o texto que o analista escreveu na curadoria trazia frases erradas sobre o projeto, formato quebrado e termos sem explicação; o Eric "
               "escolheu aplicar a curadoria com consertos, e cada troca fica aqui com o motivo, o trecho de antes e o de depois, para ele conferir. -->"),
              f"# Consertos do Claude na curadoria das leituras, aplicados em {data}", "",
              (f"{_plural(total, 'conserto', 'consertos')} em {_plural(len(consertos), 'leitura', 'leituras')}. Cada conserto troca um trecho do texto que o analista escreveu e o Eric "
               "colou na página da curadoria; o resto do texto dele ficou como estava. O arquivo de cada leitura está em `Programacao/AgenteCore/biblioteca_producao_leitura/`."), ""]
    for vid in sorted(consertos):
        lista = consertos[vid]
        partes += [f"## `{vid}` ({_plural(len(lista), 'conserto', 'consertos')})", ""]
        for i, c in enumerate(lista, 1):
            partes += [f"{i}. Motivo: {c['motivo'].strip()}", "", "   Antes:", "", "   ~~~text"] + ["   " + l for l in c["antigo"].split("\n")] + ["   ~~~", "", "   Depois:", "", "   ~~~text"]
            partes += ["   " + l for l in c["novo"].split("\n")] + ["   ~~~", ""]
    return "\n".join(partes).rstrip("\n") + "\n"


def aplicar(respostas: list[dict], raiz_leitura: Path = bl.PASTA_LEITURA, raiz_bib: Path = bl.PASTA_BIBLIOTECA, corrigir: bool = False, hoje: str | None = None,
            consertos: dict[str, list[dict]] | None = None, quem: str = QUEM_PADRAO) -> dict:
    """Aplica as respostas da página aos arquivos da camada: aprovada grava `curado: sim` e a nota, editada troca o corpo pelo texto salvo; adiada não toca
    no arquivo. Recusa estado fora da lista, leitura inexistente, leitura já curada (sem `corrigir`), corpo que mudou desde a página e texto vazio.
    `consertos` traz, por leitura editada, as trocas do Claude sobre o texto salvo; `quem` é quem curou, como a nota vai dizer.
    Devolve as contagens, os erros e, por leitura aplicada, o que os filtros acusam no texto final."""
    consertos = consertos or {}
    raiz_leitura, raiz_bib = Path(raiz_leitura), Path(raiz_bib)
    hoje = hoje or dt.date.today().isoformat()
    data = f"{hoje[8:10]}/{hoje[5:7]}/{hoje[0:4]}"
    leituras = bl.carregar(raiz_leitura)
    limiares = ft.carregar_limiares(ft.ARQ_LIMIARES)
    r = {"aprovadas": 0, "editadas": 0, "adiadas": 0, "erros": [], "itens": []}
    for resp in respostas:
        vid, estado = resp.get("id"), resp.get("estado")
        if estado not in ESTADOS:
            r["erros"].append(f"{vid}: estado {estado!r} fora de {ESTADOS}")
            continue
        if estado == "adiada":
            r["adiadas"] += 1
            continue
        l = leituras.get(vid)
        if l is None:
            r["erros"].append(f"{vid}: leitura não existe em {raiz_leitura}")
            continue
        arq = raiz_leitura / l["caminho"]
        cab, corpo = separar(arq.read_text(encoding="utf-8"))
        if "\ncurado: sim\n" in cab and not corrigir:
            r["erros"].append(f"{vid}: já curada (curado: sim no cabeçalho); use --corrigir para trocar")
            continue
        atual = ft.sha16(corpo)
        if resp.get("corpo_sha") != atual:
            r["erros"].append(f"{vid}: o corpo da leitura mudou desde a página (marca da página {resp.get('corpo_sha')}, atual {atual}); regere a página com --gerar")
            continue
        novo = corpo if estado == "aprovada" else _normalizar(resp.get("texto") or "")
        if estado == "editada" and not novo.strip():
            r["erros"].append(f"{vid}: resposta editada sem texto")
            continue
        lista = consertos.get(vid) or []
        if lista and estado != "editada":
            r["erros"].append(f"{vid}: consertos só valem para resposta editada (esta é {estado})")
            continue
        if lista:
            novo, erros_c = _aplicar_consertos(novo, lista)
            if erros_c:
                r["erros"] += [f"{vid}: {e}" for e in erros_c]
                continue
        nota = f"Curada em {data} {quem} na página da curadoria: {'aprovada como estava' if estado == 'aprovada' else 'texto revisado'}."
        if lista:
            nota += f" Depois, {_plural(len(lista), 'conserto', 'consertos')} do Claude neste texto, a pedido do Eric (o que mudou e por quê: `{ARQ_CONSERTOS_MD}`)."
        novo = _anotar_curadoria(novo, nota)
        cab_novo = cab.replace("\ncurado: nao\n", "\ncurado: sim\n", 1)
        if lista:
            cab_novo = _marcar_consertos(cab_novo, lista, data)
        arq.write_text(cab_novo + novo, encoding="utf-8", newline="\n")
        _, filtros = _filtros(novo, limiares)
        r["itens"].append({"id": vid, "caminho": l["caminho"], "estado": estado, "consertos": len(lista),
                           "filtros": {"aprovado": filtros["aprovado"], "falhas": filtros["falhas"], "termos_sem_expansao": filtros["termos_sem_expansao"]}})
        r["aprovadas" if estado == "aprovada" else "editadas"] += 1
    return r


def estado(raiz_leitura: Path = bl.PASTA_LEITURA) -> dict:
    leituras = bl.carregar(Path(raiz_leitura))
    em_aberto = sorted(i for i, l in leituras.items() if not l["curado"])
    return {"total": len(leituras), "curadas": len(leituras) - len(em_aberto), "em_aberto": em_aberto}


def main() -> int:
    ap = argparse.ArgumentParser(description="Página de curadoria das leituras dos verbetes e aplicação das respostas aos arquivos.")
    ap.add_argument("--gerar", action="store_true", help="gera a página da curadoria")
    ap.add_argument("--saida", type=Path, default=SAIDA, help=f"o HTML gerado (padrão: {SAIDA.relative_to(RAIZ)})")
    ap.add_argument("--aplicar", type=Path, help="arquivo JSON com a lista de respostas lidas do banco da página")
    ap.add_argument("--corrigir", action="store_true", help="com --aplicar: troca uma leitura já curada")
    ap.add_argument("--consertos", type=Path, help="com --aplicar: arquivo JSON {id: [{antigo, novo, motivo}]} com as trocas do Claude sobre o texto salvo; grava a lista em .md ao lado")
    ap.add_argument("--quem", default=QUEM_PADRAO, help="com --aplicar: quem curou, como a nota da seção Curadoria vai dizer (padrão: pelo Eric)")
    ap.add_argument("--estado", action="store_true", help="quantas leituras estão curadas e quais faltam")
    ap.add_argument("--raiz", type=Path, default=bl.PASTA_BIBLIOTECA, help="pasta da biblioteca (padrão: biblioteca_producao)")
    ap.add_argument("--destino", type=Path, default=bl.PASTA_LEITURA, help="pasta da camada de leitura (padrão: biblioteca_producao_leitura)")
    args = ap.parse_args()
    if args.aplicar:
        consertos = json.loads(args.consertos.read_text(encoding="utf-8")) if args.consertos else None
        r = aplicar(json.loads(args.aplicar.read_text(encoding="utf-8")), args.destino, args.raiz, corrigir=args.corrigir, consertos=consertos, quem=args.quem)
        if consertos and not r["erros"]:
            args.consertos.with_suffix(".md").write_text(render_consertos(consertos), encoding="utf-8", newline="\n")
            print(f"lista dos consertos: {args.consertos.with_suffix('.md').name} ({sum(len(v) for v in consertos.values())} em {len(consertos)} leituras)")
        for e in r["erros"]:
            print("  erro:", e)
        reprovam = [x["id"] for x in r["itens"] if not x["filtros"]["aprovado"]]
        print(f"aplicadas: {r['aprovadas']} aprovadas e {r['editadas']} editadas; {r['adiadas']} adiadas; {len(r['erros'])} erro(s); "
              f"filtros depois da curadoria: {len(r['itens']) - len(reprovam)} de {len(r['itens'])} aprovadas" + (f" (reprovam: {', '.join(reprovam)})" if reprovam else ""))
        falhas = bl.conferir(args.raiz, args.destino)
        for f in falhas:
            print("  " + f)
        print(f"biblioteca_leitura --check: {'tudo bate' if not falhas else str(len(falhas)) + ' falha(s)'}")
        return 1 if r["erros"] or falhas else 0
    if args.gerar:
        lista = itens(args.raiz, args.destino)
        args.saida.write_text(pagina(lista), encoding="utf-8", newline="\n")
        reprovam = [x["id"] for x in lista if not x["filtros"]["aprovado"]]
        print(f"{args.saida.name}: {len(lista)} leituras ({sum(1 for x in lista if x['curado'])} já curadas; os filtros reprovam {len(reprovam)}), {args.saida.stat().st_size:,} bytes")
        return 0
    if args.estado:
        e = estado(args.destino)
        print(f"{e['curadas']} de {e['total']} leituras curadas; em aberto: {', '.join(e['em_aberto']) or 'nenhuma'}")
        return 0
    ap.error("informe --gerar, --aplicar respostas.json ou --estado")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
