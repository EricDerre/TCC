# ! Alteração de IA - Revisar: arquivo novo (pacote I2 do instalador único): instala e confere, num Linux de `apt`, o que a
# célula L-U2404 de 18/11/2026 mostrou faltando: os pacotes certos do PHP, o `python3-venv`, o serviço e o root do MariaDB,
# as bibliotecas do Chromium e o Ollama na versão testada.
# ! Motivo: o `install.py` parava em "Não foi possível subir o MariaDB" com o serviço no ar (testava "no ar" entrando como
# root sem senha, e o root do Ubuntu só entra por unix_socket: `ERROR 1698 (28000): Access denied`), instalava `php` e
# `php-mysql` (que trazem o Apache e não trazem o mbstring: `Call to undefined function mb_strimwidth()`), não instalava o
# `python3-venv` (`ensurepip is not available`), baixava o Chromium sem as bibliotecas (`libnspr4.so: cannot open shared
# object file`) e, para o Ollama, só imprimia o comando. Os três arquivos que as corridas importam não podem mudar antes de a
# corrida 28b ser lida; este módulo os importa e fica no lugar deles até o pacote I3.
# ! Alteração de IA - Revisar: (19/11/2026, pacote I3 do instalador único) desde o pacote I3 este módulo é a biblioteca dos passos
# de Linux chamada por `install.instalar_no_linux`; as opções do PHP e o serviço do banco foram para o `_env_common.py`.
# ! Motivo: a corrida 28b foi lida em 19/11/2026, e os consertos que moravam em módulos provisórios entraram nos arquivos que o
# Windows e as corridas já importam (`_env_common.py` e `install.py`); aqui ficam só os passos que o Linux precisa e o Windows não.
"""Instalação e conferência das ferramentas num Linux de `apt`. Só biblioteca padrão."""
import importlib.util
import json
import os
import re
import subprocess
import sys
import time
import urllib.request
from collections.abc import Callable, Mapping
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

# ! Alteração de IA - Revisar: tirados os comentários de supressão do E402 dos imports abaixo; a ordem é a que o ruff pede (`--select I,RUF100`).
# ! Motivo: o `E402` não está ligado neste projeto, então a supressão não suprimia nada, e o ruff apontava `RUF100` (diretiva sem efeito) e `I001` (imports fora de ordem); fica no mesmo estilo de `instalador/conferir.py`.
import _env_common as env
import install

# ! Alteração de IA - Revisar: (19/11/2026, pacote I3) o import deixa de trazer `servicos`.
# ! Motivo: `instalador/servicos.py` deixou de existir; as opções do PHP agora vêm de `_env_common.php_extension_flags`.
from instalador import conferir, sistema, versoes

OLLAMA_SCRIPT = "https://ollama.com/install.sh"
OLLAMA_API = "http://127.0.0.1:11434"
EXTENSOES_DO_PHP = ("mysqli", "pdo_mysql", "mbstring")
AVISO_DO_ROOT = (
    "O site legado (Programacao/CobaiaFront/conn/connect.php) entra no MariaDB como root, sem senha.\n"
    "Neste sistema o root do MariaDB só entra pelo usuário root do Linux (unix_socket). Para o site funcionar,\n"
    "o instalador troca essa entrada para senha vazia: qualquer usuário desta máquina passa a entrar como root\n"
    "do MariaDB. Não aceite numa máquina que tenha um MariaDB em uso de verdade."
)


class Falha(Exception):
    """Um passo obrigatório não deu certo; a mensagem diz o que aconteceu e o que a pessoa pode fazer."""


def como_root(uid: int | None = None, tem_sudo: bool | None = None) -> list[str]:
    """O começo dos comandos que precisam de root: nada para quem já é root, `sudo` para os outros."""
    # ! Alteração de IA - Revisar: (19/11/2026, pacote I3) a decisão entre nada e `sudo` vem de `_env_common.prefixo_de_root`;
    # aqui só a falta do sudo vira `Falha`.
    # ! Motivo: `_env_common.subir_servico_no_linux` precisa da mesma decisão para ligar o serviço do MariaDB, e ela existia
    # só neste módulo; com duas cópias, uma mudaria sem a outra.
    prefixo = env.prefixo_de_root(uid, tem_sudo)
    if prefixo is None:
        # ! Alteração de IA - Revisar: a mensagem não manda mais rodar o instalador como root.
        # ! Motivo: como root as venvs e o navegador ficam na pasta do root e a entrada do root do MariaDB passa no teste pelo
        # unix_socket sem ser trocada; `install.main` agora recusa rodar como root, então a mensagem manda instalar o sudo.
        raise Falha("este passo precisa do sudo, e a máquina não tem; instale o sudo (como root: apt-get install -y sudo) e "
                    "rode o instalador de novo, como usuário comum")
    return prefixo


# ! Alteração de IA - Revisar: (19/11/2026) `pacote_instalado` e a instalação dos pacotes passam a servir também ao `dnf`.
# ! Motivo: célula L-F45 de 19/11/2026 (suspeita HL3 confirmada): no Fedora o instalador rodava `sudo apt-get update`
# ("sudo: apt-get: command not found") e parava em "PHP foi instalado mas não foi encontrado automaticamente. Feche e
# reabra o terminal", que manda a pessoa fazer a coisa errada. A decisão 141 põe o Fedora como melhor esforço.
def pacote_instalado(nome: str, familia: str = "apt") -> bool:
    """O gerenciador de pacotes diz que o pacote está instalado? (`dpkg-query` no `apt`, `rpm -q` no `dnf`.)"""
    if familia == "dnf":
        # ! Alteração de IA - Revisar: (19/11/2026, revisão da segunda rodada, M-1) pergunta ao `rpm` por `--whatprovides`.
        # ! Motivo: no Fedora o comando `curl` pode vir do pacote `curl-minimal`, que provê `curl`; com `rpm -q curl` o
        # instalador acharia que falta e rodaria `dnf install curl`, que entra em conflito com o `curl-minimal` instalado.
        return subprocess.run(["rpm", "-q", "--whatprovides", nome], capture_output=True, text=True, check=False).returncode == 0
    r = subprocess.run(["dpkg-query", "-W", "-f", "${db:Status-Status}", nome], capture_output=True, text=True, check=False)
    return r.returncode == 0 and r.stdout.strip() == "installed"


def pacotes_desejados(familia: str, falta_venv: bool) -> list[str]:
    """Os pacotes do sistema que o projeto usa, da tabela de `instalador/sistema.py`; o do venv só quando o Python em uso
    não tem o `ensurepip`."""
    tabela = sistema.pacotes(familia)
    return [*tabela["base"], *(tabela["venv"] if falta_venv else []), *tabela["php"], *tabela["mariadb"]]


def pacotes_que_faltam(pacotes: list[str], instalado: Callable[[str], bool] | None = None, familia: str = "apt") -> list[str]:
    """Os pacotes que o gerenciador da família não tem instalados. `instalado` só serve para os testes trocarem a consulta."""
    if instalado is None:
        return [p for p in pacotes if not pacote_instalado(p, familia)]
    return [p for p in pacotes if not instalado(p)]


def comando_apt(pacotes: list[str], prefixo: list[str]) -> list[str]:
    """`apt-get install` sem pergunta na tela (o DEBIAN_FRONTEND vai pelo `env`, porque o `sudo` não repassa variáveis)."""
    # ! Alteração de IA - Revisar: o comando ganha `--no-remove`: o `apt-get` não pode remover nenhum pacote já instalado.
    # ! Motivo: numa máquina com o `mysql-server`, `apt-get install -y mariadb-server` resolvia o conflito removendo o MySQL sem
    # perguntar; o `install.py` antigo pulava a instalação quando achava um cliente de banco.
    return [*prefixo, "env", "DEBIAN_FRONTEND=noninteractive", "apt-get", "install", "-y", "--no-remove", *pacotes]


def comando_de_instalar(pacotes: list[str], prefixo: list[str], familia: str) -> list[str]:
    """O comando que instala os pacotes sem pergunta na tela. O `dnf` não remove pacote em conflito sem o `--allowerasing`."""
    if familia == "dnf":
        return [*prefixo, "dnf", "install", "-y", *pacotes]
    return comando_apt(pacotes, prefixo)


def falta_o_modulo_de_venv() -> bool:
    """No Debian e no Ubuntu o `ensurepip` vem no pacote `python3-venv`; sem ele o `python -m venv` não cria a venv."""
    return importlib.util.find_spec("ensurepip") is None


def instalar_pacotes_do_sistema(info: dict) -> list[str]:
    """Instala pelo `apt` ou pelo `dnf` só o que falta e devolve a lista do que instalou."""
    familia = info["familia"]
    faltam = pacotes_que_faltam(pacotes_desejados(familia, falta_o_modulo_de_venv()), familia=familia)
    if not faltam:
        env.log("Pacotes do sistema: nada a instalar.")
        return []
    prefixo = como_root()
    env.log("Pacotes do sistema que faltam: " + " ".join(faltam))
    # ! Alteração de IA - Revisar: o `apt-get update` com falha passa a gerar um aviso, e a falha do `install` explica o `--no-remove`.
    # ! Motivo: numa máquina com o `mysql-server`, `apt-get install -y mariadb-server` removia o MySQL sem perguntar; agora o
    # `apt` recusa (`--no-remove`) e a mensagem diz que esta máquina tem outro servidor de banco, que o instalador não troca.
    # ! Alteração de IA - Revisar: (19/11/2026) o `apt-get update` só roda na família `apt`, e o comando de instalar vem de `comando_de_instalar`.
    # ! Motivo: célula L-F45 (HL3): no Fedora o instalador rodava `sudo apt-get update` e recebia "sudo: apt-get: command not found".
    if familia == "apt":
        atualizacao = env.run([*prefixo, "apt-get", "update"])
        if atualizacao.returncode != 0:
            env.log(f"Aviso: o `apt-get update` saiu com código {atualizacao.returncode}; o instalador segue, mas a lista de "
                    "pacotes pode estar velha.")
    if env.run(comando_de_instalar(faltam, prefixo, familia)).returncode != 0:
        if familia == "dnf":
            raise Falha("o dnf não conseguiu instalar: " + " ".join(faltam) + ". A mensagem dele está logo acima.")
        raise Falha("o apt-get não conseguiu instalar: " + " ".join(faltam) + ". A mensagem dele está logo acima. O "
                    "instalador não deixa o apt remover pacotes (`--no-remove`): se a mensagem fala em pacotes a remover, "
                    "esta máquina tem outro servidor de banco (por exemplo o mysql-server), e o instalador não o troca.")
    return faltam


def ler_extensoes(saida: str) -> dict[str, bool]:
    """Linhas `mysqli=1` viram {'mysqli': True}; a extensão que não aparece conta como não carregada."""
    achadas = dict(re.findall(r"^(\w+)=([01])\s*$", saida, re.MULTILINE))
    return {nome: achadas.get(nome) == "1" for nome in EXTENSOES_DO_PHP}


def conferir_php() -> str:
    """O PHP existe e, com as opções com que o site sobe, carrega mysqli, pdo_mysql e mbstring. Devolve o executável."""
    php = env.find_php()
    if not php:
        raise Falha("o PHP não foi encontrado depois da instalação dos pacotes")
    codigo = (f"foreach ({json.dumps(list(EXTENSOES_DO_PHP))} as $x) "
              '{ echo $x, "=", extension_loaded($x) ? "1" : "0", "\\n"; }')
    # ! Alteração de IA - Revisar: (19/11/2026, pacote I3) as opções do PHP vêm de `env.php_extension_flags` (antes `servicos.opcoes_do_php`).
    # ! Motivo: a regra por sistema (no Linux só o `output_buffering`) passou para o `_env_common.py`, para o site subir e esta conferência usarem as mesmas opções.
    r = subprocess.run([php, *env.php_extension_flags(php), "-r", codigo], capture_output=True, text=True,
                       encoding="utf-8", errors="replace", check=False)
    faltam = [nome for nome, carregada in ler_extensoes(r.stdout).items() if not carregada]
    if faltam:
        raise Falha(f"o PHP ({php}) não carregou: {', '.join(faltam)}. No Debian e no Ubuntu elas vêm nos pacotes "
                    "php-mysql e php-mbstring.")
    env.log(f"PHP: {php}, com {', '.join(EXTENSOES_DO_PHP)}.")
    return php


# ! Alteração de IA - Revisar: (19/11/2026, pacote I3) `subir_banco` passa a chamar `_env_common.ensure_mariadb_running`;
# saíram deste módulo `banco_no_ar`, `systemd_no_ar` e `comando_de_subir_o_banco`, que foram para o `_env_common.py`.
# ! Motivo: o conserto das suspeitas HL12 (acesso recusado não é banco desligado) e HL7 (sem o systemd o serviço sobe por
# `service mariadb start`) morava só aqui, e o `run.py` e a prova, que chamam `ensure_mariadb_running`, ficavam sem ele.
def subir_banco(cli: str) -> None:
    """Liga o serviço do MariaDB se ele não responde. Quem liga é `_env_common.ensure_mariadb_running`."""
    if not env.ensure_mariadb_running(cli):
        raise Falha("o MariaDB não subiu; a mensagem do comando que tentou ligar o serviço está logo acima.")


def confirmar_root_sem_senha(ambiente: Mapping[str, str], tem_terminal: bool, perguntar: Callable[[str], str] = input) -> bool:
    """`COBAIA_ROOT_SEM_SENHA=1` aceita e `=0` recusa, sem pergunta; sem a variável, pergunta se houver terminal."""
    valor = ambiente.get("COBAIA_ROOT_SEM_SENHA")
    if valor in ("0", "1"):
        return valor == "1"
    if not tem_terminal:
        return False
    resposta = perguntar("Trocar a entrada do root do MariaDB para senha vazia? [s/N] ")
    return resposta.strip().lower() in ("s", "sim", "y", "yes")


def garantir_root_sem_senha(cli: str, ambiente: Mapping[str, str] | None = None, tem_terminal: bool | None = None) -> None:
    """Se o root ainda não entra sem senha: avisa, pede a confirmação e chama o conserto que o `_env_common` já tem."""
    if env._can_connect(cli):
        return
    ambiente = os.environ if ambiente is None else ambiente
    if tem_terminal is None:
        tem_terminal = bool(sys.stdin and sys.stdin.isatty())
    for linha in AVISO_DO_ROOT.splitlines():
        env.log(linha)
    if not confirmar_root_sem_senha(ambiente, tem_terminal):
        raise Falha("a entrada do root do MariaDB não foi trocada. Rode o instalador de novo e responda s, ou aceite sem "
                    "pergunta com: COBAIA_ROOT_SEM_SENHA=1 ./install.sh")
    if not env.ensure_root_no_password(cli):
        raise Falha("não foi possível deixar o root do MariaDB sem senha; as mensagens acima dizem o que tentar à mão.")


def python_da_venv(pasta: Path) -> Path:
    return pasta / ("Scripts/python.exe" if env.OS_NAME == "Windows" else "bin/python")


# ! Alteração de IA - Revisar: função nova `conferir_pasta_da_venv`, chamada antes de `install.setup_cobaia_api()` e no começo de `preparar_agente`.
# ! Motivo: com a `.venv` presente, `install.setup_cobaia_api` roda `.venv/bin/pip` sem conferir se existe e o instalador morria em
# `FileNotFoundError` com traceback; acontece com a venv que o instalador antigo deixou quando parou no `ensurepip is not
# available` (célula L-U2404) e com um clone do Windows usado pelo WSL.
def conferir_pasta_da_venv(pasta: Path) -> None:
    """Uma `.venv` que existe sem o `python` e o `pip` dentro veio de outro sistema (a do Windows, num clone usado pelo WSL)
    ou de uma instalação que parou no meio. O instalador não a apaga sozinho: diz o que fazer."""
    if not pasta.exists():
        return
    python_venv = python_da_venv(pasta)
    pip = python_venv.with_name("pip.exe" if env.OS_NAME == "Windows" else "pip")
    if not python_venv.exists() or not pip.exists():
        raise Falha(f"a pasta {pasta} existe, mas não tem {python_venv.name} e {pip.name} dentro: ela veio de outro sistema "
                    "(por exemplo, foi criada no Windows) ou de uma instalação que parou no meio. Apague a pasta e rode o "
                    "instalador de novo.")


def conferir_venv(pasta: Path, modulos: tuple[str, ...]) -> None:
    """A venv existe e importa os módulos; o `install.py` não confere o resultado do `pip`."""
    python_venv = python_da_venv(pasta)
    if not python_venv.exists():
        raise Falha(f"{python_venv} não existe: a venv não foi criada")
    r = subprocess.run([str(python_venv), "-c", "import " + ", ".join(modulos)], capture_output=True, text=True, check=False)
    if r.returncode != 0:
        raise Falha(f"a venv {pasta} não importa {', '.join(modulos)}: {(r.stderr or r.stdout).strip()[-400:]}")


def bibliotecas_que_faltam(saida_do_ldd: str) -> list[str]:
    """Os nomes das linhas `libX.so => not found` do `ldd`, sem repetição."""
    return sorted(set(re.findall(r"^\s*(\S+) => not found", saida_do_ldd, re.MULTILINE)))


def binarios_do_chromium(base: Path | None = None) -> list[Path]:
    """Os executáveis do Chromium que o Playwright baixou (o navegador e o `chrome-headless-shell`)."""
    base = base or Path.home() / ".cache" / "ms-playwright"
    nomes = ("chrome", "chrome-headless-shell", "headless_shell")
    return sorted(p for p in base.glob("chromium*/*/*") if p.name in nomes and p.is_file())


def comando_do_chromium(python_venv: str, com_bibliotecas: bool) -> list[str]:
    return [python_venv, "-m", "playwright", "install", *(["--with-deps"] if com_bibliotecas else []), "chromium"]


def instalar_chromium(python_venv: Path, info: dict) -> None:
    """Baixa o Chromium do Playwright e, no `apt`, as bibliotecas do sistema de que ele precisa."""
    com_bibliotecas = info["familia"] == "apt"
    if env.playwright_chromium_instalado():
        env.log("Chromium do Playwright já baixado.")
    elif env.run(comando_do_chromium(str(python_venv), com_bibliotecas)).returncode != 0:
        raise Falha("o Playwright não conseguiu baixar o Chromium ou instalar as bibliotecas dele; a mensagem está acima.")
    faltam: list[str] = []
    for binario in binarios_do_chromium():
        r = subprocess.run(["ldd", str(binario)], capture_output=True, text=True, check=False)
        faltam += bibliotecas_que_faltam(r.stdout)
    if not faltam:
        return
    lista = " ".join(sorted(set(faltam)))
    if not com_bibliotecas:
        # ! Alteração de IA - Revisar: (19/11/2026) numa distribuição de melhor esforço (Fedora), a falta das bibliotecas do
        # Chromium vira aviso e a instalação segue.
        # ! Motivo: célula L-F45: o Playwright avisa "your OS is not officially supported by Playwright; downloading fallback
        # build for ubuntu24.04-x64" e o Chromium não abre ("libnspr4.so: cannot open shared object file"). O plano aprovado
        # garante só o site e a API no Fedora (N1) e deixa as bibliotecas do navegador fora do escopo (seção 8).
        if info.get("suporte") == "melhor_esforco":
            env.log(f"Aviso: o Chromium do Playwright não vai abrir nesta distribuição sem estas bibliotecas do sistema: {lista}")
            env.log("O instalador não as instala fora do Debian e do Ubuntu; o site e a API funcionam sem elas.")
            return
        raise Falha(f"faltam bibliotecas do sistema para o Chromium abrir: {lista}")
    env.log(f"Faltam bibliotecas do sistema para o Chromium: {lista}")
    if env.run([str(python_venv), "-m", "playwright", "install-deps", "chromium"]).returncode != 0:
        raise Falha(f"não foi possível instalar as bibliotecas do Chromium ({lista}); a mensagem está acima.")


def versao_do_ollama(ollama: str) -> str:
    """O número da versão do executável, ou vazio se a saída não tiver um."""
    r = subprocess.run([ollama, "--version"], capture_output=True, text=True, encoding="utf-8", errors="replace", check=False)
    return conferir.extrair_versao("ollama", (r.stdout or "") + "\n" + (r.stderr or ""))


def decidir_ollama(encontrada: str | None, registro: dict) -> str:
    """'instalar' se não há Ollama; 'usar' se a versão é a testada; 'avisar' se é outra dentro da faixa ou não deu para ler;
    'parar' se está fora da faixa. O instalador nunca troca um Ollama que já está na máquina (seção 3.2 do plano)."""
    if encontrada is None:
        return "instalar"
    return {"igual": "usar", "fora_da_faixa": "parar"}.get(versoes.comparar(encontrada, registro), "avisar")


def instalar_ollama(versao: str) -> None:
    """Baixa o script oficial para `.ferramentas/ollama/install.sh` e roda com `OLLAMA_VERSION`. O script usa o sudo."""
    roteiro = RAIZ / ".ferramentas" / "ollama" / "install.sh"
    env.log(f"Baixando o script oficial do Ollama ({OLLAMA_SCRIPT}) para instalar a versão {versao}...")
    try:
        install.baixar_arquivo(OLLAMA_SCRIPT, roteiro)
    except OSError as e:
        raise Falha(f"não foi possível baixar {OLLAMA_SCRIPT}: {e}") from e
    if env.run(["sh", str(roteiro)], env={**os.environ, "OLLAMA_VERSION": versao}).returncode != 0:
        raise Falha("o script do Ollama saiu com erro; a mensagem dele está logo acima.")


def ollama_responde(espera: int = 5) -> bool:
    try:
        with urllib.request.urlopen(f"{OLLAMA_API}/api/version", timeout=espera) as resposta:
            return resposta.status == 200
    except OSError:
        return False


def garantir_ollama_no_ar(ollama: str) -> subprocess.Popen | None:
    """Espera o serviço do Ollama responder; se não há serviço, sobe `ollama serve` e devolve o processo, para ser encerrado
    depois."""
    for _ in range(5):
        if ollama_responde():
            return None
        time.sleep(2)
    processo = subprocess.Popen([ollama, "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(30):
        time.sleep(2)
        if ollama_responde():
            return processo
    processo.terminate()
    raise Falha("o Ollama não respondeu em /api/version 60 s depois de `ollama serve` subir")


def preparar_ollama(ferr: dict, ambiente: Mapping[str, str] | None = None) -> str:
    """Instala o Ollama na versão testada se ele falta, confere a versão se ele existe, e baixa o modelo."""
    ambiente = os.environ if ambiente is None else ambiente
    registro = ferr["ollama"]
    ollama = env.find_ollama()
    encontrada = versao_do_ollama(ollama) if ollama else None
    decisao = decidir_ollama(encontrada, registro)
    if decisao == "instalar":
        instalar_ollama(registro["testada"])
        ollama = env.find_ollama()
        if not ollama:
            raise Falha("o script do Ollama terminou, mas o executável `ollama` não apareceu no PATH")
        # ! Alteração de IA - Revisar: depois do script oficial, confere a versão do executável contra a testada do versoes.json.
        # ! Motivo: o instalador passava `OLLAMA_VERSION` ao script e seguia sem conferir; se o script ignorasse a variável ou
        # instalasse outra, o `ollama pull` e as medidas rodariam numa versão que o projeto não testou.
        instalada = versao_do_ollama(ollama)
        if instalada and versoes.comparar(instalada, registro) != "igual":
            raise Falha(f"o script do Ollama instalou a versão {instalada}, e não a {registro['testada']} que foi pedida")
    elif decisao == "parar":
        # ! Alteração de IA - Revisar: a mensagem passa a mostrar a faixa inteira que o projeto aceita, não só o piso.
        # ! Motivo: com só `a partir do {aceita_de}` a pessoa não via o teto (`aceita_ate`) e achava que um Ollama mais novo servia.
        raise Falha(f"o Ollama desta máquina é o {encontrada}, fora da faixa que o projeto aceita (de {registro['aceita_de']} "
                    f"a {registro.get('aceita_ate') or 'a mais nova'}). O instalador não troca um Ollama já instalado; para atualizar: "
                    f"curl -fsSL {OLLAMA_SCRIPT} | OLLAMA_VERSION={registro['testada']} sh")
    elif decisao == "avisar":
        env.log(f"Aviso: o Ollama desta máquina é o {encontrada or 'de versão não lida'}; o projeto testou o "
                f"{registro['testada']}. Ele fica como está.")
    processo = garantir_ollama_no_ar(ollama)
    try:
        modelo = ambiente.get("COBAIA_MODELO_LLM", ferr["modelo"]["nome"])
        if env.modelo_llm_ja_baixado(ollama, modelo):
            env.log(f"Modelo {modelo} já baixado.")
        else:
            env.log(f"Baixando o modelo {modelo} (pode demorar na primeira vez)...")
            if env.run([ollama, "pull", modelo]).returncode != 0:
                raise Falha(f"`ollama pull {modelo}` falhou; a mensagem está logo acima.")
    finally:
        if processo is not None:
            processo.terminate()
    return ollama


def preparar_agente(info: dict, ferr: dict) -> None:
    """A venv do AgenteCore, o Chromium do Playwright com as bibliotecas e o Ollama com o modelo."""
    pasta = env.AGENTE_CORE / ".venv"
    conferir_pasta_da_venv(pasta)
    if not pasta.exists():
        env.log("Criando venv do AgenteCore...")
        env.run([sys.executable, "-m", "venv", str(pasta)])
    else:
        env.log("venv do AgenteCore já existe.")
    python_venv = python_da_venv(pasta)
    if not python_venv.exists():
        raise Falha(f"{python_venv} não existe: a venv do AgenteCore não foi criada")
    if env.run([str(python_venv), "-m", "pip", "install", "-r", str(env.AGENTE_CORE / "requirements.txt")]).returncode != 0:
        raise Falha("o pip não conseguiu instalar as dependências do AgenteCore; a mensagem está logo acima.")
    conferir_venv(pasta, ("playwright", "matplotlib"))
    instalar_chromium(python_venv, info)
    preparar_ollama(ferr)
