# core/dialog/__init__.py
"""
Gestor de Diálogo para el agente Zuly.
Implementa la Fase 1 del Plan Maestro Unificado: Comprensión y Ambigüedad.
"""

from typing import Dict, Any, Tuple, List, Optional
from core.intents.intent_manager import Intent
from core.utils.logging import log_info, log_warning, log_debug
import os
import json
from core.dialog.cognitive_risk_explainer import CognitiveRiskExplainer
from core.dialog.clarification_question_generator import ClarificationQuestionGenerator

class DialogDecision:
    """Tipos de decisiones que puede tomar el gestor de diálogo."""
    EXECUTE = "EXECUTE"      # Todo claro, proceder a ejecución (o safeguard)
    CLARIFY = "CLARIFY"      # Falta información o hay ambigüedad
    REJECT = "REJECT"       # La orden no tiene sentido o es inválida

class DialogManager:
    """
    Gestiona la interacción con el usuario para resolver ambigüedades.
    
    Regla de Oro: Nunca inventar datos. Si falta algo, se pregunta.
    """
    
    def __init__(self):
        # Definición de parámetros estrictamente necesarios por comando
        # Nota: Usamos la nomenclatura de EntityExtractor ('posicion', 'objeto', etc.)
        self.requirements = {
            'blender.create_cube': ['posicion'],
            'blender.create_sphere': ['posicion'],
            'blender.create_primitive': ['objeto', 'posicion'],
            'blender.move_object': ['objeto', 'posicion'],
            'blender.rotate_object': ['objeto', 'rotacion'],
            'blender.scale_object': ['objeto', 'tamaño'],
            'blender.apply_material': ['objeto', 'material_name'],
            'blender.set_material_color': ['material_name', 'color'],
        }
        
        # Umbrales de confianza
        self.CONFIDENCE_THRESHOLD_LOW = 0.4
        self.CONFIDENCE_THRESHOLD_HIGH = 0.8

    def validate_intent(self, intent: Intent, context: Optional[Dict[str, Any]] = None) -> Tuple[str, str, Dict[str, Any]]:
        """
        Analiza una intención y decide si el agente puede proceder.
        
        Args:
            intent: La intención procesada por el IntentManager.
            context: Contexto de ejecución (incluyendo modo).
            
        Returns:
            Tuple[str, str, Dict]: (Decisión, Mensaje al usuario, Metadatos)
        """
        context = context or {}
        mode = context.get('mode', 'hybrid')
        cmd_name = getattr(intent, 'command', 'unknown')
        log_debug(f"DialogManager analizando comando: {cmd_name} (Modo: {mode})")
        
        # Caso 0: Intención nula o desconocida
        if not intent or cmd_name == 'unknown' or cmd_name == 'system.noop':
            return (
                DialogDecision.REJECT, 
                "Acción no identificada en la petición. Se requiere mayor especificidad para proceder.",
                {}
            )

        # SI EL MODO ES REACTIVO (Automatizado), permitimos pasar si la confianza es decente
        # e ignoramos bloqueos de paradigma que son para el chat interactivo
        if mode == 'reactive' and intent.confidence >= self.CONFIDENCE_THRESHOLD_LOW:
             log_info(f"Bypass de DialogManager por modo REACTIVO para: {cmd_name}")
             return (DialogDecision.EXECUTE, "Ejecución automatizada permitida.", {})

        # Integración Fase 5.7 y 5.9: Chequeo PREVIO de riesgos y conceptos bloqueados
        report_path = "transcription_evaluation_report.json"
        
        # DEBUG PRINTS REMOVED (Clean implementation)
        if os.path.exists(report_path):
            try:
                with open(report_path, 'r') as f:
                    evaluation_report = json.load(f)
                
                # 0. Chequeo de Paradigmas Evolutivos (Fase 5.12)
                paradigms = evaluation_report.get("detected_paradigms", {})
                dominant_paradigm = paradigms.get("dominant_paradigm")
                compatibility = paradigms.get("compatibility_status")
                
                if compatibility in ["REQUIERE_INTERPRETACION", "NO_EJECUTABLE"]:
                    log_info(f"Bloqueo por paradigma no soportado: {dominant_paradigm}")
                    return (
                        DialogDecision.REJECT,
                        f"Detectado paradigma {dominant_paradigm.replace('PARADIGM_', '').lower()}. El entorno actual opera bajo un paradigma distinto. Se requiere reinterpretación conceptual antes de cualquier ejecución.",
                        {"paradigm": dominant_paradigm}
                    )

                # 1. Bloqueo por Conceptos Procedurales (Prioridad Máxima)
                detected_concepts = evaluation_report.get("detected_concepts", [])
                for concept in detected_concepts:
                    if concept.get("concept") == "GEOMETRY_NODES_CONCEPTO" and concept.get("execution") == "BLOQUEADA":
                        log_info("Bloqueo por concepto procedural detectado (Geometry Nodes).")
                        return (
                            DialogDecision.REJECT,
                            f"Detectado sistema procedural (Geometry Nodes). Concepto registrado como descriptivo. Se requiere definición explícita de geometría base y objetivo.",
                            {"concept": concept}
                        )

                # 2. Explicación de Riesgos
                explainer = CognitiveRiskExplainer(evaluation_report)
                dialog_messages = explainer.explain()
                log_debug(f"Fase 5.7 - Mensajes de riesgo: {dialog_messages}")
                
            except Exception as e:
                log_warning(f"Error procesando reporte de evaluación: {e}")

        # Caso 1: Confianza muy baja (Ambigüedad real)
        if intent.confidence < self.CONFIDENCE_THRESHOLD_LOW:
            return (
                DialogDecision.REJECT,
                "Petición con ambigüedad excedida. Se requiere reformulación clara para evitar acciones no deseadas.",
                {'confidence': intent.confidence}
            )

        # Caso 2: Confianza media (Requiere confirmación/aclaración)
        if intent.confidence < self.CONFIDENCE_THRESHOLD_HIGH:
            msg = f"Detectada intención potencial para '{cmd_name}' con confianza media. Se requiere confirmación para proceder."
            return (
                DialogDecision.CLARIFY,
                msg,
                {'intent': cmd_name, 'confidence': intent.confidence}
            )

        # Caso 3: Verificar parámetros obligatorios (Blindaje contra invención de datos)
        required_params = self.requirements.get(cmd_name, [])
        missing_params = [p for p in required_params if p not in intent.parameters]
        
        if missing_params:
            msg = f"Detectada intención para '{cmd_name}'. Se requiere especificar: {', '.join(missing_params)}."
            return (
                DialogDecision.CLARIFY,
                msg,
                {'missing': missing_params}
            )

        # Caso 4: Todo correcto
        log_info(f"Intención '{cmd_name}' validada por DialogManager.")
        return (
            DialogDecision.EXECUTE,
            f"Validación completada. Ejecutando {cmd_name}...",
            {}
        )

    def handle_rejection(self, reason: str) -> str:
        """Genera un mensaje de rechazo con explicación."""
        return f"Orden rechazada: {reason}"
