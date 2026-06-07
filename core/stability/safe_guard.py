# core/stability/safe_guard.py
"""
Módulo de Estabilidad y Seguridad (Safeguard) para el agente Zuly.
Implementa el Blindaje de la Fase 4 del Plan Maestro Unificado.
"""

from typing import Dict, Any, Tuple, List
from core.intents.intent_manager import Intent
from core.utils.logging import log_info, log_warning, log_error, log_debug

class SafeGuardDecision:
    """Tipos de veredicto del SafeGuard."""
    APPROVED = "APPROVED"               # Acción segura, proceder.
    CONFIRM = "CONFIRM"                # Requiere confirmación humana explícita.
    BLOCKED = "BLOCKED"                # Acción prohibida en el contexto actual.

class SafeGuard:
    """
    Módulo estricto y antipático encargado de proteger la integridad del sistema.
    
    Regla de Oro: El humano es la autoridad absoluta. Acciones de alto impacto 
    siempre requieren confirmación.
    """
    
    def __init__(self):
        # Acciones destructivas o de alto impacto
        self.critical_actions = {
            'blender.delete_object': 'Eliminación de geometría',
            'blender.clear_scene': 'Borrado total de la escena',
            'blender.render_animation': 'Gasto elevado de tiempo/recursos',
            'blender.export_fbx': 'Exportación de datos externos',
            'blender.export_obj': 'Exportación de datos externos',
            'blender.export_gltf': 'Exportación de datos externos',
            'system.save_project': 'Sobrescritura de archivo de proyecto'
        }
        
        # Acciones creativas o iterativas (Fase 5/6)
        self.autonomous_actions = [
            'blender.generate_scene',
            'blender.auto_style',
            'learning.apply_strategy'
        ]
        
        self.history = []

    def verify(self, intent: Intent, context: Dict[str, Any] = None) -> Tuple[str, str, Dict[str, Any]]:
        """
        Evalúa el riesgo de una intención antes de ser enviada al ejecutor.
        
        Args:
            intent: La intención validada por el DialogManager.
            context: Contexto adicional (modo actual, presupuesto, etc).
            
        Returns:
            Tuple[str, str, Dict]: (Veredicto, Mensaje explicativo, Metadatos de riesgo)
        """
        log_debug(f"SafeGuard verificando impacto de: {intent.command}")
        
        reason = ""
        risk_level = "low"
        
        # 1. Verificar si es una acción crítica/destructiva
        if intent.command in self.critical_actions:
            description = self.critical_actions[intent.command]
            reason = f"La acción '{intent.command}' implica {description}."
            return (
                SafeGuardDecision.CONFIRM,
                f"⚠️ BLOQUEO DE SEGURIDAD: {reason} ¿Estás totalmente seguro de proceder?",
                {'risk': 'high', 'reason': intent.command}
            )

        # 2. Verificar si es una acción con "Libre Albedrío" (Fase 6 proyectada)
        if intent.command in self.autonomous_actions:
            return (
                SafeGuardDecision.CONFIRM,
                f"ℹ️ CONTROL HUMANO: Zuly propone una acción autónoma creativa ({intent.command}). ¿Permites que continúe?",
                {'risk': 'medium', 'type': 'autonomous'}
            )

        # 3. Registro de auditoría
        self._log_decision(intent.command, SafeGuardDecision.APPROVED)
        
        return (
            SafeGuardDecision.APPROVED,
            "Acción validada por SafeGuard.",
            {'risk': 'low'}
        )

    def _log_decision(self, command: str, decision: str):
        """Mantiene un registro interno de auditoría."""
        self.history.append({
            'command': command,
            'decision': decision,
            'timestamp': '...' # En implementación real usaría datetime
        })
        log_info(f"SafeGuard Audit: {command} -> {decision}")
