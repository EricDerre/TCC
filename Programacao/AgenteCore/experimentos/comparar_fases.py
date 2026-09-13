#!/usr/bin/env python3
# ! Alteração de IA - Revisar: cria comparar_fases.py -- compara as três fases de teste (2-A
# Ryzen, 2-B i5-alvo, 3) por modelo, lendo os avaliacao.json já gravados por avaliar.py (2-A e
# 2-B) e o avaliacao_fase3.json/resumo_fase3.json já gravados por avaliar_fase3.py (Fase 3), e
# grava comparacao_fases.json e a tabela comparacao_fases.md dentro da pasta de saída da
# Fase 3 (caminhos.fase3(saida)).
# ! Motivo: as três fases foram avaliadas por avaliadores diferentes (avaliar.py agrega a 2-A
# e a 2-B por CONDIÇÃO de biblioteca; avaliar_fase3.py agrega a Fase 3 por ÉPOCA da
# biblioteca) e nenhum dos dois põe as três lado a lado -- a escolha do modelo final do TCC
# precisa do ganho A0->A2 (2-B), do ganho L0->L3 (Fase 3) e do risco de adesão cega (A5) na
# MESMA tabela, por modelo. Este módulo não reavalia nada: relê os três arquivos já fechados
# e só recalcula a acurácia balanceada (que a 2-A/2-B nunca calculou) com a MESMA função da
# Fase 3, para o número sair igual nas colunas que vêm de fases diferentes.
# ! Alteração de IA - Revisar: Fix round 1 da revisão da Tarefa 9 -- estende o negrito
# "melhor valor" das Tabelas 1-2 para a 3 (menor s/caso e menor tokens) e a 4 (menor em 5
# riscos, maior no teto A3; comparando MODELOS, não fases -- ver _tabela_riscos); a Tabela 5
# fica sem negrito (não há "melhor" entre duas fases comparadas); e troca o p-valor da
# Tabela 5 de `_n` (1 casa) para `_p` (4 casas + '*' quando p < 0,05).
# ! Motivo: a revisão apontou que `_n(p_mcnemar)` arredondava um p de 0,002 para "0,0",
# indistinguível de p=1,0 -- o número que decide se um Δ é ou não distinguível do acaso
# ficava ilegível. E o negrito só nas Tabelas 1-2 escondia, nas Tabelas 3-4, qual fase foi
# mais barata ou qual modelo teve menos risco -- a mesma pergunta que o negrito já respondia
# para o acerto.
"""Comparação entre as fases 2-A, 2-B e 3 por modelo: acerto pareado (2A_linear_ryzen, 2B_A0,
2B_A2, 2B_A3, F3_L0..L3), adesão cega (2B_A5), tentativas de decorar e autoenvenenamento
(Fase 3), e pareamentos caso a caso (McNemar exato) entre fases adjacentes. Grava
comparacao_fases.json (os números) e comparacao_fases.md (a mesma tabela pronta para colar
no Memorial -- nenhum número ali é digitado à mão).

Negrito no Markdown: Tabelas 1-2 (acerto) e 1b-2b (acurácia balanceada), o maior valor da
linha (entre fases, mesmo modelo); Tabela 3, o menor s/caso e o menor tokens de saída da linha
(em separado); Tabela 4, o menor valor da COLUNA (entre modelos) em 5 dos 6 riscos, e o maior
na coluna do teto A3; Tabela 5, nenhum (compara duas fases, não há "melhor" candidato).

Métrica primária: a coluna "F3 melhor" das Tabelas 1-2/1b-2b e o "melhor modelo da Fase 3" do
parágrafo por fase são escolhidos pela ACURÁCIA BALANCEADA (média do acerto por causa raiz),
não pelo acerto simples — o acerto simples pode ser inflado por um modelo que responde sempre
a causa mais frequente do recorte (onda final, achado I6)."""
import argparse
import json
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
# nas tabelas daqui (Δ, →, —) -- sem isso o script aborta com UnicodeEncodeError depois de já
# ter gravado os arquivos, e quem roda vê um traceback no lugar do resumo.
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


# --------------------------------------------------------------------- constantes

# ! Alteração de IA - Revisar: os 4 casos cujo texto no banco (banco_casos.py/
# banco_casos_extra.py) foi corrigido entre a Fase 2-B e a Fase 3.
# ! Motivo: achado 4.20 do Memorial -- sin-1/sin-2/semt-13 descreviam o sintoma "R$ NaN" e
# efe-13 "cartões duplicados", nenhum dos dois produzido por produtos_api.php de fato
# (teste_fixtures_corrigidos documenta a correção). A 2-B rodou com os fixtures ANTIGOS; a
# Fase 3 roda com os corrigidos. Comparar o acerto desses 4 ids entre a 2-B e a Fase 3
# misturaria enunciados diferentes sob o mesmo id de caso, então os pareamentos entre as duas
# fases excluem esses ids (conjunto "86" = 90 − 4).
CASOS_ALTERADOS_NA_FASE3 = ("sin-1", "sin-2", "semt-13", "efe-13")

# ! Alteração de IA - Revisar: nome fixo da máquina da Fase 2-A.
# ! Motivo: a 2-A rodou antes de executar_bateria.py passar a gravar maquina.json (a 2-B foi a
# primeira fase com esse registro -- ver caminhos.py), então não há arquivo para ler; é o
# único dado desta tabela que não sai de um arquivo, porque o arquivo nunca existiu.
MAQUINA_2A = "Ryzen 7 5800H"

# Condições da Fase 2-B usadas nas colunas: A0 (sem biblioteca, linha de base), A2 (com
# recuperação -- o que a Fase 3 também usa), A3 (o verbete de ouro sempre entregue -- o teto
# de acerto alcançável só com a biblioteca perfeita) e A5 (a causa plantada no contexto -- a
# adesão cega).
_CONDICOES_2B = ("A0", "A2", "A3", "A5")

# Colunas F3 na ordem das versões da biblioteca (L0..L3 = executar_fase3.EPOCAS_PADRAO + 1
# passadas de diagnóstico).
_EPOCAS_F3 = (0, 1, 2, 3)

# Ordem de preferência para a linha "representativa" da Tabela de riscos: o estado mais
# avançado da biblioteca que o modelo tem disponível, caindo para trás quando faltar.
_ORDEM_RISCO = ("F3_L3", "F3_L0", "2B_A2", "2B_A0", "2A_linear_ryzen")


# ------------------------------------------------------------------------ leitura

def _maquina_de(arquivo_avaliacao: Path) -> str | None:
    """! Alteração de IA - Revisar: lê o campo 'cpu' de maquina.json ao lado do avaliacao.json
    informado (mesma pasta de resultados), com encoding 'utf-8-sig'; None se o arquivo não
    existir.
    ! Motivo: a 2-B e a Fase 3 gravam maquina.json (executar_bateria.py/executar_fase3.py) --
    ler o nome da CPU do arquivo em vez de escrever a string à mão é o que evita a tabela
    mostrar a máquina errada se um dia a corrida rodar noutro notebook. 'utf-8-sig' e não
    'utf-8': resultados_alvo/maquina.json foi gravado por rodar_fase2b.ps1 (ConvertTo-Json |
    Out-File), que no Windows PowerShell 5.1 grava UTF-8 COM BOM por padrão (3 bytes EF BB BF
    antes do '{') -- lendo com 'utf-8' comum, json.loads aborta com 'Unexpected UTF-8 BOM'
    antes de a tabela sair; 'utf-8-sig' descarta o BOM quando ele existe e funciona igual a
    'utf-8' quando não existe (ex.: se um dia o arquivo for gravado em Python)."""
    arquivo = arquivo_avaliacao.parent / "maquina.json"
    if not arquivo.exists():
        return None
    return json.loads(arquivo.read_text(encoding="utf-8-sig")).get("cpu")


def carregar_2a(caminho: Path) -> list[dict]:
    """! Alteração de IA - Revisar: os registros de avaliacao.json da Fase 2-A (Ryzen) na
    condição A0, braço linear -- os únicos comparáveis com a 2-B e a Fase 3 (as duas rodam só
    o braço linear).
    ! Motivo: avaliacao.json da 2-A também tem as estratégias 'compilador' e 'dominio' (uma
    ablação que não existe nas fases seguintes) e alguns registros sem a chave 'condicao'
    (formato antigo, anterior a ela existir) -- sem os dois filtros a média da 2-A sairia
    sobre um conjunto de casos diferente do das outras colunas da mesma linha."""
    registros = json.loads(caminho.read_text(encoding="utf-8"))
    return [r for r in registros
            if r.get("condicao", "A0") == "A0" and r["estrategia"] == "linear"]


def carregar_2b(caminho: Path, condicao: str) -> list[dict]:
    """! Alteração de IA - Revisar: os registros de avaliacao.json da Fase 2-B (braço linear,
    a única condição que roda com biblioteca) numa condição -- A0, A2, A3 (teto) ou A5
    (adesão cega).
    ! Motivo: o mesmo arquivo tem as 6 condições (A0..A5) misturadas linha a linha -- sem o
    filtro por 'condicao' e 'estrategia', a coluna 2B_A2 incluiria também os diagnósticos de
    A0/A3/A5 do mesmo modelo, inflando o n e misturando condições diferentes na mesma
    média."""
    registros = json.loads(caminho.read_text(encoding="utf-8"))
    return [r for r in registros
            if r["condicao"] == condicao and r["estrategia"] == "linear"]


def carregar_fase3(c3: dict) -> list[dict]:
    """! Alteração de IA - Revisar: os registros de avaliacao_fase3.json da pasta de saída da
    Fase 3; lista vazia se a corrida ainda não existe.
    ! Motivo: comparar as fases pode acontecer ANTES de a Fase 3 ter rodado (ex.: só para
    conferir 2-A contra 2-B) -- lista vazia em vez de FileNotFoundError é o que permite ao
    script seguir e gravar os modelos só com as colunas 2-A/2-B, F3_* em null."""
    if not c3["avaliacao"].exists():
        return []
    return json.loads(c3["avaliacao"].read_text(encoding="utf-8"))


def carregar_particao(c3: dict) -> dict:
    """! Alteração de IA - Revisar: particao.json (regra, semente, contagens e {'casos':
    {id: {particao, classe, nivel, hash}}}); {} se a Fase 3 ainda não gravou a partição.
    ! Motivo: é o único arquivo que diz quais dos 90 ids são os 36 'de avaliação' (nunca
    entraram na biblioteca) -- sem ele, nos_36_avaliacao e os pareamentos '36'/'54' não têm
    como filtrar os casos, e {} devolve ids_avaliacao/ids_aprendizado vazios em vez de
    quebrar quando a Fase 3 ainda não rodou."""
    if not c3["particao"].exists():
        return {}
    return json.loads(c3["particao"].read_text(encoding="utf-8"))


def carregar_resumo_fase3(c3: dict) -> dict:
    """! Alteração de IA - Revisar: resumo_fase3.json inteiro; {} se a Fase 3 ainda não
    gravou o resumo.
    ! Motivo: só dois blocos dele são lidos aqui (documentacao para tentativas_de_decorar_F3,
    flips para autoenvenenamento_F3) -- os outros (pareado_vs_L0, cochran_q etc.) não têm
    equivalente nesta comparação entre fases e ficam só no relatório da própria Fase 3
    (avaliar_fase3.imprimir_resumo)."""
    if not c3["resumo"].exists():
        return {}
    return json.loads(c3["resumo"].read_text(encoding="utf-8"))


# --------------------------------------------------------------------- agregação (COL)

def _coluna(registros: list[dict], maquina: str | None,
           com_ancoragem: bool = True) -> dict | None:
    """! Alteração de IA - Revisar: agrega uma lista de registros já avaliados (2-A, 2-B ou
    Fase 3 -- as três compartilham os campos de avaliar.avaliar_registro) na estrutura COL do
    JSON de comparação: n, acerto e IC de Wilson, acurácia balanceada, mediana de segundos,
    média de tokens de saída, fora-do-conjunto, formato-ok-conteúdo-errado e, quando a
    condição tem biblioteca (com_ancoragem), citou_verbete/ouro_no_contexto. None (em vez de
    uma linha com n=0) sinaliza 'esta coluna não existe para este modelo'.
    ! Motivo: nenhuma das colunas de origem calcula acurácia balanceada por si (só
    avaliar_fase3 calcula, e só para a Fase 3) -- para comparar A0/A2/L0/L3 lado a lado com a
    MESMA métrica ela precisa ser recalculada aqui, com a função importada de avaliar_fase3
    (não reimplementada), para o número não divergir do que a Fase 3 já publica no resumo
    dela. citou_verbete/ouro_no_contexto saem None em A0 e na 2-A porque, sem biblioteca no
    contexto, os dois campos são sempre False por construção -- 0% ali mediria a ausência de
    biblioteca, não o comportamento do modelo."""
    n = len(registros)
    if n == 0:
        return None
    acertos = sum(1 for r in registros if r["causa_correta"])

    def pct(campo: str) -> float:
        return round(100 * sum(1 for r in registros if r[campo]) / n, 1)

    tempos = (r["segundos"] for r in registros)
    tokens = [r["tokens_saida"] for r in registros if r.get("tokens_saida") is not None]
    return {
        "n": n,
        "acerto_pct": round(100 * acertos / n, 1),
        "ic95": list(avaliar.wilson(acertos, n)),
        "acuracia_balanceada_pct": avaliar_fase3.acuracia_balanceada(
            [(r["causa_esperada"], r["causa_respondida"]) for r in registros]),
        "segundos_mediana": avaliar._mediana(tempos),
        "tokens_saida_medio": round(sum(tokens) / len(tokens)) if tokens else None,
        "fora_do_conjunto_pct": pct("fora_do_conjunto"),
        "formato_ok_conteudo_errado_pct": pct("formato_valido_conteudo_errado"),
        "hit3_pct": pct("ouro_no_contexto") if com_ancoragem else None,
        "citou_verbete_pct": pct("citou_verbete") if com_ancoragem else None,
        "maquina": maquina,
    }


def _por_epoca(fase3: list[dict], modelo: str) -> dict[int, list[dict]]:
    """! Alteração de IA - Revisar: {biblioteca_epoca: registros} de um modelo dentro dos
    avaliados da Fase 3.
    ! Motivo: montar_por_modelo e gerar_pareamentos precisam separar os diagnósticos de L0,
    L1, L2 e L3 do MESMO modelo repetidas vezes (uma para cada coluna F3_L*, outra para os
    pareamentos F3_L0×F3_L3) -- agrupar uma vez só aqui evita filtrar a lista de avaliados
    inteira de novo a cada coluna."""
    agrupado: dict[int, list[dict]] = defaultdict(list)
    for r in fase3:
        if r["modelo"] == modelo:
            agrupado[r["biblioteca_epoca"]].append(r)
    return agrupado


def _melhor_f3(colunas: dict[int, dict | None]) -> dict:
    """! Alteração de IA - Revisar: dentre as colunas F3_L0..L3 presentes, a de maior
    ACURÁCIA BALANCEADA (acuracia_balanceada_pct) -- {'biblioteca_epoca': None} quando
    nenhuma existe. Até a onda final (achado I6) o critério era acerto_pct.
    ! Motivo: é a coluna 'F3 melhor' das Tabelas 1-2 -- qual época de biblioteca deu o melhor
    diagnóstico, sem o leitor ter de comparar as 4 colunas anteriores à mão. A acurácia
    balanceada é a métrica primária do trabalho (avaliar_fase3.acuracia_balanceada: média do
    acerto por causa raiz presente no recorte); escolher pelo acerto simples premiaria a
    época em que o modelo mais respondeu a causa dominante do recorte, não a em que
    diagnosticou melhor. Em empate fica a época mais BAIXA (a ordem de iteração é 0..3 e
    max() preserva o primeiro máximo), porque afirmar que uma época mais tardia é melhor sem
    uma diferença medida seria uma alegação que o próprio número não sustenta."""
    presentes = {ep: col for ep, col in colunas.items() if col}
    if not presentes:
        return {"biblioteca_epoca": None}
    melhor_epoca = max(presentes, key=lambda ep: presentes[ep]["acuracia_balanceada_pct"])
    return {"biblioteca_epoca": melhor_epoca, **presentes[melhor_epoca]}


def _tentativas_de_decorar(resumo_f3: dict, modelo: str) -> dict | None:
    """! Alteração de IA - Revisar: {'total', 'por_epoca': {'1': n, '2': n, '3': n}} de
    resumo_fase3.json['documentacao'] -- None se a Fase 3 não tem esse modelo
    (documentacao_por_epoca de avaliar_fase3.py já soma motivos_rejeicao['copia_do_caso'] +
    ['copia_do_caso_acumulada'] nesse campo).
    ! Motivo: a chave vem convertida para string (str(d['epoca'])) porque JSON não tem chave
    inteira -- gravar com chave int e reler dá chave string de volta (json.dump converte na
    escrita), e o dicionário em memória ficaria diferente do que está no arquivo. Construir já
    com string evita essa divergência entre o que a função devolve e o que
    comparacao_fases.json guarda."""
    linhas = [d for d in resumo_f3.get("documentacao", []) if d["modelo"] == modelo]
    if not linhas:
        return None
    por_epoca = {str(d["epoca"]): d["tentativas_de_decorar"] for d in linhas}
    return {"total": sum(por_epoca.values()), "por_epoca": por_epoca}


def _autoenvenenamento(resumo_f3: dict, modelo: str) -> dict | None:
    """! Alteração de IA - Revisar: {'L0→L1': pct, 'L1→L2': pct, 'L2→L3': pct} de
    resumo_fase3.json['flips'], restrito à partição 'avaliacao' (os 36 casos que nunca entram
    na biblioteca) -- None se a Fase 3 não tem esse modelo.
    ! Motivo: 'flips' também tem a linha da partição 'todos' e da 'aprendizado' -- sem o
    filtro por partição=='avaliacao', a Tabela de riscos mostraria o autoenvenenamento medido
    sobre casos que o próprio modelo usou para editar a biblioteca, que é o pior lugar para
    medir generalização, não o melhor."""
    linhas = [f for f in resumo_f3.get("flips", [])
              if f["modelo"] == modelo and f["particao"] == "avaliacao"]
    if not linhas:
        return None
    return {f["transicao"]: f["autoenvenenamento_pct"] for f in linhas}


def montar_por_modelo(modelo: str, regs_2a: list[dict], regs_2b: dict[str, list[dict]],
                      fase3: list[dict], resumo_f3: dict, ids_avaliacao: set[str],
                      maquina_2a: str | None, maquina_2b: str | None,
                      maquina_f3: str | None) -> dict:
    """! Alteração de IA - Revisar: monta o bloco por_modelo[modelo] inteiro -- nos_90 e
    nos_36_avaliacao (mesmas 7 colunas, a segunda restrita aos ids da partição 'avaliacao'),
    adesão cega (A5), teto (A3), tentativas de decorar e autoenvenenamento (Fase 3).
    ! Motivo: nos_90 e nos_36_avaliacao precisam ser EXATAMENTE as mesmas colunas calculadas
    do mesmo jeito (só o filtro de casos muda) -- calculá-las com a mesma função interna
    (bloco()) em vez de duas implementações evita a segunda ganhar uma coluna que a primeira
    não tem, o que é o mesmo cuidado de avaliar_fase3._com_particao_todos."""
    por_epoca = _por_epoca(fase3, modelo)

    def bloco(filtro) -> dict:
        colunas = {
            "2A_linear_ryzen": _coluna(filtro(regs_2a), maquina_2a, com_ancoragem=False),
            "2B_A0": _coluna(filtro(regs_2b.get("A0", [])), maquina_2b, com_ancoragem=False),
            "2B_A2": _coluna(filtro(regs_2b.get("A2", [])), maquina_2b),
            "2B_A3": _coluna(filtro(regs_2b.get("A3", [])), maquina_2b),
        }
        for epoca in _EPOCAS_F3:
            colunas[f"F3_L{epoca}"] = _coluna(filtro(por_epoca.get(epoca, [])), maquina_f3)
        colunas["F3_melhor"] = _melhor_f3(
            {epoca: colunas[f"F3_L{epoca}"] for epoca in _EPOCAS_F3})
        return colunas

    nos_90 = bloco(lambda regs: regs)
    nos_36 = bloco(lambda regs: [r for r in regs if r["caso"] in ids_avaliacao])

    a5 = regs_2b.get("A5", [])
    plantados = [r for r in a5 if r.get("causa_plantada")]
    adesao_cega = (round(100 * sum(1 for r in plantados if r["seguiu_causa_plantada"])
                         / len(plantados), 1) if plantados else None)
    teto = nos_90["2B_A3"]["acerto_pct"] if nos_90["2B_A3"] else None

    return {
        "nos_90": nos_90, "nos_36_avaliacao": nos_36,
        "adesao_cega_2B_A5_pct": adesao_cega, "teto_2B_A3_pct": teto,
        "tentativas_de_decorar_F3": _tentativas_de_decorar(resumo_f3, modelo),
        "autoenvenenamento_F3": _autoenvenenamento(resumo_f3, modelo),
    }


# --------------------------------------------------------------------- pareamentos

def _pareavel(mesma_maquina: bool, mesmos_fixtures: bool) -> str:
    """! Alteração de IA - Revisar: frase curta da coluna 'pareável?' -- montada a partir das
    duas condições que tornam um Δ diretamente comparável (mesma máquina para o tempo, mesmos
    enunciados de caso para o acerto).
    ! Motivo: só a 2-A roda em máquina diferente (Ryzen, contra o i5-alvo da 2-B e da Fase 3)
    e só os 4 ids do achado 4.20 mudam de enunciado entre a 2-B e a Fase 3 -- a frase sai
    sozinha das duas condições, em vez de listar à mão qual par tem qual ressalva no texto do
    Memorial."""
    acerto = "acerto sim" if mesmos_fixtures else "acerto com ressalva (fixtures diferentes)"
    tempo = "tempo sim" if mesma_maquina else "tempo não (máquina diferente)"
    return f"{acerto}; {tempo}"


def _parear(modelo: str, a_nome: str, b_nome: str, a_regs: list[dict], b_regs: list[dict],
           conjunto: str, mesma_maquina: bool, mesmos_fixtures: bool = True,
           excluir: tuple[str, ...] = ()) -> dict | None:
    """! Alteração de IA - Revisar: pareamento caso a caso (McNemar exato) entre duas colunas
    do MESMO modelo -- intersecta os ids de caso presentes nos dois lados (excluindo os de
    `excluir`) e devolve n, acerto de cada lado, Δ pp, b/c e p; None se não sobrar caso comum.
    ! Motivo: é o mesmo desenho de avaliar.comparar_com_base e avaliar_fase3.pareado_vs_l0
    (uma corrida por condição/época, McNemar é o teste indicado por Dietterich 1998 para esse
    desenho), agora entre FASES em vez de entre condições da mesma fase ou épocas da mesma
    biblioteca -- por isso a conta é refeita aqui em vez de chamar uma das duas funções
    prontas, que pressupõem que os dois lados venham da mesma lista de avaliados."""
    casos_a = {r["caso"]: r["causa_correta"] for r in a_regs if r["caso"] not in excluir}
    casos_b = {r["caso"]: r["causa_correta"] for r in b_regs if r["caso"] not in excluir}
    comuns = sorted(set(casos_a) & set(casos_b))
    n = len(comuns)
    if n == 0:
        return None
    b = sum(1 for c in comuns if casos_b[c] and not casos_a[c])
    cc = sum(1 for c in comuns if casos_a[c] and not casos_b[c])
    acerto_a = round(100 * sum(casos_a[c] for c in comuns) / n, 1)
    acerto_b = round(100 * sum(casos_b[c] for c in comuns) / n, 1)
    return {
        "modelo": modelo, "a": a_nome, "b": b_nome, "conjunto": conjunto, "n_comuns": n,
        "acerto_a_pct": acerto_a, "acerto_b_pct": acerto_b,
        "delta_pp": round(acerto_b - acerto_a, 1),
        "b_so_b": b, "c_so_a": cc, "p_mcnemar": avaliar.mcnemar_exato(b, cc),
        "mesma_maquina": mesma_maquina, "mesmos_fixtures": mesmos_fixtures,
        "pareavel": _pareavel(mesma_maquina, mesmos_fixtures),
    }


def gerar_pareamentos(modelo: str, regs_2a: list[dict], regs_2b: dict[str, list[dict]],
                      fase3: list[dict], ids_avaliacao: set[str],
                      ids_aprendizado: set[str]) -> list[dict]:
    """! Alteração de IA - Revisar: as 6 comparações do desenho da Tarefa 9, por modelo --
    2A×2B_A0 e 2B_A0×2B_A2 nos 90 casos; 2B_A2×F3_L0 nos 86 (excluindo os 4 ids do achado
    4.20) e nos 36 de avaliação; F3_L0×F3_L3 nos 36 de avaliação e nos 54 de aprendizado.
    ! Motivo: é a lista de pares que decide 'o ganho de A0 para A2 se sustenta contra a
    biblioteca original da Fase 3?' e 'o que a biblioteca editada pelo modelo ganhou generaliza
    para os 36 casos que ele nunca viu?' -- cada par só existe se houver caso comum (_parear
    devolve None e é descartado), então um modelo sem corrida de Fase 3 sai só com os dois
    primeiros pares (2A×2B_A0, 2B_A0×2B_A2)."""
    por_epoca = _por_epoca(fase3, modelo)
    l0, l3 = por_epoca.get(0, []), por_epoca.get(3, [])
    a0, a2 = regs_2b.get("A0", []), regs_2b.get("A2", [])

    def so(regs: list[dict], ids: set[str]) -> list[dict]:
        return [r for r in regs if r["caso"] in ids]

    candidatos = [
        _parear(modelo, "2A_linear_ryzen", "2B_A0", regs_2a, a0, "90", mesma_maquina=False),
        _parear(modelo, "2B_A0", "2B_A2", a0, a2, "90", mesma_maquina=True),
        _parear(modelo, "2B_A2", "F3_L0", a2, l0, "86", mesma_maquina=True,
               excluir=CASOS_ALTERADOS_NA_FASE3),
        # ! Alteração de IA - Revisar: o pareamento nos 36 também exclui os 4 ids do achado
        # 4.20 -- onda final (achado M13).
        # ! Motivo: hoje os 4 caem em 'aprendizado' (teste_particao confere), então o filtro
        # não muda nada; mas se a semente ou o banco mudarem e um deles for para 'avaliacao',
        # o pareamento 2B_A2 x F3_L0 nos 36 passaria a comparar enunciados diferentes sob o
        # mesmo id, exatamente o que o conjunto '86' já evita.
        _parear(modelo, "2B_A2", "F3_L0", so(a2, ids_avaliacao), so(l0, ids_avaliacao),
               "36", mesma_maquina=True, excluir=CASOS_ALTERADOS_NA_FASE3),
        _parear(modelo, "F3_L0", "F3_L3", so(l0, ids_avaliacao), so(l3, ids_avaliacao),
               "36", mesma_maquina=True),
        _parear(modelo, "F3_L0", "F3_L3", so(l0, ids_aprendizado), so(l3, ids_aprendizado),
               "54", mesma_maquina=True),
    ]
    return [p for p in candidatos if p is not None]


# --------------------------------------------------------------------- montagem geral

def montar_comparacao(caminho_2a: Path, caminho_2b: Path, c3: dict) -> dict:
    """! Alteração de IA - Revisar: monta o dicionário completo de comparacao_fases.json --
    metadados, por_modelo (uma entrada por modelo presente em 2-A/2-B/Fase 3) e pareamentos.
    ! Motivo: a lista de modelos não é fixa no código -- sai da UNIÃO dos modelos com corrida
    de Fase 3 (colunas completas) com os modelos que só rodaram 2-A/2-B (ex.: phi4-mini:3.8b e
    qwen2.5-coder:1.5b, que o desenho da Fase 3 não leva adiante por serem mais fracos que os
    4 escolhidos -- ver decisão em claude-memoria); calcular a lista em vez de digitá-la é o
    que faz o script continuar certo se a Fase 3 rodar com um subconjunto diferente de
    modelos."""
    regs_2a = carregar_2a(caminho_2a)
    regs_2b = {cond: carregar_2b(caminho_2b, cond) for cond in _CONDICOES_2B}
    fase3 = carregar_fase3(c3)
    particao = carregar_particao(c3)
    resumo_f3 = carregar_resumo_fase3(c3)

    casos_particao = particao.get("casos", {})
    ids_avaliacao = {cid for cid, v in casos_particao.items() if v["particao"] == "avaliacao"}
    ids_aprendizado = {cid for cid, v in casos_particao.items()
                       if v["particao"] == "aprendizado"}

    maquina_2a = MAQUINA_2A
    maquina_2b = _maquina_de(caminho_2b)
    maquina_f3 = _maquina_de(c3["avaliacao"]) or maquina_2b

    modelos_f3 = sorted({r["modelo"] for r in fase3})
    # Pressupõe que a condição A0 da 2-B é o SUPERCONJUNTO de modelos do projeto -- todo
    # modelo que rodou a 2-A ou a Fase 3 também rodou a 2-B A0 (é a condição em que TODO
    # modelo entra, nem que seja só como linha de base); um modelo que só tivesse rodado a
    # 2-A ou só a Fase 3, sem nunca ter passado pela 2-B A0, ficaria fora de `modelos_extra`.
    modelos_extra = sorted({r["modelo"] for r in regs_2b["A0"]} - set(modelos_f3))
    modelos = modelos_f3 + modelos_extra

    por_modelo, pareamentos = {}, []
    for modelo in modelos:
        regs_2a_m = [r for r in regs_2a if r["modelo"] == modelo]
        regs_2b_m = {cond: [r for r in regs if r["modelo"] == modelo]
                    for cond, regs in regs_2b.items()}
        por_modelo[modelo] = montar_por_modelo(
            modelo, regs_2a_m, regs_2b_m, fase3, resumo_f3, ids_avaliacao,
            maquina_2a, maquina_2b, maquina_f3)
        pareamentos += gerar_pareamentos(modelo, regs_2a_m, regs_2b_m, fase3,
                                         ids_avaliacao, ids_aprendizado)

    return {
        "metadados": {
            "gerado_em": datetime.now().isoformat(timespec="seconds"),
            "fontes": {"2a": str(caminho_2a), "2b": str(caminho_2b),
                      "f3": str(c3["avaliacao"])},
            "casos_alterados_na_fase3": list(CASOS_ALTERADOS_NA_FASE3),
            "n_avaliacao": len(ids_avaliacao),
        },
        "por_modelo": por_modelo,
        "pareamentos": pareamentos,
    }


# ---------------------------------------------------------------------------- Markdown

def _n(v) -> str:
    """! Alteração de IA - Revisar: formata um número (ou None) no padrão do Memorial --
    vírgula decimal, 1 casa, '—' quando o valor não foi medido.
    ! Motivo: é a porta de formatação de todo número do Markdown que NÃO é p-valor (para
    p-valor, ver _p) -- 1 casa é o suficiente para acerto%, Δ pp, segundos e tokens, mas
    arredondaria um p pequeno (0,002) para "0,0", que é ilegível para julgar significância;
    por isso o p tem formatador próprio, com mais casas."""
    if v is None:
        return "—"
    if isinstance(v, float):
        return f"{v:.1f}".replace(".", ",")
    return str(v)


def _p(v: float | None) -> str:
    """! Alteração de IA - Revisar: p-valor com 4 casas decimais e vírgula, mais um '*' colado
    (sem espaço) quando p < 0,05; '—' se v for None.
    ! Motivo: _n arredonda em 1 casa, o que faz um p de 0,002 (Tabela 5, McNemar exato) sair
    como "0,0" -- indistinguível de p=0,04 ou p=1,0, justamente os casos em que a tabela
    precisa dizer se a diferença é ou não distinguível do acaso. O '*' colado ao valor (não
    precedido de espaço) repete a convenção já usada em avaliar.py (`p={valor}{sig}`) e em
    avaliar_fase3.imprimir_resumo (`p_holm={... }{marca}`), para o mesmo p ser lido do mesmo
    jeito nas três fases."""
    if v is None:
        return "—"
    texto = f"{v:.4f}".replace(".", ",")
    return f"{texto}*" if v < 0.05 else texto


def _pct(v) -> str:
    """! Alteração de IA - Revisar: _n(v) com '%' -- '—' já sai de _n quando v é None.
    ! Motivo: toda célula de percentual das Tabelas 3-4 passa por aqui em vez de concatenar
    '%' à mão em cada tabela, para o símbolo não faltar (ou sobrar num '—%') em nenhuma."""
    return "—" if v is None else f"{_n(v)}%"


def _ic(col: dict | None) -> str:
    """! Alteração de IA - Revisar: '[lo–hi]' do intervalo de Wilson de uma COL; '—' se a
    coluna não existir (col é None).
    ! Motivo: col['ic95'] é a lista [lo, hi] que avaliar.wilson devolve -- ler os dois limites
    e formatar aqui em vez de em cada chamador é o que garante o mesmo travessão de intervalo
    (–, não -) nas 3 tabelas que mostram IC."""
    if not col:
        return "—"
    lo, hi = col["ic95"]
    return f"[{_n(lo)}–{_n(hi)}]"


def _celula_acerto(col: dict | None) -> str:
    """! Alteração de IA - Revisar: 'acerto% [IC]' de uma COL para a Tabela 1/2; '—' se a
    coluna não existir.
    ! Motivo: é o texto que aparece em toda célula das duas tabelas de acerto -- calculado
    numa função só para as duas tabelas (nos_90 e nos_36_avaliacao) nunca divergirem no
    formato."""
    return "—" if not col else f"{_n(col['acerto_pct'])}% {_ic(col)}"


def _com_negrito(pares: list[tuple[str, float | None]],
                 direcao: str = "maior") -> list[str]:
    """! Alteração de IA - Revisar: dado (texto, valor) por célula de uma linha OU coluna,
    devolve os textos com '**negrito**' no(s) de valor mais favorável -- MAIOR (`direcao=
    "maior"`, o padrão) ou MENOR (`direcao="menor"`); os None ficam de fora da comparação e
    saem sem marcação; em empate, todas as células no valor extremo saem em negrito.
    ! Motivo: a regra "negrito no melhor valor" da Tarefa 9 (Fix round 1, item 1) não tem uma
    direção só -- acerto% e teto A3% são melhores quanto MAIORES (Tabelas 1, 2 e a coluna de
    teto na Tabela 4), enquanto s/caso, tokens de saída, fora-do-conjunto%, formato-errado%,
    adesão cega%, tentativas de decorar e autoenvenenamento são melhores quanto MENORES
    (Tabela 3 e o resto da Tabela 4). Um parâmetro de direção evita duplicar esta função uma
    vez para cada sentido -- e funciona tanto comparando as colunas de uma LINHA (Tabelas 1-3,
    o mesmo modelo em fases diferentes) quanto as linhas de uma COLUNA (Tabela 4, o mesmo
    risco em modelos diferentes): a função só enxerga a lista de pares, não o eixo da tabela."""
    validos = [v for _, v in pares if v is not None]
    if not validos:
        return [t for t, _ in pares]
    extremo = max(validos) if direcao == "maior" else min(validos)
    return [f"**{t}**" if v == extremo else t for t, v in pares]


_COLUNAS_ACERTO = ("2A_linear_ryzen", "2B_A0", "2B_A2", "F3_L0", "F3_L3")

# Legenda das Tabelas 1-2/1b-2b, impressa uma vez depois delas (ver gerar_markdown).
_LEGENDA_ACERTO = (
    "_Acerto = causa raiz correta, com IC de Wilson a 95%; acurácia balanceada = média do "
    "acerto por causa raiz presente no recorte (avaliar_fase3.acuracia_balanceada), a "
    "métrica primária do trabalho. **F3 melhor** = a versão da biblioteca (L0..L3) com a "
    "maior acurácia balanceada do modelo (em empate, a mais baixa) — a mesma versão nas "
    "tabelas de acerto e de acurácia balanceada. A média do rodapé diz quantos modelos "
    "entram em cada coluna quando o número difere entre elas._")


def _celula_metrica(col: dict | None, metrica: str) -> str:
    """! Alteração de IA - Revisar: célula de uma COL para a métrica pedida -- 'acerto% [IC]'
    para acerto_pct (o IC de Wilson é do acerto simples) e só 'x%' para a acurácia
    balanceada; '—' sem coluna. Onda final (achado I6).
    ! Motivo: _tabela_acerto passou a gerar também as tabelas de acurácia balanceada, e o
    IC de Wilson não vale para ela (é o intervalo de uma proporção simples, não de uma média
    de proporções) -- mostrar o IC do acerto ao lado da balanceada seria colar um intervalo
    de outra métrica."""
    if not col:
        return "—"
    if metrica == "acerto_pct":
        return _celula_acerto(col)
    return f"{_n(col[metrica])}%"


def _modelos(n: int) -> str:
    """! Alteração de IA - Revisar: '1 modelo' / 'N modelos' para o rodapé de média.
    ! Motivo: o rodapé antigo dizia 'N modelo(s) com Fase 3' para todas as colunas, mas a
    média de 2-A/2-B inclui também os modelos SEM Fase 3 (phi4-mini, os 1.5b) -- o N impresso
    só valia para a coluna F3 melhor; ver _tabela_acerto."""
    return f"{n} modelo" + ("s" if n != 1 else "")


def _tabela_acerto(titulo: str, por_modelo: dict, chave_bloco: str,
                   metrica: str = "acerto_pct") -> list[str]:
    """! Alteração de IA - Revisar: Tabela 'Acerto por modelo e fase' (ou 'Acurácia
    balanceada por modelo e fase', com metrica='acuracia_balanceada_pct') -- nos_90 ou
    nos_36_avaliacao conforme `chave_bloco`, com rodapé de média por coluna que diz o número
    de modelos de CADA coluna quando ele difere entre elas.
    ! Motivo: são as Tabelas 1 e 2 do briefing da Tarefa 9 e, desde a onda final (achado
    I6), as 1b e 2b com a métrica primária -- a mesma função gera as quatro (só trocam
    chave_bloco e metrica) para as colunas nunca divergirem entre os recortes. O rodapé
    antigo rotulava a média de todas as colunas como 'N modelo(s) com Fase 3', mas as
    colunas 2-A/2-B somam também os modelos que não rodaram a Fase 3 (item 8 da onda final):
    agora, se todas as colunas têm o mesmo N, ele vai no rótulo; senão cada célula diz o seu.
    A coluna 'F3 melhor' é a versão escolhida por _melhor_f3 (acurácia balanceada) nas duas
    métricas, para o leitor achar a MESMA época nas duas tabelas."""
    linhas = [
        f"### {titulo}", "",
        "| Modelo | 2-A linear (Ryzen) | 2-B A0 | 2-B A2 | F3 L0 | F3 L3 | F3 melhor |",
        "|---|---|---|---|---|---|---|",
    ]
    somas: dict[str, list[float]] = defaultdict(list)
    somas_melhor: list[float] = []
    for modelo, dados in sorted(por_modelo.items()):
        bloco = dados[chave_bloco]
        valores = [bloco[c][metrica] if bloco[c] else None for c in _COLUNAS_ACERTO]
        melhor = bloco["F3_melhor"]
        tem_f3 = melhor.get("biblioteca_epoca") is not None
        melhor_txt = (f"{_celula_metrica(melhor, metrica)} (L{melhor['biblioteca_epoca']})"
                      if tem_f3 else "—")
        textos = [_celula_metrica(bloco[c], metrica) for c in _COLUNAS_ACERTO] + [melhor_txt]
        textos = _com_negrito(list(zip(textos, valores + [
            melhor.get(metrica) if tem_f3 else None])))
        for c, v in zip(_COLUNAS_ACERTO, valores):
            if v is not None:
                somas[c].append(v)
        if tem_f3:
            somas_melhor.append(melhor[metrica])
        linhas.append(f"| {modelo} | " + " | ".join(textos) + " |")
    listas = [somas[c] for c in _COLUNAS_ACERTO] + [somas_melhor]
    medias = [round(sum(vs) / len(vs), 1) if vs else None for vs in listas]
    contagens = [len(vs) for vs in listas]
    if len(set(contagens)) == 1:
        rotulo = f"**Média ({_modelos(contagens[0])})**"
        celulas = [_pct(m) for m in medias]
    else:
        rotulo = "**Média**"
        celulas = ["—" if m is None else f"{_pct(m)} ({_modelos(n)})"
                   for m, n in zip(medias, contagens)]
    linhas.append(f"| {rotulo} | " + " | ".join(celulas) + " |")
    linhas.append("")
    return linhas


def _tabela_custo(por_modelo: dict) -> list[str]:
    """! Alteração de IA - Revisar: Tabela 'Custo e prolixidade' -- s/caso mediana e tokens
    de saída médios por coluna, nos 90 casos; negrito no MENOR s/caso e no MENOR tokens de
    saída da linha (Fix round 1, item 1 -- os dois são calculados e negritados em separado,
    porque a coluna mais barata em tempo não precisa ser a mais concisa em tokens).
    ! Motivo: é a Tabela 3 do briefing -- a coluna 2-A leva '*' no cabeçalho porque o achado
    4.26 mediu que o tempo NÃO reproduz entre Ryzen e i5-alvo (o acerto sim); marcar aqui é o
    que impede alguém comparar segundos de máquinas diferentes como se fossem a mesma
    medição. O negrito segue a mesma leitura das Tabelas 1-2 (o melhor valor NESTA linha,
    entre as fases desta coluna), só que 'melhor' aqui é o MENOR (menos tempo, menos texto),
    daí `_com_negrito(..., direcao="menor")` em vez do padrão."""
    linhas = [
        "### Custo e prolixidade", "",
        "| Modelo | 2-A linear (Ryzen)* | 2-B A0 | 2-B A2 | F3 L0 | F3 L3 |",
        "|---|---|---|---|---|---|",
    ]
    for modelo, dados in sorted(por_modelo.items()):
        bloco = dados["nos_90"]
        colunas = [bloco.get(c) for c in _COLUNAS_ACERTO]
        segs_txt = _com_negrito(
            [(_n(col["segundos_mediana"]) if col else "—",
              col["segundos_mediana"] if col else None) for col in colunas],
            direcao="menor")
        toks_txt = _com_negrito(
            [(_n(col["tokens_saida_medio"]) if col else "—",
              col["tokens_saida_medio"] if col else None) for col in colunas],
            direcao="menor")
        celulas = [("—" if not col else f"{s} s / {t} tok")
                  for col, s, t in zip(colunas, segs_txt, toks_txt)]
        linhas.append(f"| {modelo} | " + " | ".join(celulas) + " |")
    linhas.append("")
    return linhas


def _coluna_representativa(bloco: dict) -> dict | None:
    """! Alteração de IA - Revisar: a coluna mais avançada disponível para um modelo
    (F3_L3 > F3_L0 > 2B_A2 > 2B_A0 > 2A) -- usada na Tabela de riscos.
    ! Motivo: fora_do_conjunto_pct e formato_ok_conteudo_errado_pct existem em toda coluna,
    mas o briefing pede UM número por risco por modelo, não uma célula por coluna -- ler o
    estado mais avançado da biblioteca que o modelo alcançou é o que dá o retrato mais
    recente do comportamento dele, em vez de repetir a leitura em 5 colunas."""
    for chave in _ORDEM_RISCO:
        if bloco.get(chave):
            return bloco[chave]
    return None


def _tabela_riscos(por_modelo: dict) -> list[str]:
    """! Alteração de IA - Revisar: Tabela 'Modos de falha e riscos' -- fora do conjunto e
    formato-ok-conteúdo-errado da coluna mais avançada disponível (ver
    _coluna_representativa), adesão cega (A5) e teto (A3) sempre da 2-B, tentativas de
    decorar e autoenvenenamento L2→L3 sempre da Fase 3; negrito no melhor valor de cada
    RISCO (cada coluna desta tabela), comparando os MODELOS -- não entre fases como nas
    Tabelas 1-3 (Fix round 1, item 1).
    ! Motivo: é a Tabela 4 do briefing -- adesão cega e teto são medidas exclusivas da 2-B
    (a Fase 3 não roda A5/A3) e tentativas de decorar/autoenvenenamento são exclusivas da
    Fase 3 (a 2-B não edita a biblioteca), então cada uma lê sempre da mesma fonte em vez de
    tentar achar a 'melhor disponível' como fora_do_conjunto/formato_errado fazem. O negrito
    é por COLUNA (não por linha, como nas Tabelas 1-3) porque aqui cada linha tem 6
    métricas de UNIDADES DIFERENTES (%, contagem) -- comparar 'fora do conjunto' com
    'tentativas de decorar' dentro da mesma linha não tem resposta; a comparação que faz
    sentido é 'qual modelo tem o menor fora-do-conjunto', que é a mesma pergunta lida por
    coluna. Cinco das seis colunas são melhores quanto MENORES (menos erro, menos risco);
    o teto A3 é melhor quanto MAIOR (o teto é o acerto alcançável com a biblioteca perfeita,
    então mais alto é melhor, não pior)."""
    modelos = sorted(por_modelo)

    def risco(modelo: str, campo: str) -> float | None:
        col = _coluna_representativa(por_modelo[modelo]["nos_90"])
        return col[campo] if col else None

    fora_vals = [risco(m, "fora_do_conjunto_pct") for m in modelos]
    formato_vals = [risco(m, "formato_ok_conteudo_errado_pct") for m in modelos]
    adesao_vals = [por_modelo[m]["adesao_cega_2B_A5_pct"] for m in modelos]
    teto_vals = [por_modelo[m]["teto_2B_A3_pct"] for m in modelos]
    decorar_vals = [(por_modelo[m]["tentativas_de_decorar_F3"] or {}).get("total")
                    for m in modelos]
    auto_vals = [(por_modelo[m]["autoenvenenamento_F3"] or {}).get("L2→L3")
                for m in modelos]

    fora_txt = _com_negrito([(_pct(v), v) for v in fora_vals], direcao="menor")
    formato_txt = _com_negrito([(_pct(v), v) for v in formato_vals], direcao="menor")
    adesao_txt = _com_negrito([(_pct(v), v) for v in adesao_vals], direcao="menor")
    teto_txt = _com_negrito([(_pct(v), v) for v in teto_vals], direcao="maior")
    decorar_txt = _com_negrito([(_n(v), v) for v in decorar_vals], direcao="menor")
    auto_txt = _com_negrito([(_pct(v), v) for v in auto_vals], direcao="menor")

    linhas = [
        "### Modos de falha e riscos", "",
        "| Modelo | Fora do conjunto % | Formato ok / conteúdo errado % | Adesão cega "
        "A5 % | Teto A3 % | Tentativas de decorar (F3) | Autoenvenenamento L2→L3 "
        "(F3, 36 casos) % |",
        "|---|---|---|---|---|---|---|",
    ]
    for i, modelo in enumerate(modelos):
        linhas.append(f"| {modelo} | {fora_txt[i]} | {formato_txt[i]} | {adesao_txt[i]} | "
                      f"{teto_txt[i]} | {decorar_txt[i]} | {auto_txt[i]} |")
    linhas.append("")
    return linhas


def _tabela_pareamentos(pareamentos: list[dict]) -> list[str]:
    """! Alteração de IA - Revisar: Tabela 'Pareamentos' -- uma linha por comparação de
    gerar_pareamentos, na ordem em que foram geradas (por modelo, depois pelas 6 comparações
    do desenho); SEM negrito (Fix round 1, item 1) -- cada linha compara duas FASES
    diferentes, não é um conjunto de valores do mesmo modelo onde um seja "o melhor".
    ! Motivo: é a Tabela 5 do briefing -- transcreve cada dicionário de pareamento numa linha
    sem recalcular nada, para o número da tabela ser garantidamente o mesmo do JSON. O p usa
    o formatador `_p` (4 casas + '*' se p < 0,05), não `_n` (Fix round 1, item 2): `_n`
    arredondaria em 1 casa e um p de 0,002 sairia "0,0", indistinguível de p=1,0 -- justamente
    o número que diz se o Δ da linha é ou não distinguível do acaso."""
    linhas = [
        "### Pareamentos", "",
        "_Sem negrito nesta tabela: cada linha compara duas fases diferentes do MESMO "
        "modelo (ex.: 2-B A2 × Fase 3 L0) -- não há \"melhor valor\" entre `a` e `b`, só um "
        "Δ e um p que dizem se a diferença é grande e se é distinguível do acaso._",
        "",
        "| Modelo | a | b | Conjunto | n | Δ pp | b/c | p | Pareável? |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for p in pareamentos:
        linhas.append(f"| {p['modelo']} | {p['a']} | {p['b']} | {p['conjunto']} | "
                      f"{p['n_comuns']} | {_n(p['delta_pp'])} | {p['b_so_b']}/{p['c_so_a']} "
                      f"| {_p(p['p_mcnemar'])} | {p['pareavel']} |")
    linhas.append("")
    return linhas


def _melhor(por_modelo: dict, chave: str) -> tuple[str | None, float | None]:
    """! Alteração de IA - Revisar: (modelo, acerto_pct) da coluna `chave` de nos_90 com o
    maior acerto -- (None, None) se nenhum modelo tiver essa coluna.
    ! Motivo: é o 'melhor modelo e acerto' que o parágrafo por fase cita para a 2-A
    (2A_linear_ryzen) e a 2-B (2B_A2) -- calculado sobre nos_90 em vez de digitado, para o
    parágrafo nunca citar um modelo que a tabela ao lado não sustenta."""
    candidatos = [(m, d["nos_90"][chave]["acerto_pct"]) for m, d in por_modelo.items()
                 if d["nos_90"].get(chave)]
    return max(candidatos, key=lambda x: x[1]) if candidatos else (None, None)


def _melhor_f3_geral(por_modelo: dict) -> tuple[str | None, float | None, float | None,
                                                int | None]:
    """! Alteração de IA - Revisar: (modelo, acurácia balanceada, acerto_pct, época) do
    melhor 'F3_melhor' entre os modelos com Fase 3 -- escolhido pela acurácia balanceada,
    o mesmo critério de _melhor_f3 (onda final, achado I6).
    ! Motivo: 'o melhor modelo da Fase 3' não é necessariamente o de maior acerto em L3 --
    _melhor_f3 já escolheu, por modelo, a época de maior acurácia balanceada; aqui só falta
    escolher o modelo entre esses melhores, com a MESMA métrica, para o parágrafo dizer
    'modelo X, B% de acurácia balanceada em Lz' com o z certo. O acerto simples vai junto
    como informação, não como critério."""
    candidatos = [(m, d["nos_90"]["F3_melhor"]) for m, d in por_modelo.items()
                 if d["nos_90"]["F3_melhor"].get("biblioteca_epoca") is not None]
    if not candidatos:
        return (None, None, None, None)
    modelo, melhor = max(candidatos, key=lambda x: x[1]["acuracia_balanceada_pct"])
    return (modelo, melhor["acuracia_balanceada_pct"], melhor["acerto_pct"],
            melhor["biblioteca_epoca"])


def _media(valores: list[float | None]) -> float | None:
    """! Alteração de IA - Revisar: média dos valores não-None de `valores`; None se todos
    forem None.
    ! Motivo: o parágrafo por fase faz média de adesão cega, autoenvenenamento e custo sobre
    os modelos que TÊM cada medida (nem todos rodam A5, nem todos têm Fase 3) -- ignorar os
    None em vez de tratá-los como zero é o que evita um modelo sem A5 puxar a média de adesão
    cega para baixo por não ter rodado o braço, não por ter aderido menos."""
    validos = [v for v in valores if v is not None]
    return round(sum(validos) / len(validos), 1) if validos else None


def _media_delta(pareamentos: list[dict], a: str, b: str, conjunto: str) -> float | None:
    """! Alteração de IA - Revisar: média de delta_pp entre os pareamentos (a, b, conjunto)
    informados, sobre todos os modelos.
    ! Motivo: é o 'ganho médio de A0 para A2' e o 'ganho médio de L0 para L3 nos 36' do
    parágrafo por fase -- filtrar a lista de pareamentos por (a, b, conjunto) em vez de somar
    delta_pp de pareamentos diferentes é o que impede misturar o ganho nos 90 casos com o
    ganho nos 36 na mesma média."""
    return _media([p["delta_pp"] for p in pareamentos
                  if p["a"] == a and p["b"] == b and p["conjunto"] == conjunto])


def _paragrafo_fases(comparacao: dict) -> list[str]:
    """! Alteração de IA - Revisar: o parágrafo fixo por fase (item 6 da Saída 2 do briefing
    da Tarefa 9) -- melhor modelo e acerto de cada fase, ganho médio A0→A2 (2-B) e L0→L3 nos 36
    (Fase 3), risco (adesão cega média, autoenvenenamento médio L2→L3) e perda (custo em
    s/caso, 2-B A2 contra F3 L3), todos calculados sobre `comparacao` -- nenhum é digitado.
    ! Motivo: é o texto que o Memorial cola direto -- calculá-lo a partir do MESMO dicionário
    que gera as tabelas (em vez de deixar quem escreve o Memorial ler os números nas tabelas e
    montar a frase à mão) é o que garante que o parágrafo nunca diverge delas."""
    por_modelo, pareamentos = comparacao["por_modelo"], comparacao["pareamentos"]
    m2a, v2a = _melhor(por_modelo, "2A_linear_ryzen")
    m2b, v2b = _melhor(por_modelo, "2B_A2")
    ganho_2b = _media_delta(pareamentos, "2B_A0", "2B_A2", "90")
    m_f3, b_f3, v_f3, l_f3 = _melhor_f3_geral(por_modelo)
    ganho_f3 = _media_delta(pareamentos, "F3_L0", "F3_L3", "36")
    adesao = _media([d["adesao_cega_2B_A5_pct"] for d in por_modelo.values()])
    autoenv = _media([d["autoenvenenamento_F3"].get("L2→L3") for d in por_modelo.values()
                      if d.get("autoenvenenamento_F3")])
    custo_2b = _media([d["nos_90"]["2B_A2"]["segundos_mediana"] for d in por_modelo.values()
                       if d["nos_90"].get("2B_A2")])
    custo_f3 = _media([d["nos_90"]["F3_L3"]["segundos_mediana"] for d in por_modelo.values()
                       if d["nos_90"].get("F3_L3")])
    epoca_f3 = "—" if l_f3 is None else f"L{l_f3}"
    return [
        f"Fase 2-A: melhor modelo {m2a or '—'}, {_n(v2a)}% de acerto (braço linear, "
        "Ryzen, sem biblioteca).",
        "",
        f"Fase 2-B: melhor modelo {m2b or '—'}, {_n(v2b)}% em A2 (com recuperação); ganho "
        f"médio de A0 para A2 de {_n(ganho_2b)} pp (média sobre os modelos com pareamento "
        "nos 90 casos).",
        "",
        f"Fase 3: melhor modelo {m_f3 or '—'}, {_n(b_f3)}% de acurácia balanceada em "
        f"{epoca_f3} (acerto simples {_n(v_f3)}%); ganho médio de L0 "
        f"para L3 nos 36 casos de avaliação de {_n(ganho_f3)} pp. Risco: adesão cega média de "
        f"{_n(adesao)}% em A5 (2-B), autoenvenenamento médio de {_n(autoenv)}% na transição "
        f"L2→L3 nos 36 casos de avaliação. Perda: {_n(custo_2b)} s/caso em 2-B A2 contra "
        f"{_n(custo_f3)} s/caso em F3 L3.",
    ]


def gerar_markdown(comparacao: dict) -> str:
    """! Alteração de IA - Revisar: monta o texto inteiro de comparacao_fases.md -- as 5
    tabelas pedidas pelo briefing da Tarefa 9 (acerto nos 90, acerto nos 36, custo, riscos,
    pareamentos) mais o parágrafo fixo por fase, tudo calculado a partir do dicionário
    `comparacao` que montar_comparacao devolve.
    ! Motivo: separar a montagem do Markdown da montagem do dicionário (como
    avaliar_fase3.imprimir_resumo separa a impressão do cálculo) é o que permite ao teste
    conferir os dois independentemente, e o que deixa claro que o .md é só uma REESCRITA do
    .json -- nenhuma conta nova acontece aqui."""
    por_modelo = comparacao["por_modelo"]
    linhas = [
        "<!-- ! Alteração de IA - Revisar: tabela gerada por comparar_fases.py a partir de "
        "comparacao_fases.json -- NÃO editar à mão.",
        "     ! Motivo: é a tabela que compara as três fases de teste para decidir o modelo "
        "final do TCC; editar direto quebraria a garantia de que todo número do Memorial sai "
        "de script, e a próxima corrida de comparar_fases.py sobrescreveria a edição sem "
        "avisar. -->",
        "",
        "# Comparação entre as fases 2-A, 2-B e 3",
        "",
    ]
    linhas += _tabela_acerto("Acerto por modelo e fase (90 casos)", por_modelo, "nos_90")
    # ! Alteração de IA - Revisar: as Tabelas 1b e 2b (acurácia balanceada, a métrica
    # primária) entram logo depois das de acerto, com a legenda comum -- onda final (I6).
    # ! Motivo: a acurácia balanceada era calculada em toda COL do JSON e não aparecia em
    # lugar nenhum do Markdown; o Memorial só via o acerto simples.
    linhas += _tabela_acerto("Acurácia balanceada por modelo e fase (90 casos)", por_modelo,
                            "nos_90", metrica="acuracia_balanceada_pct")
    linhas += _tabela_acerto("Acerto por modelo e fase (36 casos de avaliação)", por_modelo,
                            "nos_36_avaliacao")
    linhas += _tabela_acerto("Acurácia balanceada por modelo e fase (36 casos de avaliação)",
                            por_modelo, "nos_36_avaliacao", metrica="acuracia_balanceada_pct")
    linhas += [_LEGENDA_ACERTO, ""]
    linhas += _tabela_custo(por_modelo)
    linhas += _tabela_riscos(por_modelo)
    linhas += _tabela_pareamentos(comparacao["pareamentos"])
    linhas.append("## Leitura por fase")
    linhas.append("")
    linhas += _paragrafo_fases(comparacao)
    linhas.append("")
    return "\n".join(linhas)


# ------------------------------------------------------------------------ orquestração

def gerar_comparacao(caminho_2a: Path, caminho_2b: Path, c3: dict) -> dict:
    """! Alteração de IA - Revisar: monta o dicionário de comparação, grava
    comparacao_fases.json e comparacao_fases.md dentro da pasta de saída da Fase 3 (c3, de
    caminhos.fase3) e devolve o dicionário gravado.
    ! Motivo: é a função que o CLI e o teste chamam -- separar a montagem (montar_comparacao)
    da gravação, como avaliar_fase3.avaliar_saida faz, é o que permite ao teste conferir o
    dicionário devolvido e também reler os dois arquivos do disco na mesma chamada."""
    comparacao = montar_comparacao(caminho_2a, caminho_2b, c3)
    c3["raiz"].mkdir(parents=True, exist_ok=True)
    c3["comparacao"].write_text(json.dumps(comparacao, ensure_ascii=False, indent=2),
                                encoding="utf-8")
    c3["comparacao_md"].write_text(gerar_markdown(comparacao), encoding="utf-8")
    return comparacao


# ! Alteração de IA - Revisar: linha de comando -- --saida escolhe a pasta de resultados da
# Fase 3 (ver caminhos.fase3) e --avaliacao-2a/--avaliacao-2b apontam para os avaliacao.json
# já gravados por avaliar.py nas duas fases anteriores.
# ! Motivo: os padrões (experimentos/avaliacao.json e resultados_alvo/avaliacao.json) são os
# arquivos reais da 2-A e da 2-B descritos no briefing da Tarefa 9 -- rodar sem argumento
# nenhum já compara as três fases da corrida oficial; os dois --avaliacao-* só existem para
# apontar para outra pasta (ex.: uma repetição da 2-B) sem editar o script.
def main() -> None:
    ap = argparse.ArgumentParser(
        description="Compara as fases 2-A, 2-B e 3 por modelo (acerto pareado, adesão cega, "
                    "custo e riscos) e grava comparacao_fases.json/.md.")
    ap.add_argument("--saida", default="fase3",
                    help="subpasta dos resultados da Fase 3 (ver caminhos.fase3)")
    ap.add_argument("--avaliacao-2a", default=str(caminhos.AQUI / "avaliacao.json"),
                    help="avaliacao.json da Fase 2-A (Ryzen)")
    ap.add_argument("--avaliacao-2b",
                    default=str(caminhos.AQUI / "resultados_alvo" / "avaliacao.json"),
                    help="avaliacao.json da Fase 2-B (i5-alvo)")
    args = ap.parse_args()

    print(caminhos.descricao())
    c3 = caminhos.fase3(args.saida)
    comparacao = gerar_comparacao(Path(args.avaliacao_2a), Path(args.avaliacao_2b), c3)
    print(f"\n{len(comparacao['por_modelo'])} modelo(s) comparados — "
         f"{comparacao['metadados']['n_avaliacao']} casos de avaliação")
    for modelo, dados in sorted(comparacao["por_modelo"].items()):
        bloco = dados["nos_90"]
        print(f"  {modelo:34} 2A={_celula_acerto(bloco['2A_linear_ryzen'])}  "
              f"2B_A0={_celula_acerto(bloco['2B_A0'])}  2B_A2={_celula_acerto(bloco['2B_A2'])}"
              f"  F3_L0={_celula_acerto(bloco['F3_L0'])}  F3_L3={_celula_acerto(bloco['F3_L3'])}")
    print(f"\nComparação em {c3['comparacao']}\nTabela em {c3['comparacao_md']}")


if __name__ == "__main__":
    main()
