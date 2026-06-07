import pytest
import sys
import os

# Añadir el path raíz para importar core
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.explain.decision_explainer import DecisionExplainer

def test_explain_blocked_by_guard():
    data = {
        "intention": "BORRAR",
        "guard_result": {
            "status": "BLOQUEADO",
            "reason": "No hay objetos seleccionados."
        }
    }
    result = DecisionExplainer.explain(data)
    assert "No ejecuté 'BORRAR'" in result["human_summary"]
    assert "no hay objetos seleccionados" in result["human_summary"].lower()
    assert result["technical_log"]["guard_status"] == "BLOQUEADO"

def test_explain_successful_execution():
    data = {
        "intention": "CREAR_CUBO",
        "guard_result": {"status": "PERMITIDO", "reason": "OK"},
        "execution_result": {
            "success": True,
            "message": "Cubo añadido a la escena."
        }
    }
    result = DecisionExplainer.explain(data)
    assert "éxito" in result["human_summary"]
    assert "Cubo añadido" in result["human_summary"]
    assert result["technical_log"]["execution"]["success"] is True

def test_explain_failed_execution():
    data = {
        "intention": "RENDER",
        "guard_result": {"status": "PERMITIDO", "reason": "OK"},
        "execution_result": {
            "success": False,
            "message": "Error de memoria en la GPU."
        }
    }
    result = DecisionExplainer.explain(data)
    assert "error técnico" in result["human_summary"]
    assert "Error de memoria" in result["human_summary"]

def test_explain_only_validation():
    data = {
        "intention": "MOVER",
        "guard_result": {"status": "PERMITIDO", "reason": "OK"}
    }
    result = DecisionExplainer.explain(data)
    assert "validada" in result["human_summary"]
