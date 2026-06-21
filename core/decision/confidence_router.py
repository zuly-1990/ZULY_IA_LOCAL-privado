from typing import Dict, Any, Tuple
from core.utils.logging import log_info, log_warning, log_debug
from core.cognition.zuly_memory_rag import ZulyMemoryRAG

class ConfidenceRouter:
    """
    Enrutador de Confianza para ZULY.
    Decide si un comando se puede resolver usando la memoria local (gratis y rápida),
    si necesita refuerzo de una IA gratuita (Groq/DeepSeek), o si requiere 
    el razonamiento avanzado de la IA principal (Gemini).
    """
    def __init__(self):
        self.rag = ZulyMemoryRAG()
        # Umbrales de confianza
        self.THRESHOLD_LOCAL = 0.85
        self.THRESHOLD_REINFORCE = 0.60

    def route_command(self, query: str) -> Tuple[str, Dict[str, Any]]:
        """
        Analiza el comando y decide la ruta de ejecución.
        Retorna la ruta ('local', 'reinforce', 'advanced') y el contexto encontrado.
        """
        log_info(f"Enrutando comando: '{query}'")
        
        # Buscar en memoria local
        results = self.rag.search(query, top_k=1)
        
        if not results:
            log_info("No se encontró contexto en memoria local. Ruta: ADVANCED.")
            return 'advanced', {}

        best_match = results[0]
        confidence = best_match['similarity']
        
        log_info(f"Confianza de memoria local: {confidence:.2f}")

        if confidence >= self.THRESHOLD_LOCAL:
            log_info("Confianza ALTA. Ruta: LOCAL (Ejecución Directa).")
            return 'local', best_match
        elif confidence >= self.THRESHOLD_REINFORCE:
            log_info("Confianza MEDIA. Ruta: REINFORCE (Uso de API gratuita para verificación).")
            return 'reinforce', best_match
        else:
            log_info("Confianza BAJA. Ruta: ADVANCED (Requiere razonamiento profundo).")
            return 'advanced', best_match

    def execute_with_api(self, query: str, route: str, context: Dict[str, Any]) -> str:
        """
        Ejecuta el comando utilizando la API adecuada según la ruta.
        Esta función se integra con el multi_api_orchestrator.
        """
        if route == 'local':
            # Extraer el handler sugerido del contexto de memoria
            handler_str = context['text'].split('handler: ')[-1] if 'handler: ' in context['text'] else 'unknown'
            return f"Ejecutando handler local: {handler_str}"
        elif route == 'reinforce':
            # Delegar a API rápida y gratuita
            return "Ejecutando con Groq/DeepSeek (API rápida)..."
        else:
            # Delegar a la API pesada
            return "Ejecutando con Gemini Pro (API principal)..."
