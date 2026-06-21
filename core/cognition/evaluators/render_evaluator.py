"""
render_evaluator.py

Evaluador especializado en auditar la calidad y veracidad de los archivos de imagen generados.
Integrado con Gemini Vision para análisis visual avanzado.
"""

import os
from pathlib import Path
from typing import Dict, List, Any, Optional
from core.utils.logging import log_info, log_warning, log_error
from core.external.multi_api_orchestrator import MultiAPIOrchestrator

class RenderEvaluator:
    """Auditor de archivos de imagen usando Inteligencia Artificial"""
    
    def __init__(self):
        self.ai_orchestrator = MultiAPIOrchestrator()

    def evaluate(self, file_path: Optional[str], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Audita un archivo de imagen, física y visualmente usando Gemini Vision.
        """
        findings = []
        score = 0.0
        status = 'FAILED'

        if not file_path:
            return {'status': 'MISSING_PATH', 'score': 0.0, 'findings': ['No se proporcionó ruta de archivo']}

        path = Path(file_path)
        
        # 1. Existencia física
        if not path.exists():
            findings.append(f"Archivo no encontrado: {path}")
            return {'status': 'NOT_FOUND', 'score': 0.0, 'findings': findings}

        # 2. Integridad básica (Tamaño)
        file_size = os.path.getsize(path)
        findings.append(f"Archivo detectado: {path.name} ({file_size / 1024:.1f} KB)")
        
        if file_size == 0:
            findings.append("ERROR: El archivo está vacío (0 bytes)")
            return {'status': 'EMPTY_FILE', 'score': 0.1, 'findings': findings}
        elif file_size < 1000:
            findings.append("ADVERTENCIA: Archivo excesivamente pequeño, posible error de cabecera")
            score = 0.3
        else:
            score = 0.5 # Aprobado físicamente, falta validación IA

        # 3. Verificación de formato
        if path.suffix.lower() not in ['.png', '.jpg', '.jpeg']:
            findings.append(f"ADVERTENCIA: Formato inesperado {path.suffix}")
            score -= 0.1

        # 4. Análisis visual con Gemini
        prompt_evaluacion = "Analiza este render 3D. Describe brevemente lo que ves, la calidad de la iluminación y si detectas algún error de geometría."
        if context and 'target_concept' in context:
            prompt_evaluacion += f" Especialmente verifica si representa adecuadamente el concepto: '{context['target_concept']}'."
            
        log_info(f"Solicitando análisis visual a Gemini para {path.name}...")
        ia_feedback = self.ai_orchestrator.analyze_image_with_vision(prompt_evaluacion, str(path))
        
        if "ERROR" in ia_feedback:
            findings.append("⚠️ No se pudo realizar evaluación visual IA: " + ia_feedback)
            # Damos pase con penalización leve si falla la red pero la imagen existe
            score += 0.2
            status = 'PHYSICALLY_VALID_ONLY'
        else:
            findings.append(f"🧠 Análisis de Gemini Vision:\n{ia_feedback}")
            # Si Gemini no reporta "error" ni "vacío", damos puntaje alto
            if "error" not in ia_feedback.lower() and "empty" not in ia_feedback.lower():
                score += 0.5
                status = 'SUCCESS_AI_VERIFIED'
            else:
                score += 0.2
                status = 'AI_WARNINGS_FOUND'

        return {
            'status': status,
            'score': max(0.0, min(1.0, score)),
            'findings': findings
        }
