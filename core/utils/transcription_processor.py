# core/utils/transcription_processor.py
import re
import json
from typing import List, Dict, Any
from core.structural_interpreter import StructuralInterpreter
from core.utils.transcription_evaluator import TranscriptionEvaluator

class TranscriptionProcessor:
    """
    Módulo para procesar transcripciones (YouTube/Voz) y convertirlas en 
    reportes estructurales v1.1.
    """

    def __init__(self):
        self.interpreter = StructuralInterpreter()
        self.evaluator = TranscriptionEvaluator()
        # Lista de muletillas y palabras no técnicas a eliminar
        self.filler_words = [
            r'\beh\b', r'\boh\b', r'\bbueh\b', r'\bbueno\b', r'\bok\b',
            r'\bvale\b', r'\bentonces\b', r'\bmira\b', r'\bo sea\b',
            r'\beso es\b', r'\bdigamos\b'
        ]

    def clean_text(self, text: str) -> str:
        """
        Limpia el texto de muletillas y ruido innecesario.
        """
        cleaned = text.lower()
        for pattern in self.filler_words:
            cleaned = re.sub(pattern, '', cleaned)
        
        # Eliminar espacios dobles resultantes
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        return cleaned

    def segment_didactic_steps(self, text: str) -> List[str]:
        """
        Divide la transcripción en pasos lógicos basados en conectores secuenciales.
        """
        # Conectores que indican un nuevo paso
        connectors = r'(?:\.\s|\bпосле\b|\bluego\b|\bdespués\b|\bdespues\b|\bprimero\b|\bpaso \d+:?|\by finalmente\b|\bpor último\b)'
        
        # Dividir por conectores pero manteniendo el sentido
        segments = re.split(connectors, text, flags=re.IGNORECASE)
        
        # Limpiar segmentos vacíos
        steps = [s.strip() for s in segments if s.strip()]
        return steps

    def process_transcription(self, raw_text: str) -> Dict[str, Any]:
        """
        Flujo completo: Ingesta -> Limpieza -> Segmentación -> Interpretación -> Reporte.
        """
        clean_text = self.clean_text(raw_text)
        steps = self.segment_didactic_steps(clean_text)
        
        step_reports = []
        global_warnings = []
        accumulated_elements = []
        
        for i, step_text in enumerate(steps):
            # Pasar elementos acumulados para detectar relaciones entre pasos
            interpretation = self.interpreter.interpret(step_text, context_elements=accumulated_elements)
            
            # Actualizar elementos acumulados
            accumulated_elements.extend(interpretation["elements"])
            
            step_report = {
                "step_number": i + 1,
                "original_segment": step_text,
                "structural_map": interpretation
            }
            step_reports.append(step_report)
            
            # Acumular advertencias globales
            for warning in interpretation.get("warnings", []):
                global_warnings.append(f"Paso {i+1}: {warning}")

        final_report = {
            "version": "1.1.1-transcription-eval",
            "full_raw_text": raw_text,
            "cleaned_text": clean_text,
            "steps_count": len(steps),
            "steps": step_reports,
            "global_warnings": global_warnings,
            "total_elements_detected": sum(len(s["structural_map"]["elements"]) for s in step_reports)
        }
        
        # Aplicar evaluación de confianza
        confidence_data = self.evaluator.calculate_confidence(final_report)
        final_report.update(confidence_data)
        
        return final_report

    def save_report(self, report: Dict[str, Any], filename: str = "transcription_structural_report.json"):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        print(f"Reporte guardado en: {filename}")

if __name__ == "__main__":
    processor = TranscriptionProcessor()
    sample = "Eh bueno, primero crea un cubo en 0,0,0. Luego mira, pon una esfera encima del cubo y por último escala la esfera a 2."
    report = processor.process_transcription(sample)
    print(json.dumps(report, indent=2))
