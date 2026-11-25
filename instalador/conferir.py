#!/usr/bin/env python3
# ! Alteração de IA - Revisar: arquivo novo (pacote I1 do instalador único): a prova de uma instalação em quatro níveis (N1, o
# site e a API no ar com o seed; N2, o Chromium do Playwright abre o site; N3, o Ollama responde com um modelo pequeno; N4, o
# `qwen2.5:7b` baixa e responde), gravada em `registro.json`.
# ! Motivo: o `install.py` termina em "Instalação concluída" sem conferir nada do que instalou; no Linux ele nem instala o
# Ollama. Para provar a instalação em máquina limpa (pedido do Eric de 18/11/2026) é preciso um comando que suba os serviços,
# abra a página, chame o modelo e deixe a evidência em arquivo, igual nos três sistemas.
"""Uso: python -m instalador.conferir --celula <id> --saida <pasta> [--ate N1|N2|N3|N4] [--modelo-pequeno <nome>] [--reproduzir]
Sobe os serviços das cobaias, confere cada nível e grava <pasta>/registro.json. Código de saída 1 se algum nível falhou.
Importa `_env_common`, `run` e `restaurar_banco` sem alterá-los."""
import argparse
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import time
import traceback
import urllib.error
import urllib.request
from collections.abc import Callable
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

# ! Alteração de IA - Revisar: (19/11/2026, pacote I3) o import deixa de trazer `servicos`; volta a ser `registro, sistema, versoes`.
# ! Motivo: `instalador/servicos.py` deixou de existir; as opções do PHP por sistema estão em `_env_common.php_extension_flags`, que o `run.start_services` já chama.
from instalador import registro, sistema, versoes

REQUISITO = {"N2": "N1", "N4": "N3"}
OLLAMA = "http://127.0.0.1:11434"
_servicos: list[subprocess.Popen] = []
# ! Alteração de IA - Revisar: dicionário `_achadas`, onde as sondas guardam versões que só se conhecem com o serviço no ar
# (Ollama em /api/version, Playwright e Chromium no N2, identificador do modelo no N4).
# ! Motivo: o registro anotava a versão do Ollama pela saída de `ollama --version`, que sem servidor imprime um aviso em vez do
# número, e nunca anotava Playwright, Chromium nem o modelo; assim o julgamento do versoes.json não via essas ferramentas.
_achadas: dict[str, str] = {}


# ! Alteração de IA - Revisar: `ErroHttp` e `classificar_erro_do_ollama`; `_baixar` passa a levantar `ErroHttp` com o corpo da resposta.
# ! Motivo: o `urllib` esconde o corpo de um HTTP 500; o texto "model requires more system memory" do Ollama (que marca o
# 'nao_coube' do N4) ficava só no corpo, então toda falta de memória virava 'falhou'.
class ErroHttp(OSError):
    def __init__(self, status: int, url: str, corpo: str):
        super().__init__(f"HTTP {status} em {url}: {corpo[:600]}")
        self.status = status
        self.corpo = corpo


def classificar_erro_do_ollama(corpo: str) -> str:
    """'nao_coube' se o corpo do erro fala de memória; senão 'falhou'."""
    return "nao_coube" if "memory" in corpo.lower() else "falhou"


# ! Alteração de IA - Revisar: funções puras `identificador_nas_tags`, `extrair_versao` e `memoria_do_meminfo`.
# ! Motivo: o identificador do modelo era calculado lendo o manifesto em disco (não confere com o que `ollama list` mostra e
# falha sem permissão), a versão de cada ferramenta era a primeira linha da saída (que no Windows é o caminho do executável)
# e a memória da máquina não ia para o registro, embora decida o 'nao_coube' do N4.
def identificador_nas_tags(tags: dict, nome: str) -> str:
    """O `digest` (sem `sha256:`) do modelo `nome` na resposta de /api/tags; vazio se o Ollama não o lista."""
    for item in tags.get("models", []):
        if nome in (item.get("name"), item.get("model")):
            return str(item.get("digest", "")).removeprefix("sha256:")
    return ""


def extrair_versao(ferramenta: str, saida: str) -> str:
    """Só o número da versão na saída de `<ferramenta> --version`; vazio se não houver."""
    padroes = {"ollama": r"version is\s+(\d+(?:\.\d+)+)", "mariadb": r"Ver\s+(\d+(?:\.\d+)+)",
               "php": r"^PHP\s+(\d+(?:\.\d+)+)"}
    if ferramenta not in padroes:
        return ""
    achado = re.search(padroes[ferramenta], saida, re.MULTILINE)
    return achado.group(1) if achado else ""


def memoria_do_meminfo(texto: str) -> dict:
    """`memoria_total_gb` e `memoria_livre_gb` de um /proc/meminfo; a chave que faltar não entra."""
    dados = {}
    for chave, nome in (("MemTotal", "memoria_total_gb"), ("MemAvailable", "memoria_livre_gb")):
        achado = re.search(rf"^{chave}:\s+(\d+)\s*kB", texto, re.MULTILINE)
        if achado:
            dados[nome] = round(int(achado.group(1)) / 1048576, 1)
    return dados


def rodar(reg: dict, sondas: dict[str, Callable[[], tuple[str, str]]], ate: str = "N4") -> dict:
    """Roda as sondas na ordem dos níveis até `ate`. Nível cujo requisito não passou fica 'nao_rodou'; sonda que estoura vira
    'falhou' com o erro literal."""
    for nivel in registro.NIVEIS[:registro.NIVEIS.index(ate) + 1]:
        requisito = REQUISITO.get(nivel)
        if requisito and reg["niveis"][requisito]["estado"] != "passou":
            registro.anotar_nivel(reg, nivel, "nao_rodou", f"depende do {requisito}, que não passou")
            continue
        inicio = time.time()
        try:
            estado, detalhe = sondas[nivel]()
        except Exception as e:
            estado, detalhe = "falhou", f"{type(e).__name__}: {e}\n{traceback.format_exc(limit=3)}"
        registro.anotar_nivel(reg, nivel, estado, detalhe, round(time.time() - inicio, 1))
    return reg


def _baixar(url: str, dados: dict | None = None, espera: int = 30) -> tuple[int, str]:
    corpo = json.dumps(dados).encode("utf-8") if dados is not None else None
    pedido = urllib.request.Request(url, data=corpo, headers={"Content-Type": "application/json"} if corpo else {})
    try:
        with urllib.request.urlopen(pedido, timeout=espera) as resposta:
            return resposta.status, resposta.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        raise ErroHttp(e.code, url, e.read().decode("utf-8", errors="replace")) from e


def sonda_n1() -> tuple[str, str]:
    """O banco com o seed, o CobaiaFront na 8080 e a CobaiaAPI na 8000. Deixa os serviços no ar para o N2."""
    import _env_common as env
    import restaurar_banco
    import run
    cli = env.find_mysql_cli()
    if not cli:
        return "falhou", "cliente do MariaDB não encontrado (find_mysql_cli)"
    if not env.ensure_mariadb_running(cli):
        return "falhou", "o MariaDB não respondeu (ensure_mariadb_running)"
    contagens = restaurar_banco.contar(cli)
    if contagens != restaurar_banco.CONTAGENS_DO_SEED:
        return "falhou", f"contagens do banco {contagens}, esperado {restaurar_banco.CONTAGENS_DO_SEED}"
    # ! Alteração de IA - Revisar: (19/11/2026, pacote I3) saiu a troca na memória das opções do `php -S` que vinha aqui, antes de `run.start_services()`.
    # ! Motivo: célula L-U2404 de 18/11/2026 (HL4): com `-d extension_dir=/usr/bin/ext` o `php -S` subia sem `mysqli` e o N1
    # falhava com `Class "mysqli" not found`. Agora `run.start_services` recebe do `_env_common.php_extension_flags` as opções
    # do sistema (no Linux só o `output_buffering`), então a troca aqui não tem mais o que fazer.
    # ! Alteração de IA - Revisar: (19/11/2026, revisão do pacote I3, achado 1) a sonda recusa quando a 8080 ou a 8000 já
    # respondem antes de ela subir os serviços, e confere, depois da espera, se os dois processos que ela subiu seguem vivos.
    # ! Motivo: `run.start_services` não confere se as portas estão livres, e `run.wait_until_ready` só vê se a porta aceita
    # conexão. Com um `run.cmd` ou um `Cobaia.exe` aberto na máquina, o `php -S` e o `uvicorn` novos saíam na hora por porta
    # ocupada e a prova passava olhando o site e a API antigos; na célula ALVO isso esconderia um defeito dos arquivos novos.
    ocupadas = [str(porta) for porta in (run.FRONT_PORT, run.API_PORT) if run._port_responds(porta)]
    if ocupadas:
        return "falhou", (f"já há serviço respondendo na porta {' e na '.join(ocupadas)} antes de a prova subir os dela; "
                          "feche o run.cmd, o run.sh ou o Cobaia.exe que está aberto e rode a prova de novo")
    try:
        subidos = run.start_services()
    except SystemExit:
        return "falhou", "run.start_services encerrou; a mensagem dele está no log logo acima"
    _servicos.extend(subidos)
    if not run.wait_until_ready(60):
        return "falhou", f"as portas {run.FRONT_PORT} e {run.API_PORT} não responderam em 60 s"
    mortos = [nome for nome, processo in zip(("o site (php -S)", "a API (uvicorn)"), subidos) if processo.poll() is not None]
    if mortos:
        return "falhou", f"{' e '.join(mortos)} saiu logo depois de subir; a mensagem está no log logo acima"
    status, corpo = _baixar(f"http://localhost:{run.API_PORT}/api/produtos")
    produtos = json.loads(corpo)
    if status != 200 or len(produtos) != contagens["tbprodutos"]:
        return "falhou", f"/api/produtos devolveu {status} com {len(produtos)} produtos, esperado {contagens['tbprodutos']}"
    status, pagina = _baixar(f"http://localhost:{run.FRONT_PORT}/produtos_geral.php")
    if status != 200 or "Fatal error" in pagina or "Warning" in pagina:
        return "falhou", f"produtos_geral.php devolveu {status}; começo da página: {pagina[:400]}"
    if not any(p["nome"] in pagina for p in produtos):
        return "falhou", "produtos_geral.php abriu, mas nenhum produto do banco aparece nela"
    return "passou", f"{len(produtos)} produtos na API e na página do site"


# ! Alteração de IA - Revisar: (19/11/2026) o roteiro do navegador lê a versão do Playwright por `importlib.metadata`.
# ! Motivo: célula L-U2404 `novo` de 19/11/2026 (rodada `20261119-094340`): o Chromium abriu, a página carregou e o N2 falhou
# na linha do `print` com `AttributeError: module 'playwright' has no attribute '__version__'`; o pacote 1.64.1 não tem esse
# atributo, e a versão instalada na venv é o que o `importlib.metadata.version("playwright")` devolve.
ROTEIRO_DO_NAVEGADOR = """
import sys
from importlib.metadata import version
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    navegador = p.chromium.launch(headless=True)
    pagina = navegador.new_page()
    pagina.goto(sys.argv[1], wait_until="load", timeout=60000)
    print(version("playwright"), navegador.version, pagina.title(), sep="|")
    navegador.close()
"""


def sonda_n2(ferramentas: dict) -> tuple[str, str]:
    """A venv do AgenteCore abre o Chromium do Playwright, sem janela, na página do CobaiaFront. Exige o Playwright fixado."""
    import run
    from _env_common import AGENTE_CORE, OS_NAME
    python_venv = AGENTE_CORE / ".venv" / ("Scripts/python.exe" if OS_NAME == "Windows" else "bin/python")
    if not python_venv.exists():
        return "falhou", f"{python_venv} não existe: a venv do AgenteCore não foi criada"
    r = subprocess.run([str(python_venv), "-c", ROTEIRO_DO_NAVEGADOR, f"http://localhost:{run.FRONT_PORT}/"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=180, check=False)
    if r.returncode != 0:
        return "falhou", (r.stderr or r.stdout).strip()[-1500:]
    playwright_versao, chromium_versao, titulo = r.stdout.strip().split("|", 2)
    _achadas["playwright"] = playwright_versao
    _achadas["chromium"] = chromium_versao
    if versoes.comparar(playwright_versao, ferramentas["playwright"]) != "igual":
        return "falhou", (f"a venv do AgenteCore tem o Playwright {playwright_versao}; "
                          f"a versão fixada é {ferramentas['playwright']['testada']}")
    return "passou", f"Playwright {playwright_versao}, Chromium {chromium_versao}, título da página: {titulo}"


# ! Alteração de IA - Revisar: (19/11/2026, pacote I3) função nova `_modelo_presente`; `_ollama_responde` só roda o `ollama
# pull` quando o Ollama não lista o modelo.
# ! Motivo: a prova rodava `ollama pull` sempre. Nas células limpas isso não faz diferença (o modelo nunca está lá), mas a
# célula ALVO roda na máquina das corridas, onde o `qwen2.5:7b` das medidas já está baixado: se a etiqueta mudasse no
# registro de modelos, o `pull` trocaria o modelo medido sem ninguém pedir. A docstring já dizia "baixa o modelo se faltar".
# ! Alteração de IA - Revisar: (19/11/2026, revisão do pacote I3, achado 3) `_modelo_presente` passa a devolver `None` quando não
# deu para ler `/api/tags`, e `_ollama_responde` falha nesse caso em vez de baixar.
# ! Motivo: uma falha passageira na leitura de `/api/tags` devolvia False e levava ao `ollama pull`, inclusive do `qwen2.5:7b` na
# máquina das medidas, que era justamente o que esta função queria evitar.
def _modelo_presente(modelo: str) -> bool | None:
    """O Ollama já lista o modelo em /api/tags? None quando não deu para ler a lista."""
    try:
        _, corpo = _baixar(f"{OLLAMA}/api/tags", espera=30)
        return bool(identificador_nas_tags(json.loads(corpo), modelo))
    except (OSError, ValueError):
        return None


# ! Alteração de IA - Revisar: (19/11/2026, pacote I3) função nova `ler_passos_da_instalacao`; o `main` copia o resultado
# para a chave `instalacao` do registro.
# ! Motivo: a seção 3.3 do plano aprovado pede no `registro.json` o tempo de cada passo da instalação; o `install.py` passou
# a gravar esses tempos em `.ferramentas/instalacao/passos.json` (desvio 7 do anexo do plano), e a prova roda depois, em
# outro processo.
def ler_passos_da_instalacao(arquivo: Path | None = None) -> dict:
    """O que o `install.py` gravou sobre a última instalação desta pasta (quando, com que resultado e quanto levou cada
    passo); vazio se o arquivo não existe ou não abre."""
    arquivo = arquivo or RAIZ / ".ferramentas" / "instalacao" / "passos.json"
    try:
        dados = json.loads(arquivo.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    if not isinstance(dados, dict):
        return {}
    dados.pop("tag_ia", None)
    return dados


def _ollama_responde(modelo: str) -> tuple[str, str]:
    """Baixa o modelo se faltar e pede uma resposta curta, só em CPU. Se o Ollama não está no ar, tenta subir `ollama serve`."""
    from _env_common import find_ollama
    ollama = find_ollama()
    if not ollama:
        return "falhou", "o executável do Ollama não foi encontrado (find_ollama)"
    try:
        _, corpo = _baixar(f"{OLLAMA}/api/version", espera=5)
    except OSError:
        _servicos.append(subprocess.Popen([ollama, "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL))
        corpo = None
        for _ in range(30):                      # a cada 2 s, até 60 s
            time.sleep(2)
            try:
                _, corpo = _baixar(f"{OLLAMA}/api/version", espera=5)
                break
            except OSError:
                continue
        if corpo is None:
            return "falhou", "o Ollama não respondeu em /api/version 60 s depois de `ollama serve` subir"
    versao = json.loads(corpo)["version"]
    _achadas["ollama"] = versao
    presente = _modelo_presente(modelo)
    if presente is None:
        return "falhou", (f"Ollama {versao}: não deu para ler a lista de modelos em /api/tags; a prova não baixa o {modelo} "
                          "sem saber se ele já está na máquina")
    if not presente:
        try:
            r = subprocess.run([ollama, "pull", modelo], capture_output=True, text=True, encoding="utf-8", errors="replace",
                               timeout=3600, check=False)
        except subprocess.TimeoutExpired:
            return "falhou", f"ollama pull {modelo} não terminou em 3600 s"
        if r.returncode != 0:
            return "falhou", f"ollama pull {modelo}: {(r.stderr or r.stdout).strip()[-800:]}"
    pedido = {"model": modelo, "prompt": "Responda só com a palavra: pronto", "stream": False,
              "options": {"num_gpu": 0, "num_predict": 16, "temperature": 0.1}}
    try:
        _, corpo = _baixar(f"{OLLAMA}/api/generate", pedido, espera=900)
    except ErroHttp as e:
        return classificar_erro_do_ollama(e.corpo), f"Ollama {versao}, {modelo}: {e}"
    except OSError as e:
        return "falhou", f"Ollama {versao}, {modelo}: {e}"
    resposta = json.loads(corpo).get("response", "").strip()
    if not resposta:
        return "falhou", f"Ollama {versao}, {modelo}: resposta vazia"
    return "passou", f"Ollama {versao}, {modelo} respondeu: {resposta[:80]}"


def sonda_n3(modelo: str) -> tuple[str, str]:
    return _ollama_responde(modelo)


def sonda_n4(ferramentas: dict) -> tuple[str, str]:
    """O modelo do projeto: baixa, responde e o identificador que o Ollama lista em /api/tags confere com o versoes.json."""
    reg = ferramentas["modelo"]
    estado, detalhe = _ollama_responde(reg["nome"])
    if estado != "passou":
        return estado, detalhe
    _, corpo = _baixar(f"{OLLAMA}/api/tags", espera=30)
    identificador = identificador_nas_tags(json.loads(corpo), reg["nome"])
    if not identificador:
        return "falhou", f"{detalhe}; o Ollama não listou {reg['nome']} em /api/tags, identificador não conferido"
    _achadas["modelo"] = identificador[:12]
    if versoes.comparar_identificador(identificador, reg) != "igual":
        return "falhou", f"{detalhe}; mas o identificador do modelo é {identificador[:12]}, e o testado é {reg['testada'][:12]}"
    return "passou", f"{detalhe}; identificador {identificador[:12]} confere"


def _maquina() -> dict:
    dados = {"plataforma": platform.platform(), "arquitetura": platform.machine(), "python": platform.python_version(),
             "nucleos": os.cpu_count()}
    sistema_operacional = platform.system()
    try:
        if sistema_operacional == "Linux":
            dados.update(memoria_do_meminfo(Path("/proc/meminfo").read_text(encoding="utf-8")))
        elif sistema_operacional == "Darwin":
            r = subprocess.run(["sysctl", "-n", "hw.memsize"], capture_output=True, text=True, check=False)
            dados["memoria_total_gb"] = round(int(r.stdout.strip()) / 1024 ** 3, 1)
        else:
            comando = ["powershell", "-NoProfile", "-Command",
                       "$o = Get-CimInstance Win32_OperatingSystem; \"$($o.TotalVisibleMemorySize)|$($o.FreePhysicalMemory)\""]
            r = subprocess.run(comando, capture_output=True, text=True, check=False)
            total, livre = r.stdout.strip().split("|")
            dados["memoria_total_gb"] = round(int(total) / 1048576, 1)
            dados["memoria_livre_gb"] = round(int(livre) / 1048576, 1)
    except (OSError, ValueError):
        dados.setdefault("memoria_total_gb", None)
    try:
        if sistema_operacional == "Windows":
            import install
            dados["administrador"] = install.eh_administrador()
        else:
            dados["administrador"] = os.geteuid() == 0
            dados["sudo_sem_senha"] = bool(shutil.which("sudo")) and subprocess.run(
                ["sudo", "-n", "true"], capture_output=True, check=False).returncode == 0
    except (OSError, AttributeError):
        dados.setdefault("administrador", None)
    if sistema_operacional == "Windows":
        comando = ["powershell", "-NoProfile", "-Command",
                   "$m = Get-MpComputerStatus; \"$($m.AntivirusEnabled)|$($m.RealTimeProtectionEnabled)|$($m.IsTamperProtected)\""]
        r = subprocess.run(comando, capture_output=True, text=True, check=False)
        if r.returncode == 0 and r.stdout.count("|") == 2:
            antivirus, tempo_real, adulteracao = r.stdout.strip().split("|")
            dados["defender"] = {"antivirus": antivirus, "tempo_real": tempo_real, "protecao_contra_adulteracao": adulteracao}
        else:
            dados["defender"] = {"erro": (r.stderr or r.stdout).strip()[:300]}
    return dados


def _versoes_encontradas() -> dict[str, str]:
    """A versão de cada ferramenta que dá para ler sem subir nada."""
    import _env_common as env
    achadas = {"python": platform.python_version()}
    for nome, executavel, argumento in (("php", env.find_php(), "-v"), ("mariadb", env.find_mariadbd_server(), "--version"),
                                        ("ollama", env.find_ollama(), "--version")):
        if executavel:
            r = subprocess.run([executavel, argumento], capture_output=True, text=True, encoding="utf-8", errors="replace", check=False)
            achadas[nome] = extrair_versao(nome, (r.stdout or "") + "\n" + (r.stderr or ""))
    return achadas


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--celula", required=True)
    ap.add_argument("--saida", required=True, type=Path)
    ap.add_argument("--ate", choices=registro.NIVEIS, default="N4")
    ap.add_argument("--modelo-pequeno", default=os.environ.get("COBAIA_MODELO_PEQUENO", "qwen2.5:0.5b"))
    ap.add_argument("--reproduzir", action="store_true")
    args = ap.parse_args(argv)
    ferramentas = versoes.carregar()
    reg = registro.novo(args.celula, sistema.detectar(), _maquina())
    reg["instalacao"] = ler_passos_da_instalacao()
    sondas = {"N1": sonda_n1, "N2": lambda: sonda_n2(ferramentas), "N3": lambda: sonda_n3(args.modelo_pequeno),
              "N4": lambda: sonda_n4(ferramentas)}
    iniciais = _versoes_encontradas()
    try:
        rodar(reg, sondas, ate=args.ate)
        registro.anotar_versoes(reg, {**iniciais, **_achadas}, ferramentas, reproduzir=args.reproduzir)
    finally:
        caminho = registro.gravar(reg, args.saida)
        for processo in _servicos:
            try:
                if processo.poll() is None:
                    processo.terminate()
            except OSError as e:
                print(f"não foi possível encerrar o processo {processo.pid}: {e}")
        try:
            import _env_common as env
            env.stop_managed_mariadbd()
        except Exception as e:
            print(f"não foi possível desligar o MariaDB: {e}")
    for nivel, dados in reg["niveis"].items():
        print(f"{nivel}: {dados['estado']} {dados['detalhe'][:160]}")
    print(f"registro gravado em {caminho}")
    impedidas = registro.impedida_por_versao(reg)
    if impedidas:
        print(f"versão impede: {', '.join(impedidas)}")
    return 1 if registro.falhou(reg) or impedidas else 0


if __name__ == "__main__":
    sys.exit(main())
