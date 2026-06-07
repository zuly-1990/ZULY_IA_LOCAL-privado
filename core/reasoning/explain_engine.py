# Explainability Engine

"""Explainability utilities for ZULY.

This module provides a pure‑logic function ``explain`` that receives a combined
context dictionary (output of the previous reasoning steps) and returns a
human‑readable explanation, an assessed risk level, and whether human
confirmation is required.

No ``bpy`` imports or side‑effects are performed – the function only builds
strings based on the supplied data.
"""

from __future__ import annotations
from typing import Dict

# ---------------------------------------------------------------------------
# Risk mapping – maps the classification from the intention stage to a risk
# descriptor that will be part of the final explanation.
# ---------------------------------------------------------------------------
_RISK_MAP = {
    "SEGURA": "BAJO",
    "AMBIGUA": "MEDIO",
    "PELIGROSA": "ALTO",
    "INCOMPLETA": "ALTO",
}

# Decision description mapping – human‑friendly wording for the decision
# values that the resolution engine returns.
_DECISION_DESC = {
    "READY": "ejecutar la acción en el futuro",
    "SUGGEST": "sugerir una acción alternativa",
    "ABORT": "detener la ejecución",
}


def explain(context: Dict[str, object]) -> Dict[str, object]:
    """Generate an explanation for a given reasoning context.

    Parameters
    ----------
    context: dict
        Expected keys (all optional, missing keys will be treated as empty
        strings):
        - ``intencion``: the original user intention.
        - ``clasificacion``: classification label (SEGURA, AMBIGUA, …).
        - ``decision``: final decision from the resolution engine.
        - ``reason``: short reason string produced by the resolution engine.
        - ``suggestion`` (optional): alternative action when decision is
          ``SUGGEST``.

    Returns
    -------
    dict
        ``explicacion`` (str): a concise, non‑technical Spanish sentence.
        ``riesgo`` (str): one of ``BAJO``, ``MEDIO`` or ``ALTO``.
        ``requiere_confirmacion_humana`` (bool): true when the decision is
        ``SUGGEST`` or ``ABORT`` (i.e. when human oversight is needed).
    """
    # Extract values with safe defaults
    intencion = context.get("intencion", "")
    clasificacion = context.get("clasificacion", "INCOMPLETA")
    decision = context.get("decision", "ABORT")
    reason = context.get("reason", "")
    suggestion = context.get("suggestion")

    # Determine risk based on classification
    riesgo = _RISK_MAP.get(clasificacion, "ALTO")

    # Human‑friendly description of the decision
    decision_desc = _DECISION_DESC.get(decision, "tomar una acción")

    # Build the explanation sentence
    # We keep it short and avoid technical jargon.
    explicacion_parts = []
    if intencion:
        explicacion_parts.append(f"La intención '{intencion}'")
    else:
        explicacion_parts.append("La intención proporcionada")

    explicacion_parts.append(f"fue clasificada como {clasificacion.lower()}")
    if reason:
        explicacion_parts.append(f"porque {reason.lower()}")
    explicacion_parts.append(f". Se decidió {decision_desc}")
    if decision == "SUGGEST" and suggestion:
        explicacion_parts.append(f" (sugerencia: {suggestion.lower()})")

    explicacion = " ".join(explicacion_parts).strip()

    requiere_confirmacion = decision in {"SUGGEST", "ABORT"}

    return {
        "explicacion": explicacion,
        "riesgo": riesgo,
        "requiere_confirmacion_humana": requiere_confirmacion,
    }


if __name__ == "__main__":  # pragma: no cover
    # Simple demo
    demo_context = {
        "intencion": "borrar cubo",
        "clasificacion": "SEGURA",
        "decision": "READY",
        "reason": "Intención segura y preaprobada",
    }
    print(explain(demo_context))
