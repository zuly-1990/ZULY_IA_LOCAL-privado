"""
Command Gate - Puerta de Comandos Explícitos (Fase 5.17)

Responsabilidad:
- Definir la única vía legítima para recibir órdenes
- NO interpretar comandos
- NO transformar comandos
- NO generar intención interna
- SOLO definir límites

Principio Rector:
"Obedecer no implica comprender."

El sistema puede ejecutar un comando sin entenderlo,
sin evaluarlo y sin desear nada.
"""

from typing import List


class CommandGate:
    """
    Puerta pasiva de validación de comandos explícitos.
    
    No interpreta, no decide, no ejecuta.
    
    Asegura que:
    - Nada interno genere acción
    - Nada observado dispare ejecución
    - No exista interpretación semántica
    - Solo comandos explícitos, humanos y permitidos puedan pasar
    """
    
    # Tipos de comandos PROHIBIDOS
    FORBIDDEN_COMMAND_TYPES: List[str] = [
        "implicit",           # Comandos implícitos
        "derived",            # Inferidos
        "automatic",          # Generados por el sistema
        "state_based",        # Basados en estado
        "pattern_based",      # Basados en patrones
        "self_generated",     # Generados por ZULY
        "timed",              # Disparados por tiempo
        "conditional",        # Condicionales
        "heuristic",          # Heurísticos
    ]
    
    # Tipos de comandos PERMITIDOS (solo explícitos)
    ALLOWED_COMMAND_TYPES: List[str] = [
        "explicit_human",     # Comando humano explícito
        "manual_test",        # Tests controlados
    ]
    
    @staticmethod
    def is_forbidden(command_type: str) -> bool:
        """
        Verifica si un tipo de comando está prohibido.
        
        Args:
            command_type: Tipo de comando a verificar
            
        Returns:
            True si está prohibido, False si está permitido
        """
        return command_type in CommandGate.FORBIDDEN_COMMAND_TYPES
    
    @staticmethod
    def is_allowed(command_type: str) -> bool:
        """
        Verifica si un tipo de comando está permitido.
        
        Args:
            command_type: Tipo de comando a verificar
            
        Returns:
            True si está permitido, False si está prohibido
        """
        return command_type in CommandGate.ALLOWED_COMMAND_TYPES
    
    @staticmethod
    def get_forbidden_types() -> List[str]:
        """
        Retorna lista de tipos de comandos prohibidos.
        
        Returns:
            Lista de tipos prohibidos
        """
        return CommandGate.FORBIDDEN_COMMAND_TYPES.copy()
    
    @staticmethod
    def get_allowed_types() -> List[str]:
        """
        Retorna lista de tipos de comandos permitidos.
        
        Returns:
            Lista de tipos permitidos
        """
        return CommandGate.ALLOWED_COMMAND_TYPES.copy()


# Constantes de validación
COMMAND_RECEPTION_ALLOWED = True
COMMAND_GENERATION_ALLOWED = False

# Mensaje de advertencia
WARNING_MESSAGE = (
    "Obedecer no implica comprender. "
    "ZULY puede ejecutar un comando sin entenderlo, "
    "sin evaluarlo y sin desear nada."
)
