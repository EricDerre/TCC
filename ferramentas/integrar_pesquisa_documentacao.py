#!/usr/bin/env python3
# ! Alteração de IA - Revisar: script novo (29/09/2026) que integra o levantamento sobre a qualidade da
# documentação autogerida (rodada 4: 8 tópicos pesquisados por agentes, verificação cética e síntese) ao
# Memorial: `--montar` junta os arquivos por tópico de `.superpowers/sdd/fase3b-e-fechamento/pesquisa/r4/`
# (<key>.pesquisa.json, <key>.verificacao.json, <key>.sintese.json e mapa.json) em `r4-final.json` com a
# mesma forma do r3-final.json; a integração grava `levantamento-2026-09-29-documentacao-autogerida.md`
# (§6.13.1–6.13.8, §6.13.9 rejeitadas/não verificadas, §6.13.10 mapa de filtros adotado/adiado/descartado),
# acrescenta o bloco de referências novas em `referencias.md` (dedup) e a linha no índice do Memorial;
# `--check` regera e compara.
# ! Motivo: pedido do Eric em 29/09/2026 (ficha 2): "pesquisas de literatura e estudos sobre como melhorar
# as saídas da documentação autogerida e evitar alucinações", com filtros na geração e na gestão. Mesmo
# desenho de integrar_pesquisa_llms.py (rodada 3): o texto entra por script, nunca colado à mão, e o que
# foi rejeitado fica com o motivo. A rodada 4 rodou por agentes avulsos (não por Workflow), então este
# script também faz a montagem que o Workflow fazia — a regra de "verificada" é a mesma do pesquisa-llms-
# locais.js: só suporte yes/partial, fonte existente e ano válido entram na síntese.
"""Uso:
    python ferramentas/integrar_pesquisa_documentacao.py --montar            (gera r4-final.json e as listas para a síntese)
    python ferramentas/integrar_pesquisa_documentacao.py [--simular]         (integra ao Memorial)
    python ferramentas/integrar_pesquisa_documentacao.py --check
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import integrar_pesquisa_llms as ipl  # noqa: E402
import render_levantamento as rl  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")

RAIZ = rl.RAIZ
DOC_DIR = RAIZ / "Documentacao" / "memorial"
LEVANTAMENTO = DOC_DIR / "2-pesquisa-e-literatura" / "levantamento-2026-09-29-documentacao-autogerida.md"
MEMORIAL = RAIZ / "Documentacao" / "Memorial de Desenvolvimento.md"
R4 = rl.SDD / "pesquisa" / "r4"
FINAL = rl.SDD / "pesquisa" / "r4-final.json"
ROTULO = "levantamento de 29/09/2026"

TITULOS_R4 = {
    "r4-alucinacao-em-documentacao-gerada": "Alucinação em documentação e conhecimento gerados por LLM",
    "r4-verificacao-e-autocritica": "Verificação, autocrítica e refinamento da própria saída em modelos pequenos",
    "r4-admissao-e-curadoria-de-memoria": "Admissão, consolidação e curadoria de memória escrita pelo próprio agente",
    "r4-fundamentacao-e-atribuicao": "Fundamentação em fontes, atribuição e medidas de fidelidade",
    "r4-restricao-de-formato-e-validadores": "Modelos de saída, esquemas e validadores programáticos",
    "r4-abstencao-e-confianca": "Abstenção, confiança e quando não escrever",
    "r4-manutencao-de-documentacao-por-llm": "Manutenção e atualização de documentação por LLM",
    "r4-avaliacao-da-qualidade-de-documentacao": "Medidas de qualidade de documentação gerada e juízes automáticos",
}
ORDEM_R4 = tuple(TITULOS_R4)
N_REJ = len(ORDEM_R4) + 1
N_MAPA = len(ORDEM_R4) + 2


# ------------------------------------------------------------------ montagem (o que o Workflow fazia)

def _para_verificada(c: dict, d: dict) -> dict:
    return {"claim_pt": c.get("claim_pt", ""), "number": d.get("corrected_number") or c.get("number", ""),
            "condition": c.get("condition", ""), "support": d.get("claim_supported"),
            "ref": d.get("corrected_citation") or "", "url": c.get("url", ""),
            "relevance": c.get("relevance_to_project_pt", "")}


def _para_rejeitada(c: dict, d: dict | None, motivo: str) -> dict:
    fonte = f'{c.get("authors", "")}. {c.get("source_title", "")}. {c.get("venue", "")}, {c.get("year", "")}. {c.get("url", "")}'.strip()
    return {"claim": c.get("claim_pt", ""), "fonte": fonte, "motivo": motivo if d is None else f'{motivo}: {d.get("notes_pt", "")}'.strip(": ")}


def montar_topico(key: str) -> dict:
    pesq = json.loads((R4 / f"{key}.pesquisa.json").read_text(encoding="utf-8"))
    arq_ver = R4 / f"{key}.verificacao.json"
    vereditos = {}
    if arq_ver.exists():
        for v in json.loads(arq_ver.read_text(encoding="utf-8")).get("vereditos", []):
            vereditos[int(v["indice"])] = v
    verified, rejeitadas = [], []
    for i, c in enumerate(pesq.get("claims", [])):
        d = vereditos.get(i)
        if d is None:
            rejeitadas.append(_para_rejeitada(c, None, "não verificada (sem veredito do verificador)"))
        elif not d.get("exists"):
            rejeitadas.append(_para_rejeitada(c, d, "fonte não encontrada"))
        elif not d.get("year_ok"):
            rejeitadas.append(_para_rejeitada(c, d, "ano anterior a 2024 sem ser fonte clássica"))
        elif d.get("claim_supported") in ("yes", "partial"):
            verified.append(_para_verificada(c, d))
        elif d.get("claim_supported") == "no":
            rejeitadas.append(_para_rejeitada(c, d, "a fonte não sustenta o número ou a condição"))
        else:
            rejeitadas.append(_para_rejeitada(c, d, "não verificável (fonte não abriu)"))
    arq_sin = R4 / f"{key}.sintese.json"
    synthesis = json.loads(arq_sin.read_text(encoding="utf-8")) if arq_sin.exists() else None
    return {"key": key, "titulo": TITULOS_R4[key], "prompt": pesq.get("titulo", ""),
            "pesquisa": {"summary_pt": pesq.get("summary_pt", ""), "n_claims": len(pesq.get("claims", []))},
            "verified": verified, "rejeitadas": rejeitadas, "synthesis": synthesis,
            "open_questions": pesq.get("open_questions_pt", [])}


def _linha_verificada(v: dict, i: int) -> str:
    return (f'{i + 1}. {v["claim_pt"]} [número: {v["number"]}; condição: {v["condition"]}; suporte: {v["support"]}] '
            f'REF: {v["ref"]}' + (f' | relevância: {v["relevance"]}' if v.get("relevance") else ""))


def montar() -> dict:
    topicos = {}
    for key in ORDEM_R4:
        if not (R4 / f"{key}.pesquisa.json").exists():
            print(f"  {key}: sem pesquisa"); continue
        t = montar_topico(key)
        topicos[key] = t
        # lista numerada das verificadas, para o agente de síntese ler (nunca o JSON inteiro)
        (R4 / f"{key}.verificadas.txt").write_text(
            "\n".join(_linha_verificada(v, i) for i, v in enumerate(t["verified"])) or "(nenhuma sobreviveu)",
            encoding="utf-8")
        print(f"  {key}: {len(t['verified'])} verificadas, {len(t['rejeitadas'])} rejeitadas/não verificadas, "
              f"síntese {'sim' if t['synthesis'] else 'não'}")
    arq_mapa = R4 / "mapa.json"
    mapa = json.loads(arq_mapa.read_text(encoding="utf-8")) if arq_mapa.exists() else {}
    dado = {"topicos": topicos, "mapa": mapa}
    FINAL.write_text(json.dumps(dado, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"gravado: {FINAL.name} ({len(topicos)} tópicos; mapa com {len(mapa.get('linhas', []))} linhas)")
    return dado


# ------------------------------------------------------------------ render (mesmas peças da rodada 3)

def secao_r4(numero: int, key: str, item: dict) -> str:
    rl.TITULOS_CURTOS.setdefault(key, TITULOS_R4[key])
    texto = rl.secao(numero, key, item)
    texto = texto.replace("#### 6.9.", "#### 6.13.", 1)
    return texto.replace("##### Implicações para a Fase 3", "##### Implicações para a biblioteca autogerida (Fase 4)", 1)


def bloco_rejeitadas_r4(dados: dict) -> str:
    partes = [f"#### 6.13.{N_REJ} Afirmações rejeitadas, não verificadas ou de suporte parcial (com o motivo)", "",
              "Cada linha é uma afirmação que um pesquisador trouxe e o verificador cético não confirmou (fonte inexistente, ano anterior a 2024 sem ser clássico, número ou condição que a fonte não sustenta, fonte que não abriu). Nenhuma delas entrou nas sínteses; ficam aqui para o descarte ser rastreável.", ""]
    for k in ORDEM_R4:
        it = dados.get(k) or {}
        rej = it.get("rejeitadas") or []
        parciais = [v for v in (it.get("verified") or []) if v.get("support") == "partial"]
        if not rej and not parciais:
            continue
        partes.append(f"*`{k}`* — {len(rej)} rejeitada(s)/não verificada(s), {len(parciais)} parcial(is)")
        for r in rej:
            partes.append(f"- Rejeitada: {r.get('claim', '')} — *fonte declarada:* {r.get('fonte', '')} — *motivo:* {r.get('motivo', '')}")
        for v in parciais:
            partes.append(f"- Parcial: {v.get('claim_pt', '')} — *número que a fonte sustenta:* {v.get('number', '')} — *ref.:* {v.get('ref', '')}")
        partes.append("")
    return "\n".join(partes)


def bloco_mapa_r4(mapa: dict) -> str:
    partes = [f"#### 6.13.{N_MAPA} Filtros para a documentação autogerida: adotado / adiado / descartado", "",
              f"Gerado das 8 sínteses acima ({ROTULO}). Cada linha é um filtro candidato para a GERAÇÃO ou a GESTÃO da documentação que o modelo escreve na biblioteca: *adotado* = entra no desenho da Fase 4 com `qwen2.5:7b` nesta máquina, além da revisão humana que continua; *adiado* = depende de medir custo no i5, de outro modelo ou de a Fase 4 avançar; *descartado* = não entra, com o motivo. A coluna Tema diz se o filtro age na geração (o que o modelo escreve) ou na gestão (admissão, revisão, atualização, correção).", "",
              ipl.tabela_mapa(mapa), "", "**Riscos**", "", "| Risco | Mitigação | Fonte |", "|---|---|---|"]
    for r in mapa.get("riscos", []):
        partes.append(f"| {ipl._cel(r['risco'])} | {ipl._cel(r['mitigacao'])} | {ipl._cel(r['fonte'])} |")
    partes += ["", "**Leitura**", "", (mapa.get("leitura_pt") or "").strip(), ""]
    return "\n".join(partes)


def contagens(dados: dict) -> list[tuple[str, int, int, int]]:
    return [(k, *rl.contagem(dados.get(k) or {})) for k in ORDEM_R4]


def cabecalho(dados: dict) -> str:
    cont = contagens(dados)
    tot = [sum(c[i] for c in cont) for i in (1, 2, 3)]
    linhas = [
        "<!-- ! Alteração de IA - Revisar: arquivo gerado por ferramentas/integrar_pesquisa_documentacao.py a partir da rodada 4 de pesquisa (29/09/2026) — NÃO editar as subseções à mão (o --check compara com o regerado).",
        "     ! Motivo: levantamento pedido pelo Eric em 29/09/2026 (ficha 2 de pendencias.md): como melhorar a documentação que o próprio modelo escreve na biblioteca e evitar alucinação, com filtros na geração e na gestão; cada afirmação passou por verificação cética e o que foi rejeitado ou descartado fica registrado com o motivo (§6.13.9 e §6.13.10). -->",
        "", "# Levantamento bibliográfico — qualidade da documentação autogerida (29/09/2026)", "",
        "Parte do [Memorial de Desenvolvimento](../../Memorial%20de%20Desenvolvimento.md). Continua o [levantamento da Fase 3](levantamento-2026-09-11-fase-3.md) (§6.9), o [mapa de decisões](mapa-de-decisoes-fase-3.md) (§6.10) e o [levantamento das LLMs locais](levantamento-2026-09-22-llms-locais.md) (§6.12). O que motivou: na Fase 3 o modelo escolhido ganhou acerto com a própria biblioteca, mas 41% das edições aceitas eram erradas e a maioria das corretas, redundantes (análise decisória §8); a sonda de 28/09/2026 mostrou que ele não percebe uma correção feita no sistema (roadmap §3). Referências completas em [referencias.md](referencias.md).",
        "", "### 6.13 Levantamento sobre a documentação autogerida", "",
        f"Oito tópicos, no mesmo fluxo das rodadas anteriores, agora com agentes avulsos em vez de um Workflow: um pesquisador por tópico (10–16 afirmações com número e condição), um verificador cético por tópico (fonte existe? ano ≥ 2024? número e condição batem?) e uma síntese só com o que sobreviveu. Totais: **{tot[0]} aprovadas, {tot[1]} rejeitadas, {tot[2]} não verificadas**.",
        "", "| Tópico | Aprovadas | Rejeitadas | Não verificadas |", "|---|---|---|---|",
    ]
    linhas += [f"| `{k}` | {a} | {r} | {t} |" for k, a, r, t in cont]
    return "\n".join(linhas) + "\n"


def render(dados: dict, mapa: dict) -> str:
    secoes = [secao_r4(i + 1, k, dados.get(k) or {"titulo": TITULOS_R4[k]}) for i, k in enumerate(ORDEM_R4)]
    return cabecalho(dados) + "\n" + "\n".join(secoes) + "\n" + bloco_rejeitadas_r4(dados) + "\n" + bloco_mapa_r4(mapa)


def integrar_referencias(dados: dict, simular: bool) -> None:
    texto, quase = rl.bloco_referencias(dados, ORDEM_R4, ROTULO)
    texto = texto.replace(f"### Rodada 2 do levantamento ({ROTULO})", f"### Levantamento da documentação autogerida ({ROTULO})", 1)
    texto = texto.replace("a partir das sínteses da rodada 2", "a partir das sínteses do levantamento da documentação autogerida (integrar_pesquisa_documentacao.py)", 1)
    n_novas = sum(1 for l in texto.splitlines() if l.startswith("- "))
    atual = rl.REFERENCIAS.read_text(encoding="utf-8")
    if f"### Levantamento da documentação autogerida ({ROTULO})" in atual:
        print(f"referências: bloco já existe ({n_novas} novas ao regerar); não regravado")
    elif not simular:
        rl.REFERENCIAS.write_text(atual.rstrip("\n") + "\n\n" + texto, encoding="utf-8")
        print(f"referências: +{n_novas} novas")
    else:
        print(f"referências: {n_novas} novas (simulado)")
    for q in quase:
        print("  quase-duplicata (conferir):", q)


def integrar_memorial(simular: bool) -> None:
    s = MEMORIAL.read_text(encoding="utf-8")
    if "levantamento-2026-09-29-documentacao-autogerida.md" in s:
        print("Memorial: índice já tem a linha"); return
    m = re.search(r"^- \[Levantamento — LLMs locais[^\n]*\n", s, re.M)
    assert m, "linha do levantamento das LLMs locais no índice do Memorial não encontrada"
    linha = ("<!-- ! Alteração de IA - Revisar: linha nova no índice (29/09/2026) para o levantamento sobre a documentação autogerida (§6.13). ! Motivo: gerado por integrar_pesquisa_documentacao.py; sem a linha o índice não leva ao levantamento nem ao mapa de filtros. -->\n"
             "- [Levantamento — qualidade da documentação autogerida (29/09/2026)](memorial/2-pesquisa-e-literatura/levantamento-2026-09-29-documentacao-autogerida.md) — §6.13: alucinação em documentação gerada, verificação e autocrítica, admissão e curadoria de memória, fundamentação e atribuição, esquemas e validadores, abstenção e confiança, manutenção de documentação, medidas de qualidade; §6.13.9 rejeitadas com motivo; §6.13.10 filtros adotados / adiados / descartados para a geração e a gestão da biblioteca.\n")
    s2 = s[:m.end()] + linha + s[m.end():]
    if not simular:
        MEMORIAL.write_text(s2, encoding="utf-8")
    print("Memorial: linha do índice " + ("simulada" if simular else "gravada"))


def check() -> int:
    if not FINAL.exists() or not LEVANTAMENTO.exists():
        print("--check: nada integrado ainda"); return 1
    entrada = json.loads(FINAL.read_text(encoding="utf-8"))
    esperado = render(entrada["topicos"], entrada["mapa"])
    atual = LEVANTAMENTO.read_text(encoding="utf-8")
    e, a = rl._normalizar(esperado), rl._normalizar(atual)
    if e == a:
        print("--check: levantamento da documentação autogerida idêntico ao regerado"); return 0
    import difflib
    print("--check: DIFERE"); print("\n".join(list(difflib.unified_diff(a, e, lineterm=""))[:30])); return 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--montar", action="store_true", help="junta pesquisa + verificação + síntese em r4-final.json")
    ap.add_argument("--simular", action="store_true")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    if args.check:
        return check()
    if args.montar:
        montar(); return 0
    entrada = json.loads(FINAL.read_text(encoding="utf-8"))
    dados, mapa = entrada["topicos"], entrada["mapa"]
    faltam = [k for k in ORDEM_R4 if k not in dados or not (dados[k].get("synthesis"))]
    print(f"tópicos com síntese: {len(ORDEM_R4) - len(faltam)}/{len(ORDEM_R4)}" + (f" — sem síntese: {faltam}" if faltam else ""))
    print("mapa:", len(mapa.get("linhas", [])), "linhas,", len(mapa.get("riscos", [])), "riscos")
    if faltam or not mapa.get("linhas"):
        raise SystemExit("integração exige as 8 sínteses e o mapa — rode --montar depois de gravá-los")
    for k, a, r, t in contagens(dados):
        print(f"  {k}: {a} aprovadas, {r} rejeitadas, {t} não verificadas")
    texto = render(dados, mapa)
    if args.simular:
        print(f"levantamento: {len(texto)} caracteres (simulado)")
    else:
        LEVANTAMENTO.write_text(texto, encoding="utf-8")
        print(f"levantamento gravado: {LEVANTAMENTO.name} ({len(texto)} caracteres)")
    integrar_referencias(dados, args.simular)
    integrar_memorial(args.simular)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
