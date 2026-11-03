#!/usr/bin/env python3
# ! Alteração de IA - Revisar: testes de gerar_tcc_docx.py (03/11/2026): um Markdown mínimo com o bloco Dados, resumo,
# siglas, três seções numeradas (com alíneas, citação longa e uma tabela com fonte), referências, glossário e apêndice é
# gerado sobre o molde do orientador em pasta temporária; os testes conferem que o .docx é um zip válido com XML bem
# formado, que o corpo tem os sete autores na capa e na folha de rosto, os títulos com nível de estrutura (outlineLvl)
# para o sumário, a tabela com o título "Tabela 1", a quebra de seção com numeração a partir de zero (a capa não conta)
# e o cabeçalho com o número da página só na segunda seção, o papel A4 com margens de 3 e 2 cm, `updateFields` nas
# configurações, as alíneas com `;` e `.` completados, os comentários HTML fora do Word, e que o Markdown sem o bloco
# Dados ou com título sem número é recusado.
# ! Motivo: o .docx é o que o grupo e o orientador leem; sem os testes, uma mudança no gerador poderia soltar um arquivo
# que o Word não abre, perder autores na capa, numerar a capa ou tirar os títulos do sumário sem ninguém perceber.
# Uso: python ferramentas/testar_gerar_tcc_docx.py
"""Testes de gerar_tcc_docx.py: python ferramentas/testar_gerar_tcc_docx.py"""
from __future__ import annotations

import re
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from xml.dom import minidom

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gerar_tcc_docx as g

AUTORES = ["Ana Um", "Bia Dois", "Caio Três", "Dora Quatro", "Edu Cinco", "Fábio Seis", "Gil Sete"]
MARKDOWN = f"""<!-- comentário que não vai para o Word: SEGREDO -->
## Dados

- **Universidade:** Universidade de Teste
- **Curso:** Curso de Teste
- **Autores:** {' | '.join(AUTORES)}
- **Título:** Título do trabalho de teste
- **Subtítulo:** Subtítulo de teste
- **Natureza:** Trabalho apresentado ao curso de teste.
- **Orientador:** Orientador: Prof. Teste
- **Local:** São Paulo
- **Ano:** 2026
- **Versão:** 1
- **Data:** 03/11/2026

# RESUMO

Primeira frase do resumo. Segunda frase do resumo.

Palavras-chave: um; dois; três.

# LISTA DE ABREVIATURAS E SIGLAS

- **API** interface de programação
- **E2E** de ponta a ponta

# 1 INTRODUÇÃO

Parágrafo de abertura com **negrito** e *itálico*.

## 1.1 Objetivos

- primeiro item sem pontuação
- segundo item

> Citação longa com mais de três linhas, recuada.

# 2 RESULTADOS

Tabela: Resultado de teste
| Modelo | Acerto |
|---|---|
| a | 1 |
| b | 2 |
Fonte: tabela de teste.

Texto depois da tabela.

# REFERÊNCIAS

SOBRENOME, A. Título. Local: Editora, 2025.

OUTRO, B. Segundo título. Revista, 2024.

# GLOSSÁRIO

**Termo:** definição do termo.

# APÊNDICE A - Apêndice de teste

Texto do apêndice.
"""


class Base(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        self.pasta = Path(self.tmp.name)
        self.entrada = self.pasta / "tcc.md"
        self.entrada.write_text(MARKDOWN, encoding="utf-8")
        self.saida = self.pasta / "tcc.docx"
        self.doc = g.gerar(self.entrada, g.MOLDE, self.saida)
        with zipfile.ZipFile(self.saida) as z:
            self.xml = z.read("word/document.xml").decode("utf-8")
            self.settings = z.read("word/settings.xml").decode("utf-8")
            self.nomes = z.namelist()

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def textos(self) -> list[str]:
        return re.findall(r"<w:t[^>]*>([^<]*)</w:t>", self.xml)


class TesteGeracao(Base):
    def teste_zip_e_xml_validos(self) -> None:
        minidom.parseString(self.xml.encode("utf-8"))
        self.assertIn("word/styles.xml", self.nomes)
        self.assertIn("word/header1.xml", self.nomes)
        self.assertEqual(self.saida.name, "tcc.docx")
        self.assertEqual(g.nome_de_saida(self.doc), "TCC_v1_20261103.docx")

    def teste_capa_e_folha_de_rosto_com_os_sete_autores(self) -> None:
        textos = self.textos()
        for autor in AUTORES:
            self.assertEqual(textos.count(autor.upper()), 2, autor)
        self.assertEqual(textos.count("TÍTULO DO TRABALHO DE TESTE:"), 2)
        self.assertIn("Trabalho apresentado ao curso de teste.", textos)
        self.assertIn("Orientador: Prof. Teste", textos)

    def teste_titulos_no_sumario_e_papel_a4(self) -> None:
        self.assertIn("1 INTRODUÇÃO", self.textos())
        self.assertGreaterEqual(self.xml.count('<w:outlineLvl w:val="0"/>'), 6)  # resumo, siglas, sumário, 1, 2, refs, glossário, apêndice
        self.assertIn('<w:outlineLvl w:val="1"/>', self.xml)
        self.assertEqual(self.xml.count('<w:pgSz w:w="11906" w:h="16838"/>'), 2)
        self.assertEqual(self.xml.count('w:top="1701" w:right="1134" w:bottom="1134" w:left="1701"'), 2)
        self.assertIn('<w:updateFields w:val="true"/>', self.settings)
        self.assertIn('TOC \\o "1-3"', self.xml)

    def teste_numeracao_so_da_segunda_secao(self) -> None:
        secoes = re.findall(r"<w:sectPr>.*?</w:sectPr>|<w:sectPr .*?</w:sectPr>", self.xml, re.DOTALL)
        self.assertEqual(len(secoes), 2)
        self.assertIn('<w:pgNumType w:start="0"/>', secoes[0])
        self.assertNotIn("headerReference", secoes[0])
        self.assertIn("headerReference", secoes[1])

    def teste_tabela_alineas_e_citacao(self) -> None:
        textos = self.textos()
        self.assertIn(" – Resultado de teste", textos)
        self.assertIn("APÊNDICE A – APÊNDICE DE TESTE", textos)
        self.assertIn("SEQ Tabela", self.xml)
        self.assertEqual(self.doc.tabelas, ["Resultado de teste"])
        self.assertIn("a) primeiro item sem pontuação;", textos)
        self.assertIn("b) segundo item.", textos)
        self.assertIn('<w:ind w:left="2268"/>', self.xml)
        self.assertEqual(self.xml.count("<w:tbl>"), 1)

    def teste_comentarios_nao_vao_para_o_word(self) -> None:
        self.assertNotIn("SEGREDO", self.xml)
        self.assertNotIn("<!--", self.xml.split("<w:body>")[1])
        self.assertEqual(g.tirar_comentarios("fim da frase <!-- fonte: x -->. Outra <!-- y -->, e (dois <!-- z -->)."),
                         "fim da frase. Outra, e (dois).")

    def teste_resumo_em_paragrafo_unico_e_siglas(self) -> None:
        self.assertIn("Primeira frase do resumo. Segunda frase do resumo.", self.textos())
        self.assertIn("Palavras-chave: um; dois; três.", "".join(self.textos()))
        self.assertIn("API", self.textos())


class TesteRecusas(unittest.TestCase):
    def teste_sem_bloco_dados(self) -> None:
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
            p = Path(tmp) / "x.md"
            p.write_text("# 1 INTRODUÇÃO\n\nTexto.\n", encoding="utf-8")
            with self.assertRaises(g.ErroDeEntrada):
                g.ler_markdown(p)

    def teste_titulo_sem_numero(self) -> None:
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
            p = Path(tmp) / "x.md"
            p.write_text(MARKDOWN.replace("# 2 RESULTADOS", "# RESULTADOS SEM NÚMERO"), encoding="utf-8")
            with self.assertRaises(g.ErroDeEntrada):
                g.ler_markdown(p)


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    unittest.main(verbosity=1)
