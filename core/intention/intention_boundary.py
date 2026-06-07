"""
Intention Boundary - Cortafuegos de Intención (Fase 5.16)

Responsabilidad:
- Definir qué NO puede convertirse en intención
- Actuar como cortafuegos semántico pasivo
- NO crear intención
- NO ejecutar intención
- NO decidir
- SOLO definir límites

Principio Rector:
"Percibir no implica querer."

ZULY puede observar, registrar, monitorear.
Pero no puede desear, decidir o actuar a partir de eso.
"""

from typing import List


class IntentionBoundary:
    """
    Define qué NO puede convertirse en intención dentro del sistema.
    
    Cortafuegos semántico pasivo.
    
    Asegura que NINGUNA parte del sistema:
    - Genere intención automáticamente
    - Convierta señales en decisiones
    - Active comportamiento emergente
    - Inicie acción sin autorización explícita
    """
    
    # Fuentes PROHIBIDAS de intención
    FORBIDDEN_INTENT_SOURCES: List[str] = [
        "state_snapshot",          # Estado observado
        "logs",                    # Logs del sistema
        "metrics",                 # Métricas internas
        "errors",                  # Errores
        "performance_data",        # Rendimiento
        "pattern_memory",          # Patrones
        "history",                 # Historial
        "external_signals",        # Señales externas
        "time_elapsed",            # Paso del tiempo
        "self_reflection",         # Autorreferencia
    ]
    
    # Fuentes PERMITIDAS de intención (solo explícitas)
    ALLOWED_INTENT_SOURCES: List[str] = [
        "explicit_command",        # Comando explícito
        "manual_trigger",          # Disparo manual
        "controlled_test",         # Tests
    ]
    
    @staticmethod
    def is_forbidden(source: str) -> bool:
        """
        Verifica si una fuente de intención está prohibida.
        
        Args:
            source: Fuente de intención a verificar
            
        Returns:
            True si está prohibida, False si está permitida
        """
        return source in IntentionBoundary.FORBIDDEN_INTENT_SOURCES
    
    @staticmethod
    def is_allowed(source: str) -> bool:
        """
        Verifica si una fuente de intención está permitida.
        
        Args:
            source: Fuente de intención a verificar
            
        Returns:
            True si está permitida, False si está prohibida
        """
        return source in IntentionBoundary.ALLOWED_INTENT_SOURCES
    
    @staticmethod
    def get_forbidden_sources() -> List[str]:
        """
        Retorna lista de fuentes prohibidas de intención.
        
        Returns:
            Lista de fuentes prohibidas
        """
        return IntentionBoundary.FORBIDDEN_INTENT_SOURCES.copy()
    
    @staticmethod
    def get_allowed_sources() -> List[str]:
        """
        Retorna lista de fuentes permitidas de intención.
        
        Returns:
            Lista de fuentes permitidas
        """
        return IntentionBoundary.ALLOWED_INTENT_SOURCES.copy()


# Constantes de validación
PERCEPTION_ALLOWED = True
INTENTION_FROM_PERCEPTION = False

# Mensaje de advertencia
WARNING_MESSAGE = (
    "Percibir no implica querer. "
    "ZULY puede observar, registrar y monitorear, "
    "pero no puede desear, decidir o actuar a partir de eso."
)
