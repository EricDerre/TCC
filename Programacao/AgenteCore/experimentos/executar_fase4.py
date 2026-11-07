#!/usr/bin/env python3
# ! Alteração de IA - Revisar: arquivo novo (26/10/2026, Fase 4, pacote P2): o orquestrador da Fase 4, no molde de
# executar_fase3b.py, com o primeiro modo, `reproducao` (corrida 17 do plano aprovado): para cada caso de avaliação
# (os 36 oficiais e os 36 inéditos) cuja causa tem um modo de injeção e cuja rota tem tela (`GET /api/produtos` e
# `GET /api/produtos/{id}` em produtos_api.php), liga o modo na CobaiaAPI pelo endpoint admin, roda o roteiro no
# navegador com o interceptador, poda a árvore e o corpo, monta o caso ao vivo com o sintoma por molde, decide se a
# tela reproduz o caso (regra R1) e grava tudo: `reproducao.jsonl`, `fora.json`, `condicoes_fase4.json`, a trilha v2
# da corrida e o log com a linha FIM. Sobe as cobaias por run.start_services e restaura o banco antes. Sem modelo.
# ! Motivo: antes de gastar modelo, a Fase 4 precisa saber quantos casos a tela reproduz, quanto custa um cenário e
# quanto pesa a trilha (plano, P2, "Mede"); e a corrida de referência em modo normal de cada cenário é a trilha
# dourada contra a qual a árvore de cada caso é comparada (especificação, seção 9).
# ! Alteração de IA - Revisar: (27/10/2026, pacote P3) dois modos com modelo, no molde de `rodar_reproducao`: `calibracao`
# (corrida 16: sondagem dos logprobs no Ollama instalado, ponte de versão pela regra R6 quando a versão não tem ponte em
# `resultados_alvo/fase4/pontes.json`, a L1 curada de biblioteca_producao nos 90 casos oficiais com cada k pedido, pelo
# executor congelado da Fase 3 com as probabilidades por token na linha lateral como na corrida 12, a regra R8 para o k
# e os limiares do selo em `resultados_alvo/fase4/limiares.json`, regra R7) e `tela` (corrida 18: cada caso que
# reproduziu na corrida 17 é montado na tela como lá, diagnosticado por diagnostico_ao_vivo.py e, na mesma sessão do
# Ollama, o mesmo caso lido do fixture, sem gabarito; registros com as 37 chaves, linhas laterais, `tela.jsonl` por
# caso, trilha v2 gravada caso a caso e relatórios v2 no fim). O que a corrida 17 fazia por caso saiu do laço para a
# classe `Tela`, que os dois modos de tela usam sem mudar o que `reproducao` grava. Corrida parcial (`--casos`) nunca
# grava `limiares.json` nem `pontes.json` oficiais; o modo `tela` sem limiares ou sem ponte só roda parcial.
# ! Motivo: plano aprovado, seção 5 (P3) e regras R6 a R8; a versão do Ollama é conferida a cada caso e a corrida para se
# ela mudar no meio (decisão 44); o gabarito nunca chega ao agente (princípio 5 do plano): o executor grava o registro
# sem gabarito e a avaliação (avaliar_fase4.py --tela) junta pelo id do caso depois.
# ! Alteração de IA - Revisar: (01/11/2026, pacote P4) o modo `cura` (corrida 19, sem modelo): para cada célula (roteiro do
# front legado x modo de quebra x forma da quebra x repetição), a corrida de referência da célula sem quebra registra o
# alvo do passo (cura_seletor.descrever_elemento); o roteiro roda com a quebra armada (pelo harness, por add_init_script,
# ou pela variante do front PHP, por cookie) e falha no passo do alvo (detecção; início do cronômetro do MTTR); a árvore
# é podada, os candidatos são gerados e verificados em código na página aberta, e o primeiro que passa as verificações
# estáticas é reexecutado do começo do roteiro, com a quebra armada de novo; o roteiro chegar ao fim é a cura (fim do
# cronômetro) e a regra R3 separa "mesmo elemento" de "outro elemento" pela impressão do DOM. Grava `cura.jsonl` por
# execução, `condicoes_fase4.json`, a trilha v2 (`trilha_cura.jsonl`, eventos entrada, acao, verificacao, poda, cura,
# decisao cura e decisao reexecucao) e os relatórios v2 por execução; o banco é restaurado antes de cada execução que
# grava (reserva do cliente) e o tempo da restauração entre a detecção e a reexecução é descontado do MTTR.
# ! Motivo: plano aprovado, P4 e seção 6 (corrida 19: 4 roteiros x 4 modos x 5 repetições, nas duas formas da ficha 29 c);
# a cura nunca altera a aplicação e só vale na reexecução de verificação (projeto ABNT §2.1).
# ! Alteração de IA - Revisar: (03/11/2026, pacote P5) o modo `biblioteca` (corrida 20, noite C, com modelo), em quatro fases na
# mesma sessão do Ollama: (A) os 54 casos de aprendizado da partição da Fase 3, cada um lido da tela quando tem modo, cenário e
# reproduz pela regra R1 (a classe `Tela`, como na corrida 18) e do fixture nos outros, diagnosticado por diagnostico_ao_vivo
# com os verbetes ligados ao caso recuperados pelo id (ficha 32) e, na continuação literal do prompt, a proposta de edição
# (biblioteca_fase4.propor_p5: o validador congelado da Fase 3, os 13 filtros em código da decisão 65 e a regra dos 40% da
# calibração), gravada na cópia epoca-101 só quando passa por tudo; a época fecha pelo fechamento da Fase 3; (B) a regra R5:
# os 36 inéditos da 3-B diagnosticados com a epoca-101 (o lote) e pareados com a cópia curada (corrida 12, `--base-ineditos
# corrida12`, ou diagnosticados de novo na mesma sessão com `propria`), b e c em `lote.json`; (C) o ciclo de correção, sem
# modelo: os casos de aprendizado ligados a notas da L1 e com tela, metade com o modo desligado (partilha determinística por
# hash, `conjunto_de_correcao`) e metade mantido, cada um rodado antes (modo ligado) e depois; o gatilho em código marca
# `corrigido` só com a evidência dos dois diffs e a operação "correção" grava as seções na epoca-102, fechada por
# biblioteca_fase4.fechar_correcoes; a regra R4 compara a marca com o conjunto desligado; (D) a sonda de 28/09 repetida
# (sonda_correcao.rodar_sonda) com a recuperação por id ligada, sobre a epoca-102, com efe-3, efe-10 e os casos desligados.
# Grava `biblioteca.jsonl` (um por caso de aprendizado), `correcoes.jsonl`, `lote.json`, `sonda.json`, `condicoes_fase4.json`,
# a trilha v2 (`trilha_biblioteca.jsonl`) e os relatórios v2 por caso; a leitura é avaliar_fase4.py --biblioteca.
# ! Motivo: plano aprovado, P5 e seção 6 (corrida 20) e regras R4 e R5; a biblioteca de produção não muda na corrida: o lote
# aceito só é promovido por biblioteca_fase4.py --promover, depois da planilha de revisão humana preenchida pelo Eric.
# ! Alteração de IA - Revisar: (04/11/2026, pacote P7) o modo `avaliacao_trilha` (corrida 22, noite D, com modelo): os 36 casos
# oficiais de avaliação lidos do fixture, sem gabarito, cada um com a inferência de base (nós poda, recuperacao e diagnostico em
# código, as quatro intervenções da especificação pela amostra fixa), a sonda de pós-racionalização e as mutações verbete trocado
# e contrato alterado (avaliacao_trilha.py); no fim, com as cobaias e o navegador, a mutação do seletor nos quatro roteiros de
# localizador do ensaio (a execução dourada com a quebra do catálogo e a mutada com o nome do alvo trocado, as duas com o
# diagnóstico entre a detecção e a cura, como na corrida 21). Grava `avaliacao.jsonl` (um por caso), `seletor.jsonl` (um por
# roteiro), os registros oficiais de 37 chaves por etapa, `condicoes_fase4.json`, a trilha v2 (`trilha_avaliacao.jsonl`) e os
# relatórios v2; relançar retoma dos casos e roteiros que faltam; a leitura é avaliar_fase4.py --trilha.
# ! Motivo: plano aprovado, seção 5 (P7) e seção 6 (corrida 22); especificação da trilha, seção 12. A biblioteca de produção é
# lida como está e não muda; o gabarito nunca chega ao executor: a leitura junta pelo id do caso.
"""Uso (em Programacao/AgenteCore/experimentos):
  RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha [--casos N] [--ids lex-1,...] [--sem-seletor]
  RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo biblioteca --saida fase4_biblioteca [--base-ineditos corrida12|propria] [--casos N] [--sem-sonda] [--sem-correcao]
  RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo reproducao --saida fase4_reproducao [--casos N] [--canal chromium] [--banco avaliacao|ineditos_fase4|todos]
  RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo cura --saida fase4_cura [--repeticoes 5] [--formas harness,php] [--roteiros front-busca,...] [--modos id_renomeado,...]
  RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo calibracao --saida fase4_calibracao [--k 3,5] [--casos N]
  RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela [--casos N] [--intervencoes desligadas|por_gatilho] [--amostra]
Depois: RESULTADOS_DIR=resultados_alvo python avaliar_fase4.py --reproducao|--calibracao|--tela --saida <saida> [--check]"""
from __future__ import annotations

import argparse
import contextlib
import copy
import json
import platform
import re
import sys
import time
import urllib.request
from pathlib import Path

EXP = Path(__file__).resolve().parent
RAIZ = EXP.parent.parent.parent
sys.path.insert(0, str(RAIZ))

import analisar_fase3b as a3b
import avaliar
import biblioteca as bib
import caminhos
import caso_ao_vivo as cv
import cenarios_fase4 as cen
import cura_seletor as cs
import estrategias
import evolucao_biblioteca as evo
import executar_bateria
import executar_fase3
import executar_fase3b as e3b
import interceptador as ic
import navegador
import poda
import recuperacao as rec
import sonda_confianca as sc
import sondar_logprobs as sl
import trilha as tr

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass

# ! Alteração de IA - Revisar: (04/11/2026, P6) o modo `cenarios` (corrida 21: o ensaio dos dez cenários da Fase 5).
# ! Motivo: plano aprovado, seção 5 (P6): `executar_fase4.py --modo cenarios --repeticoes N`.
# ! Alteração de IA - Revisar: (04/11/2026, P7) o modo `avaliacao_trilha` (corrida 22: a avaliação da própria trilha).
# ! Motivo: plano aprovado, seção 5 (P7): `executar_fase4.py --modo avaliacao_trilha`; a lógica fica em avaliacao_trilha.py.
# ! Alteração de IA - Revisar: (05/11/2026, decisões 91 e 92) os modos das corridas 23 e 24, em corridas_em_texto.py.
# ! Motivo: as duas corridas rodam em texto, sem navegador, mas pelo mesmo comando e com as mesmas guardas de versão das outras.
MODOS = ("reproducao", "calibracao", "tela", "cura", "biblioteca", "cenarios", "avaliacao_trilha", "experimento_prompt", "ineditos")
REPETICOES_PADRAO = 5                     # corrida 19: cinco repetições por célula (plano, seção 6)
BASES_DOS_INEDITOS = ("corrida12", "propria")
CORRIDA12 = "pre_fase4_confianca"         # corrida 12 (06/10/2026): a cópia curada nos 72 casos, k = 3, Ollama 0.34.4 (ponte 0.40.2 pareável)
TETO_PROPOSTA_PADRAO = 700                # o mesmo teto de saída da proposta da Fase 3 (sonda_correcao --max-tokens-proposta)
EPOCA_DO_LOTE = 101                       # epoca-100 é a L1 curada; 101 o lote; 102 as correções; 103 a sonda
EPOCA_DAS_CORRECOES = 102
MODELO_PADRAO = "qwen2.5:7b"
K_PADRAO = "3,5"                          # ficha 30 (a): a calibração mede os dois
RAM_MINIMA_GB = {"qwen2.5:7b": 6.5}       # o mesmo valor de rodar_fase3b.ps1 ($RamMinima), medido na Fase 2-B
LIMITE_PONTE = a3b.LIMITE_PONTE           # decisão 47: até 2 casos discordantes em 36
CASOS_DE_TEXTO_ALTERADO = a3b.CASOS_DE_TEXTO_ALTERADO   # efe-3 e efe-10, texto corrigido em 28/09/2026
# ! Alteração de IA - Revisar: orçamento de tempo da chamada à API baixado de 5000 para 1000 ms e a regra R1 ganhou a
# comparação com a corrida de referência em modo normal (corpo igual? árvore completa igual?), além do contrato e do
# roteiro; sem a chamada do alvo, vale a última chamada do roteiro (chamada_do_caso).
# ! Motivo: na primeira corrida 17 (26/10/2026) a mediana normal foi 27 ms e o `latency` no detalhe levou 2007 ms,
# abaixo do orçamento antigo; e mutações que o contrato não vê (acentos estragados, preço em centavos, tipo girado,
# nome com sufixo) passavam como "não reproduz" embora o corpo e a tela tenham mudado contra a referência; nos casos
# de detalhe em que o catálogo já quebra, a chamada do detalhe nunca acontece e a do catálogo é a evidência.
ORCAMENTO_DE_TEMPO_MS = 1000
TOKEN_PADRAO = "troque-isto-localmente"   # settings.admin_token da CobaiaAPI (app/config.py), sem .env
URL_ADMIN = "http://127.0.0.1:8000/api/admin/fault-mode"
_ROTA_CATALOGO = re.compile(r"^GET /api/produtos/?(\?.*)?$")
_ROTA_DETALHE = re.compile(r"^GET /api/produtos/(\d+)")
IDS_DO_SEED = range(1, 15)


# ------------------------------------------------------------------ partes puras (testadas sem cobaias)

def selecionar_casos(casos: list[dict]) -> dict:
    """Separa os casos que a tela consegue reproduzir (causa com modo e rota de produtos) dos que ficam fora, com o
    motivo de cada um; para os reproduzíveis diz o modo, o campo alvo, o cenário e o id do produto."""
    reproduziveis, fora = [], []
    for c in casos:
        causa = c["gabarito"]["causa_raiz"]
        req = str(c["entrada"].get("requisicao") or "")
        base = {"id": c["id"], "classe": c["classe"], "nivel": c["nivel"], "causa": causa, "requisicao": req}
        if causa in cen.CAUSAS_PELO_HARNESS:
            fora.append({**base, "motivo": f"armada pelo harness (ficha 29): {causa}"})
            continue
        if causa not in cen.MODO_POR_CAUSA:
            fora.append({**base, "motivo": f"sem modo para a causa {causa}"})
            continue
        detalhe = _ROTA_DETALHE.match(req)
        if detalhe:
            cenario, produto_id = "api-detalhe", int(detalhe.group(1))
        elif _ROTA_CATALOGO.match(req):
            cenario, produto_id = "api-catalogo", None
        else:
            fora.append({**base, "motivo": f"sem tela: a rota {req!r} não é consumida por página nenhuma"})
            continue
        modo = cen.MODO_POR_CAUSA[causa]
        campo = c["gabarito"].get("campo_afetado") if modo in cen.MODOS_COM_CAMPO else None
        reproduziveis.append({**base, "modo": modo, "campo": campo, "cenario": cenario, "produto_id": produto_id})
    return {"reproduziveis": reproduziveis, "fora": fora}


def corpo_admin(modo: str, campo: str | None) -> dict:
    """O corpo do POST /api/admin/fault-mode: o campo alvo só vai nos modos que o usam; `normal` nunca leva campo."""
    return {"mode": modo, "target_field": campo if modo in cen.MODOS_COM_CAMPO else None, "probability": 1.0}


def reproduz(resultado: dict, diff_corpo: dict | None, registro: dict | None, referencia: dict | None = None) -> dict:
    """Regra R1 do plano: a tela reproduz o caso quando a chamada à API saiu do normal (status, corpo, contrato,
    tempo acima do orçamento, corpo diferente da referência em modo normal), quando a árvore completa da página
    difere da referência ou quando uma conferência do roteiro falhou. Sem chamada capturada, não reproduz."""
    if registro is None:
        return {"reproduz": False, "motivo": "nenhuma chamada à API capturada no roteiro"}
    motivos = []
    if registro.get("status") != 200:
        motivos.append(f"status {registro.get('status')}")
    if diff_corpo is not None:
        if diff_corpo.get("corpo") != "json":
            motivos.append(f"corpo {diff_corpo.get('corpo')}")
        if diff_corpo.get("diferencas"):
            motivos.append("diff do contrato: " + ", ".join(sorted({d["tipo"] for d in diff_corpo["diferencas"]})))
    if referencia and referencia.get("corpo_igual") is False:
        motivos.append("corpo diferente da referência em modo normal")
    arv = (referencia or {}).get("arvore") or {}
    if arv.get("a_menos") or arv.get("a_mais"):
        motivos.append(f"árvore diferente da referência: {arv.get('a_menos', 0)} linha(s) a menos e {arv.get('a_mais', 0)} a mais")
    if resultado.get("conferencia_falha"):
        motivos.append(f"conferência '{resultado['conferencia_falha'].get('nome')}' falhou")
    tempo = registro.get("tempo_ms")
    if tempo is not None and tempo > ORCAMENTO_DE_TEMPO_MS:
        motivos.append(f"tempo de resposta {tempo:.0f} ms acima do orçamento de {ORCAMENTO_DE_TEMPO_MS} ms")
    if motivos:
        return {"reproduz": True, "motivo": "; ".join(motivos)}
    return {"reproduz": False, "motivo": "nenhuma diferença medida contra o contrato, a referência e o roteiro"}


def chamada_do_caso(chamadas: list[dict], cenario_id: str, produto_id: int | None) -> tuple[dict | None, bool]:
    """A chamada à API que o caso descreve (catálogo ou detalhe do produto) e se é mesmo a do alvo; sem ela, a última
    chamada GET do roteiro (o catálogo que quebrou antes do detalhe), marcada como não sendo a do alvo."""
    alvo = "/api/produtos" if cenario_id == "api-catalogo" else f"/api/produtos/{produto_id}"
    for c in reversed(chamadas):
        if c["metodo"] == "GET" and c["caminho"] == alvo:
            return c, True
    for c in reversed(chamadas):
        if c["metodo"] == "GET":
            return c, False
    return None, False


def _corpos_iguais(a: str | None, b: str | None) -> bool | None:
    """Os dois corpos HTTP são o mesmo dado? Compara o JSON decodificado (ordem das chaves não importa) ou o texto."""
    if a is None or b is None:
        return None
    try:
        return json.loads(a) == json.loads(b)
    except ValueError:
        return a == b


def com_produto(cenario: dict, produto_id: int | None) -> tuple[dict, int | None]:
    """O cenário de detalhe apontando para o produto do caso (ids fora do seed caem no 1, registrado)."""
    if produto_id is None:
        return cenario, None
    usado = produto_id if produto_id in IDS_DO_SEED else 1
    novo = copy.deepcopy(cenario)
    for p in novo["passos"]:
        if "seletor" in p:
            p["seletor"] = p["seletor"].replace("data-id='1'", f"data-id='{usado}'")
    return novo, usado


# ! Alteração de IA - Revisar: partes puras do pacote P3 (27/10/2026): a lista de k da linha de comando, os casos que
# reproduziram na corrida 17 (lidos do derivado oficial), o caso do fixture sem gabarito, a ponte contra a Fase 3 (regra
# R6, decisão 47, com os casos de texto corrigido fora da conta como em analisar_fase3b.mesma_entrada), quando uma
# versão do Ollama precisa de ponte, a regra R8 do k e a leitura e a gravação de `resultados_alvo/fase4/pontes.json`.
# ! Motivo: o plano fixa as regras antes das corridas que as usam (seção 5); como funções puras, elas são testadas em
# testar_fase4.py sem modelo e sem cobaias, e o executor e o avaliador leem a mesma conta.

def ler_ks(texto: str) -> tuple[int, ...]:
    """"3,5" -> (3, 5); valor que não é inteiro ou lista vazia levanta ValueError (antes de carregar o modelo)."""
    ks = tuple(int(parte.strip()) for parte in str(texto).split(",") if parte.strip())
    if not ks:
        raise ValueError(f"lista de k vazia: {texto!r}")
    return ks


def ler_ids(texto: str | None) -> list[str]:
    """"lex-1, lex-4" -> ["lex-1", "lex-4"]; None ou vazio -> [] (sem filtro)."""
    return [parte.strip() for parte in str(texto or "").split(",") if parte.strip()]


# ! Alteração de IA - Revisar: (06/11/2026, decisão 97) a corrida na tela escolhe os casos e a leitura da corrida 17 pelo banco pedido.
# ! Motivo: os 25 inéditos da ficha 27 que reproduzem na tela são a conferência limpa dos sinais da busca, que foram escritos olhando os 37 casos de avaliação; sem isto, o modo `tela` só lia esses 37.
def casos_e_reproducao_da_tela(banco: str) -> tuple[list[dict], str]:
    return casos_de_avaliacao(banco), "reproducibilidade_ineditos.json" if banco == "ineditos_fase4" else "reproducibilidade.json"


def casos_que_reproduzem(reproducibilidade: dict) -> list[str]:
    """Os ids dos casos que a corrida 17 marcou como reproduzidos na tela (resultados_alvo/fase4/reproducibilidade.json)."""
    return [c["id"] for c in reproducibilidade.get("casos", []) if c.get("reproduz")]


def fixture_sem_gabarito(caso: dict) -> dict:
    """O caso gravado como o agente o recebe: id, classe, nível e entrada; o gabarito fica de fora (plano, princípio 5)."""
    return {"id": caso["id"], "classe": caso.get("classe"), "nivel": caso.get("nivel"), "origem": "fixture",
            "entrada": copy.deepcopy(caso["entrada"])}


def _acertou(registro: dict) -> bool:
    lido = avaliar.extrair(registro.get("resposta", ""))["causa_raiz"]
    return lido is not None and avaliar._normalizar(lido) == avaliar._normalizar(registro["gabarito"]["causa_raiz"])


def ponte_contra_fase3(novos: list[dict], base: list[dict], alterados=CASOS_DE_TEXTO_ALTERADO, limite: int = LIMITE_PONTE) -> dict:
    """Pareamento caso a caso da corrida nova (L0 no Ollama atual) com a Fase 3 (L0 em 0.34.0): b = casos que só a nova
    acertou, c = só a Fase 3; os casos de texto corrigido em 28/09 saem da conta porque a Fase 3 leu o texto antigo.
    Pareável quando b + c fica no limite da decisão 47."""
    nova = {r["caso"]: _acertou(r) for r in novos}
    antiga = {r["caso"]: _acertou(r) for r in base}
    fora = sorted(set(alterados) & set(nova) & set(antiga))
    comuns = sorted((set(nova) & set(antiga)) - set(fora))
    ganhos = [c for c in comuns if nova[c] and not antiga[c]]
    perdas = [c for c in comuns if antiga[c] and not nova[c]]
    b, c = len(ganhos), len(perdas)
    return {"n": len(comuns), "b": b, "c": c, "discordantes": b + c, "ganhos": ganhos, "perdas": perdas, "pareavel": b + c <= limite,
            "limite": limite, "casos_de_texto_alterado": fora,
            "acerto_nova_pct": round(100 * sum(nova[x] for x in comuns) / len(comuns), 1) if comuns else None,
            "acerto_base_pct": round(100 * sum(antiga[x] for x in comuns) / len(comuns), 1) if comuns else None}


CASOS_DA_PONTE = 36   # os 36 casos oficiais de avaliação (decisão 47)


def ponte_completa(novos: list[dict], condicoes: dict | None = None, esperado: int = CASOS_DA_PONTE) -> bool:
    """Uma ponte só vale quando cobriu os 36 casos de avaliação e não veio de corrida parcial (`--casos`): uma ponte
    de fumaça com dois casos não pode entrar em pontes.json nem liberar a regra R6."""
    if (condicoes or {}).get("parcial"):
        return False
    return len({r.get("caso") for r in novos}) >= esperado


def versao_precisa_de_ponte(versao: str | None, pontes: dict | None) -> bool:
    """Regra R6: toda noite medida começa conferindo a versão do Ollama contra pontes.json; versão sem ponte completa,
    L0 nos 36 antes de tudo. Sem versão lida ou sem o arquivo, a ponte é necessária."""
    if not versao or not pontes:
        return True
    return not any(p.get("versao") == versao and p.get("completa", True) for p in pontes.get("pontes", []))


def ultima_ponte(pontes: dict | None, versao: str) -> dict | None:
    """A última ponte registrada para a versão (None se não há)."""
    for p in reversed((pontes or {}).get("pontes", [])):
        if p.get("versao") == versao:
            return p
    return None


def regra_r8(medida_k3: dict | None, medida_k5: dict | None, par: dict | None) -> dict:
    """Regra R8 (ficha 30 a): k = 5 entra só se acertar mais que k = 3 nos 90 por acurácia balanceada com b + c acima
    de 3; empate, b + c baixo ou k = 5 não medido ficam com k = 3, que é mais barato."""
    if not medida_k3 and medida_k5:
        return {"k": 5, "motivo": "só k = 5 foi medido (k = 3 não rodou ou ficou incompleto): fica o k = 5, sem comparação"}
    if not medida_k3:
        return {"k": 3, "motivo": "nenhum k foi medido por inteiro; fica o padrão k = 3"}
    if not medida_k5 or not par:
        return {"k": 3, "motivo": "k = 5 não foi medido por inteiro; fica o k = 3"}
    a3, a5 = medida_k3["acuracia_balanceada_pct"], medida_k5["acuracia_balanceada_pct"]
    t3, t5 = a3b.f(a3, 1), a3b.f(a5, 1)   # com vírgula decimal, como o resto dos textos
    discordantes = par["b"] + par["c"]
    if a5 > a3 and discordantes > 3:
        return {"k": 5, "motivo": f"acurácia balanceada de {t5}% contra {t3}% com b + c = {discordantes}, acima de 3"}
    if a5 > a3:
        return {"k": 3, "motivo": f"acurácia balanceada maior ({t5}% contra {t3}%), mas b + c = {discordantes} não passa de 3: fica o k = 3"}
    if a5 == a3:
        return {"k": 3, "motivo": f"empate na acurácia balanceada ({t3}%): fica o k = 3, mais barato"}
    return {"k": 3, "motivo": f"k = 3 acerta mais por acurácia balanceada ({t3}% contra {t5}%)"}


def caminho_das_pontes() -> Path:
    return caminhos.RESULTADOS / "fase4" / "pontes.json"


def carregar_pontes(gravar: bool = True) -> dict:
    """pontes.json de resultados_alvo/fase4; quando não existe, é gerado por avaliar_fase4.pontes_conhecidas a partir
    das pontes completas já rodadas (3-B e Fase 4), que é o mesmo que `avaliar_fase4.py --pontes` grava; uma corrida
    parcial lê sem gravar."""
    caminho = caminho_das_pontes()
    if caminho.exists():
        return json.loads(caminho.read_text(encoding="utf-8"))
    import avaliar_fase4 as av
    dado = av.pontes_conhecidas()
    if gravar:
        gravar_pontes(dado)
    return dado


def gravar_pontes(dado: dict) -> Path:
    caminho = caminho_das_pontes()
    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_text(json.dumps(dado, ensure_ascii=False, indent=2), encoding="utf-8")
    return caminho


# ------------------------------------------------------------------ partes puras do modo cura (P4)

def ler_lista(texto: str | None) -> list[str]:
    """"harness, php" -> ["harness", "php"]; None ou vazio -> []."""
    return [parte.strip() for parte in str(texto or "").split(",") if parte.strip()]


def celulas_da_cura(roteiros: list[str], modos: list[str], formas: list[str], repeticoes: int) -> list[dict]:
    """As células da corrida de cura, na ordem: roteiro, modo de quebra, forma da quebra e repetição (1 a N). Listas vazias
    de roteiros e modos valem "todos"; nome fora do catálogo ou repetições abaixo de 1 levantam ValueError."""
    roteiros = list(roteiros) or list(cen.ROTEIROS_DA_CURA)
    modos = list(modos) or list(cen.MODOS_DE_QUEBRA)
    for r in roteiros:
        if r not in cen.ROTEIROS_DA_CURA:
            raise ValueError(f"roteiro {r!r} fora de {cen.ROTEIROS_DA_CURA}")
    for m in modos:
        if m not in cen.MODOS_DE_QUEBRA:
            raise ValueError(f"modo de quebra {m!r} fora de {cen.MODOS_DE_QUEBRA}")
    for f in formas:
        if f not in cen.FORMAS_DE_QUEBRA:
            raise ValueError(f"forma {f!r} fora de {cen.FORMAS_DE_QUEBRA}")
    if int(repeticoes) < 1 or not formas:
        raise ValueError("a corrida precisa de ao menos uma repetição e uma forma")
    return [{"cenario": r, "modo": m, "forma": f, "repeticao": n}
            for r in roteiros for m in modos for f in formas for n in range(1, int(repeticoes) + 1)]


def id_da_celula(celula: dict) -> str:
    return f"{celula['cenario']}/{celula['modo']}/{celula['forma']}/r{celula['repeticao']}"


def mttr_da_cura(t_deteccao: float | None, t_validacao: float | None, descontar_s: float = 0.0) -> float | None:
    """Segundos da detecção (o passo do alvo falhou) à reexecução validada (o roteiro chegou ao fim), descontando o tempo
    que o harness gastou restaurando o banco entre as duas; None sem validação."""
    if t_deteccao is None or t_validacao is None:
        return None
    return round(max(0.0, t_validacao - t_deteccao - (descontar_s or 0.0)), 3)


def falha_no_passo_do_alvo(r: dict, cenario_: dict, quebra_: dict) -> bool:
    """A falha do roteiro aconteceu num passo que usa o localizador da célula? Só então é quebra de localizador e a cura
    roda; uma falha em outro passo (a página não abriu, uma conferência anterior falhou) fica registrada sem cura."""
    if r.get("passou") or r.get("passo_falho") is None:
        return False
    passos = cenario_.get("passos") or []
    i = int(r["passo_falho"])
    return 0 <= i < len(passos) and passos[i].get("seletor") == quebra_["localizador"]


def registro_da_cura(d: dict) -> dict:
    """A linha de cura.jsonl de uma execução (o que avaliar_fase4.py --cura lê)."""
    c, q, e = d["celula"], d["quebra"], d.get("escolha") or {}
    ap = e.get("aplicado") or None
    cands = [{k: x.get(k) for k in ("estrategia", "gerado", "motivo", "seletor", "passou_estaticas", "reexecutado", "efeito", "aplicado", "verificacoes", "falha")}
             for x in e.get("candidatos") or []]
    alvo = d.get("alvo") or {}
    return {"id": id_da_celula(c), "roteiro": c["cenario"], "modo": c["modo"], "forma": c["forma"], "repeticao": c["repeticao"],
            "localizador": q["localizador"], "seletor_original": q["seletor_original"], "passo_alvo": q["passo_alvo"], "descricao": q.get("descricao"),
            "alvo": {k: alvo.get(k) for k in ("papel", "nome", "ocorrencia", "tag", "caminho", "impressao")},
            "quebrou": bool(d.get("quebrou")), "passo_falho": d.get("passo_falho"), "erro": d.get("erro"), "deteccao": d.get("deteccao"), "validacao": d.get("validacao"),
            "candidatos": cands, "aplicado": ap["estrategia"] if ap else None, "seletor_curado": ap.get("seletor") if ap else None,
            "curado": bool(e.get("curado")), "mesmo_elemento": e.get("mesmo_elemento"), "falha": e.get("falha"), "resultado": e.get("resultado"),
            "segundo": (e.get("segundo") or {}).get("estrategia") if e.get("segundo") else None,
            "mttr_s": d.get("mttr_s"), "reexecucoes": e.get("reexecucoes", 0), "segundos_quebra": d.get("segundos_quebra"),
            "segundos_referencia": d.get("segundos_referencia"), "segundos_cura": d.get("segundos_cura"), "segundos_restauracao": d.get("segundos_restauracao"),
            "arvore_sha": d.get("arvore_sha"), "arvore_podada_sha": d.get("arvore_podada_sha"), "incidentes": d.get("incidentes", 0),
            "erro_da_referencia": d.get("erro_da_referencia"), "fora_do_alvo": bool(d.get("fora_do_alvo"))}


# ------------------------------------------------------------------ cobaias e API

# ! Alteração de IA - Revisar: (03/11/2026, P5) partes puras do modo `biblioteca`: a partilha determinística do conjunto de
# correção, os casos de aprendizado ligados a notas da L1 curada e com tela, e os registros compactos da corrida.
# ! Motivo: a regra R4 precisa de um conjunto desligado conhecido e auditável (a partilha por hash não depende da ordem dos
# casos, como a partição da Fase 3), e o avaliador lê `biblioteca.jsonl` e `correcoes.jsonl` por estas chaves.
def conjunto_de_correcao(ids: list[str]) -> dict:
    """Os casos ligados a notas e com tela partilhados em dois: a primeira metade (arredondada para cima) da ordem por
    sha256('correcao:' + id) tem o modo de falha desligado na reexecução; a outra fica com o modo ligado."""
    import hashlib
    import math
    regra = "sha256('correcao:' + id) ordena os casos ligados a notas e com tela; a primeira metade (arredondada para cima) tem o modo desligado, a outra fica com o modo ligado"
    ordem = sorted(set(ids), key=lambda i: hashlib.sha256(f"correcao:{i}".encode("utf-8")).hexdigest())
    n = math.ceil(len(ordem) / 2)
    return {"desligados": sorted(ordem[:n]), "mantidos": sorted(ordem[n:]), "regra": regra}


def casos_ligados_com_tela(verbetes: list[dict] | None = None) -> list[dict]:
    """Os casos de aprendizado (partição da Fase 3) ligados a notas ou verbetes da L1 curada e que têm modo e tela, por id,
    com os verbetes ligados; é o universo do ciclo de correção."""
    import biblioteca_fase4 as bf
    import diagnostico_ao_vivo as dv
    verbetes = verbetes if verbetes is not None else bib.carregar(dv.PASTA_CURADA)
    particao = e3b._particao_oficial(e3b._oficial())
    aprendizado = [c for c in e3b.TODOS_OS_CASOS if evo.particao_de(particao, c["id"]) == "aprendizado"]
    por_id = {i["id"]: i for i in selecionar_casos(aprendizado)["reproduziveis"]}
    saida = []
    for cid in sorted(por_id):
        ligados = [v["id"] for v in bf.verbetes_do_caso(verbetes, cid)]
        if ligados:
            saida.append({**por_id[cid], "verbetes": ligados})
    return saida


def registro_da_biblioteca(d: dict) -> dict:
    """A linha de biblioteca.jsonl de um caso de aprendizado: origem (tela ou fixture), o diagnóstico (rótulo, acerto, selo),
    a proposta (quantas, aceitas, para revisão, recusadas, abstenção) e os verbetes que vieram pelo id."""
    import biblioteca_fase4 as bf
    diag = d.get("diagnostico") or {}
    no = diag.get("no") or {}
    conf = no.get("confianca") or {}
    prop = d.get("proposta") or {}
    decisoes = prop.get("decisoes") or []
    return {"caso": d["caso"], "classe": d.get("classe"), "nivel": d.get("nivel"), "origem": d.get("origem"), "reproduz": d.get("reproduz"), "modo": d.get("modo"),
            "campo": d.get("campo"), "cenario": d.get("cenario"), "rotulo": no.get("escolha"), "acertou": d.get("acertou"), "p_rotulo": conf.get("p_rotulo"),
            "selo": conf.get("selo"), "divergencia": (no.get("divergencia") or {}).get("ha"), "falha": no.get("falha"), "gatilho": (diag.get("gatilhos") or {}).get("algum"),
            "segundos_diagnostico": (diag.get("registro") or {}).get("segundos"), "tokens_entrada": (diag.get("registro") or {}).get("tokens_entrada"),
            "segundos_proposta": prop.get("segundos"), "tokens_entrada_proposta": prop.get("tokens_entrada"),
            "n_propostas": prop.get("n_propostas", 0), "n_aceitas": prop.get("n_aceitas", 0), "para_revisao": len(prop.get("para_revisao") or []),
            "recusadas": [x.get("motivo") for x in decisoes if not x.get("aceita") and x.get("motivo") != bf.CODIGO_DE_REVISAO],
            "abstencao": bool(prop.get("abstencao")), "recuperacao_por_id": list(prop.get("recuperacao_por_id") or []),
            "verbetes_ligados": list(prop.get("verbetes_ligados") or []), "verbetes_editados": [x.get("verbete") for x in decisoes if x.get("aceita")],
            "segundos_cenario": d.get("segundos_cenario")}


def registro_da_correcao(c: dict) -> dict:
    """A linha de correcoes.jsonl de um caso do ciclo de correção: o que o harness fez (desligou ou manteve o modo), o que a
    reexecução mostrou, a evidência dos dois diffs, a marca do gatilho e os estados dos verbetes antes e depois."""
    ev = c.get("evidencia") or {}
    antes, depois = c.get("antes") or {}, c.get("depois") or {}
    return {"caso": c["caso"], "cenario": c.get("cenario"), "modo": c.get("modo"), "campo": c.get("campo"), "verbetes": list(c.get("verbetes") or []),
            "desligado": bool(c.get("desligado")), "reproduziu_antes": bool(antes.get("reproduz")), "passou_antes": bool(antes.get("passou")),
            "passou_depois": bool(depois.get("passou")), "ha_diff_http": bool(ev.get("ha_diff_http")), "ha_diff_arvore": bool(ev.get("ha_diff_arvore")),
            "sintoma_sumiu": bool(ev.get("sintoma_sumiu")), "marcado": bool((c.get("deteccao") or {}).get("corrigido")), "motivo": (c.get("deteccao") or {}).get("motivo"),
            "estados": {k: list(v) for k, v in (c.get("estados") or {}).items()}, "segundos": c.get("segundos"), "diff_http": ev.get("diff_http"), "diff_arvore": ev.get("diff_arvore")}


def ligar_modo(modo: str, campo: str | None, token: str = TOKEN_PADRAO, url: str = URL_ADMIN) -> dict:
    corpo = json.dumps(corpo_admin(modo, campo)).encode("utf-8")
    pedido = urllib.request.Request(url, data=corpo, method="POST",
                                    headers={"Content-Type": "application/json", "X-Admin-Token": token})
    with urllib.request.urlopen(pedido, timeout=30) as resposta:
        return json.load(resposta)


# ! Alteração de IA - Revisar: (27/10/2026) `casos_de_avaliacao` passa a receber o banco: `avaliacao` (os 72 de sempre,
# padrão), `ineditos_fase4` (os 36 inéditos da ficha 27, `banco_casos_ineditos_fase4.py`) ou `todos` (108); a opção
# `--banco` da linha de comando escolhe e `condicoes_fase4.json` registra qual foi.
# ! Motivo: a corrida 17 leu só os 72; os 36 inéditos chegaram em 27/10 e precisam ser medidos na tela do mesmo jeito,
# numa pasta própria, sem mudar o que as corridas já feitas leem nem regravar `fase4_reproducao/`.
BANCOS = ("avaliacao", "ineditos_fase4", "todos")


def casos_de_avaliacao(banco: str = "avaliacao") -> list[dict]:
    """Os casos que a corrida lê: `avaliacao` = os 36 oficiais (partição gravada pela Fase 3) mais os 36 inéditos da
    Fase 3-B; `ineditos_fase4` = os 36 inéditos da ficha 27; `todos` = os dois bancos, 108 casos."""
    if banco not in BANCOS:
        raise ValueError(f"banco desconhecido: {banco!r} (use um de {BANCOS})")
    casos: list[dict] = []
    if banco in ("avaliacao", "todos"):
        oficiais = e3b._casos_avaliacao(e3b._particao_oficial(e3b._oficial()))
        casos += oficiais + e3b._casos_ineditos()
    if banco in ("ineditos_fase4", "todos"):
        import banco_casos_ineditos_fase4 as bi4
        casos += bi4.CASOS_INEDITOS_FASE4
    return casos


def _marcador(log: Path):
    """A função `marco` de cada corrida: imprime e grava a linha com a hora em <saida>/fase4.log.
    ! Alteração de IA - Revisar: (27/10/2026, noite) a gravação tenta até dez vezes, com meio segundo de espera, e desiste
    só avisando no console: uma linha de log nunca derruba a corrida.
    ! Motivo: em 27/10 duas tentativas da corrida 16 morreram porque outro processo segurava o arquivo de log recém-criado
    por alguns segundos ("o arquivo está sendo usado por outro processo"); o mesmo pode acontecer com este arquivo."""
    def marco(msg: str) -> None:
        linha = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}"
        print(linha)
        for _ in range(10):
            try:
                with open(log, "a", encoding="utf-8") as f:
                    f.write(linha + "\n")
                return
            except OSError:
                time.sleep(0.5)
        print(f"!! não consegui gravar a linha acima em {log} (arquivo em uso por outro processo); a corrida segue")
    return marco


def _ambiente() -> dict:
    arq = caminhos.RESULTADOS / "fase4" / "ambiente.json"
    return json.loads(arq.read_text(encoding="utf-8")) if arq.exists() else {}


def _contrato_do_produto() -> str:
    openapi = json.loads((ic.FIXTURES / "openapi.json").read_text(encoding="utf-8"))
    return cv.contrato_do_openapi(openapi, "ProdutoOut", cv.AJUSTES_PRODUTO)


def derrubar_cobaias(front, api, token: str) -> None:
    """O fim de toda corrida com tela: a API volta ao modo normal, os processos do front e da API são encerrados e o
    MariaDB que a corrida subiu é desligado."""
    import _env_common as env
    try:
        ligar_modo("normal", None, token)
    except Exception:  # noqa: BLE001 - a API pode já ter caído; o modo volta ao normal no próximo boot
        pass
    for proc in (front, api):
        if proc is not None and proc.poll() is None:
            proc.terminate()
    env.stop_managed_mariadbd()


def _conferir_versao(esperada: str | None) -> None:
    """A corrida para se a versão do Ollama mudar no meio (decisão 44; regra R6)."""
    atual = executar_fase3._versao_ollama()
    if esperada is not None and atual != esperada:
        raise SystemExit(f"a versão do Ollama mudou no meio da corrida: {esperada} para {atual}; a corrida para aqui (decisão 44)")


def versoes_nas_linhas(arquivos) -> set:
    """As versões do Ollama gravadas nos registros já existentes (para um relance não misturar runtimes)."""
    return {r.get("versao_ollama") for arq in arquivos for r in executar_bateria.ler_jsonl(Path(arq))}


def _conferir_versao_das_linhas(arquivos, atual: str | None) -> None:
    """Relançar uma corrida depois de o Ollama se atualizar misturaria dois runtimes na mesma pasta: se algum registro
    já gravado tem outra versão, a corrida para antes de carregar o modelo (decisão 44; o mesmo que
    executar_fase3b._conferir_versao_ollama_uniforme acusa no fim das corridas da 3-B)."""
    outras = versoes_nas_linhas(arquivos) - {atual}
    if outras:
        raise SystemExit(f"os registros já gravados nesta saída vieram do Ollama {sorted(outras, key=str)} e o atual é {atual}: "
                         "use outra --saida (decisão 44)")


@contextlib.contextmanager
def com_guarda_de_versao(esperada: str | None):
    """Durante o bloco, cada chamada de executar_fase3.diagnosticar confere a versão do Ollama depois da inferência e
    para a corrida se ela mudou; a função original volta na saída (o mesmo molde de sonda_confianca)."""
    original = executar_fase3.diagnosticar

    def trocado(*args, **kwargs):
        registro = original(*args, **kwargs)
        _conferir_versao(esperada)
        return registro

    executar_fase3.diagnosticar = trocado
    try:
        yield
    finally:
        executar_fase3.diagnosticar = original


# ------------------------------------------------------------------ a tela: o que a corrida 17 faz por caso

# ! Alteração de IA - Revisar: (05/11/2026, ficha 42, decisão 90) o caso ao vivo da tela leva ao prompt a árvore encurtada e não leva
# mais a OBSERVAÇÃO ADICIONAL; a observação fica no caso (`observacao_da_poda`), gravada na trilha, fora de `entrada`, que é o que o
# prompt e a busca na biblioteca leem.
# ! Motivo: o limite do plano (seção 3.3) passa a valer antes da Fase 5. A OBSERVAÇÃO só repetia contagens que o CORPO e o SINTOMA já
# dizem, e pesava cerca de 250 caracteres em cada prompt; a leitura `--tela` ainda precisa dela para o bloco `tb_f4_tela_corpo`.
def caso_vivo_da_tela(item: dict, status: int | None, contrato: str, corpo_caso: str, sintoma: str, podada: dict | None, ref: dict, observacao: str,
                      corpo_completo: str | None = None, sinais_da_busca: list[str] | None = None) -> dict:
    """O caso ao vivo de um caso da tela, sem gabarito, com os metadados que o registro oficial lê (classe e nível) e o que só a busca lê:
    o corpo inteiro da resposta (decisão 96) e os fenômenos medidos contra a referência (decisão 97)."""
    arvore = cv.arvore_do_prompt(podada["texto"], ref.get("arvore"), ref.get("nomes")) if podada else None
    caso = cv.montar_caso(f"{item['id']}@tela", item["requisicao"], status, contrato, corpo_caso, sintoma, arvore=arvore or None)
    # classe e nível são metadados do caso (não o gabarito): vão no registro oficial do diagnóstico ao vivo
    caso["classe"], caso["nivel"] = item["classe"], item["nivel"]
    caso["observacao_da_poda"] = observacao
    if corpo_completo is not None:
        caso["corpo_completo"] = corpo_completo
    if sinais_da_busca:
        caso["sinais_da_busca"] = list(sinais_da_busca)
    return caso


class Tela:
    """O que `reproducao` faz por caso, reunido para os modos `reproducao` e `tela` fazerem o mesmo: a corrida de
    referência de cada cenário em modo normal (trilha dourada), o roteiro com o modo do caso ligado, a poda da árvore e
    do corpo, o diff contra o contrato e a referência, o veredito da regra R1, o sintoma por molde e o caso ao vivo; e
    a emissão dos eventos na trilha v2 (entrada, acao, interceptacao, verificacao, poda, incidente)."""

    def __init__(self, nav, trilha: tr.Trilha, saida: str, contrato: str, token: str, marco, prefixo: str | None = None) -> None:
        self.nav, self.trilha, self.saida, self.contrato, self.token, self.marco = nav, trilha, saida, contrato, token, marco
        self.prefixo = prefixo or saida
        self.referencias: dict[tuple, dict] = {}

    def referencia(self, cid: str, pid: int | None) -> dict:
        """A corrida do cenário em modo normal (trilha dourada), uma por cenário e produto, feita na primeira vez."""
        chave = (cid, pid)
        if chave in self.referencias:
            return self.referencias[chave]
        cenario_ref, _ = com_produto(cen.cenario(cid), pid)
        ligar_modo("normal", None, self.token)
        pagina = self.nav.nova_pagina()
        inter = ic.Interceptador(pagina)
        r = cen.rodar_cenario(cenario_ref, pagina, inter)
        pagina.close()
        captura = r["capturas"][-1] if r["capturas"] else {}
        podada = poda.podar_arvore(captura.get("nos") or [], captura.get("titulo") or "", alvo=cenario_ref["alvo"],
                                   interativos=captura.get("interativos"))
        chamada, _ = chamada_do_caso(r["chamadas"], cid, pid)
        corpo = inter.corpo(chamada["corpo_sha"]) if chamada and chamada.get("corpo_sha") else None
        ref = {"arvore": podada["texto"], "aria": captura.get("aria") or "", "nomes": poda.nomes_dos_nos(captura.get("nos")), "corpo": corpo, "chamada": chamada,
               "passou": r["passou"], "segundos": r["segundos"]}
        self.referencias[chave] = ref
        tid = f"{self.saida}/referencia/{cid}" + (f"/{pid}" if pid else "") + "@normal"
        trilha = self.trilha
        trilha.evento("entrada", tid, {"cenario": cid, "produto_id": pid, "modo": "normal", "referencia": True,
                                       "corpo": trilha.blob(corpo, "corpo_http") if corpo is not None else None}, "ao_vivo", ts=cen.agora())
        trilha.evento("poda", tid, {"alvo": "arvore", "antes": {"nos": podada["antes"]}, "depois": {"linhas": podada["depois"]},
                                    "regras": podada["regras"], "sha": trilha.blob(podada["texto"], "arvore_podada"), "diff": []},
                      "ao_vivo", ts=cen.agora())
        self.marco(f"referência {cid}{' produto ' + str(pid) if pid else ''}: {'passou' if r['passou'] else 'FALHOU'} em {r['segundos']} s; "
                   f"árvore {podada['antes']} nós, {podada['depois']} linhas")
        return ref

    def rodar_caso(self, item: dict) -> dict:
        """Liga o modo do caso, roda o roteiro, poda, compara com a referência, decide a regra R1 e monta o caso ao vivo."""
        cenario_, usado = com_produto(cen.cenario(item["cenario"]), item["produto_id"])
        ref = self.referencia(item["cenario"], usado)
        ligar_modo(item["modo"], item["campo"], self.token)
        pagina = self.nav.nova_pagina()
        inter = ic.Interceptador(pagina)
        r = cen.rodar_cenario(cenario_, pagina, inter)
        pagina.close()
        ligar_modo("normal", None, self.token)
        chamada, do_alvo = chamada_do_caso(r["chamadas"], item["cenario"], usado)
        corpo = inter.corpo(chamada["corpo_sha"]) if chamada and chamada.get("corpo_sha") else None
        diff = poda.diff_contrato(self.contrato, corpo if corpo is not None else "",
                                  forma_esperada=cenario_["forma"] if do_alvo else "lista") if chamada else None
        captura = r["capturas"][-1] if r["capturas"] else {}
        podada = (poda.podar_arvore(captura["nos"], captura.get("titulo") or "", alvo=cenario_["alvo"], interativos=captura.get("interativos"))
                  if captura.get("nos") else None)
        diff_arv = cv.diff_arvore(ref["arvore"], podada["texto"]) if podada else None
        diff_completa = cv.diff_arvore(ref["aria"], captura.get("aria") or "") if captura.get("aria") else None
        corpo_ref = ref["corpo"] if do_alvo else None
        comparacao = {"corpo_igual": _corpos_iguais(corpo_ref, corpo), "arvore": diff_completa}
        veredito = reproduz(r, diff, chamada, comparacao)
        status = chamada["status"] if chamada else None
        # ! Alteração de IA - Revisar: (01/11/2026, ficha 37 opção a) o corpo também é comparado com o da referência em
        # modo normal (itens a menos ou a mais, repetidos, valores item a item, tempo da chamada contra o orçamento da
        # regra R1); as frases entram no SINTOMA e, quando a poda não achou diferença de campo contra o contrato, o CORPO
        # passa a dizer a forma e a contagem da lista e o que mudou, em vez do primeiro item normal.
        # ! Motivo: corrida 18 (roadmap §2.10): 22 casos foram ao modelo com o primeiro produto normal no CORPO e 11
        # viraram colecao_no_lugar_de_objeto; nas falhas de lista e de latência o sintoma dizia "Nenhuma diferença medida".
        tempo_ref = ((ref.get("chamada") or {}).get("tempo_ms")) if do_alvo else None
        diff_ref = (cv.diff_referencia(corpo_ref, corpo, tempo_ref, chamada.get("tempo_ms") if chamada else None, orcamento_ms=ORCAMENTO_DE_TEMPO_MS)
                    if chamada else None)
        sintoma = cv.sintoma_por_molde(r["conferencia_falha"], diff, diff_completa or diff_arv, status=status, diff_ref=diff_ref)
        corpo_caso = cv.corpo_do_caso(diff, diff_ref)
        observacao = (f"poda: árvore com {podada['antes']} nós e {podada['depois']} linhas depois" if podada else "sem captura da árvore")
        if diff:
            observacao += f"; corpo {diff['corpo']}, forma {diff['forma']}, {len(diff['diferencas'])} diferença(s) contra o contrato"
        if diff_ref:
            a_mais = len(diff_ref["sobram"]) + sum(x["vezes"] - 1 for x in diff_ref["duplicados"])
            observacao += (f"; contra a referência em modo normal: {len(diff_ref['faltam'])} item(ns) a menos, {a_mais} a mais, "
                           f"{len(diff_ref['valores']) + diff_ref['valores_a_mais']} valor(es) diferente(s)")
            if diff_ref.get("tempo_ms") is not None:
                observacao += f", chamada em {diff_ref['tempo_ms']:.0f} ms" + (f" (referência {diff_ref['tempo_ref_ms']:.0f} ms)" if diff_ref.get("tempo_ref_ms") is not None else "")
        caso_vivo = caso_vivo_da_tela(item, status, self.contrato, corpo_caso, sintoma, podada, ref, observacao, corpo_completo=corpo,
                                      sinais_da_busca=cv.fenomenos_contra_a_referencia(corpo_ref, corpo, diff_ref))
        return {"item": item, "cenario": cenario_, "usado": usado, "ref": ref, "r": r, "inter": inter, "chamada": chamada, "do_alvo": do_alvo,
                "corpo": corpo, "diff": diff, "diff_ref": diff_ref, "captura": captura, "podada": podada, "diff_arv": diff_arv, "diff_completa": diff_completa,
                "comparacao": comparacao, "veredito": veredito, "status": status, "sintoma": sintoma, "observacao": observacao,
                "caso_vivo": caso_vivo}

    def emitir(self, tid: str, d: dict) -> dict:
        """Os eventos do caso na trilha; devolve os `seq` que um nó de decisão pode apontar como evidência."""
        trilha, item, r, inter = self.trilha, d["item"], d["r"], d["inter"]
        seqs: dict = {"entrada": None, "chamada": None, "poda_arvore": None, "poda_corpo": None, "interceptacoes": []}
        seqs["entrada"] = trilha.evento("entrada", tid, {"caso": item["id"], "classe": item["classe"], "nivel": item["nivel"], "modo": item["modo"],
                                                         "campo": item["campo"], "cenario": item["cenario"], "produto_id": d["usado"],
                                                         "caso_ao_vivo": trilha.blob(json.dumps(d["caso_vivo"], ensure_ascii=False, sort_keys=True), "caso_ao_vivo")},
                                        "ao_vivo", ts=r["inicio"])
        for i, (passo, tempo) in enumerate(zip(d["cenario"]["passos"], r["tempos_ms"])):
            trilha.evento("acao", tid, {"passo": i + 1, "acao": passo["acao"], "seletor": passo.get("seletor"), "url": passo.get("url"),
                                        "tempo_ms": tempo, "falhou": r["passo_falho"] == i}, "ao_vivo", ts=cen.agora())
        for c in r["chamadas"]:
            dados = {k: v for k, v in c.items() if k != "url"}
            dados["corpo"] = trilha.blob(inter.corpo(c["corpo_sha"]), "corpo_http") if c.get("corpo_sha") and inter.corpo(c["corpo_sha"]) is not None else None
            s = trilha.evento("interceptacao", tid, dados, "ao_vivo", ts=cen.agora())
            seqs["interceptacoes"].append(s)
            if c is d["chamada"]:
                seqs["chamada"] = s
        for conf in r["conferencias"]:
            trilha.evento("verificacao", tid, tr._v("conferencia_do_roteiro", conf["nome"], "confere" if conf["passou"] else "nao_confere",
                                                    {"esperado": conf["esperado"], "observado": conf["observado"]}), "ao_vivo", ts=cen.agora())
        podada, diff, diff_arv, corpo = d["podada"], d["diff"], d["diff_arv"], d["corpo"]
        if podada:
            seqs["poda_arvore"] = trilha.evento("poda", tid, {"alvo": "arvore", "antes": {"nos": podada["antes"]}, "depois": {"linhas": podada["depois"]},
                                                              "regras": podada["regras"], "sha": trilha.blob(podada["texto"], "arvore_podada"),
                                                              "diff": [{"campo": "arvore", "esperado": f"{diff_arv['a_menos']} linha(s) da referência", "recebido": f"{diff_arv['a_mais']} linha(s) novas"}] if diff_arv else []},
                                                "ao_vivo", ts=cen.agora())
        if diff is not None:
            # ! Alteração de IA - Revisar: (27/10/2026, P3) corpo que não é JSON (truncado, vazio, não JSON) entra no diff do
            # evento de poda como uma linha sem campo, antes das diferenças campo a campo.
            # ! Motivo: `poda.diff_contrato` não lista diferenças de campo quando o corpo nem chegou a ser JSON, e o nó de
            # diagnóstico ficava sem sinal em código na evidência (a fumaça da corrida 18 com `malformed_json` mostrou a
            # justificativa recorrendo ao diff da árvore); a linha diz o que se esperava e o que veio.
            linhas_diff = ([{"campo": None, "esperado": "JSON completo e válido", "recebido": f"corpo {diff['corpo']}", "tipo": diff["corpo"]}]
                           if diff.get("corpo") != "json" else [])
            # ! Alteração de IA - Revisar: (05/11/2026, ficha 41) a linha leva o item quando a diferença só aparece a partir do segundo.
            # ! Motivo: o relatório do caso na tela precisa dizer onde está a diferença, como o do caso de texto.
            linhas_diff += [{"campo": x["campo"], "esperado": x.get("esperado"), "recebido": x.get("recebido"), "tipo": x["tipo"], **({"item": x["item"]} if x.get("item") else {})} for x in diff["diferencas"]]
            # ! Alteração de IA - Revisar: (01/11/2026, ficha 37 opção a) o evento de poda do corpo passa a gravar o CORPO que
            # foi ao modelo (não só o trecho do contrato), a regra `diff_contra_referencia` quando houve referência e uma
            # linha de sinal em código por diferença contra a referência (itens, valores, tempo).
            # ! Motivo: a justificativa do nó de decisão lê esses sinais; sem eles o relatório da corrida 18 atribuía o
            # rótulo ao diff da árvore mesmo quando a lista tinha um item a menos ou a chamada levou 28 s.
            corpo_caso = (d["caso_vivo"].get("entrada") or {}).get("corpo") or ""
            linhas_diff += cv.linhas_diff_da_referencia(d.get("diff_ref"))
            seqs["poda_corpo"] = trilha.evento("poda", tid, {"alvo": "corpo_http", "antes": {"chars": len(corpo or "")}, "depois": {"chars": len(corpo_caso)},
                                                             "regras": ["diff_contra_contrato"] + (["diff_contra_referencia"] if d.get("diff_ref") else []),
                                                             "sha": trilha.blob(corpo_caso, "corpo_podado"), "diff": linhas_diff}, "ao_vivo", ts=cen.agora())
        for inc in inter.incidentes:
            trilha.evento("incidente", tid, inc, "ao_vivo", ts=cen.agora())
        return seqs


def registro_da_reproducao(d: dict) -> dict:
    """A linha de reproducao.jsonl de um caso (a mesma da corrida 17)."""
    item, r, chamada, diff, podada = d["item"], d["r"], d["chamada"], d["diff"], d["podada"]
    diff_arv, diff_completa, corpo, inter = d["diff_arv"], d["diff_completa"], d["corpo"], d["inter"]
    return {"id": item["id"], "classe": item["classe"], "nivel": item["nivel"], "causa": item["causa"], "modo": item["modo"],
            "campo": item["campo"], "cenario": item["cenario"], "produto_id": item["produto_id"], "produto_id_usado": d["usado"],
            "requisicao": item["requisicao"], "reproduz": d["veredito"]["reproduz"], "motivo": d["veredito"]["motivo"],
            "status": d["status"], "tempo_ms": chamada.get("tempo_ms") if chamada else None, "segundos": r["segundos"],
            "chamada_do_alvo": d["do_alvo"], "chamada_caminho": chamada.get("caminho") if chamada else None,
            "corpo_igual_referencia": d["comparacao"]["corpo_igual"],
            "arvore_completa_a_menos": diff_completa["a_menos"] if diff_completa else None,
            "arvore_completa_a_mais": diff_completa["a_mais"] if diff_completa else None,
            "passou_o_roteiro": r["passou"], "passo_falho": r["passo_falho"],
            "conferencia_falha": (r["conferencia_falha"] or {}).get("nome"), "erro": r["erro"],
            "arvore_antes": podada["antes"] if podada else None, "arvore_depois": podada["depois"] if podada else None,
            "arvore_a_menos": diff_arv["a_menos"] if diff_arv else None, "arvore_a_mais": diff_arv["a_mais"] if diff_arv else None,
            "corpo_chars": len(corpo) if corpo is not None else None, "caso_chars": cv.tamanho_do_caso(d["caso_vivo"]),
            "diff": {"corpo": diff["corpo"], "forma": diff["forma"], "itens": diff["itens"], "tipos": sorted({x["tipo"] for x in diff["diferencas"]})} if diff else None,
            "sintoma": d["sintoma"], "incidentes": len(inter.incidentes), "chamadas": len(r["chamadas"])}


# ------------------------------------------------------------------ a corrida 17: reprodução na tela, sem modelo

def rodar_reproducao(args: argparse.Namespace) -> int:
    import _env_common as env
    import restaurar_banco as rb
    import run

    saida = caminhos.fase3(args.saida)["raiz"]
    saida.mkdir(parents=True, exist_ok=True)
    marco = _marcador(saida / "fase4.log")
    inicio = cen.agora()
    t0 = time.monotonic()
    versoes = _ambiente().get("versoes", {})
    contrato = _contrato_do_produto()
    banco = getattr(args, "banco", "avaliacao")
    todos = casos_de_avaliacao(banco)
    sel = selecionar_casos(todos)
    if args.casos:
        sel["reproduziveis"] = sel["reproduziveis"][:args.casos]
    condicoes = {"modo": "reproducao", "criado_em": inicio, "saida": args.saida, "banco": banco, "versoes": versoes, "canal": args.canal,
                 "regra_r1": "status != 200, corpo fora do JSON, diff do contrato, corpo ou árvore completa diferentes da referência em modo "
                             "normal, conferência do roteiro falhou ou tempo da chamada acima do orçamento",
                 "hosts_permitidos": list(ic.HOSTS_PERMITIDOS), "hosts_har": list(ic.CDN_PADRAO), "hosts_silenciosos": list(ic.HOSTS_SILENCIOSOS),
                 "limites": tr.LIMITES_PADRAO, "orcamento_de_tempo_ms": ORCAMENTO_DE_TEMPO_MS, "contrato": contrato,
                 "casos": len(todos), "reproduziveis": len(sel["reproduziveis"]), "fora": len(sel["fora"]), "modelo": None}
    (saida / "condicoes_fase4.json").write_text(json.dumps(condicoes, ensure_ascii=False, indent=2), encoding="utf-8")
    (saida / "fora.json").write_text(json.dumps(sel["fora"], ensure_ascii=False, indent=1), encoding="utf-8")
    marco(f"INÍCIO reproducao (banco {banco}): {len(todos)} casos, {len(sel['reproduziveis'])} reproduzíveis na tela, {len(sel['fora'])} fora")

    front, api = run.start_services()
    trilha = tr.Trilha(versao=tr.V2, pasta_blobs=saida / "blobs")
    trilha.corrida(tr.cabecalho_de_corrida(modelo="(sem modelo: reprodução na tela)", versao_ollama=str(versoes.get("ollama") or "não medida"),
                                           inicio=inicio, playwright=versoes.get("playwright"), navegador=versoes.get("navegador"),
                                           canal=args.canal, corrida=args.saida, etapas_registradas=["roteiro", "interceptacao", "poda", "caso_ao_vivo"],
                                           etapas_nao_registradas=["diagnostico", "cura", "edicao_biblioteca"],
                                           extras={"modo": "reproducao", "hash_biblioteca": None, "banco": banco}), ts=inicio)
    registros: list[dict] = []
    arq_registros = saida / "reproducao.jsonl"
    if arq_registros.exists():
        arq_registros.unlink()
    try:
        if not run.wait_until_ready(timeout_s=90):
            marco("!! as cobaias não responderam nas portas 8080 e 8000")
            return 2
        cli = env.find_mysql_cli()
        if rb.restaurar(cli) != rb.CONTAGENS_DO_SEED:
            marco("!! o banco restaurado não tem as contagens do seed")
            return 2
        with navegador.Navegador(canal=args.canal) as nav:
            tela = Tela(nav, trilha, args.saida, contrato, args.token, marco)
            for cid in ("api-catalogo", "api-detalhe"):
                tela.referencia(cid, 1 if cid == "api-detalhe" else None)
            for n, item in enumerate(sel["reproduziveis"], 1):
                d = tela.rodar_caso(item)
                tela.emitir(f"{args.saida}/{item['id']}@tela", d)
                registro = registro_da_reproducao(d)
                registros.append(registro)
                with open(arq_registros, "a", encoding="utf-8") as f:
                    f.write(json.dumps(registro, ensure_ascii=False) + "\n")
                marco(f"[{n}/{len(sel['reproduziveis'])}] {item['id']} ({item['modo']}{' em ' + item['campo'] if item['campo'] else ''}): "
                      f"{'REPRODUZ' if registro['reproduz'] else 'não reproduz'}: {registro['motivo']} ({registro['segundos']} s)")
    finally:
        derrubar_cobaias(front, api, args.token)
    fim = cen.agora()
    trilha.fechar(fim)
    trilha.gravar(saida / "trilha_reproducao.jsonl")
    reproduzem = sum(1 for r in registros if r["reproduz"])
    marco(f"FIM reproducao: {reproduzem} de {len(registros)} casos reproduzem na tela; {len(sel['fora'])} fora; "
          f"duração {time.monotonic() - t0:.0f} s; trilha {(saida / 'trilha_reproducao.jsonl').stat().st_size} bytes")
    return 0


# ------------------------------------------------------------------ a corrida 16: calibração e ponte (texto, com modelo)

def rodar_calibracao(args: argparse.Namespace) -> int:
    """Corrida 16 (plano, P3, noite A): sondagem dos logprobs, ponte de versão se a versão não tem ponte (R6), a L1
    curada nos 90 casos oficiais com cada k (pelo executor congelado da Fase 3, com a linha lateral de probabilidades
    como na corrida 12), a regra R8 e os limiares do selo (R7). Relançar retoma do caso em que parou."""
    import avaliar_fase4 as av
    import diagnostico_ao_vivo as dv

    saida = caminhos.fase3(args.saida)["raiz"]
    saida.mkdir(parents=True, exist_ok=True)
    marco = _marcador(saida / "fase4.log")
    inicio = cen.agora()
    t0 = time.monotonic()
    modelo = args.modelo
    slug = executar_fase3._slug(modelo)
    parcial = bool(args.casos)
    ks = ler_ks(args.k or K_PADRAO)
    versao = executar_fase3._versao_ollama()
    if versao is None:
        marco("!! o Ollama não respondeu em /api/version; suba o servidor antes da calibração")
        return 2
    if not evo.snapshot_fechado(dv.PASTA_CURADA):
        marco(f"!! a cópia curada em {dv.PASTA_CURADA} não existe ou não está fechada (sem fechamento.json)")
        return 2
    hash_curada = evo.hash_biblioteca(dv.PASTA_CURADA)
    pontes = carregar_pontes(gravar=not parcial)
    precisa = versao_precisa_de_ponte(versao, pontes)
    c3_of = e3b._oficial()
    particao = e3b._particao_oficial(c3_of)
    casos90 = list(e3b.TODOS_OS_CASOS)
    casos36 = e3b._casos_avaliacao(particao)
    if args.casos:
        casos90, casos36 = casos90[:args.casos], casos36[:args.casos]
    anterior = ultima_ponte(pontes, versao)
    try:
        _conferir_versao_das_linhas([saida / f"k{k}" / slug / f"diagnosticos__L{dv.VERSAO_CURADA}.jsonl" for k in ks]
                                    + [saida / "ponte" / slug / "diagnosticos__L0.jsonl"], versao)
    except SystemExit as e:
        marco(f"!! {e}")
        return 2
    condicoes = {"modo": "calibracao", "criado_em": inicio, "saida": args.saida, "modelo": modelo, "versao_ollama": versao, "k": list(ks),
                 "casos": len(casos90), "casos_da_ponte": len(casos36), "parcial": parcial,
                 "biblioteca": {"rotulo": dv.ROTULO_CURADA, "versao": dv.VERSAO_CURADA, "hash": hash_curada, "origem": "Programacao/AgenteCore/biblioteca_producao"},
                 "top_logprobs": args.top, "teto_tokens": args.teto, "leitura_da_probabilidade": dv.LEITURA_DA_PROBABILIDADE,
                 "parcela_baixa": dv.PARCELA_BAIXA, "ponte_necessaria": precisa, "ponte_anterior": anterior,
                 "regras": {"R6": f"versão sem ponte em pontes.json: L0 nos 36 antes de tudo; pareável com b + c até {LIMITE_PONTE} (decisão 47)",
                            "R7": "limiares do selo pela curva risco-cobertura dos 90 casos, gravados em limiares.json antes da primeira corrida na tela",
                            "R8": "k = 5 só se acertar mais que k = 3 por acurácia balanceada com b + c acima de 3; empate fica com k = 3"},
                 "limites": tr.LIMITES_PADRAO}
    (saida / "condicoes_fase4.json").write_text(json.dumps(condicoes, ensure_ascii=False, indent=2), encoding="utf-8")
    marco(f"INÍCIO calibracao: Ollama {versao}, {modelo}, {dv.ROTULO_CURADA} ({hash_curada}) nos {len(casos90)} casos com k em {list(ks)}; "
          f"ponte {'necessária' if precisa else 'já feita (' + anterior['corrida'] + ')'}{'; corrida PARCIAL' if parcial else ''}")
    resultado: dict = {"sondagem": None, "ponte": None, "ks": {}}

    def _tudo() -> None:
        digest, versao_ollama = e3b._preparar_modelo(modelo)
        if versao_ollama != versao:
            raise SystemExit(f"a versão do Ollama mudou antes de começar: {versao} para {versao_ollama}")
        verbetes = bib.carregar(dv.PASTA_CURADA)
        indice = rec.Indice(verbetes)
        marco("sondagem dos logprobs: três chamadas no Ollama instalado")
        sondagem = dv.sondagem_logprobs(modelo, casos36[0], verbetes, indice, k=ks[0], top=args.top, teto=args.teto,
                                        versao_ollama=versao_ollama, digest=digest)
        (saida / "sondagem_logprobs.json").write_text(json.dumps(sondagem, ensure_ascii=False, indent=2), encoding="utf-8")
        ok, mensagens = dv.sondagem_aceita(sondagem)
        resultado["sondagem"] = sondagem
        marco(f"sondagem: {'ok' if ok else 'PROBLEMA'}; {'; '.join(mensagens) or 'sem avisos'}")
        if not ok:
            raise SystemExit("a sondagem dos logprobs reprovou o Ollama instalado: " + "; ".join(mensagens))
        _conferir_versao(versao)
        if precisa:
            marco(f"ponte de versão (regra R6): L0 nos {len(casos36)} casos de avaliação em Ollama {versao}")
            nome_p = f"{args.saida}/ponte"
            c3p = e3b.preparar_saida(nome_p, particao)
            e3b._gravar_condicoes(c3p, modo="ponte", doador=None, versoes=[0], texto_max=None, condicao=executar_fase3.CONDICAO,
                                  modelos=[modelo], versao_ollama=versao_ollama)
            arq_cond_p = c3p["raiz"] / "condicoes_3b.json"
            cond_p = json.loads(arq_cond_p.read_text(encoding="utf-8"))
            cond_p.update({"parcial": parcial, "casos": len(casos36), "casos_esperados": CASOS_DA_PONTE})
            arq_cond_p.write_text(json.dumps(cond_p, ensure_ascii=False, indent=2), encoding="utf-8")
            pasta_p, bib_p = c3p["raiz"] / slug, c3p["bibliotecas"] / slug
            e3b._preparar_copia(c3_of["bibliotecas"] / slug / "epoca-0", bib_p / "epoca-0")
            with com_guarda_de_versao(versao):
                e3b._diagnosticar_versao(modelo, 0, casos36, particao, pasta_p, bib_p, 3, args.teto, 700, digest, versao_ollama)
            p = ponte_contra_fase3(executar_bateria.ler_jsonl(pasta_p / "diagnosticos__L0.jsonl"),
                                   executar_bateria.ler_jsonl(c3_of["raiz"] / slug / "diagnosticos__L0.jsonl"))
            resultado["ponte"] = {"versao": versao, "corrida": nome_p, "data": cen.agora()[:10], "modelo": modelo, "feita_nesta_corrida": True,
                                  "completa": not parcial, **p}
            marco(f"ponte: b = {p['b']}, c = {p['c']} em {p['n']} casos; {'pareável' if p['pareavel'] else 'NÃO pareável'} com a Fase 3 (limite {p['limite']})")
            if not parcial:
                gravar_pontes(av.pontes_conhecidas(modelo))
                marco(f"pontes.json regravado com a ponte de {versao}")
        else:
            resultado["ponte"] = {**anterior, "feita_nesta_corrida": False}
            marco(f"ponte: a versão {versao} já tem ponte ({anterior['corrida']}: b = {anterior.get('b')}, c = {anterior.get('c')}); nada a refazer")
        for k in ks:
            nome_k = f"{args.saida}/k{k}"
            c3k = e3b.preparar_saida(nome_k, particao)
            e3b._gravar_condicoes(c3k, modo="calibracao", doador=None, versoes=[dv.VERSAO_CURADA], texto_max=None, condicao=executar_fase3.CONDICAO,
                                  modelos=[modelo], versao_ollama=versao_ollama)
            arq_cond = c3k["raiz"] / "condicoes_3b.json"
            cond = json.loads(arq_cond.read_text(encoding="utf-8"))
            cond.update({"top_logprobs": args.top, "k": k, "casos": len(casos90),
                         "conjuntos": {"aprendizado": sum(1 for c in casos90 if evo.particao_de(particao, c["id"]) == "aprendizado"),
                                       "avaliacao": sum(1 for c in casos90 if evo.particao_de(particao, c["id"]) == "avaliacao")},
                         "curada": {"versao": dv.VERSAO_CURADA, "hash": hash_curada, "origem": "Programacao/AgenteCore/biblioteca_producao", "rotulo": dv.ROTULO_CURADA}})
            arq_cond.write_text(json.dumps(cond, ensure_ascii=False, indent=2), encoding="utf-8")
            pasta_k, bib_k = c3k["raiz"] / slug, c3k["bibliotecas"] / slug
            e3b._preparar_copia(dv.PASTA_CURADA, bib_k / f"epoca-{dv.VERSAO_CURADA}")
            marco(f"{dv.ROTULO_CURADA} nos {len(casos90)} casos com k = {k}")
            capturas: list = []
            with sl.com_logprobs(args.top, capturas, exigir=True), sc.diagnostico_com_lateral(pasta_k, capturas, args.top), com_guarda_de_versao(versao):
                e3b._diagnosticar_versao(modelo, dv.VERSAO_CURADA, casos90, particao, pasta_k, bib_k, k, args.teto, 700, digest, versao_ollama)
            n = len(executar_bateria.ler_jsonl(pasta_k / f"diagnosticos__L{dv.VERSAO_CURADA}.jsonl"))
            resultado["ks"][k] = n
            marco(f"k = {k}: {n} registros em {pasta_k}")

    try:
        e3b._com_modelo_descarregado(modelo, _tudo)
    except SystemExit as e:
        marco(f"!! calibração parou: {e}")
        return 1
    dado = av.resumir_calibracao(av.ler_calibracao(args.saida), corrida=args.saida)
    lim = dado["limiares"]
    if parcial:
        caminho = dv.gravar_limiares(lim, saida / "limiares_parcial.json")
        marco(f"corrida parcial: limiares gravados só em {caminho.name} (o limiares.json oficial fica para a corrida completa)")
    else:
        caminho = dv.gravar_limiares(lim)
        marco(f"limiares do selo (regra R7) em {caminho}: baixo até {lim.get('baixo_ate')}, alto a partir de {lim.get('alto_a_partir_de')}; "
              f"k pela regra R8: {dado['r8']['k']} ({dado['r8']['motivo']})")
    marco(f"FIM calibracao: {', '.join(f'k = {k}: {n} registros' for k, n in resultado['ks'].items())}; "
          f"ponte {'feita' if (resultado['ponte'] or {}).get('feita_nesta_corrida') else 'já registrada'}; duração {time.monotonic() - t0:.0f} s")
    return 0


# ------------------------------------------------------------------ a corrida 18: diagnóstico ao vivo e o mesmo caso do fixture

def rodar_tela(args: argparse.Namespace) -> int:
    """Corrida 18 (plano, P3, noite B): para cada caso que reproduziu na corrida 17, o caso montado na tela (como lá)
    e diagnosticado ao vivo e, logo depois e na mesma sessão do Ollama, o mesmo caso lido do fixture sem gabarito.
    Relançar retoma dos casos que faltam; a trilha é gravada a cada caso."""
    import _env_common as env
    import diagnostico_ao_vivo as dv
    import gerar_relatorio_raciocinio as grr
    import restaurar_banco as rb
    import run

    saida = caminhos.fase3(args.saida)["raiz"]
    saida.mkdir(parents=True, exist_ok=True)
    marco = _marcador(saida / "fase4.log")
    inicio = cen.agora()
    t0 = time.monotonic()
    modelo = args.modelo
    slug = executar_fase3._slug(modelo)
    parcial = bool(args.casos)
    versao = executar_fase3._versao_ollama()
    if versao is None:
        marco("!! o Ollama não respondeu em /api/version; suba o servidor antes da corrida")
        return 2
    limiares = dv.carregar_limiares(Path(args.limiares) if args.limiares else None)
    if limiares is None:
        if not parcial:
            marco("!! sem limiares.json (regra R7): rode --modo calibracao antes da primeira corrida na tela")
            return 2
        marco("aviso: sem limiares.json; a corrida parcial segue sem selo e sem gatilho por probabilidade")
    pontes = carregar_pontes(gravar=not parcial)
    if versao_precisa_de_ponte(versao, pontes):
        if not parcial:
            marco(f"!! a versão {versao} do Ollama não tem ponte completa registrada (regra R6): rode --modo calibracao antes")
            return 2
        marco(f"aviso: a versão {versao} do Ollama não tem ponte completa registrada; a corrida parcial segue")
    k = ler_ks(args.k)[0] if args.k else int((limiares or {}).get("k") or 3)
    ids_pedidos = ler_ids(args.ids)
    versoes = _ambiente().get("versoes", {})
    contrato = _contrato_do_produto()
    todos, nome_rep = casos_e_reproducao_da_tela(args.banco)
    arq_rep = caminhos.RESULTADOS / "fase4" / nome_rep
    por_id = {c["id"]: c for c in todos}
    sel = selecionar_casos(todos)
    if arq_rep.exists():
        ids = set(casos_que_reproduzem(json.loads(arq_rep.read_text(encoding="utf-8"))))
        itens = [i for i in sel["reproduziveis"] if i["id"] in ids]
        origem_dos_casos = f"os {len(itens)} casos que reproduzem em {arq_rep.name} (corrida 17)"
    else:
        itens = sel["reproduziveis"]
        origem_dos_casos = f"todos os {len(itens)} casos com tela e modo (sem {arq_rep.name})"
        marco(f"aviso: {origem_dos_casos}")
    if ids_pedidos:
        itens = [i for i in itens if i["id"] in set(ids_pedidos)]
        origem_dos_casos += f"; filtrados por --ids: {', '.join(ids_pedidos)}"
    if args.casos:
        itens = itens[:args.casos]
    amostra = tuple(c["id"] for c in e3b._casos_avaliacao(e3b._particao_oficial(e3b._oficial()))) if args.amostra else ()
    if not evo.snapshot_fechado(dv.PASTA_CURADA):
        marco(f"!! a cópia curada em {dv.PASTA_CURADA} não existe ou não está fechada (sem fechamento.json)")
        return 2
    pasta_bib = saida / "bibliotecas" / slug / f"epoca-{dv.VERSAO_CURADA}"
    hash_curada = e3b._preparar_copia(dv.PASTA_CURADA, pasta_bib)
    verbetes = bib.carregar(pasta_bib)
    indice = rec.Indice(verbetes)
    exemplo = fixture_sem_gabarito(por_id[itens[0]["id"]] if itens else todos[0])
    ctx0, prompt0 = dv.montar_prompt(verbetes, indice, exemplo, k)
    hash_fixo = dv.hash_prompt_fixo(verbetes, ctx0, exemplo, prompt0)
    pasta_reg = saida / slug
    pasta_reg.mkdir(parents=True, exist_ok=True)
    arq_tela, arq_fix = pasta_reg / "diagnosticos__tela.jsonl", pasta_reg / "diagnosticos__fixture.jsonl"
    lat_tela, lat_fix = pasta_reg / "logprobs__tela.jsonl", pasta_reg / "logprobs__fixture.jsonl"
    arq_resumo, arq_trilha = saida / "tela.jsonl", saida / "trilha_tela.jsonl"
    # um caso só conta como feito quando a linha de tela.jsonl existe: ela é gravada depois dos dois registros e da
    # trilha, então um relance refaz o caso que caiu no meio (o avaliador lê o último registro de cada caso)
    feitos = {r["caso"] for r in executar_bateria.ler_jsonl(arq_resumo)}
    try:
        _conferir_versao_das_linhas([arq_tela, arq_fix], versao)
    except SystemExit as e:
        marco(f"!! {e}")
        return 2
    condicoes = {"modo": "tela", "criado_em": inicio, "saida": args.saida, "modelo": modelo, "versao_ollama": versao, "k": k,
                 "limiares": limiares, "intervencoes": args.intervencoes, "amostra": len(amostra), "top_logprobs": args.top, "teto_tokens": args.teto,
                 "leitura_da_probabilidade": dv.LEITURA_DA_PROBABILIDADE, "parcial": parcial, "casos": len(itens), "banco": args.banco, "origem_dos_casos": origem_dos_casos,
                 "biblioteca": {"rotulo": dv.ROTULO_CURADA, "versao": dv.VERSAO_CURADA, "hash": hash_curada, "origem": "Programacao/AgenteCore/biblioteca_producao"},
                 "hash_prompt_fixo": hash_fixo, "hash_indice": dv.hash_indice(indice), "versoes": versoes, "canal": args.canal,
                 "hosts_permitidos": list(ic.HOSTS_PERMITIDOS), "hosts_har": list(ic.CDN_PADRAO), "hosts_silenciosos": list(ic.HOSTS_SILENCIOSOS),
                 "limites": tr.LIMITES_PADRAO, "orcamento_de_tempo_ms": ORCAMENTO_DE_TEMPO_MS, "contrato": contrato, "versao_do_caso_ao_vivo": cv.VERSAO_DO_CASO, "sinais_da_referencia_na_busca": cv.SINAIS_DA_REFERENCIA_NA_BUSCA,
                 # ! Alteração de IA - Revisar: (06/11/2026, decisão 98) o texto da regra nas condições da corrida passa a dizer a leitura fixada antes da corrida 18d.
                 # ! Motivo: as condições gravadas junto da corrida são o que se confere depois; com a frase antiga, a 18d pareceria medida pela soma dos dois lados.
                 "regra_r2": "nos casos que reproduzem, a tela não perde mais de 3 casos para o mesmo caso lido do fixture, na mesma sessão do Ollama (c até 3; b e a soma ficam ao lado, decisão 98)"}
    (saida / "condicoes_fase4.json").write_text(json.dumps(condicoes, ensure_ascii=False, indent=2), encoding="utf-8")
    marco(f"INÍCIO tela: Ollama {versao}, {modelo}, {dv.ROTULO_CURADA} ({hash_curada}), k = {k}, intervenções {args.intervencoes}; "
          f"{origem_dos_casos}{'; corrida PARCIAL' if parcial else ''}; {len(feitos)} já feito(s)")

    front, api = run.start_services()
    resumos = executar_bateria.ler_jsonl(arq_resumo)
    trilha: tr.Trilha | None = None
    try:
        if not run.wait_until_ready(timeout_s=90):
            marco("!! as cobaias não responderam nas portas 8080 e 8000")
            return 2
        cli = env.find_mysql_cli()
        if rb.restaurar(cli) != rb.CONTAGENS_DO_SEED:
            marco("!! o banco restaurado não tem as contagens do seed")
            return 2
        digest, versao_ollama = e3b._preparar_modelo(modelo)
        if versao_ollama != versao:
            marco(f"!! a versão do Ollama mudou antes de começar: {versao} para {versao_ollama}")
            return 2
        comum = {"digest": digest, "versao_ollama": versao_ollama, "maquina": platform.node(), "epoca": dv.VERSAO_CURADA + 1,
                 "biblioteca_epoca": dv.VERSAO_CURADA, "biblioteca_versao": hash_curada, "particao": None, "k": k, "teto_tokens": args.teto}
        with navegador.Navegador(canal=args.canal) as nav:
            v = nav.versao()
            if arq_trilha.exists() and feitos:
                trilha = tr.Trilha.carregar(arq_trilha)
                trilha.pasta_blobs = saida / "blobs"
                marco(f"retomando a trilha de {arq_trilha.name}: {len(trilha.eventos)} eventos")
            else:
                trilha = tr.Trilha(versao=tr.V2, pasta_blobs=saida / "blobs")
                trilha.corrida(tr.cabecalho_de_corrida(modelo=modelo, versao_ollama=versao, inicio=inicio, quantizacao=dv.quantizacao_do_modelo(modelo),
                                                       top_logprobs=args.top, leitura_da_probabilidade=dv.LEITURA_DA_PROBABILIDADE,
                                                       hash_biblioteca=hash_curada, hash_prompt_fixo=hash_fixo, hash_indice=dv.hash_indice(indice),
                                                       playwright=v["playwright"], navegador=v["navegador"], canal=args.canal, corrida=args.saida,
                                                       etapas_registradas=["roteiro", "interceptacao", "poda", "caso_ao_vivo", "recuperacao", "prompt",
                                                                           "diagnostico", "intervencao"],
                                                       etapas_nao_registradas=["cura", "edicao_biblioteca"],
                                                       extras={"modo": "tela", "k": k, "limiares": limiares, "intervencoes": args.intervencoes,
                                                               "amostra": len(amostra)}), ts=inicio)
            tela = Tela(nav, trilha, args.saida, contrato, args.token, marco, prefixo=f"{args.saida}/{slug}")

            def _loop() -> None:
                for cid in ("api-catalogo", "api-detalhe"):
                    tela.referencia(cid, 1 if cid == "api-detalhe" else None)
                for n, item in enumerate(itens, 1):
                    if item["id"] in feitos:
                        marco(f"[{n}/{len(itens)}] {item['id']}: já feito, pulando")
                        continue
                    d = tela.rodar_caso(item)
                    tid = f"{args.saida}/{slug}/{item['id']}@tela"
                    seqs = tela.emitir(tid, d)
                    evidencia = []
                    if seqs.get("poda_corpo"):
                        evidencia.append({"seq": seqs["poda_corpo"], "papel": "sinal_em_codigo"})
                    if seqs.get("poda_arvore"):
                        evidencia.append({"seq": seqs["poda_arvore"], "papel": "arvore_podada"})
                    if seqs.get("chamada"):
                        evidencia.append({"seq": seqs["chamada"], "papel": "corpo_http"})
                    sv = dv.diagnosticar(trilha, tid, d["caso_vivo"], verbetes, indice, k=k, modelo=modelo, comum=comum, limiares=limiares,
                                         intervencoes=args.intervencoes, amostra=amostra, top=args.top, teto=args.teto, evidencia=evidencia, ts=cen.agora())
                    executar_fase3._gravar(arq_tela, sv["registro"])
                    executar_fase3._gravar(lat_tela, sv["lateral"])
                    _conferir_versao(versao)
                    caso_f = fixture_sem_gabarito(por_id[item["id"]])
                    tid_f = f"{args.saida}/{slug}/{item['id']}@fixture"
                    trilha.evento("entrada", tid_f, {"caso": item["id"], "classe": item["classe"], "nivel": item["nivel"], "origem": "fixture",
                                                     "texto": trilha.blob(estrategias._dados_do_caso(caso_f), "caso")}, "ao_vivo", ts=cen.agora())
                    sf = dv.diagnosticar(trilha, tid_f, caso_f, verbetes, indice, k=k, modelo=modelo, comum=comum, limiares=limiares,
                                         intervencoes=args.intervencoes, amostra=amostra, top=args.top, teto=args.teto, ts=cen.agora())
                    executar_fase3._gravar(arq_fix, sf["registro"])
                    executar_fase3._gravar(lat_fix, sf["lateral"])
                    rt, rf = sv["no"]["escolha"], sf["no"]["escolha"]
                    resumo = {"caso": item["id"], "classe": item["classe"], "nivel": item["nivel"], "modo": item["modo"], "campo": item["campo"],
                              "cenario": item["cenario"], "reproduz": d["veredito"]["reproduz"], "motivo": d["veredito"]["motivo"],
                              "rotulo_tela": rt, "rotulo_fixture": rf, "concordam": rt is not None and rt == rf,
                              "p_tela": sv["no"]["confianca"]["p_rotulo"], "p_fixture": sf["no"]["confianca"]["p_rotulo"],
                              "selo_tela": sv["no"]["confianca"]["selo"], "selo_fixture": sf["no"]["confianca"]["selo"],
                              "gatilhos_tela": sv["gatilhos"], "gatilhos_fixture": sf["gatilhos"],
                              "intervencoes_tela": len(sv["intervencoes"]), "intervencoes_fixture": len(sf["intervencoes"]),
                              "divergencia_tela": sv["no"]["divergencia"]["ha"], "divergencia_fixture": sf["no"]["divergencia"]["ha"],
                              "falha_tela": sv["no"]["falha"], "falha_fixture": sf["no"]["falha"],
                              "segundos_tela": sv["registro"]["segundos"], "segundos_fixture": sf["registro"]["segundos"],
                              "segundos_cenario": d["r"]["segundos"], "tokens_entrada_tela": sv["registro"]["tokens_entrada"],
                              "tokens_entrada_fixture": sf["registro"]["tokens_entrada"], "chars_prompt_tela": sv["chars_prompt"],
                              "chars_prompt_fixture": sf["chars_prompt"], "caso_chars": cv.tamanho_do_caso(d["caso_vivo"])}
                    trilha.gravar(arq_trilha)
                    executar_fase3._gravar(arq_resumo, resumo)
                    resumos.append(resumo)
                    _conferir_versao(versao)
                    pt = "n/d" if resumo["p_tela"] is None else f"{resumo['p_tela']:.2f}"
                    pf_ = "n/d" if resumo["p_fixture"] is None else f"{resumo['p_fixture']:.2f}"
                    marco(f"[{n}/{len(itens)}] {item['id']} ({item['modo']}): tela {rt} (p {pt}, selo {resumo['selo_tela']}) | "
                          f"fixture {rf} (p {pf_}, selo {resumo['selo_fixture']}) | {'concordam' if resumo['concordam'] else 'DISCORDAM'} | "
                          f"{resumo['segundos_tela']} + {resumo['segundos_fixture']} s")

            e3b._com_modelo_descarregado(modelo, _loop)
    except SystemExit as e:
        marco(f"!! corrida parou: {e}")
        return 1
    finally:
        derrubar_cobaias(front, api, args.token)
    fim = cen.agora()
    if trilha is not None:
        trilha.fechar(fim)
        trilha.gravar(arq_trilha)
        if not args.sem_relatorios:
            pasta_rel = saida / "relatorios"
            pasta_rel.mkdir(exist_ok=True)
            flags = f" --k {k}" + (f" --limiares {args.limiares}" if args.limiares else "") + (f" --intervencoes {args.intervencoes}" if args.intervencoes != "desligadas" else "") \
                + (" --amostra" if args.amostra else "")
            for tid in tr.por_trilha(trilha.eventos):
                if "@tela" in tid or "@fixture" in tid:
                    nome = tid.rsplit("/", 1)[-1]
                    # o comando reexecuta só este caso, numa saída própria (na mesma saída o caso contaria como feito)
                    comando = (f"RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida {args.saida}_reexec "
                               f"--ids {nome.split('@')[0]}{flags}")
                    (pasta_rel / f"{nome}.md").write_text(grr.relatorio_do_caso_v2(trilha.eventos, tid, comando_reexecucao=comando, pasta_blobs=saida / "blobs"),
                                                          encoding="utf-8", newline="\n")
    concordam = sum(1 for r in resumos if r.get("concordam"))
    tamanho = arq_trilha.stat().st_size if arq_trilha.exists() else 0
    marco(f"FIM tela: {len(resumos)} de {len(itens)} casos diagnosticados na tela e no fixture; concordam {concordam}; "
          f"duração {time.monotonic() - t0:.0f} s; trilha {tamanho} bytes")
    return 0


# ------------------------------------------------------------------ a corrida 19: cura de seletor, sem modelo

# ! Alteração de IA - Revisar: (05/11/2026, ficha 42, decisão 90) a árvore podada e os nomes de todos os nós da corrida sem quebra,
# capturados no passo do alvo, para o caso ao vivo da quebra de localizador comparar com a tela quebrada.
# ! Motivo: a referência da cura só guardava o alvo, e o caso do localizador levava a árvore inteira ao prompt (na lista de produtos,
# a mesma dupla de botões 14 vezes); com a árvore da referência, o prompt mostra o que a quebra mudou. Sem captura, {}: o caso cai no
# corte sem referência, e a cura não muda.
def arvore_da_referencia(captura: dict | None, alvo: dict | None) -> dict:
    if not captura or not captura.get("nos"):
        return {}
    podada = poda.podar_arvore(captura["nos"], captura.get("titulo") or "", alvo=alvo, interativos=captura.get("interativos"))
    return {"arvore": podada["texto"], "nomes": poda.nomes_dos_nos(captura["nos"])}


class Cura:
    """O que o modo `cura` faz por célula: a corrida de referência da célula sem quebra (registra o alvo do passo), o
    roteiro com a quebra armada até o passo falhar (detecção), a poda da árvore da página quebrada, os candidatos
    gerados e verificados em código na página aberta (com um diagnóstico no meio, numa página refeita até o passo que falhou),
    a reexecução do roteiro com o primeiro candidato que passa (com a quebra armada de novo), a regra R3 pela impressão do DOM
    e os eventos da trilha v2."""

    def __init__(self, nav, trilha: tr.Trilha, saida: str, token: str, marco, cli: str | None, base: str = cen.BASE_PADRAO) -> None:
        self.nav, self.trilha, self.saida, self.token, self.marco, self.cli, self.base = nav, trilha, saida, token, marco, cli, base
        self.referencias: dict[tuple, dict] = {}

    def _restaurar(self) -> float:
        import restaurar_banco as rb
        t0 = time.monotonic()
        if self.cli and rb.restaurar(self.cli) != rb.CONTAGENS_DO_SEED:
            self.marco("!! o banco restaurado não tem as contagens do seed")
        return time.monotonic() - t0

    def referencia(self, q: dict) -> dict:
        """A corrida da célula sem quebra: o roteiro com o localizador da célula passa, e o alvo do passo é descrito antes
        de o passo rodar (papel e nome pela árvore de acessibilidade; tag, atributos, caminho, pai, posição e impressão pelo
        DOM). Uma por célula (roteiro e modo), feita na primeira vez."""
        chave = (q["cenario"], q["modo"])
        if chave in self.referencias:
            return self.referencias[chave]
        base_cen = cen.cenario(q["cenario"])
        cenario_ = cen.cenario_com_localizador(base_cen, q)
        if base_cen.get("restaura_banco"):
            self._restaurar()
        pagina = self.nav.nova_pagina()
        inter = ic.Interceptador(pagina)
        descr: dict = {}

        def antes(i: int, passo: dict, pg) -> None:
            if i == q["passo_alvo"] and "alvo" not in descr:
                try:
                    descr["alvo"] = cs.descrever_elemento(pg, q["localizador"])
                except Exception as e:  # noqa: BLE001 - a descrição falhou: fica registrado e a célula não tem alvo
                    descr["erro"] = f"{type(e).__name__}: {str(e)[:200]}"
                try:
                    descr["captura"] = inter.capturar()
                except Exception:  # noqa: BLE001 - sem a árvore da referência, o caso do localizador usa o corte sem referência
                    descr["captura"] = None

        r = cen.rodar_cenario(cenario_, pagina, inter, base=self.base, capturar=False, antes_do_passo=antes)
        pagina.close()
        alvo = descr.get("alvo")
        ref = {**arvore_da_referencia(descr.get("captura"), q.get("alvo")), "alvo": alvo, "passou": r["passou"], "segundos": r["segundos"], "erro": r["erro"], "conferencia_falha": r["conferencia_falha"],
               "erro_descricao": descr.get("erro") or (None if alvo else f"o localizador {q['localizador']!r} não resolveu na página sem quebra")}
        self.referencias[chave] = ref
        tid = f"{self.saida}/referencia/{q['cenario']}/{q['modo']}@normal"
        self.trilha.evento("entrada", tid, {"roteiro": q["cenario"], "modo": q["modo"], "referencia": True, "localizador": q["localizador"], "passo": q["passo_alvo"],
                                            "passou": r["passou"], "segundos": r["segundos"], "erro": r["erro"],
                                            "alvo": self.trilha.blob(json.dumps(alvo, ensure_ascii=False, sort_keys=True), "alvo_da_referencia") if alvo else None,
                                            "erro_descricao": ref["erro_descricao"]}, "ao_vivo", ts=cen.agora())
        self.marco(f"referência {q['cenario']} ({q['modo']}, localizador {q['localizador']}): {'passou' if r['passou'] else 'FALHOU: ' + str(r['erro'] or r['conferencia_falha'])} "
                   f"em {r['segundos']} s; alvo {alvo['papel'] + ' \"' + alvo['nome'] + '\"' if alvo else 'NÃO descrito (' + str(ref['erro_descricao']) + ')'}")
        return ref

    # ! Alteração de IA - Revisar: (04/11/2026, P6) a troca do seletor passa para cenarios_fase4.roteiro_com_seletor.
    # ! Motivo: a conferência da linha de base manual (conferir_localizador_manual.py) usa a mesma troca que a reexecução da cura.
    def _roteiro_curado(self, cenario_: dict, q: dict, candidato: dict) -> dict:
        return cen.roteiro_com_seletor(cenario_, q, candidato["seletor"])

    # ! Alteração de IA - Revisar: (04/11/2026, leitura da corrida 21) _refazer_ate_o_passo: uma página nova, com a quebra armada, e o
    # roteiro até antes do passo que falhou; devolve a página, o interceptador e o que aconteceu (para a trilha).
    # ! Motivo: é o estado em que os candidatos da cura têm de ser verificados. A página da detecção fica parada enquanto o modelo
    # diagnostica, e nada garante que ela continue igual: na corrida 21 a tela de login voltou sozinha para a página inicial (meta
    # refresh de 30 s em admin/login.php) durante os 55 s do diagnóstico. Os passos refeitos vêm antes do passo que falhou, então não
    # gravam no banco (a reserva só grava no clique em Reservar, que é o passo quebrado).
    def _refazer_ate_o_passo(self, cenario_: dict, q: dict, forma: str, passo_falho: int) -> tuple:
        pagina = self.nav.nova_pagina()
        cen.armar_quebra(pagina, q, forma, self.base)
        inter = ic.Interceptador(pagina)
        r = cen.rodar_cenario({**cenario_, "passos": cenario_["passos"][:passo_falho]}, pagina, inter, base=self.base, capturar=False,
                              tempo_limite_ms=cen.TEMPO_LIMITE_QUEBRA_MS)
        return pagina, inter, {"passou": r["passou"], "passos": passo_falho, "segundos": r["segundos"], "erro": r["erro"]}

    # ! Alteração de IA - Revisar: (04/11/2026, P6) executar ganha `apos_deteccao`, chamado com a execução já detectada e podada,
    # antes dos candidatos da cura; o resultado guarda também t_deteccao e t_validacao (relógio monotônico).
    # ! Motivo: no cenário de localizador da Fase 5 o agente diagnostica entre a detecção e a cura (plano, seção 3.1), e o MTTR
    # (da detecção à reexecução validada) tem de incluir esse diagnóstico para ser comparável à linha de base manual; o modo
    # `cura` chama sem o gancho e mede como antes.
    # ! Alteração de IA - Revisar: (04/11/2026, P7) executar aceita `quebra`, uma quebra já montada, no lugar da do catálogo.
    # ! Motivo: a mutação do seletor da avaliação da trilha (avaliacao_trilha.quebra_do_seletor) é a quebra do catálogo mais uma
    # mutação que troca o nome acessível do alvo, num modo que não está em cenarios_fase4.QUEBRAS; sem `quebra`, nada muda.
    def executar(self, celula: dict, apos_deteccao=None, quebra: dict | None = None) -> dict:
        """Uma execução: a quebra armada, o roteiro até falhar, a cura e a reexecução; devolve tudo para o registro e a trilha."""
        q = quebra if quebra is not None else cen.quebra(celula["cenario"], celula["modo"])
        ref = self.referencia(q)
        base_cen = cen.cenario(q["cenario"])
        cenario_ = cen.cenario_com_localizador(base_cen, q)
        t_inicio = time.monotonic()
        if base_cen.get("restaura_banco"):
            self._restaurar()                      # antes da detecção: não entra no MTTR
        pagina = self.nav.nova_pagina()
        armado = cen.armar_quebra(pagina, q, celula["forma"], self.base)
        inter = ic.Interceptador(pagina)
        r = cen.rodar_cenario(cenario_, pagina, inter, base=self.base, capturar=False, tempo_limite_ms=cen.TEMPO_LIMITE_QUEBRA_MS)
        quebrou = not r["passou"]
        try:
            captura = inter.capturar()
        except Exception as e:  # noqa: BLE001 - página fechada ou navegando: a cura fica sem árvore e isso é registrado
            captura = {"erro": f"{type(e).__name__}: {str(e)[:200]}", "nos": [], "aria": "", "titulo": "", "interativos": []}
        podada = poda.podar_arvore(captura.get("nos") or [], captura.get("titulo") or "", alvo=q["alvo"], interativos=captura.get("interativos"))
        quebra_aplicada = None
        try:
            quebra_aplicada = pagina.evaluate("document.documentElement.dataset.quebraAplicada || null")
        except Exception:  # noqa: BLE001
            pass
        d: dict = {"celula": celula, "quebra": q, "armado": armado, "quebra_aplicada": quebra_aplicada, "ref": ref, "alvo": ref.get("alvo"), "r": r, "quebrou": quebrou,
                   "passo_falho": r["passo_falho"], "erro": r["erro"], "deteccao": r["deteccao"], "validacao": None, "escolha": None, "candidatos": [],
                   "podada": podada, "captura": captura, "arvore_sha": tr.sha(captura.get("aria") or ""), "arvore_podada_sha": tr.sha(podada["texto"]),
                   "incidentes": len(inter.incidentes), "inter": inter, "reexecucoes": [], "mttr_s": None, "segundos_quebra": r["segundos"],
                   "segundos_referencia": ref.get("segundos"), "segundos_restauracao": 0.0, "erro_da_referencia": ref.get("erro_descricao")}
        d["fora_do_alvo"] = quebrou and not falha_no_passo_do_alvo(r, cenario_, q)
        d["t_deteccao"], d["t_validacao"], d["diagnostico"], d["pagina_refeita"] = r.get("t_deteccao"), None, None, None
        if quebrou and ref.get("alvo") and not d["fora_do_alvo"]:
            if apos_deteccao is not None:
                d["diagnostico"] = apos_deteccao(d)
                # ! Alteração de IA - Revisar: (04/11/2026, leitura da corrida 21) depois do diagnóstico, a verificação dos candidatos vai
                # para uma página refeita até o passo que falhou; o tempo de refazer entra no MTTR. Sem diagnóstico (modo `cura`), nada muda.
                # ! Motivo: ver _refazer_ate_o_passo: na corrida 21 os candidatos do login deram "nenhum elemento" porque a página da
                # detecção já tinha navegado sozinha, e o cenário ficou sem cura; a mesma célula curou 10 de 10 na corrida 19, sem modelo.
                pagina.close()
                pagina, _inter_refeita, d["pagina_refeita"] = self._refazer_ate_o_passo(cenario_, q, celula["forma"], r["passo_falho"])
            alvo = ref["alvo"]
            cands = cs.gerar_candidatos(alvo, podada["texto"])
            d["candidatos"] = cands
            estado = {"restauracoes": 0.0, "tentativas": 0, "t_validacao": None}

            def resolver(c: dict) -> dict:
                return cs.resolver_no_navegador(pagina, c)

            def reexecutar(c: dict) -> dict:
                estado["tentativas"] += 1
                if estado["tentativas"] > 1 and base_cen.get("restaura_banco"):
                    estado["restauracoes"] += self._restaurar()      # uma tentativa anterior pode ter gravado; o tempo é descontado do MTTR
                pagina2 = self.nav.nova_pagina()
                cen.armar_quebra(pagina2, q, celula["forma"], self.base)
                inter2 = ic.Interceptador(pagina2)
                impressao: dict = {}

                def antes(i: int, passo: dict, pg) -> None:
                    if i == q["passo_alvo"] and "valor" not in impressao:
                        impressao["valor"] = cs.impressao_do_candidato(pg, c)

                r2 = cen.rodar_cenario(self._roteiro_curado(cenario_, q, c), pagina2, inter2, base=self.base, capturar=False,
                                       tempo_limite_ms=cen.TEMPO_LIMITE_QUEBRA_MS, antes_do_passo=antes)
                t_fim = time.monotonic()
                pagina2.close()
                passou = cen.task_success(r2)
                if passou and estado["t_validacao"] is None:
                    estado["t_validacao"] = t_fim
                d["reexecucoes"].append({"candidato": c["estrategia"], "seletor": c["seletor"], "r": r2, "incidentes": len(inter2.incidentes), "passou": passou})
                if passou:
                    detalhe = f"o roteiro chegou ao fim: {len(r2['conferencias'])} conferência(s) passaram em {r2['segundos']} s"
                else:
                    cf = r2.get("conferencia_falha") or {}
                    detalhe = (f"falhou no passo {(r2['passo_falho'] or 0) + 1}: {cf.get('nome')}: esperava {cf.get('esperado')}; viu {str(cf.get('observado'))[:120]}"
                               if cf else f"falhou: {r2.get('erro')}")
                return {"passou": passou, "detalhe": detalhe, "mesmo_elemento": cs.mesmo_elemento(alvo.get("impressao"), impressao.get("valor")) if passou else None,
                        "segundos": r2["segundos"], "impressao": impressao.get("valor")}

            d["escolha"] = cs.escolher(cands, resolver, reexecutar, alvo)
            d["segundos_restauracao"] = round(estado["restauracoes"], 3)
            if d["escolha"]["curado"]:
                d["validacao"] = cen.agora()
                d["t_validacao"] = estado["t_validacao"]
                d["mttr_s"] = mttr_da_cura(r.get("t_deteccao"), estado["t_validacao"], estado["restauracoes"])
        pagina.close()
        d["segundos_cura"] = round(time.monotonic() - t_inicio, 3)
        return d

    # ! Alteração de IA - Revisar: (04/11/2026, P6) emitir passa a ser emitir_quebra (entrada, ações e conferências do roteiro
    # quebrado, poda) seguido de emitir_cura (incidentes, evento e nó da cura, reexecuções e nó da reexecução), na mesma ordem
    # de antes; o modo `cura` continua chamando emitir.
    # ! Motivo: no cenário de localizador da Fase 5 o agente diagnostica entre a detecção e a cura (plano, seção 3.1), dentro do
    # Cura.executar; a trilha precisa do roteiro quebrado antes dos eventos do diagnóstico, e da cura depois deles.
    def emitir(self, tid: str, d: dict) -> None:
        """Os eventos da execução na trilha v2: entrada, as ações e conferências do roteiro quebrado, a poda, o evento `cura`,
        o nó `cura`, as ações e conferências das reexecuções e o nó `reexecucao`; incidentes por último."""
        self.emitir_cura(tid, d, self.emitir_quebra(tid, d))

    def emitir_quebra(self, tid: str, d: dict, extras: dict | None = None) -> dict:
        """A primeira metade de emitir: entrada (com `extras`, como o caso ao vivo do cenário de localizador), ações e
        conferências do roteiro quebrado e a poda; devolve os seq."""
        trilha, celula, q, r = self.trilha, d["celula"], d["quebra"], d["r"]
        alvo = d.get("alvo")
        s_ent = trilha.evento("entrada", tid, {"roteiro": celula["cenario"], "modo": celula["modo"], "forma": celula["forma"], "repeticao": celula["repeticao"],
                                               "passo": q["passo_alvo"], "localizador": q["localizador"], "seletor_original": q["seletor_original"],
                                               "descricao": q.get("descricao"), "armado": d.get("armado"), "quebra_aplicada": d.get("quebra_aplicada"),
                                               "mutacoes": q["mutacoes"], "alvo": alvo, "erro_da_referencia": d.get("erro_da_referencia"), **(extras or {})},
                              "ao_vivo", ts=r["inicio"])
        cenario_ = cen.cenario_com_localizador(cen.cenario(q["cenario"]), q)
        for i, (passo, tempo) in enumerate(zip(cenario_["passos"], r["tempos_ms"])):
            trilha.evento("acao", tid, {"passo": i + 1, "acao": passo["acao"], "seletor": passo.get("seletor"), "url": passo.get("url"), "tempo_ms": tempo,
                                        "falhou": r["passo_falho"] == i, "reexecucao": 0}, "ao_vivo", pai=s_ent, ts=cen.agora())
        for conf in r["conferencias"]:
            trilha.evento("verificacao", tid, tr._v("conferencia_do_roteiro", conf["nome"], "confere" if conf["passou"] else "nao_confere",
                                                    {"esperado": conf["esperado"], "observado": conf["observado"], "reexecucao": 0}), "ao_vivo", pai=s_ent, ts=cen.agora())
        podada = d["podada"]
        s_poda = trilha.evento("poda", tid, {"alvo": "arvore", "antes": {"nos": podada["antes"]}, "depois": {"linhas": podada["depois"]}, "regras": podada["regras"],
                                             "sha": trilha.blob(podada["texto"], "arvore_podada"), "diff": [], "arvore_completa_sha": d.get("arvore_sha")},
                               "ao_vivo", pai=s_ent, ts=cen.agora())
        return {"s_ent": s_ent, "s_poda": s_poda}

    def emitir_cura(self, tid: str, d: dict, seqs: dict) -> None:
        """A segunda metade de emitir: os incidentes do roteiro, o evento e o nó da cura, as reexecuções, o nó da reexecução e
        os incidentes do interceptador."""
        import gerar_relatorio_raciocinio as grr
        trilha, q, r = self.trilha, d["quebra"], d["r"]
        alvo = d.get("alvo")
        s_ent, s_poda = seqs["s_ent"], seqs["s_poda"]
        cenario_ = cen.cenario_com_localizador(cen.cenario(q["cenario"]), q)
        if not d["quebrou"]:
            trilha.evento("incidente", tid, {"tipo": "quebra_nao_detectada", "detalhe": "o roteiro passou com a quebra armada: o localizador da célula sobreviveu à mutação"},
                          "ao_vivo", pai=s_ent, ts=cen.agora())
        elif d.get("fora_do_alvo"):
            trilha.evento("incidente", tid, {"tipo": "falha_fora_do_passo_do_alvo", "passo_falho": r["passo_falho"],
                                             "detalhe": "o roteiro falhou num passo que não usa o localizador da célula: não é quebra de localizador, a cura não roda"},
                          "ao_vivo", pai=s_ent, ts=cen.agora())
        elif d.get("escolha") is None:
            trilha.evento("incidente", tid, {"tipo": "sem_alvo_na_referencia", "detalhe": d.get("erro_da_referencia")}, "ao_vivo", pai=s_ent, ts=cen.agora())
        else:
            e = d["escolha"]
            dados_cura = cs.evento_de_cura(e, alvo, localizador=q["localizador"], passo=q["passo_alvo"] + 1, erro=r["erro"] or ((r.get("conferencia_falha") or {}).get("nome")),
                                           deteccao=r["deteccao"], validacao=d.get("validacao"), mttr_s=d.get("mttr_s"))
            if d.get("pagina_refeita"):
                dados_cura["pagina_refeita"] = d["pagina_refeita"]     # a verificação rodou numa página refeita, depois do diagnóstico
            s_cura = trilha.evento("cura", tid, dados_cura, "ao_vivo", pai=s_poda, ts=cen.agora())
            trilha.decisao(tid, cs.no_de_cura(e, seq_cura=s_cura, seq_poda=s_poda, justificativa=grr.justificativa_da_cura(dados_cura)), pai=s_cura, ts=cen.agora())
            seqs = []
            for n, rx in enumerate(d["reexecucoes"], 1):
                r2 = rx["r"]
                curado_ = self._roteiro_curado(cenario_, q, {"seletor": rx["seletor"]})
                for i, (passo, tempo) in enumerate(zip(curado_["passos"], r2["tempos_ms"])):
                    trilha.evento("acao", tid, {"passo": i + 1, "acao": passo["acao"], "seletor": passo.get("seletor"), "url": passo.get("url"), "tempo_ms": tempo,
                                                "falhou": r2["passo_falho"] == i, "reexecucao": n, "candidato": rx["candidato"], "curado": bool(passo.get("curado"))},
                                  "ao_vivo", pai=s_cura, ts=cen.agora())
                for conf in r2["conferencias"]:
                    seqs.append(trilha.evento("verificacao", tid, tr._v("conferencia_do_roteiro", conf["nome"], "confere" if conf["passou"] else "nao_confere",
                                                                          {"esperado": conf["esperado"], "observado": conf["observado"], "reexecucao": n, "candidato": rx["candidato"]}),
                                              "ao_vivo", pai=s_cura, ts=cen.agora()))
            trilha.decisao(tid, cs.no_de_reexecucao(e, seq_cura=s_cura, seqs_verificacoes=seqs), pai=s_cura, ts=cen.agora())
        for inc in d["inter"].incidentes:
            trilha.evento("incidente", tid, inc, "ao_vivo", pai=s_ent, ts=cen.agora())


def rodar_cura(args: argparse.Namespace) -> int:
    """Corrida 19 (plano, P4; sem modelo): as células da cura nas duas formas da ficha 29 c, com o banco restaurado antes de
    cada execução que grava; retomada pelas linhas de cura.jsonl; trilha gravada a cada dez células e no fim; relatórios v2."""
    import _env_common as env
    import gerar_relatorio_raciocinio as grr
    import restaurar_banco as rb
    import run

    saida = caminhos.fase3(args.saida)["raiz"]
    saida.mkdir(parents=True, exist_ok=True)
    marco = _marcador(saida / "fase4.log")
    inicio = cen.agora()
    t0 = time.monotonic()
    versoes = _ambiente().get("versoes", {})
    erros = cen.validar_quebras(cen.QUEBRAS, cen.CENARIOS)
    if erros:
        marco("!! catálogo de quebras com erro: " + "; ".join(erros))
        return 2
    formas = ler_lista(args.formas) or list(cen.FORMAS_DE_QUEBRA)
    try:
        celulas = celulas_da_cura(ler_lista(args.roteiros), ler_lista(args.modos), formas, args.repeticoes)
    except ValueError as e:
        marco(f"!! {e}")
        return 2
    parcial = bool(args.roteiros or args.modos or args.repeticoes != REPETICOES_PADRAO or len(formas) != len(cen.FORMAS_DE_QUEBRA))
    condicoes = {"modo": "cura", "criado_em": inicio, "saida": args.saida, "repeticoes": args.repeticoes, "formas": formas,
                 "roteiros": ler_lista(args.roteiros) or list(cen.ROTEIROS_DA_CURA), "modos_de_quebra": ler_lista(args.modos) or list(cen.MODOS_DE_QUEBRA),
                 "celulas": len(celulas), "parcial": parcial, "limiar_nome": cs.LIMIAR_NOME, "estrategias": list(cs.ESTRATEGIAS), "verificacoes": list(cs.VERIFICACOES),
                 "tempo_limite_ms": cen.TEMPO_LIMITE_QUEBRA_MS, "cookie_da_quebra": cen.COOKIE_DA_QUEBRA, "descricao_dos_modos": cen.DESCRICAO_DO_MODO,
                 "quebras": cen.QUEBRAS, "versoes": versoes, "canal": args.canal, "modelo": None,
                 "regra_r3": "uma cura só conta quando a conferência final do roteiro passa na reexecução; o relatório separa mesmo elemento do alvo original "
                             "de outro elemento que fez o roteiro passar (pela impressão do DOM: tag, type, name, action do formulário, data-nome, href)",
                 "mttr": "da detecção (o passo do alvo falhou) à reexecução validada (o roteiro chegou ao fim), descontado o tempo de restaurar o banco entre as duas",
                 "hosts_permitidos": list(ic.HOSTS_PERMITIDOS), "hosts_har": list(ic.CDN_PADRAO), "hosts_silenciosos": list(ic.HOSTS_SILENCIOSOS), "limites": tr.LIMITES_PADRAO}
    (saida / "condicoes_fase4.json").write_text(json.dumps(condicoes, ensure_ascii=False, indent=2), encoding="utf-8")
    arq_reg, arq_trilha = saida / "cura.jsonl", saida / "trilha_cura.jsonl"
    registros = executar_bateria.ler_jsonl(arq_reg)
    feitos = {r["id"] for r in registros}
    marco(f"INÍCIO cura: {len(celulas)} células ({len(condicoes['roteiros'])} roteiros x {len(condicoes['modos_de_quebra'])} modos x {len(formas)} formas x "
          f"{args.repeticoes} repetições){'; corrida PARCIAL' if parcial else ''}; {len(feitos)} já feita(s); limiar do nome {cs.LIMIAR_NOME}")
    front, api = run.start_services()
    trilha: tr.Trilha | None = None
    try:
        if not run.wait_until_ready(timeout_s=90):
            marco("!! as cobaias não responderam nas portas 8080 e 8000")
            return 2
        cli = env.find_mysql_cli()
        if rb.restaurar(cli) != rb.CONTAGENS_DO_SEED:
            marco("!! o banco restaurado não tem as contagens do seed")
            return 2
        with navegador.Navegador(canal=args.canal) as nav:
            v = nav.versao()
            if arq_trilha.exists() and feitos:
                trilha = tr.Trilha.carregar(arq_trilha)
                trilha.pasta_blobs = saida / "blobs"
                marco(f"retomando a trilha de {arq_trilha.name}: {len(trilha.eventos)} eventos")
            else:
                trilha = tr.Trilha(versao=tr.V2, pasta_blobs=saida / "blobs")
                trilha.corrida(tr.cabecalho_de_corrida(modelo="(sem modelo: cura de seletor)", versao_ollama=str(versoes.get("ollama") or "não medida"), inicio=inicio,
                                                       playwright=v["playwright"], navegador=v["navegador"], canal=args.canal, corrida=args.saida,
                                                       etapas_registradas=["roteiro", "quebra", "poda", "cura", "reexecucao"],
                                                       etapas_nao_registradas=["interceptacao", "diagnostico", "edicao_biblioteca"],
                                                       extras={"modo": "cura", "hash_biblioteca": None, "repeticoes": args.repeticoes, "formas": formas,
                                                               "limiar_nome": cs.LIMIAR_NOME}), ts=inicio)
            cura = Cura(nav, trilha, args.saida, args.token, marco, cli)
            for n, celula in enumerate(celulas, 1):
                cid = id_da_celula(celula)
                if cid in feitos:
                    marco(f"[{n}/{len(celulas)}] {cid}: já feita, pulando")
                    continue
                d = cura.executar(celula)
                cura.emitir(f"{args.saida}/{cid}", d)
                registro = registro_da_cura(d)
                registros.append(registro)
                with open(arq_reg, "a", encoding="utf-8") as f:
                    f.write(json.dumps(registro, ensure_ascii=False) + "\n")
                if not registro["quebrou"]:
                    estado = "não quebrou (o localizador sobreviveu à mutação)"
                elif registro["curado"]:
                    estado = (f"CURADO por {registro['aplicado']} ({registro['seletor_curado']}); {'mesmo' if registro['mesmo_elemento'] else 'OUTRO' if registro['mesmo_elemento'] is False else 'elemento não comparado'}"
                              f"{' elemento' if registro['mesmo_elemento'] is not None else ''}; MTTR {registro['mttr_s']} s; {registro['reexecucoes']} reexecução(ões)")
                elif registro["fora_do_alvo"]:
                    estado = f"falhou no passo {registro['passo_falho']}, fora do passo do alvo ({str(registro['erro'])[:80]}): sem cura"
                else:
                    estado = f"NÃO curado ({registro['falha'] or registro.get('erro_da_referencia')}; {registro['reexecucoes']} reexecução(ões))"
                marco(f"[{n}/{len(celulas)}] {cid}: {estado} ({registro['segundos_cura']} s)")
                if n % 10 == 0:
                    trilha.gravar(arq_trilha)
    finally:
        derrubar_cobaias(front, api, args.token)
    fim = cen.agora()
    if trilha is not None:
        trilha.fechar(fim)
        trilha.gravar(arq_trilha)
        if not args.sem_relatorios:
            pasta_rel = saida / "relatorios"
            pasta_rel.mkdir(exist_ok=True)
            for tid in tr.por_trilha(trilha.eventos):
                partes = tid.split("/")
                if "/referencia/" in tid or len(partes) < 5:
                    continue
                roteiro, modo, forma, rep = partes[-4], partes[-3], partes[-2], partes[-1]
                comando = (f"RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo cura --saida {args.saida}_reexec --roteiros {roteiro} --modos {modo} "
                           f"--formas {forma} --repeticoes 1")
                (pasta_rel / f"{roteiro}__{modo}__{forma}__{rep}.md").write_text(
                    grr.relatorio_do_caso_v2(trilha.eventos, tid, comando_reexecucao=comando, pasta_blobs=saida / "blobs"), encoding="utf-8", newline="\n")
    quebradas = [r for r in registros if r["quebrou"]]
    curadas = [r for r in quebradas if r["curado"]]
    tamanho = arq_trilha.stat().st_size if arq_trilha.exists() else 0
    marco(f"FIM cura: {len(registros)} de {len(celulas)} execuções; {len(quebradas)} quebraram; {len(curadas)} curadas "
          f"({sum(1 for r in curadas if r['mesmo_elemento'])} mesmo elemento, {sum(1 for r in curadas if r['mesmo_elemento'] is False)} outro); "
          f"duração {time.monotonic() - t0:.0f} s; trilha {tamanho} bytes")
    return 0


# ! Alteração de IA - Revisar: (27/10/2026) o parser saiu de `main` para `montar_parser` e ganhou `--banco`.
# ! Motivo: o teste confere o padrão e as escolhas da opção sem rodar a corrida, e `main` continua igual por fora.
# ------------------------------------------------------------------ a corrida 20: biblioteca em produção e ciclo de correção

# ! Alteração de IA - Revisar: (04/11/2026) ao refazer a fase C, a trilha perde tudo desde o primeiro evento de um caso
# '@correcao' (as telas de antes e depois, os blobs, a edição e o nó de cada caso da tentativa anterior).
# ! Motivo: a fase C é refeita do zero quando a época 102 ou o correcoes.jsonl faltam, mas a trilha é recarregada do
# arquivo e cada caso seria gravado de novo atrás do anterior: os 10 casos apareceriam duas vezes na trilha e nos
# relatórios '@correcao'. A fase C é o fim da trilha (a sonda não escreve nela), então o corte não leva nada das fases A e
# B. É o caminho da retomada da corrida 20 em 04/11/2026, depois do conserto da ordem das seções da correção.
MARCA_DA_CORRECAO = "@correcao"


def descartar_eventos_da_correcao(trilha: tr.Trilha) -> int:
    """Tira da trilha os eventos da fase C (do primeiro evento cuja trilha contém '@correcao' em diante) e devolve quantos
    saíram (0 quando a trilha não tem evento da fase C)."""
    i = next((k for k, e in enumerate(trilha.eventos) if MARCA_DA_CORRECAO in (e.get("trilha") or "")), None)
    return 0 if i is None else trilha.descartar_desde(i)


def _lado_da_correcao(d: dict) -> dict:
    """O que biblioteca_fase4.evidencia_de_correcao precisa de uma corrida do cenário: passou, corpo, tempo, árvore podada,
    a conferência que falhou e o veredito da regra R1."""
    chamada = d.get("chamada") or {}
    podada = d.get("podada") or {}
    return {"passou": bool(d["r"]["passou"]), "corpo": d.get("corpo"), "tempo_ms": chamada.get("tempo_ms"), "arvore": podada.get("texto") or "",
            "conferencia_falha": d["r"].get("conferencia_falha"), "reproduz": bool((d.get("veredito") or {}).get("reproduz")), "status": d.get("status")}


def rodar_biblioteca(args: argparse.Namespace) -> int:
    """Corrida 20 (plano, P5, noite C): as quatro fases descritas no cabeçalho do arquivo, retomáveis (cada fase sabe o que já
    foi gravado); a biblioteca de produção não muda."""
    import _env_common as env
    import biblioteca_fase4 as bf
    import diagnostico_ao_vivo as dv
    import gerar_relatorio_raciocinio as grr
    import restaurar_banco as rb
    import run
    import shutil
    import sonda_correcao

    saida = caminhos.fase3(args.saida)["raiz"]
    saida.mkdir(parents=True, exist_ok=True)
    marco = _marcador(saida / "fase4.log")
    inicio = cen.agora()
    t0 = time.monotonic()
    modelo = args.modelo
    slug = executar_fase3._slug(modelo)
    parcial = bool(args.casos)
    versao = executar_fase3._versao_ollama()
    if versao is None:
        marco("!! o Ollama não respondeu em /api/version; suba o servidor antes da corrida")
        return 2
    limiares = dv.carregar_limiares(Path(args.limiares) if args.limiares else None)
    if limiares is None:
        if not parcial:
            marco("!! sem limiares.json (regra R7): rode --modo calibracao antes")
            return 2
        marco("aviso: sem limiares.json; a corrida parcial segue sem selo")
    pontes = carregar_pontes(gravar=not parcial)
    if versao_precisa_de_ponte(versao, pontes):
        if not parcial:
            marco(f"!! a versão {versao} do Ollama não tem ponte completa registrada (regra R6): rode --modo calibracao antes")
            return 2
        marco(f"aviso: a versão {versao} do Ollama não tem ponte completa registrada; a corrida parcial segue")
    k = ler_ks(args.k)[0] if args.k else int((limiares or {}).get("k") or 3)
    versoes = _ambiente().get("versoes", {})
    contrato = _contrato_do_produto()
    if not evo.snapshot_fechado(dv.PASTA_CURADA):
        marco(f"!! a cópia curada em {dv.PASTA_CURADA} não existe ou não está fechada (sem fechamento.json)")
        return 2
    particao = e3b._particao_oficial(e3b._oficial())
    aprendizado = [c for c in e3b.TODOS_OS_CASOS if evo.particao_de(particao, c["id"]) == "aprendizado"]
    ineditos = e3b._casos_ineditos()
    por_id_ined = {c["id"]: c for c in ineditos}
    verbetes_curada = bib.carregar(dv.PASTA_CURADA)
    com_tela = {i["id"]: i for i in selecionar_casos(aprendizado)["reproduziveis"]}
    ligados = casos_ligados_com_tela(verbetes_curada)
    if args.casos:
        aprendizado, ineditos, ligados = aprendizado[:args.casos], ineditos[:args.casos], ligados[:args.casos]
    conjunto = conjunto_de_correcao([c["id"] for c in ligados])
    casos_sonda = sorted(set(CASOS_DE_TEXTO_ALTERADO) | set(conjunto["desligados"]))
    if args.casos:
        casos_sonda = casos_sonda[:args.casos]
    ids_ineditos = {c["id"] for c in ineditos}
    # a biblioteca de leitura (epoca-100 = L1 curada) e as parcelas da calibração para a regra dos 40%
    pasta_bib = saida / "bibliotecas" / slug
    leitura = pasta_bib / f"epoca-{dv.VERSAO_CURADA}"
    hash_curada = e3b._preparar_copia(dv.PASTA_CURADA, leitura)
    verbetes = bib.carregar(leitura)
    indice = rec.Indice(verbetes)
    exemplo = fixture_sem_gabarito(aprendizado[0])
    ctx0, prompt0 = dv.montar_prompt(verbetes, indice, exemplo, k)
    hash_fixo = dv.hash_prompt_fixo(verbetes, ctx0, exemplo, prompt0)
    arq_cal = caminhos.RESULTADOS / "fase4_calibracao" / f"k{k}" / slug / f"diagnosticos__L{dv.VERSAO_CURADA}.jsonl"
    regs_cal = executar_bateria.ler_jsonl(arq_cal)
    if not regs_cal:
        if not parcial:
            marco(f"!! sem os registros da calibração em {arq_cal} (regra dos 40% e ficha 32)")
            return 2
        marco(f"aviso: sem os registros da calibração em {arq_cal}; a corrida parcial segue sem a regra dos 40%")
    parcelas = bf.parcela_nos_contextos(regs_cal)
    aprendidos = [v["id"] for v in verbetes if v["pasta"] == evo.PASTA_APRENDIDOS]
    recuperacao_cal = bf.recuperacao_dos_aprendidos(regs_cal, aprendidos)
    # a base da regra R5 nos inéditos
    base_regs: list[dict] | None = None
    if args.base_ineditos == "corrida12":
        arq_base = caminhos.RESULTADOS / CORRIDA12 / slug / f"diagnosticos__L{dv.VERSAO_CURADA}.jsonl"
        base_regs = [r for r in executar_bateria.ler_jsonl(arq_base) if r.get("caso") in ids_ineditos and r.get("biblioteca_versao") == hash_curada]
        versoes_base = sorted({r.get("versao_ollama") for r in base_regs}, key=str)
        origem_da_base = f"{CORRIDA12} (corrida 12, cópia curada {hash_curada}, Ollama {', '.join(map(str, versoes_base)) or 'n/d'})"
        if len(base_regs) < len(ineditos):
            marco(f"!! a base da regra R5 em {arq_base} cobre {len(base_regs)} dos {len(ineditos)} inéditos; use --base-ineditos propria")
            return 2
    else:
        origem_da_base = "os 36 inéditos diagnosticados com a cópia curada na mesma sessão (--base-ineditos propria)"
    pasta_reg = saida / slug
    pasta_reg.mkdir(parents=True, exist_ok=True)
    arq_diag, lat_diag = pasta_reg / f"diagnosticos__L{dv.VERSAO_CURADA}.jsonl", pasta_reg / f"logprobs__L{dv.VERSAO_CURADA}.jsonl"
    arq_prop = pasta_reg / f"propostas__E{EPOCA_DO_LOTE}.jsonl"
    arq_reav, lat_reav = pasta_reg / f"reavaliacao__E{EPOCA_DO_LOTE}.jsonl", pasta_reg / "logprobs__reavaliacao.jsonl"
    arq_base_propria, lat_base = pasta_reg / f"reavaliacao__L{dv.VERSAO_CURADA}.jsonl", pasta_reg / "logprobs__base.jsonl"
    arq_resumo, arq_corr, arq_trilha = saida / "biblioteca.jsonl", saida / "correcoes.jsonl", saida / "trilha_biblioteca.jsonl"
    arq_lote, arq_sonda = saida / "lote.json", saida / "sonda.json"
    feitos = {r["caso"] for r in executar_bateria.ler_jsonl(arq_resumo)}
    try:
        _conferir_versao_das_linhas([arq_diag, arq_prop, arq_reav, arq_base_propria], versao)
    except SystemExit as e:
        marco(f"!! {e}")
        return 2
    n_sonda = 2 * len(casos_sonda) if not args.sem_sonda else 0
    previstas = 2 * len(aprendizado) + len(ineditos) * (2 if base_regs is None else 1) + n_sonda
    condicoes = {"modo": "biblioteca", "criado_em": inicio, "saida": args.saida, "modelo": modelo, "versao_ollama": versao, "k": k, "limiares": limiares,
                 "parcial": parcial, "casos": len(aprendizado), "com_tela": sum(1 for c in aprendizado if c["id"] in com_tela), "ineditos": len(ineditos),
                 "base_ineditos": args.base_ineditos, "origem_da_base": origem_da_base, "conjunto_de_correcao": conjunto, "casos_ligados_com_tela": [c["id"] for c in ligados],
                 "casos_da_sonda": casos_sonda, "sem_sonda": args.sem_sonda, "sem_correcao": args.sem_correcao, "inferencias_previstas": previstas,
                 "biblioteca": {"rotulo": dv.ROTULO_CURADA, "versao": dv.VERSAO_CURADA, "hash": hash_curada, "origem": "Programacao/AgenteCore/biblioteca_producao"},
                 "epocas": {"lote": EPOCA_DO_LOTE, "correcoes": EPOCA_DAS_CORRECOES, "sonda": EPOCA_DAS_CORRECOES + 1},
                 "hash_prompt_fixo": hash_fixo, "hash_indice": dv.hash_indice(indice), "teto_proposta": args.teto_proposta, "top_logprobs": args.top, "teto_tokens": args.teto,
                 "filtros": list(bf.FILTROS), "pesos": bf.PESO_POR_TIPO, "orcamento_de_peso_por_verbete": bf.ORCAMENTO_DE_PESO_POR_VERBETE, "limiar_redundancia": bf.LIMIAR_REDUNDANCIA,
                 "parcela_para_revisao": bf.PARCELA_PARA_REVISAO, "parcelas_para_revisao": {v: round(parcelas[v], 4) for v in bf.verbetes_para_revisao(parcelas)},
                 "calibracao": str(arq_cal.relative_to(caminhos.RESULTADOS)) if regs_cal else None, "recuperacao_dos_aprendidos": recuperacao_cal,
                 "aprendidos_sem_recuperacao": bf.aprendidos_sem_recuperacao(recuperacao_cal), "regra_r4": bf.REGRA_R4, "regra_r5": bf.REGRA_R5,
                 "versoes": versoes, "canal": args.canal, "hosts_permitidos": list(ic.HOSTS_PERMITIDOS), "hosts_har": list(ic.CDN_PADRAO),
                 "hosts_silenciosos": list(ic.HOSTS_SILENCIOSOS), "limites": tr.LIMITES_PADRAO, "orcamento_de_tempo_ms": ORCAMENTO_DE_TEMPO_MS, "contrato": contrato}
    (saida / "condicoes_fase4.json").write_text(json.dumps(condicoes, ensure_ascii=False, indent=2), encoding="utf-8")
    marco(f"INÍCIO biblioteca: Ollama {versao}, {modelo}, {dv.ROTULO_CURADA} ({hash_curada}), k = {k}; {len(aprendizado)} casos de aprendizado "
          f"({condicoes['com_tela']} com tela), {len(ineditos)} inéditos (base {args.base_ineditos}), correção em {len(ligados)} casos "
          f"({len(conjunto['desligados'])} desligados), sonda em {len(casos_sonda)}; {previstas} inferências previstas{'; corrida PARCIAL' if parcial else ''}; "
          f"{len(feitos)} caso(s) já feito(s)")

    front, api = run.start_services()
    trilha: tr.Trilha | None = None
    estado: dict = {"lote": None, "correcao": None, "sonda": None, "aceitas": 0}
    try:
        if not run.wait_until_ready(timeout_s=90):
            marco("!! as cobaias não responderam nas portas 8080 e 8000")
            return 2
        cli = env.find_mysql_cli()
        if rb.restaurar(cli) != rb.CONTAGENS_DO_SEED:
            marco("!! o banco restaurado não tem as contagens do seed")
            return 2
        digest, versao_ollama = e3b._preparar_modelo(modelo)
        if versao_ollama != versao:
            marco(f"!! a versão do Ollama mudou antes de começar: {versao} para {versao_ollama}")
            return 2
        comum = {"digest": digest, "versao_ollama": versao_ollama, "maquina": platform.node(), "epoca": EPOCA_DO_LOTE, "biblioteca_epoca": dv.VERSAO_CURADA,
                 "biblioteca_versao": hash_curada, "particao": particao, "k": k, "teto_tokens": args.teto}
        with navegador.Navegador(canal=args.canal) as nav:
            v = nav.versao()
            if arq_trilha.exists() and feitos:
                trilha = tr.Trilha.carregar(arq_trilha)
                trilha.pasta_blobs = saida / "blobs"
                marco(f"retomando a trilha de {arq_trilha.name}: {len(trilha.eventos)} eventos")
            else:
                trilha = tr.Trilha(versao=tr.V2, pasta_blobs=saida / "blobs")
                trilha.corrida(tr.cabecalho_de_corrida(modelo=modelo, versao_ollama=versao, inicio=inicio, quantizacao=dv.quantizacao_do_modelo(modelo),
                                                       top_logprobs=args.top, leitura_da_probabilidade=dv.LEITURA_DA_PROBABILIDADE,
                                                       hash_biblioteca=hash_curada, hash_prompt_fixo=hash_fixo, hash_indice=dv.hash_indice(indice),
                                                       playwright=v["playwright"], navegador=v["navegador"], canal=args.canal, corrida=args.saida,
                                                       etapas_registradas=["roteiro", "interceptacao", "poda", "caso_ao_vivo", "recuperacao", "prompt",
                                                                           "diagnostico", "edicao_biblioteca", "correcao"],
                                                       etapas_nao_registradas=["cura", "intervencao"],
                                                       extras={"modo": "biblioteca", "k": k, "limiares": limiares, "base_ineditos": args.base_ineditos}), ts=inicio)
            tela = Tela(nav, trilha, args.saida, contrato, args.token, marco, prefixo=f"{args.saida}/{slug}")

            def _loop() -> None:
                # ---- fase A: diagnóstico e proposta nos casos de aprendizado
                registros_prop = executar_bateria.ler_jsonl(arq_prop)
                raiz_escrita = evo.abrir_epoca(pasta_bib, EPOCA_DO_LOTE, registros_prop)
                ordem = sum(r.get("n_aceitas", 0) for r in registros_prop)
                pesos_usados: dict = {}
                for r in registros_prop:
                    for d_ in r.get("decisoes") or []:
                        if d_.get("aceita") and d_.get("verbete"):
                            pesos_usados[d_["verbete"]] = pesos_usados.get(d_["verbete"], 0) + (d_.get("peso") or 0)
                novos = sum(1 for r in registros_prop for d_ in r.get("decisoes") or [] if d_.get("aceita") and (d_.get("edicao") or {}).get("operacao") == "novo_verbete")
                ctx_validacao = {"raiz": raiz_escrita, "verbetes": bib.carregar(raiz_escrita), "casos": e3b.TODOS_OS_CASOS, "ids_visiveis": set(), "epoca": EPOCA_DO_LOTE,
                                 "caso_id": None, "modelo": modelo, "novos_nesta_epoca": novos, "aceitas_no_caso": 0, "k": k}
                filtros_ctx = {"parcelas": parcelas, "corpo_http": None, "corrigidos": {}, "pesos_usados": pesos_usados, "casos_da_rodada": {c["id"] for c in aprendizado},
                               "fontes": bf.fontes_das_cobaias(), "rotas": bf.rotas_do_openapi(), "data": inicio[:10]}
                pendentes = [c for c in aprendizado if c["id"] not in feitos]
                if pendentes:
                    for cid in ("api-catalogo", "api-detalhe"):
                        tela.referencia(cid, 1 if cid == "api-detalhe" else None)
                for n, caso in enumerate(aprendizado, 1):
                    if caso["id"] in feitos:
                        continue
                    item = com_tela.get(caso["id"])
                    d = tela.rodar_caso(item) if item is not None else None
                    origem = "tela" if d is not None and d["veredito"]["reproduz"] else "fixture"
                    tid = f"{args.saida}/{slug}/{caso['id']}@{origem}"
                    extras = bf.verbetes_do_caso(verbetes, caso["id"])
                    evidencia: list[dict] = []
                    if origem == "tela":
                        seqs = tela.emitir(tid, d)
                        for chave, papel in (("poda_corpo", "sinal_em_codigo"), ("poda_arvore", "arvore_podada"), ("chamada", "corpo_http")):
                            if seqs.get(chave):
                                evidencia.append({"seq": seqs[chave], "papel": papel})
                        caso_diag = d["caso_vivo"]
                        corpo_http = d.get("corpo")
                    else:
                        caso_diag = fixture_sem_gabarito(caso)
                        trilha.evento("entrada", tid, {"caso": caso["id"], "classe": caso["classe"], "nivel": caso["nivel"], "origem": "fixture",
                                                       "texto": trilha.blob(estrategias._dados_do_caso(caso_diag), "caso")}, "ao_vivo", ts=cen.agora())
                        if d is not None:
                            trilha.evento("incidente", tid, {"tipo": "tela_nao_reproduz", "detalhe": d["veredito"]["motivo"]}, "ao_vivo", ts=cen.agora())
                        corpo_http = str(caso["entrada"].get("corpo") or "") or None
                    sv = dv.diagnosticar(trilha, tid, caso_diag, verbetes, indice, k=k, modelo=modelo, comum=comum, limiares=limiares, intervencoes="desligadas",
                                         top=args.top, teto=args.teto, evidencia=evidencia, ts=cen.agora(), extras=extras)
                    executar_fase3._gravar(arq_diag, sv["registro"])
                    executar_fase3._gravar(lat_diag, sv["lateral"])
                    _conferir_versao(versao)
                    ctx = sv["ctx"]
                    prompt_diag = estrategias.linear_com_biblioteca(caso_diag, ctx["texto"])
                    caso_prop = {**caso_diag, "id": caso["id"], "gabarito": caso["gabarito"]}
                    ouro = rec.verbete_ouro(verbetes, caso)
                    ctx_validacao.update({"caso_id": caso["id"], "aceitas_no_caso": 0, "ids_visiveis": set(ctx["verbetes_ids"]) | {ouro["id"]}})
                    filtros_ctx["corpo_http"] = corpo_http
                    rp = bf.propor_p5(modelo, caso_prop, sv["registro"], ctx, prompt_diag, verbetes, args.teto_proposta, comum, ctx_validacao, pasta_bib, ordem, filtros_ctx,
                                      trilha=trilha, tid=tid, evidencia=evidencia + [{"seq": sv["seq_inferencia"], "papel": "resposta"}], ts=cen.agora())
                    ordem += rp["n_aceitas"]
                    executar_fase3._gravar(arq_prop, {kk: vv for kk, vv in rp.items() if kk not in ("no", "seq_inferencia", "seq_decisao")})
                    _conferir_versao(versao)
                    acertou = _acertou({**sv["registro"], "gabarito": caso["gabarito"]})
                    resumo = registro_da_biblioteca({"caso": caso["id"], "classe": caso["classe"], "nivel": caso["nivel"], "origem": origem,
                                                     "reproduz": d["veredito"]["reproduz"] if d else None, "modo": item["modo"] if item else None,
                                                     "campo": item["campo"] if item else None, "cenario": item["cenario"] if item else None, "diagnostico": sv,
                                                     "acertou": acertou, "proposta": rp, "segundos_cenario": d["r"]["segundos"] if d else None})
                    trilha.gravar(arq_trilha)
                    executar_fase3._gravar(arq_resumo, resumo)
                    feitos.add(caso["id"])
                    pr = "n/d" if resumo["p_rotulo"] is None else f"{resumo['p_rotulo']:.2f}"
                    marco(f"[A {n}/{len(aprendizado)}] {caso['id']} ({origem}): {resumo['rotulo']} (p {pr}, {'acertou' if acertou else 'errou'}) | "
                          f"proposta: {rp['n_aceitas']}/{rp['n_propostas']} no lote, {len(rp['para_revisao'])} para revisão, "
                          f"{', '.join(rp['motivos_rejeicao']) or ('NENHUMA' if rp['abstencao'] else 'sem recusa')} | por id: {', '.join(rp['recuperacao_por_id']) or 'nenhum'} | "
                          f"{sv['registro']['segundos']} + {rp['segundos']} s")
                registros_prop = executar_bateria.ler_jsonl(arq_prop)
                estado["aceitas"] = sum(r.get("n_aceitas", 0) for r in registros_prop)
                if not evo.snapshot_fechado(raiz_escrita):
                    fechamento = evo.fechar_epoca(pasta_bib, EPOCA_DO_LOTE, modelo, e3b.TODOS_OS_CASOS, estado["aceitas"], versao_ollama=versao_ollama)
                    marco(f"epoca-{EPOCA_DO_LOTE} (o lote) fechada: hash {fechamento['hash']}, {fechamento['n_notas']} notas, {fechamento['n_retificacoes']} retificações, "
                          f"{fechamento['n_verbetes_novos']} verbetes novos, {fechamento['aceitas_na_epoca']} edições aceitas")
                fechamento = json.loads((raiz_escrita / "fechamento.json").read_text(encoding="utf-8"))
                # ---- fase B: a regra R5 nos inéditos
                verbetes_lote = bib.carregar(raiz_escrita)
                indice_lote = rec.Indice(verbetes_lote)
                comum_lote = {**comum, "epoca": EPOCA_DO_LOTE + 1, "biblioteca_epoca": EPOCA_DO_LOTE, "biblioteca_versao": fechamento["hash"]}

                def _diagnosticar_ineditos(arq: Path, lat: Path, verbs: list[dict], ind: rec.Indice, com: dict, rotulo: str) -> list[dict]:
                    prontos = {r["caso"] for r in executar_bateria.ler_jsonl(arq)}
                    for n, caso in enumerate(ineditos, 1):
                        if caso["id"] in prontos:
                            continue
                        caso_f = fixture_sem_gabarito(caso)
                        tid = f"{args.saida}/{slug}/{caso['id']}@{rotulo}"
                        trilha.evento("entrada", tid, {"caso": caso["id"], "classe": caso["classe"], "nivel": caso["nivel"], "origem": "fixture", "etapa": rotulo,
                                                       "texto": trilha.blob(estrategias._dados_do_caso(caso_f), "caso")}, "ao_vivo", ts=cen.agora())
                        s = dv.diagnosticar(trilha, tid, caso_f, verbs, ind, k=k, modelo=modelo, comum=com, limiares=limiares, intervencoes="desligadas",
                                            top=args.top, teto=args.teto, ts=cen.agora())
                        executar_fase3._gravar(arq, s["registro"])
                        executar_fase3._gravar(lat, s["lateral"])
                        trilha.gravar(arq_trilha)
                        _conferir_versao(versao)
                        marco(f"[B {rotulo} {n}/{len(ineditos)}] {caso['id']}: {s['no']['escolha']} ({s['registro']['segundos']} s)")
                    return [{**r, "gabarito": por_id_ined[r["caso"]]["gabarito"]} for r in executar_bateria.ler_jsonl(arq) if r["caso"] in por_id_ined]

                novos_regs = _diagnosticar_ineditos(arq_reav, lat_reav, verbetes_lote, indice_lote, comum_lote, "lote")
                base = ([{**r, "gabarito": por_id_ined[r["caso"]]["gabarito"]} for r in base_regs] if base_regs is not None
                        else _diagnosticar_ineditos(arq_base_propria, lat_base, verbetes, indice, comum, "base"))
                r5 = bf.avaliar_lote(base, novos_regs)
                edicoes = [{**d_["edicao"], "peso": d_.get("peso"), "granularidade": d_.get("granularidade"), "proveniencia": d_.get("proveniencia")}
                           for r in registros_prop for d_ in r.get("decisoes") or [] if d_.get("aceita") and d_.get("edicao")]
                para_revisao = [{**d_["edicao"], "peso": d_.get("peso"), "granularidade": d_.get("granularidade"), "proveniencia": d_.get("proveniencia"), "para_revisao": True}
                                for r in registros_prop for d_ in r.get("decisoes") or [] if d_.get("motivo") == bf.CODIGO_DE_REVISAO and d_.get("edicao")]
                conflitos = bf.resolver_conflito([{**e, "ordem": i + 1, "data": inicio[:10], "evidencia": e.get("operacao")} for i, e in enumerate(edicoes)])
                lote = {"edicoes": edicoes, "para_revisao": para_revisao, "parcelas": {v: round(parcelas[v], 4) for v in bf.verbetes_para_revisao(parcelas)},
                        "fechamento": fechamento, "r5": r5, "origem_da_base": origem_da_base, "versao_ollama": versao, "metricas": bf.metricas_da_rodada(registros_prop),
                        "conflitos": [c for c in conflitos if not c.get("prevalece")], "auditoria": bf.auditoria(verbetes_lote, {}, [{"verbete": e["verbete"], "caso": e["caso"]} for e in edicoes]),
                        "amostra_para_revisao": [{"verbete": e["verbete"], "operacao": e["operacao"], "caso": e["caso"]} for e in bf.amostra_para_revisao(edicoes + para_revisao, parcelas)]}
                arq_lote.write_text(json.dumps(lote, ensure_ascii=False, indent=2), encoding="utf-8")
                # ! Alteração de IA - Revisar: (04/11/2026) a planilha passa por bf.gravar_planilha_de_revisao, que não apaga
                # uma revisão já feita à mão.
                # ! Motivo: esta linha roda a cada partida, inclusive na retomada; ver gravar_planilha_de_revisao.
                if bf.gravar_planilha_de_revisao(saida / "revisao_do_lote.md", bf.planilha_de_revisao(edicoes + para_revisao, parcelas, args.saida)) == "mantida":
                    marco("!! revisao_do_lote.md tem mudança feita à mão e foi mantida; a versão gerada agora está em revisao_do_lote.nova.md")
                estado["lote"] = r5
                marco(f"regra R5: {r5['motivo']} (p = {r5['p_mcnemar']}); lote com {len(edicoes)} edição(ões), {len(para_revisao)} para revisão humana")
                # ---- fase C: o ciclo de correção, sem modelo
                raiz_corr = pasta_bib / f"epoca-{EPOCA_DAS_CORRECOES}"
                if not args.sem_correcao and ligados:
                    if evo.snapshot_fechado(raiz_corr) and arq_corr.exists():
                        marco(f"ciclo de correção já feito (epoca-{EPOCA_DAS_CORRECOES} fechada); pulando")
                    else:
                        # ! Alteração de IA - Revisar: (04/11/2026) refazer a fase C também tira da trilha os eventos da
                        # tentativa anterior (descartar_eventos_da_correcao) e descarta a sonda já começada (pasta sonda/ e
                        # sonda.json), que leu a época 102 que vai ser refeita.
                        # ! Motivo: sem o corte, os casos da fase C apareceriam duas vezes na trilha; a sonda é a fase D,
                        # feita sobre a época 102, e reaproveitar os registros dela misturaria leituras da época antiga com
                        # a nova (a retomada da época congelada da Fase 3 pula os casos que já estão no JSONL).
                        n_desc = descartar_eventos_da_correcao(trilha)
                        if n_desc:
                            trilha.gravar(arq_trilha)
                            marco(f"fase C refeita: {n_desc} evento(s) da tentativa anterior saíram da trilha")
                        if (saida / "sonda").exists() or arq_sonda.exists():
                            if (saida / "sonda").exists():
                                shutil.rmtree(saida / "sonda")
                            if arq_sonda.exists():
                                arq_sonda.unlink()
                            marco("sonda descartada: ela lê a época 102, que vai ser refeita")
                        if raiz_corr.exists():
                            shutil.rmtree(raiz_corr)
                        if arq_corr.exists():
                            arq_corr.unlink()
                        evo.copiar_biblioteca(raiz_escrita, raiz_corr)
                        evo._limpar_gerados(raiz_corr)
                        corrigidos: dict[str, list[str]] = {}
                        desligados = set(conjunto["desligados"])
                        for n, item in enumerate(ligados, 1):
                            t_c = time.monotonic()
                            desligado = item["id"] in desligados
                            tid = f"{args.saida}/{slug}/{item['id']}@correcao"
                            d_antes = tela.rodar_caso(item)
                            seqs_a = tela.emitir(tid + "/antes", d_antes)
                            d_depois = tela.rodar_caso({**item, "modo": "normal", "campo": None} if desligado else item)
                            seqs_d = tela.emitir(tid + "/depois", d_depois)
                            antes, depois = _lado_da_correcao(d_antes), _lado_da_correcao(d_depois)
                            forma = d_antes["cenario"]["forma"] if d_antes.get("do_alvo") else "lista"
                            ev = bf.evidencia_de_correcao(antes, depois, contrato, forma_esperada=forma, orcamento_ms=ORCAMENTO_DE_TEMPO_MS)
                            det = bf.detectar_correcao(ev)
                            estados: dict = {}
                            if det["corrigido"]:
                                for vid in item["verbetes"]:
                                    v_atual = next(x for x in evo._carregar_verbetes(raiz_corr) if x["id"] == vid)
                                    estado_antes = bf.estado_do_verbete(v_atual)
                                    bf.corrigir(raiz_corr, vid, item["id"], bf.sugestao_do_modelo(v_atual, item["id"]),
                                                bf.solucao_aplicada_por_molde(item["id"], item["cenario"], item["modo"], ev, inicio[:10]), inicio[:10])
                                    estados[vid] = (estado_antes, "corrigido")
                                    corrigidos.setdefault(vid, []).append(item["id"])
                            seqs = [{"seq": s, "papel": papel} for s, papel in ((seqs_a.get("poda_corpo"), "sinal_em_codigo"), (seqs_a.get("poda_arvore"), "arvore_podada"),
                                                                              (seqs_d.get("poda_corpo"), "sinal_em_codigo"), (seqs_d.get("poda_arvore"), "arvore_podada")) if s]
                            for vid in item["verbetes"]:
                                trilha.evento("edicao_biblioteca", tid, {"etapa": "correcao", "caso": item["id"], "verbete": vid, "origem": "harness", "modo_depois": "normal" if desligado else item["modo"],
                                                                         "estado_antes": estados.get(vid, (bf.estado_do_verbete(next(x for x in evo._carregar_verbetes(raiz_corr) if x["id"] == vid)),))[0],
                                                                         "estado_depois": "corrigido" if vid in estados else "sem mudança",
                                                                         "evidencia": {kk: ev[kk] for kk in ("passou_depois", "ha_diff_http", "ha_diff_arvore", "sintoma_sumiu")},
                                                                         "marcado": det["corrigido"], "motivo": det["motivo"]}, "ao_vivo", ts=cen.agora())
                            trilha.decisao(tid, bf.no_de_correcao(item["id"], item["verbetes"], det, ev, seqs, {kk: list(vv) for kk, vv in estados.items()}), ts=cen.agora())
                            c = {"caso": item["id"], "cenario": item["cenario"], "modo": item["modo"], "campo": item["campo"], "verbetes": item["verbetes"], "desligado": desligado,
                                 "antes": antes, "depois": depois, "evidencia": ev, "deteccao": det, "estados": estados, "segundos": round(time.monotonic() - t_c, 2)}
                            executar_fase3._gravar(arq_corr, registro_da_correcao(c))
                            trilha.gravar(arq_trilha)
                            marco(f"[C {n}/{len(ligados)}] {item['id']} ({item['modo']}, {'desligado' if desligado else 'mantido'}): antes {'falhou' if not antes['passou'] else 'passou'}"
                                  f"{' e reproduz' if antes['reproduz'] else ''}, depois {'passou' if depois['passou'] else 'falhou'}; fio {'mudou' if ev['ha_diff_http'] else 'igual'}, "
                                  f"árvore {'mudou' if ev['ha_diff_arvore'] else 'igual'}; {'CORRIGIDO ' + ', '.join(estados) if det['corrigido'] else 'não marcado'}")
                        fech_corr = bf.fechar_correcoes(pasta_bib, EPOCA_DAS_CORRECOES, modelo, e3b.TODOS_OS_CASOS, corrigidos, versao_ollama=versao_ollama, anterior=EPOCA_DO_LOTE)
                        marco(f"epoca-{EPOCA_DAS_CORRECOES} (correções) fechada: hash {fech_corr['hash']}, {fech_corr['correcoes']} correção(ões) em {len(corrigidos)} verbete(s)")
                    estado["correcao"] = bf.regra_r4(executar_bateria.ler_jsonl(arq_corr))
                    marco(f"regra R4: {estado['correcao']['marcados']} marcada(s), {estado['correcao']['acertos']} certa(s) de {estado['correcao']['desligados']} desligado(s); "
                          f"precisão {estado['correcao']['precisao_pct']}%, revocação {estado['correcao']['revocacao_pct']}%")
                # ---- fase D: a sonda de 28/09 repetida com a recuperação por id
                if not args.sem_sonda and casos_sonda:
                    if arq_sonda.exists():
                        marco("sonda já feita (sonda.json existe); pulando")
                        estado["sonda"] = json.loads(arq_sonda.read_text(encoding="utf-8"))
                    else:
                        origem_sonda = raiz_corr if evo.snapshot_fechado(raiz_corr) else raiz_escrita
                        versao_sonda = EPOCA_DAS_CORRECOES if origem_sonda == raiz_corr else EPOCA_DO_LOTE
                        casos_s = [c for c in e3b.TODOS_OS_CASOS if c["id"] in set(casos_sonda)]
                        pasta_sonda = saida / "sonda"
                        res = sonda_correcao.rodar_sonda(modelo, casos_s, origem_sonda, versao_sonda, pasta_sonda / slug, pasta_sonda / "bibliotecas" / slug, k,
                                                         args.teto, args.teto_proposta, digest, versao_ollama, recuperacao_por_id=True)
                        dado_sonda = {"casos": res["resumo"], "anterior": bf.sonda_anterior(), "origem": origem_sonda.name, "epoca": res["epoca"], "hash_lido": res["hash_lido"],
                                      "recuperacao_por_id": True, "ids": casos_sonda, "k": k}
                        arq_sonda.write_text(json.dumps(dado_sonda, ensure_ascii=False, indent=2), encoding="utf-8")
                        estado["sonda"] = dado_sonda
                        for x in res["resumo"]:
                            marco(f"[D] {x['caso']}: {x['rotulo']} ({'acertou' if x['acertou'] else 'errou'}); {x['n_aceitas']}/{x['n_propostas']} propostas aceitas"
                                  f"{', NENHUMA' if x['abstencao'] else ''}; por id: {', '.join(x['por_id']) or 'nenhum'}; menciona a correção: {'sim' if x['menciona_correcao'] else 'não'}")

            e3b._com_modelo_descarregado(modelo, _loop)
    except SystemExit as e:
        marco(f"!! corrida parou: {e}")
        return 1
    finally:
        derrubar_cobaias(front, api, args.token)
    fim = cen.agora()
    if trilha is not None:
        trilha.fechar(fim)
        trilha.gravar(arq_trilha)
        if not args.sem_relatorios:
            pasta_rel = saida / "relatorios"
            pasta_rel.mkdir(exist_ok=True)
            for tid in tr.por_trilha(trilha.eventos):
                if tid is None or not tid.endswith(("@tela", "@fixture", "@lote", "@base", "@correcao")):
                    continue
                nome = tid.rsplit("/", 1)[-1]
                comando = f"RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo biblioteca --saida {args.saida}_reexec --casos 1 --sem-sonda --sem-correcao"
                (pasta_rel / f"{nome}.md").write_text(grr.relatorio_do_caso_v2(trilha.eventos, tid, comando_reexecucao=comando, pasta_blobs=saida / "blobs"),
                                                      encoding="utf-8", newline="\n")
    tamanho = arq_trilha.stat().st_size if arq_trilha.exists() else 0
    r5 = estado["lote"] or {}
    r4 = estado["correcao"] or {}
    n_sonda_feita = len((estado["sonda"] or {}).get("casos") or [])
    marco(f"FIM biblioteca: {len(feitos)} de {len(aprendizado)} casos de aprendizado; {estado['aceitas']} edição(ões) no lote; R5 {r5.get('veredito', 'não medida')} "
          f"(b = {r5.get('b', 'n/d')}, c = {r5.get('c', 'n/d')}); correção: {r4.get('marcados', 'n/d')} marcada(s) de {r4.get('desligados', 'n/d')} desligado(s); "
          f"sonda em {n_sonda_feita} caso(s); duração {time.monotonic() - t0:.0f} s; trilha {tamanho} bytes")
    return 0


# ------------------------------------------------------------------ a corrida 21: ensaio dos cenários da Fase 5 (pacote P6)

# ! Alteração de IA - Revisar: (04/11/2026, P6) as partes puras do modo `cenarios`: as execuções do ensaio na ordem
# (celulas_do_ensaio), o banco restaurado e conferido contra o seed no começo de cada repetição (preparar_repeticao), a versão
# do navegador igual em todas (conferir_navegador), o caso ao vivo de uma quebra de localizador (caso_do_localizador) e o
# registro de uma execução com o MTTR e o Task Success das fichas 35 e 36 (registro_do_cenario).
# ! Motivo: plano aprovado, seção 5 (P6): os testes escritos antes pedem o cronômetro da detecção à validação, o Task Success
# só com roteiro concluído sem erro (ou causa e campo certos no contrato), o banco conferido por hash e o navegador fixo; com
# as contas fora do laço da corrida, o teste confere cada uma sem navegador nem modelo.
def celulas_do_ensaio(repeticoes: int, casos: int = 0) -> list[dict]:
    """As execuções do ensaio: repetição por repetição, os dez cenários na ordem do catálogo (ou os N primeiros com --casos)."""
    base = list(cen.CENARIOS_DO_ENSAIO)[:casos] if casos else list(cen.CENARIOS_DO_ENSAIO)
    return [{"id": f"{c['id']}#{r}", "cenario": c, "repeticao": r} for r in range(1, max(1, repeticoes) + 1) for c in base]


def preparar_repeticao(n: int, restaurar, hash_atual, hash_do_seed: str) -> str:
    """Restaura o banco antes da repetição n e confere as contagens e o hash das tabelas contra o seed; recusa se não baterem."""
    import restaurar_banco as rb
    contagens = restaurar()
    if contagens != rb.CONTAGENS_DO_SEED:
        raise SystemExit(f"repetição {n}: as contagens do banco restaurado ({contagens}) não são as do seed ({rb.CONTAGENS_DO_SEED})")
    h = hash_atual()
    if h != hash_do_seed:
        raise SystemExit(f"repetição {n}: o banco restaurado tem hash {h} e o do seed é {hash_do_seed}")
    return h


def conferir_navegador(versoes: list) -> str | None:
    """A versão do navegador é a mesma em todas as repetições (plano, P6); devolve a versão, ou None sem nenhuma."""
    unicas = sorted({v for v in versoes if v})
    if len(unicas) > 1:
        raise SystemExit(f"a versão do navegador mudou entre as repetições: {', '.join(unicas)}")
    return unicas[0] if unicas else None


def caso_do_localizador(cenario_: dict, d: dict) -> dict:
    """O caso ao vivo de uma quebra de localizador, nas chaves dos casos gravados: a página, o passo que falhou, o seletor que
    não resolveu e a árvore podada; a página PHP do front legado não tem contrato de API."""
    q, r = d["quebra"], d["r"]
    cf = r.get("conferencia_falha")
    try:
        sintoma = cv.sintoma_por_molde(cf, None, None, status=200)
    except Exception:  # noqa: BLE001 - o molde foi feito para o contrato; sem frase, vale a descrição do passo
        sintoma = ""
    if not str(sintoma or "").strip():
        sintoma = f"o roteiro parou no passo {(r.get('passo_falho') or 0) + 1}: {(cf or {}).get('nome') or r.get('erro') or 'o elemento não foi achado'}"
    podada = d.get("podada") or {}
    observacao = f"roteiro {cenario_['cenario']}; o localizador {q['localizador']} do passo {q['passo_alvo'] + 1} não resolveu"
    if r.get("erro"):
        observacao += f"; {str(r['erro'])[:200]}"
    # ! Alteração de IA - Revisar: (05/11/2026, ficha 42, decisão 90) a árvore encurtada contra a referência da célula e a observação fora da entrada, como no caso da tela.
    # ! Motivo: 9 dos 10 cenários da corrida 21b passaram do limite do prompt; a observação repetia o seletor que a linha SELETOR QUE FALHOU e o SINTOMA já dizem.
    ref = d.get("ref") or {}
    caso = cv.montar_caso(f"{cenario_['id']}@cenario", f"GET {q['pagina']}", 200, "(página PHP do front legado: sem contrato de API)",
                          "(HTML da página; nenhuma chamada à API falhou)", sintoma, arvore=cv.arvore_do_prompt(podada.get("texto") or "", ref.get("arvore"), ref.get("nomes")) or None,
                          seletor_quebrado=q["localizador"])
    caso["observacao_da_poda"] = observacao
    return caso


# ! Alteração de IA - Revisar: (04/11/2026, P6) o registro ganha motivo_deteccao, a ficha da falha (o que a detecção acusou:
# a conferência ou o passo do roteiro que falhou, ou o que o fio mostrou), vazia quando não houve detecção.
# ! Motivo: o protocolo da linha de base manual entrega ao integrante a ficha que a corrida 21 gravou para cada cenário, para ele
# começar da mesma falha que o agente; antes o registro guardava só o instante da detecção, e a ficha teria de ser reescrita à mão.
def registro_do_cenario(cenario_: dict, repeticao: int, navegador_: str | None, hash_inicio: str | None, deteccao: str | None,
                        t_deteccao: float | None, t_diagnostico: float | None, conferencia: dict | None, rotulo: str | None, p_rotulo,
                        cura: dict | None = None, t_validacao: float | None = None, restauracoes: float = 0.0, selo: str | None = None,
                        segundos: float | None = None, segundos_diagnostico: float | None = None, origem_deteccao: str | None = None,
                        motivo_deteccao: str | None = None) -> dict:
    """Uma execução do ensaio. Contrato (ficha 35): o cronômetro para no diagnóstico conferido e o Task Success é causa e campo
    certos. Localizador: o cronômetro para na reexecução validada (descontada a restauração do banco) e o Task Success é a cura
    aplicada com o roteiro concluído sem erro. Sem detecção, nem MTTR nem Task Success nem ficha da falha."""
    detectou = t_deteccao is not None
    if cenario_["tipo"] == "contrato":
        ts = detectou and cen.task_success_contrato(conferencia, cenario_["causa"], cenario_.get("campo"))
        t_fim = t_diagnostico if (conferencia or {}).get("conferido") else None
    else:
        ts = detectou and bool((cura or {}).get("curado"))
        t_fim = t_validacao if (cura or {}).get("curado") else None
    mttr = cen.mttr_monotonico(t_deteccao, t_fim, descontar=restauracoes) if detectou else None
    return {"cenario": cenario_["id"], "tipo": cenario_["tipo"], "roteiro": cenario_["cenario"], "modo": cenario_["modo"], "campo": cenario_.get("campo"),
            "causa_esperada": cenario_["causa"], "classe": cenario_["classe"], "repeticao": repeticao, "navegador": navegador_, "hash_inicio": hash_inicio,
            "detectou": detectou, "origem_deteccao": origem_deteccao if detectou else None, "deteccao": deteccao,
            "motivo_deteccao": motivo_deteccao if detectou else None, "mttr_s": mttr, "task_success": bool(ts),
            "rotulo": rotulo, "p_rotulo": p_rotulo, "selo": selo, "conferido": (conferencia or {}).get("conferido") if conferencia is not None else None,
            "conferencia": conferencia, "cura": cura, "restauracoes_s": round(restauracoes or 0.0, 3), "segundos_diagnostico": segundos_diagnostico,
            "segundos": segundos}


# ! Alteração de IA - Revisar: (04/11/2026, P6) rodar_cenarios: a corrida 21, o ensaio dos dez cenários da ficha 36 com
# `--repeticoes` repetições (o ensaio usa 1); contrato pelo caminho do modo `tela` (Tela.rodar_caso e o diagnóstico ao vivo),
# localizador pelo do modo `cura` (Cura.executar), com o diagnóstico entre a detecção e a cura pelo gancho apos_deteccao.
# ! Motivo: plano aprovado, seção 5 (P6), e fichas 35 e 36 (decisão 79). A detecção do contrato segue a regra R1 do plano (a
# conferência do roteiro que falhou, ou, quando a tela não mostra, o fio diferente do contrato e da referência): o type_drift e
# a escala no preço passam nas conferências da tela e só aparecem no fio. O banco é restaurado e conferido por hash no começo de
# cada repetição e a versão do navegador é conferida em todas. Relançar retoma das execuções que faltam em cenarios.jsonl.
def rodar_cenarios(args: argparse.Namespace) -> int:
    """Corrida 21 (plano, P6; ensaio, dia): os dez cenários da ficha 36 com o agente inteiro (diagnóstico ao vivo nos dez, cura de
    seletor nos quatro de localizador), o MTTR e o Task Success de cada execução em cenarios.jsonl e a trilha v2."""
    import diagnostico_ao_vivo as dv
    import gerar_relatorio_raciocinio as grr

    import _env_common as env
    import restaurar_banco as rb
    import run

    saida = caminhos.fase3(args.saida)["raiz"]
    saida.mkdir(parents=True, exist_ok=True)
    marco = _marcador(saida / "fase4.log")
    inicio = cen.agora()
    t0 = time.monotonic()
    modelo = args.modelo
    slug = executar_fase3._slug(modelo)
    parcial = bool(args.casos)
    versao = executar_fase3._versao_ollama()
    if versao is None:
        marco("!! o Ollama não respondeu em /api/version; suba o servidor antes da corrida")
        return 2
    limiares = dv.carregar_limiares(Path(args.limiares) if args.limiares else None)
    if limiares is None:
        if not parcial:
            marco("!! sem limiares.json (regra R7): rode --modo calibracao antes")
            return 2
        marco("aviso: sem limiares.json; a corrida parcial segue sem selo")
    pontes = carregar_pontes(gravar=not parcial)
    if versao_precisa_de_ponte(versao, pontes):
        if not parcial:
            marco(f"!! a versão {versao} do Ollama não tem ponte completa registrada (regra R6): rode --modo calibracao antes")
            return 2
        marco(f"aviso: a versão {versao} do Ollama não tem ponte completa registrada; a corrida parcial segue")
    k = ler_ks(args.k)[0] if args.k else int((limiares or {}).get("k") or 3)
    versoes = _ambiente().get("versoes", {})
    contrato = _contrato_do_produto()
    celulas = celulas_do_ensaio(args.repeticoes, args.casos)
    if not evo.snapshot_fechado(dv.PASTA_CURADA):
        marco(f"!! a biblioteca de produção em {dv.PASTA_CURADA} não existe ou não está fechada (sem fechamento.json)")
        return 2
    fech_prod = json.loads((dv.PASTA_CURADA / "fechamento.json").read_text(encoding="utf-8"))
    pasta_bib = saida / "bibliotecas" / slug / f"epoca-{dv.VERSAO_CURADA}"
    hash_bib = e3b._preparar_copia(dv.PASTA_CURADA, pasta_bib)
    verbetes = bib.carregar(pasta_bib)
    indice = rec.Indice(verbetes)
    exemplo = fixture_sem_gabarito(casos_de_avaliacao("avaliacao")[0])
    ctx0, prompt0 = dv.montar_prompt(verbetes, indice, exemplo, k)
    hash_fixo = dv.hash_prompt_fixo(verbetes, ctx0, exemplo, prompt0)
    pasta_reg = saida / slug
    pasta_reg.mkdir(parents=True, exist_ok=True)
    arq_diag, arq_lat = pasta_reg / "diagnosticos__cenarios.jsonl", pasta_reg / "logprobs__cenarios.jsonl"
    arq_resumo, arq_trilha = saida / "cenarios.jsonl", saida / "trilha_cenarios.jsonl"
    registros = executar_bateria.ler_jsonl(arq_resumo)
    feitos = {f"{r['cenario']}#{r['repeticao']}" for r in registros}
    try:
        _conferir_versao_das_linhas([arq_diag], versao)
    except SystemExit as e:
        marco(f"!! {e}")
        return 2
    condicoes = {"modo": "cenarios", "criado_em": inicio, "saida": args.saida, "modelo": modelo, "versao_ollama": versao, "k": k, "limiares": limiares,
                 "repeticoes": args.repeticoes, "parcial": parcial, "execucoes": len(celulas), "cenarios": [c["id"] for c in cen.CENARIOS_DO_ENSAIO],
                 "catalogo": [dict(c) for c in cen.CENARIOS_DO_ENSAIO], "troca_da_ficha_36": cen.TROCA_DA_FICHA_36,
                 "biblioteca": {"hash": hash_bib, "origem": "Programacao/AgenteCore/biblioteca_producao", "origem_do_lote": fech_prod.get("origem_do_lote"),
                                "epoca": fech_prod.get("epoca")},
                 "mttr": {"contrato": "da detecção (conferência do roteiro que falhou, ou o fio diferente do contrato e da referência, pela regra R1) "
                                      "ao diagnóstico conferido em código (ficha 35)",
                          "localizador": "da detecção (o passo do localizador falhou) à reexecução validada, com o diagnóstico entre as duas e a "
                                         "restauração do banco descontada"},
                 "task_success": {"contrato": "diagnóstico conferido com a causa e o campo certos (ficha 35)",
                                  "localizador": "cura aplicada e o roteiro concluído sem erro na reexecução"},
                 "top_logprobs": args.top, "teto_tokens": args.teto, "hash_prompt_fixo": hash_fixo, "hash_indice": dv.hash_indice(indice), "versoes": versoes,
                 "canal": args.canal, "contrato": contrato, "limites": tr.LIMITES_PADRAO, "orcamento_de_tempo_ms": ORCAMENTO_DE_TEMPO_MS, "versao_do_caso_ao_vivo": cv.VERSAO_DO_CASO, "sinais_da_referencia_na_busca": cv.SINAIS_DA_REFERENCIA_NA_BUSCA}
    (saida / "condicoes_fase4.json").write_text(json.dumps(condicoes, ensure_ascii=False, indent=2), encoding="utf-8")
    marco(f"INÍCIO cenarios: Ollama {versao}, {modelo}, biblioteca de produção ({hash_bib}"
          f"{', lote ' + str(fech_prod.get('origem_do_lote')) if fech_prod.get('origem_do_lote') else ''}), k = {k}; {len(celulas)} execução(ões) "
          f"({len({c['cenario']['id'] for c in celulas})} cenários x {args.repeticoes} repetição(ões)){'; corrida PARCIAL' if parcial else ''}; {len(feitos)} já feita(s)")
    front, api = run.start_services()
    trilha: tr.Trilha | None = None
    try:
        if not run.wait_until_ready(timeout_s=90):
            marco("!! as cobaias não responderam nas portas 8080 e 8000")
            return 2
        cli = env.find_mysql_cli()
        if rb.restaurar(cli) != rb.CONTAGENS_DO_SEED:
            marco("!! o banco restaurado não tem as contagens do seed")
            return 2
        hash_do_seed = rb.hash_das_tabelas(cli)
        digest, versao_ollama = e3b._preparar_modelo(modelo)
        if versao_ollama != versao:
            marco(f"!! a versão do Ollama mudou antes de começar: {versao} para {versao_ollama}")
            return 2
        comum = {"digest": digest, "versao_ollama": versao_ollama, "maquina": platform.node(), "epoca": dv.VERSAO_CURADA + 1,
                 "biblioteca_epoca": dv.VERSAO_CURADA, "biblioteca_versao": hash_bib, "particao": None, "k": k, "teto_tokens": args.teto}
        with navegador.Navegador(canal=args.canal) as nav:
            v = nav.versao()
            versoes_nav = [r.get("navegador") for r in registros] + [v["navegador"]]
            conferir_navegador(versoes_nav)
            if arq_trilha.exists() and feitos:
                trilha = tr.Trilha.carregar(arq_trilha)
                trilha.pasta_blobs = saida / "blobs"
                marco(f"retomando a trilha de {arq_trilha.name}: {len(trilha.eventos)} eventos")
            else:
                trilha = tr.Trilha(versao=tr.V2, pasta_blobs=saida / "blobs")
                trilha.corrida(tr.cabecalho_de_corrida(modelo=modelo, versao_ollama=versao, inicio=inicio, quantizacao=dv.quantizacao_do_modelo(modelo),
                                                       top_logprobs=args.top, leitura_da_probabilidade=dv.LEITURA_DA_PROBABILIDADE,
                                                       hash_biblioteca=hash_bib, hash_prompt_fixo=hash_fixo, hash_indice=dv.hash_indice(indice),
                                                       playwright=v["playwright"], navegador=v["navegador"], canal=args.canal, corrida=args.saida,
                                                       etapas_registradas=["roteiro", "interceptacao", "poda", "caso_ao_vivo", "recuperacao", "prompt",
                                                                           "diagnostico", "cura"],
                                                       etapas_nao_registradas=["intervencao", "edicao_biblioteca"],
                                                       extras={"modo": "cenarios", "k": k, "limiares": limiares, "repeticoes": args.repeticoes,
                                                               "cenarios": [c["id"] for c in cen.CENARIOS_DO_ENSAIO]}), ts=inicio)
            tela = Tela(nav, trilha, args.saida, contrato, args.token, marco, prefixo=f"{args.saida}/{slug}")
            cura = Cura(nav, trilha, args.saida, args.token, marco, cli)

            def _diagnosticar(tid: str, caso: dict, evidencia: list) -> dict:
                sv = dv.diagnosticar(trilha, tid, caso, verbetes, indice, k=k, modelo=modelo, comum=comum, limiares=limiares,
                                     intervencoes="desligadas", top=args.top, teto=args.teto, evidencia=evidencia, ts=cen.agora())
                executar_fase3._gravar(arq_diag, sv["registro"])
                executar_fase3._gravar(arq_lat, sv["lateral"])
                return sv

            def _loop() -> None:
                if any(c["cenario"]["tipo"] == "contrato" for c in celulas):
                    tela.referencia("api-catalogo", None)
                rep_atual, h_rep = None, None
                for n, cel in enumerate(celulas, 1):
                    if cel["id"] in feitos:
                        marco(f"[{n}/{len(celulas)}] {cel['id']}: já feita, pulando")
                        continue
                    if cel["repeticao"] != rep_atual:
                        rep_atual = cel["repeticao"]
                        h_rep = preparar_repeticao(rep_atual, lambda: rb.restaurar(cli), lambda: rb.hash_das_tabelas(cli), hash_do_seed)
                        conferir_navegador(versoes_nav + [nav.versao()["navegador"]])
                        marco(f"repetição {rep_atual}: banco restaurado e conferido (hash {h_rep}); navegador {v['navegador']}")
                    c = cel["cenario"]
                    tid = f"{args.saida}/{slug}/{cel['id']}"
                    t_cel = time.monotonic()
                    if c["tipo"] == "contrato":
                        item = {**c, "id": cel["id"], "produto_id": None, "requisicao": "GET /api/produtos"}
                        d = tela.rodar_caso(item)
                        t_fio = time.monotonic()
                        seqs = tela.emitir(tid, d)
                        # ! Alteração de IA - Revisar: (04/11/2026, P6) a ficha da falha de cada detecção vai para o registro.
                        # ! Motivo: é o que o integrante da linha de base manual recebe; no fio, o motivo da regra R1.
                        if d["r"].get("t_deteccao") is not None:
                            t_det, origem, deteccao = d["r"]["t_deteccao"], "conferencia_do_roteiro", d["r"]["deteccao"]
                            motivo = cen.motivo_do_roteiro(d["r"])
                        elif d["veredito"]["reproduz"]:
                            t_det, origem, deteccao = t_fio, "contrato_no_fio", cen.agora()
                            motivo = f"o roteiro passou na tela, mas o fio acusou: {d['veredito']['motivo']}"
                        else:
                            t_det, origem, deteccao, motivo = None, None, None, None
                        sv = conf = t_diag = None
                        if t_det is not None:
                            evidencia = [{"seq": s, "papel": p} for s, p in ((seqs.get("poda_corpo"), "sinal_em_codigo"), (seqs.get("poda_arvore"), "arvore_podada"),
                                                                            (seqs.get("chamada"), "corpo_http")) if s]
                            sv = _diagnosticar(tid, d["caso_vivo"], evidencia)
                            t_diag = time.monotonic()
                            conf = cen.diagnostico_conferido(sv["registro"].get("resposta"), d["caso_vivo"])
                        reg = registro_do_cenario(c, cel["repeticao"], v["navegador"], h_rep, deteccao=deteccao, t_deteccao=t_det, t_diagnostico=t_diag,
                                                  conferencia=conf, rotulo=sv["no"]["escolha"] if sv else None,
                                                  p_rotulo=sv["no"]["confianca"]["p_rotulo"] if sv else None, selo=sv["no"]["confianca"]["selo"] if sv else None,
                                                  segundos=round(time.monotonic() - t_cel, 3), segundos_diagnostico=sv["registro"]["segundos"] if sv else None,
                                                  origem_deteccao=origem, motivo_deteccao=motivo)
                    else:
                        guardado: dict = {}

                        # c, tid e guardado entram como valores padrão: a função é da execução desta volta do laço
                        def apos_deteccao(d_: dict, c: dict = c, tid: str = tid, guardado: dict = guardado) -> dict:
                            caso = caso_do_localizador(c, d_)
                            blob = trilha.blob(json.dumps(caso, ensure_ascii=False, sort_keys=True), "caso_ao_vivo")
                            guardado["seqs"] = cura.emitir_quebra(tid, d_, extras={"caso_ao_vivo": blob, "cenario_da_fase_5": c["id"]})
                            sv_ = _diagnosticar(tid, caso, [{"seq": guardado["seqs"]["s_poda"], "papel": "arvore_podada"}])
                            guardado["sv"], guardado["t_diag"] = sv_, time.monotonic()
                            return {"rotulo": sv_["no"]["escolha"], "p_rotulo": sv_["no"]["confianca"]["p_rotulo"]}

                        celula = {"id": cel["id"], "cenario": c["cenario"], "modo": c["modo"], "forma": c["forma"], "repeticao": cel["repeticao"]}
                        d = cura.executar(celula, apos_deteccao=apos_deteccao)
                        cura.emitir_cura(tid, d, guardado["seqs"]) if "seqs" in guardado else cura.emitir(tid, d)
                        sv = guardado.get("sv")
                        e = d.get("escolha") or {}
                        aplicado = (e.get("aplicado") or {}) if isinstance(e.get("aplicado"), dict) else {}
                        reg = registro_do_cenario(c, cel["repeticao"], v["navegador"], h_rep, deteccao=d["r"].get("deteccao"), t_deteccao=d.get("t_deteccao"),
                                                  t_diagnostico=guardado.get("t_diag"), conferencia=None, rotulo=sv["no"]["escolha"] if sv else None,
                                                  p_rotulo=sv["no"]["confianca"]["p_rotulo"] if sv else None, selo=sv["no"]["confianca"]["selo"] if sv else None,
                                                  cura={"curado": bool(e.get("curado")), "estrategia": aplicado.get("estrategia"), "reexecucoes": e.get("reexecucoes"),
                                                        "mesmo_elemento": e.get("mesmo_elemento"), "falha": e.get("falha"),
                                                        "pagina_refeita_s": (d.get("pagina_refeita") or {}).get("segundos")} if d.get("escolha") is not None else {"curado": False},
                                                  t_validacao=d.get("t_validacao"), restauracoes=d.get("segundos_restauracao") or 0.0,
                                                  segundos=round(time.monotonic() - t_cel, 3), segundos_diagnostico=sv["registro"]["segundos"] if sv else None,
                                                  origem_deteccao="passo_do_localizador" if d.get("t_deteccao") is not None else None,
                                                  motivo_deteccao=cen.motivo_do_roteiro(d["r"]) if d.get("t_deteccao") is not None else None)
                    trilha.gravar(arq_trilha)
                    executar_fase3._gravar(arq_resumo, reg)
                    registros.append(reg)
                    _conferir_versao(versao)
                    marco(f"[{n}/{len(celulas)}] {cel['id']} ({c['tipo']}, {c['modo']}): "
                          + (f"detectou ({reg['origem_deteccao']}); {reg['rotulo']}" if reg["detectou"] else "NÃO detectou")
                          + f"; Task Success {'sim' if reg['task_success'] else 'não'}; MTTR {reg['mttr_s']} s; {reg['segundos']} s")

            e3b._com_modelo_descarregado(modelo, _loop)
    except SystemExit as e:
        marco(f"!! corrida parou: {e}")
        return 1
    finally:
        derrubar_cobaias(front, api, args.token)
    fim = cen.agora()
    if trilha is not None:
        trilha.fechar(fim)
        trilha.gravar(arq_trilha)
        if not args.sem_relatorios:
            pasta_rel = saida / "relatorios"
            pasta_rel.mkdir(exist_ok=True)
            for tid in tr.por_trilha(trilha.eventos):
                if tid is None or "#" not in tid.rsplit("/", 1)[-1]:
                    continue
                nome = tid.rsplit("/", 1)[-1].replace("#", "__r")
                comando = f"RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo cenarios --saida {args.saida}_reexec --repeticoes 1"
                (pasta_rel / f"{nome}.md").write_text(grr.relatorio_do_caso_v2(trilha.eventos, tid, comando_reexecucao=comando, pasta_blobs=saida / "blobs"),
                                                      encoding="utf-8", newline="\n")
    sucessos = sum(1 for r in registros if r.get("task_success"))
    tamanho = arq_trilha.stat().st_size if arq_trilha.exists() else 0
    marco(f"FIM cenarios: {len(registros)} de {len(celulas)} execuções; Task Success {sucessos}; duração {time.monotonic() - t0:.0f} s; trilha {tamanho} bytes")
    return 0


# ------------------------------------------------------------------ a corrida 22: avaliação da própria trilha

# ! Alteração de IA - Revisar: (04/11/2026, P7) _roteiro_do_seletor e rodar_avaliacao_trilha: o modo `avaliacao_trilha` (ver o
# cabeçalho do arquivo). Os casos de texto rodam primeiro, sem cobaias; o bloco do seletor sobe o front, a API, o MariaDB e o
# navegador só no fim, e cada roteiro roda duas vezes pelo mesmo caminho da corrida 21 (Cura.executar com o diagnóstico no
# gancho apos_deteccao): a dourada com a quebra do catálogo e a mutada com a quebra composta de avaliacao_trilha.quebra_do_seletor.
# ! Motivo: plano aprovado, seção 5 (P7) e seção 6 (corrida 22); especificação da trilha, seção 12. As cobaias ficam fora dos
# casos de texto para não segurar RAM enquanto o modelo diagnostica 36 casos com nove inferências cada.
def _roteiro_do_seletor(cura: "Cura", trilha: tr.Trilha, c: dict, q: dict, etapa: str, tid: str, diagnosticar) -> tuple[dict, dict | None]:
    """Uma execução de roteiro de localizador do bloco do seletor (a dourada ou a mutada), como na corrida 21: a quebra armada,
    a detecção, o diagnóstico ao vivo entre a detecção e a cura, a cura numa página refeita até o passo que falhou e a reexecução."""
    guardado: dict = {}
    mutacao = None if etapa == "dourada" else {"tipo": "seletor_quebrado", "modo": q["modo"], "extra": q["mutacoes"][-1]}

    def apos_deteccao(d_: dict) -> dict:
        caso = caso_do_localizador(c, d_)
        caso["id"] = f"{c['id']}@{etapa}"
        blob = trilha.blob(json.dumps(caso, ensure_ascii=False, sort_keys=True), "caso_ao_vivo")
        guardado["seqs"] = cura.emitir_quebra(tid, d_, extras={"caso_ao_vivo": blob, "cenario_da_fase_5": c["id"], "etapa": etapa, "mutacao": mutacao})
        sv_ = diagnosticar(tid, caso, [{"seq": guardado["seqs"]["s_poda"], "papel": "arvore_podada"}])
        guardado["sv"] = sv_
        return {"rotulo": sv_["no"]["escolha"], "p_rotulo": sv_["no"]["confianca"]["p_rotulo"]}

    celula = {"id": f"{c['cenario']}@{etapa}", "cenario": c["cenario"], "modo": q["modo"], "forma": "harness", "repeticao": 1}
    d = cura.executar(celula, apos_deteccao=apos_deteccao, quebra=q)
    if "seqs" in guardado:
        cura.emitir_cura(tid, d, guardado["seqs"])
    else:
        cura.emitir(tid, d)
    return d, guardado.get("sv")


def rodar_avaliacao_trilha(args: argparse.Namespace) -> int:
    """Corrida 22 (plano, P7, noite D): os 36 casos de avaliação lidos do fixture (base com as quatro intervenções, sonda de
    pós-racionalização, verbete trocado e contrato alterado) e, no fim, a mutação do seletor nos quatro roteiros de localizador
    com as cobaias e o navegador; relançar retoma dos casos e roteiros que faltam; a trilha é gravada a cada caso."""
    import _env_common as env
    import avaliacao_trilha as at
    import diagnostico_ao_vivo as dv
    import gerar_relatorio_raciocinio as grr
    import restaurar_banco as rb
    import run

    saida = caminhos.fase3(args.saida)["raiz"]
    saida.mkdir(parents=True, exist_ok=True)
    marco = _marcador(saida / "fase4.log")
    inicio = cen.agora()
    t0 = time.monotonic()
    modelo = args.modelo
    slug = executar_fase3._slug(modelo)
    ids_pedidos = ler_ids(args.ids)
    parcial = bool(args.casos) or bool(ids_pedidos) or bool(args.sem_seletor)
    versao = executar_fase3._versao_ollama()
    if versao is None:
        marco("!! o Ollama não respondeu em /api/version; suba o servidor antes da corrida")
        return 2
    limiares = dv.carregar_limiares(Path(args.limiares) if args.limiares else None)
    if limiares is None:
        if not parcial:
            marco("!! sem limiares.json (regra R7): rode --modo calibracao antes")
            return 2
        marco("aviso: sem limiares.json; a corrida parcial segue sem selo e sem gatilho por probabilidade")
    pontes = carregar_pontes(gravar=not parcial)
    if versao_precisa_de_ponte(versao, pontes):
        if not parcial:
            marco(f"!! a versão {versao} do Ollama não tem ponte completa registrada (regra R6): rode --modo calibracao antes")
            return 2
        marco(f"aviso: a versão {versao} do Ollama não tem ponte completa registrada; a corrida parcial segue")
    k = ler_ks(args.k)[0] if args.k else int((limiares or {}).get("k") or 3)
    versoes = _ambiente().get("versoes", {})
    contrato = _contrato_do_produto()
    casos36 = e3b._casos_avaliacao(e3b._particao_oficial(e3b._oficial()))
    amostra = tuple(c["id"] for c in casos36)      # os 36 estão na amostra fixa: as quatro intervenções rodam em todos (plano, P7)
    itens = [c for c in casos36 if not ids_pedidos or c["id"] in set(ids_pedidos)]
    if args.casos:
        itens = itens[:args.casos]
    roteiros = [] if args.sem_seletor else list(at.ROTEIROS_DO_SELETOR)
    if args.casos:
        roteiros = roteiros[:args.casos]
    if not evo.snapshot_fechado(dv.PASTA_CURADA):
        marco(f"!! a biblioteca de produção em {dv.PASTA_CURADA} não existe ou não está fechada (sem fechamento.json)")
        return 2
    fech_prod = json.loads((dv.PASTA_CURADA / "fechamento.json").read_text(encoding="utf-8"))
    pasta_bib = saida / "bibliotecas" / slug / f"epoca-{dv.VERSAO_CURADA}"
    hash_bib = e3b._preparar_copia(dv.PASTA_CURADA, pasta_bib)
    verbetes = bib.carregar(pasta_bib)
    indice = rec.Indice(verbetes)
    exemplo = fixture_sem_gabarito(casos36[0])
    ctx0, prompt0 = dv.montar_prompt(verbetes, indice, exemplo, k)
    hash_fixo = dv.hash_prompt_fixo(verbetes, ctx0, exemplo, prompt0)
    pasta_reg = saida / slug
    pasta_reg.mkdir(parents=True, exist_ok=True)
    etapas = tuple(at.ETAPAS) + ("seletor",)
    arq_diag = {e: pasta_reg / f"diagnosticos__{e}.jsonl" for e in etapas}
    arq_lat = {e: pasta_reg / f"logprobs__{e}.jsonl" for e in etapas}
    arq_resumo, arq_seletor, arq_trilha = saida / "avaliacao.jsonl", saida / "seletor.jsonl", saida / "trilha_avaliacao.jsonl"
    linhas = executar_bateria.ler_jsonl(arq_resumo)
    feitos = {r["caso"] for r in linhas}
    registros_sel = executar_bateria.ler_jsonl(arq_seletor)
    feitos_sel = {r["roteiro"] for r in registros_sel}
    try:
        _conferir_versao_das_linhas(list(arq_diag.values()), versao)
    except SystemExit as e:
        marco(f"!! {e}")
        return 2
    previstas = at.inferencias_previstas(len(itens), len(roteiros))
    condicoes = {"modo": "avaliacao_trilha", "criado_em": inicio, "saida": args.saida, "modelo": modelo, "versao_ollama": versao, "k": k, "limiares": limiares,
                 "intervencoes": "por_gatilho", "amostra": len(amostra), "top_logprobs": args.top, "teto_tokens": args.teto,
                 "leitura_da_probabilidade": dv.LEITURA_DA_PROBABILIDADE, "parcial": parcial, "casos": len(itens), "ids": ids_pedidos,
                 "roteiros_do_seletor": roteiros, "sem_seletor": bool(args.sem_seletor), "etapas": list(at.ETAPAS), "mutacoes": list(at.MUTACOES),
                 "no_previsto": at.NO_PREVISTO, "inferencias_por_caso": at.INFERENCIAS_POR_CASO, "inferencias_previstas": previstas,
                 "biblioteca": {"hash": hash_bib, "origem": "Programacao/AgenteCore/biblioteca_producao", "origem_do_lote": fech_prod.get("origem_do_lote"),
                                "epoca": fech_prod.get("epoca")},
                 "hash_prompt_fixo": hash_fixo, "hash_indice": dv.hash_indice(indice), "versoes": versoes, "canal": args.canal, "contrato": contrato,
                 "hosts_permitidos": list(ic.HOSTS_PERMITIDOS), "hosts_har": list(ic.CDN_PADRAO), "hosts_silenciosos": list(ic.HOSTS_SILENCIOSOS),
                 "limites": tr.LIMITES_PADRAO, "mutacao_do_seletor": at.MUTACAO_DO_SELETOR, "semente_da_amostra": at.SEMENTE_DA_AMOSTRA,
                 "sonda": ("um trecho que afirma a causa respondida pela base, plantado só na memória no Resumo do primeiro verbete entregue que a FONTE "
                           "não citou; pós-racionalização é a FONTE passar a citar o plantado com o rótulo igual"),
                 "regra": ("especificação da trilha, seção 12: TPR x TNR da divergência sinalizada contra os erros reais (acaso 0,25); a trilha aponta o nó "
                           "previsto de cada mutação (verbete trocado: recuperacao; contrato alterado: poda; seletor quebrado: cura); taxa de "
                           "pós-racionalização da FONTE")}
    (saida / "condicoes_fase4.json").write_text(json.dumps(condicoes, ensure_ascii=False, indent=2), encoding="utf-8")
    marco(f"INÍCIO avaliacao_trilha: Ollama {versao}, {modelo}, biblioteca de produção ({hash_bib}"
          f"{', lote ' + str(fech_prod.get('origem_do_lote')) if fech_prod.get('origem_do_lote') else ''}), k = {k}; {len(itens)} caso(s) de texto, "
          f"{len(roteiros)} roteiro(s) do seletor; {previstas} inferências previstas{'; corrida PARCIAL' if parcial else ''}; "
          f"{len(feitos)} caso(s) e {len(feitos_sel)} roteiro(s) já feito(s)")
    trilha: tr.Trilha | None = None
    try:
        digest, versao_ollama = e3b._preparar_modelo(modelo)
        if versao_ollama != versao:
            marco(f"!! a versão do Ollama mudou antes de começar: {versao} para {versao_ollama}")
            return 2
        comum = {"digest": digest, "versao_ollama": versao_ollama, "maquina": platform.node(), "epoca": dv.VERSAO_CURADA + 1,
                 "biblioteca_epoca": dv.VERSAO_CURADA, "biblioteca_versao": hash_bib, "particao": None, "k": k, "teto_tokens": args.teto}
        if arq_trilha.exists() and (feitos or feitos_sel):
            trilha = tr.Trilha.carregar(arq_trilha)
            trilha.pasta_blobs = saida / "blobs"
            marco(f"retomando a trilha de {arq_trilha.name}: {len(trilha.eventos)} eventos")
        else:
            trilha = tr.Trilha(versao=tr.V2, pasta_blobs=saida / "blobs")
            trilha.corrida(tr.cabecalho_de_corrida(modelo=modelo, versao_ollama=versao, inicio=inicio, quantizacao=dv.quantizacao_do_modelo(modelo),
                                                   top_logprobs=args.top, leitura_da_probabilidade=dv.LEITURA_DA_PROBABILIDADE,
                                                   hash_biblioteca=hash_bib, hash_prompt_fixo=hash_fixo, hash_indice=dv.hash_indice(indice),
                                                   playwright=versoes.get("playwright"), navegador=versoes.get("navegador"), canal=args.canal, corrida=args.saida,
                                                   etapas_registradas=["caso", "poda", "recuperacao", "prompt", "diagnostico", "intervencao", "sonda", "mutacao",
                                                                       "roteiro", "quebra", "cura", "reexecucao"],
                                                   etapas_nao_registradas=["interceptacao", "edicao_biblioteca"],
                                                   extras={"modo": "avaliacao_trilha", "k": k, "limiares": limiares, "intervencoes": "por_gatilho", "amostra": len(amostra),
                                                           "etapas": list(at.ETAPAS), "mutacoes": list(at.MUTACOES), "no_previsto": at.NO_PREVISTO}), ts=inicio)

        def _bloco_do_seletor() -> None:
            front, api = run.start_services()
            try:
                if not run.wait_until_ready(timeout_s=90):
                    raise SystemExit("as cobaias não responderam nas portas 8080 e 8000")
                cli = env.find_mysql_cli()
                if rb.restaurar(cli) != rb.CONTAGENS_DO_SEED:
                    raise SystemExit("o banco restaurado não tem as contagens do seed")
                with navegador.Navegador(canal=args.canal) as nav:
                    v = nav.versao()
                    cura = Cura(nav, trilha, args.saida, args.token, marco, cli)

                    def _diagnosticar(tid: str, caso: dict, evidencia: list) -> dict:
                        sv = dv.diagnosticar(trilha, tid, caso, verbetes, indice, k=k, modelo=modelo, comum=comum, limiares=limiares,
                                             intervencoes="desligadas", top=args.top, teto=args.teto, evidencia=evidencia, ts=cen.agora())
                        executar_fase3._gravar(arq_diag["seletor"], sv["registro"])
                        executar_fase3._gravar(arq_lat["seletor"], sv["lateral"])
                        return sv

                    for n, roteiro in enumerate(roteiros, 1):
                        if roteiro in feitos_sel:
                            marco(f"[seletor {n}/{len(roteiros)}] {roteiro}: já feito, pulando")
                            continue
                        c = next(x for x in cen.CENARIOS_DE_LOCALIZADOR if x["cenario"] == roteiro)
                        q_d, q_m = cen.quebra(roteiro, c["modo"]), at.quebra_do_seletor(roteiro)
                        t_rot = time.monotonic()
                        tid_d, tid_m = f"{args.saida}/{slug}/{roteiro}@dourada", f"{args.saida}/{slug}/{roteiro}@seletor_quebrado"
                        d_d, sv_d = _roteiro_do_seletor(cura, trilha, c, q_d, "dourada", tid_d, _diagnosticar)
                        _conferir_versao(versao)
                        d_m, sv_m = _roteiro_do_seletor(cura, trilha, c, q_m, "seletor_quebrado", tid_m, _diagnosticar)
                        _conferir_versao(versao)
                        # o nó `cura` é comparado pela estratégia e pelo seletor aplicado: a mutação troca o nome do alvo por um parecido, e a
                        # cura pode ir à mesma estratégia com outro seletor (produtos, cuja dourada já cura por nome parecido)
                        diff = at.diff_entre_trilhas(trilha.eventos, tid_d, tid_m, cura_pelo_seletor=True)
                        reg = at.registro_do_seletor(roteiro, c, q_d, q_m, at.lado_do_seletor(d_d, sv_d, at.nos_da_trilha(trilha.eventos, tid_d)),
                                                     at.lado_do_seletor(d_m, sv_m, at.nos_da_trilha(trilha.eventos, tid_m)), diff, round(time.monotonic() - t_rot, 2))
                        reg["navegador"] = v["navegador"]
                        trilha.gravar(arq_trilha)
                        executar_fase3._gravar(arq_seletor, reg)
                        registros_sel.append(reg)
                        div = reg["primeiro_no_divergente"]
                        marco(f"[seletor {n}/{len(roteiros)}] {roteiro}: dourada {reg['dourada']['estrategia'] or 'sem cura'} ({reg['dourada']['rotulo']}); "
                              f"mutada {reg['mutada']['estrategia'] or 'sem cura'} ({reg['mutada']['rotulo']}); primeiro nó divergente "
                              f"{div['decisao'] if div else 'nenhum'} (previsto cura: {'sim' if reg['aponta_o_previsto'] else 'NÃO'}); {reg['segundos']} s")
            finally:
                derrubar_cobaias(front, api, args.token)

        def _loop() -> None:
            for n, caso in enumerate(itens, 1):
                if caso["id"] in feitos:
                    marco(f"[{n}/{len(itens)}] {caso['id']}: já feito, pulando")
                    continue
                cf = fixture_sem_gabarito(caso)
                raiz_tid = f"{args.saida}/{slug}/{caso['id']}"
                t_caso = time.monotonic()
                b = at.rodar_base(trilha, f"{raiz_tid}@base", cf, verbetes, indice, k=k, modelo=modelo, comum=comum, limiares=limiares, top=args.top,
                                  teto=args.teto, amostra=amostra, ts=cen.agora())
                executar_fase3._gravar(arq_diag["base"], b["registro"])
                executar_fase3._gravar(arq_lat["base"], b["lateral"])
                _conferir_versao(versao)
                s = at.rodar_sonda(trilha, f"{raiz_tid}@sonda", cf, verbetes, indice, b, k=k, modelo=modelo, comum=comum, limiares=limiares, top=args.top,
                                   teto=args.teto, ts=cen.agora())
                if s["registro"] is not None:
                    executar_fase3._gravar(arq_diag["sonda"], s["registro"])
                    executar_fase3._gravar(arq_lat["sonda"], s["lateral"])
                _conferir_versao(versao)
                ms: dict = {}
                for tipo in ("verbete_trocado", "contrato_alterado"):
                    m = at.rodar_mutacao(trilha, f"{raiz_tid}@{tipo}", tipo, cf, verbetes, indice, b, k=k, modelo=modelo, comum=comum, limiares=limiares,
                                         top=args.top, teto=args.teto, ts=cen.agora())
                    if m["registro"] is not None:
                        executar_fase3._gravar(arq_diag[tipo], m["registro"])
                        executar_fase3._gravar(arq_lat[tipo], m["lateral"])
                    ms[tipo] = m
                    _conferir_versao(versao)
                linha = at.linha_do_caso(b, s, ms, segundos_total=round(time.monotonic() - t_caso, 2))
                trilha.gravar(arq_trilha)
                executar_fase3._gravar(arq_resumo, linha)
                linhas.append(linha)
                ls, lv, lc = linha["sonda"], linha["mutacoes"]["verbete_trocado"], linha["mutacoes"]["contrato_alterado"]

                def no_de(l: dict) -> str:
                    return "n/a" if not l["aplicavel"] else ((l["primeiro_no_divergente"] or {}).get("decisao") or "sem divergência")

                p = "n/d" if linha["p_rotulo"] is None else f"{linha['p_rotulo']:.2f}"
                sonda_txt = ("n/a" if not ls["aplicavel"] else ("cita o plantado" if ls["cita_plantado"] else "não cita") + (", rótulo mudou" if ls["mudou_rotulo"] else ""))
                marco(f"[{n}/{len(itens)}] {caso['id']}: {linha['rotulo']} (p {p}, selo {linha['selo']}); intervenções {len(linha['intervencoes'])} "
                      f"({sum(1 for i in linha['intervencoes'] if i['mudou_rotulo'])} mudaram o rótulo, {sum(1 for i in linha['intervencoes'] if i['limite_inferior'])} com limite inferior); "
                      f"sonda: {sonda_txt}; verbete trocado: {no_de(lv)}; contrato alterado: {no_de(lc)}; {linha['segundos_total']} s")
            if roteiros:
                _bloco_do_seletor()

        e3b._com_modelo_descarregado(modelo, _loop)
    except SystemExit as e:
        marco(f"!! corrida parou: {e}")
        return 1
    fim = cen.agora()
    if trilha is not None:
        trilha.fechar(fim)
        trilha.gravar(arq_trilha)
        if not args.sem_relatorios:
            pasta_rel = saida / "relatorios"
            pasta_rel.mkdir(exist_ok=True)
            prefixo = f"{args.saida}/{slug}/"
            for tid in tr.por_trilha(trilha.eventos):
                if not str(tid).startswith(prefixo):
                    continue
                nome = tid.rsplit("/", 1)[-1]
                caso_id, etapa = nome.split("@", 1) if "@" in nome else (nome, "base")
                if etapa in ("dourada", "seletor_quebrado"):
                    comando = f"RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida {args.saida}_reexec --casos 0"
                else:
                    comando = f"RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida {args.saida}_reexec --ids {caso_id} --sem-seletor"
                (pasta_rel / f"{nome}.md").write_text(grr.relatorio_do_caso_v2(trilha.eventos, tid, comando_reexecucao=comando, pasta_blobs=saida / "blobs"),
                                                      encoding="utf-8", newline="\n")
    tamanho = arq_trilha.stat().st_size if arq_trilha.exists() else 0
    marco(f"FIM avaliacao_trilha: {len(linhas)} de {len(itens)} casos de texto; {len(registros_sel)} de {len(roteiros)} roteiros do seletor; "
          f"duração {time.monotonic() - t0:.0f} s; trilha {tamanho} bytes")
    return 0


def montar_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--modo", choices=MODOS, required=True)
    ap.add_argument("--saida", required=True, help="pasta da corrida em RESULTADOS_DIR (ex.: fase4_reproducao)")
    ap.add_argument("--casos", type=int, default=0, help="limita aos N primeiros casos (0 = todos); corrida parcial não grava derivado oficial")
    ap.add_argument("--canal", choices=navegador.CANAIS, default="chromium")
    ap.add_argument("--token", default=TOKEN_PADRAO, help="X-Admin-Token da CobaiaAPI")
    ap.add_argument("--banco", choices=BANCOS, default="avaliacao",
                    help="quais casos a corrida lê: avaliacao (os 72, padrão), ineditos_fase4 (os 36 da ficha 27) ou todos (108)")
    # ! Alteração de IA - Revisar: opções dos modos com modelo (27/10/2026, P3).
    # ! Motivo: a calibração mede k = 3 e 5 (ficha 30) e a tela lê o k escolhido de limiares.json; as intervenções ficam
    # desligadas na corrida 18 (o custo delas não está na noite B do plano) e ligam por gatilho quando pedido (P7).
    ap.add_argument("--modelo", default=MODELO_PADRAO)
    ap.add_argument("--k", default=None, help=f"calibracao: lista de k separada por vírgula (padrão {K_PADRAO}); tela: um k (padrão: o de limiares.json)")
    ap.add_argument("--top", type=int, default=20, help="alternativas por posição pedidas ao Ollama (top_logprobs)")
    ap.add_argument("--teto", type=int, default=600, help="teto de tokens de saída do diagnóstico")
    ap.add_argument("--intervencoes", choices=("desligadas", "por_gatilho"), default="desligadas",
                    help="tela: rodar as intervenções da especificação (6.1) quando um gatilho dispara")
    ap.add_argument("--amostra", action="store_true", help="tela: os 36 casos oficiais de avaliação disparam o gatilho da amostra fixa")
    ap.add_argument("--limiares", default=None, help="tela: outro limiares.json (padrão: resultados_alvo/fase4/limiares.json)")
    ap.add_argument("--ids", default=None, help="tela: só estes casos, separados por vírgula (reexecução de um caso numa saída própria)")
    ap.add_argument("--sem-relatorios", action="store_true", help="tela e cura: não gravar os relatórios v2 por caso no fim")
    # ! Alteração de IA - Revisar: opções do modo cura (01/11/2026, P4): repetições por célula, formas da quebra e filtros de
    # roteiros e modos para a fumaça e a reexecução de uma célula.
    # ! Motivo: a corrida 19 é 4 roteiros x 4 modos x 5 repetições nas duas formas (plano, seção 6); a fumaça roda uma
    # repetição num roteiro só, e o relatório de cada execução traz o comando que a refaz sozinha.
    ap.add_argument("--repeticoes", type=int, default=REPETICOES_PADRAO, help="cura: repetições por célula (roteiro x modo x forma); "
                    "cenarios: repetições dos dez cenários (o ensaio da corrida 21 usa 1)")
    ap.add_argument("--formas", default="harness,php", help="cura: formas da quebra separadas por vírgula (harness, php)")
    ap.add_argument("--roteiros", default=None, help="cura: só estes roteiros do front legado, separados por vírgula (padrão: os quatro)")
    ap.add_argument("--modos", default=None, help="cura: só estes modos de quebra, separados por vírgula (padrão: os quatro)")
    # ! Alteração de IA - Revisar: (03/11/2026, P5) as opções do modo biblioteca.
    # ! Motivo: a base da regra R5 pode ser a corrida 12 (o plano conta 156 inferências) ou a mesma sessão (36 a mais); a
    # fumaça precisa pular a sonda e o ciclo de correção; o teto da proposta é o da Fase 3.
    ap.add_argument("--base-ineditos", choices=BASES_DOS_INEDITOS, default="corrida12",
                    help="biblioteca: a base da regra R5 nos 36 inéditos (corrida12 = cópia curada da corrida 12; propria = diagnosticar na mesma sessão)")
    ap.add_argument("--sem-sonda", action="store_true", help="biblioteca: não repete a sonda de correção (fumaça)")
    ap.add_argument("--sem-correcao", action="store_true", help="biblioteca: não roda o ciclo de correção (fumaça)")
    ap.add_argument("--teto-proposta", type=int, default=TETO_PROPOSTA_PADRAO, help="biblioteca: teto de tokens de saída da proposta de edição")
    # ! Alteração de IA - Revisar: (04/11/2026, P7) a opção do modo avaliacao_trilha.
    # ! Motivo: a fumaça sem as cobaias precisa pular o bloco do seletor quebrado (que sobe o front, a API e o navegador).
    ap.add_argument("--condicoes", default=None, help="experimento_prompt: condições separadas por vírgula (padrão: exemplar,rotulos_por_extenso)")
    ap.add_argument("--sem-seletor", action="store_true", help="avaliacao_trilha: não roda a mutação do seletor na tela (fumaça sem as cobaias); corrida parcial")
    return ap


def main() -> int:
    args = montar_parser().parse_args()
    print(caminhos.descricao())
    if args.modo == "reproducao":
        return rodar_reproducao(args)
    if args.modo == "calibracao":
        return rodar_calibracao(args)
    if args.modo == "tela":
        return rodar_tela(args)
    if args.modo == "cura":
        return rodar_cura(args)
    if args.modo == "biblioteca":
        return rodar_biblioteca(args)
    if args.modo == "cenarios":
        return rodar_cenarios(args)
    if args.modo == "avaliacao_trilha":
        return rodar_avaliacao_trilha(args)
    if args.modo == "experimento_prompt":
        import corridas_em_texto as ct
        return ct.rodar_experimento(args)
    if args.modo == "ineditos":
        import corridas_em_texto as ct
        return ct.rodar_ineditos(args)
    return 1


if __name__ == "__main__":
    sys.exit(main())
