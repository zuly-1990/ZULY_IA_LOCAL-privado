"""
visual_confirmation.py

FASE 18.5: Confirmación Visual
Antes de cualquier operación, listar:
- Objeto
- Tipo
- Ubicación
- Colección

Regla: Si no puede describir → no tocar.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from core.utils.logging import log_info, log_warning


@dataclass
class ObjectDescription:
    """Descripción visual de un objeto."""
    name: str
    type: str
    location: List[float]
    collection: str
    scale: List[float]
    visible: bool
    custom_props: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'type': self.type,
            'location': self.location,
            'collection': self.collection,
            'scale': self.scale,
            'visible': self.visible,
            'custom_props': self.custom_props
        }
    
    def describe(self) -> str:
        """Genera descripción legible."""
        loc_str = f"({self.location[0]:.2f}, {self.location[1]:.2f}, {self.location[2]:.2f})"
        return f"{self.name} [{self.type}] @ {loc_str} in {self.collection}"


class VisualConfirmation:
    """
    Sistema de confirmación visual antes de operaciones.
    
    REGLA: Si no puede describir un objeto, no lo toca.
    """
    
    def __init__(self, adapter=None):
        self._adapter = adapter
    
    def _get_adapter(self):
        """Obtiene adapter si no está configurado."""
        if self._adapter is None:
            try:
                from core.adapters import get_engine_adapter
                self._adapter = get_engine_adapter()
            except Exception:
                pass
        return self._adapter
    
    def describe_object(self, object_name: str) -> Optional[ObjectDescription]:
        """
        Obtiene descripción detallada de un objeto.
        
        Args:
            object_name: Nombre del objeto
        
        Returns:
            ObjectDescription o None si no puede describir
        """
        adapter = self._get_adapter()
        if not adapter or not adapter.is_available():
            log_warning("Cannot describe object - adapter not available")
            return None
        
        try:
            # Obtener información del objeto
            obj_info = adapter.get_object(object_name)
            
            if not obj_info.get('success', False):
                log_warning(f"Cannot describe '{object_name}' - not found")
                return None
            
            return ObjectDescription(
                name=obj_info.get('name', object_name),
                type=obj_info.get('type', 'UNKNOWN'),
                location=obj_info.get('location', [0, 0, 0]),
                collection=obj_info.get('collection', 'Scene Collection'),
                scale=obj_info.get('scale', [1, 1, 1]),
                visible=obj_info.get('visible', True),
                custom_props=obj_info.get('custom_properties', {})
            )
        
        except Exception as e:
            log_warning(f"Error describing object '{object_name}': {e}")
            return None
    
    def describe_all_objects(self) -> List[ObjectDescription]:
        """
        Obtiene descripción de todos los objetos en la escena.
        
        Returns:
            Lista de ObjectDescription
        """
        adapter = self._get_adapter()
        if not adapter or not adapter.is_available():
            return []
        
        try:
            scene_state = adapter.get_scene_state()
            objects = scene_state.get('objects', [])
            
            descriptions = []
            for obj in objects:
                descriptions.append(ObjectDescription(
                    name=obj.get('name', 'unknown'),
                    type=obj.get('type', 'UNKNOWN'),
                    location=obj.get('location', [0, 0, 0]),
                    collection=obj.get('collection', 'Scene Collection'),
                    scale=obj.get('scale', [1, 1, 1]),
                    visible=obj.get('visible', True),
                    custom_props=obj.get('custom_properties', {})
                ))
            
            return descriptions
        
        except Exception as e:
            log_warning(f"Error describing scene: {e}")
            return []
    
    def can_operate_on(self, object_name: str) -> bool:
        """
        Verifica si se puede operar sobre un objeto.
        
        REGLA: Solo si puede describirlo completamente.
        
        Args:
            object_name: Nombre del objeto
        
        Returns:
            True si puede operar, False si no
        """
        description = self.describe_object(object_name)
        
        if description is None:
            log_warning(f"❌ Cannot operate on '{object_name}' - cannot describe")
            return False
        
        log_info(f"✓ Can operate on: {description.describe()}")
        return True
    
    def confirm_before_action(
        self,
        action: str,
        target_name: str
    ) -> Dict[str, Any]:
        """
        Genera confirmación visual antes de una acción.
        
        Args:
            action: Acción a realizar
            target_name: Nombre del objeto objetivo
        
        Returns:
            Dict con confirmación o rechazo
        """
        description = self.describe_object(target_name)
        
        if description is None:
            return {
                'can_proceed': False,
                'reason': f"Cannot describe target '{target_name}'",
                'action': action,
                'target': None
            }
        
        return {
            'can_proceed': True,
            'action': action,
            'target': description.to_dict(),
            'confirmation': f"Will {action} on {description.describe()}"
        }
    
    def list_scene_objects(self) -> str:
        """
        Lista todos los objetos de la escena en formato legible.
        
        Returns:
            String con lista de objetos
        """
        descriptions = self.describe_all_objects()
        
        if not descriptions:
            return "No objects in scene (or cannot access)"
        
        lines = ["Scene Objects:"]
        for i, desc in enumerate(descriptions, 1):
            lines.append(f"  {i}. {desc.describe()}")
        
        return "\n".join(lines)


# Singleton
_visual_confirmation: Optional[VisualConfirmation] = None


def get_visual_confirmation() -> VisualConfirmation:
    """Obtiene la instancia global de VisualConfirmation."""
    global _visual_confirmation
    if _visual_confirmation is None:
        _visual_confirmation = VisualConfirmation()
    return _visual_confirmation


def can_operate_on(object_name: str) -> bool:
    """Helper para verificar si se puede operar sobre un objeto."""
    return get_visual_confirmation().can_operate_on(object_name)
