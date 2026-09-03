# ! Alteração de IA - Revisar: orquestrador da Fase 2-B — roda, em sequência e um modelo por
# vez, a ablação de quantização do 1.5B, os braços A1/A2 nos seis modelos, A3–A5 nos três
# modelos das ablações e, no fim, avaliação, gráficos e relatório. Tudo resumível.
# ! Motivo: são ~2.000 inferências em CPU, 15–20 h; a Fase 2-B foi colocada em standby em
# 03/09/2026 à noite para rodar no dia seguinte, e o roteiro precisava ficar no repositório
# (não em arquivo temporário da sessão de IA) para ser disparado com um único comando. Cada
# etapa chama executar_bateria.py, que grava um JSONL por caso e pula o que já foi feito — o
# script pode ser interrompido e relançado sem repetir trabalho. Log em experimentos/fase2b.log.
#
# Uso (PowerShell, na pasta experimentos):
#   powershell -ExecutionPolicy Bypass -File .\rodar_fase2b.ps1
# Pré-requisitos: Ollama no ar, nenhum outro modelo residente (`ollama ps` vazio), venv do
# AgenteCore criada pelo instalador (para os gráficos).
$ErrorActionPreference = "Continue"
$env:PYTHONIOENCODING = "utf-8"
Set-Location $PSScriptRoot
$Log = Join-Path $PSScriptRoot "fase2b.log"
$Venv = Join-Path $PSScriptRoot "..\.venv\Scripts\python.exe"

function Marco($texto) {
    $linha = "== {0}  {1} ==" -f $texto, (Get-Date -Format "dd/MM HH:mm:ss")
    Write-Host $linha
    Add-Content -Path $Log -Value $linha -Encoding utf8
}
function Rodar($args_) {
    # Chama o Python do sistema (biblioteca padrão basta para a bateria) e anexa a saída ao log.
    & python @args_ 2>&1 | Tee-Object -FilePath $Log -Append
}

$residentes = (& ollama ps | Measure-Object -Line).Lines - 1
if ($residentes -gt 0) {
    Write-Host "Ha modelo residente no Ollama (ollama ps). Descarregue antes: a regra e um modelo por vez."
    exit 1
}

Marco "inicio da Fase 2-B"

# 0. Ablação de quantização no piso: mesmo modelo em q8_0 e fp16, braço A0 linear (teto 900,
#    igual à 2-A). As tags são baixadas se faltarem (ollama pull é idempotente).
foreach ($tag in @("qwen2.5-coder:1.5b-instruct-q8_0", "qwen2.5-coder:1.5b-instruct-fp16")) {
    if (-not (& ollama list | Select-String -SimpleMatch $tag)) { & ollama pull $tag }
}
Marco "ablacao de quantizacao (A0 linear)"
Rodar @("executar_bateria.py", "--modelos", "qwen2.5-coder:1.5b-instruct-q8_0", "qwen2.5-coder:1.5b-instruct-fp16", "--estrategias", "linear", "--condicao", "A0")

# 1. Biblioteca inteira (A1) e recuperada (A2) nos seis modelos, do mais rápido ao mais lento.
$todos = @("qwen2.5-coder:1.5b", "qwen2.5-coder:3b", "phi4-mini:3.8b", "qwen2.5:7b", "qwen2.5-coder:7b", "granite4.2:8b")
foreach ($m in $todos) {
    foreach ($c in @("A1", "A2")) {
        Marco "$m / $c"
        Rodar @("executar_bateria.py", "--modelos", $m, "--condicao", $c)
    }
}

# 2. Ablações (ouro, distratores, adversarial) nos três modelos: piso não degenerado, padrão
#    de produção atual e melhor modelo.
foreach ($m in @("phi4-mini:3.8b", "qwen2.5-coder:3b", "granite4.2:8b")) {
    foreach ($c in @("A3", "A4", "A5")) {
        Marco "$m / $c"
        Rodar @("executar_bateria.py", "--modelos", $m, "--condicao", $c)
    }
}

# 3. Avaliação final, gráficos e relatório navegável.
Marco "avaliacao final"
Rodar @("avaliar.py")
& $Venv gerar_graficos.py 2>&1 | Tee-Object -FilePath $Log -Append
Rodar @("gerar_relatorio.py")
Marco "FIM da Fase 2-B"
