#!/usr/bin/env python3
# ! Alteração de IA - Revisar: aplica os gabaritos aos resultados e agrega as métricas —
# agora também por CONDIÇÃO de biblioteca (Fase 2-B), com Δ contra a linha de base,
# McNemar pareado por caso, intervalo de Wilson, ancoragem, recuperação e flips de
# quantização.
# ! Motivo: com 270 inferências por modelo, conferir à mão é inviável e subjetivo. O
# gabarito de cada caso traz a causa raiz do conjunto fechado, o campo afetado e listas de
# termos, então a pontuação é determinística e repetível. Na Fase 2-B cada modelo roda o
# MESMO conjunto de 90 casos sob várias condições — comparação pareada, executada uma vez
# por condição; para esse desenho Dietterich (1998) mostra que McNemar é o único teste
# com erro tipo I aceitável (Memorial §6.5). Os cortes antigos ficam restritos a A0 para
# os números da Fase 2-A continuarem reproduzíveis.
#
# A métrica "formato_valido_conteudo_errado" existe por causa de um achado da literatura
# (The Constraint Tax, único trabalho no regime sub-3B): medir apenas "a resposta parseou?"
# deixa cego para a maior parte dos erros, porque saída perfeitamente formatada com
# conteúdo semanticamente errado chegou a 88,9% dos casos naquele estudo.
import json
import math
import re
import statistics
import unicodedata
from collections import defaultdict
from pathlib import Path

import biblioteca as bib
from taxonomia import CAUSAS_RAIZ

AQUI = Path(__file__).resolve().parent
SAIDA = AQUI / "resultados"


def _normalizar(texto: str) -> str:
    """Minúsculas e sem acento, para os termos casarem independente de grafia."""
    sem_acento = unicodedata.normalize("NFKD", texto)
    return "".join(c for c in sem_acento if not unicodedata.combining(c)).lower()


_PERMITIDAS = {_normalizar(c) for c in CAUSAS_RAIZ}

# Sufixos de tag do Ollama que identificam a mesma família/porte noutra quantização —
# usados para parear a ablação Q8 com o modelo Q4_K_M padrão e contar flips.
_SUFIXO_QUANT = re.compile(r"-instruct-(q8_0|fp16|q6_k|q5_k_m|q4_k_m|q4_0)$", re.IGNORECASE)


def _base_modelo(nome: str) -> str:
    return _SUFIXO_QUANT.sub("", nome)


def extrair(resposta: str) -> dict:
    """Lê as linhas finais pedidas no prompt. Tolerante: aceita a linha em qualquer
    posição e ignora marcação de negrito que alguns modelos acrescentam."""
    limpa = resposta.replace("*", "").replace("`", "")

    def _campo(nome):
        m = re.search(rf"{nome}\s*:\s*(.+)", limpa, re.IGNORECASE)
        return m.group(1).strip() if m else None

    causa = _campo("CAUSA_RAIZ")
    fonte = _campo("FONTE")
    return {
        "causa_raiz": causa.split()[0].lower() if causa and causa.split() else None,
        "campo": _campo("CAMPO"),
        "impacto": _campo("IMPACTO"),
        "fonte_ids": re.findall(r"\[([a-z0-9_\-]+)\]", fonte) if fonte else [],
    }


def avaliar_registro(r: dict, causas_com_defeito: set[str]) -> dict:
    gab = r["gabarito"]
    resposta = r.get("resposta", "")
    lido = extrair(resposta)
    resp_norm = _normalizar(resposta)

    # Comparação sem acento: o conjunto fechado é escrito sem acentuação, e alguns modelos
    # devolvem "coleção_no_lugar_de_objeto" em vez de "colecao_no_lugar_de_objeto". Exigir
    # a grafia exata mediria transcrição, não diagnóstico — o rótulo escolhido é o mesmo.
    formato_ok = lido["causa_raiz"] is not None
    causa_norm = _normalizar(lido["causa_raiz"]) if formato_ok else None
    causa_ok = formato_ok and causa_norm == _normalizar(gab["causa_raiz"])
    # Responder fora do conjunto permitido é falha de seguir instrução, diferente de
    # escolher o rótulo errado dentro do conjunto — as duas contam separado.
    fora_do_conjunto = formato_ok and causa_norm not in _PERMITIDAS

    campo_esperado = gab.get("campo_afetado")
    if campo_esperado is None:
        campo_ok = lido["campo"] is None or "nenhum" in _normalizar(lido["campo"] or "")
    else:
        campo_ok = bool(lido["campo"]) and _normalizar(campo_esperado) in _normalizar(lido["campo"])

    esperados = [t for t in gab.get("termos_esperados", []) if _normalizar(t) in resp_norm]
    proibidos = [t for t in gab.get("termos_proibidos", []) if _normalizar(t) in resp_norm]

    # Campos da Fase 2-B; registros da 2-A não os têm e recebem os valores de A0.
    condicao = r.get("condicao", "A0")
    dados = r.get("verbetes_ids") or []
    citados = set(lido["fonte_ids"]) | {i for i in dados if f"[{i}]" in resposta}
    plantada = r.get("causa_plantada")

    return {
        **{k: r[k] for k in ("modelo", "caso", "classe", "nivel", "estrategia", "segundos",
                             "tokens_saida", "somente_cpu")},
        "condicao": condicao,
        "modelo_base": _base_modelo(r["modelo"]),
        "tokens_entrada": r.get("tokens_entrada", 0),
        "prefill_ms": r.get("prefill_ms"),
        "geracao_ms": r.get("geracao_ms"),
        "chars_contexto": r.get("chars_contexto", 0),
        "erro_infra": bool(r.get("erro")),
        "formato_valido": formato_ok,
        "fora_do_conjunto": fora_do_conjunto,
        "causa_correta": causa_ok,
        "campo_correto": campo_ok,
        # parseou certinho mas errou o conteúdo — o erro que passa despercebido
        "formato_valido_conteudo_errado": formato_ok and not causa_ok,
        "termos_esperados_encontrados": len(esperados),
        "termos_esperados_total": len(gab.get("termos_esperados", [])),
        # termo proibido presente indica diagnóstico numa direção errada conhecida
        "sinal_de_diagnostico_errado": len(proibidos) > 0,
        "causa_respondida": lido["causa_raiz"],
        "causa_esperada": gab["causa_raiz"],
        # ancoragem e recuperação (só fazem sentido fora de A0)
        "citou_verbete": bool(citados & set(dados)),
        "ouro_no_contexto": bool(r.get("verbete_ouro")) and r["verbete_ouro"] in dados,
        "causa_plantada": plantada,
        "seguiu_causa_plantada": bool(plantada) and causa_norm == _normalizar(plantada),
        "defeito_documentado": gab["causa_raiz"] in causas_com_defeito,
    }


def carregar() -> list[dict]:
    linhas = []
    for arq in sorted(SAIDA.glob("*.jsonl")):
        with open(arq, encoding="utf-8") as f:
            for linha in f:
                try:
                    linhas.append(json.loads(linha))
                except json.JSONDecodeError:
                    continue
    return linhas


def wilson(acertos: int, n: int, z: float = 1.96) -> tuple[float, float]:
    """Intervalo de confiança de 95% para uma proporção (Wilson), em pontos percentuais."""
    if n == 0:
        return (0.0, 0.0)
    p = acertos / n
    denom = 1 + z * z / n
    centro = (p + z * z / (2 * n)) / denom
    meia = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return (round(100 * (centro - meia), 1), round(100 * (centro + meia), 1))


def mcnemar_exato(b: int, c: int) -> float:
    """p bilateral do teste de McNemar exato (binomial): b = só a 2ª condição acertou,
    c = só a 1ª acertou. Com n = b + c pequeno, a versão exata é a indicada."""
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    cauda = sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n
    return round(min(1.0, 2 * cauda), 4)


def _mediana(valores):
    v = [x for x in valores if x is not None]
    return round(statistics.median(v), 1) if v else None


def agregar(avaliados: list[dict], *chaves: str) -> list[dict]:
    grupos = defaultdict(list)
    for a in avaliados:
        grupos[tuple(a[k] for k in chaves)].append(a)

    saida = []
    for chave, itens in sorted(grupos.items(), key=lambda x: [str(v) for v in x[0]]):
        n = len(itens)
        validos = [i for i in itens if i["segundos"] is not None]
        acertos = sum(i["causa_correta"] for i in itens)
        pct = lambda campo: round(100 * sum(i[campo] for i in itens) / n, 1)  # noqa: E731
        linha = {
            **dict(zip(chaves, chave)),
            "n": n,
            "erros_infra": sum(i["erro_infra"] for i in itens),
            "causa_correta_pct": round(100 * acertos / n, 1),
            "causa_correta_ic95": wilson(acertos, n),
            "campo_correto_pct": pct("campo_correto"),
            "formato_valido_pct": pct("formato_valido"),
            "formato_ok_conteudo_errado_pct": pct("formato_valido_conteudo_errado"),
            "fora_do_conjunto_pct": pct("fora_do_conjunto"),
            "diagnostico_errado_pct": pct("sinal_de_diagnostico_errado"),
            "segundos_medio": round(sum(i["segundos"] for i in validos) / len(validos), 2)
                if validos else None,
            "segundos_mediana": _mediana(i["segundos"] for i in validos),
            "tokens_saida_medio": round(sum(i["tokens_saida"] for i in validos) / len(validos))
                if validos else None,
            "tokens_entrada_mediana": _mediana(i["tokens_entrada"] for i in validos),
            "prefill_ms_mediana": _mediana(i["prefill_ms"] for i in validos),
            "geracao_ms_mediana": _mediana(i["geracao_ms"] for i in validos),
        }
        if "condicao" in chaves and chave[chaves.index("condicao")] != "A0":
            linha["citou_verbete_pct"] = pct("citou_verbete")
            linha["ouro_no_contexto_pct"] = pct("ouro_no_contexto")
            if any(i["causa_plantada"] for i in itens):
                linha["seguiu_causa_plantada_pct"] = pct("seguiu_causa_plantada")
        saida.append(linha)
    return saida


def comparar_com_base(avaliados: list[dict]) -> list[dict]:
    """Para cada (modelo, condição ≠ A0) no braço linear: Δ de acerto contra A0-linear do
    mesmo modelo, pareado caso a caso, com McNemar exato."""
    por_chave = defaultdict(dict)
    for a in avaliados:
        if a["estrategia"] == "linear":
            por_chave[(a["modelo"], a["condicao"])][a["caso"]] = a["causa_correta"]
    saida = []
    for (modelo, cond), casos in sorted(por_chave.items()):
        if cond == "A0":
            continue
        base = por_chave.get((modelo, "A0"))
        if not base:
            continue
        comuns = sorted(set(casos) & set(base))
        b = sum(1 for c in comuns if casos[c] and not base[c])
        cc = sum(1 for c in comuns if base[c] and not casos[c])
        n = len(comuns)
        if not n:
            continue
        acerto_base = round(100 * sum(base[c] for c in comuns) / n, 1)
        acerto_cond = round(100 * sum(casos[c] for c in comuns) / n, 1)
        saida.append({
            "modelo": modelo, "condicao": cond, "n_pares": n,
            "acerto_A0_pct": acerto_base, "acerto_pct": acerto_cond,
            "delta_pp": round(acerto_cond - acerto_base, 1),
            "so_condicao_acertou": b, "so_A0_acertou": cc,
            "p_mcnemar": mcnemar_exato(b, cc),
        })
    return saida


def flips_quantizacao(avaliados: list[dict]) -> list[dict]:
    """Mesmo modelo-base em quantizações diferentes, mesma condição e estratégia: acerto
    de cada um e quantas respostas mudaram de lado (flips), pareado por caso."""
    por = defaultdict(dict)
    for a in avaliados:
        por[(a["modelo_base"], a["condicao"], a["estrategia"], a["modelo"])][a["caso"]] = a
    saida = []
    grupos = defaultdict(list)
    for (base, cond, est, modelo) in por:
        grupos[(base, cond, est)].append(modelo)
    for (base, cond, est), modelos in sorted(grupos.items()):
        if base not in modelos or len(modelos) < 2:
            continue
        ref = por[(base, cond, est, base)]
        for m in sorted(modelos):
            if m == base:
                continue
            var = por[(base, cond, est, m)]
            comuns = sorted(set(ref) & set(var))
            if not comuns:
                continue
            c2e = sum(1 for c in comuns if ref[c]["causa_correta"] and not var[c]["causa_correta"])
            e2c = sum(1 for c in comuns if var[c]["causa_correta"] and not ref[c]["causa_correta"])
            mudou = sum(1 for c in comuns
                        if ref[c]["causa_respondida"] != var[c]["causa_respondida"])
            n = len(comuns)
            acerto_ref = sum(ref[c]["causa_correta"] for c in comuns)
            acerto_var = sum(var[c]["causa_correta"] for c in comuns)
            saida.append({
                "modelo_base": base, "variante": m, "condicao": cond, "estrategia": est,
                "n": n,
                "acerto_base_pct": round(100 * acerto_ref / n, 1),
                "acerto_variante_pct": round(100 * acerto_var / n, 1),
                "flips_certo_para_errado": c2e, "flips_errado_para_certo": e2c,
                "respostas_diferentes_pct": round(100 * mudou / len(comuns), 1),
                "segundos_base": _mediana(ref[c]["segundos"] for c in comuns),
                "segundos_variante": _mediana(var[c]["segundos"] for c in comuns),
            })
    return saida


def main() -> None:
    brutos = carregar()
    if not brutos:
        print(f"Nenhum resultado em {SAIDA}. Rode executar_bateria.py primeiro.")
        return

    try:
        causas_com_defeito = bib.causas_com_defeito_documentado(bib.carregar())
    except FileNotFoundError:
        causas_com_defeito = set()
    avaliados = [avaliar_registro(r, causas_com_defeito) for r in brutos]
    (AQUI / "avaliacao.json").write_text(
        json.dumps(avaliados, ensure_ascii=False, indent=2), encoding="utf-8")

    # Cortes da Fase 2-A, restritos a A0 e ao modelo Q4_K_M padrão: continuam produzindo
    # exatamente os números já publicados nos gráficos 01–06.
    base = [a for a in avaliados if a["condicao"] == "A0" and a["modelo"] == a["modelo_base"]]
    cortes_base = {
        "por_modelo": ("modelo",),
        "por_modelo_estrategia": ("modelo", "estrategia"),
        "por_modelo_classe": ("modelo", "classe"),
        "por_modelo_nivel": ("modelo", "nivel"),
        "por_estrategia": ("estrategia",),
    }
    resumo = {nome: agregar(base, *ch) for nome, ch in cortes_base.items()}

    # Cortes da Fase 2-B: por condição, sempre no braço linear (o único que roda com
    # biblioteca), incluindo a linha de base A0-linear para leitura lado a lado.
    linear = [a for a in avaliados if a["estrategia"] == "linear"]
    cortes_2b = {
        "por_modelo_condicao": ("modelo", "condicao"),
        "por_modelo_condicao_classe": ("modelo", "condicao", "classe"),
        "por_modelo_condicao_nivel": ("modelo", "condicao", "nivel"),
        "por_modelo_condicao_defeito": ("modelo", "condicao", "defeito_documentado"),
        "por_condicao": ("condicao",),
    }
    resumo.update({nome: agregar(linear, *ch) for nome, ch in cortes_2b.items()})
    resumo["comparacoes"] = comparar_com_base(avaliados)
    resumo["quantizacao"] = flips_quantizacao(avaliados)
    (AQUI / "resumo_metricas.json").write_text(
        json.dumps(resumo, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"{len(brutos)} inferências avaliadas\n")
    print(f"{'modelo':34} {'cond':5} {'n':>4} {'causa%':>7} {'IC95':>14} {'campo%':>7} "
          f"{'cita%':>6} {'ouro%':>6} {'prefill ms':>11} {'seg':>6}")
    for r in resumo["por_modelo_condicao"]:
        ic = f"{r['causa_correta_ic95'][0]}–{r['causa_correta_ic95'][1]}"
        print(f"{r['modelo']:34} {r['condicao']:5} {r['n']:4} {r['causa_correta_pct']:7} {ic:>14} "
              f"{r['campo_correto_pct']:7} {str(r.get('citou_verbete_pct', '-')):>6} "
              f"{str(r.get('ouro_no_contexto_pct', '-')):>6} "
              f"{str(r['prefill_ms_mediana'] or '-'):>11} {str(r['segundos_mediana'] or '-'):>6}")

    if resumo["comparacoes"]:
        print("\nΔ contra A0 (linear, pareado por caso; McNemar exato):")
        for c in resumo["comparacoes"]:
            sig = "*" if c["p_mcnemar"] < 0.05 else " "
            print(f"  {c['modelo']:34} {c['condicao']}: {c['acerto_A0_pct']:5} → {c['acerto_pct']:5} "
                  f"({c['delta_pp']:+.1f} pp) b={c['so_condicao_acertou']} c={c['so_A0_acertou']} "
                  f"p={c['p_mcnemar']}{sig}")
    if resumo["quantizacao"]:
        print("\nQuantização (flips contra o Q4_K_M padrão):")
        for q in resumo["quantizacao"]:
            print(f"  {q['variante']:40} {q['condicao']}/{q['estrategia']}: "
                  f"{q['acerto_base_pct']} → {q['acerto_variante_pct']}%  "
                  f"flips ✓→✗ {q['flips_certo_para_errado']}, ✗→✓ {q['flips_errado_para_certo']}, "
                  f"resposta diferente em {q['respostas_diferentes_pct']}%")

    # Guarda contra o modo de falha que já ocorreu uma vez: resposta cortada no teto de
    # tokens nunca chega às linhas finais, e o caso pontua zero por truncamento, não por
    # erro de raciocínio. Duas situações diferentes, que antes eram contadas como uma só:
    #  - bateu no teto MAS já tinha emitido a resposta: o corte pegou só texto sobrando,
    #    o caso continua válido;
    #  - bateu no teto SEM concluir: aí sim o caso é inválido, e a nota zero seria lida
    #    como erro de raciocínio quando na verdade a resposta nunca saiu.
    # A segunda contagem é também uma medida legítima do modelo: com instrução explícita
    # de brevidade e orçamento generoso, não concluir é característica dele, não do teste.
    cortado_ok = defaultdict(int)
    cortado_sem_resposta = defaultdict(int)
    for b in brutos:
        if b.get("teto_tokens") and b.get("tokens_saida", 0) >= b["teto_tokens"]:
            chave = (b["modelo"], b.get("condicao", "A0"), b["estrategia"])
            if "CAUSA_RAIZ" in b.get("resposta", ""):
                cortado_ok[chave] += 1
            else:
                cortado_sem_resposta[chave] += 1
    if cortado_sem_resposta:
        print("\n!! NÃO CONCLUÍRAM DENTRO DO ORÇAMENTO DE TOKENS (casos inválidos):")
        for (m, cond, e), n in sorted(cortado_sem_resposta.items()):
            print(f"   {m} / {cond} / {e}: {n} respostas sem CAUSA_RAIZ — excluir ou refazer com teto maior")
    if cortado_ok:
        print("\n(i) Cortadas no teto mas COM resposta emitida (casos válidos):")
        for (m, cond, e), n in sorted(cortado_ok.items()):
            print(f"   {m} / {cond} / {e}: {n}")

    infra = sum(a["erro_infra"] for a in avaliados)
    if infra:
        print(f"\n!! {infra} inferências com erro de infraestrutura (rede/timeout) — contadas "
              "como erradas nos percentuais; ver coluna erros_infra")
    cpu = [a for a in avaliados if not a["somente_cpu"]]
    if cpu:
        print(f"\n!! {len(cpu)} inferências NÃO ficaram só em CPU — medição comprometida")


if __name__ == "__main__":
    main()
