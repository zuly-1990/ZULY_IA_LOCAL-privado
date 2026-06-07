import json
import os
import sys
from pathlib import Path

# Agregar root al path
sys.path.insert(0, str(Path(__file__).parent))

from core.utils.transcription_evaluator import evaluate_transcription, TranscriptionEvaluator
from core.dialog import DialogManager, DialogDecision
from core.intents.intent_manager import Intent
from core.utils.nlu import CommandIntent

def test_procedural_detection_blocking():
    print("="*60)
    print("TEST: Verificación de Bloqueo por Geometry Nodes")
    print("="*60)

    # 1. Crear archivo de transcripción dummy
    dummy_file = "test_transcription_gn.txt"
    content = """
    Hola amigos.
    Hoy vamos a usar geometry nodes para distribuir instancias.
    Es un sistema procedural muy potente.
    """
    with open(dummy_file, "w", encoding="utf-8") as f:
        f.write(content)
    
    print("[1] Archivo de transcripción creado.")

    # 2. Generar reporte de evaluación
    print("[2] Evaluando transcripción...")
    evaluator = TranscriptionEvaluator()
    # Mocking structural interpreter result for simplicity or use the real one if integrated
    # Let's use evaluate_transcription which uses StructuralInterpreter
    # Assuming StructuralInterpreter is working or doesn't crash on this text
    
    try:
        report = evaluate_transcription(dummy_file)
    except Exception as e:
        print(f"[ERROR] Falló evaluation: {e}")
        return False
        
    # Verificar que detectó el concepto
    detected = report.get("detected_concepts", [])
    gn_detected = any(c["concept"] == "GEOMETRY_NODES_CONCEPTO" for c in detected)
    
    if gn_detected:
        print(f"[OK] Concepto 'GEOMETRY_NODES_CONCEPTO' detectado.")
    else:
        print(f"[FAIL] NO se detectó el concepto procedural.")
        return False

    # 3. Guardar reporte para que DialogManager lo lea
    report_path = "transcription_evaluation_report.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f)
    print(f"[3] Reporte guardado en {report_path}.")

    import core.dialog
    print(f"DEBUG: core.dialog file: {core.dialog.__file__}")

    # Imprimir contenido del reporte generado
    with open(report_path, "r", encoding="utf-8") as f:
        print(f"DEBUG: Generated JSON Content: {f.read()}")

    dm = DialogManager()
    
    # Intención dummy (confiable)
    # Usamos Intent de intent_manager que es lo que espera DialogManager
    intent = Intent(
        name="test_intent",
        command="blender.create_cube",
        confidence=0.95,
        raw_input="test input",
        parameters={"posicion": [0,0,0]}
    )
    
    decision, message, meta = dm.validate_intent(intent)
    
    print(f"\nDECISIÓN: {decision}")
    print(f"MENSAJE: {message}")
    
    # 5. Validar resultado
    expected_msg = "Detectado sistema procedural (Geometry Nodes)"
    
    if decision == DialogDecision.REJECT:
        print("[OK] Decisión fue REJECT.")
        if expected_msg in message:
            print("[OK] Mensaje contiene advertencia correcta.")
        else:
            print("[FAIL] Mensaje incorrecto.")
            print(f"       Esperado: {expected_msg}...")
            print(f"       Recibido: {message}")
            return False
    else:
        print(f"[FAIL] Decisión incorrecta. Esperado REJECT, recibido {decision}")
        return False

    # Cleanup
    if os.path.exists(dummy_file): os.remove(dummy_file)
    # Don't delete report to allow manual inspection if needed, or delete it:
    if os.path.exists(report_path): os.remove(report_path)

    return True

if __name__ == "__main__":
    success = test_procedural_detection_blocking()
    sys.exit(0 if success else 1)
