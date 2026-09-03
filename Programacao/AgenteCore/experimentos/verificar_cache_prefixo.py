#!/usr/bin/env python3
# ! Alteração de IA - Revisar: "Verificação 0" da Fase 2-B — mede se o Ollama reaproveita o
# cache de KV quando o prefixo do prompt (a biblioteca inteira) é idêntico entre chamadas.
# ! Motivo: a issue #14780 do Ollama documenta que o backend de CPU do motor novo NÃO
# reaproveitava nada na v0.17.1 (o prompt inteiro era reavaliado a cada chamada); as
# correções aparecem referenciadas na 0.30.8 e esta máquina está na 0.33.2. Não dá para
# assumir: se o cache funciona, o prefill da biblioteca (~5 mil tokens em CPU) é pago uma
# vez por modelo e o braço "biblioteca inteira" quase não custa tempo; se não funciona,
# são dezenas de segundos a mais por caso e o desenho reduz a biblioteca antes de rodar.
# O diagnóstico é prompt_eval_count: com cache, a 2ª chamada avalia só os tokens novos.
import argparse
import sys

import biblioteca as bib
import cliente_ollama as oll
from banco_casos import CASOS
from estrategias import ESTRATEGIAS, linear_com_biblioteca


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--modelo", default="qwen2.5-coder:3b")
    args = ap.parse_args()

    residentes = [m["nome"] for m in oll.residentes()]
    if any(not n.startswith(args.modelo) for n in residentes):
        sys.exit(f"outro modelo residente ({residentes}) — rode depois da bateria terminar, "
                 "para não disputar CPU/memória (regra de um modelo por vez)")

    prefixo = bib.render_biblioteca(bib.carregar())
    caso1, caso2 = CASOS[0], CASOS[1]
    plano = [
        ("A  prefixo + caso 1", linear_com_biblioteca(caso1, prefixo)),
        ("B  prefixo + caso 1 (repetido)", linear_com_biblioteca(caso1, prefixo)),
        ("C  prefixo + caso 2 (só o fim muda)", linear_com_biblioteca(caso2, prefixo)),
        ("D  caso 1 sem prefixo", ESTRATEGIAS["linear"](caso1)),
        ("E  prefixo + caso 1 (depois de D)", linear_com_biblioteca(caso1, prefixo)),
    ]
    print(f"modelo {args.modelo} · biblioteca ≈ {bib.estimar_tokens(prefixo)} tokens (estimado)\n")
    print(f"{'chamada':38} {'tok. avaliados':>14} {'prefill ms':>11} {'total ms':>9}")
    medidas = []
    for rotulo, prompt in plano:
        r = oll.gerar(args.modelo, prompt, max_tokens=8)
        medidas.append(r)
        print(f"{rotulo:38} {r['tokens_entrada']:14} {r['prefill_ms']:11} {r['total_ms']:9}")

    a, b, c, d = medidas[0], medidas[1], medidas[2], medidas[3]
    print()
    # Contagem real do tokenizador deste modelo — substitui a estimativa por caracteres.
    if a["tokens_entrada"] and d["tokens_entrada"]:
        biblioteca_tok = a["tokens_entrada"] - d["tokens_entrada"]
        folga = oll.NUM_CTX - a["tokens_entrada"] - 600
        print(f"biblioteca ≈ {biblioteca_tok} tokens neste tokenizador; prompt A1 = "
              f"{a['tokens_entrada']} tokens; folga com resposta de 600 = {folga} tokens "
              f"({'OK' if folga > 0 else 'NÃO CABE — encurtar a biblioteca'})")
        if a["tokens_entrada"] < d["tokens_entrada"]:
            print("(a chamada A avaliou menos tokens que D: havia cache de uma execução "
                  "anterior — a contagem da biblioteca acima não é confiável)")
    # ! Alteração de IA - Revisar: o veredito passa a usar o TEMPO de prefill, não a contagem
    # de tokens.
    # ! Motivo: medido nesta máquina (Ollama 0.33.2, CPU): a repetição exata levou 105 ms de
    # prefill contra 80.653 ms da primeira chamada, mas prompt_eval_count veio 5.723 nas duas —
    # o Ollama reporta o tamanho do prompt, não o que de fato reavaliou. Com o critério antigo
    # o script imprimia "NÃO FUNCIONA" com o cache funcionando perfeitamente.
    razao_b = b["prefill_ms"] / max(a["prefill_ms"], 1)
    razao_c = c["prefill_ms"] / max(a["prefill_ms"], 1)
    if razao_b < 0.2:
        print(f"CACHE DE PREFIXO FUNCIONA: a repetição exata levou {b['prefill_ms']} ms de "
              f"prefill contra {a['prefill_ms']} ms na primeira chamada ({razao_b:.1%}).")
        if razao_c < 0.5:
            print(f"E vale para prefixo comum com sufixo diferente (chamada C: {c['prefill_ms']} "
                  f"ms, {razao_c:.1%}) — o braço A1 paga o prefill da biblioteca uma vez por "
                  "modelo e depois só o do caso.")
        else:
            print(f"Mas NÃO para sufixo diferente (chamada C: {c['prefill_ms']} ms, "
                  f"{razao_c:.1%}): só repetição exata reaproveita; cada caso de A1 paga o "
                  "prefill inteiro.")
    else:
        print("CACHE DE PREFIXO NÃO FUNCIONA nesta versão/backend: a repetição levou "
              f"{b['prefill_ms']} ms contra {a['prefill_ms']} ms. Reduzir a biblioteca inteira "
              "antes de rodar A1 e registrar o custo real de prefill no resultado.")
    if d["prefill_ms"] and d["tokens_entrada"]:
        print(f"prefill sem cache ≈ {1000 * d['tokens_entrada'] / d['prefill_ms']:.0f} tokens/s "
              "neste modelo e CPU")
    oll.descarregar(args.modelo)


if __name__ == "__main__":
    main()
