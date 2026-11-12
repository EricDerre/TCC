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
import painel_fases as pf
import painel_grupo as pg
import painel_textos as pt  # noqa: E402
import painel_leituras as pl  # noqa: E402
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
        "readme": (gd.RAIZ / "DETALHES-TECNICOS.md").read_text(encoding="utf-8"),
        "analise3b": gd.ler_json(gd.F3 / "analise_fase3b.json"),
        "relatorio3b": (gd.MEMORIAL / "3-resultados-e-analises" / "fase-3b-relatorio.md").read_text(encoding="utf-8"),
        "pend": pt.ler_pendencias(gd.MEMORIAL / "pendencias.md"),
        **gd.contexto_pre_fase4(),
        **gd.contexto_fase4(),
        **gd.contexto_pos_fase4(),
        **gd.contexto_arvores(),
        **gd.contexto_progresso(),
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
    # ! Alteração de IA - Revisar: (11/11/2026) a navegação lateral passa a ser por fase: o teste confere os grupos pelo atributo `data-grupo`, a ordem das fases,
    # a aba de visão abrindo cada fase e um cabeçalho clicável por fase.
    # ! Motivo: o Eric pediu, em 11/11/2026, abas que detalhem cada fase, com as abas dos tópicos embaixo de cada uma: a lista antiga, em ordem de importância, não
    # dizia de que fase era cada aba, e o título do grupo não se distinguia da aba clicável. A ordem por importância de 06/10/2026 deixa de valer.
    def teste_navegacao_lateral_por_fase(self):
        html = gd.pagina(self.ctx["dados"] | {"topicos": self.dados_t}, gd.blocos_tabelas(gd.F3 / "tabelas_relatorio.md"), {},
                         pt.ler_pendencias(gd.MEMORIAL / "pendencias.md"), self.ctx["road"], self.html)
        lateral = re.search(r'<aside class="lateral" id="lateral">(.*?)</aside>', html, re.S)
        self.assertTrue(lateral, "a navegação fica num <aside class=\"lateral\">")
        self.assertIn('<nav aria-label="Seções">', lateral.group(1))
        self.assertEqual(re.findall(r'data-alvo="([^"]+)"', lateral.group(1)), [sid for _, abas in tp.NAV for sid, _, _ in abas])
        self.assertEqual(re.findall(r'data-grupo="([^"]+)"', lateral.group(1)), [g for g, _ in tp.NAV])
        self.assertEqual([g for g, _ in tp.NAV], [pf.GERAL] + [f["grupo"] for f in pf.FASES] + [pf.APOIO])
        self.assertEqual([abas[0][0] for _, abas in tp.NAV], ["inicio"] + [f["sid"] for f in pf.FASES] + ["pesquisa"])
        self.assertEqual(pf.abas_fora_de_lugar(tp.NAV), [], "fase sem grupo, grupo que não abre pela visão da fase, ou atalho para aba que não existe")
        self.assertEqual(lateral.group(1).count('class="fase-topo"'), len(pf.FASES), "cada fase tem um cabeçalho que abre a visão dela")
        nomes = [nome for _, abas in tp.NAV for _, nome, _ in abas]
        self.assertEqual(len(nomes), len(set(nomes)), "duas abas com o mesmo nome confundem a navegação")
        self.assertIn("if(window.aoMostrar) window.aoMostrar(id);", html, "ao trocar de aba, a fase dela abre na lateral")
        self.assertIn("window.aoMostrar = function(id)", html)
        # ! Alteração de IA - Revisar: (27/10/2026) o grupo "Fase 4" entra depois da Pré-Fase 4, com a aba "Reprodução na tela".
        # ! Motivo: a Fase 4 abriu em 26/10 e a corrida 17 é a primeira análise dela; o grupo fica na ordem cronológica, logo
        # depois da pesquisa que a preparou, sem mexer na ordem por importância que o Eric pediu para os grupos anteriores.
        # ! Alteração de IA - Revisar: (07/11/2026) o grupo "Pós-Fase 4" entra depois do "Fase 4".
        # ! Motivo: a Pós-Fase 4 foi especificada e pesquisada nesta data e ganhou a sua aba; a ordem dos grupos segue a ordem das fases.
        # ! Alteração de IA - Revisar: (11/11/2026) saem as duas conferências que fixavam os oito grupos por importância e a primeira aba de cada um.
        # ! Motivo: a ordem dos grupos e a aba que abre cada um passaram a vir das fases (conferidas no começo deste teste).
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
            # ! Alteração de IA - Revisar: (05/11/2026) o teste confere a frase "N passaram a acertar e M passaram a errar" no lugar de "b = N".
            # ! Motivo: a aba deixou de mostrar b e c soltos no texto à vista; os mesmos dois números continuam conferidos contra o JSON.
            self.assertIn(f'{bibl["reavaliacao"]["b"]} passaram a acertar e {bibl["reavaliacao"]["c"]} passaram a errar', secao)
        self.assertIn(f'{r["aceitas"]} de {r["propostas"]}', secao)
        self.assertIn('id="g-bib-filtros"', secao)
        self.assertIn("tb_f4_biblioteca_filtros", secao)
        self.assertIn("regra R4", secao.lower().replace("r4", "R4").replace("regra r4", "regra R4"))

    def teste_tela_mostra_a_18c_como_leitura_vigente(self):
        # ! Alteração de IA - Revisar: (05/11/2026, decisão 90) a aba da tela lê tela_v3.json: as três corridas, o verbete certo no contexto e o selo, com a 18b e a 18 como o registro de antes.
        # ! Motivo: a decisão 90 diz que a leitura nova passa a valer quando a corrida rodar, e o Eric decide pelo painel.
        tela, v2, v3 = self.ctx.get("tela"), self.ctx.get("tela_v2"), self.ctx.get("tela_v3")
        if not v3:
            return
        d, h = tp.secao_tela(tela, v2, self.ctx["road"], gd.cartoes_corridas, tela_v3=v3)
        r3 = v3["resumo"]
        self.assertEqual(d["v3"]["resumo"]["concordam"], r3["concordam"])
        self.assertEqual(d["v3"]["verbete"], v3["verbete_certo"])
        self.assertEqual(d["v3"]["selo"], v3["acerto_por_selo"])
        self.assertEqual([x["nome"] for x in d["corridas"]], ["18", "18b", "18c"])
        self.assertEqual(d["corridas"][-1]["acerto_tela"], r3["acerto_tela"])
        self.assertEqual([x["acerto_tela_v3"] for x in d["por_classe"]], [x["acerto_tela"] for x in v3["por_classe"]])
        self.assertEqual(sum(x["tela_v3"] for x in d["rotulos"]), r3["casos"])
        for trecho in ('id="g-tela-corridas"', 'id="g-tela-verbete"', "corrida 18c", "tela_v3.json", f'{r3["concordam"]} de {r3["casos"]}', "Rótulo na tela (18c)"):
            self.assertIn(trecho, h)
        # ! Alteração de IA - Revisar: (06/11/2026, decisão 98) a aba diz a regra R2 pelos casos que a tela perde, com os que ela ganha ao lado.
        # ! Motivo: o Eric fixou essa leitura antes da corrida 18d, e o cartão que dizia "só um lado acerta" contaria a tela melhor como defeito.
        self.assertIn(f'a tela perde {r3["c"]} e ganha {r3["b"]}', h)
        self.assertIn("decisão 98", h)
        # ! Alteração de IA - Revisar: (05/11/2026) o caso a caso e as tabelas recolhidas também mostram a leitura vigente, e o gráfico das causas não esconde nomes.
        # ! Motivo: na página publicada, "Caso a caso" ainda listava a corrida 18, e o gráfico das causas pulava metade dos nomes do eixo, com tipo_divergente entre os visíveis por acaso.
        for trecho in (f'Caso a caso, na corrida 18c ({r3["casos"]} casos)', "Acerto na tela (18c)", "Dado na tela (18c)", 'class="chart alto"><canvas id="g-tela-rotulos"', "Prompts da tela acima do limite, na corrida 18 ("):
            self.assertIn(trecho, h)
        primeiro = v3["casos"][0]
        bloco = h[h.index(f'Caso a caso, na corrida 18c ({r3["casos"]} casos)'):]
        self.assertIn(f'<code>{primeiro["rotulo_tela"]}</code>', bloco[:bloco.index("</tr>", bloco.index("<tbody>"))], "a primeira linha do caso a caso é a da 18c")
        self.assertIn("autoSkip:false", tp.JS_TOPICOS[tp.JS_TOPICOS.index("function telaRotulos("):tp.JS_TOPICOS.index("function telaCorridas(")])
        d0, h0 = tp.secao_tela(tela, v2, self.ctx["road"], gd.cartoes_corridas)
        self.assertIsNone(d0["v3"], "sem a 18c, a aba fica como era")
        self.assertNotIn('id="g-tela-verbete"', h0)
        self.assertIn("function telaVerbete(", tp.JS_TOPICOS)
        self.assertIn("function telaCorridas(", tp.JS_TOPICOS)
        secao = self.html[self.html.index('<section id="tela"'):].split("</section>")[0]
        self.assertIn('id="g-tela-verbete"', secao, "a página real traz a 18c")

    def teste_tela_mostra_a_18d_e_os_ineditos_como_leitura_vigente(self):
        # ! Alteração de IA - Revisar: (06/11/2026, decisões 97 e 98) a aba da tela lê tela_v4.json e tela_ineditos.json: a regra pelos casos que a tela perde, nas cinco corridas, e os inéditos como a conferência limpa; a 18c fica recolhida.
        # ! Motivo: a regra fechou na corrida 18d pela leitura fixada antes dela, e a aba é onde o Eric lê isso; a 18c continua à vista como registro, sem disputar os cartões.
        tela, v2, v3, v4, ine = self.ctx.get("tela"), self.ctx.get("tela_v2"), self.ctx.get("tela_v3"), self.ctx.get("tela_v4"), self.ctx.get("tela_ineditos")
        if not v4:
            return
        d, h = tp.secao_tela(tela, v2, self.ctx["road"], gd.cartoes_corridas, tela_v3=v3, tela_v4=v4, tela_ineditos=ine)
        r4, ri = v4["resumo"], ine["resumo"]
        self.assertEqual(d["v4"]["resumo"]["concordam"], r4["concordam"])
        self.assertEqual(d["v4"]["verbete"], v4["verbete_certo"])
        self.assertEqual(d["ineditos"]["verbete"], ine["verbete_certo"])
        self.assertEqual([x["nome"] for x in d["corridas"]], ["18", "18b", "18c", "18d"])
        self.assertEqual([(x["nome"], x["perde"], x["ganha"]) for x in d["regra"]][-2:], [("18d", r4["c"], r4["b"]), ("18e", ri["c"], ri["b"])])
        self.assertEqual(d["limite_r2"], r4["limite_r2"])
        self.assertEqual([x["acerto_tela_v4"] for x in d["por_classe"]], [x["acerto_tela"] for x in v4["por_classe"]])
        self.assertEqual(sum(x["tela_v4"] for x in d["rotulos"]), r4["casos"])
        for trecho in ('id="g-tela-corridas"', 'id="g-tela-verbete"', 'id="g-tela-regra"', "corrida 18d", "corrida 18e", "tela_v4.json", "tela_ineditos.json",
                       f'a tela perde {r4["c"]} e ganha {r4["b"]}', f'a tela perde {ri["c"]} e ganha {ri["b"]}', f'Caso a caso, na corrida 18d ({r4["casos"]} casos)',
                       f'Caso a caso, nos inéditos, corrida 18e ({ri["casos"]} casos)', "Corrida 18c contra a 18d", "A leitura da corrida 18c", "Rótulo na tela (18d)"):
            self.assertIn(trecho, h)
        for canvas in ('id="g-tela-corridas"', 'id="g-tela-verbete"'):
            self.assertEqual(h.count(canvas), 1, "um gráfico só, com a leitura vigente")
        self.assertIn("function telaRegra(", tp.JS_TOPICOS)
        d0, _ = tp.secao_tela(tela, v2, self.ctx["road"], gd.cartoes_corridas, tela_v3=v3)
        self.assertIsNone(d0["v4"], "sem a 18d, a aba fica como era")
        secao = self.html[self.html.index('<section id="tela"'):].split("</section>")[0]
        self.assertIn('id="g-tela-regra"', secao, "a página real traz a 18d")

    def teste_cenarios_mostra_a_21d_como_leitura_vigente(self):
        # ! Alteração de IA - Revisar: (06/11/2026, decisão 97) a aba dos cenários lê cenarios_v4.json e compara a 21d com a 21c.
        # ! Motivo: da 21c para a 21d só mudou a busca, e é essa comparação que diz se os sinais novos mexeram nos dez cenários da Fase 5.
        c, c2, c3, c4 = self.ctx.get("cenarios"), self.ctx.get("cenarios_v2"), self.ctx.get("cenarios_v3"), self.ctx.get("cenarios_v4")
        if not c4:
            return
        d, h = tp.secao_cenarios(c, c2, self.ctx["road"], gd.cartoes_corridas, cen_v3=c3, cen_v4=c4)
        self.assertEqual(d["geral"]["mttr_media_s"], c4["geral"]["mttr_media_s"])
        self.assertEqual(d["por_cenario"][0]["mttr_anterior"], c3["por_cenario"][0]["mttr_media_s"])
        self.assertIn("21c", d["rotulo_anterior"])
        self.assertIn("21d", d["rotulo_vigente"])
        for trecho in ("cenarios_v4.md", "MTTR 21d (s)", "MTTR 21c (s)", "corrida 21d", "Os sinais novos da busca"):
            self.assertIn(trecho, h)
        secao = self.html[self.html.index('<section id="cenarios"'):].split("</section>")[0]
        self.assertIn("cenarios_v4.md", secao, "a página real traz a 21d")

    def teste_cenarios_mostra_a_21c_como_leitura_vigente(self):
        # ! Alteração de IA - Revisar: (05/11/2026, decisão 90) a aba dos cenários lê cenarios_v3.json e compara a 21c com a 21b.
        # ! Motivo: o que a repetição mudou foi o tamanho do prompt, e a comparação que importa agora é contra a corrida de antes do corte, não contra a 21.
        c, c2, c3 = self.ctx.get("cenarios"), self.ctx.get("cenarios_v2"), self.ctx.get("cenarios_v3")
        if not c3:
            return
        d, h = tp.secao_cenarios(c, c2, self.ctx["road"], gd.cartoes_corridas, cen_v3=c3)
        self.assertEqual(d["geral"]["mttr_media_s"], c3["geral"]["mttr_media_s"])
        self.assertEqual(d["por_cenario"][0]["mttr_anterior"], c2["por_cenario"][0]["mttr_media_s"])
        self.assertIn("21b", d["rotulo_anterior"])
        self.assertIn("21c", d["rotulo_vigente"])
        for trecho in ("cenarios_v3.md", "MTTR 21c (s)", "MTTR 21b (s)", "corrida 21c"):
            self.assertIn(trecho, h)
        self.assertIn("C.rotulo_anterior", tp.JS_TOPICOS)
        d0, h0 = tp.secao_cenarios(c, c2, self.ctx["road"], gd.cartoes_corridas)
        self.assertIn("21b", d0["rotulo_vigente"], "sem a 21c, a aba compara a 21b com a 21")
        self.assertIn("MTTR 21 (s)", h0)
        secao = self.html[self.html.index('<section id="cenarios"'):].split("</section>")[0]
        self.assertIn("cenarios_v3.md", secao, "a página real traz a 21c")

    def teste_ineditos_da_corrida_24_usa_os_numeros_do_json(self):
        # ! Alteração de IA - Revisar: (06/11/2026) a aba da corrida 24 lê ineditos.json: o acerto, por classe, com e sem o verbete certo, e a comparação com a corrida 18e.
        # ! Motivo: pela regra do painel, toda análise nova vira uma aba lida dos JSON, e o número vai para o TCC.
        ined = self.ctx.get("ineditos_f4")
        self.assertTrue(ined, "a leitura da corrida 24 existe")
        d, h = tp.secao_ineditos_f4(ined, self.ctx["road"], gd.cartoes_corridas, self.ctx.get("analise3b"))
        r = ined["resumo"]
        self.assertEqual(d["resumo"]["acertos"], r["acertos"])
        self.assertEqual([x["acertos"] for x in d["por_classe"]], [x["acertos"] for x in ined["por_classe"]])
        self.assertEqual(d["verbete"], ined["verbete_certo"])
        for trecho in ('id="g-ined-classe"', 'id="g-ined-verbete"', f'{r["acertos"]} de {r["casos"]}', "ineditos.json", "corrida 24", f'{ined["lado_escrito_18e"]["mesmo_rotulo"]} de {ined["lado_escrito_18e"]["casos"]}'):
            self.assertIn(trecho, h)
        _, vazia = tp.secao_ineditos_f4(None, self.ctx["road"], gd.cartoes_corridas)
        self.assertIn("ainda não foi rodada", vazia)
        self.assertIn("function inedClasse(", tp.JS_TOPICOS)
        self.assertIn("function inedVerbete(", tp.JS_TOPICOS)
        self.assertIn('<section id="ineditosf4"', self.html)
        self.assertIn("ineditosf4", [i for _, itens in tp.NAV for i, *_ in itens])

    def teste_pos_fase4_le_o_levantamento_o_plano_e_as_fichas(self):
        # ! Alteração de IA - Revisar: (07/11/2026) a aba da Pós-Fase 4 lê o levantamento §6.15 (a tabela do cabeçalho e o mapa), o plano em rascunho (os pacotes) e as fichas 49 a 54; sem o levantamento, o estado vazio.
        # ! Motivo: a regra do painel é uma aba por análise, e o Eric decide pelo painel: as fichas 53 e 54 estão abertas e a aba precisa mostrá-las com os vereditos que as sustentam.
        self.assertIn("posfase4", [sid for _, abas in tp.NAV for sid, _, _ in abas])
        self.assertIn("function posFontes(", tp.JS_TOPICOS)
        self.assertIn("posFontes", tp.DESENHAR_TOPICOS["posfase4"])
        _, vazia = tp.secao_pos_fase4(None, None, [])
        self.assertIn('<section id="posfase4"', vazia)
        self.assertIn("integrar_pesquisa_pos_fase4.py", vazia)
        lev = ("### 6.15 Levantamento da Pós-Fase 4\n\n| Subseção | Parte | Leitura | Fontes com endereço |\n|---|---|---|---|\n| §6.15.1 | 1 | `pos4-revisao-estilo-pr` | 9 |\n| §6.15.2 | 3 | `pos4-repo-gepa` | 2 |\n\n"
               "#### 6.15.1 O hub (`pos4-revisao-estilo-pr`; 9 fontes com endereço)\n\ntexto\n\n#### 6.15.2 Repositório gepa-ai/gepa (`pos4-repo-gepa`; 2 fontes com endereço)\n\ntexto\n\n"
               "| Dimensão do syllabus | O projeto | Seção e página |\n|---|---|---|\n| Nível de teste | sistema | 2.2.1, p. 26 |\n\n"
               "#### 6.15.3 Mapa adotado, ideia, adiado, descartado\n\nintro\n\n| Leitura | Para o Claude Code | Para o agente | O que fica | Veredito |\n|---|---|---|---|---|\n"
               "| O hub (`pos4-revisao-estilo-pr`) | n/a | base do hub | o desenho | **adotado** |\n| Repositório gepa-ai/gepa (`pos4-repo-gepa`) | opcional | não é filtro | candidato futuro | **adiado** |\n")
        plano = "## 7. Ordem\n\n### Q0. Registro e pesquisa (sessão de 07/11/2026; feito)\nTexto.\n\n### Q1. Relatório v3 (sessões 2 e 3; sem máquina)\nTexto.\n"
        d, h = tp.secao_pos_fase4(lev, plano, self.ctx["pend"])
        self.assertEqual([x["fontes"] for x in d["leituras"]], [9, 2])
        self.assertEqual([x["rotulo"] for x in d["leituras"]], ["Hub estilo PR", "gepa"])
        self.assertEqual([x["veredito"] for x in d["mapa"]], ["adotado", "adiado"])
        self.assertEqual(d["vereditos"], {"adiado": 1})
        for trecho in ("g-pos4-fontes", "base do hub", "candidato futuro", "Q1", "Relatório v3", "ficha 53", "ficha 54", "decisão 101", "2.2.1, p. 26"):
            self.assertIn(trecho, h)
        real = self.ctx.get("levantamento_pos4")
        if real:
            secao = self.html[self.html.index('<section id="posfase4"'):].split("</section>")[0]
            import integrar_pesquisa_pos_fase4 as ipp
            dados_reais = self.dados_t["posfase4"]
            self.assertEqual([x["chave"] for x in dados_reais["leituras"]], [t[0] for t in ipp.TOPICOS], "uma linha do cabeçalho por leitura, na ordem fixa")
            self.assertEqual([m["chave"] for m in dados_reais["mapa"]], [m[0] for m in ipp.MAPA], "uma linha do mapa por leitura")
            self.assertEqual(sum(x["fontes"] for x in dados_reais["leituras"]), sum(len(v["fontes"]) for v in ipp.carregar().values()), "as fontes contadas batem com o integrador")
            self.assertIn("ficha 54", secao)

    def teste_texto_usa_os_numeros_do_json(self):
        # ! Alteração de IA - Revisar: (07/11/2026, Pós-Fase 4, pacote Q2) a aba "O que chega ao analista" lê texto.json: quantos relatórios e leituras passam nos
        # filtros antes e depois, a parcela por critério, os termos sem o significado e os limiares com a fonte; sem o JSON, o estado vazio.
        # ! Motivo: a regra do painel é uma aba por análise, lida do JSON versionado, e o Eric decide por ela: os números da aba têm de ser os de texto.json.
        self.assertIn("texto", [sid for _, abas in tp.NAV for sid, _, _ in abas])
        for f in ("txtCriterios", "txtTermos"):
            self.assertIn(f"function {f}(", tp.JS_TOPICOS)
            self.assertIn(f, tp.DESENHAR_TOPICOS["texto"])
        self.assertIn(("texto", "Métrica"), pl.TABELAS_A_VISTA)
        self.assertIn("texto", pl.RESPOSTA_SIMPLES)
        for g in ("g-texto-criterios", "g-texto-termos"):
            self.assertIn(g, pl.COMO_LER_GRAFICO)
        _, vazia = tp.secao_texto(None)
        self.assertIn('<section id="texto"', vazia)
        self.assertIn("avaliar_fase4.py --texto", vazia)
        real = self.ctx.get("texto")
        self.assertTrue(real, "texto.json existe em resultados_alvo/fase4")
        d, h = tp.secao_texto(real)
        rel, ver = real["resumo"]["relatorios"], real["resumo"]["verbetes"]
        for trecho in (f'{rel["depois"]["aprovados"]} de {rel["depois"]["n"]}', f'{rel["antes"]["aprovados"]} de {rel["antes"]["n"]}',
                       f'{ver["depois"]["aprovados"]} de {ver["depois"]["n"]}', "g-texto-criterios", "g-texto-termos", "percentil 95"):
            self.assertIn(trecho, h)
        chaves = [m["chave"] for m in real["metricas"] if m["regra"] in ("ate", "zero")]
        self.assertEqual(d["criterios"]["chaves"], chaves)
        self.assertEqual([s["nome"] for s in d["criterios"]["series"]], ["relatórios v2", "relatórios v3", "verbetes", "camada de leitura"])
        self.assertEqual(d["criterios"]["series"][1]["pct"], [rel["depois"]["criterios"][ch]["passam_pct"] for ch in chaves])
        self.assertEqual(d["criterios"]["series"][2]["pct"], [ver["antes"]["criterios"][ch]["passam_pct"] for ch in chaves])
        self.assertEqual(sum(d["termos"]["antes"]), sum(rel["antes"]["termos_sem_expansao"].values()) + sum(ver["antes"]["termos_sem_expansao"].values()))
        self.assertEqual(sum(d["termos"]["depois"]), sum(rel["depois"]["termos_sem_expansao"].values()) + sum(ver["depois"]["termos_sem_expansao"].values()))
        for m in real["metricas"]:
            self.assertIn(m["nome"], h, "toda métrica aparece com o nome, o limiar e a fonte")
        lim = real["limiares"]["valores"]["repeticao_razao"]["valor"]
        self.assertIn(f"{lim:.4f}".replace(".", ","), h)
        self.assertNotIn("—", h)
        self.assertNotIn("→", h)
        # ! Alteração de IA - Revisar: (10/11/2026) a aba mostra a curadoria das leituras: quantas estão curadas, quantas o analista aprovou e quantas reescreveu, e os
        # consertos do Claude, lidos de curadoria_leituras/respostas.json e consertos.json.
        # ! Motivo: a regra do painel pede que toda curadoria apareça numa aba lida dos arquivos; a aba ainda dizia que o que reprovava ficava "para a curadoria do Eric",
        # depois de as 39 leituras terem sido curadas por um analista e consertadas (decisão 115).
        cur = self.ctx.get("curadoria_leituras")
        self.assertTrue(cur and cur.get("respostas") and cur.get("consertos"), "respostas.json e consertos.json da curadoria existem em resultados_alvo/fase4/curadoria_leituras")
        d, h = tp.secao_texto(real, cur)
        cam = next(g for g in real["grupos"] if g["id"] == "camada_de_leitura")
        curadas = sum(1 for p in cam["pares"] if p["curado"])
        reescritas = sum(1 for x in cur["respostas"] if x["estado"] == "editada")
        aprovadas = sum(1 for x in cur["respostas"] if x["estado"] == "aprovada")
        n_cons = sum(len(v) for v in cur["consertos"].values())
        for trecho in (f"{curadas} de {ver['depois']['n']}", f"{reescritas} reescritas", f"{aprovadas} aprovadas como estavam", f"{n_cons} consertos", "um analista", "decisão 115",
                       "A curadoria, leitura a leitura"):
            self.assertIn(trecho, h, trecho)
        self.assertEqual(d["curadoria"], {"curadas": curadas, "aprovadas": aprovadas, "reescritas": reescritas, "consertos": n_cons, "leituras_consertadas": len(cur["consertos"])})
        self.assertNotIn("que a curadoria do Eric reescreve", h)
        self.assertIn("analista", pl.RESPOSTA_SIMPLES["texto"])
        self.assertNotIn("—", h)
        self.assertNotIn("→", h)
        secao = self.html[self.html.index('<section id="texto"'):].split("</section>")[0]
        self.assertIn(f'{rel["depois"]["aprovados"]} de {rel["depois"]["n"]}', secao, "a página real traz a leitura")
        self.assertEqual(json.dumps(self.dados_t["texto"], ensure_ascii=False)[:1], "{")

    def teste_arvore_usa_os_numeros_dos_json(self):
        # ! Alteração de IA - Revisar: (08/11/2026, Pós-Fase 4, pacote Q3) a aba "Árvore de decisão" lê os arvores/INDICE.json das três corridas vigentes e o JSON de cada
        # trilha: as árvores, os nós que viraram decisões, as afirmações por rótulo, os casos com divergência e com cura, os filtros do Q2 e o explorador com um caso por
        # árvore; sem as pastas, o estado vazio.
        # ! Motivo: a regra do painel é uma aba por análise, lida do JSON versionado, e o Eric decide por ela: os números da aba têm de ser os dos índices gravados.
        self.assertIn("arvore", [sid for _, abas in tp.NAV for sid, _, _ in abas])
        for f in ("arvRotulos", "arvConfianca", "arvExplorar"):
            self.assertIn(f"function {f}(", tp.JS_TOPICOS)
            self.assertIn(f, tp.DESENHAR_TOPICOS["arvore"])
        self.assertIn("arvore", pl.RESPOSTA_SIMPLES)
        for g in ("g-arvore-rotulos", "g-arvore-confianca"):
            self.assertIn(g, pl.COMO_LER_GRAFICO)
        _, vazia = tp.secao_arvore(None)
        self.assertIn('<section id="arvore"', vazia)
        self.assertIn("arvore_de_decisao.py --saida", vazia)
        real = self.ctx.get("arvores")
        self.assertTrue(real, "arvores/INDICE.json existe nas três corridas vigentes")
        self.assertEqual([c["corrida"] for c in real], ["fase4_tela_v4", "fase4_ensaio_v4", "fase4_ineditos"])
        d, h = tp.secao_arvore(real)
        resumos = [c["indice"]["resumo"] for c in real]
        total = sum(r["trilhas"] for r in resumos)
        com_div, com_cura = sum(r["com_divergencia"] for r in resumos), sum(r["com_cura"] for r in resumos)
        observado = sum(r["rotulos"]["observado"] for r in resumos)
        afirmacoes = sum(r["afirmacoes"] for r in resumos)
        for trecho in (f"{total} árvores", f"{com_div} de {total}", f"{com_cura} de {total}", f"{observado} de {afirmacoes}", "g-arvore-rotulos", "g-arvore-confianca", "arv-explorador"):
            self.assertIn(trecho, h)
        self.assertEqual(d["resumo"]["arvores"], total)
        self.assertEqual(d["resumo"]["rotulos"]["observado"], observado)
        self.assertEqual(d["resumo"]["filtros"], {"n": sum(r["filtros"]["n"] for r in resumos), "aprovados": sum(r["filtros"]["aprovados"] for r in resumos)})
        self.assertEqual([s["nome"] for s in d["rotulos"]["series"]], ["observado", "conferido", "declarado", "desconhecido"])
        self.assertEqual(d["rotulos"]["series"][0]["n"], [r["rotulos"]["observado"] for r in resumos])
        self.assertEqual(sum(d["confianca"]["series"][0]["n"]), sum(r["por_confianca"].get("alta", 0) for r in resumos))
        casos = [x for c in d["explorador"]["corridas"] for x in c["casos"]]
        self.assertEqual(len(casos), total, "o explorador leva uma árvore por trilha")
        for x in casos:
            self.assertTrue(x["decisoes"] and all(a[1] in ("observado", "conferido", "declarado", "desconhecido") for dd in x["decisoes"] for a in dd["afirmacoes"]), x["nome"])
            self.assertEqual([dd["chave"] for dd in x["decisoes"]][:3], ["leitura", "verbetes", "causa"])
        com_cura_expl = [x for x in casos if x["resumo"]["cura"]]
        self.assertEqual(len(com_cura_expl), com_cura)
        self.assertTrue(all(x["decisoes"][-1]["chave"] == "cura" for x in com_cura_expl))
        padrao = d["explorador"]["padrao"]
        self.assertIn(padrao["caso"], [x["nome"] for x in d["explorador"]["corridas"][padrao["corrida"]]["casos"]])
        self.assertNotIn("—", h)
        self.assertNotIn("→", h)
        secao = self.html[self.html.index('<section id="arvore"'):].split("</section>")[0]
        self.assertIn(f"{com_div} de {total}", secao, "a página real traz a leitura")
        self.assertEqual(json.dumps(self.dados_t["arvore"], ensure_ascii=False)[:1], "{")

    def teste_progresso_e_git_usam_os_numeros_dos_json(self):
        # ! Alteração de IA - Revisar: (08/11/2026, Pós-Fase 4, pacote Q4) a aba "Barra e Git" lê taxas_progresso.json, erro_progresso.json e impacto_git.json (e
        # fumaca_progresso.json quando a fumaça real tiver rodado): as taxas do modelo nesta máquina, o erro da estimativa por fase e a prova da seleção pelo diff
        # do Git no histórico do repositório; sem os arquivos, o estado vazio.
        # ! Motivo: a regra do painel é uma aba por análise, lida do JSON versionado, e o Eric decide por ela: os números da aba têm de ser os dos arquivos gravados.
        self.assertIn("progresso", [sid for _, abas in tp.NAV for sid, _, _ in abas])
        for f in ("progErro", "progGit"):
            self.assertIn(f"function {f}(", tp.JS_TOPICOS)
            self.assertIn(f, tp.DESENHAR_TOPICOS["progresso"])
        self.assertIn("progresso", pl.RESPOSTA_SIMPLES)
        for g in ("g-prog-erro", "g-git-pares"):
            self.assertIn(g, pl.COMO_LER_GRAFICO)
        _, vazia = tp.secao_progresso(None, None, None)
        self.assertIn('<section id="progresso"', vazia)
        self.assertIn("progresso.py --taxas", vazia)
        taxas, erro, impacto = self.ctx.get("taxas_progresso"), self.ctx.get("erro_progresso"), self.ctx.get("impacto_git")
        self.assertTrue(taxas and erro and impacto, "os três JSON do Q4 existem em resultados_alvo/fase4")
        d, h = tp.secao_progresso(taxas, erro, impacto, self.ctx.get("fumaca_progresso"))
        m = taxas["por_modelo"]["qwen2.5:7b"]
        r = erro["por_modelo"]["qwen2.5:7b"]["fora_da_corrida"]
        for trecho in (f"{m['prefill_tokens_por_s']['mediana']:.1f}".replace(".", ","), f"{m['geracao_tokens_por_s']['mediana']:.2f}".replace(".", ","),
                       f"{r['total_s']['erro_abs_mediana_s']:.1f}".replace(".", ","), f"{impacto['resumo']['selecao_parcial']} de {impacto['resumo']['pares']}",
                       "g-prog-erro", "g-git-pares", "fumaça"):
            self.assertIn(trecho, h, trecho)
        self.assertEqual(d["erro"]["fases"], ["prefill", "geração", "prefill mais geração"])
        self.assertEqual(d["erro"]["series"][0]["n"][2], r["total_s"]["erro_abs_mediana_s"])
        self.assertEqual(len(d["git"]["pares"]), impacto["resumo"]["pares"])
        self.assertEqual(d["git"]["selecionados"], [len(p["selecao"]["cenarios"]) for p in impacto["pares"]])
        self.assertEqual(d["git"]["total"], impacto["mapa"]["cenarios"])
        self.assertEqual(d["resumo"]["registros"], m["n"])
        self.assertNotIn("—", h)
        self.assertNotIn("→", h)
        secao = self.html[self.html.index('<section id="progresso"'):].split("</section>")[0]
        self.assertIn(f"{impacto['resumo']['selecao_parcial']} de {impacto['resumo']['pares']}", secao, "a página real traz a leitura")
        self.assertEqual(json.dumps(self.dados_t["progresso"], ensure_ascii=False)[:1], "{")

    def teste_revisao_v3_usa_os_numeros_do_json(self):
        # ! Alteração de IA - Revisar: (10/11/2026, Pós-Fase 4, pacote Q5) a aba "Revisão humana" lê leitura_revisao_v3.json (a sessão com revisor humano dos
        # relatórios v3 e das árvores da corrida 24, ficha 40 opção b): a adesão apropriada por grupo, o erro localizado, o tempo até a decisão, a utilidade e a
        # tabela caso a caso com o comentário do revisor; sem o arquivo, o estado vazio.
        # ! Motivo: a regra do painel é uma aba por análise, lida do JSON versionado, e o Eric decide por ela: os números da aba têm de ser os do arquivo gravado.
        self.assertIn("revisaov3", [sid for _, abas in tp.NAV for sid, _, _ in abas])
        for f in ("revV3Adesao", "revV3Utilidade"):
            self.assertIn(f"function {f}(", tp.JS_TOPICOS)
            self.assertIn(f, tp.DESENHAR_TOPICOS["revisaov3"])
        self.assertIn("revisaov3", pl.RESPOSTA_SIMPLES)
        for g in ("g-revv3-adesao", "g-revv3-utilidade"):
            self.assertIn(g, pl.COMO_LER_GRAFICO)
        _, vazia = tp.secao_revisao_v3(None)
        self.assertIn('<section id="revisaov3"', vazia)
        self.assertIn("avaliar_fase4.py --revisao_v3", vazia)
        rev = self.ctx.get("revisao_v3")
        self.assertTrue(rev, "leitura_revisao_v3.json existe em resultados_alvo/fase4")
        d, h = tp.secao_revisao_v3(rev, self.ctx.get("revisao_trilha"))
        r = rev["resumo"]
        certos, errados = rev["adesao"][0], rev["adesao"][1]
        for trecho in (f"{r['adesao_apropriada']} de {r['relatorios']}", f"{r['adesao_pct']:.1f}".replace(".", ","), f"{r['erros_localizados']} de {r['erros_na_amostra']}",
                       f"{certos['aceitou']} de {certos['n']}", f"{errados['recusou']} de {errados['n']}", "g-revv3-adesao", "g-revv3-utilidade", "ficha 40", "relatorio-",
                       rev["casos"][0]["comentario"][:40]):
            self.assertIn(trecho, h, trecho)
        self.assertEqual(d["adesao"]["grupos"], [certos["grupo"], errados["grupo"]])
        self.assertEqual(d["adesao"]["series"][0]["n"], [certos["apropriadas"], errados["apropriadas"]])
        self.assertEqual(d["adesao"]["series"][1]["n"], [certos["n"] - certos["apropriadas"], errados["n"] - errados["apropriadas"]])
        self.assertEqual(sum(d["utilidade"]["series"][0]["n"]) + sum(d["utilidade"]["series"][1]["n"]), r["relatorios"])
        self.assertEqual(d["resumo"]["adesao_pct"], r["adesao_pct"])
        self.assertEqual(h.count("<code>relatorio-"), len([c for c in rev["casos"] if c["apropriada"] is False]))
        # ! Alteração de IA - Revisar: (10/11/2026) a aba diz quem respondeu cada relatório e só dá o tempo onde ele foi medido.
        # ! Motivo: a versão de 10/11/2026 dizia que o Eric tinha lido os 36 relatórios em 31 s de mediana; quase todas as respostas vieram de um analista, coladas
        # pelo Eric, e o tempo que a página mediu nelas era o da troca entre os dois.
        origem = {x["origem"]: x["n"] for x in rev["por_origem"]}
        tempo_n = next(x for x in rev["tempo"] if x["grupo"] == "todos")["n"]
        self.assertGreater(origem.get("analista", 0), 0, "a leitura gravada separa as respostas do analista")
        for trecho in (f"{origem['analista']} de {r['relatorios']}", "um analista", "troca entre os dois", "digitada ou colada pelo Eric",
                       f"{rev['pagina']['intervalo_entre_relatorios_mediana_s']} s", "decisão 114", "Quem respondeu"):
            self.assertIn(trecho, h, trecho)
        # o tempo: sem nenhuma resposta dada na página por quem leu, a aba diz que ele não foi medido e não mostra número nenhum de segundos como tempo de leitura
        if tempo_n:
            self.assertIn(f"medido em {tempo_n} de {r['relatorios']}", h)
        else:
            self.assertIn(f"não foi medido em nenhum dos {r['relatorios']}", h)
            self.assertNotIn("n/d s", h)
        if rev.get("quem_leu"):
            self.assertIn(rev["quem_leu"]["quem"], h)
            self.assertIn(rev["quem_leu"]["relacao_com_o_projeto"], h)
        for trecho in ("O revisor (o autor do trabalho) leu os", "Decidir é rápido"):
            self.assertNotIn(trecho, h, trecho)
        self.assertEqual(d["resumo"]["respostas_do_analista"], origem["analista"])
        self.assertEqual(d["resumo"]["tempo_medido_em"], tempo_n)
        self.assertIn("analista", pl.RESPOSTA_SIMPLES["revisaov3"])
        self.assertNotIn("meio minuto", pl.RESPOSTA_SIMPLES["revisaov3"])
        self.assertNotIn("—", h)
        self.assertNotIn("→", h)
        secao = self.html[self.html.index('<section id="revisaov3"'):].split("</section>")[0]
        self.assertIn(f"{r['adesao_apropriada']} de {r['relatorios']}", secao, "a página real traz a leitura")
        self.assertEqual(json.dumps(self.dados_t["revisaov3"], ensure_ascii=False)[:1], "{")

    def teste_sem_notas_usa_os_numeros_do_json(self):
        # ! Alteração de IA - Revisar: (10/11/2026, ficha 63 opção b, decisão 116) a aba "Notas do modelo" lê sem_notas_previa.json (a prévia sem modelo da corrida 25:
        # o que muda no contexto dos 72 casos quando a biblioteca perde as notas do modelo e os verbetes aprendidos) e, quando a corrida tiver rodado, sem_notas.json
        # (os pares contra as corridas 22 e 24 e o veredito pela regra fixada antes); sem os arquivos, o estado vazio.
        # ! Motivo: a regra do painel é uma aba por análise, lida do JSON versionado, e o Eric decide por ela. A corrida ainda não rodou: a aba tem de dizer isso, mostrar
        # o que já se sabe sem o modelo e, depois da corrida, mostrar o resultado sem ninguém mexer no código.
        self.assertIn("semnotas", [sid for _, abas in tp.NAV for sid, _, _ in abas])
        for f in ("semNotasContexto", "semNotasPares"):
            self.assertIn(f"function {f}(", tp.JS_TOPICOS)
            self.assertIn(f, tp.DESENHAR_TOPICOS["semnotas"])
        self.assertIn("semnotas", pl.RESPOSTA_SIMPLES)
        for g in ("g-semnotas-contexto", "g-semnotas-pares"):
            self.assertIn(g, pl.COMO_LER_GRAFICO)
        _, vazia = tp.secao_sem_notas(None, None)
        self.assertIn('<section id="semnotas"', vazia)
        self.assertIn("experimento_sem_notas.py --previa", vazia)
        previa = self.ctx.get("sem_notas_previa")
        self.assertTrue(previa, "sem_notas_previa.json existe em resultados_alvo/fase4")
        r, b = previa["resumo"], previa["biblioteca"]
        d, h = tp.secao_sem_notas(previa, None)
        for trecho in (f"{b['notas_retiradas']} notas", f"{b['notas_em_forma_de_instrucao']} de {b['notas_retiradas']}", f"{r['contextos_que_mudam']} de {r['casos']}",
                       f"{r['com_aprendido_na_referencia']} de {r['casos']}", "decisão 116", "ficha 63", "rodar_experimento_sem_notas.ps1", "corrida 22", "corrida 24", "corrida 16",
                       previa["casos_com_verbetes_diferentes"][0]["caso"], "g-semnotas-contexto", "ainda não rodou", "0,05"):
            self.assertIn(trecho, h, trecho)
        # antes da corrida o gráfico dos pares já existe, só com os acertos das corridas de referência (todo gráfico da página tem a sua leitura, e toda leitura o seu gráfico)
        self.assertIn("g-semnotas-pares", h)
        self.assertEqual([s["n"] for s in d["pares"]["series"]], [[x["acertos_referencia"] for x in previa["por_banco"]]])
        self.assertEqual(d["previa"]["casos"], r["casos"])
        self.assertEqual([sum(s["n"][i] for s in d["previa"]["series"]) for i in range(len(d["previa"]["grupos"]))], [x["casos"] for x in previa["por_banco"]])
        # com a leitura da corrida, a aba mostra o veredito, os pares e o segundo gráfico, e deixa de dizer que não rodou
        par = {"casos": 36, "acertos_sem_notas": 28, "acerto_sem_notas_pct": 77.8, "wilson_lo_pct": 61.9, "wilson_hi_pct": 88.3, "acertos_referencia": 31, "acerto_referencia_pct": 86.1,
               "b": 1, "c": 4, "saldo": -3, "p": 0.375, "mesmo_rotulo": 30, "ganhos": ["lex-1"], "perdas": ["lex-2", "lex-3", "sin-5", "efe-5"]}
        leitura = {"metadados": {"corrida": "fase4_sem_notas", "gerado_em": "2026-11-11T10:00:00"}, "condicoes": {"versao_ollama": "0.40.15"},
                   "regra": {"alfa": 0.05, "texto": previa["regra"], "pareavel": True, "mesma_versao_das_referencias": False,
                             "ponte": {"corrida": "fase3b_ponte_04015", "versao": "0.40.15", "b": 1, "c": 0, "n": 35, "limite": 2, "pareavel": True}},
                   "resumo": {**par, "casos": 72, "acertos_sem_notas": 53, "acerto_sem_notas_pct": 73.6, "acertos_referencia": 56, "acerto_referencia_pct": 77.8, "b": 2, "c": 5, "saldo": -3, "p": 0.4531,
                              "mesmo_rotulo": 61, "completo": True, "sai_do_ruido": False, "veredito": "dentro do ruído", "tokens_entrada_mediana": 1010, "tokens_entrada_mediana_referencia": 1150,
                              "segundos_mediana": 58.2, "segundos_mediana_referencia": 66.4},
                   "por_banco": [{**par, "banco": "avaliacao", "referencia": "corrida 22"}, {**par, "banco": "ineditos", "referencia": "corrida 24", "acertos_sem_notas": 25, "acertos_referencia": 25,
                                                                                            "b": 1, "c": 1, "p": 1.0, "ganhos": ["run-22"], "perdas": ["lex-27"]}],
                   "por_mudanca_do_contexto": [{"mudanca": m, "casos": n, "acertos_sem_notas": n - 5, "acertos_referencia": n - 4, "b": 1, "c": 2, "mesmo_rotulo": n - 3}
                                               for m, n in (("contexto idêntico", 0), ("mesmos verbetes, sem as notas", 59), ("mesmos verbetes, outra ordem", 4), ("verbetes diferentes", 9))],
                   "contra_a_corrida_16": {"corrida": "16", **par, "biblioteca": "1fca10f1a6f6", "versao_ollama": "0.40.2"}, "por_classe": [],
                   "casos": [{"caso": "lex-2", "banco": "avaliacao", "gabarito": "campo_ausente", "rotulo": "tipo_divergente", "rotulo_referencia": "campo_ausente", "mudou": "perda",
                              "mudanca_do_contexto": "mesmos verbetes, sem as notas", "verbetes_ids": ["a", "b", "c"], "verbetes_ids_referencia": ["a", "b", "c"]},
                             {"caso": "lex-9", "banco": "avaliacao", "gabarito": "campo_ausente", "rotulo": "campo_ausente", "rotulo_referencia": "campo_ausente", "mudou": "",
                              "mudanca_do_contexto": "mesmos verbetes, sem as notas", "verbetes_ids": ["a", "b", "c"], "verbetes_ids_referencia": ["a", "b", "c"]}]}
        d2, h2 = tp.secao_sem_notas(previa, leitura)
        for trecho in ("dentro do ruído", "53 de 72", "56 de 72", "0,453", "fase3b_ponte_04015", "g-semnotas-pares", "<code>lex-2</code>", "1fca10f1a6f6"):
            self.assertIn(trecho, h2, trecho)
        self.assertNotIn("ainda não rodou", h2)
        self.assertNotIn("<code>lex-9</code>", h2, "a tabela caso a caso traz só os que mudaram de acerto")
        self.assertEqual([s["n"] for s in d2["pares"]["series"]], [[28, 25], [31, 25]])

    def teste_segundo_passe_usa_os_numeros_do_json(self):
        # ! Alteração de IA - Revisar: (10/11/2026, ficha 66 opção b, decisão 120) a aba "Segundo passe" lê segundo_passe_previa.json (a prévia sem modelo da corrida 26: os
        # casos com sinal, o que o segundo pedido alcança, o tamanho do prompt e os desenhos descartados) e, quando a corrida tiver rodado, segundo_passe.json (o que a
        # segunda resposta consertaria e estragaria, o que a regra de escolha trocou e o veredito pela regra fixada antes); sem os arquivos, o estado vazio.
        # ! Motivo: a regra do painel é uma aba por análise, lida do JSON versionado, e o Eric decide por ela. A corrida ainda não rodou: a aba tem de dizer isso, mostrar o
        # que a conta sem modelo já diz (o resultado não tem como sair do ruído) e, depois da corrida, mostrar o resultado sem ninguém mexer no código. Os dois gráficos
        # existem antes e depois da corrida, porque todo gráfico da página precisa da sua leitura e toda leitura do seu gráfico.
        self.assertIn("segpasse", [sid for _, abas in tp.NAV for sid, _, _ in abas])
        for f in ("segPasseAlcance", "segPasseResultado"):
            self.assertIn(f"function {f}(", tp.JS_TOPICOS)
            self.assertIn(f, tp.DESENHAR_TOPICOS["segpasse"])
        self.assertIn("segpasse", pl.RESPOSTA_SIMPLES)
        for g in ("g-segpasse-alcance", "g-segpasse-resultado"):
            self.assertIn(g, pl.COMO_LER_GRAFICO)
        _, vazia = tp.secao_segundo_passe(None, None)
        self.assertIn('<section id="segpasse"', vazia)
        self.assertIn("experimento_segundo_passe.py --previa", vazia)
        previa = self.ctx.get("segundo_passe_previa")
        self.assertTrue(previa, "segundo_passe_previa.json existe em resultados_alvo/fase4")
        r, des = previa["resumo"], previa["desenho"]
        d, h = tp.secao_segundo_passe(previa, None)
        for trecho in (f"{r['com_sinal']} de {r['casos']}", f"{r['erros_com_sinal']} dos {r['erros']}", f"{r['erros_ao_alcance']} dos {r['erros_com_sinal']}", "decisão 120", "ficha 66",
                       "rodar_fila_pre_fase5.ps1", "corrida 22", "corrida 24", str(des["limite_de_tokens"]), "ainda não rodou", "0,05", "g-segpasse-alcance", "g-segpasse-resultado",
                       previa["casos"][0]["caso"], "posições 4 a 6", "descartado", "escolhido"):
            self.assertIn(trecho, h, trecho)
        # antes da corrida o gráfico do resultado traz só os erros e os acertos da primeira resposta, por sinal
        self.assertEqual([s["n"] for s in d["resultado"]["series"]], [[x["erros"] for x in previa["por_sinal"]], [x["acertos"] for x in previa["por_sinal"]]])
        self.assertEqual(d["alcance"]["grupos"], [x["sinal"] for x in previa["por_sinal"]])
        self.assertEqual([sum(s["n"][i] for s in d["alcance"]["series"]) for i in range(len(d["alcance"]["grupos"]))], [x["casos"] for x in previa["por_sinal"]])
        # com a leitura da corrida, a aba mostra o veredito, o que a segunda resposta faria sozinha e o que a regra trocou, e deixa de dizer que não rodou
        grupo = {"casos": 8, "erros_primeira": 3, "acertos_primeira": 5, "acertos_segunda": 3, "mesmo_rotulo": 4, "consertaria": 1, "estragaria": 2, "trocas": 1, "b": 1, "c": 0}
        leitura = {"metadados": {"corrida": "fase4_segundo_passe", "gerado_em": "2026-11-11T12:00:00"},
                   "condicoes": {"versao_ollama": "0.40.15", "verbetes_seguintes": 3, "posicoes": [4, 5, 6], "limite_de_tokens": des["limite_de_tokens"]},
                   "regra": {"alfa": 0.05, "texto": previa["regra"], "escolha": "fica a primeira resposta, salvo quando a segunda é mais provável e não acende sinal", "pareavel": True,
                             "mesma_versao_das_referencias": False, "ponte": {"corrida": "fase3b_ponte_04015", "versao": "0.40.15", "b": 1, "c": 0, "n": 35, "limite": 2, "pareavel": True}},
                   "resumo": {"casos": 72, "com_sinal": 24, "segundos_passes": 24, "acertos_primeira": 56, "acertos_final": 55, "erros_primeira_com_sinal": 10, "acertos_primeira_com_sinal": 14,
                              "acertos_segunda": 9, "mesmo_rotulo": 13, "consertaria": 2, "estragaria": 5, "trocas": 4, "b": 1, "c": 2, "saldo": -1, "p": 1.0, "ganhos": ["sin-5"],
                              "perdas": ["efe-2", "lex-8"], "completo": True, "sai_do_ruido": False, "veredito": "dentro do ruído", "tokens_entrada_mediana": 1290,
                              "tokens_entrada_mediana_primeira": 1185, "tokens_entrada_maximo": 1520, "limite_de_tokens": des["limite_de_tokens"], "acima_do_limite": 7, "segundos_mediana": 71.2,
                              "segundos_mediana_primeira": 66.0, "segundos_no_total": 1700.0},
                   "por_sinal": [{"sinal": g, **grupo} for g in des["grupos_de_sinal"]],
                   "por_banco": [{"banco": "avaliacao", "referencia": "corrida 22", **grupo, "casos": 36, "com_sinal": 8, "segundos_passes": 8, "acertos_primeira_no_banco": 31},
                                 {"banco": "ineditos", "referencia": "corrida 24", **grupo, "casos": 36, "com_sinal": 16, "segundos_passes": 16, "acertos_primeira_no_banco": 25}],
                   "por_alcance": [{"alcance": a, **grupo} for a in des["alcances"]],
                   "por_regra": [{"regra": nome, "trocas": t, "b": b, "c": c, "acertos": 56 + b - c, "p": 1.0}
                                 for nome, t, b, c in (("sempre a primeira (o agente de hoje)", 0, 0, 0), ("sempre a segunda", 11, 2, 5), ("a de maior probabilidade, sem olhar os sinais", 6, 2, 3),
                                                       ("a regra fixada antes da corrida", 4, 1, 2))],
                   "motivos": [{"motivo": "as duas respostas dão a mesma causa", "casos": 13, "troca": False},
                               {"motivo": "a segunda dá outra causa da lista, sem sinal aceso e com probabilidade maior", "casos": 4, "troca": True}],
                   "casos": [{"caso": "sin-5", "banco": "avaliacao", "sinal": des["grupos_de_sinal"][0], "gabarito": "campo_ausente", "rotulo_primeira": "colecao_no_lugar_de_objeto", "acerto_primeira": False,
                              "p_primeira": 0.625, "rotulo_segunda": "campo_ausente", "acerto_segunda": True, "p_segunda": 0.91, "selo_segunda": "medio", "fonte_divergente_segunda": False,
                              "efeito_da_segunda": "consertaria", "fica": "segunda", "motivo": "a segunda dá outra causa da lista, sem sinal aceso e com probabilidade maior", "mudou": "ganho",
                              "alcance": des["alcances"][1], "verbetes_segunda": ["campo_ausente", "campo_renomeado", "valor_fora_do_dominio"], "tokens_entrada": 1180}]}
        d2, h2 = tp.secao_segundo_passe(previa, leitura)
        for trecho in ("dentro do ruído", "2 dos 10", "5 dos 14", "de 56 a 55", "1,000", "fase3b_ponte_04015", "<code>sin-5</code>", "sempre a segunda", "a regra fixada antes da corrida"):
            self.assertIn(trecho, h2, trecho)
        self.assertNotIn("ainda não rodou", h2)
        self.assertEqual([s["n"] for s in d2["resultado"]["series"]], [[3, 3, 3], [5, 5, 5], [1, 1, 1], [2, 2, 2], [1, 1, 1], [0, 0, 0]])
        self.assertNotIn("—", h2)
        self.assertNotIn("→", h2)
        secao = self.html[self.html.index('<section id="segpasse"'):].split("</section>")[0]
        self.assertIn(f"{r['com_sinal']} de {r['casos']}", secao, "a página real traz a prévia")
        # ! Alteração de IA - Revisar: (11/11/2026) a aba também é montada com uma leitura que sai do próprio `experimento_segundo_passe.resumir`, e não só com a
        # leitura escrita à mão acima.
        # ! Motivo: a fila regera o painel logo depois da corrida, na janela do Eric; se a leitura gravada pela corrida tivesse uma chave com outro nome, a aba só
        # quebraria lá, no fim de quatro horas de máquina.
        import os
        os.environ.setdefault("RESULTADOS_DIR", "resultados_alvo")
        sys.path.insert(0, str(gd.EXP))
        from testar_pos_fase4 import _dados_do_segundo_passe, _resumo_sp
        real = _resumo_sp(_dados_do_segundo_passe(), corrida="fase4_segundo_passe")
        d3, h3 = tp.secao_segundo_passe(previa, real)
        self.assertIn(real["resumo"]["veredito"], h3)
        self.assertIn(f"<code>{real['casos'][0]['caso']}</code>", h3)
        self.assertNotIn("ainda não rodou", h3)
        self.assertEqual(len(d3["resultado"]["series"]), 6)

    def teste_analista_usa_os_numeros_dos_json(self):
        # ! Alteração de IA - Revisar: (10/11/2026, ficha 67 opção b, decisão 121) a aba "Analista de documentação" lê portoes_m1.json (a medida M1: os portões 3, 4 e 5 da
        # proposta aplicados às 92 propostas da corrida 20, contra a revisão humana) e, da corrida 27 (a medida M2), a prévia sem modelo e a leitura quando existirem; sem
        # os arquivos, o estado vazio.
        # ! Motivo: a regra do painel é uma aba por análise, lida do JSON versionado, e o Eric decide por ela. A M1 já rodou; a corrida 27 espera o Eric, e a aba tem de
        # mostrar as duas coisas sem número digitado. Os gráficos existem antes e depois da corrida, porque todo gráfico da página precisa da sua leitura.
        self.assertIn("analista", [sid for _, abas in tp.NAV for sid, _, _ in abas])
        for f in ("analistaPortoes", "analistaSequencia"):
            self.assertIn(f"function {f}(", tp.JS_TOPICOS)
            self.assertIn(f, tp.DESENHAR_TOPICOS["analista"])
        self.assertIn("analista", pl.RESPOSTA_SIMPLES)
        for g in ("g-analista-portoes", "g-analista-sequencia"):
            self.assertIn(g, pl.COMO_LER_GRAFICO)
        _, vazia = tp.secao_analista(None, None, None)
        self.assertIn('<section id="analista"', vazia)
        self.assertIn("portoes_de_edicao.py --m1", vazia)
        m1 = self.ctx.get("portoes_m1")
        self.assertTrue(m1, "portoes_m1.json existe em resultados_alvo/fase4")
        r = m1["resumo"]
        d, h = tp.secao_analista(m1, None, None)
        for trecho in (f"{r['forma_recusa']} das {r['propostas']}", f"{r['sobram_depois_dos_tres']} de {r['revisadas']}", "decisão 121", "ficha 67", "M1", "corrida 20", "g-analista-portoes",
                       "g-analista-sequencia", f"<code>{m1['revisadas'][0]['caso']}</code>", "revisão humana"):
            self.assertIn(trecho, h, trecho)
        self.assertEqual(len(d["portoes"]["grupos"]), len(m1["por_portao"]))

        def recusa(p, veredito):
            return next(x["recusa"] for x in p["nas_revisadas"]["por_veredito"] if x["veredito"] == veredito)

        self.assertEqual([s["n"] for s in d["portoes"]["series"]], [[recusa(p, v) for p in m1["por_portao"]] for v in ("Errada", "Parcial", "Correta")])
        etapas = m1["em_sequencia"] + m1["outras_sequencias"]
        self.assertEqual([sum(s["n"][i] for s in d["sequencia"]["series"]) for i in range(len(d["sequencia"]["grupos"]))], [x["sobram"] for x in etapas])
        self.assertNotIn("→", h)
        secao = self.html[self.html.index('<section id="analista"'):].split("</section>")[0]
        self.assertIn(f"{r['forma_recusa']} das {r['propostas']}", secao, "a página real traz a M1")
        # ! Alteração de IA - Revisar: (11/11/2026, decisão 121) a parte da corrida 27 (medida M2) na mesma aba: antes de a corrida rodar, a prévia sem modelo
        # (analista_previa.json: os 54 casos, a ficha, o tamanho do pedido, as instruções congeladas com o hash) e dois gráficos que já existem (as três leituras só com a
        # corrida 20, e os casos com lacuna e sem lacuna); depois, a leitura (analista.json) com os três vereditos e, quando houver, a revisão humana às cegas.
        # ! Motivo: a corrida 27 roda na janela do Eric, e a aba tem de mostrar o que já se sabe e o prompt que ele aprova, e depois o resultado, sem ninguém mexer no
        # código. A leitura de teste sai do próprio `experimento_analista.resumir`, para o formato que a aba lê ser o que a corrida grava.
        import os
        os.environ.setdefault("RESULTADOS_DIR", "resultados_alvo")
        sys.path.insert(0, str(gd.EXP))
        import experimento_analista as ea
        from testar_pos_fase4 import _dados_do_analista
        for f in ("analistaLeituras", "analistaCasos"):
            self.assertIn(f"function {f}(", tp.JS_TOPICOS)
            self.assertIn(f, tp.DESENHAR_TOPICOS["analista"])
        for g in ("g-analista-leituras", "g-analista-casos"):
            self.assertIn(g, pl.COMO_LER_GRAFICO)
        previa = self.ctx.get("analista_previa")
        self.assertTrue(previa, "analista_previa.json existe em resultados_alvo/fase4")
        p, c20 = previa["resumo"], previa["corrida_20"]
        d3, h3 = tp.secao_analista(m1, previa, None)
        for trecho in ("ainda não rodou", previa["prompt"]["hash_das_instrucoes"], f"{p['com_lacuna']} de {p['casos']}", "rodar_fila_pre_fase5.ps1", "g-analista-leituras", "g-analista-casos",
                       "corrida 27", "M2", "revisao_propostas.py", f"<code>{previa['casos'][0]['caso']}</code>", previa["prompt"]["lembrete_final"], f"{p['minutos_estimados']} minutos",
                       f"{r['forma_recusa']} das {r['propostas']}", "g-analista-portoes"):
            self.assertIn(trecho, h3, trecho)
        self.assertIn('<pre class="bruto">', h3, "as instruções do analista aparecem inteiras, como texto")
        # antes da corrida o gráfico das leituras só tem a corrida 20, e o dos casos só os grupos e quem o desenho chamaria
        self.assertEqual([s["nome"] for s in d3["leituras"]["series"]], ["corrida 20"])
        self.assertEqual(d3["leituras"]["series"][0]["rotulos"], [f"{c20['abstencoes']} de {c20['casos']}", f"{c20['afirmacoes']} de {c20['com_texto']}",
                                                                 f"{c20['por_veredito']['Correta']} de {c20['passaram_nos_filtros']}"])
        self.assertEqual(len(d3["leituras"]["grupos"]), 3)
        self.assertEqual([s["nome"] for s in d3["casos"]["series"]], ["casos do grupo", "o desenho chamaria o analista"])
        self.assertEqual(d3["casos"]["series"][0]["n"], [p["com_lacuna"], p["sem_lacuna"]])
        self.assertEqual(sum(d3["casos"]["series"][1]["n"]), p["seriam_chamados"])
        self.assertEqual(d3["portoes"], d["portoes"], "os gráficos da M1 continuam os mesmos")
        self.assertNotIn("→", h3)
        # o prompt de exemplo traz o verbete como o modelo o lê, e o verbete é texto de origem: o travessão dele fica; fora desses blocos, nenhum
        self.assertNotIn("—", re.sub(r"<pre.*?</pre>", "", h3, flags=re.DOTALL))
        # com a leitura da corrida, a aba mostra as três leituras com o veredito de cada uma e deixa de dizer que não rodou
        x = _dados_do_analista()
        lei = ea.resumir(x["registros"], x["corrida20"], x["condicoes"], ponte=x["ponte"], corrida="fase4_analista", gerado_em="2026-11-11T12:00:00")
        d4, h4 = tp.secao_analista(m1, previa, lei)
        self.assertNotIn("ainda não rodou", h4)
        for trecho in ("2 de 10", "5 de 6", "sai do ruído: mais afirmações na corrida 27", "falta a revisão humana", "fase3b_ponte_04015", "<code>c-n1</code>", "dentro do ruído",
                       "A rota de lista devolve os sete campos do contrato em cada item.", ea.DESTINOS[-1], "g-analista-leituras", "g-analista-casos"):
            self.assertIn(trecho, h4, trecho)
        self.assertEqual([s["nome"] for s in d4["leituras"]["series"]], ["corrida 20", "corrida 27"])
        self.assertEqual(d4["leituras"]["series"][1]["rotulos"], ["2 de 10", "5 de 6", "sem revisão"])
        self.assertEqual(d4["leituras"]["series"][1]["n"], [20.0, 83.3, None])
        self.assertEqual([s["nome"] for s in d4["casos"]["series"]], ["casos do grupo", "o desenho chamaria o analista", "abstenções", "propostas", "passam nos cinco portões"])
        self.assertEqual([s["n"] for s in d4["casos"]["series"]][2:], [[0, 2], [7, 0], [4, 0]])
        # com a revisão humana às cegas gravada, entram quem revisou, a parcela correta das duas corridas e os portões contra a revisão
        revisao = {"quem": "revisor de teste", "itens": [{"origem": "27", "caso": c, "veredito": v} for c, v in (("c-n1", "Correta"), ("c-n2", "Correta"), ("c-n3", "Parcial"), ("c-s1", "Errada"),
                                                                                                             ("c-x8", "Correta"), ("c-x9", "Correta"))]
                   + [{"origem": "20", "caso": f"z-{n}", "veredito": v} for n, v in enumerate(["Correta"] * 2 + ["Parcial"] * 9 + ["Errada"] * 9)]}
        lei_r = ea.resumir(x["registros"], x["corrida20"], x["condicoes"], ponte=x["ponte"], corrida="fase4_analista", gerado_em="2026-11-11T12:00:00", revisao=revisao)
        d5, h5 = tp.secao_analista(m1, previa, lei_r)
        for trecho in ("revisor de teste", "4 de 6", "2 de 20", "sai do ruído: parcela correta maior na corrida 27", "pelo mesmo revisor"):
            self.assertIn(trecho, h5, trecho)
        self.assertNotIn("falta a revisão humana", h5)
        self.assertEqual(d5["leituras"]["series"][1]["rotulos"], ["2 de 10", "5 de 6", "4 de 6"])
        self.assertIn(f"{p['com_lacuna']} de {p['casos']}", secao, "a página real traz a prévia da corrida 27")

    def teste_fluxo_usa_os_numeros_dos_json(self):
        # ! Alteração de IA - Revisar: (10/11/2026, decisão 118, sessão da pesquisa) a aba "Fluxo do agente" lê resumo_para_o_painel.json (as contagens da rodada 7 da pesquisa, os
        # vereditos por ideia, o mapa e as tabelas, gerados por integrar_pesquisa_fluxo_do_agente.py) e medidas_do_repositorio.json (os números das corridas, de
        # medidas_fluxo_do_agente.py), e mostra as fichas 65 a 67; sem os arquivos, o estado vazio. A aba Pesquisa passa a contar a rodada 7.
        # ! Motivo: a regra do painel é uma aba por análise, lida dos JSON versionados, e o Eric decide por ela: as três fichas novas estão abertas, e os números da aba têm
        # de ser os dos dois arquivos, nunca digitados.
        self.assertIn("fluxo", [sid for _, abas in tp.NAV for sid, _, _ in abas])
        for f in ("fluxoConferencia", "fluxoPosicao", "fluxoCusto", "fluxoAfirmacoes"):
            self.assertIn(f"function {f}(", tp.JS_TOPICOS)
            self.assertIn(f, tp.DESENHAR_TOPICOS["fluxo"])
        self.assertIn("fluxo", pl.RESPOSTA_SIMPLES)
        for g in ("g-fluxo-conferencia", "g-fluxo-posicao", "g-fluxo-custo", "g-fluxo-afirmacoes"):
            self.assertIn(g, pl.COMO_LER_GRAFICO)
        self.assertIn(("fluxo", "Tema"), pl.TABELAS_A_VISTA)
        _, vazia = tp.secao_fluxo(None, None, [])
        self.assertIn('<section id="fluxo"', vazia)
        self.assertIn("integrar_pesquisa_fluxo_do_agente.py", vazia)
        resumo, medidas = self.ctx.get("fluxo_resumo"), self.ctx.get("fluxo_medidas")
        self.assertTrue(resumo and medidas, "resumo_para_o_painel.json e medidas_do_repositorio.json existem em dados/pesquisa-fluxo-do-agente")
        d, h = tp.secao_fluxo(resumo, medidas, self.ctx["pend"])
        tot = resumo["totais"]
        conf = medidas["ideia_1"]["conferencia_depois_da_resposta"]["por_corrida"]
        os72 = medidas["ideia_2"]["os_72_casos"]
        forma = medidas["ideia_3"]["forma_de_instrucao"]
        cen = medidas["ideia_3"]["cenarios_do_analista"]
        for trecho in (f"{tot['fontes']} fontes", f"{tot['aprovadas']} de {tot['afirmacoes']}", f"{conf[3]['erros_contraditos']} de {conf[3]['erros']}",
                       f"{os72['disparos']} de {os72['casos']}", f"{forma['em_forma_de_instrucao']} de {forma['propostas']}", "ficha 65", "ficha 66", "ficha 67", "decisão 118",
                       "proposta-analista-de-documentacao.md", "levantamento-2026-11-10-fluxo-do-agente.md", "g-fluxo-conferencia", "g-fluxo-posicao", "g-fluxo-custo", "g-fluxo-afirmacoes",
                       "Como ler", "tab-mapa-fluxo", resumo["vereditos"][0]["nome"], resumo["vereditos"][2]["nome"], "corrida 25"):
            self.assertIn(trecho, h, trecho)
        self.assertNotIn("→", h)
        self.assertNotIn("—", h)
        self.assertNotIn("{{", h)
        # os dados dos gráficos batem com os dois arquivos
        self.assertEqual(len(d["afirmacoes"]["topicos"]), tot["topicos"])
        self.assertEqual(sum(sum(s["n"]) for s in d["afirmacoes"]["series"]), tot["afirmacoes"])
        self.assertEqual([s["n"] for s in d["conferencia"]["series"]], [[c["erros_contraditos"] for c in conf], [c["erros"] - c["erros_contraditos"] for c in conf]])
        c24, c22 = medidas["ideia_2"]["corrida_24"], medidas["ideia_2"]["corrida_22"]["cruzamento"]
        self.assertEqual([s["n"] for s in d["posicao"]["series"]], [[p["erros"] for p in c24["posicao_do_verbete_certo"]], [p["erros"] for p in c22["posicao_do_verbete_certo"]]])
        self.assertEqual(d["custo"]["segundos"], [cen["medido_hoje"]["segundos"]] + [c["segundos"] for c in cen["cenarios"]])
        self.assertEqual(len(d["custo"]["cenarios"]), len(d["custo"]["segundos"]))
        # o mapa traz uma linha por opção, com o veredito lido do resumo
        for linha in resumo["mapa"]:
            self.assertIn(linha["opcao"], h)
        # a aba diz se a corrida 25 já rodou, pelo arquivo de medidas
        self.assertIn("ainda não rodou" if not medidas["ideia_3"]["corrida_25"]["rodou"] else "já rodou", h)
        import copy
        rodou = copy.deepcopy(medidas)
        rodou["ideia_3"]["corrida_25"] = {"rodou": True, "resumo": {"veredito": "dentro do ruído"}}
        self.assertIn("já rodou", tp.secao_fluxo(resumo, rodou, self.ctx["pend"])[1])
        # a página real traz a aba, e a aba Pesquisa conta a rodada 7
        secao = self.html[self.html.index('<section id="fluxo"'):].split("</section>")[0]
        self.assertIn("ficha 67", secao)
        self.assertEqual(tp.RODADAS[-1][0], "levantamento-2026-11-10-fluxo-do-agente.md")
        rodadas = self.dados_t["pesquisa"]["rodadas"]
        self.assertEqual((rodadas[-1]["aprovadas"], rodadas[-1]["rejeitadas"], rodadas[-1]["nao_verificadas"]), (tot["aprovadas"], tot["rejeitadas"], tot["nao_verificadas"]))
        pesquisa = self.html[self.html.index('<section id="pesquisa"'):].split("</section>")[0]
        self.assertIn("§6.16", pesquisa)
        self.assertIn("Rodada 7", pesquisa)

    def teste_conferencia_mostra_as_respostas_do_eric(self):
        # ! Alteração de IA - Revisar: (06/11/2026, decisão 100) com as respostas gravadas, a aba diz que os casos foram conferidos, por quem, como e o que mudou.
        # ! Motivo: a ficha 44 nasceu de a conferência não estar registrada, e a aba não pode continuar dizendo que nenhuma pessoa conferiu.
        real, resp = self.ctx.get("conferencia_ineditos"), self.ctx.get("conferencia_respostas")
        self.assertTrue(real and resp, "o documento e as respostas existem")
        _, sem = tp.secao_conferencia(real)
        self.assertIn("nenhuma pessoa os conferiu ainda", sem)
        _, h = tp.secao_conferencia(real, resp)
        self.assertNotIn("nenhuma pessoa", h)
        for trecho in ("decisão 100", f'{len(resp["respostas"])} apontados', "conferencia_ineditos_respostas.json", "Resposta do Eric", "resultados da corrida 18e"):
            self.assertIn(trecho, h)
        self.assertEqual(set(resp["respostas"]), {x["caso"] for x in real["casos"] if x["veredito"] == "ver"})
        self.assertEqual(resp["mudancas"], [])
        secao = self.html[self.html.index('<section id="conferencia"'):].split("</section>")[0]
        self.assertIn("decisão 100", secao, "a página real traz a conferência")

    def teste_experimento_usa_os_numeros_do_json(self):
        # ! Alteração de IA - Revisar: (05/11/2026, decisão 91) a aba da corrida 23 lê experimento_prompt.json: o acerto de cada condição contra a corrida 16, caso a caso, sem número digitado à mão.
        # ! Motivo: a regra do painel é uma aba por análise, e o número dos dois itens vai para o TCC.
        self.assertIn("experimento", [sid for _, abas in tp.NAV for sid, _, _ in abas])
        self.assertIn("function expAcerto(", tp.JS_TOPICOS)
        self.assertIn("function expTrocas(", tp.JS_TOPICOS)
        d, vazia = tp.secao_experimento(None, self.ctx["road"], gd.cartoes_corridas)
        self.assertIn('<section id="experimento"', vazia)
        self.assertIn("ainda não foi rodada", vazia)
        self.assertEqual(d["condicoes"], [])
        exp = self.ctx.get("experimento_prompt")
        if not exp:
            return
        d, h = tp.secao_experimento(exp, self.ctx["road"], gd.cartoes_corridas)
        self.assertEqual(d["base"]["acerto_pct"], exp["base"]["acerto_pct"])
        self.assertEqual([(x["b"], x["c"]) for x in d["condicoes"]], [(x["b"], x["c"]) for x in exp["por_condicao"]])
        for x in exp["por_condicao"]:
            self.assertIn(f'{x["acertos"]} de {x["n"]}', h)
        for trecho in ('id="g-exp-acerto"', 'id="g-exp-trocas"', "tb_f4_exp_resumo", "decisão 91"):
            self.assertIn(trecho, h)
        self.assertNotIn("—", h.split('<p class="lead">')[1].split("</p>")[0], "a frase de abertura não leva travessão")

    def teste_conferencia_dos_ineditos_usa_o_json_e_mostra_cada_caso(self):
        # ! Alteração de IA - Revisar: (05/11/2026, decisão 92) a aba da conferência lê conferencia_ineditos.json: os casos para olhar primeiro, e cada caso com o gabarito, o que a corrida 17 viu e a pré-análise.
        # ! Motivo: o Eric decide pelo painel, e a ficha 46 pede a conferência dele antes da corrida 24; a pré-análise é do Claude e a aba precisa dizer isso.
        self.assertIn("conferencia", [sid for _, abas in tp.NAV for sid, _, _ in abas])
        _, vazia = tp.secao_conferencia(None)
        self.assertIn('<section id="conferencia"', vazia)
        self.assertIn("gerar_conferencia_ineditos.py", vazia)
        sint = {"resumo": {"casos": 2, "ok": 1, "ver": 1, "reproduzem": 1, "fora_da_tela": 1, "sem_preanalise": 0},
                "por_classe": [{"classe": 1, "casos": 2, "ok": 1, "ver": 1, "reproduzem": 1}],
                "casos": [{"caso": "x-2", "classe": 1, "nivel": 3, "veredito": "ver", "o_que_olhar": "Olhar o <id>.", "causa_vizinha": "campo_ausente", "evidencia": "b.py:2", "tela": "fora: sem tela",
                           "entrada": {"requisicao": "POST /api/pedidos", "status": 201, "contrato": "id: inteiro", "corpo": '{"id": "a"}', "sintoma": "Sintoma dois"},
                           "gabarito": {"causa_raiz": "tipo_divergente", "campo_afetado": "id", "termos_esperados": ["tipo"], "termos_proibidos": ["json"]}},
                          {"caso": "x-1", "classe": 1, "nivel": 1, "veredito": "ok", "o_que_olhar": "", "causa_vizinha": None, "evidencia": "a.py:1", "tela": "reproduz: corpo diferente",
                           "entrada": {"requisicao": "GET /api/produtos", "status": 200, "contrato": "id: inteiro", "corpo": "{}", "sintoma": "Sintoma um", "observacao": "Observação um", "arvore": "document"},
                           "gabarito": {"causa_raiz": "corpo_vazio", "campo_afetado": None, "termos_esperados": [], "termos_proibidos": []}}]}
        _, h = tp.secao_conferencia(sint)
        for trecho in ("x-2", "x-1", "tipo_divergente", "corpo_vazio", "Sintoma um", "Observação um", "fora: sem tela", "reproduz: corpo diferente", "ficha 46", "pré-análise"):
            self.assertIn(trecho, h)
        self.assertIn("Olhar o &lt;id&gt;.", h, "o texto do caso entra escapado")
        self.assertLess(h.index("<code>x-2</code>"), h.index("<code>x-1</code>"), "os casos para olhar vêm primeiro")
        real = self.ctx.get("conferencia_ineditos")
        if real:
            secao = self.html[self.html.index('<section id="conferencia"'):].split("</section>")[0]
            self.assertEqual(secao.count("<details>"), real["resumo"]["casos"] + 1, "um bloco por caso, mais o resumo por classe")

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
        # ! Alteração de IA - Revisar: (05/11/2026) o título do bloco passou de "Execuções sem Task Success" para "Execuções que não chegaram ao resultado (sem Task Success)".
        # ! Motivo: o Eric pediu texto à vista sem a sigla solta; o teste continua conferindo que o bloco aparece só quando há execução sem sucesso.
        self.assertIn("Execuções que não chegaram ao resultado", h)
        self.assertIn("candidato_invalido", h)
        self.assertIn("tb_f4_cenarios_sem_sucesso", h)
        _, h_sem = tp.secao_cenarios({**sint, "sem_task_success": []}, None, self.ctx["road"], gd.cartoes_corridas)
        self.assertNotIn("Execuções que não chegaram ao resultado", h_sem)
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
        self.assertIn("As duas últimas corridas, cenário a cenário", h2)
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
        cen_ = self.ctx.get("cenarios_v3") or self.ctx.get("cenarios_v2") or self.ctx.get("cenarios")
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
        # ! Alteração de IA - Revisar: (05/11/2026) a frase conferida passou de "por gatilho" para "aviso de checagem extra".
        # ! Motivo: a aba deixou de usar "gatilho" no texto à vista; o teste continua conferindo que o cartão do sinal por esse aviso existe.
        self.assertIn("aviso de checagem extra", h)
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
        # ! Alteração de IA - Revisar: (05/11/2026, decisão 95) a medida com revisor humano passou a em aberto, para depois da Pós-Fase 4.
        # ! Motivo: o Eric reabriu a ficha 40; o bloco da sessão continua sem mandar decidir aqui, porque quem revisa fica para quando o formato estiver fechado.
        self.assertIn("em aberto (decisão 95)", h_rev)
        self.assertNotIn("ficha 40", h_rev, "o bloco da sessão não pede decisão")
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
        # ! Alteração de IA - Revisar: (11/11/2026) a aba do fechamento passa a ser a última do grupo da Fase 4; quem abre o grupo é a visão da fase.
        # ! Motivo: com a navegação por fase, o grupo abre pela aba de visão (o caminho da fase e os tópicos) e segue a ordem do documento do TCC, em que o fechamento vem no fim.
        grupo = next(abas for nome, abas in tp.NAV if nome == "Fase 4")
        self.assertEqual(grupo[0][0], "f-4", "a visão da fase abre o grupo")
        self.assertEqual(grupo[-1][0], "fechamentof4", "a aba do fechamento fecha o grupo da fase")
        self.assertEqual(tp._classe_regra("Cumprida"), "cumprida")
        self.assertEqual(tp._classe_regra("Cumprida, com ressalva: os 100% vêm do desenho"), "ressalva")
        self.assertEqual(tp._classe_regra("Não cumprida: limitação declarada, decisão 82"), "nao")
        self.assertEqual(tp._classe_regra("Medida: o plano não fixou limite"), "medida")
        md = ("# Relatório\n\n## 1. Perguntas\n\ntexto da seção um\n\n## 10. As regras\n\n| Regra | O que ela pede | Corrida | Resultado | Estado |\n|---|---|---|---|---|\n"
              "| R1 | pede a | 17 | 37 de 37 | Cumprida |\n| R2 | pede b | 18b | b + c = 9 | Não cumprida: limitação declarada |\n| R3 | pede c | 19 | 160 de 160 | Cumprida, com ressalva: desenho |\n"
              "| R4 | pede d | 20 | 100,0% | Medida: sem limite |\n\n## 11. Entrega\n\ntexto da seção onze\n\n## 12. Limitações\n\ntexto da seção doze\n\n## 13. O que não saiu\n\ntexto da seção treze\n\n## 15. O que o TCC carrega\n\ntexto da seção quinze\n")
        tela = {"resumo": {"concordam": 26, "casos": 37, "discordantes": 9, "limite_r2": 3, "b": 2, "c": 7}}
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
        r2 = (self.ctx.get("tela_v4") or self.ctx.get("tela_v3") or self.ctx["tela_v2"])["resumo"]
        secao_f4 = self.html[self.html.index('<section id="fechamentof4"'):].split("</section>")[0]
        self.assertIn(f'{r2["concordam"]} de {r2["casos"]}', secao_f4)
        self.assertNotEqual(self.ctx["tela"]["resumo"]["concordam"], r2["concordam"])
        if self.ctx.get("tela_v4"):
            self.assertIn("corrida 18d;", secao_f4)
            self.assertNotIn("corrida 18c;", secao_f4, "o cartão diz a corrida vigente")
        elif self.ctx.get("tela_v3"):
            self.assertIn("corrida 18c", secao_f4)
            self.assertNotIn("corrida 18b;", secao_f4, "o cartão diz a corrida vigente")
        faltam = tp._corridas_que_faltam_f4(self.ctx["road"])
        if faltam:
            self.assertIn("Corridas que faltam antes da Fase 5", self.html)
            self.assertIn(f'id="corrida-{faltam[0]}-f4"', self.html)
            # ! Alteração de IA - Revisar: (10/11/2026, decisão 116) o cartão das corridas que faltam não diz mais de que fichas elas vieram.
            # ! Motivo: o texto fixo dizia "pedidas pelas respostas às fichas 42 a 44", o que valia para as corridas 18c, 21c, 23 e 24; a corrida 25 veio da ficha 63, e
            # o cartão de cada corrida, lido do roadmap, já diz de onde ela veio.
            self.assertNotIn("pedidas pelas respostas às fichas 42 a 44", self.html)
            self.assertIn("o comando e o pré-requisito de cada uma estão nos cartões abaixo", self.html)

    def teste_slots_cobrem_os_modelos_das_fases(self):
        for m in self.ctx["dados"]["modelos"]:
            self.assertIn(m, tp.SLOTS)
        for x in self.ctx["ablacao"]["por_modelo_condicao"]:
            self.assertIn(x["modelo"], tp.SLOTS)

    def teste_dados_dos_topicos_sao_serializaveis(self):
        json.dumps(self.dados_t, ensure_ascii=False)


# ! Alteração de IA - Revisar: (05/11/2026) testes das duas regras de painel_leituras: todo gráfico com "Como ler" e nenhum dado cru à vista.
# ! Motivo: o Eric pediu o gráfico e a leitura à vista e os dados em "mais informações"; sem o teste, a próxima aba nova sairia sem explicação e ninguém notaria.
class TesteLeituras(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pagina = (gd.RAIZ / "Documentacao" / "dashboard" / "painel-do-projeto.html").read_text(encoding="utf-8")

    def teste_todo_grafico_tem_como_ler_e_nenhuma_leitura_sobra(self):
        ids = set(re.findall(r'<canvas id="([^"]+)"', self.pagina))
        self.assertTrue(ids)
        self.assertEqual(ids - set(pl.COMO_LER_GRAFICO), set(), "gráfico sem explicação")
        self.assertEqual(set(pl.COMO_LER_GRAFICO) - ids, set(), "explicação de gráfico que não existe")
        self.assertEqual(self.pagina.count('class="como-ler"') >= len(ids), True)

    def teste_nenhuma_tabela_de_dados_a_vista(self):
        ini, fim = self.pagina.index("<main>"), self.pagina.index("</main>")
        aba, prof, soltas = "", 0, []
        for m in re.finditer(r'<section id="([^"]+)"|<details|</details>|<table><thead><tr><th[^>]*>(.*?)</th>', self.pagina[ini:fim], re.S):
            t = m.group(0)
            if t.startswith("<section"):
                aba = m.group(1)
            elif t.startswith("<details"):
                prof += 1
            elif t == "</details>":
                prof -= 1
            elif prof == 0 and (aba, re.sub(r"<[^>]+>", "", m.group(2)).strip()) not in pl.TABELAS_A_VISTA:
                soltas.append((aba, m.group(2)[:40]))
        self.assertEqual(soltas, [])

    def teste_aplicar_recolhe_tabela_com_o_filtro_e_guarda_a_que_e_conteudo(self):
        tab = '<div class="tabela"><table><thead><tr><th>Modelo</th></tr></thead><tbody><tr><td>1</td></tr></tbody></table></div>'
        filtro = '<div class="filtros filtro-tabela" data-alvo="x"><button>a</button></div>'
        conteudo = '<div class="tabela"><table><thead><tr><th>Regra</th></tr></thead><tbody></tbody></table></div>'
        grafico = '<div class="chart"><canvas id="g-doc"></canvas></div>'
        html_ = f'<style>a{{}}</style><main><section id="fechamentof4"><h2>Título</h2>{filtro}{tab}{conteudo}{grafico}{tab}</section></main>'
        saida = pl.aplicar(html_)
        self.assertIn(f'<summary>Mais informações: Título</summary>{filtro}{tab}</details>', saida)
        self.assertIn(f'</details>{conteudo}', saida)
        self.assertIn('<summary>Mais informações: Título (2)</summary>', saida)
        self.assertIn(f'{grafico}<p class="como-ler"><strong>Como ler:</strong>', saida)
        self.assertIn(pl.CSS, saida)

    # ! Alteração de IA - Revisar: (05/11/2026, decisão 92) a tabela dos casos para olhar fica à vista na aba da conferência.
    # ! Motivo: no painel publicado ela saiu recolhida em "Mais informações", e é o conteúdo principal da aba: é por ela que o Eric começa a conferência.
    def teste_casos_para_olhar_ficam_a_vista_na_conferencia(self):
        tab = '<div class="tabela"><table><thead><tr><th>Caso</th></tr></thead><tbody><tr><td>x-1</td></tr></tbody></table></div>'
        saida = pl.aplicar(f'<style>a{{}}</style><main><section id="conferencia"><h2>Os casos para olhar</h2>{tab}</section></main>')
        self.assertNotIn("Mais informações: Os casos para olhar", saida)
        self.assertIn(tab, saida)

    def teste_figura_repetida_vai_para_mais_informacoes_com_a_leitura(self):
        fig = '<figure><img src="x" alt="Fase 3 · acerto"><figcaption>Figura 12 — Fase 3</figcaption></figure>'
        saida = pl.aplicar(f'<style></style><main><section id="fase3"><h2>T</h2>{fig}</section></main>')
        self.assertIn('<details class="mais-info"><summary>Mais informações: figura 12, Fase 3 · acerto</summary>' + fig + '<p class="como-ler">', saida)

    # ! Alteração de IA - Revisar: (11/11/2026) a frase direta é procurada na página sem as marcas do glossário e já com a troca por "grupo".
    # ! Motivo: a página gravada passa por mais dois passos depois de painel_leituras (gerar_dashboard.montar): o glossário marca o termo dentro da frase, e
    # painel_grupo troca o nome do autor e "você". Comparar letra a letra com o texto de RESPOSTA_SIMPLES deixaria de achar a frase sem que ela tivesse saído.
    def teste_resposta_simples_entra_e_o_paragrafo_antigo_fica_recolhido(self):
        pagina = re.sub(r'<span class="termo"[^>]*>([^<]*)</span>', r"\1", self.pagina)
        for aba, texto in pl.RESPOSTA_SIMPLES.items():
            self.assertIn(f'<p class="lead">{pg.texto_para_o_grupo(texto)}</p><details class="mais-info"><summary>Mais informações: a resposta com todos os números</summary>', pagina, aba)
            self.assertIn(f'<section id="{aba}"', self.pagina, aba)
        saida = pl.aplicar('<style></style><main><section id="tela" hidden><h1>T</h1><p class="lead">b + c = 9</p></section></main>')
        self.assertIn(pl.RESPOSTA_SIMPLES["tela"], saida)
        self.assertIn("<p>b + c = 9</p></details>", saida)

    def teste_nota_vai_com_a_tabela_e_titulo_sem_conteudo_sai(self):
        tab = '<div class="tabela"><table><thead><tr><th>Modelo</th></tr></thead><tbody></tbody></table></div>'
        saida = pl.aplicar(f'<style></style><main><section id="tela"><h2>Dados</h2><p class="nota">Bloco x.</p>{tab}<h2>Outro</h2><p>Texto.</p>{tab}</section></main>')
        self.assertNotIn("<h2>Dados</h2>", saida)
        self.assertIn(f'<summary>Mais informações: Dados</summary><p class="nota">Bloco x.</p>{tab}</details>', saida)
        self.assertIn("<h2>Outro</h2><p>Texto.</p><details", saida)

    def teste_cartoes_de_corrida_so_a_vista_no_roadmap_e_no_fechamento(self):
        cartao = '<div class="corridas"><article><div class="fatos2"><div>x</div></div></article></div>'
        saida = pl.aplicar(f'<style></style><main><section id="tela"><h2>As corridas</h2>{cartao}</section><section id="fechamentof4"><h2>Faltam</h2>{cartao}</section></main>')
        self.assertIn(f'<summary>Mais informações: As corridas</summary>{cartao}</details>', saida)
        self.assertIn(f'<h2>Faltam</h2>{cartao}', saida)

    def teste_leituras_sem_travessao_nem_seta(self):
        for texto in list(pl.COMO_LER_GRAFICO.values()) + list(pl.COMO_LER_FIGURA.values()) + list(pl.RESPOSTA_SIMPLES.values()):
            self.assertNotRegex(texto, "[—→↔]")
        self.assertEqual(set(pl.COMO_LER_FIGURA), set(gd.FIGURAS))


if __name__ == "__main__":
    unittest.main(verbosity=1)
