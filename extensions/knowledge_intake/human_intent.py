"""
Módulo de Intención Humana Manual (Fase 5.18)

Permite registrar declaraciones explícitas de intención sobre proyectos.
No ejecuta acciones, solo registra la voluntad del usuario.
"""

from typing import Dict, Any
from datetime import datetime

def register_intent(project_name: str, intent: str) -> Dict[str, Any]:
    """
    Registra intención humana manual.
    NO ejecuta acciones.
    NO modifica Blender.
    
    Args:
        project_name: Nombre del archivo o proyecto (.blend)
        intent: Descripción de la intención (ej: "PRACTICA", "PRODUCCION")
        
    Returns:
        Diccionario con el registro estructurado.
    """
    return {
        "project": project_name,
        "intent": intent,
        "source": "HUMAN_DECLARATION",
        "timestamp": datetime.now().isoformat()
    }
