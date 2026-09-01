@echo off
rem ! Alteracao de IA - Revisar: atalho clicavel que chama o run.ps1 com
rem -ExecutionPolicy Bypass.
rem ! Motivo: mesma razao do install.cmd - o Windows bloqueia .ps1 nao assinado por
rem padrao e chamar .\run.ps1 direto falha com PSSecurityException. O Bypass vale so
rem para esta execucao, sem mexer em configuracao permanente da maquina.
rem SEM ACENTO de proposito: testado que o cmd.exe le o arquivo na codepage OEM e
rem os bytes UTF-8 de c-cedilha/til re-tokenizam a linha rem, imprimindo um erro
rem espurio antes do script rodar.
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0run.ps1" %*
pause
