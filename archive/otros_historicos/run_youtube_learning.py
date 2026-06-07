# run_youtube_learning.py
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
    tutorial_path = Path("ZULY_LAB/entrenamiento_youtube/tutorial_arquitectura_36.txt")
    
    if not tutorial_path.exists():
        log_error(f"No se encuentra el archivo: {tutorial_path}")
        return

    log_info(f"Leyendo tutorial: {tutorial_path}")
    with open(tutorial_path, "r", encoding="utf-8") as f:
        raw_text = f.read()

    log_info("Procesando transcripción...")
    report = processor.process_transcription(raw_text)
    
    # Guardar reporte detallado
    report_path = Path("ZULY_LAB/dataset_patrones/reporte_arquitectura_36.json")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    log_success(f"Reporte estructural generado en: {report_path}")
    log_info(f"Pasos detectados: {report['steps_count']}")
    log_info(f"Elementos detectados: {report['total_elements_detected']}")
    log_info(f"Confianza: {report.get('confidence_score', 0)}")

    # Mostrar hallazgos
    for step in report['steps']:
        print(f"\n[PASO {step['step_number']}]: {step['original_segment']}")
        for element in step['structural_map']['elements']:
            print(f"  - Elemento: {element['type']} (ID: {element['id']})")
            if element['parameters']:
                print(f"    Parámetros: {element['parameters']}")

if __name__ == "__main__":
    run_learning()
