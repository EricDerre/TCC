# ! Alteração de IA - Revisar: arquivo novo (11/11/2026) com os testes de `painel_fases.py`: a leitura do README e do roadmap, a navegação lateral por fase, a
# faixa de sub-abas, os cartões do roadmap em linha, a aba de visão de cada fase e o Início.
# ! Motivo: o painel passou a ser organizado por fase a pedido do Eric. Sem teste, uma fase poderia ficar sem a pergunta do README ou sem a linha do roadmap,
# uma corrida nova poderia ficar sem fase, um passo poderia apontar para uma aba que não existe, e o texto longo do estado poderia voltar para dentro do cartão,
# que era justamente o defeito do Roadmap (cartões estreitos e altos, com o texto descendo por várias rolagens).
"""Testes de painel_fases.py. Uso: python ferramentas/testar_painel_fases.py"""
import re
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parent))
import painel_fases as pf
import painel_textos as pt

RAIZ = Path(__file__).resolve().parents[1]
README_REAL = pf.README.read_text(encoding="utf-8")
ROAD_REAL = pt.ler_roadmap(RAIZ / "Documentacao" / "memorial" / "roadmap.md")
DECISOES = (RAIZ / "Documentacao" / "memorial" / "1-decisoes-e-historico" / "decisoes.md").read_text(encoding="utf-8")
FLUXO = {"k": 3, "modelo": "modelo:7b"}

README_FALSO = """# Projeto

[![selo](x)](y)

O projeto em uma frase, **com negrito**.

> Aviso de data.

## O problema

Primeiro problema, da API.

Segundo problema, da tela.

O agente trata os dois.

## Como o agente trabalha

**Como ler:** siga as setas.

**A ideia central:** o modelo opina e o código confere.

## Onde o projeto está

| Fase | A pergunta que ela responde | Estado |
|---|---|---|
| 1 | Temos ambiente? | Concluída |
<!-- comentário
     entre as linhas da tabela -->
| 4 | Funciona na tela? | Em andamento (dois pacotes feitos) |
| 5 | É mais rápido? | Não iniciada |

## O que já descobrimos

Texto de abertura.

### Ler da tela é tão bom quanto ler um caso escrito?

![Barras por versão](Documentacao/figuras/tela.png)

**Como ler:** cada barra é uma versão.

**O que isso mostra:** a tela passou à frente.

Segundo parágrafo da leitura.

### O que ainda não dá para afirmar

- **Que é mais rápido.** Falta medir.
- **Que repete.** Uma repetição só.

## Os dois sistemas de teste

| Sistema | O que é |
|---|---|
| CobaiaFront | Site |
"""


def _corrida(numero: str, nome: str, classe: str):
    return pt.Corrida(numero=numero, nome=nome, comando="comando", tempo="", prerequisito="", fecha="", estado=classe, classe=classe, saida=None)


ROAD = {"data": "11/11/2026",
        "fases": [pt.Fase("1 — Ambiente e cobaias", "Instalador e cobaias", "Concluída — o texto longo do estado da fase um", "concluida"),
                  pt.Fase("4 — Agente na tela", "Interceptador e poda", "Em andamento: o texto longo do estado da fase quatro", "andamento"),
                  pt.Fase("5 — Medição de valor", "MTTR e Task Success", "Não iniciada: o texto longo do estado da fase cinco", "nao_iniciada"),
                  pt.Fase("Documentação", "Memorial e TCC", "Em andamento: o texto longo do estado da documentação", "andamento")],
        "posicao": "Estamos no fim do **Mês 5**.",
        "corridas": [_corrida("16", "**Calibração da Fase 4** — texto comprido", "feita"), _corrida("18b", "**Repetição da corrida 18**: outro texto", "pendente"),
                     _corrida("Q4", "**A fumaça da barra** (Pós-Fase 4)", "feita"), _corrida("99", "**Corrida sem fase**", "pendente")],
        "fora_da_maquina": "Fora da máquina: nada.", "secoes": [("2.9 Corrida 16: primeira leitura", "Texto da leitura.")]}
NAV = [("Visão geral", [("inicio", "Início", "O projeto"), ("roadmap", "Roadmap", "As fases"), ("pendencias", "Pendências", "As fichas")]),
       ("Fase 1", [("f-1", "Fase 1", "A visão da fase 1")]),
       ("Fase 4", [("f-4", "Fase 4", "A visão da fase 4"), ("calibracao", "Calibração", "Quantos verbetes entregar?"), ("tela", "Tela e caso escrito", "O mesmo diagnóstico?")]),
       ("Fase 5", [("f-5", "Fase 5", "A visão da fase 5")]),
       ("Pesquisa e documentação", [("pesquisa", "Pesquisa", "A literatura")])]
FASE = {f["grupo"]: f for f in pf.FASES}


def _cartoes(road, numeros=None, sufixo=""):
    return f'<div class="corridas">{",".join(numeros)}</div>'


def _pagina() -> str:
    return "<main>" + "".join(f'<section id="{sid}" hidden>\n<h1>{nome}</h1>\n</section>\n' for _, abas in NAV for sid, nome, _ in abas) + "</main>"


class TesteLeitura(unittest.TestCase):
    def teste_tabela_do_readme_passa_pelos_comentarios_entre_as_linhas(self):
        self.assertEqual(pf.tabela_do_readme(README_FALSO), {"1": ("Temos ambiente?", "Concluída"), "4": ("Funciona na tela?", "Em andamento (dois pacotes feitos)"),
                                                            "5": ("É mais rápido?", "Não iniciada")})

    def teste_apresentacao_problema_e_ideia_central(self):
        self.assertEqual(pf.apresentacao_do_readme(README_FALSO), "O projeto em uma frase, **com negrito**.")
        self.assertEqual(pf.problema_do_readme(README_FALSO), ["Primeiro problema, da API.", "Segundo problema, da tela.", "O agente trata os dois."])
        self.assertEqual(pf.ideia_central_do_readme(README_FALSO), "o modelo opina e o código confere.")

    def teste_descobertas_e_limites(self):
        achados = pf.descobertas_do_readme(README_FALSO)
        self.assertEqual(achados, [{"pergunta": "Ler da tela é tão bom quanto ler um caso escrito?", "figura": "Documentacao/figuras/tela.png", "alt": "Barras por versão",
                                    "como_ler": "cada barra é uma versão.", "mostra": ["a tela passou à frente.", "Segundo parágrafo da leitura."]}])
        self.assertEqual(pf.limites_do_readme(README_FALSO), ["**Que é mais rápido.** Falta medir.", "**Que repete.** Uma repetição só."])

    def teste_readme_real_tem_o_que_o_painel_le(self):
        tabela = pf.tabela_do_readme(README_REAL)
        self.assertEqual([f["readme"] for f in pf.FASES if f["readme"] not in tabela], [], "fase sem linha na tabela do README")
        achados = pf.descobertas_do_readme(README_REAL)
        self.assertEqual({a["pergunta"] for a in achados}, set(pf.DESCOBERTAS), "toda descoberta do README precisa de uma fase e de uma aba, e nenhuma pode sobrar")
        for a in achados:
            self.assertTrue(a["como_ler"] and a["mostra"], a["pergunta"])
            self.assertTrue((RAIZ / a["figura"]).is_file(), a["figura"])
        self.assertTrue(pf.limites_do_readme(README_REAL))
        self.assertEqual(len(pf.problema_do_readme(README_REAL)), 3)
        self.assertTrue(pf.apresentacao_do_readme(README_REAL).startswith("Trabalho de Conclusão de Curso"))
        self.assertTrue(pf.ideia_central_do_readme(README_REAL))
        cobaias = pf.cobaias_do_readme(README_REAL)
        self.assertEqual(cobaias.count("<h3>"), 2, "um cartão para cada sistema de teste")
        self.assertIn("CobaiaFront", cobaias)
        self.assertIn('<span class="rotulo">Para que serve</span>', cobaias)
        self.assertLess(cobaias.index("<p>"), cobaias.index('<div class="problema cobaias">'), "o parágrafo que apresenta os sistemas vem antes dos cartões")

    def teste_roadmap_real_tem_linha_para_cada_fase_e_fase_para_cada_corrida(self):
        self.assertEqual([f["grupo"] for f in pf.FASES if pf.linha_do_roadmap(ROAD_REAL, f) is None], [])
        self.assertEqual([c.numero for c in ROAD_REAL["corridas"] if pf.fase_da_corrida(c.numero) is None], [], "corrida do roadmap sem fase: acrescentar em FAIXAS_DE_CORRIDAS")
        linhas = [pf.linha_do_roadmap(ROAD_REAL, f).nome for f in pf.FASES]
        self.assertEqual(len(linhas), len(set(linhas)), "duas fases não podem cair na mesma linha do roadmap")

    def teste_fase_da_corrida(self):
        casos = {"1": "Fase 3-B", "10": "Fase 3-B", "12": "Pré-Fase 4", "14": "Fase 3-B", "18b": "Fase 4", "24": "Fase 4", "25": "Pós-Fase 4", "Q4": "Pós-Fase 4", "99": None, "": None}
        for numero, grupo in casos.items():
            self.assertEqual(pf.fase_da_corrida(numero), grupo, numero)

    def teste_fluxo_e_figura_lidos_dos_arquivos(self):
        fluxo = pf.ler_fluxo()
        self.assertIsInstance(fluxo["k"], int)
        self.assertTrue(fluxo["modelo"])
        self.assertTrue(pf.carregar_figura("Documentacao/figuras/como-o-agente-trabalha.png").startswith("data:image/png;base64,"))
        self.assertIsNone(pf.carregar_figura("Documentacao/figuras/nao-existe.png"))
        self.assertIsNone(pf.carregar_figura("../fora-do-projeto.png"))
        self.assertIsNone(pf.carregar_figura("README.md"))


class TesteNavegacao(unittest.TestCase):
    def teste_ordem_das_abas_e_dos_grupos(self):
        h = pf.html_navegacao(NAV, ROAD)
        self.assertEqual(re.findall(r'data-alvo="([^"]+)"', h), [sid for _, abas in NAV for sid, _, _ in abas])
        self.assertEqual(re.findall(r'data-grupo="([^"]+)"', h), [g for g, _ in NAV])

    def teste_fase_e_cabecalho_com_estado_e_as_abas_ficam_recuadas(self):
        h = pf.html_navegacao(NAV, ROAD)
        fase4 = h[h.index('data-grupo="Fase 4"'):h.index('data-grupo="Fase 5"')]
        self.assertIn('class="nav-grupo nav-fase andamento"', h[h.index('data-grupo="Fase 4"') - 60:h.index('data-grupo="Fase 4"')])
        self.assertRegex(fase4, r'<button class="fase-topo" data-alvo="f-4"[^>]*title="Em andamento">')
        self.assertIn('<span class="rot">Fase 4</span><span class="nome">Agente na tela</span><span class="qtd" aria-hidden="true">2</span>', fase4)
        sub = fase4[fase4.index('<div class="nav-sub">'):]
        self.assertEqual(re.findall(r'data-alvo="([^"]+)"', sub), ["calibracao", "tela"])
        fase1 = h[h.index('data-grupo="Fase 1"'):h.index('data-grupo="Fase 4"')]
        self.assertIn('<span class="qtd" aria-hidden="true"></span>', fase1, "fase só com a visão não mostra contagem")
        self.assertIn("nav-fase concluida", h)
        self.assertIn("nav-fase nao_iniciada", h)

    def teste_grupo_geral_tem_titulo_e_nao_tem_cabecalho_de_fase(self):
        h = pf.html_navegacao(NAV, ROAD)
        geral = h[:h.index('data-grupo="Fase 1"')]
        self.assertIn('<span class="grupo">Visão geral</span>', geral)
        self.assertNotIn("fase-topo", geral)
        self.assertEqual(h.count('class="fase-topo"'), 3)

    def teste_faixa_de_sub_abas_entra_em_toda_aba_de_fase(self):
        saida = pf.com_trilho(_pagina(), NAV, ROAD)
        for sid in ("f-1", "f-4", "calibracao", "tela", "f-5"):
            ini = saida.index(f'<section id="{sid}" hidden>') + len(f'<section id="{sid}" hidden>')
            self.assertTrue(saida[ini:].lstrip().startswith('<nav class="trilho'), sid)
        for sid in ("inicio", "roadmap", "pendencias", "pesquisa"):
            ini = saida.index(f'<section id="{sid}" hidden>')
            self.assertNotIn("trilho", saida[ini:saida.index("</section>", ini)], sid)
        faixa = saida[saida.index('<section id="tela"'):]
        faixa = faixa[:faixa.index("</nav>")]
        self.assertIn('<nav class="trilho andamento" aria-label="Abas da Fase 4">', faixa)
        self.assertEqual(re.findall(r'<button data-alvo="([^"]+)"( class="aqui")?>([^<]+)</button>', faixa),
                         [("f-4", "", "Visão da fase"), ("calibracao", "", "Calibração"), ("tela", ' class="aqui"', "Tela e caso escrito")])
        self.assertIn('<span class="chip andamento">Em andamento</span>', faixa)
        self.assertEqual(pf.com_trilho(saida, NAV, ROAD), saida, "aplicar duas vezes dá o mesmo")


class TesteRoadmap(unittest.TestCase):
    def teste_cartao_em_linha_com_pergunta_estado_e_saiba_mais(self):
        h = pf.cartoes_do_roadmap(NAV, ROAD, pf.tabela_do_readme(README_FALSO))
        self.assertEqual(h.count('<article class="linha-fase'), 4, "três fases e a linha da documentação")
        fase4 = h[h.index('<article class="linha-fase andamento">'):]
        fase4 = fase4[:fase4.index("</article>")]
        self.assertIn("<b>Fase 4</b><small>Agente na tela</small>", fase4)
        self.assertIn('<span class="rotulo">A pergunta que ela responde</span>Funciona na tela?', fase4)
        self.assertIn('<span class="rotulo">O que é</span>Interceptador e poda', fase4)
        self.assertIn('<span class="rotulo">Estado</span>Em andamento (dois pacotes feitos)', fase4)
        self.assertIn('<a class="saiba-mais" href="#f-4" data-ir="f-4|">Saiba mais</a><small>2 tópicos · 2 corridas</small>', fase4)

    def teste_texto_longo_do_estado_fica_fora_do_cartao_da_fase(self):
        h = pf.cartoes_do_roadmap(NAV, ROAD, pf.tabela_do_readme(README_FALSO))
        for trecho in ("o texto longo do estado da fase um", "o texto longo do estado da fase quatro", "o texto longo do estado da fase cinco"):
            self.assertNotIn(trecho, h)
        fase1 = h[h.index('<article class="linha-fase concluida">'):]
        fase1 = fase1[:fase1.index("</article>")]
        self.assertNotIn('<span class="rotulo">Estado</span>', fase1, "quando o README diz só a etiqueta, ela não é repetida")
        self.assertIn('<span class="chip concluida">Concluída</span>', fase1)

    def teste_linha_que_nao_e_fase_vem_no_fim_com_o_estado_recolhido(self):
        h = pf.cartoes_do_roadmap(NAV, ROAD, pf.tabela_do_readme(README_FALSO))
        ultima = h[h.rindex('<article class="linha-fase'):]
        self.assertIn("<b>Documentação</b>", ultima)
        self.assertIn("<details><summary>Estado completo</summary><p>Em andamento: o texto longo do estado da documentação</p></details>", ultima)
        self.assertNotIn("Saiba mais", ultima)

    def teste_aba_do_roadmap_agrupa_as_corridas_por_fase(self):
        h = pf.secao_roadmap(ROAD, NAV, _cartoes, README_FALSO)
        self.assertTrue(h.startswith('<section id="roadmap" hidden>'))
        self.assertIn('<details class="grupo-corridas" open><summary>Fase 4 <span class="nota">2 corridas: 1 feita, 1 por rodar</span></summary><div class="corridas">16,18b</div></details>', h)
        self.assertIn('<details class="grupo-corridas"><summary>Pós-Fase 4 <span class="nota">1 corrida: 1 feita</span></summary><div class="corridas">Q4</div></details>', h)
        self.assertIn('<details class="grupo-corridas" open><summary>Sem fase</summary><div class="corridas">99</div></details>', h)
        self.assertIn('<details class="secao-roadmap"><summary>2.9 Corrida 16: primeira leitura</summary>', h)
        self.assertIn("Estamos no fim do <strong>Mês 5</strong>.", h)
        self.assertLess(h.index("linhas-fase"), h.index("grupo-corridas"))


class TesteVisaoDaFase(unittest.TestCase):
    def teste_fase_do_agente_traz_o_fluxo_os_topicos_e_as_corridas(self):
        h = pf.secao_fase(FASE["Fase 4"], NAV, ROAD, README_FALSO, FLUXO, figura=lambda rel: "data:image/png;base64,AAAA")
        self.assertTrue(h.startswith('<section id="f-4" hidden>'))
        self.assertIn("<h1>Fase 4: o agente na tela</h1>", h)
        self.assertIn('<p class="pergunta-fase">Funciona na tela?</p>', h)
        self.assertIn('<span class="chip andamento">Em andamento</span> Em andamento (dois pacotes feitos)</p><p class="nota">2 tópicos e 2 corridas no roadmap (1 feita)</p>', h)
        self.assertIn("Separa os 3 verbetes de documentação mais parecidos com o caso.", h)
        self.assertIn("modelo:7b, na própria máquina", h)
        self.assertEqual(len(re.findall(r'<li class="(?:codigo|modelo)">', h)), 6)
        self.assertEqual(h.count('<li class="modelo">'), 1, "só um passo é do modelo")
        self.assertIn('<a class="topico" href="#calibracao" data-ir="calibracao|"><b>Calibração</b><span>Quantos verbetes entregar?</span><em>Abrir</em></a>', h)
        self.assertIn('<a class="topico" href="#tela" data-ir="tela|">', h)
        self.assertIn('<li><span class="numero">16</span><a href="#roadmap" data-ir="roadmap|corrida-16">Calibração da Fase 4</a><span class="chip feita">Feita</span></li>', h)
        self.assertIn('data-ir="roadmap|corrida-18b"', h)
        self.assertNotIn("corrida-Q4", h)
        self.assertIn("<summary>Mais detalhes: o estado completo da fase, como está no roadmap</summary><p>Em andamento: o texto longo do estado da fase quatro</p>", h)

    def teste_passo_so_ganha_atalho_para_aba_que_existe(self):
        h = pf.secao_fase(FASE["Fase 4"], NAV, ROAD, README_FALSO, FLUXO, figura=None)
        self.assertIn('data-ir="calibracao|">ver na aba</a>', h)
        self.assertNotIn('data-ir="reproducao|"', h, "a aba não está na navegação de teste")
        self.assertNotIn('data-ir="cura|"', h)

    def teste_descoberta_da_fase_vem_com_figura_como_ler_e_leitura(self):
        h = pf.secao_fase(FASE["Fase 4"], NAV, ROAD, README_FALSO, FLUXO, figura=lambda rel: "data:image/png;base64,AAAA" if rel == "Documentacao/figuras/tela.png" else None)
        achado = h[h.index('<article class="achado">'):h.index("</article>")]
        self.assertIn("<h3>Ler da tela é tão bom quanto ler um caso escrito?</h3>", achado)
        self.assertIn('<img src="data:image/png;base64,AAAA" alt="Barras por versão">', achado)
        self.assertIn("<strong>Como ler:</strong> cada barra é uma versão.", achado)
        self.assertIn("<p><strong>O que isso mostra:</strong> a tela passou à frente.</p><p>Segundo parágrafo da leitura.</p>", achado)
        self.assertIn('data-ir="tela|">Ver os números na aba</a>', achado)
        sem = pf.secao_fase(FASE["Fase 1"], NAV, ROAD, README_FALSO, FLUXO, figura=None)
        self.assertNotIn("O que a fase mostrou", sem)

    def teste_fase_sem_topico_e_sem_corrida_nao_ganha_os_blocos(self):
        h = pf.secao_fase(FASE["Fase 1"], NAV, ROAD, README_FALSO, FLUXO, figura=None)
        self.assertIn('<ol class="cadeia">', h)
        self.assertEqual(len(re.findall(r'<li class="(?:codigo|modelo|pessoa|saida)">', h)), len(FASE["Fase 1"]["passos"]))
        self.assertIn('<p class="legenda-cadeia">', h)
        self.assertIn("<strong>Como ler:</strong>", h)
        self.assertNotIn("Tópicos desta fase", h)
        self.assertNotIn("Corridas desta fase", h)
        self.assertIn("A aba segue a seção 6.1 do documento do TCC.", h)

    def teste_todas_as_fases_viram_aba(self):
        h = pf.secoes_das_fases(NAV, ROAD_REAL, README_REAL, FLUXO, figura=None)
        self.assertEqual(re.findall(r'<section id="([^"]+)" hidden>', h), [f["sid"] for f in pf.FASES])
        self.assertEqual(h.count("<section"), h.count("</section>"))


class TesteInicio(unittest.TestCase):
    def setUp(self):
        ficha = SimpleNamespace(aberta=True, depende_do_eric=True, id_html="ficha-70", numero=70, titulo="Uma decisão em aberto", campos={"Recomendação": "opção (a)"})
        fechada = SimpleNamespace(aberta=False, depende_do_eric=True, id_html="ficha-1", numero=1, titulo="Fechada", campos={})
        self.pend = [SimpleNamespace(fichas=[ficha, fechada])]
        self.dados = {"vencedor": {"modelo": "modelo:7b", "biblioteca_epoca": 1}}

    def teste_resumo_do_projeto(self):
        h = pf.secao_inicio(self.dados, self.pend, ROAD, NAV, README_FALSO, FLUXO)
        self.assertTrue(h.startswith('<section id="inicio">'), "o Início é a aba que abre: não começa escondida")
        self.assertIn('<p class="lead">O projeto em uma frase, <strong>com negrito</strong>.</p>', h)
        self.assertIn("<h3>Quando a API muda sem avisar</h3><p>Primeiro problema, da API.</p>", h)
        self.assertIn("<h3>O que o agente faz</h3><p>O agente trata os dois.</p>", h)
        self.assertIn('<p class="ideia-central"><strong>A ideia central:</strong> o modelo opina e o código confere.</p>', h)
        self.assertIn("Separa os 3 verbetes", h)
        self.assertIn('<div class="problema cobaias"><div><h3>CobaiaFront</h3><p><span class="rotulo">O que é</span>Site</p></div></div>', h)
        self.assertNotIn("<table", h, "os dois sistemas de teste viram cartões: tabela solta seria recolhida pelo painel como se fosse dado")
        self.assertLess(h.index("<h2>O problema</h2>"), h.index("<h2>Como o agente trabalha</h2>"))
        self.assertLess(h.index("<h2>Como o agente trabalha</h2>"), h.index("<h2>O caminho do projeto</h2>"))
        self.assertLess(h.index("<h2>O caminho do projeto</h2>"), h.index("<h2>O que já descobrimos</h2>"))

    def teste_caminho_do_projeto_tem_todas_as_fases_com_estado_e_pergunta(self):
        h = pf.secao_inicio(self.dados, self.pend, ROAD, NAV, README_FALSO, FLUXO)
        caminho = h[h.index('<ol class="caminho">'):h.index("</ol>", h.index('<ol class="caminho">'))]
        self.assertEqual(re.findall(r'data-ir="([^"|]+)\|"', caminho), [f["sid"] for f in pf.FASES])
        self.assertIn('<li class="andamento"><a href="#f-4" data-ir="f-4|"><b>Fase 4</b><span class="estado">Em andamento</span><span class="q">Funciona na tela?</span></a></li>', caminho)
        self.assertIn('aria-label="1 de 9 fases concluídas, 1 em andamento"', h)

    def teste_cartoes_de_numero(self):
        h = pf.secao_inicio(self.dados, self.pend, ROAD, NAV, README_FALSO, FLUXO)
        self.assertIn("<span>Fase atual</span><b>Fase 4</b><small>Agente na tela</small>", h)
        self.assertIn("<span>Modelo escolhido</span><b>modelo:7b</b>", h)
        self.assertIn("<span>Fichas abertas</span><b>1</b><small>1 esperam decisão</small>", h)
        self.assertIn("<span>Corridas no roadmap</span><b>2 feitas</b><small>2 por rodar</small>", h)

    def teste_descobertas_limites_decisoes_e_corridas(self):
        h = pf.secao_inicio(self.dados, self.pend, ROAD, NAV, README_FALSO, FLUXO)
        self.assertIn('<article class="descoberta"><span class="fase-de">Fase 4</span><h3>Ler da tela é tão bom quanto ler um caso escrito?</h3><p>a tela passou à frente.</p>'
                      '<a href="#f-4" data-ir="f-4|">Ver a figura e a leitura</a></article>', h)
        self.assertIn('<ul class="limites"><li><strong>Que é mais rápido.</strong> Falta medir.</li><li><strong>Que repete.</strong> Uma repetição só.</li></ul>', h)
        self.assertIn('data-ir="pendencias|ficha-70"><span class="numero">70</span> Uma decisão em aberto</a>', h)
        self.assertNotIn("ficha-1\"", h)
        self.assertIn('data-ir="roadmap|corrida-18b">Repetição da corrida 18</a><span class="chip pendente">Pendente</span>', h)
        self.assertNotIn("corrida-16", h, "corrida feita não entra na lista do que falta rodar")
        self.assertIn("<summary>Mapa do painel: todas as abas, por fase</summary>", h)

    def teste_sem_ficha_e_sem_corrida_por_rodar(self):
        road = {**ROAD, "corridas": [c for c in ROAD["corridas"] if c.classe == "feita"]}
        h = pf.secao_inicio(self.dados, [], road, NAV, README_FALSO, FLUXO)
        self.assertIn("Nenhuma decisão em aberto", h)
        self.assertIn("Nenhuma corrida por rodar", h)


class TesteCoerencia(unittest.TestCase):
    def _nav_completa(self):
        ids = {alvo for f in pf.FASES for _, _, _, alvo in pf._passos(f, FLUXO) if alvo} | {alvo for _, alvo in pf.DESCOBERTAS.values()}
        ids |= {alvo for _, _, alvo in [*pf.SAIDAS_DO_AGENTE, pf.TRILHA_DO_AGENTE]}
        nav = [(f["grupo"], [(f["sid"], f["grupo"], "")]) for f in pf.FASES]
        return nav + [("Outras", [(i, i, "") for i in sorted(ids)])]

    def teste_acusa_fase_sem_grupo_visao_fora_do_comeco_e_atalho_para_aba_que_nao_existe(self):
        nav = self._nav_completa()
        self.assertEqual(pf.abas_fora_de_lugar(nav), [])
        sem_fase = [g for g in nav if g[0] != "Fase 3"]
        self.assertTrue(any("Fase 3: a fase não tem grupo" in e for e in pf.abas_fora_de_lugar(sem_fase)))
        trocada = [(g, [("outra", "x", "")] + abas) if g == "Fase 1" else (g, abas) for g, abas in nav]
        self.assertTrue(any("Fase 1: a primeira aba do grupo precisa ser a visão da fase (f-1)" in e for e in pf.abas_fora_de_lugar(trocada)))
        sem_aba = [(g, [a for a in abas if a[0] != "cruzada"]) for g, abas in nav]
        erros = pf.abas_fora_de_lugar(sem_aba)
        self.assertTrue(any("cruzada" in e and "passo" in e for e in erros) and any("cruzada" in e and "descoberta" in e for e in erros), erros)

    def teste_decisoes_citadas_existem(self):
        textos = " ".join(x for f in pf.FASES for _, _, x, _ in pf._passos(f, FLUXO))
        citadas = sorted({int(n) for n in re.findall(r"decisão (\d+)", textos)})
        self.assertTrue(citadas)
        self.assertEqual([n for n in citadas if not re.search(rf"^\| {n} \|", DECISOES, re.MULTILINE)], [])

    def teste_texto_do_modulo_sem_travessao_seta_nome_nem_voce(self):
        textos = [f["titulo"] + " " + f["curto"] for f in pf.FASES] + [t + " " + x for f in pf.FASES for _, t, x, _ in pf._passos(f, FLUXO)]
        textos += [t + " " + x for t, x, _ in [*pf.SAIDAS_DO_AGENTE, pf.TRILHA_DO_AGENTE]] + list(pf.TIPOS.values()) + list(pf.ROTULO_ESTADO.values())
        for texto in textos:
            self.assertNotRegex(texto, r"[—→↔]|\bEric\b|\b[Vv]ocês?\b", texto)
        h = pf.secao_inicio({"vencedor": {"modelo": "m", "biblioteca_epoca": 1}}, [], ROAD, NAV, README_FALSO, FLUXO) + pf.secao_roadmap(ROAD, NAV, _cartoes, README_FALSO)
        self.assertNotRegex(re.sub(r"<[^>]+>", " ", h).replace("1 — Ambiente", "").replace("4 — Agente", "").replace("5 — Medição", ""), r"[—→↔]|\bEric\b|\b[Vv]ocês?\b")

    def teste_estilo_e_script(self):
        for seletor in (".nav-fase", ".fase-topo", ".nav-sub", "nav.trilho", ".linha-fase", ".saiba-mais", ".cadeia", ".caminho", ".descoberta", ".topico", ".linhas-corrida"):
            self.assertIn(seletor, pf.CSS, seletor)
        self.assertIn("window.aoMostrar = function(id)", pf.JS)
        self.assertNotIn("</script>", pf.JS)


# A página gravada por gerar_dashboard.py: a navegação por fase, a faixa de sub-abas, o glossário e a troca por "grupo" juntos, como o leitor recebe.
class TestePaginaGerada(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import painel_glossario as pglos
        import painel_grupo as pg
        import painel_topicos as tp
        cls.pg, cls.pglos, cls.nav = pg, pglos, tp.NAV
        cls.pagina = (RAIZ / "Documentacao" / "dashboard" / "painel-do-projeto.html").read_text(encoding="utf-8")
        ini, fim = cls.pagina.index("<main>"), cls.pagina.index("</main>")
        cls.main = cls.pagina[ini:fim]
        cls.secoes = dict(re.findall(r'<section id="([^"]+)"[^>]*>(.*?)</section>', cls.main, re.DOTALL))

    def teste_toda_aba_da_navegacao_tem_secao_e_toda_secao_tem_aba(self):
        ids = [sid for _, abas in self.nav for sid, _, _ in abas]
        self.assertEqual(sorted(ids), sorted(self.secoes), "aba sem seção, ou seção sem aba")
        self.assertEqual(pf.abas_fora_de_lugar(self.nav), [])

    def teste_aba_de_fase_comeca_pela_faixa_com_as_abas_irmas(self):
        for grupo, abas in self.nav:
            fase = pf.fase_do_grupo(grupo)
            for sid, _, _ in abas:
                corpo = self.secoes[sid].lstrip()
                if fase is None:
                    self.assertFalse(corpo.startswith('<nav class="trilho'), sid)
                    continue
                self.assertTrue(corpo.startswith('<nav class="trilho'), f"{sid}: a aba de fase começa pela faixa de sub-abas")
                faixa = corpo[:corpo.index("</nav>")]
                self.assertEqual(re.findall(r'data-alvo="([^"]+)"', faixa), [s for s, _, _ in abas], sid)
                self.assertEqual(re.findall(r'data-alvo="([^"]+)" class="aqui"', faixa), [sid])

    def teste_visao_de_cada_fase_tem_pergunta_caminho_e_topicos(self):
        perguntas = pf.tabela_do_readme(README_REAL)
        grupos = dict(self.nav)
        for f in pf.FASES:
            corpo = self.secoes[f["sid"]]
            self.assertIn('<p class="pergunta-fase">', corpo, f["sid"])
            self.assertIn(pt.inline(perguntas[f["readme"]][0]), re.sub(r'<span class="termo"[^>]*>|</span>', "", corpo), f["sid"])
            self.assertIn('<ol class="cadeia">', corpo, f["sid"])
            self.assertEqual(len(re.findall(r'<a class="topico" ', corpo)), len(grupos[f["grupo"]]) - 1, f["sid"])
            self.assertIn("Mais detalhes: o estado completo da fase", corpo, f["sid"])

    def teste_descobertas_do_readme_aparecem_com_figura_na_fase(self):
        for a in pf.descobertas_do_readme(README_REAL):
            grupo, _ = pf.DESCOBERTAS[a["pergunta"]]
            corpo = self.secoes[pf.fase_do_grupo(grupo)["sid"]]
            self.assertIn(f'alt="{pf._esc(a["alt"])}"', corpo, a["pergunta"])
        self.assertEqual(self.secoes["inicio"].count('<article class="descoberta">'), len(pf.DESCOBERTAS))

    def teste_roadmap_em_linhas_e_inicio_com_o_resumo_do_projeto(self):
        road = self.secoes["roadmap"]
        self.assertEqual(road.count('<article class="linha-fase'), len(ROAD_REAL["fases"]))
        self.assertEqual(road.count('class="saiba-mais"'), len(pf.FASES))
        self.assertNotIn('<div class="fases">', self.main, "os cartões estreitos e altos das fases saíram")
        for c in ROAD_REAL["corridas"]:
            self.assertEqual(road.count(f'id="corrida-{c.numero}"'), 1, c.numero)
        inicio = self.secoes["inicio"]
        for trecho in ("<h2>O problema</h2>", "<h2>Como o agente trabalha</h2>", '<ol class="caminho">', "<h2>O que já descobrimos</h2>", "<h2>O que ainda não dá para afirmar</h2>"):
            self.assertIn(trecho, inicio)

    def teste_pagina_fala_do_grupo(self):
        self.assertEqual(self.pg.sobras(self.pagina), [], "o painel fala do grupo, e não do autor nem de você")
        texto = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", re.sub(r"<(script|style)\b.*?</\1>", " ", self.main, flags=re.DOTALL)))
        self.assertEqual(re.findall(r"\b(?:[Oo]|[Dd]o|[Pp]elo|[Aa]o|[Nn]o) o grupo\b|\bgrupo grupo\b", texto), [], "artigo dobrado na troca do nome")

    def teste_glossario_marca_os_termos_e_lista_no_fim_de_cada_aba(self):
        ids = {t["id"] for t in self.pglos.TERMOS}
        marcados = re.findall(r'<span class="termo" tabindex="0" data-termo="([^"]+)">', self.main)
        self.assertGreater(len(marcados), 200)
        self.assertEqual(set(marcados) - ids, set())
        for sid, corpo in self.secoes.items():
            termos = re.findall(r'data-termo="([^"]+)"', corpo)
            self.assertEqual(len(termos), len(set(termos)), f"{sid}: cada termo é marcado uma vez por aba")
            if sid == "glossario":
                self.assertEqual(termos, [])
            elif termos:
                self.assertIn(f"Termos e métodos desta aba ({len(termos)})", corpo, sid)
        self.assertIn("window.GLOSSARIO = ", self.pagina)
        for t in self.pglos.TERMOS:
            self.assertEqual(self.secoes["glossario"].count(f'id="termo-{t["id"]}"'), 1, t["id"])
        self.assertNotRegex(self.main, r'<[^<>]*<span class="termo"', "a marca do termo não entra dentro de outra marcação")

    def teste_metodo_citado_no_painel_vem_com_resumo_e_fonte(self):
        por_id = {t["id"]: t for t in self.pglos.TERMOS}
        vistos = set()
        for sid, corpo in self.secoes.items():
            if "termos-da-aba" not in corpo:
                continue
            lista = corpo[corpo.index('<details class="termos-da-aba">'):]
            for termo in re.findall(r'data-ir="glossario\|termo-([^"]+)"', lista):
                t = por_id[termo]
                if t["grupo"] == "metodo":
                    vistos.add(termo)
                    self.assertIn("Neste projeto:", lista, f"{sid}: {termo}")
                    if t["fontes"]:
                        self.assertIn("Fonte:", lista, f"{sid}: {termo}")
        self.assertGreaterEqual(len(vistos), 12, "os métodos citados no painel aparecem nas listas")

    def teste_ids_sem_repeticao(self):
        ids = re.findall(r' id="([^"]+)"', self.pagina)
        self.assertEqual(sorted({i for i in ids if ids.count(i) > 1}), [])


if __name__ == "__main__":
    unittest.main()
