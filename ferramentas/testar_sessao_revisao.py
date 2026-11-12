#!/usr/bin/env python3
# ! Alteração de IA - Revisar: testes da página da sessão de revisão dos relatórios da trilha (05/11/2026): a página não carrega nada
# do resultado dos casos, mostra um relatório por vez, mede o tempo só com o relatório à vista e passa as respostas para a planilha
# revisao_trilha.md com os valores que ela aceita.
# ! Motivo: a adesão apropriada (aceitar o diagnóstico certo e recusar o errado, especificação da trilha, seção 12 c) só vale às cegas e a
# sessão não se repete com o mesmo leitor; um vazamento do gabarito ou um tempo mal medido estragaria a única medida da Fase 4 com revisor humano.
"""Uso: python ferramentas/testar_sessao_revisao.py (a parte do navegador só roda com o Python da .venv, que tem o Playwright)."""
from __future__ import annotations

import json
import re
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import painel_topicos as tp  # noqa: E402
import sessao_revisao as sr  # noqa: E402

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    sync_playwright = None

CABECALHO = ("| # | Caso | Classe | Relatório | Tempo até a decisão (s) | Erro localizado (sim, não, n.a.) | Decisão (aceitar, recusar) | "
             "Utilidade (1 a 5) | Avaliação (certo, errado) | Comentário |")
EM_BRANCO = "(em branco) | (em branco) | (em branco) | (em branco) | (em branco) |  |"


def _planilha(casos: list[str]) -> str:
    linhas = ["<!-- ! Alteração de IA - Revisar: planilha de exemplo.", "     ! Motivo: testes. -->", "# Sessão de revisão dos relatórios da trilha (corrida fase4_trilha)", "",
              "Como preencher, um relatório por vez.", "", CABECALHO, "|---|---|---|---|---|---|---|---|---|---|"]
    linhas += [f"| {i + 1} | `{c}` | {i + 7} | `relatorios_x/{c}@base.md` | {EM_BRANCO}" for i, c in enumerate(casos)]
    return "\n".join(linhas) + "\n"


def _relatorio(caso: str, extra: str = "") -> str:
    return (f"<!-- ! Alteração de IA - Revisar: relatório. -->\n# Caso `{caso}`: o que o agente fez, declarou e conferiu\n\n## 1. Veredito\n\n"
            f"Causa respondida: `tipo_divergente`.\n\n| Campo | Valor |\n|---|---|\n| Selo | médio |\n\n{extra}\n\n## Rastro\n\n- evento 1, `poda`: escolha `x`\n"
            f"- evento 2, `diagnostico`: escolha `y`\n\nSem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.\n\nMARCA_{caso}\n")


def _pasta_de_sessao(raiz: Path, casos: list[str], extra: str = "") -> Path:
    (raiz / "relatorios_x").mkdir(parents=True, exist_ok=True)
    planilha = raiz / "revisao_trilha.md"
    planilha.write_text(_planilha(casos), encoding="utf-8", newline="\n")
    for c in casos:
        (raiz / "relatorios_x" / f"{c}@base.md").write_text(_relatorio(c, extra), encoding="utf-8", newline="\n")
    return planilha


def _como_publicada(pagina: str) -> str:
    """O esqueleto que a publicação põe em volta da página: sem ele o navegador abriria em modo de compatibilidade e sem a codificação certa."""
    return ('<!doctype html><html><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1,viewport-fit=cover">'
            '<style>:root{color-scheme:light;padding-block:env(safe-area-inset-top,0px) env(safe-area-inset-bottom,0px)}body{margin:0;font:14px system-ui}img{max-width:100%}[hidden]{display:none!important}</style>'
            f"</head><body>{pagina}</body></html>")


def _sem_relatorios(pagina: str) -> str:
    return re.sub(r"<template.*?</template>", "", pagina, flags=re.S)


class TesteDaPagina(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.raiz = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def teste_ler_planilha_devolve_as_linhas_na_ordem_sem_as_crases(self):
        planilha = _pasta_de_sessao(self.raiz, ["zeta-2", "alfa-1"])
        linhas = sr.ler_planilha(planilha)
        self.assertEqual([x["caso"] for x in linhas], ["zeta-2", "alfa-1"])
        self.assertEqual([x["posicao"] for x in linhas], [1, 2])
        self.assertEqual(linhas[0]["relatorio"], "relatorios_x/zeta-2@base.md")

    def teste_pagina_tem_um_relatorio_por_caso_na_ordem_e_deixa_a_classe_de_fora(self):
        planilha = _pasta_de_sessao(self.raiz, ["zeta-2", "alfa-1"])
        pagina = sr.pagina(sr.ler_planilha(planilha), planilha.parent)
        casos = json.loads(re.search(r'<script type="application/json" id="casos">(.*?)</script>', pagina, re.S).group(1))
        self.assertEqual(casos, [{"posicao": 1, "caso": "relatorio-1"}, {"posicao": 2, "caso": "relatorio-2"}])
        for i, c in enumerate(["zeta-2", "alfa-1"]):
            self.assertEqual(pagina.count(f"MARCA_{c}"), 1, c)
            self.assertRegex(pagina, rf'(?s)<template id="rel-{i}">.*MARCA_{c}.*?</template>')
        self.assertNotIn("MARCA_", _sem_relatorios(pagina), "um relatório fora do template apareceria antes de o cronômetro ligar")

    def teste_pagina_nao_le_nada_do_resultado_que_esta_ao_lado_da_planilha(self):
        planilha = _pasta_de_sessao(self.raiz, ["zeta-2"])
        (self.raiz / "trilha.json").write_text('{"casos": [{"caso": "zeta-2", "acerto": false, "gabarito": "SEGREDO_DO_GABARITO"}]}', encoding="utf-8")
        (self.raiz / "trilha.md").write_text("SEGREDO_DO_GABARITO", encoding="utf-8")
        self.assertNotIn("SEGREDO_DO_GABARITO", sr.pagina(sr.ler_planilha(planilha), planilha.parent))

    def teste_pagina_recusa_relatorio_que_traga_o_resultado_e_aceita_a_frase_fixa_sem_gabarito(self):
        for trecho in ("causa_correta: tipo_divergente", "verbete_de_ouro_no_contexto", "Causa esperada: tipo_divergente", "| causa_esperada | x |", "O agente acertou este caso."):
            planilha = _pasta_de_sessao(self.raiz, ["zeta-2"], extra=trecho)
            with self.assertRaises(ValueError, msg=trecho) as erro:
                sr.pagina(sr.ler_planilha(planilha), planilha.parent)
            self.assertIn("zeta-2", str(erro.exception))
        planilha = _pasta_de_sessao(self.raiz, ["zeta-2"], extra="O contrato esperado pela tela e nulo_inesperado são textos do próprio caso.")
        self.assertIn("MARCA_zeta-2", sr.pagina(sr.ler_planilha(planilha), planilha.parent))

    # ! Alteração de IA - Revisar: (08/11/2026, Pós-Fase 4, pacote Q5) o perfil v3 da página: os textos da sessão da corrida 24 (relatórios v3 com a árvore de decisão,
    # planilha revisao_v3.md) no lugar dos da corrida 22, e a frase da taxa da faixa de confiança aceita só nesse perfil.
    # ! Motivo: a ficha 40 foi fechada pela opção (b) e a sessão com revisor humano roda nesta mesma página; a árvore diz "acertou a causa em N de M" sobre a corrida de
    # calibração (decisão 110), que não é o resultado do caso, e o perfil da corrida 22 continua recusando qualquer "acertou".
    def teste_perfil_v3_troca_os_textos_da_sessao_e_aceita_a_taxa_da_faixa_na_arvore(self):
        planilha = _pasta_de_sessao(self.raiz, ["zeta-2"], extra="Na calibração, dos 26 casos da faixa média, o agente acertou a causa em 22 de 26: 84,6% (observado).")
        with self.assertRaises(ValueError):
            sr.pagina(sr.ler_planilha(planilha), planilha.parent)
        pagina = sr.pagina(sr.ler_planilha(planilha), planilha.parent, perfil=sr.PERFIL_V3)
        self.assertIn("MARCA_zeta-2", pagina)
        for trecho in ("Revisão dos relatórios v3 e das árvores de decisão", "corrida 24", "revisao_v3.md", "ineditos.json", "bloco 12, Veredito do agente", "sessao_revisao_v3_v1", "1 relatórios"):
            self.assertIn(trecho, pagina, trecho)
        for trecho in ("corrida 22", "revisao_trilha.md", "trilha.json", "sessao_revisao_trilha_v1", "@@"):
            self.assertNotIn(trecho, pagina, trecho)
        casos = json.loads(re.search(r'<script type="application/json" id="casos">(.*?)</script>', pagina, re.DOTALL).group(1))
        self.assertEqual(casos, [{"posicao": 1, "caso": "relatorio-1"}])
        antiga = sr.pagina(sr.ler_planilha(_pasta_de_sessao(self.raiz, ["zeta-2"])), planilha.parent)
        for trecho in ("corrida 22", "revisao_trilha.md", "sessao_revisao_trilha_v1", "seção 1, Veredito"):
            self.assertIn(trecho, antiga, trecho)

    def teste_pagina_para_quando_falta_um_relatorio(self):
        planilha = _pasta_de_sessao(self.raiz, ["zeta-2"])
        (self.raiz / "relatorios_x" / "zeta-2@base.md").unlink()
        with self.assertRaises(FileNotFoundError):
            sr.pagina(sr.ler_planilha(planilha), planilha.parent)

    def teste_conteudo_do_relatorio_nao_vira_marcacao_da_pagina(self):
        extra = "Corpo: </template><script>alert(1)</script>\n\n```\n</template><img src=x onerror=alert(2)>\n```"
        planilha = _pasta_de_sessao(self.raiz, ["zeta-2", "alfa-1"], extra=extra)
        pagina = sr.pagina(sr.ler_planilha(planilha), planilha.parent)
        self.assertEqual(pagina.count("</template>"), 2)
        self.assertNotIn("<script>alert", pagina)
        self.assertNotIn("<img src=x", pagina)

    def teste_pagina_cumpre_o_contrato_do_artefato_e_a_regra_de_texto_do_projeto(self):
        planilha = _pasta_de_sessao(self.raiz, ["zeta-2"])
        pagina = sr.pagina(sr.ler_planilha(planilha), planilha.parent)
        self.assertTrue(pagina.startswith("<title>"), "o título precisa estar no início do arquivo")
        for trecho in ('<meta name="claude:viewport-fit-sides" content="cover">', "padding-left:max(16px,env(safe-area-inset-left,0px))",
                       "padding-right:max(16px,env(safe-area-inset-right,0px))", ":root:not([data-theme=light])", ":root[data-theme=dark]",
                       "! Alteração de IA - Revisar", "! Motivo:", 'collection("respostas")', "font-variant-numeric:tabular-nums"):
            self.assertIn(trecho, pagina, trecho)
        casca = _sem_relatorios(pagina)
        for proibido in ("<html", "<body", "<!doctype", "—", "→", "alert(", "confirm(", "prompt(", "window.print", "Classe", "gabarito"):
            self.assertNotIn(proibido, casca, proibido)

    # ! Alteração de IA - Revisar: (05/11/2026) a página troca o nome do caso por relatorio-N em todo lugar e tira o comando de reexecução.
    # ! Motivo: o prefixo do nome diz a família do defeito e reduz as 23 causas possíveis a 3 a 6; um analista de verdade não teria esse nome, e o revisor julgaria com uma pista a mais.
    def teste_pagina_troca_o_nome_do_caso_por_um_neutro_em_todo_lugar(self):
        extra = ("Trilha `fase4_trilha/qwen2.5_7b/zeta-2@base`; modelo x.\n\nComando para reexecutar o caso: `python executar_fase4.py --ids zeta-2 --sem-seletor`\n\n"
                 "| 1207 | 1 | entrada | programa | ao_vivo | t | caso zeta-2 |\n\nO caso zeta-20 é outro.")
        planilha = _pasta_de_sessao(self.raiz, ["zeta-2"], extra=extra)
        pagina = sr.pagina(sr.ler_planilha(planilha), planilha.parent)
        sem_marca = pagina.replace("MARCA_zeta-2", "").replace("zeta-20", "")
        self.assertNotIn("zeta-2", sem_marca)
        self.assertIn("fase4_trilha/qwen2.5_7b/relatorio-1@base", pagina)
        self.assertIn("caso relatorio-1", pagina)
        self.assertIn("Caso <code>relatorio-1</code>", pagina)
        self.assertNotIn("Comando para reexecutar", pagina)
        self.assertIn("zeta-20", pagina, "um nome que só começa igual não é o nome do caso")

    def teste_pagina_recusa_relatorio_que_cite_o_nome_de_outro_caso(self):
        planilha = _pasta_de_sessao(self.raiz, ["zeta-2"], extra="Parecido com run-7.")
        with self.assertRaises(ValueError) as erro:
            sr.pagina(sr.ler_planilha(planilha), planilha.parent)
        self.assertIn("zeta-2", str(erro.exception))

    # ! Alteração de IA - Revisar: (05/11/2026) a pergunta sobre o erro explica o que marcar quando o diagnóstico parece certo, e a página deixa de se dizer às cegas.
    # ! Motivo: na primeira resposta real, o revisor aceitou o diagnóstico, avaliou como certo e marcou que achou o erro, o que sugere ter lido "erro" como o defeito do sistema; e, a partir do relatório 2, ele lê a pré-análise do Claude antes de decidir, então "às cegas" deixou de ser verdade.
    def teste_pagina_explica_a_pergunta_do_erro_e_nao_se_diz_as_cegas(self):
        planilha = _pasta_de_sessao(self.raiz, ["zeta-2"])
        pagina = sr.pagina(sr.ler_planilha(planilha), planilha.parent)
        self.assertIn("Se o diagnóstico parece certo, marque Não vi erro.", pagina)
        casca = _sem_relatorios(pagina).lower()
        self.assertNotIn("às cegas", casca)

    def teste_relatorio_com_lista_vira_itens_e_nao_um_paragrafo_so(self):
        saida = tp._relatorio_para_html("Antes da lista.\n- evento 1: `a`\n- evento 2: `b`\n\nDepois da lista.")
        self.assertIn("<p>Antes da lista.</p>", saida)
        self.assertEqual(saida.count("<li>"), 2)
        self.assertIn("<p>Depois da lista.</p>", saida)

    @unittest.skipUnless(sr.PLANILHA.exists(), "planilha real ausente")
    def teste_pagina_real_sai_da_planilha_real(self):
        linhas = sr.ler_planilha(sr.PLANILHA)
        pagina = sr.pagina(linhas, sr.PLANILHA.parent)
        self.assertEqual(pagina.count('<template id="rel-'), len(linhas))
        self.assertEqual(sr.RE_NOME_DE_CASO.findall(pagina), [], "nenhum nome real de caso na página")
        self.assertGreater(len(linhas), 0)


def _resposta(posicao: int, **muda) -> dict:
    base = {"posicao": posicao, "caso": f"relatorio-{posicao}", "segundos": 143, "segundos_relogio": 150, "pausas": 0, "retomadas": 0, "decisao": "aceitar", "erro_localizado": "n.a.",
            "utilidade": 4, "avaliacao": "certo", "comentario": ""}
    return {**base, **muda}


class TesteDaGravacao(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.planilha = _pasta_de_sessao(Path(self._tmp.name), ["zeta-2", "alfa-1"])
        self.original = self.planilha.read_text(encoding="utf-8")

    def tearDown(self):
        self._tmp.cleanup()

    def teste_gravar_preenche_so_as_celulas_do_revisor(self):
        faltam = sr.gravar_respostas(self.planilha, [_resposta(1, comentario="na seção 2 | linha um\nlinha dois")])
        self.assertEqual(faltam, ["alfa-1"])
        texto = self.planilha.read_text(encoding="utf-8")
        self.assertIn("| 1 | `zeta-2` | 7 | `relatorios_x/zeta-2@base.md` | 143 | n.a. | aceitar | 4 | certo | na seção 2 / linha um linha dois |", texto)
        self.assertIn(f"| 2 | `alfa-1` | 8 | `relatorios_x/alfa-1@base.md` | {EM_BRANCO}", texto)
        self.assertEqual(texto.split("| 1 |")[0], self.original.split("| 1 |")[0], "o cabeçalho da planilha não muda")

    def teste_gravar_com_todas_as_respostas_deixa_a_planilha_preenchida_e_comentario_vazio_no_formato_original(self):
        faltam = sr.gravar_respostas(self.planilha, [_resposta(1), _resposta(2, decisao="recusar", erro_localizado="não", avaliacao="errado", utilidade=2)])
        self.assertEqual(faltam, [])
        texto = self.planilha.read_text(encoding="utf-8")
        self.assertNotIn("(em branco)", texto)
        self.assertIn("| 2 | `alfa-1` | 8 | `relatorios_x/alfa-1@base.md` | 143 | não | recusar | 2 | errado |  |", texto)

    def teste_gravar_recusa_valor_que_a_planilha_nao_aceita_e_nao_muda_o_arquivo(self):
        ruins = [_resposta(99), _resposta(1, caso="relatorio-2"), _resposta(1, decisao="talvez"), _resposta(1, erro_localizado="nao"), _resposta(1, utilidade=6),
                 _resposta(1, utilidade="4"), _resposta(1, avaliacao=""), _resposta(1, segundos=-1), _resposta(1, segundos=1.5), _resposta(1, segundos=True)]
        for ruim in ruins:
            with self.assertRaises(ValueError, msg=str(ruim)):
                sr.gravar_respostas(self.planilha, [_resposta(2), ruim])
            self.assertEqual(self.planilha.read_text(encoding="utf-8"), self.original, str(ruim))

    # ! Alteração de IA - Revisar: (05/11/2026, decisão 86) a gravação aceita o parecer do Claude aprovado pelo Eric, sem tempo medido e marcado como tal.
    # ! Motivo: o Eric aprovou o parecer para os relatórios 2 a 11 sem responder na página; o tempo não existe e não pode virar número, e uma resposta sem tempo e sem essa marca continua sendo erro.
    def teste_gravar_aceita_parecer_aprovado_sem_tempo_e_recusa_resposta_comum_sem_tempo(self):
        parecer = """| # | Relatório | Causa do agente | Selo | Erro localizado | Decisão | Utilidade | Avaliação | Causa que eu daria | Confiança |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `relatorio-1` | `causa_x` | alto | n.a. | aceitar | 3 | certo | a mesma | alta |
| 2 | `relatorio-2` | `causa_x` | alto | n.a. | aceitar | 3 | certo | a mesma | alta |
| 3 | `relatorio-3` | `causa_y` | alto | n.a. | recusar | 3 | errado | `causa_k` | média |
| 4 | `relatorio-4` | `causa_z` | baixo | sim | recusar | 4 | errado | `causa_y` | alta |
| 5 | `relatorio-5` | `causa_z` | alto | não | aceitar | 2 | certo | a mesma | média |
"""
        respostas = sr.respostas_do_parecer(parecer, desde=2, comentario="Parecer aprovado")
        self.assertEqual([r["posicao"] for r in respostas], [2, 3, 4, 5])
        self.assertEqual((respostas[0]["caso"], respostas[0]["segundos"], respostas[0]["origem"], respostas[0]["decisao"], respostas[0]["utilidade"], respostas[0]["comentario"]), ("relatorio-2", None, sr.ORIGEM_PARECER, "aceitar", 3, "Parecer aprovado"))
        self.assertEqual((respostas[2]["erro_localizado"], respostas[2]["avaliacao"]), ("sim", "errado"))
        sr.gravar_respostas(self.planilha, [_resposta(1), respostas[0]])
        texto = self.planilha.read_text(encoding="utf-8")
        self.assertIn(f"| 2 | `alfa-1` | 8 | `relatorios_x/alfa-1@base.md` | {sr.TEMPO_NAO_MEDIDO} | n.a. | aceitar | 3 | certo | Parecer aprovado |", texto)
        self.assertIn("| 1 | `zeta-2` | 7 | `relatorios_x/zeta-2@base.md` | 143 |", texto)
        with self.assertRaises(ValueError):
            sr.gravar_respostas(self.planilha, [_resposta(1, segundos=None)], corrigir=True)

    # ! Alteração de IA - Revisar: (10/11/2026) a gravação aceita a resposta de um analista, colada pelo Eric, sem tempo medido e marcada com a origem "analista".
    # ! Motivo: na sessão de 09 e 10/11/2026 o Eric passou os relatórios a um analista e colou na página o que ele respondeu; o tempo que a página mediu nesses
    # relatórios é o da troca entre os dois, não o de uma leitura, e não pode entrar na planilha como tempo até a decisão.
    def teste_gravar_aceita_resposta_de_um_analista_sem_tempo_e_troca_a_linha_ja_preenchida_so_com_corrigir(self):
        sr.gravar_respostas(self.planilha, [_resposta(1), _resposta(2, segundos=31, comentario="texto do analista")])
        do_analista = _resposta(2, segundos=None, origem=sr.ORIGEM_ANALISTA, comentario="texto do analista")
        with self.assertRaises(ValueError):
            sr.gravar_respostas(self.planilha, [do_analista])
        sr.gravar_respostas(self.planilha, [do_analista], corrigir=True)
        texto = self.planilha.read_text(encoding="utf-8")
        self.assertIn(f"| 2 | `alfa-1` | 8 | `relatorios_x/alfa-1@base.md` | {sr.TEMPO_NAO_MEDIDO} | n.a. | aceitar | 4 | certo | texto do analista |", texto)
        self.assertIn("| 1 | `zeta-2` | 7 | `relatorios_x/zeta-2@base.md` | 143 |", texto)
        self.assertIn(sr.ORIGEM_ANALISTA, sr.ORIGENS_SEM_TEMPO)
        with self.assertRaises(ValueError):
            sr.gravar_respostas(self.planilha, [_resposta(1, segundos=None, origem="outra")], corrigir=True)

    @unittest.skipUnless((sr.PLANILHA.parent / "pre_analise_revisao_trilha.md").exists(), "pré-análise real ausente")
    def teste_parecer_real_cobre_os_relatorios_da_planilha_com_valores_aceitos(self):
        respostas = sr.respostas_do_parecer((sr.PLANILHA.parent / "pre_analise_revisao_trilha.md").read_text(encoding="utf-8"), desde=1, comentario="x")
        self.assertEqual([r["posicao"] for r in respostas], [x["posicao"] for x in sr.ler_planilha(sr.PLANILHA)])
        self.assertEqual([sr._erros_da_resposta(r) for r in respostas], [[] for _ in respostas])

    def teste_gravar_nao_sobrescreve_linha_preenchida_sem_pedir(self):
        sr.gravar_respostas(self.planilha, [_resposta(1)])
        sr.gravar_respostas(self.planilha, [_resposta(1)])
        with self.assertRaises(ValueError) as erro:
            sr.gravar_respostas(self.planilha, [_resposta(1, decisao="recusar")])
        self.assertIn("relatório 1", str(erro.exception))
        sr.gravar_respostas(self.planilha, [_resposta(1, decisao="recusar")], corrigir=True)
        self.assertIn("| 143 | n.a. | recusar | 4 | certo |  |", self.planilha.read_text(encoding="utf-8"))


_BANCO_FALSO = """
(() => {
  const CHAVE = 'banco_falso';
  const ler = () => JSON.parse(localStorage.getItem(CHAVE) || '{}');
  const ouvintes = new Set();
  const foto = () => { const o = ler(); const docs = Object.keys(o).sort().map(id => ({id, exists: true, data: () => o[id], metadata: {fromCache: false, hasPendingWrites: false}}));
    return {docs, size: docs.length, empty: docs.length === 0, docChanges: () => [], metadata: {fromCache: false, hasPendingWrites: false}}; };
  window.__falhas = 0;
  const colecao = (nome) => ({
    path: nome,
    doc: (id) => ({id, path: nome + '/' + id, set: async (d) => {
      if (window.__falhas > 0) { window.__falhas -= 1; throw {code: 'unavailable', message: 'banco fora do ar'}; }
      const o = ler(); o[id] = d; localStorage.setItem(CHAVE, JSON.stringify(o)); ouvintes.forEach(f => f(foto()));
    }}),
    onSnapshot: (f, e) => { ouvintes.add(f); setTimeout(() => f(foto()), 0); return () => ouvintes.delete(f); },
  });
  window.claude = {use: async (n) => n === 'db' ? {collection: colecao} : null};
})();
"""
_SEM_BANCO = "window.claude = {use: async () => null};"
_LONGO = ("`" + "resultados_alvo/fase4/relatorios_revisao_trilha/" * 3 + "`\n\n" + "| " + " | ".join(f"coluna_larga_{i}" for i in range(14)) + " |\n|" + "---|" * 14 + "\n| " + " | ".join("valor" for _ in range(14)) + " |\n\n"
          "```\n" + '{"corpo": "' + "x" * 400 + '"}' + "\n```\n\n" + "\n\n".join(f"Parágrafo {i} do relatório, para dar altura à leitura." for i in range(40)))


@unittest.skipUnless(sync_playwright, "sem Playwright neste Python")
class TesteNoNavegador(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._tmp = tempfile.TemporaryDirectory()
        planilha = _pasta_de_sessao(Path(cls._tmp.name), ["zeta-2", "alfa-1", "beta-3"], extra=_LONGO)
        cls.arquivo = Path(cls._tmp.name) / "pagina.html"
        cls.arquivo.write_text(_como_publicada(sr.pagina(sr.ler_planilha(planilha), planilha.parent)), encoding="utf-8", newline="\n")
        cls._pw = sync_playwright().start()
        cls._navegador = cls._pw.chromium.launch()

    @classmethod
    def tearDownClass(cls):
        cls._navegador.close()
        cls._pw.stop()
        cls._tmp.cleanup()

    def _abrir(self, script: str = _BANCO_FALSO, largura: int = 1300, altura: int = 900, preparo: str | None = None):
        ctx = self._navegador.new_context(viewport={"width": largura, "height": altura})
        self.addCleanup(ctx.close)
        ctx.route("http*://**", lambda r: r.abort())
        ctx.add_init_script(script)
        pg = ctx.new_page()
        self.erros: list[str] = []
        pg.on("pageerror", lambda e: self.erros.append(str(e)))
        if preparo:
            # o preparo roda uma vez só, antes de a página abrir, e não a cada recarga
            pg.goto(self.arquivo.as_uri(), wait_until="domcontentloaded")
            pg.evaluate(preparo)
        pg.goto(self.arquivo.as_uri(), wait_until="domcontentloaded")
        pg.wait_for_function("document.getElementById('palco').dataset.pronta === 'sim'")
        return pg

    def _docs(self, pg) -> dict:
        return pg.evaluate("JSON.parse(localStorage.getItem('banco_falso') || '{}')")

    def _visivel(self, pg, seletor: str) -> bool:
        return pg.locator(seletor).is_visible()

    def _completar(self, pg, erro="na", utilidade=4, avaliacao="certo", comentario=""):
        pg.click(f'label[for="erro-{erro}"]')
        pg.click(f'label[for="util-{utilidade}"]')
        pg.click(f'label[for="aval-{avaliacao}"]')
        if comentario:
            pg.fill("#comentario", comentario)

    def _um_relatorio_inteiro(self, pg, decisao="aceitar", **respostas):
        pg.click("#abrir")
        pg.click(f"#{decisao}")
        self._completar(pg, **respostas)
        pg.click("#salvar")

    def teste_relatorio_so_aparece_depois_de_abrir_e_a_resposta_chega_ao_banco(self):
        pg = self._abrir()
        self.assertTrue(self._visivel(pg, "#comecar"))
        self.assertEqual(pg.get_by_text("MARCA_zeta-2").count(), 0)
        pg.click("#comecar")
        self.assertTrue(self._visivel(pg, "#abrir"))
        self.assertEqual(pg.get_by_text("MARCA_zeta-2").count(), 0)
        pg.click("#abrir")
        self.assertTrue(pg.get_by_text("MARCA_zeta-2").is_visible())
        pg.wait_for_timeout(1300)
        pg.click("#recusar")
        pg.click("#salvar")
        self.assertIn("Falta responder", pg.inner_text("#mensagem"))
        self.assertEqual(self._docs(pg), {})
        self._completar(pg, erro="sim", utilidade=2, avaliacao="errado", comentario="na seção 2")
        pg.click("#salvar")
        pg.wait_for_function("Object.keys(JSON.parse(localStorage.getItem('banco_falso') || '{}')).length === 1")
        doc = self._docs(pg)["relatorio-1"]
        self.assertEqual((doc["posicao"], doc["caso"], doc["decisao"], doc["erro_localizado"], doc["utilidade"], doc["avaliacao"], doc["comentario"]), (1, "relatorio-1", "recusar", "sim", 2, "errado", "na seção 2"))
        self.assertGreaterEqual(doc["segundos"], 1)
        self.assertLessEqual(doc["segundos"], 3)
        self.assertEqual((doc["pausas"], doc["retomadas"]), (0, 0))
        self.assertTrue(self._visivel(pg, "#abrir"), "depois de salvar, o próximo relatório fica esperando o clique")
        self.assertEqual(pg.get_by_text("MARCA_alfa-1").count(), 0)
        self.assertEqual(self.erros, [])

    def teste_pausa_esconde_o_relatorio_e_nao_conta_tempo(self):
        pg = self._abrir()
        pg.click("#comecar")
        pg.click("#abrir")
        pg.click("#pausar")
        self.assertFalse(self._visivel(pg, "#relatorio"))
        pg.wait_for_timeout(2200)
        pg.click("#continuar")
        self.assertTrue(self._visivel(pg, "#relatorio"))
        pg.click("#aceitar")
        self._completar(pg)
        pg.click("#salvar")
        pg.wait_for_function("Object.keys(JSON.parse(localStorage.getItem('banco_falso') || '{}')).length === 1")
        doc = self._docs(pg)["relatorio-1"]
        self.assertLessEqual(doc["segundos"], 1, "o tempo da pausa entrou na conta")
        self.assertGreaterEqual(doc["segundos_relogio"], 2)
        self.assertEqual(doc["pausas"], 1)

    def teste_pagina_escondida_nao_conta_tempo(self):
        pg = self._abrir()
        pg.click("#comecar")
        pg.click("#abrir")
        pg.evaluate("""() => { Object.defineProperty(document, 'visibilityState', {configurable: true, get: () => 'hidden'}); document.dispatchEvent(new Event('visibilitychange')); }""")
        pg.wait_for_timeout(2200)
        pg.evaluate("""() => { Object.defineProperty(document, 'visibilityState', {configurable: true, get: () => 'visible'}); document.dispatchEvent(new Event('visibilitychange')); }""")
        pg.click("#aceitar")
        self._completar(pg)
        pg.click("#salvar")
        pg.wait_for_function("Object.keys(JSON.parse(localStorage.getItem('banco_falso') || '{}')).length === 1")
        self.assertLessEqual(self._docs(pg)["relatorio-1"]["segundos"], 1)

    def teste_recarregar_no_meio_da_leitura_guarda_o_tempo_e_volta_pausado(self):
        pg = self._abrir()
        pg.click("#comecar")
        pg.click("#abrir")
        pg.wait_for_timeout(1300)
        pg.reload(wait_until="domcontentloaded")
        pg.wait_for_function("document.getElementById('palco').dataset.pronta === 'sim'")
        self.assertTrue(self._visivel(pg, "#continuar"))
        self.assertFalse(self._visivel(pg, "#relatorio"))
        pg.click("#continuar")
        self.assertTrue(pg.get_by_text("MARCA_zeta-2").is_visible())
        pg.click("#aceitar")
        self._completar(pg)
        pg.click("#salvar")
        pg.wait_for_function("Object.keys(JSON.parse(localStorage.getItem('banco_falso') || '{}')).length === 1")
        doc = self._docs(pg)["relatorio-1"]
        self.assertGreaterEqual(doc["segundos"], 1)
        self.assertEqual(doc["retomadas"], 1)

    def teste_recarregar_depois_de_decidir_guarda_a_decisao_e_as_respostas(self):
        pg = self._abrir()
        pg.click("#comecar")
        pg.click("#abrir")
        pg.click("#recusar")
        pg.click('label[for="util-5"]')
        pg.fill("#comentario", "rascunho")
        pg.reload(wait_until="domcontentloaded")
        pg.wait_for_function("document.getElementById('palco').dataset.pronta === 'sim'")
        self.assertTrue(self._visivel(pg, "#salvar"))
        self.assertTrue(pg.get_by_text("MARCA_zeta-2").is_visible())
        self.assertTrue(pg.locator("#dec-recusar").is_checked())
        self.assertTrue(pg.locator("#util-5").is_checked())
        self.assertEqual(pg.input_value("#comentario"), "rascunho")

    def teste_voltar_a_ler_religa_o_cronometro_de_onde_parou(self):
        pg = self._abrir()
        pg.click("#comecar")
        pg.click("#abrir")
        pg.wait_for_timeout(1100)
        pg.click("#aceitar")
        pg.wait_for_timeout(1500)
        pg.click("#voltar-a-ler")
        self.assertTrue(self._visivel(pg, "#aceitar"))
        pg.wait_for_timeout(1100)
        pg.click("#recusar")
        self._completar(pg)
        pg.click("#salvar")
        pg.wait_for_function("Object.keys(JSON.parse(localStorage.getItem('banco_falso') || '{}')).length === 1")
        doc = self._docs(pg)["relatorio-1"]
        self.assertEqual(doc["decisao"], "recusar")
        self.assertGreaterEqual(doc["segundos"], 2)
        self.assertLessEqual(doc["segundos"], 3, "o tempo depois da primeira decisão não é leitura")

    def teste_volta_no_primeiro_sem_resposta_e_nao_mostra_o_inicio(self):
        pg = self._abrir()
        pg.click("#comecar")
        self._um_relatorio_inteiro(pg)
        pg.wait_for_function("Object.keys(JSON.parse(localStorage.getItem('banco_falso') || '{}')).length === 1")
        pg.reload(wait_until="domcontentloaded")
        pg.wait_for_function("document.getElementById('palco').dataset.pronta === 'sim'")
        self.assertFalse(self._visivel(pg, "#comecar"))
        self.assertTrue(self._visivel(pg, "#abrir"))
        self.assertIn("Relatório 2 de 3", pg.inner_text("#antes"))
        self.assertIn("salvo", pg.get_attribute("#pip-0", "class"))
        self.assertTrue(pg.locator("#pip-2").is_disabled(), "a ordem é a da planilha: não se pula relatório")

    def teste_documento_de_outro_id_no_banco_nao_conta(self):
        pg = self._abrir(preparo="localStorage.setItem('banco_falso', JSON.stringify({sonda: {x: 1}}))")
        self.assertTrue(self._visivel(pg, "#comecar"))
        self.assertNotIn("salvo", pg.get_attribute("#pip-0", "class"))

    def teste_fim_mostra_todas_as_respostas_e_corrigir_mantem_o_tempo(self):
        pg = self._abrir()
        pg.click("#comecar")
        for _ in range(3):
            self._um_relatorio_inteiro(pg, comentario="primeira")
        pg.wait_for_selector("#fim:not([hidden])")
        self.assertEqual(pg.locator("#fim tbody tr").count(), 3)
        self.assertIn("3 respostas", pg.inner_text("#fim h2"))
        pg.wait_for_function("Object.keys(JSON.parse(localStorage.getItem('banco_falso') || '{}')).length === 3")
        antes = self._docs(pg)["relatorio-1"]
        pg.click('button[data-corrigir="0"]')
        self.assertTrue(pg.get_by_text("MARCA_zeta-2").is_visible())
        self.assertEqual(pg.input_value("#comentario"), "primeira")
        pg.fill("#comentario", "corrigida")
        pg.click("#salvar")
        pg.wait_for_selector("#fim:not([hidden])")
        pg.wait_for_function("JSON.parse(localStorage.getItem('banco_falso'))['relatorio-1'].comentario === 'corrigida'")
        depois = self._docs(pg)["relatorio-1"]
        self.assertEqual(depois["segundos"], antes["segundos"])
        self.assertIn("editado_em", depois)
        self.assertNotIn("editado_em", antes)
        self.assertEqual(self.erros, [])

    def teste_sem_banco_guarda_no_navegador_e_oferece_copiar(self):
        pg = self._abrir(_SEM_BANCO)
        self.assertTrue(self._visivel(pg, "#aviso"))
        pg.click("#comecar")
        for _ in range(3):
            self._um_relatorio_inteiro(pg)
        pg.wait_for_selector("#fim:not([hidden])")
        self.assertIn("neste navegador", pg.inner_text("#fim"))
        pg.reload(wait_until="domcontentloaded")
        pg.wait_for_function("document.getElementById('palco').dataset.pronta === 'sim'")
        pg.wait_for_selector("#fim:not([hidden])")
        texto = pg.input_value("#respostas-texto")
        self.assertEqual([d["caso"] for d in json.loads(texto)], ["relatorio-1", "relatorio-2", "relatorio-3"])

    def teste_falha_ao_salvar_nao_perde_a_resposta_e_tentar_de_novo_envia(self):
        pg = self._abrir()
        pg.evaluate("window.__falhas = 2")
        pg.click("#comecar")
        self._um_relatorio_inteiro(pg)
        pg.wait_for_selector("#tentar:visible", timeout=6000)
        self.assertIn("banco fora do ar", pg.inner_text("#aviso"))
        self.assertTrue(self._visivel(pg, "#abrir"), "a falha não prende a sessão")
        self.assertEqual(self._docs(pg), {})
        pg.reload(wait_until="domcontentloaded")
        pg.wait_for_function("document.getElementById('palco').dataset.pronta === 'sim'")
        pg.evaluate("window.__falhas = 0")
        self.assertIn("Relatório 2 de 3", pg.inner_text("#antes"), "a resposta pendente conta como respondida")
        pg.click("#tentar")
        pg.wait_for_function("Object.keys(JSON.parse(localStorage.getItem('banco_falso') || '{}')).length === 1")
        pg.wait_for_selector("#tentar", state="hidden")
        self.assertEqual(self._docs(pg)["relatorio-1"]["caso"], "relatorio-1")

    def teste_no_celular_a_decisao_fica_a_vista_e_a_pagina_nao_rola_de_lado(self):
        pg = self._abrir(largura=390, altura=844)
        lado = "document.documentElement.scrollWidth - document.documentElement.clientWidth"
        self.assertEqual(pg.evaluate(lado), 0, "início")
        pg.click("#comecar")
        pg.click("#abrir")
        self.assertEqual(pg.evaluate(lado), 0, "lendo")
        pg.evaluate("window.scrollTo(0, 900)")
        caixa = pg.locator("#aceitar").bounding_box()
        self.assertGreaterEqual(caixa["y"], 0)
        self.assertLessEqual(caixa["y"] + caixa["height"], 844, "o botão de decidir sumiu da tela durante a leitura")
        pg.click("#aceitar")
        self.assertEqual(pg.evaluate(lado), 0, "decidido")
        self.assertLess(pg.locator("#salvar").bounding_box()["y"], pg.get_by_text("MARCA_zeta-2").bounding_box()["y"], "a ficha vem antes do relatório no celular")

    def teste_no_computador_relatorio_e_ficha_ficam_lado_a_lado(self):
        pg = self._abrir()
        pg.click("#comecar")
        pg.click("#abrir")
        pg.click("#aceitar")
        ficha, relatorio = pg.locator("#painel").bounding_box(), pg.locator("#relatorio").bounding_box()
        self.assertGreaterEqual(ficha["x"], relatorio["x"] + relatorio["width"])


if __name__ == "__main__":
    unittest.main(verbosity=1)
