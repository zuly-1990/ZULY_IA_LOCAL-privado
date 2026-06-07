"""
State Guard - Sellado de Límites del Estado (Fase 5.15)

Responsabilidad:
- Definir qué NO se puede hacer con el estado
- Actuar como muralla semántica
- NO ejecutar lógica
- NO observar estado
- SOLO definir límites

Principio Rector:
"Saber no implica poder."

ZULY conoce su estado, pero no tiene permiso para hacer nada con él.
"""

from typing import List


class StateGuard:
    """
    Define límites explícitos del uso del estado.
    
    El estado NO puede influir en decisiones.
    El estado NO puede modificar comportamiento.
    El estado NO puede condicionar flujos.
    
    Este guard es una muralla semántica, NO ejecuta lógica.
    """
    
    # Usos PROHIBIDOS del estado
    FORBIDDEN_USES: List[str] = [
        "decision_making",        # NO decidir basado en estado
        "flow_control",           # NO condicionar flujos
        "learning_trigger",       # NO activar aprendizaje
        "pattern_selection",      # NO seleccionar patrones
        "security_override",      # NO modificar seguridad
        "execution_condition",    # NO condicionar ejecución
        "behavior_modification",  # NO modificar comportamiento
        "automatic_retry",        # NO reintentar automáticamente
        "optimization",           # NO optimizar basado en estado
        "heuristics"             # NO crear heurísticas
    ]
    
    # Usos PERMITIDOS del estado (solo lectura pasiva)
    ALLOWED_USES: List[str] = [
        "logging",               # Solo para logs
        "monitoring",            # Solo para observación
        "debugging",             # Solo para debug
        "reporting"              # Solo para reportes
    ]
    
    @staticmethod
    def is_forbidden(use_case: str) -> bool:
        """
        Verifica si un caso de uso está prohibido.
        
        Args:
            use_case: Caso de uso a verificar
            
        Returns:
            True si está prohibido, False si está permitido
        """
        return use_case in StateGuard.FORBIDDEN_USES
    
    @staticmethod
    def is_allowed(use_case: str) -> bool:
        """
        Verifica si un caso de uso está permitido.
        
        Args:
            use_case: Caso de uso a verificar
            
        Returns:
            True si está permitido, False si está prohibido
        """
        return use_case in StateGuard.ALLOWED_USES
    
    @staticmethod
    def get_forbidden_uses() -> List[str]:
        """
        Retorna lista de usos prohibidos.
        
        Returns:
            Lista de usos prohibidos
        """
        return StateGuard.FORBIDDEN_USES.copy()
    
    @staticmethod
    def get_allowed_uses() -> List[str]:
        """
        Retorna lista de usos permitidos.
        
        Returns:
            Lista de usos permitidos
        """
        return StateGuard.ALLOWED_USES.copy()


# Constantes de validación
STATE_CAN_BE_READ = True
STATE_CAN_BE_USED = False

# Mensaje de advertencia
WARNING_MESSAGE = (
    "El estado es observable pero NO ejecutable. "
    "ZULY conoce su estado, pero no tiene permiso para hacer nada con él."
)
