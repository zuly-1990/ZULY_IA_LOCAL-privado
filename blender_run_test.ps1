# blender_run_test.ps1
# Script PowerShell para ejecutar pruebas en Blender

# Detectar rutas posibles de Blender
$blender_paths = @(
    # RUTA LOCAL (únicamente disponible y verificada)
    "C:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe"
    # NOTA: Otras rutas comentadas porque no existen en el sistema
    # "C:\Program Files\Blender Foundation\Blender 3.6\blender.exe",
    # "C:\Program Files\Blender Foundation\Blender 4.0\blender.exe",
    # "C:\Program Files (x86)\Blender Foundation\Blender\blender.exe",
    # "$env:ProgramFiles\Blender Foundation\Blender 3.6\blender.exe"
)

# Buscar Blender
$blender_exe = $null
foreach ($path in $blender_paths) {
    if (Test-Path $path) {
        $blender_exe = $path
        break
    }
}

if ($null -eq $blender_exe) {
    Write-Host "❌ Blender no encontrado" -ForegroundColor Red
    Write-Host "Rutas buscadas:" -ForegroundColor Yellow
    foreach ($path in $blender_paths) {
        Write-Host "  - $path"
    }
    exit 1
}

Write-Host "✅ Blender encontrado: $blender_exe" -ForegroundColor Green
Write-Host "Ejecutando pruebas..." -ForegroundColor Cyan

# Ejecutar pruebas
$script_path = (Get-Item blender_test.py).FullName
& "$blender_exe" --background --python "$script_path"

Write-Host "`n✅ Pruebas completadas" -ForegroundColor Green
