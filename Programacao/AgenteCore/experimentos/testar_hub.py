#!/usr/bin/env python3
# ! Alteração de IA - Revisar: arquivo novo (25/11/2026, Pós-Fase 4, pacote Q6): os testes do hub central, no mesmo formato sem pytest de
# testar_pos_fase4.py (funções teste_<nome>(), main() roda todas em ordem de definição e termina em "N testes ok"). Etapa 1: os dados do hub
# (`hub_dados.py`: as corridas, a lista de casos, as iterações do mesmo caso, o caso montado da trilha com o relatório v3 em blocos, a evidência,
# a árvore de decisão e os eventos, e o que mudou entre duas iterações), o conversor de Markdown da página (`hub_pagina.md_para_html`) e a
# revisão (`hub_revisao.py`: comentário preso a um trecho, conversas com estado, veredito de cinco valores com os rascunhos gravados juntos, os
# campos severidade, prioridade e estado da seção 5.5 do syllabus CTFL 4.0, a sugestão "a causa é outra" e a marca de lido). Os testes foram
# escritos ANTES dos módulos: a primeira rodada falha por ModuleNotFoundError em `hub_dados`, o RED aceito para módulo novo.
# ! Motivo: o plano aprovado da Pós-Fase 4 (seções 3.6 e 7, Q6) e a ficha 97 (decisão 157) pedem os testes antes do código. Três promessas do
# desenho só ficam de pé com teste: o hub não escreve nas pastas das corridas (os registros oficiais nunca são regravados), o agente não consegue
# dar veredito nem preencher a 5.5 (plano, princípio 4: a IA nunca aprova sozinha), e nenhum caminho de arquivo vindo do navegador chega ao
# disco (o texto das respostas das cobaias entra na página, então o conversor de Markdown também é testado contra marcação HTML no conteúdo).
"""Testes do hub central (Pós-Fase 4, pacote Q6), sem pytest (asserts em Python puro). Uso (em Programacao/AgenteCore/experimentos):
  PYTHONIOENCODING=utf-8 python testar_hub.py
"""
import argparse
import contextlib
import http.client
import http.server
import inspect
import io
import json
import os
import re
import shutil
import sys
import threading
import time
import traceback
import urllib.parse
import zipfile
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    with contextlib.suppress(OSError, ValueError, AttributeError):
        sys.stdout.reconfigure(encoding="utf-8")

EXP = Path(__file__).resolve().parent
RA = EXP / "resultados_alvo"
if str(EXP) not in sys.path:
    sys.path.insert(0, str(EXP))

import gerar_relatorio_raciocinio as grr
import hub
import hub_dados as hd
import hub_pagina as hp
import hub_revisao as hr
import navegador
import taxonomia
import testar_pos_fase4 as tp4
import trilha

_TEMPORARIOS = tp4._TEMPORARIOS
ANALISTA = {"nome": "revisor de teste", "papel": "analista"}
AGENTE = {"nome": "agente (qwen2.5:7b)", "papel": "agente"}
IT1 = {"tid": "c1/qwen2.5_7b/lex-1@tela", "hash": "aaaa1111", "numero": 1}
IT2 = {"tid": "c2/qwen2.5_7b/lex-1@tela", "hash": "bbbb2222", "numero": 2}


def _erro(funcao, *args, tipo=ValueError, **kwargs) -> str:
    """Chama a função e devolve a mensagem do erro esperado; falha se ela não recusar."""
    try:
        funcao(*args, **kwargs)
    except tipo as e:
        return str(e)
    raise AssertionError(f"{getattr(funcao, '__name__', funcao)} devia recusar {args} {kwargs}")


def _trilhas_com_decisao(pasta: Path) -> list[str]:
    """Contagem independente do hub: os ids das trilhas com nó de decisão no arquivo de trilha da corrida."""
    modo = json.loads((pasta / "condicoes_fase4.json").read_text(encoding="utf-8"))["modo"]
    eventos = trilha.ler(pasta / f"trilha_{modo}.jsonl")
    return [tid for tid, seq in trilha.por_trilha(eventos).items() if tid and any(e["tipo"] == "decisao" for e in seq)]


def _retrato(pastas: list[Path]) -> dict:
    """O nome, o tamanho e a hora de modificação de cada arquivo das pastas, para provar que nada foi escrito nelas."""
    return {str(a): (a.stat().st_size, a.stat().st_mtime_ns) for p in pastas for a in sorted(p.rglob("*")) if a.is_file()}


def _acervo_de_teste() -> tuple["hd.Acervo", Path]:
    """Duas corridas de mentira com o mesmo caso `lex-1`: na primeira o agente respondeu `resposta_truncada` com confiança alta; na segunda,
    feita depois, respondeu `corpo_nao_e_json` com confiança média. A segunda corrida tem também o caso `lex-4`."""
    raiz = tp4._temp()
    for nome, inicio, casos in (("c1", "2026-11-06T09:53:30", [("lex-1", "alto", 0.9989, tp4.RESPOSTA_TELA, None)]),
                                ("c2", "2026-11-07T10:00:00", [("lex-1", "medio", 0.9, tp4.RESPOSTA_TEXTO, "corpo_nao_e_json"), ("lex-4", "alto", 0.995, tp4.RESPOSTA_TELA, None)])):
        pasta = raiz / nome
        pasta.mkdir()
        t = trilha.Trilha(versao=trilha.V2)
        cab = tp4._cabecalho(nome, "tela")
        cab["inicio"] = inicio
        t.corrida(cab, ts=inicio)
        for caso, selo, p, resposta, escolha in casos:
            tid = tp4._caso_na_tela(t, nome, caso, selo, p, resposta)
            if escolha:     # o ajudante da tela grava sempre `resposta_truncada` no nó; aqui a segunda corrida responde outra causa
                for e in t.eventos:
                    if e.get("trilha") == tid and e["tipo"] == "decisao":
                        e["dados"]["escolha"] = escolha
        for e in t.eventos:
            if e.get("trilha"):
                e["ts"] = inicio[:11] + "10:05:00"
        t.fechar(fim=inicio[:11] + "11:00:00")
        t.gravar(pasta / "trilha_tela.jsonl")
        (pasta / "condicoes_fase4.json").write_text(json.dumps({"modo": "tela", "saida": nome, "k": 3, "modelo": "qwen2.5:7b"}), encoding="utf-8")
    return hd.Acervo(raiz, corridas=("c1", "c2"), leituras=tp4._leituras_de_teste(), descobrir=False), raiz


# ------------------------------------------------------------------ etapa 1: os dados do hub

def teste_hub_chave_do_caso_tira_a_repeticao_e_a_origem():
    assert hd.chave_do_caso("fase5_agente_b/qwen2.5_7b/contrato-field_missing#2") == "contrato-field_missing"
    assert hd.chave_do_caso("fase4_tela_v4/qwen2.5_7b/lex-1@tela") == "lex-1" and hd.chave_do_caso("fase4_tela_v4/qwen2.5_7b/lex-1@fixture") == "lex-1"
    assert hd.chave_do_caso("fase4_ineditos/qwen2.5_7b/lex-22") == "lex-22"


def teste_hub_acervo_lista_as_corridas_padrao_e_todo_caso_com_diagnostico():
    acervo = hd.Acervo(RA, descobrir=False)
    corridas = acervo.corridas()
    assert [c["pasta"] for c in corridas] == [c["pasta"] for c in hd.CORRIDAS_PADRAO] == ["fase4_tela_v4", "fase4_ensaio_v4", "fase4_ineditos", "fase5_agente_b"]
    indice = acervo.indice()
    for c in corridas:
        esperados = _trilhas_com_decisao(RA / c["pasta"])
        do_hub = [linha["tid"] for linha in indice if linha["corrida"] == c["pasta"]]
        assert sorted(do_hub) == sorted(esperados) and c["casos"] == len(esperados), (c["pasta"], len(do_hub), len(esperados))
        assert c["rotulo"] and c["modelo"] and c["inicio"], c
    assert len({linha["tid"] for linha in indice}) == len(indice), "cada trilha aparece uma vez"
    for linha in indice:
        assert linha["titulo"] and linha["caso"] == hd.chave_do_caso(linha["tid"]) and linha["hash"] and linha["ts"], linha
        assert 1 <= linha["iteracao"] <= linha["iteracoes"], linha
        assert linha["confianca"] in ("alta", "média", "baixa", "desconhecida"), linha
        assert isinstance(linha["divergencia"], bool) and isinstance(linha["cura"], bool), linha


def teste_hub_iteracoes_do_mesmo_caso_saem_em_ordem_de_tempo():
    acervo = hd.Acervo(RA, descobrir=False)
    its = acervo.iteracoes("contrato-field_missing")
    esperadas = [t for pasta in ("fase4_ensaio_v4", "fase5_agente_b") for t in _trilhas_com_decisao(RA / pasta) if hd.chave_do_caso(t) == "contrato-field_missing"]
    assert sorted(i["tid"] for i in its) == sorted(esperadas) and len(its) >= 2, its
    assert [i["numero"] for i in its] == list(range(1, len(its) + 1)) and [i["ts"] for i in its] == sorted(i["ts"] for i in its), its
    assert its[0]["corrida"] == "fase4_ensaio_v4" and its[-1]["corrida"] == "fase5_agente_b", "a corrida 21d veio antes da 28b"
    do_lex = acervo.iteracoes("lex-1")
    assert [i["tid"].rsplit("/", 1)[-1] for i in do_lex] == ["lex-1@tela", "lex-1@fixture"], do_lex
    assert acervo.iteracoes("caso-que-nao-existe") == []


def teste_hub_caso_traz_o_relatorio_em_blocos_a_evidencia_a_arvore_e_a_trilha():
    acervo = hd.Acervo(RA, descobrir=False)
    tid = "fase5_agente_b/qwen2.5_7b/contrato-field_missing#1"
    caso = acervo.caso(tid)
    blocos = caso["relatorio"]["blocos"]
    assert [b["titulo"] for b in blocos] == list(grr.CAMPOS_55 + grr.SECOES_MANTIDAS_V3), [b["titulo"] for b in blocos]
    assert len({b["id"] for b in blocos}) == len(blocos) and all(b["html"].strip() and b["texto"].strip() and b["numero"] == n for n, b in enumerate(blocos, 1))
    assert [b["grupo"] for b in blocos] == ["5.5"] * len(grr.CAMPOS_55) + ["agente"] * len(grr.SECOES_MANTIDAS_V3)
    eventos = trilha.ler(RA / "fase5_agente_b" / "trilha_cenarios.jsonl")
    v3 = grr.relatorio_do_caso_v3(eventos, tid, pasta_blobs=RA / "fase5_agente_b" / "blobs", leituras=acervo.leituras, arquivo_trilha="trilha_cenarios.jsonl",
                                  comando_reexecucao=grr.comando_de_reexecucao("cenarios", "fase5_agente_b", tid, 3),
                                  relatorio_v2="../relatorios/contrato-field_missing__r1.md")
    for b in blocos:
        assert b["markdown"] in v3, f"o bloco {b['titulo']} é um trecho do relatório v3, sem reescrita"
    ev = {e["id"]: e for e in caso["evidencia"]}
    assert {"resposta", "tela", "contrato", "verbetes", "texto_do_modelo"} <= set(ev), sorted(ev)
    assert "GET /api/produtos" in ev["resposta"]["nota"] and "200" in ev["resposta"]["nota"] and "Picanha" in ev["resposta"]["texto"], ev["resposta"]["nota"]
    assert ev["tela"]["texto"].startswith("document ") and "preco: " in ev["contrato"]["texto"]
    assert "campo_ausente" in json.dumps(ev["verbetes"], ensure_ascii=False) and "CAUSA_RAIZ: campo_ausente" in ev["texto_do_modelo"]["texto"]
    assert ev["texto_do_modelo"]["rotulo"] == "texto do modelo", "o que o modelo escreveu vem rotulado (plano, princípio 3)"
    assert [d["chave"] for d in caso["arvore"]["decisoes"]] == ["leitura", "verbetes", "causa"] and caso["arvore"]["eventos"]["hash"] == caso["hash"]
    do_arquivo = [e for e in eventos if e.get("trilha") == tid]
    assert [e["seq"] for e in caso["trilha"]] == [e["seq"] for e in do_arquivo] and all(e["resumo"] for e in caso["trilha"])
    assert {"tipo", "ts", "origem", "pai", "dados"} <= set(caso["trilha"][0])
    agente = caso["comentario_do_agente"]
    assert agente["autor"]["papel"] == "agente" and agente["veredito"] == "comentar" and "campo_ausente" in agente["texto"], agente
    assert caso["caso"] == "contrato-field_missing" and caso["iteracao"] == 2 and len(caso["iteracoes"]) == len(acervo.iteracoes("contrato-field_missing"))
    assert caso["titulo"] and caso["corrida"]["pasta"] == "fase5_agente_b" and caso["trace"] == {"existe": False, "arquivo": None}


def teste_hub_caso_com_cura_traz_a_quarta_decisao_e_caso_de_texto_nao_inventa_tela():
    acervo = hd.Acervo(RA, descobrir=False)
    cura = acervo.caso("fase5_agente_b/qwen2.5_7b/localizador-front-busca#1")
    assert [d["chave"] for d in cura["arvore"]["decisoes"]] == ["leitura", "verbetes", "causa", "cura"] and cura["resumo"]["cura"] is True
    texto = acervo.caso("fase4_ineditos/qwen2.5_7b/lex-22")
    ids = [e["id"] for e in texto["evidencia"]]
    assert "tela" not in ids and {"resposta", "contrato", "texto_do_modelo"} <= set(ids), ids


def teste_hub_tid_desconhecido_ou_com_caminho_e_recusado():
    acervo = hd.Acervo(RA, descobrir=False)
    for ruim in ("../../Windows/win.ini", "fase4_ineditos/../../x", "fase4_ineditos/qwen2.5_7b/nao-existe", "", "C:\\Windows\\win.ini", "fase4_fumaca_progresso/qwen2.5_7b/lex-22"):
        _erro(acervo.caso, ruim, tipo=KeyError)
    _erro(hd.Acervo, RA, corridas=("../fora",))
    _erro(hd.Acervo, RA, corridas=("nao_existe_esta_corrida",))
    _, raiz = _acervo_de_teste()
    (raiz / "sub").mkdir()
    assert "nome de pasta" in _erro(hd.Acervo, raiz / "sub", corridas=("../c1",)), "uma corrida de verdade, mas fora da raiz do hub, também é recusada"


def teste_hub_nao_escreve_nas_pastas_das_corridas():
    pastas = [RA / c["pasta"] for c in hd.CORRIDAS_PADRAO]
    antes = _retrato(pastas)
    acervo = hd.Acervo(RA, descobrir=False)
    for linha in acervo.indice():
        acervo.caso(linha["tid"])
    assert _retrato(pastas) == antes, "o hub só lê: nenhum arquivo novo, apagado ou alterado nas pastas das corridas"


def teste_hub_o_que_mudou_entre_duas_iteracoes_do_mesmo_caso():
    acervo, _ = _acervo_de_teste()
    its = acervo.iteracoes("lex-1")
    assert [i["corrida"] for i in its] == ["c1", "c2"] and [i["numero"] for i in its] == [1, 2], its
    mud = {m["campo"]: m for m in acervo.mudancas(its[0]["tid"], its[1]["tid"])}
    assert mud["causa respondida"]["antes"] == "resposta_truncada" and mud["causa respondida"]["depois"] == "corpo_nao_e_json", mud
    assert mud["confiança"]["antes"] == "alta" and mud["confiança"]["depois"] == "média", mud
    assert "corrida" in mud and mud["corrida"]["antes"] == "c1" and mud["corrida"]["depois"] == "c2"
    assert acervo.mudancas(its[0]["tid"], its[0]["tid"]) == [], "a mesma iteração não mudou nada"
    caso2 = acervo.caso(its[1]["tid"])
    assert caso2["iteracao"] == 2 and [m["campo"] for m in caso2["mudancas_desde_a_anterior"]] == list(mud), caso2["mudancas_desde_a_anterior"]
    assert acervo.caso(its[0]["tid"])["mudancas_desde_a_anterior"] == []
    assert acervo.caso(acervo.iteracoes("lex-4")[0]["tid"])["iteracoes"][0]["numero"] == 1


def teste_hub_acervo_enxerga_caso_novo_quando_a_trilha_cresce():
    acervo, raiz = _acervo_de_teste()
    assert len(acervo.indice()) == 3
    t = trilha.Trilha.carregar(raiz / "c2" / "trilha_tela.jsonl")
    tp4._caso_na_tela(t, "c2", "lex-7", "baixo", 0.5, tp4.RESPOSTA_TELA)
    t.gravar(raiz / "c2" / "trilha_tela.jsonl")
    assert sorted(linha["caso"] for linha in acervo.indice()) == ["lex-1", "lex-1", "lex-4", "lex-7"], "uma corrida em andamento aparece sem reabrir o hub"


# ------------------------------------------------------------------ etapa 1: o Markdown da página

def teste_hub_markdown_vira_html_sem_deixar_passar_marcacao_do_conteudo():
    md = "\n".join(["Texto com `codigo <b>` e **negrito** e <script>alert(1)</script>.", "",  # noqa: FLY002 - uma linha de Markdown por item, como no arquivo
                    "| Campo | Valor |", "|---|---|", "| `preco` | <img src=x onerror=alert(1)> |", "",
                    "- item um", "  - sub item", "- item dois", "",
                    "1. primeiro", "2. segundo", "",
                    "> citação do <caso>", "",
                    "```json", '{"a": "<x>"}', "```", "",
                    "[fora](https://exemplo.org/a) e [dentro](../relatorios/lex-1.md) e [mau](javascript:alert(1))"])
    h = hp.md_para_html(md)
    assert "<script>" not in h and "<img" not in h and "onerror=alert(1)&gt;" in h and "&lt;script&gt;alert(1)&lt;/script&gt;" in h, h
    assert "<code>codigo &lt;b&gt;</code>" in h and "<strong>negrito</strong>" in h
    assert "<table>" in h and "<th>Campo</th>" in h and "<td><code>preco</code></td>" in h
    assert "<ul><li>item um<ul><li>sub item</li></ul></li><li>item dois</li></ul>" in h.replace("\n", "")
    assert "<ol><li>primeiro</li><li>segundo</li></ol>" in h.replace("\n", "")
    assert "<blockquote>" in h and "citação do &lt;caso&gt;" in h
    assert '<pre><code>{&quot;a&quot;: &quot;&lt;x&gt;&quot;}</code></pre>' in h or "<pre><code>{\"a\": \"&lt;x&gt;\"}</code></pre>" in h, h
    assert '<a href="https://exemplo.org/a" target="_blank" rel="noopener noreferrer">fora</a>' in h
    assert 'href="javascript' not in h and 'href="../relatorios' not in h and "dentro" in h, "só endereço http(s) vira link; o resto fica como texto"
    assert hp.md_para_html("<!-- comentário de IA -->\n\n## Título\n\ntexto") == "<h2>Título</h2>\n<p>texto</p>"


# ------------------------------------------------------------------ etapa 1: a revisão

def _revisoes() -> "hr.Revisoes":
    return hr.Revisoes(tp4._temp() / "revisoes")


def _comentar(rev, caso="lex-1", texto="Este trecho não bate com o contrato.", conversa=None, ancora=None, autor=ANALISTA, iteracao=IT1, **extras) -> dict:
    return rev.registrar(caso, {"tipo": "comentario", "autor": autor, "iteracao": iteracao, "texto": texto, "conversa": conversa, "ancora": ancora, **extras})


def teste_revisao_comentario_preso_a_um_trecho_abre_conversa_e_a_resposta_entra_nela():
    rev = _revisoes()
    ancora = {"bloco": "b12-veredito-do-agente", "trecho": "resposta truncada", "inicio": 10, "fim": 27}
    c1 = _comentar(rev, ancora=ancora, rotulo="problema", bloqueante=True)
    c2 = _comentar(rev, texto="Concordo, o corpo veio cortado.", conversa=c1["conversa"])
    geral = _comentar(rev, texto="Comentário geral da revisão.")
    assert c1["id"] != c2["id"] and c1["conversa"] == c2["conversa"] != geral["conversa"] and c1["ts"]
    e = hr.estado(rev.eventos("lex-1"), [IT1])
    assert [len(c["comentarios"]) for c in e["conversas"]] == [2, 1] and e["conversas"][0]["ancora"] == ancora and e["conversas"][1]["ancora"] is None
    assert e["conversas"][0]["estado"] == "ativa" and e["conversas"][0]["comentarios"][0]["rotulo"] == "problema" and e["conversas"][0]["comentarios"][0]["bloqueante"] is True
    assert e["conversas"][0]["comentarios"][1]["autor"] == ANALISTA and e["contagem"] == {"conversas": 2, "ativas": 2, "resolvidas": 0, "nao_serao_tratadas": 0, "comentarios": 3}
    assert "conversa" in _erro(_comentar, rev, conversa="nao-existe") and "texto" in _erro(_comentar, rev, texto="   ")
    _erro(_comentar, rev, ancora={"bloco": "b1", "trecho": "", "inicio": 0, "fim": 0})
    _erro(_comentar, rev, ancora={"bloco": "b1", "trecho": "x", "inicio": 5, "fim": 2})
    _erro(_comentar, rev, conversa=c1["conversa"], ancora=ancora)   # a âncora é de quem abre a conversa, não de uma resposta
    _erro(_comentar, rev, rotulo="rotulo-que-nao-existe")
    _erro(_comentar, rev, autor={"nome": "", "papel": "analista"})
    _erro(_comentar, rev, autor={"nome": "x", "papel": "gerente"})


def teste_revisao_estado_da_conversa_muda_e_o_historico_fica():
    rev = _revisoes()
    c = _comentar(rev)
    for estado in ("resolvida", "nao_sera_tratada", "ativa", "resolvida"):
        rev.registrar("lex-1", {"tipo": "estado_da_conversa", "autor": ANALISTA, "iteracao": IT1, "conversa": c["conversa"], "estado": estado})
    e = hr.estado(rev.eventos("lex-1"), [IT1])
    assert e["conversas"][0]["estado"] == "resolvida" and [h["estado"] for h in e["conversas"][0]["historico"]] == ["resolvida", "nao_sera_tratada", "ativa", "resolvida"]
    assert e["contagem"]["resolvidas"] == 1 and e["contagem"]["ativas"] == 0
    assert tuple(hr.ESTADOS_DA_CONVERSA) == ("ativa", "resolvida", "nao_sera_tratada")
    _erro(rev.registrar, "lex-1", {"tipo": "estado_da_conversa", "autor": ANALISTA, "iteracao": IT1, "conversa": c["conversa"], "estado": "fechada"})
    _erro(rev.registrar, "lex-1", {"tipo": "estado_da_conversa", "autor": ANALISTA, "iteracao": IT1, "conversa": "outra", "estado": "resolvida"})
    _erro(rev.registrar, "lex-1", {"tipo": "tipo_que_nao_existe", "autor": ANALISTA, "iteracao": IT1})


def teste_revisao_enviada_grava_os_rascunhos_e_o_veredito_de_uma_vez():
    rev = _revisoes()
    rascunhos = [{"texto": "O campo certo é `preco`.", "ancora": {"bloco": "b13-evidencia", "trecho": "preco", "inicio": 3, "fim": 8}, "rotulo": "sugestao", "bloqueante": False},
                 {"texto": "Falta dizer o impacto para o cliente.", "ancora": None}]
    gravados = rev.enviar_revisao("lex-1", autor=ANALISTA, iteracao=IT1, veredito="aprovar_com_sugestoes", resumo="Causa certa, texto a melhorar.",
                                  desfecho="diagnostico_correto", rascunhos=rascunhos, campos_55={"severidade": "alta", "prioridade": "média", "estado": "aguardando correção"},
                                  causa_sugerida=None)
    assert [g["tipo"] for g in gravados] == ["comentario", "comentario", "campos_55", "veredito"] and len({g["revisao"] for g in gravados}) == 1, gravados
    assert rev.eventos("lex-1") == gravados
    e = hr.estado(rev.eventos("lex-1"), [IT1])
    assert e["veredito_atual"]["veredito"] == "aprovar_com_sugestoes" and e["veredito_atual"]["resumo"] == "Causa certa, texto a melhorar." and e["veredito_atual"]["desfecho"] == "diagnostico_correto"
    assert e["veredito_vale_para_a_iteracao_atual"] is True and len(e["conversas"]) == 2 and e["campos_55"] == {"severidade": "alta", "prioridade": "média", "estado": "aguardando correção"}
    assert tuple(hr.VEREDITOS) == ("aprovar", "aprovar_com_sugestoes", "aguardar_autor", "rejeitar", "comentar"), "os cinco valores do Azure DevOps mais o comentar"
    antes = rev.arquivo("lex-1").read_bytes()
    _erro(rev.enviar_revisao, "lex-1", autor=ANALISTA, iteracao=IT1, veredito="aprovar", resumo="", rascunhos=[{"texto": "bom", "ancora": None}, {"texto": "  ", "ancora": None}])
    assert rev.arquivo("lex-1").read_bytes() == antes, "um rascunho inválido não deixa gravar nada da revisão"
    assert hr.estado(rev.eventos("lex-1"), [IT1, IT2])["veredito_vale_para_a_iteracao_atual"] is False, "o veredito foi dado na iteração 1; a 2 chegou depois"


def teste_revisao_a_ia_nunca_aprova_sozinha():
    rev = _revisoes()
    for veredito in ("aprovar", "aprovar_com_sugestoes", "aguardar_autor", "rejeitar"):
        msg = _erro(rev.registrar, "lex-1", {"tipo": "veredito", "autor": AGENTE, "iteracao": IT1, "veredito": veredito, "resumo": "x"})
        assert "agente" in msg and "comenta" in msg, msg
    _erro(rev.enviar_revisao, "lex-1", autor=AGENTE, iteracao=IT1, veredito="aprovar", resumo="x")
    _erro(rev.registrar, "lex-1", {"tipo": "campos_55", "autor": AGENTE, "iteracao": IT1, "severidade": "alta", "prioridade": "alta", "estado": "aberto"})
    _erro(rev.registrar, "lex-1", {"tipo": "causa_sugerida", "autor": AGENTE, "iteracao": IT1, "causa": "campo_ausente"})
    _erro(rev.registrar, "lex-1", {"tipo": "estado_da_conversa", "autor": AGENTE, "iteracao": IT1, "conversa": "c1", "estado": "resolvida"})
    assert not rev.arquivo("lex-1").exists(), "nada do que foi recusado chegou ao disco"
    ok = rev.registrar("lex-1", {"tipo": "veredito", "autor": AGENTE, "iteracao": IT1, "veredito": "comentar", "resumo": "Causa provável: campo ausente."})
    assert ok["veredito"] == "comentar" and _comentar(rev, autor=AGENTE)["autor"] == AGENTE, "o agente pode comentar"


def teste_revisao_campos_da_5_5_so_aceitam_os_valores_declarados():
    rev = _revisoes()
    assert hr.estado([], [IT1])["campos_55"] == {"severidade": None, "prioridade": None, "estado": "aberto"}, "o estado inicial é dado pelo código; severidade e prioridade ficam em branco"
    assert tuple(hr.ESTADOS_55) == ("aberto", "adiado", "duplicado", "aguardando correção", "aguardando teste de confirmação", "reaberto", "fechado", "rejeitado"), \
        "os exemplos de estado da seção 5.5 do syllabus CTFL 4.0, na tradução do BSTQB"
    rev.registrar("lex-1", {"tipo": "campos_55", "autor": ANALISTA, "iteracao": IT1, "severidade": "crítica", "prioridade": "alta", "estado": "reaberto"})
    rev.registrar("lex-1", {"tipo": "campos_55", "autor": ANALISTA, "iteracao": IT1, "severidade": None, "prioridade": "baixa", "estado": "fechado"})
    assert hr.estado(rev.eventos("lex-1"), [IT1])["campos_55"] == {"severidade": None, "prioridade": "baixa", "estado": "fechado"}
    for ruim in ({"severidade": "gravíssima", "prioridade": "alta", "estado": "aberto"}, {"severidade": "alta", "prioridade": "urgente", "estado": "aberto"},
                 {"severidade": "alta", "prioridade": "alta", "estado": "em análise"}, {"severidade": "alta", "prioridade": "alta"}):
        _erro(rev.registrar, "lex-1", {"tipo": "campos_55", "autor": ANALISTA, "iteracao": IT1, **ruim})


def teste_revisao_a_causa_e_outra_so_aceita_causa_da_lista_e_guarda_quem_sugeriu():
    rev = _revisoes()
    rev.registrar("lex-1", {"tipo": "causa_sugerida", "autor": ANALISTA, "iteracao": IT1, "causa": "campo_renomeado", "campo": "preco", "texto": "O campo veio como `valor`."})
    s = hr.estado(rev.eventos("lex-1"), [IT1])["causa_sugerida"]
    assert s["causa"] == "campo_renomeado" and s["campo"] == "preco" and s["autor"] == ANALISTA and s["iteracao"] == IT1 and s["ts"], s
    assert set(hr.CAUSAS) == set(taxonomia.CAUSAS_RAIZ)
    _erro(rev.registrar, "lex-1", {"tipo": "causa_sugerida", "autor": ANALISTA, "iteracao": IT1, "causa": "causa_inventada"})
    assert hr.estado([], [IT1])["causa_sugerida"] is None


def teste_revisao_rejeitar_pede_o_motivo_e_o_desfecho_tem_lista_fechada():
    rev = _revisoes()
    assert "motivo" in _erro(rev.registrar, "lex-1", {"tipo": "veredito", "autor": ANALISTA, "iteracao": IT1, "veredito": "rejeitar", "resumo": " "})
    ok = rev.registrar("lex-1", {"tipo": "veredito", "autor": ANALISTA, "iteracao": IT1, "veredito": "rejeitar", "resumo": "A causa é outra.", "desfecho": "agente_errou"})
    assert ok["desfecho"] == "agente_errou" and set(hr.DESFECHOS) == {"diagnostico_correto", "agente_errou", "decisao_intencional"}
    _erro(rev.registrar, "lex-1", {"tipo": "veredito", "autor": ANALISTA, "iteracao": IT1, "veredito": "aprovar", "resumo": "", "desfecho": "outro"})
    _erro(rev.registrar, "lex-1", {"tipo": "veredito", "autor": ANALISTA, "iteracao": IT1, "veredito": "talvez", "resumo": ""})


def teste_revisao_marca_de_lido_cai_quando_chega_iteracao_nova():
    rev = _revisoes()
    assert hr.estado([], [IT1])["lido"] is None and hr.estado([], [IT1])["lido_valido"] is False
    rev.registrar("lex-1", {"tipo": "lido", "autor": ANALISTA, "iteracao": IT1})
    e1 = hr.estado(rev.eventos("lex-1"), [IT1])
    assert e1["lido"]["hash"] == IT1["hash"] and e1["lido_valido"] is True and e1["iteracoes_novas_desde_o_lido"] == 0
    e2 = hr.estado(rev.eventos("lex-1"), [IT1, IT2])
    assert e2["lido_valido"] is False and e2["iteracoes_novas_desde_o_lido"] == 1, "a marca vale para a iteração lida; a nova pede outra leitura"
    refeita = hr.estado(rev.eventos("lex-1"), [{**IT1, "hash": "cccc3333"}])
    assert refeita["lido_valido"] is False, "os mesmos eventos regravados com outro conteúdo também derrubam a marca"
    rev.registrar("lex-1", {"tipo": "lido", "autor": ANALISTA, "iteracao": IT2})
    assert hr.estado(rev.eventos("lex-1"), [IT1, IT2])["lido_valido"] is True


def teste_revisao_conversa_aberta_em_iteracao_anterior_fica_marcada():
    rev = _revisoes()
    _comentar(rev, iteracao=IT1)
    _comentar(rev, iteracao=IT2, texto="Na segunda rodada a causa mudou.")
    e = hr.estado(rev.eventos("lex-1"), [IT1, IT2])
    assert [c["de_iteracao_anterior"] for c in e["conversas"]] == [True, False] and [c["iteracao"]["numero"] for c in e["conversas"]] == [1, 2]
    _erro(_comentar, rev, iteracao={"tid": "x"})
    _erro(_comentar, rev, iteracao=None)


def teste_revisao_arquivo_so_cresce_e_nome_de_caso_com_caminho_e_recusado():
    rev = _revisoes()
    _comentar(rev)
    primeiro = rev.arquivo("lex-1").read_bytes()
    _comentar(rev, texto="segundo")
    rev.registrar("lex-1", {"tipo": "lido", "autor": ANALISTA, "iteracao": IT1})
    depois = rev.arquivo("lex-1").read_bytes()
    assert depois.startswith(primeiro) and len(depois.splitlines()) == 3, "cada evento é uma linha acrescentada; nada é reescrito"
    assert [json.loads(l)["id"] for l in depois.decode("utf-8").splitlines()] == [e["id"] for e in rev.eventos("lex-1")]
    assert rev.arquivo("contrato-field_missing").name == "contrato-field_missing.jsonl" and rev.arquivo("lex-1").parent == rev.pasta
    for ruim in ("../fora", "a/b", "a\\b", "", ".", "..", "lex 1", "lex-1.jsonl/..", "C:lex", "x" * 200):
        _erro(rev.arquivo, ruim)
        _erro(_comentar, rev, caso=ruim)
    assert rev.eventos("caso-sem-revisao") == [] and sorted(p.name for p in rev.pasta.iterdir()) == ["lex-1.jsonl"]


# ------------------------------------------------------------------ etapa 2: o servidor e a página

# ! Alteração de IA - Revisar: (25/11/2026, pacote Q6, etapa 2) os testes do servidor (`hub.py`) e da página (`hub_pagina.pagina`, `CSS` e `JS`),
# escritos ANTES do código: a primeira rodada falha por ModuleNotFoundError em `hub`. Os do servidor falam HTTP de verdade com um servidor
# subido numa porta livre; os da página abrem o Chromium do Playwright sem janela e fazem o que o analista faz: listar, abrir um caso,
# selecionar um trecho e comentar, responder, resolver, guardar rascunhos, dar o veredito, preencher a 5.5, sugerir outra causa, trocar de
# iteração e recarregar para conferir que ficou gravado. Sem o Playwright instalado (Python do PATH), os testes da página são pulados com aviso.
# ! Motivo: o plano (seção 7, Q6) pede "testes com o navegador headless sobre a página". O texto que vem das cobaias e do modelo entra na
# página, então um dos testes planta marcação HTML no corpo da resposta e no comentário e confere que ela aparece como texto e não roda. O
# servidor só escuta na própria máquina e recusa pedido de gravação que não venha da própria página (endereço de origem trocado ou tipo de
# conteúdo que um formulário de outro site consegue mandar), porque ele grava em disco.
_PULADOS: list[str] = []


# ! Alteração de IA - Revisar: (25/11/2026, ficha 109, decisão 170) os ajudantes deste arquivo passaram a abrir o acervo com `descobrir=False`
# (o de teste e os das quatro corridas oficiais) e o servidor com a sonda dos serviços e a conferência do Ollama de mentira, quando o teste
# não dá as suas.
# ! Motivo: o acervo passou a achar sozinho as pastas `hub_...` das corridas lançadas pelo botão, e a tela "Início" passou a perguntar se o
# site, a API e o Ollama respondem. Os testes daqui falam de corridas fixas (a corrida de mentira copia a trilha de `c2`, com os mesmos
# identificadores, e as contas das corridas oficiais não podem mudar quando alguém rodar os cenários pelo hub nesta máquina), e nenhum teste
# pode bater nas portas de verdade. A descoberta e a tela "Início" têm os testes delas em `testar_central.py`.
@contextlib.contextmanager
def _hub_no_ar(acervo, **opcoes):
    """O servidor do hub numa porta livre, com as revisões numa pasta temporária; devolve o endereço, as revisões e o servidor."""
    rev = hr.Revisoes(tp4._temp() / "revisoes")
    opcoes = {"sonda": lambda porta: False, "ollama_no_ar": lambda: False, "garantir_ollama": lambda: None, **opcoes}
    srv = hub.criar_servidor(acervo, rev, porta=0, **opcoes)
    fio = threading.Thread(target=srv.serve_forever, daemon=True)
    fio.start()
    try:
        yield f"http://127.0.0.1:{srv.server_address[1]}", rev, srv
    finally:
        srv.shutdown()
        srv.server_close()
        fio.join(timeout=5)


def _http(base: str, metodo: str, caminho: str, corpo=None, cabecalhos: dict | None = None) -> tuple[int, dict, bytes]:
    porta = int(base.rsplit(":", 1)[1])
    con = http.client.HTTPConnection("127.0.0.1", porta, timeout=20)
    cab = dict(cabecalhos or {})
    dados = None
    if corpo is not None:
        dados = corpo if isinstance(corpo, bytes) else json.dumps(corpo).encode("utf-8")
        cab.setdefault("Content-Type", "application/json")
    try:
        con.request(metodo, caminho, body=dados, headers=cab)
        r = con.getresponse()
        return r.status, {k.lower(): v for k, v in r.getheaders()}, r.read()
    finally:
        con.close()


def _json(base: str, metodo: str, caminho: str, corpo=None, cabecalhos: dict | None = None) -> tuple[int, dict]:
    status, _, bruto = _http(base, metodo, caminho, corpo, cabecalhos)
    return status, json.loads(bruto.decode("utf-8"))


@contextlib.contextmanager
def _navegador():
    """Uma página do Chromium do Playwright, sem janela, e a lista dos erros de script e de console vistos nela; None sem o Playwright."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        nome = inspect.stack()[2].function
        _PULADOS.append(nome)
        print(f"aviso: {nome} pulado (o Playwright não está neste Python; rode com o da venv: ../.venv/Scripts/python.exe testar_hub.py)")
        yield None, None
        return
    with sync_playwright() as pw:
        nav = pw.chromium.launch(headless=True)
        try:
            pagina = nav.new_context(viewport={"width": 1500, "height": 950}).new_page()
            erros: list[str] = []
            pagina.on("pageerror", lambda e: erros.append(f"erro de script: {e}"))
            pagina.on("console", lambda m: erros.append(f"console: {m.text}") if m.type == "error" else None)
            pagina.set_default_timeout(8000)
            yield pagina, erros
        finally:
            nav.close()


def _abrir_caso(pagina, base: str, tid: str, revisor: str | None = "Revisor de Teste") -> None:
    pagina.goto(base + "/")
    pagina.wait_for_selector("#lista-de-casos .item-caso")
    if revisor is not None:
        pagina.fill("#nome-do-revisor", revisor)
    pagina.click(f'#lista-de-casos .item-caso[data-tid="{tid}"]')
    pagina.wait_for_selector(f'#caso[data-tid="{tid}"] section.bloco')


def _esperar_texto(pagina, seletor: str, texto: str) -> None:
    """Espera o elemento trazer o texto. A página só roda script vindo do hub (Content-Security-Policy), e a espera do Playwright por uma
    expressão escrita em texto é barrada por essa regra; a espera por localizador não depende dela."""
    pagina.locator(seletor, has_text=texto).wait_for()


def _selecionar(pagina, seletor: str, trecho: str) -> None:
    """Seleciona `trecho` dentro do elemento, como o arrastar do mouse faria, e solta o botão."""
    achou = pagina.evaluate("""([sel, trecho]) => {
        const raiz = document.querySelector(sel);
        const w = document.createTreeWalker(raiz, NodeFilter.SHOW_TEXT);
        let n;
        while ((n = w.nextNode())) {
            const i = n.data.indexOf(trecho);
            if (i >= 0) {
                const r = document.createRange();
                r.setStart(n, i); r.setEnd(n, i + trecho.length);
                const s = getSelection(); s.removeAllRanges(); s.addRange(r);
                raiz.dispatchEvent(new MouseEvent('mouseup', {bubbles: true}));
                return true;
            }
        }
        return false;
    }""", [seletor, trecho])
    assert achou, f"o trecho {trecho!r} não está num nó de texto de {seletor}"


def _palavra_do_bloco(caso: dict, bloco: str) -> str:
    """Uma palavra só de letras do texto de um bloco do relatório, que serve de trecho a comentar."""
    texto = next(b["texto"] for b in caso["relatorio"]["blocos"] if b["id"] == bloco)
    return re.search(r"[A-Za-zÀ-ú]{8,}", texto).group(0)


def teste_servidor_so_escuta_na_propria_maquina_e_entrega_a_pagina_o_indice_e_o_caso():
    acervo, _ = _acervo_de_teste()
    _erro(hub.criar_servidor, acervo, hr.Revisoes(tp4._temp()), porta=0, endereco="0.0.0.0")
    with _hub_no_ar(acervo) as (base, _, srv):
        assert srv.server_address[0] == "127.0.0.1"
        status, cab, corpo = _http(base, "GET", "/")
        pagina = corpo.decode("utf-8")
        assert status == 200 and cab["content-type"].startswith("text/html") and '<script src="/hub.js"' in pagina and 'href="/hub.css"' in pagina, cab
        assert "default-src 'self'" in cab["content-security-policy"] and "unsafe-inline" not in cab["content-security-policy"], "nenhum script escrito dentro da página roda"
        assert cab["x-content-type-options"] == "nosniff" and "<script>" not in pagina, "a página não traz script embutido"
        assert _http(base, "GET", "/hub.js")[0] == 200 and _http(base, "GET", "/hub.css")[1]["content-type"].startswith("text/css")
        status, indice = _json(base, "GET", "/api/indice")
        assert status == 200 and [c["pasta"] for c in indice["corridas"]] == ["c1", "c2"] and len(indice["casos"]) == 3, indice["corridas"]
        assert set(indice["opcoes"]) >= {"vereditos", "estados_da_conversa", "severidades", "prioridades", "estados_55", "rotulos", "desfechos", "causas"}
        assert indice["opcoes"]["estados_55"] == list(hr.ESTADOS_55) and all("revisao" in c for c in indice["casos"])
        tid = indice["casos"][0]["tid"]
        status, caso = _json(base, "GET", "/api/caso?tid=" + urllib.parse.quote(tid, safe=""))
        assert status == 200 and caso["tid"] == tid and len(caso["relatorio"]["blocos"]) == 17 and caso["revisao"]["campos_55"]["estado"] == "aberto"
        assert "arvore_html" in caso and 'class="origem' in caso["arvore_html"]
        for ruim in ("/api/caso?tid=" + urllib.parse.quote("../../x", safe=""), "/api/caso", "/api/caso?tid=c9/qwen2.5_7b/lex-1@tela", "/nao-existe", "/../hub_dados.py",
                     "/hub_dados.py", "/api/indice/../../hub.py"):
            status, _, corpo = _http(base, "GET", ruim)
            assert status == 404 and b"import " not in corpo, (ruim, status)


def teste_servidor_grava_a_revisao_como_analista_e_recusa_o_que_nao_veio_da_pagina():
    acervo, raiz = _acervo_de_teste()
    antes = _retrato([raiz / "c1", raiz / "c2"])
    with _hub_no_ar(acervo) as (base, rev, _):
        tid = acervo.iteracoes("lex-1")[1]["tid"]
        pedido = {"tid": tid, "acao": "comentar", "autor": {"nome": "Ana", "papel": "agente"}, "texto": "Comentário <b>geral</b>.", "ancora": None,
                  "iteracao": {"tid": "forjada", "hash": "0000", "numero": 9}}
        status, r = _json(base, "POST", "/api/revisao", pedido)
        assert status == 200 and r["revisao"]["contagem"]["comentarios"] == 1, r
        gravado = rev.eventos("lex-1")[0]
        assert gravado["autor"] == {"nome": "Ana", "papel": "analista"}, "o que vem da página é sempre do analista; o agente não escreve pela página"
        assert gravado["iteracao"] == {"tid": tid, "hash": acervo.iteracoes("lex-1")[1]["hash"], "numero": 2}, "a iteração é a do caso aberto, posta pelo servidor"
        status, r = _json(base, "POST", "/api/revisao", {"tid": tid, "acao": "enviar_revisao", "autor": {"nome": "Ana"}, "veredito": "rejeitar", "resumo": "", "rascunhos": []})
        assert status == 400 and "motivo" in r["erro"], r
        status, r = _json(base, "POST", "/api/revisao", {"tid": tid, "acao": "enviar_revisao", "autor": {"nome": "Ana"}, "veredito": "aprovar", "resumo": "ok",
                                                        "rascunhos": [{"texto": "um", "ancora": None}], "campos_55": {"severidade": "baixa", "prioridade": None, "estado": "fechado"},
                                                        "causa_sugerida": {"causa": "campo_ausente", "campo": "preco", "texto": ""}, "desfecho": "agente_errou"})
        assert status == 200 and r["revisao"]["veredito_atual"]["veredito"] == "aprovar" and r["revisao"]["causa_sugerida"]["causa"] == "campo_ausente", r
        assert [e["tipo"] for e in rev.eventos("lex-1")] == ["comentario", "comentario", "campos_55", "causa_sugerida", "veredito"]
        conversa = rev.eventos("lex-1")[0]["conversa"]
        for acao, extra in (("estado_da_conversa", {"conversa": conversa, "estado": "resolvida"}), ("lido", {}),
                            ("campos_55", {"severidade": None, "prioridade": "alta", "estado": "reaberto"}),
                            ("causa_sugerida", {"causa": "campo_renomeado", "campo": None, "texto": "x"}),
                            ("comentar", {"texto": "resposta", "conversa": conversa})):
            status, r = _json(base, "POST", "/api/revisao", {"tid": tid, "acao": acao, "autor": {"nome": "Ana"}, **extra})
            assert status == 200, (acao, r)
        assert r["revisao"]["conversas"][0]["estado"] == "resolvida" and r["revisao"]["lido_valido"] is True and r["revisao"]["campos_55"]["estado"] == "reaberto"
        n = len(rev.eventos("lex-1"))
        ok = {"tid": tid, "acao": "lido", "autor": {"nome": "Ana"}}
        assert _json(base, "POST", "/api/revisao", {**ok, "acao": "apagar_tudo"})[0] == 400
        assert _json(base, "POST", "/api/revisao", {**ok, "tid": "../../x"})[0] == 404
        assert _json(base, "POST", "/api/revisao", {**ok, "autor": {"nome": "  "}})[0] == 400
        assert _http(base, "POST", "/api/revisao", json.dumps(ok).encode(), {"Content-Type": "text/plain"})[0] == 415, "formulário de outro site não manda application/json"
        assert _http(base, "POST", "/api/revisao", ok, {"Host": "outro-site.example"})[0] == 403, "pedido com o nome de outro endereço é recusado"
        assert _http(base, "POST", "/api/revisao", ok, {"Origin": "http://outro-site.example"})[0] == 403
        assert _http(base, "POST", "/api/revisao", b"{nao e json", {"Content-Type": "application/json"})[0] == 400
        assert _http(base, "POST", "/api/revisao", b"[" + b"1," * 700000 + b"1]", {"Content-Type": "application/json"})[0] == 413
        assert _http(base, "POST", "/api/indice", ok)[0] == 404 and _http(base, "PUT", "/api/revisao", ok)[0] == 405 and _http(base, "DELETE", "/api/revisao", ok)[0] == 405
        con = http.client.HTTPConnection("127.0.0.1", int(base.rsplit(":", 1)[1]), timeout=20)     # a mesma conexão, um pedido recusado e depois um bom
        try:
            for esperado, tipo in ((415, "text/plain"), (200, "application/json")):
                con.request("POST", "/api/revisao", body=json.dumps(ok).encode(), headers={"Content-Type": tipo})
                r = con.getresponse()
                r.read()
                assert r.status == esperado, "depois de uma recusa a conexão continua servindo: o corpo recusado foi lido inteiro"
        finally:
            con.close()
        n += 1
        assert len(rev.eventos("lex-1")) == n, "nenhum pedido recusado gravou evento"
        assert sorted(p.name for p in rev.pasta.iterdir()) == ["lex-1.jsonl"]
    assert _retrato([raiz / "c1", raiz / "c2"]) == antes, "a revisão fica na pasta dela; as pastas das corridas não mudam"


def teste_hub_conferir_monta_todos_os_casos_das_corridas_padrao_sem_subir_servidor():
    # ! Alteração de IA - Revisar: (26/11/2026) o teste passa a pedir as quatro corridas padrão pelo nome (`--corridas`).
    # ! Motivo: em 26/11/2026 o Eric rodou os cenários pelo botão do hub, e a pasta `hub_20261126_080944` passou a existir em `resultados_alvo/`; sem
    # `--corridas`, o `--conferir` também conta as corridas lançadas pelo botão (180 casos em 5 corridas), e o teste, que confere as quatro corridas
    # padrão, falhava por causa de uma pasta que não é dele. Com as corridas pedidas pelo nome, a procura das pastas `hub_...` fica desligada.
    saida = io.StringIO()
    with contextlib.redirect_stdout(saida):
        codigo = hub.main(["--conferir", "--corridas", ",".join(c["pasta"] for c in hd.CORRIDAS_PADRAO)])
    texto = saida.getvalue()
    total = sum(len(_trilhas_com_decisao(RA / c["pasta"])) for c in hd.CORRIDAS_PADRAO)
    assert codigo == 0 and f"{total} casos" in texto and "corrida 28b" in texto, texto


def teste_arvore_em_html_traz_cada_afirmacao_com_a_origem_e_o_texto_do_modelo_a_parte():
    acervo = hd.Acervo(RA, descobrir=False)
    arvore = acervo.caso("fase5_agente_b/qwen2.5_7b/localizador-front-busca#1")["arvore"]
    h = hp.arvore_para_html(arvore)
    for rotulo, n in arvore["resumo"]["rotulos"].items():
        assert h.count(f'class="origem origem-{rotulo}"') == n, (rotulo, n)
    assert h.count('<section class="decisao"') == 4 and 'data-decisao="cura"' in h and 'class="texto-do-modelo"' in h and "texto do modelo" in h
    assert "<table>" in h and "<script" not in h


def teste_pagina_lista_os_casos_reais_e_abre_um_caso_com_relatorio_evidencia_arvore_e_trilha():
    with _navegador() as (pagina, erros):
        if pagina is None:
            return
        acervo = hd.Acervo(RA, descobrir=False)
        with _hub_no_ar(acervo) as (base, _, _srv):
            tid = "fase5_agente_b/qwen2.5_7b/contrato-field_missing#1"
            pagina.goto(base + "/")
            pagina.wait_for_selector("#lista-de-casos .item-caso")
            assert pagina.locator("#lista-de-casos .item-caso").count() == len(acervo.indice())
            assert str(len(acervo.indice())) in pagina.inner_text("#contagem-de-casos")
            pagina.select_option("#filtro-corrida", "fase5_agente_b")
            assert pagina.locator("#lista-de-casos .item-caso:visible").count() == len(_trilhas_com_decisao(RA / "fase5_agente_b"))
            pagina.fill("#filtro-texto", "field_missing")
            visiveis = pagina.locator("#lista-de-casos .item-caso:visible")
            assert visiveis.count() == 5 and all("field_missing" in visiveis.nth(i).get_attribute("data-tid") for i in range(5))
            pagina.click(f'#lista-de-casos .item-caso[data-tid="{tid}"]')
            pagina.wait_for_selector(f'#caso[data-tid="{tid}"] section.bloco')
            assert pagina.locator("#aba-relatorio section.bloco").count() == 17
            assert "Veredito do agente" in pagina.inner_text('section.bloco[data-bloco="b12-veredito-do-agente"] h3')
            assert "campo_ausente" in pagina.inner_text("#comentario-do-agente") and "só comenta" in pagina.inner_text("#comentario-do-agente")
            assert "iteração 2 de 6" in pagina.inner_text("#cabecalho-do-caso").lower()
            pagina.click('#evidencia button[data-evidencia="resposta"]')
            assert "Picanha" in pagina.inner_text("#evidencia-conteudo") and "GET /api/produtos" in pagina.inner_text("#evidencia-conteudo")
            pagina.click('#evidencia button[data-evidencia="tela"]')
            assert pagina.inner_text("#evidencia-conteudo").lstrip().startswith("a árvore") or "document " in pagina.inner_text("#evidencia-conteudo")
            pagina.click('#evidencia button[data-evidencia="texto_do_modelo"]')
            assert "CAUSA_RAIZ: campo_ausente" in pagina.inner_text("#evidencia-conteudo") and "texto do modelo" in pagina.inner_text("#evidencia-conteudo")
            pagina.click('button[data-aba="arvore"]')
            assert pagina.locator("#aba-arvore .decisao").count() == 3 and pagina.locator("#aba-arvore .origem").count() > 10 and pagina.is_hidden("#aba-relatorio")
            pagina.click('button[data-aba="trilha"]')
            n_eventos = len(acervo.caso(tid)["trilha"])
            assert pagina.locator("#aba-trilha tr.evento").count() == n_eventos
            pagina.click('#aba-trilha button[data-tipo="decisao"]')
            assert pagina.locator("#aba-trilha tr.evento:visible").count() == 1
            pagina.click("#aba-trilha tr.evento:visible")
            assert '"escolha": "campo_ausente"' in pagina.inner_text("#aba-trilha .detalhe-do-evento:visible")
            pagina.reload()
            pagina.wait_for_selector(f'#caso[data-tid="{tid}"] #aba-trilha tr.evento')
            assert pagina.is_visible("#aba-trilha") and pagina.is_hidden("#aba-relatorio"), "o endereço guarda o caso e a aba: recarregar volta ao mesmo lugar"
        assert erros == [], erros


def teste_pagina_comentario_num_trecho_vira_conversa_com_resposta_e_estado_e_fica_depois_de_recarregar():
    with _navegador() as (pagina, erros):
        if pagina is None:
            return
        acervo, _ = _acervo_de_teste()
        tid = acervo.iteracoes("lex-1")[1]["tid"]
        bloco = "b12-veredito-do-agente"
        palavra = _palavra_do_bloco(acervo.caso(tid), bloco)
        with _hub_no_ar(acervo) as (base, rev, _srv):
            _abrir_caso(pagina, base, tid)
            assert pagina.is_hidden("#comentar-trecho")
            _selecionar(pagina, f'section.bloco[data-bloco="{bloco}"] .conteudo', palavra)
            pagina.click("#comentar-trecho")
            assert palavra in pagina.inner_text("#form-comentario .trecho-citado")
            pagina.fill("#texto-do-comentario", "Isto é <b>texto</b>, não marcação.")
            pagina.select_option("#rotulo-do-comentario", "problema")
            pagina.check("#bloqueante")
            pagina.click("#comentar-agora")
            conversa = pagina.locator(f'section.bloco[data-bloco="{bloco}"] .conversa')
            conversa.wait_for()
            assert "Isto é <b>texto</b>, não marcação." in conversa.inner_text() and conversa.locator("b").count() == 0, "o comentário aparece como texto"
            assert "Revisor de Teste" in conversa.inner_text() and "problema" in conversa.inner_text() and "bloqueante" in conversa.inner_text()
            assert pagina.inner_text(f'section.bloco[data-bloco="{bloco}"] mark.trecho-comentado') == palavra
            conversa.locator("textarea.resposta").fill("Concordo.")
            conversa.locator("button.responder").click()
            pagina.locator(".conversa .comentario").nth(1).wait_for()
            conversa.locator("button.resolver").click()
            pagina.wait_for_selector(f'section.bloco[data-bloco="{bloco}"] .conversa[data-estado="resolvida"]')
            eventos = rev.eventos("lex-1")
            assert [e["tipo"] for e in eventos] == ["comentario", "comentario", "estado_da_conversa"]
            ancora = eventos[0]["ancora"]
            assert ancora["bloco"] == bloco and ancora["trecho"] == palavra and ancora["fim"] - ancora["inicio"] == len(palavra), ancora
            assert eventos[0]["rotulo"] == "problema" and eventos[0]["bloqueante"] is True and eventos[0]["autor"] == {"nome": "Revisor de Teste", "papel": "analista"}
            pagina.reload()
            pagina.wait_for_selector(f'section.bloco[data-bloco="{bloco}"] .conversa[data-estado="resolvida"]')
            assert pagina.locator(".conversa .comentario").count() == 2 and pagina.input_value("#nome-do-revisor") == "Revisor de Teste"
            assert pagina.inner_text(f'section.bloco[data-bloco="{bloco}"] mark.trecho-comentado') == palavra
            pagina.locator(f'section.bloco[data-bloco="{bloco}"] .conversa button.reabrir').click()
            pagina.wait_for_selector(f'section.bloco[data-bloco="{bloco}"] .conversa[data-estado="ativa"]')
            item = pagina.locator(f'#lista-de-casos .item-caso[data-tid="{tid}"]')
            assert "1 conversa ativa" in item.inner_text()
        assert erros == [], erros


def teste_pagina_sem_nome_de_revisor_nao_grava_e_avisa():
    with _navegador() as (pagina, erros):
        if pagina is None:
            return
        acervo, _ = _acervo_de_teste()
        tid = acervo.iteracoes("lex-4")[0]["tid"]
        with _hub_no_ar(acervo) as (base, rev, _srv):
            _abrir_caso(pagina, base, tid, revisor=None)
            pagina.click("#comentar-geral")
            pagina.fill("#texto-do-comentario", "Sem nome.")
            pagina.click("#comentar-agora")
            _esperar_texto(pagina, "#erro", "quem está revisando")
            assert rev.eventos("lex-4") == []
        assert erros == [], erros


def teste_pagina_revisao_com_rascunhos_veredito_campos_da_5_5_e_outra_causa():
    with _navegador() as (pagina, erros):
        if pagina is None:
            return
        acervo, _ = _acervo_de_teste()
        tid = acervo.iteracoes("lex-1")[1]["tid"]
        palavra = _palavra_do_bloco(acervo.caso(tid), "b13-evidencia")
        with _hub_no_ar(acervo) as (base, rev, _srv):
            _abrir_caso(pagina, base, tid)
            _selecionar(pagina, 'section.bloco[data-bloco="b13-evidencia"] .conteudo', palavra)
            pagina.click("#comentar-trecho")
            pagina.fill("#texto-do-comentario", "Rascunho preso ao trecho.")
            pagina.click("#guardar-rascunho")
            pagina.click("#comentar-geral")
            pagina.fill("#texto-do-comentario", "Rascunho geral.")
            pagina.click("#guardar-rascunho")
            assert pagina.locator("#rascunhos .rascunho").count() == 2 and "2" in pagina.inner_text("#enviar-revisao") and rev.eventos("lex-1") == [], "rascunho não vai ao servidor"
            pagina.reload()
            pagina.wait_for_selector(f'#caso[data-tid="{tid}"] section.bloco')
            assert pagina.locator("#rascunhos .rascunho").count() == 2, "o rascunho sobrevive a recarregar a página"
            pagina.select_option("#severidade", "alta")
            pagina.select_option("#prioridade", "média")
            pagina.select_option("#estado-55", "aguardando correção")
            pagina.select_option("#causa-sugerida", "campo_renomeado")
            pagina.fill("#campo-sugerido", "preco")
            pagina.select_option("#desfecho", "agente_errou")
            pagina.select_option("#veredito", "aguardar_autor")
            pagina.fill("#resumo-da-revisao", "A causa é outra: o campo foi renomeado.")
            pagina.click("#enviar-revisao")
            _esperar_texto(pagina, "#veredito-atual", "Aguardar o autor")
            eventos = rev.eventos("lex-1")
            assert [e["tipo"] for e in eventos] == ["comentario", "comentario", "campos_55", "causa_sugerida", "veredito"] and len({e["revisao"] for e in eventos}) == 1
            assert eventos[0]["ancora"]["trecho"] == palavra and eventos[1]["ancora"] is None
            assert {k: eventos[2][k] for k in ("severidade", "prioridade", "estado")} == {"severidade": "alta", "prioridade": "média", "estado": "aguardando correção"}
            assert eventos[3]["causa"] == "campo_renomeado" and eventos[3]["campo"] == "preco" and eventos[4]["desfecho"] == "agente_errou"
            assert pagina.locator("#rascunhos .rascunho").count() == 0 and pagina.locator(".conversa").count() == 2
            assert "campo_renomeado" in pagina.inner_text("#causa-atual") and "Revisor de Teste" in pagina.inner_text("#causa-atual")
            assert "Aguardar o autor" in pagina.inner_text(f'#lista-de-casos .item-caso[data-tid="{tid}"]')
            pagina.reload()
            pagina.wait_for_selector(f'#caso[data-tid="{tid}"] section.bloco')
            assert "Aguardar o autor" in pagina.inner_text("#veredito-atual") and pagina.input_value("#severidade") == "alta" and pagina.input_value("#estado-55") == "aguardando correção"
            pagina.select_option("#veredito", "rejeitar")
            pagina.fill("#resumo-da-revisao", "")
            pagina.click("#enviar-revisao")
            _esperar_texto(pagina, "#erro", "motivo")
            assert len(rev.eventos("lex-1")) == 5, "a recusa do servidor aparece na página e nada é gravado"
            pagina.select_option("#estado-55", "fechado")
            pagina.click("#gravar-55")
            pagina.wait_for_selector("#erro:empty", state="attached")
            _esperar_texto(pagina, "#aviso-55", "gravado")
            assert rev.eventos("lex-1")[-1]["tipo"] == "campos_55" and rev.eventos("lex-1")[-1]["estado"] == "fechado"
        recusa = [e for e in erros if "status of 400" in e]     # o navegador anota no console a recusa (400) do veredito sem motivo, que o teste provocou
        assert len(recusa) == 1 and [e for e in erros if e not in recusa] == [], erros


def teste_pagina_iteracoes_dizem_o_que_mudou_e_a_marca_de_lido_cai_na_iteracao_nova():
    with _navegador() as (pagina, erros):
        if pagina is None:
            return
        acervo, _ = _acervo_de_teste()
        it1, it2 = acervo.iteracoes("lex-1")
        with _hub_no_ar(acervo) as (base, rev, _srv):
            _abrir_caso(pagina, base, it1["tid"])
            assert "iteração 1 de 2" in pagina.inner_text("#cabecalho-do-caso").lower() and "há iteração mais nova" in pagina.inner_text("#aviso-de-iteracao").lower()
            pagina.check("#marca-lido")
            _esperar_texto(pagina, "#aviso-lido", "lida")
            assert rev.eventos("lex-1")[0]["tipo"] == "lido" and rev.eventos("lex-1")[0]["iteracao"]["numero"] == 1
            pagina.select_option("#seletor-de-iteracao", it2["tid"])
            pagina.wait_for_selector(f'#caso[data-tid="{it2["tid"]}"] section.bloco')
            texto = pagina.inner_text("#mudancas")
            assert "causa respondida" in texto and "resposta_truncada" in texto and "corpo_nao_e_json" in texto and "confiança" in texto, texto
            assert not pagina.is_checked("#marca-lido") and "iteração nova" in pagina.inner_text("#aviso-lido"), "a marca era da iteração 1"
            assert "iteração 2 de 2" in pagina.inner_text("#cabecalho-do-caso").lower() and pagina.inner_text("#aviso-de-iteracao").strip() == ""
            pagina.check("#marca-lido")
            _esperar_texto(pagina, "#aviso-lido", "lida")
            assert [e["iteracao"]["numero"] for e in rev.eventos("lex-1")] == [1, 2]
        assert erros == [], erros


def teste_pagina_mostra_como_texto_a_marcacao_que_vier_no_corpo_da_resposta():
    with _navegador() as (pagina, erros):
        if pagina is None:
            return
        acervo, raiz = _acervo_de_teste()
        veneno = '<img src=x onerror="window.__veneno=1"><script>window.__veneno=2</script>'
        arq = raiz / "c2" / "trilha_tela.jsonl"
        arq.write_text(arq.read_text(encoding="utf-8").replace("resposta truncada de propos", veneno.replace('"', '\\\\\\"')).replace(
            "A resposta veio cortada.", veneno.replace('"', '\\\\\\"')), encoding="utf-8", newline="\n")
        tid = acervo.iteracoes("lex-1")[1]["tid"]
        assert "onerror" in json.dumps(acervo.caso(tid)["evidencia"]), "o corpo plantado chegou à evidência"
        with _hub_no_ar(acervo) as (base, _, _srv):
            _abrir_caso(pagina, base, tid)
            for aba in ("resposta", "sintoma"):
                pagina.click(f'#evidencia button[data-evidencia="{aba}"]')
                assert "onerror" in pagina.inner_text("#evidencia-conteudo"), aba
            pagina.click('button[data-aba="trilha"]')
            pagina.click('button[data-aba="arvore"]')
            pagina.click('button[data-aba="relatorio"]')
            pagina.wait_for_timeout(300)
            assert pagina.evaluate("window.__veneno") is None, "nenhuma marcação vinda da cobaia foi executada"
            assert pagina.locator("#caso img").count() == 0 and pagina.locator("#caso script").count() == 0
        assert [e for e in erros if "Content Security Policy" not in e] == [], erros


# ------------------------------------------------------------------ etapa 3: o trace na falha, a corrida ao vivo e os botões

# ! Alteração de IA - Revisar: (25/11/2026, pacote Q6, etapa 3) os testes dos três itens da decisão 93 e dos botões, escritos ANTES do código: a
# primeira rodada falha por AttributeError em `navegador.nome_do_trace`. O trace do Playwright gravado só da página em que o roteiro falhou
# (`navegador.Navegador` com `pasta_dos_traces`, provado numa página local que falha de propósito, sem as cobaias e sem banco) e desligado
# por padrão no executor; o estado da corrida em andamento e o último diagnóstico dela (`hub_dados.AoVivo`, o "Cérebro ao vivo"); a
# execução dos cenários pelo hub, que só dispara quando o servidor é criado com permissão e roda uma corrida por vez (com um lançador de
# mentira, que grava o estado da barra e uma trilha, no lugar do `rodar_fase4.ps1`); e, na página, a vista "Corrida ao vivo", o botão que
# abre a árvore e o atalho para o trace.
# ! Motivo: ficha 45 e decisão 93 (o trace decidido na ficha 33 não tinha sido feito, e o TCC não podia dizer que existia), plano, seção 3.6,
# item 7 (os botões), e ficha 97. O trace muda o tempo de cada passo (o navegador grava tela e estrutura a cada ação), então ele entra
# desligado, para o agente medido nas corridas 18d, 21d e 28b continuar o mesmo; o teste confere que, desligado, a página é aberta como
# antes e que o navegador de mentira dos testes da Fase 4, que só tem `nova_pagina`, continua servindo. A corrida com o modelo não roda
# daqui (regra do projeto): por isso o lançador é uma função que o teste troca.
FALSA_CORRIDA = r'''
import json, shutil, sys, time
from pathlib import Path
pasta, origem, demora = Path(sys.argv[1]), Path(sys.argv[2]), float(sys.argv[3])
pasta.mkdir(parents=True, exist_ok=True)
def estado(e, f):
    (pasta / "progresso.json").write_text(json.dumps({"etapa": "lex-4@tela · diagnóstico", "modelo": "qwen2.5:7b", "estado": e, "fase": "prefill", "fracao": f,
        "decorrido_s": 1.0, "estimativa_s": 2.0, "inferencias_concluidas": 0, "gravado_em": "2026-11-25T10:00:00", "versao": 1}), encoding="utf-8")
estado("determinado", 0.4)
print("corrida de mentira no ar", flush=True)
time.sleep(demora)
shutil.copy(origem / "trilha_tela.jsonl", pasta / "trilha_tela.jsonl")
shutil.copy(origem / "condicoes_fase4.json", pasta / "condicoes_fase4.json")
estado("concluido", 1.0)
print("FIM da corrida de mentira", flush=True)
'''


def _estado_da_barra(pasta: Path, estado: str = "determinado", fracao: float | None = 0.4, etapa: str = "lex-4@tela · diagnóstico", idade_s: float = 0.0) -> Path:
    """Grava um `progresso.json` como `progresso.py` grava, com a hora de modificação `idade_s` segundos atrás."""
    arq = pasta / "progresso.json"
    arq.write_text(json.dumps({"etapa": etapa, "modelo": "qwen2.5:7b", "estado": estado, "fase": "prefill", "tokens_prompt": 1200, "decorrido_s": 20.0, "estimativa_s": 50.0,
                               "fracao": fracao, "inferencias_concluidas": 1, "iniciado_em": "2026-11-25T10:00:00", "gravado_em": "2026-11-25T10:00:20", "versao": 1},
                              ensure_ascii=False), encoding="utf-8")
    quando = time.time() - idade_s
    os.utime(arq, (quando, quando))
    return arq


def _ate(ler, pronto, segundos: float = 10.0):
    """Chama `ler` até `pronto(valor)` ser verdadeiro e devolve o valor lido."""
    def tentar():
        valor = ler()
        return valor if pronto(valor) else None

    return _esperar(tentar, segundos)


def _esperar(condicao, segundos: float = 10.0, passo: float = 0.1):
    """Chama `condicao` até ela devolver algo verdadeiro, ou falha depois de `segundos`."""
    fim = time.monotonic() + segundos
    while time.monotonic() < fim:
        valor = condicao()
        if valor:
            return valor
        time.sleep(passo)
    raise AssertionError("a condição esperada não aconteceu a tempo")


@contextlib.contextmanager
def _site_de_teste():
    """Um site local de duas páginas: `boa.html` tem o botão que o roteiro procura; `quebrada.html` não tem."""
    pasta = tp4._temp()
    (pasta / "boa.html").write_text("<html><head><title>boa</title></head><body><button id='reservar'>Reservar</button></body></html>", encoding="utf-8")
    (pasta / "quebrada.html").write_text("<html><head><title>quebrada</title></head><body><button id='reservar_v2'>Reservar</button></body></html>", encoding="utf-8")

    class Mudo(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *args) -> None:
            pass

    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), lambda *a, **k: Mudo(*a, directory=str(pasta), **k))
    fio = threading.Thread(target=srv.serve_forever, daemon=True)
    fio.start()
    try:
        yield f"http://127.0.0.1:{srv.server_address[1]}"
    finally:
        srv.shutdown()
        srv.server_close()
        fio.join(timeout=5)


def _tem_playwright() -> bool:
    try:
        import playwright.sync_api  # noqa: F401
    except ImportError:
        nome = inspect.stack()[1].function
        _PULADOS.append(nome)
        print(f"aviso: {nome} pulado (o Playwright não está neste Python; rode com o da venv: ../.venv/Scripts/python.exe testar_hub.py)")
        return False
    return True


def teste_trace_o_nome_do_arquivo_e_o_mesmo_do_relatorio_do_caso():
    for tid in ("fase5_agente_b/qwen2.5_7b/contrato-field_missing#2", "fase4_tela_v4/qwen2.5_7b/lex-1@tela", "fase4_ineditos/qwen2.5_7b/lex-22"):
        assert navegador.nome_do_trace(tid) == grr.nome_do_relatorio(tid) + ".zip", tid
    assert hd.PASTA_DOS_TRACES == navegador.PASTA_DOS_TRACES == "traces"


def teste_trace_desligado_o_navegador_abre_a_pagina_como_antes():
    if not _tem_playwright():
        return
    with navegador.Navegador() as nav:
        assert nav.pasta_dos_traces is None
        pagina = nav.nova_pagina()
        assert len(nav.navegador.contexts) == 1 and len(pagina.context.pages) == 1
        assert nav.reter_trace(pagina) is None and nav.gravar_traces("a/b/caso#1") == [] and nav.descartar_traces() == 0
        pagina.close()
        assert nav.navegador.contexts == [], "sem trace, fechar a página fecha o contexto dela, como sempre foi"


def teste_trace_ligado_grava_so_o_da_pagina_em_que_o_roteiro_falhou():
    if not _tem_playwright():
        return
    from playwright.sync_api import TimeoutError as TempoEsgotado
    pasta = tp4._temp() / "corrida" / "traces"
    with _site_de_teste() as site, navegador.Navegador(pasta_dos_traces=pasta) as nav:
        boa = nav.nova_pagina()                        # a corrida de referência: passa, e o trace dela é jogado fora
        boa.goto(site + "/boa.html")
        boa.wait_for_selector("#reservar", timeout=2000)
        boa.close()
        quebrada = nav.nova_pagina()                   # o roteiro do caso: o localizador não resolve
        quebrada.goto(site + "/quebrada.html")
        falhou = False
        try:
            quebrada.wait_for_selector("#reservar", timeout=400)
        except TempoEsgotado:
            falhou = True
        assert falhou
        nav.reter_trace(quebrada)
        quebrada.close()
        assert not pasta.exists(), "nada é gravado antes de o executor dizer de que caso é"
        gravados = nav.gravar_traces("corrida/qwen2.5_7b/localizador-front-cliente-reserva#2")
        assert gravados == [pasta / "localizador-front-cliente-reserva__r2.zip"] and [p.name for p in pasta.iterdir()] == ["localizador-front-cliente-reserva__r2.zip"]
        with zipfile.ZipFile(gravados[0]) as z:
            nomes = z.namelist()
        assert any(n.endswith(".trace") for n in nomes) and any(n.startswith("resources/") for n in nomes), nomes[:5]
        assert nav.navegador.contexts == [], "os contextos das duas páginas foram fechados"
        outra = nav.nova_pagina()                      # um caso em que o roteiro passa: nenhum arquivo novo
        outra.goto(site + "/boa.html")
        outra.close()
        assert nav.gravar_traces("corrida/qwen2.5_7b/caso-que-passou#1") == [] and len(list(pasta.iterdir())) == 1
        retida = nav.nova_pagina()                     # retido e depois descartado (o executor recomeçou o caso): nada gravado
        retida.goto(site + "/quebrada.html")
        nav.reter_trace(retida)
        retida.close()
        assert nav.descartar_traces() == 1 and nav.gravar_traces("corrida/qwen2.5_7b/descartado#1") == [] and len(list(pasta.iterdir())) == 1
        assert nav.navegador.contexts == []


def teste_trace_no_executor_vem_desligado_e_nao_exige_nada_do_navegador_de_mentira():
    import executar_fase4 as ex
    args = ex.montar_parser().parse_args(["--modo", "cenarios", "--saida", "qualquer"])
    assert args.trace_na_falha is False, "desligado por padrão: o agente medido nas corridas 18d, 21d e 28b continua o mesmo"
    pasta = tp4._temp()
    assert ex.navegador_da_corrida(args, pasta).pasta_dos_traces is None
    ligado = ex.montar_parser().parse_args(["--modo", "cenarios", "--saida", "qualquer", "--trace-na-falha"])
    assert ligado.trace_na_falha is True and ex.navegador_da_corrida(ligado, pasta).pasta_dos_traces == pasta / "traces"

    class SoAbrePagina:                 # o navegador de mentira dos testes da Fase 4: só tem nova_pagina
        def nova_pagina(self):
            return object()

    assert ex._trace(SoAbrePagina(), "reter_trace", object()) is None and ex._trace(SoAbrePagina(), "gravar_traces", "a/b/c") is None

    class Anota:
        def __init__(self) -> None:
            self.chamadas: list = []

        def gravar_traces(self, tid: str) -> list:
            self.chamadas.append(("gravar_traces", tid))
            return ["x"]

    nav = Anota()
    assert ex._trace(nav, "gravar_traces", "a/b/c") == ["x"] and nav.chamadas == [("gravar_traces", "a/b/c")]
    for funcao, trechos in ((ex.Tela.rodar_caso, ('_trace(self.nav, "descartar_traces")', '_trace(self.nav, "reter_trace", pagina)')),
                            (ex.Tela.emitir, ('_trace(self.nav, "gravar_traces", tid)',)),
                            (ex.Cura.executar, ('_trace(self.nav, "descartar_traces")', '_trace(self.nav, "reter_trace", pagina)')),
                            (ex.Cura.emitir_cura, ('_trace(self.nav, "gravar_traces", tid)',))):
        fonte = inspect.getsource(funcao)
        for trecho in trechos:
            assert trecho in fonte, (funcao.__qualname__, trecho)
    ps1 = (EXP / "rodar_fase4.ps1").read_bytes()
    assert ps1.startswith(b"\xef\xbb\xbf") and b"[switch]$TraceNaFalha" in ps1 and b'"--trace-na-falha"' in ps1, "o lançador passa a opção adiante, e continua em UTF-8 com BOM"


def teste_hub_trace_do_caso_aparece_e_e_entregue_quando_o_arquivo_existe():
    acervo, raiz = _acervo_de_teste()
    com, sem = acervo.iteracoes("lex-1")[1]["tid"], acervo.iteracoes("lex-4")[0]["tid"]
    (raiz / "c2" / "traces").mkdir()
    arq = raiz / "c2" / "traces" / "lex-1@tela.zip"
    with zipfile.ZipFile(arq, "w") as z:
        z.writestr("trace.trace", "{}")
    assert acervo.caso(com)["trace"] == {"existe": True, "arquivo": "lex-1@tela.zip"} and acervo.caso(sem)["trace"] == {"existe": False, "arquivo": None}
    assert acervo.trace(com) == arq and acervo.trace(sem) is None
    _erro(acervo.trace, "../../x", tipo=KeyError)
    with _hub_no_ar(acervo) as (base, _, _srv):
        status, cab, corpo = _http(base, "GET", "/api/trace?tid=" + urllib.parse.quote(com, safe=""))
        assert status == 200 and cab["content-type"] == "application/zip" and corpo == arq.read_bytes(), cab
        assert "attachment" in cab["content-disposition"] and "lex-1@tela.zip" in cab["content-disposition"]
        for ruim in (sem, "../../x", "c2/qwen2.5_7b/../../traces/lex-1@tela"):
            assert _http(base, "GET", "/api/trace?tid=" + urllib.parse.quote(ruim, safe=""))[0] == 404, ruim
        _, caso = _json(base, "GET", "/api/caso?tid=" + urllib.parse.quote(com, safe=""))
        assert "show-trace" in caso["trace"]["comando"] and caso["trace"]["comando"].endswith("lex-1@tela.zip"), caso["trace"]


def teste_ao_vivo_le_o_estado_da_barra_e_o_ultimo_diagnostico_da_corrida_mais_recente():
    acervo, raiz = _acervo_de_teste()
    vivo = hd.AoVivo(raiz, leituras=acervo.leituras)
    assert vivo.ler() == {"ha_corrida": False}, "sem nenhum progresso.json, não há corrida para mostrar"
    _estado_da_barra(raiz / "c1", estado="concluido", fracao=1.0, idade_s=3600)
    _estado_da_barra(raiz / "c2", estado="determinado", fracao=0.4, idade_s=0)
    d = vivo.ler()
    assert d["ha_corrida"] is True and d["pasta"] == "c2" and d["em_andamento"] is True and d["idade_s"] < 5, d
    assert d["progresso"]["estado"] == "determinado" and d["progresso"]["fracao"] == 0.4 and d["progresso"]["etapa"].startswith("lex-4@tela")
    u = d["ultimo_diagnostico"]
    assert u["tid"] == "c2/qwen2.5_7b/lex-4@tela" and u["caso"] == "lex-4" and u["escolha"] == "resposta_truncada" and u["confianca"] == "alta", u
    assert [a["opcao"] for a in u["alternativas"]][:2] == ["resposta_truncada", "corpo_nao_e_json"] and u["alternativas"][0]["escolhida"] is True
    assert 0.99 < u["alternativas"][0]["probabilidade"] <= 1 and [v["id"] for v in u["verbetes"]] == ["resposta_truncada", "contagem_inconsistente", "entidade-produto"]
    assert u["titulo"] and d["diagnosticos"] == 2
    _estado_da_barra(raiz / "c2", estado="determinado", fracao=0.4, idade_s=120)
    parado = vivo.ler()
    assert parado["em_andamento"] is False and parado["pasta"] == "c2" and parado["idade_s"] >= 119, "o arquivo parou de ser regravado: a inferência não está mais rodando"
    nova = raiz / "hub_20261125_100000"
    nova.mkdir()
    _estado_da_barra(nova, estado="indeterminado", fracao=None, etapa="lex-1@tela · diagnóstico")
    comecando = vivo.ler()
    assert comecando["pasta"] == nova.name and comecando["ultimo_diagnostico"] is None and comecando["diagnosticos"] == 0 and comecando["em_andamento"] is True
    (nova / "progresso.json").write_text("{pela metade", encoding="utf-8")
    assert vivo.ler()["progresso"] is None, "um arquivo lido no meio da regravação não derruba a leitura"


def _lancador_de_mentira(raiz: Path, demora: float = 0.5):
    return lambda saida, opcoes: [sys.executable, "-c", FALSA_CORRIDA, str(raiz / saida), str(raiz / "c2"), str(demora)]


def teste_servidor_execucao_so_dispara_com_permissao_e_uma_corrida_por_vez():
    acervo, raiz = _acervo_de_teste()
    with _hub_no_ar(acervo) as (base, _, _srv):
        status, e = _json(base, "GET", "/api/execucao")
        assert status == 200 and e["permitida"] is False and e["em_andamento"] is False, e
        assert "rodar_fase4.ps1" in e["comando"] and "-Modo cenarios" in e["comando"] and "-Repeticoes 1" in e["comando"] and "-Saida hub_" in e["comando"], e["comando"]
        status, r = _json(base, "POST", "/api/execucao", {"acao": "rodar", "repeticoes": 1})
        assert status == 403 and "--permitir-execucao" in r["erro"], r
        assert not list(raiz.glob("hub_*")), "sem permissão nada é lançado"
    with _hub_no_ar(acervo, permitir_execucao=True, comando_da_corrida=_lancador_de_mentira(raiz, 0.8)) as (base, _, _srv):
        assert _json(base, "POST", "/api/execucao", {"acao": "rodar", "repeticoes": 99})[0] == 400
        assert _json(base, "POST", "/api/execucao", {"acao": "rodar", "repeticoes": "2; del"})[0] == 400
        assert _json(base, "POST", "/api/execucao", {"acao": "formatar"})[0] == 400
        assert _http(base, "POST", "/api/execucao", {"acao": "rodar", "repeticoes": 1}, {"Origin": "http://outro-site.example"})[0] == 403
        status, r = _json(base, "POST", "/api/execucao", {"acao": "rodar", "repeticoes": 1, "saida": "../fora"})
        assert status == 200 and r["em_andamento"] is True and re.fullmatch(r"hub_\d{8}_\d{6}", r["saida"]), "o nome da pasta é dado pelo servidor, não pelo pedido"
        saida = r["saida"]
        assert _json(base, "POST", "/api/execucao", {"acao": "rodar", "repeticoes": 1})[0] == 409, "uma corrida por vez"
        vivo = _ate(lambda: _json(base, "GET", "/api/ao-vivo")[1], lambda d: d.get("pasta") == saida)
        assert vivo["progresso"]["estado"] in ("determinado", "concluido")
        fim = _ate(lambda: _json(base, "GET", "/api/execucao")[1], lambda d: d["terminou"])
        assert fim["codigo"] == 0 and fim["em_andamento"] is False and fim["saida"] == saida and "FIM da corrida de mentira" in fim["log"], fim
        depois = _json(base, "GET", "/api/ao-vivo")[1]
        assert depois["progresso"]["estado"] == "concluido" and depois["ultimo_diagnostico"]["escolha"] == "resposta_truncada"
    with _hub_no_ar(acervo, permitir_execucao=True, comando_da_corrida=_lancador_de_mentira(raiz, 30)) as (base, _, _srv):
        assert _json(base, "POST", "/api/execucao", {"acao": "parar"})[0] == 409, "não há corrida para parar"
        assert _json(base, "POST", "/api/execucao", {"acao": "rodar", "repeticoes": 2})[1]["em_andamento"] is True
        status, r = _json(base, "POST", "/api/execucao", {"acao": "parar"})
        assert status == 200, r
        parou = _ate(lambda: _json(base, "GET", "/api/execucao")[1], lambda d: d["terminou"])
        assert parou["codigo"] != 0 and parou["parada_pelo_hub"] is True, parou


def teste_pagina_ao_vivo_mostra_a_barra_o_ultimo_diagnostico_e_o_comando_para_copiar():
    with _navegador() as (pagina, erros):
        if pagina is None:
            return
        acervo, raiz = _acervo_de_teste()
        _estado_da_barra(raiz / "c2", estado="determinado", fracao=0.4)
        with _hub_no_ar(acervo) as (base, _, _srv):
            pagina.goto(base + "/")
            pagina.wait_for_selector("#lista-de-casos .item-caso")
            assert pagina.is_hidden("#ao-vivo")
            pagina.click("#abrir-ao-vivo")
            pagina.wait_for_selector('#barra[aria-valuenow="40"]')
            assert pagina.is_visible("#ao-vivo") and pagina.is_hidden("#caso")
            assert "lex-4@tela" in pagina.inner_text("#etapa-ao-vivo") and "c2" in pagina.inner_text("#estado-ao-vivo")
            assert "resposta_truncada" in pagina.inner_text("#cerebro") and pagina.locator("#cerebro .alternativa").count() >= 2
            assert "contagem_inconsistente" in pagina.inner_text("#cerebro")
            assert "rodar_fase4.ps1" in pagina.inner_text("#comando-da-corrida") and pagina.is_hidden("#rodar-cenarios"), "sem permissão, a página mostra o comando para copiar"
            _estado_da_barra(raiz / "c2", estado="determinado", fracao=0.8)
            pagina.wait_for_selector('#barra[aria-valuenow="80"]', timeout=8000)      # a página relê sozinha
            pagina.click("#abrir-ultimo")
            pagina.wait_for_selector('#caso[data-tid="c2/qwen2.5_7b/lex-4@tela"] section.bloco')
            assert pagina.is_hidden("#ao-vivo")
            pagina.click("#abrir-ao-vivo")
            pagina.wait_for_selector("#ao-vivo:visible")
            pagina.reload()
            pagina.wait_for_selector('#barra[aria-valuenow="80"]')
            assert pagina.is_visible("#ao-vivo"), "o endereço guarda a vista: recarregar volta à corrida ao vivo"
        assert erros == [], erros


def teste_pagina_roda_os_cenarios_quando_permitido_e_mostra_o_fim():
    with _navegador() as (pagina, erros):
        if pagina is None:
            return
        acervo, raiz = _acervo_de_teste()
        with _hub_no_ar(acervo, permitir_execucao=True, comando_da_corrida=_lancador_de_mentira(raiz, 1.0)) as (base, _, _srv):
            pagina.goto(base + "/")
            pagina.wait_for_selector("#lista-de-casos .item-caso")
            pagina.click("#abrir-ao-vivo")
            pagina.wait_for_selector("#rodar-cenarios:visible")
            assert "nenhuma corrida" in pagina.inner_text("#estado-ao-vivo").lower() and pagina.is_hidden("#comando-da-corrida")
            pagina.select_option("#repeticoes", "1")
            pagina.click("#rodar-cenarios")
            _esperar_texto(pagina, "#estado-da-execucao", "em andamento")
            pagina.wait_for_selector("#parar-corrida:visible")
            pagina.locator("#estado-da-execucao", has_text="terminou").wait_for(timeout=15000)
            assert "FIM da corrida de mentira" in pagina.inner_text("#log-da-execucao") and pagina.is_hidden("#parar-corrida")
            pagina.wait_for_selector('#barra[aria-valuenow="100"]')
            assert "resposta_truncada" in pagina.inner_text("#cerebro")
        assert erros == [], erros


def teste_pagina_abre_a_arvore_pelo_botao_e_oferece_o_trace_quando_ele_existe():
    with _navegador() as (pagina, erros):
        if pagina is None:
            return
        acervo, raiz = _acervo_de_teste()
        (raiz / "c2" / "traces").mkdir()
        with zipfile.ZipFile(raiz / "c2" / "traces" / "lex-1@tela.zip", "w") as z:
            z.writestr("trace.trace", "{}")
        com, sem = acervo.iteracoes("lex-1")[1]["tid"], acervo.iteracoes("lex-4")[0]["tid"]
        with _hub_no_ar(acervo) as (base, _, _srv):
            _abrir_caso(pagina, base, com)
            assert "show-trace" in pagina.inner_text("#trace-do-caso")
            assert pagina.get_attribute("#trace-do-caso a", "href") == "/api/trace?tid=" + urllib.parse.quote(com, safe="")
            pagina.click("#abrir-arvore")
            assert pagina.is_visible("#aba-arvore") and pagina.is_hidden("#aba-relatorio")
            _abrir_caso(pagina, base, sem)
            assert pagina.locator("#trace-do-caso a").count() == 0 and "trace desligado" in pagina.inner_text("#trace-do-caso")
        assert erros == [], erros


# ! Alteração de IA - Revisar: (25/11/2026, pacote Q6, etapa 4) teste da ideia aproveitada do estudo do `visual-explainer` (decisão 126): passar o
# mouse numa conversa acende o trecho comentado no relatório, e passar no trecho acende a conversa. Escrito ANTES do código: a primeira
# rodada falha porque nenhum dos dois ganha a marca.
# ! Motivo: o estudo (`5-metodo-e-ferramental/estudo-visual-explainer-para-o-hub.md`) registra a ideia do realce ligado, em que o termo do
# texto e a parte da figura que tratam da mesma coisa se acendem juntos; no hub, com várias conversas num bloco, é o que diz de relance a que
# trecho cada uma se refere. A marca é uma borda, e não só uma cor, para quem não distingue as cores também ver.
def teste_pagina_conversa_e_trecho_comentado_se_acendem_juntos():
    with _navegador() as (pagina, erros):
        if pagina is None:
            return
        acervo, _ = _acervo_de_teste()
        tid = acervo.iteracoes("lex-1")[1]["tid"]
        bloco = "b12-veredito-do-agente"
        palavra = _palavra_do_bloco(acervo.caso(tid), bloco)
        with _hub_no_ar(acervo) as (base, _, _srv):
            status, _r = _json(base, "POST", "/api/revisao", {"tid": tid, "acao": "comentar", "autor": {"nome": "Ana"}, "texto": "Sobre este trecho.",
                                                             "ancora": {"bloco": bloco, "trecho": palavra, "inicio": 0, "fim": len(palavra)}})
            assert status == 200
            _abrir_caso(pagina, base, tid)
            marca, conversa = f'section.bloco[data-bloco="{bloco}"] mark.trecho-comentado', f'section.bloco[data-bloco="{bloco}"] .conversa'
            assert pagina.inner_text(marca) == palavra and pagina.locator(marca + ".aceso").count() == 0 and pagina.locator(conversa + ".acesa").count() == 0
            pagina.hover(conversa + " .cab-conversa")
            pagina.wait_for_selector(marca + ".aceso")
            assert pagina.locator(conversa + ".acesa").count() == 1
            pagina.hover("#titulo-do-caso")
            pagina.wait_for_selector(marca + ".aceso", state="detached")
            pagina.hover(marca)
            pagina.wait_for_selector(conversa + ".acesa")
        assert erros == [], erros


# ------------------------------------------------------------------ Q7: a seleção pelo Git no hub

# ! Alteração de IA - Revisar: (25/11/2026, Pós-Fase 4, pacote Q7) os testes da seleção pelo Git no hub, escritos ANTES do código: a primeira rodada
# falha porque `criar_servidor` não aceita `selecao_git`. O servidor mostra a decisão de `impacto_git` para o que mudou (`/api/selecao`), põe
# `-Selecao git` e `-Desde <commit>` no comando da corrida e recusa um `desde` que não seja um commit; a página mostra o que rodaria, o que
# ficaria de fora e por quê, antes de qualquer corrida.
# ! Motivo: plano aprovado da Pós-Fase 4, seção 3.7 ("a seleção diz quais cenários rodar e por quê") e pacote Q7 (a seleção ligada ao hub). A
# decisão vem de uma função que o teste troca, para o teste não depender do estado do repositório no dia em que roda; o `desde` vira parte de
# uma linha de comando, e por isso só passa se for o identificador de um commit.
DECISAO_Q7 = {"modo": "selecionada", "regras": ["conferencia_contra_a_rodada_completa"], "commit_atual": "def5678abc", "arvore_suja": True,
              "motivo": "seleção parcial: 2 de 10 cenários do ensaio, pelos arquivos no mapa; os 8 deixados de fora ficam registrados para a conferência contra a rodada completa (regra 3)",
              "cenarios": ["localizador-front-admin-login", "localizador-front-admin-produtos"], "deixados_de_fora": ["contrato-field_missing", "localizador-front-busca"],
              "por_que": {"localizador-front-admin-login": ["Programacao/CobaiaFront/admin/login.php: página do cenário"],
                          "localizador-front-admin-produtos": ["Programacao/CobaiaFront/admin/login.php: página aberta por um passo do cenário"]},
              "arquivos": [{"arquivo": "Programacao/CobaiaFront/admin/login.php", "classe": "no_mapa", "motivo": "no mapa"}]}


def _selecao_de_mentira(pedidos: list):
    def selecao(desde):
        pedidos.append(desde)
        return {**DECISAO_Q7, "commit_testado": desde or "abc1234"}
    return selecao


def teste_servidor_selecao_pelo_git_mostra_a_decisao_e_entra_no_comando():
    acervo, _ = _acervo_de_teste()
    pedidos, vistos = [], []

    def lancador(saida, opcoes):
        vistos.append(dict(opcoes))
        return [sys.executable, "-c", "print('ok')"]

    with _hub_no_ar(acervo, selecao_git=_selecao_de_mentira(pedidos), permitir_execucao=True, comando_da_corrida=lancador) as (base, _, _srv):
        status, d = _json(base, "GET", "/api/selecao")
        assert status == 200 and d["modo"] == "selecionada" and d["commit_testado"] == "abc1234" and pedidos == [None], d
        assert _json(base, "GET", "/api/selecao?desde=0123abc")[1]["commit_testado"] == "0123abc" and pedidos[-1] == "0123abc"
        for ruim in ("HEAD", "abc; rm -rf x", "../x", "zzzzzzz", "abc12"):
            status, r = _json(base, "GET", "/api/selecao?desde=" + urllib.parse.quote(ruim, safe=""))
            assert status == 400 and "commit" in r["erro"], (ruim, r)
        assert len(pedidos) == 2, "um desde recusado nem chega à função que lê o Git"
        e = _json(base, "GET", "/api/execucao")[1]
        assert "-Selecao" not in e["comando_sugerido"] and "-Repeticoes 1" in e["comando_sugerido"]
        e = _json(base, "GET", "/api/execucao?selecao=git&desde=0123abc&repeticoes=3")[1]
        assert e["comando_sugerido"].endswith("-Repeticoes 3 -LeituraNaPasta -Selecao git -Desde 0123abc"), e["comando_sugerido"]
        assert _json(base, "GET", "/api/execucao?selecao=git")[1]["comando_sugerido"].endswith("-Selecao git")
        for ruim in ("selecao=tudo", "selecao=git&desde=abc%3B+rm", "repeticoes=99"):
            assert _json(base, "GET", "/api/execucao?" + ruim)[0] == 400, ruim
        for ruim in ({"selecao": "outra"}, {"selecao": "git", "desde": "abc; rm"}, {"selecao": "todos", "desde": "0123abc"}):
            assert _json(base, "POST", "/api/execucao", {"acao": "rodar", "repeticoes": 1, **ruim})[0] == 400, ruim
        assert vistos == []
        assert _json(base, "POST", "/api/execucao", {"acao": "rodar", "repeticoes": 2, "selecao": "git", "desde": "0123abc"})[0] == 200
        assert vistos == [{"repeticoes": 2, "selecao": "git", "desde": "0123abc"}]
        _esperar(lambda: _json(base, "GET", "/api/execucao")[1]["terminou"])
        assert _json(base, "POST", "/api/execucao", {"acao": "rodar", "repeticoes": 1})[0] == 200 and vistos[-1] == {"repeticoes": 1, "selecao": "todos", "desde": None}
        _esperar(lambda: _json(base, "GET", "/api/execucao")[1]["terminou"])
    assert hub.comando_padrao("hub_x", {"repeticoes": 1, "selecao": "todos", "desde": None})[-1] == "-LeituraNaPasta"
    assert hub.comando_padrao("hub_x", {"repeticoes": 1})[-1] == "-LeituraNaPasta", "sem a seleção, o comando é o de antes"


def teste_pagina_selecao_pelo_git_mostra_o_que_rodaria_e_muda_o_comando():
    with _navegador() as (pagina, erros):
        if pagina is None:
            return
        acervo, _ = _acervo_de_teste()
        pedidos: list = []
        with _hub_no_ar(acervo, selecao_git=_selecao_de_mentira(pedidos)) as (base, _, _srv):
            pagina.goto(base + "/")
            pagina.wait_for_selector("#lista-de-casos .item-caso")
            pagina.click("#abrir-ao-vivo")
            pagina.wait_for_selector("#comando-da-corrida:visible")
            assert "-Selecao" not in pagina.inner_text("#comando-da-corrida") and pagina.inner_text("#previa-da-selecao").strip() == "" and pedidos == []
            pagina.select_option("#selecao-da-corrida", "git")
            _esperar_texto(pagina, "#previa-da-selecao", "seleção parcial")
            texto = pagina.inner_text("#previa-da-selecao")
            for trecho in ("localizador-front-admin-login", "contrato-field_missing", "abc1234", "def5678", "admin/login.php", "ainda não commitadas"):
                assert trecho in texto, (trecho, texto)
            _esperar_texto(pagina, "#comando-da-corrida", "-Selecao git")
            pagina.fill("#desde-da-corrida", "0123abc")
            pagina.dispatch_event("#desde-da-corrida", "change")
            _esperar_texto(pagina, "#comando-da-corrida", "-Desde 0123abc")
            _esperar_texto(pagina, "#previa-da-selecao", "0123abc")
            pagina.fill("#desde-da-corrida", "isto nao e um commit")
            pagina.dispatch_event("#desde-da-corrida", "change")
            _esperar_texto(pagina, "#erro", "commit")
            pagina.select_option("#selecao-da-corrida", "todos")
            pagina.wait_for_selector("#erro:empty", state="attached")
            pagina.locator("#comando-da-corrida", has_text="-Selecao").wait_for(state="detached")
            assert pagina.inner_text("#previa-da-selecao").strip() == ""
        assert [e for e in erros if "status of 400" not in e] == [], erros


# ! Alteração de IA - Revisar: (25/11/2026, pacote Q6) teste do resumo do hub (`hub.py --resumo`), escrito ANTES do código: a primeira rodada falha por
# AttributeError em `hub.resumo`. O resumo diz quantos casos o hub mostra por corrida, quantos casos distintos e quantos têm mais de uma
# iteração, as listas fechadas da revisão e quantos testes o runner tem, e fica gravado em `resultados_alvo/fase4/hub.{json,md}` com `--check`.
# ! Motivo: a aba do painel e os textos do roadmap e do README citam esses números, e a regra do projeto é que nenhum número seja digitado à
# mão: eles saem deste arquivo, que o teste compara com o acervo de verdade.
def teste_hub_resumo_gravado_e_conferido_contra_o_acervo():
    acervo = hd.Acervo(RA, descobrir=False)
    indice = acervo.indice()
    dado, md = hub.resumo(acervo)
    assert [c["pasta"] for c in dado["corridas"]] == [c["pasta"] for c in hd.CORRIDAS_PADRAO] and sum(c["casos"] for c in dado["corridas"]) == len(indice)
    por_caso: dict[str, int] = {}
    for linha in indice:
        por_caso[linha["caso"]] = por_caso.get(linha["caso"], 0) + 1
    t = dado["total"]
    assert t["casos"] == len(indice) and t["casos_distintos"] == len(por_caso) and t["com_mais_de_uma_iteracao"] == sum(1 for n in por_caso.values() if n > 1), t
    assert t["maior_numero_de_iteracoes"] == max(por_caso.values()) and t["com_divergencia"] == sum(1 for l in indice if l["divergencia"]) and t["com_cura"] == sum(1 for l in indice if l["cura"])
    assert dado["revisao"]["vereditos"] == list(hr.VEREDITOS) and dado["revisao"]["estados_55"] == list(hr.ESTADOS_55) and dado["revisao"]["causas"] == len(hr.CAUSAS)
    assert dado["relatorio"]["blocos"] == len(grr.CAMPOS_55) + len(grr.SECOES_MANTIDAS_V3) and dado["relatorio"]["campos_da_5_5"] == len(grr.CAMPOS_55)
    meus = [n for n, o in vars(sys.modules[__name__]).items() if n.startswith("teste_") and inspect.isfunction(o)]
    assert dado["testes"]["total"] == len(meus) and 0 < dado["testes"]["no_navegador"] < len(meus), dado["testes"]
    assert "—" not in md and "→" not in md and f"{len(indice)} casos" in md
    gravado = RA / "fase4" / "hub.json"
    assert gravado.exists(), "hub.json ainda não gravado (python hub.py --resumo)"
    assert hub.pf.sem_data(json.loads(gravado.read_text(encoding="utf-8"))) == hub.pf.sem_data(json.loads(json.dumps(dado, ensure_ascii=False))), "o arquivo gravado difere do acervo de agora (hub.py --resumo --check)"
    saida = io.StringIO()
    with contextlib.redirect_stdout(saida):
        assert hub.main(["--resumo", "--check"]) == 0, saida.getvalue()


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
        if _PULADOS:
            print(f"aviso: {len(_PULADOS)} teste(s) da página pulado(s), sem o Playwright neste Python")
        print(f"{len(testes)} testes ok")
    finally:
        for caminho in _TEMPORARIOS:
            shutil.rmtree(caminho, ignore_errors=True)


if __name__ == "__main__":
    main()
