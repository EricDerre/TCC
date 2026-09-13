#!/usr/bin/env python3
# ! Alteração de IA - Revisar: cria gerar_relatorio_fase3.py — o relatório HTML navegável da
# Fase 3: um arquivo único (sem fetch, sem dependência de rede) com o resumo modelo × biblioteca
# (L0..L3) × partição, a documentação que cada modelo escreveu por época, a comparação pareada
# contra a L0 e o Cochran Q, as propostas de edição caso a caso (prompt inteiro, resposta crua,
# decisões com código de rejeição) e os diagnósticos caso a caso, os dois com filtros em
# <select>, e os diffs de biblioteca gerados a cada época fechada.
# ! Motivo: avaliar_fase3.py responde "quanto" (percentuais, Δ, p) mas não "por quê" — para
# entender por que um modelo piorou de uma época para outra é preciso ler o que ele ESCREVEU na
# biblioteca e a resposta que deu a cada caso, lado a lado com o gabarito. Isso hoje só dá para
# fazer abrindo os JSONL e os .md de diff à mão, pasta por pasta, modelo por modelo. Segue o
# esqueleto de gerar_relatorio.py (arquivo único, JSON embutido, filtros em JS) com uma
# diferença deliberada: aqui o texto embutido no JSON já sai de html.escape ANTES do
# json.dumps (e não só filtrado por um esc() no JavaScript, como em gerar_relatorio.py). A
# resposta e o prompt são texto que o MODELO escreveu sobre um caso de bug fictício — podem
# conter qualquer coisa, inclusive algo que se pareça com "</script>" — e um JSON cru embutido
# num <script> quebra a tag no meio se essa sequência aparecer dentro de uma string; escapando
# antes, o próprio arquivo estático já mostra o texto seguro (e a tag nunca aparece), sem
# depender de o navegador rodar o JavaScript primeiro.
"""Relatório HTML navegável da Fase 3: resumo modelo × biblioteca × partição, documentação
escrita por época, comparação pareada contra a L0, Cochran Q, propostas e diagnósticos caso a
caso com filtros, e os diffs de biblioteca de cada época fechada."""
import argparse
import html
import json
import re
import sys
from pathlib import Path

import avaliar_fase3
import caminhos

# ! Alteração de IA - Revisar: força UTF-8 na saída do console, copiado de
# biblioteca.py:25-32.
# ! Motivo: no Windows o console pode estar em cp1252; os nomes de modelo e as mensagens deste
# script têm acentos, e sem isso o script aborta com UnicodeEncodeError ao imprimir o resumo.
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


# --------------------------------------------------------------------- colunas das tabelas

# ! Alteração de IA - Revisar: as mesmas colunas de gerar_relatorio.CAMPOS_TABELA (2-B), com
# 'condicao' trocada por 'biblioteca_epoca' + 'particao' (os dois eixos que substituem a
# condição de biblioteca na Fase 3) e quatro colunas próprias acrescentadas ao final.
# ! Motivo: o corte da 2-B era modelo × condição (A0..A5); aqui é modelo × versão da biblioteca
# (L0..L3, escrita pelo próprio modelo) × partição (aprendizado nunca mede generalização,
# avaliação nunca entra na biblioteca) — os dois eixos precisam aparecer para a linha ser
# identificável. As quatro colunas novas (balanceada, nota no contexto, citou verbete anotado/
# novo) são justamente o que a Fase 3 mede e a 2-B não tinha como medir (não havia biblioteca
# escrita pelo modelo para citar).
CAMPOS_TABELA_FASE3 = [
    ("modelo", "modelo"), ("biblioteca_epoca", "L"), ("particao", "partição"), ("n", "n"),
    ("causa_correta_pct", "causa %"), ("causa_correta_ic95", "IC 95%"),
    ("campo_correto_pct", "campo %"), ("fora_do_conjunto_pct", "fora %"),
    ("citou_verbete_pct", "citou %"), ("ouro_no_contexto_pct", "ouro %"),
    ("acuracia_balanceada_pct", "balanceada %"), ("contexto_com_nota_pct", "nota no ctx %"),
    ("citou_verbete_anotado_pct", "citou anotado %"), ("citou_verbete_novo_pct", "citou novo %"),
    ("tokens_entrada_mediana", "tok. entrada"), ("prefill_ms_mediana", "prefill ms"),
    ("segundos_mediana", "seg"),
]

CAMPOS_DOCUMENTACAO = [
    ("modelo", "modelo"), ("epoca", "época"), ("n_propostas", "propostas"),
    ("n_aceitas", "aceitas"), ("aceitas_pct", "aceitas %"), ("n_nenhuma", "nenhuma"),
    ("n_respostas_truncadas", "truncadas"), ("notas_aceitas", "notas"),
    ("retificacoes_aceitas", "retificações"), ("verbetes_novos_aceitos", "verbetes novos"),
    # bytes crus dos .md do diff (não o texto renderizado do prompt — ver avaliar_fase3.
    # documentacao_por_epoca, onda final I4).
    ("tokens_md_estimados_acrescentados", "tokens md +"),
    ("tentativas_de_decorar", "tent. decorar"),
    ("prefill_proposta_vs_diagnostico", "prefill ms/tok prop. × diag."),
    ("top3_motivos_rejeicao", "top-3 motivos de rejeição"),
]

CAMPOS_PAREADO = [
    ("modelo", "modelo"), ("biblioteca_epoca", "L"), ("particao", "partição"),
    ("n_pares", "n pares"), ("acerto_L0_pct", "L0 %"), ("acerto_pct", "versão %"),
    ("delta_pp", "Δ pp"), ("b", "b"), ("c", "c"), ("razao_bc", "b/c"),
    ("p_mcnemar", "p"), ("p_holm_marcado", "p (Holm)"), ("g_cohen", "g"),
]

CAMPOS_COCHRAN = [("modelo", "modelo"), ("particao", "partição"), ("n_casos", "n casos"),
                  ("q", "Q"), ("gl", "gl"), ("p", "p")]

CAMPOS_FLIPS = [
    ("modelo", "modelo"), ("transicao", "transição"), ("particao", "partição"),
    ("n_pares", "n pares"), ("certo_para_errado", "certo→errado"),
    ("errado_para_certo", "errado→certo"), ("autoenvenenamento_pct", "autoenvenenamento %"),
]


# --------------------------------------------------------------------------- página (esqueleto)

_MODELO = """<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><title>Fase 3 — relatório</title>
<style>
body{font:14px/1.45 system-ui,sans-serif;margin:0;padding:24px;color:#0b0b0b;background:#fcfcfb}
h1{font-size:20px;margin:0 0 4px}h2{font-size:16px;margin:28px 0 8px}
.tabela-scroll{overflow-x:auto;margin:8px 0}
table{border-collapse:collapse;font-size:12.5px}th,td{border-bottom:1px solid #e5e4e0;padding:4px 8px;text-align:left;white-space:nowrap}
th{color:#52514e;font-weight:600}td.num{text-align:right;font-variant-numeric:tabular-nums}
.filtros{display:flex;gap:12px;flex-wrap:wrap;margin:12px 0}.filtros label{font-size:12px;color:#52514e}
select{font:inherit}#lista-propostas,#lista-diagnosticos{display:grid;gap:10px}
.caso{border:1px solid #e5e4e0;border-radius:6px;padding:10px 12px;background:#fff}
.caso header{display:flex;gap:10px;flex-wrap:wrap;font-size:12px;color:#52514e;margin-bottom:6px}
.ok{color:#1baf7a;font-weight:600}.erro{color:#eb6834;font-weight:600}
pre{white-space:pre-wrap;font-size:12px;background:#f5f4f1;padding:8px;border-radius:4px;margin:6px 0 0;word-break:break-word}
details summary{cursor:pointer;font-size:12px;color:#52514e}
details{margin-top:6px}
</style></head><body>
<!-- ! Alteração de IA - Revisar: relatório HTML GERADO por gerar_relatorio_fase3.py a partir
     de avaliacao_fase3.json, resumo_fase3.json e dos JSONL/diff em resultados/fase3 (ou na
     pasta de --saida) — não editar à mão, o próximo `python gerar_relatorio_fase3.py` sobrescreve.
     ! Motivo: nenhum número deste relatório é digitado — todos saem de avaliar_fase3.py; editar
     aqui perderia a rastreabilidade do dado até o JSONL que o gerou. -->
<h1>Fase 3 — biblioteca escrita pelo modelo, época a época</h1>
<p style="color:#52514e;margin:0">Gerado por gerar_relatorio_fase3.py a partir de
avaliacao_fase3.json, resumo_fase3.json e dos JSONL/diff em __RAIZ__. Nenhum número digitado
à mão.</p>

<h2>Resumo — modelo × biblioteca (L0..L3) × partição</h2>
__TABELA_RESUMO__

<h2>Documentação escrita pelo modelo, por época</h2>
__TABELA_DOCUMENTACAO__

<h2>Comparação pareada contra a L0 e Cochran Q</h2>
__TABELA_PAREADO__
__TABELA_COCHRAN__
<h3 style="font-size:13px;margin:16px 0 6px">Flips entre épocas (autoenvenenamento = certo → errado)</h3>
__TABELA_FLIPS__

<h2>Propostas caso a caso</h2>
<div class="filtros">
<label>modelo <select id="p-modelo"><option value="">todos</option></select></label>
<label>época <select id="p-epoca"><option value="">todas</option></select></label>
<label>partição <select id="p-particao"><option value="">todas</option></select></label>
<label>aceita <select id="p-aceita"><option value="">todas</option>
<option value="sim">sim</option><option value="não">não</option>
<option value="nenhuma">nenhuma</option></select></label>
<label>motivo <select id="p-motivo"><option value="">todos</option></select></label>
<label>acertou o diagnóstico <select id="p-acerto"><option value="">todos</option>
<option value="1">sim</option><option value="0">não</option></select></label>
<span id="p-contagem" style="font-size:12px;color:#52514e"></span>
</div>
<div id="lista-propostas"></div>

<h2>Diagnósticos caso a caso</h2>
<div class="filtros">
<label>modelo <select id="d-modelo"><option value="">todos</option></select></label>
<label>biblioteca <select id="d-biblioteca"><option value="">todas</option></select></label>
<label>partição <select id="d-particao"><option value="">todas</option></select></label>
<label>classe <select id="d-classe"><option value="">todas</option></select></label>
<label>nível <select id="d-nivel"><option value="">todos</option></select></label>
<label>acerto <select id="d-acerto"><option value="">todos</option>
<option value="1">só acertos</option><option value="0">só erros</option></select></label>
<span id="d-contagem" style="font-size:12px;color:#52514e"></span>
</div>
<div id="lista-diagnosticos"></div>

<h2>Diffs por época</h2>
__DIFFS__

<script>
var CLASSES = {1:"Léxica",2:"Sintática",3:"Semântica",4:"Tradução",5:"Runtime",6:"Efeito"};
var LIMITE_CARTOES = 400;
function val(id){return document.getElementById(id).value;}
function opcoes(id, valores){
  var s = document.getElementById(id);
  valores.forEach(function(v){var o=document.createElement("option");o.value=v;o.textContent=v;s.appendChild(o);});
}
function unicos(dados, campo){
  return Array.from(new Set(dados.map(function(d){return d[campo];}))).sort();
}
function unicosAninhados(dados, campoLista){
  var s = new Set();
  dados.forEach(function(d){(d[campoLista]||[]).forEach(function(v){s.add(v);});});
  return Array.from(s).sort();
}

// --------------------------------------------------------------- propostas caso a caso
// Os textos abaixo (resposta, prompt, parse, texto/motivo/detalhe de cada decisão) já saem
// ESCAPADOS de gerar_relatorio_fase3.py (html.escape em Python, antes do json.dumps) — o
// JavaScript só concatena para montar o cartão. Escapar de novo aqui trocaria "&lt;" por
// "&amp;lt;" na tela.
var DADOS_PROPOSTAS = __DADOS_PROPOSTAS__;
opcoes("p-modelo", unicos(DADOS_PROPOSTAS, "modelo"));
opcoes("p-epoca", unicos(DADOS_PROPOSTAS, "epoca"));
opcoes("p-particao", unicos(DADOS_PROPOSTAS, "particao"));
opcoes("p-motivo", unicosAninhados(DADOS_PROPOSTAS, "motivos_rejeicao"));

function linhaDecisao(d){
  return "<tr><td>" + d.numero + "</td><td>" + d.operacao + "</td><td>" + d.verbete + "</td>"
    + "<td class=\\"" + (d.aceita ? "ok" : "erro") + "\\">" + (d.aceita ? "sim" : "não") + "</td>"
    + "<td>" + d.motivo + "</td><td>" + d.detalhe + "</td></tr>";
}
function cartaoProposta(p){
  var tabelaDecisoes = p.decisoes.length
    ? "<table><thead><tr><th>#</th><th>operação</th><th>verbete</th><th>aceita</th><th>motivo</th><th>detalhe</th></tr></thead><tbody>"
      + p.decisoes.map(linhaDecisao).join("") + "</tbody></table>"
    : "<p style=\\"color:#52514e;font-size:12px;margin:6px 0 0\\">nenhum bloco de proposta nesta resposta</p>";
  return "<div class=\\"caso\\"><header><b>" + p.caso + "</b><span>" + p.modelo + "</span>"
    + "<span>época " + p.epoca + " / " + p.particao + "</span>"
    + "<span class=\\"" + (p.acertou_diagnostico ? "ok" : "erro") + "\\">"
    + (p.acertou_diagnostico ? "acertou o diagnóstico" : "errou o diagnóstico") + "</span>"
    + "<span>causa mostrada: <code>" + p.causa_correta_mostrada + "</code></span>"
    + "<span>" + p.n_aceitas + "/" + p.n_propostas + " aceita(s) — " + p.aceite + "</span>"
    + (p.segundos == null ? "" : "<span>" + p.segundos + " s"
        + (p.prefill_ms ? " · prefill " + p.prefill_ms + " ms" : "") + "</span>")
    + "</header>"
    + (p.ids_visiveis.length
        ? "<div style=\\"font-size:12px;color:#52514e\\">ids visíveis: " + p.ids_visiveis.join(", ") + "</div>"
        : "")
    + "<pre>" + p.resposta + "</pre>"
    + tabelaDecisoes
    + "<details><summary>prompt completo</summary><pre>" + p.prompt + "</pre></details>"
    + "<details><summary>propostas parseadas</summary><pre>" + p.propostas_parseadas + "</pre></details>"
    + "</div>";
}
function filtrarPropostas(){
  var f = {modelo: val("p-modelo"), epoca: val("p-epoca"), particao: val("p-particao"),
           aceita: val("p-aceita"), motivo: val("p-motivo"), acerto: val("p-acerto")};
  var sel = DADOS_PROPOSTAS.filter(function(d){
    return (!f.modelo || d.modelo === f.modelo)
        && (!f.epoca || String(d.epoca) === f.epoca)
        && (!f.particao || d.particao === f.particao)
        && (!f.aceita || d.aceite === f.aceita)
        && (!f.motivo || d.motivos_rejeicao.indexOf(f.motivo) !== -1)
        && (!f.acerto || String(d.acertou_diagnostico ? 1 : 0) === f.acerto);
  });
  document.getElementById("p-contagem").textContent = sel.length + " de " + DADOS_PROPOSTAS.length + " registros";
  document.getElementById("lista-propostas").innerHTML = sel.slice(0, LIMITE_CARTOES).map(cartaoProposta).join("")
    + (sel.length > LIMITE_CARTOES ? "<p style=\\"color:#52514e\\">mostrando os " + LIMITE_CARTOES + " primeiros — refine os filtros</p>" : "");
}
["p-modelo","p-epoca","p-particao","p-aceita","p-motivo","p-acerto"].forEach(function(id){
  document.getElementById(id).addEventListener("change", filtrarPropostas);
});
filtrarPropostas();

// ------------------------------------------------------------- diagnósticos caso a caso
var DADOS_DIAGNOSTICOS = __DADOS_DIAGNOSTICOS__;
opcoes("d-modelo", unicos(DADOS_DIAGNOSTICOS, "modelo"));
opcoes("d-biblioteca", unicos(DADOS_DIAGNOSTICOS, "biblioteca_epoca"));
opcoes("d-particao", unicos(DADOS_DIAGNOSTICOS, "particao"));
opcoes("d-classe", unicos(DADOS_DIAGNOSTICOS, "classe"));
opcoes("d-nivel", unicos(DADOS_DIAGNOSTICOS, "nivel"));

function cartaoDiagnostico(d){
  return "<div class=\\"caso\\"><header><b>" + d.caso + "</b><span>" + d.modelo + "</span>"
    + "<span>L" + d.biblioteca_epoca + " / " + d.particao + "</span>"
    + "<span>" + CLASSES[d.classe] + " · nível " + d.nivel + "</span>"
    + "<span class=\\"" + (d.causa_correta ? "ok" : "erro") + "\\">" + (d.causa_correta ? "acertou" : "errou") + "</span>"
    + "<span>esperado: <code>" + d.causa_esperada + "</code> · respondeu: <code>" + d.causa_respondida + "</code></span>"
    + "<span>notas no contexto: " + d.notas_no_contexto + "</span>"
    + (d.segundos == null ? "" : "<span>" + d.segundos + " s"
        + (d.prefill_ms ? " · prefill " + d.prefill_ms + " ms" : "") + "</span>")
    + "</header>"
    + (d.verbetes_ids.length
        ? "<div style=\\"font-size:12px;color:#52514e\\">verbetes: " + d.verbetes_ids.join(", ")
          + (d.verbete_ouro ? " · ouro: " + d.verbete_ouro : "") + "</div>"
        : "")
    + "<pre>" + d.resposta + "</pre>"
    + "<details><summary>sintoma do caso</summary><pre>" + d.sintoma + "</pre></details>"
    + "</div>";
}
function filtrarDiagnosticos(){
  var f = {modelo: val("d-modelo"), biblioteca: val("d-biblioteca"), particao: val("d-particao"),
           classe: val("d-classe"), nivel: val("d-nivel"), acerto: val("d-acerto")};
  var sel = DADOS_DIAGNOSTICOS.filter(function(d){
    return (!f.modelo || d.modelo === f.modelo)
        && (!f.biblioteca || String(d.biblioteca_epoca) === f.biblioteca)
        && (!f.particao || d.particao === f.particao)
        && (!f.classe || String(d.classe) === f.classe)
        && (!f.nivel || String(d.nivel) === f.nivel)
        && (!f.acerto || String(d.causa_correta ? 1 : 0) === f.acerto);
  });
  document.getElementById("d-contagem").textContent = sel.length + " de " + DADOS_DIAGNOSTICOS.length + " registros";
  document.getElementById("lista-diagnosticos").innerHTML = sel.slice(0, LIMITE_CARTOES).map(cartaoDiagnostico).join("")
    + (sel.length > LIMITE_CARTOES ? "<p style=\\"color:#52514e\\">mostrando os " + LIMITE_CARTOES + " primeiros — refine os filtros</p>" : "");
}
["d-modelo","d-biblioteca","d-particao","d-classe","d-nivel","d-acerto"].forEach(function(id){
  document.getElementById(id).addEventListener("change", filtrarDiagnosticos);
});
filtrarDiagnosticos();
</script>
</body></html>
"""


# --------------------------------------------------------------------------- tabelas (servidor)

def _tabela_generica(linhas: list[dict], campos: list[tuple[str, str]]) -> str:
    """! Alteração de IA - Revisar: monta uma <table> a partir de uma lista de linhas e uma
    lista (campo, rótulo) — mesma forma de gerar_relatorio._tabela, reaproveitada aqui nas
    cinco tabelas server-side do relatório (resumo, documentação, pareado, Cochran, flips).
    ! Motivo: as cinco têm a MESMA estrutura (cabeçalho de rótulos, uma linha por registro,
    valor ausente vira "—", lista de 2 vira "a–b", tudo passando por html.escape) — só os
    campos mudam de uma para outra. Repetir a montagem cinco vezes seria cinco lugares para o
    mesmo defeito de escaping aparecer se um deles fosse escrito à mão em vez de reaproveitado."""
    if not linhas:
        return '<p style="color:#52514e">sem dados.</p>'
    cab = "".join(f"<th>{html.escape(r)}</th>" for _, r in campos)
    corpo = []
    for linha in linhas:
        celulas = []
        for campo, _ in campos:
            v = linha.get(campo)
            if isinstance(v, list):
                v = f"{v[0]}–{v[1]}"
            celulas.append(f'<td class="num">{html.escape(str(v if v is not None else "—"))}</td>')
        corpo.append("<tr>" + "".join(celulas) + "</tr>")
    tabela = f"<table><thead><tr>{cab}</tr></thead><tbody>{''.join(corpo)}</tbody></table>"
    return f'<div class="tabela-scroll">{tabela}</div>'


def _tabela_resumo(resumo: dict) -> str:
    """! Alteração de IA - Revisar: a tabela 1 do relatório (modelo × biblioteca × partição),
    ligando resumo["por_modelo_biblioteca_particao"] a CAMPOS_TABELA_FASE3.
    ! Motivo: função própria (e não a chamada direta de _tabela_generica em main) para o nome
    no template (__TABELA_RESUMO__) apontar para um lugar só, e para trocar a chave do resumo
    lida aqui sem mexer em gerar_relatorio()."""
    linhas = resumo.get("por_modelo_biblioteca_particao", [])
    return _tabela_generica(linhas, CAMPOS_TABELA_FASE3)


def _num_ou_traco(v) -> str:
    """! Alteração de IA - Revisar: "—" para None, senão str(v).
    ! Motivo: as medianas de prefill (proposta e diagnóstico) podem faltar quando nenhum
    registro do grupo tem os dois campos (avaliar_fase3._ms_por_token devolve None nesse
    caso) — juntar "None" cru na coluna "X / Y" ficaria ilegível."""
    return "—" if v is None else str(v)


def _linha_documentacao(d: dict) -> dict:
    """! Alteração de IA - Revisar: achata um registro de resumo["documentacao"] (que traz
    por_operacao e motivos_rejeicao como dicionários aninhados) nas colunas planas que
    CAMPOS_DOCUMENTACAO espera.
    ! Motivo: _tabela_generica só lê linha.get(campo) direto — sem achatar aqui, "notas
    aceitas" (dentro de por_operacao["nota"]["aceitas"]) e o top-3 de motivos (que precisa de
    ordenar o histograma e formatar como texto) não teriam onde entrar na tabela genérica sem
    duplicar a lógica de avaliar_fase3.imprimir_resumo em cada uma das cinco tabelas."""
    top = sorted(((n, c) for c, n in d["motivos_rejeicao"].items() if n), reverse=True)[:3]
    top3 = ", ".join(f"{c} {n}" for n, c in top) or "nenhuma rejeição"
    por_op = d.get("por_operacao", {})
    return {
        "modelo": d["modelo"], "epoca": d["epoca"],
        "n_propostas": d["n_propostas"], "n_aceitas": d["n_aceitas"],
        "aceitas_pct": d["aceitas_pct"], "n_nenhuma": d["n_nenhuma"],
        "n_respostas_truncadas": d["n_respostas_truncadas"],
        "notas_aceitas": por_op.get("nota", {}).get("aceitas", 0),
        "retificacoes_aceitas": por_op.get("retificacao", {}).get("aceitas", 0),
        "verbetes_novos_aceitos": por_op.get("novo_verbete", {}).get("aceitas", 0),
        "tokens_md_estimados_acrescentados": d["tokens_md_estimados_acrescentados"],
        "tentativas_de_decorar": d["tentativas_de_decorar"],
        "prefill_proposta_vs_diagnostico": (
            f"{_num_ou_traco(d['prefill_ms_por_token_proposta'])} / "
            f"{_num_ou_traco(d['prefill_ms_por_token_diagnostico'])}"),
        "top3_motivos_rejeicao": top3,
    }


def _tabela_documentacao(resumo: dict) -> str:
    """! Alteração de IA - Revisar: a tabela 2 (documentação por época), ordenada por
    (modelo, época) antes de render.
    ! Motivo: resumo["documentacao"] sai de avaliar_saida concatenado slug por slug (ordem
    alfabética de pasta), cada um já em ordem de época — mas isso agrupa por modelo, não
    intercala por época; a ordenação aqui é só para a leitura ficar previsível (modelo A
    E1..E3, modelo B E1..E3), sem depender da ordem de iteração dos slugs no disco."""
    linhas = sorted(resumo.get("documentacao", []), key=lambda d: (d["modelo"], d["epoca"]))
    return _tabela_generica([_linha_documentacao(d) for d in linhas], CAMPOS_DOCUMENTACAO)


def _tabela_pareado(resumo: dict) -> str:
    """! Alteração de IA - Revisar: a tabela 3a (Δ pareado contra a L0), com o p de Holm
    marcado com "*" quando < 0,05.
    ! Motivo: mesma regra do console de avaliar_fase3.imprimir_resumo — marcar o p AJUSTADO
    (e não o bruto) evita que quem lê o relatório julgue "significativo" uma das três
    comparações a 5% brutos sem lembrar do ajuste de Holm."""
    linhas = []
    for p in resumo.get("pareado_vs_L0", []):
        marca = "*" if p["p_holm"] is not None and p["p_holm"] < 0.05 else ""
        linhas.append({**p, "p_holm_marcado": f"{p['p_holm']}{marca}"
                       if p["p_holm"] is not None else "—"})
    return _tabela_generica(linhas, CAMPOS_PAREADO)


def _tabela_cochran(resumo: dict) -> str:
    """! Alteração de IA - Revisar: a tabela 3b (Cochran Q sobre as versões de biblioteca).
    ! Motivo: função própria (em vez de chamar _tabela_generica direto do template) para o
    nome __TABELA_COCHRAN__ ficar ligado a uma única linha de código, igual às outras quatro
    tabelas deste relatório."""
    return _tabela_generica(resumo.get("cochran_q", []), CAMPOS_COCHRAN)


def _tabela_flips(resumo: dict) -> str:
    """! Alteração de IA - Revisar: a tabela 3c (flips entre épocas por transição/partição).
    ! Motivo: resumo["flips"] (recorte por partição) é o pedido no briefing ("flips por
    transição"); resumo["flips_por_classe"] fica de fora desta tabela — é outro recorte dos
    mesmos números, e mostrar os dois duplicaria a tabela sem nenhum filtro para diferenciá-
    las."""
    return _tabela_generica(resumo.get("flips", []), CAMPOS_FLIPS)


# ------------------------------------------------------------------------- diffs por época

def _bloco_diffs(c3: dict, slugs: list[str], nome_por_slug: dict[str, str]) -> str:
    """! Alteração de IA - Revisar: um <details> por modelo e época com o conteúdo de
    bibliotecas/<slug>/diff__E<n>.md, escapado.
    ! Motivo: diff__E<n>.md é GERADO por evolucao_biblioteca.escrever_diff a cada
    fechar_epoca e fica FORA da pasta epoca-n/ (irmão dela, não dentro — ver a atualização
    após a Tarefa 5 no briefing desta tarefa); sem juntar aqui, ler o que cada modelo mudou em
    cada época seria abrir de 3 a 12 arquivos .md à mão, pasta por pasta. Escapado porque o
    diff pode conter qualquer caractere que o modelo tenha escrito num verbete, inclusive '<'
    ou '>' dentro de um trecho de código citado na nota."""
    blocos = []
    for slug in slugs:
        modelo = nome_por_slug.get(slug, slug)
        pasta_bib = c3["bibliotecas"] / slug
        for epoca in sorted(n for n in avaliar_fase3.snapshots_do_modelo(c3, slug) if n >= 1):
            arquivo = pasta_bib / f"diff__E{epoca}.md"
            if not arquivo.exists():
                continue
            texto = arquivo.read_text(encoding="utf-8")
            blocos.append(
                f"<details><summary>{html.escape(modelo)} — diff__E{epoca}</summary>"
                f"<pre>{html.escape(texto)}</pre></details>")
    return "".join(blocos) or '<p style="color:#52514e">nenhum diff__E&lt;n&gt;.md encontrado.</p>'


# ---------------------------------------------------------------- dados embutidos (JSON)

def _dado_diagnostico(a: dict, bruto: dict, sintoma: str) -> dict:
    """! Alteração de IA - Revisar: monta o registro de UM diagnóstico para o JSON embutido —
    junta avaliacao_fase3.json (acerto, causa esperada/respondida, ancoragem) com o bruto do
    JSONL (resposta, verbetes_ids, verbete_ouro), e ESCAPA aqui, ANTES do json.dumps, todo
    campo de texto livre.
    ! Motivo: avaliar_registro_fase3 não grava a resposta crua nem os ids recuperados (só os
    booleanos citou_verbete/ouro_no_contexto) — por isso a junção com o JSONL pela chave
    (modelo, biblioteca_epoca, caso), do jeito que gerar_relatorio.py já faz para a Fase 2-B.
    resposta e sintoma são texto que o MODELO (ou o banco de casos) escreveu — podem conter
    qualquer coisa, inclusive algo que pareça HTML/script; escapando aqui o arquivo estático já
    grava o texto seguro, e o JavaScript que monta o cartão só concatena (escapar de novo lá
    trocaria "&lt;" por "&amp;lt;" na tela)."""
    return {
        "caso": html.escape(a["caso"]), "modelo": html.escape(a["modelo"]),
        "biblioteca_epoca": a["biblioteca_epoca"], "particao": html.escape(a["particao"] or ""),
        "classe": a["classe"], "nivel": a["nivel"],
        "causa_correta": bool(a["causa_correta"]),
        "causa_esperada": html.escape(a["causa_esperada"] or ""),
        "causa_respondida": html.escape(a["causa_respondida"] or ""),
        "notas_no_contexto": a["notas_no_contexto"],
        "verbetes_ids": [html.escape(i) for i in bruto.get("verbetes_ids", [])],
        "verbete_ouro": html.escape(bruto.get("verbete_ouro") or ""),
        "segundos": a.get("segundos"), "prefill_ms": a.get("prefill_ms"),
        "resposta": html.escape(bruto.get("resposta", "")),
        "sintoma": html.escape(sintoma),
    }


def _dado_proposta(p: dict) -> dict:
    """! Alteração de IA - Revisar: monta o registro de UMA proposta para o JSON embutido,
    direto do JSONL (propostas não passam por avaliar_fase3 — quem avalia diagnóstico é
    avaliar_registro_fase3, proposta não tem "acerto" próprio), com o mesmo escape de texto
    livre de _dado_diagnostico mais um resumo de aceite para o filtro.
    ! Motivo: resposta, prompt, e o texto/motivo/detalhe de cada decisão são texto que o
    MODELO escreveu — mesmo risco de _dado_diagnostico. O filtro "aceita" do briefing (sim/
    não/nenhuma) pede um valor por CARTÃO, mas um cartão (uma proposta) pode trazer de 0 a N
    blocos com aceita diferente cada um; "aceite" resume isso: nenhuma quando o modelo
    respondeu NENHUMA (nenhum bloco), sim quando ao menos um bloco foi aceito, não quando
    houve proposta mas nenhum bloco foi aceito."""
    if p.get("nenhuma"):
        aceite = "nenhuma"
    elif p.get("n_aceitas", 0) > 0:
        aceite = "sim"
    else:
        aceite = "não"
    decisoes = [{
        "numero": d.get("numero", 0),
        "operacao": html.escape(d.get("operacao") or ""),
        "verbete": html.escape(d.get("verbete") or ""),
        "aceita": bool(d.get("aceita")),
        "motivo": html.escape(d.get("motivo") or ""),
        "detalhe": html.escape(d.get("detalhe") or ""),
    } for d in p.get("decisoes", [])]
    return {
        "caso": html.escape(p["caso"]), "modelo": html.escape(p["modelo"]),
        "epoca": p["epoca"], "particao": html.escape(p.get("particao") or ""),
        "acertou_diagnostico": bool(p.get("acertou_diagnostico")),
        "causa_correta_mostrada": html.escape(p.get("causa_correta_mostrada") or ""),
        "ids_visiveis": [html.escape(i) for i in p.get("ids_visiveis", [])],
        "resposta": html.escape(p.get("resposta", "")),
        "prompt": html.escape(p.get("prompt", "")),
        "propostas_parseadas": html.escape(json.dumps(
            p.get("propostas_parseadas", []), ensure_ascii=False, indent=2)),
        "decisoes": decisoes, "aceite": aceite,
        "n_propostas": p.get("n_propostas", 0), "n_aceitas": p.get("n_aceitas", 0),
        "motivos_rejeicao": [html.escape(m) for m in p.get("motivos_rejeicao", [])],
        "segundos": p.get("segundos"), "prefill_ms": p.get("prefill_ms"),
    }


def _json_seguro(dados: list[dict]) -> str:
    """! Alteração de IA - Revisar: json.dumps com uma segunda linha de defesa contra
    "</script>" no meio do JSON embutido — troca "</" por "<\\/" no texto já serializado.
    ! Motivo: cada campo de texto livre já passou por html.escape em _dado_diagnostico/
    _dado_proposta (o que elimina todo "<" e ">" vindo de dado), mas esta troca cobre também
    qualquer campo que um cartão futuro venha a acrescentar sem escapar — "<\\/" é uma barra
    escapada dentro de uma string JSON válida (json.loads devolve "/" de volta) e nunca forma
    a sequência "</script" que o parser HTML procura para fechar a tag."""
    return json.dumps(dados, ensure_ascii=False).replace("</", "<\\/")


# ------------------------------------------------------------------------------- orquestração

def gerar_relatorio(c3: dict) -> Path | None:
    """! Alteração de IA - Revisar: lê avaliacao_fase3.json, resumo_fase3.json e os JSONL/diff
    de cada modelo em c3["raiz"], monta a página e grava em c3["relatorio"]. Devolve o caminho
    gravado, ou None se avaliacao_fase3.json/resumo_fase3.json ainda não existirem.
    ! Motivo: separar a montagem da leitura de argumentos (main() abaixo só cuida de --saida e
    impressão) é o que permite ao teste chamar esta função direto com o c3 de uma árvore
    sintética em pasta temporária, do mesmo jeito que avaliar_fase3.avaliar_saida(c3) já faz —
    sem subir um subprocesso nem depender de sys.argv."""
    if not c3["resumo"].exists() or not c3["avaliacao"].exists():
        return None
    resumo = json.loads(c3["resumo"].read_text(encoding="utf-8"))
    avaliacao = json.loads(c3["avaliacao"].read_text(encoding="utf-8"))

    slugs = avaliar_fase3.slugs_da_saida(c3)
    diagnosticos_todos: list[dict] = []
    propostas_todos: list[dict] = []
    nome_por_slug: dict[str, str] = {}
    for slug in slugs:
        diagnosticos, propostas = avaliar_fase3.carregar_modelo(c3, slug)
        nome_por_slug[slug] = diagnosticos[0]["modelo"] if diagnosticos else slug.replace("_", ":")
        diagnosticos_todos += diagnosticos
        propostas_todos += propostas

    brutos = {(r["modelo"], r["biblioteca_epoca"], r["caso"]): r for r in diagnosticos_todos}
    from banco_casos import CASOS
    from banco_casos_extra import CASOS_EXTRA
    sintomas = {c["id"]: c["entrada"].get("sintoma", "") for c in CASOS + CASOS_EXTRA}

    dados_diag = [_dado_diagnostico(
        a, brutos.get((a["modelo"], a["biblioteca_epoca"], a["caso"]), {}),
        sintomas.get(a["caso"], "")) for a in avaliacao]
    dados_prop = [_dado_proposta(p) for p in propostas_todos]

    # ! Alteração de IA - Revisar: os placeholders __NOME__ do template são trocados numa
    # passada só (re.sub com callback), e não por uma cadeia de .replace — onda final (item 7).
    # ! Motivo: com a cadeia, o texto inserido por uma troca era varrido pelas trocas
    # seguintes: uma resposta do modelo contendo a sequência literal "__DADOS_DIAGNOSTICOS__"
    # (dentro do JSON de propostas) recebia o JSON de diagnósticos inteiro no lugar — o
    # arquivo dobrava de tamanho e o JavaScript quebrava ao ler a string. Com uma passada
    # única sobre o template, o que o modelo escreveu nunca é reinterpretado como marcador.
    trocas = {
        "__RAIZ__": html.escape(str(c3["raiz"])),
        "__TABELA_RESUMO__": _tabela_resumo(resumo),
        "__TABELA_DOCUMENTACAO__": _tabela_documentacao(resumo),
        "__TABELA_PAREADO__": _tabela_pareado(resumo),
        "__TABELA_COCHRAN__": _tabela_cochran(resumo),
        "__TABELA_FLIPS__": _tabela_flips(resumo),
        "__DIFFS__": _bloco_diffs(c3, slugs, nome_por_slug),
        "__DADOS_PROPOSTAS__": _json_seguro(dados_prop),
        "__DADOS_DIAGNOSTICOS__": _json_seguro(dados_diag),
    }
    pagina = re.sub(r"__[A-Z_]+__", lambda m: trocas[m.group(0)], _MODELO)

    destino = c3["relatorio"]
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(pagina, encoding="utf-8")
    print(f"{destino} ({len(dados_diag)} diagnóstico(s), {len(dados_prop)} proposta(s), "
          f"{round(destino.stat().st_size / 1024)} KB)")
    return destino


# ! Alteração de IA - Revisar: linha de comando — --saida escolhe a subpasta dos resultados da
# Fase 3 (ver caminhos.fase3), igual a avaliar_fase3.py e gerar_graficos_fase3.py.
# ! Motivo: a mesma --saida das outras ferramentas da Fase 3 deixa o comando anotado no
# caderno de laboratório igual nas três (avaliar, gráficos, relatório) — trocar a convenção só
# aqui obrigaria a lembrar qual script usa qual nome de opção.
def main() -> None:
    ap = argparse.ArgumentParser(
        description="Relatório HTML navegável da Fase 3: resumo, documentação por época, "
                    "comparação pareada, propostas e diagnósticos caso a caso, diffs.")
    ap.add_argument("--saida", default="fase3",
                    help="subpasta dos resultados da Fase 3 (ver caminhos.fase3)")
    args = ap.parse_args()

    print(caminhos.descricao())
    c3 = caminhos.fase3(args.saida)
    destino = gerar_relatorio(c3)
    if destino is None:
        print(f"avaliacao_fase3.json ou resumo_fase3.json não encontrado em {c3['raiz']}. "
              "Rode avaliar_fase3.py primeiro.")


if __name__ == "__main__":
    main()
