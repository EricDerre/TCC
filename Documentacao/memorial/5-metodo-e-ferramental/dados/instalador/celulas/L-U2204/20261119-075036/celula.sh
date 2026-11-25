#!/usr/bin/env bash
# Gerado por ferramentas/instalador_matriz/celula_wsl.ps1. Partes: preparo (root), usuario (cobaia), copia (root).
PARTE="$1"
case "$PARTE" in
preparo)
    # O estado da imagem antes de qualquer coisa, e o usuario comum com sudo sem senha.
    mkdir -p /root/evidencia
    cp /etc/os-release /root/evidencia/os-release.txt
    (systemctl is-system-running 2>&1 || true) > /root/evidencia/systemd.txt
    (python3 --version 2>&1 || echo "sem python3") > /root/evidencia/python3.txt
    (command -v sudo || echo "sem sudo") > /root/evidencia/sudo.txt
    # O WSL acrescenta o PATH do Windows ao da instancia; um Linux de verdade nao tem isso. Desliga antes de criar o usuario
    # (a configuracao vale depois do wsl --terminate que o celula_wsl.ps1 faz logo apos esta parte).
    if [ -f /etc/wsl.conf ]; then cp /etc/wsl.conf /root/evidencia/wsl-conf-original.txt; else echo "sem wsl.conf" > /root/evidencia/wsl-conf-original.txt; fi
    if ! grep -qs appendWindowsPath /etc/wsl.conf; then
        if grep -qs '^\[interop\]' /etc/wsl.conf; then
            sed -i '/^\[interop\]/a appendWindowsPath=false' /etc/wsl.conf
        else
            printf '\n[interop]\nappendWindowsPath=false\n' >> /etc/wsl.conf
        fi
    fi
    # Celula sem o systemd (suspeita HL7): o estado original ja ficou em systemd.txt e em wsl-conf-original.txt.
    if [ "$2" = "sem-systemd" ]; then
        if grep -qs '^systemd' /etc/wsl.conf; then
            sed -i 's/^systemd.*/systemd=false/' /etc/wsl.conf
        elif grep -qs '^\[boot\]' /etc/wsl.conf; then
            sed -i '/^\[boot\]/a systemd=false' /etc/wsl.conf
        else
            printf '\n[boot]\nsystemd=false\n' >> /etc/wsl.conf
        fi
    fi
    cp /etc/wsl.conf /root/evidencia/wsl-conf-usado.txt
    FALHAS=0
    id cobaia >/dev/null 2>&1 || useradd -m -s /bin/bash cobaia || FALHAS=$((FALHAS + 1))
    mkdir -p /etc/sudoers.d || FALHAS=$((FALHAS + 1))
    echo 'cobaia ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/cobaia || FALHAS=$((FALHAS + 1))
    chmod 440 /etc/sudoers.d/cobaia || FALHAS=$((FALHAS + 1))
    echo "$FALHAS" > /root/evidencia/saida_preparo.txt
    ;;
usuario)
    ID="$2"; ATE="$3"; MODELO="$4"; PACOTE="$5"
    EVID="$HOME/evidencia"
    mkdir -p "$EVID"
    tar xzf "$PACOTE" -C "$HOME"
    echo $? > "$EVID/saida_abrir_pacote.txt"
    cd "$HOME/TCC-main" || exit 90
    # ! Alteracao de IA - Revisar: (pacote I2, tarefa 5) exporta as duas variaveis que o instalador novo le, antes do ./install.sh.
    # ! Motivo: sem terminal o instalador novo nao pergunta se troca a entrada do root do MariaDB e para; e sem a variavel do
    # modelo ele baixa o qwen2.5:7b (4,7 GB) mesmo numa celula que so vai ate o N3.
    # O que a pessoa responderia: aceita a troca do root do MariaDB e, abaixo do N4, escolhe o modelo pequeno.
    export COBAIA_ROOT_SEM_SENHA=1
    [ "$ATE" = "N4" ] || export COBAIA_MODELO_LLM="$MODELO"
    # Primeiro o que o README manda; se faltar a permissao de execucao (codigo 126), pelo bash.
    # instalacao.log e sempre o log da rodada que executou o instalador; a chamada direta grava antes em instalacao_direto.log.
    (timeout 5400 ./install.sh) > "$EVID/instalacao_direto.log" 2>&1 < /dev/null
    DIRETO=$?
    echo "$DIRETO" > "$EVID/saida_install_direto.txt"
    if [ "$DIRETO" -eq 126 ]; then
        (timeout 5400 bash install.sh) > "$EVID/instalacao.log" 2>&1 < /dev/null
        echo $? > "$EVID/saida_install_bash.txt"
    else
        mv "$EVID/instalacao_direto.log" "$EVID/instalacao.log"
    fi
    # A prova, com o Python que o instalador trouxe ou com o do sistema.
    PY=$(ls .ferramentas/python/*/bin/python3 2>/dev/null | head -n 1)
    [ -n "$PY" ] || PY=$(command -v python3)
    if [ -z "$PY" ]; then
        echo "sem Python para rodar a prova" > "$EVID/conferir.log"
        echo 97 > "$EVID/saida_conferir.txt"
    else
        # ! Alteração de IA - Revisar: (pacote I2) o limite de duas horas da prova passa a interromper com `-s INT`.
        # ! Motivo: o `timeout` sem `-s` manda SIGTERM, que mata o Python sem passar pelo `finally` do `main` de
        # instalador/conferir.py, e a celula ficava sem registro.json; com a interrupcao do teclado o registro e gravado
        # e os servicos sao desligados antes de o processo sair.
        timeout -s INT 7200 "$PY" -m instalador.conferir --celula "$ID" --saida "$EVID" --ate "$ATE" --modelo-pequeno "$MODELO" > "$EVID/conferir.log" 2>&1 < /dev/null
        echo $? > "$EVID/saida_conferir.txt"
    fi
    ;;
suspeitas)
    # As sondas das suspeitas HL1 a HL11, depois do instalador e da prova: cada uma grava o comando e a saida literal
    # em evidencia/suspeitas/HLn.txt. O roteiro vem no pacote (ferramentas/instalador_matriz/sondas_suspeitas.sh).
    CLONE_SH="$2"
    # ! Alteracao de IA - Revisar: (pacote I2, tarefa 5) procura as sondas primeiro ao lado deste celula.sh (copia gravada na evidencia).
    # ! Motivo: as rodadas como-esta das outras distribuicoes usam o pacote de 18/11, que traz as sondas daquele dia; com a copia
    # na pasta de evidencia, a sonda que mudar depois vale tambem para elas.
    SONDAS="$(dirname "$0")/sondas_suspeitas.sh"
    [ -f "$SONDAS" ] || SONDAS="$HOME/TCC-main/ferramentas/instalador_matriz/sondas_suspeitas.sh"
    if [ -f "$SONDAS" ]; then
        timeout 5400 bash "$SONDAS" "$HOME/TCC-main" "$HOME/evidencia/suspeitas" "$HOME/evidencia" "$CLONE_SH" > "$HOME/evidencia/sondas.log" 2>&1 < /dev/null
        echo $? > "$HOME/evidencia/saida_sondas.txt"
    else
        echo "o pacote nao traz $SONDAS" > "$HOME/evidencia/sondas.log"
        echo 96 > "$HOME/evidencia/saida_sondas.txt"
    fi
    ;;
copia)
    DESTINO="$2"
    cp -r /root/evidencia/. "$DESTINO/"
    cp -r /home/cobaia/evidencia/. "$DESTINO/"
    ;;
*)
    echo "parte desconhecida: $PARTE" >&2
    exit 64
    ;;
esac
