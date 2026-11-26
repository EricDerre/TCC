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
    for nome in ("tempo-por-cenario", "agente-e-pessoas"):
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


# ! Alteração de IA - Revisar: (24/11/2026, Fase 5, decisão 151) teste novo da figura da medição de valor: o tempo de reparo do agente e o das pessoas, cenário a
# cenário, com o menor e o maior tempo de cada lado, e o Task Success de cada lado na tabela de dados.
# ! Motivo: é o resultado central do TCC e a descoberta nova do README. A figura só pode trazer o que a leitura `avaliar_fase5.py --comparar` gravou em
# `fase5/medicao.json`: se uma coluna saísse de outro lugar, ou a média ficasse fora da faixa entre o menor e o maior tempo, o gráfico do resultado principal
# sairia publicado errado sem ninguém notar. O Task Success vai só para a tabela, porque o veredito dele depende de uma sessão (a ressalva está no README).
def teste_figura_do_agente_contra_as_pessoas_le_a_medicao_da_fase_5():
    m = g._j("fase5/medicao.json")
    f = FIGS["agente-e-pessoas"]
    assert "fase5/medicao.json" in f["fonte"] and "28b" in f["fonte"], f["fonte"]
    assert len(f["linhas"]) == len(m["tempo"]["por_cenario"]) == len(f["cab"]) - 1, (len(f["linhas"]), f["cab"])
    sucesso = {x["cenario"]: x for x in m["task_success"]["por_cenario"]}
    for linha, x in zip(f["linhas"], m["tempo"]["por_cenario"]):
        assert linha[:2] == [g.NOME_CENARIO[x["cenario"]], x["tipo"]], linha
        assert linha[2:9] == [x["agente_media_s"], x["agente_min_s"], x["agente_max_s"], x["pessoas_media_s"], x["pessoas_min_s"], x["pessoas_max_s"], x["diferenca_s"]], linha
        assert linha[3] <= linha[2] <= linha[4] and linha[6] <= linha[5] <= linha[7], linha
        s = sucesso[x["cenario"]]
        assert linha[9:] == [f'{s["agente_sucessos"]} de {s["agente_n"]}', f'{s["pessoas_sucessos"]} de {s["pessoas_n"]}'], linha
    geral = m["tempo"]["geral"]
    assert f["geral"] == {"agente_s": m["lados"]["agente"]["geral"]["tempo_media_s"], "pessoas_s": m["lados"]["pessoas"]["geral"]["tempo_media_s"],
                          "diferenca_media_s": geral["diferenca_media_s"], "agente_mais_rapido": geral["sinais"]["agente"], "pessoas_mais_rapidas": geral["sinais"]["pessoas"],
                          "empates": geral["sinais"]["empates"], "cenarios": len(m["tempo"]["por_cenario"])}, f["geral"]


# ! Alteração de IA - Revisar: (25/11/2026, Pós-Fase 4, pacote Q8) teste novo da figura "revisao-humana": quantos relatórios do analista de QA foram decisões apropriadas, separados por diagnóstico certo e errado.
# ! Motivo: a figura entra no README como a única forma de ver a revisão às cegas dos 36 relatórios da corrida 24; se a soma das faixas não batesse com os 30 de 36 da leitura (`leitura_revisao_v3.json`, `adesao_apropriada`), a figura sairia contando outra coisa sem ninguém notar.
def teste_figura_da_revisao_humana_bate_com_a_leitura_da_sessao():
    d = g._j("fase4/leitura_revisao_v3.json")
    f = FIGS["revisao-humana"]
    assert "leitura_revisao_v3.json" in f["fonte"], f["fonte"]
    assert [l[0] for l in f["linhas"]] == ["Diagnósticos certos", "Diagnósticos errados"], f["linhas"]
    for nome, casos, apropriadas, nao in f["linhas"]:
        assert casos == apropriadas + nao, nome
    assert sum(l[1] for l in f["linhas"]) == d["resumo"]["relatorios"] == 36
    assert sum(l[2] for l in f["linhas"]) == d["resumo"]["adesao_apropriada"] == 30
    assert [l[1] for l in f["linhas"]] == [d["resumo"]["acertos_na_corrida"], d["resumo"]["erros_na_corrida"]] == [25, 11]
    assert [l[2:] for l in f["linhas"]] == [[20, 5], [10, 1]], "aceitar o certo e recusar o errado são as decisões apropriadas"


# ! Alteração de IA - Revisar: (25/11/2026, Pós-Fase 4, pacote Q8) teste novo da figura "experimentos-pos-fase-4": as três mudanças testadas depois da Fase 4 (corridas 25, 26 e 27), cada uma com a referência, a mudança e o valor-p.
# ! Motivo: o README passa a afirmar que nenhuma das três sai do ruído (p acima de 0,05); a figura só pode dizer isso se os números vierem de `sem_notas.json`, `segundo_passe.json` e `analista.json`, com os mesmos valores que o roadmap registra (56 e 54 de 72, p 0,6875; 56 e 54 de 72, p 0,625; 1 de 20 e 3 de 8, p 0,0581).
def teste_figura_dos_experimentos_da_pos_fase_4_le_os_tres_registros():
    f = FIGS["experimentos-pos-fase-4"]
    for rel in ("sem_notas.json", "segundo_passe.json", "analista.json"):
        assert rel in f["fonte"], (rel, f["fonte"])
    assert len(f["linhas"]) == 3 and len(f["linhas"][0]) == len(f["cab"]), f["linhas"]
    # colunas: experimento, casos da referência, certos da referência, casos da mudança, certos da mudança, p
    assert [l[1:] for l in f["linhas"]] == [[72, 56, 72, 54, 0.6875], [72, 56, 72, 54, 0.625], [20, 1, 8, 3, 0.0581]], f["linhas"]
    assert all(l[5] > 0.05 for l in f["linhas"]), "nenhuma das três sai do ruído"
    assert [n in l[0] for n, l in zip(("corrida 25", "corrida 26", "corrida 27"), f["linhas"])] == [True] * 3
    assert "0,6875" in g.gerar_md(FIGS) and "0,0581" in g.gerar_md(FIGS), "o valor-p sai inteiro na tabela de dados"


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
