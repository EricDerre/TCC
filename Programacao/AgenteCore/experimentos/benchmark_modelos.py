#!/usr/bin/env python3
# NOTA (Fase 2-B): script CONGELADO como registro da primeira leva (RESULTADO_FASE2.md);
# o cliente do Ollama em uso pelos experimentos atuais esta em cliente_ollama.py.
# ! Alteração de IA - Revisar: compara os portes do Qwen2.5-Coder (1.5B/3B/7B) nas duas
# tarefas reais do agente, forçando inferência em CPU.
# ! Motivo: a metodologia (seção 3.2 do projeto de pesquisa) exige escolher o porte do
# modelo por comparação, e o problema de pesquisa afirma operar "sob restrições de
# hardware local". Esta máquina tem uma GTX 1650, então medir com GPU inflaria o
# resultado e não sustentaria essa afirmação — por isso todas as medições enviam
# num_gpu=0, e o script confere em /api/ps se o modelo realmente ficou fora da VRAM.
# Usa apenas biblioteca padrão de propósito: nesta fase o AgenteCore ainda não tem venv,
# e o benchmark não deve depender de nada além do Ollama já instalado.
import argparse
import json
import statistics
import time
import urllib.error
import urllib.request
from pathlib import Path

from prompts_benchmark import TAREFAS

OLLAMA = "http://localhost:11434"
AQUI = Path(__file__).resolve().parent


def _post(caminho: str, corpo: dict, timeout: int = 600) -> dict:
    req = urllib.request.Request(
        f"{OLLAMA}{caminho}",
        data=json.dumps(corpo).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read())


def _get(caminho: str, timeout: int = 30) -> dict:
    with urllib.request.urlopen(f"{OLLAMA}{caminho}", timeout=timeout) as resp:
        return json.loads(resp.read())


def gerar(modelo: str, instrucao: str, cenario: str) -> dict:
    """Uma inferência, com a GPU desligada explicitamente (num_gpu=0)."""
    inicio = time.perf_counter()
    r = _post("/api/generate", {
        "model": modelo,
        "prompt": f"{instrucao}\n\n{cenario}",
        "stream": False,
        "options": {"num_gpu": 0, "temperature": 0.1, "num_predict": 300},
    })
    segundos = time.perf_counter() - inicio
    return {
        "segundos": round(segundos, 2),
        "tokens_saida": r.get("eval_count", 0),
        "tokens_entrada": r.get("prompt_eval_count", 0),
        "resposta": r.get("response", "").strip(),
    }


def memoria_carregada(modelo: str) -> dict:
    """Lê /api/ps para registrar quanta memória o modelo ocupa e confirmar que
    nada foi para a VRAM (size_vram deve ser 0 com num_gpu=0)."""
    for m in _get("/api/ps").get("models", []):
        if m.get("name", "").startswith(modelo.split(":")[0]) and modelo.split(":")[-1] in m.get("name", ""):
            total = m.get("size", 0)
            vram = m.get("size_vram", 0)
            return {
                "memoria_mb": round(total / 1024 / 1024),
                "vram_mb": round(vram / 1024 / 1024),
                "somente_cpu": vram == 0,
            }
    return {"memoria_mb": None, "vram_mb": None, "somente_cpu": None}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--modelos", nargs="+",
                    default=["qwen2.5-coder:1.5b", "qwen2.5-coder:3b", "qwen2.5-coder:7b"])
    ap.add_argument("--repeticoes", type=int, default=3)
    args = ap.parse_args()

    instalados = {m["name"] for m in _get("/api/tags").get("models", [])}
    resultados = []

    for modelo in args.modelos:
        if modelo not in instalados:
            print(f"[bench] {modelo} nao esta baixado — pulando.")
            continue
        for tarefa in TAREFAS:
            print(f"[bench] {modelo} / {tarefa['nome']} ...", flush=True)
            medidas, ultima = [], None
            for _ in range(args.repeticoes):
                try:
                    ultima = gerar(modelo, tarefa["instrucao"], tarefa["cenario"])
                except (urllib.error.URLError, TimeoutError) as e:
                    print(f"[bench]   ERRO: {e}")
                    break
                medidas.append(ultima["segundos"])
            if not medidas:
                continue
            mem = memoria_carregada(modelo)
            resultados.append({
                "modelo": modelo,
                "tarefa": tarefa["nome"],
                "segundos_mediana": round(statistics.median(medidas), 2),
                "segundos_min": min(medidas),
                "segundos_max": max(medidas),
                "tokens_entrada": ultima["tokens_entrada"],
                "tokens_saida": ultima["tokens_saida"],
                **mem,
                "resposta": ultima["resposta"],
            })
            print(f"[bench]   mediana {resultados[-1]['segundos_mediana']}s "
                  f"| {mem['memoria_mb']} MB | somente_cpu={mem['somente_cpu']}")

    (AQUI / "resultado_benchmark.json").write_text(
        json.dumps(resultados, ensure_ascii=False, indent=2), encoding="utf-8")

    # O cabeçalho abaixo vai para dentro do arquivo gerado: como ele é reescrito a cada
    # execução, o marcador precisa ser emitido pelo gerador para não se perder.
    linhas = ["<!-- ! Alteração de IA - Revisar: tabela gerada por benchmark_modelos.py.",
              "     ! Motivo: saída de medição, reescrita a cada execução — não editar à mão;",
              "     a leitura e as conclusões estão em RESULTADO_FASE2.md. -->",
              "",
              "| Modelo | Tarefa | Mediana (s) | Faixa (s) | Tokens ent./saída | Memória | Só CPU |",
              "|---|---|---|---|---|---|---|"]
    for r in resultados:
        linhas.append(
            f"| {r['modelo']} | {r['tarefa']} | {r['segundos_mediana']} | "
            f"{r['segundos_min']}–{r['segundos_max']} | {r['tokens_entrada']}/{r['tokens_saida']} | "
            f"{r['memoria_mb']} MB | {'sim' if r['somente_cpu'] else 'NAO'} |")
    (AQUI / "resultado_benchmark.md").write_text("\n".join(linhas) + "\n", encoding="utf-8")
    print("\n".join(linhas))


if __name__ == "__main__":
    main()
