"""
render_evaluator.py

Evaluador especializado en auditar la calidad y veracidad de los archivos de imagen generados.
"""

import os
from pathlib import Path
from typing import Dict, List, Any, Optional
from core.utils.logging import log_info, log_warning

class RenderEvaluator:
    """Auditor de archivos de imagen"""

    def evaluate(self, file_path: Optional[str], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Audita un archivo de imagen.
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
            status = 'EMPTY_FILE'
            score = 0.1
        elif file_size < 1000: # < 1KB es sospechoso para un render
            findings.append("ADVERTENCIA: Archivo excesivamente pequeño, posible error de cabecera")
            status = 'SUSPICIOUS'
            score = 0.3
        else:
            status = 'PHYSICALLY_VALID'
            score = 0.9

        # 3. Verificación de formato (basado en extensión)
        if path.suffix.lower() not in ['.png', '.jpg', '.jpeg']:
            findings.append(f"ADVERTENCIA: Formato inesperado {path.suffix}")
            score -= 0.1

        # 4. Verificación de contexto (si se esperaba un resultado específico)
        if context and 'expected_min_size' in context:
            if file_size < context['expected_min_size']:
                findings.append(f"No cumple con el tamaño mínimo esperado: {context['expected_min_size']} bytes")
                score *= 0.8

        if status == 'PHYSICALLY_VALID' and score >= 0.8:
            status = 'SUCCESS'

        return {
            'status': status,
            'score': max(0.0, min(1.0, score)),
            'findings': findings
        }
