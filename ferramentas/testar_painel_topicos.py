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
        "ineditos": gd.ler_json(gd.EXP / "resultados_alvo" / "fase3b_ineditos" / "resumo_fase3.json"),
        "curadoria": gd.ler_json(gd.EXP.parent / "biblioteca_producao" / "curadoria.json"),
        "planilha_curadoria": (gd.F3 / "curadoria_L1__qwen2.5_7b.md").read_text(encoding="utf-8"),
        "recuperador": gd.ler_json(gd.EXP / "resultados_alvo" / "recuperador" / "experimento_recuperador.json"),
        "ablacao": gd.ler_json(gd.EXP / "resultados_alvo" / "ablacao_base_instruct" / "resumo_metricas.json"),
        "medicao_mcp": gd.ler_json(medicao) if medicao.exists() else None,
        "readme": (gd.RAIZ / "README.md").read_text(encoding="utf-8"),
        "analise3b": gd.ler_json(gd.F3 / "analise_fase3b.json"),
        "relatorio3b": (gd.MEMORIAL / "3-resultados-e-analises" / "fase-3b-relatorio.md").read_text(encoding="utf-8"),
        "pend": pt.ler_pendencias(gd.MEMORIAL / "pendencias.md"),
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

    def teste_comparativo_usa_os_numeros_do_json(self):
        cq = self.ctx["cq"]
        n_vence = len(cq["onde_o_coder_vence"])
        self.assertIn(f"<b>{n_vence}</b>", self.html)
        self.assertEqual(len(self.dados_t["cq"]["trajetoria"]["36"]), 7)  # 2-A, 2-B A0/A2, F3 L0..L3 (sem "melhor")
        self.assertEqual(len(self.dados_t["cq"]["confronto"]["90"]), 3 + 4)

    def teste_tres_b_compara_oficiais_e_ineditos_nas_mesmas_versoes(self):
        t = self.dados_t["tresb"]
        self.assertEqual(t["Ls"], ["0", "1", "3"])
        for m in t["modelos"]:
            self.assertEqual(set(t["ineditos"][m]), set(t["oficiais"][m]))

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

    def teste_curadoria_conta_as_edicoes_da_planilha(self):
        total = sum(sum(v.values()) for v in self.dados_t["curadoria"]["por"].values())
        self.assertEqual(total, self.ctx["curadoria"]["edicoes_na_epoca"])

    def teste_mapa_de_filtros_sem_asteriscos_e_com_vereditos_contados(self):
        secao = self.html[self.html.index('<section id="pesquisa"'):]
        self.assertNotIn("**", secao.split("</section>")[0])
        self.assertRegex(secao, r'data-valor="adotado" aria-pressed="false">Adotado \(\d+\)')
        self.assertNotIn('data-valor="outro"', secao.split("</section>")[0])

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
