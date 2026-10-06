#!/usr/bin/env python3
# ! Alteração de IA - Revisar: script novo (01/10/2026, Pré-Fase 4) que analisa a sonda de confiança (corrida 12): acha
# nos tokens gravados o trecho do rótulo da causa, calcula a probabilidade que o modelo deu a ele e mede se essa
# probabilidade separa os diagnósticos certos dos errados, ao lado dos dois sinais que não custam inferência (a causa
# respondida ser tratada por um verbete do contexto, e a causa respondida ser de uma classe que a rota de busca
# aponta). Grava resultados_alvo/pre_fase4/confianca.json e confianca.md (com --check e --colar).
# ! Motivo: o levantamento (§6.9.9 e §6.12.8) apontou a probabilidade do rótulo como sinal barato de incerteza e deixou
# em aberto se ela serve numa taxonomia de 23 causas com um modelo de 7B quantizado; a Fase 4 só deve usá-la para pedir
# revisão humana se a medida sustentar. A medida principal foi fixada ANTES de a corrida rodar, para o resultado não
# escolher a conta: a probabilidade conjunta dos tokens do rótulo que o modelo escreveu. As secundárias (o primeiro
# token do rótulo e a massa das alternativas que levariam a outra causa) saem ao lado e rotuladas como secundárias; a
# massa das alternativas é um limite inferior, porque o Ollama devolve só as 20 alternativas mais prováveis de cada
# posição. O intervalo de confiança reamostra CASOS (não linhas): com duas versões da biblioteca na mesma corrida, o
# mesmo caso aparece duas vezes, e tratá-las como independentes estreitaria o intervalo à toa.
"""Uso (em Programacao/AgenteCore/experimentos):
  RESULTADOS_DIR=resultados_alvo python analisar_confianca.py [--saida pre_fase4_confianca] [--check] [--colar]
"""
from __future__ import annotations

import argparse
import json
import math
import random
import sys
from datetime import datetime
from pathlib import Path

import analisar_fase3b as a3b
import avaliar
import biblioteca as bib
import caminhos
import executar_fase3
import gerar_atlas
import pre_fase4 as pf
import sonda_confianca as sc
import trilha

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass

NOME = "confianca"
PREFIXO = "tb_conf_"
MEDIDA_PRINCIPAL = "p_conjunta"
REPLICAS = 2000
SEMENTE = 20261001
FRACOES_DE_REVISAO = (0.1, 0.2, 0.3)
_MARCAS = "*`"
NOME_DO_SINAL = {"p_conjunta": "probabilidade conjunta dos tokens do rótulo (medida principal)",
                 "p_primeiro": "probabilidade do primeiro token do rótulo",
                 "um_menos_massa": "1 menos a massa das alternativas que levam a outra causa (limite inferior)",
                 "sustentado": "a causa respondida é tratada por um verbete do contexto (sim ou não, sem inferência)",
                 "coerente": "a causa respondida é de uma classe que a rota de busca aponta (sim ou não, sem inferência)"}


# ------------------------------------------------------------------ o trecho do rótulo e as probabilidades

def _bytes(t: dict) -> bytes:
    return bytes(t["bytes"]) if t.get("bytes") is not None else t.get("token", "").encode("utf-8")


def trecho_do_rotulo(tokens: list[dict]) -> dict | None:
    """Os tokens que escrevem o rótulo da causa (a primeira palavra depois de CAUSA_RAIZ:), achados pela posição em
    BYTES, porque um caractere acentuado pode vir partido entre dois tokens. A leitura do rótulo é a de
    trilha.localizar_declaracoes (a mesma de avaliar.extrair). Devolve `ini` e `fim` (índices dos tokens, fim
    exclusivo) e `texto`; None quando a resposta não tem a linha. O token que traz o fim do rótulo junto com a quebra
    de linha entra inteiro."""
    limites = [0]
    for t in tokens:
        limites.append(limites[-1] + len(_bytes(t)))
    texto = b"".join(_bytes(t) for t in tokens).decode("utf-8", errors="replace")
    campo = trilha.localizar_declaracoes(texto)["campos"]["causa_raiz"]
    if campo is None:
        return None
    b_ini, b_fim = len(texto[:campo["ini"]].encode("utf-8")), len(texto[:campo["fim"]].encode("utf-8"))
    dentro = [k for k in range(len(tokens)) if limites[k] < b_fim and limites[k + 1] > b_ini]
    if not dentro:
        return None
    return {"ini": dentro[0], "fim": dentro[-1] + 1, "texto": avaliar._normalizar(campo["valor"])}


def probabilidade_conjunta(tokens: list[dict], trecho: dict) -> float:
    return math.exp(sum(tokens[k]["logprob"] for k in range(trecho["ini"], trecho["fim"])))


def probabilidade_do_primeiro(tokens: list[dict], trecho: dict) -> float:
    return math.exp(tokens[trecho["ini"]]["logprob"])


def _parte_do_rotulo(texto_do_token: str, primeiro: bool) -> tuple[str, bool]:
    """Do texto de um token, a parte que pertence ao rótulo e se o token fecha o rótulo (tem espaço ou quebra de linha
    depois dela). No primeiro token do rótulo o espaço do começo não conta. Token só de marcas não diz nada ("", False);
    token que já começa por espaço ou quebra, depois do primeiro, fecha o rótulo no que estava escrito ("", True)."""
    limpo = "".join(ch for ch in texto_do_token if ch not in _MARCAS)
    if primeiro:
        limpo = limpo.lstrip()
    if not limpo:
        return "", False
    if limpo[0].isspace():
        return "", True
    palavra = limpo.split()[0]
    return palavra, len(limpo) > len(palavra)


def alternativas_divergentes(tokens: list[dict], trecho: dict, causas: list[str]) -> dict:
    """Em cada posição do rótulo, as alternativas que o modelo pesou e que levariam a OUTRA causa do conjunto: o que
    já foi escrito do rótulo mais a alternativa é começo (ou, se a alternativa fecha o rótulo, o nome inteiro) de uma
    causa diferente da respondida. A massa de cada uma é a probabilidade do que já foi escrito vezes a da alternativa.
    A soma é um limite inferior da probabilidade de outra causa (só as alternativas devolvidas entram). `segunda` é a
    de maior massa, com as causas a que ela leva."""
    respondida = trecho["texto"]
    escrito, acumulada = "", 1.0
    massa, segunda = 0.0, None
    for k in range(trecho["ini"], trecho["fim"]):
        t = tokens[k]
        primeiro = escrito == ""
        for alt in t.get("top_logprobs") or []:
            if alt["token"] == t["token"]:
                continue
            parte, fecha = _parte_do_rotulo(alt["token"], primeiro)
            candidato = avaliar._normalizar(escrito + parte)
            if not candidato or (not parte and not fecha):
                continue
            compativeis = [c for c in causas if (c == candidato if fecha else c.startswith(candidato))]
            if not compativeis or respondida in compativeis:
                continue
            m = acumulada * math.exp(alt["logprob"])
            massa += m
            if segunda is None or m > segunda["p"]:
                segunda = {"causas": compativeis, "p": m, "token": alt["token"], "posicao": k - trecho["ini"]}
        parte, _ = _parte_do_rotulo(t["token"], primeiro)
        escrito += parte
        acumulada *= math.exp(t["logprob"])
    return {"massa_divergente": massa, "segunda": segunda}


def gabarito_na_segunda(divergentes: dict, gabarito: str) -> bool:
    """A causa certa era a alternativa de maior massa que o modelo deixou de escolher?"""
    s = divergentes.get("segunda")
    return bool(s) and avaliar._normalizar(gabarito) in s["causas"]


# ------------------------------------------------------------------ separa acerto de erro?

def auroc(notas: list[float], acertos: list[bool]) -> float | None:
    """A chance de um diagnóstico certo, tirado ao acaso, ter nota maior que um errado tirado ao acaso (empate vale
    meio). 0,5 é o mesmo que sortear; 1,0 separa tudo. None quando só há certos ou só há errados."""
    certos = [n for n, a in zip(notas, acertos) if a]
    errados = [n for n, a in zip(notas, acertos) if not a]
    if not certos or not errados:
        return None
    soma = sum(1.0 if c > e else 0.5 if c == e else 0.0 for c in certos for e in errados)
    return soma / (len(certos) * len(errados))


def auroc_com_intervalo(notas: list[float], acertos: list[bool], grupos: list[str], replicas: int = REPLICAS, semente: int = SEMENTE) -> dict:
    """AUROC com intervalo de 95% por reamostragem dos CASOS (`grupos`: o caso de cada linha): cada réplica sorteia
    casos com reposição e leva todas as linhas de cada caso sorteado. Réplica sem certos ou sem errados é descartada."""
    base = {"n": len(notas), "casos": len(set(grupos)), "erros": sum(1 for a in acertos if not a)}
    valor = auroc(notas, acertos)
    if valor is None:
        return {**base, "auroc": None, "ic95": None, "replicas_validas": 0}
    por_caso: dict[str, list[int]] = {}
    for k, g in enumerate(grupos):
        por_caso.setdefault(g, []).append(k)
    chaves = sorted(por_caso)
    sorteio = random.Random(semente)
    valores = []
    for _ in range(replicas):
        idx = [k for g in (sorteio.choice(chaves) for _ in chaves) for k in por_caso[g]]
        v = auroc([notas[k] for k in idx], [acertos[k] for k in idx])
        if v is not None:
            valores.append(v)
    valores.sort()
    ic = [round(valores[int(0.025 * (len(valores) - 1))], 4), round(valores[int(0.975 * (len(valores) - 1))], 4)] if valores else None
    return {**base, "auroc": round(valor, 4), "ic95": ic, "replicas_validas": len(valores)}


def risco_por_cobertura(notas: list[float], acertos: list[bool]) -> list[dict]:
    """Respondendo só os k diagnósticos de maior nota: a cobertura (k sobre o total) e o risco (erros entre os k)."""
    ordem = sorted(range(len(notas)), key=lambda k: (-notas[k], k))
    pontos, erros = [], 0
    for k, i in enumerate(ordem, 1):
        erros += not acertos[i]
        pontos.append({"cobertura": round(k / len(notas), 4), "risco": erros / k, "limiar": notas[i]})
    return pontos


def revisao(notas: list[float], acertos: list[bool], fracao: float) -> dict:
    """Mandando para revisão humana a fração de menor nota: quantos erros ela pega e quantos acertos revisa à toa."""
    n = len(notas)
    k = int(round(fracao * n))
    ordem = sorted(range(n), key=lambda i: (notas[i], i))
    revisados, resto = ordem[:k], ordem[k:]
    erros = sum(1 for a in acertos if not a)
    pegos = sum(1 for i in revisados if not acertos[i])
    return {"revisados": k, "erros_pegos": pegos, "erros": erros, "acertos_revisados": k - pegos,
            "risco_no_que_sobra": round(sum(1 for i in resto if not acertos[i]) / len(resto), 4) if resto else None}


# ------------------------------------------------------------------ leitura da corrida

def _jsonl(arq: Path) -> list[dict]:
    return [json.loads(l) for l in arq.read_text(encoding="utf-8").splitlines() if l.strip()] if arq.exists() else []


def _rotas_da_base(hash_da_biblioteca: str) -> dict[str, list[str]] | None:
    """As rotas dos casos oficiais para esta biblioteca, lidas da corrida oficial (None se ela não estiver no disco ou
    não tiver lido esta biblioteca): é o que o atlas usa para dizer que classe a rota de um caso aponta."""
    if not caminhos.fase3(gerar_atlas.BASE)["raiz"].exists():
        return None
    for f in gerar_atlas.ler_fatias([gerar_atlas.BASE]):
        if f["biblioteca"] == hash_da_biblioteca:
            return {r["caso"]: list(r.get("verbetes_ids") or []) for r in f["registros"]}
    return None


def montar(saida: str = sc.SAIDA_PADRAO, replicas: int = REPLICAS, gerado_em: str | None = None) -> dict:
    c3 = caminhos.fase3(saida)
    todos = trilha._todos_os_casos()
    classe_do_caso = {i: c["classe"] for i, c in todos.items()}
    classes_da_causa: dict[str, set] = {}
    for c in todos.values():
        classes_da_causa.setdefault(c["gabarito"]["causa_raiz"], set()).add(c["classe"])
    causas = sorted(avaliar._PERMITIDAS)
    oficiais = _casos_oficiais()
    linhas = []
    for arq in sorted(c3["raiz"].glob("*/diagnosticos__L*.jsonl")):
        versao = int(arq.stem.split("__L")[1])
        slug = arq.parent.name
        registros = _jsonl(arq)
        laterais = {l["caso"]: l for l in _jsonl(arq.parent / f"logprobs__L{versao}.jsonl")}
        verbetes = bib.carregar(c3["bibliotecas"] / slug / f"epoca-{versao}")
        ids = sorted(v["id"] for v in verbetes)
        base = _rotas_da_base(registros[0]["biblioteca_versao"]) if registros else None
        atlas_inteiro = gerar_atlas.atlas_de_recuperacao(base, classe_do_caso, ids, gerar_atlas.CLASSES) if base else None
        for r in registros:
            lat = laterais.get(r["caso"])
            if lat is None:
                raise SystemExit(f"{arq}: caso {r['caso']} sem linha em logprobs__L{versao}.jsonl")
            tokens = sc.expandir(lat["logprobs"])
            lido = avaliar.extrair(r["resposta"])
            acerto = bool(avaliar.avaliar_registro(r, set())["causa_correta"])
            decl = trilha.localizar_declaracoes(r["resposta"])
            ver = {v["regra"]: v for v in trilha.verificar(r, todos[r["caso"]], verbetes, decl)}
            sustentado = ver["rotulo_sustentado_por_verbete_do_contexto"]["resultado"] == "confere"
            coerente = None
            if atlas_inteiro is not None:
                rota = list(r.get("verbetes_ids") or [])
                at = (gerar_atlas.atlas_de_recuperacao({c: x for c, x in base.items() if c != r["caso"]}, classe_do_caso, ids, gerar_atlas.CLASSES)
                      if r["caso"] in base else atlas_inteiro)
                prevista = gerar_atlas.prever_classe(rota, at, gerar_atlas.CLASSES)[0]
                coerente = None if prevista is None else prevista in classes_da_causa.get(lido["causa_raiz"] or "", set())
            linha = {"caso": r["caso"], "modelo": r["modelo"], "versao": versao, "classe": r["classe"],
                     "conjunto": "oficiais" if r["caso"] in oficiais else "ineditos",
                     "gabarito": r["gabarito"]["causa_raiz"], "rotulo": lido["causa_raiz"], "acerto": acerto,
                     "sustentado": sustentado, "coerente": coerente, "p_conjunta": None, "p_primeiro": None, "massa_divergente": None,
                     "tokens_do_rotulo": 0, "segunda": None, "gabarito_na_segunda": None}
            trecho = trecho_do_rotulo(tokens)
            if trecho is not None:
                if trecho["texto"] != avaliar._normalizar(lido["causa_raiz"] or ""):
                    raise SystemExit(f"caso {r['caso']}: o rótulo achado nos tokens ({trecho['texto']}) não é o que o avaliador leu ({lido['causa_raiz']})")
                div = alternativas_divergentes(tokens, trecho, causas)
                linha.update({"p_conjunta": round(probabilidade_conjunta(tokens, trecho), 6), "p_primeiro": round(probabilidade_do_primeiro(tokens, trecho), 6),
                              "massa_divergente": round(div["massa_divergente"], 6), "tokens_do_rotulo": trecho["fim"] - trecho["ini"],
                              "segunda": None if div["segunda"] is None else {"causas": div["segunda"]["causas"], "p": round(div["segunda"]["p"], 6)},
                              "gabarito_na_segunda": gabarito_na_segunda(div, r["gabarito"]["causa_raiz"])})
            linhas.append(linha)

    grupos_de_linhas = [("todas as versões", linhas)] if len({(l["modelo"], l["versao"]) for l in linhas}) > 1 else []
    for chave in sorted({(l["modelo"], l["versao"]) for l in linhas}):
        grupos_de_linhas.append((f"{chave[0]}, L{chave[1]}", [l for l in linhas if (l["modelo"], l["versao"]) == chave]))
    resumos = [_resumo(nome, ls, replicas) for nome, ls in grupos_de_linhas]
    return {"metadados": {"script": "analisar_confianca.py", "gerado_em": gerado_em or datetime.now().isoformat(timespec="seconds"),
                          "saida": saida, "medida_principal": MEDIDA_PRINCIPAL, "replicas": replicas, "semente": SEMENTE,
                          "nota_sobre_a_massa": "limite inferior: só entram as alternativas que o Ollama devolveu em cada posição",
                          "pareamento_com_a_fase_3": _pareamento(linhas)},
            "resumos": resumos, "casos": linhas}


def _casos_oficiais() -> set[str]:
    from banco_casos import CASOS
    from banco_casos_extra import CASOS_EXTRA
    return {c["id"] for c in list(CASOS) + list(CASOS_EXTRA)}


def _pareamento(linhas: list[dict]) -> list[dict]:
    """Por modelo e versão: quantos rótulos dos casos oficiais saíram iguais aos da corrida oficial da Fase 3 (os casos
    de texto corrigido em 28/09 ficam de fora, porque a entrada mudou)."""
    saida = []
    for modelo, versao in sorted({(l["modelo"], l["versao"]) for l in linhas}):
        arq = caminhos.fase3("fase3")["raiz"] / executar_fase3._slug(modelo) / f"diagnosticos__L{versao}.jsonl"
        oficiais = {r["caso"]: avaliar.extrair(r["resposta"])["causa_raiz"] for r in _jsonl(arq)}
        pares = [(l["rotulo"], oficiais[l["caso"]]) for l in linhas if (l["modelo"], l["versao"]) == (modelo, versao)
                 and l["caso"] in oficiais and l["caso"] not in a3b.CASOS_DE_TEXTO_ALTERADO]
        if pares:
            saida.append({"modelo": modelo, "versao": versao, "casos": len(pares), "rotulos_iguais": sum(1 for a, b in pares if a == b)})
    return saida


def _resumo(nome: str, linhas: list[dict], replicas: int) -> dict:
    com_p = [l for l in linhas if l["p_conjunta"] is not None]
    acertos = [l["acerto"] for l in com_p]
    grupos = [l["caso"] for l in com_p]
    sinais = {
        "p_conjunta": auroc_com_intervalo([l["p_conjunta"] for l in com_p], acertos, grupos, replicas),
        "p_primeiro": auroc_com_intervalo([l["p_primeiro"] for l in com_p], acertos, grupos, replicas),
        "um_menos_massa": auroc_com_intervalo([1 - l["massa_divergente"] for l in com_p], acertos, grupos, replicas),
        "sustentado": auroc_com_intervalo([1.0 if l["sustentado"] else 0.0 for l in com_p], acertos, grupos, replicas),
    }
    com_rota = [l for l in com_p if l["coerente"] is not None]
    if com_rota:
        sinais["coerente"] = auroc_com_intervalo([1.0 if l["coerente"] else 0.0 for l in com_rota], [l["acerto"] for l in com_rota], [l["caso"] for l in com_rota], replicas)
    pontos = risco_por_cobertura([l["p_conjunta"] for l in com_p], acertos) if com_p else []
    erros = [l for l in com_p if not l["acerto"]]
    return {"nome": nome, "casos": len(linhas), "sem_rotulo": len(linhas) - len(com_p), "erros": sum(1 for l in linhas if not l["acerto"]),
            "acerto_pct": round(100 * sum(1 for l in linhas if l["acerto"]) / len(linhas), 1) if linhas else None,
            "sinais": sinais,
            "p_conjunta_mediana": {"certos": _mediana([l["p_conjunta"] for l in com_p if l["acerto"]]), "errados": _mediana([l["p_conjunta"] for l in erros])},
            "area_sob_risco": round(sum(p["risco"] for p in pontos) / len(pontos), 4) if pontos else None,
            "revisao": [{"fracao": fr, **revisao([l["p_conjunta"] for l in com_p], acertos, fr)} for fr in FRACOES_DE_REVISAO] if com_p else [],
            "erros_com_o_gabarito_na_segunda": sum(1 for l in erros if l["gabarito_na_segunda"])}


def _mediana(valores: list[float]) -> float | None:
    if not valores:
        return None
    v = sorted(valores)
    meio = len(v) // 2
    return round(v[meio] if len(v) % 2 else (v[meio - 1] + v[meio]) / 2, 6)


# ------------------------------------------------------------------ Markdown derivado

def _f(v, casas: int = 3) -> str:
    return "n/d" if v is None else f"{v:.{casas}f}".replace(".", ",")


def _sinal(s: dict | None) -> str:
    if not s or s["auroc"] is None:
        return "n/d"
    return f"{_f(s['auroc'])} [{_f(s['ic95'][0])} a {_f(s['ic95'][1])}]" if s["ic95"] else _f(s["auroc"])


def render(dado: dict) -> str:
    meta = dado["metadados"]
    md = pf.cabecalho("Sonda de confiança: a probabilidade do rótulo separa acerto de erro?", "analisar_confianca.py",
                      f"os registros e os arquivos `logprobs__L<n>.jsonl` de `{meta['saida']}`", meta["gerado_em"][:10])
    md += ["", f"Medida principal, fixada antes da corrida: {NOME_DO_SINAL['p_conjunta'].split(' (')[0]}. A coluna de cada sinal traz a AUROC (0,5 é o mesmo que "
           f"sortear; 1,0 separa tudo) e, entre colchetes, o intervalo de 95% por reamostragem dos casos ({meta['replicas']} réplicas, semente {meta['semente']}). "
           f"A massa das alternativas é {meta['nota_sobre_a_massa']}.", ""]
    md += ["<!-- tabela:tb_conf_resumo -->",
           "| Recorte | Casos | Erros | Probabilidade conjunta do rótulo | Primeiro token do rótulo | 1 menos a massa de outra causa | Causa tratada por verbete do contexto | "
           "Causa na classe que a rota aponta | Mediana da conjunta nos certos | Mediana nos errados | Erros com a causa certa como segunda opção |",
           "|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in dado["resumos"]:
        s = r["sinais"]
        md.append(f"| {r['nome']} | {r['casos']} | {r['erros']} | {_sinal(s['p_conjunta'])} | {_sinal(s['p_primeiro'])} | {_sinal(s['um_menos_massa'])} | "
                  f"{_sinal(s['sustentado'])} | {_sinal(s.get('coerente'))} | {_f(r['p_conjunta_mediana']['certos'])} | {_f(r['p_conjunta_mediana']['errados'])} | "
                  f"{r['erros_com_o_gabarito_na_segunda']} de {r['erros']} |")
    md += ["<!-- /tabela:tb_conf_resumo -->", "",
           "Se o agente mandar para revisão humana a parcela de menor probabilidade conjunta: quantos erros ela pega, quantos acertos são revisados à toa e o risco no que sobra.", "",
           "<!-- tabela:tb_conf_revisao -->",
           "| Recorte | Parcela revisada | Casos revisados | Erros pegos | Acertos revisados à toa | Risco no que sobra |",
           "|---|---|---|---|---|---|"]
    for r in dado["resumos"]:
        for x in r["revisao"]:
            md.append(f"| {r['nome']} | {_f(100 * x['fracao'], 0)}% | {x['revisados']} | {x['erros_pegos']} de {x['erros']} | {x['acertos_revisados']} | "
                      f"{'n/d' if x['risco_no_que_sobra'] is None else _f(100 * x['risco_no_que_sobra'], 1) + '%'} |")
    md += ["<!-- /tabela:tb_conf_revisao -->", "", "Caso a caso, da menor probabilidade conjunta para a maior:", "",
           "<!-- tabela:tb_conf_casos -->",
           "| Caso | Biblioteca | Conjunto | Resultado | Causa respondida | Probabilidade conjunta | Primeiro token | Massa de outra causa | Segunda opção | Tratada por verbete do contexto | Na classe da rota |",
           "|---|---|---|---|---|---|---|---|---|---|---|"]
    sim_nao = {True: "sim", False: "não", None: "n/d"}
    for l in sorted(dado["casos"], key=lambda l: (l["p_conjunta"] is None, l["p_conjunta"] or 0, l["caso"], l["versao"])):
        segunda = "nenhuma" if not l["segunda"] else f"{' ou '.join(l['segunda']['causas'])} ({_f(l['segunda']['p'])})"
        md.append(f"| `{l['caso']}` | L{l['versao']} | {l['conjunto']} | {'certo' if l['acerto'] else 'errado'} | `{l['rotulo']}` | {_f(l['p_conjunta'])} | {_f(l['p_primeiro'])} | "
                  f"{_f(l['massa_divergente'])} | {segunda} | {sim_nao[l['sustentado']]} | {sim_nao[l['coerente']]} |")
    md += ["<!-- /tabela:tb_conf_casos -->", ""]
    if meta["pareamento_com_a_fase_3"]:
        md += ["Rótulos iguais aos da corrida oficial da Fase 3 nos casos oficiais (sem os casos de texto corrigido em 28/09): "
               + "; ".join(f"`{p['modelo']}` L{p['versao']}: {p['rotulos_iguais']} de {p['casos']}" for p in meta["pareamento_com_a_fase_3"]) + ".", ""]
    return "\n".join(md)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--saida", default=sc.SAIDA_PADRAO)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--colar", action="store_true")
    args = ap.parse_args()
    print(caminhos.descricao())
    if not list(caminhos.fase3(args.saida)["raiz"].glob("*/diagnosticos__L*.jsonl")):
        print(f"a corrida {args.saida} ainda não rodou (sem diagnósticos em {caminhos.fase3(args.saida)['raiz']}): nada a analisar")
        return 0
    dado = montar(args.saida)
    return pf.fechar(NOME, dado, render(dado), PREFIXO, check=args.check, colar=args.colar)


if __name__ == "__main__":
    sys.exit(main())
