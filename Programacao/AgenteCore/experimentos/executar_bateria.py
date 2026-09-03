#!/usr/bin/env python3
# ! Alteração de IA - Revisar: executor da bateria — roda os casos de um modelo por vez,
# nas três estratégias, gravando cada resultado assim que termina.
# ! Motivo: são centenas de inferências em CPU, de horas de duração. Gravar em JSONL a cada
# caso é o que permite interromper e retomar sem repetir o que já rodou (uma execução que
# perdesse tudo ao ser interrompida seria inviável na prática). O descarregamento explícito
# entre modelos atende à exigência de não ter dois modelos disputando memória — sem isso, o
# Ollama mantém o anterior residente e as medições de memória e latência ficam contaminadas.
import argparse
import json
import time
from pathlib import Path

import biblioteca as bib
import cliente_ollama as oll
import recuperacao as rec
from banco_casos import CASOS
from banco_casos_extra import CASOS_EXTRA
from estrategias import ESTRATEGIAS, linear_com_biblioteca

AQUI = Path(__file__).resolve().parent
SAIDA = AQUI / "resultados"
TODOS_OS_CASOS = CASOS + CASOS_EXTRA


def _ja_feitos(arquivo: Path, condicao: str) -> set[tuple[str, str]]:
    """Chaves (caso, estratégia) já gravadas NESTA condição, para retomar de onde parou.
    Registros da Fase 2-A não têm o campo 'condicao' e contam como A0."""
    if not arquivo.exists():
        return set()
    feitos = set()
    with open(arquivo, encoding="utf-8") as f:
        for linha in f:
            try:
                r = json.loads(linha)
                if r.get("condicao", "A0") == condicao:
                    feitos.add((r["caso"], r["estrategia"]))
            except (json.JSONDecodeError, KeyError):
                continue  # linha truncada por interrupção: será refeita
    return feitos


def _arquivo_saida(modelo: str, condicao: str) -> Path:
    """! Alteração de IA - Revisar: um arquivo por (modelo, condição); A0 mantém o nome
    antigo para os resultados da Fase 2-A continuarem válidos sem conversão.
    ! Motivo: a retomada é por arquivo. Se as condições fossem gravadas juntas, uma
    execução interrompida de A2 poderia ser confundida com A1 já feita, e o Δ contra a
    linha de base sairia de registros misturados."""
    nome = modelo.replace(":", "_")
    return SAIDA / (f"{nome}.jsonl" if condicao == "A0" else f"{nome}__{condicao}.jsonl")


def rodar_modelo(modelo: str, casos: list[dict], estrategias: list[str],
                 max_tokens: int = 900, condicao: str = "A0", k: int = 3) -> None:
    SAIDA.mkdir(exist_ok=True)
    arquivo = _arquivo_saida(modelo, condicao)
    feitos = _ja_feitos(arquivo, condicao)

    # A biblioteca só é carregada quando a condição usa; em A0 o prompt é o mesmo da
    # Fase 2-A, byte a byte, para a linha de base continuar comparável.
    verbetes = indice = None
    if condicao != "A0":
        verbetes = bib.carregar()
        problemas = bib.validar(verbetes, TODOS_OS_CASOS)
        if problemas:
            raise SystemExit("biblioteca inválida — rode validar_banco.py:\n  " +
                             "\n  ".join(problemas))
        indice = rec.Indice(verbetes)
        print(f"biblioteca: {bib.resumo(verbetes)}")

    digest = oll.instalados().get(modelo, "?")
    pendentes = [(c, e) for c in casos for e in estrategias if (c["id"], e) not in feitos]
    print(f"\n=== {modelo} (digest {digest}) — condição {condicao} ===")
    print(f"{len(feitos)} já feitos, {len(pendentes)} pendentes")
    if not pendentes:
        return

    # ! Alteração de IA - Revisar: confere ANTES de inferir que o maior prompt cabe no
    # num_ctx junto com a resposta, usando o pior chars/token medido na Fase 2-A.
    # ! Motivo: quando o prompt excede num_ctx o Ollama descarta os tokens do COMEÇO em
    # silêncio — e o começo é justamente a biblioteca. O caso rodaria "com biblioteca" no
    # registro e sem biblioteca de fato, sem nenhum erro para acusar.
    if condicao != "A0":
        maior = max(len(linear_com_biblioteca(c, rec.contexto(verbetes, indice, c,
                                                                condicao, k)["texto"]))
                    for c, _ in pendentes)
        estimado = round(maior / bib.CHARS_POR_TOKEN) + max_tokens
        if estimado > oll.NUM_CTX:
            raise SystemExit(f"maior prompt de {condicao} estimado em {estimado} tokens "
                             f"(com resposta) > num_ctx {oll.NUM_CTX} — encurtar a biblioteca")
        print(f"maior prompt estimado: {estimado - max_tokens} tokens + {max_tokens} de resposta")

    inicio_lote = time.time()
    with open(arquivo, "a", encoding="utf-8") as f:
        for i, (caso, nome_estrategia) in enumerate(pendentes, 1):
            if condicao == "A0":
                ctx = {"texto": "", "verbetes_ids": [], "verbete_ouro": None,
                       "causa_plantada": None}
                prompt = ESTRATEGIAS[nome_estrategia](caso)
            else:
                ctx = rec.contexto(verbetes, indice, caso, condicao, k)
                prompt = linear_com_biblioteca(caso, ctx["texto"])
            try:
                r = oll.gerar(modelo, prompt, max_tokens=max_tokens)
            except Exception as e:  # falha de rede/timeout não deve derrubar a bateria
                r = {"segundos": None, "tokens_entrada": 0, "tokens_saida": 0,
                     "resposta": "", "erro": f"{type(e).__name__}: {e}"}

            # Segunda guarda, agora com a contagem REAL do tokenizador do modelo: se o
            # prompt encostou em num_ctx menos a resposta, o Ollama já pode ter descartado
            # o começo (a biblioteca) sem avisar. A primeira inferência de cada condição
            # decide; não vale gastar horas para descobrir no fim.
            if (condicao != "A0" and i == 1 and r.get("tokens_entrada")
                    and r["tokens_entrada"] + max_tokens >= oll.NUM_CTX - 16):
                raise SystemExit(
                    f"prompt avaliado em {r['tokens_entrada']} tokens + {max_tokens} de resposta "
                    f"encosta em num_ctx {oll.NUM_CTX}: provável truncamento do prefixo — "
                    "encurtar a biblioteca ou reduzir --max-tokens (registro NÃO gravado)")

            residentes = oll.residentes()
            registro = {
                "modelo": modelo, "digest": digest,
                "caso": caso["id"], "classe": caso["classe"], "nivel": caso["nivel"],
                "estrategia": nome_estrategia,
                "condicao": condicao,
                "verbetes_ids": ctx["verbetes_ids"],
                "verbete_ouro": ctx["verbete_ouro"],
                "causa_plantada": ctx["causa_plantada"],
                "chars_contexto": len(ctx["texto"]),
                "gabarito": caso["gabarito"],
                "teto_tokens": max_tokens,
                **r,
                "somente_cpu": all(m["vram_mb"] == 0 for m in residentes),
                "modelos_residentes": len(residentes),
                "memoria_mb": residentes[0]["memoria_mb"] if residentes else None,
            }
            f.write(json.dumps(registro, ensure_ascii=False) + "\n")
            f.flush()  # grava já: interromper aqui não perde o caso

            if i % 10 == 0 or i == len(pendentes):
                decorrido = time.time() - inicio_lote
                resta = decorrido / i * (len(pendentes) - i)
                print(f"  {i}/{len(pendentes)} — {decorrido/60:.1f} min decorridos, "
                      f"~{resta/60:.1f} min restantes")

    oll.descarregar(modelo)
    time.sleep(2)
    ok, nomes = oll.um_modelo_por_vez()
    if nomes:
        print(f"  aviso: ainda residente após descarregar: {nomes}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--modelos", nargs="+", required=True)
    ap.add_argument("--estrategias", nargs="+", default=list(ESTRATEGIAS))
    # ! Alteração de IA - Revisar: o teto de resposta passa a depender da condição — 900 em
    # A0 (igual à Fase 2-A) e 600 nos braços com biblioteca, salvo valor explícito.
    # ! Motivo: com num_ctx fixo em 8192, prompt e resposta dividem o mesmo orçamento; a
    # biblioteca inteira (~6,5 mil tokens no pior tokenizador medido) mais o maior caso
    # não deixam 900 para a resposta. Na Fase 2-A nenhuma resposta linear passou de
    # 600 tokens (ver Memorial §4.18), e o avaliar.py acusa qualquer resposta cortada
    # sem CAUSA_RAIZ — o caso não passa despercebido.
    ap.add_argument("--max-tokens", type=int, default=None,
                    help="teto de tokens por resposta (padrao: 900 em A0, 600 com biblioteca); "
                         "respostas no teto sao truncadas e invalidam o caso (ver avaliar.py)")
    ap.add_argument("--casos", type=int, default=0,
                    help="usar apenas os N primeiros casos (0 = todos os 90)")
    # ! Alteração de IA - Revisar: condição de biblioteca da Fase 2-B (A0 = sem biblioteca,
    # igual à Fase 2-A; A1 inteira; A2 recuperada top-k; A3 só o verbete certo; A4
    # distratores plausíveis; A5 verbete errado + registro falso).
    # ! Motivo: são os braços do desenho experimental aprovado; fora de A0 a estratégia é
    # forçada para 'linear' porque foi a vencedora da Fase 2-A e cruzar as três com as
    # condições triplicaria o custo sem responder nada novo.
    ap.add_argument("--condicao", choices=rec.CONDICOES, default="A0")
    ap.add_argument("--k", type=int, default=3, help="verbetes recuperados em A2/A4")
    args = ap.parse_args()

    casos = TODOS_OS_CASOS[:args.casos] if args.casos else TODOS_OS_CASOS
    max_tokens = args.max_tokens or (900 if args.condicao == "A0" else 600)
    estrategias = args.estrategias
    if args.condicao != "A0" and estrategias != ["linear"]:
        print("condição com biblioteca: estratégia fixada em 'linear' (vencedora da Fase 2-A)")
        estrategias = ["linear"]
    instalados = oll.instalados()

    print(f"{len(casos)} casos x {len(estrategias)} estratégias "
          f"= {len(casos) * len(estrategias)} inferências por modelo")

    for modelo in args.modelos:
        if modelo not in instalados:
            print(f"\n!! {modelo} não está baixado — pulando.")
            continue
        ok, nomes = oll.um_modelo_por_vez()
        if not ok:
            print(f"!! há {len(nomes)} modelos residentes antes de começar: {nomes}")
        rodar_modelo(modelo, casos, estrategias, max_tokens, args.condicao, args.k)

    print(f"\nResultados em {SAIDA}")


if __name__ == "__main__":
    main()
