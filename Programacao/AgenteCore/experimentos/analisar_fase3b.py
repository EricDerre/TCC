#!/usr/bin/env python3
# ! Alteração de IA - Revisar: análise de fechamento da Fase 3-B (01/10/2026). Lê os registros avaliados da
# Fase 3 oficial, das duas pontes de versão (Ollama 0.34.1 e 0.34.4), dos 36 casos inéditos e da troca
# cruzada (L1 e L3 do qwen2.5:7b lidas pelos dois Coder) e grava analise_fase3b.json (registro) e
# analise_fase3b.md (blocos `<!-- tabela:tb_… -->` que o relatório da 3-B do Memorial cola; --check regera e
# compara, --colar cola). Faz os pareamentos caso a caso que os resumos de cada corrida não trazem: leitor
# com a biblioteca do doador contra o próprio L0 na mesma versão do Ollama, contra a própria biblioteca na
# Fase 3 e contra o doador lendo a mesma biblioteca; oficiais e inéditos somados (72 casos); e quantos casos
# mudam de certo para errado entre três corridas de L0 do mesmo modelo.
# ! Motivo: a troca cruzada grava só L1 e L3, sem L0 na mesma saída, então o resumo dela não tem pareamento
# nenhum (`pareado_vs_L0` vazio); `decidir_modelo.comparar_3b` pareia cada saída só contra a mesma (modelo,
# versão) da Fase 3, e a ponte de 30/09 mostrou que o Coder 7B não é pareável com a Fase 3 em 0.34.4 (decisão
# 47). Sem este script a pergunta da cruzada ("o ganho é da biblioteca ou de quem a lê?") seria respondida
# com números contados à mão, contra a regra do projeto.
"""Uso (em Programacao/AgenteCore/experimentos):
  RESULTADOS_DIR=resultados_alvo python analisar_fase3b.py [--check] [--colar]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from datetime import datetime
from itertools import combinations
from pathlib import Path

import avaliar
import avaliar_fase3
import caminhos
import taxonomia

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass

DOADOR = "qwen2.5:7b"
LEITORES = ["qwen2.5-coder:7b", "qwen2.5-coder:3b"]
PONTES = ["fase3b_ponte", "fase3b_ponte_0344"]
INEDITOS = "fase3b_ineditos"
CRUZADA = "fase3b_cruzada_qwen"
# ! Alteração de IA - Revisar: (06/10/2026) as duas corridas opcionais do roadmap entram na análise: o Coder 7B nos
# mesmos 36 inéditos (corrida 7, pasta `fase3b_ineditos_coder7b`) e a adesão cega sobre a L3 própria (corrida 5,
# `fase3b_a5`).
# ! Motivo: o Eric rodou as duas em 06/10. Os inéditos do Coder entram na mesma lista dos inéditos (as linhas e a soma
# com os oficiais saem iguais às dos outros modelos) e ganham o confronto modelo contra modelo, que era a condição 1 do
# comparativo qwen × Coder para rever a decisão 52; o A5 responde se a biblioteca própria muda a adesão cega (H5).
INEDITOS_EXTRA = ["fase3b_ineditos_coder7b"]
A5 = "fase3b_a5"
VERSOES_CRUZADA = (1, 3)
LIMITE_PONTE = 2  # decisão 47: até 2 casos discordantes em 36, a corrida é pareável com a Fase 3
# Casos cujo sintoma foi corrigido no banco em 28/09/2026 (achado 4.36, decisão 58): as corridas criadas a partir
# dessa data leram o texto novo; a Fase 3 e a ponte de 21/09, o antigo.
CASOS_DE_TEXTO_ALTERADO = frozenset({"efe-3", "efe-10"})
DATA_DA_CORRECAO = "2026-09-28"
EXP = Path(__file__).resolve().parent
F3 = caminhos.fase3("fase3")
SAIDA_JSON = F3["raiz"] / "analise_fase3b.json"
SAIDA_MD = F3["raiz"] / "analise_fase3b.md"
DOC_ALVO = EXP.parent.parent.parent / "Documentacao" / "memorial" / "3-resultados-e-analises" / "fase-3b-relatorio.md"
CLASSES = {k: (v.get("id", str(k)) if isinstance(v, dict) else str(v)) for k, v in taxonomia.CLASSES.items()}
NOMES_CONTRA = {"l0_ponte": "o próprio L0 na ponte (mesma versão do Ollama)", "propria": "a própria biblioteca na Fase 3",
                "doador": "o doador lendo a mesma biblioteca (Fase 3)"}


def ler(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def slug(modelo: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]", "_", modelo)


# ------------------------------------------------------------------ medidas sobre registros avaliados

def celula(avaliados: list[dict], modelo: str, epoca: int) -> dict[str, dict]:
    """Os registros de um (modelo, versão da biblioteca) na partição de avaliação, por id do caso."""
    return {r["caso"]: r for r in avaliados
            if r["modelo"] == modelo and r["biblioteca_epoca"] == epoca and r.get("particao") == "avaliacao"}


def _pct(parte: int, total: int) -> float | None:
    return round(100 * parte / total, 1) if total else None


def medir(cel: dict[str, dict]) -> dict:
    """Acerto, intervalo de Wilson, acurácia balanceada, uso do contexto e custo de uma célula."""
    regs = list(cel.values())
    n = len(regs)
    acertos = sum(1 for r in regs if r["causa_correta"])
    ic = avaliar.wilson(acertos, n) if n else (None, None)
    rotulo, parcela, distintos = avaliar_fase3.distribuicao_de_rotulos([r.get("causa_respondida") for r in regs])
    return {
        "n": n, "acertos": acertos, "acerto_pct": _pct(acertos, n), "ic95": [ic[0], ic[1]],
        "acuracia_balanceada_pct": avaliar_fase3.acuracia_balanceada([(r["causa_esperada"], r.get("causa_respondida")) for r in regs]) if n else None,
        "ouro_no_contexto_pct": _pct(sum(1 for r in regs if r.get("ouro_no_contexto")), n),
        "contexto_com_nota_pct": _pct(sum(1 for r in regs if r.get("contexto_com_nota")), n),
        "citou_verbete_anotado_pct": _pct(sum(1 for r in regs if r.get("citou_verbete_anotado")), n),
        "segundos_mediana": avaliar._mediana([r.get("segundos") for r in regs]),
        "tokens_entrada_mediana": avaliar._mediana([r.get("tokens_entrada") for r in regs]),
        "rotulo_mais_frequente": rotulo, "parcela_rotulo_pct": parcela, "n_rotulos": distintos,
    }


def parear(nova: dict[str, dict], base: dict[str, dict]) -> dict:
    """Pareamento caso a caso: b = casos que só `nova` acertou (ganhos), c = casos que só `base` acertou
    (perdas); McNemar exato e g de Cohen sobre b e c; delta em pontos percentuais sobre os casos comuns."""
    comuns = sorted(set(nova) & set(base))
    ganhos = [c for c in comuns if nova[c]["causa_correta"] and not base[c]["causa_correta"]]
    perdas = [c for c in comuns if base[c]["causa_correta"] and not nova[c]["causa_correta"]]
    b, c = len(ganhos), len(perdas)
    return {"n_comuns": len(comuns), "b": b, "c": c, "p_mcnemar": avaliar.mcnemar_exato(b, c),
            "g_cohen": avaliar_fase3.g_cohen(b, c), "delta_pp": round(100 * (b - c) / len(comuns), 1) if comuns else None,
            "ganhos": ganhos, "perdas": perdas,
            "rotulos_diferentes": sum(1 for x in comuns if nova[x].get("causa_respondida") != base[x].get("causa_respondida"))}


def sem_casos(cel: dict[str, dict], casos) -> dict[str, dict]:
    """A mesma célula sem os casos pedidos (os que não existem nela são ignorados)."""
    return {caso: r for caso, r in cel.items() if caso not in casos}


# ! Alteração de IA - Revisar: pareamento "com a mesma entrada" (01/10/2026, depois da revisão do relatório): quando uma
# das duas corridas rodou antes e a outra depois de um caso ter o texto corrigido, o caso sai da conta.
# ! Motivo: os casos `efe-3` e `efe-10` tiveram o sintoma corrigido em 28/09/2026 (achado 4.36). A ponte de 30/09 e a
# troca cruzada leram o texto novo; a Fase 3 e a ponte de 21/09, o antigo. Contar o `efe-3` como "caso que mudou entre
# corridas iguais" mistura a correção do caso com a variação do modelo: no Coder 7B são 4 casos com ele e 3 sem.
def mesma_entrada(nova: dict[str, dict], base: dict[str, dict], alterados=frozenset(), cruza: bool = False) -> dict:
    """Campos do pareamento refeito sem os casos de texto alterado, quando o par cruza a data da correção."""
    fora = sorted(set(alterados) & set(nova) & set(base)) if cruza else []
    par = parear(sem_casos(nova, fora), sem_casos(base, fora))
    return {"casos_de_texto_alterado": fora, "n_mesma_entrada": par["n_comuns"], "b_mesma_entrada": par["b"], "c_mesma_entrada": par["c"],
            "p_mesma_entrada": par["p_mcnemar"], "discordantes_mesma_entrada": par["b"] + par["c"], "casos_mesma_entrada": sorted(par["ganhos"] + par["perdas"])}


def juntar(**conjuntos: dict[str, dict]) -> dict[str, dict]:
    """Une células de conjuntos de casos diferentes (oficiais e inéditos) sem deixar ids iguais colidirem:
    a chave vira `conjunto:caso`."""
    return {f"{nome}:{caso}": r for nome, cel in conjuntos.items() for caso, r in cel.items()}


def ruido_entre_corridas(modelo: str, corridas: dict[str, dict[str, dict]], alterados=frozenset(), depois=frozenset()) -> list[dict]:
    """Para cada par de corridas do mesmo modelo e da mesma biblioteca (L0): quantos casos mudaram de certo
    para errado ou o contrário, quais, e quantos trocaram de rótulo. `alterados` são os casos que tiveram o texto
    corrigido e `depois` os nomes das corridas que rodaram depois da correção: no par que cruza a correção, esses
    casos saem da contagem "com a mesma entrada"."""
    linhas = []
    for (nome_a, cel_a), (nome_b, cel_b) in combinations(corridas.items(), 2):
        par = parear(cel_b, cel_a)
        linhas.append({"modelo": modelo, "corrida_a": nome_a, "corrida_b": nome_b, "n_comuns": par["n_comuns"],
                       "discordantes": par["b"] + par["c"], "b": par["b"], "c": par["c"],
                       "casos": sorted(par["ganhos"] + par["perdas"]), "rotulos_diferentes": par["rotulos_diferentes"],
                       **mesma_entrada(cel_b, cel_a, alterados, (nome_a in depois) != (nome_b in depois))})
    return linhas


def fontes_do_contexto(bruto: dict) -> list[str]:
    """Ids de verbete que a resposta cita na linha FONTE e que estavam no contexto recuperado. Mais tolerante
    que `avaliar.extrair`, que só lê um id por colchete: aqui `[a, b]` conta os dois."""
    m = re.search(r"FONTE\s*:\s*(.+)", (bruto.get("resposta") or "").replace("*", "").replace("`", ""), re.IGNORECASE)
    if not m:
        return []
    citados = re.findall(r"[a-z0-9_\-]+", m.group(1).lower())
    no_contexto = bruto.get("verbetes_ids") or []
    return [v for v in no_contexto if v in citados]


# ------------------------------------------------------------------ leitura dos arquivos

def _brutos(raiz: Path, modelo: str, epoca: int) -> dict[str, dict]:
    arq = raiz / slug(modelo) / f"diagnosticos__L{epoca}.jsonl"
    if not arq.exists():
        return {}
    regs = [json.loads(l) for l in arq.read_text(encoding="utf-8").splitlines() if l.strip()]
    return {r["caso"]: r for r in regs if r.get("particao", "avaliacao") == "avaliacao"}


def _texto_do_log(p: Path) -> str:
    b = p.read_bytes()
    return b.decode("utf-16") if b[:2] in (b"\xff\xfe", b"\xfe\xff") else b.decode("utf-8", errors="replace")


def resumo_da_corrida(saida: str) -> dict:
    """Contagem, versões do Ollama, erros e hash da biblioteca dos registros brutos de uma saída da 3-B, e a
    janela de horário lida dos marcos `== … dd/mm hh:mm:ss ==` do fase3b.log."""
    raiz = caminhos.fase3(saida)["raiz"]
    regs = []
    for arq in sorted(raiz.glob("*/diagnosticos__L*.jsonl")):
        regs += [json.loads(l) for l in arq.read_text(encoding="utf-8").splitlines() if l.strip()]
    condicoes = ler(raiz / "condicoes_3b.json") if (raiz / "condicoes_3b.json").exists() else {}
    inicio = fim = None
    log = raiz / "fase3b.log"
    if log.exists():
        marcos = re.findall(r"^== .*?(\d{2}/\d{2} \d{2}:\d{2}):\d{2} ==\s*$", _texto_do_log(log), re.M)
        if marcos:
            inicio, fim = marcos[0], marcos[-1]
    bibliotecas = sorted({f'L{r.get("biblioteca_epoca")}={r.get("biblioteca_versao")}' for r in regs})
    return {"saida": saida, "modo": condicoes.get("modo"), "doador": condicoes.get("doador"),
            "modelos": sorted({r["modelo"] for r in regs}), "n_registros": len(regs),
            "versoes_ollama": sorted({str(r.get("versao_ollama")) for r in regs}),
            "erros": sum(1 for r in regs if r.get("erro")), "bibliotecas": bibliotecas, "inicio": inicio, "fim": fim}


def carregar() -> dict:
    """Lê do disco tudo o que `montar` precisa (corridas oficiais em `caminhos.fase3`)."""
    pontes = []
    for nome in PONTES:
        c3 = caminhos.fase3(nome)
        if c3["avaliacao"].exists():
            condicoes = ler(c3["raiz"] / "condicoes_3b.json") if (c3["raiz"] / "condicoes_3b.json").exists() else {}
            pontes.append((nome, condicoes.get("versao_ollama") or "?", ler(c3["avaliacao"])))
    brutos = {}
    raiz_cruzada = caminhos.fase3(CRUZADA)["raiz"]
    raiz_ponte = caminhos.fase3(pontes[-1][0])["raiz"] if pontes else None
    for m in LEITORES:
        for epoca in VERSOES_CRUZADA:
            brutos[("cruzada", m, epoca)] = _brutos(raiz_cruzada, m, epoca)
        if raiz_ponte:
            brutos[("ponte", m, 0)] = _brutos(raiz_ponte, m, 0)
    def depois_da_correcao(saida: str) -> bool:
        arq = caminhos.fase3(saida)["raiz"] / "condicoes_3b.json"
        return arq.exists() and str(ler(arq).get("criado_em", "")) >= DATA_DA_CORRECAO

    depois = [nome for nome, _, _ in pontes if depois_da_correcao(nome)] + (["cruzada"] if depois_da_correcao(CRUZADA) else [])
    ineditos = ler(caminhos.fase3(INEDITOS)["avaliacao"])
    for nome in INEDITOS_EXTRA:
        c3 = caminhos.fase3(nome)
        if c3["avaliacao"].exists():
            ineditos += ler(c3["avaliacao"])
    c3_a5 = caminhos.fase3(A5)
    a5 = ler(c3_a5["avaliacao"]) if c3_a5["avaliacao"].exists() else []
    comp = F3["raiz"] / "comparacao_fases.json"
    adesao_2b = {m: d.get("adesao_cega_2B_A5_pct") for m, d in ler(comp).get("por_modelo", {}).items()} if comp.exists() else {}
    return {"f3": ler(F3["avaliacao"]), "pontes": pontes, "cruzada": ler(caminhos.fase3(CRUZADA)["avaliacao"]),
            "ineditos": ineditos, "brutos": brutos,
            "corridas": [resumo_da_corrida(s) for s in PONTES + [INEDITOS, CRUZADA] + INEDITOS_EXTRA + [A5] if caminhos.fase3(s)["raiz"].exists()],
            "doador": DOADOR, "leitores": LEITORES,
            "casos_de_texto_alterado": CASOS_DE_TEXTO_ALTERADO, "corridas_depois": frozenset(depois), "a5": a5, "adesao_2b": adesao_2b}


# ------------------------------------------------------------------ montagem

def _contagem_do_rotulo(rotulo: str | None, cel: dict[str, dict], l0: dict[str, dict]) -> dict:
    """Para o rótulo mais respondido de uma célula: quantas respostas o trazem, quantas o traziam com L0 e quantos
    casos o têm como causa no gabarito (um rótulo muito respondido que nenhum caso tem é sinal de desvio)."""
    return {"respostas_no_rotulo": sum(1 for r in cel.values() if r.get("causa_respondida") == rotulo),
            "respostas_no_rotulo_com_l0": sum(1 for r in l0.values() if r.get("causa_respondida") == rotulo),
            "casos_com_esse_gabarito": sum(1 for r in cel.values() if r.get("causa_esperada") == rotulo)}


def _linha_celula(leitor: str, epoca: int, origem: str, rotulo: str, versao: str | None, cel: dict[str, dict]) -> dict:
    return {"leitor": leitor, "biblioteca_epoca": epoca, "origem": origem, "biblioteca": rotulo, "versao_ollama": versao, **medir(cel)}


def montar(f3: list[dict], pontes: list[tuple[str, str, list[dict]]], cruzada: list[dict], ineditos: list[dict],
           brutos: dict, corridas: list[dict], doador: str, leitores: list[str],
           casos_de_texto_alterado=frozenset(), corridas_depois=frozenset(), a5: list[dict] | None = None,
           adesao_2b: dict | None = None) -> dict:
    """Monta o registro da análise. `pontes` vem na ordem em que rodaram; a última é a linha de base (L0) da
    troca cruzada, por ser a que rodou na mesma versão do Ollama. `casos_de_texto_alterado` são os casos corrigidos
    depois da Fase 3 e `corridas_depois` os nomes das saídas que rodaram depois da correção (o nome "cruzada" vale
    para a troca cruzada); a Fase 3 é sempre anterior. `ineditos` pode trazer mais de um modelo (o Coder 7B rodou nos
    mesmos 36 em 06/10); `a5` são os registros avaliados da adesão cega sobre a L3 própria e `adesao_2b` a adesão
    cega de cada modelo na Fase 2-B (A5 sobre a biblioteca original), para a comparação."""
    modelos = [doador] + list(leitores)
    versao_f3 = "0.34.0"
    nome_ponte, versao_ponte, av_ponte = pontes[-1]
    alterados = frozenset(casos_de_texto_alterado)
    cruzada_depois = "cruzada" in corridas_depois

    # --- pontes de versão: L0 de cada ponte contra o L0 da Fase 3
    bloco_pontes = []
    for nome, versao, av in pontes:
        linhas = []
        for m in sorted({r["modelo"] for r in av}):
            cel = celula(av, m, 0)
            par = parear(cel, celula(f3, m, 0))
            med = medir(cel)
            igual = mesma_entrada(cel, celula(f3, m, 0), alterados, nome in corridas_depois)
            linhas.append({"modelo": m, "n": med["n"], "acerto_pct": med["acerto_pct"], "ic95": med["ic95"],
                           "acuracia_balanceada_pct": med["acuracia_balanceada_pct"], **par,
                           "pareavel": par["b"] + par["c"] <= LIMITE_PONTE, **igual,
                           "pareavel_mesma_entrada": igual["discordantes_mesma_entrada"] <= LIMITE_PONTE})
        bloco_pontes.append({"saida": nome, "versao": versao, "linhas": linhas})

    # --- quantos casos mudam entre corridas de L0 do mesmo modelo
    ruido, oscilam = [], {}
    for m in modelos:
        corridas_l0 = {f"Fase 3 ({versao_f3})": celula(f3, m, 0)}
        depois = set()
        for nome, versao, av in pontes:
            if celula(av, m, 0):
                corridas_l0[f"ponte {versao}"] = celula(av, m, 0)
                if nome in corridas_depois:
                    depois.add(f"ponte {versao}")
        ruido += ruido_entre_corridas(m, corridas_l0, alterados, depois)
        # casos em que o acerto do modelo não foi o mesmo em todas as corridas de L0 (oscilam sem a biblioteca mudar)
        comuns = set.intersection(*(set(c) for c in corridas_l0.values()))
        oscilam[m] = sorted(c for c in comuns if len({cel[c]["causa_correta"] for cel in corridas_l0.values()}) > 1)

    # --- casos inéditos e a soma com os 36 oficiais
    linhas_ineditos, agrupado = [], []
    for m in sorted({r["modelo"] for r in ineditos}):
        base_in = celula(ineditos, m, 0)
        for epoca in sorted({r["biblioteca_epoca"] for r in ineditos if r["modelo"] == m}):
            cel = celula(ineditos, m, epoca)
            linha = {"modelo": m, "biblioteca_epoca": epoca, **medir(cel)}
            if epoca != 0:
                par_in = parear(cel, base_in)
                linha["contra_l0"] = par_in
                # o mesmo modelo, a mesma versão da biblioteca, nos 36 oficiais da Fase 3 (para comparar as trocas de rótulo)
                linha["rotulos_diferentes_nos_oficiais"] = parear(celula(f3, m, epoca), celula(f3, m, 0))["rotulos_diferentes"]
                par_of = parear(celula(f3, m, epoca), celula(f3, m, 0))
                soma = parear(juntar(oficiais=celula(f3, m, epoca), ineditos=cel),
                              juntar(oficiais=celula(f3, m, 0), ineditos=base_in))
                nova = juntar(oficiais=celula(f3, m, epoca), ineditos=cel)
                velha = juntar(oficiais=celula(f3, m, 0), ineditos=base_in)
                agrupado.append({"modelo": m, "biblioteca_epoca": epoca, "oficiais": {k: par_of[k] for k in ("b", "c")},
                                 "ineditos": {k: par_in[k] for k in ("b", "c")}, **soma,
                                 "acerto_l0_pct": _pct(sum(1 for r in velha.values() if r["causa_correta"]), len(velha)),
                                 "acerto_pct": _pct(sum(1 for r in nova.values() if r["causa_correta"]), len(nova))})
            linhas_ineditos.append(linha)

    # --- os mesmos inéditos, modelo contra modelo (corrida 7: o Coder 7B nos 36 que o doador já tinha rodado)
    entre_modelos = []
    for m in sorted({r["modelo"] for r in ineditos} - {doador}):
        for epoca in sorted({r["biblioteca_epoca"] for r in ineditos if r["modelo"] == m}):
            cel_m, cel_d = celula(ineditos, m, epoca), celula(ineditos, doador, epoca)
            if not cel_m or not cel_d:
                continue
            par = parear(cel_m, cel_d)
            soma = parear(juntar(oficiais=celula(f3, m, epoca), ineditos=cel_m), juntar(oficiais=celula(f3, doador, epoca), ineditos=cel_d))
            por_classe_m = {}
            for k, nome in sorted(CLASSES.items()):
                rm = [r for r in cel_m.values() if r.get("classe") == k]
                rd = [r for r in cel_d.values() if r.get("classe") == k]
                if rm:
                    por_classe_m[nome] = {"n": len(rm), "acertos": sum(1 for r in rm if r["causa_correta"]), "acertos_doador": sum(1 for r in rd if r["causa_correta"])}
            entre_modelos.append({"modelo": m, "doador": doador, "biblioteca_epoca": epoca, "acerto_pct": medir(cel_m)["acerto_pct"],
                                  "acerto_doador_pct": medir(cel_d)["acerto_pct"],
                                  **{k: par[k] for k in ("n_comuns", "b", "c", "p_mcnemar", "delta_pp", "ganhos", "perdas", "rotulos_diferentes")},
                                  "somados": {k: soma[k] for k in ("n_comuns", "b", "c", "p_mcnemar", "delta_pp")}, "por_classe": por_classe_m})

    # --- adesão cega sobre a biblioteca própria (corrida 5: A5 sobre a L3 de cada modelo nos 36 oficiais)
    linhas_a5 = []
    for m in sorted({r["modelo"] for r in (a5 or [])}):
        regs = [r for r in a5 if r["modelo"] == m]
        epoca = regs[0]["biblioteca_epoca"]
        n = len(regs)
        seguiu = sum(1 for r in regs if r.get("seguiu_causa_plantada"))
        acertos = sum(1 for r in regs if r["causa_correta"])
        linhas_a5.append({"modelo": m, "biblioteca_epoca": epoca, "n": n, "seguiu": seguiu, "seguiu_pct": _pct(seguiu, n), "acertos": acertos,
                          "acerto_pct": _pct(acertos, n), "ouro_no_contexto_pct": _pct(sum(1 for r in regs if r.get("ouro_no_contexto")), n),
                          "acerto_a2_pct": medir(celula(f3, m, epoca))["acerto_pct"], "adesao_2b_pct": (adesao_2b or {}).get(m)})

    # --- troca cruzada
    celulas, pareados, cochran, por_classe, rotulos, casos = [], [], [], [], [], []
    for m in modelos:
        celulas.append(_linha_celula(m, 0, "fase3", f"L0, Fase 3 (Ollama {versao_f3})", versao_f3, celula(f3, m, 0)))
        celulas.append(_linha_celula(m, 0, "ponte", f"L0, ponte (Ollama {versao_ponte})", versao_ponte, celula(av_ponte, m, 0)))
        for epoca in VERSOES_CRUZADA:
            celulas.append(_linha_celula(m, epoca, "fase3", f"L{epoca} própria, Fase 3 (Ollama {versao_f3})", versao_f3, celula(f3, m, epoca)))
        if m == doador:
            continue
        for epoca in VERSOES_CRUZADA:
            celulas.append(_linha_celula(m, epoca, "cruzada", f"L{epoca} do doador, cruzada (Ollama {versao_ponte})", versao_ponte, celula(cruzada, m, epoca)))
    pareavel = {l["modelo"]: l["pareavel"] for l in bloco_pontes[-1]["linhas"]}
    for m in leitores:
        l0 = celula(av_ponte, m, 0)
        for epoca in VERSOES_CRUZADA:
            nova = celula(cruzada, m, epoca)
            for contra, base, ok, cruza in (("l0_ponte", l0, True, cruzada_depois != (nome_ponte in corridas_depois)),
                                            ("propria", celula(f3, m, epoca), pareavel.get(m, False), cruzada_depois),
                                            ("doador", celula(f3, doador, epoca), pareavel.get(m, False) and pareavel.get(doador, False), cruzada_depois)):
                par = parear(nova, base)
                pareados.append({"leitor": m, "biblioteca_epoca": epoca, "contra": contra, "mesma_versao_do_ollama": contra == "l0_ponte",
                                 "pareavel_pela_ponte": ok, **par, **mesma_entrada(nova, base, alterados, cruza),
                                 "em_casos_que_oscilam": sorted(set(par["ganhos"] + par["perdas"]) & set(oscilam.get(m, []))) if contra == "l0_ponte" else []})
            bruto = brutos.get(("cruzada", m, epoca), {})
            bruto_l0 = brutos.get(("ponte", m, 0), {})
            citadas = Counter(v for r in bruto.values() for v in set(fontes_do_contexto(r)))
            presentes = Counter(v for r in bruto.values() for v in set(r.get("verbetes_ids") or []))
            med = medir(nova)
            rotulos.append({"leitor": m, "biblioteca": f"L{epoca} do doador", "rotulo_mais_frequente": med["rotulo_mais_frequente"],
                            "parcela_rotulo_pct": med["parcela_rotulo_pct"], "n_rotulos": med["n_rotulos"],
                            **_contagem_do_rotulo(med["rotulo_mais_frequente"], nova, l0),
                            "fontes_mais_citadas": [{"verbete": v, "respostas": q} for v, q in sorted(citadas.items(), key=lambda x: (-x[1], x[0]))[:3]],
                            "verbetes_mais_presentes": [{"verbete": v, "casos": q} for v, q in sorted(presentes.items(), key=lambda x: (-x[1], x[0]))[:3]]})
            for caso in sorted(nova):
                if caso in l0 and nova[caso]["causa_correta"] != l0[caso]["causa_correta"]:
                    casos.append({"leitor": m, "biblioteca_epoca": epoca, "caso": caso, "mudou_para": "certo" if nova[caso]["causa_correta"] else "errado",
                                  "esperado": nova[caso]["causa_esperada"], "resposta_l0": l0[caso].get("causa_respondida"),
                                  "resposta": nova[caso].get("causa_respondida"), "ouro_no_contexto": bool(nova[caso].get("ouro_no_contexto")),
                                  "fontes_citadas": fontes_do_contexto(bruto.get(caso, {})), "fontes_citadas_l0": fontes_do_contexto(bruto_l0.get(caso, {})),
                                  "doador_acertou": bool(celula(f3, doador, epoca).get(caso, {}).get("causa_correta"))})
        med0 = medir(l0)
        citadas0 = Counter(v for r in brutos.get(("ponte", m, 0), {}).values() for v in set(fontes_do_contexto(r)))
        presentes0 = Counter(v for r in brutos.get(("ponte", m, 0), {}).values() for v in set(r.get("verbetes_ids") or []))
        rotulos.append({"leitor": m, "biblioteca": "L0 (ponte)", "rotulo_mais_frequente": med0["rotulo_mais_frequente"],
                        "parcela_rotulo_pct": med0["parcela_rotulo_pct"], "n_rotulos": med0["n_rotulos"],
                        **_contagem_do_rotulo(med0["rotulo_mais_frequente"], l0, l0),
                        "fontes_mais_citadas": [{"verbete": v, "respostas": q} for v, q in sorted(citadas0.items(), key=lambda x: (-x[1], x[0]))[:3]],
                        "verbetes_mais_presentes": [{"verbete": v, "casos": q} for v, q in sorted(presentes0.items(), key=lambda x: (-x[1], x[0]))[:3]]})
        comuns = sorted(set(l0) & set(celula(cruzada, m, 1)) & set(celula(cruzada, m, 3)))
        q, gl, p = avaliar_fase3.cochran_q([[l0[c]["causa_correta"], celula(cruzada, m, 1)[c]["causa_correta"],
                                             celula(cruzada, m, 3)[c]["causa_correta"]] for c in comuns])
        cochran.append({"leitor": m, "condicoes": ["L0 (ponte)", "L1 do doador", "L3 do doador"], "n": len(comuns), "q": q, "gl": gl, "p": p})
        for rotulo_bib, cel in ([("L0 (ponte)", l0)] + [(f"L{e} do doador", celula(cruzada, m, e)) for e in VERSOES_CRUZADA]
                                + [(f"L{e} própria (Fase 3)", celula(f3, m, e)) for e in VERSOES_CRUZADA]):
            for k, nome in sorted(CLASSES.items()):
                regs = [r for r in cel.values() if r.get("classe") == k]
                if regs:
                    por_classe.append({"leitor": m, "biblioteca": rotulo_bib, "classe": nome, "acertos": sum(1 for r in regs if r["causa_correta"]), "n": len(regs)})

    return {
        "metadados": {"gerado_em": datetime.now().isoformat(timespec="seconds"), "doador": doador, "leitores": list(leitores),
                      "limite_da_ponte": LIMITE_PONTE, "ponte_de_base": nome_ponte, "versao_da_ponte_de_base": versao_ponte,
                      "casos_de_texto_alterado": sorted(alterados), "corridas_depois_da_correcao": sorted(corridas_depois),
                      "fontes": {"fase3": "resultados_alvo/fase3/avaliacao_fase3.json", "pontes": [n for n, _, _ in pontes],
                                 "ineditos": INEDITOS, "ineditos_extra": INEDITOS_EXTRA, "a5": A5, "cruzada": CRUZADA}},
        "corridas": corridas,
        "pontes": bloco_pontes,
        "ruido_l0": ruido,
        "oscilam_em_l0": oscilam,
        "ineditos": {"linhas": linhas_ineditos, "agrupado": agrupado, "entre_modelos": entre_modelos,
                     "efeito_minimo_detectavel": avaliar_fase3.efeito_minimo_detectavel((36, 72))},
        "a5": {"linhas": linhas_a5},
        "cruzada": {"celulas": celulas, "pareados": pareados, "cochran": cochran, "por_classe": por_classe, "rotulos": rotulos, "casos": casos},
    }


# ------------------------------------------------------------------ markdown (blocos colados no Memorial)

def f(v, casas=1) -> str:
    if v is None:
        return "n/a"
    if isinstance(v, bool):
        return "sim" if v else "não"
    if isinstance(v, float):
        return f"{v:.{casas}f}".replace(".", ",")
    return str(v)


def fd(v) -> str:
    return "n/a" if v is None else (f"{v:+.1f}".replace(".", ",") + " pp")


def fic(ic) -> str:
    return "n/a" if not ic or ic[0] is None else f"{f(float(ic[0]))} a {f(float(ic[1]))}"


def fcasos(lista: list[str]) -> str:
    return ", ".join(f"`{c}`" for c in lista) if lista else "nenhum"


def tab(nome: str, cab: list[str], linhas: list[list[str]]) -> str:
    corpo = "\n".join("| " + " | ".join(l) + " |" for l in linhas)
    return f"<!-- tabela:{nome} -->\n| " + " | ".join(cab) + " |\n|" + "---|" * len(cab) + f"\n{corpo}\n<!-- /tabela:{nome} -->"


def render(dado: dict) -> str:
    cz = dado["cruzada"]
    nomes_classe = [nome for _, nome in sorted(CLASSES.items())]
    blocos = []
    blocos.append(tab("tb_corridas", ["Corrida (pasta em `resultados_alvo/`)", "Modo", "Modelos", "Registros", "Ollama nos registros", "Erros", "Bibliotecas lidas (hash)", "Início", "Fim"],
                      [[f'`{c["saida"]}`', f(c["modo"]), ", ".join(c["modelos"]), f(c["n_registros"]), ", ".join(c["versoes_ollama"]), f(c["erros"]),
                        "; ".join(c["bibliotecas"]), f(c["inicio"]), f(c["fim"])] for c in dado["corridas"]]))
    blocos.append(tab("tb_pontes", ["Ponte (Ollama)", "Modelo", "Acerto em L0 nos 36 (IC 95%)", "Acurácia balanceada", "b", "c", "p (McNemar)", "Passaram a certos", "Passaram a errados", f"Pareável (b + c até {dado['metadados']['limite_da_ponte']})", "b / c sem o caso de texto corrigido", "Caso de texto corrigido entre as corridas"],
                      [[p["versao"], f'`{l["modelo"]}`', f'{f(l["acerto_pct"])}% ({fic(l["ic95"])})', f(l["acuracia_balanceada_pct"]) + "%", f(l["b"]), f(l["c"]), f(l["p_mcnemar"], 4),
                        fcasos(l["ganhos"]), fcasos(l["perdas"]), "sim" if l["pareavel"] else "**não**", f'{l["b_mesma_entrada"]} / {l["c_mesma_entrada"]}',
                        fcasos(l["casos_de_texto_alterado"])] for p in dado["pontes"] for l in p["linhas"]]))
    blocos.append(tab("tb_ruido", ["Modelo (L0, 36 casos)", "Corrida A", "Corrida B", "Casos que mudaram de acerto", "Com a mesma entrada (sem o caso de texto corrigido)", "Só B acertou", "Só A acertou", "Rótulos que mudaram", "Quais mudaram de acerto"],
                      [[f'`{l["modelo"]}`', l["corrida_a"], l["corrida_b"], f(l["discordantes"]), f(l["discordantes_mesma_entrada"]), f(l["b"]), f(l["c"]), f(l["rotulos_diferentes"]), fcasos(l["casos"])] for l in dado["ruido_l0"]]))
    blocos.append(tab("tb_ineditos", ["Modelo", "Biblioteca", "Acerto nos 36 inéditos (IC 95%)", "Acurácia balanceada", "Contra L0: b / c", "p (McNemar)", "Rótulos que mudaram contra L0", "s por diagnóstico (mediana)"],
                      [[f'`{l["modelo"]}`', f'L{l["biblioteca_epoca"]}', f'{f(l["acerto_pct"])}% ({fic(l["ic95"])})', f(l["acuracia_balanceada_pct"]) + "%",
                        f'{l["contra_l0"]["b"]} / {l["contra_l0"]["c"]}' if l.get("contra_l0") else "n/a",
                        f(l["contra_l0"]["p_mcnemar"], 4) if l.get("contra_l0") else "n/a",
                        f(l["contra_l0"]["rotulos_diferentes"]) if l.get("contra_l0") else "n/a", f(l["segundos_mediana"])] for l in dado["ineditos"]["linhas"]]))
    blocos.append(tab("tb_agrupado", ["Modelo", "Biblioteca", "Casos (oficiais + inéditos)", "Acerto com L0", "Acerto com a biblioteca", "Oficiais: b / c", "Inéditos: b / c", "Somados: b / c", "Diferença", "p (McNemar)"],
                      [[f'`{l["modelo"]}`', f'L{l["biblioteca_epoca"]}', f(l["n_comuns"]), f(l["acerto_l0_pct"]) + "%", f(l["acerto_pct"]) + "%", f'{l["oficiais"]["b"]} / {l["oficiais"]["c"]}',
                        f'{l["ineditos"]["b"]} / {l["ineditos"]["c"]}', f'{l["b"]} / {l["c"]}', fd(l["delta_pp"]), f(l["p_mcnemar"], 4)] for l in dado["ineditos"]["agrupado"]]))
    blocos.append(tab("tb_ineditos_modelos", ["Modelo", "Biblioteca (a de cada um)", "Acerto nos 36 inéditos", f"Acerto do `{dado['metadados']['doador']}`", "b (só o modelo)", "c (só o doador)",
                                              "Diferença", "p (McNemar)", "Rótulos diferentes", "Nos 72 (oficiais + inéditos): b / c", "p nos 72"]
                      + [f"{n}: modelo / doador (acertos de n)" for n in nomes_classe],
                      [[f'`{l["modelo"]}`', f'L{l["biblioteca_epoca"]}', f(l["acerto_pct"]) + "%", f(l["acerto_doador_pct"]) + "%", f(l["b"]), f(l["c"]), fd(l["delta_pp"]), f(l["p_mcnemar"], 4),
                        f(l["rotulos_diferentes"]), f'{l["somados"]["b"]} / {l["somados"]["c"]}', f(l["somados"]["p_mcnemar"], 4)]
                       + [f'{l["por_classe"][n]["acertos"]} / {l["por_classe"][n]["acertos_doador"]} (de {l["por_classe"][n]["n"]})' if n in l["por_classe"] else "n/a" for n in nomes_classe]
                       for l in dado["ineditos"].get("entre_modelos", [])]))
    blocos.append(tab("tb_a5", ["Modelo", "Biblioteca", "Casos", "Seguiu a causa plantada", "Acertou mesmo assim", "O mesmo modelo, a mesma biblioteca, em A2 (Fase 3, acerto)",
                                "Adesão cega na Fase 2-B (A5 sobre a biblioteca original)", "Verbete de ouro no contexto"],
                      [[f'`{l["modelo"]}`', f'L{l["biblioteca_epoca"]} própria', f(l["n"]), f'{l["seguiu"]} ({f(l["seguiu_pct"])}%)', f'{l["acertos"]} ({f(l["acerto_pct"])}%)',
                        f(l["acerto_a2_pct"]) + "%", "não medida" if l["adesao_2b_pct"] is None else f(l["adesao_2b_pct"]) + "%", f(l["ouro_no_contexto_pct"]) + "%"]
                       for l in dado.get("a5", {}).get("linhas", [])]))
    blocos.append(tab("tb_cruzada", ["Quem lê", "Biblioteca lida", "Acerto nos 36 (IC 95%)", "Acurácia balanceada", "Verbete de ouro no contexto", "Contexto com nota", "Citou verbete anotado", "Tokens de entrada (mediana)", "s por diagnóstico (mediana)"],
                      [[f'`{c["leitor"]}`', c["biblioteca"], f'{f(c["acerto_pct"])}% ({fic(c["ic95"])})', f(c["acuracia_balanceada_pct"]) + "%", f(c["ouro_no_contexto_pct"]) + "%",
                        f(c["contexto_com_nota_pct"]) + "%", f(c["citou_verbete_anotado_pct"]) + "%", f(c["tokens_entrada_mediana"], 0), f(c["segundos_mediana"])] for c in cz["celulas"]]))
    blocos.append(tab("tb_cruzada_pareados", ["Leitor com a biblioteca do doador", "Comparado com", "Mesma versão do Ollama", "Pareável pela ponte", "b (ganhos)", "c (perdas)", "Diferença", "p (McNemar)", "b / c sem o caso de texto corrigido", "Rótulos que mudaram", "Ganhou", "Perdeu", "Trocas em casos que já oscilam entre corridas de L0"],
                      [[f'`{p["leitor"]}` lendo L{p["biblioteca_epoca"]}', NOMES_CONTRA[p["contra"]], f(p["mesma_versao_do_ollama"]), f(p["pareavel_pela_ponte"]), f(p["b"]), f(p["c"]), fd(p["delta_pp"]),
                        f(p["p_mcnemar"], 4), f'{p["b_mesma_entrada"]} / {p["c_mesma_entrada"]}', f(p["rotulos_diferentes"]), fcasos(p["ganhos"]), fcasos(p["perdas"]),
                        fcasos(p["em_casos_que_oscilam"]) if p["contra"] == "l0_ponte" else "n/a"] for p in cz["pareados"]]
                      ))
    linhas_classe = []
    for chave in dict.fromkeys((l["leitor"], l["biblioteca"]) for l in cz["por_classe"]):
        por = {l["classe"]: l for l in cz["por_classe"] if (l["leitor"], l["biblioteca"]) == chave}
        linhas_classe.append([f"`{chave[0]}`", chave[1]] + [f'{por[n]["acertos"]} / {por[n]["n"]}' if n in por else "n/a" for n in nomes_classe])
    blocos.append(tab("tb_cruzada_classe", ["Quem lê", "Biblioteca lida"] + [f"{n} (acertos / casos)" for n in nomes_classe], linhas_classe))
    blocos.append(tab("tb_cruzada_rotulos", ["Quem lê", "Biblioteca lida", "Rótulo mais respondido", "Respostas com ele", "Respostas com ele em L0", "Casos com essa causa no gabarito", "Rótulos distintos", "Verbetes mais citados na linha FONTE (respostas)", "Verbetes mais presentes no contexto (casos)"],
                      [[f'`{r["leitor"]}`', r["biblioteca"], f'`{r["rotulo_mais_frequente"]}`', f'{f(r["respostas_no_rotulo"])} ({f(r["parcela_rotulo_pct"])}%)', f(r["respostas_no_rotulo_com_l0"]), f(r["casos_com_esse_gabarito"]), f(r["n_rotulos"]),
                        "; ".join(f'`{x["verbete"]}` ({x["respostas"]})' for x in r["fontes_mais_citadas"]) or "n/a",
                        "; ".join(f'`{x["verbete"]}` ({x["casos"]})' for x in r.get("verbetes_mais_presentes", [])) or "n/a"] for r in cz["rotulos"]]))
    blocos.append(tab("tb_cruzada_casos", ["Quem lê", "Biblioteca do doador", "Caso", "Passou a", "Causa do gabarito", "Resposta com L0", "Resposta com a biblioteca do doador", "Fonte citada com L0", "Fonte citada com a biblioteca do doador", "Verbete de ouro no contexto", "O doador acerta este caso com ela"],
                      [[f'`{c["leitor"]}`', f'L{c["biblioteca_epoca"]}', f'`{c["caso"]}`', c["mudou_para"], f'`{c["esperado"]}`', f'`{c["resposta_l0"]}`', f'`{c["resposta"]}`',
                        fcasos(c["fontes_citadas_l0"]), fcasos(c["fontes_citadas"]), f(c["ouro_no_contexto"]), f(c["doador_acertou"])] for c in cz["casos"]]))
    m = dado["metadados"]
    cab = ["<!-- ! Alteração de IA - Revisar: documento DERIVADO, gerado por analisar_fase3b.py a partir dos registros avaliados da Fase 3 e da Fase 3-B (--check regera e compara); não editar à mão.",
           "     ! Motivo: nenhum número digitado à mão; o relatório da Fase 3-B do Memorial cola estes blocos. -->",
           f"# Análise de fechamento da Fase 3-B, gerada em {m['gerado_em'][:10]}", "",
           f"Doador da troca cruzada: `{m['doador']}`. Leitores: {', '.join('`' + x + '`' for x in m['leitores'])}. Linha de base da cruzada: L0 da ponte `{m['ponte_de_base']}` "
           f"(Ollama {m['versao_da_ponte_de_base']}). b conta os casos que só a primeira condição acertou; c, os que só a segunda acertou. "
           f"Uma ponte é pareável com a Fase 3 quando b + c fica em até {m['limite_da_ponte']} (decisão 47).", ""]
    return "\n".join(cab) + "\n\n" + "\n\n".join(blocos) + "\n"


# ------------------------------------------------------------------ colagem no documento do Memorial

BLOCO_CHEIO_RE = re.compile(r"(<!-- tabela:(tb_[a-z0-9_]+) -->\n.*?\n<!-- /tabela:\2 -->)", re.S)
BLOCO_ALVO_RE = re.compile(r"<!-- tabela:(tb_[a-z0-9_]+) -->\n(?:.*?\n)?<!-- /tabela:\1 -->", re.S)


def blocos_de(md: str) -> dict[str, str]:
    return {m.group(2): m.group(1) for m in BLOCO_CHEIO_RE.finditer(md)}


def colar(doc: Path, md: str) -> tuple[int, bool]:
    """Substitui todo bloco `<!-- tabela:tb_X -->…<!-- /tabela:tb_X -->` do documento (vazio ou não) pelo bloco
    gerado; um nome sem bloco gerado interrompe."""
    blocos = blocos_de(md)
    s = doc.read_text(encoding="utf-8")
    faltando = [n for n in BLOCO_ALVO_RE.findall(s) if n not in blocos]
    if faltando:
        raise SystemExit(f"{doc.name}: bloco(s) sem tabela gerada: {faltando}")
    novo, n = BLOCO_ALVO_RE.subn(lambda m: blocos[m.group(1)], s)
    if novo != s:
        doc.write_text(novo, encoding="utf-8", newline="\n")
    return n, novo != s


def conferir_doc(doc: Path, md: str) -> list[str]:
    blocos = blocos_de(md)
    return [n for n, b in blocos_de(doc.read_text(encoding="utf-8")).items() if blocos.get(n) != b]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true", help="regera e compara com os arquivos gravados e com os blocos do Memorial")
    ap.add_argument("--colar", action="store_true", help="cola os blocos gerados no relatório da Fase 3-B do Memorial")
    args = ap.parse_args()
    print(caminhos.descricao())
    dado = montar(**carregar())
    md = render(dado)
    if args.check:
        atual = SAIDA_MD.read_text(encoding="utf-8") if SAIDA_MD.exists() else ""
        antigo = ler(SAIDA_JSON) if SAIDA_JSON.exists() else {}
        sem_data = lambda d: {k: ({kk: vv for kk, vv in v.items() if kk != "gerado_em"} if k == "metadados" else v) for k, v in d.items()}  # noqa: E731
        ok_json = sem_data(antigo) == sem_data(json.loads(json.dumps(dado, ensure_ascii=False)))
        ok_md = atual.split("\n", 3)[-1] == md.split("\n", 3)[-1] if atual else False
        divergentes = conferir_doc(DOC_ALVO, md) if DOC_ALVO.exists() else []
        if ok_json and ok_md and not divergentes:
            doc = f"os blocos de {DOC_ALVO.name}" if DOC_ALVO.exists() else f"({DOC_ALVO.name} ainda não existe, nada a conferir nele)"
            print(f"--check: {SAIDA_MD.name}, {SAIDA_JSON.name} e {doc} batem com os dados atuais")
            return
        print(f"--check: DIFERE (json {'ok' if ok_json else 'difere'}; md {'ok' if ok_md else 'difere'}; "
              f"blocos divergentes no documento: {divergentes})")
        sys.exit(1)
    if args.colar:
        n, mudou = colar(DOC_ALVO, md)
        print(f"{DOC_ALVO.name}: {n} bloco(s) colado(s); mudou: {mudou}")
        return
    SAIDA_JSON.write_text(json.dumps(dado, ensure_ascii=False, indent=2), encoding="utf-8")
    SAIDA_MD.write_text(md, encoding="utf-8", newline="\n")
    print(f"gravado: {SAIDA_JSON.name} e {SAIDA_MD.name}: {len(dado['cruzada']['pareados'])} pareamento(s) da cruzada, "
          f"{len(dado['pontes'])} ponte(s), {len(dado['ineditos']['agrupado'])} linha(s) de oficiais + inéditos")


if __name__ == "__main__":
    main()
