@echo off
chcp 65001 >nul
echo ========================================
echo    INSTALADOR CORREGIDO - MONITOR LOL
echo ========================================
echo.

:: Verificar permisos de administrador
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ERROR: Debes ejecutar como Administrador
    echo Haz clic derecho -> "Ejecutar como administrador"
    pause
    exit /b 1
)

echo [1/5] Verificando Python...
python --version

echo [2/5] Instalando dependencias...
pip install pywin32 psutil

echo [3/5] Registrando servicio...
cd /d "%~dp0"
python "%~dp0lol_monitor.py" install

echo [4/5] Iniciando servicio...
python "%~dp0lol_monitor.py" start

echo [5/5] Verificando instalacion...
timeout /t 3 /nobreak >nul
sc query LolTimeTracker | findstr "STATE"

echo.
echo ✅ INSTALACION COMPLETADA
echo.
echo Servicio: League of Legends Time Tracker
echo Estado: Debe aparecer como RUNNING
echo.
pause
