# ! Alteração de IA - Revisar: gerador das tabelas do relatório da Fase 3 (Memorial,
# `fase-3-relatorio-por-modelo.md`) a partir dos registros oficiais em resultados_alvo/fase3/
# (resumo_fase3.json, decisao_modelo.json e as marcas de tempo de fase3.log); grava o documento
# DERIVADO `resultados_alvo/fase3/tabelas_relatorio.md` e, com --check, confere que cada bloco
# `<!-- tabela:NOME -->…<!-- /tabela:NOME -->` colado no Memorial é byte a byte o bloco regerado.
# ! Motivo: a regra do projeto é "nenhum número digitado à mão em Markdown" (decisão 36 e
# .claude/rules/documentacao.md); o relatório tem oito tabelas com centenas de células que, coladas
# à mão em 22/09/2026, ficariam sem conferência mecânica. Com o bloco marcado no Markdown, o
# --check acusa qualquer célula que divirja de resumo_fase3.json — o mesmo desenho de
# comparar_fases.py e decidir_modelo.py. Este script só LÊ os registros oficiais e nunca os regrava.
"""Tabelas do relatório da Fase 3, saídas de resumo_fase3.json (22/09/2026).

Uso:
    python gerar_tabelas_relatorio_fase3.py --saida fase3            # grava tabelas_relatorio.md
    python gerar_tabelas_relatorio_fase3.py --saida fase3 --check    # confere o derivado e o Memorial
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import caminhos  # noqa: E402
import taxonomia  # noqa: E402

RAIZ_REPO = Path(__file__).resolve().parents[3]
MEMORIAL = [
    RAIZ_REPO / "Documentacao/memorial/3-resultados-e-analises/fase-3-relatorio-por-modelo.md",
    RAIZ_REPO / "Documentacao/memorial/3-resultados-e-analises/comparacao-entre-fases.md",
    RAIZ_REPO / "Documentacao/memorial/3-resultados-e-analises/analise-decisoria-modelo-final.md",
]
MODELOS = ["granite4.2:8b", "qwen2.5-coder:7b", "qwen2.5:7b", "qwen2.5-coder:3b"]
EPOCAS = [0, 1, 2, 3]
TRANSICOES = ["L0→L1", "L1→L2", "L2→L3"]


def _n(v) -> str:
    """Vírgula decimal, 1 casa, '—' para None (mesma regra de comparar_fases._n)."""
    if v is None:
        return "—"
    if isinstance(v, int):
        return str(v)
    return f"{v:.1f}".replace(".", ",")


def _pct(v) -> str:
    return "—" if v is None else f"{_n(v)}%"


def _p(v) -> str:
    if v is None:
        return "—"
    return f"{v:.4f}".replace(".", ",") + ("*" if v < 0.05 else "")


def _linha(celulas) -> str:
    return "| " + " | ".join(celulas) + " |"


def _tabela(cabecalho: list[str], linhas: list[list[str]]) -> list[str]:
    return [_linha(cabecalho), _linha(["---"] * len(cabecalho))] + [_linha(l) for l in linhas]


def _indice(resumo: dict, chave: str, *campos: str) -> dict[tuple, dict]:
    return {tuple(l[c] for c in campos): l for l in resumo[chave]}


# --------------------------------------------------------------------------------- tabelas

def curva_acerto(resumo: dict) -> list[str]:
    """§3: acerto de causa raiz por modelo × L, nos 36 e nos 54 (`causa_correta_pct`)."""
    idx = _indice(resumo, "por_modelo_biblioteca_particao", "modelo", "biblioteca_epoca", "particao")
    cab = ["Modelo"] + [f"L{e} (36)" for e in EPOCAS] + [f"L{e} (54)" for e in EPOCAS]
    linhas = []
    for m in MODELOS:
        cel = [f"`{m}`"]
        for part in ("avaliacao", "aprendizado"):
            for e in EPOCAS:
                cel.append(_pct(idx[(m, e, part)]["causa_correta_pct"]))
        linhas.append(cel)
    return _tabela(cab, linhas)


def curva_balanceada(resumo: dict) -> list[str]:
    """§3: acurácia balanceada por modelo × L, nos 36, 54 e 90 (`acuracia_balanceada_pct`)."""
    idx = _indice(resumo, "por_modelo_biblioteca_particao", "modelo", "biblioteca_epoca", "particao")
    cab = ["Modelo"] + [f"L{e} (36)" for e in EPOCAS] + [f"L{e} (54)" for e in EPOCAS] + \
          [f"L{e} (90)" for e in EPOCAS]
    linhas = []
    for m in MODELOS:
        cel = [f"`{m}`"]
        for part in ("avaliacao", "aprendizado", "todos"):
            for e in EPOCAS:
                cel.append(_pct(idx[(m, e, part)]["acuracia_balanceada_pct"]))
        linhas.append(cel)
    return _tabela(cab, linhas)


def qualidade(resumo: dict) -> list[str]:
    """§3: forma da resposta nos 36, por modelo × L."""
    idx = _indice(resumo, "por_modelo_biblioteca_particao", "modelo", "biblioteca_epoca", "particao")
    cab = ["Modelo", "L", "Rótulo mais frequente (parcela)", "Rótulos distintos",
           "Formato ok / conteúdo errado", "Fora do conjunto", "Citou verbete",
           "Ouro no contexto", "Contexto com nota", "Verbete novo no contexto"]
    linhas = []
    for m in MODELOS:
        for e in EPOCAS:
            l = idx[(m, e, "avaliacao")]
            linhas.append([f"`{m}`", f"L{e}",
                           f"`{l['rotulo_mais_frequente']}` ({_pct(l['parcela_rotulo_mais_frequente_pct'])})",
                           str(l["n_rotulos_distintos"]), _pct(l["formato_ok_conteudo_errado_pct"]),
                           _pct(l["fora_do_conjunto_pct"]), _pct(l["citou_verbete_pct"]),
                           _pct(l["ouro_no_contexto_pct"]), _pct(l["contexto_com_nota_pct"]),
                           _pct(l["verbete_novo_no_contexto_pct"])])
    return _tabela(cab, linhas)


def por_classe(resumo: dict) -> list[str]:
    """§3: acerto por classe de defeito (nos 90; o resumo não desmembra classe por partição), L0..L3."""
    idx = _indice(resumo, "por_modelo_biblioteca_classe", "modelo", "biblioteca_epoca", "particao", "classe")
    cab = ["Modelo", "Classe (n)"] + [f"L{e}" for e in EPOCAS]
    linhas = []
    for m in MODELOS:
        for c in sorted(taxonomia.CLASSES):
            l0 = idx[(m, 0, "todos", c)]
            cel = [f"`{m}`", f"{c} {taxonomia.CLASSES[c]['id']} ({l0['n']})"]
            for e in EPOCAS:
                cel.append(_pct(idx[(m, e, "todos", c)]["causa_correta_pct"]))
            linhas.append(cel)
    return _tabela(cab, linhas)


def por_nivel(resumo: dict) -> list[str]:
    """§3: acerto por nível de dificuldade (nos 90), L0..L3."""
    idx = _indice(resumo, "por_modelo_biblioteca_nivel", "modelo", "biblioteca_epoca", "particao", "nivel")
    cab = ["Modelo", "Nível (n)"] + [f"L{e}" for e in EPOCAS]
    linhas = []
    for m in MODELOS:
        for nv in sorted(taxonomia.NIVEIS):
            l0 = idx[(m, 0, "todos", nv)]
            cel = [f"`{m}`", f"{nv} {taxonomia.NIVEIS[nv]['id']} ({l0['n']})"]
            for e in EPOCAS:
                cel.append(_pct(idx[(m, e, "todos", nv)]["causa_correta_pct"]))
            linhas.append(cel)
    return _tabela(cab, linhas)


def pareado(resumo: dict) -> list[str]:
    """§4: cada L contra L0 (McNemar exato, Holm por célula, g de Cohen) e Q de Cochran."""
    idx = _indice(resumo, "pareado_vs_L0", "modelo", "biblioteca_epoca", "particao")
    coq = _indice(resumo, "cochran_q", "modelo", "particao")
    cab = ["Modelo", "Partição (n)", "L1 vs L0", "L2 vs L0", "L3 vs L0", "Q de Cochran (L0..L3)"]
    linhas = []
    for m in MODELOS:
        for part, n in (("avaliacao", 36), ("aprendizado", 54), ("todos", 90)):
            cel = [f"`{m}`", f"{part} ({n})"]
            for e in (1, 2, 3):
                l = idx[(m, e, part)]
                cel.append(f"{_pct(l['acerto_L0_pct'])}→{_pct(l['acerto_pct'])} "
                           f"(Δ {_n(l['delta_pp'])} pp; b/c {l['b']}/{l['c']}; p {_p(l['p_mcnemar'])}; "
                           f"Holm {_p(l['p_holm'])}; g {_n(l['g_cohen'])})")
            q = coq[(m, part)]
            cel.append(f"Q {_n(q['q'])}, gl {q['gl']}, p {_p(q['p'])}")
            linhas.append(cel)
    return _tabela(cab, linhas)


def flips(resumo: dict) -> list[str]:
    """§4: flips entre versões consecutivas (✓→✗ = autoenvenenamento da H5; ✗→✓ = ganho)."""
    idx = _indice(resumo, "flips", "modelo", "transicao", "particao")
    cab = ["Modelo", "Partição (n)"] + [f"{t}: ✓→✗ / ✗→✓ (autoenv.)" for t in TRANSICOES]
    linhas = []
    for m in MODELOS:
        for part, n in (("avaliacao", 36), ("aprendizado", 54)):
            cel = [f"`{m}`", f"{part} ({n})"]
            for t in TRANSICOES:
                l = idx[(m, t, part)]
                cel.append(f"{l['certo_para_errado']} / {l['errado_para_certo']} "
                           f"({_pct(l['autoenvenenamento_pct'])})")
            linhas.append(cel)
    return _tabela(cab, linhas)


def mde(resumo: dict) -> list[str]:
    """§4: menor diferença que o McNemar exato aponta (d = round(0,2·n) discordantes)."""
    cab = ["n", "Pares discordantes supostos", "b mínimo (p < 0,05)", "Δ mínimo (pp)"]
    linhas = [[str(l["n"]), str(l["discordantes"]), str(l["b_min"]), _n(l["delta_pp"])]
              for l in resumo["efeito_minimo_detectavel"]]
    return _tabela(cab, linhas)


def recuperacao(resumo: dict) -> list[str]:
    """§5: hit@k e MRR por biblioteca (modelo × L), nos 90 e nos 36."""
    idx = _indice(resumo, "recuperacao", "modelo", "biblioteca_epoca")
    cab = ["Modelo", "L", "Verbetes (novos)", "Tokens est.", "hit@1 / hit@3 / hit@5 / MRR (90)",
           "hit@1 / hit@3 / hit@5 / MRR (36)", "Ouro deslocado por novo", "Ouro recuperável após edição"]
    linhas = []
    for m in MODELOS:
        for e in EPOCAS:
            l = idx[(m, e)]
            t, a = l["todos"], l["avaliacao"]
            rec = l["ouro_recuperavel_apos_edicao"]
            linhas.append([f"`{m}`", f"L{e}", f"{l['n_verbetes']} ({l['n_verbetes_novos']})",
                           str(l["tokens_estimados"]),
                           f"{_n(t['hit@1'])} / {_n(t['hit@3'])} / {_n(t['hit@5'])} / {t['mrr']:.3f}".replace(".", ","),
                           f"{_n(a['hit@1'])} / {_n(a['hit@3'])} / {_n(a['hit@5'])} / {a['mrr']:.3f}".replace(".", ","),
                           str(l["ouro_deslocado_por_novo"]), "—" if rec is None else str(rec)])
    return _tabela(cab, linhas)


def documentacao(resumo: dict) -> list[str]:
    """§6: o que cada modelo escreveu por época e o tamanho da biblioteca ao fechar."""
    cab = ["Modelo", "Época", "Propostas", "Aceitas", "%", "Notas", "Retificações", "Verbetes novos",
           "NENHUMA", "Sem FIM", "Cortadas no teto", "Tokens acrescentados (est.)",
           "Biblioteca ao fechar (verbetes / tokens est.)", "Aceitas quando errou / quando acertou"]
    linhas = []
    for l in resumo["documentacao"]:
        po = l["por_operacao"]
        linhas.append([f"`{l['modelo']}`", f"E{l['epoca']}", str(l["n_propostas"]), str(l["n_aceitas"]),
                       _pct(l["aceitas_pct"]), str(po["nota"]["aceitas"]), str(po["retificacao"]["aceitas"]),
                       str(po["novo_verbete"]["aceitas"]), str(l["n_nenhuma"]), str(l["n_fim_ausente"]),
                       str(l["n_respostas_truncadas"]), str(l["tokens_md_estimados_acrescentados"]),
                       f"{l['biblioteca']['n_verbetes']} / {l['biblioteca']['tokens_estimados']}",
                       f"{l['quando_errou']['aceitas']} de {l['quando_errou']['propostas']} / "
                       f"{l['quando_acertou']['aceitas']} de {l['quando_acertou']['propostas']}"])
    return _tabela(cab, linhas)


def rejeicoes(resumo: dict) -> list[str]:
    """§6: histograma dos códigos de rejeição por modelo, somado nas 3 épocas (só códigos com ocorrência)."""
    soma: dict[str, dict[str, int]] = {m: {} for m in MODELOS}
    for l in resumo["documentacao"]:
        for cod, n in l["motivos_rejeicao"].items():
            soma[l["modelo"]][cod] = soma[l["modelo"]].get(cod, 0) + n
    # desempate pelo nome: sem ele a ordem dos códigos com o mesmo total mudava entre execuções
    # (iteração de conjunto) e o --check acusava divergência falsa (visto em 22/09/2026)
    codigos = sorted({c for m in MODELOS for c, n in soma[m].items() if n},
                     key=lambda c: (-sum(soma[m].get(c, 0) for m in MODELOS), c))
    cab = ["Código de rejeição"] + [f"`{m}`" for m in MODELOS] + ["Total"]
    linhas = [[f"`{c}`"] + [str(soma[m].get(c, 0)) for m in MODELOS]
              + [str(sum(soma[m].get(c, 0) for m in MODELOS))] for c in codigos]
    totais = [sum(soma[m].values()) for m in MODELOS]
    linhas.append(["**Total de rejeições**"] + [str(t) for t in totais] + [str(sum(totais))])
    return _tabela(cab, linhas)


def _horas_por_modelo(c3: dict) -> dict[str, str]:
    """Horas de cada modelo pelas marcas `== <modelo>: 3 epoca(s)…  dd/mm HH:MM:SS ==` do fase3.log;
    o último modelo termina na marca `== avaliacao`."""
    log = c3["raiz"] / "fase3.log"
    if not log.exists():
        return {}
    marcas: list[tuple[str, datetime]] = []
    padrao = re.compile(r"^== (.+?): 3 epoca\(s\).*?(\d\d)/(\d\d) (\d\d:\d\d:\d\d) ==")
    fim = re.compile(r"^== avaliacao\s+(\d\d)/(\d\d) (\d\d:\d\d:\d\d) ==")
    ano = datetime.now().year
    for linha in log.read_text(encoding="utf-8", errors="replace").splitlines():
        m = padrao.match(linha)
        if m:
            marcas.append((m.group(1), datetime.strptime(f"{ano}-{m.group(3)}-{m.group(2)} {m.group(4)}",
                                                         "%Y-%m-%d %H:%M:%S")))
            continue
        f = fim.match(linha)
        if f and marcas:
            marcas.append(("__fim__", datetime.strptime(f"{ano}-{f.group(2)}-{f.group(1)} {f.group(3)}",
                                                        "%Y-%m-%d %H:%M:%S")))
    horas = {}
    for (modelo, inicio), (_, proximo) in zip(marcas, marcas[1:]):
        if modelo == "__fim__":
            continue
        total = (proximo - inicio).total_seconds() / 3600
        horas[modelo] = f"{int(total):02d}h{int(round((total - int(total)) * 60)):02d}"
    return horas


def custo(resumo: dict, c3: dict) -> list[str]:
    """§9: custo por inferência na máquina-alvo — diagnóstico por L (nos 90) e proposta por época."""
    idx = _indice(resumo, "por_modelo_biblioteca_particao", "modelo", "biblioteca_epoca", "particao")
    doc = _indice(resumo, "documentacao", "modelo", "epoca")
    horas = _horas_por_modelo(c3)
    # linhas separadas para diagnóstico (por L lida) e proposta (por época): o diagnóstico da
    # época e lê L(e-1), então o prefill ms/token do diagnóstico da época e vai na linha de L(e-1)
    cab = ["Modelo", "Inferência", "Mediana s (p95)", "Prefill / geração (mediana, s)",
           "Tokens de saída (média)", "Prefill ms/token", "Horas do modelo (log)"]
    linhas = []
    for m in MODELOS:
        for e in EPOCAS:
            l = idx[(m, e, "todos")]
            d = doc.get((m, e + 1))
            linhas.append([f"`{m}`", f"diagnóstico com L{e}" + (" (passada final)" if e == 3 else f" (época {e + 1})"),
                           f"{_n(l['segundos_mediana'])} ({_n(l['segundos_p95'])})",
                           f"{_n(l['prefill_ms_mediana'] / 1000)} / {_n(l['geracao_ms_mediana'] / 1000)}",
                           str(l["tokens_saida_medio"]),
                           _n(d["prefill_ms_por_token_diagnostico"]) if d else "—",
                           horas.get(m, "—") if e == 0 else ""])
        for e in (1, 2, 3):
            d = doc[(m, e)]
            linhas.append([f"`{m}`", f"proposta na época {e}", _n(d["segundos_mediana_proposta"]), "—",
                           str(d["tokens_saida_medio_proposta"]), _n(d["prefill_ms_por_token_proposta"]), ""])
    return _tabela(cab, linhas)


def revisao(decisao: dict) -> list[str]:
    """§7: revisão humana das edições, como decidir_modelo.py a apurou (planilhas revisao_edicoes__*.md)."""
    rev = decisao["revisao_humana"]
    if rev["status"] == "sem_avaliacao":
        return [rev["frase"]]
    cab = ["Modelo", "n", "Correta", "Parcial", "Errada", "Sem avaliação"]
    linhas = [[f"`{m}`", str(p["n"]), _pct(p["Correta"]), _pct(p["Parcial"]), _pct(p["Errada"]),
               _pct(p["sem_avaliacao"])] for m, p in sorted(rev["por_modelo"].items())]
    return _tabela(cab, linhas) + ["", f"_Fonte: {rev['fonte']}._"]


SECOES_COMPARACAO = {
    "### Acerto por modelo e fase (90 casos)": "cf_acerto_90",
    "### Acurácia balanceada por modelo e fase (90 casos)": "cf_balanceada_90",
    "### Acerto por modelo e fase (36 casos de avaliação)": "cf_acerto_36",
    "### Acurácia balanceada por modelo e fase (36 casos de avaliação)": "cf_balanceada_36",
    "### Custo e prolixidade": "cf_custo",
    "### Modos de falha e riscos": "cf_riscos",
    "### Pareamentos": "cf_pareamentos",
    "## Leitura por fase": "cf_leitura",
}


SECOES_DECISAO = {
    "## 1. Regra da decisão 36": "dm_regra_36",
    "## 2. Bootstrap por caso": "dm_bootstrap",
    "## 3. Estabilidade do ranking": "dm_estabilidade",
    "## 4. Fronteira de Pareto": "dm_pareto",
    "## 5. Escore ponderado e sensibilidade": "dm_escore",
    "## 6. Fase 3-B": "dm_3b",
    "## 7. Revisão humana": "dm_revisao",
    "## Frase da decisão": "dm_frase",
}


def _secoes(arquivo: Path, mapa: dict[str, str], fronteiras: tuple[str, ...]) -> dict[str, list[str]]:
    """Corta `arquivo` nas linhas que começam por uma das `fronteiras` e devolve, pelo nome do
    `mapa` (casado por prefixo do cabeçalho), as linhas de cada seção; cabeçalhos de nível
    inferior às fronteiras ficam como conteúdo."""
    if not arquivo.exists():
        return {}
    blocos: dict[str, list[str]] = {}
    atual = None
    for linha in arquivo.read_text(encoding="utf-8").splitlines():
        if linha.startswith(fronteiras):
            atual = next((nome for cab, nome in mapa.items() if linha.strip().startswith(cab)), None)
            if atual:
                blocos[atual] = []
            continue
        if atual:
            blocos[atual].append(linha)
    for nome, linhas in blocos.items():
        while linhas and not linhas[0].strip():
            linhas.pop(0)
        while linhas and not linhas[-1].strip():
            linhas.pop()
    return blocos


def blocos_comparacao(c3: dict) -> dict[str, list[str]]:
    """Seções de comparacao_fases.md (gerado por comparar_fases.py) como blocos `cf_*` e de
    decisao_modelo.md (decidir_modelo.py) como blocos `dm_*`, para a comparação entre fases e a
    análise decisória do Memorial colarem as tabelas com a mesma conferência."""
    return {**_secoes(c3["raiz"] / "comparacao_fases.md", SECOES_COMPARACAO, ("## ", "### ")),
            **_secoes(c3["raiz"] / "decisao_modelo.md", SECOES_DECISAO, ("## ",))}


def gerar(resumo: dict, decisao: dict, c3: dict) -> dict[str, list[str]]:
    return {**blocos_comparacao(c3),
        "curva_acerto": curva_acerto(resumo),
        "curva_balanceada": curva_balanceada(resumo),
        "qualidade": qualidade(resumo),
        "por_classe": por_classe(resumo),
        "por_nivel": por_nivel(resumo),
        "pareado": pareado(resumo),
        "flips": flips(resumo),
        "mde": mde(resumo),
        "recuperacao": recuperacao(resumo),
        "documentacao": documentacao(resumo),
        "rejeicoes": rejeicoes(resumo),
        "custo": custo(resumo, c3),
        "revisao": revisao(decisao),
    }


# ------------------------------------------------------------------------ gravar / conferir

def bloco(nome: str, linhas: list[str]) -> str:
    return f"<!-- tabela:{nome} -->\n" + "\n".join(linhas) + f"\n<!-- /tabela:{nome} -->"


def render(tabelas: dict[str, list[str]], fontes: dict[str, str]) -> str:
    cab = ["<!-- ! Alteração de IA - Revisar: gerado por gerar_tabelas_relatorio_fase3.py a partir de "
           "resumo_fase3.json, decisao_modelo.json e fase3.log -- NÃO editar à mão.",
           "     ! Motivo: são as tabelas coladas no relatório da Fase 3 do Memorial; o --check confere "
           "que cada bloco colado é idêntico ao regerado, para nenhum número entrar digitado. -->", "",
           "# Tabelas do relatório da Fase 3", "",
           "Fontes: " + "; ".join(f"`{k}` = `{v}`" for k, v in fontes.items()) + ".", ""]
    corpo = []
    for nome, linhas in tabelas.items():
        corpo += [f"## {nome}", "", bloco(nome, linhas), ""]
    return "\n".join(cab + corpo)


BLOCO_RE = re.compile(r"<!-- tabela:([a-z0-9_]+) -->\n(.*?)\n<!-- /tabela:\1 -->", re.S)


def conferir(caminho: Path, tabelas: dict[str, list[str]]) -> int:
    """Compara os blocos marcados de `caminho` com os regerados; devolve o número de divergências."""
    if not caminho.exists():
        print(f"--check: {caminho.name} não existe (ignorado)")
        return 0
    texto = caminho.read_text(encoding="utf-8")
    divergencias = 0
    achados = BLOCO_RE.findall(texto)
    for nome, corpo in achados:
        esperado = "\n".join(tabelas.get(nome, []))
        if nome not in tabelas:
            print(f"--check: {caminho.name}: bloco `{nome}` desconhecido")
            divergencias += 1
        elif corpo != esperado:
            print(f"--check: {caminho.name}: bloco `{nome}` DIFERE do regerado")
            divergencias += 1
    print(f"--check: {caminho.name}: {len(achados)} bloco(s) conferido(s), {divergencias} divergente(s)")
    return divergencias


def main() -> None:
    ap = argparse.ArgumentParser(description="Tabelas do relatório da Fase 3 (Memorial) a partir dos "
                                             "registros oficiais; --check confere o derivado e o Memorial.")
    ap.add_argument("--saida", default="fase3")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    print(caminhos.descricao())
    c3 = caminhos.fase3(args.saida)
    resumo = json.loads(c3["resumo"].read_text(encoding="utf-8"))
    decisao_path = c3["raiz"] / "decisao_modelo.json"
    decisao = json.loads(decisao_path.read_text(encoding="utf-8")) if decisao_path.exists() else \
        {"revisao_humana": {"status": "sem_avaliacao", "frase": "decisao_modelo.json ausente"}}
    tabelas = gerar(resumo, decisao, c3)
    destino = c3["raiz"] / "tabelas_relatorio.md"
    texto = render(tabelas, {"resumo": c3["resumo"].name, "decisao": decisao_path.name, "log": "fase3.log"})
    if args.check:
        divergencias = 0
        if destino.exists() and destino.read_text(encoding="utf-8") != texto:
            print(f"--check: {destino.name} DIFERE do regerado")
            divergencias += 1
        for md in MEMORIAL:
            divergencias += conferir(md, tabelas)
        print("--check: tudo ok" if not divergencias else f"--check: {divergencias} divergência(s)")
        raise SystemExit(1 if divergencias else 0)
    destino.write_text(texto, encoding="utf-8")
    print(f"{len(tabelas)} tabelas em {destino}")


if __name__ == "__main__":
    main()
