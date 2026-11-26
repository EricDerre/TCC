# ! Alteração de IA - Revisar: arquivo novo (pacote I1 do instalador único, decisões 140 e 141): diz a família do sistema em
# que o instalador roda (Windows; macOS com Homebrew; Linux de `apt`, de `dnf` ou sem suporte) e os nomes dos pacotes de cada uma.
# ! Motivo: o `install.py` só distinguia Windows, Linux e Darwin e, no Linux, chamava `apt-get` direto; num Fedora ou num Arch
# ele parava com "comando não encontrado", sem dizer o que fazer. A decisão 141 fixou quais distribuições são suportadas, quais
# são melhor esforço e quais recebem uma mensagem clara.
"""Família do sistema e pacotes por família. Só biblioteca padrão; não instala nada."""
import platform
import shutil
from pathlib import Path

SUPORTADAS = {"ubuntu": ("22.04", "24.04", "26.04"), "debian": ("12", "13")}
PACOTES = {
    "apt": {"base": ["curl", "ca-certificates", "zstd"], "venv": ["python3-venv"],
            "php": ["php-cli", "php-mysql", "php-mbstring"], "mariadb": ["mariadb-server"]},
    # ! Alteração de IA - Revisar: (19/11/2026, pacote I2, célula L-F45) o `gawk` entra nos pacotes de base do `dnf`.
    # ! Motivo: na rodada 20261119-134801 do Fedora 45 no WSL o script oficial do Ollama parou com "The following tools are
    # required but missing: - awk", porque a imagem não traz o `awk`; o instalador saía com erro depois de o site e a API já
    # estarem prontos. No Debian e no Ubuntu o `awk` (mawk) já vem na imagem, por isso a lista do `apt` não muda.
    "dnf": {"base": ["curl", "zstd", "gawk"], "venv": [],
            "php": ["php-cli", "php-mysqlnd", "php-mbstring"], "mariadb": ["mariadb-server"]},
    # ! Alteração de IA - Revisar: (25/11/2026, consertos da primeira execução do Actions) entra a tabela do `brew`: o PHP pela fórmula `php` e o MariaDB pela fórmula `mariadb@11.8`; sem pacotes de base nem do módulo `venv`.
    # ! Motivo: execuções M-15 e M-15I (macOS 15) de 25/11/2026: o macOS seguia o caminho antigo e parou em "Não foi possível subir o MariaDB" com o `brew services start mariadb` já feito; passa a seguir o fluxo por família. Decisão do dono do projeto (decisão 161, 25/11/2026): a fórmula `mariadb` do Homebrew já está na 13.1.2 e o `versoes.json` aceita o MariaDB só até a 13.0 (testado 11.8.9), então um Mac atualizado instalaria tudo e pararia no fim; a fórmula `mariadb@11.8` é a série testada. O `curl`, o `zstd` e o Python vêm do macOS e do `install.sh`, por isso `base` e `venv` ficam vazios.
    "brew": {"base": [], "venv": [], "php": ["php"], "mariadb": ["mariadb@11.8"]},
}


def ler_os_release(texto: str) -> dict[str, str]:
    """As linhas CHAVE=valor de /etc/os-release, sem aspas; comentário e linha vazia ficam de fora."""
    dados = {}
    for linha in texto.splitlines():
        linha = linha.strip()
        if not linha or linha.startswith("#") or "=" not in linha:
            continue
        chave, valor = linha.split("=", 1)
        dados[chave.strip()] = valor.strip().strip('"').strip("'")
    return dados


# ! Alteração de IA - Revisar: (25/11/2026, consertos da primeira execução do Actions, tarefa E) `familia` ganha o parâmetro `maquina` (o `platform.machine()`); no macOS com Homebrew, `x86_64` (processador Intel) dá `suporte` "melhor_esforco" e nome "macOS (Intel)", e os outros casos continuam "suportado"; sem Homebrew continua "falta_homebrew". `detectar` passa o `platform.machine()`.
# ! Motivo: decisão do dono do projeto de 25/11/2026 ("Melhor esforço, célula fica"): nos arquivos públicos do Homebrew (`Formula/p/php.rb`, `Formula/m/mariadb.rb`, `Formula/m/mariadb@11.8.rb`, lidos em 25/11/2026) o bloco `bottle` só traz pacote pronto de macOS para Apple Silicon (`arm64_sequoia`, `arm64_tahoe`, `arm64_golden_gate`) e para Linux; num Mac Intel o `brew install` compila do código-fonte e pode levar mais de uma hora, então o Mac Intel entra como o Fedora, como melhor esforço (a célula `M-15I` continua no fluxo). Nada disso foi observado em execução ainda: a segunda execução do fluxo é a que prova.
def familia(sistema: str, os_release: dict[str, str] | None = None, tem_brew: bool = False,
            maquina: str | None = None) -> dict:
    """A família (quem instala os pacotes) e o grau de suporte, pela decisão 141. `maquina` é o `platform.machine()`
    (só o macOS usa: `x86_64` é o Mac com processador Intel)."""
    if sistema == "Windows":
        return {"sistema": sistema, "familia": "windows", "id": "windows", "versao": "", "nome": "Windows", "suporte": "suportado"}
    if sistema == "Darwin":
        intel = (maquina or "").lower() in ("x86_64", "amd64")
        if not tem_brew:
            suporte = "falta_homebrew"
        else:
            suporte = "melhor_esforco" if intel else "suportado"
        return {"sistema": sistema, "familia": "brew", "id": "macos", "versao": "",
                "nome": "macOS (Intel)" if intel else "macOS", "suporte": suporte}
    if sistema != "Linux":
        return {"sistema": sistema, "familia": "nao_suportado", "id": sistema.lower(), "versao": "", "nome": sistema,
                "suporte": "nao_suportado"}
    dados = os_release or {}
    ident = dados.get("ID", "").lower()
    parecidos = {ident, *dados.get("ID_LIKE", "").lower().split()}
    nome = dados.get("PRETTY_NAME") or dados.get("NAME") or "Linux"
    versao = dados.get("VERSION_ID", "")
    if parecidos & {"debian", "ubuntu"}:
        suporte = "suportado" if versao in SUPORTADAS.get(ident, ()) else "melhor_esforco"
        return {"sistema": sistema, "familia": "apt", "id": ident, "versao": versao, "nome": nome, "suporte": suporte}
    if ident == "fedora":
        return {"sistema": sistema, "familia": "dnf", "id": ident, "versao": versao, "nome": nome, "suporte": "melhor_esforco"}
    return {"sistema": sistema, "familia": "nao_suportado", "id": ident, "versao": "", "nome": nome, "suporte": "nao_suportado"}


def pacotes(nome_da_familia: str) -> dict[str, list[str]]:
    """Os pacotes de sistema por grupo (base, venv, php, mariadb) para as famílias que o instalador sabe instalar."""
    if nome_da_familia not in PACOTES:
        raise ValueError(f"sem tabela de pacotes para a família {nome_da_familia}")
    return PACOTES[nome_da_familia]


def mensagem_nao_suportado(info: dict, ferramentas: dict) -> str:
    """O que dizer a quem roda o instalador num sistema sem suporte: o que ele instalaria, para a pessoa instalar à mão."""
    php, maria, py = ferramentas["php"], ferramentas["mariadb"], ferramentas["python"]
    return (
        f"Este instalador não tem suporte a {info['nome']}.\n"
        "O que ele instala nos sistemas suportados, para você instalar à mão:\n"
        f"  - PHP {php['aceita_de']} a {php['aceita_ate']}, com as extensões mysqli, pdo_mysql e mbstring;\n"
        f"  - MariaDB {maria['aceita_de']} ou mais novo, com o usuário root local sem senha;\n"
        f"  - Python {py['aceita_de']} ou mais novo, com o módulo venv;\n"
        "  - as bibliotecas de sistema do Chromium do Playwright;\n"
        "  - o Ollama (https://ollama.com/download).\n"
        "Sistemas suportados: Ubuntu 22.04, 24.04 e 26.04; Debian 12 e 13; Fedora, como melhor esforço."
    )


def detectar() -> dict:
    """A família do sistema em que este processo roda."""
    sistema = platform.system()
    arquivo = Path("/etc/os-release")
    dados = ler_os_release(arquivo.read_text(encoding="utf-8", errors="replace")) if sistema == "Linux" and arquivo.exists() else None
    return familia(sistema, dados, tem_brew=bool(shutil.which("brew")), maquina=platform.machine())
