# consolidate_reinforcement_patterns.py
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
    
    # 1. Patrón: Trazado de Muros (Plane Tracing)
    wall_tracing_components = [
        {
            "id": "segmento_muro_base",
            "type": "plane",
            "technique": "loop_cut_extrude",
            "description": "Plano inicial que se subdivide y extruye siguiendo el calco"
        }
    ]
    storage.save_pattern(
        "trazado_muros_2d", 
        "Técnica de modelado de muros desde plano 2D usando planos, loop-cuts (Ctrl+R) y extrusión (E).",
        wall_tracing_components
    )

    # 2. Patrón: Cubierta/Suelo (Single Vert Method)
    single_vert_components = [
        {
            "id": "perimetro_vertices",
            "type": "mesh_from_verts",
            "technique": "single_vert_fill",
            "description": "Perímetro trazado con vértices simples y rellenado con F"
        }
    ]
    storage.save_pattern(
        "suelo_techo_perimetral", 
        "Técnica para crear suelos o techos complejos trazando vértices uno a uno y rellenando la cara resultante.",
        single_vert_components
    )

    # Registrar experiencias en HeuristicMemory
    diagnosis = {
        "findings": [
            "Técnica de trazado desde AutoCAD validada.",
            "Uso de Loop Cut para ramificaciones de muros detectado.",
            "Método de Single Vert para perímetros complejos identificado."
        ]
    }
    
    h_memory.store_experience(
        "architectural_workflow_cad_to_3d", 
        {"workflow": ["plane_tracing", "single_vert", "loop_cuts"]}, 
        0.9, 
        diagnosis
    )
    
    log_success("Patrones de refuerzo y experiencia técnica consolidados exitosamente.")

if __name__ == "__main__":
    consolidate()
