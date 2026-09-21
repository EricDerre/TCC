# ! Alteração de IA - Revisar: script novo (21/09/2026) que confere a documentação antes de entregar: links relativos,
# tag `! Alteração de IA - Revisar` acompanhada de `! Motivo` em todo arquivo tocado no git, frases obsoletas, as
# hipóteses H1–H6 idênticas em plano × achados × relatório, BOM e ausência de travessão nos `.ps1`, e a lista de
# arquivos no working tree.
# ! Motivo: na Fase 3 essas conferências eram feitas por agentes revisores (~1,6 M tokens por onda); são checagens
# mecânicas que a máquina faz em segundos, como o Eric pediu — o modelo só lê o resumo das falhas.
"""Uso: python ferramentas/conferir_docs.py [--obsoletas "frase1|frase2"] [--sem-git]  → código 0 se tudo passou."""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

RAIZ = Path(__file__).resolve().parents[1]
PASTAS_MD = ("Documentacao", "claude-memoria", ".claude")
ARQUIVOS_MD_RAIZ = ("README.md",)
OBSOLETAS_PADRAO = [
    "bateria não executada", "aguardando decisão do Eric", "31/08/2026 a 12/09/2026", "em implementação (Fase 3)",
    "26 códigos de rejeição", "172 verificações", "Fase 3 (plano aprovado)",
]
PLANO_F3 = RAIZ / "claude-memoria" / "plano-aprovado-fase-3.md"
ACHADOS = RAIZ / "Documentacao" / "memorial" / "3-resultados-e-analises" / "achados-dos-modelos.md"
RELATORIO_F3 = RAIZ / "Documentacao" / "memorial" / "3-resultados-e-analises" / "fase-3-relatorio-por-modelo.md"


def _md_alvo() -> list[Path]:
    arqs = [RAIZ / a for a in ARQUIVOS_MD_RAIZ]
    for pasta in PASTAS_MD:
        arqs += sorted((RAIZ / pasta).rglob("*.md"))
    return [a for a in arqs if a.is_file()]


def conferir_links() -> list[str]:
    falhas = []
    for a in _md_alvo():
        t = a.read_text(encoding="utf-8", errors="replace")
        # remove blocos de código para não conferir links de exemplo
        t = re.sub(r"```.*?```", "", t, flags=re.S)
        for m in re.finditer(r"\]\(([^)\s]+?)(?:#[^)]*)?\)", t):
            alvo = m.group(1)
            if alvo.startswith(("http://", "https://", "mailto:", "#")):
                continue
            alvo_limpo = alvo.replace("%20", " ")
            destino = (a.parent / alvo_limpo).resolve()
            # links escritos a partir da raiz do repositório (o plano da 2-B usa essa forma) valem se existirem lá
            if not destino.exists() and not (RAIZ / alvo_limpo).exists():
                falhas.append(f"{a.relative_to(RAIZ)}: link quebrado → {alvo}")
    return falhas


def arquivos_tocados() -> list[Path]:
    try:
        saida = subprocess.run(["git", "status", "--short"], cwd=RAIZ, capture_output=True, text=True, encoding="utf-8").stdout
    except OSError:
        return []
    arqs = []
    for linha in saida.splitlines():
        caminho = linha[3:].strip().strip('"')
        p = RAIZ / caminho
        if p.is_file():
            arqs.append(p)
        elif p.is_dir():
            arqs += [x for x in p.rglob("*") if x.is_file()]
    return arqs


def conferir_tags(arqs: list[Path]) -> list[str]:
    falhas = []
    for a in arqs:
        if a.suffix.lower() not in (".md", ".py", ".ps1", ".json", ".cmd", ".bat", ".php", ".js", ".yaml", ".yml", ".txt"):
            continue
        if "resultados_alvo" in a.as_posix() or ".superpowers" in a.as_posix():
            continue
        t = a.read_text(encoding="utf-8", errors="replace")
        tags = len(re.findall(r"de IA - Revisar", t))
        motivos = len(re.findall(r"! Motivo", t))
        if tags == 0:
            falhas.append(f"{a.relative_to(RAIZ)}: sem tag de IA")
        elif motivos == 0:
            falhas.append(f"{a.relative_to(RAIZ)}: tag sem `! Motivo`")
    return falhas


# Planos aprovados são artefatos congelados: o texto original fica e o anexo registra os desvios.
CONGELADOS = ("plano-aprovado-",)
# Scripts anteriores à regra do BOM (raiz do repositório, Cobaia): reportados como aviso, não como falha.
PS1_PRE_EXISTENTES = ("build_exe.ps1", "install.ps1", "run.ps1")


def conferir_obsoletas(frases: list[str]) -> list[str]:
    achados = []
    for a in _md_alvo():
        if any(c in a.name for c in CONGELADOS):
            continue
        texto = a.read_text(encoding="utf-8", errors="replace")
        # comentários HTML inteiros saem da varredura: é onde as tags citam a frase antiga como motivo
        texto = re.sub(r"<!--.*?-->", lambda m: chr(10) * m.group(0).count(chr(10)), texto, flags=re.S)
        for i, l in enumerate(texto.splitlines(), start=1):
            for f in frases:
                if f and f in l:
                    achados.append(f"{a.relative_to(RAIZ)}:{i}: \"{f}\"")
    return achados


def _hipoteses(texto: str) -> dict[str, str]:
    norm = lambda s: re.sub(r"[\s*|`]+", " ", s).strip(" .")
    return {m.group(1): norm(m.group(2)) for m in re.finditer(r"\*\*(H[1-6])\*\*\s*[—:|-]\s*([^\n]+)", texto)}


def conferir_hipoteses() -> list[str]:
    falhas = []
    if not PLANO_F3.is_file():
        return ["plano aprovado da Fase 3 não encontrado"]
    hp = _hipoteses(PLANO_F3.read_text(encoding="utf-8"))
    if len(hp) != 6:
        return [f"plano: {len(hp)} hipóteses encontradas (esperado 6)"]
    for nome, arq in (("achados", ACHADOS), ("relatório", RELATORIO_F3)):
        norm = re.sub(r"[\s*|`]+", " ", arq.read_text(encoding="utf-8"))
        for k, v in hp.items():
            if v not in norm:
                falhas.append(f"{nome}: {k} difere do plano")
    return falhas


def conferir_ps1() -> list[str]:
    falhas: list[str] = []
    avisos: list[str] = []
    for a in list(RAIZ.rglob("*.ps1")):
        if ".venv" in a.parts or "node_modules" in a.parts:
            continue
        b = a.read_bytes()
        pre = a.name in PS1_PRE_EXISTENTES and a.parent == RAIZ
        destino = avisos if pre else falhas
        prefixo = "aviso (pré-existente, parse conferido em 21/09): " if pre else ""
        if b[:3] != b"\xef\xbb\xbf":
            destino.append(f"{prefixo}{a.relative_to(RAIZ)}: sem BOM")
        if "—".encode("utf-8") in b:
            destino.append(f"{prefixo}{a.relative_to(RAIZ)}: contém travessão")
    for av in avisos:
        print("   ", av)
    return falhas


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--obsoletas", help="frases separadas por |, além das padrão")
    ap.add_argument("--sem-git", action="store_true", help="não confere tags dos arquivos do working tree")
    args = ap.parse_args()
    frases = OBSOLETAS_PADRAO + (args.obsoletas.split("|") if args.obsoletas else [])
    blocos = [("links relativos", conferir_links()), ("frases obsoletas", conferir_obsoletas(frases)),
              ("hipóteses H1–H6", conferir_hipoteses()), ("arquivos .ps1", conferir_ps1())]
    if not args.sem_git:
        tocados = arquivos_tocados()
        blocos.append((f"tag + motivo nos {len(tocados)} arquivos tocados", conferir_tags(tocados)))
    total = 0
    for nome, falhas in blocos:
        print(f"{nome}: {'ok' if not falhas else str(len(falhas)) + ' problema(s)'}")
        for f in falhas:
            print("   ", f)
        total += len(falhas)
    print("RESULTADO:", "tudo ok" if total == 0 else f"{total} problema(s)")
    return 0 if total == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
