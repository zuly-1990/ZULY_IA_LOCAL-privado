# run_cubo_project.ps1
# Script para ejecutar el Proyecto de Exploracion de Cubos (ASCII friendly)

# Detectar rutas posibles de Blender
$blender_paths = @(
    "C:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe",
    "C:\Program Files\Blender Foundation\Blender 3.6\blender.exe",
    "C:\Program Files\Blender Foundation\Blender 4.0\blender.exe",
    "$env:ProgramFiles\Blender Foundation\Blender 3.6\blender.exe"
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
    Write-Host "[ERROR] Blender no encontrado" -ForegroundColor Red
    Write-Host "Por favor, instala Blender 3.6 o ajusta la ruta en este script."
    exit 1
}

Write-Host "[OK] Blender encontrado: $blender_exe" -ForegroundColor Green
Write-Host "Iniciando Proyecto de Exploracion de Cubos..." -ForegroundColor Cyan
Write-Host "Esto tomara unos minutos (creacion + renderizado)..." -ForegroundColor Yellow

# Ejecutar script
$script_path = (Get-Item "proyecto_cubo_completo.py").FullName
& "$blender_exe" --background --python "$script_path"

Write-Host "`n[LISTO] Proyecto completado!" -ForegroundColor Green
Write-Host "Revisa la carpeta export/cubos para ver los resultados." -ForegroundColor Cyan
