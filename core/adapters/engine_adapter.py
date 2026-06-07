"""
core/adapters/engine_adapter.py

Interfaz abstracta para motores 3D.
Define el contrato que todos los adapters deben cumplir.

AJUSTES APLICADOS:
- Adapter Stateless (Ajuste 1)
- Contrato explícito de errores (Ajuste 2)
- Métodos para observadores (Ajuste 3)
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Literal
from enum import Enum


class EngineError(Enum):
    """Códigos de error estándar para todos los adapters (Ajuste 2)."""
    ENGINE_NOT_AVAILABLE = "ENGINE_NOT_AVAILABLE"
    OBJECT_NOT_FOUND = "OBJECT_NOT_FOUND"
    INVALID_PARAMS = "INVALID_PARAMS"
    OPERATION_FAILED = "OPERATION_FAILED"
    UNSUPPORTED_OPERATION = "UNSUPPORTED_OPERATION"


class EngineAdapter(ABC):
    """
    Interfaz abstracta para motores 3D.
    
    REGLAS:
    1. El adapter debe ser STATELESS cuando sea posible (Ajuste 1)
    2. Todos los métodos retornan Dict con estructura estándar
    3. Los errores usan códigos de EngineError (Ajuste 2)
    4. El adapter ejecuta → consulta → devuelve → olvida
    """
    
    # ========================================================================
    # UTILIDADES Y ESTADO
    # ========================================================================
    
    @abstractmethod
    def is_available(self) -> bool:
        """
        Verifica si el motor está disponible y funcional.
        
        Returns:
            bool: True si el motor puede ejecutar operaciones
        """
        pass
    
    @abstractmethod
    def get_engine_info(self) -> Dict[str, Any]:
        """
        Retorna información del motor 3D.
        
        Returns:
            Dict con: name, version, capabilities
        """
        pass
    
    # ========================================================================
    # PRIMITIVAS
    # ========================================================================
    
    @abstractmethod
    def create_primitive(
        self, 
        primitive_type: Literal['cube', 'sphere', 'cylinder', 'cone', 'plane'],
        **params
    ) -> Dict[str, Any]:
        """
        Crea una primitiva geométrica.
        
        Args:
            primitive_type: Tipo de primitiva
            **params: location, scale, radius, etc.
        
        Returns:
            {
                'success': bool,
                'object_name': str,
                'location': [x, y, z],
                'error': str (opcional, código de EngineError)
            }
        """
        pass
    
    # ========================================================================
    # TRANSFORMACIONES
    # ========================================================================
    
    @abstractmethod
    def move_object(
        self, 
        object_name: Optional[str],
        location: Optional[List[float]] = None,
        offset: Optional[List[float]] = None
    ) -> Dict[str, Any]:
        """
        Mueve un objeto.
        
        Args:
            object_name: Nombre del objeto (None = activo)
            location: Posición absoluta [x, y, z]
            offset: Desplazamiento relativo [dx, dy, dz]
        
        Returns:
            {
                'success': bool,
                'object_name': str,
                'new_location': [x, y, z],
                'error': str (opcional)
            }
        """
        pass
    
    @abstractmethod
    def rotate_object(
        self,
        object_name: Optional[str],
        rotation: List[float],
        degrees: bool = False
    ) -> Dict[str, Any]:
        """
        Rota un objeto.
        
        Args:
            object_name: Nombre del objeto (None = activo)
            rotation: [x, y, z] en radianes (o grados si degrees=True)
            degrees: Si True, convierte de grados a radianes
        
        Returns:
            {
                'success': bool,
                'object_name': str,
                'rotation': [x, y, z],
                'error': str (opcional)
            }
        """
        pass
    
    @abstractmethod
    def scale_object(
        self,
        object_name: Optional[str],
        scale: float | List[float]
    ) -> Dict[str, Any]:
        """
        Escala un objeto.
        
        Args:
            object_name: Nombre del objeto (None = activo)
            scale: Escala uniforme (float) o por eje [x, y, z]
        
        Returns:
            {
                'success': bool,
                'object_name': str,
                'scale': [x, y, z],
                'error': str (opcional)
            }
        """
        pass
    
    # ========================================================================
    # ESCENA Y OBSERVACIÓN (Ajuste 3)
    # ========================================================================
    
    @abstractmethod
    def get_scene_state(self) -> Dict[str, Any]:
        """
        Retorna el estado completo de la escena.
        
        IMPORTANTE: Este método es usado por observadores (Ajuste 3).
        
        Returns:
            {
                'success': bool,
                'objects': [
                    {'name': str, 'type': str, 'location': [x,y,z], ...}
                ],
                'active_object': str,
                'collections': [...],
                'error': str (opcional)
            }
        """
        pass
    
    @abstractmethod
    def get_active_object(self) -> Optional[str]:
        """
        Retorna el nombre del objeto activo.
        
        Returns:
            str: Nombre del objeto activo, o None si no hay
        """
        pass
    
    @abstractmethod
    def get_object_info(self, object_name: str) -> Dict[str, Any]:
        """
        Retorna información detallada de un objeto.
        
        Args:
            object_name: Nombre del objeto
        
        Returns:
            {
                'success': bool,
                'name': str,
                'type': str,
                'location': [x, y, z],
                'rotation': [x, y, z],
                'scale': [x, y, z],
                'error': str (opcional)
            }
        """
        pass
    
    # ========================================================================
    # MATERIALES
    # ========================================================================
    
    @abstractmethod
    def create_material(self, name: str, **properties) -> Dict[str, Any]:
        """
        Crea un material.
        
        Args:
            name: Nombre del material
            **properties: color, metallic, roughness, etc.
        
        Returns:
            {
                'success': bool,
                'material_name': str,
                'error': str (opcional)
            }
        """
        pass
    
    @abstractmethod
    def apply_material(self, object_name: str, material_name: str) -> Dict[str, Any]:
        """
        Aplica un material a un objeto.
        
        Args:
            object_name: Nombre del objeto
            material_name: Nombre del material
        
        Returns:
            {
                'success': bool,
                'object_name': str,
                'material_name': str,
                'error': str (opcional)
            }
        """
        pass
    
    # ========================================================================
    # ILUMINACIÓN
    # ========================================================================
    
    @abstractmethod
    def create_light(
        self,
        light_type: Literal['POINT', 'SUN', 'SPOT', 'AREA'],
        **params
    ) -> Dict[str, Any]:
        """
        Crea una fuente de luz.
        
        Args:
            light_type: Tipo de luz
            **params: location, energy, color, etc.
        
        Returns:
            {
                'success': bool,
                'light_name': str,
                'type': str,
                'error': str (opcional)
            }
        """
        pass
    
    # ========================================================================
    # RENDER Y EXPORTACIÓN
    # ========================================================================
    
    @abstractmethod
    def render_scene(self, output_path: str, **settings) -> Dict[str, Any]:
        """
        Renderiza la escena.
        
        Args:
            output_path: Ruta de salida del render
            **settings: resolution, samples, engine, etc.
        
        Returns:
            {
                'success': bool,
                'output_path': str,
                'render_time': float (segundos),
                'error': str (opcional)
            }
        """
        pass
    
    @abstractmethod
    def export_scene(
        self,
        format: Literal['FBX', 'OBJ', 'GLTF', 'BLEND'],
        output_path: str,
        **options
    ) -> Dict[str, Any]:
        """
        Exporta la escena.
        
        Args:
            format: Formato de exportación
            output_path: Ruta de salida
            **options: Opciones específicas del formato
        
        Returns:
            {
                'success': bool,
                'output_path': str,
                'format': str,
                'error': str (opcional)
            }
        """
        pass
    
    # ========================================================================
    # CÁMARAS (FASE 17 CIERRE)
    # ========================================================================
    
    @abstractmethod
    def create_camera(self, **params) -> Dict[str, Any]:
        """Crea una cámara."""
        pass
    
    @abstractmethod
    def set_active_camera(self, camera_name: str) -> Dict[str, Any]:
        """Establece la cámara activa."""
        pass
    
    @abstractmethod
    def position_camera(self, camera_name: str, location: List[float], look_at: List[float]) -> Dict[str, Any]:
        """Posiciona una cámara mirando un punto."""
        pass
    
    # ========================================================================
    # MODIFICADORES (FASE 17 CIERRE)
    # ========================================================================
    
    @abstractmethod
    def add_modifier(self, object_name: str, modifier_type: str, **params) -> Dict[str, Any]:
        """Agrega un modificador a un objeto."""
        pass
    
    # ========================================================================
    # ACTUALIZACIONES DE LUZ Y MATERIAL (FASE 17 CIERRE)
    # ========================================================================
    
    @abstractmethod
    def update_light(self, light_name: str, **properties) -> Dict[str, Any]:
        """Actualiza propiedades de una luz existente."""
        pass
    
    @abstractmethod
    def update_material(self, material_name: str, **properties) -> Dict[str, Any]:
        """Actualiza propiedades de un material existente."""
        pass
    
    # ========================================================================
    # JERARQUÍA Y ENSAMBLAJE (FASE 19)
    # ========================================================================
    
    @abstractmethod
    def set_parent(
        self,
        child_name: str,
        parent_name: Optional[str] = None,
        keep_transform: bool = True
    ) -> Dict[str, Any]:
        """
        Establece relación parent/child entre objetos.
        
        Args:
            child_name: Nombre del objeto hijo
            parent_name: Nombre del objeto padre (None para desparentar)
            keep_transform: Si True, mantiene la transformación mundial del hijo
        
        Returns:
            {
                'success': bool,
                'child': str,
                'parent': Optional[str],
                'error': str (opcional)
            }
        """
        pass
    
    @abstractmethod
    def get_parent(self, object_name: str) -> Optional[str]:
        """
        Obtiene el nombre del objeto padre.
        
        Args:
            object_name: Nombre del objeto
        
        Returns:
            str: Nombre del padre, o None si no tiene
        """
        pass
    
    @abstractmethod
    def get_children(self, object_name: str) -> List[str]:
        """
        Obtiene la lista de objetos hijos.
        
        Args:
            object_name: Nombre del objeto
        
        Returns:
            List[str]: Nombres de los hijos
        """
        pass
    
    @abstractmethod
    def align_objects(
        self,
        target_name: str,
        reference_name: str,
        mode: Literal['center', 'top', 'bottom', 'left', 'right', 'front', 'back']
    ) -> Dict[str, Any]:
        """
        Alinea un objeto relativamente a otro.
        
        Args:
            target_name: Objeto a mover
            reference_name: Objeto de referencia
            mode: Tipo de alineación
        
        Returns:
            {
                'success': bool,
                'target': str,
                'reference': str,
                'new_location': [x, y, z],
                'error': str (opcional)
            }
        """
        pass

    # ========================================================================
    # GESTIÓN DE OBJETOS (ULTRA EMERGENCIA)
    # ========================================================================

    @abstractmethod
    def delete_object(self, object_name: str) -> Dict[str, Any]:
        """Borra un objeto."""
        pass

    @abstractmethod
    def duplicate_object(self, object_name: str, new_name: Optional[str] = None) -> Dict[str, Any]:
        """Duplica un objeto."""
        pass

    @abstractmethod
    def select_object(self, object_name: str) -> Dict[str, Any]:
        """Selecciona un objeto."""
        pass

    @abstractmethod
    def deselect_all(self) -> Dict[str, Any]:
        """Deselecciona todos los objetos."""
        pass

    @abstractmethod
    def select_all_by_type(self, type_name: str) -> Dict[str, Any]:
        """Selecciona todos los objetos de un tipo."""
        pass

    @abstractmethod
    def rename_object(self, old_name: str, new_name: str) -> Dict[str, Any]:
        """Renombra un objeto."""
        pass
    
    # ========================================================================
    # UTILIDADES DE ERROR (Ajuste 2)
    # ========================================================================
    
    def _error_response(
        self,
        error_code: EngineError,
        message: str = "",
        **extra_data
    ) -> Dict[str, Any]:
        """
        Genera una respuesta de error estándar.
        
        Args:
            error_code: Código de error de EngineError
            message: Mensaje descriptivo adicional
            **extra_data: Datos adicionales para el contexto
        
        Returns:
            Dict con estructura estándar de error
        """
        response = {
            'success': False,
            'error': error_code.value if hasattr(error_code, 'value') else error_code,
            'message': message
        }
        response.update(extra_data)
        return response
    
    def _success_response(self, **data) -> Dict[str, Any]:
        """
        Genera una respuesta de éxito estándar.
        
        Args:
            **data: Datos de la respuesta
        
        Returns:
            Dict con success=True y los datos proporcionados
        """
        return {'success': True, **data}
