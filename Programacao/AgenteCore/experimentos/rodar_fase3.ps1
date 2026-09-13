# ! Alteração de IA - Revisar: orquestrador da Fase 3 (diagnóstico + proposta de edição da
# biblioteca, por época, um modelo por vez) na MÁQUINA-ALVO (notebook corporativo Intel
# i5-1235U, 16 GB, sem GPU dedicada). Confere o ambiente, baixa o que falta, imprime a
# projeção de tempo, roda cada modelo (épocas de aprendizado + passada final) e, no fim,
# avalia, compara com as fases 2-A/2-B, gera gráficos e relatório. Retomável: cada JSONL já
# gravado é pulado pelo próprio executar_fase3.py, então relançar o script só refaz o que
# faltou. Log em <Resultados>\<fase3|fase3_piloto>\fase3.log. O modo -Piloto roda só
# qwen2.5-coder:3b, 10 casos e 1 época, gravando em fase3_piloto\, para validar o encanamento
# antes da corrida real de dezenas de horas com os 4 modelos.
# ! Motivo: na MÁQUINA-ALVO porque os tempos que entram na tese são os dela e as comparações
# com a Fase 2-B são pareadas caso a caso (executar_fase3.py grava maquina.json e a comparação
# não pode misturar máquinas). Um modelo por vez porque os 16 GB não comportam dois modelos
# residentes sem contaminar tempo e memória (é o que EsperarRam e a checagem de Residentes
# garantem). Retomável porque são dezenas de horas em sessões de vários dias, cada inferência
# custa ~1 min em CPU e uma queda no meio não pode obrigar a refazer o que já foi gravado.
# As funções Marco/Falha/Rodar/RamLivreGB/Residentes/EsperarRam abaixo são cópia
# literal de rodar_fase2b.ps1 (mesmo texto, mesmo comportamento). Este script não importa
# funções de outro .ps1 - não há um mecanismo tão simples quanto o "import" do Python para
# isso, e um terceiro arquivo só para hospedar essas funções obrigaria os dois orquestradores
# a carregá-lo (dot-sourcing), acoplando os dois só para não repetir ~40 linhas. Manter os
# dois arquivos independentes é o preço de poder alterar um sem revisar o outro no meio de
# uma corrida de dezenas de horas.
#
# Uso (PowerShell, de dentro de experimentos\):
#   powershell -ExecutionPolicy Bypass -File rodar_fase3.ps1
#   powershell -ExecutionPolicy Bypass -File rodar_fase3.ps1 -Piloto
# Pode ser interrompido (Ctrl+C) e relançado: cada caso já gravado é pulado.
#   -SemAvaliacao   só roda as baterias (diagnóstico + proposta); pula avaliação/gráficos/relatório
#   -Piloto         1 modelo (qwen2.5-coder:3b), 10 casos, 1 época, pasta fase3_piloto
#   -Resultados X   grava em experimentos\X em vez de resultados_alvo
#   -Modelos ...    lista de modelos a rodar (padrão: os 4 da Fase 3)
#   -Epocas N       épocas de aprendizado antes da passada final (padrão 3)
param(
    [string]$Resultados = "resultados_alvo",
    [string[]]$Modelos = @("qwen2.5-coder:3b", "qwen2.5:7b", "qwen2.5-coder:7b", "granite4.2:8b"),
    [int]$Epocas = 3,
    [switch]$Piloto,
    [switch]$SemAvaliacao
)
$ErrorActionPreference = "Continue"
$env:PYTHONIOENCODING = "utf-8"
# ! Alteração de IA - Revisar: PYTHONUNBUFFERED=1 para o python.exe gravar o stdout linha a
# linha quando a saída vai para o pipe da função Rodar - onda final de correções.
# ! Motivo: com a saída num pipe ("2>&1 | ForEach-Object"), o Python guarda o stdout num
# bloco de ~8 KB e só o entrega quando o bloco enche ou o processo termina; como
# executar_fase3.py imprime pouco (1 linha a cada 10 casos e 1 por proposta), o console e o
# fase3.log ficavam horas sem nada e recebiam tudo de uma vez no fim de cada modelo - e, se o
# processo fosse morto ou a máquina reiniciasse, as linhas presas no bloco se perdiam (os
# JSONL não, que são gravados com flush por linha). Não muda nenhum dado gravado.
$env:PYTHONUNBUFFERED = "1"
# ! Alteração de IA - Revisar: o console passa a decodificar a saída dos processos nativos
# (python.exe, ollama.exe) como UTF-8 sem BOM - onda final de correções.
# ! Motivo: o python imprime em UTF-8 (PYTHONIOENCODING acima), mas o Windows PowerShell 5.1
# decodificava esses bytes com a codepage OEM do console (850 no pt-BR) antes de gravar no
# log, e o fase3.log do piloto saiu com "recupera├º├úo" no lugar de "recuperação". Só
# legibilidade do log: os .jsonl/.json são gravados pelo próprio Python em UTF-8 correto. O
# try é porque o setter lança erro quando não há console anexado (ex.: tarefa agendada), e
# um log com acento trocado não justifica derrubar a corrida.
try { [Console]::OutputEncoding = New-Object System.Text.UTF8Encoding($false) } catch { }
$env:RESULTADOS_DIR = $Resultados
Set-Location $PSScriptRoot

$Saida = if ($Piloto) { "fase3_piloto" } else { "fase3" }
$Dir = Join-Path $PSScriptRoot "$Resultados\$Saida"
New-Item -ItemType Directory -Force -Path $Dir | Out-Null
$Log = Join-Path $Dir "fase3.log"
$VenvDir = Join-Path $PSScriptRoot "..\.venv"
$Venv = Join-Path $VenvDir "Scripts\python.exe"
$Inicio = Get-Date

$ExtrasCasos = @()
if ($Piloto) {
    $Modelos = @("qwen2.5-coder:3b")
    $Epocas = 1
    $ExtrasCasos = @("--casos", "10")
}

# RAM livre mínima por modelo (peso residente medido na 2-B + cache de contexto), em GB; só
# os 4 modelos da Fase 3 - ao contrário da 2-B, aqui não há variantes de quantização.
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
# ! Alteração de IA - Revisar: Rodar não usa mais "2>&1 | Tee-Object -FilePath $Log -Append"
# (o padrão literal da 2-B) - troquei o consumidor do pipe por um ForEach-Object que ecoa no
# console (Write-Host) e grava no log com Add-Content -Encoding utf8.
# ! Motivo: rodando o piloto real desta tarefa (powershell -File rodar_fase3.ps1 -Piloto), o
# trecho de fase3.log escrito por validar_banco.py saiu como "c\x00a\x00s\x00o\x00s\x00..." -
# UTF-16 - enquanto as linhas do Marco (Add-Content -Encoding utf8) ficaram corretas em UTF-8
# no mesmo arquivo. Causa: o Tee-Object do Windows PowerShell 5.1 não tem parâmetro
# -Encoding, e o encoding padrão dele para escrever arquivo é Unicode (UTF-16) quando o
# processo roda via "-File" sem console interativo anexado - confirmado testando
# "[Console]::OutputEncoding = UTF8" antes do Tee-Object, que não mudou nada (a escrita do
# Tee-Object independe disso). O mesmo defeito já existe, sem correção, no
# resultados_alvo\fase2b.log gravado pela 2-B (mesmo padrão "c\x00a\x00s\x00o\x00s\x00" nos
# trechos vindos de Rodar) - não mexi em rodar_fase2b.ps1 porque a Fase 2-B já fechou e seus
# arquivos em resultados_alvo\ não podem mudar; fica registrado no relatório da Tarefa 12
# para o Eric decidir se vale corrigir lá também. Add-Content -Encoding utf8 é o mesmo
# comando que o Marco já usa com sucesso nas linhas de marco deste log, então reaproveitar
# ele aqui elimina a mistura de codificação no mesmo arquivo sem inventar mecanismo novo.
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

# ---------- 0. checagens de ambiente (iguais às da 2-B) ----------
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
foreach ($tag in $Modelos) {
    # "tag " com espaço evita falso positivo caso um nome desta lista vire prefixo de outro
    # no "ollama list" (é o que acontece na 2-B entre qwen2.5-coder:1.5b e as variantes
    # -instruct-q8_0/-fp16; aqui os 4 modelos da Fase 3 não colidem, mas o teste custa nada).
    if (-not ($lista | Select-String -SimpleMatch "$tag ")) { $faltando += $tag }
}
$textoFaltando = if ($faltando.Count -gt 0) { $faltando -join ", " } else { "nenhum" }
Marco ("disco livre {0} GB; RAM livre {1} GB; modelos faltando: {2}" -f $discoLivreGB, (RamLivreGB), $textoFaltando)
if ($faltando.Count -gt 0 -and $discoLivreGB -lt 30) {
    Falha "Menos de 30 GB livres no disco e ha modelos para baixar. Libere espaco."
}
foreach ($tag in $faltando) {
    Marco "baixando $tag"
    # mesma troca de Tee-Object por ForEach-Object explicada na função Rodar, acima.
    & ollama pull $tag 2>&1 | ForEach-Object {
        Write-Host $_
        Add-Content -Path $Log -Value $_ -Encoding utf8
    }
}
# ! Alteração de IA - Revisar: depois dos downloads, o "ollama list" é conferido de novo e o
# script para (Falha) se algum modelo continuar faltando - onda final de correções.
# ! Motivo: o resultado do "ollama pull" não era conferido (nem o código de saída nem um novo
# "ollama list"); com o download falhando (sem rede, disco cheio, tag inexistente), o modelo
# continuava ausente e o executar_fase3.py o pulava com a mensagem "!! nao esta baixado -
# pulando" e código 0 - a corrida "terminava bem" sem aquele modelo. Herdado do molde
# (rodar_fase2b.ps1); hoje os 4 modelos da Fase 3 já estão instalados, então só dispara numa
# máquina nova.
if ($faltando.Count -gt 0) {
    $lista = & ollama list
    $aindaFaltando = @($faltando | Where-Object { -not ($lista | Select-String -SimpleMatch "$_ ") })
    if ($aindaFaltando.Count -gt 0) {
        Falha ("download de {0} falhou - o modelo continua fora do 'ollama list'. Confira rede/disco/tag e rode de novo." -f ($aindaFaltando -join ", "))
    }
}
if (-not (Test-Path $Venv)) {
    Marco "criando a venv do AgenteCore (matplotlib, para os graficos)"
    & python -m venv $VenvDir
    & $Venv -m pip install --quiet -r (Join-Path $PSScriptRoot "..\requirements.txt")
}
# O maquina.json desta corrida quem grava e o executar_fase3.py (função maquina_atual, dentro
# de c3["maquina"]) - não duplicamos o registro aqui como a 2-B faz, para não ter dois
# arquivos descrevendo a mesma máquina e podendo divergir entre si.

# ---------- 1. validação da biblioteca/índice e dos testes do harness ----------
Marco "validar indice e biblioteca"
Rodar @("validar_banco.py", "--indice")
if ($LASTEXITCODE -ne 0) { Falha "validar_banco.py acusou problema - corrija antes de rodar a bateria." }
Marco "testes automatizados da Fase 3 (sem LLM, < 30 s)"
Rodar @("testar_fase3.py")
if ($LASTEXITCODE -ne 0) { Falha "testar_fase3.py falhou - corrija antes de rodar a bateria." }

# ---------- 2. projeção de tempo e execução, um modelo por vez ----------
Marco "projecao de tempo"
# ! Alteração de IA - Revisar: a projeção recebe os mesmos --epocas e --casos da corrida que
# vai rodar logo abaixo - onda final de correções.
# ! Motivo: no piloto a projeção foi impressa para 90 casos e 3 épocas (9,81 h) e a corrida
# real foi de 10 casos e 1 época (13 min); a projeção descrevia outra corrida. Com os mesmos
# argumentos, o número impresso é o da corrida deste lançamento (o executar_fase3.py já
# conta epocas+1 passadas de diagnóstico e epocas de proposta a partir de --epocas).
Rodar (@("executar_fase3.py", "--modelos") + $Modelos + @("--so-projecao", "--epocas", $Epocas, "--saida", $Saida) + $ExtrasCasos)
# ! Alteração de IA - Revisar: a parada de um modelo (código de saída diferente de 0 do
# executar_fase3.py, ou modelo pulado por falta de RAM em EsperarRam) passa a ser anotada em
# $Falhas, com AVISO no log; o laço continua no próximo modelo, como antes - onda final de
# correções.
# ! Motivo: o código de saída do executar_fase3.py não era conferido e o "PULADO" do
# EsperarRam não entrava em resumo nenhum: se o Ollama caísse (3 tentativas esgotadas ->
# SystemExit -> código 1), se a RAM não liberasse em 5 min ou se um modelo não estivesse
# baixado, o script seguia para a avaliação com dados parciais, imprimia "FIM da Fase 3" e
# terminava com código 0 - numa corrida de ~60 h de madrugada a falha só aparecia procurando
# "!!" no log. Seguir para o próximo modelo continua certo (cada modelo tem a própria cópia
# da biblioteca e o próprio JSONL); o que muda é o desfecho: FIM lista os modelos com falha e
# o script sai com código 1.
$Falhas = @()
foreach ($m in $Modelos) {
    if (EsperarRam $m) {
        Marco ("{0}: {1} epoca(s) de aprendizado + passada final  (RAM livre {2} GB)" -f $m, $Epocas, (RamLivreGB))
        Rodar (@("executar_fase3.py", "--modelos", $m, "--epocas", $Epocas, "--saida", $Saida) + $ExtrasCasos)
        if ($LASTEXITCODE -ne 0) {
            $Falhas += $m
            Marco ("AVISO: {0} terminou com codigo {1} - veja as linhas '!!' acima; relance o script para retomar" -f $m, $LASTEXITCODE)
        }
    } else {
        $Falhas += $m
    }
}

# ---------- 3. avaliação, comparação com as fases 2-A/2-B, gráficos e relatório ----------
if (-not $SemAvaliacao) {
    Marco "avaliacao"
    Rodar @("avaliar_fase3.py", "--saida", $Saida, "--gerar-revisao")
    Marco "comparacao com as fases 2-A e 2-B"
    Rodar @("comparar_fases.py", "--saida", $Saida)
    Marco "graficos (venv com matplotlib)"
    # mesma troca de Tee-Object por ForEach-Object explicada acima, na função Rodar.
    & $Venv gerar_graficos_fase3.py --saida $Saida 2>&1 | ForEach-Object {
        Write-Host $_
        Add-Content -Path $Log -Value $_ -Encoding utf8
    }
    Marco "relatorio"
    Rodar @("gerar_relatorio_fase3.py", "--saida", $Saida)
}

$duracao = (Get-Date) - $Inicio
# ! Alteração de IA - Revisar: o FIM diz quais modelos falharam/foram pulados e o script sai
# com código 1 quando houve algum - onda final de correções (ver $Falhas, acima).
# ! Motivo: "FIM da Fase 3" com código 0 e um modelo faltando era enganoso; com a lista no
# marco e o código 1, quem encadeia o script ou lê só a última linha do log sabe que precisa
# relançar (a retomada refaz só o que faltou).
$textoFalhas = if ($Falhas.Count -gt 0) { $Falhas -join ", " } else { "nenhum" }
Marco ("FIM da Fase 3 - duracao total {0:d2}h{1:d2} - modelos com falha: {2}" -f [int]$duracao.TotalHours, $duracao.Minutes, $textoFalhas)
if ($Falhas.Count -gt 0) { exit 1 }
