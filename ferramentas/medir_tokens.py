# ! Alteração de IA - Revisar: script novo (21/09/2026) que soma o consumo de tokens do Claude Code a partir dos
# transcritos locais (`~/.claude/projects/<slug>/*.jsonl` e `subagents/**/*.jsonl`), por dia, modelo e tipo de agente.
# ! Motivo: o plano complementar exige medir "antes e depois" das medidas de economia de tokens; `/usage` e `/insights`
# são interativos e não guardam histórico por dia, e o `ccusage` (npm) faria a mesma leitura destes arquivos — é
# processamento local, sem custo de tokens, como o Eric pediu.
"""Uso: python ferramentas/medir_tokens.py [--projeto SLUG] [--desde AAAA-MM-DD] [--ate AAAA-MM-DD] [--json saida.json]
                                         [--agentes ROTULO=ID,ROTULO=ID,...]

Cada linha `assistant` de um transcrito traz `message.usage` (input, cache_creation, cache_read, output). A mesma
resposta aparece em várias linhas (uma por bloco de conteúdo), com o mesmo `message.id`: conta-se uma vez por id.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from collections import defaultdict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

RAIZ_PROJETOS = Path.home() / ".claude" / "projects"
CAMPOS = ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens", "output_tokens")


def _pasta_projeto(slug: str | None) -> Path:
    if slug:
        return RAIZ_PROJETOS / slug
    # o slug do Claude Code troca todo caractere não alfanumérico do caminho do repositório por "-"
    caminho = os.getcwd()
    slug = "".join(c if c.isalnum() else "-" for c in caminho)
    return RAIZ_PROJETOS / slug


def _tipo(arquivo: Path) -> str:
    partes = arquivo.as_posix()
    if "/workflows/" in partes:
        return "workflow"
    if "/subagents/" in partes:
        return "subagente"
    return "principal"


# ! Alteração de IA - Revisar: `ler_usos` aceita uma lista de arquivos (29/09/2026); sem ela, lê a pasta inteira como antes.
# ! Motivo: a soma por subagente (`--agentes`) precisa ler só os transcritos `agent-<id>.jsonl` pedidos, com a mesma
# regra de contar cada resposta uma vez por message.id, em vez de duplicar a leitura noutra função.
def ler_usos(pasta: Path, arquivos: list[Path] | None = None) -> list[dict]:
    """Uma entrada por resposta do modelo (deduplicada por message.id)."""
    usos: list[dict] = []
    vistos: set[str] = set()
    for arquivo in sorted(arquivos if arquivos is not None else pasta.rglob("*.jsonl")):
        tipo = _tipo(arquivo)
        try:
            linhas = arquivo.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        for linha in linhas:
            if '"usage"' not in linha:
                continue
            try:
                r = json.loads(linha)
            except json.JSONDecodeError:
                continue
            m = r.get("message")
            if not isinstance(m, dict) or not isinstance(m.get("usage"), dict):
                continue
            chave = m.get("id") or r.get("uuid") or f"{arquivo}:{len(usos)}"
            if chave in vistos:
                continue
            vistos.add(chave)
            u = m["usage"]
            usos.append({
                "dia": (r.get("timestamp") or "")[:10],
                "modelo": m.get("model") or "?",
                "tipo": tipo,
                "plugin": r.get("attributionPlugin") or "",
                "skill": r.get("attributionSkill") or "",
                **{c: int(u.get(c) or 0) for c in CAMPOS},
            })
    return usos


def agregar(usos: list[dict], por: str) -> dict[str, dict[str, int]]:
    soma: dict[str, dict[str, int]] = defaultdict(lambda: {c: 0 for c in CAMPOS} | {"respostas": 0})
    for u in usos:
        s = soma[u[por] or "(vazio)"]
        s["respostas"] += 1
        for c in CAMPOS:
            s[c] += u[c]
    return dict(soma)


def _tabela(titulo: str, grupos: dict[str, dict[str, int]]) -> None:
    print(f"\n{titulo}")
    print(f"{'grupo':<28}{'respostas':>10}{'input':>12}{'cache_cria':>12}{'cache_le':>14}{'output':>10}{'cache %':>9}")
    for nome, s in sorted(grupos.items()):
        lido = s["cache_read_input_tokens"]
        total_entrada = s["input_tokens"] + s["cache_creation_input_tokens"] + lido
        pct = 100.0 * lido / total_entrada if total_entrada else 0.0
        print(f"{nome[:27]:<28}{s['respostas']:>10}{s['input_tokens']:>12}{s['cache_creation_input_tokens']:>12}"
              f"{lido:>14}{s['output_tokens']:>10}{pct:>8.1f}%")


def main() -> int:
    ap = argparse.ArgumentParser(description="Soma o consumo de tokens do Claude Code a partir dos transcritos locais.")
    ap.add_argument("--projeto", help="slug da pasta em ~/.claude/projects (padrão: o do diretório atual)")
    ap.add_argument("--desde", help="AAAA-MM-DD inclusive")
    ap.add_argument("--ate", help="AAAA-MM-DD inclusive")
    ap.add_argument("--json", help="grava o agregado em JSON")
    # ! Alteração de IA - Revisar: opção --agentes ROTULO=ID,... (29/09/2026): soma, por rótulo, só os transcritos de
    # subagente cujo nome contém o ID (os `agent-<id>.jsonl` da sessão) e imprime entrada, cache, saída, total e novos.
    # ! Motivo: a regra de permanência do codebase-memory-mcp (decisão 49) compara a mesma tarefa feita por subagentes
    # com ferramentas diferentes (grep × servidor); o agregado por dia, modelo e tipo mistura todos os subagentes.
    # "total" soma os quatro campos de `usage`; "novos" deixa de fora a leitura de cache (entrada nova + criação + saída).
    ap.add_argument("--agentes", help="ROTULO=ID,... : soma só os transcritos de subagente cujo nome contém cada ID")
    args = ap.parse_args()
    pasta = _pasta_projeto(args.projeto)
    if not pasta.is_dir():
        print(f"pasta não encontrada: {pasta}")
        return 2
    if args.agentes:
        por_agente: dict[str, dict[str, int]] = {}
        for par in (x.strip() for x in args.agentes.split(",") if x.strip()):
            rotulo, ident = par.split("=", 1)
            arquivos = sorted(pasta.rglob(f"*{ident}*.jsonl"))
            usos_ag = ler_usos(pasta, arquivos)
            soma = {c: sum(u[c] for u in usos_ag) for c in CAMPOS}
            soma["respostas"], soma["arquivos"] = len(usos_ag), len(arquivos)
            soma["total"] = sum(soma[c] for c in CAMPOS)
            soma["novos"] = soma["input_tokens"] + soma["cache_creation_input_tokens"] + soma["output_tokens"]
            por_agente[rotulo] = soma
        print(f"{'rótulo':<18}{'arq':>4}{'resp':>6}{'input':>9}{'cache_cria':>12}{'cache_le':>11}"
              f"{'output':>9}{'total':>10}{'novos':>9}")
        for rotulo, s in por_agente.items():
            print(f"{rotulo[:17]:<18}{s['arquivos']:>4}{s['respostas']:>6}{s['input_tokens']:>9}"
                  f"{s['cache_creation_input_tokens']:>12}{s['cache_read_input_tokens']:>11}{s['output_tokens']:>9}"
                  f"{s['total']:>10}{s['novos']:>9}")
        if args.json:
            Path(args.json).write_text(json.dumps({"pasta": str(pasta), "por_agente": por_agente},
                                                  ensure_ascii=False, indent=1), encoding="utf-8")
            print(f"gravado em {args.json}")
        return 0
    usos = ler_usos(pasta)
    if args.desde:
        usos = [u for u in usos if u["dia"] >= args.desde]
    if args.ate:
        usos = [u for u in usos if u["dia"] <= args.ate]
    print(f"{len(usos)} respostas do modelo em {pasta}")
    por_dia, por_modelo, por_tipo = agregar(usos, "dia"), agregar(usos, "modelo"), agregar(usos, "tipo")
    _tabela("Por dia", por_dia)
    _tabela("Por modelo", por_modelo)
    _tabela("Por tipo de agente", por_tipo)
    total = agregar(usos, "tipo")
    saida_total = sum(s["output_tokens"] for s in total.values())
    print(f"\nTotal de saída (tokens gerados): {saida_total}")
    if args.json:
        Path(args.json).write_text(json.dumps({"pasta": str(pasta), "n_respostas": len(usos), "por_dia": por_dia,
                                               "por_modelo": por_modelo, "por_tipo": por_tipo},
                                              ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"gravado em {args.json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
