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
import cliente_ollama as co
import diagnostico_ao_vivo as dv
import evolucao_biblioteca as evo
import executar_fase3
import executar_fase4 as ex
import medir_prompt_tela as mp
import navegador
import recuperacao as rec
import trilha as tr

# ! Alteração de IA - Revisar: (06/11/2026, decisão 97) a conferência passa a comparar com as corridas 18c e 21c e grava em outro arquivo.
# ! Motivo: os sinais novos mudam a busca, e o que precisa ser conferido agora é o efeito deles sobre a leitura vigente; `corte_prompt_tela.json` fica como o registro da conferência do corte, citado nos documentos.
# ! Alteração de IA - Revisar: (06/11/2026) a conferência passa a comparar com as corridas 18d, 18e e 21d, inclui os 25 inéditos que reproduzem na tela e diz se o prompt ficou igual, byte a byte; grava em outro arquivo.
# ! Motivo: o teto nas listas do caso ao vivo só pode valer sem corrida nova se os prompts das corridas 18d e 21d não mudarem, e isso precisa ser medido, não presumido; `busca_prompt_tela.json` fica como o registro da conferência dos sinais da busca, citado nos documentos.
ARQUIVO = "teto_prompt_tela.json"
CORRIDAS_DE_ANTES = {"18d": ("fase4_tela_v4", "trilha_tela.jsonl", "diagnosticos__tela.jsonl"), "18e": ("fase4_tela_ineditos", "trilha_tela.jsonl", "diagnosticos__tela.jsonl"),
                     "21d": ("fase4_ensaio_v4", "trilha_cenarios.jsonl", "diagnosticos__cenarios.jsonl")}
K = 3  # regra R8, corrida 16
PROMPTS_NOVOS: dict[str, str] = {}  # o prompt que cada caso mandaria, para a medida depois de as cobaias descerem


def linha_do_caso(caso: str, prompt_novo: str, ids_mesma_biblioteca: list[str], ids_producao: list[str], prompt_antigo: str, tokens_antigos: int, ids_antigos: list[str],
                  causa: str | None = None, ids_fixture: list[str] | None = None) -> dict:
    """Um caso: os tamanhos antes e depois, os tokens estimados pela razão de tokens por caractere do prompt guardado, o que mudou os
    verbetes e, com a `causa` do gabarito, se o verbete da causa certa estava entre os recuperados (o id do verbete é o nome da causa).
    `ids_fixture` são os verbetes que o caso escrito recupera na mesma biblioteca, a régua do que a busca alcança."""
    return {"caso": caso, "causa": causa, "prompt_igual": prompt_novo == prompt_antigo, "ouro_fixture": causa in ids_fixture if causa and ids_fixture is not None else None, "verbetes_fixture": ids_fixture, "ouro_antes": causa in ids_antigos if causa else None, "ouro_mesma_biblioteca": causa in ids_mesma_biblioteca if causa else None,
            "ouro_producao": causa in ids_producao if causa else None, "chars_antes": len(prompt_antigo), "chars_depois": len(prompt_novo), "tokens_antes": tokens_antigos,
            "tokens_estimados": round(len(prompt_novo) * tokens_antigos / len(prompt_antigo)),
            "verbetes_antes": list(ids_antigos), "verbetes_mesma_biblioteca": list(ids_mesma_biblioteca), "verbetes_producao": list(ids_producao),
            "mudou_pelo_corte": list(ids_mesma_biblioteca) != list(ids_antigos), "mudou_pela_biblioteca": list(ids_producao) != list(ids_mesma_biblioteca)}


# ! Alteração de IA - Revisar: (06/11/2026) a medida dos prompts que mudaram de tamanho, com o próprio Ollama: `keep_alive` 0 descarrega o modelo a cada chamada, para o cache de prefixo não esconder tokens, e `num_predict` 1 não gera resposta.
# ! Motivo: a estimativa pela razão de tokens por caractere exagerou em `semt-27`: disse 1447, e o medido foi 1367, porque o texto que saiu tinha mais tokens por caractere que o resto do prompt; o prompt guardado do mesmo caso mediu 1829, igual à corrida 18e.
def medir_tokens(prompt: str) -> int:
    corpo = {"model": "qwen2.5:7b", "prompt": prompt, "stream": False, "keep_alive": 0,
             "options": {"num_gpu": 0, "num_ctx": co.NUM_CTX, "temperature": co.TEMPERATURA, "num_predict": 1}}
    return co._post("/api/generate", corpo).get("prompt_eval_count", 0)


def medir_os_que_mudaram_de_tamanho(linhas: list[dict], prompts: dict[str, str]) -> None:
    for x in linhas:
        if x["chars_depois"] != x["chars_antes"]:
            x["tokens_medidos"] = medir_tokens(prompts[x["caso"]])


def resumir(linhas: list[dict], limite: int) -> dict:
    """O que a corrida repetida vai ler: casos acima do limite e casos cujos verbetes mudam, por cada motivo."""
    tokens = [x.get("tokens_medidos") or x["tokens_estimados"] for x in linhas]
    return {"casos": len(linhas), "acima_do_limite": [x["caso"] for x in linhas if (x.get("tokens_medidos") or x["tokens_estimados"]) > limite],
            "prompt_igual": sum(1 for x in linhas if x.get("prompt_igual")), "prompt_diferente": [x["caso"] for x in linhas if not x.get("prompt_igual")],
            "tokens": {"min": min(tokens), "mediana": statistics.median(tokens), "max": max(tokens)} if tokens else None,
            "mudou_pelo_corte": [x["caso"] for x in linhas if x["mudou_pelo_corte"]], "mudou_pela_biblioteca": [x["caso"] for x in linhas if x["mudou_pela_biblioteca"]],
            "ouro": {"antes": sum(1 for x in linhas if x.get("ouro_antes")), "mesma_biblioteca": sum(1 for x in linhas if x.get("ouro_mesma_biblioteca")),
                     "producao": sum(1 for x in linhas if x.get("ouro_producao")), "fixture": sum(1 for x in linhas if x.get("ouro_fixture"))},
            "perdeu_o_ouro_pelo_corte": [x["caso"] for x in linhas if x.get("ouro_antes") and not x.get("ouro_mesma_biblioteca")],
            "ganhou_o_ouro_pelo_corte": [x["caso"] for x in linhas if x.get("ouro_mesma_biblioteca") and not x.get("ouro_antes")],
            "perdeu_o_ouro_pela_biblioteca": [x["caso"] for x in linhas if x.get("ouro_mesma_biblioteca") and not x.get("ouro_producao")],
            "ganhou_o_ouro_pela_biblioteca": [x["caso"] for x in linhas if x.get("ouro_producao") and not x.get("ouro_mesma_biblioteca")]}


def verbetes_do_caso(guardados: dict[str, list[str]], caso: str) -> list[str]:
    """Os verbetes do prompt guardado do caso; na trilha dos cenários o id não leva o sufixo `@tela` nem `@cenario` e, no localizador, leva o número da repetição."""
    # ! Alteração de IA - Revisar: (06/11/2026) acha também o id `localizador-z#1` da trilha a partir do id `localizador-z@cenario` do caso.
    # ! Motivo: sem isto, os quatro cenários de localizador vinham sem verbetes guardados, e a conferência dizia que o verbete certo tinha acabado de chegar neles: o "de 1 para 9" da conferência do corte era, nos registros, de 5 para 9.
    base = caso.split("@")[0]
    return guardados.get(caso) or guardados.get(base) or next((v for k, v in guardados.items() if k.split("#")[0] == base), [])


def _verbetes_guardados(raiz: Path, pasta: str, arq_trilha: str) -> dict[str, list[str]]:
    saida = {}
    for linha in (raiz / pasta / arq_trilha).read_text(encoding="utf-8").splitlines():
        r = json.loads(linha) if linha.strip() else {}
        if r.get("tipo") == "prompt" and r["dados"].get("etapa") == "diagnostico":
            saida[r["trilha"].split("/")[-1]] = r["dados"].get("verbetes_ids") or []
    return saida


def _guardados(raiz: Path, corrida: str) -> tuple[dict, dict]:
    pasta, arq_trilha, arq_diag = CORRIDAS_DE_ANTES[corrida]
    registros, _ = mp._ler_corrida(raiz, pasta, arq_trilha, arq_diag)
    return {caso: (tokens, prompt) for caso, tokens, prompt in registros}, _verbetes_guardados(raiz, pasta, arq_trilha)


def _biblioteca(pasta: Path) -> tuple[list[dict], rec.Indice]:
    verbetes = bib.carregar(pasta)
    return verbetes, rec.Indice(verbetes)


def _pasta_da_biblioteca(raiz: Path, corrida: str) -> Path:
    slug = executar_fase3._slug("qwen2.5:7b")
    return min((raiz / CORRIDAS_DE_ANTES[corrida][0] / "bibliotecas" / slug).glob("epoca-*"))


def conferir(caso: dict, guardados: tuple[dict, dict], antiga: tuple, producao: tuple, causa: str | None = None, fixture: dict | None = None) -> dict:
    """A linha do caso e o que o prompt novo leva, para ler sem abrir o navegador de novo."""
    prompts, verbetes = guardados
    tokens, prompt_antigo = prompts[caso["id"]]
    ctx_antiga, _ = dv.montar_prompt(antiga[0], antiga[1], caso, K)
    ctx_prod, prompt = dv.montar_prompt(producao[0], producao[1], caso, K)
    PROMPTS_NOVOS[caso["id"]] = prompt
    e = caso["entrada"]
    return {**linha_do_caso(caso["id"], prompt, ctx_antiga["verbetes_ids"], ctx_prod["verbetes_ids"], prompt_antigo, tokens, verbetes_do_caso(verbetes, caso["id"]), causa=causa,
                         ids_fixture=dv.montar_prompt(producao[0], producao[1], ex.fixture_sem_gabarito(fixture), K)[0]["verbetes_ids"] if fixture else None),
            "arvore": e.get("arvore"), "sintoma": e.get("sintoma"), "corpo": e.get("corpo"), "sinais_da_busca": caso.get("sinais_da_busca")}


def main() -> int:
    import _env_common as env
    import restaurar_banco as rb
    import run

    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--casos", type=int, default=0, help="só os N primeiros casos de cada corrida (fumaça); não grava o arquivo")
    ap.add_argument("--medir-tokens", action="store_true", help="mede com o Ollama os prompts que mudaram de tamanho, cerca de 90 s por prompt")
    args = ap.parse_args()
    raiz = caminhos.RESULTADOS
    t0 = time.monotonic()
    limite = json.loads((raiz / "fase4" / mp.ARQUIVO).read_text(encoding="utf-8"))["limite"]["tokens"]
    producao = _biblioteca(dv.PASTA_CURADA)
    antigas = {c: _biblioteca(_pasta_da_biblioteca(raiz, c)) for c in CORRIDAS_DE_ANTES}
    guardados = {c: _guardados(raiz, c) for c in CORRIDAS_DE_ANTES}
    saida = caminhos.fase3("fase4_corte_conferencia")["raiz"]
    saida.mkdir(parents=True, exist_ok=True)
    marco = print
    contrato = ex._contrato_do_produto()

    def casos_do_banco(banco: str) -> tuple[list[dict], dict, dict]:
        casos, nome_rep = ex.casos_e_reproducao_da_tela(banco)
        ids = set(ex.casos_que_reproduzem(json.loads((raiz / "fase4" / nome_rep).read_text(encoding="utf-8"))))
        return [i for i in ex.selecionar_casos(casos)["reproduziveis"] if i["id"] in ids], {c["id"]: c["gabarito"]["causa_raiz"] for c in casos}, {c["id"]: c for c in casos}

    itens, gabarito, por_id = casos_do_banco("avaliacao")
    itens_ineditos, gabarito_ineditos, por_id_ineditos = casos_do_banco("ineditos_fase4")
    celulas = ex.celulas_do_ensaio(1)
    if args.casos:
        itens, itens_ineditos, celulas = itens[:args.casos], itens_ineditos[:args.casos], celulas[:args.casos] + celulas[-1:]
    token = ex.TOKEN_PADRAO
    front, api = run.start_services()
    linhas: dict[str, list[dict]] = {"18d": [], "18e": [], "21d": []}
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
                linhas["18d"].append(conferir(d["caso_vivo"], guardados["18d"], antigas["18d"], producao, causa=gabarito.get(item["id"]), fixture=por_id.get(item["id"])))
                marco(f"[18d {n}/{len(itens)}] {item['id']}: {linhas['18d'][-1]['tokens_antes']} para {linhas['18d'][-1]['tokens_estimados']} tokens")
            for n, item in enumerate(itens_ineditos, 1):
                d = tela.rodar_caso(item)
                linhas["18e"].append(conferir(d["caso_vivo"], guardados["18e"], antigas["18e"], producao, causa=gabarito_ineditos.get(item["id"]), fixture=por_id_ineditos.get(item["id"])))
                marco(f"[18e {n}/{len(itens_ineditos)}] {item['id']}: {linhas['18e'][-1]['tokens_antes']} para {linhas['18e'][-1]['tokens_estimados']} tokens")
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
                linhas["21d"].append(conferir(caso, guardados["21d"], antigas["21d"], producao, causa=c.get("causa")))
                marco(f"[21d {n}/{len(celulas)}] {caso['id']}: {linhas['21d'][-1]['tokens_antes']} para {linhas['21d'][-1]['tokens_estimados']} tokens")
        rb.restaurar(cli)
    finally:
        ex.derrubar_cobaias(front, api, token)
    if args.medir_tokens:
        for v in linhas.values():
            medir_os_que_mudaram_de_tamanho(v, PROMPTS_NOVOS)
    dado = {"o_que_e": "o prompt que o caso ao vivo com o teto nas listas mandaria ao modelo, montado sem modelo e comparado com o prompt guardado nas corridas 18d, 18e e 21d; "
                       "os tokens são estimados pela razão de tokens por caractere do prompt guardado de cada caso, e os prompts que mudaram de tamanho são medidos com o próprio Ollama (`tokens_medidos`)",
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
