# ! Alteracao de IA - Revisar: orquestrador da Fase 3-B (ponte, cruzada, texto_max, a5,
# ineditos - diagnosticos complementares a Fase 3 oficial, sempre sobre COPIAS dos snapshots
# fechados de resultados_alvo\fase3\, nunca sobre a corrida oficial). Confere o ambiente
# (mesmas checagens de rodar_fase3.ps1: Python, Ollama no ar, nenhum modelo residente), roda
# testar_fase3.py e testar_fase3b.py, roda executar_fase3b.py um modelo por vez (EsperarRam
# entre um e outro, como rodar_fase3.ps1) e, ao fim, avaliar_fase3b.py. Log em
# <Resultados>\<Saida>\fase3b.log.
# ! Motivo: as funcoes Marco/Falha/Rodar/RamLivreGB/Residentes/EsperarRam e a tabela
# $RamMinima abaixo sao copia literal de rodar_fase3.ps1 (mesmo texto, mesmo comportamento) -
# a Fase 3-B roda na MESMA maquina-alvo, com a MESMA exigencia de um modelo residente por vez
# (os 16 GB nao comportam dois), entao reescrever essas funcoes de outro jeito so criaria duas
# fontes da verdade para "quanta RAM cada modelo precisa" e "como ler ollama ps" sem nenhum
# ganho. Este script nao altera executar_fase3.py, evolucao_biblioteca.py nem nada em
# resultados_alvo\fase3\ - so le a corrida oficial (bibliotecas\<slug>\epoca-N fechadas e
# particao.json) e grava em <Resultados>\<Saida>, uma pasta nova por invocacao.
#
# Uso (PowerShell, de dentro de experimentos\):
#   powershell -ExecutionPolicy Bypass -File rodar_fase3b.ps1 -Modo ponte -Saida fase3b_ponte
#   powershell -ExecutionPolicy Bypass -File rodar_fase3b.ps1 -Modo cruzada -Saida fase3b_cruzada_qwen3b -Doador qwen2.5-coder:3b -Modelos qwen2.5:7b,qwen2.5-coder:7b,granite4.2:8b
#   powershell -ExecutionPolicy Bypass -File rodar_fase3b.ps1 -Modo texto_max -Saida fase3b_texto_max -TextoMax 600
#   powershell -ExecutionPolicy Bypass -File rodar_fase3b.ps1 -Modo a5 -Saida fase3b_a5
#   powershell -ExecutionPolicy Bypass -File rodar_fase3b.ps1 -Modo ineditos -Saida fase3b_ineditos
#   -Modelos ...    lista de modelos (padrao: os 4 da Fase 3); no modo cruzada, os LEITORES
#                   (sem o -Doador); no modo texto_max e ignorada (fixo em granite4.2:8b)
#   -Doador X       modelo dono da biblioteca lida pelos outros (obrigatorio no modo cruzada)
#   -Versoes ...    versoes de biblioteca a ler (padrao por modo: cruzada 1 3; ineditos 0 1 3)
#   -TextoMax N     teto de TEXTO em caracteres no modo texto_max (padrao 600)
#   -Resultados X   le a corrida oficial em X\fase3 e grava em X\<Saida> (padrao resultados_alvo)
param(
    [Parameter(Mandatory = $true)]
    [ValidateSet("ponte", "cruzada", "texto_max", "a5", "ineditos")]
    [string]$Modo,
    [Parameter(Mandatory = $true)]
    [string]$Saida,
    [string[]]$Modelos = @("qwen2.5-coder:3b", "qwen2.5:7b", "qwen2.5-coder:7b", "granite4.2:8b"),
    [string]$Doador,
    [int[]]$Versoes,
    [int]$TextoMax = 600,
    [string]$Resultados = "resultados_alvo"
)
$ErrorActionPreference = "Continue"
$env:PYTHONIOENCODING = "utf-8"
# PYTHONUNBUFFERED=1 e o OutputEncoding do console: mesma razao de rodar_fase3.ps1 (o Python
# grava o stdout em blocos de ~8 KB por padrao dentro do pipe da funcao Rodar, e o console do
# Windows PowerShell 5.1 decodifica a saida de processos nativos na codepage OEM sem isso).
$env:PYTHONUNBUFFERED = "1"
try { [Console]::OutputEncoding = New-Object System.Text.UTF8Encoding($false) } catch { }
$env:RESULTADOS_DIR = $Resultados
Set-Location $PSScriptRoot

if ($Saida -eq "fase3") {
    Write-Host "ERRO: -Saida nao pode ser 'fase3' - e a pasta da corrida oficial, que este script so le." -ForegroundColor Red
    exit 1
}

$Dir = Join-Path $PSScriptRoot "$Resultados\$Saida"
New-Item -ItemType Directory -Force -Path $Dir | Out-Null
$Log = Join-Path $Dir "fase3b.log"
$Inicio = Get-Date

# RAM livre minima por modelo (peso residente medido na 2-B + cache de contexto), em GB -
# copiado de rodar_fase3.ps1 (mesmos 4 modelos da Fase 3, mesmos valores medidos la).
$RamMinima = @{
    "qwen2.5-coder:3b" = 3.5; "qwen2.5:7b" = 6.5; "qwen2.5-coder:7b" = 6.5; "granite4.2:8b" = 8.0
}

function Marco($texto) {
    $linha = "== {0}  {1} ==" -f $texto, (Get-Date -Format "dd/MM HH:mm:ss")
    Write-Host $linha -ForegroundColor Cyan
    Add-Content -Path $Log -Value $linha -Encoding utf8
}
function Falha($texto) {
    Write-Host "ERRO: $texto" -ForegroundColor Red
    Add-Content -Path $Log -Value "ERRO: $texto" -Encoding utf8
    exit 1
}
# Rodar troca Tee-Object (que grava UTF-16 no Windows PowerShell 5.1 quando o script roda via
# -File, sem console interativo) por ForEach-Object + Add-Content -Encoding utf8 - mesma
# correcao e mesmo motivo de rodar_fase3.ps1 (linha "c\x00a\x00s\x00o\x00s\x00..." no log do
# piloto da Fase 3 antes da troca).
function Rodar($argumentos) {
    & python @argumentos 2>&1 | ForEach-Object {
        Write-Host $_
        Add-Content -Path $Log -Value $_ -Encoding utf8
    }
}
function RamLivreGB {
    return [math]::Round((Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory / 1MB, 1)
}
function Residentes {
    $saida = & ollama ps 2>$null
    if (-not $saida) { return -1 }
    return ($saida | Measure-Object -Line).Lines - 1
}
function EsperarRam($modelo) {
    $minimo = $RamMinima[$modelo]
    if (-not $minimo) { $minimo = 4.0 }
    $tentativas = 0
    while ((RamLivreGB) -lt $minimo -and $tentativas -lt 10) {
        Write-Host ("RAM livre {0} GB, {1} precisa de {2} GB - feche programas; nova checagem em 30 s" -f (RamLivreGB), $modelo, $minimo) -ForegroundColor Yellow
        Start-Sleep -Seconds 30
        $tentativas++
    }
    if ((RamLivreGB) -lt $minimo) {
        Marco ("PULADO {0}: RAM livre {1} GB menor que {2} GB. Libere memoria e relance o script - ele retoma daqui" -f $modelo, (RamLivreGB), $minimo)
        return $false
    }
    return $true
}

# ---------- 0. checagens de ambiente (Python, Ollama no ar, nenhum residente - mesmas de rodar_fase3.ps1) ----------
Marco "checagens de ambiente"
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Falha "Python 3 nao encontrado no PATH."
}
if (-not (Get-Command ollama -ErrorAction SilentlyContinue)) {
    Falha "Ollama nao encontrado no PATH."
}
if ((Residentes) -lt 0) {
    Write-Host "Servidor do Ollama nao responde - iniciando..."
    Start-Process -FilePath "ollama" -ArgumentList "serve" -WindowStyle Hidden
    $espera = 0
    while ((Residentes) -lt 0 -and $espera -lt 30) { Start-Sleep -Seconds 2; $espera++ }
    if ((Residentes) -lt 0) { Falha "Ollama nao subiu. Abra o aplicativo Ollama e rode de novo." }
}
if ((Residentes) -gt 0) {
    & ollama ps
    Falha "Ha modelo residente no Ollama. Regra do experimento: um modelo por vez. Descarregue (ollama stop <modelo>) e rode de novo."
}
Marco ("RAM livre {0} GB; modo {1}; saida {2}" -f (RamLivreGB), $Modo, $Saida)

# ---------- 1. testes automatizados (sem LLM, < 30 s cada) ----------
Marco "testes automatizados da Fase 3 e da Fase 3-B (sem LLM)"
Rodar @("testar_fase3.py")
if ($LASTEXITCODE -ne 0) { Falha "testar_fase3.py falhou - corrija antes de rodar a Fase 3-B." }
Rodar @("testar_fase3b.py")
if ($LASTEXITCODE -ne 0) { Falha "testar_fase3b.py falhou - corrija antes de rodar a Fase 3-B." }

# ---------- 2. execucao, um modelo por vez ----------
# texto_max e fixo em granite4.2:8b (executar_fase3b.py ignora -Modelos nesse modo); os outros
# quatro modos rodam a lista de -Modelos um de cada vez, com EsperarRam entre eles - igual ao
# laco de rodar_fase3.ps1. No modo cruzada, -Modelos e a lista de LEITORES (sem o -Doador);
# executar_fase3b.py para com erro claro se -Doador faltar ou aparecer tambem em -Modelos.
$ModelosDaRodada = if ($Modo -eq "texto_max") { @("granite4.2:8b") } else { $Modelos }

$Falhas = @()
foreach ($m in $ModelosDaRodada) {
    if (-not (EsperarRam $m)) {
        $Falhas += $m
        continue
    }
    $Argumentos = @("executar_fase3b.py", "--modo", $Modo, "--saida", $Saida)
    if ($Modo -ne "texto_max") { $Argumentos += @("--modelos", $m) }
    if ($Modo -eq "cruzada") { $Argumentos += @("--doador", $Doador) }
    if ($Versoes) { $Argumentos += @("--versoes") + $Versoes }
    if ($Modo -eq "texto_max") { $Argumentos += @("--texto-max", $TextoMax) }

    Marco ("{0}: modo {1}  (RAM livre {2} GB)" -f $m, $Modo, (RamLivreGB))
    Rodar $Argumentos
    if ($LASTEXITCODE -ne 0) {
        $Falhas += $m
        Marco ("AVISO: {0} terminou com codigo {1} - veja as linhas '!!' acima; relance o script para retomar" -f $m, $LASTEXITCODE)
    }
}

# ---------- 3. avaliacao ----------
Marco "avaliacao"
Rodar @("avaliar_fase3b.py", "--saida", $Saida)

$duracao = (Get-Date) - $Inicio
# ! Alteracao de IA - Revisar: o FIM lista os modelos/passos com falha e o script sai com
# codigo 1 quando houve algum - mesma politica de rodar_fase3.ps1 (secao 3, $Falhas).
# ! Motivo: sem isso, um modelo que parasse (RAM insuficiente em EsperarRam, ou
# executar_fase3b.py saindo com codigo 1 ou 2) deixaria "FIM" no log com codigo 0, e quem
# encadeia o script ou le so a ultima linha nao saberia que precisa relancar.
$textoFalhas = if ($Falhas.Count -gt 0) { $Falhas -join ", " } else { "nenhum" }
Marco ("FIM da Fase 3-B ({0}) - duracao total {1:d2}h{2:d2} - modelos com falha: {3}" -f $Modo, [int]$duracao.TotalHours, $duracao.Minutes, $textoFalhas)
if ($Falhas.Count -gt 0) { exit 1 }
