"""
modifiers.py - Handlers para modificadores en Blender
FASE 17: Refactorizado para usar EngineAdapter.
"""

from typing import Dict, Any
from core.utils.logging import log_success, log_warning, log_info


def add_subdivision_surface_handler(parameters: Dict[str, Any], adapter=None) -> Dict[str, Any]:
    """
    Agrega un modificador Subdivision Surface usando EngineAdapter.
    
    FASE 17: Ahora usa EngineAdapter en lugar de bpy directo.
    
    Parameters:
        parameters: Dict con:
            - object_name: str
            - levels: int (niveles de subdivisión)
            - render_levels: int (niveles para render)
        adapter: EngineAdapter instance
    """
    if adapter is None:
        from core.adapters import get_engine_adapter
        adapter = get_engine_adapter()
    
    if not adapter or not adapter.is_available():
        return {'success': False, 'error': 'Engine adapter not available'}
    
    try:
        obj_name = parameters.get('object_name')
        levels = parameters.get('levels', 2)
        render_levels = parameters.get('render_levels', 3)
        
        if not obj_name:
            return {'success': False, 'error': 'Missing object_name'}
        
        if levels < 0 or levels > 6:
            return {'success': False, 'error': 'Levels must be 0-6'}
        
        # Agregar modificador usando adapter
        result = adapter.add_modifier(
            obj_name,
            'SUBSURF',
            levels=levels,
            render_levels=render_levels
        )
        
        if result.get('success', False):
            log_success(f"Subdivision Surface agregado a '{obj_name}'")
        
        return {
            'success': result.get('success', False),
            'object_name': obj_name,
            'levels': levels,
            'render_levels': render_levels,
            'message': 'Modificador agregado' if result.get('success') else result.get('error', 'Error')
        }
    
    except Exception as e:
        log_warning(f"Error adding subdivision surface: {e}")
        return {'success': False, 'error': str(e)}


def add_array_modifier_handler(parameters: Dict[str, Any], adapter=None) -> Dict[str, Any]:
    """
    Agrega un modificador Array usando EngineAdapter.
    
    FASE 17: Ahora usa EngineAdapter en lugar de bpy directo.
    """
    if adapter is None:
        from core.adapters import get_engine_adapter
        adapter = get_engine_adapter()
    
    if not adapter or not adapter.is_available():
        return {'success': False, 'error': 'Engine adapter not available'}
    
    try:
        obj_name = parameters.get('object_name')
        count = parameters.get('count', 3)
        offset_x = parameters.get('offset_x', 2.0)
        offset_y = parameters.get('offset_y', 0.0)
        offset_z = parameters.get('offset_z', 0.0)
        
        if not obj_name:
            return {'success': False, 'error': 'Missing object_name'}
        
        if count < 1 or count > 1000:
            return {'success': False, 'error': 'Count must be 1-1000'}
        
        result = adapter.add_modifier(
            obj_name,
            'ARRAY',
            count=count,
            offset_x=offset_x,
            offset_y=offset_y,
            offset_z=offset_z
        )
        
        if result.get('success', False):
            log_success(f"Array modifier agregado a '{obj_name}' con {count} copias")
        
        return {
            'success': result.get('success', False),
            'object_name': obj_name,
            'count': count,
            'offset': (offset_x, offset_y, offset_z),
            'message': 'Array modifier agregado' if result.get('success') else result.get('error', 'Error')
        }
    
    except Exception as e:
        log_warning(f"Error adding array modifier: {e}")
        return {'success': False, 'error': str(e)}


def add_weighted_normal_handler(parameters: Dict[str, Any], adapter=None) -> Dict[str, Any]:
    """Agrega modificador Weighted Normal (normales de alta calidad en mallas densas)."""
    if adapter is None:
        from core.adapters import get_engine_adapter
        adapter = get_engine_adapter()

    if not adapter or not adapter.is_available():
        return {'success': False, 'error': 'Engine adapter not available'}

    try:
        obj_name = parameters.get('object_name')
        if not obj_name:
            return {'success': False, 'error': 'Missing object_name'}
        keep = parameters.get('keep_sharp', True)
        result = adapter.add_modifier(obj_name, 'WEIGHTED_NORMAL', keep_sharp=keep)
        if result.get('success', False):
            log_success(f"Weighted Normal agregado a '{obj_name}'")
        return {
            'success': result.get('success', False),
            'object_name': obj_name,
            'message': 'Weighted Normal agregado' if result.get('success') else result.get('error', 'Error'),
        }
    except Exception as e:
        log_warning(f"Error weighted normal: {e}")
        return {'success': False, 'error': str(e)}


def add_bevel_modifier_handler(parameters: Dict[str, Any], adapter=None) -> Dict[str, Any]:
    """
    Agrega un modificador Bevel usando EngineAdapter.
    
    FASE 17: Ahora usa EngineAdapter en lugar de bpy directo.
    """
    if adapter is None:
        from core.adapters import get_engine_adapter
        adapter = get_engine_adapter()
    
    if not adapter or not adapter.is_available():
        return {'success': False, 'error': 'Engine adapter not available'}
    
    try:
        obj_name = parameters.get('object_name')
        width = parameters.get('width', 0.1)
        segments = parameters.get('segments', 2)
        
        if not obj_name:
            return {'success': False, 'error': 'Missing object_name'}
        
        if width <= 0:
            return {'success': False, 'error': 'Width must be positive'}
        
        result = adapter.add_modifier(
            obj_name,
            'BEVEL',
            width=width,
            segments=segments
        )
        
        if result.get('success', False):
            log_success(f"Bevel modifier agregado a '{obj_name}'")
        
        return {
            'success': result.get('success', False),
            'object_name': obj_name,
            'width': width,
            'segments': segments,
            'message': 'Bevel modifier agregado' if result.get('success') else result.get('error', 'Error')
        }
    
    except Exception as e:
        log_warning(f"Error adding bevel modifier: {e}")
        return {'success': False, 'error': str(e)}

def apply_modifier_handler(parameters: Dict[str, Any], adapter=None) -> Dict[str, Any]:
    """
    Aplica (hace permanente) un modificador en un objeto.

    Parameters:
        object_name: str
        modifier_name: str opcional (nombre exacto del modificador en Blender)
        apply_last: bool opcional (True = aplicar el último de la pila)
    """
    if adapter is None:
        from core.adapters import get_engine_adapter
        adapter = get_engine_adapter()

    if not adapter or not adapter.is_available():
        return {'success': False, 'error': 'Engine adapter not available'}

    apply_fn = getattr(adapter, 'apply_modifier', None)
    if not callable(apply_fn):
        return {'success': False, 'error': 'apply_modifier no soportado en este adapter'}

    try:
        obj_name = parameters.get('object_name')
        if not obj_name:
            return {'success': False, 'error': 'Missing object_name'}

        modifier_name = parameters.get('modifier_name')
        apply_last = bool(parameters.get('apply_last', False))

        result = apply_fn(
            obj_name,
            modifier_name,
            apply_last=apply_last,
        )

        if result.get('success', False):
            log_success(f"Modificador aplicado en '{obj_name}'")

        return {
            'success': result.get('success', False),
            'object_name': obj_name,
            'modifier_applied': result.get('modifier_applied'),
            'message': result.get('message', 'Modificador aplicado' if result.get('success') else result.get('error', 'Error')),
        }
    except Exception as e:
        log_warning(f"Error apply_modifier: {e}")
        return {'success': False, 'error': str(e)}


def add_boolean_modifier_handler(parameters: Dict[str, Any], adapter=None) -> Dict[str, Any]:
    """
    Agrega un modificador Boolean usando EngineAdapter.
    """
    if adapter is None:
        from core.adapters import get_engine_adapter
        adapter = get_engine_adapter()
    
    if not adapter or not adapter.is_available():
        return {'success': False, 'error': 'Engine adapter not available'}
    
    try:
        obj_name = parameters.get('object_name')
        operation = parameters.get('operation', 'DIFFERENCE')
        operand_object = parameters.get('operand_object')
        hide_operand = parameters.get('hide_operand', True)
        material_mode = parameters.get('material_mode')
        
        if not obj_name:
            return {'success': False, 'error': 'Missing object_name'}
        if not operand_object:
            return {'success': False, 'error': 'Missing operand_object'}
        
        mod_params = dict(
            operation=operation,
            operand_object=operand_object,
            hide_operand=hide_operand,
        )
        if material_mode:
            mod_params['material_mode'] = material_mode

        result = adapter.add_modifier(
            obj_name,
            'BOOLEAN',
            **mod_params,
        )
        
        if result.get('success', False):
            log_success(f"Boolean modifier ({operation}) agregado a '{obj_name}' con operando '{operand_object}'")
        
        return {
            'success': result.get('success', False),
            'object_name': obj_name,
            'operation': operation,
            'operand_object': operand_object,
            'message': 'Boolean modifier agregado' if result.get('success') else result.get('error', 'Error')
        }
    
    except Exception as e:
        log_warning(f"Error adding boolean modifier: {e}")
        return {'success': False, 'error': str(e)}
