#!/usr/bin/env python3
# ! Alteração de IA - Revisar: experimento OFFLINE do recuperador da biblioteca (29/09/2026, ficha
# 11f decidida pelo Eric: "faça tudo agora"): mede hit@1/3/5 e MRR do verbete de ouro com três
# métodos — o BM25 com sinais determinísticos que a Fase 3 usou, o embedding denso do Ollama e o
# híbrido dos dois por fusão de posições (RRF) — em k = 3 e k = 5, nos 90 casos oficiais e nos 36
# inéditos, lendo as bibliotecas L0 (original), L1 e L3 do qwen2.5:7b; também o hit@3 por classe.
# Nenhum diagnóstico de LLM: só busca. Saída em resultados_alvo/recuperador/ (JSON = registro; MD =
# derivado, com --check).
# ! Motivo: a pendência antiga do recuperador dizia que hit@3 de 79% limitava o acerto (com o verbete
# certo no contexto o acerto ia a 100%) e listava três experimentos baratos e offline — k = 5,
# embedding denso e sinais para a classe de tradução (verbete certo no top-3 em só 47%). O Eric
# mandou fazer agora; o levantamento das LLMs locais (decisão 55) já apontou a recuperação híbrida
# BM25 + embedding pequeno com reordenação para a Fase 4, e este script é a medida que decide se
# ela entra e com que k. O experimento não muda nenhum registro oficial nem base_conhecimento/.
"""Uso (em Programacao/AgenteCore/experimentos, com o Ollama no ar e nenhum outro modelo residente):
  RESULTADOS_DIR=resultados_alvo python experimento_recuperador.py --embedding embeddinggemma:300m
  RESULTADOS_DIR=resultados_alvo python experimento_recuperador.py --check   (regera o .md a partir do .json)
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

import biblioteca as bib
import caminhos
import evolucao_biblioteca as evo
import recuperacao as rec
import taxonomia
from banco_casos import CASOS
from banco_casos_extra import CASOS_EXTRA
from banco_casos_ineditos import CASOS_INEDITOS

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass

F3 = caminhos.fase3("fase3")
SAIDA = caminhos.RESULTADOS / "recuperador"
BIBLIOTECAS = {
    "L0 (original)": F3["bibliotecas"] / "qwen2.5_7b" / "epoca-0",
    "L1 qwen2.5:7b": F3["bibliotecas"] / "qwen2.5_7b" / "epoca-1",
    "L3 qwen2.5:7b": F3["bibliotecas"] / "qwen2.5_7b" / "epoca-3",
}
CONJUNTOS = {"90 oficiais": CASOS + CASOS_EXTRA, "36 inéditos": CASOS_INEDITOS}
KS = (1, 3, 5)
K_RRF = 60  # constante clássica da fusão de posições (Cormack, Clarke e Büttcher, 2009)


# ------------------------------------------------------------------ métodos de busca

def pontuador_bm25(verbetes: list[dict]):
    """O recuperador da Fase 3 como está: BM25 + reforços por endpoint, entidade e status."""
    indice = rec.Indice(verbetes)
    return lambda caso: [v for _, v in rec.pontuar(indice, caso)]


def _cosseno(a: list[float], b: list[float]) -> float:
    num = sum(x * y for x, y in zip(a, b))
    den = math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b))
    return num / den if den else 0.0


class Embutidor:
    """Chama /api/embed do Ollama uma vez por texto distinto (as consultas dos casos são as mesmas
    para as três bibliotecas, e a maior parte dos verbetes também)."""

    def __init__(self, modelo: str):
        import cliente_ollama as oll
        self.oll = oll
        self.modelo = modelo
        self.cache: dict[str, list[float]] = {}
        self.chamadas = 0

    def __call__(self, texto: str) -> list[float]:
        if texto not in self.cache:
            self.cache[texto] = self.oll.embed(self.modelo, texto)
            self.chamadas += 1
        return self.cache[texto]


def texto_natural(caso: dict) -> str:
    """O caso como texto corrido (sintoma, observação, mensagem de erro, requisição), sem a tokenização
    do BM25 — a consulta que um modelo de embedding espera."""
    return " ".join(str(caso.get(k) or "") for k in ("sintoma", "observacao", "mensagem_erro", "requisicao")).strip()


def pontuador_denso(verbetes: list[dict], embutir: Embutidor, consulta: str = "termos"):
    """Cosseno entre o embedding da consulta do caso e o de cada verbete (o mesmo texto indexável do
    BM25). consulta='termos' usa os mesmos termos que o BM25 (a montagem de validar_banco.
    pontuador_embedding); consulta='texto' usa o texto corrido do caso."""
    vetores = [(v, embutir(rec._texto_indexavel(v))) for v in verbetes]

    def pontuar(caso: dict) -> list[dict]:
        q = embutir(texto_natural(caso) if consulta == "texto" else " ".join(rec.sinais_do_caso(caso)["consulta"]))
        return [v for v, _ in sorted(vetores, key=lambda vv: (-_cosseno(q, vv[1]), vv[0]["id"]))]
    return pontuar


def pontuador_hibrido(verbetes: list[dict], p_bm25, p_denso):
    """Fusão de posições (RRF): cada verbete soma 1/(K_RRF + posição) nas duas listas."""
    por_id = {v["id"]: v for v in verbetes}

    def pontuar(caso: dict) -> list[dict]:
        pontos: dict[str, float] = defaultdict(float)
        for ordem in (p_bm25(caso), p_denso(caso)):
            for pos, v in enumerate(ordem, 1):
                pontos[v["id"]] += 1.0 / (K_RRF + pos)
        return [por_id[i] for i, _ in sorted(pontos.items(), key=lambda x: (-x[1], x[0]))]
    return pontuar


# ------------------------------------------------------------------ medição

def medir(verbetes: list[dict], casos: list[dict], pontuador) -> dict:
    r = rec.avaliar_recuperacao(verbetes, casos, ks=KS, pontuador=pontuador)
    por_classe = {}
    for classe in sorted({c["classe"] for c in casos}):
        sub = [c for c in casos if c["classe"] == classe]
        rc = rec.avaliar_recuperacao(verbetes, sub, ks=(3,), pontuador=pontuador)
        por_classe[str(classe)] = {"hit@3": rc["hit@3"], "n": rc["n"]}
    return {**{k: r[k] for k in r if k != "posicao_por_caso"}, "por_classe": por_classe}


def rodar(embedding: str | None) -> dict:
    embutir = Embutidor(embedding) if embedding else None
    linhas = []
    hashes = {}
    for nome_bib, raiz in BIBLIOTECAS.items():
        if not raiz.exists():
            raise SystemExit(f"biblioteca não encontrada: {raiz}")
        verbetes = bib.carregar(raiz)
        hashes[nome_bib] = evo.hash_biblioteca(raiz)
        metodos = {"bm25 (Fase 3)": pontuador_bm25(verbetes)}
        if embutir:
            metodos["denso (termos do BM25)"] = pontuador_denso(verbetes, embutir, "termos")
            metodos["denso (texto do caso)"] = pontuador_denso(verbetes, embutir, "texto")
            metodos["híbrido RRF (bm25 + denso termos)"] = pontuador_hibrido(
                verbetes, metodos["bm25 (Fase 3)"], metodos["denso (termos do BM25)"])
            metodos["híbrido RRF (bm25 + denso texto)"] = pontuador_hibrido(
                verbetes, metodos["bm25 (Fase 3)"], metodos["denso (texto do caso)"])
        for nome_conj, casos in CONJUNTOS.items():
            for nome_met, p in metodos.items():
                m = medir(verbetes, casos, p)
                linhas.append({"biblioteca": nome_bib, "conjunto": nome_conj, "metodo": nome_met, **m})
                print(f'{nome_bib:14} {nome_conj:12} {nome_met:16} hit@1 {m["hit@1"]:5} hit@3 {m["hit@3"]:5} '
                      f'hit@5 {m["hit@5"]:5} mrr {m["mrr"]}')
    return {"metadados": {"gerado_em": datetime.now().isoformat(timespec="seconds"),
                          "embedding": embedding, "chamadas_embed": embutir.chamadas if embutir else 0,
                          "k_rrf": K_RRF, "bibliotecas": hashes,
                          "n_casos": {k: len(v) for k, v in CONJUNTOS.items()}},
            "resultados": linhas}


# ------------------------------------------------------------------ markdown derivado

def _fmt(v, casas: int = 1) -> str:
    return "—" if v is None else (f"{v:.{casas}f}".replace(".", ",") if isinstance(v, float) else str(v))


def _nome_classe(chave: str) -> str:
    v = taxonomia.CLASSES.get(int(chave), chave)
    return v.get("id", str(chave)) if isinstance(v, dict) else str(v)


def render(dado: dict) -> str:
    meta = dado["metadados"]
    partes = [
        "<!-- ! Alteração de IA - Revisar: documento DERIVADO de experimento_recuperador.json, gerado por "
        "experimento_recuperador.py (--check regera e compara); não editar à mão.",
        "     ! Motivo: regra do projeto — nenhum número digitado à mão em Markdown de resultados. -->",
        f"# Experimento do recuperador — {meta['gerado_em'][:10]}",
        "",
        f"Embedding: `{meta['embedding']}` ({meta['chamadas_embed']} chamadas ao /api/embed); fusão de posições "
        f"com k = {meta['k_rrf']}. Bibliotecas: " + "; ".join(f"{k} (hash {v})" for k, v in meta["bibliotecas"].items())
        + ". Casos: " + "; ".join(f"{k} = {v}" for k, v in meta["n_casos"].items()) + ".",
        "",
    ]
    for conj in dict.fromkeys(l["conjunto"] for l in dado["resultados"]):
        partes += [f"## {conj}", "", "| Biblioteca | Método | hit@1 | hit@3 | hit@5 | MRR |", "|---|---|---|---|---|---|"]
        for l in dado["resultados"]:
            if l["conjunto"] == conj:
                partes.append(f'| {l["biblioteca"]} | {l["metodo"]} | {_fmt(l["hit@1"])}% | {_fmt(l["hit@3"])}% | '
                              f'{_fmt(l["hit@5"])}% | {_fmt(l["mrr"], 3)} |')
        partes.append("")
        classes = sorted({c for l in dado["resultados"] if l["conjunto"] == conj for c in l["por_classe"]}, key=int)
        partes += ["### hit@3 por classe", "", "| Biblioteca | Método | " + " | ".join(f"{c} {_nome_classe(c)}" for c in classes) + " |",
                   "|---|---|" + "---|" * len(classes)]
        for l in dado["resultados"]:
            if l["conjunto"] == conj:
                partes.append(f'| {l["biblioteca"]} | {l["metodo"]} | ' + " | ".join(
                    _fmt(l["por_classe"].get(c, {}).get("hit@3")) + "%" for c in classes) + " |")
        partes.append("")
    return "\n".join(partes)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--embedding", default="embeddinggemma:300m",
                    help="modelo de embedding do Ollama ('' desliga o denso e o híbrido)")
    ap.add_argument("--check", action="store_true", help="regera o .md a partir do .json e compara")
    args = ap.parse_args()
    print(caminhos.descricao())
    SAIDA.mkdir(parents=True, exist_ok=True)
    arq_json, arq_md = SAIDA / "experimento_recuperador.json", SAIDA / "experimento_recuperador.md"
    if args.check:
        dado = json.loads(arq_json.read_text(encoding="utf-8"))
        atual = arq_md.read_text(encoding="utf-8") if arq_md.exists() else ""
        if atual == render(dado):
            print(f"--check: {arq_md.name} idêntico ao regerado")
            return
        print(f"--check: {arq_md.name} DIFERE do regerado")
        sys.exit(1)
    dado = rodar(args.embedding or None)
    arq_json.write_text(json.dumps(dado, ensure_ascii=False, indent=2), encoding="utf-8")
    arq_md.write_text(render(dado), encoding="utf-8", newline="\n")
    print(f"gravado: {arq_json} e {arq_md.name} ({len(dado['resultados'])} linhas)")


if __name__ == "__main__":
    main()
