# run_youtube_learning_v3.py
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
    tutorial_path = Path("ZULY_LAB/entrenamiento_youtube/tutorial_cortes_bisect.txt")
    
    if not tutorial_path.exists():
        log_error(f"No se encuentra el archivo: {tutorial_path}")
        return

    log_info(f"Leyendo tutorial de cortes: {tutorial_path}")
    with open(tutorial_path, "r", encoding="utf-8") as f:
        raw_text = f.read()

    log_info("Procesando técnicas de bisección...")
    report = processor.process_transcription(raw_text)
    
    # Guardar reporte detallado
    report_path = Path("ZULY_LAB/dataset_patrones/reporte_cortes_bisect.json")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    log_success(f"Reporte de bisección generado en: {report_path}")
    log_info(f"Conceptos clave identificados: Cortes, Bisect, Fill, Clear Inner/Outer")

if __name__ == "__main__":
    run_learning()
