#!/usr/bin/env python3
# ! Alteração de IA - Revisar: script novo (01/10/2026, Pré-Fase 4) que monta o ATLAS do projeto com os dados que já
# medimos: para cada versão da biblioteca, em quantos casos de cada classe de defeito cada verbete entrou no contexto
# (a "rota" do caso), o quanto ele é de uma classe só, onde ele fica no desenho, quantas vezes cada modelo o citou e
# com que acerto, as confusões entre causas e a rota de cada caso em cada corrida. Grava
# resultados_alvo/pre_fase4/atlas.json e atlas.md (com --check), e é a fonte da aba "Atlas" do painel.
# ! Motivo: o Eric pediu (01/10/2026) para validar o "expert atlas" do repositório colibri e levar uma visualização
# desse tipo para o painel. Os modelos do projeto são densos, sem especialistas que um roteador escolha, então o que
# se transfere é o MÉTODO de medição do atlas (c/tools/expert_atlas do colibri; levantamento §6.14.5): contar por
# item independente e não por token, corrigir pela taxa de base de cada classe, exigir repetição em pelo menos dois
# itens e validar deixando um item de fora. Aqui o item é o caso de teste, a entidade é o verbete da biblioteca e a
# escolha é a da busca (BM25 com os reforços de endpoint, entidade e status), que põe três verbetes no contexto de
# cada caso. Duas ressalvas ficam gravadas no próprio dado: parte da afinidade vem do desenho da biblioteca (um
# verbete de erro por causa, e reforços calculados em código), e a posição no desenho é a média das âncoras das seis
# classes ponderada pela afinidade medida, não uma semelhança de significado. Só leitura dos registros oficiais.
"""Uso (em Programacao/AgenteCore/experimentos):
  RESULTADOS_DIR=resultados_alvo python gerar_atlas.py [--check] [--colar]
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

import avaliar
import biblioteca as bib
import caminhos
import executar_fase3
import pre_fase4 as pf
import taxonomia

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass

NOME = "atlas"
PREFIXO = "tb_atlas_"
# Os dois limiares são os do expert_atlas do colibri: especialista a partir de 0,5 de especialização, e só com
# evidência repetida em pelo menos dois itens independentes (aqui, dois casos distintos).
LIMIAR_ESPECIALISTA = 0.5
MINIMO_DE_CASOS = 2
# Corridas lidas, na ordem em que as fatias aparecem; a primeira é a base: os 90 casos oficiais definem o atlas de cada
# biblioteca, e as outras entram como rotas, citações e, nos casos inéditos, previsão fora da amostra.
CORRIDAS = ["fase3", "fase3b_ineditos", "fase3b_cruzada_qwen"]
BASE = "fase3"
# Decisão 52: o modelo e a versão da biblioteca escolhidos para a Fase 4.
MODELO_DECIDIDO, VERSAO_DECIDIDA = "qwen2.5:7b", 1
CLASSES = sorted(taxonomia.CLASSES)
NOME_DA_CLASSE = {1: "léxica", 2: "sintática", 3: "semântica", 4: "tradução", 5: "runtime", 6: "efeito"}
NOME_DO_ROTULO = {"especialista": "especialista", "generalista": "generalista", "sem_repeticao": "sem repetição",
                  "nunca_recuperado": "nunca recuperado"}
ANGULO_DE_OURO = math.pi * (3 - math.sqrt(5))


# ------------------------------------------------------------------ o método (funções puras)

def afinidade(n: dict[int, int], total_por_classe: dict[int, int]) -> dict:
    """Do número de casos distintos de cada classe em que a entidade apareceu (`n`) e do total de casos de cada classe:
    a taxa por classe (`f`, que corrige a taxa de base), a afinidade (`p`, as taxas levadas a somar 1), a entropia em
    bits e a especialização (1 menos a entropia sobre o máximo, log2 do número de classes). As listas seguem a ordem
    crescente das classes."""
    classes = sorted(total_por_classe)
    contagem = [int(n.get(c, 0)) for c in classes]
    f = [contagem[i] / total_por_classe[c] if total_por_classe[c] else 0.0 for i, c in enumerate(classes)]
    soma = sum(f)
    if not soma:
        return {"n": contagem, "f": [round(x, 4) for x in f], "p": None, "entropia_bits": None, "especializacao": None,
                "dominante": None, "itens": 0}
    p = [x / soma for x in f]
    entropia = -sum(x * math.log2(x) for x in p if x > 0)
    especializacao = 1 - entropia / math.log2(len(classes)) if len(classes) > 1 else None
    maior = max(p)
    dominantes = [c for c, x in zip(classes, p) if abs(x - maior) < 1e-12]
    return {"n": contagem, "f": [round(x, 4) for x in f], "p": [round(x, 4) for x in p], "entropia_bits": round(entropia, 3) + 0.0,
            "especializacao": None if especializacao is None else round(max(0.0, especializacao), 3),
            "dominante": dominantes[0] if len(dominantes) == 1 else None, "itens": sum(contagem)}


def rotular(itens: int, especializacao: float | None) -> str:
    """nunca_recuperado, sem_repeticao (menos de MINIMO_DE_CASOS casos distintos: não dá para chamar de nada),
    especialista (especialização a partir do limiar) ou generalista."""
    if not itens:
        return "nunca_recuperado"
    if itens < MINIMO_DE_CASOS:
        return "sem_repeticao"
    return "especialista" if especializacao is not None and especializacao >= LIMIAR_ESPECIALISTA else "generalista"


def atlas_de_recuperacao(rotas: dict[str, list[str]], classe_do_caso: dict[str, int], ids: list[str],
                         classes: list[int] | None = None) -> dict[str, dict]:
    """O atlas de uma biblioteca: para cada verbete, a afinidade com as classes medida pelas rotas (`rotas[caso]` é a
    lista dos verbetes que a busca pôs no contexto do caso, na ordem). Conta casos distintos: um verbete que aparece
    duas vezes na rota do mesmo caso conta uma vez."""
    classes = classes or sorted(set(classe_do_caso[c] for c in rotas))
    total = {c: 0 for c in classes}
    for caso in rotas:
        total[classe_do_caso[caso]] += 1
    contagem: dict[str, Counter] = {i: Counter() for i in ids}
    primeiro: Counter = Counter()
    for caso, rota in rotas.items():
        for i in dict.fromkeys(rota):
            contagem.setdefault(i, Counter())[classe_do_caso[caso]] += 1
        if rota:
            primeiro[rota[0]] += 1
    saida = {}
    for i in sorted(contagem):
        a = afinidade(contagem[i], total)
        saida[i] = {**a, "rotulo": rotular(a["itens"], a["especializacao"]), "vezes_em_primeiro": primeiro.get(i, 0)}
    return saida


def prever_classe(recuperados: list[str], atlas: dict[str, dict], classes: list[int]) -> tuple[int | None, dict[int, float]]:
    """A classe que o atlas atribui a um caso pelos verbetes da rota dele: soma das afinidades de cada verbete, e a
    classe de maior soma. Empate ou rota sem nenhum verbete com evidência devolvem None."""
    pontos = {c: 0.0 for c in classes}
    com_evidencia = False
    for i in dict.fromkeys(recuperados):
        p = (atlas.get(i) or {}).get("p")
        if p:
            com_evidencia = True
            for c, x in zip(classes, p):
                pontos[c] += x
    if not com_evidencia:
        return None, {}
    pontos = {c: round(x, 4) for c, x in pontos.items()}
    maior = max(pontos.values())
    vencedores = [c for c in classes if abs(pontos[c] - maior) < 1e-9]
    return (vencedores[0] if len(vencedores) == 1 else None), pontos


def _resumo_da_previsao(previsoes: list[tuple[str, int, int | None, bool]], classes: list[int]) -> dict:
    """previsoes: (caso, classe verdadeira, classe prevista ou None, havia evidência?)."""
    acertos = sum(1 for _, c, p, _ in previsoes if p == c)
    erros = [{"caso": caso, "classe": c, "previsto": p, "motivo": "sem_evidencia" if not ev else ("empate" if p is None else "outra_classe")}
             for caso, c, p, ev in previsoes if p != c]
    return {"total": len(previsoes), "acertos": acertos, "acerto_pct": round(100 * acertos / len(previsoes), 1) if previsoes else None,
            "empates": sum(1 for e in erros if e["motivo"] == "empate"), "sem_evidencia": sum(1 for e in erros if e["motivo"] == "sem_evidencia"),
            "acaso_pct": round(100 / len(classes), 1),
            "por_classe": [{"classe": k, "n": sum(1 for _, c, _, _ in previsoes if c == k), "acertos": sum(1 for _, c, p, _ in previsoes if c == k and p == c)}
                           for k in classes if any(c == k for _, c, _, _ in previsoes)],
            "erros": erros}


def previsoes_deixando_um_de_fora(rotas: dict[str, list[str]], classe_do_caso: dict[str, int], ids: list[str],
                                  classes: list[int] | None = None) -> dict[str, int | None]:
    """Para cada caso, a classe prevista por um atlas montado sem ele (None em empate ou sem evidência)."""
    classes = classes or sorted(set(classe_do_caso[c] for c in rotas))
    saida = {}
    for caso in rotas:
        resto = {c: r for c, r in rotas.items() if c != caso}
        saida[caso] = prever_classe(rotas[caso], atlas_de_recuperacao(resto, classe_do_caso, ids, classes), classes)
    return saida


def deixar_um_de_fora(rotas: dict[str, list[str]], classe_do_caso: dict[str, int], ids: list[str],
                      classes: list[int] | None = None) -> dict:
    """A validação do expert_atlas: tira um caso, monta o atlas com os outros e pergunta de que classe é o caso tirado.
    Empate e falta de evidência contam como erro."""
    classes = classes or sorted(set(classe_do_caso[c] for c in rotas))
    prev = previsoes_deixando_um_de_fora(rotas, classe_do_caso, ids, classes)
    return _resumo_da_previsao([(caso, classe_do_caso[caso], p, bool(pontos)) for caso, (p, pontos) in prev.items()], classes)


def fora_da_amostra(atlas: dict[str, dict], classes: list[int], rotas: dict[str, list[str]], classe_do_caso: dict[str, int]) -> dict:
    """O atlas pronto prevê a classe de casos que não entraram na conta dele (os inéditos)."""
    previsoes = []
    for caso, rota in rotas.items():
        p, pontos = prever_classe(rota, atlas, classes)
        previsoes.append((caso, classe_do_caso[caso], p, bool(pontos)))
    return _resumo_da_previsao(previsoes, classes)


def ancoras(classes: list[int]) -> dict[int, dict]:
    """A âncora de cada classe num círculo de raio 1, a primeira no alto e as outras no sentido horário."""
    return {c: {"x": round(math.cos(-math.pi / 2 + 2 * math.pi * k / len(classes)), 4),
                "y": round(math.sin(-math.pi / 2 + 2 * math.pi * k / len(classes)), 4)} for k, c in enumerate(classes)}


def raio_do_no(itens: int) -> float:
    return round(0.034 + 0.0125 * math.sqrt(itens), 4)


def posicoes(atlas: dict[str, dict], classes: list[int]) -> dict[str, dict]:
    """Onde cada verbete fica no desenho: a média das âncoras das classes ponderada pela afinidade (quem é de uma classe
    só fica na âncora dela; quem se reparte fica no meio), seguida de um afastamento só o bastante para dois nós não
    ficarem um em cima do outro. Verbete nunca recuperado não tem afinidade: vai para uma fila fora do círculo
    (`fora`). O resultado não depende da ordem de entrada nem de sorteio."""
    anc = ancoras(classes)
    ordem = sorted(atlas)
    dentro = [i for i in ordem if atlas[i].get("p")]
    alvo = {i: (sum(p * anc[c]["x"] for c, p in zip(classes, atlas[i]["p"])), sum(p * anc[c]["y"] for c, p in zip(classes, atlas[i]["p"]))) for i in dentro}
    raio = {i: raio_do_no(atlas[i]["itens"]) for i in ordem}
    pos = {i: [alvo[i][0], alvo[i][1]] for i in dentro}
    folga = 0.012

    def afastar() -> None:
        for a_idx, a in enumerate(dentro):
            for b_idx in range(a_idx + 1, len(dentro)):
                b = dentro[b_idx]
                dx, dy = pos[b][0] - pos[a][0], pos[b][1] - pos[a][1]
                d = math.hypot(dx, dy)
                minimo = raio[a] + raio[b] + folga
                if d >= minimo:
                    continue
                if d < 1e-9:      # no mesmo ponto: a direção sai dos índices, sempre a mesma
                    ang = ANGULO_DE_OURO * (a_idx * 31 + b_idx)
                    dx, dy, d = math.cos(ang), math.sin(ang), 1.0
                passo = (minimo - d) / 2
                pos[a][0] -= dx / d * passo
                pos[a][1] -= dy / d * passo
                pos[b][0] += dx / d * passo
                pos[b][1] += dy / d * passo

    for _ in range(260):
        afastar()
        for i in dentro:  # puxa de volta para o lugar medido, para o afastamento não levar ninguém para longe
            pos[i][0] += (alvo[i][0] - pos[i][0]) * 0.03
            pos[i][1] += (alvo[i][1] - pos[i][1]) * 0.03
    for _ in range(400):
        afastar()
    saida = {i: {"x": round(pos[i][0], 4), "y": round(pos[i][1], 4), "r": raio[i], "fora": False} for i in dentro}
    fora = [i for i in ordem if i not in pos]
    passo = 0.16
    for k, i in enumerate(fora):
        saida[i] = {"x": round((k - (len(fora) - 1) / 2) * passo, 4), "y": 1.42, "r": raio[i], "fora": True}
    return saida


# ------------------------------------------------------------------ leitura das corridas

def _jsonl(arq: Path) -> list[dict]:
    return [json.loads(l) for l in arq.read_text(encoding="utf-8").splitlines() if l.strip()]


def ler_fatias(corridas: list[str]) -> list[dict]:
    """Uma fatia por arquivo de diagnósticos gravado (corrida, modelo, versão da biblioteca), com os registros."""
    fatias = []
    for corrida in corridas:
        c3 = caminhos.fase3(corrida)
        arq_cond = c3["raiz"] / "condicoes_3b.json"
        cond = json.loads(arq_cond.read_text(encoding="utf-8")) if arq_cond.exists() else {}
        for arq in sorted(c3["raiz"].glob("*/diagnosticos__L*.jsonl")):
            registros = _jsonl(arq)
            if not registros:
                continue
            versao = int(arq.stem.split("__L")[1])
            hashes = sorted({str(r.get("biblioteca_versao")) for r in registros})
            if len(hashes) != 1:
                raise SystemExit(f"{arq}: registros com mais de uma biblioteca ({hashes})")
            modelo = registros[0]["modelo"]
            fatias.append({"id": f"{corrida}/{arq.parent.name}/L{versao}", "corrida": corrida, "conjunto": cond.get("modo") or "oficiais",
                           "modelo": modelo, "slug": arq.parent.name, "versao": versao, "biblioteca": hashes[0],
                           "dono_da_biblioteca": cond.get("doador") or modelo, "registros": registros,
                           "snapshot": c3["bibliotecas"] / arq.parent.name / f"epoca-{versao}"})
    return fatias


def _resumo_da_fatia(f: dict, previsao: dict[str, int | None] | None, classes_da_causa: dict[str, set] | None = None) -> dict:
    """Acerto, competência por causa, confusões entre causas, citações por verbete e dois cruzamentos com o acerto do
    modelo. `rota_e_acerto`: a rota aponta a classe verdadeira do caso? (usa o gabarito; serve para entender.)
    `resposta_e_rota`: a causa que o modelo respondeu é de uma classe que a rota aponta? (não usa o gabarito do caso;
    é um sinal que o agente pode calcular sozinho.) `previsao`: classe prevista pelo atlas para cada caso."""
    regs = f["registros"]
    causas: dict[str, dict] = {}
    confusoes: Counter = Counter()
    citacoes: dict[str, dict] = {}
    fora_do_contexto = 0
    acertos = 0
    cruz = {"aponta": {"n": 0, "acertos": 0}, "nao_aponta": {"n": 0, "acertos": 0}}
    coerencia = {"coerente": {"n": 0, "acertos": 0}, "incoerente": {"n": 0, "acertos": 0}, "sem_previsao": {"n": 0, "acertos": 0}}
    for r in regs:
        av = avaliar.avaliar_registro(r, set())
        lido = avaliar.extrair(r.get("resposta", ""))
        ok = bool(av["causa_correta"])
        acertos += ok
        gab = r["gabarito"]["causa_raiz"]
        c = causas.setdefault(gab, {"n": 0, "acertos": 0})
        c["n"] += 1
        c["acertos"] += ok
        if not ok:
            confusoes[(gab, lido["causa_raiz"])] += 1
        for i in dict.fromkeys(lido["fonte_ids"]):
            if i not in (r.get("verbetes_ids") or []):
                fora_do_contexto += 1
                continue
            x = citacoes.setdefault(i, {"casos": 0, "certos": 0, "por_classe": [0] * len(CLASSES)})
            x["casos"] += 1
            x["certos"] += ok
            x["por_classe"][CLASSES.index(r["classe"])] += 1
        if previsao is not None:
            prevista = previsao.get(r["caso"])
            lado = cruz["aponta" if prevista == r["classe"] else "nao_aponta"]
            lado["n"] += 1
            lado["acertos"] += ok
            da_resposta = (classes_da_causa or {}).get(lido["causa_raiz"] or "", set())
            lado = coerencia["sem_previsao" if prevista is None else ("coerente" if prevista in da_resposta else "incoerente")]
            lado["n"] += 1
            lado["acertos"] += ok
    for lado in list(cruz.values()) + list(coerencia.values()):
        lado["acerto_pct"] = round(100 * lado["acertos"] / lado["n"], 1) if lado["n"] else None
    return {"id": f["id"], "corrida": f["corrida"], "conjunto": f["conjunto"], "modelo": f["modelo"], "slug": f["slug"], "versao": f["versao"],
            "biblioteca": f["biblioteca"], "dono_da_biblioteca": f["dono_da_biblioteca"], "casos": len(regs), "acertos": acertos,
            "acerto_pct": round(100 * acertos / len(regs), 1),
            "causas": {k: causas[k] for k in sorted(causas)},
            "confusoes": [[g, resp, n] for (g, resp), n in sorted(confusoes.items(), key=lambda kv: (-kv[1], kv[0][0], str(kv[0][1])))],
            "citacoes": {k: citacoes[k] for k in sorted(citacoes)}, "citados_fora_do_contexto": fora_do_contexto,
            "rota_e_acerto": cruz if previsao is not None else None,
            "resposta_e_rota": coerencia if previsao is not None and classes_da_causa is not None else None}


def montar(corridas: list[str] | None = None, base: str | None = None, gerado_em: str | None = None) -> dict:
    corridas = corridas or CORRIDAS
    base = base or BASE
    fatias = ler_fatias(corridas)
    if not fatias:
        raise SystemExit(f"nenhum diagnóstico gravado em {caminhos.RESULTADOS} para as corridas {corridas}")
    casos: dict[str, dict] = {}
    for f in fatias:
        for r in f["registros"]:
            casos.setdefault(r["caso"], {"classe": r["classe"], "nivel": r["nivel"], "gabarito": r["gabarito"]["causa_raiz"],
                                         "conjunto": "ineditos" if f["conjunto"] == "ineditos" else "oficiais", "rotas": {}})
    classe_do_caso = {c: d["classe"] for c, d in casos.items()}

    # o atlas de cada biblioteca sai das rotas da corrida base; a mesma biblioteca tem de dar a mesma rota ao mesmo caso
    bibliotecas: dict[str, dict] = {}
    divergencias = []
    for f in (x for x in fatias if x["corrida"] == base):
        rotas = {r["caso"]: list(r.get("verbetes_ids") or []) for r in f["registros"]}
        b = bibliotecas.get(f["biblioteca"])
        if b is None:
            verbetes = bib.carregar(f["snapshot"])
            bibliotecas[f["biblioteca"]] = {"rotas": rotas, "meta": {v["id"]: v for v in verbetes}, "fatias": [f["id"]], "versoes": {(f["modelo"], f["versao"])}}
        else:
            b["fatias"].append(f["id"])
            b["versoes"].add((f["modelo"], f["versao"]))
            for caso, rota in rotas.items():
                if b["rotas"].get(caso) != rota:
                    divergencias.append({"biblioteca": f["biblioteca"], "caso": caso, "fatia": f["id"]})
    original = next((f["biblioteca"] for f in fatias if f["corrida"] == base and f["versao"] == 0), None)
    sem_o_caso: dict[tuple[str, str], dict] = {}     # (biblioteca, caso) -> atlas montado sem esse caso

    def atlas_sem(h: str, caso: str) -> dict:
        if (h, caso) not in sem_o_caso:
            resto = {c: r for c, r in bibliotecas[h]["rotas"].items() if c != caso}
            sem_o_caso[(h, caso)] = atlas_de_recuperacao(resto, classe_do_caso, sorted(bibliotecas[h]["meta"]), CLASSES)
        return sem_o_caso[(h, caso)]

    saida_bibliotecas = {}
    for h in sorted(bibliotecas):
        b = bibliotecas[h]
        ids = sorted(b["meta"])
        at = atlas_de_recuperacao(b["rotas"], classe_do_caso, ids, CLASSES)
        prev = {caso: prever_classe(rota, atlas_sem(h, caso), CLASSES) for caso, rota in b["rotas"].items()}
        loo = _resumo_da_previsao([(caso, classe_do_caso[caso], p, bool(pontos)) for caso, (p, pontos) in prev.items()], CLASSES)
        donos = [] if h == original else sorted({m for m, v in b["versoes"] if v > 0})
        verbetes = {}
        for i in ids:
            m = b["meta"][i]
            verbetes[i] = {"titulo": m["meta"].get("titulo", i), "pasta": m["pasta"], "tipo": m["meta"].get("tipo"),
                           "causa_raiz": m["meta"].get("causa_raiz"), "notas_do_modelo": len(bib.notas(m)), **at[i]}
        saida_bibliotecas[h] = {
            "original": h == original, "escrita_por": donos, "versoes": sorted([m, v] for m, v in b["versoes"]),
            "casos": len(b["rotas"]), "total_por_classe": [sum(1 for c in b["rotas"] if classe_do_caso[c] == k) for k in CLASSES],
            "verbetes": verbetes, "contagem_por_rotulo": dict(sorted(Counter(v["rotulo"] for v in verbetes.values()).items())),
            "posicoes": posicoes(at, CLASSES),
            "validacao": {"deixando_um_de_fora": loo, "ineditos": None}}

    causa_classe: dict[str, set] = {}
    for d in casos.values():
        causa_classe.setdefault(d["gabarito"], set()).add(d["classe"])
    saida_fatias = []
    for f in fatias:
        b = saida_bibliotecas.get(f["biblioteca"])
        previsao = None
        if b is not None:
            # a classe que a rota do caso aponta: se o caso entrou na conta do atlas, vale o atlas montado sem ele
            previsao = {}
            for r in f["registros"]:
                rota = list(r.get("verbetes_ids") or [])
                na_base = r["caso"] in bibliotecas[f["biblioteca"]]["rotas"]
                previsao[r["caso"]] = prever_classe(rota, atlas_sem(f["biblioteca"], r["caso"]) if na_base else b["verbetes"], CLASSES)[0]
            if f["conjunto"] == "ineditos" and b["validacao"]["ineditos"] is None:
                rotas = {r["caso"]: list(r.get("verbetes_ids") or []) for r in f["registros"]}
                b["validacao"]["ineditos"] = fora_da_amostra(b["verbetes"], CLASSES, rotas, classe_do_caso)
        resumo = _resumo_da_fatia(f, previsao, causa_classe)
        saida_fatias.append(resumo)
        for r in f["registros"]:
            lido = avaliar.extrair(r.get("resposta", ""))
            casos[r["caso"]]["rotas"][f["id"]] = {
                "recuperados": list(r.get("verbetes_ids") or []), "citados": list(dict.fromkeys(lido["fonte_ids"])), "rotulo": lido["causa_raiz"],
                "acerto": bool(avaliar.avaliar_registro(r, set())["causa_correta"]),
                "classe_da_rota": None if previsao is None else previsao.get(r["caso"])}

    decidida = next((f["id"] for f in saida_fatias if f["corrida"] == base and f["modelo"] == MODELO_DECIDIDO and f["versao"] == VERSAO_DECIDIDA),
                    saida_fatias[0]["id"])
    return {
        "metadados": {
            "script": "gerar_atlas.py", "gerado_em": gerado_em or datetime.now().isoformat(timespec="seconds"),
            "corridas": corridas, "base": base, "fatia_decidida": decidida, "biblioteca_original": original,
            "metodo": {"origem": "expert_atlas do repositório colibri (c/tools/expert_atlas), aplicado à busca de verbetes",
                       "item": "caso de teste", "entidade": "verbete da biblioteca", "escolha": "os k verbetes que a busca põe no contexto do caso",
                       "limiar_especialista": LIMIAR_ESPECIALISTA, "minimo_de_casos": MINIMO_DE_CASOS,
                       "entropia_maxima_bits": round(math.log2(len(CLASSES)), 3)},
            "ressalvas": ["Parte da afinidade vem do desenho da biblioteca: há um verbete de erro por causa, e a busca soma reforços por endpoint, "
                          "entidade e status calculados em código.",
                          "A posição no desenho é a média das âncoras das classes ponderada pela afinidade medida; não é semelhança de significado.",
                          "Os modelos do projeto são densos: o atlas descreve a busca e o uso que cada modelo fez do contexto, não o interior do modelo."],
            "divergencias_de_rota": divergencias},
        "classes": [{"n": c, "id": taxonomia.CLASSES[c]["id"], "nome": NOME_DA_CLASSE.get(c, taxonomia.CLASSES[c]["id"]),
                     "pergunta": taxonomia.CLASSES[c]["pergunta"], "ancora": ancoras(CLASSES)[c]} for c in CLASSES],
        "causas": [{"id": k, "classes": sorted(v), "casos": sum(1 for d in casos.values() if d["gabarito"] == k)} for k, v in sorted(causa_classe.items())],
        "bibliotecas": saida_bibliotecas,
        "fatias": saida_fatias,
        "casos": {c: casos[c] for c in sorted(casos)},
    }


# ------------------------------------------------------------------ Markdown derivado

def _f(v, casas: int = 1) -> str:
    return "n/d" if v is None else f"{v:.{casas}f}".replace(".", ",")


def _nome_da_biblioteca(h: str, b: dict) -> str:
    if b["original"]:
        return f"original, L0 (`{h}`)"
    return "; ".join(f"L{v} do `{m}`" for m, v in b["versoes"]) + f" (`{h}`)"


def render(dado: dict) -> str:
    meta = dado["metadados"]
    bibs = dado["bibliotecas"]
    md = pf.cabecalho("Atlas da busca e do uso dos verbetes", "gerar_atlas.py",
                      "os registros de diagnóstico das corridas " + ", ".join(f"`{c}`" for c in meta["corridas"]), meta["gerado_em"][:10])
    md += ["", f"Método do `expert_atlas` do repositório colibri aplicado ao que o projeto mede: o item é o {meta['metodo']['item']}, a entidade é o "
           f"{meta['metodo']['entidade']}, e a escolha é a da busca ({meta['metodo']['escolha']}). Especialista: especialização a partir de "
           f"{_f(meta['metodo']['limiar_especialista'])} em pelo menos {meta['metodo']['minimo_de_casos']} casos distintos. Entropia máxima: "
           f"{_f(meta['metodo']['entropia_maxima_bits'], 3)} bits (seis classes).", ""]
    md += ["Ressalvas:", ""] + [f"- {r}" for r in meta["ressalvas"]] + [""]

    md += ["<!-- tabela:tb_atlas_bibliotecas -->",
           "| Biblioteca | Verbetes | Recuperados em algum caso | Especialistas | Generalistas | Sem repetição | Nunca recuperados |",
           "|---|---|---|---|---|---|---|"]
    for h, b in bibs.items():
        c = b["contagem_por_rotulo"]
        md.append(f"| {_nome_da_biblioteca(h, b)} | {len(b['verbetes'])} | {sum(1 for v in b['verbetes'].values() if v['itens'])} | {c.get('especialista', 0)} | "
                  f"{c.get('generalista', 0)} | {c.get('sem_repeticao', 0)} | {c.get('nunca_recuperado', 0)} |")
    md += ["<!-- /tabela:tb_atlas_bibliotecas -->", ""]

    decidida = next(f for f in dado["fatias"] if f["id"] == meta["fatia_decidida"])
    b = bibs[decidida["biblioteca"]]
    md += [f"Verbetes da biblioteca da fatia decidida ({_nome_da_biblioteca(decidida['biblioteca'], b)}), do mais recuperado para o menos:", "",
           "<!-- tabela:tb_atlas_verbetes -->",
           "| Verbete | Pasta | Casos em que entrou no contexto | Vezes em primeiro | Classe dominante | Especialização | Entropia (bits) | Rótulo | Notas do modelo |",
           "|---|---|---|---|---|---|---|---|---|"]
    for i, v in sorted(b["verbetes"].items(), key=lambda kv: (-kv[1]["itens"], kv[0])):
        dom = "nenhuma" if v["dominante"] is None else NOME_DA_CLASSE.get(v["dominante"], str(v["dominante"]))
        md.append(f"| `{i}` | {v['pasta']} | {v['itens']} | {v['vezes_em_primeiro']} | {dom} | {_f(v['especializacao'], 2)} | {_f(v['entropia_bits'], 2)} | "
                  f"{NOME_DO_ROTULO[v['rotulo']]} | {v['notas_do_modelo']} |")
    md += ["<!-- /tabela:tb_atlas_verbetes -->", ""]

    md += ["Validação: o atlas de cada biblioteca prevê a classe de um caso pelos verbetes da rota dele. Na primeira coluna de acerto o caso previsto "
           "ficou de fora da montagem do atlas; na segunda, o atlas dos casos oficiais prevê os casos inéditos.", "",
           "<!-- tabela:tb_atlas_validacao -->",
           "| Biblioteca | Casos | Acertos deixando um de fora | Acerto | Empates | Sem evidência | Inéditos previstos | Acerto nos inéditos | Acaso |",
           "|---|---|---|---|---|---|---|---|---|"]
    for h, b in bibs.items():
        loo, ined = b["validacao"]["deixando_um_de_fora"], b["validacao"]["ineditos"]
        md.append(f"| {_nome_da_biblioteca(h, b)} | {loo['total']} | {loo['acertos']} | {_f(loo['acerto_pct'])}% | {loo['empates']} | {loo['sem_evidencia']} | "
                  + (f"{ined['acertos']} de {ined['total']} | {_f(ined['acerto_pct'])}% | " if ined else "n/d | n/d | ") + f"{_f(loo['acaso_pct'])}% |")
    md += ["<!-- /tabela:tb_atlas_validacao -->", ""]

    md += ["Por fatia (corrida, modelo e versão da biblioteca): o acerto do modelo, as citações e dois cruzamentos. O primeiro usa o gabarito: a rota aponta a "
           "classe verdadeira do caso? O segundo não usa: a causa que o modelo respondeu é de uma classe que a rota aponta? (Nos casos em que a rota "
           "empata ou não tem evidência o segundo cruzamento não se aplica.)", "",
           "<!-- tabela:tb_atlas_fatias -->",
           "| Fatia | Casos | Acerto do modelo | Verbetes citados (distintos) | Citações fora do contexto | Rota aponta a classe: acerto | Rota não aponta: acerto | "
           "Resposta na classe da rota: acerto | Resposta fora da classe da rota: acerto |",
           "|---|---|---|---|---|---|---|---|---|"]
    for f in dado["fatias"]:
        ra = f["rota_e_acerto"]
        aponta = f"{_f(ra['aponta']['acerto_pct'])}% ({ra['aponta']['acertos']} de {ra['aponta']['n']})" if ra and ra["aponta"]["n"] else "n/d"
        nao = f"{_f(ra['nao_aponta']['acerto_pct'])}% ({ra['nao_aponta']['acertos']} de {ra['nao_aponta']['n']})" if ra and ra["nao_aponta"]["n"] else "n/d"
        rr = f["resposta_e_rota"]
        coer = f"{_f(rr['coerente']['acerto_pct'])}% ({rr['coerente']['acertos']} de {rr['coerente']['n']})" if rr and rr["coerente"]["n"] else "n/d"
        inco = f"{_f(rr['incoerente']['acerto_pct'])}% ({rr['incoerente']['acertos']} de {rr['incoerente']['n']})" if rr and rr["incoerente"]["n"] else "n/d"
        md.append(f"| `{f['id']}` | {f['casos']} | {_f(f['acerto_pct'])}% ({f['acertos']}) | {len(f['citacoes'])} | {f['citados_fora_do_contexto']} | {aponta} | {nao} | {coer} | {inco} |")
    md += ["<!-- /tabela:tb_atlas_fatias -->", ""]
    return "\n".join(md)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--colar", action="store_true")
    args = ap.parse_args()
    print(caminhos.descricao())
    dado = montar()
    if dado["metadados"]["divergencias_de_rota"]:
        print(f"AVISO: {len(dado['metadados']['divergencias_de_rota'])} rota(s) diferentes para a mesma biblioteca e o mesmo caso")
    return pf.fechar(NOME, dado, render(dado), PREFIXO, check=args.check, colar=args.colar)


if __name__ == "__main__":
    sys.exit(main())
