#!/usr/bin/env python3
# ! Alteração de IA - Revisar: arquivo novo (26/10/2026, Fase 4, pacote P2): a avaliação da corrida 17 (reprodução na
# tela), no molde de analisar_fase3b.py e pre_fase4.py: lê `reproducao.jsonl` e `fora.json` da pasta da corrida,
# resume por classe, por nível e por modo (quantos casos a tela reproduz, regra R1), o custo de um cenário em segundos
# e os tamanhos (árvore antes e depois, corpo, caso ao vivo), e grava `resultados_alvo/fase4/reproducibilidade.{json,md}`
# com os blocos `tb_f4_reproducao_*`, com `--check` e `--colar` como os outros avaliadores.
# ! Motivo: nenhum número do relatório da Fase 4 é digitado à mão (regra do projeto); o que a corrida 17 mede entra
# no roadmap, no relatório da fase e no painel por estes blocos, com a origem de cada número no JSON.
# ! Alteração de IA - Revisar: (27/10/2026, pacote P3) as leituras da corrida 16 (`--calibracao`: acerto e acurácia
# balanceada por k, AUROC da probabilidade do rótulo e da conjunta nos 90 com intervalo por reamostragem dos casos,
# revisão humana por parcela, curva risco-cobertura, regra R8, limiares do selo, ponte R6 e sondagem dos logprobs; grava
# `calibracao.{json,md}` e `limiares.json`) e da corrida 18 (`--tela`: acerto na tela e no fixture, concordância, regra
# R2 com b e c, selos, gatilhos, divergências, tempos, tamanho da trilha e o prompt contra o maior da calibração; grava
# `tela.{json,md}`), mais `--pontes` (regrava `pontes.json` a partir das pontes já rodadas) e `--pasta` (corrida parcial
# grava os derivados na própria pasta, nunca em resultados_alvo/fase4). As funções de probabilidade são as de
# analisar_confianca.py e de diagnostico_ao_vivo.py; as de pareamento, as de analisar_fase3b.py.
# ! Motivo: plano aprovado, P3 ("Mede": acerto na tela contra o gabarito, concordância tela × texto, custo por caso,
# AUROC nos 90 e os limiares) e regras R2, R6, R7 e R8; o gabarito só entra aqui, nunca no executor.
# ! Alteração de IA - Revisar: (01/11/2026, pacote P4) a leitura da corrida 19 (`--cura`): aplica a regra R3 (uma cura só
# conta quando a conferência final do roteiro passa na reexecução; "mesmo elemento do alvo original" separado de "outro
# elemento que fez o roteiro passar") e grava a taxa de cura por modo de quebra, por roteiro e por forma (harness contra
# a variante do PHP, com a árvore da página quebrada comparada célula a célula), o tempo da detecção à reexecução
# validada (MTTR), o que cada estratégia de candidato rendeu e em que verificação foi recusada, os casos "outro elemento"
# e os não curados, em `cura.{json,md}` (blocos `tb_f4_cura_*`).
# ! Motivo: plano aprovado, P4 ("Mede": a primeira medida de MTTR só do agente, a taxa de cura e onde a geração em código
# falha) e regra R3; decisão 80 (as duas formas comparadas pelo relatório).
# ! Alteração de IA - Revisar: (03/11/2026, pacote P5) a leitura da corrida 20 (`--biblioteca`): quantos casos de aprendizado
# vieram da tela e do fixture, o acerto do diagnóstico, quantas propostas cada filtro barrou (os 13 da decisão 65 e o validador
# da Fase 3), o lote (edições, peso, para revisão humana), a regra R5 (b e c na reavaliação dos 36 inéditos contra a base), a
# regra R4 (precisão e revocação da marca corrigido contra o conjunto desligado), a sonda de 28/09 repetida com a recuperação
# por id (caso a caso contra a leitura de 28/09) e a recuperação dos verbetes aprendidos (ficha 32), em `biblioteca.{json,md}`
# (blocos `tb_f4_biblioteca_*`). O gabarito dos inéditos entra aqui, nunca no executor.
# ! Motivo: plano aprovado, P5 ("Mede": quantas propostas cada filtro barra, se um lote melhora os inéditos, a precisão do
# ciclo de correção em código, o que o modelo propõe quando recebe as notas do próprio caso) e regras R4 e R5.
"""Uso (em Programacao/AgenteCore/experimentos):
  RESULTADOS_DIR=resultados_alvo python avaliar_fase4.py --biblioteca --saida fase4_biblioteca [--check] [--colar] [--pasta ...]
  RESULTADOS_DIR=resultados_alvo python avaliar_fase4.py --reproducao --saida fase4_reproducao [--check] [--colar]
  RESULTADOS_DIR=resultados_alvo python avaliar_fase4.py --cura --saida fase4_cura [--check] [--colar] [--pasta ...]
  RESULTADOS_DIR=resultados_alvo python avaliar_fase4.py --reproducao --saida fase4_reproducao_ineditos --nome reproducibilidade_ineditos --titulo "..." [--check]
  RESULTADOS_DIR=resultados_alvo python avaliar_fase4.py --calibracao --saida fase4_calibracao [--check] [--colar] [--pasta ...]
  RESULTADOS_DIR=resultados_alvo python avaliar_fase4.py --tela --saida fase4_tela [--check] [--colar] [--pasta ...]
  RESULTADOS_DIR=resultados_alvo python avaliar_fase4.py --pontes [--check]"""
from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

import analisar_confianca as conf
import analisar_fase3b as a3b
import avaliar
import avaliar_fase3
import caminhos
import cenarios_fase4 as cen
import cura_seletor as cs
import diagnostico_ao_vivo as dv
import executar_bateria
import executar_fase3
import executar_fase4 as ex
import pre_fase4 as pf
import sonda_confianca as sc
import trilha as tr

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass

NOME = "reproducibilidade"
PREFIXO = "tb_f4_reproducao_"
# ! Alteração de IA - Revisar: (27/10/2026) título do relatório em constante e `render(dado, titulo)`; `--nome` e
# `--titulo` na linha de comando, para a corrida sobre os 36 inéditos da ficha 27 sair em arquivos próprios
# (`reproducibilidade_ineditos.{json,md}`) com o título certo; `--colar` só com o nome padrão.
# ! Motivo: `pf.fechar` grava pelo nome e os blocos têm o mesmo prefixo nas duas corridas; sem nome próprio a
# segunda avaliação apagaria a leitura da corrida 17, e colar os blocos dos inéditos no relatório trocaria os da 17.
TITULO = "Reprodução dos casos na tela (corrida 17)"
NOME_CALIBRACAO, PREFIXO_CALIBRACAO = "calibracao", "tb_f4_calibracao_"
TITULO_CALIBRACAO = "Calibração e ponte da Fase 4 (corrida 16)"
NOME_TELA, PREFIXO_TELA = "tela", "tb_f4_tela_"
TITULO_TELA = "Diagnóstico ao vivo e o mesmo caso do fixture (corrida 18)"
LIMITE_R2 = 3   # regra R2: a variação entre corridas iguais (0 a 3 casos em 36, relatório da Fase 3-B)
NOME_CURA, PREFIXO_CURA = "cura", "tb_f4_cura_"
TITULO_CURA = "Cura de seletor (corrida 19)"
NOME_BIBLIOTECA = "biblioteca"
PREFIXO_BIBLIOTECA = "tb_f4_biblioteca_"
TITULO_BIBLIOTECA = "Biblioteca em produção e ciclo de correção (corrida 20)"
RELATORIO = caminhos.AQUI.parent.parent.parent / "Documentacao" / "memorial" / "3-resultados-e-analises" / "fase-4-relatorio.md"


def pasta_fase4() -> Path:
    return caminhos.RESULTADOS / "fase4"


def ler(saida: str) -> tuple[list[dict], list[dict]]:
    raiz = caminhos.fase3(saida)["raiz"]
    arq = raiz / "reproducao.jsonl"
    registros = [json.loads(l) for l in arq.read_text(encoding="utf-8").splitlines() if l.strip()] if arq.exists() else []
    arq_fora = raiz / "fora.json"
    fora = json.loads(arq_fora.read_text(encoding="utf-8")) if arq_fora.exists() else []
    return registros, fora


def _pct(parte: int, total: int) -> float | None:
    return round(100 * parte / total, 1) if total else None


def _mediana(valores: list) -> float | None:
    v = [x for x in valores if isinstance(x, (int, float))]
    return round(statistics.median(v), 3) if v else None


def _json(caminho: Path) -> dict | None:
    return json.loads(caminho.read_text(encoding="utf-8")) if caminho.exists() else None


def resumir(registros: list[dict], fora: list[dict], gerado_em: str | None = None, corrida: str | None = None) -> dict:
    """O resumo da reprodução: totais, por classe, por nível, por modo, tempo por cenário e tamanhos."""
    na_tela = len(registros)
    reproduzem = sum(1 for r in registros if r.get("reproduz"))
    casos = na_tela + len(fora)
    classes = sorted({int(r["classe"]) for r in registros} | {int(f["classe"]) for f in fora})
    niveis = sorted({int(r["nivel"]) for r in registros} | {int(f["nivel"]) for f in fora})

    def linha(chave: str, valor: int) -> dict:
        dentro = [r for r in registros if int(r[chave]) == valor]
        de_fora = [f for f in fora if int(f[chave]) == valor]
        rep = sum(1 for r in dentro if r.get("reproduz"))
        return {chave: valor, "casos": len(dentro) + len(de_fora), "na_tela": len(dentro), "reproduzem": rep, "fora": len(de_fora),
                "reproduzem_pct": _pct(rep, len(dentro) + len(de_fora))}

    modos = Counter(r["modo"] for r in registros)
    por_modo = [{"modo": m, "casos": n, "reproduzem": sum(1 for r in registros if r["modo"] == m and r.get("reproduz")),
                 "motivos": sorted({r["motivo"] for r in registros if r["modo"] == m})} for m, n in sorted(modos.items())]
    motivos_fora = Counter(f["motivo"].split(":")[0] for f in fora)
    return {"metadados": {"gerado_em": gerado_em or datetime.now().isoformat(timespec="seconds"), "corrida": corrida,
                          "fonte": "reproducao.jsonl e fora.json gravados por executar_fase4.py --modo reproducao"},
            "resumo": {"casos": casos, "na_tela": na_tela, "reproduzem": reproduzem, "fora": len(fora),
                       "reproduzem_pct": _pct(reproduzem, casos), "reproduzem_dos_na_tela_pct": _pct(reproduzem, na_tela),
                       "roteiro_falhou": sum(1 for r in registros if not r.get("passou_o_roteiro", True)),
                       "com_erro": sum(1 for r in registros if r.get("erro"))},
            "por_classe": [linha("classe", c) for c in classes],
            "por_nivel": [linha("nivel", n) for n in niveis],
            "por_modo": por_modo,
            "fora_por_motivo": [{"motivo": m, "casos": n} for m, n in sorted(motivos_fora.items())],
            "tempo": {"mediana_s": _mediana([r.get("segundos") for r in registros]), "max_s": max([r.get("segundos") or 0 for r in registros], default=None),
                      "soma_s": round(sum(r.get("segundos") or 0 for r in registros), 1), "tempo_api_mediana_ms": _mediana([r.get("tempo_ms") for r in registros])},
            "tamanhos": {"arvore_antes_mediana": _mediana([r.get("arvore_antes") for r in registros]),
                         "arvore_depois_mediana": _mediana([r.get("arvore_depois") for r in registros]),
                         "corpo_chars_mediana": _mediana([r.get("corpo_chars") for r in registros]),
                         "caso_chars_mediana": _mediana([r.get("caso_chars") for r in registros])},
            "casos": [{k: r.get(k) for k in ("id", "classe", "nivel", "causa", "modo", "campo", "cenario", "reproduz", "motivo", "status",
                                               "tempo_ms", "segundos", "arvore_antes", "arvore_depois", "corpo_chars", "caso_chars", "erro")} for r in registros],
            "fora": fora}


def render(dado: dict, titulo: str = TITULO) -> str:
    f = a3b.f
    r = dado["resumo"]

    def n(v) -> str:
        return "não medido" if v is None else (f(v) if isinstance(v, float) else str(v))

    blocos = [
        a3b.tab("tb_f4_reproducao_resumo", ["Casos de avaliação", "Com tela e modo", "Reproduzem na tela", "Fora (sem tela, sem modo ou pelo harness)",
                                            "Reproduzem (% dos casos)", "Reproduzem (% dos com tela)", "Roteiro falhou", "Com erro do harness"],
                [[str(r["casos"]), str(r["na_tela"]), str(r["reproduzem"]), str(r["fora"]), n(r["reproduzem_pct"]), n(r["reproduzem_dos_na_tela_pct"]),
                  str(r["roteiro_falhou"]), str(r["com_erro"])]]),
        a3b.tab("tb_f4_reproducao_por_classe", ["Classe", "Casos", "Com tela e modo", "Reproduzem", "Fora", "Reproduzem (%)"],
                [[str(x["classe"]), str(x["casos"]), str(x["na_tela"]), str(x["reproduzem"]), str(x["fora"]), n(x["reproduzem_pct"])] for x in dado["por_classe"]]),
        a3b.tab("tb_f4_reproducao_por_nivel", ["Nível", "Casos", "Com tela e modo", "Reproduzem", "Fora", "Reproduzem (%)"],
                [[str(x["nivel"]), str(x["casos"]), str(x["na_tela"]), str(x["reproduzem"]), str(x["fora"]), n(x["reproduzem_pct"])] for x in dado["por_nivel"]]),
        a3b.tab("tb_f4_reproducao_por_modo", ["Modo de injeção", "Casos", "Reproduzem", "Motivos registrados"],
                [[f"`{x['modo']}`", str(x["casos"]), str(x["reproduzem"]), "; ".join(x["motivos"])] for x in dado["por_modo"]]),
        a3b.tab("tb_f4_reproducao_custo", ["Tempo por cenário (mediana, s)", "Tempo por cenário (máximo, s)", "Tempo total dos cenários (s)",
                                           "Tempo da chamada à API (mediana, ms)", "Árvore antes da poda (mediana, nós)", "Árvore depois (mediana, linhas)",
                                           "Corpo HTTP (mediana, caracteres)", "Caso ao vivo (mediana, caracteres)"],
                [[n(dado["tempo"]["mediana_s"]), n(dado["tempo"]["max_s"]), n(dado["tempo"]["soma_s"]), n(dado["tempo"]["tempo_api_mediana_ms"]),
                  n(dado["tamanhos"]["arvore_antes_mediana"]), n(dado["tamanhos"]["arvore_depois_mediana"]), n(dado["tamanhos"]["corpo_chars_mediana"]),
                  n(dado["tamanhos"]["caso_chars_mediana"])]]),
        a3b.tab("tb_f4_reproducao_casos", ["Caso", "Classe", "Nível", "Causa", "Modo", "Campo", "Cenário", "Reproduz", "Motivo", "Status", "Segundos"],
                [[f"`{c['id']}`", str(c["classe"]), str(c["nivel"]), f"`{c['causa']}`", f"`{c['modo']}`", f"`{c['campo']}`" if c.get("campo") else "",
                  c["cenario"], "sim" if c["reproduz"] else "não", c["motivo"], n(c.get("status")), n(c.get("segundos"))] for c in dado["casos"]]),
        a3b.tab("tb_f4_reproducao_fora", ["Caso", "Classe", "Nível", "Causa", "Por que ficou fora"],
                [[f"`{x['id']}`", str(x["classe"]), str(x["nivel"]), f"`{x['causa']}`", x["motivo"]] for x in dado["fora"]]),
    ]
    cab = pf.cabecalho(titulo, "avaliar_fase4.py", "reproducao.jsonl e fora.json da corrida",
                       dado["metadados"]["gerado_em"][:10])
    cab += ["", "Um caso reproduz na tela quando a chamada à CobaiaAPI sai do normal (status, corpo, contrato ou tempo acima do orçamento) "
                "ou quando uma conferência do roteiro falha (regra R1 do plano aprovado). Os casos fora são os de rota sem página "
                "(pedidos), os de causa sem modo de injeção e os de quebra de localizador, que o harness arma (ficha 29).", ""]
    return "\n".join(cab) + "\n\n" + "\n\n".join(blocos) + "\n"


# ------------------------------------------------------------------ corrida 16: calibração e ponte

def _n(v) -> str:
    return "não medido" if v is None else (a3b.f(v) if isinstance(v, float) else str(v))


def _sim(v) -> str:
    return {True: "sim", False: "não"}.get(v, "n/d")


def _ic(s: dict | None) -> str:
    if not s or s.get("auroc") is None:
        return "n/d"
    ic = s.get("ic95")
    return a3b.f(s["auroc"], 3) + (f" [{a3b.f(ic[0], 3)}; {a3b.f(ic[1], 3)}]" if ic else "")


def _linhas_de(registros: list[dict], laterais: list[dict]) -> list[dict]:
    """Uma linha por diagnóstico: o rótulo lido, o acerto contra o gabarito (só aqui o gabarito entra) e a
    probabilidade do rótulo lida nos tokens da linha lateral, pela leitura de diagnostico_ao_vivo.confianca_do_rotulo."""
    lat = {l["caso"]: l for l in laterais}
    linhas = []
    for r in registros:
        tokens = sc.expandir(lat[r["caso"]]["logprobs"]) if r["caso"] in lat else []
        c = dv.confianca_do_rotulo(tokens) if tokens else None
        lido = avaliar.extrair(r.get("resposta", ""))["causa_raiz"]
        gab = (r.get("gabarito") or {}).get("causa_raiz")
        acerto = lido is not None and gab is not None and avaliar._normalizar(lido) == avaliar._normalizar(gab)
        linhas.append({"caso": r["caso"], "classe": r.get("classe"), "particao": r.get("particao"), "gabarito": gab, "rotulo": lido, "acerto": acerto,
                       "p": c["p_rotulo"] if c else None, "p_conjunta": c["p_conjunta"] if c else None, "margem": c["margem"] if c else None,
                       "segunda": c["segunda"]["opcao"] if c and c["segunda"] else None, "segundos": r.get("segundos"),
                       "tokens_entrada": r.get("tokens_entrada"), "k": r.get("k")})
    return linhas


def _medida_de_k(k: int, linhas: list[dict], esperado: int | None = None) -> dict:
    """O que a calibração mede para um k: acerto, acurácia balanceada (avaliar_fase3), custo, AUROC dos dois sinais
    com intervalo por reamostragem dos casos, revisão por parcela e a curva risco-cobertura (analisar_confianca).
    `completo` diz se o k cobriu todos os casos pedidos (um k interrompido não entra na regra R8 nem nos limiares)."""
    n = len(linhas)
    acertos = sum(1 for l in linhas if l["acerto"])
    pares = [(l["gabarito"], l["rotulo"]) for l in linhas if l["gabarito"]]
    validas = [l for l in linhas if isinstance(l["p"], (int, float))]
    notas = [l["p"] for l in validas]
    acs = [l["acerto"] for l in validas]
    grupos = [l["caso"] for l in validas]
    por_particao = {}
    for p in ("avaliacao", "aprendizado"):
        sub = [l for l in linhas if l.get("particao") == p]
        if sub:
            por_particao[p] = {"n": len(sub), "acertos": sum(1 for l in sub if l["acerto"]), "acerto_pct": _pct(sum(1 for l in sub if l["acerto"]), len(sub))}
    certos = [l["p"] for l in validas if l["acerto"]]
    errados = [l["p"] for l in validas if not l["acerto"]]
    return {"k": k, "n": n, "casos_esperados": esperado, "completo": esperado is None or n == esperado,
            "acertos": acertos, "acerto_pct": _pct(acertos, n),
            "acuracia_balanceada_pct": avaliar_fase3.acuracia_balanceada(pares) if pares else None,
            "sem_rotulo": sum(1 for l in linhas if l["rotulo"] is None), "sem_probabilidade": n - len(validas),
            "segundos_mediana": _mediana([l["segundos"] for l in linhas]), "tokens_entrada_mediana": _mediana([l["tokens_entrada"] for l in linhas]),
            "tokens_entrada_max": max([l["tokens_entrada"] for l in linhas if isinstance(l["tokens_entrada"], (int, float))], default=None),
            "sinais": {"p_rotulo": conf.auroc_com_intervalo(notas, acs, grupos) if validas else None,
                       "p_conjunta": conf.auroc_com_intervalo([l["p_conjunta"] for l in validas], acs, grupos) if validas else None},
            "revisao": [{"fracao": f, **conf.revisao(notas, acs, f)} for f in conf.FRACOES_DE_REVISAO] if validas else [],
            "curva": conf.risco_por_cobertura(notas, acs) if validas else [],
            "por_particao": por_particao, "p_mediana_certos": _mediana(certos), "p_mediana_errados": _mediana(errados), "casos": linhas}


def resumir_calibracao(bruto: dict, gerado_em: str | None = None, corrida: str | None = None) -> dict:
    """A leitura da corrida 16: as medidas por k, a regra R8 (k escolhido), os limiares do selo (regra R7) pelo k
    escolhido, a ponte (regra R6) e a sondagem dos logprobs."""
    cond = bruto.get("condicoes") or {}
    esperado = cond.get("casos")
    por_k = {}
    for k in sorted(bruto.get("k", {})):
        dados = bruto["k"][k]
        por_k[int(k)] = _medida_de_k(int(k), _linhas_de(dados["registros"], dados["laterais"]), esperado)
    # a regra R8 e os limiares só olham os k que cobriram todos os casos (um k interrompido entraria com acurácia
    # sobre menos casos); o k dos limiares é o k escolhido, para a tela ler um só
    validos = {k: m for k, m in por_k.items() if m["completo"]}
    med3, med5 = validos.get(3), validos.get(5)
    par = None
    if med3 and med5:
        def celula(m: dict) -> dict:
            return {l["caso"]: {"causa_correta": l["acerto"], "causa_respondida": l["rotulo"]} for l in m["casos"]}
        par = a3b.parear(celula(med5), celula(med3))
    r8 = {**ex.regra_r8(med3, med5, par), "par": par}
    escolhido = validos.get(r8["k"]) or (validos[min(validos)] if validos else (por_k[min(por_k)] if por_k else None))
    limiares = None
    if escolhido:
        limiares = dv.calcular_limiares([{"caso": l["caso"], "p": l["p"], "acerto": l["acerto"]} for l in escolhido["casos"]],
                                        parcela=dv.PARCELA_BAIXA, k=escolhido["k"], origem=f"{corrida}/k{escolhido['k']}")
    k_escolhido = escolhido["k"] if escolhido else r8["k"]
    # ! Alteração de IA - Revisar: (28/10/2026, leitura da corrida 16) a leitura ganha `por_selo`: quantos casos e quantos
    # erros caem em cada selo (baixo, medio, alto) com os limiares desta corrida, e os ids dos casos errados de cada selo.
    # ! Motivo: a tabela de revisão só mostra a parcela baixa; os erros que saem com selo alto (probabilidade acima da
    # mediana dos acertos) são o número que o roadmap e o painel precisam citar, e não podiam ser contados à mão.
    por_selo = None
    if escolhido and limiares:
        por_selo = []
        for nome in ("baixo", "medio", "alto"):
            sub = [l for l in escolhido["casos"] if dv.selo(l["p"], limiares) == nome]
            errados = sorted(l["caso"] for l in sub if not l["acerto"])
            por_selo.append({"selo": nome, "casos": len(sub), "certos": len(sub) - len(errados), "errados": len(errados),
                             "erro_pct": _pct(len(errados), len(sub)) if sub else None, "casos_errados": errados})
    sondagem = None
    son = bruto.get("sondagem")
    if son:
        ok, mensagens = dv.sondagem_aceita(son)
        c = son["conferencias"]
        sondagem = {"ok": ok, "mensagens": mensagens, "temperatura": c["temperatura"].get("veredito"), "razao": c["temperatura"].get("razao"),
                    "tokens_com_logprob": c["a"].get("tokens_com_logprob"), "top_por_posicao_max": c["a"].get("top_por_posicao_max"),
                    "tem_bytes": c["a"].get("tem_bytes"), "texto_bate": c["a"].get("texto_bate"),
                    "tokens_que_partem_caractere": c["a"].get("tokens_que_partem_caractere"),
                    "resposta_igual_sem_logprobs": c.get("resposta_igual_sem_logprobs"), "rotulo_lido": c.get("rotulo_lido"), "p_rotulo": c.get("p_rotulo"),
                    "versao_ollama": son.get("metadados", {}).get("versao_ollama"), "modelo": son.get("metadados", {}).get("modelo"),
                    "caso": son.get("metadados", {}).get("caso")}
    return {"metadados": {"gerado_em": gerado_em or datetime.now().isoformat(timespec="seconds"), "corrida": corrida,
                          "fonte": "k<n>/<modelo>/diagnosticos__L100.jsonl e logprobs__L100.jsonl, sondagem_logprobs.json, ponte/ e pontes.json da corrida",
                          "modelo": cond.get("modelo"), "versao_ollama": cond.get("versao_ollama"), "parcial": bool(cond.get("parcial"))},
            "por_k": [por_k[k] for k in sorted(por_k)], "r8": r8, "k_escolhido": k_escolhido, "limiares": limiares, "por_selo": por_selo,
            "ponte": bruto.get("ponte"), "sondagem": sondagem,
            "condicoes": {k: cond.get(k) for k in ("modelo", "versao_ollama", "k", "casos", "casos_da_ponte", "parcial", "biblioteca", "top_logprobs",
                                                   "teto_tokens", "leitura_da_probabilidade", "parcela_baixa", "ponte_necessaria")}}


def render_calibracao(dado: dict) -> str:
    lim = dado.get("limiares") or {}
    p = dado.get("ponte") or {}
    s = dado.get("sondagem") or {}
    r8 = dado["r8"]
    par = r8.get("par") or {}
    blocos = [
        a3b.tab("tb_f4_calibracao_resumo", ["Ollama", "Modelo", "Casos", "k medidos", "k escolhido (R8)", "Selo baixo até (p)", "Selo alto a partir de (p)",
                                            "Ponte pareável (R6)", "Sondagem dos logprobs"],
                [[_n(dado["metadados"].get("versao_ollama")), f"`{dado['metadados'].get('modelo')}`", _n(max([x["n"] for x in dado["por_k"]], default=0)),
                  ", ".join(str(x["k"]) for x in dado["por_k"]) or "nenhum", str(dado["k_escolhido"]), _n(lim.get("baixo_ate")), _n(lim.get("alto_a_partir_de")),
                  _sim(p.get("pareavel")) if p else "n/d", ("ok" if s.get("ok") else "problema") if s else "não rodou"]]),
        a3b.tab("tb_f4_calibracao_por_k", ["k", "Casos", "Completo", "Acertos", "Acerto (%)", "Acurácia balanceada (%)", "Nos 36 de avaliação (%)", "Nos 54 de aprendizado (%)",
                                           "s por diagnóstico (mediana)", "Tokens de entrada (mediana)", "Tokens de entrada (máximo)",
                                           "AUROC p do rótulo [IC 95%]", "AUROC p conjunta [IC 95%]", "Sem rótulo"],
                [[str(x["k"]), str(x["n"]), _sim(x["completo"]), str(x["acertos"]), _n(x["acerto_pct"]), _n(x["acuracia_balanceada_pct"]),
                  _n((x["por_particao"].get("avaliacao") or {}).get("acerto_pct")), _n((x["por_particao"].get("aprendizado") or {}).get("acerto_pct")),
                  _n(x["segundos_mediana"]), _n(x["tokens_entrada_mediana"]), _n(x["tokens_entrada_max"]),
                  _ic(x["sinais"].get("p_rotulo")), _ic(x["sinais"].get("p_conjunta")), str(x["sem_rotulo"])] for x in dado["por_k"]]),
        a3b.tab("tb_f4_calibracao_revisao", ["k", "Parcela revisada", "Casos revisados", "Erros pegos", "Acertos revisados à toa", "Risco no que sobra"],
                [[str(x["k"]), a3b.f(100 * rv["fracao"], 0) + "%", str(rv["revisados"]), f"{rv['erros_pegos']} de {rv['erros']}", str(rv["acertos_revisados"]),
                  "n/d" if rv["risco_no_que_sobra"] is None else a3b.f(100 * rv["risco_no_que_sobra"], 1) + "%"] for x in dado["por_k"] for rv in x["revisao"]]),
        # ! Alteração de IA - Revisar: (28/10/2026) bloco `tb_f4_calibracao_selos`, os casos e os erros por selo do k escolhido.
        # ! Motivo: é a origem citável dos "erros com selo alto" no roadmap e no painel (sem limiares, uma linha "sem limiares").
        a3b.tab("tb_f4_calibracao_selos", ["Selo", "Casos", "Certos", "Errados", "Erro (%)", "Casos errados"],
                [[x["selo"], str(x["casos"]), str(x["certos"]), str(x["errados"]), _n(x["erro_pct"]), ", ".join(f"`{c}`" for c in x["casos_errados"]) or "nenhum"]
                 for x in dado.get("por_selo") or []] or [["sem limiares"] + [""] * 5]),
        a3b.tab("tb_f4_calibracao_r8", ["Acurácia balanceada k = 3 (%)", "Acurácia balanceada k = 5 (%)", "b (só k = 5 acerta)", "c (só k = 3 acerta)",
                                        "p (McNemar exato)", "k escolhido", "Motivo"],
                [[_n(next((x["acuracia_balanceada_pct"] for x in dado["por_k"] if x["k"] == 3), None)),
                  _n(next((x["acuracia_balanceada_pct"] for x in dado["por_k"] if x["k"] == 5), None)),
                  _n(par.get("b")), _n(par.get("c")), _n(par.get("p_mcnemar")), str(r8["k"]), r8["motivo"]]]),
        a3b.tab("tb_f4_calibracao_ponte", ["Ollama", "Corrida da ponte", "Feita nesta corrida", "Casos pareados", "b (só a ponte acerta)", "c (só a Fase 3 acerta)",
                                           "Pareável (b + c até o limite)", "Casos de texto corrigido fora da conta"],
                [[_n(p.get("versao")), _n(p.get("corrida")), _sim(p.get("feita_nesta_corrida")), _n(p.get("n")), _n(p.get("b")), _n(p.get("c")),
                  f"{_sim(p.get('pareavel'))} (limite {p.get('limite')})" if p else "n/d", ", ".join(p.get("casos_de_texto_alterado") or []) or "nenhum"]]),
        a3b.tab("tb_f4_calibracao_sondagem", ["Ollama", "Tokens com probabilidade", "Alternativas por posição (máx.)", "Bytes por token", "Texto remontado bate",
                                              "Probabilidade antes ou depois da temperatura", "Resposta igual sem logprobs", "Rótulo lido", "p do rótulo", "Avisos"],
                [[_n(s.get("versao_ollama")), _n(s.get("tokens_com_logprob")), _n(s.get("top_por_posicao_max")), _sim(s.get("tem_bytes")), _sim(s.get("texto_bate")),
                  _n(s.get("temperatura")), _sim(s.get("resposta_igual_sem_logprobs")), _n(s.get("rotulo_lido")), _n(s.get("p_rotulo")),
                  "; ".join(s.get("mensagens") or []) or "nenhum"]] if s else [["não rodou"] + [""] * 9]),
    ]
    escolhido = next((x for x in dado["por_k"] if x["k"] == dado["k_escolhido"]), dado["por_k"][0] if dado["por_k"] else None)
    linhas = []
    if escolhido:
        for l in sorted(escolhido["casos"], key=lambda l: (l["p"] is None, l["p"] or 0, l["caso"])):
            linhas.append([f"`{l['caso']}`", _n(l.get("particao")), f"`{l['gabarito']}`", f"`{l['rotulo']}`", "certo" if l["acerto"] else "errado",
                           _n(l["p"]), _n(l["p_conjunta"]), _n(l.get("segunda")), _n(dv.selo(l["p"], lim) if lim else None)])
    blocos.append(a3b.tab("tb_f4_calibracao_casos", ["Caso", "Partição", "Gabarito", "Rótulo", "Resultado", "p do rótulo", "p conjunta", "Segunda causa", "Selo"], linhas))
    cab = pf.cabecalho(TITULO_CALIBRACAO, "avaliar_fase4.py", "os registros, as linhas laterais, a sondagem e a ponte da corrida 16",
                       dado["metadados"]["gerado_em"][:10])
    cab += ["", f"A probabilidade do rótulo é lida no primeiro token depois de CAUSA_RAIZ: (especificação da trilha, seção 14); a conjunta é a medida "
                f"da corrida 12. O selo segue a ficha 31 (a): baixo é a parcela de {a3b.f(100 * dv.PARCELA_BAIXA, 0)}% de menor probabilidade (gatilho de "
                "intervenção e de revisão humana), alto fica acima da mediana dos acertos, médio entre os dois (regra R7). A regra R8 escolhe o k; a "
                "regra R6 confere a ponte de versão contra a Fase 3 (decisão 47)."
                + (" Corrida PARCIAL: os números abaixo não valem como calibração." if dado["metadados"].get("parcial") else ""), ""]
    return "\n".join(cab) + "\n\n" + "\n\n".join(blocos) + "\n"


def ler_calibracao(saida: str) -> dict:
    """O bruto da corrida 16 na pasta da corrida: por k, os registros e as linhas laterais; a sondagem; a ponte (feita
    nesta corrida, ou a registrada em pontes.json para a versão); as condições."""
    raiz = caminhos.fase3(saida)["raiz"]
    cond = _json(raiz / "condicoes_fase4.json") or {}
    modelo = cond.get("modelo") or ex.MODELO_PADRAO
    slug = executar_fase3._slug(modelo)
    ks: dict = {}
    for pasta in sorted(raiz.glob("k*")):
        if not pasta.is_dir() or not pasta.name[1:].isdigit():
            continue
        registros = executar_bateria.ler_jsonl(pasta / slug / f"diagnosticos__L{dv.VERSAO_CURADA}.jsonl")
        if registros:
            ks[int(pasta.name[1:])] = {"registros": registros, "laterais": executar_bateria.ler_jsonl(pasta / slug / f"logprobs__L{dv.VERSAO_CURADA}.jsonl")}
    ponte = None
    arq_ponte = raiz / "ponte" / slug / "diagnosticos__L0.jsonl"
    if arq_ponte.exists():
        base = executar_bateria.ler_jsonl(caminhos.fase3("fase3")["raiz"] / slug / "diagnosticos__L0.jsonl")
        novos = executar_bateria.ler_jsonl(arq_ponte)
        ponte = {"versao": cond.get("versao_ollama"), "corrida": f"{saida}/ponte", "modelo": modelo, "feita_nesta_corrida": True,
                 "completa": ex.ponte_completa(novos, {"parcial": cond.get("parcial")}), **ex.ponte_contra_fase3(novos, base)}
    elif cond.get("versao_ollama"):
        anterior = ex.ultima_ponte(_json(ex.caminho_das_pontes()), cond["versao_ollama"])
        ponte = {**anterior, "feita_nesta_corrida": False} if anterior else None
    return {"k": ks, "sondagem": _json(raiz / "sondagem_logprobs.json"), "ponte": ponte, "condicoes": cond}


# ------------------------------------------------------------------ corrida 18: a tela contra o fixture (regra R2)

def _leitura_do_caso_ao_vivo(entrada: dict | None) -> dict:
    """O que o caso ao vivo levou ao modelo, lido da entrada gravada na trilha: o começo do CORPO, quantas diferenças
    a poda achou contra o contrato (da OBSERVAÇÃO "corpo json, forma lista, N diferença(s) contra o contrato"), a forma
    do corpo e o começo do SINTOMA. Sem entrada (corrida antiga, teste), tudo None."""
    if not entrada:
        return {"corpo_tela": None, "diferencas_contra_contrato": None, "forma_do_corpo": None, "sintoma_tela": None}
    obs = str(entrada.get("observacao") or "")
    m = re.search(r"(\d+) diferen", obs)
    forma = re.search(r"forma (\w+)", obs)
    return {"corpo_tela": str(entrada.get("corpo") or "")[:80], "diferencas_contra_contrato": int(m.group(1)) if m else None,
            "forma_do_corpo": forma.group(1) if forma else None, "sintoma_tela": str(entrada.get("sintoma") or "")[:160]}


def resumir_tela(tela: list[dict], fixture: list[dict], casos: list[dict], por_caso: list[dict] | None = None, trilha_info: dict | None = None,
                 calibracao: dict | None = None, gerado_em: str | None = None, corrida: str | None = None, vivos: dict | None = None) -> dict:
    """A leitura da corrida 18: para cada caso diagnosticado na tela e no fixture, o acerto contra o gabarito (só aqui
    ele entra, pelo id do caso), a concordância entre os dois rótulos, a regra R2 (b = só a tela acerta, c = só o
    fixture; b + c até o limite), os selos, os gatilhos, as divergências, os tempos e o tamanho da trilha.
    `vivos` (id do caso para a entrada do caso ao vivo, da trilha) dá o bloco `corpo`: o que a poda deixou no CORPO."""
    gab = {c["id"]: c for c in casos}

    def base_id(x) -> str:
        return str(x).split("@")[0]

    t = {base_id(r["caso"]): r for r in tela}
    f = {base_id(r["caso"]): r for r in fixture}
    pc = {p["caso"]: p for p in por_caso or []}
    vv = {base_id(k): v for k, v in (vivos or {}).items()}
    linhas = []
    for i in [i for i in t if i in f and i in gab]:
        rt = avaliar.extrair(t[i].get("resposta", ""))["causa_raiz"]
        rf = avaliar.extrair(f[i].get("resposta", ""))["causa_raiz"]
        g = gab[i]["gabarito"]["causa_raiz"]
        at = rt is not None and avaliar._normalizar(rt) == avaliar._normalizar(g)
        af = rf is not None and avaliar._normalizar(rf) == avaliar._normalizar(g)
        p = pc.get(i, {})
        linhas.append({"caso": i, "classe": gab[i].get("classe"), "nivel": gab[i].get("nivel"), "gabarito": g, "rotulo_tela": rt, "rotulo_fixture": rf,
                       "acerto_tela": at, "acerto_fixture": af, "concordam": rt is not None and rf is not None and avaliar._normalizar(rt) == avaliar._normalizar(rf),
                       "reproduz": p.get("reproduz"), "p_tela": p.get("p_tela"), "p_fixture": p.get("p_fixture"), "selo_tela": p.get("selo_tela"),
                       "selo_fixture": p.get("selo_fixture"), "segundos_tela": p.get("segundos_tela", t[i].get("segundos")),
                       "segundos_fixture": p.get("segundos_fixture", f[i].get("segundos")), "gatilho_tela": bool((p.get("gatilhos_tela") or {}).get("algum")),
                       "intervencoes_tela": p.get("intervencoes_tela") or 0, "divergencia_tela": bool(p.get("divergencia_tela")),
                       "falha_tela": p.get("falha_tela"), "tokens_entrada_tela": t[i].get("tokens_entrada"), "tokens_entrada_fixture": f[i].get("tokens_entrada"),
                       **_leitura_do_caso_ao_vivo(vv.get(i))})
    # ! Alteração de IA - Revisar: (01/11/2026, leitura da corrida 18) a leitura ganha `rotulos` (quantas vezes cada causa
    # foi respondida na tela e no fixture, contra quantas vezes é o gabarito) e `corpo` (os casos em que a poda não achou
    # diferença contra o contrato e mostrou só o primeiro item da lista: quantos concordam, quantos viram
    # colecao_no_lugar_de_objeto na tela, quantos acertam; e os casos cujo sintoma por molde diz "Nenhuma diferença medida").
    # ! Motivo: na corrida 18 a discordância tela × fixture ficou longe do limite da regra R2 e o roadmap precisa dizer
    # por quê com número de script: o caso ao vivo só descreve diferenças de campo contra o contrato, e nas falhas de
    # lista (contagem, duplicado, codificação, escala, latência) ele leva ao modelo o primeiro produto normal.
    def contagem(campo: str) -> dict:
        c: dict = {}
        for l in linhas:
            chave = l.get(campo) or "sem rótulo"
            c[chave] = c.get(chave, 0) + 1
        return c

    ct, cf, cg = contagem("rotulo_tela"), contagem("rotulo_fixture"), contagem("gabarito")
    rotulos = [{"rotulo": x, "tela": ct.get(x, 0), "fixture": cf.get(x, 0), "gabarito": cg.get(x, 0)}
               for x in sorted(set(ct) | set(cf) | set(cg), key=lambda x: (-(ct.get(x, 0) + cf.get(x, 0) + cg.get(x, 0)), x))]
    sem_dif = [l for l in linhas if l["diferencas_contra_contrato"] == 0]
    com_dif = [l for l in linhas if (l["diferencas_contra_contrato"] or 0) > 0]
    corpo = {"casos_lidos": sum(1 for l in linhas if l["diferencas_contra_contrato"] is not None),
             "sem_diferenca_contra_contrato": len(sem_dif), "sem_diferenca_concordam": sum(1 for l in sem_dif if l["concordam"]),
             "sem_diferenca_acerto_tela": sum(1 for l in sem_dif if l["acerto_tela"]),
             "sem_diferenca_colecao_na_tela": sum(1 for l in sem_dif if l["rotulo_tela"] == "colecao_no_lugar_de_objeto"),
             "sem_diferenca_casos": sorted(l["caso"] for l in sem_dif),
             "com_diferenca_contra_contrato": len(com_dif), "com_diferenca_concordam": sum(1 for l in com_dif if l["concordam"]),
             "com_diferenca_acerto_tela": sum(1 for l in com_dif if l["acerto_tela"]),
             "sintoma_sem_medida": sum(1 for l in linhas if str(l["sintoma_tela"] or "").startswith("Nenhuma diferença medida")),
             "sintoma_sem_medida_casos": sorted(l["caso"] for l in linhas if str(l["sintoma_tela"] or "").startswith("Nenhuma diferença medida"))}
    par = a3b.parear({l["caso"]: {"causa_correta": l["acerto_tela"], "causa_respondida": l["rotulo_tela"]} for l in linhas},
                     {l["caso"]: {"causa_correta": l["acerto_fixture"], "causa_respondida": l["rotulo_fixture"]} for l in linhas})
    n = len(linhas)

    def selos(chave: str) -> dict:
        return {s: sum(1 for l in linhas if l[chave] == s) for s in ("alto", "medio", "baixo")}

    classes = sorted({l["classe"] for l in linhas if l["classe"] is not None})
    por_classe = []
    for c in classes:
        sub = [l for l in linhas if l["classe"] == c]
        por_classe.append({"classe": c, "casos": len(sub), "acerto_tela": sum(1 for l in sub if l["acerto_tela"]),
                           "acerto_fixture": sum(1 for l in sub if l["acerto_fixture"]), "concordam": sum(1 for l in sub if l["concordam"])})
    prompt = None
    if calibracao:
        medida = next((x for x in calibracao.get("por_k", []) if x["k"] == calibracao.get("k_escolhido")), None)
        maximo = (medida or {}).get("tokens_entrada_max")
        if maximo:
            limite = round(1.1 * maximo)
            acima = [l["caso"] for l in linhas if isinstance(l["tokens_entrada_tela"], (int, float)) and l["tokens_entrada_tela"] > limite]
            prompt = {"maximo_da_calibracao": maximo, "limite_mais_10_pct": limite, "acima": acima,
                      "maximo_da_tela": max([l["tokens_entrada_tela"] for l in linhas if isinstance(l["tokens_entrada_tela"], (int, float))], default=None)}
    resumo = {"casos": n, "reproduzem": sum(1 for l in linhas if l["reproduz"]), "acerto_tela": sum(1 for l in linhas if l["acerto_tela"]),
              "acerto_fixture": sum(1 for l in linhas if l["acerto_fixture"]), "concordam": sum(1 for l in linhas if l["concordam"]),
              "b": par["b"], "c": par["c"], "discordantes": par["b"] + par["c"], "limite_r2": LIMITE_R2, "dentro_do_limite_r2": par["b"] + par["c"] <= LIMITE_R2,
              "p_mcnemar": par["p_mcnemar"], "casos_que_mudaram": sorted(par["ganhos"] + par["perdas"]),
              "selos_tela": selos("selo_tela"), "selos_fixture": selos("selo_fixture"), "gatilhos_tela": sum(1 for l in linhas if l["gatilho_tela"]),
              "divergencias_tela": sum(1 for l in linhas if l["divergencia_tela"]), "intervencoes_tela": sum(l["intervencoes_tela"] for l in linhas),
              "segundos_tela_mediana": _mediana([l["segundos_tela"] for l in linhas]), "segundos_fixture_mediana": _mediana([l["segundos_fixture"] for l in linhas]),
              "p_tela_mediana": _mediana([l["p_tela"] for l in linhas]), "p_fixture_mediana": _mediana([l["p_fixture"] for l in linhas]),
              "trilha_bytes": (trilha_info or {}).get("bytes"), "trilha_eventos": (trilha_info or {}).get("eventos"),
              "trilha_blobs_externos": (trilha_info or {}).get("blobs_externos")}
    resumo["acerto_tela_pct"] = _pct(resumo["acerto_tela"], n)
    resumo["acerto_fixture_pct"] = _pct(resumo["acerto_fixture"], n)
    resumo["concordancia_pct"] = _pct(resumo["concordam"], n)
    return {"metadados": {"gerado_em": gerado_em or datetime.now().isoformat(timespec="seconds"), "corrida": corrida,
                          "fonte": "diagnosticos__tela.jsonl, diagnosticos__fixture.jsonl, tela.jsonl e trilha_tela.jsonl da corrida; gabarito dos bancos de casos"},
            "resumo": resumo, "por_classe": por_classe, "prompt_contra_calibracao": prompt, "rotulos": rotulos, "corpo": corpo, "casos": linhas}


def render_tela(dado: dict) -> str:
    r = dado["resumo"]
    pr = dado.get("prompt_contra_calibracao")
    cp = dado.get("corpo") or {}
    blocos = [
        a3b.tab("tb_f4_tela_resumo", ["Casos", "Reproduzem na tela", "Acerto na tela", "Acerto no fixture", "Concordam (mesmo rótulo)", "Concordância (%)",
                                      "b (só a tela acerta)", "c (só o fixture acerta)", "b + c", "Limite R2", "Dentro do limite", "p (McNemar exato)",
                                      "Selos na tela (alto / médio / baixo)", "Gatilhos na tela", "Divergências na tela", "s por caso na tela (mediana)",
                                      "s por caso no fixture (mediana)", "Trilha (bytes)"],
                [[str(r["casos"]), str(r["reproduzem"]), f"{r['acerto_tela']} ({_n(r['acerto_tela_pct'])}%)", f"{r['acerto_fixture']} ({_n(r['acerto_fixture_pct'])}%)",
                  str(r["concordam"]), _n(r["concordancia_pct"]), str(r["b"]), str(r["c"]), str(r["discordantes"]), str(r["limite_r2"]), _sim(r["dentro_do_limite_r2"]),
                  _n(r["p_mcnemar"]), f"{r['selos_tela']['alto']} / {r['selos_tela']['medio']} / {r['selos_tela']['baixo']}", str(r["gatilhos_tela"]),
                  str(r["divergencias_tela"]), _n(r["segundos_tela_mediana"]), _n(r["segundos_fixture_mediana"]), _n(r["trilha_bytes"])]]),
        a3b.tab("tb_f4_tela_por_classe", ["Classe", "Casos", "Acerto na tela", "Acerto no fixture", "Concordam"],
                [[str(x["classe"]), str(x["casos"]), str(x["acerto_tela"]), str(x["acerto_fixture"]), str(x["concordam"])] for x in dado["por_classe"]]),
        # ! Alteração de IA - Revisar: (01/11/2026) blocos `tb_f4_tela_rotulos` e `tb_f4_tela_corpo`, e as duas colunas finais
        # de `tb_f4_tela_casos` (diferenças contra o contrato e o começo do CORPO do caso ao vivo).
        # ! Motivo: são a origem citável de "o rótulo que a tela puxa" e de "a poda mostrou o primeiro item" no roadmap e no painel.
        a3b.tab("tb_f4_tela_rotulos", ["Rótulo", "Dado na tela", "Dado no fixture", "É o gabarito de"],
                [[f"`{x['rotulo']}`", str(x["tela"]), str(x["fixture"]), str(x["gabarito"])] for x in dado.get("rotulos") or []] or [["nenhum", "", "", ""]]),
        a3b.tab("tb_f4_tela_corpo", ["Casos com o caso ao vivo lido", "Sem diferença contra o contrato", "Desses, mesmo rótulo", "Desses, acerto na tela",
                                     "Desses, colecao_no_lugar_de_objeto na tela", "Com diferença contra o contrato", "Desses, mesmo rótulo", "Desses, acerto na tela",
                                     "Sintoma \"Nenhuma diferença medida\""],
                [[_n(cp.get("casos_lidos")), _n(cp.get("sem_diferenca_contra_contrato")), _n(cp.get("sem_diferenca_concordam")), _n(cp.get("sem_diferenca_acerto_tela")),
                  _n(cp.get("sem_diferenca_colecao_na_tela")), _n(cp.get("com_diferenca_contra_contrato")), _n(cp.get("com_diferenca_concordam")),
                  _n(cp.get("com_diferenca_acerto_tela")), _n(cp.get("sintoma_sem_medida"))]]),
        a3b.tab("tb_f4_tela_casos", ["Caso", "Classe", "Gabarito", "Rótulo na tela", "Rótulo no fixture", "Tela", "Fixture", "Concordam", "p tela", "Selo tela",
                                     "p fixture", "Selo fixture", "Gatilho", "Divergência", "s tela", "s fixture", "Diferenças contra o contrato", "CORPO do caso ao vivo (começo)"],
                [[f"`{l['caso']}`", str(l["classe"]), f"`{l['gabarito']}`", f"`{l['rotulo_tela']}`", f"`{l['rotulo_fixture']}`",
                  "certo" if l["acerto_tela"] else "errado", "certo" if l["acerto_fixture"] else "errado", _sim(l["concordam"]), _n(l["p_tela"]), _n(l["selo_tela"]),
                  _n(l["p_fixture"]), _n(l["selo_fixture"]), _sim(l["gatilho_tela"]), _sim(l["divergencia_tela"]), _n(l["segundos_tela"]), _n(l["segundos_fixture"]),
                  _n(l.get("diferencas_contra_contrato")), ("`" + str(l.get("corpo_tela") or "")[:60].replace("|", "¦").replace("`", "'") + "`") if l.get("corpo_tela") else "n/d"]
                 for l in dado["casos"]]),
    ]
    cab = pf.cabecalho(TITULO_TELA, "avaliar_fase4.py", "os registros da tela e do fixture, tela.jsonl e a trilha da corrida 18",
                       dado["metadados"]["gerado_em"][:10])
    cab += ["", f"Regra R2 do plano aprovado: nos casos que reproduzem, o rótulo dado ao caso lido da tela e o rótulo dado ao caso lido do fixture, na "
                f"mesma sessão do Ollama, diferem em no máximo {LIMITE_R2} casos (a variação entre corridas iguais); acima disso, o molde do sintoma e a "
                "poda são revistos antes da próxima noite. O gabarito entra só nesta leitura, nunca no agente."
                + (f" Prompt contra a calibração (seção 3.3 do plano): maior prompt da tela {pr['maximo_da_tela']} tokens, limite de "
                   f"{pr['limite_mais_10_pct']} (10% acima do maior da calibração, {pr['maximo_da_calibracao']}); casos acima: "
                   + (", ".join(f"`{c}`" for c in pr["acima"]) or "nenhum") + "." if pr else ""), ""]
    return "\n".join(cab) + "\n\n" + "\n\n".join(blocos) + "\n"


def ler_tela(saida: str) -> dict:
    """O bruto da corrida 18: os registros da tela e do fixture, o resumo por caso, o tamanho da trilha, os casos com
    gabarito (dos bancos) e a leitura da calibração, quando existe."""
    raiz = caminhos.fase3(saida)["raiz"]
    cond = _json(raiz / "condicoes_fase4.json") or {}
    slug = executar_fase3._slug(cond.get("modelo") or ex.MODELO_PADRAO)
    info = None
    vivos: dict = {}
    arq_trilha = raiz / "trilha_tela.jsonl"
    if arq_trilha.exists():
        eventos = tr.ler(arq_trilha)
        cab = eventos[0]["dados"] if eventos and eventos[0]["tipo"] == "corrida" else {}
        tamanho = cab.get("tamanho") or {}
        info = {"bytes": arq_trilha.stat().st_size, "eventos": tamanho.get("eventos", len(eventos)), "blobs_externos": tamanho.get("blobs_externos", 0)}
        # ! Alteração de IA - Revisar: (01/11/2026) os blobs `caso_ao_vivo` da trilha dão a entrada de cada caso ao vivo
        # (id "<caso>@tela"), para a leitura dizer o que a poda deixou no CORPO e no SINTOMA.
        # ! Motivo: os registros oficiais só guardam a resposta; o texto que foi ao modelo vive na trilha.
        for e in eventos:
            d = e.get("dados") or {}
            if e.get("tipo") == "blob" and d.get("papel") == "caso_ao_vivo" and isinstance(d.get("texto"), str):
                try:
                    reg = json.loads(d["texto"])
                except ValueError:
                    continue
                if isinstance(reg, dict) and reg.get("id") and isinstance(reg.get("entrada"), dict):
                    vivos[str(reg["id"])] = reg["entrada"]
    return {"tela": executar_bateria.ler_jsonl(raiz / slug / "diagnosticos__tela.jsonl"),
            "fixture": executar_bateria.ler_jsonl(raiz / slug / "diagnosticos__fixture.jsonl"),
            "casos": ex.casos_de_avaliacao("avaliacao"), "por_caso": executar_bateria.ler_jsonl(raiz / "tela.jsonl"), "trilha_info": info,
            "calibracao": _json(pasta_fase4() / f"{NOME_CALIBRACAO}.json"), "condicoes": cond, "vivos": vivos}


# ------------------------------------------------------------------ corrida 19: cura de seletor (regra R3)

def ler_cura(saida: str) -> dict:
    raiz = caminhos.fase3(saida)["raiz"]
    return {"registros": executar_bateria.ler_jsonl(raiz / "cura.jsonl"), "condicoes": _json(raiz / "condicoes_fase4.json") or {}}


def _grupo_da_cura(chave: str, valor, registros: list[dict]) -> dict:
    """As contagens da regra R3 num grupo de execuções (por modo, por roteiro ou por forma)."""
    quebradas = [r for r in registros if r.get("quebrou")]
    curadas = [r for r in quebradas if r.get("curado")]
    mttr = [r["mttr_s"] for r in curadas if isinstance(r.get("mttr_s"), (int, float))]
    aplicadas = Counter(r["aplicado"] for r in curadas if r.get("aplicado"))
    return {chave: valor, "execucoes": len(registros), "quebrou": len(quebradas), "curadas": len(curadas),
            "taxa_de_cura_pct": _pct(len(curadas), len(quebradas)), "mesmo_elemento": sum(1 for r in curadas if r.get("mesmo_elemento") is True),
            "outro_elemento": sum(1 for r in curadas if r.get("mesmo_elemento") is False), "nao_curadas": len(quebradas) - len(curadas),
            "nao_quebrou": len(registros) - len(quebradas), "mttr_mediana_s": _mediana(mttr), "mttr_max_s": max(mttr, default=None),
            "estrategias_aplicadas": dict(sorted(aplicadas.items()))}


def _comparar_formas(registros: list[dict]) -> dict:
    """Célula a célula (roteiro e modo), a forma pelo harness contra a forma pelo PHP: a árvore da página quebrada é a mesma
    (sha do snapshot completo) e o resultado (quebrou, curou, por repetição) é o mesmo?"""
    por_celula: dict[tuple, dict[str, list[dict]]] = {}
    for r in registros:
        por_celula.setdefault((r["roteiro"], r["modo"]), {}).setdefault(r["forma"], []).append(r)
    comparadas, iguais, diferentes, mesmo_resultado = 0, 0, [], 0
    for (roteiro, modo), formas in sorted(por_celula.items()):
        if "harness" not in formas or "php" not in formas:
            continue
        comparadas += 1
        sha_h = {r.get("arvore_sha") for r in formas["harness"]}
        sha_p = {r.get("arvore_sha") for r in formas["php"]}
        if sha_h == sha_p and len(sha_h) == 1:
            iguais += 1
        else:
            diferentes.append(f"{roteiro}/{modo}")
        res_h = sorted((bool(r.get("quebrou")), bool(r.get("curado")), r.get("aplicado")) for r in formas["harness"])
        res_p = sorted((bool(r.get("quebrou")), bool(r.get("curado")), r.get("aplicado")) for r in formas["php"])
        if res_h == res_p:
            mesmo_resultado += 1
    return {"celulas_comparadas": comparadas, "arvore_igual": iguais, "arvore_diferente": diferentes, "mesmo_resultado": mesmo_resultado}


def _por_estrategia(quebradas: list[dict]) -> list[dict]:
    saida = []
    for e in cs.ESTRATEGIAS:
        cands = [c for r in quebradas for c in (r.get("candidatos") or []) if c.get("estrategia") == e]
        gerados = [c for c in cands if c.get("gerado")]
        recusada = Counter()
        for c in gerados:
            for v in cs.VERIFICACOES:
                if ((c.get("verificacoes") or {}).get(v) or {}).get("resultado") == "nao_confere":
                    recusada[v] += 1
        saida.append({"estrategia": e, "execucoes": len(cands), "gerada": len(gerados), "passou_estaticas": sum(1 for c in gerados if c.get("passou_estaticas")),
                      "reexecutada": sum(1 for c in gerados if c.get("reexecutado")), "aplicada": sum(1 for c in gerados if c.get("aplicado")),
                      "recusada_em": {v: recusada.get(v, 0) for v in cs.VERIFICACOES}})
    return saida


def resumir_cura(registros: list[dict], condicoes: dict, gerado_em: str | None = None, corrida: str | None = None) -> dict:
    """A leitura da corrida 19: totais da regra R3, por modo de quebra, por roteiro, por forma, a comparação das duas
    formas, o rendimento de cada estratégia, os casos "outro elemento", os não curados e a lista das execuções."""
    quebradas = [r for r in registros if r.get("quebrou")]
    curadas = [r for r in quebradas if r.get("curado")]
    mttr = [r["mttr_s"] for r in curadas if isinstance(r.get("mttr_s"), (int, float))]
    modos = [m for m in cen.MODOS_DE_QUEBRA if any(r["modo"] == m for r in registros)]
    roteiros = [x for x in cen.ROTEIROS_DA_CURA if any(r["roteiro"] == x for r in registros)]
    formas = [f for f in cen.FORMAS_DE_QUEBRA if any(r["forma"] == f for r in registros)]
    compacto = ("id", "roteiro", "modo", "forma", "repeticao", "localizador", "quebrou", "passo_falho", "aplicado", "seletor_curado", "curado", "mesmo_elemento",
                "falha", "mttr_s", "reexecucoes", "segundos_quebra", "segundos_cura", "erro_da_referencia", "fora_do_alvo")
    r3_ok = all(any(c.get("aplicado") and (c.get("efeito") or {}).get("resultado") == "confere" for c in (r.get("candidatos") or [])) for r in curadas)
    return {"metadados": {"gerado_em": gerado_em or datetime.now().isoformat(timespec="seconds"), "corrida": corrida,
                          "fonte": "cura.jsonl e condicoes_fase4.json gravados por executar_fase4.py --modo cura", "parcial": bool(condicoes.get("parcial"))},
            "resumo": {"execucoes": len(registros), "quebras_detectadas": len(quebradas), "nao_quebrou": len(registros) - len(quebradas), "curadas": len(curadas),
                       "nao_curadas": len(quebradas) - len(curadas), "taxa_de_cura_pct": _pct(len(curadas), len(quebradas)),
                       "mesmo_elemento": sum(1 for r in curadas if r.get("mesmo_elemento") is True), "outro_elemento": sum(1 for r in curadas if r.get("mesmo_elemento") is False),
                       "mttr_mediana_s": _mediana(mttr), "mttr_min_s": min(mttr, default=None), "mttr_max_s": max(mttr, default=None),
                       "reexecucoes_mediana": _mediana([r.get("reexecucoes") for r in quebradas]), "repeticoes": condicoes.get("repeticoes"),
                       "limiar_nome": condicoes.get("limiar_nome"), "formas": condicoes.get("formas") or formas, "tempo_limite_ms": condicoes.get("tempo_limite_ms"),
                       "celulas": len({(r["roteiro"], r["modo"], r["forma"]) for r in registros}),
                       "fora_do_alvo": sum(1 for r in quebradas if r.get("fora_do_alvo"))},
            "por_modo": [_grupo_da_cura("modo", m, [r for r in registros if r["modo"] == m]) for m in modos],
            "por_roteiro": [_grupo_da_cura("roteiro", x, [r for r in registros if r["roteiro"] == x]) for x in roteiros],
            "por_forma": [_grupo_da_cura("forma", f, [r for r in registros if r["forma"] == f]) for f in formas],
            "formas": _comparar_formas(registros), "por_estrategia": _por_estrategia(quebradas),
            "outro_elemento": [{k: r.get(k) for k in ("id", "roteiro", "modo", "forma", "repeticao", "aplicado", "seletor_curado", "mttr_s")} for r in curadas if r.get("mesmo_elemento") is False],
            "nao_curadas": [{k: r.get(k) for k in ("id", "roteiro", "modo", "forma", "repeticao", "falha", "reexecucoes", "erro_da_referencia", "fora_do_alvo", "passo_falho", "erro")}
                            for r in quebradas if not r.get("curado")],
            "nao_quebrou": [{k: r.get(k) for k in ("id", "roteiro", "modo", "forma", "repeticao", "localizador")} for r in registros if not r.get("quebrou")],
            "execucoes": [{k: r.get(k) for k in compacto} for r in registros],
            "regra_r3": {"texto": "uma cura só conta quando a conferência final do roteiro passa na reexecução; o relatório separa \"mesmo elemento do alvo original\" "
                                  "de \"outro elemento que fez o roteiro passar\"", "cumprida": r3_ok},
            "condicoes": {k: condicoes.get(k) for k in ("repeticoes", "formas", "roteiros", "modos_de_quebra", "celulas", "parcial", "limiar_nome", "tempo_limite_ms", "mttr", "descricao_dos_modos")}}


def render_cura(dado: dict) -> str:
    r = dado["resumo"]
    f = dado.get("formas") or {}

    def grupo(bloco: str, chave: str, rotulo: str, linhas: list[dict]) -> str:
        return a3b.tab(bloco, [rotulo, "Execuções", "Quebraram", "Curadas", "Taxa de cura (%)", "Mesmo elemento", "Outro elemento", "Não curadas", "Não quebrou",
                               "MTTR mediana (s)", "MTTR máximo (s)", "Estratégias aplicadas"],
                       [[f"`{x[chave]}`", str(x["execucoes"]), str(x["quebrou"]), str(x["curadas"]), _n(x["taxa_de_cura_pct"]), str(x["mesmo_elemento"]), str(x["outro_elemento"]),
                         str(x["nao_curadas"]), str(x["nao_quebrou"]), _n(x["mttr_mediana_s"]), _n(x["mttr_max_s"]),
                         ", ".join(f"`{k}` {v}" for k, v in x["estrategias_aplicadas"].items()) or "nenhuma"] for x in linhas] or [["sem execuções"] + [""] * 11])

    blocos = [
        a3b.tab("tb_f4_cura_resumo", ["Execuções", "Quebras detectadas", "Não quebrou", "Curadas", "Não curadas", "Taxa de cura (%)", "Mesmo elemento", "Outro elemento",
                                      "MTTR mediana (s)", "MTTR mínimo (s)", "MTTR máximo (s)", "Reexecuções (mediana)", "Repetições", "Limiar do nome", "Formas", "Tempo limite (ms)"],
                [[str(r["execucoes"]), str(r["quebras_detectadas"]), str(r["nao_quebrou"]), str(r["curadas"]), str(r["nao_curadas"]), _n(r["taxa_de_cura_pct"]),
                  str(r["mesmo_elemento"]), str(r["outro_elemento"]), _n(r["mttr_mediana_s"]), _n(r["mttr_min_s"]), _n(r["mttr_max_s"]), _n(r["reexecucoes_mediana"]),
                  _n(r.get("repeticoes")), _n(r.get("limiar_nome")), ", ".join(r.get("formas") or []), _n(r.get("tempo_limite_ms"))]]),
        grupo("tb_f4_cura_por_modo", "modo", "Modo de quebra", dado["por_modo"]),
        grupo("tb_f4_cura_por_roteiro", "roteiro", "Roteiro", dado["por_roteiro"]),
        grupo("tb_f4_cura_por_forma", "forma", "Forma da quebra", dado["por_forma"]),
        a3b.tab("tb_f4_cura_formas", ["Células comparadas (harness e php)", "Mesma árvore da página quebrada", "Árvore diferente em", "Mesmo resultado (quebrou, curou, estratégia)"],
                [[str(f.get("celulas_comparadas", 0)), str(f.get("arvore_igual", 0)), ", ".join(f"`{c}`" for c in f.get("arvore_diferente") or []) or "nenhuma", str(f.get("mesmo_resultado", 0))]]),
        a3b.tab("tb_f4_cura_estrategias", ["Estratégia", "Gerada", "Passou as estáticas", "Reexecutada", "Aplicada (curou)"] + [f"Recusada em {v}" for v in cs.VERIFICACOES],
                [[f"`{x['estrategia']}`", str(x["gerada"]), str(x["passou_estaticas"]), str(x["reexecutada"]), str(x["aplicada"])] + [str(x["recusada_em"][v]) for v in cs.VERIFICACOES]
                 for x in dado["por_estrategia"]]),
        a3b.tab("tb_f4_cura_outro_elemento", ["Execução", "Roteiro", "Modo", "Forma", "Estratégia aplicada", "Seletor curado", "MTTR (s)"],
                [[f"`{x['id']}`", x["roteiro"], f"`{x['modo']}`", x["forma"], f"`{x['aplicado']}`", f"`{x['seletor_curado']}`", _n(x["mttr_s"])] for x in dado["outro_elemento"]]
                or [["nenhuma"] + [""] * 6]),
        a3b.tab("tb_f4_cura_nao_curadas", ["Execução", "Roteiro", "Modo", "Forma", "Falha", "Reexecuções", "Fora do passo do alvo", "Erro"],
                [[f"`{x['id']}`", x["roteiro"], f"`{x['modo']}`", x["forma"], f"`{x['falha']}`" if x.get("falha") else "", str(x["reexecucoes"]),
                  _sim(bool(x.get("fora_do_alvo"))), _n(x.get("erro_da_referencia") or (str(x.get("erro"))[:120] if x.get("erro") else None))]
                 for x in dado["nao_curadas"]] or [["nenhuma"] + [""] * 7]),
        a3b.tab("tb_f4_cura_execucoes", ["Execução", "Localizador", "Quebrou", "Passo", "Curada", "Estratégia", "Seletor curado", "Mesmo elemento", "Falha", "MTTR (s)", "Reexecuções", "Segundos"],
                [[f"`{x['id']}`", f"`{x['localizador']}`", _sim(x["quebrou"]), _n(x["passo_falho"]), _sim(x["curado"]), f"`{x['aplicado']}`" if x.get("aplicado") else "",
                  f"`{x['seletor_curado']}`" if x.get("seletor_curado") else "", _sim(x["mesmo_elemento"]), f"`{x['falha']}`" if x.get("falha") else "", _n(x["mttr_s"]),
                  str(x["reexecucoes"]), _n(x["segundos_cura"])] for x in dado["execucoes"]] or [["nenhuma"] + [""] * 11]),
    ]
    cab = pf.cabecalho(TITULO_CURA, "avaliar_fase4.py", "cura.jsonl e condicoes_fase4.json da corrida", dado["metadados"]["gerado_em"][:10])
    cab += ["", "Uma cura só conta quando a conferência final do roteiro passa na reexecução com o candidato no lugar do localizador (regra R3 do plano "
                "aprovado); \"mesmo elemento\" e \"outro elemento\" saem da impressão do DOM (tag, type, name, action do formulário, data-nome, href), que nenhum "
                "modo de quebra muda. O MTTR vai da detecção (o passo do alvo falhou) à reexecução validada, descontado o tempo de restaurar o banco. As "
                "duas formas da quebra (pelo harness no navegador e pela variante do front PHP, ficha 29 c) são comparadas célula a célula pela árvore da "
                "página quebrada e pelo resultado.", ""]
    return "\n".join(cab) + "\n\n" + "\n\n".join(blocos) + "\n"


# ------------------------------------------------------------------ corrida 20: biblioteca em produção e ciclo de correção (R4 e R5)

def ler_biblioteca(saida: str) -> dict:
    """Tudo o que a leitura da corrida 20 precisa: condições, biblioteca.jsonl, as propostas, lote.json, a reavaliação (os
    registros do lote e os da base, com o gabarito dos inéditos juntado aqui), correcoes.jsonl, sonda.json e a trilha."""
    import biblioteca_fase4 as bf
    import executar_fase3b as e3b
    raiz = caminhos.fase3(saida)["raiz"]
    cond = _json(raiz / "condicoes_fase4.json") or {}
    slug = executar_fase3._slug(cond.get("modelo") or ex.MODELO_PADRAO)
    registros = executar_bateria.ler_jsonl(raiz / "biblioteca.jsonl")
    propostas = executar_bateria.ler_jsonl(raiz / slug / f"propostas__E{ex.EPOCA_DO_LOTE}.jsonl")
    lote = _json(raiz / "lote.json")
    try:
        por_id_ined = {c["id"]: c for c in e3b._casos_ineditos()}
    except SystemExit:
        por_id_ined = {}

    def com_gabarito(regs: list[dict]) -> list[dict]:
        return [{**r, "gabarito": por_id_ined[r["caso"]]["gabarito"]} for r in regs if r.get("caso") in por_id_ined]

    novo = com_gabarito(executar_bateria.ler_jsonl(raiz / slug / f"reavaliacao__E{ex.EPOCA_DO_LOTE}.jsonl"))
    if cond.get("base_ineditos") == "propria":
        base = com_gabarito(executar_bateria.ler_jsonl(raiz / slug / f"reavaliacao__L{dv.VERSAO_CURADA}.jsonl"))
    else:
        arq_base = caminhos.RESULTADOS / ex.CORRIDA12 / slug / f"diagnosticos__L{dv.VERSAO_CURADA}.jsonl"
        hash_curada = (cond.get("biblioteca") or {}).get("hash")
        base = com_gabarito([r for r in executar_bateria.ler_jsonl(arq_base) if not hash_curada or r.get("biblioteca_versao") == hash_curada])
    reavaliacao = {"base": base, "novo": novo, "origem_da_base": (lote or {}).get("origem_da_base") or cond.get("origem_da_base")} if novo else None
    correcoes = executar_bateria.ler_jsonl(raiz / "correcoes.jsonl")
    sonda = _json(raiz / "sonda.json")
    if sonda is not None and not sonda.get("anterior"):
        sonda["anterior"] = bf.sonda_anterior()
    diag = executar_bateria.ler_jsonl(raiz / slug / f"diagnosticos__L{dv.VERSAO_CURADA}.jsonl")
    inferencias = len(diag) + len(propostas) + len(novo) + (len(base) if cond.get("base_ineditos") == "propria" else 0) + 2 * len((sonda or {}).get("casos") or [])
    segundos = sum((r.get("segundos_diagnostico") or 0) + (r.get("segundos_proposta") or 0) for r in registros) + sum(r.get("segundos") or 0 for r in novo) \
        + sum(x.get("segundos") or 0 for x in (sonda or {}).get("casos") or [])
    arq_trilha = raiz / "trilha_biblioteca.jsonl"
    trilha_info = ({"bytes": arq_trilha.stat().st_size, "eventos": sum(1 for l in arq_trilha.read_text(encoding="utf-8").splitlines() if l.strip())}
                   if arq_trilha.exists() else None)
    por_id_corrida: Counter = Counter(v for r in registros for v in r.get("recuperacao_por_id") or [])
    recuperacao = {"aprendidos_na_calibracao": cond.get("recuperacao_dos_aprendidos") or {},
                   "por_id_nesta_corrida": {"casos_com_verbete_por_id": sum(1 for r in registros if r.get("recuperacao_por_id")), "verbetes": dict(por_id_corrida)}}
    return {"condicoes": cond, "registros": registros, "propostas": propostas, "lote": lote, "reavaliacao": reavaliacao, "correcoes": correcoes, "sonda": sonda,
            "recuperacao": recuperacao, "trilha_info": trilha_info, "inferencias": inferencias, "segundos": round(segundos, 1)}


def _sonda_resumida(sonda: dict | None) -> dict | None:
    if not sonda or not sonda.get("casos"):
        return None
    anterior = sonda.get("anterior") or {}
    por_caso = []
    for x in sonda["casos"]:
        a = anterior.get(x["caso"])
        mudou = None if a is None else ((x.get("n_propostas"), x.get("n_aceitas"), sorted(x.get("motivos") or []), bool(x.get("abstencao")))
                                        != (a.get("n_propostas"), a.get("n_aceitas"), sorted(a.get("motivos") or []), bool(a.get("abstencao"))))
        por_caso.append({"caso": x["caso"], "rotulo": x.get("rotulo"), "acertou": x.get("acertou"), "n_propostas": x.get("n_propostas"), "n_aceitas": x.get("n_aceitas"),
                         "abstencao": bool(x.get("abstencao")), "motivos": list(x.get("motivos") or []), "menciona_correcao": bool(x.get("menciona_correcao")),
                         "por_id": list(x.get("por_id") or []), "segundos": x.get("segundos"),
                         "rotulo_anterior": a.get("rotulo") if a else None, "acertou_anterior": a.get("acertou") if a else None,
                         "n_propostas_anterior": a.get("n_propostas") if a else None, "n_aceitas_anterior": a.get("n_aceitas") if a else None,
                         "motivos_anteriores": list(a.get("motivos") or []) if a else [], "mudou_proposta": mudou})
    return {"casos": len(por_caso), "acertos": sum(1 for x in por_caso if x["acertou"]), "mudaram_proposta": sum(1 for x in por_caso if x["mudou_proposta"] is True),
            "sem_sonda_anterior": sum(1 for x in por_caso if x["mudou_proposta"] is None), "mencionam_correcao": sum(1 for x in por_caso if x["menciona_correcao"]),
            "abstencoes": sum(1 for x in por_caso if x["abstencao"]), "com_verbete_por_id": sum(1 for x in por_caso if x["por_id"]),
            "origem": sonda.get("origem"), "epoca": sonda.get("epoca"), "por_caso": por_caso}


def resumir_biblioteca(bruto: dict, gerado_em: str | None = None, corrida: str | None = None) -> dict:
    """A leitura da corrida 20: os casos de aprendizado (tela e fixture, acerto), as propostas e o que cada filtro barrou, o
    lote, a regra R5 na reavaliação dos inéditos, a regra R4 no ciclo de correção, a sonda contra 28/09 e a recuperação dos
    aprendidos."""
    import biblioteca_fase4 as bf
    cond = bruto.get("condicoes") or {}
    registros = bruto.get("registros") or []
    propostas = bruto.get("propostas") or []
    m = bf.metricas_da_rodada(propostas)
    lote_b = bruto.get("lote") or {}
    fech = lote_b.get("fechamento") or {}
    edicoes = lote_b.get("edicoes") or []
    para_revisao = lote_b.get("para_revisao") or []
    reav = bruto.get("reavaliacao")
    reavaliacao = None
    if reav and reav.get("novo"):
        r5 = bf.avaliar_lote(reav.get("base") or [], reav["novo"])
        reavaliacao = {**r5, "acerto_base_pct": _pct(r5["acerto_base"], r5["n"]), "acerto_novo_pct": _pct(r5["acerto_novo"], r5["n"]), "origem_da_base": reav.get("origem_da_base")}
    correcoes = bruto.get("correcoes") or []
    r4 = bf.regra_r4(correcoes) if correcoes else None
    correcao = ({**r4, "por_caso": [{k: c.get(k) for k in ("caso", "cenario", "modo", "verbetes", "desligado", "reproduziu_antes", "passou_depois", "ha_diff_http",
                                                                "ha_diff_arvore", "sintoma_sumiu", "marcado", "motivo", "estados", "segundos")} for c in correcoes]}
                if r4 else None)
    sonda = _sonda_resumida(bruto.get("sonda"))
    rec_b = bruto.get("recuperacao") or {}
    na_cal = rec_b.get("aprendidos_na_calibracao") or {}
    por_id_c = rec_b.get("por_id_nesta_corrida") or {}
    acertos = sum(1 for r in registros if r.get("acertou"))
    compacto = ("caso", "classe", "nivel", "origem", "reproduz", "modo", "cenario", "rotulo", "acertou", "p_rotulo", "selo", "divergencia", "falha", "n_propostas", "n_aceitas",
                "para_revisao", "recusadas", "abstencao", "recuperacao_por_id", "verbetes_editados", "segundos_diagnostico", "segundos_proposta")
    return {"metadados": {"gerado_em": gerado_em or datetime.now().isoformat(timespec="seconds"), "corrida": corrida,
                          "fonte": "biblioteca.jsonl, propostas__E101.jsonl, lote.json, reavaliacao__E101.jsonl, correcoes.jsonl e sonda.json gravados por executar_fase4.py --modo biblioteca",
                          "parcial": bool(cond.get("parcial"))},
            "resumo": {"casos": len(registros), "da_tela": sum(1 for r in registros if r.get("origem") == "tela"), "do_fixture": sum(1 for r in registros if r.get("origem") == "fixture"),
                       "acertos_diagnostico": acertos, "acerto_pct": _pct(acertos, len(registros)), "propostas": m["propostas"], "aceitas": m["aceitas"],
                       "abstencoes": m["abstencoes"], "para_revisao": m["para_revisao"], "recusadas_p5": sum(m["recusadas_p5"].values()),
                       "recusadas_fase3": sum(m["recusadas_fase3"].values()), "taxa_de_rejeicao_pct": m["taxa_de_rejeicao_pct"], "peso_aceito": m["peso_aceito"],
                       "casos_com_verbete_por_id": por_id_c.get("casos_com_verbete_por_id", sum(1 for r in registros if r.get("recuperacao_por_id"))),
                       "inferencias": bruto.get("inferencias"), "segundos": bruto.get("segundos"), "trilha_bytes": (bruto.get("trilha_info") or {}).get("bytes"),
                       "trilha_eventos": (bruto.get("trilha_info") or {}).get("eventos"), "k": cond.get("k"), "hash_biblioteca": (cond.get("biblioteca") or {}).get("hash"),
                       "hash_do_lote": fech.get("hash"), "base_ineditos": cond.get("base_ineditos")},
            "filtros": [{"filtro": f, "recusas": m["por_filtro"].get(f, 0)} for f in bf.FILTROS],
            "rejeicoes": {"fase3": m["recusadas_fase3"], "p5": m["recusadas_p5"]},
            "lote": {"edicoes": len(edicoes), "para_revisao": len(para_revisao), "hash": fech.get("hash"), "n_notas": fech.get("n_notas"), "n_verbetes": fech.get("n_verbetes"),
                     "n_verbetes_novos": fech.get("n_verbetes_novos"), "por_tipo": dict(sorted(Counter(e.get("operacao") for e in edicoes).items())),
                     "peso": sum(e.get("peso") or 0 for e in edicoes), "aceitas_por_tipo": m["aceitas_por_tipo"],
                     "lista": [{k: e.get(k) for k in ("verbete", "operacao", "caso", "peso", "granularidade")} for e in edicoes],
                     "revisao": [{k: e.get(k) for k in ("verbete", "operacao", "caso", "peso")} for e in para_revisao], "conflitos": lote_b.get("conflitos") or []},
            "reavaliacao": reavaliacao, "correcao": correcao, "sonda": sonda,
            "recuperacao": {"aprendidos_na_calibracao": na_cal, "aprendidos_sem_recuperacao": bf.aprendidos_sem_recuperacao(na_cal),
                            "casos_com_verbete_por_id": por_id_c.get("casos_com_verbete_por_id", 0), "verbetes_por_id": por_id_c.get("verbetes") or {}},
            "regra_r4": {"texto": bf.REGRA_R4, "cumprida": None},
            "regra_r5": {"texto": bf.REGRA_R5, "veredito": reavaliacao["veredito"] if reavaliacao else None},
            "casos": [{k: r.get(k) for k in compacto} for r in registros],
            "condicoes": {k: cond.get(k) for k in ("k", "casos", "com_tela", "ineditos", "base_ineditos", "origem_da_base", "conjunto_de_correcao", "casos_da_sonda",
                                                    "parcelas_para_revisao", "parcela_para_revisao", "inferencias_previstas", "parcial", "teto_proposta")}}


def render_biblioteca(dado: dict) -> str:
    r = dado["resumo"]
    lote = dado["lote"]
    reav = dado.get("reavaliacao")
    corr = dado.get("correcao")
    sonda = dado.get("sonda")
    rec_ = dado.get("recuperacao") or {}
    blocos = [
        a3b.tab("tb_f4_biblioteca_resumo", ["Casos de aprendizado", "Da tela", "Do fixture", "Acertos do diagnóstico", "Acerto (%)", "Propostas", "Aceitas (lote)", "Abstenções (NENHUMA)",
                                            "Para revisão humana", "Recusadas pelos filtros do P5", "Recusadas pela Fase 3", "Taxa de rejeição (%)", "Casos com verbete pelo id",
                                            "Inferências", "Segundos", "Trilha (bytes)", "k", "Base dos inéditos"],
                [[str(r["casos"]), str(r["da_tela"]), str(r["do_fixture"]), str(r["acertos_diagnostico"]), _n(r["acerto_pct"]), str(r["propostas"]), str(r["aceitas"]), str(r["abstencoes"]),
                  str(r["para_revisao"]), str(r["recusadas_p5"]), str(r["recusadas_fase3"]), _n(r["taxa_de_rejeicao_pct"]), str(r["casos_com_verbete_por_id"]), _n(r.get("inferencias")),
                  _n(r.get("segundos")), _n(r.get("trilha_bytes")), _n(r.get("k")), _n(r.get("base_ineditos"))]]),
        a3b.tab("tb_f4_biblioteca_filtros", ["Filtro em código (decisão 65)", "Propostas barradas ou seguradas"], [[f"`{x['filtro']}`", str(x["recusas"])] for x in dado["filtros"]]),
        a3b.tab("tb_f4_biblioteca_rejeicoes", ["Quem recusou", "Código", "Propostas"],
                [["validador da Fase 3", f"`{k}`", str(v)] for k, v in (dado["rejeicoes"].get("fase3") or {}).items()]
                + [["filtros do P5", f"`{k}`", str(v)] for k, v in (dado["rejeicoes"].get("p5") or {}).items()] or [["nenhuma recusa", "", ""]]),
        a3b.tab("tb_f4_biblioteca_lote", ["Edições no lote", "Para revisão humana", "Peso somado", "Por tipo", "Hash do lote", "Notas na cópia", "Verbetes", "Verbetes novos"],
                [[str(lote["edicoes"]), str(lote["para_revisao"]), str(lote["peso"]), ", ".join(f"`{k}` {v}" for k, v in lote["por_tipo"].items()) or "nenhuma",
                  _n(lote["hash"]), _n(lote["n_notas"]), _n(lote["n_verbetes"]), _n(lote["n_verbetes_novos"])]]),
        a3b.tab("tb_f4_biblioteca_reavaliacao", ["Inéditos pareados", "Acerto com a cópia curada (%)", "Acerto com o lote (%)", "b (passaram a acertar)", "c (passaram a errar)",
                                                  "p (McNemar exato)", "Veredito R5", "Casos que mudaram", "Base"],
                [[str(reav["n"]), _n(reav["acerto_base_pct"]), _n(reav["acerto_novo_pct"]), str(reav["b"]), str(reav["c"]), _n(reav["p_mcnemar"]), reav["veredito"],
                  ", ".join(f"`{c}`" for c in reav["ganhos"] + reav["perdas"]) or "nenhum", _n(reav.get("origem_da_base"))]] if reav else [["não medida"] + [""] * 8]),
        a3b.tab("tb_f4_biblioteca_correcao", ["Casos com sintoma antes", "Modo desligado", "Modo mantido", "Marcados corrigido", "Certos", "Falsos positivos", "Perdidos",
                                              "Precisão (%)", "Revocação (%)", "Kappa", "Sem sintoma antes"],
                [[str(corr["universo"]), str(corr["desligados"]), str(corr["mantidos"]), str(corr["marcados"]), str(corr["acertos"]), str(corr["falsos_positivos"]), str(corr["perdidos"]),
                  _n(corr["precisao_pct"]), _n(corr["revocacao_pct"]), _n(corr["kappa"]), ", ".join(f"`{c}`" for c in corr["sem_sintoma_antes"]) or "nenhum"]] if corr else [["não medida"] + [""] * 10]),
        a3b.tab("tb_f4_biblioteca_correcao_casos", ["Caso", "Modo", "Verbetes", "Modo desligado", "Reproduziu antes", "Passou depois", "Fio mudou", "Árvore mudou", "Marcado", "Motivo"],
                [[f"`{c['caso']}`", f"`{c['modo']}`", ", ".join(f"`{v}`" for v in c.get("verbetes") or []), _sim(c["desligado"]), _sim(c["reproduziu_antes"]), _sim(c["passou_depois"]),
                  _sim(c["ha_diff_http"]), _sim(c["ha_diff_arvore"]), _sim(c["marcado"]), _n(c.get("motivo"))] for c in (corr or {}).get("por_caso") or []] or [["nenhum"] + [""] * 9]),
        a3b.tab("tb_f4_biblioteca_sonda", ["Caso", "Rótulo agora", "Acertou", "Propostas", "Aceitas", "NENHUMA", "Motivos de recusa", "Menciona a correção", "Verbetes pelo id",
                                           "Rótulo em 28/09", "Propostas em 28/09", "Aceitas em 28/09", "Mudou a proposta"],
                [[f"`{x['caso']}`", _n(x["rotulo"]), _sim(x["acertou"]), str(x["n_propostas"]), str(x["n_aceitas"]), _sim(x["abstencao"]), ", ".join(f"`{m}`" for m in x["motivos"]) or "nenhum",
                  _sim(x["menciona_correcao"]), ", ".join(f"`{v}`" for v in x["por_id"]) or "nenhum", _n(x["rotulo_anterior"]), _n(x["n_propostas_anterior"]), _n(x["n_aceitas_anterior"]),
                  "sem sonda anterior" if x["mudou_proposta"] is None else _sim(x["mudou_proposta"])] for x in (sonda or {}).get("por_caso") or []] or [["não medida"] + [""] * 12]),
        a3b.tab("tb_f4_biblioteca_revisao", ["Verbete", "Operação", "Caso", "Peso", "Parcela na calibração (%)"],
                [[f"`{e['verbete']}`", _n(e["operacao"]), f"`{e['caso']}`", _n(e["peso"]), _n(round(100 * (dado["condicoes"].get("parcelas_para_revisao") or {}).get(e["verbete"], 0), 1))]
                 for e in lote["revisao"]] or [["nenhuma"] + [""] * 4]),
        a3b.tab("tb_f4_biblioteca_recuperacao", ["Verbete aprendido", "Vezes na calibração (k = 3)", "Vezes pelo id nesta corrida"],
                [[f"`{v}`", str(n), str((rec_.get("verbetes_por_id") or {}).get(v, 0))] for v, n in sorted((rec_.get("aprendidos_na_calibracao") or {}).items())] or [["nenhum", "", ""]]),
        a3b.tab("tb_f4_biblioteca_casos", ["Caso", "Origem", "Rótulo", "Acertou", "Selo", "Propostas", "Aceitas", "Para revisão", "Recusadas", "NENHUMA", "Pelo id", "Verbetes editados", "Segundos"],
                [[f"`{c['caso']}`", _n(c["origem"]), _n(c["rotulo"]), _sim(c["acertou"]), _n(c["selo"]), str(c["n_propostas"]), str(c["n_aceitas"]), str(c["para_revisao"]),
                  ", ".join(f"`{m}`" for m in c.get("recusadas") or []) or "", _sim(c["abstencao"]), ", ".join(f"`{v}`" for v in c.get("recuperacao_por_id") or []) or "",
                  ", ".join(f"`{v}`" for v in c.get("verbetes_editados") or []) or "", _n(round((c.get("segundos_diagnostico") or 0) + (c.get("segundos_proposta") or 0), 1))]
                 for c in dado["casos"]] or [["nenhum"] + [""] * 12]),
    ]
    cab = pf.cabecalho(TITULO_BIBLIOTECA, "avaliar_fase4.py", "biblioteca.jsonl, propostas, lote.json, reavaliacao, correcoes.jsonl e sonda.json da corrida", dado["metadados"]["gerado_em"][:10])
    cab += ["", "Cada caso de aprendizado foi diagnosticado (da tela quando reproduz, do fixture nos outros) e, na continuação do mesmo prompt, o modelo propôs edições; "
                "o validador congelado da Fase 3 decide primeiro e os 13 filtros em código da decisão 65 depois; a regra dos 40% segura para revisão humana a nota em "
                "verbete presente em 40% ou mais dos contextos da calibração. A regra R5 compara o lote com a cópia curada nos 36 inéditos (b e c); a regra R4 compara "
                "a marca corrigido do ciclo de correção com o conjunto de casos cujo modo o harness desligou. A sonda repete a de 28/09/2026 com a recuperação por id ligada.", ""]
    return "\n".join(cab) + "\n\n" + "\n\n".join(blocos) + "\n"


# ------------------------------------------------------------------ pontes de versão (regra R6)

def pontes_conhecidas(modelo: str = ex.MODELO_PADRAO) -> dict:
    """pontes.json refeito das pontes já rodadas: as da Fase 3-B (analisar_fase3b.PONTES) e as das corridas da Fase 4
    (`fase4_*/ponte`), cada uma pareada com a Fase 3 pela mesma conta de executar_fase4.ponte_contra_fase3."""
    slug = executar_fase3._slug(modelo)
    base = executar_bateria.ler_jsonl(caminhos.fase3("fase3")["raiz"] / slug / "diagnosticos__L0.jsonl")
    pastas = [(nome, caminhos.fase3(nome)["raiz"]) for nome in a3b.PONTES]
    pastas += sorted((f"{p.parent.name}/ponte", p) for p in caminhos.RESULTADOS.glob("fase4_*/ponte") if p.is_dir())
    entradas = []
    for nome, raiz in pastas:
        arq = raiz / slug / "diagnosticos__L0.jsonl"
        if not arq.exists():
            continue
        cond = _json(raiz / "condicoes_3b.json") or {}
        # a ponte de uma corrida da Fase 4 diz se foi parcial no condicoes_3b.json da própria subpasta e no
        # condicoes_fase4.json da corrida; uma ponte parcial ou que não cobriu os 36 fica de fora
        pai = _json(raiz.parent / "condicoes_fase4.json") or {}
        novos = executar_bateria.ler_jsonl(arq)
        if not ex.ponte_completa(novos, {"parcial": cond.get("parcial") or pai.get("parcial")}):
            continue
        versao = cond.get("versao_ollama") or (novos[0].get("versao_ollama") if novos else None)
        entradas.append({"versao": versao, "corrida": nome, "data": str(cond.get("criado_em") or "")[:10], "modelo": modelo, "completa": True,
                         **ex.ponte_contra_fase3(novos, base)})
    entradas.sort(key=lambda e: (e["data"], e["corrida"]))
    return {"gerado_por": "avaliar_fase4.py --pontes", "modelo": modelo, "limite": ex.LIMITE_PONTE,
            "base": "resultados_alvo/fase3/<modelo>/diagnosticos__L0.jsonl (Ollama 0.34.0)",
            "regra": "R6: versão do Ollama sem ponte aqui, L0 nos 36 de avaliação antes de tudo; pareável com b + c até o limite (decisão 47)",
            "pontes": entradas}


def nome_dos_arquivos(pedido: str | None, modo: str) -> str:
    """O nome dos arquivos da leitura em resultados_alvo/fase4: o pedido por --nome ou o padrão do modo
    (reproducibilidade, calibracao, tela)."""
    padrao = {"reproducao": NOME, "calibracao": NOME_CALIBRACAO, "tela": NOME_TELA, "cura": NOME_CURA, "biblioteca": NOME_BIBLIOTECA}[modo]
    return pedido or padrao


def _conferir_ou_gravar_json(caminho: Path, dado: dict, check: bool, ignorar=("gravado_em",)) -> int:
    """Grava o JSON (com `gravado_em`) ou, com check, compara com o gravado sem a data; devolve 1 quando difere."""
    def limpo(d: dict) -> dict:
        return {k: v for k, v in d.items() if k not in ignorar}
    if check:
        antigo = _json(caminho)
        if antigo is not None and limpo(antigo) == limpo(json.loads(json.dumps(dado, ensure_ascii=False))):
            print(f"--check: {caminho.name} bate com os dados atuais")
            return 0
        print(f"--check: {caminho.name} DIFERE" + (" (não existe)" if antigo is None else ""))
        return 1
    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_text(json.dumps({**dado, "gravado_em": datetime.now().isoformat(timespec="seconds")}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"gravado: {caminho}")
    return 0


def montar_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--reproducao", action="store_true", help="avalia a corrida 17 (reprodução na tela)")
    ap.add_argument("--calibracao", action="store_true", help="avalia a corrida 16 (calibração e ponte) e grava limiares.json")
    ap.add_argument("--tela", action="store_true", help="avalia a corrida 18 (diagnóstico ao vivo contra o fixture, regra R2)")
    ap.add_argument("--pontes", action="store_true", help="regrava resultados_alvo/fase4/pontes.json a partir das pontes já rodadas")
    ap.add_argument("--cura", action="store_true", help="avalia a corrida 19 (cura de seletor, regra R3)")
    ap.add_argument("--biblioteca", action="store_true", help="avalia a corrida 20 (biblioteca em produção e ciclo de correção, regras R4 e R5)")
    ap.add_argument("--saida", default="fase4_reproducao")
    # ! Alteração de IA - Revisar: (01/11/2026, ficha 37) `--nome` sem padrão fixo: cada modo tem o seu (reproducibilidade,
    # tela) e `--tela --nome tela_v2` grava a leitura da repetição da corrida 18 sem regravar `tela.{json,md}`.
    # ! Motivo: o padrão era "reproducibilidade" para todo modo, e a leitura da tela ignorava a opção.
    ap.add_argument("--nome", default=None, help="nome dos arquivos em resultados_alvo/fase4 (padrão: reproducibilidade para --reproducao, "
                                                 "tela para --tela; ex.: reproducibilidade_ineditos, tela_v2)")
    ap.add_argument("--titulo", default=TITULO, help="título do relatório .md")
    ap.add_argument("--pasta", default=None, help="pasta dos derivados (padrão resultados_alvo/fase4); corrida parcial grava na pasta da própria corrida")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--colar", action="store_true")
    return ap


def main() -> int:
    ap = montar_parser()
    args = ap.parse_args()
    print(caminhos.descricao())
    modos = [m for m in ("reproducao", "calibracao", "tela", "pontes", "cura", "biblioteca") if getattr(args, m)]
    if len(modos) != 1:
        ap.error("informe um de --reproducao, --calibracao, --tela, --cura, --biblioteca ou --pontes")
    pasta = Path(args.pasta) if args.pasta else pasta_fase4()
    oficial = pasta.resolve() == pasta_fase4().resolve()

    def parcial_na_pasta_oficial(cond: dict) -> bool:
        """Uma corrida parcial (--casos) nunca grava derivado em resultados_alvo/fase4: só com --pasta apontando para outra pasta."""
        if cond.get("parcial") and oficial:
            print("corrida parcial (--casos): os derivados não vão para resultados_alvo/fase4; passe --pasta com a pasta da própria corrida")
            return True
        return False

    if args.pontes:
        return _conferir_ou_gravar_json(pasta / "pontes.json", pontes_conhecidas(), args.check)
    if args.biblioteca:
        bruto = ler_biblioteca(args.saida)
        if not bruto["registros"]:
            print(f"sem biblioteca.jsonl em {caminhos.fase3(args.saida)['raiz']}")
            return 2
        if parcial_na_pasta_oficial(bruto["condicoes"]):
            return 2
        nome_b = nome_dos_arquivos(args.nome, "biblioteca")
        if args.colar and nome_b != NOME_BIBLIOTECA:
            ap.error("--colar só com o nome padrão")
        dado = resumir_biblioteca(bruto, corrida=args.saida)
        return pf.fechar(nome_b, dado, render_biblioteca(dado), PREFIXO_BIBLIOTECA, check=args.check, colar=args.colar, pasta=pasta, doc=RELATORIO)
    if args.cura:
        bruto = ler_cura(args.saida)
        if not bruto["registros"]:
            print(f"sem cura.jsonl em {caminhos.fase3(args.saida)['raiz']}")
            return 2
        if parcial_na_pasta_oficial(bruto["condicoes"]):
            return 2
        nome_c = nome_dos_arquivos(args.nome, "cura")
        if args.colar and nome_c != NOME_CURA:
            ap.error("--colar só com o nome padrão")
        dado = resumir_cura(bruto["registros"], bruto["condicoes"], corrida=args.saida)
        return pf.fechar(nome_c, dado, render_cura(dado), PREFIXO_CURA, check=args.check, colar=args.colar, pasta=pasta, doc=RELATORIO)
    if args.reproducao:
        nome = nome_dos_arquivos(args.nome, "reproducao")
        if args.colar and nome != NOME:
            ap.error("--colar só com o nome padrão: os blocos das duas corridas têm os mesmos nomes no relatório")
        registros, fora = ler(args.saida)
        if not registros and not fora:
            print(f"sem reproducao.jsonl em {caminhos.fase3(args.saida)['raiz']}")
            return 2
        dado = resumir(registros, fora, corrida=args.saida)
        return pf.fechar(nome, dado, render(dado, args.titulo), PREFIXO, check=args.check, colar=args.colar, pasta=pasta, doc=RELATORIO)
    if args.calibracao:
        bruto = ler_calibracao(args.saida)
        if not bruto["k"]:
            print(f"sem registros de calibração em {caminhos.fase3(args.saida)['raiz']}")
            return 2
        if parcial_na_pasta_oficial(bruto["condicoes"]):
            return 2
        dado = resumir_calibracao(bruto, corrida=args.saida)
        codigo = pf.fechar(NOME_CALIBRACAO, dado, render_calibracao(dado), PREFIXO_CALIBRACAO, check=args.check, colar=args.colar, pasta=pasta, doc=RELATORIO)
        if dado["limiares"] and not args.colar:
            codigo = max(codigo, _conferir_ou_gravar_json(pasta / "limiares.json", dado["limiares"], args.check))
        return codigo
    bruto = ler_tela(args.saida)
    if not bruto["tela"]:
        print(f"sem diagnósticos da tela em {caminhos.fase3(args.saida)['raiz']}")
        return 2
    if parcial_na_pasta_oficial(bruto["condicoes"]):
        return 2
    dado = resumir_tela(bruto["tela"], bruto["fixture"], bruto["casos"], bruto["por_caso"], bruto["trilha_info"], bruto["calibracao"], corrida=args.saida,
                        vivos=bruto.get("vivos"))
    nome_t = nome_dos_arquivos(args.nome, "tela")
    if args.colar and nome_t != NOME_TELA:
        ap.error("--colar só com o nome padrão: os blocos das duas corridas têm os mesmos nomes no relatório")
    return pf.fechar(nome_t, dado, render_tela(dado), PREFIXO_TELA, check=args.check, colar=args.colar, pasta=pasta, doc=RELATORIO)


if __name__ == "__main__":
    sys.exit(main())
