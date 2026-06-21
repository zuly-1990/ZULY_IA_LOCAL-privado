import json
import sqlite3
import os
import hashlib
from typing import Dict, List, Any, Optional, Tuple
from core.utils.logging import log_info, log_error, log_warning, log_debug

try:
    from sentence_transformers import SentenceTransformer
    import numpy as np
    HAS_SENTENCE_TRANSFORMERS = True
except ImportError:
    HAS_SENTENCE_TRANSFORMERS = False
    log_warning("sentence-transformers no está instalado. ZulyMemoryRAG usará búsqueda por palabras clave en modo degradado.")

class ZulyMemoryRAG:
    """
    RAG Local para ZULY basado en memoria de experiencias.
    Permite buscar comandos y soluciones anteriores usando similitud semántica,
    reduciendo la dependencia de APIs externas.
    """
    _instance = None
    _model = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ZulyMemoryRAG, cls).__new__(cls)
        return cls._instance

    def __init__(self, db_path: str = 'bitacora/memory.db'):
        if not hasattr(self, 'initialized'):
            self.db_path = db_path
            self._ensure_db_schema()
            self._init_model()
            self.initialized = True

    def _init_model(self):
        """Inicializa el modelo de embeddings BAAI/bge-small-en-v1.5"""
        if HAS_SENTENCE_TRANSFORMERS and self._model is None:
            try:
                log_info("Cargando modelo de embeddings (bge-small)... esto puede tomar un momento.")
                self._model = SentenceTransformer('BAAI/bge-small-en-v1.5')
                log_info("Modelo de embeddings cargado correctamente.")
            except Exception as e:
                log_error(f"Error cargando el modelo de embeddings: {e}")
                self._model = None

    def _ensure_db_schema(self):
        """Asegura que la tabla de memoria soporte embeddings"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        try:
            with sqlite3.connect(self.db_path) as conn:
                # Tabla para almacenar embeddings asociados a experiencias
                conn.execute('''
                    CREATE TABLE IF NOT EXISTS rag_embeddings (
                        id INTEGER PRIMARY KEY,
                        experience_id INTEGER,
                        text_content TEXT NOT NULL,
                        embedding BLOB,
                        FOREIGN KEY(experience_id) REFERENCES experiences(id)
                    )
                ''')
                conn.commit()
        except sqlite3.OperationalError as e:
            log_error(f"Error creando esquema RAG en SQLite: {e}")

    def _get_embedding(self, text: str) -> Optional[bytes]:
        """Convierte texto a un vector y lo serializa a bytes"""
        if not self._model:
            return None
        try:
            vector = self._model.encode(text)
            return vector.tobytes()
        except Exception as e:
            log_error(f"Error generando embedding para '{text}': {e}")
            return None

    def ingest_experience(self, experience_id: int, text_context: str):
        """Guarda la experiencia y su embedding"""
        embedding_bytes = self._get_embedding(text_context)
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                INSERT INTO rag_embeddings (experience_id, text_content, embedding)
                VALUES (?, ?, ?)
            ''', (experience_id, text_context, embedding_bytes))
            conn.commit()
            
    def _cosine_similarity(self, a: Any, b: Any) -> float:
        """Calcula similitud del coseno entre dos vectores"""
        if np.linalg.norm(a) == 0 or np.linalg.norm(b) == 0:
            return 0.0
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    def search(self, query: str, top_k: int = 3, threshold: float = 0.75) -> List[Dict[str, Any]]:
        """Busca las experiencias más similares semánticamente"""
        if not self._model:
            return self._fallback_keyword_search(query, top_k)
            
        query_vector = self._model.encode(query)
        results = []
        
        with sqlite3.connect(self.db_path) as conn:
            # Traemos todos los embeddings (en un entorno enorme usaríamos Chroma/FAISS, 
            # pero para memoria local de comandos SQLite con escaneo lineal en memoria es suficiente).
            cursor = conn.execute('SELECT experience_id, text_content, embedding FROM rag_embeddings WHERE embedding IS NOT NULL')
            rows = cursor.fetchall()
            
            for exp_id, text, emb_bytes in rows:
                vector = np.frombuffer(emb_bytes, dtype=np.float32)
                sim = self._cosine_similarity(query_vector, vector)
                if sim >= threshold:
                    results.append({
                        'experience_id': exp_id,
                        'text': text,
                        'similarity': float(sim)
                    })
                    
        results.sort(key=lambda x: x['similarity'], reverse=True)
        return results[:top_k]

    def _fallback_keyword_search(self, query: str, top_k: int) -> List[Dict[str, Any]]:
        """Búsqueda simple por palabras clave si no hay modelo de IA local"""
        keywords = query.lower().split()
        results = []
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute('SELECT experience_id, text_content FROM rag_embeddings')
            rows = cursor.fetchall()
            for exp_id, text in rows:
                text_lower = text.lower()
                matches = sum(1 for kw in keywords if kw in text_lower)
                if matches > 0:
                    sim = matches / len(keywords)
                    results.append({
                        'experience_id': exp_id,
                        'text': text,
                        'similarity': sim
                    })
        results.sort(key=lambda x: x['similarity'], reverse=True)
        return results[:top_k]

    def learn(self, user_query: str, success: bool, handler_used: str):
        """Registra un nuevo aprendizaje de un comando resuelto"""
        if success:
            # Dummy experience_id para el ejemplo, deberia venir de C2
            # Generamos un id pseudo-aleatorio basado en hash
            exp_id = int(hashlib.md5(user_query.encode()).hexdigest()[:8], 16) % 1000000
            self.ingest_experience(exp_id, f"Comando: '{user_query}' -> resuelto por handler: {handler_used}")
