# consolidate_architectural_pattern.py
import sys
import os
import json
from pathlib import Path

# Agregar el directorio raíz al path para importar módulos de core
sys.path.append(os.path.abspath(os.getcwd()))

from core.assembly.pattern_storage import PatternStorage
from core.utils.logging import log_success, log_info

def consolidate():
    # Inicializar almacenamiento de patrones
    # Notar que PatternStorage usa JSONStorage internamente
    storage = PatternStorage()
    
    # Definir el patrón de la columna basado en el tutorial de YouTube
    # Mujental: Plano (base) -> Cilindro (fuste) -> Cubo (capitel)
    
    components = [
        {
            "id": "base_plana",
            "type": "plane",
            "location": [0, 0, 0],
            "scale": 1.0,
            "description": "Base estructural del activo"
        },
        {
            "id": "fuste_columna",
            "type": "cylinder",
            "parent": "base_plana",
            "location": [0, 0, 1.0], # Levantado sobre el plano
            "scale": [0.5, 0.5, 2.0], # Ajustado a forma de columna
            "vertices": 12,
            "description": "Cuerpo de la columna con 12 divisiones"
        },
        {
            "id": "capitel_cubo",
            "type": "cube",
            "parent": "fuste_columna",
            "location": [0, 0, 2.0], # Encima del fuste
            "scale": 0.6,
            "description": "Capitel superior biselado"
        }
    ]
    
    pattern_name = "columna_arquitectonica_36"
    description = "Patrón de columna modular extraído de tutorial Mujental (YouTube) para Blender 3.6."
    
    success = storage.save_pattern(pattern_name, description, components)
    
    if success:
        log_success(f"Patrón '{pattern_name}' consolidado exitosamente en PatternStorage.")
        
        # También registrar en la memoria heurística de la Fase C2
        try:
            from core.cognition.memory.heuristic_memory import HeuristicMemory
            h_memory = HeuristicMemory()
            experience = {
                "objective": "Aprender modelado arquitectónico modular",
                "source": "YouTube (Mujental)",
                "pattern_id": pattern_name,
                "score": 0.8,
                "diagnosis": {"findings": ["Estructura modular validada por TranscriptionProcessor.", "Pasos claros: base, fuste, capitel."]}
            }
            h_memory.store_experience("architectural_modeling_youtube", {"pattern": pattern_name}, 0.8, experience["diagnosis"])
            log_success("Experiencia de aprendizaje registrada en HeuristicMemory.")
        except Exception as e:
            log_info(f"Nota: No se pudo registrar en HeuristicMemory (opcional): {e}")

if __name__ == "__main__":
    consolidate()
