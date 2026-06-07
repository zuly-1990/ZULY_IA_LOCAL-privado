#!/usr/bin/env bash
# blender_run_test.sh
# Script para ejecutar pruebas en Blender desde línea de comandos

# Detectar sistema operativo
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    # Windows
    BLENDER_PATH="C:\Program Files\Blender Foundation\Blender 3.6\blender.exe"
else
    # Linux/Mac
    BLENDER_PATH=$(which blender)
fi

if [ ! -f "$BLENDER_PATH" ]; then
    echo "❌ Blender no encontrado en: $BLENDER_PATH"
    echo "Cambia la ruta según tu instalación"
    exit 1
fi

echo "Ejecutando pruebas en Blender..."
"$BLENDER_PATH" --background --python blender_test.py
