import os
import glob
import json
import logging
from typing import Dict, Any

from core.cognition.c2_experience_memory import C2ExperienceMemory

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s - %(message)s')
logger = logging.getLogger("C2Trainer")

def load_and_train():
    memory = C2ExperienceMemory(db_path='bitacora/memory.db')
    
    # Ruta donde se encuentran los patrones parseados
    pattern_files = glob.glob("ZULY_LAB/dataset_patrones/reporte_*.json")
    
    total_loaded = 0
    
    for file_path in pattern_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            steps = data.get("steps", [])
            for step in steps:
                original_segment = step.get("original_segment", "Tutorial Paso a Paso")
                structural_map = step.get("structural_map", {})
                
                evaluation = {
                    "status": "success",
                    "score": 1.0,
                    "parameters": structural_map,
                    "metrics_passed": 1,
                    "metrics_total": 1,
                    "issues": [],
                    "recommendations": ["Patrón extraído de validación en YouTube"]
                }
                
                # Guardar experiencia
                memory.record_experience(objective=original_segment, evaluation=evaluation)
                total_loaded += 1
                
            logger.info(f"Procesado: {os.path.basename(file_path)} - {len(steps)} experiencias aprendidas.")
                
        except Exception as e:
            logger.error(f"Error procesando {file_path}: {e}")
            
    logger.info(f"=== Entrenamiento C2 Completado ===")
    logger.info(f"Se inyectaron {total_loaded} nuevas experiencias en la memoria.")

if __name__ == "__main__":
    load_and_train()
