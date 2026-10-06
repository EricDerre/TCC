#!/usr/bin/env python3
# ! Alteração de IA - Revisar: testes das abas por tópico do painel (30/09/2026): cada seção nova é gerada a
# partir dos arquivos reais do repositório, os números-chave batem com os JSON de origem, o mapa de filtros
# da rodada 4 é lido sem os asteriscos do Markdown, e toda função de gráfico e seletor citados existem.
# ! Motivo: o painel é o compilador das análises e o Eric decide por ele; um erro de leitura (como o
# veredito "**adotado**" contado como "outro", visto na primeira geração) sairia publicado sem aviso.
"""Uso: python ferramentas/testar_painel_topicos.py"""
from __future__ import annotations

import json
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gerar_dashboard as gd  # noqa: E402
import painel_textos as pt  # noqa: E402
import painel_topicos as tp  # noqa: E402


def _ctx() -> dict:
    r = gd.ler_json(gd.F3 / "resumo_fase3.json")
    c = gd.ler_json(gd.F3 / "comparacao_fases.json")
    d = gd.ler_json(gd.F3 / "decisao_modelo.json")
    m2b = gd.ler_json(gd.EXP / "resultados_alvo" / "resumo_metricas.json")
    m2a = gd.ler_json(gd.EXP / "resumo_metricas.json")
    dados = gd.montar_dados(r, c, d, m2b, m2a)
    road = pt.ler_roadmap(gd.MEMORIAL / "roadmap.md")
    medicao = gd.MEMORIAL / "5-metodo-e-ferramental" / "dados" / "medicao-permanencia-mcp.json"
    return {
        "dados": dados, "road": road, "cartoes_corridas": gd.cartoes_corridas, "md_para_html": gd.md_para_html,
        "md_doc_para_html": pt.md_doc_para_html,
        "cq": gd.ler_json(gd.F3 / "comparativo_qwen_coder.json"), "blocos_cq": gd.blocos_tabelas(gd.F3 / "comparativo_qwen_coder.md"),
        "ineditos": gd.resumo_dos_ineditos(),
        "curadoria": gd.ler_json(gd.EXP.parent / "biblioteca_producao" / "curadoria.json"),
        "planilha_curadoria": (gd.F3 / "curadoria_L1__qwen2.5_7b.md").read_text(encoding="utf-8"),
        "recuperador": gd.ler_json(gd.EXP / "resultados_alvo" / "recuperador" / "experimento_recuperador.json"),
        "ablacao": gd.ler_json(gd.EXP / "resultados_alvo" / "ablacao_base_instruct" / "resumo_metricas.json"),
        "medicao_mcp": gd.ler_json(medicao) if medicao.exists() else None,
        "readme": (gd.RAIZ / "README.md").read_text(encoding="utf-8"),
        "analise3b": gd.ler_json(gd.F3 / "analise_fase3b.json"),
        "relatorio3b": (gd.MEMORIAL / "3-resultados-e-analises" / "fase-3b-relatorio.md").read_text(encoding="utf-8"),
        "pend": pt.ler_pendencias(gd.MEMORIAL / "pendencias.md"),
        **gd.contexto_pre_fase4(),
    }


class TestesAbasPorTopico(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ctx = _ctx()
        cls.dados_t, cls.html = tp.montar(cls.ctx)

    def teste_toda_aba_do_mapa_existe_na_pagina(self):
        ids_topicos = [sid for _, abas in tp.NAV for sid, _, _ in abas]
        html = gd.pagina(self.ctx["dados"] | {"topicos": self.dados_t}, gd.blocos_tabelas(gd.F3 / "tabelas_relatorio.md"), {},
                         pt.ler_pendencias(gd.MEMORIAL / "pendencias.md"), self.ctx["road"], self.html)
        for sid in ids_topicos:
            self.assertIn(f'<section id="{sid}"', html, sid)
            self.assertIn(f'data-alvo="{sid}"', html, sid)
        ids = re.findall(r' id="([^"]+)"', html)
        repetidos = {i for i in ids if ids.count(i) > 1}
        self.assertFalse(repetidos, f"ids repetidos na página: {sorted(repetidos)[:10]}")

    # ! Alteração de IA - Revisar: teste novo (06/10/2026) da navegação lateral em ordem de importância.
    # ! Motivo: o Eric pediu a barra de seções na lateral (com 23 abas a faixa horizontal ficou ilegível) e a ordem
    # por importância: primeiro o projeto e o que depende dele, depois a decisão e os resultados, a biblioteca gerida
    # pelo modelo, a Pré-Fase 4, a pesquisa e, por último, as fases anteriores.
    def teste_navegacao_lateral_em_ordem_de_importancia(self):
        html = gd.pagina(self.ctx["dados"] | {"topicos": self.dados_t}, gd.blocos_tabelas(gd.F3 / "tabelas_relatorio.md"), {},
                         pt.ler_pendencias(gd.MEMORIAL / "pendencias.md"), self.ctx["road"], self.html)
        lateral = re.search(r'<aside class="lateral" id="lateral">(.*?)</aside>', html, re.S)
        self.assertTrue(lateral, "a navegação fica num <aside class=\"lateral\">")
        self.assertIn('<nav aria-label="Seções">', lateral.group(1))
        self.assertEqual(re.findall(r'data-alvo="([^"]+)"', lateral.group(1)), [sid for _, abas in tp.NAV for sid, _, _ in abas])
        self.assertEqual(re.findall(r'<span class="grupo">([^<]+)</span>', lateral.group(1)), [g for g, _ in tp.NAV])
        self.assertEqual([g for g, _ in tp.NAV], ["Projeto", "Decisão e resultados", "Biblioteca gerida pelo modelo", "Pré-Fase 4", "Pesquisa e método", "Fases anteriores"])
        self.assertEqual([abas[0][0] for _, abas in tp.NAV], ["inicio", "decisao", "fase3", "colibri", "pesquisa", "fases2"])
        # em tela estreita a lateral vira gaveta aberta por um botão
        self.assertIn('<button class="menu" aria-controls="lateral" aria-expanded="false">', html)
        self.assertRegex(html, r"@media \(max-width:\s*900px\)\{[^}]*\.lateral\{")
        self.assertIn("menu-aberto", html)

    def teste_comparativo_usa_os_numeros_do_json(self):
        cq = self.ctx["cq"]
        n_vence = len(cq["onde_o_coder_vence"])
        self.assertIn(f"<b>{n_vence}</b>", self.html)
        self.assertEqual(len(self.dados_t["cq"]["trajetoria"]["36"]), 7)  # 2-A, 2-B A0/A2, F3 L0..L3 (sem "melhor")
        self.assertEqual(len(self.dados_t["cq"]["confronto"]["90"]), 3 + 4)
        # ! Alteração de IA - Revisar: (06/10/2026) o confronto nos 36 inéditos (corrida 7) entra na aba, lido do JSON.
        # ! Motivo: era a condição 1 do comparativo para rever a decisão 52; o Eric rodou a corrida em 06/10.
        secao = self.html[self.html.index('<section id="comparativo"'):].split("</section>")[0]
        for x in cq.get("confronto_ineditos", []):
            if x["L"] == 1:
                self.assertIn(f'<b>{x["so_qwen"]} × {x["so_coder"]}</b>', secao)
                self.assertIn("ficha 21", secao)
        self.assertNotIn("se o Eric quiser, o Coder 7B nos 36 inéditos", secao)

    def teste_tres_b_compara_oficiais_e_ineditos_nas_mesmas_versoes(self):
        t = self.dados_t["tresb"]
        self.assertEqual(t["Ls"], ["0", "1", "3"])
        for m in t["modelos"]:
            self.assertEqual(set(t["ineditos"][m]), set(t["oficiais"][m]))
        # ! Alteração de IA - Revisar: (06/10/2026) o Coder 7B entra na aba quando a corrida 7 está no disco, e as duas
        # corridas opcionais ganham tabelas lidas de analise_fase3b.json (modelo contra modelo; adesão cega A5).
        # ! Motivo: o Eric rodou as corridas 5 e 7 em 06/10; sem isto a aba continuaria dizendo que só o qwen e o 3B rodaram.
        an = self.ctx.get("analise3b") or {}
        secao = self.html[self.html.index('<section id="tresb"'):].split("</section>")[0]
        if (gd.EXP / "resultados_alvo" / "fase3b_ineditos_coder7b" / "resumo_fase3.json").exists():
            self.assertIn("qwen2.5-coder:7b", t["modelos"])
        self.assertEqual(secao.count("<tr data-entre-modelos="), len(an.get("ineditos", {}).get("entre_modelos", [])))
        self.assertEqual(secao.count("<tr data-a5="), len(an.get("a5", {}).get("linhas", [])))
        for l in an.get("a5", {}).get("linhas", []):
            self.assertIn(f'{l["seguiu"]} ({tp.fmt(l["seguiu_pct"])}%)', secao)

    # ! Alteração de IA - Revisar: teste novo (30/09/2026, noite): o painel lista todas as pontes de versão da
    # decisão, cada uma com a versão do Ollama da própria saída, e marca como divergente quem passa de b + c = 2.
    # ! Motivo: a ponte em 0.34.4 (`fase3b_ponte_0344`) deu o Coder 7B com b + c = 4; o painel lia só a saída
    # `fase3b_ponte` (0.34.1) pelo nome fixo e continuaria dizendo que a ponte é pareável.
    def teste_pontes_de_versao_lidas_da_decisao(self):
        tres_b = self.ctx["dados"]["tres_b"]
        esperadas = [nome for nome, s in tres_b.items() if s.get("modo") == "ponte"]
        pontes = self.ctx["dados"]["pontes"]
        self.assertEqual([p["saida"] for p in pontes], esperadas)
        secao = self.html[self.html.index('<section id="tresb"'):].split("</section>")[0]
        for p in pontes:
            self.assertRegex(p["versao"], r"^\d+\.\d+\.\d+$", p["saida"])
            self.assertIn(f'Ollama {p["versao"]}', secao)
            for x in p["linhas"]:
                self.assertEqual(x["pareavel"], x["b"] + x["c"] <= 2, (p["saida"], x["modelo"]))
        n_divergentes = sum(not x["pareavel"] for p in pontes for x in p["linhas"])
        self.assertEqual(secao.count("<td>divergente</td>"), n_divergentes)
        self.assertEqual(secao.count("<td>pareável</td>"), sum(len(p["linhas"]) for p in pontes) - n_divergentes)
        ultima = pontes[-1]
        n_ok = sum(x["pareavel"] for x in ultima["linhas"])
        self.assertTrue(re.search(rf'<b[^>]*>{n_ok} de {len(ultima["linhas"])} pareáveis</b>', secao), "cartão da ponte mais recente")

    # ! Alteração de IA - Revisar: teste novo (30/09/2026, noite): nenhuma aba pode sair com os asteriscos do
    # negrito do Markdown à vista (fora de trechos de código).
    # ! Motivo: na primeira versão do §2.3 do roadmap o negrito tinha nome de modelo entre crases dentro
    # (`**O `qwen2.5-coder:3b` e o ...**`); o conversor de painel_textos separava primeiro os trechos entre crases
    # e só depois procurava o negrito, então os `**` saíram literais nas abas Roadmap e Fase 3-B. O mesmo defeito
    # já estava publicado na tabela §1 do roadmap (`**decisão 52: `qwen2.5:7b` com L1**`) sem ninguém notar.
    def teste_nenhuma_aba_com_asteriscos_de_negrito_a_vista(self):
        html = gd.pagina(self.ctx["dados"] | {"topicos": self.dados_t}, gd.blocos_tabelas(gd.F3 / "tabelas_relatorio.md"), {},
                         pt.ler_pendencias(gd.MEMORIAL / "pendencias.md"), self.ctx["road"], self.html)
        ids = re.findall(r'<section id="([a-z0-9_-]+)"', html)
        self.assertGreaterEqual(len(ids), 18)
        for sid in ids:
            secao = html[html.index(f'<section id="{sid}"'):].split("</section>")[0]
            sem_codigo = re.sub(r"<(code|pre)\b[^>]*>.*?</\1>", "", secao, flags=re.S)
            achado = re.search(r".{0,60}\*\*.{0,60}", sem_codigo)
            self.assertIsNone(achado, f"aba {sid}: negrito do Markdown não convertido em {achado.group(0)!r}" if achado else "")

    # ! Alteração de IA - Revisar: dois testes novos (01/10/2026) para as abas Troca cruzada e Fechamento.
    # ! Motivo: as duas abas nasceram na integração da Fase 3-B; a primeira mostra os pareamentos da cruzada, que
    # decidem a leitura "o ganho é do par modelo e biblioteca", e a segunda responde se as Fases 3 e 3-B podem
    # ser dadas por concluídas. Um número trocado ali mudaria a decisão que o Eric toma pelo painel.
    def teste_cruzada_usa_os_numeros_da_analise(self):
        an = self.ctx["analise3b"]
        secao = self.html[self.html.index('<section id="cruzada"'):].split("</section>")[0]
        t = self.dados_t["cruzada"]
        self.assertEqual(t["versoes"], ["0", "1", "3"])
        self.assertEqual(t["leitores"], an["metadados"]["leitores"])
        cel = {(c["leitor"], c["origem"], c["biblioteca_epoca"]): c for c in an["cruzada"]["celulas"]}
        for m in t["leitores"]:
            self.assertEqual(set(t["doador_lido"][m]), {"0", "1", "3"})
            self.assertEqual(t["doador_lido"][m]["0"]["acerto"], cel[(m, "ponte", 0)]["acerto_pct"])
            self.assertEqual(t["doador_lido"][m]["1"]["acerto"], cel[(m, "cruzada", 1)]["acerto_pct"])
            self.assertEqual(t["propria"][m]["3"]["bal"], cel[(m, "fase3", 3)]["acuracia_balanceada_pct"])
        par = {(p["leitor"], p["biblioteca_epoca"]): p for p in an["cruzada"]["pareados"] if p["contra"] == "l0_ponte"}
        for linha in t["trocas"]:
            if linha["leitor"] in t["leitores"]:
                self.assertEqual((linha["b"], linha["c"]), (par[(linha["leitor"], linha["epoca"])]["b"], par[(linha["leitor"], linha["epoca"])]["c"]))
        self.assertEqual(len(t["trocas"]), 2 + 2 * len(t["leitores"]))
        self.assertEqual(secao.count("<tr data-valor="), len(an["cruzada"]["pareados"]))
        for sel in ("g-cz-leit", "g-cz-trocas"):
            self.assertIn(f'id="{sel}"', secao)

    def teste_fechamento_conta_os_topicos_do_relatorio(self):
        secao = self.html[self.html.index('<section id="fechamento"'):].split("</section>")[0]
        md = pt.sem_comentarios(self.ctx["relatorio3b"])
        corpo = next(c for titulo, c in pt.secoes(md) if titulo.startswith("9. "))
        _, linhas, _ = pt.primeira_tabela(corpo)
        self.assertGreaterEqual(len(linhas), 20)
        self.assertEqual(secao.count("<tr data-valor="), len(linhas))
        t = self.dados_t["fechamento"]
        self.assertEqual(sum(t["contagem"].values()), len(linhas))
        self.assertNotIn("outro", t["contagem"], "tópico do fechamento com estado fora do vocabulário")
        abertas = [f for b in self.ctx["pend"] for f in b.fichas if f.aberta]
        self.assertEqual(t["fichas_abertas"], len(abertas))
        for f in abertas:
            self.assertIn(f'data-ir="pendencias|{f.id_html}"', secao)

    # ! Alteração de IA - Revisar: teste novo (01/10/2026) para a primeira aba da Pré-Fase 4, "Modelos grandes pelo disco".
    # ! Motivo: a aba responde se o colibri serve a esta máquina, com a conta de viabilidade_modelos_grandes.json, a
    # medição do disco e a amostra de probabilidades do Ollama; é por ela que o Eric lê o veredito, e um número
    # trocado (quantas famílias cabem, quantos minutos por resposta) inverteria a leitura.
    def teste_colibri_usa_os_numeros_da_viabilidade(self):
        v = self.ctx["viabilidade"]
        self.assertIsNotNone(v, "falta resultados_alvo/pre_fase4/viabilidade_modelos_grandes.json")
        secao = self.html[self.html.index('<section id="colibri"'):].split("</section>")[0]
        # o veredito tem três estados: roda com folga, fica no limite (cabe no disco livre e pede exatamente a RAM instalada) ou não roda
        rodam = [f["nome"] for f in v["familias"] if f["roda"] == "sim"]
        limite = [f["nome"] for f in v["familias"] if f["roda"] == "no_limite"]
        self.assertIn(f"<b>{len(rodam)} de {len(v['familias'])}</b>", secao)
        self.assertEqual(secao.count("<tr data-familia="), len(v["familias"]))
        self.assertEqual(secao.count('data-veredito="sim"'), len(rodam))
        self.assertEqual(secao.count('data-veredito="no_limite"'), len(limite))
        self.assertEqual(secao.count('data-veredito="nao"'), len(v["familias"]) - len(rodam) - len(limite))
        self.assertNotIn("passa da instalada", secao, "a máquina está no mínimo de RAM declarado, não abaixo dele")
        t = self.dados_t["colibri"]
        self.assertEqual(len(t["barras"]), 1 + len(v["medidas_de_terceiros"]))
        self.assertTrue(t["barras"][0]["hoje"])
        self.assertEqual(t["barras"][0]["minutos"], round(v["medianas_do_agente"]["segundos"] / 60, 2))
        for b, m in zip(t["barras"][1:], v["medidas_de_terceiros"]):
            self.assertEqual(b["minutos"], round(m["minutos_por_resposta"], 2))
        self.assertIn('id="g-co-min"', secao)
        sem_codigo = re.sub(r"<(code|pre)\b[^>]*>.*?</\1>", "", secao, flags=re.S)
        self.assertNotIn("—", sem_codigo, "texto novo do painel sem travessão")
        self.assertNotIn("→", sem_codigo)
        if self.ctx["logprobs_amostra"]:
            self.assertGreaterEqual(secao.count('class="tok"'), 5, "a amostra mostra a probabilidade token a token")
            self.assertIn("<tr data-alternativa=", secao)
        for numero in ("11", "12", "13"):
            self.assertIn(f'id="corrida-{numero}-co"', secao)

    # ! Alteração de IA - Revisar: teste novo (01/10/2026) para a aba "Raciocínio aberto" da Pré-Fase 4.
    # ! Motivo: a aba mostra o que as trilhas remontadas das corridas gravadas permitem conferir sem o gabarito e um
    # relatório de caso inteiro; os números vêm de indicadores_raciocinio.json, e o relatório de exemplo precisa
    # sair com as três camadas e com os blocos de código preservados.
    def teste_raciocinio_usa_os_indicadores_e_mostra_um_relatorio(self):
        ind = self.ctx["indicadores_raciocinio"]
        self.assertIsNotNone(ind, "falta resultados_alvo/pre_fase4/indicadores_raciocinio.json")
        secao = self.html[self.html.index('<section id="raciocinio"'):].split("</section>")[0]
        total = sum(c["diagnosticos"] for c in ind["corridas"])
        sem = sum(c["sem_raciocinio_antes_das_linhas"] for c in ind["corridas"])
        self.assertIn(f"<b>{sem} de {total}</b>", secao)
        self.assertEqual(secao.count("<tr data-conferencia="), sum(len(c["conferencias"]) for c in ind["corridas"]))
        t = self.dados_t["raciocinio"]
        self.assertEqual(len(t["trilhas"]), len(ind["corridas"]))
        for linha, c in zip(t["trilhas"], ind["corridas"]):
            self.assertEqual(linha["sustentado"], c["acerto_por_sustentacao"]["sustentado"]["acerto_pct"])
            self.assertEqual(linha["n_nao"], c["acerto_por_sustentacao"]["nao_sustentado"]["n"])
        self.assertIn('id="g-ra-sus"', secao)
        # ! Alteração de IA - Revisar: (06/10/2026) a sonda de confiança (corrida 12) entra na aba, lida de confianca.json.
        # ! Motivo: a aba prometia a análise da probabilidade do rótulo "quando a corrida 12 terminar"; ela terminou em 06/10.
        conf = self.ctx.get("confianca")
        if conf:
            tot = conf["resumos"][0]
            self.assertIn(f'<b>{tp.fmt(tot["sinais"]["p_conjunta"]["auroc"], 3)}</b>', secao)
            self.assertIn('id="g-ra-conf"', secao)
            self.assertEqual(len(t["confianca"]["bibliotecas"]), len(conf["resumos"]) - 1)
            self.assertEqual(secao.count("<tr data-conf-acerto="), len(conf["acerto"]))
            self.assertNotIn("quando a rodada B da pesquisa e a corrida 12 terminarem", secao)
        if self.ctx["relatorio_exemplo"]:
            for titulo in ("O que o programa fez", "O que o modelo declarou", "O que o código conferiu", "Avaliação contra o gabarito"):
                self.assertIn(f"<h4>{titulo}</h4>", secao)
            self.assertIn('<pre class="bruto"><code>', secao)
            self.assertNotIn("```", secao, "cerca de código do Markdown não convertida")
        sem_codigo = re.sub(r"<(code|pre)\b[^>]*>.*?</\1>", "", secao, flags=re.S)
        self.assertNotIn("—", sem_codigo, "texto novo do painel sem travessão")
        self.assertNotIn("→", sem_codigo)

    # ! Alteração de IA - Revisar: teste novo (01/10/2026) para o explorador de casos da aba "Raciocínio aberto".
    # ! Motivo: o explorador mostra, para qualquer caso das trilhas versionadas, as três camadas lado a lado (o que o
    # programa fez, o que o modelo declarou, o que o código conferiu) e, à parte, a avaliação contra o gabarito. O
    # recorte que vai para a página tem de trazer todos os diagnósticos das trilhas, com a causa que o avaliador leu.
    def teste_raciocinio_tem_o_explorador_de_casos(self):
        ind = self.ctx["indicadores_raciocinio"]
        trilhas = self.ctx["trilhas"]
        self.assertTrue(trilhas, "faltam as trilhas em resultados_alvo/pre_fase4/trilhas/")
        ex = self.dados_t["raciocinio"]["explorador"]
        self.assertEqual(len(ex["trilhas"]), len(ind["corridas"]))
        self.assertEqual(sum(len(t["casos"]) for t in ex["trilhas"]), sum(c["diagnosticos"] for c in ind["corridas"]))
        for t in ex["trilhas"]:
            eventos = trilhas[t["arquivo"]]
            causas = {e["trilha"]: e["dados"].get("lido") for e in eventos if e["tipo"] == "declaracao" and e["dados"]["campo"] == "causa_raiz"}
            for c in t["casos"]:
                self.assertEqual(c["modelo"]["causa"], causas[c["trilha"]], c["trilha"])
                self.assertEqual(len([x for x in c["programa"]["candidatos"] if x["entregue"]]), 3, c["trilha"])
                self.assertTrue(c["conferencias"] and all("usa_gabarito" not in x for x in c["conferencias"]))
                self.assertEqual({x["regra"] for x in c["avaliacao"]}, {"causa_correta", "campo_correto", "verbete_de_ouro_no_contexto"})
        secao = self.html[self.html.index('<section id="raciocinio"'):].split("</section>")[0]
        self.assertIn('class="ra-explorador"', secao)
        self.assertIn('class="ra-sel-trilha"', secao)
        self.assertIn("function raExplorar(", tp.JS_TOPICOS)
        self.assertIn("raExplorar", tp.DESENHAR_TOPICOS["raciocinio"])

    def teste_curadoria_conta_as_edicoes_da_planilha(self):
        total = sum(sum(v.values()) for v in self.dados_t["curadoria"]["por"].values())
        self.assertEqual(total, self.ctx["curadoria"]["edicoes_na_epoca"])

    def teste_mapa_de_filtros_sem_asteriscos_e_com_vereditos_contados(self):
        secao = self.html[self.html.index('<section id="pesquisa"'):]
        self.assertNotIn("**", secao.split("</section>")[0])
        self.assertRegex(secao, r'data-valor="adotado" aria-pressed="false">Adotado \(\d+\)')
        self.assertNotIn('data-valor="outro"', secao.split("</section>")[0])

    # ! Alteração de IA - Revisar: dois testes novos (01/10/2026) para a rodada 5 da pesquisa (Pré-Fase 4) no painel.
    # ! Motivo: (1) a aba Pesquisa lia o mapa de filtros "do último levantamento da lista"; com a rodada 5 na lista ela
    # passaria a procurar o §6.13.10 no arquivo errado e a geração do painel pararia; o mapa de filtros é o da rodada
    # 4 e tem de ser lido do arquivo dela. (2) A aba "Modelos grandes pelo disco" mostra o mapa adotado, adiado,
    # descartado da parte A, lido do levantamento §6.14.13; os vereditos contados no painel têm de ser os do arquivo.
    def teste_pesquisa_lista_a_rodada_5_e_le_o_mapa_de_filtros_da_rodada_4(self):
        secao = self.html[self.html.index('<section id="pesquisa"'):].split("</section>")[0]
        r4 = (tp.PESQUISA / "levantamento-2026-09-29-documentacao-autogerida.md").read_text(encoding="utf-8")
        _, filtros, _ = pt.primeira_tabela(r4[r4.index("#### 6.13.10"):])
        self.assertEqual(secao.count("<tr data-valor="), len(filtros))
        r5 = (tp.PESQUISA / tp.LEVANTAMENTO_PRE_FASE4).read_text(encoding="utf-8")
        topicos_r5 = [l for l in r5.splitlines() if tp._TOPICO.match(l)]
        self.assertGreaterEqual(len(topicos_r5), 5)
        for l in topicos_r5:
            self.assertIn(f"§{tp._TOPICO.match(l).group(1)} ", secao)
        self.assertIn("Rodada 5 (01/10): Pré-Fase 4", secao)
        self.assertNotIn("Quatro rodadas", secao)
        n_ref = sum(1 for l in (tp.PESQUISA / "referencias.md").read_text(encoding="utf-8").splitlines() if l.startswith("- "))
        self.assertIn(f"<b>{n_ref}</b>", secao)
        self.assertIn('data-ir="colibri|"', secao, "a aba Pesquisa leva ao mapa de viabilidade da aba do colibri")

    def teste_colibri_mostra_o_mapa_da_literatura(self):
        r5 = (tp.PESQUISA / tp.LEVANTAMENTO_PRE_FASE4).read_text(encoding="utf-8")
        trecho = r5[r5.index("#### 6.14.13"):]
        cab, linhas, _ = pt.primeira_tabela(trecho)
        self.assertGreaterEqual(len(linhas), 20)
        i_v = cab.index("Veredito")
        cont = {}
        for r in linhas:
            v = re.sub(r"[*`_]", "", r[i_v]).strip().lower()
            cont[v] = cont.get(v, 0) + 1
        self.assertEqual(set(cont), {"adotado", "adiado", "descartado"})
        secao = self.html[self.html.index('<section id="colibri"'):].split("</section>")[0]
        self.assertIn('id="tab-mapa-co"', secao)
        self.assertEqual(secao.count("<tr data-valor="), len(linhas))
        for v, n in cont.items():
            self.assertIn(f'data-valor="{v}" aria-pressed="false">{v.capitalize()} ({n})</button>', secao)
        _, riscos, _ = pt.primeira_tabela(trecho[trecho.index("**Riscos**"):])
        self.assertEqual(secao.count("<tr data-risco="), len(riscos))
        self.assertNotIn("entra nesta aba quando for integrada", secao)
        sem_codigo = re.sub(r"<(code|pre)\b[^>]*>.*?</\1>", "", secao, flags=re.S)
        self.assertNotIn("**", sem_codigo)
        self.assertIn(f"<b>{cont['adotado']} adotadas</b>", secao)
        # ! Alteração de IA - Revisar: (05/10/2026) os avisos do cabeçalho do levantamento sobre a memória da máquina e
        # sobre as correções da revisão aparecem na aba, lidos do arquivo, e o texto das sínteses mostrado é o corrigido.
        # ! Motivo: o Eric decide pelo painel; sem os avisos ele leria as sínteses corrigidas sem saber que foram corrigidas
        # nem por quê, e a aba mostraria "15,69 GB" sem a nota de que a máquina tem 16 GB instalados.
        for aviso in ("O que mudou depois de a parte A ser escrita", "Memória da máquina", "Correções da revisão"):
            if re.search(r"^\d+\. \*\*" + re.escape(aviso) + r"\.\*\* ", r5, re.M):
                self.assertIn(f'<p class="nota"><strong>{aviso}.</strong> ', secao, aviso)
        if "**Correções feitas depois da revisão**" in r5:
            self.assertIn("trechos foram corrigidos por script", secao)
            self.assertNotIn("abaixo dos 16 GB mínimos do colibri", secao)

    # ! Alteração de IA - Revisar: teste novo (01/10/2026) para a aba "Atlas" da Pré-Fase 4.
    # ! Motivo: a aba desenha o mapa dos verbetes em SVG no próprio Python (o primeiro quadro tem de ser legível sem
    # script) e entrega ao script da página um recorte do atlas.json; os números-chave, a quantidade de nós e as trocas
    # entre causas têm de ser os do arquivo, e o passeio guiado não pode citar verbete ou caso que a página não tenha.
    def teste_atlas_desenha_o_mapa_e_usa_os_numeros_do_atlas(self):
        at = self.ctx["atlas"]
        self.assertIsNotNone(at, "falta resultados_alvo/pre_fase4/atlas.json")
        secao = self.html[self.html.index('<section id="atlas"'):].split("</section>")[0]
        t = self.dados_t["atlas"]
        meta = at["metadados"]
        f = next(x for x in at["fatias"] if x["id"] == meta["fatia_decidida"])
        b = at["bibliotecas"][f["biblioteca"]]
        self.assertEqual(t["padrao"], {"bib": f["biblioteca"], "fatia": f["id"]})
        # um nó por verbete da união das bibliotecas mostradas; os da biblioteca decidida já vêm posicionados
        todos = {i for x in t["bibs"].values() for i in x["verbetes"]}
        self.assertEqual(secao.count('<g class="at-no'), len(todos))
        self.assertEqual(secao.count('style="transform:translate('), len(b["verbetes"]))
        for h in t["bibs"]:
            self.assertEqual(set(t["bibs"][h]["verbetes"]), set(at["bibliotecas"][h]["verbetes"]))
        cont = b["contagem_por_rotulo"]
        self.assertIn(f'<b>{cont["especialista"]} de {len(b["verbetes"])}</b>', secao)
        self.assertIn(f'<b>{cont["nunca_recuperado"]}</b>', secao)
        loo = b["validacao"]["deixando_um_de_fora"]
        self.assertIn(f'{loo["acertos"]} de {loo["total"]}', secao)
        # as fatias da página são fatias do atlas, com as rotas dos mesmos casos
        ids = {x["id"] for x in at["fatias"]}
        for x in t["fatias"]:
            self.assertIn(x["id"], ids)
            original = next(y for y in at["fatias"] if y["id"] == x["id"])
            self.assertEqual(len(x["rotas"]), original["casos"])
            self.assertEqual(sum(1 for r in x["rotas"].values() if r["ok"]), original["acertos"])
        # a figura das trocas sai com as trocas da fatia decidida
        self.assertEqual(secao.count('<path class="at-aresta"'), len(f["confusoes"]))
        self.assertEqual(secao.count('<g class="at-causa"'), len(at["causas"]))
        # o passeio guiado só aponta para o que a página tem
        self.assertGreaterEqual(len(t["paradas"]), 4)
        for p in t["paradas"]:
            fatia = next(x for x in t["fatias"] if x["id"] == p["fatia"])
            self.assertEqual(fatia["bib"], p["bib"])
            if p.get("no"):
                self.assertIn(p["no"], t["bibs"][p["bib"]]["verbetes"])
            if p.get("caso"):
                self.assertIn(p["caso"], fatia["rotas"])
        sem_codigo = re.sub(r"<(code|pre)\b[^>]*>.*?</\1>", "", secao, flags=re.S)
        self.assertNotIn("—", sem_codigo, "texto novo do painel sem travessão")
        self.assertNotIn("→", sem_codigo)
        self.assertIn("function atlasIniciar(", tp.JS_TOPICOS)

    # ! Alteração de IA - Revisar: teste novo (01/10/2026): a aba Atlas mostra a validação do texto do Gemini, lida do
    # relatório da Pré-Fase 4 (§3.1), uma linha por afirmação, com o veredito em destaque.
    # ! Motivo: o Eric pediu que a descrição do Gemini fosse validada; a resposta fica no relatório e o painel é onde
    # ele a lê. Se o título da subseção mudar no relatório, a aba perderia a tabela sem ninguém notar.
    def teste_atlas_traz_a_validacao_do_texto_do_gemini(self):
        md = pt.sem_comentarios((gd.MEMORIAL / "3-resultados-e-analises" / "pre-fase-4-relatorio.md").read_text(encoding="utf-8"))
        trecho = md[md.index("### 3.1 "):]
        trecho = trecho[:trecho.index("\n### ", 4)]
        cab, linhas, _ = pt.primeira_tabela(trecho)
        self.assertEqual(cab[:2], ["O que o Gemini afirmou", "Veredito"])
        self.assertGreaterEqual(len(linhas), 8)
        secao = self.html[self.html.index('<section id="atlas"'):].split("</section>")[0]
        self.assertEqual(secao.count("<tr data-afirmacao="), len(linhas))
        self.assertIn("position is measured routing affinity, not a learned embedding", secao)
        vereditos = re.findall(r'<tr data-afirmacao="\d+" data-veredito="([a-z]+)"', secao)
        self.assertEqual(len(vereditos), len(linhas))
        self.assertTrue(set(vereditos) <= {"certo", "ressalva", "errado"}, vereditos)
        self.assertEqual(vereditos.count("errado"), sum(1 for r in linhas if r[1].strip().lower().startswith("errado")))

    def teste_funcoes_de_grafico_e_seletores_existem(self):
        for funcs in tp.DESENHAR_TOPICOS.values():
            for f in funcs:
                self.assertIn(f"function {f}(", tp.JS_TOPICOS, f)
        for sel, f in tp.SELETORES_TOPICOS.items():
            self.assertIn(f'id="{sel}"', self.html, sel)
            self.assertIn(f"function {f}(", tp.JS_TOPICOS, f)

    def teste_slots_cobrem_os_modelos_das_fases(self):
        for m in self.ctx["dados"]["modelos"]:
            self.assertIn(m, tp.SLOTS)
        for x in self.ctx["ablacao"]["por_modelo_condicao"]:
            self.assertIn(x["modelo"], tp.SLOTS)

    def teste_dados_dos_topicos_sao_serializaveis(self):
        json.dumps(self.dados_t, ensure_ascii=False)


if __name__ == "__main__":
    unittest.main(verbosity=1)
