"""
retention_policy.py

FASE 19: Políticas de Retención de Memoria

Define límites y estrategias para gestión de memoria en ZULY.
"""

from typing import Dict, Any
from dataclasses import dataclass


@dataclass
class RetentionConfig:
    """Configuración de retención para un componente."""
    
    max_live_items: int
    """Máximo de items en memoria/storage activo"""
    
    archive_after_days: int
    """Días antes de archivar"""
    
    compress_archives: bool = True
    """Si se comprimen los archives con gzip"""
    
    auto_cleanup: bool = True
    """Si se ejecuta limpieza automática"""


class RetentionPolicy:
    """
    Políticas centralizadas de retención de memoria.
    
    Define límites y estrategias para cada componente del sistema
    que genera datos históricos.
    """
    
    # Configuración por defecto
    DEFAULT_POLICIES: Dict[str, RetentionConfig] = {
        'trace_core': RetentionConfig(
            max_live_items=1000,
            archive_after_days=30,
            compress_archives=True,
            auto_cleanup=True
        ),
        'action_logger': RetentionConfig(
            max_live_items=10,  # Sesiones
            archive_after_days=7,
            compress_archives=True,
            auto_cleanup=True
        ),
        'pattern_memory': RetentionConfig(
            max_live_items=500,
            archive_after_days=60,
            compress_archives=True,
            auto_cleanup=False  # Patrones son valiosos
        ),
        'consequence_memory': RetentionConfig(
            max_live_items=200,
            archive_after_days=30,
            compress_archives=True,
            auto_cleanup=True
        )
    }
    
    def __init__(self, custom_policies: Dict[str, RetentionConfig] = None):
        """
        Inicializa políticas de retención.
        
        Args:
            custom_policies: Políticas personalizadas (opcional)
        """
        self.policies = self.DEFAULT_POLICIES.copy()
        
        if custom_policies:
            self.policies.update(custom_policies)
    
    def get_policy(self, component: str) -> RetentionConfig:
        """
        Obtiene la política para un componente.
        
        Args:
            component: Nombre del componente
        
        Returns:
            RetentionConfig para el componente
        
        Raises:
            KeyError si el componente no tiene política definida
        """
        if component not in self.policies:
            raise KeyError(f"No retention policy defined for '{component}'")
        
        return self.policies[component]
    
    def set_policy(self, component: str, config: RetentionConfig):
        """
        Establece política personalizada para un componente.
        
        Args:
            component: Nombre del componente
            config: Nueva configuración
        """
        self.policies[component] = config
    
    def should_archive(self, component: str, age_days: int) -> bool:
        """
        Determina si un item debe ser archivado basado en edad.
        
        Args:
            component: Nombre del componente
            age_days: Edad del item en días
        
        Returns:
            True si debe archivarse
        """
        policy = self.get_policy(component)
        return age_days >= policy.archive_after_days
    
    def should_cleanup(self, component: str, current_count: int) -> bool:
        """
        Determina si se necesita limpieza basado en cantidad.
        
        Args:
            component: Nombre del componente
            current_count: Cantidad actual de items
        
        Returns:
            True si se debe ejecutar cleanup
        """
        policy = self.get_policy(component)
        
        if not policy.auto_cleanup:
            return False
        
        return current_count > policy.max_live_items
    
    def get_all_policies(self) -> Dict[str, RetentionConfig]:
        """Retorna todas las políticas configuradas."""
        return self.policies.copy()
    
    def to_dict(self) -> Dict[str, Dict[str, Any]]:
        """Exporta políticas a formato dict."""
        return {
            component: {
                'max_live_items': config.max_live_items,
                'archive_after_days': config.archive_after_days,
                'compress_archives': config.compress_archives,
                'auto_cleanup': config.auto_cleanup
            }
            for component, config in self.policies.items()
        }


# Singleton global
_retention_policy: RetentionPolicy = None


def get_retention_policy() -> RetentionPolicy:
    """Obtiene la instancia global de RetentionPolicy."""
    global _retention_policy
    if _retention_policy is None:
        _retention_policy = RetentionPolicy()
    return _retention_policy
