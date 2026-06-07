# backup_zuly.ps1
# Respaldo simple sin caracteres especiales para evitar errores de codificación

$Timestamp = Get-Date -Format "yyyyMMdd_HHmm"
$BackupDir = "backups"
$ZipFile = "$BackupDir\ZULY_BACKUP_$Timestamp.zip"

if (!(Test-Path $BackupDir)) {
    New-Item -ItemType Directory -Path $BackupDir
}

Write-Output "Iniciando respaldo..."

# Filtrar archivos para no incluir carpetas pesadas
$Items = Get-ChildItem -Path . -Exclude ".venv", "zuly_env", ".pytest_cache", "backups"

Compress-Archive -Path $Items.FullName -DestinationPath $ZipFile -Force

if (Test-Path $ZipFile) {
    Write-Output "Respaldo exitoso: $ZipFile"
}
else {
    Write-Output "Error en el respaldo"
}
