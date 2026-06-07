"""
Registro de Intención Humana (Fase 5.18)

Responsabilidad ÚNICA:
Registrar intención humana como texto libre.

Reglas:
- NO analizar significado
- NO clasificar
- NO traducir
- NO corregir
- NO ejecutar nada
"""

from typing import Dict, Any
from datetime import datetime

class IntentionRegistry:
    """
    Registro formal de intenciones humanas.
    ZULY escucha, no responde.
    """
    
    def register(self, project_name: str, intention_text: str) -> Dict[str, Any]:
        """
        Registra una intención humana declarativa.
        
        Args:
            project_name: Nombre del proyecto .blend
            intention_text: Texto declarativo de la intención
            
        Returns:
            Dict con el registro estructurado.
            
        Raises:
            ValueError: Si la validación básica falla.
        """
        # Validaciones PERMITIDAS
        if not isinstance(intention_text, str):
            raise ValueError("La intención debe ser texto.")
            
        if not intention_text.strip():
            raise ValueError("La intención no puede estar vacía.")
            
        if len(intention_text) > 500:
            raise ValueError("La intención es demasiado larga (max 500 caracteres).")
            
        # Retorno estructurado (Pasivo)
        return {
            "project": project_name,
            "intention": intention_text,
            "source": "HUMAN_DECLARATION",
            "timestamp": datetime.now().isoformat()
        }
