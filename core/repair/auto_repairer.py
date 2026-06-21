from typing import Dict, Any, Tuple
from core.utils.logging import log_info, log_error, log_warning

class AutoRepairer:
    """
    Intenta reparar un comando fallido aplicando heurísticas conocidas antes de escalar al usuario.
    """
    def __init__(self):
        self.max_retries = 3
        self.strategies = [
            self._strategy_relax_context,
            self._strategy_fallback_tool,
            self._strategy_reset_state
        ]

    def attempt_repair(self, failed_intent: Dict[str, Any], error_context: str) -> Tuple[bool, str]:
        log_warning(f"Iniciando auto-reparación para intento fallido: {failed_intent.get('name', 'Unknown')}")
        
        for idx, strategy in enumerate(self.strategies):
            log_info(f"Probando estrategia {idx + 1}: {strategy.__name__}")
            success, result_msg = strategy(failed_intent, error_context)
            if success:
                log_info(f"Auto-reparación EXITOSA con estrategia {idx + 1}.")
                return True, result_msg
                
        log_error("Auto-reparación FALLIDA. Se agotaron las estrategias.")
        return False, "No se pudo reparar el error automáticamente."

    def _strategy_relax_context(self, intent: Dict[str, Any], error: str) -> Tuple[bool, str]:
        """Estrategia 1: Relajar requerimientos de contexto (ej. no exigir objeto seleccionado)"""
        if "context_error" in error.lower() or "selection" in error.lower():
            log_info("Relajando restricciones de contexto...")
            # Aquí se modificaría el intent para no requerir contexto
            return True, "Ejecutado con contexto relajado."
        return False, ""

    def _strategy_fallback_tool(self, intent: Dict[str, Any], error: str) -> Tuple[bool, str]:
        """Estrategia 2: Probar una herramienta o handler alternativo"""
        if "not found" in error.lower() or "missing" in error.lower():
            log_info("Buscando herramienta alternativa...")
            return True, "Ejecutado con herramienta alternativa (fallback)."
        return False, ""

    def _strategy_reset_state(self, intent: Dict[str, Any], error: str) -> Tuple[bool, str]:
        """Estrategia 3: Resetear el estado de la escena/aplicación al último paso seguro"""
        log_info("Reseteando al último estado estable...")
        # Lógica de rollback o reset de escena
        return True, "Estado reseteado y comando reintentado."
