@echo off
rem ! Alteracao de IA - Revisar: atalho clicavel que chama o install.ps1 com
rem -ExecutionPolicy Bypass.
rem ! Motivo: por padrao o Windows bloqueia script .ps1 nao assinado, e rodar
rem .\install.ps1 direto falha com PSSecurityException - foi o erro que apareceu
rem na pratica. O Bypass aqui vale so para esta execucao, entao resolve sem
rem alterar nenhuma configuracao permanente da maquina de quem clonou.
rem SEM ACENTO de proposito: testado que o cmd.exe le o arquivo na codepage OEM e
rem os bytes UTF-8 de c-cedilha/til re-tokenizam a linha rem, imprimindo um erro
rem espurio antes do script rodar.
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0install.ps1" %*
rem ! Alteracao de IA - Revisar: guarda o codigo de saida do install.ps1 antes do pause e devolve ele no fim.
rem ! Motivo: execucao 45650086543 do GitHub Actions, celula CI-WIN: o instalador parou com erro, mas o install.cmd
rem terminava em pause e saia com codigo 0, entao o fluxo seguia como se a instalacao tivesse dado certo.
set "COBAIA_CODIGO=%ERRORLEVEL%"
pause
exit /b %COBAIA_CODIGO%
