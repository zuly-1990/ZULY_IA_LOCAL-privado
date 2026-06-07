"""
environment_guard.py

FASE 18.5: Control de Entorno
Verifica que ZULY solo actúa dentro de contextos válidos.

Regla: Si el contexto no es válido → NO ejecutar nada.
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from core.utils.logging import log_info, log_warning, log_error


@dataclass
class EnvironmentContext:
    """Contexto de entorno validado."""
    scene_name: str
    collection_name: str
    file_path: Optional[str]
    object_count: int
    is_valid: bool
    validation_errors: List[str]


class EnvironmentGuard:
    """
    Guardia de entorno que verifica contexto antes de actuar.
    
    REGLAS:
    - Solo actúa en escena activa válida
    - Solo actúa en colecciones objetivo permitidas
    - Si no puede verificar → NO ejecutar
    """
    
    def __init__(self, adapter=None):
        """
        Inicializa el guardia de entorno.
        
        Args:
            adapter: EngineAdapter (si es None, se obtiene automáticamente)
        """
        self._adapter = adapter
        self._allowed_collections: List[str] = []  # Vacío = todas permitidas
        self._last_context: Optional[EnvironmentContext] = None
    
    def _get_adapter(self):
        """Obtiene adapter si no está configurado."""
        if self._adapter is None:
            try:
                from core.adapters import get_engine_adapter
                self._adapter = get_engine_adapter()
            except Exception:
                pass
        return self._adapter
    
    def validate_environment(self) -> EnvironmentContext:
        """
        Valida el entorno actual antes de cualquier operación.
        
        Returns:
            EnvironmentContext con el resultado de la validación.
        """
        errors = []
        adapter = self._get_adapter()
        
        # Si no hay adapter disponible
        if not adapter or not adapter.is_available():
            return EnvironmentContext(
                scene_name="unknown",
                collection_name="unknown",
                file_path=None,
                object_count=0,
                is_valid=False,
                validation_errors=["Engine adapter not available"]
            )
        
        try:
            # Obtener estado de la escena
            scene_state = adapter.get_scene_state()
            
            if not scene_state.get('success', False):
                errors.append("Could not retrieve scene state")
                return EnvironmentContext(
                    scene_name="unknown",
                    collection_name="unknown",
                    file_path=None,
                    object_count=0,
                    is_valid=False,
                    validation_errors=errors
                )
            
            # Extraer información
            scene_name = scene_state.get('scene_name', 'Scene')
            objects = scene_state.get('objects', [])
            object_count = len(objects)
            
            # Determinar colección (por ahora, usar "Scene Collection" como default)
            collection_name = scene_state.get('active_collection', 'Scene Collection')
            file_path = scene_state.get('file_path')
            
            # Validar colección si hay restricciones
            if self._allowed_collections and collection_name not in self._allowed_collections:
                errors.append(f"Collection '{collection_name}' not in allowed list")
            
            # Contexto es válido si no hay errores
            is_valid = len(errors) == 0
            
            context = EnvironmentContext(
                scene_name=scene_name,
                collection_name=collection_name,
                file_path=file_path,
                object_count=object_count,
                is_valid=is_valid,
                validation_errors=errors
            )
            
            self._last_context = context
            
            if is_valid:
                log_info(f"✓ Environment valid: {scene_name} ({object_count} objects)")
            else:
                log_warning(f"✗ Environment invalid: {errors}")
            
            return context
            
        except Exception as e:
            log_error(f"Environment validation error: {e}")
            return EnvironmentContext(
                scene_name="error",
                collection_name="error",
                file_path=None,
                object_count=0,
                is_valid=False,
                validation_errors=[str(e)]
            )
    
    def set_allowed_collections(self, collections: List[str]):
        """Define las colecciones permitidas."""
        self._allowed_collections = collections
        log_info(f"Allowed collections set: {collections}")
    
    def clear_allowed_collections(self):
        """Permite todas las colecciones."""
        self._allowed_collections = []
        log_info("All collections now allowed")
    
    def can_proceed(self) -> bool:
        """
        Verifica si se puede proceder con una operación.
        
        Esta es la verificación principal que debe llamarse
        ANTES de cualquier operación.
        
        Returns:
            True si el entorno es válido, False si no.
        """
        context = self.validate_environment()
        return context.is_valid
    
    def get_last_context(self) -> Optional[EnvironmentContext]:
        """Retorna el último contexto validado."""
        return self._last_context
    
    def describe_current_state(self) -> Dict[str, Any]:
        """
        Describe el estado actual del entorno para confirmación visual.
        
        Returns:
            Dict con descripción completa del entorno.
        """
        context = self.validate_environment()
        
        if not context.is_valid:
            return {
                'valid': False,
                'errors': context.validation_errors,
                'description': "Cannot describe invalid environment"
            }
        
        adapter = self._get_adapter()
        scene_state = adapter.get_scene_state() if adapter else {}
        
        objects_description = []
        for obj in scene_state.get('objects', []):
            objects_description.append({
                'name': obj.get('name', 'unknown'),
                'type': obj.get('type', 'unknown'),
                'location': obj.get('location', [0, 0, 0]),
                'collection': context.collection_name
            })
        
        return {
            'valid': True,
            'scene': context.scene_name,
            'collection': context.collection_name,
            'file_path': context.file_path,
            'object_count': context.object_count,
            'objects': objects_description
        }


# Singleton para uso global
_environment_guard: Optional[EnvironmentGuard] = None


def get_environment_guard() -> EnvironmentGuard:
    """Obtiene la instancia global del EnvironmentGuard."""
    global _environment_guard
    if _environment_guard is None:
        _environment_guard = EnvironmentGuard()
    return _environment_guard


def validate_before_action() -> bool:
    """
    Función helper para validar antes de cualquier acción.
    
    Uso:
        if not validate_before_action():
            return {'success': False, 'error': 'Invalid environment'}
    """
    return get_environment_guard().can_proceed()
