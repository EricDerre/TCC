#!/usr/bin/env python3
# ! Alteração de IA - Revisar: cria gerar_graficos_fase3.py -- as figuras 12 a 17 do TCC
# (Fase 3 e a comparação entre as três fases de teste), continuando a numeração de
# gerar_graficos.py (01-06 Fase 2-A, 07-11 Fase 2-B).
# ! Motivo: resumo_fase3.json e comparacao_fases.json (Tarefas 8 e 9) têm as métricas por
# versão de biblioteca (L0..L3), por época de proposta e a comparação pareada entre fases,
# mas nenhum gráfico as lê ainda -- as tabelas do Memorial citam número solto sem a figura
# ao lado. Reaproveita de gerar_graficos.py a paleta e as funções de estilo (_base, _titular,
# _salvar, _rotular, _curto, SERIES, RAMPA, TINTA, TINTA_2, GRADE, SUPERFICIE) em vez de
# reescrevê-las, para as figuras 12-17 saírem com a MESMA aparência das 01-11 -- até três
# matizes categóricas por gráfico, rótulo direto em todo ponto/barra, "sem dado" explícito
# onde a corrida não cobre um modelo, PNG + SVG. Nenhum valor é digitado à mão: tudo sai de
# resumo_fase3.json e comparacao_fases.json (nunca dos JSONL brutos).
"""Gera as figuras 12-17: acerto por versão da biblioteca (por modelo, um painel cada),
recuperação do verbete certo por versão, propostas de edição (aceitas e motivos de
rejeição), crescimento da biblioteca em tokens, e a comparação entre as fases 2-A, 2-B e 3
(acerto e custo contra acerto). Fonte de dados: só resumo_fase3.json e comparacao_fases.json
-- nunca os JSONL de diagnóstico/proposta."""
import argparse
import json
import math
import sys

import gerar_graficos as gg
from gerar_graficos import (_base, _curto, _rotular, _salvar, _titular, GRADE, RAMPA, SERIES,
                            SUPERFICIE, TINTA, TINTA_2)
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

import caminhos

# ! Alteração de IA - Revisar: força UTF-8 na saída do console, copiado de
# biblioteca.py:25-32.
# ! Motivo: no Windows o console pode estar em cp1252; os nomes de gráfico e os avisos de
# "sem dado" têm acentos, e sem isso o script aborta com UnicodeEncodeError ao imprimi-los.
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


# --------------------------------------------------------------------- constantes

# ! Alteração de IA - Revisar: ordem fixa dos 4 modelos da corrida oficial da Fase 3, do mais
# rápido ao mais lento (a mesma ordem de executar_fase3.VELOCIDADE_MEDIDA).
# ! Motivo: as figuras 12, 13, 14, 16 e 17 mostram um painel ou grupo de barras por modelo; sem
# uma ordem fixa a mesma figura sairia com os modelos em posições diferentes a cada corrida
# (dict e set não garantem ordem), dificultando comparar a figura de uma versão do relatório
# com a de outra.
ORDEM_MODELOS = ("qwen2.5-coder:3b", "qwen2.5:7b", "qwen2.5-coder:7b", "granite4.2:8b")

# Colunas de comparacao_fases.json usadas nas figuras 16 e 17, na ordem cronológica das
# fases (2-A -> 2-B sem biblioteca -> 2-B recuperada -> Fase 3 original -> Fase 3 editada).
COLUNAS_COMPARACAO = ("2A_linear_ryzen", "2B_A0", "2B_A2", "F3_L0", "F3_L3")
ROTULO_COLUNA = {"2A_linear_ryzen": "2-A linear", "2B_A0": "2-B A0", "2B_A2": "2-B A2",
                 "F3_L0": "F3 L0", "F3_L3": "F3 L3"}


def _ordenar_modelos(modelos_presentes) -> list[str]:
    """! Alteração de IA - Revisar: ordena os modelos presentes num resumo/comparação pela
    ORDEM_MODELOS da corrida oficial, e põe qualquer modelo fora dessa lista no final, em
    ordem alfabética.
    ! Motivo: resumo_fase3.json e comparacao_fases.json guardam o modelo como chave de
    dict/valor de set, que não preservam ordem -- sem esta função, a figura 12 (por exemplo)
    sairia com os 4 modelos em posições diferentes a cada execução. Os nomes fora da lista
    (o teste sintético usa 'modelo-zero'/'modelo-um', que não existem na corrida real) caem
    no fim em vez de desaparecer ou quebrar, para a mesma função valer também nos dados
    fictícios do teste e num piloto com um subconjunto de modelos."""
    presentes = set(modelos_presentes)
    conhecidos = [m for m in ORDEM_MODELOS if m in presentes]
    extras = sorted(presentes - set(conhecidos))
    return conhecidos + extras


def _estilizar_eixo(ax, eixo_grade: str = "y") -> None:
    """! Alteração de IA - Revisar: aplica a MESMA aparência de eixo de gerar_graficos._base
    (fundo, grade, remoção das bordas superior/direita, cor dos ticks) a um Axes que já
    existe.
    ! Motivo: _base cria a figura E o eixo juntos, sempre em par único -- um painel múltiplo
    (uma figura, vários Axes, como as figuras 12 e 14 precisam, um painel por modelo) não tem
    como reaproveitar _base sem criar uma figura nova por painel. Reescrever aqui as mesmas
    cinco chamadas de estilo é o que mantém os painéis da Fase 3 com a MESMA aparência dos
    gráficos de eixo único da 2-A/2-B. `eixo_grade='x'` é usado na figura 14 (barras
    horizontais), onde a grade de referência precisa acompanhar o eixo NUMÉRICO (a contagem
    de propostas), não o categórico (o motivo)."""
    ax.set_facecolor(SUPERFICIE)
    ax.grid(axis=eixo_grade, color=GRADE, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    for lado in ("top", "right"):
        ax.spines[lado].set_visible(False)
    for lado in ("left", "bottom"):
        ax.spines[lado].set_color(GRADE)
    ax.tick_params(colors=TINTA_2, labelsize=9, length=0)


def _grade_paineis(n: int, largura: float = 11.0, altura_por_linha: float = 4.3):
    """! Alteração de IA - Revisar: cria uma figura com `n` painéis numa grade de até 2
    colunas (linhas = ceil(n/2)), escondendo os eixos que sobrarem quando `n` for ímpar, e
    devolve (fig, lista de Axes na ordem de leitura, esquerda-direita/cima-baixo).
    ! Motivo: a corrida oficial da Fase 3 tem 4 modelos (grade 2x2, como pede o briefing da
    Tarefa 10), mas o teste sintético roda com 2 (para não depender do banco de 90 casos) e
    um piloto pode ter menos ainda -- uma grade fixa 2x2 quebraria (IndexError) com um número
    de modelos diferente de 4. Calcular a grade a partir de `n` é o que deixa a mesma função
    valer para os dois casos. `squeeze=False` garante que `eixos` seja sempre uma matriz 2D
    mesmo com 1 linha ou 1 coluna, para o `.flatten()` funcionar igual em qualquer `n`."""
    colunas = 2 if n > 1 else 1
    linhas = math.ceil(n / colunas)
    fig, eixos = plt.subplots(linhas, colunas, figsize=(largura, altura_por_linha * linhas),
                              dpi=150, squeeze=False)
    fig.patch.set_facecolor(SUPERFICIE)
    eixos_flat = list(eixos.flatten())
    for ax in eixos_flat[n:]:
        ax.set_visible(False)
    return fig, eixos_flat[:n]


def _titular_fig(fig, titulo: str, subtitulo: str | None = None) -> None:
    """! Alteração de IA - Revisar: título e subtítulo da FIGURA inteira (fig.suptitle /
    fig.text), para as figuras 12 e 14, que têm um painel por modelo. As posições em y são
    calculadas em POLEGADAS a partir do topo (fig.get_size_inches()[1]) e só DEPOIS convertidas
    para fração de figura, e o espaço dos painéis é reservado com fig.subplots_adjust(top=...)
    chamado DEPOIS de fig.tight_layout() (não com o `rect` de tight_layout).
    ! Motivo (Fix round 1 da revisão da Tarefa 10): a primeira versão usava frações fixas de
    figura (suptitle no y padrão do matplotlib, ~0,98, e o subtítulo em fig.text(..., 0.953,
    ...)) e reservava o topo com `tight_layout(rect=(0,0,1,0.90))`. Duas figuras usam
    _grade_paineis, que muda a ALTURA da figura conforme o número de modelos (2 modelos = 1
    linha = ~4,3'; 4 modelos = 2 linhas = ~8,6') -- e uma fração fixa de figura corresponde a
    uma distância em POLEGADAS diferente em cada caso. Na figura de 8,6' a folga entre y=0,98 e
    y=0,953 já é pequena demais para caber uma linha de 13pt mais uma de 9pt sem colidir; na de
    4,3' ela é ainda mais apertada (a mesma fração equivale a metade da distância em
    polegadas) -- foi isso que fez título e subtítulo aparecerem entrelaçados e ilegíveis em
    12-fase3-acerto-por-epoca.png e 14-fase3-propostas-por-motivo.png (achado da revisão,
    round 1). Calcular a partir de polegadas reais faz o mesmo espaçamento visual valer para
    qualquer número de linhas de painéis. `tight_layout()` sem `rect` roda primeiro para o
    matplotlib acomodar rótulos de eixo/legenda; só then `subplots_adjust(top=...)` sobrescreve
    a margem superior com a calculada aqui -- `tight_layout(rect=...)` não serve porque ele
    IGNORA suptitle/fig.text ao calcular o que cabe (é a causa raiz do defeito: o matplotlib não
    conhece esses dois elementos como parte do layout)."""
    fig.tight_layout()
    altura = fig.get_size_inches()[1]
    fig.suptitle(titulo, color=TINTA, fontsize=13, fontweight="600", x=0.02, ha="left",
                y=1 - 0.32 / altura)
    margem_polegadas = 0.62
    if subtitulo:
        fig.text(0.02, 1 - 0.66 / altura, subtitulo, color=TINTA_2, fontsize=9, ha="left",
                 va="top")
        margem_polegadas = 1.08
    fig.subplots_adjust(top=1 - margem_polegadas / altura)


# --------------------------------------------------------------------------- figura 12

def fig_12(resumo: dict) -> None:
    """! Alteração de IA - Revisar: figura 12 -- um painel por modelo (grade 2x2 na corrida
    oficial), acerto da causa raiz por versão da biblioteca (L0..L3): linha cheia SERIES[0]
    para os 36 casos de avaliação (nunca entraram na biblioteca) e tracejada SERIES[1] para
    os 54 de aprendizado, valor rotulado em cada ponto.
    ! Motivo: é a pergunta central da Fase 3 -- 'o acerto melhora conforme o modelo edita a
    própria biblioteca?' -- e ela só faz sentido separada por partição: o ganho nos 54 casos
    de aprendizado pode ser o modelo memorizando o que ele mesmo escreveu sobre aqueles casos
    (o texto contém pistas do caso, mesmo sem copiá-lo por completo), enquanto o ganho nos 36
    de avaliação é o único que mede generalização de verdade. Um painel por modelo (em vez de
    uma única figura com 8 linhas) é o que evita 4 modelos x 2 partições = 8 linhas coloridas
    disputando os mesmos 3 matizes permitidos."""
    linhas = resumo.get("por_modelo_biblioteca_particao", [])
    modelos = _ordenar_modelos({l["modelo"] for l in linhas})
    if not modelos:
        print("  12-fase3-acerto-por-epoca: sem dado")
        return

    fig, eixos = _grade_paineis(len(modelos))
    # ! Alteração de IA - Revisar: o rótulo da avaliação fica ACIMA do ponto com va="bottom"
    # (o texto cresce para cima, se afastando do marcador) e o do aprendizado fica ABAIXO com
    # va="top" (o texto cresce para baixo) -- as duas âncoras se afastam do ponto, não se
    # aproximam dele.
    # ! Motivo: a primeira versão usava as direções trocadas (va="top" no deslocamento
    # positivo e va="bottom" no negativo), que faz o texto CRESCER NA DIREÇÃO do marcador em
    # vez de se afastar -- nos pontos em que as duas linhas quase se cruzam (ex.: L0-L1 do
    # qwen2.5-coder:3b, onde avaliação e aprendizado diferem por só 1-5 pp), os dois rótulos
    # ficavam colados no marcador e um por cima do outro, em vez de um acima e um abaixo com
    # folga.
    series = (("avaliacao", SERIES[0], "-", 4, "bottom"),
             ("aprendizado", SERIES[1], "--", -6, "top"))
    for ax, modelo in zip(eixos, modelos):
        _estilizar_eixo(ax)
        algum_ponto = False
        for particao, cor, estilo, deslocamento, alinhamento in series:
            pontos = sorted((l["biblioteca_epoca"], l["causa_correta_pct"]) for l in linhas
                            if l["modelo"] == modelo and l["particao"] == particao)
            if not pontos:
                continue
            algum_ponto = True
            xs = [p[0] for p in pontos]
            ys = [p[1] for p in pontos]
            ax.plot(xs, ys, color=cor, linestyle=estilo, marker="o", markersize=5,
                    linewidth=1.8, zorder=3)
            for x, y in zip(xs, ys):
                ax.text(x, y + deslocamento, f"{y:.0f}%", ha="center", va=alinhamento,
                        color=TINTA_2, fontsize=7.5)
        if not algum_ponto:
            ax.text(0.5, 0.5, "sem dado", ha="center", va="center", transform=ax.transAxes,
                    color=TINTA_2, fontsize=9, style="italic")
        ax.set_xticks(range(4))
        ax.set_xticklabels([f"L{e}" for e in range(4)])
        ax.set_xlim(-0.4, 3.4)
        ax.set_ylim(0, 112)
        ax.set_yticks(range(0, 101, 20))
        ax.yaxis.set_major_formatter(PercentFormatter())
        ax.set_title(_curto(modelo), color=TINTA, fontsize=10, fontweight="600", loc="left")

    _titular_fig(fig, "Acerto por versão da biblioteca do modelo",
                "Linha cheia: 36 casos de avaliação (sem feedback) · tracejada: 54 de "
                "aprendizado")
    _salvar(fig, "12-fase3-acerto-por-epoca")


# --------------------------------------------------------------------------- figura 13

def fig_13(resumo: dict) -> None:
    """! Alteração de IA - Revisar: figura 13 -- barras agrupadas por modelo, 4 barras (L0..L3)
    em RAMPA[2:6] (matiz única, mais escura a cada versão), altura = hit@3 do verbete de ouro
    nos 36 casos de avaliação; a MRR da mesma versão entra como texto pequeno sob cada grupo.
    ! Motivo: a Fase 3 só vê os k verbetes que a recuperação BM25 traz -- se o acerto cai de
    uma versão para outra (figura 12), este gráfico é o que separa 'o modelo raciocinou pior'
    de 'o verbete certo deixou de ser recuperado' (a documentação que o próprio modelo
    acrescenta muda o índice). hit@3 e MRR medem a mesma coisa em granularidades diferentes
    (limiar rígido vs. posição média) -- por isso o MRR entra como anotação, não como uma
    quarta cor: um gráfico com hit@3 (barra) e MRR (barra também) precisaria de 8 matizes
    para 4 modelos, acima do limite de legibilidade de três matizes por figura."""
    linhas = resumo.get("recuperacao", [])
    modelos = _ordenar_modelos({l["modelo"] for l in linhas})
    if not modelos:
        print("  13-fase3-recuperacao-por-epoca: sem dado")
        return

    fig, ax = _base(9.8, 5.6)
    n_epocas = 4
    largura = 0.8 / n_epocas
    for epoca in range(n_epocas):
        pos = [x + (epoca - (n_epocas - 1) / 2) * (largura + 0.01) for x in range(len(modelos))]
        linhas_epoca = [next((l for l in linhas if l["modelo"] == modelo
                             and l["biblioteca_epoca"] == epoca), None) for modelo in modelos]
        vals = [l["avaliacao"]["hit@3"] if l else None for l in linhas_epoca]
        pos_ok = [p for p, v in zip(pos, vals) if v is not None]
        val_ok = [v for v in vals if v is not None]
        barras = ax.bar(pos_ok, val_ok, width=largura, color=RAMPA[2 + epoca], zorder=3,
                        label=f"L{epoca}")
        _rotular(ax, barras)
        # ! Alteração de IA - Revisar: a MRR de CADA barra entra sob a própria barra (não uma
        # string só por grupo de modelo).
        # ! Motivo: a primeira versão juntava as 4 MRR de um modelo numa única linha de texto
        # centrada no grupo ("MRR L0 0,50 · L1 0,55 · L2 0,60 · L3 0,65") -- larga demais para
        # a largura de um grupo de 4 barras, e o texto de um grupo invadia o do vizinho (ficava
        # ilegível, ex. "...L3 0,65MRR L0..." colado). Uma anotação curta por barra, alinhada
        # embaixo dela, ocupa a MESMA largura que a barra já ocupa e nunca invade o grupo ao
        # lado.
        for p, l in zip(pos, linhas_epoca):
            texto = f"{l['avaliacao']['mrr']:.2f}" if l else "sem dado"
            if epoca == 0:
                texto = f"MRR {texto}" if l else texto
            ax.text(p, -0.17, texto, transform=ax.get_xaxis_transform(), ha="center",
                    va="top", fontsize=6.5, color=TINTA_2, rotation=90 if not l else 0)

    ax.set_xticks(range(len(modelos)))
    ax.set_xticklabels([_curto(m) for m in modelos], rotation=20, ha="right")
    ax.set_ylim(0, 112)
    ax.set_yticks(range(0, 101, 20))
    ax.yaxis.set_major_formatter(PercentFormatter())
    leg = ax.legend(frameon=False, fontsize=9, ncols=n_epocas, loc="upper center",
                    bbox_to_anchor=(0.5, -0.30))
    for t in leg.get_texts():
        t.set_color(TINTA_2)
    _titular(ax, "Recuperação do verbete certo com a biblioteca de cada modelo",
             "hit@3 nos 36 casos de avaliação · MRR da mesma versão sob cada grupo de barras")
    _salvar(fig, "13-fase3-recuperacao-por-epoca")


# --------------------------------------------------------------------------- figura 14

def fig_14(resumo: dict) -> None:
    """! Alteração de IA - Revisar: figura 14 -- um painel por modelo, barras horizontais com
    a soma das 3 épocas: 'aceitas' em SERIES[2], cada código de rejeição (motivos_rejeicao)
    em SERIES[1] ordenado por contagem decrescente, e 'nenhuma' (o modelo decidiu não propor
    edição) em SERIES[0]; contagem rotulada ao lado de cada barra.
    ! Motivo: documentacao_por_epoca (avaliar_fase3.py) já soma os códigos de rejeição por
    época; aqui eles são somados também ENTRE épocas porque a pergunta do Memorial é 'o que
    trava o modelo ao editar a biblioteca', e não 'em que época' -- o histograma por época já
    está na tabela de texto do relatório da Fase 3, este gráfico é o retrato agregado. Os
    códigos com contagem zero (motivos_rejeicao começa com TODOS os códigos de
    evolucao_biblioteca.CODIGOS_REJEICAO em zero, de propósito, para a soma bater com o total
    de propostas recusadas) são descartados aqui -- um painel com ~20 barras vazias tornaria
    ilegível justamente os poucos motivos que aconteceram de verdade."""
    linhas = resumo.get("documentacao", [])
    modelos = _ordenar_modelos({l["modelo"] for l in linhas})
    if not modelos:
        print("  14-fase3-propostas-por-motivo: sem dado")
        return

    fig, eixos = _grade_paineis(len(modelos), altura_por_linha=4.6)
    for ax, modelo in zip(eixos, modelos):
        _estilizar_eixo(ax, eixo_grade="x")
        do_modelo = [l for l in linhas if l["modelo"] == modelo]
        aceitas = sum(l.get("n_aceitas", 0) for l in do_modelo)
        nenhuma = sum(l.get("n_nenhuma", 0) for l in do_modelo)
        motivos: dict[str, int] = {}
        for l in do_modelo:
            for codigo, n in l.get("motivos_rejeicao", {}).items():
                if n:
                    motivos[codigo] = motivos.get(codigo, 0) + n
        motivos_ordenados = sorted(motivos.items(), key=lambda kv: -kv[1])

        categorias = ["aceitas"] + [c for c, _ in motivos_ordenados] + ["nenhuma"]
        valores = [aceitas] + [n for _, n in motivos_ordenados] + [nenhuma]
        cores = [SERIES[2]] + [SERIES[1]] * len(motivos_ordenados) + [SERIES[0]]

        posicoes = list(range(len(categorias)))
        barras = ax.barh(posicoes, valores, color=cores, zorder=3)
        maior = max(valores) if valores else 0
        for b, v in zip(barras, valores):
            ax.text(b.get_width() + max(maior, 1) * 0.02, b.get_y() + b.get_height() / 2,
                    f"{v}", va="center", ha="left", color=TINTA_2, fontsize=8)
        ax.set_yticks(posicoes)
        ax.set_yticklabels([c.replace("_", " ") for c in categorias], fontsize=8)
        ax.invert_yaxis()
        ax.set_xlim(0, maior * 1.18 if maior else 1)
        ax.set_title(_curto(modelo), color=TINTA, fontsize=10, fontweight="600", loc="left")

    _titular_fig(fig, "Propostas de edição: aceitas e motivos de rejeição",
                "Soma das 3 épocas de aprendizado · 'nenhuma' = o modelo decidiu não propor "
                "edição naquele caso")
    _salvar(fig, "14-fase3-propostas-por-motivo")


# --------------------------------------------------------------------------- figura 15

def _series_fig_15(resumo: dict) -> dict[str, list[tuple[int, int]]]:
    """! Alteração de IA - Revisar: {modelo: [(versão, tokens_estimados), ...]} lido de
    resumo['recuperacao'] (uma linha por versão L0..L3 de cada modelo, com o tamanho
    RENDERIZADO da biblioteca copiado do fechamento.json), em ordem de versão -- onda final
    (achado I4).
    ! Motivo: a versão anterior misturava duas unidades na mesma reta: tokens_estimados do
    fechamento (texto renderizado, o que entra no prompt) para L1..L3 e, para reconstruir o
    L0, subtraía tokens_estimados_acrescentados do diff da época 1 -- que mede bytes crus do
    .md (frontmatter, cabeçalhos, a linha de rastreio), cerca de 2,5x maior que o mesmo
    acréscimo renderizado. O L0 saía errado para baixo. Agora avaliar_fase3.
    recuperacao_por_epoca grava o tamanho de CADA versão, L0 inclusive, e a figura só lê."""
    series: dict[str, list[tuple[int, int]]] = {}
    for linha in resumo.get("recuperacao", []):
        if linha.get("tokens_estimados") is None:
            continue
        series.setdefault(linha["modelo"], []).append(
            (linha["biblioteca_epoca"], linha["tokens_estimados"]))
    return {modelo: sorted(pontos) for modelo, pontos in series.items()}


def fig_15(resumo: dict) -> None:
    """! Alteração de IA - Revisar: figura 15 -- um painel, uma linha por modelo (SERIES[0],
    marcador diferente por modelo, rótulo de texto no fim da linha) com o tamanho renderizado
    da biblioteca (tokens estimados do fechamento.json de cada versão, ver _series_fig_15)
    por versão L0..L3, mais uma linha de referência tracejada TINTA_2 no tamanho da
    biblioteca ORIGINAL (L0).
    ! Motivo: as 4 linhas usam a MESMA cor de propósito -- é o mesmo tamanho medido (tokens),
    a variável que muda é o modelo, e distinguir 4 modelos por matiz estouraria o limite de 3
    cores categóricas; marcador + rótulo no fim da linha já bastam para identificar qual linha
    é de qual modelo (a mesma lógica de custo_versus_acerto em gerar_graficos.py, que
    identifica os 6 modelos por texto, não por cor). Como a cópia de L0 é idêntica para todos
    os modelos (base_conhecimento/ nunca é escrita pela Fase 3), a linha tracejada é o L0 do
    primeiro modelo que tiver a versão 0."""
    series = _series_fig_15(resumo)
    modelos = _ordenar_modelos(series)
    if not modelos:
        print("  15-fase3-crescimento-da-biblioteca: sem dado")
        return

    fig, ax = _base(9.4, 5.4)
    marcadores = ("o", "s", "^", "D", "P", "X")
    l0_valores = []
    for i, modelo in enumerate(modelos):
        xs = [versao for versao, _ in series[modelo]]
        ys = [tokens for _, tokens in series[modelo]]
        if xs[0] == 0:
            l0_valores.append(ys[0])
        ax.plot(xs, ys, color=SERIES[0], marker=marcadores[i % len(marcadores)],
               markersize=6, linewidth=1.6, zorder=3)
        ax.text(xs[-1] + 0.08, ys[-1], _curto(modelo), color=TINTA_2, fontsize=8, va="center")

    if l0_valores:
        base = l0_valores[0]
        ax.axhline(base, color=TINTA_2, linestyle="--", linewidth=1.2, zorder=2)
        ax.text(0, base, " L0 (biblioteca original)", color=TINTA_2, fontsize=7.5,
               va="bottom")

    ax.set_xticks(range(4))
    ax.set_xticklabels([f"L{e}" for e in range(4)])
    ax.set_xlim(-0.3, 3.9)
    ax.set_xlabel("versão da biblioteca", color=TINTA_2, fontsize=9)
    ax.set_ylabel("tokens estimados (texto renderizado)", color=TINTA_2, fontsize=9)
    _titular(ax, "Tamanho da biblioteca de cada modelo por versão",
            "Texto renderizado que entra no prompt, por versão fechada; tracejado marca o "
            "tamanho original (L0), igual para todos os modelos")
    _salvar(fig, "15-fase3-crescimento-da-biblioteca")


# --------------------------------------------------------------------------- figura 16

def fig_16(comparacao: dict) -> None:
    """! Alteração de IA - Revisar: figura 16 -- barras agrupadas por modelo, 5 barras em
    RAMPA[1:6] (2-A linear no Ryzen · 2-B sem biblioteca · 2-B recuperada · Fase 3 original ·
    Fase 3 editada), altura = acerto da causa raiz em nos_90; 'sem dado' onde o modelo não
    tem aquela coluna.
    ! Motivo: é o gráfico que resume as três fases de teste numa figura só -- a tabela de
    texto (comparacao_fases.md) tem as mesmas 5 colunas mais o IC de Wilson, mas só o gráfico
    deixa visível de relance qual fase deu o maior salto para cada modelo. RAMPA[1:6] (e não
    SERIES) porque são 5 categorias na mesma figura -- acima do limite de 3 matizes -- e a
    ordem das fases (mais clara a mais escura) é cronológica, então o degradê carrega
    informação de ordem que 5 cores arbitrárias não teriam."""
    por_modelo = comparacao.get("por_modelo", {})
    modelos = _ordenar_modelos(por_modelo)
    if not modelos:
        print("  16-comparacao-entre-fases: sem dado")
        return

    fig, ax = _base(10.6, 5.2)
    n = len(COLUNAS_COMPARACAO)
    largura = 0.8 / n
    for i, coluna in enumerate(COLUNAS_COMPARACAO):
        pos = [x + (i - (n - 1) / 2) * (largura + 0.01) for x in range(len(modelos))]
        vals = []
        for modelo in modelos:
            bloco = (por_modelo.get(modelo, {}).get("nos_90") or {}).get(coluna)
            vals.append(bloco["acerto_pct"] if bloco else None)
        pos_ok = [p for p, v in zip(pos, vals) if v is not None]
        val_ok = [v for v in vals if v is not None]
        barras = ax.bar(pos_ok, val_ok, width=largura, color=RAMPA[1 + i], zorder=3,
                        label=ROTULO_COLUNA[coluna])
        _rotular(ax, barras)
        for p, v in zip(pos, vals):
            if v is None:
                ax.text(p, 2, "sem dado", ha="center", va="bottom", fontsize=7,
                        color=TINTA_2, style="italic", rotation=90)

    ax.set_xticks(range(len(modelos)))
    ax.set_xticklabels([_curto(m) for m in modelos], rotation=20, ha="right")
    ax.set_ylim(0, 112)
    ax.set_yticks(range(0, 101, 20))
    ax.yaxis.set_major_formatter(PercentFormatter())
    leg = ax.legend(frameon=False, fontsize=9, ncols=n, loc="upper center",
                    bbox_to_anchor=(0.5, -0.24))
    for t in leg.get_texts():
        t.set_color(TINTA_2)
    _titular(ax, "Comparação entre as três fases de teste",
            "2-A medida no Ryzen (achado 4.26: o tempo não reproduz entre máquinas, o acerto "
            "sim) · 2-B e Fase 3 no notebook i5-alvo")
    _salvar(fig, "16-comparacao-entre-fases")


# --------------------------------------------------------------------------- figura 17

# ! Alteração de IA - Revisar: candidatos de deslocamento (dx, dy, em pontos tipográficos)
# do rótulo em relação ao ponto, na ordem em que _espalhar_rotulos os tenta: os 4 quadrantes
# colados ao ponto, depois os mesmos 4 uma linha mais longe, os dois lados na horizontal, e
# assim por diante -- onda final (item 9).
# ! Motivo: com os dados reais do piloto, o deslocamento fixo em 4 quadrantes alternados da
# versão anterior deixou "q2.5:7b · 2-B A0" por cima de "q2.5-coder:3b · F3 L0" e o
# aglomerado dos 1.5b (2-A, 2-B A0, 2-B A2, fp16, q8_0) ilegível: a alternância só evita a
# colisão entre pontos CONSECUTIVOS na ordem de custo, não entre vizinhos no plano.
DESLOCAMENTOS_ROTULO = (
    (9, 11), (9, -15), (-9, 11), (-9, -15),
    (9, 24), (9, -28), (-9, 24), (-9, -28),
    (14, 0), (-14, 0),
    (9, 37), (9, -41), (-9, 37), (-9, -41),
    (9, 50), (-9, 50), (9, -54), (-9, -54),
)
# Largura média de um caractere da fonte, em frações do tamanho da fonte (DejaVu Sans a
# 6,6 pt: medido ~0,55-0,60 em; 0,58 é conservador para o texto não sair mais largo que a
# caixa calculada).
LARGURA_POR_CARACTERE = 0.58
# Raio do marcador da figura 17 em pontos (scatter s=100 é a ÁREA, em pt²: diâmetro 10 pt).
RAIO_MARCADOR_PT = 5.0


def _caixa_rotulo(ancora: tuple[float, float], dx: float, dy: float, largura: float,
                  altura: float) -> tuple[float, float, float, float]:
    """! Alteração de IA - Revisar: (x0, y0, x1, y1), em pontos, da caixa que um rótulo de
    `largura` x `altura` ocupa quando ancorado em `ancora` com deslocamento (dx, dy): à
    esquerda do texto se dx > 0 (ha='left'), à direita se dx < 0 (ha='right'), centrado
    verticalmente (va='center') -- exatamente como fig_17 chama ax.annotate.
    ! Motivo: é a mesma conta para posicionar (em _espalhar_rotulos) e para o teste conferir
    que duas caixas não se cruzam; escrita duas vezes, uma diferença de âncora faria o teste
    aprovar uma sobreposição real."""
    x, y = ancora
    x0 = x + dx if dx > 0 else x + dx - largura
    y0 = y + dy - altura / 2
    return (x0, y0, x0 + largura, y0 + altura)


def _caixas_se_cruzam(a: tuple[float, float, float, float],
                      b: tuple[float, float, float, float]) -> bool:
    """! Alteração de IA - Revisar: True se os dois retângulos (x0, y0, x1, y1) têm área em
    comum (encostar pela borda não conta).
    ! Motivo: é o teste de colisão de _espalhar_rotulos; separado para o teste automatizado
    usar a mesma regra."""
    return a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]


def _area_cruzada(a: tuple[float, float, float, float],
                  b: tuple[float, float, float, float]) -> float:
    """! Alteração de IA - Revisar: área da interseção de dois retângulos (0 se não cruzam).
    ! Motivo: quando nenhum candidato de DESLOCAMENTOS_ROTULO fica livre (aglomerado muito
    denso), _espalhar_rotulos escolhe o que menos invade os outros, em vez de desistir."""
    largura = min(a[2], b[2]) - max(a[0], b[0])
    altura = min(a[3], b[3]) - max(a[1], b[1])
    return largura * altura if largura > 0 and altura > 0 else 0.0


def _espalhar_rotulos(ancoras: list[tuple[float, float]], larguras: list[float],
                      altura: float, candidatos=DESLOCAMENTOS_ROTULO,
                      raio_marcador: float = RAIO_MARCADOR_PT) -> list[tuple[int, int]]:
    """! Alteração de IA - Revisar: escolhe, para cada ponto (em pontos tipográficos), o
    primeiro deslocamento de `candidatos` cuja caixa de rótulo não cruza nenhum marcador
    nem nenhuma caixa já posta; se nenhum ficar livre, o de menor área invadida. Devolve os
    (dx, dy) na ordem das âncoras -- onda final (item 9).
    ! Motivo: ver DESLOCAMENTOS_ROTULO. Escolhe o primeiro deslocamento livre na ordem recebida, sem voltar atrás (fig_17 passa
    os pontos em ordem de custo crescente), o que a torna determinística: a mesma
    comparacao_fases.json dá sempre a mesma figura. Um ponto isolado fica com o primeiro
    candidato (acima e à direita), como na versão anterior."""
    ocupadas = [(x - raio_marcador, y - raio_marcador, x + raio_marcador, y + raio_marcador)
                for x, y in ancoras]
    saida: list[tuple[int, int]] = []
    for ancora, largura in zip(ancoras, larguras):
        caixas = [(dx, dy, _caixa_rotulo(ancora, dx, dy, largura, altura))
                  for dx, dy in candidatos]
        livre = next(((dx, dy, caixa) for dx, dy, caixa in caixas
                      if not any(_caixas_se_cruzam(caixa, o) for o in ocupadas)), None)
        if livre is None:
            livre = min(caixas, key=lambda c: sum(_area_cruzada(c[2], o) for o in ocupadas))
        dx, dy, caixa = livre
        ocupadas.append(caixa)
        saida.append((dx, dy))
    return saida


def fig_17(comparacao: dict) -> None:
    """! Alteração de IA - Revisar: figura 17 -- dispersão custo (segundos/caso, mediana) x
    acerto, um ponto por (modelo, fase) das mesmas 5 colunas da figura 16; rótulo
    `_curto(modelo) · fase` em cada ponto, com uma linha fina ligando o rótulo ao ponto e a
    direção do deslocamento alternando em 4 quadrantes (na ordem de leitura por custo
    crescente); a coluna 2-A sai com marcador VAZADO (sem preenchimento) para diferenciar a
    máquina (Ryzen) sem inventar uma quarta cor.
    ! Motivo: a figura 16 mostra o acerto isolado; esta mostra o preço pago por ele -- o canto
    superior esquerdo (barato e certeiro) é onde qualquer modelo/fase quer estar. Um marcador
    vazado em vez de uma cor nova para a 2-A segue a mesma regra de 'identidade por
    forma/texto, não por matiz' de custo_versus_acerto e prefill_versus_acerto em
    gerar_graficos.py. Com 4 modelos x 5 fases (20 pontos, o dobro do maior gráfico
    equivalente da 2-B, que tem 6 modelos x 1 ponto), um deslocamento fixo (sempre para cima e
    à direita, como em custo_versus_acerto) empilha os rótulos das colunas 2B_A2/F3_L0 do
    MESMO modelo -- que ficam perto uma da outra de propósito (é o par que a Tabela de
    pareamentos de comparar_fases.py mede) -- e o texto de uma linha invade o de outra. Alternar
    a direção a cada ponto (percorridos em ordem de custo, então vizinhos no gráfico tendem a
    cair em posições consecutivas desta lista) espalha os rótulos ao redor do grupo em vez de
    empilhá-los todos no mesmo canto, e a linha fina (cor da grade, não uma cor nova) deixa
    rastreável qual rótulo é de qual ponto mesmo quando dois ficam próximos. Quando dois pontos
    CONSECUTIVOS nesta ordem são do MESMO modelo e caem a poucos pontos de distância um do
    outro (Fix round 1 da revisão: item 'minor'), o segundo rótulo empilha diretamente abaixo do
    primeiro (mesmo lado, mesmo `ha`) em vez de girar para o quadrante seguinte -- girar nesse
    caso desenharia duas linhas finas se CRUZANDO entre os dois pontos vizinhos, mais difícil de
    seguir do que uma pilha reta.

    ! Alteração de IA - Revisar (onda final, item 9): a alternância de quadrantes e a pilha
    por modelo foram substituídas por _espalhar_rotulos, que posiciona cada rótulo em pontos
    tipográficos testando colisão com os marcadores e com os rótulos já postos (candidatos em
    DESLOCAMENTOS_ROTULO). A conversão de dados para pontos usa ax.transData depois de fixar
    os limites dos eixos, e a largura do texto é estimada por LARGURA_POR_CARACTERE.
    ! Motivo: conferido com a comparacao_fases.json do piloto (4 modelos da Fase 3 + os da
    2-A/2-B, 27 pontos), a regra anterior deixou "q2.5:7b · 2-B A0" sobre "q2.5-coder:3b ·
    F3 L0" e os cinco pontos dos 1.5b no canto inferior esquerdo com os rótulos uns sobre os
    outros -- ela só olhava o ponto anterior na ordem de custo, e vizinhos no plano não são
    necessariamente consecutivos nessa ordem."""
    por_modelo = comparacao.get("por_modelo", {})
    modelos = _ordenar_modelos(por_modelo)
    if not modelos:
        print("  17-custo-versus-acerto-tres-fases: sem dado")
        return

    pontos = []
    for modelo in modelos:
        bloco = por_modelo.get(modelo, {}).get("nos_90") or {}
        for coluna in COLUNAS_COMPARACAO:
            col = bloco.get(coluna)
            if col and col.get("segundos_mediana") is not None and col.get("acerto_pct") is not None:
                pontos.append((modelo, coluna, col["segundos_mediana"], col["acerto_pct"]))
    if not pontos:
        print("  17-custo-versus-acerto-tres-fases: sem dado")
        return
    pontos.sort(key=lambda p: (p[2], p[3]))

    fig, ax = _base(11.6, 6.8)
    ax.grid(color=GRADE, linewidth=0.8, zorder=0)
    for modelo, coluna, x, y in pontos:
        vazado = coluna == "2A_linear_ryzen"
        ax.scatter(x, y, s=100, facecolor="none" if vazado else SERIES[0],
                  edgecolor=SERIES[0], linewidth=1.6, zorder=3)

    ax.set_xlabel("segundos por caso (mediana)", color=TINTA_2, fontsize=9)
    ax.set_ylabel("acerto da causa raiz", color=TINTA_2, fontsize=9)
    ax.set_ylim(0, 100)
    ax.yaxis.set_major_formatter(PercentFormatter())

    # Os limites dos eixos têm de estar fechados ANTES de converter os pontos para a escala
    # em que os rótulos são medidos (pontos tipográficos): get_xlim() força o autoscale do x.
    ax.get_xlim()
    fonte = 6.6
    textos = [f"{_curto(modelo)} · {ROTULO_COLUNA[coluna]}" for modelo, coluna, _, _ in pontos]
    em_pixels = ax.transData.transform([(x, y) for _, _, x, y in pontos])
    ancoras = [(float(px) * 72 / fig.dpi, float(py) * 72 / fig.dpi) for px, py in em_pixels]
    larguras = [len(texto) * fonte * LARGURA_POR_CARACTERE for texto in textos]
    deslocamentos = _espalhar_rotulos(ancoras, larguras, fonte * 1.25)
    for (modelo, coluna, x, y), texto, (dx, dy) in zip(pontos, textos, deslocamentos):
        ax.annotate(texto, (x, y), textcoords="offset points", xytext=(dx, dy),
                   fontsize=fonte, ha="left" if dx > 0 else "right", va="center",
                   color=TINTA_2,
                   arrowprops=dict(arrowstyle="-", color=GRADE, linewidth=0.7,
                                   shrinkA=0, shrinkB=3))
    _titular(ax, "Custo contra acerto nas três fases",
            "Marcador vazado = 2-A (Ryzen, tempo não comparável às demais) · canto superior "
            "esquerdo é o melhor")
    _salvar(fig, "17-custo-versus-acerto-tres-fases")


# ------------------------------------------------------------------------------- CLI

# ! Alteração de IA - Revisar: linha de comando -- --saida escolhe a pasta de resultados da
# Fase 3 (ver caminhos.fase3) e sobrescreve gerar_graficos.GRAFICOS para o piloto (que grava
# os próprios gráficos dentro da pasta dele, e não na pasta comum das figuras 01-11/12-17
# oficiais -- ver o comentário de caminhos.fase3).
# ! Motivo: --saida fase3 (o padrão) é a corrida oficial, cujos gráficos entram na sequência
# única 01-17 do TCC; qualquer outro nome (ex.: fase3_piloto) é descartável e não deve se
# misturar com essa sequência nem sobrescrever as figuras da corrida oficial se rodado por
# engano.
def main() -> None:
    ap = argparse.ArgumentParser(
        description="Gera as figuras 12-17 (Fase 3 e comparação entre fases) a partir de "
                    "resumo_fase3.json e comparacao_fases.json.")
    ap.add_argument("--saida", default="fase3",
                    help="subpasta dos resultados da Fase 3 (ver caminhos.fase3)")
    args = ap.parse_args()

    print(caminhos.descricao())
    c3 = caminhos.fase3(args.saida)
    if not c3["resumo"].exists() or not c3["comparacao"].exists():
        print(f"resumo_fase3.json ou comparacao_fases.json não encontrado em {c3['raiz']}. "
             "Rode avaliar_fase3.py e comparar_fases.py primeiro.")
        return
    resumo = json.loads(c3["resumo"].read_text(encoding="utf-8"))
    comparacao = json.loads(c3["comparacao"].read_text(encoding="utf-8"))

    gg.GRAFICOS = c3["graficos"]
    gg.GRAFICOS.mkdir(parents=True, exist_ok=True)

    print(f"Gerando gráficos em {gg.GRAFICOS}:")
    fig_12(resumo)
    fig_13(resumo)
    fig_14(resumo)
    fig_15(resumo)
    fig_16(comparacao)
    fig_17(comparacao)
    print(f"\nGráficos em {gg.GRAFICOS}")


if __name__ == "__main__":
    main()
