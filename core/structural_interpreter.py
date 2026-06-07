# core/structural_interpreter.py
import re
from typing import Dict, List, Any, Optional
from core.knowledge.atomic_dictionary import ATOMIC_DICTIONARY
from core.utils.logging import log_info, log_debug

class StructuralValidator:
    """
    Capa de Validación Estructural (No Física).
    Detecta incoherencias lógicas y relaciones huérfanas antes de cualquier acción.
    """
    @staticmethod
    def validate(map_data: Dict[str, Any]) -> List[str]:
        warnings = []
        element_ids = {el["id"] for el in map_data["elements"]}
        
        # 1. Validar Relaciones Huérfanas
        for rel in map_data.get("relations", []):
            if rel["source"] not in element_ids:
                warnings.append(f"Relación huérfana: El origen '{rel['source']}' no existe.")
            if rel["target"] not in element_ids:
                warnings.append(f"Relación huérfana: El destino '{rel['target']}' no existe.")
        
        # 2. Validar Incoherencias de Rol
        for el in map_data["elements"]:
            if el["role"] == "support" and not any(r["source"] == el["id"] for r in map_data.get("relations", [])):
                # Si es un soporte pero no está 'soportando' nada (en relaciones)
                # Ojo: esto es una advertencia, no un error fatal
                warnings.append(f"Incoherencia lógica: El objeto '{el['id']}' se define como 'support' pero no tiene relaciones de soporte asignadas.")

        return warnings

class StructuralInterpreter:
    """
    Módulo de Interpretación Estructural para Zuly - v1.1 Refactoreado.
    Separa procesos Deterministas (Diccionario) de Heurísticos (Regex).
    """

    def __init__(self):
        self.dict = ATOMIC_DICTIONARY
        self.validator = StructuralValidator()

    def interpret(self, text: str, context_elements: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Analiza el texto y genera un Mapa Estructural v1.1.1.
        Soporta 'context_elements' para detectar relaciones con objetos definidos previamente.
        """
        log_info(f"Interpretando estructura (v1.1.1): {text}")
        text_lower = text.lower()
        
        elements = self._extract_elements(text_lower)
        
        # Combinar con elementos previos para detección de relaciones
        all_elements = (context_elements or []) + elements
        relations = self._extract_relations(all_elements, text_lower)
        
        # Filtrar relaciones para solo incluir las que involucran al menos un elemento nuevo
        # para evitar duplicidad si se procesa por pasos.
        new_ids = {el["id"] for el in elements}
        filtered_relations = [
            r for r in relations 
            if r["source"] in new_ids or r["target"] in new_ids
        ]
        
        result = {
            "version": "1.1.1",
            "source_text": text,
            "elements": elements,
            "relations": filtered_relations,
            "structurally_complete": self._check_global_completeness(elements),
            "is_complete": self._check_global_completeness(elements), # Alias para v1.0
            "missing_parameters": self._get_all_missing_params(elements),
            "warnings": [],
            "executable": False # Siempre false en esta fase según reglas estrictas
        }

        # Aplicar validación estructural lógica
        result["warnings"] = self.validator.validate(result)
        
        return result

    def _extract_elements(self, text: str) -> List[Dict[str, Any]]:
        # No dividir por comas para evitar romper coordenadas (0,0,0)
        parts = re.split(r'[.;]|\b(?:y|and)\b', text)
        elements = []
        counts = {}

        for part in parts:
            part = part.strip()
            if not part:
                continue
                
            p_type = self._identify_primitive(part)
            if p_type:
                # Generar ID único
                counts[p_type] = counts.get(p_type, 0) + 1
                el_id = f"{p_type}_{counts[p_type]}"
                
                element = {
                    "id": el_id,
                    "type": p_type,
                    "role": self._identify_role(part),
                    "parameters": self._extract_parameters(part, p_type),
                    "missing_parameters": self._get_missing_parameters(part, p_type),
                    "raw_context": part
                }
                element["structurally_complete"] = len(element["missing_parameters"]) == 0
                element["is_complete"] = element["structurally_complete"] # Alias para v1.0
                elements.append(element)
        
        return elements

    # --- MÉTODOS DETERMINISTAS (Seguros/Diccionario) ---
    def _identify_primitive(self, text: str) -> Optional[str]:
        """
        Retorna la primitiva cuya palabra clave aparece PRIMERO en el texto.
        Esto evita que en frases como 'esfera sobre el cubo' se detecte el 'cubo'
        si éste aparece primero en el diccionario atómico.
        """
        first_match = None
        min_pos = float('inf')

        for p_name, data in self.dict["primitives"].items():
            for kw in data["keywords"]:
                pos = text.find(kw)
                if pos != -1 and pos < min_pos:
                    min_pos = pos
                    first_match = p_name
        
        return first_match

    def _identify_role(self, text: str) -> str:
        """Asigna roles solo si son explícitos en el texto."""
        for r_name, keywords in self.dict["roles"].items():
            for kw in keywords:
                if re.search(rf'\b{re.escape(kw)}\b', text):
                    return r_name
        return "undefined"

    # --- MÉTODOS HEURÍSTICOS (Flexibles/Regex/Frágiles) ---
    def _extract_parameters(self, text: str, primitive: str) -> Dict[str, Any]:
        """
        HEURÍSTICA: Intenta extraer números cercanos a palabras clave.
        """
        params = {}
        num_pattern = r'(-?\d+(?:\.\d+)?)'
        
        # Ubicación
        loc_pattern = rf'(?:en|posicion|posición|ubicación|ubicacion|at)\s*{num_pattern}[,\s]+{num_pattern}[,\s]+{num_pattern}'
        loc_match = re.search(loc_pattern, text)
        if loc_match:
            params["location"] = [float(loc_match.group(1)), float(loc_match.group(2)), float(loc_match.group(3))]

        # Otros parámetros numéricos
        for param_type, keywords in self.dict["transformations"].items():
            if param_type == "location": continue
            for kw in keywords:
                pattern = rf'\b{re.escape(kw)}\b\s*(?:de|es|:)?\s*{num_pattern}\b'
                val_match = re.search(pattern, text)
                if val_match:
                    params[param_type] = float(val_match.group(1))
                    break
        
        return params

    def _get_missing_parameters(self, text: str, p_type: str) -> List[str]:
        missing = []
        mandatory = self.dict["primitives"][p_type]["mandatory_params"]
        params = self._extract_parameters(text, p_type)
        
        for m in mandatory:
            if m not in params:
                missing.append(m)
        return missing

    def _extract_relations(self, elements: List[Dict[str, Any]], text: str) -> List[Dict[str, Any]]:
        """
        HEURÍSTICA CRÍTICA: Intenta vincular objetos por cercanía de texto.
        Este es el punto principal para ser reemplazado por un SemanticParser en el futuro.
        """
        relations = []
        if not elements: return relations

        # Patrón para detectar relaciones espaciales
        for rel_type, keywords in self.dict["spatial_relations"].items():
            # Buscamos frases que conecten dos primitivas
            for i, el_source in enumerate(elements):
                for j, el_target in enumerate(elements):
                    if i == j: continue
                    
                    source_kw = self.dict["primitives"][el_source["type"]]["keywords"][0]
                    target_kw = self.dict["primitives"][el_target["type"]]["keywords"][0]
                    
                    for kw in keywords:
                        pattern = rf'{source_kw}.*{re.escape(kw)}.*{target_kw}'
                        if re.search(pattern, text):
                            relations.append({
                                "type": rel_type,
                                "source": el_source["id"],
                                "target": el_target["id"]
                            })
                            break # Evitar duplicados si varios keywords coinciden
        
        return relations

    def _check_global_completeness(self, elements: List[Dict[str, Any]]) -> bool:
        if not elements:
            return False
        return all(el["structurally_complete"] for el in elements)

    def _get_all_missing_params(self, elements: List[Dict[str, Any]]) -> List[str]:
        all_missing = []
        for el in elements:
            for m in el["missing_parameters"]:
                all_missing.append(f"{el['id']}:{m}")
        return all_missing

if __name__ == "__main__":
    interpreter = StructuralInterpreter()
    test_text = "Crea un cubo como base en 0,0,0. Añade una esfera encima del cubo."
    result = interpreter.interpret(test_text)
    import json
    print(json.dumps(result, indent=2))
