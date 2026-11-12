# ! Alteração de IA - Revisar: arquivo novo (11/11/2026) com os testes de `painel_grupo.py`, escritos antes do código: a troca do nome do autor e de "você" por
# "grupo" no texto que o painel mostra, sem tocar em marcação, classe, identificador, estilo nem imagem embutida.
# ! Motivo: o Eric pediu que o painel fale do grupo ("tudo o que cita meu nome vamos mudar para Grupo, assim como você também"). O painel é montado das fichas, do
# roadmap e das decisões do Memorial, que são o registro interno e continuam citando quem decidiu; a troca acontece só na montagem da página, e sem teste ela
# poderia estragar um comando, um caminho ou a concordância de uma frase.
"""Testes de painel_grupo.py. Uso: python ferramentas/testar_painel_grupo.py"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import painel_grupo as pg


class TesteTexto(unittest.TestCase):
    def teste_nome_com_artigo_e_preposicao(self):
        casos = {"o Eric respondeu as fichas": "o grupo respondeu as fichas", "O Eric escolheu medir": "O grupo escolheu medir", "pelo Eric em 10/11/2026": "pelo grupo em 10/11/2026",
                 "decisão do Eric": "decisão do grupo", "Do Eric, no quadro": "Do grupo, no quadro", "pergunta ao Eric": "pergunta ao grupo", "com o Eric na sala": "com o grupo na sala",
                 "do próprio Eric": "do próprio grupo", "pelo próprio Eric": "pelo próprio grupo"}
        for antes, depois in casos.items():
            self.assertEqual(pg.texto_para_o_grupo(antes), depois, antes)

    def teste_nome_sozinho(self):
        self.assertEqual(pg.texto_para_o_grupo("Quem decide: Eric"), "Quem decide: Grupo")
        self.assertEqual(pg.texto_para_o_grupo("Eric (10/11/2026), no quadro"), "Grupo (10/11/2026), no quadro")
        self.assertEqual(pg.texto_para_o_grupo("decisão — Eric aprovou"), "decisão — Grupo aprovou")
        self.assertEqual(pg.texto_para_o_grupo("o pré-requisito é Eric rodar a corrida"), "o pré-requisito é o grupo rodar a corrida")

    def teste_frases_que_pedem_cuidado(self):
        self.assertEqual(pg.texto_para_o_grupo("lançada pelo Eric da janela dele, na fila"), "lançada pelo grupo de uma janela do PowerShell, na fila")
        self.assertEqual(pg.texto_para_o_grupo("o Eric roda na janela dele"), "o grupo roda numa janela do PowerShell")
        self.assertEqual(pg.texto_para_o_grupo("um analista de QA da empresa em que o Eric trabalha, que atua com teste"),
                         "um analista de QA da empresa de um integrante do grupo, que atua com teste")
        self.assertEqual(pg.texto_para_o_grupo("a L1 dele e a cópia curada"), "a L1 dele e a cópia curada", "o pronome que não fala do autor fica")

    def teste_voce(self):
        casos = {"se você quiser a marca": "se o grupo quiser a marca", "Você decide pela ficha": "O grupo decide pela ficha", "O que precisa de você": "O que precisa do grupo",
                 "fica para você conferir": "fica para o grupo conferir", "medido por você": "medido pelo grupo", "combinado com você": "combinado com o grupo",
                 "cabe a você": "cabe ao grupo", "por sua vez": "por sua vez"}
        for antes, depois in casos.items():
            self.assertEqual(pg.texto_para_o_grupo(antes), depois, antes)

    def teste_caminho_com_o_nome_do_usuario(self):
        self.assertEqual(pg.texto_para_o_grupo(r"C:\Users\Eric.Derre\Documents\TCC\run.py"), r"C:\Users\usuario\Documents\TCC\run.py")
        self.assertEqual(pg.texto_para_o_grupo(r"C:\\Users\\Eric.Derre\\MariaDB"), r"C:\\Users\\usuario\\MariaDB", "dentro de JSON a barra vem dobrada")

    def teste_aplicar_duas_vezes_da_o_mesmo(self):
        frase = "O Eric respondeu; se você quiser, o comando do Eric roda na janela dele em C:\\Users\\Eric.Derre\\x"
        uma = pg.texto_para_o_grupo(frase)
        self.assertEqual(pg.texto_para_o_grupo(uma), uma)
        self.assertNotRegex(uma, r"\bEric\b|[Vv]ocê")


class TestePagina(unittest.TestCase):
    def teste_troca_no_texto_e_deixa_a_marcacao(self):
        html = ('<ol class="lista-eric"><li data-quem="eric">Quem decide: Eric</li></ol><p>O Eric <strong>respondeu</strong> e você confere.</p>'
                '<img alt="figura do Eric" src="data:image/png;base64,AAA+Eric/BBB=">')
        saida = pg.para_o_grupo(html)
        self.assertIn('<ol class="lista-eric"><li data-quem="eric">Quem decide: Grupo</li></ol>', saida)
        self.assertIn("<p>O grupo <strong>respondeu</strong> e o grupo confere.</p>", saida)
        self.assertIn('alt="figura do grupo"', saida)
        self.assertIn('src="data:image/png;base64,AAA+Eric/BBB="', saida, "a imagem embutida não é texto")

    def teste_atributos_que_a_pessoa_le_ou_copia(self):
        html = '<button class="copiar" data-cmd="powershell -File &quot;C:\\Users\\Eric.Derre\\Documents\\TCC\\x.ps1&quot;" title="comando do Eric" aria-label="copiar para você">copiar</button>'
        saida = pg.para_o_grupo(html)
        self.assertIn("C:\\Users\\usuario\\Documents\\TCC\\x.ps1", saida)
        self.assertIn('title="comando do grupo"', saida)
        self.assertIn('aria-label="copiar para o grupo"', saida)
        self.assertIn('class="copiar"', saida)

    def teste_script_e_estilo(self):
        html = ('<style>.lista-eric{color:red}/* do Eric */</style><script>window.DADOS = {"rotulo":"resposta do Eric, lendo na página","respostas_do_eric":1};'
                'let fEric = false;</script>')
        saida = pg.para_o_grupo(html)
        self.assertIn(".lista-eric{color:red}/* do Eric */", saida, "o estilo não é texto do painel")
        self.assertIn('"rotulo":"resposta do grupo, lendo na página"', saida)
        self.assertIn('"respostas_do_eric":1', saida)
        self.assertIn("let fEric = false;", saida)

    def teste_o_que_sobra(self):
        html = "<p>O Eric decidiu.</p><script>var x = 'o Eric';</script><code>Eric.Derre</code><p>Você viu?</p><i title='do Eric'>x</i>"
        sobras = pg.sobras(html)
        self.assertEqual(len(sobras), 5, sobras)
        self.assertTrue(any("O Eric decidiu" in s for s in sobras) and any("Você viu" in s for s in sobras), sobras)
        self.assertEqual(pg.sobras(pg.para_o_grupo(html)), [])
        self.assertEqual(pg.sobras('<ol class="lista-eric"><li data-quem="eric">ok</li></ol><style>/* do Eric */</style>'), [], "classe, identificador e estilo não contam")


if __name__ == "__main__":
    unittest.main()
