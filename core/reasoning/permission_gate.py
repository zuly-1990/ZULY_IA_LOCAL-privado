# Permission gate utilities

"""Permission gate utilities for ZULY.

The function :func:`evaluate_permission` receives the full classification
report produced by ``classify_intention`` (or a simulated intention) and
decides whether human permission is required before any action could be
executed.

The decision rules are **fixed** and must not be altered – they are taken
directly from the specification for Phase 6.2:

+----------------+----------------------+-----------+
| Clasificación | Requiere permiso?    | Estado    |
+----------------+----------------------+-----------+
| SEGURA         | ``False``            | PREAPROBADA |
| AMBIGUA        | ``True``             | BLOQUEADA   |
| PELIGROSA      | ``True``             | BLOQUEADA   |
| INCOMPLETA     | ``True``             | BLOQUEADA   |
+----------------+----------------------+-----------+

The module is deterministic, contains no ``bpy`` calls and never performs
real actions – it only returns a structured dictionary.
"""

from __future__ import annotations
from typing import Dict

# Mapping from classification to permission requirement and state.
_PERMISSION_MAP = {
    "SEGURA": (False, "PREAPROBADA"),
    "AMBIGUA": (True, "BLOQUEADA"),
    "PELIGROSA": (True, "BLOQUEADA"),
    "INCOMPLETA": (True, "BLOQUEADA"),
}

# Human‑readable motives for each classification.
_MOTIVO_MAP = {
    "SEGURA": "Acción segura y preaprobada",
    "AMBIGUA": "Falta claridad, requiere revisión humana",
    "PELIGROSA": "Acción con impacto estructural irreversible",
    "INCOMPLETA": "Intención incompleta, necesita confirmación",
}


def evaluate_permission(classification_report: Dict[str, object], simulation_report: dict | None = None) -> Dict[str, object]:
    """Evaluate whether a human permission is required.

    Parameters
    ----------
    classification_report: dict
        The full report returned by ``classify_intention``.
        Expected keys include ``intencion`` and ``clasificacion``.
    simulation_report: dict | None, optional
        Currently unused – placeholder for future simulation data.

    Returns
    -------
    dict
        A dictionary with the following keys:

        - ``intencion`` – passed through unchanged.
        - ``clasificacion`` – passed through unchanged.
        - ``requiere_permiso_humano`` – ``True`` if the action must be
          blocked pending human approval.
        - ``motivo`` – a short explanation of the decision.
        - ``estado`` – ``PREAPROBADA`` or ``BLOQUEADA`` according to the
          table above.
        - ``accion_ejecutada`` – always ``False`` because no real action is
          performed in this phase.
    """
    classification = classification_report.get("clasificacion", "INCOMPLETA")
    requiere_permiso, estado = _PERMISSION_MAP.get(classification, (True, "BLOQUEADA"))
    motivo = _MOTIVO_MAP.get(classification, "Motivo no definido")

    return {
        "intencion": classification_report.get("intencion"),
        "clasificacion": classification,
        "requiere_permiso_humano": requiere_permiso,
        "motivo": motivo,
        "estado": estado,
        "accion_ejecutada": False,
    }


if __name__ == "__main__":  # pragma: no cover
    # Simple demo when run directly.
    from core.reasoning.intention_classifier import classify_intention

    examples = [
        "borrar cubo",
        "modificar objeto",
        "borrar colección principal",
        "",
    ]
    for ex in examples:
        report = classify_intention(ex)
        print(evaluate_permission(report))
