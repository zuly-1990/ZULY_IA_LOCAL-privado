import os
import json
import numpy as np

try:
    from sentence_transformers import SentenceTransformer
    from sklearn.metrics.pairwise import cosine_similarity
    HAS_SENTENCE_TRANSFORMERS = True
except ImportError:
    HAS_SENTENCE_TRANSFORMERS = False

class RAG3DManager:
    """
    Pilar 2: RAG 3D (Recuperación Aumentada por Generación en 3D)
    Este gestor escanea una librería física de modelos 3D (.obj, .fbx, .blend)
    y usa embeddings semánticos para buscar la pieza perfecta que el usuario necesite,
    evitando que DeepSeek tenga que modelar formas complejas desde cero.
    """
    def __init__(self, library_path="/opt/zuly/libreria_3d"):
        self.library_path = library_path
        self.metadata_file = os.path.join(self.library_path, "metadata.json")
        self.model = None
        self.index = []
        
        if not os.path.exists(self.library_path):
            os.makedirs(self.library_path, exist_ok=True)
            # Crear un metadata básico de ejemplo si no existe
            if not os.path.exists(self.metadata_file):
                ejemplo = {
                    "silla_moderna_01.obj": {"descripcion": "Silla de oficina moderna con ruedas y reposabrazos", "tags": ["mueble", "oficina", "silla"]},
                    "puerta_madera.blend": {"descripcion": "Puerta rústica de madera de roble con marco", "tags": ["arquitectura", "puerta", "madera"]},
                    "ventana_cristal.obj": {"descripcion": "Ventana de cristal doble con marco de aluminio negro", "tags": ["arquitectura", "ventana", "cristal"]}
                }
                with open(self.metadata_file, "w", encoding="utf-8") as f:
                    json.dump(ejemplo, f, indent=4)
                    
        self._load_index()

    def _load_index(self):
        """Carga la metadata y genera embeddings si es necesario."""
        if not HAS_SENTENCE_TRANSFORMERS:
            print("[RAG 3D] ADVERTENCIA: sentence-transformers no instalado. Búsqueda semántica desactivada.")
            return

        if not self.model:
            print("[RAG 3D] Cargando modelo de embeddings (all-MiniLM-L6-v2)...")
            self.model = SentenceTransformer('all-MiniLM-L6-v2')

        try:
            with open(self.metadata_file, "r", encoding="utf-8") as f:
                self.metadata = json.load(f)
        except Exception:
            self.metadata = {}

        self.index = []
        for filename, data in self.metadata.items():
            texto = f"{data.get('descripcion', '')} " + " ".join(data.get('tags', []))
            vector = self.model.encode(texto)
            self.index.append({
                "filename": filename,
                "vector": vector,
                "data": data
            })
        print(f"[RAG 3D] Índice cargado con {len(self.index)} objetos.")

    def buscar_objeto(self, query: str, top_k=1) -> list:
        """Encuentra los modelos 3D más relevantes para una búsqueda semántica."""
        if not HAS_SENTENCE_TRANSFORMERS or not self.index:
            return []

        query_vector = self.model.encode([query])[0]
        resultados = []
        
        for item in self.index:
            similitud = cosine_similarity([query_vector], [item["vector"]])[0][0]
            resultados.append({
                "archivo": os.path.join(self.library_path, item["filename"]),
                "similitud": similitud,
                "info": item["data"]
            })
            
        # Ordenar por similitud
        resultados = sorted(resultados, key=lambda x: x["similitud"], reverse=True)
        return resultados[:top_k]

if __name__ == "__main__":
    # Test local
    rag = RAG3DManager("test_lib")
    if HAS_SENTENCE_TRANSFORMERS:
        res = rag.buscar_objeto("quiero construir una casa rústica")
        print(f"Resultado de búsqueda: {res}")
