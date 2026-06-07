"""
core/adapters/mock_adapter.py

Implementación Mock del EngineAdapter para testing sin motor 3D real.

PROPÓSITO:
- Permitir que el core ejecute sin Blender instalado
- Facilitar tests unitarios rápidos
- Validar el contrato de EngineAdapter

CARACTERÍSTICAS:
- Stateless (Ajuste 1)
- Simula operaciones sin efectos reales
- Retorna respuestas válidas según el contrato
- Usa códigos de error estándar (Ajuste 2)
"""

from typing import Dict, Any, List, Optional, Literal
from core.adapters.engine_adapter import EngineAdapter, EngineError
from core.utils.logging import log_info, log_debug


class MockAdapter(EngineAdapter):
    """
    Adapter simulado para testing.
    
    REGLA: Este adapter NO mantiene estado de escena real.
    Simula operaciones y retorna respuestas válidas.
    """
    
    def __init__(self):
        """Inicializa el MockAdapter."""
        self._mock_objects = {}  # Simulación mínima de objetos
        self._active_object = None
        self._object_counter = 0
        self._hierarchy = {}  # FASE 19: parent/child tracking {child_name: parent_name}
        log_info("🔧 MockAdapter inicializado (modo simulación)")

    
    # ========================================================================
    # UTILIDADES Y ESTADO
    # ========================================================================
    
    def is_available(self) -> bool:
        """MockAdapter siempre está disponible."""
        return True
    
    def get_engine_info(self) -> Dict[str, Any]:
        """Retorna información del motor simulado."""
        return self._success_response(
            name="MockEngine",
            version="1.0.0",
            capabilities=[
                "primitives", "transforms", "materials",
                "lights", "render", "export"
            ]
        )
    
    # ========================================================================
    # PRIMITIVAS
    # ========================================================================
    
    def create_primitive(
        self,
        primitive_type: Literal['cube', 'sphere', 'cylinder', 'cone', 'plane'],
        **params
    ) -> Dict[str, Any]:
        """Simula la creación de una primitiva."""
        if primitive_type not in ['cube', 'sphere', 'cylinder', 'cone', 'plane']:
            return self._error_response(
                EngineError.INVALID_PARAMS,
                f"Tipo de primitiva no válido: {primitive_type}"
            )
        
        location = params.get('location', [0, 0, 0])
        scale = params.get('scale', 1.0)
        
        # --- FASE 18.5: Intención Dimensional ---
        dimension_intent = params.get('dimension_intent')
        if dimension_intent:
            val_m = dimension_intent.get('meters', 1.0)
            scale = val_m / 2.0 if primitive_type == 'cube' else val_m
        
        # Generar nombre único
        self._object_counter += 1
        default_name = f"{primitive_type.capitalize()}_{self._object_counter:03d}"
        object_name = params.get('name') or default_name
        
        # Simular objeto
        adapter_type = 'MESH' # Por defecto para primitivas
        if primitive_type == 'light': adapter_type = 'LIGHT'
        elif primitive_type == 'camera': adapter_type = 'CAMERA'
        
        # FIX: Asignar vertex_count correcto para cada primitivo
        vertex_counts = {
            'cube': 24,        # 8 vértices pero 24 con caras duplicadas
            'sphere': 482,     # ~482 vértices tipicamente
            'cylinder': 100,   # ~100 vértices
            'cone': 120,       # ~120 vértices
            'plane': 4         # 4 vértices
        }
        
        vertex_count = vertex_counts.get(primitive_type, 24)
        
        self._mock_objects[object_name] = {
            'type': adapter_type,
            'location': list(location),
            'rotation': [0, 0, 0],
            'scale': [scale, scale, scale] if isinstance(scale, (int, float)) else list(scale),
            'intended_dimension': dimension_intent,
            'vertex_count': params.get('vertex_count', vertex_count)  # FIX: vertex_count ahora correcto
        }
        self._active_object = object_name
        
        log_debug(f"🔧 Mock: Creada primitiva {primitive_type} → {object_name}")
        
        return self._success_response(
            object_name=object_name,
            location=list(location),
            scale=scale,
            message=f"{primitive_type.capitalize()} creado en modo simulación"
        )
    
    # ========================================================================
    # TRANSFORMACIONES
    # ========================================================================
    
    def move_object(
        self,
        object_name: Optional[str],
        location: Optional[List[float]] = None,
        offset: Optional[List[float]] = None
    ) -> Dict[str, Any]:
        """Simula el movimiento de un objeto."""
        # Determinar objeto target
        target = object_name or self._active_object
        
        if not target:
            return self._error_response(
                EngineError.OBJECT_NOT_FOUND,
                "No hay objeto activo seleccionado"
            )
        
        if target not in self._mock_objects:
            return self._error_response(
                EngineError.OBJECT_NOT_FOUND,
                f"Objeto '{target}' no encontrado"
            )
        
        # Aplicar transformación
        obj = self._mock_objects[target]
        if location:
            obj['location'] = list(location)
        elif offset:
            obj['location'] = [
                obj['location'][0] + offset[0],
                obj['location'][1] + offset[1],
                obj['location'][2] + offset[2]
            ]
        else:
            return self._error_response(
                EngineError.INVALID_PARAMS,
                "Debe proporcionar 'location' o 'offset'"
            )
        
        log_debug(f"🔧 Mock: Movido {target} → {obj['location']}")
        
        return self._success_response(
            object_name=target,
            new_location=obj['location'],
            message=f"Objeto movido a {obj['location']}"
        )
    
    def rotate_object(
        self,
        object_name: Optional[str],
        rotation: List[float],
        degrees: bool = False
    ) -> Dict[str, Any]:
        """Simula la rotación de un objeto."""
        import math
        
        target = object_name or self._active_object
        
        if not target or target not in self._mock_objects:
            return self._error_response(
                EngineError.OBJECT_NOT_FOUND,
                f"Objeto '{target}' no encontrado"
            )
        
        # Convertir grados a radianes si es necesario
        rot = list(rotation)
        if degrees:
            rot = [math.radians(r) for r in rot]
        
        self._mock_objects[target]['rotation'] = rot
        
        log_debug(f"🔧 Mock: Rotado {target} → {rot}")
        
        return self._success_response(
            object_name=target,
            rotation=rot,
            message="Objeto rotado en modo simulación"
        )
    
    def scale_object(
        self,
        object_name: Optional[str],
        scale: float | List[float]
    ) -> Dict[str, Any]:
        """Simula el escalado de un objeto."""
        target = object_name or self._active_object
        
        if not target or target not in self._mock_objects:
            return self._error_response(
                EngineError.OBJECT_NOT_FOUND,
                f"Objeto '{target}' no encontrado"
            )
        
        # Aplicar escala
        if isinstance(scale, (list, tuple)):
            self._mock_objects[target]['scale'] = list(scale)
        else:
            self._mock_objects[target]['scale'] = [scale, scale, scale]
        
        log_debug(f"🔧 Mock: Escalado {target} → {self._mock_objects[target]['scale']}")
        
        return self._success_response(
            object_name=target,
            scale=self._mock_objects[target]['scale'],
            message="Objeto escalado en modo simulación"
        )
    
    # ========================================================================
    # ESCENA Y OBSERVACIÓN
    # ========================================================================
    
    def get_scene_state(self) -> Dict[str, Any]:
        """Retorna el estado simulado de la escena."""
        objects = [
            {
                'name': name,
                'type': data['type'],
                'location': data['location'],
                'rotation': data['rotation'],
                'scale': data['scale'],
                'parent': self.get_parent(name),
                'vertex_count': data.get('vertex_count', 0),
                'intended_dimension': data.get('intended_dimension')
            }
            for name, data in self._mock_objects.items()
        ]
        
        return self._success_response(
            objects=objects,
            active_object=self._active_object,
            object_count=len(objects),
            collections=[],
            message="Estado de escena simulado"
        )
    
    def clear_scene(self) -> Dict[str, Any]:
        """Borra todos los objetos del estado simulado."""
        self._mock_objects = {}
        self._active_object = None
        self._object_counter = 0
        self._hierarchy = {}
        log_info("🔧 Mock: Escena limpiada")
        return self._success_response()
    
    def get_active_object(self) -> Optional[str]:
        """Retorna el objeto activo simulado."""
        return self._active_object
    
    def get_object_info(self, object_name: str) -> Dict[str, Any]:
        """Retorna información de un objeto simulado."""
        if object_name not in self._mock_objects:
            return self._error_response(
                EngineError.OBJECT_NOT_FOUND,
                f"Objeto '{object_name}' no encontrado"
            )
        
        data = self._mock_objects[object_name]
        return self._success_response(
            name=object_name,
            type=data['type'],
            location=data['location'],
            rotation=data['rotation'],
            scale=data['scale']
        )
    
    def get_object(self, object_name: str) -> Dict[str, Any]:
        """Alias para get_object_info - compatibilidad con VisualConfirmation."""
        return self.get_object_info(object_name)
    
    # ========================================================================
    # MATERIALES
    # ========================================================================
    
    def create_material(self, name: str, **properties) -> Dict[str, Any]:
        """Simula la creación de un material."""
        log_debug(f"🔧 Mock: Material creado → {name}")
        return self._success_response(
            material_name=name,
            properties=properties,
            message=f"Material '{name}' creado en modo simulación"
        )
    
    def create_texture_material(self, name: str, image_path: str, **properties) -> Dict[str, Any]:
        """Simula la creación de un material con textura de imagen."""
        log_debug(f"🔧 Mock: Material de textura creado → {name} (Imagen: {image_path})")
        return self._success_response(
            material_name=name,
            image_path=image_path,
            properties=properties,
            message=f"Material de textura '{name}' creado en modo simulación"
        )
    
    def apply_material(self, object_name: str, material_name: str) -> Dict[str, Any]:
        """Simula la aplicación de un material."""
        if object_name not in self._mock_objects:
            return self._error_response(
                EngineError.OBJECT_NOT_FOUND,
                f"Objeto '{object_name}' no encontrado"
            )
        
        log_debug(f"🔧 Mock: Material '{material_name}' aplicado a '{object_name}'")
        return self._success_response(
            object_name=object_name,
            material_name=material_name,
            message=f"Material aplicado en modo simulación"
        )
    
    # ========================================================================
    # ILUMINACIÓN
    # ========================================================================
    
    def create_light(
        self,
        light_type: Literal['POINT', 'SUN', 'SPOT', 'AREA'],
        **params
    ) -> Dict[str, Any]:
        """Simula la creación de una luz."""
        self._object_counter += 1
        default_name = f"Light_{light_type}_{self._object_counter:03d}"
        light_name = params.get('name', default_name)
        
        # Guardar en mock_objects para que update_light pueda encontrarla
        self._mock_objects[light_name] = {
            'type': 'LIGHT',
            'light_type': light_type,
            'location': list(params.get('location', [0, 0, 5])),
            'rotation': [0, 0, 0],
            'scale': [1, 1, 1],
            'energy': params.get('energy', 1.0),
            'color': params.get('color', [1.0, 1.0, 1.0])
        }
        
        log_debug(f"🔧 Mock: Luz creada → {light_name} ({light_type})")
        
        return self._success_response(
            light_name=light_name,
            type=light_type,
            location=params.get('location', [0, 0, 5]),
            energy=params.get('energy', 1.0),
            message=f"Luz {light_type} creada en modo simulación"
        )
    
    # ========================================================================
    # RENDER Y EXPORTACIÓN
    # ========================================================================
    
    def render_scene(self, output_path: str, **settings) -> Dict[str, Any]:
        """Simula el renderizado de la escena."""
        log_info(f"🔧 Mock: Render simulado → {output_path}")
        
        return self._success_response(
            output_path=output_path,
            render_time=0.1,  # Simulado instantáneo
            resolution=settings.get('resolution', [1920, 1080]),
            samples=settings.get('samples', 128),
            message="Render completado en modo simulación"
        )
    
    def export_scene(
        self,
        format: Literal['FBX', 'OBJ', 'GLTF', 'BLEND'],
        output_path: str,
        **options
    ) -> Dict[str, Any]:
        """Simula la exportación de la escena."""
        log_info(f"🔧 Mock: Exportación simulada → {output_path} ({format})")
        
        return self._success_response(
            output_path=output_path,
            format=format,
            object_count=len(self._mock_objects),
            message=f"Escena exportada a {format} en modo simulación"
        )
    
    # ========================================================================
    # CÁMARAS (FASE 17 CIERRE)
    # ========================================================================
    
    def create_camera(self, **params) -> Dict[str, Any]:
        """Simula la creación de una cámara."""
        self._object_counter += 1
        name = params.get('name', f'Camera_{self._object_counter:03d}')
        location = params.get('location', [10, -10, 5])
        
        self._mock_objects[name] = {
            'type': 'CAMERA',
            'location': list(location),
            'rotation': [0, 0, 0],
            'scale': [1, 1, 1]
        }
        
        log_debug(f"🔧 Mock: Cámara creada → {name}")
        return self._success_response(camera_name=name, location=location)
    
    def set_active_camera(self, camera_name: str) -> Dict[str, Any]:
        """Simula establecer cámara activa."""
        if camera_name not in self._mock_objects:
            return self._error_response(EngineError.OBJECT_NOT_FOUND, f"Cámara {camera_name} no encontrada")
        
        log_debug(f"🔧 Mock: Cámara activa → {camera_name}")
        return self._success_response(camera_name=camera_name)
    
    def position_camera(self, camera_name: str, location: List[float], look_at: List[float]) -> Dict[str, Any]:
        """Simula posicionar una cámara."""
        if camera_name not in self._mock_objects:
            return self._error_response(EngineError.OBJECT_NOT_FOUND, f"Cámara {camera_name} no encontrada")
        
        self._mock_objects[camera_name]['location'] = list(location)
        log_debug(f"🔧 Mock: Cámara posicionada → {camera_name}")
        return self._success_response(camera_name=camera_name, location=location, look_at=look_at)
    
    # ========================================================================
    # MODIFICADORES (FASE 17 CIERRE)
    # ========================================================================
    
    def add_modifier(self, object_name: str, modifier_type: str, **params) -> Dict[str, Any]:
        """Simula agregar un modificador."""
        if object_name not in self._mock_objects:
            return self._error_response(EngineError.OBJECT_NOT_FOUND, f"Objeto {object_name} no encontrado")
        
        stack = self._mock_objects[object_name].setdefault('_modifier_stack', [])
        stack.append(f"{modifier_type}_{len(stack)}")
        log_debug(f"🔧 Mock: Modificador {modifier_type} agregado a {object_name}")
        return self._success_response(object_name=object_name, modifier_type=modifier_type)

    def validate_mesh_topology(self, object_name: str) -> Dict[str, Any]:
        """Simula auditoría de malla (V3 / bmesh) con métricas sanas."""
        if object_name not in self._mock_objects:
            return self._error_response(
                EngineError.OBJECT_NOT_FOUND,
                f"Objeto '{object_name}' no encontrado",
            )
        metrics = {
            "is_watertight": True,
            "non_manifold_edges_count": 0,
            "loose_vertices_count": 0,
            "zero_area_faces_count": 0,
            "total_vertices": 8,
            "total_edges": 12,
            "total_faces": 6,
        }
        return self._success_response(object_name=object_name, metrics=metrics)

    def apply_modifier(
        self,
        object_name: str,
        modifier_name: str = None,
        *,
        apply_last: bool = False,
    ) -> Dict[str, Any]:
        """Simula aplicar un modificador (stack mock simplificado)."""
        if object_name not in self._mock_objects:
            return self._error_response(EngineError.OBJECT_NOT_FOUND, f"Objeto {object_name} no encontrado")
        stack = self._mock_objects[object_name].setdefault('_modifier_stack', [])
        if not stack:
            return self._error_response(EngineError.INVALID_PARAMS, "No hay modificadores para aplicar")
        if modifier_name:
            try:
                stack.remove(modifier_name)
                popped = modifier_name
            except ValueError:
                return self._error_response(EngineError.INVALID_PARAMS, f"Modificador {modifier_name!r} no en pila mock")
        elif apply_last:
            popped = stack.pop()
        else:
            popped = stack.pop(0)
        log_debug(f"🔧 Mock: apply_modifier {popped!r} en {object_name}")
        return self._success_response(object_name=object_name, modifier_applied=popped)
    
    # ========================================================================
    # ACTUALIZACIONES (FASE 17 CIERRE)
    # ========================================================================
    
    def update_light(self, light_name: str, **properties) -> Dict[str, Any]:
        """Simula actualizar una luz."""
        if light_name not in self._mock_objects:
            return self._error_response(EngineError.OBJECT_NOT_FOUND, f"Luz {light_name} no encontrada")
        
        log_debug(f"🔧 Mock: Luz actualizada → {light_name}")
        return self._success_response(light_name=light_name, **properties)
    
    def update_material(self, material_name: str, **properties) -> Dict[str, Any]:
        """Simula actualizar un material."""
        log_debug(f"🔧 Mock: Material actualizado → {material_name}")
        return self._success_response(material_name=material_name, **properties)
    
    # ========================================================================
    # JERARQUÍA Y ENSAMBLAJE (FASE 19)
    # ========================================================================
    
    def set_parent(
        self,
        child_name: str,
        parent_name: Optional[str] = None,
        keep_transform: bool = True
    ) -> Dict[str, Any]:
        """Simula establecer relación parent/child."""
        # Verificar que el hijo existe
        if child_name not in self._mock_objects:
            return self._error_response(
                EngineError.OBJECT_NOT_FOUND,
                f"Objeto hijo '{child_name}' no encontrado"
            )
        
        # Si hay padre, verificar que existe
        if parent_name is not None:
            if parent_name not in self._mock_objects:
                return self._error_response(
                    EngineError.OBJECT_NOT_FOUND,
                    f"Objeto padre '{parent_name}' no encontrado"
                )
            
            # Prevenir ciclos (A parent de B, B parent de A)
            temp_parent = parent_name
            while temp_parent:
                if temp_parent == child_name:
                    return self._error_response(
                        EngineError.INVALID_PARAMS,
                        f"Ciclo detectado: '{child_name}' no puede ser padre de su ancestro '{parent_name}'"
                    )
                temp_parent = self._hierarchy.get(temp_parent)
            
            # Establecer relación
            self._hierarchy[child_name] = parent_name
            log_debug(f"🔧 Mock: Parentado → {child_name} → {parent_name}")
        else:
            # Desparentar
            if child_name in self._hierarchy:
                del self._hierarchy[child_name]
                log_debug(f"🔧 Mock: Desparentado → {child_name}")
        
        return self._success_response(
            child=child_name,
            parent=parent_name,
            message=f"Relación parent/child {'establecida' if parent_name else 'removida'}"
        )
    
    def get_parent(self, object_name: str) -> Optional[str]:
        """Obtiene el nombre del padre simulado."""
        if object_name not in self._mock_objects:
            return None
        return self._hierarchy.get(object_name)
    
    def get_children(self, object_name: str) -> List[str]:
        """Obtiene la lista de hijos simulados."""
        if object_name not in self._mock_objects:
            return []
        
        return [
            child for child, parent in self._hierarchy.items()
            if parent == object_name
        ]
    
    def align_objects(
        self,
        target_name: str,
        reference_name: str,
        mode: Literal['center', 'top', 'bottom', 'left', 'right', 'front', 'back']
    ) -> Dict[str, Any]:
        """Simula alineación de objetos."""
        # Verificar que ambos objetos existen
        if target_name not in self._mock_objects:
            return self._error_response(
                EngineError.OBJECT_NOT_FOUND,
                f"Objeto target '{target_name}' no encontrado"
            )
        
        if reference_name not in self._mock_objects:
            return self._error_response(
                EngineError.OBJECT_NOT_FOUND,
                f"Objeto reference '{reference_name}' no encontrado"
            )
        
        target = self._mock_objects[target_name]
        reference = self._mock_objects[reference_name]
        
        # Calcular dimensiones basadas en scale
        target_dims = target['scale']
        ref_dims = reference['scale']
        ref_loc = reference['location']
        
        # Calcular nueva posición según modo
        new_location = list(target['location'])
        
        if mode == 'center':
            new_location = list(ref_loc)
        elif mode == 'top':
            new_location[2] = ref_loc[2] + ref_dims[2] / 2 + target_dims[2] / 2
            new_location[0] = ref_loc[0]
            new_location[1] = ref_loc[1]
        elif mode == 'bottom':
            new_location[2] = ref_loc[2] - ref_dims[2] / 2 - target_dims[2] / 2
            new_location[0] = ref_loc[0]
            new_location[1] = ref_loc[1]
        elif mode == 'left':
            new_location[0] = ref_loc[0] - ref_dims[0] / 2 - target_dims[0] / 2
            new_location[1] = ref_loc[1]
        elif mode == 'right':
            new_location[0] = ref_loc[0] + ref_dims[0] / 2 + target_dims[0] / 2
            new_location[1] = ref_loc[1]
        elif mode == 'front':
            new_location[1] = ref_loc[1] + ref_dims[1] / 2 + target_dims[1] / 2
            new_location[0] = ref_loc[0]
        elif mode == 'back':
            new_location[1] = ref_loc[1] - ref_dims[1] / 2 - target_dims[1] / 2
            new_location[0] = ref_loc[0]
        
        # Actualizar ubicación
        target['location'] = new_location
        
        log_debug(f"🔧 Mock: Alineado {target_name} → {reference_name} ({mode})")
        
        return self._success_response(
            target=target_name,
            reference=reference_name,
            new_location=new_location,
            mode=mode,
            message=f"Objeto alineado {mode} con {reference_name}"
        )

    # ========================================================================
    # GESTIÓN DE OBJETOS (ULTRA EMERGENCIA)
    # ========================================================================

    def delete_object(self, object_name: str) -> Dict[str, Any]:
        """Borra un objeto del estado simulado."""
        if object_name not in self._mock_objects:
            return self._error_response(
                EngineError.OBJECT_NOT_FOUND,
                f"Objeto '{object_name}' no encontrado"
            )
        
        del self._mock_objects[object_name]
        
        # Limpiar jerarquía
        if object_name in self._hierarchy:
            del self._hierarchy[object_name]
        
        # Si era el activo, poner a None
        if self._active_object == object_name:
            self._active_object = None
            
        log_debug(f"🔧 Mock: Objeto '{object_name}' eliminado")
        return self._success_response(message=f"Objeto '{object_name}' eliminado")

    def duplicate_object(self, object_name: str, new_name: Optional[str] = None) -> Dict[str, Any]:
        """Duplica un objeto en el estado simulado."""
        if object_name not in self._mock_objects:
            return self._error_response(
                EngineError.OBJECT_NOT_FOUND,
                f"Objeto '{object_name}' no encontrado"
            )
        
        # Crear copia
        self._object_counter += 1
        name = new_name or f"{object_name}_copy_{self._object_counter:03d}"
        
        self._mock_objects[name] = self._mock_objects[object_name].copy()
        # Las listas deben ser copiadas para no compartir referencia
        self._mock_objects[name]['location'] = list(self._mock_objects[name]['location'])
        self._mock_objects[name]['rotation'] = list(self._mock_objects[name]['rotation'])
        self._mock_objects[name]['scale'] = list(self._mock_objects[name]['scale'])
        
        self._active_object = name
        
        log_debug(f"🔧 Mock: Objeto '{object_name}' duplicado como '{name}'")
        return self._success_response(object_name=name, message=f"Objeto duplicado como '{name}'")

    def select_object(self, object_name: str) -> Dict[str, Any]:
        """Simula la selección de un objeto."""
        if object_name not in self._mock_objects:
            return self._error_response(
                EngineError.OBJECT_NOT_FOUND,
                f"Objeto '{object_name}' no encontrado"
            )
        
        self._active_object = object_name
        log_debug(f"🔧 Mock: Objeto '{object_name}' seleccionado")
        return self._success_response(object_name=object_name)

    def deselect_all(self) -> Dict[str, Any]:
        """Simula la deselección de todos los objetos."""
        self._active_object = None
        log_debug("🔧 Mock: Todos los objetos deseleccionados")
        return self._success_response()

    def select_all_by_type(self, type_name: str) -> Dict[str, Any]:
        """Simula la selección por tipo (solo loggea en mock)."""
        log_debug(f"🔧 Mock: Seleccionados todos los objetos tipo '{type_name}'")
        return self._success_response(type=type_name)

    def rename_object(self, old_name: str, new_name: str) -> Dict[str, Any]:
        """Renombra un objeto en el estado simulado."""
        if old_name not in self._mock_objects:
            return self._error_response(
                EngineError.OBJECT_NOT_FOUND,
                f"Objeto '{old_name}' no encontrado"
            )
            
        if new_name in self._mock_objects:
            return self._error_response(
                EngineError.INVALID_PARAMS,
                f"Ya existe un objeto con el nombre '{new_name}'"
            )
            
        # Mover datos
        self._mock_objects[new_name] = self._mock_objects.pop(old_name)
        
        # Actualizar jerarquía como hijo
        if old_name in self._hierarchy:
            self._hierarchy[new_name] = self._hierarchy.pop(old_name)
            
        # Actualizar jerarquía como padre
        for child, parent in self._hierarchy.items():
            if parent == old_name:
                self._hierarchy[child] = new_name
                
        # Actualizar objeto activo
        if self._active_object == old_name:
            self._active_object = new_name
            
        log_debug(f"🔧 Mock: Objeto '{old_name}' renombrado a '{new_name}'")
        return self._success_response(old_name=old_name, new_name=new_name)

