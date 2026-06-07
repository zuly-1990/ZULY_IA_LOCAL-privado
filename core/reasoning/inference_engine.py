# Inference Engine

"""Controlled inference layer for ZULY.

This module uses historical data from the consequence memory to emit logical
risk judgments about actions. It does not decide or execute; it only analyzes
experience.
"""

from typing import Dict, Any

def infer_risk(accion: str, memory_summary: Dict[str, Any]) -> Dict[str, Any]:
    """Emit a logical judgment based on historical statistics.
    
    Parameters
    ----------
    accion: str
        The action to analyze.
    memory_summary: dict
        Summary counts (COHERENTE, FALLO_DE_CONTEXTO, INCONSISTENTE).
        
    Rules:
    - If errors (FALLO_DE_CONTEXTO) > successes (COHERENTE) -> ALTO_RIESGO
    - If any inconsistencies (INCONSISTENTE) > 0 -> RIESGO_MODERADO
    - Otherwise -> BAJO_RIESGO
    """
    resumen = memory_summary.get("resumen", {})
    coherentes = resumen.get("COHERENTE", 0)
    fallos = resumen.get("FALLO_DE_CONTEXTO", 0)
    inconsistentes = resumen.get("INCONSISTENTE", 0)
    
    # 1. Logic filter
    if fallos > coherentes:
        juicio = "ALTO_RIESGO"
        explicacion = "Los fallos de contexto previos superan a los éxitos"
        recomendacion = "Abortar o revisar el entorno antes de proceder"
    elif inconsistentes > 0:
        juicio = "RIESGO_MODERADO"
        explicacion = "Se detectaron inconsistencias previas en esta acción"
        recomendacion = "Solicitar confirmación humana"
    else:
        juicio = "BAJO_RIESGO"
        explicacion = "La acción tiene un historial mayoritariamente coherente"
        recomendacion = "Proceder con precaución bajo supervisión"

    return {
        "accion": accion,
        "juicio": juicio,
        "explicacion": explicacion,
        "recomendacion": recomendacion,
        "accion_ejecutada": False
    }
