"""
cameras.py - Handlers para cámaras en Blender
FASE 17: Refactorizado para usar EngineAdapter.
"""

from typing import Dict, Any
from core.utils.logging import log_success, log_warning, log_info


def create_camera_handler(parameters: Dict[str, Any], adapter=None) -> Dict[str, Any]:
    """
    Crea una cámara usando EngineAdapter.
    
    FASE 17: Ahora usa EngineAdapter en lugar de bpy directo.
    
    Parameters:
        parameters: Dict con:
            - name: str (nombre de la cámara)
            - location: [x, y, z]
            - focal_length: float (default 50)
            - sensor_width: float (default 36)
        adapter: EngineAdapter instance
    """
    if adapter is None:
        from core.adapters import get_engine_adapter
        adapter = get_engine_adapter()
    
    if not adapter or not adapter.is_available():
        return {'success': False, 'error': 'Engine adapter not available'}
    
    try:
        name = parameters.get('name', 'Camera_001')
        location = parameters.get('location', [10, -10, 5])
        focal_length = parameters.get('focal_length', 50.0)
        sensor_width = parameters.get('sensor_width', 36.0)
        
        # Crear cámara usando adapter
        result = adapter.create_camera(
            name=name,
            location=location,
            focal_length=focal_length
        )
        
        if not result.get('success', False):
            return result
        
        log_success(f"Cámara '{name}' creada")
        
        return {
            'success': True,
            'object_name': result.get('camera_name', name),
            'camera_name': result.get('camera_name', name),
            'location': location,
            'focal_length': focal_length,
            'message': f'Cámara creada exitosamente'
        }
    
    except Exception as e:
        log_warning(f"Error creating camera: {e}")
        return {'success': False, 'error': str(e)}


def set_active_camera_handler(parameters: Dict[str, Any], adapter=None) -> Dict[str, Any]:
    """
    Establece una cámara como activa usando EngineAdapter.
    
    FASE 17: Ahora usa EngineAdapter en lugar de bpy directo.
    """
    if adapter is None:
        from core.adapters import get_engine_adapter
        adapter = get_engine_adapter()
    
    if not adapter or not adapter.is_available():
        return {'success': False, 'error': 'Engine adapter not available'}
    
    try:
        camera_name = parameters.get('camera_name')
        
        if not camera_name:
            return {'success': False, 'error': 'Missing camera_name'}
        
        result = adapter.set_active_camera(camera_name)
        
        if result.get('success', False):
            log_success(f"Cámara '{camera_name}' establecida como activa")
        
        return result
    
    except Exception as e:
        log_warning(f"Error setting active camera: {e}")
        return {'success': False, 'error': str(e)}


def position_camera_handler(parameters: Dict[str, Any], adapter=None) -> Dict[str, Any]:
    """
    Posiciona y orienta una cámara mirando un punto usando EngineAdapter.
    
    FASE 17: Ahora usa EngineAdapter en lugar de bpy directo.
    """
    if adapter is None:
        from core.adapters import get_engine_adapter
        adapter = get_engine_adapter()
    
    if not adapter or not adapter.is_available():
        return {'success': False, 'error': 'Engine adapter not available'}
    
    try:
        camera_name = parameters.get('camera_name')
        location = parameters.get('location', [10, -10, 5])
        look_at = parameters.get('look_at', [0, 0, 0])
        
        if not camera_name:
            return {'success': False, 'error': 'Missing camera_name'}
        
        result = adapter.position_camera(camera_name, location, look_at)
        
        if result.get('success', False):
            log_success(f"Cámara '{camera_name}' posicionada")
        
        return result
    
    except Exception as e:
        log_warning(f"Error positioning camera: {e}")
        return {'success': False, 'error': str(e)}
