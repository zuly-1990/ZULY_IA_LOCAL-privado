"""
pattern_storage.py

FASE 19: Almacenamiento de patrones de construcción.

Permite guardar y recuperar patrones de estructuras compuestas
para su reutilización.
"""

from typing import Dict, Any, List, Optional
from core.learning.storage_interface import JSONStorage
from core.utils.logging import log_info, log_debug, log_error


class PatternStorage:
    """
    Almacenamiento de patrones de construcción reutilizables.
    
    Un patrón define una estructura compuesta:
    - Componentes (primitivas)
    - Relaciones jerárquicas (parent/child)
    - Posiciones relativas
    """
    
    def __init__(self, storage_path: str = "memory/assembly_patterns.json"):
        """
        Inicializa el almacenamiento de patrones.
        
        Args:
            storage_path: Ruta al archivo JSON de patrones
        """
        self.storage = JSONStorage(storage_path)
        self.patterns: List[Dict] = self.storage.load()
        log_debug(f"PatternStorage inicializado: {len(self.patterns)} patrones cargados")
    
    def save_pattern(self, name: str, description: str, components: List[Dict]) -> bool:
        """
        Guarda un nuevo patrón de construcción.
        
        Args:
            name: Nombre único del patrón
            description: Descripción legible
            components: Lista de componentes [
                {
                    'type': 'cube'|'sphere'|...,
                    'location': [x, y, z],
                    'parent': 'component_name' | None,
                    'scale': float | [x, y, z],
                    ...
                }
            ]
        
        Returns:
            bool: True si se guardó correctamente
        """
        # Verificar si ya existe
        existing = self.get_pattern(name)
        if existing:
            log_debug(f"⚠️ Patrón '{name}' ya existe, sobrescribiendo")
            # Eliminar existente
            self.patterns = [p for p in self.patterns if p.get('name') != name]
        
        pattern = {
            'name': name,
            'description': description,
            'components': components,
            'component_count': len(components)
        }
        
        self.patterns.append(pattern)
        success = self.storage.save(self.patterns)
        
        if success:
            log_info(f"✓ Patrón guardado: {name} ({len(components)} componentes)")
        else:
            log_error(f"❌ Error guardando patrón: {name}")
        
        return success
    
    def get_pattern(self, name: str) -> Optional[Dict]:
        """
        Obtiene un patrón por nombre.
        
        Args:
            name: Nombre del patrón
        
        Returns:
            Dict del patrón o None si no existe
        """
        for pattern in self.patterns:
            if pattern.get('name') == name:
                return pattern
        return None
    
    def list_patterns(self) -> List[Dict]:
        """
        Lista todos los patrones disponibles.
        
        Returns:
            Lista de patrones con metadatos
        """
        return [
            {
                'name': p.get('name'),
                'description': p.get('description'),
                'component_count': p.get('component_count', 0)
            }
            for p in self.patterns
        ]
    
    def delete_pattern(self, name: str) -> bool:
        """
        Elimina un patrón.
        
        Args:
            name: Nombre del patrón
        
        Returns:
            bool: True si se eliminó
        """
        original_count = len(self.patterns)
        self.patterns = [p for p in self.patterns if p.get('name') != name]
        
        if len(self.patterns) < original_count:
            success = self.storage.save(self.patterns)
            if success:
                log_info(f"✓ Patrón eliminado: {name}")
            return success
        
        return False
