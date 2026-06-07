"""
Archimesh Capability - Capacidad de Zuly para usar Archimesh add-on.
Registrada en el sistema de capabilities de Zuly.
"""

CAPABILITY_ID = "archimesh"
CAPABILITY_VERSION = "1.0.0"
CAPABILITY_DESCRIPTION = "Generación de elementos arquitectónicos con Archimesh"


def verificar():
    """
    Verifica si Archimesh está disponible en Blender.
    
    Returns:
        bool: True si archimesh está activo, False si no.
    """
    try:
        import bpy
        import addon_utils
        
        enabled, loaded = addon_utils.check("archimesh")
        if enabled:
            return True
            
        # Intentar activarlo
        try:
            addon_utils.enable("archimesh")
            enabled, _ = addon_utils.check("archimesh")
            return enabled
        except:
            return False
            
    except Exception as e:
        print(f"[ARCHIMESH_CAP] Error verificando: {e}")
        return False


def info():
    """Retorna información sobre la capacidad."""
    return {
        "id": CAPABILITY_ID,
        "version": CAPABILITY_VERSION,
        "description": CAPABILITY_DESCRIPTION,
        "available": verificar(),
        "elements": [
            "door", "window", "stairs", "column", "shelves", 
            "roof", "room", "kitchen", "fence"
        ]
    }
