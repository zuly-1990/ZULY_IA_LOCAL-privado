import json
import os
import sys
from pathlib import Path

# Add root
sys.path.insert(0, str(Path(__file__).parent))

from core.dialog import DialogManager, DialogDecision
from core.intents.intent_manager import Intent

def test_logic():
    print("TESTING PARADIGM BLOCKING LOGIC")
    
    # Mock Report
    report = {
        "detected_paradigms": {
            "dominant_paradigm": "PARADIGM_DECLARATIVE",
            "compatibility_status": "REQUIERE_INTERPRETACION"
        },
        "detected_concepts": []
    }
    
    # Write temp report
    with open("transcription_evaluation_report.json", "w") as f:
        json.dump(report, f)
        
    dm = DialogManager()
    intent = Intent("test", "blender.create_cube", 0.9, "hacer cosas", {})
    
    decision, msg, meta = dm.validate_intent(intent)
    
    print(f"DECISION: {decision}")
    print(f"MESSAGE: {msg}")
    
    if decision == DialogDecision.REJECT and "paradigm declarative" in msg.lower():
        print("PASS")
    else:
        print("FAIL")

if __name__ == "__main__":
    test_logic()
