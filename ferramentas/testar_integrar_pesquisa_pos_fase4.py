#!/usr/bin/env python3
# ! Alteração de IA - Revisar: testes novos (07/11/2026) do integrador da rodada 6 da pesquisa (Pós-Fase 4): os títulos dos
# arquivos de leitura descem de nível e perdem o H1; as referências são extraídas nos quatro formatos em que os subagentes
# as escreveram (negrito com numeração, negrito com marca de confiança no fim, parágrafo simples, complemento dentro de um
# item de lista); a subseção sai no formato fixo com a contagem de fontes; o bloco de referências entra antes do bloco da
# Pré-Fase 4, sem repetir referência já listada, e a frase do total é a mesma que o integrador da Pré-Fase 4 escreve; a linha
# do índice do Memorial entra logo depois da linha da Pré-Fase 4 e é regravável; o texto do script não usa travessão nem seta.
# ! Motivo: a rodada 6 não veio de um Workflow com JSON de sínteses, e sim de treze leituras em Markdown; sem os testes, um
# formato de referência que o extrator não reconhece sairia do levantamento sem aviso, e o bloco de referências, se entrasse
# depois do bloco da Pré-Fase 4, quebraria o --check de integrar_pesquisa_pre_fase4.py, que trata o bloco dele como o último.
"""Uso: python ferramentas/testar_integrar_pesquisa_pos_fase4.py"""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import integrar_pesquisa_pos_fase4 as ipp
import integrar_pesquisa_pre_fase4 as ip

TEXTO_A = ("# Base A: revisão no estilo pull request\n\nConsulta feita em 7 nov. 2026.\n\n## a) Modelo de revisão\n\n"
           "**1. GITHUB. About pull request reviews.** GitHub Docs. Disponível em: https://docs.github.com/x. Acesso em: 7 nov. 2026.\n"
           "- Uma revisão termina em um de três estados.\n\n### Detalhe\n\n"
           "**2. GITHUB. Reviewing proposed changes in a pull request.** GitHub Docs. Disponível em: https://docs.github.com/y. Acesso em: 7 nov. 2026.\n")
TEXTO_B = ("# Base B: indicador de progresso\n\n"
           "**NIELSEN, Jakob. Response times: the 3 important limits. Nielsen Norman Group, 1993. Disponível em: https://www.nngroup.com/articles/response-times-3-important-limits/. Acesso em: 7 nov. 2026.** (aberta e lida)\n"
           "- Estabelece os limites de 0,1 s, 1 s e 10 s.\n")
TEXTO_C = ("# Base C: árvore de decisão\n\n"
           "**1. MILLER, Tim. Explanation in artificial intelligence. Artificial Intelligence, v. 267, 2019. Disponível em: https://arxiv.org/abs/1706.07269. Acesso em: 7 nov. 2026.**\n"
           "- Fonte complementar, só bibliográfica (página aberta): LIM, B. Y.; DEY, A. K. Why and why not explanations. In: CHI, 2009. Disponível em: https://bibtex.github.io/CHI-2009-LimDA.html. Acesso em: 7 nov. 2026. Pelo título, é o estudo.\n"
           "- Complemento (aberta): https://langfuse.com/docs descreve as abas (Acesso em: 7 nov. 2026).\n")
TEXTO_REPO = ("# Repositório 05: sodiumsun/agenttrail\n\nFontes lidas: página do repositório.\n\n## 1 O que é\n\n- É um observador local.\n\n## 6 Referências\n\n"
              "SODIUMSUN. **agenttrail**: local observability for AI coding agents. Disponível em: https://github.com/sodiumsun/agenttrail. Acesso em: 7 nov. 2026. (Citada no README; não lida por mim.)\n")
TOPICOS_DE_TESTE = [("pos4-a", "a.md", "1", "O hub à imagem de uma pull request", "subagente"),
                    ("pos4-b", "b.md", "1", "A barra de progresso", "subagente"),
                    ("pos4-c", "c.md", "1", "A árvore de decisão", "subagente"),
                    ("pos4-repo", "repo.md", "3", "sodiumsun/agenttrail", "subagente")]
REFS = ("# Referências levantadas\n\n## 9. Referências levantadas\n\n"
        "Além das 7 do projeto de pesquisa, os levantamentos de 11/09, 21/09, 22/09, 29/09 e 01/10/2026 produziram as **3** referências abaixo, organizadas por tema.\n\n"
        "### Raciocínio\n\n"
        "- MILLER, T. Explanation in artificial intelligence. 2019. Disponível em: https://arxiv.org/abs/1706.07269. Acesso em: 1 out. 2026.\n"
        "- OUTRA, A. Título qualquer. 2020. Disponível em: https://exemplo.org/a. Acesso em: 1 out. 2026.\n\n"
        + ip.TITULO_REFS + "\n\n<!-- tag da Pré-Fase 4 -->\n\n"
        "- ZZZ, B. Último da lista. 2024. Disponível em: https://exemplo.org/z. Acesso em: 1 out. 2026.\n")
MEMORIAL = ("- [Levantamento: documentação autogerida](memorial/x.md): §6.13.\n"
            + ip.TAG_DO_INDICE + " (§6.14), gravada por integrar_pesquisa_pre_fase4.py. ! Motivo: sem a linha o índice não leva ao levantamento. -->\n"
            + ip.MARCA_DO_INDICE + "(memorial/2-pesquisa-e-literatura/levantamento-2026-10-01-pre-fase-4.md): §6.14, 14 de 14 tópicos integrados.\n"
            "- [Referências levantadas](memorial/2-pesquisa-e-literatura/referencias.md) — §9: todas as fontes, por tema.\n")


def _pasta_de_teste() -> Path:
    pasta = Path(tempfile.mkdtemp(prefix="pos4_"))
    for nome, texto in (("a.md", TEXTO_A), ("b.md", TEXTO_B), ("c.md", TEXTO_C), ("repo.md", TEXTO_REPO)):
        (pasta / nome).write_text(texto, encoding="utf-8")
    return pasta


class TestesIntegradorPosFase4(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pasta = _pasta_de_teste()
        cls.dados = ipp.carregar(cls.pasta, TOPICOS_DE_TESTE)

    def teste_tira_o_comentario_de_tag_do_topo_da_leitura(self):
        # ! Alteração de IA - Revisar: (07/11/2026) a tag de IA no topo de cada leitura não entra no levantamento.
        # ! Motivo: conferir_docs.py exige a tag em todo arquivo escrito por IA, e o comentário, se entrasse, ficaria no meio da subseção gerada.
        pasta = Path(tempfile.mkdtemp(prefix="pos4_tag_"))
        (pasta / "t.md").write_text("<!-- ! Alteração de IA - Revisar: leitura.\n     ! Motivo: teste. -->\n\n# Título\n\nCorpo.\n", encoding="utf-8")
        dados = ipp.carregar(pasta, [("pos4-t", "t.md", "1", "Título", "subagente")])
        self.assertEqual(dados["pos4-t"]["texto"], "Corpo.")

    def teste_rebaixa_os_titulos_e_tira_o_h1(self):
        self.assertEqual(ipp.rebaixar("# Título\n\nIntro.\n\n## A\n### B\n#### C\ntexto"), "Intro.\n\n##### A\n###### B\n###### C\ntexto")

    def teste_extrai_referencias_nos_formatos_dos_arquivos(self):
        self.assertEqual(ipp.extrair_referencias(TEXTO_A), [
            "GITHUB. About pull request reviews. GitHub Docs. Disponível em: https://docs.github.com/x. Acesso em: 7 nov. 2026.",
            "GITHUB. Reviewing proposed changes in a pull request. GitHub Docs. Disponível em: https://docs.github.com/y. Acesso em: 7 nov. 2026."])
        self.assertEqual(ipp.extrair_referencias(TEXTO_B), [
            "NIELSEN, Jakob. Response times: the 3 important limits. Nielsen Norman Group, 1993. Disponível em: https://www.nngroup.com/articles/response-times-3-important-limits/. Acesso em: 7 nov. 2026."])
        self.assertEqual(ipp.extrair_referencias(TEXTO_C), [
            "MILLER, Tim. Explanation in artificial intelligence. Artificial Intelligence, v. 267, 2019. Disponível em: https://arxiv.org/abs/1706.07269. Acesso em: 7 nov. 2026.",
            "LIM, B. Y.; DEY, A. K. Why and why not explanations. In: CHI, 2009. Disponível em: https://bibtex.github.io/CHI-2009-LimDA.html. Acesso em: 7 nov. 2026."])
        self.assertEqual(ipp.extrair_referencias(TEXTO_REPO), [
            "SODIUMSUN. agenttrail: local observability for AI coding agents. Disponível em: https://github.com/sodiumsun/agenttrail. Acesso em: 7 nov. 2026."])

    def teste_carrega_os_topicos_na_ordem_com_o_texto_rebaixado_e_as_fontes(self):
        self.assertEqual(list(self.dados), [t[0] for t in TOPICOS_DE_TESTE])
        a = self.dados["pos4-a"]
        self.assertEqual((a["titulo"], a["parte"], a["leitor"], a["n_fontes"]), ("O hub à imagem de uma pull request", "1", "subagente", 2))
        self.assertTrue(a["texto"].startswith("Consulta feita em 7 nov. 2026."))
        self.assertIn("##### a) Modelo de revisão", a["texto"])
        self.assertNotIn("# Base A", a["texto"])

    def teste_subsecao_no_formato_fixo_com_a_contagem_de_fontes(self):
        s = ipp.secao(3, "pos4-c", self.dados["pos4-c"])
        self.assertTrue(s.startswith("#### 6.15.3 A árvore de decisão (`pos4-c`; 2 fontes com endereço)\n\n*Leitura de:* subagente"), s[:160])
        self.assertIn("MILLER, Tim.", s)
        self.assertTrue(ipp.secao(4, "pos4-repo", self.dados["pos4-repo"]).startswith("#### 6.15.4 sodiumsun/agenttrail (`pos4-repo`; 1 fonte com endereço)"))

    def teste_render_na_ordem_fixa_com_o_mapa_no_fim_e_sem_travessao_nem_seta(self):
        t = ipp.render(self.dados, TOPICOS_DE_TESTE)
        self.assertIn("# Levantamento bibliográfico: Pós-Fase 4 (07/11/2026)", t)
        self.assertIn("### 6.15 Levantamento da Pós-Fase 4", t)
        posicoes = [t.index(f"#### 6.15.{i} ") for i in range(1, len(TOPICOS_DE_TESTE) + 1)]
        self.assertEqual(posicoes, sorted(posicoes))
        self.assertIn(f"#### 6.15.{len(TOPICOS_DE_TESTE) + 1} Mapa", t)
        self.assertLess(posicoes[-1], t.index("Mapa"))
        self.assertIn("| §6.15.1 | 1 | `pos4-a` | 2 |", t)
        self.assertNotIn("—", t)
        self.assertNotIn("→", t)

    def teste_o_mapa_cobre_todos_os_topicos_da_rodada(self):
        self.assertEqual([m[0] for m in ipp.MAPA], [t[0] for t in ipp.TOPICOS])
        for linha in ipp.MAPA:
            self.assertIn(linha[4], ("adotado", "ideia", "adiado", "descartado"), linha[0])

    def teste_bloco_de_referencias_entra_antes_do_bloco_da_pre_fase_4_e_e_regravavel(self):
        novo, novas, total = ipp.referencias_com_bloco(REFS, self.dados)
        self.assertEqual((novas, total), (5, 8))  # MILLER repete o endereço de uma já listada; sobram 2 + 1 + 1 + 1
        self.assertEqual(novo.count(ipp.TITULO_REFS), 1)
        self.assertLess(novo.index(ipp.TITULO_REFS), novo.index(ip.TITULO_REFS))
        self.assertIn(f"os levantamentos de {ip.DATAS_DOS_LEVANTAMENTOS} produziram as **8** referências abaixo", novo)
        self.assertEqual(novo.count("arxiv.org/abs/1706.07269"), 1)
        self.assertIn("- GITHUB. About pull request reviews.", novo)
        self.assertEqual(ipp.referencias_com_bloco(novo, self.dados), (novo, 5, 8))
        # o integrador da Pré-Fase 4 corta o arquivo no título do bloco dele: o bloco da Pós-Fase 4 fica inteiro na parte que ele preserva
        self.assertIn(ipp.TITULO_REFS, ip._sem_o_bloco(novo))
        self.assertEqual(ipp.omitidas(REFS, self.dados), ["MILLER, Tim. Explanation in artificial intelligence. Artificial Intelligence, v. 267, 2019. Disponível em: https://arxiv.org/abs/1706.07269. Acesso em: 7 nov. 2026."])

    def teste_linha_do_indice_entra_depois_da_pre_fase_4_e_e_regravavel(self):
        novo = ipp.memorial_com_linha(MEMORIAL, self.dados)
        self.assertEqual(novo.count(ipp.MARCA_DO_INDICE), 1)
        self.assertLess(novo.index(ip.MARCA_DO_INDICE), novo.index(ipp.TAG_DO_INDICE))
        self.assertLess(novo.index(ipp.MARCA_DO_INDICE), novo.index("- [Referências levantadas]"))
        self.assertIn(f"{len(TOPICOS_DE_TESTE)} tópicos", novo)
        self.assertEqual(ipp.memorial_com_linha(novo, self.dados), novo)

    def teste_texto_do_script_sem_travessao_nem_seta(self):
        for l in Path(ipp.__file__).read_text(encoding="utf-8").splitlines():
            self.assertNotIn("—", l, l)
            self.assertNotIn("→", l, l)

    def teste_arquivos_reais_quando_estao_na_maquina(self):
        if not ipp.DADOS.exists():
            self.skipTest("a pasta das leituras não está nesta máquina")
        dados = ipp.carregar()
        self.assertEqual(list(dados), [t[0] for t in ipp.TOPICOS])
        for k, item in dados.items():
            self.assertGreaterEqual(item["n_fontes"], 1, k)
        t = ipp.render(dados)
        self.assertNotIn("—", t)
        self.assertNotIn("→", t)
        if ipp.LEVANTAMENTO.exists():
            self.assertEqual(ipp.check(), 0)


if __name__ == "__main__":
    unittest.main(verbosity=1)
