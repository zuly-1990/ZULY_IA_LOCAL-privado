import pytest
import sys
import os

# Añadir el path raíz para importar core
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.authorization.human_gate import HumanGate

def test_authorize_low_risk_action():
    result = HumanGate.authorize("LIST_OBJECTS")
    assert result["risk"] == HumanGate.LOW
    assert result["action"] == "EXECUTE"

def test_authorize_medium_risk_action():
    result = HumanGate.authorize("DELETE")
    assert result["risk"] == HumanGate.MEDIUM
    assert result["action"] == "ASK"
    assert "confirmación humana" in result["reason"]

def test_authorize_high_risk_action():
    result = HumanGate.authorize("RESET_SCENE")
    assert result["risk"] == HumanGate.HIGH
    assert result["action"] == "BLOCK"
    assert "ALTO RIESGO" in result["reason"]

def test_authorize_unknown_action_defaults_to_medium():
    result = HumanGate.authorize("COMPLEX_UNKNOWN_COMMAND")
    assert result["risk"] == HumanGate.MEDIUM
    assert result["action"] == "ASK"

def test_authorize_case_insensitivity():
    result = HumanGate.authorize("list_collections")
    assert result["risk"] == HumanGate.LOW
    assert result["action"] == "EXECUTE"
