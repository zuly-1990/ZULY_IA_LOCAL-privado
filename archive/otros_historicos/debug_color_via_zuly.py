#!/usr/bin/env python3
"""
Script para debug del handler de color usando Zuly
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from core.agent import Agent
from core.utils.logging import log

def main():
    log("Iniciando debug del handler de color")

    # Crear agente
    agent = Agent()

    # Ejecutar el handler de color
    try:
        result = agent.execute_via_router('blender.set_material_color', {
            'material_name': 'BlueDot',
            'color': [1.0, 0.0, 0.0, 1.0]  # Rojo
        })

        log(f"Resultado del handler: {result}")

        # Verificar el color actual
        check_result = agent.execute_via_router('blender.get_material_color', {
            'material_name': 'BlueDot'
        })

        log(f"Color actual del material: {check_result}")

    except Exception as e:
        log(f"Error ejecutando handler: {e}")

if __name__ == "__main__":
    main()