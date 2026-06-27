#!/bin/bash
# Zuly Backup Manager
# Comprime la libreria 3D y la sube a MEGA

LIBRERIA_DIR="/opt/zuly/libreria_3d/arquitectura"
BACKUP_DIR="/opt/zuly/libreria_3d/backups"
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M")
BACKUP_FILE="${BACKUP_DIR}/zuly_backup_${TIMESTAMP}.tar.gz"

mkdir -p "$BACKUP_DIR"

echo "[$(date)] Iniciando Backup a MEGA..."

# Comprimir la carpeta de arquitectura
tar -czf "$BACKUP_FILE" "$LIBRERIA_DIR"

# Verificar si se comprimio bien
if [ -f "$BACKUP_FILE" ]; then
    echo "[$(date)] Archivo comprimido creado: $BACKUP_FILE. Subiendo a MEGA..."
    
    # Subir a MEGA usando rclone
    /usr/bin/rclone copy "$BACKUP_FILE" zuly_mega:Zuly_Backups/
    
    if [ $? -eq 0 ]; then
        echo "[$(date)] Subida exitosa a MEGA."
        
        # Limpiar backups locales antiguos (mantener solo el ultimo)
        ls -t ${BACKUP_DIR}/zuly_backup_*.tar.gz | tail -n +2 | xargs -I {} rm -- {}
    else
        echo "[$(date)] Error subiendo a MEGA."
    fi
else
    echo "[$(date)] Error comprimiendo la libreria."
fi

echo "[$(date)] Proceso de Backup finalizado."
