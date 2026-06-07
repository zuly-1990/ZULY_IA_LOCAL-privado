"""
failsafe_executor.py

FASE 18.5: Modo Seguro (Fail-Safe)
Si una orden falla:
- Detener ejecución
- Reportar error
- Esperar nueva instrucción
- NUNCA "intentar arreglar solo"
"""

from typing import Dict, Any, Callable, Optional, List
from dataclasses import dataclass
from enum import Enum
from core.utils.logging import log_info, log_warning, log_error, log_success


class ExecutionState(Enum):
    """Estados de ejecución."""
    READY = "ready"
    EXECUTING = "executing"
    STOPPED = "stopped"  # Detenido por fallo
    WAITING = "waiting"  # Esperando instrucción


@dataclass
class FailsafeResult:
    """Resultado de una ejecución en modo seguro."""
    success: bool
    action: str
    result: Optional[Dict[str, Any]]
    error: Optional[str]
    stopped: bool  # Si se detuvo la ejecución
    message: str


class FailsafeExecutor:
    """
    Ejecutor en modo seguro.
    
    REGLAS:
    1. Si falla → detener inmediatamente
    2. Reportar error explícito
    3. Esperar nueva instrucción
    4. NUNCA intentar arreglar automáticamente
    """
    
    def __init__(self):
        self._state = ExecutionState.READY
        self._last_error: Optional[str] = None
        self._execution_queue: List[Dict] = []
        self._completed_actions: List[FailsafeResult] = []
    
    @property
    def state(self) -> ExecutionState:
        """Estado actual del ejecutor."""
        return self._state
    
    @property
    def is_stopped(self) -> bool:
        """Verifica si está detenido por fallo."""
        return self._state == ExecutionState.STOPPED
    
    @property
    def last_error(self) -> Optional[str]:
        """Último error registrado."""
        return self._last_error
    
    def reset(self):
        """Reinicia el ejecutor para nueva instrucción."""
        self._state = ExecutionState.READY
        self._last_error = None
        self._execution_queue = []
        log_info("🔄 Failsafe executor reset - ready for new instruction")
    
    def execute_single(
        self,
        action_name: str,
        handler: Callable,
        parameters: Dict[str, Any],
        adapter=None
    ) -> FailsafeResult:
        """
        Ejecuta una sola acción en modo seguro.
        
        Args:
            action_name: Nombre de la acción
            handler: Función handler a ejecutar
            parameters: Parámetros para el handler
            adapter: EngineAdapter opcional
        
        Returns:
            FailsafeResult con el resultado
        """
        # Verificar si estamos detenidos
        if self._state == ExecutionState.STOPPED:
            return FailsafeResult(
                success=False,
                action=action_name,
                result=None,
                error="Executor is stopped. Call reset() first.",
                stopped=True,
                message="Cannot execute - system stopped due to previous error"
            )
        
        self._state = ExecutionState.EXECUTING
        log_info(f"🔧 Executing: {action_name}")
        
        try:
            # Ejecutar handler
            if adapter is not None:
                result = handler(parameters, adapter=adapter)
            else:
                result = handler(parameters)
            
            # Verificar resultado
            if isinstance(result, dict) and result.get('success', False):
                # Éxito
                self._state = ExecutionState.READY
                log_success(f"✓ {action_name} completed successfully")
                
                failsafe_result = FailsafeResult(
                    success=True,
                    action=action_name,
                    result=result,
                    error=None,
                    stopped=False,
                    message=result.get('message', 'Action completed')
                )
            else:
                # Fallo en el handler
                error_msg = result.get('error', 'Unknown error') if isinstance(result, dict) else 'Handler returned invalid response'
                self._handle_failure(action_name, error_msg)
                
                failsafe_result = FailsafeResult(
                    success=False,
                    action=action_name,
                    result=result,
                    error=error_msg,
                    stopped=True,
                    message=f"Action failed: {error_msg}"
                )
        
        except Exception as e:
            # Excepción durante ejecución
            error_msg = str(e)
            self._handle_failure(action_name, error_msg)
            
            failsafe_result = FailsafeResult(
                success=False,
                action=action_name,
                result=None,
                error=error_msg,
                stopped=True,
                message=f"Exception during execution: {error_msg}"
            )
        
        self._completed_actions.append(failsafe_result)
        return failsafe_result
    
    def _handle_failure(self, action_name: str, error: str):
        """Maneja un fallo según protocolo fail-safe."""
        self._state = ExecutionState.STOPPED
        self._last_error = error
        
        log_error(f"✗ FAILSAFE STOP: {action_name} failed")
        log_error(f"  Error: {error}")
        log_warning("🛑 Execution stopped. Waiting for new instruction.")
        log_warning("   Call reset() to continue.")
    
    def execute_sequence(
        self,
        actions: List[Dict[str, Any]],
        adapter=None
    ) -> List[FailsafeResult]:
        """
        Ejecuta una secuencia de acciones, deteniéndose en el primer fallo.
        
        Args:
            actions: Lista de {action_name, handler, parameters}
            adapter: EngineAdapter opcional
        
        Returns:
            Lista de resultados (puede ser incompleta si hubo fallo)
        """
        results = []
        
        for action in actions:
            result = self.execute_single(
                action_name=action['action_name'],
                handler=action['handler'],
                parameters=action.get('parameters', {}),
                adapter=adapter
            )
            results.append(result)
            
            # Si falló, detenerse
            if not result.success:
                log_warning(f"🛑 Sequence stopped at action {len(results)}/{len(actions)}")
                break
        
        return results
    
    def get_status_report(self) -> Dict[str, Any]:
        """Obtiene reporte de estado del ejecutor."""
        return {
            'state': self._state.value,
            'is_stopped': self.is_stopped,
            'last_error': self._last_error,
            'completed_actions': len(self._completed_actions),
            'message': self._get_status_message()
        }
    
    def _get_status_message(self) -> str:
        """Genera mensaje de estado legible."""
        if self._state == ExecutionState.READY:
            return "Ready for instructions"
        elif self._state == ExecutionState.EXECUTING:
            return "Executing action..."
        elif self._state == ExecutionState.STOPPED:
            return f"STOPPED: {self._last_error}. Call reset() to continue."
        elif self._state == ExecutionState.WAITING:
            return "Waiting for new instruction"
        return "Unknown state"


# Singleton para uso global
_failsafe_executor: Optional[FailsafeExecutor] = None


def get_failsafe_executor() -> FailsafeExecutor:
    """Obtiene la instancia global del FailsafeExecutor."""
    global _failsafe_executor
    if _failsafe_executor is None:
        _failsafe_executor = FailsafeExecutor()
    return _failsafe_executor
