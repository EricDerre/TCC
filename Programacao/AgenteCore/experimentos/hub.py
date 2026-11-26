#!/usr/bin/env python3
# ! Alteração de IA - Revisar: arquivo novo (25/11/2026, Pós-Fase 4, pacote Q6): o servidor do hub central. Sobe o `http.server` da biblioteca
# padrão só em 127.0.0.1 e atende seis endereços: a página (`/`), o estilo (`/hub.css`), o programa (`/hub.js`), a lista (`/api/indice`), o
# caso (`/api/caso?tid=...`) e a gravação da revisão (`POST /api/revisao`). `Hub` junta o acervo das corridas (`hub_dados.Acervo`) com as
# revisões (`hub_revisao.Revisoes`); `--conferir` monta todos os casos sem subir servidor e diz quantos são.
# ! Motivo: plano aprovado da Pós-Fase 4, seção 3.6 ("uma aplicação local, servida por http.server da biblioteca padrão"), e ficha 97 (decisão
# 157). O servidor grava em disco, então ele: só escuta na própria máquina; não serve arquivo nenhum do disco (cada endereço é uma função, e o
# que não é um dos seis recebe 404); só aceita gravação em JSON vinda do próprio endereço (um formulário de outro site aberto no mesmo
# navegador não consegue mandar `application/json` sem pedir licença, e o cabeçalho de origem é conferido); grava tudo como analista (o agente
# não escreve pela página) e põe ele mesmo a iteração do caso no evento, para o navegador não poder dizer que revisou outra.
# ! Alteração de IA - Revisar: (25/11/2026, etapa 3) o servidor passou a atender também o trace de um caso (`/api/trace?tid=...`), o estado da
# corrida em andamento (`/api/ao-vivo`) e a execução dos cenários (`GET` e `POST /api/execucao`); são nove endereços, e o resto continua 404.
# ! Motivo: decisão 93 (trace na falha e "Cérebro ao vivo") e plano, seção 3.6, item 7 (os botões). O trace é o único arquivo que o servidor
# entrega do disco, e o caminho dele é montado pelo acervo a partir da trilha achada, nunca do texto do pedido.
# ! Alteração de IA - Revisar: (25/11/2026, ficha 109, decisão 170) o hub passa a ser a central aberta pelo `Cobaia.exe`. Entram: a opção
# `--pelo-exe` (o `run.py` a passa ao subir o hub junto com o site e a API); dois endereços novos, `/api/central` (o estado do site, da API,
# do Ollama e do próprio hub, e os atalhos) e `/api/metricas` (as métricas por corrida e o resultado da Fase 5, de `hub_dados.metricas`); e,
# com `--pelo-exe`, o botão de rodar os cenários liberado, chamando o `executar_fase4.py` direto com `--cobaias-no-ar`, depois de conferir
# que o Ollama responde. São onze endereços, e o resto continua 404.
# ! Motivo: o Eric pediu que o hub seja a central de tudo, aberta quando o `.exe` roda, de onde se rodam os testes e se veem as métricas.
# Quem dá dois cliques no `.exe` não passa `--permitir-execucao`, e o `rodar_fase4.ps1` não serve a esse caminho: ele roda antes as baterias
# com banco, confere a memória livre e sobe e derruba o site, a API e o banco, que o `.exe` já deixou no ar. `python hub.py` sozinho continua
# só mostrando o comando para copiar (decisão 157).
"""O hub central (Pós-Fase 4, pacote Q6). Uso (em Programacao/AgenteCore/experimentos):
  python hub.py                       # sobe em http://127.0.0.1:8765 com as corridas 18d, 21d, 24 e 28b e abre o navegador
  python hub.py --porta 8770 --sem-abrir
  python hub.py --corridas fase5_agente_b,fase4_ineditos
  python hub.py --conferir            # monta todos os casos sem subir servidor e diz quantos são
  python hub.py --pelo-exe            # como o Cobaia.exe o abre: o site e a API já estão no ar, e o botão de rodar os cenários fica liberado
As revisões ficam em resultados_alvo/hub/revisoes/<caso>.jsonl. Nada é escrito nas pastas das corridas.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import contextlib
import datetime as dt
import json
import os
import re
import shutil
import socket
import subprocess
import sys
import threading
import time
import urllib.parse
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import etapas_ao_vivo as ea
import gerar_relatorio_raciocinio as grr
import hub_dados as hd
import hub_pagina as hp
import hub_revisao as hr
import pre_fase4 as pf

EXP = Path(__file__).resolve().parent
RESULTADOS = EXP / "resultados_alvo"
PASTA_DAS_REVISOES = RESULTADOS / "hub" / "revisoes"
PORTA_PADRAO = 8765
ENDERECO = "127.0.0.1"
NOMES_LOCAIS = ("127.0.0.1", "localhost")
LIMITE_DO_CORPO = 1_000_000
POLITICA = "default-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'; form-action 'none'"
BLOCOS_DO_RELATORIO = tuple(f"b{n}-{hp.slug(nome)}" for n, nome in enumerate(grr.CAMPOS_55 + grr.SECOES_MANTIDAS_V3, start=1))
CAMPOS_DO_RASCUNHO = ("texto", "ancora", "rotulo", "bloqueante", "conversa")
# ! Alteração de IA - Revisar: (26/11/2026) o hub passa a servir o painel do projeto desta máquina em `/painel` (o arquivo que
# `ferramentas/gerar_dashboard.py` grava) e deixa de apontar para o painel publicado no claude.ai. `estado_do_painel` diz se o arquivo existe,
# quando foi gerado e se alguma das três fontes que mais mudam (as fichas, o roadmap e as decisões) foi alterada depois dele.
# ! Motivo: o Eric aprovou o molde do hub e pediu que "Abrir o painel do projeto" abra o HTML local, e que esse local esteja em dia. O painel
# traz script e estilo embutidos e carrega a biblioteca de gráficos e as fontes de fora, o que as regras da página do hub proíbem; por isso ele
# sai com regras próprias (`POLITICA_DO_PAINEL`), numa caixa separada (`sandbox`, sem `allow-same-origin`): o que roda dentro do painel não lê nem
# grava nada do que o hub serve, e um pedido de gravação vindo dele é recusado pela conferência de origem. O aviso de atraso compara a hora dos
# arquivos, e não o conteúdo: é um lembrete para regerar; a conferência exata continua sendo `python ferramentas/gerar_dashboard.py --check`.
# ! Alteração de IA - Revisar: (26/11/2026, ficha 116, decisão 178) nota acrescentada, sem mudar as regras: desde a decisão 178 a biblioteca de
# gráficos vai embutida no painel, e o painel gerado no repositório não pede mais nada a `cdn.jsdelivr.net`.
# ! Motivo: o comentário acima diz que o painel carrega a biblioteca de fora, o que deixou de valer para o painel gerado aqui. O endereço continua
# permitido em `POLITICA_DO_PAINEL` só para o painel gerado numa cópia sem `ferramentas/terceiros/chart.umd.js`, caso em que o gerador volta a
# pedir a biblioteca à internet; tirar o endereço faria esse painel abrir sem gráficos mesmo com internet.
RAIZ_DO_REPOSITORIO = EXP.parent.parent.parent
PAINEL_LOCAL = RAIZ_DO_REPOSITORIO / "Documentacao" / "dashboard" / "painel-do-projeto.html"
FONTES_DO_PAINEL = (RAIZ_DO_REPOSITORIO / "Documentacao" / "memorial" / "pendencias.md", RAIZ_DO_REPOSITORIO / "Documentacao" / "memorial" / "roadmap.md",
                    RAIZ_DO_REPOSITORIO / "Documentacao" / "memorial" / "1-decisoes-e-historico" / "decisoes.md")
POLITICA_DO_PAINEL = ("default-src 'none'; script-src 'unsafe-inline' https://cdn.jsdelivr.net; style-src 'unsafe-inline' https://fonts.googleapis.com; "
                      "font-src https://fonts.gstatic.com data:; img-src data:; connect-src 'none'; object-src 'none'; base-uri 'none'; form-action 'none'; "
                      "frame-ancestors 'none'; sandbox allow-scripts allow-popups allow-popups-to-escape-sandbox")


def estado_do_painel(painel: Path, fontes=()) -> dict:
    """Se o painel local existe, quando foi gerado e se alguma fonte foi alterada depois dele (pela hora dos arquivos)."""
    try:
        gerado = painel.stat().st_mtime
    except OSError:
        return {"url": "/painel", "existe": False, "gerado_em": None, "atrasado": False, "fonte_mais_nova": None}
    mais_nova = None
    for fonte in fontes:
        try:
            alterada = fonte.stat().st_mtime
        except OSError:
            continue
        if alterada > gerado and (mais_nova is None or alterada > mais_nova[0]):
            mais_nova = (alterada, fonte.name)
    return {"url": "/painel", "existe": True, "gerado_em": dt.datetime.fromtimestamp(gerado).isoformat(timespec="seconds"), "atrasado": mais_nova is not None,
            "fonte_mais_nova": mais_nova[1] if mais_nova else None}


class Recusa(Exception):
    """Um pedido que o servidor recusa, com o código HTTP da resposta."""

    def __init__(self, codigo: int, mensagem: str) -> None:
        super().__init__(mensagem)
        self.codigo = codigo


def opcoes() -> dict:
    """As listas fechadas que a página mostra nos seletores, lidas de `hub_revisao` (nenhuma é digitada na página)."""
    pares = lambda d: [[k, v] for k, v in d.items()]
    return {"vereditos": pares(hr.VEREDITOS), "estados_da_conversa": pares(hr.ESTADOS_DA_CONVERSA), "severidades": list(hr.SEVERIDADES),
            "prioridades": list(hr.PRIORIDADES), "estados_55": list(hr.ESTADOS_55), "rotulos": pares(hr.ROTULOS), "desfechos": pares(hr.DESFECHOS),
            "causas": list(hr.CAUSAS)}


# ! Alteração de IA - Revisar: (25/11/2026, pacote Q6, etapa 3) `Execucao` é o botão "rodar os cenários" do hub: monta o comando do lançador
# (`rodar_fase4.ps1 -Modo cenarios -Saida hub_<data>_<hora> -Repeticoes N -LeituraNaPasta`), lança-o num processo à parte quando o hub foi
# aberto com `--permitir-execucao`, guarda a saída dele em `<resultados>/hub/execucoes/<saida>.log`, diz se terminou e com que código, e
# para a corrida a pedido. Sem a permissão, só mostra o comando, para o analista copiar e rodar na janela dele.
# ! Motivo: plano, seção 3.6, item 7 (os botões), e ficha 97 (decisão 157: o botão só dispara com a opção). A corrida com o modelo pede a
# memória livre da máquina e não roda de dentro do aplicativo Claude (decisão 112); por isso o padrão é mostrar o comando. O nome da pasta
# de saída é dado aqui, pela hora, e as repetições são um inteiro de 1 a 5: nada do que o navegador manda entra na linha de comando como
# texto. É uma corrida por vez, porque o Ollama carrega um modelo de cada vez e as duas disputariam a mesma memória. `-LeituraNaPasta` faz
# o avaliador gravar na pasta da corrida, e não em `resultados_alvo/fase4`, onde estão as leituras oficiais.
REPETICOES_PERMITIDAS = (1, 2, 3, 4, 5)
TAMANHO_DO_LOG = 4000


# ! Alteração de IA - Revisar: (25/11/2026, Pós-Fase 4, pacote Q7) o comando da corrida ganhou `-Selecao git` e `-Desde <commit>`, e `opcoes_da_corrida`
# confere as três opções que a página pode mandar (repetições, seleção e commit de partida) antes de qualquer uma virar parte da linha de comando.
# ! Motivo: plano, seção 3.7 (a seleção pelo Git ligada ao hub). O `desde` vem digitado pelo analista e entra numa linha de comando: só passa se
# for o identificador de um commit (de 7 a 40 caracteres hexadecimais), e só junto com a seleção pelo Git.
SELECOES = ("todos", "git")
_COMMIT = re.compile(r"^[0-9a-fA-F]{7,40}$")


def opcoes_da_corrida(repeticoes=1, selecao="todos", desde=None) -> dict:
    if isinstance(repeticoes, bool) or not isinstance(repeticoes, int) or repeticoes not in REPETICOES_PERMITIDAS:
        raise ValueError(f"repeticoes: esperava um inteiro entre {REPETICOES_PERMITIDAS[0]} e {REPETICOES_PERMITIDAS[-1]}")
    selecao = selecao or "todos"
    if selecao not in SELECOES:
        raise ValueError(f"selecao: {selecao!r} não é uma de {SELECOES}")
    desde = desde or None
    if desde is not None and (not isinstance(desde, str) or not _COMMIT.match(desde)):
        raise ValueError("desde: esperava o identificador de um commit (de 7 a 40 caracteres hexadecimais)")
    if desde is not None and selecao != "git":
        raise ValueError("desde: o commit de partida só vale com a seleção pelo Git")
    return {"repeticoes": repeticoes, "selecao": selecao, "desde": desde}


def comando_padrao(saida: str, opcoes: dict) -> list[str]:
    comando = ["powershell", "-ExecutionPolicy", "Bypass", "-File", "rodar_fase4.ps1", "-Modo", "cenarios", "-Saida", saida,
               "-Repeticoes", str(opcoes["repeticoes"]), "-LeituraNaPasta"]
    if opcoes.get("selecao") == "git":
        comando += ["-Selecao", "git"]
        if opcoes.get("desde"):
            comando += ["-Desde", opcoes["desde"]]
    return comando


# ! Alteração de IA - Revisar: (25/11/2026, ficha 109, decisão 170) o que a corrida lançada pelo hub aberto pelo `Cobaia.exe` usa:
# `comando_direto` (o `executar_fase4.py` chamado pelo mesmo Python que roda o hub, no modo `cenarios`, com `--cobaias-no-ar`),
# `pasta_dos_resultados` (o valor de `RESULTADOS_DIR` que a corrida recebe), `porta_responde` (a sonda dos serviços) e
# `garantir_ollama_no_ar` (inicia o servidor do Ollama se a porta 11434 não responde e espera até 30 s).
# ! Motivo: o `.exe` já deixou o site (8080), a API (8000) e o banco no ar, e o `rodar_fase4.ps1` subiria tudo de novo nas mesmas portas e
# desligaria o banco no fim. `--casos 10` deixa a corrida marcada como parcial nas condições gravadas, como a corrida curta do pacote Q7:
# ela é uso do produto, não medida do TCC, e não pode ser confundida com uma noite completa. O Ollama é conferido aqui porque o lançador
# `.ps1`, que fazia essa conferência, não participa deste caminho; sem ele no ar a corrida morreria no primeiro diagnóstico, e a página só
# mostraria o fim do log. A sonda só abre e fecha a conexão: não faz pedido nenhum ao site, à API ou ao modelo.
PORTA_DO_SITE, PORTA_DA_API, PORTA_DO_OLLAMA = 8080, 8000, 11434
ESPERA_DO_OLLAMA_S = 30
CENARIOS_DA_CORRIDA_DO_HUB = 10


def comando_direto(saida: str, opcoes: dict, python: str | None = None) -> list[str]:
    comando = [python or sys.executable, "executar_fase4.py", "--modo", "cenarios", "--saida", saida, "--casos", str(CENARIOS_DA_CORRIDA_DO_HUB),
               "--repeticoes", str(opcoes["repeticoes"]), "--cobaias-no-ar", "--etapas-ao-vivo"]      # a hora de cada etapa, só nas corridas do botão (decisão 176)
    if opcoes.get("selecao") == "git":
        comando += ["--selecao", "git"]
        if opcoes.get("desde"):
            comando += ["--desde", opcoes["desde"]]
    return comando


def pasta_dos_resultados(raiz: Path) -> str:
    """O `RESULTADOS_DIR` da corrida: o nome da pasta quando ela fica em `experimentos/` (como o `rodar_fase4.ps1` manda), ou o caminho inteiro."""
    raiz = Path(raiz)
    return raiz.name if raiz.resolve().parent == EXP else str(raiz)


def porta_responde(porta: int, espera_s: float = 0.5) -> bool:
    """Diz se alguma coisa aceita conexão nesta porta desta máquina."""
    for nome in ("127.0.0.1", "::1"):
        try:
            with socket.create_connection((nome, porta), timeout=espera_s):
                return True
        except OSError:
            continue
    return False


def _achar_ollama() -> str | None:
    """O programa do Ollama: o do PATH, ou o que o instalador do projeto sabe achar (`_env_common.find_ollama`, na raiz do repositório)."""
    achado = shutil.which("ollama")
    if achado:
        return achado
    raiz = str(EXP.parent.parent.parent)
    if raiz not in sys.path:
        sys.path.append(raiz)
    try:
        import _env_common
        return _env_common.find_ollama()
    except Exception:  # noqa: BLE001 - sem o módulo do instalador (ou com ele quebrado), o hub só diz que não achou o Ollama
        return None


def _iniciar_ollama(programa: str) -> None:
    escondido = {"creationflags": subprocess.CREATE_NO_WINDOW} if os.name == "nt" else {"start_new_session": True}
    subprocess.Popen([programa, "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL, **escondido)


def garantir_ollama_no_ar(espera_s: float = ESPERA_DO_OLLAMA_S, sonda=porta_responde, achar=_achar_ollama, lancar=_iniciar_ollama, pausa_s: float = 0.5) -> str | None:
    """Deixa o Ollama no ar antes da corrida: devolve None quando ele responde, ou a frase que a página mostra quando não deu."""
    if sonda(PORTA_DO_OLLAMA):
        return None
    programa = achar()
    if not programa:
        return "o Ollama não foi encontrado nesta máquina: rode o instalador (o Cobaia.exe instala o Ollama e o modelo) e tente de novo"
    try:
        lancar(programa)
    except OSError as e:
        return f"o Ollama não pôde ser iniciado ({e}): abra o Ollama e tente de novo"
    limite = time.monotonic() + espera_s
    while time.monotonic() < limite:
        if sonda(PORTA_DO_OLLAMA):
            return None
        time.sleep(pausa_s)
    return f"o Ollama não respondeu em {espera_s:g} s depois de iniciado: abra o Ollama e tente de novo"


class Execucao:
    """A corrida de cenários lançada pelo hub: uma por vez, só com permissão."""

    # ! Alteração de IA - Revisar: (25/11/2026, ficha 109, decisão 170) `pelo_exe` libera o botão sem `--permitir-execucao`, troca o comando
    # padrão pelo `comando_direto` e faz `rodar` conferir o Ollama (`garantir_ollama`, trocável nos testes) antes de lançar; a corrida recebe
    # `RESULTADOS_DIR` e `PYTHONUNBUFFERED` no ambiente, como o `rodar_fase4.ps1` dava.
    # ! Motivo: é o caminho de quem abriu o hub pelo `Cobaia.exe` (ver o comentário de `comando_direto`). A conferência do Ollama fica fora
    # da trava da execução: ela pode esperar até 30 s, e a página relê o estado da corrida a cada dois segundos.
    def __init__(self, raiz: Path, permitida: bool = False, comando_da_corrida=None, pelo_exe: bool = False, garantir_ollama=None) -> None:
        self.raiz, self.pelo_exe = Path(raiz), bool(pelo_exe)
        self.permitida = bool(permitida) or self.pelo_exe
        self._padrao = comando_direto if self.pelo_exe else comando_padrao
        self._comando = comando_da_corrida or self._padrao
        self._garantir_ollama = garantir_ollama or garantir_ollama_no_ar
        self._trava = threading.Lock()
        self._processo: subprocess.Popen | None = None
        self._arquivo_do_log = None
        self._ultima: dict | None = None

    @staticmethod
    def _nome_da_saida() -> str:
        return dt.datetime.now().strftime("hub_%Y%m%d_%H%M%S")

    def _atualizar(self) -> None:
        if self._processo is not None and self._ultima is not None and self._ultima["codigo"] is None:
            codigo = self._processo.poll()
            if codigo is not None:
                self._ultima.update({"codigo": codigo, "fim": dt.datetime.now().isoformat(timespec="seconds")})
                if self._arquivo_do_log is not None:
                    self._arquivo_do_log.close()
                    self._arquivo_do_log = None

    def _log(self) -> str:
        if not self._ultima:
            return ""
        try:
            return Path(self._ultima["arquivo_do_log"]).read_bytes()[-TAMANHO_DO_LOG:].decode("utf-8", errors="replace")
        except OSError:
            return ""

    def estado(self, opcoes: dict | None = None) -> dict:
        """O estado da corrida lançada pelo hub e o comando sugerido para as opções dadas (o que a página mostra para copiar)."""
        opcoes = opcoes or opcoes_da_corrida()
        with self._trava:
            self._atualizar()
            u = self._ultima
            rodando = bool(u and u["codigo"] is None)
            sugerido = " ".join(self._padrao(self._nome_da_saida(), opcoes))
            return {"permitida": self.permitida, "pelo_exe": self.pelo_exe, "em_andamento": rodando, "terminou": bool(u and u["codigo"] is not None), "codigo": u["codigo"] if u else None,
                    "saida": u["saida"] if u else None, "inicio": u["inicio"] if u else None, "fim": u["fim"] if u else None,
                    "parada_pelo_hub": bool(u and u["parada_pelo_hub"]), "comando": u["comando"] if u else sugerido, "comando_sugerido": sugerido,
                    "repeticoes": list(REPETICOES_PERMITIDAS), "selecoes": list(SELECOES), "log": self._log()}

    def rodar(self, repeticoes, selecao="todos", desde=None) -> dict:
        if not self.permitida:
            raise Recusa(403, "o hub foi aberto sem --permitir-execucao: copie o comando e rode na sua janela, na pasta experimentos")
        opcoes = opcoes_da_corrida(repeticoes, selecao, desde)
        n = opcoes["repeticoes"]

        def recusar_se_rodando() -> None:
            self._atualizar()
            if self._ultima and self._ultima["codigo"] is None:
                raise Recusa(409, f"a corrida {self._ultima['saida']} ainda está rodando: uma corrida por vez")

        ambiente = {**os.environ, "PYTHONIOENCODING": "utf-8"}
        if self.pelo_exe:
            with self._trava:
                recusar_se_rodando()
            problema = self._garantir_ollama()
            if problema:
                raise Recusa(409, problema)
            ambiente.update({"RESULTADOS_DIR": pasta_dos_resultados(self.raiz), "PYTHONUNBUFFERED": "1"})
        with self._trava:
            recusar_se_rodando()
            saida = self._nome_da_saida()
            while (self.raiz / saida).exists() or (self._ultima and self._ultima["saida"] == saida):
                time.sleep(0.2)
                saida = self._nome_da_saida()
            comando = [str(x) for x in self._comando(saida, opcoes)]
            pasta_dos_logs = self.raiz / "hub" / "execucoes"
            pasta_dos_logs.mkdir(parents=True, exist_ok=True)
            arquivo = pasta_dos_logs / f"{saida}.log"
            self._arquivo_do_log = arquivo.open("wb")
            self._processo = subprocess.Popen(comando, cwd=str(EXP), stdout=self._arquivo_do_log, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, env=ambiente)
            self._ultima = {"saida": saida, "comando": " ".join(comando) if self._comando is self._padrao else "(lançador de teste)", "inicio": dt.datetime.now().isoformat(timespec="seconds"),
                            "fim": None, "codigo": None, "parada_pelo_hub": False, "arquivo_do_log": str(arquivo), "repeticoes": n}
        return self.estado()

    def parar(self) -> dict:
        with self._trava:
            self._atualizar()
            if not self._ultima or self._ultima["codigo"] is not None:
                raise Recusa(409, "não há corrida lançada pelo hub rodando agora")
            self._ultima["parada_pelo_hub"] = True
            pid = self._processo.pid
            if os.name == "nt":     # o lançador abre o PowerShell, que abre o Python e o navegador: a árvore inteira é encerrada
                subprocess.run(["taskkill", "/PID", str(pid), "/T", "/F"], capture_output=True, check=False)
            else:
                self._processo.terminate()
        with contextlib.suppress(subprocess.TimeoutExpired):
            self._processo.wait(timeout=10)
        return self.estado()


class Hub:
    """O que o servidor responde: o acervo das corridas e as revisões, juntos."""

    def __init__(self, acervo: hd.Acervo, revisoes: hr.Revisoes, execucao: Execucao | None = None, selecao_git=None, sonda=None, ollama_no_ar=None,
                 painel: Path | None = None, fontes_do_painel=None) -> None:
        self.acervo = acervo
        self.revisoes = revisoes
        self.execucao = execucao or Execucao(acervo.raiz)
        self.vivo = hd.AoVivo(acervo.raiz, leituras=acervo.leituras, calibracao=acervo.calibracao, limiares=acervo.limiares)
        self._selecao_git = selecao_git
        self._sonda = sonda or porta_responde
        self._ollama_no_ar = ollama_no_ar or (lambda: self._sonda(PORTA_DO_OLLAMA))
        self.painel = Path(painel) if painel is not None else PAINEL_LOCAL
        self.fontes_do_painel = tuple(fontes_do_painel) if fontes_do_painel is not None else FONTES_DO_PAINEL

    # ! Alteração de IA - Revisar: (25/11/2026, ficha 109, decisão 170) `central` é a tela "Início" do hub: diz se o site (porta 8080), a API
    # (8000) e o Ollama (11434) respondem agora, dá os endereços do site, da documentação da API e do painel publicado, e diz quantos casos e
    # corridas o hub tem e se o botão de rodar os cenários está liberado.
    # ! Motivo: o Eric pediu o hub como central de tudo, aberta pelo `.exe`: é dela que se chega ao site e à API. As três sondas correm ao
    # mesmo tempo porque, no Windows, uma porta fechada só é dada como fechada no fim do tempo de espera, e em fila a tela levaria segundos
    # para aparecer. A sonda só abre e fecha a conexão. O endereço do painel é o do artefato publicado do projeto, o mesmo do README.
    def central(self) -> dict:
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as fila:
            site, api, ollama = fila.submit(self._sonda, PORTA_DO_SITE), fila.submit(self._sonda, PORTA_DA_API), fila.submit(self._ollama_no_ar)
            no_ar = {"site": bool(site.result()), "api": bool(api.result()), "ollama": bool(ollama.result()), "hub": True}
        servicos = [{"id": "site", "nome": "Site de demonstração (CobaiaFront)", "url": f"http://localhost:{PORTA_DO_SITE}"},
                    {"id": "api", "nome": "API do site (CobaiaAPI)", "url": f"http://localhost:{PORTA_DA_API}/docs"},
                    {"id": "ollama", "nome": "Ollama, que roda o modelo do agente", "url": None},
                    {"id": "hub", "nome": "Hub central", "url": None}]
        return {"servicos": [{**s, "no_ar": no_ar[s["id"]]} for s in servicos], "painel": estado_do_painel(self.painel, self.fontes_do_painel), "pelo_exe": self.execucao.pelo_exe,
                "execucao_permitida": self.execucao.permitida, "casos": len(self.acervo.indice()), "corridas": len(self.acervo.corridas())}

    # ! Alteração de IA - Revisar: (25/11/2026, Pós-Fase 4, pacote Q7) `selecao` devolve o que a seleção pelo Git rodaria agora: a decisão de
    # `impacto_git.decidir_para_a_corrida` para o diff do commit de partida (o `desde` pedido, ou o último commit testado do registro em
    # `<resultados>/hub/commits_testados.jsonl`) até a pasta de trabalho.
    # ! Motivo: plano, seção 3.7: "a seleção diz quais cenários rodar e por quê". A página mostra a decisão antes de qualquer corrida, com o
    # que ficaria de fora à vista, para o analista não lançar uma corrida selecionada sem saber o que ela deixa de testar.
    def selecao(self, desde: str | None) -> dict:
        desde = desde or None
        if desde is not None and not _COMMIT.match(desde):
            raise ValueError("desde: esperava o identificador de um commit (de 7 a 40 caracteres hexadecimais)")
        if self._selecao_git is not None:
            return self._selecao_git(desde)
        import impacto_git as ig
        return ig.decidir_para_a_corrida(desde=desde, registro=self.acervo.raiz / "hub" / "commits_testados.jsonl")

    def ao_vivo(self) -> dict:
        """A corrida em andamento e o último diagnóstico dela; diz também se esse caso está entre os do hub, para a página poder abri-lo."""
        dado = self.vivo.ler()
        ultimo = dado.get("ultimo_diagnostico")
        if ultimo:
            try:
                self.acervo.iteracao(ultimo["tid"])
                ultimo["no_hub"] = True
            except KeyError:
                ultimo["no_hub"] = False
        return dado

    def trace(self, tid: str) -> Path:
        arq = self.acervo.trace(tid)            # KeyError se a trilha não está no hub
        if arq is None:
            raise KeyError("este caso não tem trace gravado")
        return arq

    def executar(self, pedido: dict) -> dict:
        if not isinstance(pedido, dict):
            raise ValueError("pedido: esperava um objeto")  # noqa: TRY004 - toda recusa de um pedido é ValueError, que o servidor traduz em 400
        if pedido.get("acao") == "rodar":
            return self.execucao.rodar(pedido.get("repeticoes"), pedido.get("selecao"), pedido.get("desde"))
        if pedido.get("acao") == "parar":
            return self.execucao.parar()
        raise ValueError(f"acao: {pedido.get('acao')!r} não é uma ação da execução")

    def _iteracoes(self, caso: str) -> list[dict]:
        return [{"tid": i["tid"], "hash": i["hash"], "numero": i["numero"]} for i in self.acervo.iteracoes(caso)]

    def _resumo(self, estado: dict) -> dict:
        v = estado["veredito_atual"]
        return {"veredito": v["veredito"] if v else None, "veredito_rotulo": hr.VEREDITOS[v["veredito"]] if v else None,
                "vale_para_a_iteracao_atual": estado["veredito_vale_para_a_iteracao_atual"], "ativas": estado["contagem"]["ativas"],
                "conversas": estado["contagem"]["conversas"], "estado_55": estado["campos_55"]["estado"]}

    def _desta_iteracao(self, estado: dict, tid: str, hash_: str) -> dict:
        lido = estado["lido"]
        return {"lida": bool(lido and lido["tid"] == tid and lido["hash"] == hash_)}

    def indice(self) -> dict:
        casos = self.acervo.indice()
        resumos: dict[str, dict] = {}
        for linha in casos:
            if linha["caso"] not in resumos:
                resumos[linha["caso"]] = self._resumo(hr.estado(self.revisoes.eventos(linha["caso"]), self._iteracoes(linha["caso"])))
            linha["revisao"] = resumos[linha["caso"]]
        return {"corridas": self.acervo.corridas(), "casos": casos, "opcoes": opcoes()}

    def caso(self, tid: str) -> dict:
        """O caso do acervo mais a revisão dele e o que mudou desde a última iteração que o analista leu ou julgou (ou desde a anterior)."""
        caso = self.acervo.caso(tid)
        eventos = self.revisoes.eventos(caso["caso"])
        estado = hr.estado(eventos, self._iteracoes(caso["caso"]))
        vistas = {e["iteracao"]["tid"] for e in eventos if e["tipo"] == "lido" or (e["tipo"] == "veredito" and e["autor"]["papel"] == "analista")}
        anteriores = [i for i in caso["iteracoes"] if i["numero"] < caso["iteracao"]]
        ja_vistas = [i for i in anteriores if i["tid"] in vistas]
        referencia = (ja_vistas or anteriores or [None])[-1]
        caso["mudancas"] = {"de": referencia["numero"] if referencia else None, "motivo": "a última que você leu ou julgou" if ja_vistas else "a anterior",
                            "itens": self.acervo.mudancas(referencia["tid"], tid) if referencia else []}
        caso["arvore_html"] = hp.arvore_para_html(caso["arvore"])
        arq = self.acervo.trace(tid)
        if arq is not None:         # o comando que abre o trace no visualizador do Playwright, para copiar
            caso["trace"]["comando"] = "..\\.venv\\Scripts\\playwright.exe show-trace " + (f'"{arq}"' if " " in str(arq) else str(arq))
        caso["revisao"] = estado
        caso["revisao_desta_iteracao"] = self._desta_iteracao(estado, tid, caso["hash"])
        return caso

    def revisar(self, pedido: dict) -> dict:
        """Grava uma ação do analista. O autor é sempre o analista e a iteração é a da trilha pedida, as duas postas aqui."""
        if not isinstance(pedido, dict):
            raise ValueError("pedido: esperava um objeto")  # noqa: TRY004 - toda recusa de um pedido é ValueError, que o servidor traduz em 400
        it = self.acervo.iteracao(pedido.get("tid"))          # KeyError se a trilha não está no hub
        caso, iteracao = it["caso"], {"tid": it["tid"], "hash": it["hash"], "numero": it["numero"]}
        nome = (pedido.get("autor") or {}).get("nome") if isinstance(pedido.get("autor"), dict) else None
        autor = {"nome": nome, "papel": "analista"}
        comum = {"autor": autor, "iteracao": iteracao}
        acao = pedido.get("acao")

        def conferir_bloco(ancora) -> None:
            if isinstance(ancora, dict) and ancora.get("bloco") not in BLOCOS_DO_RELATORIO:
                raise ValueError(f"ancora.bloco: {ancora.get('bloco')!r} não é um bloco do relatório")

        if acao == "comentar":
            conferir_bloco(pedido.get("ancora"))
            self.revisoes.registrar(caso, {"tipo": "comentario", **comum, **{k: pedido.get(k) for k in CAMPOS_DO_RASCUNHO}})
        elif acao == "estado_da_conversa":
            self.revisoes.registrar(caso, {"tipo": "estado_da_conversa", **comum, "conversa": pedido.get("conversa"), "estado": pedido.get("estado")})
        elif acao == "lido":
            self.revisoes.registrar(caso, {"tipo": "lido", **comum})
        elif acao == "campos_55":
            self.revisoes.registrar(caso, {"tipo": "campos_55", **comum, **{k: pedido[k] for k in ("severidade", "prioridade", "estado") if k in pedido}})
        elif acao == "causa_sugerida":
            self.revisoes.registrar(caso, {"tipo": "causa_sugerida", **comum, **{k: pedido.get(k) for k in ("causa", "campo", "texto")}})
        elif acao == "enviar_revisao":
            rascunhos = pedido.get("rascunhos") or []
            if not isinstance(rascunhos, list) or not all(isinstance(r, dict) for r in rascunhos):
                raise ValueError("rascunhos: esperava uma lista de comentários")
            for r in rascunhos:
                conferir_bloco(r.get("ancora"))
            for chave in ("campos_55", "causa_sugerida"):
                if pedido.get(chave) is not None and not isinstance(pedido[chave], dict):
                    raise ValueError(f"{chave}: esperava um objeto")
            self.revisoes.enviar_revisao(caso, autor=autor, iteracao=iteracao, veredito=pedido.get("veredito"), resumo=pedido.get("resumo") or "",
                                         desfecho=pedido.get("desfecho"), rascunhos=[{k: r.get(k) for k in CAMPOS_DO_RASCUNHO} for r in rascunhos],
                                         campos_55=pedido.get("campos_55"), causa_sugerida=pedido.get("causa_sugerida"))
        else:
            raise ValueError(f"acao: {acao!r} não é uma ação do hub")
        estado = hr.estado(self.revisoes.eventos(caso), self._iteracoes(caso))
        return {"ok": True, "revisao": estado, "revisao_desta_iteracao": self._desta_iteracao(estado, it["tid"], it["hash"]), "resumo": self._resumo(estado)}


def _tratador(hub: Hub, falar: bool):
    class Tratador(BaseHTTPRequestHandler):
        server_version = "HubDoAgente/1"
        protocol_version = "HTTP/1.1"

        def log_message(self, formato, *args) -> None:
            if falar:
                super().log_message(formato, *args)

        def _responder(self, codigo: int, corpo: bytes, tipo: str, extras: dict | None = None, politica: str = POLITICA) -> None:
            self.send_response(codigo)
            self.send_header("Content-Type", tipo)
            self.send_header("Content-Length", str(len(corpo)))
            for nome, valor in (extras or {}).items():
                self.send_header(nome, valor)
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Referrer-Policy", "no-referrer")
            self.send_header("Content-Security-Policy", politica)
            self.end_headers()
            self.wfile.write(corpo)

        def _json(self, codigo: int, dado) -> None:
            self._responder(codigo, json.dumps(dado, ensure_ascii=False).encode("utf-8"), "application/json; charset=utf-8")

        def _atender(self, funcao) -> None:
            """Roda a função do endereço e traduz a recusa em código HTTP: 404 para o que não existe no hub, 400 para o que não passa na validação."""
            try:
                funcao()
            except Recusa as e:
                self._json(e.codigo, {"erro": str(e)})
            except KeyError as e:
                self._json(404, {"erro": str(e.args[0]) if e.args else "não encontrado"})
            except ValueError as e:
                self._json(400, {"erro": str(e)})

        def _da_propria_pagina(self) -> None:
            """Recusa o pedido de gravação que não veio da página do próprio hub: nome de endereço que não é o desta máquina, ou origem de outro site."""
            porta = self.server.server_address[1]
            nome = (self.headers.get("Host") or "").rsplit(":", 1)[0].strip("[]").lower()
            if nome not in NOMES_LOCAIS:
                raise Recusa(403, "o hub só atende pelo endereço desta máquina")
            origem = self.headers.get("Origin")
            if origem is not None and origem not in {f"http://{n}:{porta}" for n in NOMES_LOCAIS}:
                raise Recusa(403, "o pedido veio de outra página, não da página do hub")

        # ! Alteração de IA - Revisar: (25/11/2026, etapa 2) o corpo do pedido é lido inteiro antes de qualquer recusa, e só depois vêm as
        # conferências (endereço, origem, tipo de conteúdo, JSON); os outros verbos (PUT, DELETE, PATCH) também leem o corpo e respondem 405.
        # ! Motivo: na primeira rodada dos testes o servidor recusava (403, 415, 404) sem ler o corpo; como a conexão fica aberta para o pedido
        # seguinte, o resto do corpo era lido como se fosse um pedido novo, e o servidor imprimia "Bad request version" seguido de
        # "ConnectionAbortedError: [WinError 10053]". Lendo antes, não sobra pedaço na conexão. Acima do limite o corpo é esvaziado sem ser
        # guardado, até um teto, e a conexão é fechada.
        def _ler_corpo(self) -> bytes:
            try:
                tamanho = int(self.headers.get("Content-Length") or "")
            except ValueError:
                self.close_connection = True
                raise Recusa(411, "faltou o tamanho do pedido") from None
            if tamanho > LIMITE_DO_CORPO:
                restante = min(tamanho, 20 * LIMITE_DO_CORPO)
                while restante > 0:
                    lido = self.rfile.read(min(65536, restante))
                    if not lido:
                        break
                    restante -= len(lido)
                self.close_connection = True
                raise Recusa(413, f"o pedido passa de {LIMITE_DO_CORPO} bytes")
            return self.rfile.read(tamanho)

        def _corpo_json(self, bruto: bytes) -> dict:
            if not (self.headers.get("Content-Type") or "").lower().startswith("application/json"):
                raise Recusa(415, "o hub só aceita gravação em JSON")
            try:
                return json.loads(bruto.decode("utf-8"))
            except ValueError:      # inclui UnicodeDecodeError
                raise Recusa(400, "o pedido não é JSON válido") from None

        def _verbo_que_o_hub_nao_tem(self) -> None:
            def rota() -> None:
                self._ler_corpo()
                raise Recusa(405, "o hub só atende GET e POST")

            self._atender(rota)

        do_PUT = do_DELETE = do_PATCH = _verbo_que_o_hub_nao_tem  # nomes fixados por http.server

        def do_GET(self) -> None:  # nome fixado por http.server
            partes = urllib.parse.urlsplit(self.path)
            consulta = urllib.parse.parse_qs(partes.query)

            def rota() -> None:
                if partes.path == "/":
                    self._responder(200, hp.pagina().encode("utf-8"), "text/html; charset=utf-8")
                elif partes.path == "/hub.css":
                    self._responder(200, hp.CSS.encode("utf-8"), "text/css; charset=utf-8")
                elif partes.path == "/hub.js":
                    self._responder(200, hp.JS.encode("utf-8"), "text/javascript; charset=utf-8")
                elif partes.path == "/api/indice":
                    self._json(200, hub.indice())
                elif partes.path == "/api/caso":
                    self._json(200, hub.caso((consulta.get("tid") or [""])[0]))
                elif partes.path == "/api/ao-vivo":
                    self._json(200, hub.ao_vivo())
                elif partes.path == "/painel":       # o painel local, lido do disco a cada pedido e servido com as regras dele
                    try:
                        corpo = hub.painel.read_bytes()
                    except OSError:
                        raise Recusa(404, "o painel ainda não foi gerado nesta máquina: rode python ferramentas/gerar_dashboard.py na raiz do repositório") from None
                    self._responder(200, corpo, "text/html; charset=utf-8", politica=POLITICA_DO_PAINEL)
                elif partes.path == "/api/central":
                    self._json(200, hub.central())
                elif partes.path == "/api/metricas":
                    self._json(200, hd.metricas(hub.acervo))
                elif partes.path == "/api/execucao":
                    um = lambda chave: (consulta.get(chave) or [None])[0]
                    try:
                        repeticoes = int(um("repeticoes") or 1)
                    except ValueError:
                        raise ValueError("repeticoes: esperava um inteiro") from None
                    self._json(200, hub.execucao.estado(opcoes_da_corrida(repeticoes, um("selecao"), um("desde"))))
                elif partes.path == "/api/selecao":
                    self._json(200, hub.selecao((consulta.get("desde") or [None])[0]))
                elif partes.path == "/api/trace":
                    arq = hub.trace((consulta.get("tid") or [""])[0])
                    self._responder(200, arq.read_bytes(), "application/zip", {"Content-Disposition": f'attachment; filename="{arq.name}"'})
                else:
                    raise Recusa(404, "endereço que o hub não tem")

            self._atender(rota)

        def do_POST(self) -> None:  # nome fixado por http.server
            partes = urllib.parse.urlsplit(self.path)

            def rota() -> None:
                bruto = self._ler_corpo()
                if partes.path not in ("/api/revisao", "/api/execucao"):
                    raise Recusa(404, "endereço que o hub não tem")
                self._da_propria_pagina()
                pedido = self._corpo_json(bruto)
                self._json(200, hub.revisar(pedido) if partes.path == "/api/revisao" else hub.executar(pedido))

            self._atender(rota)

    return Tratador


class Servidor(ThreadingHTTPServer):
    """O servidor do hub: um fio por pedido, e sem rastro no terminal quando o navegador fecha a conexão no meio de uma resposta."""
    daemon_threads = True

    def handle_error(self, request, client_address) -> None:
        if isinstance(sys.exc_info()[1], ConnectionError):
            return
        super().handle_error(request, client_address)


def criar_servidor(acervo: hd.Acervo, revisoes: hr.Revisoes, porta: int = PORTA_PADRAO, endereco: str = ENDERECO, falar: bool = False,
                   permitir_execucao: bool = False, comando_da_corrida=None, selecao_git=None, pelo_exe: bool = False, garantir_ollama=None,
                   sonda=None, ollama_no_ar=None, painel: Path | None = None, fontes_do_painel=None) -> ThreadingHTTPServer:
    """O servidor do hub, pronto para `serve_forever()`; `porta=0` pede uma porta livre ao sistema. Só aceita escutar na própria máquina.
    `permitir_execucao` libera o botão que lança a corrida de cenários; `pelo_exe` também libera, e faz a corrida usar o site e a API que
    o `Cobaia.exe` já subiu. `comando_da_corrida(saida, opcoes)` troca o lançador, `selecao_git(desde)` troca a leitura do Git,
    `garantir_ollama()` troca a conferência do Ollama e `sonda(porta)` e `ollama_no_ar()` trocam a leitura dos serviços (todos, nos testes)."""
    if endereco != ENDERECO:
        raise ValueError(f"o hub só escuta em {ENDERECO}: ele grava em disco e não tem senha")
    execucao = Execucao(acervo.raiz, permitir_execucao, comando_da_corrida, pelo_exe=pelo_exe, garantir_ollama=garantir_ollama)
    return Servidor((endereco, porta), _tratador(Hub(acervo, revisoes, execucao, selecao_git, sonda=sonda, ollama_no_ar=ollama_no_ar, painel=painel,
                                                     fontes_do_painel=fontes_do_painel), falar))


def conferir(acervo: hd.Acervo) -> int:
    """Monta todos os casos do acervo, como a página pediria, e diz quantos são por corrida; sai com 1 se algum não montar."""
    indice = acervo.indice()
    falhas = []
    for linha in indice:
        try:
            caso = acervo.caso(linha["tid"])
            hp.arvore_para_html(caso["arvore"])
        except Exception as e:  # noqa: BLE001 - a conferência relata qualquer caso que não monte, em vez de parar no primeiro
            falhas.append(f"{linha['tid']}: {type(e).__name__}: {e}")
    for c in acervo.corridas():
        print(f"{c['rotulo']} ({c['pasta']}): {c['casos']} casos, trilha {c['trilha']}")
    print(f"{len(indice)} casos em {len(acervo.corridas())} corridas; {len({l['caso'] for l in indice})} casos distintos (as iterações do mesmo caso contam uma vez)")
    for f in falhas:
        print("!! " + f)
    return 1 if falhas else 0


# ! Alteração de IA - Revisar: (25/11/2026, pacote Q6) `resumo` conta o que o hub mostra (casos por corrida, casos distintos, quantos têm mais de uma
# iteração, com divergência e com cura), as listas fechadas da revisão, os blocos do relatório e os testes do runner; `--resumo` grava
# `resultados_alvo/fase4/hub.{json,md}` e `--resumo --check` compara com o gravado.
# ! Motivo: o painel, o roadmap e o README dizem quantos casos o hub junta e o que ele oferece, e nenhum número do projeto é digitado à mão:
# eles são lidos deste arquivo, gerado do acervo e do próprio código.
NOME_DO_RESUMO = "hub"
PREFIXO_DO_RESUMO = "tb_f4_hub_"


def resumo(acervo: hd.Acervo) -> tuple[dict, str]:
    indice = acervo.indice()
    por_caso: dict[str, int] = {}
    for linha in indice:
        por_caso[linha["caso"]] = por_caso.get(linha["caso"], 0) + 1
    fonte_dos_testes = (EXP / "testar_hub.py").read_text(encoding="utf-8")
    nomes = re.findall(r"^def (teste_\w+)\(", fonte_dos_testes, flags=re.MULTILINE)
    corridas = [{k: c.get(k) for k in ("pasta", "rotulo", "descricao", "modo", "modelo", "inicio", "fim", "casos")} for c in acervo.corridas()]
    dado = {"metadados": {"gerado_em": dt.datetime.now().isoformat(timespec="seconds"), "gerado_por": "hub.py --resumo", "fonte": "as trilhas das corridas em resultados_alvo/ e o código do hub"},
            "corridas": corridas,
            "total": {"casos": len(indice), "casos_distintos": len(por_caso), "com_mais_de_uma_iteracao": sum(1 for n in por_caso.values() if n > 1),
                      "maior_numero_de_iteracoes": max(por_caso.values(), default=0), "com_divergencia": sum(1 for l in indice if l["divergencia"]),
                      "com_cura": sum(1 for l in indice if l["cura"])},
            "relatorio": {"blocos": len(BLOCOS_DO_RELATORIO), "campos_da_5_5": len(grr.CAMPOS_55), "blocos_do_agente": len(grr.SECOES_MANTIDAS_V3)},
            "revisao": {"vereditos": list(hr.VEREDITOS), "estados_da_conversa": list(hr.ESTADOS_DA_CONVERSA), "estados_55": list(hr.ESTADOS_55),
                        "severidades": list(hr.SEVERIDADES), "prioridades": list(hr.PRIORIDADES), "rotulos": list(hr.ROTULOS), "desfechos": list(hr.DESFECHOS),
                        "causas": len(hr.CAUSAS)},
            "testes": {"arquivo": "testar_hub.py", "total": len(nomes), "no_navegador": sum(1 for n in nomes if n.startswith("teste_pagina_"))}}
    t = dado["total"]
    linhas = pf.cabecalho("O que o hub central mostra (Pós-Fase 4, pacote Q6)", "hub.py --resumo", dado["metadados"]["fonte"], dado["metadados"]["gerado_em"][:10])
    linhas += ["", (f"O hub junta {t['casos']} casos com diagnóstico, de {len(corridas)} corridas; são {t['casos_distintos']} casos distintos, porque o mesmo caso diagnosticado "
                    f"mais de uma vez aparece como iterações ({t['com_mais_de_uma_iteracao']} casos têm mais de uma, e o que tem mais tem {t['maior_numero_de_iteracoes']}). "
                    f"Em {t['com_divergencia']} casos o que o modelo declarou não bate com o que o código conferiu, e em {t['com_cura']} houve cura de localizador. "
                    f"Cada caso abre com o relatório em {dado['relatorio']['blocos']} blocos ({dado['relatorio']['campos_da_5_5']} campos da seção 5.5 do syllabus e "
                    f"{dado['relatorio']['blocos_do_agente']} do que o agente fez). O runner `testar_hub.py` tem {dado['testes']['total']} testes, "
                    f"{dado['testes']['no_navegador']} deles abrindo a página no navegador sem janela."), "",
               f"<!-- tabela:{PREFIXO_DO_RESUMO}corridas -->", "| Corrida | Pasta | Modo | Modelo | Início | Casos no hub |", "|---|---|---|---|---|---|"]
    linhas += [f"| {c['rotulo']} | `{c['pasta']}` | {c['modo']} | `{c['modelo']}` | {str(c['inicio'])[:10]} | {c['casos']} |" for c in corridas]
    linhas += [f"<!-- /tabela:{PREFIXO_DO_RESUMO}corridas -->", ""]
    return dado, "\n".join(linhas)


# ! Alteração de IA - Revisar: (26/11/2026) `prova_do_botao` resume as corridas lançadas pelo botão de rodar os cenários (as pastas `hub_<data>_<hora>` de
# `resultados_alvo/` que têm `cenarios.jsonl`): quando rodaram, com que modelo, quantas execuções, em quantas o agente chegou ao resultado e em
# quantas a falha foi detectada. `python hub.py --botao [--check]` grava o resumo em `resultados_alvo/fase4/botao_do_hub.{json,md}`.
# ! Motivo: o Eric rodou os cenários pelo botão em 26/11/2026, a prova que faltava do hub aberto pelo `Cobaia.exe` (decisão 170). As pastas dessas
# corridas ficam fora do git (decisão 171), então o roadmap, o painel e o texto do TCC precisam de um derivado versionado para citar; sem ele, o
# número só existiria nesta máquina. Numa cópia sem as pastas o `--check` não tem o que comparar e sai com 0, dizendo isso, em vez de acusar diferença.
NOME_DA_PROVA_DO_BOTAO = "botao_do_hub"


def prova_do_botao(raiz: Path) -> tuple[dict, str]:
    raiz = Path(raiz)
    corridas = []
    for pasta in sorted(p for p in raiz.glob(hd.PREFIXO_DO_HUB + "*") if p.is_dir()):
        registros = hd._registros_dos_cenarios(pasta)
        if registros is None:
            continue
        try:
            cab = hd.Acervo(raiz, corridas=(pasta.name,), leituras={}, descobrir=False).corridas()[0]
        except (OSError, ValueError, KeyError):
            cab = {}
        # (26/11/2026, decisão 176) as marcas da hora de cada etapa, quando a corrida as gravou: quantas são e em quantos casos dão o tempo das seis etapas
        marcas = ea.ler(pasta)
        com_as_seis = sum(1 for t in ea.tempos_por_caso(marcas).values() if all(e in t for e in ("roteiro", "deteccao", "poda", "busca", "modelo", "selo")))
        corridas.append({"pasta": pasta.name, "inicio": cab.get("inicio"), "fim": cab.get("fim"), "modelo": cab.get("modelo"), "versao_ollama": cab.get("versao_ollama"),
                         "marcas": len(marcas), "casos_com_o_tempo_das_seis_etapas": com_as_seis,
                         "execucoes": len(registros), "cenarios": len({r.get("cenario") for r in registros}),
                         "task_success": sum(1 for r in registros if r.get("task_success") is True), "detectou": sum(1 for r in registros if r.get("detectou") is True)})
    dado = {"metadados": {"gerado_em": dt.datetime.now().isoformat(timespec="seconds"), "gerado_por": "hub.py --botao",
                          "fonte": "as pastas hub_<data>_<hora> de resultados_alvo/ (cenarios.jsonl e o cabeçalho da trilha)"},
            "total": len(corridas), "corridas": corridas}
    linhas = pf.cabecalho("As corridas lançadas pelo botão do hub", "hub.py --botao", dado["metadados"]["fonte"], dado["metadados"]["gerado_em"][:10])
    if corridas:
        u = corridas[-1]
        quando = (f"em {u['inicio'][8:10]}/{u['inicio'][5:7]}/{u['inicio'][:4]}, das {u['inicio'][11:16]}" + (f" às {u['fim'][11:16]}" if u.get("fim") else "")) if u.get("inicio") else "sem hora gravada"
        linhas += ["", (f"O botão de rodar os cenários do hub lançou {len(corridas)} {'corrida' if len(corridas) == 1 else 'corridas'} nesta máquina. A última, {quando}, rodou "
                        f"{u['execucoes']} execuções de {u['cenarios']} cenários com o modelo `{u['modelo']}` (Ollama {u['versao_ollama']}): o agente chegou ao resultado em "
                        f"{u['task_success']} de {u['execucoes']}, e a falha foi detectada em {u['detectou']} de {u['execucoes']}. As corridas do botão são uso do produto, não medida "
                        "do TCC, e as pastas delas ficam fora do git (decisão 171): este arquivo é o registro versionado.")]
        com_marcas = [c for c in corridas if c["marcas"]]
        if com_marcas:
            m = com_marcas[-1]
            linhas += ["", (f"Na corrida `{m['pasta']}`, lançada com a opção `--etapas-ao-vivo` (decisão 176), o agente gravou a hora de cada etapa: {m['marcas']} marcas, e "
                            f"{m['casos_com_o_tempo_das_seis_etapas']} de {m['execucoes']} casos têm o tempo das seis etapas no diagrama do hub.")]
        linhas += ["", "| Pasta | Início | Fim | Execuções | Cenários | Chegou ao resultado | Falha detectada | Marcas da hora de cada etapa |", "|---|---|---|---|---|---|---|---|"]
        linhas += [f"| `{c['pasta']}` | {c['inicio']} | {c['fim']} | {c['execucoes']} | {c['cenarios']} | {c['task_success']} de {c['execucoes']} | {c['detectou']} de {c['execucoes']} | {c['marcas']} |"
                   for c in corridas]
    else:
        linhas += ["", "Nenhuma corrida lançada pelo botão do hub foi encontrada nesta máquina."]
    return dado, "\n".join(linhas + [""])


def argumentos(argv: list[str] | None = None) -> argparse.Namespace:
    """As opções da linha de comando do hub."""
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--porta", type=int, default=PORTA_PADRAO, help=f"porta em {ENDERECO} (padrão {PORTA_PADRAO}; as cobaias usam 8080 e 8000)")
    ap.add_argument("--corridas", default=None, help="pastas de corrida em resultados_alvo/, separadas por vírgula (padrão: 18d, 21d, 24 e 28b)")
    ap.add_argument("--resultados", default=str(RESULTADOS), help="a pasta dos resultados (padrão: resultados_alvo/)")
    ap.add_argument("--revisoes", default=None, help="onde ficam os arquivos de revisão (padrão: <resultados>/hub/revisoes)")
    ap.add_argument("--sem-abrir", action="store_true", help="não abre o navegador")
    ap.add_argument("--falar", action="store_true", help="imprime cada pedido atendido")
    ap.add_argument("--conferir", action="store_true", help="monta todos os casos sem subir servidor e diz quantos são")
    ap.add_argument("--resumo", action="store_true", help="grava em <resultados>/fase4/hub.{json,md} o que o hub mostra (casos por corrida, iterações, listas da revisão, testes)")
    ap.add_argument("--check", action="store_true", help="com --resumo: regera e compara com o gravado, sem gravar")
    ap.add_argument("--permitir-execucao", action="store_true", help="libera o botão que lança a corrida de cenários (rodar_fase4.ps1) a partir da página; "
                                                                      "sem a opção, a página só mostra o comando para copiar")
    ap.add_argument("--pelo-exe", action="store_true", help="como o Cobaia.exe abre o hub: o site, a API e o banco já estão no ar, e o botão de rodar os cenários "
                                                             "fica liberado e chama o executar_fase4.py com --cobaias-no-ar")
    ap.add_argument("--botao", action="store_true", help="grava em <resultados>/fase4/botao_do_hub.{json,md} o resumo das corridas lançadas pelo botão do hub "
                                                         "(as pastas hub_<data>_<hora>); com --check, regera e compara sem gravar")
    return ap.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = argumentos(argv)
    raiz = Path(args.resultados)
    if args.botao:
        dado, md = prova_do_botao(raiz)
        if args.check and not dado["corridas"]:
            print(f"--check: nenhuma pasta {hd.PREFIXO_DO_HUB}... com cenarios.jsonl nesta cópia; não há o que conferir, e o resumo gravado fica como está")
            return 0
        return pf.fechar(NOME_DA_PROVA_DO_BOTAO, dado, md, "tb_f4_botao_", check=args.check, pasta=raiz / "fase4",
                         doc=EXP.parent.parent.parent / "Documentacao" / "memorial" / "3-resultados-e-analises" / "fase-4-relatorio.md")
    corridas = tuple(c.strip() for c in args.corridas.split(",") if c.strip()) if args.corridas else None
    # quem pede as corridas pelo nome, ou o resumo gravado do pacote Q6, fala só delas; sem isso o hub também mostra as corridas lançadas pelo botão
    acervo = hd.Acervo(raiz, corridas=corridas, descobrir=corridas is None and not args.resumo)
    if args.conferir:
        return conferir(acervo)
    if args.resumo:
        dado, md = resumo(acervo)
        return pf.fechar(NOME_DO_RESUMO, dado, md, PREFIXO_DO_RESUMO, check=args.check, pasta=raiz / "fase4",
                         doc=EXP.parent.parent.parent / "Documentacao" / "memorial" / "3-resultados-e-analises" / "fase-4-relatorio.md")
    revisoes = hr.Revisoes(Path(args.revisoes) if args.revisoes else raiz / "hub" / "revisoes")
    servidor = criar_servidor(acervo, revisoes, porta=args.porta, falar=args.falar, permitir_execucao=args.permitir_execucao, pelo_exe=args.pelo_exe)
    url = f"http://{ENDERECO}:{servidor.server_address[1]}/"
    print(f"Hub no ar em {url} ({len(acervo.indice())} casos). As revisões ficam em {revisoes.pasta}. Ctrl+C encerra.", flush=True)
    print("O botão de rodar os cenários está liberado e usa o site e a API que já estão no ar." if args.pelo_exe
          else "O botão de rodar os cenários está liberado." if args.permitir_execucao
          else "O botão de rodar os cenários mostra o comando para copiar (abra com --permitir-execucao para ele lançar a corrida).", flush=True)
    if not args.sem_abrir:
        with contextlib.suppress(Exception):
            webbrowser.open(url)
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nHub encerrado.")
    finally:
        servidor.server_close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
