import json
import os
import sys
from pathlib import Path
from typing import Dict, Any

# Agregar root al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.utils.transcription_evaluator import evaluate_transcription, TranscriptionEvaluator
from core.dialog import DialogManager, DialogDecision
from core.intents.intent_manager import Intent
from core.structural_interpreter import StructuralInterpreter

REPORT_FILE = "transcription_evaluation_report.json"

def process_file(file_path: str) -> Dict[str, Any]:
    print(f"\n{'='*60}")
    print(f"PROCESANDO: {os.path.basename(file_path)}")
    print(f"{'='*60}")
    
    # 1. Pipeline: Ingesta -> Evaluación -> Reporte
    print("[1] Evaluación de Transcripción...")
    if not os.path.exists(file_path):
        print(f"[ERROR] Archivo no encontrado: {file_path}")
        return {}
    
    # Usamos la función helper que ya hace Interpreter + Evaluator
    evaluation_result = evaluate_transcription(file_path)
    
    # Guardamos el reporte físico porque DialogManager lo lee del disco
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        json.dump(evaluation_result, f, indent=2)
    print(f"[2] Reporte guardado en {REPORT_FILE}")
    print(f"    Score: {evaluation_result['tutorial_confidence_score']} ({evaluation_result['confidence_level']})")
    print(f"    Detected Concepts: {evaluation_result.get('detected_concepts', 'None')}")
    
    # 2. Pipeline: Dialog Manager (Simulación)
    print("[3] Consulta al Dialog Manager...")
    dm = DialogManager()
    
    # Derivamos un Intent Dummy adecuado al contenido para probar el bloqueo/aviso
    # Nota: En un flujo real, el NLU extraería esto antes. Aquí simulamos el input del NLU.
    filename = os.path.basename(file_path)
    
    if "geometry_nodes" in filename:
        # Caso Procedural: Intent genérico que debería ser bloqueado por el reporte
        intent = Intent("test_proc", "blender.create_cube", 0.9, "usar geometry nodes", {})
    elif "ambiguo" in filename:
        # Caso Ambiguo: Intent con confianza media/baja o parámetros faltantes
        intent = Intent("test_ambiguo", "blender.create_cube", 0.6, "pon un cubo", {}) 
    else:
        # Caso Básico: Intent claro
        intent = Intent("test_clear", "blender.create_cube", 0.95, "crea un cubo", {"posicion": [0,0,0]})
        
    decision, message, meta = dm.validate_intent(intent)
    
    print(f"[RESULTADO DIÁLOGO]")
    print(f"  DECISIÓN: {decision}")
    print(f"  MENSAJE:  {message}")
    
    return {
        "file": filename,
        "score": evaluation_result['tutorial_confidence_score'],
        "decision": decision,
        "message": message,
        "execution_blocked": decision != DialogDecision.EXECUTE or "Bloqueada por modo observación" in message # Futuro
    }

def main():
    test_dir = os.path.join("tests", "transcriptions_real")
    files = [
        "tuto_cubo_basico.txt",
        "tuto_cubo_ambiguo.txt",
        "tuto_geometry_nodes.txt"
    ]
    
    results = []
    
    for f in files:
        full_path = os.path.join(test_dir, f)
        res = process_file(full_path)
        results.append(res)
        
    # Resumen Final
    print(f"\n{'#'*60}")
    print("RESUMEN DE VALIDACIÓN FASE 5.10")
    print(f"{'#'*60}")
    
    success_count = 0
    for r in results:
        status = "✅ PASS"
        
        # Criterios de éxito esperados
        if "basico" in r["file"]:
            if r["decision"] != DialogDecision.EXECUTE: status = "❌ FAIL (Debería ser EXECUTE)"
        elif "ambiguo" in r["file"]:
            if r["decision"] == DialogDecision.EXECUTE: status = "❌ FAIL (Debería ser CLARIFY/REJECT)"
        elif "geometry" in r["file"]:
            if r["decision"] != DialogDecision.REJECT: status = "❌ FAIL (Debería ser REJECT)"
            
        if "✅" in status: success_count += 1
            
        print(f"File: {r['file']:<25} | Score: {r['score']} | Decision: {r['decision']:<10} | {status}")

    print(f"\nÉxito: {success_count}/{len(files)}")
    
    # Cleanup
    if os.path.exists(REPORT_FILE):
        os.remove(REPORT_FILE)

if __name__ == "__main__":
    main()
