# Result Observer

"""Result observation and auto-verification layer for ZULY.

This module provides utilities to observe the current state of Blender (simulated
or real) and compare it against the expected result of an execution.
"""

import os
from typing import Dict, Any

LOG_FILE = "logs/execution_log.txt"

def _log_observation(action: str, status: str):
    """Append an observation entry to the log file."""
    os.makedirs("logs", exist_ok=True)
    entry = f"[OBSERVACION] accion={action} estado={status}\n"
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(entry)

def observe_result(execution_report: Dict[str, Any], current_context: Dict[str, Any]) -> Dict[str, Any]:
    """Observe current context and verify against expected results.
    
    Parameters
    ----------
    execution_report: dict
        Contains 'accion', 'parametros', and 'resultado_esperado'.
    current_context: dict
        The observed state of Blender (objects, active object, selection).
        
    Returns
    -------
    dict
        Verification report with 'estado', 'verificacion', and 'detalle'.
    """
    action = execution_report.get("accion", "unknown")
    expected = execution_report.get("resultado_esperado", {})
    
    # Extract observation data from current context
    # format of current_context should match what we expect (e.g., from a Blender observer)
    active_object = current_context.get("active_object", None)
    selected_objects = current_context.get("selected_objects", [])
    existing_objects = current_context.get("existing_objects", [])

    # Expected values
    expected_active = expected.get("objeto_seleccionado") # Simplified assumption

    # Logic:
    # 1. Check if expected object even exists
    if expected_active and expected_active not in existing_objects:
        status = "FALLO_DE_CONTEXTO"
        detail = f"El objeto esperado '{expected_active}' no existe en la escena."
        is_valid = False
        requires_help = True
    # 2. Check if result matches expectations
    elif expected_active == active_object:
        status = "COHERENTE"
        detail = "El objeto activo coincide con lo esperado."
        is_valid = True
        requires_help = False
    else:
        status = "INCONSISTENTE"
        detail = f"El objeto activo '{active_object}' no coincide con el esperado '{expected_active}'."
        is_valid = False
        requires_help = True

    _log_observation(action, status)

    return {
        "estado": status,
        "accion": action,
        "verificacion": is_valid,
        "detalle": detail,
        "requiere_intervencion_humana": requires_help
    }
