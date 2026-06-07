"""
core/intents/intent_router.py
=============================

Router de intenciones. Conecta intenciones clasificadas
con sus comandos ejecutables correspondientes en Blender o el sistema.
"""

from typing import Dict, Any, Optional, Callable
from dataclasses import dataclass
from enum import Enum


class CommandStatus(Enum):
    """Estado de ejecución de un comando."""
    PENDING = "pending"
    EXECUTING = "executing"
    SUCCESS = "success"
    FAILED = "failed"
    RETRIED = "retried"


@dataclass
class CommandResult:
    """Resultado de la ejecución de un comando."""
    status: CommandStatus
    command: str
    intent: str
    output: Any = None
    error: str = None
    attempts: int = 1


class IntentRouter:
    """
    Router que convierte intenciones en ejecuciones de comandos.
    
    Conecta cada intención con su handler correspondiente,
    gestiona reintentos y proporciona retroalimentación.
    """
    
    def __init__(self, command_handlers: Dict[str, Callable] = None):
        """
        Inicializa el router.
        
        Args:
            command_handlers: Dict mapeo comando → función ejecutable
        """
        self.command_handlers = command_handlers or {}
        self.execution_history = []
        self.max_retries = 2
    
    def register_handler(self, command: str, handler: Callable) -> None:
        """
        Registra un handler para un comando.
        
        Args:
            command: Nombre del comando (ej: 'blender.create_primitive')
            handler: Función ejecutable para el comando
        """
        self.command_handlers[command] = handler
    
    def route_and_execute(self, intent: Dict, entities: Dict) -> CommandResult:
        """
        Enruta una intención a su handler y ejecuta el comando.
        
        Args:
            intent: Objeto Intent con nombre, command, etc.
            entities: Diccionario de entidades extraídas
            
        Returns:
            CommandResult con el resultado de la ejecución
        """
        command = intent.get('command', 'system.noop')
        intent_name = intent.get('name', 'unknown')
        
        result = CommandResult(
            status=CommandStatus.PENDING,
            command=command,
            intent=intent_name
        )
        
        # Obtener handler
        handler = self.command_handlers.get(command)
        if not handler:
            result.status = CommandStatus.FAILED
            result.error = f"No handler found for command: {command}"
            self.execution_history.append(result)
            return result
        
        # Ejecutar con reintentos
        for attempt in range(1, self.max_retries + 1):
            result.attempts = attempt
            result.status = CommandStatus.EXECUTING
            
            try:
                # Ejecutar handler
                output = handler(entities)
                
                result.status = CommandStatus.SUCCESS
                result.output = output
                self.execution_history.append(result)
                return result
                
            except Exception as e:
                result.error = str(e)
                
                if attempt < self.max_retries:
                    result.status = CommandStatus.RETRIED
                else:
                    result.status = CommandStatus.FAILED
        
        self.execution_history.append(result)
        return result
    
    def get_history(self, limit: int = None) -> list:
        """
        Obtiene historial de ejecuciones.
        
        Args:
            limit: Número máximo de registros a retornar
            
        Returns:
            Lista de CommandResult ordenada por fecha
        """
        if limit:
            return self.execution_history[-limit:]
        return self.execution_history
    
    def get_handler_list(self) -> Dict[str, str]:
        """Obtiene lista de handlers registrados."""
        return {
            cmd: handler.__doc__ or 'No documentation'
            for cmd, handler in self.command_handlers.items()
        }
    
    def clear_history(self) -> None:
        """Limpia el historial de ejecuciones."""
        self.execution_history.clear()
