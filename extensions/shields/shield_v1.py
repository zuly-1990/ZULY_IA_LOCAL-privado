"""
Shield v1 - Escudo Externo de Comandos

Este shield valida comandos ANTES de que lleguen al core.

IMPORTANTE:
- NO importa nada de /core (excepto interfaces públicas si es necesario)
- NO ejecuta comandos
- NO decide "inteligentemente"
- NO lee estado
- SOLO autoriza o bloquea

Regla de oro: "El shield solo autoriza o bloquea, nunca ejecuta."
"""

from typing import Dict, Any, Callable
from extensions.shields.rules import ShieldRules


class ShieldV1:
    """
    Escudo externo de validación de comandos.
    
    Valida comandos según reglas estáticas ANTES de enviarlos al core.
    
    NO ejecuta.
    NO decide.
    NO lee estado.
    SOLO valida.
    """
    
    @staticmethod
    def validate_command(command: Dict[str, Any]) -> Dict[str, Any]:
        """
        Valida un comando según reglas estáticas.
        
        Args:
            command: Diccionario con información del comando
                     Debe contener: 'type', 'callable'
        
        Returns:
            Diccionario con resultado de validación:
            {
                'allowed': bool,
                'reason': str
            }
        """
        # Validación 1: Campos obligatorios
        for field in ShieldRules.REQUIRED_FIELDS:
            if field not in command:
                return {
                    'allowed': False,
                    'reason': ShieldRules.get_block_reason('missing_field') + f": {field}"
                }
        
        # Validación 2: Tipo de comando
        command_type = command.get('type', '')
        
        # Verificar si está explícitamente bloqueado
        if ShieldRules.is_type_blocked(command_type):
            return {
                'allowed': False,
                'reason': ShieldRules.get_block_reason('blocked_type') + f": {command_type}"
            }
        
        # Verificar si está permitido
        if not ShieldRules.is_type_allowed(command_type):
            return {
                'allowed': False,
                'reason': ShieldRules.get_block_reason('invalid_type') + f": {command_type}"
            }
        
        # Validación 3: Callable es ejecutable
        if not callable(command.get('callable')):
            return {
                'allowed': False,
                'reason': ShieldRules.get_block_reason('not_callable')
            }
        
        # Si pasa todas las validaciones
        return {
            'allowed': True,
            'reason': 'Comando validado correctamente'
        }


# Constantes
SHIELD_VERSION = "1.0"
SHIELD_MODE = "STATIC_RULES"

# Mensaje de advertencia
WARNING_MESSAGE = (
    "Shield v1 solo valida comandos según reglas estáticas. "
    "NO ejecuta, NO decide, NO lee estado."
)
