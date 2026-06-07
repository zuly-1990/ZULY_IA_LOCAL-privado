"""
core/adapters/__init__.py

Factory para auto-detección y provisión de adapters de motores 3D.
"""

from typing import Optional
from core.utils.logging import log_info, log_warning

# Feature flag de emergencia (Ajuste 4)
USE_ENGINE_ADAPTER = True


_adapter_instance = None

def get_engine_adapter(force_mock: bool = False):
    """
    Auto-detecta y retorna el adapter apropiado. (Patrón Singleton)
    
    Args:
        force_mock: Si True, fuerza el uso de MockAdapter (útil para tests)
    
    Returns:
        EngineAdapter: Instancia del adapter apropiado
    """
    global _adapter_instance
    
    if not USE_ENGINE_ADAPTER:
        log_warning("⚠️ USE_ENGINE_ADAPTER=False, usando comportamiento legacy")
        return None
    
    # Si ya hay una instancia y no estamos forzando un cambio radical, retornarla
    if _adapter_instance is not None and not force_mock:
        return _adapter_instance
    
    if force_mock:
        from core.adapters.mock_adapter import MockAdapter
        log_info("🔧 Usando MockAdapter (forzado)")
        _adapter_instance = MockAdapter()
        return _adapter_instance
    
    # Intentar cargar BlenderAdapter
    try:
        from core.adapters.blender_adapter import BlenderAdapter
        adapter = BlenderAdapter()
        if adapter.is_available():
            log_info("✓ BlenderAdapter disponible y activo")
            _adapter_instance = adapter
            return _adapter_instance
        else:
            log_warning("⚠️ BlenderAdapter no disponible (bpy no encontrado)")
    except ImportError as e:
        log_warning(f"⚠️ No se pudo importar BlenderAdapter: {e}")
    
    # Fallback a MockAdapter
    from core.adapters.mock_adapter import MockAdapter
    log_info("🔧 Usando MockAdapter (fallback)")
    _adapter_instance = MockAdapter()
    return _adapter_instance


__all__ = ['get_engine_adapter', 'USE_ENGINE_ADAPTER']
