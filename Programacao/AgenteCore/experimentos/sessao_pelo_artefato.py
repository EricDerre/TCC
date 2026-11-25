#!/usr/bin/env python3
# ! Alteração de IA - Revisar: arquivo novo (16/11/2026, Fase 5, decisão 136): a sessão da linha de base manual feita por uma página
# publicada (um artefato do claude.ai por integrante), sem ninguém instalar nada. Três partes. (1) `capturar_material`: roda aqui,
# com as cobaias no ar e sem modelo, cada um dos dez cenários e o treino, e guarda o que o teste e o navegador registraram: nos
# cenários de contrato, a chamada à API (status, tempo e corpo) e a foto da tela; nos de localizador, a foto da tela, o HTML da
# página no passo que quebrou e onde está o elemento do passo. (2) `pagina_da_sessao`: monta a página de um integrante, com o
# tutorial, o botão Começar e a sessão inteira (três perguntas, treino, os dez cenários na ordem sorteada), que grava cada evento
# com a hora do relógio do navegador. (3) `importar_sessao`: traz a sessão gravada pela página para o registro da sessão
# (sessao.jsonl), no mesmo formato dos comandos presenciais, refazendo aqui a conta do corrigido.
# ! Motivo: o Eric decidiu que os integrantes fazem a sessão pelo artefato publicado: tudo o que tem de rodar roda antes, nesta
# máquina, e fica para a pessoa só a parte do diagnóstico. Uma página publicada não alcança as cobaias, o banco nem o navegador
# desta máquina, e abrir a máquina para a internet exporia um site inseguro de propósito num notebook corporativo; com o
# material capturado antes, a página não precisa de nada daqui. O registro sai no formato da versão 2 do protocolo para o comando
# `planilha` e a leitura da Fase 5 (avaliar_fase5.py) lerem as sessões sem mudança.
"""A sessão da linha de base manual pelo artefato publicado (Fase 5, decisão 136): captura do material, página e importação."""
from __future__ import annotations

import base64
import datetime as dt
import json
from pathlib import Path

import cenarios_fase4 as cen
import linha_de_base_manual as lbm

RAIZ = Path(__file__).resolve().parents[3]
PASTA_DO_MATERIAL = "fase5_material"
NOME_DO_MATERIAL = "material.json"
VERSAO_DO_MATERIAL = 1
LARGURA_DA_FOTO, ALTURA_DA_FOTO, QUALIDADE_DA_FOTO = 1100, 720, 55


def arquivo_do_material(pasta: str | Path = PASTA_DO_MATERIAL) -> Path:
    return lbm._pasta(pasta) / NOME_DO_MATERIAL


# ------------------------------------------------------------------ a captura (precisa das cobaias, do banco e do navegador)

# ! Alteração de IA - Revisar: (16/11/2026, decisão 136) `JS_FOTO_DO_HTML`: roda dentro da página do cenário e devolve o HTML dela
# sem script, estilo e comentário (`html`), o mesmo corpo escrito uma linha por elemento, com recuo, para a pessoa ler (`fonte`),
# e o caminho do elemento do passo desde a raiz, como a posição de cada filho (`alvo`). No fim relê o próprio `html` do jeito que
# a página da sessão vai ler e confere que o caminho leva ao mesmo elemento, que o seletor que conserta o acha em primeiro lugar e
# quantos elementos o localizador quebrado acha.
# ! Motivo: a página publicada confere o seletor do integrante contra esta fotografia, e não contra o site. O elemento do passo é
# guardado pela posição na árvore, e não por um atributo posto nele, porque um atributo de marca apareceria no HTML que a pessoa
# lê e seria a resposta. Se a releitura do HTML mudasse a árvore, a página aprovaria ou recusaria o seletor errado: por isso a
# conferência é feita já na captura, e a captura para se ela falhar.
JS_FOTO_DO_HTML = r"""
(p) => {
  const marca = 'data-alvo-da-captura';
  const vivo = p.alvo ? document.querySelector(p.alvo) : null;
  if (p.alvo && !vivo) return {erro: 'o seletor que conserta não achou o elemento do passo na página'};
  if (vivo) vivo.setAttribute(marca, '1');
  const copia = document.documentElement.cloneNode(true);
  if (vivo) vivo.removeAttribute(marca);
  copia.querySelectorAll('script, style, noscript, link, meta, template, iframe, object, embed, base').forEach((e) => e.remove());
  const andador = document.createTreeWalker(copia, NodeFilter.SHOW_COMMENT);
  const comentarios = [];
  while (andador.nextNode()) comentarios.push(andador.currentNode);
  comentarios.forEach((c) => c.remove());
  const alvo = copia.querySelector('[' + marca + ']');
  if (alvo) alvo.removeAttribute(marca);
  const caminho = [];
  for (let no = alvo; no && no !== copia; no = no.parentElement) caminho.unshift(Array.prototype.indexOf.call(no.parentElement.children, no));
  const html = copia.outerHTML;
  const VAZIOS = new Set(['area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'source', 'track', 'wbr']);
  const abre = (el) => '<' + el.tagName.toLowerCase() + Array.from(el.attributes).map((a) => ' ' + a.name + '="' + a.value.replace(/"/g, '&quot;') + '"').join('') + '>';
  const linhas = [];
  const escreve = (no, nivel) => {
    const recuo = '  '.repeat(nivel);
    if (no.nodeType === 3) { const t = no.nodeValue.replace(/\s+/g, ' ').trim(); if (t) linhas.push(recuo + t); return; }
    if (no.nodeType !== 1) return;
    const nome = no.tagName.toLowerCase();
    if (VAZIOS.has(nome)) { linhas.push(recuo + abre(no)); return; }
    const filhos = Array.from(no.childNodes).filter((f) => f.nodeType === 1 || (f.nodeType === 3 && f.nodeValue.trim()));
    if (!filhos.length) { linhas.push(recuo + abre(no) + '</' + nome + '>'); return; }
    if (filhos.length === 1 && filhos[0].nodeType === 3) {
      const t = filhos[0].nodeValue.replace(/\s+/g, ' ').trim();
      if (t.length <= 90) { linhas.push(recuo + abre(no) + t + '</' + nome + '>'); return; }
    }
    linhas.push(recuo + abre(no));
    filhos.forEach((f) => escreve(f, nivel + 1));
    linhas.push(recuo + '</' + nome + '>');
  };
  const corpo = copia.querySelector('body');
  if (corpo) escreve(corpo, 0);
  const lido = new DOMParser().parseFromString(html, 'text/html');
  let no = lido.documentElement;
  for (const i of caminho) no = no && no.children[i];
  const acha = (s) => { try { return lido.querySelectorAll(s); } catch (e) { return null; } };
  const doBom = p.alvo ? acha(p.alvo) : null;
  const doQuebrado = p.quebrado ? acha(p.quebrado) : null;
  return {html, fonte: linhas.join('\n'), alvo: caminho,
          conferido: {o_caminho_leva_ao_alvo: !!(alvo && no && no.outerHTML === alvo.outerHTML),
                      o_seletor_que_conserta_acha_o_alvo_primeiro: !!(doBom && doBom.length && doBom[0] === no),
                      quantos_o_localizador_quebrado_acha: doQuebrado ? doQuebrado.length : null}};
}
"""


def _foto(pagina) -> str:
    """A foto da tela como o integrante a veria, em JPEG e base64 (vai dentro da página da sessão)."""
    return base64.b64encode(pagina.screenshot(type="jpeg", quality=QUALIDADE_DA_FOTO)).decode("ascii")


def _chamada_da_api(inter, caminho: str = "/api/produtos") -> dict | None:
    """A última chamada à API que o roteiro fez nesse caminho, com o corpo como chegou."""
    for reg in reversed(inter.registros()):
        if reg["caminho"].rstrip("/") == caminho:
            return {"metodo": reg["metodo"], "caminho": reg["caminho"], "status": reg["status"], "tempo_ms": reg["tempo_ms"],
                    "content_type": reg["content_type"], "corpo": inter.corpo(reg["corpo_sha"]) if reg["corpo_sha"] else None}
    return None


# ! Alteração de IA - Revisar: (16/11/2026, decisão 136) `capturar_material`: para cada cenário, restaura o banco, liga a falha
# pelas mesmas funções das sessões presenciais (`executar_fase4.ligar_modo` no contrato; os cookies da variante PHP,
# `cenarios_fase4.armar_quebra`, no localizador), roda o roteiro do agente até ele parar e guarda o material; o treino usa o modo
# do treino e a página sem falha. Cada cenário de localizador só entra se as três conferências da fotografia passarem.
# ! Motivo: é o "tudo o que tem de rodar roda aqui antes" da decisão 136. A falha é armada do mesmo jeito que o agente a
# encontrou e que a versão 2 do protocolo armava para a pessoa; o que muda é que a pessoa recebe o registro do que aconteceu, e
# não o site no ar. A ficha da falha continua sendo a da corrida 21.
def capturar_material(canal: str = "chromium", token: str | None = None, saida: str = lbm.SAIDA_DO_ENSAIO, forma: str = "php", falar=print) -> dict:
    import executar_fase4 as ex
    import interceptador as ic
    import navegador
    token = token or ex.TOKEN_PADRAO
    fichas = lbm._registros_do_ensaio(saida)
    material: dict = {"versao": VERSAO_DO_MATERIAL, "capturado_em": dt.datetime.now().isoformat(timespec="seconds"), "forma_da_quebra": forma,
                      "contrato": ex._contrato_do_produto(), "cenarios": {}, "treino": {}}

    def pagina_nova(nav):
        return nav.navegador.new_page(viewport={"width": LARGURA_DA_FOTO, "height": ALTURA_DA_FOTO})

    def contrato(nav, roteiro: dict, modo: str, campo: str | None) -> dict:
        ex.ligar_modo(modo, campo, token)
        try:
            pagina = pagina_nova(nav)
            inter = ic.Interceptador(pagina)
            cen.rodar_cenario(roteiro, pagina, inter, capturar=False)
            chamada = _chamada_da_api(inter)
            foto = _foto(pagina)
            pagina.close()
        finally:
            ex.ligar_modo("normal", None, token)
        if chamada is None:
            raise SystemExit(f"!! o roteiro com o modo {modo} não deixou nenhuma chamada a /api/produtos registrada")
        return {"chamada": chamada, "tela": foto}

    def fotografia(pagina, alvo: str, quebrado: str | None, de_que: str) -> dict:
        f = pagina.evaluate(JS_FOTO_DO_HTML, {"alvo": alvo, "quebrado": quebrado})
        c = f.get("conferido") or {}
        if f.get("erro") or not (c.get("o_caminho_leva_ao_alvo") and c.get("o_seletor_que_conserta_acha_o_alvo_primeiro")):
            raise SystemExit(f"!! a fotografia do HTML de {de_que} não confere: {f.get('erro') or c}")
        return {"html": f["html"], "fonte": f["fonte"], "alvo": f["alvo"], "conferido": c, "tela": _foto(pagina)}

    with navegador.Navegador(canal=canal) as nav:
        material["navegador"] = nav.versao()["navegador"]
        for c in cen.CENARIOS_DO_ENSAIO:
            cid = c["id"]
            material["hash_do_banco"], _ = lbm._restaurar_banco()
            base = {"tipo": c["tipo"], "ficha": lbm.ficha_da_falha(cid, fichas), "roteiro": lbm.passos_do_roteiro(cid)}
            if not base["ficha"]:
                raise SystemExit(f"!! sem ficha da falha para {cid} em {saida}/cenarios.jsonl")
            if c["tipo"] == "contrato":
                base.update(contrato(nav, cen.cenario(c["cenario"]), c["modo"], c["campo"]))
            else:
                roteiro, q = lbm.roteiro_do_integrante(cid)
                pagina = pagina_nova(nav)
                cen.armar_quebra(pagina, q, forma)
                r = cen.rodar_cenario(roteiro, pagina, None, capturar=False, tempo_limite_ms=cen.TEMPO_LIMITE_QUEBRA_MS)
                if cen.task_success(r) or r.get("passo_falho") != q["passo_alvo"]:
                    raise SystemExit(f"!! {cid}: o roteiro com a quebra armada não parou no passo do localizador (parou em {r.get('passo_falho')})")
                base.update(fotografia(pagina, lbm.SELETOR_DO_ENSAIO[cid], q["localizador"], cid))
                if base["conferido"]["quantos_o_localizador_quebrado_acha"]:
                    raise SystemExit(f"!! {cid}: o localizador quebrado ainda acha elemento na fotografia")
                base["passo"] = q["passo_alvo"] + 1
                pagina.close()
            material["cenarios"][cid] = base
            falar(f"capturado: {cid} ({c['tipo']})")
        # o treino: o contrato com o modo do treino e o exercício de seletor na página sem falha
        t = lbm.TREINO_DE_CONTRATO
        material["treino"]["contrato"] = {"ficha": lbm.ficha_do_treino(), "roteiro": lbm._passos_numerados(cen.cenario(t["cenario"])),
                                          "causa": t["causa"], "campo": t["campo"], **contrato(nav, cen.cenario(t["cenario"]), t["modo"], t["campo"])}
        s = lbm.TREINO_DE_SELETOR
        ex.ligar_modo("normal", None, token)
        pagina = pagina_nova(nav)
        ic.Interceptador(pagina)
        pagina.goto(cen.BASE_PADRAO + s["pagina"])
        pagina.wait_for_selector(s["referencia"], timeout=60000)
        material["treino"]["seletor"] = {"alvo_em_palavras": f'o botão "{s["alvo"]["nome"]}" do primeiro produto',
                                         **fotografia(pagina, s["referencia"], None, "o treino de seletor")}
        pagina.close()
        falar("capturado: o treino (contrato e seletor)")
    return material


def gravar_material(material: dict, arquivo: Path) -> Path:
    # a tag vai num campo porque JSON não aceita comentário (como em fixtures_fase4/hashes_areas_so_leitura.json)
    material = {**material, "tag_ia": {
        "alteracao": "! Alteração de IA - Revisar: gravado por `linha_de_base_manual.py material --gravar` (Fase 5, decisão 136): o que o teste e o "
                     "navegador registraram em cada um dos dez cenários e no treino, com a falha armada nesta máquina; é o material que a página da "
                     "sessão mostra ao integrante.",
        "motivo": "! Motivo: a sessão da linha de base manual é feita por uma página publicada, que não alcança as cobaias; tudo o que tem de rodar "
                  "roda antes, aqui, e a página leva só o registro."}}
    arquivo.parent.mkdir(parents=True, exist_ok=True)
    arquivo.write_text(json.dumps(material, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return arquivo


def ler_material(arquivo: Path | None = None) -> dict:
    return json.loads((arquivo or arquivo_do_material()).read_text(encoding="utf-8"))


# ------------------------------------------------------------------ a página de cada integrante

FORMATO_DA_SESSAO = 3
PREFIXO_DO_CODIGO = "SESSAO3."
ARQUIVOS_DAS_PAGINAS = {n: RAIZ / "Documentacao" / "dashboard" / f"sessao-integrante-{n}.html" for n in range(1, lbm.INTEGRANTES + 1)}


# ! Alteração de IA - Revisar: (16/11/2026, decisão 136) `dados_da_pagina`: o que a página de um integrante leva embutido: os dez
# cenários pela posição na ordem sorteada dele (sem o nome do cenário, o modo de falha nem a resposta esperada), o material de
# cada um, o treino (o único que leva a resposta, porque a página a diz no fim), as 23 causas com a definição, as três perguntas
# de perfil, o limite e os avisos.
# ! Motivo: a página é lida por quem vai ser medido. Com a ordem embutida pela posição, a planilha e o registro continuam casando
# pelo sorteio, e o que identifica o cenário fica fora do que a pessoa recebe.
def dados_da_pagina(integrante: int, material: dict) -> dict:
    vezes = []
    for p, cid in enumerate(lbm.ordem_dos_integrantes()[integrante], 1):
        x = material["cenarios"][cid]
        v = {"ordem": p, "tipo": x["tipo"], "ficha": x["ficha"], "roteiro": x["roteiro"], "tela": x["tela"]}
        if x["tipo"] == "contrato":
            v["chamada"] = x["chamada"]
        else:
            v.update(passo=x["passo"], fonte=x["fonte"], html=x["html"], alvo=x["alvo"])
        vezes.append(v)
    t = material["treino"]
    # ! Alteração de IA - Revisar: (17/11/2026, ficha 77, decisão 137) a página leva também o texto do aviso do integrante: a pergunta
    # do fim de cada cenário, o que conta, o que não conta e o tamanho máximo.
    # ! Motivo: o tutorial e a tela do cenário fechado têm de dizer a mesma coisa, e as duas saem das constantes do ajudante.
    return {"formato": FORMATO_DA_SESSAO, "integrante": integrante, "limite_s": lbm.LIMITE_S, "aviso_s": lbm.AVISO_FINAL_S,
            "avisos": dict(lbm.AVISOS_DA_PAGINA), "causas": [[c, d] for c, d in lbm.DEFINICAO_DAS_CAUSAS.items()], "contrato": material["contrato"],
            "ocorrencia": {"pergunta": lbm.PERGUNTA_DA_OCORRENCIA, "conta": lbm.O_QUE_CONTA_COMO_OCORRENCIA,
                           "nao_conta": lbm.O_QUE_NAO_CONTA_COMO_OCORRENCIA, "limite": lbm.LIMITE_DA_OCORRENCIA},
            "perguntas": dict(lbm.PERGUNTAS_DE_PERFIL), "vezes": vezes,
            "treino": {"contrato": {k: t["contrato"][k] for k in ("ficha", "roteiro", "chamada", "tela", "causa", "campo")},
                       "seletor": {k: t["seletor"][k] for k in ("alvo_em_palavras", "fonte", "html", "alvo", "tela")}}}


# ! Alteração de IA - Revisar: (16/11/2026, decisão 136) `ESTILO_DA_SESSAO` e `PROGRAMA`: as telas da sessão e o programa que roda
# na página do integrante. Depois do botão Começar ele mostra, em ordem, as três perguntas, o treino e os dez cenários; em cada
# cenário o tempo começa no clique em "Abrir o cenário" e a página grava um evento com a hora do relógio do navegador a cada
# passo (início, entrega e resposta no contrato, cada tentativa no localizador, fim). O seletor do integrante é conferido contra
# a fotografia do HTML, lida com DOMParser e nunca posta na página viva. A sessão é guardada em três lugares: no navegador
# (para voltar de onde parou), no banco do artefato (quando a pessoa pode gravar nele) e, no fim, num código para copiar.
# ! Motivo: sem facilitador ao lado, é a página que arma o cenário, avisa do tempo e fecha no limite, pelas mesmas regras da seção
# 6 do protocolo. O banco do artefato só aceita gravação do dono e de quem foi convidado por e-mail como editor, e some para
# quem não está logado: por isso a página nunca depende dele para seguir, e o código da sessão existe para nenhuma sessão se
# perder. No contrato a página não diz se a resposta está certa, e a resposta esperada dos dez cenários não está nela.
# ! Alteração de IA - Revisar: (17/11/2026, ficha 77, decisão 137) a tela do cenário fechado ganhou a pergunta "Alguma coisa de fora
# atrapalhou este cenário?", com uma caixa de texto que pode ficar vazia. O que a pessoa escrever é gravado como evento
# `ocorrencia`, com a hora, no clique que leva ao próximo cenário (ou que termina a sessão).
# ! Motivo: a regra L14 do plano só anula a medida de um cenário por falha do protocolo anotada na hora (equipamento que travou,
# interrupção de fora), e na sessão pela página não há facilitador ao lado para anotar. A pergunta fica depois que o tempo parou
# para não entrar no tempo do cenário, e antes do próximo para o aviso ser escrito na hora. O formato da sessão continua o 3:
# os endereços já tinham sido mandados aos integrantes, e uma sessão sem aviso é igual à de antes.
ESTILO_DA_SESSAO = """
#tutorial { display: flex; flex-direction: column; gap: 2.5rem; }
#sessao { display: flex; flex-direction: column; gap: 1.5rem; }
.progresso { font-family: var(--mono); font-size: 0.875rem; color: var(--apagado); margin: 0; }
.estado-do-banco { font-size: 0.875rem; color: var(--apagado); margin: 0; }
.bloco { display: flex; flex-direction: column; gap: 0.5rem; min-width: 0; }
.ficha { background: var(--papel); border: 1px solid var(--fio); border-radius: 4px; padding: 0.75rem 1rem; font-family: var(--mono); font-size: 0.9375rem; overflow-wrap: anywhere; }
.roteiro { padding-left: 1.75rem; display: flex; flex-direction: column; gap: 0.25rem; font-family: var(--mono); font-size: 0.875rem; overflow-wrap: anywhere; }
.chamada { display: grid; grid-template-columns: repeat(auto-fit, minmax(9rem, 1fr)); gap: 0.5rem 1rem; }
.chamada div { display: flex; flex-direction: column; }
pre.alto { max-height: 26rem; overflow: auto; }
.foto { display: block; width: 100%; height: auto; border: 1px solid var(--fio); border-radius: 4px; }
.resposta { display: flex; flex-direction: column; gap: 0.625rem; background: var(--papel); border: 1px solid var(--fio); border-radius: 4px; padding: 1rem 1.125rem; }
.resposta label, .resposta legend { font-weight: 600; }
.resposta input[type=text], .resposta select, .resposta textarea, .codigo-da-sessao { font: inherit; font-family: var(--mono); font-size: 0.9375rem; padding: 0.5rem 0.625rem; border: 1px solid var(--fio); border-radius: 4px; background: var(--fundo); color: var(--tinta); width: 100%; min-width: 0; }
.codigo-da-sessao { min-height: 7rem; overflow-wrap: anywhere; }
fieldset { border: 0; padding: 0; margin: 0; display: flex; flex-wrap: wrap; gap: 0.25rem 1.25rem; }
fieldset legend { padding: 0; width: 100%; }
fieldset label { font-weight: 400; }
.botoes { display: flex; flex-wrap: wrap; gap: 0.75rem; align-items: center; }
.nota { font-size: 0.9375rem; color: var(--apagado); min-height: 1.5rem; overflow-wrap: anywhere; margin: 0; }
.resultado { border: 1px solid var(--fio); border-radius: 4px; padding: 0.875rem 1rem; background: var(--papel); display: flex; flex-direction: column; gap: 0.375rem; }
.resultado.certo { border-color: var(--certo); background: var(--certo-fundo); }
.resultado strong { font-size: 1.0625rem; }
"""

PROGRAMA = r"""
(() => {
  "use strict";
  const D = JSON.parse(new TextDecoder().decode(Uint8Array.from(atob(DADOS_EM_BASE64), (c) => c.charCodeAt(0))));
  const CHAVE = "sessao-do-integrante-" + D.integrante;
  const CAMINHO = "sessoes/integrante-" + D.integrante;
  const PREFIXO = "SESSAO3.";
  const el = (id) => document.getElementById(id);
  const esc = (t) => String(t == null ? "" : t).replace(/[&<>"]/g, (c) => ({"&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;"}[c]));
  const agora = () => Date.now() / 1000;
  let estado = {formato: D.formato, integrante: D.integrante, etapa: "tutorial", ordem: 1, perfil: null, treino: {}, eventos: [], navegador: navigator.userAgent};
  let banco = null, podeGravar = false, respondeu = false, salvo = false, fila = Promise.resolve(), relogio = null, avisou = false, verTutorial = false;
  const documentos = {};

  // ---- guardar: neste navegador, no banco do artefato e, no fim, no código da sessão
  function guardarAqui() { try { localStorage.setItem(CHAVE, JSON.stringify(estado)); } catch (e) { /* sem armazenamento neste navegador */ } }
  function guardar() {
    guardarAqui();
    if (banco && podeGravar) {
      const copia = JSON.parse(JSON.stringify(estado));
      fila = fila.then(() => banco.doc(CAMINHO).set(copia)).then(() => { salvo = true; pintarBanco(); }, (e) => { salvo = false; if (!e || e.code !== "unavailable") podeGravar = false; pintarBanco(); });
    }
    pintarBanco();
  }
  function pintarBanco() {
    const p = el("estado-do-banco");
    if (!p) return;
    p.hidden = estado.etapa === "tutorial";
    p.textContent = banco && podeGravar ? (salvo ? "Sessão guardada pela página." : "Guardando a sessão...")
      : respondeu ? "A página não consegue guardar a sessão sozinha para você. Ela fica guardada neste navegador, e no fim você copia o código da sessão e manda ao facilitador."
      : "Conferindo se a página consegue guardar a sessão...";
  }
  function paraBase64(texto) {
    const bytes = new TextEncoder().encode(texto);
    let s = "";
    for (let i = 0; i < bytes.length; i += 0x8000) s += String.fromCharCode.apply(null, bytes.subarray(i, i + 0x8000));
    return btoa(s);
  }

  // ---- os eventos e o que eles dizem de uma vez (a posição do cenário na ordem do integrante)
  function evento(nome, extra) { estado.eventos.push(Object.assign({evento: nome, ordem: estado.ordem, relogio_s: agora()}, extra || {})); }
  function daVez(ordem) {
    const r = {inicio: null, fechado: false, tentativas: 0, motivo: null};
    estado.eventos.forEach((e) => {
      if (e.ordem !== ordem) return;
      if (e.evento === "inicio" && r.inicio === null) r.inicio = e.relogio_s;
      if (e.evento === "tentativa") r.tentativas += 1;
      if (e.evento === "fim_do_armar") { r.fechado = true; r.motivo = e.motivo || null; }
    });
    return r;
  }
  const vezAtual = () => D.vezes[estado.ordem - 1];

  // ---- o relógio do cenário aberto: avisa quando falta pouco e fecha no limite
  function pararRelogio() { if (relogio) { clearInterval(relogio); relogio = null; } }
  function ligarRelogio() { pararRelogio(); relogio = setInterval(tique, 1000); tique(); }
  function tique() {
    const v = daVez(estado.ordem);
    if (estado.etapa !== "vez" || v.inicio === null || v.fechado) { pararRelogio(); return; }
    const passado = agora() - v.inicio;
    if (passado >= D.limite_s) { evento("fim_do_armar", {motivo: "limite"}); guardar(); pararRelogio(); pintar(); return; }
    if (!avisou && passado >= D.limite_s - D.aviso_s) {
      avisou = true;
      const a = el("aviso-do-tempo");
      if (a) { a.textContent = D.avisos.dois_minutos; a.hidden = false; }
    }
  }

  // ---- o material de um cenário
  function corpoEmLinhas(corpo) { return String(corpo == null ? "(a resposta veio sem corpo)" : corpo).replace(/\},\s*\{/g, "},\n{"); }
  function material(v) {
    let h = "";
    if (v.ficha) h += '<section class="bloco"><h3>A ficha da falha</h3><p class="ficha">' + esc(v.ficha) + "</p></section>";
    if (v.roteiro) h += '<section class="bloco"><h3>O roteiro do teste</h3><ol class="roteiro">' + v.roteiro.map((p) => "<li>" + esc(p.replace(/^\d+\.\s*/, "")) + "</li>").join("") + "</ol></section>";
    if (v.chamada) {
      const c = v.chamada;
      h += '<section class="bloco"><h3>A chamada à API</h3><dl class="chamada"><div><dt>Pedido</dt><dd><code>' + esc(c.metodo + " " + c.caminho) + "</code></dd></div><div><dt>Status</dt><dd><code>" + esc(c.status)
        + "</code></dd></div><div><dt>Tempo</dt><dd><code>" + esc(Math.round(c.tempo_ms)) + " ms</code></dd></div><div><dt>Tipo do conteúdo</dt><dd><code>" + esc(c.content_type || "não informado")
        + '</code></dd></div></dl><figure class="codigo"><figcaption>O corpo da resposta, como chegou (um item por linha)</figcaption><pre class="alto"><code>' + esc(corpoEmLinhas(c.corpo)) + "</code></pre></figure></section>";
      h += '<section class="bloco"><h3>O contrato esperado de cada item</h3><pre><code>' + esc(D.contrato) + "</code></pre></section>";
    }
    h += '<section class="bloco"><h3>A foto da tela</h3><img class="foto" alt="Foto da tela do site quando o teste rodou" src="data:image/jpeg;base64,' + v.tela + '"></section>';
    if (v.fonte) h += '<section class="bloco"><h3>O HTML da página</h3><pre class="alto"><code>' + esc(v.fonte) + "</code></pre></section>";
    return h;
  }
  const listaDasCausas = () => '<section class="bloco"><h3>As ' + D.causas.length + ' causas</h3><ol class="causas">' + D.causas.map((c) => "<li><code>" + esc(c[0]) + "</code><span>" + esc(c[1]) + "</span></li>").join("") + "</ol></section>";
  const formularioDoContrato = () => '<form id="resposta" class="resposta"><label for="causa">Causa</label><select id="causa" required><option value="">escolha uma das ' + D.causas.length + "</option>"
    + D.causas.map((c) => "<option>" + esc(c[0]) + "</option>").join("") + '</select><label for="campo">Campo afetado (deixe em branco para nenhum)</label><input id="campo" type="text" autocomplete="off" spellcheck="false">'
    + '<div class="botoes"><button type="submit" class="botao">Entregar a resposta</button></div></form>';
  const formularioDoSeletor = (rotulo) => '<form id="resposta" class="resposta"><label for="seletor">Seu seletor CSS</label><input id="seletor" type="text" autocomplete="off" spellcheck="false" required>'
    + '<div class="botoes"><button type="button" class="botao secundario" id="testar">Testar seletor</button><button type="submit" class="botao">' + rotulo + '</button></div><p id="resultado-do-teste" class="nota" role="status"></p></form>';

  // ---- a conferência do seletor contra a fotografia do HTML (lida à parte, nunca posta nesta página)
  function examinar(v, chave, seletor) {
    if (!documentos[chave]) documentos[chave] = new DOMParser().parseFromString(v.html, "text/html");
    const doc = documentos[chave];
    let achados;
    try { achados = doc.querySelectorAll(seletor); } catch (e) { return {valido: false, quantos: 0, passou: false, primeiro: ""}; }
    let alvo = doc.documentElement;
    v.alvo.forEach((i) => { alvo = alvo && alvo.children[i]; });
    return {valido: true, quantos: achados.length, passou: achados.length > 0 && achados[0] === alvo, primeiro: achados.length ? achados[0].cloneNode(false).outerHTML : ""};
  }
  function dizerOTeste(r) {
    return !r.valido ? "O navegador não entendeu esse seletor." : r.quantos === 0 ? "O seletor não acha nenhum elemento." : "O seletor acha " + r.quantos + " elemento(s). O primeiro é " + r.primeiro;
  }

  // ---- as telas
  function telaDoPerfil() {
    const p = D.perguntas;
    const simNao = (nome, pergunta) => "<fieldset><legend>" + esc(pergunta) + '</legend><label><input type="radio" name="' + nome + '" id="' + nome + '-sim" value="sim" required> Sim</label><label><input type="radio" name="'
      + nome + '" id="' + nome + '-nao" value="nao"> Não</label></fieldset>';
    return "<h2>Três perguntas antes de começar</h2><p>As respostas ficam com o número do integrante, sem o nome. Não escreva nada que identifique você.</p>"
      + '<form id="perfil" class="resposta"><label for="pratica">' + esc(p.pratica) + '</label><input id="pratica" type="text" required maxlength="200" autocomplete="off">'
      + simNao("usou", p.ja_usou_as_ferramentas_do_desenvolvedor) + simNao("leu", p.ja_leu_a_lista_dos_cenarios) + '<div class="botoes"><button type="submit" class="botao">Continuar para o treino</button></div></form>';
  }
  function telaDoTreinoDeContrato() {
    const t = D.treino.contrato, feito = estado.treino.contrato;
    let h = "<h2>Treino 1 de 2: um cenário de contrato</h2><p>Sem cronômetro. Serve para você conhecer o material e a forma da resposta. Só no treino a página diz a resposta certa.</p>";
    if (estado.perfil && estado.perfil.ja_leu_a_lista_dos_cenarios) h += '<aside class="aviso"><p class="aviso-titulo">Antes de continuar</p><p>Você respondeu que já leu a lista dos cenários. Avise o facilitador antes de seguir.</p></aside>';
    h += material(t) + listaDasCausas();
    if (!feito) return h + formularioDoContrato();
    return h + '<div class="resultado' + (feito.acertou ? " certo" : "") + '"><strong>' + (feito.acertou ? "Era isso." : "A resposta do treino era outra.") + "</strong><p>A causa era <code>" + esc(t.causa) + "</code> e o campo, <code>"
      + esc(t.campo || "nenhum") + "</code>. Você respondeu <code>" + esc(feito.causa) + "</code> e <code>" + esc(feito.campo || "nenhum") + '</code>.</p></div><div class="botoes"><button type="button" class="botao" id="seguir">Continuar o treino</button></div>';
  }
  function telaDoTreinoDeSeletor() {
    const t = D.treino.seletor, feito = estado.treino.seletor;
    return "<h2>Treino 2 de 2: um seletor</h2><p>Sem cronômetro e sem falha armada. Escreva um seletor CSS que ache " + esc(t.alvo_em_palavras) + ". Pode testar e conferir quantas vezes quiser.</p>" + material(t)
      + formularioDoSeletor("Conferir") + '<div id="conferido">' + (feito ? resultadoDoTreinoDeSeletor(feito) : "") + '</div><div class="botoes"><button type="button" class="botao" id="seguir">Ir para os cenários</button></div>';
  }
  const resultadoDoTreinoDeSeletor = (f) => '<div class="resultado' + (f.achou ? " certo" : "") + '"><strong>' + (f.achou ? "Achou o elemento certo." : "Ainda não é o elemento certo.") + "</strong><p>É assim que a página responde nos cenários de localizador.</p></div>";
  function telaDaVez() {
    const v = vezAtual(), s = daVez(estado.ordem), total = D.vezes.length;
    const tipo = v.tipo === "contrato" ? "contrato" : "localizador";
    let h = '<p class="progresso">Cenário ' + estado.ordem + " de " + total + "</p><h2>Cenário de " + tipo + "</h2>";
    if (s.inicio === null) {
      return h + "<p>" + (tipo === "contrato" ? "A resposta é uma causa da lista e o campo afetado, ou nenhum. A entrega é uma só." : "A resposta é um seletor CSS para o elemento do passo que quebrou. Você pode tentar mais de uma vez.")
        + " O tempo começa no clique, e o limite é de " + Math.round(D.limite_s / 60) + ' minutos.</p><div class="botoes"><button type="button" class="botao" id="abrir">Abrir o cenário</button></div>';
    }
    if (s.fechado) {
      const texto = s.motivo === "entrega" ? ["Resposta registrada.", "No cenário de contrato a página não diz se ela está certa."]
        : s.motivo === "passou" ? [D.avisos.passou, "O seletor achou o elemento do passo. Tentativas: " + s.tentativas + "."]
        : s.motivo === "limite" ? [D.avisos.esgotado, "O cenário foi fechado e conta como não resolvido."] : ["Cenário encerrado sem resposta.", "Ele conta como não resolvido."];
      return h + '<div class="resultado' + (s.motivo === "passou" ? " certo" : "") + '"><strong>' + esc(texto[0]) + "</strong><p>" + esc(texto[1]) + "</p></div>"
        + '<div class="resposta"><label for="ocorrencia">' + esc(D.ocorrencia.pergunta) + '</label><p class="nota">Só o que não é do cenário: ' + esc(D.ocorrencia.conta)
        + ". Não entra: " + esc(D.ocorrencia.nao_conta) + '. Se nada atrapalhou, deixe em branco.</p><textarea id="ocorrencia" rows="2" maxlength="' + D.ocorrencia.limite + '"></textarea></div>'
        + '<p>A pausa é livre. O tempo do próximo cenário só começa quando você abrir.</p><div class="botoes"><button type="button" class="botao" id="seguir">'
        + (estado.ordem < total ? "Próximo cenário" : "Terminar a sessão") + "</button></div>";
    }
    h += '<p id="aviso-do-tempo" class="aviso" role="status" hidden></p>' + material(v);
    h += tipo === "contrato" ? listaDasCausas() + formularioDoContrato() : formularioDoSeletor("Entregar");
    return h + '<div class="botoes" id="encerrar-caixa"><button type="button" class="botao secundario" id="encerrar">Encerrar sem resposta</button></div>';
  }
  function telaDoFim() {
    return "<h2>Sessão concluída</h2><p>Obrigado. Por favor, não comente os cenários nem as respostas com os outros integrantes até as sessões deles acabarem.</p>"
      + '<section class="bloco"><h3>O código da sessão</h3><p>Se a linha acima disser que a página não guardou a sessão sozinha, copie este código inteiro e mande ao facilitador. Se ela guardou, ele fica só de reserva.</p>'
      + '<textarea id="codigo" class="codigo-da-sessao" readonly rows="6">' + esc(PREFIXO + paraBase64(JSON.stringify(estado))) + '</textarea><div class="botoes"><button type="button" class="botao" id="copiar">Copiar o código</button><p id="copiado" class="nota" role="status"></p></div></section>';
  }

  function pintar() {
    const tutorial = el("tutorial"), sessao = el("sessao"), botao = el("botao-comecar");
    const dentro = estado.etapa !== "tutorial";
    tutorial.hidden = dentro && !verTutorial;
    sessao.hidden = !dentro;
    if (botao) botao.hidden = dentro;
    pintarBanco();
    if (!dentro) return;
    const telas = {"perfil": telaDoPerfil, "treino-contrato": telaDoTreinoDeContrato, "treino-seletor": telaDoTreinoDeSeletor, "vez": telaDaVez, "fim": telaDoFim};
    sessao.innerHTML = '<div class="botoes"><button type="button" class="botao secundario" id="ver-tutorial">' + (verTutorial ? "Esconder o tutorial" : "Ver o tutorial") + "</button></div>" + telas[estado.etapa]();
    ligar();
    if (estado.etapa === "vez") {
      const s = daVez(estado.ordem);
      if (s.inicio !== null && !s.fechado) {
        if (agora() - s.inicio >= D.limite_s - D.aviso_s) { avisou = false; }
        if (!relogio) ligarRelogio(); else tique();
      }
    }
  }
  function irPara(etapa) { estado.etapa = etapa; avisou = false; guardar(); pintar(); el("sessao").scrollIntoView(); }

  function ligar() {
    const ao = (id, tipo, fn) => { const e = el(id); if (e) e.addEventListener(tipo, fn); };
    ao("ver-tutorial", "click", () => { verTutorial = !verTutorial; pintar(); if (verTutorial) el("tutorial").scrollIntoView(); });
    ao("perfil", "submit", (ev) => {
      ev.preventDefault();
      const marcado = (nome) => { const m = document.querySelector('input[name="' + nome + '"]:checked'); return m ? m.value === "sim" : null; };
      const pratica = el("pratica").value.trim(), usou = marcado("usou"), leu = marcado("leu");
      if (!pratica || usou === null || leu === null) return;
      estado.perfil = {pratica: pratica, ja_usou_as_ferramentas_do_desenvolvedor: usou, ja_leu_a_lista_dos_cenarios: leu, relogio_s: agora()};
      irPara("treino-contrato");
    });
    ao("seguir", "click", () => {
      if (estado.etapa === "treino-contrato") irPara("treino-seletor");
      else if (estado.etapa === "treino-seletor") { estado.ordem = 1; irPara("vez"); }
      else if (estado.etapa === "vez") {
        // o aviso de que algo de fora atrapalhou é gravado aqui, com a hora, antes de a página passar para o próximo cenário
        const caixa = el("ocorrencia"), aviso = caixa ? caixa.value.trim().slice(0, D.ocorrencia.limite) : "";
        if (aviso) evento("ocorrencia", {texto: aviso});
        if (estado.ordem < D.vezes.length) { estado.ordem += 1; irPara("vez"); } else irPara("fim");
      }
    });
    ao("abrir", "click", () => { if (daVez(estado.ordem).inicio !== null) return; evento("inicio"); avisou = false; guardar(); pintar(); ligarRelogio(); });
    ao("testar", "click", () => {
      const seletor = el("seletor").value.trim();
      if (!seletor) return;
      const v = estado.etapa === "vez" ? vezAtual() : D.treino.seletor;
      el("resultado-do-teste").textContent = dizerOTeste(examinar(v, estado.etapa === "vez" ? "vez-" + estado.ordem : "treino", seletor));
    });
    ao("resposta", "submit", (ev) => {
      ev.preventDefault();
      if (estado.etapa === "treino-contrato") {
        const causa = el("causa").value, campo = el("campo").value.trim(), semCampo = !campo || campo.toLowerCase() === "nenhum";
        if (!causa) return;
        const t = D.treino.contrato;
        estado.treino.contrato = {causa: causa, campo: semCampo ? null : campo, acertou: causa === t.causa && (t.campo ? campo === t.campo : semCampo), relogio_s: agora()};
        guardar(); pintar(); return;
      }
      if (estado.etapa === "treino-seletor") {
        const seletor = el("seletor").value.trim();
        if (!seletor) return;
        const r = examinar(D.treino.seletor, "treino", seletor);
        estado.treino.seletor = {seletor: seletor, achou: r.passou, relogio_s: agora()};
        guardar();
        el("resultado-do-teste").textContent = dizerOTeste(r);
        el("conferido").innerHTML = resultadoDoTreinoDeSeletor(estado.treino.seletor);
        return;
      }
      if (estado.etapa !== "vez") return;
      const s = daVez(estado.ordem), v = vezAtual();
      if (s.inicio === null || s.fechado) return;
      if (v.tipo === "contrato") {
        const causa = el("causa").value, campo = el("campo").value.trim();
        if (!causa) return;
        evento("entrega");
        evento("resposta", {causa: causa, campo: campo});
        evento("fim_do_armar", {motivo: "entrega"});
        guardar(); pararRelogio(); pintar(); return;
      }
      const seletor = el("seletor").value.trim();
      if (!seletor) return;
      const r = examinar(v, "vez-" + estado.ordem, seletor);
      evento("tentativa", {seletor: seletor, corrigido: r.passou, motivo: r.passou ? null : !r.valido ? "o navegador não entendeu o seletor" : r.quantos === 0 ? "o seletor não achou elemento" : "o primeiro elemento achado não é o do passo"});
      if (r.passou) { evento("fim_do_armar", {motivo: "passou"}); guardar(); pararRelogio(); pintar(); return; }
      guardar();
      el("resultado-do-teste").textContent = D.avisos.nao_passou + " " + dizerOTeste(r);
    });
    ao("encerrar", "click", () => {
      el("encerrar-caixa").innerHTML = '<p class="nota">Encerrar mesmo? O cenário conta como não resolvido.</p><button type="button" class="botao" id="encerrar-sim">Sim, encerrar</button><button type="button" class="botao secundario" id="encerrar-nao">Voltar ao cenário</button>';
      el("encerrar-sim").addEventListener("click", () => { if (daVez(estado.ordem).fechado) return; evento("fim_do_armar", {motivo: "desistencia"}); guardar(); pararRelogio(); pintar(); });
      el("encerrar-nao").addEventListener("click", () => { el("encerrar-caixa").innerHTML = '<button type="button" class="botao secundario" id="encerrar">Encerrar sem resposta</button>'; ligar(); });
    });
    ao("copiar", "click", () => {
      const caixa = el("codigo"), dizer = (t) => { el("copiado").textContent = t; };
      const naMao = () => { caixa.focus(); caixa.select(); dizer("Código selecionado: copie com Ctrl+C."); };
      try { navigator.clipboard.writeText(caixa.value).then(() => dizer("Código copiado."), naMao); } catch (e) { naMao(); }
    });
  }

  async function iniciar() {
    try { const guardado = JSON.parse(localStorage.getItem(CHAVE) || "null"); if (guardado && guardado.formato === D.formato && guardado.integrante === D.integrante) estado = guardado; } catch (e) { /* começa do zero */ }
    const botao = el("botao-comecar");
    if (botao) botao.addEventListener("click", () => { if (estado.etapa === "tutorial") irPara("perfil"); });
    pintar();
    let db = null, user = null, pode = null;
    try { db = window.claude ? await window.claude.use("db") : null; } catch (e) { db = null; }
    try { user = window.claude ? await window.claude.use("user") : null; } catch (e) { user = null; }
    if (db) {
      try { pode = user ? await user.can("data.write") : null; } catch (e) { pode = null; }
      banco = db;
      podeGravar = pode !== false;
      try {
        const foto = await db.doc(CAMINHO).get();
        const remoto = foto.exists ? foto.data() : null;
        if (remoto && remoto.formato === D.formato && Array.isArray(remoto.eventos)) {
          if (remoto.eventos.length > estado.eventos.length || (estado.etapa === "tutorial" && remoto.etapa !== "tutorial")) { estado = JSON.parse(JSON.stringify(remoto)); guardarAqui(); pintar(); }
          salvo = true;
        }
      } catch (e) { /* segue sem a cópia do banco */ }
    }
    respondeu = true;
    if (estado.etapa !== "tutorial" && banco && podeGravar) guardar();
    pintarBanco();
  }
  iniciar();
})();
"""


def pagina_da_sessao(integrante: int, material: dict) -> str:
    """A página de um integrante: o tutorial, o botão Começar e a sessão, com os dados embutidos em base64."""
    import tutorial_do_integrante as tut
    dados = dados_da_pagina(integrante, material)
    blob = base64.b64encode(json.dumps(dados, ensure_ascii=False, separators=(",", ":")).encode("utf-8")).decode("ascii")
    cenarios, limite = len(dados["vezes"]), lbm.LIMITE_S // 60
    fontes = ("https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&amp;family=IBM+Plex+Sans:wght@400;500;600&amp;"
              "family=IBM+Plex+Sans+Condensed:wght@600&amp;display=swap")
    partes = [
        f"<title>Sessão do integrante {integrante}</title>",
        '<meta name="claude:viewport-fit-sides" content="cover">',
        "<!-- ! Alteração de IA - Revisar: página gerada por `python linha_de_base_manual.py paginas --gravar` (sessao_pelo_artefato.py): a sessão da "
        f"linha de base manual do integrante {integrante}, com o tutorial, o botão Começar e os cenários na ordem sorteada dele.\n"
        "     ! Motivo: decisão 136. Os integrantes fazem a sessão por uma página publicada, sem instalar nada; o material de cada cenário foi "
        "capturado antes, na máquina do projeto, e a página grava o tempo e a resposta de cada um. -->",
        f'<link rel="stylesheet" href="{fontes}">',
        f"<style>{tut.ESTILO}{ESTILO_DA_SESSAO}</style>",
        '<div class="pagina">',
        "<header>",
        '<p class="sobre">Linha de base manual</p>',
        f"<h1>Sessão do integrante {integrante}</h1>",
        '<p class="chamada">Leia o tutorial até o fim. O botão Começar fica na última seção.</p>',
        f'<ul class="fatos"><li>{cenarios} cenários</li><li>até {limite} min por cenário</li><li>reserve {tut.teto_da_sessao()}</li></ul>',
        "</header>",
        '<p id="estado-do-banco" class="estado-do-banco" role="status" hidden></p>',
        '<div id="tutorial">',
        tut.secoes_em_html(),
        "</div>",
        '<div id="sessao" hidden></div>',
        "<footer>Esta página é só sua: ela traz os cenários na ordem sorteada para você. O tutorial é o mesmo para os três integrantes.</footer>",
        "</div>",
        f'<script>const DADOS_EM_BASE64 = "{blob}";</script>',
        f"<script>{PROGRAMA}</script>",
    ]
    return "\n".join(partes) + "\n"


def blob_da_pagina(pagina: str) -> str:
    """O bloco em base64 que a página leva embutido."""
    import re
    achado = re.search(r'const DADOS_EM_BASE64 = "([A-Za-z0-9+/=]+)";', pagina)
    if not achado:
        raise ValueError("a página não tem os dados embutidos")
    return achado.group(1)


def dados_embutidos(pagina: str) -> dict:
    return json.loads(base64.b64decode(blob_da_pagina(pagina)).decode("utf-8"))


def gravar_paginas(material: dict | None = None) -> list[Path]:
    material = material or ler_material()
    for n, arquivo in ARQUIVOS_DAS_PAGINAS.items():
        arquivo.parent.mkdir(parents=True, exist_ok=True)
        arquivo.write_text(pagina_da_sessao(n, material), encoding="utf-8", newline="\n")
    return list(ARQUIVOS_DAS_PAGINAS.values())


def conferir_paginas(material: dict | None = None) -> list[str]:
    """As páginas gravadas que faltam ou diferem do que o código gera a partir do material (vazio quando estão em dia)."""
    material = material or ler_material()
    return [a.name for n, a in ARQUIVOS_DAS_PAGINAS.items() if not a.exists() or a.read_text(encoding="utf-8") != pagina_da_sessao(n, material)]


# ------------------------------------------------------------------ trazer para cá a sessão que a página gravou

# ! Alteração de IA - Revisar: (16/11/2026, decisão 136) `ler_codigo` (o código da sessão, ou o JSON lido do banco do artefato,
# vira o dicionário da sessão), `eventos_do_registro` (cada evento da página vira um evento do registro, no formato dos comandos
# presenciais: o cenário e o tipo saem do sorteio pela posição, a hora é refeita do relógio no fuso desta máquina, o corrigido do
# contrato é a regra do agente, e o seletor que passou na página é rodado no roteiro de verdade), `importar_sessao` (acrescenta
# ao registro, uma vez por integrante) e `perfil_da_sessao` (as três respostas mais a anotação do facilitador).
# ! Motivo: a página confere o seletor contra uma fotografia do HTML, e o que o protocolo conta como corrigido é o roteiro do
# agente chegar ao fim com o seletor: por isso a importação roda o roteiro aqui e é ele que vale. A resposta esperada do contrato
# não está na página, então o corrigido só pode ser calculado aqui. Com o registro no mesmo formato, o comando `planilha` e a
# leitura da Fase 5 não mudam; sessão malformada é recusada inteira, antes de qualquer gravação.
def ler_codigo(texto: str) -> dict:
    t = (texto or "").strip()
    try:
        if t.startswith(PREFIXO_DO_CODIGO):
            dado = json.loads(base64.b64decode(t[len(PREFIXO_DO_CODIGO):], validate=True).decode("utf-8"))
        else:
            dado = json.loads(t)
    except Exception as e:  # noqa: BLE001 - qualquer defeito do texto é o mesmo erro para quem importa
        raise ValueError(f"o texto não é um código de sessão nem o JSON de uma sessão ({type(e).__name__})") from None
    if not isinstance(dado, dict):
        raise ValueError("o texto não é uma sessão")
    return dado


def _numero(x) -> bool:
    return isinstance(x, (int, float)) and not isinstance(x, bool)


# ! Alteração de IA - Revisar: (17/11/2026, ficha 77, decisão 137) `ocorrencias_da_sessao` lista os avisos que o integrante deixou no
# fim dos cenários (a posição e o texto limpo). `eventos_do_registro` e `importar_sessao` passam a receber `anular`, as posições
# cuja linha o facilitador anulou: cada aviso vira um evento `ocorrencia` do registro, com o texto, a hora em que foi escrito,
# se a linha foi anulada e a hora da decisão. Sessão com aviso não entra sem a decisão, e posição sem aviso não pode ser anulada.
# ! Motivo: a regra L14 do plano só anula a medida de um cenário por falha do protocolo anotada na hora, antes de qualquer número
# ser lido. Na sessão pela página quem anota na hora é a pessoa; a decisão do facilitador fica gravada na importação, que não
# mostra tempo nenhum, e o comando `planilha` só a copia para as observações. O tempo e a resposta do cenário não mudam.
def ocorrencias_da_sessao(sessao: dict) -> list[tuple[int, str]]:
    """Os avisos do integrante, na ordem em que foram escritos: a posição do cenário e o texto como vai para o registro."""
    saida = []
    for b in sessao.get("eventos") if isinstance(sessao.get("eventos"), list) else []:
        if isinstance(b, dict) and b.get("evento") == lbm.EVENTO_DA_OCORRENCIA:
            texto, ordem = lbm.texto_da_ocorrencia(b.get("texto")), b.get("ordem")
            if texto is None or not isinstance(ordem, int) or isinstance(ordem, bool):
                raise ValueError("aviso do integrante sem texto ou sem a posição do cenário")
            saida.append((ordem, texto))
    return saida


def eventos_do_registro(sessao: dict, conferir_seletor=None, anular=None) -> tuple[list[dict], list[str]]:
    """Os eventos da sessão no formato do registro e os avisos. `conferir_seletor(cenario, seletor)` roda o roteiro de verdade
    com o seletor que passou na página; sem ela, vale o que a página conferiu. `anular` são as posições cuja linha o
    facilitador anulou pelo aviso do integrante."""
    anuladas = set(anular or ())
    decidida_em = lbm.hora_do_relogio(lbm._relogio())
    if sessao.get("formato") != FORMATO_DA_SESSAO:
        raise ValueError(f"a sessão não está no formato {FORMATO_DA_SESSAO} da página")
    n = sessao.get("integrante")
    if not isinstance(n, int) or isinstance(n, bool) or not 1 <= n <= lbm.INTEGRANTES:
        raise ValueError(f"integrante {n!r} fora da planilha")
    brutos = sessao.get("eventos")
    if not isinstance(brutos, list):
        raise ValueError("a sessão não tem a lista de eventos")
    navegador_ = str(sessao.get("navegador") or "")[:300]
    saida: list[dict] = []
    for i, b in enumerate(brutos, 1):
        if not isinstance(b, dict):
            raise ValueError(f"evento {i}: não é um evento")
        nome, ordem, t = b.get("evento"), b.get("ordem"), b.get("relogio_s")
        if nome not in lbm.EVENTOS_DA_VEZ and nome != lbm.EVENTO_DA_OCORRENCIA:
            raise ValueError(f"evento {i}: {nome!r} não é um evento da sessão")
        if not isinstance(ordem, int) or isinstance(ordem, bool) or not 1 <= ordem <= len(cen.CENARIOS_DO_ENSAIO):
            raise ValueError(f"evento {i}: posição {ordem!r} fora da ordem do integrante")
        if not _numero(t):
            raise ValueError(f"evento {i}: sem a hora do relógio")
        vez = lbm.vez_do_cenario(n, ordem)
        campos: dict = {"origem": "artefato"}
        if nome == "inicio":
            campos.update(navegador=navegador_, hash_do_banco=None, segundos_do_banco=0.0, forma=None, ficha=None)
        elif nome in ("entrega", "resposta"):
            if vez["tipo"] != "contrato":
                raise ValueError(f"evento {i}: {nome} numa posição de localizador")
            if nome == "resposta":
                causa = lbm.causa_da_lista(b.get("causa"))
                if causa is None:
                    raise ValueError(f"evento {i}: a causa {b.get('causa')!r} não é uma das {len(lbm.DEFINICAO_DAS_CAUSAS)}")
                campo = lbm.campo_entregue(b.get("campo"))
                campos.update(causa=causa, campo=campo, corrigido=lbm.resultado_da_entrega(vez["cenario"], causa, campo), recusada=False)
        elif nome == "tentativa":
            if vez["tipo"] != "localizador":
                raise ValueError(f"evento {i}: tentativa de seletor numa posição de contrato")
            seletor = b.get("seletor")
            if not isinstance(seletor, str) or not seletor.strip():
                raise ValueError(f"evento {i}: tentativa sem seletor")
            passou = bool(b.get("corrigido"))
            campos.update(seletor=seletor.strip(), corrigido=passou, segundos_do_banco=0.0, segundos_do_roteiro=None, motivo=b.get("motivo"),
                          passou_na_pagina=passou, conferido_no_roteiro=None)
        elif nome == lbm.EVENTO_DA_OCORRENCIA:
            texto = lbm.texto_da_ocorrencia(b.get("texto"))
            if texto is None:
                raise ValueError(f"evento {i}: aviso do integrante sem texto")
            campos.update(texto=texto, anulada=ordem in anuladas, decidida_em=decidida_em)
        else:
            campos.update(motivo=b.get("motivo"))
        saida.append(lbm.montar_evento(nome, vez, float(t), **campos))
    # o aviso é do cenário que a pessoa abriu, e só o que ela escreveu na hora pode anular a linha (regra L14)
    abertas = {e["ordem"] for e in saida if e["evento"] == "inicio"}
    com_aviso = {e["ordem"] for e in saida if e["evento"] == lbm.EVENTO_DA_OCORRENCIA}
    if com_aviso - abertas:
        raise ValueError(f"aviso do integrante em posição que não foi aberta: {sorted(com_aviso - abertas)}")
    if anuladas - com_aviso:
        raise ValueError(f"posição {', '.join(str(p) for p in sorted(anuladas - com_aviso))} sem aviso do integrante: só anula a linha a falha "
                         "que a pessoa escreveu na hora (regra L14)")
    avisos: list[str] = []
    # o roteiro de verdade, uma vez por cenário de localizador, com o primeiro seletor que passou na página
    conferidas: set[int] = set()
    for e in saida:
        if e["evento"] == "tentativa" and e["passou_na_pagina"] and e["ordem"] not in conferidas and conferir_seletor is not None:
            conferidas.add(e["ordem"])
            e["conferido_no_roteiro"] = bool(conferir_seletor(e["cenario"], e["seletor"]))
            if not e["conferido_no_roteiro"]:
                e["corrigido"] = False
                e["motivo"] = "passou na conferência da página e não passou no roteiro de verdade, rodado na importação"
                avisos.append(f"integrante {n}, ordem {e['ordem']}: o seletor {e['seletor']!r} passou na página e não passou no roteiro de verdade; "
                              "o cenário fica não corrigido")
    resumo = lbm.resumo_do_registro(saida)
    if len(resumo) != len(cen.CENARIOS_DO_ENSAIO):
        avisos.append(f"integrante {n}: a sessão tem {len(resumo)} de {len(cen.CENARIOS_DO_ENSAIO)} cenários abertos")
    abertos = [str(p) for (_, p), r in resumo.items() if not r["fechado"]]
    if abertos:
        avisos.append(f"integrante {n}: cenário(s) que não foram fechados na página: {', '.join(abertos)}")
    # o treino, para a leitura saber que cada integrante treinou
    primeiro = saida[0]["relogio_s"] if saida else 0.0
    treino = sessao.get("treino") if isinstance(sessao.get("treino"), dict) else {}
    antes = []
    for parte in ("contrato", "seletor"):
        t = treino.get(parte)
        if isinstance(t, dict):
            campos = {k: t.get(k) for k in (("causa", "campo", "acertou") if parte == "contrato" else ("seletor", "achou"))}
            antes.append(lbm.montar_evento("treino", {"integrante": n}, float(t["relogio_s"]) if _numero(t.get("relogio_s")) else primeiro,
                                           origem="artefato", parte=parte, **campos))
        else:
            avisos.append(f"integrante {n}: a sessão não tem o treino de {parte}")
    return antes + saida, avisos


def importar_sessao(sessao: dict, arquivo: Path, conferir_seletor=None, anular=None) -> dict:
    """Acrescenta a sessão ao registro; ValueError se ela é malformada, se o integrante já está no registro ou se ela tem aviso
    do integrante e o facilitador não disse quais posições anular (`anular`; conjunto vazio para nenhuma)."""
    if anular is None and ocorrencias_da_sessao(sessao):
        raise ValueError("a sessão tem aviso do integrante e falta a decisão do facilitador: diga quais posições anular, ou nenhuma (`--anular`)")
    eventos_do_registro(sessao, anular=anular)                      # confere a sessão inteira antes de rodar qualquer roteiro
    n = sessao["integrante"]
    if any(e.get("integrante") == n for e in lbm.ler_registro(arquivo)):
        raise ValueError(f"o integrante {n} já tem eventos em {arquivo.name}: a sessão dele já foi trazida")
    eventos, avisos = eventos_do_registro(sessao, conferir_seletor, anular)
    arquivo.parent.mkdir(parents=True, exist_ok=True)
    with open(arquivo, "a", encoding="utf-8", newline="\n") as f:
        f.writelines(json.dumps(e, ensure_ascii=False) + "\n" for e in eventos)
    return {"avisos": avisos, "eventos": len(eventos), "cenarios": len(lbm.resumo_do_registro(eventos))}


def perfil_da_sessao(sessao: dict, conhece_o_codigo: bool, o_que_conhece: str = "") -> dict:
    p = sessao.get("perfil") if isinstance(sessao.get("perfil"), dict) else {}
    return lbm.perfil_do_integrante({"pratica": str(p.get("pratica") or ""),
                                     "ja_usou_as_ferramentas_do_desenvolvedor": p.get("ja_usou_as_ferramentas_do_desenvolvedor"),
                                     "ja_leu_a_lista_dos_cenarios": p.get("ja_leu_a_lista_dos_cenarios"),
                                     "conhece_o_codigo_das_cobaias": bool(conhece_o_codigo), "o_que_conhece": o_que_conhece if conhece_o_codigo else ""})
