#!/usr/bin/env python3
# ! Alteração de IA - Revisar: arquivo novo (03/11/2026, Fase 4, pacote P5): a biblioteca em produção e o ciclo de
# correção do plano aprovado (seção 3.7). A L1 curada (`biblioteca_producao/`) continua a biblioteca de partida e só
# cresce por acréscimo validado: o validador da Fase 3 (`evolucao_biblioteca.validar_proposta`, 30 códigos, congelado)
# e, depois dele, os 13 filtros em código da decisão 65 (`FILTROS`), na ordem fixa: evidência obrigatória (o MOTIVO
# cita a evidência do caso e a retificação tem TRECHO); atomicidade (uma alegação curta, sem lista); abstenção válida
# ("NENHUMA" é saída contada à parte); fonte confiável (mensagem entre aspas e endpoint conferidos contra o código das
# cobaias e o `openapi.json`); granularidade (retificar ou só sinalizar; sinalização sem trecho específico é recusada);
# peso por tipo de edição com orçamento por verbete e rodada; redundância por n-gramas contra o verbete de destino;
# proveniência por edição (caso, modelo, época, data); auditoria por etapa (admissão separada da atualização, e nenhuma
# proposta sobre um caso que o verbete já registra como corrigido); resolução determinística de conflito entre edições
# do mesmo trecho; métricas por rodada; revisão humana amostral dirigida (planilha de revisão, porta final antes de
# promover); e a regra dos 40% (nota em verbete presente em 40% ou mais dos contextos da calibração vai para revisão
# humana antes de entrar). Antes de todos, a regra da especificação da trilha (seção 10): nenhum trecho literal de
# corpo HTTP entra numa proposta. Cada verbete tem origem (humano, modelo) e estado (`status`: não corrigido ou
# corrigido); a operação "correção" acrescenta as seções "Solução sugerida" e "Solução aplicada" com data, muda só a
# linha do status (que só avança) e nunca remove texto; o gatilho marca `corrigido` só com a evidência dos dois diffs
# (o fio e a árvore mudaram entre a corrida que falhava e a que passou); a recuperação por id traz ao contexto os
# verbetes ligados ao caso pelas notas `[E1 · <caso> · …]` ou pelo caso de origem; o lote só entra depois da
# reavaliação nos 36 inéditos (regra R5: b maior ou igual a c; senão fica em espera com o motivo). Só biblioteca padrão.
# ! Motivo: plano aprovado, seções 3.2 (linha "Biblioteca em produção"), 3.7 e 5 (P5: "cada filtro em código recusa o
# exemplo mínimo que o motiva e aceita o contraexemplo; a operação correção nunca remove bytes e só avança o estado; o
# gatilho marca corrigido só com a evidência dos dois diffs; a recuperação por id traz as notas do caso e nada mais; a
# regra dos 40% manda para revisão a nota do verbete mais recuperado da calibração; um lote com c maior que b fica em
# espera; nenhum texto de corpo HTTP entra em proposta sem validação"); roadmap §4.2 (requisito do Eric, 28/09/2026);
# fichas 32 (decisão 79) e 26; a sonda de 28/09 (roadmap §3) mostrou que, sem isso, o modelo repete as edições antigas
# e nada registra a correção. `evolucao_biblioteca.py`, `estrategias.py` e `executar_fase3.py` continuam congelados:
# são importados, nunca alterados.
"""Biblioteca em produção e ciclo de correção (Fase 4, P5).

Uso direto (em Programacao/AgenteCore/experimentos):
  python biblioteca_fase4.py --planilha <saida>            escreve a planilha de revisão humana do lote de uma corrida
  python biblioteca_fase4.py --promover <saida>            aplica o lote aceito (R5) e revisado à biblioteca de produção
  python biblioteca_fase4.py --espera                       move para aprendidos_em_espera/ os verbetes aprendidos nunca recuperados (ficha 32)
O modo `biblioteca` de executar_fase4.py é quem usa as funções daqui durante a corrida 20."""
from __future__ import annotations

import argparse
import contextlib
import datetime as dt
import hashlib
import json
import math
import re
import shutil
import sys
from pathlib import Path

import avaliar
import biblioteca as bib
import caminhos
import caso_ao_vivo as cv
import estrategias
import evolucao_biblioteca as evo
import executar_bateria
import executar_fase3
import poda
import recuperacao as rec
import trilha as tr
import validar_banco

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:  # noqa: BLE001 - console sem reconfigure: segue como está
        pass

EXP = Path(__file__).resolve().parent
RAIZ = EXP.parent.parent.parent
PASTA_CURADA = EXP.parent / "biblioteca_producao"
PASTA_DE_ESPERA = EXP.parent / "aprendidos_em_espera"
FIXTURES = EXP / "fixtures_fase4"
PASTAS_DE_CODIGO = (RAIZ / "Programacao" / "CobaiaAPI" / "app", RAIZ / "Programacao" / "CobaiaFront")
EXTENSOES_DE_CODIGO = (".py", ".php", ".js", ".html")

ORIGENS = ("humano", "modelo", "sistema_sob_teste")
ESTADOS = ("nao_corrigido", "corrigido")
OPERACAO_CORRECAO = "correcao"
FILTROS = ("evidencia_obrigatoria", "atomicidade", "abstencao_valida", "fonte_confiavel", "granularidade", "peso_por_tipo",
           "redundancia", "proveniencia", "auditoria_por_etapa", "conflito_deterministico", "metricas_por_rodada",
           "revisao_humana_amostral", "regra_dos_40")
# os filtros que decidem proposta a proposta, na ordem; os outros cinco agem na rodada (abstenção, conflito, métricas,
# revisão amostral) ou são a regra dos 40%, que segura em vez de recusar
FILTROS_POR_PROPOSTA = ("evidencia_obrigatoria", "atomicidade", "fonte_confiavel", "granularidade", "peso_por_tipo", "redundancia",
                        "proveniencia", "auditoria_por_etapa")
CODIGOS_P5 = ("texto_de_origem_proibida", "sem_evidencia_do_caso", "texto_nao_atomico", "mensagem_nao_encontrada_no_codigo",
              "endpoint_fora_do_openapi", "sinalizacao_sem_trecho", "peso_acima_do_orcamento", "redundante", "sem_proveniencia",
              "proposta_sobre_caso_corrigido", "superada_por_conflito", "para_revisao_humana")
CODIGO_DE_REVISAO = "para_revisao_humana"
PESO_POR_TIPO = {"nota": 1, "sinalizacao": 1, "retificacao": 2, "novo_verbete": 3}
ORCAMENTO_DE_PESO_POR_VERBETE = 4         # por rodada: uma retificação e duas notas, ou um verbete novo e uma nota
MAX_FRASES = 2
MAX_ENUMERACOES = 1                        # "; " separando itens: duas ou mais viram lista
N_GRAMA = 3
LIMIAR_REDUNDANCIA = 0.5
PARCELA_PARA_REVISAO = 0.4                 # achado 4.42: contrato-produto estava em 15 dos 36 contextos
MIN_CHARS_TRECHO_PROIBIDO = 20
MIN_CHARS_MENSAGEM = 12
MIN_CHARS_TRECHO = 15                      # o mesmo mínimo de evolucao_biblioteca (retificacao_sem_trecho)
TETO_CHARS_CORRECOES = bib.TETO_CHARS_CORRECOES
SECAO_SUGERIDA, SECAO_APLICADA = bib.SECOES_DA_CORRECAO
SEM_NOTA = "(sem nota do modelo para este caso)"
AMOSTRA_DE_REVISAO = 6
CELULA_EM_BRANCO = "(em branco)"
VEREDITOS_DA_REVISAO = ("Correta", "Parcial", "Errada")
REGRA_R4 = "precisão e revocação da marca corrigido contra o conjunto conhecido de modos desligados (sem limiar pré-registrado: é medida)"
REGRA_R5 = ("um lote de acréscimos entra se, na reavaliação nos 36 inéditos, o número de casos que passam a acertar for maior ou igual ao "
            "dos que passam a errar (b maior ou igual a c); senão o lote fica em espera com o motivo")
ORIGEM_RE = re.compile(r"a partir do caso ([a-z]+-\d+)")
ASPAS_RE = re.compile(r'"([^"\n]{%d,})"|\'([^\'\n]{%d,})\'|“([^”\n]{%d,})”' % (MIN_CHARS_MENSAGEM, MIN_CHARS_MENSAGEM, MIN_CHARS_MENSAGEM))
FRASE_RE = re.compile(r"[.!?]+(?:\s+|$)")
SINALIZACAO_RE = re.compile(r"pode(m)? estar|verificar|conferir se|possivelmente|desatualizad|talvez|revisar|a confirmar|checar se")
MARCAS_DE_CORRECAO = ("solucao aplicada", "corrigid", "nao ocorre mais", "deixou de ocorrer", "ja registra", "ja esta documentad", "ja foi resolvid")

_FONTES: dict = {}


def hoje() -> str:
    return dt.date.today().isoformat()


# ------------------------------------------------------------------ origem, estado, casos ligados e recuperação por id

def origem_do_verbete(v: dict) -> str:
    """'modelo' para os verbetes escritos pelo modelo na Fase 3 (pasta aprendidos/, tipo aprendido); 'humano' para os
    escritos à mão. Texto do sistema sob teste nunca vira verbete (especificação, seção 10)."""
    if v.get("pasta") == evo.PASTA_APRENDIDOS or v.get("meta", {}).get("tipo") == "aprendido":
        return "modelo"
    return "humano"


def estado_do_verbete(v: dict) -> str:
    """O estado controlado do verbete: 'corrigido' só depois da operação de correção; qualquer outro status (ativo,
    nao_corrigido) vale como não corrigido para o ciclo de correção."""
    return "corrigido" if v.get("meta", {}).get("status") == "corrigido" else "nao_corrigido"


def _texto_do_verbete(v: dict) -> str:
    caminho = v.get("caminho")
    return caminho.read_text(encoding="utf-8") if isinstance(caminho, Path) and caminho.exists() else ""


def caso_de_origem(v: dict) -> str | None:
    """O caso de origem de um verbete escrito pelo modelo ("criado pelo modelo ... a partir do caso efe-13")."""
    m = ORIGEM_RE.search(_texto_do_verbete(v))
    return m.group(1) if m else None


def casos_do_verbete(v: dict) -> list[str]:
    """Os casos ligados ao verbete, sem repetição e na ordem em que aparecem: os das notas `[E<n> · <caso> · …]` e,
    nos verbetes escritos pelo modelo, o caso de origem."""
    saida: list[str] = []
    for n in bib.notas(v):
        if n["caso"] not in saida:
            saida.append(n["caso"])
    origem = caso_de_origem(v)
    if origem and origem not in saida:
        saida.append(origem)
    return saida


def verbetes_do_caso(verbetes: list[dict], caso_id: str) -> list[dict]:
    """A recuperação por id: os verbetes ligados ao caso (ficha 32; plano, seção 3.7, item 4), na ordem da biblioteca."""
    return [v for v in verbetes if caso_id in casos_do_verbete(v)]


def notas_do_caso(verbetes: list[dict], caso_id: str) -> list[dict]:
    """As notas escritas a partir do caso, com o verbete em que estão, e nada mais."""
    return [{"verbete": v["id"], **n} for v in verbetes for n in bib.notas(v) if n["caso"] == caso_id]


def sugestao_do_modelo(v: dict, caso_id: str) -> str:
    """O que o modelo escreveu a partir do caso: o texto das notas do caso neste verbete ou, num verbete criado a partir
    do caso, o resumo do verbete; vazio quando o caso não está ligado ao verbete."""
    textos = [n["texto"] for n in bib.notas(v) if n["caso"] == caso_id]
    if textos:
        return " ".join(textos)
    if caso_de_origem(v) == caso_id:
        return v["secoes"].get("Resumo", "").replace("\n", " ").strip()
    return ""


def casos_corrigidos(v: dict) -> list[str]:
    return [c["caso"] for c in bib.correcoes(v)]


def contexto_com_id(verbetes: list[dict], indice: rec.Indice, caso: dict, k: int = 3, caso_id: str | None = None) -> dict:
    """O contexto ao vivo (os k da busca) mais os verbetes recuperados pelo id do caso, depois dos k e sem repetição."""
    import diagnostico_ao_vivo as dv
    return dv.contexto_ao_vivo(verbetes, indice, caso, k, extras=verbetes_do_caso(verbetes, caso_id or caso["id"]))


@contextlib.contextmanager
def com_recuperacao_por_id(verbetes: list[dict] | None = None):
    """Durante o bloco, executar_fase3.contexto_e_prompt (o executor congelado da Fase 3, usado pela sonda de
    correção) acrescenta ao contexto A2 os verbetes ligados ao caso pelo id, depois dos k da busca; fora do bloco,
    o executor volta ao normal. Os verbetes ligados são procurados na biblioteca que a chamada recebe."""
    original = executar_fase3.contexto_e_prompt

    def trocado(verbetes_: list[dict], indice: rec.Indice, caso: dict, k: int) -> tuple[dict, str]:
        ctx, prompt = original(verbetes_, indice, caso, k)
        extras = [v for v in verbetes_do_caso(verbetes_ or verbetes or [], caso["id"]) if v["id"] not in ctx["verbetes_ids"]]
        if not extras:
            return ctx, prompt
        por_id = {v["id"]: v for v in verbetes_}
        sel = [por_id[i] for i in ctx["verbetes_ids"] if i in por_id] + extras
        ctx = {**ctx, "texto": rec._envelope(sel), "verbetes_ids": [v["id"] for v in sel], "por_id": [v["id"] for v in extras]}
        return ctx, estrategias.linear_com_biblioteca(caso, ctx["texto"])

    executar_fase3.contexto_e_prompt = trocado
    try:
        yield
    finally:
        executar_fase3.contexto_e_prompt = original


# ------------------------------------------------------------------ a calibração: parcela de contextos e os aprendidos

def parcela_nos_contextos(registros: list[dict]) -> dict[str, float]:
    """Para cada verbete, a parcela dos contextos (registros de diagnóstico) em que a busca o entregou."""
    if not registros:
        return {}
    contagem: dict[str, int] = {}
    for r in registros:
        for i in r.get("verbetes_ids") or []:
            contagem[i] = contagem.get(i, 0) + 1
    return {i: n / len(registros) for i, n in contagem.items()}


def verbetes_para_revisao(parcelas: dict[str, float], limiar: float = PARCELA_PARA_REVISAO) -> list[str]:
    """Os verbetes cuja nota vai para revisão humana antes de entrar: parcela maior ou igual ao limiar, dos mais aos
    menos recuperados."""
    return sorted((v for v, p in parcelas.items() if p >= limiar), key=lambda v: (-parcelas[v], v))


def recuperacao_dos_aprendidos(registros: list[dict], aprendidos: list[str]) -> dict[str, int]:
    """Quantas vezes cada verbete aprendido entrou num contexto da calibração (ficha 32)."""
    saida = {a: 0 for a in aprendidos}
    for r in registros:
        for i in r.get("verbetes_ids") or []:
            if i in saida:
                saida[i] += 1
    return saida


def aprendidos_sem_recuperacao(recuperacao: dict[str, int]) -> list[str]:
    return sorted(a for a, n in recuperacao.items() if n == 0)


# ------------------------------------------------------------------ os filtros em código da decisão 65

def _campo(campos: dict, nome: str) -> str:
    return re.sub(r"\s+", " ", str(campos.get(nome) or "")).strip()


def termos_de_evidencia(caso: dict) -> set[str]:
    """Os termos que uma proposta pode citar como evidência do caso: o campo afetado, o status, a rota (inteira e o
    último trecho), as palavras do sintoma e da observação, as chaves do corpo JSON e os sinais calculados em código."""
    e = caso.get("entrada") or {}
    termos: set[str] = set()
    campo = (caso.get("gabarito") or {}).get("campo_afetado")
    if campo:
        termos.add(bib.normalizar(str(campo)))
    if e.get("status") is not None:
        termos.add(str(e["status"]))
    for chave in ("sintoma", "observacao", "seletor_quebrado"):
        termos.update(t for t in bib.tokens(str(e.get(chave) or "")) if len(t) >= 3)
    req = str(e.get("requisicao") or "")
    m = re.search(r"(/api/[^\s?|)]+)", req)
    if m:
        termos.add(m.group(1).lower())
        termos.add(m.group(1).rstrip("/").rsplit("/", 1)[-1].lower())
    corpo = e.get("corpo")
    if isinstance(corpo, str) and corpo.strip():
        try:
            dado = json.loads(corpo)
        except ValueError:
            dado = None
        itens = dado if isinstance(dado, list) else [dado] if isinstance(dado, dict) else []
        for item in itens[:3]:
            if isinstance(item, dict):
                termos.update(bib.normalizar(str(k)) for k in item)
    termos.update(t for t in bib.tokens(" ".join(rec.sinais_deterministicos(caso))) if len(t) >= 3)
    return termos


def filtro_evidencia_obrigatoria(campos: dict, caso: dict) -> dict | None:
    """O MOTIVO precisa citar ao menos um termo da evidência do caso, e a retificação precisa do TRECHO."""
    if _campo(campos, "OPERACAO").lower() == "retificacao" and len(evo._sem_aspas_delimitadoras(_campo(campos, "TRECHO"))) < MIN_CHARS_TRECHO:
        return {"codigo": "sem_evidencia_do_caso", "detalhe": f"retificação sem TRECHO de ao menos {MIN_CHARS_TRECHO} caracteres"}
    motivo = _campo(campos, "MOTIVO")
    termos = termos_de_evidencia(caso)
    citados = sorted(t for t in set(bib.tokens(motivo)) | {bib.normalizar(motivo)} if t in termos)
    if not citados:
        return {"codigo": "sem_evidencia_do_caso", "detalhe": "o MOTIVO não cita nenhum termo da evidência do caso (campo, status, rota, sintoma, chaves do corpo)"}
    return None


def filtro_atomicidade(campos: dict) -> dict | None:
    """O TEXTO traz uma alegação: no máximo duas frases e sem enumeração."""
    texto = _campo(campos, "TEXTO")
    frases = [f for f in FRASE_RE.split(texto) if f.strip()]
    if len(frases) > MAX_FRASES:
        return {"codigo": "texto_nao_atomico", "detalhe": f"{len(frases)} frases no TEXTO (máximo {MAX_FRASES})"}
    if texto.count("; ") > MAX_ENUMERACOES or re.search(r"(^|\s)(\d\)|[a-z]\)|- )", texto):
        return {"codigo": "texto_nao_atomico", "detalhe": "o TEXTO enumera itens; uma alegação por proposta"}
    return None


def classificar_resposta(parseado: dict) -> str:
    """'abstencao' (NENHUMA, saída válida), 'propostas' (há bloco PROPOSTA) ou 'sem_bloco'."""
    if parseado.get("blocos"):
        return "propostas"
    return "abstencao" if parseado.get("nenhuma") else "sem_bloco"


def fontes_das_cobaias() -> str:
    """O código das duas cobaias (CobaiaAPI/app e CobaiaFront: .py, .php, .js, .html) e o openapi.json, normalizados
    como bib.normalizar, num texto só, lido uma vez por processo."""
    if "texto" not in _FONTES:
        partes = []
        for pasta in PASTAS_DE_CODIGO:
            for arq in sorted(pasta.rglob("*")):
                if arq.is_file() and arq.suffix in EXTENSOES_DE_CODIGO and ".venv" not in arq.parts and "vendor" not in arq.parts:
                    try:
                        partes.append(arq.read_text(encoding="utf-8", errors="replace"))
                    except OSError:
                        continue
        if (FIXTURES / "openapi.json").exists():
            partes.append((FIXTURES / "openapi.json").read_text(encoding="utf-8"))
        _FONTES["texto"] = bib.normalizar("\n".join(partes))
    return _FONTES["texto"]


def rotas_do_openapi() -> set[str]:
    """As rotas do openapi.json das cobaias na forma de bib.ENDPOINTS: 'GET /api/produtos/{id}'."""
    arq = FIXTURES / "openapi.json"
    if not arq.exists():
        return set(bib.ENDPOINTS)
    dado = json.loads(arq.read_text(encoding="utf-8"))
    rotas = set()
    for caminho, metodos in (dado.get("paths") or {}).items():
        rota = re.sub(r"\{[^}]+\}", "{id}", caminho)
        for metodo in metodos:
            rotas.add(f"{metodo.upper()} {rota}")
    return rotas


def filtro_fonte_confiavel(campos: dict, fontes: str, rotas: set[str]) -> dict | None:
    """Toda mensagem entre aspas (12 caracteres ou mais) e toda rota citadas no TEXTO existem no código ou no openapi."""
    texto = _campo(campos, "TEXTO")
    for m in ASPAS_RE.finditer(texto):
        mensagem = next(g for g in m.groups() if g)
        if bib.normalizar(mensagem) not in fontes:
            return {"codigo": "mensagem_nao_encontrada_no_codigo", "detalhe": f"a mensagem \"{mensagem[:60]}\" não está no código das cobaias nem no openapi.json"}
    for verbo, caminho in evo.ENDPOINT_CITADO_RE.findall(texto):
        rota = re.sub(r"/\d+(?=/|$)", "/{id}", caminho.rstrip(".,;:!?)"))
        if f"{verbo} {rota}" not in rotas:
            return {"codigo": "endpoint_fora_do_openapi", "detalhe": f"a rota {verbo} {rota} não está no openapi.json"}
    return None


def granularidade(campos: dict) -> str | None:
    """Numa retificação: 'retificar' (propõe o texto certo) ou 'sinalizar' (só aponta o trecho como suspeito)."""
    if _campo(campos, "OPERACAO").lower() != "retificacao":
        return None
    return "sinalizar" if SINALIZACAO_RE.search(bib.normalizar(_campo(campos, "TEXTO"))) else "retificar"


def filtro_granularidade(campos: dict, alvo: dict | None) -> dict | None:
    """Uma sinalização precisa de trecho específico: TRECHO que é uma seção inteira ou mais de metade do verbete é recusado."""
    if granularidade(campos) != "sinalizar" or alvo is None:
        return None
    trecho = bib.normalizar(evo._sem_aspas_delimitadoras(_campo(campos, "TRECHO")))
    secoes = {bib.normalizar(s.replace("\n", " ")) for s in alvo.get("secoes", {}).values() if s}
    base = bib.normalizar(bib.render_base(alvo))
    if trecho in secoes or (base and len(trecho) > len(base) / 2):
        return {"codigo": "sinalizacao_sem_trecho", "detalhe": "a sinalização aponta uma seção inteira, não um trecho"}
    return None


def peso_da_edicao(operacao: str, granularidade_: str | None) -> int:
    if operacao == "retificacao" and granularidade_ == "sinalizar":
        return PESO_POR_TIPO["sinalizacao"]
    return PESO_POR_TIPO.get(operacao, 1)


def filtro_peso_por_tipo(operacao: str, granularidade_: str | None, verbete_id: str, pesos_usados: dict, orcamento: int = ORCAMENTO_DE_PESO_POR_VERBETE) -> dict | None:
    """O peso da edição somado ao já aceito no verbete nesta rodada não passa do orçamento."""
    peso = peso_da_edicao(operacao, granularidade_)
    usado = pesos_usados.get(verbete_id, 0)
    if usado + peso > orcamento:
        return {"codigo": "peso_acima_do_orcamento", "detalhe": f"[{verbete_id}] já tem peso {usado} nesta rodada; mais {peso} passaria do orçamento {orcamento}"}
    return None


def _ngramas(texto: str, n: int = N_GRAMA) -> set[tuple[str, ...]]:
    palavras = bib.tokens(texto)
    return {tuple(palavras[i:i + n]) for i in range(len(palavras) - n + 1)}


def similaridade_ngramas(a: str, b: str, n: int = N_GRAMA) -> float:
    """A parcela dos n-gramas de palavras de `a` que aparecem em `b` (0 quando `a` tem menos de n palavras)."""
    ga = _ngramas(a, n)
    if not ga:
        return 0.0
    return len(ga & _ngramas(b, n)) / len(ga)


def filtro_redundancia(campos: dict, alvo: dict | None, limiar: float = LIMIAR_REDUNDANCIA) -> dict | None:
    """Paráfrase do que o verbete de destino já diz (notas incluídas) é recusada."""
    if alvo is None:
        return None
    s = similaridade_ngramas(_campo(campos, "TEXTO"), bib.render(alvo))
    if s >= limiar:
        return {"codigo": "redundante", "detalhe": f"{s:.0%} dos {N_GRAMA}-gramas do TEXTO já estão em [{alvo['id']}]"}
    return None


def proveniencia(edicao: dict, data: str) -> dict:
    return {"origem": "modelo", "caso": edicao.get("caso"), "modelo": edicao.get("modelo"), "epoca": edicao.get("epoca"), "data": data}


def filtro_proveniencia(edicao: dict, casos_da_rodada: set[str]) -> dict | None:
    """Toda edição leva o caso de origem (um caso desta rodada), o modelo e a época."""
    caso = edicao.get("caso")
    if not caso or caso not in casos_da_rodada or not edicao.get("modelo") or edicao.get("epoca") is None:
        return {"codigo": "sem_proveniencia", "detalhe": f"edição sem caso de origem desta rodada, modelo ou época (caso {caso!r})"}
    return None


def filtro_auditoria_por_etapa(verbete_id: str, caso_id: str, corrigidos: dict[str, list[str]]) -> dict | None:
    """Uma proposta nova sobre um caso que o verbete já registra como corrigido é a edição antiga voltando (sonda de 28/09)."""
    if caso_id in (corrigidos.get(verbete_id) or []):
        return {"codigo": "proposta_sobre_caso_corrigido", "detalhe": f"[{verbete_id}] já registra o caso {caso_id} como corrigido"}
    return None


def auditoria(verbetes: list[dict], corrigidos: dict[str, list[str]], admitidas: list[dict]) -> dict:
    """A auditoria por etapa: admissão (o que entrou nesta rodada) e atualização (o que já estava e pode ter ficado
    obsoleto: os verbetes com casos corrigidos e as notas desses casos)."""
    por_id = {v["id"]: v for v in verbetes}
    atualizacao = []
    for vid, casos in sorted(corrigidos.items()):
        v = por_id.get(vid)
        notas = [n for n in bib.notas(v)] if v else []
        atualizacao.append({"verbete": vid, "casos_corrigidos": list(casos), "notas_do_caso": sum(1 for n in notas if n["caso"] in casos),
                            "notas_no_verbete": len(notas)})
    return {"admissao": list(admitidas), "atualizacao": atualizacao}


_RANQUE_DA_EVIDENCIA = {"correcao": 2, "retificacao": 1, "nota": 0}


def resolver_conflito(edicoes: list[dict]) -> list[dict]:
    """Edições sobre o mesmo verbete e o mesmo trecho com textos diferentes se contradizem: prevalece a de evidência mais
    forte (correção, depois retificação, depois nota), depois a mais recente pela data, depois a de maior ordem; as
    outras ficam registradas como superadas, sem apagar."""
    grupos: dict[tuple, list[int]] = {}
    for i, e in enumerate(edicoes):
        if e.get("operacao") in ("retificacao", OPERACAO_CORRECAO) and e.get("trecho"):
            grupos.setdefault((e.get("verbete"), bib.normalizar(str(e["trecho"]))), []).append(i)
    saida = [{**e, "prevalece": True} for e in edicoes]
    for indices in grupos.values():
        textos = {bib.normalizar(str(edicoes[i].get("texto") or "")) for i in indices}
        if len(indices) < 2 or len(textos) < 2:
            continue
        vencedor = max(indices, key=lambda i: (_RANQUE_DA_EVIDENCIA.get(edicoes[i].get("evidencia") or edicoes[i].get("operacao"), 0),
                                               str(edicoes[i].get("data") or ""), edicoes[i].get("ordem") or 0))
        for i in indices:
            if i != vencedor:
                saida[i].update({"prevalece": False, "codigo": "superada_por_conflito", "superada_por": edicoes[vencedor].get("ordem")})
    return saida


def metricas_da_rodada(registros_propostas: list[dict]) -> dict:
    """As contagens da rodada, sem intervenção humana: casos, abstenções, propostas, aceitas por tipo e peso, o que a
    validação da Fase 3 e o que cada filtro recusou, o que foi segurado para revisão e a taxa de rejeição."""
    por_filtro = {f: 0 for f in FILTROS}
    recusadas_fase3: dict[str, int] = {}
    recusadas_p5: dict[str, int] = {}
    aceitas_por_tipo: dict[str, int] = {}
    propostas = aceitas = para_revisao = peso_aceito = 0
    for r in registros_propostas:
        for d in r.get("decisoes") or []:
            propostas += 1
            if d.get("aceita"):
                aceitas += 1
                op = (d.get("edicao") or {}).get("operacao") or d.get("operacao") or "?"
                aceitas_por_tipo[op] = aceitas_por_tipo.get(op, 0) + 1
                peso_aceito += d.get("peso") or 0
                continue
            if d.get("motivo") == CODIGO_DE_REVISAO:
                para_revisao += 1
                por_filtro["regra_dos_40"] += 1
            elif d.get("filtro"):
                recusadas_p5[d["motivo"]] = recusadas_p5.get(d["motivo"], 0) + 1
                por_filtro[d["filtro"]] = por_filtro.get(d["filtro"], 0) + 1
            else:
                recusadas_fase3[d.get("motivo") or "?"] = recusadas_fase3.get(d.get("motivo") or "?", 0) + 1
    recusadas = sum(recusadas_fase3.values()) + sum(recusadas_p5.values())
    return {"casos": len(registros_propostas), "abstencoes": sum(1 for r in registros_propostas if r.get("abstencao")), "propostas": propostas,
            "aceitas": aceitas, "para_revisao": para_revisao, "recusadas_fase3": dict(sorted(recusadas_fase3.items())),
            "recusadas_p5": dict(sorted(recusadas_p5.items())), "por_filtro": por_filtro, "aceitas_por_tipo": dict(sorted(aceitas_por_tipo.items())),
            "peso_aceito": peso_aceito, "taxa_de_rejeicao_pct": round(100 * recusadas / propostas, 1) if propostas else None}


def amostra_para_revisao(edicoes: list[dict], parcelas: dict[str, float], n: int = AMOSTRA_DE_REVISAO) -> list[dict]:
    """A amostra dirigida da revisão humana: primeiro o que a regra dos 40% segurou, depois o maior peso, depois o
    verbete mais recuperado na calibração."""
    ordenadas = sorted(edicoes, key=lambda e: (not e.get("para_revisao"), -(e.get("peso") or 0), -parcelas.get(e.get("verbete"), 0.0), e.get("verbete") or ""))
    return ordenadas[:n]


def planilha_de_revisao(edicoes: list[dict], parcelas: dict[str, float], corrida: str) -> str:
    """A planilha de revisão humana do lote (uma linha por edição, a coluna Avaliação em branco para o Eric preencher
    com Correta, Parcial ou Errada), no molde da curadoria da L1."""
    linhas = ["<!-- ! Alteração de IA - Revisar: planilha de revisão humana do lote de acréscimos da corrida " + corrida + ", gerada por",
              "     biblioteca_fase4.planilha_de_revisao; preencher a coluna Avaliação (Correta, Parcial ou Errada) e o Comentário.",
              "     ! Motivo: revisão humana como porta final (decisão 65): nenhuma edição vira parte permanente da biblioteca sem passar por aqui. -->",
              "", f"# Revisão humana do lote ({corrida})", "",
              "| # | Verbete | Operação | Caso | Peso | Segurada pela regra dos 40% | Parcela na calibração | Texto | Motivo | Avaliação | Comentário |",
              "|---|---|---|---|---|---|---|---|---|---|---|"]
    for i, e in enumerate(amostra_para_revisao(edicoes, parcelas, n=len(edicoes)), 1):
        parcela = parcelas.get(e.get("verbete"))
        linhas.append("| " + " | ".join([str(i), f"`{e.get('verbete')}`", str(e.get("operacao")), str(e.get("caso") or ""), str(e.get("peso") or ""),
                                         "sim" if e.get("para_revisao") else "não", f"{100 * parcela:.1f}%".replace(".", ",") if parcela is not None else "",
                                         _esc(e.get("texto") or ""), _esc(e.get("motivo") or ""), CELULA_EM_BRANCO, ""]) + " |")
    return "\n".join(linhas) + "\n"


def _esc(texto: str) -> str:
    return str(texto).replace("|", "\\|").replace("\n", " ")


def revisao_preenchida(planilha: str) -> bool:
    """A planilha está preenchida quando tem ao menos uma linha de edição e nenhuma célula de avaliação em branco."""
    linhas = [l for l in planilha.splitlines() if l.startswith("| ") and not l.startswith("| # |")]
    return bool(linhas) and not any(f"| {CELULA_EM_BRANCO} |" in l for l in linhas)


def filtro_regra_dos_40(verbete_id: str, parcelas: dict[str, float], limiar: float = PARCELA_PARA_REVISAO) -> dict | None:
    """Nota em verbete presente em 40% ou mais dos contextos da calibração vai para revisão humana antes de entrar."""
    p = parcelas.get(verbete_id)
    if p is not None and p >= limiar:
        return {"codigo": CODIGO_DE_REVISAO, "detalhe": f"[{verbete_id}] esteve em {100 * p:.1f}% dos contextos da calibração (limiar {100 * limiar:.0f}%)"}
    return None


def filtro_texto_de_origem_proibida(campos: dict, corpo_http: str | None, minimo: int = MIN_CHARS_TRECHO_PROIBIDO) -> dict | None:
    """Nenhum trecho literal de corpo HTTP (um pedaço de `minimo` caracteres ou mais) entra numa proposta (especificação, seção 10)."""
    if not corpo_http:
        return None
    texto = re.sub(r"\s+", " ", str(campos.get("TEXTO") or "")).strip()
    corpo = re.sub(r"\s+", " ", corpo_http).strip()
    for i in range(0, max(0, len(texto) - minimo + 1)):
        pedaco = texto[i:i + minimo]
        if pedaco in corpo:
            return {"codigo": "texto_de_origem_proibida", "detalhe": f"o TEXTO repete um trecho literal do corpo HTTP do caso: \"{pedaco}\""}
    return None


def filtrar_proposta(campos: dict, edicao: dict, caso: dict, alvo: dict | None, ctx: dict) -> dict:
    """Aplica, na ordem fixa, a regra do texto de origem proibida e os filtros por proposta; a primeira recusa decide.
    O que passa leva a granularidade, o peso e, pela regra dos 40%, a marca de revisão humana (segurada, não recusada).
    `ctx`: parcelas, corpo_http, corrigidos, pesos_usados, casos_da_rodada, fontes, rotas."""
    operacao = edicao.get("operacao") or _campo(campos, "OPERACAO").lower()
    verbete_id = edicao.get("verbete") or _campo(campos, "VERBETE")
    gran = granularidade(campos)
    peso = peso_da_edicao(operacao, gran)
    ordem = (("especificacao_10", lambda: filtro_texto_de_origem_proibida(campos, ctx.get("corpo_http"))),
             ("evidencia_obrigatoria", lambda: filtro_evidencia_obrigatoria(campos, caso)),
             ("atomicidade", lambda: filtro_atomicidade(campos)),
             ("fonte_confiavel", lambda: filtro_fonte_confiavel(campos, ctx.get("fontes") if ctx.get("fontes") is not None else fontes_das_cobaias(),
                                                                ctx.get("rotas") or rotas_do_openapi())),
             ("granularidade", lambda: filtro_granularidade(campos, alvo)),
             ("peso_por_tipo", lambda: filtro_peso_por_tipo(operacao, gran, verbete_id, ctx.get("pesos_usados") or {})),
             ("redundancia", lambda: filtro_redundancia(campos, alvo)),
             ("proveniencia", lambda: filtro_proveniencia(edicao, set(ctx.get("casos_da_rodada") or ()))),
             ("auditoria_por_etapa", lambda: filtro_auditoria_por_etapa(verbete_id, edicao.get("caso"), ctx.get("corrigidos") or {})))
    for nome, checar in ordem:
        r = checar()
        if r is not None:
            return {"aceita": False, "codigo": r["codigo"], "filtro": nome, "detalhe": r["detalhe"], "granularidade": gran, "peso": peso, "para_revisao": False}
    r = filtro_regra_dos_40(verbete_id, ctx.get("parcelas") or {})
    if r is not None:
        return {"aceita": True, "codigo": r["codigo"], "filtro": "regra_dos_40", "detalhe": r["detalhe"], "granularidade": gran, "peso": peso, "para_revisao": True}
    return {"aceita": True, "codigo": None, "filtro": None, "detalhe": None, "granularidade": gran, "peso": peso, "para_revisao": False}


# ------------------------------------------------------------------ o ciclo de correção

def evidencia_de_correcao(antes: dict, depois: dict, contrato: str, forma_esperada: str | None = "lista", orcamento_ms: float = 1000) -> dict:
    """A evidência do gatilho: o que mudou no fio (corpo e tempo da chamada contra o contrato e entre as duas corridas) e na
    árvore podada entre a corrida que falhava (`antes`) e a que passou (`depois`). Cada lado: passou, corpo, tempo_ms,
    arvore, conferencia_falha."""
    def contrato_de(lado: dict) -> dict | None:
        corpo = lado.get("corpo")
        return poda.diff_contrato(contrato, corpo, forma_esperada) if corpo is not None else None

    def n_diferencas(d: dict | None) -> int | None:
        if d is None:
            return None
        return len(d["diferencas"]) + (1 if d["corpo"] != "json" else 0)

    da, dd = contrato_de(antes), contrato_de(depois)
    campos_antes = [x["campo"] for x in (da or {}).get("diferencas", []) if x.get("campo")]
    campos_depois = {x["campo"] for x in (dd or {}).get("diferencas", []) if x.get("campo")}
    ref = cv.diff_referencia(depois.get("corpo"), antes.get("corpo"), depois.get("tempo_ms"), antes.get("tempo_ms"), orcamento_ms=orcamento_ms)
    lento = lambda lado: lado.get("tempo_ms") is not None and lado["tempo_ms"] > orcamento_ms  # noqa: E731
    corpos_diferentes = (antes.get("corpo") or "") != (depois.get("corpo") or "")
    diff_http = {"diferencas_contrato_antes": n_diferencas(da), "diferencas_contrato_depois": n_diferencas(dd),
                 "corpo_antes": (da or {}).get("corpo"), "corpo_depois": (dd or {}).get("corpo"),
                 "campos_que_voltaram": [c for c in campos_antes if c not in campos_depois], "corpos_diferentes": corpos_diferentes,
                 "itens_antes": (ref or {}).get("itens_ref") if ref else None, "itens_depois": (ref or {}).get("itens") if ref else None,
                 "faltavam": list((ref or {}).get("sobram") or []), "sobravam": list((ref or {}).get("faltam") or []),
                 "valores_diferentes": len((ref or {}).get("valores") or []), "lento_antes": bool(lento(antes)), "lento_depois": bool(lento(depois)),
                 "tempo_antes_ms": antes.get("tempo_ms"), "tempo_depois_ms": depois.get("tempo_ms")}
    ha_http = corpos_diferentes or diff_http["lento_antes"] != diff_http["lento_depois"] or (n_diferencas(da) or 0) != (n_diferencas(dd) or 0)
    arv = cv.diff_arvore(antes.get("arvore") or "", depois.get("arvore") or "")
    diff_arvore = {"a_menos": arv["a_menos"], "a_mais": arv["a_mais"]}
    passou_depois = bool(depois.get("passou"))
    sem_diferenca_depois = (n_diferencas(dd) or 0) == 0
    return {"passou_depois": passou_depois, "diff_http": diff_http, "ha_diff_http": bool(ha_http), "diff_arvore": diff_arvore,
            "ha_diff_arvore": arv["a_menos"] + arv["a_mais"] > 0, "conferencia_passou": depois.get("conferencia_falha") is None,
            "sintoma_sumiu": passou_depois and sem_diferenca_depois and depois.get("conferencia_falha") is None}


def detectar_correcao(evidencia: dict) -> dict:
    """O gatilho em código: marca corrigido só quando a reexecução passou E o fio mudou E a árvore mudou."""
    if not evidencia.get("passou_depois"):
        return {"corrigido": False, "motivo": "a reexecução ainda falha: nada a marcar"}
    if not evidencia.get("ha_diff_http"):
        return {"corrigido": False, "motivo": "o roteiro passou, mas nada mudou no fio (corpo e tempo da chamada iguais): sem evidência de correção"}
    if not evidencia.get("ha_diff_arvore"):
        return {"corrigido": False, "motivo": "o roteiro passou e o fio mudou, mas a árvore da página é a mesma: sem evidência na tela"}
    return {"corrigido": True, "motivo": "o roteiro passou e o fio e a árvore mudaram entre a corrida que falhava e a que passou"}


def _plural(n: int, um: str, varios: str) -> str:
    return f"{n} {um if n == 1 else varios}"


def solucao_aplicada_por_molde(caso_id: str, cenario: str, modo: str, evidencia: dict, data: str) -> str:
    """O texto da solução aplicada, por molde, só com o que a evidência mostrou (nunca o nome da causa)."""
    h, a = evidencia.get("diff_http") or {}, evidencia.get("diff_arvore") or {}
    fio = []
    if h.get("campos_que_voltaram"):
        fio.append(f"o campo {', '.join(h['campos_que_voltaram'])} voltou ao corpo" if len(h["campos_que_voltaram"]) == 1
                   else f"os campos {', '.join(h['campos_que_voltaram'])} voltaram ao corpo")
    if h.get("diferencas_contrato_antes") is not None and h.get("diferencas_contrato_depois") is not None and h["diferencas_contrato_antes"] != h["diferencas_contrato_depois"]:
        fio.append(f"{_plural(h['diferencas_contrato_antes'], 'diferença', 'diferenças')} contra o contrato antes e {h['diferencas_contrato_depois']} depois")
    if h.get("faltavam"):
        fio.append(f"{_plural(len(h['faltavam']), 'item que faltava voltou', 'itens que faltavam voltaram')}")
    if h.get("sobravam"):
        fio.append(f"{_plural(len(h['sobravam']), 'item a mais sumiu', 'itens a mais sumiram')}")
    if h.get("valores_diferentes"):
        fio.append(f"{_plural(h['valores_diferentes'], 'valor voltou', 'valores voltaram')} ao da referência")
    if h.get("lento_antes") and not h.get("lento_depois"):
        fio.append("a chamada deixou de passar do orçamento de tempo")
    if not fio:
        fio.append("o corpo da resposta mudou" if h.get("corpos_diferentes") else "nenhuma diferença medida no fio")
    tela = f"{_plural(a.get('a_mais', 0), 'linha da árvore voltou', 'linhas da árvore voltaram')} e {_plural(a.get('a_menos', 0), 'sumiu', 'sumiram')}"
    frase = f"Em {data}, o cenário {cenario} do caso {caso_id} voltou a passar com o modo {modo} desligado: no fio, {'; '.join(fio)}; na tela, {tela}."
    return frase[:TETO_CHARS_CORRECOES]


def _inserir_na_secao(linhas: list[str], secao: str, nova: str) -> list[str]:
    """Acrescenta `nova` ao fim da seção `## <secao>` (criando a seção no fim do arquivo quando não existe)."""
    cabecalho = f"## {secao}"
    inicio = next((i for i, l in enumerate(linhas) if l.strip() == cabecalho), None)
    if inicio is None:
        while linhas and linhas[-1].strip() == "":
            linhas.pop()
        return linhas + ["", cabecalho, nova]
    fim = next((i for i in range(inicio + 1, len(linhas)) if linhas[i].startswith("## ")), len(linhas))
    while fim > inicio + 1 and linhas[fim - 1].strip() == "":
        fim -= 1
    return linhas[:fim] + [nova] + linhas[fim:]


def corrigir(raiz: Path, verbete_id: str, caso_id: str, sugerida: str, aplicada: str, data: str) -> Path:
    """A operação "correção": acrescenta a linha do caso às seções "Solução sugerida" e "Solução aplicada" (criadas no fim do
    arquivo quando não existem), avança o status para corrigido mexendo só na linha do status (com uma linha de comentário
    dizendo de onde avançou) e nunca remove texto. Verbete obsoleto não se corrige."""
    arquivo = next((p for p in raiz.rglob(f"{verbete_id}.md") if not evo._e_gerado(p.name)), None)
    if arquivo is None:
        raise ValueError(f"verbete {verbete_id!r} não existe em {raiz}")
    texto = arquivo.read_text(encoding="utf-8")
    meta, _ = bib._parse_frontmatter(texto)
    status = meta.get("status")
    if status == "obsoleto":
        raise ValueError(f"[{verbete_id}] está obsoleto: a correção não se aplica")
    linhas = texto.split("\n")
    fim_fm = next((i for i, l in enumerate(linhas) if i > 0 and l.strip() == "---"), None)
    if fim_fm is None:
        raise ValueError(f"frontmatter sem '---' de fechamento em {arquivo}")
    if status != "corrigido":
        indice = next(i for i in range(1, fim_fm) if linhas[i].lstrip().startswith("status:"))
        linhas[indice] = "status: corrigido"
        linhas.insert(fim_fm, f"# ! Alteração pelo harness da Fase 4 (correção, caso {caso_id}, {data}) - Revisar: status avançou de {status} para corrigido.")
    sugerida_ = re.sub(r"\s+", " ", sugerida or "").strip() or SEM_NOTA
    aplicada_ = re.sub(r"\s+", " ", aplicada or "").strip()
    linhas = _inserir_na_secao(linhas, SECAO_SUGERIDA, f"- [{caso_id} · {data}] {sugerida_}")
    linhas = _inserir_na_secao(linhas, SECAO_APLICADA, f"- [{caso_id} · {data}] {aplicada_}")
    novo = "\n".join(linhas)
    if not novo.endswith("\n"):
        novo += "\n"
    arquivo.write_text(novo, encoding="utf-8")
    return arquivo


_STATUS_MUDOU_RE = re.compile(r"^(?P<rel>.+?): 'status' mudou de '(?P<de>[^']*)' para '(?P<para>[^']*)'$")


def conferir_correcao(raiz_antes: Path, raiz_depois: Path, corrigidos: dict[str, list[str]]) -> list[str]:
    """A validação da correção: o invariante de só acréscimo da Fase 3 continua valendo (fora o avanço permitido do status
    nos verbetes corrigidos), o estado só avança, o trecho apontado (a nota do caso) continua no verbete, as duas seções
    têm a linha de cada caso e as correções renderizadas cabem no teto."""
    violacoes = []
    antes = {v["id"]: v for v in evo._carregar_verbetes(raiz_antes)}
    depois = {v["id"]: v for v in evo._carregar_verbetes(raiz_depois)}
    for msg in evo.conferir_somente_acrescimo(raiz_antes, raiz_depois):
        m = _STATUS_MUDOU_RE.match(msg)
        if m:
            vid = Path(m.group("rel")).stem
            if m.group("para") == "corrigido" and m.group("de") in ("ativo", "nao_corrigido") and vid in corrigidos:
                continue
        violacoes.append(msg)
    for vid, va in antes.items():
        vd = depois.get(vid)
        if vd is None:
            continue
        if estado_do_verbete(va) == "corrigido" and estado_do_verbete(vd) != "corrigido":
            violacoes.append(f"[{vid}]: o estado recuou de corrigido para {vd['meta'].get('status')}")
    for vid, casos in corrigidos.items():
        vd = depois.get(vid)
        if vd is None:
            violacoes.append(f"[{vid}]: verbete corrigido não está na cópia")
            continue
        if estado_do_verbete(vd) != "corrigido":
            violacoes.append(f"[{vid}]: corrigido sem o status corrigido")
        registrados = {c["caso"]: c for c in bib.correcoes(vd)}
        for caso in casos:
            c = registrados.get(caso)
            if c is None or not c.get("aplicada"):
                violacoes.append(f"[{vid}]: sem a linha do caso {caso} nas seções de correção")
                continue
            if c["sugerida"] != SEM_NOTA and c["sugerida"] not in sugestao_do_modelo(vd, caso):
                violacoes.append(f"[{vid}]: a solução sugerida do caso {caso} não é a nota do modelo que está no verbete (sumiu ou foi reescrita)")
        tam = len(bib.render_correcoes(vd))
        if tam > TETO_CHARS_CORRECOES:
            violacoes.append(f"[{vid}]: correções renderizadas com {tam} caracteres (teto {TETO_CHARS_CORRECOES})")
    return violacoes


def fechar_correcoes(pasta_bib: Path, n: int, modelo: str, casos: list[dict], corrigidos: dict[str, list[str]], versao_ollama: str | None = None,
                     anterior: int | None = None) -> dict:
    """Fecha a época das correções (epoca-<n>): biblioteca válida, a conferência da correção contra a época anterior, o
    índice, o diff e o fechamento.json (o da Fase 3 mais a contagem de correções)."""
    raiz = pasta_bib / f"epoca-{n}"
    anterior_ = pasta_bib / f"epoca-{anterior if anterior is not None else n - 1}"
    verbetes = evo._carregar_verbetes(raiz)
    problemas = bib.validar(verbetes, casos, teto_global=None)
    if problemas:
        raise SystemExit(f"época {n} de correções não fecha: biblioteca inválida: " + "; ".join(problemas))
    violacoes = conferir_correcao(anterior_, raiz, corrigidos)
    if violacoes:
        raise SystemExit(f"época {n} de correções não fecha: " + "; ".join(violacoes))
    validar_banco.escrever_indice(verbetes, raiz)
    evo.escrever_diff(anterior_, raiz, pasta_bib / f"diff__E{n}", anterior_.name, raiz.name)
    n_correcoes = sum(len(c) for c in corrigidos.values())
    dado = evo.fechar_snapshot(raiz, n, modelo, n_correcoes, versao_ollama=versao_ollama)
    dado = {**dado, "correcoes": n_correcoes, "verbetes_corrigidos": {k: list(v) for k, v in sorted(corrigidos.items())}, "operacao": OPERACAO_CORRECAO}
    evo._gravar_json_atomico(raiz / "fechamento.json", dado)
    return dado


def regra_r4(registros: list[dict]) -> dict:
    """Precisão e revocação da marca corrigido contra o conjunto conhecido de modos desligados, nos casos que reproduziam
    o sintoma antes; os sem sintoma antes ficam listados à parte. Kappa de Cohen entre a marca e o desligamento."""
    universo = [r for r in registros if r.get("reproduziu_antes")]
    desligados = [r for r in universo if r.get("desligado")]
    marcados = [r for r in universo if r.get("marcado")]
    acertos = [r for r in marcados if r.get("desligado")]
    fp = [r for r in marcados if not r.get("desligado")]
    perdidos = [r for r in desligados if not r.get("marcado")]
    n = len(universo)
    kappa = None
    if n:
        po = (len(acertos) + sum(1 for r in universo if not r.get("marcado") and not r.get("desligado"))) / n
        pe = (len(marcados) / n) * (len(desligados) / n) + (1 - len(marcados) / n) * (1 - len(desligados) / n)
        kappa = round((po - pe) / (1 - pe), 3) if pe < 1 else None
    return {"universo": n, "desligados": len(desligados), "mantidos": n - len(desligados), "marcados": len(marcados), "acertos": len(acertos),
            "falsos_positivos": len(fp), "perdidos": len(perdidos),
            "precisao_pct": round(100 * len(acertos) / len(marcados), 1) if marcados else None,
            "revocacao_pct": round(100 * len(acertos) / len(desligados), 1) if desligados else None,
            "sem_sintoma_antes": [r.get("caso") for r in registros if not r.get("reproduziu_antes")], "kappa": kappa}


# ------------------------------------------------------------------ o lote e a regra R5

def _acertou(registro: dict) -> bool:
    lido = avaliar.extrair(registro.get("resposta", ""))["causa_raiz"]
    return lido is not None and avaliar._normalizar(lido) == avaliar._normalizar((registro.get("gabarito") or {}).get("causa_raiz", ""))


def avaliar_lote(base: list[dict], novos: list[dict]) -> dict:
    """A regra R5 sobre os registros pareados pelo caso: b = casos que só a biblioteca com o lote acerta, c = só a de
    partida; o lote é aceito quando b é maior ou igual a c, senão fica em espera com o motivo."""
    por_caso_base = {r["caso"]: _acertou(r) for r in base}
    pares = [(r["caso"], por_caso_base[r["caso"]], _acertou(r)) for r in novos if r["caso"] in por_caso_base]
    ganhos = sorted(c for c, a, b in pares if b and not a)
    perdas = sorted(c for c, a, b in pares if a and not b)
    b, c = len(ganhos), len(perdas)
    veredito = "aceito" if b >= c else "em_espera"
    motivo = (f"b = {b} (passaram a acertar) e c = {c} (passaram a errar) nos {len(pares)} casos pareados: "
              + ("o lote entra (b maior ou igual a c)" if veredito == "aceito" else "o lote fica em espera (c maior que b)"))
    return {"n": len(pares), "b": b, "c": c, "ganhos": ganhos, "perdas": perdas, "acerto_base": sum(1 for _, a, _ in pares if a),
            "acerto_novo": sum(1 for _, _, x in pares if x), "p_mcnemar": avaliar.mcnemar_exato(b, c), "veredito": veredito, "motivo": motivo}


# ------------------------------------------------------------------ a proposta com os filtros (P5) e a trilha

def _no_de_edicao(decisoes: list[dict], classe: str, caso_id: str, ids_visiveis: list[str], seq_inferencia: int, evidencia: list[dict]) -> dict:
    """O nó de decisão `edicao_biblioteca`: as propostas como alternativas (escore = quantas das duas validações passaram),
    a abstenção como alternativa própria, a escolha (a primeira edição aplicada ou nenhuma), a divergência entre o que
    o modelo propôs e o que o código recusou, e a falha da taxonomia quando nada entrou."""
    alternativas = []
    for d in decisoes:
        escore = 2 if d.get("aceita") or d.get("motivo") == CODIGO_DE_REVISAO else (1 if d.get("filtro") else 0)
        resultado = "aplicada" if d.get("aceita") else ("para_revisao" if d.get("motivo") == CODIGO_DE_REVISAO else f"recusada:{d.get('motivo')}")
        alternativas.append({"opcao": f"proposta_{d.get('numero')}", "escore": escore, "operacao": d.get("operacao"), "verbete": d.get("verbete"), "resultado": resultado})
    alternativas.append({"opcao": "nenhuma", "escore": 1 if classe == "abstencao" else 0, "operacao": None, "verbete": None,
                         "resultado": "abstencao" if classe == "abstencao" else ("sem_bloco" if classe == "sem_bloco" else "nao_escolhida")})
    aplicadas = [d for d in decisoes if d.get("aceita")]
    seguradas = [d for d in decisoes if d.get("motivo") == CODIGO_DE_REVISAO]
    recusadas = [d for d in decisoes if not d.get("aceita") and d.get("motivo") != CODIGO_DE_REVISAO]
    escolha = f"proposta_{aplicadas[0]['numero']}" if aplicadas else "nenhuma"
    if aplicadas:
        resultado = "lote"
    elif seguradas:
        resultado = "para_revisao"
    elif classe == "abstencao":
        resultado = "abstencao"
    elif classe == "sem_bloco":
        resultado = "sem_bloco"
    else:
        resultado = "recusada"
    codigos = [d.get("motivo") for d in recusadas]
    divergencia = {"ha": bool(recusadas), "entre": ["modelo", "verificacao"],
                   "detalhe": (f"o modelo propôs {len(decisoes)} edição(ões) e o código recusou {len(recusadas)}: {', '.join(str(c) for c in codigos)}" if recusadas
                               else "nenhuma proposta do modelo foi recusada pelo código")}
    falha = None
    if "texto_de_origem_proibida" in codigos:
        falha = "texto_de_origem_proibida"
    elif resultado in ("recusada", "sem_bloco"):
        falha = "acrescimo_recusado_pela_validacao"
    no = tr.no_de_decisao("edicao_biblioteca", escolha=escolha, alternativas=alternativas, evidencia=evidencia, resultado=resultado, divergencia=divergencia,
                          confianca=None, prov={"used": list(ids_visiveis), "wasDerivedFrom": [caso_id], "wasGeneratedBy": seq_inferencia}, falha=falha,
                          extras={"caso": caso_id, "aplicadas": [d.get("verbete") for d in aplicadas], "para_revisao": [d.get("verbete") for d in seguradas],
                                  "recusadas": [{"numero": d.get("numero"), "verbete": d.get("verbete"), "codigo": d.get("motivo"), "filtro": d.get("filtro")} for d in recusadas]})
    no["justificativa"] = justificativa_da_edicao(no, decisoes)
    no["contraste"] = contraste_da_edicao(no, decisoes)
    return no


def justificativa_da_edicao(no: dict, decisoes: list[dict]) -> str:
    """A frase por molde do nó de edição: o que o modelo propôs, o que entrou, o que ficou para revisão e o que o código recusou."""
    caso = no.get("caso")
    if not decisoes:
        if no.get("resultado") == "abstencao":
            return f"O modelo respondeu NENHUMA para o caso {caso}: abstenção válida, nada entrou na biblioteca e nada foi recusado."
        return f"O modelo não escreveu bloco PROPOSTA nem NENHUMA para o caso {caso}: nada entrou na biblioteca (sem_bloco)."
    partes = [f"O modelo propôs {len(decisoes)} edição(ões) para o caso {caso}."]
    for d in decisoes:
        alvo = f"[{d.get('verbete')}]"
        if d.get("aceita"):
            partes.append(f"A proposta {d.get('numero')} ({d.get('operacao')} em {alvo}, peso {d.get('peso')}) passou pela validação da Fase 3 e pelos filtros e entrou no lote.")
        elif d.get("motivo") == CODIGO_DE_REVISAO:
            partes.append(f"A proposta {d.get('numero')} ({d.get('operacao')} em {alvo}) passou pelas validações, mas ficou segurada para revisão humana: {d.get('detalhe')}.")
        else:
            quem = f"o filtro {d.get('filtro')}" if d.get("filtro") else "a validação da Fase 3"
            partes.append(f"A proposta {d.get('numero')} ({d.get('operacao') or 'sem operação'} em {alvo}) foi recusada por {quem} com o código {d.get('motivo')}: {d.get('detalhe')}.")
    return " ".join(partes).replace("—", ",").replace("→", "para")


def contraste_da_edicao(no: dict, decisoes: list[dict]) -> str:
    """"Esta e não a segunda": a edição escolhida contra a segunda proposta (ou contra a abstenção)."""
    escolha = no.get("escolha")
    if escolha == "nenhuma":
        return "nenhuma edição entrou: " + ("abstenção válida do modelo" if no.get("resultado") == "abstencao" else
                                             ("as propostas ficaram para revisão humana" if no.get("resultado") == "para_revisao" else
                                              "toda proposta foi recusada pelo código"))
    outras = [d for d in decisoes if f"proposta_{d.get('numero')}" != escolha]
    if not outras:
        return f"{escolha} e não a abstenção: o modelo propôs uma edição que passou por todas as validações"
    d = outras[0]
    estado = "também entrou no lote" if d.get("aceita") else ("ficou para revisão humana" if d.get("motivo") == CODIGO_DE_REVISAO else f"foi recusada ({d.get('motivo')})")
    return f"{escolha} e não proposta_{d.get('numero')}: a primeira passou por todas as validações; a segunda {estado}"


def propor_p5(modelo: str, caso: dict, registro_diag: dict, ctx: dict, prompt_diag: str, verbetes_leitura: list[dict], teto: int, comum: dict,
              ctx_validacao: dict, pasta_bib: Path, ordem: int, filtros_ctx: dict, trilha: tr.Trilha | None = None, tid: str | None = None,
              evidencia=(), ts: str | None = None) -> dict:
    """A inferência de proposta de um caso de aprendizado, como executar_fase3.propor (o segundo prompt é a continuação
    literal do de diagnóstico; o validador congelado da Fase 3 decide primeiro) e, depois dele, os filtros em código do
    P5: a edição só é gravada na cópia quando passa pelos dois e não é segurada pela regra dos 40%; as seguradas ficam
    em `para_revisao`; o registro tem a forma da Fase 3 (abrir_epoca reconstrói a época dele) mais os campos do P5; com
    `trilha`, emite a inferência, um evento `edicao_biblioteca` por bloco e o nó de decisão."""
    resposta_diag = registro_diag.get("resposta", "")
    causa_respondida, acertou = executar_fase3.diagnostico_acertou(caso, resposta_diag)
    ouro = rec.verbete_ouro(verbetes_leitura, caso)
    ids_visiveis = sorted(set(ctx["verbetes_ids"]) | {ouro["id"]})
    prompt = estrategias.proposta_de_edicao(prompt_diag, resposta_diag, caso, acertou, causa_respondida, bib.render(ouro), ids_visiveis)
    r = executar_fase3.inferir_com_repeticao(modelo, prompt, teto, caso["id"], "proposta")
    executar_bateria.guarda_tokens_reais(r.get("tokens_entrada", 0), teto, f"proposta da época {comum.get('epoca')}")
    parseado = evo.parsear_propostas(r.get("resposta", ""), r.get("tokens_saida"), teto)
    classe = classificar_resposta(parseado)
    raiz = ctx_validacao["raiz"]
    data = filtros_ctx.get("data") or hoje()
    pesos = filtros_ctx.setdefault("pesos_usados", {})
    decisoes: list[dict] = []
    filtros: list[dict] = []
    para_revisao: list[dict] = []
    s_inf = None
    if trilha is not None:
        s_inf = trilha.evento("inferencia", tid, {"etapa": "proposta", "resposta": trilha.blob(r.get("resposta", ""), "resposta"), "prompt": trilha.blob(prompt, "prompt"),
                                                  "segundos": r.get("segundos"), "tokens_entrada": r.get("tokens_entrada"), "tokens_saida": r.get("tokens_saida"),
                                                  "prefill_ms": r.get("prefill_ms"), "geracao_ms": r.get("geracao_ms"), "ids_visiveis": ids_visiveis,
                                                  "recuperacao_por_id": list(ctx.get("por_id") or [])}, "ao_vivo", ts=ts)
    ev = list(evidencia) + ([{"seq": s_inf, "papel": "resposta"}] if s_inf else [])
    for bloco in parseado["blocos"]:
        campos = bloco.get("campos", {})
        veredito3 = evo.validar_proposta(bloco, ctx_validacao)
        numero = bloco.get("numero", 0)
        decisao = {"numero": numero, "operacao": campos.get("OPERACAO", "").strip() or None, "verbete": campos.get("VERBETE", "").strip() or None,
                   "aceita": False, "motivo": veredito3["motivo"], "detalhe": veredito3["detalhe"], "edicao": None, "filtro": None, "peso": None,
                   "granularidade": None, "para_revisao": False, "proveniencia": None}
        v5 = None
        if veredito3["aceita"]:
            edicao = veredito3["edicao"]
            alvo = next((v for v in ctx_validacao["verbetes"] if v["id"] == edicao["verbete"]), None)
            v5 = filtrar_proposta(campos, edicao, caso, alvo, filtros_ctx)
            decisao.update({"operacao": edicao["operacao"], "verbete": edicao["verbete"], "filtro": v5["filtro"], "peso": v5["peso"],
                            "granularidade": v5["granularidade"], "detalhe": v5["detalhe"] or veredito3["detalhe"]})
            if not v5["aceita"]:
                decisao["motivo"] = v5["codigo"]
            elif v5["para_revisao"]:
                decisao.update({"motivo": v5["codigo"], "edicao": edicao, "para_revisao": True, "proveniencia": proveniencia(edicao, data)})
                para_revisao.append(edicao)
            else:
                evo.aplicar_edicao(raiz, edicao)
                ordem += 1
                evo.registrar_historico(pasta_bib, edicao, {"ordem": ordem, "acertou_diagnostico": acertou, "hash_apos": evo.hash_biblioteca(raiz),
                                                           "proveniencia": proveniencia(edicao, data), "peso": v5["peso"], "granularidade": v5["granularidade"]})
                ctx_validacao["verbetes"] = bib.carregar(raiz)
                ctx_validacao["aceitas_no_caso"] += 1
                if edicao["operacao"] == "novo_verbete":
                    ctx_validacao["novos_nesta_epoca"] += 1
                pesos[edicao["verbete"]] = pesos.get(edicao["verbete"], 0) + v5["peso"]
                decisao.update({"aceita": True, "motivo": None, "edicao": edicao, "proveniencia": proveniencia(edicao, data)})
        decisoes.append(decisao)
        filtros.append({"numero": numero, "fase3": {"aceita": veredito3["aceita"], "motivo": veredito3["motivo"]}, "p5": v5, "aplicada": decisao["aceita"]})
        if trilha is not None:
            s_ed = trilha.evento("edicao_biblioteca", tid, {"etapa": "proposta", "caso": caso["id"], "numero": numero, "operacao": decisao["operacao"],
                                                             "verbete": decisao["verbete"], "origem": "modelo", "veredito_fase3": {"aceita": veredito3["aceita"], "motivo": veredito3["motivo"],
                                                                                                                              "detalhe": veredito3["detalhe"]},
                                                             "filtro": decisao["filtro"], "codigo": None if decisao["aceita"] else decisao["motivo"], "detalhe": decisao["detalhe"],
                                                             "aplicada": decisao["aceita"], "para_revisao": decisao["para_revisao"], "peso": decisao["peso"],
                                                             "granularidade": decisao["granularidade"], "proveniencia": decisao["proveniencia"],
                                                             "texto": trilha.blob(_campo(campos, "TEXTO"), "proposta") if campos.get("TEXTO") else None,
                                                             "hash_biblioteca_apos": evo.hash_biblioteca(raiz)}, "ao_vivo", pai=s_inf, ts=ts)
            if decisao["verbete"] and decisao["verbete"] in ids_visiveis:
                ev.append({"seq": s_ed, "papel": "verbete_entregue", "id": decisao["verbete"]})
    if not parseado["blocos"] and not parseado["nenhuma"]:
        veredito = evo.validar_proposta(None, ctx_validacao)
        decisoes.append({"numero": 0, "operacao": None, "verbete": None, "aceita": False, "motivo": veredito["motivo"], "detalhe": veredito["detalhe"],
                         "edicao": None, "filtro": None, "peso": None, "granularidade": None, "para_revisao": False, "proveniencia": None})
    registro = {"modelo": modelo, "digest": comum.get("digest"), "versao_ollama": comum.get("versao_ollama"), "maquina": comum.get("maquina"),
                "fase": "4", "tipo": "proposta", "epoca": comum.get("epoca"), "biblioteca_epoca": comum.get("biblioteca_epoca"),
                "biblioteca_versao": comum.get("biblioteca_versao"), "caso": caso["id"], "classe": caso.get("classe"), "nivel": caso.get("nivel"),
                "particao": "aprendizado", "k": comum.get("k"), "verbetes_ids": list(ctx["verbetes_ids"]), "verbete_ouro": ouro["id"],
                "ouro_no_contexto": ouro["id"] in ctx["verbetes_ids"], "ids_visiveis": ids_visiveis, "causa_correta_mostrada": caso["gabarito"]["causa_raiz"],
                "campo_mostrado": caso["gabarito"].get("campo_afetado") or "nenhum", "causa_respondida": causa_respondida, "acertou_diagnostico": acertou,
                "prompt": prompt, "teto_tokens": teto, **r, "contexto_estourou": executar_fase3._estourou(r.get("tokens_entrada", 0), teto),
                "resposta_truncada": parseado["truncada"], "nenhuma": parseado["nenhuma"], "propostas_parseadas": parseado["blocos"], "decisoes": decisoes,
                "n_propostas": len(parseado["blocos"]), "n_aceitas": sum(1 for d in decisoes if d["aceita"]),
                "motivos_rejeicao": [d["motivo"] for d in decisoes if not d["aceita"] and d["motivo"]], "abstencao": classe == "abstencao",
                "filtros": filtros, "para_revisao": para_revisao, "recuperacao_por_id": list(ctx.get("por_id") or []),
                "verbetes_ligados": [v["id"] for v in verbetes_do_caso(verbetes_leitura, caso["id"])],
                **executar_bateria.ambiente_residente(), "hash_biblioteca_apos": evo.hash_biblioteca(raiz)}
    if trilha is not None:
        no = _no_de_edicao(decisoes, classe, caso["id"], ids_visiveis, s_inf, ev)
        s_no = trilha.decisao(tid, no, pai=s_inf, ts=ts)
        registro.update({"no": no, "seq_inferencia": s_inf, "seq_decisao": s_no})
    return registro


def no_de_correcao(caso_id: str, verbetes_ids: list[str], deteccao: dict, evidencia_: dict, seqs: list[dict], estados: dict) -> dict:
    """O nó de decisão `edicao_biblioteca` do ciclo de correção: corrigido ou não, com a evidência dos dois diffs apontada
    por evento; a divergência fica em False porque a solução aplicada sai do molde da evidência, não de uma declaração."""
    corrigido = bool(deteccao.get("corrigido"))
    escore = int(bool(evidencia_.get("passou_depois"))) + int(bool(evidencia_.get("ha_diff_http"))) + int(bool(evidencia_.get("ha_diff_arvore")))
    alternativas = [{"opcao": "corrigido", "escore": escore, "detalhe": "a reexecução passou e o fio e a árvore mudaram"},
                    {"opcao": "nao_corrigido", "escore": 3 - escore, "detalhe": "falta ao menos uma das três evidências"}]
    no = tr.no_de_decisao("edicao_biblioteca", escolha="corrigido" if corrigido else "nao_corrigido", alternativas=alternativas, evidencia=seqs,
                          resultado="correcao_registrada" if corrigido else "sem_correcao",
                          divergencia={"ha": False, "entre": ["programa", "verificacao"], "detalhe": "a solução aplicada sai do molde da evidência medida; a sugerida é o texto do modelo, registrado sem julgamento"},
                          confianca=None, prov={"used": list(verbetes_ids), "wasDerivedFrom": [caso_id], "wasGeneratedBy": None}, falha=None,
                          extras={"caso": caso_id, "operacao": OPERACAO_CORRECAO, "estados": estados, "motivo": deteccao.get("motivo")})
    no["justificativa"] = (f"O caso {caso_id} foi reapresentado com o modo de falha desligado: {deteccao.get('motivo')}. "
                           + (f"Os verbetes {', '.join(verbetes_ids)} passaram a corrigido, com a solução sugerida (o texto do modelo) e a solução aplicada (o molde da evidência)."
                              if corrigido else "Nenhum verbete mudou de estado."))
    no["contraste"] = (f"corrigido e não nao_corrigido: {escore} de 3 evidências presentes" if corrigido else
                       f"nao_corrigido e não corrigido: só {escore} de 3 evidências presentes (reexecução, fio, árvore)")
    return no


def sonda_anterior(pasta: Path | None = None, versao: int = 1) -> dict:
    """A leitura da sonda de 28/09/2026 (`resultados_alvo/fase3b_correcao`): por caso, o rótulo, o acerto, as propostas, as
    aceitas e os motivos de recusa, para a comparação caso a caso com a sonda repetida."""
    pasta = pasta or caminhos.RESULTADOS / "fase3b_correcao" / executar_fase3._slug("qwen2.5:7b")
    diag = {r["caso"]: r for r in executar_bateria.ler_jsonl(pasta / f"diagnosticos__L{versao}.jsonl")}
    prop = {r["caso"]: r for r in executar_bateria.ler_jsonl(pasta / f"propostas__E{versao + 1}.jsonl")}
    saida = {}
    for cid, d in diag.items():
        p_ = prop.get(cid) or {}
        rotulo = avaliar.extrair(d.get("resposta", ""))["causa_raiz"]
        gabarito = (d.get("gabarito") or {}).get("causa_raiz")
        saida[cid] = {"rotulo": rotulo, "acertou": rotulo is not None and gabarito is not None and avaliar._normalizar(rotulo) == avaliar._normalizar(gabarito),
                      "n_propostas": p_.get("n_propostas", 0), "n_aceitas": p_.get("n_aceitas", 0), "motivos": list(p_.get("motivos_rejeicao") or []),
                      "abstencao": bool(p_.get("nenhuma")), "verbetes_ids": list(d.get("verbetes_ids") or [])}
    return saida


# ------------------------------------------------------------------ promoção à produção e a pasta de espera (ficha 32)

def promover(saida: str, destino: Path = PASTA_CURADA, planilha: Path | None = None, modelo: str = "qwen2.5:7b", epoca: int = 101) -> dict:
    """Aplica à biblioteca de produção o lote aceito pela regra R5 e revisado pelo Eric: só com `lote.json` dizendo
    `aceito`, a planilha de revisão preenchida e o invariante de só acréscimo contra a cópia atual; grava o fechamento.json
    novo com o hash e a origem do lote. Nunca roda sozinha: é o comando que o Eric dispara depois da revisão."""
    raiz = caminhos.fase3(saida)["raiz"]
    lote = json.loads((raiz / "lote.json").read_text(encoding="utf-8"))
    if (lote.get("r5") or {}).get("veredito") != "aceito":
        raise SystemExit(f"o lote de {saida} não foi aceito pela regra R5 ({(lote.get('r5') or {}).get('veredito')}): nada a promover")
    planilha = planilha or raiz / "revisao_do_lote.md"
    if not planilha.exists() or not revisao_preenchida(planilha.read_text(encoding="utf-8")):
        raise SystemExit(f"a planilha de revisão {planilha} não existe ou tem avaliação em branco: a revisão humana é a porta final")
    origem = raiz / "bibliotecas" / executar_fase3._slug(modelo) / f"epoca-{epoca}"
    if not evo.snapshot_fechado(origem):
        raise SystemExit(f"a época do lote ({origem}) não está fechada")
    violacoes = evo.conferir_somente_acrescimo(destino, origem)
    if violacoes:
        raise SystemExit("o lote não é só acréscimo sobre a produção atual: " + "; ".join(violacoes))
    hash_antes = evo.hash_biblioteca(destino)
    for arq in sorted(origem.rglob("*.md")):
        if evo._e_gerado(arq.name):
            continue
        alvo = destino / arq.relative_to(origem)
        alvo.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(arq, alvo)
    verbetes = evo._carregar_verbetes(destino)
    validar_banco.escrever_indice(verbetes, destino)
    dado = evo.fechar_snapshot(destino, epoca, modelo, len(lote.get("edicoes") or []), versao_ollama=lote.get("versao_ollama"))
    dado = {**dado, "origem_do_lote": saida, "hash_anterior": hash_antes, "planilha": planilha.name, "promovido_em": dt.datetime.now().isoformat(timespec="seconds")}
    evo._gravar_json_atomico(destino / "fechamento.json", dado)
    return dado


def mover_para_espera(origem: Path = PASTA_CURADA, destino: Path = PASTA_DE_ESPERA, ids: list[str] | None = None, registros=None) -> list[str]:
    """Ficha 32: os verbetes aprendidos que a calibração nunca recuperou saem do índice para `aprendidos_em_espera/` (pasta
    irmã da biblioteca, fora do que bib.carregar lê), sem apagar; o fechamento.json da produção é regravado."""
    verbetes = evo._carregar_verbetes(origem)
    aprendidos = [v["id"] for v in verbetes if v["pasta"] == evo.PASTA_APRENDIDOS]
    if ids is None:
        ids = aprendidos_sem_recuperacao(recuperacao_dos_aprendidos(registros or [], aprendidos))
    movidos = []
    destino.mkdir(parents=True, exist_ok=True)
    for v in verbetes:
        if v["id"] in ids:
            shutil.move(str(v["caminho"]), str(destino / v["caminho"].name))
            movidos.append(v["id"])
    if movidos:
        restantes = evo._carregar_verbetes(origem)
        validar_banco.escrever_indice(restantes, origem)
        antigo = json.loads((origem / "fechamento.json").read_text(encoding="utf-8")) if (origem / "fechamento.json").exists() else {}
        dado = evo.fechar_snapshot(origem, antigo.get("epoca", 100), antigo.get("modelo", "qwen2.5:7b"), antigo.get("aceitas_na_epoca", 0),
                                   versao_ollama=antigo.get("versao_ollama"))
        evo._gravar_json_atomico(origem / "fechamento.json", {**dado, "aprendidos_em_espera": movidos, "hash_anterior": antigo.get("hash")})
    return movidos


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--planilha", metavar="SAIDA", help="escreve <saida>/revisao_do_lote.md a partir de lote.json")
    ap.add_argument("--promover", metavar="SAIDA", help="aplica o lote aceito e revisado de <saida> à biblioteca de produção")
    ap.add_argument("--espera", action="store_true", help="move para aprendidos_em_espera/ os aprendidos nunca recuperados na calibração (k = 3)")
    ap.add_argument("--modelo", default="qwen2.5:7b")
    args = ap.parse_args()
    print(caminhos.descricao())
    if args.planilha:
        raiz = caminhos.fase3(args.planilha)["raiz"]
        lote = json.loads((raiz / "lote.json").read_text(encoding="utf-8"))
        texto = planilha_de_revisao((lote.get("edicoes") or []) + (lote.get("para_revisao") or []), lote.get("parcelas") or {}, args.planilha)
        (raiz / "revisao_do_lote.md").write_text(texto, encoding="utf-8", newline="\n")
        print(f"planilha gravada em {raiz / 'revisao_do_lote.md'}")
        return 0
    if args.promover:
        dado = promover(args.promover, modelo=args.modelo)
        print(f"lote promovido: hash {dado['hash_anterior']} para {dado['hash']} ({dado['n_verbetes']} verbetes)")
        return 0
    if args.espera:
        arq = caminhos.RESULTADOS / "fase4_calibracao" / "k3" / executar_fase3._slug(args.modelo) / "diagnosticos__L100.jsonl"
        movidos = mover_para_espera(registros=executar_bateria.ler_jsonl(arq))
        print(f"movidos para {PASTA_DE_ESPERA}: {movidos or 'nenhum'}")
        return 0
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
