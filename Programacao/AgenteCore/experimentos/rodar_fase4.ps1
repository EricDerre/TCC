# ! Alteracao de IA - Revisar: orquestrador da Fase 4 (26/10/2026, pacote P2), no molde de rodar_fase3b.ps1: confere
# a venv do AgenteCore (onde esta o Playwright), roda testar_fase4.py, roda executar_fase4.py no modo pedido e, ao
# fim, avaliar_fase4.py. Log em <Resultados>\<Saida>\fase4.log (o executar_fase4.py grava a linha FIM). Modo
# disponivel neste pacote: reproducao (corrida 17, sem modelo); os modos com modelo entram no P3 com a ponte de versao.
# ! Motivo: o plano aprovado (secao 6) fixa um comando por corrida com -Modo e -Saida, e o painel le o roadmap por
# esses comandos; o script e o lugar unico das conferencias de ambiente antes de cada corrida.
#
# Uso (PowerShell, de dentro de experimentos\):
#   powershell -ExecutionPolicy Bypass -File rodar_fase4.ps1 -Modo reproducao -Saida fase4_reproducao
#   -Casos N        limita aos N primeiros casos reproduziveis (0 = todos)
#   -Canal X        chromium (padrao) ou msedge
#   -Resultados X   pasta de resultados (padrao resultados_alvo)
param(
    [Parameter(Mandatory = $true)][ValidateSet("reproducao")][string]$Modo,
    [Parameter(Mandatory = $true)][string]$Saida,
    [int]$Casos = 0,
    [ValidateSet("chromium", "msedge")][string]$Canal = "chromium",
    [string]$Resultados = "resultados_alvo"
)
$ErrorActionPreference = "Stop"
$env:PYTHONIOENCODING = "utf-8"
$env:PYTHONUNBUFFERED = "1"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$env:RESULTADOS_DIR = $Resultados
$Aqui = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Aqui
$Venv = Join-Path $Aqui "..\.venv\Scripts\python.exe"
if (-not (Test-Path $Venv)) {
    Write-Host "!! venv do AgenteCore nao encontrada em $Venv (rode install.py primeiro)"
    exit 2
}
$Log = Join-Path (Join-Path (Join-Path $Aqui $Resultados) $Saida) "fase4.log"

function Marco([string]$Msg) {
    $linha = "[{0}] {1}" -f (Get-Date -Format "yyyy-MM-dd HH:mm:ss"), $Msg
    Write-Host $linha
    $dir = Split-Path -Parent $Log
    if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Force $dir | Out-Null }
    Add-Content -Encoding utf8 -Path $Log -Value $linha
}

Marco "rodar_fase4.ps1: modo $Modo, saida $Saida, canal $Canal, resultados $Resultados"
Marco "testar_fase4.py"
& python testar_fase4.py
if ($LASTEXITCODE -ne 0) { Marco "!! testar_fase4.py falhou (codigo $LASTEXITCODE)"; exit 1 }

Marco "executar_fase4.py --modo $Modo --saida $Saida --canal $Canal"
$Argumentos = @("executar_fase4.py", "--modo", $Modo, "--saida", $Saida, "--canal", $Canal)
if ($Casos -gt 0) { $Argumentos += @("--casos", "$Casos") }
& $Venv @Argumentos
if ($LASTEXITCODE -ne 0) { Marco "!! executar_fase4.py saiu com codigo $LASTEXITCODE"; exit $LASTEXITCODE }

Marco "avaliar_fase4.py --$Modo --saida $Saida"
& python avaliar_fase4.py "--$Modo" --saida $Saida
if ($LASTEXITCODE -ne 0) { Marco "!! avaliar_fase4.py saiu com codigo $LASTEXITCODE"; exit $LASTEXITCODE }
Marco "FIM rodar_fase4.ps1 (modo $Modo)"
exit 0
