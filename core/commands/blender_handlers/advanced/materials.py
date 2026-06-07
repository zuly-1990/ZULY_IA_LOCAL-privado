"""
materials.py - Handlers para materiales y texturas en Blender
FASE 17: Refactorizado para usar EngineAdapter.
"""

from typing import Dict, Any
from core.utils.logging import log_success, log_warning, log_info


def create_material_handler(parameters: Dict[str, Any], adapter=None) -> Dict[str, Any]:
    """
    Crea un material usando EngineAdapter.
    
    FASE 17: Ahora usa EngineAdapter en lugar de bpy directo.
    
    Parameters:
        parameters: Dict con:
            - name: str (nombre del material)
            - color: [r, g, b, a] (color RGBA)
            - metallic: float 0-1
            - roughness: float 0-1
        adapter: EngineAdapter instance
    """
    if adapter is None:
        from core.adapters import get_engine_adapter
        adapter = get_engine_adapter()
    
    if not adapter or not adapter.is_available():
        return {'success': False, 'error': 'Engine adapter not available'}
    
    try:
        name = parameters.get('name', 'Material_001')
        color = parameters.get('color', [1.0, 1.0, 1.0, 1.0])
        metallic = parameters.get('metallic', 0.0)
        roughness = parameters.get('roughness', 0.5)
        
        # Validar parámetros
        if not isinstance(name, str) or len(name) == 0:
            return {'success': False, 'error': 'Invalid material name'}
        
        if metallic < 0 or metallic > 1:
            return {'success': False, 'error': 'Metallic must be 0-1'}
        
        if roughness < 0 or roughness > 1:
            return {'success': False, 'error': 'Roughness must be 0-1'}
        
        # Crear material usando adapter
        result = adapter.create_material(
            name=name,
            color=color[:3] if len(color) >= 3 else color,
            metallic=metallic,
            roughness=roughness
        )
        
        if not result.get('success', False):
            return result
        
        log_success(f"Material '{name}' creado")
        
        return {
            'success': True,
            'material_name': result.get('material_name', name),
            'color': color,
            'metallic': metallic,
            'roughness': roughness,
            'message': f'Material {name} creado exitosamente'
        }
    
    except Exception as e:
        log_warning(f"Error creating material: {e}")
        return {'success': False, 'error': str(e)}


def apply_material_handler(parameters: Dict[str, Any], adapter=None) -> Dict[str, Any]:
    """
    Aplica un material a un objeto usando EngineAdapter.
    
    FASE 17: Ahora usa EngineAdapter en lugar de bpy directo.
    """
    if adapter is None:
        from core.adapters import get_engine_adapter
        adapter = get_engine_adapter()
    
    if not adapter or not adapter.is_available():
        return {'success': False, 'error': 'Engine adapter not available'}
    
    try:
        obj_name = parameters.get('object_name') or parameters.get('name')
        mat_name = parameters.get('material_name') or parameters.get('material')
        
        if not obj_name or not mat_name:
            return {
                'success': False, 
                'error': f"Missing object_name ({obj_name}) or material_name ({mat_name})",
                'debug_params': parameters
            }
        
        # Verificar si el material existe, si no, intentar crearlo si es un color conocido
        # Esto ayuda en pruebas de estrés como "Dale material de oro" sin haberlo creado antes.
        common_materials = {
            'oro': [0.8, 0.5, 0.0],
            'plata': [0.8, 0.8, 0.8],
            'cobre': [0.7, 0.3, 0.1],
            'vidrio': [0.9, 0.9, 1.0],
            'metal': [0.6, 0.6, 0.6],
            'madera': [0.4, 0.2, 0.1],
            'concreto': [0.5, 0.5, 0.5],
            'hojas': [0.1, 0.4, 0.1],
            'tronco': [0.3, 0.2, 0.1],
            'rojo': [1.0, 0.0, 0.0],
            'verde': [0.0, 1.0, 0.0],
            'azul': [0.0, 0.0, 1.0]
        }
        
        # Primero ver si el material existe
        scene_state = adapter.get_scene_state()
        # Nota: SceneMonitor/Adapter no listan materiales directamente en get_scene_state de forma fácil
        # pero adapter.apply_material fallará si no existe.
        
        result = adapter.apply_material(obj_name, mat_name)
        
        if not result.get('success', False) and result.get('error') == 'OBJECT_NOT_FOUND' and 'Material' in result.get('message', ''):
            # Si el error es que el MATERIAL no existe, intentamos crearlo
            mat_lower = mat_name.lower()
            if mat_lower in common_materials:
                log_info(f"Material '{mat_name}' no encontrado. Creándolo automáticamente...")
                create_res = adapter.create_material(name=mat_name, color=common_materials[mat_lower], metallic=0.9, roughness=0.1)
                if create_res.get('success', False):
                    result = adapter.apply_material(obj_name, mat_name)
        
        if result.get('success', False):
            log_success(f"Material '{mat_name}' aplicado a '{obj_name}'")
        
        return result
    
    except Exception as e:
        log_warning(f"Error applying material: {e}")
        return {'success': False, 'error': str(e)}


def set_material_color_handler(parameters: Dict[str, Any], adapter=None) -> Dict[str, Any]:
    """
    Cambia el color de un material usando EngineAdapter.
    
    FASE 17: Ahora usa EngineAdapter en lugar de bpy directo.
    """
    log_info(f"set_material_color_handler called with parameters: {parameters}")
    
    if adapter is None:
        from core.adapters import get_engine_adapter
        adapter = get_engine_adapter()
        log_info(f"Got adapter: {type(adapter).__name__}")
    else:
        log_info(f"Adapter passed: {type(adapter).__name__}")
    
    if not adapter or not adapter.is_available():
        return {'success': False, 'error': 'Engine adapter not available'}
    
    try:
        mat_name = parameters.get('material_name')
        color = parameters.get('color', [1.0, 1.0, 1.0, 1.0])
        
        if not mat_name:
            return {'success': False, 'error': 'Missing material_name'}
        
        log_info(f"Calling adapter.update_material({mat_name}, color={color})")
        result = adapter.update_material(mat_name, color=color)
        log_info(f"adapter.update_material returned: {result}")
        
        if result.get('success', False):
            log_success(f"Color del material '{mat_name}' actualizado")
        
        return result
    
    except Exception as e:
        log_warning(f"Error setting material color: {e}")
        return {'success': False, 'error': str(e)}


def create_texture_material_handler(parameters: Dict[str, Any], adapter=None) -> Dict[str, Any]:
    """
    Crea un material con textura de imagen usando EngineAdapter.
    
    Parameters:
        parameters: Dict con:
            - name: str (nombre del material)
            - image_path: str (ruta absoluta a la imagen)
            - metallic: float 0-1
            - roughness: float 0-1
        adapter: EngineAdapter instance
    """
    if adapter is None:
        from core.adapters import get_engine_adapter
        adapter = get_engine_adapter()
    
    if not adapter or not adapter.is_available():
        return {'success': False, 'error': 'Engine adapter not available'}
    
    try:
        name = parameters.get('name', 'TextureMaterial')
        image_path = parameters.get('image_path')
        metallic = parameters.get('metallic', 0.0)
        roughness = parameters.get('roughness', 0.5)
        
        if not image_path:
            return {'success': False, 'error': 'Missing image_path'}
        
        # El adapter debe soportar create_texture_material
        if hasattr(adapter, 'create_texture_material'):
            result = adapter.create_texture_material(
                name=name,
                image_path=image_path,
                metallic=metallic,
                roughness=roughness
            )
        else:
            return {'success': False, 'error': 'Adapter does not support texture materials'}
        
        if result.get('success', False):
            log_success(f"Material de textura '{name}' creado con '{image_path}'")
        
        return result
    
    except Exception as e:
        log_warning(f"Error creating texture material: {e}")
        return {'success': False, 'error': str(e)}
