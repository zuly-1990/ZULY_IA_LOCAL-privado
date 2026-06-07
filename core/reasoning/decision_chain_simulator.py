# Decision Chain Simulator

"""Decision chain simulation utilities.

This module implements a deterministic, heuristic‑based simulation of a
sequence of actions that would follow an initial intention.  It is purely
logical – no Blender (`bpy`) calls are made and no real actions are executed.
"""

from __future__ import annotations
from typing import Dict, List

from core.reasoning.intention_classifier import classify_intention
from core.reasoning.permission_gate import evaluate_permission

# Simple mapping from classification to a list of simulated steps.
_SIMULATION_STEPS = {
    "SEGURA": [
        {"accion_simulada": "Eliminar objeto", "impacto": "Objeto desaparece de la escena", "riesgo": "BAJO"},
        {"accion_simulada": "Actualizar dependencias", "impacto": "Colección queda vacía", "riesgo": "BAJO"},
    ],
    "AMBIGUA": [
        {"accion_simulada": "Modificar objeto (incógnito)", "impacto": "Cambios no claros", "riesgo": "MEDIO"},
    ],
    "PELIGROSA": [
        {"accion_simulada": "Borrar colección principal", "impacto": "Estructura completa desaparece", "riesgo": "ALTO"},
    ],
    "INCOMPLETA": [
        {"accion_simulada": "Operación indefinida", "impacto": "Sin efecto definido", "riesgo": "MEDIO"},
    ],
}

def _determine_global_evaluation(classification: str, permission_required: bool) -> str:
    """Return the global evaluation string based on classification and permission.

    - If permission is required (dangerous or ambiguous) → ``BLOQUEADA``.
    - If classification is ``AMBIGUA`` but permission is not required (should not happen) → ``RIESGOSA``.
    - Otherwise → ``ACEPTABLE``.
    """
    if permission_required:
        if classification == "AMBIGUA":
            return "RIESGOSA"
        return "BLOQUEADA"
    return "ACEPTABLE"

def simulate_decision_chain(initial_intention: str, observed_context: dict) -> Dict[str, object]:
    """Simulate a chain of decisions starting from an initial intention.

    Parameters
    ----------
    initial_intention: str
        The raw textual intention supplied by the user.
    observed_context: dict
        Contextual information about the current scene (currently unused).

    Returns
    -------
    dict
        A dictionary with the keys:
        - ``intencion_inicial``
        - ``cadena_simulada`` (list of step dictionaries)
        - ``evaluacion_global`` (ACEPTABLE / RIESGOSA / BLOQUEADA)
        - ``requiere_permiso_humano`` (bool from permission gate)
        - ``accion_ejecutada`` (always False in this phase)
    """
    # 1️⃣ Classification
    classification_report = classify_intention(initial_intention, observed_context)
    classification = classification_report.get("clasificacion", "INCOMPLETA")

    # 2️⃣ Permission gate
    permission_report = evaluate_permission(classification_report)
    requiere_permiso = permission_report.get("requiere_permiso_humano", True)

    # 3️⃣ Build simulated chain – stop if permission required.
    simulated_chain: List[Dict[str, object]] = []
    if not requiere_permiso:
        steps = _SIMULATION_STEPS.get(classification, [])
        for idx, step in enumerate(steps, start=1):
            simulated_chain.append({
                "paso": idx,
                "accion_simulada": step["accion_simulada"],
                "impacto": step["impacto"],
                "riesgo": step["riesgo"],
            })
    # If permission required, chain remains empty (blocked).

    evaluacion_global = _determine_global_evaluation(classification, requiere_permiso)

    return {
        "intencion_inicial": initial_intention,
        "cadena_simulada": simulated_chain,
        "evaluacion_global": evaluacion_global,
        "requiere_permiso_humano": requiere_permiso,
        "accion_ejecutada": False,
    }

if __name__ == "__main__":  # pragma: no cover
    # Simple demo
    examples = ["borrar cubo", "borrar colección principal", "modificar objeto"]
    for ex in examples:
        print(simulate_decision_chain(ex, {}))
