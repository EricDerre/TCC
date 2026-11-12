# ! Alteração de IA - Revisar: arquivo novo (11/11/2026) com os testes de `painel_glossario.py`: a lista dos termos e dos métodos, a marcação do termo na primeira
# vez em que ele aparece em cada aba, a lista "Termos e métodos desta aba" e a aba "Glossário e métodos".
# ! Motivo: o Eric pediu que o painel explique métodos e termos técnicos onde eles aparecem, e que todo método venha com resumo, com o que o projeto faz de
# diferente e com a citação. Sem teste, um método poderia entrar sem fonte, uma chave de fonte poderia deixar de achar a linha em `referencias.md` depois de uma
# rodada de pesquisa, e a marcação poderia entrar dentro de um comando, de um título ou de um atributo e quebrar a página.
"""Testes de painel_glossario.py. Uso: python ferramentas/testar_painel_glossario.py"""
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import painel_glossario as g

RAIZ = Path(__file__).resolve().parents[1]
REFS = (RAIZ / "Documentacao" / "memorial" / "2-pesquisa-e-literatura" / "referencias.md").read_text(encoding="utf-8")
# O método e o sobrenome que a fonte dele precisa trazer: a referência original de cada um, ou a que o documento do TCC cita na seção 5.7.
FONTE_DO_METODO = {"wilson": "WILSON", "mcnemar": "McNEMAR", "bootstrap": "EFRON", "acuracia-balanceada": "BRODERSEN", "cochran": "COCHRAN", "holm": "HOLM", "g-cohen": "COHEN",
                   "auroc": "FAWCETT", "bm25": "ROBERTSON", "hit-k": "VOORHEES", "tpr-tnr": "GUAN", "flesch": "FLESCH", "troca-de-rotulo": "DUTTA"}
# As entradas do glossário do documento do TCC que o painel também precisa explicar (pelo id do termo aqui).
DO_GLOSSARIO_DO_TCC = ["acuracia-balanceada", "api", "arvore-de-acessibilidade", "biblioteca", "carimbo", "caso-escrito", "ineditos", "ciclo-de-correcao", "corrida", "contrato",
                       "self-healing", "e2e", "epoca", "llm", "mttr", "ollama", "playwright", "poda", "ponte", "probabilidade-da-resposta", "qa", "quantizacao", "rag",
                       "recuperacao-por-id", "selo", "task-success", "token", "trilha", "validacao-em-codigo"]


def _aba(sid: str, corpo: str) -> str:
    return f'<section id="{sid}" hidden>\n<h1>Título</h1>\n{corpo}\n</section>'


def _marcas(html_: str) -> list[tuple[str, str]]:
    return re.findall(r'<span class="termo" tabindex="0" data-termo="([^"]+)">([^<]*)</span>', html_)


class TesteTermos(unittest.TestCase):
    def teste_ids_unicos_e_grupos_conhecidos(self):
        ids = [t["id"] for t in g.TERMOS]
        self.assertEqual(len(ids), len(set(ids)), [i for i in ids if ids.count(i) > 1])
        self.assertEqual({t["grupo"] for t in g.TERMOS}, {chave for chave, _ in g.GRUPOS})

    def teste_todo_termo_tem_resumo_curto_e_padroes_que_compilam(self):
        for t in g.TERMOS:
            self.assertTrue(t["termo"].strip() and t["curto"].strip(), t["id"])
            self.assertLessEqual(len(t["curto"]), 260, f'{t["id"]}: o resumo curto vai numa dica, não cabe um parágrafo')
            self.assertTrue(t["padroes"], t["id"])
            for p in t["padroes"]:
                re.compile(p)

    def teste_todo_metodo_tem_resumo_explicacao_e_o_que_o_projeto_faz(self):
        metodos = [t for t in g.TERMOS if t["grupo"] == "metodo"]
        self.assertGreaterEqual(len(metodos), 20)
        for t in metodos:
            self.assertTrue(t["explicacao"].strip(), f'{t["id"]}: método sem explicação')
            self.assertTrue(t["no_projeto"].strip(), f'{t["id"]}: método sem dizer o que o projeto faz com ele')

    def teste_toda_fonte_resolve_em_uma_linha_de_referencias(self):
        self.assertEqual(g.fontes_que_faltam(REFS), [])
        n_chaves = sum(len(t["fontes"]) for t in g.TERMOS)
        self.assertEqual(len(g.fontes_que_faltam("")), n_chaves, "sem a lista de referências, toda chave precisa ser acusada")
        self.assertIsNone(g.fonte("ref:AUTOR QUE NÃO EXISTE", REFS))

    def teste_metodo_da_literatura_cita_a_fonte_dele(self):
        por_id = {t["id"]: t for t in g.TERMOS}
        for termo, sobrenome in FONTE_DO_METODO.items():
            fontes = [g.fonte(c, REFS) or "" for c in por_id[termo]["fontes"]]
            self.assertTrue(any(sobrenome in f for f in fontes), f"{termo}: falta a fonte de {sobrenome} ({fontes})")

    def teste_fonte_sai_sem_negrito_e_sem_a_marca_de_conferencia(self):
        texto = g.fonte("ref:COHEN, J. **Statistical power", REFS)
        self.assertIn("Statistical power analysis", texto)
        self.assertNotIn("**", texto)
        self.assertNotIn("suporte parcial", texto)

    def teste_texto_sem_travessao_seta_nome_nem_voce(self):
        for t in g.TERMOS:
            texto = " ".join([t["termo"], t["curto"], t["explicacao"], t["no_projeto"]])
            self.assertNotRegex(texto, r"[—→↔]", t["id"])
            self.assertNotRegex(texto, r"\bEric\b|\b[Vv]ocês?\b", t["id"])

    def teste_termos_do_glossario_do_tcc_estao_no_painel(self):
        ids = {t["id"] for t in g.TERMOS}
        self.assertEqual([i for i in DO_GLOSSARIO_DO_TCC if i not in ids], [])


class TesteAnotar(unittest.TestCase):
    def teste_marca_so_a_primeira_ocorrencia_de_cada_aba(self):
        pagina = _aba("a", "<p>O verbete entra. Outro verbete também.</p>") + _aba("b", "<p>Aqui o verbete aparece de novo.</p>")
        saida = g.anotar(pagina, REFS)
        self.assertEqual(_marcas(saida), [("verbete", "verbete"), ("verbete", "verbete")])
        primeira = saida[:saida.index('<section id="b"')]
        self.assertEqual(len(_marcas(primeira)), 1)
        self.assertIn("Outro verbete também", primeira, "a segunda ocorrência da mesma aba fica como estava")

    def teste_nao_marca_codigo_titulo_botao_link_nem_atributo(self):
        corpo = ('<h2>O BM25 no título</h2><p><code>BM25</code> <a href="#x">BM25</a> <button>BM25</button></p><p title="BM25">sem termo</p>'
                 '<table><thead><tr><th>BM25</th></tr></thead></table><script>var a = "BM25";</script><details><summary>BM25</summary><p>dentro</p></details>')
        saida = g.anotar(_aba("a", corpo), REFS)
        self.assertEqual(_marcas(saida), [], saida)
        self.assertIn('<p title="BM25">sem termo</p>', saida)
        self.assertEqual(_marcas(g.anotar(_aba("a", "<p>O BM25 no texto</p>"), REFS)), [("bm25", "BM25")])

    def teste_so_a_classe_exata_impede_a_marca(self):
        self.assertEqual(_marcas(g.anotar(_aba("a", '<div class="kpi"><b>BM25</b></div>'), REFS)), [], "o cartão de número não leva marca")
        self.assertEqual(_marcas(g.anotar(_aba("a", "<div class='kpi'><span>BM25</span></div>"), REFS)), [], "o gerador escreve a classe do cartão com aspas simples")
        self.assertEqual(_marcas(g.anotar(_aba("a", '<div class="numeros marcadas"><p>BM25</p></div>'), REFS)), [("bm25", "BM25")],
                         "uma classe que só contém o nome de outra não pode tirar a marca do bloco inteiro")

    def teste_prefere_o_termo_mais_especifico(self):
        saida = g.anotar(_aba("a", "<p>Usamos o intervalo de confiança de 95% pelo método de escore de Wilson e o teste exato de McNemar. O IC é largo.</p>"), REFS)
        self.assertEqual(_marcas(saida), [("wilson", "intervalo de confiança de 95% pelo método de escore de Wilson"), ("mcnemar", "teste exato de McNemar"), ("ic", "IC")])

    def teste_lista_do_fim_da_aba_traz_resumo_o_que_o_projeto_faz_e_fonte(self):
        saida = g.anotar(_aba("a", "<p>O teste de McNemar compara as corridas.</p>"), REFS)
        lista = saida[saida.index('<details class="termos-da-aba">'):saida.index("</details>") + len("</details>")]
        self.assertIn("Termos e métodos desta aba (2)", lista)
        self.assertIn('data-ir="glossario|termo-mcnemar"', lista)
        self.assertIn("Neste projeto:", lista, "o método diz o que o projeto faz com ele")
        self.assertIn("McNEMAR, Quinn.", lista, "o método vem com a citação")
        self.assertIn("Acesso em: 11 nov. 2026.<br>RASCHKA, S.", lista, "cada fonte em uma linha: emendadas, não dá para ver onde uma acaba")
        self.assertLess(saida.index('<details class="termos-da-aba">'), saida.index("</section>"), "a lista fica dentro da aba")
        self.assertEqual(lista.count("<dt>"), 2)

    def teste_aba_sem_termo_nao_ganha_lista(self):
        self.assertNotIn("termos-da-aba", g.anotar(_aba("a", "<p>Nada de especial aqui.</p>"), REFS))

    def teste_aplicar_duas_vezes_da_o_mesmo(self):
        pagina = _aba("a", "<p>O verbete entra. Outro verbete e o prompt.</p>") + _aba("b", "<p>O selo de confiança e a corrida.</p>")
        uma = g.anotar(pagina, REFS)
        self.assertEqual(g.anotar(uma, REFS), uma)

    def teste_marcacao_continua_bem_formada(self):
        corpo = '<p>O <strong>verbete</strong> e o prompt.</p><ul><li>A corrida 25 usa o BM25<li>e a poda</ul><p>Fim com token.</p><img alt="verbete" src="x.png">'
        saida = g.anotar(_aba("a", corpo), REFS)
        self.assertNotRegex(saida, r'<[^<>]*<span class="termo"', "a marca não entra dentro de outra marcação")
        self.assertIn('<img alt="verbete" src="x.png">', saida)
        acrescidos = saida.count("</span>") - _aba("a", corpo).count("</span>")
        self.assertEqual(acrescidos, len(_marcas(saida)) + saida[saida.index("termos-da-aba"):].count('<span class="nota">'))
        self.assertIn(("poda", "poda"), _marcas(saida), "o item de lista sem fechamento não trava a marca dos seguintes")

    def teste_aba_do_glossario_nao_e_marcada(self):
        pagina = g.secao_glossario(REFS) + _aba("a", "<p>O verbete.</p>")
        saida = g.anotar(pagina, REFS)
        glossario = saida[saida.index('<section id="glossario"'):saida.index("</section>")]
        self.assertEqual(_marcas(glossario), [])
        self.assertNotIn("termos-da-aba", glossario)


class TesteAba(unittest.TestCase):
    def teste_aba_tem_uma_entrada_por_termo_nos_grupos(self):
        aba = g.secao_glossario(REFS)
        self.assertTrue(aba.startswith('<section id="glossario" hidden>'))
        for t in g.TERMOS:
            self.assertEqual(aba.count(f'id="termo-{t["id"]}"'), 1, t["id"])
        for _, titulo in g.GRUPOS:
            self.assertIn(f"<h2>{titulo}</h2>", aba)
        self.assertIn("McNEMAR, Quinn.", aba)
        self.assertIn("<br>OPITZ, J.", aba, "cada fonte em uma linha")
        self.assertIn("<strong>Neste projeto.</strong>", aba)
        # o título de uma fonte é copiado como está em referencias.md (um deles traz travessão); o que o módulo escreve não pode trazer
        self.assertNotRegex(re.sub(r'<p class="nota"><strong>Fonte\.</strong>.*?</p>', "", aba), r"[—→]")

    def teste_script_leva_os_dados_e_fecha_no_lugar(self):
        s = g.script()
        self.assertTrue(s.startswith("<script>") and s.endswith("</script>"))
        self.assertEqual(s.count("</script>"), 1)
        for t in g.TERMOS:
            self.assertIn(f'"{t["id"]}":', s)
        self.assertIn(".dica-termo", g.CSS)
        self.assertIn(".termo{", g.CSS)


if __name__ == "__main__":
    unittest.main()
