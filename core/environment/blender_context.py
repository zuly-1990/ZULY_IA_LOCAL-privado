"""
Fase A: Contexto de Blender
FASE 17: Refactorizado para usar EngineAdapter

Provee información sobre el entorno de ejecución de Blender.
"""

import sys
from typing import Dict, Any


def get_blender_context(adapter=None) -> Dict[str, Any]:
    """
    Obtiene el contexto actual del entorno Blender.
    Retorna un diccionario seguro incluso si no se está ejecutando en Blender.
    
    FASE 17: Ahora usa EngineAdapter en lugar de bpy directo.
    
    Args:
        adapter: EngineAdapter instance (si es None, se obtiene automáticamente)
    """
    context = {
        "is_blender": False,
        "executable": sys.executable,  # Ruta al python/blender actual
        "active_file": None,
        "active_scene": None,
        "mode": "unknown",
        "version": None
    }
    
    # Obtener adapter si no se proporciona
    if adapter is None:
        from core.adapters import get_engine_adapter
        adapter = get_engine_adapter()
    
    # Verificar disponibilidad del motor
    if not adapter or not adapter.is_available():
        context["mode"] = "external_script"
        context["active_file"] = "N/A"
        context["active_scene"] = "N/A"
        return context
    
    try:
        # Obtener información del motor
        engine_info = adapter.get_engine_info()
        
        if engine_info.get('success', False):
            context["is_blender"] = True
            context["version"] = engine_info.get('version_string', engine_info.get('version', 'Unknown'))
            
            # Determinar modo real desde el adapter (Fase 17+)
            context["mode"] = engine_info.get("active_mode", "OBJECT")
            if engine_info.get("is_background"):
                 # Si estamos en background, el modo contextual para ZULY es OBJECT
                 # (Para evitar bloqueos de V2 que espera interacción humana en modo GUI)
                 context["mode"] = "OBJECT"
            
            # Obtener estado de la escena
            scene_state = adapter.get_scene_state()
            if scene_state.get('success', False):
                # Modo granular desde la escena si está disponible
                context["mode"] = scene_state.get("active_mode", context["mode"])
                
                # Archivo activo (vía bpy si está disponible)
                try:
                    import bpy
                    context["active_file"] = bpy.data.filepath or "New Project"
                except:
                    context["active_file"] = "Memory (Unsaved)"
                
                context["active_scene"] = "Scene"
        else:
            context["mode"] = "error"
            context["error"] = engine_info.get('error', 'Unknown error')
            
    except Exception as e:
        context["error"] = str(e)
        context["mode"] = "error"
    
    return context
