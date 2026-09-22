# ! Alteração de IA - Revisar: script novo (22/09/2026) que integra o levantamento das LLMs locais
# (Workflow `pesquisa-llms-locais`, 8 tópicos) ao Memorial: grava
# `levantamento-2026-09-22-llms-locais.md` (§6.12.1–6.12.8, §6.12.9 rejeitadas/não verificadas,
# §6.12.10 mapa adotado/adiado/descartado), acrescenta o bloco de referências novas em `referencias.md`
# (dedup contra as existentes) e substitui a §7.9 de `ferramental-das-llms-locais.md` pela tabela
# adotado/adiado/descartado; `--check` regera as subseções e compara com o arquivo.
# ! Motivo: é o mesmo desenho de `integrar_pesquisa.py`/`render_levantamento.py` (rodadas 1 e 2): o texto
# das sínteses entra por script, nunca colado à mão, e o que foi descartado fica com o motivo — exigência
# do Eric para o documento final. Reaproveita `render_levantamento.secao` e `bloco_referencias`, trocando
# só a numeração (6.12) e o rótulo das implicações (agente local / Fase 4).
"""Uso:
    python ferramentas/integrar_pesquisa_llms.py --entrada <wf_*.json ou r3-final.json> [--simular]
    python ferramentas/integrar_pesquisa_llms.py --check
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import render_levantamento as rl  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")

RAIZ = rl.RAIZ
DOC_DIR = RAIZ / "Documentacao" / "memorial"
LEVANTAMENTO = DOC_DIR / "2-pesquisa-e-literatura" / "levantamento-2026-09-22-llms-locais.md"
FERRAMENTAL = DOC_DIR / "5-metodo-e-ferramental" / "ferramental-das-llms-locais.md"
MEMORIAL = RAIZ / "Documentacao" / "Memorial de Desenvolvimento.md"
FINAL = rl.SDD / "pesquisa" / "r3-final.json"
DATA = "22/09/2026"
ROTULO = "levantamento de 22/09/2026"

TITULOS_R3 = {
    "r3-prompting-saida-estruturada": "Prompting para modelos pequenos e saída estruturada",
    "r3-inferencia-cpu": "Inferência em CPU com llama.cpp e Ollama",
    "r3-rag-corpus-pequeno": "RAG em corpus pequeno",
    "r3-cache-de-respostas": "Cache de respostas e reuso de computação",
    "r3-modelos-pequenos-2025-2026": "Modelos pequenos de 2025–2026 e português",
    "r3-frameworks-locais": "Estruturas de prompt e de agente para modelos locais",
    "r3-robustez-formato-prompt": "Robustez ao formato do prompt",
    "r3-verificadores-baratos": "Verificadores e autoavaliação baratos",
}
ORDEM_R3 = tuple(TITULOS_R3)
N_REJ = len(ORDEM_R3) + 1
N_MAPA = len(ORDEM_R3) + 2


def carregar(entrada: Path) -> dict:
    """Aceita o arquivo de estado do Workflow (`result`) ou o r3-final.json já normalizado."""
    dados = json.loads(entrada.read_text(encoding="utf-8"))
    if "result" in dados and isinstance(dados["result"], dict):
        dados = dados["result"]
    brutos = dados.get("topicos", [])
    # o Workflow devolve uma lista; o r3-final.json gravado por este script guarda o dicionário por key
    topicos = dict(brutos) if isinstance(brutos, dict) else {t["key"]: t for t in brutos if t}
    for t in topicos.values():
        # o Workflow separa "além do teto" em lista própria e sem acento; o renderizador reconhece
        # a frase acentuada dentro de `rejeitadas`
        for r in t.pop("alem_do_teto", []) or []:
            t.setdefault("rejeitadas", []).append({**r, "motivo": "além do teto de 12 verificações: não verificada"})
    return {"topicos": topicos, "mapa": dados.get("mapa") or {}}


def secao_r3(numero: int, key: str, item: dict) -> str:
    rl.TITULOS_CURTOS.setdefault(key, TITULOS_R3[key])
    texto = rl.secao(numero, key, item)
    texto = texto.replace("#### 6.9.", "#### 6.12.", 1)
    return texto.replace("##### Implicações para a Fase 3", "##### Implicações para o agente local (Fase 4)", 1)


def bloco_rejeitadas_r3(dados: dict) -> str:
    partes = [f"#### 6.12.{N_REJ} Afirmações rejeitadas, não verificadas ou de suporte parcial (com o motivo)", "",
              "Cada linha é uma afirmação que um pesquisador trouxe e o verificador cético não confirmou (fonte inexistente, ano anterior a 2024 sem ser clássico, número ou condição que a fonte não sustenta, fonte que não abriu) ou que ficou além do teto de 12 verificações por tópico. Nenhuma delas entrou nas sínteses; ficam aqui para o descarte ser rastreável.", ""]
    for k in ORDEM_R3:
        it = dados.get(k) or {}
        rej = [r for r in (it.get("rejeitadas") or []) if not rl.eh_alem_do_teto(r)]
        teto = [r for r in (it.get("rejeitadas") or []) if rl.eh_alem_do_teto(r)]
        parciais = [v for v in (it.get("verified") or []) if v.get("support") == "partial"]
        if not rej and not parciais and not teto:
            continue
        partes.append(f"*`{k}`* — {len(rej)} rejeitada(s), {len(parciais)} parcial(is), {len(teto)} não verificada(s)")
        for r in rej:
            partes.append(f"- Rejeitada: {r.get('claim', '')} — *fonte declarada:* {r.get('fonte', '')} — *motivo:* {r.get('motivo', '')}")
        for r in teto:
            partes.append(f"- Não verificada: {r.get('claim', '')} — *fonte declarada:* {r.get('fonte', '')} — *motivo:* {r.get('motivo', '')}")
        for v in parciais:
            partes.append(f"- Parcial: {v.get('claim_pt', '')} — *número que a fonte sustenta:* {v.get('number', '')} — *ref.:* {v.get('ref', '')}")
        partes.append("")
    return "\n".join(partes)


def _cel(s: str) -> str:
    return (s or "").replace("|", "/").replace("\n", " ").strip()


def tabela_mapa(mapa: dict) -> str:
    linhas = ["| Tema | Opção | Veredito | Motivo | Fonte |", "|---|---|---|---|---|"]
    for l in mapa.get("linhas", []):
        linhas.append(f"| {_cel(l['tema'])} | {_cel(l['opcao'])} | **{l['veredito']}** | {_cel(l['motivo_pt'])} | {_cel(l['fonte'])} |")
    return "\n".join(linhas)


def bloco_mapa(mapa: dict) -> str:
    partes = [f"#### 6.12.{N_MAPA} Mapa adotado / adiado / descartado para o agente local", "",
              f"Gerado das 8 sínteses acima ({ROTULO}); a mesma tabela está em [ferramental-das-llms-locais.md](../5-metodo-e-ferramental/ferramental-das-llms-locais.md) (§7.9). *Adotado* = entra na Fase 4 com o modelo decidido (`qwen2.5:7b`, biblioteca L1) e a máquina descrita; *adiado* = só com outra máquina, outro endpoint ou depois da Fase 4; *descartado* = não entra, com o motivo.", "",
              tabela_mapa(mapa), "", "**Riscos para a Fase 4**", "",
              "| Risco | Mitigação | Fonte |", "|---|---|---|"]
    for r in mapa.get("riscos", []):
        partes.append(f"| {_cel(r['risco'])} | {_cel(r['mitigacao'])} | {_cel(r['fonte'])} |")
    partes += ["", "**Leitura**", "", (mapa.get("leitura_pt") or "").strip(), ""]
    return "\n".join(partes)


def contagens(dados: dict) -> list[tuple[str, int, int, int]]:
    return [(k, *rl.contagem(dados.get(k) or {})) for k in ORDEM_R3]


def cabecalho(dados: dict) -> str:
    cont = contagens(dados)
    tot = [sum(c[i] for c in cont) for i in (1, 2, 3)]
    linhas = [
        "<!-- ! Alteração de IA - Revisar: arquivo gerado por ferramentas/integrar_pesquisa_llms.py a partir do resultado do Workflow pesquisa-llms-locais (22/09/2026) — NÃO editar as subseções à mão (o --check compara com o regerado).",
        "     ! Motivo: levantamento pedido pelo Eric em 21/09/2026 sobre repositórios, práticas e arquitetura para melhorar as LLMs locais do agente; cada afirmação passou por verificação cética e o que foi rejeitado ou descartado fica registrado com o motivo (§6.12.9 e §6.12.10). -->",
        "", "# Levantamento bibliográfico — LLMs locais do agente (22/09/2026)", "",
        "Parte do [Memorial de Desenvolvimento](../../Memorial%20de%20Desenvolvimento.md). Continua o [levantamento da Fase 3](levantamento-2026-09-11-fase-3.md) (§6.9) e o [mapa de decisões](mapa-de-decisoes-fase-3.md) (§6.10); a análise decisória do modelo é a §6.11. O veredito por tecnologia (adotado / adiado / descartado) está em §6.12.10 e em [ferramental-das-llms-locais.md](../5-metodo-e-ferramental/ferramental-das-llms-locais.md). Referências completas em [referencias.md](referencias.md).",
        "", "### 6.12 Levantamento das LLMs locais", "",
        f"Oito tópicos, no mesmo fluxo das rodadas anteriores: um pesquisador por tópico (10–16 afirmações com número e condição), até 12 verificadores céticos por tópico (fonte existe? ano ≥ 2024? número e condição batem?) e uma síntese só com o que sobreviveu. Totais: **{tot[0]} aprovadas, {tot[1]} rejeitadas, {tot[2]} não verificadas** (além do teto de 12).",
        "", "| Tópico | Aprovadas | Rejeitadas | Não verificadas |", "|---|---|---|---|",
    ]
    linhas += [f"| `{k}` | {a} | {r} | {t} |" for k, a, r, t in cont]
    return "\n".join(linhas) + "\n"


def render_levantamento(dados: dict, mapa: dict) -> str:
    secoes = [secao_r3(i + 1, k, dados.get(k) or {"titulo": TITULOS_R3[k]}) for i, k in enumerate(ORDEM_R3)]
    return cabecalho(dados) + "\n" + "\n".join(secoes) + "\n" + bloco_rejeitadas_r3(dados) + "\n" + bloco_mapa(mapa)


def bloco_ferramental(mapa: dict) -> str:
    return "\n".join([
        "## 7.9 O que a pesquisa específica cobriu (22/09/2026): adotado, adiado e descartado", "",
        "<!-- ! Alteração de IA - Revisar: seção regravada por ferramentas/integrar_pesquisa_llms.py com o mapa do levantamento das LLMs locais (22/09/2026); antes dizia o que a pesquisa \"vai cobrir\".",
        "     ! Motivo: o levantamento rodou (8 tópicos, verificação cética, sínteses em §6.12); a tabela abaixo é o veredito por tecnologia, com motivo e fonte — é o que o Eric pediu que ficasse documentado, inclusive o descartado. -->",
        "<!-- mapa-llms:inicio -->",
        f"Fonte: [levantamento-2026-09-22-llms-locais.md](../2-pesquisa-e-literatura/levantamento-2026-09-22-llms-locais.md) (§6.12.1–6.12.8: sínteses; §6.12.9: rejeitadas; §6.12.10: este mapa com os riscos e a leitura). *Adotado* = entra na Fase 4 com `qwen2.5:7b`/L1 nesta máquina; *adiado* = depende de outra máquina, outro endpoint ou de a Fase 4 avançar; *descartado* = não entra, pelo motivo dado.", "",
        tabela_mapa(mapa), "",
        "<!-- mapa-llms:fim -->", "",
    ])


def integrar_ferramental(mapa: dict, simular: bool) -> None:
    s = FERRAMENTAL.read_text(encoding="utf-8")
    novo = bloco_ferramental(mapa)
    if "<!-- mapa-llms:inicio -->" in s:
        s2 = re.sub(r"## 7\.9 .*?<!-- mapa-llms:fim -->\n\n?", novo, s, count=1, flags=re.S)
    else:
        m = re.search(r"^## 7\.9 .*$", s, re.M)
        assert m, "§7.9 não encontrada"
        s2 = s[:m.start()] + novo
    if not simular and s2 != s:
        FERRAMENTAL.write_text(s2, encoding="utf-8")
    print(f"ferramental §7.9: {'simulado' if simular else 'gravado'} ({len(mapa.get('linhas', []))} linhas)")


def integrar_referencias(dados: dict, simular: bool) -> None:
    texto, quase = rl.bloco_referencias(dados, ORDEM_R3, ROTULO)
    texto = texto.replace(f"### Rodada 2 do levantamento ({ROTULO})", f"### Levantamento das LLMs locais ({ROTULO})", 1)
    texto = texto.replace("a partir das sínteses da rodada 2", "a partir das sínteses do levantamento das LLMs locais (integrar_pesquisa_llms.py)", 1)
    n_novas = sum(1 for l in texto.splitlines() if l.startswith("- "))
    atual = rl.REFERENCIAS.read_text(encoding="utf-8")
    if f"### Levantamento das LLMs locais ({ROTULO})" in atual:
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
    if "levantamento-2026-09-22-llms-locais.md" in s:
        print("Memorial: índice já tem a linha"); return
    m = re.search(r"^- \[Mapa de decisões[^\n]*\n", s, re.M)
    assert m, "linha do mapa no índice do Memorial não encontrada"
    linha = ("<!-- ! Alteração de IA - Revisar: linha nova no índice (22/09/2026) para o levantamento das LLMs locais (§6.12). ! Motivo: gerado por integrar_pesquisa_llms.py; sem a linha o índice não leva ao levantamento nem ao mapa adotado/descartado. -->\n"
             "- [Levantamento — LLMs locais do agente (22/09/2026)](memorial/2-pesquisa-e-literatura/levantamento-2026-09-22-llms-locais.md) — §6.12: prompting e saída estruturada, inferência em CPU, RAG em corpus pequeno, cache de respostas, modelos pequenos de 2025–2026 e português, estruturas de prompt e de agente, robustez ao formato, verificadores baratos; §6.12.9 rejeitadas com motivo; §6.12.10 mapa adotado / adiado / descartado para a Fase 4.\n")
    s2 = s[:m.end()] + linha + s[m.end():]
    if not simular:
        MEMORIAL.write_text(s2, encoding="utf-8")
    print("Memorial: linha do índice " + ("simulada" if simular else "gravada"))


def check() -> int:
    if not FINAL.exists() or not LEVANTAMENTO.exists():
        print("--check: nada integrado ainda"); return 1
    entrada = carregar(FINAL)
    esperado = render_levantamento(entrada["topicos"], entrada["mapa"])
    atual = LEVANTAMENTO.read_text(encoding="utf-8")
    e, a = rl._normalizar(esperado), rl._normalizar(atual)
    if e == a:
        print("--check: levantamento das LLMs locais idêntico ao regerado"); return 0
    import difflib
    print("--check: DIFERE"); print("\n".join(list(difflib.unified_diff(a, e, lineterm=""))[:30])); return 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--entrada", default=str(FINAL))
    ap.add_argument("--simular", action="store_true")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    if args.check:
        return check()
    entrada = carregar(Path(args.entrada))
    dados, mapa = entrada["topicos"], entrada["mapa"]
    faltam = [k for k in ORDEM_R3 if k not in dados or not (dados[k].get("synthesis"))]
    print(f"tópicos com síntese: {len(ORDEM_R3) - len(faltam)}/{len(ORDEM_R3)}" + (f" — sem síntese: {faltam}" if faltam else ""))
    print("mapa:", len(mapa.get("linhas", [])), "linhas,", len(mapa.get("riscos", [])), "riscos")
    for k, a, r, t in contagens(dados):
        print(f"  {k}: {a} aprovadas, {r} rejeitadas, {t} não verificadas")
    texto = render_levantamento(dados, mapa)
    if args.simular:
        print(f"levantamento: {len(texto)} caracteres (simulado)")
    else:
        FINAL.parent.mkdir(parents=True, exist_ok=True)
        FINAL.write_text(json.dumps({"topicos": dados, "mapa": mapa}, ensure_ascii=False, indent=1), encoding="utf-8")
        LEVANTAMENTO.write_text(texto, encoding="utf-8")
        print(f"levantamento gravado: {LEVANTAMENTO.name} ({len(texto)} caracteres)")
    integrar_referencias(dados, args.simular)
    integrar_ferramental(mapa, args.simular)
    integrar_memorial(args.simular)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
