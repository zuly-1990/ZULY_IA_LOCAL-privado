"""
Handler para limpiar la escena de Blender.
"""
from typing import Dict, Any

def clear_scene_handler(parameters: Dict[str, Any], adapter=None) -> Dict[str, Any]:
    """
    Handler para blender.clear_scene.
    Borra todos los objetos de la escena.
    """
    if not adapter:
        return {'success': False, 'error': 'No adapter provided'}
        
    return adapter.clear_scene()

def rename_object_handler(parameters: Dict[str, Any], adapter=None) -> Dict[str, Any]:
    """
    Handler para blender.rename_object.
    Renombra un objeto existente.
    """
    if not adapter:
        return {'success': False, 'error': 'No adapter provided'}
        
    # Extraer parámetros (name/object_name es el antiguo, new_name es el nuevo)
    # NLU pone el primer nombre citado en 'name' o 'object_name'
    # Si la petición es "Rename 'A' to 'B'", NLU necesita ser inteligente.
    # POR AHORA: Si hay un 'name' y un 'new_name', los usamos.
    # Si no, intentamos deducir de 'parameters'.
    
    old_name = parameters.get('old_name') or parameters.get('name') or parameters.get('object_name')
    new_name = parameters.get('new_name')
    
    # Mejora NLU temporal si no detectó new_name (Case 15 soporte)
    if not new_name and 'name' in parameters:
        # Si NLU no separó old/new, puede que estén mezclados o falte uno
        # En el stress test Case 15: "Rename 'Cubo_Test' to 'Cubo_Final'"
        # Nuestro NLU extraer parámetros básicos.
        pass

    if not old_name or not new_name:
        return {
            'success': False, 
            'error': 'Missing parameters for rename. Need old name and new name.',
            'hint': "Example: Rename 'Old' to 'New'"
        }
        
    result = adapter.rename_object(old_name, new_name)
    if result.get('success'):
        result['effect'] = 'property' # Rename es un cambio de propiedad
    return result

def set_object_visibility_handler(parameters: Dict[str, Any], adapter=None) -> Dict[str, Any]:
    """
    Handler para blender.set_object_visibility.
    Oculta o muestra un objeto.
    """
    if not adapter:
        return {'success': False, 'error': 'No adapter provided'}
        
    object_name = parameters.get('name') or parameters.get('object_name')
    visible = parameters.get('visible', True)
    
    if not object_name:
        return {'success': False, 'error': 'Missing object_name'}
        
    result = adapter.set_object_visibility(object_name, visible)
    if result.get('success'):
        result['effect'] = 'property'
    return result

def set_parent_handler(parameters: Dict[str, Any], adapter=None) -> Dict[str, Any]:
    """
    Handler para blender.set_parent.
    Establece la jerarquía entre dos objetos.
    """
    if not adapter:
        return {'success': False, 'error': 'No adapter provided'}
        
    child_name = parameters.get('child') or parameters.get('name') or parameters.get('object_name')
    parent_name = parameters.get('parent')
    
    if not child_name:
        return {'success': False, 'error': 'Missing child name'}
        
    result = adapter.set_parent(child_name, parent_name)
    if result.get('success'):
        result['effect'] = 'hierarchy' # Cambio de jerarquía
    return result
