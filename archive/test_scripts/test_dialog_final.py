import json
import os
import sys
from pathlib import Path

# Add root
sys.path.insert(0, str(Path(__file__).parent))

from core.dialog import DialogManager, DialogDecision
from core.intents.intent_manager import Intent

def test():
    print("STARTING ISOLATED TEST")
    
    # 1. Create Report
    report = {
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
    
    # 2. Dialog Manager
    dm = DialogManager()
    
    # Intent that would normally require params, to prove blocking happens FIRST
    intent = Intent("test", "blender.create_cube", 0.9, "crea cubo", {})
    
    decision, msg, meta = dm.validate_intent(intent)
    
    print(f"DECISION: {decision}")
    print(f"MESSAGE: {msg}")
    
    if decision == DialogDecision.REJECT and "Geometry Nodes" in msg:
        print("PASS")
    else:
        print("FAIL")

if __name__ == "__main__":
    test()
