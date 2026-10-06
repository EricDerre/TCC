# ! Alteracao de IA - Revisar: orquestrador da sonda de confianca da Pre-Fase 4 (01/10/2026). Confere o
# ambiente (Python, Ollama no ar, nenhum modelo residente), roda testar_fase3.py, testar_fase3b.py e
# testar_pre_fase4.py, espera a RAM livre que o modelo pede, roda sonda_confianca.py e, no fim, analisar_confianca.py: o modelo decidido
# com a biblioteca que ele mesmo escreveu, nos 36 casos oficiais de avaliacao e nos 36 ineditos, com o
# mesmo prompt e os mesmos parametros da Fase 3, pedindo ao Ollama a probabilidade de cada token. Log em
# <Resultados>\<Saida>\sonda_confianca.log.
# ! Motivo: as funcoes Marco/Falha/Rodar/RamLivreGB/Residentes/EsperarRam e a tabela $RamMinima sao copia
# de rodar_fase3b.ps1 (mesma maquina-alvo, mesma regra de um modelo residente por vez); reescreve-las de
# outro jeito criaria duas fontes da verdade para "quanta RAM cada modelo precisa". A corrida leva mais de
# uma hora e roda sem ninguem olhando: sem as checagens e sem o log, uma parada no meio (Ollama fora do
# ar, RAM insuficiente) so seria vista de manha. Relancar o script retoma do caso em que parou, porque
# sonda_confianca.py usa o mesmo executor da Fase 3, que nao refaz caso ja gravado.
#
# Uso (PowerShell, de dentro de experimentos\):
#   powershell -ExecutionPolicy Bypass -File rodar_sonda_confianca.ps1
#   powershell -ExecutionPolicy Bypass -File rodar_sonda_confianca.ps1 -Versoes 0,1
#   powershell -ExecutionPolicy Bypass -File rodar_sonda_confianca.ps1 -Versoes 0,1 -Curada
#   -Versoes ...    versoes da biblioteca do proprio modelo (padrao: 1; com 0,1 roda tambem a L0)
#   -Curada         roda tambem a copia curada da L1 (Programacao\AgenteCore\biblioteca_producao), gravada como
#                   L100 nos arquivos ("L1 curada" nas analises) - ficha 18 (a), decidida em 06/10/2026
#   -Modelo X       modelo a sondar (padrao qwen2.5:7b)
#   -Saida X        pasta de saida em <Resultados> (padrao pre_fase4_confianca)
#   -Top N          alternativas por posicao pedidas ao Ollama (padrao 20)
#   -Resultados X   le a corrida oficial em X\fase3 e grava em X\<Saida> (padrao resultados_alvo)
param(
    [string[]]$Versoes = @("1"),
    [switch]$Curada,
    [string]$Modelo = "qwen2.5:7b",
    [string]$Saida = "pre_fase4_confianca",
    [int]$Top = 20,
    [string]$Resultados = "resultados_alvo"
)
# -Versoes chega como UMA string "0,1" quando o script e chamado por "powershell -File" (conferido em
# 23/09/2026 para rodar_fase3b.ps1): dividir por virgula aqui e converter depois.
$Versoes = @($Versoes | ForEach-Object { "$_" -split "," } | ForEach-Object { $_.Trim() } | Where-Object { $_ } | ForEach-Object { [int]$_ })
$ErrorActionPreference = "Continue"
$env:PYTHONIOENCODING = "utf-8"
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
$Log = Join-Path $Dir "sonda_confianca.log"
$Inicio = Get-Date

# RAM livre minima por modelo, em GB - copiado de rodar_fase3b.ps1 (valores medidos na Fase 2-B).
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
        Marco ("PARADO {0}: RAM livre {1} GB menor que {2} GB. Libere memoria e relance o script - ele retoma daqui" -f $modelo, (RamLivreGB), $minimo)
        return $false
    }
    return $true
}

# ---------- 0. checagens de ambiente ----------
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
# ! Alteracao de IA - Revisar: (06/10/2026) -Curada acrescenta "--curada" aos argumentos da sonda, e o marco diz se a
# copia curada entra; a pasta de producao e conferida antes dos testes, para a corrida nao parar depois de horas.
# ! Motivo: ficha 18 (a): medir a copia curada da L1 nos 72 casos na mesma noite da sonda, para ela sair com as
# probabilidades por token; sem a conferencia antecipada, uma pasta faltando so apareceria depois das versoes 0 e 1.
$TextoCurada = "nao"
if ($Curada) {
    $PastaCurada = Join-Path (Split-Path $PSScriptRoot -Parent) "biblioteca_producao"
    if (-not (Test-Path (Join-Path $PastaCurada "fechamento.json"))) {
        Falha "copia curada nao encontrada ou nao fechada em $PastaCurada (falta fechamento.json)."
    }
    $TextoCurada = "sim (L100, de $PastaCurada)"
}
Marco ("RAM livre {0} GB; modelo {1}; versoes {2}; copia curada {3}; saida {4}" -f (RamLivreGB), $Modelo, ($Versoes -join ","), $TextoCurada, $Saida)

# ---------- 1. testes automatizados (sem LLM) ----------
Marco "testes automatizados da Fase 3, da Fase 3-B e da Pre-Fase 4 (sem LLM)"
Rodar @("testar_fase3.py")
if ($LASTEXITCODE -ne 0) { Falha "testar_fase3.py falhou - corrija antes de rodar a sonda." }
Rodar @("testar_fase3b.py")
if ($LASTEXITCODE -ne 0) { Falha "testar_fase3b.py falhou - corrija antes de rodar a sonda." }
Rodar @("testar_pre_fase4.py")
if ($LASTEXITCODE -ne 0) { Falha "testar_pre_fase4.py falhou - corrija antes de rodar a sonda." }

# ---------- 2. a sonda ----------
$Falhou = $false
if (-not (EsperarRam $Modelo)) {
    $Falhou = $true
} else {
    $Argumentos = @("sonda_confianca.py", "--saida", $Saida, "--modelo", $Modelo, "--top", $Top)
    if ($Curada) { $Argumentos += "--curada" }
    $Argumentos += @("--versoes") + $Versoes
    Marco ("{0}: sonda de confianca  (RAM livre {1} GB)" -f $Modelo, (RamLivreGB))
    Rodar $Argumentos
    if ($LASTEXITCODE -ne 0) {
        $Falhou = $true
        Marco ("AVISO: a sonda terminou com codigo {0} - veja as linhas '!!' acima; relance o script para retomar" -f $LASTEXITCODE)
    }
}

# ---------- 3. analise (sem LLM) ----------
# ! Alteracao de IA - Revisar: passo novo (01/10/2026): com a sonda inteira, roda analisar_confianca.py, que grava
# pre_fase4\confianca.json e confianca.md (a probabilidade do rotulo separa acerto de erro?).
# ! Motivo: a corrida roda de noite, sem ninguem olhando; com a analise no fim, o resultado ja esta pronto de manha,
# sem depender de outra sessao. A analise so le os arquivos gravados; se ela falhar, a corrida continua valendo.
if (-not $Falhou) {
    Marco "analise da sonda (analisar_confianca.py)"
    Rodar @("analisar_confianca.py", "--saida", $Saida)
    if ($LASTEXITCODE -ne 0) {
        Marco ("AVISO: a analise terminou com codigo {0}; os registros da sonda estao gravados e a analise pode ser refeita depois" -f $LASTEXITCODE)
    }
}

$duracao = (Get-Date) - $Inicio
$textoFalha = if ($Falhou) { "sim" } else { "nao" }
# As horas sao truncadas com [math]::Floor antes do [int]: no PowerShell, [int] arredonda para o inteiro
# mais proximo, e 1h46 sairia como 02h46 (corrigido em rodar_fase3b.ps1 em 30/09/2026).
Marco ("FIM da sonda de confianca - duracao total {0:d2}h{1:d2} - parou antes do fim: {2}" -f [int][math]::Floor($duracao.TotalHours), $duracao.Minutes, $textoFalha)
if ($Falhou) { exit 1 }
