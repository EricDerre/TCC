#!/usr/bin/env python3
# ! Alteração de IA - Revisar: arquivo novo (25/11/2026, Pós-Fase 4, pacote Q6): os dados do hub central. `Acervo` lê as trilhas v2 das
# corridas que o hub mostra (por padrão a 18d, a 21d, a 24 e a 28b) e monta, na hora e em memória: a lista de casos com diagnóstico; as
# iterações do mesmo caso (cada vez que o agente diagnosticou aquele caso, em ordem de tempo, em qualquer das corridas); o caso inteiro, com
# o relatório v3 partido em blocos, a evidência ao lado (a resposta da API, a árvore da tela, o contrato, o sintoma, os verbetes entregues
# pela camada de leitura, o pedido enviado ao modelo e o texto do modelo), a árvore de decisão e os eventos da trilha; e o que mudou entre
# duas iterações. O relatório sai de `gerar_relatorio_raciocinio.relatorio_do_caso_v3` e a árvore de `arvore_de_decisao.arvore_do_caso`, as
# mesmas funções dos pacotes Q1 e Q3, sem reescrever o texto delas.
# ! Motivo: plano aprovado da Pós-Fase 4, seção 3.6 (itens 1 e 4), e ficha 97 (decisão 157). O hub só lê: os registros oficiais em
# `resultados_alvo/` nunca são regravados, e a corrida 28b não tem `relatorios_v3/` nem `arvores/` gravados, então montar em memória é o
# único jeito de mostrá-la sem escrever na pasta dela. Um caso é procurado pelo identificador da trilha num dicionário montado dos arquivos;
# o identificador que vem da página nunca vira caminho de arquivo. A leitura é refeita quando o arquivo da trilha muda de tamanho ou de hora,
# para uma corrida em andamento aparecer sem reabrir o hub.
"""Os dados do hub central (Pós-Fase 4, pacote Q6): corridas, casos, iterações e o caso montado da trilha gravada."""
from __future__ import annotations

import json
import re
import threading
import time
from pathlib import Path

import arvore_de_decisao as ad
import biblioteca_leitura as bl
import gerar_relatorio_raciocinio as grr
import hub_pagina as hp
import trilha as tr

# as corridas que o hub mostra quando nenhuma é pedida: as três leituras vigentes da Fase 4 e a medida do agente na Fase 5
CORRIDAS_PADRAO = (
    {"pasta": "fase4_tela_v4", "rotulo": "corrida 18d", "descricao": "os casos de avaliação diagnosticados na tela e em texto (Fase 4)"},
    {"pasta": "fase4_ensaio_v4", "rotulo": "corrida 21d", "descricao": "o ensaio dos dez cenários, uma execução de cada (Fase 4)"},
    {"pasta": "fase4_ineditos", "rotulo": "corrida 24", "descricao": "os casos inéditos, em texto (Fase 4)"},
    {"pasta": "fase5_agente_b", "rotulo": "corrida 28b", "descricao": "a medida do agente na Fase 5: dez cenários, cinco repetições"},
)
PASTA_DOS_TRACES = "traces"
_NOME_DE_CORRIDA = re.compile(r"^[A-Za-z0-9_][A-Za-z0-9_-]{0,79}$")
_SHA = re.compile(r"^[0-9a-f]{8,64}$")
# o que é comparado entre duas iterações do mesmo caso, na ordem em que aparece na página
CAMPOS_DA_MUDANCA = (("corrida", "rotulo_da_corrida"), ("origem do caso", "origem"), ("causa respondida", "escolha"), ("campo apontado", "campo"), ("confiança", "confianca"),
                     ("verbetes entregues", "verbetes"), ("divergência entre o declarado e o conferido", "divergencia"), ("cura de localizador", "cura"),
                     ("falha registrada", "falha"))


def chave_do_caso(tid: str) -> str:
    """O caso de uma trilha, sem a repetição (`#2`) nem a origem (`@tela`, `@fixture`): é o que junta as iterações do mesmo caso."""
    return tid.rsplit("/", 1)[-1].split("@")[0].split("#")[0]


def _em_palavras(valor) -> str:
    if isinstance(valor, bool):
        return "sim" if valor else "não"
    if isinstance(valor, (list, tuple)):
        return ", ".join(str(v) for v in valor) or "nenhum"
    return "nenhum" if valor is None else str(valor)


class Acervo:
    """As corridas que o hub mostra, lidas das pastas em `raiz` (o `resultados_alvo/`); nada é escrito nelas."""

    def __init__(self, raiz: Path, corridas: tuple[str, ...] | None = None, leituras: dict | None = None, calibracao: dict | None = None,
                 limiares: dict | None = None) -> None:
        self.raiz = Path(raiz)
        padrao = {c["pasta"]: c for c in CORRIDAS_PADRAO}
        nomes = tuple(corridas) if corridas else tuple(padrao)
        self._corridas: list[dict] = []
        for nome in nomes:
            if not isinstance(nome, str) or not _NOME_DE_CORRIDA.match(nome):
                raise ValueError(f"corrida: {nome!r} não é nome de pasta de corrida")
            pasta = self.raiz / nome
            if not pasta.is_dir() or self._arquivo_da_trilha(pasta) is None:
                raise ValueError(f"corrida: a pasta {nome!r} não existe em {self.raiz} ou não tem trilha gravada")
            self._corridas.append({"pasta": nome, "rotulo": padrao.get(nome, {}).get("rotulo", nome), "descricao": padrao.get(nome, {}).get("descricao", "")})
        self.leituras = leituras if leituras is not None else bl.carregar()
        self.calibracao = calibracao if calibracao is not None else ad.carregar_calibracao(self.raiz / "fase4" / "calibracao.json")
        self.limiares = limiares if limiares is not None else ad.carregar_limiares(self.raiz / "fase4" / "limiares.json")
        self._cache: dict[str, dict] = {}
        self._trava = threading.RLock()

    # ------------------------------------------------------------------ a leitura de uma corrida

    @staticmethod
    def _condicoes(pasta: Path) -> dict:
        arq = pasta / "condicoes_fase4.json"
        try:
            return json.loads(arq.read_text(encoding="utf-8")) if arq.exists() else {}
        except ValueError:
            return {}

    @classmethod
    def _arquivo_da_trilha(cls, pasta: Path) -> Path | None:
        modo = cls._condicoes(pasta).get("modo")
        if modo and (pasta / f"trilha_{modo}.jsonl").exists():
            return pasta / f"trilha_{modo}.jsonl"
        return next(iter(sorted(pasta.glob("trilha_*.jsonl"))), None)

    def _linha(self, corrida: dict, eventos: list[dict], tid: str, pasta: Path) -> dict:
        arvore = ad.arvore_do_caso(eventos, tid, pasta_blobs=pasta / "blobs", leituras=self.leituras, calibracao=self.calibracao, limiares=self.limiares)
        c = grr._contexto_v3(eventos, tid, pasta / "blobs", self.leituras)
        r = arvore["resumo"]
        origem = "localizador da tela" if c["eh_localizador"] else ("texto do caso" if c["eh_texto"] else "tela")
        return {"tid": tid, "corrida": corrida["pasta"], "rotulo_da_corrida": corrida["rotulo"], "nome": c["nome"], "caso": chave_do_caso(tid), "titulo": c["titulo"],
                "escolha": r["escolha"], "causa_em_palavras": r["causa_em_palavras"], "campo": r["campo"], "selo": r["selo"], "confianca": r["confianca"] or "desconhecida",
                "divergencia": bool(r["divergencia"]), "cura": bool(r["cura"]), "falha": r["falha"], "classe": c["classe"], "nivel": c["nivel"], "origem": origem,
                "verbetes": list(c["entregues"]), "ts": c["ts_entrada"] or c["seq"][0].get("ts") or "", "seq": c["seq"][0]["seq"], "hash": arvore["eventos"]["hash"]}

    def _carregar(self, corrida: dict) -> dict:
        """Os eventos e as linhas da lista de uma corrida, relidos só quando o arquivo da trilha muda. Se o arquivo estiver sendo regravado
        pela corrida neste instante e vier pela metade, vale a última leitura boa."""
        pasta = self.raiz / corrida["pasta"]
        arq = self._arquivo_da_trilha(pasta)
        with self._trava:
            guardado = self._cache.get(corrida["pasta"])
            try:
                info = arq.stat() if arq else None
                assinatura = (str(arq), info.st_mtime_ns, info.st_size) if info else None
                if guardado and guardado["assinatura"] == assinatura:
                    return guardado
                eventos = tr.ler(arq) if arq else []
                cab = next((e["dados"] for e in eventos if e["tipo"] == "corrida"), {})
                tids = [tid for tid, seq in tr.por_trilha(eventos).items() if tid and any(e["tipo"] == "decisao" for e in seq)]
                linhas = [self._linha(corrida, eventos, tid, pasta) for tid in tids]
            except (OSError, ValueError, KeyError):
                if guardado:
                    return guardado
                raise
            condicoes = self._condicoes(pasta)
            novo = {"assinatura": assinatura, "pasta": pasta, "arquivo": arq, "eventos": eventos, "cab": cab, "condicoes": condicoes, "linhas": linhas,
                    "por_tid": {l["tid"]: l for l in linhas}}
            self._cache[corrida["pasta"]] = novo
            return novo

    # ------------------------------------------------------------------ a lista

    def corridas(self) -> list[dict]:
        saida = []
        for corrida in self._corridas:
            dado = self._carregar(corrida)
            cab = dado["cab"]
            saida.append({**corrida, "modo": dado["condicoes"].get("modo") or cab.get("modo"), "modelo": cab.get("modelo"), "inicio": cab.get("inicio"), "fim": cab.get("fim"),
                          "versao_ollama": cab.get("versao_ollama"), "hash_biblioteca": cab.get("hash_biblioteca"), "trilha": dado["arquivo"].name if dado["arquivo"] else None,
                          "casos": len(dado["linhas"])})
        return saida

    def _todas(self) -> list[dict]:
        ordem = {c["pasta"]: i for i, c in enumerate(self._corridas)}
        linhas = [dict(l) for corrida in self._corridas for l in self._carregar(corrida)["linhas"]]
        por_caso: dict[str, list[dict]] = {}
        for l in linhas:
            por_caso.setdefault(l["caso"], []).append(l)
        for grupo in por_caso.values():
            grupo.sort(key=lambda l: (l["ts"], ordem[l["corrida"]], l["seq"]))
            for n, l in enumerate(grupo, start=1):
                l["iteracao"], l["iteracoes"] = n, len(grupo)
        return linhas

    def indice(self) -> list[dict]:
        """Uma linha por trilha com diagnóstico, na ordem das corridas e dos casos dentro delas, com o número da iteração dentro do caso."""
        return [{k: v for k, v in l.items() if k != "seq"} for l in self._todas()]

    def iteracoes(self, caso: str) -> list[dict]:
        """As iterações de um caso, da mais antiga à mais nova: cada diagnóstico que o agente fez dele, em qualquer das corridas."""
        do_caso = sorted((l for l in self._todas() if l["caso"] == caso), key=lambda l: l["iteracao"])
        return [{"numero": l["iteracao"], "tid": l["tid"], "hash": l["hash"], "corrida": l["corrida"], "rotulo_da_corrida": l["rotulo_da_corrida"], "nome": l["nome"],
                 "ts": l["ts"], "escolha": l["escolha"], "confianca": l["confianca"], "origem": l["origem"]} for l in do_caso]

    def _achar(self, tid: str) -> tuple[dict, dict]:
        """A corrida carregada e a linha de uma trilha, procuradas pelo identificador entre as trilhas lidas; o que não está lá é recusado."""
        if isinstance(tid, str):
            for corrida in self._corridas:
                dado = self._carregar(corrida)
                if tid in dado["por_tid"]:
                    return dado, next(l for l in self._todas() if l["tid"] == tid)
        raise KeyError(f"trilha {tid!r} não está nas corridas do hub")

    def iteracao(self, tid: str) -> dict:
        """O caso, o hash dos eventos e o número da iteração de uma trilha; é o que o servidor grava em cada evento de revisão."""
        with self._trava:
            _, linha = self._achar(tid)
            return {"caso": linha["caso"], "tid": linha["tid"], "hash": linha["hash"], "numero": linha["iteracao"]}

    # ! Alteração de IA - Revisar: (25/11/2026, pacote Q6, etapa 3) `trace` devolve o arquivo do trace do Playwright de uma trilha, quando a
    # corrida o gravou, e `arvore` devolve só a árvore de decisão dela, sem montar o relatório.
    # ! Motivo: decisão 93. O caminho do trace é montado aqui, da pasta da corrida e do nome do caso, depois de a trilha ser achada entre as
    # trilhas lidas; o identificador que vem da página nunca entra num caminho. A árvore sozinha serve à vista "Corrida ao vivo", que relê
    # o último diagnóstico a cada dois segundos e não precisa do relatório inteiro.
    def trace(self, tid: str) -> Path | None:
        with self._trava:
            dado, _ = self._achar(tid)
            arq = dado["pasta"] / PASTA_DOS_TRACES / f"{grr.nome_do_relatorio(tid)}.zip"
            return arq if arq.is_file() else None

    def arvore(self, tid: str) -> dict:
        with self._trava:
            dado, _ = self._achar(tid)
            return ad.arvore_do_caso(dado["eventos"], tid, pasta_blobs=dado["pasta"] / "blobs", leituras=self.leituras, calibracao=self.calibracao, limiares=self.limiares)

    def mudancas(self, tid_de: str, tid_para: str) -> list[dict]:
        """O que mudou de uma iteração para outra, campo a campo, só o que é diferente."""
        _, antes = self._achar(tid_de)
        _, depois = self._achar(tid_para)
        saida = []
        for rotulo, chave in CAMPOS_DA_MUDANCA:
            a, d = _em_palavras(antes.get(chave)), _em_palavras(depois.get(chave))
            if a != d:
                saida.append({"campo": rotulo, "antes": a, "depois": d})
        return saida

    # ------------------------------------------------------------------ o caso

    def _relatorio(self, dado: dict, tid: str) -> dict:
        pasta, cond = dado["pasta"], dado["condicoes"]
        modo = cond.get("modo") or dado["cab"].get("modo")
        k = cond.get("k") if isinstance(cond.get("k"), int) else 3
        nome = grr.nome_do_relatorio(tid)
        v2 = f"../relatorios/{nome}.md" if (pasta / "relatorios" / f"{nome}.md").exists() else None
        md = grr.relatorio_do_caso_v3(dado["eventos"], tid, comando_reexecucao=grr.comando_de_reexecucao(modo, cond.get("saida") or pasta.name, tid, k),
                                      pasta_blobs=pasta / "blobs", leituras=self.leituras, arquivo_trilha=dado["arquivo"].name, relatorio_v2=v2)
        partes: list[tuple[str | None, list[str]]] = [(None, [])]
        em_codigo = False
        for linha in md.split("\n"):
            if linha.startswith("```"):
                em_codigo = not em_codigo
            if linha.startswith("## ") and not em_codigo:
                partes.append((linha[3:].strip(), []))
            else:
                partes[-1][1].append(linha)
        blocos, rastro = [], ""
        for titulo, linhas in partes[1:]:
            corpo = "\n".join(linhas).strip("\n")
            m = re.match(r"^(\d+)\. (.*)$", titulo)
            if not m:
                rastro = hp.md_para_html(corpo)
                continue
            n, nome_do_bloco = int(m.group(1)), m.group(2)
            marcado = hp.md_para_html(corpo)
            blocos.append({"id": f"b{n}-{hp.slug(nome_do_bloco)}", "numero": n, "titulo": nome_do_bloco, "grupo": "5.5" if n <= len(grr.CAMPOS_55) else "agente",
                           "markdown": corpo, "html": marcado, "texto": hp.texto_puro(marcado)})
        return {"preambulo_html": hp.md_para_html("\n".join(l for l in partes[0][1] if not l.startswith("# "))), "blocos": blocos, "rastro_html": rastro}

    def _evidencia(self, c: dict) -> list[dict]:
        dados, vivo, inter, blobs = c["dados_do_caso"] or {}, c["caso_vivo"] or {}, c["inter"] or {}, c["blobs"]
        saida = []
        corpo = vivo.get("corpo_completo") or dados.get("corpo")
        if corpo is not None or dados.get("requisicao"):
            nota = "; ".join(x for x in (dados.get("requisicao") or c["requisicao"], f"status {dados.get('status')}" if dados.get("status") is not None else None,
                                         inter.get("content_type"), f"{inter['tempo_ms']} ms" if inter.get("tempo_ms") is not None else None) if x)
            item = {"id": "resposta", "titulo": "Resposta da API", "tipo": "codigo", "nota": nota, "texto": str(corpo if corpo is not None else "")}
            if vivo.get("corpo_completo") and dados.get("corpo") and dados["corpo"] != vivo["corpo_completo"]:
                item["texto_podado"] = str(dados["corpo"])
            saida.append(item)
        if dados.get("arvore"):
            saida.append({"id": "tela", "titulo": "Árvore da tela", "tipo": "codigo", "nota": vivo.get("observacao_da_poda") or "a árvore de acessibilidade depois da poda",
                          "texto": str(dados["arvore"])})
        if dados.get("contrato"):
            saida.append({"id": "contrato", "titulo": "Contrato", "tipo": "codigo", "nota": "o que a interface espera receber", "texto": str(dados["contrato"])})
        sintoma = "\n\n".join(str(x) for x in (dados.get("sintoma"), dados.get("observacao")) if x)
        if sintoma:
            saida.append({"id": "sintoma", "titulo": "Sintoma", "tipo": "texto", "nota": "o que foi visto na tela ou descrito no caso", "texto": sintoma})
        if c["entregues"]:
            itens = []
            for vid in c["entregues"]:
                leitura = self.leituras.get(vid) or {}
                itens.append({"id": vid, "titulo": leitura.get("titulo") or vid, "arquivo": f"{grr.PREFIXO_DA_LEITURA}/{leitura['caminho']}" if leitura.get("caminho") else None,
                              "curado": bool(leitura.get("curado")),
                              "secoes": [{"titulo": t, "html": hp.md_para_html(corpo_)} for t, corpo_ in (leitura.get("secoes") or {}).items() if str(corpo_).strip()]})
            saida.append({"id": "verbetes", "titulo": "Verbetes entregues", "tipo": "verbetes", "nota": "o que o modelo recebeu da biblioteca, pela camada de leitura", "itens": itens})
        prompt = next((e["dados"] for e in c["por_tipo"].get("prompt", []) if e["dados"].get("etapa") == "diagnostico"), None)
        if prompt and blobs.get(prompt.get("sha")):
            saida.append({"id": "pedido", "titulo": "Pedido ao modelo", "tipo": "codigo", "nota": f"o texto enviado ao modelo, montado pelo código ({prompt.get('chars')} caracteres)",
                          "texto": blobs[prompt["sha"]]})
        inferencia = next((e["dados"] for e in c["por_tipo"].get("inferencia", []) if e["dados"].get("etapa") == "diagnostico"), None)
        resposta = blobs.get(inferencia.get("resposta")) if inferencia else None
        if resposta:
            saida.append({"id": "texto_do_modelo", "titulo": "Texto do modelo", "tipo": "codigo", "rotulo": ad.TEXTO_DO_MODELO,
                          "nota": "a resposta como veio, sem garantia; o que o código conferiu dela está no relatório", "texto": resposta})
        return saida

    @staticmethod
    def _eventos_da_trilha(c: dict) -> tuple[list[dict], dict]:
        blobs = c["blobs"]
        eventos, citados = [], {}
        for e in c["seq"]:
            eventos.append({"seq": e["seq"], "tipo": e["tipo"], "ts": e.get("ts"), "origem": e.get("origem"), "pai": e.get("pai"), "camada": e.get("camada"),
                            "passo": e.get("passo"), "resumo": grr._resumo_v3(e, blobs) or e["tipo"], "dados": e["dados"]})
            for valor in e["dados"].values():
                if isinstance(valor, str) and _SHA.match(valor) and blobs.get(valor) is not None:
                    citados[valor] = blobs[valor]
        return eventos, citados

    def caso(self, tid: str) -> dict:
        """Tudo o que a página mostra de uma trilha: o relatório em blocos, a evidência, a árvore, os eventos e as iterações do caso."""
        with self._trava:
            dado, linha = self._achar(tid)
            pasta, eventos = dado["pasta"], dado["eventos"]
            c = grr._contexto_v3(eventos, tid, pasta / "blobs", self.leituras)
            arvore = ad.arvore_do_caso(eventos, tid, pasta_blobs=pasta / "blobs", leituras=self.leituras, calibracao=self.calibracao, limiares=self.limiares)
            iteracoes = self.iteracoes(linha["caso"])
            anterior = next((i for i in iteracoes if i["numero"] == linha["iteracao"] - 1), None)
            trilha_, blobs = self._eventos_da_trilha(c)
            cab = dado["cab"]
            causa = (f"Causa respondida: `{linha['escolha']}` ({linha['causa_em_palavras']})" if linha["escolha"] is not None else "Sem causa respondida: a linha CAUSA_RAIZ não veio")
            comentario = (causa + (f"; campo `{linha['campo']}`" if linha["campo"] else "") + f"; confiança {linha['confianca']}"
                          + ("; o que o modelo declarou não bate com o que o código conferiu" if linha["divergencia"] else "")
                          + ("; o localizador foi curado e o roteiro refeito" if linha["cura"] else "") + ".")
            trace = self.trace(tid)
            corrida = next(x for x in self.corridas() if x["pasta"] == linha["corrida"])
            return {"tid": tid, "caso": linha["caso"], "nome": linha["nome"], "titulo": linha["titulo"], "hash": linha["hash"], "corrida": corrida,
                    "resumo": {k: v for k, v in linha.items() if k != "seq"}, "iteracao": linha["iteracao"], "iteracoes": iteracoes,
                    "mudancas_desde_a_anterior": self.mudancas(anterior["tid"], tid) if anterior else [],
                    "relatorio": self._relatorio(dado, tid), "evidencia": self._evidencia(c), "arvore": arvore, "trilha": trilha_, "blobs": blobs,
                    "comentario_do_agente": {"autor": {"nome": f"agente ({cab.get('modelo')}, biblioteca {cab.get('hash_biblioteca')})", "papel": "agente"},
                                             "veredito": "comentar", "ts": linha["ts"], "texto": comentario},
                    "trace": {"existe": trace is not None, "arquivo": trace.name if trace is not None else None}}


# ! Alteração de IA - Revisar: (25/11/2026, pacote Q6, etapa 3) `AoVivo` lê a corrida em andamento para a vista "Corrida ao vivo" do hub: acha
# o `progresso.json` gravado por último entre as pastas de `resultados_alvo/` (o estado da barra de progresso do pacote Q4), diz há quantos
# segundos ele foi regravado e se uma inferência está rodando agora, e traz o último diagnóstico da trilha daquela pasta (a causa
# respondida, a confiança, as alternativas com a probabilidade lida e os verbetes entregues).
# ! Motivo: decisão 93 e ficha 45 (a aba "Cérebro ao vivo" do plano da Fase 4, que não foi feita) e plano da Pós-Fase 4, seção 3.5 ("grava um
# arquivo de estado em JSON que o hub lê"). `progresso.py` regrava o arquivo no máximo uma vez por segundo enquanto o modelo trabalha; se
# ele está parado há mais de `LIMITE_DE_IDADE_S`, a inferência acabou ou a corrida morreu, e a página não pode continuar dizendo "rodando".
# O executor regrava a trilha inteira a cada caso; se a leitura pegar o arquivo pela metade, vale a última boa (`Acervo._carregar`).
LIMITE_DE_IDADE_S = 30
ESTADOS_RODANDO = ("indeterminado", "determinado")


class AoVivo:
    """A corrida que gravou o estado da barra por último, lida da pasta dela; nada é escrito."""

    def __init__(self, raiz: Path, leituras: dict | None = None, calibracao: dict | None = None, limiares: dict | None = None) -> None:
        self.raiz = Path(raiz)
        self.leituras, self.calibracao, self.limiares = leituras, calibracao, limiares
        self._acervos: dict[str, Acervo] = {}
        self._trava = threading.Lock()

    def _mais_recente(self) -> Path | None:
        candidatos = []
        for arq in self.raiz.glob("*/progresso.json"):
            try:
                candidatos.append((arq.stat().st_mtime, arq))
            except OSError:
                continue
        return max(candidatos)[1] if candidatos else None

    def _ultimo_diagnostico(self, pasta: Path) -> tuple[dict | None, int]:
        nome = pasta.name
        if not _NOME_DE_CORRIDA.match(nome):
            return None, 0
        try:
            if nome not in self._acervos:
                self._acervos[nome] = Acervo(self.raiz, corridas=(nome,), leituras=self.leituras, calibracao=self.calibracao, limiares=self.limiares)
            acervo = self._acervos[nome]
            linhas = acervo.indice()
            if not linhas:
                return None, 0
            linha = linhas[-1]
            causa = next((d for d in acervo.arvore(linha["tid"])["decisoes"] if d["chave"] == "causa"), {})
        except (OSError, ValueError, KeyError):
            return None, 0          # a corrida ainda não gravou trilha, ou gravou um arquivo que não dá para ler agora
        alternativas = [{"opcao": a.get("opcao"), "probabilidade": a.get("probabilidade"), "escolhida": bool(a.get("escolhida"))} for a in causa.get("alternativas") or []]
        verbetes = [{"id": v, "titulo": (acervo.leituras.get(v) or {}).get("titulo") or v} for v in linha["verbetes"]]
        return ({"tid": linha["tid"], "caso": linha["caso"], "nome": linha["nome"], "titulo": linha["titulo"], "escolha": linha["escolha"],
                 "causa_em_palavras": linha["causa_em_palavras"], "campo": linha["campo"], "confianca": linha["confianca"], "divergencia": linha["divergencia"],
                 "cura": linha["cura"], "ts": linha["ts"], "alternativas": alternativas, "verbetes": verbetes}, len(linhas))

    def ler(self) -> dict:
        with self._trava:
            arq = self._mais_recente()
            if arq is None:
                return {"ha_corrida": False}
            try:
                progresso = json.loads(arq.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                progresso = None
            try:
                idade = max(0.0, time.time() - arq.stat().st_mtime)
            except OSError:
                idade = 0.0
            ultimo, quantos = self._ultimo_diagnostico(arq.parent)
            rodando = idade <= LIMITE_DE_IDADE_S and (progresso is None or progresso.get("estado") in ESTADOS_RODANDO)
            return {"ha_corrida": True, "pasta": arq.parent.name, "progresso": progresso if isinstance(progresso, dict) else None, "idade_s": round(idade, 1),
                    "em_andamento": rodando, "ultimo_diagnostico": ultimo, "diagnosticos": quantos}
