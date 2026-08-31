@echo off
rem AI-generated wrapper - review if changed.
rem Double-clickable: avoids the PowerShell Execution Policy error
rem (unsigned .ps1 scripts are blocked by default on Windows) without
rem changing any persistent system setting -- ExecutionPolicy Bypass
rem only applies to this one invocation.
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0install.ps1" %*
pause
