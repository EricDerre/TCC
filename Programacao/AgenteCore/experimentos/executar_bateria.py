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

import cliente_ollama as oll
from banco_casos import CASOS
from banco_casos_extra import CASOS_EXTRA
from estrategias import ESTRATEGIAS

AQUI = Path(__file__).resolve().parent
SAIDA = AQUI / "resultados"
TODOS_OS_CASOS = CASOS + CASOS_EXTRA


def _ja_feitos(arquivo: Path) -> set[tuple[str, str]]:
    """Chaves (caso, estratégia) já gravadas, para retomar de onde parou."""
    if not arquivo.exists():
        return set()
    feitos = set()
    with open(arquivo, encoding="utf-8") as f:
        for linha in f:
            try:
                r = json.loads(linha)
                feitos.add((r["caso"], r["estrategia"]))
            except (json.JSONDecodeError, KeyError):
                continue  # linha truncada por interrupção: será refeita
    return feitos


def rodar_modelo(modelo: str, casos: list[dict], estrategias: list[str],
                 max_tokens: int = 900) -> None:
    SAIDA.mkdir(exist_ok=True)
    arquivo = SAIDA / f"{modelo.replace(':', '_')}.jsonl"
    feitos = _ja_feitos(arquivo)

    digest = oll.instalados().get(modelo, "?")
    pendentes = [(c, e) for c in casos for e in estrategias if (c["id"], e) not in feitos]
    print(f"\n=== {modelo} (digest {digest}) ===")
    print(f"{len(feitos)} já feitos, {len(pendentes)} pendentes")
    if not pendentes:
        return

    inicio_lote = time.time()
    with open(arquivo, "a", encoding="utf-8") as f:
        for i, (caso, nome_estrategia) in enumerate(pendentes, 1):
            prompt = ESTRATEGIAS[nome_estrategia](caso)
            try:
                r = oll.gerar(modelo, prompt, max_tokens=max_tokens)
            except Exception as e:  # falha de rede/timeout não deve derrubar a bateria
                r = {"segundos": None, "tokens_entrada": 0, "tokens_saida": 0,
                     "resposta": "", "erro": f"{type(e).__name__}: {e}"}

            residentes = oll.residentes()
            registro = {
                "modelo": modelo, "digest": digest,
                "caso": caso["id"], "classe": caso["classe"], "nivel": caso["nivel"],
                "estrategia": nome_estrategia,
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
    ap.add_argument("--max-tokens", type=int, default=900,
                    help="teto de tokens por resposta; respostas no teto sao truncadas "
                         "e invalidam o caso (ver aviso do avaliar.py)")
    ap.add_argument("--casos", type=int, default=0,
                    help="usar apenas os N primeiros casos (0 = todos os 90)")
    args = ap.parse_args()

    casos = TODOS_OS_CASOS[:args.casos] if args.casos else TODOS_OS_CASOS
    instalados = oll.instalados()

    print(f"{len(casos)} casos x {len(args.estrategias)} estratégias "
          f"= {len(casos) * len(args.estrategias)} inferências por modelo")

    for modelo in args.modelos:
        if modelo not in instalados:
            print(f"\n!! {modelo} não está baixado — pulando.")
            continue
        ok, nomes = oll.um_modelo_por_vez()
        if not ok:
            print(f"!! há {len(nomes)} modelos residentes antes de começar: {nomes}")
        rodar_modelo(modelo, casos, args.estrategias, args.max_tokens)

    print(f"\nResultados em {SAIDA}")


if __name__ == "__main__":
    main()
