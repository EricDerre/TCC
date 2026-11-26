# ! Alteracao de IA - Revisar: (25/11/2026, Pos-Fase 4, pacotes Q6 e Q7, ficha 99) lancador da fumaca real da selecao pelo Git e do trace na falha:
# roda pelo rodar_fase4.ps1 os dez cenarios do ensaio, uma repeticao de cada, com -Selecao git, -Desde <commit> e -TraceNaFalha, na pasta
# fase4_fumaca_q7; depois mostra o que a selecao decidiria de novo (com o commit desta corrida ja registrado), confere a corrida contra a rodada
# completa (impacto_git.py --conferir) e lista os traces gravados. Para na primeira etapa que falhar.
# ! Motivo: os pacotes Q6 e Q7 foram provados sem o modelo e sem as cobaias (testes com navegador de mentira, repositorio temporario e uma conta
# sobre o historico); o plano (secao 7, Q7) preve "maquina por minutos". A corrida com o modelo nao roda de dentro do aplicativo Claude (a RAM
# que o rodar_fase4.ps1 exige nao existe com ele aberto, decisao 112), entao ela fica num comando so, para a janela do Eric. -Casos 10 roda os
# dez cenarios e marca a corrida como parcial: com o trace ligado os tempos nao valem como medida, e a corrida nao pode gravar leitura oficial.
#
# Uso, numa janela do PowerShell, com o VS Code e o aplicativo Claude fechados (a RAM livre precisa chegar a 6,5 GB):
#   powershell -ExecutionPolicy Bypass -File "C:\Users\Eric.Derre\Documents\TCC\Programacao\AgenteCore\experimentos\rodar_fumaca_q7.ps1"
#
# Opcoes: -Saida (pasta da corrida, padrao fase4_fumaca_q7); -Desde (o commit testado de onde o diff parte, padrao 717f68c2, o ultimo que
# mexeu nas cobaias); -Completa (a rodada completa da conferencia, padrao fase5_agente_b, a corrida 28b).
# O rodar_fase4.ps1 roda antes a bateria testar_fase4.py (que usa o banco), confere Ollama, RAM e versao, e grava fase4.log na pasta da corrida.
param(
    [string]$Saida = "fase4_fumaca_q7",
    [string]$Desde = "717f68c2",
    [string]$Completa = "fase5_agente_b"
)
$ErrorActionPreference = "Stop"
Set-Location -LiteralPath $PSScriptRoot
$env:RESULTADOS_DIR = "resultados_alvo"
$env:PYTHONIOENCODING = "utf-8"
$env:PYTHONUNBUFFERED = "1"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

function Passo([string]$Msg) {
    Write-Host ("[{0}] {1}" -f (Get-Date -Format "dd/MM HH:mm:ss"), $Msg)
}

Passo "1 de 4: os dez cenarios, uma repeticao, com a selecao pelo Git (desde $Desde) e o trace na falha"
& powershell -ExecutionPolicy Bypass -File (Join-Path $PSScriptRoot "rodar_fase4.ps1") -Modo cenarios -Saida $Saida -Casos 10 -Repeticoes 1 -Selecao git -Desde $Desde -TraceNaFalha
if ($LASTEXITCODE -ne 0) {
    # se a corrida ja gravou cenarios.jsonl, o que falhou foi uma etapa depois dela (a leitura do avaliador, por exemplo): a conferencia ainda vale
    $Gravado = Join-Path (Join-Path (Join-Path $PSScriptRoot "resultados_alvo") $Saida) "cenarios.jsonl"
    if (-not (Test-Path $Gravado)) {
        Passo "!! a corrida parou com codigo $LASTEXITCODE antes de gravar cenarios.jsonl; veja resultados_alvo\$Saida\fase4.log"
        exit $LASTEXITCODE
    }
    Passo "aviso: o rodar_fase4.ps1 saiu com codigo $LASTEXITCODE depois de a corrida gravar cenarios.jsonl; sigo com a decisao, a conferencia e os traces"
}

Passo "2 de 4: o que a selecao decidiria agora, com o commit desta corrida ja registrado (espera-se: nada a rodar)"
& python impacto_git.py --decidir
if ($LASTEXITCODE -ne 0) { Passo "!! impacto_git.py --decidir saiu com codigo $LASTEXITCODE"; exit $LASTEXITCODE }

Passo "3 de 4: a conferencia desta corrida contra a rodada completa ($Completa)"
& python impacto_git.py --conferir $Saida --completa $Completa
if ($LASTEXITCODE -ne 0) { Passo "!! impacto_git.py --conferir saiu com codigo $LASTEXITCODE"; exit $LASTEXITCODE }

Passo "4 de 4: os traces gravados (um por roteiro que falhou)"
$PastaDosTraces = Join-Path (Join-Path (Join-Path $PSScriptRoot "resultados_alvo") $Saida) "traces"
if (Test-Path $PastaDosTraces) {
    Get-ChildItem -LiteralPath $PastaDosTraces -Filter "*.zip" | ForEach-Object { Write-Host ("  {0} ({1} KB)" -f $_.Name, [int]($_.Length / 1024)) }
} else {
    Write-Host "  nenhum trace gravado: nenhum roteiro falhou, ou a opcao nao chegou ao executor"
}
Passo "FIM. Para ver a corrida no hub: python hub.py --corridas $Saida"
exit 0
