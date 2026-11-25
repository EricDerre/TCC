# ! Alteracao de IA - Revisar: arquivo novo (18/11/2026, corrida 28b, decisao 146): a sondagem do frio, para o Eric rodar antes da noite medida da Fase 5. Faz duas
# inferencias do mesmo cenario (o primeiro do catalogo, contrato-malformed_json), pelo mesmo caminho da noite: tira o modelo da memoria (ollama stop), confere o
# ollama ps vazio e chama o rodar_fase4.ps1 -Modo cenarios -Casos 1 -Repeticoes 1; depois tira o modelo de novo, confere, e chama com -Repeticoes 2, que roda so a
# segunda execucao. No fim, avaliar_fase5.py --sondagem le o registro da barra de progresso da pasta da sondagem e diz PASSOU ou NAO PASSOU. Passa quando nenhuma
# das duas inferencias reaproveitou token do que o Ollama tinha guardado. Grava em pasta propria, resultados_alvo\fase5_sondagem_frio_<data>_<hora>, nova a cada
# sondagem, fora da pasta da noite (fase5_agente_b).
# ! Motivo: a corrida 28 (18/11/2026) mostrou que o Ollama guarda o prompt ja lido e o reaproveita quando o mesmo cenario se repete: nas repeticoes 2 a 5, a leitura
# do prompt caiu de cerca de 47 s para menos de 1 s. A noite nova roda uma repeticao por vez, com o modelo descarregado entre elas (decisao 146), e isso so mede o
# que se quer se descarregar o modelo apagar o prompt guardado. A corrida 28 nao tem como dizer isso, porque o modelo ficou carregado da primeira a ultima execucao.
# A sondagem responde em poucos minutos, antes de gastar a hora de maquina da noite; o rodar_fase5.ps1 so comeca a corrida se a ultima sondagem tiver passado.
# Com -Casos 1 o rodar_fase4.ps1 grava a leitura do ensaio na pasta da propria sondagem; o -Nome fica de segunda protecao contra a leitura da corrida 21.
#
# Uso, numa janela do PowerShell, com o VS Code e o aplicativo Claude fechados:
#   powershell -ExecutionPolicy Bypass -File "C:\Users\Eric.Derre\Documents\TCC\Programacao\AgenteCore\experimentos\rodar_sondagem_frio.ps1"
# Opcao:
#   -Simular     so imprime, na ordem, os comandos que a sondagem rodaria (e o que o teste dela usa).
param(
    [switch]$Simular
)
$ErrorActionPreference = "Stop"
Set-Location -LiteralPath $PSScriptRoot
$env:RESULTADOS_DIR = "resultados_alvo"
$env:PYTHONIOENCODING = "utf-8"
$env:PYTHONUNBUFFERED = "1"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$Modelo = "qwen2.5:7b"
$Pasta = "fase5_sondagem_frio_" + (Get-Date -Format "yyyyMMdd_HHmmss")
$Inferencias = 2
$RamMinimaGB = 7.0

function Passo([string]$Msg) {
    Write-Host ("[{0}] {1}" -f (Get-Date -Format "dd/MM HH:mm:ss"), $Msg)
}
function Parar([string]$Msg, [int]$Codigo) {
    Passo ("!! {0} (codigo {1}); a sondagem parou aqui" -f $Msg, $Codigo)
    exit $Codigo
}
function Simulado([string]$Comando) {
    Write-Host ("SIMULADO: {0}" -f $Comando)
}
function ListaDeArgumentos([int]$N) {
    return @("-Modo", "cenarios", "-Saida", $Pasta, "-Casos", "1", "-Repeticoes", "$N", "-Nome", "cenarios_sondagem")
}
function RamLivreGB {
    return [math]::Round((Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory / 1MB, 1)
}
# o ollama e chamado com a preferencia de erro em Continue, dentro de try: com Stop, o Windows PowerShell 5.1 trata como erro fatal o que um comando nativo escreve
# no erro padrao quando ha redirecionamento, e o ollama stop reclama quando o modelo ja nao esta carregado
function Residentes {
    $antes = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    $saida = $null
    try { $saida = & ollama ps 2>$null } catch { $saida = $null }
    $ErrorActionPreference = $antes
    if (-not $saida) { return -1 }
    return ($saida | Measure-Object -Line).Lines - 1
}
function DescarregarModelo {
    $antes = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    try { & ollama stop $Modelo 2>&1 | Out-Null } catch { }
    $ErrorActionPreference = $antes
    $espera = 0
    while ((Residentes) -gt 0 -and $espera -lt 15) { Start-Sleep -Seconds 2; $espera++ }
    if ((Residentes) -ne 0) { Parar "o modelo nao saiu da memoria depois do ollama stop, ou o Ollama nao responde (confira com ollama ps)" 2 }
}

Passo ("sondagem do frio: {0} inferencias do mesmo cenario, com o modelo descarregado entre elas; pasta resultados_alvo\{1}{2}" -f $Inferencias, $Pasta, $(if ($Simular) { " (simulacao: nada roda)" } else { "" }))
if (-not $Simular) {
    if (-not (Get-Command ollama -ErrorAction SilentlyContinue)) { Parar "Ollama nao encontrado no PATH" 2 }
    if ((Residentes) -lt 0) {
        Passo "servidor do Ollama nao responde - iniciando"
        Start-Process -FilePath "ollama" -ArgumentList "serve" -WindowStyle Hidden
        $espera = 0
        while ((Residentes) -lt 0 -and $espera -lt 30) { Start-Sleep -Seconds 2; $espera++ }
        if ((Residentes) -lt 0) { Parar "o Ollama nao subiu; abra o aplicativo Ollama e rode de novo" 2 }
    }
    if ((RamLivreGB) -lt $RamMinimaGB) { Parar ("memoria livre {0:N1} GB abaixo de {1:N1} GB: feche o aplicativo Claude, o VS Code e o navegador e rode de novo" -f (RamLivreGB), $RamMinimaGB) 2 }
}

for ($N = 1; $N -le $Inferencias; $N++) {
    if ($Simular) {
        Simulado ("ollama stop {0} (inferencia {1} de {2}: o modelo sai da memoria)" -f $Modelo, $N, $Inferencias)
        Simulado "ollama ps vazio"
        Simulado ("powershell -ExecutionPolicy Bypass -File .\rodar_fase4.ps1 {0}" -f ((ListaDeArgumentos $N) -join " "))
    } else {
        Passo ("inferencia {0} de {1}: o modelo sai da memoria (ollama stop) e o ollama ps e conferido" -f $N, $Inferencias)
        DescarregarModelo
        $ArgumentosDaSondagem = ListaDeArgumentos $N
        & powershell -ExecutionPolicy Bypass -File ".\rodar_fase4.ps1" @ArgumentosDaSondagem
        if ($LASTEXITCODE -ne 0) { Parar ("a inferencia {0} da sondagem (rodar_fase4.ps1 -Modo cenarios -Casos 1) saiu com erro; a sondagem nao chegou ao veredito" -f $N) $LASTEXITCODE }
    }
}

if ($Simular) {
    Simulado ("python avaliar_fase5.py --sondagem --saida {0}" -f $Pasta)
    exit 0
}
& python @("avaliar_fase5.py", "--sondagem", "--saida", $Pasta)
$Codigo = $LASTEXITCODE
if ($Codigo -eq 0) {
    Passo "PASSOU: descarregar o modelo apaga o prompt guardado. A noite pode ser lancada (rodar_fase5.ps1)"
} elseif ($Codigo -eq 1) {
    Passo "NAO PASSOU: a noite nao roda assim. Leve o resultado ao Claude"
} else {
    Passo ("a sondagem nao chegou ao veredito (codigo {0}); leve o resultado ao Claude" -f $Codigo)
}
exit $Codigo
