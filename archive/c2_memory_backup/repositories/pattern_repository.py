# core/learning/repositories/pattern_repository.py
import os
import json
from uuid import uuid4
from datetime import datetime
from typing import Dict, List, Optional
from core.utils.logging import log_info, log_error, log_warning

class PatternRepository:
    """
    Clase base para los repositorios de almacenamiento de patrones cognitivos.
    Implementación concreta inicial basada en JSON.
    """
    def __init__(self, file_path: str):
        self.file_path = file_path
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        """Asegura que el archivo JSON y la carpeta existan."""
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump([], f, indent=2)

    def load_all(self) -> List[Dict]:
        """Carga todos los patrones almacenados en este repositorio."""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            log_error(f"Error decodificando {self.file_path}. El archivo puede estar corrupto.")
            return []
        except Exception as e:
            log_error(f"Error cargando patrones de {self.file_path}: {e}")
            return []

    def save_all(self, patterns: List[Dict]) -> bool:
        """Guarda la lista completa de patrones, sobrescribiendo el archivo."""
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(patterns, f, indent=2)
            return True
        except Exception as e:
            log_error(f"Error guardando patrones en {self.file_path}: {e}")
            return False

    def add_pattern(self, pattern: Dict) -> bool:
        """Añade un patrón individual al repositorio y lo persiste."""
        # Se asume que el patrón ya trae el ID y los metadatos requeridos
        patterns = self.load_all()
        patterns.append(pattern)
        return self.save_all(patterns)

    def update_pattern(self, pattern_id: str, pattern_data: Dict) -> bool:
        """Actualiza un patrón existente por ID."""
        patterns = self.load_all()
        for i, p in enumerate(patterns):
            if p.get('pattern_id') == pattern_id:
                patterns[i] = pattern_data
                return self.save_all(patterns)
        return False

    def delete_pattern(self, pattern_id: str) -> bool:
        """Elimina un patrón por ID."""
        patterns = self.load_all()
        initial_count = len(patterns)
        patterns = [p for p in patterns if p.get('pattern_id') != pattern_id]
        if len(patterns) < initial_count:
             return self.save_all(patterns)
        return False

    def get_pattern(self, pattern_id: str) -> Optional[Dict]:
        """Obtiene un patrón por ID."""
        for p in self.load_all():
            if p.get('pattern_id') == pattern_id:
                return p
        return None


class StagingPatternRepository(PatternRepository):
    """
    Repositorio STAGING: Área de pruebas de aprendizaje inmediato. 
    NO ejecutable por Fase 6.
    """
    def __init__(self, storage_dir: str = "memory"):
        # Asegurar que storage_dir sea una carpeta, no un archivo
        super().__init__(os.path.join(storage_dir, "patterns_staging.json"))

class VerifiedPatternRepository(PatternRepository):
    """
    Repositorio VERIFIED: Patrones cristalizados, probados X veces.
    Ejecutable por Fase 6.
    """
    def __init__(self, storage_dir: str = "memory"):
        super().__init__(os.path.join(storage_dir, "patterns_verified.json"))

class QuarantinePatternRepository(PatternRepository):
    """
    Repositorio QUARANTINE: Patrones que han fallado repetidas veces.
    Aislados para depuración.
    """
    def __init__(self, storage_dir: str = "memory"):
        super().__init__(os.path.join(storage_dir, "patterns_quarantine.json"))

class PendingPatternRepository(PatternRepository):
    """
    Repositorio PENDING: Patterns awaiting for final "visto bueno" (approval) from user.
    """
    def __init__(self, storage_dir: str = "memory"):
        super().__init__(os.path.join(storage_dir, "patterns_pending.json"))
