"""
core/session/ - Gestión de sesiones y contexto de ejecución
"""

from .execution_context import ExecutionContext
from .session_manager import SessionManager

__all__ = ['ExecutionContext', 'SessionManager']
