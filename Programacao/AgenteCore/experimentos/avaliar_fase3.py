#!/usr/bin/env python3
# ! Alteração de IA - Revisar: cria avaliar_fase3.py — o avaliador da Fase 3, que lê os
# JSONL de diagnóstico e de proposta de cada modelo, os snapshots da biblioteca de cada
# época e o histórico de edições, e grava avaliacao_fase3.json (uma linha por diagnóstico) e
# resumo_fase3.json (todas as métricas do relatório), além da planilha de revisão humana.
# ! Motivo: a Fase 2-B era comparada por avaliar.py, que agrega por CONDIÇÃO de biblioteca
# (A0..A5) e não conhece época, partição nem edição do modelo. Na Fase 3 o mesmo modelo roda
# os mesmos 90 casos contra 4 versões da biblioteca — L0 (original) até L3 (depois de 3
# épocas de edição) —, e as perguntas do trabalho passam a ser "a biblioteca editada pelo
# modelo melhora o diagnóstico dele?", "o ganho vale nos 36 casos de avaliação, que nunca
# entraram na biblioteca?" e "quantos casos que ele acertava passaram a errar?". Nenhuma
# delas sai dos cortes da 2-B. Reaproveita de avaliar.py o que não muda (extrair,
# avaliar_registro, wilson, mcnemar_exato, agregar, _mediana, _normalizar), para o acerto de
# um caso ser calculado pela MESMA regra nas duas fases — se divergissem, o Memorial teria
# dois números de acerto para o mesmo registro. Nenhum número entra em relatório sem sair
# daqui.
"""Avaliação da Fase 3: métricas por versão de biblioteca x partição, comparação pareada
contra a L0 (McNemar exato com ajuste de Holm), Cochran Q sobre as 4 versões, flips,
recuperação por época, métricas da documentação escrita pelo modelo e planilha de revisão
humana das edições aceitas."""
import argparse
import hashlib
import json
import math
import re
import statistics
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

import avaliar
import biblioteca as bib
import caminhos
import evolucao_biblioteca as evo
import recuperacao as rec
from banco_casos import CASOS
from banco_casos_extra import CASOS_EXTRA
from executar_bateria import ler_jsonl

# ! Alteração de IA - Revisar: força UTF-8 na saída do console, copiado de
# biblioteca.py:25-32.
# ! Motivo: no Windows o console pode estar em cp1252, que não representa os símbolos usados
# nas tabelas daqui (Δ, →, ✓, ✗, –) — sem isso o avaliador aborta com UnicodeEncodeError
# depois de já ter gravado os JSON, e quem roda vê um traceback no lugar da tabela.
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


# --------------------------------------------------------------------- constantes

TODOS_OS_CASOS = CASOS + CASOS_EXTRA
CASOS_POR_ID = {c["id"]: c for c in TODOS_OS_CASOS}

# Tamanhos esperados de cada arquivo da corrida oficial: 90 diagnósticos por versão de
# biblioteca e 54 propostas por época (os casos de aprendizado). Arquivo menor que isso é
# corrida incompleta e vira alerta no console — os percentuais sairiam sobre um n diferente
# do que o texto do trabalho diz.
N_DIAGNOSTICOS_ESPERADOS = 90
N_PROPOSTAS_ESPERADAS = 54

# Versões da biblioteca que as 3 épocas de aprendizado produzem: L0 é a cópia da original e
# L1..L3 são as editadas ao fim de cada época (executar_fase3.EPOCAS_PADRAO + 1 passadas de
# diagnóstico, uma por versão).
VERSOES = (0, 1, 2, 3)

# Rótulo da linha somada das duas partições. Os registros trazem 'aprendizado' (os 54 casos
# cujos diagnósticos geram proposta de edição) ou 'avaliacao' (os 36 que nunca entram na
# biblioteca, onde generalização é medida); 'todos' não existe no registro, é a linha que a
# avaliação acrescenta reetiquetando os mesmos casos.
PARTICAO_TODOS = "todos"

# Rótulo usado no lugar de causa_respondida quando o modelo não emitiu a linha CAUSA_RAIZ:
# entra na distribuição de rótulos como categoria própria, porque não responder nada é um
# comportamento diferente de responder sempre o mesmo rótulo.
SEM_RESPOSTA = "(sem resposta)"

# k da recuperação (condição A2). É lido dos registros; este é o padrão de
# executar_fase3.main (--k 3) para o caso de não haver registro com o campo.
K_PADRAO = 3

# Quantidade de edições aceitas que entram na planilha de revisão humana, por modelo e por
# época. 10 x 3 épocas = 30 edições por modelo, que é o que cabe numa sessão de revisão à
# mão conferindo cada texto contra o código do cobaia.
EDICOES_POR_EPOCA_NA_REVISAO = 10

# Veredictos aceitos na coluna "Avaliação" da planilha de revisão humana.
VEREDITOS_REVISAO = ("Correta", "Parcial", "Errada")


# --------------------------------------------------------- funções estatísticas

def qui_quadrado_sf(x: float, gl: int) -> float:
    """! Alteração de IA - Revisar: P(X > x) da distribuição qui-quadrado com gl inteiro,
    calculada em forma fechada — gl par = soma finita de Poisson,
    exp(-x/2)·Σ_{j=0}^{gl/2-1} (x/2)^j / j!; gl ímpar = erfc(√(x/2)) +
    2·φ(√x)·Σ_{j=1}^{(gl-1)/2} x^(j-1/2) / (1·3·…·(2j-1)), com φ a densidade normal padrão.
    ! Motivo: é o p do Cochran Q (Q segue qui-quadrado com k-1 graus de liberdade) e a regra
    do harness é zero dependência nova — não há scipy instalado. Para gl inteiro a cauda tem
    forma fechada exata, então não é aproximação: conferido no teste contra os pontos de
    tabela 3,841 (gl 1), 5,991 (gl 2), 7,815 (gl 3) e 9,488 (gl 4) para 5%, e 11,345
    (gl 3) para 1%."""
    if gl <= 0 or x < 0:
        return 1.0
    if gl % 2 == 0:
        termo, soma = 1.0, 1.0
        for j in range(1, gl // 2):
            termo *= (x / 2) / j
            soma += termo
        return min(1.0, math.exp(-x / 2) * soma)
    # Ímpar: a cauda da normal (erfc) mais a correção com os duplos fatoriais ímpares
    # (1, 1·3, 1·3·5, ...). phi(√x) = exp(-x/2)/√(2π) é a densidade normal padrão em √x.
    soma = 0.0
    duplo_fatorial = 1.0
    for j in range(1, (gl - 1) // 2 + 1):
        duplo_fatorial *= (2 * j - 1)
        soma += x ** (j - 0.5) / duplo_fatorial
    densidade = math.exp(-x / 2) / math.sqrt(2 * math.pi)
    return min(1.0, math.erfc(math.sqrt(x / 2)) + 2 * densidade * soma)


def cochran_q(matriz: list[list[bool]]) -> tuple[float, int, float]:
    """! Alteração de IA - Revisar: Q de Cochran de uma matriz em que as linhas são os casos
    e as colunas as condições (aqui, as versões L0..L3 da biblioteca):
    Q = (k-1)·(k·Σg² − (Σg)²) / (k·Σl − Σl²), com g = acertos de cada coluna e l = acertos de
    cada linha; devolve (Q, k-1, p). Denominador zero devolve (0.0, k-1, 1.0).
    ! Motivo: McNemar compara DUAS versões por vez; com 4 versões seriam 6 comparações e a
    pergunta "alguma das versões difere das outras?" não teria resposta única. Cochran é a
    extensão de McNemar para k condições pareadas sobre os mesmos casos, que é exatamente o
    desenho da Fase 3 (o mesmo caso diagnosticado contra L0, L1, L2 e L3). O denominador zera
    quando toda linha tem o mesmo valor nas k colunas (o modelo acertou em todas ou errou em
    todas): não há discordância para medir, e a linha sai neutra em vez de dividir por
    zero."""
    if not matriz or not matriz[0]:
        return (0.0, 0, 1.0)
    k = len(matriz[0])
    colunas = [sum(1 for linha in matriz if linha[j]) for j in range(k)]
    linhas = [sum(1 for valor in linha if valor) for linha in matriz]
    denominador = k * sum(linhas) - sum(v * v for v in linhas)
    if denominador == 0:
        return (0.0, k - 1, 1.0)
    numerador = (k - 1) * (k * sum(v * v for v in colunas) - sum(colunas) ** 2)
    q = numerador / denominador
    return (round(q, 4), k - 1, round(qui_quadrado_sf(q, k - 1), 4))


def holm(ps: list[float]) -> list[float]:
    """! Alteração de IA - Revisar: ajuste de Holm passo a passo — ordena os m valores de p,
    multiplica o i-ésimo por (m − i + 1), acumula o máximo corrido (o ajustado nunca diminui
    ao descer a lista) e trunca em 1; devolve os valores na ORDEM ORIGINAL da lista.
    ! Motivo: cada modelo da Fase 3 tem três comparações contra a L0 (L1, L2 e L3) dentro da
    mesma partição. Testar as três a 5% sem ajuste faz a chance de ao menos um 'significativo'
    por acaso subir para ~14%, e o trabalho afirmaria que a biblioteca editada melhorou o
    diagnóstico quando não melhorou. Holm foi escolhido em vez de Bonferroni porque é
    uniformemente mais poderoso com o mesmo controle do erro familiar, e em vez de FDR porque
    com 3 comparações a diferença entre os dois é irrelevante e Holm é o que se explica em
    uma linha no Memorial. O arredondamento em 4 casas acompanha avaliar.mcnemar_exato, que
    já devolve o p bruto arredondado assim."""
    m = len(ps)
    if m == 0:
        return []
    ordem = sorted(range(m), key=lambda i: ps[i])
    ajustados = [0.0] * m
    corrente = 0.0
    for posicao, i in enumerate(ordem):
        corrente = max(corrente, min(1.0, ps[i] * (m - posicao)))
        ajustados[i] = round(corrente, 4)
    return ajustados


def g_cohen(b: int, c: int) -> float | None:
    """! Alteração de IA - Revisar: g de Cohen do teste pareado — b/(b+c) − 0,5, em que b é o
    número de casos que só a versão nova acertou e c os que só a L0 acertou; None quando não
    houve discordância nenhuma (b + c = 0).
    ! Motivo: o p de McNemar diz se a diferença é distinguível do acaso, não o tamanho dela;
    com 90 casos e poucas discordâncias, um p alto pode esconder um efeito grande e um p
    baixo acompanhar um efeito minúsculo. g mede a parcela das discordâncias que ficou do
    lado da biblioteca editada, centrada em zero: 0 = as mudanças se anularam, +0,5 = toda
    mudança foi para melhor, −0,5 = toda mudança foi para pior. Sem discordância o valor não
    existe (0/0) e devolver 0 seria afirmar 'empate medido' onde não houve medição."""
    if b + c == 0:
        return None
    return round(b / (b + c) - 0.5, 3)


def acuracia_balanceada(pares: list[tuple[str, str]]) -> float:
    """! Alteração de IA - Revisar: macro-recall em porcentagem a partir de pares (causa
    esperada, causa respondida) — média, sobre as causas raiz PRESENTES no gabarito do grupo,
    da fração de acertos de cada causa. Comparação sem acento, pela mesma regra de
    avaliar._normalizar que decide causa_correta.
    ! Motivo: o acerto simples pode ser inflado por uma causa que aparece muito no recorte:
    um modelo que responde sempre 'campo_ausente' pontua bem num grupo em que essa causa
    domina e zero nas outras, e a tabela mostraria acerto razoável para um modelo que não
    diagnostica nada. Na acurácia balanceada cada causa pesa igual, então responder sempre o
    mesmo rótulo derruba o número. Só entram as causas que aparecem no gabarito daquele
    recorte: as 23 do conjunto fechado não aparecem todas em todo corte (por classe, por
    nível), e contar as ausentes como zero mediria o recorte, não o modelo."""
    if not pares:
        return 0.0
    por_causa: dict[str, list[bool]] = defaultdict(list)
    for esperada, respondida in pares:
        certo = (respondida is not None
                 and avaliar._normalizar(respondida) == avaliar._normalizar(esperada))
        por_causa[esperada].append(certo)
    medias = [sum(acertos) / len(acertos) for acertos in por_causa.values()]
    return round(100 * sum(medias) / len(medias), 1)


def distribuicao_de_rotulos(rotulos: list[str | None]) -> tuple[str | None, float, int]:
    """! Alteração de IA - Revisar: (rótulo mais frequente, parcela dele em %, número de
    rótulos distintos) de uma lista de causas respondidas; None vira "(sem resposta)".
    Empate é desempatado pelo nome, para a tabela sair igual em duas execuções.
    ! Motivo: é o par de colunas que denuncia o colapso de rótulo — o modelo que responde
    'campo_ausente' em 80% dos 90 casos tem uma distribuição de saída que não se parece com a
    do gabarito (23 causas em 90 casos), e só o percentual de acerto não mostra isso. Na Fase
    3 a pergunta é mais direta: a biblioteca que o modelo escreveu pode estreitar o
    vocabulário dele de uma época para outra, e a parcela do rótulo mais frequente é o número
    que mostra se estreitou."""
    if not rotulos:
        return (None, 0.0, 0)
    contagem: dict[str, int] = defaultdict(int)
    for rotulo in rotulos:
        contagem[rotulo if rotulo else SEM_RESPOSTA] += 1
    mais = min(contagem.items(), key=lambda item: (-item[1], item[0]))
    return (mais[0], round(100 * mais[1] / len(rotulos), 1), len(contagem))


def efeito_minimo_detectavel(ns: tuple[int, ...] = (36, 54, 90)) -> list[dict]:
    """! Alteração de IA - Revisar: para cada n, a menor diferença em pontos percentuais que
    o McNemar exato consegue apontar como significativa a 5%, supondo que 20% dos casos
    discordem entre as duas versões (d = round(0,2·n)): procura o menor b acima de d/2 com
    mcnemar_exato(b, d − b) < 0,05 e devolve {n, discordantes, b_min, delta_pp}.
    ! Motivo: é a régua que impede ler "sem diferença significativa" como "sem efeito". Com
    os 36 casos de avaliação, nenhuma diferença menor que ~19 pp pode dar p < 0,05 neste
    desenho — então um Δ de 8 pp com p alto não é evidência de que a biblioteca não ajudou, é
    o experimento sendo pequeno demais para decidir. NÃO é cálculo de poder formal (que
    exigiria supor a distribuição das discordâncias); é a diferença mínima significativa dado
    o número de discordâncias suposto, e o docstring diz isso porque o número vai para o
    Memorial. A busca começa acima de d/2 porque b ≤ d/2 significa que a versão nova ficou
    IGUAL ou PIOR que a L0, e o p ali é o espelho do mesmo teste — o menor b em termos
    absolutos seria b = 0 (todas as discordâncias contra a versão nova), que é significativo
    e descreve uma piora, não o efeito mínimo detectável."""
    saida = []
    for n in ns:
        d = round(0.2 * n)
        b_min = next((b for b in range(d + 1)
                      if 2 * b > d and avaliar.mcnemar_exato(b, d - b) < 0.05), None)
        saida.append({"n": n, "discordantes": d, "b_min": b_min,
                      "delta_pp": None if b_min is None
                      else round(100 * (2 * b_min - d) / n, 1)})
    return saida


# ------------------------------------------------------------- leitura dos arquivos

def _slug(modelo: str) -> str:
    """! Alteração de IA - Revisar: mesma troca de ':' e '/' por '_' de
    executar_fase3._slug, para casar o nome do modelo com o nome da pasta dele.
    ! Motivo: o executor grava em `<raiz>/qwen2.5-coder_3b/` e os registros dentro guardam
    'qwen2.5-coder:3b' no campo modelo. Sem repetir a regra aqui, `--modelos
    qwen2.5-coder:3b` não acharia pasta nenhuma e a avaliação sairia vazia sem erro."""
    return modelo.replace(":", "_").replace("/", "_")


def slugs_da_saida(c3: dict) -> list[str]:
    """! Alteração de IA - Revisar: lista as subpastas da raiz da Fase 3 que têm ao menos um
    diagnosticos__L*.jsonl dentro.
    ! Motivo: a raiz da Fase 3 também guarda `bibliotecas/`, `graficos/` e os arquivos soltos
    (particao.json, maquina.json, as planilhas de revisão); varrer só por `is_dir()` trataria
    `bibliotecas` como se fosse um modelo e a avaliação quebraria ao procurar JSONL lá. Exigir
    o arquivo de diagnóstico é o que distingue a pasta de um modelo das outras."""
    raiz = c3["raiz"]
    if not raiz.exists():
        return []
    return sorted(p.name for p in raiz.iterdir()
                  if p.is_dir() and any(p.glob("diagnosticos__L*.jsonl")))


def carregar_modelo(c3: dict, slug: str) -> tuple[list[dict], list[dict]]:
    """! Alteração de IA - Revisar: lê todos os diagnosticos__L*.jsonl e propostas__E*.jsonl
    de um modelo, em ordem de nome de arquivo, com a leitura tolerante de
    executar_bateria.ler_jsonl.
    ! Motivo: a corrida da Fase 3 pode ser interrompida no meio da gravação de uma linha, e
    ler_jsonl já ignora a linha cortada em vez de derrubar a avaliação inteira por um
    JSONDecodeError. A ordem por nome de arquivo (L0, L1, L2, L3) é o que faz a lista sair na
    ordem das épocas, que é como as tabelas do console são lidas."""
    pasta = c3["raiz"] / slug
    diagnosticos: list[dict] = []
    for arquivo in sorted(pasta.glob("diagnosticos__L*.jsonl")):
        diagnosticos += ler_jsonl(arquivo)
    propostas: list[dict] = []
    for arquivo in sorted(pasta.glob("propostas__E*.jsonl")):
        propostas += ler_jsonl(arquivo)
    return diagnosticos, propostas


def snapshots_do_modelo(c3: dict, slug: str) -> dict[int, Path]:
    """! Alteração de IA - Revisar: {época: pasta} das cópias FECHADAS da biblioteca de um
    modelo (bibliotecas/<slug>/epoca-n com fechamento.json).
    ! Motivo: uma pasta epoca-n sem fechamento.json é época interrompida no meio — os
    verbetes lá dentro não são os que fecharam a época e o hash não existe para casar com o
    biblioteca_versao dos registros. Medir recuperação sobre ela reportaria números de uma
    biblioteca que nenhum diagnóstico viu."""
    pasta = c3["bibliotecas"] / slug
    if not pasta.exists():
        return {}
    saida = {}
    for raiz in sorted(pasta.glob("epoca-*")):
        if raiz.is_dir() and evo.snapshot_fechado(raiz):
            saida[int(raiz.name.split("-")[1])] = raiz
    return saida


def indice_das_versoes(c3: dict, slugs: list[str]) -> dict[str, dict]:
    """! Alteração de IA - Revisar: carrega CADA versão de biblioteca uma única vez e devolve
    {hash da versão: {"notas": {id do verbete: nº de notas}, "novos": {ids de aprendidos/}}}.
    ! Motivo: por diagnóstico é preciso saber se o verbete citado na linha FONTE tinha nota do
    modelo e se era um verbete novo — e são 360 diagnósticos por modelo contra 4 versões.
    Reabrir os 36 .md da cópia a cada registro seriam ~50 mil leituras de disco por modelo. A
    chave é o hash (evolucao_biblioteca.hash_biblioteca), que é o mesmo campo
    biblioteca_versao gravado em cada registro pelo executor, então a epoca-0 de todos os
    modelos — que é byte a byte a mesma — é carregada uma vez só."""
    por_versao: dict[str, dict] = {}
    for slug in slugs:
        for raiz in snapshots_do_modelo(c3, slug).values():
            versao = json.loads((raiz / "fechamento.json").read_text(
                encoding="utf-8"))["hash"]
            if versao in por_versao:
                continue
            verbetes = bib.carregar(raiz)
            por_versao[versao] = {
                "notas": {v["id"]: len(bib.notas(v)) for v in verbetes},
                "novos": {v["id"] for v in verbetes
                          if v["pasta"] == evo.PASTA_APRENDIDOS},
            }
    return por_versao


def casos_da_particao(c3: dict, alvo: str) -> list[dict]:
    """! Alteração de IA - Revisar: os casos de uma partição ('aprendizado' ou 'avaliacao')
    lidos do particao.json gravado pelo executor; sem o arquivo, recalcula com
    evolucao_biblioteca.particionar.
    ! Motivo: particao.json é a partição TRAVADA daquela corrida (gravar_ou_conferir_particao
    recusa execução com partição diferente). Recalcular sempre daria outra divisão se
    banco_casos.py mudasse depois da corrida, e as métricas de avaliação sairiam sobre casos
    que na verdade entraram na biblioteca. O recálculo só entra como saída de emergência para
    uma pasta de resultados sem o arquivo."""
    if c3["particao"].exists():
        particao = json.loads(c3["particao"].read_text(encoding="utf-8"))
    else:
        particao = evo.particionar(TODOS_OS_CASOS)
    return [c for c in TODOS_OS_CASOS
            if particao["casos"].get(c["id"], {}).get("particao") == alvo]


def conferir_arquivos(c3: dict, slugs: list[str]) -> list[dict]:
    """! Alteração de IA - Revisar: lista os JSONL com menos linhas do que a corrida oficial
    prevê — 90 diagnósticos por versão de biblioteca e 54 propostas por época.
    ! Motivo: uma corrida interrompida deixa o arquivo da época com parte dos casos, e os
    percentuais sairiam calculados sobre um n menor sem nada acusar; no Memorial a tabela
    diria '90 casos' com 61 medidos. O alerta no console lista arquivo por arquivo para a
    decisão ser relançar o modelo ou registrar o n real."""
    faltas = []
    for slug in slugs:
        pasta = c3["raiz"] / slug
        for arquivo in sorted(pasta.glob("diagnosticos__L*.jsonl")):
            n = len(ler_jsonl(arquivo))
            if n < N_DIAGNOSTICOS_ESPERADOS:
                faltas.append({"modelo": slug, "arquivo": arquivo.name, "n": n,
                               "esperado": N_DIAGNOSTICOS_ESPERADOS})
        for arquivo in sorted(pasta.glob("propostas__E*.jsonl")):
            n = len(ler_jsonl(arquivo))
            if n < N_PROPOSTAS_ESPERADAS:
                faltas.append({"modelo": slug, "arquivo": arquivo.name, "n": n,
                               "esperado": N_PROPOSTAS_ESPERADAS})
    return faltas


# ------------------------------------------------------------------ por diagnóstico

def avaliar_registro_fase3(r: dict, causas_com_defeito: set[str],
                           por_versao: dict[str, dict]) -> dict:
    """! Alteração de IA - Revisar: a avaliação de um diagnóstico da Fase 3 — tudo o que
    avaliar.avaliar_registro já calcula (acerto da causa, campo, formato, citação, ouro no
    contexto, tempos) mais os campos que só existem nesta fase: época, versão da biblioteca,
    partição, k, notas no contexto e se o modelo citou um verbete anotado ou novo.
    ! Motivo: avaliar.avaliar_registro funciona como está sobre estes registros (o executor
    grava condicao 'A2' e as mesmas colunas da Fase 2-B de propósito), então reimplementar o
    acerto aqui criaria dois números para o mesmo caso. Os campos novos respondem as perguntas
    que a 2-B não tinha: 'contexto_com_nota' separa os diagnósticos que viram documentação
    escrita pelo modelo dos que viram só a original; 'citou_verbete_anotado' e
    'citou_verbete_novo' dizem se o que ele escreveu chegou a ser usado na resposta, que é
    diferente de ter sido recuperado. Os dois saem dos ids da linha FONTE — a única citação
    que o modelo faz de propósito; 'citou_verbete' (herdado de avaliar.py) é mais largo,
    conta também o id que aparece entre colchetes em qualquer lugar do texto."""
    base = avaliar.avaliar_registro(r, causas_com_defeito)
    versao = por_versao.get(r.get("biblioteca_versao")) or {"notas": {}, "novos": set()}
    citados = avaliar.extrair(r.get("resposta", ""))["fonte_ids"]
    notas_no_contexto = r.get("notas_no_contexto", 0)
    return {
        **base,
        "epoca": r.get("epoca"),
        "biblioteca_epoca": r.get("biblioteca_epoca"),
        "biblioteca_versao": r.get("biblioteca_versao"),
        "particao": r.get("particao"),
        "k": r.get("k", K_PADRAO),
        "notas_no_contexto": notas_no_contexto,
        "contexto_com_nota": notas_no_contexto > 0,
        "citou_verbete_anotado": any(versao["notas"].get(i, 0) > 0 for i in citados),
        "citou_verbete_novo": any(i in versao["novos"] for i in citados),
        "verbete_novo_no_contexto": bool(r.get("verbetes_novos_no_contexto")),
        "contexto_estourou": bool(r.get("contexto_estourou")),
    }


# ------------------------------------------------------------------------ agregação

def _p95(valores) -> float | None:
    """! Alteração de IA - Revisar: percentil 95 pelo método do posto mais próximo (ordena e
    pega o elemento de índice ceil(0,95·n) − 1); None quando não há valor medido.
    ! Motivo: a mediana de segundos esconde a cauda, e é a cauda que decide se a corrida cabe
    na janela de tempo — na Fase 2-B o mesmo modelo teve casos de 40 s e de 200 s. Com 90
    valores por célula, interpolar entre postos mudaria o número na terceira casa e
    complicaria a explicação; o posto mais próximo é o 86º valor ordenado de 90, que é direto
    de conferir à mão."""
    ordenados = sorted(v for v in valores if v is not None)
    if not ordenados:
        return None
    return round(ordenados[math.ceil(0.95 * len(ordenados)) - 1], 2)


def agregar_fase3(avaliados: list[dict], *chaves: str) -> list[dict]:
    """! Alteração de IA - Revisar: avaliar.agregar (n, acerto com IC de Wilson, campo,
    formato, tempos, tokens) mais as colunas próprias da Fase 3 — acurácia balanceada,
    distribuição dos rótulos respondidos, ancoragem na documentação (citou/ouro/nota/verbete
    novo), contexto estourado e o percentil 95 do tempo.
    ! Motivo: avaliar.agregar só acrescenta as colunas de ancoragem quando 'condicao' é uma
    das chaves de agrupamento e é diferente de A0 — aqui as chaves são modelo, época da
    biblioteca e partição, então essas colunas não sairiam, embora TODO registro da Fase 3
    seja A2 (biblioteca recuperada) e a ancoragem seja justamente o que se quer medir época a
    época. Reaproveitar a função em vez de reescrevê-la mantém acerto, IC e tempos idênticos
    aos da Fase 2-B, coluna por coluna."""
    linhas = avaliar.agregar(avaliados, *chaves)
    grupos: dict[tuple, list[dict]] = defaultdict(list)
    for a in avaliados:
        grupos[tuple(a[k] for k in chaves)].append(a)

    for linha in linhas:
        itens = grupos[tuple(linha[k] for k in chaves)]
        n = len(itens)
        rotulo, parcela, distintos = distribuicao_de_rotulos(
            [i["causa_respondida"] for i in itens])

        # ! Alteração de IA - Revisar: percentual dos itens do grupo com o campo booleano
        # verdadeiro, com itens/n presos como valor padrão dos parâmetros.
        # ! Motivo: são seis colunas calculadas com a mesma conta; e o laço reatribui
        # `itens` e `n` a cada linha — sem prendê-los no momento da definição, todas as
        # funções `pct` criadas no laço leriam o grupo da ÚLTIMA linha.
        def pct(campo: str, itens=itens, n=n) -> float:
            return round(100 * sum(1 for i in itens if i[campo]) / n, 1)

        linha.update({
            "acuracia_balanceada_pct": acuracia_balanceada(
                [(i["causa_esperada"], i["causa_respondida"]) for i in itens]),
            "rotulo_mais_frequente": rotulo,
            "parcela_rotulo_mais_frequente_pct": parcela,
            "n_rotulos_distintos": distintos,
            "citou_verbete_pct": pct("citou_verbete"),
            "ouro_no_contexto_pct": pct("ouro_no_contexto"),
            "contexto_com_nota_pct": pct("contexto_com_nota"),
            "citou_verbete_anotado_pct": pct("citou_verbete_anotado"),
            "citou_verbete_novo_pct": pct("citou_verbete_novo"),
            "verbete_novo_no_contexto_pct": pct("verbete_novo_no_contexto"),
            "contexto_estourou_n": sum(1 for i in itens if i["contexto_estourou"]),
            "segundos_p95": _p95([i["segundos"] for i in itens]),
        })
    return linhas


def _com_particao_todos(avaliados: list[dict]) -> list[dict]:
    """! Alteração de IA - Revisar: devolve os mesmos avaliados com o campo particao trocado
    para 'todos'.
    ! Motivo: a linha somada das duas partições precisa ter EXATAMENTE as mesmas colunas das
    linhas por partição (o console imprime as três lado a lado). Reetiquetar os registros e
    passar pela mesma agregar_fase3 garante isso; calcular a linha somada por fora abriria a
    chance de uma coluna nova ser acrescentada num caminho e esquecida no outro."""
    return [{**a, "particao": PARTICAO_TODOS} for a in avaliados]


# --------------------------------------------------------------- comparação pareada

def pareado_vs_l0(avaliados: list[dict]) -> list[dict]:
    """! Alteração de IA - Revisar: por modelo x versão da biblioteca (L1..L3) x partição, o Δ
    de acerto contra a L0 pareado caso a caso — b (só a versão nova acertou), c (só a L0
    acertou), McNemar exato, g de Cohen, razão b/c e o p ajustado por Holm sobre as três
    versões do mesmo (modelo, partição).
    ! Motivo: as quatro versões rodam sobre os MESMOS 90 casos, então comparar dois
    percentuais independentes jogaria fora a informação de quais casos mudaram de lado —
    Dietterich (1998) mostra que, para uma execução por condição, McNemar é o teste com erro
    tipo I aceitável (é a mesma escolha de avaliar.comparar_com_base na Fase 2-B). razao_bc
    fica ao lado de g porque é o número que se lê direto ('trocou 3 acertos por 1 erro'), e
    p_holm porque são três comparações por modelo e partição: sem ajuste, a chance de uma
    delas sair 'significativa' por acaso sobe de 5% para cerca de 14%."""
    por: dict[tuple, dict[str, bool]] = defaultdict(dict)
    for a in avaliados:
        for particao in (a["particao"], PARTICAO_TODOS):
            por[(a["modelo"], a["biblioteca_epoca"], particao)][a["caso"]] = \
                a["causa_correta"]

    linhas = []
    for (modelo, epoca, particao), casos in por.items():
        if epoca == 0:
            continue
        base = por.get((modelo, 0, particao))
        if not base:
            continue
        comuns = sorted(set(casos) & set(base))
        if not comuns:
            continue
        b = sum(1 for c in comuns if casos[c] and not base[c])
        cc = sum(1 for c in comuns if base[c] and not casos[c])
        n = len(comuns)
        acerto_base = round(100 * sum(base[c] for c in comuns) / n, 1)
        acerto_novo = round(100 * sum(casos[c] for c in comuns) / n, 1)
        linhas.append({
            "modelo": modelo, "biblioteca_epoca": epoca, "particao": particao,
            "n_pares": n, "acerto_L0_pct": acerto_base, "acerto_pct": acerto_novo,
            "delta_pp": round(acerto_novo - acerto_base, 1), "b": b, "c": cc,
            "p_mcnemar": avaliar.mcnemar_exato(b, cc), "p_holm": None,
            "g_cohen": g_cohen(b, cc),
            "razao_bc": None if cc == 0 else round(b / cc, 2),
        })

    linhas.sort(key=lambda linha: (linha["modelo"], linha["biblioteca_epoca"],
                                   linha["particao"]))
    familias: dict[tuple, list[dict]] = defaultdict(list)
    for linha in linhas:
        familias[(linha["modelo"], linha["particao"])].append(linha)
    for familia in familias.values():
        for linha, ajustado in zip(familia, holm([x["p_mcnemar"] for x in familia])):
            linha["p_holm"] = ajustado
    return linhas


def cochran_por_modelo(avaliados: list[dict]) -> list[dict]:
    """! Alteração de IA - Revisar: por modelo x partição, o Q de Cochran sobre as versões de
    biblioteca presentes (L0..L3 na corrida oficial), contando só os casos que têm
    diagnóstico em TODAS elas.
    ! Motivo: responde de uma vez 'alguma das versões difere das outras?', sem as 6
    comparações duas a duas que as 4 versões dariam. O caso que falta numa das versões (época
    interrompida) é deixado de fora inteiro, e não preenchido com 'errou': Cochran é um teste
    pareado, e completar buraco com zero inventaria discordância que ninguém mediu. As versões
    são as que existem nos registros, e não as 4 fixas, para o teste valer também numa corrida
    parcial — gl = número de versões − 1 diz quantas entraram."""
    por: dict[tuple, dict[str, dict[int, bool]]] = defaultdict(dict)
    versoes_por_modelo: dict[str, set] = defaultdict(set)
    for a in avaliados:
        versoes_por_modelo[a["modelo"]].add(a["biblioteca_epoca"])
        for particao in (a["particao"], PARTICAO_TODOS):
            por[(a["modelo"], particao)].setdefault(a["caso"], {})[
                a["biblioteca_epoca"]] = a["causa_correta"]

    linhas = []
    for (modelo, particao), casos in sorted(por.items()):
        versoes = sorted(versoes_por_modelo[modelo])
        matriz = [[casos[caso][v] for v in versoes] for caso in sorted(casos)
                  if all(v in casos[caso] for v in versoes)]
        q, gl, p = cochran_q(matriz)
        linhas.append({"modelo": modelo, "particao": particao, "n_casos": len(matriz),
                       "q": q, "gl": gl, "p": p})
    return linhas


def calcular_flips(avaliados: list[dict], campo: str) -> list[dict]:
    """! Alteração de IA - Revisar: por modelo x transição de época (L0→L1, L1→L2, L2→L3) x
    corte (partição ou classe), quantos casos passaram de certo para errado
    (autoenvenenamento) e de errado para certo.
    ! Motivo: o Δ de acerto é um saldo — uma época que acerta 3 casos novos e perde 3 antigos
    aparece como 'sem efeito', e é exatamente o efeito que o trabalho quer mostrar: a
    documentação que o próprio modelo escreveu pode estragar diagnósticos que ele já fazia
    certo. Separar os dois sentidos é o que torna isso visível. 'autoenvenenamento' é o nome
    usado no Memorial para o sentido certo→errado, e o percentual é sobre os casos pareados da
    transição."""
    por: dict[tuple, dict[str, bool]] = defaultdict(dict)
    for a in avaliados:
        valores = ((a["particao"], PARTICAO_TODOS) if campo == "particao"
                   else (a[campo],))
        for valor in valores:
            por[(a["modelo"], valor, a["biblioteca_epoca"])][a["caso"]] = \
                a["causa_correta"]

    linhas = []
    cortes = sorted({(m, v) for (m, v, _) in por}, key=lambda x: (str(x[0]), str(x[1])))
    for modelo, valor in cortes:
        for anterior in range(max(VERSOES)):
            de = por.get((modelo, valor, anterior))
            para = por.get((modelo, valor, anterior + 1))
            if not de or not para:
                continue
            comuns = sorted(set(de) & set(para))
            if not comuns:
                continue
            c2e = sum(1 for c in comuns if de[c] and not para[c])
            e2c = sum(1 for c in comuns if para[c] and not de[c])
            linha = {"modelo": modelo, "transicao": f"L{anterior}→L{anterior + 1}"}
            if campo == "classe":
                # O corte por classe é sempre sobre os 90 casos: a pergunta ali é em que
                # tipo de erro o autoenvenenamento se concentra, não em que partição.
                linha["particao"] = PARTICAO_TODOS
            linha[campo] = valor
            linha.update({"n_pares": len(comuns), "certo_para_errado": c2e,
                          "errado_para_certo": e2c,
                          "autoenvenenamento_pct": round(100 * c2e / len(comuns), 1)})
            linhas.append(linha)
    return linhas


# ----------------------------------------------------------------------- recuperação

def _no_topo(posicao: int | None, k: int) -> bool:
    """! Alteração de IA - Revisar: True quando o verbete de ouro ficou entre os k primeiros
    (posicao_por_caso de recuperacao.avaliar_recuperacao é 1-based e None quando não entrou).
    ! Motivo: a comparação `posicao <= k` sozinha quebra com None (TypeError no meio da
    avaliação); e escrever `pos and pos <= k` trataria a posição 0 como 'não recuperado' se um
    dia o índice virasse 0-based."""
    return posicao is not None and posicao <= k


def _metricas_recuperacao(medida: dict) -> dict:
    """! Alteração de IA - Revisar: fica só com hit@1, hit@3, hit@5, mrr e n do dicionário que
    recuperacao.avaliar_recuperacao devolve.
    ! Motivo: avaliar_recuperacao também devolve posicao_por_caso, que é a posição do verbete
    de ouro em cada um dos 90 casos. Esse mapa é usado aqui dentro (é o que responde 'o ouro
    entrou no top-3?'), mas gravá-lo no resumo somaria 90 entradas por versão por modelo — na
    corrida oficial, 1.440 linhas de ruído num arquivo que é lido à mão."""
    return {campo: medida[campo] for campo in ("hit@1", "hit@3", "hit@5", "mrr", "n")}


def recuperacao_por_epoca(c3: dict, slug: str, modelo: str, k: int) -> list[dict]:
    """! Alteração de IA - Revisar: por versão da biblioteca do modelo, hit@1/3/5 e MRR do
    verbete de ouro nos 90 casos e nos 36 de avaliação, mais 'ouro_deslocado_por_novo' (casos
    em que um verbete escrito pelo modelo ocupou o top-k e o de ouro ficou de fora) e
    'ouro_recuperavel_apos_edicao' (edições aceitas da época cujo caso de origem passou a ter
    o ouro no top-3 e não tinha na época anterior).
    ! Motivo: o diagnóstico da Fase 3 só vê os k verbetes recuperados, então uma queda de
    acerto pode não ser o modelo raciocinando pior, e sim o verbete certo tendo deixado de ser
    recuperado — a documentação que o próprio modelo acrescentou muda o índice BM25. Os dois
    campos extras separam os dois efeitos opostos: 'deslocado' conta o estrago (o verbete novo
    empurrou o de ouro para fora) e 'recuperavel_apos_edicao' conta o ganho (a nota escrita
    naquele caso trouxe o verbete certo para o top-3). A pontuação é calculada UMA vez por
    caso e reaproveitada nas três medições, porque rec.pontuar percorre todos os verbetes por
    caso e são 90 casos x 4 versões x cada modelo."""
    snapshots = snapshots_do_modelo(c3, slug)
    if not snapshots:
        return []
    casos_avaliacao = casos_da_particao(c3, "avaliacao")
    historico = ler_jsonl(c3["bibliotecas"] / slug / "historico.jsonl")

    linhas, posicoes_por_epoca = [], {}
    for epoca in sorted(snapshots):
        raiz = snapshots[epoca]
        verbetes = bib.carregar(raiz)
        por_id = {v["id"]: v for v in verbetes}
        novos = {v["id"] for v in verbetes if v["pasta"] == evo.PASTA_APRENDIDOS}
        # ! Alteração de IA - Revisar: o índice BM25 da versão é construído UMA vez por
        # versão, fora do dicionário — onda final (item 6a).
        # ! Motivo: rec.Indice(verbetes) estava dentro da compreensão e era reconstruído a
        # cada um dos 90 casos (tokenização dos 36+ verbetes, 90 vezes por versão por
        # modelo) para dar sempre o mesmo índice.
        indice = rec.Indice(verbetes)
        ordem_por_caso = {c["id"]: [v["id"] for _, v in rec.pontuar(indice, c)]
                          for c in TODOS_OS_CASOS}
        fechamento = json.loads((raiz / "fechamento.json").read_text(encoding="utf-8"))

        # ! Alteração de IA - Revisar: pontuador que devolve, para um caso, os verbetes na
        # ordem já calculada em ordem_por_caso — o que recuperacao.avaliar_recuperacao
        # aceita no lugar do BM25 para não pontuar de novo.
        # ! Motivo: ordem e por_id entram como parâmetros com valor padrão (e não pelo
        # fechamento da função) porque a época seguinte reatribui os dois nomes: sem isso,
        # as medições da época 0 seriam calculadas com a biblioteca da última época do laço.
        def pontuador(caso, ordem=ordem_por_caso, por_id=por_id):
            return [por_id[i] for i in ordem[caso["id"]]]

        medida_todos = rec.avaliar_recuperacao(verbetes, TODOS_OS_CASOS,
                                               pontuador=pontuador)
        medida_avaliacao = rec.avaliar_recuperacao(verbetes, casos_avaliacao,
                                                   pontuador=pontuador)
        posicoes_por_epoca[epoca] = medida_todos["posicao_por_caso"]

        deslocado = 0
        for caso in TODOS_OS_CASOS:
            topo = ordem_por_caso[caso["id"]][:k]
            ouro = rec.verbete_ouro(verbetes, caso)["id"]
            if ouro not in topo and any(i in novos for i in topo):
                deslocado += 1

        recuperavel = None
        anterior = posicoes_por_epoca.get(epoca - 1)
        if epoca >= 1 and anterior is not None:
            recuperavel = sum(
                1 for linha in historico if linha.get("epoca") == epoca
                and _no_topo(posicoes_por_epoca[epoca].get(linha.get("caso")), 3)
                and not _no_topo(anterior.get(linha.get("caso")), 3))

        # ! Alteração de IA - Revisar: cada versão passa a levar 'chars' e 'tokens_estimados'
        # do fechamento.json — o tamanho RENDERIZADO da biblioteca (bib.render_biblioteca),
        # o texto que de fato entra no prompt — onda final (achado I4).
        # ! Motivo: a figura 15 (crescimento da biblioteca) somava tokens_estimados do
        # fechamento (renderizado) com tokens_estimados_acrescentados do diff (bytes crus do
        # .md, frontmatter e cabeçalhos inclusos, ~2,5x maior) para reconstruir o L0 — duas
        # unidades na mesma reta. Aqui há uma linha por versão L0..L3, então o tamanho de cada
        # uma sai direto do fechamento dela, sem subtrair nada.
        linhas.append({
            "modelo": modelo, "biblioteca_epoca": epoca,
            "hash": fechamento["hash"],
            "chars": fechamento.get("chars"),
            "tokens_estimados": fechamento.get("tokens_estimados"),
            "n_verbetes": len(verbetes), "n_verbetes_novos": len(novos),
            "todos": _metricas_recuperacao(medida_todos),
            "avaliacao": _metricas_recuperacao(medida_avaliacao),
            "ouro_deslocado_por_novo": deslocado,
            "ouro_recuperavel_apos_edicao": recuperavel,
        })
    return linhas


# ---------------------------------------------------------------------- documentação

def _fatia_propostas(registros: list[dict]) -> dict:
    """! Alteração de IA - Revisar: {n, propostas, aceitas} de um subconjunto de registros de
    proposta.
    ! Motivo: os cortes 'quando errou o diagnóstico' e 'quando acertou' precisam exatamente
    dos mesmos três números, e repetir as três somas em dois lugares abriria a chance de um
    deles passar a contar decisões e o outro registros."""
    return {"n": len(registros),
            "propostas": sum(r.get("n_propostas", 0) for r in registros),
            "aceitas": sum(r.get("n_aceitas", 0) for r in registros)}


def _ms_por_token(registros: list[dict]) -> float | None:
    """! Alteração de IA - Revisar: mediana de prefill_ms / tokens_entrada dos registros que
    têm os dois campos.
    ! Motivo: é a medida do cache de prefixo do Ollama. O prompt de proposta começa com o
    prompt de diagnóstico byte a byte (estrategias.proposta_de_edicao é a continuação dele),
    então se o cache agiu o prefill da proposta custa muito menos por token do que o do
    diagnóstico — sem esse par de números, a diferença de tempo entre as duas inferências
    ficaria sem explicação no Memorial. Mediana, e não média: uma recarga do modelo no meio da
    corrida deixa um prefill de dezenas de segundos que puxaria a média sozinho."""
    valores = [r["prefill_ms"] / r["tokens_entrada"] for r in registros
               if r.get("prefill_ms") and r.get("tokens_entrada")]
    return round(statistics.median(valores), 2) if valores else None


def documentacao_por_epoca(c3: dict, slug: str, modelo: str, propostas: list[dict],
                           diagnosticos: list[dict]) -> list[dict]:
    """! Alteração de IA - Revisar: por época, tudo o que o modelo ESCREVEU — quantas
    propostas fez e quantas foram aceitas, por operação, o histograma completo dos códigos de
    rejeição, as tentativas de copiar o caso para dentro da documentação, o quanto a
    biblioteca cresceu (do diff__E<n>.json) e como ela ficou (do fechamento.json), o corte
    entre propostas feitas depois de acertar e depois de errar o diagnóstico, e os tempos.
    Os totais do diff levam 'md' no nome (chars_md_acrescentados,
    tokens_md_estimados_acrescentados) porque medem bytes crus dos .md — frontmatter e
    cabeçalhos inclusos —, não o texto renderizado que entra no prompt (esse está em
    'biblioteca' e, por versão, em recuperacao_por_epoca; onda final, achado I4).
    ! Motivo: é a metade do experimento que não aparece no acerto do diagnóstico. Um modelo
    pode não melhorar nada no acerto e mesmo assim escrever documentação válida (ou o
    contrário: encher a biblioteca de cópias do enunciado do caso, que é o que
    'tentativas_de_decorar' conta — os códigos copia_do_caso e copia_do_caso_acumulada de
    evolucao_biblioteca.validar_proposta). O histograma começa com TODOS os códigos de
    CODIGOS_REJEICAO em zero de propósito: assim a soma das barras fecha com o número de
    propostas recusadas e um código que nunca aparece continua visível como zero, em vez de
    sumir da tabela. n_fim_ausente conta os blocos que chegaram sem a linha FIM — no piloto o
    qwen2.5-coder:3b escreveu as 6 propostas sem FIM nenhuma vez, e é o número que mostra se o
    modelo aprendeu o formato de saída."""
    pasta_bib = c3["bibliotecas"] / slug
    linhas = []
    for epoca in sorted({p.get("epoca") for p in propostas if p.get("epoca")}):
        da_epoca = [p for p in propostas if p.get("epoca") == epoca]
        diag_da_epoca = [d for d in diagnosticos if d.get("epoca") == epoca]
        decisoes = [d for p in da_epoca for d in p.get("decisoes", [])]

        motivos = {codigo: 0 for codigo in evo.CODIGOS_REJEICAO}
        for d in decisoes:
            if not d.get("aceita") and d.get("motivo"):
                motivos[d["motivo"]] = motivos.get(d["motivo"], 0) + 1

        por_operacao = {op: {"propostas": 0, "aceitas": 0} for op in evo.OPERACOES}
        for d in decisoes:
            operacao = bib.normalizar(d.get("operacao") or "")
            if operacao not in por_operacao:
                continue
            por_operacao[operacao]["propostas"] += 1
            if d.get("aceita"):
                por_operacao[operacao]["aceitas"] += 1

        arquivo_diff = pasta_bib / f"diff__E{epoca}.json"
        diff = (json.loads(arquivo_diff.read_text(encoding="utf-8"))
                if arquivo_diff.exists() else {})
        arquivo_fech = pasta_bib / f"epoca-{epoca}" / "fechamento.json"
        fechamento = (json.loads(arquivo_fech.read_text(encoding="utf-8"))
                      if arquivo_fech.exists() else {})

        n_propostas = sum(p.get("n_propostas", 0) for p in da_epoca)
        n_aceitas = sum(p.get("n_aceitas", 0) for p in da_epoca)
        tempos = [p.get("segundos") for p in da_epoca if p.get("segundos") is not None]
        tokens_saida = [p.get("tokens_saida") for p in da_epoca
                        if p.get("tokens_saida") is not None]
        linhas.append({
            "modelo": modelo, "epoca": epoca,
            "n_casos_aprendizado": len(da_epoca),
            "n_nenhuma": sum(1 for p in da_epoca if p.get("nenhuma")),
            "n_respostas_truncadas": sum(1 for p in da_epoca
                                         if p.get("resposta_truncada")),
            "n_sem_bloco": motivos.get("sem_bloco", 0),
            "n_fim_ausente": sum(1 for p in da_epoca
                                 for b in p.get("propostas_parseadas", [])
                                 if b.get("fim_ausente")),
            "n_propostas": n_propostas, "n_aceitas": n_aceitas,
            "aceitas_pct": round(100 * n_aceitas / n_propostas, 1) if n_propostas else 0.0,
            "por_operacao": por_operacao,
            "motivos_rejeicao": motivos,
            "tentativas_de_decorar": (motivos.get("copia_do_caso", 0)
                                      + motivos.get("copia_do_caso_acumulada", 0)),
            "chars_md_acrescentados": diff.get("chars_acrescentados"),
            "tokens_md_estimados_acrescentados": diff.get("tokens_estimados_acrescentados"),
            "verbetes_tocados": len(diff.get("arquivos_tocados", [])),
            "verbetes_novos": len(diff.get("arquivos_novos", [])),
            "quando_errou": _fatia_propostas(
                [p for p in da_epoca if p.get("acertou_diagnostico") is False]),
            "quando_acertou": _fatia_propostas(
                [p for p in da_epoca if p.get("acertou_diagnostico") is True]),
            "biblioteca": {campo: fechamento.get(campo) for campo in
                           ("n_verbetes", "n_notas", "n_retificacoes", "chars",
                            "tokens_estimados", "hash")},
            "segundos_mediana_proposta": avaliar._mediana(tempos),
            "tokens_saida_medio_proposta": (round(sum(tokens_saida) / len(tokens_saida))
                                            if tokens_saida else None),
            "prefill_ms_por_token_proposta": _ms_por_token(da_epoca),
            "prefill_ms_por_token_diagnostico": _ms_por_token(diag_da_epoca),
        })
    return linhas


# ------------------------------------------------------------ conferências de origem

def reconstrucao_ok(c3: dict, slug: str, modelo: str, diagnosticos: list[dict],
                    quantos: int = 10) -> dict:
    """! Alteração de IA - Revisar: remonta o contexto A2 dos `quantos` primeiros
    diagnósticos gravados contra a biblioteca da época 1 e confere que o sha256 de 12
    caracteres bate com o contexto_sha256 do registro.
    ! Motivo: o prompt de diagnóstico não é gravado no JSONL — ele é reconstruível a partir do
    snapshot da época mais os verbetes_ids do registro. Toda leitura posterior (gráficos,
    exemplos no Memorial, qualquer reanálise) depende disso ser verdade. Se a pasta da época
    tiver sido mexida depois da corrida, ou se a recuperação mudar de resultado, o hash deixa
    de bater e a avaliação avisa em vez de o trabalho citar um prompt que o modelo não viu.
    Dez registros, sempre os dez primeiros do arquivo, para a conferência ser determinística e
    custar frações de segundo — não é amostragem estatística, é prova de integridade."""
    raiz = c3["bibliotecas"] / slug / "epoca-1"
    registros = [d for d in diagnosticos if d.get("biblioteca_epoca") == 1][:quantos]
    if not registros or not evo.snapshot_fechado(raiz):
        return {"modelo": modelo, "conferidos": 0, "ok": 0}
    verbetes = bib.carregar(raiz)
    indice = rec.Indice(verbetes)
    # ! Alteração de IA - Revisar: 'conferidos' conta só os registros que chegaram à
    # comparação do hash — onda final (item 6b).
    # ! Motivo: era len(registros): um registro com id de caso fora do banco era pulado, mas
    # continuava contado como conferido, e o console mostrava "10 de 10 ok" tendo conferido 9.
    conferidos = ok = 0
    for r in registros:
        caso = CASOS_POR_ID.get(r.get("caso"))
        if caso is None:
            continue
        conferidos += 1
        texto = rec.contexto(verbetes, indice, caso, "A2", r.get("k", K_PADRAO))["texto"]
        if hashlib.sha256(texto.encode("utf-8")).hexdigest()[:12] == \
                r.get("contexto_sha256"):
            ok += 1
    return {"modelo": modelo, "conferidos": conferidos, "ok": ok}


# ------------------------------------------------------- planilha de revisão humana

def _cotas(contagens: dict[str, int], total: int) -> dict[str, int]:
    """! Alteração de IA - Revisar: divide `total` vagas entre as operações presentes —
    mínimo 1 para cada uma, o resto proporcional ao número de edições de cada operação (maior
    resto primeiro), nunca mais vagas do que edições existentes, e o que sobrar volta para
    quem ainda tem edição não escolhida.
    ! Motivo: se a divisão fosse só proporcional, a operação rara ficaria de fora da revisão —
    e é justamente a rara (retificação, verbete novo) que precisa de olho humano, porque é
    onde o modelo pode reescrever o sentido de um verbete. Com o mínimo de 1, a planilha
    sempre traz ao menos um exemplo de cada operação que o modelo usou naquela época."""
    presentes = sorted(op for op, n in contagens.items() if n > 0)
    if not presentes or total <= 0:
        return {}
    if len(presentes) > total:
        presentes = sorted(presentes, key=lambda op: (-contagens[op], op))[:total]
    cotas = {op: 1 for op in presentes}
    restante = total - len(presentes)
    soma = sum(contagens[op] for op in presentes)
    if restante > 0 and soma:
        exatos = {op: restante * contagens[op] / soma for op in presentes}
        for op in presentes:
            cotas[op] += int(exatos[op])
        faltam = restante - sum(int(v) for v in exatos.values())
        for op in sorted(presentes, key=lambda o: (-(exatos[o] % 1), o))[:faltam]:
            cotas[op] += 1
    cotas = {op: min(cotas[op], contagens[op]) for op in presentes}
    while sum(cotas.values()) < total:
        sobra = [op for op in presentes if cotas[op] < contagens[op]]
        if not sobra:
            break
        cotas[min(sobra, key=lambda o: (-contagens[o], o))] += 1
    return cotas


def amostrar_edicoes(historico: list[dict], modelo: str,
                     por_epoca: int = EDICOES_POR_EPOCA_NA_REVISAO) -> list[dict]:
    """! Alteração de IA - Revisar: amostra determinística de até `por_epoca` edições aceitas
    por época do historico.jsonl, repartidas entre as operações por _cotas e escolhidas, dentro
    de cada operação, pela ordem de sha256("revisao:<modelo>:<epoca>:<ordem>").
    ! Motivo: a planilha é revisada à mão, então tem de ser um subconjunto — mas escolher 'as
    10 primeiras' viesaria para o começo da época (quando a biblioteca ainda estava intacta) e
    escolher com random.sample daria uma planilha diferente a cada execução, o que quebraria a
    ideia de a planilha não ser sobrescrita. O hash de modelo+época+ordem dá sempre a mesma
    amostra, embaralhada em relação à ordem de gravação, e diferente entre modelos. A época
    entrou na chave na onda final (item 6c): a `ordem` de aceitação recomeça em 1 a cada
    época (executar_fase3.rodar_epoca), então sem ela as três épocas sorteavam sempre as
    MESMAS posições — a planilha nunca traria, por exemplo, a 1ª edição da época 2 se a 1ª
    da época 1 tivesse ficado de fora. As linhas saem ordenadas por época e ordem porque é
    assim que a revisão é lida — na sequência em que o modelo escreveu."""
    escolhidas: list[dict] = []
    for epoca in sorted({linha.get("epoca") for linha in historico}):
        da_epoca = [linha for linha in historico if linha.get("epoca") == epoca]
        por_operacao: dict[str, list[dict]] = defaultdict(list)
        for linha in da_epoca:
            por_operacao[linha.get("operacao") or "(sem operação)"].append(linha)
        cotas = _cotas({op: len(v) for op, v in por_operacao.items()}, por_epoca)
        for operacao, cota in cotas.items():
            ordenadas = sorted(por_operacao[operacao], key=lambda linha: hashlib.sha256(
                f"revisao:{modelo}:{epoca}:{linha.get('ordem')}".encode("utf-8"))
                .hexdigest())
            escolhidas += ordenadas[:cota]
    return sorted(escolhidas, key=lambda linha: (linha.get("epoca") or 0,
                                                 linha.get("ordem") or 0))


def _celula(texto: str | None) -> str:
    """! Alteração de IA - Revisar: prepara um texto do modelo para caber numa célula de
    tabela Markdown — escapa a barra vertical e troca quebra de linha por espaço.
    ! Motivo: o TEXTO e o MOTIVO da proposta são escritos pelo modelo; uma barra vertical no
    meio partiria a linha em colunas a mais e a planilha ficaria ilegível justamente na linha
    que precisa ser revisada. O escape com '\\|' é o que o Markdown entende dentro de tabela."""
    return (texto or "").replace("|", "\\|").replace("\n", " ").strip()


def gerar_planilha_revisao(c3: dict, slug: str, modelo: str) -> Path | None:
    """! Alteração de IA - Revisar: grava revisao_edicoes__<slug>.md na raiz da Fase 3 com a
    amostra de edições aceitas e a coluna Avaliação em branco; NÃO sobrescreve arquivo
    existente e devolve None nesse caso.
    ! Motivo: a planilha é o único julgamento humano do experimento (o harness mede se a
    edição é válida, não se ela é CORRETA sobre o cobaia) e é preenchida à mão ao longo de
    dias. Regravar por cima apagaria o trabalho de revisão na primeira vez que alguém
    relançasse a avaliação para refazer um gráfico — por isso a existência do arquivo é a
    trava, e não uma opção de linha de comando."""
    destino = c3["raiz"] / f"revisao_edicoes__{slug}.md"
    if destino.exists():
        return None
    historico = ler_jsonl(c3["bibliotecas"] / slug / "historico.jsonl")
    escolhidas = amostrar_edicoes(historico, modelo)
    if not escolhidas:
        return None

    linhas = [
        "<!-- ! Alteração de IA - Revisar: planilha de revisão humana das edições que o "
        "modelo fez na biblioteca, GERADA por avaliar_fase3.py --gerar-revisao.",
        "     ! Motivo: o harness só consegue medir se a edição é VÁLIDA (formato, tetos, "
        "não copiou o caso); se o que foi escrito é verdade sobre o cobaia, só conferindo",
        "     contra o código. Esta planilha existe para esse julgamento e NÃO é "
        "sobrescrita: uma nova execução da avaliação encontra o arquivo e o deixa como está. -->",
        "",
        f"# Revisão das edições aceitas — {modelo}",
        "",
        f"Amostra determinística de {len(escolhidas)} edição(ões) aceita(s), até "
        f"{EDICOES_POR_EPOCA_NA_REVISAO} por época, com ao menos uma de cada operação "
        "usada na época.",
        "",
        "Como preencher: abra o verbete citado na cópia do modelo "
        f"(`bibliotecas/{slug}/epoca-<Época>/`), leia o texto acrescentado e confira contra "
        "o código do cobaia (`Programacao/Cobaia/`). Escreva na coluna **Avaliação** um de:",
        "",
        "- `Correta` — o que está escrito é verdade sobre o sistema e ajuda no diagnóstico;",
        "- `Parcial` — é verdade em parte, ou é vago demais para ajudar;",
        "- `Errada` — afirma algo que o código não faz.",
        "",
        "Deixe a coluna em branco no que não revisar: a avaliação conta em branco (e "
        "qualquer outro valor) como `sem_avaliacao`.",
        "",
        "| # | Época | Caso | Verbete | Operação | Texto | Motivo | Avaliação | Comentário |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for i, linha in enumerate(escolhidas, 1):
        linhas.append(
            f"| {i} | {linha.get('epoca')} | {linha.get('caso')} | "
            f"{linha.get('verbete')} | {linha.get('operacao')} | "
            f"{_celula(linha.get('texto'))} | {_celula(linha.get('motivo'))} |  |  |")
    linhas.append("")
    destino.write_text("\n".join(linhas), encoding="utf-8")
    return destino


def revisao_humana(c3: dict, slug: str, modelo: str) -> list[dict]:
    """! Alteração de IA - Revisar: lê a planilha revisao_edicoes__<slug>.md já preenchida e
    conta, por operação, quantas edições foram julgadas Correta, Parcial, Errada ou ficaram
    sem avaliação; qualquer valor fora dos três entra em sem_avaliacao e é listado em
    valores_nao_reconhecidos. Devolve lista vazia enquanto ninguém tiver preenchido nada.
    ! Motivo: é o único número do trabalho que não sai de regra automática, e ele precisa
    entrar no resumo pela mesma porta que todos os outros (nenhum número digitado à mão no
    relatório). Contar o valor estranho como sem_avaliacao em vez de ignorá-lo mantém a soma
    fechando com o número de linhas da planilha; listá-lo é o que permite achar o 'correta'
    em minúscula ou o 'ok' que alguém escreveu com pressa."""
    arquivo = c3["raiz"] / f"revisao_edicoes__{slug}.md"
    if not arquivo.exists():
        return []
    por_operacao: dict[str, dict] = {}
    preenchida = False
    for linha in arquivo.read_text(encoding="utf-8").splitlines():
        if not linha.startswith("| ") or linha.startswith("| #"):
            continue
        celulas = [c.strip() for c in re.split(r"(?<!\\)\|", linha.strip("|"))]
        if len(celulas) != 9:
            continue
        operacao, veredito = celulas[4], celulas[7]
        conta = por_operacao.setdefault(operacao, {
            "modelo": modelo, "operacao": operacao, "Correta": 0, "Parcial": 0,
            "Errada": 0, "sem_avaliacao": 0, "valores_nao_reconhecidos": []})
        if veredito in VEREDITOS_REVISAO:
            conta[veredito] += 1
            preenchida = True
        else:
            conta["sem_avaliacao"] += 1
            if veredito and veredito not in conta["valores_nao_reconhecidos"]:
                conta["valores_nao_reconhecidos"].append(veredito)
                preenchida = True
    if not preenchida:
        return []
    return [por_operacao[op] for op in sorted(por_operacao)]


# ------------------------------------------------------------------- orquestração

def avaliar_saida(c3: dict, modelos: list[str] | None = None,
                  gerar_revisao: bool = False) -> tuple[list[dict], dict]:
    """! Alteração de IA - Revisar: roda a avaliação inteira de uma pasta de resultados da
    Fase 3 — avalia cada diagnóstico, monta os 13 blocos do resumo na ordem em que o relatório
    os usa e grava avaliacao_fase3.json e resumo_fase3.json. Devolve (avaliados, resumo) sem
    imprimir nada.
    ! Motivo: separar o cálculo da impressão é o que deixa o teste rodar a avaliação inteira
    sem sujar a saída do runner, e o que permite a um gerador de gráficos ou de relatório
    chamar esta função em vez de reler os JSON. A ordem das chaves do resumo é a ordem do
    relatório de propósito: quem abrir o JSON à mão lê os blocos na mesma sequência do texto
    do trabalho."""
    slugs = slugs_da_saida(c3)
    if modelos:
        pedidos = {_slug(m) for m in modelos}
        slugs = [s for s in slugs if s in pedidos]
    if not slugs:
        raise SystemExit(f"nenhum modelo com diagnósticos em {c3['raiz']} — rode "
                         "executar_fase3.py, ou confira --saida e --modelos")

    try:
        causas_com_defeito = bib.causas_com_defeito_documentado(bib.carregar(bib.BASE))
    except FileNotFoundError:
        causas_com_defeito = set()
    por_versao = indice_das_versoes(c3, slugs)

    avaliados: list[dict] = []
    propostas_por_slug: dict[str, list[dict]] = {}
    diagnosticos_por_slug: dict[str, list[dict]] = {}
    nome_por_slug: dict[str, str] = {}
    for slug in slugs:
        diagnosticos, propostas = carregar_modelo(c3, slug)
        diagnosticos_por_slug[slug] = diagnosticos
        propostas_por_slug[slug] = propostas
        nome_por_slug[slug] = (diagnosticos[0]["modelo"] if diagnosticos
                               else slug.replace("_", ":"))
        avaliados += [avaliar_registro_fase3(r, causas_com_defeito, por_versao)
                      for r in diagnosticos]

    marcados = _com_particao_todos(avaliados)
    resumo = {
        "por_modelo_biblioteca_particao":
            agregar_fase3(avaliados, "modelo", "biblioteca_epoca", "particao")
            + agregar_fase3(marcados, "modelo", "biblioteca_epoca", "particao"),
        "por_modelo_biblioteca_classe":
            agregar_fase3(marcados, "modelo", "biblioteca_epoca", "particao", "classe"),
        "por_modelo_biblioteca_nivel":
            agregar_fase3(marcados, "modelo", "biblioteca_epoca", "particao", "nivel"),
        "pareado_vs_L0": pareado_vs_l0(avaliados),
        "cochran_q": cochran_por_modelo(avaliados),
        "flips": calcular_flips(avaliados, "particao"),
        "flips_por_classe": calcular_flips(avaliados, "classe"),
        "efeito_minimo_detectavel": efeito_minimo_detectavel(),
        "recuperacao": [], "documentacao": [], "reconstrucao_ok": [],
        "revisao_humana": [],
    }
    resumo["por_modelo_biblioteca_particao"].sort(
        key=lambda linha: (linha["modelo"], linha["biblioteca_epoca"], linha["particao"]))

    for slug in slugs:
        modelo = nome_por_slug[slug]
        ks = [d["k"] for d in avaliados if d["modelo"] == modelo and d.get("k")]
        k = max(set(ks), key=ks.count) if ks else K_PADRAO
        if gerar_revisao:
            gerar_planilha_revisao(c3, slug, modelo)
        resumo["recuperacao"] += recuperacao_por_epoca(c3, slug, modelo, k)
        resumo["documentacao"] += documentacao_por_epoca(
            c3, slug, modelo, propostas_por_slug[slug], diagnosticos_por_slug[slug])
        resumo["reconstrucao_ok"].append(
            reconstrucao_ok(c3, slug, modelo, diagnosticos_por_slug[slug]))
        resumo["revisao_humana"] += revisao_humana(c3, slug, modelo)

    # ! Alteração de IA - Revisar: o resumo lista as versões de biblioteca (biblioteca_versao
    # dos registros) que não têm snapshot fechado em bibliotecas/<slug>/epoca-*/ — onda
    # final (item 6e); imprimir_resumo avisa no console.
    # ! Motivo: avaliar_registro_fase3 usa um conjunto vazio de notas e verbetes novos ({"notas": {}, "novos": set()})
    # quando a versão não está em por_versao, e as colunas citou_verbete_anotado/novo saem
    # zeradas sem nada acusar — uma pasta de época apagada ou um hash trocado passaria por
    # "o modelo nunca citou verbete anotado".
    versoes_sem_snapshot = sorted({
        r.get("biblioteca_versao") for diagnosticos in diagnosticos_por_slug.values()
        for r in diagnosticos if r.get("biblioteca_versao") not in por_versao}, key=str)
    resumo["metadados"] = {
        "saida": c3["raiz"].name,
        "modelos": [nome_por_slug[s] for s in slugs],
        "gerado_em": datetime.now().isoformat(timespec="seconds"),
        "n_diagnosticos": len(avaliados),
        "n_propostas": sum(len(p) for p in propostas_por_slug.values()),
        "versoes_sem_snapshot": versoes_sem_snapshot,
    }

    c3["raiz"].mkdir(parents=True, exist_ok=True)
    c3["avaliacao"].write_text(json.dumps(avaliados, ensure_ascii=False, indent=2),
                               encoding="utf-8")
    c3["resumo"].write_text(json.dumps(resumo, ensure_ascii=False, indent=2),
                            encoding="utf-8")
    return avaliados, resumo


# ------------------------------------------------------------------------- console

def _mais_chars(v: int | None) -> str:
    """! Alteração de IA - Revisar: "+N chars" ou "—" quando o diff da época não existe —
    onda final (item 6f).
    ! Motivo: a linha de documentação do console imprimia "+None chars" para uma época sem
    diff__E<n>.json (corrida interrompida antes de fechar), que parece um número quebrado
    em vez de um dado ausente."""
    return "—" if v is None else f"+{v} chars"


def imprimir_resumo(c3: dict, avaliados: list[dict], resumo: dict) -> None:
    """! Alteração de IA - Revisar: imprime, no estilo das tabelas de avaliar.py, o quadro
    modelo x versão da biblioteca x partição, o bloco dos Δ pareados (com * onde p_holm <
    0,05), o Cochran, os flips, a documentação por época e os alertas.
    ! Motivo: o resumo_fase3.json tem dezenas de milhares de linhas e ninguém o lê de ponta a
    ponta depois de cada corrida; o console é o que diz, em dez segundos, se a corrida está
    sadia (todos os arquivos completos, contexto nunca estourado, contexto reconstruído
    batendo) e qual o resultado principal. O asterisco vai no p AJUSTADO e não no bruto de
    propósito: marcar o bruto convidaria a ler três comparações a 5% cada uma."""
    print(f"\n{len(avaliados)} diagnósticos avaliados — {c3['raiz']}\n")
    print(f"{'modelo':26} {'L':>2} {'particao':>11} {'n':>4} {'acerto%':>8} {'IC95':>13} "
          f"{'balanc%':>8} {'cita%':>6} {'ouro%':>6} {'nota%':>6} {'s med':>7}")
    for linha in resumo["por_modelo_biblioteca_particao"]:
        ic = f"{linha['causa_correta_ic95'][0]}–{linha['causa_correta_ic95'][1]}"
        print(f"{linha['modelo']:26} {linha['biblioteca_epoca']:>2} "
              f"{linha['particao']:>11} {linha['n']:>4} "
              f"{linha['causa_correta_pct']:>8} {ic:>13} "
              f"{linha['acuracia_balanceada_pct']:>8} {linha['citou_verbete_pct']:>6} "
              f"{linha['ouro_no_contexto_pct']:>6} {linha['contexto_com_nota_pct']:>6} "
              f"{str(linha['segundos_mediana'] or '-'):>7}")

    if resumo["pareado_vs_L0"]:
        print("\nΔ contra a L0 (pareado por caso; McNemar exato, * = p ajustado por Holm "
              "< 0,05):")
        for linha in resumo["pareado_vs_L0"]:
            marca = "*" if linha["p_holm"] is not None and linha["p_holm"] < 0.05 else " "
            print(f"  {linha['modelo']:26} L{linha['biblioteca_epoca']} "
                  f"{linha['particao']:>11}: {linha['acerto_L0_pct']:>5} → "
                  f"{linha['acerto_pct']:>5} ({linha['delta_pp']:+.1f} pp) "
                  f"b={linha['b']:>2} c={linha['c']:>2} p={linha['p_mcnemar']:<7} "
                  f"holm={linha['p_holm']:<7} "
                  f"g={'-' if linha['g_cohen'] is None else linha['g_cohen']}{marca}")

    if resumo["cochran_q"]:
        print("\nCochran Q (as versões da biblioteca lado a lado, mesmos casos):")
        for linha in resumo["cochran_q"]:
            print(f"  {linha['modelo']:26} {linha['particao']:>11}: Q={linha['q']:<8} "
                  f"gl={linha['gl']} p={linha['p']} (n={linha['n_casos']})")

    if resumo["flips"]:
        print("\nFlips entre épocas (autoenvenenamento = certo → errado):")
        for linha in resumo["flips"]:
            print(f"  {linha['modelo']:26} {linha['transicao']} "
                  f"{linha['particao']:>11}: ✓→✗ {linha['certo_para_errado']:>2}, "
                  f"✗→✓ {linha['errado_para_certo']:>2} de {linha['n_pares']:>3} casos "
                  f"— autoenvenenamento {linha['autoenvenenamento_pct']}%")

    if resumo["documentacao"]:
        print("\nDocumentação escrita pelo modelo, por época:")
        for linha in resumo["documentacao"]:
            top = sorted(((n, c) for c, n in linha["motivos_rejeicao"].items() if n),
                         reverse=True)[:3]
            rejeicoes = ", ".join(f"{c} {n}" for n, c in top) or "nenhuma rejeição"
            print(f"  {linha['modelo']:26} E{linha['epoca']}: {linha['n_aceitas']}/"
                  f"{linha['n_propostas']} aceitas ({linha['aceitas_pct']}%), "
                  f"{linha['n_nenhuma']} NENHUMA, {linha['n_fim_ausente']} sem FIM, "
                  f"{_mais_chars(linha['chars_md_acrescentados'])} (md) — {rejeicoes}")

    if resumo["revisao_humana"]:
        print("\nRevisão humana das edições aceitas:")
        for linha in resumo["revisao_humana"]:
            print(f"  {linha['modelo']:26} {linha['operacao']:>14}: "
                  f"{linha['Correta']} correta(s), {linha['Parcial']} parcial(is), "
                  f"{linha['Errada']} errada(s), {linha['sem_avaliacao']} sem avaliação")

    estourou = sum(1 for a in avaliados if a["contexto_estourou"])
    if estourou:
        print(f"\n!! {estourou} diagnóstico(s) com contexto_estourou — o Ollama pode ter "
              "descartado o começo do prompt (a biblioteca) sem avisar")
    sem_snapshot = resumo["metadados"].get("versoes_sem_snapshot", [])
    if sem_snapshot:
        print(f"\n!! biblioteca_versao sem snapshot fechado em bibliotecas/: "
              f"{', '.join(str(v) for v in sem_snapshot)} — citou_verbete_anotado/novo "
              "saíram zerados para esses diagnósticos; confira as pastas epoca-*")
    for linha in resumo["reconstrucao_ok"]:
        if linha["ok"] < linha["conferidos"]:
            print(f"\n!! {linha['modelo']}: {linha['conferidos'] - linha['ok']} de "
                  f"{linha['conferidos']} contextos NÃO foram reconstruídos com o mesmo "
                  "hash — a pasta da época 1 mudou depois da corrida")
        elif linha["conferidos"] == 0:
            print(f"\n!! {linha['modelo']}: nenhum contexto conferido (sem diagnósticos "
                  "contra a época 1 ou sem a pasta epoca-1 fechada)")
    faltas = conferir_arquivos(c3, [_slug(m) for m in resumo["metadados"]["modelos"]])
    if faltas:
        print("\n!! arquivos com menos registros do que a corrida oficial prevê:")
        for falta in faltas:
            print(f"   {falta['modelo']}/{falta['arquivo']}: {falta['n']} de "
                  f"{falta['esperado']}")


# ! Alteração de IA - Revisar: linha de comando do avaliador — --saida escolhe a pasta de
# resultados da Fase 3, --modelos recorta quais modelos entram e --gerar-revisao escreve as
# planilhas de revisão humana que ainda não existem.
# ! Motivo: --gerar-revisao é uma opção separada, e não o comportamento padrão, porque a
# planilha é preenchida à mão: gerá-la sempre não faria mal (ela nunca é sobrescrita), mas a
# opção deixa explícito no comando anotado no caderno de laboratório em que momento da
# corrida as planilhas foram criadas — antes ou depois da última época de cada modelo, o que
# muda quais edições entraram na amostra.
def main() -> None:
    ap = argparse.ArgumentParser(
        description="Avaliação da Fase 3: métricas por versão de biblioteca e partição, "
                    "comparação pareada contra a L0, Cochran, flips, recuperação e "
                    "documentação escrita pelo modelo.")
    ap.add_argument("--saida", default="fase3",
                    help="subpasta dos resultados da Fase 3 (ver caminhos.fase3)")
    ap.add_argument("--gerar-revisao", action="store_true",
                    help="gera as planilhas de revisão humana que ainda não existem")
    ap.add_argument("--modelos", nargs="+", default=None,
                    help="nomes ou slugs dos modelos (padrão: todos os encontrados)")
    args = ap.parse_args()

    print(caminhos.descricao())
    c3 = caminhos.fase3(args.saida)
    if not slugs_da_saida(c3):
        print(f"Nenhum diagnóstico da Fase 3 em {c3['raiz']}. Rode executar_fase3.py "
              "primeiro.")
        return
    avaliados, resumo = avaliar_saida(c3, args.modelos, args.gerar_revisao)
    imprimir_resumo(c3, avaliados, resumo)
    print(f"\nAvaliação em {c3['avaliacao']}\nResumo em {c3['resumo']}")


if __name__ == "__main__":
    main()
