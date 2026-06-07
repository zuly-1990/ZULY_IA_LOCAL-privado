# consolidate_villa_savoye_patterns.py
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
    
    # 1. Patrón: Columna Circular (Circular Column)
    circular_col_components = [
        {
            "id": "circulo_base",
            "type": "mesh_circle",
            "technique": "fill_extrude",
            "description": "Círculo de malla rellenado y extruido verticalmente"
        }
    ]
    storage.save_pattern(
        "columna_circular_tecnica", 
        "Creación de columnas cilíndricas perfectas desde una base de círculo de malla con sellado de cara.",
        circular_col_components
    )

    # 2. Patrón: Stack de Niveles (Z-Stacking Workflow)
    stacking_components = [
        {
            "id": "nivel_importado",
            "type": "dxf_import_join",
            "technique": "position_z_snap",
            "description": "Niveles importados, unidos y posicionados en altura con Snap"
        }
    ]
    storage.save_pattern(
        "organizacion_niveles_cad", 
        "Flujo de trabajo para apilar plantas arquitectónicas importadas de CAD en el eje Z usando alineación por vértices.",
        stacking_components
    )

    # 3. Patrón: Limpieza de Topología (Merge by Distance)
    topology_fix_components = [
        {
            "id": "operacion_limpieza",
            "type": "mesh_cleanup",
            "technique": "merge_by_distance",
            "description": "Eliminación de vértices duplicados tras extrusiones o uniones"
        }
    ]
    storage.save_pattern(
        "limpieza_topologica_malla", 
        "Procedimiento estándar para corregir 'caras colapsadas' y vértices superpuestos usando Merge by Distance.",
        topology_fix_components
    )

    # 4. Patrón: Repetición Procedural Manual (Shift+R Array)
    array_manual_components = [
        {
            "id": "duplicado_repetido",
            "type": "mesh_array",
            "technique": "shift_d_shift_r",
            "description": "Duplicación (Shift+D) seguida de repetición de acción (Shift+R)"
        }
    ]
    storage.save_pattern(
        "array_manual_rapido", 
        "Creación rápida de patrones repetitivos (rejas, montantes) sin usar el modificador Array formal.",
        array_manual_components
    )

    # Registrar experiencias técnicas avanzadas
    diagnosis = {
        "findings": [
            "Flujo Villa Savoye (CAD a 3D) integrado.",
            "Solución técnica para errores de visualización (Zoom con punto .) identificada.",
            "Uso de Shift+R como alternativa rápida de Array para carpintería.",
            "Importancia de la polilínea cerrada en CAD validada."
        ]
    }
    
    h_memory.store_experience(
        "villa_savoye_advanced_workflow", 
        {"workflow": ["dxf_import", "z_stacking", "merge_cleanup", "shift_r_array"]}, 
        0.98, 
        diagnosis
    )
    
    log_success("Patrones de la Villa Savoye y experiencia técnica de alto nivel consolidados exitosamente.")

if __name__ == "__main__":
    consolidate()
