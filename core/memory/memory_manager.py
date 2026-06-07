"""
memory_manager.py

FASE 19: Gestor Central de Memoria

Orquesta políticas de retención, archivado y limpieza de memoria.
"""

import os
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from pathlib import Path

from core.memory.retention_policy import get_retention_policy, RetentionPolicy
from core.memory.archiver import SessionArchiver
from core.utils.logging import log_info, log_debug, log_success, log_warning


class MemoryManager:
    """
    Gestor central de memoria para ZULY.
    
    Responsabilidades:
    - Aplicar políticas de retención
    - Coordinar archivado
    - Ejecutar limpieza periódica
    - Generar reportes de uso
    """
    
    def __init__(self, policy: Optional[RetentionPolicy] = None):
        """
        Inicializa el gestor de memoria.
        
        Args:
            policy: RetentionPolicy personalizada (None = usar global)
        """
        self.policy = policy if policy else get_retention_policy()
        
        # Inicializar archivers para cada componente
        self.archivers = {}
        self._initialize_archivers()
    
    def _initialize_archivers(self):
        """Inicializa archivers para componentes conocidos."""
        # ActionLogger archiver
        action_log_dir = Path(__file__).parent.parent.parent / 'logs' / 'actions'
        self.archivers['action_logger'] = SessionArchiver(str(action_log_dir))
        
        # Memory archives (trazas, patrones, etc.)
        memory_dir = Path(__file__).parent.parent.parent / 'memory'
        self.archivers['memory'] = SessionArchiver(str(memory_dir))
    
    def apply_retention_policies(self, component: Optional[str] = None) -> Dict[str, Any]:
        """
        Aplica políticas de retención para uno o todos los componentes.
        
        Args:
            component: Componente específico (None = todos)
        
        Returns:
            Resultado de la operación con estadísticas
        """
        log_info("🧹 Aplicando políticas de retención...")
        
        results = {}
        components_to_process = [component] if component else list(self.policy.get_all_policies().keys())
        
        for comp in components_to_process:
            try:
                result = self._apply_policy_for_component(comp)
                results[comp] = result
            except Exception as e:
                log_warning(f"Error aplicando política para '{comp}': {e}")
                results[comp] = {'success': False, 'error': str(e)}
        
        total_archived = sum(r.get('archived_count', 0) for r in results.values())
        
        if total_archived > 0:
            log_success(f"✅ Políticas aplicadas: {total_archived} archivos archivados")
        else:
            log_info("✓ Políticas aplicadas: Sin archivos para archivar")
        
        return {
            'timestamp': datetime.now().isoformat(),
            'components_processed': len(components_to_process),
            'total_archived': total_archived,
            'details': results
        }
    
    def _apply_policy_for_component(self, component: str) -> Dict[str, Any]:
        """Aplica política para un componente específico."""
        config = self.policy.get_policy(component)
        
        # Determinar archiver apropiado
        if component == 'action_logger':
            archiver = self.archivers['action_logger']
            pattern = 'session_*.json'
        else:
            archiver = self.archivers['memory']
            pattern = '*.json'
        
        # Archivar archivos antiguos
        archived = archiver.archive_old_files(
            age_days=config.archive_after_days,
            pattern=pattern
        )
        
        return {
            'success': True,
            'archived_count': len(archived),
            'archived_files': archived,
            'age_threshold_days': config.archive_after_days
        }
    
    def get_memory_report(self) -> Dict[str, Any]:
        """
        Genera reporte completo de uso de memoria.
        
        Returns:
            Dict con estadísticas detalladas
        """
        log_debug("📊 Generando reporte de memoria...")
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'policies': self.policy.to_dict(),
            'components': {}
        }
        
        # ActionLogger stats
        action_archiver = self.archivers['action_logger']
        action_stats = action_archiver.get_archive_stats()
        
        # Contar sesiones activas
        active_sessions = list(action_archiver.base_dir.glob('session_*.json'))
        
        report['components']['action_logger'] = {
            'active_sessions': len(active_sessions),
            'archives': action_stats
        }
        
        # Memory stats (trazas, patrones, etc.)
        memory_archiver = self.archivers['memory']
        memory_stats = memory_archiver.get_archive_stats()
        
        # Contar archivos activos en memory/
        memory_dir = memory_archiver.base_dir
        active_files = []
        if memory_dir.exists():
            active_files = [f for f in memory_dir.glob('*.json') if f.is_file()]
        
        report['components']['memory'] = {
            'active_files': len(active_files),
            'archives': memory_stats
        }
        
        # Calcular totales
        total_active = sum(c.get('active_sessions', 0) + c.get('active_files', 0) 
                          for c in report['components'].values())
        total_archived = sum(c['archives']['total_archived_files'] 
                            for c in report['components'].values())
        total_size_mb = sum(c['archives']['total_size_mb'] 
                           for c in report['components'].values())
        
        report['summary'] = {
            'total_active_items': total_active,
            'total_archived_items': total_archived,
            'total_archive_size_mb': round(total_size_mb, 2)
        }
        
        return report
    
    def cleanup_old_archives(self, keep_months: int = 6) -> Dict[str, Any]:
        """
        Limpia archives muy antiguos (más de N meses).
        
        Args:
            keep_months: Meses a mantener
        
        Returns:
            Resultado de la operación
        """
        log_info(f"🗑️ Limpiando archives > {keep_months} meses...")
        
        cutoff_date = datetime.now() - timedelta(days=keep_months * 30)
        deleted_count = 0
        deleted_size = 0
        
        for archiver in self.archivers.values():
            for month_dir in archiver.archive_dir.iterdir():
                if not month_dir.is_dir():
                    continue
                
                # Parsear mes del nombre (YYYY-MM)
                try:
                    month_date = datetime.strptime(month_dir.name, "%Y-%m")
                    
                    if month_date < cutoff_date:
                        # Calcular tamaño antes de eliminar
                        dir_size = sum(f.stat().st_size for f in month_dir.rglob('*') if f.is_file())
                        
                        # Eliminar directorio completo
                        import shutil
                        shutil.rmtree(month_dir)
                        
                        deleted_count += 1
                        deleted_size += dir_size
                        
                        log_debug(f"🗑️ Eliminado archive antiguo: {month_dir.name}")
                except ValueError:
                    # Nombre de directorio no es fecha válida, ignorar
                    continue
        
        if deleted_count > 0:
            log_success(f"✅ Eliminados {deleted_count} archives antiguos ({round(deleted_size/(1024*1024), 2)} MB)")
        else:
            log_info("✓ Sin archives antiguos para eliminar")
        
        return {
            'deleted_archives': deleted_count,
            'freed_space_mb': round(deleted_size / (1024 * 1024), 2),
            'cutoff_date': cutoff_date.isoformat()
        }
    
    def search_historical_data(
        self,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
        component: str = 'action_logger'
    ) -> List[Dict[str, Any]]:
        """
        Busca datos históricos en archives.
        
        Args:
            date_from: Fecha inicial
            date_to: Fecha final
            component: Componente a buscar
        
        Returns:
            Lista de archivos encontrados
        """
        if component not in self.archivers:
            archiver_key = 'action_logger' if component == 'action_logger' else 'memory'
        else:
            archiver_key = component
        
        archiver = self.archivers[archiver_key]
        return archiver.search_archives(date_from, date_to)
    
    def get_config_summary(self) -> Dict[str, Any]:
        """Obtiene resumen de configuración actual."""
        return {
            'policies': self.policy.to_dict(),
            'archivers_initialized': list(self.archivers.keys()),
            'total_components': len(self.policy.get_all_policies())
        }


# Singleton global
_memory_manager: Optional[MemoryManager] = None


def get_memory_manager() -> MemoryManager:
    """Obtiene la instancia global de MemoryManager."""
    global _memory_manager
    if _memory_manager is None:
        _memory_manager = MemoryManager()
    return _memory_manager
