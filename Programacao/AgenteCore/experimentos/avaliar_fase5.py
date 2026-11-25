#!/usr/bin/env python3
# ! Alteração de IA - Revisar: arquivo novo (16/11/2026, Fase 5, pacote F1): a leitura da medição de valor, com cinco opções. `--custo` estima o tempo da noite
# medida (corrida 28) a partir dos registros da corrida 21d; `--antes` confere, sem chamar o modelo, que o agente de hoje é o da corrida 21d (biblioteca de
# produção, prompt fixo, índice da busca, k, limiares e versão do navegador) e sai com código 1 se algum diferir; `--agente` lê as execuções da corrida 28
# (`resultados_alvo/fase5_agente/cenarios.jsonl`); `--manual` lê a planilha da linha de base manual e o registro da sessão, e recusa a planilha dizendo a linha;
# `--comparar` põe os dois lados na mesma tabela. As quatro que gravam têm `--check` e `--colar`, e os derivados vão para `resultados_alvo/fase5/`
# (`custo`, `agente`, `manual` e `medicao`, cada um em .json e .md, com blocos `tb_f5_*`).
# ! Motivo: o plano aprovado da Fase 5 (seções 3, 4.6 e 5, decisões 132 e 133) fixa as regras de leitura L1 a L15 antes de qualquer medida, para a comparação
# entre o agente e as pessoas não ser escolhida depois de ver os números. Não existia leitura da planilha por script nem leitura que tratasse o cenário como a
# unidade: `avaliar_fase4.py --cenarios` conta cada execução como uma medida independente, e as cinco repetições do agente no mesmo cenário não são (mesmo prompt,
# temperatura 0,1). Aqui todo intervalo do tempo e todo veredito tratam o cenário como a unidade, com dez cenários, seis de contrato e quatro de localizador. A
# leitura vive em arquivo novo porque `avaliar_fase4.py`, `executar_fase4.py` e os registros das corridas não mudam nesta fase.
# ! Alteração de IA - Revisar: (18/11/2026, corrida 28b, decisões 145 e 146) a leitura oficial do agente passa a ser a da pasta nova, `resultados_alvo/fase5_agente_b`,
# e só é gravada em `resultados_alvo/fase5` com a noite completa e a frio; o bloco da noite ganha a conferência, por repetição, de que o prompt foi lido de novo
# (`conferir_frio`, pelo registro da barra de progresso da corrida); a corrida 28 fica guardada como incidente, com `--incidente 28`, em pasta e com blocos
# próprios; `--sondagem` dá o veredito da sondagem do frio; e `--situacao` diz também quantas repetições estão completas e de qual versão do Ollama.
# ! Motivo: a corrida 28 rodou em 18/11/2026 com o aplicativo Claude aberto, e nas repetições 2 a 5 o Ollama reaproveitou o prompt lido na repetição 1 (a noite
# levou 31 minutos, e não 68). O Eric decidiu refazer a noite com tudo fechado (decisão 145) e a frio, uma repetição por vez, com o modelo descarregado entre elas
# (decisão 146). As regras L1 a L15 não mudam. A conferência a frio é de validade da noite, e não regra de comparação: o limite dela foi fixado antes da corrida
# 28b, com os registros da corrida 28, em que a repetição 1 passa e as repetições 2 a 5 não.
"""Leitura da Fase 5: o MTTR e o Task Success do agente contra a linha de base manual. Em Programacao/AgenteCore/experimentos, com RESULTADOS_DIR=resultados_alvo:

  python avaliar_fase5.py --custo                 o tempo da noite medida, pelos registros da corrida 21d (grava resultados_alvo/fase5/custo.{json,md})
  ..\\.venv\\Scripts\\python.exe avaliar_fase5.py --antes   o agente de hoje é o da corrida 21d? (abre o navegador para ler a versão; não grava nada)
  python avaliar_fase5.py --agente                a corrida 28b (resultados_alvo/fase5_agente_b), em agente.{json,md}; só grava a noite completa e a frio
  python avaliar_fase5.py --incidente 28          a corrida 28, que não vale como medida, em resultados_alvo/fase5_incidente_28/agente.{json,md}
  python avaliar_fase5.py --sondagem --saida P    o veredito da sondagem do frio gravada na pasta P (é o fim do rodar_sondagem_frio.ps1)
  python avaliar_fase5.py --manual                a planilha da linha de base manual e o registro da sessão, em manual.{json,md}
  python avaliar_fase5.py --comparar              os dois lados na mesma tabela, em medicao.{json,md}
  python avaliar_fase5.py --situacao              quantas execuções da noite já estão gravadas (é o que o rodar_fase5.ps1 pergunta antes de chamar a corrida)

`--check` regera e compara com o que está gravado; `--colar` cola os blocos tb_f5_* no relatório da fase; `--pasta` troca a pasta dos derivados (uma corrida
que não é a noite completa só é lida com `--pasta`); `--saida` troca a pasta da corrida do agente; `--planilha` e `--sessao` trocam a planilha e o registro."""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import io
import json
import math
import random
import re
import sys
from datetime import datetime
from pathlib import Path

import analisar_fase3b as a3b
import avaliar
import avaliar_fase4 as av
import caminhos
import cenarios_fase4 as cen
import executar_bateria
import linha_de_base_manual as lbm
import pre_fase4 as pf
import progresso
import taxonomia

PASTA = caminhos.RESULTADOS / "fase5"
SAIDA_DO_AGENTE = "fase5_agente_b"               # a pasta da corrida 28b (rodar_fase5.ps1): a noite refeita com tudo fechado e a frio (decisões 145 e 146)
NOME_DA_CORRIDA = {"fase5_agente_b": "corrida 28b", "fase5_agente": "corrida 28, incidente", "fase4_ensaio_v4": "corrida 21d"}
# a corrida que rodou e não vale como a medida do agente: a pasta dos registros (que não é tocada), a pasta da leitura guardada e o prefixo dos blocos dela
INCIDENTES = {"28": {"saida": "fase5_agente", "pasta": "fase5_incidente_28", "prefixo": "tb_f5_incidente28_",
                     "motivo": ("A corrida 28, de 18/11/2026, foi lançada com o aplicativo Claude aberto, e o plano pede a corrida com o aplicativo Claude e o VS Code "
                                "fechados; o Eric decidiu refazer a noite (decisão 145). Nas repetições 2 a 5 dela, o Ollama reaproveitou o prompt lido na "
                                "repetição 1, e por isso a noite nova, a corrida 28b, roda a frio (decisão 146). Os números ficam como registro do incidente e não "
                                "entram na comparação com as pessoas.")}}
# a repetição vale a frio quando a primeira inferência dela não reaproveitou nenhum token e, no máximo, esta parcela dos tokens de entrada veio do que o Ollama
# tinha guardado; fixado em 18/11/2026, antes da corrida 28b: na corrida 28 a repetição 1 ficou em 12,6% e as repetições 2 a 5, em 91,7%
LIMITE_DA_PARCELA_EM_CACHE = 0.5
PREFIXO_DA_SONDAGEM = "fase5_sondagem_frio_"     # as pastas que o rodar_sondagem_frio.ps1 cria, uma por sondagem, com a data e a hora no nome
ARQUIVO_DA_SONDAGEM = "sondagem_frio.json"       # o veredito da sondagem, gravado na pasta dela
CORRIDA_DE_REFERENCIA = "fase4_ensaio_v4"        # a corrida 21d: o ensaio vigente dos dez cenários e o agente que a Fase 5 mede
PASTA_DA_SESSAO = caminhos.RESULTADOS / "fase5_manual"
REGISTRO_DA_SESSAO = "sessao.jsonl"              # o registro que linha_de_base_manual.py grava na sessão (protocolo versão 2, pacote F2)
RELATORIO = caminhos.AQUI.parent.parent.parent / "Documentacao" / "memorial" / "3-resultados-e-analises" / "fase-5-relatorio.md"
TIPOS = tuple(dict.fromkeys(c["tipo"] for c in cen.CENARIOS_DO_ENSAIO))   # contrato e localizador, na ordem do catálogo
REPETICOES = 5                                   # repetições do agente em cada cenário (projeto ABNT, seção 3.4)
INTEGRANTES = lbm.INTEGRANTES                    # três integrantes, cada um nos dez cenários (ficha 36, decisão 79)
# limite de 10 minutos por cenário (protocolo da linha de base manual, seção 6), que é também o piso da regra L6; quando o ajudante da sessão declara o limite
# (linha_de_base_manual.LIMITE_S, protocolo versão 2), vale o dele, para os dois arquivos não discordarem
LIMITE_S = float(getattr(lbm, "LIMITE_S", 600.0))
EMPATE_S = 5.0                                   # regra L8: diferença menor que 5 s, a folga do cronômetro das pessoas, conta como empate
FOLGA_S = 1.0                                    # seção 4.6: folga de 1 s entre `segundos` e o fim menos o início menos o desconto
ALFA = 0.05                                      # regras L9 e L11: o teste dos sinais separa os lados com p abaixo de 0,05
SEMENTE = av.SEMENTE_DA_REAMOSTRAGEM             # regra L7: a mesma semente das leituras da Fase 4
REAMOSTRAS = av.REAMOSTRAS
MARCA_ANULADA = "ANULADA"                        # regra L14: o facilitador começa as observações da linha com esta palavra
# seção 4.4: linha preenchida pelo cronômetro de reserva, quando a ferramenta falhou no cenário; a marca é a do ajudante da sessão (protocolo versão 2) e vale em
# qualquer ponto das observações
MARCA_A_MAO = getattr(lbm, "MARCA_A_MAO", "anotada à mão")
EVENTO_DO_CONFERIR = "tentativa"                 # o evento que `linha_de_base_manual.py conferir --vez --seletor` grava no registro da sessão (registro 2)
ITENS_QUE_PARAM = ("biblioteca", "prompt_fixo", "indice_da_busca", "k", "limiares", "navegador")
ITENS_QUE_INFORMAM = ("modelo", "top_logprobs", "teto_tokens", "playwright", "versao_do_caso_ao_vivo", "sinais_da_referencia_na_busca")
NOME_DO_ITEM = {"biblioteca": "biblioteca de produção (hash)", "prompt_fixo": "prompt fixo do diagnóstico (hash)", "indice_da_busca": "índice da busca (hash)",
                "k": "k (verbetes entregues ao modelo)", "limiares": "limiares do selo", "navegador": "versão do navegador", "modelo": "modelo",
                "top_logprobs": "alternativas por posição (top_logprobs)", "teto_tokens": "teto de tokens da resposta", "playwright": "Playwright",
                "versao_do_caso_ao_vivo": "versão do código do caso ao vivo", "sinais_da_referencia_na_busca": "busca com os sinais contra a referência"}


class LeituraRecusada(Exception):
    """A planilha da linha de base manual não pode ser lida como está; `recusas` diz por quê, linha a linha."""

    def __init__(self, recusas: list[str]) -> None:
        super().__init__("; ".join(recusas))
        self.recusas = list(recusas)


def _json(caminho: Path) -> dict | None:
    return json.loads(caminho.read_text(encoding="utf-8")) if caminho.exists() else None


def _media(valores: list) -> float | None:
    return sum(valores) / len(valores) if valores else None


def _r(v: float | None, casas: int = 2) -> float | None:
    return None if v is None else round(v, casas)


def _norm(texto: str | None) -> str:
    return avaliar._normalizar(texto or "").strip()


# ------------------------------------------------------------------ um lado da medição (regras L3 a L7)

# ! Alteração de IA - Revisar: (16/11/2026, F1) `medida` e `resumir_lado`: as medidas de um lado (as execuções do agente ou as tentativas das pessoas) viram a
# tabela por cenário, por tipo e no geral, com a mesma conta dos dois lados.
# ! Motivo: regras L3 a L6 do plano. Por cenário, a média de quem chegou ao fim do cronômetro, com o mínimo e o máximo; no geral e por tipo, a média das médias
# dos cenários, e não a média de todas as medidas, porque a unidade é o cenário (regra L2). A medida sem fim (execução sem `mttr_s`, tentativa que estourou os 10
# minutos) fica fora da média do tempo e dentro do Task Success, e entra com 600 s numa segunda conta, declarada como piso. Uma função só para os dois lados é o
# que garante a mesma régua (princípio 4 do plano).
def medida(cenario: str, tipo: str, quem, sucesso, tempo_s) -> dict:
    """Uma medida de um lado: o cenário, quem mediu (a repetição do agente ou o integrante), se teve Task Success e o tempo em segundos (None sem fim)."""
    return {"cenario": cenario, "tipo": tipo, "quem": quem, "sucesso": bool(sucesso), "tempo_s": None if tempo_s is None else float(tempo_s)}


def _cenarios_crus(medidas: list[dict]) -> list[dict]:
    """Por cenário do catálogo, na ordem dele: as contagens e as médias sem arredondar, que a média das médias e a reamostragem usam."""
    fora = sorted({m["cenario"] for m in medidas} - {c["id"] for c in cen.CENARIOS_DO_ENSAIO})
    if fora:
        raise ValueError(f"medida de cenário que não está nos dez do catálogo: {fora}")
    crus = []
    for c in cen.CENARIOS_DO_ENSAIO:
        mm = [m for m in medidas if m["cenario"] == c["id"]]
        tempos = [m["tempo_s"] for m in mm if m["tempo_s"] is not None]
        estritos = [m["tempo_s"] for m in mm if m["sucesso"] and m["tempo_s"] is not None]
        crus.append({"cenario": c["id"], "tipo": c["tipo"], "n": len(mm), "sucessos": sum(1 for m in mm if m["sucesso"]), "tempos": tempos, "tempo": _media(tempos),
                     "piso": _media([LIMITE_S if m["tempo_s"] is None else m["tempo_s"] for m in mm]), "estrita": _media(estritos), "estrita_n": len(estritos)})
    return crus


def reamostrar_por_tipo(valores_por_tipo: dict[str, list], n: int = REAMOSTRAS, semente: int = SEMENTE) -> tuple:
    """Regra L7: intervalo de 95% da média dos cenários por reamostragem (percentis 2,5 e 97,5), sorteando os cenários dentro de cada tipo, para a mistura de
    seis de contrato e quatro de localizador não mudar de uma reamostra para outra. Com um tipo só é a conta de avaliar_fase4.bootstrap_media. (None, None) sem
    valor nenhum e (v, v) com um só."""
    ordem = [t for t in TIPOS if t in valores_por_tipo] + sorted(t for t in valores_por_tipo if t not in TIPOS)
    grupos = [g for g in ([float(v) for v in valores_por_tipo[t] if v is not None] for t in ordem) if g]
    total = sum(len(g) for g in grupos)
    if total == 0:
        return (None, None)
    if total == 1:
        return (round(grupos[0][0], 2), round(grupos[0][0], 2))
    rng = random.Random(semente)
    medias = sorted(sum(rng.choice(g) for g in grupos for _ in g) / total for _ in range(n))
    return (round(medias[int(0.025 * (n - 1))], 2), round(medias[int(0.975 * (n - 1))], 2))


def _bloco(crus: list[dict]) -> dict:
    """O resumo de um conjunto de cenários (os dez, ou os de um tipo): Task Success com Wilson (regra L5), a média das médias do tempo com o intervalo da
    reamostragem por tipo (regras L3, L4 e L7), a segunda conta com 600 s (regra L6) e a leitura só com as medidas que tiveram Task Success (regra L13)."""
    n, sucessos = sum(c["n"] for c in crus), sum(c["sucessos"] for c in crus)
    lo, hi = avaliar.wilson(sucessos, n) if n else (None, None)
    com_fim = sum(len(c["tempos"]) for c in crus)

    def media_e_intervalo(chave: str) -> tuple:
        valores = [c[chave] for c in crus if c[chave] is not None]
        return _r(_media(valores)), len(valores), reamostrar_por_tipo({t: [c[chave] for c in crus if c["tipo"] == t] for t in TIPOS})

    tempo, com_tempo, ic = media_e_intervalo("tempo")
    piso, _, ic_piso = media_e_intervalo("piso")
    estrita, com_estrita, _ = media_e_intervalo("estrita")
    return {"n": n, "sucessos": sucessos, "task_success_pct": round(100 * sucessos / n, 1) if n else None, "wilson_lo_pct": lo, "wilson_hi_pct": hi,
            "cenarios": sum(1 for c in crus if c["n"]), "cenarios_com_todas_certas": sum(1 for c in crus if c["n"] and c["sucessos"] == c["n"]),
            "com_fim": com_fim, "sem_fim": n - com_fim, "cenarios_com_tempo": com_tempo, "tempo_media_s": tempo, "tempo_ic_lo_s": ic[0], "tempo_ic_hi_s": ic[1],
            "piso_media_s": piso, "piso_ic_lo_s": ic_piso[0], "piso_ic_hi_s": ic_piso[1], "estrita_cenarios": com_estrita, "estrita_media_s": estrita}


def resumir_lado(medidas: list[dict]) -> dict:
    """As medidas de um lado no geral, por tipo e por cenário (os dez do catálogo, na ordem dele, mesmo os sem medida)."""
    crus = _cenarios_crus(medidas)
    por_cenario = [{"cenario": c["cenario"], "tipo": c["tipo"], "n": c["n"], "sucessos": c["sucessos"],
                    "parcela_pct": round(100 * c["sucessos"] / c["n"], 1) if c["n"] else None, "todas_certas": bool(c["n"]) and c["sucessos"] == c["n"],
                    "com_fim": len(c["tempos"]), "sem_fim": c["n"] - len(c["tempos"]), "tempo_media_s": _r(c["tempo"], 3),
                    "tempo_min_s": min(c["tempos"]) if c["tempos"] else None, "tempo_max_s": max(c["tempos"]) if c["tempos"] else None,
                    "piso_media_s": _r(c["piso"], 3), "estrita_n": c["estrita_n"], "estrita_media_s": _r(c["estrita"], 3)} for c in crus]
    return {"geral": _bloco(crus), "por_tipo": [{"tipo": t, **_bloco([c for c in crus if c["tipo"] == t])} for t in TIPOS], "por_cenario": por_cenario}


# ------------------------------------------------------------------ a comparação dos dois lados (regras L8 a L12)

# ! Alteração de IA - Revisar: (16/11/2026, F1) a comparação do tempo: a direção de cada cenário (`direcao_do_tempo`), o teste exato dos sinais sobre os cenários
# (`teste_dos_sinais`, pela conta de `avaliar.mcnemar_exato`) e as três frases da regra L9 (`regra_l9`).
# ! Motivo: regras L8 e L9 do plano (ficha 74, decisão 132). A leitura só afirma que um lado repara mais rápido quando o intervalo de 95% da diferença média não
# contém zero e o teste dos sinais dá p abaixo de 0,05; com o zero dentro do intervalo, a diferença está dentro do ruído; com o intervalo sem o zero e o teste sem
# chegar a 0,05, a média pende para um lado e a leitura não dá veredito. As frases saem daqui para o relatório e o painel citarem o mesmo texto, sem ninguém
# redigir a conclusão depois de ver os números.
def direcao_do_tempo(agente_s: float | None, pessoas_s: float | None) -> str:
    """Quem foi mais rápido no cenário: `agente`, `pessoas`, `empate` (diferença das médias menor que 5 s) ou `sem_medida`. Cenário em que só um lado chegou
    ao fim conta para esse lado (regra L8)."""
    if agente_s is None and pessoas_s is None:
        return "sem_medida"
    if pessoas_s is None:
        return "agente"
    if agente_s is None:
        return "pessoas"
    diferenca = pessoas_s - agente_s
    if abs(diferenca) < EMPATE_S:
        return "empate"
    return "agente" if diferenca > 0 else "pessoas"


def teste_dos_sinais(direcoes: list[str]) -> dict:
    """Regra L8: o teste exato dos sinais, bicaudal, sobre os cenários, que é a conta binomial do McNemar exato do projeto: um lado para os cenários em que o
    agente foi mais rápido, o outro para os em que as pessoas foram; empate e cenário sem medida saem do teste."""
    b, c = direcoes.count("agente"), direcoes.count("pessoas")
    return {"agente": b, "pessoas": c, "empates": direcoes.count("empate"), "sem_medida": direcoes.count("sem_medida"), "p": avaliar.mcnemar_exato(b, c)}


def _s(v, casas: int = 1) -> str:
    return "n/d" if v is None else a3b.f(float(v), casas)


def _quantos(n: int, singular: str, plural: str) -> str:
    return f"nenhum {singular}" if n == 0 else (f"1 {singular}" if n == 1 else f"{n} {plural}")


def _contagem_dos_sinais(sinais: dict) -> str:
    return (f"{_quantos(sinais['agente'], 'cenário', 'cenários')} com o agente mais rápido, {_quantos(sinais['pessoas'], 'cenário', 'cenários')} com as pessoas "
            f"mais rápidas e {_quantos(sinais['empates'], 'empate', 'empates')}")


def regra_l9(diferenca_media: float | None, ic_lo: float | None, ic_hi: float | None, sinais: dict) -> dict:
    """A regra L9: `veredito` (um lado repara mais rápido), `ruido` (o intervalo contém zero), `pende` (o intervalo não contém zero, mas a direção não se repete
    em cenários suficientes) ou `sem_medida`. A diferença é o tempo das pessoas menos o MTTR do agente: positiva quando o agente foi mais rápido."""
    if diferenca_media is None or ic_lo is None or ic_hi is None:
        return {"caso": "sem_medida", "lado": None, "frase": "Nenhum cenário tem o tempo medido dos dois lados: a comparação do tempo não foi feita."}
    numeros = (f"a diferença média por cenário (tempo das pessoas menos MTTR do agente) foi de {_s(diferenca_media)} s, com intervalo de 95% de {_s(ic_lo)} a "
               f"{_s(ic_hi)} s")
    teste = f"o teste dos sinais deu p = {_s(sinais['p'], 4)} ({_contagem_dos_sinais(sinais)})"
    if ic_lo <= 0 <= ic_hi:
        return {"caso": "ruido", "lado": None, "frase": f"A diferença está dentro do ruído: {numeros}, que contém zero; {teste}."}
    lado = "agente" if ic_lo > 0 else "pessoas"
    maioria = "agente" if sinais["agente"] > sinais["pessoas"] else ("pessoas" if sinais["pessoas"] > sinais["agente"] else None)
    quem = "o agente" if lado == "agente" else "as pessoas"
    if sinais["p"] < ALFA and maioria == lado:
        afirma = "O agente reparou mais rápido que as pessoas" if lado == "agente" else "As pessoas repararam mais rápido que o agente"
        return {"caso": "veredito", "lado": lado, "frase": f"{afirma}: {numeros}, que não contém zero, e {teste}."}
    # o intervalo sem o zero e o teste sem chegar a 0,05, ou a maioria dos cenários do lado contrário ao da média: a direção da média não se repete nos cenários
    return {"caso": "pende", "lado": lado, "frase": (f"A média pende para {quem}, mas a direção não se repete em cenários suficientes: {numeros}, que não contém "
                                                    f"zero, e {teste}. A leitura não dá veredito.")}


def minimo_de_cenarios_para_veredito() -> int:
    """Regra L11: o menor número de cenários diferentes, todos na mesma direção, com que o teste dos sinais chega a p abaixo de 0,05."""
    n = 1
    while avaliar.mcnemar_exato(n, 0) >= ALFA:
        n += 1
    return n


def _comparacao_do_tempo(pares: list[dict]) -> dict:
    """A conta da regra L8 sobre uma lista de cenários ({tipo, agente_s, pessoas_s, medido}): a média das diferenças com o intervalo da reamostragem por
    tipo, a razão entre as duas médias e o teste dos sinais. Cenário sem um dos tempos fica fora da média das diferenças."""
    diferencas = {t: [p["pessoas_s"] - p["agente_s"] for p in pares if p["tipo"] == t and p["agente_s"] is not None and p["pessoas_s"] is not None] for t in TIPOS}
    todas = [d for t in TIPOS for d in diferencas[t]]
    lo, hi = reamostrar_por_tipo(diferencas)
    media_agente, media_pessoas = _media([p["agente_s"] for p in pares if p["agente_s"] is not None]), _media([p["pessoas_s"] for p in pares if p["pessoas_s"] is not None])
    sinais = teste_dos_sinais([direcao_do_tempo(p["agente_s"], p["pessoas_s"]) if p["medido"] else "sem_medida" for p in pares])
    return {"cenarios_com_os_dois_lados": len(todas), "diferenca_media_s": _r(_media(todas)), "ic_lo_s": lo, "ic_hi_s": hi,
            "razao_das_medias": _r(media_pessoas / media_agente) if media_agente and media_pessoas is not None else None, "sinais": sinais}


# ! Alteração de IA - Revisar: (16/11/2026, F1) a comparação do Task Success: os dois números com Wilson, a parcela por cenário e o teste dos sinais sobre os
# cenários em que as duas parcelas diferem.
# ! Motivo: regra L11 do plano. Com menos de seis cenários diferentes o teste não tem como chegar a 0,05 (cinco de cinco dá p = 0,0625); nesse caso a leitura diz
# que não há veredito e nem calcula o p, para o número não ser lido como resultado.
def _comparar_task_success(agente: dict, pessoas: dict) -> dict:
    do_agente, das_pessoas = {x["cenario"]: x for x in agente["por_cenario"]}, {x["cenario"]: x for x in pessoas["por_cenario"]}
    por_cenario = []
    for c in cen.CENARIOS_DO_ENSAIO:
        a, p = do_agente[c["id"]], das_pessoas[c["id"]]
        if not a["n"] or not p["n"]:
            direcao, diferenca = "sem_medida", None
        else:
            # as duas parcelas comparadas em inteiros (sucessos de um vezes medidas do outro), para 2 de 3 contra 4 de 6 dar igual
            cruzado = a["sucessos"] * p["n"] - p["sucessos"] * a["n"]
            direcao = "agente" if cruzado > 0 else ("pessoas" if cruzado < 0 else "igual")
            diferenca = round(100 * (a["sucessos"] / a["n"] - p["sucessos"] / p["n"]), 1)
        por_cenario.append({"cenario": c["id"], "tipo": c["tipo"], "agente_sucessos": a["sucessos"], "agente_n": a["n"], "agente_pct": a["parcela_pct"],
                            "pessoas_sucessos": p["sucessos"], "pessoas_n": p["n"], "pessoas_pct": p["parcela_pct"], "diferenca_pp": diferenca, "direcao": direcao})
    direcoes = [x["direcao"] for x in por_cenario]
    b, c_ = direcoes.count("agente"), direcoes.count("pessoas")
    minimo = minimo_de_cenarios_para_veredito()
    sinais = {"agente": b, "pessoas": c_, "iguais": direcoes.count("igual"), "sem_medida": direcoes.count("sem_medida"), "p": None}
    contagem = (f"{_quantos(b, 'cenário', 'cenários')} com a parcela do agente maior, {_quantos(c_, 'cenário', 'cenários')} com a das pessoas maior e "
                f"{_quantos(sinais['iguais'], 'cenário igual', 'cenários iguais')}")
    if sinais["sem_medida"] == len(direcoes):
        caso, lado, frase = "sem_medida", None, "Nenhum cenário tem o Task Success medido dos dois lados: a comparação não foi feita."
    elif b + c_ < minimo:
        caso, lado = "sem_veredito", None
        frase = (f"O Task Success dos dois lados não tem veredito: {contagem}; com menos de {minimo} cenários diferentes o teste dos sinais não tem como chegar "
                 f"a {_s(ALFA, 2)}.")
    else:
        sinais["p"] = avaliar.mcnemar_exato(b, c_)
        if sinais["p"] < ALFA:
            caso, lado = "veredito", "agente" if b > c_ else "pessoas"
            afirma = "O agente resolveu mais cenários que as pessoas" if lado == "agente" else "As pessoas resolveram mais cenários que o agente"
            frase = f"{afirma}: {contagem}; o teste dos sinais deu p = {_s(sinais['p'], 4)}."
        else:
            caso, lado = "sem_diferenca", None
            frase = f"O Task Success dos dois lados não se separa: {contagem}; o teste dos sinais deu p = {_s(sinais['p'], 4)}, sem chegar a {_s(ALFA, 2)}."
    chaves = ("n", "sucessos", "task_success_pct", "wilson_lo_pct", "wilson_hi_pct", "cenarios", "cenarios_com_todas_certas")
    return {"agente": {k: agente["geral"][k] for k in chaves}, "pessoas": {k: pessoas["geral"][k] for k in chaves}, "por_cenario": por_cenario, "sinais": sinais,
            "minimo_para_veredito": minimo, "caso": caso, "lado": lado, "frase": frase}


# ! Alteração de IA - Revisar: (16/11/2026, F1) `comparar`: os dois lados na mesma tabela, por cenário, no geral e por tipo, com a segunda conta de 600 s e o que
# é só descrição.
# ! Motivo: regras L8 a L13 do plano. Por cenário, a diferença e a razão entre o tempo das pessoas e o MTTR do agente, a faixa de cada lado e se elas se cruzam
# (L12); no geral, a regra L9; por tipo, os números sem veredito (L10: com seis cenários o teste só chega a 0,05 com os seis na mesma direção, e com quatro nunca
# chega); a segunda conta, em que a medida sem fim entra com 600 s dos dois lados (L6), traz o que a regra L9 daria, sem ser o veredito da leitura.
def comparar(agente: dict, pessoas: dict) -> dict:
    """A comparação entre dois lados já resumidos por `resumir_lado`."""
    do_agente, das_pessoas = {x["cenario"]: x for x in agente["por_cenario"]}, {x["cenario"]: x for x in pessoas["por_cenario"]}
    por_cenario, pares, pares_do_piso, linhas_do_piso = [], [], [], []
    for c in cen.CENARIOS_DO_ENSAIO:
        a, p = do_agente[c["id"]], das_pessoas[c["id"]]
        ta, tp, medido = a["tempo_media_s"], p["tempo_media_s"], bool(a["n"] and p["n"])
        faixas = [a["tempo_min_s"], a["tempo_max_s"], p["tempo_min_s"], p["tempo_max_s"]]
        por_cenario.append({"cenario": c["id"], "tipo": c["tipo"], "agente_media_s": ta, "agente_min_s": faixas[0], "agente_max_s": faixas[1], "agente_com_fim": a["com_fim"],
                            "pessoas_media_s": tp, "pessoas_min_s": faixas[2], "pessoas_max_s": faixas[3], "pessoas_com_fim": p["com_fim"],
                            "diferenca_s": _r(tp - ta) if ta is not None and tp is not None else None, "razao": _r(tp / ta) if ta and tp is not None else None,
                            "direcao": direcao_do_tempo(ta, tp) if medido else "sem_medida",
                            "faixas_se_cruzam": None if None in faixas else not (faixas[1] < faixas[2] or faixas[3] < faixas[0])})
        pares.append({"tipo": c["tipo"], "agente_s": ta, "pessoas_s": tp, "medido": medido})
        pa, pp = a["piso_media_s"], p["piso_media_s"]
        pares_do_piso.append({"tipo": c["tipo"], "agente_s": pa, "pessoas_s": pp, "medido": medido})
        linhas_do_piso.append({"cenario": c["id"], "tipo": c["tipo"], "agente_s": pa, "pessoas_s": pp, "diferenca_s": _r(pp - pa) if pa is not None and pp is not None else None})
    geral = _comparacao_do_tempo(pares)
    geral.update(regra_l9(geral["diferenca_media_s"], geral["ic_lo_s"], geral["ic_hi_s"], geral["sinais"]))
    por_tipo = []
    for t in TIPOS:
        x = _comparacao_do_tempo([p for p in pares if p["tipo"] == t])
        s = x.pop("sinais")
        por_tipo.append({"tipo": t, **x, "agente_mais_rapido": s["agente"], "pessoas_mais_rapidas": s["pessoas"], "empates": s["empates"], "sem_medida": s["sem_medida"]})
    contas = [(sum(1 for c in cen.CENARIOS_DO_ENSAIO if c["tipo"] == t), t) for t in TIPOS]
    nota = ("Por tipo de cenário a leitura mostra os números e fica sem veredito (regra L10): "
            + " e ".join(f"com {n} cenários de {t} o menor p que o teste dos sinais alcança é {_s(avaliar.mcnemar_exato(n, 0), 4)}, com os {n} na mesma direção"
                         for n, t in contas) + f"; o veredito pede p abaixo de {_s(ALFA, 2)}.")
    piso = _comparacao_do_tempo(pares_do_piso)
    veredito_do_piso = regra_l9(piso["diferenca_media_s"], piso["ic_lo_s"], piso["ic_hi_s"], piso["sinais"])
    piso.update({"o_que_a_regra_l9_daria": veredito_do_piso["caso"], "lado": veredito_do_piso["lado"], "por_cenario": linhas_do_piso})
    ea, ep = agente["geral"]["estrita_media_s"], pessoas["geral"]["estrita_media_s"]
    estrita = {"agente_media_s": ea, "agente_cenarios": agente["geral"]["estrita_cenarios"], "pessoas_media_s": ep, "pessoas_cenarios": pessoas["geral"]["estrita_cenarios"],
               "diferenca_s": _r(ep - ea) if ea is not None and ep is not None else None}
    return {"tempo": {"por_cenario": por_cenario, "geral": geral, "por_tipo": por_tipo, "nota_por_tipo": nota, "piso": piso, "estrita": estrita},
            "task_success": _comparar_task_success(agente, pessoas)}


# ------------------------------------------------------------------ a leitura do agente (corrida 28)

def ler_agente(saida: str) -> dict:
    """Os registros da corrida do agente: o último de cada cenário e repetição em cenarios.jsonl, as condições, as versões do Ollama gravadas nos diagnósticos,
    o log e o que identifica o agente da corrida 21d."""
    raiz = caminhos.RESULTADOS / saida
    ultimos: dict = {}
    for r in executar_bateria.ler_jsonl(raiz / "cenarios.jsonl"):
        ultimos[(r["cenario"], r["repeticao"])] = r
    diagnosticos = [r for arq in sorted(raiz.glob("*/diagnosticos__cenarios.jsonl")) for r in executar_bateria.ler_jsonl(arq)]
    log = (raiz / "fase4.log").read_text(encoding="utf-8-sig", errors="replace") if (raiz / "fase4.log").exists() else ""
    return {"registros": list(ultimos.values()), "condicoes": _json(raiz / "condicoes_fase4.json") or {}, "log": log,
            "versoes_ollama": sorted({r["versao_ollama"] for r in diagnosticos if r.get("versao_ollama")}), "referencia": ler_referencia(),
            "medidas": executar_bateria.ler_jsonl(raiz / progresso.NOME_DAS_MEDIDAS)}


# ! Alteração de IA - Revisar: (16/11/2026, F1) `execucoes_que_faltam` e `situacao_da_noite`: quantas das 50 execuções da noite já estão gravadas e se ela está
# completa. É o que `--situacao` imprime para o lançador, uma linha chave=valor por dado.
# ! Motivo: a primeira noite completa é a que vale (plano, princípio 3). Com as 50 execuções gravadas, relançar o `rodar_fase5.ps1` não pode chamar a corrida de
# novo: o executor regravaria `condicoes_fase4.json` da pasta da noite com a data e a versão do Ollama do relançamento, como aconteceu no relançamento da corrida
# 25 em 16/11/2026. A mesma conta diz à leitura `--agente` se ela pode gravar em `resultados_alvo/fase5`.
def execucoes_que_faltam(registros: list[dict]) -> list[str]:
    """As execuções da noite (cenário#repetição, na ordem do catálogo) que ainda não estão nos registros."""
    feitas = {f"{r['cenario']}#{r['repeticao']}" for r in registros}
    return [f"{c['id']}#{rep}" for c in cen.CENARIOS_DO_ENSAIO for rep in range(1, REPETICOES + 1) if f"{c['id']}#{rep}" not in feitas]


def situacao_da_noite(registros: list[dict], condicoes: dict | None = None) -> dict:
    """Execuções gravadas, execuções esperadas (dez cenários com cinco repetições) e se a noite está completa: nenhuma falta, nenhuma sobra e a corrida não é
    parcial."""
    esperadas = len(cen.CENARIOS_DO_ENSAIO) * REPETICOES
    return {"execucoes": len(registros), "esperadas": esperadas,
            "completa": not execucoes_que_faltam(registros) and len(registros) == esperadas and not (condicoes or {}).get("parcial")}


def repeticoes_completas(registros: list[dict]) -> int:
    """Quantas repetições, contando da primeira, já têm os dez cenários gravados: é por onde o lançador retoma, uma repetição por vez."""
    feitas = {(r["cenario"], r["repeticao"]) for r in registros}
    n = 0
    while n < REPETICOES and all((c["id"], n + 1) in feitas for c in cen.CENARIOS_DO_ENSAIO):
        n += 1
    return n


def _quando(texto) -> datetime | None:
    try:
        return datetime.fromisoformat(texto)
    except (TypeError, ValueError):
        return None


def _lista_e(numeros: list[int]) -> str:
    textos = [str(n) for n in numeros]
    return textos[0] if len(textos) == 1 else ", ".join(textos[:-1]) + " e " + textos[-1]


# ! Alteração de IA - Revisar: (18/11/2026, corrida 28b, decisão 146) `conferir_frio`: por repetição, quantos tokens de entrada vieram do que o Ollama tinha guardado
# (`medido.tokens_em_cache` do registro da barra de progresso) e se a repetição rodou a frio. A repetição é a frio quando a primeira inferência dela não
# reaproveitou nenhum token e, no máximo, metade dos tokens de entrada da repetição veio guardada.
# ! Motivo: na corrida 28 o Ollama reaproveitou nas repetições 2 a 5 o prompt lido na repetição 1: a primeira inferência da repetição 2 veio com 1217 dos 1218
# tokens guardados, e a repetição inteira com 10975 de 11966, contra 1505 de 11966 na repetição 1. Com o modelo descarregado antes da repetição, o Ollama começa
# sem nada guardado, e a primeira inferência não tem o que reaproveitar; dentro da repetição, só o começo do prompt que os cenários dividem vem guardado de um
# para o outro, como na repetição 1 da corrida 28 e na corrida 21d. O registro do localizador não traz o número da repetição, então cada inferência entra na
# repetição pela hora em que terminou (`concluido_em`), entre a primeira detecção daquela repetição e a primeira da seguinte (`deteccao` em cenarios.jsonl).
# Sem o registro numa repetição, ou sem o número de tokens guardados, a leitura não afirma que a noite foi a frio.
def conferir_frio(medidas: list[dict], registros: list[dict]) -> dict:
    """A conferência de que a noite rodou a frio: `a_frio` (True, False ou None quando não dá para dizer), o `motivo` quando não é True e a tabela por
    repetição."""
    inicios: dict[int, datetime] = {}
    for r in registros:
        t = _quando(r.get("deteccao"))
        if t is not None:
            inicios[r["repeticao"]] = min(t, inicios.get(r["repeticao"], t))
    ordem = sorted(inicios)
    por_repeticao = []
    for i, rep in enumerate(ordem):
        ate = inicios[ordem[i + 1]] if i + 1 < len(ordem) else None
        da_repeticao = [m for m in medidas if (t := _quando(m.get("concluido_em"))) is not None and t >= inicios[rep] and (ate is None or t < ate)]
        medidos = [m.get("medido") or {} for m in da_repeticao]
        guardados = [m.get("tokens_em_cache") for m in medidos]
        entrada = sum(m.get("tokens_entrada") or 0 for m in medidos)
        conhecido = bool(medidos) and entrada > 0 and all(isinstance(g, (int, float)) for g in guardados)
        parcela = sum(guardados) / entrada if conhecido else None
        por_repeticao.append({"repeticao": rep, "inferencias": len(medidos), "tokens_entrada": entrada or None, "tokens_em_cache": sum(guardados) if conhecido else None,
                              "parcela_em_cache_pct": round(100 * parcela, 1) if conhecido else None, "cache_na_primeira_inferencia": guardados[0] if guardados else None,
                              "prefill_s": round(sum(m.get("prefill_s") or 0.0 for m in medidos), 1) if medidos else None,
                              "carga_s": round(sum(m.get("carga_s") or 0.0 for m in medidos), 1) if medidos else None,
                              "a_frio": (guardados[0] == 0 and parcela <= LIMITE_DA_PARCELA_EM_CACHE) if conhecido else None})
    quentes = [x["repeticao"] for x in por_repeticao if x["a_frio"] is False]
    sem_medida = [n for n in range(1, REPETICOES + 1) if not any(x["repeticao"] == n and x["a_frio"] is not None for x in por_repeticao)]
    if quentes:
        a_frio = False
        motivo = (f"{'a repetição' if len(quentes) == 1 else 'as repetições'} {_lista_e(quentes)} não {'rodou' if len(quentes) == 1 else 'rodaram'} a frio: a primeira "
                  f"inferência já veio com tokens guardados pelo Ollama, ou mais de {100 * LIMITE_DA_PARCELA_EM_CACHE:.0f}% dos tokens de entrada da repetição vieram guardados")
    elif sem_medida:
        a_frio = None
        motivo = (f"sem medida do registro da barra de progresso ({progresso.NOME_DAS_MEDIDAS}) {'na repetição' if len(sem_medida) == 1 else 'nas repetições'} "
                  f"{_lista_e(sem_medida)}: não dá para dizer se a noite foi a frio")
    else:
        a_frio, motivo = True, None
    return {"a_frio": a_frio, "motivo": motivo, "por_repeticao": por_repeticao}


# ! Alteração de IA - Revisar: (18/11/2026, corrida 28b, decisão 146) `sondagem_do_frio` e `ultima_sondagem`: o veredito da sondagem que o Eric roda antes da noite
# (`rodar_sondagem_frio.ps1`: duas inferências do mesmo cenário, com o modelo descarregado entre elas) e a última sondagem gravada, que o lançador da noite consulta.
# ! Motivo: a noite a frio só mede o que se quer se descarregar o modelo apagar o prompt que o Ollama guardou. A corrida 28 mostrou o contrário disso com o modelo
# carregado (a segunda inferência de `contrato-malformed_json` veio com 1217 dos 1218 tokens guardados); o que ainda não foi visto é a inferência logo depois de
# o modelo sair da memória. A sondagem passa quando nenhuma das inferências reaproveitou token; se não passar, a noite não roda.
def _cenario_da_etapa(etapa: str | None) -> str:
    achado = re.match(r"[^#@\s]+", etapa or "")
    return achado.group(0) if achado else ""


def sondagem_do_frio(medidas: list[dict]) -> dict:
    """O veredito da sondagem, pelas medidas da barra de progresso gravadas na pasta dela: `passou`, a `frase` que diz por quê e as inferências lidas."""
    inferencias = [{"etapa": m.get("etapa"), "cenario": _cenario_da_etapa(m.get("etapa")), "concluido_em": m.get("concluido_em"),
                    **{k: (m.get("medido") or {}).get(k) for k in ("tokens_entrada", "tokens_em_cache", "prefill_s", "carga_s")}} for m in medidas]
    cenarios = sorted({i["cenario"] for i in inferencias})
    base = {"cenario": cenarios[0] if len(cenarios) == 1 else None, "inferencias": inferencias}
    if len(inferencias) < 2:
        return {**base, "passou": False, "frase": (f"A sondagem pede duas inferências do mesmo cenário, com o modelo descarregado entre elas, e o registro tem "
                                                    f"{len(inferencias)}.")}
    if len(cenarios) != 1:
        return {**base, "passou": False, "frase": f"As inferências da sondagem são de cenários diferentes ({', '.join(cenarios)}): ela pede o mesmo cenário duas vezes."}
    if any(not isinstance(i["tokens_em_cache"], (int, float)) or not i["tokens_entrada"] for i in inferencias):
        return {**base, "passou": False, "frase": "O Ollama não disse quantos tokens de entrada vieram do que ele tinha guardado: a sondagem não tem como passar."}
    quentes = [(n, i) for n, i in enumerate(inferencias, 1) if i["tokens_em_cache"] > 0]
    if quentes:
        n, i = quentes[0]
        return {**base, "passou": False, "frase": (f"Descarregar o modelo não apagou o prompt guardado: na inferência de número {n}, {i['tokens_em_cache']} dos "
                                                    f"{i['tokens_entrada']} tokens de entrada vieram do que o Ollama tinha guardado (leitura do prompt em "
                                                    f"{_s(i['prefill_s'], 3)} s). A noite não roda assim.")}
    primeira, ultima = inferencias[0], inferencias[-1]
    return {**base, "passou": True, "frase": (f"Depois de o modelo ser descarregado, a inferência seguinte leu o prompt de novo: nenhum dos {ultima['tokens_entrada']} "
                                               f"tokens de entrada veio do que o Ollama tinha guardado (leitura do prompt em {_s(ultima['prefill_s'], 3)} s; na primeira "
                                               f"inferência, {_s(primeira['prefill_s'], 3)} s).")}


def ultima_sondagem(raiz: Path) -> dict | None:
    """A sondagem do frio mais recente que chegou ao veredito, entre as pastas `fase5_sondagem_frio_<data>_<hora>` de `raiz`; None se não há nenhuma."""
    for pasta in sorted((p for p in raiz.glob(PREFIXO_DA_SONDAGEM + "*") if p.is_dir()), key=lambda p: p.name, reverse=True):
        gravado = _json(pasta / ARQUIVO_DA_SONDAGEM)
        if gravado is not None:
            return {"pasta": pasta.name, "passou": bool(gravado.get("passou")), "versoes_ollama": list(gravado.get("versoes_ollama") or [])}
    return None


# ! Alteração de IA - Revisar: (16/11/2026, F1) `resumir_agente`: a leitura da corrida 28 pela regra do cenário como unidade, com a conferência da noite (as 50
# execuções, uma versão do Ollama e uma do navegador, o mesmo hash do banco no começo das repetições, a linha FIM no log) e a comparação do que identifica o
# agente com o que a corrida 21d gravou.
# ! Motivo: regras L3, L5, L6, L7 e L13 do plano e a verificação da seção 14, item 3. Do lado do agente nenhuma execução é anulada (regra L14): a que falhou
# aparece como falhou, com o rótulo do diagnóstico e a falha da cura. A conferência do agente repete, com o que a corrida gravou, a etapa `--antes` do lançador:
# assim a leitura diz por si se o que foi medido é o agente da 21d.
def resumir_agente(bruto: dict, corrida: str | None = None, gerado_em: str | None = None, incidente: str | None = None) -> dict:
    ordem = {c["id"]: i for i, c in enumerate(cen.CENARIOS_DO_ENSAIO)}
    cond = bruto.get("condicoes") or {}
    regs = sorted(bruto["registros"], key=lambda r: (ordem.get(r["cenario"], len(ordem)), r["repeticao"]))
    lado = resumir_lado([medida(r["cenario"], r["tipo"], r["repeticao"], r.get("task_success"), r.get("mttr_s")) for r in regs])
    medias_do_total = []
    for linha in lado["por_cenario"]:
        do_cenario = [r for r in regs if r["cenario"] == linha["cenario"]]
        segundos = [r["segundos"] for r in do_cenario if r.get("segundos") is not None]
        linha["rotulos"] = [r.get("rotulo") or "sem diagnóstico" for r in do_cenario]
        linha["segundos_media_s"] = _r(_media(segundos), 3)
        if segundos:
            medias_do_total.append(_media(segundos))
    faltam = execucoes_que_faltam(regs)
    navegadores = sorted({r["navegador"] for r in regs if r.get("navegador")})
    hashes = sorted({r["hash_inicio"] for r in regs if r.get("hash_inicio")})
    fins = re.findall(r"FIM cenarios: [^\r\n]*", bruto.get("log") or "")
    noite = {**situacao_da_noite(regs, cond), "faltam": faltam,
             "versoes_ollama": bruto.get("versoes_ollama") or [], "navegador": {"versoes": navegadores, "unica": len(navegadores) <= 1},
             "banco": {"hashes_de_inicio": hashes, "unico": len(hashes) <= 1}, "linha_fim_no_log": bool(fins), "ultima_linha_fim": fins[-1].strip() if fins else None}
    # (18/11/2026, decisão 146) a conferência de que cada repetição leu o prompt de novo; `incidente` diz por que a corrida não vale como a medida, quando é o caso
    frio = conferir_frio(bruto.get("medidas") or [], regs)
    noite.update({"a_frio": frio["a_frio"], "frio": {"limite_da_parcela_em_cache": LIMITE_DA_PARCELA_EM_CACHE, "motivo": frio["motivo"], "por_repeticao": frio["por_repeticao"]}})
    todos_os_segundos = [r["segundos"] for r in regs if r.get("segundos") is not None]
    sem = [{"cenario": r["cenario"], "repeticao": r["repeticao"], "tipo": r["tipo"], "detectou": bool(r.get("detectou")), "rotulo": r.get("rotulo"),
            "causa_esperada": r.get("causa_esperada"), "falha_da_cura": (r.get("cura") or {}).get("falha"), "mttr_s": r.get("mttr_s"), "segundos": r.get("segundos")}
           for r in regs if not r.get("task_success")]
    referencia = bruto.get("referencia")
    return {"metadados": {"gerado_em": gerado_em or datetime.now().isoformat(timespec="seconds"), "corrida": corrida,
                          **({"gerado_por": "avaliar_fase5.py --incidente", "incidente": incidente} if incidente else {"gerado_por": "avaliar_fase5.py --agente"})},
            "condicoes": {**{k: cond.get(k) for k in ("modelo", "versao_ollama", "k", "repeticoes", "parcial", "execucoes")}, "biblioteca": (cond.get("biblioteca") or {}).get("hash")},
            "noite": noite, "mesmo_agente_da_21d": comparar_identidade(identidade_das_condicoes(cond, regs), referencia) if referencia and cond else [],
            **lado, "tempo_total": {"segundos_media_s": _r(_media(medias_do_total)), "segundos_total_s": _r(sum(todos_os_segundos), 1) if todos_os_segundos else None},
            "sem_task_success": sem}


# ------------------------------------------------------------------ o agente de hoje é o da corrida 21d? (etapa 2 do lançador)

# ! Alteração de IA - Revisar: (16/11/2026, F1) o que identifica o agente: lido das condições que uma corrida gravou (`identidade_das_condicoes`), montado hoje
# como o executor monta, sem chamar o modelo (`identidade_de_hoje`), e comparado item a item (`comparar_identidade`).
# ! Motivo: plano, princípio 2 e seção 3.4, etapa 2: a noite só roda se a biblioteca de produção, o prompt fixo, o índice da busca, o k, os limiares e a versão do
# navegador de hoje forem os de `resultados_alvo/fase4_ensaio_v4/condicoes_fase4.json`. Esses seis param a noite. Os outros itens aparecem na tabela e não param,
# porque o plano não os lista: a versão do código do caso ao vivo passou de 4 a 5 depois da 21d (o teto nas listas da decisão 99, que não muda nenhum prompt das
# corridas 18d e 21d), e parar por ela impediria a noite sem que o agente tenha mudado. Dos limiares sai a data em que o arquivo foi gravado, que não é do agente.
def identidade_das_condicoes(cond: dict, registros: list[dict] | None = None) -> dict:
    """O que identifica o agente numa corrida: de condicoes_fase4.json e, para o navegador, da versão gravada em cada execução de cenarios.jsonl."""
    navegadores = sorted({r["navegador"] for r in registros or [] if r.get("navegador")})
    limiares, versoes = cond.get("limiares"), cond.get("versoes") or {}
    return {"biblioteca": (cond.get("biblioteca") or {}).get("hash"), "prompt_fixo": cond.get("hash_prompt_fixo"), "indice_da_busca": cond.get("hash_indice"), "k": cond.get("k"),
            "limiares": {k: v for k, v in limiares.items() if k != "gravado_em"} if isinstance(limiares, dict) else None,
            "navegador": ", ".join(navegadores) if navegadores else versoes.get("navegador"), "modelo": cond.get("modelo"), "top_logprobs": cond.get("top_logprobs"),
            "teto_tokens": cond.get("teto_tokens"), "playwright": versoes.get("playwright"), "versao_do_caso_ao_vivo": cond.get("versao_do_caso_ao_vivo"),
            "sinais_da_referencia_na_busca": cond.get("sinais_da_referencia_na_busca")}


def ler_referencia() -> dict | None:
    """O que identifica o agente da corrida 21d; None se a pasta dela não tiver as condições."""
    raiz = caminhos.RESULTADOS / CORRIDA_DE_REFERENCIA
    cond = _json(raiz / "condicoes_fase4.json")
    return None if cond is None else identidade_das_condicoes(cond, executar_bateria.ler_jsonl(raiz / "cenarios.jsonl"))


def versao_do_navegador(canal: str = "chromium") -> str | None:
    """A versão do navegador que a corrida vai abrir, lida do próprio navegador como o executor lê; None quando ele não abre (sem o Playwright, que só está na
    venv do AgenteCore, ou sem o Chromium baixado)."""
    try:
        import navegador
        with navegador.Navegador(canal=canal) as nav:
            return nav.versao()["navegador"]
    except Exception as e:  # noqa: BLE001 - sem navegador a conferência não passa; o motivo vai para a tela
        print(f"!! não consegui abrir o navegador para ler a versão ({type(e).__name__}: {str(e).splitlines()[0] if str(e) else 'sem mensagem'})")
        return None


def identidade_de_hoje(ler_navegador=versao_do_navegador) -> dict:
    """O que identifica o agente no código e nos arquivos de hoje, montado como `executar_fase4.py --modo cenarios` monta antes de rodar: a biblioteca de
    produção pelo hash, o índice da busca e o prompt fixo sobre o primeiro caso de avaliação, o k e os limiares de limiares.json. Não chama o modelo."""
    import importlib.metadata

    import biblioteca as bib
    import caso_ao_vivo as cv
    import diagnostico_ao_vivo as dv
    import evolucao_biblioteca as evo
    import executar_fase4 as ex
    import recuperacao as rec
    limiares = dv.carregar_limiares()
    k = int((limiares or {}).get("k") or 3)
    verbetes = bib.carregar(dv.PASTA_CURADA)
    indice = rec.Indice(verbetes)
    exemplo = ex.fixture_sem_gabarito(ex.casos_de_avaliacao("avaliacao")[0])
    contexto, prompt = dv.montar_prompt(verbetes, indice, exemplo, k)
    try:
        playwright = importlib.metadata.version("playwright")
    except importlib.metadata.PackageNotFoundError:
        playwright = None
    return {"biblioteca": evo.hash_biblioteca(dv.PASTA_CURADA), "prompt_fixo": dv.hash_prompt_fixo(verbetes, contexto, exemplo, prompt), "indice_da_busca": dv.hash_indice(indice),
            "k": k, "limiares": {a: b for a, b in limiares.items() if a != "gravado_em"} if isinstance(limiares, dict) else None, "navegador": ler_navegador(),
            "modelo": ex.MODELO_PADRAO, "top_logprobs": dv.TOP_LOGPROBS, "teto_tokens": dv.TETO_TOKENS, "playwright": playwright,
            "versao_do_caso_ao_vivo": cv.VERSAO_DO_CASO, "sinais_da_referencia_na_busca": cv.SINAIS_DA_REFERENCIA_NA_BUSCA}


def _curto(valor) -> str | int | bool | None:
    """O valor de um item como cabe numa célula: os limiares viram os dois cortes, o k e um hash curto do conteúdo inteiro."""
    if isinstance(valor, dict):
        resumo = hashlib.sha256(json.dumps(valor, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()[:8]
        return f"baixo até {_s(valor.get('baixo_ate'), 4)}, alto a partir de {_s(valor.get('alto_a_partir_de'), 4)}, k {valor.get('k')} (conteúdo {resumo})"
    return valor


def comparar_identidade(hoje: dict, referencia: dict) -> list[dict]:
    """Item a item, o agente de um lado contra o da corrida 21d. `para` diz se a diferença no item para a noite (os seis do plano); item que falta de um dos
    lados conta como diferente."""
    itens = []
    for item in ITENS_QUE_PARAM + ITENS_QUE_INFORMAM:
        a, b, para = hoje.get(item), referencia.get(item), item in ITENS_QUE_PARAM
        itens.append({"item": item, "nome": NOME_DO_ITEM[item], "hoje": _curto(a), "na_21d": _curto(b), "igual": a == b and (a is not None or not para), "para": para})
    return itens


def o_que_difere(itens: list[dict]) -> list[str]:
    """Os itens que param a noite e não batem com a corrida 21d."""
    return [i["item"] for i in itens if i["para"] and not i["igual"]]


def _tabela_da_identidade(itens: list[dict]) -> list[str]:
    linhas = [f"  {'igual ' if i['igual'] else 'DIFERE'}  {i['nome']}: hoje {i['hoje']!r}; na corrida 21d {i['na_21d']!r}" + ("" if i["para"] else "  (só informa)") for i in itens]
    return linhas


# ------------------------------------------------------------------ o custo da noite (seção 3.2 do plano)

def ler_custo(saida: str = CORRIDA_DE_REFERENCIA) -> dict:
    """Os registros de onde sai o tempo da noite: as execuções e o log da corrida 21d e a linha FIM do log das três últimas pontes de pontes.json."""
    raiz = caminhos.RESULTADOS / saida
    ultimos: dict = {}
    for r in executar_bateria.ler_jsonl(raiz / "cenarios.jsonl"):
        ultimos[(r["cenario"], r["repeticao"])] = r
    pontes = []
    for p in reversed((_json(caminhos.RESULTADOS / "fase4" / "pontes.json") or {}).get("pontes") or []):
        arq = caminhos.RESULTADOS / p["corrida"] / "fase3b.log"
        fins = re.findall(r"FIM da Fase 3-B \(ponte\) - duracao total (\d\d)h(\d\d)", arq.read_text(encoding="utf-8-sig", errors="replace")) if arq.exists() else []
        if fins:
            pontes.append({"corrida": p["corrida"], "versao": p.get("versao"), "data": p.get("data"), "minutos": int(fins[-1][0]) * 60 + int(fins[-1][1])})
        if len(pontes) == 3:
            break
    return {"saida": saida, "registros": list(ultimos.values()), "log": (raiz / "fase4.log").read_text(encoding="utf-8-sig", errors="replace"), "pontes": pontes[::-1]}


# ! Alteração de IA - Revisar: (16/11/2026, F1) `resumir_custo`: o tempo de máquina da noite medida, pelas duas contas da seção 3.2 do plano, com a ponte à parte.
# ! Motivo: o plano citava esses números a partir de um rascunho da sessão de planejamento; aqui eles saem de script com `--check`, e o lançador `rodar_fase5.ps1`
# lê os minutos deste arquivo para anunciar a duração, em vez de trazer um número escrito. A conta de baixo multiplica o tempo médio de uma execução por 50; a de
# cima multiplica o tempo do executor inteiro por cinco, o que inclui o que ele gasta fora das execuções (subir as cobaias, restaurar o banco, as referências), e
# soma o que o `rodar_fase4.ps1` gastou fora do executor na 21d (a bateria de testes e a leitura). A ponte só roda se o Ollama tiver mudado de versão.
def resumir_custo(bruto: dict, gerado_em: str | None = None) -> dict:
    regs, log = bruto["registros"], bruto["log"]
    segundos = [r["segundos"] for r in regs if r.get("segundos") is not None]
    repeticoes_na_referencia = max((r["repeticao"] for r in regs), default=1)
    executor = int(re.findall(r"FIM cenarios:[^\r\n]*?duração (\d+) s", log)[-1])
    marcas = [datetime.strptime(m, "%Y-%m-%d %H:%M:%S") for m in re.findall(r"^\[(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d)\]", log, re.M)]
    fora = int((marcas[-1] - marcas[0]).total_seconds()) - executor
    execucoes = len(cen.CENARIOS_DO_ENSAIO) * REPETICOES
    noite_s = REPETICOES * executor / repeticoes_na_referencia + fora
    minutos_das_pontes = [p["minutos"] for p in bruto["pontes"]]
    sem_ponte = math.ceil(noite_s / 60)
    resumo = {"cenarios": len(cen.CENARIOS_DO_ENSAIO), "repeticoes": REPETICOES, "execucoes": execucoes, "execucoes_na_21d": len(regs),
              "segundos_por_execucao_na_21d": _r(_media(segundos), 1), "segundos_do_executor_na_21d": executor, "segundos_fora_do_executor_na_21d": fora,
              "horas_pelas_execucoes": round(execucoes * _media(segundos) / 3600, 2), "horas_pelo_executor": round(REPETICOES * executor / repeticoes_na_referencia / 3600, 2),
              "ponte_minutos_min": min(minutos_das_pontes) if minutos_das_pontes else None, "ponte_minutos_max": max(minutos_das_pontes) if minutos_das_pontes else None,
              "minutos_estimados_sem_ponte": sem_ponte, "minutos_estimados_com_ponte": sem_ponte + max(minutos_das_pontes) if minutos_das_pontes else None}
    return {"metadados": {"gerado_em": gerado_em or datetime.now().isoformat(timespec="seconds"), "corrida": bruto["saida"], "gerado_por": "avaliar_fase5.py --custo"},
            "resumo": resumo, "pontes": bruto["pontes"]}


# ------------------------------------------------------------------ a planilha da linha de base manual (seção 4.6 do plano)

def ler_planilha(texto: str) -> list[dict]:
    """As linhas da planilha (ponto e vírgula), cada uma com o número da linha no arquivo (o cabeçalho é a linha 1); linha toda em branco não conta."""
    linhas = list(csv.reader(io.StringIO(texto.lstrip("\ufeff")), delimiter=lbm.SEPARADOR))
    if not linhas or tuple(c.strip() for c in linhas[0]) != tuple(lbm.COLUNAS_DA_PLANILHA):
        raise LeituraRecusada([f"linha 1: as colunas da planilha não são as do protocolo ({lbm.SEPARADOR.join(lbm.COLUNAS_DA_PLANILHA)})"])
    lidas = []
    for numero, celulas in enumerate(linhas[1:], 2):
        if any(c.strip() for c in celulas):
            celulas = celulas + [""] * (len(lbm.COLUNAS_DA_PLANILHA) - len(celulas))
            lidas.append({"linha": numero, **{coluna: valor.strip() for coluna, valor in zip(lbm.COLUNAS_DA_PLANILHA, celulas)}})
    return lidas


def ler_planilha_do_arquivo(caminho: Path) -> list[dict]:
    """A planilha em UTF-8 com BOM, como `linha_de_base_manual.py` grava; se o Excel a regravou na codificação do Windows, lê assim."""
    cru = caminho.read_bytes()
    try:
        return ler_planilha(cru.decode("utf-8-sig"))
    except UnicodeDecodeError:
        return ler_planilha(cru.decode("cp1252"))


def ler_sessao(caminho: Path) -> list[dict]:
    """Os eventos do registro da sessão (um JSON por linha); lista vazia sem o arquivo."""
    return executar_bateria.ler_jsonl(caminho)


def _instante(texto: str) -> tuple[str, datetime]:
    """Uma hora da planilha: data e hora (2026-11-19T14:02:03.500) ou só a hora (14:02:03 ou 14:02:03,5), com ponto ou vírgula nos décimos."""
    limpo = texto.strip().replace(",", ".")
    if not limpo:
        raise ValueError("hora em branco")
    if re.match(r"\d{4}-\d\d-\d\d", limpo):
        return "data", datetime.fromisoformat(limpo)
    return "hora", datetime.combine(dt.date(2000, 1, 1), dt.time.fromisoformat(limpo))


def segundos_entre(inicio: str, fim: str) -> float:
    """Os segundos do início ao fim; ValueError quando uma das horas não se lê, quando uma tem data e a outra não, ou quando o fim vem antes do início."""
    (forma_a, a), (forma_b, b) = _instante(inicio), _instante(fim)
    if forma_a != forma_b:
        raise ValueError("uma hora tem data e a outra não")
    if b < a:
        raise ValueError("o fim vem antes do início")
    return round((b - a).total_seconds(), 3)


def _numero(texto: str) -> float | None:
    """Um número da planilha, com ponto ou vírgula decimal; None em branco."""
    return float(texto.strip().replace(",", ".")) if texto.strip() else None


def _marcada(observacoes: str, marca: str, no_comeco: bool = False) -> bool:
    """A marca nas observações da linha, sem diferença de maiúscula e de acento. `no_comeco` pede que as observações comecem com ela: é o caso da linha anulada,
    para um texto que só cita a palavra ("perguntou se seria anulada") não tirar a tentativa da conta."""
    texto, alvo = _norm(observacoes), _norm(marca)
    return texto.startswith(alvo) if no_comeco else alvo in texto


# ! Alteração de IA - Revisar: (16/11/2026, F1) `_conferir_linha` e `conferir_planilha`: cada linha preenchida da planilha conferida contra o sorteio, contra a
# própria conta do tempo, contra a lista das 23 causas e contra a regra do que conta como corrigido, com a recusa dizendo a linha do arquivo. O formato lido é o
# que `linha_de_base_manual.py` grava na versão 2 do protocolo (pacote F2): na planilha, as horas em HH:MM:SS e os números com vírgula decimal; no registro da
# sessão, o evento `tentativa` de cada `conferir`, com o seletor e se ele corrigiu.
# ! Motivo: seção 4.6 do plano. O tempo das pessoas entra na comparação central do TCC, e uma linha digitada errado mudaria o resultado sem ninguém ver. No
# contrato a leitura refaz `cenarios_fase4.task_success_contrato` com a causa e o campo entregues, a mesma regra do agente; no localizador exige no registro da
# sessão um `conferir` que passou com o seletor da planilha, a menos que a linha esteja marcada como anotada à mão (a ferramenta falhou no cenário e valeu o
# cronômetro de reserva). A linha anulada na hora (regra L14) é contada à parte e não entra em conta nenhuma. Tempo acima do limite de 10 minutos numa linha
# corrigida é recusado; numa linha não corrigida, a tentativa fica sem fim, como o protocolo (seção 6) manda para quem estoura o limite.
def _conferir_linha(linha: dict, c: dict, eventos: list[dict]) -> tuple[dict | None, str | None, dict]:
    """Uma linha preenchida: (a medida, None, marcas) quando vale, (None, a recusa, {}) quando não."""
    n, posicao = int(linha["integrante"]), int(linha["ordem"])
    onde = f"linha {linha['linha']} (integrante {n}, ordem {posicao}, {c['id']})"
    marcas = {"a_mao": _marcada(linha["observacoes"], MARCA_A_MAO), "sem_fim": False}
    if _norm(linha["corrigido"]) not in ("sim", "nao"):
        return None, f"{onde}: a coluna corrigido tem {linha['corrigido']!r}; ela aceita sim ou não", {}
    corrigido = _norm(linha["corrigido"]) == "sim"
    if not linha["fim"]:
        if corrigido or linha["segundos"]:
            return None, f"{onde}: sem fim, a linha não pode ter segundos nem estar marcada como corrigida (quem estoura o limite fica sem fim e não corrigido)", {}
        tempo, marcas["sem_fim"] = None, True
    else:
        try:
            bruto = segundos_entre(linha["inicio"], linha["fim"])
        except ValueError as e:
            return None, f"{onde}: inicio {linha['inicio']!r} e fim {linha['fim']!r} não dão uma duração ({e})", {}
        try:
            descontar, tempo = _numero(linha["descontar_s"]) or 0.0, _numero(linha["segundos"])
        except ValueError:
            return None, f"{onde}: segundos {linha['segundos']!r} ou descontar_s {linha['descontar_s']!r} não é número", {}
        if tempo is None:
            return None, f"{onde}: a linha tem fim e não tem segundos", {}
        if abs(tempo - (bruto - descontar)) > FOLGA_S + 1e-9:
            return None, (f"{onde}: segundos ({_s(tempo, 3)}) não é o fim menos o início menos o desconto ({_s(bruto, 3)} - {_s(descontar, 3)} = "
                          f"{_s(bruto - descontar, 3)}), com folga de {_s(FOLGA_S)} s"), {}
        if tempo > LIMITE_S:
            if corrigido:
                return None, f"{onde}: {_s(tempo)} s passa do limite de {LIMITE_S:.0f} s, e a linha está marcada como corrigida", {}
            tempo, marcas["sem_fim"] = None, True   # protocolo, seção 6: estourado o limite, o cenário fica não corrigido e sem tempo de fim
    if c["tipo"] == "contrato":
        regra, causa, campo = False, linha["causa"], None
        if linha["fim"]:
            if _norm(causa) not in avaliar._PERMITIDAS:
                return None, f"{onde}: a causa {causa!r} não está na lista das {len(taxonomia.CAUSAS_RAIZ)} causas", {}
            campo = None if not linha["campo"] or "nenhum" in _norm(linha["campo"]) else linha["campo"]
            regra = cen.task_success_contrato({"conferido": True, "causa": causa, "campo": campo}, c["causa"], c["campo"])
        if regra != corrigido and not marcas["sem_fim"]:
            return None, (f"{onde}: corrigido é {linha['corrigido']!r}, e a regra do contrato (a causa e o campo esperados do cenário) dá "
                          f"{'sim' if regra else 'não'} para a causa {causa!r} e o campo {campo or 'nenhum'!r}"), {}
    elif corrigido:
        if not linha["seletor"]:
            return None, f"{onde}: a linha está marcada como corrigida e não tem seletor", {}
        passou = any(e.get("evento") == EVENTO_DO_CONFERIR and e.get("corrigido") and str(e.get("integrante")) == str(n) and e.get("cenario") == c["id"]
                     and str(e.get("seletor") or "").strip() == linha["seletor"] for e in eventos)
        if not passou and not marcas["a_mao"]:
            return None, (f"{onde}: corrigido é sim, e o registro da sessão não tem uma tentativa do conferir que corrigiu com o seletor {linha['seletor']!r}; se a "
                          f"ferramenta falhou neste cenário e valeu o cronômetro de reserva, as observações da linha levam a marca {MARCA_A_MAO!r}"), {}
    return {**medida(c["id"], c["tipo"], n, corrigido, tempo), "ordem": posicao, "linha": linha["linha"]}, None, marcas


def conferir_planilha(linhas: list[dict], eventos: list[dict]) -> dict:
    """As linhas da planilha contra o sorteio e contra as regras da seção 4.6: as medidas que valem, as recusas (cada uma dizendo a linha) e as linhas
    anuladas, anotadas à mão e sem fim de cronômetro."""
    catalogo = {c["id"]: c for c in cen.CENARIOS_DO_ENSAIO}
    sorteio = [(n, posicao, cid) for n, ids in sorted(lbm.ordem_dos_integrantes(INTEGRANTES).items()) for posicao, cid in enumerate(ids, 1)]
    recusas, medidas, faltam, anuladas, a_mao, sem_fim = [], [], [], [], [], []
    if len(linhas) != len(sorteio):
        recusas.append(f"a planilha tem {len(linhas)} linhas de tentativa, e o sorteio tem {len(sorteio)} ({INTEGRANTES} integrantes nos {len(catalogo)} cenários)")
    for linha, (n, posicao, cid) in zip(linhas, sorteio):
        if (linha["integrante"], linha["ordem"], linha["cenario"], linha["tipo"]) != (str(n), str(posicao), cid, catalogo[cid]["tipo"]):
            recusas.append(f"linha {linha['linha']} (integrante {linha['integrante']}, ordem {linha['ordem']}, {linha['cenario']}, {linha['tipo']}): não é a linha do "
                           f"sorteio, que pede aqui integrante {n}, ordem {posicao}, {cid}, {catalogo[cid]['tipo']}")
            continue
        quem = {"linha": linha["linha"], "integrante": n, "ordem": posicao, "cenario": cid}
        if _marcada(linha["observacoes"], MARCA_ANULADA, no_comeco=True):
            anuladas.append(quem)
            continue
        if not linha["corrigido"]:
            faltam.append(linha["linha"])
            continue
        feita, recusa, marcas = _conferir_linha(linha, catalogo[cid], eventos)
        if recusa:
            recusas.append(recusa)
            continue
        medidas.append(feita)
        if marcas["a_mao"]:
            a_mao.append(quem)
        if marcas["sem_fim"]:
            sem_fim.append(quem)
    preenchidas = len(sorteio) - len(faltam) if len(linhas) == len(sorteio) else len(medidas) + len(anuladas)
    if faltam:
        recusas.insert(0, f"planilha incompleta: {len(sorteio) - len(faltam)} de {len(sorteio)} linhas preenchidas; faltam " + ", ".join(f"linha {n}" for n in faltam))
    return {"medidas": medidas, "recusas": recusas, "linhas": {"esperadas": len(sorteio), "preenchidas": preenchidas, "anuladas": anuladas, "anotadas_a_mao": a_mao,
                                                               "sem_fim": sem_fim}}


# ! Alteração de IA - Revisar: (16/11/2026, F1) `resumir_manual`: a leitura das 30 tentativas das pessoas, pela mesma conta do lado do agente, com o tempo pela
# posição na ordem e por integrante como descrição.
# ! Motivo: regras L4, L5, L6, L13 e L14 do plano. Com a planilha incompleta ou com qualquer linha recusada a leitura não sai (a exceção leva as recusas, e a
# linha de comando sai com código 2 sem mostrar número), como a leitura da sessão de revisão da Fase 4: um resultado parcial das pessoas visto antes da hora
# poderia mudar como as sessões que faltam são conduzidas.
def resumir_manual(linhas: list[dict], eventos: list[dict], gerado_em: str | None = None, origem: dict | None = None) -> dict:
    conferida = conferir_planilha(linhas, eventos)
    if conferida["recusas"]:
        raise LeituraRecusada(conferida["recusas"])
    medidas = conferida["medidas"]
    lado = resumir_lado(medidas)
    por_posicao = []
    for posicao in range(1, len(cen.CENARIOS_DO_ENSAIO) + 1):
        da_posicao = [m for m in medidas if m["ordem"] == posicao]
        tempos = [m["tempo_s"] for m in da_posicao if m["tempo_s"] is not None]
        por_posicao.append({"posicao": posicao, "n": len(da_posicao), "com_fim": len(tempos), "sucessos": sum(1 for m in da_posicao if m["sucesso"]), "tempo_media_s": _r(_media(tempos))})
    por_integrante = []
    for n in range(1, INTEGRANTES + 1):
        do_integrante = [m for m in medidas if m["quem"] == n]
        tempos = [m["tempo_s"] for m in do_integrante if m["tempo_s"] is not None]
        por_integrante.append({"integrante": n, "n": len(do_integrante), "sucessos": sum(1 for m in do_integrante if m["sucesso"]), "com_fim": len(tempos),
                               "tempo_media_s": _r(_media(tempos)), "tempo_total_s": _r(sum(tempos), 1) if tempos else None})
    return {"metadados": {"gerado_em": gerado_em or datetime.now().isoformat(timespec="seconds"), "gerado_por": "avaliar_fase5.py --manual", **(origem or {})},
            "linhas": conferida["linhas"], **lado, "por_posicao": por_posicao, "por_integrante": por_integrante}


# ! Alteração de IA - Revisar: (24/11/2026, ficha 91, decisão 151) `sem_um_integrante`: a comparação refeita sem a sessão de um integrante por vez, com a mesma
# conta da leitura (`resumir_lado` e `comparar`, regras L2 a L11) aplicada às medidas que sobram; uma linha por integrante que sai. `resumir_medicao` passa a
# aceitar as medidas das pessoas e, com elas, acrescenta no fim o campo `sem_um_integrante` e a nota `nota_sem_um_integrante`; os outros campos não mudam.
# ! Motivo: lidas as sessões em 24/11/2026, o veredito do Task Success mostrou depender da sessão de um integrante que não corrigiu nenhum cenário. O Eric decidiu
# que a leitura fica como as regras deram, com a ressalva declarada, e que a conta sem cada integrante entra como tabela gerada por script, no lugar da conta de
# rascunho que o relatório citava. Ela foi pensada depois de ver os números: pela regra L15 do plano entra marcada como exploratória e não muda veredito nenhum.
# O p do Task Success é mostrado mesmo quando sobram menos cenários diferentes do que a regra L11 pede, porque a tabela existe para mostrar de quanto o teste
# se afasta; o que a regra daria fica na coluna ao lado.
NOTA_SEM_UM_INTEGRANTE = ("Conta exploratória, acrescentada em 24/11/2026, depois de ver os números (ficha 91, decisão 151): a mesma comparação refeita sem a sessão de um "
                          "integrante por vez, com as regras L2 a L11 aplicadas às medidas que sobram. Ela não é o veredito da leitura, que continua sendo o das três sessões, "
                          "pelas regras fixadas antes das medidas; mostra de que sessão cada veredito depende. O p do Task Success aparece mesmo quando sobram menos cenários "
                          "diferentes do que a regra L11 pede para o teste valer, e a coluna ao lado diz o que a regra daria.")


def sem_um_integrante(agente: dict, medidas_das_pessoas: list[dict]) -> list[dict]:
    """A comparação sem a sessão de cada integrante, uma linha por integrante que sai: o que sobra das pessoas, o tempo (regras L8 e L9) e o Task Success (L11)."""
    linhas = []
    for n in range(1, INTEGRANTES + 1):
        resto = resumir_lado([m for m in medidas_das_pessoas if m["quem"] != n])
        c = comparar(agente, resto)
        g, tempo, ts = resto["geral"], c["tempo"]["geral"], c["task_success"]
        linhas.append({"sem_o_integrante": n,
                       "pessoas": {"tentativas": g["n"], "corrigidas": g["sucessos"], "task_success_pct": g["task_success_pct"], "com_fim": g["com_fim"], "sem_fim": g["sem_fim"],
                                   "tempo_media_s": g["tempo_media_s"]},
                       "tempo": {**{k: tempo[k] for k in ("cenarios_com_os_dois_lados", "diferenca_media_s", "ic_lo_s", "ic_hi_s", "razao_das_medias")},
                                 "agente_mais_rapido": tempo["sinais"]["agente"], "pessoas_mais_rapidas": tempo["sinais"]["pessoas"], "empates": tempo["sinais"]["empates"],
                                 "sem_medida": tempo["sinais"]["sem_medida"], "p": tempo["sinais"]["p"], "o_que_a_regra_l9_daria": tempo["caso"], "lado": tempo["lado"]},
                       "task_success": {"agente_maior": ts["sinais"]["agente"], "pessoas_maior": ts["sinais"]["pessoas"], "iguais": ts["sinais"]["iguais"],
                                        "sem_medida": ts["sinais"]["sem_medida"], "p": avaliar.mcnemar_exato(ts["sinais"]["agente"], ts["sinais"]["pessoas"]),
                                        "o_que_a_regra_l11_daria": ts["caso"], "lado": ts["lado"]}})
    return linhas


def resumir_medicao(agente: dict, manual: dict, gerado_em: str | None = None, medidas_das_pessoas: list[dict] | None = None) -> dict:
    """Os dois lados e a comparação entre eles, com as constantes das regras de leitura ao lado; com as medidas das pessoas, também a conta exploratória sem a
    sessão de cada integrante, em campos próprios no fim."""
    dado = {"metadados": {"gerado_em": gerado_em or datetime.now().isoformat(timespec="seconds"), "corrida": agente["metadados"].get("corrida"), "gerado_por": "avaliar_fase5.py --comparar"},
            "lados": {"agente": {"noite": agente["noite"], "geral": agente["geral"], "por_tipo": agente["por_tipo"], "tempo_total": agente["tempo_total"]},
                      "pessoas": {"linhas": manual["linhas"], "geral": manual["geral"], "por_tipo": manual["por_tipo"]}},
            **comparar(agente, manual),
            "regras": {"empate_s": EMPATE_S, "limite_s": LIMITE_S, "alfa": ALFA, "reamostras": REAMOSTRAS, "semente": SEMENTE,
                       "minimo_de_cenarios_no_task_success": minimo_de_cenarios_para_veredito()}}
    if medidas_das_pessoas is not None:
        dado.update({"sem_um_integrante": sem_um_integrante(agente, medidas_das_pessoas), "nota_sem_um_integrante": NOTA_SEM_UM_INTEGRANTE})
    return dado


# ------------------------------------------------------------------ os .md derivados (blocos tb_f5_*)

def cabecalho(titulo: str, origem: str, data: str) -> list[str]:
    """As três primeiras linhas de todo .md derivado da fase: a tag (duas linhas) e o título com a data, que fica fora da comparação do --check."""
    return [f"<!-- ! Alteração de IA - Revisar: documento DERIVADO, gerado por avaliar_fase5.py a partir de {origem} (--check regera e compara); não editar à mão.",
            "     ! Motivo: nenhum número digitado à mão; o relatório da Fase 5 do Memorial cola estes blocos, e as contas são as das regras L1 a L15 do plano "
            "aprovado, fixadas antes das medidas. -->",
            f"# {titulo}, gerada em {data}"]


def _faixa(lo, hi, casas: int = 1) -> str:
    return "n/d" if lo is None or hi is None else f"{_s(lo, casas)} a {_s(hi, casas)}"


def _linha_do_bloco(x: dict) -> list[str]:
    return [str(x["n"]), str(x["sucessos"]), _s(x["task_success_pct"]), _faixa(x["wilson_lo_pct"], x["wilson_hi_pct"]), f"{x['cenarios_com_todas_certas']} de {x['cenarios']}",
            str(x["com_fim"]), str(x["sem_fim"]), _s(x["tempo_media_s"]), _faixa(x["tempo_ic_lo_s"], x["tempo_ic_hi_s"]), _s(x["piso_media_s"]),
            _faixa(x["piso_ic_lo_s"], x["piso_ic_hi_s"]), _s(x["estrita_media_s"])]


def _cabecalho_do_bloco(medidas: str, tempo: str) -> list[str]:
    return [medidas, "Task Success", "Task Success (%)", "Wilson 95% (%)", "Cenários com todas certas", "Com fim de cronômetro", "Sem fim", f"{tempo} (s)",
            "Reamostragem 95% (s)", "Segunda conta, com 600 s para quem não chegou ao fim (s)", "Reamostragem 95% da segunda conta (s)", "Só com Task Success (s)"]


PROSA_DAS_REGRAS = ("A unidade é o cenário (regra L2): por cenário, a média de quem chegou ao fim do cronômetro, com o mínimo e o máximo; no geral e por tipo, a "
                    "média das médias dos cenários. O intervalo do tempo é a reamostragem dos cenários dentro de cada tipo ({reamostras} reamostras, semente "
                    "{semente}); o do Task Success é o de Wilson. Quem não chegou ao fim do cronômetro fica fora da média do tempo e dentro do Task Success; a "
                    "segunda conta põe 600 s no lugar e vale como piso.")


# ! Alteração de IA - Revisar: (18/11/2026, corrida 28b) `render_agente` recebe o prefixo dos blocos, ganha o bloco da conferência a frio e a coluna "Noite a frio",
# põe no título a corrida lida e, na leitura de um incidente, abre dizendo que a corrida não vale como a medida do agente.
# ! Motivo: a leitura da corrida 28 fica guardada com blocos `tb_f5_incidente28_*`, para não ocupar no relatório da fase o lugar dos blocos `tb_f5_agente_*`, que
# são do lado do agente na comparação e esperam a corrida 28b; o título dizia "(corrida 28)" para qualquer corrida lida.
SIM_NAO_OU_NAO_MEDIDO = {True: "sim", False: "não", None: "não medido"}


def render_agente(dado: dict, prefixo: str = "tb_f5_agente_") -> str:
    noite, cab = dado["noite"], _cabecalho_do_bloco("Execuções", "MTTR médio")
    ident = dado.get("mesmo_agente_da_21d") or []
    frio = (noite.get("frio") or {}).get("por_repeticao") or []
    blocos = [
        a3b.tab(f"{prefixo}resumo", cab, [_linha_do_bloco(dado["geral"])]),
        a3b.tab(f"{prefixo}por_tipo", ["Tipo"] + cab, [[x["tipo"]] + _linha_do_bloco(x) for x in dado["por_tipo"]]),
        a3b.tab(f"{prefixo}por_cenario", ["Cenário", "Tipo", "Execuções", "Task Success", "Com fim", "MTTR médio (s)", "Mínimo (s)", "Máximo (s)",
                                             "Segunda conta (s)", "Só com Task Success (s)", "Rótulo do diagnóstico em cada repetição", "Tempo total da execução (s)"],
                [[f"`{x['cenario']}`", x["tipo"], str(x["n"]), str(x["sucessos"]), str(x["com_fim"]), _s(x["tempo_media_s"]), _s(x["tempo_min_s"]), _s(x["tempo_max_s"]),
                  _s(x["piso_media_s"]), _s(x["estrita_media_s"]), ", ".join(f"`{r}`" for r in x.get("rotulos") or []) or "n/d", _s(x.get("segundos_media_s"))]
                 for x in dado["por_cenario"]]),
        a3b.tab(f"{prefixo}noite", ["Execuções gravadas", "Esperadas", "Noite completa", "Noite a frio", "Versões do Ollama nos diagnósticos", "Versões do navegador",
                                    "Hash do banco no começo das repetições", "Linha FIM no log", "Tempo total das execuções (s)", "Tempo total médio por cenário (s)"],
                [[str(noite["execucoes"]), str(noite["esperadas"]), a3b.f(noite["completa"]), SIM_NAO_OU_NAO_MEDIDO[noite.get("a_frio")],
                  ", ".join(noite["versoes_ollama"]) or "n/d",
                  ", ".join(noite["navegador"]["versoes"]) or "n/d", ", ".join(noite["banco"]["hashes_de_inicio"]) or "n/d", a3b.f(noite["linha_fim_no_log"]),
                  _s(dado["tempo_total"]["segundos_total_s"]), _s(dado["tempo_total"]["segundos_media_s"])]]),
        a3b.tab(f"{prefixo}frio", ["Repetição", "Inferências", "Tokens de entrada", "Tokens que vieram do que o Ollama tinha guardado", "Parcela guardada (%)",
                                   "Guardados na primeira inferência", "Leitura do prompt, somada (s)", "Carga do modelo, somada (s)", "A frio"],
                [[str(x["repeticao"]), str(x["inferencias"]), _s(x["tokens_entrada"], 0), _s(x["tokens_em_cache"], 0), _s(x["parcela_em_cache_pct"]),
                  _s(x["cache_na_primeira_inferencia"], 0), _s(x["prefill_s"]), _s(x["carga_s"]), SIM_NAO_OU_NAO_MEDIDO[x["a_frio"]]] for x in frio]
                or [["sem registro da barra de progresso"] + [""] * 8]),
        a3b.tab(f"{prefixo}identidade", ["Item", "Na corrida", "Na corrida 21d", "Igual", "Para a noite se diferir"],
                [[i["nome"], f"`{i['hoje']}`", f"`{i['na_21d']}`", a3b.f(i["igual"]), a3b.f(i["para"])] for i in ident] or [["sem a corrida 21d para comparar", "", "", "", ""]]),
        a3b.tab(f"{prefixo}sem_sucesso", ["Cenário", "Repetição", "Tipo", "Detectou", "Rótulo do diagnóstico", "Causa esperada", "Falha da cura", "MTTR (s)", "Segundos"],
                [[f"`{x['cenario']}`", str(x["repeticao"]), x["tipo"], a3b.f(x["detectou"]), f"`{x['rotulo']}`" if x["rotulo"] else "n/d", f"`{x['causa_esperada']}`",
                  f"`{x['falha_da_cura']}`" if x["falha_da_cura"] else "n/d", _s(x["mttr_s"]), _s(x["segundos"])] for x in dado["sem_task_success"]]
                or [["nenhuma"] + [""] * 8]),
    ]
    corrida = dado["metadados"].get("corrida")
    texto = cabecalho(f"O agente na Fase 5: MTTR e Task Success dos dez cenários ({NOME_DA_CORRIDA.get(corrida, corrida)})",
                      "cenarios.jsonl, condicoes_fase4.json, fase4.log e progresso_medidas.jsonl da corrida", dado["metadados"]["gerado_em"][:10])
    if dado["metadados"].get("incidente"):
        texto += ["", f"**Esta corrida não vale como a medida do agente.** {dado['metadados']['incidente']}"]
    texto += ["", (f"Corrida lida: `{dado['metadados'].get('corrida')}`. Os dez cenários da ficha 36, com o agente inteiro em cada execução. No contrato, o MTTR vai da "
                   "detecção ao diagnóstico conferido em código e o Task Success é a causa e o campo certos; no localizador, o MTTR vai da detecção à reexecução "
                   "validada, descontada a restauração do banco, e o Task Success é o roteiro concluído sem erro. "
                   + PROSA_DAS_REGRAS.format(reamostras=REAMOSTRAS, semente=SEMENTE)
                   + " Nenhuma execução é anulada: a que falhou aparece na última tabela. O tempo total da execução inclui a detecção e é só descrição."), "",
              (f"A noite vale a frio quando, em cada repetição, a primeira inferência não reaproveitou nenhum token do que o Ollama tinha guardado e no máximo "
               f"{100 * LIMITE_DA_PARCELA_EM_CACHE:.0f}% dos tokens de entrada da repetição vieram guardados. É conferência de validade da noite, fixada antes da "
               "corrida 28b com os registros da corrida 28, e não regra de comparação. O que ela não cobre: dentro de uma repetição, o começo do prompt que os "
               "cenários dividem continua vindo guardado de um cenário para o outro, e a primeira execução de cada repetição paga a carga do modelo."
               + (f" Nesta corrida: {noite['frio']['motivo']}." if (noite.get("frio") or {}).get("motivo") else "")), ""]
    return "\n".join(texto) + "\n\n" + "\n\n".join(blocos) + "\n"


def _quais(itens: list[dict]) -> str:
    return "; ".join(f"linha {i['linha']} (integrante {i['integrante']}, ordem {i['ordem']}, `{i['cenario']}`)" for i in itens) or "nenhuma"


def render_manual(dado: dict) -> str:
    linhas, cab = dado["linhas"], _cabecalho_do_bloco("Tentativas", "Tempo médio")
    blocos = [
        a3b.tab("tb_f5_manual_resumo", cab, [_linha_do_bloco(dado["geral"])]),
        a3b.tab("tb_f5_manual_por_tipo", ["Tipo"] + cab, [[x["tipo"]] + _linha_do_bloco(x) for x in dado["por_tipo"]]),
        a3b.tab("tb_f5_manual_por_cenario", ["Cenário", "Tipo", "Tentativas", "Corrigidas", "Com fim", "Tempo médio (s)", "Mínimo (s)", "Máximo (s)", "Segunda conta (s)",
                                             "Só as corrigidas (s)"],
                [[f"`{x['cenario']}`", x["tipo"], str(x["n"]), str(x["sucessos"]), str(x["com_fim"]), _s(x["tempo_media_s"]), _s(x["tempo_min_s"]), _s(x["tempo_max_s"]),
                  _s(x["piso_media_s"]), _s(x["estrita_media_s"])] for x in dado["por_cenario"]]),
        a3b.tab("tb_f5_manual_por_posicao", ["Posição na ordem do integrante", "Tentativas", "Corrigidas", "Com fim", "Tempo médio (s)"],
                [[str(x["posicao"]), str(x["n"]), str(x["sucessos"]), str(x["com_fim"]), _s(x["tempo_media_s"])] for x in dado["por_posicao"]]),
        a3b.tab("tb_f5_manual_por_integrante", ["Integrante", "Tentativas", "Corrigidas", "Com fim", "Tempo médio (s)", "Tempo somado (s)"],
                [[str(x["integrante"]), str(x["n"]), str(x["sucessos"]), str(x["com_fim"]), _s(x["tempo_media_s"]), _s(x["tempo_total_s"])] for x in dado["por_integrante"]]),
        a3b.tab("tb_f5_manual_linhas", ["Linhas esperadas", "Preenchidas", "Anuladas na hora (fora de toda conta)", "Anotadas à mão", "Sem fim de cronômetro (estourou o limite ou não entregou)"],
                [[str(linhas["esperadas"]), str(linhas["preenchidas"]), _quais(linhas["anuladas"]), _quais(linhas["anotadas_a_mao"]), _quais(linhas["sem_fim"])]]),
    ]
    texto = cabecalho("A linha de base manual na Fase 5: tempo e Task Success dos integrantes", "a planilha da linha de base manual e o registro da sessão",
                      dado["metadados"]["gerado_em"][:10])
    texto += ["", ("Três integrantes, cada um nos dez cenários, na ordem sorteada. O tempo de cada tentativa é o fim menos o início menos o desconto da restauração "
                   "do banco; no contrato o cronômetro para na entrega da causa e do campo, certa ou errada, e no localizador, no conferir que passou. "
                   + PROSA_DAS_REGRAS.format(reamostras=REAMOSTRAS, semente=SEMENTE)
                   + " A linha anulada na hora por falha do protocolo é contada à parte e não entra em conta nenhuma. O tempo pela posição na ordem e por integrante "
                     "é só descrição: mostra o aprendizado ao longo da sessão."), ""]
    return "\n".join(texto) + "\n\n" + "\n\n".join(blocos) + "\n"


NOME_DA_DIRECAO = {"agente": "agente", "pessoas": "pessoas", "empate": "empate", "sem_medida": "sem medida", "igual": "igual"}


def render_medicao(dado: dict) -> str:
    agente, pessoas, tempo, ts = dado["lados"]["agente"]["geral"], dado["lados"]["pessoas"]["geral"], dado["tempo"], dado["task_success"]
    g, piso, regras = tempo["geral"], tempo["piso"], dado["regras"]
    sinais = g["sinais"]
    blocos = [
        a3b.tab("tb_f5_medicao_resumo", ["MTTR médio do agente (s)", "Reamostragem 95% (s)", "Tempo médio das pessoas (s)", "Reamostragem 95% (s)",
                                         "Diferença média por cenário, pessoas menos agente (s)", "Reamostragem 95% da diferença (s)", "Razão entre as médias",
                                         "Cenários com os dois lados", "Agente mais rápido", "Pessoas mais rápidas", "Empates", "p do teste dos sinais", "Leitura pela regra L9"],
                [[_s(agente["tempo_media_s"]), _faixa(agente["tempo_ic_lo_s"], agente["tempo_ic_hi_s"]), _s(pessoas["tempo_media_s"]),
                  _faixa(pessoas["tempo_ic_lo_s"], pessoas["tempo_ic_hi_s"]), _s(g["diferenca_media_s"]), _faixa(g["ic_lo_s"], g["ic_hi_s"]), _s(g["razao_das_medias"], 2),
                  str(g["cenarios_com_os_dois_lados"]), str(sinais["agente"]), str(sinais["pessoas"]), str(sinais["empates"]), _s(sinais["p"], 4), g["frase"]]]),
        a3b.tab("tb_f5_medicao_tempo_por_cenario", ["Cenário", "Tipo", "MTTR médio do agente (s)", "Faixa do agente (s)", "Tempo médio das pessoas (s)", "Faixa das pessoas (s)",
                                                    "Diferença, pessoas menos agente (s)", "Razão", "Quem foi mais rápido", "As faixas se cruzam"],
                [[f"`{x['cenario']}`", x["tipo"], _s(x["agente_media_s"]), _faixa(x["agente_min_s"], x["agente_max_s"]), _s(x["pessoas_media_s"]),
                  _faixa(x["pessoas_min_s"], x["pessoas_max_s"]), _s(x["diferenca_s"]), _s(x["razao"], 2), NOME_DA_DIRECAO[x["direcao"]],
                  "n/d" if x["faixas_se_cruzam"] is None else a3b.f(x["faixas_se_cruzam"])] for x in tempo["por_cenario"]]),
        a3b.tab("tb_f5_medicao_tempo_por_tipo", ["Tipo", "Cenários com os dois lados", "Diferença média, pessoas menos agente (s)", "Reamostragem 95% (s)", "Razão entre as médias",
                                                 "Agente mais rápido", "Pessoas mais rápidas", "Empates", "Sem medida"],
                [[x["tipo"], str(x["cenarios_com_os_dois_lados"]), _s(x["diferenca_media_s"]), _faixa(x["ic_lo_s"], x["ic_hi_s"]), _s(x["razao_das_medias"], 2),
                  str(x["agente_mais_rapido"]), str(x["pessoas_mais_rapidas"]), str(x["empates"]), str(x["sem_medida"])] for x in tempo["por_tipo"]]),
        a3b.tab("tb_f5_medicao_piso", ["Segunda conta: quem não chegou ao fim entra com 600 s", "Cenários com os dois lados", "Diferença média, pessoas menos agente (s)",
                                       "Reamostragem 95% (s)", "Razão entre as médias", "Agente mais rápido", "Pessoas mais rápidas", "Empates", "p do teste dos sinais",
                                       "O que a regra L9 daria nesta conta"],
                [["piso, não é o veredito da leitura", str(piso["cenarios_com_os_dois_lados"]), _s(piso["diferenca_media_s"]), _faixa(piso["ic_lo_s"], piso["ic_hi_s"]),
                  _s(piso["razao_das_medias"], 2), str(piso["sinais"]["agente"]), str(piso["sinais"]["pessoas"]), str(piso["sinais"]["empates"]), _s(piso["sinais"]["p"], 4),
                  piso["o_que_a_regra_l9_daria"] + (f" ({piso['lado']})" if piso["lado"] else "")]]),
        a3b.tab("tb_f5_medicao_task_success", ["Lado", "Medidas", "Task Success", "Task Success (%)", "Wilson 95% (%)", "Cenários com todas certas"],
                [[nome, str(x["n"]), str(x["sucessos"]), _s(x["task_success_pct"]), _faixa(x["wilson_lo_pct"], x["wilson_hi_pct"]),
                  f"{x['cenarios_com_todas_certas']} de {x['cenarios']}"] for nome, x in (("agente", ts["agente"]), ("pessoas", ts["pessoas"]))]),
        a3b.tab("tb_f5_medicao_task_success_por_cenario", ["Cenário", "Tipo", "Agente", "Agente (%)", "Pessoas", "Pessoas (%)", "Diferença (pontos)", "Parcela maior"],
                [[f"`{x['cenario']}`", x["tipo"], f"{x['agente_sucessos']} de {x['agente_n']}", _s(x["agente_pct"]), f"{x['pessoas_sucessos']} de {x['pessoas_n']}",
                  _s(x["pessoas_pct"]), _s(x["diferenca_pp"]), NOME_DA_DIRECAO[x["direcao"]]] for x in ts["por_cenario"]]),
        a3b.tab("tb_f5_medicao_descricao", ["Só descrição (regra L13)", "Agente", "Pessoas", "Diferença, pessoas menos agente (s)"],
                [["tempo médio só com as medidas que tiveram Task Success (s)", f"{_s(tempo['estrita']['agente_media_s'])} em {tempo['estrita']['agente_cenarios']} cenários",
                  f"{_s(tempo['estrita']['pessoas_media_s'])} em {tempo['estrita']['pessoas_cenarios']} cenários", _s(tempo["estrita"]["diferenca_s"])],
                 ["tempo total médio da execução do agente, com a detecção (s)", _s(dado["lados"]["agente"]["tempo_total"]["segundos_media_s"]), "não se aplica", "não se aplica"]]),
    ]
    # ! Alteração de IA - Revisar: (24/11/2026, decisão 151) quando a leitura traz a conta sem a sessão de cada integrante, o .md ganha o bloco
    # `tb_f5_medicao_sem_um_integrante`, depois dos outros, e a nota dela no texto. O rótulo de conta exploratória vai no cabeçalho da primeira coluna.
    # ! Motivo: o relatório da fase cola o bloco e o painel o mostra; se o rótulo ficasse só no texto em volta, a tabela chegaria a esses dois lugares parecendo um
    # segundo veredito. Os outros blocos e as frases das regras L9 e L11 saem iguais com a conta e sem ela (o teste compara).
    conta = dado.get("sem_um_integrante") or []
    if conta:
        minimo = regras["minimo_de_cenarios_no_task_success"]
        da_l9 = {("veredito", "agente"): "veredito: o agente mais rápido", ("veredito", "pessoas"): "veredito: as pessoas mais rápidas", ("ruido", None): "dentro do ruído",
                 ("pende", "agente"): "a média pende para o agente, sem veredito", ("pende", "pessoas"): "a média pende para as pessoas, sem veredito",
                 ("sem_medida", None): "sem medida dos dois lados"}
        da_l11 = {("veredito", "agente"): "veredito: o agente resolveu mais", ("veredito", "pessoas"): "veredito: as pessoas resolveram mais",
                  ("sem_veredito", None): f"sem veredito (menos de {minimo} cenários diferentes)", ("sem_diferenca", None): "sem diferença que a leitura afirme",
                  ("sem_medida", None): "sem medida dos dois lados"}
        blocos.append(a3b.tab("tb_f5_medicao_sem_um_integrante",
                              ["Conta exploratória de 24/11/2026, feita depois de ver os números; não é o veredito da leitura", "Tentativas das pessoas que sobram",
                               "Corrigidas", "Tempo médio das pessoas (s)", "Diferença média por cenário, pessoas menos agente (s)", "Reamostragem 95% (s)",
                               "Cenários com o agente mais rápido", "Com as pessoas mais rápidas", "Empates", "p do teste dos sinais no tempo", "O que a regra L9 daria",
                               "Cenários com a parcela do agente maior", "Com a das pessoas maior", "Iguais", "p do teste dos sinais no Task Success", "O que a regra L11 daria"],
                              [[f"sem a sessão do integrante {x['sem_o_integrante']}", str(x["pessoas"]["tentativas"]), str(x["pessoas"]["corrigidas"]), _s(x["pessoas"]["tempo_media_s"]),
                                _s(x["tempo"]["diferenca_media_s"]), _faixa(x["tempo"]["ic_lo_s"], x["tempo"]["ic_hi_s"]), str(x["tempo"]["agente_mais_rapido"]),
                                str(x["tempo"]["pessoas_mais_rapidas"]), str(x["tempo"]["empates"]), _s(x["tempo"]["p"], 4),
                                da_l9[(x["tempo"]["o_que_a_regra_l9_daria"], x["tempo"]["lado"])], str(x["task_success"]["agente_maior"]), str(x["task_success"]["pessoas_maior"]),
                                str(x["task_success"]["iguais"]), _s(x["task_success"]["p"], 4),
                                da_l11[(x["task_success"]["o_que_a_regra_l11_daria"], x["task_success"]["lado"])]] for x in conta]))
    texto = cabecalho("A medição de valor da Fase 5: o agente contra a linha de base manual", "os registros da corrida do agente, a planilha da linha de base manual e o "
                      "registro da sessão", dado["metadados"]["gerado_em"][:10])
    texto += ["", ("O agente repara mais rápido que uma pessoa, e resolve tantos cenários quanto ela? As regras desta leitura foram fixadas no plano da fase antes de "
                   "qualquer medida (regras L1 a L15). " + PROSA_DAS_REGRAS.format(reamostras=regras["reamostras"], semente=regras["semente"])
                   + f" A diferença de cada cenário é o tempo médio das pessoas menos o MTTR médio do agente: positiva quando o agente foi mais rápido. Diferença menor "
                     f"que {_s(regras['empate_s'], 0)} s conta como empate e sai do teste dos sinais; cenário em que só um lado chegou ao fim conta para esse lado no "
                     "teste e fica fora da média das diferenças."), "",
              f"**Tempo de reparo.** {g['frase']}", "", f"**Task Success.** {ts['frase']}", "", tempo["nota_por_tipo"], ""]
    if conta:
        texto += [dado["nota_sem_um_integrante"], ""]
    return "\n".join(texto) + "\n\n" + "\n\n".join(blocos) + "\n"


def render_custo(dado: dict) -> str:
    r = dado["resumo"]
    blocos = [
        a3b.tab("tb_f5_custo_resumo", ["Execuções da noite", "Segundos por execução na corrida 21d (média)", "Horas pela média das execuções",
                                       "Segundos do executor na corrida 21d", "Horas pelo executor inteiro", "Segundos fora do executor na corrida 21d (bateria de testes e leitura)",
                                       "Ponte, se o Ollama mudou de versão (min)", "Noite sem a ponte (min)", "Noite com a ponte (min)"],
                [[f"{r['execucoes']} ({r['cenarios']} cenários x {r['repeticoes']} repetições)", _s(r["segundos_por_execucao_na_21d"]), _s(r["horas_pelas_execucoes"], 2),
                  str(r["segundos_do_executor_na_21d"]), _s(r["horas_pelo_executor"], 2), str(r["segundos_fora_do_executor_na_21d"]),
                  "n/d" if r["ponte_minutos_min"] is None else f"{r['ponte_minutos_min']} a {r['ponte_minutos_max']}", str(r["minutos_estimados_sem_ponte"]),
                  "n/d" if r["minutos_estimados_com_ponte"] is None else str(r["minutos_estimados_com_ponte"])]]),
        a3b.tab("tb_f5_custo_pontes", ["Ponte (pasta em `resultados_alvo/`)", "Versão do Ollama", "Data", "Duração (min)"],
                [[f"`{p['corrida']}`", str(p["versao"]), str(p["data"]), str(p["minutos"])] for p in dado["pontes"]] or [["nenhuma com a linha FIM no log", "", "", ""]]),
    ]
    texto = cabecalho("O tempo de máquina da noite medida da Fase 5 (corrida 28)", "cenarios.jsonl e fase4.log da corrida 21d e o log das três últimas pontes",
                      dado["metadados"]["gerado_em"][:10])
    texto += ["", (f"Estimativa feita com os registros da corrida 21d (`{dado['metadados']['corrida']}`), que rodou os dez cenários uma vez. A conta de baixo multiplica o "
                   "tempo médio de uma execução pelas execuções da noite; a de cima multiplica o tempo do executor inteiro pelas repetições, o que inclui o que ele gasta "
                   "fora das execuções, e soma o que o lançador gastou fora do executor. A ponte só roda se o Ollama tiver mudado de versão desde a última ponte "
                   "registrada. O painel, regerado no fim da noite, não está nesta conta."), ""]
    return "\n".join(texto) + "\n\n" + "\n\n".join(blocos) + "\n"


# ------------------------------------------------------------------ linha de comando

def _fechar(nome: str, dado: dict, md: str, prefixo: str, args: argparse.Namespace, pasta: Path, oficial: Path = PASTA) -> int:
    """Grava, confere ou cola pelo molde de pre_fase4.fechar; o relatório da Fase 5 só nasce no pacote F5, e até lá `--colar` não tem onde colar."""
    if args.colar and not RELATORIO.exists():
        print(f"--colar: {RELATORIO.name} ainda não existe (ele nasce no pacote F5); até lá os blocos {prefixo}* ficam em {nome}.md")
        return 2
    # ! Alteração de IA - Revisar: (16/11/2026, parte do pacote F5 adiantada) com `--pasta` diferente da pasta oficial dos derivados, o `--check` deixa de comparar
    # os blocos do relatório da fase com a leitura feita ali: `pre_fase4.fechar` recebe `blocos_de`, e a mensagem diz de qual leitura os blocos do relatório são.
    # ! Motivo: o relatório `fase-5-relatorio.md` nasceu em 16/11/2026 com os blocos `tb_f5_agente_*`, `tb_f5_manual_*` e `tb_f5_medicao_*` vazios, à espera da
    # corrida 28 e das sessões. O teste `teste_leitura_do_agente_sobre_a_corrida_21d_da_os_numeros_da_leitura_vigente` lê a corrida 21d numa pasta temporária e roda
    # o `--check`, que passou a sair com "DIFERE (blocos divergentes em fase-5-relatorio.md)": os blocos do relatório são os da leitura oficial (a corrida 28, em
    # `resultados_alvo/fase5`), e nunca os de uma leitura feita em outra pasta. O mesmo erro apareceria em 25/11, com os blocos da corrida 28 colados. Nenhuma
    # regra de leitura muda: só o que o `--check` de uma pasta que não é a oficial compara.
    # ! Alteração de IA - Revisar: (18/11/2026, corrida 28b) a pasta oficial da leitura vem por parâmetro (a do incidente é outra), e `--colar` com `--pasta`
    # fora dela é recusado.
    # ! Motivo: a leitura da corrida 28 é guardada em `resultados_alvo/fase5_incidente_28`, com blocos próprios no relatório; e uma leitura feita em pasta de
    # rascunho com `--colar` trocaria os blocos do relatório da fase por números que não são os da leitura gravada (ficou por fazer em 16/11, sem teste).
    if args.colar and pasta.resolve() != oficial.resolve():
        print(f"--colar: a leitura feita com --pasta em {pasta} não é a gravada em {oficial}, e só essa entra no relatório da fase; rode sem --pasta")
        return 2
    de_outra_leitura = None if pasta.resolve() == oficial.resolve() else f"gravada em {oficial.name}, e não desta pasta"
    return pf.fechar(nome, dado, md, prefixo, check=args.check, colar=args.colar, pasta=pasta, doc=RELATORIO, blocos_de=de_outra_leitura)


def _agente_lido(args: argparse.Namespace, oficial: bool) -> dict | None:
    """A leitura do agente pronta para gravar ou comparar; None (com o aviso impresso) quando não há registros ou quando a corrida não é a noite completa e a
    pasta dos derivados é a oficial."""
    saida = args.saida or SAIDA_DO_AGENTE
    bruto = ler_agente(saida)
    if not bruto["registros"]:
        print(f"sem cenarios.jsonl em {caminhos.RESULTADOS / saida}: a corrida 28b ainda não rodou (rodar_fase5.ps1)")
        return None
    dado = resumir_agente(bruto, corrida=saida)
    if oficial and not dado["noite"]["completa"]:
        print(f"a noite não está completa ({dado['noite']['execucoes']} de {dado['noite']['esperadas']} execuções em {saida}/cenarios.jsonl): a leitura não grava em "
              f"{PASTA}. Relance o rodar_fase5.ps1 para retomar o que falta, ou passe --pasta para ler esta corrida em outra pasta")
        return None
    # (18/11/2026, decisão 146) só a noite a frio é a medida do agente: a corrida 28, completa e com o prompt reaproveitado, não entra em resultados_alvo/fase5
    if oficial and dado["noite"]["a_frio"] is not True:
        print(f"{'a noite não foi a frio' if dado['noite']['a_frio'] is False else 'não dá para confirmar que a noite foi a frio'} ({dado['noite']['frio']['motivo']}): "
              f"a leitura não grava em {PASTA}, porque só a noite completa e a frio é a medida do agente (decisão 146). Para ler esta corrida em outra pasta, "
              "passe --pasta; leve o resultado ao Claude antes de qualquer outra coisa")
        return None
    return dado


def _manual_lido(args: argparse.Namespace) -> dict | None:
    """A leitura da planilha; None (com as recusas impressas, sem número nenhum) quando ela está incompleta ou tem linha recusada."""
    planilha = Path(args.planilha) if args.planilha else lbm.PLANILHA
    sessao = Path(args.sessao) if args.sessao else PASTA_DA_SESSAO / REGISTRO_DA_SESSAO
    if not planilha.exists():
        print(f"sem a planilha em {planilha}")
        return None
    try:
        return resumir_manual(ler_planilha_do_arquivo(planilha), ler_sessao(sessao), origem={"planilha": planilha.name, "registro_da_sessao": sessao.name})
    except LeituraRecusada as e:
        print(f"a planilha {planilha.name} não foi lida; nenhum resultado é mostrado antes de ela estar completa e conferida:")
        for recusa in e.recusas:
            print(f"  {recusa}")
        return None


def montar_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--custo", action="store_true", help="o tempo da noite medida, pelos registros da corrida 21d")
    ap.add_argument("--antes", action="store_true", help="confere, sem chamar o modelo, que o agente de hoje é o da corrida 21d; sai com 1 se diferir")
    ap.add_argument("--agente", action="store_true", help="lê a corrida do agente (corrida 28b); só grava em resultados_alvo/fase5 a noite completa e a frio")
    ap.add_argument("--incidente", default=None, metavar="CORRIDA", help="lê uma corrida guardada como incidente, fora da comparação (hoje só a 28), na pasta e com os blocos dela")
    ap.add_argument("--sondagem", action="store_true", help="com --saida, o veredito da sondagem do frio gravada naquela pasta (sai com 0 se passou); sem --saida, "
                                                            "diz ao lançador qual foi a última sondagem e se ela passou")
    ap.add_argument("--manual", action="store_true", help="lê a planilha da linha de base manual e o registro da sessão")
    ap.add_argument("--comparar", action="store_true", help="põe o agente e as pessoas na mesma tabela")
    ap.add_argument("--situacao", action="store_true", help="diz ao lançador quantas execuções da noite já estão gravadas e se ela está completa; não grava nada")
    ap.add_argument("--saida", default=None, help=f"a pasta da corrida do agente em resultados_alvo (padrão {SAIDA_DO_AGENTE}; em --custo, {CORRIDA_DE_REFERENCIA})")
    ap.add_argument("--planilha", default=None, help="a planilha da linha de base manual (padrão: a do Memorial)")
    ap.add_argument("--sessao", default=None, help=f"o registro da sessão (padrão resultados_alvo/fase5_manual/{REGISTRO_DA_SESSAO})")
    ap.add_argument("--pasta", default=None, help="pasta dos derivados (padrão resultados_alvo/fase5)")
    ap.add_argument("--canal", default="chromium", help="--antes: o canal do navegador da corrida (padrão chromium)")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--colar", action="store_true")
    return ap


def main(argv: list[str] | None = None) -> int:
    ap = montar_parser()
    args = ap.parse_args(argv)
    modos = [m for m in ("custo", "antes", "agente", "manual", "comparar", "situacao", "sondagem", "incidente") if getattr(args, m)]
    if len(modos) != 1:
        ap.error("informe um de --custo, --antes, --agente, --manual, --comparar, --situacao, --sondagem ou --incidente")
    pasta = Path(args.pasta) if args.pasta else PASTA
    oficial = pasta.resolve() == PASTA.resolve()
    if (args.antes or args.situacao or args.sondagem) and (args.check or args.colar):
        ap.error("--antes, --situacao e --sondagem não têm --check nem --colar")
    if args.situacao:
        bruto = ler_agente(args.saida or SAIDA_DO_AGENTE)
        situacao = situacao_da_noite(bruto["registros"], bruto["condicoes"])
        print(f"execucoes={situacao['execucoes']}\nesperadas={situacao['esperadas']}\ncompleta={'sim' if situacao['completa'] else 'nao'}\n"
              f"repeticoes_completas={repeticoes_completas(bruto['registros'])}\nversoes_ollama={','.join(bruto['versoes_ollama'])}")
        return 0
    if args.sondagem:
        if not args.saida:
            # é o que o rodar_fase5.ps1 pergunta antes da primeira repetição: linhas chave=valor, e o código de saída diz se a última sondagem passou
            ultima = ultima_sondagem(caminhos.RESULTADOS)
            if ultima is None:
                print("passou=sem_sondagem\npasta=\nversoes_ollama=")
                return 2
            print(f"passou={'sim' if ultima['passou'] else 'nao'}\npasta={ultima['pasta']}\nversoes_ollama={','.join(ultima['versoes_ollama'])}")
            return 0 if ultima["passou"] else 1
        raiz = caminhos.RESULTADOS / args.saida
        medidas = executar_bateria.ler_jsonl(raiz / progresso.NOME_DAS_MEDIDAS)
        if not medidas:
            print(f"sem {progresso.NOME_DAS_MEDIDAS} em {raiz}: a sondagem não gravou nenhuma inferência")
            return 2
        veredito = sondagem_do_frio(medidas)
        diagnosticos = [r for arq in sorted(raiz.glob("*/diagnosticos__cenarios.jsonl")) for r in executar_bateria.ler_jsonl(arq)]
        gravado = {"gerado_em": datetime.now().isoformat(timespec="seconds"), "gerado_por": "avaliar_fase5.py --sondagem", "pasta": raiz.name,
                   "versoes_ollama": sorted({r["versao_ollama"] for r in diagnosticos if r.get("versao_ollama")}), **veredito}
        (raiz / ARQUIVO_DA_SONDAGEM).write_text(json.dumps(gravado, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"SONDAGEM DO FRIO: {'PASSOU' if veredito['passou'] else 'NÃO PASSOU'}")
        print(veredito["frase"])
        print(f"veredito gravado em {raiz / ARQUIVO_DA_SONDAGEM}")
        return 0 if veredito["passou"] else 1
    if args.incidente:
        incidente = INCIDENTES.get(args.incidente)
        if incidente is None:
            print(f"não há incidente registrado para a corrida {args.incidente}: use um de {sorted(INCIDENTES)}")
            return 2
        oficial_do_incidente = caminhos.RESULTADOS / incidente["pasta"]
        bruto = ler_agente(incidente["saida"])
        if not bruto["registros"]:
            print(f"sem cenarios.jsonl em {caminhos.RESULTADOS / incidente['saida']}")
            return 2
        dado = resumir_agente(bruto, corrida=incidente["saida"], incidente=incidente["motivo"])
        return _fechar("agente", dado, render_agente(dado, incidente["prefixo"]), incidente["prefixo"], args, Path(args.pasta) if args.pasta else oficial_do_incidente,
                       oficial=oficial_do_incidente)
    if args.antes:
        referencia = ler_referencia()
        if referencia is None:
            print(f"!! sem condicoes_fase4.json da corrida 21d em {caminhos.RESULTADOS / CORRIDA_DE_REFERENCIA}")
            return 2
        hoje = identidade_de_hoje(ler_navegador=lambda: versao_do_navegador(args.canal))
        itens = comparar_identidade(hoje, referencia)
        print(f"o agente de hoje contra o da corrida 21d ({CORRIDA_DE_REFERENCIA}/condicoes_fase4.json):")
        print("\n".join(_tabela_da_identidade(itens)))
        difere = o_que_difere(itens)
        if hoje["navegador"] is None:
            print("!! a versão do navegador não foi lida: rode com o Python da venv do AgenteCore (..\\.venv\\Scripts\\python.exe), onde está o Playwright")
            return 2
        if difere:
            print("!! o agente de hoje NÃO é o da corrida 21d: difere em " + ", ".join(NOME_DO_ITEM[i] for i in difere) + ". A noite da Fase 5 não roda assim")
            return 1
        print("o agente de hoje é o da corrida 21d nos seis itens que identificam o agente; a noite pode rodar")
        return 0
    if args.custo:
        saida = args.saida or CORRIDA_DE_REFERENCIA
        if not (caminhos.RESULTADOS / saida / "cenarios.jsonl").exists():
            print(f"sem cenarios.jsonl em {caminhos.RESULTADOS / saida}")
            return 2
        dado = resumir_custo(ler_custo(saida))
        return _fechar("custo", dado, render_custo(dado), "tb_f5_custo_", args, pasta)
    if args.agente:
        dado = _agente_lido(args, oficial)
        return 2 if dado is None else _fechar("agente", dado, render_agente(dado), "tb_f5_agente_", args, pasta)
    if args.manual:
        dado = _manual_lido(args)
        return 2 if dado is None else _fechar("manual", dado, render_manual(dado), "tb_f5_manual_", args, pasta)
    agente = _agente_lido(args, oficial)
    manual = _manual_lido(args) if agente is not None else None
    if agente is None or manual is None:
        return 2
    # (24/11/2026, decisão 151) as medidas das pessoas, da mesma planilha e do mesmo registro que `_manual_lido` acabou de aceitar, para a conta exploratória sem a
    # sessão de cada integrante; a planilha já passou pela conferência, então aqui não há recusa
    planilha = Path(args.planilha) if args.planilha else lbm.PLANILHA
    sessao = Path(args.sessao) if args.sessao else PASTA_DA_SESSAO / REGISTRO_DA_SESSAO
    medidas = conferir_planilha(ler_planilha_do_arquivo(planilha), ler_sessao(sessao))["medidas"]
    dado = resumir_medicao(agente, manual, medidas_das_pessoas=medidas)
    return _fechar("medicao", dado, render_medicao(dado), "tb_f5_medicao_", args, pasta)


if __name__ == "__main__":
    sys.exit(main())
