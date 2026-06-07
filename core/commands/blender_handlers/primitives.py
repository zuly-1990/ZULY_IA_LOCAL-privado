"""
primitives.py

Handlers para crear primitivas en Blender.
FASE 17: Refactorizado para usar EngineAdapter.
"""

from typing import Dict, Any, Optional
from core.utils.logging import log_success, log_warning, log_info


def create_cube_handler(parameters: Dict[str, Any], adapter=None) -> Dict[str, Any]:
    """
    Crea un cubo usando EngineAdapter.
    
    FASE 17: Ahora usa EngineAdapter en lugar de bpy directo.
    
    Parameters:
        parameters: Dict con:
            - location: [x, y, z] opcional (default: [0, 0, 0])
            - scale: float opcional (default: 1.0)
            - color: [r, g, b] opcional
        adapter: EngineAdapter instance (si es None, se obtiene automáticamente)
    
    Returns:
        Dict con status y resultado
    """
    # Obtener adapter si no se proporciona
    if adapter is None:
        from core.adapters import get_engine_adapter
        adapter = get_engine_adapter()
    
    # Verificar disponibilidad
    if not adapter or not adapter.is_available():
        return {
            'success': False,
            'error': 'Engine adapter not available',
            'hint': 'Blender or compatible 3D engine required'
        }
    
    try:
        # Parámetros por defecto
        location = parameters.get('location', [0, 0, 0])
        scale = parameters.get('scale', 1.0)
        color = parameters.get('color', [1.0, 1.0, 1.0])
        
        # Validar parámetros
        if not isinstance(location, (list, tuple)) or len(location) != 3:
            return {
                'success': False,
                'error': 'Invalid location format. Expected [x, y, z]'
            }
        
        # Validar escala (puede ser float o lista [x,y,z])
        if isinstance(scale, (int, float)):
            if scale <= 0:
                return {'success': False, 'error': 'Invalid scale. Must be positive number'}
        elif isinstance(scale, (list, tuple)):
            if len(scale) != 3 or any(s <= 0 for s in scale):
                return {'success': False, 'error': 'Invalid scale vector. Must be [x,y,z] positive'}
        else:
            return {'success': False, 'error': 'Invalid scale format'}
        
        name = parameters.get('name')
        
        # Crear cubo usando adapter
        result = adapter.create_primitive(
            'cube',
            location=location,
            scale=scale,
            name=name,
            parent=parameters.get('parent')
        )
        
        if not result.get('success', False):
            return result
        
        object_name = result.get('object_name', 'Cube')
        
        # Aplicar color si está disponible
        if color and len(color) == 3:
            try:
                mat_result = adapter.create_material(
                    name="CubeMaterial",
                    color=color
                )
                if mat_result.get('success', False):
                    adapter.apply_material(object_name, "CubeMaterial")
            except Exception as e:
                log_warning(f"Could not apply color: {e}")
        
        log_success(f"Cubo creado en posición {location}")
        
        return {
            'success': True,
            'object_name': object_name,
            'location': location,
            'scale': scale,
            'message': f'Cubo creado exitosamente en {location}'
        }
    
    except Exception as e:
        log_warning(f"Error creating cube: {e}")
        return {
            'success': False,
            'error': str(e)
        }


def create_sphere_handler(parameters: Dict[str, Any], adapter=None) -> Dict[str, Any]:
    """
    Crea una esfera usando EngineAdapter.
    
    FASE 17: Ahora usa EngineAdapter en lugar de bpy directo.
    
    Parameters:
        parameters: Dict con:
            - location: [x, y, z] opcional
            - radius: float opcional (default: 1.0)
            - subdivisions: int opcional (default: 32)
            - color: [r, g, b] opcional
        adapter: EngineAdapter instance (si es None, se obtiene automáticamente)
    
    Returns:
        Dict con status y resultado
    """
    # Obtener adapter si no se proporciona
    if adapter is None:
        from core.adapters import get_engine_adapter
        adapter = get_engine_adapter()
    
    # Verificar disponibilidad
    if not adapter or not adapter.is_available():
        return {
            'success': False,
            'error': 'Engine adapter not available'
        }
    
    try:
        location = parameters.get('location', [0, 0, 0])
        radius = parameters.get('radius', 1.0)
        subdivisions = parameters.get('subdivisions', 32)
        ring_count = parameters.get('ring_count', 16)
        color = parameters.get('color', [1.0, 1.0, 1.0])
        
        # Validar parámetros
        if not isinstance(radius, (int, float)) or radius <= 0:
            return {
                'success': False,
                'error': 'Invalid radius. Must be positive'
            }
        
        name = parameters.get('name')
        
        # Crear esfera usando adapter
        result = adapter.create_primitive(
            'sphere',
            location=location,
            radius=radius,
            name=name,
            parent=parameters.get('parent'),
            segments=int(subdivisions),
            ring_count=int(ring_count),
        )
        
        if not result.get('success', False):
            return result
        
        object_name = result.get('object_name', 'Sphere')
        
        # Aplicar color
        if color and len(color) == 3:
            try:
                mat_result = adapter.create_material(
                    name="SphereMaterial",
                    color=color
                )
                if mat_result.get('success', False):
                    adapter.apply_material(object_name, "SphereMaterial")
            except Exception as e:
                log_warning(f"Could not apply color: {e}")
        
        log_success(f"Esfera creada con radio {radius}")
        
        return {
            'success': True,
            'object_name': object_name,
            'location': location,
            'radius': radius,
            'subdivisions': subdivisions,
            'message': f'Esfera creada exitosamente'
        }
    
    except Exception as e:
        log_warning(f"Error creating sphere: {e}")
        return {
            'success': False,
            'error': str(e)
        }


def create_cylinder_handler(parameters: Dict[str, Any], adapter=None) -> Dict[str, Any]:
    """
    Crea un cilindro usando EngineAdapter.
    
    FASE 17: Ahora usa EngineAdapter en lugar de bpy directo.
    
    Parameters:
        parameters: Dict con:
            - location: [x, y, z] opcional
            - radius: float opcional
            - depth: float opcional
            - vertices: int opcional (default: 32)
        adapter: EngineAdapter instance (si es None, se obtiene automáticamente)
    
    Returns:
        Dict con status y resultado
    """
    # Obtener adapter si no se proporciona
    if adapter is None:
        from core.adapters import get_engine_adapter
        adapter = get_engine_adapter()
    
    # Verificar disponibilidad
    if not adapter or not adapter.is_available():
        return {
            'success': False,
            'error': 'Engine adapter not available'
        }
    
    try:
        location = parameters.get('location', [0, 0, 0])
        radius = parameters.get('radius', 1.0)
        depth = parameters.get('depth', 2.0)
        vertices = parameters.get('vertices', 32)
        
        name = parameters.get('name')
        
        # Crear cilindro usando adapter
        result = adapter.create_primitive(
            'cylinder',
            location=location,
            radius=radius,
            scale=depth / 2.0,  # Adapter usa scale, no depth
            name=name,
            parent=parameters.get('parent')
        )
        
        if not result.get('success', False):
            return result
        
        object_name = result.get('object_name', 'Cylinder')
        
        log_success(f"Cilindro creado: radio={radius}, profundidad={depth}")
        
        return {
            'success': True,
            'object_name': object_name,
            'location': location,
            'radius': radius,
            'depth': depth,
            'message': 'Cilindro creado exitosamente'
        }
    
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


def create_plane_handler(parameters: Dict[str, Any], adapter=None) -> Dict[str, Any]:
    """
    Crea un plano usando EngineAdapter (FASE A1.4).
    """
    if adapter is None:
        from core.adapters import get_engine_adapter
        adapter = get_engine_adapter()
    
    if not adapter or not adapter.is_available():
        return {'success': False, 'error': 'Engine adapter not available'}
    
    try:
        location = parameters.get('location', [0, 0, 0])
        scale = parameters.get('scale', 1.0)
        color = parameters.get('color', [1.0, 1.0, 1.0])
        name = parameters.get('name')
        
        # Validar parámetros básicos
        if not isinstance(location, (list, tuple)) or len(location) != 3:
            return {'success': False, 'error': 'Invalid location'}
            
        # Crear plano
        result = adapter.create_primitive(
            'plane',
            location=location,
            scale=scale,
            name=name,
            parent=parameters.get('parent')
        )
        
        if not result.get('success', False):
            return result
        
        object_name = result.get('object_name', 'Plane')
        
        # Color opcional
        if color and len(color) == 3:
            try:
                mat_result = adapter.create_material(name="PlaneMaterial", color=color)
                if mat_result.get('success', False):
                    adapter.apply_material(object_name, "PlaneMaterial")
            except Exception:
                pass
        
        log_success(f"Plano creado: {object_name}")
        return {
            'success': True,
            'object_name': object_name,
            'location': location,
            'scale': scale
        }
    except Exception as e:
        log_warning(f"Error creating plane: {e}")
        return {'success': False, 'error': str(e)}

def create_cone_handler(parameters: Dict[str, Any], adapter=None) -> Dict[str, Any]:
    """
    Crea un cono usando EngineAdapter.
    """
    if adapter is None:
        from core.adapters import get_engine_adapter
        adapter = get_engine_adapter()
    
    if not adapter or not adapter.is_available():
        return {'success': False, 'error': 'Engine adapter not available'}
    
    try:
        location = parameters.get('location', [0, 0, 0])
        radius = parameters.get('radius', 1.0)
        depth = parameters.get('depth', 2.0)
        name = parameters.get('name')
        
        # Crear cono
        result = adapter.create_primitive(
            'cone',
            location=location,
            radius=radius,
            scale=depth / 1.0, # El adapter para cono usa scale para depth usualmente
            name=name,
            parent=parameters.get('parent')
        )
        
        if not result.get('success', False):
            return result
        
        object_name = result.get('object_name', 'Cone')
        
        log_success(f"Cono creado: {object_name}")
        return {
            'success': True,
            'object_name': object_name,
            'location': location,
            'radius': radius,
            'depth': depth
        }
    except Exception as e:
        log_warning(f"Error creating cone: {e}")
        return {'success': False, 'error': str(e)}
