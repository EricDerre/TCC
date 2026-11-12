#!/usr/bin/env python3
# ! Alteração de IA - Revisar: arquivo novo (10/11/2026, ficha 63 opção b, decisão 116) com a corrida 25, um experimento em texto que não muda o agente: a
# biblioteca de produção sem a seção "Notas do modelo" de cada verbete e sem a pasta `aprendidos/` lê os 36 casos oficiais de avaliação e os 36 inéditos da
# ficha 27 pelo diagnóstico do agente, e cada caso é pareado com o diagnóstico que a biblioteca de produção inteira deu a ele (corrida 22 nos oficiais, corrida 24
# nos inéditos). Traz a cópia da biblioteca (`montar_biblioteca`), a prévia sem modelo dos 72 contextos (`previa`), a corrida (`rodar`, modo `sem_notas` de
# executar_fase4.py), a leitura (`resumir` e `render`, por avaliar_fase4.py --sem_notas) e a conferência da ponte de versão para o lançador
# (`rodar_experimento_sem_notas.ps1`).
# ! Motivo: o parecer do analista de 10/11/2026 observou que as notas que o modelo escreveu na biblioteca estão em forma de instrução ("Adicionar", "Corrigir"), e
# não havia número para dizer quanto elas pesam no diagnóstico; o Eric escolheu medir antes da Fase 5, sem tocar no agente. Por isso o código é novo: o prompt
# (`estrategias.py`), a busca (`recuperacao.py`), a biblioteca de produção e o diagnóstico (`diagnostico_ao_vivo.py`) entram só para leitura, e a cópia sem notas
# vive na pasta da corrida. A ficha citava a corrida 16 para os oficiais; ela leu a biblioteca de antes do lote de 04/11/2026 (hash `1fca10f1a6f6`), em outra
# versão do Ollama, e a corrida 22 leu os mesmos 36 casos com a biblioteca de hoje: a regra usa a 22 e a 24, e a 16 entra como segunda comparação. A regra do
# veredito fica escrita aqui e testada antes de a corrida rodar, para o resultado não escolher a régua.
"""Corrida 25: a biblioteca de produção sem as notas do modelo e sem os verbetes aprendidos, em texto, contra as corridas 22 e 24. Sem navegador.

Uso (em Programacao/AgenteCore/experimentos, com RESULTADOS_DIR=resultados_alvo):
  python experimento_sem_notas.py --previa [--check]   a prévia sem modelo: quantos dos 72 contextos mudam, e como (resultados_alvo/fase4/sem_notas_previa.{json,md})
  python experimento_sem_notas.py --ponte              diz ao lançador a versão do Ollama no ar e se falta a ponte dela (regra R6)
A corrida roda por rodar_fase4.ps1 -Modo sem_notas -Saida fase4_sem_notas (o lançador rodar_experimento_sem_notas.ps1 faz a ponte antes, quando falta) e a
leitura por avaliar_fase4.py --sem_notas --saida fase4_sem_notas.
"""
from __future__ import annotations

import argparse
import collections
import json
import platform
import re
import sys
import tempfile
import time
from pathlib import Path

import analisar_fase3b as a3b
import avaliar
import avaliar_fase3
import biblioteca as bib
import caminhos
import corridas_em_texto as ct
import diagnostico_ao_vivo as dv
import estrategias
import evolucao_biblioteca as evo
import executar_bateria
import executar_fase3
import executar_fase3b as e3b
import pre_fase4 as pf
import recuperacao as rec
import trilha as tr

CORRIDA = 25
NOME, PREFIXO = "sem_notas", "tb_f4_semnotas_"
NOME_PREVIA = "sem_notas_previa"
ALFA = 0.05                                   # o corte do teste pareado, fixado antes da corrida (decisão 116)
SECAO_DAS_NOTAS = "Notas do modelo"
PASTA_DA_COPIA = "sem-notas"
ARQ_DERIVACAO = "derivacao.json"
BANCOS = ("avaliacao", "ineditos")
NOME_DO_BANCO = {"avaliacao": "os 36 oficiais de avaliação", "ineditos": "os 36 inéditos da ficha 27"}
# A referência de cada banco: a corrida que leu os mesmos casos, em texto e pelo mesmo diagnóstico, com a biblioteca de produção de hoje.
REFERENCIAS = {"avaliacao": {"corrida": "22", "saida": "fase4_trilha", "registros": "diagnosticos__base.jsonl", "linhas": "avaliacao.jsonl"},
               "ineditos": {"corrida": "24", "saida": "fase4_ineditos", "registros": "diagnosticos__ineditos.jsonl", "linhas": "ineditos.jsonl"}}
# A corrida que a ficha 63 citava para os oficiais: a calibração com k = 3, com a biblioteca de antes do lote de 04/11/2026.
CORRIDA_16 = {"corrida": "16", "saida": "fase4_calibracao", "subpasta": "k3", "registros": f"diagnosticos__L{dv.VERSAO_CURADA}.jsonl"}
MUDANCAS = ("contexto idêntico", "mesmos verbetes, sem as notas", "mesmos verbetes, outra ordem", "verbetes diferentes")
# O começo de uma nota escrita como instrução ao leitor ("Adicionar nota sobre...", "Corrigir..."), a observação do parecer do analista.
VERBOS_DE_INSTRUCAO = ("Adicionar", "Adicione", "Corrig", "Notar", "Inclu")
_RE_SECAO = re.compile(r"^##\s+(.+?)\s*$")


# ------------------------------------------------------------------ a cópia da biblioteca

def texto_sem_notas(texto: str) -> tuple[str, int]:
    """O texto de um verbete sem a seção "Notas do modelo" (do título dela até a seção seguinte ou o fim do arquivo) e quantas notas saíram. O que vem antes e
    depois fica como estava, com a quebra de linha do arquivo, e o arquivo termina numa quebra só; sem a seção, o texto volta como entrou."""
    saida, tinha, dentro, notas = [], False, False, 0
    for linha in texto.splitlines(keepends=True):
        titulo = _RE_SECAO.match(linha.rstrip("\r\n"))
        if titulo:
            dentro = titulo.group(1) == SECAO_DAS_NOTAS
            tinha = tinha or dentro
        if dentro:
            notas += linha.startswith("- [")
            continue
        saida.append(linha)
    if not tinha:
        return texto, 0
    return "".join(saida).rstrip("\r\n") + ("\r\n" if "\r\n" in texto else "\n"), notas


def _derivar(origem: Path, destino: Path) -> dict:
    """Grava em `destino` os verbetes de `origem` sem a seção das notas e sem a pasta dos aprendidos; devolve o que saiu e os dois hashes."""
    retirados, com_notas, notas, copiados = [], 0, 0, 0
    for rel, arq in sorted(evo._arquivos_md(origem).items()):
        cru = arq.read_bytes()
        original = cru.decode("utf-8")
        if Path(rel).parts[0] == evo.PASTA_APRENDIDOS:
            try:
                retirados.append(bib._parse_frontmatter(original)[0].get("id", arq.stem))
            except ValueError:
                retirados.append(arq.stem)
            continue
        texto, n = texto_sem_notas(original)
        alvo = destino / rel
        alvo.parent.mkdir(parents=True, exist_ok=True)
        alvo.write_bytes(cru if texto == original else texto.encode("utf-8"))
        copiados += 1
        com_notas += texto != original
        notas += n
    return {"origem_hash": evo.hash_biblioteca(origem), "hash": evo.hash_biblioteca(destino), "verbetes": copiados, "verbetes_retirados": sorted(retirados),
            "verbetes_com_notas": com_notas, "notas_retiradas": notas}


def montar_biblioteca(origem: Path, destino: Path) -> dict:
    """A cópia sem notas de `origem` em `destino`, com `derivacao.json` dizendo o que saiu. A origem só é lida. Quando `destino` já existe (relance da corrida),
    nada é regravado: a cópia é conferida contra uma derivação nova, e uma cópia diferente levanta SystemExit."""
    if destino.exists():
        with tempfile.TemporaryDirectory() as tmp:
            esperado = _derivar(origem, Path(tmp) / PASTA_DA_COPIA)
        arq = destino / ARQ_DERIVACAO
        gravado = json.loads(arq.read_text(encoding="utf-8")) if arq.exists() else None
        if gravado != esperado or evo.hash_biblioteca(destino) != esperado["hash"]:
            raise SystemExit(f"{destino} existe mas não é a cópia sem notas de {origem} (esperado o hash {esperado['hash']}): apague a pasta e relance")
        return esperado
    derivacao = _derivar(origem, destino)
    (destino / ARQ_DERIVACAO).write_text(json.dumps(derivacao, ensure_ascii=False, indent=2), encoding="utf-8")
    return derivacao


# ------------------------------------------------------------------ os casos e as referências

def casos_por_banco() -> dict[str, list[dict]]:
    """Os dois bancos do experimento: os 36 casos oficiais de avaliação (a partição gravada pela Fase 3) e os 36 inéditos da ficha 27."""
    import banco_casos_ineditos_fase4 as bi4
    return {"avaliacao": e3b._casos_avaliacao(e3b._particao_oficial(e3b._oficial())), "ineditos": list(bi4.CASOS_INEDITOS_FASE4)}


def casos_do_experimento(limite: int = 0) -> list[tuple[str, dict]]:
    """(banco, caso) na ordem da corrida: os oficiais e depois os inéditos; com `limite`, os N primeiros de cada banco (fumaça)."""
    return [(banco, c) for banco, casos in casos_por_banco().items() for c in (casos[:limite] if limite else casos)]


def referencias(modelo: str = dv.MODELO_PADRAO) -> dict:
    """Os registros das corridas de referência, por banco: o diagnóstico de cada caso e a linha com a probabilidade e o selo."""
    slug = executar_fase3._slug(modelo)
    saida = {}
    for banco, r in REFERENCIAS.items():
        raiz = caminhos.fase3(r["saida"])["raiz"]
        saida[banco] = {"corrida": r["corrida"], "registros": executar_bateria.ler_jsonl(raiz / slug / r["registros"]), "linhas": executar_bateria.ler_jsonl(raiz / r["linhas"])}
    return saida


def mudanca_do_contexto(novo: dict, ref: dict) -> str:
    """O que mudou no contexto entregue ao modelo entre a referência e a cópia sem notas, lido dos dois registros."""
    if novo.get("contexto_sha256") == ref.get("contexto_sha256"):
        return MUDANCAS[0]
    ids_novos, ids_ref = list(novo.get("verbetes_ids") or []), list(ref.get("verbetes_ids") or [])
    if ids_novos == ids_ref:
        return MUDANCAS[1]
    return MUDANCAS[2] if sorted(ids_novos) == sorted(ids_ref) else MUDANCAS[3]


# ------------------------------------------------------------------ a ponte de versão (regra R6)

def nome_da_ponte(versao: str) -> str:
    """A pasta da ponte de uma versão do Ollama, no nome das pontes já rodadas: 0.40.14 virou fase3b_ponte_04014."""
    return "fase3b_ponte_" + versao.replace(".", "")


def segue_depois_da_ponte(ponte: dict | None, parcial: bool) -> tuple[bool, str]:
    """Se a corrida pode seguir numa versão do Ollama diferente da das referências: só com ponte completa e pareável com a Fase 3 (b + c até o limite, decisão
    47). A fumaça de poucos casos segue de qualquer jeito, como nos outros modos. Devolve também o motivo, para o log."""
    if parcial:
        return True, "corrida parcial: segue sem conferir a ponte"
    if not ponte:
        return False, "a versão do Ollama no ar não tem ponte completa registrada (regra R6): rode a ponte antes; rodar_experimento_sem_notas.ps1 faz isso"
    discordantes = (ponte.get("b") or 0) + (ponte.get("c") or 0)
    if not ponte.get("pareavel"):
        return False, (f"a ponte da versão {ponte.get('versao')} não é pareável com a Fase 3 (b + c = {discordantes}, limite {ponte.get('limite')}): a comparação com as corridas "
                       "22 e 24, que rodaram em outra versão, não vale, e a corrida para aqui")
    return True, f"a ponte da versão {ponte.get('versao')} é pareável com a Fase 3 (b + c = {discordantes}, limite {ponte.get('limite')})"


def situacao_da_ponte() -> dict:
    """A versão do Ollama no ar, a ponte registrada para ela e o nome da pasta da ponte que falta (None quando não falta)."""
    import executar_fase4 as ex
    versao = executar_fase3._versao_ollama()
    ponte = ex.ultima_ponte(ex.carregar_pontes(gravar=False), versao) if versao else None
    completa = bool(ponte and ponte.get("completa", True))
    return {"versao": versao, "ponte": ponte if completa else None, "falta": nome_da_ponte(versao) if versao and not completa else None}


# ------------------------------------------------------------------ a regra e a leitura

def texto_da_regra() -> str:
    corte = f"{ALFA:.2f}".replace(".", ",")
    return ("Regra fixada antes da corrida (decisão 116): a diferença sai do ruído quando o teste pareado exato dos casos dos dois bancos juntos (McNemar, bilateral) "
            f"dá p abaixo de {corte}, com a corrida completa e a ponte da versão do Ollama pareável com a Fase 3 (b + c até 2, decisão 47). Fora disso a diferença fica "
            "dentro do ruído e o agente não muda; se sair do ruído, mudar o agente é outra decisão.")


def _pares(itens: list[dict]) -> dict:
    """A conta dos pares de um grupo de casos: acertos nos dois lados, b (passou a acertar sem as notas), c (passou a errar) e o p do teste pareado exato."""
    n = len(itens)
    acertos, acertos_ref = sum(1 for i in itens if i["acerto"]), sum(1 for i in itens if i["acerto_referencia"])
    ganhos, perdas = sorted(i["caso"] for i in itens if i["mudou"] == "ganho"), sorted(i["caso"] for i in itens if i["mudou"] == "perda")
    lo, hi = avaliar.wilson(acertos, n) if n else (None, None)
    return {"casos": n, "acertos_sem_notas": acertos, "acerto_sem_notas_pct": ct._pct(acertos, n), "wilson_lo_pct": lo, "wilson_hi_pct": hi, "acertos_referencia": acertos_ref,
            "acerto_referencia_pct": ct._pct(acertos_ref, n), "b": len(ganhos), "c": len(perdas), "saldo": len(ganhos) - len(perdas), "p": avaliar.mcnemar_exato(len(ganhos), len(perdas)),
            "mesmo_rotulo": sum(1 for i in itens if i["rotulo"] == i["rotulo_referencia"]), "ganhos": ganhos, "perdas": perdas}


def _veredito(pares: dict, completo: bool, pareavel: bool | None) -> tuple[bool | None, str]:
    if not completo:
        return None, "sem veredito: a corrida não cobriu todos os casos previstos"
    if pareavel is None:
        return None, "sem veredito: a versão do Ollama desta corrida não tem ponte registrada, e as referências rodaram em outra versão"
    if not pareavel:
        return None, "sem veredito: a ponte da versão do Ollama desta corrida não é pareável com a Fase 3, e a comparação com as referências não vale"
    if pares["p"] < ALFA:
        return True, "sai do ruído, a favor de tirar as notas" if pares["b"] > pares["c"] else "sai do ruído, a favor das notas"
    return False, "dentro do ruído"


def resumir(registros: list[dict], linhas: list[dict], casos: dict[str, list[dict]], refs: dict, condicoes: dict | None, ponte: dict | None = None,
            corrida16: dict | None = None, corrida: str | None = None, gerado_em: str | None = None) -> dict:
    """A cópia sem notas contra a referência de cada caso: os pares, o teste pareado, a regra do ruído, por banco, pelo que mudou no contexto, por classe e, só nos
    oficiais, contra a corrida 16. O gabarito entra só aqui, pelo id do caso."""
    condicoes = condicoes or {}
    por_id = {c["id"]: (banco, c) for banco, lista in casos.items() for c in lista}
    reg_ref = {banco: {r["caso"]: r for r in x.get("registros") or []} for banco, x in refs.items()}
    lin_ref = {banco: {l["caso"]: l for l in x.get("linhas") or []} for banco, x in refs.items()}
    extras = {l["caso"]: l for l in linhas}
    itens = []
    for r in registros:
        if r["caso"] not in por_id:
            continue
        banco, c = por_id[r["caso"]]
        ref = reg_ref.get(banco, {}).get(r["caso"])
        if ref is None:
            continue
        g = c["gabarito"]["causa_raiz"]
        rotulo, rotulo_ref = ct.rotulo_lido(r.get("resposta")), ct.rotulo_lido(ref.get("resposta"))
        acerto, acerto_ref = rotulo == g, rotulo_ref == g
        x, x_ref = extras.get(r["caso"], {}), lin_ref.get(banco, {}).get(r["caso"], {})
        ids, ids_ref = list(r.get("verbetes_ids") or []), list(ref.get("verbetes_ids") or [])
        itens.append({"caso": r["caso"], "banco": banco, "classe": c.get("classe"), "nivel": c.get("nivel"), "gabarito": g, "rotulo": rotulo, "acerto": acerto,
                      "rotulo_referencia": rotulo_ref, "acerto_referencia": acerto_ref, "mudou": "ganho" if acerto and not acerto_ref else ("perda" if acerto_ref and not acerto else ""),
                      "mudanca_do_contexto": mudanca_do_contexto(r, ref), "verbetes_ids": ids, "verbetes_ids_referencia": ids_ref, "notas_no_contexto_referencia": ref.get("notas_no_contexto"),
                      "verbete_certo_no_contexto": g in ids, "verbete_certo_no_contexto_referencia": g in ids_ref, "p_rotulo": x.get("p_rotulo"), "p_rotulo_referencia": x_ref.get("p_rotulo"),
                      "selo": x.get("selo"), "selo_referencia": x_ref.get("selo"), "tokens_entrada": r.get("tokens_entrada"), "tokens_entrada_referencia": ref.get("tokens_entrada"),
                      "segundos": r.get("segundos"), "segundos_referencia": ref.get("segundos")})
    completo = len(itens) == sum(len(v) for v in casos.values()) and not condicoes.get("parcial")
    versao = condicoes.get("versao_ollama")
    versoes_ref = {r.get("versao_ollama") for x in refs.values() for r in x.get("registros") or []}
    mesma_versao = versao is not None and versoes_ref == {versao}
    pareavel = True if mesma_versao else (bool(ponte.get("pareavel")) if ponte else None)

    def medianas(sub: list[dict]) -> dict:
        return {"tokens_entrada_mediana": ct._mediana([i["tokens_entrada"] for i in sub]), "tokens_entrada_mediana_referencia": ct._mediana([i["tokens_entrada_referencia"] for i in sub]),
                "segundos_mediana": ct._mediana([i["segundos"] for i in sub]), "segundos_mediana_referencia": ct._mediana([i["segundos_referencia"] for i in sub])}

    def balanceada(sub: list[dict], chave: str) -> float | None:
        return avaliar_fase3.acuracia_balanceada([(i["gabarito"], i[chave] or "") for i in sub]) if sub else None

    def unicos(valores) -> str:
        return ", ".join(sorted({str(v) for v in valores if v})) or "n/d"

    total = _pares(itens)
    sai, veredito = _veredito(total, completo, pareavel)
    por_banco = []
    for banco in BANCOS:
        sub = [i for i in itens if i["banco"] == banco]
        if banco not in refs:
            continue
        regs = refs[banco].get("registros") or []
        por_banco.append({"banco": banco, "referencia": f"corrida {refs[banco]['corrida']}", **_pares(sub), **medianas(sub),
                          "acuracia_balanceada_sem_notas_pct": balanceada(sub, "rotulo"), "acuracia_balanceada_referencia_pct": balanceada(sub, "rotulo_referencia"),
                          "selos": dict(sorted(collections.Counter(str(i["selo"]) for i in sub).items())), "selos_referencia": dict(sorted(collections.Counter(str(i["selo_referencia"]) for i in sub).items())),
                          "verbete_certo_no_contexto": sum(1 for i in sub if i["verbete_certo_no_contexto"]),
                          "verbete_certo_no_contexto_referencia": sum(1 for i in sub if i["verbete_certo_no_contexto_referencia"]),
                          "versao_ollama_referencia": unicos(r.get("versao_ollama") for r in regs), "biblioteca_referencia": unicos(r.get("biblioteca_versao") for r in regs)})
    por_mudanca = []
    for mudanca in MUDANCAS:
        p = _pares([i for i in itens if i["mudanca_do_contexto"] == mudanca])
        por_mudanca.append({"mudanca": mudanca, **{k: p[k] for k in ("casos", "acertos_sem_notas", "acertos_referencia", "b", "c", "mesmo_rotulo")}})
    contra_16 = None
    if corrida16 and corrida16.get("registros"):
        r16 = {r["caso"]: r for r in corrida16["registros"]}
        sub = []
        for i in itens:
            if i["banco"] != "avaliacao" or i["caso"] not in r16:
                continue
            rotulo_16 = ct.rotulo_lido(r16[i["caso"]].get("resposta"))
            acerto_16 = rotulo_16 == i["gabarito"]
            sub.append({**i, "rotulo_referencia": rotulo_16, "acerto_referencia": acerto_16,
                        "mudou": "ganho" if i["acerto"] and not acerto_16 else ("perda" if acerto_16 and not i["acerto"] else "")})
        usados = [r16[i["caso"]] for i in sub]
        contra_16 = {"corrida": corrida16.get("corrida"), **_pares(sub), "biblioteca": unicos(r.get("biblioteca_versao") for r in usados), "versao_ollama": unicos(r.get("versao_ollama") for r in usados)}
    por_classe = [{"classe": classe, "casos": len(sub), "acertos_sem_notas": sum(1 for i in sub if i["acerto"]), "acertos_referencia": sum(1 for i in sub if i["acerto_referencia"])}
                  for classe in sorted({str(i["classe"]) for i in itens}) for sub in [[i for i in itens if str(i["classe"]) == classe]]]
    return {"metadados": {"gerado_em": gerado_em or time.strftime("%Y-%m-%dT%H:%M:%S"), "corrida": corrida, "numero": CORRIDA}, "condicoes": condicoes,
            "regra": {"alfa": ALFA, "texto": texto_da_regra(), "pareavel": pareavel, "mesma_versao_das_referencias": mesma_versao, "ponte": ponte},
            "resumo": {**total, **medianas(itens), "acuracia_balanceada_sem_notas_pct": balanceada(itens, "rotulo"), "acuracia_balanceada_referencia_pct": balanceada(itens, "rotulo_referencia"),
                       "completo": completo, "sai_do_ruido": sai, "veredito": veredito},
            "por_banco": por_banco, "por_mudanca_do_contexto": por_mudanca, "contra_a_corrida_16": contra_16, "por_classe": por_classe, "casos": itens}


def _lista(ids: list[str]) -> str:
    return ", ".join(f"`{i}`" for i in ids) or "nenhum"


def render(dado: dict) -> str:
    r, regra, c16 = dado["resumo"], dado["regra"], dado.get("contra_a_corrida_16")
    b_ = (dado.get("condicoes") or {}).get("biblioteca") or {}
    n, p = ct._n, ct._p
    lote = str(b_.get("lote_promovido_em") or "")[:10]
    lote = "/".join(reversed(lote.split("-"))) if lote else ""
    ponte = regra.get("ponte")
    if regra.get("mesma_versao_das_referencias"):
        sobre_a_ponte = "A corrida rodou na mesma versão do Ollama das referências, e a ponte não entra."
    elif ponte:
        sobre_a_ponte = (f"A corrida rodou em outra versão do Ollama que as referências; a ponte dessa versão (`{ponte.get('corrida')}`) deu b = {n(ponte.get('b'))} e c = {n(ponte.get('c'))} "
                         f"em {n(ponte.get('n'))} casos, {'pareável' if ponte.get('pareavel') else 'não pareável'} com a Fase 3 (limite {n(ponte.get('limite'))}).")
    else:
        sobre_a_ponte = "A corrida rodou em outra versão do Ollama que as referências, e essa versão não tem ponte registrada."
    texto = [(f"A biblioteca de produção (`{b_.get('origem_hash')}`) sem as {n(b_.get('notas_retiradas'))} notas do modelo, que estavam em {n(b_.get('verbetes_com_notas'))} verbetes, e sem os "
              f"{len(b_.get('verbetes_retirados') or [])} verbetes aprendidos (cópia `{b_.get('hash')}`, com {n(b_.get('verbetes'))} verbetes) lê em texto os casos oficiais de avaliação e os "
              "inéditos da ficha 27, com o mesmo prompt, o mesmo modelo e o mesmo k das corridas de referência. Cada caso é pareado com o diagnóstico que a biblioteca de produção inteira "
              f"deu a ele: a corrida 22 nos oficiais e a corrida 24 nos inéditos. A ficha 63 citava a corrida 16 para os oficiais; ela leu a biblioteca de antes do lote{' de ' + lote if lote else ''}, "
              f"em outra versão do Ollama, e por isso entra só como segunda comparação (corrida {CORRIDA}, decisão 116)."),
             "", regra["texto"], "", f"Veredito: {r['veredito']}. {sobre_a_ponte}"]
    blocos = [
        a3b.tab(f"{PREFIXO}resumo", ["Casos", "Acertos sem as notas", "Acerto sem as notas (%)", "Wilson 95%", "Acertos na referência", "Acerto na referência (%)", "Passaram a acertar (b)",
                                    "Passaram a errar (c)", "Saldo", "p do teste pareado", "Mesmo rótulo", "Tokens de entrada (mediana) sem as notas", "Tokens de entrada (mediana) na referência",
                                    "Segundos (mediana) sem as notas", "Segundos (mediana) na referência", "Veredito"],
                [[n(r["casos"]), n(r["acertos_sem_notas"]), n(r["acerto_sem_notas_pct"]), f"{n(r['wilson_lo_pct'])} a {n(r['wilson_hi_pct'])}", n(r["acertos_referencia"]), n(r["acerto_referencia_pct"]),
                  n(r["b"]), n(r["c"]), n(r["saldo"]), p(r["p"]), n(r["mesmo_rotulo"]), n(r["tokens_entrada_mediana"]), n(r["tokens_entrada_mediana_referencia"]), n(r["segundos_mediana"]),
                  n(r["segundos_mediana_referencia"]), r["veredito"]]]),
        a3b.tab(f"{PREFIXO}banco", ["Banco", "Referência", "Casos", "Acertos sem as notas", "Acertos na referência", "Passaram a acertar (b)", "Passaram a errar (c)", "p do teste pareado",
                                   "Mesmo rótulo", "Verbete certo entre os entregues, sem as notas", "Verbete certo entre os entregues, na referência", "Quais passaram a acertar", "Quais passaram a errar"],
                [[NOME_DO_BANCO.get(x["banco"], x["banco"]), x["referencia"], n(x["casos"]), n(x["acertos_sem_notas"]), n(x["acertos_referencia"]), n(x["b"]), n(x["c"]), p(x["p"]), n(x["mesmo_rotulo"]),
                  n(x["verbete_certo_no_contexto"]), n(x["verbete_certo_no_contexto_referencia"]), _lista(x["ganhos"]), _lista(x["perdas"])] for x in dado["por_banco"]] or [["sem casos"] + [""] * 12]),
        a3b.tab(f"{PREFIXO}mudanca", ["O que mudou no contexto entregue ao modelo", "Casos", "Acertos sem as notas", "Acertos na referência", "Passaram a acertar (b)", "Passaram a errar (c)", "Mesmo rótulo"],
                [[x["mudanca"], n(x["casos"]), n(x["acertos_sem_notas"]), n(x["acertos_referencia"]), n(x["b"]), n(x["c"]), n(x["mesmo_rotulo"])] for x in dado["por_mudanca_do_contexto"]]),
        a3b.tab(f"{PREFIXO}corrida16", ["Casos oficiais também lidos na corrida 16", "Acertos sem as notas", "Acertos na corrida 16", "Passaram a acertar (b)", "Passaram a errar (c)", "p do teste pareado",
                                       "Mesmo rótulo", "Biblioteca da corrida 16", "Ollama da corrida 16"],
                [[n(c16["casos"]), n(c16["acertos_sem_notas"]), n(c16["acertos_referencia"]), n(c16["b"]), n(c16["c"]), p(c16["p"]), n(c16["mesmo_rotulo"]), f"`{c16['biblioteca']}`", c16["versao_ollama"]]]
                if c16 else [["sem os registros da corrida 16"] + [""] * 8]),
        a3b.tab(f"{PREFIXO}classe", ["Classe", "Casos", "Acertos sem as notas", "Acertos na referência"],
                [[n(x["classe"]), n(x["casos"]), n(x["acertos_sem_notas"]), n(x["acertos_referencia"])] for x in dado["por_classe"]] or [["sem casos", "", "", ""]]),
        a3b.tab(f"{PREFIXO}casos", ["Caso", "Banco", "Classe", "Gabarito", "Rótulo sem as notas", "Certo", "Rótulo na referência", "Certo na referência", "Mudou", "O que mudou no contexto",
                                   "Verbetes entregues sem as notas", "Verbetes entregues na referência", "Notas no contexto da referência", "Probabilidade sem as notas", "Probabilidade na referência"],
                [[f"`{i['caso']}`", i["banco"], n(i["classe"]), f"`{i['gabarito']}`", f"`{i['rotulo']}`", "sim" if i["acerto"] else "não", f"`{i['rotulo_referencia']}`",
                  "sim" if i["acerto_referencia"] else "não", i["mudou"], i["mudanca_do_contexto"], _lista(i["verbetes_ids"]), _lista(i["verbetes_ids_referencia"]),
                  n(i["notas_no_contexto_referencia"]), p(i["p_rotulo"]), p(i["p_rotulo_referencia"])] for i in dado["casos"]] or [["nenhum"] + [""] * 14]),
    ]
    cab = pf.cabecalho(f"A biblioteca sem as notas do modelo e sem os verbetes aprendidos (corrida {CORRIDA})", "avaliar_fase4.py --sem_notas", f"`{dado['metadados'].get('corrida')}`",
                       dado["metadados"]["gerado_em"][:10])
    return "\n".join(cab + [""] + texto + [""] + blocos) + "\n"


def ler(saida: str, modelo: str = dv.MODELO_PADRAO) -> dict:
    """Tudo o que a leitura precisa: os registros da corrida, os casos com o gabarito, as referências, a corrida 16 e a ponte da versão em que a corrida rodou."""
    import executar_fase4 as ex
    raiz, slug = caminhos.fase3(saida)["raiz"], executar_fase3._slug(modelo)
    arq_cond = raiz / "condicoes_fase4.json"
    condicoes = json.loads(arq_cond.read_text(encoding="utf-8")) if arq_cond.exists() else {}
    arq_16 = caminhos.fase3(CORRIDA_16["saida"])["raiz"] / CORRIDA_16["subpasta"] / slug / CORRIDA_16["registros"]
    versao = condicoes.get("versao_ollama")
    return {"registros": executar_bateria.ler_jsonl(raiz / slug / f"diagnosticos__{NOME}.jsonl"), "linhas": executar_bateria.ler_jsonl(raiz / f"{NOME}.jsonl"), "casos_por_banco": casos_por_banco(),
            "referencias": referencias(modelo), "condicoes": condicoes, "corrida16": {"corrida": CORRIDA_16["corrida"], "registros": executar_bateria.ler_jsonl(arq_16)} if arq_16.exists() else None,
            "ponte": ex.ultima_ponte(ex.carregar_pontes(gravar=False), versao) if versao else None}


# ------------------------------------------------------------------ a prévia sem modelo

def previa(gerado_em: str | None = None) -> dict:
    """Sem modelo: o que muda no contexto de cada um dos 72 casos quando a biblioteca perde as notas e os aprendidos. A busca e a montagem do contexto são código,
    então dá para saber antes da corrida em quantos casos o prompt muda, se os verbetes entregues mudam e se o verbete da causa certa continua entre eles."""
    import executar_fase4 as ex
    producao = bib.carregar(dv.PASTA_CURADA)
    fechamento = json.loads((dv.PASTA_CURADA / "fechamento.json").read_text(encoding="utf-8"))
    with tempfile.TemporaryDirectory() as tmp:
        derivacao = montar_biblioteca(dv.PASTA_CURADA, Path(tmp) / PASTA_DA_COPIA)
        sem = bib.carregar(Path(tmp) / PASTA_DA_COPIA)
    indice_p, indice_s = rec.Indice(producao), rec.Indice(sem)
    notas = [nota for v in producao for nota in bib.notas(v)]
    refs, casos = referencias(), casos_por_banco()
    por_banco, diferentes = [], []
    for banco in BANCOS:
        reg = {r["caso"]: r for r in refs[banco]["registros"]}
        k = int(next(iter(reg.values()))["k"]) if reg else ct.K_DO_EXPERIMENTO
        mudancas, certo = collections.Counter(), collections.Counter()
        refeito = com_nota = com_aprendido = acertos_ref = 0
        chars_ref, chars_sem = [], []
        for c in casos[banco]:
            ref = reg.get(c["id"])
            if ref is None:
                continue
            f = ex.fixture_sem_gabarito(c)
            ctx_p, ctx_s = dv.contexto_ao_vivo(producao, indice_p, f, k), dv.contexto_ao_vivo(sem, indice_s, f, k)
            refeito += executar_fase3._sha12(ctx_p["texto"]) == ref.get("contexto_sha256")
            com_nota += bool(ref.get("notas_no_contexto"))
            com_aprendido += bool(ref.get("verbetes_novos_no_contexto"))
            mudanca = mudanca_do_contexto({"contexto_sha256": executar_fase3._sha12(ctx_s["texto"]), "verbetes_ids": ctx_s["verbetes_ids"]}, ref)
            mudancas[mudanca] += 1
            g = c["gabarito"]["causa_raiz"]
            acertos_ref += ct.rotulo_lido(ref.get("resposta")) == g
            certo[(g in (ref.get("verbetes_ids") or []), g in ctx_s["verbetes_ids"])] += 1
            chars_ref.append(len(ctx_p["texto"]))
            chars_sem.append(len(ctx_s["texto"]))
            if mudanca == MUDANCAS[3]:
                antes, depois = list(ref.get("verbetes_ids") or []), list(ctx_s["verbetes_ids"])
                diferentes.append({"caso": c["id"], "banco": banco, "antes": antes, "depois": depois, "saiu": [i for i in antes if i not in depois], "entrou": [i for i in depois if i not in antes]})
        n_casos = sum(mudancas.values())
        por_banco.append({"banco": banco, "referencia": f"corrida {refs[banco]['corrida']}", "casos": n_casos, "k": k, "contexto_da_referencia_refeito_igual": refeito,
                          "acertos_referencia": acertos_ref, "com_nota_na_referencia": com_nota, "com_aprendido_na_referencia": com_aprendido, "mudancas": [{"mudanca": m, "casos": mudancas[m]} for m in MUDANCAS],
                          "verbete_certo": [{"antes": a, "depois": d, "casos": certo[(a, d)]} for a in (True, False) for d in (True, False)],
                          "chars_do_contexto_mediana_referencia": ct._mediana(chars_ref), "chars_do_contexto_mediana_sem_notas": ct._mediana(chars_sem),
                          "segundos_mediana_referencia": ct._mediana([r.get("segundos") for r in reg.values()])})

    def soma(mudanca: str) -> int:
        return sum(m["casos"] for b in por_banco for m in b["mudancas"] if m["mudanca"] == mudanca)

    total = sum(b["casos"] for b in por_banco)
    segundos = sum(b["casos"] * (b["segundos_mediana_referencia"] or 0) for b in por_banco)
    return {"metadados": {"gerado_em": gerado_em or time.strftime("%Y-%m-%dT%H:%M:%S"), "numero": CORRIDA},
            "biblioteca": {**derivacao, "lote_promovido_em": fechamento.get("promovido_em"), "verbetes_producao": len(producao), "verbetes_sem_notas": len(sem), "notas_em_forma_de_instrucao": sum(1 for x in notas if x["texto"].startswith(VERBOS_DE_INSTRUCAO)),
                           "tokens_estimados_producao": bib.estimar_tokens(bib.render_biblioteca(producao)), "tokens_estimados_sem_notas": bib.estimar_tokens(bib.render_biblioteca(sem))},
            "resumo": {"casos": total, "acertos_referencia": sum(b["acertos_referencia"] for b in por_banco), "contextos_identicos": soma(MUDANCAS[0]), "contextos_que_mudam": total - soma(MUDANCAS[0]), "mesmos_verbetes_sem_as_notas": soma(MUDANCAS[1]),
                       "mesmos_verbetes_outra_ordem": soma(MUDANCAS[2]), "verbetes_diferentes": soma(MUDANCAS[3]), "com_nota_na_referencia": sum(b["com_nota_na_referencia"] for b in por_banco),
                       "com_aprendido_na_referencia": sum(b["com_aprendido_na_referencia"] for b in por_banco),
                       "verbete_certo_antes": sum(v["casos"] for b in por_banco for v in b["verbete_certo"] if v["antes"]),
                       "verbete_certo_depois": sum(v["casos"] for b in por_banco for v in b["verbete_certo"] if v["depois"]),
                       "verbete_certo_mudou": sum(v["casos"] for b in por_banco for v in b["verbete_certo"] if v["antes"] != v["depois"]),
                       "inferencias": total, "minutos_estimados_pela_mediana_das_referencias": round(segundos / 60)},
            "por_banco": por_banco, "casos_com_verbetes_diferentes": diferentes, "regra": texto_da_regra()}


def render_previa(dado: dict) -> str:
    b_, r, n = dado["biblioteca"], dado["resumo"], ct._n
    texto = [(f"Sem modelo. A biblioteca de produção (`{b_['origem_hash']}`) tem {n(b_['verbetes_producao'])} verbetes e {n(b_['notas_retiradas'])} notas do modelo em "
              f"{n(b_['verbetes_com_notas'])} deles, {n(b_['notas_em_forma_de_instrucao'])} escritas como instrução. A cópia sem as notas e sem os {len(b_['verbetes_retirados'])} verbetes aprendidos "
              f"(`{b_['hash']}`) fica com {n(b_['verbetes_sem_notas'])} verbetes. Como a busca e a montagem do contexto são código, dá para saber antes da corrida {CORRIDA} o que muda no "
              "contexto de cada caso: a busca perde o texto das notas no índice, e o verbete entregue perde o trecho das notas."),
             "", (f"Dos {n(r['casos'])} casos, o contexto muda em {n(r['contextos_que_mudam'])}: em {n(r['mesmos_verbetes_sem_as_notas'])} os verbetes entregues são os mesmos, na mesma ordem, só sem as "
                  f"notas; em {n(r['mesmos_verbetes_outra_ordem'])} são os mesmos em outra ordem; em {n(r['verbetes_diferentes'])} a busca troca um verbete. Na referência, {n(r['com_nota_na_referencia'])} "
                  f"contextos traziam ao menos uma nota e {n(r['com_aprendido_na_referencia'])} traziam um verbete aprendido. O verbete da causa certa estava entre os entregues em "
                  f"{n(r['verbete_certo_antes'])} casos e continua em {n(r['verbete_certo_depois'])}; a presença dele muda em {n(r['verbete_certo_mudou'])}. Pela mediana das corridas de "
                  f"referência, as {n(r['inferencias'])} inferências levam cerca de {n(r['minutos_estimados_pela_mediana_das_referencias'])} minutos."),
             "", dado["regra"]]
    blocos = [
        a3b.tab(f"{PREFIXO}previa_biblioteca", ["Biblioteca", "Hash", "Verbetes", "Notas do modelo", "Verbetes com nota", "Notas em forma de instrução", "Tokens estimados da biblioteca inteira"],
                [["produção", f"`{b_['origem_hash']}`", n(b_["verbetes_producao"]), n(b_["notas_retiradas"]), n(b_["verbetes_com_notas"]), n(b_["notas_em_forma_de_instrucao"]), n(b_["tokens_estimados_producao"])],
                 ["sem as notas e sem os aprendidos", f"`{b_['hash']}`", n(b_["verbetes_sem_notas"]), "0", "0", "0", n(b_["tokens_estimados_sem_notas"])]]),
        a3b.tab(f"{PREFIXO}previa_banco", ["Banco", "Referência", "Casos", "Acertos na referência", "Contexto da referência refeito igual", "Com nota na referência", "Com verbete aprendido na referência"]
                + [m[0].upper() + m[1:] for m in MUDANCAS] + ["Verbete certo antes e depois", "Verbete certo só antes", "Verbete certo só depois", "Caracteres do contexto (mediana) na referência",
                                                              "Caracteres do contexto (mediana) sem as notas"],
                [[NOME_DO_BANCO.get(b["banco"], b["banco"]), b["referencia"], n(b["casos"]), n(b["acertos_referencia"]), n(b["contexto_da_referencia_refeito_igual"]), n(b["com_nota_na_referencia"]), n(b["com_aprendido_na_referencia"])]
                 + [n(m["casos"]) for m in b["mudancas"]]
                 + [n(next(v["casos"] for v in b["verbete_certo"] if v["antes"] is a and v["depois"] is d)) for a, d in ((True, True), (True, False), (False, True))]
                 + [n(b["chars_do_contexto_mediana_referencia"]), n(b["chars_do_contexto_mediana_sem_notas"])] for b in dado["por_banco"]]),
        a3b.tab(f"{PREFIXO}previa_verbetes", ["Caso", "Banco", "Verbetes na referência", "Verbetes sem as notas", "Saiu", "Entrou"],
                [[f"`{x['caso']}`", x["banco"], _lista(x["antes"]), _lista(x["depois"]), _lista(x["saiu"]), _lista(x["entrou"])] for x in dado["casos_com_verbetes_diferentes"]]
                or [["nenhum", "", "", "", "", ""]]),
    ]
    cab = pf.cabecalho(f"Prévia sem modelo da corrida {CORRIDA}: o que muda no contexto sem as notas do modelo", "experimento_sem_notas.py --previa",
                       "`biblioteca_producao/`, `fase4_trilha` e `fase4_ineditos`", dado["metadados"]["gerado_em"][:10])
    return "\n".join(cab + [""] + texto + [""] + blocos) + "\n"


# ------------------------------------------------------------------ a corrida

def rodar(args: argparse.Namespace) -> int:
    """Corrida 25: os 36 oficiais e os 36 inéditos em texto, pelo diagnóstico do agente, com a cópia sem notas da biblioteca de produção e o k e os limiares da
    calibração. Não escreve fora da pasta da corrida. Relançar retoma do caso em que parou."""
    import executar_fase4 as ex
    saida = caminhos.fase3(args.saida)["raiz"]
    saida.mkdir(parents=True, exist_ok=True)
    marco = ex._marcador(saida / "fase4.log")
    t0 = time.monotonic()
    inicio = time.strftime("%Y-%m-%dT%H:%M:%S")
    modelo, slug = args.modelo, executar_fase3._slug(args.modelo)
    parcial = bool(args.casos)
    versao, segue = ct._guardas(args, marco)
    if not segue:
        return 2
    refs = referencias(modelo)
    faltam = [f"corrida {x['corrida']}" for x in refs.values() if not x["registros"]]
    if faltam and not parcial:
        marco(f"!! faltam os registros de referência ({', '.join(faltam)}) em {caminhos.RESULTADOS}")
        return 2
    ponte = ex.ultima_ponte(ex.carregar_pontes(gravar=False), versao)
    if {r.get("versao_ollama") for x in refs.values() for r in x["registros"]} != {versao}:
        ok, motivo = segue_depois_da_ponte(ponte, parcial)
        marco(("" if ok else "!! ") + motivo)
        if not ok:
            return 2
    limiares = dv.carregar_limiares(Path(args.limiares) if args.limiares else None)
    if limiares is None and not parcial:
        marco("!! sem limiares.json (regra R7): rode --modo calibracao antes")
        return 2
    k = int((limiares or {}).get("k") or ct.K_DO_EXPERIMENTO)
    if not evo.snapshot_fechado(dv.PASTA_CURADA):
        marco(f"!! a biblioteca de produção em {dv.PASTA_CURADA} não existe ou não está fechada (sem fechamento.json)")
        return 2
    try:
        derivacao = montar_biblioteca(dv.PASTA_CURADA, saida / "bibliotecas" / slug / PASTA_DA_COPIA)
    except SystemExit as e:
        marco(f"!! {e}")
        return 2
    verbetes = bib.carregar(saida / "bibliotecas" / slug / PASTA_DA_COPIA)
    indice = rec.Indice(verbetes)
    pares = casos_do_experimento(args.casos)
    if len({c["id"] for _, c in pares}) != len(pares):
        marco("!! há caso com o mesmo id nos dois bancos; a corrida grava uma linha por id")
        return 2
    caso0 = ex.fixture_sem_gabarito(pares[0][1])
    ctx0, prompt0 = dv.montar_prompt(verbetes, indice, caso0, k)
    hash_fixo = dv.hash_prompt_fixo(verbetes, ctx0, caso0, prompt0)
    for r in REFERENCIAS.values():
        arq = caminhos.fase3(r["saida"])["raiz"] / "condicoes_fase4.json"
        fixo_ref = json.loads(arq.read_text(encoding="utf-8")).get("hash_prompt_fixo") if arq.exists() else None
        if fixo_ref and fixo_ref != hash_fixo and not parcial:
            marco(f"!! a parte fixa do prompt ({hash_fixo}) não é a da corrida {r['corrida']} ({fixo_ref}); a comparação não vale")
            return 2
    pasta_reg = saida / slug
    pasta_reg.mkdir(parents=True, exist_ok=True)
    arq_diag, arq_lat, arq_resumo, arq_trilha = pasta_reg / f"diagnosticos__{NOME}.jsonl", pasta_reg / f"logprobs__{NOME}.jsonl", saida / f"{NOME}.jsonl", saida / f"trilha_{NOME}.jsonl"
    feitos = {r["caso"] for r in executar_bateria.ler_jsonl(arq_resumo)}
    fechamento = json.loads((dv.PASTA_CURADA / "fechamento.json").read_text(encoding="utf-8"))
    condicoes = {"modo": NOME, "corrida": CORRIDA, "criado_em": inicio, "saida": args.saida, "modelo": modelo, "versao_ollama": versao, "k": k, "limiares": limiares, "casos": len(pares),
                 "casos_por_banco": {b: sum(1 for x, _ in pares if x == b) for b in BANCOS}, "parcial": parcial, "top_logprobs": args.top, "teto_tokens": args.teto,
                 "hash_prompt_fixo": hash_fixo, "hash_indice": dv.hash_indice(indice),
                 "biblioteca": {**derivacao, "origem": "Programacao/AgenteCore/biblioteca_producao", "lote_promovido_em": fechamento.get("promovido_em"),
                                "o_que_saiu": "a seção Notas do modelo de cada verbete e a pasta aprendidos/"},
                 "referencias": {b: {"corrida": r["corrida"], "saida": r["saida"]} for b, r in REFERENCIAS.items()}, "ponte": ponte, "regra": texto_da_regra()}
    (saida / "condicoes_fase4.json").write_text(json.dumps(condicoes, ensure_ascii=False, indent=2), encoding="utf-8")
    marco(f"INÍCIO {NOME}: Ollama {versao}, {modelo}, biblioteca de produção ({derivacao['origem_hash']}) sem {derivacao['notas_retiradas']} notas e sem {len(derivacao['verbetes_retirados'])} "
          f"verbetes aprendidos ({derivacao['hash']}), k = {k}; {len(pares)} casos; {len(feitos)} já feito(s)")
    digest, versao_ollama = e3b._preparar_modelo(modelo)
    if versao_ollama != versao:
        marco(f"!! a versão do Ollama mudou antes de começar: {versao} para {versao_ollama}")
        return 2
    comum = {"digest": digest, "versao_ollama": versao_ollama, "maquina": platform.node(), "epoca": dv.VERSAO_CURADA + 1, "biblioteca_epoca": dv.VERSAO_CURADA,
             "biblioteca_versao": derivacao["hash"], "particao": None}
    if arq_trilha.exists() and feitos:
        trilha = tr.Trilha.carregar(arq_trilha)
        trilha.pasta_blobs = saida / "blobs"
    else:
        trilha = tr.Trilha(versao=tr.V2, pasta_blobs=saida / "blobs")
        trilha.corrida(tr.cabecalho_de_corrida(modelo=modelo, versao_ollama=versao, inicio=inicio, quantizacao=dv.quantizacao_do_modelo(modelo), top_logprobs=args.top,
                                               leitura_da_probabilidade=dv.LEITURA_DA_PROBABILIDADE, hash_biblioteca=derivacao["hash"], hash_prompt_fixo=hash_fixo, hash_indice=dv.hash_indice(indice),
                                               corrida=args.saida, etapas_registradas=["recuperacao", "prompt", "diagnostico"],
                                               etapas_nao_registradas=["roteiro", "interceptacao", "poda", "cura", "edicao_biblioteca", "intervencao"],
                                               extras={"modo": NOME, "k": k, "limiares": limiares}), ts=inicio)

    def _loop() -> None:
        for n, (banco, caso) in enumerate(pares, 1):
            if caso["id"] in feitos:
                continue
            caso_f = ex.fixture_sem_gabarito(caso)
            tid = f"{args.saida}/{slug}/{caso['id']}"
            ts = time.strftime("%Y-%m-%dT%H:%M:%S")
            trilha.evento("entrada", tid, {"caso": caso["id"], "classe": caso["classe"], "nivel": caso["nivel"], "origem": "fixture", "texto": trilha.blob(estrategias._dados_do_caso(caso_f), "caso")},
                          "ao_vivo", ts=ts)
            sv = dv.diagnosticar(trilha, tid, caso_f, verbetes, indice, k=k, modelo=modelo, comum=comum, limiares=limiares, intervencoes="desligadas", top=args.top, teto=args.teto, ts=ts)
            executar_fase3._gravar(arq_diag, sv["registro"])
            executar_fase3._gravar(arq_lat, sv["lateral"])
            confianca = sv["no"]["confianca"]
            executar_fase3._gravar(arq_resumo, {"caso": caso["id"], "banco": banco, "p_rotulo": confianca.get("p_rotulo"), "selo": confianca.get("selo"), "verbetes_ids": sv["registro"]["verbetes_ids"],
                                                "segundos": sv["registro"]["segundos"]})
            trilha.gravar(arq_trilha)
            ex._conferir_versao(versao)
            marco(f"[{n}/{len(pares)}] {banco} {caso['id']}: {sv['no']['escolha']} (p {confianca.get('p_rotulo')}, selo {confianca.get('selo')}; {sv['registro']['segundos']} s)")

    try:
        e3b._com_modelo_descarregado(modelo, _loop)
    except SystemExit as e:
        marco(f"!! corrida parou: {e}")
        return 1
    trilha.fechar(time.strftime("%Y-%m-%dT%H:%M:%S"))
    trilha.gravar(arq_trilha)
    marco(f"FIM {NOME}: {len(pares)} casos; duração {time.monotonic() - t0:.0f} s; trilha {arq_trilha.stat().st_size} bytes")
    return 0


# ------------------------------------------------------------------ linha de comando

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--previa", action="store_true", help=f"grava a prévia sem modelo em resultados_alvo/fase4/{NOME_PREVIA}.json e .md")
    ap.add_argument("--check", action="store_true", help="com --previa: regera e compara com o gravado, sem gravar")
    ap.add_argument("--ponte", action="store_true", help="imprime a versão do Ollama no ar, a ponte que falta para ela (se falta) e se a registrada é pareável")
    args = ap.parse_args(argv)
    if args.previa:
        import avaliar_fase4 as av
        dado = previa()
        return pf.fechar(NOME_PREVIA, dado, render_previa(dado), f"{PREFIXO}previa_", check=args.check, pasta=caminhos.RESULTADOS / "fase4", doc=av.RELATORIO)
    if args.ponte:
        s = situacao_da_ponte()
        if not s["versao"]:
            print("o Ollama não respondeu em /api/version; suba o servidor antes", file=sys.stderr)
            return 3
        ponte = s["ponte"] or {}
        print(f"versao={s['versao']}")
        print(f"falta={s['falta'] or ''}")
        print(f"pareavel={'sim' if ponte.get('pareavel') else ('nao' if ponte else '')}")
        # ! Alteração de IA - Revisar: (11/11/2026) linha nova, `pasta=`, com a pasta da ponte da versão no ar (vazia quando a ponte falta).
        # ! Motivo: o lançador precisa do nome da pasta para pôr a ponte no registro das áreas só de leitura (`testar_fase4.py --registrar-ponte`) antes da bateria
        # que roda no começo da corrida; sem isso a pasta nova da ponte faz a bateria falhar, como aconteceu na corrida 25 em 11/11/2026.
        print(f"pasta={ponte.get('corrida') or ''}")
        return 0
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
