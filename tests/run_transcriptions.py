
import os
import json
import traceback
# mock del sistema de interpretación para que el evaluador tenga algo que procesar
# En un sistema real, esto llamaría a StructuralInterpreter
from core.structural_interpreter import StructuralInterpreter
from core.utils.transcription_evaluator import TranscriptionEvaluator

# Carpeta de transcripciones de prueba
TRANSCRIPTION_DIR = "tests/transcriptions"
REPORTE_FINAL = "transcription_evaluation_report.json"

def run_mass_evaluation():
    interpreter = StructuralInterpreter()
    evaluator = TranscriptionEvaluator()
    reporte = {}

    if not os.path.exists(TRANSCRIPTION_DIR):
        print(f"Error: La carpeta {TRANSCRIPTION_DIR} no existe.")
        return

    files = [f for f in os.listdir(TRANSCRIPTION_DIR) if f.endswith(".txt") or f.endswith(".py")]
    
    for filename in files:
        path = os.path.join(TRANSCRIPTION_DIR, filename)
        print(f"Evaluando transcripción: {filename}")
        
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            
            # 1. Interpretar (Simulado/Real)
            # Dividimos por líneas para simular pasos si es .txt
            steps_text = content.split('\n')
            processed_steps = []
            cumulative_elements = []
            
            for segment in steps_text:
                if not segment.strip(): continue
                # Generar mapa estructural con contexto de pasos anteriores
                step_data = interpreter.interpret(segment, context_elements=cumulative_elements)
                step_data["original_segment"] = segment
                processed_steps.append(step_data)
                
                # Acumular elementos nuevos para el siguiente paso
                if "elements" in step_data:
                    cumulative_elements.extend(step_data["elements"])
            
            # 2. Evaluar
            full_report = {"steps": processed_steps, "global_warnings": []}
            confidence_results = evaluator.calculate_confidence(full_report)
            
            # 3. Guardar resultado
            reporte[filename] = {
                "confianza": confidence_results.get("confidence_level"),
                "score": confidence_results.get("tutorial_confidence_score"),
                "claridad_promedio": confidence_results.get("average_clarity"),
                "vacios_tecnicos_totales": confidence_results.get("total_technical_gaps"),
                "recomendacion": confidence_results.get("recommendation"),
                "detalles_por_paso": [
                    {
                        "texto": s["original_segment"],
                        "claridad": s.get("clarity_score"),
                        "vacios": s.get("technical_gaps")
                    } for s in processed_steps
                ]
            }
        except Exception as e:
            print(f"Error evaluando {filename}: {e}")
            traceback.print_exc()

    # Guardar reporte final en JSON
    with open(REPORTE_FINAL, "w", encoding="utf-8") as f:
        json.dump(reporte, f, indent=4, ensure_ascii=False)

    print(f"\nEvaluacion completada. Reporte guardado en: {REPORTE_FINAL}")

    # Resumen rápido por consola
    print("\n" + "="*50)
    print("RESUMEN DE EVALUACIÓN")
    print("="*50)
    for archivo, info in reporte.items():
        print(f"[{info['confianza']}] {archivo:25} | Score: {info['score']}")
    print("="*50)

if __name__ == "__main__":
    run_mass_evaluation()
