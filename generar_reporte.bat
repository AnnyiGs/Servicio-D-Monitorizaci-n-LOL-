@echo off
chcp 65001 >nul
echo =================================
echo    ABRIENDO REPORTE ACTUAL
echo =================================
echo.
echo Ubicacion: %CD%
echo.

if exist "%CD%\reporte_lol.txt" (
    echo 📊 REPORTE ACTUAL:
    echo ======================
    type "%CD%\reporte_lol.txt"
    echo.
    echo ¿Quieres abrir el archivo completo? (S/N)
    set /p respuesta=
    if /i "%respuesta%"=="S" (
        notepad "%CD%\reporte_lol.txt"
    )
) else (
    echo ❌ No hay reporte disponible todavía
    echo Juega League of Legends para generar datos
)

echo.
pause