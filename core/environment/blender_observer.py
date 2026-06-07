"""
Fase 5.15 – Observador Pasivo de Blender
FASE 17: Refactorizado para usar EngineAdapter

Regla absoluta:
- SOLO LEE
- NO MODIFICA
"""

from typing import Dict, List


class BlenderObserver:
    """
    Observador pasivo del estado de Blender.
    NO ejecuta acciones.
    NO altera la escena.
    
    FASE 17: Ahora usa EngineAdapter en lugar de bpy directo.
    """
    
    def __init__(self, adapter=None):
        """
        Inicializa el observador con un adapter.
        
        Args:
            adapter: EngineAdapter instance (si es None, se obtiene automáticamente)
        """
        self.adapter = adapter
        if self.adapter is None:
            from core.adapters import get_engine_adapter
            self.adapter = get_engine_adapter()

    def snapshot(self) -> Dict:
        """
        Captura un snapshot del estado actual de la escena.

        Retorna información básica:
        - Objetos
        - Tipo
        - Colección
        """
        if not self.adapter or not self.adapter.is_available():
            # Adapter no disponible (tests, entorno externo)
            return {
                "object_count": 0,
                "objects": [],
                "collections_hierarchy": [],
                "source": "no_engine"
            }
        
        try:
            # Obtener estado de la escena a través del adapter
            scene_state = self.adapter.get_scene_state()
            
            if not scene_state.get('success', False):
                return {
                    "object_count": 0,
                    "objects": [],
                    "collections_hierarchy": [],
                    "source": "error",
                    "error": scene_state.get('error', 'Unknown')
                }
            
            # Convertir al formato esperado
            objects_info = []
            for obj in scene_state.get('objects', []):
                objects_info.append({
                    "name": obj['name'],
                    "type": obj['type'],
                    "collections": [obj.get('collection', 'Scene Collection')]
                })
            
            snapshot = {
                "object_count": len(objects_info),
                "objects": objects_info,
                "collections_hierarchy": scene_state.get('collections', []),
                "source": "engine_adapter"
            }
            return snapshot
            
        except Exception as e:
            return {
                "object_count": 0,
                "objects": [],
                "collections_hierarchy": [],
                "source": "error",
                "error": str(e)
            }
