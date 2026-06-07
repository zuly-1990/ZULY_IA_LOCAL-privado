# consolidate_bisect_patterns.py
import sys
import os
import json
from pathlib import Path

# Agregar el directorio raíz al path para importar módulos de core
sys.path.append(os.path.abspath(os.getcwd()))

from core.assembly.pattern_storage import PatternStorage
from core.cognition.memory.heuristic_memory import HeuristicMemory
from core.utils.logging import log_success, log_info

def consolidate():
    storage = PatternStorage()
    h_memory = HeuristicMemory()
    
    # 1. Patrón: Corte de Sección (Bisect Workflow)
    bisect_components = [
        {
            "id": "operacion_bisect",
            "type": "mesh_operation",
            "technique": "bisect_fill_clear",
            "description": "Corte de sección con limpieza de mitad y sellado de caras"
        }
    ]
    storage.save_pattern(
        "corte_seccion_tecnico", 
        "Técnica de bisección para visualización arquitectónica. Incluye 'Clear' para vista seccionada y 'Fill' para realismo.",
        bisect_components
    )

    # 2. Patrón: Protección de Geometría (Non-Selectable)
    protection_components = [
        {
            "id": "geometria_protegida",
            "type": "outliner_flag",
            "action": "disable_selection",
            "description": "Inhabilitar selección para evitar que operaciones globales (A -> Bisect) afecten al objeto"
        }
    ]
    storage.save_pattern(
        "proteccion_geometria_operativa", 
        "Uso de flags del Outliner para proteger bases o terrenos de cortes de sección globales.",
        protection_components
    )

    # Registrar experiencia técnica
    diagnosis = {
        "findings": [
            "Técnica de visualización mediante Bisect validada.",
            "Importancia de la geometría limpia para el comando 'Fill' detectada.",
            "Uso estratégico de la seleccionabilidad en el Outliner para proteger objetos."
        ]
    }
    
    h_memory.store_experience(
        "architectural_section_visualization", 
        {"operation": "bpy.ops.mesh.bisect", "options": ["fill", "clear_inner", "clear_outer"]}, 
        0.95, 
        diagnosis
    )
    
    log_success("Patrones de bisección y protección consolidados exitosamente.")

if __name__ == "__main__":
    consolidate()
