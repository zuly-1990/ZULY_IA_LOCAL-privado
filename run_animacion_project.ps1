# run_animacion_project.ps1
# Script para ejecutar la Animación Simple

$blender_paths = @(
    "C:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe",
    "C:\Program Files\Blender Foundation\Blender 3.6\blender.exe",
    "$env:ProgramFiles\Blender Foundation\Blender 3.6\blender.exe"
)

$blender_exe = $null
foreach ($path in $blender_paths) {
    if (Test-Path $path) {
        $blender_exe = $path
        break
    }
}

if ($null -eq $blender_exe) {
    Write-Host "[ERROR] Blender no encontrado" -ForegroundColor Red
    exit 1
}

Write-Host "[OK] Blender encontrado." -ForegroundColor Green
Write-Host "Renderizando animacion de 5 segundos (EEVEE)..." -ForegroundColor Cyan

$script_path = (Get-Item "proyecto_animacion_cubo.py").FullName
& "$blender_exe" --background --python "$script_path"

Write-Host "`n[LISTO] Animacion completada!" -ForegroundColor Green
Write-Host "Revisa la carpeta export/animaciones" -ForegroundColor Cyan
