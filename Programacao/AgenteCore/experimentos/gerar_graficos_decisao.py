#!/usr/bin/env python3
# ! Alteração de IA - Revisar: cria gerar_graficos_decisao.py (Tarefa P2.1) -- a figura 18,
# que fecha a sequência de figuras do TCC (12-17 em gerar_graficos_fase3.py): dispersão
# acurácia balanceada x custo em segundos por (modelo, L), com o IC 95% do bootstrap por caso
# como barra vertical e os pontos não dominados da fronteira de Pareto destacados.
# ! Motivo: decisao_modelo.json (decidir_modelo.py) tem os três números que faltavam nas
# figuras 12-17 -- o IC do bootstrap por (modelo, L) e quais combinações não são dominadas na
# troca custo/acerto/risco -- e nenhuma figura ainda mostra os candidatos (4 modelos x L0..L3)
# lado a lado. Reaproveita _base/_titular/_salvar/_curto/SERIES/GRADE/TINTA/TINTA_2 de
# gerar_graficos.py e _espalhar_rotulos/LARGURA_POR_CARACTERE de gerar_graficos_fase3.py (o
# mesmo mecanismo de rótulo da figura 17, que resolve o mesmo problema -- muitos pontos
# próximos, o rótulo não pode empilhar) em vez de reescrevê-los, para a figura 18 sair com a
# MESMA aparência das 01-17. _rotular não serve aqui: é feito para altura de BARRA
# (b.get_height()), e esta figura é uma dispersão, como a 17.
"""Gera a figura 18: dispersão acurácia balanceada (36 casos de avaliação) x custo em
segundos por (modelo, estado da biblioteca L0..L3), com o IC 95% do bootstrap por caso como
barra vertical e os pontos não dominados da fronteira de Pareto destacados. Fonte de dados:
só resultados_alvo/fase3/decisao_modelo.json (nunca os JSONL brutos nem avaliacao_fase3.json
direto)."""
import argparse
import json
import sys

import gerar_graficos as gg
from gerar_graficos import _base, _curto, _salvar, _titular, GRADE, SERIES, TINTA, TINTA_2
from gerar_graficos_fase3 import _espalhar_rotulos, LARGURA_POR_CARACTERE
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

import caminhos

# ! Alteração de IA - Revisar: força UTF-8 na saída do console, copiado de
# biblioteca.py:25-32.
# ! Motivo: no Windows o console pode estar em cp1252; os avisos de "sem dado" têm acentos, e
# sem isso o script aborta com UnicodeEncodeError ao imprimi-los.
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def fig_18(decisao: dict) -> None:
    """! Alteração de IA - Revisar: figura 18 -- um ponto por (modelo, L) candidato da regra
    36 (decisao['regra_36']['ranking']): x = segundos (mediana, 36 casos), y = acurácia
    balanceada (36 casos); barra vertical fina = IC 95% do bootstrap
    (decisao['bootstrap']['nos_36']) na mesma coluna; marcador maior e contornado = não
    dominado (decisao['pareto']['nao_dominados']); rótulo `_curto(modelo) · LN` posicionado
    por _espalhar_rotulos, como na figura 17 (gerar_graficos_fase3.fig_17).
    ! Motivo: é a figura que resume a decisão dos passos 1-5 do brief P2.1 (escolher modelo +
    estado da biblioteca) -- a regra 36 e o escore ponderado já estão nas tabelas do .md, mas
    só o gráfico mostra de relance o mapa completo de troca entre custo e acerto, e se o
    vencedor tem uma vantagem clara ou está dentro do IC de outro candidato (o que a regra 36
    sozinha, um número por linha, não deixa ver)."""
    candidatos = [c for c in decisao.get("regra_36", {}).get("ranking", [])
                 if c.get("acuracia_balanceada_36") is not None
                 and c.get("segundos_mediana_36") is not None]
    if not candidatos:
        print("  18-decisao-pareto: sem dado")
        return

    ic_por_combo = {(c["modelo"], c["biblioteca_epoca"]): c.get("ic95_bootstrap")
                    for c in decisao.get("bootstrap", {}).get("nos_36", {}).get("combos", [])}
    nao_dominados = {(c["modelo"], c["biblioteca_epoca"])
                     for c in decisao.get("pareto", {}).get("nao_dominados", [])}

    candidatos = sorted(candidatos, key=lambda c: (c["segundos_mediana_36"],
                                                    -c["acuracia_balanceada_36"]))

    fig, ax = _base(11.4, 6.8)
    ax.grid(color=GRADE, linewidth=0.8, zorder=0)

    for c in candidatos:
        chave = (c["modelo"], c["biblioteca_epoca"])
        x, y = c["segundos_mediana_36"], c["acuracia_balanceada_36"]
        ic = ic_por_combo.get(chave)
        if ic and ic[0] is not None and ic[1] is not None:
            ax.plot([x, x], [ic[0], ic[1]], color=SERIES[0], linewidth=1.3, zorder=2,
                   alpha=0.5, solid_capstyle="round")
        destacado = chave in nao_dominados
        cor = SERIES[2] if destacado else SERIES[0]
        ax.scatter(x, y, s=140 if destacado else 90, facecolor=cor,
                  edgecolor=TINTA if destacado else cor,
                  linewidth=1.7 if destacado else 1.0, zorder=3)

    ax.set_xlabel("segundos por caso (mediana, 36 casos de avaliação)", color=TINTA_2,
                 fontsize=9)
    ax.set_ylabel("acurácia balanceada (36 casos de avaliação)", color=TINTA_2, fontsize=9)
    ax.set_ylim(0, 100)
    ax.yaxis.set_major_formatter(PercentFormatter())

    # Os limites do eixo têm de estar fechados ANTES de converter os pontos para a escala em
    # que os rótulos são medidos (pontos tipográficos): get_xlim() força o autoscale do x --
    # mesma ordem de gerar_graficos_fase3.fig_17.
    ax.get_xlim()
    fonte = 6.6
    textos = [f"{_curto(c['modelo'])} · L{c['biblioteca_epoca']}" for c in candidatos]
    em_pixels = ax.transData.transform(
        [(c["segundos_mediana_36"], c["acuracia_balanceada_36"]) for c in candidatos])
    ancoras = [(float(px) * 72 / fig.dpi, float(py) * 72 / fig.dpi) for px, py in em_pixels]
    larguras = [len(t) * fonte * LARGURA_POR_CARACTERE for t in textos]
    deslocamentos = _espalhar_rotulos(ancoras, larguras, fonte * 1.25)
    for c, texto, (dx, dy) in zip(candidatos, textos, deslocamentos):
        ax.annotate(texto, (c["segundos_mediana_36"], c["acuracia_balanceada_36"]),
                   textcoords="offset points", xytext=(dx, dy), fontsize=fonte,
                   ha="left" if dx > 0 else "right", va="center", color=TINTA_2,
                   arrowprops=dict(arrowstyle="-", color=GRADE, linewidth=0.7,
                                   shrinkA=0, shrinkB=3))

    handles = [
        plt.Line2D([0], [0], marker="o", linestyle="", markerfacecolor=SERIES[0],
                  markeredgecolor=SERIES[0], markersize=8, label="candidato (modelo, L)"),
        plt.Line2D([0], [0], marker="o", linestyle="", markerfacecolor=SERIES[2],
                  markeredgecolor=TINTA, markersize=9,
                  label="não dominado: nenhum outro é ao mesmo tempo mais barato, mais "
                        "certeiro e menos arriscado"),
        plt.Line2D([0], [0], color=SERIES[0], linewidth=1.3, alpha=0.5,
                  label="IC 95% da acurácia balanceada (bootstrap por caso)"),
    ]
    leg = ax.legend(handles=handles, frameon=False, fontsize=8, loc="upper center",
                    bbox_to_anchor=(0.5, -0.13))
    for t in leg.get_texts():
        t.set_color(TINTA_2)

    _titular(ax, "Decisão de modelo e estado da biblioteca",
            "Cada ponto é um modelo com a biblioteca num estado L0-L3 · canto superior "
            "esquerdo é o melhor (barato e certeiro)")
    _salvar(fig, "18-decisao-pareto")


# ! Alteração de IA - Revisar: linha de comando -- --saida escolhe a pasta de resultados da
# Fase 3 (ver caminhos.fase3) e lê decisao_modelo.json de lá (gravado por decidir_modelo.py).
# ! Motivo: mesmo padrão de gerar_graficos_fase3.main -- rodar sem argumento nenhum gera a
# figura da corrida oficial; --saida só existe para apontar para outra pasta sem editar o
# script.
def main() -> None:
    ap = argparse.ArgumentParser(
        description="Gera a figura 18 (decisão de modelo e estado da biblioteca) a partir de "
                    "decisao_modelo.json.")
    ap.add_argument("--saida", default="fase3",
                    help="subpasta dos resultados da Fase 3 (ver caminhos.fase3)")
    args = ap.parse_args()

    print(caminhos.descricao())
    c3 = caminhos.fase3(args.saida)
    caminho_decisao = c3["raiz"] / "decisao_modelo.json"
    if not caminho_decisao.exists():
        print(f"{caminho_decisao} não existe -- rode decidir_modelo.py --saida {args.saida} "
             "primeiro.")
        return
    decisao = json.loads(caminho_decisao.read_text(encoding="utf-8"))

    gg.GRAFICOS = c3["graficos"]
    gg.GRAFICOS.mkdir(parents=True, exist_ok=True)

    print(f"Gerando gráfico em {gg.GRAFICOS}:")
    fig_18(decisao)
    print(f"\nGráfico em {gg.GRAFICOS}")


if __name__ == "__main__":
    main()
