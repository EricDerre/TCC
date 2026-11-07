#!/usr/bin/env python3
# ! Alteração de IA - Revisar: script novo (05/11/2026) que gera as figuras do README, do documento do TCC e do anexo técnico em
# `Documentacao/figuras/` e, ao lado delas, `dados-das-figuras.md`, com a tabela de cada figura. Tudo é lido dos JSON de
# `resultados_alvo/`; nenhum valor é digitado aqui.
# ! Motivo: o Eric pediu (05/11/2026) a documentação principal com gráficos e a explicação de como lê-los, no lugar de dados
# soltos no texto. As figuras 01 a 18 de `resultados_alvo/graficos/` foram feitas para quem já conhece a sigla de cada condição
# (A0, A2, L0, L3) e param na Fase 3; estas falam com quem chega agora e cobrem as Fases 3-B e 4. Os registros oficiais não são
# regravados: a saída é só `Documentacao/figuras/`.
"""Figuras para quem lê a documentação principal, uma pergunta por figura, com os dados de cada uma em `dados-das-figuras.md`.

Uso (com a venv do AgenteCore, que tem o matplotlib):
    python gerar_figuras_documentos.py           # grava as figuras e o .md
    python gerar_figuras_documentos.py --check   # só confere se o .md gravado bate com os JSON (não precisa do matplotlib)

Paleta validada com `dataviz/scripts/validate_palette.js` no fundo #fcfcfb: passa nas separações para daltonismo; o verde e o
amarelo ficam abaixo de 3:1 de contraste, por isso toda série leva rótulo direto ou legenda ao lado do valor.
"""
from __future__ import annotations

import argparse
import json
import statistics
import sys
import textwrap
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RES = AQUI / "resultados_alvo"
RAIZ = AQUI.parent.parent.parent
SAIDA = RAIZ / "Documentacao" / "figuras"
MD = SAIDA / "dados-das-figuras.md"

SUPERFICIE = "#fcfcfb"
TINTA = "#0b0b0b"
TINTA_2 = "#52514e"
GRADE = "#e5e4e0"
NEUTROS = ["#8b8a85", "#b5b4ae", "#d9d8d3"]
AZUL, LARANJA, VERDE, AMARELO = "#2a78d6", "#eb6834", "#1baf7a", "#eda100"
RAMPA = ["#c3d9f4", "#8fb9e9", "#5b98dd", "#2a78d6", "#1b5296"]
COR_MODELO = {"qwen2.5:7b": AZUL, "granite4.2:8b": LARANJA, "qwen2.5-coder:7b": VERDE, "qwen2.5-coder:3b": AMARELO}
MODELOS = list(COR_MODELO)

NOME_CENARIO = {
    "contrato-malformed_json": "Resposta cortada no meio", "contrato-field_missing": "Campo sumiu da resposta",
    "contrato-field_renamed": "Campo mudou de nome", "contrato-type_drift": "Campo mudou de tipo",
    "contrato-escala_ou_unidade_errada": "Preço na escala errada", "contrato-error_500": "API devolve erro 500",
    "localizador-front-busca": "Busca", "localizador-front-admin-login": "Login do administrador",
    "localizador-front-admin-produtos": "Lista de produtos do administrador", "localizador-front-cliente-reserva": "Reserva do cliente",
}
NOME_CLASSE = {1: "Léxica", 2: "Sintática", 3: "Semântica", 4: "Tradução", 5: "Runtime", 6: "Efeito"}
NOME_SINAL = {
    "por_gatilho": "Divergência, contada só quando há gatilho", "regra_b_por_gatilho": "Regra alternativa (ficha 39 b), só por gatilho",
    "selo_baixo": "Selo de confiança baixo", "remocao_ou_troca": "Tirar ou trocar o verbete citado muda a resposta",
    "regra_b": "Regra alternativa (ficha 39 b), em todos os casos", "qualquer": "Qualquer um dos sinais principais",
    "sem_documentacao": "Sem documentação, a resposta muda", "divergencia": "Divergência registrada, como rodou na corrida 22",
    "falha": "Conferência em código não passa", "repeticao_mudou": "Repetir a pergunta muda a resposta",
}
NOME_FORA = {"armada pelo harness (ficha 29)": "Falha armada pelo próprio teste", "sem modo para a causa dado_desatualizado": "Sem modo na API para a causa", "sem tela": "A falha não passa pela tela"}
NOME_REJEICAO = {
    "palavra_chave_invalida": "palavra-chave inválida", "duplicada": "repetida", "id_repetido": "identificador repetido",
    "sem_evidencia_do_caso": "sem evidência no caso", "mensagem_nao_encontrada_no_codigo": "mensagem que não existe no código",
    "redundante": "redundante", "texto_nao_atomico": "mistura mais de um assunto", "texto_de_origem_proibida": "copia a resposta da API",
}


def _j(rel: str) -> dict:
    return json.loads((RES / rel).read_text(encoding="utf-8"))


def _modelo_curto(m: str) -> str:
    return m


def _num(v, casas: int = 1) -> str:
    return f"{v:.{casas}f}".replace(".", ",")


def coletar() -> dict[str, dict]:
    """Lê os JSON e devolve, por figura, o título, a fonte e a tabela de dados. Só biblioteca padrão."""
    cal = _j("fase4/calibracao.json")
    # ! Alteração de IA - Revisar: (05/11/2026, decisão 90) as figuras da tela e dos cenários passam às leituras vigentes, 18c e 21c; a 18 e a 18b ficam como as barras de antes.
    # ! Motivo: a decisão 90 diz que as leituras novas passam a valer quando as corridas rodarem, e o README mostra o resultado vigente.
    # ! Alteração de IA - Revisar: (06/11/2026, decisões 97 e 98) as figuras da tela e dos cenários passam à 18d e à 21d, e entram os inéditos (18e); a média de antes do corte continua a da 21b.
    # ! Motivo: a regra R2 fechou na 18d, e os inéditos são a conferência em casos que a busca nunca viu; o README mostra o resultado vigente, com o caminho até ele.
    t1, t2, t3, t4, ti = _j("fase4/tela.json"), _j("fase4/tela_v2.json"), _j("fase4/tela_v3.json"), _j("fase4/tela_v4.json"), _j("fase4/tela_ineditos.json")
    cen, cen_ant = _j("fase4/cenarios_v4.json"), _j("fase4/cenarios_v2.json")
    bib = _j("fase4/biblioteca.json")
    tri = _j("fase4/trilha.json")
    cur = _j("fase4/cura.json")
    rep, rep_i = _j("fase4/reproducibilidade.json"), _j("fase4/reproducibilidade_ineditos.json")
    an = _j("fase3/analise_fase3b.json")
    cf = _j("fase3/comparacao_fases.json")
    dm = _j("fase3/decisao_modelo.json")
    figs: dict[str, dict] = {}

    # o agente, em passos: os únicos dados são o k escolhido e o modelo
    figs["como-o-agente-trabalha"] = {
        "titulo": "Como o agente trabalha", "fonte": "`fase4/calibracao.json` (`k_escolhido`, `metadados.modelo`)",
        "cab": ["Dado", "Valor"], "linhas": [["Verbetes entregues ao modelo (k)", cal["k_escolhido"]], ["Modelo", cal["metadados"]["modelo"]]],
    }
    # documentação e acerto: os 36 casos de avaliação, que o modelo nunca usou para aprender
    etapas = [("2B_A0", "Sem documentação"), ("2B_A2", "Biblioteca escrita à mão"), ("F3_L1", "Biblioteca escrita pelo modelo")]
    figs["documentacao-e-acerto"] = {
        "titulo": "O que a documentação fez pelo acerto", "fonte": "`fase3/comparacao_fases.json` (`nos_36_avaliacao`: `2B_A0`, `2B_A2`, `F3_L1`, `acerto_pct`)",
        "cab": ["Modelo"] + [n for _, n in etapas],
        "linhas": [[m] + [cf["por_modelo"][m]["nos_36_avaliacao"][e]["acerto_pct"] for e, _ in etapas] for m in MODELOS],
    }
    # escolha do modelo
    ic = {(c["modelo"], c["biblioteca_epoca"]): c["ic95_bootstrap"] for c in dm["bootstrap"]["nos_36"]["combos"]}
    venc = dm["regra_36"]["vencedor"]
    figs["escolha-do-modelo"] = {
        "titulo": "Por que o qwen2.5:7b com a primeira biblioteca dele", "fonte": "`fase3/decisao_modelo.json` (`regra_36.ranking`, `bootstrap.nos_36`)",
        "cab": ["Modelo", "Biblioteca", "Acurácia balanceada (%)", "Segundos por caso (mediana)", "De (%)", "Até (%)", "Escolhido"],
        "linhas": [[r["modelo"], f'L{r["biblioteca_epoca"]}', r["acuracia_balanceada_36"], r["segundos_mediana_36"], *ic[(r["modelo"], r["biblioteca_epoca"])],
                    "sim" if (r["modelo"], r["biblioteca_epoca"]) == (venc["modelo"], venc["biblioteca_epoca"]) else ""] for r in dm["regra_36"]["ranking"]],
    }
    # troca cruzada
    cel = {(c["leitor"], c["origem"], c["biblioteca_epoca"]): c for c in an["cruzada"]["celulas"]}
    doador = an["metadados"]["doador"]
    linhas_cz = [[doador, cel[(doador, "fase3", 0)]["acertos"], cel[(doador, "fase3", 1)]["acertos"], cel[(doador, "fase3", 1)]["n"], "0.34.0"]]
    for leitor in an["metadados"]["leitores"]:
        linhas_cz.append([leitor, cel[(leitor, "ponte", 0)]["acertos"], cel[(leitor, "cruzada", 1)]["acertos"], cel[(leitor, "cruzada", 1)]["n"], cel[(leitor, "cruzada", 1)]["versao_ollama"]])
    figs["quem-le-a-biblioteca"] = {
        "titulo": "O que muda quando outro modelo lê a biblioteca", "fonte": "`fase3/analise_fase3b.json` (`cruzada.celulas`)",
        "cab": ["Quem lê", "Casos certos com a biblioteca original", f"Casos certos com a biblioteca escrita pelo {doador}", "De", "Ollama"], "linhas": linhas_cz,
    }
    # casos inéditos
    ined = {(c["modelo"], c["biblioteca_epoca"]): c for c in an["ineditos"]["linhas"]}
    figs["casos-ineditos"] = {
        "titulo": "O ganho se repete em casos nunca vistos?", "fonte": "`fase3/analise_fase3b.json` (`cruzada.celulas`, origem `fase3`; `ineditos.linhas`)",
        "cab": ["Biblioteca", "Casos de avaliação certos", "Casos inéditos certos", "De"],
        "linhas": [[f"L{e}", cel[(doador, "fase3", e)]["acertos"], ined[(doador, e)]["acertos"], ined[(doador, e)]["n"]] for e in (0, 1, 3)],
    }
    # selo
    sel = {s["selo"]: s for s in cal["por_selo"]}
    figs["selo-de-confianca"] = {
        "titulo": "Quando o agente diz que tem certeza, ele acerta?", "fonte": "`fase4/calibracao.json` (`por_selo`, corrida 16, com k = 3)",
        "cab": ["Selo", "Casos", "Certos", "Errados", "Erro (%)"],
        "linhas": [[n, sel[s]["casos"], sel[s]["certos"], sel[s]["errados"], sel[s]["erro_pct"]] for s, n in (("alto", "Alto"), ("medio", "Médio"), ("baixo", "Baixo"))],
    }
    # reprodução
    def _fora(r: dict) -> dict:
        return {x["motivo"]: x["casos"] for x in r["fora_por_motivo"]}
    motivos = list(NOME_FORA)
    figs["reproducao-na-tela"] = {
        "titulo": "Quantos casos a tela consegue mostrar", "fonte": "`fase4/reproducibilidade.json` e `reproducibilidade_ineditos.json` (`resumo`, `fora_por_motivo`, corrida 17)",
        "cab": ["Conjunto", "Casos", "Reproduzem na tela"] + [NOME_FORA[m] for m in motivos],
        "linhas": [["Casos de avaliação", rep["resumo"]["casos"], rep["resumo"]["reproduzem"]] + [_fora(rep).get(m, 0) for m in motivos],
                   ["Casos inéditos da ficha 27", rep_i["resumo"]["casos"], rep_i["resumo"]["reproduzem"]] + [_fora(rep_i).get(m, 0) for m in motivos]],
    }
    # tela e caso escrito
    figs["tela-e-caso-escrito"] = {
        "titulo": "O agente acerta tanto lendo da tela?", "fonte": "`fase4/tela.json`, `tela_v2.json`, `tela_v3.json`, `tela_v4.json` e `tela_ineditos.json` (`resumo`, corridas 18, 18b, 18c, 18d e 18e)",
        "cab": ["Leitura", "Casos certos", "De"],
        "linhas": [["Caso escrito (corrida 18d)", t4["resumo"]["acerto_fixture"], t4["resumo"]["casos"]],
                   ["Tela, com os sinais novos da busca (corrida 18d)", t4["resumo"]["acerto_tela"], t4["resumo"]["casos"]],
                   ["Tela, com o prompt dentro do limite (corrida 18c)", t3["resumo"]["acerto_tela"], t3["resumo"]["casos"]],
                   ["Tela, com o caso ao vivo revisado (corrida 18b)", t2["resumo"]["acerto_tela"], t2["resumo"]["casos"]],
                   ["Tela, primeira versão do caso ao vivo (corrida 18)", t1["resumo"]["acerto_tela"], t1["resumo"]["casos"]],
                   ["Inéditos, caso escrito (corrida 18e)", ti["resumo"]["acerto_fixture"], ti["resumo"]["casos"]],
                   ["Inéditos, tela (corrida 18e)", ti["resumo"]["acerto_tela"], ti["resumo"]["casos"]]],
    }
    # prompt e limite: os tokens medidos em cada corrida, antes e depois do corte
    # ! Alteração de IA - Revisar: (05/11/2026, decisão 90) a figura passa a mostrar os tokens medidos nas corridas, antes e depois do corte, no lugar da estimativa dos cortes possíveis.
    # ! Motivo: a estimativa servia para decidir o corte; com as corridas 18c e 21c rodadas, o que vale é a medida do próprio Ollama.
    limite = t3["prompt_contra_calibracao"]["limite_mais_10_pct"]

    def tokens_de(pasta: str) -> list[int]:
        arq = RES / pasta / "qwen2.5_7b" / "diagnosticos__cenarios.jsonl"
        return [json.loads(x)["tokens_entrada"] for x in arq.read_text(encoding="utf-8").splitlines() if x.strip()]

    def linha_prompt(grupo: str, rotulo: str, tokens: list[int]) -> list:
        return [grupo, rotulo, min(tokens), statistics.median(tokens), max(tokens), sum(1 for x in tokens if x > limite), len(tokens)]

    figs["prompt-e-limite"] = {
        "titulo": "O prompt na tela cabe no limite?", "fonte": f"tokens de entrada medidos em `fase4/tela_v2.json`, `tela_v3.json`, `tela_v4.json` e `tela_ineditos.json` (`casos`) e em `fase4_ensaio_v2/`, `fase4_ensaio_v3/` e `fase4_ensaio_v4/` (`diagnosticos__cenarios.jsonl`); limite de {limite} tokens: maior prompt da calibração mais 10%",
        "cab": ["Conjunto", "Corrida", "Menor", "Mediana", "Maior", "Acima do limite", "De"],
        "linhas": [linha_prompt("Casos lidos da tela", "Antes do corte (18b)", [c["tokens_entrada_tela"] for c in t2["casos"]]),
                   linha_prompt("Casos lidos da tela", "Depois do corte (18c)", [c["tokens_entrada_tela"] for c in t3["casos"]]),
                   linha_prompt("Casos lidos da tela", "Com os sinais da busca (18d)", [c["tokens_entrada_tela"] for c in t4["casos"]]),
                   linha_prompt("Casos lidos da tela", "Inéditos, com os sinais da busca (18e)", [c["tokens_entrada_tela"] for c in ti["casos"]]),
                   linha_prompt("10 cenários", "Antes do corte (21b)", tokens_de("fase4_ensaio_v2")),
                   linha_prompt("10 cenários", "Depois do corte (21c)", tokens_de("fase4_ensaio_v3")),
                   linha_prompt("10 cenários", "Com os sinais da busca (21d)", tokens_de("fase4_ensaio_v4"))],
        "limite": limite,
    }
    # tempo por cenário
    figs["tempo-por-cenario"] = {
        "titulo": "Quanto tempo o agente leva, cenário a cenário", "fonte": "`fase4/cenarios_v4.json` (`por_cenario`, `geral`, corrida 21d) e `fase4/cenarios_v2.json` (`geral`, corrida 21b, a média de antes do corte)",
        "cab": ["Cenário", "Tipo", "Segundos da detecção ao resultado", "Chegou ao resultado", "Execuções"],
        "linhas": [[NOME_CENARIO[c["cenario"]], c["tipo"], c["mttr_media_s"], c["sucessos"], c["n"]] for c in cen["por_cenario"]],
        "por_tipo": {t["tipo"]: t["mttr_media_s"] for t in cen["por_tipo"]}, "geral": cen["geral"], "media_anterior": cen_ant["geral"]["mttr_media_s"],
    }
    # funil da biblioteca: `fechamento.json` da produção guarda o que ficou depois da revisão do lote (relatório da Fase 4, seção 7)
    r = bib["resumo"]
    fechamento = json.loads((AQUI.parent / "biblioteca_producao" / "fechamento.json").read_text(encoding="utf-8"))
    mantidas = fechamento["mantidas"] if isinstance(fechamento["mantidas"], int) else len(fechamento["mantidas"])
    fase3_top = sorted(bib["rejeicoes"]["fase3"].items(), key=lambda x: -x[1])[:3]
    p5_top = sorted(bib["rejeicoes"]["p5"].items(), key=lambda x: -x[1])[:3]
    figs["funil-da-biblioteca"] = {
        "titulo": "O que acontece com o que o agente propõe", "fonte": "`fase4/biblioteca.json` (`resumo`, `rejeicoes`, corrida 20) e `biblioteca_producao/fechamento.json` (`mantidas`)",
        "cab": ["Etapa", "Propostas que seguem", "Barradas nesta etapa"],
        "linhas": [["Propostas do modelo", r["propostas"], 0],
                   ["Passam pelo validador da Fase 3", r["propostas"] - r["recusadas_fase3"], r["recusadas_fase3"]],
                   ["Passam pelos filtros da Fase 4", r["propostas"] - r["recusadas_fase3"] - r["recusadas_p5"], r["recusadas_p5"]],
                   ["Entram no lote (uma ficou segurada para revisão)", r["aceitas"], r["para_revisao"]],
                   ["Ficam na biblioteca depois da revisão", mantidas, r["aceitas"] + r["para_revisao"] - mantidas]],
        "motivos": {"fase3": [(NOME_REJEICAO.get(k, k), v) for k, v in fase3_top], "p5": [(NOME_REJEICAO.get(k, k), v) for k, v in p5_top]},
        "propostas": r["propostas"],
    }
    # sinais da trilha
    sinais = sorted(tri["sinais"], key=lambda s: -s["produto"])
    figs["sinais-da-trilha"] = {
        "titulo": "Os sinais da trilha apontam os erros de verdade?", "fonte": "`fase4/trilha.json` (`sinais`, corrida 22)",
        "cab": ["Sinal", "Nota (TPR x TNR)", "Erros que pegou", "Erros", "Acertos que acusou", "Acertos"],
        "linhas": [[NOME_SINAL[s["sinal"]], round(s["produto"], 3), s["vp"], s["erros"], s["fp"], s["acertos"]] for s in sinais],
        "acaso": sinais[0]["acaso"], "oficial": NOME_SINAL["divergencia"],
    }
    # quantos verbetes
    figs["quantos-verbetes"] = {
        "titulo": "Entregar mais verbetes ao modelo ajuda?", "fonte": "`fase4/calibracao.json` (`por_k`, corrida 16)",
        "cab": ["Verbetes (k)", "Acurácia balanceada (%)", "Tamanho do prompt (tokens, mediana)", "Maior prompt (tokens)", "Segundos por caso (mediana)"],
        "linhas": [[x["k"], x["acuracia_balanceada_pct"], x["tokens_entrada_mediana"], x["tokens_entrada_max"], x["segundos_mediana"]] for x in cal["por_k"]],
    }
    # tela por classe
    figs["tela-por-classe"] = {
        "titulo": "Onde a leitura da tela perde acertos", "fonte": "`fase4/tela_v4.json` (`por_classe`, corrida 18d)",
        "cab": ["Classe de defeito", "Casos", "Certos na tela", "Certos no caso escrito"],
        "linhas": [[NOME_CLASSE[c["classe"]], c["casos"], c["acerto_tela"], c["acerto_fixture"]] for c in t4["por_classe"]],
    }
    # ! Alteração de IA - Revisar: (06/11/2026) a figura da corrida 24: certos e errados por classe de defeito, nos 36 inéditos da ficha 27.
    # ! Motivo: é a única medida da biblioteca final em casos que ela nunca viu, e a classe de tradução é onde ela mais erra.
    ined = _j("fase4/ineditos.json")
    figs["ineditos-por-classe"] = {
        "titulo": "E em casos que a biblioteca nunca viu?", "fonte": "`fase4/ineditos.json` (`por_classe`, `resumo`, `referencia`, corrida 24)",
        "cab": ["Classe de defeito", "Casos", "Certos", "Errados"],
        "linhas": [[NOME_CLASSE[c["classe"]], c["casos"], c["acertos"], c["erros"]] for c in ined["por_classe"]],
        "resumo": ined["resumo"], "referencia": ined["referencia"],
    }
    # onde vai o tempo
    tipos = {t["tipo"]: t for t in cen["por_tipo"]}
    figs["onde-vai-o-tempo"] = {
        "titulo": "Onde o tempo vai", "fonte": "`fase4/cura.json` (`resumo`, corrida 19), `fase4/tela_v4.json` (`resumo`, corrida 18d), `fase4/cenarios_v4.json` (`por_tipo`, corrida 21d)",
        "cab": ["Etapa", "Segundos (mediana)", "Usa o modelo"],
        "linhas": [["Cura de localizador só em código", cur["resumo"]["mttr_mediana_s"], "não"],
                   ["Diagnóstico de um caso escrito", t4["resumo"]["segundos_fixture_mediana"], "sim"],
                   ["Diagnóstico de um caso da tela", t4["resumo"]["segundos_tela_mediana"], "sim"],
                   ["Localizador, da detecção à reexecução", tipos["localizador"]["mttr_mediana_s"], "sim"],
                   ["Contrato, da detecção ao diagnóstico conferido", tipos["contrato"]["mttr_mediana_s"], "sim"]],
    }
    return figs


# ------------------------------------------------------------------------------------------------------ Markdown dos dados
def gerar_md(figs: dict[str, dict]) -> str:
    """A tabela de cada figura, para quem quer o número exato sem abrir o JSON."""
    saida = [
        "<!-- ! Alteração de IA - Revisar: arquivo GERADO por `Programacao/AgenteCore/experimentos/gerar_figuras_documentos.py` (05/11/2026); não editar à mão.",
        "     ! Motivo: cada figura da documentação principal precisa de uma tabela ao lado para quem quer o número exato; saindo do mesmo script, figura e tabela não divergem. -->",
        "# Dados das figuras", "",
        "Os números de cada figura de [`Documentacao/figuras/`](.), lidos dos registros em `Programacao/AgenteCore/experimentos/resultados_alvo/` pelo script `gerar_figuras_documentos.py`.", "",
    ]
    for nome, f in figs.items():
        saida += [f"## {f['titulo']}", "", f"[Figura]({nome}.png). Fonte: {f['fonte']}.", ""]
        saida.append("| " + " | ".join(str(c) for c in f["cab"]) + " |")
        saida.append("|" + "---|" * len(f["cab"]))
        for l in f["linhas"]:
            saida.append("| " + " | ".join(_num(c) if isinstance(c, float) else str(c) for c in l) + " |")
        saida.append("")
    return "\n".join(saida)


# ------------------------------------------------------------------------------------------------------ desenho
def desenhar(figs: dict[str, dict]) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Patch
    from matplotlib.lines import Line2D

    plt.rcParams.update({"font.family": "DejaVu Sans", "axes.titlelocation": "left"})

    def base(l=8.2, a=4.4):
        fig, ax = plt.subplots(figsize=(l, a), dpi=200)
        fig.patch.set_facecolor(SUPERFICIE)
        ax.set_facecolor(SUPERFICIE)
        limpar(ax)
        return fig, ax

    def limpar(ax, eixo="y"):
        ax.grid(axis=eixo, color=GRADE, linewidth=0.7, zorder=0)
        ax.set_axisbelow(True)
        for lado in ("top", "right"):
            ax.spines[lado].set_visible(False)
        for lado in ("left", "bottom"):
            ax.spines[lado].set_color(GRADE)
        ax.tick_params(colors=TINTA_2, labelsize=9, length=0)

    def titular(fig, titulo, sub=None):
        fig.suptitle(titulo, x=0.012, y=0.995, ha="left", va="top", fontsize=13, fontweight="bold", color=TINTA)
        if sub:
            fig.text(0.012, 0.995 - 0.058 * (4.4 / fig.get_figheight()), sub, ha="left", va="top", fontsize=9, color=TINTA_2)

    def topo(fig) -> float:
        """Fração da altura em que o gráfico termina: o título e o subtítulo ocupam a mesma altura em qualquer figura."""
        return 1 - 0.62 / fig.get_figheight()

    def salvar(fig, nome):
        fig.tight_layout(rect=(0, 0, 1, topo(fig)))
        SAIDA.mkdir(parents=True, exist_ok=True)
        fig.savefig(SAIDA / f"{nome}.png", facecolor=SUPERFICIE, bbox_inches="tight", pad_inches=0.15, metadata={"Software": None})
        plt.close(fig)
        print(f"  {nome}.png")

    def legenda(fig, itens, y=0.0, ncol=None):
        fig.legend(handles=itens, loc="lower center", bbox_to_anchor=(0.5, y), ncol=ncol or len(itens), frameon=False, fontsize=9, labelcolor=TINTA_2, handlelength=1.4, columnspacing=1.6)

    # ---- como o agente trabalha
    f = figs["como-o-agente-trabalha"]
    k = f["linhas"][0][1]
    modelo = f["linhas"][1][1]
    fig, ax = plt.subplots(figsize=(11, 5.6), dpi=200)
    fig.patch.set_facecolor(SUPERFICIE)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 60)
    ax.axis("off")
    COD, COD_B = "#eaf1fb", AZUL
    LLM, LLM_B = "#fdece4", LARANJA
    RES_, RES_B = "#f2f1ec", NEUTROS[0]

    def caixa(x, y, l, a, titulo, texto, fundo=COD, borda=COD_B, larg=24):
        ax.add_patch(FancyBboxPatch((x, y), l, a, boxstyle="round,pad=0.2,rounding_size=1.1", linewidth=1.1, edgecolor=borda, facecolor=fundo))
        ax.text(x + 0.9, y + a - 1.2, titulo, fontsize=9.6, fontweight="bold", color=TINTA, va="top", ha="left")
        ax.text(x + 0.9, y + a - 4.6, "\n".join(textwrap.wrap(texto, larg)), fontsize=8.2, color=TINTA_2, va="top", ha="left", linespacing=1.3)

    def seta(x1, y1, x2, y2, curva=0.0):
        ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=11, linewidth=1.1, color=TINTA_2, connectionstyle=f"arc3,rad={curva}"))

    largura, altura, passo = 17.6, 15.5, 20.2
    y1 = 42
    passos = [
        ("1. Roda o roteiro", "Abre a página no navegador e segue os passos, olhando a tela e as chamadas à API.", COD, COD_B),
        ("2. Detecta a falha", "Uma conferência do roteiro não passa, ou a resposta da API mudou.", COD, COD_B),
        ("3. Reduz o que viu", "Fica só o que mudou contra a tela normal: é a poda, feita em código.", COD, COD_B),
        ("4. Busca na biblioteca", f"Separa os {k} verbetes de documentação mais parecidos com o caso.", COD, COD_B),
        ("5. O modelo diagnostica", f"{modelo}, na própria máquina, só com CPU, escolhe a causa numa lista fechada.", LLM, LLM_B),
    ]
    for i, (t, x, fu, bo) in enumerate(passos):
        caixa(0.5 + i * passo, y1, largura, altura, t, x, fu, bo)
        if i:
            seta(0.5 + i * passo - (passo - largura) + 0.25, y1 + altura / 2, 0.5 + i * passo - 0.25, y1 + altura / 2)
    # selo, à direita, e os três resultados
    x_selo = 0.5 + 4 * passo
    y2 = 20.5
    caixa(x_selo, y2, largura, altura, "6. Confere e dá um selo", "O código confere a resposta e dá um selo de confiança: alto, médio ou baixo.")
    seta(x_selo + largura / 2, y1 - 0.25, x_selo + largura / 2, y2 + altura + 0.25)
    largura_r = 22.6
    resultados = [
        ("Falha de contrato", "A API mudou: sai um relatório para o analista, com a causa e o selo.", 0.5),
        ("Localizador quebrado", "A tela mudou: o código acha outro seletor e testa de novo, sem o modelo.", 0.5 + largura_r + 2.2),
        ("Aprendizado", "O modelo propõe um acréscimo à biblioteca; filtros em código decidem se entra.", 0.5 + 2 * (largura_r + 2.2)),
    ]
    for t, x, xr in resultados:
        caixa(xr, y2, largura_r, altura, t, x, RES_, RES_B, larg=33)
    # uma linha sai do alto do selo e desce para cada resultado
    y_bus = y2 + altura + 2.6
    x_saida = x_selo + 2.6
    centros = [xr + largura_r / 2 for _, _, xr in resultados]
    ax.plot([x_saida, x_saida], [y2 + altura + 0.25, y_bus], color=TINTA_2, linewidth=1.1, solid_capstyle="round")
    ax.plot([centros[0], x_saida], [y_bus, y_bus], color=TINTA_2, linewidth=1.1, solid_capstyle="round")
    for c in centros:
        seta(c, y_bus, c, y2 + altura + 0.25)
    # trilha
    ax.add_patch(FancyBboxPatch((0.5, 5.2), 98.0, 9.8, boxstyle="round,pad=0.2,rounding_size=1.1", linewidth=1.1, edgecolor=TINTA_2, facecolor=SUPERFICIE, linestyle="-"))
    ax.text(1.4, 13.6, "Trilha aberta", fontsize=9.6, fontweight="bold", color=TINTA, va="top")
    ax.text(1.4, 10.4, "Cada passo acima fica gravado: o que o agente viu, o que o modelo respondeu e o que o código conferiu. O relatório para quem revisa sai dessa trilha.", fontsize=8.4, color=TINTA_2, va="top")
    ax.add_patch(FancyArrowPatch((50, y2 - 0.25), (50, 15.3), arrowstyle="-|>", mutation_scale=11, linewidth=1.1, color=TINTA_2))
    fig.suptitle("Como o agente trabalha", x=0.012, y=0.995, ha="left", va="top", fontsize=13, fontweight="bold", color=TINTA)
    legenda(fig, [Patch(facecolor=COD, edgecolor=COD_B, label="Feito em código"), Patch(facecolor=LLM, edgecolor=LLM_B, label="Feito pelo modelo de linguagem"), Patch(facecolor=RES_, edgecolor=RES_B, label="O que sai no fim")], y=0.0)
    fig.subplots_adjust(left=0.005, right=0.995, top=0.94, bottom=0.05)
    fig.savefig(SAIDA / "como-o-agente-trabalha.png", facecolor=SUPERFICIE, bbox_inches="tight", pad_inches=0.12, metadata={"Software": None})
    plt.close(fig)
    print("  como-o-agente-trabalha.png")

    # ---- documentação e acerto
    f = figs["documentacao-e-acerto"]
    etapas = f["cab"][1:]
    fig, ax = base(8.2, 4.9)
    xs = list(range(len(etapas)))
    fins = []
    for l in f["linhas"]:
        m, vals = l[0], l[1:]
        ax.plot(xs, vals, color=COR_MODELO[m], linewidth=2, marker="o", markersize=7, markeredgecolor=SUPERFICIE, markeredgewidth=1.5, zorder=3, label=m)
        fins.append((vals[-1], m))
        ax.text(xs[0] - 0.06, vals[0], f"{_num(vals[0], 0)}%", ha="right", va="center", fontsize=8.5, color=TINTA_2)
    fins.sort()
    y_ant = -99
    for v, m in fins:
        y = max(v, y_ant + 5.2)
        y_ant = y
        ax.text(xs[-1] + 0.06, y, f"{_num(v, 0)}%  {m}", ha="left", va="center", fontsize=8.5, color=TINTA)
    ax.set_xticks(xs)
    ax.set_xticklabels(["\n".join(textwrap.wrap(e, 18)) for e in etapas], fontsize=9, color=TINTA)
    ax.set_xlim(-0.35, 2.75)
    ax.set_ylim(0, 100)
    ax.yaxis.set_major_formatter(lambda v, _: f"{v:.0f}%")
    ax.grid(axis="x", visible=False)
    titular(fig, f["titulo"], "Causa certa nos 36 casos de avaliação, que os modelos nunca usaram para aprender")
    legenda(fig, [Line2D([], [], color=COR_MODELO[m], marker="o", linewidth=2, label=m) for m in MODELOS], y=-0.005)
    fig.tight_layout(rect=(0, 0.06, 1, topo(fig)))
    fig.savefig(SAIDA / "documentacao-e-acerto.png", facecolor=SUPERFICIE, bbox_inches="tight", pad_inches=0.15, metadata={"Software": None})
    plt.close(fig)
    print("  documentacao-e-acerto.png")

    # ---- escolha do modelo
    f = figs["escolha-do-modelo"]
    fig, ax = base(8.2, 4.9)
    limpar(ax, "both")
    for l in f["linhas"]:
        m, bib_, y, x, de, ate, esc_ = l
        if esc_:
            ax.plot([x, x], [de, ate], color=COR_MODELO[m], linewidth=1.2, zorder=2)
            ax.scatter([x], [y], s=120, color=COR_MODELO[m], edgecolor=TINTA, linewidth=1.6, zorder=4)
            ax.annotate(f"Escolhido: {m}, com a primeira\nversão da biblioteca dele", (x, y), xytext=(10, -4), textcoords="offset points", fontsize=9, fontweight="bold", color=TINTA)
        else:
            ax.scatter([x], [y], s=52, color=COR_MODELO[m], edgecolor=SUPERFICIE, linewidth=1.2, zorder=3)
    ax.set_xlim(0, max(l[3] for l in f["linhas"]) * 1.08)
    ax.set_ylim(50, 100)
    ax.set_xlabel("segundos por caso (mediana): quanto mais à esquerda, mais rápido", fontsize=9, color=TINTA_2)
    ax.set_ylabel("acurácia balanceada nos 36 casos", fontsize=9, color=TINTA_2)
    ax.yaxis.set_major_formatter(lambda v, _: f"{v:.0f}%")
    titular(fig, f["titulo"], "Cada ponto é um modelo com a biblioteca num estado; a linha vertical é a margem de incerteza do escolhido")
    legenda(fig, [Line2D([], [], color=COR_MODELO[m], marker="o", linestyle="", markersize=7, label=m) for m in MODELOS], y=-0.005)
    fig.tight_layout(rect=(0, 0.06, 1, topo(fig)))
    fig.savefig(SAIDA / "escolha-do-modelo.png", facecolor=SUPERFICIE, bbox_inches="tight", pad_inches=0.15, metadata={"Software": None})
    plt.close(fig)
    print("  escolha-do-modelo.png")

    # ---- barras agrupadas em contagem
    def grupos(nome, series, cores, sub, rotulos_x=None, largura_fig=7.6):
        f = figs[nome]
        fig, ax = base(largura_fig, 4.4)
        n = f["linhas"][0][-1] if isinstance(f["linhas"][0][-1], int) else f["linhas"][0][3]
        xs = list(range(len(f["linhas"])))
        lar = 0.34
        for j, (col, rot, cor) in enumerate(zip(series, f["cab"][1:], cores)):
            vals = [l[col] for l in f["linhas"]]
            pos = [x + (j - (len(series) - 1) / 2) * (lar + 0.02) for x in xs]
            bar = ax.bar(pos, vals, width=lar, color=cor, zorder=3, label=rot)
            for b, v in zip(bar, vals):
                ax.text(b.get_x() + b.get_width() / 2, v + 0.5, str(v), ha="center", va="bottom", fontsize=9, color=TINTA)
        ax.set_xticks(xs)
        ax.set_xticklabels(rotulos_x or [l[0] for l in f["linhas"]], fontsize=9, color=TINTA)
        ax.set_ylim(0, n * 1.08)
        ax.set_ylabel(f"casos certos, de {n}", fontsize=9, color=TINTA_2)
        ax.grid(axis="x", visible=False)
        titular(fig, f["titulo"], sub)
        legenda(fig, [Patch(facecolor=c, label=f["cab"][1:][i]) for i, c in enumerate(cores)], y=-0.005)
        fig.tight_layout(rect=(0, 0.06, 1, topo(fig)))
        fig.savefig(SAIDA / f"{nome}.png", facecolor=SUPERFICIE, bbox_inches="tight", pad_inches=0.15, metadata={"Software": None})
        plt.close(fig)
        print(f"  {nome}.png")

    grupos("quem-le-a-biblioteca", [1, 2], [NEUTROS[1], AZUL], "Cada par compara o mesmo modelo, na mesma versão do Ollama, sem e com a biblioteca")
    grupos("casos-ineditos", [1, 2], [AZUL, LARANJA], "qwen2.5:7b: L0 é a biblioteca original; L1 e L3 são as versões que ele escreveu",
           rotulos_x=["Original (L0)", "Primeira versão (L1)", "Terceira versão (L3)"])

    # ---- selo
    f = figs["selo-de-confianca"]
    fig, ax = base(7.6, 3.2)
    limpar(ax, "x")
    nomes = [l[0] for l in f["linhas"]][::-1]
    certos = [l[2] for l in f["linhas"]][::-1]
    errados = [l[3] for l in f["linhas"]][::-1]
    ax.barh(nomes, certos, color=AZUL, height=0.56, zorder=3, label="Certos")
    ax.barh(nomes, errados, left=[c + 0.3 for c in certos], color=LARANJA, height=0.56, zorder=3, label="Errados")
    for i, (c, e) in enumerate(zip(certos, errados)):
        ax.text(c / 2, i, f"{c} certos", ha="center", va="center", fontsize=9, color="white", fontweight="bold")
        ax.text(c + 0.3 + e + 0.5, i, f"{e} errados", ha="left", va="center", fontsize=9, color=TINTA)
    ax.set_xlim(0, max(c + e for c, e in zip(certos, errados)) * 1.25)
    ax.set_xlabel("casos, dos 90 da calibração", fontsize=9, color=TINTA_2)
    ax.tick_params(axis="y", labelsize=10, labelcolor=TINTA)
    titular(fig, f["titulo"], "O selo vem da probabilidade que o próprio modelo dá à causa que escolheu")
    salvar(fig, "selo-de-confianca")

    # ---- reprodução
    f = figs["reproducao-na-tela"]
    fig, ax = base(8.2, 3.0)
    limpar(ax, "x")
    cores = [AZUL] + NEUTROS
    rotulos = f["cab"][2:]
    linhas = f["linhas"][::-1]
    for i, l in enumerate(linhas):
        esq = 0.0
        for j, v in enumerate(l[2:]):
            pct = 100 * v / l[1]
            ax.barh(i, pct - 0.3, left=esq, color=cores[j], height=0.56, zorder=3)
            if pct >= 7:
                ax.text(esq + (pct - 0.3) / 2, i, str(v), ha="center", va="center", fontsize=9, fontweight="bold", color="white" if j <= 1 else TINTA)
            esq += pct
    ax.set_yticks(range(len(linhas)))
    ax.set_yticklabels([f"{l[0]}\n({l[1]} casos)" for l in linhas], fontsize=9, color=TINTA)
    ax.set_xlim(0, 100)
    ax.xaxis.set_major_formatter(lambda v, _: f"{v:.0f}%")
    titular(fig, f["titulo"], "Parte das falhas nem passa pela tela; o número em cada faixa é a quantidade de casos")
    legenda(fig, [Patch(facecolor=c, label=r) for c, r in zip(cores, rotulos)], y=-0.03)
    fig.tight_layout(rect=(0, 0.1, 1, topo(fig)))
    fig.savefig(SAIDA / "reproducao-na-tela.png", facecolor=SUPERFICIE, bbox_inches="tight", pad_inches=0.15, metadata={"Software": None})
    plt.close(fig)
    print("  reproducao-na-tela.png")

    # ---- tela e caso escrito
    f = figs["tela-e-caso-escrito"]
    fig, ax = base(8.2, 5.0)
    limpar(ax, "x")
    # ! Alteração de IA - Revisar: (06/11/2026, decisões 97 e 98) sete barras em dois grupos: os 37 casos, da corrida mais nova para a primeira, e embaixo os inéditos.
    # ! Motivo: os inéditos são a conferência em casos que a busca nunca viu, e o total deles é outro; o espaço entre os grupos evita ler as barras como a mesma escala de casos.
    linhas = f["linhas"][::-1]
    ys = [0.0, 1.0] + [2.7 + i for i in range(len(linhas) - 2)]
    cores = [NEUTROS[0] if "caso escrito" in l[0].lower() else AZUL if "18d" in l[0] or "Inéditos, tela" in l[0] else NEUTROS[2] if "(corrida 18)" in l[0] else NEUTROS[1] for l in linhas]
    ax.barh(ys, [l[1] for l in linhas], color=cores, height=0.6, zorder=3)
    for y, l in zip(ys, linhas):
        ax.text(l[1] + 0.4, y, f"{l[1]} de {l[2]}", va="center", fontsize=9.5, color=TINTA)
    ax.set_yticks(ys)
    ax.set_yticklabels(["\n".join(textwrap.wrap(l[0], 34)) for l in linhas], fontsize=9, color=TINTA)
    ax.set_xlim(0, max(l[2] for l in linhas) * 1.14)
    ax.set_xlabel("casos com a causa certa", fontsize=9, color=TINTA_2)
    titular(fig, f["titulo"], "Os mesmos casos, lidos da tela e do texto escrito, na mesma sessão do modelo; embaixo, casos que a busca nunca viu")
    salvar(fig, "tela-e-caso-escrito")

    # ---- prompt e limite
    f = figs["prompt-e-limite"]
    corridas = list(dict.fromkeys(l[0] for l in f["linhas"]))
    fig, eixos = plt.subplots(1, 2, figsize=(10.6, 3.2), dpi=200, sharey=False)
    fig.patch.set_facecolor(SUPERFICIE)
    for ax, c in zip(eixos, corridas):
        ax.set_facecolor(SUPERFICIE)
        limpar(ax, "x")
        ls = [l for l in f["linhas"] if l[0] == c][::-1]
        for i, l in enumerate(ls):
            _, _, mi, me, ma, acima, de = l
            cor = NEUTROS[0] if "Antes" in l[1] else AZUL
            ax.plot([mi, ma], [i, i], color=cor, linewidth=2.2, zorder=3, solid_capstyle="round")
            ax.scatter([me], [i], s=46, color=cor, edgecolor=SUPERFICIE, linewidth=1.2, zorder=4)
            ax.text(2120, i, f"{acima} de {de}", va="center", ha="left", fontsize=8.8, color=TINTA)
        ax.axvline(f["limite"], color=LARANJA, linewidth=1.4, zorder=2)
        ax.text(f["limite"] + 12, len(ls) - 0.45, f"limite: {f['limite']}", fontsize=8.5, color=TINTA, va="bottom")
        ax.set_yticks(range(len(ls)))
        ax.set_yticklabels([l[1] for l in ls], fontsize=8.8, color=TINTA)
        ax.set_xlim(850, 2420)
        ax.set_ylim(-0.6, len(ls) - 0.1)
        ax.set_xlabel("tokens do prompt", fontsize=8.8, color=TINTA_2)
        ax.set_title(c, fontsize=9.5, color=TINTA, loc="left", pad=12)
        ax.text(2120, len(ls) - 0.45, "acima do limite", fontsize=8, color=TINTA_2, va="bottom")
    titular(fig, f["titulo"], "Cada linha vai do menor ao maior prompt, e o ponto é o valor do meio; o traço laranja é o limite do plano")
    fig.tight_layout(rect=(0, 0, 1, topo(fig)))
    fig.savefig(SAIDA / "prompt-e-limite.png", facecolor=SUPERFICIE, bbox_inches="tight", pad_inches=0.15, metadata={"Software": None})
    plt.close(fig)
    print("  prompt-e-limite.png")

    # ---- tempo por cenário
    f = figs["tempo-por-cenario"]
    fig, ax = base(8.2, 4.5)
    limpar(ax, "x")
    ordem = sorted(f["linhas"], key=lambda l: (l[1] != "contrato", -l[2]))[::-1]
    cor_tipo = {"contrato": AZUL, "localizador": LARANJA}
    ax.barh(range(len(ordem)), [l[2] for l in ordem], color=[cor_tipo[l[1]] for l in ordem], height=0.62, zorder=3)
    for i, l in enumerate(ordem):
        ax.text(l[2] + 1.5, i, f"{_num(l[2], 0)} s", va="center", fontsize=9, color=TINTA)
    ax.set_yticks(range(len(ordem)))
    ax.set_yticklabels([l[0] for l in ordem], fontsize=9, color=TINTA)
    ax.set_xlim(0, max(l[2] for l in ordem) * 1.12)
    ax.set_xlabel("segundos, da detecção da falha até o resultado", fontsize=9, color=TINTA_2)
    g = f["geral"]
    titular(fig, f["titulo"], f"{g['sucessos']} de {g['n']} chegaram ao resultado, em {_num(g['mttr_media_s'], 0)} s na média (eram {_num(f['media_anterior'], 0)} s com o prompt maior); uma repetição por cenário")
    pt = f["por_tipo"]
    legenda(fig, [Patch(facecolor=AZUL, label=f"Falha de contrato (média de {_num(pt['contrato'], 0)} s)"), Patch(facecolor=LARANJA, label=f"Localizador quebrado (média de {_num(pt['localizador'], 0)} s)")], y=-0.005)
    fig.tight_layout(rect=(0, 0.07, 1, topo(fig)))
    fig.savefig(SAIDA / "tempo-por-cenario.png", facecolor=SUPERFICIE, bbox_inches="tight", pad_inches=0.15, metadata={"Software": None})
    plt.close(fig)
    print("  tempo-por-cenario.png")

    # ---- funil
    f = figs["funil-da-biblioteca"]
    fig, ax = base(8.8, 4.0)
    limpar(ax, "x")
    linhas = f["linhas"][::-1]
    ax.barh(range(len(linhas)), [l[1] for l in linhas], color=RAMPA[::-1], height=0.62, zorder=3)
    for i, l in enumerate(linhas):
        ax.text(l[1] + 0.9, i, str(l[1]), va="center", fontsize=10, fontweight="bold", color=TINTA)
    motivos = f["motivos"]
    def resumo_motivos(m):
        return ", ".join(f"{n} ({v})" for n, v in m)
    barrados = {2: f"barradas {f['linhas'][2][2]}: {resumo_motivos(motivos['p5'])}", 3: f"barradas {f['linhas'][1][2]}: {resumo_motivos(motivos['fase3'])}",
                0: f"saíram {f['linhas'][4][2]} na revisão: as marcadas como erradas"}
    for i, txt in barrados.items():
        ax.text(linhas[i][1] + 5.5, i, "\n".join(textwrap.wrap(txt, 56)), va="center", fontsize=8.2, color=TINTA_2)
    ax.set_yticks(range(len(linhas)))
    ax.set_yticklabels(["\n".join(textwrap.wrap(l[0], 26)) for l in linhas], fontsize=9, color=TINTA)
    ax.set_xlim(0, f["propostas"] * 1.1)
    ax.set_xlabel("propostas de acréscimo à biblioteca", fontsize=9, color=TINTA_2)
    titular(fig, f["titulo"], "Corrida 20: só chega ao lote o que passa por todas as conferências em código, e o lote ainda passa por revisão")
    salvar(fig, "funil-da-biblioteca")

    # ---- sinais da trilha
    f = figs["sinais-da-trilha"]
    fig, ax = base(8.8, 4.3)
    limpar(ax, "x")
    linhas = f["linhas"][::-1]
    cores_s = [AZUL if l[0] == f["oficial"] else NEUTROS[1] for l in linhas]
    ax.barh(range(len(linhas)), [l[1] for l in linhas], color=cores_s, height=0.62, zorder=3)
    for i, l in enumerate(linhas):
        ax.text(l[1] + 0.012, i, _num(l[1], 2), va="center", fontsize=9, color=TINTA, zorder=5, bbox={"facecolor": SUPERFICIE, "edgecolor": "none", "pad": 0.8})
    ax.axvline(f["acaso"], color=LARANJA, linewidth=1.4, zorder=4)
    ax.text(f["acaso"] + 0.006, len(linhas) - 0.42, f"chutar dá {_num(f['acaso'], 2)}", fontsize=8.5, color=TINTA, va="bottom")
    ax.set_yticks(range(len(linhas)))
    ax.set_yticklabels([l[0] for l in linhas], fontsize=8.8, color=TINTA)
    ax.set_xlim(0, 1)
    ax.set_ylim(-0.6, len(linhas) - 0.1)
    ax.set_xlabel("nota de 0 a 1: alta só se o sinal acende nos erros e fica apagado nos acertos", fontsize=9, color=TINTA_2)
    titular(fig, f["titulo"], f"Corrida 22: {linhas[0][3]} erros em {linhas[0][3] + linhas[0][5]} casos, poucos demais para pôr os sinais em ordem")
    salvar(fig, "sinais-da-trilha")

    # ---- quantos verbetes
    f = figs["quantos-verbetes"]
    fig, eixos = plt.subplots(1, 2, figsize=(7.6, 3.0), dpi=200)
    fig.patch.set_facecolor(SUPERFICIE)
    rot = [f"{l[0]} verbetes" for l in f["linhas"]]
    for ax, col, tit, fmt_, teto in ((eixos[0], 1, "Acurácia balanceada", lambda v: f"{_num(v)}%", 100), (eixos[1], 2, "Tamanho do prompt (tokens, valor do meio)", lambda v: _num(v, 0), None)):
        ax.set_facecolor(SUPERFICIE)
        limpar(ax)
        vals = [l[col] for l in f["linhas"]]
        bar = ax.bar(rot, vals, color=[AZUL, NEUTROS[1]], width=0.5, zorder=3)
        for b, v in zip(bar, vals):
            ax.text(b.get_x() + b.get_width() / 2, v * 1.02, fmt_(v), ha="center", va="bottom", fontsize=9.5, color=TINTA)
        ax.set_ylim(0, (teto or max(vals)) * 1.16 if not teto else teto)
        ax.grid(axis="x", visible=False)
        ax.set_title(tit, fontsize=9.5, color=TINTA, loc="left", pad=8)
        ax.tick_params(axis="x", labelcolor=TINTA)
    titular(fig, f["titulo"], "Corrida 16: os 90 casos, com a biblioteca de produção")
    fig.tight_layout(rect=(0, 0, 1, topo(fig)))
    fig.savefig(SAIDA / "quantos-verbetes.png", facecolor=SUPERFICIE, bbox_inches="tight", pad_inches=0.15, metadata={"Software": None})
    plt.close(fig)
    print("  quantos-verbetes.png")

    # ---- tela por classe
    f = figs["tela-por-classe"]
    fig, ax = base(7.6, 3.5)
    limpar(ax, "x")
    linhas = f["linhas"][::-1]
    for i, l in enumerate(linhas):
        nome, casos, tela, esc_ = l
        pt_t, pt_e = 100 * tela / casos, 100 * esc_ / casos
        ax.plot([pt_t, pt_e], [i, i], color=NEUTROS[1], linewidth=2, zorder=2)
        ax.scatter([pt_e], [i], s=70, color=NEUTROS[0], edgecolor=SUPERFICIE, linewidth=1.3, zorder=3)
        ax.scatter([pt_t], [i], s=70, color=AZUL, edgecolor=SUPERFICIE, linewidth=1.3, zorder=4)
        ax.text(103, i, f"{tela} e {esc_} de {casos}", va="center", fontsize=8.8, color=TINTA)
    ax.set_yticks(range(len(linhas)))
    ax.set_yticklabels([l[0] for l in linhas], fontsize=9, color=TINTA)
    ax.set_xlim(0, 125)
    ax.set_xticks(range(0, 101, 20))
    ax.xaxis.set_major_formatter(lambda v, _: f"{v:.0f}%")
    ax.set_xlabel("casos com a causa certa", fontsize=9, color=TINTA_2)
    titular(fig, f["titulo"], "Corrida 18d, por classe de defeito; à direita, os certos na tela e no caso escrito")
    legenda(fig, [Line2D([], [], color=AZUL, marker="o", linestyle="", markersize=7, label="Lendo da tela"), Line2D([], [], color=NEUTROS[0], marker="o", linestyle="", markersize=7, label="Lendo o caso escrito")], y=-0.01)
    fig.tight_layout(rect=(0, 0.08, 1, topo(fig)))
    fig.savefig(SAIDA / "tela-por-classe.png", facecolor=SUPERFICIE, bbox_inches="tight", pad_inches=0.15, metadata={"Software": None})
    plt.close(fig)
    print("  tela-por-classe.png")

    # ---- inéditos por classe (corrida 24)
    f = figs["ineditos-por-classe"]
    fig, ax = base(7.6, 3.5)
    limpar(ax, "x")
    linhas = f["linhas"][::-1]
    for i, l in enumerate(linhas):
        nome, casos, certos, errados = l
        ax.barh(i, certos, color=AZUL, height=0.56, zorder=3)
        ax.barh(i, errados, left=certos, color=LARANJA, height=0.56, zorder=3)
        ax.text(casos + 0.12, i, f"{certos} de {casos}", va="center", fontsize=9.5, color=TINTA)
    ax.set_yticks(range(len(linhas)))
    ax.set_yticklabels([l[0] for l in linhas], fontsize=9, color=TINTA)
    ax.set_xlim(0, max(l[1] for l in linhas) * 1.2)
    ax.set_xticks(range(max(l[1] for l in linhas) + 1))
    ax.set_xlabel("casos", fontsize=9, color=TINTA_2)
    titular(fig, f["titulo"], f'{f["resumo"]["acertos"]} de {f["resumo"]["casos"]} na corrida 24; nos casos de avaliação, com a mesma biblioteca, {f["referencia"]["acertos"]} de {f["referencia"]["casos"]}')
    legenda(fig, [Patch(color=AZUL, label="Causa certa"), Patch(color=LARANJA, label="Causa errada")], y=-0.01)
    fig.tight_layout(rect=(0, 0.08, 1, topo(fig)))
    fig.savefig(SAIDA / "ineditos-por-classe.png", facecolor=SUPERFICIE, bbox_inches="tight", pad_inches=0.15, metadata={"Software": None})
    plt.close(fig)
    print("  ineditos-por-classe.png")

    # ---- onde vai o tempo
    f = figs["onde-vai-o-tempo"]
    fig, ax = base(8.2, 3.9)
    limpar(ax, "x")
    linhas = f["linhas"][::-1]
    ax.barh(range(len(linhas)), [l[1] for l in linhas], color=[LARANJA if l[2] == "sim" else AZUL for l in linhas], height=0.6, zorder=3)
    for i, l in enumerate(linhas):
        ax.text(l[1] + 1.2, i, f"{_num(l[1], 1 if l[1] >= 1 else 2)} s", va="center", fontsize=9, color=TINTA)
    ax.set_yticks(range(len(linhas)))
    ax.set_yticklabels(["\n".join(textwrap.wrap(l[0], 40)) for l in linhas], fontsize=8.8, color=TINTA)
    ax.set_xlim(0, max(l[1] for l in linhas) * 1.14)
    ax.set_xlabel("segundos (valor do meio)", fontsize=9, color=TINTA_2)
    titular(fig, f["titulo"], "O que é só código leva menos de um segundo; o tempo do agente é quase todo o modelo pensando")
    legenda(fig, [Patch(facecolor=AZUL, label="Só código"), Patch(facecolor=LARANJA, label="Usa o modelo")], y=-0.02)
    fig.tight_layout(rect=(0, 0.09, 1, topo(fig)))
    fig.savefig(SAIDA / "onde-vai-o-tempo.png", facecolor=SUPERFICIE, bbox_inches="tight", pad_inches=0.15, metadata={"Software": None})
    plt.close(fig)
    print("  onde-vai-o-tempo.png")


def main() -> int:
    if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--check", action="store_true", help="confere o .md gravado contra os JSON; não desenha")
    args = ap.parse_args()
    figs = coletar()
    texto = gerar_md(figs)
    if args.check:
        atual = MD.read_text(encoding="utf-8") if MD.exists() else ""
        if atual != texto:
            print(f"--check: {MD.name} DIFERE do regerado; rode sem --check")
            return 1
        faltam = [n for n in figs if not (SAIDA / f"{n}.png").exists()]
        if faltam:
            print("--check: figuras que faltam:", ", ".join(faltam))
            return 1
        print(f"--check: {MD.name} idêntico ao regerado; {len(figs)} figuras presentes")
        return 0
    SAIDA.mkdir(parents=True, exist_ok=True)
    desenhar(figs)
    MD.write_text(texto, encoding="utf-8", newline="\n")
    print(f"gravado: {MD} ({len(figs)} figuras)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
