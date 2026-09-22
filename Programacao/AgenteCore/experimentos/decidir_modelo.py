#!/usr/bin/env python3
# ! Alteração de IA - Revisar: cria decidir_modelo.py (Tarefa P2.1) -- decide modelo e estado
# da biblioteca (L0..L3) de produção a partir dos resultados oficiais da Fase 3: a regra
# pré-registrada de acurácia balanceada nos 36 casos de avaliação com veto por
# autoenvenenamento (passo 1), bootstrap por caso para o IC 95%/P(top-1) (passo 2),
# estabilidade do ranking por coluna e por classe de defeito (passo 3), fronteira de Pareto
# (passo 4), escore ponderado com varredura de sensibilidade (passo 5), comparação pareada
# contra a Fase 3-B quando houver (passo 6) e o resumo da revisão humana (passo 7); grava
# decisao_modelo.json e decisao_modelo.md.
# ! Motivo: brief-p2-decidir-modelo.md pede a decisão em duas camadas -- primeiro a regra
# fixada ANTES de olhar robustez (evita escolher, entre vários critérios possíveis, o que dá o
# resultado que já se queria), depois bootstrap/Pareto/escore/sensibilidade para mostrar se a
# regra 36 escolheu um vencedor sólido ou um empate técnico que outro corte dos mesmos dados
# desfaria. Nenhum número entra no .md à mão (constraints.md): tudo sai de
# comparacao_fases.json, resumo_fase3.json e avaliacao_fase3.json, já fechados pela Fase 3.
"""Decide o modelo e o estado da biblioteca (L0..L3) de produção a partir dos resultados
oficiais da Fase 3: regra pré-registrada (acurácia balanceada nos 36 casos de avaliação, veto
por autoenvenenamento), bootstrap por caso, estabilidade do ranking, fronteira de Pareto,
escore ponderado com varredura de sensibilidade, comparação pareada contra a Fase 3-B (quando
houver) e o resumo da revisão humana. Grava decisao_modelo.json e decisao_modelo.md dentro da
pasta da Fase 3 (ver caminhos.fase3)."""
import argparse
import json
import math
import random
import re  # 22/09/2026: _modelo_por_slug (slug da pasta a partir do nome do modelo)
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

import avaliar
import avaliar_fase3
import caminhos

# ! Alteração de IA - Revisar: força UTF-8 na saída do console, copiado de
# biblioteca.py:25-32.
# ! Motivo: no Windows o console pode estar em cp1252, que não representa os símbolos usados
# nas tabelas daqui (→, %, —) -- sem isso o script aborta com UnicodeEncodeError depois de já
# ter gravado os JSON, e quem roda vê um traceback no lugar do resumo.
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


# --------------------------------------------------------------------- constantes

# Colunas de comparacao_fases.json usadas na checagem de estabilidade do ranking (passo 3) --
# fora ficam 2A_linear_ryzen (máquina diferente, Ryzen) e 2B_A3 (teto artificial com o verbete
# de ouro sempre entregue): nenhuma das duas é um estado que o modelo alcança sozinho em
# produção, então não fazem sentido como candidatas de estabilidade da decisão.
_COLUNAS_ESTABILIDADE = ("2B_A0", "2B_A2", "F3_L0", "F3_L1", "F3_L2", "F3_L3")

# Campo de origem (em cada candidato de montar_candidatos) e se o critério é de CUSTO/RISCO
# (inverte no mín-máx: menor valor bruto -> maior escore) para cada peso de
# pesos_decisao.json['pesos'].
_CAMPO_CRITERIO = {
    "acuracia_balanceada_36": ("acuracia_balanceada_36", False),
    "acerto_36": ("acerto_36", False),
    "custo_segundos": ("segundos_mediana_36", True),
    "risco": ("risco", True),
}

_FRASE_REVISAO_VAZIA = ("Nenhuma edição foi revisada manualmente até esta corrida -- a "
                        "planilha revisao_edicoes__<slug>.md "
                        "(avaliar_fase3.gerar_planilha_revisao) está vazia ou não foi "
                        "preenchida.")


# --------------------------------------------------------------- formatação (Markdown)

def _n(v) -> str:
    """! Alteração de IA - Revisar: mesma formatação de comparar_fases._n (vírgula decimal,
    1 casa, '—' para None) -- reimplementada aqui (não importada) porque é uma função privada
    (prefixo '_') de outro módulo, e funções com '_' não fazem parte da interface que um
    módulo deveria importar de outro.
    ! Motivo: o brief P2.1 pede 'ponto decimal trocado por vírgula como em comparar_fases.py'
    -- reescrever as 4 linhas aqui evita depender de um símbolo interno de comparar_fases que
    pode mudar sem aviso (não é parte do contrato entre os dois arquivos)."""
    if v is None:
        return "—"
    if isinstance(v, float):
        return f"{v:.1f}".replace(".", ",")
    return str(v)


def _pct(v) -> str:
    """! Alteração de IA - Revisar: _n(v) com '%' -- mesma regra de comparar_fases._pct.
    ! Motivo: ver _n."""
    return "—" if v is None else f"{_n(v)}%"


def _p(v: float | None) -> str:
    """! Alteração de IA - Revisar: p-valor com 4 casas e '*' colado quando p < 0,05 -- mesma
    regra de comparar_fases._p e avaliar_fase3.imprimir_resumo.
    ! Motivo: ver _n; 4 casas porque a 1 casa de _n arredondaria um p pequeno (0,002) para
    '0,0', indistinguível de p=1,0."""
    if v is None:
        return "—"
    texto = f"{v:.4f}".replace(".", ",")
    return f"{texto}*" if v < 0.05 else texto


# --------------------------------------------------------- passo 1: regra da decisão 36

def montar_candidatos(comparacao: dict, limiar: float) -> list[dict]:
    """! Alteração de IA - Revisar: uma linha por (modelo, L) presente em
    comparacao['por_modelo'][modelo]['nos_36_avaliacao']['F3_L0'..'F3_L3'] -- acurácia
    balanceada, acerto, n, segundos mediana, fora do conjunto e formato-ok-conteúdo-errado
    (todos nos 36 casos de avaliação), autoenvenenamento máximo do MODELO (não por L -- ver
    Motivo), adesão cega (2-B A5, também por modelo) e risco (média simples dos quatro
    últimos, pulando os ausentes -- registrados em risco_componentes_ausentes). 'vetado' é
    True quando o autoenvenenamento máximo passa do limiar de pesos_decisao.json.
    ! Motivo: comparacao_fases.json guarda autoenvenenamento_F3 e adesao_cega_2B_A5_pct por
    MODELO -- autoenvenenamento_F3 é por TRANSIÇÃO (L0→L1/L1→L2/L2→L3), uma propriedade do
    processo de edição do modelo, não de um estado isolado da biblioteca -- então o veto se
    aplica a TODOS os L daquele modelo por igual: se o processo de edição se autoenvenena em
    qualquer transição, nenhum estado editado por ele deveria ser recomendado para produção
    sem essa ressalva (inclusive o próprio L0, que fica de fora da recomendação junto com os
    demais, porque a pergunta desta tarefa é 'que MODELO levar para produção', não 'que
    estado isolado')."""
    candidatos = []
    for modelo, dados in sorted(comparacao.get("por_modelo", {}).items()):
        auto = dados.get("autoenvenenamento_F3") or {}
        auto_max = max(auto.values()) if auto else None
        adesao = dados.get("adesao_cega_2B_A5_pct")
        vetado = auto_max is not None and auto_max > limiar
        nos_36 = dados.get("nos_36_avaliacao") or {}
        for epoca in avaliar_fase3.VERSOES:
            col = nos_36.get(f"F3_L{epoca}")
            if col is None:
                continue
            componentes = {
                "autoenvenenamento_max_36": auto_max,
                "adesao_cega_2B_A5_pct": adesao,
                "fora_do_conjunto_pct_36": col.get("fora_do_conjunto_pct"),
                "formato_ok_conteudo_errado_pct_36": col.get("formato_ok_conteudo_errado_pct"),
            }
            presentes = [v for v in componentes.values() if v is not None]
            ausentes = [nome for nome, v in componentes.items() if v is None]
            risco = round(sum(presentes) / len(presentes), 2) if presentes else None
            candidatos.append({
                "modelo": modelo, "biblioteca_epoca": epoca,
                "acuracia_balanceada_36": col.get("acuracia_balanceada_pct"),
                "acerto_36": col.get("acerto_pct"),
                "n_36": col.get("n"),
                "segundos_mediana_36": col.get("segundos_mediana"),
                "fora_do_conjunto_pct_36": componentes["fora_do_conjunto_pct_36"],
                "formato_ok_conteudo_errado_pct_36": componentes[
                    "formato_ok_conteudo_errado_pct_36"],
                "autoenvenenamento_max_36": auto_max,
                "adesao_cega_2B_A5_pct": adesao,
                "vetado": vetado,
                "motivo_veto": (f"autoenvenenamento máximo {_pct(auto_max)} > limiar "
                               f"{_pct(limiar)}" if vetado else None),
                "risco": risco,
                "risco_componentes_ausentes": ausentes,
            })
    return candidatos


def regra_36(candidatos: list[dict]) -> dict:
    """! Alteração de IA - Revisar: regra pré-registrada (brief P2.1, passo 1) -- ranking dos
    (modelo, L) elegíveis (acurácia balanceada nos 36 não-nula) por acurácia balanceada
    decrescente; em empate, a época (L) mais baixa vence -- mesmo critério de
    `comparar_fases._melhor_f3` (~l.233 de comparar_fases.py): a ordem de iteração ali é
    L0..L3 e max() preserva o primeiro máximo encontrado, porque 'uma época mais tardia é
    melhor' sem diferença medida não é uma alegação que o número sustenta; em empate
    remanescente (mesma época, modelos diferentes -- caso que _melhor_f3 não cobre, porque só
    compara L dentro de UM modelo), o nome do modelo desempata, só para o ranking sair sempre
    igual entre corridas. O vencedor é o primeiro da lista SEM veto; se todos estiverem
    vetados, vencedor é None.
    ! Motivo: é a Saída 1 do brief -- decidir modelo e estado da biblioteca com uma regra
    fixada ANTES de olhar robustez (bootstrap/Pareto/escore, calculados depois), para a
    decisão não ser escolhida a dedo entre vários critérios até um bater com uma preferência
    prévia."""
    elegiveis = [c for c in candidatos if c["acuracia_balanceada_36"] is not None]
    ranking = sorted(elegiveis, key=chave_desempate)
    nao_vetados = [c for c in ranking if not c["vetado"]]
    return {
        "ranking": ranking,
        "vencedor": nao_vetados[0] if nao_vetados else None,
        "criterio_desempate": "acurácia balanceada decrescente; empate -> licença mais "
                              "permissiva (Apache-2.0 antes de MIT, antes das demais; decisão "
                              "36); empate -> época (L) mais baixa (comparar_fases._melhor_f3); "
                              "empate remanescente -> nome do modelo",
        "licencas": {c["modelo"]: LICENCAS.get(c["modelo"], "desconhecida") for c in elegiveis},
    }


# ! Alteração de IA - Revisar: licença de cada modelo e ordem de preferência para o desempate da
# decisão 36 ("licença como desempate"), acrescentados em 21/09/2026 depois da revisão da P2.1.
# ! Motivo: o implementador não tinha como saber o que "licença" significava na regra; a decisão 36
# (plano da Fase 3) manda preferir a licença mais permissiva em empate de acurácia balanceada. Os 4
# modelos da Fase 3 são Apache-2.0 (Qwen2.5 e Granite 4.2 pelos model cards no Ollama), então o
# critério não muda o resultado hoje — mas fica implementado para valer se um modelo MIT ou de
# licença restritiva entrar na comparação.
LICENCAS = {
    "granite4.2:8b": "Apache-2.0",
    "qwen2.5:7b": "Apache-2.0",
    "qwen2.5-coder:7b": "Apache-2.0",
    "qwen2.5-coder:3b": "Apache-2.0",
    "phi4-mini:3.8b": "MIT",
    "qwen2.5-coder:1.5b": "Apache-2.0",
}
ORDEM_LICENCA = {"Apache-2.0": 0, "MIT": 1}


# ! Alteração de IA - Revisar: ordem única de desempate (licença, L, nome) usada pela regra 36 e pelo P(top-1) do bootstrap (P2.1, 21/09/2026).
# ! Motivo: dois lugares com ordens diferentes davam ranking e P(top-1) contraditórios; uma chave só garante o mesmo vencedor nos dois.
def chave_desempate(c: dict) -> tuple:
    """Ordem do ranking da regra 36 (e do P(top-1) do bootstrap, que usa a mesma chave): acurácia
    balanceada nos 36 decrescente; licença mais permissiva; época (L) mais baixa; nome do modelo."""
    return (-c["acuracia_balanceada_36"], ORDEM_LICENCA.get(LICENCAS.get(c["modelo"], ""), 2),
            c["biblioteca_epoca"], c["modelo"])


# --------------------------------------------------------------- passo 2: bootstrap por caso

def _reamostrar(rng: random.Random, n: int) -> list[int]:
    """! Alteração de IA - Revisar: n índices sorteados de 0..n-1 COM reposição, usando
    rng.randrange -- não random.choices, cujo algoritmo interno não é parte da API pública
    documentada e poderia mudar de versão para versão do Python (o que quebraria a
    reprodutibilidade prometida pela semente entre execuções em Pythons diferentes).
    ! Motivo: é o mesmo índice que precisa valer para TODOS os (modelo, L) dentro de uma
    réplica (brief P2.1, passo 2: 'a mesma amostra de casos vale para todos... dentro de uma
    réplica'), então o sorteio acontece uma vez por réplica em vez de uma vez por (modelo,
    L)."""
    return [rng.randrange(n) for _ in range(n)]


def _percentil(ordenados: list[float], p: float) -> float | None:
    """! Alteração de IA - Revisar: percentil pelo método do posto mais próximo (mesma regra
    de avaliar_fase3._p95: ordenados[ceil(p*n) - 1]), usado nos limites 2,5%/97,5% do IC do
    bootstrap.
    ! Motivo: reproduz o método já usado no harness em vez de interpolar (que exigiria decidir
    um método de interpolação novo só para este IC) -- com 2.000 réplicas a diferença entre os
    dois métodos fica abaixo da segunda casa decimal."""
    if not ordenados:
        return None
    idx = min(len(ordenados) - 1, max(0, math.ceil(p * len(ordenados)) - 1))
    return round(ordenados[idx], 1)


def _bootstrap_conjunto(avaliados: list[dict], ids: list[str], n_bootstrap: int,
                        semente: int) -> dict:
    """! Alteração de IA - Revisar: bootstrap por caso (com reposição) sobre uma lista de ids
    -- IC 95% percentil da acurácia balanceada (avaliar_fase3.acuracia_balanceada) e P(top-1)
    por (modelo, biblioteca_epoca); cada réplica tem exatamente um vencedor (desempate por
    licença mais permissiva, L mais baixa e depois por nome do modelo -- mesma ordem de
    chave_desempate/regra_36), para P(top-1) somar 1,0 entre os candidatos, nunca mais nem menos.
    ! Motivo: é o núcleo comum entre 'nos 36' e 'nos 90' (brief P2.1, passo 2: 'repetir nos
    90') -- calculado uma vez, parametrizado pela lista de ids, para as duas chamadas de
    bootstrap() nunca divergirem na reamostragem nem no desempate do P(top-1)."""
    pares_por_combo: dict[tuple, dict[str, tuple]] = defaultdict(dict)
    for a in avaliados:
        if a["caso"] in ids:
            pares_por_combo[(a["modelo"], a["biblioteca_epoca"])][a["caso"]] = \
                (a["causa_esperada"], a["causa_respondida"])
    combos = sorted(pares_por_combo)

    n = len(ids)
    rng = random.Random(semente)
    valores: dict[tuple, list[float]] = defaultdict(list)
    contagem_top1: dict[tuple, int] = defaultdict(int)
    for _ in range(n_bootstrap):
        idxs = _reamostrar(rng, n) if n else []
        resultado_replica = {}
        for combo in combos:
            mapa = pares_por_combo[combo]
            pares = [mapa[ids[i]] for i in idxs if ids[i] in mapa]
            if not pares:
                continue
            acc = avaliar_fase3.acuracia_balanceada(pares)
            valores[combo].append(acc)
            resultado_replica[combo] = acc
        if resultado_replica:
            vencedor = min(resultado_replica.items(),
                           key=lambda item: (-item[1], ORDEM_LICENCA.get(LICENCAS.get(item[0][0], ""), 2),
                                             item[0][1], item[0][0]))[0]
            contagem_top1[vencedor] += 1

    saida = []
    for combo in combos:
        vs = sorted(valores.get(combo, []))
        ic = [_percentil(vs, 0.025), _percentil(vs, 0.975)]
        saida.append({
            "modelo": combo[0], "biblioteca_epoca": combo[1], "ic95_bootstrap": ic,
            "p_top1": round(contagem_top1.get(combo, 0) / n_bootstrap, 4)
                     if n_bootstrap else 0.0,
        })
    return {"n": n, "combos": saida}


def bootstrap(avaliados: list[dict], n_bootstrap: int, semente: int) -> dict:
    """! Alteração de IA - Revisar: bootstrap por caso (brief P2.1, passo 2) nos 36 casos de
    avaliação e nos 90 (as duas partições somadas), reamostrando com random.Random(semente).
    ! Motivo: é a checagem de robustez do vencedor da regra 36 -- se o IC 95% de dois
    (modelo, L) se sobrepõe muito e P(top-1) fica espalhado entre vários candidatos, a
    diferença medida nos 36 casos pode ser ruído de amostra pequena, não um efeito real (mesma
    lógica de avaliar_fase3.efeito_minimo_detectavel, aplicada por reamostragem em vez de
    fórmula fechada)."""
    ids_36 = sorted({a["caso"] for a in avaliados if a["particao"] == "avaliacao"})
    ids_90 = sorted({a["caso"] for a in avaliados})
    return {
        "n_bootstrap": n_bootstrap, "semente": semente,
        "nos_36": _bootstrap_conjunto(avaliados, ids_36, n_bootstrap, semente),
        "nos_90": _bootstrap_conjunto(avaliados, ids_90, n_bootstrap, semente),
    }


# ------------------------------------------------------------ passo 3: estabilidade do ranking

def estabilidade_ranking(comparacao: dict, resumo_f3: dict) -> dict:
    """! Alteração de IA - Revisar: brief P2.1, passo 3 -- um ranking dos modelos (por
    acurácia balanceada) para cada coluna de comparacao_fases.json (_COLUNAS_ESTABILIDADE)
    nos 36 e nos 90 casos, e mais um por (classe de defeito, L) nos 90 casos, a partir de
    resumo_fase3.json['por_modelo_biblioteca_classe'] (as 23 causas do conjunto fechado se
    agrupam em 6 classes -- ver gerar_graficos_fase3.ROTULO_CLASSE). Devolve a lista de
    rankings, a posição de cada modelo em cada um e quantas vezes cada modelo ficou em 1º,
    somando as duas famílias de corte.
    ! Motivo: a regra 36 (passo 1) decide com UM corte (36 casos, biblioteca no estado L); um
    modelo que só vence ali pode ser um acaso do recorte -- se o MESMO modelo aparece em 1º na
    maioria dos cortes independentes (outra fase, outra partição, outra classe de defeito), a
    escolha é mais defensável do que se ele vencer só no corte pré-registrado. O corte por
    classe usa a partição 'todos' (90 casos), não 'avaliacao': avaliar_fase3.avaliar_saida
    monta por_modelo_biblioteca_classe só a partir de `marcados` (_com_particao_todos(
    avaliados), ~l.1092) -- 36 casos já divididos em até 6 classes deixaria alguma célula com
    1-2 casos, e o harness não grava esse corte fino por partição; filtrar por 'avaliacao'
    aqui simplesmente não acharia nenhuma linha (conferido contra o resumo_fase3.json real:
    100% das 96 linhas têm particao='todos')."""
    por_modelo = comparacao.get("por_modelo", {})
    modelos = sorted(por_modelo)
    rankings: list[dict] = []

    def registrar(nome: str, valores: dict) -> None:
        presentes = sorted(((m, v) for m, v in valores.items() if v is not None),
                           key=lambda mv: (-mv[1], mv[0]))
        if presentes:
            rankings.append({"nome": nome, "ranking": [m for m, _ in presentes],
                             "valores": dict(presentes)})

    for conjunto, chave in (("36", "nos_36_avaliacao"), ("90", "nos_90")):
        for coluna in _COLUNAS_ESTABILIDADE:
            valores = {m: ((por_modelo[m].get(chave) or {}).get(coluna) or {})
                         .get("acuracia_balanceada_pct") for m in modelos}
            registrar(f"{coluna} ({conjunto} casos)", valores)

    linhas_classe = [l for l in resumo_f3.get("por_modelo_biblioteca_classe", [])
                     if l.get("particao") == "todos"]
    for classe in sorted({l["classe"] for l in linhas_classe}):
        for epoca in avaliar_fase3.VERSOES:
            valores = {l["modelo"]: l["acuracia_balanceada_pct"] for l in linhas_classe
                      if l["classe"] == classe and l["biblioteca_epoca"] == epoca}
            registrar(f"classe {classe} L{epoca} (90 casos)", valores)

    posicoes: dict[str, dict[str, int]] = defaultdict(dict)
    top1: dict[str, int] = defaultdict(int)
    for item in rankings:
        for posicao, modelo in enumerate(item["ranking"], start=1):
            posicoes[modelo][item["nome"]] = posicao
            if posicao == 1:
                top1[modelo] += 1

    return {"rankings": rankings, "tabela_posicoes": dict(posicoes),
           "top1_por_modelo": dict(top1), "total_rankings": len(rankings)}


# --------------------------------------------------------------- passo 4: fronteira de Pareto

def pareto(candidatos: list[dict]) -> dict:
    """! Alteração de IA - Revisar: fronteira de Pareto entre (modelo, L) -- maximizando
    acurácia balanceada (36) e minimizando segundos (mediana, 36) e risco; só entram
    candidatos com os três números presentes (os demais contam em
    excluidos_dados_incompletos). Um ponto é dominado quando existe outro igual-ou-melhor nos
    três eixos e estritamente melhor em pelo menos um.
    ! Motivo: brief P2.1, passo 4 -- a regra 36 e o escore ponderado (passo 5) reduzem tudo a
    UM número; a fronteira mostra as combinações em que não há outra estritamente melhor em
    todos os eixos ao mesmo tempo, então descartar uma delas é uma troca explícita (mais caro
    por mais certeiro, por exemplo), não um erro de conta."""
    pontos = [c for c in candidatos if c["acuracia_balanceada_36"] is not None
             and c["segundos_mediana_36"] is not None and c["risco"] is not None]

    def domina(a: dict, b: dict) -> bool:
        melhor_ou_igual = (a["acuracia_balanceada_36"] >= b["acuracia_balanceada_36"]
                           and a["segundos_mediana_36"] <= b["segundos_mediana_36"]
                           and a["risco"] <= b["risco"])
        estrito = (a["acuracia_balanceada_36"] > b["acuracia_balanceada_36"]
                  or a["segundos_mediana_36"] < b["segundos_mediana_36"]
                  or a["risco"] < b["risco"])
        return melhor_ou_igual and estrito

    nao_dominados = [b for b in pontos if not any(domina(a, b) for a in pontos if a is not b)]
    nao_dominados.sort(key=lambda c: (c["modelo"], c["biblioteca_epoca"]))
    campos = ("modelo", "biblioteca_epoca", "acuracia_balanceada_36", "segundos_mediana_36",
             "risco", "vetado")
    return {
        "candidatos_considerados": len(pontos),
        "excluidos_dados_incompletos": len(candidatos) - len(pontos),
        "nao_dominados": [{k: c[k] for k in campos} for c in nao_dominados],
    }


# ------------------------------------------------------ passo 5: escore ponderado e sensibilidade

def _normalizar_minmax(valores: dict, inverter: bool) -> dict:
    """! Alteração de IA - Revisar: normalização mín-máx de um critério para [0, 1] entre os
    candidatos que têm valor -- 1,0 para todos quando todos empatam (não discrimina, mas
    também não penaliza ninguém, positivo ou negativo). `inverter=True` troca para
    (1 - normalizado), o que faz um critério de CUSTO (menor é melhor) virar 'maior é melhor'
    na mesma escala 0-1 dos demais.
    ! Motivo: acurácia balanceada (pp), segundos (s) e risco (pp, média de percentuais) estão
    em escalas numéricas diferentes -- somar os pesos direto sobre os valores brutos deixaria
    o critério de maior escala dominar o escore, mascarando o peso que pesos_decisao.json
    declara."""
    presentes = {k: v for k, v in valores.items() if v is not None}
    if not presentes:
        return {k: None for k in valores}
    lo, hi = min(presentes.values()), max(presentes.values())
    saida = {}
    for k, v in valores.items():
        if v is None:
            saida[k] = None
        elif hi == lo:
            saida[k] = 1.0
        else:
            normal = (v - lo) / (hi - lo)
            saida[k] = round((1 - normal) if inverter else normal, 4)
    return saida


def escore_ponderado(candidatos: list[dict], pesos: dict) -> dict:
    """! Alteração de IA - Revisar: brief P2.1, passo 5 -- escore = soma, por critério, do
    peso de pesos_decisao.json vezes o valor normalizado mín-máx (_normalizar_minmax); custo e
    risco entram invertidos para 'menor' valer mais escore. Vencedor é o de maior escore SEM
    veto; se todos estiverem vetados, escolhe entre todos mesmo assim (sensibilidade() chama
    esta função uma vez por passo da varredura e precisa de um vencedor em cada chamada para
    montar a lista de mudanças).
    ! Motivo: é o segundo vencedor do documento (o primeiro é o da regra 36, passo 1) -- serve
    para checar se os dois métodos concordam. A normalização é sempre recalculada sobre o
    conjunto de candidatos RECEBIDO (não sobre um mín-máx fixo), porque sensibilidade() varia
    só os pesos -- o mín-máx de cada critério não muda entre as chamadas dela."""
    def chave(c: dict) -> tuple:
        return (c["modelo"], c["biblioteca_epoca"])

    normalizados = {}
    for criterio, (campo, inverter) in _CAMPO_CRITERIO.items():
        valores = {chave(c): c[campo] for c in candidatos}
        normalizados[criterio] = _normalizar_minmax(valores, inverter)

    linhas = []
    for c in candidatos:
        k = chave(c)
        partes = {criterio: normalizados[criterio][k] for criterio in _CAMPO_CRITERIO}
        if any(v is None for v in partes.values()):
            score = None
        else:
            score = round(sum(pesos.get(criterio, 0.0) * valor
                              for criterio, valor in partes.items()), 4)
        linhas.append({"modelo": c["modelo"], "biblioteca_epoca": c["biblioteca_epoca"],
                       "score": score, "componentes_normalizados": partes,
                       "vetado": c["vetado"]})

    elegiveis = [l for l in linhas if l["score"] is not None]
    nao_vetados = [l for l in elegiveis if not l["vetado"]]
    base = nao_vetados or elegiveis
    vencedor = (min(base, key=lambda l: (-l["score"], ORDEM_LICENCA.get(LICENCAS.get(l["modelo"], ""), 2), l["biblioteca_epoca"], l["modelo"]))
               if base else None)
    linhas.sort(key=lambda l: (l["score"] is None, -(l["score"] or 0.0), l["biblioteca_epoca"],
                               l["modelo"]))
    return {"pesos": pesos, "linhas": linhas, "vencedor": vencedor}


def _renormalizar(pesos: dict, criterio: str, novo_peso: float) -> dict:
    """! Alteração de IA - Revisar: pesos_decisao.json com o peso de `criterio` fixado em
    `novo_peso` e os demais reescalados para somar (1 - novo_peso), preservando a PROPORÇÃO
    relativa entre eles (empate 50/50 -- ou 1/N -- se a soma original dos outros for zero).
    ! Motivo: é o passo de sensibilidade do brief P2.1 -- 'varrer cada peso de 0 a 1 ...
    renormalizando os demais'; preservar a proporção original (em vez de, por exemplo,
    distribuir sempre igual) é o que faz a varredura mexer em UM eixo de decisão por vez -- a
    importância relativa dos outros três continua a mesma que pesos_decisao.json declarou, em
    vez de misturar duas mudanças de critério na mesma réplica da varredura."""
    outros = {k: v for k, v in pesos.items() if k != criterio}
    resto = max(0.0, round(1 - novo_peso, 10))
    soma_outros = sum(outros.values())
    if soma_outros <= 0:
        n = len(outros) or 1
        redistribuidos = {k: resto / n for k in outros}
    else:
        redistribuidos = {k: resto * (v / soma_outros) for k, v in outros.items()}
    return {**redistribuidos, criterio: novo_peso}


def sensibilidade(candidatos: list[dict], pesos: dict, passo: float = 0.05) -> dict:
    """! Alteração de IA - Revisar: brief P2.1, passo 5 -- para cada critério, varre o peso
    dele de 0 a 1 em passos de 0,05 (21 pontos), renormalizando os demais (_renormalizar), e
    registra em que passo o vencedor do escore ponderado muda em relação ao passo anterior.
    ! Motivo: um escore com um único conjunto de pesos parece mais firme do que é -- a
    varredura mostra se o vencedor da regra 36/escore é robusto (só muda perto dos extremos,
    ou nunca muda) ou frágil (muda logo cedo, então a escolha de peso decide o resultado mais
    do que os dados medidos)."""
    n_passos = int(round(1 / passo))
    valores_w = [round(i * passo, 2) for i in range(n_passos + 1)]
    saida = {}
    for criterio in pesos:
        pontos = []
        anterior = None
        mudancas = []
        for w in valores_w:
            pesos_w = _renormalizar(pesos, criterio, w)
            venc = escore_ponderado(candidatos, pesos_w)["vencedor"]
            rotulo = f"{venc['modelo']}/L{venc['biblioteca_epoca']}" if venc else None
            pontos.append({"peso": w, "vencedor": rotulo})
            if anterior is not None and rotulo != anterior:
                mudancas.append({"peso": w, "de": anterior, "para": rotulo})
            anterior = rotulo
        saida[criterio] = {"pontos": pontos, "mudancas_de_vencedor": mudancas}
    return saida


# ---------------------------------------------------------------------------- passo 6: 3-B

def _matriz_cruzada(avaliados_3b: list[dict], doador: str | None) -> list[dict]:
    """! Alteração de IA - Revisar: uma linha por (leitor, L) do modo 'cruzada' -- acerto e
    acurácia balanceada nos 36 casos de avaliação, usando a biblioteca escrita pelo --doador
    (condicoes_3b.json).
    ! Motivo: brief P2.1, passo 6 -- 'para cruzada, matriz doador × leitor'; é a tabela que
    responde 'a documentação que o modelo X escreveu ajuda o modelo Y a diagnosticar', em vez
    de só medir cada modelo com a PRÓPRIA biblioteca (o que os outros modos da 3-B já
    respondem)."""
    por_leitor_epoca: dict[tuple, list[dict]] = defaultdict(list)
    for r in avaliados_3b:
        if r.get("particao") == "avaliacao":
            por_leitor_epoca[(r["modelo"], r["biblioteca_epoca"])].append(r)
    linhas = []
    for (leitor, epoca), regs in sorted(por_leitor_epoca.items()):
        n = len(regs)
        acertos = sum(1 for r in regs if r["causa_correta"])
        linhas.append({
            "doador": doador, "leitor": leitor, "biblioteca_epoca": epoca, "n": n,
            "acerto_pct": round(100 * acertos / n, 1) if n else None,
            "acuracia_balanceada_pct": avaliar_fase3.acuracia_balanceada(
                [(r["causa_esperada"], r["causa_respondida"]) for r in regs]),
        })
    return linhas


def comparar_3b(nome: str, c3_saida: dict, avaliados_f3: list[dict]) -> dict | None:
    """! Alteração de IA - Revisar: brief P2.1, passo 6 -- lê avaliacao_fase3.json de uma
    saída da Fase 3-B (ponte/cruzada/texto_max/inéditos), agrega acerto e acurácia balanceada
    por (modelo, L) nos 36 casos de avaliação e pareia caso a caso contra a MESMA (modelo, L)
    da Fase 3 oficial (avaliados_f3) com avaliar.mcnemar_exato (~l.155), avaliar_fase3.holm
    (~l.150, por família de modelo) e avaliar_fase3.g_cohen (~l.174); no modo 'cruzada',
    acrescenta a matriz doador x leitor (_matriz_cruzada). None se a saída não tem
    avaliacao_fase3.json ainda (o script chamador imprime 'sem 3-B').
    ! Motivo: a Fase 3-B testa hipóteses que a Fase 3 oficial não isola (ponte: o Ollama mudou
    de versão entre as duas corridas? cruzada: a biblioteca de um modelo ajuda outro? texto_max:
    o teto de 280 caracteres por nota limitou o ganho?) -- comparar pareado contra a Fase 3
    (mesmos casos, McNemar) é o que diz se a diferença é maior que o esperado por acaso, sem
    reimplementar o pareamento já usado em avaliar_fase3.pareado_vs_l0/
    comparar_fases._parear."""
    if not c3_saida["avaliacao"].exists():
        return None
    avaliados_3b = json.loads(c3_saida["avaliacao"].read_text(encoding="utf-8"))
    condicoes_path = c3_saida["raiz"] / "condicoes_3b.json"
    condicoes = (json.loads(condicoes_path.read_text(encoding="utf-8"))
                if condicoes_path.exists() else {})
    modo = condicoes.get("modo", nome)

    def mapa(avaliados: list[dict]) -> dict[tuple, dict[str, tuple]]:
        m: dict[tuple, dict[str, tuple]] = defaultdict(dict)
        for r in avaliados:
            if r.get("particao") == "avaliacao":
                m[(r["modelo"], r["biblioteca_epoca"])][r["caso"]] = (
                    r["causa_correta"], r["causa_esperada"], r["causa_respondida"])
        return m

    mapa_3b, mapa_f3 = mapa(avaliados_3b), mapa(avaliados_f3)
    linhas = []
    por_familia: dict[str, list[dict]] = defaultdict(list)
    for (modelo, epoca), casos_3b in sorted(mapa_3b.items()):
        n = len(casos_3b)
        acertos = sum(1 for v in casos_3b.values() if v[0])
        linha = {
            "modelo": modelo, "biblioteca_epoca": epoca, "n": n,
            "acerto_pct": round(100 * acertos / n, 1) if n else None,
            "acuracia_balanceada_pct": avaliar_fase3.acuracia_balanceada(
                [(v[1], v[2]) for v in casos_3b.values()]),
            "pareado_vs_f3": None,
        }
        casos_f3 = mapa_f3.get((modelo, epoca), {})
        comuns = sorted(set(casos_3b) & set(casos_f3))
        if comuns:
            b = sum(1 for c in comuns if casos_3b[c][0] and not casos_f3[c][0])
            cc = sum(1 for c in comuns if casos_f3[c][0] and not casos_3b[c][0])
            linha["pareado_vs_f3"] = {
                "n_comuns": len(comuns), "b": b, "c": cc,
                "p_mcnemar": avaliar.mcnemar_exato(b, cc),
                "g_cohen": avaliar_fase3.g_cohen(b, cc), "p_holm": None,
            }
            por_familia[modelo].append(linha["pareado_vs_f3"])
        linhas.append(linha)

    for pares in por_familia.values():
        ajustados = avaliar_fase3.holm([p["p_mcnemar"] for p in pares])
        for p, adj in zip(pares, ajustados):
            p["p_holm"] = adj

    saida = {"modo": modo, "linhas": linhas}
    if modo == "cruzada":
        saida["matriz_doador_leitor"] = _matriz_cruzada(avaliados_3b, condicoes.get("doador"))
    return saida


# ---------------------------------------------------------------------- passo 7: revisão humana

def _modelo_por_slug(avaliados_f3: list[dict] | None) -> dict[str, str]:
    """! Alteração de IA - Revisar: mapa slug -> nome do modelo a partir dos registros avaliados
    (22/09/2026): 'qwen2.5:7b' vira 'qwen2.5_7b', que é o nome da subpasta e da planilha.
    ! Motivo: avaliar_fase3.revisao_humana precisa do nome do modelo para rotular as contagens,
    e a mesma troca de ':' e '/' por '_' é a que o executor usa ao criar a pasta do modelo;
    derivar dos registros evita ler os JSONL de diagnóstico inteiros só para achar o nome."""
    modelos = {r["modelo"] for r in (avaliados_f3 or []) if r.get("modelo")}
    return {re.sub(r"[^A-Za-z0-9._-]", "_", m): m for m in modelos}


def resumo_revisao_humana(resumo_f3: dict, c3: dict | None = None,
                          avaliados_f3: list[dict] | None = None) -> dict:
    """! Alteração de IA - Revisar: brief P2.1, passo 7 -- proporções Correta/Parcial/Errada/
    sem_avaliacao por modelo, somando as linhas de resumo_fase3.json['revisao_humana'] (uma
    por operação -- avaliar_fase3.revisao_humana já agrupa por modelo ali); 'sem_avaliacao'
    com a frase padrão quando a lista está vazia ou ausente. Desde 22/09/2026, quando o
    resumo oficial não traz a revisão e `c3` é dado, lê as planilhas
    revisao_edicoes__<slug>.md direto da pasta da corrida (avaliar_fase3.revisao_humana) e
    registra a fonte em 'fonte'.
    ! Motivo: é o único número do trabalho que não sai de regra automática
    (avaliar_fase3.revisao_humana lê uma planilha preenchida à mão); sem essa marcação
    explícita, uma tabela vazia no Markdown pareceria um bug do script, não um passo do
    processo (a revisão humana) que ainda não aconteceu. A leitura direta das planilhas
    existe porque resumo_fase3.json é registro oficial da bateria de 13-15/09/2026 e não é
    regravado por este script (regra em .claude/rules/experimentos.md); as planilhas foram
    preenchidas depois da bateria e a decisão precisa enxergá-las sem tocar no resumo."""
    linhas = resumo_f3.get("revisao_humana") or []
    fonte = "resumo_fase3.json"
    if not linhas and c3 is not None:
        nomes = _modelo_por_slug(avaliados_f3)
        for slug in avaliar_fase3.slugs_da_saida(c3):
            linhas += avaliar_fase3.revisao_humana(c3, slug, nomes.get(slug, slug))
        fonte = "planilhas revisao_edicoes__<slug>.md lidas direto da pasta da corrida"
    if not linhas:
        return {"status": "sem_avaliacao", "frase": _FRASE_REVISAO_VAZIA}
    por_modelo: dict[str, dict] = {}
    for linha in linhas:
        m = por_modelo.setdefault(linha["modelo"], {"Correta": 0, "Parcial": 0, "Errada": 0,
                                                     "sem_avaliacao": 0})
        for veredito in ("Correta", "Parcial", "Errada", "sem_avaliacao"):
            m[veredito] += linha.get(veredito, 0)
    proporcoes = {}
    for modelo, contagem in por_modelo.items():
        total = sum(contagem.values())
        proporcoes[modelo] = {"n": total, **{
            v: (round(100 * contagem[v] / total, 1) if total else None)
            for v in ("Correta", "Parcial", "Errada", "sem_avaliacao")}}
    return {"status": "avaliada", "fonte": fonte, "por_modelo": proporcoes}


# ------------------------------------------------------------------------- orquestração

def montar_decisao(comparacao: dict, resumo_f3: dict, avaliados_f3: list[dict],
                   pesos_cfg: dict, saidas_3b: dict[str, dict] | None = None,
                   c3: dict | None = None) -> dict:
    """! Alteração de IA - Revisar: roda os 7 passos do brief P2.1 na ordem em que o
    Markdown os usa (regra 36, bootstrap, estabilidade, Pareto, escore ponderado +
    sensibilidade, 3-B, revisão humana) e devolve o dicionário completo de
    decisao_modelo.json.
    ! Motivo: separar o cálculo (esta função) da gravação (gravar()) é o que permite ao
    --check (conferir()) recalcular a decisão em memória sem reescrever o arquivo antes de
    comparar -- mesma separação de avaliar_fase3.avaliar_saida e comparar_fases.
    gerar_comparacao."""
    limiar = pesos_cfg["limiar_autoenvenenamento_pct"]
    pesos = pesos_cfg["pesos"]

    candidatos = montar_candidatos(comparacao, limiar)

    tres_b = None
    if saidas_3b:
        tres_b = {}
        for nome, c3_saida in saidas_3b.items():
            resultado = comparar_3b(nome, c3_saida, avaliados_f3)
            if resultado:
                tres_b[nome] = resultado
        if not tres_b:
            tres_b = None

    return {
        "regra_36": regra_36(candidatos),
        "bootstrap": bootstrap(avaliados_f3, pesos_cfg["n_bootstrap"], pesos_cfg["semente"]),
        "estabilidade_ranking": estabilidade_ranking(comparacao, resumo_f3),
        "pareto": pareto(candidatos),
        "escore_ponderado": escore_ponderado(candidatos, pesos),
        "sensibilidade": sensibilidade(candidatos, pesos),
        "tres_b": tres_b if tres_b is not None else "sem 3-B",
        # c3 (22/09/2026): permite ler as planilhas de revisão direto da pasta da corrida
        "revisao_humana": resumo_revisao_humana(resumo_f3, c3, avaliados_f3),
        "metadados": {
            "pesos": pesos_cfg,
            "gerado_em": datetime.now().isoformat(timespec="seconds"),
        },
    }


# ---------------------------------------------------------------------------- Markdown

def _peso(v: float) -> str:
    """! Alteração de IA - Revisar: formata o peso da varredura de sensibilidade com DUAS casas
    (0,15; 0,75), com vírgula decimal — corrigido em 21/09/2026 depois da revisão da P2.1.
    ! Motivo: a varredura anda de 0,05 em 0,05 e `_n()` formata com uma casa: 0,15 saía "0,1" e
    0,75 saía "0,8" no decisao_modelo.md (o JSON guardava o valor certo), e duas leituras diferentes
    (0,05 e 0,10) colidiam no mesmo texto."""
    return f"{v:.2f}".replace(".", ",")


# ! Alteração de IA - Revisar: renderiza a seção 1 (ranking da regra 36) do decisao_modelo.md a partir do JSON (P2.1, 21/09/2026).
# ! Motivo: cada seção sai de uma função só com campos do JSON, sem número literal, para o --check comparar o render com os dados.
def _tabela_regra_36(regra: dict, limiar: float) -> list[str]:
    linhas = [
        "## 1. Regra da decisão 36 (pré-registrada)", "",
        f"Ranking por acurácia balanceada nos 36 casos de avaliação; veto quando o "
        f"autoenvenenamento máximo do modelo (qualquer transição, nos 36) passa de "
        f"{_pct(limiar)}. Em empate, prevalece a licença mais permissiva (Apache-2.0 antes de "
        "MIT, antes das demais — decisão 36; os quatro modelos da Fase 3 são Apache-2.0, então o "
        "critério não separa ninguém hoje) e, persistindo o empate, a época (L) mais baixa -- "
        "mesmo critério de `comparar_fases._melhor_f3`: a ordem de iteração é L0..L3 e o máximo "
        "preserva o primeiro encontrado, porque afirmar que uma época mais tardia é melhor sem "
        "uma diferença medida não é uma alegação que o número sustenta; em empate remanescente "
        "(mesma época, modelos diferentes), o nome do modelo desempata só para o ranking sair "
        "sempre igual entre corridas.", "",
        "| Modelo | L | Acurácia balanceada (36) | Acerto (36) | n | Autoenvenenamento "
        "máx. (36) | Vetado |",
        "|---|---|---|---|---|---|---|",
    ]
    for c in regra["ranking"]:
        linhas.append(
            f"| {c['modelo']} | L{c['biblioteca_epoca']} | "
            f"{_pct(c['acuracia_balanceada_36'])} | {_pct(c['acerto_36'])} | "
            f"{_n(c['n_36'])} | {_pct(c['autoenvenenamento_max_36'])} | "
            f"{'sim' if c['vetado'] else 'não'} |")
    linhas.append("")
    venc = regra["vencedor"]
    if venc:
        linhas.append(f"**Vencedor da regra 36:** {venc['modelo']} / L{venc['biblioteca_epoca']} "
                      f"({_pct(venc['acuracia_balanceada_36'])} de acurácia balanceada).")
    else:
        linhas.append("**Vencedor da regra 36:** nenhum -- todos os candidatos foram vetados "
                      "por autoenvenenamento.")
    linhas.append("")
    return linhas


# ! Alteração de IA - Revisar: renderiza a seção 2 (bootstrap: IC 95% e P(top-1)) a partir do JSON (P2.1, 21/09/2026).
# ! Motivo: idem: nenhum número digitado no gerador; a tabela é reproduzível pelo --check.
def _tabela_bootstrap(boot: dict) -> list[str]:
    linhas = [
        f"## 2. Bootstrap por caso ({boot['n_bootstrap']} réplicas, semente {boot['semente']})",
        "", "IC 95% percentil da acurácia balanceada e P(top-1) = fração das réplicas em que "
        "o (modelo, L) tem a maior acurácia balanceada entre todos os candidatos da réplica.",
        "",
    ]
    for titulo, chave in (("Nos 36 casos de avaliação", "nos_36"), ("Nos 90 casos", "nos_90")):
        linhas += [f"### {titulo}", "",
                  "| Modelo | L | IC 95% bootstrap | P(top-1) |", "|---|---|---|---|"]
        for c in sorted(boot[chave]["combos"], key=lambda x: -x["p_top1"]):
            ic = c["ic95_bootstrap"]
            ic_txt = "—" if ic[0] is None else f"[{_n(ic[0])}–{_n(ic[1])}]%"
            linhas.append(f"| {c['modelo']} | L{c['biblioteca_epoca']} | {ic_txt} | "
                          f"{_n(round(100 * c['p_top1'], 1))}% |")
        linhas.append("")
    return linhas


# ! Alteração de IA - Revisar: renderiza a seção 3 (estabilidade do ranking por corte) a partir do JSON (P2.1, 21/09/2026).
# ! Motivo: idem.
def _tabela_estabilidade(estab: dict) -> list[str]:
    total = estab["total_rankings"]
    linhas = [
        "## 3. Estabilidade do ranking", "",
        f"{total} cortes (por coluna de comparacao_fases.json nos 36/90 casos, e por classe "
        "de defeito nos 90 casos -- resumo_fase3.json não desmembra a classe por partição), "
        "cada um com o ranking dos modelos por acurácia balanceada; abaixo, em quantos cortes "
        "cada modelo ficou em 1º.", "",
        f"| Modelo | Nº de cortes em 1º (de {total}) |", "|---|---|",
    ]
    for modelo, n in sorted(estab["top1_por_modelo"].items(), key=lambda kv: (-kv[1], kv[0])):
        linhas.append(f"| {modelo} | {n} |")
    linhas.append("")
    return linhas


# ! Alteração de IA - Revisar: renderiza a seção 4 (fronteira de Pareto) a partir do JSON (P2.1, 21/09/2026).
# ! Motivo: idem.
def _tabela_pareto(pto: dict) -> list[str]:
    linhas = [
        "## 4. Fronteira de Pareto", "",
        f"Maximizando acurácia balanceada (36) e minimizando segundos (mediana, 36) e risco "
        f"(média simples de autoenvenenamento máximo, adesão cega, fora do conjunto e "
        f"formato-ok-conteúdo-errado); {pto['candidatos_considerados']} candidatos com os "
        f"três números disponíveis ({pto['excluidos_dados_incompletos']} excluídos por dado "
        "incompleto). Não dominado = nenhum outro (modelo, L) é ao mesmo tempo mais certeiro, "
        "mais barato e menos arriscado.", "",
        "| Modelo | L | Acurácia balanceada (36) | Segundos (mediana, 36) | Risco | Vetado |",
        "|---|---|---|---|---|---|",
    ]
    for c in pto["nao_dominados"]:
        linhas.append(f"| {c['modelo']} | L{c['biblioteca_epoca']} | "
                      f"{_pct(c['acuracia_balanceada_36'])} | {_n(c['segundos_mediana_36'])} | "
                      f"{_n(c['risco'])} | {'sim' if c['vetado'] else 'não'} |")
    linhas.append("")
    return linhas


# ! Alteração de IA - Revisar: renderiza a seção 5 (escore ponderado e sensibilidade) a partir do JSON (P2.1, 21/09/2026).
# ! Motivo: idem; os pesos das mudanças de vencedor saem por _peso() com duas casas.
def _tabela_escore(esc: dict, sens: dict) -> list[str]:
    linhas = [
        "## 5. Escore ponderado e sensibilidade", "",
        "Pesos declarados em pesos_decisao.json (normalização mín-máx por critério; custo e "
        "risco invertidos, para 'menor' virar 'melhor'): " +
        ", ".join(f"{k}={_n(v)}" for k, v in esc["pesos"].items()) + ".", "",
        "| Modelo | L | Score | Vetado |", "|---|---|---|---|",
    ]
    for l in esc["linhas"]:
        linhas.append(f"| {l['modelo']} | L{l['biblioteca_epoca']} | {_n(l['score'])} | "
                      f"{'sim' if l['vetado'] else 'não'} |")
    linhas.append("")
    venc = esc["vencedor"]
    if venc:
        linhas.append(f"**Vencedor do escore ponderado:** {venc['modelo']} / "
                      f"L{venc['biblioteca_epoca']} (score {_n(venc['score'])}).")
    else:
        linhas.append("**Vencedor do escore ponderado:** nenhum -- sem candidato com os 4 "
                      "critérios completos.")
    linhas += ["", "**Sensibilidade** (varredura de 0 a 1 em passos de 0,05, renormalizando "
              "os demais pesos): em que peso o vencedor muda.", ""]
    for criterio in esc["pesos"]:
        mudancas = sens[criterio]["mudancas_de_vencedor"]
        if not mudancas:
            linhas.append(f"- `{criterio}`: o vencedor não muda em toda a varredura.")
        else:
            trechos = "; ".join(f"peso {_peso(m['peso'])} -- {m['de']} passa a {m['para']}"
                                for m in mudancas)
            linhas.append(f"- `{criterio}`: {trechos}.")
    linhas.append("")
    return linhas


# ! Alteração de IA - Revisar: renderiza a seção 6 (Fase 3-B, se houver saídas) a partir do JSON (P2.1, 21/09/2026).
# ! Motivo: idem; sem saídas 3-B a seção diz 'sem 3-B' em vez de sumir, para o leitor saber que foi olhado.
def _secao_3b(tres_b) -> list[str]:
    linhas = ["## 6. Fase 3-B", ""]
    if tres_b == "sem 3-B" or not tres_b:
        linhas += ["Sem 3-B: nenhuma das saídas em `--saidas-3b` tinha `avaliacao_fase3.json` "
                  "no momento desta corrida.", ""]
        return linhas
    for nome, dados in tres_b.items():
        # ! Alteração de IA - Revisar: colunas b (só a 3-B acertou) e c (só a Fase 3 acertou) na tabela (22/09/2026).
        # ! Motivo: o critério da decisão 47 para a ponte de versão é b + c <= 2 por modelo; sem as duas
        # contagens o leitor via só p = 1,0 e não conseguia aplicar a regra a partir do Markdown.
        linhas += [f"### {nome} (modo `{dados['modo']}`)", "",
                  "| Modelo | L | n | Acerto | Acurácia balanceada | n comuns c/ F3 | b | c | "
                  "p (McNemar) | p (Holm) | g de Cohen |",
                  "|---|---|---|---|---|---|---|---|---|---|---|"]
        for l in dados["linhas"]:
            par = l.get("pareado_vs_f3")
            if par:
                n_comuns, b, c, p_mc, p_ho, g = (
                    str(par["n_comuns"]), _n(par["b"]), _n(par["c"]), _p(par["p_mcnemar"]),
                    _p(par.get("p_holm")), _n(par["g_cohen"]))
            else:
                n_comuns, b, c, p_mc, p_ho, g = "—", "—", "—", "—", "—", "—"
            linhas.append(f"| {l['modelo']} | L{l['biblioteca_epoca']} | {_n(l['n'])} | "
                          f"{_pct(l['acerto_pct'])} | {_pct(l['acuracia_balanceada_pct'])} | "
                          f"{n_comuns} | {b} | {c} | {p_mc} | {p_ho} | {g} |")
        linhas.append("")
        if dados.get("matriz_doador_leitor"):
            linhas += ["Matriz doador × leitor:", "",
                      "| Doador | Leitor | L | n | Acerto | Acurácia balanceada |",
                      "|---|---|---|---|---|---|"]
            for m in dados["matriz_doador_leitor"]:
                linhas.append(f"| {m['doador']} | {m['leitor']} | L{m['biblioteca_epoca']} | "
                              f"{_n(m['n'])} | {_pct(m['acerto_pct'])} | "
                              f"{_pct(m['acuracia_balanceada_pct'])} |")
            linhas.append("")
    return linhas


# ! Alteração de IA - Revisar: renderiza a seção 7 (revisão humana) a partir do JSON (P2.1, 21/09/2026).
# ! Motivo: idem; 'sem_avaliacao' vira a frase padrão combinada no brief, não uma tabela vazia.
def _secao_revisao(revisao: dict) -> list[str]:
    linhas = ["## 7. Revisão humana", ""]
    if revisao["status"] == "sem_avaliacao":
        return linhas + [revisao["frase"], ""]
    # fonte (22/09/2026): diz se as contagens vieram do resumo oficial ou das planilhas
    linhas += [f"Fonte: {revisao.get('fonte', 'resumo_fase3.json')}.", "",
              "| Modelo | n | Correta | Parcial | Errada | Sem avaliação |",
              "|---|---|---|---|---|---|"]
    for modelo, p in sorted(revisao["por_modelo"].items()):
        linhas.append(f"| {modelo} | {p['n']} | {_pct(p['Correta'])} | {_pct(p['Parcial'])} | "
                      f"{_pct(p['Errada'])} | {_pct(p['sem_avaliacao'])} |")
    linhas.append("")
    return linhas


# ! Alteração de IA - Revisar: monta a 'Frase da decisão' só com campos do JSON (vencedor, acurácia, veto, Pareto, sensibilidade) (P2.1, 21/09/2026).
# ! Motivo: a frase que o Memorial cita não pode ter número digitado; qualquer mudança nos dados muda a frase pelo --check.
def _frase_decisao(decisao: dict) -> list[str]:
    venc36 = decisao["regra_36"]["vencedor"]
    linhas = ["## Frase da decisão", ""]
    if not venc36:
        linhas.append("Nenhum (modelo, L) passou no veto de autoenvenenamento da regra 36 -- "
                      "não há vencedor pré-registrado para recomendar.")
        return linhas + [""]

    venc_esc = decisao["escore_ponderado"]["vencedor"]
    n_nao_dom = len(decisao["pareto"]["nao_dominados"])
    mudancas_totais = sum(len(s["mudancas_de_vencedor"])
                          for s in decisao["sensibilidade"].values())

    texto = (f"Pela regra pré-registrada (passo 1), o modelo recomendado para produção é "
            f"**{venc36['modelo']}** com a biblioteca no estado **L{venc36['biblioteca_epoca']}"
            f"** ({_pct(venc36['acuracia_balanceada_36'])} de acurácia balanceada nos 36 "
            "casos de avaliação, sem veto por autoenvenenamento).")
    if venc_esc and (venc_esc["modelo"], venc_esc["biblioteca_epoca"]) == \
            (venc36["modelo"], venc36["biblioteca_epoca"]):
        texto += " O escore ponderado (passo 5) concorda com essa escolha."
    elif venc_esc:
        texto += (f" O escore ponderado (passo 5) aponta {venc_esc['modelo']} / "
                  f"L{venc_esc['biblioteca_epoca']} -- ver a varredura de sensibilidade antes "
                  "de decidir entre os dois.")
    linhas.append(texto)
    linhas.append("")
    linhas.append(f"A fronteira de Pareto (passo 4) tem {n_nao_dom} combinação(ões) não "
                  f"dominada(s). A varredura de sensibilidade (passo 5) trocou o vencedor em "
                  f"{mudancas_totais} ponto(s) dos pesos varridos.")
    linhas.append("")
    return linhas


def gerar_markdown(decisao: dict) -> str:
    """! Alteração de IA - Revisar: monta o texto inteiro de decisao_modelo.md -- as 7 seções
    do brief P2.1 mais a 'Frase da decisão', tudo calculado a partir do dicionário `decisao`
    que montar_decisao devolve. Nunca embute a data/hora (metadados.gerado_em fica só no
    JSON) -- mesma escolha de comparar_fases.gerar_markdown, que também não mostra timestamp
    no corpo, para o texto ser uma função pura de `decisao` e o --check comparar direto.
    ! Motivo: separar a montagem do Markdown da montagem do dicionário (como
    avaliar_fase3.imprimir_resumo separa a impressão do cálculo, e como
    comparar_fases.gerar_markdown faz para comparacao_fases.md) é o que permite ao --check
    regerar e comparar sem reler nada do disco além do que já está gravado."""
    linhas = [
        "<!-- ! Alteração de IA - Revisar: gerado por decidir_modelo.py a partir de "
        "comparacao_fases.json, resumo_fase3.json e avaliacao_fase3.json -- NÃO editar à "
        "mão.",
        "     ! Motivo: é o documento que decide o modelo e o estado da biblioteca (L0..L3) "
        "de produção do TCC; editar direto quebraria a garantia de que todo número do "
        "Memorial sai de script, e a próxima corrida de decidir_modelo.py sobrescreveria a "
        "edição sem avisar. -->",
        "", "# Decisão de modelo e estado da biblioteca", "",
    ]
    linhas += _tabela_regra_36(decisao["regra_36"],
                              decisao["metadados"]["pesos"]["limiar_autoenvenenamento_pct"])
    linhas += _tabela_bootstrap(decisao["bootstrap"])
    linhas += _tabela_estabilidade(decisao["estabilidade_ranking"])
    linhas += _tabela_pareto(decisao["pareto"])
    linhas += _tabela_escore(decisao["escore_ponderado"], decisao["sensibilidade"])
    linhas += _secao_3b(decisao["tres_b"])
    linhas += _secao_revisao(decisao["revisao_humana"])
    linhas += _frase_decisao(decisao)
    return "\n".join(linhas)


# ------------------------------------------------------------------ gravação e --check

def _caminhos_decisao(c3: dict) -> tuple[Path, Path]:
    """! Alteração de IA - Revisar: caminho de decisao_modelo.json/.md dentro da pasta da
    Fase 3 (c3['raiz']) -- não em caminhos.fase3(), que o brief da Tarefa P2.1 proíbe alterar
    ('Não altere arquivos existentes exceto testar_fase3b.py').
    ! Motivo: montar os dois caminhos aqui, ao lado de quem os usa, evita editar o módulo
    compartilhado caminhos.py só para acrescentar duas chaves que só este script lê."""
    return c3["raiz"] / "decisao_modelo.json", c3["raiz"] / "decisao_modelo.md"


def gravar(caminho_json: Path, caminho_md: Path, decisao: dict) -> None:
    """! Alteração de IA - Revisar: grava decisao_modelo.json e o .md gerado dele.
    ! Motivo: separar a gravação da montagem (como avaliar_fase3.avaliar_saida e
    comparar_fases.gerar_comparacao fazem) é o que permite ao --check montar a decisão de
    novo em memória (montar_decisao) sem reescrever o arquivo antes de comparar (conferir)."""
    caminho_json.parent.mkdir(parents=True, exist_ok=True)
    caminho_json.write_text(json.dumps(decisao, ensure_ascii=False, indent=2),
                            encoding="utf-8")
    caminho_md.write_text(gerar_markdown(decisao), encoding="utf-8")


def conferir(caminho_json: Path, caminho_md: Path, decisao: dict) -> int:
    """! Alteração de IA - Revisar: --check (brief P2.1) -- regera o texto a partir de
    `decisao` (já recalculada por quem chama, a partir dos dados atuais em disco) e compara
    com o que está gravado, ignorando só metadados.gerado_em no JSON (o .md nunca mostra a
    data -- gerar_markdown não embute timestamp no corpo, mesma escolha de
    comparar_fases.gerar_markdown). Devolve 0 se bate, 1 se difere ou se os arquivos ainda não
    existem.
    ! Motivo: 'nenhum número digitado à mão' (constraints.md) só vale se houver como provar
    que o arquivo gravado é o que o código geraria hoje -- sem excluir gerado_em, o --check
    falharia sempre (a data muda a cada corrida) mesmo com os números idênticos."""
    if not caminho_json.exists() or not caminho_md.exists():
        print(f"--check: {caminho_json.name}/{caminho_md.name} ainda não existem -- rode sem "
             "--check primeiro")
        return 1
    atual = json.loads(caminho_json.read_text(encoding="utf-8"))
    atual.get("metadados", {}).pop("gerado_em", None)
    novo = json.loads(json.dumps(decisao, ensure_ascii=False))
    novo.get("metadados", {}).pop("gerado_em", None)
    ok_json = atual == novo
    atual_md = caminho_md.read_text(encoding="utf-8")
    novo_md = gerar_markdown(decisao)
    ok_md = atual_md == novo_md
    if ok_json and ok_md:
        print(f"--check: {caminho_json.name} e {caminho_md.name} batem com os dados atuais")
        return 0
    if not ok_json:
        print(f"--check: {caminho_json.name} DIFERE (fora de metadados.gerado_em)")
    if not ok_md:
        print(f"--check: {caminho_md.name} DIFERE")
    return 1


# ------------------------------------------------------------------------------- CLI

# ! Alteração de IA - Revisar: linha de comando -- --saida escolhe a pasta de resultados da
# Fase 3 (ver caminhos.fase3), --saidas-3b lista pastas com avaliacao_fase3.json próprio da
# Fase 3-B, --pesos aponta para o JSON de pesos e --check regera e compara sem gravar.
# ! Motivo: os padrões (--saida fase3, --pesos EXP/pesos_decisao.json) rodam a decisão da
# corrida oficial sem argumento nenhum; --saidas-3b e --pesos só existem para apontar para
# outra pasta/config sem editar o script (mesmo padrão de comparar_fases.main/
# gerar_graficos_fase3.main).
def main() -> None:
    ap = argparse.ArgumentParser(
        description="Decide o modelo e o estado da biblioteca (L0..L3) de produção a partir "
                    "dos resultados oficiais da Fase 3 (regra pré-registrada, bootstrap, "
                    "Pareto e escore ponderado).")
    ap.add_argument("--saida", default="fase3",
                    help="subpasta dos resultados da Fase 3 (ver caminhos.fase3)")
    ap.add_argument("--saidas-3b", nargs="*", default=None,
                    help="pastas em resultados_alvo/ com avaliacao_fase3.json próprio da "
                        "Fase 3-B (ponte, cruzada, texto_max, inéditos)")
    ap.add_argument("--pesos", default=str(caminhos.AQUI / "pesos_decisao.json"),
                    help="JSON de pesos do escore ponderado")
    ap.add_argument("--check", action="store_true",
                    help="regera e compara com o arquivo existente (só metadados.gerado_em "
                        "pode diferir); código de saída 1 se diferente")
    args = ap.parse_args()

    print(caminhos.descricao())
    c3 = caminhos.fase3(args.saida)
    faltando = [nome for nome in ("avaliacao", "resumo", "comparacao")
               if not c3[nome].exists()]
    if faltando:
        raise SystemExit(f"faltam em {c3['raiz']}: {faltando} -- rode avaliar_fase3.py e "
                         "comparar_fases.py primeiro")

    pesos_cfg = json.loads(Path(args.pesos).read_text(encoding="utf-8"))
    comparacao = json.loads(c3["comparacao"].read_text(encoding="utf-8"))
    resumo_f3 = json.loads(c3["resumo"].read_text(encoding="utf-8"))
    avaliados_f3 = json.loads(c3["avaliacao"].read_text(encoding="utf-8"))

    saidas_3b = None
    if args.saidas_3b:
        saidas_3b = {}
        for nome in args.saidas_3b:
            c3_b = caminhos.fase3(nome)
            if c3_b["avaliacao"].exists():
                saidas_3b[nome] = c3_b
            else:
                print(f"sem 3-B em {nome}: {c3_b['avaliacao']} não existe")

    decisao = montar_decisao(comparacao, resumo_f3, avaliados_f3, pesos_cfg, saidas_3b, c3)
    decisao["metadados"]["saida"] = args.saida
    decisao["metadados"]["fontes"] = {
        "comparacao": str(c3["comparacao"]), "resumo": str(c3["resumo"]),
        "avaliacao": str(c3["avaliacao"]), "pesos": str(Path(args.pesos).resolve()),
    }

    caminho_json, caminho_md = _caminhos_decisao(c3)
    if args.check:
        raise SystemExit(conferir(caminho_json, caminho_md, decisao))

    gravar(caminho_json, caminho_md, decisao)

    venc = decisao["regra_36"]["vencedor"]
    print(f"\nVencedor (regra 36): "
         f"{venc['modelo'] + '/L' + str(venc['biblioteca_epoca']) if venc else '(nenhum)'}")
    for c in sorted(decisao["bootstrap"]["nos_36"]["combos"], key=lambda x: -x["p_top1"]):
        print(f"  P(top-1) {c['modelo']}/L{c['biblioteca_epoca']} = {c['p_top1']:.3f}")
    print(f"Não dominados (Pareto): {len(decisao['pareto']['nao_dominados'])}")
    esc = decisao["escore_ponderado"]["vencedor"]
    print(f"Vencedor (escore ponderado): "
         f"{esc['modelo'] + '/L' + str(esc['biblioteca_epoca']) if esc else '(nenhum)'}")
    print(f"\nDecisão em {caminho_json}\nTabela em {caminho_md}")


if __name__ == "__main__":
    main()
