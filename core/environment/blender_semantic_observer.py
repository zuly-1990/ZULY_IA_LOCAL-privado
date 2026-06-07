"""
Fase 5.16 – Observador Semántico Pasivo

Regla absoluta:
- SOLO INTERPRETA DATOS
- NO MODIFICA NADA
- NO EJECUTA OPERADORES
"""

from typing import Dict, List, Set


class BlenderSemanticObserver:
    """
    Analizador semántico puro.
    Toma un snapshot crudo (dict) y devuelve interpretación semántica.
    """

    def analyze(self, snapshot: Dict) -> Dict:
        """
        Analiza un snapshot de BlenderObserver.
        Entrada: Dict (snapshot crudo del observer)
        Salida: Dict (interpretación semántica enriquecida)
        """
        if not snapshot or snapshot.get("source") == "no_blender" or not snapshot.get("objects"):
            return {
                "scene_type": "EMPTY_SCENE",
                "object_summary": {},
                "semantic_tags": {},
                "confidence": 1.0
            }

        objects = snapshot.get("objects", [])
        type_counts: Dict[str, int] = {}
        semantic_tags: Dict[str, str] = {}
        
        for obj in objects:
            name = obj.get("name", "Unknown")
            obj_type = obj.get("type", "UNKNOWN")
            type_counts[obj_type] = type_counts.get(obj_type, 0) + 1
            
            # Inferencia de Rol Arquitectónico (ASM)
            role = self._infer_role(obj)
            if role:
                semantic_tags[name] = role

        # Inferencia de Tipo de Escena
        num_mesh = type_counts.get("MESH", 0)
        num_camera = type_counts.get("CAMERA", 0)
        
        roles_detected = list(set(semantic_tags.values()))
        if "MURO" in roles_detected or "SUELO" in roles_detected:
            scene_type = "ARCHITECTURAL_STRUCTURE"
            confidence = 0.95
        elif num_mesh > 0:
            scene_type = "BASIC_MODELING"
            confidence = 0.8
        else:
            scene_type = "COMPLEX_OR_UNKNOWN"
            confidence = 0.5

        return {
            "scene_type": scene_type,
            "object_summary": type_counts,
            "semantic_tags": semantic_tags,
            "roles_detected": roles_detected,
            "confidence": confidence
        }

    def _infer_role(self, obj: Dict) -> str:
        """
        Infiere el rol arquitectónico basado en dimensiones, nombre y posición.
        """
        if obj.get("type") != "MESH":
            return None
            
        name = obj.get("name", "").upper()
        dims = obj.get("dimensions", [0, 0, 0])
        loc = obj.get("location", [0, 0, 0])
        
        dx, dy, dz = dims
        zx, zy, zz = loc
        
        # 1. SUELO (Horizontal, bajo, a nivel de piso)
        if dz < 0.4 and dx > 1.5 and dy > 1.5 and zz < 0.5:
            return "SUELO"
            
        # 2. TECHO (Horizontal, bajo, elevado)
        if dz < 0.4 and dx > 1.5 and dy > 1.5 and zz > 2.0:
            return "TECHO"
            
        # 3. MURO (Vertical, alto, delgado)
        if dz > 1.5 and (dx < 0.4 or dy < 0.4):
            # Si es delgado en X/Y pero ancho en el otro, es muro. 
            # Si es delgado en ambos, podría ser columna.
            if dx > 1.0 or dy > 1.0:
                return "MURO"
            return "COLUMNA"
            
        # 4. VENTANA / CRISTAL (Muy delgado, nombre clave)
        if (dx < 0.1 or dy < 0.1 or dz < 0.1) and ("PLANE" in name or "GLASS" in name or "CRISTAL" in name):
            return "VENTANA"
            
        # 5. PILAR / COLUMNA (Vertical, base pequeña)
        if dz > 1.0 and dx < 0.8 and dy < 0.8:
            return "COLUMNA"
            
        return "ELEMENTO_GENERICO"
