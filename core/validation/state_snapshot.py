"""
core/validation/state_snapshot.py

Captura instantáneas del estado de la escena.
FASE 17: Refactorizado para usar EngineAdapter en lugar de bpy directo.
"""

from typing import Dict, Any, Optional
from core.utils.logging import log_error


class StateSnapshot:
    """
    Captura una instantánea del estado actual de la escena.
    Se utiliza para validar si los cambios esperados realmente ocurrieron.
    
    FASE 17: Ahora usa EngineAdapter en lugar de bpy directo.
    """
    
    def __init__(self, adapter=None):
        """
        Inicializa StateSnapshot con un adapter.
        
        Args:
            adapter: EngineAdapter instance (si es None, se obtiene automáticamente)
        """
        self.adapter = adapter
        if self.adapter is None:
            from core.adapters import get_engine_adapter
            self.adapter = get_engine_adapter()
    
    @staticmethod
    def capture(adapter=None) -> Dict[str, Any]:
        """
        Captura el estado actual de los objetos en la escena.
        
        Args:
            adapter: EngineAdapter instance (si es None, se obtiene automáticamente)
            
        Returns:
            Diccionario con la estructura {object_name: {type, location, collection}}
        """
        if adapter is None:
            from core.adapters import get_engine_adapter
            adapter = get_engine_adapter()
            
        if not adapter or not adapter.is_available():
            return {}
        
        try:
            # Obtener estado de la escena a través del adapter
            scene_state = adapter.get_scene_state()
            
            if not scene_state.get('success', False):
                log_error(f"Error obteniendo estado de escena: {scene_state.get('error', 'Unknown')}")
                return {}
            
            # Convertir al formato esperado
            snapshot = {}
            for obj in scene_state.get('objects', []):
                snapshot[obj['name']] = {
                    "type": obj['type'],
                    "location": tuple(round(v, 3) for v in obj['location']),
                    "rotation": tuple(round(v, 3) for v in obj.get('rotation', [0, 0, 0])),
                    "scale": tuple(round(v, 3) for v in obj.get('scale', [1, 1, 1])),
                    "collection": obj.get('collection', 'Scene Collection'),
                    "visible": obj.get('visible', True),
                    "parent": obj.get('parent'),
                    "vertex_count": obj.get('vertex_count', 0),
                    "name": obj['name']
                }
            
            return snapshot
            
        except Exception as e:
            log_error(f"Error capturando snapshot de estado: {e}")
            return {}
