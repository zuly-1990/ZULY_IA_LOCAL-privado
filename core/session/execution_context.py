"""
core/session/execution_context.py
=================================

Contexto de ejecución que mantiene el estado de una sesión del agente.
Extraído de agent.py como parte del refactoring God Objects (Fase 3).
"""

from typing import Dict, List, Any
from datetime import datetime


class ExecutionContext:
    """
    Contexto de ejecución que mantiene el estado de una sesión del agente.
    
    FASE CONSOLIDACIÓN: Ahora con límites de memoria para escalabilidad.
    """
    
    # Límites de escalabilidad (rolling window)
    MAX_EXECUTION_HISTORY = 100  # Últimos 100 comandos
    MAX_SCENE_STATES = 20  # Últimos 20 estados
    MAX_ERRORS = 50  # Últimos 50 errores
    
    def __init__(self):
        self.execution_history: List[Dict] = []  # Historial de comandos ejecutados
        self.scene_states: List[Dict] = []  # Estados capturados de la escena
        self.errors: List[str] = []  # Errores ocurridos
        self.success_count = 0
        self.failure_count = 0
        self.scene_requirements: Dict = {}  # Requisitos de escena esperados
        self.session_start = datetime.now()
    
    def add_execution(self, command_name: str, success: bool, result: Any = None, error: str = None):
        """Registra una ejecución de comando."""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'command': command_name,
            'success': success,
            'result': result,
            'error': error,
        }
        self.execution_history.append(entry)
        if success:
            self.success_count += 1
        else:
            self.failure_count += 1
            if error:
                self.errors.append(error)
        
        # Rolling window: mantener solo los últimos N elementos
        self._apply_limits()
    
    def _apply_limits(self):
        """Aplica límites de rolling window para escalabilidad."""
        if len(self.execution_history) > self.MAX_EXECUTION_HISTORY:
            self.execution_history = self.execution_history[-self.MAX_EXECUTION_HISTORY:]
        
        if len(self.scene_states) > self.MAX_SCENE_STATES:
            self.scene_states = self.scene_states[-self.MAX_SCENE_STATES:]
        
        if len(self.errors) > self.MAX_ERRORS:
            self.errors = self.errors[-self.MAX_ERRORS:]
    
    def add_scene_state(self, state: Dict):
        """Agrega un estado de escena con límite."""
        self.scene_states.append(state)
        self._apply_limits()
    
    def get_summary(self) -> Dict:
        """Retorna un resumen del contexto de ejecución."""
        return {
            'session_start': self.session_start.isoformat(),
            'commands_executed': len(self.execution_history),
            'total_successes': self.success_count,
            'total_failures': self.failure_count,
            'error_count': len(self.errors),
            'recent_errors': self.errors[-5:] if self.errors else [],
        }
    
    def get_execution_stats(self) -> Dict[str, Any]:
        """Retorna estadísticas detalladas de ejecución."""
        total = self.success_count + self.failure_count
        success_rate = (self.success_count / total * 100) if total > 0 else 0
        
        return {
            'total_commands': total,
            'success_count': self.success_count,
            'failure_count': self.failure_count,
            'success_rate_percent': round(success_rate, 1),
            'session_duration_minutes': self._get_session_duration(),
        }
    
    def _get_session_duration(self) -> float:
        """Calcula duración de sesión en minutos."""
        from datetime import datetime
        now = datetime.now()
        delta = now - self.session_start
        return round(delta.total_seconds() / 60, 1)
