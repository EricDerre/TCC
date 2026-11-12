#!/usr/bin/env python3
# ! Alteração de IA - Revisar: testes novos (10/11/2026) do integrador da rodada 7 da pesquisa (as três ideias do Eric para o fluxo do
# agente, ficha 64). A rodada tem, por tópico, uma leitura e uma segunda leitura em JSON, e as sínteses do Claude em outro JSON. Os testes
# cobrem: o cruzamento da leitura com a segunda leitura (a afirmação parcial entra com o texto corrigido, a rejeitada sai, a referência
# corrigida substitui a do leitor, a fonte sem afirmação aprovada não vai para as referências); os marcadores {{m:campo}} trocados pelo valor
# das medidas do repositório, com falha se o campo não existe; a subseção no formato fixo que a aba Pesquisa do painel lê; as sínteses só
# citando fonte aprovada; o bloco de referências antes do bloco da Pós-Fase 4, sem repetir referência e sem desfazer os blocos dos outros
# dois integradores; as duas linhas do índice do Memorial; a proposta de desenho gerada do modelo; e o texto sem travessão nem seta fora do
# cabeçalho de formato fixo.
# ! Motivo: a rodada 6 entrou sem segunda leitura e esta entra com ela; sem os testes, uma afirmação que a segunda leitura corrigiu poderia
# sair no levantamento com o texto do primeiro leitor, um número do repositório poderia ser digitado à mão nas sínteses, e o bloco de
# referências, posto no lugar errado, quebraria o --check dos integradores da Pré-Fase 4 e da Pós-Fase 4. Os testes vieram antes do código.
"""Uso: python ferramentas/testar_integrar_pesquisa_fluxo_do_agente.py"""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import integrar_pesquisa_fluxo_do_agente as ifa
import integrar_pesquisa_pos_fase4 as ipp
import integrar_pesquisa_pre_fase4 as ip

FIM = " Disponível em: https://arxiv.org/abs/{}. Acesso em: 10 nov. 2026."
LEITURA_A = {
    "_tag": "! Alteração de IA - Revisar: leitura de teste.", "_motivo": "! Motivo: teste.", "key": "r7-a", "frente": 1, "titulo": "Tópico A", "pesquisado_em": "10/11/2026",
    "pergunta": "pergunta A", "ja_levantado": [{"secao": "§6.9.14", "o_que_ja_dizia": "já dizia isto"}],
    "fontes": [
        {"id": "F01", "referencia_abnt": "ALFA, A. Primeiro estudo sobre passos. arXiv, 2024." + FIM.format("2401.00001"), "identificador": "arXiv:2401.00001", "url": "https://arxiv.org/abs/2401.00001",
         "ano": 2024, "veiculo": "preprint", "revisao_por_pares": False, "como_li": "aberta_e_lida", "o_que_li": "resumo", "ja_consta_em_referencias_md": False,
         "afirmacoes": [{"id": "F01.a", "afirmacao_pt": "afirmação confirmada", "numero": "10", "condicao": "c", "onde_na_fonte": "tabela 1"},
                        {"id": "F01.b", "afirmacao_pt": "afirmação com número errado", "numero": "99", "condicao": "c", "onde_na_fonte": "tabela 2"}],
         "nao_afirma": ["limite do leitor"], "aplicacao_ao_agente": "aplica"},
        {"id": "F02", "referencia_abnt": "BETA, B. Segundo estudo com evento errado. In: EVENTO, 2025." + FIM.format("2501.00002"), "identificador": "arXiv:2501.00002", "url": "https://arxiv.org/abs/2501.00002",
         "ano": 2025, "veiculo": "EVENTO 2025", "revisao_por_pares": True, "como_li": "so_resumo", "o_que_li": "resumo", "ja_consta_em_referencias_md": False,
         "afirmacoes": [{"id": "F02.a", "afirmacao_pt": "afirmação que a fonte não faz", "numero": "", "condicao": "c", "onde_na_fonte": "resumo"}],
         "nao_afirma": [], "aplicacao_ao_agente": "aplica"},
        {"id": "F03", "referencia_abnt": "GAMA, G. Terceiro estudo que não abriu. arXiv, 2026." + FIM.format("2601.00003"), "identificador": "arXiv:2601.00003", "url": "https://arxiv.org/abs/2601.00003",
         "ano": 2026, "veiculo": "preprint", "revisao_por_pares": False, "como_li": "so_busca", "o_que_li": "busca", "ja_consta_em_referencias_md": False,
         "afirmacoes": [{"id": "F03.a", "afirmacao_pt": "afirmação que ninguém conferiu", "numero": "", "condicao": "c", "onde_na_fonte": "resumo"}],
         "nao_afirma": [], "aplicacao_ao_agente": "aplica"},
    ],
    "nao_achei": ["o que faltou"], "rascunho_de_sintese_pt": "rascunho",
}
VERIFICACAO_A = {
    "_tag": "! Alteração de IA - Revisar: verificação de teste.", "_motivo": "! Motivo: teste.", "key": "r7-a", "verificado_em": "10/11/2026",
    "fontes": [
        {"id": "F01", "abriu": "sim", "identificador_conferido": "arXiv:2401.00001", "titulo_e_autores_batem": True, "veiculo_conferido": "não confirmado", "referencia_abnt_corrigida": "",
         "o_que_a_fonte_afirma": "afirma isto", "o_que_a_fonte_nao_afirma": ["não testou modelo pequeno"],
         "afirmacoes": [{"id": "F01.a", "veredito": "confirmada", "numero_que_a_fonte_sustenta": "", "afirmacao_corrigida_pt": "", "motivo": ""},
                        {"id": "F01.b", "veredito": "parcial", "numero_que_a_fonte_sustenta": "42", "afirmacao_corrigida_pt": "afirmação com o número certo", "motivo": "o número é outro"}]},
        {"id": "F02", "abriu": "sim", "identificador_conferido": "arXiv:2501.00002", "titulo_e_autores_batem": True, "veiculo_conferido": "não confirmado",
         "referencia_abnt_corrigida": "BETA, B. Segundo estudo, agora como preprint. arXiv, 2025." + FIM.format("2501.00002"),
         "o_que_a_fonte_afirma": "afirma outra coisa", "o_que_a_fonte_nao_afirma": ["não mede calibração"],
         "afirmacoes": [{"id": "F02.a", "veredito": "rejeitada", "numero_que_a_fonte_sustenta": "", "afirmacao_corrigida_pt": "", "motivo": "a fonte diz o contrário"}]},
        {"id": "F03", "abriu": "nao_abriu", "identificador_conferido": "", "titulo_e_autores_batem": False, "veiculo_conferido": "não confirmado", "referencia_abnt_corrigida": "",
         "o_que_a_fonte_afirma": "", "o_que_a_fonte_nao_afirma": [],
         "afirmacoes": [{"id": "F03.a", "veredito": "nao_verificada", "numero_que_a_fonte_sustenta": "", "afirmacao_corrigida_pt": "", "motivo": "a página não abriu"}]},
    ],
}
LEITURA_B = {**LEITURA_A, "key": "r7-b", "frente": 3, "titulo": "Tópico B", "ja_levantado": [],
             "fontes": [{**LEITURA_A["fontes"][0], "referencia_abnt": "DELTA, D. Estudo do tópico B sobre a base. arXiv, 2025." + FIM.format("2502.00004"), "identificador": "arXiv:2502.00004",
                         "afirmacoes": [{"id": "F01.a", "afirmacao_pt": "afirmação do tópico B", "numero": "", "condicao": "c", "onde_na_fonte": "resumo"}]}]}
VERIFICACAO_B = {**VERIFICACAO_A, "key": "r7-b",
                 "fontes": [{**VERIFICACAO_A["fontes"][0], "identificador_conferido": "arXiv:2502.00004", "veiculo_conferido": "EVENTO 2025, visto na página",
                             "afirmacoes": [{"id": "F01.a", "veredito": "confirmada", "numero_que_a_fonte_sustenta": "", "afirmacao_corrigida_pt": "", "motivo": ""}]}]}
MEDIDAS = {"maquina": {"segundos": 23.3, "tokens": 5921, "inteiro_como_float": 63.0}, "lista": [{"erros": 3}, {"erros": 5}], "texto": "53,3%"}
SINTESES = {
    "topicos": {
        "r7-a": {"titulo": "Síntese A", "texto": ["Primeiro parágrafo, com a fonte [F01] e o número {{m:lista.1.erros}}.", "**Custo.** Segundo parágrafo: {{m:maquina.segundos|1}} s."],
                 "implicacoes": ["Implicação com {{m:texto}}."], "lacunas": ["Lacuna A."]},
        "r7-b": {"titulo": "Síntese B", "texto": ["Texto B, com [F01]."], "implicacoes": ["Implicação B."], "lacunas": ["Lacuna B."]},
    },
    "vereditos": [{"ideia": 1, "nome": "Ideia um", "veredito": "Veredito um.", "literatura": "Literatura.", "repositorio": "Repositório com {{m:maquina.tokens}} tokens.",
                   "forma_que_escapa": "Forma.", "como_medir": "Medida.", "custo": "Custo.", "recomendacao": "Recomendação."}],
    "mapa": [{"tema": "Tema", "opcao": "Opção", "veredito": "adiado", "motivo": "motivo com {{m:lista.0.erros}} erros", "fonte": "§6.16.1"}],
}
TOPICOS_DE_TESTE = [("r7-a", "1", "Tópico A curto"), ("r7-b", "3", "Tópico B curto")]
REFS = ("# Referências levantadas\n\n## 9. Referências levantadas\n\n"
        "Além das 7 do projeto de pesquisa, os levantamentos de 11/09, 21/09, 22/09, 29/09, 01/10 e 07/11/2026 produziram as **3** referências abaixo, organizadas por tema.\n\n"
        "### Raciocínio\n\n- OUTRA, A. Título qualquer. 2020. Disponível em: https://exemplo.org/a. Acesso em: 1 out. 2026.\n\n"
        + ipp.TITULO_REFS + "\n\n<!-- tag da Pós-Fase 4 -->\n\n- DELTA, D. O mesmo estudo do tópico B, citado na rodada 6. 2025. Disponível em: https://arxiv.org/abs/2502.00004. Acesso em: 7 nov. 2026.\n\n"
        + ip.TITULO_REFS + "\n\n<!-- tag da Pré-Fase 4 -->\n\n- ZZZ, B. Último da lista. 2024. Disponível em: https://exemplo.org/z. Acesso em: 1 out. 2026.\n")
MEMORIAL = ("- [Levantamento: Pré-Fase 4 (01/10/2026)](memorial/x.md): §6.14.\n"
            + ipp.TAG_DO_INDICE + " (§6.15), gravada por integrar_pesquisa_pos_fase4.py. ! Motivo: sem a linha o índice não leva ao levantamento. -->\n"
            + ipp.MARCA_DO_INDICE + "(memorial/2-pesquisa-e-literatura/levantamento-2026-11-07-pos-fase-4.md): §6.15, 14 tópicos.\n"
            "- [Referências levantadas](memorial/2-pesquisa-e-literatura/referencias.md): §9.\n\n### 5. Método e ferramental\n\n"
            "- [Protocolo da linha de base manual (Fase 5)](memorial/5-metodo-e-ferramental/protocolo-linha-de-base-manual.md): versão 1.\n\n### 6. Outra seção\n")
MODELO = ("<!-- ! Alteração de IA - Revisar: modelo de teste.\n     ! Motivo: teste. -->\n\n# Proposta\n\nCusta {{m:maquina.segundos|1}} s e {{m:maquina.tokens}} tokens.\n\n"
          "<!-- medidas:custos -->\n")


def _pasta_de_teste() -> Path:
    pasta = Path(tempfile.mkdtemp(prefix="fluxo_"))
    for nome, dado in (("r7-a.json", LEITURA_A), ("r7-a.verificacao.json", VERIFICACAO_A), ("r7-b.json", LEITURA_B), ("r7-b.verificacao.json", VERIFICACAO_B),
                       ("sinteses.json", SINTESES), ("medidas_do_repositorio.json", MEDIDAS)):
        (pasta / nome).write_text(json.dumps(dado, ensure_ascii=False), encoding="utf-8")
    return pasta


class TestesIntegradorFluxoDoAgente(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pasta = _pasta_de_teste()
        cls.dados = ifa.carregar(cls.pasta, TOPICOS_DE_TESTE)

    # ---------------------------------------------------------------- marcadores das medidas
    def teste_valor_segue_o_caminho_pontilhado_e_para_no_campo_que_nao_existe(self):
        self.assertEqual(ifa.valor(MEDIDAS, "maquina.segundos"), 23.3)
        self.assertEqual(ifa.valor(MEDIDAS, "lista.1.erros"), 5)
        with self.assertRaises(SystemExit):
            ifa.valor(MEDIDAS, "maquina.nao_existe")
        with self.assertRaises(SystemExit):
            ifa.valor(MEDIDAS, "lista.7.erros")

    def teste_formata_inteiro_com_ponto_de_milhar_e_decimal_com_virgula(self):
        self.assertEqual(ifa.formatar(5921), "5.921")
        self.assertEqual(ifa.formatar(36), "36")
        self.assertEqual(ifa.formatar(63.0), "63")
        self.assertEqual(ifa.formatar(23.3, 1), "23,3")
        self.assertEqual(ifa.formatar(0.7988, 2), "0,80")
        self.assertEqual(ifa.formatar(55.96, 0), "56")
        self.assertEqual(ifa.formatar("53,3%"), "53,3%")
        with self.assertRaises(SystemExit):
            ifa.formatar(23.3)          # decimal sem dizer as casas: a escolha tem de ser de quem escreve
        with self.assertRaises(SystemExit):
            ifa.formatar([1, 2])

    def teste_preenche_os_marcadores_e_acusa_o_que_sobra(self):
        self.assertEqual(ifa.preencher("Custa {{m:maquina.segundos|1}} s, {{m:maquina.tokens}} tokens e {{m:texto}}.", MEDIDAS), "Custa 23,3 s, 5.921 tokens e 53,3%.")
        with self.assertRaises(SystemExit):
            ifa.preencher("Sobra {{m:maquina.nada}}.", MEDIDAS)
        with self.assertRaises(SystemExit):
            ifa.preencher("Marcador mal escrito {{maquina.segundos}}.", MEDIDAS)

    # ---------------------------------------------------------------- leitura cruzada com a segunda leitura
    def teste_cruza_a_leitura_com_a_segunda_leitura(self):
        a = self.dados["r7-a"]
        self.assertEqual((a["titulo"], a["frente"]), ("Tópico A curto", "1"))
        self.assertEqual(ifa.contagem(a), {"aprovadas": 2, "parciais": 1, "rejeitadas": 1, "nao_verificadas": 1})
        f1, f2, f3 = a["fontes"]
        self.assertEqual([x["texto"] for x in f1["afirmacoes"]], ["afirmação confirmada", "afirmação com o número certo"])
        self.assertEqual(f1["afirmacoes"][1]["veredito"], "parcial")
        self.assertTrue(f1["aprovada"])
        self.assertEqual(f1["nao_afirma"], ["não testou modelo pequeno"], "os limites que valem são os da segunda leitura")
        self.assertFalse(f2["aprovada"])
        self.assertTrue(f2["referencia"].startswith("BETA, B. Segundo estudo, agora como preprint."), "a referência corrigida substitui a do leitor")
        self.assertTrue(f2["referencia_corrigida"])
        self.assertFalse(f3["aprovada"])
        self.assertEqual(ifa.referencias_do_topico(a), [f1["referencia"]], "só entra referência de fonte com afirmação aprovada")

    def teste_recusa_segunda_leitura_que_nao_cobre_a_leitura(self):
        pasta = Path(tempfile.mkdtemp(prefix="fluxo_falta_"))
        (pasta / "r7-a.json").write_text(json.dumps(LEITURA_A, ensure_ascii=False), encoding="utf-8")
        with self.assertRaises(SystemExit):
            ifa.carregar(pasta, TOPICOS_DE_TESTE[:1])   # falta o arquivo da segunda leitura
        incompleta = {**VERIFICACAO_A, "fontes": VERIFICACAO_A["fontes"][:2]}
        (pasta / "r7-a.verificacao.json").write_text(json.dumps(incompleta, ensure_ascii=False), encoding="utf-8")
        with self.assertRaises(SystemExit):
            ifa.carregar(pasta, TOPICOS_DE_TESTE[:1])   # a segunda leitura não traz a fonte F03

    # ---------------------------------------------------------------- render
    def teste_subsecao_no_formato_fixo_que_o_painel_le(self):
        s = ifa.secao(1, "r7-a", self.dados["r7-a"], SINTESES["topicos"]["r7-a"], MEDIDAS)
        cab = s.splitlines()[0]
        self.assertEqual(cab, "#### 6.16.1 Tópico A curto (`r7-a` — 2 aprovadas, 1 rejeitada, 1 não verificada)")
        import painel_topicos as tp
        m = tp._TOPICO.match(cab)
        self.assertTrue(m, "o cabeçalho tem de casar com a expressão da aba Pesquisa do painel")
        self.assertEqual((m.group(3), int(m.group(4)), int(m.group(5)), int(m.group(6))), ("r7-a", 2, 1, 1))
        for trecho in ("*Título da síntese:* Síntese A", "##### O que as rodadas anteriores já diziam", "* §6.9.14: já dizia isto", "##### Texto", "o número 5.", "**Custo.** Segundo parágrafo: 23,3 s.",
                       "##### Implicações para o agente", "* Implicação com 53,3%.", "##### Lacunas", "* Lacuna A.", "##### Segunda leitura das fontes", "arXiv:2401.00001",
                       "não testou modelo pequeno", "##### Referências ABNT do tópico", "- ALFA, A. Primeiro estudo sobre passos."):
            self.assertIn(trecho, s)
        self.assertNotIn("- BETA, B.", s, "fonte sem afirmação aprovada não vai para as referências do tópico")
        self.assertNotIn("{{", s)
        b = ifa.secao(2, "r7-b", self.dados["r7-b"], SINTESES["topicos"]["r7-b"], MEDIDAS)
        self.assertTrue(b.startswith("#### 6.16.2 Tópico B curto (`r7-b` — 1 aprovada, 0 rejeitadas)"))
        self.assertNotIn("O que as rodadas anteriores já diziam", b, "sem nada já levantado, o bloco não sai")

    def teste_sinteses_so_citam_fonte_com_afirmacao_aprovada(self):
        self.assertEqual(ifa.citacoes_sem_apoio(self.dados, SINTESES), [])
        ruim = {"topicos": {**SINTESES["topicos"], "r7-a": {**SINTESES["topicos"]["r7-a"], "texto": ["Cita a rejeitada [F02] e uma que não existe [F09]."]}}}
        self.assertEqual(ifa.citacoes_sem_apoio(self.dados, ruim), [("r7-a", "F02"), ("r7-a", "F09")])

    def teste_render_tem_as_subsecoes_as_rejeitadas_os_vereditos_o_mapa_e_o_travessao_so_no_cabecalho(self):
        t = ifa.render(self.dados, SINTESES, MEDIDAS, TOPICOS_DE_TESTE, bloco_das_medidas=lambda m: "tabela das medidas\n")
        self.assertIn("# Levantamento bibliográfico: três ideias para o fluxo do agente (10/11/2026)", t)
        self.assertIn("### 6.16 Levantamento do fluxo do agente", t)
        self.assertIn("| §6.16.1 | 1 | `r7-a` | 3 | 2 | 1 | 1 | 1 |", t)
        ordem = [t.index(x) for x in ("#### 6.16.1 ", "#### 6.16.2 ", "#### 6.16.3 Afirmações rejeitadas", "#### 6.16.4 O que o repositório já mediu", "#### 6.16.5 Veredito por ideia",
                                      "#### 6.16.6 Mapa adotado")]
        self.assertEqual(ordem, sorted(ordem))
        for trecho in ("- Rejeitada [F02.a]: afirmação que a fonte não faz", "*Motivo:* a fonte diz o contrário", "- Não verificada [F03.a]:", "- Parcial [F01.b]: afirmação com o número certo",
                       "tabela das medidas", "##### Ideia 1: Ideia um", "Repositório com 5.921 tokens.", "| Tema | Opção | **adiado** | motivo com 3 erros | §6.16.1 |"):
            self.assertIn(trecho, t)
        self.assertNotIn("{{", t)
        self.assertNotIn("→", t)
        com_travessao = [l for l in t.splitlines() if "—" in l]
        self.assertEqual(len(com_travessao), 2)
        self.assertTrue(all(l.startswith("#### 6.16.") for l in com_travessao), "o travessão só fica no cabeçalho de formato fixo de cada tópico")

    # ---------------------------------------------------------------- referências, índice e proposta
    def teste_bloco_de_referencias_entra_antes_do_bloco_da_pos_fase_4_e_nao_desfaz_os_outros(self):
        novo, novas, total = ifa.referencias_com_bloco(REFS, self.dados, TOPICOS_DE_TESTE)
        self.assertEqual((novas, total), (1, 4), "ALFA entra; BETA e GAMA não têm afirmação aprovada; DELTA repete o endereço de uma referência da rodada 6")
        self.assertEqual(novo.count(ifa.TITULO_REFS), 1)
        self.assertLess(novo.index(ifa.TITULO_REFS), novo.index(ipp.TITULO_REFS))
        self.assertLess(novo.index(ipp.TITULO_REFS), novo.index(ip.TITULO_REFS))
        self.assertIn(f"os levantamentos de {ip.DATAS_DOS_LEVANTAMENTOS} produziram as **4** referências abaixo", novo)
        self.assertIn("10/11", ip.DATAS_DOS_LEVANTAMENTOS)
        self.assertIn("- ALFA, A. Primeiro estudo sobre passos.", novo)
        self.assertEqual(novo.count("arxiv.org/abs/2502.00004"), 1)
        self.assertEqual(ifa.referencias_com_bloco(novo, self.dados, TOPICOS_DE_TESTE), (novo, 1, 4), "regravar não muda nada")
        self.assertEqual(ifa.omitidas(REFS, self.dados, TOPICOS_DE_TESTE), [self.dados["r7-b"]["fontes"][0]["referencia"]])
        # os outros dois integradores cortam o arquivo no título do bloco deles: o bloco desta rodada fica inteiro na parte que eles preservam
        self.assertIn(ifa.TITULO_REFS, ipp._sem_o_bloco(novo))
        self.assertIn(ifa.TITULO_REFS, ip._sem_o_bloco(novo))

    def teste_linhas_do_indice_entram_no_lugar_e_sao_regravaveis(self):
        novo = ifa.memorial_com_linhas(MEMORIAL, self.dados, TOPICOS_DE_TESTE)
        self.assertEqual(novo.count(ifa.MARCA_DO_INDICE), 1)
        self.assertEqual(novo.count(ifa.MARCA_DA_PROPOSTA), 1)
        self.assertLess(novo.index(ipp.MARCA_DO_INDICE), novo.index(ifa.MARCA_DO_INDICE))
        self.assertLess(novo.index(ifa.MARCA_DO_INDICE), novo.index("- [Referências levantadas]"))
        self.assertLess(novo.index("- [Protocolo da linha de base manual"), novo.index(ifa.MARCA_DA_PROPOSTA))
        self.assertLess(novo.index(ifa.MARCA_DA_PROPOSTA), novo.index("### 6. Outra seção"))
        self.assertIn("2 tópicos", novo)
        self.assertEqual(ifa.memorial_com_linhas(novo, self.dados, TOPICOS_DE_TESTE), novo)
        self.assertEqual(ipp.memorial_com_linha(novo, {"x": 1}).count(ifa.MARCA_DO_INDICE), 1, "o integrador da Pós-Fase 4 regrava a linha dele sem tocar nas desta rodada")

    def teste_proposta_sai_do_modelo_com_os_marcadores_trocados_e_os_blocos_de_medidas(self):
        texto = ifa.proposta(MODELO, MEDIDAS, blocos={"custos": "| a | b |\n|---|---|\n| 1 | 2 |"})
        self.assertIn("Custa 23,3 s e 5.921 tokens.", texto)
        self.assertIn("| a | b |", texto)
        self.assertNotIn("{{", texto)
        self.assertNotIn("<!-- medidas:custos -->", texto)
        self.assertIn("gerado por ferramentas/integrar_pesquisa_fluxo_do_agente.py", texto)
        with self.assertRaises(SystemExit):
            ifa.proposta(MODELO, MEDIDAS, blocos={})    # o modelo pede um bloco que o script não tem

    def teste_resumo_para_o_painel_traz_as_contagens_e_os_textos_ja_preenchidos(self):
        r = ifa.resumo_para_o_painel(self.dados, SINTESES, MEDIDAS, TOPICOS_DE_TESTE)
        self.assertEqual([t["chave"] for t in r["topicos"]], ["r7-a", "r7-b"])
        self.assertEqual({k: r["topicos"][0][k] for k in ("secao", "frente", "fontes", "aprovadas", "parciais", "rejeitadas", "nao_verificadas")},
                         {"secao": "6.16.1", "frente": "1", "fontes": 3, "aprovadas": 2, "parciais": 1, "rejeitadas": 1, "nao_verificadas": 1})
        self.assertEqual(r["totais"], {"topicos": 2, "fontes": 4, "afirmacoes": 5, "aprovadas": 3, "parciais": 1, "rejeitadas": 1, "nao_verificadas": 1, "referencias_corrigidas": 1})
        self.assertEqual(r["vereditos"][0]["repositorio"], "Repositório com 5.921 tokens.")
        self.assertEqual(r["mapa"][0]["motivo"], "motivo com 3 erros")
        self.assertNotIn("{{", json.dumps(r, ensure_ascii=False))
        self.assertIn("de IA - Revisar", r["_tag"])
        self.assertIn("! Motivo", r["_motivo"])

    def teste_frase_da_fonte_divergente_lista_cada_falha_gravada(self):
        # ! Alteração de IA - Revisar: (10/11/2026, depois da revisão da entrega) a frase que diz, pela falha gravada na trilha, de que tipo foram os casos com a FONTE divergente.
        # ! Motivo: o gatilho junta duas conferências, e o levantamento, a proposta e a ficha 66 descreviam os casos por uma só delas sem número; a frase sai das medidas.
        os72 = {"disparos_da_fonte_divergente": 3, "fonte_divergente_por_falha": [{"falha": "causa_sem_verbete_que_a_trate", "casos": 2, "acertos": 1, "erros": 1},
                                                                                {"falha": "citacao_fora_do_contexto", "casos": 1, "acertos": 1, "erros": 0}]}
        frase = ifa.frase_da_fonte_divergente(os72)
        self.assertIn("os 3 casos em que ela acendeu", frase)
        self.assertIn("2 com a falha `causa_sem_verbete_que_a_trate` (nenhum verbete entregue trata da causa respondida; 1 acerto e 1 erro)", frase)
        self.assertIn("1 com a falha `citacao_fora_do_contexto` (a FONTE cita um verbete fora dos três entregues; 1 acerto e 0 erros)", frase)
        self.assertNotIn("—", frase)

    def teste_texto_do_script_sem_seta_e_com_travessao_so_no_formato_do_cabecalho(self):
        linhas = Path(ifa.__file__).read_text(encoding="utf-8").splitlines()
        for l in linhas:
            self.assertNotIn("→", l, l)
        self.assertLessEqual(sum(1 for l in linhas if "—" in l), 2, "o travessão só aparece no formato fixo do cabeçalho da subseção (e no comentário que o explica)")

    # ---------------------------------------------------------------- arquivos reais
    def teste_arquivos_reais_quando_estao_na_maquina(self):
        if not all((ifa.DADOS / f"{t[0]}.verificacao.json").exists() for t in ifa.TOPICOS) or not ifa.SINTESES.exists() or not ifa.MEDIDAS.exists():
            self.skipTest("as leituras, as segundas leituras, as sínteses ou as medidas não estão nesta máquina")
        dados = ifa.carregar()
        sinteses, medidas = ifa.ler_json(ifa.SINTESES), ifa.ler_json(ifa.MEDIDAS)
        self.assertEqual(list(dados), [t[0] for t in ifa.TOPICOS])
        self.assertEqual(set(sinteses["topicos"]), set(dados), "uma síntese por tópico")
        self.assertEqual([v["ideia"] for v in sinteses["vereditos"]], [1, 2, 3], "um veredito por ideia")
        self.assertEqual(ifa.citacoes_sem_apoio(dados, sinteses), [], "as sínteses só citam fonte com afirmação aprovada na segunda leitura")
        for k in dados:
            citadas = set(ifa.citacoes(sinteses["topicos"][k]))
            self.assertGreaterEqual(len(citadas), 5, f"{k}: a síntese cita poucas fontes")
        for linha in sinteses["mapa"]:
            self.assertIn(linha["veredito"], ("adotado", "adiado", "descartado"), linha["opcao"])
        texto = ifa.render(dados, sinteses, medidas)
        self.assertNotIn("{{", texto)
        self.assertNotIn("→", texto)
        self.assertTrue(all(l.startswith("#### 6.16.") for l in texto.splitlines() if "—" in l))
        # nenhum número do repositório digitado à mão nas sínteses: os textos com marcador são os únicos que falam das corridas com número
        if ifa.LEVANTAMENTO.exists():
            self.assertEqual(ifa.check(), 0)


if __name__ == "__main__":
    unittest.main(verbosity=1)
