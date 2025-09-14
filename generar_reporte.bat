@echo off
chcp 65001 >nul
echo =================================
echo    REPORTE DE TIEMPO LOL
echo =================================
echo.

if exist "reporte_lol.txt" (
    type "reporte_lol.txt"
    echo.
    set /p respuesta="¿Abrir reporte completo? (s/n): "
    if /i "%respuesta%"=="s" (
        notepad "reporte_lol.txt"
    )
) else (
    echo No hay reporte disponible todavia
    echo Juega League of Legends primero
)

echo.
pause
