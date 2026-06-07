"""
Modelo de Acción Fundacional (MAC-0)
Basado en ORDEN_ARCA_04

Este módulo no pertenece al core. Es un escudo externo que define 
el comportamiento por defecto ante la incertidumbre y el conflicto.
"""

from typing import Any, Dict, Optional

class ActionModelV1:
    """
    Modelo de Acción Fundacional (MAC-0)
    No decide, no aprende, no ejecuta lógica compleja.
    Solo define comportamiento por defecto y defensivo.
    """

    @staticmethod
    def should_act(context: Optional[Dict[str, Any]] = None) -> bool:
        """
        Ante cualquier contexto, la acción por defecto es NO actuar.
        """
        # MAC-0 Principio 1: Acción por defecto: NO-ACTUAR
        return False

    @staticmethod
    def on_conflict() -> str:
        """
        Comportamiento ante conflicto ético o técnico.
        """
        # MAC-0 Principio 3: Ante conflicto -> DETENERSE
        return "halt"

    @staticmethod
    def on_unknown_input(input_data: Any) -> str:
        """
        Comportamiento ante datos o comandos desconocidos.
        """
        # MAC-0 Principio 5: Registrar sin reaccionar
        return "store_only"

    @staticmethod
    def on_principle_violation() -> str:
        """
        Comportamiento cuando se detecta una violación de los principios de NOÉ.
        """
        # MAC-0 Jerarquía: Bloqueo absoluto
        return "deny"

    def __str__(self):
        return "ZULY Foundation Action Model (MAC-0) - Operational Shield"
