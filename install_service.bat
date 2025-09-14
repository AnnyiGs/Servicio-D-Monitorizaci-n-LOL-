@echo off
chcp 65001 >nul
echo ========================================
echo    INSTALADOR SERVICIO MONITOR LOL
echo ========================================
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

echo Instalando dependencias necesarias...
pip install pywin32 psutil

echo Instalando servicio...
python "%CD%\lol_monitor.py" install

echo Iniciando servicio...
python "%CD%\lol_monitor.py" start

echo.
echo ✅ SERVICIO INSTALADO CORRECTAMENTE
echo.
echo 📍 Ubicacion: %CD%
echo 📍 Reporte: %CD%\reporte_lol.txt
echo.
echo El servicio funciona desde esta ubicacion
echo No muevas los archivos después de instalar
echo.
pause