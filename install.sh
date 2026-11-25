#!/usr/bin/env bash
# ! Alteração de IA - Revisar: bootstrap fino (Linux/macOS) que só garante a existência
# de um Python 3 e então delega toda a instalação para install.py.
# ! Motivo: mesmo papel do install.ps1 no Windows - install.py concentra a lógica real,
# mas precisa de um Python que pode não existir na máquina. Manter aqui só essa checagem
# evita duplicar a instalação em três linguagens de shell diferentes.
# ! Alteração de IA - Revisar: (19/11/2026, pacote I2 do instalador único, decisão 140) o lançador procura um Python 3.12 ou
# mais novo que rode de verdade; se não acha, baixa o `uv` fixado em instalador/uv_fixado.txt, confere o SHA-256, instala o
# Python em .ferramentas/python (dentro do projeto) e chama o núcleo provisório, `python -m instalador.nucleo`.
# ! Motivo: o lançador antigo aceitava qualquer `python3` (o 3.10 do Ubuntu 22.04 não é versão que o projeto testa) e, sem
# Python, chamava `apt-get install python3 python3-venv python3-pip` ou `brew install python3`, cada um num sistema só. Na
# célula L-U2404 de 18/11/2026 o `install.py` chamado por ele parou em "Não foi possível subir o MariaDB"; como o
# `install.py` não pode mudar antes de a corrida 28b ser lida, a chamada vai para `instalador/nucleo.py` até o pacote I3.
# ! Alteração de IA - Revisar: (19/11/2026, pacote I3 do instalador único) o lançador volta a chamar o `install.py` (a última linha passa de `python -m instalador.nucleo` para `python install.py`).
# ! Motivo: os consertos de Linux que moravam no núcleo provisório `instalador/nucleo.py` entraram no `install.py` depois de a corrida 28b ser lida, e o módulo provisório deixou de existir.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FIXADO="$SCRIPT_DIR/instalador/uv_fixado.txt"
FERRAMENTAS="$SCRIPT_DIR/.ferramentas"

aviso() { echo "[install.sh] $*"; }

# Lê CHAVE=valor de instalador/uv_fixado.txt. O `tr` tira o \r de um clone feito no Windows; o `|| true` deixa a chave
# que falta virar texto vazio em vez de derrubar o roteiro (o `set -e` vale dentro do `$(...)`).
valor() { grep -E "^$1=" "$FIXADO" | head -n 1 | cut -d= -f2- | tr -d '\r' || true; }

if [ ! -f "$FIXADO" ]; then
    aviso "Não achei $FIXADO: a pasta do projeto está incompleta."
    exit 1
fi
PYTHON_MINIMO="$(valor PYTHON_MINIMO)"
PYTHON_VERSAO="$(valor PYTHON_VERSAO)"
UV_VERSAO="$(valor UV_VERSAO)"
if [ -z "$PYTHON_MINIMO" ] || [ -z "$PYTHON_VERSAO" ] || [ -z "$UV_VERSAO" ]; then
    aviso "$FIXADO não tem PYTHON_MINIMO, PYTHON_VERSAO e UV_VERSAO."
    exit 1
fi

# Um Python serve se roda de verdade e é o PYTHON_MINIMO ou mais novo.
python_serve() {
    "$1" -c "import sys; minimo = tuple(int(p) for p in '$PYTHON_MINIMO'.split('.')); sys.exit(0 if sys.version_info[:2] >= minimo else 1)" >/dev/null 2>&1
}

# O Python que uma rodada anterior trouxe pelo uv, se houver.
python_do_projeto() { ls "$FERRAMENTAS"/python/*/bin/python3 2>/dev/null | head -n 1 || true; }

achar_python() {
    local candidato
    if [ "${COBAIA_FORCAR_UV:-0}" != "1" ]; then
        for candidato in python3 python; do
            if command -v "$candidato" >/dev/null 2>&1 && python_serve "$candidato"; then
                command -v "$candidato"
                return 0
            fi
        done
    fi
    candidato="$(python_do_projeto)"
    if [ -n "$candidato" ] && python_serve "$candidato"; then
        echo "$candidato"
        return 0
    fi
    return 1
}

# A chave do uv_fixado.txt para este sistema e este processador.
alvo_do_uv() {
    case "$(uname -s)-$(uname -m)" in
        Linux-x86_64) echo "LINUX_X86_64" ;;
        Linux-aarch64 | Linux-arm64) echo "LINUX_AARCH64" ;;
        Darwin-arm64) echo "MACOS_AARCH64" ;;
        Darwin-x86_64) echo "MACOS_X86_64" ;;
        *) return 1 ;;
    esac
}

# ! Alteração de IA - Revisar: (19/11/2026, decisão 148, ficha 88) sem curl nem wget numa distribuição de apt, o lançador
# instala o curl e segue; nas outras, diz o que instalar.
# ! Motivo: célula L-D13 de 19/11/2026: a imagem do Debian 13 para o WSL vem sem python3, sem curl e sem wget. O lançador
# antigo instalava o Python pelo apt sozinho; este precisa de um dos dois para baixar o uv e pararia pedindo o curl, um
# passo manual que antes não existia. O instalador usa o mesmo `sudo apt-get` logo depois, para o PHP e o MariaDB.
garantir_baixador() {
    local raiz=""
    if command -v curl >/dev/null 2>&1 || command -v wget >/dev/null 2>&1; then
        return 0
    fi
    if ! command -v apt-get >/dev/null 2>&1; then
        aviso "Para baixar o Python é preciso o curl ou o wget, e esta máquina não tem nenhum dos dois."
        aviso "Instale um deles (no Fedora: sudo dnf install -y curl) e rode de novo."
        return 1
    fi
    if [ "$(id -u)" != "0" ]; then
        if ! command -v sudo >/dev/null 2>&1; then
            aviso "Para baixar o Python é preciso o curl, e esta máquina não tem o curl nem o sudo para instalá-lo."
            aviso "Como root, rode: apt-get install -y sudo curl ca-certificates. Depois rode o instalador de novo, como usuário comum."
            return 1
        fi
        raiz="sudo"
    fi
    aviso "Esta máquina não tem curl nem wget: instalando o curl pelo apt..."
    $raiz apt-get update || aviso "O apt-get update saiu com erro; seguindo."
    $raiz env DEBIAN_FRONTEND=noninteractive apt-get install -y curl ca-certificates
}

baixar() {
    if command -v curl >/dev/null 2>&1; then
        curl -fsSL --retry 3 -o "$2" "$1"
    elif command -v wget >/dev/null 2>&1; then
        wget -q -O "$2" "$1"
    else
        return 1
    fi
}

sha256_de() {
    if command -v sha256sum >/dev/null 2>&1; then
        sha256sum "$1" | cut -d' ' -f1
    else
        shasum -a 256 "$1" | cut -d' ' -f1
    fi
}

trazer_python_pelo_uv() {
    local alvo url esperado achado pacote uv
    if ! alvo="${COBAIA_UV_ALVO:-$(alvo_do_uv)}"; then
        aviso "Não há uv fixado para $(uname -s) $(uname -m). Instale o Python $PYTHON_MINIMO ou mais novo e rode de novo."
        return 1
    fi
    url="$(valor "UV_${alvo}_URL")"
    esperado="$(valor "UV_${alvo}_SHA256")"
    if [ -z "$url" ] || [ -z "$esperado" ]; then
        aviso "$FIXADO não tem o endereço e o SHA-256 do uv para $alvo."
        return 1
    fi
    uv="$(find "$FERRAMENTAS/uv" -type f -name uv 2>/dev/null | head -n 1 || true)"
    if [ -z "$uv" ]; then
        garantir_baixador || return 1
        mkdir -p "$FERRAMENTAS/uv"
        pacote="$FERRAMENTAS/uv/uv-$UV_VERSAO.tar.gz"
        aviso "Python $PYTHON_MINIMO ou mais novo não encontrado: baixando o uv $UV_VERSAO de $url"
        baixar "$url" "$pacote" || return 1
        achado="$(sha256_de "$pacote")"
        if [ "$achado" != "$esperado" ]; then
            rm -f "$pacote"
            aviso "O SHA-256 do uv baixado ($achado) não é o esperado ($esperado); o arquivo foi apagado. Rode de novo."
            return 1
        fi
        tar -xzf "$pacote" -C "$FERRAMENTAS/uv"
        rm -f "$pacote"
        uv="$(find "$FERRAMENTAS/uv" -type f -name uv | head -n 1 || true)"
        if [ -z "$uv" ]; then
            aviso "O pacote do uv não trouxe o executável uv."
            return 1
        fi
        chmod +x "$uv"
    fi
    aviso "Instalando o Python $PYTHON_VERSAO em $FERRAMENTAS/python (dentro do projeto; nada muda no sistema)..."
    UV_PYTHON_INSTALL_DIR="$FERRAMENTAS/python" UV_PYTHON_INSTALL_BIN=0 UV_PYTHON_BIN_DIR="$FERRAMENTAS/bin" \
        UV_CACHE_DIR="$FERRAMENTAS/uv/cache" UV_NO_CONFIG=1 UV_NO_PROGRESS=1 \
        "$uv" python install "$PYTHON_VERSAO"
}

if ! PY="$(achar_python)"; then
    trazer_python_pelo_uv || exit 1
    PY="$(python_do_projeto)"
    if [ -z "$PY" ] || ! python_serve "$PY"; then
        aviso "O Python instalado pelo uv não rodou. As mensagens acima dizem o que houve; rode de novo."
        exit 1
    fi
fi
aviso "Python: $PY ($("$PY" --version 2>&1))"
cd "$SCRIPT_DIR"
exec "$PY" "$SCRIPT_DIR/install.py" ${1+"$@"}
