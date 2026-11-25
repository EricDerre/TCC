# ! Alteração de IA - Revisar: recompila Cobaia.exe a partir de Cobaia.py (+ install.py/run.py/_env_common.py).
# ! Motivo: o Cobaia.exe não se autoatualiza - rode de novo sempre que qualquer um desses arquivos mudar.
# ! Alteração de IA - Revisar: gravado em UTF-8 com BOM (29/09/2026, ficha 9 de pendencias.md, decidida pelo Eric).
# ! Motivo: regra do CLAUDE.md para .ps1 - sem BOM o Windows PowerShell 5.1 lê o arquivo na codepage ANSI, e um travessão
# dentro de uma string encerraria a string no meio; aqui ele estava só em comentário (parse conferido em 21/09/2026),
# então a troca é por consistência e para silenciar o aviso de ferramentas/conferir_docs.py.
# ! Alteração de IA - Revisar: (19/11/2026, pacote I3) o roteiro confere se a compilação deu certo (código de saída do
# PyInstaller e data do Cobaia.exe) antes de dizer "atualizado", roda o PyInstaller de dentro da pasta do projeto, guarda
# a saída do pip e do PyInstaller em %TEMP%\cobaia-build.log e aceita -Saida para compilar em outra pasta.
# ! Motivo: em 19/11/2026 ele rodou 4 segundos na janela do Eric, não gravou o Cobaia.spec nem o Cobaia.exe (que ficou
# com a data de 07/11/2026) e terminou em "Cobaia.exe atualizado", porque a mensagem saía sem olhar o resultado. Chamado
# de uma janela aberta em C:\Windows\System32, o PyInstaller para em "Do not run pyinstaller from C:\Windows\System32"
# antes de gravar qualquer arquivo (reproduzido no mesmo dia), por isso a compilação entra na pasta do projeto. A saída
# vai para o arquivo por `cmd /c` porque o Windows PowerShell 5.1, quando a saída de erro está redirecionada, trata como
# erro cada linha que um programa escreve nela, e é ali que o PyInstaller escreve o andamento. O -Saida existe para
# testar o roteiro sem trocar o Cobaia.exe do repositório.
param(
    [string]$Saida = $PSScriptRoot
)
$ErrorActionPreference = "Stop"

$Saida = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($Saida).TrimEnd('\')
$fonte = Join-Path $PSScriptRoot "Cobaia.py"
$exe = Join-Path $Saida "Cobaia.exe"
$log = Join-Path $env:TEMP "cobaia-build.log"
$buildVenv = Join-Path $env:TEMP "cobaia-build-venv"
$py = Join-Path $buildVenv "Scripts\python.exe"

function Invoke-ComLog([string]$Linha) {
    & cmd /c "$Linha >> `"$log`" 2>&1"
    return $LASTEXITCODE
}

function Stop-ComMotivo([string]$Motivo) {
    Write-Host ""
    Write-Host "FALHOU: $Motivo"
    Write-Host "O Cobaia.exe de $Saida continua sendo o de antes."
    if (Test-Path $log) {
        Write-Host "Últimas linhas de ${log}:"
        Get-Content $log -Tail 15 | ForEach-Object { Write-Host "  $_" }
    }
    exit 1
}

if (Test-Path $log) { Remove-Item $log -Force }

if (-not (Test-Path $buildVenv)) {
    Write-Host "Criando a venv de compilação em $buildVenv..."
    $codigo = Invoke-ComLog "python -m venv `"$buildVenv`""
    if ($codigo -ne 0) { Stop-ComMotivo "o python -m venv devolveu o código $codigo" }
}

Write-Host "Conferindo o PyInstaller da venv de compilação (pip)..."
$codigo = Invoke-ComLog "`"$py`" -m pip install --quiet --upgrade pyinstaller"
if ($codigo -ne 0) {
    Write-Host "Aviso: o pip devolveu o código $codigo; a compilação segue com o PyInstaller que já estiver na venv."
}

Write-Host "Compilando o Cobaia.exe (menos de um minuto)..."
$inicio = Get-Date
Push-Location $PSScriptRoot
try {
    $codigo = Invoke-ComLog ("`"$py`" -m PyInstaller --onefile --console --name Cobaia " +
        "--distpath `"$Saida`" --workpath `"$(Join-Path $env:TEMP 'cobaia-build')`" --specpath `"$Saida`" " +
        "--noconfirm `"$fonte`"")
} finally {
    Pop-Location
}

if ($codigo -ne 0) { Stop-ComMotivo "o PyInstaller devolveu o código $codigo" }
if (-not (Test-Path $exe) -or (Get-Item $exe).LastWriteTime -lt $inicio) {
    Stop-ComMotivo "o PyInstaller terminou sem erro, mas não gravou $exe"
}

Write-Host ""
Write-Host "Cobaia.exe atualizado em $Saida ($((Get-Item $exe).Length) bytes)"
