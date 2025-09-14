@echo off
chcp 65001 >nul
echo ==========================================
echo    DESINSTALADOR SERVICIO MONITOR LOL
echo ==========================================
echo.
echo Ubicacion actual: %CD%
echo.

:: Verificar permisos de administrador
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ERROR: Debes ejecutar como Administrador
    echo Haz clic derecho -> "Ejecutar como administrador"
    pause
    exit /b 1
)

echo Deteniendo servicio...
python "%CD%\lol_monitor.py" stop

echo Desinstalando servicio...
python "%CD%\lol_monitor.py" remove

echo.
echo ✅ SERVICIO DESINSTALADO CORRECTAMENTE
echo.
pause