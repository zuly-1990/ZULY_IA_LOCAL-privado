#!/bin/bash
# Script de despliegue ZULY en Hetzner
echo "🚀 Iniciando despliegue ZULY..."

# Actualizar código
cd /opt/zuly
git pull origin main

# Correr pruebas
echo "🧪 Corriendo suite de pruebas..."
blender --background --python tools/zuly_qa_runner.py

echo "✅ Ciclo completado"
