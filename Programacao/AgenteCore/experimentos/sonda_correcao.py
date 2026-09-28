#!/usr/bin/env python3
# ! Alteração de IA - Revisar: sonda da Fase 3-B "detecção de correção" (28/09/2026, decisão 58):
# roda UMA época de aprendizado do executor oficial (executar_fase3.rodar_epoca, sem alterá-lo)
# sobre uma CÓPIA de um snapshot fechado de um modelo, com só os casos corrigidos como
# aprendizado, e imprime o que o modelo diagnosticou e propôs para a biblioteca ao rever esses
# casos — mais o diff entre a época lida e a época nova.
# ! Motivo: o Eric quer saber se o modelo, ao encontrar na própria biblioteca uma nota escrita a
# partir de um caso que depois foi corrigido (efe-10, época 1 do qwen2.5:7b) ou um caso cujo
# sintoma mudou (efe-3), percebe a mudança e registra "erro + solução sugerida + solução
# aplicada" sem apagar o histórico. A Fase 3-B só diagnostica (passada final, executar_fase3b);
# esta sonda precisa da época de aprendizado (diagnóstico + proposta + validação em código), que
# o executor oficial já faz — por isso reaproveita rodar_epoca e os auxiliares da 3-B em vez de
# reimplementar. Nada em resultados_alvo/fase3/ é escrito: a saída é uma pasta nova.
"""Uso (na pasta experimentos, com o Ollama no ar e nenhum modelo residente):

    RESULTADOS_DIR=resultados_alvo python sonda_correcao.py --saida fase3b_correcao \\
        --modelo qwen2.5:7b --versao 1 --casos efe-3 efe-10

Lê <RESULTADOS>/fase3/bibliotecas/<slug>/epoca-<versao> (fechada), copia para
<RESULTADOS>/<saida>/bibliotecas/<slug>/epoca-<versao>, grava particao.json com os casos pedidos
em 'aprendizado' (e nenhum em avaliação), chama executar_fase3.rodar_epoca(n=versao+1,
epocas=versao+1) — diagnóstico com k verbetes, proposta de edição, validação em código,
fechamento da epoca-<versao+1> — e imprime diagnósticos, propostas (com a decisão do validador)
e as linhas acrescentadas na época nova."""
from __future__ import annotations

import argparse
import difflib
import json
import sys
from pathlib import Path

import banco_casos
import banco_casos_extra
import caminhos
import executar_fase3
import executar_fase3b

MAX_TEXTO = 900  # caracteres impressos por resposta crua (o JSONL guarda tudo)


def _casos(ids: list[str]) -> list[dict]:
    todos = {c["id"]: c for c in banco_casos.CASOS + banco_casos_extra.CASOS_EXTRA}
    faltam = [i for i in ids if i not in todos]
    if faltam:
        raise SystemExit(f"casos inexistentes em banco_casos/banco_casos_extra: {faltam}")
    return [todos[i] for i in ids]


def _particao_so_aprendizado(casos: list[dict]) -> dict:
    """Mesmo formato de evolucao_biblioteca.particionar / executar_fase3b._particao_tudo_avaliacao,
    com todos os casos pedidos em 'aprendizado' (é o ponto: o modelo vê a causa correta e propõe)."""
    return {"regra": "Fase 3-B (sonda de detecção de correção): só os casos corrigidos, todos em "
                     "'aprendizado' — o modelo vê a causa correta e propõe edições sobre uma cópia "
                     "do snapshot de origem.",
            "semente": None, "n_aprendizado": len(casos), "n_avaliacao": 0,
            "casos": {c["id"]: {"particao": "aprendizado", "classe": c["classe"],
                                "nivel": c["nivel"], "hash": None} for c in casos}}


def _imprimir_jsonl(arquivo: Path, titulo: str) -> None:
    print(f"\n===== {titulo}: {arquivo.name} =====")
    if not arquivo.exists():
        print("(arquivo não gravado)")
        return
    for linha in arquivo.read_text(encoding="utf-8").splitlines():
        if not linha.strip():
            continue
        reg = json.loads(linha)
        cabeca = {k: reg[k] for k in ("caso_id", "id", "caso", "particao", "acertou",
                                     "causa_prevista", "causa_raiz", "segundos", "n_aceitas",
                                     "aceitas_no_caso") if k in reg}
        print("\n--", json.dumps(cabeca, ensure_ascii=False))
        for chave in ("resposta", "resposta_crua", "texto", "explicacao", "diagnostico"):
            if isinstance(reg.get(chave), str):
                print(f"[{chave}] {reg[chave][:MAX_TEXTO]}")
        # decisões do validador: qualquer lista de dicts com a chave 'aceita'
        for chave, valor in reg.items():
            if isinstance(valor, list) and valor and isinstance(valor[0], dict) and "aceita" in valor[0]:
                for d in valor:
                    ed = d.get("edicao") or {}
                    print(f"  [{chave}] aceita={d.get('aceita')} rejeicao={d.get('rejeicao') or d.get('codigo') or d.get('motivo_rejeicao')}"
                          f" | operacao={ed.get('operacao')} verbete={ed.get('verbete') or ed.get('alvo')}")
                    for k2 in ("trecho", "texto", "motivo"):
                        if isinstance(ed.get(k2), str):
                            print(f"      {k2}: {ed[k2][:MAX_TEXTO]}")


def _diff_epocas(antes: Path, depois: Path) -> None:
    print(f"\n===== linhas acrescentadas: {antes.name} -> {depois.name} =====")
    arq_antes = {p.relative_to(antes): p for p in antes.rglob("*.md")}
    arq_depois = {p.relative_to(depois): p for p in depois.rglob("*.md")}
    for rel in sorted(arq_depois):
        novo = arq_depois[rel].read_text(encoding="utf-8").splitlines()
        velho = arq_antes[rel].read_text(encoding="utf-8").splitlines() if rel in arq_antes else []
        add = [l for l in difflib.unified_diff(velho, novo, lineterm="", n=0)
               if l.startswith("+") and not l.startswith("+++")]
        if add:
            print(f"\n--- {rel}{' (NOVO)' if rel not in arq_antes else ''}")
            for l in add:
                print("  " + l[:MAX_TEXTO])
    removidos = sorted(set(arq_antes) - set(arq_depois))
    if removidos:
        print("\n!! arquivos removidos (não deveria acontecer):", removidos)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--saida", required=True, help="pasta nova em <RESULTADOS> (nunca 'fase3')")
    ap.add_argument("--modelo", required=True)
    ap.add_argument("--versao", type=int, default=1, help="época lida (snapshot fechado de origem)")
    ap.add_argument("--casos", nargs="+", required=True, help="ids dos casos corrigidos")
    ap.add_argument("--k", type=int, default=3)
    ap.add_argument("--max-tokens-diagnostico", type=int, default=600)
    ap.add_argument("--max-tokens-proposta", type=int, default=700)
    args = ap.parse_args()

    print(caminhos.descricao())
    casos = _casos(args.casos)
    particao = _particao_so_aprendizado(casos)
    c3_of = executar_fase3b._oficial()
    c3b = executar_fase3b.preparar_saida(args.saida, particao)
    slug = executar_fase3._slug(args.modelo)
    pasta, pasta_bib = c3b["raiz"] / slug, c3b["bibliotecas"] / slug
    origem = c3_of["bibliotecas"] / slug / f"epoca-{args.versao}"
    if not origem.exists():
        raise SystemExit(f"sem {origem}")
    pasta.mkdir(parents=True, exist_ok=True)
    digest, versao_ollama = executar_fase3b._preparar_modelo(args.modelo)
    hash_copia = executar_fase3b._preparar_copia(origem, pasta_bib / f"epoca-{args.versao}")
    (c3b["raiz"] / "condicoes_3b.json").write_text(json.dumps({
        "modo": "correcao", "modelo": args.modelo, "versao_lida": args.versao,
        "casos": args.casos, "k": args.k, "condicao": executar_fase3.CONDICAO,
        "hash_snapshot_lido": hash_copia, "versao_ollama": versao_ollama,
        "origem": str(origem)}, ensure_ascii=False, indent=1), encoding="utf-8")
    n = args.versao + 1
    print(f"\nsonda: {args.modelo} lê epoca-{args.versao} (hash {hash_copia}) e roda a época {n} "
          f"só com {args.casos} em aprendizado")

    def _rodar() -> None:
        executar_fase3.rodar_epoca(args.modelo, n, casos, particao, n, args.k,
                                   args.max_tokens_diagnostico, args.max_tokens_proposta,
                                   pasta, pasta_bib, digest, versao_ollama)

    executar_fase3b._com_modelo_descarregado(args.modelo, _rodar)

    _imprimir_jsonl(pasta / f"diagnosticos__L{args.versao}.jsonl", "diagnósticos")
    _imprimir_jsonl(pasta / f"propostas__E{n}.jsonl", "propostas e decisão do validador")
    _diff_epocas(pasta_bib / f"epoca-{args.versao}", pasta_bib / f"epoca-{n}")
    print(f"\nResultados em {c3b['raiz']}")


if __name__ == "__main__":
    main()
