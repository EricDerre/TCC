#!/usr/bin/env python3
# ! Alteração de IA - Revisar: arquivo novo (25/11/2026, Pós-Fase 4, pacote Q6): o servidor do hub central. Sobe o `http.server` da biblioteca
# padrão só em 127.0.0.1 e atende seis endereços: a página (`/`), o estilo (`/hub.css`), o programa (`/hub.js`), a lista (`/api/indice`), o
# caso (`/api/caso?tid=...`) e a gravação da revisão (`POST /api/revisao`). `Hub` junta o acervo das corridas (`hub_dados.Acervo`) com as
# revisões (`hub_revisao.Revisoes`); `--conferir` monta todos os casos sem subir servidor e diz quantos são.
# ! Motivo: plano aprovado da Pós-Fase 4, seção 3.6 ("uma aplicação local, servida por http.server da biblioteca padrão"), e ficha 97 (decisão
# 157). O servidor grava em disco, então ele: só escuta na própria máquina; não serve arquivo nenhum do disco (cada endereço é uma função, e o
# que não é um dos seis recebe 404); só aceita gravação em JSON vinda do próprio endereço (um formulário de outro site aberto no mesmo
# navegador não consegue mandar `application/json` sem pedir licença, e o cabeçalho de origem é conferido); grava tudo como analista (o agente
# não escreve pela página) e põe ele mesmo a iteração do caso no evento, para o navegador não poder dizer que revisou outra.
"""O hub central (Pós-Fase 4, pacote Q6). Uso (em Programacao/AgenteCore/experimentos):
  python hub.py                       # sobe em http://127.0.0.1:8765 com as corridas 18d, 21d, 24 e 28b e abre o navegador
  python hub.py --porta 8770 --sem-abrir
  python hub.py --corridas fase5_agente_b,fase4_ineditos
  python hub.py --conferir            # monta todos os casos sem subir servidor e diz quantos são
As revisões ficam em resultados_alvo/hub/revisoes/<caso>.jsonl. Nada é escrito nas pastas das corridas.
"""
from __future__ import annotations

import argparse
import contextlib
import json
import sys
import urllib.parse
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import gerar_relatorio_raciocinio as grr
import hub_dados as hd
import hub_pagina as hp
import hub_revisao as hr

EXP = Path(__file__).resolve().parent
RESULTADOS = EXP / "resultados_alvo"
PASTA_DAS_REVISOES = RESULTADOS / "hub" / "revisoes"
PORTA_PADRAO = 8765
ENDERECO = "127.0.0.1"
NOMES_LOCAIS = ("127.0.0.1", "localhost")
LIMITE_DO_CORPO = 1_000_000
POLITICA = "default-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'; form-action 'none'"
BLOCOS_DO_RELATORIO = tuple(f"b{n}-{hp.slug(nome)}" for n, nome in enumerate(grr.CAMPOS_55 + grr.SECOES_MANTIDAS_V3, start=1))
CAMPOS_DO_RASCUNHO = ("texto", "ancora", "rotulo", "bloqueante", "conversa")


class Recusa(Exception):
    """Um pedido que o servidor recusa, com o código HTTP da resposta."""

    def __init__(self, codigo: int, mensagem: str) -> None:
        super().__init__(mensagem)
        self.codigo = codigo


def opcoes() -> dict:
    """As listas fechadas que a página mostra nos seletores, lidas de `hub_revisao` (nenhuma é digitada na página)."""
    pares = lambda d: [[k, v] for k, v in d.items()]  # noqa: E731
    return {"vereditos": pares(hr.VEREDITOS), "estados_da_conversa": pares(hr.ESTADOS_DA_CONVERSA), "severidades": list(hr.SEVERIDADES),
            "prioridades": list(hr.PRIORIDADES), "estados_55": list(hr.ESTADOS_55), "rotulos": pares(hr.ROTULOS), "desfechos": pares(hr.DESFECHOS),
            "causas": list(hr.CAUSAS)}


class Hub:
    """O que o servidor responde: o acervo das corridas e as revisões, juntos."""

    def __init__(self, acervo: hd.Acervo, revisoes: hr.Revisoes) -> None:
        self.acervo = acervo
        self.revisoes = revisoes

    def _iteracoes(self, caso: str) -> list[dict]:
        return [{"tid": i["tid"], "hash": i["hash"], "numero": i["numero"]} for i in self.acervo.iteracoes(caso)]

    def _resumo(self, estado: dict) -> dict:
        v = estado["veredito_atual"]
        return {"veredito": v["veredito"] if v else None, "veredito_rotulo": hr.VEREDITOS[v["veredito"]] if v else None,
                "vale_para_a_iteracao_atual": estado["veredito_vale_para_a_iteracao_atual"], "ativas": estado["contagem"]["ativas"],
                "conversas": estado["contagem"]["conversas"], "estado_55": estado["campos_55"]["estado"]}

    def _desta_iteracao(self, estado: dict, tid: str, hash_: str) -> dict:
        lido = estado["lido"]
        return {"lida": bool(lido and lido["tid"] == tid and lido["hash"] == hash_)}

    def indice(self) -> dict:
        casos = self.acervo.indice()
        resumos: dict[str, dict] = {}
        for linha in casos:
            if linha["caso"] not in resumos:
                resumos[linha["caso"]] = self._resumo(hr.estado(self.revisoes.eventos(linha["caso"]), self._iteracoes(linha["caso"])))
            linha["revisao"] = resumos[linha["caso"]]
        return {"corridas": self.acervo.corridas(), "casos": casos, "opcoes": opcoes()}

    def caso(self, tid: str) -> dict:
        """O caso do acervo mais a revisão dele e o que mudou desde a última iteração que o analista leu ou julgou (ou desde a anterior)."""
        caso = self.acervo.caso(tid)
        eventos = self.revisoes.eventos(caso["caso"])
        estado = hr.estado(eventos, self._iteracoes(caso["caso"]))
        vistas = {e["iteracao"]["tid"] for e in eventos if e["tipo"] == "lido" or (e["tipo"] == "veredito" and e["autor"]["papel"] == "analista")}
        anteriores = [i for i in caso["iteracoes"] if i["numero"] < caso["iteracao"]]
        ja_vistas = [i for i in anteriores if i["tid"] in vistas]
        referencia = (ja_vistas or anteriores or [None])[-1]
        caso["mudancas"] = {"de": referencia["numero"] if referencia else None, "motivo": "a última que você leu ou julgou" if ja_vistas else "a anterior",
                            "itens": self.acervo.mudancas(referencia["tid"], tid) if referencia else []}
        caso["arvore_html"] = hp.arvore_para_html(caso["arvore"])
        caso["revisao"] = estado
        caso["revisao_desta_iteracao"] = self._desta_iteracao(estado, tid, caso["hash"])
        return caso

    def revisar(self, pedido: dict) -> dict:
        """Grava uma ação do analista. O autor é sempre o analista e a iteração é a da trilha pedida, as duas postas aqui."""
        if not isinstance(pedido, dict):
            raise ValueError("pedido: esperava um objeto")
        it = self.acervo.iteracao(pedido.get("tid"))          # KeyError se a trilha não está no hub
        caso, iteracao = it["caso"], {"tid": it["tid"], "hash": it["hash"], "numero": it["numero"]}
        nome = (pedido.get("autor") or {}).get("nome") if isinstance(pedido.get("autor"), dict) else None
        autor = {"nome": nome, "papel": "analista"}
        comum = {"autor": autor, "iteracao": iteracao}
        acao = pedido.get("acao")

        def conferir_bloco(ancora) -> None:
            if isinstance(ancora, dict) and ancora.get("bloco") not in BLOCOS_DO_RELATORIO:
                raise ValueError(f"ancora.bloco: {ancora.get('bloco')!r} não é um bloco do relatório")

        if acao == "comentar":
            conferir_bloco(pedido.get("ancora"))
            self.revisoes.registrar(caso, {"tipo": "comentario", **comum, **{k: pedido.get(k) for k in CAMPOS_DO_RASCUNHO}})
        elif acao == "estado_da_conversa":
            self.revisoes.registrar(caso, {"tipo": "estado_da_conversa", **comum, "conversa": pedido.get("conversa"), "estado": pedido.get("estado")})
        elif acao == "lido":
            self.revisoes.registrar(caso, {"tipo": "lido", **comum})
        elif acao == "campos_55":
            self.revisoes.registrar(caso, {"tipo": "campos_55", **comum, **{k: pedido[k] for k in ("severidade", "prioridade", "estado") if k in pedido}})
        elif acao == "causa_sugerida":
            self.revisoes.registrar(caso, {"tipo": "causa_sugerida", **comum, **{k: pedido.get(k) for k in ("causa", "campo", "texto")}})
        elif acao == "enviar_revisao":
            rascunhos = pedido.get("rascunhos") or []
            if not isinstance(rascunhos, list) or not all(isinstance(r, dict) for r in rascunhos):
                raise ValueError("rascunhos: esperava uma lista de comentários")
            for r in rascunhos:
                conferir_bloco(r.get("ancora"))
            for chave in ("campos_55", "causa_sugerida"):
                if pedido.get(chave) is not None and not isinstance(pedido[chave], dict):
                    raise ValueError(f"{chave}: esperava um objeto")
            self.revisoes.enviar_revisao(caso, autor=autor, iteracao=iteracao, veredito=pedido.get("veredito"), resumo=pedido.get("resumo") or "",
                                         desfecho=pedido.get("desfecho"), rascunhos=[{k: r.get(k) for k in CAMPOS_DO_RASCUNHO} for r in rascunhos],
                                         campos_55=pedido.get("campos_55"), causa_sugerida=pedido.get("causa_sugerida"))
        else:
            raise ValueError(f"acao: {acao!r} não é uma ação do hub")
        estado = hr.estado(self.revisoes.eventos(caso), self._iteracoes(caso))
        return {"ok": True, "revisao": estado, "revisao_desta_iteracao": self._desta_iteracao(estado, it["tid"], it["hash"]), "resumo": self._resumo(estado)}


def _tratador(hub: Hub, falar: bool):
    class Tratador(BaseHTTPRequestHandler):
        server_version = "HubDoAgente/1"
        protocol_version = "HTTP/1.1"

        def log_message(self, formato, *args) -> None:
            if falar:
                super().log_message(formato, *args)

        def _responder(self, codigo: int, corpo: bytes, tipo: str) -> None:
            self.send_response(codigo)
            self.send_header("Content-Type", tipo)
            self.send_header("Content-Length", str(len(corpo)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Referrer-Policy", "no-referrer")
            self.send_header("Content-Security-Policy", POLITICA)
            self.end_headers()
            self.wfile.write(corpo)

        def _json(self, codigo: int, dado) -> None:
            self._responder(codigo, json.dumps(dado, ensure_ascii=False).encode("utf-8"), "application/json; charset=utf-8")

        def _atender(self, funcao) -> None:
            """Roda a função do endereço e traduz a recusa em código HTTP: 404 para o que não existe no hub, 400 para o que não passa na validação."""
            try:
                funcao()
            except Recusa as e:
                self._json(e.codigo, {"erro": str(e)})
            except KeyError as e:
                self._json(404, {"erro": str(e.args[0]) if e.args else "não encontrado"})
            except ValueError as e:
                self._json(400, {"erro": str(e)})

        def _da_propria_pagina(self) -> None:
            """Recusa o pedido de gravação que não veio da página do próprio hub: nome de endereço que não é o desta máquina, ou origem de outro site."""
            porta = self.server.server_address[1]
            nome = (self.headers.get("Host") or "").rsplit(":", 1)[0].strip("[]").lower()
            if nome not in NOMES_LOCAIS:
                raise Recusa(403, "o hub só atende pelo endereço desta máquina")
            origem = self.headers.get("Origin")
            if origem is not None and origem not in {f"http://{n}:{porta}" for n in NOMES_LOCAIS}:
                raise Recusa(403, "o pedido veio de outra página, não da página do hub")

        # ! Alteração de IA - Revisar: (25/11/2026, etapa 2) o corpo do pedido é lido inteiro antes de qualquer recusa, e só depois vêm as
        # conferências (endereço, origem, tipo de conteúdo, JSON); os outros verbos (PUT, DELETE, PATCH) também leem o corpo e respondem 405.
        # ! Motivo: na primeira rodada dos testes o servidor recusava (403, 415, 404) sem ler o corpo; como a conexão fica aberta para o pedido
        # seguinte, o resto do corpo era lido como se fosse um pedido novo, e o servidor imprimia "Bad request version" seguido de
        # "ConnectionAbortedError: [WinError 10053]". Lendo antes, não sobra pedaço na conexão. Acima do limite o corpo é esvaziado sem ser
        # guardado, até um teto, e a conexão é fechada.
        def _ler_corpo(self) -> bytes:
            try:
                tamanho = int(self.headers.get("Content-Length") or "")
            except ValueError:
                self.close_connection = True
                raise Recusa(411, "faltou o tamanho do pedido") from None
            if tamanho > LIMITE_DO_CORPO:
                restante = min(tamanho, 20 * LIMITE_DO_CORPO)
                while restante > 0:
                    lido = self.rfile.read(min(65536, restante))
                    if not lido:
                        break
                    restante -= len(lido)
                self.close_connection = True
                raise Recusa(413, f"o pedido passa de {LIMITE_DO_CORPO} bytes")
            return self.rfile.read(tamanho)

        def _corpo_json(self, bruto: bytes) -> dict:
            if not (self.headers.get("Content-Type") or "").lower().startswith("application/json"):
                raise Recusa(415, "o hub só aceita gravação em JSON")
            try:
                return json.loads(bruto.decode("utf-8"))
            except ValueError:      # inclui UnicodeDecodeError
                raise Recusa(400, "o pedido não é JSON válido") from None

        def _verbo_que_o_hub_nao_tem(self) -> None:
            def rota() -> None:
                self._ler_corpo()
                raise Recusa(405, "o hub só atende GET e POST")

            self._atender(rota)

        do_PUT = do_DELETE = do_PATCH = _verbo_que_o_hub_nao_tem  # noqa: N815 - nomes fixados por http.server

        def do_GET(self) -> None:  # noqa: N802 - nome fixado por http.server
            partes = urllib.parse.urlsplit(self.path)
            consulta = urllib.parse.parse_qs(partes.query)

            def rota() -> None:
                if partes.path == "/":
                    self._responder(200, hp.pagina().encode("utf-8"), "text/html; charset=utf-8")
                elif partes.path == "/hub.css":
                    self._responder(200, hp.CSS.encode("utf-8"), "text/css; charset=utf-8")
                elif partes.path == "/hub.js":
                    self._responder(200, hp.JS.encode("utf-8"), "text/javascript; charset=utf-8")
                elif partes.path == "/api/indice":
                    self._json(200, hub.indice())
                elif partes.path == "/api/caso":
                    self._json(200, hub.caso((consulta.get("tid") or [""])[0]))
                else:
                    raise Recusa(404, "endereço que o hub não tem")

            self._atender(rota)

        def do_POST(self) -> None:  # noqa: N802 - nome fixado por http.server
            partes = urllib.parse.urlsplit(self.path)

            def rota() -> None:
                bruto = self._ler_corpo()
                if partes.path != "/api/revisao":
                    raise Recusa(404, "endereço que o hub não tem")
                self._da_propria_pagina()
                self._json(200, hub.revisar(self._corpo_json(bruto)))

            self._atender(rota)

    return Tratador


class Servidor(ThreadingHTTPServer):
    """O servidor do hub: um fio por pedido, e sem rastro no terminal quando o navegador fecha a conexão no meio de uma resposta."""
    daemon_threads = True

    def handle_error(self, request, client_address) -> None:
        if isinstance(sys.exc_info()[1], ConnectionError):
            return
        super().handle_error(request, client_address)


def criar_servidor(acervo: hd.Acervo, revisoes: hr.Revisoes, porta: int = PORTA_PADRAO, endereco: str = ENDERECO, falar: bool = False) -> ThreadingHTTPServer:
    """O servidor do hub, pronto para `serve_forever()`; `porta=0` pede uma porta livre ao sistema. Só aceita escutar na própria máquina."""
    if endereco != ENDERECO:
        raise ValueError(f"o hub só escuta em {ENDERECO}: ele grava em disco e não tem senha")
    return Servidor((endereco, porta), _tratador(Hub(acervo, revisoes), falar))


def conferir(acervo: hd.Acervo) -> int:
    """Monta todos os casos do acervo, como a página pediria, e diz quantos são por corrida; sai com 1 se algum não montar."""
    indice = acervo.indice()
    falhas = []
    for linha in indice:
        try:
            caso = acervo.caso(linha["tid"])
            hp.arvore_para_html(caso["arvore"])
        except Exception as e:  # noqa: BLE001 - a conferência relata qualquer caso que não monte, em vez de parar no primeiro
            falhas.append(f"{linha['tid']}: {type(e).__name__}: {e}")
    for c in acervo.corridas():
        print(f"{c['rotulo']} ({c['pasta']}): {c['casos']} casos, trilha {c['trilha']}")
    print(f"{len(indice)} casos em {len(acervo.corridas())} corridas; {len({l['caso'] for l in indice})} casos distintos (as iterações do mesmo caso contam uma vez)")
    for f in falhas:
        print("!! " + f)
    return 1 if falhas else 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--porta", type=int, default=PORTA_PADRAO, help=f"porta em {ENDERECO} (padrão {PORTA_PADRAO}; as cobaias usam 8080 e 8000)")
    ap.add_argument("--corridas", default=None, help="pastas de corrida em resultados_alvo/, separadas por vírgula (padrão: 18d, 21d, 24 e 28b)")
    ap.add_argument("--resultados", default=str(RESULTADOS), help="a pasta dos resultados (padrão: resultados_alvo/)")
    ap.add_argument("--revisoes", default=None, help="onde ficam os arquivos de revisão (padrão: <resultados>/hub/revisoes)")
    ap.add_argument("--sem-abrir", action="store_true", help="não abre o navegador")
    ap.add_argument("--falar", action="store_true", help="imprime cada pedido atendido")
    ap.add_argument("--conferir", action="store_true", help="monta todos os casos sem subir servidor e diz quantos são")
    args = ap.parse_args(argv)
    raiz = Path(args.resultados)
    corridas = tuple(c.strip() for c in args.corridas.split(",") if c.strip()) if args.corridas else None
    acervo = hd.Acervo(raiz, corridas=corridas)
    if args.conferir:
        return conferir(acervo)
    revisoes = hr.Revisoes(Path(args.revisoes) if args.revisoes else raiz / "hub" / "revisoes")
    servidor = criar_servidor(acervo, revisoes, porta=args.porta, falar=args.falar)
    url = f"http://{ENDERECO}:{servidor.server_address[1]}/"
    print(f"Hub no ar em {url} ({len(acervo.indice())} casos). As revisões ficam em {revisoes.pasta}. Ctrl+C encerra.")
    if not args.sem_abrir:
        with contextlib.suppress(Exception):
            webbrowser.open(url)
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nHub encerrado.")
    finally:
        servidor.server_close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
