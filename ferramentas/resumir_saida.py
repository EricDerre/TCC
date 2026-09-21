# ! Alteração de IA - Revisar: filtro novo (21/09/2026) que encurta a saída de comandos longos antes de ela chegar ao
# contexto do Claude: mantém as primeiras N linhas, as últimas M e toda linha com marca de falha/erro/total.
# ! Motivo: `testar_fase3.py` imprime ~270 linhas e `rodar_*.ps1` centenas; cada linha lida pelo modelo custa tokens
# em todos os turnos seguintes. O hook `gancho_pre_bash.py` acrescenta este filtro ao comando; o Claude vê só o
# que decide (falhas, contagens, fim), e o texto completo continua no terminal/log de quem rodou.
"""Uso: comando 2>&1 | python ferramentas/resumir_saida.py [--cabeca 5] [--cauda 40] [--max-linha 300]"""
from __future__ import annotations

import argparse
import re
import sys

PADRAO_IMPORTANTE = re.compile(
    r"(\bFALHOU\b|\bfalha|\bFAIL|\bERRO\b|\berror\b|\bTraceback\b|\bException\b|AssertionError|"
    r"testes? ok|\bok$|exit|\bFIM\b|!!|AVISO|PULADO|== |Total|total de|quebrad|inalterad|diverg)",
    re.IGNORECASE,
)


def resumir(linhas: list[str], cabeca: int, cauda: int, max_linha: int) -> list[str]:
    n = len(linhas)
    if n <= cabeca + cauda:
        return [l[:max_linha] for l in linhas]
    manter = set(range(cabeca)) | set(range(n - cauda, n))
    for i, l in enumerate(linhas):
        if PADRAO_IMPORTANTE.search(l):
            manter.add(i)
    saida: list[str] = []
    ultimo = -1
    for i in sorted(manter):
        if i != ultimo + 1:
            saida.append(f"… [{i - ultimo - 1} linha(s) omitida(s) por resumir_saida.py]")
        saida.append(linhas[i][:max_linha])
        ultimo = i
    saida.append(f"[resumir_saida.py: {n} linhas no total, {len(manter)} mostradas]")
    return saida


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cabeca", type=int, default=5)
    ap.add_argument("--cauda", type=int, default=40)
    ap.add_argument("--max-linha", type=int, default=300)
    args = ap.parse_args()
    dados = sys.stdin.buffer.read().decode("utf-8", errors="replace")
    linhas = dados.splitlines()
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    for l in resumir(linhas, args.cabeca, args.cauda, args.max_linha):
        print(l)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
