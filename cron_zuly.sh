#!/bin/bash
# Ejecutar cada 6 horas automáticamente
# Agregar a crontab: 0 */6 * * * /opt/zuly/cron_zuly.sh
/opt/zuly/deploy.sh >> /opt/zuly/logs/cron.log 2>&1
