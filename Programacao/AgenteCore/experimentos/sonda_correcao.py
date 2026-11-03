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
# ! Alteração de IA - Revisar: (03/11/2026, Fase 4, pacote P5) a sonda pode ser chamada de novo com a recuperação
# por id ligada (`--recuperacao-por-id`: biblioteca_fase4.com_recuperacao_por_id troca, só durante a sonda, o
# contexto_e_prompt do executor congelado para acrescentar os verbetes ligados ao caso pelo id) e lendo outra
# biblioteca de origem (`--origem <pasta de uma época fechada>`, por exemplo a época de correções da corrida 20);
# o que a sonda fazia em main() saiu para rodar_sonda(), que o modo `biblioteca` de executar_fase4.py chama na
# mesma sessão do Ollama, e resumo_da_sonda() resume os registros (rótulo, acerto, propostas, aceitas, motivos,
# abstenção, se a resposta menciona a correção, os verbetes que vieram pelo id) para o avaliador.
# ! Motivo: plano aprovado, P5 ("a sonda de 28/09 repetida com recuperação por id muda o que o modelo propõe"):
# a leitura de 28/09 (roadmap §3) disse que a busca por palavras não trouxe as notas do caso; repetir a mesma sonda
# com só esse ponto mudado é o que mede a diferença.
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
MARCAS_DE_CORRECAO = ("solucao aplicada", "solucao sugerida", "corrigid", "nao ocorre mais", "deixou de ocorrer", "ja registra",
                      "ja esta documentad", "ja foi resolvid", "ja esta corrig")


def menciona_correcao(texto: str) -> bool:
    """A resposta do modelo (diagnóstico ou proposta) fala da correção registrada na documentação?"""
    import biblioteca as bib
    norm = bib.normalizar(texto or "")
    return any(m in norm for m in MARCAS_DE_CORRECAO)


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


def montar_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--saida", required=True, help="pasta nova em <RESULTADOS> (nunca 'fase3')")
    ap.add_argument("--modelo", required=True)
    ap.add_argument("--versao", type=int, default=1, help="época lida (snapshot fechado de origem)")
    ap.add_argument("--casos", nargs="+", required=True, help="ids dos casos corrigidos")
    ap.add_argument("--k", type=int, default=3)
    ap.add_argument("--max-tokens-diagnostico", type=int, default=600)
    ap.add_argument("--max-tokens-proposta", type=int, default=700)
    ap.add_argument("--recuperacao-por-id", action="store_true",
                    help="P5: os verbetes ligados ao caso pelo id entram no contexto depois dos k da busca")
    ap.add_argument("--origem", default=None,
                    help="P5: pasta de uma época fechada a ler no lugar de fase3/bibliotecas/<modelo>/epoca-<versao>")
    return ap


def rodar_sonda(modelo: str, casos: list[dict], origem: Path, versao: int, pasta: Path, pasta_bib: Path, k: int, mt_diag: int, mt_prop: int,
                digest: str, versao_ollama: str | None, recuperacao_por_id: bool = False) -> dict:
    """Uma época de aprendizado do executor congelado sobre uma cópia da época de origem, só com `casos` em
    aprendizado (o modelo vê a causa correta e propõe), com ou sem a recuperação por id; devolve os caminhos dos
    JSONL e o resumo. Quem chama já preparou o modelo (um por vez) e descarrega depois."""
    import biblioteca_fase4 as bf
    particao = _particao_so_aprendizado(casos)
    pasta.mkdir(parents=True, exist_ok=True)
    hash_copia = executar_fase3b._preparar_copia(origem, pasta_bib / f"epoca-{versao}")
    n = versao + 1
    if recuperacao_por_id:
        with bf.com_recuperacao_por_id():
            executar_fase3.rodar_epoca(modelo, n, casos, particao, n, k, mt_diag, mt_prop, pasta, pasta_bib, digest, versao_ollama)
    else:
        executar_fase3.rodar_epoca(modelo, n, casos, particao, n, k, mt_diag, mt_prop, pasta, pasta_bib, digest, versao_ollama)
    arq_diag, arq_prop = pasta / f"diagnosticos__L{versao}.jsonl", pasta / f"propostas__E{n}.jsonl"
    return {"hash_lido": hash_copia, "epoca": n, "diagnosticos": arq_diag, "propostas": arq_prop,
            "resumo": resumo_da_sonda(arq_diag, arq_prop, k, recuperacao_por_id)}


def resumo_da_sonda(arq_diag: Path, arq_prop: Path, k: int, recuperacao_por_id: bool) -> list[dict]:
    """Por caso: rótulo e acerto do diagnóstico, as propostas (quantas, aceitas, motivos de recusa, abstenção), se a
    resposta menciona a correção registrada e quais verbetes vieram pelo id (os que ficaram depois dos k da busca)."""
    import executar_bateria
    import avaliar
    diag = {r["caso"]: r for r in executar_bateria.ler_jsonl(arq_diag)}
    prop = {r["caso"]: r for r in executar_bateria.ler_jsonl(arq_prop)}
    saida = []
    for cid, d in diag.items():
        p_ = prop.get(cid) or {}
        rotulo = avaliar.extrair(d.get("resposta", ""))["causa_raiz"]
        gabarito = (d.get("gabarito") or {}).get("causa_raiz")
        acertou = rotulo is not None and gabarito is not None and avaliar._normalizar(rotulo) == avaliar._normalizar(gabarito)
        ids = d.get("verbetes_ids") or []
        saida.append({"caso": cid, "rotulo": rotulo, "acertou": acertou, "n_propostas": p_.get("n_propostas", 0), "n_aceitas": p_.get("n_aceitas", 0),
                      "abstencao": bool(p_.get("nenhuma")), "motivos": list(p_.get("motivos_rejeicao") or []),
                      "menciona_correcao": menciona_correcao(d.get("resposta", "")) or menciona_correcao(p_.get("resposta", "")),
                      "por_id": ids[k:] if recuperacao_por_id else [], "verbetes_ids": ids,
                      "segundos": round((d.get("segundos") or 0) + (p_.get("segundos") or 0), 2),
                      "decisoes": [{"operacao": x.get("operacao"), "verbete": x.get("verbete"), "aceita": x.get("aceita"), "motivo": x.get("motivo")}
                                   for x in p_.get("decisoes") or []]})
    return saida


def main() -> None:
    args = montar_parser().parse_args()

    print(caminhos.descricao())
    casos = _casos(args.casos)
    particao = _particao_so_aprendizado(casos)
    c3_of = executar_fase3b._oficial()
    c3b = executar_fase3b.preparar_saida(args.saida, particao)
    slug = executar_fase3._slug(args.modelo)
    pasta, pasta_bib = c3b["raiz"] / slug, c3b["bibliotecas"] / slug
    origem = Path(args.origem) if args.origem else c3_of["bibliotecas"] / slug / f"epoca-{args.versao}"
    if not origem.exists():
        raise SystemExit(f"sem {origem}")
    pasta.mkdir(parents=True, exist_ok=True)
    digest, versao_ollama = executar_fase3b._preparar_modelo(args.modelo)
    n = args.versao + 1
    resultado: dict = {}

    def _rodar() -> None:
        resultado.update(rodar_sonda(args.modelo, casos, origem, args.versao, pasta, pasta_bib, args.k, args.max_tokens_diagnostico,
                                     args.max_tokens_proposta, digest, versao_ollama, recuperacao_por_id=args.recuperacao_por_id))

    (c3b["raiz"] / "condicoes_3b.json").write_text(json.dumps({
        "modo": "correcao", "modelo": args.modelo, "versao_lida": args.versao,
        "casos": args.casos, "k": args.k, "condicao": executar_fase3.CONDICAO,
        "recuperacao_por_id": args.recuperacao_por_id, "versao_ollama": versao_ollama,
        "origem": str(origem)}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\nsonda: {args.modelo} lê {origem.name} e roda a época {n} só com {args.casos} em aprendizado"
          f"{' (recuperação por id ligada)' if args.recuperacao_por_id else ''}")
    executar_fase3b._com_modelo_descarregado(args.modelo, _rodar)

    _imprimir_jsonl(pasta / f"diagnosticos__L{args.versao}.jsonl", "diagnósticos")
    _imprimir_jsonl(pasta / f"propostas__E{n}.jsonl", "propostas e decisão do validador")
    _diff_epocas(pasta_bib / f"epoca-{args.versao}", pasta_bib / f"epoca-{n}")
    (c3b["raiz"] / "sonda.json").write_text(json.dumps(resultado.get("resumo", []), ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nResultados em {c3b['raiz']}")


if __name__ == "__main__":
    main()
