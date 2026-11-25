#!/usr/bin/env python3
# ! Alteração de IA - Revisar: arquivo novo (16/11/2026, Fase 5, pacote F2): a bateria de testes do ajudante da sessão da linha de
# base manual na versão 2 do protocolo (linha_de_base_manual.py): o registro da sessão em sessao.jsonl (o `armar` grava o início,
# o `entregar` grava o fim do cenário de contrato no Enter do facilitador e recusa causa fora das 23, o `conferir` grava cada
# tentativa de seletor), a leitura desse registro por vez (`resumo_do_registro`), o comando `planilha` (preenche só célula vazia,
# avisa quando discorda, marca a linha anotada à mão), o `treino` (fora dos dez cenários, sem cronômetro), o perfil dos
# integrantes sem o nome, a folha do integrante com a definição das 23 causas, o texto fixo do facilitador e os blocos desses
# textos colados no protocolo. Dois testes fixam o que não pode mudar: a ficha da falha igual à da corrida 21d e os comandos da
# versão 1 (`ordem`, `armar`, `conferir`, `desarmar`). Mesmo formato sem pytest de testar_fase4.py: funções teste_<nome>(), o
# main roda todas na ordem em que estão escritas e termina em "N testes ok"; com `--todos` ele não para na primeira que falha.
# ! Motivo: o plano aprovado da Fase 5 (seção 8, pacote F2; decisão 131) pede os testes escritos antes do código e vistos falhar
# pelo motivo certo. O arquivo é novo, e não testar_fase5.py, porque testar_fase5.py é do pacote F1 (a leitura avaliar_fase5.py e
# o lançador rodar_fase5.ps1), escrito em outra sessão na mesma pasta: dois pacotes editando o mesmo arquivo de testes ao mesmo
# tempo perderiam trabalho um do outro. Nenhum teste daqui chama o modelo, sobe as cobaias, abre navegador ou mexe no banco: o
# que os comandos usam de fora (cobaias, banco, navegador, CobaiaAPI, teclado e relógio) é trocado por versões de teste que só
# anotam as chamadas, e todo registro vai para uma pasta temporária, nunca para resultados_alvo/fase5_manual.
"""Testes do ajudante da linha de base manual (Fase 5, pacote F2), sem pytest (asserts em Python puro)."""
import argparse
import contextlib
import csv
import inspect
import io
import json
import re
import shutil
import sys
import tempfile
import time
import traceback
import types
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

EXP = Path(__file__).resolve().parent
RAIZ = EXP.parent.parent.parent
RA = EXP / "resultados_alvo"

import cenarios_fase4 as cen
import linha_de_base_manual as lbm
import taxonomia

T0 = 1795270000.0            # um instante qualquer do relógio, em segundos desde 1970, para os relógios de teste
_TEMPORARIOS: list[Path] = []
_FALTA = object()
# o que existe na pasta da sessão de verdade quando a bateria começa: o último teste confere que nada mudou
_SESSAO_DE_VERDADE = RA / "fase5_manual"
_ANTES = sorted((p.name, p.stat().st_size) for p in _SESSAO_DE_VERDADE.glob("*")) if _SESSAO_DE_VERDADE.exists() else None


def _tmp() -> Path:
    pasta = Path(tempfile.mkdtemp(prefix="linha_de_base_"))
    _TEMPORARIOS.append(pasta)
    return pasta


def _posicao(integrante: int, cenario_id: str) -> int:
    """A posição do cenário na ordem sorteada do integrante (a planilha chama o cenário por ela)."""
    return lbm.ordem_dos_integrantes()[integrante].index(cenario_id) + 1


def _resultado(passou: bool) -> dict:
    """O que cen.rodar_cenario devolve, no que o `conferir` lê: passou, as conferências, os segundos e a falha."""
    return {"passou": passou, "conferencias": [{"nome": "uma conferência do roteiro", "passou": passou}], "segundos": 3.2,
            "erro": None if passou else "TimeoutError: Timeout 5000ms exceeded.", "passo_falho": None if passou else 1,
            "conferencia_falha": None if passou else {"nome": "passo 2 (esperar #buscar visível)", "passou": False,
                                                      "esperado": "esperar #buscar visível", "observado": "TimeoutError"}}


@contextlib.contextmanager
def _ambiente(respostas=(), no_ar: bool = True, roteiros=(), bancos=()):
    """Troca o que os comandos usam de fora por versões de teste e devolve o que elas anotaram: `chamadas` (banco, modo da
    CobaiaAPI, navegador, cookies, endereço aberto, roteiro rodado), `perguntas` (o texto de cada pedido ao teclado) e `saida`
    (o que o comando imprimiu). `respostas` são as respostas do teclado, em ordem (uma função recebe o texto da pergunta e
    devolve a resposta); `agora` é o relógio, que o teste adianta; `pasta` é uma pasta temporária para o registro."""
    import builtins

    import executar_fase4 as ex
    import navegador
    amb = types.SimpleNamespace(chamadas=[], perguntas=[], respostas=list(respostas), agora=T0, pasta=_tmp(), roteiros=list(roteiros),
                                bancos=list(bancos), saida=io.StringIO(), ao_abrir=None, acha=(14, True))

    class Localizador:
        def __init__(self, seletor):
            self.seletor = seletor
            self.first = self

        def count(self):
            return amb.acha[0]

        def evaluate(self, *a, **k):
            return amb.acha[1]

    class Pagina:
        def __init__(self):
            self.context = self

        def add_cookies(self, cookies):
            amb.chamadas.append(("cookies", sorted((c["name"], c["value"]) for c in cookies)))

        def add_init_script(self, script):
            amb.chamadas.append(("script_de_quebra",))

        def goto(self, url, **k):
            amb.chamadas.append(("abrir", url))
            if amb.ao_abrir:
                amb.ao_abrir()

        def wait_for_selector(self, seletor, **k):
            amb.chamadas.append(("esperar", seletor))

        def locator(self, seletor):
            amb.chamadas.append(("localizar", seletor))
            return Localizador(seletor)

        def close(self):
            pass

    class Navegador:
        def __init__(self, canal="chromium", headless=True):
            amb.chamadas.append(("navegador", canal, "sem janela" if headless else "com janela"))

        def __enter__(self):
            return self

        def __exit__(self, *exc):
            amb.chamadas.append(("navegador fechado",))

        def nova_pagina(self):
            return Pagina()

        def versao(self):
            return {"navegador": "156.0-de-teste", "playwright": "0", "canal": "chromium", "executavel": "x"}

    def teclado(texto=""):
        amb.perguntas.append(texto)
        if not amb.respostas:
            raise AssertionError(f"o comando pediu ao teclado mais do que o teste previa: {texto!r}")
        r = amb.respostas.pop(0)
        return r(texto) if callable(r) else r

    def banco():
        amb.chamadas.append(("banco",))
        return "h-seed", (amb.bancos.pop(0) if amb.bancos else 1.5)

    def modo(modo_, campo, token=None, url=None):
        amb.chamadas.append(("modo", modo_, campo))
        return {"mode": modo_}

    def roteiro(cenario_, pagina, inter=None, **k):
        amb.chamadas.append(("roteiro", [p.get("seletor") for p in cenario_["passos"]]))
        return amb.roteiros.pop(0)

    fichas = [{"cenario": c["id"], "repeticao": 1, "detectou": True, "motivo_deteccao": _ficha_de_teste(c["id"])} for c in cen.CENARIOS_DO_ENSAIO]
    trocas = [(lbm, "_cobaias_no_ar", lambda: no_ar), (lbm, "_restaurar_banco", banco), (lbm, "_registros_do_ensaio", lambda saida: fichas),
              (lbm, "_relogio", lambda: amb.agora), (ex, "ligar_modo", modo), (ex, "_contrato_do_produto", lambda: "CONTRATO DE TESTE"),
              (navegador, "Navegador", Navegador), (cen, "rodar_cenario", roteiro), (builtins, "input", teclado)]
    antigos = [(obj, nome, getattr(obj, nome, _FALTA)) for obj, nome, _ in trocas]
    for obj, nome, valor in trocas:
        setattr(obj, nome, valor)
    try:
        with contextlib.redirect_stdout(amb.saida):
            yield amb
    finally:
        for obj, nome, valor in antigos:
            if valor is _FALTA:
                delattr(obj, nome)
            else:
                setattr(obj, nome, valor)


def _ficha_de_teste(cenario_id: str) -> str:
    """A ficha que o registro de teste do ensaio traz para o cenário; não leva o nome dele, que não pode aparecer na tela."""
    return f"ficha de teste número {[c['id'] for c in cen.CENARIOS_DO_ENSAIO].index(cenario_id) + 1}"


def _rodar(*linha: str) -> int:
    """Roda um comando do ajudante como a linha de comando faria e devolve o código de saída."""
    args = lbm.montar_parser().parse_args(list(linha))
    return args.funcao(args)


def _em_ordem(texto: str, trechos: list[str]) -> None:
    pos = 0
    for t in trechos:
        achou = texto.find(t, pos)
        assert achou >= 0, f"faltou (ou saiu da ordem) na tela: {t!r}\n--- tela ---\n{texto}"
        pos = achou + len(t)


def _hms(t: float) -> str:
    return time.strftime("%H:%M:%S", time.localtime(t))


def _contrato(n: int, p: int, segundos: float, causa: str, campo: str | None, t0: float = T0) -> list[dict]:
    """Os eventos de um cenário de contrato inteiro: armado em t0 e entregue `segundos` depois."""
    vez = lbm.vez_do_cenario(n, p)
    return [lbm.montar_evento("inicio", vez, t0), lbm.montar_evento("entrega", vez, t0 + segundos),
            lbm.montar_evento("resposta", vez, t0 + segundos + 9, causa=causa, campo=campo,
                              corrigido=lbm.resultado_da_entrega(vez["cenario"], causa, campo), recusada=False),
            lbm.montar_evento("fim_do_armar", vez, t0 + segundos + 12)]


def _localizador(n: int, p: int, tentativas: list[tuple[float, str, bool, float]], t0: float = T0) -> list[dict]:
    """Os eventos de um cenário de localizador: armado em t0 e uma tentativa por item (segundos depois, seletor, corrigiu, banco)."""
    vez = lbm.vez_do_cenario(n, p)
    return [lbm.montar_evento("inicio", vez, t0)] + [
        lbm.montar_evento("tentativa", vez, t0 + seg, seletor=sel, corrigido=ok, segundos_do_banco=banco, segundos_do_roteiro=3.2, motivo=None if ok else "não achou")
        for seg, sel, ok, banco in tentativas]


def _linha(texto: str, n: int, p: int) -> dict:
    linhas = list(csv.DictReader(io.StringIO(texto), delimiter=lbm.SEPARADOR))
    return next(x for x in linhas if (x["integrante"], x["ordem"]) == (str(n), str(p)))


# ----------------------------------------------------------------------------- o que não pode mudar (versão 1)

def teste_ficha_da_falha_continua_igual_a_da_corrida_21d():
    """O integrante recebe a ficha que a detecção do agente gravou. O `armar` lê a da corrida 21 (pasta fase4_ensaio); a leitura
    vigente do ensaio é a da corrida 21d (fase4_ensaio_v4). Nos dez cenários as duas têm de ser o mesmo texto."""
    import executar_bateria
    assert lbm.SAIDA_DO_ENSAIO == "fase4_ensaio"
    da_21 = executar_bateria.ler_jsonl(RA / lbm.SAIDA_DO_ENSAIO / "cenarios.jsonl")
    da_21d = executar_bateria.ler_jsonl(RA / "fase4_ensaio_v4" / "cenarios.jsonl")
    assert len(cen.CENARIOS_DO_ENSAIO) == 10
    for c in cen.CENARIOS_DO_ENSAIO:
        a, b = lbm.ficha_da_falha(c["id"], da_21), lbm.ficha_da_falha(c["id"], da_21d)
        assert a and a == b, f"{c['id']}: a ficha que o armar mostra não é a da corrida 21d\n  21:  {a}\n  21d: {b}"


def teste_comandos_antigos_continuam_com_o_comportamento_de_hoje():
    """`ordem`, `armar`, `conferir` e `desarmar` como a versão 1 do protocolo os descreve: as mesmas opções com os mesmos
    padrões, a mesma tela, as mesmas chamadas (banco, modo da CobaiaAPI, cookies da quebra, navegador) e os mesmos códigos de saída."""
    import executar_fase4 as ex
    ap = lbm.montar_parser()
    a = ap.parse_args(["armar", "--vez", "1", "3"])
    assert (a.vez, a.cenario, a.forma, a.canal, a.token, a.saida) == ([1, 3], None, "php", "chromium", ex.TOKEN_PADRAO, "fase4_ensaio")
    a = ap.parse_args(["conferir", "--cenario", "localizador-front-busca", "--seletor", "input[name=search]"])
    assert (a.vez, a.cenario, a.seletor, a.forma, a.saida) == (None, "localizador-front-busca", "input[name=search]", "php", "fase4_ensaio")
    assert ap.parse_args(["desarmar"]).token == ex.TOKEN_PADRAO
    a = ap.parse_args(["ordem"])
    assert (a.integrantes, a.semente, a.gravar) == (3, 20261104, False)
    for ruim in (["armar"], ["armar", "--vez", "1", "3", "--cenario", "contrato-error_500"], ["conferir"], ["armar", "--cenario", "x", "--forma", "outra"]):
        try:
            with contextlib.redirect_stderr(io.StringIO()):
                ap.parse_args(ruim)
        except SystemExit:
            pass
        else:
            raise AssertionError(f"a linha de comando aceitou {ruim}")
    # ordem: uma linha por integrante, na ordem sorteada; com --gravar, a planilha em branco, e nunca por cima de uma com anotações
    ordens = lbm.ordem_dos_integrantes()
    planilha_de_verdade = lbm.PLANILHA
    try:
        with _ambiente() as amb:
            lbm.PLANILHA = amb.pasta / "planilha.csv"
            assert _rodar("ordem") == 0 and not lbm.PLANILHA.exists()
            for n, ids in ordens.items():
                assert f"integrante {n}: " + ", ".join(f"{i}. {cid}" for i, cid in enumerate(ids, 1)) in amb.saida.getvalue()
            assert _rodar("ordem", "--gravar") == 0
            em_branco = lbm.PLANILHA.read_text(encoding="utf-8-sig")
            assert em_branco == lbm.planilha_modelo(ordens) and lbm.PLANILHA.read_bytes().startswith(b"\xef\xbb\xbf")
            anotada = em_branco.replace(";;;;;;;;;;\n", ";10:00:00;;;;;;;;;\n", 1)
            lbm.PLANILHA.write_text(anotada, encoding="utf-8-sig")
            assert _rodar("ordem", "--gravar") == 0
            assert lbm.PLANILHA.read_text(encoding="utf-8-sig") == anotada, "a planilha com anotações não é regravada"
            assert (amb.pasta / "planilha.nova.csv").read_text(encoding="utf-8-sig") == em_branco
    finally:
        lbm.PLANILHA = planilha_de_verdade
    # armar um cenário de contrato pelo nome (o ensaio do facilitador)
    with _ambiente(respostas=[""]) as amb:
        assert _rodar("armar", "--cenario", "contrato-type_drift") == 0
    tela = amb.saida.getvalue()
    _em_ordem(tela, ["contrato-type_drift: banco restaurado e conferido (hash h-seed, 1.5 s)", "falha ligada na CobaiaAPI para GET /api/produtos",
                     "== Ficha da falha", _ficha_de_teste("contrato-type_drift"), "== Roteiro do teste", "1. abrir produtos_api.php",
                     "== Contrato esperado de cada produto em GET /api/produtos", "CONTRATO DE TESTE",
                     "== Resposta: uma causa desta lista e o campo afetado (ou nenhum)", ", ".join(taxonomia.CAUSAS_RAIZ),
                     "navegador 156.0-de-teste aberto para o integrante; início do cronômetro: ", "CobaiaAPI de volta ao modo normal"])
    assert re.search(r"início do cronômetro: \d\d:\d\d:\d\d", tela)
    assert amb.chamadas == [("banco",), ("modo", "type_drift", "preco"), ("navegador", "chromium", "com janela"),
                            ("abrir", cen.BASE_PADRAO + "produtos_api.php"), ("navegador fechado",), ("modo", "normal", None)], amb.chamadas
    assert len(amb.perguntas) == 1 and amb.perguntas[0].startswith("Enter fecha o navegador")
    # armar um cenário de localizador: a quebra entra pelos cookies da variante PHP e a CobaiaAPI não é tocada
    with _ambiente(respostas=[""]) as amb:
        assert _rodar("armar", "--cenario", "localizador-front-busca") == 0
    tela = amb.saida.getvalue()
    _em_ordem(tela, ["== Ficha da falha", _ficha_de_teste("localizador-front-busca"), "== Roteiro do teste",
                     "== Resposta: um seletor (CSS ou do Playwright) que ache o elemento do passo que quebrou", "início do cronômetro: "])
    assert "o passo que quebrou" in tela and "== Contrato esperado" not in tela
    assert amb.chamadas == [("banco",), ("navegador", "chromium", "com janela"), ("cookies", [("quebra", "id_renomeado"), ("quebra_pagina", "index.php")]),
                            ("abrir", cen.BASE_PADRAO + "index.php"), ("navegador fechado",)], amb.chamadas
    # sem as cobaias no ar: código 2, sem tocar no banco
    with _ambiente(no_ar=False) as amb:
        assert _rodar("armar", "--cenario", "contrato-type_drift") == 2
    assert amb.chamadas == [] and "as cobaias não responderam nas portas 8080 e 8000" in amb.saida.getvalue()
    # conferir: o roteiro do agente com o seletor do integrante; 0 quando chega ao fim sem erro, 1 quando não
    q = cen.quebra("front-busca", "id_renomeado")
    with _ambiente(roteiros=[_resultado(True)]) as amb:
        assert _rodar("conferir", "--cenario", "localizador-front-busca", "--seletor", "input[name=search]") == 0
    assert "localizador-front-busca com o seletor 'input[name=search]': CORRIGIDO (o roteiro chegou ao fim sem erro) às " in amb.saida.getvalue()
    assert "banco restaurado em 1.5 s antes do roteiro (descontar do cronômetro)" in amb.saida.getvalue()
    assert [c[0] for c in amb.chamadas] == ["banco", "navegador", "cookies", "roteiro", "navegador fechado"] and amb.chamadas[1] == ("navegador", "chromium", "sem janela")
    seletores = next(c for c in amb.chamadas if c[0] == "roteiro")[1]
    assert seletores[q["passo_alvo"]] == "input[name=search]" and q["localizador"] not in seletores
    with _ambiente(roteiros=[_resultado(False)]) as amb:
        assert _rodar("conferir", "--cenario", "localizador-front-busca", "--seletor", "#errado") == 1
    assert "com o seletor '#errado': não corrigido às " in amb.saida.getvalue()
    # conferir sem seletor: roda com o localizador quebrado; sai 0 quando a quebra está armada (o roteiro não passa)
    with _ambiente(roteiros=[_resultado(False)]) as amb:
        assert _rodar("conferir", "--cenario", "localizador-front-busca") == 0
    assert "com o localizador quebrado do roteiro: " in amb.saida.getvalue()
    assert next(c for c in amb.chamadas if c[0] == "roteiro")[1][q["passo_alvo"]] == q["localizador"]
    with _ambiente(roteiros=[_resultado(True)]) as amb:
        assert _rodar("conferir", "--cenario", "localizador-front-busca") == 1
    # desarmar: a CobaiaAPI volta ao modo normal
    with _ambiente() as amb:
        assert _rodar("desarmar") == 0
    assert amb.chamadas == [("modo", "normal", None)] and "CobaiaAPI de volta ao modo normal" in amb.saida.getvalue()


# ----------------------------------------------------------------------------- o registro da sessão

def teste_registro_grava_cada_evento_numa_linha_com_a_hora_em_milesimos():
    arq = lbm.arquivo_do_registro(_tmp())
    assert arq.name == "sessao.jsonl" and lbm.ler_registro(arq) == []
    assert lbm.arquivo_do_registro().parts[-2:] == ("fase5_manual", "sessao.jsonl"), "sem pasta, o registro é o da sessão de verdade"
    p = _posicao(2, "contrato-error_500")
    vez = lbm.vez_do_cenario(2, p)
    assert vez == {"integrante": 2, "ordem": p, "cenario": "contrato-error_500", "tipo": "contrato"}
    e = lbm.gravar_evento(arq, "inicio", vez, relogio=lambda: T0 + 2.4174, navegador="156.0")
    assert lbm.VERSAO_DO_REGISTRO == 2 and e["registro"] == 2 and e["evento"] == "inicio" and e["navegador"] == "156.0"
    assert {k: e[k] for k in vez} == vez
    assert re.fullmatch(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d\.417", e["hora"]), e["hora"]
    assert e["hora"][11:19] == _hms(T0 + 2) and abs(e["relogio_s"] - (T0 + 2.417)) < 1e-6
    e2 = lbm.gravar_evento(arq, "fim_do_armar", vez, relogio=lambda: T0 + 9)
    linhas = arq.read_text(encoding="utf-8").splitlines()
    assert len(linhas) == 2 and [json.loads(x) for x in linhas] == [e, e2] == lbm.ler_registro(arq), "uma linha por evento, só acréscimo"
    assert lbm.montar_evento("inicio", vez, T0 + 2.4174, navegador="156.0") == e, "gravar é montar o evento e acrescentar a linha"
    # o treino não é de vez nenhuma: sem ordem e sem cenário
    t = lbm.montar_evento("treino", {"integrante": 3}, T0, parte="seletor")
    assert (t["integrante"], t["ordem"], t["cenario"], t["tipo"], t["parte"]) == (3, None, None, None, "seletor")


def teste_armar_grava_o_inicio_com_o_navegador_ja_aberto_e_o_ensaio_nao_grava():
    p = _posicao(1, "contrato-malformed_json")
    visto = {}

    def enter(pergunta):
        visto["no_enter"] = lbm.ler_registro(arq)
        amb.agora = T0 + 300
        return ""

    with _ambiente(respostas=[enter]) as amb:
        arq = lbm.arquivo_do_registro(amb.pasta)
        amb.ao_abrir = lambda: visto.setdefault("ao_abrir", lbm.ler_registro(arq))
        assert _rodar("armar", "--vez", "1", str(p), "--registro", str(amb.pasta)) == 0
    assert visto["ao_abrir"] == [], "antes de o navegador abrir no endereço do roteiro não há início"
    assert [e["evento"] for e in visto["no_enter"]] == ["inicio"], "o início está gravado enquanto o integrante trabalha"
    inicio, fim = lbm.ler_registro(arq)
    assert (inicio["evento"], inicio["integrante"], inicio["ordem"], inicio["cenario"], inicio["tipo"]) == ("inicio", 1, p, "contrato-malformed_json", "contrato")
    assert abs(inicio["relogio_s"] - T0) < 1e-6 and inicio["hora"].endswith(".000")
    assert (inicio["navegador"], inicio["hash_do_banco"], inicio["segundos_do_banco"], inicio["forma"]) == ("156.0-de-teste", "h-seed", 1.5, None)
    assert inicio["ficha"] == _ficha_de_teste("contrato-malformed_json")
    assert fim["evento"] == "fim_do_armar" and abs(fim["relogio_s"] - (T0 + 300)) < 1e-6
    tela = amb.saida.getvalue()
    assert f"início do cronômetro: {_hms(T0)}" in tela, "a hora da tela é a do registro"
    assert "contrato-malformed_json" not in tela, "o nome do cenário, que diz o modo de falha, não aparece na tela"
    # cenário de localizador: o início guarda a forma da quebra
    p = _posicao(1, "localizador-front-busca")
    with _ambiente(respostas=[""]) as amb:
        arq = lbm.arquivo_do_registro(amb.pasta)
        assert _rodar("armar", "--vez", "1", str(p), "--registro", str(amb.pasta)) == 0
    assert [(e["evento"], e["tipo"], e.get("forma")) for e in lbm.ler_registro(arq)] == [("inicio", "localizador", "php"), ("fim_do_armar", "localizador", None)]
    # o ensaio do facilitador, pelo nome, não grava nada: nem o registro é criado
    with _ambiente(respostas=[""]) as amb:
        assert _rodar("armar", "--cenario", "contrato-error_500", "--registro", str(amb.pasta)) == 0
    assert not lbm.arquivo_do_registro(amb.pasta).exists()
    # sem as cobaias, nada é gravado
    with _ambiente(no_ar=False) as amb:
        assert _rodar("armar", "--vez", "1", "1", "--registro", str(amb.pasta)) == 2
    assert not lbm.arquivo_do_registro(amb.pasta).exists()


def teste_entregar_grava_o_fim_no_enter_antes_de_pedir_a_causa_e_o_campo():
    p = _posicao(1, "contrato-field_missing")
    visto = {}

    def enter(pergunta):
        visto["antes_do_enter"] = [e["evento"] for e in lbm.ler_registro(arq)]
        amb.agora = T0 + 83.417          # o instante em que o facilitador dá Enter
        return ""

    def causa(pergunta):
        visto["ao_pedir_a_causa"] = lbm.ler_registro(arq)[-1]
        amb.agora = T0 + 100             # digitar a causa e o campo leva tempo, e esse tempo não entra no cronômetro
        return "campo_ausente"

    with _ambiente(respostas=[enter, causa, "preco"]) as amb:
        arq = lbm.arquivo_do_registro(amb.pasta)
        lbm.gravar_evento(arq, "inicio", lbm.vez_do_cenario(1, p), relogio=lambda: T0)
        assert _rodar("entregar", "--vez", "1", str(p), "--registro", str(amb.pasta)) == 0
    assert visto["antes_do_enter"] == ["inicio"]
    assert visto["ao_pedir_a_causa"]["evento"] == "entrega" and abs(visto["ao_pedir_a_causa"]["relogio_s"] - (T0 + 83.417)) < 1e-6, \
        "o fim já está no arquivo quando a causa é pedida"
    assert len(amb.perguntas) == 3 and "Enter" in amb.perguntas[0] and "causa" in amb.perguntas[1].lower() and "campo" in amb.perguntas[2].lower()
    eventos = lbm.ler_registro(arq)
    assert [e["evento"] for e in eventos] == ["inicio", "entrega", "resposta"]
    r = eventos[-1]
    assert (r["causa"], r["campo"], r["corrigido"], r["recusada"]) == ("campo_ausente", "preco", True, False)
    resumo = lbm.resumo_do_registro(eventos)[(1, p)]
    assert resumo["fim"] == eventos[1]["hora"] and resumo["segundos"] == 83.417 and resumo["descontar_s"] == 0
    assert resumo["corrigido"] is True and resumo["fechado"] is True and resumo["estourou"] is False
    assert (resumo["causa"], resumo["campo"], resumo["seletor"], resumo["tentativas"]) == ("campo_ausente", "preco", None, 0)
    # a tela não diz se a resposta está certa: no contrato, quem diz é a planilha, depois da sessão
    assert not re.search(r"corrigid|acert|errad|errou", amb.saida.getvalue(), re.IGNORECASE), amb.saida.getvalue()
    # o corrigido é a regra do agente (cen.task_success_contrato): a causa e o campo esperados do cenário
    assert lbm.resultado_da_entrega("contrato-field_missing", "campo_ausente", "preco") is True
    assert lbm.resultado_da_entrega("contrato-field_missing", "campo_ausente", None) is False
    assert lbm.resultado_da_entrega("contrato-field_missing", "campo_renomeado", "preco") is False
    assert lbm.resultado_da_entrega("contrato-error_500", "erro_interno_do_servidor", None) is True
    assert lbm.resultado_da_entrega("contrato-error_500", "erro_interno_do_servidor", "preco") is False
    assert lbm.campo_entregue("nenhum") is None and lbm.campo_entregue("  ") is None and lbm.campo_entregue(" preco ") == "preco"
    # tudo na linha de comando: sem pergunta nenhuma, o fim é a hora em que o comando rodou
    p2 = _posicao(1, "contrato-error_500")
    with _ambiente() as amb:
        arq = lbm.arquivo_do_registro(amb.pasta)
        lbm.gravar_evento(arq, "inicio", lbm.vez_do_cenario(1, p2), relogio=lambda: T0)
        amb.agora = T0 + 41.5
        assert _rodar("entregar", "--vez", "1", str(p2), "--causa", "erro_interno_do_servidor", "--campo", "nenhum", "--registro", str(amb.pasta)) == 0
        assert amb.perguntas == []
        r = lbm.resumo_do_registro(lbm.ler_registro(arq))[(1, p2)]
        assert (r["segundos"], r["causa"], r["campo"], r["corrigido"]) == (41.5, "erro_interno_do_servidor", None, True)
        # a vez já tem entrega: a segunda é recusada e o registro não muda
        antes = arq.read_text(encoding="utf-8")
        assert _rodar("entregar", "--vez", "1", str(p2), "--causa", "corpo_vazio", "--registro", str(amb.pasta)) == 2
        # vez que não foi armada e vez de localizador: recusadas, nada gravado
        assert _rodar("entregar", "--vez", "2", "1", "--causa", "corpo_vazio", "--registro", str(amb.pasta)) == 2
        assert _rodar("entregar", "--vez", "1", str(_posicao(1, "localizador-front-busca")), "--causa", "localizador_quebrado", "--registro", str(amb.pasta)) == 2
        assert arq.read_text(encoding="utf-8") == antes
    # o Enter que ficou sem resposta (o comando caiu no meio): o próximo `entregar` pede só a causa e o campo daquela entrega
    with _ambiente(respostas=["tipo_divergente", "preco"]) as amb:
        arq = lbm.arquivo_do_registro(amb.pasta)
        vez = lbm.vez_do_cenario(1, _posicao(1, "contrato-type_drift"))
        lbm.gravar_evento(arq, "inicio", vez, relogio=lambda: T0)
        lbm.gravar_evento(arq, "entrega", vez, relogio=lambda: T0 + 200)
        amb.agora = T0 + 400
        assert _rodar("entregar", "--vez", "1", str(vez["ordem"]), "--registro", str(amb.pasta)) == 0
        r = lbm.resumo_do_registro(lbm.ler_registro(arq))[(1, vez["ordem"])]
        assert r["segundos"] == 200.0 and r["corrigido"] is True and len(amb.perguntas) == 2


def teste_entregar_recusa_causa_fora_das_23():
    assert len(taxonomia.CAUSAS_RAIZ) == 23
    for c in taxonomia.CAUSAS_RAIZ:
        assert lbm.causa_da_lista(c) == c
    # a grafia não é o que se mede: maiúscula, espaço no lugar do sublinhado e acento são aceitos; nome fora da lista, não
    assert lbm.causa_da_lista("  Tipo_Divergente ") == "tipo_divergente" and lbm.causa_da_lista("tipo divergente") == "tipo_divergente"
    assert lbm.causa_da_lista("codificação incorreta") == "codificacao_incorreta"
    for fora in ("causa_inventada", "type_drift", "latency", "field_missing", "", "tipo", "9"):
        assert lbm.causa_da_lista(fora) is None, fora
    p = _posicao(1, "contrato-type_drift")
    # pela linha de comando: código 2 e nada gravado
    with _ambiente() as amb:
        arq = lbm.arquivo_do_registro(amb.pasta)
        lbm.gravar_evento(arq, "inicio", lbm.vez_do_cenario(1, p), relogio=lambda: T0)
        antes = arq.read_text(encoding="utf-8")
        assert _rodar("entregar", "--vez", "1", str(p), "--causa", "type_drift", "--campo", "preco", "--registro", str(amb.pasta)) == 2
        assert arq.read_text(encoding="utf-8") == antes and "23" in amb.saida.getvalue()
    # pelo teclado, erro de digitação: o comando pede de novo, e o fim continua sendo o Enter

    def enter(pergunta):
        amb.agora = T0 + 50
        return ""

    def errada(pergunta):
        amb.agora = T0 + 70
        return "type_drift"

    with _ambiente(respostas=[enter, errada, "tipo_divergente", "preco"]) as amb:
        arq = lbm.arquivo_do_registro(amb.pasta)
        lbm.gravar_evento(arq, "inicio", lbm.vez_do_cenario(1, p), relogio=lambda: T0)
        assert _rodar("entregar", "--vez", "1", str(p), "--registro", str(amb.pasta)) == 0
        eventos = lbm.ler_registro(arq)
        assert [e["evento"] for e in eventos] == ["inicio", "entrega", "resposta"] and eventos[-1]["causa"] == "tipo_divergente"
        assert lbm.resumo_do_registro(eventos)[(1, p)]["segundos"] == 50.0
        assert "'type_drift' não é uma das 23" in amb.saida.getvalue()
    # a causa que o integrante entregou não está na lista (linha vazia): a entrega não valeu, o tempo segue, e a seguinte vale
    with _ambiente(respostas=[enter, ""]) as amb:
        arq = lbm.arquivo_do_registro(amb.pasta)
        lbm.gravar_evento(arq, "inicio", lbm.vez_do_cenario(1, p), relogio=lambda: T0)
        assert _rodar("entregar", "--vez", "1", str(p), "--registro", str(amb.pasta)) == 1
        eventos = lbm.ler_registro(arq)
        assert [e["evento"] for e in eventos] == ["inicio", "entrega", "resposta"] and eventos[-1]["recusada"] is True and eventos[-1]["causa"] is None
        r = lbm.resumo_do_registro(eventos)[(1, p)]
        assert r["fim"] is None and r["fechado"] is False and r["causa"] is None and any("recusada" in a for a in r["avisos"])
        amb.agora = T0 + 120
        assert _rodar("entregar", "--vez", "1", str(p), "--causa", "tipo_divergente", "--campo", "preco", "--registro", str(amb.pasta)) == 0
        r = lbm.resumo_do_registro(lbm.ler_registro(arq))[(1, p)]
        assert r["segundos"] == 120.0 and r["corrigido"] is True and r["fechado"] is True


def teste_conferir_grava_cada_tentativa_o_resultado_e_os_segundos_do_banco():
    p = _posicao(1, "localizador-front-busca")
    q = cen.quebra("front-busca", "id_renomeado")
    with _ambiente(roteiros=[_resultado(False), _resultado(True), _resultado(False), _resultado(True)], bancos=[1.5, 2.25, 9.0, 9.0]) as amb:
        arq = lbm.arquivo_do_registro(amb.pasta)
        lbm.gravar_evento(arq, "inicio", lbm.vez_do_cenario(1, p), relogio=lambda: T0)
        amb.agora = T0 + 60
        assert _rodar("conferir", "--vez", "1", str(p), "--seletor", "#errado", "--registro", str(amb.pasta)) == 1
        amb.agora = T0 + 130
        assert _rodar("conferir", "--vez", "1", str(p), "--seletor", "input[name=search]", "--registro", str(amb.pasta)) == 0
        eventos = lbm.ler_registro(arq)
        assert [e["evento"] for e in eventos] == ["inicio", "tentativa", "tentativa"]
        t1, t2 = eventos[1:]
        assert (t1["seletor"], t1["corrigido"], t1["segundos_do_banco"], t1["segundos_do_roteiro"]) == ("#errado", False, 1.5, 3.2) and t1["motivo"]
        assert (t2["seletor"], t2["corrigido"], t2["segundos_do_banco"], t2["motivo"]) == ("input[name=search]", True, 2.25, None)
        assert abs(t1["relogio_s"] - (T0 + 60)) < 1e-6 and abs(t2["relogio_s"] - (T0 + 130)) < 1e-6
        assert (t2["integrante"], t2["ordem"], t2["cenario"], t2["tipo"]) == (1, p, "localizador-front-busca", "localizador")
        # o roteiro que rodou é o do agente com o seletor do integrante no lugar do quebrado (a mesma troca da versão 1)
        seletores = [c[1] for c in amb.chamadas if c[0] == "roteiro"][-1]
        assert seletores[q["passo_alvo"]] == "input[name=search]" and q["localizador"] not in seletores
        r = lbm.resumo_do_registro(eventos)[(1, p)]
        assert (r["tentativas"], r["seletor"], r["descontar_s"], r["segundos"]) == (2, "input[name=search]", 3.75, 126.25)
        assert r["fim"] == t2["hora"] and r["corrigido"] is True and r["fechado"] is True and r["causa"] is None and r["campo"] is None
        tela = amb.saida.getvalue()
        assert "não corrigido" in tela and "CORRIGIDO (o roteiro chegou ao fim sem erro)" in tela
        # sem seletor (a conferência de que a quebra está armada) e pelo nome (o ensaio): nada é gravado
        assert _rodar("conferir", "--vez", "1", str(p), "--registro", str(amb.pasta)) == 0
        assert _rodar("conferir", "--cenario", "localizador-front-busca", "--seletor", "input[name=search]", "--registro", str(amb.pasta)) == 0
        assert len(lbm.ler_registro(arq)) == 3


def teste_resumo_do_registro_aplica_o_limite_e_diz_o_que_esta_aberto():
    assert lbm.LIMITE_S == 600, "o limite do protocolo: 10 minutos por cenário"
    p = _posicao(1, "contrato-type_drift")
    vez = lbm.vez_do_cenario(1, p)
    # só armado: o cenário está aberto, e a planilha não é preenchida com ele
    r = lbm.resumo_do_registro([lbm.montar_evento("inicio", vez, T0)])[(1, p)]
    assert r["fechado"] is False and r["fim"] is None and r["segundos"] is None and r["corrigido"] is False and r["inicio"].endswith(".000")
    # o armar foi encerrado sem entrega: fechado, não corrigido, sem fim
    r = lbm.resumo_do_registro([lbm.montar_evento("inicio", vez, T0), lbm.montar_evento("fim_do_armar", vez, T0 + 700)])[(1, p)]
    assert r["fechado"] is True and r["fim"] is None and r["corrigido"] is False and r["estourou"] is False
    # exatamente no limite ainda vale; um milésimo depois, não: fica sem fim e não corrigido, mesmo com a causa e o campo certos
    r = lbm.resumo_do_registro(_contrato(1, p, 600.0, "tipo_divergente", "preco"))[(1, p)]
    assert r["segundos"] == 600.0 and r["corrigido"] is True and r["estourou"] is False
    r = lbm.resumo_do_registro(_contrato(1, p, 600.001, "tipo_divergente", "preco"))[(1, p)]
    assert (r["fim"], r["segundos"], r["corrigido"], r["estourou"], r["fechado"]) == (None, None, False, True, True)
    assert r["causa"] is None and r["campo"] is None, "a resposta que chegou depois do limite fica só no registro"
    # no localizador o banco é descontado antes de comparar com o limite
    pl = _posicao(1, "localizador-front-busca")
    r = lbm.resumo_do_registro(_localizador(1, pl, [(300.0, "#a", False, 3.0), (605.0, "#b", True, 6.0)]))[(1, pl)]
    assert (r["segundos"], r["descontar_s"], r["tentativas"], r["seletor"], r["corrigido"], r["estourou"]) == (596.0, 9.0, 2, "#b", True, False)
    r = lbm.resumo_do_registro(_localizador(1, pl, [(300.0, "#a", False, 3.0), (610.0, "#b", True, 6.0)]))[(1, pl)]
    assert (r["fim"], r["segundos"], r["corrigido"], r["estourou"], r["seletor"], r["tentativas"]) == (None, None, False, True, "#b", 2)
    # nenhuma tentativa passou: o seletor é o último tentado; tentativa depois da que corrigiu não conta
    r = lbm.resumo_do_registro(_localizador(1, pl, [(100.0, "#a", False, 2.0), (200.0, "#b", False, 2.0)]))[(1, pl)]
    assert (r["seletor"], r["tentativas"], r["corrigido"], r["fechado"], r["descontar_s"]) == ("#b", 2, False, False, 4.0)
    r = lbm.resumo_do_registro(_localizador(1, pl, [(100.0, "#a", True, 2.0), (200.0, "#b", False, 2.0)]))[(1, pl)]
    assert (r["seletor"], r["tentativas"], r["segundos"], r["descontar_s"]) == ("#a", 1, 98.0, 2.0)
    # a vez armada duas vezes: vale o primeiro início, e o resumo avisa
    eventos = [lbm.montar_evento("inicio", vez, T0), lbm.montar_evento("fim_do_armar", vez, T0 + 20), lbm.montar_evento("inicio", vez, T0 + 30)]
    r = lbm.resumo_do_registro(eventos)[(1, p)]
    assert r["inicio"] == eventos[0]["hora"] and r["fechado"] is False and any("armada 2 vezes" in a for a in r["avisos"])
    r = lbm.resumo_do_registro(eventos + _contrato(1, p, 90.0, "tipo_divergente", "preco", t0=T0 + 30)[1:])[(1, p)]
    assert r["segundos"] == 120.0, "o cronômetro corre desde o primeiro início"
    # cada vez é lida só com os eventos dela; o treino e o que não tem integrante ficam de fora
    tudo = (_contrato(1, p, 50.0, "tipo_divergente", "preco") + _localizador(2, _posicao(2, "localizador-front-busca"), [(40.0, "#a", True, 1.0)])
            + [lbm.montar_evento("treino", {"integrante": 1}, T0, parte="contrato")])
    resumo = lbm.resumo_do_registro(tudo)
    assert sorted(resumo) == [(1, p), (2, _posicao(2, "localizador-front-busca"))] and resumo[(1, p)]["segundos"] == 50.0
    # o cronômetro de uma vez, para os avisos do facilitador: quanto passou (descontado o banco) e se já acabou
    aberto = _localizador(1, pl, [(100.0, "#a", False, 4.0)])
    assert lbm.cronometro_da_vez(aberto, 1, pl, T0 + 500) == {"passado_s": 496.0, "fechado": False}
    assert lbm.cronometro_da_vez(aberto, 1, pl + 1, T0 + 500) is None
    assert lbm.cronometro_da_vez(_contrato(1, p, 50.0, "tipo_divergente", "preco"), 1, p, T0 + 500)["fechado"] is True
    assert lbm.AVISO_FINAL_S == 120 and [s for s, _ in lbm.avisos_do_limite()] == [lbm.LIMITE_S - lbm.AVISO_FINAL_S, lbm.LIMITE_S]


# ----------------------------------------------------------------------------- a planilha preenchida pelo registro

def teste_planilha_preenche_as_celulas_vazias_a_partir_do_registro():
    em_branco = lbm.planilha_modelo(lbm.ordem_dos_integrantes())
    pc, pl, pa = _posicao(1, "contrato-malformed_json"), _posicao(1, "localizador-front-busca"), _posicao(1, "contrato-error_500")
    eventos = (_contrato(1, pc, 83.417, "resposta_truncada", None)
               + _localizador(1, pl, [(60.0, "#errado", False, 1.5), (130.0, "input[name=search]", True, 2.25)], t0=T0 + 1000)
               + [lbm.montar_evento("inicio", lbm.vez_do_cenario(1, pa), T0 + 2000)])       # ainda aberto
    novo, preenchidas, avisos = lbm.preencher_planilha(em_branco, lbm.resumo_do_registro(eventos))
    assert avisos == [] and len(preenchidas) == 2
    assert _linha(novo, 1, pc) == {"integrante": "1", "ordem": str(pc), "cenario": "contrato-malformed_json", "tipo": "contrato", "inicio": _hms(T0),
                                   "fim": _hms(T0 + 83), "segundos": "83,417", "descontar_s": "0", "causa": "resposta_truncada", "campo": "nenhum",
                                   "seletor": "", "tentativas": "", "corrigido": "sim", "observacoes": ""}
    assert _linha(novo, 1, pl) == {"integrante": "1", "ordem": str(pl), "cenario": "localizador-front-busca", "tipo": "localizador", "inicio": _hms(T0 + 1000),
                                   "fim": _hms(T0 + 1130), "segundos": "126,250", "descontar_s": "3,75", "causa": "", "campo": "",
                                   "seletor": "input[name=search]", "tentativas": "2", "corrigido": "sim", "observacoes": ""}
    assert _linha(novo, 1, pa) == _linha(em_branco, 1, pa), "cenário ainda aberto não entra na planilha"
    # o resto não muda: o cabeçalho, as outras linhas e as quatro colunas do sorteio
    antes, depois = em_branco.splitlines(), novo.splitlines()
    assert len(antes) == len(depois) == 31 and depois[0] == antes[0] == lbm.SEPARADOR.join(lbm.COLUNAS_DA_PLANILHA)
    assert sum(a != d for a, d in zip(antes, depois)) == 2 and [d.split(";")[:4] for d in depois] == [a.split(";")[:4] for a in antes]
    # rodar de novo não muda nada
    assert lbm.preencher_planilha(novo, lbm.resumo_do_registro(eventos)) == (novo, [], [])
    # resposta errada e cenário que estourou o limite
    pe, pt = _posicao(2, "contrato-error_500"), _posicao(2, "contrato-type_drift")
    eventos = _contrato(2, pe, 45.0, "corpo_vazio", "preco") + _contrato(2, pt, 700.0, "tipo_divergente", "preco", t0=T0 + 1000)
    novo, _, avisos = lbm.preencher_planilha(em_branco, lbm.resumo_do_registro(eventos))
    a, b = _linha(novo, 2, pe), _linha(novo, 2, pt)
    assert (a["segundos"], a["causa"], a["campo"], a["corrigido"]) == ("45,000", "corpo_vazio", "preco", "não")
    assert (b["inicio"], b["fim"], b["segundos"], b["causa"], b["campo"], b["corrigido"]) == (_hms(T0 + 1000), "", "", "", "", "não") and avisos == []
    # as células saem de celulas_do_resumo, e os números voltam com vírgula ou com ponto
    r = lbm.resumo_do_registro(_contrato(1, pc, 83.417, "resposta_truncada", None))[(1, pc)]
    assert lbm.celulas_do_resumo(r) == {k: _linha(lbm.preencher_planilha(em_branco, {(1, pc): r})[0], 1, pc)[k] for k in lbm.COLUNAS_DO_REGISTRO}
    assert lbm.COLUNAS_DO_REGISTRO == ("inicio", "fim", "segundos", "descontar_s", "causa", "campo", "seletor", "tentativas", "corrigido")
    assert lbm.numero("83,417") == 83.417 == lbm.numero("83.417") and lbm.numero(" 0 ") == 0.0 and lbm.numero("") is None and lbm.numero("abc") is None


def teste_planilha_nunca_troca_celula_preenchida_e_avisa_quando_discorda():
    em_branco = lbm.planilha_modelo(lbm.ordem_dos_integrantes())
    pc = _posicao(1, "contrato-malformed_json")
    resumo = lbm.resumo_do_registro(_contrato(1, pc, 83.417, "resposta_truncada", None))
    cheia, _, _ = lbm.preencher_planilha(em_branco, resumo)
    original = next(x for x in cheia.splitlines() if x.startswith(f"1;{pc};"))
    # o facilitador escreveu outro tempo, outra causa e uma observação: nada disso é trocado, e cada diferença vira um aviso
    assert original.endswith(";sim;"), "a última célula (observacoes) está vazia"
    a_mao = original.replace("83,417", "90").replace("resposta_truncada", "corpo_vazio") + "o integrante pediu para repetir"
    planilha = cheia.replace(original, a_mao)
    novo, preenchidas, avisos = lbm.preencher_planilha(planilha, resumo)
    assert novo == planilha and preenchidas == []
    assert len(avisos) == 2 and all("integrante 1" in a and f"ordem {pc}" in a for a in avisos)
    assert any("segundos" in a and "90" in a and "83,417" in a for a in avisos) and any("causa" in a and "corpo_vazio" in a and "resposta_truncada" in a for a in avisos)
    # linha preenchida pela metade: as vazias são preenchidas, a que discorda fica e é avisada
    meia = em_branco.replace(f"1;{pc};contrato-malformed_json;contrato;;;;", f"1;{pc};contrato-malformed_json;contrato;;;90;")
    novo, preenchidas, avisos = lbm.preencher_planilha(meia, resumo)
    linha = _linha(novo, 1, pc)
    assert linha["segundos"] == "90" and linha["inicio"] == _hms(T0) and linha["causa"] == "resposta_truncada" and len(avisos) == 1 and len(preenchidas) == 1
    # a mesma coisa escrita de outro jeito não é diferença, e a célula fica como o facilitador a escreveu
    igual = original.replace("83,417", "83.417").replace(";sim;", ";Sim;").replace(";nenhum;", ";Nenhum;")
    assert igual != original
    planilha = cheia.replace(original, igual)
    assert lbm.preencher_planilha(planilha, resumo) == (planilha, [], [])
    nao = lbm.resumo_do_registro(_contrato(1, pc, 83.417, "corpo_vazio", None))
    com_nao, _, _ = lbm.preencher_planilha(em_branco, nao)
    sem_til = com_nao.replace(";não;", ";nao;")
    assert sem_til != com_nao and lbm.preencher_planilha(sem_til, nao) == (sem_til, [], [])
    # registro de uma vez que a planilha não tem: aviso, e a planilha não ganha linha
    fora = lbm.resumo_do_registro(_contrato(1, pc, 83.417, "resposta_truncada", None))
    fora[(4, 1)] = {**fora[(1, pc)], "integrante": 4, "ordem": 1}
    novo, _, avisos = lbm.preencher_planilha(cheia, fora)
    assert novo == cheia and len(avisos) == 1 and "integrante 4" in avisos[0]


def teste_planilha_marca_a_linha_anotada_a_mao_e_o_comando_grava_com_bom():
    assert lbm.MARCA_A_MAO == "anotada à mão"
    em_branco = lbm.planilha_modelo(lbm.ordem_dos_integrantes())
    p1, p2, p3 = 1, 2, 3
    c = {p: lbm.cenario_da_vez(3, p) for p in (p1, p2, p3)}
    tipo = {x["id"]: x["tipo"] for x in cen.CENARIOS_DO_ENSAIO}

    def a_mao(p: int, observacoes: str) -> tuple[str, str]:
        vazia = f"3;{p};{c[p]};{tipo[c[p]]};;;;;;;;;;"
        return vazia, f"3;{p};{c[p]};{tipo[c[p]]};14:00:00;14:03:10;190;0;campo_ausente;preco;;;sim;{observacoes}"

    planilha = em_branco
    for p, obs in ((p1, ""), (p2, "a ferramenta travou no meio"), (p3, "valeu o cronômetro do celular, anotada à mão")):
        vazia, cheia = a_mao(p, obs)
        assert vazia in planilha
        planilha = planilha.replace(vazia, cheia)
    novo, _, avisos = lbm.preencher_planilha(planilha, {})
    # sem observação: a marca entra na célula vazia; com observação sem a marca: a célula fica e o comando pede a marca; com a marca: nada
    assert _linha(novo, 3, p1)["observacoes"] == lbm.MARCA_A_MAO
    assert _linha(novo, 3, p2)["observacoes"] == "a ferramenta travou no meio" and _linha(novo, 3, p3)["observacoes"] == "valeu o cronômetro do celular, anotada à mão"
    assert len(avisos) == 1 and "integrante 3" in avisos[0] and f"ordem {p2}" in avisos[0] and lbm.MARCA_A_MAO in avisos[0]
    for p in (p1, p2, p3):
        assert {k: v for k, v in _linha(novo, 3, p).items() if k != "observacoes"} == {k: v for k, v in _linha(planilha, 3, p).items() if k != "observacoes"}
    assert sum(a != d for a, d in zip(planilha.splitlines(), novo.splitlines())) == 1
    assert lbm.preencher_planilha(novo, {})[0] == novo, "a marca não entra duas vezes"
    # o comando: lê o registro, grava a planilha em UTF-8 com BOM e sai 0; discordância sai 1; --sem-gravar não grava
    planilha_de_verdade = lbm.PLANILHA
    pc = _posicao(1, "contrato-malformed_json")
    try:
        with _ambiente() as amb:
            lbm.PLANILHA = amb.pasta / "planilha.csv"
            assert _rodar("planilha", "--registro", str(amb.pasta)) == 2, "sem a planilha do sorteio o comando para"
            lbm.PLANILHA.write_text(em_branco, encoding="utf-8-sig")
            arq = lbm.arquivo_do_registro(amb.pasta)
            for e in _contrato(1, pc, 83.417, "resposta_truncada", None):
                with open(arq, "a", encoding="utf-8") as f:
                    f.write(json.dumps(e, ensure_ascii=False) + "\n")
            assert _rodar("planilha", "--registro", str(amb.pasta), "--sem-gravar") == 0
            assert lbm.PLANILHA.read_text(encoding="utf-8-sig") == em_branco
            assert _rodar("planilha", "--registro", str(amb.pasta)) == 0
            assert lbm.PLANILHA.read_bytes().startswith(b"\xef\xbb\xbf")
            gravada = lbm.PLANILHA.read_text(encoding="utf-8-sig")
            assert _linha(gravada, 1, pc)["segundos"] == "83,417" and _linha(gravada, 1, pc)["corrigido"] == "sim"
            horario = lbm.PLANILHA.stat().st_mtime_ns
            assert _rodar("planilha", "--registro", str(amb.pasta)) == 0 and lbm.PLANILHA.stat().st_mtime_ns == horario, "sem nada a preencher o arquivo não é regravado"
            lbm.PLANILHA.write_text(gravada.replace("83,417", "99"), encoding="utf-8-sig")
            assert _rodar("planilha", "--registro", str(amb.pasta)) == 1
            assert _linha(lbm.PLANILHA.read_text(encoding="utf-8-sig"), 1, pc)["segundos"] == "99" and "!!" in amb.saida.getvalue()
            # a planilha que o Excel regravou na codificação do Windows (cp1252) é lida assim mesmo, e volta em UTF-8 com BOM
            vazia, cheia = a_mao(p2, lbm.MARCA_A_MAO)
            lbm.PLANILHA.write_text(em_branco.replace(vazia, cheia), encoding="cp1252")
            assert not lbm.PLANILHA.read_bytes().startswith(b"\xef\xbb\xbf")
            assert _rodar("planilha", "--registro", str(amb.pasta)) == 0
            regravada = lbm.PLANILHA.read_text(encoding="utf-8-sig")
            assert lbm.PLANILHA.read_bytes().startswith(b"\xef\xbb\xbf") and _linha(regravada, 1, pc)["segundos"] == "83,417"
            assert _linha(regravada, 3, p2)["observacoes"] == lbm.MARCA_A_MAO and _linha(regravada, 3, p2)["segundos"] == "190"
    finally:
        lbm.PLANILHA = planilha_de_verdade


# ----------------------------------------------------------------------------- o treino, o perfil e os textos

def teste_treino_nao_usa_nenhum_dos_dez_cenarios_nem_o_cronometro():
    dez = cen.CENARIOS_DO_ENSAIO
    tc, ts = lbm.TREINO_DE_CONTRATO, lbm.TREINO_DE_SELETOR
    # o cenário de contrato do treino é o modo que saiu do catálogo pela troca da ficha 36
    assert tc["modo"] == cen.TROCA_DA_FICHA_36["sai"] == "latency" and tc["modo"] not in {c["modo"] for c in dez}
    assert cen.MODO_POR_CAUSA[tc["causa"]] == tc["modo"] and tc["causa"] not in {c["causa"] for c in dez} and tc["campo"] is None
    # o exercício de seletor é numa página que não está nos quatro roteiros de localizador, e o alvo é o botão "Saiba Mais..."
    assert ts["pagina"] == "produtos_api.php" and ts["pagina"] not in cen.PAGINA_DA_QUEBRA.values()
    assert ts["cenario"] == "api-catalogo" and ts["cenario"] not in cen.ROTEIROS_DA_CURA and ts["alvo"]["nome"] == "Saiba Mais..."
    for t in (tc, ts):
        assert t["id"] not in {c["id"] for c in dez}
        try:
            lbm.cenario_do_ensaio(t["id"])
        except ValueError:
            pass
        else:
            raise AssertionError(f"{t['id']} aceito como um dos dez cenários")
    ficha = lbm.ficha_do_treino()
    assert "o roteiro passou na tela, mas o fio acusou" in ficha and "orçamento de 1000 ms" in ficha

    def enter(pergunta):
        visto["no_enter"] = list(amb.chamadas)
        return ""

    # treino de contrato: liga o modo do treino, mostra o mesmo material de um cenário de contrato e não mexe no cronômetro
    visto = {}
    with _ambiente(respostas=[enter, "tempo_de_resposta_excedido", "nenhum"]) as amb:
        assert _rodar("treino", "contrato", "--integrante", "2", "--registro", str(amb.pasta)) == 0
        eventos = lbm.ler_registro(lbm.arquivo_do_registro(amb.pasta))
    assert [c for c in amb.chamadas if c[0] == "modo"] == [("modo", "latency", None), ("modo", "normal", None)]
    assert ("modo", "latency", None) in visto["no_enter"] and ("abrir", cen.BASE_PADRAO + "produtos_api.php") in visto["no_enter"]
    assert not any(c[0] in ("cookies", "script_de_quebra", "roteiro") for c in amb.chamadas), "nenhuma quebra de localizador é armada"
    assert [(e["evento"], e["integrante"], e["parte"], e["ordem"], e["cenario"]) for e in eventos] == [("treino", 2, "contrato", None, None)]
    assert (eventos[0]["causa"], eventos[0]["campo"], eventos[0]["acertou"]) == ("tempo_de_resposta_excedido", None, True)
    assert lbm.resumo_do_registro(eventos) == {}, "o treino não entra na leitura do tempo"
    tela = amb.saida.getvalue()
    _em_ordem(tela, ["== Ficha da falha", lbm.ficha_do_treino(), "== Roteiro do teste", "== Contrato esperado", "CONTRATO DE TESTE", ", ".join(taxonomia.CAUSAS_RAIZ),
                     "sem cronômetro"])
    assert "início do cronômetro" not in tela
    # sem --integrante (o ensaio do facilitador): nada é gravado
    with _ambiente(respostas=["", ""]) as amb:
        assert _rodar("treino", "contrato", "--registro", str(amb.pasta)) == 0
        assert not lbm.arquivo_do_registro(amb.pasta).exists()
    # exercício de seletor: a página sem falha nenhuma, e o seletor do integrante tem de achar o primeiro botão
    with _ambiente() as amb:
        assert _rodar("treino", "seletor", "--integrante", "2", "--seletor", ".saiba-mais", "--registro", str(amb.pasta)) == 0
        eventos = lbm.ler_registro(lbm.arquivo_do_registro(amb.pasta))
        amb.acha = (0, False)
        assert _rodar("treino", "seletor", "--seletor", "#nao-existe", "--registro", str(amb.pasta)) == 1
        assert len(lbm.ler_registro(lbm.arquivo_do_registro(amb.pasta))) == 1
    assert [c for c in amb.chamadas if c[0] == "modo"] == [("modo", "normal", None)] * 2
    assert ("abrir", cen.BASE_PADRAO + "produtos_api.php") in amb.chamadas and ("localizar", ".saiba-mais") in amb.chamadas
    assert not any(c[0] in ("cookies", "script_de_quebra", "roteiro", "banco") for c in amb.chamadas)
    assert [(e["evento"], e["parte"], e["seletor"], e["achou"], e["cenario"]) for e in eventos] == [("treino", "seletor", ".saiba-mais", True, None)]
    # com a janela: o facilitador cola os seletores um a um, e a linha vazia encerra
    with _ambiente(respostas=["#nao-existe", ".saiba-mais", ""]) as amb:
        amb.acha = (14, True)
        assert _rodar("treino", "seletor", "--integrante", "1", "--registro", str(amb.pasta)) == 0
        eventos = lbm.ler_registro(lbm.arquivo_do_registro(amb.pasta))
    assert ("navegador", "chromium", "com janela") in amb.chamadas and len(amb.perguntas) == 3
    assert [(e["parte"], e["seletor"], e["achou"]) for e in eventos] == [("seletor", ".saiba-mais", True)] and "sem cronômetro" in amb.saida.getvalue()


def teste_perfil_grava_as_tres_perguntas_sem_o_nome():
    assert list(lbm.PERGUNTAS_DE_PERFIL) == ["pratica", "ja_usou_as_ferramentas_do_desenvolvedor", "ja_leu_a_lista_dos_cenarios"], "as três da seção 4.1 do plano"
    assert all(p.endswith("?") for p in lbm.PERGUNTAS_DE_PERFIL.values()) and list(lbm.ANOTACAO_DO_FACILITADOR) == ["conhece_o_codigo_das_cobaias"]
    arq = lbm.arquivo_dos_participantes(_tmp())
    assert arq.name == "participantes.json" and lbm.arquivo_dos_participantes().parts[-2:] == ("fase5_manual", "participantes.json")
    perfil = lbm.perfil_do_integrante({"pratica": "dois anos de programação para a web, nenhum de teste", "ja_usou_as_ferramentas_do_desenvolvedor": True,
                                       "ja_leu_a_lista_dos_cenarios": False, "conhece_o_codigo_das_cobaias": True, "o_que_conhece": "o HTML do site legado"})
    lbm.gravar_perfil(arq, 2, perfil, agora="2026-11-19T14:00:00")
    dado = json.loads(arq.read_text(encoding="utf-8"))
    assert dado["integrantes"] == {"2": {**perfil, "respondido_em": "2026-11-19T14:00:00"}} and dado["perguntas"] == {**lbm.PERGUNTAS_DE_PERFIL, **lbm.ANOTACAO_DO_FACILITADOR}
    assert "de IA - Revisar" in dado["tag_ia"]["alteracao"] and dado["tag_ia"]["motivo"].startswith("! Motivo")
    assert "nome" not in json.dumps(dado["integrantes"], ensure_ascii=False).lower(), "o repositório é público: o perfil não guarda quem é"
    # nenhum campo a mais (o nome, por exemplo) e nenhum a menos; só os integrantes da planilha; um perfil não é trocado sem pedir
    for ruim in ({**perfil, "nome": "Fulano"}, {k: v for k, v in perfil.items() if k != "pratica"}, {**perfil, "ja_leu_a_lista_dos_cenarios": "talvez"}):
        try:
            lbm.perfil_do_integrante(ruim)
        except ValueError:
            pass
        else:
            raise AssertionError(f"perfil aceito: {sorted(ruim)}")
    for n, regravar in ((0, False), (4, False), (2, False)):
        try:
            lbm.gravar_perfil(arq, n, perfil, regravar=regravar)
        except ValueError:
            pass
        else:
            raise AssertionError(f"perfil do integrante {n} gravado")
    lbm.gravar_perfil(arq, 1, lbm.perfil_do_integrante({**perfil, "conhece_o_codigo_das_cobaias": False, "o_que_conhece": ""}), agora="2026-11-20T09:00:00")
    lbm.gravar_perfil(arq, 2, perfil, agora="2026-11-21T09:00:00", regravar=True)
    dado = json.loads(arq.read_text(encoding="utf-8"))
    assert sorted(dado["integrantes"]) == ["1", "2"] and dado["integrantes"]["2"]["respondido_em"] == "2026-11-21T09:00:00"
    # o comando: pelas opções ou pelo teclado; quem já leu a lista é avisado na tela, e o perfil é gravado assim mesmo
    with _ambiente() as amb:
        assert _rodar("perfil", "--integrante", "3", "--pratica", "um ano de teste manual", "--devtools", "sim", "--leu-a-lista", "sim", "--conhece-o-codigo", "nao",
                      "--registro", str(amb.pasta)) == 0
        gravado = json.loads(lbm.arquivo_dos_participantes(amb.pasta).read_text(encoding="utf-8"))["integrantes"]["3"]
        assert (gravado["pratica"], gravado["ja_usou_as_ferramentas_do_desenvolvedor"], gravado["ja_leu_a_lista_dos_cenarios"], gravado["conhece_o_codigo_das_cobaias"]) == \
            ("um ano de teste manual", True, True, False)
        assert "já leu a lista" in amb.saida.getvalue() and amb.perguntas == []
    with _ambiente(respostas=["seis meses de programação para a web", "n", "não", "s", "a CobaiaAPI"]) as amb:
        assert _rodar("perfil", "--integrante", "1", "--registro", str(amb.pasta)) == 0
        gravado = json.loads(lbm.arquivo_dos_participantes(amb.pasta).read_text(encoding="utf-8"))["integrantes"]["1"]
        assert (gravado["ja_usou_as_ferramentas_do_desenvolvedor"], gravado["ja_leu_a_lista_dos_cenarios"], gravado["conhece_o_codigo_das_cobaias"], gravado["o_que_conhece"]) == \
            (False, False, True, "a CobaiaAPI")
        for pergunta, texto in zip(amb.perguntas, lbm.PERGUNTAS_DE_PERFIL.values()):
            assert texto in pergunta, "o facilitador lê na tela a pergunta como ela está escrita"


def _sem_o_que_entrega_a_resposta(texto: str, onde: str) -> None:
    """Nenhum texto que o integrante lê ou ouve traz o nome de um dos dez cenários, de um modo de falha ou de um modo de quebra."""
    modos = ({c["modo"] for c in cen.CENARIOS_DO_ENSAIO} | set(cen.MODO_POR_CAUSA.values()) | set(cen.MODOS_DE_QUEBRA)) - set(taxonomia.CAUSAS_RAIZ)
    for proibido in sorted({c["id"] for c in cen.CENARIOS_DO_ENSAIO} | modos | {"preco", "_v2"}):
        assert proibido not in texto, f"{onde} traz {proibido!r}"
    for marca in ("—", "→", "↔"):
        assert marca not in texto, f"{onde} com {marca}"


def teste_folha_do_integrante_tem_a_definicao_de_uma_linha_das_23_causas():
    assert list(lbm.DEFINICAO_DAS_CAUSAS) == list(taxonomia.CAUSAS_RAIZ), "as 23, na ordem da lista fechada que o modelo recebe"
    folha = lbm.folha_do_integrante()
    linhas = folha.splitlines()
    for i, causa in enumerate(taxonomia.CAUSAS_RAIZ, 1):
        definicao = lbm.DEFINICAO_DAS_CAUSAS[causa]
        assert definicao and "\n" not in definicao and len(definicao) <= 110 and not definicao.endswith("."), (causa, definicao)
        assert f"{i}. `{causa}`: {definicao}" in linhas, f"a folha não traz a linha da causa {causa}"
    posicoes = [linhas.index(f"{i}. `{c}`: {lbm.DEFINICAO_DAS_CAUSAS[c]}") for i, c in enumerate(taxonomia.CAUSAS_RAIZ, 1)]
    assert posicoes == sorted(posicoes)
    _sem_o_que_entrega_a_resposta(folha, "a folha do integrante")
    assert "100" not in " ".join(lbm.DEFINICAO_DAS_CAUSAS.values()), "a definição não diz como a falha foi armada"
    # o que a seção 5 do protocolo dá ao integrante: o que recebe, o que pode, o que não pode, como responde e o limite
    for trecho in ("Pode", "Não pode", "ficha da falha", "roteiro", "F12", "bloco de notas", "assistente de IA", f"{lbm.LIMITE_S // 60} minutos",
                   f"{lbm.SEGUNDOS_DA_VOLTA_DO_LOGIN} segundos", "nenhum"):
        assert trecho in folha, f"a folha não fala de {trecho!r}"
    # o aviso da tela de login repete o que o front legado faz (admin/login.php volta sozinha para a página inicial)
    php = (RAIZ / "Programacao" / "CobaiaFront" / "admin" / "login.php").read_text(encoding="utf-8", errors="replace")
    assert f'http-equiv="refresh" content="{lbm.SEGUNDOS_DA_VOLTA_DO_LOGIN};' in php
    # a folha sai pelo comando, na tela ou num arquivo para imprimir
    with _ambiente() as amb:
        assert _rodar("folha") == 0 and amb.saida.getvalue().strip() == folha.strip()
        destino = amb.pasta / "folha.md"
        assert _rodar("folha", "--gravar", str(destino)) == 0 and destino.read_text(encoding="utf-8").strip() == folha.strip()


def teste_texto_fixo_do_facilitador_traz_as_falas_e_as_perguntas_de_perfil():
    texto = lbm.texto_do_facilitador()
    # as três falas do plano (seção 4.3) e as que repetem o que a ferramenta mostrou
    assert lbm.FALAS_DO_PLANO == ("O tempo está correndo.", "Faltam dois minutos.", "Pode entregar quando quiser.")
    assert lbm.AVISO_FINAL_S == 2 * 60, "a fala dos dois minutos é dita quando a ferramenta avisa, dois minutos antes do limite"
    assert len(lbm.FALAS_DA_FERRAMENTA) == 4
    for fala in lbm.FALAS_DO_PLANO + lbm.FALAS_DA_FERRAMENTA:
        assert f'"{fala}"' in texto, fala
    assert [f for _, f in lbm.avisos_do_limite()] == [lbm.FALAS_DO_PLANO[1], lbm.FALAS_DA_FERRAMENTA[-1]]
    for pergunta in lbm.PERGUNTAS_DE_PERFIL.values():
        assert pergunta in texto
    for trecho in ("Abertura", "Treino", "Durante um cenário", "Fecho", "sem cronômetro", f"{lbm.LIMITE_S // 60} minutos", f"{lbm.SEGUNDOS_DA_VOLTA_DO_LOGIN} segundos",
                   "observacoes", "não comente", "cronômetro de reserva"):
        assert trecho in texto, f"o texto do facilitador não fala de {trecho!r}"
    assert str(len(cen.CENARIOS_DO_ENSAIO)) in texto or "dez" in texto
    _sem_o_que_entrega_a_resposta(texto, "o texto do facilitador")
    with _ambiente() as amb:
        assert _rodar("falas") == 0 and amb.saida.getvalue().strip() == texto.strip()


def teste_protocolo_esta_na_versao_2_com_os_textos_que_o_comando_gera():
    protocolo = lbm.PROTOCOLO.read_text(encoding="utf-8")
    assert lbm.PROTOCOLO.name == "protocolo-linha-de-base-manual.md" and "Versão 2" in protocolo
    # os textos fixos estão no protocolo como blocos gerados: iguais ao que o comando imprime, conferidos por `protocolo --check`
    import analisar_fase3b as a3b
    no_documento = a3b.blocos_de(protocolo)
    gerados = a3b.blocos_de(lbm.blocos_do_protocolo())
    assert sorted(gerados) == ["tb_f5_folha_do_integrante", "tb_f5_texto_do_facilitador"] and sorted(no_documento) == sorted(gerados)
    assert lbm.folha_do_integrante().strip() in gerados["tb_f5_folha_do_integrante"] and lbm.texto_do_facilitador().strip() in gerados["tb_f5_texto_do_facilitador"]
    assert lbm.conferir_protocolo() == [], "o protocolo tem um bloco diferente do que o comando gera: rode `protocolo --colar`"
    with _ambiente():
        assert _rodar("protocolo", "--check") == 0
    # as seções que a decisão 131 mudou dizem o que mudou
    for trecho in ("`entregar`", "`treino", "`planilha`", "`perfil`", "sessao.jsonl", "participantes.json", "cronômetro de reserva", "folha de papel", lbm.MARCA_A_MAO):
        assert trecho in protocolo, f"o protocolo não fala de {trecho!r}"
    assert protocolo.count("! Alteração de IA - Revisar") >= 8 and protocolo.count("! Motivo") >= 8, "cada seção mudada leva a tag e o motivo (as duas da versão 1 mais as seis seções da versão 2)"
    # ! Alteração de IA - Revisar: (16/11/2026, decisão 136) o protocolo também tem de dizer a versão 3: a sessão pela página publicada.
    # ! Motivo: as sessões passaram a ser feitas pelo artefato; sem a seção, o documento descreveria só a forma presencial, que virou reserva.
    for trecho in ("Versão 3", "decisão 136", "## 11. A sessão pela página publicada", "linha_de_base_manual.py material", "linha_de_base_manual.py paginas --gravar",
                   "linha_de_base_manual.py importar --arquivo", "sessao-integrante-", "fase5_material/material.json",
                   "código da sessão", "Abrir o cenário", "convidado por e-mail como editor", "roteiro de verdade"):
        assert trecho in protocolo, f"o protocolo não fala de {trecho!r} (versão 3)"
    # ! Alteração de IA - Revisar: (17/11/2026, ficha 77, decisão 137) a seção 11 do protocolo tem de dizer como o integrante avisa de
    # uma falha do protocolo na sessão pela página e como o facilitador decide a anulação.
    # ! Motivo: a regra L14 pede a falha anotada na hora, e a seção 8 só dizia quem anota na forma presencial (o facilitador).
    for trecho in ("decisão 137", "regra L14", lbm.PERGUNTA_DA_OCORRENCIA, "--anular", "aviso do integrante"):
        assert trecho in protocolo, f"o protocolo não fala de {trecho!r} (aviso do integrante)"


# ! Alteração de IA - Revisar: (16/11/2026, F2) teste do comando `ensaio`, que imprime o passo a passo do ensaio do facilitador.
# ! Motivo: o protocolo (seção 4, item 3) pede que o facilitador rode os dez cenários uma vez pelo nome antes das sessões; com os
# comandos saindo do catálogo, o passo a passo não fica velho se um cenário mudar de nome, e o teste garante que nenhum comando
# do ensaio grava no registro da sessão de verdade.
def teste_ensaio_do_facilitador_sai_do_catalogo_e_nao_toca_no_registro_de_verdade():
    texto = lbm.passos_do_ensaio()
    linhas = [x.strip() for x in texto.splitlines()]
    comandos = [x for x in linhas if x.startswith("python linha_de_base_manual.py ")]
    # os dez cenários pelo nome, na ordem do catálogo, sem cronômetro
    assert [x.split()[-1] for x in comandos if " armar --cenario " in x] == [c["id"] for c in cen.CENARIOS_DO_ENSAIO]
    # os quatro de localizador: sem seletor (a quebra está armada) e com um seletor que conserta
    assert set(lbm.SELETOR_DO_ENSAIO) == {c["id"] for c in cen.CENARIOS_DE_LOCALIZADOR}
    for c in cen.CENARIOS_DE_LOCALIZADOR:
        q = cen.quebra(c["cenario"], c["modo"])
        seletor = lbm.SELETOR_DO_ENSAIO[c["id"]]
        assert seletor != q["localizador"], f"{c['id']}: o seletor do ensaio é o que a quebra derruba"
        assert f"python linha_de_base_manual.py conferir --cenario {c['id']}" in comandos
        assert any(x.startswith(f"python linha_de_base_manual.py conferir --cenario {c['id']} --seletor ") and seletor in x for x in comandos), c["id"]
    # os comandos da versão 2 são ensaiados numa pasta de teste: todo comando que grava leva --registro com ela, e a planilha é uma cópia
    assert lbm.PASTA_DO_ENSAIO == "fase5_manual_ensaio" and lbm.PASTA_DO_ENSAIO != lbm.PASTA_DA_SESSAO
    for x in comandos:
        if any(f" {c} " in x + " " for c in ("perfil", "treino", "entregar", "planilha")) or " --vez " in x:
            assert f"--registro {lbm.PASTA_DO_ENSAIO}" in x, f"comando do ensaio que gravaria na sessão de verdade: {x}"
    assert any(" planilha " in x + " " and "--planilha " in x for x in comandos), "a planilha do ensaio é uma cópia"
    for comando in ("perfil", "treino contrato", "treino seletor", "armar --vez", "entregar --vez", "conferir --vez", "planilha", "desarmar"):
        assert any(f"python linha_de_base_manual.py {comando}" in x for x in comandos), comando
    # as vezes do ensaio são uma de contrato e uma de localizador do integrante 1, tiradas do sorteio
    vezes = {tuple(int(n) for n in x.split(" --vez ")[1].split()[:2]) for x in comandos if " --vez " in x}
    assert sorted(lbm.vez_do_cenario(*v)["tipo"] for v in vezes) == ["contrato", "localizador"] and all(v[0] == 1 for v in vezes)
    assert "sem cronômetro" in texto and "RESULTADOS_DIR" in texto and "python run.py" in texto and "apagar" in texto.lower()
    for marca in ("—", "→", "↔"):
        assert marca not in texto
    with _ambiente() as amb:
        assert _rodar("ensaio") == 0 and amb.saida.getvalue().strip() == texto.strip()


# ! Alteração de IA - Revisar: (16/11/2026, F2) teste de ponta a ponta com o pacote F1: uma sessão inteira (os três integrantes nos
# dez cenários) gravada pelos eventos do ajudante e passada para a planilha pelo `preencher_planilha` tem de ser aceita, sem
# nenhuma recusa, pela leitura da Fase 5 (`avaliar_fase5.conferir_planilha`, do pacote F1).
# ! Motivo: os dois pacotes foram escritos em sessões diferentes, a partir de um contrato combinado por nota: o formato das horas,
# a vírgula decimal, o seletor escrito igual ao do registro, a linha sem fim de quem estourou o limite e a marca da linha anotada
# à mão. Se um dos lados mudar o formato, as 30 linhas das sessões de verdade seriam recusadas só no dia da leitura.
def teste_sessao_inteira_gravada_pelo_ajudante_e_aceita_pela_leitura_da_fase_5():
    import avaliar_fase5 as a5
    catalogo = {c["id"]: c for c in cen.CENARIOS_DO_ENSAIO}
    com_aspas = 'input[placeholder="Buscar; produtos"]'
    a_mao = (3, _posicao(3, "localizador-front-busca"))
    eventos, esperado_sem_fim = [], 0
    manha = time.mktime((2026, 11, 19, 9, 0, 0, 0, 0, -1))          # as 30 vezes cabem no mesmo dia: a planilha só guarda a hora
    for n, ids in lbm.ordem_dos_integrantes().items():
        for p, cid in enumerate(ids, 1):
            t0, c = manha + ((n - 1) * 10 + p - 1) * 900.25, catalogo[cid]
            if (n, p) == a_mao:
                continue                                            # a ferramenta falhou neste cenário: não há evento nenhum
            if c["tipo"] == "localizador":
                seletor = com_aspas if (n, cid) == (1, "localizador-front-busca") else "#certo"
                eventos += _localizador(n, p, [(50.25, "#errado", False, 1.5), (120.75, seletor, True, 2.25)], t0=t0)
            elif (n, cid) == (1, "contrato-error_500"):
                eventos += _contrato(n, p, 80.5, "corpo_vazio", None, t0=t0)                     # resposta errada
            elif (n, cid) == (2, "contrato-error_500"):
                eventos += _contrato(n, p, 601.0, c["causa"], c["campo"], t0=t0)                 # entregou depois do limite
                esperado_sem_fim += 1
            elif (n, cid) == (3, "contrato-error_500"):
                vez = lbm.vez_do_cenario(n, p)
                eventos += [lbm.montar_evento("inicio", vez, t0), lbm.montar_evento("fim_do_armar", vez, t0 + 650)]   # não entregou
                esperado_sem_fim += 1
            else:
                eventos += _contrato(n, p, 80.5, c["causa"], c["campo"], t0=t0)
    planilha = lbm.planilha_modelo(lbm.ordem_dos_integrantes())
    vazia = f"{a_mao[0]};{a_mao[1]};localizador-front-busca;localizador;;;;;;;;;;"
    assert vazia in planilha
    planilha = planilha.replace(vazia, vazia[:-10] + f";14:00:00;14:03:10;188,5;1,5;;;#do-papel;1;sim;{lbm.MARCA_A_MAO}")
    novo, preenchidas, avisos = lbm.preencher_planilha(planilha, lbm.resumo_do_registro(eventos))
    assert avisos == [] and len(preenchidas) == 29
    assert _linha(novo, 1, _posicao(1, "localizador-front-busca"))["seletor"] == com_aspas, "o seletor vai para a planilha como está no registro, com as aspas"
    pasta = _tmp()
    (pasta / "planilha.csv").write_text(novo, encoding="utf-8-sig")
    with open(pasta / "sessao.jsonl", "w", encoding="utf-8", newline="\n") as f:
        f.writelines(json.dumps(e, ensure_ascii=False) + "\n" for e in eventos)
    lido = a5.conferir_planilha(a5.ler_planilha_do_arquivo(pasta / "planilha.csv"), a5.ler_sessao(pasta / "sessao.jsonl"))
    assert lido["recusas"] == [], "a leitura da Fase 5 recusou linha gravada pelo ajudante:\n  " + "\n  ".join(lido["recusas"])
    assert len(lido["medidas"]) == 30 and lido["linhas"]["preenchidas"] == 30 and lido["linhas"]["anuladas"] == []
    assert [(x["integrante"], x["ordem"]) for x in lido["linhas"]["anotadas_a_mao"]] == [a_mao]
    assert len(lido["linhas"]["sem_fim"]) == esperado_sem_fim == 2


# ! Alteração de IA - Revisar: (16/11/2026, decisão 136) testes da sessão pelo artefato publicado, no lugar do teste do tutorial
# presencial da decisão 135: o tutorial reescrito para a página (tutorial_do_integrante.py), o material capturado nesta máquina
# (resultados_alvo/fase5_material/material.json), a página de cada integrante (sessao_pelo_artefato.pagina_da_sessao) e a
# importação da sessão que a página grava para o registro da sessão.
# ! Motivo: o Eric decidiu que a sessão é feita pela página publicada, com tudo o que precisa rodar já rodado aqui. A página é o
# que a pessoa lê e onde ela é medida: se ela trouxer o nome de um cenário ou a resposta esperada, a medida não vale; se a ordem
# não for a do sorteio, a planilha não casa; e se o registro importado sair diferente do que os comandos presenciais gravam, a
# leitura da Fase 5 recusa as linhas no dia da leitura.
def _das_cobaias() -> set:
    return (set(cen.PAGINA_DA_QUEBRA.values()) | {lbm.TREINO_DE_SELETOR["pagina"]} | {"EXCLUIR", "Reservar", "Saiba Mais", "Picanha", "churrasc",
                                                                                  "Eric", "Leandro", "Pedro", "Guilherme"})


def teste_tutorial_do_integrante_explica_a_sessao_pela_pagina_sem_entregar_resposta():
    import tutorial_do_integrante as tut
    md = tut.em_markdown()
    em_html = __import__("html").unescape(tut.secoes_em_html())
    dos_cenarios = {c["causa"] for c in cen.CENARIOS_DO_ENSAIO} | {lbm.TREINO_DE_CONTRATO["causa"]}
    seletores_das_cobaias = set(lbm.SELETOR_DO_ENSAIO.values()) | {q["localizador"] for q in cen.QUEBRAS} | {q["seletor_original"] for q in cen.QUEBRAS}
    for texto, onde in ((md, "o tutorial em Markdown"), (em_html, "o tutorial na página")):
        _sem_o_que_entrega_a_resposta(texto, onde)
        for proibido in sorted(_das_cobaias() | seletores_das_cobaias):
            assert proibido not in texto, f"{onde} traz {proibido!r}, que é das cobaias ou de uma pessoa"
        # os combinados de antes e o que a sessão é
        for trecho in ("repositório", "painel", "README", "documento do TCC", "assistente de IA", "avise o facilitador", "computador",
                       f"{len(cen.CENARIOS_DO_ENSAIO)} cenários", f"{lbm.LIMITE_S // 60} minutos", "sem cronômetro", "nenhum", "Abrir o cenário", "Testar seletor"):
            assert trecho in texto, f"{onde} não fala de {trecho!r}"
        for rotulo, minutos in lbm.MINUTOS_DA_SESSAO.items():
            assert f"{minutos} min" in texto, f"{onde} não diz os {minutos} minutos de {rotulo}"
        # o que pode, o que não pode e os avisos são os que a página usa
        assert lbm.PODE_NA_PAGINA in texto and lbm.NAO_PODE_NA_PAGINA in texto
        for aviso in lbm.AVISOS_DA_PAGINA.values():
            assert aviso in texto, f"{onde} não traz o aviso {aviso!r}"
        for classe in taxonomia.CLASSES.values():
            assert classe["pergunta"] in texto, f"{onde} não traz a pergunta {classe['pergunta']!r}"
        for causa, definicao in lbm.DEFINICAO_DAS_CAUSAS.items():
            assert causa in texto and definicao in texto, f"{onde} não traz a causa {causa}"
        assert tut.DOCUMENTACAO["seletores_css"] in texto
        # a parte do botão: o que já rodou antes, o que acontece depois do clique e o que fica guardado
        for trecho in ("Começar", "já rodou", "três perguntas", "treino", "código da sessão", "volta de onde você parou"):
            assert trecho in texto, f"{onde} não explica o botão: falta {trecho!r}"
    # a sessão pela página não tem facilitador ao lado nem navegador do cenário: o tutorial não manda abrir ferramenta nenhuma
    assert "F12" not in md and "bloco de notas" not in md and "Playwright" not in md
    assert list(lbm.AVISOS_DA_PAGINA) == ["dois_minutos", "esgotado", "nao_passou", "passou"]
    assert lbm.AVISOS_DA_PAGINA["dois_minutos"] == lbm.FALAS_DO_PLANO[1] and lbm.AVISOS_DA_PAGINA["esgotado"] == lbm.FALAS_DA_FERRAMENTA[3]
    # o exemplo resolvido é de uma causa que não é resposta de nenhum cenário nem do treino
    assert tut.CAUSA_DO_EXEMPLO in taxonomia.CAUSAS_RAIZ and tut.CAUSA_DO_EXEMPLO not in dos_cenarios
    assert f"causa: {tut.CAUSA_DO_EXEMPLO}" in md and md.count("causa: ") == 1, "só um exemplo de resposta de contrato"
    # os minutos do dia são os do plano aprovado (seção 4.3), e o teto da sessão sai deles e do limite
    plano = (RAIZ / "claude-memoria" / "plano-aprovado-fase-5.md").read_text(encoding="utf-8")
    m = lbm.MINUTOS_DA_SESSAO
    assert f"**Abertura ({m['abertura']} min).**" in plano and f"**Treino, sem cronômetro ({m['treino']} min;" in plano and f"**Fecho ({m['fecho']} min).**" in plano
    teto = sum(m.values()) + len(cen.CENARIOS_DO_ENSAIO) * lbm.LIMITE_S // 60
    assert tut.teto_da_sessao() == f"{teto // 60}h{teto % 60:02d}" and tut.teto_da_sessao() in md
    # o Markdown é documento derivado, gravado igual ao que o código gera; o botão só existe na página
    assert md.startswith("<!-- ! Alteração de IA - Revisar: documento DERIVADO") and "! Motivo" in md.split("-->")[0]
    assert tut.secoes()[-1]["id"] == "comecar" and 'id="comecar"' in tut.secoes_em_html() and 'id="comecar"' not in md
    assert all(re.fullmatch(r"[a-z][a-z0-9-]*", s["id"]) for s in tut.secoes()) and len({s["id"] for s in tut.secoes()}) == len(tut.secoes())
    assert tut.conferir() == [], "o tutorial gravado está diferente do que o código gera: rode `python linha_de_base_manual.py tutorial --gravar`"
    with _ambiente() as amb:
        assert _rodar("tutorial", "--check") == 0
        assert _rodar("tutorial") == 0 and md.strip() in amb.saida.getvalue()


def teste_material_capturado_tem_os_dez_cenarios_e_o_treino_conferidos():
    import executar_bateria
    import executar_fase4 as ex
    import sessao_pelo_artefato as spa
    m = spa.ler_material()
    da_21d = executar_bateria.ler_jsonl(RA / "fase4_ensaio_v4" / "cenarios.jsonl")
    da_21 = executar_bateria.ler_jsonl(RA / lbm.SAIDA_DO_ENSAIO / "cenarios.jsonl")
    # o mesmo navegador e o mesmo banco do ensaio vigente do agente
    assert m["navegador"] == da_21d[0]["navegador"] and m["hash_do_banco"] == da_21d[0]["hash_inicio"], (m["navegador"], m["hash_do_banco"])
    assert m["versao"] == spa.VERSAO_DO_MATERIAL and m["forma_da_quebra"] == "php" and m["contrato"] == ex._contrato_do_produto()
    assert "de IA - Revisar" in m["tag_ia"]["alteracao"] and m["tag_ia"]["motivo"].startswith("! Motivo")
    assert list(m["cenarios"]) == [c["id"] for c in cen.CENARIOS_DO_ENSAIO]

    # ! Alteração de IA - Revisar: (17/11/2026) o roteiro do material é comparado com o de hoje sem a data que o passo da reserva preenche.
    # ! Motivo: o roteiro `localizador-front-cliente-reserva` preenche `#data_pedido` com uma data contada a partir do dia em que
    # roda. O material foi capturado em 16/11/2026 e guarda '2026-11-19'; em 17/11 o mesmo roteiro diz '2026-11-20', e o teste
    # falhava com `AssertionError: localizador-front-cliente-reserva` sem que nada tivesse mudado. O material é o registro do
    # que rodou no dia da captura, então a data dele fica como está: o que o teste confere é que os passos são os mesmos.
    def sem_a_data(passos: list[str]) -> list[str]:
        return [re.sub(r"\d{4}-\d\d-\d\d", "<data>", p) for p in passos]

    for c in cen.CENARIOS_DO_ENSAIO:
        x = m["cenarios"][c["id"]]
        assert x["tipo"] == c["tipo"] and x["ficha"] == lbm.ficha_da_falha(c["id"], da_21) and sem_a_data(x["roteiro"]) == sem_a_data(lbm.passos_do_roteiro(c["id"])), c["id"]
        assert len(x["tela"]) > 10000, f"{c['id']}: sem a foto da tela"
        if c["tipo"] == "contrato":
            ch = x["chamada"]
            assert ch["metodo"] == "GET" and ch["caminho"] == "/api/produtos" and isinstance(ch["status"], int) and ch["tempo_ms"] > 0 and ch["corpo"], c["id"]
            assert "html" not in x and "alvo" not in x
        else:
            q = cen.quebra(c["cenario"], c["modo"])
            assert x["passo"] == q["passo_alvo"] + 1 and x["alvo"] and all(isinstance(i, int) for i in x["alvo"]), c["id"]
            assert x["conferido"]["o_caminho_leva_ao_alvo"] is True and x["conferido"]["o_seletor_que_conserta_acha_o_alvo_primeiro"] is True, c["id"]
            assert not x["conferido"]["quantos_o_localizador_quebrado_acha"], f"{c['id']}: o localizador quebrado ainda acha elemento na fotografia"
            assert x["fonte"].strip() and "<script" not in x["html"].lower() and "<!--" not in x["html"] and "chamada" not in x
            assert "data-alvo-da-captura" not in x["html"], "a marca usada na captura não pode ficar no HTML que a pessoa lê"
    # o treino: o cenário de contrato do treino (a resposta chega certa, com atraso) e o exercício de seletor sem falha
    t = m["treino"]
    assert (t["contrato"]["causa"], t["contrato"]["campo"]) == (lbm.TREINO_DE_CONTRATO["causa"], lbm.TREINO_DE_CONTRATO["campo"])
    assert t["contrato"]["ficha"] == lbm.ficha_do_treino() and t["contrato"]["chamada"]["status"] == 200 and t["contrato"]["chamada"]["tempo_ms"] > ex.ORCAMENTO_DE_TEMPO_MS
    assert t["seletor"]["conferido"]["o_caminho_leva_ao_alvo"] is True and t["seletor"]["alvo"] and lbm.TREINO_DE_SELETOR["alvo"]["nome"] in t["seletor"]["alvo_em_palavras"]
    # o comando não captura de novo por cima do material gravado, e nem sem as cobaias
    with _ambiente() as amb:
        assert _rodar("material") == 2 and "--regravar" in amb.saida.getvalue() and amb.chamadas == []


def teste_pagina_da_sessao_traz_o_tutorial_o_comecar_e_os_dez_cenarios_sem_entregar_resposta():
    import sessao_pelo_artefato as spa
    import tutorial_do_integrante as tut
    material = spa.ler_material()
    ids = {c["id"] for c in cen.CENARIOS_DO_ENSAIO}
    tipo = {c["id"]: c["tipo"] for c in cen.CENARIOS_DO_ENSAIO}
    for n in range(1, lbm.INTEGRANTES + 1):
        pagina = spa.pagina_da_sessao(n, material)
        assert pagina.startswith(f"<title>Sessão do integrante {n}</title>\n") and '<meta name="claude:viewport-fit-sides" content="cover">' in pagina[:300]
        assert "de IA - Revisar" in pagina[:1500] and "! Motivo" in pagina[:1500] and len(pagina.encode("utf-8")) < 8 * 1024 * 1024
        assert not re.search(r"<(!doctype|html|head|body|iframe)\b|@import|window\.print|\bsrc=\"http", pagina.lower()), "esqueleto próprio, moldura ou script de fora"
        assert pagina.count("<script>") == 2 and pagina.count("</script>") == 2, "dois blocos de script: os dados e o programa da página"
        for trecho in (":root {", "@media (prefers-color-scheme: dark)", ':root:not([data-theme="light"])', ':root[data-theme="dark"]', "color-scheme: dark",
                       "padding-left: max(16px, env(safe-area-inset-left, 0px))", "padding-right: max(16px, env(safe-area-inset-right, 0px))", "overflow-x: auto"):
            assert trecho in pagina, f"a página não tem {trecho!r}"
        estilo = pagina.split("<style>")[1].split("</style>")[0]
        assert not re.search(r"#[0-9a-fA-F]{3,8}\b|rgba?\(|hsla?\(", re.sub(r":root[^{]*\{[^}]*\}", "", estilo)), "cor escrita fora dos tokens do :root"
        enderecos = set(re.findall(r'href="([^"]+)"', pagina))
        assert all(e.startswith("#") or e.startswith("https://fonts.googleapis.com/") or e in tut.DOCUMENTACAO.values() for e in enderecos), sorted(enderecos)
        # os dados da sessão vão embutidos em base64: a ordem é a do sorteio deste integrante, pela posição, sem o nome do cenário
        dados = spa.dados_embutidos(pagina)
        assert dados == spa.dados_da_pagina(n, material) and dados["integrante"] == n and dados["formato"] == spa.FORMATO_DA_SESSAO == 3
        assert (dados["limite_s"], dados["aviso_s"]) == (lbm.LIMITE_S, lbm.AVISO_FINAL_S) and dados["avisos"] == lbm.AVISOS_DA_PAGINA
        assert dados["causas"] == [[c, d] for c, d in lbm.DEFINICAO_DAS_CAUSAS.items()] and dados["contrato"] == material["contrato"]
        assert dados["perguntas"] == lbm.PERGUNTAS_DE_PERFIL
        ordem = lbm.ordem_dos_integrantes()[n]
        assert [v["ordem"] for v in dados["vezes"]] == list(range(1, len(ordem) + 1)) and [v["tipo"] for v in dados["vezes"]] == [tipo[c] for c in ordem]
        for v, cid in zip(dados["vezes"], ordem):
            x = material["cenarios"][cid]
            assert v["ficha"] == x["ficha"] and v["roteiro"] == x["roteiro"] and v["tela"] == x["tela"], f"integrante {n}, posição {v['ordem']}"
            if v["tipo"] == "contrato":
                assert set(v) == {"ordem", "tipo", "ficha", "roteiro", "tela", "chamada"} and v["chamada"] == x["chamada"]
            else:
                assert set(v) == {"ordem", "tipo", "ficha", "roteiro", "tela", "passo", "fonte", "html", "alvo"} and v["alvo"] == x["alvo"] and v["html"] == x["html"]
        # só o treino leva a resposta certa; nos dez cenários ela não está em lugar nenhum da página
        assert dados["treino"]["contrato"]["causa"] == lbm.TREINO_DE_CONTRATO["causa"]
        das_vezes = json.dumps(dados["vezes"], ensure_ascii=False)
        for cid in ids:
            assert cid not in das_vezes and cid not in pagina, f"a página do integrante {n} traz o nome do cenário {cid}"
        # fora do material embutido, a página não traz nada das cobaias nem do que entrega a resposta
        visivel = __import__("html").unescape(pagina.replace(spa.blob_da_pagina(pagina), ""))
        _sem_o_que_entrega_a_resposta(visivel, f"a página do integrante {n}")
        for proibido in sorted(_das_cobaias() | set(lbm.SELETOR_DO_ENSAIO.values()) - {"button[type=submit]"}):
            assert proibido not in visivel, f"a página do integrante {n} traz {proibido!r} fora do material"
        for causa in {c["causa"] for c in cen.CENARIOS_DO_ENSAIO} - {"localizador_quebrado"}:
            assert visivel.count(causa) == 1, f"{causa} aparece fora da lista das 23 causas"
        # o tutorial inteiro, o botão no fim dele e o que o programa da página usa para guardar a sessão
        for s in tut.secoes():
            assert f'id="{s["id"]}"' in pagina
        assert pagina.index('id="tutorial"') < pagina.index('id="comecar"') < pagina.index('id="sessao"')
        for trecho in ('claude.use("db")', 'claude.use("user")', '"sessoes/integrante-"', spa.PREFIXO_DO_CODIGO, "localStorage", "Abrir o cenário", "Encerrar sem resposta",
                       "DOMParser", "querySelectorAll"):
            assert trecho in pagina, f"a página não tem {trecho!r}"
        assert "eval(" not in pagina and "innerHTML = vez.html" not in pagina, "o HTML capturado nunca entra na página viva"
        # as telas da sessão não repetem o id de uma seção do tutorial nem os da página (o programa acha cada elemento pelo id)
        dos_blocos = set(re.findall(r'id="([a-z0-9-]+)"', pagina.split("<script>")[0]))
        das_telas = set(re.findall(r'id="([a-z0-9-]+)"', spa.PROGRAMA))
        assert not dos_blocos & das_telas, f"id repetido entre a página e as telas da sessão: {sorted(dos_blocos & das_telas)}"
    # as três páginas gravadas são as que o código gera
    assert sorted(a.name for a in spa.ARQUIVOS_DAS_PAGINAS.values()) == [f"sessao-integrante-{n}.html" for n in (1, 2, 3)]
    assert spa.conferir_paginas() == [], "as páginas gravadas estão diferentes do que o código gera: rode `python linha_de_base_manual.py paginas --gravar`"
    with _ambiente():
        assert _rodar("paginas", "--check") == 0


def _sessao_da_pagina(n: int, base: float, seletor_certo: str = "#certo") -> dict:
    """Uma sessão inteira como a página do integrante `n` a grava: os dez cenários na ordem do sorteio, com um contrato errado,
    um entregue depois de encerrado por falta de resposta e, nos de localizador, uma tentativa errada e uma certa."""
    tipo = {c["id"]: c for c in cen.CENARIOS_DO_ENSAIO}
    eventos = []
    for p, cid in enumerate(lbm.ordem_dos_integrantes()[n], 1):
        t0, c = base + (p - 1) * 900.5, tipo[cid]
        eventos.append({"evento": "inicio", "ordem": p, "relogio_s": t0})
        if c["tipo"] == "localizador":
            eventos += [{"evento": "tentativa", "ordem": p, "relogio_s": t0 + 50.25, "seletor": "#errado", "corrigido": False, "motivo": "o primeiro elemento achado não é o do passo"},
                        {"evento": "tentativa", "ordem": p, "relogio_s": t0 + 120.75, "seletor": seletor_certo, "corrigido": True, "motivo": None},
                        {"evento": "fim_do_armar", "ordem": p, "relogio_s": t0 + 120.75, "motivo": "passou"}]
        elif cid == "contrato-error_500":
            eventos.append({"evento": "fim_do_armar", "ordem": p, "relogio_s": t0 + 600.0, "motivo": "limite"})
        else:
            causa = "corpo_vazio" if cid == "contrato-type_drift" else c["causa"]
            eventos += [{"evento": "entrega", "ordem": p, "relogio_s": t0 + 80.5}, {"evento": "resposta", "ordem": p, "relogio_s": t0 + 80.5, "causa": causa, "campo": c["campo"] or ""},
                        {"evento": "fim_do_armar", "ordem": p, "relogio_s": t0 + 80.5, "motivo": "entrega"}]
    return {"formato": 3, "integrante": n, "etapa": "fim", "ordem": 10, "navegador": "Mozilla/5.0 (teste)",
            "perfil": {"pratica": "um ano de programação para a web", "ja_usou_as_ferramentas_do_desenvolvedor": True, "ja_leu_a_lista_dos_cenarios": False},
            "treino": {"contrato": {"causa": lbm.TREINO_DE_CONTRATO["causa"], "campo": None, "acertou": True, "relogio_s": base - 600},
                       "seletor": {"seletor": ".um-seletor", "achou": True, "relogio_s": base - 300}},
            "eventos": eventos}


def teste_importar_traz_a_sessao_da_pagina_para_o_registro_no_formato_dos_comandos():
    import avaliar_fase5 as a5
    import sessao_pelo_artefato as spa
    manha = time.mktime((2026, 11, 19, 8, 0, 0, 0, 0, -1))
    pasta = _tmp()
    registro = lbm.arquivo_do_registro(pasta)
    conferidos = []

    def roteiro_de_verdade(cenario_id: str, seletor: str) -> bool:
        conferidos.append((cenario_id, seletor))
        return not (cenario_id == "localizador-front-busca" and seletor == "#so-na-pagina")

    # as três sessões entram, uma por integrante; a do integrante 3 tem um seletor que passou na página e não passa no roteiro de verdade
    for n in (1, 2, 3):
        sessao = _sessao_da_pagina(n, manha + (n - 1) * 10000, "#so-na-pagina" if n == 3 else "#certo")
        avisos = spa.importar_sessao(sessao, registro, conferir_seletor=roteiro_de_verdade)["avisos"]
        assert (len(avisos) == 1 and "não passou no roteiro" in avisos[0]) if n == 3 else avisos == [], avisos
    eventos = lbm.ler_registro(registro)
    assert {e["integrante"] for e in eventos} == {1, 2, 3} and all(e["registro"] == lbm.VERSAO_DO_REGISTRO and e["origem"] == "artefato" for e in eventos)
    # o cenário e o tipo vêm do sorteio, pela posição; a hora é refeita do relógio, no fuso desta máquina
    for e in eventos:
        if e["evento"] != "treino":
            assert e["cenario"] == lbm.cenario_da_vez(e["integrante"], e["ordem"]) and e["hora"] == lbm.hora_do_relogio(e["relogio_s"])
    assert sum(e["evento"] == "treino" for e in eventos) == 6 and {e["parte"] for e in eventos if e["evento"] == "treino"} == {"contrato", "seletor"}
    um_inicio = next(e for e in eventos if e["evento"] == "inicio")
    assert um_inicio["navegador"] == "Mozilla/5.0 (teste)" and um_inicio["segundos_do_banco"] == 0.0
    # o roteiro de verdade só é rodado com o seletor que passou na página, uma vez por cenário de localizador
    assert len(conferidos) == 12 and all(s in ("#certo", "#so-na-pagina") for _, s in conferidos)
    resumo = lbm.resumo_do_registro(eventos)
    assert len(resumo) == 30 and all(r["fechado"] for r in resumo.values())
    p = lbm.ordem_dos_integrantes()[1].index("contrato-field_missing") + 1
    assert (resumo[(1, p)]["segundos"], resumo[(1, p)]["causa"], resumo[(1, p)]["campo"], resumo[(1, p)]["corrigido"]) == (80.5, "campo_ausente", "preco", True)
    p = lbm.ordem_dos_integrantes()[1].index("contrato-type_drift") + 1
    assert resumo[(1, p)]["corrigido"] is False and resumo[(1, p)]["causa"] == "corpo_vazio"
    p = lbm.ordem_dos_integrantes()[1].index("contrato-error_500") + 1
    assert (resumo[(1, p)]["fim"], resumo[(1, p)]["corrigido"], resumo[(1, p)]["fechado"]) == (None, False, True)
    p = lbm.ordem_dos_integrantes()[1].index("localizador-front-busca") + 1
    assert (resumo[(1, p)]["segundos"], resumo[(1, p)]["descontar_s"], resumo[(1, p)]["tentativas"], resumo[(1, p)]["seletor"], resumo[(1, p)]["corrigido"]) == (120.75, 0.0, 2, "#certo", True)
    p = lbm.ordem_dos_integrantes()[3].index("localizador-front-busca") + 1
    assert resumo[(3, p)]["corrigido"] is False and resumo[(3, p)]["fim"] is None, "o que vale é o roteiro de verdade, rodado aqui"
    recusada = next(e for e in eventos if e["evento"] == "tentativa" and e["integrante"] == 3 and e["seletor"] == "#so-na-pagina" and e["cenario"] == "localizador-front-busca")
    assert recusada["passou_na_pagina"] is True and recusada["conferido_no_roteiro"] is False and recusada["corrigido"] is False and "roteiro" in recusada["motivo"]
    # a planilha preenchida por esse registro é aceita inteira pela leitura da Fase 5
    novo, preenchidas, avisos = lbm.preencher_planilha(lbm.planilha_modelo(lbm.ordem_dos_integrantes()), resumo)
    assert avisos == [] and len(preenchidas) == 30
    (pasta / "planilha.csv").write_text(novo, encoding="utf-8-sig")
    lido = a5.conferir_planilha(a5.ler_planilha_do_arquivo(pasta / "planilha.csv"), a5.ler_sessao(registro))
    assert lido["recusas"] == [] and len(lido["medidas"]) == 30, "\n  ".join(lido["recusas"])
    # a mesma sessão não entra duas vezes, e sessão malformada não entra
    antes = registro.read_text(encoding="utf-8")
    boa = _sessao_da_pagina(1, manha)
    ruins = [boa, {**_sessao_da_pagina(2, manha), "formato": 2}, {**_sessao_da_pagina(2, manha), "integrante": 4}]
    pc = lbm.ordem_dos_integrantes()[2].index("contrato-field_missing") + 1
    pl = lbm.ordem_dos_integrantes()[2].index("localizador-front-busca") + 1
    for troca in ({"evento": "tentativa", "ordem": pc, "relogio_s": manha, "seletor": "#x", "corrigido": True},
                  {"evento": "resposta", "ordem": pl, "relogio_s": manha, "causa": "campo_ausente", "campo": ""},
                  {"evento": "resposta", "ordem": pc, "relogio_s": manha, "causa": "type_drift", "campo": ""},
                  {"evento": "inventado", "ordem": pc, "relogio_s": manha},
                  {"evento": "inicio", "ordem": 11, "relogio_s": manha},
                  {"evento": "inicio", "ordem": pc, "relogio_s": "ontem"}):
        s = _sessao_da_pagina(2, manha)
        s["eventos"].append(troca)
        ruins.append(s)
    for ruim in ruins:
        try:
            spa.importar_sessao(ruim, lbm.arquivo_do_registro(_tmp()) if ruim is not boa else registro)
        except ValueError:
            pass
        else:
            raise AssertionError(f"sessão aceita: {str(ruim)[:120]}")
    assert registro.read_text(encoding="utf-8") == antes
    # o código da sessão que a página mostra no fim volta a ser a sessão, e o perfil dela passa pelo conferidor do perfil
    codigo = spa.PREFIXO_DO_CODIGO + __import__("base64").b64encode(json.dumps(boa, ensure_ascii=False).encode("utf-8")).decode("ascii")
    assert spa.ler_codigo(codigo) == boa and spa.ler_codigo("  " + codigo + "\n") == boa and spa.ler_codigo(json.dumps(boa)) == boa
    for ruim in ("", "SESSAO3.isto-nao-e-base64", "outra coisa"):
        try:
            spa.ler_codigo(ruim)
        except ValueError:
            pass
        else:
            raise AssertionError(f"código aceito: {ruim!r}")
    perfil = spa.perfil_da_sessao(boa, conhece_o_codigo=True, o_que_conhece="o HTML do site legado")
    assert lbm.perfil_do_integrante(perfil) == perfil and perfil["pratica"] == "um ano de programação para a web" and perfil["conhece_o_codigo_das_cobaias"] is True
    # o comando: lê o arquivo (o código ou o JSON), grava o registro e o perfil; a segunda vez é recusada
    with _ambiente() as amb:
        arq = amb.pasta / "sessao_1.txt"
        arq.write_text(codigo, encoding="utf-8")
        linha = ("importar", "--arquivo", str(arq), "--conhece-o-codigo", "nao", "--sem-conferir", "--registro", str(amb.pasta))
        assert _rodar(*linha) == 0
        assert len(lbm.resumo_do_registro(lbm.ler_registro(lbm.arquivo_do_registro(amb.pasta)))) == 10
        gravado = json.loads(lbm.arquivo_dos_participantes(amb.pasta).read_text(encoding="utf-8"))["integrantes"]["1"]
        assert gravado["conhece_o_codigo_das_cobaias"] is False and gravado["ja_usou_as_ferramentas_do_desenvolvedor"] is True
        assert "sem conferir" in amb.saida.getvalue().lower() and amb.chamadas == []
        assert _rodar(*linha) == 2


# ! Alteração de IA - Revisar: (17/11/2026, ficha 77, decisão 137) testes do aviso do integrante. A página pergunta, no fim de cada
# cenário, se alguma coisa de fora atrapalhou; o aviso vem no registro da sessão; e a importação só grava a sessão depois de o
# facilitador dizer, pelo motivo escrito, quais avisos anulam a linha. A planilha recebe o aviso nas observações, com `ANULADA`
# no começo quando ele anulou.
# ! Motivo: a regra L14 do plano da Fase 5 só anula a medida de um cenário por falha do protocolo anotada na hora, antes de
# qualquer número ser lido. Na sessão pela página não há facilitador ao lado para anotar: quem escreve na hora é a própria
# pessoa, e a decisão de anular tem de ficar gravada antes de os tempos aparecerem, senão a linha poderia ser tirada depois de
# vista. Sem o aviso, o cenário em que o computador travou entraria na conta como demora da pessoa.
def _sessao_com_avisos(n: int, base: float, avisos: dict[int, str]) -> dict:
    """A sessão da página do integrante `n` com um aviso escrito no fim de cada posição de `avisos`, antes de abrir a seguinte."""
    sessao = _sessao_da_pagina(n, base)
    eventos = []
    for e in sessao["eventos"]:
        eventos.append(e)
        if e["evento"] == "fim_do_armar" and e["ordem"] in avisos:
            eventos.append({"evento": "ocorrencia", "ordem": e["ordem"], "relogio_s": e["relogio_s"] + 12.5, "texto": avisos[e["ordem"]]})
    return {**sessao, "eventos": eventos}


def teste_pagina_pergunta_no_fim_de_cada_cenario_se_algo_de_fora_atrapalhou():
    import sessao_pelo_artefato as spa
    import tutorial_do_integrante as tut
    material = spa.ler_material()
    for n in range(1, lbm.INTEGRANTES + 1):
        dados = spa.dados_embutidos(spa.pagina_da_sessao(n, material))
        assert dados["ocorrencia"] == {"pergunta": lbm.PERGUNTA_DA_OCORRENCIA, "conta": lbm.O_QUE_CONTA_COMO_OCORRENCIA,
                                       "nao_conta": lbm.O_QUE_NAO_CONTA_COMO_OCORRENCIA, "limite": lbm.LIMITE_DA_OCORRENCIA}
    assert lbm.PERGUNTA_DA_OCORRENCIA.endswith("?") and lbm.LIMITE_DA_OCORRENCIA == 300
    # a pergunta fica na tela do cenário fechado, com o tempo parado, antes do botão que leva ao próximo; o aviso é gravado como
    # evento, com a hora, no clique nesse botão, e só quando a pessoa escreveu alguma coisa
    programa = spa.PROGRAMA
    for trecho in ('evento("ocorrencia"', 'id="ocorrencia"', "D.ocorrencia.pergunta", "D.ocorrencia.conta", "D.ocorrencia.nao_conta", "D.ocorrencia.limite"):
        assert trecho in programa, f"o programa da página não tem {trecho!r}"
    assert programa.index("if (s.fechado)") < programa.index('id="ocorrencia"') < programa.index('"Próximo cenário"')
    # os endereços já foram mandados aos integrantes: o formato da sessão e o prefixo do código não mudam
    assert spa.FORMATO_DA_SESSAO == 3 and spa.PREFIXO_DO_CODIGO == "SESSAO3."
    # o tutorial diz a pergunta, o que conta e o que não conta
    md = tut.em_markdown()
    for trecho in (lbm.PERGUNTA_DA_OCORRENCIA, lbm.O_QUE_CONTA_COMO_OCORRENCIA, lbm.O_QUE_NAO_CONTA_COMO_OCORRENCIA):
        assert trecho in md, f"o tutorial não diz {trecho!r}"
    for texto in (lbm.PERGUNTA_DA_OCORRENCIA, lbm.O_QUE_CONTA_COMO_OCORRENCIA, lbm.O_QUE_NAO_CONTA_COMO_OCORRENCIA):
        _sem_o_que_entrega_a_resposta(texto, "o texto do aviso")
    assert tut.conferir() == [] and spa.conferir_paginas() == [], "tutorial ou páginas gravadas diferentes do que o código gera"


def teste_importar_leva_o_aviso_do_integrante_e_a_anulacao_decidida_antes_dos_tempos():
    import base64
    import csv
    import io

    import avaliar_fase5 as a5
    import sessao_pelo_artefato as spa
    assert lbm.MARCA_ANULADA == a5.MARCA_ANULADA
    manha = time.mktime((2026, 11, 19, 8, 0, 0, 0, 0, -1))
    ordem = lbm.ordem_dos_integrantes()[2]
    pc, pl = ordem.index("contrato-field_missing") + 1, ordem.index("localizador-front-busca") + 1
    sem_aviso = next(p for p in range(1, len(ordem) + 1) if p not in (pc, pl))
    sessao = _sessao_com_avisos(2, manha + 10000, {pc: "o navegador   travou;\n fechei e abri de novo " + "x" * 400, pl: "  alguém me chamou na porta  "})
    # o texto do aviso é limpo antes de ir para o registro: espaços e quebras viram um espaço, o ponto e vírgula (o separador
    # da planilha) vira vírgula, e o tamanho fica no limite da página
    textos = dict(spa.ocorrencias_da_sessao(sessao))
    assert sorted(textos) == sorted((pc, pl)) and textos[pl] == "alguém me chamou na porta"
    assert textos[pc].startswith("o navegador travou, fechei e abri de novo x") and len(textos[pc]) == lbm.LIMITE_DA_OCORRENCIA and ";" not in textos[pc]
    assert spa.ocorrencias_da_sessao(_sessao_da_pagina(1, manha)) == []
    pasta = _tmp()
    registro = lbm.arquivo_do_registro(pasta)

    def recusada(s: dict, **mais) -> str:
        try:
            spa.importar_sessao(s, registro if s is sessao else lbm.arquivo_do_registro(_tmp()), **mais)
        except ValueError as e:
            return str(e)
        raise AssertionError(f"sessão aceita: {str(s)[:120]}")

    # sem a decisão do facilitador sobre os avisos a sessão não entra; anular uma posição sem aviso escrito na hora também não
    assert "anular" in recusada(sessao) and "sem aviso" in recusada(sessao, anular={sem_aviso}) and not registro.exists()
    assert "sem aviso" in recusada(_sessao_da_pagina(1, manha), anular={1})
    # aviso malformado não entra
    for ruim in ({"evento": "ocorrencia", "ordem": pc, "relogio_s": manha}, {"evento": "ocorrencia", "ordem": pc, "relogio_s": manha, "texto": "   "},
                 {"evento": "ocorrencia", "ordem": pc, "relogio_s": manha, "texto": 7}, {"evento": "ocorrencia", "ordem": 11, "relogio_s": manha, "texto": "x"},
                 {"evento": "ocorrencia", "ordem": pc, "relogio_s": "ontem", "texto": "x"}):
        s = _sessao_da_pagina(1, manha)
        s["eventos"].append(ruim)
        recusada(s, anular=set())
    # as três sessões entram; na do integrante 2 o facilitador anula a linha do contrato e mantém a do localizador
    for n in (1, 2, 3):
        spa.importar_sessao(sessao if n == 2 else _sessao_da_pagina(n, manha + (n - 1) * 10000), registro, conferir_seletor=lambda c, s: True,
                            anular={pc} if n == 2 else None)
    eventos = lbm.ler_registro(registro)
    avisos = {e["ordem"]: e for e in eventos if e["evento"] == "ocorrencia"}
    assert sorted(avisos) == sorted((pc, pl)) and all(e["integrante"] == 2 and e["origem"] == "artefato" and e["registro"] == lbm.VERSAO_DO_REGISTRO for e in avisos.values())
    assert (avisos[pc]["texto"], avisos[pc]["anulada"], avisos[pc]["cenario"]) == (textos[pc], True, "contrato-field_missing")
    assert (avisos[pl]["texto"], avisos[pl]["anulada"], avisos[pl]["cenario"]) == (textos[pl], False, "localizador-front-busca")
    for e in avisos.values():
        assert e["hora"] == lbm.hora_do_relogio(e["relogio_s"]) and re.fullmatch(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d\.\d{3}", e["decidida_em"]), e
    # o resumo de cada vez passa a dizer o aviso e se a linha foi anulada; o tempo e a resposta do cenário não mudam
    resumo = lbm.resumo_do_registro(eventos)
    assert len(resumo) == 30 and all(r["fechado"] for r in resumo.values())
    assert (resumo[(2, pc)]["ocorrencia"], resumo[(2, pc)]["anulada"], resumo[(2, pc)]["segundos"]) == (textos[pc], True, 80.5)
    assert (resumo[(2, pl)]["ocorrencia"], resumo[(2, pl)]["anulada"], resumo[(2, pl)]["segundos"]) == (textos[pl], False, 120.75)
    assert all(r["ocorrencia"] is None and r["anulada"] is False for vez, r in resumo.items() if vez not in ((2, pc), (2, pl)))
    # a planilha recebe o aviso nas observações: com ANULADA no começo quando o facilitador anulou, sem ela quando manteve
    modelo = lbm.planilha_modelo(lbm.ordem_dos_integrantes())
    novo, preenchidas, avisos_da_planilha = lbm.preencher_planilha(modelo, resumo)
    assert avisos_da_planilha == [] and len(preenchidas) == 30
    linhas = {(int(x["integrante"]), int(x["ordem"])): x for x in csv.DictReader(io.StringIO(novo), delimiter=lbm.SEPARADOR)}
    obs_c, obs_l = linhas[(2, pc)]["observacoes"], linhas[(2, pl)]["observacoes"]
    assert obs_c.startswith(lbm.MARCA_ANULADA) and "aviso do integrante" in obs_c and textos[pc] in obs_c
    assert not obs_l.upper().startswith(lbm.MARCA_ANULADA) and "aviso do integrante" in obs_l and textos[pl] in obs_l
    assert all(not x["observacoes"] for vez, x in linhas.items() if vez not in ((2, pc), (2, pl)))
    assert lbm.preencher_planilha(novo, resumo) == (novo, [], []), "rodar o comando de novo não muda nada nem avisa"
    # a leitura da Fase 5 conta a linha anulada à parte e mede as outras
    (pasta / "planilha.csv").write_text(novo, encoding="utf-8-sig")
    lido = a5.conferir_planilha(a5.ler_planilha_do_arquivo(pasta / "planilha.csv"), a5.ler_sessao(registro))
    assert lido["recusas"] == [] and len(lido["medidas"]) == 29, "\n  ".join(lido["recusas"])
    assert [(q["integrante"], q["ordem"]) for q in lido["linhas"]["anuladas"]] == [(2, pc)]
    # observação que o facilitador já escreveu não é trocada: o comando avisa
    cabecalho = modelo.split("\n")[0].split(lbm.SEPARADOR)
    mexidas = modelo.split("\n")
    for i, bruta in enumerate(mexidas[1:], 1):
        celulas = bruta.split(lbm.SEPARADOR) + [""] * len(cabecalho)
        if (celulas[cabecalho.index("integrante")], celulas[cabecalho.index("ordem")]) == ("2", str(pl)):
            celulas[cabecalho.index("observacoes")] = "o facilitador escreveu outra coisa"
            mexidas[i] = lbm.SEPARADOR.join(celulas[:len(cabecalho)])
    outro, _, avisos_da_planilha = lbm.preencher_planilha("\n".join(mexidas), resumo)
    assert "o facilitador escreveu outra coisa" in outro and textos[pl] not in outro
    assert len(avisos_da_planilha) == 1 and f"integrante 2, ordem {pl}" in avisos_da_planilha[0] and "aviso" in avisos_da_planilha[0]
    # o comando: sem --anular ele só mostra os avisos (a posição e o texto, nenhum tempo) e não grava nada
    codigo = spa.PREFIXO_DO_CODIGO + base64.b64encode(json.dumps(sessao, ensure_ascii=False).encode("utf-8")).decode("ascii")
    with _ambiente() as amb:
        arq = amb.pasta / "sessao_2.txt"
        arq.write_text(codigo, encoding="utf-8")
        linha = ("importar", "--arquivo", str(arq), "--conhece-o-codigo", "nao", "--sem-conferir", "--registro", str(amb.pasta))
        assert _rodar(*linha) == 2
        saida = amb.saida.getvalue()
        assert "--anular" in saida and f"posição {pc}" in saida and f"posição {pl}" in saida and textos[pc] in saida and textos[pl] in saida
        assert "segundos" not in saida and not re.search(r"\d\d:\d\d:\d\d", saida), "nenhum tempo aparece antes da decisão"
        assert _rodar(*linha, "--anular", "abc") == 2 and _rodar(*linha, "--anular", str(sem_aviso)) == 2
        assert not lbm.arquivo_do_registro(amb.pasta).exists() and not lbm.arquivo_dos_participantes(amb.pasta).exists()
        assert _rodar(*linha, "--anular", str(pc)) == 0
        gravados = {e["ordem"]: e["anulada"] for e in lbm.ler_registro(lbm.arquivo_do_registro(amb.pasta)) if e["evento"] == "ocorrencia"}
        assert gravados == {pc: True, pl: False}
    with _ambiente() as amb:
        arq = amb.pasta / "sessao_2.txt"
        arq.write_text(codigo, encoding="utf-8")
        assert _rodar("importar", "--arquivo", str(arq), "--conhece-o-codigo", "nao", "--sem-conferir", "--registro", str(amb.pasta), "--anular", "nenhum") == 0
        gravados = {e["ordem"]: e["anulada"] for e in lbm.ler_registro(lbm.arquivo_do_registro(amb.pasta)) if e["evento"] == "ocorrencia"}
        assert gravados == {pc: False, pl: False}


def teste_a_bateria_nao_escreve_na_pasta_da_sessao_de_verdade():
    agora = sorted((p.name, p.stat().st_size) for p in _SESSAO_DE_VERDADE.glob("*")) if _SESSAO_DE_VERDADE.exists() else None
    assert agora == _ANTES, f"resultados_alvo/fase5_manual mudou durante os testes: antes {_ANTES}, agora {agora}"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--todos", action="store_true", help="não para na primeira falha: roda todos e diz o motivo de cada uma (para ver os testes falharem antes do código)")
    args = ap.parse_args()
    modulo = sys.modules[__name__]
    testes = [(nome, obj) for nome, obj in vars(modulo).items()
              if nome.startswith("teste_") and inspect.isfunction(obj) and obj.__module__ == modulo.__name__]
    falhas = 0
    try:
        for nome, funcao in testes:
            try:
                funcao()
            except BaseException as e:  # o SystemExit do argparse também é falha do teste
                if isinstance(e, KeyboardInterrupt):
                    raise
                if not args.todos:
                    print(nome)
                    traceback.print_exc()
                    sys.exit(1)
                falhas += 1
                print(f"{nome} FALHOU: {type(e).__name__}: {' '.join(str(e).split())[:200]}")
                continue
            print(f"{nome} ok")
        if falhas:
            print(f"{falhas} de {len(testes)} testes falharam")
            sys.exit(1)
        print(f"{len(testes)} testes ok")
    finally:
        for caminho in _TEMPORARIOS:
            shutil.rmtree(caminho, ignore_errors=True)


if __name__ == "__main__":
    main()
