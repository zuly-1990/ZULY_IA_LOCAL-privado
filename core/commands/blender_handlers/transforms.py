"""
transforms.py

Handlers para transformar objetos (mover, rotar, escalar).
FASE 17: Refactorizado para usar EngineAdapter.
"""

from typing import Dict, Any
from core.utils.logging import log_success, log_warning


def move_object_handler(parameters: Dict[str, Any], adapter=None) -> Dict[str, Any]:
    """
    Mueve un objeto usando EngineAdapter.
    
    FASE 17: Ahora usa EngineAdapter en lugar de bpy directo.
    """
    if adapter is None:
        from core.adapters import get_engine_adapter
        adapter = get_engine_adapter()
    
    if not adapter or not adapter.is_available():
        return {'success': False, 'error': 'Engine adapter not available'}
    
    try:
        location = parameters.get('location')
        offset = parameters.get('offset')
        object_name = parameters.get('object_name')
        
        # Mover usando adapter
        result = adapter.move_object(object_name, location=location, offset=offset)
        
        if result.get('success', False):
            log_success(f"Objeto {result.get('object_name')} movido")
        
        return result
    
    except Exception as e:
        log_warning(f"Error moving object: {e}")
        return {'success': False, 'error': str(e)}


def rotate_object_handler(parameters: Dict[str, Any], adapter=None) -> Dict[str, Any]:
    """
    Rota un objeto usando EngineAdapter.
    
    FASE 17: Ahora usa EngineAdapter en lugar de bpy directo.
    """
    if adapter is None:
        from core.adapters import get_engine_adapter
        adapter = get_engine_adapter()
    
    if not adapter or not adapter.is_available():
        return {'success': False, 'error': 'Engine adapter not available'}
    
    try:
        rotation = parameters.get('rotation')
        degrees = parameters.get('degrees', False)
        object_name = parameters.get('object_name')
        
        if not rotation:
            return {'success': False, 'error': 'rotation parameter required'}
        
        # Rotar usando adapter
        result = adapter.rotate_object(object_name, rotation, degrees=degrees)
        
        if result.get('success', False):
            log_success(f"Objeto {result.get('object_name')} rotado")
        
        return result
    
    except Exception as e:
        log_warning(f"Error rotating object: {e}")
        return {'success': False, 'error': str(e)}


def scale_object_handler(parameters: Dict[str, Any], adapter=None) -> Dict[str, Any]:
    """
    Escala un objeto usando EngineAdapter.
    
    FASE 17: Ahora usa EngineAdapter en lugar de bpy directo.
    """
    if adapter is None:
        from core.adapters import get_engine_adapter
        adapter = get_engine_adapter()
    
    if not adapter or not adapter.is_available():
        return {'success': False, 'error': 'Engine adapter not available'}
    
    try:
        scale = parameters.get('scale', 1.0)
        object_name = parameters.get('object_name')
        
        if not scale:
            return {'success': False, 'error': 'scale parameter required'}
        
        # Escalar usando adapter
        result = adapter.scale_object(object_name, scale)
        
        if result.get('success', False):
            log_success(f"Objeto {result.get('object_name')} escalado")
        
        return result
    
    except Exception as e:
        log_warning(f"Error scaling object: {e}")
        return {'success': False, 'error': str(e)}
