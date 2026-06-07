"""
pattern_to_handler_mapper.py

Mapeo centralizado: patrón → handler real

Conecta el índice de patrones con los handlers ejecutables en blender_handlers/

FLUJO:
    decision_engine.decidir()
        ↓ (patron name)
    pattern_to_handler_mapper.get_handler()
        ↓ (handler callable)
    execute_handler()
        ↓
    resultado
"""

from typing import Optional, Dict, Any, Callable
from core.utils.logging import log_info, log_warning, log_error, log_debug

# Mapeo: patrón_name → (handler_module, handler_function)
PATTERN_HANDLER_MAP = {
    # Primitivas básicas
    "crear_cubo": ("core.commands.blender_handlers.primitives", "create_cube_handler"),
    "crear_esfera": ("core.commands.blender_handlers.primitives", "create_sphere_handler"),
    "crear_cilindro": ("core.commands.blender_handlers.primitives", "create_cylinder_handler"),
    "crear_plano": ("core.commands.blender_handlers.primitives", "create_plane_handler"),
    "crear_cono": ("core.commands.blender_handlers.primitives", "create_cone_handler"),
    
    # Transformaciones
    "mover_objeto": ("core.commands.blender_handlers.transforms", "move_object_handler"),
    "rotar_objeto": ("core.commands.blender_handlers.transforms", "rotate_object_handler"),
    "escalar_objeto": ("core.commands.blender_handlers.transforms", "scale_object_handler"),
    
    # Selección
    "eliminar_objeto": ("core.commands.blender_handlers.selection", "delete_object_handler"),
    "duplicar_objeto": ("core.commands.blender_handlers.selection", "duplicate_object_handler"),
    "seleccionar_objeto": ("core.commands.blender_handlers.selection", "select_object_handler"),
    "deseleccionar_todo": ("core.commands.blender_handlers.selection", "deselect_all_handler"),
    "seleccionar_por_tipo": ("core.commands.blender_handlers.selection", "select_all_by_type_handler"),
    
    # Escena
    "limpiar_escena": ("core.commands.blender_handlers.scene", "clear_scene_handler"),
    "renombrar_objeto": ("core.commands.blender_handlers.scene", "rename_object_handler"),
    "visibilidad_objeto": ("core.commands.blender_handlers.scene", "set_object_visibility_handler"),
    "establecer_padre": ("core.commands.blender_handlers.scene", "set_parent_handler"),
    
    # Render
    "renderizar": ("core.commands.blender_handlers.render", "render_scene_handler"),
    "renderizar_escena": ("core.commands.blender_handlers.render", "render_scene_handler"),
    
    # Sistema
    "info_sistema": ("core.commands.blender_handlers.system", "get_system_info_handler"),
    "guardar_blend": ("core.commands.blender_handlers.system", "save_blend_handler"),
    
    # Assembly (Patrones)
    "construir_estructura": ("core.commands.blender_handlers.assembly", "build_structure_handler"),
    "guardar_patron": ("core.commands.blender_handlers.assembly", "save_pattern_handler"),
    "cargar_patron": ("core.commands.blender_handlers.assembly", "load_pattern_handler"),
    "listar_patrones": ("core.commands.blender_handlers.assembly", "list_patterns_handler"),
}

# Cache para handlers cargados (evita re-importar)
_handler_cache: Dict[str, Callable] = {}


def get_handler(pattern_name: str) -> Optional[Callable]:
    """
    Obtiene el handler callable para un patrón.
    
    Args:
        pattern_name: Nombre del patrón (ej: "crear_cubo")
        
    Returns:
        Callable handler o None si no existe
        
    Examples:
        >>> handler = get_handler("crear_cubo")
        >>> result = handler({"location": [0, 0, 0]}, adapter)
    """
    pattern_name_lower = pattern_name.lower()
    
    # Verificar cache primero
    if pattern_name_lower in _handler_cache:
        return _handler_cache[pattern_name_lower]
    
    # Buscar en mapa
    if pattern_name_lower not in PATTERN_HANDLER_MAP:
        log_warning(f"Patrón no mapeado: {pattern_name}")
        return None
    
    module_name, func_name = PATTERN_HANDLER_MAP[pattern_name_lower]
    
    try:
        # Importar módulo dinámicamente
        module = __import__(module_name, fromlist=[func_name])
        
        # Obtener función
        if not hasattr(module, func_name):
            log_error(f"Handler '{func_name}' no encontrado en {module_name}")
            return None
        
        handler = getattr(module, func_name)
        
        # Guardar en cache
        _handler_cache[pattern_name_lower] = handler
        
        log_debug(f"✓ Handler cargado en cache: {pattern_name} → {func_name}")
        return handler
        
    except ImportError as e:
        log_error(f"Error importando {module_name}: {e}")
        return None
    except Exception as e:
        log_error(f"Error obteniendo handler '{func_name}': {e}")
        return None


def execute_handler(
    pattern_name: str,
    parameters: Dict[str, Any],
    adapter=None
) -> Dict[str, Any]:
    """
    Ejecuta un handler para un patrón.
    
    Esta es la interfaz principal que decision_engine usa.
    
    Args:
        pattern_name: Nombre del patrón
        parameters: Parámetros para el handler
        adapter: EngineAdapter (Blender, Mock, etc)
        
    Returns:
        Resultado de la ejecución del handler
        
    Examples:
        >>> result = execute_handler("crear_cubo", {"location": [0, 0, 0]}, adapter)
        >>> if result["success"]:
        ...     print(f"Cubo creado: {result['object_name']}")
    """
    log_info(f"▶ Ejecutando handler para patrón: {pattern_name}")
    
    # Obtener handler
    handler = get_handler(pattern_name)
    if not handler:
        return {
            'success': False,
            'error': f"Handler no encontrado para patrón '{pattern_name}'",
            'pattern': pattern_name,
            'route': 'PATTERN_MAPPER_NOT_FOUND'
        }
    
    try:
        # Ejecutar handler
        result = handler(parameters, adapter)
        
        # Agregar metadata de routing
        result['route'] = 'PATTERN_MAPPER'
        result['pattern_used'] = pattern_name
        
        if result.get('success'):
            log_info(f"✓ Handler ejecutado exitosamente: {pattern_name}")
        else:
            log_warning(f"✗ Handler falló: {result.get('error')}")
        
        return result
        
    except Exception as e:
        log_error(f"Excepción ejecutando handler '{pattern_name}': {e}")
        return {
            'success': False,
            'error': f"Excepción: {str(e)}",
            'pattern': pattern_name,
            'route': 'PATTERN_MAPPER_EXCEPTION'
        }


def get_available_patterns() -> list:
    """Lista todos los patrones disponibles."""
    return list(PATTERN_HANDLER_MAP.keys())


def is_pattern_available(pattern_name: str) -> bool:
    """Verifica si un patrón está mapeado."""
    return pattern_name.lower() in PATTERN_HANDLER_MAP


def get_pattern_handler_info(pattern_name: str) -> Optional[Dict[str, str]]:
    """Obtiene información sobre el mapeo de un patrón."""
    pattern_name_lower = pattern_name.lower()
    if pattern_name_lower not in PATTERN_HANDLER_MAP:
        return None
    
    module, func = PATTERN_HANDLER_MAP[pattern_name_lower]
    return {
        "pattern": pattern_name_lower,
        "module": module,
        "function": func
    }


def clear_handler_cache():
    """Limpia el cache de handlers (útil después de recargas)."""
    global _handler_cache
    _handler_cache.clear()
    log_info("✓ Handler cache limpiado")


if __name__ == "__main__":
    # Demo
    print("\n" + "="*70)
    print("🔧 PATTERN TO HANDLER MAPPER — Demo")
    print("="*70 + "\n")
    
    print("📋 Patrones disponibles:")
    patterns = get_available_patterns()
    for i, p in enumerate(patterns, 1):
        info = get_pattern_handler_info(p)
        print(f"  {i:2d}. {p:25s} → {info['function']}")
    
    print(f"\n✓ Total: {len(patterns)} patrones mapeados")
    
    print("\n" + "="*70)
    print("🧪 Test: Verificación de mapeo")
    print("="*70 + "\n")
    
    test_patterns = ["crear_cubo", "mover_objeto", "renderizar", "nonexistent"]
    
    for pattern in test_patterns:
        available = is_pattern_available(pattern)
        info = get_pattern_handler_info(pattern)
        
        print(f"Patrón: {pattern}")
        print(f"  Disponible: {available}")
        if info:
            print(f"  Handler: {info['function']}")
        print()
