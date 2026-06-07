# Resolution Engine

"""Resolution engine utilities for ZULY.

This module provides a deterministic, pure‑logic function ``resolve`` that
converts the output of the intention/decision simulation into a high‑level
decision object.  No ``bpy`` imports or real actions are performed – the
function only analyses the provided report and returns a structured dictionary
matching the specification for Phase 7.
"""

from __future__ import annotations
from typing import Dict

# ---------------------------------------------------------------------------
# Decision constants – these are the only allowed values for the ``decision``
# field in the returned object.
# ---------------------------------------------------------------------------
DECISION_READY = "READY"
DECISION_SUGGEST = "SUGGEST"
DECISION_ABORT = "ABORT"


def resolve(simulation_report: Dict[str, object]) -> Dict[str, object]:
    """Resolve a simulation report into a concrete decision.

    Parameters
    ----------
    simulation_report: dict
        The dictionary produced by the previous simulation step (e.g. the
        output of ``simulate_decision_chain`` or the raw classification report).
        Expected keys include ``clasificacion`` and ``requiere_permiso_humano``.

    Returns
    -------
    dict
        A decision object with the following keys:
        - ``decision``: one of ``READY``, ``SUGGEST`` or ``ABORT``.
        - ``reason``: a human‑readable explanation.
        - ``suggestion`` (optional): an alternative action when ``decision`` is
          ``SUGGEST``.
    """
    classification = simulation_report.get("clasificacion", "INCOMPLETA")
    requiere_permiso = simulation_report.get("requiere_permiso_humano", True)

    # Default reason – will be overridden in each branch.
    reason = ""
    suggestion = None

    # Decision logic – pure and deterministic.
    if classification == "SEGURA" and not requiere_permiso:
        decision = DECISION_READY
        reason = "La intención es segura y no requiere permiso humano; lista para ejecución."
    elif classification == "PELIGROSA":
        decision = DECISION_ABORT
        reason = "La intención ha sido clasificada como peligrosa; no se puede ejecutar."
    elif classification == "INCOMPLETA":
        decision = DECISION_ABORT
        reason = "La intención está incompleta o no se pudo clasificar; no se puede ejecutar."
    elif classification == "AMBIGUA" or requiere_permiso:
        # Ambiguous or any permission‑required case leads to a suggestion.
        decision = DECISION_SUGGEST
        reason = "La intención es ambigua o requiere revisión humana; se sugiere clarificación."
        suggestion = "ASK_FOR_CLARIFICATION"
    else:
        # Fallback for any unhandled case, defaults to abort for safety.
        decision = DECISION_ABORT
        reason = "Caso no cubierto por la lógica de decisión; se aborta por seguridad."

    result: Dict[str, object] = {
        "decision": decision,
        "reason": reason,
    }
    if suggestion is not None:
        result["suggestion"] = suggestion
    return result


if __name__ == "__main__":  # pragma: no cover
    # Simple demo when run directly.
    examples = [
        {"clasificacion": "SEGURA", "requiere_permiso_humano": False},
        {"clasificacion": "AMBIGUA", "requiere_permiso_humano": True},
        {"clasificacion": "PELIGROSA", "requiere_permiso_humano": True},
    ]
    for ex in examples:
        print(resolve(ex))
