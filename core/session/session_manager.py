"""
core/session/session_manager.py
===============================

Gestor de sesiones del agente Zuly.
Maneja registro de sesiones, snapshots de Blender y análisis de escena.

Extraído de agent.py como parte del refactoring God Objects (Fase 3).
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
from core.utils.logging import log_info, log_warning, log_debug
from core.session.execution_context import ExecutionContext


class SessionManager:
    """
    Gestiona el ciclo de vida de sesiones del agente Zuly.
    
    Responsabilidades:
    - Crear y gestionar ExecutionContext
    - Capturar snapshots de Blender
    - Analizar estado de escena
    - Generar reportes de sistema
    """
    
    def __init__(self, engine_adapter=None, auto_monitor: bool = True):
        self.engine_adapter = engine_adapter
        self.auto_monitor = auto_monitor
        self.execution_context = ExecutionContext()
        self._blender_history: List[Dict] = []
        self.MAX_BLENDER_HISTORY = 5
        
        # Componentes de observación (inyectados desde Agent)
        self.blender_observer = None
        self.semantic_observer = None
        self.last_scene_state: Optional[Dict] = None
    
    def set_observers(self, blender_observer, semantic_observer):
        """Inyecta observadores de Blender."""
        self.blender_observer = blender_observer
        self.semantic_observer = semantic_observer
    
    def get_blender_snapshot(self) -> Dict[str, Any]:
        """Captura y almacena un snapshot del estado de Blender."""
        if not self.blender_observer:
            return {"error": "No blender observer available"}
        
        snap = self.blender_observer.snapshot()
        self._blender_history.append(snap)
        if len(self._blender_history) > self.MAX_BLENDER_HISTORY:
            self._blender_history.pop(0)
        return snap
    
    def analyze_scene(self) -> Dict[str, Any]:
        """
        Realiza un análisis completo del entorno actual.
        Combina: Contexto + Snapshot Visual + Interpretación Semántica.
        """
        if not self.blender_observer or not self.semantic_observer:
            return {"error": "Observers not initialized"}
        
        # 1. Contexto técnico (bpy.data.objects, etc.)
        technical = self.blender_observer.snapshot()
        
        # 2. Interpretación semántica ("Es una escena de arquitectura")
        try:
            semantic = self.semantic_observer.interpret_scene(technical)
        except Exception as e:
            log_warning(f"Error en interpretación semántica: {e}")
            semantic = {"interpretation": "unknown", "confidence": 0}
        
        # 3. Consolidar análisis
        full_analysis = {
            "technical": technical,
            "semantic": semantic,
            "timestamp": datetime.now().isoformat(),
            "object_count": technical.get("object_count", 0),
            "scene_type": semantic.get("interpretation", "unknown"),
        }
        
        self.last_scene_state = full_analysis
        self.execution_context.add_scene_state(full_analysis)
        return full_analysis
    
    def compare_blender_snapshots(self, old: Dict, new: Dict) -> Dict:
        """Compara dos snapshots y detecta cambios básicos."""
        old_names = {o["name"] for o in old.get("objects", [])}
        new_names = {o["name"] for o in new.get("objects", [])}
        
        added = new_names - old_names
        removed = old_names - new_names
        
        return {
            "added": list(added),
            "removed": list(removed),
            "object_count_before": len(old_names),
            "object_count_after": len(new_names),
            "total_change": len(added) + len(removed)
        }
    
    def get_system_state(self) -> Dict[str, Any]:
        """Captura el estado completo del sistema ZULY."""
        from core.observability.system_state import SystemStateSnapshot
        return SystemStateSnapshot(self).capture()
    
    def system_report(self) -> str:
        """Genera reporte completo del sistema para humanos."""
        snapshot_data = self.get_system_state()
        
        from core.observability.system_state import SystemStateSnapshot
        snapshot = SystemStateSnapshot(self)
        snapshot.data = snapshot_data
        return snapshot.to_human_readable()
    
    def register_execution(self, command_name: str, success: bool, result: Any = None, error: str = None):
        """Registra una ejecución en el contexto."""
        self.execution_context.add_execution(command_name, success, result, error)
    
    def get_execution_summary(self) -> Dict[str, Any]:
        """Obtiene resumen de ejecución de la sesión actual."""
        return self.execution_context.get_summary()
    
    def get_stats(self) -> Dict[str, Any]:
        """Obtiene estadísticas detalladas de la sesión."""
        return self.execution_context.get_execution_stats()
    
    def register_learned_decision(self, intent: Any, response: Dict):
        """Registra una decisión autorizada en la bitácora segura."""
        log_path = "bitacora/DECISIONES_APRENDIDAS.md"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        try:
            with open(log_path, 'a', encoding='utf-8') as f:
                f.write(f"\n## {timestamp} - DECISIÓN AUTORIZADA\n")
                f.write(f"**Intención:** {intent.command_name if hasattr(intent, 'command_name') else 'unknown'}\n")
                f.write(f"**Confianza:** {intent.confidence if hasattr(intent, 'confidence') else 0:.2f}\n")
                f.write(f"**Éxito:** {response.get('success', False)}\n")
                if 'result' in response:
                    f.write(f"**Resumen:** {str(response['result'])[:200]}...\n")
        except Exception as e:
            log_warning(f"Error al registrar decisión: {e}")
    
    def register_blocked_attempt(self, user: str, reason: str):
        """Registra intentos bloqueados en la bitácora segura."""
        log_path = "bitacora/DECISIONES_APRENDIDAS.md"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        try:
            with open(log_path, 'a', encoding='utf-8') as f:
                f.write(f"\n## {timestamp} - INTENTO BLOQUEADO\n")
                f.write(f"**Usuario:** {user}\n")
                f.write(f"**Razón:** {reason}\n")
                f.write(f"**Estado:** ⚠️ MODO PROTEGIDO\n")
        except Exception as e:
            log_warning(f"Error al registrar bloqueo: {e}")
