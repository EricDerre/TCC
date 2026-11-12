#!/usr/bin/env python3
# ! Alteração de IA - Revisar: testes da revisão humana às cegas das propostas de edição (11/11/2026, corrida 27, ficha 67 opção b, decisão 121), escritos antes de
# `revisao_propostas.py`: a lista do que vai para a revisão (as propostas da corrida 27 que passam nos filtros de hoje e as 20 edições da corrida 20, embaralhadas com
# semente fixa), a página e a planilha sem nenhuma marca da origem, a leitura da planilha preenchida, a montagem do resultado que `experimento_analista.resumir` lê, a
# gravação na pasta da corrida e a recusa de gravar sem dizer quem revisou.
# ! Motivo: a medida M2 compara a parcela correta das duas corridas pela mesma pessoa, sem ela saber de qual corrida veio cada proposta; se a página ou a planilha
# deixarem escapar a origem, a comparação deixa de ser às cegas, e se o resultado gravado não tiver a forma que a leitura espera, a revisão feita se perde. Quem revisa é
# resposta do Eric: a ferramenta não tem nome padrão e recusa gravar sem ele.
"""Uso: python ferramentas/testar_revisao_propostas.py"""
from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

os.environ.setdefault("RESULTADOS_DIR", "resultados_alvo")
sys.path.insert(0, str(Path(__file__).resolve().parent))
import revisao_propostas as rp


def _registros_da_corrida_27() -> list[dict]:
    """Três registros no formato de `propostas__analista.jsonl`, sobre casos reais da corrida 20: duas propostas que passam nos filtros de hoje e uma que não passa."""
    itens = rp.ea.casos_da_corrida_20()[:3]

    def registro(item: dict, operacao: str, passa: bool, texto: str = "", termos: list | None = None) -> dict:
        caso = item["caso"]
        edicao = {"epoca": rp.ea.EPOCA, "caso": caso["id"], "numero": 1, "operacao": operacao, "verbete": caso["gabarito"]["causa_raiz"], "arquivo": "erros/x.md", "texto": texto,
                  "motivo": "O status 200 da resposta não bastou para a tela montar a lista.", "trecho": None, "palavras_chave_novas": termos or [], "sintomas_novos": [], "novo": None,
                  "modelo": "qwen2.5:7b"}
        return {"caso": caso["id"], "operacao": operacao, "abstencao": False, "malformado": None, "passa_nos_filtros_de_hoje": passa, "edicao": edicao if passa else None,
                "campos": {"TEXTO": texto}, "ficha": "FICHA DE TESTE <b>com marcação</b>"}

    return [registro(itens[0], "nota", True, texto="A interface mostra o erro de leitura quando o corpo da resposta não é JSON."),
            registro(itens[1], "sinal_de_busca", True, termos=["tela em branco", "lista vazia"]),
            registro(itens[2], "nota", False, texto="Adicionar nota sobre o corpo vazio.")]


class TesteDaRevisaoDasPropostas(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registros = _registros_da_corrida_27()
        cls.itens = rp.itens_da_revisao(cls.registros)

    def teste_itens_juntam_as_duas_corridas_embaralhados_com_semente_fixa(self):
        origens = [i["origem"] for i in self.itens]
        self.assertEqual((origens.count("27"), origens.count("20")), (2, 20), "as 2 que passam nos filtros de hoje e as 20 edições revisadas da corrida 20")
        self.assertEqual([i["n"] for i in self.itens], list(range(1, 23)))
        self.assertEqual([i["id"] for i in self.itens], [f"p{n:02d}" for n in range(1, 23)])
        self.assertEqual([(i["origem"], i["caso"], i["verbete"]) for i in rp.itens_da_revisao(self.registros)], [(i["origem"], i["caso"], i["verbete"]) for i in self.itens],
                         "a mesma semente dá a mesma ordem")
        self.assertNotEqual([(i["origem"], i["caso"], i["verbete"], i["texto"]) for i in rp.itens_da_revisao(self.registros, semente=7)],
                            [(i["origem"], i["caso"], i["verbete"], i["texto"]) for i in self.itens])
        self.assertNotEqual(origens, sorted(origens), "as duas corridas ficam misturadas")
        so_27 = rp.itens_da_revisao(self.registros, com_a_corrida_20=False)
        self.assertEqual([i["origem"] for i in so_27], ["27", "27"])
        for i in self.itens:
            self.assertIn(i["operacao"], ("nota", "retificacao", "novo_verbete", "sinal_de_busca"))
            self.assertTrue(i["verbete_texto"] and i["ficha"] and i["motivo"], i["id"])
            self.assertTrue(i["texto"] or i["palavras_chave"] or i["sintomas"], i["id"])
        sinal = next(i for i in self.itens if i["operacao"] == "sinal_de_busca")
        self.assertEqual((sinal["palavras_chave"], sinal["texto"]), (["tela em branco", "lista vazia"], ""))
        novo = next(i for i in self.itens if i["operacao"] == "novo_verbete")
        self.assertIn("verbete novo", novo["verbete_texto"])

    def teste_o_que_o_revisor_ve_nao_diz_de_qual_corrida_veio(self):
        for i in self.itens:
            publico = rp.publico(i)
            self.assertNotIn("origem", publico)
            self.assertNotIn("epoca", json.dumps(publico, ensure_ascii=False))
        planilha = rp.planilha(self.itens)
        pagina = rp.pagina(self.itens)
        for texto in (planilha.split("-->", 1)[-1], pagina.split("<main>", 1)[-1]):
            for marca in ("corrida 20", "corrida 27", "fase4_biblioteca", "fase4_analista", "E101", "E127", '"origem"'):
                self.assertNotIn(marca, texto, marca)

    def teste_planilha_as_cegas_e_lida_de_volta_depois_de_preenchida(self):
        planilha = rp.planilha(self.itens)
        linhas = [l for l in planilha.splitlines() if l.startswith("| ") and not l.startswith("| # |")]
        self.assertEqual(len(linhas), len(self.itens))
        self.assertTrue(all(l.rstrip().endswith(f"| {rp.CELULA_EM_BRANCO} |  |") for l in linhas))
        self.assertEqual(rp.vereditos_da_planilha(planilha), {i["n"]: (rp.CELULA_EM_BRANCO, "") for i in self.itens})
        preenchida = planilha.replace(f"| {rp.CELULA_EM_BRANCO} |  |", "| Parcial | vago \\| sem fato novo |", 1)
        lidos = rp.vereditos_da_planilha(preenchida)
        self.assertEqual(lidos[1], ("Parcial", "vago \\| sem fato novo"))
        self.assertEqual(sum(1 for v, _ in lidos.values() if v == rp.CELULA_EM_BRANCO), len(self.itens) - 1)
        self.assertIn("de IA - Revisar", planilha)
        self.assertIn("! Motivo:", planilha)

    def teste_pagina_mostra_uma_proposta_por_vez_com_o_verbete_a_ficha_e_os_tres_vereditos(self):
        pagina = rp.pagina(self.itens)
        self.assertIn("<title>Revisão das propostas de edição</title>", pagina)
        for trecho in ('id="correta"', 'id="parcial"', 'id="errada"', 'id="comentario"', 'collection("revisao_propostas")', "Copiar as respostas", "de IA - Revisar", "! Motivo:"):
            self.assertIn(trecho, pagina, trecho)
        self.assertIn("A interface mostra o erro de leitura quando o corpo da resposta não é JSON.", pagina)
        self.assertNotIn("<b>com marcação</b>", pagina, "o texto da ficha entra como dado, sem virar HTML")
        self.assertIn("\\u003cb>com marcação", pagina)
        self.assertNotIn("—", pagina.split("<main>", 1)[-1].split("<script", 1)[0])
        for criterio in rp.CRITERIOS.values():
            self.assertIn(criterio[:40], pagina)

    def teste_monta_o_resultado_que_a_leitura_da_corrida_27_le(self):
        respostas = [{"id": i["id"], "veredito": "Correta" if i["origem"] == "27" else "Errada", "comentario": "ok"} for i in self.itens[:-1]]
        r = rp.montar_revisao(self.itens, respostas, "revisor de teste")
        self.assertEqual(r["quem"], "revisor de teste")
        self.assertEqual(len(r["itens"]), len(self.itens))
        self.assertEqual({k for k in r["itens"][0]}, {"n", "id", "origem", "caso", "verbete", "operacao", "veredito", "comentario"})
        self.assertEqual(sum(1 for x in r["itens"] if x["veredito"] is None), 1, "o que ficou sem resposta entra sem veredito, e a leitura conta como pendente")
        self.assertEqual(r["respondidas"], len(self.itens) - 1)
        with self.assertRaises(SystemExit):
            rp.montar_revisao(self.itens, [{"id": "p01", "veredito": "Mais ou menos", "comentario": ""}], "revisor de teste")
        with self.assertRaises(SystemExit):
            rp.montar_revisao(self.itens, [{"id": "p99", "veredito": "Correta", "comentario": ""}], "revisor de teste")
        with self.assertRaises(SystemExit):
            rp.montar_revisao(self.itens, respostas, "  ")
        # a leitura da corrida 27 aceita o resultado como ele sai daqui
        from testar_pos_fase4 import _dados_do_analista
        x = _dados_do_analista()
        dado = rp.ea.resumir(x["registros"], x["corrida20"], x["condicoes"], ponte=x["ponte"], corrida="x", revisao=r)
        self.assertIsNotNone(dado["revisao"])
        self.assertEqual(dado["revisao"]["quem"], "revisor de teste")

    def teste_gravar_escreve_na_pasta_da_corrida_e_recusa_sem_quem(self):
        with tempfile.TemporaryDirectory() as tmp:
            pasta = Path(tmp)
            escritos = rp.gerar(self.registros, pasta, pasta / "pagina.html")
            self.assertEqual(sorted(p.name for p in escritos), sorted(["pagina.html", rp.ARQ_PLANILHA, rp.ARQ_CHAVE]))
            chave = json.loads((pasta / rp.ARQ_CHAVE).read_text(encoding="utf-8"))
            self.assertEqual((len(chave["itens"]), chave["semente"]), (len(self.itens), rp.SEMENTE))
            self.assertEqual({x["origem"] for x in chave["itens"]}, {"20", "27"})
            respostas = pasta / "respostas.json"
            respostas.write_text(json.dumps([{"id": i["id"], "veredito": "Parcial", "comentario": ""} for i in self.itens]), encoding="utf-8")
            self.assertEqual(rp.main(["--gravar", str(respostas), "--pasta", str(pasta)]), 2, "sem --quem a ferramenta não grava")
            self.assertFalse((pasta / rp.ARQ_REVISAO).exists())
            self.assertEqual(rp.main(["--gravar", str(respostas), "--pasta", str(pasta), "--quem", "revisor de teste"]), 0)
            gravado = json.loads((pasta / rp.ARQ_REVISAO).read_text(encoding="utf-8"))
            self.assertEqual((gravado["quem"], gravado["respondidas"], len(gravado["itens"])), ("revisor de teste", len(self.itens), len(self.itens)))
            self.assertEqual(rp.ea.ler_revisao(pasta)["quem"], "revisor de teste")
            final = (pasta / rp.ARQ_PLANILHA_FINAL).read_text(encoding="utf-8")
            self.assertIn("revisor de teste", final)
            self.assertIn("| corrida 20 |", final)
            # a planilha preenchida também serve de entrada
            preenchida = (pasta / rp.ARQ_PLANILHA).read_text(encoding="utf-8").replace(f"| {rp.CELULA_EM_BRANCO} |  |", "| Correta |  |")
            (pasta / rp.ARQ_PLANILHA).write_text(preenchida, encoding="utf-8")
            self.assertEqual(rp.main(["--gravar", "--da-planilha", "--pasta", str(pasta), "--quem", "outro revisor"]), 0)
            self.assertEqual(json.loads((pasta / rp.ARQ_REVISAO).read_text(encoding="utf-8"))["quem"], "outro revisor")

    def teste_gerar_pela_linha_de_comando_le_os_registros_da_pasta_da_corrida(self):
        # é o caminho que a fila rodar_fila_pre_fase5.ps1 usa logo depois da corrida 27: --gerar lê propostas__analista.jsonl da pasta da corrida
        import contextlib
        import io
        with tempfile.TemporaryDirectory() as tmp:
            pasta = Path(tmp)
            self.assertEqual(rp.main(["--gerar", "--pasta", str(pasta), "--saida", str(pasta / "pagina.html")]), 2, "sem os registros da corrida, nada é gerado")
            self.assertFalse((pasta / "pagina.html").exists())
            do_modelo = pasta / rp.executar_fase3._slug(rp.ea.MODELO)
            do_modelo.mkdir()
            (do_modelo / rp.ea.NOME_DO_REGISTRO).write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in self.registros), encoding="utf-8")
            saida = io.StringIO()
            with contextlib.redirect_stdout(saida):
                self.assertEqual(rp.main(["--gerar", "--pasta", str(pasta), "--saida", str(pasta / "pagina.html")]), 0)
            self.assertIn("22 itens para revisar: 2 da corrida 27 e 20 da corrida 20", saida.getvalue())
            self.assertTrue((pasta / "pagina.html").exists() and (pasta / rp.ARQ_PLANILHA).exists() and (pasta / rp.ARQ_CHAVE).exists())
            # nenhuma proposta da corrida 27 passou nos filtros: a ferramenta avisa que não há o que comparar
            (do_modelo / rp.ea.NOME_DO_REGISTRO).write_text(json.dumps(self.registros[2], ensure_ascii=False) + "\n", encoding="utf-8")
            saida = io.StringIO()
            with contextlib.redirect_stdout(saida):
                self.assertEqual(rp.main(["--gerar", "--pasta", str(pasta), "--saida", str(pasta / "pagina.html")]), 0)
            self.assertIn("nenhuma proposta da corrida 27 passou nos filtros de hoje", saida.getvalue())


if __name__ == "__main__":
    unittest.main(verbosity=1)
