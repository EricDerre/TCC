#!/usr/bin/env python3
# ! Alteração de IA - Revisar: arquivo novo (08/11/2026, Pós-Fase 4, pacote Q4): o protótipo de viabilidade da integração com o Git (seção 3.7 do
# plano), sem ligar ao agente nem ao hub. Monta o mapa dos verbetes (`arquivos:` e `endpoints:` do cabeçalho de cada verbete da biblioteca de
# produção, lida e nunca alterada) e dos cenários (`cenarios_fase4.CENARIOS`: a página de cada roteiro, as páginas abertas pelos passos e os
# arquivos PHP que elas incluem, mais a requisição da API e, por ela, os verbetes e os arquivos ligados ao endpoint); dado o `git diff
# --name-only <commit testado> <atual>` do próprio repositório, diz quais cenários e verbetes são atingidos e por quê (que arquivo, que verbete,
# que endpoint), com as três regras da base E do levantamento §6.15.5: arquivo da aplicação fora do mapa roda tudo, nunca nada; rodada completa
# periódica; a seleção é conferida contra a rodada completa e o que ela deixou de rodar fica registrado. `--prova` aplica a seleção a cada par de
# commits consecutivos que mexeram nas cobaias (histórico real do repositório) e grava `resultados_alvo/fase4/impacto_git.{json,md}` com
# `--check`; `--desde <commit>` mostra a seleção para o que mudou desde um commit. Só comandos git de leitura (log, diff --name-only).
# ! Motivo: plano aprovado da Pós-Fase 4, seção 3.7 e pacote Q7 ("protótipo de viabilidade antes da Fase 5, meia sessão, na Q4"), para o TCC dizer
# "provado em código"; a seleção por arquivo tem respaldo em Rothermel e Harrold (1997), Gligoric, Eloussi e Marinov (2015) e Memon et al. (2017),
# o mapa à mão em Azure DevOps (`TIA.UserMapFile`), e a ponte por documentação em linguagem natural (os verbetes) é nossa, sem respaldo direto;
# por isso as três regras de segurança são obrigatórias, e o mapa é declarado aproximado (os includes do PHP são resolvidos pelo caminho relativo
# ao arquivo e, se não existir, pela raiz do front; o que não existe no disco fica fora).
"""Protótipo da seleção de cenários pelo diff do Git (Pós-Fase 4, pacote Q4). Uso (em Programacao/AgenteCore/experimentos):
  RESULTADOS_DIR=resultados_alvo python impacto_git.py --prova [--check]   # a seleção par a par no histórico das cobaias -> resultados_alvo/fase4/impacto_git.{json,md}
  python impacto_git.py --desde 633ebb27 [--ate HEAD]                     # o que rodar pelo que mudou desde um commit
  python impacto_git.py --mapa                                            # o mapa dos cenários e dos verbetes

Fontes: ROTHERMEL, G.; HARROLD, M. J. A safe, efficient regression test selection technique (1997); GLIGORIC, M.; ELOUSSI, L.; MARINOV, D.
Practical regression test selection with dynamic file dependencies (2015); MEMON, A. et al. Taming Google-scale continuous testing (2017);
MICROSOFT. Use Test Impact Analysis (Azure Pipelines). Todas no levantamento §6.15.5 do Memorial.
"""
from __future__ import annotations

import argparse
import datetime as dt
import itertools
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

import biblioteca as bib
import caminhos
import cenarios_fase4 as cen
import pre_fase4 as pf

RAIZ = caminhos.AQUI.parent.parent.parent
PASTA_BIBLIOTECA = caminhos.AQUI.parent / "biblioteca_producao"
FRONT = "Programacao/CobaiaFront"
API = "Programacao/CobaiaAPI"
APLICACAO = (API, FRONT)
# o que muda dentro das pastas da aplicação sem mudar o que ela faz (com o motivo, declarado)
IGNORADOS = (("/.venv/", "ambiente virtual do Python versionado por engano e depois retirado do git: não é código da aplicação"),
             ("/__pycache__/", "bytecode gerado pelo Python"),
             (".pyc", "bytecode gerado pelo Python"),
             (f"{API}/tests/", "testes da própria cobaia: não mudam o que a aplicação faz"))
REGRAS = {"fora_do_mapa_roda_tudo": ("arquivo da aplicação que nenhum cenário nem verbete declara dispara a rodada completa, nunca nada (Azure DevOps TIA: "
                                     "arquivo que o mapa não entende roda tudo; Rothermel e Harrold, 1997: na dúvida, selecionar a mais)"),
          "rodada_completa_periodica": ("a seleção não substitui a rodada completa: ela continua em periodicidade fixa, e também quando nenhum arquivo da "
                                        "aplicação mudou (Azure DevOps TIA: rodada completa configurada, recomendada)"),
          "conferencia_contra_a_rodada_completa": ("cada seleção registra os cenários que deixou de rodar, e a rodada completa seguinte confere se algum deles "
                                                   "falhou (Azure DevOps TIA: comparar T1, os selecionados, com T2, todos)")}
CLASSES = ("fora_da_aplicacao", "ignorado", "no_mapa", "fora_do_mapa")
INCLUDE_RE = re.compile(r"""\b(?:include|require)(?:_once)?\s*\(?\s*(?:__DIR__\s*\.\s*)?['"]([^'"]+)['"]""")
PROFUNDIDADE_DOS_INCLUDES = 4
RELATORIO_F4 = RAIZ / "Documentacao" / "memorial" / "3-resultados-e-analises" / "fase-4-relatorio.md"
PREFIXO = "tb_f4_impacto_"
NOME = "impacto_git"
FONTES = ("Rothermel e Harrold (1997): seleção segura inclui todo teste capaz de expor falha no programa modificado",
          "Gligoric, Eloussi e Marinov (2015), Ekstazi: dependência em nível de arquivo cortou o tempo de teste em 32% a 54%",
          "Memon et al. (2017), Google TAP: os alvos que dependem dos arquivos modificados são a base da seleção",
          "Azure DevOps, Test Impact Analysis: mapa à mão e aproximado (TIA.UserMapFile), arquivo desconhecido roda tudo, rodada completa periódica, T1 contra T2")
sem_data = pf.sem_data


def agora() -> str:
    return dt.datetime.now().isoformat(timespec="seconds")


def _posix(caminho: str) -> str:
    return caminho.replace("\\", "/")


# ------------------------------------------------------------------ o mapa

def includes_php(arquivo: str, raiz: Path = RAIZ, profundidade: int = PROFUNDIDADE_DOS_INCLUDES, vistos: set | None = None) -> dict[str, str]:
    """Os arquivos PHP que `arquivo` (caminho relativo à raiz do repositório) inclui, direta e indiretamente, com a origem de cada um
    ("include em <arquivo>"). O caminho do include é resolvido relativo à pasta do arquivo e, se não existir, à raiz do front; o que não existe
    no disco fica fora. É um mapa aproximado, como o `TIA.UserMapFile` do Azure."""
    vistos = set() if vistos is None else vistos
    saida: dict[str, str] = {}
    if profundidade <= 0 or arquivo in vistos:
        return saida
    vistos.add(arquivo)
    caminho = raiz / arquivo
    if not caminho.exists() or caminho.suffix.lower() != ".php":
        return saida
    texto = caminho.read_text(encoding="utf-8", errors="replace")
    for alvo in INCLUDE_RE.findall(texto):
        candidatos = [caminho.parent / alvo.lstrip("/"), raiz / FRONT / alvo.lstrip("/")]
        encontrado = next((c for c in candidatos if c.exists() and c.is_file()), None)
        if encontrado is None:
            continue
        rel = _posix(str(encontrado.resolve().relative_to(raiz.resolve())))
        if rel not in saida and rel != arquivo:
            saida[rel] = f"include em {arquivo}"
        for inc, origem in includes_php(rel, raiz, profundidade - 1, vistos).items():
            saida.setdefault(inc, origem)
    return saida


def mapa(raiz: Path = RAIZ, pasta_biblioteca: Path = PASTA_BIBLIOTECA) -> dict:
    """O mapa: verbetes (arquivos: e endpoints: do cabeçalho), cenários (página, páginas abertas pelos passos, includes, endpoint, verbetes e
    arquivos ligados pelo endpoint), os cenários do ensaio com o cenário base de cada um, e o mapa inverso arquivo -> cenários e verbetes."""
    verbetes = bib.carregar(pasta_biblioteca)
    mv = {v["id"]: {"arquivos": list(v["meta"].get("arquivos", [])), "endpoints": list(v["meta"].get("endpoints", [])),
                    "caminho": _posix(str(Path(v["caminho"]).resolve().relative_to(raiz.resolve()))), "tipo": v["meta"].get("tipo")} for v in verbetes}
    por_endpoint: dict[str, list[str]] = defaultdict(list)
    for vid, v in sorted(mv.items()):
        for e in v["endpoints"]:
            por_endpoint[e].append(vid)
    mc = {}
    for c in cen.CENARIOS:
        origens: dict[str, list[str]] = defaultdict(list)
        paginas = [c["pagina"]] + [p["url"].split("?")[0] for p in c["passos"] if p.get("acao") == "abrir" and p.get("url")]
        for p in dict.fromkeys(paginas):
            rel = f"{FRONT}/{p}"
            origens[rel].append("página do cenário" if p == c["pagina"] else "página aberta por um passo do cenário")
            for inc, origem in includes_php(rel, raiz).items():
                if origem not in origens[inc]:
                    origens[inc].append(origem)
        endpoints = [c["requisicao"]] if c.get("requisicao") else []
        ligados = sorted({vid for e in endpoints for vid in por_endpoint.get(e, [])})
        # um arquivo citado por vários verbetes do endpoint leva todos eles no motivo (não só o primeiro em ordem alfabética)
        verbetes_do_arquivo: dict[str, list[str]] = defaultdict(list)
        for vid in ligados:
            for a in mv[vid]["arquivos"]:
                verbetes_do_arquivo[a].append(vid)
        for a, vids in verbetes_do_arquivo.items():
            origens[a].append(f"arquivo {'do verbete' if len(vids) == 1 else 'dos verbetes'} {', '.join(vids)} (endpoint {', '.join(endpoints)})")
        mc[c["id"]] = {"cobaia": c["cobaia"], "titulo": c["titulo"], "pagina": c["pagina"], "requisicao": c.get("requisicao"), "endpoints": endpoints,
                       "verbetes": ligados, "arquivos": sorted(origens), "arquivos_por_origem": {a: "; ".join(origens[a]) for a in sorted(origens)}}
    ensaio = {e["id"]: e["cenario"] for e in cen.CENARIOS_DO_ENSAIO}
    inverso: dict[str, dict] = defaultdict(lambda: {"cenarios": [], "verbetes": []})
    for cid, c in sorted(mc.items()):
        for a in c["arquivos"]:
            inverso[a]["cenarios"].append(cid)
    for vid, v in sorted(mv.items()):
        for a in v["arquivos"]:
            inverso[a]["verbetes"].append(vid)
    return {"verbetes": mv, "cenarios": mc, "ensaio": ensaio, "arquivos": dict(sorted(inverso.items())), "aplicacao": list(APLICACAO),
            "ignorados": [{"padrao": p, "motivo": m} for p, m in IGNORADOS]}


# ------------------------------------------------------------------ a seleção

def classificar(arquivo: str, m: dict) -> tuple[str, str]:
    """A classe de um arquivo alterado e o motivo: fora_da_aplicacao, ignorado, no_mapa ou fora_do_mapa."""
    arquivo = _posix(arquivo)
    if not any(arquivo.startswith(a + "/") for a in m["aplicacao"]):
        return "fora_da_aplicacao", f"fora das pastas da aplicação ({', '.join(m['aplicacao'])}): não muda o que as cobaias fazem"
    for item in m["ignorados"]:
        padrao = item["padrao"]
        if (padrao.startswith("/") and padrao in "/" + arquivo) or (not padrao.startswith("/") and (arquivo.startswith(padrao) or arquivo.endswith(padrao))):
            return "ignorado", item["motivo"]
    inv = m["arquivos"].get(arquivo)
    if inv:
        return "no_mapa", f"no mapa: cenários {', '.join(inv['cenarios']) or 'nenhum'}; verbetes {', '.join(inv['verbetes']) or 'nenhum'}"
    return "fora_do_mapa", "arquivo da aplicação que nenhum cenário nem verbete declara: pela regra 1, roda tudo"


def selecionar(alterados: list[str], m: dict) -> dict:
    """Dado o que mudou, os cenários (base e do ensaio) e os verbetes atingidos, com o motivo de cada um, as três regras aplicadas e o que a
    seleção deixou de rodar, para a conferência contra a rodada completa."""
    arquivos = []
    cen_sel: dict[str, list[str]] = defaultdict(list)
    verb_sel: dict[str, list[str]] = defaultdict(list)
    fora_do_mapa = []
    contagem = {c: 0 for c in CLASSES}
    for a in sorted({_posix(x) for x in alterados}):
        classe, motivo = classificar(a, m)
        contagem[classe] += 1
        if classe == "no_mapa":
            inv = m["arquivos"][a]
            for cid in inv["cenarios"]:
                cen_sel[cid].append(f"{a}: {m['cenarios'][cid]['arquivos_por_origem'][a]}")
            for vid in inv["verbetes"]:
                verb_sel[vid].append(f"{a} está em arquivos: do cabeçalho do verbete")
        elif classe == "fora_do_mapa":
            fora_do_mapa.append(a)
        arquivos.append({"arquivo": a, "classe": classe, "motivo": motivo})
    todos = sorted(m["cenarios"])
    rodar_tudo = bool(fora_do_mapa)
    if rodar_tudo:
        lista = ", ".join(fora_do_mapa[:3]) + (f" e mais {len(fora_do_mapa) - 3}" if len(fora_do_mapa) > 3 else "")
        cenarios = {cid: [f"regra 1: arquivo da aplicação fora do mapa ({lista})"] + cen_sel.get(cid, []) for cid in todos}
        motivo = f"roda tudo: {len(fora_do_mapa)} arquivo(s) da aplicação fora do mapa ({lista}); regra 1, arquivo fora do mapa roda tudo, nunca nada"
    else:
        cenarios = {cid: cen_sel[cid] for cid in sorted(cen_sel)}
        if not alterados:
            motivo = "nenhum arquivo alterado: nada a rodar pela seleção; vale a rodada completa periódica (regra 2)"
        elif cenarios:
            motivo = (f"seleção parcial: {len(cenarios)} de {len(todos)} cenários, pelos arquivos no mapa; os {len(todos) - len(cenarios)} deixados de fora ficam "
                      f"registrados para a conferência contra a rodada completa (regra 3)")
        else:
            motivo = (f"nenhum arquivo da aplicação no mapa mudou ({contagem['fora_da_aplicacao']} fora da aplicação, {contagem['ignorado']} ignorados): nada a rodar "
                      f"pela seleção; vale a rodada completa periódica (regra 2)")
    deixados = sorted(set(todos) - set(cenarios))
    ensaio = sorted(e for e, base in m["ensaio"].items() if base in cenarios)
    return {"arquivos": arquivos, "cenarios": cenarios, "verbetes": {vid: verb_sel[vid] for vid in sorted(verb_sel)}, "ensaio": ensaio,
            "rodar_tudo": rodar_tudo, "motivo": motivo,
            "deixados_de_fora": {"cenarios": deixados, "ensaio": sorted(e for e, base in m["ensaio"].items() if base in deixados)},
            "conferencia": {"rodada_completa": todos, "selecionados": sorted(cenarios), "deixados_de_fora": deixados, "regra": REGRAS["conferencia_contra_a_rodada_completa"]},
            "resumo": {"alterados": len(arquivos), "fora_da_aplicacao": contagem["fora_da_aplicacao"], "ignorados": contagem["ignorado"], "no_mapa": contagem["no_mapa"],
                       "fora_do_mapa": contagem["fora_do_mapa"], "na_aplicacao": contagem["ignorado"] + contagem["no_mapa"] + contagem["fora_do_mapa"]}}


# ------------------------------------------------------------------ o git (só leitura)

def _git(raiz: Path, *argumentos: str) -> str:
    r = subprocess.run(["git", "-C", str(raiz), *argumentos], capture_output=True, text=True, encoding="utf-8", errors="replace", check=True)
    return r.stdout


def arquivos_alterados(raiz: Path, de: str, ate: str = "HEAD", so_aplicacao: bool = False) -> list[str]:
    """`git diff --name-only <de> <ate>`, em ordem; com `so_aplicacao`, só os arquivos das pastas das cobaias."""
    linhas = [_posix(l.strip()) for l in _git(raiz, "diff", "--name-only", de, ate).splitlines() if l.strip()]
    if so_aplicacao:
        linhas = [l for l in linhas if any(l.startswith(a + "/") for a in APLICACAO)]
    return sorted(linhas)


def commits_da_aplicacao(raiz: Path) -> list[dict]:
    """Os commits que mexeram nas pastas das cobaias, do mais antigo ao mais novo (`git log --reverse -- <pastas>`)."""
    saida = []
    for linha in _git(raiz, "log", "--format=%H%x09%ad%x09%s", "--date=short", "--reverse", "--", *APLICACAO).splitlines():
        if not linha.strip():
            continue
        commit, data, assunto = linha.split("\t", 2)
        saida.append({"commit": commit, "data": data, "assunto": assunto})
    return saida


# ------------------------------------------------------------------ a prova sobre o histórico

def _compactar(s: dict) -> dict:
    """A seleção sem a lista inteira de arquivos ignorados e fora da aplicação (num commit, 3827 arquivos da venv): ficam só os da aplicação que
    o mapa classifica, mais a contagem de cada classe."""
    return {**s, "arquivos": [a for a in s["arquivos"] if a["classe"] in ("no_mapa", "fora_do_mapa")]}


def veredito(s: dict) -> str:
    if s["rodar_tudo"]:
        return "roda tudo"
    if s["cenarios"]:
        return "seleção parcial"
    return "nada a rodar"


def prova(raiz: Path = RAIZ) -> tuple[dict, str]:
    """A seleção aplicada a cada par de commits consecutivos que mexeram nas cobaias, no histórico real do repositório."""
    m = mapa(raiz)
    commits = commits_da_aplicacao(raiz)
    pares = []
    for a, b in itertools.pairwise(commits):
        s = selecionar(arquivos_alterados(raiz, a["commit"], b["commit"]), m)
        pares.append({"testado": a["commit"], "atual": b["commit"], "data": b["data"], "assunto": b["assunto"], "veredito": veredito(s),
                      "resumo": s["resumo"], "selecao": _compactar(s)})
    resumo = {"pares": len(pares), "rodar_tudo": sum(1 for p in pares if p["veredito"] == "roda tudo"),
              "selecao_parcial": sum(1 for p in pares if p["veredito"] == "seleção parcial"), "nada_a_rodar": sum(1 for p in pares if p["veredito"] == "nada a rodar"),
              "cenarios_deixados_de_fora_no_total": sum(len(p["selecao"]["deixados_de_fora"]["cenarios"]) for p in pares)}
    dado = {"metadados": {"gerado_em": agora(), "gerado_por": "impacto_git.py --prova", "repositorio": raiz.name,
                          "commits_lidos_por": f"git log --reverse -- {' '.join(APLICACAO)}", "diff_lido_por": "git diff --name-only <testado> <atual>",
                          "fontes": list(FONTES)},
            "regras": dict(REGRAS),
            "mapa": {"cenarios": len(m["cenarios"]), "ensaio": len(m["ensaio"]), "verbetes": len(m["verbetes"]),
                     "verbetes_com_endpoints": sum(1 for v in m["verbetes"].values() if v["endpoints"]),
                     "verbetes_com_arquivos": sum(1 for v in m["verbetes"].values() if v["arquivos"]), "arquivos_no_mapa": len(m["arquivos"]),
                     "por_cenario": {cid: {"cobaia": c["cobaia"], "pagina": c["pagina"], "endpoints": c["endpoints"], "verbetes": c["verbetes"], "arquivos": len(c["arquivos"])}
                                     for cid, c in m["cenarios"].items()}},
            "commits": commits, "pares": pares, "resumo": resumo}
    return dado, render_prova(dado)


def render_prova(dado: dict) -> str:
    cab = pf.cabecalho("Seleção de cenários pelo diff do Git: a prova sobre o histórico do repositório (Pós-Fase 4, pacote Q4)", "impacto_git.py --prova",
                       "git log e git diff --name-only do repositório, biblioteca_producao/ e cenarios_fase4.py", dado["metadados"]["gerado_em"][:10])
    mp, r = dado["mapa"], dado["resumo"]
    linhas = cab + ["", (f"O mapa liga {mp['cenarios']} cenários base ({mp['ensaio']} do ensaio da Fase 5) e {mp['verbetes']} verbetes ({mp['verbetes_com_arquivos']} com `arquivos:`, "
                         f"{mp['verbetes_com_endpoints']} com `endpoints:`) a {mp['arquivos_no_mapa']} arquivos da aplicação. Nos {r['pares']} pares de commits consecutivos que mexeram nas cobaias, "
                         f"a seleção rodaria tudo em {r['rodar_tudo']}, parte dos cenários em {r['selecao_parcial']} e nada em {r['nada_a_rodar']}; "
                         f"{r['cenarios_deixados_de_fora_no_total']} cenários ficaram registrados como deixados de fora, para a conferência contra a rodada completa."), "",
                    "## As três regras", ""]
    linhas += [f"- **{chave}**: {texto}" for chave, texto in dado["regras"].items()]
    linhas += ["", "## A seleção par a par", "", f"<!-- tabela:{PREFIXO}pares -->",
               "| Commit testado | Commit atual | Data | Assunto | Alterados | Fora da aplicação | Ignorados | No mapa | Fora do mapa | Veredito | Cenários selecionados | Deixados de fora |",
               "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for p in dado["pares"]:
        s, rs = p["selecao"], p["resumo"]
        linhas.append(f"| `{p['testado'][:8]}` | `{p['atual'][:8]}` | {p['data']} | {p['assunto'].replace('|', '/')} | {rs['alterados']} | {rs['fora_da_aplicacao']} | {rs['ignorados']} | "
                      f"{rs['no_mapa']} | {rs['fora_do_mapa']} | {p['veredito']} | {', '.join(s['cenarios']) or 'nenhum'} | {', '.join(s['deixados_de_fora']['cenarios']) or 'nenhum'} |")
    linhas += [f"<!-- /tabela:{PREFIXO}pares -->", "", "## Por que, em cada par", ""]
    for p in dado["pares"]:
        s = p["selecao"]
        linhas += [f"### `{p['testado'][:8]}` para `{p['atual'][:8]}` ({p['data']}): {p['veredito']}", "", s["motivo"] + ".", ""]
        for a in s["arquivos"]:
            linhas.append(f"- `{a['arquivo']}`: {a['classe'].replace('_', ' ')}; {a['motivo']}")
        if s["verbetes"]:
            linhas += ["", "Verbetes atingidos: " + "; ".join(f"`{vid}` ({len(motivos)} arquivo(s))" for vid, motivos in s["verbetes"].items()) + "."]
        if s["ensaio"]:
            linhas += ["", f"Cenários do ensaio a rodar: {', '.join(s['ensaio'])}."]
        linhas.append("")
    linhas += ["## O mapa dos cenários", "", f"<!-- tabela:{PREFIXO}cenarios -->", "| Cenário | Cobaia | Página | Endpoint | Verbetes ligados pelo endpoint | Arquivos no mapa |", "|---|---|---|---|---|---|"]
    for cid, c in mp["por_cenario"].items():
        linhas.append(f"| {cid} | {c['cobaia']} | `{c['pagina']}` | {', '.join(c['endpoints']) or 'nenhum'} | {', '.join(c['verbetes']) or 'nenhum'} | {c['arquivos']} |")
    linhas += [f"<!-- /tabela:{PREFIXO}cenarios -->", "", "Fontes: " + "; ".join(dado["metadados"]["fontes"]) + ".", ""]
    return "\n".join(linhas)


def render_selecao(s: dict, de: str, ate: str) -> str:
    linhas = [(f"Arquivos alterados de {de} até {ate}: {s['resumo']['alterados']} ({s['resumo']['no_mapa']} no mapa, {s['resumo']['fora_do_mapa']} fora do mapa, "
               f"{s['resumo']['ignorados']} ignorados, {s['resumo']['fora_da_aplicacao']} fora da aplicação)"), s["motivo"]]
    for a in s["arquivos"]:
        if a["classe"] in ("no_mapa", "fora_do_mapa"):
            linhas.append(f"  - {a['arquivo']}: {a['classe'].replace('_', ' ')}; {a['motivo']}")
    linhas.append("Cenários a rodar: " + (", ".join(s["cenarios"]) or "nenhum") + (f" (ensaio: {', '.join(s['ensaio'])})" if s["ensaio"] else ""))
    for cid, motivos in s["cenarios"].items():
        for mtv in motivos:
            linhas.append(f"  - {cid}: {mtv}")
    linhas.append("Deixados de fora (registrados para a conferência contra a rodada completa): " + (", ".join(s["deixados_de_fora"]["cenarios"]) or "nenhum"))
    return "\n".join(linhas)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--prova", action="store_true", help=f"a seleção em cada par de commits que mexeram nas cobaias -> resultados_alvo/fase4/{NOME}.{{json,md}}")
    ap.add_argument("--check", action="store_true", help="regera e compara com o que está gravado, sem gravar")
    ap.add_argument("--desde", default=None, help="commit testado: mostra a seleção para o que mudou dele até --ate")
    ap.add_argument("--ate", default="HEAD")
    ap.add_argument("--mapa", action="store_true", help="imprime o mapa dos cenários e dos verbetes")
    args = ap.parse_args(argv)
    if args.mapa:
        m = mapa()
        for cid, c in m["cenarios"].items():
            print(f"{cid} ({c['cobaia']}): endpoints {c['endpoints'] or 'nenhum'}; verbetes {c['verbetes'] or 'nenhum'}; {len(c['arquivos'])} arquivos")
            for a, origem in c["arquivos_por_origem"].items():
                print(f"    {a}: {origem}")
        print(f"{len(m['verbetes'])} verbetes, {len(m['arquivos'])} arquivos no mapa")
        return 0
    if args.desde:
        s = selecionar(arquivos_alterados(RAIZ, args.desde, args.ate), mapa())
        print(render_selecao(s, args.desde, args.ate))
        return 0
    if args.prova:
        dado, md = prova()
        return pf.fechar(NOME, dado, md, PREFIXO, check=args.check, pasta=caminhos.RESULTADOS / "fase4", doc=RELATORIO_F4)
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
