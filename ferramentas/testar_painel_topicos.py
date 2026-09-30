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
