#!/usr/bin/env python3
# ! Alteração de IA - Revisar: arquivo novo (08/11/2026, Pós-Fase 4, pacote Q4): a barra de progresso da inferência. Estima o tempo de cada
# chamada ao modelo em duas fases, com as taxas gravadas das respostas anteriores do mesmo modelo nesta máquina: a de leitura do prompt
# (prefill: os tokens do prompt, estimados pelos caracteres antes de enviar, divididos pela taxa de prefill em tokens por segundo) e a de
# escrita da resposta (geração: a mediana de tokens gerados nas respostas anteriores dividida pela taxa de geração, com o teto de saída
# como máximo). A barra começa indeterminada com a etapa nomeada ("lendo o caso, N tokens"), vira determinada assim que a estimativa existe,
# sem trocar de forma (os mesmos colchetes e a mesma largura), nunca recua, fica em 90% quando o decorrido iguala a estimativa e segue
# avançando devagar depois dela, com a estimativa refeita, em vez de parar em 99%; Ctrl+C grava o estado "cancelado" e encerra limpo. O
# estado vai para um JSON na pasta da corrida (`progresso.json`), que o hub do pacote Q6 vai ler, e cada inferência concluída deixa uma linha
# em `progresso_medidas.jsonl` com o estimado e o medido por fase. A barra observa `cliente_ollama._post` por dentro de `observando()`: o
# corpo enviado ao Ollama e a resposta devolvida passam como estão (o teste compara o registro com e sem a barra). Quando a saída não é um
# terminal (o log do `.ps1`), só saem os marcos (começo, estimativa, fim), nunca o redesenho. `--taxas` extrai as taxas das corridas
# vigentes para `resultados_alvo/fase4/taxas_progresso.json`, `--erro` mede o erro da estimativa sobre os registros gravados, `--fumaca`
# lê as medidas de uma corrida real, `--demo` mostra a barra sem modelo.
# ! Motivo: plano aprovado da Pós-Fase 4, seção 3.5 e pacote Q4; levantamento §6.15.2 (base B). A inferência leva de 40 a 130 s nesta
# máquina, de 4 a 13 vezes o limite de 10 s em que Nielsen (1993) pede indicador de fração concluída com estimativa; Myers (1985) mediu
# que 86,1% dos sujeitos preferem o indicador, que distingue espera de travamento; Harrison et al. (2007) mediram que pausas perto do fim
# parecem mais lentas, por isso a barra nunca para antes de concluir; Apple HIG e Material pedem indicador determinado quando a duração é
# estimável e a troca de indeterminado para determinado sem mudar o formato. A chamada ao modelo não é em fluxo (stream), então não há
# token a token para corrigir a geração: a correção fica na estimativa pela taxa e pela mediana, com o teto como máximo (a ficha 59
# pergunta ao Eric se a chamada passa a stream); nenhum número é digitado: as taxas saem dos registros gravados, com a origem de cada um.
"""Barra de progresso da inferência (Pós-Fase 4, pacote Q4). Uso (em Programacao/AgenteCore/experimentos):
  RESULTADOS_DIR=resultados_alvo python progresso.py --taxas [--check]    # taxas por modelo e máquina -> resultados_alvo/fase4/taxas_progresso.{json,md}
  RESULTADOS_DIR=resultados_alvo python progresso.py --erro [--check]     # erro da estimativa sobre os registros gravados -> erro_progresso.{json,md}
  RESULTADOS_DIR=resultados_alvo python progresso.py --fumaca <pasta da corrida> [--check]   # medidas de uma corrida real -> fumaca_progresso.{json,md}
  python progresso.py --demo [--segundos 8]                               # a barra no terminal, com uma inferência de mentira

Fontes: NIELSEN, J. Response times: the 3 important limits (1993); MYERS, B. A. Percent-done progress indicators (Graphics Interface '85);
HARRISON, C. et al. Rethinking the progress bar (UIST 2007); APPLE, Human Interface Guidelines: Progress indicators (2023); MATERIAL
COMPONENTS ANDROID, Progress indicator; OLLAMA, API reference: generate a completion (campos prompt_eval_count, prompt_eval_duration,
eval_count, eval_duration). Todas no levantamento §6.15.2 do Memorial.
"""
from __future__ import annotations

import argparse
import contextlib
import datetime as dt
import json
import os
import statistics
import sys
import threading
import time
from collections import defaultdict
from pathlib import Path

import caminhos
import cliente_ollama as oll
import pre_fase4 as pf
import trilha as tr

VERSAO_DO_ESTADO = 1
LARGURA = 30                        # colunas da barra entre os colchetes, nas duas formas
INTERVALO_REDESENHO_S = 0.5         # Nielsen (1993): abaixo de 1 s o fluxo de atenção se mantém
INTERVALO_GRAVACAO_S = 1.0          # o arquivo de estado é regravado no máximo uma vez por segundo
FRACAO_NA_ESTIMATIVA = 0.9          # quando o decorrido iguala a estimativa a barra está em 90%; o resto avança devagar (Harrison et al., 2007)
CHARS_POR_TOKEN_SEM_TAXAS = 3.0     # só para dizer "~N tokens" quando não há taxas do modelo; a estimativa de tempo fica indeterminada
NOME_DO_ESTADO = "progresso.json"
NOME_DAS_MEDIDAS = "progresso_medidas.jsonl"
NOME_DAS_TAXAS = "taxas_progresso"
NOME_DO_ERRO = "erro_progresso"
NOME_DA_FUMACA = "fumaca_progresso"
PREFIXO = "tb_f4_progresso_"
LEITURAS_VIGENTES = ("tela_v4.json", "cenarios_v4.json", "ineditos.json")   # as três leituras vigentes da Fase 4 (decisões 99 e 100)
ESTADOS = ("indeterminado", "determinado", "concluido", "cancelado", "falhou")
FASES = ("prefill", "geracao")
FASE_EM_PALAVRAS = {"prefill": "lendo o caso (prefill)", "geracao": "escrevendo a resposta"}
RELATORIO_F4 = caminhos.AQUI.parent.parent.parent / "Documentacao" / "memorial" / "3-resultados-e-analises" / "fase-4-relatorio.md"
FONTES = ("Nielsen (1993): limites de 0,1 s, 1 s e 10 s; acima de 10 s, indicador de fração concluída com estimativa",
          "Myers (1985): 86,1% dos sujeitos preferem o indicador de fração concluída, que distingue espera de travamento",
          "Harrison et al. (2007): pausas perto do fim parecem mais lentas; a barra nunca para antes de concluir",
          "Apple HIG (2023) e Material Components: determinado quando a duração é estimável, trocando de indeterminado sem mudar o formato",
          "Ollama, API reference: prompt_eval_count, prompt_eval_duration, eval_count e eval_duration só chegam no fim da resposta")

_ROTULO: dict = {"atual": None}
sem_data = pf.sem_data


def agora() -> str:
    return dt.datetime.now().isoformat(timespec="seconds")


def _s(ns) -> float | None:
    """Nanossegundos do Ollama em segundos, com três casas."""
    return None if ns is None else round(ns / 1e9, 3)


def _fmt(v, casas: int = 1) -> str:
    """Número em português (vírgula decimal), ou "n/d"."""
    if v is None:
        return "n/d"
    return f"{v:.{casas}f}".replace(".", ",")


# ------------------------------------------------------------------ as taxas e a estimativa

def caminho_das_taxas() -> Path:
    return caminhos.RESULTADOS / "fase4" / f"{NOME_DAS_TAXAS}.json"


def carregar_taxas(caminho: Path | None = None) -> dict | None:
    caminho = caminho or caminho_das_taxas()
    return json.loads(caminho.read_text(encoding="utf-8")) if caminho.exists() else None


def taxas_do_modelo(taxas: dict | None, modelo: str | None) -> dict | None:
    """O bloco de taxas do modelo (`por_modelo[modelo]`), ou None quando o arquivo ou o modelo faltam."""
    if not taxas or not modelo:
        return None
    return (taxas.get("por_modelo") or {}).get(modelo)


def estimar(chars_prompt: int, teto: int | None, taxas: dict | None) -> dict | None:
    """A estimativa das duas fases para um prompt de `chars_prompt` caracteres: prefill pelos tokens estimados e pela taxa de prefill;
    geração pela mediana de tokens gerados e pela taxa de geração, com o teto como máximo. None sem taxas do modelo."""
    if not taxas:
        return None
    cpt = (taxas.get("chars_por_token") or {}).get("mediana")
    pre = (taxas.get("prefill_tokens_por_s") or {}).get("mediana")
    ger = (taxas.get("geracao_tokens_por_s") or {}).get("mediana")
    saida = (taxas.get("tokens_saida") or {}).get("mediana")
    if not (cpt and pre and ger and saida):
        return None
    tokens = round(chars_prompt / cpt)
    prefill = round(tokens / pre, 3)
    geracao = round(saida / ger, 3)
    maxima = round(teto / ger, 3) if teto else None
    return {"tokens_prompt": tokens, "prefill_s": prefill, "geracao_s": geracao, "geracao_maxima_s": maxima,
            "total_s": round(prefill + geracao, 3), "maximo_s": round(prefill + maxima, 3) if maxima is not None else None,
            "origem": {"tokens_prompt": f"{chars_prompt} caracteres do prompt / {cpt} caracteres por token (mediana das corridas gravadas)",
                       "prefill_s": f"{tokens} tokens / {pre} tokens por segundo (mediana do prefill das corridas gravadas)",
                       "geracao_s": f"{saida} tokens (mediana dos gerados nas corridas gravadas) / {ger} tokens por segundo (mediana da geração)",
                       "geracao_maxima_s": f"teto de {teto} tokens / {ger} tokens por segundo" if teto else "sem teto informado"}}


def fracao(decorrido_s: float, estimativa_s: float | None) -> float | None:
    """A fração da barra pelo relógio: linear até 90% quando o decorrido iguala a estimativa e, depois, 1 - 0,1 x estimativa / decorrido,
    que cresce sempre e nunca chega a 1 (Harrison et al., 2007: a barra não pode parar perto do fim). None sem estimativa."""
    if estimativa_s is None or estimativa_s <= 0:
        return None
    if decorrido_s <= 0:
        return 0.0
    if decorrido_s < estimativa_s:
        return round(FRACAO_NA_ESTIMATIVA * decorrido_s / estimativa_s, 4)
    return round(1 - (1 - FRACAO_NA_ESTIMATIVA) * estimativa_s / decorrido_s, 4)


def estimativa_refeita(decorrido_s: float, estimativa_s: float) -> float:
    """A estimativa do total depois que o decorrido passa dela: o decorrido dividido pela fração, que anda para a frente a cada tique."""
    if decorrido_s <= estimativa_s:
        return estimativa_s
    f = fracao(decorrido_s, estimativa_s)
    return round(decorrido_s / f, 3) if f else estimativa_s


def fase_pelo_relogio(decorrido_s: float, estimativa: dict | None) -> str:
    """A fase inferida pelo relógio contra a estimativa (a chamada não é em fluxo, então a fase não é observada): prefill até a estimativa
    do prefill, geração depois; sem estimativa, prefill."""
    if not estimativa or decorrido_s < estimativa.get("prefill_s", 0):
        return "prefill"
    return "geracao"


def anunciar(rotulo: str | None) -> None:
    """Quem lança a inferência diz o que ela é ("lex-10 · diagnóstico"); a próxima barra usa o rótulo e o esquece."""
    _ROTULO["atual"] = rotulo


def _rotulo_e_limpa() -> str | None:
    r = _ROTULO["atual"]
    _ROTULO["atual"] = None
    return r


# ------------------------------------------------------------------ a barra

def _e_terminal(saida) -> bool:
    try:
        return bool(saida.isatty())
    except (AttributeError, ValueError):
        return False


class Progresso:
    """Uma barra por inferência: `iniciar` (indeterminada ou determinada), `redesenhar` a cada tique, `concluir` com a resposta do Ollama,
    `cancelar` no Ctrl+C. Escreve em `saida` (terminal: a linha redesenhada; arquivo: só os marcos) e grava o estado em `arquivo_estado`."""

    def __init__(self, saida=None, arquivo_estado: Path | None = None, taxas: dict | None = None, modelo: str | None = None,
                 relogio=time.monotonic, terminal: bool | None = None, largura: int = LARGURA, medidas: Path | None = None) -> None:
        self.saida = sys.stdout if saida is None else saida
        self.arquivo_estado = Path(arquivo_estado) if arquivo_estado else None
        self.medidas = Path(medidas) if medidas else None
        self.taxas = taxas
        self.modelo = modelo
        self.relogio = relogio
        self.terminal = _e_terminal(self.saida) if terminal is None else terminal
        self.largura = largura
        self.inferencias_concluidas = 0
        self._cheio, self._vazio = self._simbolos()
        self._estado_nome: str | None = None
        self._ultimo_tamanho = 0
        self._ultima_gravacao: float | None = None
        self._gravado_em: str | None = None
        self.etapa = self.modelo_atual = None
        self.chars = self.teto = self.tokens_prompt = None
        self.estimativa = self.medido = self.tokens_gerados = None
        self.t0 = self._decorrido_final = None
        self.iniciado_em = None
        self.erro_texto = None

    def _simbolos(self) -> tuple[str, str]:
        codificacao = getattr(self.saida, "encoding", None) or "utf-8"
        try:
            "█░".encode(codificacao)
            return "█", "░"
        except (UnicodeEncodeError, LookupError):
            return "#", "."

    # --- ciclo de vida

    def iniciar(self, etapa: str, chars_prompt: int, teto: int | None, modelo: str | None = None) -> None:
        self.t0 = self.relogio()
        self._decorrido_final = None
        self.etapa = etapa
        self.chars = chars_prompt
        self.teto = teto
        self.modelo_atual = modelo or self.modelo
        self.estimativa = estimar(chars_prompt, teto, taxas_do_modelo(self.taxas, self.modelo_atual))
        self.tokens_prompt = self.estimativa["tokens_prompt"] if self.estimativa else round(chars_prompt / CHARS_POR_TOKEN_SEM_TAXAS)
        self.medido = None
        self.tokens_gerados = None
        self.erro_texto = None
        self._estado_nome = "determinado" if self.estimativa else "indeterminado"
        self.iniciado_em = agora()
        self._ultimo_tamanho = 0
        if self.terminal:
            self._escrever_linha(self.linha(), fim=False)
        else:
            self._marco(self._marco_de_inicio())
        self._gravar(forcar=True)

    def redesenhar(self) -> None:
        if self._estado_nome not in ("indeterminado", "determinado"):
            return
        if self.terminal:
            self._escrever_linha(self.linha(), fim=False)
        self._gravar()

    def concluir(self, resposta: dict) -> dict:
        self._decorrido_final = round(self.relogio() - self.t0, 3)
        self.medido = {"prefill_s": _s(resposta.get("prompt_eval_duration")), "geracao_s": _s(resposta.get("eval_duration")),
                       "carga_s": _s(resposta.get("load_duration")), "total_s": _s(resposta.get("total_duration")),
                       "tokens_entrada": resposta.get("prompt_eval_count"), "tokens_saida": resposta.get("eval_count"),
                       "tokens_em_cache": resposta.get("prompt_eval_cached_count"), "decorrido_s": self._decorrido_final}
        self.tokens_gerados = resposta.get("eval_count")
        self._estado_nome = "concluido"
        self.inferencias_concluidas += 1
        erro = None
        if self.estimativa:
            erro = {}
            for fase, real in (("prefill_s", self.medido["prefill_s"]), ("geracao_s", self.medido["geracao_s"])):
                erro[fase] = None if real is None else round(self.estimativa[fase] - real, 3)
            real_total = None if None in (self.medido["prefill_s"], self.medido["geracao_s"]) else self.medido["prefill_s"] + self.medido["geracao_s"]
            erro["total_s"] = None if real_total is None else round(self.estimativa["total_s"] - real_total, 3)
            erro["parede_s"] = round(self.estimativa["total_s"] - self._decorrido_final, 3)
        medida = {"etapa": self.etapa, "modelo": self.modelo_atual, "chars_prompt": self.chars, "teto_tokens": self.teto, "tokens_prompt_estimados": self.tokens_prompt,
                  "estimado": self.estimativa, "medido": self.medido, "erro": erro, "concluido_em": agora()}
        if self.terminal:
            self._escrever_linha(self.linha(), fim=True)
        else:
            self._marco(self._marco_de_fim())
        self._gravar(forcar=True)
        self._anotar_medida(medida)
        return medida

    def cancelar(self) -> None:
        self._decorrido_final = round(self.relogio() - self.t0, 3) if self.t0 is not None else 0.0
        self._estado_nome = "cancelado"
        texto = f"cancelada aos {_fmt(self._decorrido_final)} s (Ctrl+C)"
        if self.terminal:
            self._escrever_linha(f"{self._colchetes()} {texto} · {self.etapa}", fim=True)
        else:
            self._marco(f"progresso: {self.etapa} {texto}; estado gravado em {self.arquivo_estado}")
        self._gravar(forcar=True)

    def falhar(self, erro: BaseException) -> None:
        self._decorrido_final = round(self.relogio() - self.t0, 3) if self.t0 is not None else 0.0
        self._estado_nome = "falhou"
        self.erro_texto = f"{type(erro).__name__}: {erro}"
        texto = f"falhou aos {_fmt(self._decorrido_final)} s ({self.erro_texto})"
        if self.terminal:
            self._escrever_linha(f"{self._colchetes()} {texto} · {self.etapa}", fim=True)
        else:
            self._marco(f"progresso: {self.etapa} {texto}")
        self._gravar(forcar=True)

    # --- o que a barra diz

    def _decorrido(self) -> float:
        if self._decorrido_final is not None:
            return self._decorrido_final
        return round(self.relogio() - self.t0, 3) if self.t0 is not None else 0.0

    def estado(self) -> dict:
        decorrido = self._decorrido()
        total = self.estimativa["total_s"] if self.estimativa else None
        fr = fracao(decorrido, total)
        if self._estado_nome == "concluido":
            fr = 1.0
        fase = "geracao" if self._estado_nome == "concluido" else fase_pelo_relogio(decorrido, self.estimativa)
        dado = {"etapa": self.etapa, "modelo": self.modelo_atual, "estado": self._estado_nome, "fase": fase, "tokens_prompt": self.tokens_prompt,
                "chars_prompt": self.chars, "teto_tokens": self.teto, "tokens_gerados": self.tokens_gerados, "decorrido_s": decorrido,
                "estimativa_s": total, "estimativa_refeita_s": estimativa_refeita(decorrido, total) if total else None, "fracao": fr,
                "estimativa": self.estimativa, "medido": self.medido, "inferencias_concluidas": self.inferencias_concluidas,
                "iniciado_em": self.iniciado_em, "gravado_em": self._gravado_em or agora(), "versao": VERSAO_DO_ESTADO}
        if self.erro_texto:
            dado["erro"] = self.erro_texto
        return dado

    def _colchetes(self, fr: float | None = None, decorrido: float | None = None) -> str:
        """A forma do indicador: os mesmos colchetes e a mesma largura, determinada (preenche) ou indeterminada (um bloco que anda)."""
        if fr is not None:
            cheios = min(self.largura, int(fr * self.largura))
            return "[" + self._cheio * cheios + self._vazio * (self.largura - cheios) + "]"
        bloco = 3
        curso = 2 * (self.largura - bloco)
        passo = int((decorrido or 0.0) / INTERVALO_REDESENHO_S) % curso if curso else 0
        pos = passo if passo < self.largura - bloco else curso - passo
        return "[" + self._vazio * pos + self._cheio * bloco + self._vazio * (self.largura - bloco - pos) + "]"

    def linha(self) -> str:
        e = self.estado()
        decorrido = e["decorrido_s"]
        if e["estado"] == "concluido":
            m = self.medido or {}
            est = self.estimativa or {}
            partes = [f"{self._colchetes(1.0)} 100%", f"{_fmt(decorrido)} s" + (f" (estimado {_fmt(est.get('total_s'))} s)" if est else ""),
                      f"prefill {_fmt(m.get('prefill_s'))} s" + (f" (estimado {_fmt(est.get('prefill_s'))})" if est else ""),
                      f"resposta {_fmt(m.get('geracao_s'))} s" + (f" (estimado {_fmt(est.get('geracao_s'))})" if est else ""),
                      f"{m.get('tokens_saida')} tokens", str(self.etapa)]
            return " · ".join(partes)
        if e["estado"] == "indeterminado":
            return " · ".join([f"{self._colchetes(None, decorrido)} {_fmt(decorrido, 0)} s", f"lendo o caso, ~{self.tokens_prompt} tokens",
                               f"sem estimativa (sem taxas de {self.modelo_atual} nesta máquina)", str(self.etapa)])
        fr = e["fracao"] or 0.0
        pct = f"{int(fr * 100)}%"
        if decorrido <= e["estimativa_s"]:
            tempo = f"{_fmt(decorrido, 0)} s de ~{_fmt(e['estimativa_s'], 0)} s"
        else:
            tempo = f"{_fmt(decorrido, 0)} s · estimativa refeita: ~{_fmt(e['estimativa_refeita_s'], 0)} s"
        fase = f"lendo o caso, {self.tokens_prompt} tokens (prefill)" if e["fase"] == "prefill" else FASE_EM_PALAVRAS["geracao"]
        return " · ".join([f"{self._colchetes(fr)} {pct}", tempo, fase, str(self.etapa)])

    def _marco_de_inicio(self) -> str:
        if self.estimativa:
            est = self.estimativa
            texto = (f"estimativa {_fmt(est['total_s'])} s (lendo o caso {_fmt(est['prefill_s'])} s, resposta {_fmt(est['geracao_s'])} s"
                     + (f"; no máximo {_fmt(est['maximo_s'])} s pelo teto de {self.teto} tokens" if est.get("maximo_s") is not None else "") + ")")
        else:
            texto = f"sem estimativa (sem taxas de {self.modelo_atual} nesta máquina)"
        return f"progresso: {self.etapa} começou: {self.tokens_prompt} tokens no prompt (estimados pelos caracteres), teto {self.teto}; {texto}"

    def _marco_de_fim(self) -> str:
        m = self.medido or {}
        est = self.estimativa
        if est:
            comparacao = (f"estimado {_fmt(est['total_s'])} s: prefill {_fmt(m.get('prefill_s'))} s (estimado {_fmt(est['prefill_s'])} s), "
                          f"resposta {_fmt(m.get('geracao_s'))} s (estimado {_fmt(est['geracao_s'])} s)")
        else:
            comparacao = f"sem estimativa: prefill {_fmt(m.get('prefill_s'))} s, resposta {_fmt(m.get('geracao_s'))} s"
        return f"progresso: {self.etapa} concluída em {_fmt(self._decorrido())} s ({comparacao}); {m.get('tokens_saida')} tokens gerados"

    # --- saída e gravação

    def _escrever_linha(self, texto: str, fim: bool) -> None:
        preenchido = texto + " " * max(0, self._ultimo_tamanho - len(texto))
        self._ultimo_tamanho = len(texto)
        try:
            self.saida.write("\r" + preenchido + ("\n" if fim else ""))
            self.saida.flush()
        except (OSError, ValueError):
            pass

    def _marco(self, texto: str) -> None:
        try:
            self.saida.write(texto + "\n")
            self.saida.flush()
        except (OSError, ValueError):
            pass

    def _gravar(self, forcar: bool = False) -> None:
        """Grava o estado em JSON, no máximo uma vez por segundo (sempre nos marcos); escreve num arquivo ao lado e troca, para quem lê
        nunca pegar meio arquivo; uma falha de gravação não derruba a corrida."""
        if not self.arquivo_estado:
            return
        t = self.relogio()
        if not forcar and self._ultima_gravacao is not None and t - self._ultima_gravacao < INTERVALO_GRAVACAO_S:
            return
        self._ultima_gravacao = t
        self._gravado_em = agora()
        try:
            self.arquivo_estado.parent.mkdir(parents=True, exist_ok=True)
            temporario = self.arquivo_estado.with_name(self.arquivo_estado.name + ".tmp")
            temporario.write_text(json.dumps(self.estado(), ensure_ascii=False, indent=1), encoding="utf-8")
            os.replace(temporario, self.arquivo_estado)
        except OSError:
            pass

    def _anotar_medida(self, medida: dict) -> None:
        if not self.medidas:
            return
        try:
            self.medidas.parent.mkdir(parents=True, exist_ok=True)
            with self.medidas.open("a", encoding="utf-8") as f:
                f.write(json.dumps(medida, ensure_ascii=False) + "\n")
        except OSError:
            pass


def ler_estado(caminho: Path) -> dict:
    return json.loads(Path(caminho).read_text(encoding="utf-8"))


def _esperar(fio: threading.Thread, segundos: float) -> None:
    fio.join(segundos)


@contextlib.contextmanager
def observando(arquivo_estado: Path | None, modelo: str | None, taxas: dict | None = None, saida=None, terminal: bool | None = None,
               medidas: Path | None = None, esperar=None, relogio=time.monotonic):
    """Durante o bloco, toda chamada de cliente_ollama a /api/generate com prompt não vazio ganha a barra: a chamada roda num fio à
    parte, com o corpo e a resposta intocados, e o fio principal redesenha a barra a cada meio segundo e grava o estado. Ctrl+C grava
    "cancelado" e encerra com SystemExit (o Ollama termina a inferência em andamento no servidor; a descarga do modelo que o executor faz
    no fim espera por ela). A chamada de prompt vazio com que `descarregar` tira o modelo da memória passa sem barra. O `_post` encontrado
    na entrada é restaurado na saída, com erro ou sem."""
    barra = Progresso(saida=saida, arquivo_estado=arquivo_estado, taxas=taxas, modelo=modelo, relogio=relogio, terminal=terminal, medidas=medidas)
    original = oll._post
    esperar = esperar or _esperar

    def trocado(caminho: str, corpo: dict, timeout: int = 900) -> dict:
        if caminho != "/api/generate" or not corpo.get("prompt"):
            return original(caminho, corpo, timeout)
        etapa = _rotulo_e_limpa() or f"inferência {barra.inferencias_concluidas + 1}"
        barra.iniciar(etapa, chars_prompt=len(corpo["prompt"]), teto=(corpo.get("options") or {}).get("num_predict"), modelo=corpo.get("model") or modelo)
        caixa: dict = {}

        def alvo() -> None:
            try:
                caixa["r"] = original(caminho, corpo, timeout)
            except BaseException as e:  # noqa: BLE001 - o erro é devolvido ao fio principal, que o relança como se a chamada fosse direta
                caixa["erro"] = e

        fio = threading.Thread(target=alvo, name="progresso-inferencia", daemon=True)
        fio.start()
        try:
            while fio.is_alive():
                esperar(fio, INTERVALO_REDESENHO_S)
                if fio.is_alive():
                    barra.redesenhar()
        except KeyboardInterrupt:
            barra.cancelar()
            raise SystemExit(f"inferência cancelada pelo usuário (Ctrl+C) aos {_fmt(barra._decorrido())} s; estado gravado em {arquivo_estado}") from None
        if "erro" in caixa:
            barra.falhar(caixa["erro"])
            raise caixa["erro"]
        barra.concluir(caixa["r"])
        return caixa["r"]

    oll._post = trocado
    try:
        yield barra
    finally:
        oll._post = original


# ------------------------------------------------------------------ as taxas, extraídas das corridas vigentes

def _jsonl(arquivo: Path) -> list[dict]:
    saida = []
    for linha in arquivo.read_text(encoding="utf-8").splitlines():
        if linha.strip():
            with contextlib.suppress(json.JSONDecodeError):
                saida.append(json.loads(linha))
    return saida


def corridas_vigentes(raiz: Path | None = None) -> list[tuple[str, Path, str]]:
    """(corrida, pasta, modo) das três leituras vigentes, lidas de <raiz>/fase4/*.json (campo metadados.corrida), como os testes da fase."""
    raiz = raiz or caminhos.RESULTADOS
    saida = []
    for nome in LEITURAS_VIGENTES:
        arq = raiz / "fase4" / nome
        if not arq.exists():
            continue
        corrida = (json.loads(arq.read_text(encoding="utf-8")).get("metadados") or {}).get("corrida")
        pasta = raiz / corrida if corrida else None
        if not pasta or not (pasta / "condicoes_fase4.json").exists():
            continue
        modo = json.loads((pasta / "condicoes_fase4.json").read_text(encoding="utf-8")).get("modo")
        saida.append((corrida, pasta, modo))
    return saida


def _amostras_da_corrida(corrida: str, pasta: Path, modo: str) -> dict:
    """As amostras cruas de uma corrida, por modelo: taxas de cada registro de diagnóstico (diagnosticos__*.jsonl) e caracteres por token de
    cada par prompt/inferência da trilha v2. Devolve também os hashes do cabeçalho da trilha."""
    por_modelo: dict = defaultdict(lambda: {"prefill": [], "geracao": [], "saida": [], "entrada": [], "carga": [], "cpt": [],
                                            "maquinas": set(), "versoes": set(), "tetos": set(), "registros": 0, "inferencias": []})
    for arq in sorted(pasta.glob("*/diagnosticos__*.jsonl")):
        for r in _jsonl(arq):
            m = por_modelo[r["modelo"]]
            m["registros"] += 1
            if r.get("prefill_ms"):
                m["prefill"].append(r["tokens_entrada"] / (r["prefill_ms"] / 1000))
            if r.get("geracao_ms"):
                m["geracao"].append(r["tokens_saida"] / (r["geracao_ms"] / 1000))
            m["saida"].append(r["tokens_saida"])
            m["entrada"].append(r["tokens_entrada"])
            m["carga"].append(r.get("carga_ms", 0))
            m["maquinas"].add(r.get("maquina"))
            m["versoes"].add(r.get("versao_ollama"))
            m["tetos"].add(r.get("teto_tokens"))
    hashes = {}
    arq_trilha = pasta / f"trilha_{modo}.jsonl"
    if arq_trilha.exists():
        eventos = tr.ler(arq_trilha)
        cab = next((e for e in eventos if e.get("tipo") == "corrida"), None)
        modelo_da_corrida = (cab or {}).get("dados", {}).get("modelo")
        if cab:
            hashes = {"hash_prompt_fixo": cab["dados"].get("hash_prompt_fixo"), "hash_biblioteca": cab["dados"].get("hash_biblioteca")}
        por_seq = {e["seq"]: e for e in eventos}
        for e in eventos:
            if e.get("tipo") != "inferencia":
                continue
            pai = por_seq.get(e.get("pai"))
            if not pai or pai.get("tipo") != "prompt" or not e["dados"].get("tokens_entrada"):
                continue
            m = por_modelo[modelo_da_corrida]
            m["cpt"].append(pai["dados"]["chars"] / e["dados"]["tokens_entrada"])
            m["inferencias"].append({"corrida": corrida, "caso": e["trilha"].rsplit("/", 1)[-1], "chars": pai["dados"]["chars"],
                                     "tokens_entrada": e["dados"]["tokens_entrada"], "tokens_saida": e["dados"].get("tokens_saida"),
                                     "prefill_ms": e["dados"].get("prefill_ms"), "geracao_ms": e["dados"].get("geracao_ms"), "segundos": e["dados"].get("segundos")})
    return {"por_modelo": por_modelo, "hashes": hashes}


def _resumo(valores: list[float], origem: str, casas: int = 3) -> dict | None:
    if not valores:
        return None
    ordenados = sorted(valores)
    if len(ordenados) >= 2:
        cortes = statistics.quantiles(ordenados, n=10, method="inclusive")
        p10, p90 = cortes[0], cortes[-1]
    else:
        p10 = p90 = ordenados[0]
    return {"mediana": round(statistics.median(ordenados), casas), "p10": round(p10, casas), "p90": round(p90, casas),
            "min": round(ordenados[0], casas), "max": round(ordenados[-1], casas), "n": len(ordenados), "origem": origem}


ORIGENS = {"prefill": "tokens_entrada / (prefill_ms / 1000) de cada registro em <corrida>/<modelo>/diagnosticos__*.jsonl das corridas vigentes",
           "geracao": "tokens_saida / (geracao_ms / 1000) de cada registro em <corrida>/<modelo>/diagnosticos__*.jsonl das corridas vigentes",
           "saida": "tokens_saida de cada registro em diagnosticos__*.jsonl (o que o modelo escreveu de fato, abaixo do teto)",
           "entrada": "tokens_entrada de cada registro em diagnosticos__*.jsonl (a contagem real do prompt feita pelo Ollama)",
           "carga": "carga_ms de cada registro em diagnosticos__*.jsonl (quase zero com o modelo residente; segundos na primeira chamada)",
           "cpt": "chars do evento prompt / tokens_entrada do evento inferencia (mesmo pai) da trilha v2 de cada corrida"}


def _agregar(amostras: list[dict]) -> dict:
    """Junta as amostras de várias corridas num bloco por modelo (mediana, p10, p90, mínimo, máximo e n de cada medida, com a origem)."""
    juntas: dict = defaultdict(lambda: {"prefill": [], "geracao": [], "saida": [], "entrada": [], "carga": [], "cpt": [],
                                        "maquinas": set(), "versoes": set(), "tetos": set(), "registros": 0})
    for a in amostras:
        for modelo, m in a["por_modelo"].items():
            j = juntas[modelo]
            for chave in ("prefill", "geracao", "saida", "entrada", "carga", "cpt"):
                j[chave] += m[chave]
            j["maquinas"] |= m["maquinas"]
            j["versoes"] |= m["versoes"]
            j["tetos"] |= m["tetos"]
            j["registros"] += m["registros"]
    por_modelo = {}
    for modelo, j in sorted(juntas.items()):
        if not j["registros"]:
            continue
        por_modelo[modelo] = {"n": j["registros"], "maquinas": sorted(x for x in j["maquinas"] if x), "versoes_ollama": sorted(x for x in j["versoes"] if x),
                              "teto_tokens": sorted(x for x in j["tetos"] if x is not None),
                              "prefill_tokens_por_s": _resumo(j["prefill"], ORIGENS["prefill"]), "geracao_tokens_por_s": _resumo(j["geracao"], ORIGENS["geracao"]),
                              "tokens_saida": _resumo(j["saida"], ORIGENS["saida"], 1), "tokens_entrada": _resumo(j["entrada"], ORIGENS["entrada"], 1),
                              "chars_por_token": _resumo(j["cpt"], ORIGENS["cpt"]), "carga_ms": _resumo(j["carga"], ORIGENS["carga"], 1)}
    return por_modelo


def extrair_taxas(raiz: Path | None = None) -> dict:
    """As taxas por modelo e máquina, extraídas dos registros das corridas vigentes; nenhum número digitado."""
    corridas = corridas_vigentes(raiz)
    amostras = [_amostras_da_corrida(c, p, m) for c, p, m in corridas]
    hashes_prompt = sorted({a["hashes"].get("hash_prompt_fixo") for a in amostras if a["hashes"]})
    hashes_bib = sorted({a["hashes"].get("hash_biblioteca") for a in amostras if a["hashes"]})
    return {"metadados": {"gerado_em": agora(), "gerado_por": "progresso.py --taxas", "corridas": [c for c, _, _ in corridas], "leituras": list(LEITURAS_VIGENTES),
                          "hash_prompt_fixo": hashes_prompt[0] if len(hashes_prompt) == 1 else hashes_prompt,
                          "hash_biblioteca": hashes_bib[0] if len(hashes_bib) == 1 else hashes_bib,
                          "metodo": ("por modelo: mediana, percentis 10 e 90 (statistics.quantiles, inclusive), mínimo, máximo e n de cada medida; a estimativa da barra usa a "
                                     "mediana, e os percentis dizem o intervalo em que a taxa variou nesta máquina"),
                          "fontes": list(FONTES)},
            "por_modelo": _agregar(amostras)}


def render_taxas(dado: dict) -> str:
    cab = pf.cabecalho("Taxas do modelo para a barra de progresso (Pós-Fase 4, pacote Q4)", "progresso.py --taxas",
                       "diagnosticos__*.jsonl e trilha_*.jsonl das corridas vigentes", dado["metadados"]["gerado_em"][:10])
    linhas = cab + ["", ("A barra estima o prefill pelos tokens do prompt (caracteres divididos pelos caracteres por token) divididos pela taxa de prefill, e a geração pela "
                         "mediana de tokens gerados dividida pela taxa de geração, com o teto como máximo. Tudo vem dos registros das corridas "
                         + ", ".join(f"`{c}`" for c in dado["metadados"]["corridas"]) + "; a mediana entra na estimativa e os percentis 10 e 90 dizem o intervalo."), ""]
    for modelo, m in dado["por_modelo"].items():
        linhas += [f"## {modelo} ({m['n']} registros; máquina {', '.join(m['maquinas'])}; Ollama {', '.join(m['versoes_ollama'])}; teto {', '.join(str(t) for t in m['teto_tokens'])} tokens)", "",
                   f"<!-- tabela:{PREFIXO}taxas_{modelo.replace(':', '_').replace('.', '_')} -->",
                   "| Medida | Mediana | P10 | P90 | Mínimo | Máximo | n | De onde vem |", "|---|---|---|---|---|---|---|---|"]
        for chave, nome in (("prefill_tokens_por_s", "prefill (tokens por segundo)"), ("geracao_tokens_por_s", "geração (tokens por segundo)"),
                            ("tokens_entrada", "tokens do prompt"), ("tokens_saida", "tokens gerados"), ("chars_por_token", "caracteres por token do prompt"), ("carga_ms", "carga do modelo (ms)")):
            r = m.get(chave)
            if r:
                linhas.append(f"| {nome} | {_fmt(r['mediana'], 3)} | {_fmt(r['p10'], 3)} | {_fmt(r['p90'], 3)} | {_fmt(r['min'], 3)} | {_fmt(r['max'], 3)} | {r['n']} | {r['origem']} |")
        linhas += [f"<!-- /tabela:{PREFIXO}taxas_{modelo.replace(':', '_').replace('.', '_')} -->", ""]
    linhas += ["Fontes da barra: " + "; ".join(dado["metadados"]["fontes"]) + ".", ""]
    return "\n".join(linhas)


# ------------------------------------------------------------------ o erro da estimativa sobre os registros gravados

def _resumo_do_erro(pares: list[tuple[float, float]]) -> dict:
    """Pares (estimado, medido) de uma fase: mediana do erro com sinal, do erro absoluto (e o percentil 90), do erro relativo, e quantos
    ficaram subestimados (estimado menor que o medido)."""
    erros = [e - m for e, m in pares]
    absolutos = sorted(abs(x) for x in erros)
    relativos = [abs(e - m) / m for e, m in pares if m]
    p90 = statistics.quantiles(absolutos, n=10, method="inclusive")[-1] if len(absolutos) >= 2 else (absolutos[0] if absolutos else None)
    return {"n": len(pares), "erro_mediana_s": round(statistics.median(erros), 3) if erros else None,
            "erro_abs_mediana_s": round(statistics.median(absolutos), 3) if absolutos else None, "erro_abs_p90_s": round(p90, 3) if p90 is not None else None,
            "erro_relativo_mediana": round(statistics.median(relativos), 4) if relativos else None, "subestimados": sum(1 for x in erros if x < 0)}


def medir_erro(raiz: Path | None = None) -> dict:
    """O erro da estimativa, por fase, sobre cada inferência gravada nas corridas vigentes, de dois jeitos: com as taxas das outras corridas
    ("fora_da_corrida", a situação real da barra numa corrida nova) e com as taxas de todas, as do arquivo ("na_amostra")."""
    corridas = corridas_vigentes(raiz)
    amostras = {c: _amostras_da_corrida(c, p, m) for c, p, m in corridas}
    todas = _agregar(list(amostras.values()))
    por_modelo: dict = {}
    for corrida, a in amostras.items():
        fora = _agregar([x for c, x in amostras.items() if c != corrida])
        for modelo, m in a["por_modelo"].items():
            bloco = por_modelo.setdefault(modelo, {"n": 0, "modos": ["fora_da_corrida", "na_amostra"], "por_registro": [],
                                                   "pares": {modo: {f: [] for f in ("prefill_s", "geracao_s", "total_s", "parede_s")} for modo in ("fora_da_corrida", "na_amostra")}})
            for inf in m["inferencias"]:
                if not (inf.get("prefill_ms") and inf.get("geracao_ms")):
                    continue
                medido = {"prefill_s": round(inf["prefill_ms"] / 1000, 3), "geracao_s": round(inf["geracao_ms"] / 1000, 3),
                          "total_s": round((inf["prefill_ms"] + inf["geracao_ms"]) / 1000, 3), "parede_s": inf.get("segundos"),
                          "tokens_entrada": inf["tokens_entrada"], "tokens_saida": inf["tokens_saida"]}
                registro = {"corrida": corrida, "caso": inf["caso"], "chars": inf["chars"], "medido": medido, "estimado": {}, "erro": {}}
                for modo, taxas in (("fora_da_corrida", fora.get(modelo)), ("na_amostra", todas.get(modelo))):
                    est = estimar(inf["chars"], None, taxas)
                    if not est:
                        continue
                    registro["estimado"][modo] = {"tokens_prompt": est["tokens_prompt"], "prefill_s": est["prefill_s"], "geracao_s": est["geracao_s"], "total_s": est["total_s"]}
                    erro = {"prefill_s": round(est["prefill_s"] - medido["prefill_s"], 3), "geracao_s": round(est["geracao_s"] - medido["geracao_s"], 3),
                            "total_s": round(est["total_s"] - medido["total_s"], 3),
                            "parede_s": round(est["total_s"] - medido["parede_s"], 3) if medido["parede_s"] is not None else None,
                            "tokens_prompt": est["tokens_prompt"] - inf["tokens_entrada"]}
                    registro["erro"][modo] = erro
                    for fase in ("prefill_s", "geracao_s", "total_s"):
                        bloco["pares"][modo][fase].append((est[fase], medido[fase]))
                    if medido["parede_s"] is not None:
                        bloco["pares"][modo]["parede_s"].append((est["total_s"], medido["parede_s"]))
                bloco["por_registro"].append(registro)
                bloco["n"] += 1
    for modelo, bloco in por_modelo.items():
        pares = bloco.pop("pares")
        for modo in bloco["modos"]:
            bloco[modo] = {fase: _resumo_do_erro(lista) for fase, lista in pares[modo].items() if lista}
            tokens = [r["erro"][modo]["tokens_prompt"] for r in bloco["por_registro"] if modo in r["erro"]]
            bloco[modo]["tokens_prompt"] = {"n": len(tokens), "erro_mediana": round(statistics.median(tokens), 1) if tokens else None,
                                            "erro_abs_mediana": round(statistics.median(abs(t) for t in tokens), 1) if tokens else None,
                                            "erro_abs_max": max((abs(t) for t in tokens), default=None)}
    return {"metadados": {"gerado_em": agora(), "gerado_por": "progresso.py --erro", "corridas": list(amostras), "taxas_de": f"{NOME_DAS_TAXAS}.json",
                          "metodo": ("cada inferência gravada é estimada pelos caracteres do prompt (evento prompt da trilha) e comparada com prefill_ms e geracao_ms do evento "
                                     "inferencia; fora_da_corrida usa as taxas das outras duas corridas (o que a barra vê numa corrida nova), na_amostra usa as taxas de "
                                     "todas, as de taxas_progresso.json; erro = estimado menos medido (negativo quer dizer que a barra acabaria antes do real); "
                                     "total_s é prefill mais geração, parede_s é o tempo de relógio da chamada, que inclui a carga do modelo")},
            "por_modelo": por_modelo}


def render_erro(dado: dict) -> str:
    cab = pf.cabecalho("Erro da estimativa da barra de progresso sobre os registros gravados (Pós-Fase 4, pacote Q4)", "progresso.py --erro",
                       "trilha_*.jsonl das corridas vigentes e taxas_progresso.json", dado["metadados"]["gerado_em"][:10])
    linhas = cab + ["", dado["metadados"]["metodo"] + ".", ""]
    for modelo, b in dado["por_modelo"].items():
        for modo in b["modos"]:
            rotulo = "taxas das outras corridas (o que a barra vê numa corrida nova)" if modo == "fora_da_corrida" else "taxas de todas as corridas (as do arquivo)"
            nome = f"{PREFIXO}erro_{modo}_{modelo.replace(':', '_').replace('.', '_')}"
            linhas += [f"## {modelo}, {rotulo}: {b['n']} inferências", "", f"<!-- tabela:{nome} -->",
                       "| Fase | n | Erro mediano (s) | Erro absoluto mediano (s) | Erro absoluto P90 (s) | Erro relativo mediano | Subestimadas |", "|---|---|---|---|---|---|---|"]
            for fase, titulo in (("prefill_s", "prefill"), ("geracao_s", "geração"), ("total_s", "prefill mais geração"), ("parede_s", "tempo de relógio da chamada")):
                r = b[modo].get(fase)
                if r:
                    linhas.append(f"| {titulo} | {r['n']} | {_fmt(r['erro_mediana_s'])} | {_fmt(r['erro_abs_mediana_s'])} | {_fmt(r['erro_abs_p90_s'])} | "
                                  f"{_fmt(r['erro_relativo_mediana'] * 100 if r['erro_relativo_mediana'] is not None else None)}% | {r['subestimados']} de {r['n']} |")
            t = b[modo].get("tokens_prompt") or {}
            linhas += [f"<!-- /tabela:{nome} -->", "",
                       (f"Tokens do prompt estimados pelos caracteres: erro mediano de {_fmt(t.get('erro_mediana'))} tokens (absoluto mediano {_fmt(t.get('erro_abs_mediana'))}, "
                        f"máximo {t.get('erro_abs_max')}) em {t.get('n')} prompts."), ""]
    return "\n".join(linhas)


# ------------------------------------------------------------------ a fumaça real: as medidas de uma corrida

def resumir_fumaca(pasta: Path) -> dict:
    """As medidas gravadas por uma corrida real (progresso_medidas.jsonl): estimado contra medido por fase, inferência a inferência."""
    pasta = Path(pasta)
    medidas = _jsonl(pasta / NOME_DAS_MEDIDAS) if (pasta / NOME_DAS_MEDIDAS).exists() else []
    com_estimativa = [m for m in medidas if m.get("estimado") and m.get("erro")]
    por_fase = {}
    for fase in ("prefill_s", "geracao_s", "total_s", "parede_s"):
        pares = []
        for m in com_estimativa:
            est = m["estimado"]["total_s"] if fase in ("total_s", "parede_s") else m["estimado"][fase]
            if fase == "parede_s":
                real = m["medido"].get("decorrido_s")
            elif fase == "total_s":
                real = None if None in (m["medido"].get("prefill_s"), m["medido"].get("geracao_s")) else m["medido"]["prefill_s"] + m["medido"]["geracao_s"]
            else:
                real = m["medido"].get(fase)
            if real is not None:
                pares.append((est, real))
        if pares:
            por_fase[fase] = _resumo_do_erro(pares)
    condicoes = pasta / "condicoes_fase4.json"
    cond = json.loads(condicoes.read_text(encoding="utf-8")) if condicoes.exists() else {}
    return {"metadados": {"gerado_em": agora(), "gerado_por": "progresso.py --fumaca", "corrida": pasta.name, "modo": cond.get("modo"), "modelo": cond.get("modelo"),
                          "versao_ollama": cond.get("versao_ollama"), "criado_em": cond.get("criado_em")},
            "inferencias": len(medidas), "com_estimativa": len(com_estimativa), "por_fase": por_fase, "medidas": medidas}


def render_fumaca(dado: dict) -> str:
    md = dado["metadados"]
    cab = pf.cabecalho("Fumaça real da barra de progresso: estimado contra medido (Pós-Fase 4, pacote Q4)", "progresso.py --fumaca",
                       f"{NOME_DAS_MEDIDAS} da corrida {md['corrida']}", md["gerado_em"][:10])
    linhas = cab + ["", (f"Corrida `{md['corrida']}` (modo {md.get('modo')}, modelo {md.get('modelo')}, Ollama {md.get('versao_ollama')}, criada em {md.get('criado_em')}): "
                         f"{dado['inferencias']} inferência(s), {dado['com_estimativa']} com estimativa."), "",
                    f"<!-- tabela:{PREFIXO}fumaca -->", "| Fase | n | Erro mediano (s) | Erro absoluto mediano (s) | Erro absoluto P90 (s) | Erro relativo mediano | Subestimadas |", "|---|---|---|---|---|---|---|"]
    for fase, titulo in (("prefill_s", "prefill"), ("geracao_s", "geração"), ("total_s", "prefill mais geração"), ("parede_s", "tempo de relógio da chamada")):
        r = dado["por_fase"].get(fase)
        if r:
            linhas.append(f"| {titulo} | {r['n']} | {_fmt(r['erro_mediana_s'])} | {_fmt(r['erro_abs_mediana_s'])} | {_fmt(r['erro_abs_p90_s'])} | "
                          f"{_fmt(r['erro_relativo_mediana'] * 100 if r['erro_relativo_mediana'] is not None else None)}% | {r['subestimados']} de {r['n']} |")
    linhas += [f"<!-- /tabela:{PREFIXO}fumaca -->", "", f"<!-- tabela:{PREFIXO}fumaca_inferencias -->",
               "| Etapa | Tokens do prompt (estimados / reais) | Prefill estimado / medido (s) | Resposta estimada / medida (s) | Total estimado / medido (s) | Tempo de relógio (s) | Tokens gerados |",
               "|---|---|---|---|---|---|---|"]
    for m in dado["medidas"]:
        est, med = m.get("estimado") or {}, m.get("medido") or {}
        total_medido = None if None in (med.get("prefill_s"), med.get("geracao_s")) else med["prefill_s"] + med["geracao_s"]
        linhas.append(f"| {m.get('etapa')} | {m.get('tokens_prompt_estimados')} / {med.get('tokens_entrada')} | {_fmt(est.get('prefill_s'))} / {_fmt(med.get('prefill_s'))} | "
                      f"{_fmt(est.get('geracao_s'))} / {_fmt(med.get('geracao_s'))} | {_fmt(est.get('total_s'))} / {_fmt(total_medido)} | {_fmt(med.get('decorrido_s'))} | {med.get('tokens_saida')} |")
    linhas += [f"<!-- /tabela:{PREFIXO}fumaca_inferencias -->", ""]
    return "\n".join(linhas)


# ------------------------------------------------------------------ a demonstração sem modelo

def demonstrar(segundos: float = 8.0, saida=None) -> None:
    """Mostra a barra com uma inferência de mentira que dura `segundos`, usando as taxas gravadas se existirem."""
    taxas = carregar_taxas()
    modelo = next(iter((taxas or {}).get("por_modelo") or {}), "modelo-de-demonstracao")
    original = oll._post

    def post_de_mentira(caminho: str, corpo: dict, timeout: int = 900) -> dict:
        time.sleep(segundos)
        return {"response": "CAUSA_RAIZ: demonstracao", "done_reason": "stop", "prompt_eval_count": 1200, "eval_count": 60, "load_duration": 30_000_000,
                "prompt_eval_duration": int(segundos * 0.8 * 1e9), "eval_duration": int(segundos * 0.2 * 1e9), "total_duration": int(segundos * 1e9)}

    oll._post = post_de_mentira
    try:
        with observando(arquivo_estado=None, modelo=modelo, taxas=taxas, saida=saida):
            anunciar("demonstração · uma inferência de mentira")
            oll.gerar(modelo, "x" * 3750, 600)
    finally:
        oll._post = original


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--taxas", action="store_true", help=f"extrai as taxas das corridas vigentes para resultados_alvo/fase4/{NOME_DAS_TAXAS}.{{json,md}}")
    ap.add_argument("--erro", action="store_true", help=f"mede o erro da estimativa sobre os registros gravados para {NOME_DO_ERRO}.{{json,md}}")
    ap.add_argument("--fumaca", default=None, help=f"pasta de uma corrida real: resume {NOME_DAS_MEDIDAS} em {NOME_DA_FUMACA}.{{json,md}}")
    ap.add_argument("--demo", action="store_true", help="mostra a barra no terminal com uma inferência de mentira")
    ap.add_argument("--segundos", type=float, default=8.0, help="duração da inferência de mentira do --demo")
    ap.add_argument("--check", action="store_true", help="regera e compara com o que está gravado, sem gravar")
    args = ap.parse_args(argv)
    pasta = caminhos.RESULTADOS / "fase4"
    if args.demo:
        demonstrar(args.segundos)
        return 0
    codigo = 0
    if args.taxas:
        dado = extrair_taxas()
        codigo = max(codigo, pf.fechar(NOME_DAS_TAXAS, dado, render_taxas(dado), PREFIXO + "taxas", check=args.check, pasta=pasta, doc=RELATORIO_F4))
    if args.erro:
        dado = medir_erro()
        codigo = max(codigo, pf.fechar(NOME_DO_ERRO, dado, render_erro(dado), PREFIXO + "erro", check=args.check, pasta=pasta, doc=RELATORIO_F4))
    if args.fumaca:
        dado = resumir_fumaca(Path(args.fumaca))
        codigo = max(codigo, pf.fechar(NOME_DA_FUMACA, dado, render_fumaca(dado), PREFIXO + "fumaca", check=args.check, pasta=pasta, doc=RELATORIO_F4))
    if not (args.taxas or args.erro or args.fumaca):
        ap.print_help()
        return 2
    return codigo


if __name__ == "__main__":
    sys.exit(main())
