import json
from typing import Dict, List, Any
from core.utils.logging import log_info, log_error, log_warning
from core.external.multi_api_orchestrator import MultiAPIOrchestrator
from core.utils.nlu import CommandIntent

class ThoughtEngine:
    """
    Motor de Pensamiento Deliberativo Nivel C4 (Comité de Expertos).
    Fase 1: Arquitecta (Gemini)
    Fase 2: Ingeniera (DeepSeek)
    Fase 3: Revisora (Groq)
    """
    
    def __init__(self):
        self.orchestrator = MultiAPIOrchestrator()
        
    def generate_plan(self, user_request: str, scene_context: Dict[str, Any], recent_errors: List[str] = None) -> List[CommandIntent]:
        """
        Analiza una petición y genera un plan estructurado de comandos usando el comité.
        """
        log_info(f"[ThoughtEngine C4] Iniciando planificación jerárquica para: {user_request}")
        
        scene_objects = [obj.get("name", "Unknown") for obj in scene_context.get("objects", [])]
        error_context = ""
        if recent_errors:
            error_context = "\nIMPORTANTE (RAG): Ten en cuenta estos errores que cometiste recientemente para NO repetirlos:\n" + "\n".join(recent_errors[-3:])
            
        # 1. FASE ARQUITECTA (Gemini)
        prompt_arquitecta = f"""
Eres Zuly Arquitecta. Diseña un plan conceptual para la petición del usuario.
Petición: "{user_request}"
Objetos actuales: {scene_objects}{error_context}

Devuelve una lista conceptual de pasos (no JSON, solo texto claro de qué hay que hacer).
"""
        log_info("[C4 - Fase 1] Consultando a la Arquitecta (Gemini)...")
        plan_conceptual = self.orchestrator.call_advanced_model(prompt_arquitecta)
        
        # 2. FASE INGENIERA (DeepSeek Coder)
        prompt_ingeniera = f"""
Eres Zuly Ingeniera. Traduce el siguiente plan conceptual a un JSON estricto con comandos.
Plan conceptual: {plan_conceptual}
Objetos actuales: {scene_objects}
Comandos válidos: blender.create_cube, blender.create_sphere, blender.create_plane, blender.create_pro_wall, blender.create_intelligent_window, blender.move_object, blender.scale_object, blender.rotate_object, blender.apply_material, blender.set_parent, blender.generate_geometry_nodes.
Nota de Arquitectura: Si el usuario pide un edificio o geometría procedural con nodos (usando blender.generate_geometry_nodes), el estilo y modelo a seguir DEBE ser inspirado en la copia más antigua y original de la "Villa Savoye" (pilotes, ventanas longitudinales, planta libre).

Devuelve ÚNICAMENTE un JSON así:
{{
  "estado_mental": "explicación",
  "plan": [
    {{"command_name": "nombre", "parameters": {{"param1": "val1"}}}}
  ]
}}
"""
        log_info("[C4 - Fase 2] Consultando a la Ingeniera (DeepSeek)...")
        json_plan_raw = self.orchestrator.call_coder_model(prompt_ingeniera)
        
        # Extraer JSON limpio
        if "```json" in json_plan_raw:
            json_plan_raw = json_plan_raw.split("```json")[1].split("```")[0].strip()
        elif "```" in json_plan_raw:
            json_plan_raw = json_plan_raw.split("```")[1].split("```")[0].strip()
            
        # 3. FASE REVISORA (Groq / Llama3)
        prompt_revisora = f"""
Revisa este JSON. Asegúrate de que los comandos sean de la lista válida y que tenga formato correcto.
JSON a revisar:
{json_plan_raw}
Si está bien, devuélvelo tal cual. Si tiene un comando no válido, cámbialo a algo similar válido. Devuelve SOLO JSON.
"""
        log_info("[C4 - Fase 3] Consultando a la Revisora (Groq)...")
        json_revisado = self.orchestrator.call_fast_model(prompt_revisora)
        
        if "```json" in json_revisado:
            json_revisado = json_revisado.split("```json")[1].split("```")[0].strip()
        elif "```" in json_revisado:
            json_revisado = json_revisado.split("```")[1].split("```")[0].strip()
            
        try:
            plan_data = json.loads(json_revisado)
            log_info(f"[ThoughtEngine C4] Plan Aprobado. Estado mental: {plan_data.get('estado_mental', '')}")
            
            intents = []
            for step in plan_data.get("plan", []):
                cmd_name = step.get("command_name")
                params = step.get("parameters", {})
                if cmd_name:
                    intents.append(CommandIntent(command_name=cmd_name, confidence=0.99, parameters=params))
                    
            return intents
            
        except Exception as e:
            log_error(f"[ThoughtEngine C4] Fallo en la validación JSON final: {e}")
            return []
