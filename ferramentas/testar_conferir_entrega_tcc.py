#!/usr/bin/env python3
# ! Alteração de IA - Revisar: testes novos (25/11/2026, decisão 158) de `conferir_entrega_tcc.py`: monta .docx mínimos em pasta temporária, um limpo e um para cada defeito (comentário do Word, texto oculto, alteração controlada, autor "Claude" nas propriedades, tag de IA no corpo, tag dentro de um PNG embutido, texto alternativo de imagem citando IA) e confere que cada um é acusado e que o limpo passa; com o PyMuPDF instalado, faz o mesmo com PDFs (limpo, com anotação, com produtor de IA, com a tag no texto); sem o PyMuPDF, testa só o caminho de biblioteca padrão.
# ! Motivo: a decisão 158 manda entregar o TCC (Word e PDF) sem nenhuma marcação de IA, inclusive as ocultas. A conferência é a última barreira antes de o Eric mandar os arquivos; se ela deixasse passar um comentário do Word ou um autor "Claude" nas propriedades, ninguém perceberia (o texto visível está limpo), e se acusasse o que é normal (o `w:webHidden` do sumário, a citação do Claude Code na seção 5.8) a entrega travaria sem motivo.
# Uso: python ferramentas/testar_conferir_entrega_tcc.py   (sem -I, para o PyMuPDF do usuário ser achado; com -I os testes de PDF com PyMuPDF são pulados)
"""Testes de conferir_entrega_tcc.py."""
from __future__ import annotations

import json
import struct
import sys
import tempfile
import unittest
import zipfile
import zlib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import conferir_entrega_tcc as c

try:
    import fitz  # type: ignore
except ImportError:  # pragma: no cover
    fitz = None

NS = ('xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
      'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
      'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
      'xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture" '
      'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"')
CORPO_LIMPO = ('<w:p><w:r><w:t>O agente de apoio (Claude Code) ajudou a escrever o código, como declara a seção 5.8.</w:t></w:r></w:p>'
               '<w:p><w:r><w:rPr><w:webHidden/></w:rPr><w:t>Sumário 1</w:t></w:r></w:p>')


def core(autor: str = "Eric Conde Derre; Ana Um", ultimo: str | None = None, extra: str = "") -> str:
    return ("<?xml version='1.0' encoding='UTF-8' standalone='yes'?>"
            '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" '
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
            f"<dc:title>Título</dc:title><dc:creator>{autor}</dc:creator>"
            f"<cp:lastModifiedBy>{ultimo or autor}</cp:lastModifiedBy>{extra}</cp:coreProperties>")


def png(texto_chunk: bytes | None = None) -> bytes:
    def chunk(tipo: bytes, dados: bytes) -> bytes:
        return struct.pack(">I", len(dados)) + tipo + dados + struct.pack(">I", zlib.crc32(tipo + dados) & 0xFFFFFFFF)
    cabecalho = struct.pack(">IIBBBBB", 1, 1, 8, 2, 0, 0, 0)
    dados = zlib.compress(b"\x00\xff\x00\x00")
    saida = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", cabecalho)
    if texto_chunk is not None:
        saida += chunk(b"tEXt", texto_chunk)
    return saida + chunk(b"IDAT", dados) + chunk(b"IEND", b"")


def docx(caminho: Path, *, corpo: str = CORPO_LIMPO, core_xml: str | None = None, extras: dict[str, bytes] | None = None,
         app: str = "<Properties><Application>Microsoft Office Word</Application></Properties>") -> Path:
    partes = {
        "[Content_Types].xml": '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"/>',
        "_rels/.rels": '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"/>',
        "word/document.xml": f'<?xml version="1.0"?><w:document {NS}><w:body>{corpo}</w:body></w:document>',
        "word/settings.xml": f'<w:settings {NS}><w:updateFields w:val="true"/></w:settings>',
        "docProps/core.xml": core_xml or core(),
        "docProps/app.xml": app,
    }
    # um comentário XML legítimo (do próprio arquivo, fora de w:t) não pode ser acusado
    partes["word/styles.xml"] = f'<w:styles {NS}><!-- estilos --><w:style w:styleId="N"/></w:styles>'
    partes.update({k: (v if isinstance(v, bytes) else v.encode("utf-8")) for k, v in (extras or {}).items()})
    with zipfile.ZipFile(caminho, "w", zipfile.ZIP_DEFLATED) as z:
        for nome, dados in partes.items():
            z.writestr(nome, dados if isinstance(dados, bytes) else dados.encode("utf-8"))
    return caminho


class TesteDocx(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        self.pasta = Path(self.tmp.name)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def falhas(self, caminho: Path) -> list[str]:
        resultados, _info = c.conferir_docx(caminho)
        return [nome for nome, estado, _onde in resultados if estado == "FALHA"]

    def teste_docx_limpo_passa(self) -> None:
        arq = docx(self.pasta / "limpo.docx")
        resultados, info = c.conferir_docx(arq)
        self.assertEqual([r for r in resultados if r[1] == "FALHA"], [])
        self.assertTrue(all(r[1] in ("OK", "AVISO") for r in resultados))
        self.assertEqual(info["Autor (dc:creator)"], "Eric Conde Derre; Ana Um")
        self.assertIn("Último a salvar (cp:lastModifiedBy)", info)
        self.assertIn("Programa (Application)", info)

    def teste_comentario_do_word(self) -> None:
        arq = docx(self.pasta / "a.docx", extras={"word/comments.xml": f'<w:comments {NS}><w:comment w:id="0"/></w:comments>'},
                   corpo='<w:p><w:commentRangeStart w:id="0"/><w:r><w:t>x</w:t></w:r><w:commentRangeEnd w:id="0"/>'
                         '<w:r><w:commentReference w:id="0"/></w:r></w:p>')
        self.assertTrue(any("coment" in f.lower() for f in self.falhas(arq)), self.falhas(arq))

    def teste_texto_oculto(self) -> None:
        arq = docx(self.pasta / "b.docx", corpo='<w:p><w:r><w:rPr><w:vanish/></w:rPr><w:t>escondido</w:t></w:r></w:p>')
        self.assertTrue(any("oculto" in f.lower() for f in self.falhas(arq)), self.falhas(arq))
        arq2 = docx(self.pasta / "b2.docx", corpo='<w:p><w:pPr><w:rPr><w:specVanish/></w:rPr></w:pPr></w:p>')
        self.assertTrue(any("oculto" in f.lower() for f in self.falhas(arq2)))

    def teste_vanish_desligado_nao_conta(self) -> None:
        arq = docx(self.pasta / "b3.docx", corpo='<w:p><w:r><w:rPr><w:vanish w:val="0"/></w:rPr><w:t>visivel</w:t></w:r></w:p>')
        self.assertEqual(self.falhas(arq), [])

    def teste_alteracao_controlada(self) -> None:
        for tag, nome in (("ins", "c1"), ("del", "c2"), ("moveFrom", "c3"), ("moveTo", "c4")):
            arq = docx(self.pasta / f"{nome}.docx",
                       corpo=f'<w:p><w:{tag} w:id="1" w:author="X"><w:r><w:t>x</w:t></w:r></w:{tag}></w:p>')
            self.assertTrue(any("controlada" in f.lower() for f in self.falhas(arq)), tag)

    def teste_autor_de_ia_nas_propriedades(self) -> None:
        for nome, xml in (("d1", core(autor="Claude")), ("d2", core(ultimo="Anthropic Claude Code")),
                          ("d3", core(extra="<dc:description>feito com ChatGPT</dc:description>"))):
            arq = docx(self.pasta / f"{nome}.docx", core_xml=xml)
            self.assertTrue(any("propriedades" in f.lower() for f in self.falhas(arq)), nome)
        arq = docx(self.pasta / "d4.docx", app="<Properties><Company>OpenAI</Company></Properties>")
        self.assertTrue(any("propriedades" in f.lower() for f in self.falhas(arq)))

    def teste_tag_no_corpo(self) -> None:
        for texto in ("! Alteração de IA - Revisar: x", "! Alteracao de IA - Revisar", "! Motivo: porque sim", "texto &lt;!-- resto --&gt;"):
            arq = docx(self.pasta / "e.docx", corpo=f"<w:p><w:r><w:t>{texto}</w:t></w:r></w:p>")
            self.assertTrue(any("tag" in f.lower() or "marc" in f.lower() for f in self.falhas(arq)), texto)

    def teste_comentario_xml_legitimo_nao_acusa(self) -> None:
        # o docx de teste tem <!-- estilos --> em word/styles.xml: não é marcação vinda do Markdown
        self.assertEqual(self.falhas(docx(self.pasta / "f.docx")), [])

    def teste_tag_em_outra_parte(self) -> None:
        arq = docx(self.pasta / "g.docx", extras={"word/header1.xml": f"<w:hdr {NS}>! Alteração de IA - Revisar</w:hdr>"})
        self.assertTrue(self.falhas(arq))

    def teste_texto_alternativo_e_nome_de_imagem(self) -> None:
        corpo = ('<w:p><w:r><w:drawing><wp:inline><wp:docPr id="1" name="Figura 1" descr="gerada pelo Claude"/>'
                 '<a:graphic><a:graphicData><pic:pic><pic:nvPicPr><pic:cNvPr id="1" name="chatgpt.png"/></pic:nvPicPr>'
                 '</pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r></w:p>')
        arq = docx(self.pasta / "h.docx", corpo=corpo)
        self.assertTrue(any("imagens" in f.lower() for f in self.falhas(arq)), self.falhas(arq))

    def teste_png_com_texto_de_ia(self) -> None:
        arq = docx(self.pasta / "i.docx", extras={"word/media/fig.png": png(b"Software\x00Claude Code")})
        self.assertTrue(any("png" in f.lower() for f in self.falhas(arq)), self.falhas(arq))
        limpo = docx(self.pasta / "i2.docx", extras={"word/media/fig.png": png(b"Software\x00matplotlib")})
        self.assertEqual(self.falhas(limpo), [])

    def teste_docvars_e_customxml(self) -> None:
        arq = docx(self.pasta / "j.docx", extras={"customXml/item1.xml": "<x>escrito por Anthropic</x>"})
        self.assertTrue(any("customxml" in f.lower() for f in self.falhas(arq)), self.falhas(arq))
        settings = f'<w:settings {NS}><w:docVars><w:docVar w:name="ia" w:val="gemini"/></w:docVars></w:settings>'
        arq2 = docx(self.pasta / "j2.docx", extras={"word/settings.xml": settings})
        self.assertTrue(any("docvars" in f.lower() or "variáveis" in f.lower() for f in self.falhas(arq2)), self.falhas(arq2))

    def teste_molde_com_caminho_de_usuario_so_avisa(self) -> None:
        settings = f'<w:settings {NS}><w:attachedTemplate r:id="rId1"/></w:settings>'
        rels = ('<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" '
                'Type="x" Target="file:///C:/Users/Fulano/AppData/Normal.dotm" TargetMode="External"/></Relationships>')
        arq = docx(self.pasta / "k.docx", extras={"word/settings.xml": settings, "word/_rels/settings.xml.rels": rels})
        resultados, _ = c.conferir_docx(arq)
        self.assertEqual([r for r in resultados if r[1] == "FALHA"], [])
        self.assertTrue(any(r[1] == "AVISO" and "template" in r[0].lower() for r in resultados), resultados)


class TesteLinhaDeComando(unittest.TestCase):
    def teste_codigo_de_saida_e_json(self) -> None:
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
            pasta = Path(tmp)
            limpo = docx(pasta / "limpo.docx")
            sujo = docx(pasta / "sujo.docx", core_xml=core(autor="Claude"))
            pdf_falso = pasta / "x.pdf"
            pdf_falso.write_bytes(b"%PDF-1.4\n1 0 obj<</Title (Titulo) /Author (Autores)>>endobj\n%%EOF\n")
            saida_json = pasta / "r.json"
            self.assertEqual(c.main([str(limpo), str(pdf_falso), "--json", str(saida_json)]), 0)
            self.assertTrue(saida_json.is_file())
            # ! Alteração de IA - Revisar: (26/11/2026, versão 5 do documento do TCC) o registro em JSON tem de sair com a tag e o motivo,
            # nas chaves `_tag` e `_motivo`, como os outros registros de `5-metodo-e-ferramental/dados/`, e continuar dizendo se está limpo.
            # ! Motivo: na geração da versão 5, o `conferir_docs.py` acusou o registro da conferência "sem tag de IA": a ferramenta
            # gravava o JSON sem as duas chaves, e todo arquivo criado com apoio de IA no repositório leva a marcação.
            registro = json.loads(saida_json.read_text(encoding="utf-8"))
            self.assertTrue(registro["_tag"].startswith("! Alteração de IA - Revisar:"), registro.get("_tag"))
            self.assertTrue(registro["_motivo"].startswith("! Motivo:"), registro.get("_motivo"))
            self.assertIs(registro["limpo"], True)
            self.assertEqual(list(registro)[:2], ["_tag", "_motivo"])
            self.assertEqual(c.main([str(sujo), str(pdf_falso)]), 1)


class TestePdfBiblioteca(unittest.TestCase):
    """Caminho sem PyMuPDF (só biblioteca padrão): metadados e busca bruta."""

    def teste_metadados_de_ia_no_pdf_bruto(self) -> None:
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
            ruim = Path(tmp) / "r.pdf"
            ruim.write_bytes(b"%PDF-1.4\n1 0 obj<</Producer (Claude) /Author (Autores)>>endobj\n%%EOF\n")
            resultados, _ = c.conferir_pdf(ruim, usar_fitz=False)
            self.assertTrue(any(r[1] == "FALHA" for r in resultados))
            bom = Path(tmp) / "b.pdf"
            bom.write_bytes(b"%PDF-1.4\n1 0 obj<</Producer (Microsoft Word) /Author (Autores)>>endobj\n%%EOF\n")
            resultados, _ = c.conferir_pdf(bom, usar_fitz=False)
            self.assertEqual([r for r in resultados if r[1] == "FALHA"], [])
            self.assertTrue(any(r[1] == "AVISO" for r in resultados))   # diz o que não conferiu

    # ! Alteração de IA - Revisar: (26/11/2026, versão 5 do documento do TCC) dois testes novos do caminho sem PyMuPDF: o título e o autor
    # lidos do dicionário de informações do PDF, e não do primeiro `/Title` do arquivo, e o texto em UTF-16 com parênteses escapados
    # decodificado inteiro.
    # ! Motivo: na versão 5, a conferência sem o PyMuPDF mostrou o título com o trecho "(E2E)" embaralhado, porque os parênteses vêm
    # escapados dentro do texto em UTF-16 e a leitura não desfazia o escape; e um leitor que pega o primeiro `/Title` do arquivo lê
    # o título do primeiro marcador ("AGRADECIMENTOS") no lugar do título do documento, que foi o que a sessão principal viu com o
    # script dela. Um trecho embaralhado nos metadados também podia esconder uma marca de IA dessa conferência.
    def teste_titulo_e_autor_saem_do_dicionario_de_informacoes_e_nao_do_primeiro_marcador(self) -> None:
        titulo = "Agente de QA (E2E) autônomo"
        autor = "João da Silva; Maria (Souza)"

        def literal_utf16(texto: str) -> bytes:
            cru = b"\xfe\xff" + texto.encode("utf-16-be")
            return b"(" + cru.replace(b"\\", b"\\\\").replace(b"(", b"\\(").replace(b")", b"\\)") + b")"

        dados = (b"%PDF-1.7\n1 0 obj<</Type /Outlines /First 2 0 R>>endobj\n"
                 b"2 0 obj<</Title (AGRADECIMENTOS) /Parent 1 0 R>>endobj\n"
                 b"5 0 obj<</Title " + literal_utf16(titulo) + b" /Author " + literal_utf16(autor) + b" /Producer (Microsoft Word)>>endobj\n"
                 b"trailer<</Root 9 0 R /Info 5 0 R>>\n%%EOF\n")
        meta = c._metadados_brutos(dados)
        self.assertEqual(meta["Title"], titulo)
        self.assertEqual(meta["Author"], autor)

    def teste_marca_de_ia_depois_de_parentese_escapado_e_achada(self) -> None:
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
            # um parêntese só: sem desfazer o escape, tudo o que vem depois dele sai desalinhado, inclusive a marca
            cru = b"\xfe\xff" + "Documento (gerado por Claude".encode("utf-16-be")
            literal = b"(" + cru.replace(b"\\", b"\\\\").replace(b"(", b"\\(").replace(b")", b"\\)") + b")"
            ruim = Path(tmp) / "r.pdf"
            ruim.write_bytes(b"%PDF-1.7\n5 0 obj<</Title " + literal + b" /Author (Autores)>>endobj\ntrailer<</Info 5 0 R>>\n%%EOF\n")
            resultados, _ = c.conferir_pdf(ruim, usar_fitz=False)
            self.assertTrue(any(r[1] == "FALHA" for r in resultados), resultados)


@unittest.skipIf(fitz is None, "PyMuPDF não instalado: testes de PDF pulados")
class TestePdfComFitz(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        self.pasta = Path(self.tmp.name)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def pdf(self, nome: str, *, produtor: str = "Microsoft Word", texto: str = "Texto normal do TCC", anotar: bool = False,
            invisivel: bool = False) -> Path:
        d = fitz.open()
        pagina = d.new_page()
        pagina.insert_text((72, 72), texto)
        if invisivel:
            pagina.insert_text((72, 120), "texto escondido", render_mode=3)
        if anotar:
            pagina.add_text_annot((100, 100), "comentário")
        d.set_metadata({"author": "Eric Conde Derre", "producer": produtor, "creator": "Microsoft Word", "title": "TCC"})
        caminho = self.pasta / nome
        d.save(caminho)
        d.close()
        return caminho

    def falhas(self, caminho: Path) -> list[str]:
        resultados, _ = c.conferir_pdf(caminho)
        return [n for n, e, _o in resultados if e == "FALHA"]

    def teste_pdf_limpo(self) -> None:
        self.assertEqual(self.falhas(self.pdf("a.pdf")), [])

    def teste_produtor_de_ia(self) -> None:
        self.assertTrue(any("metadados" in f.lower() for f in self.falhas(self.pdf("b.pdf", produtor="Claude"))))

    def teste_anotacao(self) -> None:
        self.assertTrue(any("anota" in f.lower() for f in self.falhas(self.pdf("c.pdf", anotar=True))))

    def teste_tag_no_texto(self) -> None:
        self.assertTrue(any("tag" in f.lower() or "marc" in f.lower()
                            for f in self.falhas(self.pdf("d.pdf", texto="! Alteração de IA - Revisar: x"))))

    def teste_texto_invisivel(self) -> None:
        self.assertTrue(any("invis" in f.lower() for f in self.falhas(self.pdf("e.pdf", invisivel=True))))

    def teste_arquivo_embutido(self) -> None:
        caminho = self.pdf("f.pdf")
        d = fitz.open(caminho)
        d.embfile_add("x.txt", b"conteudo")
        d.save(self.pasta / "f2.pdf")
        d.close()
        self.assertTrue(any("embutido" in f.lower() for f in self.falhas(self.pasta / "f2.pdf")))


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    unittest.main(verbosity=1)
