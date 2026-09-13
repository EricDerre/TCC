#!/usr/bin/env python3
# ! Alteração de IA - Revisar: cria executar_fase3.py — o executor da Fase 3, que roda as
# épocas de um modelo por vez: diagnóstico de cada caso com a biblioteca da época anterior,
# proposta de edição nos casos de aprendizado, aplicação das propostas aceitas na cópia da
# época atual, fechamento da época e passada final de diagnóstico com a biblioteca já
# editada.
# ! Motivo: a Fase 2-B mediu o efeito de uma biblioteca ESCRITA À MÃO; a Fase 3 mede o que
# acontece quando o próprio modelo acrescenta documentação ao longo de 3 épocas. São 4
# passadas de 90 diagnósticos mais 3 passadas de 54 propostas por modelo — dezenas de horas
# em CPU —, então tudo aqui é pensado para poder ser interrompido e retomado: cada inferência
# vira uma linha de JSONL gravada com flush, a chave de retomada é (modelo, época, caso,
# tipo), e a pasta da época é RECONSTRUÍDA do JSONL (evolucao_biblioteca.abrir_epoca) em vez
# de ser confiada como está em disco. Sem isso, uma queda no meio da época 2 obrigaria a
# refazer a corrida inteira do modelo, e uma pasta de época meio escrita faria os
# diagnósticos seguintes rodarem contra uma documentação diferente da que foi registrada.
"""Executor da Fase 3: épocas de diagnóstico e proposta de edição por modelo, com a cópia
da biblioteca de cada modelo crescendo por acréscimo a cada época. Grava um JSONL por
(modelo, época, tipo) e fecha cada época com hash, diffs e INDICE.md próprios."""
import argparse
import ctypes
import hashlib
import json
import os
import platform
import shutil
import sys
import time
from datetime import datetime
from pathlib import Path

import avaliar
import biblioteca as bib
import caminhos
import cliente_ollama as oll
import evolucao_biblioteca as evo
import recuperacao as rec
import validar_banco
from banco_casos import CASOS
from banco_casos_extra import CASOS_EXTRA
from estrategias import linear_com_biblioteca, proposta_de_edicao
from executar_bateria import (ambiente_residente, guarda_estimativa, guarda_tokens_reais,
                              inferir_seguro, ler_jsonl)

# ! Alteração de IA - Revisar: força UTF-8 na saída do console, copiado de
# biblioteca.py:25-32.
# ! Motivo: no Windows o console pode estar em cp1252, que não representa os símbolos usados
# nas mensagens daqui (·, ≈, →) — sem isso o executor aborta com UnicodeEncodeError no meio
# da corrida, depois de horas de inferência já gravadas.
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


# --------------------------------------------------------------------- constantes

TODOS_OS_CASOS = CASOS + CASOS_EXTRA

# A Fase 3 fixa o braço vencedor da Fase 2-A/2-B: prompt linear (37,4% contra 29,7% e 31,1%
# na 2-A) com a biblioteca RECUPERADA top-k (A2). Variar estratégia ou condição aqui
# misturaria dois efeitos na mesma medição — o da evolução da biblioteca e o do prompt.
ESTRATEGIA = "linear"
CONDICAO = "A2"

# Pausa entre descarregar o modelo e conferir que ele saiu da memória, igual a
# executar_bateria.py:237. É constante de módulo (e não o 2 digitado dentro da função) para
# o teste do executor poder zerá-la: são 2 segundos por modelo que não medem nada.
PAUSA_DESCARGA = 2

# ! Alteração de IA - Revisar: número de tentativas de uma mesma inferência e as pausas (em
# segundos) entre elas, quando o Ollama devolve erro de rede/timeout — round 1 de revisão.
# ! Motivo: inferir_seguro devolve {"erro": ...,"resposta": "", "tokens_entrada": 0} quando a
# chamada ao Ollama falha, e até esta correção esse dicionário virava registro: o caso ficava
# marcado como feito para sempre com resposta vazia, e num caso de aprendizado a proposta era
# montada em cima de um diagnóstico que nunca aconteceu. Numa corrida de ~60 horas, um
# soluço do servidor (recarga do modelo, pico de memória, timeout de 900 s) é esperado, e
# repetir depois de esperar resolve a maioria deles sem intervenção. As pausas sobem porque a
# causa mais comum, memória disputada com outro processo, leva dezenas de segundos para
# passar; a terceira entrada (120 s) é a pausa que valeria para uma quarta tentativa, se
# MAX_TENTATIVAS_INFERENCIA for aumentado. As constantes ficam no módulo para o teste poder
# zerar as pausas — com os valores reais, o teste sozinho levaria 1,5 minuto.
MAX_TENTATIVAS_INFERENCIA = 3
PAUSAS_ENTRE_TENTATIVAS = (30, 60, 120)

# ! Alteração de IA - Revisar: velocidades medidas na Fase 2-B, por modelo — (milissegundos
# por token de PREFILL, tokens por segundo de GERAÇÃO).
# ! Motivo: a projeção de tempo impressa no início é o que diz se a corrida de um modelo cabe
# na janela disponível antes de começá-la (a 2-B levou ~60h nesta máquina). Prefill e geração
# entram separados porque na Fase 3 o prompt é grande e a resposta é curta: o custo é
# dominado pelo prefill, e usar um único "tokens por segundo" erraria a conta por horas.
# Modelo fora desta tabela cai em VELOCIDADE_PADRAO, que é propositalmente pessimista.
VELOCIDADE_MEDIDA = {
    "granite4.2:8b": (61.8, 3.9),
    "qwen2.5-coder:7b": (44.0, 4.2),
    "qwen2.5:7b": (43.8, 4.1),
    "qwen2.5-coder:3b": (20.0, 6.3),
}
VELOCIDADE_PADRAO = (50.0, 4.0)

# Tamanhos típicos medidos na 2-B (condição A2, k=3): o prompt de diagnóstico fica em torno
# de 1.350 tokens e a resposta em 200; o de proposta repete o de diagnóstico e acrescenta a
# resposta, a correção e as instruções (~1.600 tokens), com resposta de ~350.
TOKENS_PROMPT_DIAGNOSTICO, TOKENS_RESPOSTA_DIAGNOSTICO = 1350, 200
TOKENS_PROMPT_PROPOSTA, TOKENS_RESPOSTA_PROPOSTA = 1600, 350

# ! Alteração de IA - Revisar: as constantes PASSADAS_DIAGNOSTICO/PASSADAS_PROPOSTA (4 e 3)
# saíram; a projeção conta epocas+1 passadas de diagnóstico (as épocas mais a passada final
# com a biblioteca da última época) e epocas de proposta (só as épocas de aprendizado) a
# partir do --epocas da execução — onda final de correções.
# ! Motivo: no piloto (-Piloto: 10 casos, 1 época) a projeção impressa dizia "4 passadas de
# diagnóstico e 3 de proposta ... 1,09 h" para uma corrida de 2 passadas de diagnóstico e 1
# de proposta, que levou 13 min — o número impresso não descrevia a corrida que ia rodar.
# Número de épocas de aprendizado da corrida oficial; é o padrão de --epocas e da projeção.
EPOCAS_PADRAO = 3


# ------------------------------------------------------------------------ auxiliares

def _slug(modelo: str) -> str:
    """! Alteração de IA - Revisar: nome de pasta/arquivo a partir do nome do modelo, com a
    mesma troca de ':' por '_' que executar_bateria._arquivo_saida já usa.
    ! Motivo: ':' e '/' não são aceitos em nome de arquivo no Windows — 'qwen2.5-coder:3b'
    vira 'qwen2.5-coder_3b', que é como os JSONL da Fase 2-B já estão nomeados em
    resultados_alvo/; usar outra regra aqui faria a análise ter de casar dois nomes
    diferentes para o mesmo modelo."""
    return modelo.replace(":", "_").replace("/", "_")


def _sha12(texto: str) -> str:
    """! Alteração de IA - Revisar: sha256 do texto reduzido a 12 caracteres hex.
    ! Motivo: é o campo contexto_sha256 de cada diagnóstico, que prova que dois registros da
    mesma época viram o MESMO contexto (ou não) sem gravar o prompt inteiro em todas as
    linhas do JSONL — o prompt de A2 tem ~3,5 mil caracteres e são 360 diagnósticos por
    modelo. Os mesmos 12 caracteres de evolucao_biblioteca.hash_biblioteca."""
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()[:12]


def _estourou(tokens_entrada: int, teto_tokens: int) -> bool:
    """! Alteração de IA - Revisar: repete, como valor gravado no registro, a mesma conta da
    guarda de tokens reais (executar_bateria.guarda_tokens_reais).
    ! Motivo: a guarda ABORTA a época quando o prompt encosta em num_ctx (8192), então este
    campo sai False em todo registro gravado. Ele existe para auditoria: se um dia a guarda
    for afrouxada, dá para separar na análise os registros em que o Ollama pode ter descartado
    o começo do prompt (a biblioteca) sem avisar, em vez de descobrir isso relendo tudo."""
    return bool(tokens_entrada and tokens_entrada + teto_tokens >= oll.NUM_CTX - 16)


def _gravar(arquivo: Path, registro: dict) -> None:
    """! Alteração de IA - Revisar: acrescenta uma linha ao JSONL, abrindo e fechando o
    arquivo a cada registro.
    ! Motivo: a época intercala dois arquivos (diagnosticos__L<n-1>.jsonl e
    propostas__E<n>.jsonl), então manter os dois abertos num `with` durante horas deixaria
    duas linhas a meio gravar se a corrida caísse. Abrir por registro custa microssegundos
    ao lado de uma inferência de ~60 s e garante que o que está no arquivo já está no disco;
    o flush() explícito é o mesmo de executar_bateria.py:228."""
    arquivo.parent.mkdir(parents=True, exist_ok=True)
    with arquivo.open("a", encoding="utf-8") as f:
        f.write(json.dumps(registro, ensure_ascii=False) + "\n")
        f.flush()


def _e_aprendizado(particao: dict, caso: dict) -> bool:
    """! Alteração de IA - Revisar: True quando o caso está na metade de APRENDIZADO da
    partição (evolucao_biblioteca.particionar).
    ! Motivo: só esses casos geram proposta de edição; os de avaliação são medidos época após
    época sem nunca entrar na biblioteca. Concentrar a pergunta numa função evita que um
    ponto do executor use 'aprendizado' e outro use o inverso por engano — o que faria a
    biblioteca crescer com casos que deveriam medir generalização."""
    return evo.particao_de(particao, caso["id"]) == "aprendizado"


def _ram_total_mb() -> int | None:
    """! Alteração de IA - Revisar: RAM física total em MB pelo GlobalMemoryStatusEx do
    kernel32; None fora do Windows.
    ! Motivo: o maquina.json da Fase 2-B (rodar_fase2b.ps1:136-149) registra a RAM porque os
    modelos de 7-8 B em CPU com num_ctx 8192 chegam perto do limite dos 16 GB da máquina-alvo
    — sem esse número, um resultado lento não dá para separar de um resultado com paginação.
    Aqui o executor é chamado direto por Python (não pelo .ps1), então a leitura vem por
    ctypes, sem dependência nova."""
    if platform.system() != "Windows":
        return None

    class _Memoria(ctypes.Structure):
        _fields_ = [("dwLength", ctypes.c_ulong), ("dwMemoryLoad", ctypes.c_ulong),
                    ("ullTotalPhys", ctypes.c_ulonglong),
                    ("ullAvailPhys", ctypes.c_ulonglong),
                    ("ullTotalPageFile", ctypes.c_ulonglong),
                    ("ullAvailPageFile", ctypes.c_ulonglong),
                    ("ullTotalVirtual", ctypes.c_ulonglong),
                    ("ullAvailVirtual", ctypes.c_ulonglong),
                    ("ullAvailExtendedVirtual", ctypes.c_ulonglong)]

    try:
        estado = _Memoria()
        estado.dwLength = ctypes.sizeof(_Memoria)
        if not ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(estado)):
            return None
        return round(estado.ullTotalPhys / 1024 / 1024)
    except Exception:
        return None


def maquina_atual(saida: str) -> dict:
    """! Alteração de IA - Revisar: o equivalente em Python do maquina.json que
    rodar_fase2b.ps1 grava (hostname, CPU, núcleos, RAM, sistema, Ollama, Python, início).
    ! Motivo: os resultados da Fase 3 vão ser comparados com os da Fase 2-B caso a caso, e
    tempo medido em máquina diferente não é comparável; gravar a máquina junto com os
    resultados é o que permite descartar (ou explicar) uma corrida feita em outro
    computador. A versão do Ollama vem do endpoint /api/version em vez de `ollama --version`
    porque o executor já fala com o servidor por HTTP e um subprocesso a mais poderia falhar
    com o binário fora do PATH."""
    return {
        "hostname": platform.node(),
        "cpu": platform.processor(),
        "cpus_logicas": os.cpu_count(),
        "ram_mb": _ram_total_mb(),
        "sistema": platform.platform(),
        "ollama": _versao_ollama(),
        "python": sys.version,
        "inicio": datetime.now().isoformat(timespec="seconds"),
        "saida": saida,
    }


def _versao_ollama() -> str | None:
    """! Alteração de IA - Revisar: versão do servidor Ollama por GET /api/version, ou None.
    ! Motivo: a tag de um modelo no Ollama é ponteiro mutável e o servidor muda de versão
    entre releases; sem a versão gravada, um resultado da Fase 3 não é reproduzível depois. O
    try/except é porque o executor não pode morrer por causa de um campo de metadado — se o
    servidor não responder aqui, a primeira inferência vai falhar de qualquer jeito, com uma
    mensagem melhor."""
    try:
        return oll._get("/api/version").get("version")
    except Exception:
        return None


def atualizar_maquina(caminho: Path, atual: dict) -> dict:
    """! Alteração de IA - Revisar: grava maquina.json preservando, num relance, o 'inicio'
    e a versão do Ollama da PRIMEIRA execução; cada relance entra na lista 'relances'
    ({inicio, ollama}). Gravação atômica (evolucao_biblioteca._gravar_json_atomico) — onda
    final (achados I5 e M12).
    ! Motivo: o executor regravava maquina.json inteiro a cada relance, então o 'inicio'
    passava a ser o do último relance (a corrida de ~60 h em sessões de vários dias perdia
    a data em que começou) e a versão do Ollama gravada era sempre a atual — apagando a
    prova de que a corrida começou noutra versão, que é justamente o que
    _conferir_versao_ollama precisa para abortar um relance com o servidor atualizado no
    meio. Os demais campos (CPU, RAM, Python) continuam vindo da execução atual."""
    if caminho.exists():
        gravado = json.loads(caminho.read_text(encoding="utf-8-sig"))
        relances = list(gravado.get("relances", []))
        relances.append({"inicio": atual.get("inicio"), "ollama": atual.get("ollama")})
        # 'or' em vez de get(chave, padrão): um null gravado na primeira execução (servidor
        # fora do ar no instante de maquina_atual) é substituído pelo valor atual, senão a
        # versão original ficaria vazia para sempre e _conferir_versao_ollama nunca compararia.
        dado = {**atual, "inicio": gravado.get("inicio") or atual.get("inicio"),
                "ollama": gravado.get("ollama") or atual.get("ollama"), "relances": relances}
    else:
        dado = dict(atual)
    evo._gravar_json_atomico(caminho, dado)
    return dado


def _conferir_versao_ollama(caminho_maquina: Path, atual: str | None) -> None:
    """! Alteração de IA - Revisar: para com SystemExit se a versão do Ollama de agora é
    diferente da que maquina.json gravou no início da corrida — onda final (achado I5).
    ! Motivo: o Ollama atualizou sozinho de 0.33.3 para 0.34.0 entre a 2-B e a Fase 3 (a
    máquina é corporativa, a atualização é automática). Se isso acontecer de novo no meio
    dos ~60 h, metade das épocas de um modelo sairia de um runtime e metade de outro, e a
    comparação entre as épocas — a pergunta da Fase 3 — passaria a medir também a mudança
    de versão. Parar antes da primeira inferência deixa o Eric decidir (reverter a versão,
    ou aceitar e registrar) em vez de descobrir na análise. Sem maquina.json (primeira
    execução) ou sem versão de um dos lados, não há o que comparar."""
    if not caminho_maquina.exists() or not atual:
        return
    gravada = json.loads(caminho_maquina.read_text(encoding="utf-8-sig")).get("ollama")
    if gravada and gravada != atual:
        raise SystemExit(
            f"o Ollama está na versão {atual}, mas esta corrida começou na {gravada} "
            f"(maquina.json) — as épocas de um mesmo modelo não podem misturar versões do "
            f"servidor; volte para a {gravada} ou use outra --saida para uma corrida nova")


# --------------------------------------------------------------- projeção de tempo

# ! Alteração de IA - Revisar: projeta, por modelo, quantas horas a corrida da Fase 3 leva,
# a partir das velocidades medidas na Fase 2-B.
# ! Motivo: a corrida é de dezenas de horas por modelo em CPU e é lançada em sessões de
# vários dias; sem um número impresso ANTES de começar, a única forma de descobrir que um
# modelo não cabe na janela disponível seria deixá-lo rodando e ver. A conta separa prefill
# de geração porque na Fase 3 o prompt (biblioteca + caso) é ~7x maior que a resposta — um
# "tokens por segundo" único erraria por horas. É estimativa, não medição: o piloto da
# Tarefa 12 é que mede o tempo real por caso.
def projecao_tempo(modelos: list[str], n_casos: int, n_aprendizado: int,
                   epocas: int = EPOCAS_PADRAO) -> dict:
    # epocas+1 passadas de diagnóstico (a passada final não propõe nada) e epocas de
    # proposta — ver a nota em EPOCAS_PADRAO.
    passadas_diagnostico, passadas_proposta = epocas + 1, epocas
    por_modelo = {}
    for modelo in modelos:
        prefill_ms, tokens_s = VELOCIDADE_MEDIDA.get(modelo, VELOCIDADE_PADRAO)
        s_diag = passadas_diagnostico * n_casos * (
            TOKENS_PROMPT_DIAGNOSTICO * prefill_ms / 1000
            + TOKENS_RESPOSTA_DIAGNOSTICO / tokens_s)
        s_prop = passadas_proposta * n_aprendizado * (
            TOKENS_PROMPT_PROPOSTA * prefill_ms / 1000
            + TOKENS_RESPOSTA_PROPOSTA / tokens_s)
        diagnosticos_h = round(s_diag / 3600, 2)
        propostas_h = round(s_prop / 3600, 2)
        por_modelo[modelo] = {
            "prefill_ms_por_token": prefill_ms, "tokens_por_segundo": tokens_s,
            "medido_na_fase2b": modelo in VELOCIDADE_MEDIDA,
            "diagnosticos_h": diagnosticos_h, "propostas_h": propostas_h,
            # total_h soma os dois valores JÁ arredondados para as três horas fecharem na
            # tabela impressa (senão a linha do modelo não bate com as parcelas dela).
            "total_h": round(diagnosticos_h + propostas_h, 2)}
    return {"por_modelo": por_modelo,
            "epocas": epocas, "passadas_diagnostico": passadas_diagnostico,
            "passadas_proposta": passadas_proposta,
            "total_h": round(sum(m["total_h"] for m in por_modelo.values()), 2)}


def imprimir_projecao(projecao: dict, n_casos: int, n_aprendizado: int) -> None:
    """! Alteração de IA - Revisar: imprime a tabela da projeção, sempre com a ressalva de
    que é estimativa.
    ! Motivo: o número impresso vai parar em anotação de caderno e no Memorial; sem a
    ressalva junto, uma estimativa de tabela vira 'medição' na escrita do trabalho. O
    asterisco marca o modelo que não foi medido na 2-B e está na velocidade padrão."""
    print(f"\nprojeção de tempo — {n_casos} casos "
          f"({n_aprendizado} de aprendizado), {projecao['passadas_diagnostico']} passadas "
          f"de diagnóstico e {projecao['passadas_proposta']} de proposta "
          f"({projecao['epocas']} época(s) + passada final):")
    for modelo, dados in projecao["por_modelo"].items():
        marca = "" if dados["medido_na_fase2b"] else " *"
        print(f"  {modelo}{marca}: {dados['diagnosticos_h']:.2f} h de diagnóstico + "
              f"{dados['propostas_h']:.2f} h de proposta = {dados['total_h']:.2f} h")
    print(f"  total: {projecao['total_h']:.2f} h")
    print("  (* velocidade padrão: modelo não medido na Fase 2-B)")
    print("  estimativa a partir dos ms/token da Fase 2-B; o piloto mede o tempo real.")


# ------------------------------------------------------------------------ época zero

# ! Alteração de IA - Revisar: prepara epoca-0 do modelo — cópia da biblioteca original,
# INDICE.md regerado e fechamento.json gravado — e confere que o hash bate com o da epoca-0
# de qualquer outro modelo que já tenha rodado.
# ! Motivo: as épocas são medidas por diferença contra a época 0; se dois modelos partissem
# de bibliotecas diferentes (porque base_conhecimento/ mudou entre as duas corridas), a
# comparação entre eles mediria a diferença de ponto de partida, não a de aprendizado. O
# hash é conferido contra as pastas já existentes justamente porque as corridas acontecem em
# dias diferentes. Uma pasta epoca-0 que existe mas não fechou é de uma cópia interrompida:
# é apagada e refeita, porque copiar_biblioteca recusa destino existente.
def preparar_epoca_0(pasta_bib: Path, original: Path, modelo: str,
                     bibliotecas: Path, versao_ollama: str | None = None) -> Path:
    # versao_ollama vai para o fechamento.json da epoca-0 (achado I5).
    raiz = pasta_bib / "epoca-0"
    if not evo.snapshot_fechado(raiz):
        if raiz.exists():
            print(f"  epoca-0 existia sem fechamento (cópia interrompida) — refazendo")
            shutil.rmtree(raiz)
        evo.copiar_biblioteca(original, raiz)
        verbetes = bib.carregar(raiz)
        problemas = bib.validar(verbetes, TODOS_OS_CASOS, teto_global=None)
        if problemas:
            raise SystemExit("biblioteca original inválida — rode validar_banco.py:\n  "
                             + "\n  ".join(problemas))
        validar_banco.escrever_indice(verbetes, raiz)
        evo.fechar_snapshot(raiz, 0, modelo, 0, versao_ollama=versao_ollama)

    meu = json.loads((raiz / "fechamento.json").read_text(encoding="utf-8"))["hash"]
    for outro in sorted(bibliotecas.glob("*/epoca-0/fechamento.json")):
        if outro.parent.parent == pasta_bib:
            continue
        dele = json.loads(outro.read_text(encoding="utf-8"))["hash"]
        if dele != meu:
            raise SystemExit(
                f"epoca-0 de {modelo} tem hash {meu} e a de "
                f"{outro.parent.parent.name} tem {dele} — os modelos partiriam de "
                "bibliotecas diferentes e a comparação entre eles não valeria")
    print(f"  epoca-0: hash {meu}")
    return raiz


# -------------------------------------------------------------- uma inferência de cada

def contexto_e_prompt(verbetes: list[dict], indice: rec.Indice, caso: dict,
                      k: int) -> tuple[dict, str]:
    """! Alteração de IA - Revisar: monta o contexto A2 (top-k recuperados) e o prompt de
    diagnóstico de um caso, num lugar só.
    ! Motivo: o mesmo par é usado três vezes — na guarda de tamanho antes da época, na
    inferência do diagnóstico e na RECONSTRUÇÃO do prompt quando o diagnóstico já está
    gravado e só falta a proposta (o prompt não é gravado no JSONL, é reconstruído da cópia
    da época com estes mesmos verbetes). Se os três montassem o prompt por conta própria,
    bastaria um deles passar k diferente para o prompt da proposta deixar de ser a
    continuação byte a byte do de diagnóstico — e o cache de prefixo do Ollama, que é o que
    torna a corrida viável, deixaria de valer sem nenhum erro aparecer."""
    ctx = rec.contexto(verbetes, indice, caso, CONDICAO, k)
    return ctx, linear_com_biblioteca(caso, ctx["texto"])


# ! Alteração de IA - Revisar: repete a inferência enquanto ela voltar com erro de rede, até
# MAX_TENTATIVAS_INFERENCIA, esperando PAUSAS_ENTRE_TENTATIVAS entre uma e outra; esgotadas as
# tentativas, para a execução com SystemExit sem devolver nada — round 1 de revisão.
# ! Motivo: até aqui o dicionário de erro de inferir_seguro (rede/timeout: resposta vazia,
# tokens_entrada 0) virava registro no JSONL, e a partir daí o caso contava como feito para
# sempre — a retomada nunca o refazia, a resposta vazia entrava na avaliação como diagnóstico
# errado e, num caso de aprendizado, a proposta era montada em cima de um diagnóstico que não
# aconteceu. Parar sem gravar é a mesma política da guarda de tokens (guarda_tokens_reais):
# registro que não descreve uma inferência de verdade não entra no arquivo, e a retomada
# recomeça exatamente deste caso. As mensagens impressas dizem qual caso e qual erro, porque
# numa corrida de horas ninguém está olhando o console na hora em que a falha acontece.
def inferir_com_repeticao(modelo: str, prompt: str, max_tokens: int, caso_id: str,
                          tipo: str) -> dict:
    erro = None
    for tentativa in range(1, MAX_TENTATIVAS_INFERENCIA + 1):
        r = inferir_seguro(modelo, prompt, max_tokens)
        erro = r.get("erro")
        if not erro:
            if tentativa > 1:
                print(f"     {caso_id} · {tipo}: tentativa {tentativa} deu certo")
            return r
        print(f"  !! {caso_id} · {tipo}: tentativa {tentativa} de "
              f"{MAX_TENTATIVAS_INFERENCIA} falhou — {erro}")
        if tentativa < MAX_TENTATIVAS_INFERENCIA:
            pausa = PAUSAS_ENTRE_TENTATIVAS[min(tentativa - 1,
                                                len(PAUSAS_ENTRE_TENTATIVAS) - 1)]
            print(f"     esperando {pausa} s antes de repetir")
            time.sleep(pausa)
    raise SystemExit(
        f"{tipo} do caso {caso_id} falhou nas {MAX_TENTATIVAS_INFERENCIA} tentativas — "
        f"último erro: {erro} (registro NÃO gravado; confira se o Ollama está no ar e "
        "relance: a retomada recomeça neste caso)")


# ! Alteração de IA - Revisar: uma inferência de diagnóstico, com a guarda de tokens reais
# ANTES de montar o registro, e o registro no formato dos JSONL da Fase 2-B mais os campos
# de época.
# ! Motivo: as colunas repetem as de executar_bateria.py:205-226 de propósito — a análise da
# Fase 3 compara caso a caso com a Fase 2-B, e coluna com outro nome obrigaria a converter os
# dois arquivos antes de cada gráfico. A guarda roda em TODA inferência (e não só na
# primeira, como na 2-B) porque aqui a biblioteca CRESCE a cada época: o prompt que cabia na
# época 1 pode encostar em num_ctx na época 3, e quando isso acontece o Ollama descarta os
# tokens do começo — a biblioteca — sem erro nenhum. Levantando antes de montar o registro,
# a linha não chega a ser gravada.
def diagnosticar(modelo: str, caso: dict, verbetes: list[dict], ctx: dict, prompt: str,
                 max_tokens: int, comum: dict) -> dict:
    # ! Alteração de IA - Revisar: a inferência passa por inferir_com_repeticao (round 1 de
    # revisão), que repete a chamada quando o Ollama volta com erro e para a execução se as
    # três tentativas falharem.
    # ! Motivo: antes, a falha de rede virava um registro com resposta vazia e o caso ficava
    # marcado como feito para sempre — ver inferir_com_repeticao acima.
    r = inferir_com_repeticao(modelo, prompt, max_tokens, caso["id"], "diagnóstico")
    guarda_tokens_reais(r.get("tokens_entrada", 0), max_tokens,
                        f"diagnóstico da época {comum['epoca']}")
    por_id = {v["id"]: v for v in verbetes}
    recuperados = [por_id[i] for i in ctx["verbetes_ids"] if i in por_id]
    # versao_ollama ao lado do digest: os dois dizem qual binário produziu a linha (I5).
    return {
        "modelo": modelo, "digest": comum["digest"],
        "versao_ollama": comum["versao_ollama"], "maquina": comum["maquina"],
        "caso": caso["id"], "classe": caso["classe"], "nivel": caso["nivel"],
        "estrategia": ESTRATEGIA, "condicao": CONDICAO,
        "fase": "3", "tipo": "diagnostico", "epoca": comum["epoca"],
        "biblioteca_epoca": comum["biblioteca_epoca"],
        "biblioteca_versao": comum["biblioteca_versao"],
        "particao": evo.particao_de(comum["particao"], caso["id"]), "k": comum["k"],
        "contexto_sha256": _sha12(ctx["texto"]),
        "notas_no_contexto": sum(len(bib.notas(v)) for v in recuperados),
        "verbetes_novos_no_contexto": [v["id"] for v in recuperados
                                       if v["pasta"] == evo.PASTA_APRENDIDOS],
        "contexto_estourou": _estourou(r.get("tokens_entrada", 0), max_tokens),
        "verbetes_ids": ctx["verbetes_ids"], "verbete_ouro": ctx["verbete_ouro"],
        "causa_plantada": ctx["causa_plantada"], "chars_contexto": len(ctx["texto"]),
        "gabarito": caso["gabarito"], "teto_tokens": max_tokens,
        **r,
        **ambiente_residente(),
    }


def diagnostico_acertou(caso: dict, resposta: str) -> tuple[str | None, bool]:
    """! Alteração de IA - Revisar: lê a CAUSA_RAIZ da resposta com avaliar.extrair e
    compara com o gabarito pela regra do avaliador (avaliar._normalizar).
    ! Motivo: o prompt de proposta diz ao modelo se ele acertou ou errou o diagnóstico, e
    esse veredito precisa ser o MESMO que avaliar.py vai calcular depois sobre o JSONL — se o
    executor usasse comparação exata e o avaliador comparasse sem acento, o Memorial teria
    dois números de acerto para o mesmo caso. Sem acento porque o conjunto fechado de causas
    é escrito sem acentuação e vários modelos devolvem 'coleção_no_lugar_de_objeto'."""
    causa_respondida = avaliar.extrair(resposta)["causa_raiz"]
    acertou = bool(causa_respondida) and (
        avaliar._normalizar(causa_respondida)
        == avaliar._normalizar(caso["gabarito"]["causa_raiz"]))
    return causa_respondida, acertou


# ! Alteração de IA - Revisar: a inferência de proposta de edição de um caso de aprendizado —
# monta o segundo prompt como continuação literal do de diagnóstico, parseia os blocos,
# valida um por um na ordem, aplica em disco os aceitos e devolve o registro com todas as
# decisões e o hash da cópia depois deles.
# ! Motivo: o hash gravado no fim (hash_biblioteca_apos) é o que abrir_epoca confere ao
# retomar — é ele que garante que a biblioteca reconstruída do JSONL é a mesma que o modelo
# viu. Os verbetes do ctx de validação são RECARREGADOS do disco depois de cada edição aceita
# porque a segunda proposta do mesmo caso pode mexer no verbete que a primeira acabou de
# alterar, e validar a segunda contra a versão antiga deixaria passar uma nota que estoura o
# teto de 800 caracteres do verbete. Proposta recusada não é corrigida nem podada: fica a
# decisão com o código de rejeição, que é o dado do experimento.
def propor(modelo: str, caso: dict, registro_diag: dict, ctx: dict, prompt_diag: str,
           verbetes_leitura: list[dict], max_tokens: int, comum: dict,
           ctx_validacao: dict, pasta_bib: Path, ordem: int) -> dict:
    resposta_diag = registro_diag.get("resposta", "")
    causa_respondida, acertou = diagnostico_acertou(caso, resposta_diag)
    ids_visiveis = sorted(set(ctx["verbetes_ids"]) | {ctx["verbete_ouro"]})
    # O verbete de ouro é renderizado a partir da biblioteca de LEITURA (a época anterior,
    # fechada), que é a mesma de onde saiu o contexto do diagnóstico: é o verbete que teria
    # ajudado naquele diagnóstico, não a versão já alterada nesta época.
    ouro = next(v for v in verbetes_leitura if v["id"] == ctx["verbete_ouro"])
    prompt = proposta_de_edicao(prompt_diag, resposta_diag, caso, acertou,
                                causa_respondida, bib.render(ouro), ids_visiveis)

    # ! Alteração de IA - Revisar: mesma troca do diagnóstico — a inferência de proposta passa
    # por inferir_com_repeticao (round 1 de revisão).
    # ! Motivo: uma proposta perdida por falha de rede ficava gravada como "nenhuma proposta"
    # (resposta vazia vira a decisão sem_bloco) e o caso nunca era refeito, tirando do
    # experimento uma das 54 chances de aprendizado daquela época.
    r = inferir_com_repeticao(modelo, prompt, max_tokens, caso["id"], "proposta")
    guarda_tokens_reais(r.get("tokens_entrada", 0), max_tokens,
                        f"proposta da época {comum['epoca']}")
    parseado = evo.parsear_propostas(r.get("resposta", ""), r.get("tokens_saida"),
                                     max_tokens)

    raiz = ctx_validacao["raiz"]
    decisoes = []
    for bloco in parseado["blocos"]:
        veredito = evo.validar_proposta(bloco, ctx_validacao)
        campos = bloco.get("campos", {})
        decisoes.append({
            "numero": bloco.get("numero", 0),
            "operacao": campos.get("OPERACAO", "").strip() or None,
            "verbete": campos.get("VERBETE", "").strip() or None,
            "aceita": veredito["aceita"], "motivo": veredito["motivo"],
            "detalhe": veredito["detalhe"], "edicao": veredito["edicao"]})
        if not veredito["aceita"]:
            continue
        edicao = veredito["edicao"]
        evo.aplicar_edicao(raiz, edicao)
        ordem += 1
        evo.registrar_historico(pasta_bib, edicao,
                                {"ordem": ordem, "acertou_diagnostico": acertou,
                                 "hash_apos": evo.hash_biblioteca(raiz)})
        ctx_validacao["verbetes"] = bib.carregar(raiz)
        ctx_validacao["aceitas_no_caso"] += 1
        if edicao["operacao"] == "novo_verbete":
            ctx_validacao["novos_nesta_epoca"] += 1

    if not parseado["blocos"] and not parseado["nenhuma"]:
        # Resposta que não traz bloco PROPOSTA nem a palavra NENHUMA: vira uma decisão com o
        # código 'sem_bloco', para o histograma de rejeições do relatório somar com o número
        # de casos de aprendizado em vez de ter um buraco sem explicação.
        veredito = evo.validar_proposta(None, ctx_validacao)
        decisoes.append({"numero": 0, "operacao": None, "verbete": None, "aceita": False,
                         "motivo": veredito["motivo"], "detalhe": veredito["detalhe"],
                         "edicao": None})

    return {
        "modelo": modelo, "digest": comum["digest"],
        "versao_ollama": comum["versao_ollama"], "maquina": comum["maquina"],
        "fase": "3", "tipo": "proposta", "epoca": comum["epoca"],
        "biblioteca_epoca": comum["biblioteca_epoca"],
        "biblioteca_versao": comum["biblioteca_versao"],
        "caso": caso["id"], "classe": caso["classe"], "nivel": caso["nivel"],
        "particao": evo.particao_de(comum["particao"], caso["id"]), "k": comum["k"],
        "verbetes_ids": ctx["verbetes_ids"], "verbete_ouro": ctx["verbete_ouro"],
        "ouro_no_contexto": ctx["verbete_ouro"] in ctx["verbetes_ids"],
        "ids_visiveis": ids_visiveis,
        "causa_correta_mostrada": caso["gabarito"]["causa_raiz"],
        # ! Alteração de IA - Revisar: campo_mostrado guarda o que o prompt de proposta
        # MOSTROU — "nenhum" quando o gabarito não tem campo afetado, a mesma troca de
        # estrategias.proposta_de_edicao — onda final (item 5).
        # ! Motivo: o nome do campo promete "o que foi mostrado", e o valor gravado era o
        # do gabarito (None); quem lê o JSONL para conferir o prompt contra o registro achava
        # um None onde o prompt diz "CAMPO AFETADO: nenhum". O valor cru do gabarito continua
        # em `gabarito` no registro de diagnóstico do mesmo caso.
        "campo_mostrado": caso["gabarito"]["campo_afetado"] or "nenhum",
        "causa_respondida": causa_respondida, "acertou_diagnostico": acertou,
        # O prompt de proposta é gravado inteiro (ao contrário do de diagnóstico, que é
        # reconstruível do snapshot + verbetes_ids): ele contém a resposta que o modelo deu
        # no diagnóstico e o verbete de ouro renderizado, que não saem de mais lugar nenhum.
        "prompt": prompt, "teto_tokens": max_tokens,
        **r,
        "contexto_estourou": _estourou(r.get("tokens_entrada", 0), max_tokens),
        "resposta_truncada": parseado["truncada"], "nenhuma": parseado["nenhuma"],
        "propostas_parseadas": parseado["blocos"], "decisoes": decisoes,
        "n_propostas": len(parseado["blocos"]),
        "n_aceitas": sum(1 for d in decisoes if d["aceita"]),
        "motivos_rejeicao": [d["motivo"] for d in decisoes
                             if not d["aceita"] and d["motivo"]],
        **ambiente_residente(),
        "hash_biblioteca_apos": evo.hash_biblioteca(raiz),
    }


# --------------------------------------------------------------------- uma época

def _conferir_contexto_reconstruido(caso: dict, ctx: dict, registro_diag: dict,
                                    k: int) -> None:
    """! Alteração de IA - Revisar: confere que o contexto recalculado para uma proposta órfã
    (diagnóstico já gravado, proposta não) é o MESMO que está no registro de diagnóstico —
    k, verbetes recuperados e verbete de ouro — e para a execução mostrando os dois lados se
    não for. Round 1 de revisão.
    ! Motivo: o prompt de diagnóstico não é gravado no JSONL, é remontado do snapshot da época
    anterior; a proposta é a continuação literal dele. Se alguém relançar com outro --k, ou se
    a pasta da época de leitura tiver sido mexida, a remontagem devolve outro contexto e a
    proposta viraria a continuação de um prompt que o modelo nunca viu — o registro diria que
    o modelo respondeu sobre os verbetes A, B e C tendo recebido D, E e F, e nada acusaria
    isso depois. Os três campos conferidos são exatamente os que determinam o texto do
    contexto (rec.contexto com condição A2)."""
    divergencias = []
    if registro_diag.get("k") != k:
        divergencias.append(f"k gravado {registro_diag.get('k')} x k desta execução {k}")
    if registro_diag.get("verbetes_ids") != ctx["verbetes_ids"]:
        divergencias.append(f"verbetes_ids gravados {registro_diag.get('verbetes_ids')} "
                            f"x recuperados agora {ctx['verbetes_ids']}")
    if registro_diag.get("verbete_ouro") != ctx["verbete_ouro"]:
        divergencias.append(f"verbete_ouro gravado {registro_diag.get('verbete_ouro')} "
                            f"x recuperado agora {ctx['verbete_ouro']}")
    if divergencias:
        raise SystemExit(
            f"o contexto remontado para a proposta do caso {caso['id']} não é o do "
            f"diagnóstico gravado: " + "; ".join(divergencias)
            + " — a proposta seria a continuação de um prompt que o modelo não viu; "
            "relance com o mesmo --k da execução anterior")


def _conferir_cobertura_da_epoca_fechada(n: int, casos: list[dict], particao: dict,
                                         arq_diag: Path, arq_prop: Path) -> None:
    """! Alteração de IA - Revisar: antes de pular uma época já fechada, confere que ela cobre
    todos os casos que ESTA execução pede — diagnóstico de todos e proposta de todos os de
    aprendizado — e para com SystemExit explicando a diferença. Round 1 de revisão.
    ! Motivo: a época fechada era pulada só por existir o fechamento.json. Quem rodasse um
    piloto de 3 casos e depois relançasse a corrida inteira na mesma --saida pularia a época
    1 sem os 87 casos que faltam, e a passada final mediria 90 casos contra uma biblioteca
    construída a partir de 3 — sem nenhum erro aparecer, e com o relatório dizendo que a
    época tinha rodado. A época não pode ser completada depois porque fechar_epoca já gravou
    hash, diffs e INDICE.md; a saída é apagar a pasta ou usar outra --saida."""
    feitos_d = {r["caso"] for r in ler_jsonl(arq_diag)}
    feitos_p = {r["caso"] for r in ler_jsonl(arq_prop)}
    faltam_d = [c["id"] for c in casos if c["id"] not in feitos_d]
    faltam_p = [c["id"] for c in casos
                if _e_aprendizado(particao, c) and c["id"] not in feitos_p]
    if not faltam_d and not faltam_p:
        return
    amostra_d = ", ".join(faltam_d[:5]) + ("..." if len(faltam_d) > 5 else "")
    amostra_p = ", ".join(faltam_p[:5]) + ("..." if len(faltam_p) > 5 else "")
    raise SystemExit(
        f"epoca-{n} está fechada com {len(feitos_d)} diagnóstico(s) e {len(feitos_p)} "
        f"proposta(s), mas esta execução pede {len(casos)} caso(s): faltam "
        f"{len(faltam_d)} diagnóstico(s) [{amostra_d}] e {len(faltam_p)} proposta(s) "
        f"[{amostra_p}] — pasta reutilizada com outro --casos? Apague a pasta de saída ou "
        "use outra --saida.")


# ! Alteração de IA - Revisar: roda a época n de um modelo — lê na época n-1 (fechada),
# escreve na época n, diagnostica todos os casos, propõe nos de aprendizado e fecha a época
# ao fim. Com n = epocas+1 é a passada final: só diagnóstico, sem pasta de escrita.
# ! Motivo: a retomada é toda decidida aqui, por três perguntas baratas, nesta ordem: a
# época já fechou (fechamento.json existe)? então nada a fazer. A época está aberta? então a
# pasta é reconstruída do JSONL de propostas, que é a fonte da verdade. O caso já tem
# registro no JSONL desta época? então ele não é refeito. É o que permite parar a corrida a
# qualquer momento sem perder nem repetir inferência — cada uma custa cerca de um minuto em
# CPU e são centenas por modelo.
def rodar_epoca(modelo: str, n: int, casos: list[dict], particao: dict, epocas: int,
                k: int, mt_diag: int, mt_prop: int, pasta: Path, pasta_bib: Path,
                digest: str, versao_ollama: str | None = None) -> None:
    # versao_ollama entra em todo registro (via `comum`) e no fechamento da época (I5).
    ultima = n > epocas
    leitura = pasta_bib / f"epoca-{n - 1}"
    if not evo.snapshot_fechado(leitura):
        raise SystemExit(f"época {n - 1} de {modelo} não está fechada ({leitura}) — "
                         "não dá para diagnosticar contra uma biblioteca em aberto")
    versao = json.loads((leitura / "fechamento.json").read_text(encoding="utf-8"))["hash"]

    rotulo = "passada final" if ultima else f"época {n}"
    print(f"\n-- {modelo} · {rotulo} · lê epoca-{n - 1} (hash {versao}) --")
    arq_diag = pasta / f"diagnosticos__L{n - 1}.jsonl"
    arq_prop = pasta / f"propostas__E{n}.jsonl"
    if not ultima and evo.snapshot_fechado(pasta_bib / f"epoca-{n}"):
        # ! Alteração de IA - Revisar: pular a época fechada passou a exigir que ela cubra
        # todos os casos pedidos (round 1 de revisão).
        # ! Motivo: ver _conferir_cobertura_da_epoca_fechada — época fechada com 3 casos e
        # execução pedindo 90 pulava tudo em silêncio.
        _conferir_cobertura_da_epoca_fechada(n, casos, particao, arq_diag, arq_prop)
        print(f"  epoca-{n} já fechada e cobrindo os {len(casos)} casos — pulando a época")
        return

    registros_prop = [] if ultima else ler_jsonl(arq_prop)
    raiz_escrita = None if ultima else evo.abrir_epoca(pasta_bib, n, registros_prop)

    verbetes_leitura = bib.carregar(leitura)
    indice_leitura = rec.Indice(verbetes_leitura)
    diag_por_caso = {r["caso"]: r for r in ler_jsonl(arq_diag)}
    feitos_p = {r["caso"] for r in registros_prop}
    pendentes = [c for c in casos
                 if c["id"] not in diag_por_caso
                 or (not ultima and _e_aprendizado(particao, c)
                     and c["id"] not in feitos_p)]
    print(f"  {len(casos) - len(pendentes)} caso(s) completos, {len(pendentes)} pendentes")

    if pendentes:
        # ! Alteração de IA - Revisar: a guarda estimada roda sobre o MAIOR prompt de
        # diagnóstico entre os casos pendentes, no início da época.
        # ! Motivo: mesma razão de executar_bateria.py:172-176 — quando o prompt passa de
        # num_ctx o Ollama descarta os tokens do começo, que é a biblioteca, e o caso rodaria
        # "com biblioteca" no registro e sem biblioteca de fato. Na Fase 3 isso fica mais
        # provável a cada época, porque as notas aceitas crescem dentro do verbete.
        maior = max(len(contexto_e_prompt(verbetes_leitura, indice_leitura, c, k)[1])
                    for c in pendentes)
        guarda_estimativa(maior, mt_diag, f"{rotulo} de {modelo}")

    comum = {"digest": digest, "versao_ollama": versao_ollama, "maquina": platform.node(),
             "epoca": n, "biblioteca_epoca": n - 1, "biblioteca_versao": versao,
             "particao": particao, "k": k}
    aceitas_na_epoca = sum(r.get("n_aceitas", 0) for r in registros_prop)
    ctx_validacao = None
    if not ultima:
        novos = sum(1 for r in registros_prop for d in r.get("decisoes", [])
                    if d.get("aceita") and (d.get("edicao") or {}).get("operacao")
                    == "novo_verbete")
        ctx_validacao = {"raiz": raiz_escrita, "verbetes": bib.carregar(raiz_escrita),
                         "casos": TODOS_OS_CASOS, "ids_visiveis": set(), "epoca": n,
                         "caso_id": None, "modelo": modelo, "novos_nesta_epoca": novos,
                         "aceitas_no_caso": 0, "k": k}

    inicio_lote = time.time()
    for i, caso in enumerate(pendentes, 1):
        ctx, prompt = contexto_e_prompt(verbetes_leitura, indice_leitura, caso, k)
        registro_diag = diag_por_caso.get(caso["id"])
        if registro_diag is None:
            registro_diag = diagnosticar(modelo, caso, verbetes_leitura, ctx, prompt,
                                         mt_diag, comum)
            _gravar(arq_diag, registro_diag)
            diag_por_caso[caso["id"]] = registro_diag
        else:
            # ! Alteração de IA - Revisar: o diagnóstico lido do JSONL (proposta órfã) passou
            # a ter o contexto remontado conferido contra o que está gravado — round 1 de
            # revisão.
            # ! Motivo: ver _conferir_contexto_reconstruido; relançar com outro --k montava a
            # proposta como continuação de um prompt diferente do que o modelo recebeu.
            _conferir_contexto_reconstruido(caso, ctx, registro_diag, k)

        if not ultima and _e_aprendizado(particao, caso) and caso["id"] not in feitos_p:
            # ! Alteração de IA - Revisar: proposta nunca sai de um diagnóstico gravado com
            # 'erro' (round 1 de revisão).
            # ! Motivo: desde inferir_com_repeticao nenhum registro com erro chega a ser
            # gravado, então isto só dispara em JSONL escrito pela versão anterior do
            # executor; a proposta ali sairia de uma resposta vazia, e o registro diria que o
            # modelo "não propôs nada" quando na verdade nunca foi perguntado.
            if registro_diag.get("erro"):
                raise SystemExit(
                    f"o diagnóstico gravado do caso {caso['id']} na época {n} tem erro "
                    f"({registro_diag['erro']}) e resposta vazia — apague essa linha de "
                    f"{arq_diag.name} e relance para o caso ser refeito")
            ctx_validacao["caso_id"] = caso["id"]
            ctx_validacao["aceitas_no_caso"] = 0
            ctx_validacao["ids_visiveis"] = set(ctx["verbetes_ids"]) | {ctx["verbete_ouro"]}
            registro_prop = propor(modelo, caso, registro_diag, ctx, prompt,
                                   verbetes_leitura, mt_prop, comum, ctx_validacao,
                                   pasta_bib, aceitas_na_epoca)
            _gravar(arq_prop, registro_prop)
            aceitas_na_epoca += registro_prop["n_aceitas"]
            motivos = (", ".join(registro_prop["motivos_rejeicao"])
                       or ("NENHUMA" if registro_prop["nenhuma"] else "sem rejeição"))
            print(f"  {caso['id']} · {registro_prop['n_aceitas']}/"
                  f"{registro_prop['n_propostas']} aceitas · {motivos}")

        if i % 10 == 0 or i == len(pendentes):
            decorrido = time.time() - inicio_lote
            resta = decorrido / i * (len(pendentes) - i)
            print(f"  {i}/{len(pendentes)} — {decorrido / 60:.1f} min decorridos, "
                  f"~{resta / 60:.1f} min restantes")

    if not ultima:
        # TODOS_OS_CASOS, e não `casos`: as checagens de fechar_epoca (bib.validar, incluindo
        # a sobreposição de 5-gramas que pega proposta copiada de um caso) valem contra o
        # banco inteiro mesmo quando a execução roda só N casos — uma nota que plagia um caso
        # que não foi rodado nesta corrida continua sendo plágio na corrida seguinte.
        fechamento = evo.fechar_epoca(pasta_bib, n, modelo, TODOS_OS_CASOS,
                                      aceitas_na_epoca, versao_ollama=versao_ollama)
        print(f"  epoca-{n} fechada: hash {fechamento['hash']}, "
              f"{fechamento['n_verbetes']} verbetes "
              f"({fechamento['n_verbetes_novos']} novos), "
              f"{fechamento['n_notas']} notas, "
              f"{fechamento['n_retificacoes']} retificações, "
              f"{fechamento['aceitas_na_epoca']} edições aceitas nesta época")


# ! Alteração de IA - Revisar: roda a Fase 3 inteira de UM modelo — época 0, as épocas de
# aprendizado, a passada final e o descarregamento do modelo ao fim.
# ! Motivo: um modelo residente por vez é exigência do desenho (dois modelos disputando
# memória contaminam tempo e uso de RAM), e é por isso que o descarregamento com pausa e a
# conferência vêm aqui, no fim do modelo, e não no fim de cada época — recarregar o modelo
# entre épocas jogaria fora o cache do Ollama e somaria minutos de carga a cada época.
def rodar_modelo_fase3(modelo: str, casos: list[dict], particao: dict, epocas: int,
                       k: int, mt_diag: int, mt_prop: int, c3: dict,
                       original: Path = bib.BASE) -> None:
    pasta = c3["raiz"] / _slug(modelo)
    pasta_bib = c3["bibliotecas"] / _slug(modelo)
    pasta.mkdir(parents=True, exist_ok=True)
    digest = oll.instalados().get(modelo, "?")
    # ! Alteração de IA - Revisar: a versão do Ollama é lida uma vez por modelo, conferida
    # contra a de maquina.json (_conferir_versao_ollama) e passada a todo registro e a todo
    # fechamento.json — onda final (achado I5).
    # ! Motivo: ver _conferir_versao_ollama — o servidor atualizou sozinho entre a 2-B e a
    # Fase 3, e uma atualização no meio da corrida ficaria invisível nos dados.
    versao_ollama = _versao_ollama()
    _conferir_versao_ollama(c3["maquina"], versao_ollama)
    print(f"\n=== {modelo} (digest {digest}, Ollama {versao_ollama}) — Fase 3, "
          f"{epocas} época(s), {len(casos)} casos ===")

    preparar_epoca_0(pasta_bib, original, modelo, c3["bibliotecas"], versao_ollama)
    # ! Alteração de IA - Revisar: o laço das épocas passou a rodar dentro de try/finally, com
    # o descarregamento do modelo no finally — round 1 de revisão.
    # ! Motivo: qualquer parada no meio (SystemExit das guardas e das conferências, Ctrl+C)
    # saía da função sem chamar oll.descarregar, e o modelo ficava residente ocupando 2 a 5 GB
    # até o keep_alive do Ollama expirar. O modelo seguinte da lista começaria disputando
    # memória com ele, que é justamente o que a exigência de "um modelo por vez" impede — e as
    # medições de tempo e memória desse segundo modelo sairiam contaminadas.
    try:
        # A passada final (n = epocas+1) diagnostica com a biblioteca da última época fechada
        # e não propõe nada: é ela que mede o efeito acumulado das edições sobre os casos de
        # avaliação, que nunca entraram na biblioteca.
        for n in range(1, epocas + 2):
            rodar_epoca(modelo, n, casos, particao, epocas, k, mt_diag, mt_prop,
                        pasta, pasta_bib, digest, versao_ollama)
    finally:
        # ! Alteração de IA - Revisar: o descarregamento e a conferência de residentes
        # ficam dentro de um try/except próprio — onda final (achado I7).
        # ! Motivo: se o Ollama caiu, as três tentativas de inferência esgotam e
        # inferir_com_repeticao levanta SystemExit; mas oll.um_modelo_por_vez() (GET /api/ps)
        # também falha, e uma exceção levantada dentro do finally SUBSTITUI a que estava em
        # voo — o main() recebia URLError em vez do SystemExit, não imprimia "!! modelo
        # parou" e a fila inteira caía em vez de seguir para o próximo modelo.
        # oll.descarregar já engole URLError por conta própria; a rede aqui pode falhar
        # por qualquer outra razão, e nada disso mede o experimento.
        try:
            oll.descarregar(modelo)
            time.sleep(PAUSA_DESCARGA)
            ok, nomes = oll.um_modelo_por_vez()
            if nomes:
                print(f"  aviso: ainda residente após descarregar: {nomes}")
        except Exception as e:
            print(f"  aviso: não deu para descarregar/conferir o modelo residente "
                  f"({type(e).__name__}: {e}) — confira 'ollama ps' antes do próximo modelo")


# ! Alteração de IA - Revisar: linha de comando do executor — modelos, épocas, recorte de
# casos, tetos de tokens, pasta de saída, biblioteca de partida e o modo --so-projecao, que
# imprime a projeção de tempo e sai sem gravar nada.
# ! Motivo: --so-projecao existe para poder responder "quanto tempo isso leva?" sem criar a
# pasta de resultados nem gravar particao.json — gravar a partição de uma consulta de tempo
# travaria a partição da Fase 3 inteira num diretório que talvez nunca fosse usado, e
# gravar_ou_conferir_particao recusa qualquer execução posterior com partição diferente. O
# --casos N recorta só quem RODA; a partição continua sendo calculada sobre os 90, senão o
# piloto e a corrida inteira dariam aprendizado/avaliação diferentes para o mesmo caso.
def main() -> None:
    ap = argparse.ArgumentParser(
        description="Executor da Fase 3: épocas de diagnóstico e proposta de edição da "
                    "biblioteca, um modelo por vez.")
    ap.add_argument("--modelos", nargs="+", required=True)
    ap.add_argument("--epocas", type=int, default=EPOCAS_PADRAO,
                    # ! Alteração de IA - Revisar: o padrão no help vem da constante EPOCAS_PADRAO.
                    # ! Motivo: o texto dizia "padrão 3" digitado enquanto default=EPOCAS_PADRAO; se a constante mudar, o help mentiria.
                    help=f"épocas de aprendizado (padrão {EPOCAS_PADRAO}); a passada final vem depois")
    ap.add_argument("--casos", type=int, default=0,
                    help="usar apenas os N primeiros casos (0 = todos os 90)")
    ap.add_argument("--k", type=int, default=3, help="verbetes recuperados (condição A2)")
    ap.add_argument("--max-tokens-diagnostico", type=int, default=600)
    ap.add_argument("--max-tokens-proposta", type=int, default=700)
    ap.add_argument("--saida", default="fase3",
                    help="subpasta dos resultados da Fase 3 (ver caminhos.fase3)")
    ap.add_argument("--original", default=str(bib.BASE),
                    help="biblioteca de partida copiada para epoca-0")
    ap.add_argument("--so-projecao", action="store_true",
                    help="imprime a projeção de tempo e sai, sem gravar nada")
    args = ap.parse_args()

    print(caminhos.descricao())
    c3 = caminhos.fase3(args.saida)
    casos = TODOS_OS_CASOS[:args.casos] if args.casos else TODOS_OS_CASOS
    # A partição é sempre calculada sobre os 90 casos, mesmo com --casos N: é ela que define
    # quem é aprendizado e quem é avaliação, e recalcular sobre um subconjunto daria outra
    # divisão (particionar exige as 18 células de 5) — o piloto deixaria de ser comparável
    # com a corrida inteira.
    particao = evo.particionar(TODOS_OS_CASOS)
    n_aprendizado = sum(1 for c in casos if _e_aprendizado(particao, c))
    projecao = projecao_tempo(args.modelos, len(casos), n_aprendizado, args.epocas)

    if args.so_projecao:
        imprimir_projecao(projecao, len(casos), n_aprendizado)
        return

    c3["raiz"].mkdir(parents=True, exist_ok=True)
    evo.gravar_ou_conferir_particao(c3["particao"], particao)
    # Relance preserva o início e a versão do Ollama da primeira execução (ver
    # atualizar_maquina); a conferência da versão é feita por modelo, em rodar_modelo_fase3.
    atualizar_maquina(c3["maquina"], maquina_atual(args.saida))
    imprimir_projecao(projecao, len(casos), n_aprendizado)
    print(f"\n{len(casos)} casos ({n_aprendizado} de aprendizado) x "
          f"{args.epocas} época(s) + passada final")

    instalados = oll.instalados()
    # ! Alteração de IA - Revisar: a parada de um modelo (SystemExit vindo das guardas, das
    # conferências de retomada ou das tentativas esgotadas de inferência) passou a ser
    # capturada por modelo — o laço segue para o próximo e a execução termina com código 1 se
    # algum modelo parou. Round 1 de revisão.
    # ! Motivo: são 4 modelos numa fila de ~60 horas, rodados de madrugada. Com o SystemExit
    # subindo direto, um modelo que encostasse em num_ctx na época 3 derrubava a fila inteira
    # e os outros três não rodavam — e só se descobria na manhã seguinte. Cada modelo tem a
    # sua cópia da biblioteca e o seu JSONL, então a parada de um não invalida os outros. O
    # código 1 no fim é o que impede a falha de passar por sucesso num script que encadeia.
    falhas: list[str] = []
    for modelo in args.modelos:
        if modelo not in instalados:
            print(f"\n!! {modelo} não está baixado — pulando.")
            continue
        ok, nomes = oll.um_modelo_por_vez()
        if not ok:
            print(f"!! há {len(nomes)} modelos residentes antes de começar: {nomes}")
        try:
            rodar_modelo_fase3(modelo, casos, particao, args.epocas, args.k,
                               args.max_tokens_diagnostico, args.max_tokens_proposta, c3,
                               original=Path(args.original))
        except SystemExit as e:
            print(f"\n!! {modelo} parou: {e}")
            falhas.append(modelo)

    print(f"\nResultados em {c3['raiz']}")
    if falhas:
        raise SystemExit(f"{len(falhas)} modelo(s) pararam antes do fim: "
                         f"{', '.join(falhas)} — veja as mensagens acima")


if __name__ == "__main__":
    main()
