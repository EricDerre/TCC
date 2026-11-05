# ! Alteracao de IA - Revisar: (05/11/2026, decisoes 90, 91 e 96) fila das corridas 18c, 21c e 23 da Fase 4, uma depois da outra, pelo rodar_fase4.ps1.
# ! Motivo: as tres somam cerca de 5 horas de maquina e nao dependem da conferencia da ficha 46; em fila, o Eric lanca uma vez so, com a maquina livre, e a
# fila para na primeira que falhar, em vez de seguir com uma corrida quebrada. A corrida 24 fica de fora porque espera a conferencia (decisao 92).
#
# Uso, numa janela do PowerShell, com o VS Code e o Claude fechados:
#   powershell -ExecutionPolicy Bypass -File "C:\Users\Eric.Derre\Documents\TCC\Programacao\AgenteCore\experimentos\rodar_pendencias_fase4.ps1"
#
# Cada corrida roda a bateria de testes, confere Ollama, RAM e versao, roda o modelo e grava a leitura ao fim. Relancar a fila retoma: o que ja foi
# diagnosticado nao roda de novo, e a bateria e a leitura de cada corrida repetem.
Set-Location -LiteralPath $PSScriptRoot
$Fila = @(
    @{ Nome = "18c"; Argumentos = @("-Modo", "tela", "-Saida", "fase4_tela_v3", "-Nome", "tela_v3") },
    @{ Nome = "21c"; Argumentos = @("-Modo", "cenarios", "-Saida", "fase4_ensaio_v3", "-Repeticoes", "1", "-Nome", "cenarios_v3") },
    @{ Nome = "23"; Argumentos = @("-Modo", "experimento_prompt", "-Saida", "fase4_experimento") }
)
foreach ($Corrida in $Fila) {
    Write-Host ("[{0}] corrida {1}: {2}" -f (Get-Date -Format "dd/MM HH:mm"), $Corrida.Nome, ($Corrida.Argumentos -join " "))
    & powershell -ExecutionPolicy Bypass -File ".\rodar_fase4.ps1" $Corrida.Argumentos
    if ($LASTEXITCODE -ne 0) {
        Write-Host ("[{0}] !! a corrida {1} saiu com codigo {2}; a fila parou aqui" -f (Get-Date -Format "dd/MM HH:mm"), $Corrida.Nome, $LASTEXITCODE)
        exit $LASTEXITCODE
    }
    Write-Host ("[{0}] corrida {1} terminou" -f (Get-Date -Format "dd/MM HH:mm"), $Corrida.Nome)
}
Write-Host ("[{0}] fila terminada; o log de cada corrida fica em resultados_alvo\<Saida>\fase4.log" -f (Get-Date -Format "dd/MM HH:mm"))
