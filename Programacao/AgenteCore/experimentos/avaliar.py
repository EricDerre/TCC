#!/usr/bin/env python3
# ! Alteração de IA - Revisar: aplica os gabaritos aos resultados e agrega as métricas.
# ! Motivo: com 270 inferências por modelo, conferir à mão é inviável e subjetivo. O
# gabarito de cada caso traz a causa raiz do conjunto fechado, o campo afetado e listas de
# termos, então a pontuação é determinística e repetível.
#
# A métrica "formato_valido_conteudo_errado" existe por causa de um achado da literatura
# (The Constraint Tax, único trabalho no regime sub-3B): medir apenas "a resposta parseou?"
# deixa cego para a maior parte dos erros, porque saída perfeitamente formatada com
# conteúdo semanticamente errado chegou a 88,9% dos casos naquele estudo.
import json
import re
import unicodedata
from collections import defaultdict
from pathlib import Path

from taxonomia import CAUSAS_RAIZ

AQUI = Path(__file__).resolve().parent
SAIDA = AQUI / "resultados"
_PERMITIDAS: set[str] = set()  # preenchido apos _normalizar existir


def _normalizar(texto: str) -> str:
    """Minúsculas e sem acento, para os termos casarem independente de grafia."""
    sem_acento = unicodedata.normalize("NFKD", texto)
    return "".join(c for c in sem_acento if not unicodedata.combining(c)).lower()


_PERMITIDAS.update(_normalizar(c) for c in CAUSAS_RAIZ)


def extrair(resposta: str) -> dict:
    """Lê as três linhas finais pedidas no prompt. Tolerante: aceita a linha em
    qualquer posição e ignora marcação de negrito que alguns modelos acrescentam."""
    limpa = resposta.replace("*", "").replace("`", "")
    def _campo(nome):
        m = re.search(rf"{nome}\s*:\s*(.+)", limpa, re.IGNORECASE)
        return m.group(1).strip() if m else None
    return {
        "causa_raiz": (_campo("CAUSA_RAIZ") or "").strip().split()[0].lower() or None
        if _campo("CAUSA_RAIZ") else None,
        "campo": _campo("CAMPO"),
        "impacto": _campo("IMPACTO"),
    }


def avaliar_registro(r: dict) -> dict:
    gab = r["gabarito"]
    lido = extrair(r.get("resposta", ""))
    resp_norm = _normalizar(r.get("resposta", ""))

    # Comparação sem acento: o conjunto fechado é escrito sem acentuação, e alguns modelos
    # devolvem "coleção_no_lugar_de_objeto" em vez de "colecao_no_lugar_de_objeto". Exigir
    # a grafia exata mediria transcrição, não diagnóstico — o rótulo escolhido é o mesmo.
    formato_ok = lido["causa_raiz"] is not None
    causa_ok = formato_ok and _normalizar(lido["causa_raiz"]) == _normalizar(gab["causa_raiz"])
    # Responder fora do conjunto permitido é falha de seguir instrução, diferente de
    # escolher o rótulo errado dentro do conjunto — as duas contam separado.
    fora_do_conjunto = formato_ok and _normalizar(lido["causa_raiz"]) not in _PERMITIDAS

    campo_esperado = gab.get("campo_afetado")
    if campo_esperado is None:
        campo_ok = lido["campo"] is None or "nenhum" in _normalizar(lido["campo"] or "")
    else:
        campo_ok = bool(lido["campo"]) and _normalizar(campo_esperado) in _normalizar(lido["campo"])

    esperados = [t for t in gab.get("termos_esperados", []) if _normalizar(t) in resp_norm]
    proibidos = [t for t in gab.get("termos_proibidos", []) if _normalizar(t) in resp_norm]

    return {
        **{k: r[k] for k in ("modelo", "caso", "classe", "nivel", "estrategia", "segundos",
                             "tokens_saida", "somente_cpu")},
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


def agregar(avaliados: list[dict], *chaves: str) -> list[dict]:
    grupos = defaultdict(list)
    for a in avaliados:
        grupos[tuple(a[k] for k in chaves)].append(a)

    saida = []
    for chave, itens in sorted(grupos.items(), key=lambda x: [str(v) for v in x[0]]):
        n = len(itens)
        validos = [i for i in itens if i["segundos"] is not None]
        saida.append({
            **dict(zip(chaves, chave)),
            "n": n,
            "causa_correta_pct": round(100 * sum(i["causa_correta"] for i in itens) / n, 1),
            "campo_correto_pct": round(100 * sum(i["campo_correto"] for i in itens) / n, 1),
            "formato_valido_pct": round(100 * sum(i["formato_valido"] for i in itens) / n, 1),
            "formato_ok_conteudo_errado_pct":
                round(100 * sum(i["formato_valido_conteudo_errado"] for i in itens) / n, 1),
            "fora_do_conjunto_pct":
                round(100 * sum(i["fora_do_conjunto"] for i in itens) / n, 1),
            "diagnostico_errado_pct":
                round(100 * sum(i["sinal_de_diagnostico_errado"] for i in itens) / n, 1),
            "segundos_medio": round(sum(i["segundos"] for i in validos) / len(validos), 2)
                if validos else None,
            "tokens_saida_medio": round(sum(i["tokens_saida"] for i in validos) / len(validos))
                if validos else None,
        })
    return saida


def main() -> None:
    brutos = carregar()
    if not brutos:
        print(f"Nenhum resultado em {SAIDA}. Rode executar_bateria.py primeiro.")
        return

    avaliados = [avaliar_registro(r) for r in brutos]
    (AQUI / "avaliacao.json").write_text(
        json.dumps(avaliados, ensure_ascii=False, indent=2), encoding="utf-8")

    cortes = {
        "por_modelo": ("modelo",),
        "por_modelo_estrategia": ("modelo", "estrategia"),
        "por_modelo_classe": ("modelo", "classe"),
        "por_modelo_nivel": ("modelo", "nivel"),
        "por_estrategia": ("estrategia",),
    }
    resumo = {nome: agregar(avaliados, *ch) for nome, ch in cortes.items()}
    (AQUI / "resumo_metricas.json").write_text(
        json.dumps(resumo, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"{len(brutos)} inferências avaliadas\n")
    print(f"{'modelo':22} {'estrat':11} {'n':>4} {'causa%':>7} {'campo%':>7} "
          f"{'fmt-ok/errado%':>15} {'seg':>6}")
    for r in resumo["por_modelo_estrategia"]:
        print(f"{r['modelo']:22} {r['estrategia']:11} {r['n']:4} {r['causa_correta_pct']:7} "
              f"{r['campo_correto_pct']:7} {r['formato_ok_conteudo_errado_pct']:15} "
              f"{r['segundos_medio']:6}")

    # Guarda contra o modo de falha que ja ocorreu uma vez: resposta cortada no teto de
    # tokens nunca chega as linhas finais, e o caso pontua zero por truncamento, nao por erro
    # de raciocinio. Sem este aviso, o numero seria lido como incapacidade do modelo.
    # Duas situações diferentes, que antes eram contadas como uma só:
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
            chave = (b["modelo"], b["estrategia"])
            if "CAUSA_RAIZ" in b.get("resposta", ""):
                cortado_ok[chave] += 1
            else:
                cortado_sem_resposta[chave] += 1
    if cortado_sem_resposta:
        print("\n!! NAO CONCLUIRAM DENTRO DO ORCAMENTO DE TOKENS (casos invalidos):")
        for (m, e), n in sorted(cortado_sem_resposta.items()):
            print(f"   {m} / {e}: {n} respostas sem CAUSA_RAIZ — excluir ou refazer com teto maior")
    if cortado_ok:
        print("\n(i) Cortadas no teto mas COM resposta emitida (casos válidos):")
        for (m, e), n in sorted(cortado_ok.items()):
            print(f"   {m} / {e}: {n}")

    cpu = [a for a in avaliados if not a["somente_cpu"]]
    if cpu:
        print(f"\n!! {len(cpu)} inferências NÃO ficaram só em CPU — medição comprometida")


if __name__ == "__main__":
    main()
