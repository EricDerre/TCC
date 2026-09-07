# ! Alteração de IA - Revisar: orquestrador da Fase 2-B para a MÁQUINA-ALVO (notebook
# corporativo Intel i5-1235U, 16 GB, sem GPU dedicada). Confere o ambiente, baixa o que falta,
# registra a máquina, refaz a linha de base A0 nela e roda, um modelo por vez: ablação de
# quantização, A1/A2 nos seis modelos, A3–A5 nos três modelos das ablações e, no fim,
# avaliação, gráficos e relatório. Tudo resumível; log em resultados_alvo\fase2b.log.
# ! Motivo: a Fase 2-A foi medida no Ryzen de desenvolvimento, mas a tese afirma operar em
# máquina corporativa - os números que valem são os desta máquina. A linha de base A0 é
# refeita aqui porque as comparações da 2-B são pareadas caso a caso e não podem misturar
# máquinas (CPU diferente muda o tempo e pode mudar a resposta). Os resultados vão para
# resultados_alvo\ (variável RESULTADOS_DIR, lida por caminhos.py) para não sobrescrever os
# do Ryzen em resultados\. A checagem de RAM livre por modelo existe porque o Granite ocupa
# 6,6 GB residentes e esta máquina costuma ter mais da metade da memória em uso: sem RAM, o
# Ollama falha ao carregar e a bateria gravaria 90 erros de infraestrutura em vez de dados.
#
# Uso (PowerShell, de qualquer pasta):
#   powershell -ExecutionPolicy Bypass -File Programacao\AgenteCore\experimentos\rodar_fase2b.ps1
# Pode ser interrompido (Ctrl+C) e relançado: cada caso já gravado é pulado.
#   -SemBaseline   pula a repetição de A0 (só se A0 já foi feito NESTA máquina)
#   -Resultados X  grava em experimentos\X em vez de resultados_alvo
param(
    [string]$Resultados = "resultados_alvo",
    [switch]$SemBaseline
)
$ErrorActionPreference = "Continue"
$env:PYTHONIOENCODING = "utf-8"
$env:RESULTADOS_DIR = $Resultados
Set-Location $PSScriptRoot
$Dir = Join-Path $PSScriptRoot $Resultados
New-Item -ItemType Directory -Force -Path $Dir | Out-Null
$Log = Join-Path $Dir "fase2b.log"
$VenvDir = Join-Path $PSScriptRoot "..\.venv"
$Venv = Join-Path $VenvDir "Scripts\python.exe"
$Inicio = Get-Date

$Modelos = @("qwen2.5-coder:1.5b", "qwen2.5-coder:3b", "phi4-mini:3.8b", "qwen2.5:7b", "qwen2.5-coder:7b", "granite4.2:8b")
$Variantes = @("qwen2.5-coder:1.5b-instruct-q8_0", "qwen2.5-coder:1.5b-instruct-fp16")
$Ablacoes = @("phi4-mini:3.8b", "qwen2.5-coder:3b", "granite4.2:8b")
# RAM livre mínima por modelo (peso residente medido na 2-A + cache de contexto), em GB.
$RamMinima = @{
    "qwen2.5-coder:1.5b" = 2.5; "qwen2.5-coder:3b" = 3.5; "phi4-mini:3.8b" = 4.5
    "qwen2.5:7b" = 6.5; "qwen2.5-coder:7b" = 6.5; "granite4.2:8b" = 8.0
    "qwen2.5-coder:1.5b-instruct-q8_0" = 3.0; "qwen2.5-coder:1.5b-instruct-fp16" = 4.5
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
    & python @argumentos 2>&1 | Tee-Object -FilePath $Log -Append
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
    $tentativas = 0
    while ((RamLivreGB) -lt $minimo -and $tentativas -lt 10) {
        Write-Host ("RAM livre {0} GB, {1} precisa de {2} GB - feche programas; nova checagem em 30 s" -f (RamLivreGB), $modelo, $minimo) -ForegroundColor Yellow
        Start-Sleep -Seconds 30
        $tentativas++
    }
    if ((RamLivreGB) -lt $minimo) {
        Marco ("PULADO {0}: RAM livre {1} GB < {2} GB. Libere memoria e relance o script - ele retoma daqui" -f $modelo, (RamLivreGB), $minimo)
        return $false
    }
    return $true
}
function Bateria($modelo, $condicao, $extras) {
    if (-not (EsperarRam $modelo)) { return }
    Marco ("{0} / {1}  (RAM livre {2} GB)" -f $modelo, $condicao, (RamLivreGB))
    $argumentos = @("executar_bateria.py", "--modelos", $modelo, "--condicao", $condicao) + $extras
    Rodar $argumentos
}

# ---------- 0. checagens de ambiente ----------
Marco "checagens de ambiente"
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Falha "Python 3 nao encontrado no PATH. Instale (winget install Python.Python.3.12), reabra o terminal e rode de novo."
}
$versaoOk = & python -c "import sys; print(sys.version_info >= (3, 10))"
if ("$versaoOk" -ne "True") { Falha "Python 3.10 ou mais novo e necessario (encontrado: $(& python --version))." }
if (-not (Get-Command ollama -ErrorAction SilentlyContinue)) {
    Write-Host "Ollama nao encontrado - instalando via winget..."
    winget install --id Ollama.Ollama -e --accept-package-agreements --accept-source-agreements
    Falha "Ollama instalado. Feche e reabra o terminal e rode o script de novo."
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
$unidade = $PSScriptRoot.Substring(0, 1)
$discoLivreGB = [math]::Round((Get-PSDrive -Name $unidade).Free / 1GB, 1)
$lista = & ollama list
$faltando = @()
foreach ($tag in ($Modelos + $Variantes)) {
    # "tag " com espaco: "qwen2.5-coder:1.5b" e prefixo de "qwen2.5-coder:1.5b-instruct-q8_0"
    if (-not ($lista | Select-String -SimpleMatch "$tag ")) { $faltando += $tag }
}
$textoFaltando = if ($faltando.Count -gt 0) { $faltando -join ", " } else { "nenhum" }
Marco ("disco livre {0} GB; RAM livre {1} GB; modelos faltando: {2}" -f $discoLivreGB, (RamLivreGB), $textoFaltando)
if ($faltando.Count -gt 0 -and $discoLivreGB -lt 30) {
    Falha "Menos de 30 GB livres no disco e ha modelos para baixar (~25 GB no total). Libere espaco."
}
foreach ($tag in $faltando) {
    Marco "baixando $tag"
    & ollama pull $tag 2>&1 | Tee-Object -FilePath $Log -Append
}
if (-not (Test-Path $Venv)) {
    Marco "criando a venv do AgenteCore (matplotlib, para os graficos)"
    & python -m venv $VenvDir
    & $Venv -m pip install --quiet -r (Join-Path $PSScriptRoot "..\requirements.txt")
}

# ---------- registro da maquina (vai junto com os resultados) ----------
$cpu = Get-CimInstance Win32_Processor | Select-Object -First 1
$so = Get-CimInstance Win32_OperatingSystem
$maquina = [ordered]@{
    hostname               = $env:COMPUTERNAME
    cpu                    = $cpu.Name.Trim()
    nucleos                = $cpu.NumberOfCores
    threads                = $cpu.NumberOfLogicalProcessors
    ram_gb                 = [math]::Round($so.TotalVisibleMemorySize / 1MB, 1)
    ram_livre_no_inicio_gb = (RamLivreGB)
    sistema                = "$($so.Caption) $($so.Version)"
    ollama                 = ((& ollama --version) -join " ")
    python                 = ((& python --version) -join " ")
    inicio                 = $Inicio.ToString("s")
    resultados_dir         = $Resultados
}
$maquina | ConvertTo-Json | Out-File -FilePath (Join-Path $Dir "maquina.json") -Encoding utf8
Write-Host ($maquina | ConvertTo-Json)

# ---------- 1. validacao e Verificacao 0 nesta maquina ----------
Marco "validar casos e biblioteca"
Rodar @("validar_banco.py")
if ($LASTEXITCODE -ne 0) { Falha "validar_banco.py acusou problema - corrija antes de rodar a bateria." }
Marco "verificacao 0: cache de prefixo nesta maquina"
if (EsperarRam "qwen2.5-coder:3b") { Rodar @("verificar_cache_prefixo.py", "--modelo", "qwen2.5-coder:3b") }

# ---------- 2. ablacao de quantizacao no piso (A0 linear, teto 900 como na 2-A) ----------
foreach ($v in $Variantes) { Bateria $v "A0" @("--estrategias", "linear") }

# ---------- 3. linha de base A0 (linear) refeita NESTA maquina ----------
if (-not $SemBaseline) {
    foreach ($m in $Modelos) { Bateria $m "A0" @("--estrategias", "linear") }
}

# ---------- 4. biblioteca inteira (A1) e recuperada (A2), do mais rapido ao mais lento ----------
foreach ($m in $Modelos) {
    foreach ($c in @("A1", "A2")) { Bateria $m $c @() }
}

# ---------- 5. ablacoes: so o verbete certo, distratores, adversarial ----------
foreach ($m in $Ablacoes) {
    foreach ($c in @("A3", "A4", "A5")) { Bateria $m $c @() }
}

# ---------- 6. avaliacao, graficos e relatorio (tudo dentro de resultados_alvo\) ----------
Marco "avaliacao final"
Rodar @("avaliar.py")
& $Venv gerar_graficos.py 2>&1 | Tee-Object -FilePath $Log -Append
Rodar @("gerar_relatorio.py")
$duracao = (Get-Date) - $Inicio
Marco ("FIM da Fase 2-B - duracao total {0:d2}h{1:d2}" -f [int]$duracao.TotalHours, $duracao.Minutes)
