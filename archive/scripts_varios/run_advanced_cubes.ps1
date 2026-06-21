# run_advanced_cubes.ps1
# Runner para las pruebas avanzadas de cubos

$ErrorActionPreference = "Stop"

# 1. Buscar Blender
$blender_paths = @(
    "C:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe",
    "C:\Program Files\Blender Foundation\Blender 3.6\blender.exe",
    "C:\Program Files\Blender Foundation\Blender 4.0\blender.exe",
    "$env:ProgramFiles\Blender Foundation\Blender 3.6\blender.exe"
)

$blender_exe = $null
foreach ($path in $blender_paths) {
    if (Test-Path $path) {
        $blender_exe = $path
        break
    }
}

if (-not $blender_exe) {
    Write-Error "No se encontró Blender en las rutas esperadas."
}

Write-Host "✅ Blender encontrado: $blender_exe" -ForegroundColor Green

# 2. Configurar rutas
$test_script = Join-Path (Get-Location) "tests\test_advanced_cubes.py"

if (-not (Test-Path $test_script)) {
    Write-Error "No se encontró el script de prueba en: $test_script"
}

# 3. Ejecutar
Write-Host "🚀 Iniciando pruebas avanzadas de cubos..." -ForegroundColor Cyan
Write-Host "   Script: $test_script"
Write-Host "   Espere, esto puede tardar unos segundos..."

try {
    & $blender_exe --background --python "$test_script"
    Write-Host "`n✨ Pruebas completadas exitosamente." -ForegroundColor Green
    Write-Host "   Revise la carpeta 'export/pruebas_cubo' para ver los resultados." -ForegroundColor Yellow
} catch {
    Write-Error "Falló la ejecución de Blender: $_"
}
