# ! Alteração de IA - Revisar: arquivo novo (pacote I1 do instalador único, decisão 141): cria uma instância limpa do WSL a
# partir da imagem oficial de uma distribuição, roda nela o instalador como uma pessoa rodaria, roda a prova da instalação,
# copia a evidência para o Memorial e apaga a instância.
# ! Motivo: o instalador nunca rodou em Linux. O Eric pediu o teste em máquina recém-criada, e o plano aprovado (decisão 143)
# pede a falha gravada antes de qualquer conserto; sem um roteiro que repita os mesmos passos em cada distribuição, cada célula
# seria montada à mão e as evidências não seriam comparáveis. Roda na janela do PowerShell do Eric, nunca de dentro do
# aplicativo Claude, e recusa se houver corrida rodando.
# ! Alteração de IA - Revisar: comentário sobre `-Modo`.
# ! Motivo: o parâmetro parecia mudar o que a célula roda. Não muda: `-Modo` só é gravado no celula.json, para a leitura saber
# se a célula rodou o instalador como estava (`como-esta`) ou depois dos consertos (`novo`).
param(
    [Parameter(Mandatory = $true)][string]$Id,
    [Parameter(Mandatory = $true)][string]$Imagem,
    [ValidateSet("como-esta", "novo")][string]$Modo = "como-esta",
    [ValidateSet("N1", "N2", "N3", "N4")][string]$Ate = "N3",
    [string]$ModeloPequeno = "qwen2.5:0.5b",
    [string]$Pacote = "",
    [string]$PastaInstancias = (Join-Path $env:USERPROFILE "cobaia-celulas"),
    [switch]$ManterInstancia,
    # ! Alteração de IA - Revisar: (pacote I2) dois interruptores novos. `-SemSondas` pula as sondas das suspeitas, que por
    # padrão rodam só no modo `como-esta`; `-SemSystemd` desliga o systemd da instância antes de o instalador rodar.
    # ! Motivo: o install.py para no primeiro erro e a rodada `como-esta` escondia as outras suspeitas (ver
    # sondas_suspeitas.sh); e a suspeita HL7 (sem o systemd o serviço do MariaDB não sobe) não tem como aparecer numa imagem
    # que já vem com o systemd ligado, como a do Ubuntu.
    [switch]$SemSondas,
    [switch]$SemSystemd,
    [switch]$Simular
)
$ErrorActionPreference = "Stop"
$env:WSL_UTF8 = "1"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$Raiz = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$Carimbo = Get-Date -Format "yyyyMMdd-HHmmss"
$Nome = "cobaia-$Id-$Carimbo"
$Evidencia = Join-Path $Raiz "Documentacao\memorial\5-metodo-e-ferramental\dados\instalador\celulas\$Id\$Carimbo"
$Instancia = Join-Path $PastaInstancias $Nome

# O que roda dentro da instancia. Texto literal: o PowerShell nao troca nada aqui dentro.
$RoteiroDaCelula = @'
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
    # ! Alteracao de IA - Revisar: (pacote I2) o bloco abaixo grava `systemd=false` no /etc/wsl.conf quando o segundo argumento e `sem-systemd`.
    # ! Motivo: a suspeita HL7 (sem o systemd o servico do MariaDB nao sobe) nao aparece numa imagem que ja vem com o systemd ligado,
    # como a do Ubuntu; a celula precisa desligar o systemd da instancia antes de o instalador rodar.
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
'@

function Write-Passo([string]$Texto) { Write-Host "[celula $Id] $Texto" }

function ConvertTo-CaminhoWsl([string]$Caminho) {
    $completo = [System.IO.Path]::GetFullPath($Caminho)
    return "/mnt/" + $completo.Substring(0, 1).ToLower() + ($completo.Substring(2) -replace "\\", "/")
}

function Invoke-Parte([string]$Usuario, [string[]]$Argumentos) {
    Write-Passo ("wsl -d $Nome -u $Usuario -- bash $roteiroWsl " + ($Argumentos -join " "))
    if ($Simular) { return }
    & wsl -d $Nome -u $Usuario -- bash $roteiroWsl @Argumentos | Out-Host
}

# 1. Nada pesado enquanto uma corrida roda.
$corridas = @(Get-CimInstance Win32_Process -Filter "Name='python.exe'" |
    Where-Object { $_.CommandLine -match "executar_fase|experimento_|linha_de_base_manual|avaliar_fase|sonda_" })
# ! Alteração de IA - Revisar: a recusa também enxerga os lançadores da noite (powershell/pwsh com rodar_fase, rodar_fila, etc.).
# ! Motivo: entre duas etapas de uma corrida não há python.exe da corrida rodando, e a célula começava no intervalo.
$lancadores = @(Get-CimInstance Win32_Process -Filter "Name='powershell.exe' OR Name='pwsh.exe'" |
    Where-Object { $_.CommandLine -match "rodar_fase|rodar_fila|rodar_experimento|rodar_sonda|rodar_pendencias|rodar_fumaca" })
$corridas = @($corridas) + @($lancadores)
if ($corridas.Count -gt 0) { throw "ha uma corrida rodando nesta maquina ($($corridas.Count) processo(s)); a celula nao roda agora" }
$livreGb = [math]::Round((Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory / 1MB, 1)
if ($livreGb -lt 4) { throw "so $livreGb GB de memoria livre; feche o aplicativo Claude e o VS Code e tente de novo" }
if (-not (Test-Path $Imagem)) { throw "imagem nao encontrada: $Imagem" }
if ($Evidencia -match " " -or $Raiz -match " ") { throw "o caminho do repositorio tem espaco, e o roteiro nao trata isso: $Raiz" }

# 2. O pacote que entra na celula.
if (-not $Pacote) {
    $Pacote = Join-Path $Raiz ".ferramentas\pacote\cobaia-pacote.tar.gz"
    Write-Passo "python ferramentas\instalador_matriz\empacotar.py"
    if (-not $Simular) {
        & python (Join-Path $Raiz "ferramentas\instalador_matriz\empacotar.py")
        if ($LASTEXITCODE -ne 0) { throw "o empacotador saiu com erro" }
        if (-not (Test-Path $Pacote)) { throw "o empacotador nao gerou $Pacote" }
    }
}
# ! Alteração de IA - Revisar: confere o pacote antes do wsl --import.
# ! Motivo: com -Pacote inexistente, o erro só aparecia no finally (Get-FileHash), depois de a instância já existir.
elseif (-not (Test-Path $Pacote)) { throw "pacote nao encontrado: $Pacote" }

# 3. A instancia limpa e o roteiro dela.
$roteiroWsl = (ConvertTo-CaminhoWsl $Evidencia) + "/celula.sh"
Write-Passo "wsl --import $Nome $Instancia $Imagem --version 2"
$inicio = Get-Date
if (-not $Simular) {
    New-Item -ItemType Directory -Force -Path $Evidencia, $PastaInstancias | Out-Null
    $semBom = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText((Join-Path $Evidencia "celula.sh"), ($RoteiroDaCelula -replace "`r`n", "`n") + "`n", $semBom)
    # ! Alteração de IA - Revisar: (pacote I2, tarefa 5) grava também uma cópia de sondas_suspeitas.sh na pasta de evidência, ao lado do celula.sh.
    # ! Motivo: as rodadas como-esta das outras distribuições usam o pacote guardado de 18/11/2026, que traz as sondas daquele dia;
    # com a cópia na pasta de evidência, a sonda que mudar depois vale para elas também.
    $sondas = Join-Path $PSScriptRoot "sondas_suspeitas.sh"
    if (Test-Path $sondas) {
        [System.IO.File]::WriteAllText((Join-Path $Evidencia "sondas_suspeitas.sh"), ([System.IO.File]::ReadAllText($sondas) -replace "`r`n", "`n"), $semBom)
    }
    & wsl --import $Nome $Instancia $Imagem --version 2
    if ($LASTEXITCODE -ne 0) { throw "wsl --import saiu com $LASTEXITCODE" }
}

try {
    # 4 a 7. Preparo como root, instalador e prova como usuario comum, e a evidencia de volta para o Windows.
    # ! Alteração de IA - Revisar: (pacote I2) `$comSystemd` leva ao preparo o texto `sem-systemd` quando a célula é chamada com `-SemSystemd`.
    # ! Motivo: sem esse argumento o bloco `sem-systemd` do preparo nunca roda, e a suspeita HL7 (serviço do MariaDB sem o systemd) não tem como aparecer.
    $comSystemd = "systemd-como-vier"
    if ($SemSystemd) { $comSystemd = "sem-systemd" }
    Invoke-Parte "root" @("preparo", $comSystemd)
    # ! Alteração de IA - Revisar: encerra a instância depois do preparo.
    # ! Motivo: o appendWindowsPath=false gravado no /etc/wsl.conf só vale quando a instância reinicia; sem isso a parte do usuário ainda enxerga o PATH do Windows.
    Write-Passo "wsl --terminate $Nome"
    if (-not $Simular) { & wsl --terminate $Nome | Out-Null }
    Invoke-Parte "cobaia" @("usuario", $Id, $Ate, $ModeloPequeno, (ConvertTo-CaminhoWsl $Pacote))
    # ! Alteração de IA - Revisar: (pacote I2) depois do instalador e da prova, a rodada `como-esta` roda as sondas das suspeitas.
    # ! Motivo: ver a tag de -SemSondas no começo do arquivo. O install.sh do clone do Windows vai só para a sonda da HL9
    # ler o fim de linha dele (`od -c`); ele nunca é executado de dentro da instância.
    if ($Modo -eq "como-esta" -and -not $SemSondas) {
        Invoke-Parte "cobaia" @("suspeitas", (ConvertTo-CaminhoWsl (Join-Path $Raiz "install.sh")))
    }
    Invoke-Parte "root" @("copia", (ConvertTo-CaminhoWsl $Evidencia))
}
finally {
    if (-not $Simular) {
      # ! Alteração de IA - Revisar: a montagem e a gravação do celula.json ficam dentro de try/catch.
      # ! Motivo: se o Get-FileHash ou a gravação falhava, o erro saía do finally antes do passo 8 e a instância não era apagada.
      try {
        # O codigo de saida de cada passo, lido dos arquivos que o celula.sh gravou.
        $saidas = [ordered]@{}
        Get-ChildItem -Path $Evidencia -Filter "saida_*.txt" -ErrorAction SilentlyContinue | Sort-Object Name | ForEach-Object {
            $saidas[$_.BaseName -replace "^saida_", ""] = (Get-Content $_.FullName -Raw).Trim()
        }
        $celula = [ordered]@{
            tag_ia = [ordered]@{
                alteracao = "! Alteração de IA - Revisar: arquivo gerado por ferramentas/instalador_matriz/celula_wsl.ps1: o que a celula rodou e com que codigo de saida."
                motivo = "! Motivo: o plano do instalador unico (decisao 143) pede a evidencia de cada celula em arquivo, mesmo quando o instalador para antes de a prova rodar."
            }
            id = $Id; modo = $Modo; ate = $Ate; modelo_pequeno = $ModeloPequeno
            # ! Alteração de IA - Revisar: (pacote I2) o celula.json passa a gravar `sondas` (se as sondas das suspeitas rodaram) e `sem_systemd` (se o systemd foi desligado).
            # ! Motivo: a leitura da evidência (ler_celula.py) precisa saber se a falta de um HLn na pasta é porque a sonda não rodou ou porque a suspeita não aconteceu.
            sondas = [bool]($Modo -eq "como-esta" -and -not $SemSondas); sem_systemd = [bool]$SemSystemd
            imagem = (Split-Path -Leaf $Imagem)
            imagem_sha256 = (Get-FileHash -Algorithm SHA256 $Imagem).Hash.ToLower()
            pacote_sha256 = (Get-FileHash -Algorithm SHA256 $Pacote).Hash.ToLower()
            wsl = @((& wsl --version) | Where-Object { $_.Trim() } | Select-Object -First 2)
            inicio = $inicio.ToString("s"); fim = (Get-Date).ToString("s")
            saidas = $saidas
        }
        $json = $celula | ConvertTo-Json -Depth 5
        [System.IO.File]::WriteAllText((Join-Path $Evidencia "celula.json"), $json, (New-Object System.Text.UTF8Encoding($false)))
        $saidas.GetEnumerator() | ForEach-Object { Write-Passo ("{0}: {1}" -f $_.Name, $_.Value) }
      }
      catch { Write-Passo "nao foi possivel gravar o celula.json: $($_.Exception.Message)" }
    }
    # 8. A instancia some.
    if ($ManterInstancia) {
        Write-Passo "instancia mantida: $Nome (apague com: wsl --unregister $Nome)"
    }
    else {
        Write-Passo "wsl --unregister $Nome"
        if (-not $Simular) {
            & wsl --terminate $Nome | Out-Null
            & wsl --unregister $Nome | Out-Null
            if (Test-Path $Instancia) { Remove-Item -Recurse -Force $Instancia }
        }
    }
}
Write-Passo "evidencia em $Evidencia"
