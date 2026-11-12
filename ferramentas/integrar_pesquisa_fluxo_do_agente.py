#!/usr/bin/env python3
# ! Alteração de IA - Revisar: script novo (10/11/2026) que integra ao Memorial a rodada 7 da pesquisa, a das três ideias do Eric para o
# fluxo do agente (ficha 64): o roteiro de raciocínio em passos com lista de conferência, o ciclo de reavaliação e a separação entre o
# módulo de análise e um analista de documentação. Lê, de `5-metodo-e-ferramental/dados/pesquisa-fluxo-do-agente/`, sete leituras em JSON
# (um subagente leitor por tópico), sete segundas leituras em JSON (um subagente verificador por tópico, que abriu de novo cada fonte), as
# sínteses, os vereditos e o mapa escritos pelo Claude (`sinteses.json`) e as medidas do repositório (`medidas_do_repositorio.json`, de
# `medidas_fluxo_do_agente.py`). Grava `levantamento-2026-11-10-fluxo-do-agente.md` (§6.16.1 a §6.16.7, uma subseção por tópico; §6.16.8 o
# que a segunda leitura corrigiu, rejeitou ou não conferiu; §6.16.9 o que o repositório já mediu; §6.16.10 o veredito por ideia; §6.16.11 o
# mapa), o bloco de referências novas em `referencias.md`, as duas linhas do índice do Memorial, a proposta de desenho do analista de
# documentação (gerada do modelo, com os números trocados pelos das medidas) e o resumo que a aba do painel lê; `--check` regera tudo e compara.
# ! Motivo: o Eric disse que as três ideias pedem pesquisa aprofundada antes de qualquer mudança, e a regra do Memorial é que a pesquisa entre
# por script, nunca colada à mão. Três coisas são próprias desta rodada. (1) Ela tem segunda leitura: uma afirmação só entra com o veredito do
# verificador, a parcial entra com o texto corrigido por ele, a referência corrigida substitui a do leitor, e fonte sem afirmação aprovada
# não vai para as referências. (2) Os números do repositório não são digitados: as sínteses e o modelo da proposta trazem marcadores
# `{{m:campo}}`, e o script para se um campo não existe. (3) O bloco de referências entra antes do bloco da Pós-Fase 4, porque o integrador
# dela regrava o bloco dele logo antes do bloco da Pré-Fase 4, e o da Pré-Fase 4 trata o bloco dele como o último do arquivo; a frase do
# total é escrita pelos três scripts com a mesma constante (integrar_pesquisa_pre_fase4.DATAS_DOS_LEVANTAMENTOS).
"""Uso:
    python ferramentas/integrar_pesquisa_fluxo_do_agente.py [--simular]
    python ferramentas/integrar_pesquisa_fluxo_do_agente.py --check
"""
from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import integrar_pesquisa_pos_fase4 as ipp
import integrar_pesquisa_pre_fase4 as ip
import render_levantamento as rl

sys.stdout.reconfigure(encoding="utf-8")

RAIZ = rl.RAIZ
DOC_DIR = RAIZ / "Documentacao" / "memorial"
DADOS = DOC_DIR / "5-metodo-e-ferramental" / "dados" / "pesquisa-fluxo-do-agente"
LEVANTAMENTO = DOC_DIR / "2-pesquisa-e-literatura" / "levantamento-2026-11-10-fluxo-do-agente.md"
PROPOSTA = DOC_DIR / "5-metodo-e-ferramental" / "proposta-analista-de-documentacao.md"
MODELO_DA_PROPOSTA = DADOS / "proposta-analista-de-documentacao.modelo.txt"
SINTESES = DADOS / "sinteses.json"
MEDIDAS = DADOS / "medidas_do_repositorio.json"
RESUMO_DO_PAINEL = DADOS / "resumo_para_o_painel.json"
MEMORIAL = ip.MEMORIAL
DATA = "10/11/2026"
SECAO = "6.16"
ROTULO = f"levantamento de {DATA}"
TITULO_REFS = f"### Levantamento do fluxo do agente ({ROTULO})"
MARCA_DO_INDICE = f"- [Levantamento: fluxo do agente ({DATA})]"
TAG_DO_INDICE = "<!-- ! Alteração de IA - Revisar: linha do índice para o levantamento do fluxo do agente"
MARCA_DA_PROPOSTA = f"- [Proposta de desenho: o analista de documentação ({DATA})]"
TAG_DA_PROPOSTA = "<!-- ! Alteração de IA - Revisar: linha do índice para a proposta de desenho do analista de documentação"
ANCORA_DA_PROPOSTA = "- [Protocolo da linha de base manual"

# Chave, frente (a ideia do Eric a que o tópico serve) e título curto, na ordem fixa das subseções §6.16.1 a §6.16.7.
TOPICOS = [
    ("r7-raciocinio-em-passos-em-modelo-pequeno", "1", "Raciocínio em passos antes da resposta em modelo pequeno: acerto, custo e ordem"),
    ("r7-raciocinio-calibracao-e-primeiro-token", "1", "O raciocínio escrito e a confiança lida no token do rótulo"),
    ("r7-lista-de-conferencia-em-codigo", "1", "A lista de conferência calculada em código e entregue como fato"),
    ("r7-reavaliacao-quando-ajuda", "2", "Reavaliação da própria resposta: quando ajuda e quando troca certo por errado"),
    ("r7-disparo-parada-e-evidencia-nova", "2", "Segundo passe por sinal externo, com regra de parada e evidência nova"),
    ("r7-curador-separado-da-base", "3", "Um papel separado para escrever a base de conhecimento"),
    ("r7-degradacao-e-portoes-da-base", "3", "Degradação da base com o tempo e portões de validação"),
]
FRENTES = {"1": "o roteiro de raciocínio em passos com lista de conferência", "2": "o ciclo de reavaliação pelo próprio agente",
           "3": "os dois momentos do modelo, com um analista de documentação"}
VEREDITOS = ("confirmada", "parcial", "rejeitada", "nao_verificada")
COMO_LI = {"aberta_e_lida": "aberta e lida", "so_resumo": "só o resumo", "so_busca": "só o trecho da busca"}
ABRIU = {"sim": "aberta e lida", "so_resumo": "só o resumo", "nao_abriu": "não abriu"}
_MARCADOR = re.compile(r"\{\{m:([^}|]+?)(?:\|(\d))?\}\}")
_CITACAO = re.compile(r"\[(F\d{2})\]")


def ler_json(caminho: Path) -> dict:
    return json.loads(caminho.read_text(encoding="utf-8"))


# ------------------------------------------------------------------ marcadores das medidas do repositório

def valor(medidas: dict, caminho: str):
    """O valor de um campo das medidas pelo caminho com pontos (`ideia_2.corrida_24.erros`; número indexa lista). Para se o campo não existe."""
    atual = medidas
    for parte in caminho.strip().split("."):
        try:
            atual = atual[int(parte)] if isinstance(atual, list) else atual[parte]
        except (KeyError, IndexError, ValueError, TypeError):
            raise SystemExit(f"marcador de medida sem campo: {caminho} (parou em '{parte}')") from None
    return atual


def formatar(v, casas: int | None = None) -> str:
    """Um valor das medidas como ele entra no texto: inteiro com ponto de milhar, decimal com vírgula e o número de casas pedido, texto como está."""
    if isinstance(v, (bool, list, dict)) or v is None:
        raise SystemExit(f"marcador de medida aponta para um valor que não é número nem texto: {v!r}")
    if isinstance(v, str):
        return v
    if isinstance(v, float) and casas is None:
        if not v.is_integer():
            raise SystemExit(f"marcador de medida com decimal ({v}) sem o número de casas: escreva {{{{m:campo|1}}}}")
        v = int(v)
    if isinstance(v, int) or casas == 0:
        return f"{round(v):,}".replace(",", ".")
    return f"{v:,.{casas}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def preencher(texto: str, medidas: dict) -> str:
    """Troca cada marcador `{{m:campo}}` ou `{{m:campo|casas}}` pelo valor das medidas. Para se sobrar qualquer `{{` no texto."""
    saida = _MARCADOR.sub(lambda m: formatar(valor(medidas, m.group(1)), int(m.group(2)) if m.group(2) else None), texto or "")
    if "{{" in saida:
        raise SystemExit(f"marcador mal escrito no texto: {saida[saida.index('{{'):][:60]}")
    return saida


# ------------------------------------------------------------------ carga: a leitura cruzada com a segunda leitura

def carregar(pasta: Path = DADOS, topicos: list[tuple] | None = None) -> dict:
    """{chave: tópico} na ordem fixa. Cada fonte sai com a referência que vale (a corrigida pela segunda leitura, se houver), o que a segunda
    leitura diz que ela afirma e não afirma, e as afirmações com o veredito e o texto que vale (o corrigido, nas parciais). Para se faltar a
    leitura ou a segunda leitura de um tópico, ou se a segunda leitura não cobrir todas as fontes e afirmações da leitura."""
    dados = {}
    for chave, frente, titulo in topicos or TOPICOS:
        arq_l, arq_v = pasta / f"{chave}.json", pasta / f"{chave}.verificacao.json"
        for arq in (arq_l, arq_v):
            if not arq.exists():
                raise SystemExit(f"arquivo da rodada ausente: {arq}")
        leitura, verificacao = ler_json(arq_l), ler_json(arq_v)
        por_fonte = {f["id"]: f for f in verificacao.get("fontes") or []}
        fontes = []
        for f in leitura.get("fontes") or []:
            v = por_fonte.get(f["id"])
            if v is None:
                raise SystemExit(f"{chave}: a segunda leitura não traz a fonte {f['id']}")
            por_afirmacao = {a["id"]: a for a in v.get("afirmacoes") or []}
            afirmacoes = []
            for a in f.get("afirmacoes") or []:
                x = por_afirmacao.get(a["id"])
                if x is None or x.get("veredito") not in VEREDITOS:
                    raise SystemExit(f"{chave}: a segunda leitura não traz veredito válido para a afirmação {a['id']}")
                afirmacoes.append({"id": a["id"], "veredito": x["veredito"], "texto": (x.get("afirmacao_corrigida_pt") or "").strip() or a["afirmacao_pt"],
                                   "texto_do_leitor": a["afirmacao_pt"], "numero": (x.get("numero_que_a_fonte_sustenta") or "").strip(), "motivo": (x.get("motivo") or "").strip()})
            corrigida = (v.get("referencia_abnt_corrigida") or "").strip()
            fontes.append({"id": f["id"], "referencia": corrigida or f["referencia_abnt"].strip(), "referencia_corrigida": bool(corrigida),
                           "identificador": (v.get("identificador_conferido") or "").strip() or f.get("identificador", ""), "veiculo": (v.get("veiculo_conferido") or "").strip(),
                           "como_li": f.get("como_li", ""), "abriu": v.get("abriu", ""), "afirma": (v.get("o_que_a_fonte_afirma") or "").strip(),
                           "nao_afirma": list(v.get("o_que_a_fonte_nao_afirma") or []), "afirmacoes": afirmacoes,
                           "aprovada": any(a["veredito"] in ("confirmada", "parcial") for a in afirmacoes), "ja_consta": bool(f.get("ja_consta_em_referencias_md"))})
        dados[chave] = {"chave": chave, "frente": frente, "titulo": titulo, "ja_levantado": list(leitura.get("ja_levantado") or []), "fontes": fontes,
                        "nao_achei": list(leitura.get("nao_achei") or [])}
    return dados


def contagem(topico: dict) -> dict:
    """Quantas afirmações do tópico ficaram em cada situação. Aprovada é a confirmada ou a parcial (que entra com o texto corrigido)."""
    v = [a["veredito"] for f in topico["fontes"] for a in f["afirmacoes"]]
    return {"aprovadas": v.count("confirmada") + v.count("parcial"), "parciais": v.count("parcial"), "rejeitadas": v.count("rejeitada"), "nao_verificadas": v.count("nao_verificada")}


def referencias_do_topico(topico: dict) -> list[str]:
    """As referências do tópico que entram no levantamento e em referencias.md: só as de fonte com alguma afirmação aprovada."""
    return [f["referencia"] for f in topico["fontes"] if f["aprovada"]]


def citacoes(sintese: dict) -> list[str]:
    """Os ids de fonte citados entre colchetes no texto, nas implicações e nas lacunas de uma síntese, na ordem em que aparecem."""
    partes = list(sintese.get("texto") or []) + list(sintese.get("implicacoes") or []) + list(sintese.get("lacunas") or [])
    return [m for p in partes for m in _CITACAO.findall(p)]


def citacoes_sem_apoio(dados: dict, sinteses: dict) -> list[tuple[str, str]]:
    """(tópico, id) de cada fonte que uma síntese cita e que não existe no tópico ou não tem afirmação aprovada na segunda leitura."""
    saida = []
    for chave, topico in dados.items():
        aprovadas = {f["id"] for f in topico["fontes"] if f["aprovada"]}
        for fid in dict.fromkeys(citacoes((sinteses.get("topicos") or {}).get(chave) or {})):
            if fid not in aprovadas:
                saida.append((chave, fid))
    return saida


# ------------------------------------------------------------------ render do levantamento

def _plural(n: int, um: str, muitos: str) -> str:
    return f"{n} {um if n == 1 else muitos}"


def _cel(texto: str) -> str:
    return re.sub(r"\s+", " ", str(texto or "")).replace("|", "/").strip()


def _autor_e_ano(referencia: str) -> str:
    """Os sobrenomes dos autores (ou a entidade) e o ano, para a coluna da fonte na tabela da segunda leitura: até três autores por extenso e "et al." a partir de quatro."""
    # o trecho dos autores vai até o primeiro ponto seguido de espaço que não esteja no meio de iniciais ("MOON, S. Y.; XIAO, C.")
    trecho = re.split(r"\. (?![A-Z]\.)", referencia, maxsplit=1)[0].strip()
    sobrenomes = [p.split(",")[0].strip() for p in trecho.split(";") if p.strip()]
    if "et al" in trecho:
        autor = sobrenomes[0].replace(" et al", "") + " et al."
    else:
        autor = "; ".join(sobrenomes) if len(sobrenomes) <= 3 else sobrenomes[0] + " et al."
    ano = re.findall(r"\b(?:19|20)\d{2}\b", referencia.split("Disponível em")[0])
    return f"{autor} ({ano[-1]})" if ano else autor


def _resumo_dos_vereditos(fonte: dict) -> str:
    v = [a["veredito"] for a in fonte["afirmacoes"]]
    partes = [_plural(v.count(k), um, muitos) for k, um, muitos in (("confirmada", "confirmada", "confirmadas"), ("parcial", "parcial", "parciais"), ("rejeitada", "rejeitada", "rejeitadas"),
                                                                    ("nao_verificada", "não verificada", "não verificadas")) if v.count(k)]
    return ", ".join(partes)


def secao(numero: int, chave: str, topico: dict, sintese: dict, medidas: dict) -> str:
    c = contagem(topico)
    # o cabeçalho segue o formato fixo da regra de documentação, com travessão, porque é ele que a aba Pesquisa do painel lê (painel_topicos._TOPICO)
    sufixo = f", {_plural(c['nao_verificadas'], 'não verificada', 'não verificadas')}" if c["nao_verificadas"] else ""
    partes = [f"#### {SECAO}.{numero} {topico['titulo']} (`{chave}` — {_plural(c['aprovadas'], 'aprovada', 'aprovadas')}, {_plural(c['rejeitadas'], 'rejeitada', 'rejeitadas')}{sufixo})", "",
              f"*Título da síntese:* {preencher(sintese.get('titulo', ''), medidas)}", "",
              (f"*Leitura e segunda leitura:* um subagente leitor e um subagente verificador, em {DATA}; arquivos `{chave}.json` e `{chave}.verificacao.json` em "
               f"`5-metodo-e-ferramental/dados/pesquisa-fluxo-do-agente/`. Frente: {FRENTES[topico['frente']]}."), ""]
    if topico["ja_levantado"]:
        partes += ["##### O que as rodadas anteriores já diziam", ""] + [f"* {j['secao']}: {_cel(j['o_que_ja_dizia'])}" for j in topico["ja_levantado"]] + [""]
    partes += ["##### Texto", ""]
    for paragrafo in sintese.get("texto") or []:
        partes += [preencher(paragrafo, medidas), ""]
    partes += ["##### Implicações para o agente", ""] + [f"* {preencher(x, medidas)}" for x in sintese.get("implicacoes") or []] + [""]
    partes += ["##### Lacunas", ""] + [f"* {preencher(x, medidas)}" for x in sintese.get("lacunas") or []] + [""]
    partes += ["##### Segunda leitura das fontes", "",
               ("Cada linha é uma fonte do tópico, como a segunda leitura a conferiu: o identificador, onde o evento ou o periódico foi visto (ou que não foi confirmado), "
                "como cada leitor a leu, o que ela afirma, o que ela não afirma e o veredito das afirmações que o primeiro leitor tirou dela."), "",
               "| Fonte | Identificador e veículo | Como foi lida | O que afirma | O que não afirma | Afirmações |", "|---|---|---|---|---|---|"]
    for f in topico["fontes"]:
        lida = f"1ª: {COMO_LI.get(f['como_li'], f['como_li'])}; 2ª: {ABRIU.get(f['abriu'], f['abriu'])}"
        ident = _cel(f["identificador"]) + (f"; {_cel(f['veiculo'])}" if f["veiculo"] else "")
        partes.append(f"| {f['id']} {_cel(_autor_e_ano(f['referencia']))} | {ident} | {lida} | {_cel(f['afirma'])} | {_cel('; '.join(f['nao_afirma']))} | {_resumo_dos_vereditos(f)} |")
    partes += ["", "##### Referências ABNT do tópico", ""] + [f"- {r}" for r in referencias_do_topico(topico)] + [""]
    return "\n".join(partes)


def bloco_rejeitadas(numero: int, dados: dict) -> str:
    partes = [f"#### {SECAO}.{numero} Afirmações rejeitadas, não verificadas ou de suporte parcial (com o motivo)", "",
              ("Cada linha é uma afirmação do primeiro leitor que a segunda leitura não confirmou como estava. As de suporte parcial entraram nas sínteses com o texto corrigido pelo "
               "verificador, que é o que aparece aqui, com o motivo da correção. As rejeitadas e as não verificadas não entraram. As referências corrigidas (autores, evento, versão) "
               "já saem na forma corrigida na lista de cada tópico."), ""]
    for chave, topico in dados.items():
        c = contagem(topico)
        corrigidas = [f["id"] for f in topico["fontes"] if f["referencia_corrigida"]]
        partes.append(f"*`{chave}`*: {_plural(c['rejeitadas'], 'rejeitada', 'rejeitadas')}, {_plural(c['parciais'], 'parcial', 'parciais')}, "
                      f"{_plural(c['nao_verificadas'], 'não verificada', 'não verificadas')}; {_plural(len(corrigidas), 'referência corrigida', 'referências corrigidas')}"
                      + (f" ({', '.join(corrigidas)})" if corrigidas else ""))
        for rotulo, veredito in (("Rejeitada", "rejeitada"), ("Não verificada", "nao_verificada"), ("Parcial", "parcial")):
            for f in topico["fontes"]:
                for a in f["afirmacoes"]:
                    if a["veredito"] == veredito:
                        texto = a["texto"] if veredito == "parcial" else a["texto_do_leitor"]
                        partes.append(f"- {rotulo} [{a['id']}]: {_cel(texto)} *Motivo:* {_cel(a['motivo']) or 'sem motivo declarado'}")
        partes.append("")
    return "\n".join(partes)


def _tabela(cab: list[str], linhas: list[list]) -> dict:
    """Um quadro: o cabeçalho e as linhas, com as células já como texto de uma linha só."""
    return {"cabecalho": list(cab), "linhas": [[_cel(c) for c in l] for l in linhas]}


def _em_markdown(quadro: dict) -> str:
    cab = quadro["cabecalho"]
    return "\n".join(["| " + " | ".join(cab) + " |", "|" + "---|" * len(cab)] + ["| " + " | ".join(l) + " |" for l in quadro["linhas"]])


def tabelas_das_medidas(medidas: dict) -> dict[str, str]:
    """As tabelas geradas das medidas do repositório, por nome, em Markdown: entram no §6.16.9 do levantamento e nos blocos `<!-- medidas:nome -->` da proposta."""
    return {nome: _em_markdown(quadro) for nome, quadro in quadros_das_medidas(medidas).items()}


def quadros_das_medidas(medidas: dict) -> dict[str, dict]:
    """Os mesmos quadros, como cabeçalho e linhas, para a aba do painel montar as tabelas sem repetir as contas."""
    f = formatar
    m, i1, i2, i3 = medidas["maquina"], medidas["ideia_1"], medidas["ideia_2"], medidas["ideia_3"]
    custo, cen = i3["custo_da_proposta"], i3["cenarios_do_analista"]
    maquina = _tabela(["O que", "Valor", "De onde vem"], [
        ["Leitura do prompt (prefill)", f"{f(m['prefill_tokens_por_s'], 1)} tokens por segundo", "mediana dos registros das corridas 18d, 21d e 24"],
        ["Escrita da resposta (geração)", f"{f(m['geracao_tokens_por_s'], 2)} tokens por segundo", "idem"],
        ["Cada 100 tokens escritos", f"{f(m['segundos_por_100_tokens_gerados'], 1)} s", "100 dividido pela taxa de escrita"],
        ["Prompt do diagnóstico", f"{f(m['tokens_do_prompt_mediana'])} tokens", "mediana"],
        ["Resposta do diagnóstico", f"{f(m['tokens_gerados_mediana'])} tokens", "mediana"],
        ["Um diagnóstico", f"{f(i2['corrida_24']['segundos_mediana'], 1)} s", "mediana da corrida 24"],
        ["Um raciocínio em passos, se fosse pedido", f"cerca de {f(m['tokens_de_um_raciocinio_em_passos_na_literatura'])} tokens, {f(m['segundos_de_um_raciocinio_em_passos'], 0)} s a mais",
         "o tamanho é da literatura (§6.16.1); o tempo é a conta com a taxa de escrita"],
        ["Uma proposta de edição, hoje", f"{f(custo['proposta']['tokens_entrada'])} tokens lidos, {f(custo['proposta']['tokens_saida'])} escritos, {f(custo['proposta']['segundos'], 1)} s", "mediana das propostas da corrida 20"],
    ])
    fa, c23 = i1["fase_2a"], i1["corrida_23"]
    cal = i1["calibracao"]
    nome_da_condicao = {"exemplar": "um exemplar resolvido no prompt", "rotulos_por_extenso": "os rótulos escritos em palavras"}
    ideia_1 = _tabela(["Medida", "Resultado", "De onde vem"], [
        ["Prompt direto contra prompt em etapas, `qwen2.5:7b`, 90 casos", f"{fa['linear']} no direto; {fa['estagios_compilador']} e {fa['estagios_dominio']} nos dois em etapas ({fa['linear_x_compilador']}; {fa['linear_x_dominio']})", "Fase 2-A, relatório, seção 3"],
        *[[f"Prompt com {nome_da_condicao.get(c['condicao'], c['condicao'])}, {f(c23['casos'])} casos", f"{f(c['b'])} casos ganhos e {f(c['c'])} perdidos (p = {f(c['p_mcnemar'], 2)}); {f(c['trocas_de_rotulo'])} rótulos trocados", "corrida 23"] for c in c23["condicoes"]],
        ["Probabilidade do primeiro token do rótulo como sinal de erro", f"AUROC de {f(cal['auroc_da_probabilidade'], 2)} (intervalo de 95% de {f(cal['auroc_ic95'][0], 2)} a {f(cal['auroc_ic95'][1], 2)}) em {f(cal['casos'])} casos, {f(cal['erros'])} erros", "corrida 16"],
        *[[f"Selo {s['selo'].replace('medio', 'médio')}", f"{f(s['casos'])} casos, {f(s['errados'])} errados ({f(s['erro_pct'], 1)}%)", "corrida 16"] for s in cal["por_selo"]],
        ["Regras que conferem a resposta em código, depois que ela sai", f"{f(i1['conferencias_em_codigo']['quantas'])}: " + ", ".join(f"`{r}`" for r in i1["conferencias_em_codigo"]["regras"]), "`diagnostico_ao_vivo.py`"],
    ])
    c22, c24, os72 = i2["corrida_22"], i2["corrida_24"], i2["os_72_casos"]

    def sinal(nome: str, s: dict) -> list:
        return [nome, f"pega {f(s['vp'])} dos {f(s['vp'] + s['fn'])} erros e acende em {f(s['fp'])} dos {f(s['fp'] + s['vn'])} acertos; produto {f(s['produto'], 3)} (acaso {f(s['acaso'], 2)})", "corrida 22"]

    k = {x["k"]: x for x in i2["corrida_16_numero_de_verbetes"]["por_k"]}
    par = i2["corrida_16_numero_de_verbetes"]["par"]
    sonda = c22["sonda"]
    ideia_2 = _tabela(["Medida", "Resultado", "De onde vem"], [
        sinal("A divergência que o agente sinaliza, com as intervenções em todos os casos", c22["divergencia"]),
        sinal("A mesma divergência, contada só onde um gatilho acenderia", c22["divergencia_por_gatilho"]),
        sinal("Só o selo baixo", c22["selo_baixo"]),
        ["Repetir a mesma inferência", f"mesmo rótulo em {f(c22['repeticao']['manteve'])} de {f(c22['repeticao']['n'])} casos", "corrida 22"],
        ["Trecho plantado num verbete que o modelo não citava", f"citado em {f(sonda['cita_plantado'])} de {f(sonda['casos'])} casos ({f(sonda['controle_cita'])} na corrida sem o trecho)", "corrida 22"],
        ["Proposta refeita depois de o verbete ser corrigido", f"{f(i2['corrida_20_sonda']['mudaram_a_proposta'])} de {f(i2['corrida_20_sonda']['com_proposta_anterior'])} mudaram; {f(i2['corrida_20_sonda']['mencionam_a_correcao'])} mencionam a correção", "corrida 20"],
        ["Entregar 5 verbetes no lugar de 3", f"{f(k[5]['acertos'])} acertos contra {f(k[3]['acertos'])} em {f(k[3]['n'])} casos ({f(par['b'])} ganhos, {f(par['c'])} perdidos, p = {f(par['p_mcnemar'], 2)}); o prompt vai de {f(k[3]['tokens_entrada_mediana'], 0)} a {f(k[5]['tokens_entrada_mediana'], 0)} tokens na mediana", "corrida 16"],
        ["Erros sem o verbete da causa certa entre os três entregues", f"{f(c24['erros_sem_o_verbete_certo'])} de {f(c24['erros'])} nos inéditos; {f(c22['cruzamento']['erros_sem_o_verbete_certo'])} de {f(c22['cruzamento']['erros'])} nos oficiais", "corridas 24 e 22"],
    ])
    linhas_gatilho = []
    for nome, c in (("corrida 24, 36 inéditos", c24), ("corrida 22, 36 oficiais", c22["cruzamento"])):
        for g in c["gatilhos"]:
            linhas_gatilho.append([nome, g["gatilho"], f(g["disparos"]), f"{f(g['erros_pegos'])} de {f(c['erros'])}", f"{f(g['acertos_incomodados'])} de {f(c['acertos'])}"])
    gatilhos = _tabela(["Onde", "Gatilho", "Casos em que acende", "Erros que pega", "Acertos que incomoda"], linhas_gatilho)
    posicao = _tabela(["Posição do verbete da causa certa na busca", "Casos, corrida 24", "Erros, corrida 24", "Casos, corrida 22", "Erros, corrida 22"],
                      [[p24["faixa"] + (" (os três entregues)" if p24["faixa"] == "1 a 3" else ""), f(p24["casos"]), f(p24["erros"]), f(p22["casos"]), f(p22["erros"])]
                       for p24, p22 in zip(c24["posicao_do_verbete_certo"], c22["cruzamento"]["posicao_do_verbete_certo"])])
    teto = _tabela(["Segundo passe por gatilho, nos 72 casos", "Valor"], [
        ["Casos em que um dos dois gatilhos acende", f"{f(os72['disparos'])} de {f(os72['casos'])} ({f(os72['casos_com_disparo_pct'], 0)}%)"],
        ["Erros que os gatilhos pegam", f"{f(os72['erros_pegos'])} de {f(os72['erros'])}"],
        ["Acertos em que os gatilhos acendem", f(os72["acertos_incomodados"])],
        *[[f"Erros com o verbete certo ao alcance de um segundo passe com {f(t['verbetes'])} verbetes", f"{f(t['erros_ao_alcance'])} de {f(os72['erros'])}"] for t in os72["teto_de_um_segundo_passe"]],
        ["Tempo de máquina das chamadas a mais", f"{f(os72['minutos_a_mais_dos_disparos'], 0)} minutos"],
        *[[f"Melhor cenário com {f(p['verbetes'])} verbetes: {f(p['ganhos'])} erros consertados e nenhum acerto perdido", f"p = {f(p['p'], 2)} no teste pareado exato (o corte do projeto é 0,05)"]
          for p in os72["p_do_melhor_cenario"]],
    ])
    c20, rev, forma, portao, prom, notas = i3["corrida_20"], i3["revisao_do_lote"], i3["forma_de_instrucao"], i3["portao_da_busca_no_lote"], i3["promocao"], i3["notas_do_modelo"]
    ideia_3 = _tabela(["Medida", "Resultado", "De onde vem"], [
        ["Propostas de edição", f"{f(c20['propostas'])} em {f(c20['casos'])} casos; {f(c20['abstencoes'])} casos sem proposta", "corrida 20"],
        ["O que os filtros em código fizeram", f"{f(c20['aceitas'])} aceitas, {f(c20['para_revisao'])} segurada para revisão, {f(c20['recusadas_fase3'])} recusadas pelo validador da Fase 3 e {f(c20['recusadas_p5'])} pelos filtros da Fase 4", "corrida 20"],
        ["Revisão humana das que passaram", f"{f(rev['por_veredito']['Correta'])} corretas, {f(rev['por_veredito']['Parcial'])} parciais e {f(rev['por_veredito']['Errada'])} erradas em {f(rev['edicoes_revisadas'])}", "planilha de revisão do lote"],
        *[[f"Revisão por tipo: {o['operacao'].replace('retificacao', 'retificação').replace('novo_verbete', 'verbete novo')}",
           f"{_plural(o['Correta'], 'correta', 'corretas')}, {_plural(o['Parcial'], 'parcial', 'parciais')}, {_plural(o['Errada'], 'errada', 'erradas')}", "planilha de revisão do lote"] for o in rev["por_operacao"]],
        ["Propostas que começam por verbo de instrução", f"{f(forma['em_forma_de_instrucao'])} de {f(forma['propostas'])}; entre as que passaram nos filtros, {f(forma['passaram_em_forma_de_instrucao'])} de {f(forma['passaram_nos_filtros'])}", "propostas da corrida 20"],
        ["Regra do lote (R5) nos inéditos", f"{f(c20['reavaliacao']['b'])} casos ganhos e {f(c20['reavaliacao']['c'])} perdidos em {f(c20['reavaliacao']['n'])}; lote {c20['reavaliacao']['veredito']}", "corrida 20"],
        ["O que entrou na biblioteca de produção", f"{f(prom['mantidas'])} edições mantidas e {f(prom['removidas'])} removidas na promoção; {f(prom['aprendidos_em_espera'])} verbetes aprendidos em espera", "`biblioteca_producao/fechamento.json`"],
        ["Notas do modelo na biblioteca que ele lê", f"{f(notas['notas_retiradas'])} notas em {f(notas['verbetes_com_notas'])} dos {f(notas['verbetes_producao'])} verbetes; {f(notas['notas_em_forma_de_instrucao'])} em forma de instrução", "prévia da corrida 25"],
        ["Portão da busca, edição por edição, sem modelo", f"em {f(portao['casos_com_gabarito'])} casos, {f(portao['edicoes_que_mudam_a_busca'])} das {f(portao['edicoes'])} edições mudam os três verbetes de algum caso; o verbete certo sai {f(portao['verbete_certo_sai_no_total'])} vezes e entra {f(portao['verbete_certo_entra_no_total'])}; {f(portao['edicoes_que_nenhum_caso_leria'])} edições nenhum caso leria", "medida desta rodada"],
        # ! Alteração de IA - Revisar: (10/11/2026, depois da revisão da entrega) duas linhas novas: os verbetes novos do lote que nenhum caso leria, e os diagnósticos certos
        # que o analista de QA recusou cruzados com a FONTE divergente.
        # ! Motivo: o mapa dizia que nenhum caso leria os verbetes novos (um deles teria um leitor) e a proposta dizia de que tipo eram os diagnósticos certos recusados sem
        # número medido; as duas contas passaram a existir no arquivo de medidas e aparecem aqui para o leitor conferir.
        ["Verbetes novos do lote: quantos algum caso com gabarito leria", (f"dos {f(portao['verbetes_novos']['edicoes'])}, {f(portao['verbetes_novos']['que_nenhum_caso_leria'])} nenhum caso leria e "
         f"{f(portao['verbetes_novos']['com_algum_caso'])} seria lido ({_plural(portao['verbetes_novos']['casos_que_os_leriam_no_total'], 'caso', 'casos')} no total)"), "medida desta rodada"],
        ["Revisão humana dos relatórios (a decisão que serviria de rótulo)", f"decisão apropriada em {f(i3['revisao_humana_v3']['adesao_apropriada'])} de {f(i3['revisao_humana_v3']['relatorios'])}; erro localizado em {f(i3['revisao_humana_v3']['erros_localizados'])} de {f(i3['revisao_humana_v3']['erros_na_corrida'])}", "sessão de revisão da corrida 24"],
        ["Diagnósticos certos que o analista de QA recusou", (f"{f(i3['revisao_humana_v3']['certos_recusados'])}, dos quais {f(i3['revisao_humana_v3']['certos_recusados_com_a_fonte_divergente'])} com a FONTE divergente acesa; "
         f"dos {f(i3['revisao_humana_v3']['acertos_com_a_fonte_divergente'])} acertos com ela acesa, recusou {f(i3['revisao_humana_v3']['acertos_com_a_fonte_divergente_recusados'])}"),
         "sessão de revisão da corrida 24, cruzada com a trilha"],
    ])
    por_edicao = _tabela(["Caso de origem", "Verbete", "Operação", "Casos em que os três verbetes mudam", "Verbete certo entra", "Verbete certo sai", "Casos que leriam a edição"],
                         [[e["caso"], f"`{e['verbete']}`", e["operacao"].replace("retificacao", "retificação").replace("novo_verbete", "verbete novo"), f(e["casos_em_que_os_tres_verbetes_mudam"]),
                           f(e["verbete_certo_entra"]), f(e["verbete_certo_sai"]), f(e["casos_que_leriam_a_edicao"])] for e in portao["por_edicao"]])
    hoje = cen["medido_hoje"]
    cenarios = _tabela(["O que o analista de documentação leria", "Tokens lidos", "Tokens escritos", "Tempo por chamada"], [
        [f"Como a proposta de hoje (continua o prompt do diagnóstico, até {f(i3['filtros_em_codigo']['propostas_por_caso'])} propostas)", f(hoje["tokens_lidos"]), f(hoje["tokens_escritos"]),
         f"{f(hoje['segundos'], 0)} s ({f(hoje['minutos'], 1)} min), medido"],
        *[[c["cenario"].capitalize() + ", um verbete e as instruções, uma proposta", f(c["tokens_lidos"]), f(c["tokens_escritos"]), f"{f(c['segundos'], 0)} s ({f(c['minutos'], 1)} min), estimado"] for c in cen["cenarios"]],
    ])
    portoes = i3["custo_dos_portoes"]
    custo_dos_portoes = _tabela(["Portão", "Custo nesta máquina"], [
        ["Filtros em código e portão da busca", "segundos, sem modelo"],
        ["Portão do diagnóstico em todos os casos que leriam cada edição (lote da corrida 20)", f"{f(portoes['diagnosticos_do_portao_por_edicao'])} diagnósticos, {f(portoes['horas_do_portao_por_edicao'], 1)} horas"],
        ["Reavaliação do lote nos 36 inéditos, como a regra R5 fez", f"{f(custo['reavaliacao_do_lote']['inferencias'])} diagnósticos, {f(custo['reavaliacao_do_lote']['minutos_no_total'], 0)} minutos"],
        [f"Os {f(os72['casos'])} casos (os oficiais de avaliação e os inéditos), como a corrida 25", f"{f(os72['casos'])} diagnósticos, {f(portoes['minutos_dos_72_casos'])} minutos"],
    ])
    conf = i1["conferencia_depois_da_resposta"]
    conferencia = _tabela(["Onde", "Erros", "Erros que responderam um rótulo com conferência", "Erros com o rótulo contradito", "Acertos com o rótulo contradito"],
                          [[c["corrida"], f(c["erros"]), f(c["erros_com_rotulo_conferivel"]), f"{f(c['erros_contraditos'])} de {f(c['erros'])}", f(c["acertos_contraditos"])] for c in conf["por_corrida"]])
    return {"maquina": maquina, "ideia_1": ideia_1, "conferencia": conferencia, "ideia_2": ideia_2, "gatilhos": gatilhos, "posicao": posicao, "teto": teto,
            "ideia_3": ideia_3, "portao_por_edicao": por_edicao, "cenarios": cenarios, "custo_dos_portoes": custo_dos_portoes}


# ! Alteração de IA - Revisar: (10/11/2026, depois da revisão da entrega) frase nova: pela falha gravada na trilha, de que tipo foram os casos em que a FONTE divergente acendeu.
# ! Motivo: o gatilho da FONTE junta duas conferências do agente, e o levantamento, a proposta de desenho e a ficha 66 descreviam os casos só pela segunda ("nenhum verbete
# entregue trata da causa respondida") sem número medido. A frase lê `ideia_2.os_72_casos.fonte_divergente_por_falha` e lista o que estiver lá, com o nome de cada falha.
NOME_DA_FALHA_DA_FONTE = {"causa_sem_verbete_que_a_trate": "nenhum verbete entregue trata da causa respondida",
                          "citacao_fora_do_contexto": "a FONTE cita um verbete fora dos três entregues"}


def frase_da_fonte_divergente(os72: dict) -> str:
    partes = [f"{formatar(x['casos'])} com a falha `{x['falha']}` ({NOME_DA_FALHA_DA_FONTE.get(x['falha'], x['falha'])}; {_plural(x['acertos'], 'acerto', 'acertos')} e "
              f"{_plural(x['erros'], 'erro', 'erros')})" for x in os72["fonte_divergente_por_falha"]]
    return ("A FONTE divergente junta duas conferências do agente: a linha FONTE cita um verbete fora dos três entregues, ou nenhum dos três trata da causa respondida. "
            f"Pela falha gravada na trilha, os {formatar(os72['disparos_da_fonte_divergente'])} casos em que ela acendeu nas duas corridas são: " + "; ".join(partes) + ".")


def corpo_das_medidas(medidas: dict) -> str:
    """O texto e as tabelas do que o repositório já mediu, sem o título da subseção (que o render escreve)."""
    t = tabelas_das_medidas(medidas)
    conf = medidas["ideia_1"]["conferencia_depois_da_resposta"]
    corrida_25 = medidas["ideia_3"]["corrida_25"]
    estado_25 = ("A corrida 25 já rodou; o resultado dela está em `resultados_alvo/fase4/sem_notas.json` e é registrado no roadmap pela sessão principal." if corrida_25.get("rodou")
                 else "A corrida 25, que mede quanto pesam as notas que o modelo escreveu, ainda não rodou quando este levantamento foi gerado.")
    partes = ["",
              ("As tabelas abaixo são geradas de `5-metodo-e-ferramental/dados/pesquisa-fluxo-do-agente/medidas_do_repositorio.json`, que `ferramentas/medidas_fluxo_do_agente.py` monta "
               "copiando os números dos JSON das corridas, sem rodar o modelo. Três contas são novas e também não gastam modelo: a posição do verbete da causa certa na busca refeita "
               "de cada caso (a busca refeita devolve os três verbetes gravados em todos os casos das duas corridas), o cruzamento dessa posição com o selo e com os dois gatilhos, "
               "e o efeito de cada edição do lote da corrida 20 sobre a busca. " + estado_25), "",
              "**A máquina.**", "", t["maquina"], "",
              "**Ideia 1: raciocínio em passos e lista de conferência.**", "", t["ideia_1"], "",
              (f"A lista de conferência depois da resposta, numa prévia sem modelo: {ip._POR_EXTENSO.get(len(conf['conferencias']), str(len(conf['conferencias']))).lower()} conferências de exemplo "
               "(" + ", ".join(f"`{r}`" for r in conf["conferencias"]) + ") dizem quando o rótulo respondido é contradito por um fato que o código mede no próprio caso: o corpo é um JSON "
               "inteiro, veio na forma que a rota devolve, e todos os campos têm o tipo do contrato. Como ler: quanto mais erros com o rótulo contradito, melhor; acerto contradito é alarme "
               f"falso, e nos {formatar(conf['casos_cujo_gabarito_tem_conferencia'])} casos cujo gabarito é um desses rótulos nenhuma conferência o contradiz "
               f"({formatar(conf['desses_contraditos'])}). As conferências foram escritas olhando os erros das corridas 22 e 24; os casos de aprendizado da corrida 16 não foram olhados."), "",
              t["conferencia"], "",
              "**Ideia 2: ciclo de reavaliação.**", "", t["ideia_2"], "",
              ("O que os dois gatilhos que o agente já calcula pegariam, se disparassem um segundo passe. Como ler: um gatilho bom acende em muitos erros e em poucos acertos; "
               "cada caso em que ele acende é uma chamada a mais ao modelo. " + frase_da_fonte_divergente(medidas["ideia_2"]["os_72_casos"])), "", t["gatilhos"], "",
              ("Onde o verbete da causa certa fica na lista da busca. Como ler: só os três primeiros chegam ao modelo; um segundo passe com mais verbetes só alcança o erro cujo "
               "verbete está logo abaixo."), "", t["posicao"], "", t["teto"], "",
              "**Ideia 3: o analista de documentação.**", "", t["ideia_3"], "",
              ("O portão da busca aplicado a cada edição do lote da corrida 20, uma a uma, sobre a biblioteca de antes do lote. Como ler: uma edição boa não tira o verbete certo "
               "de nenhum caso; a última coluna diz quantos casos teriam o verbete editado entre os três entregues, que é quantos diagnósticos um portão do diagnóstico teria de refazer."), "",
              t["portao_por_edicao"], "",
              "Quanto custa uma chamada do analista de documentação conforme o que ele lê, e quanto custam os portões.", "", t["cenarios"], "", t["custo_dos_portoes"], ""]
    return "\n".join(partes)


CAMPOS_DO_VEREDITO = (("veredito", "Veredito"), ("literatura", "O que a literatura sustenta"), ("repositorio", "O que o repositório já mediu"), ("forma_que_escapa", "A forma que escapa do que já foi medido"),
                      ("como_medir", "Como seria medida"), ("custo", "Quanto custa nesta máquina"), ("recomendacao", "Recomendação"))


def bloco_vereditos(numero: int, sinteses: dict, medidas: dict) -> str:
    partes = [f"#### {SECAO}.{numero} Veredito por ideia", "",
              ("Um veredito por ideia do Eric, escrito pelo Claude a partir das subseções acima e das medidas do repositório. Nenhum deles muda o agente: o que cada um recomenda está nas "
               "fichas 65 a 67 das pendências, uma por ideia, e a decisão é do Eric."), ""]
    for v in sinteses.get("vereditos") or []:
        partes += [f"##### Ideia {v['ideia']}: {v['nome']}", ""] + [f"* **{rotulo}:** {preencher(v.get(campo, ''), medidas)}" for campo, rotulo in CAMPOS_DO_VEREDITO] + [""]
    return "\n".join(partes)


def bloco_mapa(numero: int, sinteses: dict, medidas: dict) -> str:
    partes = [f"#### {SECAO}.{numero} Mapa adotado, adiado, descartado", "",
              ("Uma linha por opção, escrita pelo Claude. *Adotado* = já é assim no agente e a pesquisa confirma; *adiado* = só com decisão do Eric e medida própria, sem mudar o agente "
               "antes da Fase 5 (as linhas do analista de documentação estão na proposta de desenho); *descartado* = não serve, com o motivo."), "",
              "| Tema | Opção | Veredito | Motivo | Fonte |", "|---|---|---|---|---|"]
    partes += [f"| {_cel(l['tema'])} | {_cel(l['opcao'])} | **{l['veredito']}** | {_cel(preencher(l['motivo'], medidas))} | {_cel(l['fonte'])} |" for l in sinteses.get("mapa") or []]
    return "\n".join(partes) + "\n"


def cabecalho(dados: dict, topicos: list[tuple]) -> str:
    n = len(topicos)
    cont = {k: contagem(dados[k]) for k, *_ in topicos}
    tot = {c: sum(x[c] for x in cont.values()) for c in ("aprovadas", "parciais", "rejeitadas", "nao_verificadas")}
    n_fontes = sum(len(dados[k]["fontes"]) for k, *_ in topicos)
    n_afirmacoes = sum(len(f["afirmacoes"]) for k, *_ in topicos for f in dados[k]["fontes"])
    corrigidas = sum(1 for k, *_ in topicos for f in dados[k]["fontes"] if f["referencia_corrigida"])
    so_resumo = sum(1 for k, *_ in topicos for f in dados[k]["fontes"] if f["abriu"] != "sim")
    linhas = [
        ("<!-- ! Alteração de IA - Revisar: arquivo gerado por ferramentas/integrar_pesquisa_fluxo_do_agente.py a partir das leituras, das segundas leituras, das sínteses e das medidas "
         "guardadas em 5-metodo-e-ferramental/dados/pesquisa-fluxo-do-agente/ (rodada 7 da pesquisa, 10/11/2026). NÃO editar as subseções à mão (o --check compara com o regerado)."),
        (f"     ! Motivo: o Eric trouxe em 10/11/2026 três ideias para o fluxo do agente e disse que elas pedem pesquisa aprofundada antes de qualquer mudança (ficha 64); a pesquisa entra por "
         f"script, com cada afirmação conferida por uma segunda leitura, os números do repositório copiados dos JSON das corridas e o que não serve registrado com o motivo "
         f"(§{SECAO}.{n + 1} e §{SECAO}.{n + 4}). -->"),
        "", f"# Levantamento bibliográfico: três ideias para o fluxo do agente ({DATA})", "",
        ("Parte do [Memorial de Desenvolvimento](../../Memorial%20de%20Desenvolvimento.md). Continua o [levantamento da Pós-Fase 4](levantamento-2026-11-07-pos-fase-4.md) (§6.15). "
         "O que motivou: lendo o [parecer do analista](../3-resultados-e-analises/parecer-do-analista-2026-11-10.md), o Eric propôs olhar três mudanças no fluxo do agente: (1) um roteiro "
         "de raciocínio em passos para o diagnóstico, com uma lista de conferência; (2) um ciclo de reavaliação, em que o agente revê a própria resposta; (3) dois momentos do modelo, em "
         "que o módulo de análise diagnostica e não mexe na biblioteca, e um analista de documentação recebe o relatório pronto e só então propõe criar, corrigir ou limpar verbetes "
         "(ficha 64 das [pendências](../pendencias.md), fechada pela decisão 118: pesquisar agora, sem mudar o agente antes da Fase 5; [roadmap](../roadmap.md), §4.8). "
         "A proposta de desenho da terceira ideia está em "
         "[proposta-analista-de-documentacao.md](../5-metodo-e-ferramental/proposta-analista-de-documentacao.md). Referências completas em [referencias.md](referencias.md)."),
        "", f"### {SECAO} Levantamento do fluxo do agente", "",
        (f"{n} tópicos em três frentes, uma por ideia, em {DATA}. Cada tópico teve um subagente leitor, que abriu as fontes e gravou, fonte a fonte, o que leu e as afirmações com o "
         f"número e a condição; e um subagente verificador, que abriu de novo cada fonte, conferiu o identificador, os autores e o evento, escreveu o que a fonte afirma e o que não "
         f"afirma e deu o veredito de cada afirmação. As sínteses, os vereditos por ideia e o mapa são do Claude e só usam o que a segunda leitura aprovou. "
         f"Totais: {n_fontes} fontes e {n_afirmacoes} afirmações; **{_plural(tot['aprovadas'], 'aprovada', 'aprovadas')}** ({tot['aprovadas'] - tot['parciais']} confirmadas e "
         f"{_plural(tot['parciais'], 'parcial', 'parciais')}, que entram com o texto corrigido), **{_plural(tot['rejeitadas'], 'rejeitada', 'rejeitadas')}** e "
         f"**{_plural(tot['nao_verificadas'], 'não verificada', 'não verificadas')}**; {_plural(corrigidas, 'referência corrigida', 'referências corrigidas')} pela segunda leitura."),
        "", "| Subseção | Frente | Tópico | Fontes | Aprovadas | Parciais | Rejeitadas | Não verificadas |", "|---|---|---|---|---|---|---|---|",
    ]
    for i, (chave, frente, _) in enumerate(topicos, 1):
        c = cont[chave]
        linhas.append(f"| §{SECAO}.{i} | {frente} | `{chave}` | {len(dados[chave]['fontes'])} | {c['aprovadas']} | {c['parciais']} | {c['rejeitadas']} | {c['nao_verificadas']} |")
    avisos = [
        ("**Segunda leitura, não Workflow.** As rodadas 1 a 5 passaram por um Workflow com pesquisador, verificadores e síntese; a rodada 6 não teve verificação. Esta teve um leitor e "
         "um verificador por tópico, lançados como subagentes em duas ondas, e a síntese do Claude. "
         + ("Nenhuma afirmação foi rejeitada" if not tot["rejeitadas"] else f"{_plural(tot['rejeitadas'], 'afirmação foi rejeitada', 'afirmações foram rejeitadas')} (§{SECAO}.{n + 1})")
         + "; as parciais são as em que o verificador achou outro número, outra condição ou alcance menor. O Claude abriu por amostragem a página de quatro das fontes que mais pesam nos "
         "vereditos e confirmou o título, os autores e a afirmação central."),
        (f"**O que a segunda leitura não cobre.** {_plural(so_resumo, 'fonte ficou', 'fontes ficaram')} só no resumo ou sem abrir na segunda leitura (a coluna \"Como foi lida\" diz quais), e "
         "nas páginas longas os dois leitores leram os primeiros 100 mil caracteres, sem os apêndices. Vários preprints não têm evento confirmado; a coluna do identificador diz onde o "
         "evento foi visto. Várias fontes são de 2026 e ainda não têm revisão por pares."),
        ("**Os números do repositório.** Nenhum foi digitado: as sínteses trazem marcadores que o script troca pelo valor de `medidas_do_repositorio.json`, e esse arquivo é copiado dos "
         f"JSON das corridas por `medidas_fluxo_do_agente.py`, com `--check`. As tabelas estão no §{SECAO}.{n + 2}."),
        ("**Nada muda no agente.** Esta rodada é só pesquisa, como o Eric decidiu ao fechar a ficha 64 (decisão 118): não rodou o modelo, não tocou no prompt, na busca nem na biblioteca, "
         "e não regravou nada das corridas. O que cada veredito recomenda é decisão do Eric (fichas 65 a 67)."),
        ("**Grafia.** O texto não usa travessão nem seta, como manda a regra de documentação; o cabeçalho de cada subseção de tópico mantém o formato fixo da regra, que a aba Pesquisa "
         "do painel lê, e os títulos das fontes ficam como na fonte."),
    ]
    linhas += ["", f"{ip._POR_EXTENSO[len(avisos)]} avisos sobre o texto abaixo:", ""] + [f"{i}. {a}" for i, a in enumerate(avisos, 1)] + [""]
    return "\n".join(linhas) + "\n"


def render(dados: dict, sinteses: dict, medidas: dict, topicos: list[tuple] | None = None, bloco_das_medidas=None) -> str:
    topicos = topicos or TOPICOS
    n = len(topicos)
    secoes = [secao(i, chave, dados[chave], (sinteses.get("topicos") or {}).get(chave) or {}, medidas) for i, (chave, *_) in enumerate(topicos, 1)]
    das_medidas = (bloco_das_medidas or corpo_das_medidas)(medidas)
    return (cabecalho(dados, topicos) + "\n" + "\n".join(secoes) + "\n" + bloco_rejeitadas(n + 1, dados) + "\n"
            + f"#### {SECAO}.{n + 2} O que o repositório já mediu sobre cada ideia\n" + das_medidas + "\n" + bloco_vereditos(n + 3, sinteses, medidas) + "\n" + bloco_mapa(n + 4, sinteses, medidas))


# ------------------------------------------------------------------ referências e índice (texto entra, texto sai)

def _sem_o_bloco(atual: str) -> str:
    """O arquivo sem o bloco desta rodada: o que vem antes do título dele e o que vem do título seguinte de nível 3 em diante."""
    if TITULO_REFS not in atual:
        return atual
    ini = atual.index(TITULO_REFS)
    m = re.search(r"^### ", atual[ini + len(TITULO_REFS):], re.MULTILINE)
    antes = atual[:ini].rstrip("\n")
    return antes + "\n\n" + atual[ini + len(TITULO_REFS) + m.start():] if m else antes + "\n"


def _selecionar(resto: str, dados: dict, topicos: list[tuple]) -> tuple[list[str], list[str]]:
    """Das referências aprovadas, na ordem dos tópicos: as que entram no bloco e as omitidas por já constarem no arquivo (em qualquer bloco, antes ou depois deste) ou
    por repetirem outra desta rodada."""
    linhas = [l[2:] for l in resto.splitlines() if l.startswith("- ")]
    chaves, urls = {ip._chave(l) for l in linhas}, {ip._url(l) for l in linhas} - {""}
    novas, omitidas_ = [], []
    for chave, *_ in topicos:
        for ref in referencias_do_topico(dados[chave]):
            ch, u = ip._chave(ref), ip._url(ref)
            if ch in chaves or (u and u in urls):
                omitidas_.append(ref)
                continue
            chaves.add(ch)
            if u:
                urls.add(u)
            novas.append(ref)
    return novas, omitidas_


def omitidas(atual: str, dados: dict, topicos: list[tuple] | None = None) -> list[str]:
    return _selecionar(_sem_o_bloco(atual), dados, topicos or TOPICOS)[1]


def referencias_com_bloco(atual: str, dados: dict, topicos: list[tuple] | None = None) -> tuple[str, int, int]:
    """O texto de referencias.md com o bloco desta rodada regravado logo antes do bloco da Pós-Fase 4 (ou do da Pré-Fase 4, ou no fim), sem repetir referência que já
    conste, e com o total da frase de abertura recontado. Devolve também quantas referências novas a rodada trouxe e o total do arquivo."""
    resto = _sem_o_bloco(atual)
    novas, _ = _selecionar(resto, dados, topicos or TOPICOS)
    bloco = "\n".join([TITULO_REFS, "",
                       ("<!-- ! Alteração de IA - Revisar: bloco gerado por ferramentas/integrar_pesquisa_fluxo_do_agente.py a partir das leituras e das segundas leituras da rodada 7 (as três "
                        "ideias para o fluxo do agente); só entram referências de fonte com afirmação aprovada na segunda leitura, na forma corrigida por ela, e as já presentes no arquivo "
                        "foram omitidas (mesma chave das outras rodadas, ou o mesmo endereço). O bloco fica antes do bloco da Pós-Fase 4."),
                       ("     ! Motivo: sem a conferência as mesmas fontes entrariam duas vezes e o total do arquivo ficaria errado; e o lugar é este porque o integrador da Pós-Fase 4 regrava "
                        "o bloco dele logo antes do da Pré-Fase 4, que o integrador dela trata como o último do arquivo. -->"),
                       ""] + [f"- {r}" for r in sorted(novas, key=ip._ordem)]) + "\n"
    ancora = next((t for t in (ipp.TITULO_REFS, ip.TITULO_REFS) if t in resto), None)
    if ancora:
        i = resto.index(ancora)
        novo = resto[:i].rstrip("\n") + "\n\n" + bloco + "\n" + resto[i:]
    else:
        novo = resto.rstrip("\n") + "\n\n" + bloco
    total = sum(1 for l in novo[novo.index("## 9. Referências levantadas"):].splitlines() if l.startswith("- "))
    m = re.search(r"os levantamentos de [^*\n]*? produziram as \*\*(\d+)\*\* referências abaixo", novo)
    assert m, "frase do total de referências não encontrada"
    novo = novo[:m.start()] + f"os levantamentos de {ip.DATAS_DOS_LEVANTAMENTOS} produziram as **{total}** referências abaixo" + novo[m.end():]
    return novo, len(novas), total


def _com_linha(s: str, tag: str, marca: str, linha: str, depois_de: str) -> str:
    """Grava (ou regrava) uma linha do índice, com a tag que a acompanha, logo depois da linha que começa por `depois_de`."""
    if marca in s:
        ini = s.rfind(tag, 0, s.index(marca))
        assert ini >= 0, "linha do índice sem a tag que a acompanha"
        fim = s.index("\n", s.index(marca)) + 1
        return s[:ini] + linha + s[fim:]
    assert depois_de in s, f"linha de referência do índice do Memorial não encontrada: {depois_de}"
    fim = s.index("\n", s.index(depois_de)) + 1
    return s[:fim] + linha + s[fim:]


def memorial_com_linhas(s: str, dados: dict, topicos: list[tuple] | None = None) -> str:
    """O texto do Memorial com as duas linhas desta rodada: a do levantamento, logo depois da linha da Pós-Fase 4, e a da proposta de desenho, na lista do método e
    ferramental, logo depois do protocolo da linha de base manual."""
    n = len(topicos or TOPICOS)
    do_levantamento = (TAG_DO_INDICE + f" (§{SECAO}), gravada por integrar_pesquisa_fluxo_do_agente.py. ! Motivo: sem a linha o índice não leva ao levantamento nem aos vereditos; ela é regravada a cada integração. -->\n"
                       + MARCA_DO_INDICE + f"(memorial/2-pesquisa-e-literatura/levantamento-2026-11-10-fluxo-do-agente.md): §{SECAO}, {n} tópicos lidos e conferidos por uma segunda leitura em {DATA}, "
                       "sobre as três ideias do Eric para o fluxo do agente (o raciocínio em passos e a confiança lida no token do rótulo, a lista de conferência em código, a reavaliação da própria "
                       "resposta, o segundo passe por sinal externo, o papel separado para escrever a base e os portões de validação); "
                       f"§{SECAO}.{n + 1} o que a segunda leitura corrigiu; §{SECAO}.{n + 2} o que o repositório já mediu; §{SECAO}.{n + 3} veredito por ideia; §{SECAO}.{n + 4} mapa adotado, adiado, descartado.\n")
    da_proposta = (TAG_DA_PROPOSTA + ", gravada por integrar_pesquisa_fluxo_do_agente.py. ! Motivo: sem a linha o índice não leva à proposta; ela é regravada a cada integração. -->\n"
                   + MARCA_DA_PROPOSTA + "(memorial/5-metodo-e-ferramental/proposta-analista-de-documentacao.md): proposta, não aprovada: o segundo momento do modelo, só para a documentação. "
                   "O que o analista de documentação recebe, quando é chamado, o que pode propor, os filtros e os portões que valem e os que faltam, quanto custa nesta máquina, o que teria de ser "
                   "medido e o que conflita com as decisões 69, 103 e 105 (ficha 67).\n")
    s = _com_linha(s, TAG_DO_INDICE, MARCA_DO_INDICE, do_levantamento, ipp.MARCA_DO_INDICE)
    return _com_linha(s, TAG_DA_PROPOSTA, MARCA_DA_PROPOSTA, da_proposta, ANCORA_DA_PROPOSTA)


# ------------------------------------------------------------------ a proposta de desenho e o resumo para o painel

_BLOCO_DE_MEDIDAS = re.compile(r"^<!-- medidas:([a-z0-9_]+) -->$", re.MULTILINE)


def proposta(modelo: str, medidas: dict, blocos: dict[str, str] | None = None) -> str:
    """A proposta de desenho gerada do modelo: os marcadores `{{m:campo}}` trocados pelo valor das medidas e cada linha `<!-- medidas:nome -->` trocada pela tabela de
    mesmo nome. Para se o modelo pedir uma tabela que não existe."""
    blocos = tabelas_das_medidas(medidas) if blocos is None else blocos

    def tabela(m: re.Match) -> str:
        if m.group(1) not in blocos:
            raise SystemExit(f"o modelo da proposta pede a tabela de medidas '{m.group(1)}', que o script não gera")
        return blocos[m.group(1)]

    texto = preencher(_BLOCO_DE_MEDIDAS.sub(tabela, modelo.replace("\r\n", "\n")), medidas)
    aviso = ("<!-- ! Alteração de IA - Revisar: arquivo gerado por ferramentas/integrar_pesquisa_fluxo_do_agente.py a partir de "
             "5-metodo-e-ferramental/dados/pesquisa-fluxo-do-agente/proposta-analista-de-documentacao.modelo.txt, com os números trocados pelos de medidas_do_repositorio.json. "
             "NÃO editar à mão: mude o modelo e rode o integrador (o --check compara com o regerado).\n"
             "     ! Motivo: a proposta cita custos e contagens das corridas, e a regra é nenhum número digitado à mão; gerada do modelo, ela muda sozinha se uma medida mudar. -->\n")
    return aviso + texto.rstrip("\n") + "\n"


def resumo_para_o_painel(dados: dict, sinteses: dict, medidas: dict, topicos: list[tuple] | None = None, quadros: dict | None = None) -> dict:
    """O que a aba do painel lê: as contagens por tópico, os totais, os vereditos e o mapa já com os números das medidas, as implicações de cada síntese e os quadros
    das medidas do repositório (`quadros`, de quadros_das_medidas)."""
    topicos = topicos or TOPICOS
    linhas = []
    for i, (chave, frente, titulo) in enumerate(topicos, 1):
        c, s = contagem(dados[chave]), (sinteses.get("topicos") or {}).get(chave) or {}
        linhas.append({"secao": f"{SECAO}.{i}", "chave": chave, "frente": frente, "titulo": titulo, "titulo_da_sintese": preencher(s.get("titulo", ""), medidas),
                       "fontes": len(dados[chave]["fontes"]), **c, "implicacoes": [preencher(x, medidas) for x in s.get("implicacoes") or []],
                       "lacunas": [preencher(x, medidas) for x in s.get("lacunas") or []]})
    totais = {"topicos": len(linhas), "fontes": sum(l["fontes"] for l in linhas), "afirmacoes": sum(len(f["afirmacoes"]) for k, *_ in topicos for f in dados[k]["fontes"]),
              **{c: sum(l[c] for l in linhas) for c in ("aprovadas", "parciais", "rejeitadas", "nao_verificadas")},
              "referencias_corrigidas": sum(1 for k, *_ in topicos for f in dados[k]["fontes"] if f["referencia_corrigida"])}
    return {
        "_tag": ("! Alteração de IA - Revisar: arquivo gerado por ferramentas/integrar_pesquisa_fluxo_do_agente.py (10/11/2026): o resumo da rodada 7 da pesquisa que a aba "
                 "\"Fluxo do agente\" do painel lê, com as contagens por tópico, os vereditos por ideia e o mapa já com os números das medidas. NÃO editar à mão."),
        "_motivo": ("! Motivo: a aba do painel lê arquivos versionados e não digita número; sem este resumo ela teria de repetir a leitura cruzada das leituras com as segundas "
                    "leituras e a troca dos marcadores, e as duas contas poderiam divergir."),
        "data": DATA, "secao": SECAO, "frentes": FRENTES, "topicos": linhas, "totais": totais,
        "vereditos": [{"ideia": v["ideia"], "nome": v["nome"], **{campo: preencher(v.get(campo, ""), medidas) for campo, _ in CAMPOS_DO_VEREDITO}} for v in sinteses.get("vereditos") or []],
        "mapa": [{**l, "motivo": preencher(l["motivo"], medidas)} for l in sinteses.get("mapa") or []],
        "tabelas": quadros or {},
    }


# ------------------------------------------------------------------ gravação e conferência

def _texto_do_resumo(dados: dict, sinteses: dict, medidas: dict) -> str:
    return json.dumps(resumo_para_o_painel(dados, sinteses, medidas, quadros=quadros_das_medidas(medidas)), ensure_ascii=False, indent=1) + "\n"


def integrar_referencias(dados: dict, simular: bool) -> None:
    atual, crlf = ip._ler(rl.REFERENCIAS)
    novo, novas, total = referencias_com_bloco(atual, dados)
    print(f"referências: {novas} novas desta rodada; total do arquivo {total}" + (" (simulado)" if simular else ("" if novo != atual else " (já estava em dia)")))
    for ref in omitidas(atual, dados):
        print("  omitida (já consta no arquivo ou em outro tópico):", ref[:110])
    if not simular and novo != atual:
        ip._gravar(rl.REFERENCIAS, novo, crlf)


def integrar_memorial(dados: dict, simular: bool) -> None:
    atual, crlf = ip._ler(MEMORIAL)
    novo = memorial_com_linhas(atual, dados)
    if not simular and novo != atual:
        ip._gravar(MEMORIAL, novo, crlf)
    print("Memorial: linhas do índice " + ("simuladas" if simular else ("gravadas" if novo != atual else "já estavam em dia")))


def check() -> int:
    if not LEVANTAMENTO.exists():
        print("--check: nada integrado ainda")
        return 1
    dados, sinteses, medidas = carregar(), ler_json(SINTESES), ler_json(MEDIDAS)
    falhas = 0

    def conferir(nome: str, esperado: list[str], atual: list[str]) -> None:
        nonlocal falhas
        if esperado == atual:
            print(f"--check: {nome} em dia")
            return
        falhas += 1
        print(f"--check: {nome} DIFERE do regerado")
        print("\n".join(list(difflib.unified_diff(atual, esperado, lineterm=""))[:30]))

    sem_apoio = citacoes_sem_apoio(dados, sinteses)
    if sem_apoio:
        falhas += 1
        print(f"--check: as sínteses citam fonte sem afirmação aprovada: {sem_apoio}")
    conferir(f"levantamento do fluxo do agente ({len(dados)} tópicos)", rl._normalizar(render(dados, sinteses, medidas)), rl._normalizar(LEVANTAMENTO.read_text(encoding="utf-8")))
    refs = ip._ler(rl.REFERENCIAS)[0]
    conferir("bloco de referências e total", referencias_com_bloco(refs, dados)[0].splitlines(), refs.splitlines())
    indice = ip._ler(MEMORIAL)[0]
    conferir("linhas do índice do Memorial", memorial_com_linhas(indice, dados).splitlines(), indice.splitlines())
    if MODELO_DA_PROPOSTA.exists():
        atual = PROPOSTA.read_text(encoding="utf-8").replace("\r\n", "\n").splitlines() if PROPOSTA.exists() else []
        conferir("proposta de desenho", proposta(MODELO_DA_PROPOSTA.read_text(encoding="utf-8"), medidas).splitlines(), atual)
    atual = RESUMO_DO_PAINEL.read_text(encoding="utf-8").splitlines() if RESUMO_DO_PAINEL.exists() else []
    conferir("resumo para o painel", _texto_do_resumo(dados, sinteses, medidas).splitlines(), atual)
    return 1 if falhas else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--simular", action="store_true")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    if args.check:
        return check()
    dados, sinteses, medidas = carregar(), ler_json(SINTESES), ler_json(MEDIDAS)
    sem_apoio = citacoes_sem_apoio(dados, sinteses)
    if sem_apoio:
        raise SystemExit(f"as sínteses citam fonte sem afirmação aprovada na segunda leitura: {sem_apoio}")
    for chave, topico in dados.items():
        c = contagem(topico)
        print(f"  {chave}: {len(topico['fontes'])} fontes; {c['aprovadas']} aprovadas ({c['parciais']} parciais), {c['rejeitadas']} rejeitadas, {c['nao_verificadas']} não verificadas")
    texto = render(dados, sinteses, medidas)
    saidas = [(LEVANTAMENTO, texto), (RESUMO_DO_PAINEL, _texto_do_resumo(dados, sinteses, medidas))]
    if MODELO_DA_PROPOSTA.exists():
        saidas.append((PROPOSTA, proposta(MODELO_DA_PROPOSTA.read_text(encoding="utf-8"), medidas)))
    for caminho, conteudo in saidas:
        if args.simular:
            print(f"{caminho.name}: {len(conteudo)} caracteres (simulado)")
        else:
            caminho.write_text(conteudo, encoding="utf-8", newline="\n")
            print(f"gravado: {caminho.name} ({len(conteudo)} caracteres)")
    integrar_referencias(dados, args.simular)
    integrar_memorial(dados, args.simular)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
