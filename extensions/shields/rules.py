"""
Shield v1 - Reglas Estáticas de Validación

Este módulo define las reglas estáticas que el shield usa para validar comandos.

NO contiene lógica de decisión.
NO contiene heurísticas.
NO contiene IA.

Solo reglas explícitas y estáticas.
"""

from typing import List, Dict


class ShieldRules:
    """
    Reglas estáticas para validación de comandos.
    
    Estas reglas son INMUTABLES y EXPLÍCITAS.
    """
    
    # Tipos de comandos permitidos
    ALLOWED_COMMAND_TYPES: List[str] = [
        "explicit_human",     # Comando humano explícito
        "manual_test",        # Test manual controlado
    ]
    
    # Tipos de comandos bloqueados
    BLOCKED_COMMAND_TYPES: List[str] = [
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
    
    # Campos obligatorios en un comando
    REQUIRED_FIELDS: List[str] = [
        "type",               # Tipo de comando
        "callable",           # Función a ejecutar
    ]
    
    # Razones de bloqueo predefinidas
    BLOCK_REASONS: Dict[str, str] = {
        "invalid_type": "Tipo de comando no permitido",
        "missing_field": "Campo obligatorio faltante",
        "not_callable": "El comando no es ejecutable",
        "blocked_type": "Tipo de comando explícitamente bloqueado",
    }
    
    @staticmethod
    def is_type_allowed(command_type: str) -> bool:
        """
        Verifica si un tipo de comando está permitido.
        
        Args:
            command_type: Tipo de comando a verificar
            
        Returns:
            True si está permitido, False si no
        """
        return command_type in ShieldRules.ALLOWED_COMMAND_TYPES
    
    @staticmethod
    def is_type_blocked(command_type: str) -> bool:
        """
        Verifica si un tipo de comando está explícitamente bloqueado.
        
        Args:
            command_type: Tipo de comando a verificar
            
        Returns:
            True si está bloqueado, False si no
        """
        return command_type in ShieldRules.BLOCKED_COMMAND_TYPES
    
    @staticmethod
    def get_block_reason(reason_key: str) -> str:
        """
        Obtiene el mensaje de razón de bloqueo.
        
        Args:
            reason_key: Clave de la razón
            
        Returns:
            Mensaje de razón
        """
        return ShieldRules.BLOCK_REASONS.get(reason_key, "Razón desconocida")
