#!/usr/bin/env python3
"""
Script para ejecutar debug del handler de color dentro de Blender
"""

import bpy
import sys
from pathlib import Path

# Agregar el directorio del proyecto al path
project_dir = Path(__file__).parent
sys.path.insert(0, str(project_dir))

from core.agent import Agent
from core.utils.logging import log

def main():
    log("Iniciando debug del handler de color dentro de Blender")

    # Crear agente
    agent = Agent()

    # Primero crear el material
    try:
        create_result = agent.execute_via_router('blender.create_material', {
            'material_name': 'BlueDot',
            'color': [0.0, 0.3, 1.0, 1.0]  # Azul inicial
        })
        log(f"Resultado de creación de material: {create_result}")

        # Ahora cambiar el color usando el nombre correcto del material
        result = agent.execute_via_router('blender.set_material_color', {
            'material_name': 'Material_001',  # Usar el nombre real del material creado
            'color': [1.0, 0.0, 0.0, 1.0]  # Rojo
        })

        log(f"Resultado del handler de cambio de color: {result}")

        # Verificar el color actual (si existe el handler)
        try:
            check_result = agent.execute_via_router('blender.get_material_color', {
                'material_name': 'Material_001'  # Usar el nombre real
            })
            log(f"Color actual del material: {check_result}")
        except:
            log("No se pudo verificar el color (handler no disponible)")

    except Exception as e:
        log(f"Error ejecutando handlers: {e}")

if __name__ == "__main__":
    main()