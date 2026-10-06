#!/usr/bin/env python3
# ! Alteração de IA - Revisar: testes do integrador da rodada 5 da pesquisa (01/10/2026): a troca da expressão do
# contexto pelo número medido, a numeração fixa das subseções com e sem a parte B, o cabeçalho no formato que o
# painel lê, o texto próprio do script sem travessão nem seta, e a regravação do bloco de referências e da linha do
# índice do Memorial sem duplicar nada.
# ! Motivo: a parte B da rodada entra depois da parte A, no mesmo arquivo. Sem estes testes a segunda integração
# poderia mudar o número de uma subseção já citada no relatório da fase, repetir o bloco de referências (e errar o
# total do arquivo) ou trocar "dezenas de milhares de tokens" de uma fonte pelo número do nosso prompt.
"""Uso: python ferramentas/testar_integrar_pesquisa_pre_fase4.py"""
from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import integrar_pesquisa_pre_fase4 as ip  # noqa: E402
import painel_topicos as tp  # noqa: E402

MEDIDA = {"mediana": 1285.5, "saida": 61.0, "n": 360, "texto": "cerca de 1.300 tokens"}
# ! Alteração de IA - Revisar: (05/10/2026) medida completa, com o prefill, a geração e a memória da máquina, para os
# avisos novos do cabeçalho; e testes das correções declaradas da revisão contra o texto real da parte A.
# ! Motivo: a revisão das sínteses achou frases que comparavam a RAM livre com o mínimo de 16 GB do colibri (a máquina
# tem 16 GB instalados) e frases que davam como fato das fontes o que é medida do projeto (o prefill domina o tempo do
# diagnóstico). O cabeçalho passa a declarar os dois números a partir do JSON, e as correções só entram se cada trecho
# aparecer uma vez só no texto do agente.
MEDIDA_COMPLETA = {**MEDIDA, "prefill_s": 50.8325, "geracao_s": 14.07, "ram_instalada_gb": 16.0, "ram_visivel_gb": 15.69, "ram_livre_gb": 7.2}


def _topico(key: str, refs: list[str], texto: str = "Texto da síntese.") -> dict:
    return {"key": key, "titulo": key,
            "verified": [{"claim_pt": "Afirmação um.", "number": "1", "support": "yes", "ref": refs[0]},
                         {"claim_pt": "Afirmação dois.", "number": "2", "support": "partial", "ref": refs[0]}],
            "rejeitadas": [{"claim": "Afirmação recusada.", "fonte": "Fonte X", "motivo": "a fonte não sustenta o número"}],
            "synthesis": {"titulo": "Título da síntese", "texto_memorial_pt": texto, "implicacoes_fase3_pt": ["Implicação."],
                          "lacunas_pt": ["Lacuna."], "referencias_abnt": refs}}


REF_A = "SILVA, João. Um estudo sobre leitura de pesos do disco. arXiv:2501.00001, 2025. Disponível em: https://arxiv.org/abs/2501.00001."
REF_B = "SOUZA, Maria. Roteamento de especialistas em modelos pequenos. arXiv:2502.00002, 2025. Disponível em: https://arxiv.org/abs/2502.00002."
REF_C = "LIMA, Ana. Probabilidade do rótulo como sinal de incerteza. arXiv:2503.00003, 2025. Disponível em: https://arxiv.org/abs/2503.00003."
MAPA = {"linhas": [{"tema": "Tema", "opcao": "Opção", "veredito": "adotado", "motivo_pt": "Motivo.", "fonte": "SILVA, 2025"}],
        "riscos": [{"risco": "Risco.", "mitigacao": "Mitigação.", "fonte": "SILVA, 2025"}], "leitura_pt": "Leitura."}
REFERENCIAS = ("# Referências\n\n## 9. Referências levantadas\n\n"
               "Além das 7 do projeto de pesquisa, os levantamentos de 11/09, 21/09, 22/09 e 29/09/2026 produziram as **2** referências abaixo, organizadas por tema.\n\n"
               "### Bloco antigo (levantamento de 29/09/2026)\n\n"
               f"- {REF_A}\n- COSTA, Rui. Outro trabalho já citado no arquivo. arXiv:2401.00009, 2024.\n")
INDICE = ("# Memorial\n\n- [Levantamento — qualidade da documentação autogerida (29/09/2026)](memorial/x.md) — §6.13: texto.\n"
          "- [Outra linha](memorial/y.md)\n")


class TestesDoIntegrador(unittest.TestCase):
    def teste_troca_so_a_expressao_que_fala_do_prompt_do_agente(self):
        texto = ("o prefill de alguns milhares de tokens pesa; prompts de milhares de tokens também; "
                 "a fonte mediu contextos de dezenas de milhares de tokens e de centenas de milhares de tokens")
        novo, n = ip.corrigir(texto, MEDIDA["texto"])
        self.assertEqual(n, 2)
        self.assertIn("o prefill de cerca de 1.300 tokens pesa; prompts de cerca de 1.300 tokens também", novo)
        self.assertIn("dezenas de milhares de tokens e de centenas de milhares de tokens", novo)

    def teste_forma_do_tamanho_arredonda_para_a_centena(self):
        self.assertEqual(ip.forma_do_tamanho(1285.5), "cerca de 1.300 tokens")
        self.assertEqual(ip.forma_do_tamanho(940.0), "cerca de 900 tokens")

    def teste_numeracao_fixa_com_e_sem_a_parte_b(self):
        so_a = {"r5-atlas-e-especializacao": _topico("r5-atlas-e-especializacao", [REF_B])}
        com_b = {**so_a, "r5-confianca-por-probabilidade": _topico("r5-confianca-por-probabilidade", [REF_C])}
        t1 = ip.render(so_a, {"A": MAPA}, 0, MEDIDA)
        t2 = ip.render(com_b, {"A": MAPA, "B": MAPA}, 0, MEDIDA)
        for t in (t1, t2):
            self.assertIn("#### 6.14.5 Atlas de especialistas", t)
            self.assertIn("#### 6.14.12 Afirmações rejeitadas", t)
            self.assertIn("#### 6.14.13 Mapas", t)
        self.assertNotIn("#### 6.14.10 ", t1)
        self.assertIn("#### 6.14.10 A probabilidade do rótulo como sinal de incerteza", t2)
        self.assertIn("Esta parte da rodada ainda não rodou.", t1)
        self.assertNotIn("Esta parte da rodada ainda não rodou.", t2)

    def teste_cabecalho_da_subsecao_no_formato_que_o_painel_le(self):
        dados = {"r5-pesos-em-disco": _topico("r5-pesos-em-disco", [REF_A])}
        dados["r5-pesos-em-disco"]["rejeitadas"].append({"claim": "Sem veredito.", "fonte": "Fonte Y", "motivo": f"além do teto de {ip.TETO} verificações: não verificada"})
        linhas = [l for l in ip.render(dados, {"A": MAPA}, 0, MEDIDA).splitlines() if l.startswith("#### 6.14.3 ")]
        self.assertEqual(len(linhas), 1)
        m = tp._TOPICO.match(linhas[0])
        self.assertTrue(m, linhas[0])
        self.assertEqual((m.group(1), m.group(3), m.group(4), m.group(5), m.group(6)), ("6.14.3", "r5-pesos-em-disco", "2", "1", "1"))

    def teste_tabela_do_cabecalho_marca_o_que_ainda_nao_rodou(self):
        t = ip.render({"r5-pesos-em-disco": _topico("r5-pesos-em-disco", [REF_A])}, {"A": MAPA}, 3, MEDIDA)
        self.assertIn("| §6.14.3 | A | `r5-pesos-em-disco` | 2 | 1 | 0 |", t)
        self.assertIn("| §6.14.9 | B | `r5-atribuicao-ao-contexto` | ainda não rodou | | |", t)
        self.assertIn("**2 aprovadas, 1 rejeitada, 0 não verificadas**", t)
        self.assertIn('trocou a expressão por "cerca de 1.300 tokens" nas 3 ocorrências', t)
        self.assertIn("1.285,5 tokens", t)
        self.assertIn("a entrada é cerca de 21 vezes os 61 tokens da resposta mediana", t)

    def teste_texto_do_script_sem_travessao_nem_seta(self):
        t = ip.render({k: _topico(k, [REF_A]) for k in ip.ORDEM_R5}, {"A": MAPA, "B": MAPA}, 0, MEDIDA)
        fora_dos_cabecalhos = [l for l in t.splitlines() if not tp._TOPICO.match(l)]
        self.assertEqual(len(t.splitlines()) - len(fora_dos_cabecalhos), len(ip.ORDEM_R5))
        for l in fora_dos_cabecalhos:
            self.assertNotIn("—", l, l)
            self.assertNotIn("→", l, l)

    def teste_bloco_de_referencias_e_regravavel(self):
        so_a = {"r5-pesos-em-disco": _topico("r5-pesos-em-disco", [REF_A, REF_B])}
        r1, novas1, total1 = ip.referencias_com_bloco(REFERENCIAS, so_a)
        self.assertEqual((novas1, total1), (1, 3))  # REF_A já constava no bloco antigo
        self.assertEqual(r1.count(ip.TITULO_REFS), 1)
        self.assertIn("29/09 e 01/10/2026 produziram as **3** referências abaixo", r1)
        self.assertEqual(r1.count(REF_A), 1)
        r2, novas2, total2 = ip.referencias_com_bloco(r1, so_a)
        self.assertEqual((r2, novas2, total2), (r1, 1, 3))  # a segunda integração não muda nada
        com_b = {**so_a, "r5-confianca-por-probabilidade": _topico("r5-confianca-por-probabilidade", [REF_C, REF_B])}
        r3, novas3, total3 = ip.referencias_com_bloco(r1, com_b)
        self.assertEqual((novas3, total3), (2, 4))
        self.assertEqual(r3.count(ip.TITULO_REFS), 1)
        self.assertEqual((r3.count(REF_B), r3.count(REF_C)), (1, 1))
        self.assertLess(r3.index(REF_C), r3.index(REF_B))  # ordem alfabética dentro do bloco

    def teste_referencias_iguais_pela_url_entram_uma_vez_e_titulos_curtos_nao_se_confundem(self):
        # a mesma fonte citada por duas sínteses em formas diferentes (versão de congresso e preprint): fica a primeira
        congresso = "MUENNIGHOFF, Niklas et al. OLMoE: open mixture-of-experts language models. In: ICLR, 2025. Disponível em: https://arxiv.org/abs/2409.02060."
        preprint = "MUENNIGHOFF, Niklas; SOLDAINI, Luca et al. OLMoE: open mixture-of-experts language models. arXiv:2409.02060, 2024. Disponível em: https://arxiv.org/pdf/2409.02060v3."
        # autor sem vírgula e título de uma ou duas palavras: a chave das outras rodadas cai em "disponivel em https"
        # para os dois, e sem a URL na chave o segundo sumiria
        curto1 = "SJTU-IPADS. PowerInfer. [S. l.]: GitHub, 2024. Disponível em: https://github.com/SJTU-IPADS/PowerInfer."
        curto2 = "GGML-ORG. llama.cpp. [S. l.]: GitHub, 2024. Disponível em: https://github.com/ggml-org/llama.cpp."
        dados = {"r5-pesos-em-disco": _topico("r5-pesos-em-disco", [congresso, curto1]),
                 "r5-moe-pequenos-em-cpu": _topico("r5-moe-pequenos-em-cpu", [preprint, curto2])}
        novo, novas, total = ip.referencias_com_bloco(REFERENCIAS, dados)
        self.assertEqual((novas, total), (3, 5))
        self.assertIn(congresso, novo)
        self.assertNotIn(preprint, novo)
        self.assertIn(curto1, novo)
        self.assertIn(curto2, novo)
        self.assertEqual(ip.omitidas_pela_url(REFERENCIAS, dados), [preprint])
        # e a referência nova cuja URL já consta num bloco antigo do arquivo também não entra
        com_url_antiga = REFERENCIAS + "- **Título antigo em negrito**. 2025. https://arxiv.org/abs/2409.02060\n"
        self.assertEqual(ip.referencias_com_bloco(com_url_antiga, dados)[1], 2)

    def teste_correcoes_da_revisao_sao_aplicadas_uma_vez_e_declaradas(self):
        dados = {"r5-pesos-em-disco": _topico("r5-pesos-em-disco", [REF_A], texto="O modelo roda a 4 tok/s numa GPU. Outra frase.")}
        mapas = {"A": {"linhas": [dict(MAPA["linhas"][0], motivo_pt="Custa 2 ms por token.")], "riscos": [], "leitura_pt": "Leitura."}}
        correcoes = [{"onde": "r5-pesos-em-disco", "de": "a 4 tok/s numa GPU", "para": "a 4 tok/s numa CPU", "motivo": "a afirmação verificada mede em CPU"},
                     {"onde": "mapa:A", "de": "Custa 2 ms", "para": "Custa 2.196 ms", "motivo": "o número da afirmação verificada é 2.196 ms"}]
        self.assertEqual(ip.aplicar_correcoes(dados, mapas, correcoes), 2)
        self.assertEqual(dados["r5-pesos-em-disco"]["synthesis"]["texto_memorial_pt"], "O modelo roda a 4 tok/s numa CPU. Outra frase.")
        self.assertEqual(mapas["A"]["linhas"][0]["motivo_pt"], "Custa 2.196 ms por token.")
        t = ip.render(dados, mapas, 0, MEDIDA, correcoes)
        self.assertIn("**Correções da revisão.**", t)
        self.assertIn("a afirmação verificada mede em CPU", t)
        self.assertIn('"a 4 tok/s numa GPU"', t)
        # sem correção nenhuma o aviso não aparece
        self.assertNotIn("Correções da revisão", ip.render(dados, mapas, 0, MEDIDA, []))
        # correção cujo trecho antigo não existe (ou aparece mais de uma vez) interrompe: correção velha não passa calada
        with self.assertRaises(SystemExit):
            ip.aplicar_correcoes(dados, mapas, correcoes)
        repetido = {"r5-pesos-em-disco": _topico("r5-pesos-em-disco", [REF_A], texto="um ponto. um ponto.")}
        with self.assertRaises(SystemExit):
            ip.aplicar_correcoes(repetido, {}, [{"onde": "r5-pesos-em-disco", "de": "um ponto", "para": "dois", "motivo": "x"}])

    def teste_cabecalho_declara_a_memoria_instalada_e_o_prefill_quando_a_medida_traz(self):
        dados = {"r5-pesos-em-disco": _topico("r5-pesos-em-disco", [REF_A])}
        sem = ip.render(dados, {"A": MAPA}, 0, MEDIDA, [])
        self.assertIn("Quatro avisos sobre o texto abaixo", sem)
        self.assertNotIn("Memória da máquina", sem)
        self.assertNotIn("prefill", sem.split("### 6.14 ")[1].split("#### 6.14.1")[0])
        com = ip.render(dados, {"A": MAPA}, 0, MEDIDA_COMPLETA, [])
        self.assertIn("Cinco avisos sobre o texto abaixo", com)
        self.assertIn("5. **Memória da máquina.**", com)
        self.assertIn("16,0 GB instalados", com)
        self.assertIn("15,69 GB", com)
        self.assertIn("`maquina.ram_instalada_gb`", com)
        self.assertIn("a mediana do prefill é de 50,8 s e a da geração, de 14,1 s", com)
        self.assertIn("o prefill toma a maior parte do tempo de cada diagnóstico", com)
        correcoes = [{"onde": "r5-pesos-em-disco", "de": "Texto da síntese.", "para": "Texto corrigido.", "motivo": "motivo x"}]
        ip.aplicar_correcoes(dados, {"A": MAPA}, correcoes)
        tudo = ip.render(dados, {"A": MAPA}, 0, MEDIDA_COMPLETA, correcoes)
        self.assertIn("Seis avisos sobre o texto abaixo", tudo)
        self.assertIn("6. **Correções da revisão.**", tudo)
        self.assertIn("as correções do aviso 6", tudo)
        self.assertIn("foi corrigido (aviso 6)", tudo)
        self.assertIn("1 trecho foi corrigido por script", tudo)
        self.assertIn(f"por script em {ip.DATA_DAS_CORRECOES}", tudo)

    def teste_medidas_do_projeto_vem_do_json_e_sustentam_o_que_as_correcoes_afirmam(self):
        m = ip.medidas_do_projeto()
        for k in ("mediana", "saida", "n", "texto", "prefill_s", "geracao_s", "ram_instalada_gb", "ram_visivel_gb", "ram_livre_gb"):
            self.assertIn(k, m)
        self.assertGreaterEqual(m["ram_instalada_gb"], m["ram_visivel_gb"])
        # as correções dizem que o prefill toma a maior parte do tempo de cada diagnóstico: só vale se a mediana sustentar
        self.assertGreater(m["prefill_s"], m["geracao_s"])
        self.assertGreater(m["prefill_s"], 0.5 * (m["prefill_s"] + m["geracao_s"]))

    def teste_correcoes_declaradas_batem_com_o_texto_real_da_parte_a(self):
        if not ip.PARTES[0][1].exists():
            self.skipTest("resultado da parte A fora desta máquina (.superpowers não é versionado)")
        self.assertGreater(len(ip.CORRECOES_DA_REVISAO), 100)
        dados, mapas, _ = ip.carregar()  # interrompe se algum trecho não aparecer exatamente uma vez
        for c in ip.CORRECOES_DA_REVISAO:
            campos = ip._campos_de_texto(dados, mapas, c["onde"])
            # o trecho antigo só sobrevive se estiver contido no novo (ex.: "o repositório não tem" dentro de "do repositório não tem")
            self.assertEqual(sum(obj[k].count(c["de"]) for obj, k in campos), c["para"].count(c["de"]), c["de"][:80])
            self.assertGreaterEqual(sum(obj[k].count(c["para"]) for obj, k in campos), 1, c["para"][:80])
            for campo in ("para", "motivo"):
                self.assertNotIn("—", c[campo], c[campo][:80])
                self.assertNotIn("→", c[campo], c[campo][:80])
        # os seis lugares corrigidos: cinco tópicos da parte A e o mapa
        self.assertEqual({c["onde"] for c in ip.CORRECOES_DA_REVISAO}, {k for k in ip.ORDEM_R5 if ip.TITULOS_R5[k][0] == "A"} | {"mapa:A"})

    def teste_linha_do_indice_do_memorial_e_regravavel(self):
        so_a = {k: _topico(k, [REF_A]) for k in ip.ORDEM_R5 if ip.TITULOS_R5[k][0] == "A"}
        m1 = ip.memorial_com_linha(INDICE, so_a)
        self.assertIn("5 de 11 tópicos integrados", m1)
        self.assertEqual(ip.memorial_com_linha(m1, so_a), m1)
        linhas = m1.splitlines()
        i = next(n for n, l in enumerate(linhas) if l.startswith("- [Levantamento — qualidade da documentação autogerida"))
        self.assertTrue(linhas[i + 1].startswith("<!-- ! Alteração de IA - Revisar: linha do índice para o levantamento da Pré-Fase 4"))
        self.assertTrue(linhas[i + 2].startswith("- [Levantamento: Pré-Fase 4 (01/10/2026)]"))
        self.assertEqual(linhas[i + 3], "- [Outra linha](memorial/y.md)")
        m2 = ip.memorial_com_linha(m1, {k: _topico(k, [REF_A]) for k in ip.ORDEM_R5})
        self.assertIn("11 de 11 tópicos integrados", m2)
        self.assertEqual(m2.count("- [Levantamento: Pré-Fase 4 (01/10/2026)]"), 1)
        self.assertEqual(m2.count("linha do índice para o levantamento da Pré-Fase 4"), 1)
        nova = next(l for l in m2.splitlines() if l.startswith("- [Levantamento: Pré-Fase 4"))
        self.assertNotIn("—", nova)

    def teste_rodada_a_real_quando_o_resultado_esta_na_maquina(self):
        if not ip.PARTES[0][1].exists():
            self.skipTest("resultado da parte A fora desta máquina (.superpowers não é versionado)")
        dados, mapas, trocas = ip.carregar()
        self.assertTrue(set(k for k in ip.ORDEM_R5 if ip.TITULOS_R5[k][0] == "A") <= set(dados))
        self.assertGreater(trocas, 0)
        t = ip.render(dados, mapas, trocas, ip.medidas_do_projeto())
        corpo = t[t.index("#### 6.14.1 "):]  # o aviso do cabeçalho cita a expressão antiga entre aspas
        self.assertIsNone(re.search(r"(?<!dezenas de )(?<!centenas de )milhares de tokens", corpo))
        # as correções declaradas não acrescentam nem tiram ocorrências da expressão medida (o cabeçalho conta as trocas);
        # a lista das correções no §6.14.12 repete cada trecho antigo e novo, e fica fora da conta
        lista = ip.bloco_rejeitadas(dados)
        lista = lista[lista.index("**Correções feitas depois da revisão**"):] if "**Correções feitas depois da revisão**" in lista else ""
        self.assertEqual(corpo.count(ip.medidas_do_projeto()["texto"]) - lista.count(ip.medidas_do_projeto()["texto"]), trocas)
        for k in dados:
            self.assertTrue(dados[k].get("synthesis"), k)


if __name__ == "__main__":
    unittest.main(verbosity=1)
