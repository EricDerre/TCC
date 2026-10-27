#!/usr/bin/env python3
# ! Alteração de IA - Revisar: arquivo novo (26/10/2026, Fase 4, pacote P2): o orquestrador da Fase 4, no molde de
# executar_fase3b.py, com o primeiro modo, `reproducao` (corrida 17 do plano aprovado): para cada caso de avaliação
# (os 36 oficiais e os 36 inéditos) cuja causa tem um modo de injeção e cuja rota tem tela (`GET /api/produtos` e
# `GET /api/produtos/{id}` em produtos_api.php), liga o modo na CobaiaAPI pelo endpoint admin, roda o roteiro no
# navegador com o interceptador, poda a árvore e o corpo, monta o caso ao vivo com o sintoma por molde, decide se a
# tela reproduz o caso (regra R1) e grava tudo: `reproducao.jsonl`, `fora.json`, `condicoes_fase4.json`, a trilha v2
# da corrida e o log com a linha FIM. Sobe as cobaias por run.start_services e restaura o banco antes. Sem modelo.
# ! Motivo: antes de gastar modelo, a Fase 4 precisa saber quantos casos a tela reproduz, quanto custa um cenário e
# quanto pesa a trilha (plano, P2, "Mede"); e a corrida de referência em modo normal de cada cenário é a trilha
# dourada contra a qual a árvore de cada caso é comparada (especificação, seção 9).
"""Uso (em Programacao/AgenteCore/experimentos):
  RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo reproducao --saida fase4_reproducao [--casos N] [--canal chromium]
Depois: RESULTADOS_DIR=resultados_alvo python avaliar_fase4.py --reproducao --saida fase4_reproducao"""
from __future__ import annotations

import argparse
import copy
import json
import re
import statistics
import sys
import time
import urllib.request
from pathlib import Path

EXP = Path(__file__).resolve().parent
RAIZ = EXP.parent.parent.parent
sys.path.insert(0, str(RAIZ))

import caminhos
import caso_ao_vivo as cv
import cenarios_fase4 as cen
import executar_fase3b as e3b
import interceptador as ic
import navegador
import poda
import trilha as tr

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass

MODOS = ("reproducao",)
# ! Alteração de IA - Revisar: orçamento de tempo da chamada à API baixado de 5000 para 1000 ms e a regra R1 ganhou a
# comparação com a corrida de referência em modo normal (corpo igual? árvore completa igual?), além do contrato e do
# roteiro; sem a chamada do alvo, vale a última chamada do roteiro (chamada_do_caso).
# ! Motivo: na primeira corrida 17 (26/10/2026) a mediana normal foi 27 ms e o `latency` no detalhe levou 2007 ms,
# abaixo do orçamento antigo; e mutações que o contrato não vê (acentos estragados, preço em centavos, tipo girado,
# nome com sufixo) passavam como "não reproduz" embora o corpo e a tela tenham mudado contra a referência; nos casos
# de detalhe em que o catálogo já quebra, a chamada do detalhe nunca acontece e a do catálogo é a evidência.
ORCAMENTO_DE_TEMPO_MS = 1000
TOKEN_PADRAO = "troque-isto-localmente"   # settings.admin_token da CobaiaAPI (app/config.py), sem .env
URL_ADMIN = "http://127.0.0.1:8000/api/admin/fault-mode"
_ROTA_CATALOGO = re.compile(r"^GET /api/produtos/?(\?.*)?$")
_ROTA_DETALHE = re.compile(r"^GET /api/produtos/(\d+)")
IDS_DO_SEED = range(1, 15)


# ------------------------------------------------------------------ partes puras (testadas sem cobaias)

def selecionar_casos(casos: list[dict]) -> dict:
    """Separa os casos que a tela consegue reproduzir (causa com modo e rota de produtos) dos que ficam fora, com o
    motivo de cada um; para os reproduzíveis diz o modo, o campo alvo, o cenário e o id do produto."""
    reproduziveis, fora = [], []
    for c in casos:
        causa = c["gabarito"]["causa_raiz"]
        req = str(c["entrada"].get("requisicao") or "")
        base = {"id": c["id"], "classe": c["classe"], "nivel": c["nivel"], "causa": causa, "requisicao": req}
        if causa in cen.CAUSAS_PELO_HARNESS:
            fora.append({**base, "motivo": f"armada pelo harness (ficha 29): {causa}"})
            continue
        if causa not in cen.MODO_POR_CAUSA:
            fora.append({**base, "motivo": f"sem modo para a causa {causa}"})
            continue
        detalhe = _ROTA_DETALHE.match(req)
        if detalhe:
            cenario, produto_id = "api-detalhe", int(detalhe.group(1))
        elif _ROTA_CATALOGO.match(req):
            cenario, produto_id = "api-catalogo", None
        else:
            fora.append({**base, "motivo": f"sem tela: a rota {req!r} não é consumida por página nenhuma"})
            continue
        modo = cen.MODO_POR_CAUSA[causa]
        campo = c["gabarito"].get("campo_afetado") if modo in cen.MODOS_COM_CAMPO else None
        reproduziveis.append({**base, "modo": modo, "campo": campo, "cenario": cenario, "produto_id": produto_id})
    return {"reproduziveis": reproduziveis, "fora": fora}


def corpo_admin(modo: str, campo: str | None) -> dict:
    """O corpo do POST /api/admin/fault-mode: o campo alvo só vai nos modos que o usam; `normal` nunca leva campo."""
    return {"mode": modo, "target_field": campo if modo in cen.MODOS_COM_CAMPO else None, "probability": 1.0}


def reproduz(resultado: dict, diff_corpo: dict | None, registro: dict | None, referencia: dict | None = None) -> dict:
    """Regra R1 do plano: a tela reproduz o caso quando a chamada à API saiu do normal (status, corpo, contrato,
    tempo acima do orçamento, corpo diferente da referência em modo normal), quando a árvore completa da página
    difere da referência ou quando uma conferência do roteiro falhou. Sem chamada capturada, não reproduz."""
    if registro is None:
        return {"reproduz": False, "motivo": "nenhuma chamada à API capturada no roteiro"}
    motivos = []
    if registro.get("status") != 200:
        motivos.append(f"status {registro.get('status')}")
    if diff_corpo is not None:
        if diff_corpo.get("corpo") != "json":
            motivos.append(f"corpo {diff_corpo.get('corpo')}")
        if diff_corpo.get("diferencas"):
            motivos.append("diff do contrato: " + ", ".join(sorted({d["tipo"] for d in diff_corpo["diferencas"]})))
    if referencia and referencia.get("corpo_igual") is False:
        motivos.append("corpo diferente da referência em modo normal")
    arv = (referencia or {}).get("arvore") or {}
    if arv.get("a_menos") or arv.get("a_mais"):
        motivos.append(f"árvore diferente da referência: {arv.get('a_menos', 0)} linha(s) a menos e {arv.get('a_mais', 0)} a mais")
    if resultado.get("conferencia_falha"):
        motivos.append(f"conferência '{resultado['conferencia_falha'].get('nome')}' falhou")
    tempo = registro.get("tempo_ms")
    if tempo is not None and tempo > ORCAMENTO_DE_TEMPO_MS:
        motivos.append(f"tempo de resposta {tempo:.0f} ms acima do orçamento de {ORCAMENTO_DE_TEMPO_MS} ms")
    if motivos:
        return {"reproduz": True, "motivo": "; ".join(motivos)}
    return {"reproduz": False, "motivo": "nenhuma diferença medida contra o contrato, a referência e o roteiro"}


def chamada_do_caso(chamadas: list[dict], cenario_id: str, produto_id: int | None) -> tuple[dict | None, bool]:
    """A chamada à API que o caso descreve (catálogo ou detalhe do produto) e se é mesmo a do alvo; sem ela, a última
    chamada GET do roteiro (o catálogo que quebrou antes do detalhe), marcada como não sendo a do alvo."""
    alvo = "/api/produtos" if cenario_id == "api-catalogo" else f"/api/produtos/{produto_id}"
    for c in reversed(chamadas):
        if c["metodo"] == "GET" and c["caminho"] == alvo:
            return c, True
    for c in reversed(chamadas):
        if c["metodo"] == "GET":
            return c, False
    return None, False


def _corpos_iguais(a: str | None, b: str | None) -> bool | None:
    """Os dois corpos HTTP são o mesmo dado? Compara o JSON decodificado (ordem das chaves não importa) ou o texto."""
    if a is None or b is None:
        return None
    try:
        return json.loads(a) == json.loads(b)
    except ValueError:
        return a == b


def com_produto(cenario: dict, produto_id: int | None) -> tuple[dict, int | None]:
    """O cenário de detalhe apontando para o produto do caso (ids fora do seed caem no 1, registrado)."""
    if produto_id is None:
        return cenario, None
    usado = produto_id if produto_id in IDS_DO_SEED else 1
    novo = copy.deepcopy(cenario)
    for p in novo["passos"]:
        if "seletor" in p:
            p["seletor"] = p["seletor"].replace("data-id='1'", f"data-id='{usado}'")
    return novo, usado


# ------------------------------------------------------------------ cobaias e API

def ligar_modo(modo: str, campo: str | None, token: str = TOKEN_PADRAO, url: str = URL_ADMIN) -> dict:
    corpo = json.dumps(corpo_admin(modo, campo)).encode("utf-8")
    pedido = urllib.request.Request(url, data=corpo, method="POST",
                                    headers={"Content-Type": "application/json", "X-Admin-Token": token})
    with urllib.request.urlopen(pedido, timeout=30) as resposta:
        return json.load(resposta)


def casos_de_avaliacao() -> list[dict]:
    """Os 36 oficiais de avaliação (partição gravada pela Fase 3) mais os 36 inéditos da Fase 3-B."""
    oficiais = e3b._casos_avaliacao(e3b._particao_oficial(e3b._oficial()))
    return oficiais + e3b._casos_ineditos()


# ------------------------------------------------------------------ a corrida

def rodar_reproducao(args: argparse.Namespace) -> int:
    import _env_common as env
    import restaurar_banco as rb
    import run

    saida = caminhos.fase3(args.saida)["raiz"]
    saida.mkdir(parents=True, exist_ok=True)
    log = saida / "fase4.log"

    def marco(msg: str) -> None:
        linha = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}"
        print(linha)
        with open(log, "a", encoding="utf-8") as f:
            f.write(linha + "\n")

    inicio = cen.agora()
    t0 = time.monotonic()
    arq_ambiente = caminhos.RESULTADOS / "fase4" / "ambiente.json"
    ambiente = json.loads(arq_ambiente.read_text(encoding="utf-8")) if arq_ambiente.exists() else {}
    versoes = ambiente.get("versoes", {})
    openapi = json.loads((ic.FIXTURES / "openapi.json").read_text(encoding="utf-8"))
    contrato = cv.contrato_do_openapi(openapi, "ProdutoOut", cv.AJUSTES_PRODUTO)
    todos = casos_de_avaliacao()
    sel = selecionar_casos(todos)
    if args.casos:
        sel["reproduziveis"] = sel["reproduziveis"][:args.casos]
    condicoes = {"modo": "reproducao", "criado_em": inicio, "saida": args.saida, "versoes": versoes, "canal": args.canal,
                 "regra_r1": "status != 200, corpo fora do JSON, diff do contrato, corpo ou árvore completa diferentes da referência em modo "
                             "normal, conferência do roteiro falhou ou tempo da chamada acima do orçamento",
                 "hosts_permitidos": list(ic.HOSTS_PERMITIDOS), "hosts_har": list(ic.CDN_PADRAO), "hosts_silenciosos": list(ic.HOSTS_SILENCIOSOS),
                 "limites": tr.LIMITES_PADRAO, "orcamento_de_tempo_ms": ORCAMENTO_DE_TEMPO_MS, "contrato": contrato,
                 "casos": len(todos), "reproduziveis": len(sel["reproduziveis"]), "fora": len(sel["fora"]), "modelo": None}
    (saida / "condicoes_fase4.json").write_text(json.dumps(condicoes, ensure_ascii=False, indent=2), encoding="utf-8")
    (saida / "fora.json").write_text(json.dumps(sel["fora"], ensure_ascii=False, indent=1), encoding="utf-8")
    marco(f"INÍCIO reproducao: {len(todos)} casos, {len(sel['reproduziveis'])} reproduzíveis na tela, {len(sel['fora'])} fora")

    front, api = run.start_services()
    trilha = tr.Trilha(versao=tr.V2, pasta_blobs=saida / "blobs")
    trilha.corrida(tr.cabecalho_de_corrida(modelo="(sem modelo: reprodução na tela)", versao_ollama=str(versoes.get("ollama") or "não medida"),
                                           inicio=inicio, playwright=versoes.get("playwright"), navegador=versoes.get("navegador"),
                                           canal=args.canal, corrida=args.saida, etapas_registradas=["roteiro", "interceptacao", "poda", "caso_ao_vivo"],
                                           etapas_nao_registradas=["diagnostico", "cura", "edicao_biblioteca"],
                                           extras={"modo": "reproducao", "hash_biblioteca": None}), ts=inicio)
    registros: list[dict] = []
    arq_registros = saida / "reproducao.jsonl"
    if arq_registros.exists():
        arq_registros.unlink()
    try:
        if not run.wait_until_ready(timeout_s=90):
            marco("!! as cobaias não responderam nas portas 8080 e 8000")
            return 2
        cli = env.find_mysql_cli()
        if rb.restaurar(cli) != rb.CONTAGENS_DO_SEED:
            marco("!! o banco restaurado não tem as contagens do seed")
            return 2
        referencias: dict[tuple, dict] = {}
        with navegador.Navegador(canal=args.canal) as nav:
            def referencia(cid: str, pid: int | None) -> dict:
                """A corrida do cenário em modo normal (trilha dourada), uma por cenário e produto, feita na primeira vez."""
                chave = (cid, pid)
                if chave in referencias:
                    return referencias[chave]
                cenario_ref, _ = com_produto(cen.cenario(cid), pid)
                ligar_modo("normal", None, args.token)
                pagina = nav.nova_pagina()
                inter = ic.Interceptador(pagina)
                r = cen.rodar_cenario(cenario_ref, pagina, inter)
                pagina.close()
                captura = r["capturas"][-1] if r["capturas"] else {}
                podada = poda.podar_arvore(captura.get("nos") or [], captura.get("titulo") or "", alvo=cenario_ref["alvo"],
                                           interativos=captura.get("interativos"))
                chamada, _ = chamada_do_caso(r["chamadas"], cid, pid)
                corpo = inter.corpo(chamada["corpo_sha"]) if chamada and chamada.get("corpo_sha") else None
                ref = {"arvore": podada["texto"], "aria": captura.get("aria") or "", "corpo": corpo, "chamada": chamada,
                       "passou": r["passou"], "segundos": r["segundos"]}
                referencias[chave] = ref
                tid = f"{args.saida}/referencia/{cid}" + (f"/{pid}" if pid else "") + "@normal"
                trilha.evento("entrada", tid, {"cenario": cid, "produto_id": pid, "modo": "normal", "referencia": True,
                                               "corpo": trilha.blob(corpo, "corpo_http") if corpo is not None else None}, "ao_vivo", ts=cen.agora())
                trilha.evento("poda", tid, {"alvo": "arvore", "antes": {"nos": podada["antes"]}, "depois": {"linhas": podada["depois"]},
                                            "regras": podada["regras"], "sha": trilha.blob(podada["texto"], "arvore_podada"), "diff": []},
                              "ao_vivo", ts=cen.agora())
                marco(f"referência {cid}{' produto ' + str(pid) if pid else ''}: {'passou' if r['passou'] else 'FALHOU'} em {r['segundos']} s; "
                      f"árvore {podada['antes']} nós, {podada['depois']} linhas")
                return ref

            for cid in ("api-catalogo", "api-detalhe"):
                referencia(cid, 1 if cid == "api-detalhe" else None)
            for n, item in enumerate(sel["reproduziveis"], 1):
                cenario_, usado = com_produto(cen.cenario(item["cenario"]), item["produto_id"])
                ref = referencia(item["cenario"], usado)
                ligar_modo(item["modo"], item["campo"], args.token)
                pagina = nav.nova_pagina()
                inter = ic.Interceptador(pagina)
                r = cen.rodar_cenario(cenario_, pagina, inter)
                pagina.close()
                ligar_modo("normal", None, args.token)
                chamada, do_alvo = chamada_do_caso(r["chamadas"], item["cenario"], usado)
                corpo = inter.corpo(chamada["corpo_sha"]) if chamada and chamada.get("corpo_sha") else None
                diff = poda.diff_contrato(contrato, corpo if corpo is not None else "",
                                          forma_esperada=cenario_["forma"] if do_alvo else "lista") if chamada else None
                captura = r["capturas"][-1] if r["capturas"] else {}
                podada = (poda.podar_arvore(captura["nos"], captura.get("titulo") or "", alvo=cenario_["alvo"], interativos=captura.get("interativos"))
                          if captura.get("nos") else None)
                diff_arv = cv.diff_arvore(ref["arvore"], podada["texto"]) if podada else None
                diff_completa = cv.diff_arvore(ref["aria"], captura.get("aria") or "") if captura.get("aria") else None
                corpo_ref = ref["corpo"] if do_alvo else None
                comparacao = {"corpo_igual": _corpos_iguais(corpo_ref, corpo), "arvore": diff_completa}
                veredito = reproduz(r, diff, chamada, comparacao)
                status = chamada["status"] if chamada else None
                sintoma = cv.sintoma_por_molde(r["conferencia_falha"], diff, diff_completa or diff_arv, status=status)
                observacao = (f"poda: árvore com {podada['antes']} nós e {podada['depois']} linhas depois" if podada else "sem captura da árvore")
                if diff:
                    observacao += f"; corpo {diff['corpo']}, forma {diff['forma']}, {len(diff['diferencas'])} diferença(s) contra o contrato"
                caso_vivo = cv.montar_caso(f"{item['id']}@tela", item["requisicao"], status, contrato, (diff or {}).get("trecho") or "",
                                           sintoma, arvore=podada["texto"] if podada else None, observacao=observacao)
                tid = f"{args.saida}/{item['id']}@tela"
                trilha.evento("entrada", tid, {"caso": item["id"], "classe": item["classe"], "nivel": item["nivel"], "modo": item["modo"],
                                               "campo": item["campo"], "cenario": item["cenario"], "produto_id": usado,
                                               "caso_ao_vivo": trilha.blob(json.dumps(caso_vivo, ensure_ascii=False, sort_keys=True), "caso_ao_vivo")},
                              "ao_vivo", ts=r["inicio"])
                for i, (passo, tempo) in enumerate(zip(cenario_["passos"], r["tempos_ms"])):
                    trilha.evento("acao", tid, {"passo": i + 1, "acao": passo["acao"], "seletor": passo.get("seletor"), "url": passo.get("url"),
                                                "tempo_ms": tempo, "falhou": r["passo_falho"] == i}, "ao_vivo", ts=cen.agora())
                for c in r["chamadas"]:
                    dados = {k: v for k, v in c.items() if k != "url"}
                    dados["corpo"] = trilha.blob(inter.corpo(c["corpo_sha"]), "corpo_http") if c.get("corpo_sha") and inter.corpo(c["corpo_sha"]) is not None else None
                    trilha.evento("interceptacao", tid, dados, "ao_vivo", ts=cen.agora())
                for conf in r["conferencias"]:
                    trilha.evento("verificacao", tid, tr._v("conferencia_do_roteiro", conf["nome"], "confere" if conf["passou"] else "nao_confere",
                                                            {"esperado": conf["esperado"], "observado": conf["observado"]}), "ao_vivo", ts=cen.agora())
                if podada:
                    trilha.evento("poda", tid, {"alvo": "arvore", "antes": {"nos": podada["antes"]}, "depois": {"linhas": podada["depois"]},
                                                "regras": podada["regras"], "sha": trilha.blob(podada["texto"], "arvore_podada"),
                                                "diff": [{"campo": "arvore", "esperado": f"{diff_arv['a_menos']} linha(s) da referência", "recebido": f"{diff_arv['a_mais']} linha(s) novas"}] if diff_arv else []},
                                  "ao_vivo", ts=cen.agora())
                if diff is not None:
                    trilha.evento("poda", tid, {"alvo": "corpo_http", "antes": {"chars": len(corpo or "")}, "depois": {"chars": len(diff.get("trecho") or "")},
                                                "regras": ["diff_contra_contrato"], "sha": trilha.blob(diff.get("trecho") or "", "corpo_podado"),
                                                "diff": [{"campo": d["campo"], "esperado": d.get("esperado"), "recebido": d.get("recebido"), "tipo": d["tipo"]} for d in diff["diferencas"]]},
                                  "ao_vivo", ts=cen.agora())
                for inc in inter.incidentes:
                    trilha.evento("incidente", tid, inc, "ao_vivo", ts=cen.agora())
                registro = {"id": item["id"], "classe": item["classe"], "nivel": item["nivel"], "causa": item["causa"], "modo": item["modo"],
                            "campo": item["campo"], "cenario": item["cenario"], "produto_id": item["produto_id"], "produto_id_usado": usado,
                            "requisicao": item["requisicao"], "reproduz": veredito["reproduz"], "motivo": veredito["motivo"],
                            "status": status, "tempo_ms": chamada.get("tempo_ms") if chamada else None, "segundos": r["segundos"],
                            "chamada_do_alvo": do_alvo, "chamada_caminho": chamada.get("caminho") if chamada else None,
                            "corpo_igual_referencia": comparacao["corpo_igual"],
                            "arvore_completa_a_menos": diff_completa["a_menos"] if diff_completa else None,
                            "arvore_completa_a_mais": diff_completa["a_mais"] if diff_completa else None,
                            "passou_o_roteiro": r["passou"], "passo_falho": r["passo_falho"],
                            "conferencia_falha": (r["conferencia_falha"] or {}).get("nome"), "erro": r["erro"],
                            "arvore_antes": podada["antes"] if podada else None, "arvore_depois": podada["depois"] if podada else None,
                            "arvore_a_menos": diff_arv["a_menos"] if diff_arv else None, "arvore_a_mais": diff_arv["a_mais"] if diff_arv else None,
                            "corpo_chars": len(corpo) if corpo is not None else None, "caso_chars": len(json.dumps(caso_vivo, ensure_ascii=False)),
                            "diff": {"corpo": diff["corpo"], "forma": diff["forma"], "itens": diff["itens"], "tipos": sorted({d["tipo"] for d in diff["diferencas"]})} if diff else None,
                            "sintoma": sintoma, "incidentes": len(inter.incidentes), "chamadas": len(r["chamadas"])}
                registros.append(registro)
                with open(arq_registros, "a", encoding="utf-8") as f:
                    f.write(json.dumps(registro, ensure_ascii=False) + "\n")
                marco(f"[{n}/{len(sel['reproduziveis'])}] {item['id']} ({item['modo']}{' em ' + item['campo'] if item['campo'] else ''}): "
                      f"{'REPRODUZ' if veredito['reproduz'] else 'não reproduz'}: {veredito['motivo']} ({r['segundos']} s)")
    finally:
        try:
            ligar_modo("normal", None, args.token)
        except Exception:  # noqa: BLE001 - a API pode já ter caído; o modo volta ao normal no próximo boot
            pass
        for proc in (front, api):
            if proc.poll() is None:
                proc.terminate()
        env.stop_managed_mariadbd()
    fim = cen.agora()
    trilha.fechar(fim)
    trilha.gravar(saida / "trilha_reproducao.jsonl")
    reproduzem = sum(1 for r in registros if r["reproduz"])
    marco(f"FIM reproducao: {reproduzem} de {len(registros)} casos reproduzem na tela; {len(sel['fora'])} fora; "
          f"duração {time.monotonic() - t0:.0f} s; trilha {(saida / 'trilha_reproducao.jsonl').stat().st_size} bytes")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--modo", choices=MODOS, required=True)
    ap.add_argument("--saida", required=True, help="pasta da corrida em RESULTADOS_DIR (ex.: fase4_reproducao)")
    ap.add_argument("--casos", type=int, default=0, help="limita aos N primeiros casos reproduzíveis (0 = todos)")
    ap.add_argument("--canal", choices=navegador.CANAIS, default="chromium")
    ap.add_argument("--token", default=TOKEN_PADRAO, help="X-Admin-Token da CobaiaAPI")
    args = ap.parse_args()
    print(caminhos.descricao())
    if args.modo == "reproducao":
        return rodar_reproducao(args)
    return 1


if __name__ == "__main__":
    sys.exit(main())
