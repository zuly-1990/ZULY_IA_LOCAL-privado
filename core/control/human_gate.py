# Human Gate

"""Human-in-the-Loop gate for ZULY.

This module provides pure‑logic utilities that stop execution until an explicit
human confirmation is received.  No Blender (`bpy`) imports or side‑effects are
performed – the functions only build and transform dictionaries.
"""

from __future__ import annotations
from typing import Dict

# ---------------------------------------------------------------------------
# Public constants – possible states returned by the gate.
# ---------------------------------------------------------------------------
STATE_WAITING = "ESPERANDO_CONFIRMACION"
STATE_AUTHORIZED = "AUTORIZADO"
STATE_BLOCKED = "BLOQUEADO"


def _build_message(decision_packet: Dict[str, object]) -> str:
    """Create a human‑readable message based on the decision packet.

    The message varies according to the classification:
    - ``SEGURA``   → simple confirmation request.
    - ``AMBIGUA``  → request clarification.
    - ``PELIGROSA`` or ``INCOMPLETA`` → strong warning.
    """
    classification = decision_packet.get("clasificacion", "INCOMPLETA")
    intencion = decision_packet.get("intencion", "<sin intención>")
    # Basic templates – keep them short and clear.
    if classification == "SEGURA":
        return f"¿Confirmas ejecutar la acción: '{intencion}'?"
    if classification == "AMBIGUA":
        return f"La intención es ambigua. ¿Podrías aclarar la acción deseada para '{intencion}'?"
    # PELIGROSA or INCOMPLETA
    return f"Advertencia: la intención '{intencion}' está clasificada como {classification.lower()}. ¿Confirmas proceder?"


def create_gate_packet(decision_packet: Dict[str, object]) -> Dict[str, object]:
    """Create the initial gate packet that pauses execution.

    The returned dictionary always contains:
    - ``estado`` set to ``ESPERANDO_CONFIRMACION``.
    - ``mensaje_al_humano`` with a clear request.
    - ``accion_autorizada`` set to ``False`` (no action yet).
    """
    return {
        "estado": STATE_WAITING,
        "mensaje_al_humano": _build_message(decision_packet),
        "accion_autorizada": False,
    }


def apply_human_response(gate_packet: Dict[str, object], response: str) -> Dict[str, object]:
    """Process a human response ("sí" / "no") and update the gate packet.

    Parameters
    ----------
    gate_packet: dict
        The packet produced by :func:`create_gate_packet`.
    response: str
        Human answer – case‑insensitive, accepted values are ``"si"``,
        ``"sí"`` (Spanish affirmative) and ``"no"``.

    Returns
    -------
    dict
        Updated packet with ``estado`` set to ``AUTORIZADO`` or ``BLOQUEADO``
        and ``accion_autorizada`` reflecting the decision.
    """
    normalized = response.strip().lower()
    if normalized in {"si", "sí", "yes", "y"}:
        gate_packet["estado"] = STATE_AUTHORIZED
        gate_packet["accion_autorizada"] = True
    else:
        # Any non‑affirmative answer is treated as a rejection.
        gate_packet["estado"] = STATE_BLOCKED
        gate_packet["accion_autorizada"] = False
    return gate_packet


if __name__ == "__main__":  # pragma: no cover
    # Simple demo
    demo = {
        "intencion": "borrar cubo",
        "clasificacion": "SEGURA",
    }
    packet = create_gate_packet(demo)
    print(packet)
    # Simulate a "sí" response
    print(apply_human_response(packet, "si"))
