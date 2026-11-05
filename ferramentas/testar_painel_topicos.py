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
        **gd.contexto_fase4(),
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
        # ! Alteração de IA - Revisar: (27/10/2026) o grupo "Fase 4" entra depois da Pré-Fase 4, com a aba "Reprodução na tela".
        # ! Motivo: a Fase 4 abriu em 26/10 e a corrida 17 é a primeira análise dela; o grupo fica na ordem cronológica, logo
        # depois da pesquisa que a preparou, sem mexer na ordem por importância que o Eric pediu para os grupos anteriores.
        self.assertEqual([g for g, _ in tp.NAV], ["Projeto", "Decisão e resultados", "Biblioteca gerida pelo modelo", "Pré-Fase 4", "Fase 4", "Pesquisa e método", "Fases anteriores"])
        # ! Alteração de IA - Revisar: (05/11/2026, P8) o grupo "Fase 4" passa a abrir pela aba "Fechamento da fase".
        # ! Motivo: a regra do mapa é a aba mais importante de cada grupo em primeiro, e com a fase fechada essa é a do fechamento.
        self.assertEqual([abas[0][0] for _, abas in tp.NAV], ["inicio", "decisao", "fase3", "colibri", "fechamentof4", "pesquisa", "fases2"])
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
        # ! Alteração de IA - Revisar: (23/10/2026) a repetição dos inéditos (corrida 15) entra na aba com o saldo lido de analise_fase3b.json.
        # ! Motivo: a ficha 21 fechou pela repetição; a aba precisa mostrar o número da corrida 15 ao lado do da corrida 7.
        for x in cq.get("confronto_ineditos_repeticao", []):
            if x["L"] == 1:
                self.assertIn(f'<b>{x["so_qwen"]} × {x["so_coder"]}</b>', secao)
                self.assertIn("corrida 15", secao)
                self.assertIn("decisão 73", secao)

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
    # descartado da parte A, lido do levantamento §6.14.16 (era §6.14.13 até 23/10/2026; o número vem do arquivo); os
    # vereditos contados no painel têm de ser os do arquivo.
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

    # ! Alteração de IA - Revisar: (23/10/2026) teste do bloco da literatura da parte B (onda 1) na aba "Raciocínio aberto".
    # ! Motivo: a aba mostra o mapa de arquitetura da trilha lido do levantamento §6.14 (mapa "Parte B, onda 1"); os vereditos
    # contados no painel têm de ser os do arquivo, as cinco sínteses têm de estar lá, e a frase antiga "entra nesta aba quando
    # a rodada B terminar" tem de sumir quando a onda 1 estiver integrada.
    def teste_raciocinio_mostra_o_mapa_de_arquitetura_da_literatura(self):
        r5 = (tp.PESQUISA / tp.LEVANTAMENTO_PRE_FASE4).read_text(encoding="utf-8")
        blocos = tp._blocos_dos_mapas(r5[re.search(r"^#### 6\.14\.\d+ Mapas adotado", r5, re.M).start():])
        self.assertTrue(any(k.startswith("Parte A") for k in blocos), list(blocos))
        nome = next((k for k in blocos if k.startswith("Parte B, onda 1")), None)
        if not nome or "ainda não rodou" in blocos[nome]:
            self.skipTest("a onda 1 da parte B ainda não foi integrada ao levantamento")
        cab, linhas, _ = pt.primeira_tabela(blocos[nome])
        self.assertGreaterEqual(len(linhas), 18)
        i_v = cab.index("Veredito")
        cont = {}
        for r in linhas:
            v = re.sub(r"[*`_]", "", r[i_v]).strip().lower()
            cont[v] = cont.get(v, 0) + 1
        secao = self.html[self.html.index('<section id="raciocinio"'):].split("</section>")[0]
        self.assertIn('id="tab-mapa-ra"', secao)
        tab = secao[secao.index('id="tab-mapa-ra"'):].split("</table>")[0]
        self.assertEqual(tab.count("<tr data-valor="), len(linhas))
        filtros = secao[secao.index('data-alvo="tab-mapa-ra"'):].split("</div>")[0]
        for v, n in cont.items():
            self.assertIn(f'data-valor="{v}" aria-pressed="false">{v.capitalize()} ({n})</button>', filtros)
        for chave in tp.TOPICOS_RACIOCINIO:
            self.assertIn(f'data-sintese="{chave}"', secao)
        for chave in tp.TOPICOS_VISUALIZACAO:
            self.assertNotIn(f'data-sintese="{chave}"', secao)
        self.assertNotIn("entra nesta aba quando a rodada B da pesquisa terminar", secao)
        self.assertIn(f'{cont.get("adotado", 0)} adotadas', secao)
        # a aba do colibri continua com o mapa da parte A, não com o da parte B
        colibri = self.html[self.html.index('<section id="colibri"'):].split("</section>")[0]
        cab_a, linhas_a, _ = pt.primeira_tabela(blocos[next(k for k in blocos if k.startswith("Parte A"))])
        self.assertEqual(colibri[colibri.index('id="tab-mapa-co"'):].split("</table>")[0].count("<tr data-valor="), len(linhas_a))

    # ! Alteração de IA - Revisar: (23/10/2026) teste da aba "Cérebro e memória" (onda 2 da parte B): mapa, gráfico por tema e as quatro sínteses.
    # ! Motivo: a aba responde às perguntas do Eric de 23/10 (cérebro ao vivo, Brainiac, grafos) só com o levantamento §6.14; os
    # vereditos contados no painel e no gráfico têm de ser os do arquivo.
    def teste_cerebro_mostra_o_mapa_da_onda_2(self):
        r5 = (tp.PESQUISA / tp.LEVANTAMENTO_PRE_FASE4).read_text(encoding="utf-8")
        blocos = tp._blocos_dos_mapas(r5[re.search(r"^#### 6\.14\.\d+ Mapas adotado", r5, re.M).start():])
        nome = next((k for k in blocos if k.startswith("Parte B, onda 2")), None)
        if not nome or "ainda não rodou" in blocos[nome]:
            self.skipTest("a onda 2 da parte B ainda não foi integrada ao levantamento")
        cab, linhas, _ = pt.primeira_tabela(blocos[nome])
        self.assertGreaterEqual(len(linhas), 18)
        secao = self.html[self.html.index('<section id="cerebro"'):].split("</section>")[0]
        tab = secao[secao.index('id="tab-mapa-ce"'):].split("</table>")[0]
        self.assertEqual(tab.count("<tr data-valor="), len(linhas))
        temas = self.dados_t["cerebro"]["temas"]
        self.assertEqual(sum(t["adotado"] + t["adiado"] + t["descartado"] + t["outro"] for t in temas), len(linhas))
        self.assertEqual(len(temas), len({re.sub(r"[*`_]", "", r[cab.index("Tema")]).strip() for r in linhas}))
        self.assertIn('id="g-ce-temas"', secao)
        self.assertIn("ceTemas", tp.DESENHAR_TOPICOS["cerebro"])
        for chave in tp.TOPICOS_VISUALIZACAO:
            self.assertIn(f'data-sintese="{chave}"', secao)
        for chave in tp.TOPICOS_RACIOCINIO:
            self.assertNotIn(f'data-sintese="{chave}"', secao)
        self.assertIn(f'{sum(t["adotado"] for t in temas)} servem agora', secao)
        self.assertNotIn("—", secao.split("<details")[0])

    def teste_colibri_mostra_o_mapa_da_literatura(self):
        r5 = (tp.PESQUISA / tp.LEVANTAMENTO_PRE_FASE4).read_text(encoding="utf-8")
        trecho = r5[re.search(r"^#### 6\.14\.\d+ Mapas adotado", r5, re.M).start():]
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

    # ! Alteração de IA - Revisar: teste novo (27/10/2026) da aba "Reprodução na tela" (Fase 4).
    # ! Motivo: a aba lê reproducibilidade.json (corrida 17) e reproducibilidade_ineditos.json (os 36 inéditos da ficha 27);
    # os números-chave, a soma por classe e os dados do gráfico precisam bater com os JSON, e a aba tem de existir mesmo
    # sem os arquivos (estado vazio), como as da Pré-Fase 4.
    def teste_reproducao_usa_os_numeros_dos_json(self):
        rep, ined = self.ctx.get("reproducao"), self.ctx.get("reproducao_ineditos")
        secao = self.html[self.html.index('<section id="reproducao"'):].split("</section>")[0]
        t = self.dados_t["reproducao"]
        self.assertEqual([c["classe"] for c in t["classes"]], [1, 2, 3, 4, 5, 6])
        self.assertIn("function repClasses(", tp.JS_TOPICOS)
        d, h = tp.secao_reproducao(None, None, self.ctx["road"], gd.cartoes_corridas)
        self.assertIn('<section id="reproducao"', h)
        self.assertIn("ainda não foi rodada", h)
        self.assertTrue(all(c["avaliacao"] is None for c in d["classes"]))
        if not rep:
            self.assertIn("ainda não foi rodada", secao)
            return
        r = rep["resumo"]
        self.assertIn(f'>{r["reproduzem"]} de {r["casos"]}</b>', secao)
        self.assertEqual(sum(c["avaliacao"]["reproduzem"] for c in t["classes"]), r["reproduzem"])
        self.assertEqual(sum(c["avaliacao"]["casos"] for c in t["classes"]), r["casos"])
        self.assertIn(f'{tp.fmt(rep["tempo"]["mediana_s"], 3)} s', secao)
        self.assertIn('id="g-rep-classe"', secao)
        self.assertIn("tb_f4_reproducao_resumo", secao)
        if ined:
            ri = ined["resumo"]
            self.assertIn(f'>{ri["reproduzem"]} de {ri["casos"]}</b>', secao)
            self.assertEqual(sum(c["ineditos"]["reproduzem"] for c in t["classes"]), ri["reproduzem"])
            self.assertEqual(t["rotulos"]["ineditos"], f'{ri["casos"]} inéditos')
        else:
            self.assertIn("ainda não rodada", secao)

    # ! Alteração de IA - Revisar: teste novo (27/10/2026, P3) da aba "Calibração" (Fase 4, corrida 16).
    # ! Motivo: a aba lê calibracao.json e limiares.json (avaliar_fase4.py --calibracao); os números-chave e os dados do
    # gráfico precisam bater com o JSON, e a aba tem de existir mesmo sem os arquivos (estado vazio), como as outras.
    def teste_calibracao_usa_os_numeros_dos_json(self):
        cal, lim = self.ctx.get("calibracao"), self.ctx.get("limiares")
        secao = self.html[self.html.index('<section id="calibracao"'):].split("</section>")[0]
        t = self.dados_t["calibracao"]
        self.assertIn("function calK(", tp.JS_TOPICOS)
        self.assertIn("function calCurva(", tp.JS_TOPICOS)
        d, h = tp.secao_calibracao(None, None, self.ctx["road"], gd.cartoes_corridas)
        self.assertIn('<section id="calibracao"', h)
        self.assertIn("ainda não foi rodada", h)
        self.assertEqual(d["por_k"], [])
        self.assertEqual(d["por_selo"], [])
        if not cal:
            self.assertIn("ainda não foi rodada", secao)
            return
        # (28/10/2026) os casos e os erros por selo saem do JSON (bloco tb_f4_calibracao_selos), nunca contados à mão
        if cal.get("por_selo"):
            self.assertEqual(t["por_selo"], cal["por_selo"])
            self.assertIn("tb_f4_calibracao_selos", secao)
            alto = next(x for x in cal["por_selo"] if x["selo"] == "alto")
            self.assertIn(f'{alto["errados"]} de {alto["casos"]}', secao)
        self.assertEqual([x["k"] for x in t["por_k"]], [x["k"] for x in cal["por_k"]])
        self.assertEqual([x["acertos"] for x in t["por_k"]], [x["acertos"] for x in cal["por_k"]])
        self.assertEqual(t["k_escolhido"], cal["k_escolhido"])
        self.assertIn(f'>k = {cal["k_escolhido"]}</b>', secao)
        self.assertIn('id="g-cal-k"', secao)
        self.assertIn("tb_f4_calibracao_resumo", secao)
        if cal.get("limiares"):
            self.assertEqual(t["limiares"]["baixo_ate"], cal["limiares"]["baixo_ate"])
            self.assertIn(tp.fmt(cal["limiares"]["baixo_ate"], 3), secao)
        if lim:
            self.assertEqual(lim["k"], cal["limiares"]["k"])

    def teste_tela_usa_os_numeros_dos_json(self):
        # (01/11/2026) a aba da corrida 18 lê tela.json: regra R2, acerto por classe e rótulos por lado, nunca digitados à mão
        tela = self.ctx.get("tela")
        secao = self.html[self.html.index('<section id="tela"'):].split("</section>")[0]
        t = self.dados_t["tela"]
        self.assertIn("function telaClasses(", tp.JS_TOPICOS)
        self.assertIn("function telaRotulos(", tp.JS_TOPICOS)
        d, h = tp.secao_tela(None, None, self.ctx["road"], gd.cartoes_corridas)
        self.assertIn('<section id="tela"', h)
        self.assertIn("ainda não foi rodada", h)
        self.assertEqual(d["por_classe"], [])
        if not tela:
            self.assertIn("ainda não foi rodada", secao)
            return
        r = tela["resumo"]
        # a repetição (18b): com a própria leitura como segunda corrida, a comparação fecha em zero mudanças
        d2, h2 = tp.secao_tela(tela, tela, self.ctx["road"], gd.cartoes_corridas)
        self.assertEqual(d2["v2"]["resumo"]["concordam"], r["concordam"])
        self.assertEqual((d2["v2"]["ganhos"], d2["v2"]["perdas"], d2["v2"]["mudaram"]), (0, 0, 0))
        self.assertIn("corrida 18b", h2)
        self.assertIn("Rótulo na tela (18b)", h2)
        v2 = self.ctx.get("tela_v2")
        if v2:
            self.assertEqual(t["v2"]["resumo"]["concordam"], v2["resumo"]["concordam"])
            self.assertIn("corrida 18b", secao)
        else:
            self.assertIsNone(t["v2"])
        self.assertEqual(t["resumo"]["concordam"], r["concordam"])
        self.assertEqual(t["resumo"]["discordantes"], r["b"] + r["c"])
        self.assertEqual([x["acerto_tela"] for x in t["por_classe"]], [x["acerto_tela"] for x in tela["por_classe"]])
        self.assertEqual(sum(x["tela"] for x in t["rotulos"]), r["casos"])
        self.assertEqual(sum(x["gabarito"] for x in t["rotulos"]), r["casos"])
        self.assertIn(f'{r["concordam"]} de {r["casos"]}', secao)
        self.assertIn('id="g-tela-classe"', secao)
        self.assertIn("tb_f4_tela_resumo", secao)

    def teste_cura_usa_os_numeros_do_json(self):
        # ! Alteração de IA - Revisar: (01/11/2026, P4) a aba da corrida 19 lê cura.json: taxa de cura, MTTR, mesmo elemento
        # contra outro elemento (regra R3) e as duas formas de quebra, nunca digitados à mão; sem o arquivo, o estado vazio.
        # ! Motivo: a regra do painel é uma aba por análise, lida dos JSON; o Eric decide pelo painel.
        cura = self.ctx.get("cura")
        secao = self.html[self.html.index('<section id="cura"'):].split("</section>")[0]
        self.assertIn("function curaModos(", tp.JS_TOPICOS)
        self.assertIn("function curaRoteiros(", tp.JS_TOPICOS)
        d, h = tp.secao_cura(None, self.ctx["road"], gd.cartoes_corridas)
        self.assertIn('<section id="cura"', h)
        self.assertIn("ainda não foi rodada", h)
        self.assertEqual(d["por_modo"], [])
        if not cura:
            self.assertIn("ainda não foi rodada", secao)
            return
        r = cura["resumo"]
        t = self.dados_t["cura"]
        self.assertEqual(t["resumo"]["curadas"], r["curadas"])
        self.assertEqual([x["curadas"] for x in t["por_modo"]], [x["curadas"] for x in cura["por_modo"]])
        self.assertEqual(sum(x["execucoes"] for x in t["por_roteiro"]), r["execucoes"])
        self.assertIn(f'{r["curadas"]} de {r["quebras_detectadas"]}', secao)
        self.assertIn('id="g-cura-modo"', secao)
        self.assertIn("tb_f4_cura_resumo", secao)
        self.assertIn("outro elemento", secao)

    def teste_biblioteca_usa_os_numeros_do_json(self):
        # ! Alteração de IA - Revisar: (03/11/2026, P5) a aba da corrida 20 lê biblioteca.json: edições no lote, o que cada filtro
        # barrou, a regra R5 (b e c nos inéditos), a regra R4 (precisão e revocação da marca corrigido) e a sonda, nunca digitados à
        # mão; sem o arquivo, o estado vazio.
        # ! Motivo: a regra do painel é uma aba por análise, lida dos JSON; o Eric decide pelo painel.
        bibl = self.ctx.get("biblioteca")
        secao = self.html[self.html.index('<section id="biblioteca"'):].split("</section>")[0]
        self.assertIn("function bibFiltros(", tp.JS_TOPICOS)
        self.assertIn("function bibReavaliacao(", tp.JS_TOPICOS)
        d, h = tp.secao_biblioteca(None, self.ctx["road"], gd.cartoes_corridas)
        self.assertIn('<section id="biblioteca"', h)
        self.assertIn("ainda não foi rodada", h)
        self.assertEqual(d["filtros"], [])
        if not bibl or not bibl.get("resumo") or not bibl["resumo"].get("casos"):
            self.assertIn("ainda não foi rodada", secao)
            return
        r = bibl["resumo"]
        t = self.dados_t["biblioteca"]
        self.assertEqual(t["resumo"]["aceitas"], r["aceitas"])
        self.assertEqual([x["recusas"] for x in t["filtros"]], [x["recusas"] for x in bibl["filtros"]])
        if bibl.get("reavaliacao"):
            self.assertEqual(t["reavaliacao"]["b"], bibl["reavaliacao"]["b"])
            self.assertIn(f'b = {bibl["reavaliacao"]["b"]}', secao)
        self.assertIn(f'{r["aceitas"]} de {r["propostas"]}', secao)
        self.assertIn('id="g-bib-filtros"', secao)
        self.assertIn("tb_f4_biblioteca_filtros", secao)
        self.assertIn("regra R4", secao.lower().replace("r4", "R4").replace("regra r4", "regra R4"))

    def teste_cenarios_usa_os_numeros_do_json(self):
        # ! Alteração de IA - Revisar: (04/11/2026, P6) a aba da corrida 21 lê cenarios.json: Task Success com Wilson, MTTR com
        # reamostragem, por tipo e por cenário, a ficha da falha de cada cenário e o protocolo da linha de base manual; sem o
        # arquivo, o estado vazio. Os dados sintéticos cobrem a aba com números enquanto a corrida 21 não roda.
        # ! Motivo: a regra do painel é uma aba por análise, lida dos JSON; o Eric decide pelo painel, e a ficha da falha de cada
        # cenário é o que o protocolo entrega ao integrante.
        self.assertIn("cenarios", [sid for _, abas in tp.NAV for sid, _, _ in abas])
        self.assertIn("function cenMttr(", tp.JS_TOPICOS)
        self.assertIn("function cenSucesso(", tp.JS_TOPICOS)
        d, h = tp.secao_cenarios(None, None, self.ctx["road"], gd.cartoes_corridas)
        self.assertIn('<section id="cenarios"', h)
        self.assertIn("ainda não foi rodada", h)
        self.assertIn("protocolo-linha-de-base-manual.md", h)
        self.assertEqual(d["por_cenario"], [])

        def linha(n: int, suc: int, mttr: float) -> dict:
            return {"n": n, "sucessos": suc, "task_success_pct": round(100 * suc / n, 1), "wilson_lo_pct": 10.0, "wilson_hi_pct": 90.0, "detectados": n,
                    "mttr_n": n, "mttr_media_s": mttr, "mttr_mediana_s": mttr, "mttr_ic_lo_s": mttr - 1, "mttr_ic_hi_s": mttr + 1}

        sint = {"metadados": {"gerado_em": "2026-11-04T20:00:00", "corrida": "fase4_ensaio"},
                "condicoes": {"repeticoes": 1, "modelo": "qwen2.5:7b", "versao_ollama": "0.40.14", "k": 3},
                "geral": linha(10, 7, 61.5), "por_tipo": [{"tipo": "contrato", **linha(6, 4, 70.25)}, {"tipo": "localizador", **linha(4, 3, 48.0)}],
                "por_cenario": [{"cenario": "contrato-type_drift", "tipo": "contrato", "modo": "type_drift", "classe": 3, "causa_esperada": "tipo_divergente",
                                 **linha(1, 1, 64.0), "rotulos": {"tipo_divergente": 1}, "segundos_media": 80.0,
                                 "fichas_da_falha": ["o roteiro passou na tela, mas o fio acusou: diff do contrato: tipo_diferente"]}],
                "tempo": {"execucoes": 10, "segundos_media": 90.5, "segundos_total": 905.0, "estimativa_fase5_h": 1.26},
                "deteccao": {"conferencia_do_roteiro": 4, "contrato_no_fio": 2, "passo_do_localizador": 4},
                "sem_task_success": [{"cenario": "localizador-front-admin-login", "repeticao": 1, "tipo": "localizador", "detectou": True, "rotulo": "localizador_quebrado",
                                      "causa_esperada": "localizador_quebrado", "falha_da_cura": "candidato_invalido", "segundos": 63.4}],
                "navegador": {"versoes": ["156.0.8078.4"], "unica": True}, "banco": {"hashes_de_inicio": ["h-seed"], "unico": True}}
        d, h = tp.secao_cenarios(sint, None, self.ctx["road"], gd.cartoes_corridas)
        # ! Alteração de IA - Revisar: (04/11/2026, leitura da corrida 21) as execuções sem Task Success aparecem na aba, com a falha da cura.
        # ! Motivo: o Eric decide pelo painel; na corrida 21 o zero do login precisa vir com o motivo, lido do JSON.
        self.assertIn("Execuções sem Task Success", h)
        self.assertIn("candidato_invalido", h)
        self.assertIn("tb_f4_cenarios_sem_sucesso", h)
        _, h_sem = tp.secao_cenarios({**sint, "sem_task_success": []}, None, self.ctx["road"], gd.cartoes_corridas)
        self.assertNotIn("Execuções sem Task Success", h_sem)
        # ! Alteração de IA - Revisar: (04/11/2026, corrida 21b) com a repetição, os números principais são os dela, a comparação fica cenário a
        # cenário e a execução sem Task Success da corrida 21 continua visível, com o nome da corrida.
        # ! Motivo: a 21b roda com a correção da cura e é a leitura vigente; a 21 é o registro de como o defeito apareceu e não pode sumir do painel.
        cena_v2 = {**sint["por_cenario"][0], **linha(1, 1, 70.5), "segundos_media": 86.0}
        v2 = {**sint, "geral": linha(10, 10, 66.25), "por_cenario": [cena_v2], "sem_task_success": [], "tempo": {**sint["tempo"], "estimativa_fase5_h": 1.5}}
        d2, h2 = tp.secao_cenarios(sint, v2, self.ctx["road"], gd.cartoes_corridas)
        self.assertEqual(d2["geral"]["sucessos"], 10)
        self.assertEqual([x["mttr_media_s"] for x in d2["por_cenario"]], [70.5])
        self.assertEqual([x["mttr_anterior"] for x in d2["por_cenario"]], [64.0])
        self.assertIn("corrida 21b", h2.split('<p class="lead">')[1].split("</p>")[0])
        self.assertIn("10 de 10", h2)
        self.assertIn("As duas corridas, cenário a cenário", h2)
        self.assertIn("candidato_invalido", h2)
        self.assertIn("cenarios_v2.json", h2)
        self.assertIn("66,2", h2)
        self.assertIn("1,50", h2)
        self.assertEqual(d["geral"]["sucessos"], 7)
        self.assertEqual([x["mttr_media_s"] for x in d["por_cenario"]], [64.0])
        self.assertIn("7 de 10", h)
        self.assertIn("o fio acusou: diff do contrato: tipo_diferente", h)
        self.assertIn('id="g-cen-mttr"', h)
        self.assertIn('id="g-cen-ts"', h)
        self.assertIn("tb_f4_cenarios_por_cenario", h)
        self.assertIn("1,26", h)
        self.assertNotIn("—", h.split('<p class="lead">')[1].split("</p>")[0], "a frase de abertura não leva travessão")
        cen_ = self.ctx.get("cenarios_v2") or self.ctx.get("cenarios")
        secao = self.html[self.html.index('<section id="cenarios"'):].split("</section>")[0]
        if not cen_ or not cen_.get("geral", {}).get("n"):
            self.assertIn("ainda não foi rodada", secao)
            return
        t = self.dados_t["cenarios"]
        self.assertEqual(t["geral"]["sucessos"], cen_["geral"]["sucessos"])
        self.assertEqual([x["sucessos"] for x in t["por_cenario"]], [x["sucessos"] for x in cen_["por_cenario"]])
        self.assertIn(f'{cen_["geral"]["sucessos"]} de {cen_["geral"]["n"]}', secao)

    def teste_trilha_usa_os_numeros_do_json(self):
        # ! Alteração de IA - Revisar: (04/11/2026, P7) a aba da corrida 22 lê trilha.json: TPR x TNR por sinal (contra o acaso 0,25), as
        # intervenções com o limite inferior, a sonda de pós-racionalização, as mutações (verbete trocado, contrato alterado, seletor
        # quebrado) com o nó previsto e a amostra dos 12 relatórios da sessão de revisão; sem o arquivo, o estado vazio. Os dados
        # sintéticos cobrem a aba enquanto a corrida 22 não roda.
        # ! Motivo: regra do painel (uma aba por análise, lida dos JSON); a avaliação da própria trilha é a sétima análise da Fase 4.
        self.assertIn("trilha", [sid for _, abas in tp.NAV for sid, _, _ in abas])
        self.assertIn("function triSinais(", tp.JS_TOPICOS)
        self.assertIn("function triMutacoes(", tp.JS_TOPICOS)
        d, h = tp.secao_trilha(None, self.ctx["road"], gd.cartoes_corridas)
        self.assertIn('<section id="trilha"', h)
        self.assertIn("ainda não foi rodada", h)
        self.assertEqual(d["sinais"], [])

        def sinal(nome: str, tpr, tnr) -> dict:
            return {"sinal": nome, "descricao": f"o sinal {nome}", "erros": 12, "acertos": 24, "vp": 8, "fn": 4, "fp": 6, "vn": 18, "tpr": tpr, "tnr": tnr,
                    "produto": None if tpr is None else round(tpr * tnr, 4), "acaso": 0.25}

        def mut(tipo: str, previsto: str, apl: int, prev: int, outro: int, sem: int, mudou: int, sem_alvo: int = 0) -> dict:
            return {"tipo": tipo, "no_previsto": previsto, "casos": apl + sem_alvo, "aplicaveis": apl, "sem_alvo": sem_alvo, "previsto": prev, "outro_no": outro,
                    "sem_divergencia": sem, "rotulo_mudou": mudou, "previsto_pct": round(100 * prev / apl, 1) if apl else None}

        sint = {"metadados": {"gerado_em": "2026-11-05T06:00:00", "corrida": "fase4_trilha"},
                "condicoes": {"modelo": "qwen2.5:7b", "versao_ollama": "0.40.14", "k": 3, "casos": 36, "inferencias_previstas": 296, "biblioteca": {"hash": "95af35290860"}},
                "resumo": {"casos": 36, "acertos": 24, "erros": 12, "acerto_pct": 66.7, "tpr": 0.6667, "tnr": 0.75, "produto": 0.5, "acaso": 0.25},
                "sinais": [sinal("divergencia", 0.6667, 0.75), sinal("por_gatilho", 0.6, 0.9), sinal("remocao_ou_troca", 0.5, 0.8), sinal("sem_documentacao", 0.9, 0.2), sinal("repeticao_mudou", 0.1, 0.95),
                           sinal("selo_baixo", 0.5, 0.9), sinal("falha", 0.25, 1.0), sinal("qualquer", 0.75, 0.7)],
                "intervencoes": [{"tipo": t, "descricao": t, "n": 36, "mudou_rotulo": m, "limite_inferior": li, "queda_media_p": 0.2}
                                 for t, m, li in (("remocao", 10, 4), ("troca", 6, 2), ("sem_documentacao", 20, 9), ("repeticao_da_base", 2, 0))],
                "repeticao": {"n": 36, "manteve": 34, "mudou": 2}, "fonte": {"casos": 36, "verificada_pela_remocao": 10, "sem_efeito_medido": 26},
                "sonda": {"casos": 36, "com_alvo": 30, "sem_alvo": 4, "sem_rotulo": 2, "cita_plantado": 12, "mudou_rotulo": 3, "pos_racionalizacao": 9, "taxa_pct": 30.0,
                          "controle_n": 30, "controle_cita": 2, "controle_pct": 6.7},
                "mesmo_prompt": [{"par": "repeticao_da_base", "descricao": "a repetição", "n": 36, "mesmo_prompt": 36, "mesma_resposta": 16, "mesma_fonte": 33, "mesmo_rotulo": 36},
                                 {"par": "verbete_trocado_e_troca", "descricao": "a mutação e a troca", "n": 36, "mesmo_prompt": 36, "mesma_resposta": 12, "mesma_fonte": 30, "mesmo_rotulo": 34}],
                "mutacoes": [mut("verbete_trocado", "recuperacao", 36, 33, 2, 1, 14), mut("contrato_alterado", "poda", 20, 19, 1, 0, 7, sem_alvo=16),
                             mut("seletor_quebrado", "cura", 4, 3, 1, 0, 0)],
                "mutacoes_casos": [{"tipo": "verbete_trocado", "caso": "lex-1", "aplicavel": True, "primeiro_no": "recuperacao", "aponta_o_previsto": True, "rotulo_base": "x", "rotulo_depois": "x"}],
                "seletor": {"roteiros": [{"roteiro": r, "modo_dourado": "id_renomeado", "modo_mutado": "id_renomeado+nome_do_alvo", "estrategia_dourada": "papel_e_nome",
                                          "estrategia_mutada": "caminho_do_ancestral_com_id", "curada_dourada": True, "curada_mutada": True, "rotulo_dourado": "localizador_quebrado",
                                          "rotulo_mutado": "localizador_quebrado", "primeiro_no": "cura", "aponta_o_previsto": True, "mttr_dourada_s": 60.0, "mttr_mutada_s": 70.0}
                                         for r in ("front-busca", "front-admin-login", "front-admin-produtos", "front-cliente-reserva")],
                            "curadas_dourada": 4, "curadas_mutada": 4},
                "amostra_revisao": [{"posicao": i + 1, "caso": f"c{i}", "classe": 1, "relatorio": f"relatorios/c{i}@base.md"} for i in range(12)],
                "casos": [{"caso": "lex-1", "classe": 1, "gabarito": "x", "rotulo": "x", "acerto": True, "p_rotulo": 0.9, "selo": "alto", "falha": None,
                           "sinais": {"divergencia": False, "remocao_ou_troca": False, "sem_documentacao": True, "repeticao_mudou": False, "selo_baixo": False, "falha": False, "qualquer": False},
                           "intervencoes": 4, "limite_inferior": 1, "sonda": "sem efeito", "verbete_trocado": "recuperacao", "contrato_alterado": "poda", "segundos_total": 400.0}]}
        d, h = tp.secao_trilha(sint, self.ctx["road"], gd.cartoes_corridas)
        self.assertIn('id="g-tri-sinais"', h)
        self.assertIn('id="g-tri-mutacoes"', h)
        self.assertIn("tb_f4_trilha_sinais", h)
        self.assertIn("0,50", h, "o produto TPR x TNR do sinal principal")
        self.assertIn("0,25", h, "o acaso")
        self.assertIn("30,0", h, "a taxa de pós-racionalização")
        self.assertIn("33 de 36", h, "as mutações que apontaram o nó previsto")
        self.assertIn("12 relatórios", h)
        # ! Alteração de IA - Revisar: (05/11/2026, leitura da corrida 22) a aba mostra a divergência só por gatilho, o controle da sonda e as
        # inferências de mesmo prompt; a tabela caso a caso só entra depois de a planilha da sessão de revisão estar preenchida.
        # ! Motivo: a sessão é às cegas e o painel é o que o Eric lê; a tabela diz quais relatórios estão certos, e a aba publicada a
        # entregaria antes da sessão. O por_gatilho é o que o agente mostra fora da avaliação; sem o controle, a sonda superestima.
        self.assertIn("por gatilho", h)
        self.assertIn("0,54", h, "o produto do sinal por gatilho")
        self.assertIn("2 de 30", h, "o controle da sonda")
        self.assertIn("tb_f4_trilha_mesmo_prompt", h)
        self.assertNotIn("<code>lex-1</code>", h, "antes da sessão a aba não diz o resultado de nenhum caso")
        self.assertNotIn("Caso a caso", h)
        self.assertIn("depois da sessão de revisão", h)
        _, h_depois = tp.secao_trilha(sint, self.ctx["road"], gd.cartoes_corridas, revisao_preenchida=True)
        self.assertIn("<code>lex-1</code>", h_depois)
        self.assertIn("Caso a caso", h_depois)
        # ! Alteração de IA - Revisar: (05/11/2026, sessão de revisão) a lista dos casos da amostra também só entra depois da sessão, e antes a aba aponta para a página da sessão.
        # ! Motivo: o nome e a classe dizem a família do defeito, e a posição na lista é a mesma da página, que mostra só um nome neutro.
        self.assertNotIn("<code>c0</code>", h)
        self.assertIn("<code>c0</code>", h_depois)
        self.assertIn(tp.URL_SESSAO_REVISAO, h)
        # ! Alteração de IA - Revisar: (05/11/2026, decisão 86) com a leitura da sessão, a aba mostra quem decidiu cada relatório e o parecer do Claude contra o gabarito, sem chamar isso de medida com revisor humano.
        # ! Motivo: o Eric lê pela aba; se ela somasse tudo como revisão humana, a limitação das decisões 85 e 86 sumiria justamente onde ele decide.
        rev = {"resumo": {"relatorios": 5, "respostas_do_revisor": 1, "pareceres_aprovados": 4, "acertos_na_amostra": 3, "erros_na_amostra": 2, "erros_localizados": 1},
               "por_origem": [{"origem": "revisor", "n": 1, "apropriadas": 1, "pct": 100.0, "ic": [20.7, 100.0], "avaliacao_bate": 1}, {"origem": "parecer_aprovado", "n": 4, "apropriadas": 2, "pct": 50.0, "ic": [15.0, 85.0], "avaliacao_bate": 2}],
               "parecer": {"n": 5, "apropriadas": 3, "pct": 60.0, "ic": [23.1, 88.2], "causa_certa": 3, "pct_causa": 60.0, "avaliacao_bate": 3, "errou_a_decisao": ["a-3", "b-2"], "errou_a_causa": ["a-3", "b-2"]},
               "tempo": [{"grupo": "todos", "n": 1, "mediana": 307, "minimo": 307, "maximo": 307}], "duvidas_de_leitura": ["a-1"],
               "casos": [{"posicao": 1, "caso": "a-1", "gabarito": "causa_x", "rotulo": "causa_x", "acerto": True, "origem": "revisor", "segundos": 307, "erro_localizado": "sim", "decisao": "aceitar", "apropriada": True, "utilidade": 4, "avaliacao": "certo",
                          "parecer": {"decisao": "aceitar", "causa": None, "causa_dada": "causa_x", "causa_certa": True, "confianca": "alta"}}]}
        _, h_rev = tp.secao_trilha(sint, self.ctx["road"], gd.cartoes_corridas, revisao_preenchida=True, rev=rev)
        self.assertIn("A sessão de revisão", h_rev)
        self.assertIn("Só 1 dos 5 relatórios", h_rev)
        self.assertIn("não cumpre", h_rev)
        self.assertIn("tb_f4_revisao_parecer", h_rev)
        self.assertIn("pode ter lido", h_rev)
        self.assertIn("O que o parecer do Claude diz", h_rev)
        self.assertIn("3 de 5 decisões", h_rev)
        self.assertIn("limitação declarada (decisão 87)", h_rev)
        self.assertNotIn("ficha 40", h_rev, "a ficha 40 já foi decidida")
        self.assertNotIn("O que o parecer do Claude diz", h_depois)
        self.assertIn("307", h_rev)
        self.assertNotIn("não cumpre", h_depois, "sem a leitura da sessão, a aba não afirma nada sobre ela")
        # ! Alteração de IA - Revisar: (05/11/2026, decisão 88) a aba diz que a regra do carimbo de conflito ficou como está e que o TCC reporta as duas contas.
        # ! Motivo: a frase antiga dizia que a ficha 39 ainda ia decidir; o Eric lê pela aba e veria uma decisão já tomada como pendente.
        self.assertIn("decisão 88", h)
        self.assertNotIn("A ficha 39 decide", h)
        self.assertIn("revisao_trilha", self.ctx)
        self.assertIn("revisao_trilha_preenchida", self.ctx)
        self.assertEqual([s["sinal"] for s in d["sinais"]], [s["sinal"] for s in sint["sinais"]])
        self.assertEqual(d["mutacoes"][0]["previsto"], 33)
        self.assertNotIn("—", h.split('<p class="lead">')[1].split("</p>")[0], "a frase de abertura não leva travessão")
        tri = self.ctx.get("trilha")
        secao = self.html[self.html.index('<section id="trilha"'):].split("</section>")[0]
        if not tri or not (tri.get("resumo") or {}).get("casos"):
            self.assertIn("ainda não foi rodada", secao)
            return
        t = self.dados_t["trilha"]
        self.assertEqual(t["resumo"]["produto"], tri["resumo"]["produto"])
        self.assertIn(f'{tri["resumo"]["acertos"]} de {tri["resumo"]["casos"]}', secao)
        if not self.ctx["revisao_trilha_preenchida"]:
            self.assertNotIn("Caso a caso", secao, "a sessão de revisão é às cegas: a aba publicada não traz o resultado por caso")
            self.assertNotIn("<th>Resultado</th>", secao, "a coluna que diria quais relatórios estão certos fica fora até a sessão")
            self.assertNotIn("<th>Gabarito</th>", secao)

    def teste_funcoes_de_grafico_e_seletores_existem(self):
        for funcs in tp.DESENHAR_TOPICOS.values():
            for f in funcs:
                self.assertIn(f"function {f}(", tp.JS_TOPICOS, f)
        for sel, f in tp.SELETORES_TOPICOS.items():
            self.assertIn(f'id="{sel}"', self.html, sel)
            self.assertIn(f"function {f}(", tp.JS_TOPICOS, f)

    # ! Alteração de IA - Revisar: (05/11/2026, pacote P8) teste da aba "Fechamento da fase": as regras lidas da seção 10 do relatório da Fase 4, com o estado de cada uma, as fichas abertas e os cartões lidos dos JSON das leituras vigentes.
    # ! Motivo: é a aba que o plano chama de aba da fase (seção 3.8), e o Eric decide pelo painel; sem o teste, uma regra não cumprida poderia aparecer como cumprida, ou o cartão poderia ler a corrida que não vale.
    def teste_fechamento_da_fase_4_le_o_relatorio_e_as_leituras_vigentes(self):
        grupo = next(abas for nome, abas in tp.NAV if nome == "Fase 4")
        self.assertEqual(grupo[0][0], "fechamentof4", "a aba do fechamento abre o grupo da fase")
        self.assertEqual(tp._classe_regra("Cumprida"), "cumprida")
        self.assertEqual(tp._classe_regra("Cumprida, com ressalva: os 100% vêm do desenho"), "ressalva")
        self.assertEqual(tp._classe_regra("Não cumprida: limitação declarada, decisão 82"), "nao")
        self.assertEqual(tp._classe_regra("Medida: o plano não fixou limite"), "medida")
        md = ("# Relatório\n\n## 1. Perguntas\n\ntexto da seção um\n\n## 10. As regras\n\n| Regra | O que ela pede | Corrida | Resultado | Estado |\n|---|---|---|---|---|\n"
              "| R1 | pede a | 17 | 37 de 37 | Cumprida |\n| R2 | pede b | 18b | b + c = 9 | Não cumprida: limitação declarada |\n| R3 | pede c | 19 | 160 de 160 | Cumprida, com ressalva: desenho |\n"
              "| R4 | pede d | 20 | 100,0% | Medida: sem limite |\n\n## 11. Entrega\n\ntexto da seção onze\n\n## 12. Limitações\n\ntexto da seção doze\n\n## 13. O que não saiu\n\ntexto da seção treze\n\n## 15. O que o TCC carrega\n\ntexto da seção quinze\n")
        tela = {"resumo": {"concordam": 26, "casos": 37, "discordantes": 9, "limite_r2": 3}}
        cura = {"resumo": {"curadas": 160, "execucoes": 160, "mttr_mediana_s": 0.639}}
        cen = {"geral": {"sucessos": 10, "n": 10, "mttr_media_s": 105.18}}
        rev = {"resumo": {"respostas_do_revisor": 1, "pareceres_aprovados": 10}}
        # ! Alteração de IA - Revisar: (05/11/2026, decisões 90 a 92) a aba recebe o roadmap, mostra as corridas que faltam antes da Fase 5, lidas pelo estado, e a seção 13 do relatório à vista.
        # ! Motivo: com as fichas 42 a 45 fechadas, a aba diria só "nenhuma ficha aberta", como se não restasse nada, e as corridas 18c, 21c, 23 e 24 ainda vão rodar.
        Corrida = type("Corrida", (), {})

        def corrida(numero, classe):
            c = Corrida()
            c.numero, c.classe = numero, classe
            return c
        road_teste = {"corridas": [corrida("13", "aguarda"), corrida("16", "feita"), corrida("18c", "aguarda"), corrida("21c", "pendente"), corrida("22", "feita"), corrida("x", "aguarda")]}
        self.assertEqual(tp._corridas_que_faltam_f4(road_teste), ["18c", "21c"], "só da corrida 16 em diante, e só as que não estão feitas")
        self.assertEqual(tp._corridas_que_faltam_f4(None), [])
        d, h = tp.secao_fechamento_f4(md, self.ctx["pend"], self.ctx["md_doc_para_html"], tela=tela, cura=cura, cenarios=cen, revisao=rev, road=self.ctx["road"], cartoes_corridas=self.ctx["cartoes_corridas"])
        self.assertIn("texto da seção treze", h)
        self.assertEqual(d["contagem"], {"cumprida": 1, "nao": 1, "ressalva": 1, "medida": 1})
        self.assertIn('<section id="fechamentof4" hidden>', h)
        self.assertIn('<span class="chip nao_cumprida">Não cumprida</span><br><span class="nota">limitação declarada</span>', h)
        self.assertIn('<span class="chip concluida">Cumprida</span>', h)
        for texto in ("26 de 37", "160 de 160", "0,639", "10 de 10", "105,2", "1 resposta do Eric", "10 pareceres", "texto da seção um", "texto da seção onze", "texto da seção doze", "texto da seção quinze", "R2"):
            self.assertIn(texto, h, texto)
        abertas = [f for b in self.ctx["pend"] for f in b.fichas if f.aberta]
        self.assertEqual(d["fichas_abertas"], len(abertas))
        for f in abertas:
            self.assertIn(f.id_html, h, f.numero)
        # sem o relatório, o estado vazio
        d0, h0 = tp.secao_fechamento_f4(None, [], self.ctx["md_doc_para_html"])
        self.assertIn('<section id="fechamentof4" hidden>', h0)
        self.assertEqual(d0["contagem"], {})
        # com os arquivos reais, a aba lê as leituras vigentes, não as corridas 18 e 21
        d_real = self.dados_t["fechamentof4"]
        self.assertTrue(d_real["contagem"], "o relatório da fase existe e a tabela da seção 10 foi lida")
        r2 = self.ctx["tela_v2"]["resumo"]
        self.assertIn(f'{r2["concordam"]} de {r2["casos"]}', self.html)
        self.assertNotEqual(self.ctx["tela"]["resumo"]["concordam"], r2["concordam"])
        faltam = tp._corridas_que_faltam_f4(self.ctx["road"])
        if faltam:
            self.assertIn("Corridas que faltam antes da Fase 5", self.html)
            self.assertIn(f'id="corrida-{faltam[0]}-f4"', self.html)

    def teste_slots_cobrem_os_modelos_das_fases(self):
        for m in self.ctx["dados"]["modelos"]:
            self.assertIn(m, tp.SLOTS)
        for x in self.ctx["ablacao"]["por_modelo_condicao"]:
            self.assertIn(x["modelo"], tp.SLOTS)

    def teste_dados_dos_topicos_sao_serializaveis(self):
        json.dumps(self.dados_t, ensure_ascii=False)


if __name__ == "__main__":
    unittest.main(verbosity=1)
