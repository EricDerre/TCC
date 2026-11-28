#!/usr/bin/env python3
# ! Alteração de IA - Revisar: arquivo novo (27/11/2026): os testes da coletânea de erros sorteados para a banca (`coletanea.py`;
# plano aprovado em claude-memoria/plano-aprovado-coletanea-da-banca.md, decisões 193 a 197): as 64 cartas, o gabarito pelo modo, a
# prova de cada carta nos registros versionados, a pilha pelo número da banca, a posição seguinte lida de `sorteios.jsonl` e o
# comando que refaz o sorteio. Funções teste_<nome>(); main() roda todas e termina em "N testes ok". Sem modelo, sem cobaias, sem banco.
# ! Motivo: a coletânea é o que a banca vai ver como prova de que as rodadas não são casos fixos; se uma carta tiver o gabarito errado
# ou a prova faltando, ou se a pilha repetir um erro, o argumento cai na frente dela. Estes testes conferem isso sem rodar nada.
"""Testes da coletânea de erros sorteados para a banca (decisões 193 a 197)."""
from __future__ import annotations

import copy
import datetime as dt
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import traceback
from collections import Counter
from pathlib import Path

EXP = Path(__file__).resolve().parent
sys.path.insert(0, str(EXP))

import cenarios_fase4 as cen  # noqa: E402
import coletanea as cl  # noqa: E402


def _ids() -> list[str]:
    return [c["id"] for c in cl.cartas()]


def teste_sao_64_cartas_com_58_erros_e_6_sem_erro():
    c = cl.cartas()
    assert len(c) == 64, len(c)
    assert Counter(x["tipo"] for x in c) == {"contrato": 42, "localizador": 16, "sem_erro": 6}
    assert len(set(_ids())) == 64


def teste_a_conferencia_da_coletanea_sai_limpa():
    erros = cl.validar()
    assert erros == [], erros


def teste_o_gabarito_vem_do_modo():
    causa_do_modo = {m: c for c, m in cen.MODO_POR_CAUSA.items()}
    for x in cl.cartas():
        if x["tipo"] == "contrato":
            assert x["causa"] == causa_do_modo[x["modo"]], x["id"]
        elif x["tipo"] == "localizador":
            assert (x["causa"], x["classe"], x["forma"]) == ("localizador_quebrado", 6, "harness"), x["id"]
            assert x["modo"] in cen.MODOS_DE_QUEBRA and x["cenario"] in cen.ROTEIROS_DA_CURA, x["id"]
        else:
            assert (x["modo"], x["causa"], x["classe"], x["campo"]) == ("normal", None, None, None), x["id"]


def teste_as_classes_dos_erros_sao_as_contadas_no_plano():
    por_classe = Counter(x["classe"] for x in cl.cartas() if x["tipo"] != "sem_erro")
    assert por_classe == {1: 8, 2: 11, 3: 11, 4: 5, 5: 6, 6: 17}, por_classe


def teste_os_dez_da_medida_estao_marcados_e_sao_os_do_ensaio():
    medidas = [x for x in cl.cartas() if x["medido_na_fase_5"]]
    assert len(medidas) == 10
    do_ensaio = {(c["cenario"], c["modo"], c.get("campo")) for c in cen.CENARIOS_DO_ENSAIO}
    assert {(x["cenario"], x["modo"], x["campo"]) for x in medidas} == do_ensaio


def teste_a_pagina_do_detalhe_leva_o_produto_e_a_requisicao():
    for x in cl.cartas():
        if x["cenario"] == "api-detalhe":
            assert isinstance(x["produto_id"], int) and x["requisicao"] == f"GET /api/produtos/{x['produto_id']}", x["id"]
        elif x["cenario"] == "api-catalogo":
            assert x["produto_id"] is None and x["requisicao"] == "GET /api/produtos", x["id"]
        else:
            assert x["produto_id"] is None and x["requisicao"] is None, x["id"]


def teste_cada_carta_tem_a_descricao_em_palavras():
    for x in cl.cartas():
        d = cl.descricao(x)
        assert d and "None" not in d and "{" not in d, (x["id"], d)
    assert "preco" in cl.descricao(cl.carta("contrato/api-catalogo/field_missing/preco"))


def _com(cartas: list[dict], id_: str, **troca) -> list[dict]:
    novas = copy.deepcopy(cartas)
    for x in novas:
        if x["id"] == id_:
            x.update(troca)
    return novas


def teste_a_conferencia_recusa_carta_errada():
    base = cl.cartas()
    alvo = "contrato/api-catalogo/field_missing/preco"
    casos = {
        "modo": _com(base, alvo, modo="modo_que_nao_existe"),
        "causa": _com(base, alvo, causa="tipo_divergente"),
        "campo fora do contrato": _com(base, alvo, campo="preco_v9"),
        "prova": _com(base, alvo, prova=["fase4_reproducao", "sin-999"]),
        "classe": _com(base, alvo, classe=5),
        "campo na resposta inteira": _com(base, "contrato/api-catalogo/malformed_json", campo="preco"),
        "página": _com(base, "localizador/front-busca/id_renomeado", cenario="front-que-nao-existe"),
        "repetida": base + [copy.deepcopy(base[0])],
    }
    for nome, cartas in casos.items():
        erros = cl.validar(cartas)
        assert erros, f"{nome}: a conferência deixou passar"
    # o erro diz qual carta está errada
    assert any(alvo in e for e in cl.validar(casos["causa"]))


def teste_a_pilha_e_a_mesma_para_o_mesmo_numero_e_refeita_sem_o_modulo():
    a = cl.ordem_da_pilha("4821")
    assert a == cl.ordem_da_pilha("4821") and sorted(a) == sorted(_ids())
    assert a != cl.ordem_da_pilha("4822")
    # a mesma conta feita à mão, só com o SHA-256, como qualquer pessoa da banca poderia refazer
    assert a == sorted(_ids(), key=lambda i: hashlib.sha256(f"4821|{i}".encode("utf-8")).hexdigest())


def teste_tirar_da_pilha_nao_repete_ate_ela_acabar():
    pos, vistas, ultima = 0, [], None
    while True:
        ultima = cl.tirar("77", pos, 10)
        vistas += ultima["cartas"]
        pos = ultima["proxima"]
        if ultima["acabou"]:
            break
    assert len(vistas) == 64 and sorted(vistas) == sorted(_ids())
    assert len(ultima["cartas"]) == 4 and ultima["proxima"] == 64 and ultima["total"] == 64
    try:
        cl.tirar("77", 64, 5)
    except ValueError as e:
        assert "acabou" in str(e)
    else:
        raise AssertionError("tirar com a pilha vazia deveria recusar")


def teste_o_numero_da_banca_e_so_de_algarismos():
    assert cl.normalizar_numero(" 4821 ") == "4821" and cl.normalizar_numero("0") == "0"
    for ruim in ("", "48a1", "-3", "1" * 19, "4 821", None):
        try:
            cl.normalizar_numero(ruim)
        except ValueError:
            continue
        raise AssertionError(f"{ruim!r} deveria ser recusado")
    assert cl.numero_do_relogio(dt.datetime(2026, 12, 4, 19, 30, 5)) == "20261204193005"


def teste_a_posicao_seguinte_sai_do_registro_dos_sorteios():
    with tempfile.TemporaryDirectory() as t:
        reg = Path(t) / "hub" / cl.ARQUIVO_DOS_SORTEIOS
        assert cl.proxima_posicao("4821", reg) == 0
        s1 = cl.sortear("4821", 5, reg, "hub_20261204_193000", "digitado", quando="2026-12-04T19:30:00")
        cl.gravar_sorteio(s1, Path(t) / "hub_20261204_193000", reg)
        assert cl.proxima_posicao("4821", reg) == 5 and cl.proxima_posicao("9", reg) == 0
        s2 = cl.sortear("4821", 3, reg, "hub_20261204_194000", "digitado")
        assert s2["posicao"] == 5 and s2["cartas"] == cl.ordem_da_pilha("4821")[5:8]
        # uma linha de outra coletânea (outro código) não mexe na pilha desta
        with reg.open("a", encoding="utf-8") as f:
            f.write(json.dumps({**s1, "codigo_da_coletanea": "outro", "posicao": 40, "proxima": 45}) + "\n")
        assert cl.proxima_posicao("4821", reg) == 5


def teste_o_sorteio_gravado_tem_o_que_refaz_a_lista():
    with tempfile.TemporaryDirectory() as t:
        reg, pasta = Path(t) / "sorteios.jsonl", Path(t) / "hub_x"
        s = cl.sortear("4821", 5, reg, "hub_x", "digitado", quando="2026-12-04T19:30:00")
        assert {"quando", "corrida", "numero", "origem", "codigo_da_coletanea", "posicao", "quantas", "cartas", "proxima", "total", "acabou",
                "comando"} <= set(s)
        assert s["codigo_da_coletanea"] == cl.hash_da_coletanea() and s["cartas"] == cl.ordem_da_pilha("4821")[:5]
        assert s["comando"] == cl.comando_que_refaz("4821", 5, 0)
        arq = cl.gravar_sorteio(s, pasta, reg)
        assert json.loads(arq.read_text(encoding="utf-8")) == s
        assert json.loads(reg.read_text(encoding="utf-8").splitlines()[-1]) == s
        for ruim in ({"quantas": 4}, {"origem": "outra"}):
            try:
                cl.sortear(**{"numero": "1", "quantas": 5, "registro": reg, "corrida": "x", "origem": "digitado", **ruim})
            except ValueError:
                continue
            raise AssertionError(f"{ruim} deveria ser recusado")


def teste_o_comando_refaz_a_mesma_lista():
    env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
    r = subprocess.run([sys.executable, str(EXP / "coletanea.py"), "--sortear", "--numero", "4821", "--quantas", "5", "--posicao", "0"],
                       capture_output=True, text=True, encoding="utf-8", env=env, cwd=str(EXP))
    assert r.returncode == 0, r.stderr
    saida = r.stdout
    posicoes = [saida.index(i) for i in cl.ordem_da_pilha("4821")[:5]]
    assert posicoes == sorted(posicoes), saida
    assert cl.hash_da_coletanea() in saida


def teste_a_conferencia_pela_linha_de_comando():
    env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
    r = subprocess.run([sys.executable, str(EXP / "coletanea.py"), "--conferir"], capture_output=True, text=True, encoding="utf-8", env=env, cwd=str(EXP))
    assert r.returncode == 0 and "64 cartas" in r.stdout, (r.stdout, r.stderr)


def teste_o_codigo_da_coletanea_muda_quando_ela_muda():
    h = cl.hash_da_coletanea()
    assert len(h) == 64 and h == cl.hash_da_coletanea(cl.cartas())
    assert cl.hash_da_coletanea(_com(cl.cartas(), "sem-erro/api-catalogo", nivel=3)) != h


def teste_os_grupos_cobrem_todas_as_cartas():
    chaves = [g["classe"] for g in cl.GRUPOS]
    assert chaves == [1, 2, 3, 4, 5, 6, None]
    assert all(x["classe"] in chaves for x in cl.cartas())


def main() -> None:
    testes = [(n, f) for n, f in globals().items() if n.startswith("teste_") and callable(f)]
    falhas = 0
    for nome, f in testes:
        try:
            f()
        except Exception:  # noqa: BLE001 - o runner mostra a falha e segue
            falhas += 1
            print(f"FALHOU {nome}")
            traceback.print_exc()
    if falhas:
        print(f"{falhas} de {len(testes)} testes falharam")
        sys.exit(1)
    print(f"{len(testes)} testes ok")


if __name__ == "__main__":
    main()
