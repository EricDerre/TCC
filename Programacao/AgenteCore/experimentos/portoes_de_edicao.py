#!/usr/bin/env python3
# ! Alteração de IA - Revisar: arquivo novo (10/11/2026, ficha 67 opção b, decisão 121) com os três portões por edição que a proposta de desenho do analista de
# documentação acrescenta aos filtros de hoje (`5-metodo-e-ferramental/proposta-analista-de-documentacao.md`, seção 4.5) e com a medida M1 da mesma proposta (seção 6).
# Portão 3, a forma de instrução: recusa o texto que começa por verbo de edição ("Adicionar nota sobre...", "Corrigir a junção..."), porque ele fala com quem vai mexer no
# verbete e não afirma um fato do sistema. Portão 4, os filtros de texto: as oito medidas de prolixidade e objetividade do pacote Q2 (`filtros_de_texto.py`), com os
# limiares calibrados no corpus. Portão 5, a busca: aplica a edição a uma cópia temporária da biblioteca, refaz a busca dos casos com gabarito (a causa certa conhecida)
# e recusa a edição que tira o verbete da causa certa dos três entregues de algum caso; no sinal de busca (palavras-chave e sintomas novos num verbete que já existe),
# exige que o caso de origem passe a receber o verbete. A medida M1 aplica os três às 92 propostas da corrida 20 e compara com a revisão humana das 20 que passaram nos
# filtros de hoje: quantas erradas e parciais cada portão recusaria e quantas corretas perderia. Grava `resultados_alvo/fase4/portoes_m1.{json,md}`, com `--check`.
# ! Motivo: o Eric aprovou a proposta como base de desenho e pediu a M1 antes da Fase 5 (decisão 121); ela não gasta modelo e diz quanto os portões novos barrariam antes
# de qualquer implementação. Os mesmos portões são os que a corrida 27 (a medida M2) aplica às propostas do analista, por isso ficam num módulo próprio, fora do agente:
# o validador da Fase 3 (`evolucao_biblioteca.py`), os filtros da Fase 4 (`biblioteca_fase4.py`), a busca (`recuperacao.py`) e os filtros de texto entram só para leitura,
# e nenhuma biblioteca é alterada (a edição entra numa cópia temporária). A contagem publicada pela pesquisa da ficha 64 (76 das 92 propostas em forma de instrução) usou
# cinco radicais; a lista fechada deste portão pega também "Retificar", "Adicionado", "Cria" e os rótulos seguidos de dois-pontos, e a medida mostra as duas contagens.
"""Portões por edição da proposta do analista de documentação (3: forma de instrução; 4: filtros de texto; 5: busca) e a medida M1 sobre a corrida 20. Sem modelo.

Uso (em Programacao/AgenteCore/experimentos, com RESULTADOS_DIR=resultados_alvo):
  python portoes_de_edicao.py --m1 [--check]   aplica os portões 3, 4 e 5 às 92 propostas da corrida 20, contra a revisão humana (resultados_alvo/fase4/portoes_m1.{json,md})
"""
from __future__ import annotations

import argparse
import collections
import json
import sys
import tempfile
import time
from pathlib import Path

import analisar_fase3b as a3b
import biblioteca as bib
import biblioteca_fase4 as b4
import caminhos
import corridas_em_texto as ct
import diagnostico_ao_vivo as dv
import evolucao_biblioteca as evo
import executar_bateria
import executar_fase3
import executar_fase3b as e3b
import experimento_sem_notas as esn
import filtros_de_texto as ft
import pre_fase4 as pf
import recuperacao as rec

MEDIDA = "M1"
NOME_M1, PREFIXO_M1 = "portoes_m1", "tb_f4_portoes_"
PORTOES = ("forma", "texto", "busca")
NOME_DO_PORTAO = {"forma": "portão 3, a forma de instrução", "texto": "portão 4, os filtros de texto", "busca": "portão 5, a busca"}
REGRA_DO_PORTAO = {"forma": "recusa o texto que começa por verbo de edição ou por rótulo seguido de dois-pontos (lista fechada)",
                   "texto": "recusa o texto que reprova em alguma das medidas de prolixidade e objetividade do pacote Q2, com os limiares do corpus",
                   "busca": ("recusa a edição que, aplicada numa cópia da biblioteca, tira o verbete da causa certa dos três entregues de algum caso com gabarito; no sinal de busca, "
                             "exige que o caso de origem passe a receber o verbete")}
VEREDITOS = b4.VEREDITOS_DA_REVISAO            # Correta, Parcial, Errada
OPERACAO_SINAL = "sinal_de_busca"             # palavras-chave e sintomas novos num verbete que já existe, sem nota no corpo (proposta, seção 4.4)
K_DA_BUSCA = ct.K_DO_EXPERIMENTO              # os três verbetes que o diagnóstico recebe (regra R8)
CORRIDA_20 = "fase4_biblioteca"
MODELO = dv.MODELO_PADRAO
DESTINOS = ("aceita pelos filtros de hoje", "segurada para revisão humana (regra dos 40%)", "recusada pelo validador da Fase 3", "recusada pelos filtros da Fase 4")

# Verbos de edição, nas formas em que abrem uma frase de instrução ou de registro de mudança: infinitivo ("Adicionar"), imperativo ("Adicione"), particípio
# ("Adicionado") e, só nos verbos que não descrevem o sistema, a terceira pessoa ("Adiciona", "Corrige", "Cria"). Ficam de fora as formas que também são nome
# ("nota", "detalhe", "registros", "ajuste"), para uma afirmação que comece por elas não ser recusada.
_VERBOS_DE_EDICAO = (
    ("adicionar", "adicione", "adicionem", "adiciona", "adicionado", "adicionada", "adicionados", "adicionadas", "adicionando"),
    ("acrescentar", "acrescente", "acrescentem", "acrescenta", "acrescentado", "acrescentada", "acrescentados", "acrescentadas", "acrescentando"),
    ("incluir", "inclua", "incluam", "inclui", "incluído", "incluída", "incluídos", "incluídas", "incluindo"),
    ("inserir", "insira", "insiram", "insere", "inserido", "inserida", "inseridos", "inseridas", "inserindo"),
    ("corrigir", "corrija", "corrijam", "corrige", "corrigido", "corrigida", "corrigidos", "corrigidas", "corrigindo"),
    ("retificar", "retifique", "retifiquem", "retifica", "retificado", "retificada", "retificados", "retificadas", "retificando"),
    ("criar", "crie", "criem", "cria", "criado", "criada", "criados", "criadas", "criando"),
    ("notar", "note", "notem"),
    ("anotar", "anote", "anotem", "anotado", "anotada"),
    ("atualizar", "atualize", "atualizem", "atualizado", "atualizada", "atualizados", "atualizadas"),
    ("remover", "remova", "removam", "removido", "removida", "removidos", "removidas"),
    ("substituir", "substitua", "substituam", "substituído", "substituída", "substituídos", "substituídas"),
    ("documentar", "documente", "documentem", "documentado", "documentada"),
    ("registrar", "registre", "registrem", "registrado", "registrada"),
    ("mencionar", "mencione", "mencionem", "mencionado", "mencionada"),
    ("esclarecer", "esclareça", "esclareçam", "esclarecido", "esclarecida"),
    ("explicar", "explique", "expliquem", "explicado", "explicada"),
    ("detalhar", "detalhado", "detalhada"),
    ("destacar", "destacado", "destacada"),
    ("revisar", "revise", "revisem", "revisado", "revisada"),
    ("alterar", "altere", "alterem", "alterado", "alterada"),
    ("modificar", "modifique", "modifiquem", "modificado", "modificada"),
    ("ajustar", "ajustado", "ajustada"),
    ("verificar", "verifique", "verifiquem"),
    ("conferir", "confira", "confiram"),
    ("considerar", "considere", "considerem"),
    ("lembrar", "lembre", "lembrem"),
    ("garantir", "garanta", "garantam"),
    ("evitar", "evite", "evitem"),
    ("deve-se", "devemos", "recomenda-se", "sugere-se"),
)
_FORMAS_DE_EDICAO = frozenset(forma for verbo in _VERBOS_DE_EDICAO for forma in verbo)
# Rótulos que abrem um registro de mudança quando vêm seguidos de dois-pontos ("Retificação: onde diz...", "Nota: o contrato...").
_ROTULOS_DE_EDICAO = frozenset(("retificação", "retificacao", "correção", "correcao", "nota", "observação", "observacao", "obs", "adição", "adicao", "inclusão", "inclusao",
                                "atualização", "atualizacao"))
_ABERTURAS = "\"'“”‘’«»([{*-–•"


# ------------------------------------------------------------------ portão 3: a forma de instrução

def primeira_palavra(texto: str) -> tuple[str, bool]:
    """A primeira palavra do texto, em minúsculas e sem as aspas ou os sinais que a abrem, e se ela vem seguida de dois-pontos."""
    partes = str(texto or "").strip().lstrip(_ABERTURAS).split()
    if not partes:
        return "", False
    crua = partes[0]
    com_dois_pontos = crua.endswith(":")
    return crua.strip(_ABERTURAS + ".,;:!?").lower(), com_dois_pontos


def portao_da_forma(texto: str) -> dict:
    """Portão 3: o texto de uma edição tem de afirmar um fato sobre o sistema. Recusa o que começa por verbo de edição (a lista fechada `_FORMAS_DE_EDICAO`) ou por
    rótulo de mudança seguido de dois-pontos; texto vazio também não passa."""
    palavra, com_dois_pontos = primeira_palavra(texto)
    if not palavra:
        return {"passa": False, "primeira_palavra": "", "motivo": "o texto está vazio"}
    if palavra in _FORMAS_DE_EDICAO:
        return {"passa": False, "primeira_palavra": palavra,
                "motivo": f"começa por \"{palavra}\", verbo de edição: o texto fala com quem vai mexer no verbete e não afirma um fato do sistema"}
    if com_dois_pontos and palavra in _ROTULOS_DE_EDICAO:
        return {"passa": False, "primeira_palavra": palavra + ":", "motivo": f"começa pelo rótulo \"{palavra}:\", que é registro de mudança e não afirmação sobre o sistema"}
    return {"passa": True, "primeira_palavra": palavra, "motivo": None}


# ------------------------------------------------------------------ portão 4: os filtros de texto do pacote Q2

def portao_do_texto(texto: str, limiares: dict | None = None) -> dict:
    """Portão 4: as medidas de prolixidade e objetividade de `filtros_de_texto.py` contra os limiares do corpus (`limiares_texto.json`). Passa o texto que não reprova em
    nenhuma; o Flesch abaixo de 50 só acende o alarme."""
    av = ft.avaliar(ft.medir(texto), limiares or ft.carregar_limiares())
    reprovados = [ch for ch, c in av["criterios"].items() if c["passa"] is False]
    return {"passa": bool(av["aprovado"]), "reprovados": reprovados, "alarme_flesch": bool(av["alarme_flesch"]), "termos_sem_expansao": list(av["termos_sem_expansao"])}


# ------------------------------------------------------------------ portão 5: a busca refeita com a edição aplicada

def casos_com_gabarito() -> list[dict]:
    """Os casos com a causa certa conhecida: os 90 oficiais e os 36 inéditos da ficha 27, os mesmos da medida da pesquisa da ficha 64."""
    return list(e3b.TODOS_OS_CASOS) + list(esn.casos_por_banco()["ineditos"])


class BuscaDosCasos:
    """A busca do agente refeita, sem modelo, para os casos com gabarito sobre uma biblioteca de base: a consulta de cada caso, o verbete da causa certa e os três
    verbetes que a busca entrega antes de qualquer edição. A base só é lida."""

    def __init__(self, base: Path, casos: list[dict] | None = None):
        import executar_fase4 as ex
        self.base = Path(base)
        self.casos = list(casos) if casos is not None else casos_com_gabarito()
        self.certo = {c["id"]: c["gabarito"]["causa_raiz"] for c in self.casos}
        self.consultas = {c["id"]: dv.caso_da_busca(ex.fixture_sem_gabarito(c)) for c in self.casos}
        self.verbetes = bib.carregar(self.base)
        self.antes = self.tres(self.base)

    def tres(self, pasta: Path) -> dict[str, list[str]]:
        """caso -> os ids dos três verbetes que a busca entrega com a biblioteca de `pasta`."""
        indice = rec.Indice(bib.carregar(pasta))
        return {cid: [v["id"] for _, v in rec.pontuar(indice, consulta)[:K_DA_BUSCA]] for cid, consulta in self.consultas.items()}


def aplicar_sinal_de_busca(raiz: Path, edicao: dict) -> Path:
    """Grava numa cópia da biblioteca o sinal de busca: as palavras-chave e os sintomas novos entram no frontmatter do verbete, sem nota no corpo. Usa a mesma edição de
    texto do frontmatter das notas (`evolucao_biblioteca._acrescentar_ao_frontmatter`), que só acrescenta."""
    destino = raiz / edicao["arquivo"]
    destino.write_text(evo._acrescentar_ao_frontmatter(destino.read_text(encoding="utf-8"), edicao), encoding="utf-8")
    return destino


def portao_da_busca(busca: BuscaDosCasos, edicao: dict) -> dict:
    """Portão 5: aplica a edição a uma cópia temporária da base, refaz a busca dos casos com gabarito e conta em quantos os três verbetes mudam, em quantos o verbete da
    causa certa entra ou sai dos três e quantos casos passariam a ler o verbete editado. Recusa a edição que tira o verbete certo de algum caso; no sinal de busca, recusa
    também o que não faz o caso de origem passar a receber o verbete. Nada é gravado fora da pasta temporária."""
    with tempfile.TemporaryDirectory() as tmp:
        copia = Path(tmp) / "biblioteca"
        evo.copiar_biblioteca(busca.base, copia)
        evo._limpar_gerados(copia)
        if edicao["operacao"] == OPERACAO_SINAL:
            aplicar_sinal_de_busca(copia, edicao)
        else:
            evo.aplicar_edicao(copia, edicao)
        depois = busca.tres(copia)
    antes, certo, verbete, origem = busca.antes, busca.certo, edicao["verbete"], edicao.get("caso")
    mudam = [c for c in antes if antes[c] != depois[c]]
    entra = sorted(c for c in mudam if certo[c] not in antes[c] and certo[c] in depois[c])
    sai = sorted(c for c in mudam if certo[c] in antes[c] and certo[c] not in depois[c])
    recebia = origem in antes and verbete in antes[origem]
    recebe = origem in depois and verbete in depois[origem]
    motivos = []
    if sai:
        motivos.append(f"o verbete da causa certa sai dos três entregues de {len(sai)} caso(s): {', '.join(sai)}")
    if edicao["operacao"] == OPERACAO_SINAL and (recebia or not recebe):
        motivos.append("o caso de origem já recebia o verbete, e o sinal não muda a busca dele" if recebia else "o caso de origem continua sem receber o verbete")
    return {"passa": not motivos, "motivo": "; ".join(motivos) or None, "casos_em_que_os_tres_verbetes_mudam": len(mudam), "verbete_certo_entra": len(entra),
            "verbete_certo_sai": len(sai), "casos_que_leriam_a_edicao": sum(1 for c in depois if verbete in depois[c]), "casos_que_ganham_o_verbete_certo": entra,
            "casos_que_perdem_o_verbete_certo": sai, "origem_recebe_o_verbete_antes": recebia, "origem_recebe_o_verbete_depois": recebe}


# ------------------------------------------------------------------ a corrida 20, só lida

def _pasta_da_corrida_20() -> Path:
    return caminhos.fase3(CORRIDA_20)["raiz"]


def base_da_corrida_20() -> Path:
    """A biblioteca de antes do lote da corrida 20 (a cópia que o diagnóstico dos 54 casos de aprendizado leu), em que cada edição é aplicada uma a uma."""
    return _pasta_da_corrida_20() / "bibliotecas" / executar_fase3._slug(MODELO) / f"epoca-{dv.VERSAO_CURADA}"


def edicoes_do_lote_da_corrida_20() -> list[dict]:
    """As 20 edições que passaram nos filtros da corrida 20, na ordem do lote: as aceitas e depois a segurada para revisão."""
    lote = json.loads((_pasta_da_corrida_20() / "lote.json").read_text(encoding="utf-8"))
    return list(lote.get("edicoes") or []) + list(lote.get("para_revisao") or [])


def propostas_da_corrida_20() -> list[dict]:
    """As propostas de edição da corrida 20, uma por bloco PROPOSTA, com o que os filtros de hoje fizeram com cada uma e, nas que viraram edição, o veredito da revisão
    humana do lote. Para se uma edição do lote não tiver linha na planilha de revisão, porque aí a comparação com a pessoa ficaria incompleta."""
    pasta = _pasta_da_corrida_20()
    vereditos = b4.vereditos_da_planilha((pasta / "revisao_do_lote.md").read_text(encoding="utf-8"))
    itens = []
    for r in executar_bateria.ler_jsonl(pasta / executar_fase3._slug(MODELO) / "propostas__E101.jsonl"):
        for bloco, dec in zip(r.get("propostas_parseadas") or [], r.get("decisoes") or []):
            edicao = dec.get("edicao")
            if dec.get("aceita"):
                destino = DESTINOS[0]
            elif dec.get("para_revisao"):
                destino = DESTINOS[1]
            else:
                destino = DESTINOS[2] if dec.get("filtro") is None else DESTINOS[3]
            veredito = None
            if edicao:
                chave = b4._chave_da_planilha(edicao)
                if chave not in vereditos:
                    raise SystemExit(f"a edição do caso {r['caso']} em [{edicao.get('verbete')}] passou nos filtros e não tem linha em revisao_do_lote.md")
                veredito = vereditos[chave][0]
            itens.append({"caso": r["caso"], "numero": dec.get("numero"), "operacao": dec.get("operacao"), "verbete": dec.get("verbete"),
                          "texto": (bloco.get("campos") or {}).get("TEXTO", ""), "destino": destino, "codigo": dec.get("motivo"), "edicao": edicao, "veredito": veredito})
    return itens


# ------------------------------------------------------------------ a medida M1

def _por_veredito(itens: list[dict], recusada) -> list[dict]:
    return [{"veredito": v, "edicoes": sum(1 for i in itens if i["veredito"] == v), "recusa": sum(1 for i in itens if i["veredito"] == v and recusada(i)),
             "passa": sum(1 for i in itens if i["veredito"] == v and not recusada(i))} for v in VEREDITOS]


def _etapa(nome: str, sobram: list[dict]) -> dict:
    return {"etapa": nome, "sobram": len(sobram), **{v: sum(1 for i in sobram if i["veredito"] == v) for v in VEREDITOS}}


def medir_m1(gerado_em: str | None = None) -> dict:
    """A medida M1: os portões 3, 4 e 5 aplicados às propostas da corrida 20. Os portões 3 e 4 leem o texto e valem para todas; o portão 5 precisa da edição, e só as que
    passaram nos filtros de hoje viraram edição. A comparação com a revisão humana é feita nessas: quantas erradas e parciais cada portão recusaria e quantas corretas
    perderia, cada um sozinho e os três em sequência."""
    limiares = ft.carregar_limiares()
    busca = BuscaDosCasos(base_da_corrida_20())
    itens = []
    for p in propostas_da_corrida_20():
        forma, texto = portao_da_forma(p["texto"]), portao_do_texto(p["texto"], limiares)
        resultado_da_busca = portao_da_busca(busca, p["edicao"]) if p["edicao"] else None
        itens.append({**{k: p[k] for k in ("caso", "numero", "operacao", "verbete", "texto", "destino", "codigo", "veredito")},
                      "forma": forma, "forma_pela_lista_da_pesquisa": p["texto"].strip().startswith(esn.VERBOS_DE_INSTRUCAO), "texto_passa": texto["passa"],
                      "texto_reprovados": texto["reprovados"], "alarme_flesch": texto["alarme_flesch"], "busca": resultado_da_busca})
    revisadas = [i for i in itens if i["veredito"] is not None]
    for i in revisadas:
        i["passa_nos_tres"] = bool(i["forma"]["passa"] and i["texto_passa"] and i["busca"]["passa"])
    recusada = {"forma": lambda i: not i["forma"]["passa"], "texto": lambda i: not i["texto_passa"], "busca": lambda i: i["busca"] is not None and not i["busca"]["passa"]}
    por_portao = []
    for portao in PORTOES:
        aplicaveis = [i for i in itens if portao != "busca" or i["busca"] is not None]
        por_veredito = _por_veredito(revisadas, recusada[portao])
        corretas = next(x for x in por_veredito if x["veredito"] == VEREDITOS[0])
        recusa_nas_revisadas = sum(1 for i in revisadas if recusada[portao](i))
        por_portao.append({"portao": portao, "nome": NOME_DO_PORTAO[portao], "regra": REGRA_DO_PORTAO[portao],
                           "nas_propostas": {"recusa": sum(1 for i in aplicaveis if recusada[portao](i)), "passa": sum(1 for i in aplicaveis if not recusada[portao](i)),
                                             "nao_se_aplica": len(itens) - len(aplicaveis)},
                           "nas_revisadas": {"recusa": recusa_nas_revisadas, "passa": len(revisadas) - recusa_nas_revisadas, "por_veredito": por_veredito},
                           "corretas": corretas["edicoes"], "corretas_perdidas": corretas["recusa"], "erradas_e_parciais": len(revisadas) - corretas["edicoes"],
                           "erradas_e_parciais_recusadas": recusa_nas_revisadas - corretas["recusa"]})
    depois_do_3 = [i for i in revisadas if i["forma"]["passa"]]
    depois_do_4 = [i for i in depois_do_3 if i["texto_passa"]]
    depois_do_5 = [i for i in depois_do_4 if i["busca"]["passa"]]
    em_sequencia = [_etapa("passaram nos filtros de hoje e foram revisadas", revisadas), _etapa("depois do portão 3 (forma de instrução)", depois_do_3),
                    _etapa("depois do portão 4 (filtros de texto)", depois_do_4), _etapa("depois do portão 5 (busca)", depois_do_5)]
    outras = [_etapa("só os portões 4 e 5, sem o da forma", [i for i in revisadas if i["texto_passa"] and i["busca"]["passa"]]),
              _etapa("só o portão 5, o da busca", [i for i in revisadas if i["busca"]["passa"]])]
    palavras = collections.Counter(i["forma"]["primeira_palavra"] or "(vazio)" for i in itens)
    recusa_da_palavra = {i["forma"]["primeira_palavra"] or "(vazio)": not i["forma"]["passa"] for i in itens}
    criterios = [{"criterio": m["chave"], "nome": m["nome"], "reprovadas": sum(1 for i in itens if m["chave"] in i["texto_reprovados"]),
                  "reprovadas_nas_revisadas": sum(1 for i in revisadas if m["chave"] in i["texto_reprovados"])} for m in ft.METRICAS if m["regra"] in ("ate", "zero")]
    com_busca = [i["busca"] for i in revisadas]
    forma, texto, busca_ = por_portao
    return {"metadados": {"gerado_em": gerado_em or time.strftime("%Y-%m-%dT%H:%M:%S"), "medida": MEDIDA, "corrida": CORRIDA_20},
            "o_que_e": ("Os portões 3, 4 e 5 da proposta do analista de documentação aplicados, sem modelo, às propostas de edição da corrida 20, contra a revisão humana do lote "
                        "(ficha 67, decisão 121). Os portões 3 e 4 leem o texto da proposta; o portão 5 aplica a edição a uma cópia da biblioteca de antes do lote e refaz a busca "
                        "dos casos com gabarito, e por isso só vale para as propostas que viraram edição."),
            "resumo": {"propostas": len(itens), "casos": len({i["caso"] for i in itens}), "revisadas": len(revisadas),
                       "por_veredito": {v: sum(1 for i in revisadas if i["veredito"] == v) for v in VEREDITOS},
                       "forma_recusa": forma["nas_propostas"]["recusa"], "forma_passa": forma["nas_propostas"]["passa"],
                       "forma_pela_lista_da_pesquisa": sum(1 for i in itens if i["forma_pela_lista_da_pesquisa"]),
                       "forma_pela_lista_da_pesquisa_nas_revisadas": sum(1 for i in revisadas if i["forma_pela_lista_da_pesquisa"]),
                       "texto_recusa": texto["nas_propostas"]["recusa"], "texto_com_alarme_flesch": sum(1 for i in itens if i["alarme_flesch"]),
                       "busca_recusa": busca_["nas_revisadas"]["recusa"], "sobram_depois_dos_tres": len(depois_do_5),
                       "sobram_sem_o_portao_da_forma": outras[0]["sobram"], "sinais_de_busca_na_corrida": sum(1 for i in itens if i["operacao"] == OPERACAO_SINAL)},
            "por_portao": por_portao, "em_sequencia": em_sequencia, "outras_sequencias": outras,
            "por_destino": [{"destino": d, "propostas": sum(1 for i in itens if i["destino"] == d), "forma_recusa": sum(1 for i in itens if i["destino"] == d and not i["forma"]["passa"]),
                             "texto_recusa": sum(1 for i in itens if i["destino"] == d and not i["texto_passa"])} for d in DESTINOS],
            "criterios_do_texto": criterios,
            "primeiras_palavras": [{"palavra": w, "propostas": n, "recusada_pela_forma": recusa_da_palavra[w]} for w, n in sorted(palavras.items(), key=lambda x: (-x[1], x[0]))],
            "busca": {"casos_com_gabarito": len(busca.casos), "base": evo.hash_biblioteca(busca.base), "edicoes": len(com_busca),
                      "edicoes_que_mudam_a_busca": sum(1 for b in com_busca if b["casos_em_que_os_tres_verbetes_mudam"]),
                      "verbete_certo_entra": sum(b["verbete_certo_entra"] for b in com_busca), "verbete_certo_sai": sum(b["verbete_certo_sai"] for b in com_busca),
                      "edicoes_recusadas": sum(1 for b in com_busca if not b["passa"])},
            "revisadas": revisadas, "propostas": itens}


def _sim(v: bool | None) -> str:
    return "n/a" if v is None else ("passa" if v else "recusa")


def _por_extenso(etapa: dict) -> str:
    """Os vereditos das edições que sobram numa etapa, com o plural certo ("1 correta, 8 parciais e 6 erradas")."""
    nomes = (("Correta", "correta", "corretas"), ("Parcial", "parcial", "parciais"), ("Errada", "errada", "erradas"))
    partes = [f"{etapa[chave]} {um if etapa[chave] == 1 else varios}" for chave, um, varios in nomes]
    return f"{partes[0]}, {partes[1]} e {partes[2]}"


def render_m1(dado: dict) -> str:
    r, n = dado["resumo"], ct._n
    v = r["por_veredito"]
    forma, texto, busca = dado["por_portao"]
    seq, outras = dado["em_sequencia"], dado["outras_sequencias"]

    def contra_a_revisao(p: dict) -> str:
        pv = {x["veredito"]: x for x in p["nas_revisadas"]["por_veredito"]}
        return (f"recusaria {n(pv['Errada']['recusa'])} das {n(pv['Errada']['edicoes'])} erradas e {n(pv['Parcial']['recusa'])} das {n(pv['Parcial']['edicoes'])} parciais, e perderia "
                f"{n(pv['Correta']['recusa'])} das {n(pv['Correta']['edicoes'])} corretas")

    texto_md = [(f"Medida {MEDIDA} da proposta do analista de documentação (ficha 67, decisão 121), sem modelo. Na corrida 20 o modelo fez {n(r['propostas'])} propostas de edição em "
                 f"{n(r['casos'])} casos; {n(r['revisadas'])} passaram nos filtros de hoje e a revisão humana do lote julgou {n(v['Correta'])} corretas, {n(v['Parcial'])} parciais e "
                 f"{n(v['Errada'])} erradas. Aqui os três portões novos da proposta são aplicados a essas propostas: o portão 3 e o portão 4 leem o texto e valem para as "
                 f"{n(r['propostas'])}; o portão 5 aplica a edição a uma cópia da biblioteca de antes do lote e refaz a busca de {n(dado['busca']['casos_com_gabarito'])} casos com "
                 f"gabarito, e por isso só vale para as {n(r['revisadas'])} que viraram edição."),
                "", (f"Cada portão sozinho, contra a revisão humana das {n(r['revisadas'])}. O portão 3, a forma de instrução, {contra_a_revisao(forma)}; nas {n(r['propostas'])} propostas "
                     f"ele recusaria {n(r['forma_recusa'])} (a contagem publicada pela pesquisa, com cinco radicais, dava {n(r['forma_pela_lista_da_pesquisa'])}). O portão 4, os filtros "
                     f"de texto, {contra_a_revisao(texto)}; nas {n(r['propostas'])} ele recusaria {n(r['texto_recusa'])}. O portão 5, a busca, {contra_a_revisao(busca)}: nas "
                     f"{n(dado['busca']['edicoes'])} edições o verbete da causa certa sai dos três entregues {n(dado['busca']['verbete_certo_sai'])} vezes e entra "
                     f"{n(dado['busca']['verbete_certo_entra'])}."),
                "", (f"Os três em sequência. Das {n(seq[0]['sobram'])} edições, sobram {n(seq[1]['sobram'])} depois do portão 3, {n(seq[2]['sobram'])} depois do portão 4 e "
                     f"{n(seq[3]['sobram'])} depois do portão 5: {_por_extenso(seq[3])}. Sem o portão da forma, os portões 4 e 5 deixariam {n(outras[0]['sobram'])}: "
                     f"{_por_extenso(outras[0])}."),
                "", ("Como ler. O portão da forma, aplicado ao que o modelo escreve hoje, esvazia o lote e leva junto as edições corretas: ele só faz sentido com um prompt que peça a frase "
                     "como ela vai ficar no verbete, que é o que a corrida 27 mede. Os portões em código olham a forma do texto e o efeito na busca; nenhum deles diz se a afirmação é "
                     "verdadeira, e a revisão de uma pessoa continua sendo a porta final. A corrida 20 não tem proposta do tipo sinal de busca, então a segunda regra do portão 5 (o caso "
                     "de origem tem de passar a receber o verbete) não foi exercitada aqui.")]

    def linha_do_portao(p: dict) -> list[str]:
        pv = {x["veredito"]: x for x in p["nas_revisadas"]["por_veredito"]}
        return [p["nome"], p["regra"], n(p["nas_propostas"]["recusa"]), n(p["nas_propostas"]["passa"]), n(p["nas_propostas"]["nao_se_aplica"]), n(p["nas_revisadas"]["recusa"]),
                f"{n(pv['Errada']['recusa'])} de {n(pv['Errada']['edicoes'])}", f"{n(pv['Parcial']['recusa'])} de {n(pv['Parcial']['edicoes'])}",
                f"{n(pv['Correta']['recusa'])} de {n(pv['Correta']['edicoes'])}"]

    blocos = [
        a3b.tab(f"{PREFIXO_M1}resumo", ["Propostas", "Casos", "Revisadas por uma pessoa", "Corretas", "Parciais", "Erradas", "O portão 3 recusaria", "O portão 4 recusaria",
                                       "O portão 5 recusaria (das revisadas)", "Sobram depois dos três", "Sobram sem o portão da forma"],
                [[n(r["propostas"]), n(r["casos"]), n(r["revisadas"]), n(v["Correta"]), n(v["Parcial"]), n(v["Errada"]), n(r["forma_recusa"]), n(r["texto_recusa"]), n(r["busca_recusa"]),
                  n(r["sobram_depois_dos_tres"]), n(r["sobram_sem_o_portao_da_forma"])]]),
        a3b.tab(f"{PREFIXO_M1}portoes", ["Portão", "Regra", "Recusa nas propostas", "Passa nas propostas", "Não se aplica", "Recusa nas revisadas", "Erradas recusadas",
                                        "Parciais recusadas", "Corretas perdidas"], [linha_do_portao(p) for p in dado["por_portao"]]),
        a3b.tab(f"{PREFIXO_M1}sequencia", ["Etapa", "Edições que sobram", "Corretas", "Parciais", "Erradas"],
                [[x["etapa"], n(x["sobram"]), n(x["Correta"]), n(x["Parcial"]), n(x["Errada"])] for x in seq + outras]),
        a3b.tab(f"{PREFIXO_M1}destino", ["O que os filtros de hoje fizeram", "Propostas", "O portão 3 recusaria", "O portão 4 recusaria"],
                [[x["destino"], n(x["propostas"]), n(x["forma_recusa"]), n(x["texto_recusa"])] for x in dado["por_destino"]]),
        a3b.tab(f"{PREFIXO_M1}criterios", ["Medida do portão 4", "Propostas reprovadas", "Reprovadas entre as revisadas"],
                [[x["nome"], n(x["reprovadas"]), n(x["reprovadas_nas_revisadas"])] for x in dado["criterios_do_texto"]]),
        a3b.tab(f"{PREFIXO_M1}palavras", ["Primeira palavra do texto", "Propostas", "O portão 3"],
                [[f"`{x['palavra']}`", n(x["propostas"]), "recusa" if x["recusada_pela_forma"] else "passa"] for x in dado["primeiras_palavras"]]),
        a3b.tab(f"{PREFIXO_M1}revisadas", ["Caso", "Verbete", "Operação", "Revisão humana", "Portão 3", "Portão 4", "Portão 5", "Casos em que os três verbetes mudam",
                                          "Verbete certo entra", "Verbete certo sai", "Passa nos três", "Texto"],
                [[f"`{i['caso']}`", f"`{i['verbete']}`", n(i["operacao"]), i["veredito"], _sim(i["forma"]["passa"]), _sim(i["texto_passa"]), _sim(i["busca"]["passa"]),
                  n(i["busca"]["casos_em_que_os_tres_verbetes_mudam"]), n(i["busca"]["verbete_certo_entra"]), n(i["busca"]["verbete_certo_sai"]), "sim" if i["passa_nos_tres"] else "não",
                  b4._esc(i["texto"])] for i in dado["revisadas"]]),
        a3b.tab(f"{PREFIXO_M1}propostas", ["Caso", "Proposta", "Operação", "Verbete", "O que os filtros de hoje fizeram", "Código da recusa", "Revisão humana", "Portão 3", "Portão 4",
                                          "Medidas reprovadas no portão 4", "Portão 5", "Texto"],
                [[f"`{i['caso']}`", n(i["numero"]), n(i["operacao"]), f"`{i['verbete']}`", i["destino"], n(i["codigo"]) if i["codigo"] else "", i["veredito"] or "",
                  _sim(i["forma"]["passa"]), _sim(i["texto_passa"]), ", ".join(i["texto_reprovados"]), _sim(i["busca"]["passa"] if i["busca"] else None), b4._esc(i["texto"])]
                 for i in dado["propostas"]]),
    ]
    cab = pf.cabecalho(f"Medida {MEDIDA}: os portões 3, 4 e 5 nas propostas de edição da corrida 20", "portoes_de_edicao.py --m1",
                       "`fase4_biblioteca/` (propostas, lote e revisão do lote) e `limiares_texto.json`", dado["metadados"]["gerado_em"][:10])
    return "\n".join(cab + [""] + texto_md + [""] + blocos) + "\n"


# ------------------------------------------------------------------ linha de comando

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--m1", action="store_true", help=f"aplica os portões às propostas da corrida 20 e grava resultados_alvo/fase4/{NOME_M1}.json e .md")
    ap.add_argument("--check", action="store_true", help="com --m1: regera e compara com o gravado, sem gravar")
    args = ap.parse_args(argv)
    if args.m1:
        import avaliar_fase4 as av
        dado = medir_m1()
        return pf.fechar(NOME_M1, dado, render_m1(dado), PREFIXO_M1, check=args.check, pasta=caminhos.RESULTADOS / "fase4", doc=av.RELATORIO)
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
