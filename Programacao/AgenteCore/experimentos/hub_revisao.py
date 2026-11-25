#!/usr/bin/env python3
# ! Alteração de IA - Revisar: arquivo novo (25/11/2026, Pós-Fase 4, pacote Q6): a revisão do hub central. Cada caso tem um arquivo JSONL em
# `resultados_alvo/hub/revisoes/<caso>.jsonl`, fora da trilha, e cada linha é um evento que só é acrescentado: comentário (preso a um trecho de um
# bloco do relatório, ou geral), mudança de estado de uma conversa (ativa, resolvida, não será tratada), veredito de cinco valores (aprovar,
# aprovar com sugestões, aguardar o autor, rejeitar, comentar), os campos severidade, prioridade e estado da seção 5.5 do syllabus CTFL 4.0, a
# sugestão "a causa é outra" e a marca de lido. `estado()` refaz, a partir dos eventos, o que a página mostra. `enviar_revisao()` grava os
# rascunhos e o veredito numa escrita só, ou não grava nada.
# ! Motivo: plano aprovado da Pós-Fase 4, seção 3.6 (itens 2 a 6), e ficha 97 (decisão 157). O arquivo só cresce para o histórico da revisão
# ser dado do TCC e nunca se perder numa regravação; todo evento passa pela mesma validação antes de chegar ao disco, e é nela que fica a regra
# do princípio 4 do plano: o agente só comenta, e veredito, 5.5, causa corrigida e estado de conversa são do analista. O nome do arquivo sai do
# identificador do caso por uma expressão que só aceita letras, números, hífen e sublinhado, para nenhum caminho vindo da página chegar ao disco.
"""A revisão do hub central (Pós-Fase 4, pacote Q6): eventos em JSONL por caso, só com acréscimo, e o estado refeito a partir deles.

Fontes do desenho (levantamento §6.15.1 do Memorial): Microsoft Learn, "Review and comment on pull requests" (conversas com estado, voto de
cinco valores, iterações, a revisão do Copilot sai sempre como comentário); GitHub Docs, "Reviewing proposed changes in a pull request"
(comentário pendente enviado junto com a revisão, marca de visto que cai quando o arquivo muda); Conventional Comments (rótulo e decoração de
bloqueio); ISTQB CTFL 4.0, seção 5.5, tradução do BSTQB, p. 51 (os exemplos de estado do defeito).
"""
from __future__ import annotations

import datetime as dt
import json
import re
import threading
from pathlib import Path

import taxonomia

VEREDITOS = {"aprovar": "Aprovar", "aprovar_com_sugestoes": "Aprovar com sugestões", "aguardar_autor": "Aguardar o autor", "rejeitar": "Rejeitar",
             "comentar": "Comentar"}
ESTADOS_DA_CONVERSA = {"ativa": "ativa", "resolvida": "resolvida", "nao_sera_tratada": "não será tratada"}
# os exemplos de estado da seção 5.5 do syllabus CTFL 4.0 (tradução do BSTQB, p. 51); o inicial é "aberto", dado pelo código
ESTADOS_55 = ("aberto", "adiado", "duplicado", "aguardando correção", "aguardando teste de confirmação", "reaberto", "fechado", "rejeitado")
# o syllabus não dá escala para severidade e prioridade: estas duas são do hub, declaradas
SEVERIDADES = ("crítica", "alta", "média", "baixa")
PRIORIDADES = ("alta", "média", "baixa")
ROTULOS = {"sugestao": "sugestão", "problema": "problema", "duvida": "dúvida", "elogio": "elogio", "nota": "nota"}
DESFECHOS = {"diagnostico_correto": "o diagnóstico está certo", "agente_errou": "o agente errou", "decisao_intencional": "é decisão intencional do projeto, não defeito"}
CAUSAS = tuple(taxonomia.CAUSAS_RAIZ)
PAPEIS = ("analista", "agente")
TIPOS = ("comentario", "estado_da_conversa", "veredito", "campos_55", "causa_sugerida", "lido")
SO_DO_ANALISTA = ("estado_da_conversa", "campos_55", "causa_sugerida", "lido")
LIMITE_DO_TEXTO = 4000
_NOME_DE_CASO = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{0,99}$")


def agora() -> str:
    return dt.datetime.now().isoformat(timespec="seconds")


def _texto(valor, campo: str, obrigatorio: bool = True, limite: int = LIMITE_DO_TEXTO) -> str:
    if valor is None and not obrigatorio:
        return ""
    if not isinstance(valor, str):
        raise ValueError(f"{campo}: esperava texto")
    valor = valor.strip()
    if obrigatorio and not valor:
        raise ValueError(f"{campo}: o texto está vazio")
    if len(valor) > limite:
        raise ValueError(f"{campo}: o texto passa de {limite} caracteres")
    return valor


def _autor(valor) -> dict:
    if not isinstance(valor, dict):
        raise ValueError("autor: esperava nome e papel")
    papel = valor.get("papel")
    if papel not in PAPEIS:
        raise ValueError(f"autor: o papel {papel!r} não é um de {PAPEIS}")
    return {"nome": _texto(valor.get("nome"), "autor.nome", limite=80), "papel": papel}


def _iteracao(valor) -> dict:
    if not isinstance(valor, dict):
        raise ValueError("iteracao: esperava a trilha, o hash dos eventos e o número da iteração revisada")
    numero = valor.get("numero")
    if not isinstance(numero, int) or isinstance(numero, bool) or numero < 1:
        raise ValueError("iteracao.numero: esperava um inteiro a partir de 1")
    return {"tid": _texto(valor.get("tid"), "iteracao.tid", limite=300), "hash": _texto(valor.get("hash"), "iteracao.hash", limite=80), "numero": numero}


def _ancora(valor) -> dict | None:
    if valor is None:
        return None
    if not isinstance(valor, dict):
        raise ValueError("ancora: esperava o bloco, o trecho e a posição dele no bloco")
    inicio, fim = valor.get("inicio"), valor.get("fim")
    if not all(isinstance(x, int) and not isinstance(x, bool) for x in (inicio, fim)) or inicio < 0 or fim <= inicio:
        raise ValueError("ancora: a posição do trecho no bloco é inválida (o fim vem depois do início)")
    return {"bloco": _texto(valor.get("bloco"), "ancora.bloco", limite=120), "trecho": _texto(valor.get("trecho"), "ancora.trecho", limite=2000), "inicio": inicio, "fim": fim}


def _conversas_abertas(eventos: list[dict]) -> set[str]:
    return {e["conversa"] for e in eventos if e.get("tipo") == "comentario"}


def validar(evento: dict, anteriores: list[dict]) -> dict:
    """O evento conferido e normalizado, sem `id`, `ts` nem `revisao`; `anteriores` são os eventos já aceitos do mesmo caso (para saber que
    conversas existem). Recusa com ValueError, dizendo o que não bate."""
    if not isinstance(evento, dict):
        raise ValueError("evento: esperava um objeto")
    tipo = evento.get("tipo")
    if tipo not in TIPOS:
        raise ValueError(f"tipo: {tipo!r} não é um de {TIPOS}")
    autor = _autor(evento.get("autor"))
    base = {"tipo": tipo, "autor": autor, "iteracao": _iteracao(evento.get("iteracao"))}
    if autor["papel"] == "agente" and tipo in SO_DO_ANALISTA:
        raise ValueError(f"{tipo}: o agente só comenta; isto é do analista (a IA nunca aprova sozinha)")
    if tipo == "comentario":
        conversa = evento.get("conversa")
        ancora = _ancora(evento.get("ancora"))
        if conversa is not None:
            if conversa not in _conversas_abertas(anteriores):
                raise ValueError(f"conversa: {conversa!r} não existe neste caso")
            if ancora is not None:
                raise ValueError("ancora: o trecho é de quem abre a conversa; a resposta entra na conversa que já existe")
        rotulo = evento.get("rotulo")
        if rotulo is not None and rotulo not in ROTULOS:
            raise ValueError(f"rotulo: {rotulo!r} não é um de {tuple(ROTULOS)}")
        return {**base, "texto": _texto(evento.get("texto"), "texto"), "conversa": conversa, "ancora": ancora, "rotulo": rotulo, "bloqueante": bool(evento.get("bloqueante"))}
    if tipo == "estado_da_conversa":
        if evento.get("conversa") not in _conversas_abertas(anteriores):
            raise ValueError(f"conversa: {evento.get('conversa')!r} não existe neste caso")
        if evento.get("estado") not in ESTADOS_DA_CONVERSA:
            raise ValueError(f"estado: {evento.get('estado')!r} não é um de {tuple(ESTADOS_DA_CONVERSA)}")
        return {**base, "conversa": evento["conversa"], "estado": evento["estado"]}
    if tipo == "veredito":
        veredito = evento.get("veredito")
        if veredito not in VEREDITOS:
            raise ValueError(f"veredito: {veredito!r} não é um de {tuple(VEREDITOS)}")
        if autor["papel"] == "agente" and veredito != "comentar":
            raise ValueError("veredito: o agente só comenta; aprovar, pedir espera ou rejeitar é do analista (a IA nunca aprova sozinha)")
        resumo = _texto(evento.get("resumo"), "resumo", obrigatorio=False)
        if veredito == "rejeitar" and not resumo:
            raise ValueError("resumo: rejeitar pede o motivo no resumo da revisão")
        desfecho = evento.get("desfecho")
        if desfecho is not None and desfecho not in DESFECHOS:
            raise ValueError(f"desfecho: {desfecho!r} não é um de {tuple(DESFECHOS)}")
        return {**base, "veredito": veredito, "resumo": resumo, "desfecho": desfecho}
    if tipo == "campos_55":
        for campo in ("severidade", "prioridade", "estado"):
            if campo not in evento:
                raise ValueError(f"{campo}: faltou no evento (severidade e prioridade podem vir em branco; o estado não)")
        severidade, prioridade, estado_ = evento["severidade"], evento["prioridade"], evento["estado"]
        if severidade is not None and severidade not in SEVERIDADES:
            raise ValueError(f"severidade: {severidade!r} não é um de {SEVERIDADES}")
        if prioridade is not None and prioridade not in PRIORIDADES:
            raise ValueError(f"prioridade: {prioridade!r} não é um de {PRIORIDADES}")
        if estado_ not in ESTADOS_55:
            raise ValueError(f"estado: {estado_!r} não é um de {ESTADOS_55}")
        return {**base, "severidade": severidade, "prioridade": prioridade, "estado": estado_}
    if tipo == "causa_sugerida":
        if evento.get("causa") not in CAUSAS:
            raise ValueError(f"causa: {evento.get('causa')!r} não está na lista de causas do agente")
        campo = _texto(evento.get("campo"), "campo", obrigatorio=False, limite=120) or None
        return {**base, "causa": evento["causa"], "campo": campo, "texto": _texto(evento.get("texto"), "texto", obrigatorio=False)}
    return base     # lido: a iteração marcada é a do próprio evento


class Revisoes:
    """Os arquivos de revisão de uma pasta: um JSONL por caso, lido inteiro e acrescentado linha a linha, com uma trava para o servidor."""

    def __init__(self, pasta: Path) -> None:
        self.pasta = Path(pasta)
        self._trava = threading.Lock()

    def arquivo(self, caso: str) -> Path:
        if not isinstance(caso, str) or not _NOME_DE_CASO.match(caso):
            raise ValueError(f"caso: {caso!r} não é um identificador de caso (letras, números, hífen e sublinhado)")
        return self.pasta / f"{caso}.jsonl"

    def eventos(self, caso: str) -> list[dict]:
        arq = self.arquivo(caso)
        if not arq.exists():
            return []
        return [json.loads(linha) for linha in arq.read_text(encoding="utf-8").splitlines() if linha.strip()]

    def _acrescentar(self, caso: str, novos: list[dict], anteriores: list[dict], revisao: bool) -> list[dict]:
        """Numera, data e grava os eventos já validados, todos numa escrita só."""
        n = len(anteriores)
        momento = agora()
        marca = f"r{n + 1}" if revisao else None
        prontos = []
        for i, ev in enumerate(novos, start=1):
            pronto = {"id": f"e{n + i}", "ts": momento, "revisao": marca, **ev}
            if pronto["tipo"] == "comentario" and pronto["conversa"] is None:
                pronto["conversa"] = f"c{n + i}"
            prontos.append(pronto)
        arq = self.arquivo(caso)
        arq.parent.mkdir(parents=True, exist_ok=True)
        with arq.open("a", encoding="utf-8", newline="\n") as f:
            f.write("".join(json.dumps(p, ensure_ascii=False) + "\n" for p in prontos))
        return prontos

    def registrar(self, caso: str, evento: dict) -> dict:
        """Valida e acrescenta um evento ao arquivo do caso; devolve o evento como ficou gravado."""
        with self._trava:
            anteriores = self.eventos(caso)
            return self._acrescentar(caso, [validar(evento, anteriores)], anteriores, revisao=False)[0]

    def enviar_revisao(self, caso: str, autor: dict, iteracao: dict, veredito: str, resumo: str = "", desfecho: str | None = None, rascunhos=(),
                       campos_55: dict | None = None, causa_sugerida: dict | None = None) -> list[dict]:
        """A revisão inteira de uma vez: os comentários em rascunho, os campos da 5.5 e a causa corrigida (quando vierem) e, por último, o
        veredito. Tudo é validado antes; se um item não passa, nada é gravado."""
        with self._trava:
            anteriores = self.eventos(caso)
            comum = {"autor": autor, "iteracao": iteracao}
            pedidos = [{"tipo": "comentario", **comum, **dict(r)} for r in rascunhos]
            if campos_55 is not None:
                pedidos.append({"tipo": "campos_55", **comum, **campos_55})
            if causa_sugerida is not None:
                pedidos.append({"tipo": "causa_sugerida", **comum, **causa_sugerida})
            pedidos.append({"tipo": "veredito", **comum, "veredito": veredito, "resumo": resumo, "desfecho": desfecho})
            vistos = list(anteriores)
            validos = []
            for p in pedidos:
                v = validar(p, vistos)
                validos.append(v)
                # uma resposta em rascunho pode citar uma conversa que já existia; conversa aberta no mesmo envio ainda não tem id
                vistos.append({**v, "conversa": v.get("conversa") or f"c{len(vistos) + 1}"} if v["tipo"] == "comentario" else v)
            return self._acrescentar(caso, validos, anteriores, revisao=True)


def _mesma(a: dict | None, b: dict | None) -> bool:
    return bool(a and b and a.get("tid") == b.get("tid") and a.get("hash") == b.get("hash"))


def estado(eventos: list[dict], iteracoes: list[dict]) -> dict:
    """O que a página mostra de um caso, refeito dos eventos: as conversas com os comentários e o estado, os vereditos, os campos da 5.5, a
    causa corrigida e a marca de lido. `iteracoes` são as iterações do caso em ordem (tid, hash, numero); a última é a atual."""
    atual = iteracoes[-1] if iteracoes else None
    conversas: dict[str, dict] = {}
    vereditos, campos, causa, lido = [], {"severidade": None, "prioridade": None, "estado": "aberto"}, None, None
    for e in eventos:
        tipo = e.get("tipo")
        if tipo == "comentario":
            c = conversas.setdefault(e["conversa"], {"id": e["conversa"], "ancora": e.get("ancora"), "estado": "ativa", "historico": [], "iteracao": e["iteracao"],
                                                    "de_iteracao_anterior": not _mesma(e["iteracao"], atual), "aberta_em": e["ts"], "comentarios": []})
            c["comentarios"].append({k: e.get(k) for k in ("id", "autor", "ts", "texto", "rotulo", "bloqueante", "revisao")})
        elif tipo == "estado_da_conversa" and e.get("conversa") in conversas:
            conversas[e["conversa"]]["estado"] = e["estado"]
            conversas[e["conversa"]]["historico"].append({"estado": e["estado"], "autor": e["autor"], "ts": e["ts"]})
        elif tipo == "veredito":
            vereditos.append({k: e.get(k) for k in ("id", "autor", "ts", "veredito", "resumo", "desfecho", "iteracao", "revisao")})
        elif tipo == "campos_55":
            campos = {k: e.get(k) for k in ("severidade", "prioridade", "estado")}
        elif tipo == "causa_sugerida":
            causa = {k: e.get(k) for k in ("id", "autor", "ts", "causa", "campo", "texto", "iteracao")}
        elif tipo == "lido":
            lido = {**e["iteracao"], "ts": e["ts"], "autor": e["autor"]}
    do_analista = [v for v in vereditos if v["autor"]["papel"] == "analista"]
    veredito_atual = do_analista[-1] if do_analista else None
    lista = list(conversas.values())
    novas = len(iteracoes)
    if lido is not None:
        posicao = next((i for i, it in enumerate(iteracoes) if it.get("tid") == lido["tid"]), None)
        novas = len(iteracoes) - 1 - posicao if posicao is not None else len(iteracoes)
    return {"conversas": lista, "vereditos": vereditos, "veredito_atual": veredito_atual,
            "veredito_vale_para_a_iteracao_atual": bool(veredito_atual and _mesma(veredito_atual["iteracao"], atual)),
            "campos_55": campos, "causa_sugerida": causa, "lido": lido, "lido_valido": _mesma(lido, atual), "iteracoes_novas_desde_o_lido": novas,
            "contagem": {"conversas": len(lista), "ativas": sum(1 for c in lista if c["estado"] == "ativa"),
                         "resolvidas": sum(1 for c in lista if c["estado"] == "resolvida"),
                         "nao_serao_tratadas": sum(1 for c in lista if c["estado"] == "nao_sera_tratada"),
                         "comentarios": sum(len(c["comentarios"]) for c in lista)}}
