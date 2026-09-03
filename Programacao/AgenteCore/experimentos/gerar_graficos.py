#!/usr/bin/env python3
# ! Alteração de IA - Revisar: gera os gráficos do experimento em PNG e SVG.
# ! Motivo: os números da avaliação precisam entrar no documento do TCC, e capturar tela de
# terminal produziria imagem ilegível em impressão. Tudo é lido de resumo_metricas.json —
# nenhum valor é digitado à mão, então gráfico e dados não podem divergir.
#
# Escolhas de cor não são estéticas, são de legibilidade e foram verificadas com o
# validador de paleta: no máximo três matizes categóricas (azul, laranja, verde-água), que
# é o limite que passa nos limiares de separação para daltonismo quando todos os pares
# aparecem juntos. O verde-água fica abaixo de 3:1 de contraste no fundo claro, o que
# obriga rótulo direto visível em cada barra — por isso todo gráfico rotula os valores.
# Onde seriam necessárias mais de três cores (6 modelos x 6 classes), usa-se mapa de calor
# de matiz única em vez de multiplicar matizes.
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

AQUI = Path(__file__).resolve().parent
GRAFICOS = AQUI / "graficos"

SUPERFICIE = "#fcfcfb"
TINTA = "#0b0b0b"
TINTA_2 = "#52514e"
GRADE = "#e5e4e0"
SERIES = ["#2a78d6", "#eb6834", "#1baf7a"]
RAMPA = ["#eaf1fb", "#c3d9f4", "#8fb9e9", "#5b98dd", "#2a78d6", "#1b5296"]

ROTULO_ESTRATEGIA = {"linear": "Linear", "compilador": "Estágios (compilador)",
                     "dominio": "Estágios (domínio)"}
ROTULO_CLASSE = {1: "Léxica", 2: "Sintática", 3: "Semântica",
                 4: "Tradução", 5: "Runtime", 6: "Efeito"}
ROTULO_NIVEL = {1: "Fácil", 2: "Médio", 3: "Difícil"}


def _base(largura=8.4, altura=4.6):
    fig, ax = plt.subplots(figsize=(largura, altura), dpi=150)
    fig.patch.set_facecolor(SUPERFICIE)
    ax.set_facecolor(SUPERFICIE)
    ax.grid(axis="y", color=GRADE, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    for lado in ("top", "right"):
        ax.spines[lado].set_visible(False)
    for lado in ("left", "bottom"):
        ax.spines[lado].set_color(GRADE)
    ax.tick_params(colors=TINTA_2, labelsize=9, length=0)
    return fig, ax


def _titular(ax, titulo, subtitulo=None):
    # pad generoso: o subtítulo fica logo acima do eixo e o título acima dele; com pad
    # menor as duas linhas se sobrepõem e o resultado fica ilegível na impressão.
    ax.set_title(titulo, color=TINTA, fontsize=12, fontweight="600", loc="left", pad=30)
    if subtitulo:
        ax.text(0, 1.015, subtitulo, transform=ax.transAxes, color=TINTA_2,
                fontsize=9, va="bottom")


def _salvar(fig, nome):
    GRAFICOS.mkdir(exist_ok=True)
    for ext in ("png", "svg"):
        fig.savefig(GRAFICOS / f"{nome}.{ext}", facecolor=SUPERFICIE,
                    bbox_inches="tight", pad_inches=0.25)
    plt.close(fig)
    print(f"  {nome}.png / .svg")


def _rotular(ax, barras, sufixo="%"):
    """Rótulo direto em cada barra — obrigatório: uma das matizes fica abaixo de
    3:1 de contraste no fundo claro, e o rótulo é o que garante a leitura."""
    for b in barras:
        alt = b.get_height()
        ax.text(b.get_x() + b.get_width() / 2, alt + 1.5, f"{alt:.0f}{sufixo}",
                ha="center", va="bottom", color=TINTA_2, fontsize=8)


def acerto_por_modelo(resumo):
    dados = sorted(resumo["por_modelo"], key=lambda r: -r["causa_correta_pct"])
    fig, ax = _base()
    barras = ax.bar([d["modelo"].replace("qwen2.5", "q2.5") for d in dados],
                    [d["causa_correta_pct"] for d in dados],
                    color=SERIES[0], width=0.6, zorder=3)
    _rotular(ax, barras)
    ax.set_ylim(0, 100)
    ax.yaxis.set_major_formatter(PercentFormatter())
    _titular(ax, "Acerto da causa raiz, por modelo",
             "Proporção de casos em que o modelo identificou corretamente a causa da falha")
    plt.setp(ax.get_xticklabels(), rotation=20, ha="right")
    _salvar(fig, "01-acerto-por-modelo")


def acerto_por_estrategia(resumo):
    modelos = sorted({r["modelo"] for r in resumo["por_modelo_estrategia"]})
    estrategias = ["linear", "compilador", "dominio"]
    fig, ax = _base(9.6, 4.8)
    largura = 0.26
    for i, est in enumerate(estrategias):
        vals = [next((r["causa_correta_pct"] for r in resumo["por_modelo_estrategia"]
                      if r["modelo"] == m and r["estrategia"] == est), None) for m in modelos]
        pos = [x + (i - 1) * (largura + 0.015) for x in range(len(modelos))]
        pos_ok = [p for p, v in zip(pos, vals) if v is not None]
        val_ok = [v for v in vals if v is not None]
        barras = ax.bar(pos_ok, val_ok, width=largura, color=SERIES[i], zorder=3,
                        label=ROTULO_ESTRATEGIA[est])
        _rotular(ax, barras)
        for p, v in zip(pos, vals):
            if v is None:
                ax.text(p, 2, "sem\ndado", ha="center", va="bottom",
                        fontsize=7, color=TINTA_2, style="italic")
    ax.set_xticks(range(len(modelos)))
    ax.set_xticklabels([m.replace("qwen2.5", "q2.5") for m in modelos], rotation=20, ha="right")
    ax.set_ylim(0, 100)
    ax.yaxis.set_major_formatter(PercentFormatter())
    leg = ax.legend(frameon=False, fontsize=9, ncols=3, loc="upper center",
                    bbox_to_anchor=(0.5, -0.22))
    for t in leg.get_texts():
        t.set_color(TINTA_2)
    _titular(ax, "Acerto por estratégia de raciocínio",
             "Estágios nomeados como fases de compilador contra os mesmos estágios com nomes do domínio")
    _salvar(fig, "02-acerto-por-estrategia")


def acerto_por_classe(resumo):
    modelos = sorted({r["modelo"] for r in resumo["por_modelo_classe"]})
    classes = sorted(ROTULO_CLASSE)
    matriz = [[next((r["causa_correta_pct"] for r in resumo["por_modelo_classe"]
                     if r["modelo"] == m and r["classe"] == c), 0) for c in classes]
              for m in modelos]

    fig, ax = plt.subplots(figsize=(8.6, 4.4), dpi=150)
    fig.patch.set_facecolor(SUPERFICIE)
    mapa = matplotlib.colors.LinearSegmentedColormap.from_list("azul", RAMPA)
    im = ax.imshow(matriz, cmap=mapa, vmin=0, vmax=100, aspect="auto")
    ax.set_xticks(range(len(classes)), [ROTULO_CLASSE[c] for c in classes])
    ax.set_yticks(range(len(modelos)), [m.replace("qwen2.5", "q2.5") for m in modelos])
    ax.tick_params(colors=TINTA_2, labelsize=9, length=0)
    for lado in ax.spines.values():
        lado.set_visible(False)
    for i in range(len(modelos)):
        for j in range(len(classes)):
            v = matriz[i][j]
            ax.text(j, i, f"{v:.0f}", ha="center", va="center", fontsize=8,
                    color="#ffffff" if v > 55 else TINTA)
    cb = fig.colorbar(im, ax=ax, shrink=0.8)
    cb.outline.set_visible(False)
    cb.ax.tick_params(colors=TINTA_2, labelsize=8, length=0)
    cb.set_label("acerto (%)", color=TINTA_2, fontsize=9)
    _titular(ax, "Acerto por classe de erro",
             "Matiz única: quanto mais escuro, maior o acerto. Valor impresso em cada célula")
    _salvar(fig, "03-acerto-por-classe")


def acerto_por_nivel(resumo):
    modelos = sorted({r["modelo"] for r in resumo["por_modelo_nivel"]})
    fig, ax = _base(9.6, 4.8)
    largura = 0.26
    for i, nivel in enumerate((1, 2, 3)):
        vals = [next((r["causa_correta_pct"] for r in resumo["por_modelo_nivel"]
                      if r["modelo"] == m and r["nivel"] == nivel), 0.0) for m in modelos]
        pos = [x + (i - 1) * (largura + 0.015) for x in range(len(modelos))]
        barras = ax.bar(pos, vals, width=largura, color=SERIES[i], zorder=3,
                        label=ROTULO_NIVEL[nivel])
        _rotular(ax, barras)
    ax.set_xticks(range(len(modelos)))
    ax.set_xticklabels([m.replace("qwen2.5", "q2.5") for m in modelos], rotation=20, ha="right")
    ax.set_ylim(0, 100)
    ax.yaxis.set_major_formatter(PercentFormatter())
    leg = ax.legend(frameon=False, fontsize=9, ncols=3, loc="upper center",
                    bbox_to_anchor=(0.5, -0.22))
    for t in leg.get_texts():
        t.set_color(TINTA_2)
    _titular(ax, "Acerto por nível de dificuldade",
             "Fácil: sinal explícito · Médio: contrato divergente · Difícil: falha de lógica ou estado")
    _salvar(fig, "04-acerto-por-nivel")


def custo_versus_acerto(resumo):
    """Dispersão com rótulo direto em cada ponto: identidade por texto, não por cor —
    com seis modelos, seis matizes não passariam nos limiares de separação."""
    dados = resumo["por_modelo"]
    fig, ax = _base(8.4, 5.0)
    ax.grid(color=GRADE, linewidth=0.8, zorder=0)
    for d in dados:
        ax.scatter(d["segundos_medio"], d["causa_correta_pct"], s=110,
                   color=SERIES[0], edgecolor=SUPERFICIE, linewidth=2, zorder=3)
        ax.annotate(d["modelo"].replace("qwen2.5", "q2.5"),
                    (d["segundos_medio"], d["causa_correta_pct"]),
                    textcoords="offset points", xytext=(9, 3),
                    fontsize=8.5, color=TINTA_2)
    ax.set_xlabel("segundos por inferência (mediana, só CPU)", color=TINTA_2, fontsize=9)
    ax.set_ylabel("acerto da causa raiz", color=TINTA_2, fontsize=9)
    ax.set_ylim(0, 100)
    ax.yaxis.set_major_formatter(PercentFormatter())
    _titular(ax, "Custo contra acerto",
             "Canto superior esquerdo é o melhor: mais acerto por menos tempo")
    _salvar(fig, "05-custo-versus-acerto")


def formato_valido_conteudo_errado(resumo):
    dados = sorted(resumo["por_modelo"], key=lambda r: -r["formato_ok_conteudo_errado_pct"])
    fig, ax = _base()
    barras = ax.bar([d["modelo"].replace("qwen2.5", "q2.5") for d in dados],
                    [d["formato_ok_conteudo_errado_pct"] for d in dados],
                    color=SERIES[1], width=0.6, zorder=3)
    _rotular(ax, barras)
    ax.set_ylim(0, 100)
    ax.yaxis.set_major_formatter(PercentFormatter())
    _titular(ax, "Resposta bem formatada e mesmo assim errada",
             "Saída que respeita o formato pedido mas aponta a causa errada — o erro que passa despercebido")
    plt.setp(ax.get_xticklabels(), rotation=20, ha="right")
    _salvar(fig, "06-formato-valido-conteudo-errado")


def main() -> None:
    arq = AQUI / "resumo_metricas.json"
    if not arq.exists():
        print("resumo_metricas.json não encontrado. Rode avaliar.py primeiro.")
        return
    resumo = json.loads(arq.read_text(encoding="utf-8"))
    print("Gerando gráficos em graficos/:")
    acerto_por_modelo(resumo)
    acerto_por_estrategia(resumo)
    acerto_por_classe(resumo)
    acerto_por_nivel(resumo)
    custo_versus_acerto(resumo)
    formato_valido_conteudo_errado(resumo)


if __name__ == "__main__":
    main()
