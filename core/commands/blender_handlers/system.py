"""
system.py

Handlers para funciones de sistema.
FASE 17: Refactorizado para usar EngineAdapter.
"""

from typing import Dict, Any
from core.utils.logging import log_success, log_info, log_warning
import os

def get_system_info_handler(parameters: Dict[str, Any], adapter=None) -> Dict[str, Any]:
    """
    Obtiene información del sistema usando EngineAdapter.
    
    FASE 17: Ahora usa EngineAdapter en lugar de bpy directo.
    """
    if adapter is None:
        from core.adapters import get_engine_adapter
        adapter = get_engine_adapter()
    
    if not adapter or not adapter.is_available():
        return {'success': False, 'error': 'Engine adapter not available'}
    
    try:
        import sys
        
        # Obtener info del motor
        engine_info = adapter.get_engine_info()
        
        if not engine_info.get('success', False):
            return engine_info
        
        info = {
            'engine_name': engine_info.get('name', 'Unknown'),
            'engine_version': engine_info.get('version', 'Unknown'),
            'engine_version_full': engine_info.get('version_string', 'Unknown'),
            'python_version': f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
            'platform': sys.platform,
            'capabilities': engine_info.get('capabilities', [])
        }
        
        log_success("System info retrieved")
        
        return {
            'success': True,
            'system_info': info,
            'message': 'System information retrieved'
        }
    
    except Exception as e:
        return {'success': False, 'error': str(e)}

def save_blend_handler(parameters: Dict[str, Any], adapter=None) -> Dict[str, Any]:
    """
    Guarda el archivo .blend usando EngineAdapter.
    
    FASE 17: Ahora usa EngineAdapter en lugar de bpy directo.
    
    NOTA: La funcionalidad de guardar archivo no está en el adapter estándar.
    Esta es una limitación conocida del desacoplamiento.
    """
    if adapter is None:
        from core.adapters import get_engine_adapter
        adapter = get_engine_adapter()
    
    if not adapter or not adapter.is_available():
        return {'success': False, 'error': 'Engine adapter not available'}
    
    try:
        from pathlib import Path
        from datetime import datetime
        
        filepath = parameters.get('filepath') or parameters.get('path')
        filename = parameters.get('filename')
        
        # FASE 5: Si no hay filepath en parámetros, pero hay una ruta en el mensaje original (heurística)
        if not filepath and 'in' in str(parameters).lower():
            # Intento de rescate si el NLU falló en extraer la ruta pero está en el contexto
            pass # Implementar si es necesario, por ahora confiaremos en parámetros explícitos
            
        # Si no se da ruta, usar una por defecto
        if not filepath:
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"zuly_save_{timestamp}.blend"
                
            # FASE 17/Weekend 3: Usar ZULY_PROJECTS como ruta estándar (según manual)
            base_dir = Path(os.getcwd()) / "ZULY_PROJECTS"
            base_dir.mkdir(parents=True, exist_ok=True)
            filepath = str(base_dir / filename)
        
        log_info(f"Guardando archivo en: {filepath}")
        
        # Usar adapter para exportar (como BLEND)
        result = adapter.export_scene('BLEND', filepath)
        
        if result.get('success', False):
            log_success(f"Archivo guardado exitosamente: {filepath}")
        
        return result
    
    except Exception as e:
        log_warning(f"Error guardando archivo: {e}")
        return {'success': False, 'error': str(e)}
