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
from datetime import datetime, timezone
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
            # ! Alteração de IA - Revisar: o nome em caixa-alta agora aparece 3 vezes (capa, folha de rosto e folha de aprovação).
            # ! Motivo: a folha de aprovação nova repete autores e título, como manda a NBR 14724.
            self.assertEqual(textos.count(autor.upper()), 3, autor)
        self.assertEqual(textos.count("TÍTULO DO TRABALHO DE TESTE:"), 3)
        self.assertIn("Trabalho apresentado ao curso de teste.", textos)
        self.assertIn("Orientador: Prof. Teste", textos)

    def teste_titulos_no_sumario_e_papel_a4(self) -> None:
        self.assertIn("1 INTRODUÇÃO", self.textos())
        self.assertGreaterEqual(self.xml.count('<w:outlineLvl w:val="0"/>'), 6)  # resumo, siglas, sumário, 1, 2, refs, glossário, apêndice
        self.assertIn('<w:outlineLvl w:val="1"/>', self.xml)
        # ! Alteração de IA - Revisar: o documento passou de 2 para 4 seções do Word (capa e rosto / ficha / aprovação até sumário / texto), então a conta de A4 e margens sobe de 2 para 4.
        # ! Motivo: a ficha catalográfica precisa de página própria que não entra na numeração impressa; no Word isso só se faz com seção própria.
        self.assertEqual(self.xml.count('<w:pgSz w:w="11906" w:h="16838"/>'), 4)
        self.assertEqual(self.xml.count('w:top="1701" w:right="1134" w:bottom="1134" w:left="1701"'), 4)
        self.assertIn('<w:updateFields w:val="true"/>', self.settings)
        self.assertIn('TOC \\o "1-3"', self.xml)

    def teste_numeracao_so_da_segunda_secao(self) -> None:
        secoes = re.findall(r"<w:sectPr>.*?</w:sectPr>|<w:sectPr .*?</w:sectPr>", self.xml, re.DOTALL)
        # ! Alteração de IA - Revisar: o teste passa a esperar 4 seções (ver a explicação em teste_titulos_no_sumario_e_papel_a4); o cabeçalho com o número continua só na última, e a capa continua em zero.
        # ! Motivo: a regra "capa não conta e número só na parte textual" não mudou; mudou o número de seções que a cumprem.
        self.assertEqual(len(secoes), 4)
        self.assertIn('<w:pgNumType w:start="0"/>', secoes[0])
        for sec in secoes[:3]:
            self.assertNotIn("headerReference", sec)
        self.assertIn("headerReference", secoes[3])

    def teste_tabela_alineas_e_citacao(self) -> None:
        textos = self.textos()
        self.assertIn(" – Resultado de teste", textos)
        self.assertIn("APÊNDICE A – APÊNDICE DE TESTE", textos)
        self.assertIn("SEQ Tabela", self.xml)
        self.assertEqual(self.doc.tabelas, ["Resultado de teste"])
        self.assertIn("a) primeiro item sem pontuação;", textos)
        self.assertIn("b) segundo item.", textos)
        self.assertIn('<w:ind w:left="2268"/>', self.xml)
        # ! Alteração de IA - Revisar: duas tabelas no corpo (a caixa da ficha catalográfica e a tabela de resultado de teste).
        # ! Motivo: a ficha catalográfica é uma tabela de uma célula, para a caixa ter o tamanho exato de 12,5 x 7,5 cm.
        self.assertEqual(self.xml.count("<w:tbl>"), 2)

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


# ! Alteração de IA - Revisar: testes novos (25/11/2026, decisão 158) da ficha catalográfica, da folha de aprovação, da
# numeração que não conta a ficha e das propriedades do arquivo (autor, título, datas, sem Company/Manager/Template do molde).
# ! Motivo: a entrega do TCC passa a ter folha de aprovação e ficha catalográfica (NBR 14724) e nenhum rastro de IA nas
# propriedades do arquivo; sem teste, uma mudança no gerador poderia contar a ficha como página numerada (a Introdução sairia
# com número errado e o "N f." da ficha ficaria errado) ou soltar o autor "python-docx" do molde de volta no arquivo.
EXTRAS = """- **Grau:** Bacharelado em Ciência da Computação
- **CDD:** 005.1
- **CDU:** 004.4
- **Ficha elaborada por:** Biblioteca de Teste
- **Banca:** Prof. Dr. Fulano de Tal - Instituto Um | Profa. Dra. Beltrana Souza - Instituto Dois
"""


def com_extras() -> str:
    return MARKDOWN.replace("- **Data:** 03/11/2026\n", "- **Data:** 03/11/2026\n" + EXTRAS)


class TesteNomes(unittest.TestCase):
    def teste_inversao_de_nomes_brasileiros(self) -> None:
        casos = {
            "Eric Conde Derre": "Derre, Eric Conde",
            "Guilherme Penha dos Santos": "Santos, Guilherme Penha dos",
            "Erick do Carmo Esteves": "Esteves, Erick do Carmo",
            "Kennedy Fernando de Oliveira Gundim": "Gundim, Kennedy Fernando de Oliveira",
            "João da Silva Filho": "Silva Filho, João da",
            "Pedro Neto": "Neto, Pedro",
            "Carlos Alberto Júnior": "Alberto Júnior, Carlos",
            "Madonna": "Madonna",
        }
        for nome, esperado in casos.items():
            self.assertEqual(g.inverter_nome(nome), esperado, nome)

    def teste_orientador_sem_titulacao(self) -> None:
        self.assertEqual(g.sem_titulacao("Prof. Me. Rafael Oliveira Cotrin"), "Rafael Oliveira Cotrin")
        self.assertEqual(g.sem_titulacao("Profa. Dra. Ana Lima"), "Ana Lima")
        self.assertEqual(g.sem_titulacao("Rafael Cotrin"), "Rafael Cotrin")

    def teste_algarismos_romanos(self) -> None:
        self.assertEqual([g.romano(n) for n in (1, 2, 4, 9, 14)], ["I", "II", "IV", "IX", "XIV"])


class TesteFicha(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        self.pasta = Path(self.tmp.name)
        self.md = self.pasta / "tcc.md"
        self.md.write_text(MARKDOWN, encoding="utf-8")
        self.doc = g.ler_markdown(self.md)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def linhas(self, **kw) -> list[str]:
        return g.linhas_da_ficha(self.doc.dados, g.palavras_chave(self.doc), kw.get("folhas", "12"))

    def teste_entrada_e_titulo_com_mais_de_tres_autores(self) -> None:
        l = self.linhas()
        self.assertEqual(l[0], "Um, Ana")
        self.assertTrue(l[1].startswith("Título do trabalho de teste : subtítulo de teste / Ana Um [et al.]. – São Paulo, 2026."), l[1])
        self.assertEqual(l[2], "12 f. : il.")

    def teste_titulo_com_tres_autores_lista_todos(self) -> None:
        self.doc.dados["Autores"] = "Ana Um | Bia Dois | Caio Três"
        l = self.linhas()
        self.assertIn("/ Ana Um, Bia Dois e Caio Três. – São Paulo, 2026.", l[1])

    def teste_orientador_grau_e_assuntos(self) -> None:
        texto = "\n".join(self.linhas())
        self.assertIn("Orientador: Prof. Teste.", texto)
        self.assertIn("Trabalho de Conclusão de Curso (Graduação) – Universidade de Teste, São Paulo, 2026.", texto)
        self.assertIn("1. Um. 2. Dois. 3. Três.", texto)
        self.assertIn("I. Dois, Bia. II. Três, Caio.", texto)
        self.assertIn("VII. Teste, orient. VIII. Título.", texto)  # orientador sem a titulação "Prof."

    def teste_grau_cdd_cdu_e_quem_elaborou(self) -> None:
        md = self.pasta / "extras.md"
        md.write_text(com_extras(), encoding="utf-8")
        doc = g.ler_markdown(md)
        l = g.linhas_da_ficha(doc.dados, g.palavras_chave(doc), "12")
        self.assertIn("(Bacharelado em Ciência da Computação)", "\n".join(l))
        self.assertEqual(g.cdd_cdu(doc.dados), "CDD 005.1 / CDU 004.4")
        self.assertEqual(g.cdd_cdu(self.doc.dados), "")
        self.assertEqual(g.frase_da_ficha(doc.dados), "Ficha catalográfica elaborada por Biblioteca de Teste.")
        self.assertEqual(g.frase_da_ficha(self.doc.dados), "Ficha catalográfica elaborada pelos autores.")

    def teste_caixa_12_5_por_7_5_cm(self) -> None:
        xml = g.ficha_catalografica(self.doc.dados, g.palavras_chave(self.doc), None)
        self.assertEqual(xml.count("<w:tbl>"), 1)
        self.assertIn('<w:tblW w:w="7087" w:type="dxa"/>', xml)   # 12,5 cm
        self.assertIn('<w:trHeight w:val="4252" w:hRule="exact"/>', xml)   # 7,5 cm
        self.assertIn('<w:jc w:val="center"/>', xml)
        self.assertIn('<w:sz w:val="20"/>', xml)   # corpo 10
        self.assertIn("NUMPAGES", xml)    # sem --folhas, o número vem de campo do Word
        self.assertIn("Ficha catalográfica elaborada pelos autores.", xml)

    def teste_folhas_fixas(self) -> None:
        xml = g.ficha_catalografica(self.doc.dados, g.palavras_chave(self.doc), 87)
        self.assertNotIn("NUMPAGES", xml)
        self.assertIn("87 f. : il.", re.sub(r"<[^>]+>", "", xml))


class TesteElementosPreTextuais(unittest.TestCase):
    def gerar(self, md: str):
        self.tmp = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        self.addCleanup(self.tmp.cleanup)
        pasta = Path(self.tmp.name)
        (pasta / "t.md").write_text(md, encoding="utf-8")
        g.gerar(pasta / "t.md", g.MOLDE, pasta / "t.docx", folhas=None)
        with zipfile.ZipFile(pasta / "t.docx") as z:
            return z.read("word/document.xml").decode("utf-8"), z

    def textos(self, xml: str) -> list[str]:
        return re.findall(r"<w:t[^>]*>([^<]*)</w:t>", xml)

    def teste_ordem_dos_elementos(self) -> None:
        xml, _ = self.gerar(MARKDOWN)
        t = " ".join(self.textos(xml))
        ordem = [t.index("Trabalho apresentado ao curso de teste."), t.index("Ficha catalográfica elaborada pelos autores."),
                 t.index("BANCA EXAMINADORA"), t.index("RESUMO"), t.index("SUMÁRIO"), t.index("1 INTRODUÇÃO")]
        self.assertEqual(ordem, sorted(ordem))

    def teste_aprovacao_sem_banca_tem_orientador_e_dois_examinadores(self) -> None:
        xml, _ = self.gerar(MARKDOWN)
        t = self.textos(xml)
        self.assertIn("Aprovado em: ____/____/________.", t)
        self.assertEqual(t.count("Examinador(a)"), 2)
        self.assertIn("Prof. Teste", t)
        self.assertIn("(Orientador)", t)
        self.assertIn("Universidade de Teste", t)
        self.assertEqual(t.count("ANA UM"), 3)   # capa, folha de rosto e folha de aprovação

    def teste_aprovacao_com_banca(self) -> None:
        xml, _ = self.gerar(com_extras())
        t = self.textos(xml)
        self.assertIn("Prof. Dr. Fulano de Tal", t)
        self.assertIn("Instituto Um", t)
        self.assertIn("Profa. Dra. Beltrana Souza", t)
        self.assertIn("Instituto Dois", t)
        self.assertNotIn("Examinador(a)", t)

    def teste_ficha_nao_conta_na_numeracao(self) -> None:
        xml, _ = self.gerar(MARKDOWN)
        secoes = re.findall(r"<w:sectPr>.*?</w:sectPr>|<w:sectPr .*?</w:sectPr>", xml, re.DOTALL)
        self.assertEqual(len(secoes), 4)
        self.assertIn('<w:pgNumType w:start="0"/>', secoes[0])     # capa = 0, folha de rosto = 1
        self.assertNotIn("pgNumType", secoes[1])                    # a ficha (verso) fica sem número e sem reiniciar
        self.assertIn('<w:pgNumType w:start="2"/>', secoes[2])     # aprovação volta a contar a partir de 2
        self.assertNotIn("pgNumType", secoes[3])                    # texto continua a contagem
        self.assertIn("headerReference", secoes[3])
        for sec in secoes[:3]:
            self.assertNotIn("headerReference", sec)
        # a ficha é a única seção de uma página: o spacer e a tabela ficam entre o 1.º e o 2.º sectPr
        # (a frase da ficha é o último parágrafo da seção: o sectPr vem no pPr dele, logo antes do texto)
        fim0 = xml.index(secoes[0]) + len(secoes[0])
        pos1 = xml.index(secoes[1])
        frase = xml.index("Ficha catalográfica elaborada pelos autores.")
        self.assertGreater(frase, fim0)
        self.assertLess(frase - pos1, 800)
        self.assertGreater(xml.index("BANCA EXAMINADORA"), pos1)


class TesteProps(unittest.TestCase):
    def teste_propriedades_do_arquivo(self) -> None:
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
            pasta = Path(tmp)
            (pasta / "t.md").write_text(MARKDOWN, encoding="utf-8")
            g.gerar(pasta / "t.md", g.MOLDE, pasta / "t.docx")
            with zipfile.ZipFile(pasta / "t.docx") as z:
                core = z.read("docProps/core.xml").decode("utf-8")
                app = z.read("docProps/app.xml").decode("utf-8")
                settings = z.read("word/settings.xml").decode("utf-8")
                self.assertNotIn("docProps/thumbnail.jpeg", z.namelist())
                minidom.parseString(core.encode("utf-8"))
                minidom.parseString(app.encode("utf-8"))
        autores = "; ".join(AUTORES)
        self.assertIn(f"<dc:creator>{autores}</dc:creator>", core)
        self.assertIn(f"<cp:lastModifiedBy>{autores}</cp:lastModifiedBy>", core)
        self.assertIn("<dc:title>Título do trabalho de teste: Subtítulo de teste</dc:title>", core)
        agora = datetime.now(timezone.utc)
        for tag in ("created", "modified"):
            m = re.search(rf'<dcterms:{tag} xsi:type="dcterms:W3CDTF">(\d{{4}})-', core)
            self.assertTrue(m and int(m.group(1)) == agora.year, tag)
        for proibido in ("python-docx", "dc:description", "cp:keywords", "cp:category", "2013"):
            self.assertNotIn(proibido, core)
        self.assertNotIn("savePreviewPicture", settings)
        for proibido in ("<Company", "<Manager", "<Template"):
            self.assertNotIn(proibido, app)
        for texto in (core, app):
            self.assertIsNone(re.search(r"claude|anthropic|chatgpt|openai|copilot|gemini|deepseek|gpt-", texto, re.I))


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    unittest.main(verbosity=1)
