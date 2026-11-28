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
import statistics
import threading
import time
from pathlib import Path

import arvore_de_decisao as ad
import biblioteca_leitura as bl
import etapas_ao_vivo as ea
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


# ! Alteração de IA - Revisar: (25/11/2026, ficha 109, decisão 170) o acervo passa a achar sozinho as corridas lançadas pelo botão do hub: toda
# pasta `hub_<data>_<hora>` de `resultados_alvo/` que já tem trilha entra depois das corridas fixas, com o rótulo "lançada pelo hub em ...".
# A procura é refeita a cada leitura, e `descobrir=False` a desliga.
# ! Motivo: o Eric pediu o hub como central, de onde se rodam os testes; sem isso a corrida lançada da página terminava e os casos dela não
# apareciam na lista sem fechar o hub e abri-lo de novo com `--corridas`. Só o prefixo `hub_` entra, porque é o nome que o próprio servidor dá
# à pasta (`Execucao._nome_da_saida`); as outras pastas de `resultados_alvo/` continuam fora, a menos que sejam pedidas. Uma pasta nova cuja
# trilha ainda está sendo gravada e não dá para ler é pulada naquela leitura, sem derrubar a lista. O resumo do pacote Q6
# (`hub.py --resumo`), a vista "Corrida ao vivo" e os testes das quatro corridas oficiais desligam a procura, para continuarem falando só
# das corridas que nomeiam.
PREFIXO_DO_HUB = "hub_"
_DATA_DO_HUB = re.compile(r"^hub_(\d{4})(\d{2})(\d{2})_(\d{2})(\d{2})\d{2}$")


def rotulo_da_corrida_do_hub(nome: str) -> str:
    """O rótulo de uma corrida lançada pelo botão do hub, com a data e a hora tiradas do nome da pasta."""
    m = _DATA_DO_HUB.match(nome)
    return f"lançada pelo hub em {m[3]}/{m[2]}/{m[1]} às {m[4]}:{m[5]}" if m else f"lançada pelo hub ({nome})"


class Acervo:
    """As corridas que o hub mostra, lidas das pastas em `raiz` (o `resultados_alvo/`); nada é escrito nelas."""

    def __init__(self, raiz: Path, corridas: tuple[str, ...] | None = None, leituras: dict | None = None, calibracao: dict | None = None,
                 limiares: dict | None = None, descobrir: bool = True) -> None:
        self.raiz = Path(raiz)
        padrao = {c["pasta"]: c for c in CORRIDAS_PADRAO}
        nomes = tuple(corridas) if corridas else tuple(padrao)
        self._fixas: list[dict] = []
        self._descobrir = bool(descobrir)
        for nome in nomes:
            if not isinstance(nome, str) or not _NOME_DE_CORRIDA.match(nome):
                raise ValueError(f"corrida: {nome!r} não é nome de pasta de corrida")
            pasta = self.raiz / nome
            if not pasta.is_dir() or self._arquivo_da_trilha(pasta) is None:
                raise ValueError(f"corrida: a pasta {nome!r} não existe em {self.raiz} ou não tem trilha gravada")
            self._fixas.append({"pasta": nome, "rotulo": padrao.get(nome, {}).get("rotulo", nome), "descricao": padrao.get(nome, {}).get("descricao", "")})
        self.leituras = leituras if leituras is not None else bl.carregar()
        self.calibracao = calibracao if calibracao is not None else ad.carregar_calibracao(self.raiz / "fase4" / "calibracao.json")
        self.limiares = limiares if limiares is not None else ad.carregar_limiares(self.raiz / "fase4" / "limiares.json")
        self._cache: dict[str, dict] = {}
        self._trava = threading.RLock()

    def _descobertas(self) -> list[dict]:
        """As corridas lançadas pelo botão do hub que já têm trilha legível, em ordem de nome (que é a ordem de data)."""
        if not self._descobrir:
            return []
        fixas = {c["pasta"] for c in self._fixas}
        try:
            pastas = sorted(p for p in self.raiz.glob(PREFIXO_DO_HUB + "*") if p.is_dir())
        except OSError:
            return []
        achadas = []
        for pasta in pastas:
            if pasta.name in fixas or not _NOME_DE_CORRIDA.match(pasta.name) or self._arquivo_da_trilha(pasta) is None:
                continue
            corrida = {"pasta": pasta.name, "rotulo": rotulo_da_corrida_do_hub(pasta.name), "descricao": "os cenários rodados a partir do botão do hub; não é medida do TCC"}
            try:
                self._carregar(corrida)
            except (OSError, ValueError, KeyError):
                continue            # a corrida está gravando a trilha agora: entra na próxima leitura
            achadas.append(corrida)
        return achadas

    @property
    def _corridas(self) -> list[dict]:
        return self._fixas + self._descobertas()

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
        corridas = self._corridas
        ordem = {c["pasta"]: i for i, c in enumerate(corridas)}
        linhas = [dict(l) for corrida in corridas for l in self._carregar(corrida)["linhas"]]
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

    def processo(self, tid: str) -> dict:
        """A linha de produção de um caso (as seis etapas, as três saídas e a rede), montada dos eventos da trilha dele; ver `processo_do_caso`."""
        with self._trava:
            dado, _ = self._achar(tid)
            c = grr._contexto_v3(dado["eventos"], tid, dado["pasta"] / "blobs", self.leituras)
            return processo_do_caso(c, self.arvore(tid), _registro_do_cenario(dado["pasta"], tid), dado["cab"].get("modelo"), _tempos_das_marcas(dado["pasta"], tid))

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
                    "processo": processo_do_caso(c, arvore, _registro_do_cenario(pasta, tid), cab.get("modelo"), _tempos_das_marcas(pasta, tid)),
                    "comentario_do_agente": {"autor": {"nome": f"agente ({cab.get('modelo')}, biblioteca {cab.get('hash_biblioteca')})", "papel": "agente"},
                                             "veredito": "comentar", "ts": linha["ts"], "texto": comentario},
                    "trace": {"existe": trace is not None, "arquivo": trace.name if trace is not None else None}}


# ! Alteração de IA - Revisar: (26/11/2026, molde visual do hub, ficha 113) `processo_do_caso` monta a linha de produção de um caso para o diagrama
# da página: as seis etapas da figura "Como o agente trabalha" (roda o roteiro, detecta a falha, reduz o que viu, busca na biblioteca, o modelo
# diagnostica, confere e dá um selo), cada uma com o estado, o tempo que a trilha grava, uma frase curta e o detalhe que o cartão ampliado mostra;
# as três saídas (falha de contrato, localizador quebrado, aprendizado); a contagem dos eventos da trilha; a linha do cenário, quando a corrida
# gravou `cenarios.jsonl`; e a rede que liga os sinais do caso, os verbetes pontuados, as causas possíveis e o resultado.
# ! Motivo: o Eric testou o hub e pediu o processo em diagrama, com o tempo de cada etapa e o resultado ao abrir cada cartão, no lugar do texto
# corrido. Tudo sai dos eventos já gravados, sem mudar o agente. A trilha só traz tempo para os passos do roteiro (`acao.tempo_ms`), para a
# inferência (`inferencia.segundos`, com a leitura do caso e a escrita da resposta) e para a cura (`cura.mttr_s`); a detecção, a poda, a busca e a
# conferência saem sem tempo (`tempo_gravado` falso), porque a hora dos eventos é a do bloco em que foram gravados, e não a de cada etapa. Num
# caso em texto não houve roteiro, detecção nem poda, e essas etapas saem como "não se aplica" em vez de inventadas.
ETAPAS_DO_PROCESSO = (("roteiro", "Roda o roteiro", "codigo"), ("deteccao", "Detecta a falha", "codigo"), ("poda", "Reduz o que viu", "codigo"),
                      ("busca", "Busca na biblioteca", "codigo"), ("modelo", "O modelo diagnostica", "modelo"), ("selo", "Confere e dá um selo", "codigo"))
TEMPO_NAO_GRAVADO = ("A trilha grava o tempo dos passos do roteiro, da inferência do modelo e da cura. A detecção, a poda, a busca e a conferência são "
                     "feitas em código e a corrida não cronometra cada uma: elas aparecem sem tempo, sem estimativa no lugar.")
NOS_POR_CAMADA = 6


def _registro_do_cenario(pasta: Path, tid: str) -> dict | None:
    """A linha de `cenarios.jsonl` da execução deste caso (o cenário e a repetição do identificador), ou None."""
    registros = _registros_dos_cenarios(pasta)
    if not registros:
        return None
    cenario, _, repeticao = tid.rsplit("/", 1)[-1].split("@")[0].partition("#")
    numero = int(repeticao) if repeticao.isdigit() else 1
    return next((r for r in registros if r.get("cenario") == cenario and (r.get("repeticao") or 1) == numero), None)


def _medida(valor: dict | None) -> str:
    """`{"nos": 193}` vira "193 nós"; é o tamanho antes e depois da poda, como o evento grava."""
    nomes = {"nos": "nós", "linhas": "linhas", "chars": "caracteres", "itens": "itens", "bytes": "bytes"}
    return ", ".join(f"{v} {nomes.get(k, k)}" for k, v in (valor or {}).items()) or "sem medida"


def _rede_do_caso(arvore: dict, decisao_do_diagnostico: dict | None, cura: dict | None) -> dict:
    por_chave = {d["chave"]: d for d in arvore["decisoes"]}
    d_verbetes, d_causa = por_chave.get("verbetes") or {}, por_chave.get("causa") or {}
    sinais = d_verbetes.get("sinais") or {}
    nos_sinais = [{"id": f"s-{chave}", "rotulo": rotulo, "valor": None, "destaque": False}
                  for chave, rotulo in (("endpoint", sinais.get("endpoint")), ("entidade", sinais.get("entidade")),
                                        ("status", f"status {sinais['status']}" if sinais.get("status") is not None else None),
                                        ("termos", f"{sinais['termos']} termos do caso" if sinais.get("termos") is not None else None)) if rotulo]
    verbetes = [a for a in d_verbetes.get("alternativas") or [] if a.get("opcao")][:NOS_POR_CAMADA]
    teto = max((a.get("pontuacao") or 0 for a in verbetes), default=0) or 1
    nos_verbetes = [{"id": f"v-{a['opcao']}", "rotulo": a["opcao"], "valor": a.get("pontuacao"), "destaque": bool(a.get("escolhida"))} for a in verbetes]
    causas = [a for a in d_causa.get("alternativas") or [] if a.get("opcao")][:NOS_POR_CAMADA]
    nos_causas = [{"id": f"c-{a['opcao']}", "rotulo": a["opcao"], "valor": a.get("probabilidade"), "destaque": bool(a.get("escolhida"))} for a in causas]
    resultado = []
    if d_causa.get("escolha"):
        confianca = (d_causa.get("confianca") or {}).get("palavra")
        resultado.append({"id": "r-causa", "rotulo": d_causa.get("causa_em_palavras") or d_causa["escolha"], "valor": d_causa.get("probabilidade"), "destaque": True,
                          "nota": f"confiança {confianca}" if confianca else None})
    if cura:
        resultado.append({"id": "r-cura", "rotulo": f"curado por {cura.get('escolha')}" if cura.get("curado") else "localizador não curado", "valor": None,
                          "destaque": bool(cura.get("curado")), "nota": None})
    arestas = []
    for v, no in zip(verbetes, nos_verbetes):
        if v.get("escolhida"):
            arestas += [{"de": s["id"], "para": no["id"], "peso": round(min(1.0, max(0.0, (v.get("pontuacao") or 0) / teto)), 3)} for s in nos_sinais]
    ids_dos_verbetes = {n["id"] for n in nos_verbetes}
    sustenta = {a.get("opcao"): a.get("sustentada_por") or [] for a in (decisao_do_diagnostico or {}).get("alternativas") or []}
    for a, no in zip(causas, nos_causas):
        peso = round(min(1.0, max(0.0, a.get("probabilidade") or 0)), 3)
        arestas += [{"de": f"v-{vid}", "para": no["id"], "peso": peso} for vid in sustenta.get(a["opcao"], []) if f"v-{vid}" in ids_dos_verbetes]
        if a.get("escolhida") and resultado and resultado[0]["id"] == "r-causa":
            arestas.append({"de": no["id"], "para": "r-causa", "peso": peso})
    if len(resultado) == 2:
        arestas.append({"de": "r-causa", "para": "r-cura", "peso": 1.0})
    elif resultado and resultado[0]["id"] == "r-cura" and nos_causas:
        arestas.append({"de": nos_causas[0]["id"], "para": "r-cura", "peso": 1.0})
    return {"camadas": [{"id": "sinais", "titulo": "O que o agente viu", "nos": nos_sinais},
                        {"id": "verbetes", "titulo": "Verbetes da biblioteca", "nos": nos_verbetes},
                        {"id": "causas", "titulo": "Causas possíveis", "nos": nos_causas},
                        {"id": "resultado", "titulo": "Resultado", "nos": resultado}], "arestas": arestas}


# ! Alteração de IA - Revisar: (26/11/2026, ficha 114, decisão 176) quando a corrida gravou as marcas da hora de cada etapa (`etapas_ao_vivo.jsonl`, só nas
# corridas lançadas pelo botão do hub), o tempo das seis etapas do caso passa a ser o das marcas (`tempo_de` = "marcas"), e o tempo que a trilha
# grava para o roteiro e para a inferência fica ao lado, em `tempo_pela_trilha_s`. Sem marcas para o caso, tudo continua como antes.
# ! Motivo: a decisão 176 manda gravar a hora de cada etapa só nessas corridas. As duas fontes medem coisas diferentes (a marca do roteiro inclui
# abrir e fechar a página; a trilha soma só os passos), então o cartão mostra uma só, a das marcas, que vale para as seis, e o cartão ampliado diz a outra.
def _tempos_das_marcas(pasta: Path, tid: str) -> dict | None:
    """O tempo de cada etapa deste caso pelas marcas da corrida, ou None quando a corrida não as gravou para ele."""
    return ea.tempos_por_caso(ea.ler(pasta)).get(tid.rsplit("/", 1)[-1])


def processo_do_caso(c: dict, arvore: dict, registro: dict | None = None, modelo: str | None = None, das_marcas: dict | None = None) -> dict:
    seq, por_tipo = c["seq"], c["por_tipo"]
    tipo = "localizador" if c["eh_localizador"] else ("texto" if c["eh_texto"] else "contrato")
    por_chave = {d["chave"]: d for d in arvore["decisoes"]}
    d_causa, d_cura = por_chave.get("causa") or {}, por_chave.get("cura")
    inferencia = next((e for e in seq if e["tipo"] == "inferencia" and e["dados"].get("etapa") in (None, "diagnostico", "diagnóstico")), None)
    seq_da_inferencia = inferencia["seq"] if inferencia else None
    decisao = next((e["dados"] for e in por_tipo.get("decisao", []) if e["dados"].get("decisao") == "diagnostico"), None)
    entrada = c["entrada"] or {}

    def etapa(numero: int, estado: str, tempo_s, resumo: str, detalhe: dict) -> dict:
        ident, titulo, feito_por = ETAPAS_DO_PROCESSO[numero - 1]
        return {"id": ident, "numero": numero, "titulo": titulo, "feito_por": feito_por, "estado": estado, "tempo_s": tempo_s, "tempo_gravado": tempo_s is not None,
                "tempo_de": "trilha" if tempo_s is not None else None, "tempo_pela_trilha_s": None, "resumo": resumo, "detalhe": detalhe}

    # 1. o roteiro: os passos de antes do diagnóstico, com o tempo de cada um, e as chamadas à API que o navegador fez
    acoes = [e["dados"] for e in seq if e["tipo"] == "acao" and not e["dados"].get("reexecucao")]
    chamadas = [{"metodo": d.get("metodo"), "caminho": d.get("caminho"), "status": d.get("status"), "tempo_ms": d.get("tempo_ms")} for d in (e["dados"] for e in por_tipo.get("interceptacao", []))]
    nome_do_roteiro = entrada.get("roteiro") or entrada.get("cenario")
    if acoes:
        tempos = [a["tempo_ms"] for a in acoes if isinstance(a.get("tempo_ms"), (int, float))]
        e1 = etapa(1, "feita", round(sum(tempos) / 1000, 2) if tempos else None,
                   f"{len(acoes)} {'passo' if len(acoes) == 1 else 'passos'}" + (f" do roteiro {nome_do_roteiro}" if nome_do_roteiro else "")
                   + (f"; {len(chamadas)} {'chamada' if len(chamadas) == 1 else 'chamadas'} à API" if chamadas else ""),
                   {"roteiro": nome_do_roteiro, "chamadas": chamadas,
                    "passos": [{"passo": a.get("passo"), "acao": a.get("acao"), "seletor": a.get("seletor") or a.get("url"), "tempo_ms": a.get("tempo_ms"), "falhou": bool(a.get("falhou"))} for a in acoes]})
    else:
        e1 = etapa(1, "nao_se_aplica", None, "caso em texto: não houve roteiro" if tipo == "texto" else "a trilha não tem os passos do roteiro", {"roteiro": nome_do_roteiro, "passos": [], "chamadas": chamadas})

    # 2. a detecção: as conferências do roteiro (de antes da inferência), o passo que falhou ou o que a corrida gravou como motivo
    antes = [e["dados"] for e in por_tipo.get("verificacao", []) if e.get("pai") is None and (seq_da_inferencia is None or e["seq"] < seq_da_inferencia)]
    conferencias = [{"alvo": d.get("alvo"), "regra": d.get("regra"), "resultado": d.get("resultado"), "esperado": (d.get("evidencia") or {}).get("esperado"),
                     "observado": (d.get("evidencia") or {}).get("observado")} for d in antes]
    passo_que_falhou = next((a for a in acoes if a.get("falhou")), None)
    erro = (d_cura or {}).get("erro")
    motivo = (registro or {}).get("motivo_deteccao")
    if motivo or conferencias or passo_que_falhou or erro:
        nao_passaram = [x for x in conferencias if x["resultado"] != "confere"]
        frase = (motivo or (f"o passo {passo_que_falhou.get('passo')} não achou o localizador" if passo_que_falhou
                            else (f"{len(nao_passaram)} de {len(conferencias)} conferências do roteiro não passaram" if nao_passaram else "as conferências do roteiro passaram; a falha veio da resposta da API")))
        e2 = etapa(2, "feita", None, frase, {"origem": (registro or {}).get("origem_deteccao"), "conferencias": conferencias, "erro": erro.split("\n")[0] if erro else None,
                                            "passo": passo_que_falhou.get("passo") if passo_que_falhou else None})
    else:
        e2 = etapa(2, "nao_se_aplica", None, "o caso já chega como falha: esta corrida não registra a detecção", {"origem": None, "conferencias": [], "erro": None, "passo": None})

    # 3. a poda: o tamanho antes e depois, e as regras que tiraram o que não muda
    podas = [e["dados"] for e in por_tipo.get("poda", [])]
    if podas:
        itens = [{"alvo": d.get("alvo"), "antes": d.get("antes"), "depois": d.get("depois"), "antes_em_palavras": _medida(d.get("antes")), "depois_em_palavras": _medida(d.get("depois")),
                  "regras": d.get("regras") or {}} for d in podas]
        e3 = etapa(3, "feita", None, "; ".join(f"{i['alvo']}: {i['antes_em_palavras']} viram {i['depois_em_palavras']}" for i in itens[:2]), {"itens": itens})
    else:
        e3 = etapa(3, "nao_se_aplica", None, "caso em texto: não houve tela para reduzir" if tipo == "texto" else "a trilha não tem a poda deste caso", {"itens": []})

    # 4. a busca: os verbetes pontuados e os k entregues ao modelo
    candidatos = next((e["dados"] for e in por_tipo.get("candidatos", [])), None)
    if candidatos:
        itens = sorted((i for i in candidatos.get("itens") or [] if isinstance(i, dict)), key=lambda i: i.get("posicao") or 10 ** 6)
        entregues = [i["id"] for i in itens if i.get("escolhido")]
        e4 = etapa(4, "feita", None, f"{len(entregues)} de {len(itens)} verbetes entregues ao modelo",
                   {"k": candidatos.get("k"), "pontuados": len(itens), "sinais": candidatos.get("sinais") or {},
                    "verbetes": [{"id": i.get("id"), "pontuacao": i.get("pontuacao"), "entregue": bool(i.get("escolhido"))} for i in itens[:8]]})
    else:
        e4 = etapa(4, "nao_se_aplica", None, "a trilha não tem a busca deste caso", {"k": None, "pontuados": 0, "sinais": {}, "verbetes": []})

    # 5. o modelo: a causa respondida, as alternativas com a probabilidade lida e o tempo da inferência
    alternativas = [{"opcao": a.get("opcao"), "probabilidade": a.get("probabilidade"), "escolhida": bool(a.get("escolhida"))} for a in d_causa.get("alternativas") or []]
    if inferencia:
        i = inferencia["dados"]
        em_segundos = lambda ms: round(ms / 1000, 1) if isinstance(ms, (int, float)) else None
        e5 = etapa(5, "feita", i.get("segundos"), (f"respondeu {d_causa['escolha']}" if d_causa.get("escolha") else "não respondeu uma causa da lista"),
                   {"modelo": modelo, "segundos": i.get("segundos"), "prefill_s": em_segundos(i.get("prefill_ms")), "geracao_s": em_segundos(i.get("geracao_ms")),
                    "tokens_entrada": i.get("tokens_entrada"), "tokens_saida": i.get("tokens_saida"), "causa": d_causa.get("escolha"),
                    "causa_em_palavras": d_causa.get("causa_em_palavras"), "campo": d_causa.get("campo"), "alternativas": alternativas})
    else:
        e5 = etapa(5, "nao_se_aplica", None, "a trilha não tem a inferência deste caso", {"modelo": modelo, "alternativas": alternativas, "causa": d_causa.get("escolha")})

    # 6. a conferência e o selo: o que o código checou do que o modelo disse, e a confiança
    depois = [e["dados"] for e in por_tipo.get("verificacao", []) if seq_da_inferencia is not None and e.get("pai") == seq_da_inferencia]
    confianca = d_causa.get("confianca") or {}
    if depois or confianca.get("palavra"):
        conferem = sum(1 for d in depois if d.get("resultado") == "confere")
        gatilhos = [nome for nome, ligado in (d_causa.get("gatilhos") or {}).items() if ligado and nome != "algum"]
        divergencia = d_causa.get("divergencia")
        e6 = etapa(6, "feita", None, (f"confiança {confianca['palavra']}" if confianca.get("palavra") else "sem selo de confiança") + f"; {conferem} de {len(depois)} conferências passaram",
                   {"confianca": confianca.get("palavra"), "selo": confianca.get("selo"), "probabilidade": confianca.get("p_rotulo"),
                    "conferencias": {"total": len(depois), "conferem": conferem,
                                     "itens": [{"alvo": d.get("alvo"), "regra": d.get("regra"), "resultado": d.get("resultado")} for d in depois[:24]]},
                    "divergencia": bool(divergencia), "detalhe_da_divergencia": (divergencia or {}).get("detalhe") if isinstance(divergencia, dict) else None, "gatilhos": gatilhos})
    else:
        e6 = etapa(6, "nao_se_aplica", None, "a trilha não tem a conferência deste caso", {"confianca": None, "selo": None, "probabilidade": None,
                                                                                         "conferencias": {"total": 0, "conferem": 0, "itens": []}, "divergencia": False, "gatilhos": []})

    # as três saídas da figura
    saida = lambda ident, titulo, estado, resumo, tempo_s=None, detalhe=None: {"id": ident, "titulo": titulo, "estado": estado, "resumo": resumo, "tempo_s": tempo_s, "detalhe": detalhe or {}}
    if tipo != "localizador" and d_causa.get("escolha"):
        s1 = saida("contrato", "Falha de contrato", "saiu", f"relatório para o analista: {d_causa.get('causa_em_palavras') or d_causa['escolha']}",
                   detalhe={"causa": d_causa["escolha"], "causa_em_palavras": d_causa.get("causa_em_palavras"), "campo": d_causa.get("campo"), "confianca": confianca.get("palavra")})
    else:
        s1 = saida("contrato", "Falha de contrato", "nao_se_aplica", "a falha deste caso é da tela, não da API" if tipo == "localizador" else "o modelo não respondeu uma causa")
    if d_cura:
        s2 = saida("localizador", "Localizador quebrado", "saiu", (f"curado por {d_cura.get('escolha')}" if d_cura.get("curado") else "nenhum candidato serviu"), d_cura.get("mttr_s"),
                   {"curado": bool(d_cura.get("curado")), "estrategia": d_cura.get("escolha"), "seletor": d_cura.get("seletor"), "localizador": d_cura.get("localizador"),
                    "reexecucao": d_cura.get("reexecucao"), "candidatos": len(d_cura.get("alternativas") or []), "mttr_s": d_cura.get("mttr_s")})
    else:
        s2 = saida("localizador", "Localizador quebrado", "nao_se_aplica", "não houve localizador a consertar neste caso")
    s3 = saida("aprendizado", "Aprendizado", "nao_se_aplica", "esta corrida não propõe acréscimo à biblioteca")
    cenario = ({k: registro.get(k) for k in ("segundos", "segundos_diagnostico", "mttr_s", "task_success", "detectou", "origem_deteccao")} if registro else None)
    etapas = [e1, e2, e3, e4, e5, e6]
    for e in etapas:            # as marcas da corrida, quando existem para este caso (decisão 176)
        if das_marcas and isinstance(das_marcas.get(e["id"]), (int, float)):
            e.update({"tempo_pela_trilha_s": e["tempo_s"], "tempo_s": das_marcas[e["id"]], "tempo_gravado": True, "tempo_de": "marcas"})
    falta_tempo = any(e["estado"] == "feita" and not e["tempo_gravado"] for e in etapas)
    return {"tipo": tipo, "etapas": etapas, "saidas": [s1, s2, s3], "trilha": {"eventos": len(seq), "hash": arvore["eventos"]["hash"]},
            "cenario": cenario, "tempo_nao_gravado": TEMPO_NAO_GRAVADO if falta_tempo else None, "rede": _rede_do_caso(arvore, decisao, d_cura)}


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


# ! Alteração de IA - Revisar: (27/11/2026, coletânea da banca, decisões 194 a 196) `coletanea_da_corrida` lê a rodada da coletânea de uma pasta de
# corrida (o `sorteio.json` que o executor grava antes do primeiro erro e o `cenarios.jsonl`) e monta o que a vista "Corrida ao vivo" mostra: o
# número, de onde veio, a posição na pilha e quantas cartas faltam; um cartão por carta, escondido até a resposta, e depois com o que foi ligado,
# a causa e o campo certos, o que o agente disse e se acertou; a grade das 64 cartas por grupo, com as reveladas e as das rodadas anteriores do
# mesmo número acesas; a lista e o comando que refaz o sorteio, só no fim; e a conferência do mesmo agente da medida (os códigos do prompt fixo
# e da biblioteca contra os da corrida 28b).
# ! Motivo: a banca tem de comparar a resposta com o erro na hora, sem ver o erro antes. Por isso nada da carta escondida sai daqui: o cartão só
# tem a posição, e o quadrado apagado da grade não leva o nome (um quadrado apagado tanto pode ser carta escondida quanto carta não tirada). A
# carta se revela quando a linha dela entra no `cenarios.jsonl`, o que o executor faz só depois do diagnóstico e da cura.
CORRIDA_DA_MEDIDA = "fase5_agente_b"


def _ler_json(arq: Path):
    try:
        return json.loads(Path(arq).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def _veredito_da_carta(carta: dict, registro: dict) -> str:
    if carta["tipo"] == "sem_erro":
        return "errado: acusou falha onde não havia" if registro.get("detectou") else "certo: nada foi acusado"
    if not registro.get("detectou"):
        return "não detectou"
    return "acertou" if registro.get("task_success") else "errou"


def _mesmo_agente(pasta: Path) -> dict | None:
    esta, medida = _ler_json(pasta / "condicoes_fase4.json"), _ler_json(pasta.parent / CORRIDA_DA_MEDIDA / "condicoes_fase4.json")
    if not isinstance(esta, dict) or not isinstance(medida, dict):
        return None
    biblioteca = lambda c: (c.get("biblioteca") or {}).get("hash") if isinstance(c.get("biblioteca"), dict) else None
    return {"prompt_fixo": bool(esta.get("hash_prompt_fixo")) and esta.get("hash_prompt_fixo") == medida.get("hash_prompt_fixo"),
            "biblioteca": bool(biblioteca(esta)) and biblioteca(esta) == biblioteca(medida), "referencia": CORRIDA_DA_MEDIDA}


def coletanea_da_corrida(pasta: Path, registro: Path) -> dict | None:
    """A rodada da coletânea gravada nesta pasta, pronta para a página; None quando a pasta não é de uma rodada da coletânea."""
    import coletanea as cl
    pasta = Path(pasta)
    s = _ler_json(pasta / cl.ARQUIVO_DO_SORTEIO)
    if not isinstance(s, dict) or not s.get("cartas"):
        return None
    respondidas = {r.get("cenario"): r for r in (_registros_dos_cenarios(pasta) or [])}
    nome_do_grupo = {g["classe"]: g["nome"] for g in cl.GRUPOS}
    rodada, reveladas = [], set()
    for i, id_ in enumerate(s["cartas"]):
        posicao = s["posicao"] + i + 1
        base = {"posicao": posicao, "nome": f"carta-{posicao:02d}"}
        r = respondidas.get(id_)
        try:
            c = cl.carta(id_)
        except KeyError:
            c = None
        if r is None or c is None:
            rodada.append({**base, "revelada": False})
            continue
        reveladas.add(id_)
        rodada.append({**base, "revelada": True, "id": id_, "tipo": c["tipo"], "grupo": nome_do_grupo.get(c["classe"]), "o_que_foi_ligado": cl.descricao(c),
                       "causa_certa": c["causa"], "campo_certo": c["campo"], "medido_na_fase_5": c["medido_na_fase_5"], "veredito": _veredito_da_carta(c, r),
                       "agente": {"detectou": bool(r.get("detectou")), "rotulo": r.get("rotulo"), "campo": (r.get("conferencia") or {}).get("campo"),
                                  "curado": (r.get("cura") or {}).get("curado") if c["tipo"] == "localizador" else None, "mttr_s": r.get("mttr_s")}})
    antes = {id_ for x in cl.sorteios_do_numero(s["numero"], registro, s.get("codigo_da_coletanea")) if x.get("posicao", 0) < s["posicao"] for id_ in x.get("cartas") or []}
    grade = []
    for g in cl.GRUPOS:
        quadrados = []
        for c in cl.cartas():
            if c["classe"] != g["classe"]:
                continue
            marca = "revelada" if c["id"] in reveladas else "antes" if c["id"] in antes else ""
            quadrados.append({"marca": marca, "id": c["id"] if marca else None, "descricao": cl.descricao(c) if marca else None})
        grade.append({"classe": g["classe"], "nome": g["nome"], "pergunta": g["pergunta"], "cartas": quadrados})
    fim = len(reveladas) == len(s["cartas"])
    return {"corrida": pasta.name, "quando": s.get("quando"), "numero": s["numero"], "origem": s.get("origem"), "de": s["posicao"] + 1, "ate": s["proxima"],
            "total": s["total"], "faltam": s["total"] - s["proxima"], "quantas": s.get("quantas"), "cartas_da_rodada": rodada, "grade": grade,
            "lista": list(s["cartas"]) if fim else None, "comando": s.get("comando") if fim else None, "mesmo_agente": _mesmo_agente(pasta)}


class AoVivo:
    """A corrida que gravou o estado da barra por último, lida da pasta dela; nada é escrito."""

    def __init__(self, raiz: Path, leituras: dict | None = None, calibracao: dict | None = None, limiares: dict | None = None) -> None:
        self.raiz = Path(raiz)
        self.leituras, self.calibracao, self.limiares = leituras, calibracao, limiares
        self._acervos: dict[str, Acervo] = {}
        self._trava = threading.Lock()

    def _mais_recente(self) -> Path | None:
        candidatos = []
        for padrao in ("*/progresso.json", "*/" + ea.NOME_DO_ARQUIVO):      # o estado da barra de progresso e as marcas das etapas (decisão 176)
            for arq in self.raiz.glob(padrao):
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
                self._acervos[nome] = Acervo(self.raiz, corridas=(nome,), leituras=self.leituras, calibracao=self.calibracao, limiares=self.limiares, descobrir=False)
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
        try:        # a linha de produção do último caso diagnosticado, para o diagrama da vista ao vivo (molde visual, ficha 113)
            processo = acervo.processo(linha["tid"])
        except (OSError, ValueError, KeyError):
            processo = None
        return ({"tid": linha["tid"], "caso": linha["caso"], "nome": linha["nome"], "titulo": linha["titulo"], "escolha": linha["escolha"],
                 "causa_em_palavras": linha["causa_em_palavras"], "campo": linha["campo"], "confianca": linha["confianca"], "divergencia": linha["divergencia"],
                 "cura": linha["cura"], "ts": linha["ts"], "alternativas": alternativas, "verbetes": verbetes, "processo": processo}, len(linhas))

    # ! Alteração de IA - Revisar: (26/11/2026, ficha 114, decisão 176) a leitura ao vivo passa a usar também as marcas da hora de cada etapa, quando a
    # corrida as grava: a etapa acesa (`etapa_agora`) é a da última marca, se ela tem menos de meio minuto e o caso não terminou, ou a do modelo,
    # enquanto a barra de progresso diz que a inferência está rodando; `tempos_agora` traz o tempo das etapas que o caso em andamento já passou.
    # ! Motivo: sem as marcas, a corrida só regrava o estado durante a inferência, e só a etapa do modelo podia aparecer acesa (ver o molde visual,
    # ficha 113). Durante a inferência a marca do modelo fica parada por mais de meio minuto, e é a barra que diz que a corrida está viva; fora
    # dela, uma marca parada há mais de meio minuto quer dizer que a corrida parou ou morreu, e nada fica aceso.
    def ler(self) -> dict:
        with self._trava:
            arq = self._mais_recente()
            if arq is None:
                return {"ha_corrida": False}
            pasta, agora = arq.parent, time.time()
            arq_da_barra = pasta / "progresso.json"
            try:
                progresso = json.loads(arq_da_barra.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                progresso = None
            try:
                idade = max(0.0, agora - arq_da_barra.stat().st_mtime)
                rodando = idade <= LIMITE_DE_IDADE_S and (progresso is None or progresso.get("estado") in ESTADOS_RODANDO)
            except OSError:
                idade, rodando = None, False
            marcas = ea.ler(pasta)
            try:
                idade_das_marcas = max(0.0, agora - (pasta / ea.NOME_DO_ARQUIVO).stat().st_mtime)
            except OSError:
                idade_das_marcas = None
            ultima = marcas[-1] if marcas else None
            pela_marca = bool(ultima and ultima["etapa"] != "fim" and idade_das_marcas is not None and idade_das_marcas <= LIMITE_DE_IDADE_S)
            no_modelo = bool(rodando and isinstance(progresso, dict) and progresso.get("estado") in ESTADOS_RODANDO)
            etapa_agora = caso_agora = None
            if no_modelo:
                etapa_agora = "modelo"
                caso_agora = ultima.get("caso") if ultima and ultima["etapa"] == "modelo" else (str(progresso.get("etapa") or "").split(" · ")[0] or None)
            elif pela_marca:
                etapa_agora, caso_agora = ultima["etapa"], ultima.get("caso")
            ultimo, quantos = self._ultimo_diagnostico(pasta)
            # ! Alteração de IA - Revisar: (27/11/2026, coletânea da banca) a leitura ao vivo traz também a rodada da coletânea, quando a corrida é uma.
            # ! Motivo: a vista "Corrida ao vivo" mostra a pilha, a grade e o cartão de cada carta; nas outras corridas a chave vem vazia (None).
            coletanea = coletanea_da_corrida(pasta, self.raiz / "hub" / "sorteios.jsonl")
            return {"ha_corrida": True, "pasta": pasta.name, "progresso": progresso if isinstance(progresso, dict) else None, "coletanea": coletanea,
                    "idade_s": round(idade if idade is not None else (idade_das_marcas or 0.0), 1), "em_andamento": bool(rodando or pela_marca),
                    "etapa_agora": etapa_agora, "caso_agora": caso_agora,
                    "tempos_agora": ea.tempos_por_caso(marcas).get(str(caso_agora), {}) if caso_agora is not None else {},
                    "ultimo_diagnostico": ultimo, "diagnosticos": quantos}



# ! Alteração de IA - Revisar: (25/11/2026, ficha 109, decisão 170) `metricas` monta o que a vista "Métricas" do hub mostra. Por corrida do
# acervo: quantos casos têm diagnóstico e a confiança deles (da trilha) e, quando a corrida rodou cenários, quantas execuções, em quantas o
# agente chegou ao resultado (Task Success), em quantas a falha foi detectada e o tempo médio de reparo, tudo lido do `cenarios.jsonl` da
# pasta. No alto, o resultado da Fase 5 (o agente contra as pessoas), com as frases e as contagens copiadas de `fase5/medicao.json` e a
# ressalva do Task Success.
# ! Motivo: o Eric pediu que do hub se vejam as métricas. Nenhum número é digitado: tudo sai dos registros gravados, a cada pedido. O tempo de
# reparo é a média dos cenários (primeiro a média das execuções de cada cenário, depois a média entre os cenários), a mesma conta da leitura da
# Fase 5; a média simples das execuções da corrida 28b daria 66,0 s ao lado dos 66,3 s que o TCC cita. `vale_como_medida` separa as corridas
# que são leitura do TCC (as quatro que o hub abre por padrão) das lançadas pelo botão do hub, que são uso do produto e não medida; de uma
# pasta pedida por `--corridas` o hub não sabe dizer, e devolve None. A ressalva só aparece quando o próprio `medicao.json` traz a conta sem a
# sessão de um integrante e ela muda o veredito do Task Success (decisão 151); o texto não cita número nem nome.
def _registros_dos_cenarios(pasta: Path) -> list[dict] | None:
    """As linhas de `cenarios.jsonl` de uma corrida; None quando ela não rodou cenários. Uma linha pela metade (corrida gravando) é pulada."""
    try:
        linhas = (pasta / "cenarios.jsonl").read_text(encoding="utf-8").splitlines()
    except OSError:
        return None
    registros = []
    for linha in linhas:
        try:
            registro = json.loads(linha) if linha.strip() else None
        except ValueError:
            continue
        if isinstance(registro, dict):
            registros.append(registro)
    return registros


def _tempo(registro: dict) -> float | None:
    valor = registro.get("mttr_s")
    return float(valor) if isinstance(valor, (int, float)) and not isinstance(valor, bool) else None


def _metricas_dos_cenarios(registros: list[dict]) -> dict:
    por_cenario: dict[str, list[dict]] = {}
    for r in registros:
        por_cenario.setdefault(str(r.get("cenario")), []).append(r)
    linhas, medias = [], []
    for nome, grupo in por_cenario.items():
        tempos = [t for t in (_tempo(r) for r in grupo) if t is not None]
        media = statistics.fmean(tempos) if tempos else None
        if media is not None:
            medias.append(media)
        linhas.append({"cenario": nome, "tipo": grupo[0].get("tipo"), "execucoes": len(grupo), "task_success": sum(1 for r in grupo if r.get("task_success") is True),
                       "detectou": sum(1 for r in grupo if r.get("detectou") is True), "mttr_media_s": round(media, 1) if media is not None else None})
    return {"execucoes": len(registros), "task_success": sum(1 for r in registros if r.get("task_success") is True),
            "detectou": sum(1 for r in registros if r.get("detectou") is True), "mttr_media_s": round(statistics.fmean(medias), 1) if medias else None,
            "cenarios_com_tempo": len(medias), "por_cenario": linhas}


def _resultado_da_fase_5(raiz: Path) -> dict | None:
    """As frases e as contagens da comparação do agente com as pessoas, copiadas de `fase5/medicao.json`; None se a leitura não existe ou não está completa."""
    try:
        medicao = json.loads((raiz / "fase5" / "medicao.json").read_text(encoding="utf-8"))
        tempo, sucesso = medicao["tempo"]["geral"]["frase"], medicao["task_success"]
        lados = {lado: {"sucessos": sucesso[lado]["sucessos"], "n": sucesso[lado]["n"]} for lado in ("agente", "pessoas")}
    except (OSError, ValueError, KeyError, TypeError):
        return None
    conta = medicao.get("sem_um_integrante")
    mudam = [x for x in conta if isinstance(x, dict) and (x.get("task_success") or {}).get("o_que_a_regra_l11_daria") not in (None, "veredito")] if isinstance(conta, list) else []
    ressalva = None
    if sucesso.get("caso") == "veredito" and mudam:
        quem = "de um integrante só" if len(mudam) == 1 else "de mais de um integrante"
        ressalva = (f"Esse veredito depende da sessão {quem}: sem ela, numa conta feita depois de ver os números e fora das regras fixadas antes, o Task Success "
                    "fica sem veredito, e o resultado do tempo continua o mesmo (decisão 151).")
    def tempo_medio(lado: str) -> float | None:
        valor = (((medicao.get("lados") or {}).get(lado) or {}).get("geral") or {}).get("tempo_media_s")
        return round(float(valor), 1) if isinstance(valor, (int, float)) and not isinstance(valor, bool) else None

    return {"tempo": tempo, "task_success": sucesso.get("frase"), **lados, "ressalva": ressalva, "tempo_medio_s": {"agente": tempo_medio("agente"), "pessoas": tempo_medio("pessoas")},
            "corrida": (medicao.get("metadados") or {}).get("corrida")}


def metricas(acervo: Acervo) -> dict:
    """O que a vista "Métricas" mostra: o resultado da Fase 5 no alto e uma linha por corrida do acervo, tudo lido dos arquivos gravados."""
    oficiais = {c["pasta"] for c in CORRIDAS_PADRAO}
    por_corrida: dict[str, list[dict]] = {}
    for linha in acervo.indice():
        por_corrida.setdefault(linha["corrida"], []).append(linha)
    corridas = []
    for corrida in acervo.corridas():
        pasta = corrida["pasta"]
        registros = _registros_dos_cenarios(acervo.raiz / pasta)
        dos_cenarios = _metricas_dos_cenarios(registros) if registros else {"execucoes": None, "task_success": None, "detectou": None, "mttr_media_s": None,
                                                                             "cenarios_com_tempo": 0, "por_cenario": []}
        contagem: dict[str, int] = {}
        for linha in por_corrida.get(pasta, []):
            contagem[linha["confianca"]] = contagem.get(linha["confianca"], 0) + 1
        ordem = [*ad.CONFIANCA_EM_PALAVRAS.values(), *sorted(set(contagem) - set(ad.CONFIANCA_EM_PALAVRAS.values()))]     # alta, média, baixa e o que mais houver
        confianca = {nome: contagem[nome] for nome in ordem if nome in contagem}
        corridas.append({"pasta": pasta, "rotulo": corrida["rotulo"], "descricao": corrida["descricao"], "inicio": corrida.get("inicio"), "casos": corrida["casos"],
                         "confianca": confianca, **dos_cenarios,
                         "vale_como_medida": True if pasta in oficiais else (False if pasta.startswith(PREFIXO_DO_HUB) else None)})
    return {"fase5": _resultado_da_fase_5(acervo.raiz), "corridas": corridas}
