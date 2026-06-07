"""
herramientas/scripts_externos/run_crear_primitiva.py
Script externo para ejecutar el comando CrearPrimitiva de Zuly.
Este script puede ser invocado directamente para realizar la creación de una primitiva en Blender,
utilizando la lógica definida en el núcleo de Zuly.
"""

import sys
import os

# Ajustar el PYTHONPATH para poder importar módulos de Zuly
# Asume que el script se ejecuta desde la raíz del proyecto Zuly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from core.commands.blender_commands import CrearPrimitiva
from core.agent import Agent

def main():
    """
    Función principal para ejecutar el comando CrearPrimitiva.
    """
    print("Iniciando ejecución del script run_crear_primitiva.py...")
    agente = Agent()
    comando_cubo = CrearPrimitiva()
    agente.ejecutar_comando(comando_cubo)
    print("Script run_crear_primitiva.py completado.")

if __name__ == "__main__":
    main()











