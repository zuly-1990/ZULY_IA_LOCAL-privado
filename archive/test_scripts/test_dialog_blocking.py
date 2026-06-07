import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from core.dialog import DialogManager, DialogDecision
from core.intents.intent_manager import Intent

def test():
    print("STARTING TEST")
    
    # 1. Create Mock Report
    report = {
        "steps": [],
        "detected_concepts": [
            {
                "concept": "GEOMETRY_NODES_CONCEPTO",
                "confidence_impact": "NEUTRAL",
                "execution": "BLOQUEADA",
                "term_detected": "geometry nodes"
            }
        ]
    }
    
    report_path = "transcription_evaluation_report.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f)
    print(f"Report written to {os.path.abspath(report_path)}")
    
    # 2. Check DialogManager
    import core.dialog
    print(f"Dialog Module: {core.dialog.__file__}")
    
    dm = DialogManager()
    intent = Intent(
        name="test",
        command="blender.create_cube",
        confidence=0.99,
        raw_input="crea cubo",
        parameters={"posicion": [0,0,0]}
    )
    
    print("Validating intent...")
    decision, msg, meta = dm.validate_intent(intent)
    
    print(f"DECISION: {decision}")
    print(f"MESSAGE: {msg}")
    
    if decision == DialogDecision.REJECT and "Geometry Nodes" in msg:
        print("SUCCESS: Blocked correctly.")
        return True
    else:
        print("FAILURE: Did not block.")
        return False

if __name__ == "__main__":
    if test():
        sys.exit(0)
    else:
        sys.exit(1)
