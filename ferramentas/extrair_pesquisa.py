# ! Alteração de IA - Revisar: script novo (21/09/2026) que recolhe, dos artefatos salvos do Workflow de pesquisa
# `wf_add7e8f0-e81` (arquivo de estado `wf_add7e8f0-e81.json` e diário `journal.jsonl`), tudo o que a rodada 2 já
# produziu e gera (a) a entrada fixa `r2-entrada.json`, (b) o script do Workflow curto `pesquisa-r2.js` e, depois da
# execução, (c) o `r2-final.json` mesclado que `render_levantamento.py` transforma em Markdown.
# ! Motivo: o Workflow antigo caiu três vezes por limite de sessão e, ao ser retomado, reaproveitou só 2,5% e 8,3% do
# cache e trocou a lista de lacunas a cada crítica. Tratar o que já foi verificado como entrada fixa (extraída aqui,
# em processamento local, sem tokens) evita rerodar ~300 agentes e garante que a lista de lacunas não muda de novo.
"""Uso:
  python ferramentas/extrair_pesquisa.py                 # concilia e grava .superpowers/sdd/fase3b-e-fechamento/pesquisa/r2-entrada.json
  python ferramentas/extrair_pesquisa.py --gerar-workflow  # + grava .superpowers/sdd/fase3b-e-fechamento/pesquisa-r2.js
  python ferramentas/extrair_pesquisa.py --mesclar <wf_xxx.json>  # junta a saída do Workflow curto em r2-final.json
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

RAIZ = Path(__file__).resolve().parents[1]
SDD = RAIZ / ".superpowers" / "sdd" / "fase3b-e-fechamento"
CC = (Path.home() / ".claude" / "projects" / "c--Users-Eric-Derre-Documents-TCC"
      / "5c1c8fa0-31ce-4489-b7e9-314bf40961a1")
ESTADO_PADRAO = CC / "workflows" / "wf_add7e8f0-e81.json"
DIARIO_PADRAO = CC / "subagents" / "workflows" / "wf_add7e8f0-e81" / "journal.jsonl"
SCRIPT_ANTIGO = RAIZ / ".superpowers" / "sdd" / "delegated-hopping-steele" / "pesquisa-fase3.js"

# Contagens conhecidas (levantadas em 21/09/2026 a partir do diário) — o script PARA se algo não bater.
ESPERADO_R2 = {
    "r2-conflito-contexto-conhecimento-e-sicofancia-documental": ("sintese_pendente", 20, 0),
    "r2-validacao-de-artefatos-gerados-e-limites-da-autocorrecao": ("sintese_pendente", 16, 4),
    "r2-prompting-em-estagios-e-cot-em-modelos-pequenos": ("sintese_pendente", 19, 0),
    "r2-metricas-de-qualidade-de-documentacao-e-inconsistencia-doc-codigo": ("verificacao_pendente", 0, 18),
    "r2-aprendizado-sem-atualizacao-de-pesos-e-ancoragem-em-faceli": ("verificacao_pendente", 0, 18),
    "r2-taxonomia-rotulos-ouro-e-rca-com-llm": ("verificacao_pendente", 0, 20),
    "r2-agente-autonomo-de-qa-autonomia-e-supervisao": ("completo", 20, 0),
    "r2-recuperacao-em-corpus-pequeno-curado-e-crescente": ("pesquisa_pendente", 0, 0),
}
CHAVES_R1 = ("tokenizacao", "arquitetura", "rag", "memoria", "metricas", "otimizacao", "faceli", "selfhealing")


def _ler_jsonl(caminho: Path):
    for linha in caminho.read_text(encoding="utf-8", errors="replace").splitlines():
        if linha.strip():
            try:
                yield json.loads(linha)
            except json.JSONDecodeError:
                continue


def resultados_do_diario(diario: Path) -> dict[str, list]:
    """label -> lista de resultados (na ordem do diário).

    As linhas `result` do diário não trazem o label, só `agentId`/`key`; o label está na linha
    `started` do mesmo agente — por isso a junção pelos dois identificadores."""
    label_por_id: dict[str, str] = {}
    exec_por_id: dict[str, int] = {}
    por_label: dict[str, list] = {}
    n_started = 0
    for r in _ler_jsonl(diario):
        ident = r.get("agentId") or r.get("key") or ""
        if r.get("type") == "started":
            label_por_id[ident] = r.get("label") or ""
            # as três execuções iniciaram 174, 174 e 297 agentes, nesta ordem (levantado em 21/09/2026)
            exec_por_id[ident] = 0 if n_started < 174 else (1 if n_started < 348 else 2)
            n_started += 1
        elif r.get("type") == "result":
            label = r.get("label") or label_por_id.get(ident, "")
            por_label.setdefault(label, []).append({"execucao": exec_por_id.get(ident, -1), "result": r.get("result")})
    return por_label


def _da_execucao(lista: list | None, execucao: int):
    """Resultado da execução pedida (0 = 11/09 manhã, 1 = 11/09 tarde, 2 = 13/09); -1 = a última que existir."""
    lista = lista or []
    if execucao < 0:
        return lista[-1]["result"] if lista else None
    for item in lista:
        if item["execucao"] == execucao:
            return item["result"]
    return None


def lista_b(por_label: dict[str, list], chaves_r2: set[str]) -> list[dict]:
    """A crítica cujas lacunas batem com as chaves r2 realmente executadas."""
    for item in reversed(por_label.get("critica", [])):
        res = item["result"]
        lac = (res or {}).get("lacunas") or []
        if {"r2-" + l["key"] for l in lac} == chaves_r2:
            return lac
    raise SystemExit("crítica com a lista B não encontrada no diário")


def compactar_verificada(v: dict) -> dict:
    return {k: v.get(k, "") for k in ("claim_pt", "number", "condition", "support", "ref", "url", "relevance")}


def _r1_do_diario(por_label: dict[str, list], k: str, execucao: str) -> dict:
    """Rodada 1 a partir do diário: `primeira` = execução de 11/09 (a que foi integrada no Memorial em
    §6.9.1–6.9.8); `ultima` = a de 13/09 (a que ficou no arquivo de estado). As três execuções rerodaram
    pesquisa, verificação e síntese, e os textos diferem — o Memorial cita a primeira."""
    idx = {"primeira": 0, "segunda": 1, "ultima": -1}[execucao]
    pesq = _da_execucao(por_label.get("pesquisa:" + k), idx) or {}
    sint = _da_execucao(por_label.get("sintese:" + k), idx)
    claims = pesq.get("claims") or []
    verified, rejeitadas = [], []
    for i, c in enumerate(claims):
        if i >= 20:
            rejeitadas.append({"claim": c.get("claim_pt", ""), "fonte": c.get("source_title", ""),
                               "motivo": "além do teto de 20 afirmações por tópico; não verificada"})
            continue
        d = _da_execucao(por_label.get(f"verifica:{k}#{i + 1}"), idx)
        if d and d.get("exists") and d.get("year_ok") and d.get("claim_supported") in ("yes", "partial"):
            verified.append({"claim_pt": c.get("claim_pt", ""), "number": d.get("corrected_number") or c.get("number", ""),
                             "condition": c.get("condition", ""), "support": d.get("claim_supported"),
                             "ref": d.get("corrected_citation", ""), "url": c.get("url", ""),
                             "relevance": c.get("relevance_to_project_pt", "")})
        else:
            rejeitadas.append({"claim": c.get("claim_pt", ""), "fonte": c.get("source_title", ""),
                               "motivo": (f"{d.get('claim_supported')} / exists={d.get('exists')} / year_ok={d.get('year_ok')} / {d.get('notes_pt', '')}"
                                          if d else "verificador falhou")})
    return {"summary_pt": pesq.get("summary_pt", ""), "verified": verified, "rejeitadas": rejeitadas,
            "synthesis": sint, "open_questions": pesq.get("open_questions_pt") or []}


def extrair(estado: Path, diario: Path, r1_execucao: str = "primeira") -> dict:
    d = json.loads(estado.read_text(encoding="utf-8"))
    topicos = {t["topic"]["key"]: t for t in d["result"]["topicos"]}
    por_label = resultados_do_diario(diario)
    chaves_r2 = {k for k in ESPERADO_R2}
    lacunas = {("r2-" + l["key"]): l for l in lista_b(por_label, chaves_r2)}

    saida = {"gerado_em": datetime.now().isoformat(timespec="seconds"), "estado": str(estado),
             "diario": str(diario), "r1": {}, "r2": {}}
    saida["r1_execucao"] = r1_execucao
    for k in CHAVES_R1:
        t = topicos[k]
        if r1_execucao == "estado":
            pesq = _da_execucao(por_label.get("pesquisa:" + k), -1) or {}
            item = {"summary_pt": pesq.get("summary_pt", ""), "verified": [compactar_verificada(v) for v in t.get("verified") or []],
                    "rejeitadas": t.get("rejeitadas") or [], "synthesis": t.get("synthesis"), "open_questions": t.get("open_questions") or []}
        else:
            item = _r1_do_diario(por_label, k, r1_execucao)
        saida["r1"][k] = {"titulo": t["topic"]["titulo"], **item}
    print("rodada 1 (" + r1_execucao + "):", {k: (len(v["verified"]), len(v["rejeitadas"]), "sint" if v["synthesis"] else "SEM") for k, v in saida["r1"].items()})
    problemas = []
    for k, (estado_esp, n_ver, n_rej) in ESPERADO_R2.items():
        lac = lacunas[k]
        t = topicos.get(k)
        pesq = _da_execucao(por_label.get("pesquisa:" + k), -1) or {}
        item = {"titulo": lac["titulo"], "prompt": lac["prompt"], "por_que_pt": lac.get("por_que_pt", ""),
                "estado": estado_esp, "summary_pt": pesq.get("summary_pt", ""),
                "claims": pesq.get("claims") or [], "open_questions_pt": pesq.get("open_questions_pt") or [],
                "verified": [compactar_verificada(v) for v in (t or {}).get("verified") or []],
                "rejeitadas": (t or {}).get("rejeitadas") or [], "synthesis": (t or {}).get("synthesis")}
        nv, nr = len(item["verified"]), len(item["rejeitadas"])
        if (nv, nr) != (n_ver, n_rej):
            problemas.append(f"{k}: esperado {n_ver} verificadas/{n_rej} rejeitadas, achado {nv}/{nr}")
        if estado_esp == "verificacao_pendente" and not item["claims"]:
            problemas.append(f"{k}: pesquisa sem claims no diário")
        if estado_esp == "sintese_pendente" and not item["summary_pt"]:
            problemas.append(f"{k}: summary_pt da pesquisa ausente no diário")
        if estado_esp == "completo" and not item["synthesis"]:
            problemas.append(f"{k}: síntese esperada e ausente")
        saida["r2"][k] = item
    print(f"{'lacuna':72s} estado                 verif rej claims síntese")
    for k, it in saida["r2"].items():
        print(f"{k:72s} {it['estado']:22s} {len(it['verified']):5d} {len(it['rejeitadas']):3d} {len(it['claims']):6d} {'sim' if it['synthesis'] else 'não'}")
    if problemas:
        raise SystemExit("conciliação falhou:\n  " + "\n  ".join(problemas))
    return saida


def _trecho_script_antigo(inicio: str, fim: str) -> str:
    s = SCRIPT_ANTIGO.read_text(encoding="utf-8")
    a = s.index(inicio)
    b = s.index(fim, a)
    return s[a:b]


def gerar_workflow(entrada: dict, destino: Path) -> None:
    """Escreve o Workflow curto com a entrada inlinada (sem acesso a disco dentro do script)."""
    cabecalho = _trecho_script_antigo("const CONTEXTO = [", "const TOPICOS = [")  # CONTEXTO + REGRAS
    esquemas = _trecho_script_antigo("const FINDINGS = {", "function promptPesquisa(")  # FINDINGS, VERDICT, SYNTH, CRITIC
    # entrada enxuta para o script: só o que os prompts precisam
    # O Workflow aceita scripts de até 512 KB com a entrada inlinada: os campos que só alimentam o mapa
    # (afirmações da rodada 1 e dos tópicos já completos) entram truncados; o que vai ser verificado ou
    # sintetizado entra inteiro, só com a relevância encurtada.
    def _t(texto: str, n: int) -> str:
        texto = (texto or "").strip()
        return texto if len(texto) <= n else texto[: n - 1] + "…"

    def _para_mapa(v: dict) -> dict:
        return {"claim_pt": _t(v.get("claim_pt"), 260), "number": _t(v.get("number"), 120),
                "condition": _t(v.get("condition"), 140), "ref": _t(v.get("ref"), 110)}

    compacto = {"r1": {}, "r2": {}}
    for k, it in entrada["r1"].items():
        s = it["synthesis"] or {}
        compacto["r1"][k] = {"titulo": it["titulo"], "implicacoes": [_t(x, 400) for x in s.get("implicacoes_fase3_pt", [])],
                             "verified": [_para_mapa(v) for v in it["verified"]]}
    for k, it in entrada["r2"].items():
        completo = it["estado"] == "completo"
        compacto["r2"][k] = {
            "titulo": it["titulo"], "prompt": it["prompt"], "estado": it["estado"],
            "summary_pt": "" if completo else it["summary_pt"],
            "claims": [{**c, "relevance_to_project_pt": _t(c.get("relevance_to_project_pt"), 220)} for c in it["claims"]]
                      if it["estado"] == "verificacao_pendente" else [],
            "verified": [_para_mapa(v) for v in it["verified"]] if completo
                        else [{**v, "relevance": _t(v.get("relevance"), 220), "condition": _t(v.get("condition"), 400)} for v in it["verified"]],
            "implicacoes": [_t(x, 400) for x in (it["synthesis"] or {}).get("implicacoes_fase3_pt", [])],
        }
    dados = json.dumps(compacto, ensure_ascii=False)
    script = f"""export const meta = {{
  name: 'pesquisa-r2',
  description: 'Fecha a rodada 2 da pesquisa bibliografica da Fase 3 a partir do que ja foi verificado: 3 sinteses diretas, 56 verificacoes + 3 sinteses, 1 pesquisa nova com verificacao e sintese, e o mapa de decisoes',
  phases: [
    {{ title: 'Verificação', detail: 'verificadores ceticos (Sonnet) para as 3 lacunas pesquisadas sem verificacao e para a lacuna nova' }},
    {{ title: 'Síntese', detail: 'texto em portugues para o Memorial, so com afirmacoes que sobreviveram' }},
    {{ title: 'Mapa', detail: 'mapa achado -> numero -> fonte -> decisao da Fase 3, com as 16 sinteses' }},
  ],
}}

{cabecalho}
{esquemas}
const MAPA = {{
  type: 'object',
  properties: {{
    linhas: {{ type: 'array', items: {{ type: 'object', properties: {{ achado: {{ type: 'string' }}, numero: {{ type: 'string' }}, fonte: {{ type: 'string' }}, decisao_fase3: {{ type: 'string' }} }}, required: ['achado', 'numero', 'fonte', 'decisao_fase3'] }} }},
    riscos: {{ type: 'array', items: {{ type: 'object', properties: {{ risco: {{ type: 'string' }}, mitigacao: {{ type: 'string' }}, fonte: {{ type: 'string' }} }}, required: ['risco', 'mitigacao', 'fonte'] }} }},
    metricas: {{ type: 'array', items: {{ type: 'object', properties: {{ metrica: {{ type: 'string' }}, fonte: {{ type: 'string' }} }}, required: ['metrica', 'fonte'] }} }},
    capitulos_faceli: {{ type: 'array', items: {{ type: 'object', properties: {{ capitulo: {{ type: 'string' }}, secao_memorial: {{ type: 'string' }} }}, required: ['capitulo', 'secao_memorial'] }} }},
    leitura_pt: {{ type: 'string' }},
  }},
  required: ['linhas', 'riscos', 'metricas', 'capitulos_faceli', 'leitura_pt'],
}}

const ENTRADA = {dados}

function promptPesquisa(t) {{
  return CONTEXTO + '\\n\\n' + REGRAS + '\\n\\nTOPICO: ' + t.titulo + '\\n' + t.prompt
}}

function promptVerifica(c, titulo) {{
  return [
    'Voce e um verificador CETICO de citacoes para um TCC. Somente leitura: use WebSearch/WebFetch; nao escreva arquivos.',
    'Topico: ' + titulo,
    'Afirmacao: ' + c.claim_pt,
    'Numero declarado: ' + c.number + ' | Condicao: ' + c.condition,
    'Citacao declarada: ' + c.authors + '. ' + c.source_title + '. ' + c.venue + ', ' + c.year + '. ' + c.url,
    '',
    'Tarefas: (1) confirme que a fonte existe com esse titulo e autores (busque o titulo exato entre aspas; abra a pagina/abstract); (2) confirme o ano: year_ok=true se publicado em 2024 ou depois, OU se for o livro Faceli et al., OU se a citacao for de fonte classica citada por trabalho de 2024+; (3) confirme se o NUMERO e a CONDICAO declarados aparecem na fonte: claim_supported = yes (numero e condicao batem), partial (a fonte sustenta a ideia mas o numero ou a condicao divergem: diga o valor certo em corrected_number), no (a fonte diz outra coisa), unverifiable (nao conseguiu abrir a fonte).',
    'Em corrected_citation escreva a citacao correta e completa no formato: SOBRENOME, Nome; ... Titulo. Veiculo, ano. DOI/URL. (formato ABNT NBR 6023).',
    'Em notes_pt explique em 2-4 frases o que voce checou e o que encontrou. Resposta final: apenas o JSON do esquema.',
  ].join('\\n')
}}

function linhaVerificada(v, i) {{
  return (i + 1) + '. ' + v.claim_pt + ' [numero: ' + v.number + '; condicao: ' + v.condition + '; suporte: ' + v.support + '] REF: ' + v.ref + (v.relevance ? ' | relevancia: ' + v.relevance : '')
}}

function promptSintese(titulo, summary, verificadas) {{
  const aceitas = verificadas.map(linhaVerificada).join('\\n')
  return [
    CONTEXTO,
    '',
    'Voce vai escrever a secao de fundamentacao teorica sobre "' + titulo + '" para o Memorial de Desenvolvimento do TCC, em portugues do Brasil, com APENAS as afirmacoes verificadas abaixo (nao acrescente fontes novas; nao invente numeros; onde o suporte for partial, use o numero corrigido e marque "[parcial]").',
    'Resumo preliminar do pesquisador (use como guia de estrutura, mas confie so nas afirmacoes verificadas): ' + summary,
    '',
    'AFIRMACOES VERIFICADAS:',
    aceitas || '(nenhuma sobreviveu - diga isso e escreva um texto curto apontando o que precisa ser pesquisado)',
    '',
    'Produza: titulo; texto_memorial_pt (800-1500 palavras, com numero e condicao em cada afirmacao e citacao autor-data entre parenteses, ex.: (LIU et al., 2024); marque com "[parcial]" as afirmacoes de suporte partial); implicacoes_fase3_pt (8-14 itens, cada um terminando com a referencia entre parenteses no padrao "(AUTOR et al., ANO - afirmacao N)"); lacunas_pt (o que a literatura levantada NAO responde para este projeto, 5-12 itens, incluindo se o livro Faceli et al. ficou de fora e por que); referencias_abnt (uma entrada ABNT NBR 6023 por fonte citada, ordem alfabetica, terminando em "Acesso em: 21 set. 2026."). Resposta final: apenas o JSON do esquema.',
  ].join('\\n')
}}

function paraVerificada(c, d) {{
  return {{ claim_pt: c.claim_pt, number: d.corrected_number || c.number, condition: c.condition, support: d.claim_supported, ref: d.corrected_citation, url: c.url, relevance: c.relevance_to_project_pt || '' }}
}}

async function verificaTudo(key, titulo, claims) {{
  const lista = claims.slice(0, 20)
  if (claims.length > 20) log(key + ': ' + (claims.length - 20) + ' afirmacoes alem do teto de 20 ficaram sem verificacao')
  const vereditos = await parallel(lista.map((c, i) => () =>
    agent(promptVerifica(c, titulo), {{ label: 'verifica:' + key + '#' + (i + 1), phase: 'Verificação', schema: VERDICT, agentType: 'Explore', model: 'sonnet', effort: 'medium' }})))
  const verificadas = [], rejeitadas = []
  lista.forEach((c, i) => {{
    const d = vereditos[i]
    if (d && d.exists && d.year_ok && (d.claim_supported === 'yes' || d.claim_supported === 'partial')) verificadas.push(paraVerificada(c, d))
    else rejeitadas.push({{ claim: c.claim_pt, fonte: c.source_title, motivo: d ? (d.claim_supported + ' / exists=' + d.exists + ' / year_ok=' + d.year_ok + ' / ' + d.notes_pt) : 'verificador falhou' }})
  }})
  log(key + ': ' + verificadas.length + '/' + lista.length + ' afirmacoes sobreviveram a verificacao')
  return {{ verificadas, rejeitadas }}
}}

async function sintetiza(key, titulo, summary, verificadas) {{
  return agent(promptSintese(titulo, summary, verificadas), {{ label: 'sintese:' + key, phase: 'Síntese', schema: SYNTH, agentType: 'Explore', effort: 'high' }})
}}

async function fechaLacuna(key) {{
  const it = ENTRADA.r2[key]
  let verificadas = it.verified, rejeitadas = [], pesquisa = null
  if (it.estado === 'pesquisa_pendente') {{
    pesquisa = await agent(promptPesquisa({{ titulo: it.titulo, prompt: it.prompt }}), {{ label: 'pesquisa:' + key, phase: 'Verificação', schema: FINDINGS, agentType: 'Explore', effort: 'high' }})
    if (!pesquisa) {{ log('pesquisa:' + key + ' falhou'); return {{ key, pesquisa: null, verificadas: [], rejeitadas: [], synthesis: null }} }}
    const r = await verificaTudo(key, it.titulo, pesquisa.claims)
    verificadas = r.verificadas; rejeitadas = r.rejeitadas
  }} else if (it.estado === 'verificacao_pendente') {{
    const r = await verificaTudo(key, it.titulo, it.claims)
    verificadas = r.verificadas; rejeitadas = r.rejeitadas
  }}
  const summary = pesquisa ? pesquisa.summary_pt : it.summary_pt
  const synthesis = await sintetiza(key, it.titulo, summary, verificadas)
  return {{ key, pesquisa, verificadas, rejeitadas, synthesis, open_questions: pesquisa ? (pesquisa.open_questions_pt || []) : [] }}
}}

const pendentes = Object.keys(ENTRADA.r2).filter(k => ENTRADA.r2[k].estado !== 'completo')
log('Lacunas a fechar: ' + pendentes.length + ' (3 so sintese, 3 verificacao + sintese, 1 pesquisa completa)')
const fechadas = (await parallel(pendentes.map(k => () => fechaLacuna(k)))).filter(Boolean)
const porChave = {{}}
for (const f of fechadas) porChave[f.key] = f
log('Sinteses concluidas: ' + fechadas.filter(f => f.synthesis).length + '/' + pendentes.length)

phase('Mapa')
function blocoTopico(titulo, implicacoes, verificadas) {{
  return '### ' + titulo + '\\nImplicacoes: ' + (implicacoes || []).join(' | ') + '\\nAfirmacoes verificadas: ' + (verificadas || []).map((v, i) => (i + 1) + ') ' + v.claim_pt + ' [' + v.number + '; ' + v.condition + '] (' + v.ref + ')').join(' ')
}}
const blocos = []
for (const k of Object.keys(ENTRADA.r1)) blocos.push(blocoTopico(ENTRADA.r1[k].titulo, ENTRADA.r1[k].implicacoes, ENTRADA.r1[k].verified))
for (const k of Object.keys(ENTRADA.r2)) {{
  const it = ENTRADA.r2[k]
  const f = porChave[k]
  const impl = f && f.synthesis ? f.synthesis.implicacoes_fase3_pt : it.implicacoes
  const ver = f ? f.verificadas : it.verified
  blocos.push(blocoTopico(it.titulo, impl, ver))
}}
const mapa = await agent([
  CONTEXTO,
  '',
  'Somente leitura. Voce recebe as implicacoes e as afirmacoes verificadas de ' + blocos.length + ' topicos de uma revisao bibliografica. A Fase 3 JA RODOU (13-15/09/2026): 4 modelos x 3 epocas, biblioteca editada pelo proprio modelo atras de validacao em codigo; o que se decide agora e o modelo final e o estado de biblioteca de producao. Escreva, em portugues do Brasil, um MAPA DE DECISOES para a analise dos resultados: (1) linhas (15-30): achado da literatura -> numero -> fonte (autor-data) -> decisao ou criterio de leitura da Fase 3 que ele fundamenta (ex.: usar acuracia balanceada, ler L1 e nao so L3, tratar autoenvenenamento como veto, esperar ganho atenuado em modelos pequenos como curadores); (2) riscos que a literatura aponta para a decisao (deriva, saturacao, sicofancia a documentacao errada, teste reutilizado, runtime que muda) com mitigacao e fonte; (3) metricas que a literatura sustenta para escolher o modelo (com fonte); (4) capitulos_faceli: que capitulos do livro Faceli et al. (3. ed., 2025) ancoram cada secao do Memorial (6.1 a 6.11); (5) leitura_pt: 300-500 palavras dizendo o que a literatura previa para a Fase 3 e como ler um resultado sem significancia estatistica com n=36. Nao invente fontes; cite so as que aparecem abaixo. Resposta final: apenas o JSON do esquema.',
  '',
  blocos.join('\\n\\n'),
].join('\\n'), {{ label: 'mapa-de-decisoes', phase: 'Mapa', schema: MAPA, agentType: 'Explore', effort: 'high' }})
log('Mapa: ' + (mapa ? mapa.linhas.length + ' linhas' : 'falhou'))

return {{ fechadas, mapa }}
"""
    destino.write_text(script, encoding="utf-8", newline="\n")
    print(f"workflow gravado em {destino} ({len(script)} chars; entrada inlinada {len(dados)} chars)")


def mesclar(entrada: dict, estado_r2: Path, destino: Path) -> None:
    d = json.loads(estado_r2.read_text(encoding="utf-8"))
    res = d.get("result") or {}
    final = {"gerado_em": datetime.now().isoformat(timespec="seconds"), "r1": entrada["r1"], "r2": {}, "mapa": res.get("mapa")}
    por_chave = {f["key"]: f for f in (res.get("fechadas") or []) if f}
    for k, it in entrada["r2"].items():
        f = por_chave.get(k)
        # afirmações além do teto de 20 nunca foram verificadas: entram como rejeitadas com esse motivo
        alem_do_teto = [{"claim": c.get("claim_pt", ""), "fonte": c.get("source_title", ""),
                         "motivo": "além do teto de 20 afirmações por tópico; não verificada"}
                        for c in (it.get("claims") or [])[20:]]
        final["r2"][k] = {
            "titulo": it["titulo"], "prompt": it["prompt"], "por_que_pt": it["por_que_pt"],
            "estado_antes": it["estado"],
            "verified": f["verificadas"] if f else it["verified"],
            "rejeitadas": (it["rejeitadas"] if it["estado"] != "verificacao_pendente" else []) + (f["rejeitadas"] if f else []) + alem_do_teto,
            "synthesis": (f["synthesis"] if f else None) or it["synthesis"],
            "open_questions": (f.get("open_questions") if f else None) or it.get("open_questions_pt") or [],
            "pesquisa_nova": bool(f and f.get("pesquisa")),
        }
    faltam = [k for k, v in final["r2"].items() if not v["synthesis"]]
    destino.write_text(json.dumps(final, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"r2-final gravado em {destino}; sínteses faltando: {faltam or 'nenhuma'}; mapa: {'ok' if final['mapa'] else 'AUSENTE'}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--estado", default=str(ESTADO_PADRAO))
    ap.add_argument("--diario", default=str(DIARIO_PADRAO))
    ap.add_argument("--gerar-workflow", action="store_true")
    ap.add_argument("--mesclar", help="caminho do wf_*.json do Workflow pesquisa-r2")
    ap.add_argument("--r1", choices=("primeira", "segunda", "ultima", "estado"), default="primeira",
                    help="qual execução da rodada 1 usar: primeira (11/09 manhã), segunda (11/09 tarde), ultima (13/09) ou estado (arquivo wf_*.json); --check do render diz qual está no Memorial")
    args = ap.parse_args()
    (SDD / "pesquisa").mkdir(parents=True, exist_ok=True)
    entrada = extrair(Path(args.estado), Path(args.diario), args.r1)
    caminho = SDD / "pesquisa" / "r2-entrada.json"
    caminho.write_text(json.dumps(entrada, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"entrada gravada em {caminho} ({caminho.stat().st_size} bytes)")
    if args.gerar_workflow:
        gerar_workflow(entrada, SDD / "pesquisa-r2.js")
    if args.mesclar:
        mesclar(entrada, Path(args.mesclar), SDD / "pesquisa" / "r2-final.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
