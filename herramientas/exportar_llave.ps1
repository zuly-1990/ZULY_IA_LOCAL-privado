# exportar_llave.ps1
# Herramienta para mover tu identidad Zuly a una Bóveda USB

$ProjectDir = Get-Location
$KeyFile = ".zuly_identity.key"
$KeyPath = Join-Path $ProjectDir $KeyFile

if (!(Test-Path $KeyPath)) {
    Write-Host "✗ No se encontró la llave local en $ProjectDir" -ForegroundColor Red
    exit
}

$Drives = Get-PSDrive -PSProvider FileSystem | Where-Object { $_.DisplayRoot -ne $null }
Write-Host "--- DETECTOR DE BÓVEDAS USB ---" -ForegroundColor Cyan
$i = 1
$DriveList = @()

foreach ($Drive in $Drives) {
    Write-Host "$i) $($Drive.Name): [$($Drive.DisplayRoot)]"
    $DriveList += $Drive.Name + ":"
    $i++
}

$Choice = Read-Host "Selecciona el número de la unidad USB para tu Bóveda"
$TargetDrive = $DriveList[$Choice - 1]

if ($TargetDrive) {
    $VaultDir = Join-Path $TargetDrive "ZULY_VAULT"
    if (!(Test-Path $VaultDir)) {
        New-Item -ItemType Directory -Path $VaultDir
    }
    
    Copy-Item -Path $KeyPath -Destination (Join-Path $VaultDir $KeyFile) -Force
    Write-Host "✓ ¡Llave exportada a la Bóveda en $TargetDrive\ZULY_VAULT!" -ForegroundColor Green
    Write-Host "Ahora puedes borrar el archivo .zuly_identity.key de la PC si quieres máxima seguridad." -ForegroundColor Yellow
}
else {
    Write-Host "Selección inválida." -ForegroundColor Red
}
