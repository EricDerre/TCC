# ! Alteracao de IA - Revisar: (08/11/2026, Pos-Fase 4, pacote Q4, ficha 60) lancador da fumaca real da barra de progresso: roda pelo rodar_fase4.ps1 uma
# inferencia do modelo no modo ineditos (um caso em texto, sem navegador nem cobaias) na pasta fase4_fumaca_progresso, depois resume as medidas da barra
# (progresso.py --fumaca) em resultados_alvo\fase4\fumaca_progresso.{json,md}, regera o painel e roda os testes dele. Para na primeira etapa que falhar.
# ! Motivo: o plano aprovado (secao 7, Q4) pede uma fumaca real de um caso para medir o erro da estimativa; a fumaca lancada de dentro do aplicativo Claude
# em 08/11/2026 parou na checagem de RAM (3,9 GB livres contra os 6,5 GB que o rodar_fase4.ps1 exige), e o Eric prefere fechar o aplicativo e lancar na
# janela dele: um comando so, com a leitura e o painel no fim, para nao esquecer nenhuma etapa. O registro dos numeros no roadmap e a republicacao do
# painel ficam para a proxima sessao do Claude, que le fumaca_progresso.json.
#
# Uso, numa janela do PowerShell, com o VS Code e o aplicativo Claude fechados (a RAM livre precisa chegar a 6,5 GB):
#   powershell -ExecutionPolicy Bypass -File "C:\Users\Eric.Derre\Documents\TCC\Programacao\AgenteCore\experimentos\rodar_fumaca_progresso.ps1"
#
# Opcoes: -Saida (pasta da corrida, padrao fase4_fumaca_progresso); -Casos (quantos casos, padrao 1); -SemPainel (nao regera o painel).
# O rodar_fase4.ps1 roda antes a bateria testar_fase4.py, confere Ollama, RAM e versao, e grava fase4.log na pasta da corrida; a barra sai no console
# e o estado dela fica em resultados_alvo\<Saida>\progresso.json. Relancar com a mesma -Saida retoma o que faltar.
param(
    [string]$Saida = "fase4_fumaca_progresso",
    [int]$Casos = 1,
    [switch]$SemPainel
)
$ErrorActionPreference = "Stop"
Set-Location -LiteralPath $PSScriptRoot
$env:RESULTADOS_DIR = "resultados_alvo"
$env:PYTHONIOENCODING = "utf-8"
$env:PYTHONUNBUFFERED = "1"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$Raiz = (Resolve-Path (Join-Path $PSScriptRoot "..\..\..")).Path

function Passo([string]$Msg) {
    Write-Host ("[{0}] {1}" -f (Get-Date -Format "dd/MM HH:mm:ss"), $Msg)
}
function Parar([string]$Msg, [int]$Codigo) {
    Passo ("!! {0} (codigo {1}); a fumaca parou aqui" -f $Msg, $Codigo)
    exit $Codigo
}

Passo ("fumaca real da barra de progresso: rodar_fase4.ps1 -Modo ineditos -Saida {0} -Casos {1}" -f $Saida, $Casos)
& powershell -ExecutionPolicy Bypass -File ".\rodar_fase4.ps1" -Modo ineditos -Saida $Saida -Casos $Casos
if ($LASTEXITCODE -ne 0) { Parar "rodar_fase4.ps1 saiu com erro" $LASTEXITCODE }

$Pasta = Join-Path (Join-Path $PSScriptRoot "resultados_alvo") $Saida
Passo ("leitura das medidas da barra: progresso.py --fumaca {0}" -f $Pasta)
& python progresso.py --fumaca $Pasta
if ($LASTEXITCODE -ne 0) { Parar "progresso.py --fumaca saiu com erro" $LASTEXITCODE }
& python progresso.py --fumaca $Pasta --check
if ($LASTEXITCODE -ne 0) { Parar "progresso.py --fumaca --check difere do gravado" $LASTEXITCODE }

if (-not $SemPainel) {
    Passo "painel: gerar_dashboard.py, testar_painel_textos.py e testar_painel_topicos.py"
    & python (Join-Path $Raiz "ferramentas\gerar_dashboard.py")
    if ($LASTEXITCODE -ne 0) { Parar "gerar_dashboard.py saiu com erro" $LASTEXITCODE }
    & python (Join-Path $Raiz "ferramentas\testar_painel_textos.py")
    if ($LASTEXITCODE -ne 0) { Parar "testar_painel_textos.py falhou" $LASTEXITCODE }
    & python (Join-Path $Raiz "ferramentas\testar_painel_topicos.py")
    if ($LASTEXITCODE -ne 0) { Parar "testar_painel_topicos.py falhou" $LASTEXITCODE }
}

Passo ("FIM: o estimado contra o medido por fase esta em resultados_alvo\fase4\fumaca_progresso.md (e .json); o estado da barra em {0}\progresso.json; a aba 'Barra e Git' do painel ja le o arquivo" -f $Pasta)
Passo "proxima sessao do Claude: registrar os numeros no roadmap (secao 4.8, paragrafo do Q4) e republicar o painel no mesmo endereco"
exit 0
