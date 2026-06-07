# run_youtube_learning_v2.py
import sys
import os
import json
from pathlib import Path

# Agregar el directorio raíz al path para importar módulos de core
sys.path.append(os.path.abspath(os.getcwd()))

from core.utils.transcription_processor import TranscriptionProcessor
from core.utils.logging import log_info, log_success, log_error

def run_learning():
    processor = TranscriptionProcessor()
    tutorial_path = Path("ZULY_LAB/entrenamiento_youtube/tutorial_arquitectura_2d_a_3d.txt")
    
    if not tutorial_path.exists():
        log_error(f"No se encuentra el archivo: {tutorial_path}")
        return

    log_info(f"Leyendo tutorial de refuerzo: {tutorial_path}")
    with open(tutorial_path, "r", encoding="utf-8") as f:
        raw_text = f.read()

    log_info("Procesando transcripción con motor LYZU...")
    report = processor.process_transcription(raw_text)
    
    # Guardar reporte detallado
    report_path = Path("ZULY_LAB/dataset_patrones/reporte_arquitectura_2d_3d.json")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    log_success(f"Reporte de refuerzo generado en: {report_path}")
    log_info(f"Pasos detectados: {report['steps_count']}")
    log_info(f"Elementos detectados: {report['total_elements_detected']}")
    log_info(f"Nivel de Confianza: {report.get('confidence_level', 'N/A')}")

    # Extraer conceptos clave detectados para la bitácora
    elements = []
    for step in report['steps']:
        for el in step['structural_map']['elements']:
            elements.append(el['type'])
    
    log_info(f"Conceptos clave identificados: {set(elements)}")

if __name__ == "__main__":
    run_learning()
