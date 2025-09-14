@echo off
echo ==========================================
echo    DESINSTALADOR SERVICIO MONITOR LOL
echo ==========================================
echo.

:: Cambiar a la carpeta donde está este archivo
cd /d "%~dp0"

:: Verificar si es administrador
net session >nul 2>&1
if not %errorLevel% == 0 (
    echo ERROR: Debes ejecutar como Administrador
    echo Haz clic derecho -> "Ejecutar como administrador"
    pause
    exit /b 1
)

echo Deteniendo servicio...
python lol_monitor.py stop

echo Desinstalando servicio...
python lol_monitor.py remove

echo.
echo SERVICIO DESINSTALADO CORRECTAMENTE
echo.
pause
