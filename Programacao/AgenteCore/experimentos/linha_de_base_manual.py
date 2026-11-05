#!/usr/bin/env python3
# ! Alteração de IA - Revisar: arquivo novo (04/11/2026, Fase 4, pacote P6): o ajudante da sessão cronometrada da linha de base
# manual da Fase 5 (protocolo em Documentacao/memorial/5-metodo-e-ferramental/protocolo-linha-de-base-manual.md), com quatro
# comandos: `ordem` sorteia com semente fixa a ordem dos dez cenários de cada integrante e grava a planilha modelo; `armar`
# restaura o banco, liga a falha do cenário da vez (o modo na CobaiaAPI, ou a quebra do localizador pelos cookies da variante
# PHP do front) e abre para o integrante o mesmo Chromium do agente, mostrando a ficha da falha que a corrida 21 gravou;
# `conferir` roda o roteiro de localizador com o seletor do integrante e diz se ele chegou ao fim sem erro; `desarmar` volta a
# CobaiaAPI ao modo normal. O facilitador chama o cenário pela vez (integrante e posição na ordem), e o nome do cenário, que diz
# o modo de falha, não aparece na tela.
# ! Motivo: a decisão 79 (ficha 36) pede a linha de base por três integrantes, cada um nos dez cenários, numa sessão agendada com
# o protocolo escrito. Para o tempo do integrante ser comparável ao MTTR do agente, a falha tem de ser ligada pelas mesmas funções
# da corrida (executar_fase4.ligar_modo e cenarios_fase4.armar_quebra), no mesmo navegador, e o "corrigido" do localizador tem de
# ser conferido pela mesma reexecução (cenarios_fase4.roteiro_com_seletor e task_success); feito à mão, cada um desses passos
# poderia sair diferente do que o agente teve.
"""Ajudante da sessão da linha de base manual (Fase 5). Na venv do AgenteCore, com RESULTADOS_DIR=resultados_alvo e as cobaias
no ar (`python run.py` na raiz do repositório, em outra janela):

  python linha_de_base_manual.py ordem --gravar
  python linha_de_base_manual.py armar --vez 1 3
  python linha_de_base_manual.py conferir --vez 1 3 --seletor "input[name=search]"
  python linha_de_base_manual.py desarmar

`--vez N P` é o cenário na posição P da ordem do integrante N (a planilha diz qual é); `--cenario <id>` serve para o ensaio do
facilitador. `conferir` sai 0 quando o roteiro chega ao fim sem erro com o seletor do integrante (corrigido) e 1 quando não."""
from __future__ import annotations

import argparse
import csv
import io
import random
import sys
import time
from pathlib import Path
from urllib.parse import urljoin

import cenarios_fase4 as cen

RAIZ = Path(__file__).resolve().parents[3]
SEMENTE_DA_ORDEM = 20261104
INTEGRANTES = 3
SAIDA_DO_ENSAIO = "fase4_ensaio"
PLANILHA = RAIZ / "Documentacao" / "memorial" / "5-metodo-e-ferramental" / "planilha-linha-de-base-manual.csv"
SEPARADOR = ";"   # o Excel em português abre o CSV separado por ponto e vírgula em colunas
COLUNAS_DA_PLANILHA = ("integrante", "ordem", "cenario", "tipo", "inicio", "fim", "segundos", "descontar_s", "causa", "campo",
                       "seletor", "tentativas", "corrigido", "observacoes")


def cenario_do_ensaio(cenario_id: str) -> dict:
    c = next((x for x in cen.CENARIOS_DO_ENSAIO if x["id"] == cenario_id), None)
    if c is None:
        raise ValueError(f"{cenario_id!r} não é um dos dez cenários do ensaio: use um de {[x['id'] for x in cen.CENARIOS_DO_ENSAIO]}")
    return c


def roteiro_do_integrante(cenario_id: str, seletor: str | None = None) -> tuple[dict, dict]:
    """O roteiro do cenário de localizador com o seletor do integrante no lugar do quebrado (sem seletor, o roteiro do agente,
    com o localizador quebrado) e a quebra do cenário."""
    c = cenario_do_ensaio(cenario_id)
    if c["tipo"] != "localizador":
        raise ValueError(f"{cenario_id!r} é de contrato: só os cenários de localizador têm seletor para conferir")
    q = cen.quebra(c["cenario"], c["modo"])
    base = cen.cenario_com_localizador(cen.cenario(c["cenario"]), q)
    return (cen.roteiro_com_seletor(base, q, seletor) if seletor else base), q


def ordem_dos_integrantes(integrantes: int = INTEGRANTES, semente: int = SEMENTE_DA_ORDEM) -> dict[int, list[str]]:
    """A ordem dos dez cenários de cada integrante, sorteada com a semente mais o número do integrante: o que um integrante
    aprende num cenário se espalha entre os cenários, e a mesma semente dá sempre a mesma ordem."""
    ordens = {}
    for n in range(1, integrantes + 1):
        ids = [c["id"] for c in cen.CENARIOS_DO_ENSAIO]
        random.Random(semente + n).shuffle(ids)
        ordens[n] = ids
    return ordens


def cenario_da_vez(integrante: int, posicao: int, semente: int = SEMENTE_DA_ORDEM) -> str:
    ordens = ordem_dos_integrantes(max(INTEGRANTES, integrante), semente)
    if integrante < 1 or not 1 <= posicao <= len(ordens[integrante]):
        raise ValueError(f"vez fora da planilha: integrante {integrante}, posição {posicao}")
    return ordens[integrante][posicao - 1]


def planilha_modelo(ordens: dict[int, list[str]]) -> str:
    """A planilha da sessão: uma linha por integrante e cenário, na ordem sorteada, com as colunas da medição em branco."""
    tipos = {c["id"]: c["tipo"] for c in cen.CENARIOS_DO_ENSAIO}
    saida = io.StringIO()
    w = csv.writer(saida, delimiter=SEPARADOR, lineterminator="\n")
    w.writerow(COLUNAS_DA_PLANILHA)
    for n, ids in sorted(ordens.items()):
        for i, cid in enumerate(ids, 1):
            w.writerow([n, i, cid, tipos[cid]] + [""] * (len(COLUNAS_DA_PLANILHA) - 4))
    return saida.getvalue()


def ficha_da_falha(cenario_id: str, registros: list[dict]) -> str | None:
    """O que a detecção acusou na primeira execução do cenário que detectou, como o ensaio gravou em cenarios.jsonl."""
    for r in sorted((r for r in registros if r.get("cenario") == cenario_id), key=lambda r: r.get("repeticao") or 0):
        if r.get("detectou") and r.get("motivo_deteccao"):
            return r["motivo_deteccao"]
    return None


def endereco_inicial(cenario_id: str) -> str:
    """O endereço do primeiro passo `abrir` do roteiro: o integrante começa por onde o roteiro começa."""
    c = cenario_do_ensaio(cenario_id)
    primeiro = next(p for p in cen.cenario(c["cenario"])["passos"] if p.get("acao") == "abrir")
    return urljoin(cen.BASE_PADRAO, primeiro["url"])


def passos_do_roteiro(cenario_id: str) -> list[str]:
    """Os passos do roteiro numerados, com o valor de cada preenchimento, e o passo do localizador quebrado marcado."""
    c = cenario_do_ensaio(cenario_id)
    if c["tipo"] == "localizador":
        roteiro, q = roteiro_do_integrante(cenario_id)
        alvo = q["passo_alvo"]
    else:
        roteiro, alvo = cen.cenario(c["cenario"]), None
    linhas = []
    for i, p in enumerate(roteiro["passos"]):
        texto = cen._descrever(p)
        if p.get("acao") == "preencher":
            texto += f" com {cen.valor_do_passo(p)!r}"
        if i == alvo:
            texto += " (o passo que quebrou: este localizador não acha mais o elemento)"
        linhas.append(f"{i + 1}. {texto}")
    return linhas


# ------------------------------------------------------------------ comandos (precisam das cobaias, do banco e do navegador)

def _registros_do_ensaio(saida: str) -> list[dict]:
    import caminhos
    import executar_bateria
    arq = caminhos.fase3(saida)["raiz"] / "cenarios.jsonl"
    return executar_bateria.ler_jsonl(arq) if arq.exists() else []


def _restaurar_banco() -> tuple[str, float]:
    sys.path.insert(0, str(RAIZ))
    import _env_common as env
    import restaurar_banco as rb
    cli = env.find_mysql_cli()
    t0 = time.monotonic()
    if rb.restaurar(cli) != rb.CONTAGENS_DO_SEED:
        raise SystemExit("!! o banco restaurado não tem as contagens do seed")
    return rb.hash_das_tabelas(cli), round(time.monotonic() - t0, 2)


def _cobaias_no_ar() -> bool:
    sys.path.insert(0, str(RAIZ))
    import run
    return run.wait_until_ready(timeout_s=5)


def _cenario_pedido(args: argparse.Namespace) -> tuple[str, str]:
    if args.vez:
        n, p = args.vez
        return cenario_da_vez(n, p), f"integrante {n}, cenário {p} de {len(cen.CENARIOS_DO_ENSAIO)}"
    cenario_do_ensaio(args.cenario)
    return args.cenario, args.cenario


def armar(args: argparse.Namespace) -> int:
    import executar_fase4 as ex
    import navegador
    import taxonomia
    cid, rotulo = _cenario_pedido(args)
    c = cenario_do_ensaio(cid)
    if not _cobaias_no_ar():
        print("!! as cobaias não responderam nas portas 8080 e 8000: suba com `python run.py` na raiz do repositório")
        return 2
    h, seg = _restaurar_banco()
    print(f"{rotulo}: banco restaurado e conferido (hash {h}, {seg} s)")
    if c["tipo"] == "contrato":
        ex.ligar_modo(c["modo"], c["campo"], args.token)
        print("falha ligada na CobaiaAPI para GET /api/produtos")
    ficha = ficha_da_falha(cid, _registros_do_ensaio(args.saida))
    print("\n== Ficha da falha (o que a detecção do agente acusou neste cenário na corrida 21)")
    print(ficha or f"(sem ficha: {args.saida}/cenarios.jsonl não tem este cenário; rode a corrida 21 antes da sessão)")
    print("\n== Roteiro do teste")
    print("\n".join(passos_do_roteiro(cid)))
    if c["tipo"] == "contrato":
        print("\n== Contrato esperado de cada produto em GET /api/produtos (o mesmo que o agente recebe)")
        print(ex._contrato_do_produto())
        print("\n== Resposta: uma causa desta lista e o campo afetado (ou nenhum)")
        print(", ".join(taxonomia.CAUSAS_RAIZ))
    else:
        print("\n== Resposta: um seletor (CSS ou do Playwright) que ache o elemento do passo que quebrou")
    with navegador.Navegador(canal=args.canal, headless=False) as nav:
        pagina = nav.nova_pagina()
        if c["tipo"] == "localizador":
            cen.armar_quebra(pagina, cen.quebra(c["cenario"], c["modo"]), args.forma)
        pagina.goto(endereco_inicial(cid))
        print(f"\nnavegador {nav.versao()['navegador']} aberto para o integrante; início do cronômetro: {time.strftime('%H:%M:%S')}")
        try:
            input("Enter fecha o navegador e desarma o cenário (F12 abre as ferramentas do desenvolvedor)... ")
        except EOFError:
            pass
    if c["tipo"] == "contrato":
        ex.ligar_modo("normal", None, args.token)
        print("CobaiaAPI de volta ao modo normal")
    return 0


def conferir(args: argparse.Namespace) -> int:
    import navegador
    cid, rotulo = _cenario_pedido(args)
    roteiro, q = roteiro_do_integrante(cid, args.seletor)
    if not _cobaias_no_ar():
        print("!! as cobaias não responderam nas portas 8080 e 8000: suba com `python run.py` na raiz do repositório")
        return 2
    _, seg_banco = _restaurar_banco()
    with navegador.Navegador(canal=args.canal) as nav:
        pagina = nav.nova_pagina()
        cen.armar_quebra(pagina, q, args.forma)
        r = cen.rodar_cenario(roteiro, pagina, None, capturar=False, tempo_limite_ms=cen.TEMPO_LIMITE_QUEBRA_MS)
        pagina.close()
    for conf in r["conferencias"]:
        print(f"  {'confere' if conf['passou'] else 'NÃO confere'}: {conf['nome']}")
    ok = cen.task_success(r)
    if not args.seletor:
        print(f"{rotulo}, com o localizador quebrado do roteiro: {cen.motivo_do_roteiro(r) or 'o roteiro passou (a quebra não foi armada?)'}")
        return 0 if not ok else 1
    if not ok:
        print(f"  {cen.motivo_do_roteiro(r)}")
    print(f"{rotulo} com o seletor {args.seletor!r}: {'CORRIGIDO (o roteiro chegou ao fim sem erro)' if ok else 'não corrigido'} às "
          f"{time.strftime('%H:%M:%S')}; roteiro em {r['segundos']} s; banco restaurado em {seg_banco} s antes do roteiro (descontar do cronômetro)")
    return 0 if ok else 1


def desarmar(args: argparse.Namespace) -> int:
    import executar_fase4 as ex
    ex.ligar_modo("normal", None, args.token)
    print("CobaiaAPI de volta ao modo normal; feche o navegador do integrante se ainda estiver aberto")
    return 0


def ordem(args: argparse.Namespace) -> int:
    ordens = ordem_dos_integrantes(args.integrantes, args.semente)
    for n, ids in ordens.items():
        print(f"integrante {n}: " + ", ".join(f"{i}. {cid}" for i, cid in enumerate(ids, 1)))
    if args.gravar:
        texto = planilha_modelo(ordens)
        destino = PLANILHA
        if destino.exists() and destino.read_text(encoding="utf-8-sig") != texto:
            destino = destino.with_suffix(".nova.csv")
            print(f"!! {PLANILHA.name} já tem anotações e foi mantida; a planilha em branco foi para {destino.name}")
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_text(texto, encoding="utf-8-sig")
        print(f"planilha gravada em {destino}")
    return 0


def montar_parser() -> argparse.ArgumentParser:
    import executar_fase4 as ex
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="comando", required=True)
    p = sub.add_parser("ordem", help="a ordem sorteada dos dez cenários de cada integrante")
    p.add_argument("--integrantes", type=int, default=INTEGRANTES)
    p.add_argument("--semente", type=int, default=SEMENTE_DA_ORDEM)
    p.add_argument("--gravar", action="store_true", help=f"grava a planilha modelo em {PLANILHA.name}")
    p.set_defaults(funcao=ordem)
    for nome, funcao, ajuda in (("armar", armar, "liga a falha do cenário e abre o navegador do integrante"),
                                ("conferir", conferir, "roda o roteiro de localizador com o seletor do integrante")):
        p = sub.add_parser(nome, help=ajuda)
        qual = p.add_mutually_exclusive_group(required=True)
        qual.add_argument("--vez", type=int, nargs=2, metavar=("INTEGRANTE", "POSICAO"), help="o cenário da vez, pela ordem sorteada")
        qual.add_argument("--cenario", help="o cenário pelo nome (ensaio do facilitador)")
        p.add_argument("--forma", choices=cen.FORMAS_DE_QUEBRA, default="php", help="como armar a quebra de localizador (padrão php)")
        p.add_argument("--canal", default="chromium")
        p.add_argument("--token", default=ex.TOKEN_PADRAO, help="X-Admin-Token da CobaiaAPI")
        p.add_argument("--saida", default=SAIDA_DO_ENSAIO, help="a corrida de onde sai a ficha da falha")
        if nome == "conferir":
            p.add_argument("--seletor", help="o seletor do integrante; sem ele, roda com o localizador quebrado e mostra a ficha da falha")
        p.set_defaults(funcao=funcao)
    p = sub.add_parser("desarmar", help="volta a CobaiaAPI ao modo normal")
    p.add_argument("--token", default=ex.TOKEN_PADRAO)
    p.set_defaults(funcao=desarmar)
    return ap


def main() -> int:
    args = montar_parser().parse_args()
    return args.funcao(args)


if __name__ == "__main__":
    sys.exit(main())
