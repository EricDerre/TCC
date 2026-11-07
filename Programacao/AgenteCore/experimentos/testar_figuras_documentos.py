#!/usr/bin/env python3
# ! Alteração de IA - Revisar: testes novos (05/11/2026) de gerar_figuras_documentos.py: as somas de cada figura fecham com o total lido dos registros, e o .md gravado é o que o script gera hoje.
# ! Motivo: essas figuras substituem os números no README e no documento do TCC; uma etapa do funil ou uma faixa da reprodução que não somasse sairia publicada sem ninguém notar, porque ali a figura é a única forma de ver o dado.
"""Testes sem LLM e sem matplotlib. Uso: python testar_figuras_documentos.py (qualquer Python; termina em `N testes ok`)."""
from __future__ import annotations

import sys

import gerar_figuras_documentos as g

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

FIGS = g.coletar()


def teste_funil_fecha_em_cada_etapa():
    """Cada etapa é a anterior menos o que ela barrou; o lote soma o que ficou segurado para revisão."""
    l = FIGS["funil-da-biblioteca"]["linhas"]
    assert l[0][1] - l[1][2] == l[1][1]
    assert l[1][1] - l[2][2] == l[2][1]
    assert l[3][1] + l[3][2] == l[2][1]
    assert l[3][1] + l[3][2] - l[4][1] == l[4][2]


def teste_reproducao_soma_os_casos_de_cada_conjunto():
    for linha in FIGS["reproducao-na-tela"]["linhas"]:
        assert linha[1] == sum(linha[2:]), linha


def teste_selo_soma_os_casos_da_calibracao():
    linhas = FIGS["selo-de-confianca"]["linhas"]
    for nome, casos, certos, errados, _ in linhas:
        assert casos == certos + errados, nome
    assert sum(l[1] for l in linhas) == g._j("fase4/calibracao.json")["limiares"]["n"]


def teste_contagens_nao_passam_do_total():
    for nome in ("quem-le-a-biblioteca", "casos-ineditos"):
        for linha in FIGS[nome]["linhas"]:
            assert linha[1] <= linha[3] and linha[2] <= linha[3], (nome, linha)
    for _, certos, de in FIGS["tela-e-caso-escrito"]["linhas"]:
        assert certos <= de
    for _, casos, tela, escrito in FIGS["tela-por-classe"]["linhas"]:
        assert tela <= casos and escrito <= casos


def teste_tempo_da_cura_e_o_unico_sem_modelo():
    linhas = FIGS["onde-vai-o-tempo"]["linhas"]
    assert [l[2] for l in linhas].count("não") == 1
    assert linhas[0][1] < 1 < linhas[1][1]


def teste_todos_os_nomes_tem_texto_sem_sigla_de_codigo():
    """O nome que aparece na figura é o texto simples, não o identificador do código."""
    for nome in ("tempo-por-cenario",):
        for linha in FIGS[nome]["linhas"]:
            assert "-" not in linha[0] and "_" not in linha[0], linha[0]
    assert all("_" not in l[0] for l in FIGS["sinais-da-trilha"]["linhas"])


# ! Alteração de IA - Revisar: (05/11/2026, decisão 90) as figuras da tela e dos cenários leem a 18c e a 21c, e a do prompt mede os tokens reais, antes e depois do corte.
# ! Motivo: a decisão 90 diz que as leituras novas passam a valer quando as corridas rodarem; a figura do prompt mostrava estimativas de cortes possíveis, e agora há a medida.
def teste_figuras_usam_as_leituras_vigentes():
    # ! Alteração de IA - Revisar: (06/11/2026, decisões 97 e 98) as figuras passam à 18d e à 21d, e a da tela ganha as linhas da 18c e dos inéditos (18e).
    # ! Motivo: a regra R2 fechou na 18d pela leitura fixada antes dela, e os inéditos são a conferência limpa: o README precisa mostrar as duas.
    t4, ti, c4, c2 = g._j("fase4/tela_v4.json")["resumo"], g._j("fase4/tela_ineditos.json")["resumo"], g._j("fase4/cenarios_v4.json")["geral"], g._j("fase4/cenarios_v2.json")["geral"]
    linhas = FIGS["tela-e-caso-escrito"]["linhas"]
    assert [l[1] for l in linhas][:2] == [t4["acerto_fixture"], t4["acerto_tela"]], linhas
    assert "18d" in linhas[1][0] and any("18c" in l[0] for l in linhas) and any("18b" in l[0] for l in linhas) and any("(corrida 18)" in l[0] for l in linhas), linhas
    ine = [l for l in linhas if "18e" in l[0]]
    assert [l[1:] for l in ine] == [[ti["acerto_fixture"], ti["casos"]], [ti["acerto_tela"], ti["casos"]]], ine
    assert FIGS["tempo-por-cenario"]["geral"]["mttr_media_s"] == c4["mttr_media_s"]
    assert FIGS["tempo-por-cenario"]["media_anterior"] == c2["mttr_media_s"], "a referência do tempo continua a de antes do corte do prompt"
    assert "18d" in FIGS["tela-por-classe"]["fonte"] and "21d" in FIGS["onde-vai-o-tempo"]["fonte"] and "18d" in FIGS["onde-vai-o-tempo"]["fonte"]
    prompt = FIGS["prompt-e-limite"]
    assert prompt["limite"] == 1409
    assert [l[1] for l in prompt["linhas"]] == ["Antes do corte (18b)", "Depois do corte (18c)", "Com os sinais da busca (18d)", "Inéditos, com os sinais da busca (18e)", "Antes do corte (21b)", "Depois do corte (21c)", "Com os sinais da busca (21d)"], prompt["linhas"]
    for l in prompt["linhas"]:
        assert l[2] <= l[3] <= l[4], l
    assert [l[5] for l in prompt["linhas"]] == [37, 0, 0, 2, 9, 0, 0], "só os dois inéditos em que a lista muda inteira passaram do limite depois do corte"
    assert len({l[0] for l in prompt["linhas"]}) == 2, "dois painéis: casos da tela e cenários"


# ! Alteração de IA - Revisar: (06/11/2026) a figura da corrida 24: certos e errados por classe de defeito, nos 36 inéditos.
# ! Motivo: é a única medida da biblioteca final em casos que ela nunca viu, e a classe de tradução é onde ela mais erra; o README precisa mostrar isso.
def teste_figura_dos_ineditos_da_corrida_24():
    d = g._j("fase4/ineditos.json")
    f = FIGS["ineditos-por-classe"]
    assert sum(l[2] for l in f["linhas"]) == d["resumo"]["acertos"] and sum(l[3] for l in f["linhas"]) == d["resumo"]["casos"] - d["resumo"]["acertos"], f["linhas"]
    assert f["resumo"]["casos"] == d["resumo"]["casos"] and f["referencia"]["acertos"] == d["referencia"]["acertos"]
    assert all("_" not in l[0] for l in f["linhas"]), "o nome na figura é o texto simples"


def teste_titulos_sem_travessao_nem_seta():
    for f in FIGS.values():
        for c in "—→↔":
            assert c not in f["titulo"], f["titulo"]


def teste_md_gravado_bate_com_os_registros_e_as_figuras_existem():
    assert g.MD.read_text(encoding="utf-8") == g.gerar_md(FIGS), "rode gerar_figuras_documentos.py"
    for nome in FIGS:
        assert (g.SAIDA / f"{nome}.png").exists(), nome


if __name__ == "__main__":
    testes = [v for k, v in sorted(globals().items()) if k.startswith("teste_") and callable(v)]
    for t in testes:
        t()
    print(f"{len(testes)} testes ok")
