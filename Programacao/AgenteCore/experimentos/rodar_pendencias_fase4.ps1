# ! Alteracao de IA - Revisar: (06/11/2026, decisao 97) fila das corridas 18d, 21d e 18e, com os sinais da busca contra a referencia, uma depois da outra, pelo rodar_fase4.ps1.
# ! Motivo: os sinais foram escritos olhando os 37 casos de avaliacao, entao a 18d e a 21d medem o efeito neles e nos dez cenarios, e a 18e confere nos 25 ineditos que reproduzem na tela, que a busca nunca viu.
# Em fila, o Eric lanca uma vez so, com a maquina livre, e a fila para na primeira que falhar. A corrida 24 fica de fora porque espera a conferencia da ficha 46 (decisao 92).
# A versao anterior desta fila rodou as corridas 18c, 21c e 23 em 05/11/2026; os comandos delas estao no roadmap.
#
# Uso, numa janela do PowerShell, com o VS Code e o Claude fechados:
#   powershell -ExecutionPolicy Bypass -File "C:\Users\Eric.Derre\Documents\TCC\Programacao\AgenteCore\experimentos\rodar_pendencias_fase4.ps1"
#
# Cada corrida roda a bateria de testes, confere Ollama, RAM e versao, roda o modelo e grava a leitura ao fim. Relancar a fila retoma: o que ja foi
# diagnosticado nao roda de novo, e a bateria e a leitura de cada corrida repetem.
Set-Location -LiteralPath $PSScriptRoot
$Fila = @(
    @{ Nome = "18d"; Argumentos = @("-Modo", "tela", "-Saida", "fase4_tela_v4", "-Nome", "tela_v4") },
    @{ Nome = "21d"; Argumentos = @("-Modo", "cenarios", "-Saida", "fase4_ensaio_v4", "-Repeticoes", "1", "-Nome", "cenarios_v4") },
    @{ Nome = "18e"; Argumentos = @("-Modo", "tela", "-Saida", "fase4_tela_ineditos", "-Nome", "tela_ineditos", "-Banco", "ineditos_fase4") }
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
