# Safe Executor

"""Safe execution layer for ZULY.

This module implements a controlled execution gate that allows only safe,
reversible, and whitelisted micro-actions in Blender. Every action is logged
for traceability.
"""

import datetime
import os
import uuid
from typing import Dict, Any

# Whitelist of safe micro-actions
SAFE_ACTIONS = [
    "seleccionar_objeto",
    "deseleccionar_todo",
    "enfocar_objeto",
    "mostrar_info_objeto"
]

LOG_FILE = "logs/execution_log.txt"

def _log_execution(action: str, params: Dict[str, Any], result: str, origin: str):
    """Append an execution entry to the log file."""
    os.makedirs("logs", exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] ID: {uuid.uuid4().hex[:8]} | ORIGEN: {origin} | ACCION: {action} | PARAMS: {params} | RESULTADO: {result}\n"
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(entry)

def execute(request: Dict[str, Any]) -> Dict[str, Any]:
    """Execute a safe action in Blender context (simulated in this layer).
    
    Validates:
    1. Authorization flag.
    2. Whitelist containment.
    3. Human origin.
    """
    is_authorized = request.get("accion_autorizada", False)
    action = request.get("accion", "")
    params = request.get("parametros", {})
    origin = request.get("origen_confirmacion", "sistema")

    # 1. Authorization Filter
    if not is_authorized:
        _log_execution(action, params, "RECHAZADO: No autorizado", origin)
        return {
            "estado": "BLOQUEADO",
            "motivo": "Acción no autorizada por el humano",
            "accion": action
        }

    # 2. Whitelist Filter
    if action not in SAFE_ACTIONS:
        _log_execution(action, params, "RECHAZADO: Fuera de lista blanca", origin)
        return {
            "estado": "BLOQUEADO",
            "motivo": f"Acción '{action}' no está en la lista blanca de seguridad",
            "accion": action
        }

    # 3. Origin Filter
    if origin != "humano":
        _log_execution(action, params, "RECHAZADO: Origen no humano", origin)
        return {
            "estado": "BLOQUEADO",
            "motivo": "Solo se permiten acciones con origen humano explícito",
            "accion": action
        }

    # 4. Simulation/Execution (In Phase 10, we simulate the 'OK' after validation)
    # Note: In a real Blender environment, 'bpy' calls would happen here.
    result_status = "OK"
    _log_execution(action, params, result_status, origin)

    return {
        "estado": "ACCION_EJECUTADA",
        "accion": action,
        "resultado": result_status,
        "reversible": True,
        "registro_id": f"exec_{uuid.uuid4().hex[:6]}"
    }
