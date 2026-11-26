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
import json
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


# ------------------------------------------------------------------ Q7: a decisão de uma corrida, o registro e a conferência

# ! Alteração de IA - Revisar: (25/11/2026, Pós-Fase 4, pacote Q7) a seleção deixa de ser só protótipo e passa a decidir uma corrida. `decidir`
# aplica as três regras da base E ao que mudou e devolve o modo (completa, selecionada ou nada), os cenários do ensaio a rodar, os deixados de
# fora e o motivo de cada um; `decidir_para_a_corrida` lê do Git o commit atual, o que mudou desde o último commit testado e o que ainda não
# foi commitado nas pastas das cobaias; `registrar` e `ler_registro` guardam, num arquivo que só cresce, o commit que cada corrida testou;
# `conferir` compara uma corrida selecionada com uma rodada completa e diz que falha a seleção teria deixado passar; e
# `conferencia_historica` faz essa conta para a seleção de cada par de commits do histórico contra uma rodada completa gravada.
# ! Motivo: plano aprovado da Pós-Fase 4, seção 3.7 e pacote Q7, e decisão 152. O protótipo do Q4 dizia o que a seleção escolheria e ninguém
# usava a escolha. As três regras são o que torna a seleção segura com um mapa escrito à mão: na dúvida roda tudo (arquivo fora do mapa,
# falta de ponto de partida, cenário atingido que o ensaio não roda); a rodada completa volta em prazo fixo, porque o mapa pode estar velho; e
# o que ficou de fora é conferido contra a rodada completa, que é a única medida do que a seleção perdeu. A corrida testa a pasta de trabalho,
# não o último commit: por isso o que ainda não foi commitado nas pastas das cobaias entra na conta. Só comandos de leitura do Git.
REGISTRO = caminhos.RESULTADOS / "hub" / "commits_testados.jsonl"
TIPOS_DE_CORRIDA = ("completa", "selecionada")
DIAS_ATE_A_COMPLETA = 7
NOME_DA_CONFERENCIA = "conferencia_git"
PREFIXO_DA_CONFERENCIA = "tb_f4_conferencia_"
ARQUIVO_DA_DECISAO = "impacto_git.json"
_COMMIT = re.compile(r"^[0-9a-fA-F]{7,40}$")


def ler_registro(arquivo: Path | None = None) -> list[dict]:
    """As corridas que registraram o commit testado, da mais antiga à mais nova; lista vazia sem o arquivo."""
    arquivo = Path(arquivo) if arquivo else REGISTRO
    if not arquivo.exists():
        return []
    return [json.loads(l) for l in arquivo.read_text(encoding="utf-8").splitlines() if l.strip()]


def registrar(arquivo: Path | None, entrada: dict) -> dict:
    """Acrescenta ao registro o commit que uma corrida testou. Só entra corrida completa ou selecionada: a que não rodou nada não testou commit nenhum."""
    arquivo = Path(arquivo) if arquivo else REGISTRO
    if entrada.get("tipo") not in TIPOS_DE_CORRIDA:
        raise ValueError(f"tipo: {entrada.get('tipo')!r} não é um de {TIPOS_DE_CORRIDA}")
    if not isinstance(entrada.get("commit"), str) or not entrada["commit"].strip():
        raise ValueError("commit: faltou o commit que a corrida testou")
    pronta = {"quando": entrada.get("quando") or agora(), "tipo": entrada["tipo"], "commit": entrada["commit"].strip(), "corrida": entrada.get("corrida"),
              "arvore_suja": bool(entrada.get("arvore_suja")), "cenarios": list(entrada.get("cenarios") or []), "deixados_de_fora": list(entrada.get("deixados_de_fora") or [])}
    arquivo.parent.mkdir(parents=True, exist_ok=True)
    with arquivo.open("a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(pronta, ensure_ascii=False) + "\n")
    return pronta


def ultimo_commit_testado(registro: list[dict]) -> str | None:
    return registro[-1]["commit"] if registro else None


def ultima_completa(registro: list[dict]) -> dict | None:
    return next((e for e in reversed(registro) if e.get("tipo") == "completa"), None)


def commit_atual(raiz: Path = RAIZ) -> str:
    return _git(raiz, "rev-parse", "HEAD").strip()


def alterados_na_arvore(raiz: Path = RAIZ) -> list[str]:
    """Os arquivos das pastas das cobaias alterados, criados ou apagados e ainda não commitados (`git status --porcelain`), em ordem."""
    partes = _git(raiz, "status", "--porcelain", "-z", "--untracked-files=all", "--", *APLICACAO).split("\0")
    saida, i = [], 0
    while i < len(partes):
        item = partes[i]
        i += 1
        if len(item) < 4:
            continue
        saida.append(_posix(item[3:]))
        if item[0] in "RC":         # renomeado ou copiado: o item seguinte é o nome antigo
            i += 1
    return sorted(set(saida))


def _dias_entre(antes: str, depois: str) -> int:
    return (dt.datetime.fromisoformat(depois) - dt.datetime.fromisoformat(antes)).days


def decidir(alterados: list[str], m: dict, registro: list[dict], agora: str | None = None, desde: str | None = None, commit_atual: str | None = None,
            completa_a_cada_dias: int = DIAS_ATE_A_COMPLETA, arvore_suja: bool = False) -> dict:
    """O que uma corrida de cenários roda, dado o que mudou: o modo (`completa`, `selecionada` ou `nada`), os cenários do ensaio, os deixados de
    fora, as regras aplicadas e o motivo. `desde` é o commit testado de onde o diff parte; sem ele não há seleção."""
    momento = agora or globals()["agora"]()
    s = selecionar(alterados, m)
    todos = sorted(m["ensaio"])
    base = {"commit_testado": desde, "commit_atual": commit_atual, "arvore_suja": bool(arvore_suja), "alterados": s["resumo"],
            "arquivos": [a for a in s["arquivos"] if a["classe"] in ("no_mapa", "fora_do_mapa")], "verbetes": sorted(s["verbetes"]), "completa_a_cada_dias": completa_a_cada_dias}

    def completa(regra: str | None, motivo: str) -> dict:
        return {**base, "modo": "completa", "regras": [regra] if regra else [], "motivo": motivo, "cenarios": todos, "deixados_de_fora": [],
                "por_que": {c: [motivo] for c in todos}}

    if desde is None:
        return completa(None, "não há commit testado registrado nem `--desde`: sem ponto de partida para o diff, roda tudo")
    if s["rodar_tudo"]:
        return completa("fora_do_mapa_roda_tudo", s["motivo"])
    ultima = ultima_completa(registro)
    if ultima is None:
        return completa("rodada_completa_periodica", "nenhuma rodada completa está registrada: a seleção só vale entre duas rodadas completas (regra 2)")
    dias = _dias_entre(ultima["quando"], momento)
    if dias >= completa_a_cada_dias:
        return completa("rodada_completa_periodica", f"a última rodada completa (`{ultima.get('corrida')}`) foi há {dias} dias, e o prazo é de {completa_a_cada_dias}: "
                                                     "roda tudo (regra 2)")
    ensaio = sorted(s["ensaio"])
    if s["cenarios"] and not ensaio:
        return completa(None, f"a mudança atinge {', '.join(sorted(s['cenarios']))}, que não tem execução no ensaio: na dúvida, roda tudo")
    if not ensaio:
        return {**base, "modo": "nada", "regras": ["rodada_completa_periodica"], "motivo": s["motivo"], "cenarios": [], "deixados_de_fora": todos, "por_que": {}}
    deixados = sorted(set(todos) - set(ensaio))
    return {**base, "modo": "selecionada", "regras": ["conferencia_contra_a_rodada_completa"],
            "motivo": (f"seleção parcial: {len(ensaio)} de {len(todos)} cenários do ensaio, pelos arquivos no mapa; os {len(deixados)} deixados de fora ficam registrados "
                       "para a conferência contra a rodada completa (regra 3)"),
            "cenarios": ensaio, "deixados_de_fora": deixados, "por_que": {e: list(s["cenarios"][m["ensaio"][e]]) for e in ensaio}}


def decidir_para_a_corrida(raiz: Path = RAIZ, desde: str | None = None, completa_a_cada_dias: int = DIAS_ATE_A_COMPLETA, registro: Path | None = None,
                           agora: str | None = None) -> dict:
    """A decisão para a corrida que vai rodar agora nesta pasta: o ponto de partida é `desde` ou o último commit testado do registro; o que mudou
    é o diff dele até o commit atual mais o que ainda não foi commitado nas pastas das cobaias."""
    if desde is not None and not _COMMIT.match(desde):
        raise ValueError("--desde: esperava o identificador de um commit (de 7 a 40 caracteres hexadecimais)")
    reg = ler_registro(registro)
    partida = desde or ultimo_commit_testado(reg)
    na_arvore = alterados_na_arvore(raiz)
    alterados = sorted(set((arquivos_alterados(raiz, partida, "HEAD") if partida else []) + na_arvore))
    return decidir(alterados, mapa(), reg, agora=agora, desde=partida, commit_atual=commit_atual(raiz), completa_a_cada_dias=completa_a_cada_dias,
                   arvore_suja=bool(na_arvore))


def _por_cenario(registros: list[dict]) -> dict[str, dict]:
    saida: dict[str, dict] = {}
    for r in registros:
        x = saida.setdefault(r["cenario"], {"execucoes": 0, "task_success": 0})
        x["execucoes"] += 1
        x["task_success"] += 1 if r.get("task_success") else 0
    return saida


def _passou(x: dict) -> bool:
    return x["task_success"] == x["execucoes"]


def conferir(decisao: dict, registros_da_selecionada: list[dict], registros_da_completa: list[dict]) -> dict:
    """A regra 3: cada cenário do ensaio, se rodou na seleção, e o que a rodada completa mostra dele. A falha perdida é o cenário deixado de
    fora que não passou em todas as execuções da rodada completa."""
    sel, comp = _por_cenario(registros_da_selecionada), _por_cenario(registros_da_completa)
    escolhidos = set(decisao.get("cenarios") or [])
    linhas, perdidas, discordam, sem_completa = [], [], [], []
    for c in sorted(escolhidos | set(decisao.get("deixados_de_fora") or []) | set(comp)):
        na, x, y = c in escolhidos, comp.get(c), sel.get(c)
        if na:
            if x is None or y is None:
                situacao = "selecionado, mas não rodou nas duas corridas"
            elif _passou(x) == _passou(y):
                situacao = "rodou nas duas e o resultado é o mesmo"
            else:
                situacao = "rodou nas duas e o resultado não é o mesmo"
                discordam.append(c)
        elif x is None:
            situacao = "ficou de fora e não rodou na rodada completa"
            sem_completa.append(c)
        elif _passou(x):
            situacao = "ficou de fora e passou na rodada completa"
        else:
            situacao = f"ficou de fora e falhou na rodada completa ({x['task_success']} de {x['execucoes']} execuções com Task Success): a seleção perderia esta falha"
            perdidas.append(c)
        linhas.append({"cenario": c, "na_selecao": na, "completa": x, "selecionada": y if na else None, "situacao": situacao})
    return {"regra": REGRAS["conferencia_contra_a_rodada_completa"],
            "decisao": {k: decisao.get(k) for k in ("modo", "commit_testado", "commit_atual", "arvore_suja", "motivo")}, "cenarios": linhas,
            "resumo": {"selecionados": len(escolhidos), "deixados_de_fora": len(decisao.get("deixados_de_fora") or []), "falhas_perdidas": perdidas,
                       "discordancias": discordam, "sem_rodada_completa": sem_completa, "segura": not perdidas and not sem_completa}}


def render_conferencia(c: dict, selecionada: str, completa: str) -> str:
    r = c["resumo"]
    linhas = [f"# Conferência da seleção pelo Git contra a rodada completa: `{selecionada}` contra `{completa}`", "",
              (f"A corrida `{selecionada}` rodou {r['selecionados']} cenários e deixou {r['deixados_de_fora']} de fora. Falhas perdidas (cenário deixado de fora que não passou "
               f"em todas as execuções da rodada completa `{completa}`): " + (", ".join(f"`{x}`" for x in r["falhas_perdidas"]) or "nenhuma") + ". "
               + ("A seleção foi segura para esta mudança." if r["segura"] else "A seleção não foi segura para esta mudança.")), "",
              "| Cenário | Na seleção | Rodada completa | Corrida selecionada | Situação |", "|---|---|---|---|---|"]
    for x in c["cenarios"]:
        f = lambda y: f"{y['task_success']} de {y['execucoes']}" if y else "não rodou"
        linhas.append(f"| `{x['cenario']}` | {'sim' if x['na_selecao'] else 'não'} | {f(x['completa'])} | {f(x['selecionada']) if x['na_selecao'] else 'fora'} | {x['situacao']} |")
    linhas += ["", "Regra aplicada: " + c["regra"] + ".", ""]
    return "\n".join(linhas)


def conferencia_historica(raiz: Path = RAIZ, completa: str = "fase5_agente_b") -> tuple[dict, str]:
    """A regra 3 aplicada, como conta retrospectiva, à seleção de cada par de commits que mexeu nas cobaias: que cenários cada seleção deixaria
    de fora e o que a rodada completa gravada mostra deles. Nenhuma dessas seleções rodou de verdade."""
    dado_da_prova, _ = prova(raiz)
    arquivo = caminhos.RESULTADOS / completa / "cenarios.jsonl"
    registros = [json.loads(l) for l in arquivo.read_text(encoding="utf-8").splitlines() if l.strip()]
    por = _por_cenario(registros)
    falharam = sorted(c for c, x in por.items() if not _passou(x))
    pares = []
    for p in dado_da_prova["pares"]:
        deixados = sorted(p["selecao"]["deixados_de_fora"]["ensaio"])
        perdidas = sorted(set(deixados) & set(falharam))
        pares.append({"testado": p["testado"], "atual": p["atual"], "data": p["data"], "assunto": p["assunto"], "veredito": p["veredito"],
                      "selecionados": sorted(p["selecao"]["ensaio"]), "deixados_de_fora": deixados, "falhas_perdidas": perdidas, "segura": not perdidas})
    resumo = {"pares": len(pares), "pares_que_rodam_tudo": sum(1 for x in pares if x["veredito"] == "roda tudo"),
              "pares_seguros": sum(1 for x in pares if x["segura"]), "pares_com_falha_perdida": sum(1 for x in pares if not x["segura"]),
              "cenarios_deixados_de_fora_no_total": sum(len(x["deixados_de_fora"]) for x in pares)}
    dado = {"metadados": {"gerado_em": agora(), "gerado_por": "impacto_git.py --conferir-historico", "repositorio": raiz.name,
                          "natureza": ("conta retrospectiva: nenhuma destas seleções rodou de verdade; a pergunta é o que cada uma teria deixado passar se tivesse sido usada "
                                       "no lugar da rodada completa"), "fontes": list(FONTES)},
            "regra": REGRAS["conferencia_contra_a_rodada_completa"],
            "completa": {"corrida": completa, "arquivo": f"{completa}/cenarios.jsonl", "execucoes": len(registros), "cenarios": len(por),
                         "task_success": sum(x["task_success"] for x in por.values()), "cenarios_com_falha": falharam, "por_cenario": por},
            "pares": pares, "resumo": resumo}
    return dado, render_conferencia_historica(dado)


def render_conferencia_historica(dado: dict) -> str:
    c, r = dado["completa"], dado["resumo"]
    cab = pf.cabecalho("Seleção pelo Git conferida contra a rodada completa: a conta retrospectiva sobre o histórico (Pós-Fase 4, pacote Q7)",
                       "impacto_git.py --conferir-historico", f"git log e git diff --name-only do repositório e {c['arquivo']}", dado["metadados"]["gerado_em"][:10])
    linhas = cab + ["", (f"Esta é uma conta retrospectiva: nenhuma das seleções abaixo rodou de verdade. Para cada par de commits consecutivos que mexeram nas cobaias, ela "
                         f"pergunta que cenários a seleção deixaria de fora e o que a rodada completa `{c['corrida']}` mostra deles. Nessa rodada, {c['task_success']} das "
                         f"{c['execucoes']} execuções tiveram Task Success; os cenários com alguma execução sem sucesso foram: "
                         + (", ".join(f"`{x}`" for x in c["cenarios_com_falha"]) or "nenhum") + ". "
                         f"Dos {r['pares']} pares, {r['pares_que_rodam_tudo']} rodam tudo pela regra 1, {r['pares_seguros']} não deixam de fora nenhum cenário com falha e "
                         f"{r['pares_com_falha_perdida']} deixariam de fora um cenário que falhou na rodada completa. É para esses que existe a regra 2: a rodada completa "
                         "volta em prazo fixo, e a seleção só vale entre duas delas."), "",
                    f"<!-- tabela:{PREFIXO_DA_CONFERENCIA}pares -->",
                    "| Commit testado | Commit atual | Data | Veredito da seleção | Cenários selecionados | Deixados de fora | Falhas perdidas | Segura |", "|---|---|---|---|---|---|---|---|"]
    for p in dado["pares"]:
        linhas.append(f"| `{p['testado'][:8]}` | `{p['atual'][:8]}` | {p['data']} | {p['veredito']} | {len(p['selecionados'])} | {len(p['deixados_de_fora'])} | "
                      f"{', '.join(p['falhas_perdidas']) or 'nenhuma'} | {'sim' if p['segura'] else 'não'} |")
    linhas += [f"<!-- /tabela:{PREFIXO_DA_CONFERENCIA}pares -->", "", "Regra aplicada: " + dado["regra"] + ".", "", "Fontes: " + "; ".join(dado["metadados"]["fontes"]) + ".", ""]
    return "\n".join(linhas)


def conferir_corridas(selecionada: str, completa: str, check: bool = False) -> int:
    """A regra 3 para uma corrida selecionada de verdade: lê a decisão gravada na pasta dela e os registros das duas corridas, imprime a
    conferência e grava `conferencia_git.{json,md}` na pasta da corrida selecionada (com `check`, só compara)."""
    pasta = caminhos.RESULTADOS / selecionada
    ler = lambda arq: [json.loads(l) for l in arq.read_text(encoding="utf-8").splitlines() if l.strip()] if arq.exists() else []
    decisao = json.loads((pasta / ARQUIVO_DA_DECISAO).read_text(encoding="utf-8"))["decisao"]
    c = conferir(decisao, ler(pasta / "cenarios.jsonl"), ler(caminhos.RESULTADOS / completa / "cenarios.jsonl"))
    c["corridas"] = {"selecionada": selecionada, "completa": completa}
    md = render_conferencia(c, selecionada, completa)
    print(md)
    arq_json, arq_md = pasta / f"{NOME_DA_CONFERENCIA}.json", pasta / f"{NOME_DA_CONFERENCIA}.md"
    texto = json.dumps(c, ensure_ascii=False, indent=1)
    if check:
        igual = arq_json.exists() and arq_json.read_text(encoding="utf-8") == texto and arq_md.exists() and arq_md.read_text(encoding="utf-8") == md
        print("--check: " + ("bate com o gravado" if igual else "DIFERE do gravado"))
        return 0 if igual else 1
    arq_json.write_text(texto, encoding="utf-8", newline="\n")
    arq_md.write_text(md, encoding="utf-8", newline="\n")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--prova", action="store_true", help=f"a seleção em cada par de commits que mexeram nas cobaias -> resultados_alvo/fase4/{NOME}.{{json,md}}")
    ap.add_argument("--check", action="store_true", help="regera e compara com o que está gravado, sem gravar")
    ap.add_argument("--desde", default=None, help="commit testado: mostra a seleção para o que mudou dele até --ate")
    ap.add_argument("--ate", default="HEAD")
    ap.add_argument("--mapa", action="store_true", help="imprime o mapa dos cenários e dos verbetes")
    ap.add_argument("--decidir", action="store_true", help="Q7: o que uma corrida de cenários rodaria agora (o diff do último commit testado, ou de --desde, até a pasta de trabalho)")
    ap.add_argument("--conferir", default=None, help="Q7: a corrida selecionada a conferir contra a rodada completa de --completa (regra 3)")
    ap.add_argument("--conferir-historico", action="store_true",
                    help=f"Q7: a regra 3 como conta retrospectiva sobre os pares do histórico -> resultados_alvo/fase4/{NOME_DA_CONFERENCIA}.{{json,md}}")
    ap.add_argument("--completa", default="fase5_agente_b", help="a rodada completa da conferência (padrão: a corrida 28b)")
    args = ap.parse_args(argv)
    if args.decidir:
        d = decidir_para_a_corrida(desde=args.desde)
        print(f"modo: {d['modo']}\nmotivo: {d['motivo']}\ncommit testado: {d['commit_testado']}\ncommit atual: {d['commit_atual']}"
              f"{' (com alterações não commitadas nas cobaias)' if d['arvore_suja'] else ''}\ncenários: {', '.join(d['cenarios']) or 'nenhum'}\n"
              f"deixados de fora: {', '.join(d['deixados_de_fora']) or 'nenhum'}")
        return 0
    if args.conferir:
        return conferir_corridas(args.conferir, args.completa, check=args.check)
    if args.conferir_historico:
        dado, md = conferencia_historica(RAIZ, completa=args.completa)
        return pf.fechar(NOME_DA_CONFERENCIA, dado, md, PREFIXO_DA_CONFERENCIA, check=args.check, pasta=caminhos.RESULTADOS / "fase4", doc=RELATORIO_F4)
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
