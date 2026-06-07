"""
Observador de Acciones Humanas en Blender (Fase 5.16)

Responsabilidad ÚNICA:
Comparar dos estados (snapshots) y detectar diferencias.
Traducir diferencias a eventos: CREATE, DELETE, MODIFY.

Reglas:
- NO ejecuta acciones en Blender.
- NO modifica nada.
- Solo compara diccionarios.
"""

from typing import Dict, List, Any
from datetime import datetime

class BlenderActionObserver:
    """
    Detecta acciones humanas comparando snapshots consecutivos.
    """
    
    def detect_changes(self, snapshot_before: Dict[str, Any], snapshot_after: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Compara el estado 'antes' con 'después' para identificar acciones.
        """
        events = []
        timestamp = datetime.now().isoformat()
        
        # Validar estructura básica
        if not self._is_valid_snapshot(snapshot_before) or not self._is_valid_snapshot(snapshot_after):
            return [] # No se puede comparar si falta data
            
        objects_before = {obj["name"]: obj for obj in snapshot_before.get("objects", [])}
        objects_after = {obj["name"]: obj for obj in snapshot_after.get("objects", [])}
        
        # 1. Detectar CREACIÓN (En after, no en before)
        for name, obj in objects_after.items():
            if name not in objects_before:
                events.append({
                    "event": "HUMAN_ACTION",
                    "type": "CREATE",
                    "object": name,
                    "timestamp": timestamp,
                    "validated_by_v0": True
                })
        
        # 2. Detectar BORRADO (En before, no en after)
        for name, obj in objects_before.items():
            if name not in objects_after:
                events.append({
                    "event": "HUMAN_ACTION",
                    "type": "DELETE",
                    "object": name,
                    "timestamp": timestamp,
                    "validated_by_v0": True
                })
                
        # 3. Detectar MODIFICACIÓN (En ambos, propiedades distintas)
        for name, obj_after in objects_after.items():
            if name in objects_before:
                obj_before = objects_before[name]
                if self._has_changed(obj_before, obj_after):
                    events.append({
                        "event": "HUMAN_ACTION",
                        "type": "MODIFY",
                        "object": name,
                        "timestamp": timestamp,
                        "validated_by_v0": True
                    })
                    
        return events

    def _is_valid_snapshot(self, snapshot: Dict) -> bool:
        """Valida que el snapshot tenga la estructura mínima necesaria (lista de objects)."""
        return isinstance(snapshot, dict) and "objects" in snapshot and isinstance(snapshot["objects"], list)

    def _has_changed(self, obj_a: Dict, obj_b: Dict) -> bool:
        """Determina si hubo cambios significativos (Posición, Rotación, Escala)."""
        # Comparación simple de propiedades clave.
        # Asumimos que snapshot guarda location/rotation/scale como tuplas/listas/dicts.
        
        # Location
        if obj_a.get("location") != obj_b.get("location"):
            return True
            
        # Rotation
        if obj_a.get("rotation") != obj_b.get("rotation"):
            return True
            
        # Scale
        if obj_a.get("dimensions") != obj_b.get("dimensions"): # Usamos dimensions o scale
             return True

        return False
