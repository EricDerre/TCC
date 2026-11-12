#!/usr/bin/env python3
# ! Alteração de IA - Revisar: cria testar_pos_fase4.py, o runner de testes da Pós-Fase 4 (pacote Q1: o relatório v3 por
# caso no molde do relatório de defeitos da seção 5.5 do syllabus CTFL 4.0, em `gerar_relatorio_raciocinio.py`, e a camada
# de leitura dos verbetes, `biblioteca_leitura.py`), no mesmo formato sem pytest de testar_fase4.py: funções teste_<nome>(),
# main() roda todas em ordem de definição e termina em "N testes ok". A tag deste cabeçalho cobre as funções de teste e os
# ajudantes de teste. Os testes foram escritos ANTES dos módulos: a primeira rodada falha por ModuleNotFoundError em
# `biblioteca_leitura` e por AttributeError em `relatorio_do_caso_v3`, que é o RED aceito para módulo e função novos.
# ! Motivo: o plano aprovado da Pós-Fase 4 (seção 7, Q1) pede os testes antes do código: as trilhas gravadas das corridas
# 18d, 21d e 24 regeram o v3 sem erro, cada campo da 5.5 presente em cada relatório, hash do prompt fixo inalterado, cada
# verbete da biblioteca com a sua leitura (mesmo id e mesmos campos do frontmatter) e nenhuma leitura dentro do prompt. O
# arquivo é separado de testar_fase4.py porque aquele importa o navegador (Playwright, só na venv) e leva minutos; estes
# testes rodam com o Python do PATH, sem máquina e sem modelo.
# ! Alteração de IA - Revisar: (Pós-Fase 4, pacote Q2) o bloco "Q2: os filtros determinísticos" ao fim do arquivo testa `filtros_de_texto.py`
# e a leitura antes e depois de `avaliar_fase4.py --texto`, escritos ANTES do código: a primeira rodada falha por ModuleNotFoundError em
# `filtros_de_texto`, o RED aceito para módulo novo. Três textos de controle (um bom, um prolixo, um com jargão), a separação silábica
# conferida numa amostra de palavras, a extração da prosa do Markdown, o corpus de referência lido dos "! Motivo:" do repositório e do
# exemplo canônico do Eric sem copiar texto nenhum, a calibração pelo percentil 95, a leitura gravada e conferida com --check e a fumaça
# sobre os relatórios v3 e a camada de leitura reais.
# ! Motivo: o plano aprovado (seções 3.3 e 7, Q2) pede os testes antes do código e os três textos de controle; sem a amostra de sílabas
# conferida, o Flesch adaptado sairia de uma contagem que ninguém conferiu, e sem a fumaça sobre os arquivos reais um limiar poderia reprovar
# o molde do relatório v3 sem ninguém notar (o plano manda ajustar o molde até passar e registrar a leitura antes e depois).
# ! Alteração de IA - Revisar: (08/11/2026, Pós-Fase 4, pacote Q3) o bloco "Q3: a árvore de decisão" ao fim do arquivo testa `arvore_de_decisao.py`,
# escrito ANTES do código: a primeira rodada falha por ModuleNotFoundError em `arvore_de_decisao`, o RED aceito para módulo novo. Os quatro rótulos
# de origem e a regra de que "desconhecido" nunca vira percentual; a árvore de um caso da tela de teste (três decisões, toda afirmação com rótulo,
# os sinais da busca marcados como desconhecidos quando a trilha não os guarda); a confiança em palavras com a taxa de acerto da faixa na calibração
# e sem percentual quando a calibração falta; dois casos reais com divergência (lex-10 na tela, lex-24 em texto) e um caso real com cura
# (localizador-front-busca) conferidos campo a campo; as 83 trilhas vigentes geradas sem erro, com cada nó virando decisão e o Markdown passando
# nos filtros do Q2; a gravação em `arvores/` com índice e `--check`, sem tocar no resto da pasta; e a fumaça de que as árvores das três corridas
# estão gravadas e batem com a regeração.
# ! Motivo: o plano aprovado (seções 3.4 e 7, Q3) pede os testes antes do código, sobre as 83 trilhas das corridas vigentes, incluindo um caso
# com divergência e um com cura; sem o teste do "desconhecido" sem percentual, uma faixa sem calibração sairia com uma taxa inventada, que é o
# risco que o rótulo existe para impedir.
# ! Alteração de IA - Revisar: (08/11/2026, Pós-Fase 4, pacote Q4) o bloco "Q4: a barra de progresso e o protótipo do Git" ao fim do arquivo testa
# `progresso.py` e `impacto_git.py`, escritos ANTES do código: a primeira rodada falha por ModuleNotFoundError em `progresso`, o RED aceito para módulo
# novo. A estimativa das duas fases com taxas conhecidas (prefill pelos tokens do prompt e pela taxa; geração pela mediana de tokens gerados e pela taxa,
# com o teto como máximo); a fração que nunca recua, fica em 90% quando o decorrido iguala a estimativa e segue avançando devagar depois dela; a barra
# indeterminada que vira determinada sem trocar de forma e só chega a 100% na conclusão; o arquivo de estado gravado e lido de volta; o cancelamento
# (Ctrl+C) que grava "cancelado" e encerra limpo; a integração com um Ollama de mentira (a barra redesenhada no terminal, só os marcos quando a saída é um
# arquivo, o estado "concluido", a medida estimado contra real por fase, e o registro da inferência e o corpo enviado iguais aos de antes, também por dentro
# de `diagnostico_ao_vivo.inferir`); as taxas extraídas das corridas vigentes com a origem de cada número e o `--check`; o erro da estimativa medido sobre
# os registros gravados; `executar_fase4.com_progresso` nos modos com modelo e a mesma lista no `.ps1`; e, no protótipo do Git, o mapa lido do frontmatter
# dos verbetes e das rotas dos cenários sem alterar a biblioteca, a seleção com as três regras da base E, o diff de um repositório temporário e de um
# commit conhecido, e a prova sobre o histórico do repositório gravada com `--check`. Os imports `io`, `statistics`, `subprocess` e `time` entraram para
# esses testes.
# ! Motivo: o plano aprovado (seções 3.5, 3.7 e 7, Q4) pede os testes antes do código, o teste com Ollama de mentira e a medida do erro da estimativa; a
# barra observa a chamada ao modelo sem mudar o que ela envia nem o que ela grava, e só um teste que compara os dois lados prova isso; sem o teste da
# fração, uma barra que parasse em 99% passaria despercebida, e é a situação que Harrison et al. (2007) mostram que parece mais lenta.
"""Testes da Pós-Fase 4, sem pytest (asserts em Python puro). Uso (em Programacao/AgenteCore/experimentos):
  PYTHONIOENCODING=utf-8 python testar_pos_fase4.py
"""
import argparse
import contextlib
import inspect
import io
import itertools
import json
import re
import shutil
import statistics
import subprocess
import sys
import tempfile
import time
import traceback
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    with contextlib.suppress(OSError, ValueError, AttributeError):
        sys.stdout.reconfigure(encoding="utf-8")

EXP = Path(__file__).resolve().parent
AGENTE = EXP.parent
RAIZ = AGENTE.parent.parent
RA = EXP / "resultados_alvo"
LEITURAS_VIGENTES = ("tela_v4.json", "cenarios_v4.json", "ineditos.json")   # as três leituras vigentes da Fase 4 (decisões 99 e 100)
TRILHAS_ESPERADAS = {"fase4_tela_v4": {"@tela": 37, "@fixture": 37}, "fase4_ensaio_v4": {"#1": 10}, "fase4_ineditos": {"": 36}}

import biblioteca as bib
import gerar_relatorio_raciocinio as grr
import trilha

_TEMPORARIOS: list[Path] = []
TS = "2026-11-06T09:53:45"
CONTRATO = "id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano"
RESPOSTA_TELA = ("CAUSA_RAIZ: resposta_truncada\nCAMPO: nenhum\nIMPACTO: A interface exibiu uma tela vazia, enquanto esperava 14 cartões.\n"
                 "FONTE: [resposta_truncada]")
RESPOSTA_LOCALIZADOR = ("CAUSA_RAIZ: localizador_quebrado\nCAMPO: nenhum\nIMPACTO: O usuário não consegue iniciar uma busca.\n"
                        "FONTE: [localizador_quebrado]")
RESPOSTA_TEXTO = ("CAUSA_RAIZ: corpo_nao_e_json\nCAMPO: nenhum\nIMPACTO: A página Produtos exibe uma mensagem de erro.\n"
                  "FONTE: [corpo_nao_e_json]")
CASO_ESCRITO = ("REQUISIÇÃO: GET /api/produtos\n\nSTATUS HTTP: 200\n\nCONTRATO ESPERADO PELA INTERFACE: " + CONTRATO +
                "\n\nCORPO DA RESPOSTA:\n<html><body><h1>Erro</h1></body></html>\n\n"
                "SINTOMA OBSERVADO: A pagina Produtos (API) abre sem nenhum cartao e a linha de status fica vermelha.\n\n"
                "OBSERVAÇÃO ADICIONAL: O Content-Type da resposta e text/html, nao application/json.")
JARGAO_PROIBIDO = ("prov.used", "gen_ai", "logprob", "wasDerivedFrom", "hit@3")


def _temp() -> Path:
    p = Path(tempfile.mkdtemp(prefix="pos_fase4_teste_"))
    _TEMPORARIOS.append(p)
    return p


def _cabecalho(corrida: str, modo: str, com_navegador: bool = True) -> dict:
    return trilha.cabecalho_de_corrida(modelo="qwen2.5:7b", versao_ollama="0.40.14", inicio="2026-11-06T09:53:30", quantizacao="Q4_K_M",
                                       hash_biblioteca="95af35290860", hash_prompt_fixo="2e42cf9c31826941", hash_indice="11e763ba9cb1fdf4",
                                       playwright="1.64.1" if com_navegador else None, navegador="156.0.8078.4" if com_navegador else None,
                                       canal="chromium" if com_navegador else None, corrida=corrida, extras={"modo": modo, "k": 3})


def _declaracoes_e_verificacoes(t: trilha.Trilha, tid: str, s_inf: int, resposta: str, entregues: list[str]) -> list[dict]:
    decl = trilha.localizar_declaracoes(resposta)
    for chave, _ in trilha._CAMPOS:
        item = decl["campos"][chave]
        lido = decl["lido"]["fonte_ids"] if chave == "fonte" else decl["lido"][chave]
        dados = {"campo": chave, "ausente": True, "valor": None, "lido": lido} if item is None else {"campo": chave, "lido": lido, **item}
        t.evento("declaracao", tid, dados, "ao_vivo", pai=s_inf, ts=TS)
    for f in decl["fontes"]:
        t.evento("declaracao", tid, {"campo": "fonte_citada", **f}, "ao_vivo", pai=s_inf, ts=TS)
    causa = decl["lido"]["causa_raiz"]
    citado = decl["lido"]["fonte_ids"][0]
    verificacoes = [trilha._v("quatro_linhas_presentes", "resposta", "confere", {"ausentes": []}),
                    trilha._v("rotulo_no_conjunto", causa, "confere", "23 causas permitidas"),
                    trilha._v("fonte_existe_na_biblioteca", citado, "confere", None),
                    trilha._v("fonte_estava_no_contexto", citado, "confere", {"contexto": entregues}),
                    trilha._v("campo_existe_no_caso", "nenhum", "nao_se_aplica", "o modelo não apontou campo"),
                    trilha._v("rotulo_sustentado_por_verbete_do_contexto", causa, "confere", {"verbetes": [citado]}),
                    trilha._v("impacto", decl["lido"]["impacto"], "nao_verificavel", "a frase de impacto não tem contraparte no caso para conferir por código"),
                    trilha._v("fonte_formato_valido", f"[{citado}]", "confere", {"ids": [citado], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"}),
                    trilha._v("fonte_contem_termo_da_causa", citado, "confere", {"termo": causa})]
    for v in verificacoes:
        t.evento("verificacao", tid, v, "ao_vivo", pai=s_inf, ts=TS)
    return verificacoes


def _busca_e_inferencia(t: trilha.Trilha, tid: str, entregues: list[str], resposta: str, pai: int | None) -> tuple[int, int]:
    itens = [{"id": i, "posicao": n + 1, "pontuacao": 30.0 - n, "bm25": 30.0 - n, "reforco_endpoint": 0.0, "reforco_entidade": 0.0,
              "reforco_status": 0.0, "escolhido": True} for n, i in enumerate(entregues)]
    itens.append({"id": "limites-do-sistema", "posicao": 4, "pontuacao": 19.7, "bm25": 19.7, "reforco_endpoint": 0.0, "reforco_entidade": 0.0,
                  "reforco_status": 0.0, "escolhido": False})
    s_cand = t.evento("candidatos", tid, {"k": 3, "hash_indice": "11e763ba9cb1fdf4", "itens": itens}, "ao_vivo", pai=pai, ts=TS)
    s_prompt = t.evento("prompt", tid, {"etapa": "diagnostico", "sha": t.blob("DOCUMENTAÇÃO DO SISTEMA ... (prompt de teste)", "prompt"), "chars": 3938,
                                        "prompt_sha256": "23f9d2879369", "hash_prompt_fixo": "2e42cf9c31826941", "verbetes_ids": entregues},
                        "ao_vivo", pai=s_cand, ts=TS)
    s_inf = t.evento("inferencia", tid, {"etapa": "diagnostico", "resposta": t.blob(resposta, "resposta"), "segundos": 87.8, "tokens_entrada": 1218,
                                         "tokens_saida": 65, "prefill_ms": 61610, "geracao_ms": 15040, "done_reason": "stop", "top_logprobs": 20},
                     "ao_vivo", pai=s_prompt, ts=TS)
    return s_cand, s_inf


def _no_diagnostico(t: trilha.Trilha, tid: str, escolha: str, segunda: str, entregues: list[str], evidencia: list[dict], s_inf: int,
                    verificacoes: list[dict], selo: str, p: float, campo=None, divergencia: dict | None = None) -> dict:
    no = trilha.no_de_decisao("diagnostico", escolha,
                              alternativas=[{"opcao": escolha, "escore": p, "sustentada_por": [escolha]}, {"opcao": segunda, "escore": 0.001, "sustentada_por": []}],
                              evidencia=evidencia + [{"seq": s_inf, "papel": "resposta"}], resultado="rotulo_emitido",
                              divergencia=divergencia or {"ha": False, "entre": [], "detalhe": None},
                              confianca={"logprob_rotulo": -0.001, "p_rotulo": p, "alternativas_top": 20, "selo": selo, "leitura": "primeiro_token_do_rotulo",
                                         "limiares": {"baixo_ate": 0.8317943867608124, "alto_a_partir_de": 0.9898271080008889}},
                              prov={"used": entregues}, extras={"campo": campo, "gatilhos": {"probabilidade": selo == "baixo", "fonte_divergente": False, "amostra": False,
                                                                                            "algum": selo == "baixo"}, "intervencoes": [], "intervencoes_puladas": None,
                                                                "k": 3, "modo_de_intervencao": "desligadas"})
    no["justificativa"] = grr.justificativa_por_molde(no, eventos=t.eventos, verificacoes=verificacoes, intervencoes=[])
    no["contraste"] = grr.contraste_por_molde(no)
    t.decisao(tid, no, pai=s_inf, ts=TS)
    return no


def _trilha_tela(corrida: str = "_fumaca_q1", caso: str = "lex-1", selo: str = "alto", p: float = 0.9989, resposta: str = RESPOSTA_TELA,
                 divergencia: dict | None = None) -> tuple[trilha.Trilha, str]:
    """Uma trilha v2 com um caso da tela (como a corrida 18d grava)."""
    t = trilha.Trilha(versao=trilha.V2)
    t.corrida(_cabecalho(corrida, "tela"), ts="2026-11-06T09:53:30")
    tid = _caso_na_tela(t, corrida, caso, selo, p, resposta, divergencia)
    t.fechar(fim="2026-11-06T11:12:59")
    return t, tid


def _caso_na_tela(t: trilha.Trilha, corrida: str, caso: str, selo: str, p: float, resposta: str = RESPOSTA_TELA, divergencia: dict | None = None) -> str:
    """Acrescenta à trilha `t` um caso da tela: roteiro, interceptação, conferência que falhou, poda da árvore e do corpo, busca, prompt,
    inferência, declarações, conferências e o nó `diagnostico`. Devolve o id da trilha do caso."""
    tid = f"{corrida}/qwen2.5_7b/{caso}@tela"
    caso_vivo = {"id": f"{caso}@tela", "classe": 1, "nivel": 1, "origem": "ao_vivo", "corpo_completo": '[{"id": 1, "nome": "resposta truncada de propos',
                 "entrada": {"requisicao": "GET /api/produtos", "status": 200, "contrato": CONTRATO, "corpo": '...[{"id": 1, "nome": "resposta truncada de propos',
                             "sintoma": "A conferência 'grid com 14 cartões' falhou: esperava 14 elementos; viu 0 elementos. A resposta veio cortada.",
                             "arvore": 'document "Produtos (API)"\n    text "Erro ao carregar produtos da CobaiaAPI"'},
                 "observacao_da_poda": "poda: árvore com 54 nós e 21 linhas depois; corpo truncado"}
    t.evento("entrada", tid, {"caso": caso, "classe": 1, "nivel": 1, "modo": "malformed_json", "campo": None, "cenario": "api-catalogo",
                              "produto_id": None, "caso_ao_vivo": t.blob(json.dumps(caso_vivo, ensure_ascii=False), "caso_ao_vivo")}, "ao_vivo", ts=TS)
    t.evento("acao", tid, {"passo": 1, "acao": "abrir", "seletor": None, "url": "produtos_api.php", "tempo_ms": 111.9, "falhou": False}, "ao_vivo", ts=TS)
    t.evento("acao", tid, {"passo": 2, "acao": "esperar", "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "url": None,
                           "tempo_ms": 6.5, "falhou": False}, "ao_vivo", ts=TS)
    t.evento("acao", tid, {"passo": 3, "acao": "conferir", "seletor": "#produtos-api-grid .saiba-mais", "url": None, "tempo_ms": 2.0, "falhou": True}, "ao_vivo", ts=TS)
    s_int = t.evento("interceptacao", tid, {"metodo": "GET", "caminho": "/api/produtos", "consulta": "", "host": "localhost:8000", "status": 200,
                                            "content_type": "application/json", "content_length": 47, "corpo_chars": 47, "tempo_ms": 32.7, "tipo_recurso": "fetch",
                                            "corpo": t.blob('[{"id": 1, "nome": "resposta truncada de propos', "corpo_http"), "corpo_sha": "8d7d3410d730489f",
                                            "aresta": {"de": "produtos_api.php", "para": "GET /api/produtos", "host": "localhost:8000", "tipo": "chamada_http"}},
                     "ao_vivo", ts=TS)
    t.evento("verificacao", tid, trilha._v("conferencia_do_roteiro", "grid com 14 cartões", "nao_confere", {"esperado": "14 elementos", "observado": "0 elementos"}),
             "ao_vivo", ts=TS)
    s_arv = t.evento("poda", tid, {"alvo": "arvore", "antes": {"nos": 54}, "depois": {"linhas": 21}, "regras": {"cartoes_omitidos": 0, "imagens_removidas": 2},
                                   "diff": [{"campo": "arvore", "esperado": "22 linha(s) da referência", "recebido": "4 linha(s) novas"}],
                                   "sha": t.blob('document "Produtos (API)"\n  main\n    text "Erro ao carregar produtos da CobaiaAPI"', "arvore_podada")}, "ao_vivo", ts=TS)
    s_poda = t.evento("poda", tid, {"alvo": "corpo_http", "antes": {"chars": 47}, "depois": {"chars": 50}, "regras": ["diff_contra_contrato"],
                                    "diff": [{"campo": None, "esperado": "JSON completo e válido", "recebido": "corpo truncado", "tipo": "truncado"}],
                                    "sha": t.blob('...[{"id": 1, "nome": "resposta truncada de propos', "corpo_podado")}, "ao_vivo", ts=TS)
    entregues = ["resposta_truncada", "contagem_inconsistente", "entidade-produto"]
    s_cand, s_inf = _busca_e_inferencia(t, tid, entregues, resposta, None)
    verificacoes = _declaracoes_e_verificacoes(t, tid, s_inf, resposta, entregues)
    evidencia = [{"seq": s_poda, "papel": "sinal_em_codigo"}, {"seq": s_arv, "papel": "arvore_podada"}, {"seq": s_int, "papel": "corpo_http"}] + \
        [{"seq": s_cand, "papel": "verbete_entregue", "id": i} for i in entregues]
    _no_diagnostico(t, tid, "resposta_truncada", "corpo_nao_e_json", entregues, evidencia, s_inf, verificacoes, selo, p, divergencia=divergencia)
    return tid


def _trilha_localizador(corrida: str = "_fumaca_q1") -> tuple[trilha.Trilha, str]:
    """Uma trilha v2 de uma execução de localizador do ensaio (como a corrida 21d grava): a quebra, o passo que falhou, o diagnóstico,
    a cura com os candidatos, a reexecução validada."""
    tid = f"{corrida}/qwen2.5_7b/localizador-front-busca#1"
    t = trilha.Trilha(versao=trilha.V2)
    t.corrida(_cabecalho(corrida, "cenarios"), ts="2026-11-06T11:13:26")
    alvo = {"papel": "searchbox", "nome": "search", "ocorrencia": 1, "seletor": "#buscar", "tag": "input", "caminho": "#form-busca > div:nth-of-type(1) > input:nth-of-type(1)",
            "atributos": {"id": "buscar", "name": "buscar", "placeholder": "Buscar produto"}}
    caso_vivo = {"id": "localizador-front-busca#1", "origem": "ao_vivo", "entrada": {"requisicao": "GET index.php", "status": 200, "contrato": "n/a",
                 "seletor_quebrado": "#buscar", "sintoma": "O passo 2 (esperar #buscar) falhou: o localizador não resolveu em 5 s."}}
    s_ent = t.evento("entrada", tid, {"roteiro": "front-busca", "cenario_da_fase_5": "localizador-front-busca", "repeticao": 1, "passo": 1, "localizador": "#buscar",
                                      "seletor_original": "#buscar", "modo": "id_renomeado", "forma": "harness", "quebra_aplicada": "1",
                                      "armado": {"forma": "harness", "modo": "id_renomeado", "como": "add_init_script no DOMContentLoaded", "mutacoes": 1},
                                      "mutacoes": [{"op": "renomear_id", "seletor": "#buscar", "para": "buscar_v2"}],
                                      "descricao": "o campo de busca perde o id `buscar` (vira `buscar_v2`); o roteiro localiza por `#buscar`",
                                      "alvo": alvo, "erro_da_referencia": None, "caso_ao_vivo": t.blob(json.dumps(caso_vivo, ensure_ascii=False), "caso_ao_vivo")},
                     "ao_vivo", ts=TS)
    t.evento("acao", tid, {"passo": 1, "acao": "abrir", "seletor": None, "url": "index.php", "tempo_ms": 172.7, "falhou": False, "reexecucao": 0}, "ao_vivo", pai=s_ent, ts=TS)
    t.evento("acao", tid, {"passo": 2, "acao": "esperar", "seletor": "#buscar", "url": None, "tempo_ms": 5019.2, "falhou": True, "reexecucao": 0}, "ao_vivo", pai=s_ent, ts=TS)
    s_arv = t.evento("poda", tid, {"alvo": "arvore", "antes": {"nos": 250}, "depois": {"linhas": 37}, "regras": {"cartoes_omitidos": 16}, "diff": [],
                                   "sha": t.blob('document "Churrascaria"\n  searchbox "search" id="buscar_v2"', "arvore_podada"), "arvore_completa_sha": "a38fdc1b98a186f6"},
                     "ao_vivo", pai=s_ent, ts=TS)
    entregues = ["localizador_quebrado", "tempo_de_resposta_excedido", "limites-do-sistema"]
    s_cand, s_inf = _busca_e_inferencia(t, tid, entregues, RESPOSTA_LOCALIZADOR, None)
    verificacoes = _declaracoes_e_verificacoes(t, tid, s_inf, RESPOSTA_LOCALIZADOR, entregues)
    evidencia = [{"seq": s_arv, "papel": "arvore_podada"}] + [{"seq": s_cand, "papel": "verbete_entregue", "id": i} for i in entregues]
    _no_diagnostico(t, tid, "localizador_quebrado", "tempo_de_resposta_excedido", entregues, evidencia, s_inf, verificacoes, "medio", 0.9088)
    candidatos = [{"estrategia": "papel_e_nome", "seletor": 'role=searchbox[name="search"]', "gerado": True, "motivo": "a árvore podada tem 1 searchbox \"search\"",
                   "passou_estaticas": True, "reexecutado": True, "aplicado": True, "cadeia": ['role=searchbox[name="search"]'], "falha": None,
                   "efeito": {"resultado": "confere", "detalhe": "o roteiro chegou ao fim: 2 conferência(s) passaram em 0.399 s", "segundos": 0.399},
                   "verificacoes": {"resolve_um_elemento": {"resultado": "confere", "detalhe": "1 elemento"}, "visivel_e_habilitado": {"resultado": "confere", "detalhe": None},
                                    "mesmo_papel": {"resultado": "confere", "detalhe": "papel 'searchbox'"}, "nome_parecido": {"resultado": "confere", "detalhe": "1.0"},
                                    "efeito_na_reexecucao": {"resultado": "confere", "detalhe": "o roteiro chegou ao fim"}}},
                  {"estrategia": "caminho_do_ancestral_com_id", "seletor": "#form-busca > div:nth-of-type(1) > input:nth-of-type(1)", "gerado": True, "motivo": "ancestral #form-busca",
                   "passou_estaticas": True, "reexecutado": False, "aplicado": False, "falha": None, "efeito": None,
                   "verificacoes": {"resolve_um_elemento": {"resultado": "confere", "detalhe": "1 elemento"}, "visivel_e_habilitado": {"resultado": "confere", "detalhe": None},
                                    "mesmo_papel": {"resultado": "confere", "detalhe": "papel 'searchbox'"}, "nome_parecido": {"resultado": "confere", "detalhe": "1.0"},
                                    "efeito_na_reexecucao": {"resultado": "nao_tentado", "detalhe": None}}},
                  {"estrategia": "data_nome", "seletor": None, "gerado": False, "motivo": "o alvo não tem data-nome", "passou_estaticas": False, "reexecutado": False,
                   "aplicado": False, "falha": None, "efeito": None, "verificacoes": {}}]
    cura = {"passo": 2, "localizador": "#buscar", "erro": "TimeoutError: Page.wait_for_selector: Timeout 5000ms exceeded. Call log: - waiting for locator(\"#buscar\") to be visible",
            "alvo": alvo, "limiar_nome": 0.8, "candidatos": candidatos, "aplicado": {"estrategia": "papel_e_nome", "seletor": 'role=searchbox[name="search"]'},
            "curado": True, "mesmo_elemento": True, "reexecucoes": 1, "falha": None, "mttr_s": 79.1, "deteccao": "2026-11-06T11:22:10", "validacao": "2026-11-06T11:23:29"}
    cura["justificativa"] = grr.justificativa_da_cura(cura)
    s_cura = t.evento("cura", tid, cura, "ao_vivo", pai=s_arv, ts="2026-11-06T11:23:23")
    no_cura = trilha.no_de_decisao("cura", "papel_e_nome",
                                   alternativas=[{"opcao": "papel_e_nome", "escore": 5, "aplicado": True, "seletor": 'role=searchbox[name="search"]'},
                                                 {"opcao": "caminho_do_ancestral_com_id", "escore": 4, "aplicado": False, "seletor": "#form-busca > div:nth-of-type(1) > input:nth-of-type(1)"}],
                                   evidencia=[{"seq": s_cura, "papel": "candidato_de_seletor"}, {"seq": s_arv, "papel": "arvore_podada"}], resultado="curado",
                                   divergencia={"ha": True, "entre": ["programa", "verificacao"], "detalhe": "o segundo candidato também passou as verificações estáticas e não foi tentado: a ordem fixa decidiu"},
                                   prov={"used": ["papel_e_nome"]}, contraste="`papel_e_nome` e não `caminho_do_ancestral_com_id`: o segundo também passou as verificações estáticas, mas vem depois na ordem fixa.",
                                   justificativa=cura["justificativa"])
    t.decisao(tid, no_cura, pai=s_cura, ts="2026-11-06T11:23:23")
    t.evento("acao", tid, {"passo": 1, "acao": "abrir", "seletor": None, "url": "index.php", "tempo_ms": 198.7, "falhou": False, "reexecucao": 1, "candidato": "papel_e_nome", "curado": False},
             "ao_vivo", pai=s_cura, ts="2026-11-06T11:23:23")
    t.evento("acao", tid, {"passo": 2, "acao": "esperar", "seletor": 'role=searchbox[name="search"]', "url": None, "tempo_ms": 5.7, "falhou": False, "reexecucao": 1,
                           "candidato": "papel_e_nome", "curado": True}, "ao_vivo", pai=s_cura, ts="2026-11-06T11:23:23")
    s_v = t.evento("verificacao", tid, trilha._v("conferencia_do_roteiro", "dois produtos com Picanha no nome", "confere",
                                                {"esperado": "2 elementos", "observado": "2 elementos", "candidato": "papel_e_nome", "reexecucao": 1}), "ao_vivo", pai=s_cura, ts="2026-11-06T11:23:23")
    no_re = trilha.no_de_decisao("reexecucao", "validada", alternativas=[{"opcao": "validada"}, {"opcao": "falhou"}],
                                 evidencia=[{"seq": s_cura, "papel": "candidato_de_seletor"}, {"seq": s_v, "papel": "sinal_em_codigo"}], resultado="roteiro_concluido",
                                 divergencia={"ha": False, "entre": [], "detalhe": "o roteiro passou e o elemento é o mesmo da referência"}, prov={"used": ["papel_e_nome"], "wasGeneratedBy": s_cura},
                                 extras={"mesmo_elemento": True})
    t.decisao(tid, no_re, pai=s_cura, ts="2026-11-06T11:23:23")
    t.fechar(fim="2026-11-06T11:26:54")
    return t, tid


def _trilha_texto(corrida: str = "_fumaca_q1", caso: str = "lex-22") -> tuple[trilha.Trilha, str]:
    """Uma trilha v2 de um caso lido em texto (como a corrida 24 grava): entrada com o texto do caso, busca, prompt, inferência e o nó."""
    tid = f"{corrida}/qwen2.5_7b/{caso}"
    t = trilha.Trilha(versao=trilha.V2)
    t.corrida(_cabecalho(corrida, "ineditos", com_navegador=False), ts="2026-11-06T13:52:23")
    t.evento("entrada", tid, {"caso": caso, "classe": 1, "nivel": 1, "origem": "fixture", "texto": t.blob(CASO_ESCRITO, "caso")}, "ao_vivo", ts="2026-11-06T13:52:34")
    entregues = ["corpo_nao_e_json", "mensagens-de-erro-do-codigo", "corpo_vazio"]
    s_cand, s_inf = _busca_e_inferencia(t, tid, entregues, RESPOSTA_TEXTO, None)
    verificacoes = _declaracoes_e_verificacoes(t, tid, s_inf, RESPOSTA_TEXTO, entregues)
    evidencia = [{"seq": s_cand, "papel": "verbete_entregue", "id": i} for i in entregues]
    _no_diagnostico(t, tid, "corpo_nao_e_json", "corpo_vazio", entregues, evidencia, s_inf, verificacoes, "baixo", 0.71)
    t.fechar(fim="2026-11-06T14:35:54")
    return t, tid


def _leituras_de_teste() -> dict:
    """A camada de leitura gerada numa pasta temporária a partir da biblioteca de produção, carregada como o relatório a lê."""
    import biblioteca_leitura as bl
    pasta = _temp() / "leitura"
    bl.gerar(bl.PASTA_BIBLIOTECA, pasta, gerado_em="2026-11-07")
    return bl.carregar(pasta)


def _secao(texto: str, nome: str) -> str:
    """O texto de uma seção `## N. nome` (ou `## nome`) até a próxima seção de segundo nível."""
    m = re.search(r"^## (?:\d+\. )?" + re.escape(nome) + r"\s*$(.*?)(?=^## |\Z)", texto, flags=re.DOTALL | re.MULTILINE)
    assert m, f"seção {nome!r} ausente"
    return m.group(1)


def _sem_codigo(texto: str) -> str:
    """O texto sem os blocos de código e sem os trechos entre crases (onde valores literais do modelo e do caso ficam como vieram)."""
    sem_blocos = re.sub(r"```.*?```", "", texto, flags=re.DOTALL)
    return re.sub(r"`[^`\n]*`", "", sem_blocos)


def _conferir_v3(texto: str) -> None:
    """O que todo relatório v3 tem de ter: os onze campos da 5.5 na ordem, os seis blocos mantidos do v2 depois deles, o rastro,
    nenhum travessão nem seta fora dos trechos literais e nenhum jargão da trilha no texto corrido."""
    posicoes = []
    for n, nome in enumerate(grr.CAMPOS_55 + grr.SECOES_MANTIDAS_V3, start=1):
        m = re.search(rf"^## {n}\. {re.escape(nome)}\s*$", texto, flags=re.MULTILINE)
        assert m, f"falta a seção '## {n}. {nome}'"
        posicoes.append(m.start())
    assert posicoes == sorted(posicoes), "as seções não estão na ordem fixa"
    assert "## Rastro" in texto and texto.rfind("## Rastro") > posicoes[-1]
    prosa = _sem_codigo(texto)
    assert "—" not in prosa and "→" not in prosa, "travessão ou seta no texto corrido"
    for termo in JARGAO_PROIBIDO:
        assert termo not in prosa, f"jargão da trilha no texto: {termo}"


# ----------------------------------------------------------------------------- Q1: o relatório v3 no molde da 5.5

def teste_v3_tem_os_onze_campos_da_55_na_ordem_e_os_blocos_do_v2_depois():
    assert len(grr.CAMPOS_55) == 11 and grr.CAMPOS_55[0] == "Identificador" and grr.CAMPOS_55[-1] == "Referências"
    assert grr.CAMPOS_55[7:10] == ("Severidade", "Prioridade", "Estado"), "os três campos do analista vêm antes das referências"
    assert len(grr.SECOES_MANTIDAS_V3) == 6 and grr.SECOES_MANTIDAS_V3[0] == "Veredito do agente"
    t, tid = _trilha_tela()
    texto = grr.relatorio_do_caso_v3(t.eventos, tid, comando_reexecucao="python executar_fase4.py --modo tela --ids lex-1", leituras=_leituras_de_teste(),
                                     arquivo_trilha="trilha_tela.jsonl")
    _conferir_v3(texto)
    assert texto.startswith("<!-- ! Alteração de IA - Revisar:") and "! Motivo:" in texto[:1200], "o relatório derivado leva a tag e o motivo"
    assert grr.MARCA_DO_MOLDE in _secao(texto, "Veredito do agente")
    assert "python executar_fase4.py --modo tela --ids lex-1" in _secao(texto, "Descrição para reproduzir")
    assert f"`{grr.hash_da_trilha(t.eventos, tid)}`" in _secao(texto, "Referências") and "trilha_tela.jsonl" in _secao(texto, "Referências")


def teste_v3_identificador_titulo_autor_e_referencias_vem_da_trilha_e_da_camada_de_leitura():
    t, tid = _trilha_tela()
    leituras = _leituras_de_teste()
    texto = grr.relatorio_do_caso_v3(t.eventos, tid, leituras=leituras, relatorio_v2="relatorios/lex-1@tela.md")
    titulo = next(l for l in texto.splitlines() if l.startswith("# "))
    assert "Resposta truncada" in titulo and "GET /api/produtos" in titulo, titulo
    assert "resposta_truncada" not in titulo, "o título diz a causa em palavras, pelo título do verbete da camada de leitura"
    ident = _secao(texto, "Identificador")
    assert f"`{tid}`" in ident and "`lex-1`" in ident and "`_fumaca_q1`" in ident
    autor = _secao(texto, "Data, organização e autor")
    assert "06/11/2026" in autor and "09:53:45" in autor and "qwen2.5:7b" in autor and "95af35290860" in autor
    assert "revisão humana" in autor, "o autor é o agente, e o relatório diz que ninguém revisou ainda"
    objeto = _secao(texto, "Objeto de teste e ambiente")
    for trecho in ("produtos_api.php", "GET /api/produtos", "localhost:8000", "0.40.14", "1.64.1", "156.0.8078.4", "95af35290860", "ambiente.json", "num_ctx 8192"):
        assert trecho in objeto, trecho
    contexto = _secao(texto, "Contexto")
    assert "api-catalogo" in contexto and "passo 3" in contexto and "malformed_json" in contexto and "classe 1" in contexto and "nível 1" in contexto
    refs = _secao(texto, "Referências")
    assert "biblioteca_producao_leitura/erros/resposta_truncada.md" in refs, "a FONTE citada aponta para a camada de leitura"
    assert "biblioteca_producao_leitura/erros/contagem_inconsistente.md" in refs and "biblioteca_producao_leitura/negocio/entidade-produto.md" in refs, \
        "os verbetes entregues também apontam para a camada de leitura"
    assert "relatorios/lex-1@tela.md" in refs and "banco_casos" in refs
    for nome in ("Severidade", "Prioridade"):
        s = _secao(texto, nome)
        assert grr.EM_BRANCO in s and "classe 1 (" in s and "nível 1 (" in s, nome
    assert _secao(texto, "Estado").strip().startswith("aberto")


def teste_v3_escreve_codigos_com_o_significado_e_sem_jargao():
    t, tid = _trilha_tela()
    texto = grr.relatorio_do_caso_v3(t.eventos, tid, leituras=_leituras_de_teste())
    repro = _secao(texto, "Descrição para reproduzir")
    assert f"status 200 ({grr.STATUS_EM_PALAVRAS[200]})" in repro, "código de situação com o significado junto"
    assert "1. abrir `produtos_api.php`" in repro.lower() or "1. Abrir `produtos_api.php`" in repro, "os passos do roteiro até a falha"
    assert "falhou" in repro and "grid com 14 cartões" in repro and "14 elementos" in repro and "0 elementos" in repro
    assert "resposta truncada de propos" in repro, "o trecho da resposta, como a poda deixou"
    contexto = _secao(texto, "Contexto")
    assert f"`malformed_json` ({grr.MODO_EM_PALAVRAS['malformed_json']})" in contexto, "o modo de injeção com o significado junto"
    esperado = _secao(texto, "Resultado esperado e resultado real")
    assert "JSON completo e válido" in esperado and "corpo truncado" in esperado and CONTRATO in esperado
    assert "22 linha(s) da referência" in esperado and "4 linha(s) novas" in esperado
    veredito = _secao(texto, "Veredito do agente")
    assert grr.SELO_EM_PALAVRAS["alto"] in veredito and "1,00" in veredito, "o selo em palavras, com a probabilidade"
    assert "texto do modelo" in veredito and "14 cartões" in veredito, "a frase de impacto é rotulada como texto do modelo"
    assert "Resposta truncada" in veredito and "resposta_truncada" in veredito, "a causa em palavras ao lado do rótulo"
    for selo in ("alto", "medio", "baixo"):
        assert grr.SELO_EM_PALAVRAS[selo] and "selo" not in grr.SELO_EM_PALAVRAS[selo].lower()
    t2, tid2 = _trilha_tela(selo="baixo", p=0.61)
    veredito2 = _secao(grr.relatorio_do_caso_v3(t2.eventos, tid2), "Veredito do agente")
    assert grr.SELO_EM_PALAVRAS["baixo"] in veredito2 and "hipótese" in veredito2
    t3, tid3 = _trilha_tela(divergencia={"ha": True, "entre": ["modelo", "verificacao"], "detalhe": "o campo declarado não aparece no caso"})
    assert "o campo declarado não aparece no caso" in _secao(grr.relatorio_do_caso_v3(t3.eventos, tid3), "Veredito do agente")


def teste_v3_caso_de_texto_e_de_localizador():
    leituras = _leituras_de_teste()
    t, tid = _trilha_texto()
    texto = grr.relatorio_do_caso_v3(t.eventos, tid, leituras=leituras)
    _conferir_v3(texto)
    titulo = next(l for l in texto.splitlines() if l.startswith("# "))
    assert "Corpo não é JSON" in titulo and "GET /api/produtos" in titulo, titulo
    objeto = _secao(texto, "Objeto de teste e ambiente")
    assert "sem navegador" in objeto and "GET /api/produtos" in objeto
    repro = _secao(texto, "Descrição para reproduzir")
    assert "GET /api/produtos" in repro and "<html><body><h1>Erro</h1>" in repro and "linha de status fica vermelha" in repro and "text/html" in repro
    assert f"status 200 ({grr.STATUS_EM_PALAVRAS[200]})" in repro
    esperado = _secao(texto, "Resultado esperado e resultado real")
    assert CONTRATO in esperado and "<html><body><h1>Erro</h1>" in esperado
    assert "banco_casos_ineditos_fase4" in _secao(texto, "Referências")
    assert grr.SELO_EM_PALAVRAS["baixo"] in _secao(texto, "Veredito do agente")

    t, tid = _trilha_localizador()
    texto = grr.relatorio_do_caso_v3(t.eventos, tid, leituras=leituras, comando_reexecucao="python executar_fase4.py --modo cenarios")
    _conferir_v3(texto)
    titulo = next(l for l in texto.splitlines() if l.startswith("# "))
    assert "Localizador (seletor) quebrado" in titulo and "front-busca" in titulo and "#buscar" in titulo, titulo
    contexto = _secao(texto, "Contexto")
    assert "front-busca" in contexto and "passo 2" in contexto and f"`id_renomeado` ({grr.MODO_EM_PALAVRAS['id_renomeado']})" in contexto
    repro = _secao(texto, "Descrição para reproduzir")
    assert "index.php" in repro and "#buscar" in repro and "perde o id" in repro and "TimeoutError" in repro
    esperado = _secao(texto, "Resultado esperado e resultado real")
    assert "#buscar" in esperado and "searchbox" in esperado and "5" in esperado
    veredito = _secao(texto, "Veredito do agente")
    assert 'role=searchbox[name="search"]' in veredito and "papel_e_nome" in veredito and "mesmo elemento" in veredito
    assert "79,1 s" in veredito, "o tempo da detecção à reexecução validada"
    assert 'role=searchbox[name="search"]' in _secao(texto, "Linha de ação")


def _pasta_de_corrida_de_teste(nome: str = "_fumaca_q1") -> Path:
    """Uma pasta de corrida como a tela grava: condicoes_fase4.json, a trilha e um relatório v2 do caso."""
    raiz = _temp() / nome
    raiz.mkdir()
    t = trilha.Trilha(versao=trilha.V2)
    t.corrida(_cabecalho(nome, "tela"), ts="2026-11-06T09:53:30")
    tid = _caso_na_tela(t, nome, "lex-1", "alto", 0.9989)
    _caso_na_tela(t, nome, "lex-4", "medio", 0.9)
    t.fechar(fim="2026-11-06T11:12:59")
    t.gravar(raiz / "trilha_tela.jsonl")
    (raiz / "condicoes_fase4.json").write_text(json.dumps({"modo": "tela", "saida": nome, "k": 3, "modelo": "qwen2.5:7b"}), encoding="utf-8")
    (raiz / "relatorios").mkdir()
    (raiz / "relatorios" / "lex-1@tela.md").write_text(grr.relatorio_do_caso_v2(t.eventos, tid), encoding="utf-8", newline="\n")
    return raiz


def teste_v3_da_corrida_grava_um_por_trilha_com_indice_e_confere_com_check():
    raiz = _pasta_de_corrida_de_teste()
    leituras = _leituras_de_teste()
    r = grr.gerar_v3_da_pasta(raiz, leituras=leituras)
    pasta = raiz / "relatorios_v3"
    assert r["pasta"] == pasta and sorted(r["gravados"]) == ["INDICE.md", "lex-1@tela.md", "lex-4@tela.md"], r
    assert (pasta / "lex-1@tela.md").exists() and (pasta / "INDICE.md").exists()
    texto = (pasta / "lex-1@tela.md").read_text(encoding="utf-8")
    _conferir_v3(texto)
    assert "--saida _fumaca_q1_reexec --ids lex-1 --k 3" in texto, "o comando de reexecução de um caso da tela, como o executor grava"
    assert "../relatorios/lex-1@tela.md" in _secao(texto, "Referências"), "o v2 do mesmo caso, quando a corrida o gravou"
    indice = (pasta / "INDICE.md").read_text(encoding="utf-8")
    assert "lex-1@tela.md" in indice and "lex-4@tela.md" in indice and "Resposta truncada" in indice and "—" not in indice and "→" not in indice
    assert grr.gerar_v3_da_pasta(raiz, leituras=leituras, check=True)["diferentes"] == []
    (pasta / "lex-4@tela.md").write_text("alterado à mão", encoding="utf-8")
    assert grr.gerar_v3_da_pasta(raiz, leituras=leituras, check=True)["diferentes"] == ["lex-4@tela.md"]
    assert grr.comando_de_reexecucao("cenarios", "fase4_ensaio_v4", "fase4_ensaio_v4/qwen2.5_7b/contrato-field_missing#1", 3).endswith("--saida fase4_ensaio_v4_reexec --repeticoes 1")
    assert grr.comando_de_reexecucao("ineditos", "fase4_ineditos", "fase4_ineditos/qwen2.5_7b/lex-22", 3).endswith("--saida fase4_ineditos_reexec --ids lex-22")
    assert grr.nome_do_relatorio("fase4_ensaio_v4/qwen2.5_7b/contrato-field_missing#1") == "contrato-field_missing__r1"
    assert grr.nome_do_relatorio("fase4_tela_v4/qwen2.5_7b/lex-1@tela") == "lex-1@tela" and grr.nome_do_relatorio("fase4_ineditos/qwen2.5_7b/lex-22") == "lex-22"


def _corridas_vigentes() -> list[tuple[str, Path, list[dict]]]:
    """(corrida, pasta, eventos) das três leituras vigentes, lidas de resultados_alvo/fase4/*.json (campo metadados.corrida)."""
    saida = []
    for nome in LEITURAS_VIGENTES:
        corrida = json.loads((RA / "fase4" / nome).read_text(encoding="utf-8"))["metadados"]["corrida"]
        pasta = RA / corrida
        modo = json.loads((pasta / "condicoes_fase4.json").read_text(encoding="utf-8"))["modo"]
        saida.append((corrida, pasta, trilha.ler(pasta / f"trilha_{modo}.jsonl")))
    return saida


def teste_v3_regera_as_tres_corridas_vigentes_sem_erro():
    leituras = _leituras_de_teste()
    for corrida, pasta, eventos in _corridas_vigentes():
        esperadas = TRILHAS_ESPERADAS[corrida]
        contagem = {sufixo: 0 for sufixo in esperadas}
        for tid, seq in trilha.por_trilha(eventos).items():
            if not any(e["tipo"] == "decisao" for e in seq):
                continue
            texto = grr.relatorio_do_caso_v3(eventos, tid, leituras=leituras, pasta_blobs=pasta / "blobs")
            _conferir_v3(texto)
            nome = tid.rsplit("/", 1)[-1]
            for sufixo in esperadas:
                if sufixo and sufixo in nome or (not sufixo and "@" not in nome and "#" not in nome):
                    contagem[sufixo] += 1
        assert contagem == esperadas, (corrida, contagem)


def teste_hash_do_prompt_fixo_e_da_biblioteca_inalterados_e_nenhuma_leitura_no_prompt():
    import biblioteca_leitura as bl
    import diagnostico_ao_vivo as dv
    import evolucao_biblioteca as evo
    import recuperacao as rec
    from banco_casos import CASOS
    cabecalhos = [next(e["dados"] for e in eventos if e["tipo"] == "corrida") for _, _, eventos in _corridas_vigentes()]
    hashes_prompt = {c["hash_prompt_fixo"] for c in cabecalhos}
    hashes_bib = {c["hash_biblioteca"] for c in cabecalhos}
    assert len(hashes_prompt) == 1 and len(hashes_bib) == 1, "as três corridas vigentes rodaram com o mesmo prompt fixo e a mesma biblioteca"
    assert evo.hash_biblioteca(bl.PASTA_BIBLIOTECA) == hashes_bib.pop(), "a biblioteca de produção mudou"
    verbetes = bib.carregar(bl.PASTA_BIBLIOTECA)
    assert len(verbetes) == 39 and all(bl.PASTA_BIBLIOTECA in v["caminho"].parents for v in verbetes)
    assert not any(bl.PASTA_LEITURA in v["caminho"].parents for v in verbetes), "a busca carrega só a biblioteca, nunca a camada de leitura"
    indice = rec.Indice(verbetes)
    ctx, prompt = dv.montar_prompt(verbetes, indice, CASOS[0], 3)
    assert dv.hash_prompt_fixo(verbetes, ctx, CASOS[0], prompt) == hashes_prompt.pop(), "o prompt fixo mudou"
    assert bl.MARCA_DA_LEITURA not in prompt and "## O que conferir" not in prompt, "nenhuma leitura entra no prompt"


# ----------------------------------------------------------------------------- Q1: a camada de leitura dos verbetes

def teste_leitura_um_arquivo_por_verbete_com_o_id_e_os_campos_do_frontmatter():
    import biblioteca_leitura as bl
    assert bl.PASTA_LEITURA == AGENTE / "biblioteca_producao_leitura" and bl.PASTA_BIBLIOTECA == AGENTE / "biblioteca_producao"
    pasta = _temp() / "leitura"
    r = bl.gerar(bl.PASTA_BIBLIOTECA, pasta, gerado_em="2026-11-07")
    verbetes = bib.carregar(bl.PASTA_BIBLIOTECA)
    assert len(r["gerados"]) == len(verbetes) == 39 and r["mantidos"] == [] and (pasta / "INDICE.md").exists(), r
    leituras = bl.carregar(pasta)
    assert sorted(leituras) == sorted(v["id"] for v in verbetes), "uma leitura por verbete, pelo id"
    for v in verbetes:
        rel = v["caminho"].relative_to(bl.PASTA_BIBLIOTECA).as_posix()
        arquivo = pasta / rel
        assert arquivo.exists(), f"a leitura de {v['id']} mora no mesmo caminho relativo: {rel}"
        texto = arquivo.read_text(encoding="utf-8")
        meta, corpo = bib._parse_frontmatter(texto)
        for chave, valor in v["meta"].items():
            assert meta.get(chave) == valor, (v["id"], chave, meta.get(chave), valor)
        assert meta["verbete"] == rel and meta["curado"] == "nao" and meta["gerado_em"] == "2026-11-07" and len(meta["hash_do_verbete"]) == 16
        assert meta["hash_do_verbete"] == bl.hash_do_verbete(v["caminho"])
        assert "de IA - Revisar" in texto and "! Motivo:" in texto, "arquivo gerado por IA leva a tag e o motivo"
        assert bl.MARCA_DA_LEITURA in texto and f"`{v['id']}`" in texto
        secoes = bib._parse_secoes(corpo)
        for s in bl.SECOES_DA_LEITURA:
            assert s in secoes, (v["id"], s)
        assert secoes["O que é"].strip() and secoes["Onde está no código"].strip() and secoes["O que conferir"].strip() and secoes["Como aparece na tela"].strip(), v["id"]
        assert "—" not in texto and "→" not in texto, v["id"]
        l = leituras[v["id"]]
        assert l["titulo"] == v["meta"]["titulo"] and l["caminho"] == rel and l["curado"] is False and l.get("causa_raiz") == v["meta"].get("causa_raiz")
    assert bl.conferir(bl.PASTA_BIBLIOTECA, pasta) == []
    antes = {p: p.read_text(encoding="utf-8") for p in pasta.rglob("*.md")}
    bl.gerar(bl.PASTA_BIBLIOTECA, pasta, gerado_em="2026-11-07")
    assert {p: p.read_text(encoding="utf-8") for p in pasta.rglob("*.md")} == antes, "gerar de novo não muda nada"


def teste_leitura_escreve_tipo_status_e_sistema_com_o_significado():
    import biblioteca_leitura as bl
    verbetes = bib.carregar(bl.PASTA_BIBLIOTECA)
    por_id = {v["id"]: v for v in verbetes}
    texto = bl.leitura_do_verbete(por_id["campo_ausente"], verbetes, bl.PASTA_BIBLIOTECA, gerado_em="2026-11-07")
    assert f"erro ({bl.TIPO_EM_PALAVRAS['erro']})" in texto and f"ativo ({bl.STATUS_EM_PALAVRAS['ativo']})" in texto
    assert bl.SISTEMA_EM_PALAVRAS["CobaiaAPI"] in texto
    assert "`campo_renomeado` (Campo renomeado)" in texto, "as causas vizinhas saem com o título do verbete delas"
    assert "Programacao/CobaiaAPI/app/fault_injection.py" in texto and "GET /api/produtos" in texto
    assert "undefined" in texto, "os sinais do verbete"
    assert "texto do modelo" in texto and "sin-1" in texto, "as notas do modelo ficam rotuladas e com o caso de origem"
    assert "Motivo:" in texto and "— Motivo" not in texto
    defeito = bl.leitura_do_verbete(por_id["ancora-saiba-mais"], verbetes, bl.PASTA_BIBLIOTECA, gerado_em="2026-11-07")
    assert f"nao_corrigido ({bl.STATUS_EM_PALAVRAS['nao_corrigido']})" in defeito and f"defeito_conhecido ({bl.TIPO_EM_PALAVRAS['defeito_conhecido']})" in defeito
    sem_sinais = bl.leitura_do_verbete(por_id["mensagens-de-erro-do-codigo"], verbetes, bl.PASTA_BIBLIOTECA, gerado_em="2026-11-07")
    _, corpo = bib._parse_frontmatter(sem_sinais)
    assert bib._parse_secoes(corpo)["Como aparece na tela"].strip(), "sem seção Sinais, os sintomas do cabeçalho preenchem o bloco"


def teste_leitura_curada_a_mao_fica_e_verbete_mudado_e_acusado():
    import biblioteca_leitura as bl
    pasta = _temp() / "leitura"
    bl.gerar(bl.PASTA_BIBLIOTECA, pasta, gerado_em="2026-11-07")
    arquivo = pasta / "erros" / "campo_ausente.md"
    curado = arquivo.read_text(encoding="utf-8").replace("curado: nao", "curado: sim") + "\nTexto escrito à mão pelo analista.\n"
    arquivo.write_text(curado, encoding="utf-8", newline="\n")
    r = bl.gerar(bl.PASTA_BIBLIOTECA, pasta, gerado_em="2026-11-08")
    assert r["mantidos"] == ["campo_ausente"] and "campo_ausente" not in r["gerados"]
    assert arquivo.read_text(encoding="utf-8") == curado, "a leitura curada à mão não é regravada"
    assert bl.carregar(pasta)["campo_ausente"]["curado"] is True
    assert bl.conferir(bl.PASTA_BIBLIOTECA, pasta) == []
    bib_copia = _temp() / "biblioteca"
    shutil.copytree(bl.PASTA_BIBLIOTECA, bib_copia)
    verbete = bib_copia / "erros" / "campo_ausente.md"
    verbete.write_text(verbete.read_text(encoding="utf-8") + "\n- um sinal novo\n", encoding="utf-8", newline="\n")
    falhas = bl.conferir(bib_copia, pasta)
    assert len(falhas) == 1 and "campo_ausente" in falhas[0] and "mudou" in falhas[0], falhas
    outro = pasta / "erros" / "campo_renomeado.md"
    outro.write_text(outro.read_text(encoding="utf-8").replace("titulo: Campo renomeado", "titulo: Outro título"), encoding="utf-8", newline="\n")
    falhas = bl.conferir(bl.PASTA_BIBLIOTECA, pasta)
    assert len(falhas) == 1 and "campo_renomeado" in falhas[0] and "titulo" in falhas[0], falhas
    (pasta / "erros" / "campo_renomeado.md").unlink()
    falhas = bl.conferir(bl.PASTA_BIBLIOTECA, pasta)
    assert any("campo_renomeado" in f and "sem leitura" in f for f in falhas), falhas
    (pasta / "erros" / "inventado.md").write_text("---\nid: inventado\ntitulo: X\ncurado: nao\n---\n## O que é\nx\n", encoding="utf-8")
    assert any("inventado" in f and "sem verbete" in f for f in bl.conferir(bl.PASTA_BIBLIOTECA, pasta))


def teste_leitura_real_existe_e_bate_com_a_biblioteca():
    import biblioteca_leitura as bl
    assert bl.PASTA_LEITURA.is_dir(), "a camada de leitura ainda não foi gerada em biblioteca_producao_leitura/"
    assert bl.conferir(bl.PASTA_BIBLIOTECA, bl.PASTA_LEITURA) == []
    leituras = bl.carregar(bl.PASTA_LEITURA)
    assert len(leituras) == 39 and (bl.PASTA_LEITURA / "INDICE.md").exists()
    indice = (bl.PASTA_LEITURA / "INDICE.md").read_text(encoding="utf-8")
    assert "de IA - Revisar" in indice and "! Motivo" in indice and all(i in indice for i in leituras)


def teste_relatorios_v3_das_corridas_vigentes_gravados_e_conferidos():
    """A fumaça sem modelo: os relatórios v3 das três corridas vigentes estão gravados na pasta de cada corrida e batem com a regeração."""
    import biblioteca_leitura as bl
    leituras = bl.carregar(bl.PASTA_LEITURA)
    for corrida, pasta, _ in _corridas_vigentes():
        assert (pasta / "relatorios_v3" / "INDICE.md").exists(), f"{corrida}: relatórios v3 ainda não gravados"
        r = grr.gerar_v3_da_pasta(pasta, leituras=leituras, check=True)
        assert r["diferentes"] == [], (corrida, r["diferentes"][:5])
        assert len(r["gravados"]) == sum(TRILHAS_ESPERADAS[corrida].values()) + 1, (corrida, len(r["gravados"]))


# ----------------------------------------------------------------------------- Q2: os filtros determinísticos de prolixidade e objetividade

# Separação silábica conferida à mão, pela divisão silábica padrão do português do Brasil (cada palavra cobre uma regra do separador:
# ditongo decrescente, ditongo nasal, hiato entre vogais fortes, hiato com i/u acentuado, i/u + vogal no fim da palavra sem acento em outra
# sílaba, "ia/io/ie/ua/uo" finais átonos com acento em outra sílaba, u mudo depois de q e g, vogal fraca seguida de consoante final).
AMOSTRA_DE_SILABAS = {
    "a": 1, "é": 1, "não": 1, "mãe": 1, "põe": 1, "sei": 1, "pai": 1, "mais": 1, "seu": 1, "quem": 1, "que": 1, "quais": 1,
    "dia": 2, "lua": 2, "rua": 2, "tela": 2, "ação": 2, "água": 2, "série": 2, "voo": 2, "país": 2, "baú": 2, "ruim": 2, "raiz": 2, "sair": 2,
    "qualquer": 2, "igual": 2, "quase": 2, "jeito": 2, "noite": 2, "trilha": 2, "ponta": 2, "média": 2, "ações": 2, "guia": 2, "caos": 2,
    "leem": 2, "prêmio": 2, "muito": 2, "tempo": 2, "campo": 2, "guerra": 2, "pinguim": 2,
    "ciência": 3, "ideia": 3, "família": 3, "história": 3, "atual": 3, "área": 3, "saída": 3, "saúde": 3, "viagem": 3, "piano": 3,
    "sequência": 3, "linguagem": 3, "Europa": 3, "saudade": 3, "cuidado": 3, "verbete": 3, "contrato": 3, "motivo": 3, "coelho": 3,
    "frequência": 3, "código": 3, "resposta": 3, "produtos": 3, "ausente": 3, "janela": 3, "exceção": 3, "aquele": 3, "quieto": 3, "tranquilo": 3,
    "referência": 4, "coordenar": 4, "quantidade": 4, "usuário": 4, "poesia": 4, "aéreo": 4, "relatório": 4, "analista": 4, "necessário": 4,
    "evidência": 4, "interface": 4,
    "diagnóstico": 5, "localizador": 5, "probabilidade": 6,
}
# Os três textos de controle do plano (seção 7, Q2): um que segue a regra de escrita dos comentários deste repositório, um prolixo (frases
# compridas, enchimento, a mesma frase repetida) e um com jargão e sigla sem expansão; o quarto mostra a sigla expandida na primeira menção.
TEXTO_BOM = ("A poda do corpo levava o primeiro item normal da lista quando não havia diferença de campo contra o contrato. "
             "Agora o diff é calculado contra a referência em modo normal, e o sintoma diz o que mudou. "
             "O status 200 (a API respondeu sem código de erro) continua passando pela conferência do roteiro.")
TEXTO_PROLIXO = ("Vale ressaltar que, neste momento, a poda do corpo da resposta, que é basicamente a etapa responsável por reduzir o tamanho do "
                 "conteúdo que chega ao modelo, acabava levando, de fato, o primeiro item normal da lista sempre que não havia nenhuma diferença de "
                 "campo contra o contrato esperado pela interface, o que, na verdade, fazia com que o sintoma descrito não dissesse realmente o que "
                 "tinha mudado contra a referência. "
                 "Vale ressaltar que, neste momento, a poda do corpo da resposta acabava levando o primeiro item normal da lista. "
                 "Vale ressaltar que, neste momento, a poda do corpo da resposta acabava levando o primeiro item normal da lista.")
TEXTO_JARGAO = ("O snapshot do estado sofreu uma race condition no guard-rail da poda. "
                "O logprob do rótulo caiu e o hit@3 da busca também; o MTTR subiu.")
TEXTO_JARGAO_EXPANDIDO = "O MTTR (o tempo entre perceber a falha e ter o resultado) subiu de 72 s para 101 s."
LIMIARES_DO_TESTE = {"palavras_por_frase_media": 20, "palavras_por_frase_max": 30, "preenchimento_razao": 0.02, "repeticao_razao": 0.05, "compressao": 1.5}


def teste_filtros_separa_silabas_na_amostra_conferida():
    import filtros_de_texto as ft
    erros = [(p, ft.silabas(p), n) for p, n in AMOSTRA_DE_SILABAS.items() if ft.silabas(p) != n]
    assert erros == [], f"{len(erros)} de {len(AMOSTRA_DE_SILABAS)} palavras fora da contagem conferida: {erros}"
    assert ft.silabas("2026") == 1 and ft.silabas("x") == 1 and ft.silabas("segunda-feira") == 5


def teste_filtros_conta_frases_e_palavras_e_calcula_o_flesch_adaptado():
    import filtros_de_texto as ft
    assert ft.frases("O caso efe-3 (ex. da classe 6) passou. Veja a p. 50 do syllabus. Fim") == ["O caso efe-3 (ex. da classe 6) passou.", "Veja a p. 50 do syllabus.", "Fim"]
    assert ft.frases("Primeira linha sem ponto\nSegunda linha. Terceira frase!") == ["Primeira linha sem ponto", "Segunda linha.", "Terceira frase!"]
    assert ft.palavras("O status 200 (a API respondeu) continua, e não para.") == ["O", "status", "200", "a", "API", "respondeu", "continua", "e", "não", "para"]
    bom = ft.medir(TEXTO_BOM)
    assert bom["frases"] == 3 and bom["palavras"] == 54 and bom["palavras_por_frase_max"] == 20 and bom["palavras_por_frase_media"] == 18.0
    assert bom["comprimentos_das_frases"] == [20, 18, 16]
    curto = ft.medir("A tela abre. O campo some.")
    assert curto["palavras"] == 6 and curto["silabas"] == 10
    assert abs(curto["flesch"] - (248.835 - 1.015 * 3 - 84.6 * (10 / 6))) < 0.01, "a fórmula do NILC-Metrix: 248,835 - 1,015 x palavras por frase - 84,6 x sílabas por palavra"
    assert ft.FLESCH_ALARME == 50.0 and ft.FORMULA_FLESCH == (248.835, 1.015, 84.6)
    assert ft.percentil([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 95) == 9.55 and ft.percentil([5], 95) == 5 and ft.percentil([3, 1, 2], 50) == 2


def teste_filtros_texto_bom_passa_e_prolixo_e_com_jargao_reprovam():
    import filtros_de_texto as ft
    lim = ft.limiares_fixos(LIMIARES_DO_TESTE, origem="valores fixados pelo teste")
    assert {m["chave"] for m in ft.METRICAS} == {"palavras_por_frase_media", "palavras_por_frase_max", "flesch", "preenchimento_razao", "repeticao_razao",
                                                  "compressao", "termos_sem_expansao_n", "densidade_dominio"} and len(ft.METRICAS) == 8
    assert all(m["fonte"] for m in ft.METRICAS), "toda métrica declara a fonte"
    bom = ft.medir(TEXTO_BOM)
    av = ft.avaliar(bom, lim)
    assert av["aprovado"] is True, av
    assert bom["termos_sem_expansao"] == [] and bom["preenchimentos"] == {} and bom["repeticao_razao"] == 0.0 and bom["compressao"] < 1.5
    assert isinstance(av["alarme_flesch"], bool), "o Flesch é alarme, não critério de aprovação"
    prolixo = ft.medir(TEXTO_PROLIXO)
    avp = ft.avaliar(prolixo, lim)
    assert avp["aprovado"] is False
    for c in ("palavras_por_frase_media", "palavras_por_frase_max", "preenchimento_razao", "repeticao_razao", "compressao"):
        assert avp["criterios"][c]["passa"] is False, (c, avp["criterios"][c])
    assert avp["criterios"]["termos_sem_expansao_n"]["passa"] is True
    assert prolixo["preenchimentos"]["vale ressaltar"] == 3 and prolixo["preenchimentos"]["neste momento"] == 3 and prolixo["preenchimentos"]["basicamente"] == 1
    assert prolixo["preenchimento_razao"] > 0.1 and prolixo["repeticao_razao"] > 0.2 and prolixo["compressao"] > bom["compressao"]
    assert prolixo["palavras_por_frase_max"] > 60 and prolixo["palavras_por_frase_media"] > 30
    jargao = ft.medir(TEXTO_JARGAO)
    assert jargao["termos_sem_expansao"] == ["guard-rail", "hit@3", "logprob", "mttr", "race condition", "snapshot"], jargao["termos_sem_expansao"]
    avj = ft.avaliar(jargao, lim)
    assert avj["aprovado"] is False and avj["criterios"]["termos_sem_expansao_n"]["passa"] is False and avj["criterios"]["termos_sem_expansao_n"]["valor"] == 6
    expandido = ft.medir(TEXTO_JARGAO_EXPANDIDO)
    assert expandido["termos_sem_expansao"] == [] and ft.avaliar(expandido, lim)["aprovado"] is True, "a sigla com o significado na mesma frase não conta"
    curto = ft.medir("A tela abre. O campo some.")
    assert ft.avaliar(curto, lim)["alarme_flesch"] is False
    dominio = ft.medir("Confira o campo `imagem` em `GET /api/produtos` e compare com o contrato esperado pela interface.")
    assert dominio["trechos_em_codigo"] == 2 and dominio["termos_do_dominio"] == 5 and dominio["palavras"] == 14 and abs(dominio["densidade_dominio"] - 5 / 14) < 1e-3
    assert set(bom) >= {m["chave"] for m in ft.METRICAS} | {"palavras", "frases", "silabas", "trechos_em_codigo", "termos_sem_expansao", "preenchimentos", "termos_do_dominio"}
    for chave in ("flesch", "densidade_dominio"):
        assert av["criterios"][chave]["passa"] is None, "alarme e comparação não aprovam nem reprovam"


def teste_filtros_extrai_a_prosa_do_markdown():
    import filtros_de_texto as ft
    md = ("<!-- ! Alteração de IA - Revisar: relatório derivado.\n     ! Motivo: comentário que o analista não lê como texto do relatório. -->\n"
          "# Título do relatório\n\nPrimeira frase do corpo. Segunda frase, com `codigo_x` dentro.\n\n| Onde | Esperado |\n|---|---|\n| corpo | JSON válido |\n\n"
          "```text\nbloco de código\n```\n\n<details><summary>31 eventos da trilha, na ordem.</summary>\n\n| seq | Tipo |\n|---|---|\n| 1 | acao |\n\n</details>\n\n"
          "> Sintoma citado do caso, que o molde não escreveu.\n\n- item um da lista\n- **item dois** com [um link](x.md).\n")
    p = ft.prosa_de_markdown(md)
    prosa = p["prosa"]
    for fora in ("Título", "Esperado", "bloco de código", "Motivo", "<details>", "codigo_x", "x.md", "**", "Sintoma citado"):
        assert fora not in prosa, fora
    for dentro in ("Primeira frase do corpo.", "31 eventos da trilha, na ordem.", "item um da lista", "item dois com um link."):
        assert dentro in prosa, dentro
    assert p["trechos_em_codigo"] == 1
    m = ft.medir(md)
    assert m["frases"] == 5 and m["trechos_em_codigo"] == 1, (m["frases"], ft.frases(prosa))
    assert ft.medir("")["palavras"] == 0 and ft.medir("")["frases"] == 0 and ft.medir("")["flesch"] is None


def teste_filtros_corpus_le_os_motivos_do_repositorio_e_o_exemplo_sem_copiar_texto():
    import filtros_de_texto as ft
    raiz = _temp() / "repo"
    (raiz / "ferramentas").mkdir(parents=True)
    (raiz / "ferramentas" / "a.py").write_text("# ! Alteração de IA - Revisar: troca a busca.\n# ! Motivo: a busca levava o primeiro item da lista quando não havia\n"
                                                "# diferença de campo contra o contrato.\nx = 1\n", encoding="utf-8")
    (raiz / "doc.md").write_text("<!-- ! Alteração de IA - Revisar: seção nova.\n     ! Motivo: o roadmap mandava esperar pela especificação,\n     que chegou nesta data. -->\n# Título\n",
                                 encoding="utf-8")
    (raiz / "p.php").write_text("<?php\n// ! Alteração de IA - Revisar: filtro novo.\n// ! Motivo: o estorno reabria itens de pedidos já cancelados.\n", encoding="utf-8")
    (raiz / "r.cmd").write_text("rem ! Alteracao de IA - Revisar: sem acento.\nrem ! Motivo: o cmd.exe le o arquivo na codepage OEM e os bytes UTF-8 re-tokenizam a linha.\n",
                                encoding="utf-8")
    (raiz / "s.sql").write_text("-- ! Motivo: a coluna real da tabela chama id_produto, e nao produto_id.\nSELECT 1;\n", encoding="utf-8")
    (raiz / "z_dup.py").write_text("# ! Motivo: a busca levava o primeiro item da lista quando não havia\n# diferença de campo contra o contrato.\n", encoding="utf-8")
    (raiz / "curto.py").write_text("# ! Motivo: idem.\n", encoding="utf-8")
    (raiz / "regra.md").write_text("# Regra\n\nA tag leva a marca \"! Motivo:\" na linha seguinte, e os textos \"! Motivo:\" do repositório formam o corpus.\n", encoding="utf-8")
    (raiz / "um.py").write_text("# ! Alteração de IA - Revisar: troca o limite. ! Motivo: a mesma linha traz a tag e o motivo inteiro, e os dois valem.\n", encoding="utf-8")
    derivados = raiz / "Programacao" / "AgenteCore" / "experimentos" / "resultados_alvo"
    derivados.mkdir(parents=True)
    (derivados / "x.md").write_text("<!-- ! Motivo: relatório derivado, gerado por script, que não entra no corpus de referência. -->\n", encoding="utf-8")
    arquivos = sorted(p.relative_to(raiz).as_posix() for p in raiz.rglob("*") if p.is_file())
    itens = ft.corpus_do_repositorio(raiz, arquivos=arquivos)
    textos = [i["texto"] for i in itens]
    assert len(itens) == 6, [i["origem"] for i in itens]
    assert "a busca levava o primeiro item da lista quando não havia diferença de campo contra o contrato." in textos, textos
    assert "o roadmap mandava esperar pela especificação, que chegou nesta data." in textos, textos
    assert "o cmd.exe le o arquivo na codepage OEM e os bytes UTF-8 re-tokenizam a linha." in textos
    assert "a mesma linha traz a tag e o motivo inteiro, e os dois valem." in textos, "a tag e o motivo na mesma linha valem"
    assert not any("na linha seguinte" in t or "formam o corpus" in t for t in textos), "a menção da marca no meio de uma frase não é comentário"
    assert all("Motivo" not in t and "-->" not in t and "Altera" not in t for t in textos)
    assert {i["origem"].rsplit(":", 1)[0] for i in itens} == {"ferramentas/a.py", "doc.md", "p.php", "r.cmd", "s.sql", "um.py"}
    assert all(i["fonte"] == "motivo" and int(i["origem"].rsplit(":", 1)[1]) >= 1 for i in itens)
    assert not ft.arquivo_no_corpus("Programacao/AgenteCore/experimentos/resultados_alvo/fase4/texto.md")
    assert not ft.arquivo_no_corpus("Programacao/AgenteCore/biblioteca_producao/erros/campo_ausente.md")
    assert not ft.arquivo_no_corpus("Programacao/AgenteCore/biblioteca_producao_leitura/erros/campo_ausente.md")
    assert not ft.arquivo_no_corpus("Programacao/AgenteCore/aprendidos_em_espera/x.md")
    assert not ft.arquivo_no_corpus("Documentacao/dashboard/painel-do-projeto.html") and not ft.arquivo_no_corpus("Cobaia.exe")
    assert ft.arquivo_no_corpus("ferramentas/painel_topicos.py") and ft.arquivo_no_corpus("Documentacao/memorial/roadmap.md") and ft.arquivo_no_corpus(".claude/CLAUDE.md")
    memoria = _temp() / "feedback-resumo-tecnico-aba-ocorrencia.md"
    memoria.write_text("---\nname: x\n---\nTexto da memória.\n\n**Exemplo canônico (escrito pelo Eric, caso OC 0, teste):**\n\n```\n[arquivo.apl] \n\n-> dlg_x\n\n"
                       "  -> Fun_A (Alteração)\n    -> Marca os itens do pedido originador como pendentes antes de gerar o pedido eletrônico e confere as linhas "
                       "atualizadas contra a busca. \nMotivo: a situação pendente só era gravada no fim, sem conferência, e duas efetivações próximas geravam pedido sem item.\n"
                       "\n\n  -> Fun_B (Função Nova)\n```\n\n- Vocabulário: nada.\n", encoding="utf-8")
    exemplo = ft.exemplo_canonico(memoria)
    assert len(exemplo) == 2 and all(len(x.split()) >= 5 for x in exemplo), exemplo
    assert not any("->" in x or "[arquivo.apl]" in x or x.startswith("Motivo:") for x in exemplo), exemplo
    cal = ft.calibrar(itens + [{"origem": f"exemplo canônico, linha {n}", "fonte": "exemplo_canonico", "texto": t} for n, t in enumerate(exemplo, start=1)])
    assert cal["metadados"]["corpus"] == {"itens": 8, "por_fonte": {"exemplo_canonico": 2, "motivo": 6}, "frases": cal["metadados"]["corpus"]["frases"]}
    assert cal["metadados"]["corpus"]["frases"] >= 8
    dump = json.dumps(cal, ensure_ascii=False)
    assert "pedido originador" not in dump and "re-tokenizam" not in dump, "nenhum texto do corpus é copiado para a calibração"
    for item in cal["itens"]:
        assert "texto" not in item and set(item) >= {"origem", "fonte", "sha16", "palavras", "frases", "palavras_por_frase_media", "flesch"}, item
    medias = [i["palavras_por_frase_media"] for i in cal["itens"]]
    assert cal["limiares"]["palavras_por_frase_media"]["valor"] == round(ft.percentil(medias, 95), 2)
    assert cal["limiares"]["palavras_por_frase_media"]["tipo"] == "calibracao" and cal["limiares"]["palavras_por_frase_media"]["provisorio_do_plano"] == 20
    pooladas = [c for i in itens + [{"texto": t} for t in exemplo] for c in ft.medir(i["texto"])["comprimentos_das_frases"]]
    assert cal["limiares"]["palavras_por_frase_max"]["valor"] == round(ft.percentil(pooladas, 95), 2) and cal["limiares"]["palavras_por_frase_max"]["provisorio_do_plano"] == 30
    assert cal["limiares"]["flesch"] == {**cal["limiares"]["flesch"], "valor": 50.0, "tipo": "fonte"} and "corpus" in cal["limiares"]["flesch"]
    assert cal["limiares"]["termos_sem_expansao_n"]["valor"] == 0 and cal["limiares"]["termos_sem_expansao_n"]["tipo"] == "fonte"
    assert cal["limiares"]["densidade_dominio"]["valor"] is None and cal["limiares"]["palavras"]["tipo"] == "covariavel"
    for chave in ("preenchimento_razao", "repeticao_razao", "compressao"):
        assert cal["limiares"][chave]["tipo"] == "calibracao" and cal["limiares"][chave]["valor"] is not None, chave
    aprovados = sum(1 for i in itens if ft.avaliar(ft.medir(i["texto"]), cal)["aprovado"])
    assert aprovados >= 5, "os limiares calibrados no corpus aceitam o próprio corpus (percentil 95)"
    arq = _temp() / "limiares_texto.json"
    ft.gravar_limiares(arq, cal)
    assert ft.carregar_limiares(arq)["limiares"] == cal["limiares"]


def _pasta_de_leitura_de_teste() -> Path:
    import biblioteca_leitura as bl
    pasta = _temp() / "leitura"
    bl.gerar(bl.PASTA_BIBLIOTECA, pasta, gerado_em="2026-11-07")
    return pasta


def teste_texto_le_antes_e_depois_de_uma_corrida_e_da_camada_e_grava_com_check():
    import biblioteca_leitura as bl
    import filtros_de_texto as ft
    import pre_fase4 as pf
    raiz = _pasta_de_corrida_de_teste("_fumaca_q2")
    pasta_leitura = _pasta_de_leitura_de_teste()
    grr.gerar_v3_da_pasta(raiz, leituras=bl.carregar(pasta_leitura))
    lim = ft.limiares_fixos(LIMIARES_DO_TESTE, origem="valores fixados pelo teste")
    bruto = ft.ler_textos(corridas=[("_fumaca_q2", raiz)], raiz_bib=bl.PASTA_BIBLIOTECA, raiz_leitura=pasta_leitura)
    assert [c["id"] for c in bruto["corridas"]] == ["_fumaca_q2"] and bruto["corridas"][0]["modo"] == "tela"
    rel = {r["nome"]: r for r in bruto["corridas"][0]["relatorios"]}
    assert set(rel) == {"lex-1@tela", "lex-4@tela"}
    assert rel["lex-1@tela"]["v2_origem"] == "gravado" and rel["lex-4@tela"]["v2_origem"] == "regerado", "sem v2 gravado, o v2 é regerado da trilha"
    assert rel["lex-1@tela"]["v2"].startswith("<!--") and "## 1. Identificador" in rel["lex-1@tela"]["v3"]
    assert len(bruto["verbetes"]) == 39 and all(v["verbete"] and v["leitura"] for v in bruto["verbetes"])
    assert [m["caso"] for m in bruto["modelo"]] == ["lex-1@tela", "lex-4@tela"] and all("14 cartões" in m["texto"] for m in bruto["modelo"])
    dado = ft.resumir_texto(bruto, lim, gerado_em="2026-11-08T10:00:00")
    grupos = {g["id"]: g for g in dado["grupos"]}
    assert list(grupos) == ["_fumaca_q2", "camada_de_leitura"]
    g = grupos["_fumaca_q2"]
    assert g["tipo"] == "relatorios" and g["antes"]["n"] == 2 and g["depois"]["n"] == 2 and g["v2_origem"] == {"gravados": 1, "regerados": 1}
    for versao in ("antes", "depois"):
        ag = g[versao]
        assert set(ag) >= {"n", "aprovados", "aprovados_pct", "alarme_flesch", "medias", "criterios", "termos_sem_expansao", "preenchimentos"}
        assert set(ag["medias"]) >= {m["chave"] for m in ft.METRICAS} | {"palavras"} and set(ag["criterios"]) == {m["chave"] for m in ft.METRICAS if m["regra"] in ("ate", "zero")}
    par = {p["nome"]: p for p in g["pares"]}["lex-1@tela"]
    assert set(par["antes"]) >= {m["chave"] for m in ft.METRICAS} | {"aprovado", "alarme_flesch", "palavras", "termos_sem_expansao"}
    cam = grupos["camada_de_leitura"]
    assert cam["tipo"] == "verbetes" and cam["antes"]["n"] == 39 and cam["depois"]["n"] == 39 and {p["id"] for p in cam["pares"]} == {v["id"] for v in bruto["verbetes"]}
    assert dado["modelo"]["n"] == 2 and dado["modelo"]["medias"]["palavras"] > 0
    assert [m["chave"] for m in dado["metricas"]] == [m["chave"] for m in ft.METRICAS] and all(m["fonte"] and m["regra"] for m in dado["metricas"])
    assert dado["resumo"]["relatorios"]["depois"]["n"] == 2 and dado["resumo"]["verbetes"]["antes"]["n"] == 39
    assert dado["metadados"]["gerado_por"] == "avaliar_fase4.py --texto" and dado["limiares"]["origem"] == "valores fixados pelo teste"
    pasta = _temp() / "derivados"
    md = ft.render_texto(dado)
    assert "<!-- tabela:tb_f4_texto_resumo -->" in md and "<!-- tabela:tb_f4_texto_metricas -->" in md and "—" not in md and "→" not in md
    assert pf.fechar(ft.NOME, dado, md, ft.PREFIXO, pasta=pasta, doc=pasta / "sem_relatorio.md") == 0
    assert (pasta / "texto.json").exists() and (pasta / "texto.md").exists()
    outro_dia = ft.resumir_texto(bruto, lim, gerado_em="2026-11-09T10:00:00")
    assert pf.fechar(ft.NOME, outro_dia, ft.render_texto(outro_dia), ft.PREFIXO, check=True, pasta=pasta, doc=pasta / "sem_relatorio.md") == 0
    outro_dia["resumo"]["relatorios"]["depois"]["n"] = 99
    assert pf.fechar(ft.NOME, outro_dia, ft.render_texto(outro_dia), ft.PREFIXO, check=True, pasta=pasta, doc=pasta / "sem_relatorio.md") == 1


def teste_texto_json_gravado_bate_com_a_regeracao_e_o_molde_v3_passa_nos_filtros():
    """A fumaça sem modelo: a calibração e a leitura antes e depois estão gravadas em resultados_alvo/fase4, batem com a regeração, e todo
    relatório v3 das três corridas vigentes passa nos critérios (o plano manda ajustar o molde até passar)."""
    import filtros_de_texto as ft
    import pre_fase4 as pf
    arq_lim, arq = RA / "fase4" / "limiares_texto.json", RA / "fase4" / "texto.json"
    assert arq_lim.exists(), "calibre com: python filtros_de_texto.py --calibrar"
    assert arq.exists(), "grave com: RESULTADOS_DIR=resultados_alvo python avaliar_fase4.py --texto"
    lim = ft.carregar_limiares(arq_lim)
    assert lim["metadados"]["corpus"]["por_fonte"]["motivo"] >= 500 and lim["metadados"]["corpus"]["por_fonte"]["exemplo_canonico"] >= 5
    assert all("texto" not in i for i in lim["itens"]) and "TargetERP" not in json.dumps(lim["itens"], ensure_ascii=False)
    dado = json.loads(arq.read_text(encoding="utf-8"))
    assert pf.sem_data(dado["limiares"]) == pf.sem_data({k: v for k, v in lim.items() if k != "itens"}) or dado["limiares"]["gerado_em"] == lim["metadados"]["gerado_em"]
    corridas = {c: p for c, p, _ in _corridas_vigentes()}
    grupos = {g["id"]: g for g in dado["grupos"]}
    assert set(grupos) == set(corridas) | {"camada_de_leitura"}
    for corrida in corridas:
        g = grupos[corrida]
        assert g["antes"]["n"] == g["depois"]["n"] == sum(TRILHAS_ESPERADAS[corrida].values()), (corrida, g["antes"]["n"], g["depois"]["n"])
        reprovados = [p["nome"] for p in g["pares"] if not p["depois"]["aprovado"]]
        assert reprovados == [], (corrida, reprovados[:5], [p["depois"] for p in g["pares"] if not p["depois"]["aprovado"]][:1])
        assert g["depois"]["termos_sem_expansao"] == {}, (corrida, g["depois"]["termos_sem_expansao"])
    cam = grupos["camada_de_leitura"]
    assert cam["antes"]["n"] == cam["depois"]["n"] == 39 and cam["depois"]["aprovados"] >= cam["antes"]["aprovados"]
    regerado = ft.resumir_texto(ft.ler_textos(), lim, gerado_em=dado["metadados"]["gerado_em"])
    assert pf.sem_data(regerado) == pf.sem_data(dado), "texto.json não bate com a regeração: rode avaliar_fase4.py --texto"


# ----------------------------------------------------------------------------- Q3: a árvore de decisão

LIMIARES_DO_SELO = {"baixo_ate": 0.8317943867608124, "alto_a_partir_de": 0.9898271080008889}   # os mesmos cortes de resultados_alvo/fase4/limiares.json
TID_DIVERGENCIA_TELA = "fase4_tela_v4/qwen2.5_7b/lex-10@tela"            # a resposta veio sem a linha FONTE (falha formato_das_quatro_linhas)
TID_DIVERGENCIA_TEXTO = "fase4_ineditos/qwen2.5_7b/lex-24"               # nenhum verbete entregue trata da causa respondida
TID_CURA = "fase4_ensaio_v4/qwen2.5_7b/localizador-front-busca#1"        # cura aplicada por papel_e_nome, segundo candidato não tentado


def _calibracao_de_teste() -> dict:
    """A leitura da corrida de calibração como `avaliar_fase4.py --calibracao` a grava (só os campos que a árvore lê): os cortes do selo e o acerto por faixa."""
    return {"metadados": {"gerado_em": "2026-11-05T10:56:38", "corrida": "fase4_calibracao"}, "k_escolhido": 3,
            "limiares": {**LIMIARES_DO_SELO, "n": 90, "k": 3, "origem": "fase4_calibracao/k3"},
            "por_selo": [{"selo": "baixo", "casos": 27, "certos": 12, "errados": 15, "erro_pct": 55.6},
                         {"selo": "medio", "casos": 26, "certos": 22, "errados": 4, "erro_pct": 15.4},
                         {"selo": "alto", "casos": 37, "certos": 34, "errados": 3, "erro_pct": 8.1}]}


def _limiares_de_teste() -> dict:
    return {**LIMIARES_DO_SELO, "n": 90, "k": 3, "origem": "fase4_calibracao/k3", "medida": "p_rotulo"}


def _afirmacoes(arvore: dict, chave: str) -> list[dict]:
    return next(d for d in arvore["decisoes"] if d["chave"] == chave)["afirmacoes"]


def _textos(afirmacoes: list[dict], origem: str | None = None) -> list[str]:
    return [a["texto"] for a in afirmacoes if origem is None or a["origem"] == origem]


def _tem(textos: list[str], *trechos: str) -> bool:
    return any(all(t in x for t in trechos) for x in textos)


def _conferir_arvore(arvore: dict) -> None:
    """O que toda árvore tem de ter: decisões numeradas na ordem, toda afirmação com um dos quatro rótulos, nenhum percentual numa afirmação
    desconhecida, o bloco do texto do modelo rotulado e o resumo com a contagem por rótulo igual à soma das afirmações."""
    import arvore_de_decisao as ad
    assert [d["numero"] for d in arvore["decisoes"]] == list(range(1, len(arvore["decisoes"]) + 1))
    assert [d["chave"] for d in arvore["decisoes"]][:3] == ["leitura", "verbetes", "causa"]
    contagem = {r: 0 for r in ad.ROTULOS}
    for d in arvore["decisoes"]:
        assert d["afirmacoes"], f"decisão {d['chave']} sem afirmação"
        assert d["titulo"] and "escolha" in d
        for a in d["afirmacoes"]:
            assert a["origem"] in ad.ROTULOS, (d["chave"], a)
            assert a["texto"].strip(), (d["chave"], a)
            if a["origem"] == "desconhecido":
                assert "%" not in a["texto"], ("desconhecido com percentual", a)
            contagem[a["origem"]] += 1
    assert arvore["resumo"]["rotulos"] == contagem
    assert arvore["texto_do_modelo"]["rotulo"] == ad.TEXTO_DO_MODELO
    assert set(arvore["rotulos"]) == set(ad.ROTULOS)


def _conferir_markdown_da_arvore(md: str) -> None:
    import arvore_de_decisao as ad
    assert md.startswith("<!-- ! Alteração de IA - Revisar") and "! Motivo" in md
    assert "## Decisão 1: " in md and "## Decisão 2: " in md and "## Decisão 3: " in md and "## Texto do modelo" in md and "## Rastro" in md
    for r in ad.ROTULOS:
        assert f"{r} (" in md, f"a legenda dos rótulos não explica {r}"
    prosa = _sem_codigo(md)
    assert "—" not in prosa and "→" not in prosa, "travessão ou seta no texto corrido da árvore"
    for termo in JARGAO_PROIBIDO + ("p_rotulo", "k = 3", "num_ctx"):
        assert termo not in prosa, f"jargão da trilha na árvore: {termo}"


def teste_arvore_rotulos_de_origem_e_afirmacao_desconhecida_sem_percentual():
    import arvore_de_decisao as ad
    assert ad.ROTULOS == ("observado", "conferido", "declarado", "desconhecido")
    assert set(ad.SIGNIFICADO_DO_ROTULO) == set(ad.ROTULOS) and all(ad.SIGNIFICADO_DO_ROTULO[r] for r in ad.ROTULOS)
    assert ad.TEXTO_DO_MODELO == "texto do modelo"
    a = ad.afirmacao("A poda levou 54 nós a 21 linhas.", "observado", eventos=[19])
    assert a == {"texto": "A poda levou 54 nós a 21 linhas.", "origem": "observado", "eventos": [19]}
    for ruim in ("medido", "", None):
        try:
            ad.afirmacao("x", ruim)
        except ValueError:
            pass
        else:
            raise AssertionError(f"rótulo {ruim!r} aceito")
    try:
        ad.afirmacao("acertou 91,9% dos casos", "desconhecido")
    except ValueError:
        pass
    else:
        raise AssertionError("uma afirmação desconhecida com percentual foi aceita")
    assert ad.afirmacao("a taxa desta faixa é desconhecida", "desconhecido")["origem"] == "desconhecido"


def teste_arvore_confianca_em_palavras_com_a_taxa_da_faixa_e_desconhecida_sem_calibracao():
    import arvore_de_decisao as ad
    cal, lim = _calibracao_de_teste(), _limiares_de_teste()
    conf = {"p_rotulo": 0.9989376663617734, "selo": "alto", "limiares": LIMIARES_DO_SELO}
    c = ad.confianca_em_palavras(conf, cal, lim)
    assert c["palavra"] == "alta" and c["selo"] == "alto" and c["historico"] == {"casos": 37, "certos": 34, "acerto_pct": 91.9}
    textos = [a["texto"] for a in c["afirmacoes"]]
    assert _tem(textos, "alta", "0,999") and _tem(textos, "34 de 37", "91,9%"), textos
    assert all(a["origem"] == "observado" for a in c["afirmacoes"]), c["afirmacoes"]
    assert not any(re.search(r"\blogprob|\bhit@|\bk\s*=", t) for t in textos), textos
    medio = ad.confianca_em_palavras({"p_rotulo": 0.9088, "selo": "medio", "limiares": LIMIARES_DO_SELO}, cal, lim)
    assert medio["palavra"] == "média" and medio["historico"]["certos"] == 22 and _tem([a["texto"] for a in medio["afirmacoes"]], "22 de 26")
    baixo = ad.confianca_em_palavras({"p_rotulo": 0.71, "selo": "baixo", "limiares": LIMIARES_DO_SELO}, cal, lim)
    assert baixo["palavra"] == "baixa" and _tem([a["texto"] for a in baixo["afirmacoes"]], "12 de 27")
    # sem a leitura da calibração a faixa fica sem taxa, e a afirmação é desconhecida, sem percentual
    sem = ad.confianca_em_palavras(conf, None, lim)
    assert sem["palavra"] == "alta" and sem["historico"] is None
    desconhecidas = [a for a in sem["afirmacoes"] if a["origem"] == "desconhecido"]
    assert desconhecidas and all("%" not in a["texto"] for a in desconhecidas), sem["afirmacoes"]
    # cortes do nó diferentes dos da calibração: a taxa da calibração não vale para esta faixa
    outra = ad.confianca_em_palavras({"p_rotulo": 0.9989, "selo": "alto", "limiares": {"baixo_ate": 0.5, "alto_a_partir_de": 0.95}}, cal, lim)
    assert outra["historico"] is None and any(a["origem"] == "desconhecido" for a in outra["afirmacoes"])
    # sem probabilidade lida não há selo nem palavra
    nada = ad.confianca_em_palavras({"p_rotulo": None, "selo": None}, cal, lim)
    assert nada["palavra"] is None and nada["afirmacoes"] and all(a["origem"] == "desconhecido" and "%" not in a["texto"] for a in nada["afirmacoes"])


def teste_arvore_de_um_caso_da_tela_tem_as_tres_decisoes_com_rotulo_em_toda_afirmacao():
    import arvore_de_decisao as ad
    t, tid = _trilha_tela()
    arv = ad.arvore_do_caso(t.eventos, tid, leituras=_leituras_de_teste(), calibracao=_calibracao_de_teste(), limiares=_limiares_de_teste())
    _conferir_arvore(arv)
    assert arv["trilha"] == tid and arv["caso"] == "lex-1" and arv["corrida"] == "_fumaca_q1" and arv["eventos"]["hash"] == grr.hash_da_trilha(t.eventos, tid)
    assert [d["chave"] for d in arv["decisoes"]] == ["leitura", "verbetes", "causa"], "sem cura, a árvore tem três decisões"
    # decisão 1: o que a poda tirou e manteve, e por qual regra em código
    d1 = _textos(_afirmacoes(arv, "leitura"), "observado")
    assert _tem(d1, "54 nós", "21 linhas") and _tem(d1, "2 imagens"), d1
    assert _tem(d1, "47 caracteres", "50 caracteres") and _tem(d1, "contrato"), d1
    assert not _textos(_afirmacoes(arv, "leitura"), "declarado"), "a poda é toda em código: nada declarado pelo modelo"
    # decisão 2: os três entregues, os de fora com a pontuação, e o sinal que decidiu
    d2 = next(d for d in arv["decisoes"] if d["chave"] == "verbetes")
    assert d2["entregues"] == ["resposta_truncada", "contagem_inconsistente", "entidade-produto"]
    fora = [a for a in d2["alternativas"] if not a["escolhida"]]
    assert [a["opcao"] for a in fora] == ["limites-do-sistema"] and "19,7" in fora[0]["detalhe"], d2["alternativas"]
    assert _tem(_textos(d2["afirmacoes"], "observado"), "limites-do-sistema", "19,7"), d2["afirmacoes"]
    assert _tem(_textos(d2["afirmacoes"], "desconhecido"), "sinais"), "a trilha de teste não guarda os sinais da consulta: a árvore diz que não sabe"
    # decisão 3: a causa escolhida contra a segunda, a confiança em palavras, a evidência e a divergência
    d3 = next(d for d in arv["decisoes"] if d["chave"] == "causa")
    assert d3["escolha"] == "resposta_truncada" and d3["segunda"] == "corpo_nao_e_json" and d3["campo"] is None
    assert d3["confianca"]["palavra"] == "alta" and d3["confianca"]["historico"]["certos"] == 34
    textos3 = _textos(d3["afirmacoes"])
    assert _tem(_textos(d3["afirmacoes"], "declarado"), "resposta_truncada") and _tem(_textos(d3["afirmacoes"], "declarado"), "não apontou campo"), textos3
    assert _tem(_textos(d3["afirmacoes"], "observado"), "corpo_nao_e_json", "0,001"), textos3
    assert _tem(_textos(d3["afirmacoes"], "observado"), "34 de 37", "91,9%"), textos3
    assert _tem(_textos(d3["afirmacoes"], "observado"), "JSON completo e válido", "corpo truncado"), "o trecho medido em código é a evidência"
    assert _tem(_textos(d3["afirmacoes"], "observado"), "Resposta truncada", "biblioteca_producao_leitura/"), "o verbete é citado pela camada de leitura"
    assert _tem(_textos(d3["afirmacoes"], "conferido"), "estava entre os entregues") or _tem(_textos(d3["afirmacoes"], "conferido"), "contexto"), textos3
    assert d3["divergencia"] is None and _tem(_textos(d3["afirmacoes"], "conferido"), "Nenhuma divergência"), textos3
    assert not any(re.search(r"\blogprob|\bhit@|\bk\s*=", t) for t in textos3), textos3
    # o texto do modelo fica à parte, rotulado
    tm = arv["texto_do_modelo"]
    assert tm["rotulo"] == "texto do modelo" and tm["impacto"].startswith("A interface exibiu uma tela vazia") and "CAUSA_RAIZ: resposta_truncada" in tm["resposta"]
    assert arv["resumo"] == {**arv["resumo"], "divergencia": False, "cura": False, "selo": "alto", "confianca": "alta", "decisoes": 3}
    md = ad.render_markdown(arv)
    _conferir_markdown_da_arvore(md)
    assert "## Decisão 4" not in md and "(observado)" in md and "(declarado)" in md and "(conferido)" in md and "(desconhecido)" in md


def _arvore_real(tid: str) -> dict:
    import arvore_de_decisao as ad
    import biblioteca_leitura as bl
    corrida = tid.split("/")[0]
    pasta, eventos = next((p, ev) for c, p, ev in _corridas_vigentes() if c == corrida)
    return ad.arvore_do_caso(eventos, tid, pasta_blobs=pasta / "blobs", leituras=bl.carregar(bl.PASTA_LEITURA), calibracao=ad.carregar_calibracao(), limiares=ad.carregar_limiares())


def teste_arvore_de_um_caso_real_com_divergencia_conferida_campo_a_campo():
    import arvore_de_decisao as ad
    # lex-10 na tela: a resposta veio sem a linha FONTE
    arv = _arvore_real(TID_DIVERGENCIA_TELA)
    _conferir_arvore(arv)
    d3 = next(d for d in arv["decisoes"] if d["chave"] == "causa")
    assert d3["escolha"] == "resposta_truncada" and d3["segunda"] == "corpo_nao_e_json" and d3["confianca"]["palavra"] == "alta"
    assert d3["divergencia"] == {"ha": True, "entre": ["modelo", "verificacao"], "detalhe": "faltam na resposta as linhas FONTE"}
    assert d3["falha"] == "formato_das_quatro_linhas"
    conferidas = _textos(d3["afirmacoes"], "conferido")
    assert _tem(conferidas, "diverge", "faltam na resposta as linhas FONTE"), conferidas
    assert _tem(conferidas, "formato_das_quatro_linhas", "programa"), "a falha sai com o significado e a origem da taxonomia"
    assert _tem(_textos(d3["afirmacoes"], "declarado"), "FONTE", "não veio") or _tem(_textos(d3["afirmacoes"], "declarado"), "FONTE", "não escreveu"), d3["afirmacoes"]
    assert arv["texto_do_modelo"]["fonte"] is None and arv["resumo"]["divergencia"] is True and arv["resumo"]["cura"] is False
    d1 = _textos(_afirmacoes(arv, "leitura"), "observado")
    assert _tem(d1, "54 nós", "21 linhas") and _tem(d1, "8 ") and _tem(d1, "47 caracteres", "50 caracteres"), d1
    d2 = next(d for d in arv["decisoes"] if d["chave"] == "verbetes")
    assert d2["entregues"] == ["resposta_truncada", "contagem_inconsistente", "entidade-produto"]
    assert _tem(_textos(d2["afirmacoes"], "observado"), "GET /api/produtos") and _tem(_textos(d2["afirmacoes"], "observado"), "Produto"), "os sinais da consulta (rota, entidade, status)"
    assert not _textos(d2["afirmacoes"], "desconhecido"), "na trilha real os sinais estão gravados"
    assert _tem(_textos(d2["afirmacoes"], "observado"), "limites-do-sistema"), "o primeiro verbete que ficou de fora"
    # lex-24 em texto: nenhum verbete entregue trata da causa respondida, e o modelo apontou o campo `resumo`
    arv2 = _arvore_real(TID_DIVERGENCIA_TEXTO)
    _conferir_arvore(arv2)
    d3 = next(d for d in arv2["decisoes"] if d["chave"] == "causa")
    assert d3["escolha"] == "codificacao_incorreta" and d3["segunda"] == "formato_de_data_divergente" and d3["campo"] == "resumo"
    assert d3["divergencia"]["detalhe"] == "nenhum verbete entregue trata da causa respondida codificacao_incorreta" and d3["falha"] == "causa_sem_verbete_que_a_trate"
    assert _tem(_textos(d3["afirmacoes"], "declarado"), "`resumo`") and _tem(_textos(d3["afirmacoes"], "conferido"), "resumo", "aparece no caso"), d3["afirmacoes"]
    assert _tem(_textos(d3["afirmacoes"], "conferido"), "entidade-produto") and _tem(_textos(d3["afirmacoes"], "conferido"), "contrato-produto"), "os dois verbetes citados na FONTE, conferidos"
    assert _tem(_textos(d3["afirmacoes"], "observado"), "FONTE divergente") or _tem(_textos(d3["afirmacoes"], "observado"), "gatilho"), "o gatilho de revisão disparou"
    d1 = _afirmacoes(arv2, "leitura")
    assert _tem(_textos(d1, "observado"), "em texto") and next(d for d in arv2["decisoes"] if d["chave"] == "leitura")["alternativas"] == []
    assert arv2["resumo"]["divergencia"] is True and len(arv2["decisoes"]) == 3
    assert ad.FALHA_EM_PALAVRAS["causa_sem_verbete_que_a_trate"] and set(ad.FALHA_EM_PALAVRAS) == {f for tipos in trilha.TAXONOMIA_DE_FALHAS.values() for f in tipos}


def teste_arvore_de_um_caso_real_com_cura_conferida_campo_a_campo():
    arv = _arvore_real(TID_CURA)
    _conferir_arvore(arv)
    assert [d["chave"] for d in arv["decisoes"]] == ["leitura", "verbetes", "causa", "cura"]
    d3 = next(d for d in arv["decisoes"] if d["chave"] == "causa")
    assert d3["escolha"] == "localizador_quebrado" and d3["confianca"]["palavra"] == "média" and _tem(_textos(d3["afirmacoes"]), "22 de 26")
    d4 = next(d for d in arv["decisoes"] if d["chave"] == "cura")
    assert d4["escolha"] == "papel_e_nome" and d4["seletor"] == 'role=searchbox[name="search"]' and d4["curado"] is True and d4["mesmo_elemento"] is True
    por_opcao = {a["opcao"]: a for a in d4["alternativas"]}
    assert set(por_opcao) == {"papel_e_nome", "papel_e_nome_parecido", "texto_contido", "data_id", "caminho_do_ancestral_com_id", "posicao_entre_irmaos"}
    assert por_opcao["papel_e_nome"]["escolhida"] and not por_opcao["caminho_do_ancestral_com_id"]["escolhida"]
    assert "não foi tentado" in por_opcao["caminho_do_ancestral_com_id"]["detalhe"] or "ordem fixa" in por_opcao["caminho_do_ancestral_com_id"]["detalhe"]
    assert "não gerado" in por_opcao["texto_contido"]["detalhe"] and "texto visível" in por_opcao["texto_contido"]["detalhe"]
    assert "não gerado" in por_opcao["data_id"]["detalhe"] and "data-id" in por_opcao["data_id"]["detalhe"]
    textos = _textos(d4["afirmacoes"])
    assert _tem(textos, "73,3 s") and _tem(textos, "mesmo elemento") and _tem(textos, "passo 2", "falhou"), textos
    assert _tem(textos, "5 verificações") or _tem(textos, "cinco verificações"), textos
    assert _tem(textos, "validada") or _tem(textos, "chegou ao fim"), "a reexecução validada entra na decisão da cura"
    assert d4["divergencia"]["ha"] is True and "ordem fixa" in d4["divergencia"]["detalhe"] and _tem(textos, "ordem fixa"), d4["divergencia"]
    assert {a["origem"] for a in d4["afirmacoes"]} <= {"observado"}, "a cura roda sem modelo: nada declarado nem conferido contra o modelo"
    assert arv["resumo"]["cura"] is True and arv["resumo"]["divergencia"] is True and arv["resumo"]["decisoes"] == 4
    d1 = _textos(_afirmacoes(arv, "leitura"), "observado")
    assert _tem(d1, "250 nós", "37 linhas") and _tem(d1, "16 cartões") and _tem(d1, "21 imagens"), d1


def teste_arvore_gera_as_83_trilhas_vigentes_e_cada_no_vira_decisao_com_rotulo():
    import arvore_de_decisao as ad
    import biblioteca_leitura as bl
    import filtros_de_texto as ft
    leituras, cal, lim = bl.carregar(bl.PASTA_LEITURA), ad.carregar_calibracao(), ad.carregar_limiares()
    limiares_texto = ft.carregar_limiares()
    por_no = {"diagnostico": "causa", "cura": "cura", "reexecucao": "cura"}
    geradas, reprovadas, com_divergencia, com_cura = 0, [], 0, 0
    for corrida, pasta, eventos in _corridas_vigentes():
        contagem = {sufixo: 0 for sufixo in TRILHAS_ESPERADAS[corrida]}
        for tid, seq in trilha.por_trilha(eventos).items():
            nos = [e["dados"]["decisao"] for e in seq if e["tipo"] == "decisao"]
            if not nos:
                continue
            arv = ad.arvore_do_caso(eventos, tid, pasta_blobs=pasta / "blobs", leituras=leituras, calibracao=cal, limiares=lim)
            _conferir_arvore(arv)
            chaves = {d["chave"] for d in arv["decisoes"]}
            assert {por_no[n] for n in nos} <= chaves, (tid, nos, chaves)
            assert ("cura" in chaves) == any(e["tipo"] == "cura" for e in seq), tid
            assert arv["resumo"]["decisoes"] == len(arv["decisoes"]) and arv["resumo"]["afirmacoes"] == sum(arv["resumo"]["rotulos"].values())
            md = ad.render_markdown(arv)
            _conferir_markdown_da_arvore(md)
            medida = ft.avaliar(ft.medir(md), limiares_texto)
            if not medida["aprovado"]:
                reprovadas.append((tid, medida["termos_sem_expansao"], {k: v for k, v in medida["criterios"].items() if v["passa"] is False}))
            geradas += 1
            com_divergencia += arv["resumo"]["divergencia"]
            com_cura += arv["resumo"]["cura"]
            nome = tid.rsplit("/", 1)[-1]
            for sufixo in TRILHAS_ESPERADAS[corrida]:
                if sufixo and sufixo in nome or (not sufixo and "@" not in nome and "#" not in nome):
                    contagem[sufixo] += 1
        assert contagem == TRILHAS_ESPERADAS[corrida], (corrida, contagem)
    assert geradas == 120 and com_divergencia >= 1 and com_cura == 4, (geradas, com_divergencia, com_cura)
    assert reprovadas == [], f"{len(reprovadas)} árvores reprovam nos filtros do Q2: {reprovadas[:3]}"


def teste_arvores_da_pasta_gravam_md_json_e_indice_sem_tocar_no_resto_e_conferem_com_check():
    import arvore_de_decisao as ad
    import filtros_de_texto as ft
    raiz = _pasta_de_corrida_de_teste("_fumaca_q3")
    antes = {p: p.read_bytes() for p in raiz.rglob("*") if p.is_file()}
    r = ad.gerar_da_pasta(raiz, leituras=_leituras_de_teste(), calibracao=_calibracao_de_teste(), limiares=_limiares_de_teste(), limiares_texto=ft.carregar_limiares())
    pasta = raiz / "arvores"
    assert r["pasta"] == pasta and sorted(r["gravados"]) == ["INDICE.json", "INDICE.md", "lex-1@tela.json", "lex-1@tela.md", "lex-4@tela.json", "lex-4@tela.md"], r
    assert {p: p.read_bytes() for p in raiz.rglob("*") if p.is_file() and pasta not in p.parents} == antes, "nada fora de arvores/ pode mudar"
    arv = json.loads((pasta / "lex-1@tela.json").read_text(encoding="utf-8"))
    _conferir_arvore(arv)
    md = (pasta / "lex-1@tela.md").read_text(encoding="utf-8")
    _conferir_markdown_da_arvore(md)
    assert md == ad.render_markdown(arv)
    indice = json.loads((pasta / "INDICE.json").read_text(encoding="utf-8"))
    assert indice["corrida"] == "_fumaca_q3" and indice["modo"] == "tela" and indice["hash_prompt_fixo"] == "2e42cf9c31826941" and indice["hash_biblioteca"] == "95af35290860"
    assert indice["resumo"]["trilhas"] == 2 and indice["resumo"]["nos_por_decisao"] == {"diagnostico": 2} and indice["resumo"]["com_cura"] == 0
    assert indice["resumo"]["filtros"]["n"] == 2 and 0 <= indice["resumo"]["filtros"]["aprovados"] <= 2
    assert set(indice["resumo"]["rotulos"]) == set(ad.ROTULOS) and indice["resumo"]["decisoes_por_chave"] == {"leitura": 2, "verbetes": 2, "causa": 2}
    assert [a["nome"] for a in indice["arvores"]] == ["lex-1@tela", "lex-4@tela"] and indice["arvores"][0]["confianca"] == "alta" and indice["arvores"][1]["confianca"] == "média"
    texto_indice = (pasta / "INDICE.md").read_text(encoding="utf-8")
    assert "lex-1@tela.md" in texto_indice and "lex-4@tela.md" in texto_indice and "—" not in texto_indice and "→" not in texto_indice
    assert ad.gerar_da_pasta(raiz, leituras=_leituras_de_teste(), calibracao=_calibracao_de_teste(), limiares=_limiares_de_teste(), limiares_texto=ft.carregar_limiares(), check=True)["diferentes"] == []
    (pasta / "lex-4@tela.md").write_text("alterado à mão", encoding="utf-8")
    assert ad.gerar_da_pasta(raiz, leituras=_leituras_de_teste(), calibracao=_calibracao_de_teste(), limiares=_limiares_de_teste(), limiares_texto=ft.carregar_limiares(), check=True)["diferentes"] == ["lex-4@tela.md"]
    assert ad.main(["--pasta", str(raiz), "--check", "--calibracao", "nenhuma"]) == 1
    assert ad.main(["--pasta", str(raiz), "--calibracao", "nenhuma"]) == 0
    sem_cal = json.loads((pasta / "lex-1@tela.json").read_text(encoding="utf-8"))
    assert next(d for d in sem_cal["decisoes"] if d["chave"] == "causa")["confianca"]["historico"] is None, "sem calibração, a faixa fica sem taxa"
    assert ad.main(["--pasta", str(raiz), "--check", "--calibracao", "nenhuma"]) == 0


def teste_arvores_das_corridas_vigentes_gravadas_e_conferidas():
    """A fumaça sem modelo: as árvores das três corridas vigentes estão gravadas em arvores/ e batem com a regeração; todas passam nos filtros do Q2."""
    import arvore_de_decisao as ad
    import biblioteca_leitura as bl
    import filtros_de_texto as ft
    leituras, cal, lim, lt = bl.carregar(bl.PASTA_LEITURA), ad.carregar_calibracao(), ad.carregar_limiares(), ft.carregar_limiares()
    total = 0
    for corrida, pasta, _ in _corridas_vigentes():
        assert (pasta / "arvores" / "INDICE.json").exists(), f"{corrida}: árvores ainda não gravadas"
        r = ad.gerar_da_pasta(pasta, leituras=leituras, calibracao=cal, limiares=lim, limiares_texto=lt, check=True)
        assert r["diferentes"] == [], (corrida, r["diferentes"][:5])
        esperadas = sum(TRILHAS_ESPERADAS[corrida].values())
        assert len(r["gravados"]) == 2 * esperadas + 2, (corrida, len(r["gravados"]))
        indice = json.loads((pasta / "arvores" / "INDICE.json").read_text(encoding="utf-8"))
        assert indice["resumo"]["trilhas"] == esperadas and indice["resumo"]["filtros"] == {"n": esperadas, "aprovados": esperadas}, indice["resumo"]
        assert indice["hash_prompt_fixo"] == "2e42cf9c31826941" and indice["hash_biblioteca"] == "95af35290860"
        total += esperadas
    assert total == 120


# ------------------------------------------------------------------ Q4: a barra de progresso e o protótipo do Git

TAXAS_DE_TESTE = {"metadados": {"gerado_em": "2026-11-08T10:00:00", "corridas": ["_teste"], "hash_prompt_fixo": "2e42cf9c31826941", "hash_biblioteca": "95af35290860"},
                  "por_modelo": {"modelo-de-teste": {
                      "n": 3, "maquinas": ["maquina-de-teste"], "versoes_ollama": ["0.40.14"], "teto_tokens": [600],
                      "prefill_tokens_por_s": {"mediana": 25.0, "p10": 20.0, "p90": 30.0, "min": 19.0, "max": 31.0, "n": 3, "origem": "teste"},
                      "geracao_tokens_por_s": {"mediana": 5.0, "p10": 4.8, "p90": 5.2, "min": 4.7, "max": 5.3, "n": 3, "origem": "teste"},
                      "tokens_saida": {"mediana": 60, "p10": 50, "p90": 80, "min": 45, "max": 88, "n": 3, "origem": "teste"},
                      "tokens_entrada": {"mediana": 1000, "p10": 900, "p90": 1200, "min": 850, "max": 1400, "n": 3, "origem": "teste"},
                      "chars_por_token": {"mediana": 3.5, "p10": 3.4, "p90": 3.6, "min": 3.3, "max": 3.7, "n": 3, "origem": "teste"},
                      "carga_ms": {"mediana": 30, "p10": 28, "p90": 9000, "min": 25, "max": 9064, "n": 3, "origem": "teste"}}}}
RESPOSTA_OLLAMA_DE_TESTE = {"response": "CAUSA_RAIZ: campo_ausente\nCAMPO: preco\nIMPACTO: x\nFONTE: [campo_ausente]", "done_reason": "stop",
                            "prompt_eval_count": 1000, "prompt_eval_cached_count": 55, "eval_count": 7, "load_duration": 30_000_000,
                            "prompt_eval_duration": 40_000_000_000, "eval_duration": 1_400_000_000, "total_duration": 41_430_000_000, "context": [1, 2, 3]}
CAMPOS_DO_ESTADO = {"etapa", "modelo", "estado", "fase", "tokens_prompt", "chars_prompt", "teto_tokens", "tokens_gerados", "decorrido_s", "estimativa_s",
                    "estimativa_refeita_s", "fracao", "estimativa", "medido", "inferencias_concluidas", "iniciado_em", "gravado_em", "versao"}
COMMITS_DA_APLICACAO = ["e854a0eb", "ab4da6a1", "26432d2c", "084fce09", "603c423e", "3e8cfc14", "4f3b3e26", "633ebb27"]   # git log -- Programacao/CobaiaAPI Programacao/CobaiaFront


class _Relogio:
    """Um relógio de teste: o tempo só anda quando o teste manda."""
    def __init__(self, inicio: float = 1000.0) -> None:
        self.t = inicio

    def __call__(self) -> float:
        return self.t


class _Tela(io.StringIO):
    """Um fluxo que se apresenta como terminal, para a barra redesenhar a linha."""
    def isatty(self) -> bool:
        return True


def _barra_de(linha: str) -> str:
    """O trecho entre colchetes da linha da barra (a forma do indicador)."""
    m = re.search(r"\[[^\]]*\]", linha)
    assert m, linha
    return m.group(0)


def _taxas_de_teste() -> dict:
    return json.loads(json.dumps(TAXAS_DE_TESTE))


def _post_de_mentira(chamadas: list, demora_s: float = 0.0, resposta: dict | None = None, com_logprobs: bool = True):
    """Um `_post` no lugar do Ollama: guarda o corpo enviado, espera `demora_s` e devolve a resposta no formato do Ollama."""
    def post(caminho: str, corpo: dict, timeout: int = 900) -> dict:
        chamadas.append(json.loads(json.dumps(corpo)))
        if demora_s:
            time.sleep(demora_s)
        r = dict(resposta or RESPOSTA_OLLAMA_DE_TESTE)
        if com_logprobs and corpo.get("logprobs"):
            r["logprobs"] = [{"token": t, "logprob": -0.1, "bytes": list(t.encode("utf-8")), "top_logprobs": [{"token": t, "logprob": -0.1}]}
                             for t in ("CAUSA_RAIZ", ":", " campo_ausente", "\n", "CAMPO: preco\nIMPACTO: x\nFONTE: [campo_ausente]")]
        return r
    return post


@contextlib.contextmanager
def _ollama_trocado(post):
    import cliente_ollama as oll
    original = oll._post
    oll._post = post
    try:
        yield
    finally:
        oll._post = original


def teste_progresso_estima_as_duas_fases_com_taxas_conhecidas():
    import progresso as pg
    taxas = pg.taxas_do_modelo(_taxas_de_teste(), "modelo-de-teste")
    est = pg.estimar(chars_prompt=3500, teto=600, taxas=taxas)
    assert est["tokens_prompt"] == 1000, est                       # 3500 chars / 3,5 chars por token
    assert est["prefill_s"] == 40.0, est                           # 1000 tokens / 25 tokens por segundo
    assert est["geracao_s"] == 12.0, est                           # mediana de 60 tokens gerados / 5 tokens por segundo
    assert est["geracao_maxima_s"] == 120.0, est                   # o teto de 600 tokens / 5 tokens por segundo
    assert est["total_s"] == 52.0 and est["maximo_s"] == 160.0, est
    for fase in ("tokens_prompt", "prefill_s", "geracao_s", "geracao_maxima_s"):
        assert "mediana" in est["origem"][fase] or "teto" in est["origem"][fase], est["origem"]
    assert pg.estimar(chars_prompt=3500, teto=600, taxas=None) is None, "sem taxas do modelo nesta máquina não há estimativa"
    assert pg.taxas_do_modelo(_taxas_de_teste(), "outro-modelo") is None


def teste_progresso_fracao_nunca_recua_nao_para_no_fim_e_a_fase_segue_o_relogio():
    import progresso as pg
    estimativa = 52.0
    tempos = (0, 10, 26, 52, 60, 104, 300, 3000)
    valores = [pg.fracao(t, estimativa) for t in tempos]
    assert valores[0] == 0.0
    assert all(b >= a for a, b in itertools.pairwise(valores)), valores
    assert abs(pg.fracao(26, estimativa) - 0.45) < 1e-9 and abs(pg.fracao(52, estimativa) - 0.9) < 1e-9, "90% quando o decorrido iguala a estimativa"
    assert 0.9 < pg.fracao(60, estimativa) < pg.fracao(104, estimativa) < pg.fracao(300, estimativa) < 1.0, "segue avançando devagar depois da estimativa"
    assert all(v < 1.0 for v in valores), "só a conclusão leva a 100%"
    assert pg.estimativa_refeita(104, estimativa) > estimativa and pg.estimativa_refeita(26, estimativa) == estimativa
    assert pg.fracao(10, None) is None, "sem estimativa a barra é indeterminada"
    est = {"prefill_s": 40.0, "geracao_s": 12.0}
    assert pg.fase_pelo_relogio(10, est) == "prefill" and pg.fase_pelo_relogio(45, est) == "geracao" and pg.fase_pelo_relogio(10, None) == "prefill"


def teste_progresso_indeterminada_vira_determinada_sem_trocar_de_forma_e_conclui_em_cem_por_cento():
    import progresso as pg
    rel = _Relogio()
    p = pg.Progresso(saida=_Tela(), arquivo_estado=None, taxas=None, modelo="modelo-de-teste", relogio=rel, terminal=True)
    p.iniciar("lex-1 · diagnóstico", chars_prompt=3500, teto=600)
    assert p.estado()["estado"] == "indeterminado" and p.estado()["estimativa_s"] is None
    l1 = p.linha()
    rel.t += 3
    l2 = p.linha()
    assert "lendo o caso" in l1 and "lex-1 · diagnóstico" in l1 and "sem estimativa" in l1, l1
    assert _barra_de(l1) != _barra_de(l2), "a barra indeterminada se mexe"
    assert len(_barra_de(l1)) == len(_barra_de(l2)) == pg.LARGURA + 2
    q = pg.Progresso(saida=_Tela(), arquivo_estado=None, taxas=_taxas_de_teste(), modelo="modelo-de-teste", relogio=rel, terminal=True)
    q.iniciar("lex-1 · diagnóstico", chars_prompt=3500, teto=600)
    e = q.estado()
    assert e["estado"] == "determinado" and e["estimativa_s"] == 52.0 and e["fase"] == "prefill" and e["tokens_prompt"] == 1000 and e["fracao"] == 0.0, e
    assert len(_barra_de(q.linha())) == pg.LARGURA + 2, "a forma não muda entre indeterminada e determinada"
    rel.t += 26
    assert "45%" in q.linha() and q.estado()["fracao"] == 0.45 and q.estado()["fase"] == "prefill", q.linha()
    rel.t += 20
    assert q.estado()["fase"] == "geracao" and "resposta" in q.linha(), q.linha()
    rel.t += 60
    e = q.estado()
    assert 0.9 < e["fracao"] < 1.0 and e["estimativa_refeita_s"] > 52.0 and "estimativa refeita" in q.linha(), (e, q.linha())
    fracoes = []
    for _ in range(5):
        rel.t += 7
        fracoes.append(q.estado()["fracao"])
    assert all(b > a for a, b in itertools.pairwise(fracoes)) and fracoes[-1] < 1.0, fracoes
    medida = q.concluir({**RESPOSTA_OLLAMA_DE_TESTE, "prompt_eval_duration": 42_000_000_000, "eval_duration": 11_000_000_000, "eval_count": 55})
    e = q.estado()
    assert e["estado"] == "concluido" and e["fracao"] == 1.0 and e["tokens_gerados"] == 55 and e["fase"] == "geracao", e
    assert e["medido"]["prefill_s"] == 42.0 and e["medido"]["geracao_s"] == 11.0 and e["medido"]["tokens_entrada"] == 1000, e["medido"]
    assert medida["estimado"]["prefill_s"] == 40.0 and medida["erro"]["prefill_s"] == -2.0 and medida["erro"]["geracao_s"] == 1.0, medida
    assert "100%" in q.linha() and q.saida.getvalue().endswith("\n")


def teste_progresso_estado_gravado_em_json_e_lido_de_volta():
    import progresso as pg
    rel = _Relogio()
    arquivo = _temp() / "corrida" / "progresso.json"
    p = pg.Progresso(saida=None, arquivo_estado=arquivo, taxas=_taxas_de_teste(), modelo="modelo-de-teste", relogio=rel, terminal=False)
    p.iniciar("lex-1 · diagnóstico", chars_prompt=3500, teto=600)
    assert arquivo.exists(), "o estado é gravado no início, antes da primeira resposta"
    rel.t += 10
    p.redesenhar()
    lido = pg.ler_estado(arquivo)
    assert lido == p.estado()
    assert CAMPOS_DO_ESTADO <= set(lido), sorted(CAMPOS_DO_ESTADO - set(lido))
    assert lido["decorrido_s"] == 10.0 and lido["estado"] == "determinado" and lido["modelo"] == "modelo-de-teste" and lido["versao"] == 1
    assert re.match(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}", lido["gravado_em"]) and lido["medido"] is None and lido["tokens_gerados"] is None
    p.concluir(RESPOSTA_OLLAMA_DE_TESTE)
    assert pg.ler_estado(arquivo)["estado"] == "concluido" and pg.ler_estado(arquivo)["inferencias_concluidas"] == 1


def teste_progresso_cancelamento_grava_o_estado_e_encerra_limpo():
    import cliente_ollama as oll
    import progresso as pg
    arquivo = _temp() / "progresso.json"
    tela = _Tela()

    def interromper(fio, segundos: float) -> None:
        raise KeyboardInterrupt

    with _ollama_trocado(_post_de_mentira([], demora_s=1.5)), \
            pg.observando(arquivo_estado=arquivo, modelo="modelo-de-teste", taxas=_taxas_de_teste(), saida=tela, terminal=True, esperar=interromper):
        try:
            oll._post("/api/generate", {"model": "modelo-de-teste", "prompt": "x" * 3500, "options": {"num_predict": 600}})
            raise AssertionError("o Ctrl+C devia encerrar a inferência")
        except SystemExit as e:
            assert "cancelad" in str(e).lower() and "progresso.json" in str(e), str(e)
    estado = pg.ler_estado(arquivo)
    assert estado["estado"] == "cancelado" and estado["tokens_gerados"] is None, estado
    assert "cancelad" in tela.getvalue().lower() and tela.getvalue().endswith("\n")


def teste_progresso_com_ollama_de_mentira_barra_no_terminal_marcos_sem_terminal_e_registro_igual():
    import cliente_ollama as oll
    import progresso as pg
    import sondar_logprobs as sl
    chamadas: list = []
    pasta = _temp()
    prompt = "x" * 3500
    with _ollama_trocado(_post_de_mentira(chamadas, demora_s=1.2)):
        sem_barra = oll.gerar("modelo-de-teste", prompt, 600)
        tela = _Tela()
        with pg.observando(arquivo_estado=pasta / "progresso.json", modelo="modelo-de-teste", taxas=_taxas_de_teste(), saida=tela, medidas=pasta / "progresso_medidas.jsonl"):
            pg.anunciar("lex-1 · diagnóstico")
            capturas: list = []
            with sl.com_logprobs(20, capturas):
                com_barra = oll.gerar("modelo-de-teste", prompt, 600)
            oll._post("/api/generate", {"model": "modelo-de-teste", "prompt": "", "keep_alive": 0})   # a descarga do modelo passa sem barra
        for chave, valor in sem_barra.items():
            if chave != "segundos":
                assert com_barra[chave] == valor, (chave, valor, com_barra[chave])
        assert abs(sem_barra["segundos"] - com_barra["segundos"]) < 0.3, (sem_barra["segundos"], com_barra["segundos"])
        assert {k: v for k, v in chamadas[1].items() if k not in ("logprobs", "top_logprobs")} == chamadas[0], "o corpo enviado ao Ollama não muda"
        assert capturas and capturas[0]["resposta"]["eval_count"] == 7, "a captura das probabilidades continua funcionando por dentro da barra"
        texto = tela.getvalue()
        assert texto.count("\r") >= 2 and "lex-1 · diagnóstico" in texto and "100%" in texto and texto.endswith("\n"), texto[-300:]
        assert texto.count("\n") == 1, "no terminal a inferência ocupa uma linha só, redesenhada; a descarga não imprime nada"
        estado = pg.ler_estado(pasta / "progresso.json")
        assert estado["estado"] == "concluido" and estado["tokens_gerados"] == 7 and estado["inferencias_concluidas"] == 1 and estado["etapa"] == "lex-1 · diagnóstico", estado
        medidas = [json.loads(l) for l in (pasta / "progresso_medidas.jsonl").read_text(encoding="utf-8").splitlines()]
        assert len(medidas) == 1 and medidas[0]["estimado"]["prefill_s"] == 40.0 and medidas[0]["medido"]["prefill_s"] == 40.0 and medidas[0]["medido"]["geracao_s"] == 1.4, medidas
        assert medidas[0]["etapa"] == "lex-1 · diagnóstico" and medidas[0]["erro"]["prefill_s"] == 0.0
        log = io.StringIO()
        with pg.observando(arquivo_estado=pasta / "p2.json", modelo="modelo-de-teste", taxas=_taxas_de_teste(), saida=log, terminal=False):
            oll.gerar("modelo-de-teste", prompt, 600)
        linhas = log.getvalue().splitlines()
        assert len(linhas) == 2 and "\r" not in log.getvalue(), linhas
        assert "inferência 1" in linhas[0] and "1000 tokens" in linhas[0] and "52" in linhas[0], linhas[0]
        assert "concluíd" in linhas[1] and "prefill" in linhas[1], linhas[1]
        log2 = io.StringIO()
        with pg.observando(arquivo_estado=pasta / "p3.json", modelo="modelo-de-teste", taxas=None, saida=log2, terminal=False):
            oll.gerar("modelo-de-teste", prompt, 600)
        assert "sem estimativa" in log2.getvalue().splitlines()[0] and pg.ler_estado(pasta / "p3.json")["estado"] == "concluido"


def teste_progresso_anunciado_pelo_diagnostico_ao_vivo_sem_mudar_a_chamada():
    import diagnostico_ao_vivo as dv
    import progresso as pg
    chamadas: list = []
    pasta = _temp()
    with _ollama_trocado(_post_de_mentira(chamadas)):
        r0, _ = dv.inferir("modelo-de-teste", "y" * 3500, 600, "lex-1", 20)
        with pg.observando(arquivo_estado=pasta / "progresso.json", modelo="modelo-de-teste", taxas=_taxas_de_teste(), saida=io.StringIO(), terminal=False):
            r1, captura = dv.inferir("modelo-de-teste", "y" * 3500, 600, "lex-1", 20)
    assert {k: v for k, v in r0.items() if k != "segundos"} == {k: v for k, v in r1.items() if k != "segundos"}
    assert chamadas[0] == chamadas[1], "a chamada do agente é a mesma com e sem a barra"
    assert captura["resposta"]["eval_count"] == 7
    estado = pg.ler_estado(pasta / "progresso.json")
    assert estado["etapa"] == "lex-1 · diagnóstico" and estado["estado"] == "concluido", estado


def teste_progresso_taxas_extraidas_das_corridas_vigentes_com_origem_e_check():
    import progresso as pg
    taxas = pg.extrair_taxas()
    assert taxas["metadados"]["corridas"] == ["fase4_tela_v4", "fase4_ensaio_v4", "fase4_ineditos"]
    assert taxas["metadados"]["hash_prompt_fixo"] == "2e42cf9c31826941" and taxas["metadados"]["hash_biblioteca"] == "95af35290860"
    m = taxas["por_modelo"]["qwen2.5:7b"]
    assert m["n"] == 120 and m["maquinas"] == ["TARGET_TSP030"] and m["versoes_ollama"] == ["0.40.14"] and m["teto_tokens"] == [600], {k: m[k] for k in ("n", "maquinas", "versoes_ollama", "teto_tokens")}
    for chave in ("prefill_tokens_por_s", "geracao_tokens_por_s", "tokens_saida", "tokens_entrada", "chars_por_token", "carga_ms"):
        d = m[chave]
        assert {"mediana", "p10", "p90", "min", "max", "n", "origem"} <= set(d), (chave, sorted(d))
        assert d["min"] <= d["p10"] <= d["mediana"] <= d["p90"] <= d["max"], (chave, d)
        assert d["n"] == 120, (chave, d["n"])
    assert "diagnosticos__" in m["prefill_tokens_por_s"]["origem"] and "trilha" in m["chars_por_token"]["origem"], "cada número diz de onde veio"
    # a mesma conta, feita à parte sobre os registros: a mediana do prefill em tokens por segundo
    taxas_prefill, taxas_geracao = [], []
    for _, pasta, _ in _corridas_vigentes():
        for arq in sorted((pasta / "qwen2.5_7b").glob("diagnosticos__*.jsonl")):
            for linha in arq.read_text(encoding="utf-8").splitlines():
                r = json.loads(linha)
                taxas_prefill.append(r["tokens_entrada"] / (r["prefill_ms"] / 1000))
                taxas_geracao.append(r["tokens_saida"] / (r["geracao_ms"] / 1000))
    assert len(taxas_prefill) == 120
    assert m["prefill_tokens_por_s"]["mediana"] == round(statistics.median(taxas_prefill), 3), (m["prefill_tokens_por_s"]["mediana"], statistics.median(taxas_prefill))
    assert m["geracao_tokens_por_s"]["mediana"] == round(statistics.median(taxas_geracao), 3)
    assert 15 < m["prefill_tokens_por_s"]["mediana"] < 60 and 3 < m["geracao_tokens_por_s"]["mediana"] < 6 and 2.5 < m["chars_por_token"]["mediana"] < 3.6
    gravado = RA / "fase4" / "taxas_progresso.json"
    assert gravado.exists(), "taxas_progresso.json ainda não gravado (progresso.py --taxas)"
    assert pg.sem_data(pg.carregar_taxas(gravado)) == pg.sem_data(taxas), "o arquivo gravado difere da extração de agora (progresso.py --taxas --check)"
    assert (RA / "fase4" / "taxas_progresso.md").exists()


def teste_progresso_erro_da_estimativa_medido_sobre_os_registros_gravados_com_check():
    import progresso as pg
    erro = pg.medir_erro()
    r = erro["por_modelo"]["qwen2.5:7b"]
    assert r["n"] == 120 and set(r["modos"]) == {"fora_da_corrida", "na_amostra"}, (r["n"], r.get("modos"))
    for modo in ("fora_da_corrida", "na_amostra"):
        for fase in ("prefill_s", "geracao_s", "total_s"):
            d = r[modo][fase]
            assert {"erro_abs_mediana_s", "erro_abs_p90_s", "erro_relativo_mediana", "erro_mediana_s", "subestimados", "n"} <= set(d), (modo, fase, sorted(d))
            assert d["n"] == 120 and 0 <= d["subestimados"] <= 120 and d["erro_abs_mediana_s"] <= d["erro_abs_p90_s"], (modo, fase, d)
    assert r["fora_da_corrida"]["total_s"]["erro_abs_mediana_s"] < 60, "a estimativa erra menos que a própria inferência dura"
    assert len(r["por_registro"]) == 120 and {"corrida", "caso", "estimado", "medido", "erro"} <= set(r["por_registro"][0])
    assert erro["metadados"]["taxas_de"] == "taxas_progresso.json", erro["metadados"]
    gravado = RA / "fase4" / "erro_progresso.json"
    assert gravado.exists(), "erro_progresso.json ainda não gravado (progresso.py --erro)"
    assert pg.sem_data(json.loads(gravado.read_text(encoding="utf-8"))) == pg.sem_data(erro), "o arquivo gravado difere da medida de agora (progresso.py --erro --check)"


def teste_executar_fase4_liga_a_barra_nos_modos_com_modelo_e_o_ps1_diz_onde_fica_o_estado():
    import caminhos
    import cliente_ollama as oll
    import executar_fase4 as ex
    import progresso as pg
    # ! Alteração de IA - Revisar: (10/11/2026, decisão 116) o modo `sem_notas` (corrida 25) entra na lista dos modos com modelo.
    # ! Motivo: a corrida 25 chama o modelo 72 vezes e ganha a barra de progresso e as conferências de Ollama, RAM e versão como as outras.
    # ! Alteração de IA - Revisar: (10/11/2026, decisão 120) o modo `segundo_passe` (corrida 26) entra na lista dos modos com modelo.
    # ! Motivo: a corrida 26 chama o modelo uma vez por caso com sinal (24 vezes) e ganha a barra de progresso e as conferências de Ollama, RAM e versão como as outras.
    # ! Alteração de IA - Revisar: (11/11/2026, decisão 121) o modo `analista` (corrida 27) entra na lista dos modos com modelo.
    # ! Motivo: a corrida 27 chama o modelo uma vez por caso de aprendizado (54 vezes) e ganha a barra de progresso e as conferências de Ollama, RAM e versão como as outras.
    assert set(ex.MODOS_COM_MODELO) == {"calibracao", "tela", "biblioteca", "cenarios", "avaliacao_trilha", "experimento_prompt", "ineditos", "sem_notas", "segundo_passe", "analista"}
    bruto = (EXP / "rodar_fase4.ps1").read_bytes()
    assert bruto[:3] == b"\xef\xbb\xbf", "rodar_fase4.ps1 precisa de BOM"
    texto = bruto.decode("utf-8-sig")
    assert "—" not in texto, "travessão quebra o parse do .ps1"
    linha_com_modelo = texto.split("$ComModelo =", 1)[1].split("\n", 1)[0]
    assert set(re.findall(r'\$Modo -eq "([a-z_]+)"', linha_com_modelo)) == set(ex.MODOS_COM_MODELO), "a lista dos modos com modelo do .ps1 e a do executor têm de ser a mesma"
    assert "progresso.json" in texto, "o .ps1 diz no log onde está o estado da barra"
    assert "com_progresso" in inspect.getsource(ex.main)
    raiz = _temp()
    original = caminhos.RESULTADOS
    caminhos.RESULTADOS = raiz
    try:
        chamadas: list = []
        with _ollama_trocado(_post_de_mentira(chamadas)):
            args = argparse.Namespace(modo="ineditos", saida="_fumaca_q4", modelo="modelo-de-teste")
            codigo = ex.com_progresso(args, lambda a: (oll.gerar(a.modelo, "z" * 700, 600), 0)[1], saida=io.StringIO())
            assert codigo == 0
            estado = pg.ler_estado(raiz / "_fumaca_q4" / "progresso.json")
            assert estado["estado"] == "concluido" and estado["modelo"] == "modelo-de-teste" and estado["chars_prompt"] == 700, estado
            args2 = argparse.Namespace(modo="reproducao", saida="_fumaca_q4_sem_modelo", modelo="modelo-de-teste")
            assert ex.com_progresso(args2, lambda a: 0, saida=io.StringIO()) == 0
            assert not (raiz / "_fumaca_q4_sem_modelo").exists(), "modo sem modelo não ganha barra nem pasta"
    finally:
        caminhos.RESULTADOS = original


def teste_impacto_mapa_vem_do_frontmatter_dos_verbetes_e_das_rotas_dos_cenarios_sem_alterar_a_biblioteca():
    import cenarios_fase4 as cen
    import evolucao_biblioteca as evo
    import impacto_git as ig
    antes = evo.hash_biblioteca(ig.PASTA_BIBLIOTECA)
    m = ig.mapa()
    assert evo.hash_biblioteca(ig.PASTA_BIBLIOTECA) == antes == "95af35290860", "o mapa só lê a biblioteca de produção"
    verbetes = bib.carregar(ig.PASTA_BIBLIOTECA)
    assert set(m["verbetes"]) == {v["id"] for v in verbetes} and len(m["verbetes"]) == 39
    for v in verbetes:
        assert m["verbetes"][v["id"]]["arquivos"] == list(v["meta"].get("arquivos", [])) and m["verbetes"][v["id"]]["endpoints"] == list(v["meta"].get("endpoints", [])), v["id"]
    assert sum(1 for x in m["verbetes"].values() if x["endpoints"]) == 24 and sum(1 for x in m["verbetes"].values() if x["arquivos"]) == 38
    assert m["verbetes"]["contrato-produto"]["endpoints"] == ["GET /api/produtos", "GET /api/produtos/{id}"]
    assert set(m["cenarios"]) == {c["id"] for c in cen.CENARIOS}
    c = m["cenarios"]["api-catalogo"]
    assert c["cobaia"] == "api" and c["endpoints"] == ["GET /api/produtos"], c
    assert "Programacao/CobaiaFront/produtos_api.php" in c["arquivos"] and "Programacao/CobaiaFront/menu_publico.php" in c["arquivos"], c["arquivos"]
    assert c["arquivos_por_origem"]["Programacao/CobaiaFront/menu_publico.php"].startswith("include"), c["arquivos_por_origem"]
    assert "contrato-produto" in c["verbetes"] and "campo_ausente" in c["verbetes"] and "contrato-pedido" not in c["verbetes"], c["verbetes"]
    assert "Programacao/CobaiaAPI/app/routers/produtos.py" in c["arquivos"], "os arquivos dos verbetes do endpoint entram no cenário"
    b = m["cenarios"]["front-busca"]
    assert b["endpoints"] == [] and b["verbetes"] == [] and {"Programacao/CobaiaFront/index.php", "Programacao/CobaiaFront/menu_publico.php", "Programacao/CobaiaFront/quebra.php",
                                                               "Programacao/CobaiaFront/conn/connect.php"} <= set(b["arquivos"]), b["arquivos"]
    assert set(m["ensaio"]) == {c["id"] for c in cen.CENARIOS_DO_ENSAIO} and m["ensaio"]["contrato-malformed_json"] == "api-catalogo" and m["ensaio"]["localizador-front-busca"] == "front-busca"
    assert "api-catalogo" in m["arquivos"]["Programacao/CobaiaAPI/app/routers/produtos.py"]["cenarios"] and "contrato-produto" in m["arquivos"]["Programacao/CobaiaAPI/app/routers/produtos.py"]["verbetes"]
    assert all((ig.RAIZ / a).exists() for a in m["arquivos"]), [a for a in m["arquivos"] if not (ig.RAIZ / a).exists()]


def teste_impacto_selecao_diz_cenarios_verbetes_e_motivo_e_aplica_as_tres_regras_da_base_e():
    import cenarios_fase4 as cen
    import impacto_git as ig
    m = ig.mapa()
    s = ig.selecionar(["Programacao/CobaiaAPI/app/routers/produtos.py"], m)
    assert s["rodar_tudo"] is False and set(s["cenarios"]) == {"api-catalogo", "api-detalhe"}, s["cenarios"]
    assert "contrato-produto" in s["verbetes"] and all(s["verbetes"][v] for v in s["verbetes"])
    assert any("contrato-produto" in x and "GET /api/produtos" in x for x in s["cenarios"]["api-catalogo"]), s["cenarios"]["api-catalogo"]
    assert set(s["ensaio"]) == {c["id"] for c in cen.CENARIOS_DE_CONTRATO}
    assert s["deixados_de_fora"]["cenarios"] == ["front-admin-login", "front-admin-produtos", "front-busca", "front-cliente-reserva"]
    assert s["conferencia"]["rodada_completa"] == sorted(m["cenarios"]) and s["conferencia"]["deixados_de_fora"] == s["deixados_de_fora"]["cenarios"]
    assert s["arquivos"] == [{"arquivo": "Programacao/CobaiaAPI/app/routers/produtos.py", "classe": "no_mapa", "motivo": s["arquivos"][0]["motivo"]}] and "contrato-produto" in s["arquivos"][0]["motivo"]
    s2 = ig.selecionar(["Programacao/CobaiaFront/js/novo.js"], m)
    assert s2["rodar_tudo"] is True and set(s2["cenarios"]) == set(m["cenarios"]) and set(s2["ensaio"]) == set(m["ensaio"]), "arquivo da aplicação fora do mapa roda tudo, nunca nada"
    assert s2["arquivos"][0]["classe"] == "fora_do_mapa" and s2["deixados_de_fora"]["cenarios"] == [] and "fora do mapa" in s2["motivo"]
    s3 = ig.selecionar(["Documentacao/memorial/roadmap.md"], m)
    assert s3["rodar_tudo"] is False and s3["cenarios"] == {} and s3["arquivos"][0]["classe"] == "fora_da_aplicacao" and "rodada completa" in s3["motivo"], s3["motivo"]
    s4 = ig.selecionar(["Programacao/CobaiaAPI/.venv/Lib/site-packages/x.py", "Programacao/CobaiaAPI/tests/test_x.py", "Programacao/CobaiaAPI/app/__pycache__/a.cpython-312.pyc"], m)
    assert s4["rodar_tudo"] is False and s4["cenarios"] == {} and all(a["classe"] == "ignorado" for a in s4["arquivos"]), s4["arquivos"]
    s5 = ig.selecionar(["Programacao/CobaiaFront/admin/login.php", "Programacao/CobaiaAPI/pyproject.toml"], m)
    assert s5["rodar_tudo"] is True and "front-admin-login" in s5["cenarios"] and "usuario-e-login" in s5["verbetes"]
    assert [a["classe"] for a in s5["arquivos"]] == ["fora_do_mapa", "no_mapa"], s5["arquivos"]
    assert set(ig.REGRAS) == {"fora_do_mapa_roda_tudo", "rodada_completa_periodica", "conferencia_contra_a_rodada_completa"} and all(ig.REGRAS.values())
    assert ig.selecionar([], m)["motivo"].startswith("nenhum arquivo")


def teste_impacto_le_o_diff_de_um_repositorio_temporario_e_de_um_commit_conhecido_do_historico():
    import impacto_git as ig
    repo = _temp()

    def git(*argumentos: str) -> str:
        return subprocess.run(["git", "-c", "user.name=teste", "-c", "user.email=teste@exemplo.com", *argumentos], cwd=repo, check=True,
                              capture_output=True, text=True, encoding="utf-8").stdout.strip()

    git("init", "-q")
    (repo / "Programacao" / "CobaiaAPI" / "app" / "routers").mkdir(parents=True)
    (repo / "Programacao" / "CobaiaAPI" / "app" / "routers" / "produtos.py").write_text("x = 1\n", encoding="utf-8")
    git("add", "-A")
    git("commit", "-q", "-m", "a")
    a = git("rev-parse", "HEAD")
    (repo / "Programacao" / "CobaiaAPI" / "app" / "routers" / "produtos.py").write_text("x = 2\n", encoding="utf-8")
    (repo / "Documentacao").mkdir()
    (repo / "Documentacao" / "nota.md").write_text("nota\n", encoding="utf-8")
    git("add", "-A")
    git("commit", "-q", "-m", "b")
    b = git("rev-parse", "HEAD")
    assert ig.arquivos_alterados(repo, a, b) == ["Documentacao/nota.md", "Programacao/CobaiaAPI/app/routers/produtos.py"]
    assert ig.arquivos_alterados(repo, a, "HEAD", so_aplicacao=True) == ["Programacao/CobaiaAPI/app/routers/produtos.py"]
    assert ig.arquivos_alterados(repo, b, b) == []
    s = ig.selecionar(ig.arquivos_alterados(repo, a, b), ig.mapa())
    assert set(s["cenarios"]) == {"api-catalogo", "api-detalhe"} and [x["classe"] for x in s["arquivos"]] == ["fora_da_aplicacao", "no_mapa"]
    alterados = ig.arquivos_alterados(RAIZ, "633ebb27^", "633ebb27", so_aplicacao=True)
    assert len(alterados) == 5 and "Programacao/CobaiaFront/quebra.php" in alterados and "Programacao/CobaiaFront/menu_publico.php" in alterados, alterados
    commits = ig.commits_da_aplicacao(RAIZ)
    assert [c["commit"][:8] for c in commits] == COMMITS_DA_APLICACAO and all({"commit", "data", "assunto"} <= set(c) for c in commits), commits


def teste_impacto_prova_no_historico_do_repositorio_gravada_e_conferida_com_check():
    import impacto_git as ig
    dado, md = ig.prova()
    assert [c["commit"][:8] for c in dado["commits"]] == COMMITS_DA_APLICACAO
    pares = dado["pares"]
    assert len(pares) == 7 and pares[0]["testado"][:8] == "e854a0eb" and pares[0]["atual"][:8] == "ab4da6a1" and pares[-1]["atual"][:8] == "633ebb27"
    por = {p["atual"][:8]: p for p in pares}
    assert por["4f3b3e26"]["selecao"]["rodar_tudo"] is False and set(por["4f3b3e26"]["selecao"]["cenarios"]) == {"api-catalogo", "api-detalhe"}, por["4f3b3e26"]["selecao"]["cenarios"]
    assert por["4f3b3e26"]["resumo"]["ignorados"] == 1 and por["4f3b3e26"]["resumo"]["no_mapa"] == 2, por["4f3b3e26"]["resumo"]
    fora = [a["arquivo"] for a in por["084fce09"]["selecao"]["arquivos"] if a["classe"] == "fora_do_mapa"]
    assert por["084fce09"]["selecao"]["rodar_tudo"] is True and "Programacao/CobaiaAPI/pyproject.toml" in fora, fora
    na_venv = len(ig.arquivos_alterados(RAIZ, "603c423e", "3e8cfc14", so_aplicacao=True))   # a retirada da venv do git: só arquivos ignorados
    assert na_venv > 2000 and por["3e8cfc14"]["selecao"]["cenarios"] == {} and por["3e8cfc14"]["resumo"]["ignorados"] == por["3e8cfc14"]["resumo"]["na_aplicacao"] == na_venv, por["3e8cfc14"]["resumo"]
    assert por["633ebb27"]["selecao"]["rodar_tudo"] is False and {"front-busca", "front-admin-login", "front-admin-produtos", "front-cliente-reserva"} <= set(por["633ebb27"]["selecao"]["cenarios"])
    # os cenários da API também entram, porque menu_publico.php (alterado) é incluído por produtos_api.php: o mapa dos includes liga os dois
    assert por["633ebb27"]["selecao"]["deixados_de_fora"]["cenarios"] == [] and any("menu_publico.php" in x and "include" in x for x in por["633ebb27"]["selecao"]["cenarios"]["api-catalogo"])
    assert set(dado["regras"]) == set(ig.REGRAS) and dado["mapa"]["cenarios"] == len(ig.mapa()["cenarios"]) and dado["mapa"]["verbetes"] == 39
    resumo = dado["resumo"]
    assert resumo["pares"] == 7 and resumo["rodar_tudo"] + resumo["selecao_parcial"] + resumo["nada_a_rodar"] == 7, resumo
    assert resumo["rodar_tudo"] >= 2 and resumo["selecao_parcial"] >= 2 and resumo["nada_a_rodar"] >= 1, resumo
    assert "—" not in md and "→" not in md and "quebra.php" in md and "pyproject.toml" in md
    gravado = RA / "fase4" / "impacto_git.json"
    assert gravado.exists(), "impacto_git.json ainda não gravado (impacto_git.py --prova)"
    assert ig.sem_data(json.loads(gravado.read_text(encoding="utf-8"))) == ig.sem_data(dado), "o arquivo gravado difere da prova de agora (impacto_git.py --prova --check)"
    assert (RA / "fase4" / "impacto_git.md").read_text(encoding="utf-8").split("\n", 3)[-1] == md.split("\n", 3)[-1]


# ------------------------------------------------------------------ Q5: a sessão de revisão com revisor humano, por cartões
# ! Alteração de IA - Revisar: (08/11/2026, Pós-Fase 4, pacote Q5) testes de `revisao_v3.py` e da leitura `avaliar_fase4.py --revisao_v3`: a ordem dos 36 casos da
# corrida 24 sorteada com semente fixa, sem revelar o acerto; a cópia da sessão (relatório v3 mais árvore de decisão) sem o nome do caso, a classe, o nível e o comando
# de reexecução, e a recusa de um texto que traga o resultado do caso ou o nome de outro; a planilha `revisao_v3.md` e as cópias gravadas com --check, com a planilha
# nunca regravada depois de começada; o cartão (início marcado, resposta com o tempo, valor inválido, linha repetida ou cartão sem início recusados, próximo em branco);
# e a leitura contra `ineditos.json`, que só sai com a planilha inteira.
# ! Motivo: a ficha 40 foi fechada em 08/11/2026 pela opção (b): o Eric faz a sessão aqui, um relatório por cartão; como na sessão de 05/11/2026, a conta e o registro
# têm de existir e estar testados antes do primeiro cartão, para a leitura não depender de nada escrito depois de ver as respostas.
import revisao_v3 as rv


def _casos_de_revisao_de_teste(n: int = 4) -> list[dict]:
    """Os n primeiros casos reais de ineditos.json (os relatórios v3 e as árvores deles existem na corrida 24)."""
    casos = json.loads((RA / "fase4" / "ineditos.json").read_text(encoding="utf-8"))["casos"]
    return [dict(c) for c in casos[:n]]


def _pasta_de_revisao_de_teste(casos: list[dict]) -> Path:
    pasta = _temp()
    (pasta / "ineditos.json").write_text(json.dumps({"metadados": {"corrida": "fase4_ineditos"}, "casos": casos}, ensure_ascii=False), encoding="utf-8")
    return pasta


def teste_revisao_v3_amostra_inteira_embaralhada_com_semente_fixa_sem_revelar_o_acerto():
    casos = [{"caso": f"lex-{i}", "classe": 1 + i % 6, "acerto": i % 3 != 0} for i in range(1, 37)]
    a, b = rv.amostra(casos), rv.amostra(casos)
    assert [x["caso"] for x in a] == [x["caso"] for x in b] and len(a) == 36
    assert [x["posicao"] for x in a] == list(range(1, 37))
    assert [x["caso"] for x in a] != sorted(x["caso"] for x in a)
    acertos = [x["acerto"] for x in a]
    assert acertos != sorted(acertos) and acertos != sorted(acertos, reverse=True)
    assert all(x["relatorio"] == f"{rv.PASTA_SESSAO}/relatorio-{x['posicao']}.md" for x in a)
    assert sorted(x["caso"] for x in a) == sorted(c["caso"] for c in casos)


def teste_revisao_v3_copia_da_sessao_esconde_nome_classe_nivel_e_comando_e_mantem_o_relatorio_e_a_arvore():
    v3 = (RA / "fase4_ineditos" / "relatorios_v3" / "lex-22.md").read_text(encoding="utf-8")
    arvore = (RA / "fase4_ineditos" / "arvores" / "lex-22.md").read_text(encoding="utf-8")
    copia = rv.copia_da_sessao(v3, arvore, "lex-22", 7, 36)
    assert "lex-22" not in copia and copia.count("relatorio-7") >= 10, copia.count("relatorio-7")
    assert not rv.RE_NOME_DE_CASO.search(copia)
    sobras = [m.group(0) for m in re.finditer(r".{0,30}(classe \d|n[íi]vel \d|--ids|Comando (?:para reexecutar|de reexecução)).{0,30}", copia)]
    assert not sobras, sobras
    assert rv.CLASSE_OMITIDA in copia
    assert copia.lstrip().startswith("<!-- ! Alteração de IA - Revisar") and "# Relatório 7 de 36" in copia
    for trecho in ("## 6. Descrição para reproduzir", "<html><body><h1>Erro</h1>", "## Decisão 2: que verbetes entram", "acertou a causa em 22 de 26"):
        assert trecho in copia, trecho


def teste_revisao_v3_copia_recusa_texto_com_o_resultado_ou_com_o_nome_de_outro_caso():
    v3 = "# Relatório de defeito\n\nCaso `lex-22` da corrida `fase4_ineditos`.\n"
    arvore = "# Árvore de decisão do caso `lex-22`\n\nResumo.\n"
    for ruim in ("o agente acertou este caso", "causa_correta: corpo_vazio", "a decisão errou", "o rótulo esperado era outro"):
        try:
            rv.copia_da_sessao(v3 + ruim + "\n", arvore, "lex-22", 1, 1)
        except ValueError as e:
            assert "resultado" in str(e), e
        else:
            raise AssertionError(f"aceitou um texto com o resultado: {ruim!r}")
    try:
        rv.copia_da_sessao(v3, arvore + "Como em `sin-5`.\n", "lex-22", 1, 1)
    except ValueError as e:
        assert "sin-5" in str(e), e
    else:
        raise AssertionError("aceitou o nome de outro caso")
    copia = rv.copia_da_sessao(v3, arvore + "Na calibração, o agente acertou a causa em 22 de 26: 84,6% (observado).\n", "lex-22", 1, 1)
    assert "acertou a causa em 22 de 26" in copia and "lex-22" not in copia and "relatorio-1" in copia


def teste_revisao_v3_gera_planilha_e_copias_com_check_e_nao_regrava_a_planilha_comecada():
    casos = _casos_de_revisao_de_teste(4)
    pasta = _pasta_de_revisao_de_teste(casos)
    r = rv.gerar(pasta, RA / "fase4_ineditos")
    assert r["planilha"] == "gravada" and r["copias"] == 4 and not r["diferentes"]
    planilha = (pasta / rv.NOME_PLANILHA).read_text(encoding="utf-8")
    linhas = [l for l in planilha.splitlines() if re.match(r"^\| \d+ \|", l)]
    assert len(linhas) == 4 and all(rv.CELULA_EM_BRANCO in l for l in linhas) and "ineditos.json" in planilha
    assert sorted(x["caso"] for x in rv.ler_planilha(pasta)) == sorted(c["caso"] for c in casos)
    assert all((pasta / x["relatorio"]).exists() for x in r["amostra"])
    assert rv.gerar(pasta, RA / "fase4_ineditos", check=True)["diferentes"] == []
    (pasta / r["amostra"][0]["relatorio"]).write_text("mudado", encoding="utf-8")
    assert rv.gerar(pasta, RA / "fase4_ineditos", check=True)["diferentes"] == [r["amostra"][0]["relatorio"]]
    rv.gerar(pasta, RA / "fase4_ineditos")
    assert rv.gerar(pasta, RA / "fase4_ineditos", check=True)["diferentes"] == []
    rv.marcar_inicio(pasta, 1, agora=100.0)
    rv.responder(pasta, 1, decisao="aceitar", avaliacao="certo", erro="n.a.", utilidade=4, agora=130.0)
    r2 = rv.gerar(pasta, RA / "fase4_ineditos")
    assert r2["planilha"] == "mantida" and "| 30 | n.a. | aceitar | 4 | certo |" in (pasta / rv.NOME_PLANILHA).read_text(encoding="utf-8")
    assert not (pasta / "revisao_v3.nova.md").exists()
    assert rv.gerar(pasta, RA / "fase4_ineditos", check=True)["diferentes"] == []


def teste_revisao_v3_cartao_marca_o_inicio_grava_a_resposta_com_o_tempo_e_recusa_invalido_repetido_ou_sem_inicio():
    pasta = _pasta_de_revisao_de_teste(_casos_de_revisao_de_teste(3))
    rv.gerar(pasta, RA / "fase4_ineditos")
    p = rv.proximo_em_branco(pasta)
    assert p["posicao"] == 1 and p["faltam"] == 3 and p["total"] == 3 and p["relatorio"] == f"{rv.PASTA_SESSAO}/relatorio-1.md"
    try:
        rv.responder(pasta, 1, decisao="aceitar", avaliacao="certo", erro="n.a.", utilidade=4, agora=10.0)
    except ValueError as e:
        assert "início" in str(e), e
    else:
        raise AssertionError("respondeu sem o início marcado")
    rv.marcar_inicio(pasta, 1, agora=1000.0)
    r = rv.responder(pasta, 1, decisao="recusar", avaliacao="errado", erro="sim", utilidade=2, comentario="a causa | é outra", agora=1012.4)
    assert r["segundos"] == 12 and r["caso"] == "relatorio-1" and r["comentario"] == "a causa / é outra"
    linha = next(l for l in (pasta / rv.NOME_PLANILHA).read_text(encoding="utf-8").splitlines() if l.startswith("| 1 |"))
    assert linha.endswith("| 12 | sim | recusar | 2 | errado | a causa / é outra |"), linha
    respostas = json.loads((pasta / rv.PASTA_SESSAO / rv.NOME_RESPOSTAS).read_text(encoding="utf-8"))
    assert len(respostas) == 1 and respostas[0]["posicao"] == 1 and respostas[0]["segundos"] == 12 and respostas[0]["inicio"]
    assert rv.proximo_em_branco(pasta)["posicao"] == 2
    rv.marcar_inicio(pasta, 2, agora=2000.0)
    for ruim in ({"utilidade": 6}, {"utilidade": 0}, {"decisao": "talvez"}, {"erro": "sim?"}, {"avaliacao": "ok"}):
        try:
            rv.responder(pasta, 2, **{"decisao": "aceitar", "avaliacao": "certo", "erro": "n.a.", "utilidade": 3, "agora": 2005.0, **ruim})
        except ValueError:
            pass
        else:
            raise AssertionError(f"aceitou {ruim}")
    assert rv.proximo_em_branco(pasta)["posicao"] == 2
    try:
        rv.responder(pasta, 1, decisao="aceitar", avaliacao="certo", erro="n.a.", utilidade=4, agora=3000.0)
    except ValueError as e:
        assert "preenchid" in str(e), e
    else:
        raise AssertionError("regravou uma linha preenchida sem corrigir")
    r = rv.responder(pasta, 1, decisao="aceitar", avaliacao="certo", erro="n.a.", utilidade=4, agora=3000.0, corrigir=True)
    assert r["segundos"] == 2000 and r["corrigida"]
    assert len(json.loads((pasta / rv.PASTA_SESSAO / rv.NOME_RESPOSTAS).read_text(encoding="utf-8"))) == 2


def teste_revisao_v3_leitura_le_a_planilha_contra_ineditos_json_e_so_sai_inteira():
    import avaliar_fase4 as av
    casos = _casos_de_revisao_de_teste(36)
    um_certo = next(c for c in casos if c["acerto"])
    um_errado = next(c for c in casos if not c["acerto"])
    pasta = _pasta_de_revisao_de_teste([um_certo, um_errado])
    rv.gerar(pasta, RA / "fase4_ineditos")
    kw = {"planilha": rv.NOME_PLANILHA, "fonte": rv.FONTE, "titulo": av.TITULO_REVISAO_V3, "prefixo": av.PREFIXO_REVISAO_V3, "nota": av.nota_da_revisao_v3,
          "origem_sem_tempo": av.ORIGEM_ANALISTA, "rotulos": av.ROTULO_ORIGEM_V3, "doc": pasta / "sem_relatorio.md"}
    assert av.fechar_revisao(pasta, av.NOME_REVISAO_V3, **kw) == 2 and not (pasta / f"{av.NOME_REVISAO_V3}.json").exists()
    ordem = {x["caso"]: x["posicao"] for x in rv.ler_planilha(pasta)}
    rv.marcar_inicio(pasta, ordem[um_certo["caso"]], agora=0.0)
    rv.responder(pasta, ordem[um_certo["caso"]], decisao="aceitar", avaliacao="certo", erro="n.a.", utilidade=4, agora=40.0)
    rv.marcar_inicio(pasta, ordem[um_errado["caso"]], agora=100.0)
    rv.responder(pasta, ordem[um_errado["caso"]], decisao="recusar", avaliacao="errado", erro="sim", utilidade=3, agora=190.0)
    assert av.fechar_revisao(pasta, av.NOME_REVISAO_V3, **kw) == 0
    dado = json.loads((pasta / f"{av.NOME_REVISAO_V3}.json").read_text(encoding="utf-8"))
    r = dado["resumo"]
    assert r["relatorios"] == 2 and r["adesao_apropriada"] == 2 and r["respostas_do_revisor"] == 2 and r["pareceres_aprovados"] == 0 and r["erros_localizados"] == 1
    assert r["respostas_do_analista"] == 0
    assert dado["metadados"]["planilha"] == rv.NOME_PLANILHA and dado["metadados"]["corrida"] == "fase4_ineditos" and r["tempo_mediana_s"] == 65
    assert dado["casos"][0]["caso"] in (um_certo["caso"], um_errado["caso"]) and dado["parecer"] is None
    md = (pasta / f"{av.NOME_REVISAO_V3}.md").read_text(encoding="utf-8")
    assert f"{av.PREFIXO_REVISAO_V3}resumo" in md and "tb_f4_revisao_resumo" not in md and av.TITULO_REVISAO_V3 in md and "página da sessão" in md and "revisao_v3.md" in md
    assert "1 dos 1 erros" in md and "1 dos 1 acertos" in md
    assert av.fechar_revisao(pasta, av.NOME_REVISAO_V3, check=True, **kw) == 0
    # ! Alteração de IA - Revisar: (10/11/2026) a segunda metade do teste: uma linha passa a ser a resposta de um analista (sem tempo medido) e a leitura a separa.
    # ! Motivo: na sessão de 09 e 10/11/2026 quase todas as respostas vieram de um analista a quem o Eric passou os relatórios; a leitura tinha registrado as 36
    # como do Eric, com o tempo da troca entre os dois no lugar do tempo de leitura.
    planilha = pasta / rv.NOME_PLANILHA
    texto = planilha.read_text(encoding="utf-8")
    assert "| 90 | sim | recusar | 3 | errado |" in texto
    planilha.write_text(texto.replace("| 90 | sim | recusar | 3 | errado |", f"| {av.TEMPO_NAO_MEDIDO} | sim | recusar | 3 | errado |", 1), encoding="utf-8", newline="\n")
    assert av.fechar_revisao(pasta, av.NOME_REVISAO_V3, **kw) == 0
    dado = json.loads((pasta / f"{av.NOME_REVISAO_V3}.json").read_text(encoding="utf-8"))
    r = dado["resumo"]
    assert (r["respostas_do_revisor"], r["respostas_do_analista"], r["pareceres_aprovados"]) == (1, 1, 0), r
    assert r["adesao_apropriada"] == 2 and r["tempo_mediana_s"] == 40, "o tempo só conta onde a página mediu uma leitura"
    assert [(x["origem"], x["n"], x["apropriadas"]) for x in dado["por_origem"]] == [("revisor", 1, 1), (av.ORIGEM_ANALISTA, 1, 1)]
    assert next(x for x in dado["tempo"] if x["grupo"] == "todos")["n"] == 1
    assert next(c for c in dado["casos"] if c["caso"] == um_errado["caso"])["origem"] == av.ORIGEM_ANALISTA
    md = (pasta / f"{av.NOME_REVISAO_V3}.md").read_text(encoding="utf-8")
    for trecho in (av.ROTULO_ORIGEM_V3["revisor"], av.ROTULO_ORIGEM_V3[av.ORIGEM_ANALISTA], "um analista", "não medido", "1 dos 2 relatórios", "troca entre os dois"):
        assert trecho in md, trecho
    assert "parecer do Claude" not in md and "pré-análise" not in md
    assert av.fechar_revisao(pasta, av.NOME_REVISAO_V3, check=True, **kw) == 0
    # com a declaração de quem leu gravada ao lado, a leitura a carrega e a nota a cita
    (pasta / rv.PASTA_SESSAO / "quem_leu.json").write_text(json.dumps({"declarado_em": "2026-11-10", "quem": "um analista de QA da empresa em que o Eric trabalha",
                                                                      "relacao_com_o_projeto": "não participou do projeto nem conhecia o agente"}, ensure_ascii=False), encoding="utf-8")
    assert av.ARQ_QUEM_LEU_V3 == f"{rv.PASTA_SESSAO}/quem_leu.json"
    assert av.fechar_revisao(pasta, av.NOME_REVISAO_V3, quem_leu=av.ARQ_QUEM_LEU_V3, **kw) == 0
    dado = json.loads((pasta / f"{av.NOME_REVISAO_V3}.json").read_text(encoding="utf-8"))
    assert dado["quem_leu"]["quem"] == "um analista de QA da empresa em que o Eric trabalha"
    assert "um analista de QA da empresa em que o Eric trabalha" in (pasta / f"{av.NOME_REVISAO_V3}.md").read_text(encoding="utf-8")
    # a leitura de 05/11 continua separando o parecer do Claude aprovado, como antes
    assert av.ler_planilha_de_revisao(planilha.read_text(encoding="utf-8"))["linhas"][0]["origem"] in ("revisor", "parecer_aprovado")
    assert {l["origem"] for l in av.ler_planilha_de_revisao(planilha.read_text(encoding="utf-8"), origem_sem_tempo=av.ORIGEM_ANALISTA)["linhas"]} == {"revisor", av.ORIGEM_ANALISTA}


# ! Alteração de IA - Revisar: (10/11/2026) teste de `avaliar_fase4.resumo_da_pagina` e da parte da nota da revisão que cita o registro da página.
# ! Motivo: é desse registro (as horas de cada resposta no banco da página) que sai a evidência de que o comentário chegou pronto e foi colado, e a resposta trocada
# depois de salva não pode entrar na conta da velocidade, porque o comentário dela é de outra hora.
def teste_revisao_v3_registro_da_pagina_mede_como_as_respostas_entraram_e_a_nota_o_cita():
    import avaliar_fase4 as av
    respostas = [
        {"posicao": 1, "segundos": 200, "aberto_em": "2026-11-09T10:00:00.000Z", "decidido_em": "2026-11-09T10:03:20.000Z", "salvo_em": "2026-11-09T10:04:20.000Z", "comentario": "x" * 90, "editado_em": None},
        {"posicao": 2, "segundos": 30, "aberto_em": "2026-11-09T10:05:00.000Z", "decidido_em": "2026-11-09T10:05:30.000Z", "salvo_em": "2026-11-09T10:05:40.000Z", "comentario": "y" * 600, "editado_em": None},
        {"posicao": 3, "segundos": 280, "aberto_em": "2026-11-09T10:06:00.000Z", "decidido_em": "2026-11-09T10:10:40.000Z", "salvo_em": "2026-11-09T10:10:45.000Z", "comentario": "z" * 500,
         "editado_em": "2026-11-09T19:00:00.000Z"},
    ]
    pg = av.resumo_da_pagina(respostas)
    assert pg["respostas"] == 3 and pg["intervalo_entre_relatorios_mediana_s"] == 180 and pg["decisao_ao_salvamento_mediana_s"] == 10 and pg["comentario_mediana_chars"] == 500
    assert pg["editadas_depois"] == [3] and pg["segundos_na_pagina"] == {"1": 200, "2": 30, "3": 280}
    assert (pg["comentarios_medidos"], pg["comentarios_acima_de_10_chars_por_s"]) == (2, 1), "a resposta trocada depois de salva fica fora da conta da velocidade"
    assert pg["primeira_abertura"] == "2026-11-09T10:00:00.000Z" and pg["ultimo_salvamento"] == "2026-11-09T10:10:45.000Z"
    assert av.resumo_da_pagina([{"posicao": 1, "segundos": 12, "inicio": "2026-11-09T10:00:00"}]) is None
    dado = {"resumo": {"relatorios": 3, "erros_na_amostra": 1, "erros_na_corrida": 1, "acertos_na_amostra": 2, "acertos_na_corrida": 2},
            "casos": [{"posicao": 1, "origem": "revisor"}, {"posicao": 2, "origem": av.ORIGEM_ANALISTA}, {"posicao": 3, "origem": av.ORIGEM_ANALISTA}], "pagina": pg}
    nota = av.nota_da_revisao_v3(dado)
    for trecho in ("1 dos 3 relatórios, na posição 1 da planilha, foi respondido pelo Eric", "Nos outros 2", "passaram 180 s na mediana", "500 caracteres na mediana", "salvo 10 s depois da decisão",
                   "em 1 dos 2 relatórios cuja resposta não foi trocada depois", "A resposta do relatório 3 foi trocada depois de salva", "tinha medido 280 s", "não está registrado"):
        assert trecho in nota, trecho
    # ! Alteração de IA - Revisar: (10/11/2026) a nota com a declaração de quem leu e com todas as respostas de um analista.
    # ! Motivo: o Eric declarou no quadro que o analista é de QA da empresa, não participou do projeto e respondeu os 36 relatórios; a nota dizia "dois leitores" e
    # que quem leu não estava registrado.
    so_analista = {**dado, "casos": [{"posicao": p, "origem": av.ORIGEM_ANALISTA} for p in (1, 2, 3)],
                   "quem_leu": {"declarado_em": "2026-11-10", "quem": "um analista de QA da empresa em que o Eric trabalha",
                                "relacao_com_o_projeto": "não participou do projeto nem conhecia o agente", "ferramenta_de_ia": None, "o_que_recebeu": None}}
    nota = av.nota_da_revisao_v3(so_analista)
    for trecho in ("Um leitor só, que não é o autor do trabalho", "os 3 relatórios foram respondidos por um analista de QA da empresa em que o Eric trabalha", "Pela declaração do Eric em 10/11/2026",
                   "não participou do projeto nem conhecia o agente", "se usou alguma ferramenta para ler ou redigir não foi declarado", "o que recebeu para ler não foi declarado",
                   "Nesses 3 relatórios o tempo entra como não medido", "o Eric digitou ou colou a resposta na página", "a página tinha medido 280 s antes da troca",
                   "No outro, o comentário entrou mais devagar que isso, no ritmo de quem digita; pela declaração do Eric, essa resposta também é do analista"):
        assert trecho in nota, trecho
    assert av.ROTULO_ORIGEM_V3[av.ORIGEM_ANALISTA] == "resposta de um analista, digitada ou colada pelo Eric"
    assert "Dois leitores" not in nota and "não está registrado" not in nota and "leitura do Eric" not in nota


# ------------------------------------------------------------------ corrida 25: a biblioteca sem as notas do modelo (ficha 63, decisão 116)

# ! Alteração de IA - Revisar: (10/11/2026, ficha 63 opção b, decisão 116) testes de `experimento_sem_notas.py`, escritos ANTES do código: a primeira rodada falha
# por ModuleNotFoundError, o RED aceito para módulo novo. A cópia da biblioteca sem a seção "Notas do modelo" e sem a pasta `aprendidos/` (o resto byte a byte, a
# origem intocada, a cópia alterada acusada no relance); a mesma cópia feita da biblioteca de produção, em que sobra só a parte escrita à mão dos verbetes; o nome
# da pasta da ponte de uma versão do Ollama; a regra que decide se a corrida segue depois da ponte; o resumo dos pares contra a referência com a regra do ruído
# fixada antes da corrida (teste pareado exato dos casos, com a ponte pareável); o Markdown da leitura; e a prévia sem modelo dos 72 contextos gravada e conferida.
# ! Motivo: o Eric escolheu no quadro medir, antes da Fase 5 e sem mudar o agente, quanto pesam as notas que o modelo escreveu na biblioteca (25 das 26 em forma de
# instrução, a observação do parecer do analista que procede). A corrida custa cerca de duas horas de máquina na janela dele; a regra do veredito tem de estar
# escrita e testada antes de o resultado existir, e a cópia da biblioteca tem de provar que só tirou o que diz que tirou.
_VERBETE_COM_NOTAS = ("---\r\n# comentário do frontmatter\r\nid: erro_a\r\ntitulo: Erro A\r\nsistema: CobaiaAPI\r\nentidade_principal: Produto\r\ntipo: erro\r\nstatus: ativo\r\n"
                      "sintomas: [preco vazio, acrescentado pelo modelo]\r\npalavras_chave: [preco, nulo]\r\ncausas_relacionadas: [campo_ausente]\r\n---\r\n"
                      "## Resumo\r\nO campo preco vem vazio.\r\n\r\n## Sinais\r\n- preco nulo\r\n\r\n## Causa\r\nA rota devolve nulo.\r\n\r\n## Notas do modelo\r\n"
                      "- [E1 · lex-3 · nota] Adicionar que o preco pode vir como texto. — Motivo: o caso mostrou.\r\n"
                      "- [E101 · run-5 · retificação de \"A rota devolve nulo\"] A rota devolve zero. — Motivo: visto no caso.\r\n")
_VERBETE_SEM_NOTAS = ("---\nid: contrato_b\ntitulo: Contrato B\nsistema: CobaiaAPI\nentidade_principal: Produto\ntipo: contrato\nstatus: ativo\nsintomas: [campo a mais]\n"
                      "palavras_chave: [contrato]\n---\n## Resumo\nO contrato do produto.\n\n## Sinais\n- campo a mais\n")
_VERBETE_APRENDIDO = ("---\nid: novo_c\ntitulo: Novo C\nsistema: Ambos\nentidade_principal: Interface\ntipo: aprendido\nstatus: ativo\nsintomas: [lista vazia]\n"
                      "palavras_chave: [fetch]\ncausas_relacionadas: [estado_da_tela_divergente]\n---\n## Resumo\nAdicionar verbete sobre a tela.\n\n## Sinais\n- lista vazia\n")


def _biblioteca_de_teste_com_notas() -> Path:
    raiz = _temp() / "biblioteca"
    for rel, texto in (("erros/erro_a.md", _VERBETE_COM_NOTAS), ("contratos/contrato_b.md", _VERBETE_SEM_NOTAS), ("aprendidos/novo_c.md", _VERBETE_APRENDIDO),
                       ("INDICE.md", "# índice\n")):
        arq = raiz / rel
        arq.parent.mkdir(parents=True, exist_ok=True)
        arq.write_bytes(texto.encode("utf-8"))
    (raiz / "fechamento.json").write_text("{}", encoding="utf-8")
    return raiz


def teste_sem_notas_copia_a_biblioteca_sem_a_secao_das_notas_e_sem_os_aprendidos():
    import biblioteca as bib
    import evolucao_biblioteca as evo
    import experimento_sem_notas as esn
    origem = _biblioteca_de_teste_com_notas()
    hash_origem = evo.hash_biblioteca(origem)
    destino = origem.parent / "copia" / "sem-notas"
    d = esn.montar_biblioteca(origem, destino)
    assert sorted(p.relative_to(destino).as_posix() for p in destino.rglob("*") if p.is_file()) == ["contratos/contrato_b.md", "derivacao.json", "erros/erro_a.md"]
    assert (destino / "contratos/contrato_b.md").read_bytes() == _VERBETE_SEM_NOTAS.encode("utf-8"), "o verbete sem notas é copiado byte a byte"
    cru = (destino / "erros/erro_a.md").read_bytes()
    assert b"Notas do modelo" not in cru and b"E101" not in cru
    assert cru == _VERBETE_COM_NOTAS.split("## Notas do modelo")[0].rstrip("\r\n").encode("utf-8") + b"\r\n", "o que vem antes da seção fica byte a byte, com a quebra de linha do arquivo"
    antes = {v["id"]: v for v in bib.carregar(origem)}
    depois = {v["id"]: v for v in bib.carregar(destino)}
    assert sorted(depois) == ["contrato_b", "erro_a"]
    for vid, v in depois.items():
        assert bib.notas(v) == [] and bib.render(v) == bib.render_base(antes[vid]) and v["meta"] == antes[vid]["meta"], vid
    assert d == {"origem_hash": hash_origem, "hash": evo.hash_biblioteca(destino), "verbetes": 2, "verbetes_retirados": ["novo_c"], "verbetes_com_notas": 1, "notas_retiradas": 2}, d
    assert json.loads((destino / "derivacao.json").read_text(encoding="utf-8")) == d
    assert evo.hash_biblioteca(origem) == hash_origem, "a biblioteca de origem não é tocada"
    # relançar com a cópia pronta devolve o mesmo, sem regravar; uma cópia alterada é acusada
    assert esn.montar_biblioteca(origem, destino) == d
    (destino / "erros/erro_a.md").write_bytes(cru + b"mexido\r\n")
    try:
        esn.montar_biblioteca(origem, destino)
    except SystemExit as e:
        assert "apague" in str(e), e
    else:
        raise AssertionError("a cópia alterada tinha de ser acusada")
    # a seção no meio do arquivo sai sem levar a seguinte, e o arquivo sem a seção volta como entrou
    assert esn.texto_sem_notas("## Resumo\nA.\n\n## Notas do modelo\n- [E1 · lex-1 · nota] B. — Motivo: C.\n\n## Causa\nD.\n") == ("## Resumo\nA.\n\n## Causa\nD.\n", 1)
    assert esn.texto_sem_notas("## Resumo\nA.\n") == ("## Resumo\nA.\n", 0)


def teste_sem_notas_na_biblioteca_de_producao_sobra_a_parte_escrita_a_mao():
    import biblioteca as bib
    import biblioteca_leitura as bl
    import evolucao_biblioteca as evo
    import experimento_sem_notas as esn
    fech = json.loads((bl.PASTA_BIBLIOTECA / "fechamento.json").read_text(encoding="utf-8"))
    destino = _temp() / "sem-notas"
    d = esn.montar_biblioteca(bl.PASTA_BIBLIOTECA, destino)
    producao = {v["id"]: v for v in bib.carregar(bl.PASTA_BIBLIOTECA)}
    aprendidos = sorted(vid for vid, v in producao.items() if v["pasta"] == evo.PASTA_APRENDIDOS)
    assert d["origem_hash"] == fech["hash"] == evo.hash_biblioteca(bl.PASTA_BIBLIOTECA), "a produção continua como foi fechada"
    assert d["verbetes_retirados"] == aprendidos and len(aprendidos) == fech["n_verbetes_novos"], d
    assert d["notas_retiradas"] == fech["n_notas"] + fech["n_retificacoes"] == sum(len(bib.notas(v)) for v in producao.values()), d
    assert d["verbetes"] == fech["n_verbetes"] - fech["n_verbetes_novos"], d
    copia = bib.carregar(destino)
    assert len(copia) == d["verbetes"]
    for v in copia:
        assert bib.notas(v) == [] and bib.render(v) == bib.render_base(producao[v["id"]]) and v["meta"] == producao[v["id"]]["meta"], v["id"]


def teste_sem_notas_ponte_da_versao_nome_da_pasta_e_regra_para_seguir():
    import experimento_sem_notas as esn
    # o nome segue o das quatro pontes já rodadas: a versão sem os pontos
    assert [esn.nome_da_ponte(v) for v in ("0.34.4", "0.40.2", "0.40.14", "0.40.15")] == ["fase3b_ponte_0344", "fase3b_ponte_0402", "fase3b_ponte_04014", "fase3b_ponte_04015"]
    assert esn.segue_depois_da_ponte({"versao": "0.40.15", "pareavel": True, "b": 1, "c": 0, "limite": 2}, parcial=False)[0] is True
    segue, motivo = esn.segue_depois_da_ponte({"versao": "9.9.9", "pareavel": False, "b": 2, "c": 2, "limite": 2}, parcial=False)
    assert segue is False and "9.9.9" in motivo and "b + c = 4" in motivo and "22 e 24" in motivo, motivo
    segue, motivo = esn.segue_depois_da_ponte(None, parcial=False)
    assert segue is False and "ponte" in motivo
    assert esn.segue_depois_da_ponte(None, parcial=True)[0] is True, "a fumaça de poucos casos segue sem ponte, como nos outros modos"
    assert esn.segue_depois_da_ponte({"versao": "9.9.9", "pareavel": False, "b": 2, "c": 2, "limite": 2}, parcial=True)[0] is True


def _reg_sem_notas(caso: str, causa: str, ids: list[str], sha: str, tokens: int = 1000, segundos: float = 60.0, notas: int = 0, versao: str = "0.40.15", bib_: str = "semnotas0001") -> dict:
    return {"caso": caso, "resposta": f"Curto.\nCAUSA_RAIZ: {causa}\nCAMPO: nenhum\nIMPACTO: O usuário não vê o dado.\nFONTE: nenhum", "verbetes_ids": ids, "contexto_sha256": sha,
            "tokens_entrada": tokens, "segundos": segundos, "notas_no_contexto": notas, "verbetes_novos_no_contexto": [], "biblioteca_versao": bib_, "versao_ollama": versao}


def _dados_do_resumo_sem_notas(ganhos: int = 0, perdas: int = 0) -> dict:
    """Seis casos (quatro de avaliação, dois inéditos) com um par de cada tipo, mais `ganhos` e `perdas` casos extras de avaliação para mover o teste pareado."""
    certo, errado, ined = "campo_ausente", "tipo_divergente", "corpo_vazio"
    abc, acb, abd = ["v-a", "v-b", "v-c"], ["v-a", "v-c", "v-b"], ["v-a", "v-b", "v-d"]
    casos = {"avaliacao": [{"id": f"a-{n}", "classe": "lexica", "nivel": 1, "gabarito": {"causa_raiz": certo}} for n in (1, 2, 3, 4)],
             "ineditos": [{"id": f"i-{n}", "classe": "runtime", "nivel": 2, "gabarito": {"causa_raiz": ined}} for n in (1, 2)]}
    novos = [_reg_sem_notas("a-1", certo, abc, "n1", tokens=900), _reg_sem_notas("a-2", certo, abd, "n2", tokens=900), _reg_sem_notas("a-3", errado, acb, "n3", tokens=900),
             _reg_sem_notas("a-4", errado, abc, "igual", tokens=900), _reg_sem_notas("i-1", ined, abc, "n5", tokens=900), _reg_sem_notas("i-2", ined, abc, "n6", tokens=900)]
    ref_a = [_reg_sem_notas("a-1", certo, abc, "r1", tokens=1100, notas=2, versao="0.40.14", bib_="producao0001"), _reg_sem_notas("a-2", errado, abc, "r2", tokens=1100, notas=1, versao="0.40.14", bib_="producao0001"),
             _reg_sem_notas("a-3", certo, abc, "r3", tokens=1100, notas=1, versao="0.40.14", bib_="producao0001"), _reg_sem_notas("a-4", errado, abc, "igual", tokens=1100, notas=0, versao="0.40.14", bib_="producao0001")]
    ref_i = [_reg_sem_notas("i-1", ined, abc, "r5", tokens=1100, notas=3, versao="0.40.14", bib_="producao0001"), _reg_sem_notas("i-2", errado, abc, "r6", tokens=1100, notas=3, versao="0.40.14", bib_="producao0001")]
    c16 = [_reg_sem_notas("a-1", certo, abc, "c1", versao="0.40.2", bib_="curada000001"), _reg_sem_notas("a-2", certo, abc, "c2", versao="0.40.2", bib_="curada000001"),
           _reg_sem_notas("a-3", certo, abc, "c3", versao="0.40.2", bib_="curada000001"), _reg_sem_notas("a-4", errado, abc, "c4", versao="0.40.2", bib_="curada000001"),
           _reg_sem_notas("fora-1", certo, abc, "c5", versao="0.40.2", bib_="curada000001")]
    for n in range(ganhos):
        casos["avaliacao"].append({"id": f"g-{n}", "classe": "lexica", "nivel": 1, "gabarito": {"causa_raiz": certo}})
        novos.append(_reg_sem_notas(f"g-{n}", certo, abc, f"ng{n}"))
        ref_a.append(_reg_sem_notas(f"g-{n}", errado, abc, f"rg{n}", versao="0.40.14", bib_="producao0001"))
    for n in range(perdas):
        casos["avaliacao"].append({"id": f"p-{n}", "classe": "lexica", "nivel": 1, "gabarito": {"causa_raiz": certo}})
        novos.append(_reg_sem_notas(f"p-{n}", errado, abc, f"np{n}"))
        ref_a.append(_reg_sem_notas(f"p-{n}", certo, abc, f"rp{n}", versao="0.40.14", bib_="producao0001"))
    linhas = [{"caso": r["caso"], "banco": "ineditos" if r["caso"].startswith("i-") else "avaliacao", "p_rotulo": 0.9, "selo": "medio"} for r in novos]
    referencias = {"avaliacao": {"corrida": "22", "registros": ref_a, "linhas": [{"caso": r["caso"], "p_rotulo": 0.8, "selo": "baixo"} for r in ref_a]},
                   "ineditos": {"corrida": "24", "registros": ref_i, "linhas": [{"caso": r["caso"], "p_rotulo": 0.8, "selo": "baixo"} for r in ref_i]}}
    condicoes = {"modo": "sem_notas", "parcial": False, "versao_ollama": "0.40.15", "k": 3, "casos": len(novos),
                 "biblioteca": {"hash": "semnotas0001", "origem_hash": "producao0001", "verbetes": 36, "verbetes_retirados": ["x", "y", "z"], "verbetes_com_notas": 20, "notas_retiradas": 26}}
    return {"registros": novos, "linhas": linhas, "casos_por_banco": casos, "referencias": referencias, "condicoes": condicoes, "corrida16": {"corrida": "16", "registros": c16},
            "ponte": {"versao": "0.40.15", "corrida": "fase3b_ponte_04015", "pareavel": True, "b": 1, "c": 0, "limite": 2, "n": 35}}


def teste_sem_notas_resume_os_pares_e_aplica_a_regra_fixada_antes_da_corrida():
    import avaliar
    import experimento_sem_notas as esn
    assert (esn.NOME, esn.PREFIXO, esn.ALFA) == ("sem_notas", "tb_f4_semnotas_", 0.05)
    x = _dados_do_resumo_sem_notas()
    d = esn.resumir(x["registros"], x["linhas"], x["casos_por_banco"], x["referencias"], x["condicoes"], ponte=x["ponte"], corrida16=x["corrida16"], corrida="x", gerado_em="2026-11-10T00:00:00")
    r = d["resumo"]
    assert (r["casos"], r["acertos_sem_notas"], r["acertos_referencia"], r["b"], r["c"], r["saldo"], r["mesmo_rotulo"]) == (6, 4, 3, 2, 1, 1, 3), r
    assert r["p"] == avaliar.mcnemar_exato(2, 1) and r["ganhos"] == ["a-2", "i-2"] and r["perdas"] == ["a-3"], r
    assert r["completo"] is True and r["sai_do_ruido"] is False and r["veredito"] == "dentro do ruído", r
    assert (r["tokens_entrada_mediana"], r["tokens_entrada_mediana_referencia"]) == (900, 1100), r
    assert d["regra"]["alfa"] == esn.ALFA and d["regra"]["pareavel"] is True and d["regra"]["ponte"]["corrida"] == "fase3b_ponte_04015" and "0,05" in d["regra"]["texto"], d["regra"]
    bancos = {b["banco"]: b for b in d["por_banco"]}
    assert (bancos["avaliacao"]["casos"], bancos["avaliacao"]["b"], bancos["avaliacao"]["c"], bancos["avaliacao"]["referencia"]) == (4, 1, 1, "corrida 22"), bancos["avaliacao"]
    assert (bancos["ineditos"]["acertos_sem_notas"], bancos["ineditos"]["acertos_referencia"], bancos["ineditos"]["referencia"]) == (2, 1, "corrida 24"), bancos["ineditos"]
    assert bancos["avaliacao"]["versao_ollama_referencia"] == "0.40.14" and bancos["avaliacao"]["biblioteca_referencia"] == "producao0001"
    mud = {m["mudanca"]: m for m in d["por_mudanca_do_contexto"]}
    assert {k: v["casos"] for k, v in mud.items()} == {"contexto idêntico": 1, "mesmos verbetes, sem as notas": 3, "mesmos verbetes, outra ordem": 1, "verbetes diferentes": 1}, mud
    assert (mud["verbetes diferentes"]["b"], mud["mesmos verbetes, outra ordem"]["c"], mud["contexto idêntico"]["mesmo_rotulo"]) == (1, 1, 1), mud
    c16 = d["contra_a_corrida_16"]
    assert (c16["casos"], c16["acertos_sem_notas"], c16["acertos_referencia"], c16["b"], c16["c"], c16["biblioteca"], c16["versao_ollama"]) == (4, 2, 3, 0, 1, "curada000001", "0.40.2"), c16
    caso = {c["caso"]: c for c in d["casos"]}
    assert (caso["a-2"]["mudou"], caso["a-3"]["mudou"], caso["a-1"]["mudou"]) == ("ganho", "perda", ""), caso
    assert caso["a-2"]["mudanca_do_contexto"] == "verbetes diferentes" and caso["a-2"]["verbetes_ids_referencia"] == ["v-a", "v-b", "v-c"] and caso["a-2"]["notas_no_contexto_referencia"] == 1
    assert (caso["a-1"]["p_rotulo"], caso["a-1"]["p_rotulo_referencia"], caso["a-1"]["selo"], caso["a-1"]["selo_referencia"], caso["a-1"]["banco"]) == (0.9, 0.8, "medio", "baixo", "avaliacao")
    assert [c["classe"] for c in d["por_classe"]] == ["lexica", "runtime"] and d["por_classe"][0]["acertos_sem_notas"] == 2 and d["por_classe"][0]["acertos_referencia"] == 2
    # a regra: com seis ganhos a mais (8 contra 1) a diferença sai do ruído a favor de tirar as notas; com nove perdas a mais (2 contra 10), a favor das notas
    for ganhos, perdas, esperado in ((6, 0, "sai do ruído, a favor de tirar as notas"), (0, 9, "sai do ruído, a favor das notas")):
        y = _dados_do_resumo_sem_notas(ganhos, perdas)
        r2 = esn.resumir(y["registros"], y["linhas"], y["casos_por_banco"], y["referencias"], y["condicoes"], ponte=y["ponte"], corrida="x")["resumo"]
        assert r2["p"] < esn.ALFA and r2["sai_do_ruido"] is True and r2["veredito"] == esperado, r2
    # sem ponte pareável, ou com a corrida incompleta, não há veredito
    sem_ponte = esn.resumir(x["registros"], x["linhas"], x["casos_por_banco"], x["referencias"], x["condicoes"], ponte=None, corrida="x")["resumo"]
    assert sem_ponte["sai_do_ruido"] is None and sem_ponte["veredito"].startswith("sem veredito") and "ponte" in sem_ponte["veredito"], sem_ponte
    nao_pareavel = esn.resumir(x["registros"], x["linhas"], x["casos_por_banco"], x["referencias"], x["condicoes"], ponte={**x["ponte"], "pareavel": False, "b": 3, "c": 1}, corrida="x")["resumo"]
    assert nao_pareavel["sai_do_ruido"] is None and "não é pareável" in nao_pareavel["veredito"], nao_pareavel
    incompleta = esn.resumir(x["registros"][:-1], x["linhas"][:-1], x["casos_por_banco"], x["referencias"], x["condicoes"], ponte=x["ponte"], corrida="x")["resumo"]
    assert incompleta["completo"] is False and incompleta["sai_do_ruido"] is None and "não cobriu" in incompleta["veredito"] and incompleta["casos"] == 5, incompleta
    # a mesma versão do Ollama das referências não pede ponte
    mesma = {**x["condicoes"], "versao_ollama": "0.40.14"}
    assert esn.resumir(x["registros"], x["linhas"], x["casos_por_banco"], x["referencias"], mesma, ponte=None, corrida="x")["resumo"]["sai_do_ruido"] is False


def teste_sem_notas_render_traz_os_blocos_a_regra_e_o_veredito():
    import experimento_sem_notas as esn
    x = _dados_do_resumo_sem_notas()
    d = esn.resumir(x["registros"], x["linhas"], x["casos_por_banco"], x["referencias"], x["condicoes"], ponte=x["ponte"], corrida16=x["corrida16"], corrida="fase4_sem_notas", gerado_em="2026-11-10T00:00:00")
    md = esn.render(d)
    for bloco in ("resumo", "banco", "mudanca", "corrida16", "classe", "casos"):
        assert f"<!-- tabela:{esn.PREFIXO}{bloco} -->" in md and f"<!-- /tabela:{esn.PREFIXO}{bloco} -->" in md, bloco
    for trecho in ("corrida 25", "decisão 116", "0,05", "dentro do ruído", "corrida 22", "corrida 24", "corrida 16", "`a-2`", "ganho", "perda", "26 notas"):
        assert trecho in md, trecho
    assert md.splitlines()[2].startswith("# ") and "gerada em 2026-11-10" in md.splitlines()[2]
    assert "—" not in md and "→" not in md, "sem travessão nem seta no texto gerado"
    sem16 = esn.render(esn.resumir(x["registros"], x["linhas"], x["casos_por_banco"], x["referencias"], x["condicoes"], ponte=x["ponte"], corrida="x", gerado_em="2026-11-10T00:00:00"))
    assert f"<!-- tabela:{esn.PREFIXO}corrida16 -->" in sem16, "sem os registros da corrida 16 o bloco sai com a linha que diz isso"


def teste_sem_notas_previa_dos_72_contextos_esta_gravada_e_bate_com_a_regeracao():
    import experimento_sem_notas as esn
    d = esn.previa()
    assert [b["banco"] for b in d["por_banco"]] == ["avaliacao", "ineditos"] and all(b["casos"] == 36 for b in d["por_banco"]), d["por_banco"]
    for b in d["por_banco"]:
        assert b["contexto_da_referencia_refeito_igual"] == b["casos"], "a biblioteca de produção de hoje refaz o contexto que a corrida de referência gravou"
        assert sum(m["casos"] for m in b["mudancas"]) == b["casos"] and sum(v["casos"] for v in b["verbete_certo"]) == b["casos"], b
    bibl = d["biblioteca"]
    assert bibl["verbetes_producao"] - bibl["verbetes_sem_notas"] == len(bibl["verbetes_retirados"]) and bibl["notas_retiradas"] > 0, bibl
    assert d["resumo"]["casos"] == 72 and d["resumo"]["contextos_que_mudam"] + d["resumo"]["contextos_identicos"] == 72, d["resumo"]
    # os acertos das referências, lidos dos registros, são os das leituras oficiais das corridas 22 e 24
    oficiais = [json.loads((RA / "fase4" / nome).read_text(encoding="utf-8"))["resumo"]["acertos"] for nome in ("trilha.json", "ineditos.json")]
    assert [b["acertos_referencia"] for b in d["por_banco"]] == oficiais and d["resumo"]["acertos_referencia"] == sum(oficiais), (d["por_banco"], oficiais)
    md = esn.render_previa(d)
    assert f"<!-- tabela:{esn.PREFIXO}previa_banco -->" in md and "—" not in md and "→" not in md
    pasta = RA / "fase4"
    assert (pasta / "sem_notas_previa.json").exists() and (pasta / "sem_notas_previa.md").exists(), "rode python experimento_sem_notas.py --previa"
    assert esn.main(["--previa", "--check"]) == 0


# ------------------------------------------------------------------ corrida 26: o segundo passe do diagnóstico (ficha 66, decisão 120)

# ! Alteração de IA - Revisar: (10/11/2026, ficha 66 opção b, decisão 120) testes da corrida 26 (`experimento_segundo_passe.py`), escritos ANTES do módulo: a primeira
# rodada falha por ModuleNotFoundError em `experimento_segundo_passe`, o RED aceito para módulo novo. Conferem: os casos com sinal lidos das corridas 22 e 24 (os 24 da
# conta sem modelo de `medidas_do_repositorio.json`, na ordem da corrida); o segundo pedido com os três verbetes seguintes da mesma busca (posições 4 a 6) no prompt
# congelado, sem os três primeiros e sem a primeira resposta; a regra de escolha entre as duas respostas, caso a caso; o resumo com o que o segundo passe sozinho
# consertaria e estragaria, o que a regra troca, a conta por sinal, por banco e pelo alcance do verbete da causa certa, e o veredito pela regra fixada antes; os blocos
# do Markdown; e a prévia sem modelo gravada, com `--check`.
# ! Motivo: a corrida roda na janela do Eric e custa máquina; a regra de escolha e a do veredito têm de estar escritas e testadas antes, para o resultado não escolher a
# régua, e o segundo pedido não pode repetir o contexto do primeiro nem falar da primeira resposta, que é o desenho que a pesquisa da ficha 64 diz que troca resposta
# certa por errada (levantamento §6.16.4). Os números de controle vêm do arquivo de medidas da pesquisa, e não de constantes escritas aqui.
_MEDIDAS_DO_FLUXO = RAIZ / "Documentacao" / "memorial" / "5-metodo-e-ferramental" / "dados" / "pesquisa-fluxo-do-agente" / "medidas_do_repositorio.json"


def teste_segundo_passe_os_casos_com_sinal_sao_os_24_da_conta_sem_modelo():
    import corridas_em_texto as ct
    import experimento_segundo_passe as sp
    assert (sp.CORRIDA, sp.NOME, sp.PREFIXO, sp.ALFA, sp.VERBETES_SEGUINTES) == (26, "segundo_passe", "tb_f4_segpasse_", 0.05, 3)
    primeiras = sp.primeiras_respostas()
    assert {b: (x["corrida"], len(x["casos"])) for b, x in primeiras.items()} == {"avaliacao": ("22", 36), "ineditos": ("24", 36)}, {b: len(x["casos"]) for b, x in primeiras.items()}
    um = primeiras["avaliacao"]["casos"]["lex-4"]
    assert set(um["sinais"]) == {"selo_baixo", "fonte_divergente"} and um["registro"]["caso"] == "lex-4" and "p_rotulo" in um["linha"], um
    itens = sp.casos_com_sinal()
    medidas = json.loads(_MEDIDAS_DO_FLUXO.read_text(encoding="utf-8"))["ideia_2"]["os_72_casos"]
    assert len(itens) == medidas["disparos"], (len(itens), medidas["disparos"])
    assert [b for b, _, _ in itens] == sorted((b for b, _, _ in itens), key=sp.BANCOS.index), "os oficiais primeiro, depois os inéditos"
    assert all(p["sinais"]["selo_baixo"] or p["sinais"]["fonte_divergente"] for _, _, p in itens), "só entra caso com um sinal aceso"
    erros = sum(1 for _, c, p in itens if ct.rotulo_lido(p["registro"]["resposta"]) != c["gabarito"]["causa_raiz"])
    assert (erros, len(itens) - erros) == (medidas["erros_pegos"], medidas["acertos_incomodados"]), erros
    assert sum(1 for _, _, p in itens if p["sinais"]["fonte_divergente"]) == medidas["disparos_da_fonte_divergente"]
    assert [b for b, _, _ in sp.casos_com_sinal(1)] == ["avaliacao", "ineditos"], "a fumaça pega os N primeiros casos com sinal de cada banco"
    grupos = [sp.grupo_do_sinal(s) for s in ({"selo_baixo": True, "fonte_divergente": False}, {"selo_baixo": False, "fonte_divergente": True}, {"selo_baixo": True, "fonte_divergente": True})]
    assert tuple(grupos) == sp.GRUPOS_DE_SINAL and sp.grupo_do_sinal({"selo_baixo": False, "fonte_divergente": False}) is None


def teste_segundo_passe_o_pedido_leva_os_tres_verbetes_seguintes_da_mesma_busca_no_prompt_congelado():
    import diagnostico_ao_vivo as dv
    import estrategias
    import executar_fase4 as ex
    import experimento_segundo_passe as sp
    import recuperacao as rec
    verbetes = bib.carregar(dv.PASTA_CURADA)
    indice = rec.Indice(verbetes)
    _, caso, primeira = sp.casos_com_sinal()[0]
    caso_f = ex.fixture_sem_gabarito(caso)
    assert "gabarito" not in caso_f, "o gabarito não entra no pedido"
    ordem = [v["id"] for _, v in rec.pontuar(indice, dv.caso_da_busca(caso_f))]
    gravados = list(primeira["registro"]["verbetes_ids"])
    assert ordem[:3] == gravados, "a busca de agora devolve os três verbetes que a corrida de referência gravou"
    prox = sp.seguintes(indice, caso_f, gravados)
    assert [v["id"] for v in prox] == ordem[3:6] and not set(gravados) & {v["id"] for v in prox}
    assert [v["id"] for v in sp.seguintes(indice, caso_f, gravados, 2)] == ordem[3:5]
    ctx, prompt = sp.prompt_do_segundo_passe(verbetes, indice, caso_f, prox)
    assert ctx["verbetes_ids"] == ordem[3:6], ctx["verbetes_ids"]
    assert prompt == estrategias.linear_com_biblioteca(caso_f, rec._envelope(prox)), "o segundo pedido é o prompt congelado do diagnóstico, só com outros verbetes"
    ctx1, prompt1 = dv.montar_prompt(verbetes, indice, caso_f, 3)
    assert dv.hash_prompt_fixo(verbetes, ctx, caso_f, prompt) == dv.hash_prompt_fixo(verbetes, ctx1, caso_f, prompt1), "a parte fixa do prompt é a do primeiro pedido"
    for v in verbetes:
        if v["id"] in gravados:
            assert bib.render(v) not in prompt, f"o verbete {v['id']} do primeiro pedido não volta no segundo"
    assert primeira["registro"]["resposta"].strip() not in prompt and "primeira resposta" not in prompt.lower(), "o segundo pedido não fala da primeira resposta"
    try:
        sp.seguintes(indice, caso_f, ["outro-verbete", *gravados[1:]])
    except SystemExit as e:
        assert "mesma busca" in str(e), e
    else:
        raise AssertionError("a busca que não devolve os três verbetes gravados tinha de parar a corrida")


def teste_segundo_passe_regra_de_escolha_fica_a_primeira_salvo_segunda_sem_sinal_e_mais_provavel():
    import experimento_segundo_passe as sp
    primeira = {"rotulo": "campo_ausente", "p_rotulo": 0.62, "selo_baixo": True, "fonte_divergente": False}

    def segunda(**troca) -> dict:
        return {"rotulo": "tipo_divergente", "p_rotulo": 0.95, "selo_baixo": False, "fonte_divergente": False, **troca}

    troca = sp.escolher(primeira, segunda())
    assert troca == {"fica": "segunda", "motivo": sp.MOTIVOS[-1]}, troca
    for seg, trecho in ((segunda(rotulo="campo_ausente"), "mesma causa"), (segunda(rotulo=None, p_rotulo=None, selo_baixo=True), "não traz uma causa da lista"),
                        (segunda(rotulo="causa_inventada"), "não traz uma causa da lista"), (segunda(p_rotulo=0.80, selo_baixo=True), "selo baixo"),
                        (segunda(fonte_divergente=True), "FONTE divergente"), (segunda(p_rotulo=0.62), "não passa a da primeira"), (segunda(p_rotulo=0.50), "não passa a da primeira")):
        e = sp.escolher(primeira, seg)
        assert e["fica"] == "primeira" and trecho in e["motivo"] and e["motivo"] in sp.MOTIVOS, (seg, e)
    # a primeira confiante só com a FONTE divergente: uma segunda menos provável não troca
    confiante = {"rotulo": "codificacao_incorreta", "p_rotulo": 0.999, "selo_baixo": False, "fonte_divergente": True}
    assert sp.escolher(confiante, segunda(p_rotulo=0.99))["fica"] == "primeira"
    # a primeira sem causa lida não tem probabilidade: uma segunda sem sinal aceso troca
    sem_causa = {"rotulo": None, "p_rotulo": None, "selo_baixo": True, "fonte_divergente": False}
    assert sp.escolher(sem_causa, segunda())["fica"] == "segunda"
    assert len(sp.MOTIVOS) == 6 and len(set(sp.MOTIVOS)) == 6
    regra = sp.texto_da_regra()
    for trecho in ("decisão 120", "0,05", "selo baixo", "FONTE", "probabilidade maior", "fica a primeira", "ponte", "outra decisão"):
        assert trecho in regra, trecho
    assert "—" not in regra and "→" not in regra


def _resposta_sp(causa: str | None) -> str:
    return "Curto.\n" + (f"CAUSA_RAIZ: {causa}\n" if causa else "") + "CAMPO: nenhum\nIMPACTO: O usuário não vê o dado.\nFONTE: nenhum"


def _dados_do_segundo_passe(ganhos: int = 0, perdas: int = 0) -> dict:
    """Sete casos em dois bancos, cinco com sinal: um conserto que a regra aceita (a-2), um acerto que a regra estraga (a-3), um acerto que o segundo passe estragaria e
    a regra protege (a-4), um erro que continua com a mesma causa (a-5) e um conserto que a regra recusa pelo selo baixo (i-2); `ganhos` e `perdas` acrescentam casos
    iguais ao a-2 e ao a-3 para mover o teste pareado."""
    certo, errado, ined = "campo_ausente", "tipo_divergente", "corpo_vazio"
    sem_o_certo, com_o_certo, seguintes_sem, seguintes_com = ["v-a", "v-b", "v-c"], [certo, "v-b", "v-c"], ["v-d", "v-e", "v-f"], [certo, "v-e", "v-f"]
    casos = {"avaliacao": [], "ineditos": []}
    primeiras = {"avaliacao": {"corrida": "22", "casos": {}}, "ineditos": {"corrida": "24", "casos": {}}}
    registros, linhas = [], []

    def caso(cid: str, banco: str, gabarito: str, primeira: tuple, segunda: tuple | None) -> None:
        rot1, p1, ids1, selo_baixo, fonte = primeira
        casos[banco].append({"id": cid, "classe": "lexica" if banco == "avaliacao" else "runtime", "nivel": 1, "gabarito": {"causa_raiz": gabarito}})
        primeiras[banco]["casos"][cid] = {"registro": {"caso": cid, "resposta": _resposta_sp(rot1), "verbetes_ids": ids1, "tokens_entrada": 1100, "segundos": 60.0, "versao_ollama": "0.40.14",
                                                         "biblioteca_versao": "producao0001"},
                                          "linha": {"caso": cid, "p_rotulo": p1, "selo": "baixo" if selo_baixo else "alto"}, "sinais": {"selo_baixo": selo_baixo, "fonte_divergente": fonte}}
        if segunda is None:
            return
        rot2, p2, ids2, selo_baixo2, fonte2, tokens = segunda
        registros.append({"caso": cid, "resposta": _resposta_sp(rot2), "verbetes_ids": ids2, "tokens_entrada": tokens, "segundos": 70.0, "versao_ollama": "0.40.15", "biblioteca_versao": "producao0001"})
        linhas.append({"caso": cid, "banco": banco, "p_rotulo": p2, "selo": "baixo" if selo_baixo2 else "medio", "selo_baixo": selo_baixo2, "fonte_divergente": fonte2, "posicoes": [4, 5, 6]})

    caso("a-1", "avaliacao", certo, (certo, 0.99, com_o_certo, False, False), None)
    caso("a-2", "avaliacao", certo, (errado, 0.60, sem_o_certo, True, False), (certo, 0.95, seguintes_com, False, False, 1500))
    caso("a-3", "avaliacao", certo, (certo, 0.70, com_o_certo, True, False), (errado, 0.90, seguintes_sem, False, False, 1300))
    caso("a-4", "avaliacao", certo, (certo, 0.999, sem_o_certo, False, True), (errado, 0.95, seguintes_sem, False, False, 1300))
    caso("a-5", "avaliacao", certo, (errado, 0.50, sem_o_certo, True, True), (errado, 0.97, seguintes_sem, False, False, 1300))
    caso("i-1", "ineditos", ined, (errado, 0.99, sem_o_certo, False, False), None)
    caso("i-2", "ineditos", ined, (errado, 0.40, sem_o_certo, True, False), (ined, 0.70, seguintes_sem, True, False, 1300))
    for n in range(ganhos):
        caso(f"g-{n}", "avaliacao", certo, (errado, 0.60, sem_o_certo, True, False), (certo, 0.95, seguintes_com, False, False, 1300))
    for n in range(perdas):
        caso(f"p-{n}", "avaliacao", certo, (certo, 0.70, com_o_certo, True, False), (errado, 0.90, seguintes_sem, False, False, 1300))
    condicoes = {"modo": "segundo_passe", "parcial": False, "versao_ollama": "0.40.15", "verbetes_seguintes": 3, "posicoes": [4, 5, 6], "limite_de_tokens": 1409,
                 "biblioteca": {"hash": "producao0001"}}
    return {"registros": registros, "linhas": linhas, "casos_por_banco": casos, "primeiras": primeiras, "condicoes": condicoes,
            "ponte": {"versao": "0.40.15", "corrida": "fase3b_ponte_04015", "pareavel": True, "b": 1, "c": 0, "limite": 2, "n": 35}}


def _resumo_sp(x: dict, **troca) -> dict:
    import experimento_segundo_passe as sp
    args = {"ponte": x["ponte"], "corrida": "x", "gerado_em": "2026-11-10T00:00:00", **troca}
    return sp.resumir(x["registros"], x["linhas"], x["casos_por_banco"], x["primeiras"], x["condicoes"], **args)


def teste_segundo_passe_resume_o_que_conserta_o_que_estraga_e_aplica_a_regra_fixada_antes():
    import avaliar
    import experimento_segundo_passe as sp
    x = _dados_do_segundo_passe()
    d = _resumo_sp(x)
    r = d["resumo"]
    assert (r["casos"], r["com_sinal"], r["segundos_passes"], r["acertos_primeira"]) == (7, 5, 5, 3), r
    assert (r["erros_primeira_com_sinal"], r["acertos_primeira_com_sinal"]) == (3, 2), r
    # o segundo passe sozinho: o que ele consertaria e o que estragaria se a segunda resposta valesse sempre
    assert (r["consertaria"], r["estragaria"], r["mesmo_rotulo"], r["acertos_segunda"]) == (2, 2, 1, 2), r
    # a regra fixada antes: duas trocas, um ganho e uma perda
    assert (r["trocas"], r["b"], r["c"], r["saldo"], r["acertos_final"]) == (2, 1, 1, 0, 3), r
    assert r["p"] == avaliar.mcnemar_exato(1, 1) and r["ganhos"] == ["a-2"] and r["perdas"] == ["a-3"], r
    assert r["completo"] is True and r["sai_do_ruido"] is False and r["veredito"] == "dentro do ruído", r
    assert (r["tokens_entrada_mediana"], r["tokens_entrada_mediana_primeira"], r["acima_do_limite"], r["limite_de_tokens"]) == (1300, 1100, 1, 1409), r
    assert d["regra"]["alfa"] == sp.ALFA and d["regra"]["pareavel"] is True and d["regra"]["texto"] == sp.texto_da_regra(), d["regra"]
    sinais = {s["sinal"]: s for s in d["por_sinal"]}
    assert list(sinais) == list(sp.GRUPOS_DE_SINAL)
    so_selo, so_fonte, os_dois = (sinais[g] for g in sp.GRUPOS_DE_SINAL)
    assert (so_selo["casos"], so_selo["erros_primeira"], so_selo["consertaria"], so_selo["estragaria"], so_selo["trocas"], so_selo["b"], so_selo["c"]) == (3, 2, 2, 1, 2, 1, 1), so_selo
    assert (so_fonte["casos"], so_fonte["estragaria"], so_fonte["trocas"], so_fonte["c"]) == (1, 1, 0, 0), so_fonte
    assert (os_dois["casos"], os_dois["mesmo_rotulo"], os_dois["consertaria"]) == (1, 1, 0), os_dois
    bancos = {b["banco"]: b for b in d["por_banco"]}
    assert (bancos["avaliacao"]["casos"], bancos["avaliacao"]["com_sinal"], bancos["avaliacao"]["b"], bancos["avaliacao"]["c"], bancos["avaliacao"]["referencia"]) == (5, 4, 1, 1, "corrida 22"), bancos
    assert (bancos["ineditos"]["casos"], bancos["ineditos"]["com_sinal"], bancos["ineditos"]["consertaria"], bancos["ineditos"]["trocas"]) == (2, 1, 1, 0), bancos
    alcance = {a["alcance"]: a for a in d["por_alcance"]}
    assert list(alcance) == list(sp.ALCANCES) and [alcance[a]["casos"] for a in sp.ALCANCES] == [1, 1, 3], alcance
    assert alcance[sp.ALCANCES[1]]["consertaria"] == 1 and alcance[sp.ALCANCES[0]]["estragaria"] == 1, alcance
    regras = {x_["regra"]: x_ for x_ in d["por_regra"]}
    assert [(x_["b"], x_["c"], x_["acertos"]) for x_ in d["por_regra"]] == [(0, 0, 3), (2, 2, 3), (2, 1, 4), (1, 1, 3)], d["por_regra"]
    assert next(iter(regras)).startswith("sempre a primeira") and list(regras)[-1].startswith("a regra fixada antes"), list(regras)
    motivos = {m["motivo"]: m["casos"] for m in d["motivos"]}
    assert motivos == {sp.MOTIVOS[0]: 0, sp.MOTIVOS[1]: 1, sp.MOTIVOS[2]: 1, sp.MOTIVOS[3]: 0, sp.MOTIVOS[4]: 1, sp.MOTIVOS[5]: 2}, motivos
    caso = {c["caso"]: c for c in d["casos"]}
    assert sorted(caso) == ["a-2", "a-3", "a-4", "a-5", "i-2"], "só os casos com segundo passe entram na lista"
    assert (caso["a-2"]["fica"], caso["a-2"]["mudou"], caso["a-2"]["efeito_da_segunda"], caso["a-2"]["alcance"], caso["a-2"]["sinal"]) == ("segunda", "ganho", "consertaria", sp.ALCANCES[1], sp.GRUPOS_DE_SINAL[0])
    assert (caso["a-3"]["fica"], caso["a-3"]["mudou"], caso["a-3"]["efeito_da_segunda"], caso["a-3"]["alcance"]) == ("segunda", "perda", "estragaria", sp.ALCANCES[0])
    assert (caso["a-4"]["fica"], caso["a-4"]["mudou"], caso["a-4"]["efeito_da_segunda"], caso["a-4"]["rotulo_final"]) == ("primeira", "", "estragaria", "campo_ausente")
    assert (caso["a-5"]["efeito_da_segunda"], caso["i-2"]["efeito_da_segunda"], caso["i-2"]["fica"], caso["i-2"]["acerto_final"]) == ("continua errado", "consertaria", "primeira", False)
    assert (caso["a-2"]["p_primeira"], caso["a-2"]["p_segunda"], caso["a-2"]["verbetes_segunda"], caso["a-2"]["tokens_entrada"]) == (0.60, 0.95, ["campo_ausente", "v-e", "v-f"], 1500)
    # a regra do veredito: oito ganhos contra uma perda saem do ruído a favor do segundo passe; um ganho contra dez perdas, contra ele
    for ganhos, perdas, esperado in ((7, 0, "sai do ruído, a favor do segundo passe"), (0, 9, "sai do ruído, contra o segundo passe")):
        r2 = _resumo_sp(_dados_do_segundo_passe(ganhos, perdas))["resumo"]
        assert r2["p"] < sp.ALFA and r2["sai_do_ruido"] is True and r2["veredito"] == esperado, r2
    # sem ponte pareável, ou com a corrida incompleta, não há veredito
    sem_ponte = _resumo_sp(x, ponte=None)["resumo"]
    assert sem_ponte["sai_do_ruido"] is None and sem_ponte["veredito"].startswith("sem veredito") and "ponte" in sem_ponte["veredito"], sem_ponte
    nao_pareavel = _resumo_sp(x, ponte={**x["ponte"], "pareavel": False, "b": 3, "c": 1})["resumo"]
    assert nao_pareavel["sai_do_ruido"] is None and "não é pareável" in nao_pareavel["veredito"], nao_pareavel
    incompleta = sp.resumir(x["registros"][:-1], x["linhas"][:-1], x["casos_por_banco"], x["primeiras"], x["condicoes"], ponte=x["ponte"], corrida="x")["resumo"]
    assert incompleta["completo"] is False and incompleta["sai_do_ruido"] is None and "não cobriu" in incompleta["veredito"] and incompleta["segundos_passes"] == 4, incompleta
    # a mesma versão do Ollama das corridas de referência não pede ponte
    mesma = {**x, "condicoes": {**x["condicoes"], "versao_ollama": "0.40.14"}}
    assert _resumo_sp(mesma, ponte=None)["resumo"]["sai_do_ruido"] is False


def teste_segundo_passe_render_traz_os_blocos_a_regra_e_o_veredito():
    import experimento_segundo_passe as sp
    d = _resumo_sp(_dados_do_segundo_passe(), corrida="fase4_segundo_passe")
    md = sp.render(d)
    for bloco in ("resumo", "sinal", "banco", "alcance", "regras", "motivos", "casos"):
        assert f"<!-- tabela:{sp.PREFIXO}{bloco} -->" in md and f"<!-- /tabela:{sp.PREFIXO}{bloco} -->" in md, bloco
    for trecho in ("corrida 26", "decisão 120", "0,05", "dentro do ruído", "corrida 22", "corrida 24", "`a-2`", "ganho", "perda", "consertaria", "estragaria", "posições 4 a 6", "1409"):
        assert trecho in md, trecho
    assert md.splitlines()[2].startswith("# ") and "gerada em 2026-11-10" in md.splitlines()[2]
    assert "—" not in md and "→" not in md, "sem travessão nem seta no texto gerado"


def teste_segundo_passe_previa_esta_gravada_e_bate_com_a_regeracao():
    import avaliar
    import experimento_segundo_passe as sp
    d = sp.previa()
    r, medidas = d["resumo"], json.loads(_MEDIDAS_DO_FLUXO.read_text(encoding="utf-8"))["ideia_2"]["os_72_casos"]
    assert (r["casos"], r["com_sinal"], r["erros_com_sinal"], r["acertos_com_sinal"]) == (medidas["casos"], medidas["disparos"], medidas["erros_pegos"], medidas["acertos_incomodados"]), r
    assert r["so_selo_baixo"] + r["so_fonte_divergente"] + r["os_dois_sinais"] == r["com_sinal"] and r["busca_refeita_igual"] == r["com_sinal"], r
    assert r["erros_com_sinal"] == r["erros_ao_alcance"] + r["erros_com_o_verbete_certo_ja_entregue"] + r["erros_fora_do_alcance"], r
    teto = {t["verbetes"]: t["erros_ao_alcance"] for t in medidas["teto_de_um_segundo_passe"]}
    assert teto[5] <= r["erros_ao_alcance"] <= teto[10], "as posições 4 a 6 alcançam pelo menos o que as posições 4 e 5 alcançam, e no máximo o que as posições 4 a 10 alcançam"
    # o que a corrida consegue enxergar: nem no melhor cenário o teste pareado passa do corte
    assert r["p_do_melhor_cenario"] == avaliar.mcnemar_exato(r["erros_ao_alcance"], 0) and r["p_do_melhor_cenario"] >= sp.ALFA, r
    assert r["consertos_para_sair_do_ruido"] == 6 and r["erros_ao_alcance"] < r["consertos_para_sair_do_ruido"], r
    assert r["inferencias"] == r["com_sinal"] and r["minutos_estimados"] > 0, r
    desenho = d["desenho"]
    limite = json.loads((RA / "fase4" / "prompt_tela_blocos.json").read_text(encoding="utf-8"))["limite"]["tokens"]
    assert (desenho["verbetes_seguintes"], desenho["posicoes"], desenho["k_do_primeiro_pedido"], desenho["limite_de_tokens"]) == (3, [4, 5, 6], 3, limite), desenho
    assert sum(1 for a in d["alternativas"] if a["escolhido"]) == 1 and len(d["alternativas"]) >= 4, d["alternativas"]
    escolhida = next(a for a in d["alternativas"] if a["escolhido"])
    assert (escolhida["erros_ao_alcance"], escolhida["acima_do_limite"], escolhida["tokens_estimados_mediana"]) == (r["erros_ao_alcance"], r["acima_do_limite"], r["tokens_estimados_mediana"]), escolhida
    assert len(d["casos"]) == r["com_sinal"] and all(len(c["seguintes"]) == 3 and c["posicoes"] == [4, 5, 6] for c in d["casos"])
    assert sum(g["casos"] for g in d["por_sinal"]) == r["com_sinal"] and [b["banco"] for b in d["por_banco"]] == ["avaliacao", "ineditos"]
    assert d["regra"] == sp.texto_da_regra()
    md = sp.render_previa(d)
    for bloco in ("previa_resumo", "previa_sinal", "previa_alternativas", "previa_casos"):
        assert f"<!-- tabela:{sp.PREFIXO}{bloco} -->" in md, bloco
    assert "—" not in md and "→" not in md
    pasta = RA / "fase4"
    assert (pasta / "segundo_passe_previa.json").exists() and (pasta / "segundo_passe_previa.md").exists(), "rode python experimento_segundo_passe.py --previa"
    assert sp.main(["--previa", "--check"]) == 0


# ------------------------------------------------------------------ medida M1: os portões 3, 4 e 5 nas propostas da corrida 20 (ficha 67, decisão 121)

# ! Alteração de IA - Revisar: (10/11/2026, ficha 67 opção b, decisão 121) testes dos portões por edição da proposta do analista de documentação (`portoes_de_edicao.py`)
# e da medida M1, escritos ANTES do módulo: a primeira rodada falha por ModuleNotFoundError em `portoes_de_edicao`, o RED aceito para módulo novo. Conferem: o portão 3
# (a forma de instrução) em frases reais da corrida 20 e em afirmações, e que ele pega pelo menos o que a contagem publicada da pesquisa pegava; o portão 4 (os filtros de
# texto do pacote Q2) com um texto bom e um reprovado; o portão 5 (a busca refeita com a edição aplicada numa cópia) nas 20 edições do lote da corrida 20, contra os
# números da medida da pesquisa, sem tocar na biblioteca de base, e a regra do sinal de busca (o caso de origem tem de passar a receber o verbete); a medida M1 inteira
# (as 92 propostas, as 20 revisadas, cada portão contra o veredito da revisão humana e os portões em sequência); e o documento derivado gravado, com `--check`.
# ! Motivo: a M1 é a única das medidas da proposta que não gasta modelo e sai nesta sessão; os portões são os mesmos que a corrida 27 aplica às propostas novas, então um
# erro aqui contaminaria as duas. Os números de controle vêm do arquivo de medidas da pesquisa e de `biblioteca.json`, e não de constantes escritas aqui.
def teste_portao_da_forma_recusa_verbo_de_edicao_e_deixa_passar_a_afirmacao():
    import experimento_sem_notas as esn
    import portoes_de_edicao as pe
    recusadas = ("Adicionar nota sobre a necessidade de verificar se a resposta é um objeto ou uma coleção.", "Adicione um exemplo de sintoma para clarificar o caso.",
                 "Corrigir a junção entre tbprodutos e tbtipos, garantindo que id_tipo_produto esteja correto.", "Retificar a informação sobre a validação do status do pedido na API.",
                 "Adicionado sintomas para campos ausentes em objetos JSON.", "Adiciona que a defasagem pode ser causada por cache do navegador.",
                 "Cria um verbete dedicado para a resposta truncada correta.", "\"Corrigir a afirmação para: 'Contrato mudou no servidor sem atualizar o cliente.'\"",
                 "Retificação: onde diz \"Fora dele\", leia: limite num proxy.", "Notar que o contrato especifica a estrutura do JSON esperado.", "Incluir o total na resposta da API.",
                 "Nota: o contrato não aborda o truncamento.", "Verifique o Content-Length para evitar esse problema.")
    passam = ("O cancelamento depende de um redirect, o que pode causar divergência na interface.", "Um campo preço ausente na resposta da API resulta em botões sem informações relevantes.",
              "Ocorre quando o corpo da resposta JSON é cortado antes de ser completamente enviado.", "A rota GET /api/produtos devolve a lista inteira, sem o total.",
              "Registros duplicados aparecem quando o POST /api/pedidos é repetido sem chave de idempotência.", "Notas antigas do verbete continuam valendo.",
              "Detalhe do pedido vem sem o campo status quando a consulta falha.")
    for texto in recusadas:
        r = pe.portao_da_forma(texto)
        assert r["passa"] is False and r["motivo"] and r["primeira_palavra"], (texto, r)
    for texto in passam:
        r = pe.portao_da_forma(texto)
        assert r["passa"] is True and r["motivo"] is None, (texto, r)
    assert pe.portao_da_forma("")["passa"] is False and pe.portao_da_forma("   ")["passa"] is False, "texto vazio não é afirmação"
    # o portão pega pelo menos o que a contagem publicada da pesquisa pegava (os cinco radicais de experimento_sem_notas.VERBOS_DE_INSTRUCAO)
    propostas = pe.propostas_da_corrida_20()
    pela_pesquisa = [p for p in propostas if p["texto"].strip().startswith(esn.VERBOS_DE_INSTRUCAO)]
    medidas = json.loads(_MEDIDAS_DO_FLUXO.read_text(encoding="utf-8"))["ideia_3"]["forma_de_instrucao"]
    assert (len(propostas), len(pela_pesquisa)) == (medidas["propostas"], medidas["em_forma_de_instrucao"]), (len(propostas), len(pela_pesquisa))
    assert all(pe.portao_da_forma(p["texto"])["passa"] is False for p in pela_pesquisa), "toda proposta que a pesquisa contou como instrução é recusada pelo portão"


def teste_portao_do_texto_aplica_os_filtros_do_pacote_q2():
    import filtros_de_texto as ft
    import portoes_de_edicao as pe
    limiares = ft.carregar_limiares()
    bom = pe.portao_do_texto("A rota de detalhe do produto devolve um objeto com sete campos. A lista devolve os mesmos campos em cada item.", limiares)
    assert bom["passa"] is True and bom["reprovados"] == [], bom
    medidas = ft.medir("O prefill do modelo usa o hit@3 da busca.")
    assert medidas["termos_sem_expansao_n"] > 0, "controle: o texto de teste tem termo da lista fechada sem a explicação"
    ruim = pe.portao_do_texto("O prefill do modelo usa o hit@3 da busca.", limiares)
    assert ruim["passa"] is False and "termos_sem_expansao_n" in ruim["reprovados"] and ruim["termos_sem_expansao"], ruim
    assert pe.portao_do_texto("A rota devolve um objeto.")["passa"] is True, "sem limiares passados, o portão lê limiares_texto.json"


def teste_portao_da_busca_refaz_a_busca_com_a_edicao_aplicada_numa_copia():
    import evolucao_biblioteca as evo
    import portoes_de_edicao as pe
    base = pe.base_da_corrida_20()
    hash_antes = evo.hash_biblioteca(base)
    busca = pe.BuscaDosCasos(base)
    medidas = json.loads(_MEDIDAS_DO_FLUXO.read_text(encoding="utf-8"))["ideia_3"]["portao_da_busca_no_lote"]
    assert len(busca.casos) == medidas["casos_com_gabarito"] and all(len(v) == 3 for v in busca.antes.values())
    edicoes = pe.edicoes_do_lote_da_corrida_20()
    assert len(edicoes) == medidas["edicoes"]
    chaves = ("casos_em_que_os_tres_verbetes_mudam", "verbete_certo_entra", "verbete_certo_sai", "casos_que_leriam_a_edicao")
    for e, esperado in zip(edicoes, medidas["por_edicao"]):
        r = pe.portao_da_busca(busca, e)
        assert (e["caso"], e["verbete"], e["operacao"]) == (esperado["caso"], esperado["verbete"], esperado["operacao"])
        assert {k: r[k] for k in chaves} == {k: esperado[k] for k in chaves}, (e["caso"], e["verbete"], r)
        assert r["passa"] is (r["verbete_certo_sai"] == 0) and len(r["casos_que_perdem_o_verbete_certo"]) == r["verbete_certo_sai"], r
        assert (r["motivo"] is None) is r["passa"]
    assert evo.hash_biblioteca(base) == hash_antes, "a biblioteca de base só é lida: a edição entra numa cópia temporária"
    # o sinal de busca: palavras-chave e sintomas novos num verbete que já existe; o caso de origem tem de passar a recebê-lo
    sem_o_certo = next(cid for cid, tres in busca.antes.items() if busca.certo[cid] not in tres and busca.certo[cid] in {v["id"] for v in busca.verbetes})
    alvo = next(v for v in busca.verbetes if v["id"] == busca.certo[sem_o_certo])
    sinal = {"operacao": pe.OPERACAO_SINAL, "caso": sem_o_certo, "verbete": alvo["id"], "arquivo": alvo["caminho"].relative_to(base).as_posix(), "texto": "", "motivo": "",
             "trecho": None, "palavras_chave_novas": [], "sintomas_novos": [], "novo": None, "modelo": "qwen2.5:7b", "epoca": 101, "numero": 1}
    inocuo = pe.portao_da_busca(busca, sinal)
    assert inocuo["passa"] is False and "caso de origem" in inocuo["motivo"] and inocuo["origem_recebe_o_verbete_depois"] is False, inocuo
    # com os termos da própria consulta do caso como palavras-chave novas, a busca passa a entregar o verbete ao caso de origem
    import recuperacao as rec
    termos = [t for t in dict.fromkeys(rec.sinais_do_caso(busca.consultas[sem_o_certo])["consulta"]) if len(t) > 3][:12]
    forte = pe.portao_da_busca(busca, {**sinal, "palavras_chave_novas": termos, "sintomas_novos": termos})
    assert forte["origem_recebe_o_verbete_antes"] is False and forte["casos_que_leriam_a_edicao"] >= 1, forte
    assert forte["origem_recebe_o_verbete_depois"] is True, "com os termos do caso no verbete, a busca do caso de origem passa a entregá-lo"
    assert forte["passa"] is (forte["verbete_certo_sai"] == 0), forte


def teste_m1_mede_os_tres_portoes_nas_92_propostas_contra_a_revisao_humana():
    import portoes_de_edicao as pe
    d = pe.medir_m1(gerado_em="2026-11-10T00:00:00")
    r = d["resumo"]
    medidas = json.loads(_MEDIDAS_DO_FLUXO.read_text(encoding="utf-8"))["ideia_3"]
    bibl = json.loads((RA / "fase4" / "biblioteca.json").read_text(encoding="utf-8"))["resumo"]
    assert (r["propostas"], r["casos"], r["revisadas"]) == (bibl["propostas"], bibl["casos"], medidas["revisao_do_lote"]["edicoes_revisadas"]), r
    assert {v: r["por_veredito"][v] for v in pe.VEREDITOS} == medidas["revisao_do_lote"]["por_veredito"], r["por_veredito"]
    assert [p["portao"] for p in d["por_portao"]] == list(pe.PORTOES)
    for p in d["por_portao"]:
        rev = p["nas_revisadas"]
        assert rev["recusa"] + rev["passa"] == r["revisadas"], p
        assert sum(x["recusa"] for x in rev["por_veredito"]) == rev["recusa"] and [x["veredito"] for x in rev["por_veredito"]] == list(pe.VEREDITOS), p
        assert p["corretas_perdidas"] == next(x["recusa"] for x in rev["por_veredito"] if x["veredito"] == "Correta"), p
        assert p["erradas_e_parciais_recusadas"] == rev["recusa"] - p["corretas_perdidas"], p
        todas = p["nas_propostas"]
        assert todas["recusa"] + todas["passa"] + todas["nao_se_aplica"] == r["propostas"], p
    forma, texto, busca = d["por_portao"]
    assert forma["nas_propostas"]["nao_se_aplica"] == 0 and texto["nas_propostas"]["nao_se_aplica"] == 0
    assert busca["nas_propostas"]["nao_se_aplica"] == r["propostas"] - r["revisadas"], "o portão da busca só se aplica ao que virou edição"
    # a contagem publicada da pesquisa (cinco radicais) fica ao lado da do portão, que pega mais
    assert r["forma_pela_lista_da_pesquisa"] == medidas["forma_de_instrucao"]["em_forma_de_instrucao"] <= forma["nas_propostas"]["recusa"], r
    assert r["forma_pela_lista_da_pesquisa_nas_revisadas"] == medidas["forma_de_instrucao"]["passaram_em_forma_de_instrucao"] <= forma["nas_revisadas"]["recusa"], r
    b = d["busca"]
    assert (b["casos_com_gabarito"], b["edicoes"], b["verbete_certo_entra"], b["verbete_certo_sai"]) == (medidas["portao_da_busca_no_lote"]["casos_com_gabarito"], r["revisadas"],
                                                                                                    medidas["portao_da_busca_no_lote"]["verbete_certo_entra_no_total"],
                                                                                                    medidas["portao_da_busca_no_lote"]["verbete_certo_sai_no_total"]), b
    # os portões em sequência nunca aumentam o que sobra, e cada etapa soma os vereditos
    seq = d["em_sequencia"]
    assert [x["sobram"] for x in seq] == sorted((x["sobram"] for x in seq), reverse=True) and seq[0]["sobram"] == r["revisadas"] and len(seq) == 4, seq
    assert all(sum(x[v] for v in pe.VEREDITOS) == x["sobram"] for x in seq + d["outras_sequencias"]), seq
    assert seq[-1]["sobram"] == r["sobram_depois_dos_tres"] == sum(1 for x in d["revisadas"] if x["passa_nos_tres"]), r
    assert len(d["revisadas"]) == r["revisadas"] and len(d["propostas"]) == r["propostas"]
    assert all(x["veredito"] in pe.VEREDITOS and x["busca"] is not None for x in d["revisadas"])
    assert sum(x["propostas"] for x in d["por_destino"]) == r["propostas"] and sum(x["propostas"] for x in d["primeiras_palavras"]) == r["propostas"]
    assert all(x["recusada_pela_forma"] in (True, False) for x in d["primeiras_palavras"])


def teste_m1_render_e_documento_gravado_com_check():
    import portoes_de_edicao as pe
    d = pe.medir_m1(gerado_em="2026-11-10T00:00:00")
    md = pe.render_m1(d)
    for bloco in ("resumo", "portoes", "sequencia", "destino", "criterios", "palavras", "revisadas", "propostas"):
        assert f"<!-- tabela:{pe.PREFIXO_M1}{bloco} -->" in md and f"<!-- /tabela:{pe.PREFIXO_M1}{bloco} -->" in md, bloco
    for trecho in ("M1", "decisão 121", "corrida 20", "revisão humana", "Correta", "Parcial", "Errada", "portão 3", "portão 4", "portão 5"):
        assert trecho in md, trecho
    assert md.splitlines()[2].startswith("# ") and "gerada em 2026-11-10" in md.splitlines()[2]
    assert "—" not in md.split("<!-- tabela:")[0] and "→" not in md, "sem travessão nem seta no texto corrido gerado"
    pasta = RA / "fase4"
    assert (pasta / "portoes_m1.json").exists() and (pasta / "portoes_m1.md").exists(), "rode python portoes_de_edicao.py --m1"
    assert pe.main(["--m1", "--check"]) == 0


# ------------------------------------------------------------------ corrida 27 (medida M2): o analista de documentação com a ficha curta do caso (ficha 67, decisão 121)

# ! Alteração de IA - Revisar: (11/11/2026, ficha 67 opção b, decisão 121) testes da corrida 27 (`experimento_analista.py`), escritos ANTES do módulo: a primeira rodada falha
# por ModuleNotFoundError em `experimento_analista`, o RED aceito para módulo novo. Conferem: o prompt do analista congelado com hash, com a parte fixa na frente e o formato
# de uma proposta só; a leitura da corrida 20 pela trilha (os 54 casos de aprendizado, a origem de cada um, a lista da busca e o nó do diagnóstico) e a ficha curta de cada
# caso (as linhas pedidas pela proposta de desenho, dentro do orçamento de tokens, sem trecho literal do corpo HTTP e sem a frase de impacto e a linha FONTE do modelo); o
# leitor da resposta (as quatro saídas, a tolerância a acento e negrito, o bloco que copia o modelo do formato, a resposta cortada); a validação do sinal de busca, que o
# validador da Fase 3 não conhece; os cinco portões em cadeia; o teste exato de Fisher; o resumo contra a corrida 20 com a regra fixada antes; e a prévia gravada.
# ! Motivo: a corrida 27 custa cerca de uma hora e meia na janela do Eric, e a comparação com a corrida 20 só vale se o analista receber o mesmo caso, a mesma resposta do
# agente e a mesma biblioteca de antes do lote; um erro na ficha ou no leitor da resposta só apareceria depois da corrida. O prompt é peça medida: por isso fica congelado
# com hash e o teste acusa qualquer mudança de uma letra.
def teste_analista_prompt_congelado_com_hash_e_formato_de_uma_proposta():
    import estrategias
    import evolucao_biblioteca as evo
    import experimento_analista as ea
    assert (ea.CORRIDA, ea.NOME, ea.PREFIXO, ea.ALFA, ea.ORCAMENTO_DA_FICHA) == (27, "analista", "tb_f4_analista_", 0.05, 400)
    assert ea.OPERACOES == ("sinal_de_busca", "nota", "retificacao") and ea.ABSTENCAO == "nenhuma"
    assert ea.hash_das_instrucoes() == ea.HASH_DAS_INSTRUCOES and len(ea.HASH_DAS_INSTRUCOES) == 16, "as instruções do analista mudaram: o prompt é peça medida e fica congelado"
    fixo = ea.INSTRUCOES
    for trecho in ("sinal_de_busca", "nota", "retificacao", "nenhuma", "PROPOSTA", "OPERACAO:", "PALAVRAS_CHAVE:", "SINTOMAS:", "TRECHO:", "TEXTO:", "MOTIVO:", "FIM",
                   f"{evo.TEXTO_MIN} a {evo.TEXTO_MAX}", f"{evo.MOTIVO_MIN} a {evo.MOTIVO_MAX}", f"ate {evo.MAX_PALAVRAS_CHAVE_NOVAS} termos", f"ate {evo.MAX_SINTOMAS_NOVOS} sintomas",
                   "Uma proposta só", "afirmação"):
        assert trecho in fixo, trecho
    assert "novo_verbete" not in fixo and "VERBETE:" not in fixo, "o analista não cria verbete nem escolhe o verbete: a edição entra no da causa certa"
    assert "—" not in fixo and "→" not in fixo
    prompt_a = ea.prompt_do_analista("REQUISIÇÃO: GET /api/produtos\nSINTOMA: a lista vem vazia.", "[campo_ausente] Campo ausente\nTexto do verbete A.")
    prompt_b = ea.prompt_do_analista("REQUISIÇÃO: GET /api/pedidos\nSINTOMA: outro caso.", "[tipo_divergente] Tipo divergente\nTexto do verbete B.")
    assert prompt_a.startswith(fixo) and prompt_b.startswith(fixo), "a parte fixa vem na frente, igual em todo caso, para o Ollama reaproveitar a leitura dela"
    assert "Texto do verbete A." in prompt_a and "SINTOMA: a lista vem vazia." in prompt_a and prompt_a.index("Texto do verbete A.") < prompt_a.index("SINTOMA: a lista vem vazia.")
    assert prompt_a.rstrip().endswith(ea.LEMBRETE_FINAL) and ea.LEMBRETE_FINAL in prompt_b
    # o prompt do diagnóstico e o da proposta de edição de hoje não entram
    assert "CAUSA_RAIZ:" not in prompt_a and "CORREÇÃO DESTE CASO" not in prompt_a and estrategias._FORMATO_COM_FONTE not in prompt_a


def teste_analista_le_a_corrida_20_e_monta_a_ficha_curta_de_cada_caso():
    import biblioteca_fase4 as b4
    import corridas_em_texto as ct
    import experimento_analista as ea
    itens = ea.casos_da_corrida_20()
    resumo20 = {json.loads(l)["caso"]: json.loads(l) for l in (RA / "fase4_biblioteca" / "biblioteca.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()}
    assert len(itens) == len(resumo20) == 54 and [i["caso"]["id"] for i in itens] == list(resumo20), "os mesmos 54 casos de aprendizado, na ordem da corrida 20"
    base = ea.base_da_corrida_20()
    verbetes = {v["id"]: v for v in bib.carregar(base)}
    for i in itens:
        cid, esperado = i["caso"]["id"], resumo20[i["caso"]["id"]]
        g = i["caso"]["gabarito"]["causa_raiz"]
        assert i["origem"] == esperado["origem"] and i["no"]["escolha"] == esperado["rotulo"] and i["acertou"] is esperado["acertou"], cid
        assert i["no"]["confianca"]["selo"] == esperado["selo"], cid
        entregues = i["entregues"]
        assert 3 <= len(entregues) <= 4 and (i["posicao_do_ouro"] is None or i["posicao_do_ouro"] >= 1), cid
        assert (g in entregues) is (i["ouro_entregue"]), cid
        ficha = ea.ficha_do_caso(i, verbetes)
        for linha in ("REQUISIÇÃO: ", "SINTOMA: ", "DIFERENÇA MEDIDA CONTRA O CONTRATO: ", "BUSCA: ", "RESPOSTA DO AGENTE: ", "CONFERÊNCIAS QUE NÃO CONFERIRAM: ", "DECISÃO DE QUEM REVISOU: "):
            assert sum(1 for l in ficha.splitlines() if l.startswith(linha)) == 1, (cid, linha)
        assert all(f"[{e}]" in ficha for e in entregues) and f"[{g}]" in ficha, cid
        decisao = next(l for l in ficha.splitlines() if l.startswith("DECISÃO DE QUEM REVISOU: "))
        assert ("aceito" in decisao) is i["acertou"] and ("recusado" in decisao) is (not i["acertou"]) and f"Causa certa: {g}" in decisao, (cid, decisao)
        assert ea.tokens_estimados(ficha) <= ea.ORCAMENTO_DA_FICHA, (cid, ea.tokens_estimados(ficha))
        # nenhum trecho literal do corpo HTTP (a mesma regra de 20 caracteres do filtro da Fase 4), e nada do que o modelo escreveu além da causa e do campo
        assert b4.filtro_texto_de_origem_proibida({"TEXTO": ficha}, i["corpo_http"]) is None, cid
        assert "IMPACTO:" not in ficha and "FONTE:" not in ficha, cid
        resposta = i["registro"]["resposta"]
        impacto = next((l.split(":", 1)[1].strip() for l in resposta.splitlines() if l.startswith("IMPACTO:")), "")
        # a frase de impacto do modelo não entra na ficha; quando ela aparece, é porque o modelo copiou o sintoma do caso, que entra
        assert not impacto or impacto not in ficha or impacto in str(i["lido"]["entrada"].get("sintoma")), (cid, "a frase de impacto do modelo não entra na ficha")
        assert "—" not in ficha and "→" not in ficha, cid
        assert i["acertou"] is (ct.rotulo_lido(resposta) == g), cid
    # a seleção da seção 4.2 da proposta: quem teria lacuna e quem o desenho chamaria
    com_lacuna = [i for i in itens if i["selecao"]["lacuna"]]
    assert sum(1 for i in itens if not i["acertou"]) <= len(com_lacuna) < len(itens)
    assert all(i["selecao"]["seria_chamado"] is (i["selecao"]["lacuna"] and not i["selecao"]["verbete_ja_registra_o_caso"]) for i in itens)
    # um caso da tela e um do fixture, conferidos no conteúdo
    tela = next(i for i in itens if i["origem"] == "tela")
    fixture = next(i for i in itens if i["origem"] == "fixture")
    assert tela["lido"]["entrada"]["requisicao"] and fixture["lido"]["entrada"]["sintoma"] == fixture["caso"]["entrada"]["sintoma"], "o caso escrito é lido como o diagnóstico o leu"
    assert "gabarito" in fixture["lido"] and fixture["lido"]["id"] == fixture["caso"]["id"]


def teste_analista_le_a_resposta_nas_quatro_saidas():
    import experimento_analista as ea

    def bloco(operacao: str, **campos) -> str:
        linhas = ["PROPOSTA", f"OPERACAO: {operacao}"] + [f"{k}: {v}" for k, v in campos.items()] + ["FIM"]
        return "\n".join(linhas)

    nota = ea.parsear_resposta(bloco("nota", PALAVRAS_CHAVE="nenhuma", SINTOMAS="nenhum", TEXTO="A rota de lista devolve cada item com os sete campos do contrato.",
                                     MOTIVO="O campo preco não veio na resposta."))
    assert (nota["operacao"], nota["abstencao"], nota["malformado"], nota["blocos"]) == ("nota", False, None, 1), nota
    assert nota["campos"]["TEXTO"].startswith("A rota de lista") and nota["campos"]["MOTIVO"].startswith("O campo preco")
    sinal = ea.parsear_resposta(bloco("sinal de busca", PALAVRAS_CHAVE="preco ausente, cartao sem valor", SINTOMAS="botao com valor undefined", MOTIVO="O verbete ficou na posição 5."))
    assert sinal["operacao"] == "sinal_de_busca" and sinal["malformado"] is None and "TEXTO" not in sinal["campos"], sinal
    retif = ea.parsear_resposta("**PROPOSTA**\n**OPERAÇÃO:** retificação\nTRECHO: \"o corpo vem vazio\"\nTEXTO: O corpo vem com o status 204\ne sem conteúdo.\nMOTIVO: O status do caso é 204.\nFIM")
    assert retif["operacao"] == "retificacao" and retif["campos"]["TEXTO"] == "O corpo vem com o status 204 e sem conteúdo." and retif["campos"]["TRECHO"], retif
    for texto in ("NENHUMA", "PROPOSTA\nOPERACAO: nenhuma\nMOTIVO: O verbete já bastava para este caso.\nFIM", "Nenhuma."):
        r = ea.parsear_resposta(texto)
        assert r["abstencao"] is True and r["operacao"] is None and r["malformado"] is None, (texto, r)
    for texto, trecho in (("Não sei o que propor.", "sem bloco"), (bloco("nota", MOTIVO="O campo preco não veio na resposta."), "TEXTO"),
                          (bloco("sinal_de_busca | nota | retificacao | nenhuma", TEXTO="x", MOTIVO="y"), "formato"), (bloco("novo_verbete", TEXTO="x" * 70, MOTIVO="y" * 30), "OPERACAO"),
                          (bloco("retificacao", TEXTO="A frase certa do verbete fica assim, com o status 204.", MOTIVO="O status do caso é 204."), "TRECHO"),
                          (bloco("sinal_de_busca", PALAVRAS_CHAVE="nenhuma", SINTOMAS="nenhum", MOTIVO="O verbete ficou na posição 5."), "PALAVRAS_CHAVE")):
        r = ea.parsear_resposta(texto)
        assert r["abstencao"] is False and r["malformado"] and trecho in r["malformado"], (texto, r)
    dois = ea.parsear_resposta(bloco("nota", TEXTO="A primeira frase vale como proposta do caso inteiro aqui.", MOTIVO="O campo preco não veio.") + "\n\n"
                               + bloco("nota", TEXTO="A segunda fica de fora, porque é uma proposta por caso.", MOTIVO="O campo nome não veio."))
    assert dois["blocos"] == 2 and dois["campos"]["TEXTO"].startswith("A primeira") and dois["malformado"] is None, dois
    cortada = ea.parsear_resposta("PROPOSTA\nOPERACAO: nota\nTEXTO: A rota de lista devolve cada item com os sete campos\nMOTIVO: O campo", tokens_saida=700, teto=700)
    assert cortada["truncada"] is True and cortada["malformado"] and "cortada" in cortada["malformado"], cortada
    inteira = ea.parsear_resposta(bloco("nota", TEXTO="A rota de lista devolve cada item com os sete campos do contrato.", MOTIVO="O campo preco não veio."), tokens_saida=90, teto=700)
    assert inteira["truncada"] is False and inteira["fim_ausente"] is False


def _contexto_do_analista():
    import experimento_analista as ea
    if "ctx" not in _CONTEXTO_DO_ANALISTA:
        _CONTEXTO_DO_ANALISTA["ctx"] = ea.contexto_dos_portoes()
        _CONTEXTO_DO_ANALISTA["itens"] = ea.casos_da_corrida_20()
    return _CONTEXTO_DO_ANALISTA["ctx"], _CONTEXTO_DO_ANALISTA["itens"]


_CONTEXTO_DO_ANALISTA: dict = {}


def teste_analista_valida_o_sinal_de_busca_que_o_validador_da_fase_3_nao_conhece():
    import evolucao_biblioteca as evo
    import experimento_analista as ea
    ctx, itens = _contexto_do_analista()
    item = next(i for i in itens if not i["ouro_entregue"])
    ouro = ctx["por_id"][item["caso"]["gabarito"]["causa_raiz"]]
    motivo = "O verbete da causa certa ficou fora dos tres entregues pela busca neste caso."
    bom = ea.validar_sinal_de_busca({"PALAVRAS_CHAVE": "termo inedito xyz, outro termo novo qwe", "SINTOMAS": "sintoma inedito abc", "MOTIVO": motivo}, item["lido"], ouro, ctx)
    assert bom["aceita"] is True and bom["motivo"] is None, bom
    e = bom["edicao"]
    assert (e["operacao"], e["verbete"], e["caso"], e["texto"], e["trecho"], e["novo"]) == (ea.OPERACOES[0], ouro["id"], item["caso"]["id"], "", None, None), e
    assert e["palavras_chave_novas"] == ["termo inedito xyz", "outro termo novo qwe"] and e["sintomas_novos"] == ["sintoma inedito abc"] and e["arquivo"].endswith(f"{ouro['id']}.md"), e
    muitos = ", ".join(f"termo novo {n}" for n in range(evo.MAX_PALAVRAS_CHAVE_NOVAS + 1))
    for campos, codigo in (({"PALAVRAS_CHAVE": muitos, "SINTOMAS": "nenhum", "MOTIVO": motivo}, "palavra_chave_invalida"),
                           ({"PALAVRAS_CHAVE": "Termo com (parenteses)!", "SINTOMAS": "nenhum", "MOTIVO": motivo}, "palavra_chave_invalida"),
                           ({"PALAVRAS_CHAVE": ", ".join(ouro["meta"].get("palavras_chave", [])[:2]) or "nenhuma", "SINTOMAS": "nenhum", "MOTIVO": motivo}, "sinal_sem_termo_novo"),
                           ({"PALAVRAS_CHAVE": "termo inedito xyz", "SINTOMAS": "nenhum", "MOTIVO": "curto"}, "motivo_curto"),
                           ({"PALAVRAS_CHAVE": "termo inedito xyz", "SINTOMAS": "nenhum", "MOTIVO": ""}, "motivo_ausente"),
                           ({"PALAVRAS_CHAVE": "termo inedito xyz", "SINTOMAS": "nenhum", "MOTIVO": f"O caso {item['caso']['id']} mostrou que a busca nao entregou o verbete."}, "copia_do_caso")):
        r = ea.validar_sinal_de_busca(campos, item["lido"], ouro, ctx)
        assert r["aceita"] is False and r["motivo"] == codigo and r["edicao"] is None, (campos, r)
    assert "sinal_sem_termo_novo" in ea.CODIGOS_NOVOS


def teste_analista_aplica_os_cinco_portoes_em_cadeia():
    import evolucao_biblioteca as evo
    import experimento_analista as ea
    ctx, itens = _contexto_do_analista()
    hash_antes = evo.hash_biblioteca(ctx["base"])
    item = next(i for i in itens if not i["ouro_entregue"])
    abst = ea.aplicar_portoes(ea.parsear_resposta("NENHUMA"), item, ctx)
    assert abst["destino"] == ea.DESTINOS[0] and abst["parou_em"] is None and abst["edicao"] is None and all(v is None for v in abst["portoes"].values()), abst
    ruim = ea.aplicar_portoes(ea.parsear_resposta("Não sei."), item, ctx)
    assert ruim["destino"] == ea.DESTINOS[1] and ruim["parou_em"] == "formato" and ruim["codigo"], ruim
    campo = item["caso"]["gabarito"].get("campo_afetado") or "status"
    instrucao = ea.aplicar_portoes(ea.parsear_resposta(
        "PROPOSTA\nOPERACAO: nota\nPALAVRAS_CHAVE: nenhuma\nSINTOMAS: nenhum\n"
        f"TEXTO: Adicionar nota sobre a necessidade de conferir o campo {campo} na resposta da API antes de montar a tela do usuario.\n"
        f"MOTIVO: O campo {campo} do caso mostrou a lacuna na documentacao do sistema.\nFIM"), item, ctx)
    assert instrucao["portoes"]["forma"]["passa"] is False and instrucao["portoes"]["texto"] is not None, "os portões 3 e 4 leem o texto mesmo quando outro portão recusa"
    assert instrucao["passa_nos_cinco"] is False and instrucao["parou_em"] in ea.PORTOES and instrucao["destino"] in ea.DESTINOS, instrucao
    if instrucao["portoes"]["validador"]["passa"] and instrucao["portoes"]["filtros"]["passa"]:
        assert instrucao["parou_em"] == "forma" and instrucao["passa_nos_filtros_de_hoje"] is True and instrucao["portoes"]["busca"] is not None, instrucao
    sinal = ea.aplicar_portoes(ea.parsear_resposta(
        "PROPOSTA\nOPERACAO: sinal_de_busca\nPALAVRAS_CHAVE: termo inedito xyz\nSINTOMAS: nenhum\n"
        f"MOTIVO: O campo {campo} do caso mostrou que a busca deixou o verbete fora dos entregues.\nFIM"), item, ctx)
    assert sinal["portoes"]["forma"] is None and sinal["portoes"]["texto"] is None, "o sinal de busca não tem texto: os portões 3 e 4 não se aplicam"
    assert sinal["portoes"]["validador"]["passa"] is True and sinal["edicao"]["operacao"] == ea.OPERACOES[0], sinal
    if sinal["portoes"]["filtros"]["passa"]:
        busca = sinal["portoes"]["busca"]
        assert busca is not None and busca["passa"] is False and "caso de origem" in busca["motivo"] and sinal["parou_em"] == "busca", sinal
    assert set(sinal["portoes"]) == set(ea.PORTOES) and len(ea.DESTINOS) == len(ea.PORTOES) + 3
    assert evo.hash_biblioteca(ctx["base"]) == hash_antes, "a biblioteca de antes do lote só é lida"


def teste_analista_fisher_exato_bate_com_valores_conhecidos():
    import experimento_analista as ea
    assert ea.fisher_exato(1, 9, 11, 3) == 0.0028, ea.fisher_exato(1, 9, 11, 3)        # o exemplo clássico: p bilateral 0,002759
    assert ea.fisher_exato(3, 1, 1, 3) == 0.4857, ea.fisher_exato(3, 1, 1, 3)          # a prova do chá de Fisher: p bilateral 0,4857
    assert ea.fisher_exato(5, 5, 5, 5) == 1.0 and ea.fisher_exato(0, 0, 0, 0) == 1.0 and ea.fisher_exato(2, 18, 2, 18) == 1.0
    assert ea.fisher_exato(0, 10, 10, 0) < 0.001


def _registro_do_analista(caso: str, operacao: str | None, destino: int, *, texto: str = "", forma: bool | None = None, texto_passa: bool | None = None, busca: bool | None = None,
                          validador: bool | None = None, filtros: bool | None = None, lacuna: bool = True, acertou: bool = False, origem: str = "fixture") -> dict:
    import experimento_analista as ea
    portoes = {"validador": None if validador is None else {"passa": validador, "codigo": None if validador else "texto_curto", "detalhe": None},
               "filtros": None if filtros is None else {"passa": filtros, "codigo": None if filtros else "sem_evidencia_do_caso", "filtro": None, "detalhe": None, "para_revisao": False},
               "forma": None if forma is None else {"passa": forma, "primeira_palavra": texto.split(" ")[0].lower() if texto else "", "motivo": None if forma else "verbo de edição"},
               "texto": None if texto_passa is None else {"passa": texto_passa, "reprovados": [] if texto_passa else ["termos_sem_expansao_n"], "alarme_flesch": False, "termos_sem_expansao": []},
               "busca": None if busca is None else {"passa": busca, "motivo": None if busca else "o verbete da causa certa sai", "verbete_certo_entra": 0, "verbete_certo_sai": 0 if busca else 1,
                                                    "casos_em_que_os_tres_verbetes_mudam": 1, "casos_que_leriam_a_edicao": 3}}
    ordem = [p for p in ea.PORTOES if portoes[p] is not None and not portoes[p]["passa"]]
    return {"caso": caso, "origem": origem, "acertou_diagnostico": acertou, "selecao": {"lacuna": lacuna, "verbete_ja_registra_o_caso": False, "seria_chamado": lacuna},
            "operacao": operacao, "abstencao": destino == 0, "malformado": "sem bloco PROPOSTA" if destino == 1 else None, "blocos": 0 if destino in (0, 1) else 1,
            "campos": {"TEXTO": texto, "MOTIVO": "O campo preco não veio na resposta."} if texto else {}, "destino": ea.DESTINOS[destino], "parou_em": ordem[0] if ordem else None,
            "codigo": None, "portoes": portoes, "edicao": {"caso": caso, "verbete": "campo_ausente", "operacao": operacao, "texto": texto} if validador else None,
            "passa_nos_filtros_de_hoje": bool(validador and filtros), "passa_nos_cinco": destino == len(ea.DESTINOS) - 1, "copia_do_exemplo": False,
            "tokens_entrada": 1200, "tokens_saida": 150, "segundos": 90.0, "ficha_tokens": 300, "versao_ollama": "0.40.15"}


def _dados_do_analista(abstencoes: int = 2) -> dict:
    """Dez casos: `abstencoes` abstenções, uma resposta sem bloco, quatro notas (duas afirmações que passam nos cinco, uma instrução recusada pela forma e uma recusada pelo
    validador), um sinal de busca recusado pela busca e o resto notas que passam; a corrida 20 de comparação tem 92 propostas em 54 casos, nenhuma abstenção e 20 revisadas."""
    import experimento_analista as ea
    regs = [_registro_do_analista(f"c-{n}", None, 0, lacuna=False, acertou=True) for n in range(abstencoes)]
    regs.append(_registro_do_analista("c-sem", None, 1))
    regs.append(_registro_do_analista("c-n1", "nota", 7, texto="A rota de lista devolve os sete campos do contrato em cada item.", forma=True, texto_passa=True, busca=True, validador=True, filtros=True))
    regs.append(_registro_do_analista("c-n2", "nota", 7, texto="O cartão fica sem preço quando o campo não vem.", forma=True, texto_passa=True, busca=True, validador=True, filtros=True, origem="tela"))
    regs.append(_registro_do_analista("c-n3", "nota", 4, texto="Adicionar nota sobre o campo preco ausente.", forma=False, texto_passa=True, busca=True, validador=True, filtros=True))
    regs.append(_registro_do_analista("c-n4", "nota", 2, texto="A rota devolve.", forma=True, texto_passa=True, validador=False))
    regs.append(_registro_do_analista("c-s1", "sinal_de_busca", 6, busca=False, validador=True, filtros=True))
    while len(regs) < 10:
        regs.append(_registro_do_analista(f"c-x{len(regs)}", "nota", 7, texto="A interface espera um objeto na rota de detalhe do produto.", forma=True, texto_passa=True, busca=True, validador=True,
                                          filtros=True))
    corrida20 = {"casos": 54, "propostas": 92, "abstencoes": 0, "passaram_nos_filtros": 20, "com_texto": 92, "afirmacoes": 6, "por_veredito": {"Correta": 2, "Parcial": 9, "Errada": 9},
                 "por_operacao": {"nota": 41, "novo_verbete": 25, "retificacao": 26}, "tokens_entrada_mediana": 2358, "tokens_saida_mediana": 361, "segundos_mediana": 158.2,
                 "abstencao_por_caso": {r["caso"]: False for r in regs}}
    condicoes = {"modo": "analista", "parcial": False, "versao_ollama": "0.40.15", "casos": len(regs), "hash_das_instrucoes": ea.HASH_DAS_INSTRUCOES, "versao_ollama_da_corrida_20": "0.40.14"}
    return {"registros": regs, "corrida20": corrida20, "condicoes": condicoes, "ponte": {"versao": "0.40.15", "corrida": "fase3b_ponte_04015", "pareavel": True, "b": 1, "c": 0, "limite": 2, "n": 35}}


def teste_analista_resume_contra_a_corrida_20_e_aplica_a_regra_fixada_antes():
    import avaliar
    import experimento_analista as ea
    x = _dados_do_analista()
    d = ea.resumir(x["registros"], x["corrida20"], x["condicoes"], ponte=x["ponte"], corrida="x", gerado_em="2026-11-11T00:00:00")
    r = d["resumo"]
    assert (r["casos"], r["abstencoes"], r["sem_bloco"], r["propostas"], r["com_texto"], r["afirmacoes"]) == (10, 2, 1, 7, 6, 5), r
    assert (r["passam_nos_filtros_de_hoje"], r["passam_nos_cinco"], r["vao_para_a_revisao"]) == (6, 4, 6), r
    assert r["por_operacao"] == {"sinal_de_busca": 1, "nota": 6, "retificacao": 0}, r["por_operacao"]
    assert (r["tokens_entrada_mediana"], r["tokens_saida_mediana"], r["segundos_mediana"], r["segundos_no_total"]) == (1200, 150, 90.0, 900.0), r
    le = {x_["leitura"]: x_ for x_ in d["leituras"]}
    assert list(le) == ["abstencao", "forma", "parcela_correta"]
    assert (le["abstencao"]["corrida_27"], le["abstencao"]["corrida_20"], le["abstencao"]["b"], le["abstencao"]["c"]) == ("2 de 10", "0 de 54", 2, 0), le["abstencao"]
    assert le["abstencao"]["p"] == avaliar.mcnemar_exato(2, 0) and le["abstencao"]["veredito"] == "dentro do ruído", le["abstencao"]
    assert (le["forma"]["corrida_27"], le["forma"]["corrida_20"]) == ("5 de 6", "6 de 92") and le["forma"]["p"] == ea.fisher_exato(5, 1, 6, 86), le["forma"]
    assert le["forma"]["p"] < ea.ALFA and le["forma"]["veredito"] == "sai do ruído: mais afirmações na corrida 27", le["forma"]
    assert le["parcela_correta"]["p"] is None and le["parcela_correta"]["veredito"].startswith("sem veredito") and "revisão humana" in le["parcela_correta"]["veredito"], le["parcela_correta"]
    assert d["regra"]["texto"] == ea.texto_da_regra() and d["regra"]["pareavel"] is True and r["completo"] is True
    portoes = {p["portao"]: p for p in d["por_portao"]}
    assert list(portoes) == list(ea.PORTOES)
    assert (portoes["validador"]["avaliadas"], portoes["validador"]["recusa"], portoes["forma"]["avaliadas"], portoes["forma"]["recusa"], portoes["busca"]["recusa"]) == (7, 1, 6, 1, 1), portoes
    assert portoes["forma"]["nao_se_aplica"] == 1 and portoes["filtros"]["avaliadas"] == 6
    destinos = {x_["destino"]: x_["casos"] for x_ in d["por_destino"]}
    assert list(destinos) == list(ea.DESTINOS) and sum(destinos.values()) == 10 and destinos[ea.DESTINOS[0]] == 2 and destinos[ea.DESTINOS[-1]] == 4, destinos
    lacuna = {x_["grupo"]: x_ for x_ in d["por_lacuna"]}
    assert (lacuna["sem lacuna"]["casos"], lacuna["sem lacuna"]["abstencoes"], lacuna["com lacuna"]["casos"], lacuna["com lacuna"]["abstencoes"]) == (2, 2, 8, 0), lacuna
    assert {x_["origem"]: x_["casos"] for x_ in d["por_origem"]} == {"fixture": 9, "tela": 1}
    assert len(d["casos"]) == 10 and d["casos"][2]["destino"] == ea.DESTINOS[1]
    # seis abstenções contra nenhuma saem do ruído; com a revisão humana preenchida, a parcela correta ganha o teste
    seis = _dados_do_analista(abstencoes=6)
    d6 = ea.resumir(seis["registros"], seis["corrida20"], seis["condicoes"], ponte=seis["ponte"], corrida="x")
    ab = d6["leituras"][0]
    assert ab["p"] < ea.ALFA and ab["veredito"] == "sai do ruído: mais abstenção na corrida 27", ab
    revisao = {"quem": None, "itens": [{"origem": "27", "caso": c, "veredito": v} for c, v in (("c-n1", "Correta"), ("c-n2", "Correta"), ("c-n3", "Parcial"), ("c-s1", "Errada"),
                                                                                             ("c-x8", "Correta"), ("c-x9", "Correta"))]
               + [{"origem": "20", "caso": f"z-{n}", "veredito": v} for n, v in enumerate(["Correta"] * 2 + ["Parcial"] * 9 + ["Errada"] * 9)]}
    dr = ea.resumir(x["registros"], x["corrida20"], x["condicoes"], ponte=x["ponte"], corrida="x", revisao=revisao)
    pc = dr["leituras"][2]
    assert (pc["corrida_27"], pc["corrida_20"]) == ("4 de 6", "2 de 20") and pc["p"] == ea.fisher_exato(4, 2, 2, 18) and pc["veredito"].startswith("sai do ruído"), pc
    assert dr["revisao"]["corrida_27"] == {"Correta": 4, "Parcial": 1, "Errada": 1} and dr["revisao"]["corrida_20_pelo_mesmo_revisor"] == {"Correta": 2, "Parcial": 9, "Errada": 9}, dr["revisao"]
    assert dr["revisao"]["pendentes"] == 0 and [g["portao"] for g in dr["revisao"]["portoes_contra_a_revisao"]] == ["forma", "texto", "busca"]
    # sem ponte pareável, ou com a corrida incompleta, não há veredito
    sem_ponte = ea.resumir(x["registros"], x["corrida20"], x["condicoes"], ponte=None, corrida="x")
    assert all(l["veredito"].startswith("sem veredito") for l in sem_ponte["leituras"]) and "ponte" in sem_ponte["leituras"][0]["veredito"], sem_ponte["leituras"]
    parcial = ea.resumir(x["registros"][:-1], x["corrida20"], {**x["condicoes"], "casos": 10}, ponte=x["ponte"], corrida="x")
    assert parcial["resumo"]["completo"] is False and "não cobriu" in parcial["leituras"][0]["veredito"], parcial["leituras"]


def teste_analista_render_traz_os_blocos_a_regra_e_as_tres_leituras():
    import experimento_analista as ea
    x = _dados_do_analista()
    d = ea.resumir(x["registros"], x["corrida20"], x["condicoes"], ponte=x["ponte"], corrida="fase4_analista", gerado_em="2026-11-11T00:00:00")
    md = ea.render(d)
    for bloco in ("resumo", "leituras", "portoes", "destino", "lacuna", "origem", "codigos", "casos"):
        assert f"<!-- tabela:{ea.PREFIXO}{bloco} -->" in md and f"<!-- /tabela:{ea.PREFIXO}{bloco} -->" in md, bloco
    for trecho in ("corrida 27", "decisão 121", "M2", "corrida 20", "0,05", "abstenção", "forma do texto", "parcela correta", "revisão humana", "`c-n1`", ea.HASH_DAS_INSTRUCOES):
        assert trecho in md, trecho
    assert md.splitlines()[2].startswith("# ") and "gerada em 2026-11-11" in md.splitlines()[2]
    assert "—" not in md and "→" not in md, "sem travessão nem seta no texto gerado"


def teste_analista_previa_esta_gravada_e_bate_com_a_regeracao():
    import experimento_analista as ea
    d = ea.previa()
    r = d["resumo"]
    bibl = json.loads((RA / "fase4" / "biblioteca.json").read_text(encoding="utf-8"))["resumo"]
    assert (r["casos"], r["acertos_do_diagnostico"]) == (bibl["casos"], bibl["acertos_diagnostico"]), r
    assert r["origem_tela"] + r["origem_fixture"] == r["casos"] and r["ouro_entregue"] + r["ouro_fora_dos_entregues"] == r["casos"], r
    assert r["com_lacuna"] + r["sem_lacuna"] == r["casos"] and r["seriam_chamados"] <= r["com_lacuna"], r
    assert r["ficha_tokens_maximo"] <= ea.ORCAMENTO_DA_FICHA and r["fichas_acima_do_orcamento"] == 0, r
    assert r["inferencias"] == r["casos"] and r["minutos_estimados"] > 0 and r["prompt_tokens_mediana"] < r["prompt_tokens_da_proposta_de_hoje"], r
    assert d["prompt"]["hash_das_instrucoes"] == ea.HASH_DAS_INSTRUCOES and d["prompt"]["instrucoes"] == ea.INSTRUCOES and d["prompt"]["exemplo"].startswith(ea.INSTRUCOES), d["prompt"]["hash_das_instrucoes"]
    assert d["corrida_20"]["propostas"] == bibl["propostas"] and d["corrida_20"]["abstencoes"] == bibl["abstencoes"], d["corrida_20"]
    assert d["poder"]["abstencoes_para_sair_do_ruido"] == 6 and d["poder"]["corretas_em_20_para_sair_do_ruido"] > d["corrida_20"]["por_veredito"]["Correta"], d["poder"]
    assert len(d["casos"]) == r["casos"] and d["regra"] == ea.texto_da_regra()
    md = ea.render_previa(d)
    for bloco in ("previa_resumo", "previa_selecao", "previa_poder", "previa_casos"):
        assert f"<!-- tabela:{ea.PREFIXO}{bloco} -->" in md, bloco
    assert "```text" in md and ea.INSTRUCOES.splitlines()[0] in md, "a prévia mostra o prompt inteiro de um caso"
    assert "→" not in md.replace(d["prompt"]["exemplo"], "")
    pasta = RA / "fase4"
    assert (pasta / "analista_previa.json").exists() and (pasta / "analista_previa.md").exists(), "rode python experimento_analista.py --previa"
    assert ea.main(["--previa", "--check"]) == 0


def main() -> None:
    argparse.ArgumentParser(description=__doc__).parse_args()
    modulo = sys.modules[__name__]
    testes = [(nome, obj) for nome, obj in vars(modulo).items()
              if nome.startswith("teste_") and inspect.isfunction(obj) and obj.__module__ == modulo.__name__]
    try:
        for nome, funcao in testes:
            try:
                funcao()
            except Exception:  # noqa: BLE001 - o runner pega qualquer falha do teste para imprimir o rastro e parar com código 1
                print(nome)
                traceback.print_exc()
                sys.exit(1)
            print(f"{nome} ok")
        print(f"{len(testes)} testes ok")
    finally:
        for caminho in _TEMPORARIOS:
            shutil.rmtree(caminho, ignore_errors=True)


if __name__ == "__main__":
    main()
