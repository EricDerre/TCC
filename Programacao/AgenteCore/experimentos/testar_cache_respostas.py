# ! Alteração de IA - Revisar: testes de cache_respostas.py (22/09/2026): desligado por padrão, chave
# estável, acerto marcado como vindo do cache, recusa em pasta de corrida oficial; sem Ollama (gerar falso).
# ! Motivo: o cache exato só pode existir se for impossível confundi-lo com uma medição — cada teste
# aqui protege uma dessas garantias (decisão 48), e a suíte roda em < 1 s, sem modelo residente.
"""Uso: PYTHONIOENCODING=utf-8 python testar_cache_respostas.py"""
from __future__ import annotations

import os
import shutil
import sys
import tempfile
import traceback
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cache_respostas as cr  # noqa: E402

_TEMPORARIOS: list[Path] = []


def _pasta() -> Path:
    p = Path(tempfile.mkdtemp(prefix="cache_respostas_"))
    _TEMPORARIOS.append(p)
    return p


def _gerar_falso(contador: list[int]):
    def gerar(modelo: str, prompt: str, max_tokens: int = 400) -> dict:
        contador[0] += 1
        return {"segundos": 1.5, "tokens_entrada": 10, "tokens_saida": 3, "carga_ms": 0,
                "prefill_ms": 900, "geracao_ms": 600, "total_ms": 1500, "resposta": f"r{contador[0]}"}
    return gerar


def teste_desligado_por_padrao_nao_grava_nem_le() -> None:
    """Sem CACHE_RESPOSTAS=1, gerar_com_cache chama o gerador toda vez e não cria o banco."""
    os.environ.pop("CACHE_RESPOSTAS", None)
    banco = _pasta() / "cache.sqlite"
    n = [0]
    r1 = cr.gerar_com_cache("m:1b", "p", 5, digest="abc", gerar=_gerar_falso(n), banco=banco)
    r2 = cr.gerar_com_cache("m:1b", "p", 5, digest="abc", gerar=_gerar_falso(n), banco=banco)
    assert n[0] == 2 and r1["resposta"] == "r1" and r2["resposta"] == "r2"
    assert "do_cache" in r1 and r1["do_cache"] is False
    assert not banco.exists(), "banco criado com o cache desligado"


def teste_ligado_grava_e_devolve_marcado() -> None:
    """Ligado: a 1ª chamada gera e grava; a 2ª volta do banco com do_cache=True, tempos zerados e a
    mesma resposta; prompt, modelo, digest ou opções diferentes são chaves diferentes."""
    os.environ["CACHE_RESPOSTAS"] = "1"
    try:
        banco = _pasta() / "cache.sqlite"
        n = [0]
        g = _gerar_falso(n)
        r1 = cr.gerar_com_cache("m:1b", "p", 5, digest="abc", gerar=g, banco=banco)
        r2 = cr.gerar_com_cache("m:1b", "p", 5, digest="abc", gerar=g, banco=banco)
        assert n[0] == 1, "segunda chamada não veio do cache"
        assert r1["do_cache"] is False and r2["do_cache"] is True
        assert r2["resposta"] == "r1"
        assert r2["prefill_ms"] == 0 and r2["geracao_ms"] == 0 and r2["segundos"] == 0.0, r2
        assert r2["medido_em"] == r1["medido_em"] or "medido_em" in r2
        cr.gerar_com_cache("m:1b", "p2", 5, digest="abc", gerar=g, banco=banco)
        cr.gerar_com_cache("m:1b", "p", 6, digest="abc", gerar=g, banco=banco)
        cr.gerar_com_cache("m:1b", "p", 5, digest="xyz", gerar=g, banco=banco)
        cr.gerar_com_cache("m:2b", "p", 5, digest="abc", gerar=g, banco=banco)
        assert n[0] == 5, n
        assert cr.tamanho(banco) == 5
    finally:
        os.environ.pop("CACHE_RESPOSTAS", None)


def teste_chave_estavel_e_sem_colisao_de_separador() -> None:
    """A chave é sha256 de campos separados por NUL: 'a|b' + 'c' não colide com 'a' + 'b|c'."""
    k1 = cr.chave("m", "d", "a|b", {"num_predict": 5})
    k2 = cr.chave("m", "d", "a|b", {"num_predict": 5})
    assert k1 == k2 and len(k1) == 64
    assert cr.chave("m|d", "", "x", {}) != cr.chave("m", "d", "x", {})
    assert cr.chave("m", "d", "x", {"num_predict": 5}) != cr.chave("m", "d", "x", {"num_predict": 6})


def teste_recusa_em_pasta_oficial() -> None:
    """Ligado e com RESULTADOS apontando para a área oficial (resultados_alvo), gerar_com_cache
    levanta RuntimeError antes de inferir ou gravar."""
    os.environ["CACHE_RESPOSTAS"] = "1"
    original = cr.caminhos.RESULTADOS
    try:
        cr.caminhos.RESULTADOS = Path("C:/qualquer/resultados_alvo")
        n = [0]
        try:
            cr.gerar_com_cache("m:1b", "p", 5, digest="abc", gerar=_gerar_falso(n), banco=_pasta() / "c.sqlite")
        except RuntimeError as e:
            assert "resultados_alvo" in str(e)
        else:
            raise AssertionError("não recusou em pasta oficial")
        assert n[0] == 0
        assert cr.cache_permitido() is False
        cr.caminhos.RESULTADOS = Path("C:/qualquer/resultados")
        assert cr.cache_permitido() is True
    finally:
        cr.caminhos.RESULTADOS = original
        os.environ.pop("CACHE_RESPOSTAS", None)


def main() -> None:
    testes = [(n, f) for n, f in globals().items() if n.startswith("teste_") and callable(f)]
    try:
        for nome, funcao in testes:
            try:
                funcao()
            except Exception:
                print(nome)
                traceback.print_exc()
                sys.exit(1)
            print(f"{nome} ok")
        print(f"{len(testes)} testes ok")
    finally:
        for caminho in _TEMPORARIOS:
            shutil.rmtree(caminho, ignore_errors=True)


if __name__ == "__main__":
    main()
