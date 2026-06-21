# ZULY → Blender Real - Script de Ejecución
# PowerShell script para ejecutar ZULY con el Blender local

$ErrorActionPreference = "Stop"

$BLENDER_PATH = ".\blender\v3\blender-3.6.0-zuly\blender.exe"
$SCRIPT_PATH = ".\test_zuly_blender_real.py"

Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host "EJECUTANDO ZULY CON BLENDER REAL" -ForegroundColor Yellow
Write-Host "=====================================================================" -ForegroundColor Cyan

Write-Host ""
Write-Host "Blender: $BLENDER_PATH" -ForegroundColor Cyan
Write-Host "Script: $SCRIPT_PATH" -ForegroundColor Cyan
Write-Host ""
Write-Host "Ejecutando..." -ForegroundColor Green
Write-Host ""

# Ejecutar Blender en modo background con el script de ZULY
& $BLENDER_PATH --background --python $SCRIPT_PATH

Write-Host ""
Write-Host "Ejecucion completada" -ForegroundColor Green
Write-Host "Revisa el archivo test_zuly_real.blend para ver el resultado" -ForegroundColor Yellow
Write-Host ""
