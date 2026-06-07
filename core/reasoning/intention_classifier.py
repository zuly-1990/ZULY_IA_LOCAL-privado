# Intention classification utilities

"""Intention classification utilities for ZULY.

This module provides a deterministic, heuristic‑based implementation of
`classify_intention`.  It follows the adjustments requested for Phase 6.1:

* Classification order is from highest to lowest risk (PELIGROSA → AMBIGUA →
  SEGURA → INCOMPLETA).
* Priority mapping reflects cognitive care rather than urgency.
* Empty or whitespace‑only intention texts are treated as INCOMPLETA.

No Blender (`bpy`) calls are made and no actions are executed – the function
only analyses the supplied text.
"""

from __future__ import annotations
from typing import Dict, List
from core.utils.units import parse_dimension, to_meters

# ---------------------------------------------------------------------------
# Keyword tables – simple deterministic heuristics.
# ---------------------------------------------------------------------------
SEGURA_KEYWORDS: List[str] = [
    "borrar cubo",
    "eliminar objeto",
    "remover luz",
    "desactivar render",
]

AMBIGUA_KEYWORDS: List[str] = [
    "modificar objeto",
    "cambiar material",
    "ajustar posición",
    "actualizar escena",
]

PELIGROSA_KEYWORDS: List[str] = [
    "borrar colección principal",
    "eliminar escena",
    "resetear todo",
    "destruir jerarquía",
]

INCOMPLETA_KEYWORDS: List[str] = [
    "hacer algo",
    "arreglar escena",
    "optimizar",
    "mejorar",
]

# ---------------------------------------------------------------------------
# Priority mapping – higher priority means more human attention required.
# ---------------------------------------------------------------------------
PRIORITY_MAP = {
    "PELIGROSA": "ALTA",
    "AMBIGUA": "MEDIA",
    "SEGURA": "BAJA",
    "INCOMPLETA": "MEDIA",
}


def _match_category(text: str) -> str:
    """Return the first matching category based on the risk‑ordered tables.

    The order is deliberately from highest to lowest risk so that any overlap
    (e.g. a phrase containing both a *PELIGROSA* and a *SEGURA* keyword) will
    result in the more dangerous classification.
    """
    lowered = text.lower()
    for kw in PELIGROSA_KEYWORDS:
        if kw in lowered:
            return "PELIGROSA"
    for kw in AMBIGUA_KEYWORDS:
        if kw in lowered:
            return "AMBIGUA"
    for kw in SEGURA_KEYWORDS:
        if kw in lowered:
            return "SEGURA"
    for kw in INCOMPLETA_KEYWORDS:
        if kw in lowered:
            return "INCOMPLETA"
    return "INCOMPLETA"


def classify_intention(intention_text: str, observed_context: dict | None = None) -> Dict[str, object]:
    """Classify an intention and return a structured report.

    Parameters
    ----------
    intention_text: str
        The raw textual intention.
    observed_context: dict | None, optional
        Currently unused – kept for future extensions.

    Returns
    -------
    dict
        ``{"intencion": ..., "clasificacion": ..., "motivo": ..., 
        "requiere_confirmacion_humana": ..., "prioridad": ..., 
        "accion_ejecutada": False}``
    """
    # Guard against empty or whitespace‑only input.
    if not intention_text or not intention_text.strip():
        return {
            "intencion": intention_text,
            "clasificacion": "INCOMPLETA",
            "motivo": "Texto de intención vacío",
            "requiere_confirmacion_humana": True,
            "prioridad": PRIORITY_MAP["INCOMPLETA"],
            "accion_ejecutada": False,
        }

    category = _match_category(intention_text)
    
    # --- FASE 18.5: Detección de intención dimensional ---
    val, unit = parse_dimension(intention_text)
    dimension_metadata = None
    if val is not None:
        dimension_metadata = {
            "value": val,
            "unit": unit,
            "meters": to_meters(val, unit)
        }
        # Si tiene dimensiones exactas, aumenta el motivo de la clasificación
        motivo_precision = f" con precisión de {val}{unit}"
    else:
        motivo_precision = ""

    # Human confirmation is required for ambiguous or dangerous intents.
    requiere_confirmacion = category in {"AMBIGUA", "PELIGROSA"}

    # Motive generation – simple but explanatory.
    if category == "SEGURA":
        motivo = "Acción reversible y sin impacto estructural"
    elif category == "AMBIGUA":
        motivo = "Falta información suficiente para determinar seguridad"
    elif category == "PELIGROSA":
        motivo = "Impacta múltiples objetos o jerarquías críticas"
    else:
        motivo = "Intención no especificada claramente"

    return {
        "intencion": intention_text,
        "clasificacion": category,
        "motivo": motivo + motivo_precision,
        "requiere_confirmacion_humana": requiere_confirmacion,
        "prioridad": PRIORITY_MAP.get(category, "MEDIA"),
        "dimension_intent": dimension_metadata,
        "accion_ejecutada": False,
    }


if __name__ == "__main__":  # pragma: no cover
    # Simple demo when run directly.
    examples = [
        "borrar cubo",
        "modificar objeto",
        "borrar colección principal",
        "hacer algo",
        "",
    ]
    for ex in examples:
        print(classify_intention(ex))
