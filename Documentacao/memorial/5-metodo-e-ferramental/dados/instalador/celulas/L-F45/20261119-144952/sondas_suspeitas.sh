#!/usr/bin/env bash
# ! Alteração de IA - Revisar: arquivo novo (pacote I2 do instalador único): as sondas das suspeitas HL1 a HL11 do plano
# aprovado (seção 1.3 e desvio 4). Roda dentro da célula de Linux, como o usuário comum, depois do instalador e da prova, e
# grava em <saída>/HLn.txt o comando, a saída literal e o código de saída de cada teste.
# ! Motivo: o install.py para no primeiro erro, e a rodada `como-esta` só mostraria esse; cada suspeita escondida atrás dele
# custaria mais uma rodada na janela do Eric. Cada sonda repete o comando que o instalador (ou o run.py) usaria e, quando
# precisa passar de uma falha para testar a seguinte, aplica o contorno que uma pessoa aplicaria e deixa o contorno escrito
# no arquivo. Nada aqui conserta o instalador: é a evidência que decide quais consertos entram.
# Uso: bash sondas_suspeitas.sh <repositório extraído> <pasta de saída> <pasta da evidência> [install.sh do clone do Windows]
REPO="$1"; SAIDA="$2"; EVID="$3"; CLONE_SH="${4:-}"
mkdir -p "$SAIDA" "$HOME/sonda"
cd "$REPO" || exit 90
PY=$(command -v python3 || command -v python || true)
CLI=$(command -v mariadb || command -v mysql || true)
PHP=$(command -v php || true)
LIMITE=600

# sonda <HLn> <o que testa> <comando...>: grava o comando, a saída e o código de saída em <saída>/<HLn>.txt.
sonda() {
    local arquivo="$SAIDA/$1.txt" rotulo="$2" codigo
    shift 2
    {
        echo "### $rotulo"
        echo "\$ $*"
        timeout "$LIMITE" "$@" 2>&1 < /dev/null
        codigo=$?
        echo "[codigo de saida: $codigo]"
        echo
    } >> "$arquivo"
    return "$codigo"
}

# nota <HLn> <texto>: uma linha no arquivo da suspeita (por que uma sonda não rodou, que contorno foi aplicado).
nota() { printf '### %s\n\n' "$2" >> "$SAIDA/$1.txt"; }

banco_rodando() { ps -eo args 2>/dev/null | grep -Eq '[m]ariadbd|[m]ysqld'; }

EXTENSOES='foreach (["mysqli", "pdo_mysql", "mbstring"] as $x) { echo $x, ": ", extension_loaded($x) ? "carregada" : "NAO carregada", "\n"; }'

# Os dois roteiros de Python das sondas vão para arquivo, para o comando gravado em HLn.txt caber numa linha.
BUSCA="$HOME/sonda/buscar_pagina.py"
ABRIR="$HOME/sonda/abrir_chromium.py"
cat > "$BUSCA" <<'FIM_DA_BUSCA'
import re, sys, urllib.error, urllib.request
try:
    with urllib.request.urlopen(sys.argv[1], timeout=30) as r:
        status, corpo = r.status, r.read().decode("utf-8", "replace")
except urllib.error.HTTPError as e:
    status, corpo = e.code, e.read().decode("utf-8", "replace")
print("HTTP", status, "com", len(corpo), "caracteres")
erros = re.findall(r"(?:Fatal error|Warning|Uncaught|ERRO)[^\n]{0,400}", corpo)
print("\n".join(erros[:5]) if erros else "nenhum Fatal error, Warning ou ERRO na pagina")
FIM_DA_BUSCA
cat > "$ABRIR" <<'FIM_DO_ABRIR'
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    navegador = p.chromium.launch(headless=True)
    print("o Chromium abriu, versao", navegador.version)
    navegador.close()
FIM_DO_ABRIR

# pagina <HLn> <porta> <o que testa> <opções do php...>: sobe o `php -S` como o run.py sobe, pede produtos_geral.php e
# mostra os erros da página e o que o servidor escreveu.
pagina() {
    local suspeita="$1" porta="$2" rotulo="$3" servidor
    local registro_do_php="$SAIDA/php_servidor_$2.log"
    shift 3
    "$PHP" -S "localhost:$porta" -t Programacao/CobaiaFront "$@" > "$registro_do_php" 2>&1 < /dev/null &
    servidor=$!
    sleep 3
    sonda "$suspeita" "$rotulo" "$PY" "$BUSCA" "http://localhost:$porta/produtos_geral.php"
    kill "$servidor" 2>/dev/null
    wait "$servidor" 2>/dev/null
    sonda "$suspeita" "o que o php -S escreveu ($rotulo)" tail -n 15 "$registro_do_php"
}

# ---- HL1: ./install.sh sem permissão de execução (a chamada direta fica em instalacao_direto.log, feita pelo celula.sh)
sonda HL1 "modo do install.sh e do run.sh no pacote (644 = sem permissao de execucao)" stat -c '%a %n' install.sh run.sh

# ---- HL3: distribuição sem apt-get
sonda HL3 "gerenciadores de pacote que a distribuicao tem" bash -c 'for g in apt-get dnf pacman zypper apk; do command -v "$g" || echo "sem $g"; done'

# ---- HL7: sem o systemd, o serviço não sobe e o plano B (servidor direto, como usuário comum) também não
sonda HL7 "o systemd esta no ar? (processo 1 e estado)" bash -c 'cat /proc/1/comm; systemctl is-system-running 2>&1'
sonda HL7 "servico mariadb" bash -c 'systemctl is-enabled mariadb 2>&1; systemctl is-active mariadb 2>&1'
sonda HL7 "processos do banco" bash -c 'ps -eo user,pid,args 2>/dev/null | grep -E "[m]ariadbd|[m]ysqld" || echo "nenhum mariadbd rodando"'
SERVIDOR=$(command -v mariadbd || command -v mysqld || true)
if [ -z "$SERVIDOR" ]; then
    nota HL7 "plano B nao testado: o servidor do MariaDB nao esta instalado"
elif banco_rodando; then
    nota HL7 "plano B nao testado nesta celula: o servico do sistema ja deixou o banco no ar"
else
    LIMITE=25 sonda HL7 "plano B do _env_common: o servidor direto, como usuario comum (25 s; codigo 124 = ficou no ar)" "$SERVIDOR"
    sonda HL7 "contorno para as sondas seguintes: sudo service mariadb start" sudo service mariadb start
    sleep 5
fi

# ---- HL10: o root do MariaDB entra por unix_socket; o conserto do instalador (ALTER USER pelo sudo) nunca rodou
if [ -n "$CLI" ]; then
    sonda HL10 "root sem senha pelo usuario comum, como o _can_connect do _env_common" "$CLI" -u root -e "SELECT 1;"
    sonda HL10 "como o root local esta cadastrado no servidor" sudo "$CLI" -u root -e "SHOW GRANTS FOR 'root'@'localhost';"
    if [ -n "$PY" ]; then
        sonda HL10 "o conserto que o instalador tenta (_env_common.ensure_root_no_password)" "$PY" -c 'import _env_common as e; print("ensure_root_no_password devolveu", e.ensure_root_no_password(e.find_mysql_cli()))'
    fi
    if ! "$CLI" -u root -e "SELECT 1;" >/dev/null 2>&1; then
        sonda HL10 "o mesmo SQL do conserto, com o erro a vista" sudo "$CLI" -u root -e "ALTER USER 'root'@'localhost' IDENTIFIED VIA mysql_native_password USING PASSWORD(''); FLUSH PRIVILEGES;"
    fi
    sonda HL10 "root sem senha depois do conserto" "$CLI" -u root -e "SELECT 1;"
    sonda HL10 "como o root local ficou cadastrado" sudo "$CLI" -u root -e "SHOW GRANTS FOR 'root'@'localhost';"
    sonda HL10 "root sem senha pela rede local (127.0.0.1:3306, por onde a CobaiaAPI entra)" "$CLI" -u root -h 127.0.0.1 -P 3306 --protocol=TCP -e "SELECT CURRENT_USER();"
else
    nota HL10 "nao rodou: o cliente do MariaDB nao esta instalado"
fi

# ---- HL4 e HL11: as opções que o run.py passa ao php (pasta de extensões do Windows) e a falta do php-mbstring
OPCOES=()
if [ -n "$PHP" ]; then
    sonda HL11 "pacotes do PHP que o instalador deixou" bash -c 'dpkg-query -W -f "\${Package} \${Version}\n" "php*" 2>/dev/null || rpm -qa "php*" 2>/dev/null || echo "sem dpkg e sem rpm"'
    sonda HL11 "extensoes que o php carrega sozinho" "$PHP" -r "$EXTENSOES"
    sonda HL4 "pasta de extensoes do php (extension_dir)" "$PHP" -r 'echo ini_get("extension_dir"), "\n";'
    if [ -n "$PY" ]; then
        mapfile -t OPCOES < <("$PY" -c 'import _env_common as e; print("\n".join(e.php_extension_flags(e.find_php())))')
        sonda HL4 "extensoes com as opcoes que o run.py passa (_env_common.php_extension_flags)" "$PHP" "${OPCOES[@]}" -r "$EXTENSOES"
    fi
else
    nota HL4 "nao rodou: o php nao esta instalado"
    nota HL11 "nao rodou: o php nao esta instalado"
fi
if [ -n "$PHP" ] && [ -n "$PY" ] && [ -n "$CLI" ] && "$CLI" -u root -e "SELECT 1;" >/dev/null 2>&1; then
    sonda HL11 "aplicar os .sql como o instalador (install.apply_sql_files)" "$PY" -c 'import install, _env_common as e; install.apply_sql_files(e.find_mysql_cli())'
    pagina HL4 8080 "produtos_geral.php com as opcoes que o run.py passa" "${OPCOES[@]}"
    pagina HL11 8081 "produtos_geral.php sem as opcoes de extensao (so o output_buffering)" -d output_buffering=4096
elif [ -n "$PHP" ]; then
    nota HL4 "a pagina do site nao foi testada: falta python3, o cliente do banco ou o root do banco sem senha"
    nota HL11 "a pagina do site nao foi testada: falta python3, o cliente do banco ou o root do banco sem senha"
fi

# ---- HL2: python3 presente e sem o python3-venv
if [ -n "$PY" ]; then
    sonda HL2 "o Python que o install.sh usaria" "$PY" --version
    sonda HL2 "o pacote python3-venv esta instalado?" bash -c 'dpkg-query -W -f "\${Status} \${Version}\n" python3-venv 2>&1 || true'
    if sonda HL2 "criar a venv como o install.py faz (python -m venv)" "$PY" -m venv "$HOME/sonda/venv"; then
        nota HL2 "a venv foi criada sem contorno"
    elif command -v apt-get >/dev/null 2>&1; then
        rm -rf "$HOME/sonda/venv"
        LIMITE=900 sonda HL2 "contorno para as sondas seguintes: sudo apt-get install -y python3-venv" sudo apt-get install -y python3-venv
        sonda HL2 "criar a venv depois do contorno" "$PY" -m venv "$HOME/sonda/venv"
    fi
else
    nota HL2 "nao rodou: nao ha python3 nem python no PATH"
fi

# ---- HL6: o `playwright install chromium` não instala as bibliotecas do sistema
VENV_PY="$HOME/sonda/venv/bin/python"
if [ -x "$VENV_PY" ]; then
    FIXADO=$(grep -E '^playwright==' Programacao/AgenteCore/requirements.txt | head -n 1)
    LIMITE=900 sonda HL6 "instalar o Playwright fixado numa venv so da sonda" "$VENV_PY" -m pip install --quiet --disable-pip-version-check "$FIXADO"
    LIMITE=1800 sonda HL6 "baixar o Chromium como o install.py faz (playwright install chromium, sem --with-deps)" "$VENV_PY" -m playwright install chromium
    sonda HL6 "abrir o Chromium sem janela" "$VENV_PY" "$ABRIR"
    sonda HL6 "bibliotecas de sistema que faltam ao Chromium (ldd)" bash -c 'achou=0; for b in $(find "$HOME/.cache/ms-playwright" -type f \( -name chrome -o -name headless_shell -o -name chrome-headless-shell \) 2>/dev/null); do echo "$b"; ldd "$b" | grep "not found" && achou=1; done; [ "$achou" = 1 ] || echo "nenhuma biblioteca faltando"'
else
    nota HL6 "nao rodou: nao foi possivel criar a venv da sonda (ver HL2)"
fi

# ---- HL5: o Ollama não é instalado no Linux, e a instalação termina dizendo que concluiu
sonda HL5 "o ollama esta no PATH?" bash -c 'command -v ollama || echo "sem ollama no PATH"'
if [ -n "$PY" ]; then
    sonda HL5 "o que o install.ensure_ollama faz no Linux" "$PY" -c 'import install; print("ensure_ollama devolveu:", install.ensure_ollama())'
fi
sonda HL5 "a rodada do instalador chegou a Instalacao concluida?" bash -c 'grep -n "Instalação concluída" "$0"/instalacao*.log || echo "nenhum log da rodada tem a linha de conclusao"' "$EVID"

# ---- HL8: o Python 3.10 ou 3.11 da distribuição compila os arquivos do projeto?
if [ -n "$PY" ]; then
    sonda HL8 "compilar os .py do projeto com o Python do sistema (so os erros aparecem)" "$PY" -m compileall -q -x '[/]\.venv[/]' Programacao/AgenteCore Programacao/CobaiaAPI ferramentas instalador
    sonda HL8 "compilar os .py da raiz" "$PY" -m py_compile install.py _env_common.py run.py restaurar_banco.py Cobaia.py testar_instalador.py
else
    nota HL8 "nao rodou: nao ha python3 nem python no PATH"
fi

# ---- HL9: o install.sh com o fim de linha do Windows (CRLF), como fica num clone feito no Windows e usado pelo WSL
mkdir -p "$HOME/sonda/crlf"
printf 'print("install.py de mentira: o lancador chegou ate o fim")\n' > "$HOME/sonda/crlf/install.py"
sed 's/$/\r/' install.sh > "$HOME/sonda/crlf/install.sh"
chmod +x "$HOME/sonda/crlf/install.sh"
sonda HL9 "comeco do install.sh do pacote, como o git entrega" od -c -N 24 install.sh
if [ -n "$CLONE_SH" ] && [ -f "$CLONE_SH" ]; then
    sonda HL9 "comeco do install.sh do clone do Windows (so leitura; nunca executado)" od -c -N 24 "$CLONE_SH"
fi
sonda HL9 "bash install.sh com o fim de linha do Windows (install.py de mentira ao lado)" bash "$HOME/sonda/crlf/install.sh"
sonda HL9 "./install.sh com o fim de linha do Windows" "$HOME/sonda/crlf/install.sh"

echo "sondas terminadas"
