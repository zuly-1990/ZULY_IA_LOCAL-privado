# core/utils/transcription_evaluator.py
import re
import os
from typing import List, Dict, Any

class TranscriptionEvaluator:
    """
    Módulo de Evaluación y Confianza para Zuly.
    Analiza la claridad y calidad técnica de las instrucciones sin usar APIs externas.
    """

    def __init__(self):
        # Términos ambiguos que reducen el score de claridad
        self.ambiguous_terms = [
            r'un poco', r'más o menos', r'mas o menos', r'por ahí', r'por ahi',
            r'quizás', r'quizas', r'tal vez', r'cerca de', r'aproximadamente',
            r'algo así', r'algo asi', r'muevelo un poco', r'muevela un poco'
        ]

    def evaluate_step_clarity(self, step_text: str) -> float:
        """
        Calcula un score de claridad (0.0 - 1.0) basado en la ausencia de ambigüedad.
        """
        score = 1.0
        matches = 0
        for term in self.ambiguous_terms:
            if re.search(term, step_text, re.IGNORECASE):
                matches += 1
        
        # Penalización: cada término ambiguo resta 0.25 (mínimo 0.0)
        score = max(0.0, score - (matches * 0.25))
        return score

    def detect_technical_gaps(self, step_report: Dict[str, Any]) -> List[str]:
        """
        Analiza el mapa estructural del paso para detectar vacíos técnicos.
        """
        gaps = []
        # Soporta tanto si el mapa está en una clave como si el reporte ES el mapa
        map_data = step_report.get("structural_map", step_report)
        
        # 1. Objetos sin ubicación ni relación (flotando en el limbo lingüístico)
        for el in map_data["elements"]:
            parameters = el.get("parameters", {})
            has_location = "location" in parameters
            is_target_of_rel = any(r["target"] == el["id"] for r in map_data.get("relations", []))
            is_source_of_rel = any(r["source"] == el["id"] for r in map_data.get("relations", []))
            
            if not has_location and not is_target_of_rel and not is_source_of_rel:
                gaps.append(f"El objeto '{el['id']}' no tiene ubicación definida ni relaciones espaciales.")
            
            # 2. Roles sin parámetros críticos (ej: soporte sin dimensiones)
            if el["role"] == "support" and "size" not in parameters:
                gaps.append(f"El soporte '{el['id']}' carece de dimensiones especificadas.")

        return gaps

    def calculate_confidence(self, report: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calcula el índice de confianza global del tutorial.
        """
        steps = report.get("steps", [])
        if not steps:
            return {"score": 0.0, "level": "BAJO", "reason": "No hay pasos procesados."}

        clarity_scores = []
        total_gaps = 0
        
        for step in steps:
            step_text = step["original_segment"]
            clarity = self.evaluate_step_clarity(step_text)
            step["clarity_score"] = clarity
            clarity_scores.append(clarity)
            
            # Detectar vacíos específicos
            step_gaps = self.detect_technical_gaps(step)
            step["technical_gaps"] = step_gaps
            total_gaps += len(step_gaps)

        avg_clarity = sum(clarity_scores) / len(clarity_scores)
        
        # Penalización por advertencias estructurales previas y nuevos vacíos
        warning_count = len(report.get("global_warnings", []))
        penalty = (warning_count * 0.05) + (total_gaps * 0.1)
        
        final_score = max(0.0, avg_clarity - penalty)
        
        # Clasificación
        if final_score >= 0.8:
            level = "ALTO"
            recommendation = "Tutorial confiable y preciso."
        elif final_score >= 0.5:
            level = "MEDIO"
            recommendation = "Tutorial usable pero requiere supervisión o ajustes manuales."
        else:
            level = "BAJO"
            recommendation = "Riesgo de mala práctica o instrucciones altamente ambiguas."

        return {
            "tutorial_confidence_score": round(final_score, 2),
            "confidence_level": level,
            "average_clarity": round(avg_clarity, 2),
            "total_technical_gaps": total_gaps,
            "recommendation": recommendation,
            "ambiguous_language_detected": avg_clarity < 1.0,
            "technical_gaps_detected": total_gaps > 0,
            "ambiguous_steps": [s for s in steps if s.get("clarity_score", 1.0) < 1.0 or s.get("technical_gaps")],
            "detected_concepts": self.detect_procedural_concepts(report),
            "detected_paradigms": self.detect_paradigms(report)
        }

    def detect_procedural_concepts(self, report: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        [Fase 5.9] Detecta conceptos procedurales descriptivos (no ejecutables).
        """
        detected = []
        from core.knowledge.atomic_dictionary import ATOMIC_DICTIONARY
        procedural_defs = ATOMIC_DICTIONARY.get("procedural_descriptors", {})
        print(f"DEBUG: procedural keys: {procedural_defs.keys()}")
        
        # Unificar todo el texto del tutorial
        full_text = " ".join([s.get("original_segment", "") for s in report.get("steps", [])]).lower()
        print(f"DEBUG: full_text: {full_text}")
        
        for concept_id, definition in procedural_defs.items():
            for keyword in definition.get("keywords", []):
                if keyword in full_text:
                    detected.append({
                        "concept": concept_id,
                        "confidence_impact": "NEUTRAL",
                        "execution": "BLOQUEADA",
                        "term_detected": keyword
                    })
                    # Solo reportar una vez por concepto
                    break
            
        return detected

    def detect_paradigms(self, report: Dict[str, Any]) -> Dict[str, Any]:
        """
        [Fase 5.12] Detecta el paradigma técnico dominante en el tutorial.
        """
        from core.knowledge.atomic_dictionary import ATOMIC_DICTIONARY
        paradigms_def = ATOMIC_DICTIONARY.get("paradigms", {})
        
        full_text = " ".join([s.get("original_segment", "") for s in report.get("steps", [])]).lower()
        
        detected_counts = {}
        detected_list = []
        
        for p_id, p_data in paradigms_def.items():
            count = 0
            for kw in p_data.get("keywords", []):
                if kw in full_text:
                    count += 1
            if count > 0:
                detected_counts[p_id] = count
                detected_list.append(p_id)
                
        # Determinación de paradigma dominante (prioriza el más complejo/restrictivo)
        compatibility = "SUPPORTED"
        if "PARADIGM_PROCEDURAL_EVALUATED" in detected_list:
            dominant = "PARADIGM_PROCEDURAL_EVALUATED"
            compatibility = "NO_EJECUTABLE"
        elif "PARADIGM_DECLARATIVE" in detected_list:
            dominant = "PARADIGM_DECLARATIVE"
            compatibility = "REQUIERE_INTERPRETACION"
        elif "PARADIGM_MODULAR" in detected_list:
            dominant = "PARADIGM_MODULAR"
            compatibility = "SUPPORTED"
        elif "PARADIGM_IMPERATIVE" in detected_list:
            dominant = "PARADIGM_IMPERATIVE"
            compatibility = "LEGACY"
        else:
            dominant = "PARADIGM_IMPERATIVE" # Default
            
        return {
            "adherent_paradigms": detected_list,
            "dominant_paradigm": dominant,
            "compatibility_status": compatibility
        }

def evaluate_transcription(file_path: str) -> Dict[str, Any]:
    """
    Función auxiliar para evaluar una transcripción desde un archivo.
    """
    from core.structural_interpreter import StructuralInterpreter
    interpreter = StructuralInterpreter()
    evaluator = TranscriptionEvaluator()
    
    if not os.path.exists(file_path):
        return {"error": f"Archivo no encontrado: {file_path}", "confidence_level": "BAJO"}
        
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    steps_text = content.split('\n')
    processed_steps = []
    cumulative_elements = []
    
    for segment in steps_text:
        if not segment.strip(): continue
        step_data = interpreter.interpret(segment, context_elements=cumulative_elements)
        step_data["original_segment"] = segment
        processed_steps.append(step_data)
        if "elements" in step_data:
            cumulative_elements.extend(step_data["elements"])
            
    full_report = {"steps": processed_steps, "global_warnings": []}
    return evaluator.calculate_confidence(full_report)
