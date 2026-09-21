# ! Alteração de IA - Revisar: script novo (21/09/2026) que integra a rodada 2 da pesquisa no Memorial: corrige a
# introdução e a tabela de contagens do levantamento (números reais da primeira execução), tira as duas linhas de
# depuração, substitui o parágrafo "O que ficou sem rodar", acrescenta §6.9.9–6.9.17 e os blocos novos de
# `referencias.md`, e grava `mapa-de-decisoes-fase-3.md` (§6.10) — tudo a partir de `r2-final.json`, idempotente.
# ! Motivo: a integração da rodada 1 foi feita à mão em 11/09 e deixou lixo de depuração e uma contagem errada
# ("166 verificações, 12 rejeitadas"); fazer a da rodada 2 por script (processamento local, sem tokens) garante o
# formato das oito subseções existentes e deixa o descarte registrado com motivo, como o Eric pediu.
"""Uso: python ferramentas/integrar_pesquisa.py [--entrada r2-final.json] [--data 21/09/2026] [--simular]"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import render_levantamento as rl  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")

RAIZ = rl.RAIZ
MAPA = RAIZ / "Documentacao" / "memorial" / "2-pesquisa-e-literatura" / "mapa-de-decisoes-fase-3.md"
TITULO_R2 = {
    "r2-conflito-contexto-conhecimento-e-sicofancia-documental": "conflito entre contexto recuperado e conhecimento paramétrico",
    "r2-validacao-de-artefatos-gerados-e-limites-da-autocorrecao": "validação em código de artefatos escritos por LLM",
    "r2-metricas-de-qualidade-de-documentacao-e-inconsistencia-doc-codigo": "qualidade de documentação técnica",
    "r2-recuperacao-em-corpus-pequeno-curado-e-crescente": "recuperação em corpus pequeno e crescente",
    "r2-aprendizado-sem-atualizacao-de-pesos-e-ancoragem-em-faceli": "aprender sem atualizar pesos e a ancoragem no livro-guia",
    "r2-prompting-em-estagios-e-cot-em-modelos-pequenos": "decomposição em estágios em modelos pequenos",
    "r2-taxonomia-rotulos-ouro-e-rca-com-llm": "taxonomia de causa raiz e rótulos-ouro",
    "r2-agente-autonomo-de-qa-autonomia-e-supervisao": "arquitetura de agentes autônomos de QA",
}


def _ler(p: Path) -> tuple[str, bool]:
    s = p.read_bytes().decode("utf-8")
    crlf = "\r\n" in s
    return s.replace("\r\n", "\n"), crlf


def _gravar(p: Path, s: str, crlf: bool) -> None:
    if crlf:
        s = s.replace("\n", "\r\n")
    p.write_bytes(s.encode("utf-8"))


def contagens(dados: dict, chaves: tuple[str, ...]) -> list[tuple[str, int, int, int]]:
    """(key, aprovadas, rejeitadas por veredito, além do teto)"""
    linhas = []
    for k in chaves:
        it = dados.get(k) or {}
        rej = it.get("rejeitadas") or []
        teto = sum(1 for r in rej if "além do teto" in (r.get("motivo") or ""))
        linhas.append((k, len(it.get("verified") or []), len(rej) - teto, teto))
    return linhas


def tabela_contagens(r1: list, r2: list) -> str:
    def linha(k, a, r, t):
        return f"| `{k}` | {a} | {r} | {t} |"
    partes = ["| Tópico | Aprovadas | Rejeitadas | Além do teto (não verificadas) |", "|---|---|---|---|"]
    partes += [linha(*x) for x in r1]
    partes.append(f"| **rodada 1** | **{sum(x[1] for x in r1)}** | **{sum(x[2] for x in r1)}** | **{sum(x[3] for x in r1)}** |")
    partes += [linha(*x) for x in r2]
    partes.append(f"| **rodada 2** | **{sum(x[1] for x in r2)}** | **{sum(x[2] for x in r2)}** | **{sum(x[3] for x in r2)}** |")
    partes.append(f"| **total** | **{sum(x[1] for x in r1 + r2)}** | **{sum(x[2] for x in r1 + r2)}** | **{sum(x[3] for x in r1 + r2)}** |")
    return "\n".join(partes)


def bloco_mapa(mapa: dict, data: str) -> str:
    def esc(s: str) -> str:
        return (s or "").replace("|", "\\|").replace("\n", " ")
    partes = [
        "<!-- ! Alteração de IA - Revisar: arquivo gerado por ferramentas/integrar_pesquisa.py a partir do mapa de decisões produzido pelo Workflow pesquisa-r2 (" + data + "); a coluna \"Resultado medido na Fase 3\" é preenchida na análise decisória (P2).",
        "     ! Motivo: a análise dos resultados da Fase 3 deve ser lida contra o que a literatura previa; este mapa liga cada achado verificado (número e fonte) ao critério de leitura que ele fundamenta, e fica separado do levantamento para ser citado pelo relatório da Fase 3 e pela análise decisória. -->",
        "",
        "# Mapa de decisões — o que a literatura previa para a Fase 3",
        "",
        f"Parte do [Memorial de Desenvolvimento](../../Memorial%20de%20Desenvolvimento.md). Gerado em {data} das 16 sínteses verificadas do [levantamento](levantamento-2026-09-11-fase-3.md) (§6.9.1–6.9.16). As referências completas estão em [referencias.md](referencias.md).",
        "",
        "### 6.10 Mapa de decisões",
        "",
        "#### 6.10.1 Achado → número → fonte → critério de leitura da Fase 3",
        "",
        "| # | Achado da literatura | Número | Fonte | Decisão ou critério de leitura | Resultado medido na Fase 3 |",
        "|---|---|---|---|---|---|",
    ]
    for i, l in enumerate(mapa.get("linhas") or [], start=1):
        partes.append(f"| {i} | {esc(l.get('achado'))} | {esc(l.get('numero'))} | {esc(l.get('fonte'))} | {esc(l.get('decisao_fase3'))} | *(P2)* |")
    partes += ["", "#### 6.10.2 Riscos apontados pela literatura para a decisão", "", "| Risco | Mitigação | Fonte |", "|---|---|---|"]
    for r in mapa.get("riscos") or []:
        partes.append(f"| {esc(r.get('risco'))} | {esc(r.get('mitigacao'))} | {esc(r.get('fonte'))} |")
    partes += ["", "#### 6.10.3 Métricas que a literatura sustenta para escolher o modelo", "", "| Métrica | Fonte |", "|---|---|"]
    for m in mapa.get("metricas") or []:
        partes.append(f"| {esc(m.get('metrica'))} | {esc(m.get('fonte'))} |")
    partes += ["", "#### 6.10.4 Capítulos do livro-guia (Faceli et al., 3. ed., 2025) por seção do Memorial", "", "| Capítulo | Seção do Memorial |", "|---|---|"]
    for c in mapa.get("capitulos_faceli") or []:
        partes.append(f"| {esc(c.get('capitulo'))} | {esc(c.get('secao_memorial'))} |")
    partes += ["", "#### 6.10.5 Leitura", "", (mapa.get("leitura_pt") or "").strip(), ""]
    return "\n".join(partes)


def integrar(entrada: Path, data: str, simular: bool) -> int:
    dados_json = json.loads(entrada.read_text(encoding="utf-8"))
    dados = {**dados_json["r1"], **dados_json["r2"]}
    faltando = [k for k in rl.ORDEM_R2 if not (dados.get(k) or {}).get("synthesis")]
    if faltando:
        print("sínteses ausentes — não integro:", faltando)
        return 2
    if not dados_json.get("mapa"):
        print("mapa de decisões ausente — não integro")
        return 2
    texto, crlf = _ler(rl.LEVANTAMENTO)
    if "#### 6.9.9 " in texto:
        print("a rodada 2 já está integrada (6.9.9 presente); nada a fazer")
        return 0

    c1, c2 = contagens(dados, rl.ORDEM_R1), contagens(dados, rl.ORDEM_R2)
    a1, r1, t1 = (sum(x[i] for x in c1) for i in (1, 2, 3))
    a2, r2, t2 = (sum(x[i] for x in c2) for i in (1, 2, 3))

    # 1) linhas de depuração
    texto = re.sub(r"\n+(TOTAL sinteses:.*|VERIFICACOES:.*)\n", "\n", texto)
    # 2) frase das contagens
    antiga = "Os números deste arquivo são, portanto, os que sobreviveram: **154 afirmações aprovadas e 12 rejeitadas**, em **166 verificações**."
    assert antiga in texto, "frase das contagens não encontrada"
    nova = (f"Os números deste arquivo são, portanto, os que sobreviveram. Rodada 1 (11/09/2026): **{a1} afirmações aprovadas, {r1} rejeitadas** "
            f"em **{a1 + r1} verificações**, mais **{t1} não verificadas** por exceder o teto de 20 afirmações por tópico. "
            f"Rodada 2 ({data}, §6.9.9–6.9.16): **{a2} aprovadas, {r2} rejeitadas** em **{a2 + r2} verificações**, mais **{t2} além do teto**.")
    texto = texto.replace(antiga, nova)
    # 3) tabela
    ini = texto.index("| Tópico | Aprovadas | Rejeitadas |")
    fim = texto.index("| **total** | **154** | **12** |") + len("| **total** | **154** | **12** |")
    tag_tabela = ("<!-- ! Alteração de IA - Revisar: tabela e frase das contagens refeitas em " + data + " por ferramentas/integrar_pesquisa.py, com os números reais da primeira execução do fluxo de pesquisa (a que está nas subseções) e a rodada 2.\n"
                  "     ! Motivo: a contagem de 11/09 (\"154 aprovadas e 12 rejeitadas em 166 verificações\", \"tokenizacao com 10 rejeições\") somava execuções repetidas do mesmo fluxo; conferido no diário em 21/09: tokenizacao teve 19 aprovadas e nenhuma rejeição, e três afirmações (arquitetura 2, metricas 1) nunca foram verificadas por passar do teto de 20 por tópico. -->\n")
    texto = texto[:ini] + tag_tabela + tabela_contagens(c1, c2) + texto[fim:]
    # 4) parágrafo sobre tokenizacao
    par_tok = re.search(r"\nO tópico `tokenizacao` concentra 10 das 12 rejeições:.*?\n", texto)
    assert par_tok, "parágrafo do tokenizacao não encontrado"
    rej_r1 = [k for k, a, r, t in c1 if r]
    teto_r1 = [f"`{k}` {t}" for k, a, r, t in c1 if t]
    novo_par = ("\nNa rodada 1 as rejeições foram em " + ", ".join(f"`{k}`" for k in rej_r1) +
                " (uma em cada); as afirmações não verificadas por excederem o teto ficaram em " + ", ".join(teto_r1) +
                ". As afirmações rejeitadas e as de suporte parcial, com o motivo de cada verificador, estão listadas em §6.9.17. A seção §6.7 usa só o que sobrou.\n")
    texto = texto[:par_tok.start()] + novo_par + texto[par_tok.end():]
    # 5) parágrafo "O que ficou sem rodar"
    par_sem = re.search(r"\n\*\*O que ficou sem rodar\.\*\*.*?\n", texto)
    assert par_sem, "parágrafo 'O que ficou sem rodar' não encontrado"
    temas = "; ".join(TITULO_R2[k] for k in rl.ORDEM_R2)
    novo_sem = (f"\n**Rodada 2 ({data}).** As lacunas apontadas ao fim de cada tópico foram consolidadas por um crítico de completude em oito temas — {temas} — e cada tema passou pelo mesmo fluxo (pesquisa, verificação cética de cada afirmação, síntese só com o que sobreviveu): subseções §6.9.9 a §6.9.16. As afirmações rejeitadas e as parciais das duas rodadas estão em §6.9.17, e o [mapa de decisões](mapa-de-decisoes-fase-3.md) (§6.10) liga os achados verificados aos critérios de leitura dos resultados da Fase 3.\n")
    texto = texto[:par_sem.start()] + novo_sem + texto[par_sem.end():]
    # 6) cabeçalhos da rodada 1 com as contagens reais
    for i, (k, a, r, t) in enumerate(c1, start=1):
        pad = re.compile(r"^#### 6\.9\.%d (.*?) \(`%s` — \d+ aprovadas?, \d+ rejeitadas?\)$" % (i, re.escape(k)), re.M)
        m = pad.search(texto)
        assert m, f"cabeçalho 6.9.{i} não encontrado"
        texto = texto[:m.start()] + f"#### 6.9.{i} {m.group(1)} (`{k}` — {a} {'aprovada' if a == 1 else 'aprovadas'}, {r + t} {'rejeitada' if r + t == 1 else 'rejeitadas'})" + texto[m.end():]
    # 7) subseções novas ao fim
    secoes = [rl.secao(9 + i, k, dados[k]) for i, k in enumerate(rl.ORDEM_R2)]
    rejeitadas = rl.bloco_rejeitadas(9 + len(rl.ORDEM_R2), dados)
    tag_fim = ("\n<!-- ! Alteração de IA - Revisar: subseções §6.9.9–6.9.17 acrescentadas em " + data + " por ferramentas/integrar_pesquisa.py a partir de r2-final.json (rodada 2 da pesquisa: Workflow pesquisa-r2, verificadores em Sonnet, sínteses no modelo da sessão), sem reescrita; só os títulos internos de cada síntese foram rebaixados a negrito, como na rodada 1.\n"
               "     ! Motivo: fecha a pendência 13 (rodada complementar) e registra o que foi descartado com o motivo; o texto das sínteses é o que os agentes produziram, para não introduzir número sem origem. -->\n\n")
    texto = texto.rstrip("\n") + "\n" + tag_fim + "\n".join(secoes) + "\n" + rejeitadas + "\n"
    # referencias.md
    refs_texto, refs_crlf = _ler(rl.REFERENCIAS)
    bloco, quase = rl.bloco_referencias(dados, rl.ORDEM_R2, f"levantamento de {data}")
    n_novas = bloco.count("\n- ")
    m_total = re.search(r"o levantamento produziu as \*\*(\d+)\*\* referências abaixo", refs_texto)
    assert m_total, "frase do total de referências não encontrada"
    total_novo = int(m_total.group(1)) + n_novas
    refs_novo = refs_texto[:m_total.start(1)] + str(total_novo) + refs_texto[m_total.end(1):]
    refs_novo = refs_novo.replace("o levantamento produziu as **", "os levantamentos de 11/09 e de " + data + " produziram as **", 1) if "os levantamentos de" not in refs_novo else refs_novo
    refs_novo = refs_novo.rstrip("\n") + "\n\n" + bloco
    # mapa
    mapa_texto = bloco_mapa(dados_json["mapa"], data)

    print(f"levantamento: +{len(secoes)} subseções, rejeitadas §6.9.17; contagens r1 {a1}/{r1}/{t1}, r2 {a2}/{r2}/{t2}")
    print(f"referencias.md: {n_novas} referências novas (total {total_novo}); quase-duplicatas a conferir: {len(quase)}")
    for q in quase:
        print("   ", q)
    print(f"mapa: {len(dados_json['mapa'].get('linhas') or [])} linhas, {len(dados_json['mapa'].get('riscos') or [])} riscos")
    if simular:
        print("(simulação: nada gravado)")
        return 0
    _gravar(rl.LEVANTAMENTO, texto, crlf)
    _gravar(rl.REFERENCIAS, refs_novo, refs_crlf)
    MAPA.write_text(mapa_texto, encoding="utf-8", newline="\n")
    print("gravado.")
    return 0


def rerender(entrada: Path, data: str) -> int:
    """Regera no lugar as subseções já integradas (§6.9.1–6.9.17) e o bloco de referências da rodada 2,
    depois de uma correção no renderizador — sem tocar em introdução, tabela ou tags."""
    dados_json = json.loads(entrada.read_text(encoding="utf-8"))
    dados = {**dados_json["r1"], **dados_json["r2"]}
    texto, crlf = _ler(rl.LEVANTAMENTO)
    if "#### 6.9.9 " not in texto:
        print("rodada 2 ainda não integrada; use o modo normal")
        return 2
    ordem = list(rl.ORDEM_R1) + list(rl.ORDEM_R2)
    for i, k in enumerate(ordem, start=1):
        m = re.search(r"(?ms)^#### 6\.9\.%d .*?(?=^#### 6\.9\.\d+ |\Z)" % i, texto)
        assert m, f"subseção 6.9.{i} não encontrada"
        # o comentário de IA que antecede a 6.9.9 fica dentro da 6.9.8 no corte por cabeçalho: preservá-lo
        atual = m.group(0)
        cauda = ""
        tag = re.search(r"(?s)\n<!--.*?-->\n*\Z", atual)
        if tag:
            cauda = tag.group(0)
        texto = texto[:m.start()] + rl.secao(i, k, dados[k]).rstrip("\n") + "\n\n" + cauda.lstrip("\n") + texto[m.end():]
    m = re.search(r"(?ms)^#### 6\.9\.%d .*\Z" % (len(ordem) + 1), texto)
    assert m, "bloco de rejeitadas não encontrado"
    texto = texto[:m.start()] + rl.bloco_rejeitadas(len(ordem) + 1, dados) + "\n"
    _gravar(rl.LEVANTAMENTO, texto, crlf)
    # referências: refaz o bloco da rodada 2 com o dedup atual e recalcula o total
    refs_texto, refs_crlf = _ler(rl.REFERENCIAS)
    marca = "\n### Rodada 2 do levantamento"
    if marca in refs_texto:
        refs_texto = refs_texto[:refs_texto.index(marca)].rstrip("\n") + "\n"
    base = sum(1 for l in refs_texto.splitlines() if l.startswith("- "))
    rl.REFERENCIAS.write_bytes((refs_texto.replace("\n", "\r\n") if refs_crlf else refs_texto).encode("utf-8"))
    bloco, quase = rl.bloco_referencias(dados, rl.ORDEM_R2, f"levantamento de {data}")
    n_novas = bloco.count("\n- ")
    m_total = re.search(r"produziram as \*\*(\d+)\*\* referências abaixo", refs_texto)
    assert m_total, "frase do total não encontrada"
    refs_texto = refs_texto[:m_total.start(1)] + str(base + n_novas) + refs_texto[m_total.end(1):]
    _gravar(rl.REFERENCIAS, refs_texto.rstrip("\n") + "\n\n" + bloco, refs_crlf)
    print(f"regeradas {len(ordem)} subseções + rejeitadas; referências: {base} anteriores + {n_novas} novas = {base + n_novas}; quase-duplicatas: {len(quase)}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--entrada", default=str(rl.SDD / "pesquisa" / "r2-final.json"))
    ap.add_argument("--data", default="21/09/2026")
    ap.add_argument("--simular", action="store_true")
    ap.add_argument("--rerender", action="store_true", help="regera as subseções e o bloco de referências já integrados")
    args = ap.parse_args()
    if args.rerender:
        return rerender(Path(args.entrada), args.data)
    return integrar(Path(args.entrada), args.data, args.simular)


if __name__ == "__main__":
    raise SystemExit(main())
