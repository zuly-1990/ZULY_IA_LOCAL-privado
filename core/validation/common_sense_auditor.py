from typing import Dict, Any, List
import logging

log = logging.getLogger("LYZU")

class CommonSenseAuditor:
    """
    Módulo de Lógica Común y Funcionalidad Arquitectónica de ZULY (Fase 6).
    Se encarga de auditar edificios para asegurar que "tienen sentido para los humanos".
    """
    
    def __init__(self):
        self.rules = [
            self._rule_circulation,
            self._rule_accessibility,
            self._rule_gravity
        ]

    def audit_building(self, building_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Audita los datos semánticos de un edificio y retorna advertencias.
        building_data debería contener una lista de niveles, habitaciones, puertas, escaleras, etc.
        """
        log.info("🕵️‍♀️ [CommonSenseAuditor] Iniciando auditoría funcional...")
        
        report = {
            "passed": True,
            "warnings": [],
            "critical_errors": []
        }
        
        # Validar formato mínimo
        if not building_data or "levels" not in building_data:
            report["critical_errors"].append("Datos del edificio insuficientes para auditar. Falta 'levels'.")
            report["passed"] = False
            return report

        # Ejecutar todas las reglas
        for rule in self.rules:
            rule_result = rule(building_data)
            report["warnings"].extend(rule_result.get("warnings", []))
            report["critical_errors"].extend(rule_result.get("critical_errors", []))
            
        if report["critical_errors"]:
            report["passed"] = False
            
        log.info(f"🕵️‍♀️ [CommonSenseAuditor] Auditoría completada. {len(report['critical_errors'])} Errores, {len(report['warnings'])} Ads.")
        return report

    def _rule_circulation(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Regla 1: Si hay más de 1 nivel habitable, debe haber escaleras/rampas y huecos en las losas."""
        res = {"warnings": [], "critical_errors": []}
        levels = data.get("levels", [])
        
        habitable_levels = [lvl for lvl in levels if lvl.get("is_habitable", True)]
        
        if len(habitable_levels) > 1:
            stairs = data.get("vertical_circulation", [])
            if not stairs:
                res["critical_errors"].append("[CIRCULACIÓN] El edificio tiene múltiples niveles pero no hay escaleras o rampas interconectando pisos. La gente no vuela.")
            else:
                # Validar hueco en la losa
                slab_cutouts = sum([len(lvl.get("slab_cutouts", [])) for lvl in levels])
                if slab_cutouts < len(habitable_levels) - 1:
                     res["critical_errors"].append("[CIRCULACIÓN] Las escaleras chocan contra el techo. Hay niveles que no tienen un hueco en la losa superior para el acceso.")
                     
        return res

    def _rule_accessibility(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Regla 2: Todo cuarto cerrado debe tener al menos una puerta."""
        res = {"warnings": [], "critical_errors": []}
        
        for i, lvl in enumerate(data.get("levels", [])):
            rooms = lvl.get("rooms", [])
            for r_idx, room in enumerate(rooms):
                doors = room.get("doors", 0)
                if doors == 0:
                    res["critical_errors"].append(f"[ACCESIBILIDAD] Habitación {r_idx} en Nivel {i} es una caja sellada (0 puertas).")
                
                windows = room.get("windows", 0)
                room_type = room.get("type", "unknown").lower()
                if windows == 0 and room_type in ["bedroom", "living_room", "kitchen"]:
                    res["warnings"].append(f"[HABITABILIDAD] Habitación {r_idx} ({room_type}) no tiene ventanas. Parecerá una prisión.")
                    
        return res

    def _rule_gravity(self, data: Dict[str, Any]) -> Dict[str, Any]:
         """Regla 3: (Básica) Las losas de techos superiores deben estar apoyadas."""
         res = {"warnings": [], "critical_errors": []}
         # Lógica simulada: Si la losa voladiza > 4 metros sin columnas
         for lvl in data.get("levels", []):
             for slab in lvl.get("slabs", []):
                 overhang = slab.get("overhang_length", 0)
                 if overhang > 5.0:
                     res["critical_errors"].append(f"[ESTRUCTURA] Losa en {lvl.get('name')} vuela más de 5 metros ({overhang}m) sin soporte. Podría colapsar gravitacionalmente.")
         return res
