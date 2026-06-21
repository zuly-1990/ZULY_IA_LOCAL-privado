import os
from pathlib import Path
from core.utils.logging import log_info, log_error
from core.cognition.zuly_memory_rag import ZulyMemoryRAG
import hashlib

class KnowledgeIngestor:
    """
    Ingesta conocimiento desde tutoriales de YouTube, addons y scripts locales.
    Llena la memoria del RAG para que ZULY comience con un conocimiento base profesional.
    """
    def __init__(self, rag: ZulyMemoryRAG):
        self.rag = rag
        self.tutorials_path = Path('ZULY_LAB/entrenamiento_youtube')
        self.transcriptions_path = Path('tests/transcriptions')

    def ingest_directory(self, directory: Path, source_type: str):
        if not directory.exists():
            log_error(f"Directorio no encontrado: {directory}")
            return

        count = 0
        for file_path in directory.glob('*.txt'):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Generamos un ID pseudoaleatorio basado en el hash del nombre del archivo
                exp_id = int(hashlib.md5(file_path.name.encode()).hexdigest()[:8], 16) % 1000000
                context = f"[{source_type.upper()}] Archivo: {file_path.name}\nContenido: {content[:2000]}"
                
                self.rag.ingest_experience(exp_id, context)
                count += 1
            except Exception as e:
                log_error(f"Error ingestando archivo {file_path}: {e}")

        log_info(f"Ingestados {count} documentos desde {directory} como {source_type}.")

    def run_full_ingestion(self):
        log_info("Iniciando ingesta de conocimiento masiva...")
        self.ingest_directory(self.tutorials_path, "tutorial_youtube")
        self.ingest_directory(self.transcriptions_path, "transcription")
        log_info("Ingesta finalizada. ZULY ahora conoce estos tutoriales y patrones.")
