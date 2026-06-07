# execute_lab_real.ps1
# Script para ejecutar el Laboratorio Plan D en Blender real

$blender_exe = "C:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe"
$script_path = "C:\Users\Admin\Desktop\ZULY_IA_LOCAL\run_plan_d_laboratory.py"

if (-not (Test-Path $blender_exe)) {
    Write-Host "❌ Blender no encontrado en: $blender_exe" -ForegroundColor Red
    exit 1
}

Write-Host "🚀 Iniciando PLAN D - LABORATORIO A1 (REAL)" -ForegroundColor Cyan
Write-Host "Blender: $blender_exe"
Write-Host "Script: $script_path"
Write-Host "-------------------------------------------------------"

# Ejecutar Blender en background con el script del laboratorio
& "$blender_exe" --background --python "$script_path"

Write-Host "-------------------------------------------------------"
Write-Host "✅ Ejecución del laboratorio completada." -ForegroundColor Green
