#!/usr/bin/env python3
# ! Alteração de IA - Revisar: testes da página de curadoria das leituras (10/11/2026, Pós-Fase 4): a página mostra uma leitura por vez com o texto
# num campo editável, o verbete original ao lado e o que os filtros do pacote Q2 acusam; as respostas gravadas no banco da página (aprovada, editada
# ou adiada) são aplicadas aos arquivos de `biblioteca_producao_leitura/` com `curado: sim`, sem quebrar o `--check` de biblioteca_leitura.py e sem
# regravar uma leitura já curada.
# ! Motivo: a curadoria das 39 leituras é do Eric, e ele pediu uma página para fazê-la (como a da sessão de revisão); o que a página grava tem de
# chegar aos arquivos exatamente como ele deixou, e uma leitura curada nunca pode ser regravada por engano.
"""Uso: python ferramentas/testar_curadoria_leituras.py"""
from __future__ import annotations

import json
import re
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import curadoria_leituras as cl

RAIZ = Path(__file__).resolve().parent.parent
BIB = RAIZ / "Programacao" / "AgenteCore" / "biblioteca_producao"
VERBETES_DE_TESTE = ("erros/corpo_vazio.md", "contratos/contrato-produto.md")


class TesteDaCuradoria(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.raiz = Path(self._tmp.name)
        self.bib = self.raiz / "biblioteca_producao"
        self.leitura = self.raiz / "biblioteca_producao_leitura"
        for rel in VERBETES_DE_TESTE:
            destino = self.bib / rel
            destino.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(BIB / rel, destino)
        cl.bl.gerar(self.bib, self.leitura, gerado_em="2026-11-07")

    def tearDown(self):
        self._tmp.cleanup()

    def teste_separar_devolve_cabecalho_e_corpo_que_recompoem_o_arquivo(self):
        texto = (self.leitura / "erros" / "corpo_vazio.md").read_text(encoding="utf-8")
        cab, corpo = cl.separar(texto)
        self.assertEqual(cab + corpo, texto)
        self.assertTrue(cab.startswith("---\n") and cab.rstrip("\n").endswith("---"))
        self.assertIn("\ncurado: nao\n", cab)
        self.assertTrue(corpo.startswith(("\n# Corpo vazio", "# Corpo vazio")), corpo[:40])
        with self.assertRaises(ValueError):
            cl.separar("sem cabeçalho")

    def teste_itens_trazem_corpo_verbete_e_o_que_os_filtros_acusam(self):
        itens = cl.itens(self.bib, self.leitura)
        self.assertEqual([x["id"] for x in itens], ["contrato-produto", "corpo_vazio"])
        por_id = {x["id"]: x for x in itens}
        cv = por_id["corpo_vazio"]
        texto = (self.leitura / "erros" / "corpo_vazio.md").read_text(encoding="utf-8")
        self.assertEqual(cv["corpo"], cl.separar(texto)[1])
        self.assertEqual(cv["caminho"], "erros/corpo_vazio.md")
        self.assertEqual(cv["titulo"], "Corpo vazio")
        self.assertFalse(cv["curado"])
        self.assertEqual(cv["corpo_sha"], cl.ft.sha16(cv["corpo"]))
        self.assertIn("## Resumo", cv["verbete_corpo"])
        self.assertNotIn("---\nid:", cv["verbete_corpo"])
        f = cv["filtros"]
        self.assertIn("aprovado", f)
        self.assertIsInstance(f["falhas"], list)
        self.assertIsInstance(f["termos_sem_expansao"], list)
        for ch in ("palavras_por_frase_media", "palavras_por_frase_max", "termos_sem_expansao_n", "repeticao_razao"):
            self.assertIn(ch, f["medidas"])
            self.assertIn(ch, f["limiares"])
        cp = por_id["contrato-produto"]
        self.assertFalse(cp["filtros"]["aprovado"], "a leitura de contrato-produto reprova nos filtros de 07/11 (termos sem explicação)")
        self.assertTrue(cp["filtros"]["termos_sem_expansao"])
        self.assertIn("termos_sem_expansao_n", cp["filtros"]["falhas"])

    def teste_pagina_tem_um_item_por_leitura_com_o_texto_e_o_verbete_e_grava_na_colecao_curadoria(self):
        itens = cl.itens(self.bib, self.leitura)
        pagina = cl.pagina(itens)
        dados = json.loads(re.search(r'<script type="application/json" id="itens">(.*?)</script>', pagina, re.DOTALL).group(1))
        self.assertEqual([x["id"] for x in dados], ["contrato-produto", "corpo_vazio"])
        self.assertEqual(dados[1]["corpo"], itens[1]["corpo"])
        self.assertEqual(dados[1]["corpo_sha"], itens[1]["corpo_sha"])
        self.assertIn("falhas", dados[0]["filtros"])
        self.assertNotIn("verbete_corpo", dados[0], "o verbete vai como HTML num template, não no JSON")
        for i in range(2):
            self.assertRegex(pagina, rf'<template id="verb-{i}">')
            self.assertRegex(pagina, rf'<template id="prev-{i}">')
        self.assertIn("<title>Curadoria das leituras dos verbetes</title>", pagina)
        self.assertIn('collection("curadoria")', pagina)
        self.assertIn("2 leituras", pagina)
        self.assertNotIn("@@", pagina)
        propria = re.sub(r"<template.*?</template>", "", pagina, flags=re.DOTALL)   # o verbete original traz travessões escritos pelo modelo; o texto da página, não
        self.assertNotIn("—", propria)
        self.assertNotIn("→", propria)

    def teste_aplicar_grava_curado_sim_o_texto_editado_e_a_nota_e_recusa_repetida_adiada_ou_desatualizada(self):
        itens = {x["id"]: x for x in cl.itens(self.bib, self.leitura)}
        novo = itens["contrato-produto"]["corpo"].replace("## O que é", "## O que é\n\nFrase nova do Eric.", 1)
        respostas = [{"id": "corpo_vazio", "estado": "aprovada", "corpo_sha": itens["corpo_vazio"]["corpo_sha"]},
                     {"id": "contrato-produto", "estado": "editada", "texto": novo, "corpo_sha": itens["contrato-produto"]["corpo_sha"]}]
        r = cl.aplicar(respostas, self.leitura, self.bib, hoje="2026-11-10")
        self.assertEqual((r["aprovadas"], r["editadas"], r["adiadas"], r["erros"]), (1, 1, 0, []))
        cv = (self.leitura / "erros" / "corpo_vazio.md").read_text(encoding="utf-8")
        cab, corpo = cl.separar(cv)
        self.assertIn("\ncurado: sim\n", cab)
        self.assertNotIn("curado: nao", cab)
        self.assertNotIn(cl.bl.TEXTO_DA_CURADORIA, corpo)
        self.assertIn("Curada em 10/11/2026 pelo Eric na página da curadoria: aprovada como estava.", corpo)
        self.assertEqual(corpo.split("## Curadoria")[0], itens["corpo_vazio"]["corpo"].split("## Curadoria")[0], "antes da seção Curadoria nada muda numa leitura aprovada")
        cp = (self.leitura / "contratos" / "contrato-produto.md").read_text(encoding="utf-8")
        cab2, corpo2 = cl.separar(cp)
        self.assertIn("\ncurado: sim\n", cab2)
        self.assertIn("Frase nova do Eric.", corpo2)
        self.assertIn("Curada em 10/11/2026 pelo Eric na página da curadoria: texto revisado.", corpo2)
        self.assertEqual(cl.bl.conferir(self.bib, self.leitura), [])
        g = cl.bl.gerar(self.bib, self.leitura, gerado_em="2026-11-30")
        self.assertEqual(sorted(g["mantidos"]), ["contrato-produto", "corpo_vazio"])
        self.assertIn("Frase nova do Eric.", (self.leitura / "contratos" / "contrato-produto.md").read_text(encoding="utf-8"))
        self.assertEqual([x["id"] for x in r["itens"]], ["corpo_vazio", "contrato-produto"])
        self.assertIn("filtros", r["itens"][1])
        r2 = cl.aplicar(respostas, self.leitura, self.bib, hoje="2026-11-10")
        self.assertEqual((r2["aprovadas"], r2["editadas"]), (0, 0))
        self.assertEqual(len(r2["erros"]), 2)
        self.assertTrue(all("já curada" in e for e in r2["erros"]), r2["erros"])
        r3 = cl.aplicar([{"id": "corpo_vazio", "estado": "adiada"}], self.leitura, self.bib, hoje="2026-11-10")
        self.assertEqual((r3["adiadas"], r3["erros"]), (1, []))
        r4 = cl.aplicar([{"id": "corpo_vazio", "estado": "editada", "texto": "x", "corpo_sha": "0000000000000000"}], self.leitura, self.bib, hoje="2026-11-10", corrigir=True)
        self.assertEqual(len(r4["erros"]), 1)
        self.assertIn("mudou", r4["erros"][0])
        r5 = cl.aplicar([{"id": "nao-existe", "estado": "aprovada", "corpo_sha": "x"}], self.leitura, self.bib, hoje="2026-11-10")
        self.assertEqual(len(r5["erros"]), 1)

    # ! Alteração de IA - Revisar: (10/11/2026) testes do aplicador com consertos e com quem curou: cada conserto troca um trecho que ocorre uma vez só no texto
    # salvo na página, o cabeçalho ganha a tag com o motivo de cada troca, a nota da seção Curadoria diz quem curou e quantos consertos houve, e um conserto
    # que não acha o trecho deixa o arquivo como estava; `render_consertos` lista cada troca com o antes e o depois.
    # ! Motivo: na curadoria de 10/11/2026 o texto de 26 leituras foi escrito por um analista e colado pelo Eric; ele trazia frases erradas sobre o projeto
    # (busca vetorial, épocas de treinamento), uma linha colada e termos ainda sem explicação, e o Eric escolheu no quadro aplicar a curadoria com esses
    # consertos; cada troca precisa ficar registrada, com o motivo, no arquivo e numa lista conferível.
    def teste_aplicar_com_consertos_troca_o_trecho_marca_o_cabecalho_e_anota_quem_curou(self):
        itens = {x["id"]: x for x in cl.itens(self.bib, self.leitura)}
        salvo = itens["contrato-produto"]["corpo"].replace("## O que é", "## O que é\n\nFrase errada do analista.", 1)
        respostas = [{"id": "contrato-produto", "estado": "editada", "texto": salvo, "corpo_sha": itens["contrato-produto"]["corpo_sha"]},
                     {"id": "corpo_vazio", "estado": "aprovada", "corpo_sha": itens["corpo_vazio"]["corpo_sha"]}]
        consertos = {"contrato-produto": [{"antigo": "Frase errada do analista.", "novo": "Frase consertada.", "motivo": "a frase dizia que a busca é vetorial, e a busca deste projeto é por palavras"}]}
        quem = "por um analista, com o Eric passando a leitura e colando a resposta,"
        r = cl.aplicar(respostas, self.leitura, self.bib, hoje="2026-11-10", consertos=consertos, quem=quem)
        self.assertEqual((r["aprovadas"], r["editadas"], r["erros"]), (1, 1, []))
        cab, corpo = cl.separar((self.leitura / "contratos" / "contrato-produto.md").read_text(encoding="utf-8"))
        self.assertIn("Frase consertada.", corpo)
        self.assertNotIn("Frase errada do analista.", corpo)
        self.assertIn("\ncurado: sim\n", cab)
        self.assertIn("# ! Alteração de IA - Revisar: (10/11/2026) 1 conserto do Claude no texto que o analista escreveu na curadoria desta leitura", cab)
        self.assertIn("# ! Motivo: a frase dizia que a busca é vetorial, e a busca deste projeto é por palavras", cab)
        self.assertIn("Curada em 10/11/2026 por um analista, com o Eric passando a leitura e colando a resposta, na página da curadoria: texto revisado.", corpo)
        self.assertIn("1 conserto do Claude", corpo)
        self.assertIn(cl.ARQ_CONSERTOS_MD, corpo)
        cv = (self.leitura / "erros" / "corpo_vazio.md").read_text(encoding="utf-8")
        self.assertIn("Curada em 10/11/2026 por um analista, com o Eric passando a leitura e colando a resposta, na página da curadoria: aprovada como estava.", cv)
        self.assertNotIn("conserto", cl.separar(cv)[0])
        self.assertEqual(cl.bl.conferir(self.bib, self.leitura), [])
        item = next(x for x in r["itens"] if x["id"] == "contrato-produto")
        self.assertEqual(item["consertos"], 1)
        self.assertEqual(cl.bl.carregar(self.leitura)["contrato-produto"]["curado"], True)

    def teste_conserto_que_nao_acha_o_trecho_uma_vez_so_deixa_o_arquivo_como_estava(self):
        itens = {x["id"]: x for x in cl.itens(self.bib, self.leitura)}
        antes = (self.leitura / "contratos" / "contrato-produto.md").read_text(encoding="utf-8")
        salvo = itens["contrato-produto"]["corpo"].replace("## O que é", "## O que é\n\nFrase do analista. Frase do analista.", 1)
        resposta = {"id": "contrato-produto", "estado": "editada", "texto": salvo, "corpo_sha": itens["contrato-produto"]["corpo_sha"]}
        for conserto, trecho in (({"antigo": "isto não está no texto", "novo": "x", "motivo": "m"}, "não aparece"), ({"antigo": "Frase do analista.", "novo": "x", "motivo": "m"}, "2 vezes"),
                                 ({"antigo": "## O que é", "novo": "x"}, "motivo")):
            r = cl.aplicar([resposta], self.leitura, self.bib, hoje="2026-11-10", consertos={"contrato-produto": [conserto]})
            self.assertEqual((r["editadas"], len(r["erros"])), (0, 1), conserto)
            self.assertIn(trecho, r["erros"][0])
            self.assertEqual((self.leitura / "contratos" / "contrato-produto.md").read_text(encoding="utf-8"), antes)
        r = cl.aplicar([{"id": "corpo_vazio", "estado": "aprovada", "corpo_sha": itens["corpo_vazio"]["corpo_sha"]}], self.leitura, self.bib, hoje="2026-11-10",
                       consertos={"corpo_vazio": [{"antigo": "## O que é", "novo": "x", "motivo": "m"}]})
        self.assertEqual((r["aprovadas"], len(r["erros"])), (0, 1))
        self.assertIn("só valem para resposta editada", r["erros"][0])

    def teste_render_consertos_lista_cada_troca_com_o_motivo_o_antes_e_o_depois(self):
        consertos = {"contrato-produto": [{"antigo": "Frase errada do analista.", "novo": "Frase consertada.", "motivo": "a frase dizia que a busca é vetorial"}],
                     "corpo_vazio": [{"antigo": "linha um\nlinha dois", "novo": "linha única", "motivo": "duas linhas coladas"}, {"antigo": "a", "novo": "b", "motivo": "duas linhas coladas"}]}
        md = cl.render_consertos(consertos, hoje="2026-11-10")
        self.assertTrue(md.startswith("<!-- ! Alteração de IA - Revisar"))
        self.assertIn("! Motivo:", md)
        for trecho in ("## `contrato-produto` (1 conserto)", "## `corpo_vazio` (2 consertos)", "a frase dizia que a busca é vetorial", "Frase errada do analista.", "Frase consertada.",
                       "linha um", "linha única", "3 consertos em 2 leituras", "10/11/2026"):
            self.assertIn(trecho, md, trecho)
        self.assertNotIn("\u2014", md)
        self.assertNotIn("\u2192", md)

    def teste_estado_conta_curadas_e_em_aberto(self):
        e = cl.estado(self.leitura)
        self.assertEqual((e["total"], e["curadas"], e["em_aberto"]), (2, 0, ["contrato-produto", "corpo_vazio"]))
        itens = {x["id"]: x for x in cl.itens(self.bib, self.leitura)}
        cl.aplicar([{"id": "corpo_vazio", "estado": "aprovada", "corpo_sha": itens["corpo_vazio"]["corpo_sha"]}], self.leitura, self.bib, hoje="2026-11-10")
        e = cl.estado(self.leitura)
        self.assertEqual((e["total"], e["curadas"], e["em_aberto"]), (2, 1, ["contrato-produto"]))


if __name__ == "__main__":
    unittest.main(verbosity=1)
