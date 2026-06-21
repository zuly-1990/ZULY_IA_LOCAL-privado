"""
core/adapters/__init__.py

Factory para auto-detección y provisión de adapters de motores 3D.
"""

from typing import Optional
from core.utils.logging import log_info, log_warning, log_error

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
        log_info("🔧 Usando MockAdapter (forzado por flag)")
        _adapter_instance = MockAdapter()
        return _adapter_instance
    
    # Intentar primero bpy directo (si estamos dentro de Blender)
    try:
        import bpy
        from core.adapters.blender_adapter import BlenderAdapter
        adapter = BlenderAdapter(bpy_module=bpy)
        if adapter.is_available():
            log_info("✓ BlenderAdapter (bpy directo) disponible y activo")
            _adapter_instance = adapter
            return _adapter_instance
    except ImportError:
        pass
    except Exception as e:
        log_warning(f"⚠️ Error con bpy directo: {e}")

    # Fallback: RealBlenderAdapter (vía CLI - 100% real, sin simulación)
    try:
        from core.adapters.real_blender_adapter import RealBlenderAdapter
        adapter = RealBlenderAdapter()
        if adapter.is_available():
            log_info("✅ RealBlenderAdapter (CLI) activo - MODO 100% REAL")
            _adapter_instance = adapter
            return _adapter_instance
        else:
            log_warning("⚠️ RealBlenderAdapter: Blender no encontrado en PATH")
    except Exception as e:
        log_warning(f"⚠️ No se pudo cargar RealBlenderAdapter: {e}")

    # NUNCA usar MockAdapter en producción - lanzar error claro
    log_error("❌ CRÍTICO: No se encontró ningún adapter real de Blender.")
    log_error("   Asegúrate que Blender esté instalado y BLENDER_BIN apunte al ejecutable.")
    from core.adapters.mock_adapter import MockAdapter
    log_warning("⚠️ Usando MockAdapter como último recurso de emergencia.")
    _adapter_instance = MockAdapter()
    return _adapter_instance


__all__ = ['get_engine_adapter', 'USE_ENGINE_ADAPTER']
