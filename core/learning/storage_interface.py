"""
Interfaz Abstracta de Almacenamiento - Ajuste A3

Propósito:
- Definir capa abstracta para almacenamiento de patrones
- Implementación actual: JSON
- Preparar para futuro: DB/binario/híbrido

Regla: Preparar el camino, no recorrerlo
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class StorageInterface(ABC):
    """
    Interfaz abstracta para almacenamiento de patrones.
    
    Permite cambiar backend sin modificar PatternMemory.
    """
    
    @abstractmethod
    def load(self) -> List[Dict[str, Any]]:
        """
        Carga todos los patrones desde almacenamiento.
        
        Returns:
            Lista de patrones
        """
        pass
    
    @abstractmethod
    def save(self, patterns: List[Dict[str, Any]]) -> bool:
        """
        Guarda todos los patrones a almacenamiento.
        
        Args:
            patterns: Lista de patrones a guardar
            
        Returns:
            True si exitoso, False si error
        """
        pass
    
    @abstractmethod
    def append(self, pattern: Dict[str, Any]) -> bool:
        """
        Agrega un patrón al almacenamiento.
        
        Args:
            pattern: Patrón a agregar
            
        Returns:
            True si exitoso, False si error
        """
        pass
    
    @abstractmethod
    def get_stats(self) -> Dict[str, Any]:
        """
        Retorna estadísticas del almacenamiento.
        
        Returns:
            Diccionario con estadísticas
        """
        pass


class JSONStorage(StorageInterface):
    """
    Implementación de almacenamiento en JSON.
    
    Implementación actual de ZULY.
    Simple, portable, sin dependencias.
    """
    
    def __init__(self, storage_path: str):
        """
        Inicializa almacenamiento JSON.
        
        Args:
            storage_path: Ruta al archivo JSON
        """
        import os
        self.storage_path = storage_path
        self._ensure_directory()
    
    def _ensure_directory(self):
        """Crea directorio si no existe."""
        import os
        directory = os.path.dirname(self.storage_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
    
    def load(self) -> List[Dict[str, Any]]:
        """Carga patrones desde JSON."""
        import os
        import json
        
        if not os.path.exists(self.storage_path):
            return []
        
        try:
            with open(self.storage_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            from core.utils.logging import log_error
            log_error(f"[JSONStorage] Error cargando: {e}")
            return []
    
    def save(self, patterns: List[Dict[str, Any]]) -> bool:
        """Guarda patrones a JSON."""
        import json
        
        try:
            self._ensure_directory()
            with open(self.storage_path, 'w', encoding='utf-8') as f:
                json.dump(patterns, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            from core.utils.logging import log_error
            log_error(f"[JSONStorage] Error guardando: {e}")
            return False
    
    def append(self, pattern: Dict[str, Any]) -> bool:
        """Agrega patrón a JSON (carga, agrega, guarda)."""
        patterns = self.load()
        patterns.append(pattern)
        return self.save(patterns)
    
    def get_stats(self) -> Dict[str, Any]:
        """Estadísticas del almacenamiento JSON."""
        import os
        
        if not os.path.exists(self.storage_path):
            return {
                'backend': 'JSON',
                'file_exists': False,
                'file_size_bytes': 0,
                'pattern_count': 0
            }
        
        patterns = self.load()
        file_size = os.path.getsize(self.storage_path)
        
        return {
            'backend': 'JSON',
            'file_exists': True,
            'file_size_bytes': file_size,
            'file_size_kb': round(file_size / 1024, 2),
            'pattern_count': len(patterns)
        }


# Placeholder para futuras implementaciones
class SQLiteStorage(StorageInterface):
    """
    Implementación futura: SQLite
    
    Ventajas:
    - Búsqueda indexada
    - Queries SQL
    - Mejor escalabilidad
    
    NO implementar ahora.
    """
    
    def __init__(self, db_path: str):
        raise NotImplementedError("SQLiteStorage no implementado aún")
    
    def load(self) -> List[Dict[str, Any]]:
        raise NotImplementedError()
    
    def save(self, patterns: List[Dict[str, Any]]) -> bool:
        raise NotImplementedError()
    
    def append(self, pattern: Dict[str, Any]) -> bool:
        raise NotImplementedError()
    
    def get_stats(self) -> Dict[str, Any]:
        raise NotImplementedError()
