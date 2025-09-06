@echo off
setlocal

:: Ruta del script PowerShell
set PS_SCRIPT=%~dp0install_classroom_software.ps1

set PS_UV=%~dp0env_uv.ps1

:: Ejecutar PowerShell con política temporal de ejecución
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%PS_SCRIPT%"

:: powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%PS_UV%"

echo.
pause
