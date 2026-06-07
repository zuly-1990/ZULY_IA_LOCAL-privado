"""
Knowledge Intake v1 - Ingesta de Conocimiento Crudo

Permite recibir conocimiento externo auténtico SIN procesarlo.

IMPORTANTE:
- NO interpreta contenido
- NO aprende patrones
- NO extrae conclusiones
- NO generaliza
- SOLO almacena y etiqueta

Principio: "El conocimiento entra crudo. La interpretación vendrá después."
"""

import json
import os
from typing import Dict, Any, List
from datetime import datetime
from extensions.knowledge_intake.schema import KnowledgeSchema, SourceType, SpeakerType, ContextType


class IntakeV1:
    """
    Sistema de ingesta de conocimiento crudo.
    
    Recibe y almacena conocimiento sin procesarlo.
    
    NO analiza.
    NO interpreta.
    NO decide.
    SOLO guarda.
    """
    
    def __init__(self, storage_path: str = "data/knowledge_intake"):
        """
        Inicializa el sistema de ingesta.
        
        Args:
            storage_path: Ruta donde almacenar el conocimiento
        """
        self.storage_path = storage_path
        self._ensure_storage_exists()
    
    def _ensure_storage_exists(self):
        """Crea el directorio de almacenamiento si no existe."""
        os.makedirs(self.storage_path, exist_ok=True)
    
    def receive(
        self,
        raw_text: str,
        source: SourceType = "informal_interview",
        speaker_type: SpeakerType = "unknown",
        context: ContextType = "unknown",
        metadata: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Recibe conocimiento crudo y lo almacena SIN PROCESAR.
        
        Args:
            raw_text: Texto exacto como se recibió (SIN MODIFICAR)
            source: Tipo de fuente
            speaker_type: Tipo de hablante
            context: Contexto
            metadata: Metadatos adicionales
        
        Returns:
            Entrada creada con ID único
        """
        # Crear entrada usando schema
        entry = KnowledgeSchema.create_entry(
            raw_text=raw_text,
            source=source,
            speaker_type=speaker_type,
            context=context,
            metadata=metadata
        )
        
        # Generar ID único
        entry_id = self._generate_id()
        entry["id"] = entry_id
        
        # Guardar
        self._save_entry(entry)
        
        return entry
    
    def _generate_id(self) -> str:
        """
        Genera ID único para la entrada.
        
        Returns:
            ID único basado en timestamp
        """
        return f"intake_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
    
    def _save_entry(self, entry: Dict[str, Any]):
        """
        Guarda entrada en almacenamiento.
        
        Args:
            entry: Entrada a guardar
        """
        # Validar estructura
        if not KnowledgeSchema.validate_entry(entry):
            raise ValueError("Entrada no tiene estructura válida")
        
        # Guardar como JSON individual
        filename = f"{entry['id']}.json"
        filepath = os.path.join(self.storage_path, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(entry, f, ensure_ascii=False, indent=2)
    
    def get_entry(self, entry_id: str) -> Dict[str, Any]:
        """
        Recupera una entrada por ID.
        
        Args:
            entry_id: ID de la entrada
        
        Returns:
            Entrada recuperada
        """
        filename = f"{entry_id}.json"
        filepath = os.path.join(self.storage_path, filename)
        
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Entrada {entry_id} no encontrada")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def list_entries(self) -> List[str]:
        """
        Lista IDs de todas las entradas.
        
        Returns:
            Lista de IDs
        """
        if not os.path.exists(self.storage_path):
            return []
        
        entries = []
        for filename in os.listdir(self.storage_path):
            if filename.endswith('.json'):
                entry_id = filename[:-5]  # Remover .json
                entries.append(entry_id)
        
        return sorted(entries)


# Constantes
INTAKE_VERSION = "1.0"
PROCESSING_ENABLED = False

# Mensaje de advertencia
WARNING_MESSAGE = (
    "Intake v1 solo recibe y almacena conocimiento crudo. "
    "NO procesa, NO analiza, NO interpreta, NO aprende."
)
