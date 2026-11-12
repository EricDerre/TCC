#!/usr/bin/env python3
# ! Alteração de IA - Revisar: testes novos (10/11/2026) do script que junta as medidas do repositório citadas pela rodada 7 da
# pesquisa (ficha 64): a faixa em que cai a posição do verbete da causa certa na busca; o cruzamento, caso a caso, do acerto com o
# selo de confiança, com os dois gatilhos que o agente já calcula (probabilidade baixa e FONTE divergente) e com essa posição; o
# teto de um segundo passe com mais verbetes; a leitura da linha do `qwen2.5:7b` na tabela do relatório da Fase 2-A; e, com os
# arquivos das corridas na máquina, que os números do arquivo gerado são os dos JSON de origem e que a busca refeita agora devolve
# os mesmos três verbetes que cada corrida gravou.
# ! Motivo: o levantamento, a proposta de desenho e a aba do painel desta rodada citam números das corridas 16, 20, 22, 23 e 24;
# a regra do repositório é nenhum número digitado à mão, e uma conta nova (em que posição da busca fica o verbete que faltou nos
# erros) só vale se a busca refeita for a mesma que a corrida usou. Os testes vieram antes do código.
"""Uso: python ferramentas/testar_medidas_fluxo_do_agente.py"""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import medidas_fluxo_do_agente as mf

# seis casos inventados: dois erros sem o verbete certo entre os três entregues (um na posição 4, com selo baixo; um na posição 12,
# só com a FONTE divergente), um erro com o verbete certo no contexto e selo alto, e três acertos (um deles com selo baixo)
CASOS = [
    {"caso": "a-1", "acerto": False, "selo": "baixo", "gatilho_probabilidade": True, "gatilho_fonte": False, "posicao": 4},
    {"caso": "a-2", "acerto": False, "selo": "medio", "gatilho_probabilidade": False, "gatilho_fonte": True, "posicao": 12},
    {"caso": "a-3", "acerto": False, "selo": "alto", "gatilho_probabilidade": False, "gatilho_fonte": False, "posicao": 2},
    {"caso": "a-4", "acerto": True, "selo": "baixo", "gatilho_probabilidade": True, "gatilho_fonte": False, "posicao": 1},
    {"caso": "a-5", "acerto": True, "selo": "alto", "gatilho_probabilidade": False, "gatilho_fonte": False, "posicao": 3},
    {"caso": "a-6", "acerto": True, "selo": "medio", "gatilho_probabilidade": False, "gatilho_fonte": False, "posicao": 6},
]
TABELA_2A = ("## 3. Estratégias de prompt\n\n| Modelo | Linear | Estágios (compilador) | Estágios (domínio) | linear × compilador | linear × domínio | compilador × domínio |\n"
             "|---|---|---|---|---|---|---|\n| `granite4.2:8b` | 67,8% | 52,2% | 48,9% | 20/6, **p = 0,009** | 23/6, **p = 0,002** | 13/10, p = 0,68 |\n"
             "| `qwen2.5:7b` | 53,3% | 47,8% | 48,9% | 14/9, p = 0,41 | 13/9, p = 0,52 | 4/5, p = 1,00 |\n\n## 4. Outra seção\n")


class TestesMedidasFluxoDoAgente(unittest.TestCase):
    def teste_faixa_da_posicao(self):
        esperado = {1: "1 a 3", 3: "1 a 3", 4: "4 a 5", 5: "4 a 5", 6: "6 a 10", 10: "6 a 10", 11: "acima de 10", 39: "acima de 10", None: "sem verbete da causa"}
        for posicao, faixa in esperado.items():
            self.assertEqual(mf.faixa_da_posicao(posicao), faixa, posicao)

    def teste_cruzamento_conta_acertos_erros_e_o_verbete_certo(self):
        c = mf.cruzar(CASOS)
        self.assertEqual((c["casos"], c["acertos"], c["erros"]), (6, 3, 3))
        self.assertEqual(c["verbete_certo_no_contexto"], {"presente": {"casos": 3, "acertos": 2}, "ausente": {"casos": 3, "acertos": 1}})
        self.assertEqual(c["erros_sem_o_verbete_certo"], 2)
        self.assertEqual(c["posicao_do_verbete_certo"], [{"faixa": "1 a 3", "casos": 3, "erros": 1}, {"faixa": "4 a 5", "casos": 1, "erros": 1},
                                                         {"faixa": "6 a 10", "casos": 1, "erros": 0}, {"faixa": "acima de 10", "casos": 1, "erros": 1}])

    def teste_cruzamento_conta_o_que_cada_gatilho_pega_e_o_que_incomoda(self):
        g = {x["gatilho"]: x for x in mf.cruzar(CASOS)["gatilhos"]}
        self.assertEqual(list(g), ["selo baixo", "FONTE divergente", "selo baixo ou FONTE divergente"])
        self.assertEqual(g["selo baixo"], {"gatilho": "selo baixo", "disparos": 2, "erros_pegos": 1, "acertos_incomodados": 1, "erros_perdidos": 2})
        self.assertEqual(g["FONTE divergente"], {"gatilho": "FONTE divergente", "disparos": 1, "erros_pegos": 1, "acertos_incomodados": 0, "erros_perdidos": 2})
        self.assertEqual(g["selo baixo ou FONTE divergente"], {"gatilho": "selo baixo ou FONTE divergente", "disparos": 3, "erros_pegos": 2, "acertos_incomodados": 1, "erros_perdidos": 1})

    def teste_teto_do_segundo_passe_so_conta_erro_com_gatilho_e_verbete_ao_alcance(self):
        c = mf.cruzar(CASOS)
        # com 5 verbetes: só o a-1 (gatilho aceso, verbete na posição 4); com 10, o mesmo; o a-2 tem o verbete na posição 12 e o a-3 já tinha o verbete certo
        self.assertEqual(c["teto_de_um_segundo_passe"], [{"verbetes": 5, "disparos": 3, "erros_ao_alcance": 1, "erros_fora_do_alcance": 2},
                                                         {"verbetes": 10, "disparos": 3, "erros_ao_alcance": 1, "erros_fora_do_alcance": 2}])
        self.assertEqual([e["caso"] for e in c["lista_de_erros"]], ["a-1", "a-2", "a-3"])
        self.assertEqual(c["lista_de_erros"][0]["faixa"], "4 a 5")

    def teste_fonte_divergente_separada_pela_falha_gravada(self):
        # ! Alteração de IA - Revisar: (10/11/2026, depois da revisão da entrega) os casos com a FONTE divergente saem também separados pela falha que o nó de diagnóstico gravou.
        # ! Motivo: o gatilho da FONTE junta duas conferências (a FONTE cita um verbete fora dos três entregues; nenhum verbete entregue trata da causa respondida), e a proposta
        # de desenho do analista de documentação só trata a segunda como lacuna da documentação. O texto atribuía os acertos com o gatilho aceso a ela sem ter medido.
        casos = [dict(c) for c in CASOS]
        casos[1]["falha"] = "causa_sem_verbete_que_a_trate"      # o a-2, erro só com a FONTE divergente
        casos += [{"caso": "a-7", "acerto": True, "selo": "alto", "gatilho_probabilidade": False, "gatilho_fonte": True, "posicao": 1, "falha": "causa_sem_verbete_que_a_trate"},
                  {"caso": "a-8", "acerto": True, "selo": "alto", "gatilho_probabilidade": False, "gatilho_fonte": True, "posicao": 2, "falha": "citacao_fora_do_contexto"}]
        self.assertEqual(mf.cruzar(casos)["fonte_divergente_por_falha"],
                         [{"falha": "causa_sem_verbete_que_a_trate", "casos": 2, "acertos": 1, "erros": 1}, {"falha": "citacao_fora_do_contexto", "casos": 1, "acertos": 1, "erros": 0}])
        # caso sem o campo `falha` (os seis casos inventados acima) entra como "sem falha gravada", para a soma sempre fechar com os disparos do gatilho
        self.assertEqual(mf.cruzar(CASOS)["fonte_divergente_por_falha"], [{"falha": "sem falha gravada", "casos": 1, "acertos": 0, "erros": 1}])

    def teste_soma_dos_cruzamentos_leva_a_fonte_divergente_por_falha(self):
        # ! Alteração de IA - Revisar: (10/11/2026, depois da revisão da entrega) a soma de duas corridas leva também a FONTE divergente separada pela falha gravada.
        # ! Motivo: a ficha 66 descreve o segundo sinal do segundo passe pelos 72 casos das corridas 22 e 24; o total por falha tem de sair do script, e não de uma soma de cabeça.
        casos = [dict(c) for c in CASOS]
        casos[1]["falha"] = "causa_sem_verbete_que_a_trate"
        outra = casos + [{"caso": "a-8", "acerto": True, "selo": "alto", "gatilho_probabilidade": False, "gatilho_fonte": True, "posicao": 2, "falha": "citacao_fora_do_contexto"}]
        soma = mf.somar_cruzamentos([mf.cruzar(casos), mf.cruzar(outra)])
        self.assertEqual(soma["fonte_divergente_por_falha"],
                         [{"falha": "causa_sem_verbete_que_a_trate", "casos": 2, "acertos": 0, "erros": 2}, {"falha": "citacao_fora_do_contexto", "casos": 1, "acertos": 1, "erros": 0}])
        self.assertEqual(soma["disparos_da_fonte_divergente"], 3)
        self.assertEqual((soma["casos"], soma["erros"]), (13, 6))

    def teste_decisao_da_pessoa_cruzada_com_a_fonte_divergente(self):
        # ! Alteração de IA - Revisar: (10/11/2026, depois da revisão da entrega) o cruzamento da decisão de uma pessoa sobre cada relatório com o acerto e com o gatilho da FONTE.
        # ! Motivo: a proposta de desenho dizia que os diagnósticos certos recusados na sessão de revisão eram os que nenhum verbete entregue sustentava; a frase precisa de um número
        # medido, e a conta só vale se todo relatório revisado existir na corrida (por isso para com SystemExit quando falta um caso).
        casos = [{"caso": "c1", "acerto": True, "gatilho_fonte": True, "falha": "causa_sem_verbete_que_a_trate"},
                 {"caso": "c2", "acerto": True, "gatilho_fonte": True, "falha": "causa_sem_verbete_que_a_trate"},
                 {"caso": "c3", "acerto": True, "gatilho_fonte": False, "falha": None},
                 {"caso": "c4", "acerto": False, "gatilho_fonte": True, "falha": "causa_sem_verbete_que_a_trate"},
                 {"caso": "c5", "acerto": True, "gatilho_fonte": False, "falha": None}]
        revisao = [{"caso": "c1", "decisao": "recusar"}, {"caso": "c2", "decisao": "aceitar"}, {"caso": "c3", "decisao": "recusar"},
                   {"caso": "c4", "decisao": "recusar"}, {"caso": "c5", "decisao": "aceitar"}]
        self.assertEqual(mf.decisao_e_fonte_divergente(casos, revisao),
                         {"acertos_com_a_fonte_divergente": 2, "acertos_com_a_fonte_divergente_recusados": 1,
                          "certos_recusados_com_a_fonte_divergente": 1, "certos_recusados_sem_a_fonte_divergente": 1,
                          "certos_recusados_por_falha": [{"falha": "causa_sem_verbete_que_a_trate", "casos": 1}, {"falha": "sem falha gravada", "casos": 1}],
                          "erros_com_a_fonte_divergente": 1, "erros_com_a_fonte_divergente_recusados": 1})
        with self.assertRaises(SystemExit):
            mf.decisao_e_fonte_divergente(casos, revisao + [{"caso": "c9", "decisao": "aceitar"}])

    def teste_verbetes_novos_do_lote_e_quem_os_leria(self):
        # ! Alteração de IA - Revisar: (10/11/2026, depois da revisão da entrega) quantos dos verbetes novos de um lote nenhum caso com gabarito leria.
        # ! Motivo: o mapa do levantamento dizia que nenhum caso leria os verbetes novos da corrida 20, e um deles teria um leitor; o número passa a sair da conta.
        por_edicao = [{"operacao": "novo_verbete", "casos_que_leriam_a_edicao": 0}, {"operacao": "novo_verbete", "casos_que_leriam_a_edicao": 1},
                      {"operacao": "nota", "casos_que_leriam_a_edicao": 0}, {"operacao": "novo_verbete", "casos_que_leriam_a_edicao": 0}]
        self.assertEqual(mf.verbetes_novos_do_lote(por_edicao), {"edicoes": 3, "que_nenhum_caso_leria": 2, "com_algum_caso": 1, "casos_que_os_leriam_no_total": 1})
        self.assertEqual(mf.verbetes_novos_do_lote([]), {"edicoes": 0, "que_nenhum_caso_leria": 0, "com_algum_caso": 0, "casos_que_os_leriam_no_total": 0})

    def teste_le_a_linha_do_modelo_na_tabela_da_fase_2a(self):
        linha = mf.linha_da_fase_2a(TABELA_2A, "qwen2.5:7b")
        self.assertEqual(linha, {"modelo": "qwen2.5:7b", "linear": "53,3%", "estagios_compilador": "47,8%", "estagios_dominio": "48,9%",
                                 "linear_x_compilador": "14/9, p = 0,41", "linear_x_dominio": "13/9, p = 0,52"})
        with self.assertRaises(SystemExit):
            mf.linha_da_fase_2a(TABELA_2A, "modelo-que-nao-existe")

    def teste_conta_as_propostas_em_forma_de_instrucao(self):
        # ! Alteração de IA - Revisar: (10/11/2026) a contagem das propostas que começam por verbo de instrução, no total, entre as que passaram nos filtros e por veredito da revisão.
        # ! Motivo: a proposta de desenho do analista de documentação diz que falta um filtro para a forma de instrução; o número que a sustenta sai desta conta.
        verbos = ("Adicionar", "Corrig")
        self.assertTrue(mf.em_forma_de_instrucao("  Adicionar nota sobre o preço.", verbos))
        self.assertTrue(mf.em_forma_de_instrucao("Corrigir a junção.", verbos))
        self.assertFalse(mf.em_forma_de_instrucao("O preço chega como texto quando a API devolve a lista.", verbos))
        self.assertFalse(mf.em_forma_de_instrucao(None, verbos))
        propostas = [{"texto": "Adicionar nota.", "destino": "aceita"}, {"texto": "O campo some.", "destino": "aceita"}, {"texto": "Corrigir X.", "destino": "recusada"},
                     {"texto": "Adicionar Y.", "destino": "para revisão"}]
        revisadas = [{"texto": "Adicionar nota.", "veredito": "Errada"}, {"texto": "O campo some.", "veredito": "Correta"}, {"texto": "Adicionar Y.", "veredito": "Parcial"}]
        c = mf.contar_forma_de_instrucao(propostas, revisadas, verbos, ("Correta", "Parcial", "Errada"))
        self.assertEqual((c["propostas"], c["em_forma_de_instrucao"], c["passaram_nos_filtros"], c["passaram_em_forma_de_instrucao"]), (4, 3, 3, 2))
        self.assertEqual(c["por_veredito"], [{"veredito": "Correta", "edicoes": 1, "em_forma_de_instrucao": 0}, {"veredito": "Parcial", "edicoes": 1, "em_forma_de_instrucao": 1},
                                             {"veredito": "Errada", "edicoes": 1, "em_forma_de_instrucao": 1}])

    def teste_efeito_de_uma_edicao_na_busca(self):
        # ! Alteração de IA - Revisar: (10/11/2026) o que uma edição muda nos três verbetes entregues: casos que mudam, verbete certo que entra ou sai, e casos que leriam a edição.
        # ! Motivo: é a conta do portão por edição, sem modelo, que a proposta de desenho descreve; aplicada ao lote da corrida 20, diz quantas edições não mudam a busca de nenhum caso.
        antes = {"c1": ["a", "b", "c"], "c2": ["a", "b", "d"], "c3": ["x", "y", "z"]}
        depois = {"c1": ["a", "b", "c"], "c2": ["a", "e", "b"], "c3": ["x", "y", "w"]}
        certo = {"c1": "a", "c2": "e", "c3": "z"}
        self.assertEqual(mf.efeito_na_busca(antes, depois, certo, "e"),
                         {"casos_em_que_os_tres_verbetes_mudam": 2, "verbete_certo_entra": 1, "verbete_certo_sai": 1, "casos_que_leriam_a_edicao": 1})
        self.assertEqual(mf.efeito_na_busca(antes, antes, certo, "a"),
                         {"casos_em_que_os_tres_verbetes_mudam": 0, "verbete_certo_entra": 0, "verbete_certo_sai": 0, "casos_que_leriam_a_edicao": 2})

    def teste_p_pareado_exato(self):
        # ! Alteração de IA - Revisar: (10/11/2026) o p bilateral do teste pareado exato, para dizer se o melhor cenário de um segundo passe sairia do ruído.
        # ! Motivo: o veredito da ideia 2 compara o teto do segundo passe com o corte de 0,05 que o projeto usa (decisão 116); a conta sai do script.
        self.assertEqual(mf.p_pareado_exato(0, 0), 1.0)
        self.assertEqual(mf.p_pareado_exato(3, 0), 0.25)
        self.assertEqual(mf.p_pareado_exato(5, 0), 0.0625)
        self.assertEqual(mf.p_pareado_exato(6, 0), 0.0312)
        self.assertEqual(mf.p_pareado_exato(5, 8), mf.p_pareado_exato(8, 5))
        self.assertAlmostEqual(mf.p_pareado_exato(5, 8), 0.5811, places=4)   # o par k = 3 contra k = 5 da corrida 16

    def teste_conferencias_que_contradizem_o_rotulo(self):
        # ! Alteração de IA - Revisar: (10/11/2026) as cinco conferências de exemplo da prévia: cada uma só contradiz o rótulo quando o fato medido no caso o desmente.
        # ! Motivo: a prévia dimensiona a lista de conferência depois da resposta (veredito da ideia 1); uma conferência que contradissesse um rótulo certo
        # incomodaria acertos, e a medida deixaria de valer.
        contrato = "id: inteiro | nome: texto | resumo: texto|nulo | preco: numero"
        def caso(requisicao, corpo, causa="x"):
            return {"id": "c", "entrada": {"requisicao": requisicao, "contrato": contrato, "corpo": corpo}, "gabarito": {"causa_raiz": causa}}
        lista = '[{"id": 1, "nome": "A", "resumo": null, "preco": 9.5}]'
        objeto = '{"id": 1, "nome": "A", "resumo": "r", "preco": 9}'
        self.assertEqual(mf.corpo_do_caso(caso("GET /api/produtos", lista))[0], "ok")
        self.assertEqual(mf.corpo_do_caso(caso("GET /api/produtos", '[{"id": 1, "nome"'))[0], "invalido")
        self.assertEqual(mf.corpo_do_caso(caso("GET /api/produtos", "  "))[0], "vazio")
        self.assertEqual(mf.corpo_do_caso({"entrada": {}})[0], "sem corpo")
        # coleção no lugar de objeto: contradito só com a forma que a rota devolve e sem lista dentro de campo simples
        self.assertTrue(mf.rotulo_contradito(caso("GET /api/produtos", lista), "colecao_no_lugar_de_objeto"))
        self.assertTrue(mf.rotulo_contradito(caso("GET /api/produtos/7", objeto), "colecao_no_lugar_de_objeto"))
        self.assertFalse(mf.rotulo_contradito(caso("GET /api/produtos/7", lista), "colecao_no_lugar_de_objeto"), "lista na rota de detalhe é o próprio defeito")
        self.assertFalse(mf.rotulo_contradito(caso("GET /api/produtos", objeto), "colecao_no_lugar_de_objeto"), "objeto na rota de lista é o próprio defeito")
        self.assertFalse(mf.rotulo_contradito(caso("GET /api/produtos", '[{"id": 1, "nome": ["A"], "preco": 9}]'), "colecao_no_lugar_de_objeto"), "lista dentro de campo simples")
        self.assertFalse(mf.rotulo_contradito(caso("POST /api/reservas", objeto), "colecao_no_lugar_de_objeto"), "rota fora das conhecidas: sem fato medido")
        self.assertFalse(mf.rotulo_contradito(caso("GET /api/produtos", '[{"id": 1, "nome"'), "colecao_no_lugar_de_objeto"), "corpo que não é JSON inteiro: sem fato medido")
        # tipo divergente: contradito quando todo campo do contrato tem um tipo aceito
        self.assertTrue(mf.rotulo_contradito(caso("GET /api/produtos", lista), "tipo_divergente"))
        self.assertFalse(mf.rotulo_contradito(caso("GET /api/produtos", '[{"id": "1", "nome": "A", "preco": 9.5}]'), "tipo_divergente"))
        self.assertFalse(mf.rotulo_contradito(caso("GET /api/produtos", '[{"id": 1, "nome": "A", "preco": "9,50"}]'), "tipo_divergente"))
        self.assertFalse(mf.rotulo_contradito(caso("GET /api/produtos", '[{"id": true, "nome": "A", "preco": 9.5}]'), "tipo_divergente"), "booleano não é inteiro")
        # truncada, não é JSON e vazio
        self.assertTrue(mf.rotulo_contradito(caso("GET /api/produtos", lista), "resposta_truncada"))
        self.assertFalse(mf.rotulo_contradito(caso("GET /api/produtos", '[{"id": 1, "nome"'), "resposta_truncada"))
        self.assertTrue(mf.rotulo_contradito(caso("GET /api/produtos", lista), "corpo_nao_e_json"))
        self.assertFalse(mf.rotulo_contradito(caso("GET /api/produtos", "<html>erro</html>"), "corpo_nao_e_json"))
        self.assertTrue(mf.rotulo_contradito(caso("GET /api/produtos", lista), "corpo_vazio"))
        self.assertFalse(mf.rotulo_contradito(caso("GET /api/produtos", ""), "corpo_vazio"))
        # rótulo sem conferência nunca é contradito
        self.assertFalse(mf.rotulo_contradito(caso("GET /api/produtos", lista), "dado_desatualizado"))
        self.assertFalse(mf.rotulo_contradito(caso("GET /api/produtos", lista), None))

    def teste_previa_da_conferencia_conta_erros_e_acertos_contraditos(self):
        contrato = "id: inteiro | nome: texto"
        casos = {"a": {"id": "a", "entrada": {"requisicao": "GET /api/produtos", "contrato": contrato, "corpo": '[{"id": 1, "nome": "A"}]'}, "gabarito": {"causa_raiz": "valor_fora_do_dominio"}},
                 "b": {"id": "b", "entrada": {"requisicao": "GET /api/produtos", "contrato": contrato, "corpo": '[{"id": "1", "nome": "A"}]'}, "gabarito": {"causa_raiz": "tipo_divergente"}},
                 "c": {"id": "c", "entrada": {"requisicao": "GET /api/produtos", "contrato": contrato, "corpo": '[{"id": 1, "nome": "A"}]'}, "gabarito": {"causa_raiz": "dado_desatualizado"}}}
        respostas = [{"caso": "a", "rotulo": "tipo_divergente", "acerto": False}, {"caso": "b", "rotulo": "tipo_divergente", "acerto": True},
                     {"caso": "c", "rotulo": "registro_duplicado", "acerto": False}]
        p = mf.previa_da_conferencia(casos, respostas)
        self.assertEqual({k: p[k] for k in ("casos", "erros", "erros_com_rotulo_conferivel", "erros_contraditos", "acertos_contraditos")},
                         {"casos": 3, "erros": 2, "erros_com_rotulo_conferivel": 1, "erros_contraditos": 1, "acertos_contraditos": 0})
        self.assertEqual(p["lista"], [{"caso": "a", "rotulo": "tipo_divergente", "gabarito": "valor_fora_do_dominio"}])

    def teste_mediana_e_formatos(self):
        self.assertEqual(mf.mediana([3, 1, 2]), 2)
        self.assertEqual(mf.mediana([1, 2, 3, 4]), 2.5)
        self.assertIsNone(mf.mediana([]))

    def teste_texto_do_script_sem_travessao_nem_seta(self):
        for l in Path(mf.__file__).read_text(encoding="utf-8").splitlines():
            self.assertNotIn("—", l, l)
            self.assertNotIn("→", l, l)

    def teste_medidas_reais_quando_as_corridas_estao_na_maquina(self):
        if not (mf.F4 / "ineditos.json").exists() or not (mf.F4 / "trilha.json").exists():
            self.skipTest("os JSON das corridas não estão nesta máquina")
        m = mf.montar()
        for chave in ("_tag", "_motivo", "maquina", "ideia_1", "ideia_2", "ideia_3"):
            self.assertIn(chave, m)
        self.assertIn("de IA - Revisar", m["_tag"])
        self.assertIn("! Motivo", m["_motivo"])
        ined = json.loads((mf.F4 / "ineditos.json").read_text(encoding="utf-8"))
        c24 = m["ideia_2"]["corrida_24"]
        self.assertEqual(c24["verbete_certo_no_contexto"], ined["verbete_certo"], "o cruzamento refeito bate com ineditos.json")
        self.assertEqual((c24["casos"], c24["acertos"]), (ined["resumo"]["casos"], ined["resumo"]["acertos"]))
        self.assertEqual(c24["busca_refeita_igual"], c24["casos"], "a busca refeita devolve os três verbetes gravados em todos os casos")
        tri = json.loads((mf.F4 / "trilha.json").read_text(encoding="utf-8"))
        c22 = m["ideia_2"]["corrida_22"]
        self.assertEqual((c22["cruzamento"]["casos"], c22["cruzamento"]["acertos"]), (tri["resumo"]["casos"], tri["resumo"]["acertos"]))
        self.assertEqual(c22["cruzamento"]["busca_refeita_igual"], c22["cruzamento"]["casos"])
        self.assertAlmostEqual(c22["divergencia"]["produto"], tri["resumo"]["produto"])
        bibl = json.loads((mf.F4 / "biblioteca.json").read_text(encoding="utf-8"))
        c20 = m["ideia_3"]["corrida_20"]
        self.assertEqual((c20["propostas"], c20["aceitas"]), (bibl["resumo"]["propostas"], bibl["resumo"]["aceitas"]))
        self.assertEqual(sum(m["ideia_3"]["revisao_do_lote"]["por_veredito"].values()), bibl["lote"]["edicoes"] + bibl["lote"]["para_revisao"])
        taxas = json.loads((mf.F4 / "taxas_progresso.json").read_text(encoding="utf-8"))["por_modelo"][mf.MODELO]
        self.assertEqual(m["maquina"]["geracao_tokens_por_s"], taxas["geracao_tokens_por_s"]["mediana"])
        # ! Alteração de IA - Revisar: (10/11/2026, depois da revisão da entrega) as três contas novas fecham com as que já existiam.
        # ! Motivo: a separação da FONTE divergente pela falha, o cruzamento com a decisão do analista de QA e a conta dos verbetes novos são recortes de números já
        # gravados; se a soma de um recorte não der o total de origem, o recorte está lendo outra coisa.
        for cruzamento in (c24, c22["cruzamento"]):
            self.assertEqual(sum(x["casos"] for x in cruzamento["fonte_divergente_por_falha"]), cruzamento["gatilhos"][1]["disparos"])
        rh = m["ideia_3"]["revisao_humana_v3"]
        self.assertEqual(rh["certos_recusados"], rh["certos_recusados_com_a_fonte_divergente"] + rh["certos_recusados_sem_a_fonte_divergente"])
        self.assertEqual(rh["acertos_com_a_fonte_divergente"], c24["gatilhos"][1]["acertos_incomodados"])
        self.assertEqual(rh["erros_com_a_fonte_divergente"], c24["gatilhos"][1]["erros_pegos"])
        novos = next(x for x in m["ideia_3"]["revisao_do_lote"]["por_operacao"] if x["operacao"] == "novo_verbete")
        vn = m["ideia_3"]["portao_da_busca_no_lote"]["verbetes_novos"]
        self.assertEqual(vn["edicoes"], sum(v for k, v in novos.items() if k != "operacao"))
        self.assertEqual(vn["edicoes"], vn["que_nenhum_caso_leria"] + vn["com_algum_caso"])
        if mf.SAIDA.exists():
            self.assertEqual(mf.check(), 0)


if __name__ == "__main__":
    unittest.main(verbosity=1)
