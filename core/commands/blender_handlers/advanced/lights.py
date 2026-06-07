"""
lights.py - Handlers para luces en Blender
FASE 17: Refactorizado para usar EngineAdapter.
"""

from typing import Dict, Any
from core.utils.logging import log_success, log_warning, log_info


def create_light_handler(parameters: Dict[str, Any], adapter=None) -> Dict[str, Any]:
    """
    Crea una luz usando EngineAdapter.
    
    FASE 17: Ahora usa EngineAdapter en lugar de bpy directo.
    
    Parameters:
        parameters: Dict con:
            - name: str (nombre de la luz)
            - light_type: str ('POINT', 'AREA', 'SUN', 'SPOT')
            - location: [x, y, z]
            - energy: float (intensidad)
            - color: [r, g, b]
        adapter: EngineAdapter instance
    """
    if adapter is None:
        from core.adapters import get_engine_adapter
        adapter = get_engine_adapter()
    
    if not adapter or not adapter.is_available():
        return {'success': False, 'error': 'Engine adapter not available'}
    
    try:
        name = parameters.get('name', 'Light_001')
        light_type = parameters.get('light_type', 'POINT')
        location = parameters.get('location', [0, 0, 3])
        energy = parameters.get('energy', 1000.0)
        color = parameters.get('color', [1.0, 1.0, 1.0])
        
        # Validar tipo de luz
        if light_type not in ['POINT', 'AREA', 'SUN', 'SPOT']:
            return {'success': False, 'error': 'Invalid light_type'}
        
        # Crear luz usando adapter
        result = adapter.create_light(
            light_type=light_type,
            name=name,
            location=location,
            energy=energy,
            color=color
        )
        
        if not result.get('success', False):
            return result
        
        log_success(f"Luz {light_type} '{name}' creada")
        
        return {
            'success': True,
            'object_name': result.get('light_name', name),
            'light_name': result.get('light_name', name),
            'light_type': light_type,
            'location': location,
            'energy': energy,
            'message': f'Luz {light_type} creada exitosamente'
        }
    
    except Exception as e:
        log_warning(f"Error creating light: {e}")
        return {'success': False, 'error': str(e)}


def set_light_energy_handler(parameters: Dict[str, Any], adapter=None) -> Dict[str, Any]:
    """
    Cambia la intensidad de una luz usando EngineAdapter.
    
    FASE 17: Ahora usa EngineAdapter en lugar de bpy directo.
    """
    if adapter is None:
        from core.adapters import get_engine_adapter
        adapter = get_engine_adapter()
    
    if not adapter or not adapter.is_available():
        return {'success': False, 'error': 'Engine adapter not available'}
    
    try:
        light_name = parameters.get('light_name')
        energy = parameters.get('energy', 1000.0)
        
        if not light_name:
            return {'success': False, 'error': 'Missing light_name'}
        
        result = adapter.update_light(light_name, energy=energy)
        
        if result.get('success', False):
            log_success(f"Energía de luz '{light_name}' actualizada a {energy}")
        
        return result
    
    except Exception as e:
        log_warning(f"Error setting light energy: {e}")
        return {'success': False, 'error': str(e)}


def set_light_color_handler(parameters: Dict[str, Any], adapter=None) -> Dict[str, Any]:
    """
    Cambia el color de una luz usando EngineAdapter.
    
    FASE 17: Ahora usa EngineAdapter en lugar de bpy directo.
    """
    if adapter is None:
        from core.adapters import get_engine_adapter
        adapter = get_engine_adapter()
    
    if not adapter or not adapter.is_available():
        return {'success': False, 'error': 'Engine adapter not available'}
    
    try:
        light_name = parameters.get('light_name')
        color = parameters.get('color', [1.0, 1.0, 1.0])
        
        if not light_name:
            return {'success': False, 'error': 'Missing light_name'}
        
        result = adapter.update_light(light_name, color=color)
        
        if result.get('success', False):
            log_success(f"Color de luz '{light_name}' actualizado")
        
        return result
    
    except Exception as e:
        log_warning(f"Error setting light color: {e}")
        return {'success': False, 'error': str(e)}
