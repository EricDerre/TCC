#!/usr/bin/env python3
# ! Alteração de IA - Revisar: script novo (01/10/2026, Pré-Fase 4) que confere, com três chamadas ao modelo decidido,
# o que o Ollama instalado devolve quando se pede a probabilidade de cada token (`logprobs` e `top_logprobs` em
# /api/generate), e guarda as respostas cruas em resultados_alvo/pre_fase4/logprobs_amostra__<modelo>.json. Traz também o
# gancho `com_logprobs`, que acrescenta os dois campos à chamada que cliente_ollama.gerar já faz, sem mexer no que
# gerar devolve; a sonda de confiança da fase usa o mesmo gancho.
# ! Motivo: o levantamento de 22/09 (§6.12.8) recomendou a probabilidade do rótulo como sinal barato de incerteza e
# deixou escrito que a disponibilidade dela no /api/generate "não foi verificada por nenhuma das fontes". A
# documentação oficial diz que o campo existe desde a versão 0.12.11; falta ver nesta máquina (Ollama 0.34.4) o teto
# de alternativas por posição, se vêm os bytes de cada token (acento pode se partir entre dois tokens) e se a
# probabilidade devolvida é a de antes ou a de depois da temperatura 0,1 (se for a de depois, ela satura perto de 1 e
# precisa ser desfeita na conta). O gancho fica em `_post` e não em `gerar` porque executar_fase3.diagnosticar espalha
# o retorno de `gerar` dentro do registro: qualquer chave a mais ali mudaria o formato oficial de 37 chaves.
"""Uso (em Programacao/AgenteCore/experimentos, com o Ollama no ar e nenhum modelo residente):
  RESULTADOS_DIR=resultados_alvo python sondar_logprobs.py [--modelo qwen2.5:7b] [--caso ID] [--versao 1] [--top 20]
"""
from __future__ import annotations

import argparse
import contextlib
import hashlib
import json
import sys
import time
from datetime import datetime

import biblioteca as bib
import caminhos
import cliente_ollama as oll
import evolucao_biblioteca as evo
import executar_fase3
import pre_fase4 as pf
import recuperacao as rec
from banco_casos import CASOS
from banco_casos_extra import CASOS_EXTRA

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass

SAIDA = "logprobs_amostra__{slug}.json"   # uma amostra por modelo sondado
TEMPERATURA_DE_CONFERENCIA = 1.0   # só na chamada (b), que confere a ferramenta e não entra em resultado
TOKENS_DA_CONFERENCIA = 8


@contextlib.contextmanager
def com_logprobs(top: int, capturas: list, temperatura: float | None = None, num_predict: int | None = None,
                 exigir: bool = False):
    """Durante o bloco, toda chamada de cliente_ollama a /api/generate com prompt não vazio leva `logprobs` e
    `top_logprobs`; a resposta crua (sem o vetor `context`) e o corpo enviado (sem o texto do prompt, com o hash dele)
    vão para `capturas`. A chamada de prompt vazio com que `descarregar` tira o modelo da memória passa sem mudança.
    `temperatura` e `num_predict` só são trocados quando informados (uso exclusivo da conferência da ferramenta).
    Com exigir=True, resposta sem `logprobs` interrompe: uma corrida de horas não pode terminar sem o dado que foi
    buscar. O `_post` encontrado na entrada é restaurado na saída, com erro ou sem."""
    original = oll._post

    def trocado(caminho: str, corpo: dict, timeout: int = 900) -> dict:
        if caminho != "/api/generate" or not corpo.get("prompt"):
            return original(caminho, corpo, timeout)
        novo = {**corpo, "logprobs": True, "top_logprobs": top}
        if temperatura is not None or num_predict is not None:
            opcoes = dict(novo.get("options") or {})
            if temperatura is not None:
                opcoes["temperature"] = temperatura
            if num_predict is not None:
                opcoes["num_predict"] = num_predict
            novo["options"] = opcoes
        r = original(caminho, novo, timeout)
        if exigir and not r.get("logprobs"):
            raise RuntimeError("o Ollama respondeu sem `logprobs`: confira a versão instalada antes de continuar")
        capturas.append({"corpo": {k: v for k, v in novo.items() if k != "prompt"},
                         "prompt_sha256": hashlib.sha256(novo["prompt"].encode("utf-8")).hexdigest()[:12],
                         "resposta": {k: v for k, v in r.items() if k != "context"}})
        return r

    oll._post = trocado
    try:
        yield
    finally:
        oll._post = original


def _bytes_do_token(t: dict) -> bytes:
    b = t.get("bytes")
    return bytes(b) if b is not None else str(t.get("token", "")).encode("utf-8")


def texto_dos_tokens(logprobs: list[dict]) -> str:
    """O texto gerado, remontado pelos bytes de cada token: um caractere acentuado pode vir partido entre dois
    tokens, e só a junção dos bytes o devolve inteiro."""
    return b"".join(_bytes_do_token(t) for t in logprobs).decode("utf-8", errors="replace")


def tokens_que_partem_caractere(logprobs: list[dict]) -> int:
    """Quantos tokens, sozinhos, não formam texto UTF-8 válido (pedaço de caractere acentuado)."""
    n = 0
    for t in logprobs:
        try:
            _bytes_do_token(t).decode("utf-8")
        except UnicodeDecodeError:
            n += 1
    return n


def comparar_temperatura(pos_fria: dict, pos_quente: dict, t_fria: float, t_quente: float) -> dict:
    """Diz se a probabilidade que o Ollama devolve é a de antes ou a de depois da temperatura, comparando a mesma
    posição de duas chamadas iguais em tudo menos na temperatura. Antes da temperatura, a diferença de
    log-probabilidade entre dois tokens é a mesma nas duas chamadas (razão 1); depois, ela é dividida pela
    temperatura, e a razão entre as duas chamadas vale t_quente / t_fria."""
    fria = {a["token"]: a["logprob"] for a in pos_fria.get("top_logprobs") or []}
    quente = {a["token"]: a["logprob"] for a in pos_quente.get("top_logprobs") or []}
    comuns = sorted(set(fria) & set(quente), key=lambda t: -quente[t])
    if len(comuns) < 2:
        return {"veredito": "indeterminado", "razao": None, "tokens_comuns": len(comuns)}
    a, b = comuns[0], next((t for t in comuns[1:] if abs(quente[comuns[0]] - quente[t]) > 0.05), None)
    if b is None:
        return {"veredito": "indeterminado", "razao": None, "tokens_comuns": len(comuns)}
    razao = (fria[a] - fria[b]) / (quente[a] - quente[b])
    esperado_depois = t_quente / t_fria
    if abs(razao - 1.0) < 0.15:
        veredito = "antes"
    elif abs(razao - esperado_depois) / esperado_depois < 0.15:
        veredito = "depois"
    else:
        veredito = "indeterminado"
    return {"veredito": veredito, "razao": round(razao, 3), "tokens_comuns": len(comuns), "tokens_comparados": [a, b]}


def resumo_da_resposta(r: dict) -> dict:
    lp = r.get("logprobs") or []
    return {"tokens_com_logprob": len(lp),
            "top_por_posicao_max": max((len(t.get("top_logprobs") or []) for t in lp), default=0),
            "tem_bytes": bool(lp) and all(t.get("bytes") is not None for t in lp),
            "texto_bate": bool(lp) and texto_dos_tokens(lp).strip() == str(r.get("response", "")).strip(),
            "tokens_que_partem_caractere": tokens_que_partem_caractere(lp)}


def _caso(caso_id: str | None, particao: dict) -> dict:
    todos = {c["id"]: c for c in list(CASOS) + list(CASOS_EXTRA)}
    if caso_id:
        return todos[caso_id]
    return todos[sorted(i for i, c in particao["casos"].items() if c["particao"] == "avaliacao")[0]]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--modelo", default="qwen2.5:7b")
    ap.add_argument("--caso", help="id do caso (padrão: o primeiro da partição de avaliação)")
    ap.add_argument("--versao", type=int, default=1, help="versão da biblioteca do próprio modelo (0 a 3)")
    ap.add_argument("--top", type=int, default=20)
    ap.add_argument("--k", type=int, default=3)
    args = ap.parse_args()
    print(caminhos.descricao())
    c3 = caminhos.fase3("fase3")
    particao = json.loads(c3["particao"].read_text(encoding="utf-8"))
    caso = _caso(args.caso, particao)
    slug = executar_fase3._slug(args.modelo)
    snapshot = c3["bibliotecas"] / slug / f"epoca-{args.versao}"
    verbetes = bib.carregar(snapshot)
    ctx, prompt = executar_fase3.contexto_e_prompt(verbetes, rec.Indice(verbetes), caso, args.k)
    # o registro oficial do mesmo caso e da mesma versão diz qual foi o teto de tokens e qual foi a resposta
    oficial = next((json.loads(l) for l in (c3["raiz"] / slug / f"diagnosticos__L{args.versao}.jsonl").read_text(encoding="utf-8").splitlines()
                    if l.strip() and json.loads(l)["caso"] == caso["id"]), None)
    teto = (oficial or {}).get("teto_tokens") or 600
    ok, residentes = oll.um_modelo_por_vez()
    if residentes and residentes != [args.modelo]:
        print(f"há outro modelo residente ({residentes}); descarregue antes de sondar")
        return 2
    versao_ollama = executar_fase3._versao_ollama()
    digest = oll.instalados().get(args.modelo)
    print(f"modelo {args.modelo} (digest {digest}), Ollama {versao_ollama}; caso {caso['id']}, biblioteca L{args.versao} "
          f"({evo.hash_biblioteca(snapshot)}), contexto {ctx['verbetes_ids']}, teto {teto} tokens")
    capturas: list = []
    try:
        print("(a) temperatura oficial, com logprobs…")
        with com_logprobs(args.top, capturas):
            ra = oll.gerar(args.modelo, prompt, teto)
        print(f"    {ra['segundos']} s; {ra['tokens_entrada']} tokens de entrada, {ra['tokens_saida']} de saída")
        print(f"(b) temperatura {TEMPERATURA_DE_CONFERENCIA}, {TOKENS_DA_CONFERENCIA} tokens, com logprobs (conferência da ferramenta)…")
        with com_logprobs(args.top, capturas, temperatura=TEMPERATURA_DE_CONFERENCIA, num_predict=TOKENS_DA_CONFERENCIA):
            rb = oll.gerar(args.modelo, prompt, teto)
        print(f"    {rb['segundos']} s")
        print("(c) temperatura oficial, sem logprobs…")
        rc = oll.gerar(args.modelo, prompt, teto)
        print(f"    {rc['segundos']} s")
    finally:
        oll.descarregar(args.modelo)
        time.sleep(executar_fase3.PAUSA_DESCARGA)
    lp_a = capturas[0]["resposta"].get("logprobs") or []
    lp_b = capturas[1]["resposta"].get("logprobs") or []
    temperatura = (comparar_temperatura(lp_a[0], lp_b[0], oll.TEMPERATURA, TEMPERATURA_DE_CONFERENCIA)
                   if lp_a and lp_b else {"veredito": "indeterminado", "razao": None, "tokens_comuns": 0})
    registro = {
        "metadados": {"gerado_em": datetime.now().isoformat(timespec="seconds"), "modelo": args.modelo, "digest": digest,
                      "versao_ollama": versao_ollama, "caso": caso["id"], "biblioteca_epoca": args.versao,
                      "biblioteca_versao": evo.hash_biblioteca(snapshot), "verbetes_ids": ctx["verbetes_ids"],
                      "prompt_sha256": hashlib.sha256(prompt.encode("utf-8")).hexdigest()[:12], "prompt_chars": len(prompt),
                      "teto_tokens": teto, "top_pedido": args.top},
        "conferencias": {
            "a": resumo_da_resposta(capturas[0]["resposta"]),
            "b": resumo_da_resposta(capturas[1]["resposta"]),
            "temperatura": temperatura,
            "resposta_igual_sem_logprobs": ra["resposta"] == rc["resposta"],
            "resposta_igual_a_oficial": (oficial or {}).get("resposta") == ra["resposta"] if oficial else None,
        },
        "chamadas": {"a": {**capturas[0], "medicao": {k: v for k, v in ra.items() if k != "resposta"}},
                     "b": {**capturas[1], "medicao": {k: v for k, v in rb.items() if k != "resposta"}},
                     "c": {"medicao": {k: v for k, v in rc.items() if k != "resposta"}, "resposta": rc["resposta"]}},
        "resposta_oficial": (oficial or {}).get("resposta"),
    }
    pf.PASTA.mkdir(parents=True, exist_ok=True)
    saida = pf.PASTA / SAIDA.format(slug=slug)
    saida.write_text(json.dumps(registro, ensure_ascii=False, indent=2), encoding="utf-8")
    c = registro["conferencias"]
    print(f"\ngravado: {saida}")
    print(f"  (a) {c['a']}")
    print(f"  temperatura: {c['temperatura']}")
    print(f"  resposta igual sem logprobs: {c['resposta_igual_sem_logprobs']}; igual à oficial: {c['resposta_igual_a_oficial']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
