#!/usr/bin/env python3
# ! Alteração de IA - Revisar: arquivo novo (05/11/2026, ficha 42, decisão 90): confere, sem modelo, o corte do caso ao vivo antes
# das corridas 18c e 21c. Sobe as cobaias, roda os 37 casos que reproduzem e os dez cenários do ensaio pelo mesmo caminho dos modos
# `tela` e `cenarios` (Tela.rodar_caso, Cura.executar), monta o prompt que cada um mandaria ao modelo e compara com o prompt guardado
# nas corridas 18b e 21b: quantos caracteres saíram, quantos tokens se estimam contra o limite do plano e quais verbetes a busca
# passou a trazer, separando o que o corte mudou (mesma biblioteca da corrida antiga) do que a biblioteca de produção mudou. Grava
# `resultados_alvo/fase4/corte_prompt_tela.json`. Não chama o Ollama.
# ! Motivo: a decisão 90 manda conferir sem modelo os prompts novos e os verbetes recuperados antes de ocupar a máquina por 1h47,
# porque a busca lê o SINTOMA e a OBSERVAÇÃO, e os dois mudaram. A medida de `medir_prompt_tela.py` lê só os prompts guardados: o
# corte de verdade depende da árvore completa da referência e da árvore da célula da cura, que só existem com a página aberta.
"""Conferência sem modelo do corte do caso ao vivo (decisão 90), nos casos das corridas 18b e 21b. Uso: conferir_corte_tela.py [--casos N]"""
from __future__ import annotations

import argparse
import json
import statistics
import sys
import time
from pathlib import Path

import biblioteca as bib
import caminhos
import cenarios_fase4 as cen
import diagnostico_ao_vivo as dv
import evolucao_biblioteca as evo
import executar_fase3
import executar_fase4 as ex
import medir_prompt_tela as mp
import navegador
import recuperacao as rec
import trilha as tr

ARQUIVO = "corte_prompt_tela.json"
K = 3  # regra R8, corrida 16


def linha_do_caso(caso: str, prompt_novo: str, ids_mesma_biblioteca: list[str], ids_producao: list[str], prompt_antigo: str, tokens_antigos: int, ids_antigos: list[str],
                  causa: str | None = None, ids_fixture: list[str] | None = None) -> dict:
    """Um caso: os tamanhos antes e depois, os tokens estimados pela razão de tokens por caractere do prompt guardado, o que mudou os
    verbetes e, com a `causa` do gabarito, se o verbete da causa certa estava entre os recuperados (o id do verbete é o nome da causa).
    `ids_fixture` são os verbetes que o caso escrito recupera na mesma biblioteca, a régua do que a busca alcança."""
    return {"caso": caso, "causa": causa, "ouro_fixture": causa in ids_fixture if causa and ids_fixture is not None else None, "verbetes_fixture": ids_fixture, "ouro_antes": causa in ids_antigos if causa else None, "ouro_mesma_biblioteca": causa in ids_mesma_biblioteca if causa else None,
            "ouro_producao": causa in ids_producao if causa else None, "chars_antes": len(prompt_antigo), "chars_depois": len(prompt_novo), "tokens_antes": tokens_antigos,
            "tokens_estimados": round(len(prompt_novo) * tokens_antigos / len(prompt_antigo)),
            "verbetes_antes": list(ids_antigos), "verbetes_mesma_biblioteca": list(ids_mesma_biblioteca), "verbetes_producao": list(ids_producao),
            "mudou_pelo_corte": list(ids_mesma_biblioteca) != list(ids_antigos), "mudou_pela_biblioteca": list(ids_producao) != list(ids_mesma_biblioteca)}


def resumir(linhas: list[dict], limite: int) -> dict:
    """O que a corrida repetida vai ler: casos acima do limite e casos cujos verbetes mudam, por cada motivo."""
    tokens = [x["tokens_estimados"] for x in linhas]
    return {"casos": len(linhas), "acima_do_limite": [x["caso"] for x in linhas if x["tokens_estimados"] > limite],
            "tokens": {"min": min(tokens), "mediana": statistics.median(tokens), "max": max(tokens)} if tokens else None,
            "mudou_pelo_corte": [x["caso"] for x in linhas if x["mudou_pelo_corte"]], "mudou_pela_biblioteca": [x["caso"] for x in linhas if x["mudou_pela_biblioteca"]],
            "ouro": {"antes": sum(1 for x in linhas if x.get("ouro_antes")), "mesma_biblioteca": sum(1 for x in linhas if x.get("ouro_mesma_biblioteca")),
                     "producao": sum(1 for x in linhas if x.get("ouro_producao")), "fixture": sum(1 for x in linhas if x.get("ouro_fixture"))},
            "perdeu_o_ouro_pelo_corte": [x["caso"] for x in linhas if x.get("ouro_antes") and not x.get("ouro_mesma_biblioteca")],
            "ganhou_o_ouro_pelo_corte": [x["caso"] for x in linhas if x.get("ouro_mesma_biblioteca") and not x.get("ouro_antes")],
            "perdeu_o_ouro_pela_biblioteca": [x["caso"] for x in linhas if x.get("ouro_mesma_biblioteca") and not x.get("ouro_producao")],
            "ganhou_o_ouro_pela_biblioteca": [x["caso"] for x in linhas if x.get("ouro_producao") and not x.get("ouro_mesma_biblioteca")]}


def verbetes_do_caso(guardados: dict[str, list[str]], caso: str) -> list[str]:
    """Os verbetes do prompt guardado do caso; na corrida 21b a trilha do cenário de contrato não leva o sufixo `@tela`."""
    return guardados.get(caso) or guardados.get(caso.split("@")[0]) or []


def _verbetes_guardados(raiz: Path, pasta: str, arq_trilha: str) -> dict[str, list[str]]:
    saida = {}
    for linha in (raiz / pasta / arq_trilha).read_text(encoding="utf-8").splitlines():
        r = json.loads(linha) if linha.strip() else {}
        if r.get("tipo") == "prompt" and r["dados"].get("etapa") == "diagnostico":
            saida[r["trilha"].split("/")[-1]] = r["dados"].get("verbetes_ids") or []
    return saida


def _guardados(raiz: Path, corrida: str) -> tuple[dict, dict]:
    pasta, arq_trilha, arq_diag = mp.CORRIDAS[corrida]
    registros, _ = mp._ler_corrida(raiz, pasta, arq_trilha, arq_diag)
    return {caso: (tokens, prompt) for caso, tokens, prompt in registros}, _verbetes_guardados(raiz, pasta, arq_trilha)


def _biblioteca(pasta: Path) -> tuple[list[dict], rec.Indice]:
    verbetes = bib.carregar(pasta)
    return verbetes, rec.Indice(verbetes)


def _pasta_da_biblioteca(raiz: Path, corrida: str) -> Path:
    slug = executar_fase3._slug("qwen2.5:7b")
    return min((raiz / mp.CORRIDAS[corrida][0] / "bibliotecas" / slug).glob("epoca-*"))


def conferir(caso: dict, guardados: tuple[dict, dict], antiga: tuple, producao: tuple, causa: str | None = None, fixture: dict | None = None) -> dict:
    """A linha do caso e o que o prompt novo leva, para ler sem abrir o navegador de novo."""
    prompts, verbetes = guardados
    tokens, prompt_antigo = prompts[caso["id"]]
    ctx_antiga, _ = dv.montar_prompt(antiga[0], antiga[1], caso, K)
    ctx_prod, prompt = dv.montar_prompt(producao[0], producao[1], caso, K)
    e = caso["entrada"]
    return {**linha_do_caso(caso["id"], prompt, ctx_antiga["verbetes_ids"], ctx_prod["verbetes_ids"], prompt_antigo, tokens, verbetes_do_caso(verbetes, caso["id"]), causa=causa,
                         ids_fixture=dv.montar_prompt(producao[0], producao[1], ex.fixture_sem_gabarito(fixture), K)[0]["verbetes_ids"] if fixture else None),
            "arvore": e.get("arvore"), "sintoma": e.get("sintoma"), "corpo": e.get("corpo")}


def main() -> int:
    import _env_common as env
    import restaurar_banco as rb
    import run

    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--casos", type=int, default=0, help="só os N primeiros casos de cada corrida (fumaça); não grava o arquivo")
    args = ap.parse_args()
    raiz = caminhos.RESULTADOS
    t0 = time.monotonic()
    limite = json.loads((raiz / "fase4" / mp.ARQUIVO).read_text(encoding="utf-8"))["limite"]["tokens"]
    producao = _biblioteca(dv.PASTA_CURADA)
    antigas = {c: _biblioteca(_pasta_da_biblioteca(raiz, c)) for c in mp.CORRIDAS}
    guardados = {c: _guardados(raiz, c) for c in mp.CORRIDAS}
    saida = caminhos.fase3("fase4_corte_conferencia")["raiz"]
    saida.mkdir(parents=True, exist_ok=True)
    marco = print
    contrato = ex._contrato_do_produto()
    reprodutiveis = set(ex.casos_que_reproduzem(json.loads((raiz / "fase4" / "reproducibilidade.json").read_text(encoding="utf-8"))))
    casos = ex.casos_de_avaliacao("avaliacao")
    gabarito = {c["id"]: c["gabarito"]["causa_raiz"] for c in casos}
    por_id = {c["id"]: c for c in casos}
    itens = [i for i in ex.selecionar_casos(casos)["reproduziveis"] if i["id"] in reprodutiveis]
    celulas = ex.celulas_do_ensaio(1)
    if args.casos:
        itens, celulas = itens[:args.casos], celulas[:args.casos] + celulas[-1:]
    token = ex.TOKEN_PADRAO
    front, api = run.start_services()
    linhas: dict[str, list[dict]] = {"18b": [], "21b": []}
    try:
        if not run.wait_until_ready(timeout_s=90):
            marco("!! as cobaias não responderam")
            return 2
        cli = env.find_mysql_cli()
        rb.restaurar(cli)
        trilha = tr.Trilha(versao=tr.V2, pasta_blobs=saida / "blobs")
        trilha.corrida(tr.cabecalho_de_corrida(modelo="(sem modelo: conferência do corte)", versao_ollama="não medida", inicio=cen.agora(), corrida="fase4_corte_conferencia",
                                               etapas_registradas=["roteiro", "interceptacao", "poda", "caso_ao_vivo"], etapas_nao_registradas=["diagnostico"],
                                               extras={"modo": "conferencia_do_corte", "hash_biblioteca": None}), ts=cen.agora())
        with navegador.Navegador(canal="chromium") as nav:
            tela = ex.Tela(nav, trilha, "fase4_corte_conferencia", contrato, token, marco)
            for cid in ("api-catalogo", "api-detalhe"):
                tela.referencia(cid, 1 if cid == "api-detalhe" else None)
            for n, item in enumerate(itens, 1):
                d = tela.rodar_caso(item)
                linhas["18b"].append(conferir(d["caso_vivo"], guardados["18b"], antigas["18b"], producao, causa=gabarito.get(item["id"]), fixture=por_id.get(item["id"])))
                marco(f"[18b {n}/{len(itens)}] {item['id']}: {linhas['18b'][-1]['tokens_antes']} para {linhas['18b'][-1]['tokens_estimados']} tokens")
            cura = ex.Cura(nav, trilha, "fase4_corte_conferencia", token, marco, cli)
            for n, cel in enumerate(celulas, 1):
                c = cel["cenario"]
                rb.restaurar(cli)
                if c["tipo"] == "contrato":
                    caso = tela.rodar_caso({**c, "id": cel["id"], "produto_id": None, "requisicao": "GET /api/produtos"})["caso_vivo"]
                else:
                    guardado: dict = {}

                    def apos_deteccao(d_: dict, c: dict = c, guardado: dict = guardado) -> dict:
                        guardado["caso"] = ex.caso_do_localizador(c, d_)
                        return {"rotulo": None, "p_rotulo": None}

                    cura.executar({"id": cel["id"], "cenario": c["cenario"], "modo": c["modo"], "forma": c["forma"], "repeticao": cel["repeticao"]}, apos_deteccao=apos_deteccao)
                    caso = guardado.get("caso")
                    if caso is None:
                        marco(f"!! {cel['id']}: a quebra não foi detectada; sem prompt para conferir")
                        continue
                linhas["21b"].append(conferir(caso, guardados["21b"], antigas["21b"], producao, causa=c.get("causa")))
                marco(f"[21b {n}/{len(celulas)}] {caso['id']}: {linhas['21b'][-1]['tokens_antes']} para {linhas['21b'][-1]['tokens_estimados']} tokens")
        rb.restaurar(cli)
    finally:
        ex.derrubar_cobaias(front, api, token)
    dado = {"o_que_e": "o prompt que as corridas 18c e 21c mandariam ao modelo, montado sem modelo com o corte da decisão 90 e comparado com o prompt guardado nas corridas 18b e 21b; "
                       "os tokens são estimados pela razão de tokens por caractere do prompt guardado de cada caso",
            "limite": limite, "gerado_em": cen.agora(), "biblioteca_de_producao": evo.hash_biblioteca(dv.PASTA_CURADA),
            "versao_do_caso_ao_vivo": ex.cv.VERSAO_DO_CASO, "duracao_s": round(time.monotonic() - t0),
            "corridas": {nome: {"resumo": resumir(v, limite), "linhas": v} for nome, v in linhas.items()}}
    for nome, c in dado["corridas"].items():
        print(f"{nome}: {c['resumo']}")
    if args.casos:
        print("fumaça: nada gravado")
        return 0
    arq = raiz / "fase4" / ARQUIVO
    arq.write_text(json.dumps(dado, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"gravado em {arq}; {dado['duracao_s']} s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
