#!/usr/bin/env python3
# ! Alteração de IA - Revisar: cria testar_fase5.py, o runner de testes da Fase 5 (pacote F1: a leitura `avaliar_fase5.py` e o lançador da noite medida,
# `rodar_fase5.ps1`), no mesmo formato sem pytest de testar_pos_fase4.py: funções teste_<nome>(), main() roda todas em ordem de definição e termina em
# "N testes ok". A tag deste cabeçalho cobre as funções de teste e os ajudantes de teste. Os testes foram escritos ANTES do código: a primeira rodada falha
# por ModuleNotFoundError em `avaliar_fase5`, e, com o módulo ainda vazio, cada teste falha por AttributeError na função que ele chama.
# ! Motivo: o plano aprovado da Fase 5 (seções 2, 4.6, 5 e 8, pacote F1) manda escrever e testar as regras de leitura L1 a L15 com dados de mentira antes
# da noite do agente (corrida 28) e antes da primeira sessão com pessoa, para a comparação entre o agente e as pessoas não ser escolhida depois de ver os
# números. O que os testes fixam: a média por cenário e a média das médias dos cenários (regras L3 e L4); a medida sem fim de cronômetro fora da média do
# tempo e dentro do Task Success, com a segunda conta de 600 s (L6); o intervalo de Wilson e a contagem por cenário (L5); a reamostragem dos cenários
# dentro de cada tipo, com a semente de `avaliar_fase4` (L7); o teste exato dos sinais com empate abaixo de 5 s e com um lado sem fim (L8); as três frases
# da regra L9; o tipo de cenário sem veredito (L10); a comparação do Task Success (L11); as faixas de cada lado (L12); o que é só descrição (L13); a linha
# anulada (L14); a leitura da planilha da linha de base manual com planilhas de mentira (seção 4.6: completa, incompleta, tempo que não fecha, causa fora
# da lista, estouro do limite, fora da ordem e linha anotada à mão); a leitura rodada sobre os registros reais da corrida 21d, gravando numa pasta
# temporária, com os mesmos números da leitura vigente; o custo da noite; a conferência de que o agente de hoje é o da corrida 21d; e o lançador em modo
# `-Simular`. O arquivo roda com o Python do PATH, sem navegador, sem banco e sem modelo.
# ! Alteração de IA - Revisar: (18/11/2026, corrida 28b, decisões 145 e 146) testes novos e testes mudados, escritos antes do código: a conferência de que a noite
# rodou a frio, por repetição, com os registros da barra de progresso da corrida 28 (a repetição 1 passa, as repetições 2 a 5 não); a leitura oficial que só grava
# a noite completa e a frio; a corrida 28 guardada como incidente, em pasta e com blocos próprios; o veredito da sondagem do frio; `--situacao` dizendo quantas
# repetições estão completas e de qual versão do Ollama; o lançador com uma repetição por vez (descarregar o modelo, conferir, rodar, cinco vezes) na pasta nova;
# e o lançador da sondagem.
# ! Motivo: o Eric decidiu refazer a noite do agente com tudo fechado (decisão 145) e a frio (decisão 146), porque na corrida 28 o Ollama reaproveitou nas
# repetições 2 a 5 o prompt lido na repetição 1. O limite que diz "a frio" é fixado aqui, antes da noite nova, e não depois de ver os números dela.
"""Testes da Fase 5 (pacote F1), sem pytest (asserts em Python puro). Uso (em Programacao/AgenteCore/experimentos):
  PYTHONIOENCODING=utf-8 python testar_fase5.py
"""
import argparse
import base64
import contextlib
import copy
import csv
import datetime as dt
import hashlib
import inspect
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import traceback
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    with contextlib.suppress(OSError, ValueError, AttributeError):
        sys.stdout.reconfigure(encoding="utf-8")

# os caminhos padrão da leitura saem de caminhos.RESULTADOS, que lê esta variável na importação
os.environ.setdefault("RESULTADOS_DIR", "resultados_alvo")

EXP = Path(__file__).resolve().parent
AGENTE = EXP.parent
RAIZ = AGENTE.parent.parent
RA = EXP / "resultados_alvo"
CORRIDA_21D = "fase4_ensaio_v4"                    # a pasta da corrida 21d, o ensaio vigente dos dez cenários
LEITURA_VIGENTE = RA / "fase4" / "cenarios_v4.json"   # a leitura vigente da corrida 21d (avaliar_fase4.py --cenarios)
CORRIDA_28 = "fase5_agente"                        # a noite de 18/11/2026, guardada como incidente (decisão 145): 50 execuções, quatro repetições com o prompt reaproveitado

import avaliar
import avaliar_fase4 as av
import cenarios_fase4 as cen
import linha_de_base_manual as lbm
import taxonomia

import avaliar_fase5 as f5

_TEMPORARIOS: list[Path] = []
CATALOGO = {c["id"]: c for c in cen.CENARIOS_DO_ENSAIO}
CENARIOS = list(CATALOGO)
DE_CONTRATO = [cid for cid in CENARIOS if CATALOGO[cid]["tipo"] == "contrato"]
DE_LOCALIZADOR = [cid for cid in CENARIOS if CATALOGO[cid]["tipo"] == "localizador"]
INICIO_DA_SESSAO = dt.datetime(2026, 11, 19, 14, 0, 0)


def _temp() -> Path:
    p = Path(tempfile.mkdtemp(prefix="fase5_teste_"))
    _TEMPORARIOS.append(p)
    return p


def _hash_conteudo(raiz: Path) -> str:
    """sha256 de (caminho relativo, conteúdo) de cada arquivo sob a pasta, em ordem: prova que a leitura não tocou nos registros."""
    h = hashlib.sha256()
    for p in sorted(raiz.rglob("*")):
        if p.is_file():
            h.update(p.relative_to(raiz).as_posix().encode("utf-8") + b"\0" + p.read_bytes() + b"\0")
    return h.hexdigest()


def _rodar(*argumentos: str) -> tuple[int, str]:
    """Chama avaliar_fase5.main com os argumentos e devolve o código de saída e o que foi impresso."""
    saida = io.StringIO()
    with contextlib.redirect_stdout(saida), contextlib.redirect_stderr(saida):
        try:
            codigo = f5.main(list(argumentos))
        except SystemExit as e:
            codigo = e.code if isinstance(e.code, int) else 1
    return codigo, saida.getvalue()


def _medida(cenario: str, quem: int, tempo_s: float | None, sucesso: bool = True) -> dict:
    return f5.medida(cenario, CATALOGO[cenario]["tipo"], quem, sucesso, tempo_s)


def _lado(tempo, quantos: int, sucesso=lambda cid, quem: True) -> list[dict]:
    """As medidas de um lado nos dez cenários: `tempo(cid, quem)` em segundos (None = sem fim), `quantos` medidas por cenário."""
    return [_medida(cid, quem, tempo(cid, quem), sucesso(cid, quem)) for cid in CENARIOS for quem in range(1, quantos + 1)]


def _execucao(cenario: str, repeticao: int, mttr_s: float | None, sucesso: bool = True, rotulo: str | None = None) -> dict:
    """Um registro de cenarios.jsonl com os campos que a leitura usa, no formato que executar_fase4.py grava."""
    c = CATALOGO[cenario]
    return {"cenario": cenario, "tipo": c["tipo"], "modo": c["modo"], "causa_esperada": c["causa"], "repeticao": repeticao, "navegador": "156.0.8078.4",
            "hash_inicio": "9fe5e7cb64288c9d", "detectou": True, "mttr_s": mttr_s, "task_success": sucesso, "rotulo": rotulo or c["causa"],
            "segundos": None if mttr_s is None else round(mttr_s + 2.0, 3)}


# ----------------------------------------------------------------------------- regras L3 a L7: um lado

def teste_media_por_cenario_e_media_das_medias_dos_cenarios():
    a, b = DE_CONTRATO[0], DE_CONTRATO[1]
    medidas = [_medida(a, 1, 10.0), _medida(a, 2, 20.0), _medida(a, 3, 30.0), _medida(b, 1, 100.0)]
    r = f5.resumir_lado(medidas)
    por = {x["cenario"]: x for x in r["por_cenario"]}
    assert [x["cenario"] for x in r["por_cenario"]] == CENARIOS, "a tabela por cenário traz os dez, na ordem do catálogo, mesmo sem medida"
    assert (por[a]["n"], por[a]["tempo_media_s"], por[a]["tempo_min_s"], por[a]["tempo_max_s"]) == (3, 20.0, 10.0, 30.0), por[a]
    assert (por[b]["n"], por[b]["tempo_media_s"], por[b]["tempo_min_s"], por[b]["tempo_max_s"]) == (1, 100.0, 100.0, 100.0), por[b]
    assert por[DE_LOCALIZADOR[0]]["n"] == 0 and por[DE_LOCALIZADOR[0]]["tempo_media_s"] is None, por[DE_LOCALIZADOR[0]]
    # regras L3 e L4: no geral, a média das médias dos cenários (60), e não a média das quatro medidas (40)
    assert r["geral"]["tempo_media_s"] == 60.0 and r["geral"]["cenarios_com_tempo"] == 2 and r["geral"]["n"] == 4, r["geral"]
    tipos = {x["tipo"]: x for x in r["por_tipo"]}
    assert list(tipos) == ["contrato", "localizador"], list(tipos)
    assert tipos["contrato"]["tempo_media_s"] == 60.0 and tipos["localizador"]["tempo_media_s"] is None and tipos["localizador"]["n"] == 0, tipos


def teste_medida_sem_fim_fica_fora_da_media_do_tempo_e_dentro_do_task_success():
    a, b = DE_CONTRATO[0], DE_LOCALIZADOR[0]
    medidas = [_medida(a, 1, 10.0), _medida(a, 2, None, sucesso=False), _medida(a, 3, None, sucesso=False),
               _medida(b, 1, None, sucesso=False), _medida(b, 2, None, sucesso=False)]
    r = f5.resumir_lado(medidas)
    por = {x["cenario"]: x for x in r["por_cenario"]}
    # regra L6: a média do tempo só com quem chegou ao fim; o Task Success conta as três
    assert (por[a]["n"], por[a]["sucessos"], por[a]["com_fim"], por[a]["sem_fim"], por[a]["tempo_media_s"]) == (3, 1, 1, 2, 10.0), por[a]
    assert (por[b]["com_fim"], por[b]["sem_fim"], por[b]["tempo_media_s"], por[b]["tempo_min_s"]) == (0, 2, None, None), por[b]
    assert r["geral"]["tempo_media_s"] == 10.0 and r["geral"]["cenarios_com_tempo"] == 1, "cenário em que ninguém chegou ao fim fica fora da média das médias"
    assert (r["geral"]["n"], r["geral"]["sucessos"], r["geral"]["com_fim"], r["geral"]["sem_fim"]) == (5, 1, 1, 4), r["geral"]
    # a segunda conta, declarada como piso: cada medida sem fim entra com o limite de 600 s
    assert f5.LIMITE_S == 600.0, "o limite é o do protocolo da linha de base manual, 10 minutos"
    assert por[a]["piso_media_s"] == round((10.0 + 600.0 + 600.0) / 3, 3) and por[b]["piso_media_s"] == 600.0, (por[a], por[b])
    assert r["geral"]["piso_media_s"] == round(((10.0 + 600.0 + 600.0) / 3 + 600.0) / 2, 2), r["geral"]


def teste_task_success_com_wilson_e_a_contagem_por_cenario():
    falhas = {(DE_CONTRATO[0], 1), (DE_CONTRATO[0], 2), (DE_LOCALIZADOR[1], 5)}
    r = f5.resumir_lado(_lado(lambda cid, quem: 70.0, f5.REPETICOES, sucesso=lambda cid, quem: (cid, quem) not in falhas))
    g = r["geral"]
    total = len(CENARIOS) * f5.REPETICOES
    assert (g["n"], g["sucessos"]) == (total, total - len(falhas)), g
    assert g["task_success_pct"] == round(100 * (total - len(falhas)) / total, 1), g
    assert (g["wilson_lo_pct"], g["wilson_hi_pct"]) == avaliar.wilson(total - len(falhas), total), "regra L5: intervalo de Wilson de 95% no Task Success"
    # regra L5: em quantos dos dez cenários todas as medidas tiveram Task Success
    assert g["cenarios"] == len(CENARIOS) and g["cenarios_com_todas_certas"] == len(CENARIOS) - 2, g
    tipos = {x["tipo"]: x for x in r["por_tipo"]}
    n_contrato = len(DE_CONTRATO) * f5.REPETICOES
    assert (tipos["contrato"]["n"], tipos["contrato"]["sucessos"]) == (n_contrato, n_contrato - 2), tipos["contrato"]
    assert (tipos["contrato"]["wilson_lo_pct"], tipos["contrato"]["wilson_hi_pct"]) == avaliar.wilson(n_contrato - 2, n_contrato), tipos["contrato"]
    por = {x["cenario"]: x for x in r["por_cenario"]}
    assert por[DE_CONTRATO[0]]["parcela_pct"] == 60.0 and por[DE_CONTRATO[0]]["todas_certas"] is False and por[DE_CONTRATO[1]]["todas_certas"] is True, por[DE_CONTRATO[0]]


def teste_reamostragem_dos_cenarios_dentro_de_cada_tipo_com_a_semente_fixa():
    assert f5.SEMENTE == av.SEMENTE_DA_REAMOSTRAGEM and f5.REAMOSTRAS == av.REAMOSTRAS, "a semente e o número de reamostras são os de avaliar_fase4, não outros"
    # regra L7: o sorteio é dentro de cada tipo, então a mistura de seis e quatro não muda: toda reamostra tem média 40
    por_tipo = {"contrato": [0.0] * 6, "localizador": [100.0] * 4}
    assert f5.reamostrar_por_tipo(por_tipo) == (40.0, 40.0), f5.reamostrar_por_tipo(por_tipo)
    lo, hi = av.bootstrap_media([0.0] * 6 + [100.0] * 4)
    assert lo < 40.0 < hi, "sem separar por tipo, a mistura muda de uma reamostra para outra, e o intervalo abre"
    # com um tipo só, é a mesma conta de avaliar_fase4.bootstrap_media
    valores = [92.743, 73.352, 73.136, 73.439, 91.157, 84.968]
    assert f5.reamostrar_por_tipo({"contrato": valores}) == av.bootstrap_media(valores)
    # a mesma semente dá sempre o mesmo intervalo; outra semente, outro
    dois = {"contrato": valores, "localizador": [73.322, 42.291, 66.436, 68.815]}
    assert f5.reamostrar_por_tipo(dois) == f5.reamostrar_por_tipo(copy.deepcopy(dois))
    assert f5.reamostrar_por_tipo(dois, semente=f5.SEMENTE + 1) != f5.reamostrar_por_tipo(dois)
    lo, hi = f5.reamostrar_por_tipo(dois)
    media = sum(valores + dois["localizador"]) / 10
    assert lo < media < hi, (lo, media, hi)
    # sem valor nenhum não há intervalo; com um só, o intervalo é o próprio valor; valor ausente não entra
    assert f5.reamostrar_por_tipo({}) == (None, None) and f5.reamostrar_por_tipo({"contrato": [], "localizador": [None]}) == (None, None)
    assert f5.reamostrar_por_tipo({"contrato": [12.5]}) == (12.5, 12.5)
    assert f5.reamostrar_por_tipo({"contrato": valores + [None]}) == f5.reamostrar_por_tipo({"contrato": valores})


def teste_intervalo_do_tempo_medio_usa_a_reamostragem_por_tipo():
    tempos = {cid: 60.0 + 7.0 * i for i, cid in enumerate(CENARIOS)}
    r = f5.resumir_lado(_lado(lambda cid, quem: tempos[cid] + quem, 3))
    medias = {cid: tempos[cid] + 2.0 for cid in CENARIOS}
    esperado = f5.reamostrar_por_tipo({"contrato": [medias[c] for c in DE_CONTRATO], "localizador": [medias[c] for c in DE_LOCALIZADOR]})
    assert (r["geral"]["tempo_ic_lo_s"], r["geral"]["tempo_ic_hi_s"]) == esperado, (r["geral"], esperado)
    tipos = {x["tipo"]: x for x in r["por_tipo"]}
    assert (tipos["localizador"]["tempo_ic_lo_s"], tipos["localizador"]["tempo_ic_hi_s"]) == av.bootstrap_media([medias[c] for c in DE_LOCALIZADOR]), tipos["localizador"]


# ----------------------------------------------------------------------------- regras L8 a L12: a comparação

def teste_direcao_do_tempo_com_empate_abaixo_de_cinco_segundos_e_com_um_lado_sem_fim():
    assert f5.EMPATE_S == 5.0, "regra L8: diferença menor que 5 s, a folga do cronômetro das pessoas, conta como empate"
    assert f5.direcao_do_tempo(70.0, 300.0) == "agente" and f5.direcao_do_tempo(300.0, 70.0) == "pessoas"
    assert f5.direcao_do_tempo(70.0, 74.99) == "empate" and f5.direcao_do_tempo(74.99, 70.0) == "empate" and f5.direcao_do_tempo(70.0, 70.0) == "empate"
    assert f5.direcao_do_tempo(70.0, 75.0) == "agente" and f5.direcao_do_tempo(75.0, 70.0) == "pessoas", "cinco segundos exatos já não é menor que 5 s"
    # cenário em que só um lado chegou ao fim conta para esse lado
    assert f5.direcao_do_tempo(70.0, None) == "agente" and f5.direcao_do_tempo(None, 80.0) == "pessoas" and f5.direcao_do_tempo(None, None) == "sem_medida"


def teste_teste_dos_sinais_e_a_conta_do_mcnemar_exato_sem_os_empates():
    s = f5.teste_dos_sinais(["agente"] * 9 + ["pessoas"])
    assert (s["agente"], s["pessoas"], s["empates"], s["sem_medida"], s["p"]) == (9, 1, 0, 0, avaliar.mcnemar_exato(9, 1)), s
    # os valores que a regra L9 do plano cita, pela conta que o projeto já usa
    assert (avaliar.mcnemar_exato(9, 1), avaliar.mcnemar_exato(10, 0), avaliar.mcnemar_exato(8, 2)) == (0.0215, 0.002, 0.1094)
    s = f5.teste_dos_sinais(["agente"] * 7 + ["empate", "empate", "sem_medida"])
    assert (s["agente"], s["pessoas"], s["empates"], s["sem_medida"], s["p"]) == (7, 0, 2, 1, avaliar.mcnemar_exato(7, 0)), "empate e cenário sem medida saem do teste"
    assert f5.teste_dos_sinais([])["p"] == 1.0


def teste_regra_l9_as_tres_frases_e_o_caso_sem_medida():
    def sinais(b: int, c: int, e: int = 0) -> dict:
        return {"agente": b, "pessoas": c, "empates": e, "sem_medida": 0, "p": avaliar.mcnemar_exato(b, c)}

    # 1) o intervalo não contém zero e o teste dá p abaixo de 0,05: a leitura afirma
    v = f5.regra_l9(230.0, 180.0, 270.0, sinais(10, 0))
    assert (v["caso"], v["lado"]) == ("veredito", "agente") and "agente reparou mais rápido" in v["frase"], v
    v = f5.regra_l9(-40.0, -70.0, -12.0, sinais(1, 9))
    assert (v["caso"], v["lado"]) == ("veredito", "pessoas") and "pessoas repararam mais rápido" in v["frase"], v
    # 2) o intervalo contém zero: dentro do ruído, mesmo com o teste abaixo de 0,05
    for b, c in ((5, 5), (9, 1)):
        v = f5.regra_l9(8.0, -15.0, 31.0, sinais(b, c))
        assert (v["caso"], v["lado"]) == ("ruido", None) and "dentro do ruído" in v["frase"], v
    v = f5.regra_l9(8.0, 0.0, 31.0, sinais(9, 1))
    assert v["caso"] == "ruido", "o zero na ponta do intervalo conta como contido"
    # 3) o intervalo não contém zero, mas o teste não chega a 0,05: a média pende, sem veredito
    v = f5.regra_l9(120.0, 40.0, 190.0, sinais(7, 3))
    assert (v["caso"], v["lado"]) == ("pende", "agente") and "pende" in v["frase"] and "não dá veredito" in v["frase"], v
    # a média de um lado com a maioria dos cenários do outro também não é veredito: a direção da média não se repete nos cenários
    v = f5.regra_l9(50.0, 10.0, 90.0, sinais(1, 9))
    assert (v["caso"], v["lado"]) == ("pende", "agente") and "não dá veredito" in v["frase"], v
    # nos três casos os números aparecem: a diferença, o intervalo e o p
    for v in (f5.regra_l9(230.0, 180.0, 270.0, sinais(10, 0)), f5.regra_l9(8.0, -15.0, 31.0, sinais(6, 4)), f5.regra_l9(120.0, 40.0, 190.0, sinais(7, 3))):
        assert re.search(r"\d+,\d s", v["frase"]) and "p = 0," in v["frase"] and "intervalo de 95%" in v["frase"], v["frase"]
        assert "—" not in v["frase"] and "→" not in v["frase"], v["frase"]
    # sem cenário com os dois lados medidos, não há comparação
    v = f5.regra_l9(None, None, None, sinais(0, 0))
    assert (v["caso"], v["lado"]) == ("sem_medida", None), v
    assert f5.ALFA == 0.05


def teste_comparar_o_tempo_por_cenario_no_geral_e_as_tres_leituras():
    agente = f5.resumir_lado(_lado(lambda cid, quem: 70.0, f5.REPETICOES))
    # todas as pessoas a 300 s: dez cenários com o agente mais rápido
    m = f5.comparar(agente, f5.resumir_lado(_lado(lambda cid, quem: 300.0, f5.INTEGRANTES)))
    g = m["tempo"]["geral"]
    assert (g["diferenca_media_s"], g["ic_lo_s"], g["ic_hi_s"], g["cenarios_com_os_dois_lados"]) == (230.0, 230.0, 230.0, len(CENARIOS)), g
    assert g["razao_das_medias"] == round(300.0 / 70.0, 2), "a razão é o tempo médio das pessoas sobre o MTTR médio do agente"
    assert (g["sinais"]["agente"], g["sinais"]["pessoas"], g["sinais"]["p"]) == (len(CENARIOS), 0, avaliar.mcnemar_exato(len(CENARIOS), 0)), g["sinais"]
    assert (g["caso"], g["lado"]) == ("veredito", "agente"), g
    linha = m["tempo"]["por_cenario"][0]
    assert (linha["cenario"], linha["agente_media_s"], linha["pessoas_media_s"], linha["diferenca_s"], linha["razao"], linha["direcao"]) == \
        (CENARIOS[0], 70.0, 300.0, 230.0, round(300.0 / 70.0, 2), "agente"), linha
    # pessoas ora 10 s mais rápidas, ora 10 s mais lentas: a média das diferenças é zero, dentro do ruído
    m = f5.comparar(agente, f5.resumir_lado(_lado(lambda cid, quem: 60.0 if CENARIOS.index(cid) % 2 else 80.0, f5.INTEGRANTES)))
    g = m["tempo"]["geral"]
    assert g["diferenca_media_s"] == 0.0 and g["ic_lo_s"] <= 0.0 <= g["ic_hi_s"] and (g["caso"], g["lado"]) == ("ruido", None), g
    assert (g["sinais"]["agente"], g["sinais"]["pessoas"]) == (5, 5), g["sinais"]
    # sete cenários com o agente muito mais rápido e três com as pessoas um pouco mais rápidas: a média pende, o teste não chega a 0,05
    perto = {DE_CONTRATO[5], DE_LOCALIZADOR[1], DE_LOCALIZADOR[2]}
    m = f5.comparar(agente, f5.resumir_lado(_lado(lambda cid, quem: 63.0 if cid in perto else 270.0, f5.INTEGRANTES)))
    g = m["tempo"]["geral"]
    assert (g["sinais"]["agente"], g["sinais"]["pessoas"], g["sinais"]["p"]) == (7, 3, avaliar.mcnemar_exato(7, 3)), g["sinais"]
    assert g["ic_lo_s"] > 0.0 and (g["caso"], g["lado"]) == ("pende", "agente"), g
    # sem nenhuma medida das pessoas, a comparação não sai
    m = f5.comparar(agente, f5.resumir_lado([]))
    assert m["tempo"]["geral"]["caso"] == "sem_medida" and m["tempo"]["geral"]["diferenca_media_s"] is None, m["tempo"]["geral"]


def teste_comparar_empate_e_cenario_em_que_so_um_lado_chegou_ao_fim():
    so_agente, so_pessoas, empate = DE_CONTRATO[0], DE_CONTRATO[1], DE_LOCALIZADOR[0]

    def tempo_das_pessoas(cid: str, quem: int) -> float | None:
        return None if cid == so_agente else (72.0 if cid == empate else 300.0)

    def tempo_do_agente(cid: str, quem: int) -> float | None:
        return None if cid == so_pessoas else 70.0

    agente = f5.resumir_lado(_lado(tempo_do_agente, f5.REPETICOES, sucesso=lambda cid, quem: cid != so_pessoas))
    pessoas = f5.resumir_lado(_lado(tempo_das_pessoas, f5.INTEGRANTES, sucesso=lambda cid, quem: cid != so_agente))
    m = f5.comparar(agente, pessoas)
    por = {x["cenario"]: x for x in m["tempo"]["por_cenario"]}
    # regra L8: só um lado chegou ao fim: conta para esse lado no teste e fica fora da média das diferenças
    assert (por[so_agente]["direcao"], por[so_agente]["diferenca_s"]) == ("agente", None), por[so_agente]
    assert (por[so_pessoas]["direcao"], por[so_pessoas]["diferenca_s"]) == ("pessoas", None), por[so_pessoas]
    assert (por[empate]["direcao"], por[empate]["diferenca_s"]) == ("empate", 2.0), por[empate]
    g = m["tempo"]["geral"]
    assert g["cenarios_com_os_dois_lados"] == len(CENARIOS) - 2, g
    assert g["diferenca_media_s"] == round((230.0 * (len(CENARIOS) - 3) + 2.0) / (len(CENARIOS) - 2), 2), "o empate entra na média das diferenças; quem não tem os dois lados, não"
    assert (g["sinais"]["agente"], g["sinais"]["pessoas"], g["sinais"]["empates"]) == (len(CENARIOS) - 2, 1, 1), g["sinais"]
    assert g["sinais"]["p"] == avaliar.mcnemar_exato(len(CENARIOS) - 2, 1), g["sinais"]
    # a segunda conta (regra L6): com 600 s para quem não chegou ao fim, os dez cenários têm os dois lados
    piso = m["tempo"]["piso"]
    assert piso["cenarios_com_os_dois_lados"] == len(CENARIOS), piso
    por_piso = {x["cenario"]: x for x in piso["por_cenario"]}
    assert (por_piso[so_agente]["agente_s"], por_piso[so_agente]["pessoas_s"], por_piso[so_agente]["diferenca_s"]) == (70.0, 600.0, 530.0), por_piso[so_agente]
    assert (por_piso[so_pessoas]["agente_s"], por_piso[so_pessoas]["pessoas_s"], por_piso[so_pessoas]["diferenca_s"]) == (600.0, 300.0, -300.0), por_piso[so_pessoas]


def teste_por_tipo_de_cenario_a_leitura_mostra_os_numeros_e_nao_da_veredito():
    agente = f5.resumir_lado(_lado(lambda cid, quem: 70.0, f5.REPETICOES))
    m = f5.comparar(agente, f5.resumir_lado(_lado(lambda cid, quem: 300.0 if cid in DE_CONTRATO else 200.0, f5.INTEGRANTES)))
    tipos = {x["tipo"]: x for x in m["tempo"]["por_tipo"]}
    assert list(tipos) == ["contrato", "localizador"]
    assert (tipos["contrato"]["diferenca_media_s"], tipos["contrato"]["agente_mais_rapido"], tipos["contrato"]["cenarios_com_os_dois_lados"]) == (230.0, len(DE_CONTRATO), len(DE_CONTRATO))
    assert (tipos["localizador"]["diferenca_media_s"], tipos["localizador"]["ic_lo_s"], tipos["localizador"]["ic_hi_s"]) == (130.0, 130.0, 130.0), tipos["localizador"]
    for x in tipos.values():
        # regra L10: nem p, nem caso, nem lado: o tipo não tem veredito
        assert not {"p", "caso", "lado", "frase", "sinais"} & set(x), sorted(x)
    assert "sem veredito" in m["tempo"]["nota_por_tipo"] and "L10" in m["tempo"]["nota_por_tipo"], m["tempo"]["nota_por_tipo"]
    # os valores de p que a regra L10 cita: com seis cenários só seis de seis chega a 0,05; com quatro, nunca
    assert (avaliar.mcnemar_exato(len(DE_CONTRATO), 0), avaliar.mcnemar_exato(len(DE_LOCALIZADOR), 0)) == (0.0312, 0.125)


def teste_comparacao_do_task_success_pede_seis_cenarios_diferentes():
    assert f5.minimo_de_cenarios_para_veredito() == 6 and avaliar.mcnemar_exato(5, 0) == 0.0625, "regra L11: com cinco de cinco o teste não chega a 0,05"
    agente = f5.resumir_lado(_lado(lambda cid, quem: 70.0, f5.REPETICOES))

    def pessoas_errando_em(cenarios: list[str]) -> dict:
        return f5.resumir_lado(_lado(lambda cid, quem: 300.0, f5.INTEGRANTES, sucesso=lambda cid, quem: not (cid in cenarios and quem == 1)))

    # dois cenários diferentes: sem veredito, e sem p
    ts = f5.comparar(agente, pessoas_errando_em(CENARIOS[:2]))["task_success"]
    assert (ts["sinais"]["agente"], ts["sinais"]["pessoas"], ts["sinais"]["iguais"], ts["sinais"]["p"]) == (2, 0, len(CENARIOS) - 2, None), ts["sinais"]
    assert (ts["caso"], ts["lado"]) == ("sem_veredito", None) and "menos de 6" in ts["frase"], ts
    assert (ts["agente"]["sucessos"], ts["agente"]["n"], ts["pessoas"]["sucessos"], ts["pessoas"]["n"]) == (50, 50, 28, 30), ts
    assert (ts["pessoas"]["wilson_lo_pct"], ts["pessoas"]["wilson_hi_pct"]) == avaliar.wilson(28, 30), ts["pessoas"]
    linha = ts["por_cenario"][0]
    assert (linha["agente_pct"], linha["pessoas_pct"], linha["diferenca_pp"], linha["direcao"]) == (100.0, round(100 * 2 / 3, 1), round(100 - 100 * 2 / 3, 1), "agente"), linha
    assert ts["por_cenario"][5]["direcao"] == "igual", ts["por_cenario"][5]
    # seis de seis na mesma direção: o teste chega a 0,05
    ts = f5.comparar(agente, pessoas_errando_em(CENARIOS[:6]))["task_success"]
    assert (ts["sinais"]["agente"], ts["sinais"]["pessoas"], ts["sinais"]["p"]) == (6, 0, avaliar.mcnemar_exato(6, 0)), ts["sinais"]
    assert (ts["caso"], ts["lado"]) == ("veredito", "agente"), ts
    # seis diferentes, quatro para um lado e dois para o outro: o teste não separa
    agente_errando = f5.resumir_lado(_lado(lambda cid, quem: 70.0, f5.REPETICOES, sucesso=lambda cid, quem: not (cid in CENARIOS[4:6] and quem == 1)))
    ts = f5.comparar(agente_errando, pessoas_errando_em(CENARIOS[:4]))["task_success"]
    assert (ts["sinais"]["agente"], ts["sinais"]["pessoas"], ts["sinais"]["p"]) == (4, 2, avaliar.mcnemar_exato(4, 2)), ts["sinais"]
    assert (ts["caso"], ts["lado"]) == ("sem_diferenca", None), ts


def teste_faixas_de_cada_lado_e_se_elas_se_cruzam():
    a, b = CENARIOS[0], CENARIOS[1]
    agente = f5.resumir_lado(_lado(lambda cid, quem: 60.0 + 5.0 * (quem - 1), f5.REPETICOES))   # de 60 a 80 s em todo cenário
    pessoas = f5.resumir_lado(_lado(lambda cid, quem: {1: 75.0, 2: 200.0, 3: 400.0}[quem] if cid == a else {1: 200.0, 2: 300.0, 3: 400.0}[quem], f5.INTEGRANTES))
    por = {x["cenario"]: x for x in f5.comparar(agente, pessoas)["tempo"]["por_cenario"]}
    assert (por[a]["agente_min_s"], por[a]["agente_max_s"], por[a]["pessoas_min_s"], por[a]["pessoas_max_s"], por[a]["faixas_se_cruzam"]) == (60.0, 80.0, 75.0, 400.0, True), por[a]
    assert por[b]["faixas_se_cruzam"] is False, por[b]
    sem = f5.comparar(agente, f5.resumir_lado([]))["tempo"]["por_cenario"][0]
    assert sem["faixas_se_cruzam"] is None, "sem medida de um lado não há faixa para comparar"


# ----------------------------------------------------------------------------- a leitura do agente (corrida 28)

def teste_leitura_do_agente_com_a_noite_de_mentira():
    registros = [_execucao(cid, rep, 60.0 + CENARIOS.index(cid) + rep) for cid in CENARIOS for rep in range(1, f5.REPETICOES + 1)]
    registros[0] = _execucao(CENARIOS[0], 1, None, sucesso=False, rotulo="campo_ausente")            # uma execução sem fim de cronômetro
    registros[7] = _execucao(CENARIOS[1], 3, 64.0, sucesso=False, rotulo="tipo_divergente")           # uma com fim e sem Task Success
    dado = f5.resumir_agente({"registros": registros, "condicoes": {"repeticoes": f5.REPETICOES, "parcial": False}, "referencia": None}, corrida="noite_de_mentira",
                             gerado_em="2026-11-18T23:00:00")
    assert dado["noite"]["execucoes"] == 50 and dado["noite"]["esperadas"] == 50 and dado["noite"]["completa"] is True and dado["noite"]["faltam"] == [], dado["noite"]
    assert (dado["geral"]["n"], dado["geral"]["sucessos"], dado["geral"]["com_fim"], dado["geral"]["sem_fim"]) == (50, 48, 49, 1), dado["geral"]
    por = {x["cenario"]: x for x in dado["por_cenario"]}
    # regra L3: a média das repetições que chegaram ao fim, com o mínimo e o máximo
    assert (por[CENARIOS[0]]["com_fim"], por[CENARIOS[0]]["tempo_media_s"], por[CENARIOS[0]]["tempo_min_s"], por[CENARIOS[0]]["tempo_max_s"]) == (4, 63.5, 62.0, 65.0), por[CENARIOS[0]]
    # regra L13, só descrição: o rótulo de cada repetição, o tempo total da execução e a leitura só com as medidas que tiveram Task Success
    assert por[CENARIOS[0]]["rotulos"][0] == "campo_ausente" and len(por[CENARIOS[0]]["rotulos"]) == f5.REPETICOES, por[CENARIOS[0]]["rotulos"]
    assert por[CENARIOS[2]]["segundos_media_s"] == round(por[CENARIOS[2]]["tempo_media_s"] + 2.0, 3), por[CENARIOS[2]]
    assert (por[CENARIOS[1]]["tempo_media_s"], por[CENARIOS[1]]["estrita_n"], por[CENARIOS[1]]["estrita_media_s"]) == (64.0, 4, round((62 + 63 + 65 + 66) / 4, 3)), por[CENARIOS[1]]
    assert [(x["cenario"], x["repeticao"]) for x in dado["sem_task_success"]] == [(CENARIOS[0], 1), (CENARIOS[1], 3)], dado["sem_task_success"]
    # do lado do agente nenhuma execução é anulada (regra L14)
    assert "anuladas" not in dado, sorted(dado)
    # faltando uma execução, a noite não está completa, e a leitura diz qual falta
    dado = f5.resumir_agente({"registros": registros[:-1], "condicoes": {"repeticoes": f5.REPETICOES, "parcial": False}, "referencia": None}, corrida="x")
    assert dado["noite"]["completa"] is False and dado["noite"]["faltam"] == [f"{CENARIOS[-1]}#{f5.REPETICOES}"], dado["noite"]
    md = f5.render_agente(dado)
    for bloco in ("tb_f5_agente_resumo", "tb_f5_agente_por_tipo", "tb_f5_agente_por_cenario", "tb_f5_agente_noite", "tb_f5_agente_frio", "tb_f5_agente_sem_sucesso"):
        assert f"<!-- tabela:{bloco} -->" in md and f"<!-- /tabela:{bloco} -->" in md, bloco
    assert "de IA - Revisar" in md.split("\n")[0] and "! Motivo:" in md.split("\n")[1] and "—" not in md and "→" not in md


def teste_leitura_do_agente_sobre_a_corrida_21d_da_os_numeros_da_leitura_vigente():
    vigente = json.loads(LEITURA_VIGENTE.read_text(encoding="utf-8"))
    pasta = _temp()
    antes = _hash_conteudo(RA / CORRIDA_21D)
    codigo, saida = _rodar("--agente", "--saida", CORRIDA_21D, "--pasta", str(pasta))
    assert codigo == 0, saida
    dado = json.loads((pasta / "agente.json").read_text(encoding="utf-8"))
    assert (pasta / "agente.md").exists() and dado["metadados"]["corrida"] == CORRIDA_21D, sorted(p.name for p in pasta.iterdir())
    # os mesmos 10 de 10 e o mesmo MTTR médio da leitura vigente (avaliar_fase4.py --cenarios), lidos do arquivo dela
    assert (dado["geral"]["n"], dado["geral"]["sucessos"]) == (vigente["geral"]["n"], vigente["geral"]["sucessos"]), (dado["geral"], vigente["geral"])
    assert dado["geral"]["tempo_media_s"] == vigente["geral"]["mttr_media_s"], (dado["geral"]["tempo_media_s"], vigente["geral"]["mttr_media_s"])
    assert (dado["geral"]["wilson_lo_pct"], dado["geral"]["wilson_hi_pct"]) == (vigente["geral"]["wilson_lo_pct"], vigente["geral"]["wilson_hi_pct"])
    for tipo in vigente["por_tipo"]:
        meu = next(x for x in dado["por_tipo"] if x["tipo"] == tipo["tipo"])
        assert (meu["n"], meu["sucessos"], meu["tempo_media_s"]) == (tipo["n"], tipo["sucessos"], tipo["mttr_media_s"]), (meu, tipo)
        # com uma repetição por cenário, a reamostragem dentro do tipo é a mesma conta da leitura vigente
        assert (meu["tempo_ic_lo_s"], meu["tempo_ic_hi_s"]) == (tipo["mttr_ic_lo_s"], tipo["mttr_ic_hi_s"]), (meu, tipo)
    for linha in vigente["por_cenario"]:
        meu = next(x for x in dado["por_cenario"] if x["cenario"] == linha["cenario"])
        assert (meu["n"], meu["sucessos"]) == (linha["n"], linha["sucessos"]) and round(meu["tempo_media_s"], 2) == linha["mttr_media_s"], (meu, linha)
    # a 21d tem uma repetição: não é a noite completa, e a leitura diz isso
    assert (dado["noite"]["execucoes"], dado["noite"]["esperadas"], dado["noite"]["completa"]) == (len(CENARIOS), len(CENARIOS) * f5.REPETICOES, False), dado["noite"]
    assert dado["noite"]["navegador"] == vigente["navegador"] and dado["noite"]["banco"] == vigente["banco"], dado["noite"]
    assert dado["noite"]["linha_fim_no_log"] is True, dado["noite"]
    assert dado["noite"]["a_frio"] is None and "barra de progresso" in dado["noite"]["frio"]["motivo"], "a corrida 21d é de antes da barra de progresso: não dá para dizer se foi a frio"
    # a própria 21d contra ela mesma: os seis itens que identificam o agente batem
    assert all(i["igual"] for i in dado["mesmo_agente_da_21d"] if i["para"]) and len([i for i in dado["mesmo_agente_da_21d"] if i["para"]]) == 6, dado["mesmo_agente_da_21d"]
    codigo, saida = _rodar("--agente", "--saida", CORRIDA_21D, "--pasta", str(pasta), "--check")
    assert codigo == 0 and "batem" in saida, saida
    assert _hash_conteudo(RA / CORRIDA_21D) == antes, "a leitura só lê a pasta da corrida"
    # sem --pasta, uma corrida que não é a noite completa nunca grava em resultados_alvo/fase5
    existia = (RA / "fase5" / "agente.json").exists()
    codigo, saida = _rodar("--agente", "--saida", CORRIDA_21D)
    assert codigo == 2 and "não está completa" in saida and (RA / "fase5" / "agente.json").exists() == existia, saida


def teste_situacao_da_noite_diz_quantas_execucoes_e_repeticoes_estao_gravadas():
    # é o que o lançador pergunta antes de cada repetição: uma linha chave=valor por dado, sem gravar nada
    total = len(CENARIOS) * f5.REPETICOES
    codigo, saida = _rodar("--situacao", "--saida", CORRIDA_21D)
    assert codigo == 0 and saida.splitlines() == [f"execucoes={len(CENARIOS)}", f"esperadas={total}", "completa=nao", "repeticoes_completas=1", "versoes_ollama=0.40.14"], saida
    codigo, saida = _rodar("--situacao", "--saida", "pasta_que_nao_existe")
    assert codigo == 0 and saida.splitlines() == ["execucoes=0", f"esperadas={total}", "completa=nao", "repeticoes_completas=0", "versoes_ollama="], saida
    assert not (RA / "pasta_que_nao_existe").exists()
    codigo, saida = _rodar("--situacao", "--saida", CORRIDA_28)
    assert codigo == 0 and saida.splitlines() == [f"execucoes={total}", f"esperadas={total}", "completa=sim", f"repeticoes_completas={f5.REPETICOES}", "versoes_ollama=0.40.16"], saida
    noite = [_execucao(cid, rep, 70.0) for cid in CENARIOS for rep in range(1, f5.REPETICOES + 1)]
    assert f5.situacao_da_noite(noite, {"parcial": False}) == {"execucoes": 50, "esperadas": 50, "completa": True}
    assert f5.situacao_da_noite(noite[:-1], {"parcial": False})["completa"] is False and f5.situacao_da_noite(noite, {"parcial": True})["completa"] is False
    # as repetições completas contam do começo: é por onde o lançador retoma, uma repetição por vez
    assert f5.repeticoes_completas(noite) == f5.REPETICOES and f5.repeticoes_completas([]) == 0
    assert f5.repeticoes_completas(noite[:-1]) == f5.REPETICOES - 1, "falta a última execução da repetição 5"
    assert f5.repeticoes_completas([r for r in noite if r["repeticao"] == 1] + [r for r in noite if r["repeticao"] == 2][:4]) == 1
    assert f5.repeticoes_completas([r for r in noite if not (r["repeticao"] == 1 and r["cenario"] == CENARIOS[3])]) == 0, "a repetição 1 incompleta segura a contagem"


def teste_nada_e_gravado_em_fase5_antes_da_noite_salvo_o_custo():
    if (RA / f5.SAIDA_DO_AGENTE / "cenarios.jsonl").exists():
        print("  (a corrida 28 já tem registros: a pasta fase5 já pode ter as leituras)")
        return
    nomes = sorted(p.name for p in (RA / "fase5").iterdir()) if (RA / "fase5").exists() else []
    assert set(nomes) <= {"custo.json", "custo.md"}, f"antes das medidas, resultados_alvo/fase5 só tem o custo da noite: {nomes}"


# ----------------------------------------------------------------------------- a noite a frio (corrida 28b, decisões 145 e 146)

def _medidas_da_barra(saida: str) -> list[dict]:
    return [json.loads(linha) for linha in (RA / saida / "progresso_medidas.jsonl").read_text(encoding="utf-8").splitlines() if linha.strip()]


def _noite_com_barra(em_cache=lambda rep, i: 0 if i == 0 else 56, repeticoes: int = 5) -> tuple[list[dict], list[dict]]:
    """Uma noite de mentira com o registro da barra de progresso: `em_cache(rep, i)` diz quantos dos 1200 tokens de entrada da inferência de número i (de 0 a
    9) da repetição vieram do que o Ollama tinha guardado. As repetições começam de 20 em 20 minutos, e cada inferência termina 40 s depois da detecção."""
    registros, medidas = [], []
    for rep in range(1, repeticoes + 1):
        for i, cid in enumerate(CENARIOS):
            detectou = dt.datetime(2026, 11, 19, 21, 0, 0) + dt.timedelta(minutes=20 * (rep - 1) + i)
            registros.append({**_execucao(cid, rep, 60.0), "deteccao": detectou.isoformat(timespec="seconds")})
            sufixo = f"#{rep}@tela" if CATALOGO[cid]["tipo"] == "contrato" else "@cenario"   # o registro do localizador não traz a repetição
            medidas.append({"etapa": f"{cid}{sufixo} · diagnóstico", "concluido_em": (detectou + dt.timedelta(seconds=40)).isoformat(timespec="seconds"),
                            "medido": {"tokens_entrada": 1200, "tokens_em_cache": em_cache(rep, i), "prefill_s": 45.0, "carga_s": 8.0 if i == 0 else 0.03}})
    return registros, medidas


def teste_noite_a_frio_e_conferida_por_repeticao_com_os_registros_da_corrida_28():
    # o limite é fixado antes da corrida 28b, com o que a corrida 28 gravou: a repetição 1 leu o prompt de novo, e as repetições 2 a 5 reaproveitaram o guardado
    assert f5.LIMITE_DA_PARCELA_EM_CACHE == 0.5
    bruto = f5.ler_agente(CORRIDA_28)
    medidas = _medidas_da_barra(CORRIDA_28)
    assert bruto["medidas"] == medidas and len(medidas) == len(CENARIOS) * f5.REPETICOES
    frio = f5.conferir_frio(bruto["medidas"], bruto["registros"])
    por = {x["repeticao"]: x for x in frio["por_repeticao"]}
    assert sorted(por) == [1, 2, 3, 4, 5], sorted(por)
    for rep in por:
        # na corrida 28 as 50 inferências estão no arquivo na ordem em que rodaram, dez por repetição: a soma de cada bloco de dez é a da repetição
        bloco = medidas[(rep - 1) * len(CENARIOS): rep * len(CENARIOS)]
        entrada, guardados = sum(m["medido"]["tokens_entrada"] for m in bloco), sum(m["medido"]["tokens_em_cache"] for m in bloco)
        assert (por[rep]["inferencias"], por[rep]["tokens_entrada"], por[rep]["tokens_em_cache"]) == (len(CENARIOS), entrada, guardados), por[rep]
        assert por[rep]["parcela_em_cache_pct"] == round(100 * guardados / entrada, 1) and por[rep]["cache_na_primeira_inferencia"] == bloco[0]["medido"]["tokens_em_cache"], por[rep]
        assert por[rep]["prefill_s"] == round(sum(m["medido"]["prefill_s"] for m in bloco), 1), por[rep]
    assert por[1]["a_frio"] is True and por[1]["cache_na_primeira_inferencia"] == 0 and por[1]["parcela_em_cache_pct"] < 100 * f5.LIMITE_DA_PARCELA_EM_CACHE, por[1]
    for rep in (2, 3, 4, 5):
        assert por[rep]["a_frio"] is False and por[rep]["cache_na_primeira_inferencia"] > 0 and por[rep]["parcela_em_cache_pct"] > 100 * f5.LIMITE_DA_PARCELA_EM_CACHE, por[rep]
    assert frio["a_frio"] is False and "2, 3, 4 e 5" in frio["motivo"], frio["motivo"]
    # a leitura traz a conferência no bloco da noite, e a tabela por repetição
    dado = f5.resumir_agente(bruto, corrida=CORRIDA_28)
    assert dado["noite"]["completa"] is True and dado["noite"]["a_frio"] is False and dado["noite"]["frio"]["por_repeticao"] == frio["por_repeticao"], dado["noite"]
    assert dado["noite"]["frio"]["limite_da_parcela_em_cache"] == f5.LIMITE_DA_PARCELA_EM_CACHE
    md = f5.render_agente(dado)
    assert "<!-- tabela:tb_f5_agente_frio -->" in md and "a frio" in md and "—" not in md and "→" not in md


def teste_noite_a_frio_de_mentira_e_os_casos_em_que_a_conferencia_nao_passa():
    registros, medidas = _noite_com_barra()
    frio = f5.conferir_frio(medidas, registros)
    assert frio["a_frio"] is True and frio["motivo"] is None and [x["a_frio"] for x in frio["por_repeticao"]] == [True] * 5, frio
    assert frio["por_repeticao"][0]["parcela_em_cache_pct"] == round(100 * 9 * 56 / 12000, 1), "o começo do prompt que os cenários dividem vem guardado de um para o outro, dentro da repetição"
    # o registro do localizador não traz o número da repetição: a repetição sai da hora em que a inferência terminou
    assert all(x["inferencias"] == len(CENARIOS) for x in frio["por_repeticao"]), frio["por_repeticao"]
    # uma repetição em que a primeira inferência já veio com o prompt guardado não é a frio
    registros, medidas = _noite_com_barra(em_cache=lambda rep, i: 1199 if rep == 3 else (0 if i == 0 else 56))
    frio = f5.conferir_frio(medidas, registros)
    assert frio["a_frio"] is False and [x["a_frio"] for x in frio["por_repeticao"]] == [True, True, False, True, True] and "repetição 3" in frio["motivo"], frio
    # só a primeira inferência veio com o prompt guardado, e a parcela da repetição fica abaixo do limite: ainda assim não é a frio, porque o Ollama não começou vazio
    registros, medidas = _noite_com_barra(em_cache=lambda rep, i: 1199 if (rep, i) == (3, 0) else (0 if i == 0 else 56))
    frio = f5.conferir_frio(medidas, registros)
    assert frio["por_repeticao"][2]["parcela_em_cache_pct"] < 100 * f5.LIMITE_DA_PARCELA_EM_CACHE and frio["por_repeticao"][2]["a_frio"] is False and frio["a_frio"] is False, frio["por_repeticao"][2]
    # a primeira inferência sem nada guardado não basta: mais da metade dos tokens da repetição veio guardada
    registros, medidas = _noite_com_barra(em_cache=lambda rep, i: 0 if i == 0 else (1199 if rep == 2 else 56))
    frio = f5.conferir_frio(medidas, registros)
    assert frio["por_repeticao"][1]["cache_na_primeira_inferencia"] == 0 and frio["por_repeticao"][1]["a_frio"] is False and frio["a_frio"] is False, frio["por_repeticao"][1]
    # sem o registro da barra, ou sem ele numa repetição, a leitura não afirma que a noite foi a frio
    registros, medidas = _noite_com_barra()
    assert f5.conferir_frio([], registros)["a_frio"] is None and f5.conferir_frio(medidas, [])["a_frio"] is None
    ate_a_quarta = f5.conferir_frio([m for m in medidas if m["concluido_em"] < "2026-11-19T22:20:00"], registros)
    assert ate_a_quarta["a_frio"] is None and "repetição 5" in ate_a_quarta["motivo"], ate_a_quarta
    # o Ollama sem dizer quantos tokens vieram guardados: não medido
    registros, medidas = _noite_com_barra(em_cache=lambda rep, i: None if (rep, i) == (4, 5) else (0 if i == 0 else 56))
    frio = f5.conferir_frio(medidas, registros)
    assert frio["por_repeticao"][3]["a_frio"] is None and frio["a_frio"] is None, frio["por_repeticao"][3]
    # a repetição quente pesa mais que a repetição sem medida
    registros, medidas = _noite_com_barra(em_cache=lambda rep, i: None if rep == 4 else (1199 if rep == 5 else (0 if i == 0 else 56)))
    assert f5.conferir_frio(medidas, registros)["a_frio"] is False


def teste_leitura_oficial_so_grava_a_noite_completa_e_a_frio():
    assert f5.SAIDA_DO_AGENTE == "fase5_agente_b", "a leitura oficial é a da pasta nova, a da corrida 28b"
    existia = {nome: (RA / "fase5" / nome).exists() for nome in ("agente.json", "agente.md", "medicao.json")}
    # a corrida 28 está completa, mas quatro das cinco repetições reaproveitaram o prompt: não entra em resultados_alvo/fase5
    codigo, saida = _rodar("--agente", "--saida", CORRIDA_28)
    assert codigo == 2 and "não foi a frio" in saida and "2, 3, 4 e 5" in saida, saida
    codigo, saida = _rodar("--comparar", "--saida", CORRIDA_28)
    assert codigo == 2 and "não foi a frio" in saida, saida
    assert existia == {nome: (RA / "fase5" / nome).exists() for nome in existia}
    # em outra pasta ela é lida, e a leitura diz que não foi a frio
    pasta = _temp()
    codigo, saida = _rodar("--agente", "--saida", CORRIDA_28, "--pasta", str(pasta))
    assert codigo == 0 and json.loads((pasta / "agente.json").read_text(encoding="utf-8"))["noite"]["a_frio"] is False, saida
    # e uma leitura feita em outra pasta não é colada no relatório da fase
    codigo, saida = _rodar("--agente", "--saida", CORRIDA_28, "--pasta", str(pasta), "--colar")
    assert codigo == 2 and "--pasta" in saida, saida


def teste_corrida_28_fica_guardada_como_incidente_com_pasta_e_blocos_proprios():
    assert f5.INCIDENTES["28"]["saida"] == CORRIDA_28 and f5.INCIDENTES["28"]["pasta"] == "fase5_incidente_28" and f5.INCIDENTES["28"]["prefixo"] == "tb_f5_incidente28_"
    antes = _hash_conteudo(RA / CORRIDA_28)
    pasta = _temp()
    codigo, saida = _rodar("--incidente", "28", "--pasta", str(pasta))
    assert codigo == 0, saida
    dado, md = json.loads((pasta / "agente.json").read_text(encoding="utf-8")), (pasta / "agente.md").read_text(encoding="utf-8")
    assert dado["metadados"]["corrida"] == CORRIDA_28 and "decisão 145" in dado["metadados"]["incidente"], dado["metadados"]
    assert "não vale como a medida do agente" in md and "corrida 28b" in md, md[:900]
    for bloco in ("resumo", "por_tipo", "por_cenario", "noite", "frio", "identidade", "sem_sucesso"):
        assert f"<!-- tabela:tb_f5_incidente28_{bloco} -->" in md, bloco
    assert "tb_f5_agente_" not in md, "os blocos do incidente têm outro prefixo: não entram no lugar dos blocos do lado do agente"
    # os números são os dos registros da corrida, pela mesma leitura
    direto = json.loads(json.dumps(f5.resumir_agente(f5.ler_agente(CORRIDA_28), corrida=CORRIDA_28)))
    assert all(dado[k] == direto[k] for k in ("geral", "por_tipo", "por_cenario", "noite", "sem_task_success")), "a leitura do incidente é a leitura dos registros"
    assert (dado["noite"]["completa"], dado["noite"]["a_frio"], dado["geral"]["n"]) == (True, False, len(CENARIOS) * f5.REPETICOES), dado["noite"]
    assert _hash_conteudo(RA / CORRIDA_28) == antes, "a pasta da corrida 28 não é tocada"
    # a leitura do incidente está gravada na pasta dela e bate com os registros; a oficial não traz a corrida 28
    assert (RA / "fase5_incidente_28" / "agente.json").exists(), "rode `python avaliar_fase5.py --incidente 28` (com RESULTADOS_DIR=resultados_alvo)"
    codigo, saida = _rodar("--incidente", "28", "--check")
    assert codigo == 0, saida
    oficial = RA / "fase5" / "agente.json"
    if oficial.exists():
        assert json.loads(oficial.read_text(encoding="utf-8"))["metadados"]["corrida"] != CORRIDA_28, "resultados_alvo/fase5/agente.json não pode trazer a corrida 28 como a medida"
    codigo, saida = _rodar("--incidente", "99")
    assert codigo == 2 and "99" in saida, saida


def teste_sondagem_do_frio_passa_so_se_a_segunda_inferencia_ler_o_prompt_de_novo():
    # as duas primeiras inferências de um mesmo cenário na corrida 28: a segunda veio com o prompt guardado, que é o que a sondagem não pode aceitar
    da_28 = [m for m in _medidas_da_barra(CORRIDA_28) if m["etapa"].startswith(CENARIOS[0] + "#")][:2]
    assert len(da_28) == 2 and da_28[0]["medido"]["tokens_em_cache"] == 0 and da_28[1]["medido"]["tokens_em_cache"] > 0
    v = f5.sondagem_do_frio(da_28)
    assert v["passou"] is False and str(da_28[1]["medido"]["tokens_em_cache"]) in v["frase"] and len(v["inferencias"]) == 2, v
    frias = [{**m, "medido": {**m["medido"], "tokens_em_cache": 0}} for m in da_28]
    v = f5.sondagem_do_frio(frias)
    assert v["passou"] is True and v["cenario"] == CENARIOS[0], v
    # uma inferência só, cenários diferentes ou o Ollama sem dizer o que veio guardado: não passou
    assert f5.sondagem_do_frio(frias[:1])["passou"] is False and f5.sondagem_do_frio([])["passou"] is False
    assert f5.sondagem_do_frio([frias[0], {**frias[1], "etapa": CENARIOS[1] + "#2@tela · diagnóstico"}])["passou"] is False
    assert f5.sondagem_do_frio([frias[0], {**frias[1], "medido": {**frias[1]["medido"], "tokens_em_cache": None}}])["passou"] is False
    # pela linha de comando: lê a pasta da sondagem, diz PASSOU ou NÃO PASSOU, grava o veredito nela e sai com 0 ou 1
    pasta = _temp()
    (pasta / "progresso_medidas.jsonl").write_text("".join(json.dumps(m, ensure_ascii=False) + "\n" for m in frias), encoding="utf-8")
    codigo, saida = _rodar("--sondagem", "--saida", str(pasta))
    gravado = json.loads((pasta / "sondagem_frio.json").read_text(encoding="utf-8"))
    assert codigo == 0 and "PASSOU" in saida and "NÃO PASSOU" not in saida and gravado["passou"] is True, saida
    (pasta / "progresso_medidas.jsonl").write_text("".join(json.dumps(m, ensure_ascii=False) + "\n" for m in da_28), encoding="utf-8")
    codigo, saida = _rodar("--sondagem", "--saida", str(pasta))
    assert codigo == 1 and "NÃO PASSOU" in saida and json.loads((pasta / "sondagem_frio.json").read_text(encoding="utf-8"))["passou"] is False, saida
    codigo, saida = _rodar("--sondagem", "--saida", str(_temp()))
    assert codigo == 2, "pasta sem registro da barra de progresso: não há sondagem para ler"
    # é o que o lançador da noite pergunta: a última sondagem gravada, em linhas chave=valor
    raiz = _temp()
    assert f5.ultima_sondagem(raiz) is None
    for nome, passou in (("fase5_sondagem_frio_20261119_210000", False), ("fase5_sondagem_frio_20261119_213000", True)):
        (raiz / nome).mkdir()
        (raiz / nome / "sondagem_frio.json").write_text(json.dumps({"passou": passou, "versoes_ollama": ["0.40.16"]}), encoding="utf-8")
    (raiz / "fase5_sondagem_frio_20261119_220000").mkdir()   # uma sondagem que não chegou ao veredito não conta
    assert f5.ultima_sondagem(raiz) == {"pasta": "fase5_sondagem_frio_20261119_213000", "passou": True, "versoes_ollama": ["0.40.16"]}


# ----------------------------------------------------------------------------- o custo da noite e a conferência do agente

def teste_custo_da_noite_sai_dos_registros_da_corrida_21d():
    vigente = json.loads(LEITURA_VIGENTE.read_text(encoding="utf-8"))
    dado = f5.resumir_custo(f5.ler_custo(CORRIDA_21D), gerado_em="2026-11-17T09:00:00")
    r = dado["resumo"]
    log = (RA / CORRIDA_21D / "fase4.log").read_text(encoding="utf-8-sig")
    executor_s = int(re.search(r"FIM cenarios:.*duração (\d+) s", log).group(1))
    assert r["execucoes"] == len(CENARIOS) * f5.REPETICOES and r["segundos_do_executor_na_21d"] == executor_s, r
    # as duas pontas da seção 3.2 do plano: pelas execuções (a estimativa que a leitura vigente já traz) e pelo executor inteiro
    assert r["horas_pelas_execucoes"] == vigente["tempo"]["estimativa_fase5_h"], (r, vigente["tempo"])
    assert r["horas_pelo_executor"] == round(f5.REPETICOES * executor_s / 3600, 2), r
    # o que o rodar_fase4.ps1 gastou fora do executor (a bateria de testes e a leitura), pelas horas da primeira e da última linha do log
    marcas = [dt.datetime.strptime(m, "%Y-%m-%d %H:%M:%S") for m in re.findall(r"^\[(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d)\]", log, re.M)]
    assert r["segundos_fora_do_executor_na_21d"] == int((marcas[-1] - marcas[0]).total_seconds()) - executor_s, r
    # as três últimas pontes de pontes.json, com a duração da linha FIM do log de cada uma
    pontes = json.loads((RA / "fase4" / "pontes.json").read_text(encoding="utf-8"))["pontes"][-3:]
    assert [p["corrida"] for p in dado["pontes"]] == [p["corrida"] for p in pontes], dado["pontes"]
    for p in dado["pontes"]:
        fim = re.search(r"duracao total (\d\d)h(\d\d)", (RA / p["corrida"] / "fase3b.log").read_text(encoding="utf-8-sig", errors="replace"))
        assert p["minutos"] == int(fim.group(1)) * 60 + int(fim.group(2)), p
    minutos = [p["minutos"] for p in dado["pontes"]]
    assert (r["ponte_minutos_min"], r["ponte_minutos_max"]) == (min(minutos), max(minutos)), r
    assert isinstance(r["minutos_estimados_sem_ponte"], int) and r["minutos_estimados_com_ponte"] == r["minutos_estimados_sem_ponte"] + max(minutos), r
    assert r["minutos_estimados_sem_ponte"] * 60 >= f5.REPETICOES * executor_s + r["segundos_fora_do_executor_na_21d"] > (r["minutos_estimados_sem_ponte"] - 1) * 60, r
    assert r["minutos_estimados_com_ponte"] <= 120, "plano, seção 3.2: a noite inteira cabe em duas horas"
    md = f5.render_custo(dado)
    assert "<!-- tabela:tb_f5_custo_resumo -->" in md and "<!-- tabela:tb_f5_custo_pontes -->" in md and "—" not in md and "→" not in md


def teste_custo_gravado_em_fase5_bate_com_os_registros():
    assert (RA / "fase5" / "custo.json").exists(), "rode `python avaliar_fase5.py --custo` (com RESULTADOS_DIR=resultados_alvo)"
    codigo, saida = _rodar("--custo", "--check")
    assert codigo == 0, saida


def teste_identidade_do_agente_seis_itens_param_e_os_outros_so_informam():
    cond = json.loads((RA / CORRIDA_21D / "condicoes_fase4.json").read_text(encoding="utf-8"))
    registros = [json.loads(linha) for linha in (RA / CORRIDA_21D / "cenarios.jsonl").read_text(encoding="utf-8").splitlines() if linha.strip()]
    ref = f5.identidade_das_condicoes(cond, registros)
    assert f5.ITENS_QUE_PARAM == ("biblioteca", "prompt_fixo", "indice_da_busca", "k", "limiares", "navegador"), "plano, seção 3.4, etapa 2"
    assert (ref["biblioteca"], ref["prompt_fixo"], ref["indice_da_busca"], ref["k"]) == (cond["biblioteca"]["hash"], cond["hash_prompt_fixo"], cond["hash_indice"], cond["k"]), ref
    assert ref["navegador"] == registros[0]["navegador"] == cond["versoes"]["navegador"], ref["navegador"]
    assert ref["limiares"] == {k: v for k, v in cond["limiares"].items() if k != "gravado_em"}, "a data em que o arquivo dos limiares foi gravado não identifica o agente"
    itens = f5.comparar_identidade(copy.deepcopy(ref), ref)
    assert f5.o_que_difere(itens) == [] and [i["item"] for i in itens if i["para"]] == list(f5.ITENS_QUE_PARAM), itens
    for item in f5.ITENS_QUE_PARAM:
        hoje = copy.deepcopy(ref)
        hoje[item] = {**hoje[item], "baixo_ate": 0.5} if item == "limiares" else (hoje[item] + 1 if item == "k" else "outro")
        assert f5.o_que_difere(f5.comparar_identidade(hoje, ref)) == [item], item
    # o que o plano não lista como motivo para parar aparece na tabela e não para a noite: a versão do caso ao vivo passou de 4 a 5 depois da 21d
    hoje = copy.deepcopy(ref)
    hoje["versao_do_caso_ao_vivo"] = ref["versao_do_caso_ao_vivo"] + 1
    itens = f5.comparar_identidade(hoje, ref)
    caso = next(i for i in itens if i["item"] == "versao_do_caso_ao_vivo")
    assert f5.o_que_difere(itens) == [] and caso["igual"] is False and caso["para"] is False, caso
    # item que falta de um dos lados conta como diferente
    hoje = copy.deepcopy(ref)
    hoje["navegador"] = None
    assert f5.o_que_difere(f5.comparar_identidade(hoje, ref)) == ["navegador"]


def teste_agente_de_hoje_e_o_da_corrida_21d_sem_abrir_o_navegador():
    cond = json.loads((RA / CORRIDA_21D / "condicoes_fase4.json").read_text(encoding="utf-8"))
    registros = [json.loads(linha) for linha in (RA / CORRIDA_21D / "cenarios.jsonl").read_text(encoding="utf-8").splitlines() if linha.strip()]
    ref = f5.identidade_das_condicoes(cond, registros)
    # a biblioteca de produção, o prompt fixo, o índice da busca, o k e os limiares de hoje, lidos como o executor lê; a versão do navegador vem de fora
    hoje = f5.identidade_de_hoje(ler_navegador=lambda: ref["navegador"])
    difere = f5.o_que_difere(f5.comparar_identidade(hoje, ref))
    assert difere == [], f"o agente de hoje não é o da corrida 21d: difere em {difere}; a noite da Fase 5 não pode rodar assim (plano, princípio 2)"
    # com outra versão do navegador, a conferência acusa só o navegador
    hoje = f5.identidade_de_hoje(ler_navegador=lambda: "999.0.0.0")
    assert f5.o_que_difere(f5.comparar_identidade(hoje, ref)) == ["navegador"]
    # sem conseguir ler a versão do navegador, a conferência não passa
    hoje = f5.identidade_de_hoje(ler_navegador=lambda: None)
    assert f5.o_que_difere(f5.comparar_identidade(hoje, ref)) == ["navegador"]


# ----------------------------------------------------------------------------- a leitura da planilha da linha de base manual (seção 4.6)

def _virgula(valor: float) -> str:
    """O número como o comando `planilha` do ajudante grava: com vírgula decimal, para o Excel em português."""
    return f"{valor:.3f}".replace(".", ",")


def _mais(celula: str, delta: float) -> str:
    return _virgula(float(celula.replace(",", ".")) + delta)


def _evento(nome: str, n: int, posicao: int, cid: str, quando: dt.datetime, **campos) -> dict:
    """Um evento do registro da sessão, com os campos comuns do contrato do pacote F2 (registro 2)."""
    return {"registro": 2, "evento": nome, "integrante": n, "ordem": posicao, "cenario": cid, "tipo": CATALOGO[cid]["tipo"],
            "hora": quando.isoformat(timespec="milliseconds"), "relogio_s": round(quando.timestamp(), 3), **campos}


def _sessao_de_mentira(tempo=lambda n, pos, cid: 100.0 + 10.0 * pos, com_data: bool = False) -> tuple[list[dict], list[dict]]:
    """As 30 linhas da planilha preenchidas (na ordem sorteada, todas corrigidas) e os eventos do registro da sessão que as sustentam, no formato que o
    ajudante `linha_de_base_manual.py` grava na versão 2 do protocolo: na planilha, as horas em HH:MM:SS e os números com vírgula decimal; no registro, um
    `inicio` por vez, `entrega` e `resposta` no contrato e `tentativa` no localizador. Com `com_data`, a planilha leva a data, os milésimos e o ponto decimal."""
    linhas, eventos = [], []
    for n, ids in sorted(lbm.ordem_dos_integrantes().items()):
        eventos.append({"registro": 2, "evento": "treino", "integrante": n, "parte": "contrato", "hora": INICIO_DA_SESSAO.isoformat(timespec="milliseconds")})
        for pos, cid in enumerate(ids, 1):
            c = CATALOGO[cid]
            descontar = 0.0 if c["tipo"] == "contrato" else 2.5
            inicio = INICIO_DA_SESSAO + dt.timedelta(days=n - 1, minutes=12 * (pos - 1))
            fim = inicio + dt.timedelta(seconds=tempo(n, pos, cid) + descontar)
            linha = dict.fromkeys(lbm.COLUNAS_DA_PLANILHA, "")
            linha.update({"integrante": str(n), "ordem": str(pos), "cenario": cid, "tipo": c["tipo"], "corrigido": "sim"})
            if com_data:
                linha.update({"inicio": inicio.isoformat(timespec="milliseconds"), "fim": fim.isoformat(timespec="milliseconds"),
                              "segundos": f"{tempo(n, pos, cid):.3f}", "descontar_s": f"{descontar:.3f}"})
            else:
                linha.update({"inicio": inicio.strftime("%H:%M:%S"), "fim": fim.strftime("%H:%M:%S"), "segundos": _virgula(tempo(n, pos, cid)),
                              "descontar_s": _virgula(descontar) if descontar else "0"})
            eventos.append(_evento("inicio", n, pos, cid, inicio, navegador="156.0.8078.4", forma="php"))
            if c["tipo"] == "contrato":
                linha.update({"causa": c["causa"], "campo": c["campo"] or "nenhum"})
                eventos.append(_evento("entrega", n, pos, cid, fim))
                eventos.append(_evento("resposta", n, pos, cid, fim, causa=c["causa"], campo=c["campo"], corrigido=True, recusada=False))
            else:
                linha.update({"seletor": f"#novo-{pos}", "tentativas": "1"})
                eventos.append(_evento("tentativa", n, pos, cid, fim, seletor=linha["seletor"], corrigido=True, segundos_do_banco=descontar, segundos_do_roteiro=1.2, motivo=None))
            eventos.append(_evento("fim_do_armar", n, pos, cid, fim + dt.timedelta(seconds=3)))
            linhas.append(linha)
    return linhas, eventos


def _csv(linhas: list[dict]) -> str:
    saida = io.StringIO()
    w = csv.DictWriter(saida, fieldnames=lbm.COLUNAS_DA_PLANILHA, delimiter=lbm.SEPARADOR, lineterminator="\n")
    w.writeheader()
    w.writerows(linhas)
    return saida.getvalue()


def _norm_do_teste(texto: str) -> str:
    return avaliar._normalizar(texto).strip()


def _linha_de(linhas: list[dict], tipo: str, posicao: int = 0) -> int:
    """O índice (na lista) da linha de número `posicao` entre as do tipo pedido."""
    return [i for i, linha in enumerate(linhas) if linha["tipo"] == tipo][posicao]


def _recusas(linhas: list[dict], eventos: list[dict]) -> list[str]:
    try:
        f5.resumir_manual(f5.ler_planilha(_csv(linhas)), eventos)
    except f5.LeituraRecusada as e:
        return list(e.recusas)
    return []


def teste_planilha_completa_e_lida_com_as_trinta_tentativas():
    linhas, eventos = _sessao_de_mentira()
    assert len(linhas) == len(CENARIOS) * f5.INTEGRANTES == 30
    lidas = f5.ler_planilha(_csv(linhas))
    assert len(lidas) == 30 and lidas[0]["linha"] == 2 and lidas[-1]["linha"] == 31, "a linha é a do arquivo, com o cabeçalho na linha 1"
    dado = f5.resumir_manual(lidas, eventos, gerado_em="2026-11-25T10:00:00")
    g = dado["geral"]
    assert (g["n"], g["sucessos"], g["com_fim"], g["sem_fim"], g["cenarios"], g["cenarios_com_todas_certas"]) == (30, 30, 30, 0, 10, 10), g
    assert (g["wilson_lo_pct"], g["wilson_hi_pct"]) == avaliar.wilson(30, 30), g
    # regra L4: por cenário, a média dos integrantes; no geral, a média das médias
    ordens = lbm.ordem_dos_integrantes()
    medias = {cid: sum(100.0 + 10.0 * (ordens[n].index(cid) + 1) for n in ordens) / len(ordens) for cid in CENARIOS}
    por = {x["cenario"]: x for x in dado["por_cenario"]}
    for cid in CENARIOS:
        assert por[cid]["n"] == f5.INTEGRANTES and por[cid]["tempo_media_s"] == round(medias[cid], 3), (cid, por[cid], medias[cid])
    assert g["tempo_media_s"] == round(sum(medias.values()) / len(medias), 2), (g, medias)
    # regra L13, só descrição: o tempo pela posição na ordem, do primeiro ao décimo cenário de cada integrante
    assert [(x["posicao"], x["n"], x["tempo_media_s"]) for x in dado["por_posicao"]] == [(p, f5.INTEGRANTES, 100.0 + 10.0 * p) for p in range(1, 11)], dado["por_posicao"]
    assert dado["linhas"] == {"esperadas": 30, "preenchidas": 30, "anuladas": [], "anotadas_a_mao": [], "sem_fim": []}, dado["linhas"]
    md = f5.render_manual(dado)
    for bloco in ("tb_f5_manual_resumo", "tb_f5_manual_por_tipo", "tb_f5_manual_por_cenario", "tb_f5_manual_por_posicao", "tb_f5_manual_linhas"):
        assert f"<!-- tabela:{bloco} -->" in md, bloco
    assert "—" not in md and "→" not in md
    # o arquivo como o Excel grava: com BOM e separado por ponto e vírgula
    arq = _temp() / "planilha.csv"
    arq.write_text(_csv(linhas), encoding="utf-8-sig")
    assert f5.ler_planilha_do_arquivo(arq) == lidas


def teste_planilha_incompleta_sai_com_codigo_2_e_nao_mostra_numero():
    linhas, eventos = _sessao_de_mentira()
    for i in (4, 17, 29):
        linhas[i] = {**dict.fromkeys(lbm.COLUNAS_DA_PLANILHA, ""), **{k: linhas[i][k] for k in ("integrante", "ordem", "cenario", "tipo")}}
    recusas = _recusas(linhas, eventos)
    assert len(recusas) == 1 and "27 de 30" in recusas[0] and all(f"linha {n}" in recusas[0] for n in (6, 19, 31)), recusas
    pasta = _temp()
    (pasta / "planilha.csv").write_text(_csv(linhas), encoding="utf-8-sig")
    (pasta / "sessao.jsonl").write_text("".join(json.dumps(e, ensure_ascii=False) + "\n" for e in eventos), encoding="utf-8")
    codigo, saida = _rodar("--manual", "--planilha", str(pasta / "planilha.csv"), "--sessao", str(pasta / "sessao.jsonl"), "--pasta", str(pasta))
    assert codigo == 2 and "27 de 30" in saida, saida
    assert not (pasta / "manual.json").exists() and not (pasta / "manual.md").exists(), "planilha incompleta não grava leitura"
    assert "Task Success" not in saida and "tb_f5" not in saida and "%" not in saida, "planilha incompleta não mostra número de resultado"
    # a planilha em branco do repositório, como está antes das sessões, também sai com código 2
    if all(not linha["corrigido"] for linha in f5.ler_planilha_do_arquivo(lbm.PLANILHA)):
        codigo, saida = _rodar("--manual", "--pasta", str(pasta))
        assert codigo == 2 and "0 de 30" in saida, saida


def teste_planilha_com_tempo_que_nao_fecha_e_recusada_dizendo_a_linha():
    linhas, eventos = _sessao_de_mentira()
    linhas[3]["segundos"] = _mais(linhas[3]["segundos"], 2.0)
    recusas = _recusas(linhas, eventos)
    assert len(recusas) == 1 and recusas[0].startswith("linha 5 ") and "segundos" in recusas[0], recusas
    # a folga é de 1 s: a planilha guarda as horas sem os milésimos, e uma diferença menor que isso passa
    linhas, eventos = _sessao_de_mentira()
    linhas[3]["segundos"] = _mais(linhas[3]["segundos"], 0.4)
    assert _recusas(linhas, eventos) == []
    assert f5.FOLGA_S == 1.0
    # fim antes do início, hora que não se lê e tempo sem fim são recusados na mesma linha
    for campo, valor, trecho in (("fim", "13:00:00", "fim"), ("inicio", "duas e meia", "inicio"), ("fim", "", "fim")):
        linhas, eventos = _sessao_de_mentira()
        linhas[3][campo] = valor
        recusas = _recusas(linhas, eventos)
        assert len(recusas) == 1 and recusas[0].startswith("linha 5 ") and trecho in recusas[0], (campo, recusas)


def teste_planilha_com_causa_fora_da_lista_ou_corrigido_diferente_da_regra_e_recusada():
    linhas, eventos = _sessao_de_mentira()
    i = _linha_de(linhas, "contrato")
    linhas[i]["causa"] = "servidor_fora_do_ar"
    recusas = _recusas(linhas, eventos)
    assert len(recusas) == 1 and recusas[0].startswith(f"linha {i + 2} ") and "servidor_fora_do_ar" in recusas[0] and str(len(taxonomia.CAUSAS_RAIZ)) in recusas[0], recusas
    # causa da lista, mas que não é a do cenário: a regra dá "não", e a planilha diz "sim"
    linhas, eventos = _sessao_de_mentira()
    outra = next(c for c in taxonomia.CAUSAS_RAIZ if c != linhas[i]["causa"])
    linhas[i]["causa"] = outra
    recusas = _recusas(linhas, eventos)
    assert len(recusas) == 1 and recusas[0].startswith(f"linha {i + 2} ") and "corrigido" in recusas[0], recusas
    # com "não" na planilha a linha passa, e a tentativa conta no tempo e fica sem Task Success: o cronômetro para na entrega, certa ou errada
    linhas[i]["corrigido"] = "não"
    dado = f5.resumir_manual(f5.ler_planilha(_csv(linhas)), eventos)
    assert (dado["geral"]["n"], dado["geral"]["sucessos"], dado["geral"]["com_fim"]) == (30, 29, 30), dado["geral"]
    # o campo também entra na regra (cenarios_fase4.task_success_contrato): causa certa com o campo errado não é corrigido
    linhas, eventos = _sessao_de_mentira()
    j = next(k for k, linha in enumerate(linhas) if linha["tipo"] == "contrato" and CATALOGO[linha["cenario"]]["campo"])
    linhas[j]["campo"] = "nenhum"
    recusas = _recusas(linhas, eventos)
    assert len(recusas) == 1 and recusas[0].startswith(f"linha {j + 2} ") and "corrigido" in recusas[0], recusas
    # no localizador, "sim" pede no registro da sessão um conferir que passou com o seletor da planilha
    linhas, eventos = _sessao_de_mentira()
    k = _linha_de(linhas, "localizador")
    linhas[k]["seletor"] = "#outro-seletor"
    recusas = _recusas(linhas, eventos)
    assert len(recusas) == 1 and recusas[0].startswith(f"linha {k + 2} ") and "conferir" in recusas[0] and "#outro-seletor" in recusas[0], recusas
    linhas, eventos = _sessao_de_mentira()
    eventos = [{**e, "corrigido": False} if e["evento"] == "tentativa" and (e["integrante"], e["cenario"]) == (int(linhas[k]["integrante"]), linhas[k]["cenario"]) else e for e in eventos]
    assert len(_recusas(linhas, eventos)) == 1, "uma tentativa do conferir que não corrigiu não sustenta o corrigido da planilha"
    # valor de corrigido que não é sim nem não
    linhas, eventos = _sessao_de_mentira()
    linhas[0]["corrigido"] = "talvez"
    recusas = _recusas(linhas, eventos)
    assert len(recusas) == 1 and recusas[0].startswith("linha 2 ") and "talvez" in recusas[0], recusas


def teste_planilha_com_estouro_do_limite():
    # tempo acima do limite numa linha marcada como corrigida: recusada
    linhas, eventos = _sessao_de_mentira(tempo=lambda n, pos, cid: 601.0 if (n, pos) == (2, 4) else 100.0)
    recusas = _recusas(linhas, eventos)
    assert len(recusas) == 1 and recusas[0].startswith("linha 15 ") and "limite" in recusas[0], recusas
    # quem estourou o limite fica "não corrigido" e sem fim: fora da média do tempo, dentro do Task Success
    linhas, eventos = _sessao_de_mentira(tempo=lambda n, pos, cid: 100.0)
    i = 13
    linhas[i].update({"fim": "", "segundos": "", "corrigido": "não", "causa": "", "campo": "", "observacoes": "estourou os 10 minutos"})
    dado = f5.resumir_manual(f5.ler_planilha(_csv(linhas)), eventos)
    g = dado["geral"]
    assert (g["n"], g["sucessos"], g["com_fim"], g["sem_fim"], g["tempo_media_s"]) == (30, 29, 29, 1, 100.0), g
    assert dado["linhas"]["sem_fim"] == [{"linha": 15, "integrante": 2, "ordem": 4, "cenario": linhas[i]["cenario"]}], dado["linhas"]
    por = {x["cenario"]: x for x in dado["por_cenario"]}
    assert por[linhas[i]["cenario"]]["piso_media_s"] == round((100.0 + 100.0 + 600.0) / 3, 3), "na segunda conta a tentativa sem fim entra com 600 s"
    # linha sem fim marcada como corrigida não existe
    linhas[i]["corrigido"] = "sim"
    recusas = _recusas(linhas, eventos)
    assert len(recusas) == 1 and recusas[0].startswith("linha 15 "), recusas


def teste_planilha_fora_da_ordem_do_sorteio_e_recusada():
    linhas, eventos = _sessao_de_mentira()
    linhas[1], linhas[2] = linhas[2], linhas[1]
    recusas = _recusas(linhas, eventos)
    assert len(recusas) == 2 and recusas[0].startswith("linha 3 ") and recusas[1].startswith("linha 4 ") and all("sorteio" in r for r in recusas), recusas
    # cenário trocado e tipo trocado
    linhas, eventos = _sessao_de_mentira()
    i = _linha_de(linhas, "contrato")
    linhas[i]["tipo"] = "localizador"
    recusas = _recusas(linhas, eventos)
    assert recusas and recusas[0].startswith(f"linha {i + 2} ") and "sorteio" in recusas[0], recusas
    # linha a mais, linha a menos e cabeçalho com outra coluna
    linhas, eventos = _sessao_de_mentira()
    assert any("30" in r for r in _recusas(linhas[:-1], eventos)), _recusas(linhas[:-1], eventos)
    assert any("30" in r for r in _recusas(linhas + [linhas[-1]], eventos))
    try:
        f5.ler_planilha(_csv(linhas).replace("observacoes", "notas", 1))
    except f5.LeituraRecusada as e:
        assert "colunas" in e.recusas[0], e.recusas
    else:
        raise AssertionError("a leitura aceitou uma planilha com outro cabeçalho")


def teste_planilha_com_linha_anotada_a_mao_e_com_linha_anulada():
    # a ferramenta falhou num cenário de localizador: o registro da sessão não tem o conferir dele
    linhas, eventos = _sessao_de_mentira()
    i = _linha_de(linhas, "localizador", 2)
    n, cid = int(linhas[i]["integrante"]), linhas[i]["cenario"]
    eventos = [e for e in eventos if (e["integrante"], e.get("cenario")) != (n, cid)]
    recusas = _recusas(linhas, eventos)
    assert len(recusas) == 1 and recusas[0].startswith(f"linha {i + 2} ") and "conferir" in recusas[0] and f5.MARCA_A_MAO in recusas[0], recusas
    # com a marca nas observações (em qualquer ponto, sem diferença de maiúscula), a linha vale e fica contada como anotada à mão
    assert _norm_do_teste(f5.MARCA_A_MAO) == "anotada a mao" and f5.MARCA_A_MAO == getattr(lbm, "MARCA_A_MAO", f5.MARCA_A_MAO), "a marca é a do ajudante da sessão"
    linhas[i]["observacoes"] = "a ferramenta travou no conferir; linha ANOTADA À MÃO pelo cronômetro de reserva"
    dado = f5.resumir_manual(f5.ler_planilha(_csv(linhas)), eventos)
    assert dado["linhas"]["anotadas_a_mao"] == [{"linha": i + 2, "integrante": n, "ordem": int(linhas[i]["ordem"]), "cenario": cid}], dado["linhas"]
    assert (dado["geral"]["n"], dado["geral"]["sucessos"]) == (30, 30), dado["geral"]
    # a marca não dispensa as outras conferências: o tempo ainda precisa fechar
    linhas[i]["segundos"] = _mais(linhas[i]["segundos"], 30.0)
    assert len(_recusas(linhas, eventos)) == 1
    # regra L14: a linha anulada na hora é contada à parte e não entra em conta nenhuma; nada a substitui
    linhas, eventos = _sessao_de_mentira()
    j = 7
    linhas[j] = {**dict.fromkeys(lbm.COLUNAS_DA_PLANILHA, ""), **{k: linhas[j][k] for k in ("integrante", "ordem", "cenario", "tipo")},
                 "observacoes": "Anulada: a máquina travou com o cenário armado"}
    dado = f5.resumir_manual(f5.ler_planilha(_csv(linhas)), eventos)
    assert dado["linhas"]["anuladas"] == [{"linha": j + 2, "integrante": 1, "ordem": 8, "cenario": linhas[j]["cenario"]}] and dado["linhas"]["preenchidas"] == 30, dado["linhas"]
    por = {x["cenario"]: x for x in dado["por_cenario"]}
    assert dado["geral"]["n"] == 29 and por[linhas[j]["cenario"]]["n"] == f5.INTEGRANTES - 1, (dado["geral"], por[linhas[j]["cenario"]])
    # uma observação que só cita a palavra no meio do texto não anula a linha
    linhas, eventos = _sessao_de_mentira()
    linhas[j]["observacoes"] = "o integrante perguntou se a tentativa seria anulada"
    assert f5.resumir_manual(f5.ler_planilha(_csv(linhas)), eventos)["linhas"]["anuladas"] == []


def teste_planilha_aceita_ponto_decimal_e_hora_com_data_e_milesimos():
    # o comando `planilha` grava HH:MM:SS e vírgula decimal (é o formato dos outros testes); a leitura aceita também a data com os milésimos e o ponto decimal
    linhas, eventos = _sessao_de_mentira(tempo=lambda n, pos, cid: 123.4, com_data=True)
    assert "T" in linhas[0]["inicio"] and "." in linhas[0]["segundos"], linhas[0]
    dado = f5.resumir_manual(f5.ler_planilha(_csv(linhas)), eventos)
    assert (dado["geral"]["n"], dado["geral"]["tempo_media_s"]) == (30, 123.4), dado["geral"]
    linhas, eventos = _sessao_de_mentira(tempo=lambda n, pos, cid: 123.4)
    assert re.fullmatch(r"\d\d:\d\d:\d\d", linhas[0]["inicio"]) and linhas[0]["segundos"] == "123,400", linhas[0]
    assert f5.resumir_manual(f5.ler_planilha(_csv(linhas)), eventos)["geral"]["tempo_media_s"] == 123.4
    assert f5.segundos_entre("14:00:00", "14:02:03,5") == 123.5 and f5.segundos_entre("2026-11-19T14:00:00.000", "2026-11-19T14:02:03.500") == 123.5
    for inicio, fim in (("14:00:00", "13:59:59"), ("14:00:00", "2026-11-19T14:02:03"), ("", "14:00:00"), ("14:00", "x")):
        try:
            f5.segundos_entre(inicio, fim)
        except ValueError:
            continue
        raise AssertionError(f"segundos_entre aceitou {inicio!r} e {fim!r}")
    # o limite de 10 minutos é o do ajudante da sessão, quando ele o declara
    assert f5.LIMITE_S == float(getattr(lbm, "LIMITE_S", f5.LIMITE_S))


# ----------------------------------------------------------------------------- a conta exploratória sem a sessão de cada integrante (decisão 151)

# ! Alteração de IA - Revisar: (24/11/2026, ficha 91, decisão 151) teste novo, escrito antes do código: a comparação refeita sem a sessão de um integrante por vez,
# com as mesmas regras aplicadas às medidas que sobram, num campo e num bloco próprios, marcados como conta exploratória; e a prova de que o resto da leitura (os
# vereditos, os outros campos e os outros blocos) sai igual com ela e sem ela.
# ! Motivo: com as sessões lidas em 24/11/2026, o veredito do Task Success mostrou depender da sessão de um integrante só (0 de 10 corrigidos). O Eric decidiu que
# a leitura fica como as regras deram, com a ressalva declarada, e que a conta sem cada integrante entra como tabela gerada por script, e não de rascunho. Ela foi
# pensada depois de ver os números: pela regra L15 do plano, entra marcada como exploratória e não pode mudar nenhum veredito.
def teste_comparacao_sem_a_sessao_de_cada_integrante_e_exploratoria_e_nao_muda_a_leitura():
    import analisar_fase3b as a3b
    registros = [_execucao(cid, rep, 70.0) for cid in CENARIOS for rep in range(1, f5.REPETICOES + 1)]
    agente = f5.resumir_agente({"registros": registros, "condicoes": {"repeticoes": f5.REPETICOES, "parcial": False}, "referencia": None}, corrida="noite_de_mentira",
                               gerado_em="2026-11-18T23:00:00")
    # o integrante 1 leva 80 s, o 2 leva 40 s e não corrige nada, o 3 leva 300 s; o agente leva 70 s e acerta tudo
    linhas, eventos = _sessao_de_mentira(tempo=lambda n, pos, cid: {1: 80.0, 2: 40.0, 3: 300.0}[n])
    for linha in linhas:
        if linha["integrante"] == "2":
            linha["corrigido"] = "não"
            if linha["tipo"] == "contrato":
                linha["causa"] = next(c for c in taxonomia.CAUSAS_RAIZ if c != CATALOGO[linha["cenario"]]["causa"])
    lidas = f5.ler_planilha(_csv(linhas))
    manual = f5.resumir_manual(lidas, eventos, gerado_em="2026-11-24T20:00:00")
    medidas = f5.conferir_planilha(lidas, eventos)["medidas"]
    assert (manual["geral"]["n"], manual["geral"]["sucessos"]) == (30, 20) and [x["sucessos"] for x in manual["por_integrante"]] == [10, 0, 10], manual["por_integrante"]
    sem_a_conta = f5.resumir_medicao(agente, manual, gerado_em="2026-11-24T21:00:00")
    m = f5.resumir_medicao(agente, manual, gerado_em="2026-11-24T21:00:00", medidas_das_pessoas=medidas)
    # o que a leitura já dava não muda uma vírgula: os mesmos campos, com os mesmos valores, e os mesmos blocos no .md
    novos = {"sem_um_integrante", "nota_sem_um_integrante"}
    assert "sem_um_integrante" not in sem_a_conta and set(m) - set(sem_a_conta) == novos, sorted(set(m) ^ set(sem_a_conta))
    assert {k: v for k, v in m.items() if k not in novos} == sem_a_conta
    assert (m["tempo"]["geral"]["caso"], m["tempo"]["geral"]["lado"], m["task_success"]["caso"], m["task_success"]["lado"]) == ("veredito", "agente", "veredito", "agente"), m["tempo"]["geral"]
    blocos_antes, blocos_depois = a3b.blocos_de(f5.render_medicao(sem_a_conta)), a3b.blocos_de(f5.render_medicao(m))
    assert set(blocos_depois) - set(blocos_antes) == {"tb_f5_medicao_sem_um_integrante"} and all(blocos_depois[n] == blocos_antes[n] for n in blocos_antes), sorted(blocos_depois)
    # o rótulo vai dentro do bloco, porque é o bloco que o relatório cola e que o painel mostra
    bloco, nota = blocos_depois["tb_f5_medicao_sem_um_integrante"], m["nota_sem_um_integrante"]
    for texto in (bloco, nota):
        assert "exploratória" in texto and "24/11/2026" in texto and "depois de ver os números" in texto and "não é o veredito da leitura" in texto, texto[:400]
    assert "ficha 91" in nota and "decisão 151" in nota and nota in f5.render_medicao(m), nota
    assert all(f"sem a sessão do integrante {n}" in bloco for n in (1, 2, 3)) and "—" not in bloco and "→" not in bloco
    # três linhas, uma por integrante que sai, cada uma com a mesma conta da leitura aplicada às medidas que sobram
    conta = m["sem_um_integrante"]
    assert [x["sem_o_integrante"] for x in conta] == [1, 2, 3], conta
    for x in conta:
        resto = f5.resumir_lado([med for med in medidas if med["quem"] != x["sem_o_integrante"]])
        c = f5.comparar(agente, resto)
        g, sinais, ts = c["tempo"]["geral"], c["tempo"]["geral"]["sinais"], c["task_success"]
        assert x["pessoas"] == {"tentativas": resto["geral"]["n"], "corrigidas": resto["geral"]["sucessos"], "task_success_pct": resto["geral"]["task_success_pct"],
                                "com_fim": resto["geral"]["com_fim"], "sem_fim": resto["geral"]["sem_fim"], "tempo_media_s": resto["geral"]["tempo_media_s"]}, x["pessoas"]
        assert x["tempo"] == {"cenarios_com_os_dois_lados": g["cenarios_com_os_dois_lados"], "diferenca_media_s": g["diferenca_media_s"], "ic_lo_s": g["ic_lo_s"], "ic_hi_s": g["ic_hi_s"],
                              "razao_das_medias": g["razao_das_medias"], "agente_mais_rapido": sinais["agente"], "pessoas_mais_rapidas": sinais["pessoas"], "empates": sinais["empates"],
                              "sem_medida": sinais["sem_medida"], "p": sinais["p"], "o_que_a_regra_l9_daria": g["caso"], "lado": g["lado"]}, x["tempo"]
        assert x["task_success"] == {"agente_maior": ts["sinais"]["agente"], "pessoas_maior": ts["sinais"]["pessoas"], "iguais": ts["sinais"]["iguais"],
                                     "sem_medida": ts["sinais"]["sem_medida"], "p": avaliar.mcnemar_exato(ts["sinais"]["agente"], ts["sinais"]["pessoas"]),
                                     "o_que_a_regra_l11_daria": ts["caso"], "lado": ts["lado"]}, x["task_success"]
    sem_1, sem_2, sem_3 = conta
    # sem o integrante 1: sobram o 2 (40 s, nada corrigido) e o 3 (300 s): média de 170 s por cenário, 10 de 20
    assert (sem_1["pessoas"]["corrigidas"], sem_1["pessoas"]["tentativas"], sem_1["tempo"]["diferenca_media_s"], sem_1["tempo"]["agente_mais_rapido"]) == (10, 20, 100.0, len(CENARIOS)), sem_1
    assert (sem_1["tempo"]["o_que_a_regra_l9_daria"], sem_1["tempo"]["lado"], sem_1["task_success"]["o_que_a_regra_l11_daria"], sem_1["task_success"]["agente_maior"]) == \
        ("veredito", "agente", "veredito", len(CENARIOS)), sem_1
    # sem o integrante 2, que não corrigiu nada: as pessoas ficam com 20 de 20, as parcelas empatam nos dez cenários e o Task Success fica sem veredito; o p é o que
    # o teste daria, mostrado mesmo quando a regra L11 nem chega a calculá-lo
    assert (sem_2["pessoas"]["corrigidas"], sem_2["pessoas"]["tentativas"], sem_2["tempo"]["diferenca_media_s"], sem_2["tempo"]["o_que_a_regra_l9_daria"]) == (20, 20, 120.0, "veredito"), sem_2
    assert (sem_2["task_success"]["agente_maior"], sem_2["task_success"]["iguais"], sem_2["task_success"]["p"], sem_2["task_success"]["o_que_a_regra_l11_daria"],
            sem_2["task_success"]["lado"]) == (0, len(CENARIOS), avaliar.mcnemar_exato(0, 0), "sem_veredito", None), sem_2["task_success"]
    # sem o integrante 3, o mais lento: sobram 80 s e 40 s, média de 60 s, e as pessoas passam à frente do agente nos dez cenários
    assert (sem_3["tempo"]["diferenca_media_s"], sem_3["tempo"]["pessoas_mais_rapidas"], sem_3["tempo"]["agente_mais_rapido"], sem_3["tempo"]["p"]) == \
        (-10.0, len(CENARIOS), 0, avaliar.mcnemar_exato(0, len(CENARIOS))), sem_3["tempo"]
    assert (sem_3["tempo"]["o_que_a_regra_l9_daria"], sem_3["tempo"]["lado"], sem_3["task_success"]["o_que_a_regra_l11_daria"]) == ("veredito", "pessoas", "veredito"), sem_3
    # a função sozinha dá as mesmas três linhas, e a linha anulada na hora continua fora de toda conta
    assert f5.sem_um_integrante(agente, medidas) == conta
    assert "as pessoas mais rápidas" in bloco and "sem veredito" in bloco


# ----------------------------------------------------------------------------- as leituras de ponta a ponta, em pasta temporária

def teste_manual_e_comparar_de_ponta_a_ponta_em_pasta_temporaria():
    linhas, eventos = _sessao_de_mentira(tempo=lambda n, pos, cid: 240.0 + 15.0 * n)
    pasta = _temp()
    (pasta / "planilha.csv").write_text(_csv(linhas), encoding="utf-8-sig")
    (pasta / "sessao.jsonl").write_text("".join(json.dumps(e, ensure_ascii=False) + "\n" for e in eventos), encoding="utf-8")
    origem = ("--planilha", str(pasta / "planilha.csv"), "--sessao", str(pasta / "sessao.jsonl"), "--pasta", str(pasta))
    codigo, saida = _rodar("--manual", *origem)
    assert codigo == 0 and (pasta / "manual.json").exists() and (pasta / "manual.md").exists(), saida
    codigo, saida = _rodar("--manual", *origem, "--check")
    assert codigo == 0 and "batem" in saida, saida
    # a comparação lê os dois lados dos registros: a corrida 21d no lugar da noite do agente, só para provar o caminho
    codigo, saida = _rodar("--comparar", "--saida", CORRIDA_21D, *origem)
    assert codigo == 0 and (pasta / "medicao.json").exists(), saida
    m = json.loads((pasta / "medicao.json").read_text(encoding="utf-8"))
    vigente = json.loads(LEITURA_VIGENTE.read_text(encoding="utf-8"))
    assert m["lados"]["agente"]["geral"]["tempo_media_s"] == vigente["geral"]["mttr_media_s"] and m["lados"]["pessoas"]["geral"]["tempo_media_s"] == 270.0, m["lados"]
    g = m["tempo"]["geral"]
    execucoes = [json.loads(linha) for linha in (RA / CORRIDA_21D / "cenarios.jsonl").read_text(encoding="utf-8").splitlines() if linha.strip()]
    assert g["diferenca_media_s"] == round(270.0 - sum(r["mttr_s"] for r in execucoes) / len(execucoes), 2), g
    assert (g["caso"], g["lado"], g["sinais"]["agente"]) == ("veredito", "agente", len(CENARIOS)), g
    assert m["regras"] == {"empate_s": f5.EMPATE_S, "limite_s": f5.LIMITE_S, "alfa": f5.ALFA, "reamostras": f5.REAMOSTRAS, "semente": f5.SEMENTE,
                           "minimo_de_cenarios_no_task_success": f5.minimo_de_cenarios_para_veredito()}, m["regras"]
    md = (pasta / "medicao.md").read_text(encoding="utf-8")
    for bloco in ("tb_f5_medicao_resumo", "tb_f5_medicao_tempo_por_cenario", "tb_f5_medicao_tempo_por_tipo", "tb_f5_medicao_piso", "tb_f5_medicao_task_success",
                  "tb_f5_medicao_task_success_por_cenario", "tb_f5_medicao_descricao", "tb_f5_medicao_sem_um_integrante"):
        assert f"<!-- tabela:{bloco} -->" in md, bloco
    assert g["frase"] in md and m["task_success"]["frase"] in md and "—" not in md and "→" not in md
    # pela linha de comando a comparação já sai com a conta exploratória sem a sessão de cada integrante (decisão 151), lida da mesma planilha
    assert [x["sem_o_integrante"] for x in m["sem_um_integrante"]] == [1, 2, 3] and all(x["pessoas"]["tentativas"] == 20 for x in m["sem_um_integrante"]), m["sem_um_integrante"]
    assert m["nota_sem_um_integrante"] in md
    codigo, saida = _rodar("--comparar", "--saida", CORRIDA_21D, *origem, "--check")
    assert codigo == 0 and "batem" in saida, saida
    # sem --pasta, a comparação com uma corrida que não é a noite completa não grava em resultados_alvo/fase5
    existia = (RA / "fase5" / "medicao.json").exists()
    codigo, saida = _rodar("--comparar", "--saida", CORRIDA_21D, "--planilha", str(pasta / "planilha.csv"), "--sessao", str(pasta / "sessao.jsonl"))
    assert codigo == 2 and (RA / "fase5" / "medicao.json").exists() == existia, saida


def teste_linha_de_comando_pede_uma_leitura_por_vez_e_colar_espera_o_relatorio():
    for argumentos in ((), ("--agente", "--manual"), ("--custo", "--comparar")):
        codigo, saida = _rodar(*argumentos)
        assert codigo == 2 and "--custo" in saida and "--comparar" in saida, (argumentos, saida)
    if not f5.RELATORIO.exists():
        codigo, saida = _rodar("--custo", "--colar")
        assert codigo == 2 and f5.RELATORIO.name in saida and "F5" in saida, saida
    codigo, saida = _rodar("--antes", "--check")
    assert codigo == 2, "--antes é ela mesma uma conferência: não grava nada e não tem --check"


# ----------------------------------------------------------------------------- o lançador da noite medida

def _conferir_ps1(arq: Path, linhas_com_acento: int = 0) -> str:
    """O que vale para todo lançador: BOM, sem travessão nem seta, a tag com o motivo e a sintaxe aceita pelo PowerShell; devolve os comandos, sem o cabeçalho."""
    cru = arq.read_bytes()
    assert cru[:3] == b"\xef\xbb\xbf", f"{arq.name} precisa de BOM: o Windows PowerShell 5.1 lê sem BOM na codepage ANSI"
    texto = cru.decode("utf-8-sig")
    assert "—" not in texto and "→" not in texto, "sem travessão nem seta: sem BOM o travessão fecha a string no meio"
    assert "de IA - Revisar" in texto and "! Motivo:" in texto
    com_acento = [linha for linha in texto.splitlines() if any(ord(c) > 127 for c in linha)]
    assert len(com_acento) == linhas_com_acento and all(linha.startswith("$Titulo = ") for linha in com_acento), f"fora do título da leitura, {arq.name} é só ASCII: {com_acento}"
    if shutil.which("powershell"):
        caminho = "'" + str(arq).replace("'", "''") + "'"
        roteiro = ("$tokens = $null; $erros = $null; [System.Management.Automation.Language.Parser]::ParseFile(" + caminho + ", [ref]$tokens, [ref]$erros) | Out-Null; "
                   "if ($erros.Count) { $erros | ForEach-Object { Write-Output $_.Message }; exit 1 }")
        r = subprocess.run(["powershell", "-NoProfile", "-EncodedCommand", base64.b64encode(roteiro.encode("utf-16-le")).decode("ascii")], capture_output=True, text=True, encoding="utf-8",
                           errors="replace", timeout=90, check=False)
        assert r.returncode == 0, (r.stdout, r.stderr)
    return texto[texto.index("\nparam("):]


def _simular(arq: Path, *opcoes: str) -> tuple[int, list[str], str]:
    s = subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(arq), "-Simular", *opcoes], capture_output=True, text=True, encoding="utf-8",
                       errors="replace", timeout=120, check=False)
    return s.returncode, [linha.split("SIMULADO: ", 1)[1].strip() for linha in s.stdout.splitlines() if "SIMULADO: " in linha], s.stdout + s.stderr


def teste_rodar_fase5_ps1_roda_a_noite_a_frio_uma_repeticao_por_vez_na_pasta_nova():
    arq = EXP / "rodar_fase5.ps1"
    corpo = _conferir_ps1(arq, linhas_com_acento=1)
    # a pasta e o nome da leitura são os da corrida 28b: a pasta da corrida 28 (fase5_agente) e a leitura dela (cenarios_fase5) não são tocadas
    assert '$Saida = "fase5_agente_b"' in corpo and '$NomeDaLeitura = "cenarios_fase5b"' in corpo and "(corrida 28b)" in corpo and "$Repeticoes = 5" in corpo
    assert '"fase5_agente"' not in corpo and '"cenarios_fase5"' not in corpo
    # sem -Nome, rodar_fase4.ps1 -Modo cenarios grava a leitura em resultados_alvo/fase4/cenarios.{json,md}, que é a da corrida 21
    assert '"-Nome", $NomeDaLeitura' in corpo and '"-Modo", "cenarios"' in corpo and '"-Saida", $Saida' in corpo and '"-Repeticoes", "$N"' in corpo, "a lista de argumentos de cada repetição"
    chamadas = [linha.strip() for linha in corpo.splitlines() if "rodar_fase4.ps1" in linha and linha.strip().startswith("&")]
    assert len(chamadas) == 1 and "@ArgumentosDaRepeticao" in chamadas[0], f"a única chamada ao rodar_fase4.ps1 usa a lista com o -Nome: {chamadas}"
    # decisão 146: o modelo sai da memória antes de cada repetição, e o lançador confere
    assert "& ollama stop $Modelo" in corpo and '$Modelo = "qwen2.5:7b"' in corpo
    assert corpo.count("gerar_dashboard.py") == 1, "o painel é regerado uma vez só, no fim"
    assert '"experimento_sem_notas.py", "--ponte"' in corpo and '".\\rodar_fase3b.ps1" -Modo ponte' in corpo and "-Modelos qwen2.5:7b" in corpo, "a ponte da versão do Ollama (regra R6)"
    assert corpo.index('"avaliar_fase4.py", "--pontes"') < corpo.index('"testar_fase4.py", "--registrar-ponte"'), "a pasta da ponte entra no registro depois de a ponte ser lida"
    assert "$LASTEXITCODE" in corpo and "exit $Codigo" in corpo, "o lançador para na primeira etapa que falhar, com o código dela"
    assert "$RamMinimaGB = 7.0" in corpo, "plano, seção 3.4, etapa 1: espera 7,0 GB livres (o rodar_fase4.ps1 exige 6,5 GB)"
    assert '"avaliar_fase5.py", "--situacao"' in corpo and '$Noite["completa"] -eq "sim"' in corpo, "com a noite completa na pasta nova, a corrida não é chamada de novo"
    assert '$Noite["repeticoes_completas"]' in corpo, "relançar retoma na primeira repetição incompleta"
    assert '$Noite["versoes_ollama"]' in corpo, "decisão 44: a versão do Ollama é conferida antes de cada repetição contra a das execuções já gravadas"
    assert '"avaliar_fase5.py", "--sondagem"' in corpo, "sem a sondagem do frio ter passado, a noite não roda"
    if not shutil.which("powershell"):
        print("  (pulado com aviso: powershell não está no PATH; a sintaxe e a simulação do lançador não foram conferidas)")
        return
    codigo, comandos, saida = _simular(arq)
    assert codigo == 0, saida
    # as etapas na ordem: memória, o agente da 21d, a ponte, a situação da noite, a sondagem, as cinco repetições, a leitura e o painel com as cinco baterias
    antes = ["memoria livre", "avaliar_fase5.py --antes", "experimento_sem_notas.py --ponte", "avaliar_fase5.py --situacao", "avaliar_fase5.py --sondagem"]
    depois = ["avaliar_fase5.py --agente", "gerar_dashboard.py", "testar_painel_textos.py", "testar_painel_topicos.py", "testar_painel_fases.py", "testar_painel_glossario.py",
              "testar_painel_grupo.py"]
    assert len(comandos) == len(antes) + 3 * f5.REPETICOES + len(depois), comandos
    assert all(e in c for e, c in zip(antes, comandos)) and all(e in c for e, c in zip(depois, comandos[-len(depois):])), comandos
    assert re.search(r"7[.,]0 GB", comandos[0]) and "modelo residente" in comandos[0], comandos[0]
    # cinco vezes, na ordem: descarregar o modelo, conferir que ele saiu e a versão do Ollama, e rodar a repetição
    for n in range(1, f5.REPETICOES + 1):
        descarregar, conferir, rodar = comandos[len(antes) + 3 * (n - 1): len(antes) + 3 * n]
        assert descarregar.startswith("ollama stop qwen2.5:7b") and f"repeticao {n} de {f5.REPETICOES}" in descarregar, descarregar
        assert conferir.startswith("ollama ps") and "versao do Ollama" in conferir, conferir
        assert f"rodar_fase4.ps1 -Modo cenarios -Saida fase5_agente_b -Repeticoes {n} -Nome cenarios_fase5b -Titulo" in rodar, rodar
        assert "corrida 28b" in rodar and "cenários com cinco repetições" in rodar, rodar
    assert sum("rodar_fase4.ps1" in c for c in comandos) == f5.REPETICOES and not any("fase5_agente " in c or "cenarios_fase5 " in c for c in comandos), comandos
    # a duração que o lançador anuncia vem do custo gravado, e não de um número escrito no .ps1
    custo = json.loads((RA / "fase5" / "custo.json").read_text(encoding="utf-8"))["resumo"]
    assert f"cerca de {custo['minutos_estimados_sem_ponte']} minutos" in saida and f"{custo['minutos_estimados_com_ponte']} minutos" in saida, saida
    # sem o painel
    codigo, comandos, saida = _simular(arq, "-SemPainel")
    assert codigo == 0 and len(comandos) == len(antes) + 3 * f5.REPETICOES + 1 and not any("painel" in c or "gerar_dashboard" in c for c in comandos), comandos


def teste_rodar_sondagem_frio_ps1_faz_duas_inferencias_do_mesmo_cenario_com_o_modelo_descarregado_entre_elas():
    arq = EXP / "rodar_sondagem_frio.ps1"
    corpo = _conferir_ps1(arq)
    assert "fase5_agente" not in corpo and "cenarios_fase5" not in corpo, "a sondagem grava em pasta própria, fora da pasta da noite e das leituras dela"
    assert "& ollama stop $Modelo" in corpo and '"avaliar_fase5.py", "--sondagem", "--saida", $Pasta' in corpo
    chamadas = [linha.strip() for linha in corpo.splitlines() if "rodar_fase4.ps1" in linha and linha.strip().startswith("&")]
    assert len(chamadas) == 1 and "@ArgumentosDaSondagem" in chamadas[0], chamadas
    # -Casos 1 faz o rodar_fase4.ps1 gravar a leitura do ensaio na pasta da própria sondagem; o -Nome fica de segunda proteção contra a leitura da corrida 21
    assert '"-Casos", "1"' in corpo and '"-Nome", "cenarios_sondagem"' in corpo and '"-Repeticoes", "$N"' in corpo
    if not shutil.which("powershell"):
        print("  (pulado com aviso: powershell não está no PATH; a sintaxe e a simulação da sondagem não foram conferidas)")
        return
    codigo, comandos, saida = _simular(arq)
    assert codigo == 0, saida
    esperado = ["ollama stop qwen2.5:7b", "ollama ps", "-Casos 1 -Repeticoes 1 -Nome cenarios_sondagem", "ollama stop qwen2.5:7b", "ollama ps", "-Casos 1 -Repeticoes 2 -Nome cenarios_sondagem",
                "avaliar_fase5.py --sondagem --saida fase5_sondagem_frio_"]
    assert len(comandos) == len(esperado) and all(e in c for e, c in zip(esperado, comandos)), comandos
    pastas = set(re.findall(r"-Saida (fase5_sondagem_frio_\d{8}_\d{6})", " ".join(comandos)))
    assert len(pastas) == 1 and all(next(iter(pastas)) in c for c in comandos if "rodar_fase4.ps1" in c or "--sondagem" in c), "as duas inferências e o veredito na mesma pasta, nova a cada sondagem"
    assert not any("fase5_agente" in c for c in comandos), comandos


def main() -> None:
    argparse.ArgumentParser(description=__doc__).parse_args()
    modulo = sys.modules[__name__]
    testes = [(nome, obj) for nome, obj in vars(modulo).items()
              if nome.startswith("teste_") and inspect.isfunction(obj) and obj.__module__ == modulo.__name__]
    try:
        for nome, funcao in testes:
            try:
                funcao()
            except Exception:  # noqa: BLE001 - o runner pega qualquer falha do teste para imprimir o rastro e parar com código 1
                print(nome)
                traceback.print_exc()
                sys.exit(1)
            print(f"{nome} ok")
        print(f"{len(testes)} testes ok")
    finally:
        for caminho in _TEMPORARIOS:
            shutil.rmtree(caminho, ignore_errors=True)


if __name__ == "__main__":
    main()
