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
pause
