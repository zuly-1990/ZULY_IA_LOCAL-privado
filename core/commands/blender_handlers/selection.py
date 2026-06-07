"""
selection.py

Handlers para selección, deselección, eliminación y duplicación de objetos.
FASE ULTRA EMERGENCIA: Reescritos con EngineAdapter pattern.
"""

from typing import Dict, Any
from core.utils.logging import log_success, log_warning


def delete_object_handler(parameters: Dict[str, Any], adapter=None) -> Dict[str, Any]:
    """
    Elimina un objeto de la escena.
    
    Parameters:
        parameters: Dict con:
            - name / object_name: str - Nombre del objeto a eliminar
        adapter: EngineAdapter instance
    
    Returns:
        Dict con status y resultado
    """
    if adapter is None:
        from core.adapters import get_engine_adapter
        adapter = get_engine_adapter()
    
    if not adapter or not adapter.is_available():
        return {'success': False, 'error': 'Engine adapter not available'}
    
    try:
        object_name = parameters.get('name') or parameters.get('object_name')
        
        if not object_name:
            return {'success': False, 'error': 'Missing object name to delete'}
        
        # Verificar que el objeto existe antes de intentar eliminarlo
        obj_info = adapter.get_object_info(object_name)
        if not obj_info.get('success', False):
            return {
                'success': False,
                'error': f"Object '{object_name}' not found in scene"
            }
        
        # Eliminar via adapter
        result = adapter.delete_object(object_name)
        
        if result.get('success', False):
            result['effect'] = 'delete'
            result['result'] = {'name': object_name}
            log_success(f"Objeto '{object_name}' eliminado")
        
        return result
    
    except Exception as e:
        log_warning(f"Error deleting object: {e}")
        return {'success': False, 'error': str(e)}


def duplicate_object_handler(parameters: Dict[str, Any], adapter=None) -> Dict[str, Any]:
    """
    Duplica un objeto en la escena.
    
    Parameters:
        parameters: Dict con:
            - name / object_name: str - Nombre del objeto a duplicar
            - new_name: str (opcional) - Nombre del duplicado
        adapter: EngineAdapter instance
    
    Returns:
        Dict con status y resultado
    """
    if adapter is None:
        from core.adapters import get_engine_adapter
        adapter = get_engine_adapter()
    
    if not adapter or not adapter.is_available():
        return {'success': False, 'error': 'Engine adapter not available'}
    
    try:
        object_name = parameters.get('name') or parameters.get('object_name')
        new_name = parameters.get('new_name')
        
        if not object_name:
            return {'success': False, 'error': 'Missing object name to duplicate'}
        
        result = adapter.duplicate_object(object_name, new_name=new_name)
        
        if result.get('success', False):
            result['effect'] = 'create'
            log_success(f"Objeto '{object_name}' duplicado")
        
        return result
    
    except Exception as e:
        log_warning(f"Error duplicating object: {e}")
        return {'success': False, 'error': str(e)}


def select_object_handler(parameters: Dict[str, Any], adapter=None) -> Dict[str, Any]:
    """
    Selecciona un objeto por nombre.
    
    Parameters:
        parameters: Dict con:
            - name / object_name: str - Nombre del objeto a seleccionar
        adapter: EngineAdapter instance
    
    Returns:
        Dict con status y resultado
    """
    if adapter is None:
        from core.adapters import get_engine_adapter
        adapter = get_engine_adapter()
    
    if not adapter or not adapter.is_available():
        return {'success': False, 'error': 'Engine adapter not available'}
    
    try:
        object_name = parameters.get('name') or parameters.get('object_name')
        
        if not object_name:
            return {'success': False, 'error': 'Missing object name to select'}
        
        result = adapter.select_object(object_name)
        
        if result.get('success', False):
            log_success(f"Objeto '{object_name}' seleccionado")
        
        return result
    
    except Exception as e:
        log_warning(f"Error selecting object: {e}")
        return {'success': False, 'error': str(e)}


def deselect_all_handler(parameters: Dict[str, Any], adapter=None) -> Dict[str, Any]:
    """
    Deselecciona todos los objetos.
    
    Parameters:
        parameters: Dict (no requiere parámetros específicos)
        adapter: EngineAdapter instance
    
    Returns:
        Dict con status y resultado
    """
    if adapter is None:
        from core.adapters import get_engine_adapter
        adapter = get_engine_adapter()
    
    if not adapter or not adapter.is_available():
        return {'success': False, 'error': 'Engine adapter not available'}
    
    try:
        result = adapter.deselect_all()
        
        if result.get('success', False):
            log_success("Todos los objetos deseleccionados")
        
        return result
    
    except Exception as e:
        log_warning(f"Error deselecting: {e}")
        return {'success': False, 'error': str(e)}


def select_all_by_type_handler(parameters: Dict[str, Any], adapter=None) -> Dict[str, Any]:
    """
    Selecciona todos los objetos de un tipo específico.
    
    Parameters:
        parameters: Dict con:
            - type / object_type: str - Tipo de objeto (MESH, LIGHT, CAMERA, etc.)
        adapter: EngineAdapter instance
    
    Returns:
        Dict con status y resultado
    """
    if adapter is None:
        from core.adapters import get_engine_adapter
        adapter = get_engine_adapter()
    
    if not adapter or not adapter.is_available():
        return {'success': False, 'error': 'Engine adapter not available'}
    
    try:
        obj_type = parameters.get('type') or parameters.get('object_type', 'MESH')
        
        result = adapter.select_all_by_type(obj_type)
        
        if result.get('success', False):
            log_success(f"Seleccionados todos los objetos tipo '{obj_type}'")
        
        return result
    
    except Exception as e:
        log_warning(f"Error selecting by type: {e}")
        return {'success': False, 'error': str(e)}
