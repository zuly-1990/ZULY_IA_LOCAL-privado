"""
volatile_memory.py

FASE 18.5: Memoria Volátil
Al cerrar o cambiar escena:
- Limpiar referencias temporales
- Reiniciar punteros de objetos
- Sin "fantasmas" ni nombres heredados
"""

from typing import Dict, Any, Optional, Set
from core.utils.logging import log_info, log_debug, log_warning


class VolatileMemory:
    """
    Memoria volátil para referencias temporales de escena.
    
    Características:
    - Se limpia al cambiar escena
    - No persiste entre sesiones
    - Previene "fantasmas" de objetos eliminados
    """
    
    def __init__(self):
        self._object_references: Dict[str, Dict[str, Any]] = {}
        self._scene_id: Optional[str] = None
        self._collection_cache: Set[str] = set()
        self._active_object: Optional[str] = None
    
    def set_scene(self, scene_id: str):
        """
        Establece la escena actual.
        Si es diferente a la actual, limpia toda la memoria.
        
        Args:
            scene_id: Identificador de la escena
        """
        if self._scene_id != scene_id:
            if self._scene_id is not None:
                log_info(f"🔄 Scene changed: {self._scene_id} → {scene_id}")
                self.clear_all()
            self._scene_id = scene_id
            log_debug(f"📍 Scene set: {scene_id}")
    
    def clear_all(self):
        """Limpia TODA la memoria volátil."""
        old_count = len(self._object_references)
        
        self._object_references.clear()
        self._collection_cache.clear()
        self._active_object = None
        
        log_info(f"🧹 Volatile memory cleared ({old_count} references removed)")
    
    def register_object(self, name: str, data: Dict[str, Any]):
        """
        Registra un objeto en memoria volátil.
        
        Args:
            name: Nombre del objeto
            data: Datos del objeto (tipo, ubicación, etc.)
        """
        self._object_references[name] = {
            **data,
            '_registered_at': self._scene_id
        }
        log_debug(f"📝 Object registered: {name}")
    
    def unregister_object(self, name: str) -> bool:
        """
        Elimina un objeto de la memoria volátil.
        
        Args:
            name: Nombre del objeto
        
        Returns:
            True si se eliminó, False si no existía
        """
        if name in self._object_references:
            del self._object_references[name]
            log_debug(f"🗑️ Object unregistered: {name}")
            return True
        return False
    
    def get_object(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene datos de un objeto registrado.
        
        Args:
            name: Nombre del objeto
        
        Returns:
            Datos del objeto o None si no existe
        """
        return self._object_references.get(name)
    
    def object_exists(self, name: str) -> bool:
        """Verifica si un objeto está registrado."""
        return name in self._object_references
    
    def set_active_object(self, name: Optional[str]):
        """Establece el objeto activo."""
        if name is not None and name not in self._object_references:
            log_warning(f"⚠️ Setting active object '{name}' not in memory")
        self._active_object = name
    
    def get_active_object(self) -> Optional[str]:
        """Obtiene el nombre del objeto activo."""
        return self._active_object
    
    def get_all_objects(self) -> Dict[str, Dict[str, Any]]:
        """Obtiene todos los objetos registrados."""
        return dict(self._object_references)
    
    def get_object_count(self) -> int:
        """Obtiene el número de objetos registrados."""
        return len(self._object_references)
    
    def sync_with_scene(self, scene_objects: list):
        """
        Sincroniza la memoria con el estado real de la escena.
        Elimina referencias a objetos que ya no existen.
        
        Args:
            scene_objects: Lista de nombres de objetos en la escena
        """
        scene_set = set(scene_objects)
        memory_set = set(self._object_references.keys())
        
        # Objetos en memoria que ya no están en escena = fantasmas
        ghosts = memory_set - scene_set
        
        for ghost in ghosts:
            del self._object_references[ghost]
            log_warning(f"👻 Ghost removed: {ghost}")
        
        if ghosts:
            log_info(f"🧹 Removed {len(ghosts)} ghost references")
        
        # Actualizar objeto activo si fue eliminado
        if self._active_object and self._active_object not in scene_set:
            log_warning(f"⚠️ Active object '{self._active_object}' no longer exists")
            self._active_object = None
    
    def get_status(self) -> Dict[str, Any]:
        """Obtiene estado de la memoria volátil."""
        return {
            'scene_id': self._scene_id,
            'object_count': len(self._object_references),
            'collections_cached': len(self._collection_cache),
            'active_object': self._active_object,
            'objects': list(self._object_references.keys())
        }


# Singleton para uso global
_volatile_memory: Optional[VolatileMemory] = None


def get_volatile_memory() -> VolatileMemory:
    """Obtiene la instancia global de VolatileMemory."""
    global _volatile_memory
    if _volatile_memory is None:
        _volatile_memory = VolatileMemory()
    return _volatile_memory


def clear_volatile_memory():
    """Limpia la memoria volátil global."""
    get_volatile_memory().clear_all()
