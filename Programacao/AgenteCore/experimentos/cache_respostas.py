# ! Alteração de IA - Revisar: cache EXATO de respostas do Ollama (22/09/2026; decisão 48): envolve
# cliente_ollama.gerar sem alterá-lo, guarda em SQLite a resposta de (modelo, digest, prompt, opções),
# fica DESLIGADO por padrão (liga com CACHE_RESPOSTAS=1) e RECUSA funcionar quando RESULTADOS_DIR
# aponta para a área oficial (resultados_alvo). Um acerto volta com do_cache=True e tempos zerados.
# ! Motivo: o artigo do The New Stack (14/09/2026) e a literatura mostram que o cache exato corta custo em
# reexecuções idênticas (regerar avaliação e gráficos, laço de desenvolvimento da Fase 4, demonstrações);
# mas num experimento medido um acerto de cache tem prefill ≈ 0 e falsificaria justamente a variável em
# estudo — por isso ele não pode ser confundido com medição (tempos zerados, marca explícita) nem existir
# na pasta de corrida oficial. O cache semântico foi descartado (decisão 48): reaproveitar a resposta de
# outro caso por similaridade é indefensável numa banca e exigiria embeddings na mesma CPU.
"""Uso (fora de corrida medida):

    set CACHE_RESPOSTAS=1
    from cache_respostas import gerar_com_cache
    r = gerar_com_cache("qwen2.5:7b", prompt, max_tokens=600)   # r["do_cache"] diz se veio do banco

O banco padrão fica em <RESULTADOS>/cache_respostas.sqlite (nunca em resultados_alvo/)."""
from __future__ import annotations

import hashlib
import json
import os
import sqlite3
import sys
from datetime import datetime
from pathlib import Path
from typing import Callable

sys.path.insert(0, str(Path(__file__).resolve().parent))
import caminhos  # noqa: E402
import cliente_ollama as oll  # noqa: E402

PASTA_OFICIAL = "resultados_alvo"
_DIGESTS: dict[str, str] = {}


def ligado() -> bool:
    """CACHE_RESPOSTAS=1 liga; qualquer outro valor (ou ausência) deixa desligado."""
    return os.environ.get("CACHE_RESPOSTAS", "").strip() == "1"


def cache_permitido() -> bool:
    """False quando caminhos.RESULTADOS é (ou está dentro de) a área oficial `resultados_alvo`."""
    return PASTA_OFICIAL not in caminhos.RESULTADOS.parts


def chave(modelo: str, digest: str, prompt: str, opcoes: dict) -> str:
    """sha256 dos campos separados por NUL (não por '|', para 'a|b'+'c' não colidir com 'a'+'b|c');
    opções serializadas com chaves ordenadas."""
    partes = [modelo, digest, prompt, json.dumps(opcoes, sort_keys=True, ensure_ascii=False)]
    return hashlib.sha256("\0".join(partes).encode("utf-8")).hexdigest()


def _abrir(banco: Path) -> sqlite3.Connection:
    banco.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(banco)
    con.execute("CREATE TABLE IF NOT EXISTS respostas (chave TEXT PRIMARY KEY, modelo TEXT, digest TEXT, "
                "gravado_em TEXT, resultado TEXT)")
    return con


def tamanho(banco: Path) -> int:
    if not banco.exists():
        return 0
    with _abrir(banco) as con:
        return con.execute("SELECT COUNT(*) FROM respostas").fetchone()[0]


def _digest(modelo: str) -> str:
    if modelo not in _DIGESTS:
        try:
            _DIGESTS.update(oll.instalados())
        except Exception:
            _DIGESTS[modelo] = ""
    return _DIGESTS.get(modelo, "")


def gerar_com_cache(modelo: str, prompt: str, max_tokens: int = 400, *, digest: str | None = None,
                    gerar: Callable[..., dict] = oll.gerar, banco: Path | None = None) -> dict:
    """Igual a cliente_ollama.gerar, mais o campo `do_cache`. Desligado: chama `gerar` e devolve
    do_cache=False sem tocar em disco. Ligado: recusa em pasta oficial; acerto devolve a resposta
    guardada com do_cache=True, tempos zerados e `medido_em` da gravação original."""
    if not ligado():
        return {**gerar(modelo, prompt, max_tokens), "do_cache": False}
    if not cache_permitido():
        raise RuntimeError(f"cache_respostas: recusado — RESULTADOS aponta para a área oficial "
                           f"({PASTA_OFICIAL}); um acerto de cache falsificaria a medição")
    banco = banco or (caminhos.RESULTADOS / "cache_respostas.sqlite")
    digest = _digest(modelo) if digest is None else digest
    opcoes = {"num_gpu": 0, "num_ctx": oll.NUM_CTX, "temperature": oll.TEMPERATURA, "num_predict": max_tokens}
    k = chave(modelo, digest, prompt, opcoes)
    with _abrir(banco) as con:
        linha = con.execute("SELECT resultado FROM respostas WHERE chave = ?", (k,)).fetchone()
    if linha:
        guardado = json.loads(linha[0])
        return {**guardado, "segundos": 0.0, "carga_ms": 0, "prefill_ms": 0, "geracao_ms": 0,
                "total_ms": 0, "do_cache": True}
    resultado = gerar(modelo, prompt, max_tokens)
    agora = datetime.now().isoformat(timespec="seconds")
    guardado = {**resultado, "medido_em": agora}
    with _abrir(banco) as con:
        con.execute("INSERT OR REPLACE INTO respostas VALUES (?, ?, ?, ?, ?)",
                    (k, modelo, digest, agora, json.dumps(guardado, ensure_ascii=False)))
    return {**guardado, "do_cache": False}
