"""
action_logger.py

FASE 18.5: Mini-Log Interno
Registra acciones de forma ligera, local, sin red ni persistencia pesada.

Por cada acción guarda:
- Qué intentó hacer
- Dónde
- Resultado (OK / FAIL)
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
import json
import os
from core.utils.logging import log_debug


@dataclass
class ActionRecord:
    """Registro de una acción individual."""
    timestamp: str
    action: str
    target: str
    result: str  # "OK" | "FAIL"
    details: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'timestamp': self.timestamp,
            'action': self.action,
            'target': self.target,
            'result': self.result,
            'details': self.details
        }
    
    def to_log_line(self) -> str:
        """Formato de línea para log de texto."""
        status = "✓" if self.result == "OK" else "✗"
        return f"[{self.timestamp}] {status} {self.action} → {self.target}" + (f" ({self.details})" if self.details else "")


class ActionLogger:
    """
    Logger ligero de acciones para trazabilidad.
    
    Características:
    - Sin nube, sin red
    - Persistencia local simple (JSON)
    - Rolling window para evitar crecimiento infinito
    - Base para futuro Mini Book
    """
    
    MAX_RECORDS = 500  # Rolling window
    
    def __init__(self, log_dir: Optional[str] = None):
        """
        Inicializa el logger de acciones.
        
        Args:
            log_dir: Directorio para guardar logs. Si es None, usa default.
        """
        self._records: List[ActionRecord] = []
        self._session_start = datetime.now()
        self._session_id = self._session_start.strftime("%Y%m%d_%H%M%S")
        
        if log_dir is None:
            # Default: logs/ en el directorio del proyecto
            self._log_dir = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                "logs", "actions"
            )
        else:
            self._log_dir = log_dir
        
        os.makedirs(self._log_dir, exist_ok=True)
    
    def log_action(
        self,
        action: str,
        target: str,
        success: bool,
        details: Optional[str] = None
    ) -> ActionRecord:
        """
        Registra una acción.
        
        Args:
            action: Qué se intentó hacer (ej: "create_cube", "move_object")
            target: Dónde (ej: "Cube_001", "Scene")
            success: Si tuvo éxito
            details: Detalles opcionales
        
        Returns:
            El registro creado.
        """
        record = ActionRecord(
            timestamp=datetime.now().strftime("%H:%M:%S"),
            action=action,
            target=target,
            result="OK" if success else "FAIL",
            details=details
        )
        
        self._records.append(record)
        
        # Rolling window + auto-save (FASE 19)
        if len(self._records) > self.MAX_RECORDS:
            # Guardar sesión actual antes de limpiar
            self.save_session()
            
            # Archivar sesión automáticamente
            self._auto_archive_old_sessions()
            
            # Mantener solo últimos MAX_RECORDS
            self._records = self._records[-self.MAX_RECORDS:]
        
        log_debug(f"📝 Action: {record.to_log_line()}")
        
        return record
    
    def log_ok(self, action: str, target: str, details: Optional[str] = None) -> ActionRecord:
        """Shortcut para registrar acción exitosa."""
        return self.log_action(action, target, True, details)
    
    def log_fail(self, action: str, target: str, details: Optional[str] = None) -> ActionRecord:
        """Shortcut para registrar acción fallida."""
        return self.log_action(action, target, False, details)
    
    def get_recent(self, count: int = 10) -> List[ActionRecord]:
        """Obtiene las últimas N acciones."""
        return self._records[-count:]
    
    def get_session_summary(self) -> Dict[str, Any]:
        """Obtiene resumen de la sesión actual."""
        ok_count = sum(1 for r in self._records if r.result == "OK")
        fail_count = sum(1 for r in self._records if r.result == "FAIL")
        
        return {
            'session_id': self._session_id,
            'session_start': self._session_start.isoformat(),
            'total_actions': len(self._records),
            'ok_count': ok_count,
            'fail_count': fail_count,
            'success_rate': ok_count / len(self._records) if self._records else 1.0
        }
    
    def save_session(self) -> str:
        """
        Guarda la sesión actual a disco.
        
        Returns:
            Path del archivo guardado.
        """
        filename = f"session_{self._session_id}.json"
        filepath = os.path.join(self._log_dir, filename)
        
        data = {
            'session': self.get_session_summary(),
            'records': [r.to_dict() for r in self._records]
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        log_debug(f"📁 Session saved: {filepath}")
        return filepath
    
    def export_to_markdown(self) -> str:
        """
        Exporta los registros a formato Markdown.
        
        Returns:
            String con el contenido Markdown.
        """
        summary = self.get_session_summary()
        
        lines = [
            f"# Action Log - Session {self._session_id}",
            f"",
            f"**Start:** {summary['session_start']}",
            f"**Total actions:** {summary['total_actions']}",
            f"**Success rate:** {summary['success_rate']*100:.1f}%",
            f"",
            "---",
            "",
            "## Actions",
            "",
            "| Time | Status | Action | Target | Details |",
            "|------|--------|--------|--------|---------|"
        ]
        
        for record in self._records:
            status = "✅" if record.result == "OK" else "❌"
            details = record.details or "—"
            lines.append(f"| {record.timestamp} | {status} | {record.action} | {record.target} | {details} |")
        
        return "\n".join(lines)
    
    def clear(self):
        """Limpia todos los registros de la sesión actual.\"\"\""""
        self._records = []
        log_debug("📝 Action log cleared")
    
    def _auto_archive_old_sessions(self, age_days: int = 7):
        """
        FASE 19: Archiva automáticamente sesiones antiguas.
        
        Args:
            age_days: Días antes de archivar (default: 7)
        """
        try:
            from core.memory.archiver import SessionArchiver
            
            archiver = SessionArchiver(self._log_dir)
            archiver.archive_old_files(age_days=age_days, pattern='session_*.json')
        except Exception as e:
            # No fallar si el archivado falla
            log_debug(f"⚠️ Auto-archive falló: {e}")


# Singleton para uso global
_action_logger: Optional[ActionLogger] = None


def get_action_logger() -> ActionLogger:
    """Obtiene la instancia global del ActionLogger."""
    global _action_logger
    if _action_logger is None:
        _action_logger = ActionLogger()
    return _action_logger


def log_action(action: str, target: str, success: bool, details: str = None):
    """Helper function para logging rápido."""
    get_action_logger().log_action(action, target, success, details)
