"""
Knowledge Intake v1 - Schema de Conocimiento Crudo

Define la estructura para almacenar conocimiento sin procesar.

NO contiene lógica de análisis.
NO contiene clasificación semántica.
SOLO estructura de datos.
"""

from typing import Dict, Any, Literal
from datetime import datetime


# Tipos de fuentes permitidas
SourceType = Literal[
    "informal_interview",
    "casual_conversation",
    "spontaneous_response",
    "authentic_experience",
    "human_narrative"
]

# Tipos de hablante
SpeakerType = Literal[
    "adult",
    "child",
    "unknown"
]

# Contextos de conversación
ContextType = Literal[
    "casual_conversation",
    "structured_interview",
    "spontaneous_sharing",
    "storytelling",
    "unknown"
]


class KnowledgeSchema:
    """
    Schema para registro de conocimiento crudo.
    
    Define la estructura mínima sin procesar el contenido.
    """
    
    @staticmethod
    def create_entry(
        raw_text: str,
        source: SourceType = "informal_interview",
        speaker_type: SpeakerType = "unknown",
        context: ContextType = "unknown",
        metadata: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Crea una entrada de conocimiento crudo.
        
        Args:
            raw_text: Texto sin procesar (EXACTO como se recibió)
            source: Tipo de fuente
            speaker_type: Tipo de hablante
            context: Contexto de la conversación
            metadata: Metadatos adicionales opcionales
        
        Returns:
            Diccionario con estructura de conocimiento
        """
        entry = {
            "source": source,
            "speaker_type": speaker_type,
            "raw_text": raw_text,  # SIN MODIFICAR
            "context": context,
            "timestamp": datetime.now().isoformat(),
            "processed": False,  # SIEMPRE False en esta fase
            "metadata": metadata or {}
        }
        
        return entry
    
    @staticmethod
    def validate_entry(entry: Dict[str, Any]) -> bool:
        """
        Valida que una entrada tenga la estructura mínima.
        
        NO valida contenido, solo estructura.
        
        Args:
            entry: Entrada a validar
        
        Returns:
            True si tiene estructura válida, False si no
        """
        required_fields = [
            "source",
            "speaker_type",
            "raw_text",
            "context",
            "timestamp",
            "processed"
        ]
        
        for field in required_fields:
            if field not in entry:
                return False
        
        # Validar que processed es False
        if entry["processed"] is not False:
            return False
        
        # Validar que raw_text no está vacío
        if not entry["raw_text"] or not isinstance(entry["raw_text"], str):
            return False
        
        return True


# Constantes
SCHEMA_VERSION = "1.0"
PROCESSING_ALLOWED = False  # NO en esta fase

# Mensaje de advertencia
WARNING_MESSAGE = (
    "Knowledge Intake v1 solo almacena conocimiento crudo. "
    "NO procesa, NO analiza, NO interpreta."
)
