"""
core/adapters/blender_adapter.py

Implementación concreta de EngineAdapter para Blender.
ÚNICO módulo que conoce la API de Blender (bpy).

FASE 17: Desacoplamiento Estratégico
"""

from typing import Dict, Any, List, Optional, Literal, Union
import math
import os
import sys
from pathlib import Path
from core.adapters.engine_adapter import EngineAdapter, EngineError
from core.utils.logging import log_info, log_debug, log_warning, log_error
from core.utils.units import format_real_unit


class BlenderAdapter(EngineAdapter):
    """
    Adapter que encapsula TODAS las interacciones con Blender.
    
    REGLAS:
    1. Import condicional de bpy (no falla si Blender no está disponible)
    2. Único punto de contacto con la API de Blender
    3. Convierte datos de Blender a formato estándar del adapter
    4. Manejo robusto de errores
    """
    
    @staticmethod
    def _load_blender_from_config():
        """Intenta cargar bpy desde la ruta configurada en .env.blender."""
        try:
            from core.environment.blender_config import BlenderConfig
            blender_path = BlenderConfig.get_blender_path()
            
            if not blender_path:
                return None
            
            # Obtener el directorio de la instalación de Blender
            blender_dir = str(Path(blender_path).parent)
            blender_python_path = Path(blender_dir) / "3.6" / "site-packages"
            
            # Agregar a sys.path si existe
            if blender_python_path.exists():
                if str(blender_python_path) not in sys.path:
                    sys.path.insert(0, str(blender_python_path))
                log_info(f"✓ Añadido path de Blender a sys.path: {blender_python_path}")
            
            # Intentar importar bpy
            try:
                import bpy
                log_info(f"✅ Blender cargado desde: {blender_path}")
                return bpy
            except ImportError:
                log_warning(f"⚠️ No se pudo importar bpy desde {blender_python_path}")
                return None
                
        except Exception as e:
            log_debug(f"Error al intentar cargar desde configuración: {e}")
            return None
    
    def __init__(self, bpy_module=None):
        """Inicializa el BlenderAdapter con detección automática o inyección de bpy."""
        self._bpy = bpy_module
        self._available = bpy_module is not None
        
        if not self._available:
            # Intentar cargar desde configuración primero
            self._bpy = self._load_blender_from_config()
            if self._bpy is not None:
                self._available = True
                log_info("✓ BlenderAdapter inicializado correctamente (Desde configuración)")
            else:
                # Fallback: intentar detección automática
                try:
                    import bpy
                    self._bpy = bpy
                    self._available = True
                    log_info("✓ BlenderAdapter inicializado correctamente (Auto-detección)")
                except ImportError:
                    log_warning("⚠️ BlenderAdapter: bpy no disponible (Blender no detectado)")
                except Exception as e:
                    log_error(f"❌ Error inicializando BlenderAdapter: {e}")
        else:
            log_info("✓ BlenderAdapter inicializado correctamente (Inyección directa)")
    
    # ========================================================================
    # UTILIDADES Y ESTADO
    # ========================================================================
    
    def is_available(self) -> bool:
        """Verifica si Blender está disponible."""
        return self._available and self._bpy is not None
    
    def get_engine_info(self) -> Dict[str, Any]:
        """Retorna información del motor Blender."""
        if not self.is_available():
            return self._error_response(
                EngineError.ENGINE_NOT_AVAILABLE,
                "Blender no está disponible"
            )
        
        try:
            return self._success_response(
                name="Blender",
                version=".".join(map(str, self._bpy.app.version)),
                version_string=self._bpy.app.version_string,
                build_date=self._bpy.app.build_date.decode() if isinstance(
                    self._bpy.app.build_date, bytes
                ) else self._bpy.app.build_date,
                capabilities=[
                    "primitives", "transforms", "materials",
                    "lights", "cameras", "modifiers",
                    "render", "export", "collections"
                ],
                is_background=getattr(self._bpy.app, 'background', False)
            )
        except Exception as e:
            return self._error_response(
                EngineError.OPERATION_FAILED,
                f"Error obteniendo info del motor: {e}"
            )
            
    def _find_object(self, name: str) -> Optional[Any]:
        """Busca un objeto por nombre de forma insensible a mayúsculas."""
        if not self.is_available() or not name:
            return None
        
        # Primero intento exacto
        if name in self._bpy.data.objects:
            return self._bpy.data.objects[name]
            
        # Luego búsqueda insensible
        name_lower = name.lower()
        for obj in self._bpy.data.objects:
            if obj.name.lower() == name_lower:
                return obj
        
        return None

    def get_object(self, name: str) -> Optional[Any]:
        """Retorna el objeto real de Blender (para uso avanzado en scripts de assets)."""
        return self._find_object(name)

    def set_dimensions(self, name: str, dimensions: List[float]) -> Dict[str, Any]:
        """Establece las dimensiones (ancho, largo, alto) de un objeto."""
        obj = self._find_object(name)
        if not obj:
            return self._error_response(EngineError.OBJECT_NOT_FOUND)
        try:
            obj.dimensions = dimensions
            return self._success_response(name=name, dimensions=dimensions)
        except Exception as e:
            return self._error_response(EngineError.OPERATION_FAILED, f"Error set_dimensions: {e}")

    def set_rotation(self, name: str, rotation: List[float], mode: str = 'XYZ') -> Dict[str, Any]:
        """Establece la rotación Euler de un objeto."""
        obj = self._find_object(name)
        if not obj:
            return self._error_response(EngineError.OBJECT_NOT_FOUND)
        try:
            obj.rotation_euler = rotation
            return self._success_response(name=name, rotation=rotation)
        except Exception as e:
            return self._error_response(EngineError.OPERATION_FAILED, f"Error set_rotation: {e}")
    
    # ========================================================================
    # PRIMITIVAS
    # ========================================================================
    
    def create_primitive(
        self,
        primitive_type: Literal['cube', 'sphere', 'cylinder', 'cone', 'plane'],
        **params
    ) -> Dict[str, Any]:
        """Crea una primitiva geométrica en Blender."""
        if not self.is_available():
            return self._error_response(
                EngineError.ENGINE_NOT_AVAILABLE,
                "Blender no está disponible"
            )
        
        try:
            location = params.get('location', [0, 0, 0])
            scale = params.get('scale', 1.0)
            radius = params.get('radius', 1.0)
            
            # --- FASE 18.5: Intención Dimensional ---
            dimension_intent = params.get('dimension_intent')
            if dimension_intent:
                # Si hay intención dimensional, sobreescribimos scale/radius
                # En Blender, el 'size' de un cubo es el lado total.
                # 'radius' de una esfera/cilindro es el radio.
                val_m = dimension_intent.get('meters', 1.0)
                scale = val_m / 2.0  # El scale usualmente se refiere al radio en primitivas
                radius = val_m
                log_info(f"📏 Aplicando dimensión real: {val_m}m ({dimension_intent.get('original_value')}{dimension_intent.get('original_unit')})")
            
            # Preparar parámetros de escala y tamaño
            bpy_scale = (1.0, 1.0, 1.0)
            bpy_size = 2.0  # Tamaño base por defecto (radio 1)
            
            if isinstance(scale, (list, tuple)) and len(scale) == 3:
                bpy_scale = tuple(scale)
                # primitive_cube_add usa scale, pero primitive_cylinder/cone usan radius/depth
                # Para cubo: size=2 (radio 1) * scale
            else:
                # Escalar escalar
                val = float(scale)
                bpy_scale = (val, val, val)
                # Para compatibilidad con lógica anterior de radius/depth
                radius = val if radius == 1.0 else radius
            
            log_debug(f"Operator call: {primitive_type}, loc={location}, scale={bpy_scale}")
            # Crear primitiva según tipo
            loc_tup = tuple(location)
            scale_tup = tuple(bpy_scale)
            
            # Crear primitiva con parámetros base (Evitar errores de tipo en operadores específicos)
            if primitive_type == 'cube':
                self._bpy.ops.mesh.primitive_cube_add()
            elif primitive_type == 'sphere':
                self._bpy.ops.mesh.primitive_uv_sphere_add(radius=radius)
            elif primitive_type == 'cylinder':
                self._bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=2.0)
            elif primitive_type == 'cone':
                self._bpy.ops.mesh.primitive_cone_add(radius1=radius, radius2=0, depth=2.0)
            elif primitive_type == 'plane':
                self._bpy.ops.mesh.primitive_plane_add(size=2.0)
            else:
                return self._error_response(EngineError.INVALID_PARAMS, f"Tipo inválido: {primitive_type}")
            
            # Obtener objeto creado
            obj = self._bpy.context.active_object
            if not obj:
                 return self._error_response(EngineError.OPERATION_FAILED, "No se pudo obtener el objeto creado")
            
            # Aplicar transformaciones manualmente (lo más robusto posible)
            obj.location = loc_tup
            obj.scale = scale_tup
            
            # Renombrar si se solicita
            if params.get('name'):
                obj.name = params['name']
            
            object_name = obj.name
            
            # Emparentar si se solicita (Fase 18.5: Consistencia de jerarquía)
            parent_name = params.get('parent')
            if parent_name and parent_name in self._bpy.data.objects:
                parent_obj = self._bpy.data.objects[parent_name]
                obj.parent = parent_obj
                log_info(f"🔗 Emparentado {object_name} -> {parent_name}")
            elif parent_name:
                log_warning(f"⚠️ No se pudo emparentar: Padre '{parent_name}' no encontrado")
            
            # --- FASE 18.5: Guardar Metadata Dimensional ---
            if dimension_intent:
                obj["zuly_intended_value"] = dimension_intent.get('value')
                obj["zuly_intended_unit"] = dimension_intent.get('unit')
                obj["zuly_intended_meters"] = dimension_intent.get('meters')
            
            log_debug(f"✓ Primitiva creada: {primitive_type} → {object_name}")
            
            return self._success_response(
                object_name=object_name,
                location=list(location),
                scale=scale,
                primitive_type=primitive_type
            )
            
        except Exception as e:
            import traceback
            error_msg = f"Error creando primitiva {primitive_type}: {e}\n{traceback.format_exc()}"
            log_error(error_msg)
            # Retornar el mensaje de error directamente para verlo en el reporte
            return self._error_response(
                str(e), 
                error_msg
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
        """Mueve un objeto en Blender."""
        if not self.is_available():
            return self._error_response(
                EngineError.ENGINE_NOT_AVAILABLE,
                "Blender no está disponible"
            )
        
        try:
            # Determinar objeto target
            if object_name:
                obj = self._find_object(object_name)
                if not obj:
                    return self._error_response(
                        EngineError.OBJECT_NOT_FOUND,
                        f"Objeto '{object_name}' no encontrado"
                    )
                object_name = obj.name
            else:
                obj = self._bpy.context.active_object
                if not obj:
                    return self._error_response(
                        EngineError.OBJECT_NOT_FOUND,
                        "No hay objeto activo seleccionado"
                    )
                object_name = obj.name
            
            # Aplicar transformación
            if location is not None:
                obj.location = location
            elif offset is not None:
                obj.location[0] += offset[0]
                obj.location[1] += offset[1]
                obj.location[2] += offset[2]
            else:
                return self._error_response(
                    EngineError.INVALID_PARAMS,
                    "Debe proporcionar 'location' o 'offset'"
                )
            
            new_location = list(obj.location)
            log_debug(f"✓ Objeto movido: {object_name} → {new_location}")
            
            return self._success_response(
                object_name=object_name,
                new_location=new_location
            )
            
        except Exception as e:
            return self._error_response(
                EngineError.OPERATION_FAILED,
                f"Error moviendo objeto: {e}"
            )
    
    def rotate_object(
        self,
        object_name: Optional[str],
        rotation: List[float],
        degrees: bool = False
    ) -> Dict[str, Any]:
        """Rota un objeto en Blender."""
        if not self.is_available():
            return self._error_response(
                EngineError.ENGINE_NOT_AVAILABLE,
                "Blender no está disponible"
            )
        
        try:
            # Determinar objeto target
            if object_name:
                obj = self._find_object(object_name)
                if not obj:
                    return self._error_response(
                        EngineError.OBJECT_NOT_FOUND,
                        f"Objeto '{object_name}' no encontrado"
                    )
                object_name = obj.name
            else:
                obj = self._bpy.context.active_object
                if not obj:
                    return self._error_response(
                        EngineError.OBJECT_NOT_FOUND,
                        "No hay objeto activo seleccionado"
                    )
                object_name = obj.name
            
            # Convertir grados a radianes si es necesario
            rot = list(rotation)
            if degrees:
                rot = [math.radians(r) for r in rot]
            
            # Aplicar rotación
            obj.rotation_euler = rot
            
            log_debug(f"✓ Objeto rotado: {object_name} → {rot}")
            
            return self._success_response(
                object_name=object_name,
                rotation=rot
            )
            
        except Exception as e:
            return self._error_response(
                EngineError.OPERATION_FAILED,
                f"Error rotando objeto: {e}"
            )
    
    def scale_object(
        self,
        object_name: Optional[str],
        scale: float | List[float]
    ) -> Dict[str, Any]:
        """Escala un objeto en Blender."""
        if not self.is_available():
            return self._error_response(
                EngineError.ENGINE_NOT_AVAILABLE,
                "Blender no está disponible"
            )
        
        try:
            # Determinar objeto target
            if object_name:
                obj = self._find_object(object_name)
                if not obj:
                    return self._error_response(
                        EngineError.OBJECT_NOT_FOUND,
                        f"Objeto '{object_name}' no encontrado"
                    )
                object_name = obj.name
            else:
                obj = self._bpy.context.active_object
                if not obj:
                    return self._error_response(
                        EngineError.OBJECT_NOT_FOUND,
                        "No hay objeto activo seleccionado"
                    )
                object_name = obj.name
            
            # Aplicar escala
            if isinstance(scale, (list, tuple)):
                obj.scale = scale
            else:
                obj.scale = [scale, scale, scale]
            
            new_scale = list(obj.scale)
            log_debug(f"✓ Objeto escalado: {object_name} → {new_scale}")
            
            return self._success_response(
                object_name=object_name,
                scale=new_scale
            )
            
        except Exception as e:
            return self._error_response(
                EngineError.OPERATION_FAILED,
                f"Error escalando objeto: {e}"
            )
    
    # ========================================================================
    # ESCENA Y OBSERVACIÓN
    # ========================================================================
    
    def get_scene_state(self) -> Dict[str, Any]:
        """Retorna el estado completo de la escena en Blender."""
        if not self.is_available():
            return self._error_response(
                EngineError.ENGINE_NOT_AVAILABLE,
                "Blender no está disponible"
            )
        
        try:
            objects = []
            for obj in self._bpy.data.objects:
                objects.append({
                    'name': obj.name,
                    'type': obj.type,
                    'location': list(obj.location),
                    'rotation': list(obj.rotation_euler),
                    'scale': list(obj.scale),
                    'collection': obj.users_collection[0].name if obj.users_collection else "Scene Collection",
                    'visible': not obj.hide_viewport,
                    'parent': obj.parent.name if obj.parent else None,
                    'vertex_count': len(obj.data.vertices) if obj.type == 'MESH' else 0,
                    # --- FASE 18.5: Recuperar Metadata Dimensional ---
                    'intended_dimension': {
                        'value': obj.get("zuly_intended_value"),
                        'unit': obj.get("zuly_intended_unit"),
                        'meters': obj.get("zuly_intended_meters")
                    } if "zuly_intended_value" in obj else None
                })
            
            active_obj = self._bpy.context.active_object
            active_name = active_obj.name if active_obj else None
            
            # Obtener colecciones
            collections = self._get_collections_hierarchy()
            
            # Obtener el modo real de Blender
            active_mode = "OBJECT"
            try:
                active_mode = self._bpy.context.mode
            except:
                pass

            return self._success_response(
                objects=objects,
                active_object=active_name,
                active_mode=active_mode,
                object_count=len(objects),
                collections=collections
            )
            
        except Exception as e:
            return self._error_response(
                EngineError.OPERATION_FAILED,
                f"Error obteniendo estado de escena: {e}"
            )
    
    def get_active_object(self) -> Optional[str]:
        """Retorna el nombre del objeto activo."""
        if not self.is_available():
            return None
        
        try:
            obj = self._bpy.context.active_object
            return obj.name if obj else None
        except Exception:
            return None
    
    def get_object_info(self, object_name: str) -> Dict[str, Any]:
        """Retorna información detallada de un objeto."""
        if not self.is_available():
            return self._error_response(
                EngineError.ENGINE_NOT_AVAILABLE,
                "Blender no está disponible"
            )
        
        try:
            if object_name not in self._bpy.data.objects:
                return self._error_response(
                    EngineError.OBJECT_NOT_FOUND,
                    f"Objeto '{object_name}' no encontrado"
                )
            
            obj = self._bpy.data.objects[object_name]
            
            return self._success_response(
                name=obj.name,
                type=obj.type,
                location=list(obj.location),
                rotation=list(obj.rotation_euler),
                scale=list(obj.scale),
                collection=obj.users_collection[0].name if obj.users_collection else "Scene Collection",
                visible=not obj.hide_viewport
            )
            
        except Exception as e:
            return self._error_response(
                EngineError.OPERATION_FAILED,
                f"Error obteniendo info del objeto: {e}"
            )
    
    def get_object(self, object_name: str) -> Dict[str, Any]:
        """Alias para get_object_info - compatibilidad con VisualConfirmation."""
        return self.get_object_info(object_name)
    
    # ========================================================================
    # MATERIALES
    # ========================================================================
    
    def create_material(self, name: str, **properties) -> Dict[str, Any]:
        """Crea un material en Blender."""
        if not self.is_available():
            return self._error_response(
                EngineError.ENGINE_NOT_AVAILABLE,
                "Blender no está disponible"
            )
        
        try:
            # Crear material
            mat = self._bpy.data.materials.new(name=name)
            mat.use_nodes = True
            
            # Aplicar propiedades si se proporcionan
            if 'color' in properties:
                color = properties['color']
                bsdf = mat.node_tree.nodes.get('Principled BSDF')
                if bsdf:
                    bsdf.inputs['Base Color'].default_value = (*color, 1.0)
            
            if 'metallic' in properties:
                bsdf = mat.node_tree.nodes.get('Principled BSDF')
                if bsdf:
                    bsdf.inputs['Metallic'].default_value = properties['metallic']
            
            if 'roughness' in properties:
                bsdf = mat.node_tree.nodes.get('Principled BSDF')
                if bsdf:
                    bsdf.inputs['Roughness'].default_value = properties['roughness']
            
            log_debug(f"✓ Material creado: {name}")
            
            return self._success_response(
                material_name=name,
                properties=properties
            )
            
        except Exception as e:
            return self._error_response(
                EngineError.OPERATION_FAILED,
                f"Error creando material: {e}"
            )

    def create_texture_material(self, name: str, image_path: str, **properties) -> Dict[str, Any]:
        """
        Crea un material con una textura de imagen en Blender.
        
        Parameters:
            name: Nombre del material
            image_path: Ruta absoluta a la imagen
            properties: Otras propiedades BSDF (metallic, roughness)
        """
        if not self.is_available():
            return self._error_response(
                EngineError.ENGINE_NOT_AVAILABLE,
                "Blender no está disponible"
            )
        
        try:
            # Crear material
            mat = self._bpy.data.materials.new(name=name)
            mat.use_nodes = True
            nodes = mat.node_tree.nodes
            links = mat.node_tree.links
            
            # Limpiar nodos predeterminados para asegurar estructura limpia
            nodes.clear()
            
            # Crear nodos básicos
            node_output = nodes.new(type='ShaderNodeOutputMaterial')
            node_output.location = (400, 0)
            
            node_bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
            node_bsdf.location = (0, 0)
            
            node_texture = nodes.new(type='ShaderNodeTexImage')
            node_texture.location = (-400, 0)
            
            # Cargar imagen (vía bpy)
            try:
                import os
                abs_image_path = os.path.abspath(image_path)
                img = self._bpy.data.images.load(abs_image_path)
                node_texture.image = img
            except Exception as e:
                return self._error_response(
                    EngineError.OPERATION_FAILED, 
                    f"Error cargando imagen de textura en {image_path}: {e}"
                )
            
            # Vincular nodos
            links.new(node_texture.outputs['Color'], node_bsdf.inputs['Base Color'])
            links.new(node_bsdf.outputs['BSDF'], node_output.inputs['Surface'])
            
            # Aplicar propiedades adicionales
            if 'metallic' in properties:
                node_bsdf.inputs['Metallic'].default_value = properties['metallic']
            
            if 'roughness' in properties:
                node_bsdf.inputs['Roughness'].default_value = properties['roughness']
                
            log_debug(f"✓ Material de textura creado: {name} (Imagen: {image_path})")
            
            return self._success_response(
                material_name=name,
                image_path=image_path
            )
        except Exception as e:
            return self._error_response(
                EngineError.OPERATION_FAILED,
                f"Error inesperado creando material de textura: {e}"
            )
    
    def apply_material(self, object_name: str, material_name: str) -> Dict[str, Any]:
        """Aplica un material a un objeto."""
        if not self.is_available():
            return self._error_response(
                EngineError.ENGINE_NOT_AVAILABLE,
                "Blender no está disponible"
            )
        
        try:
            # Verificar objeto
            obj = self._find_object(object_name)
            if not obj:
                return self._error_response(
                    EngineError.OBJECT_NOT_FOUND,
                    f"Objeto '{object_name}' no encontrado"
                )
            
            object_name = obj.name
            
            # Verificar material
            if material_name not in self._bpy.data.materials:
                return self._error_response(
                    EngineError.OBJECT_NOT_FOUND,
                    f"Material '{material_name}' no encontrado"
                )
            
            mat = self._bpy.data.materials[material_name]
            
            # Aplicar material
            if obj.data.materials:
                obj.data.materials[0] = mat
            else:
                obj.data.materials.append(mat)
            
            log_debug(f"✓ Material aplicado: {material_name} → {object_name}")
            
            return self._success_response(
                object_name=object_name,
                material_name=material_name
            )
            
        except Exception as e:
            return self._error_response(
                EngineError.OPERATION_FAILED,
                f"Error aplicando material: {e}"
            )
    
    # ========================================================================
    # ILUMINACIÓN
    # ========================================================================
    
    def create_light(
        self,
        light_type: Literal['POINT', 'SUN', 'SPOT', 'AREA'],
        **params
    ) -> Dict[str, Any]:
        """Crea una fuente de luz en Blender."""
        if not self.is_available():
            return self._error_response(
                EngineError.ENGINE_NOT_AVAILABLE,
                "Blender no está disponible"
            )
        
        try:
            name = params.get('name', f'Light_{light_type}')
            location = params.get('location', [0, 0, 5])
            energy = params.get('energy', 1.0)
            
            # Crear luz
            light_data = self._bpy.data.lights.new(name=name, type=light_type)
            light_data.energy = energy
            
            # Crear objeto de luz
            light_obj = self._bpy.data.objects.new(name=name, object_data=light_data)
            light_obj.location = location
            
            # Vincular a la escena
            self._bpy.context.collection.objects.link(light_obj)
            
            log_debug(f"✓ Luz creada: {light_type} → {name}")
            
            return self._success_response(
                light_name=name,
                type=light_type,
                location=list(location),
                energy=energy
            )
            
        except Exception as e:
            return self._error_response(
                EngineError.OPERATION_FAILED,
                f"Error creando luz: {e}"
            )
    
    # ========================================================================
    # RENDER Y EXPORTACIÓN
    # ========================================================================
    
    def render_scene(self, output_path: str, **settings) -> Dict[str, Any]:
        """Renderiza la escena en Blender."""
        if not self.is_available():
            return self._error_response(
                EngineError.ENGINE_NOT_AVAILABLE,
                "Blender no está disponible"
            )
        
        try:
            import time
            
            scene = self._bpy.context.scene
            
            # Configurar render
            if 'resolution' in settings:
                scene.render.resolution_x = settings['resolution'][0]
                scene.render.resolution_y = settings['resolution'][1]
            
            if 'engine' in settings:
                scene.render.engine = settings['engine']
            
            if 'samples' in settings:
                if scene.render.engine == 'CYCLES':
                    scene.cycles.samples = settings['samples']
                elif scene.render.engine == 'BLENDER_EEVEE':
                    scene.eevee.taa_render_samples = settings['samples']
            
            # Configurar salida
            # ASEGURAR RUTA ABSOLUTA PARA EVITAR C:\ZULY_LAB
            abs_path = str(Path(output_path).absolute())
            scene.render.filepath = abs_path
            scene.render.image_settings.file_format = settings.get('format', 'PNG')
            
            # Renderizar
            start_time = time.time()
            self._bpy.ops.render.render(write_still=True)
            render_time = time.time() - start_time
            
            log_info(f"✓ Render completado: {abs_path} ({render_time:.2f}s)")
            
            return self._success_response(
                output_path=abs_path,
                render_time=render_time,
                resolution=[scene.render.resolution_x, scene.render.resolution_y]
            )
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            return self._error_response(
                EngineError.OPERATION_FAILED,
                f"Error renderizando escena: {e}"
            )

    def clear_scene(self) -> Dict[str, Any]:
        """Borra todos los objetos de la escena actual."""
        if not self.is_available():
            return self._error_response(
                EngineError.ENGINE_NOT_AVAILABLE,
                "Blender no está disponible"
            )
        
        try:
            # Seleccionar todo y borrar
            self._bpy.ops.object.select_all(action='SELECT')
            self._bpy.ops.object.delete()
            
            # También borrar materiales, luces, etc. no usados
            for mat in self._bpy.data.materials:
                if mat.users == 0:
                    self._bpy.data.materials.remove(mat)
            
            log_info("✓ Escena limpiada correctamente")
            return self._success_response()
            
        except Exception as e:
            return self._error_response(
                EngineError.OPERATION_FAILED,
                f"Error limpiando escena: {e}"
            )

    def rename_object(self, old_name: str, new_name: str) -> Dict[str, Any]:
        """Renombra un objeto en Blender."""
        if not self.is_available():
            return self._error_response(EngineError.ENGINE_NOT_AVAILABLE)
        
        try:
            obj = self._find_object(old_name)
            if not obj:
                return self._error_response(
                    EngineError.OBJECT_NOT_FOUND,
                    f"Objeto '{old_name}' no encontrado"
                )
            
            obj.name = new_name
            actual_name = obj.name # Blender puede auto-corregir si ya existe
            
            log_info(f"✓ Objeto '{old_name}' renombrado a '{actual_name}'")
            return self._success_response(
                old_name=old_name,
                new_name=actual_name,
                object_name=actual_name
            )
        except Exception as e:
            return self._error_response(EngineError.OPERATION_FAILED, str(e))

    def set_object_visibility(self, object_name: str, visible: bool = True) -> Dict[str, Any]:
        """Cambia la visibilidad de un objeto en el viewport y render."""
        if not self.is_available():
            return self._error_response(EngineError.ENGINE_NOT_AVAILABLE)
        
        try:
            obj = self._find_object(object_name)
            if not obj:
                return self._error_response(
                    EngineError.OBJECT_NOT_FOUND,
                    f"Objeto '{object_name}' no encontrado"
                )
            
            obj.hide_viewport = not visible
            obj.hide_render = not visible
            
            log_info(f"✓ Visibilidad de '{object_name}' establecida a {visible}")
            return self._success_response(
                object_name=object_name,
                visible=visible
            )
        except Exception as e:
            return self._error_response(EngineError.OPERATION_FAILED, str(e))
    
    def export_scene(
        self,
        format: Literal['FBX', 'OBJ', 'GLTF', 'BLEND'],
        output_path: str,
        **options
    ) -> Dict[str, Any]:
        """Exporta la escena en Blender."""
        if not self.is_available():
            return self._error_response(
                EngineError.ENGINE_NOT_AVAILABLE,
                "Blender no está disponible"
            )
        
        try:
            if format == 'FBX':
                self._bpy.ops.export_scene.fbx(filepath=output_path, **options)
            elif format == 'OBJ':
                self._bpy.ops.export_scene.obj(filepath=output_path, **options)
            elif format == 'GLTF':
                self._bpy.ops.export_scene.gltf(filepath=output_path, **options)
            elif format == 'BLEND':
                self._bpy.ops.wm.save_as_mainfile(filepath=output_path)
            else:
                return self._error_response(
                    EngineError.INVALID_PARAMS,
                    f"Formato de exportación no válido: {format}"
                )
            
            log_info(f"✓ Escena exportada: {output_path} ({format})")
            
            return self._success_response(
                output_path=output_path,
                format=format,
                object_count=len(self._bpy.data.objects)
            )
            
        except Exception as e:
            return self._error_response(
                EngineError.OPERATION_FAILED,
                f"Error exportando escena: {e}"
            )
    
    
    # ========================================================================
    # CÁMARAS (FASE 17 CIERRE)
    # ========================================================================
    
    def create_camera(self, **params) -> Dict[str, Any]:
        """Crea una cámara en Blender."""
        if not self.is_available():
            return self._error_response(EngineError.ENGINE_NOT_AVAILABLE, "Blender no disponible")
        
        try:
            import math
            name = params.get('name', 'Camera_001')
            location = params.get('location', [10, -10, 5])
            focal_length = params.get('focal_length', 50.0)
            
            camera_data = self._bpy.data.cameras.new(name=name)
            camera_data.lens = focal_length
            
            camera_obj = self._bpy.data.objects.new(name=name, object_data=camera_data)
            camera_obj.location = tuple(location)
            
            self._bpy.context.collection.objects.link(camera_obj)
            
            # Automatismo: Set active camera
            self._bpy.context.scene.camera = camera_obj
            
            log_debug(f"✓ Cámara creada y activada: {name}")
            return self._success_response(camera_name=name, location=location)
        except Exception as e:
            return self._error_response(EngineError.OPERATION_FAILED, str(e))
    
    def set_active_camera(self, camera_name: str) -> Dict[str, Any]:
        """Establece la cámara activa."""
        if not self.is_available():
            return self._error_response(EngineError.ENGINE_NOT_AVAILABLE, "Blender no disponible")
        
        try:
            camera_obj = self._bpy.data.objects.get(camera_name)
            if not camera_obj or camera_obj.type != 'CAMERA':
                return self._error_response(EngineError.OBJECT_NOT_FOUND, f"Cámara {camera_name} no encontrada")
            
            self._bpy.context.scene.camera = camera_obj
            log_debug(f"✓ Cámara activa: {camera_name}")
            return self._success_response(camera_name=camera_name)
        except Exception as e:
            return self._error_response(EngineError.OPERATION_FAILED, str(e))
    
    def position_camera(self, camera_name: str, location: List[float], look_at: List[float]) -> Dict[str, Any]:
        """Posiciona una cámara mirando un punto."""
        if not self.is_available():
            return self._error_response(EngineError.ENGINE_NOT_AVAILABLE, "Blender no disponible")
        
        try:
            import math
            from mathutils import Vector

            camera_obj = self._bpy.data.objects.get(camera_name)
            if not camera_obj or camera_obj.type != 'CAMERA':
                return self._error_response(EngineError.OBJECT_NOT_FOUND, f"Cámara {camera_name} no encontrada")
            
            # Posicionar
            camera_obj.location = Vector(location)
            
            # Mirar punto
            direction = Vector(look_at) - Vector(location)
            rot_quat = direction.to_track_quat('-Z', 'Y')
            camera_obj.rotation_euler = rot_quat.to_euler()
            
            # Automatismo: Set active camera
            self._bpy.context.scene.camera = camera_obj
            
            log_debug(f"✓ Cámara posicionada y activada: {camera_name}")
            return self._success_response(
                camera_name=camera_name,
                location=location,
                look_at=look_at
            )
        except Exception as e:
            return self._error_response(EngineError.OPERATION_FAILED, str(e))
    
    # ========================================================================
    # MODIFICADORES (FASE 17 CIERRE)
    # ========================================================================
    
    def add_modifier(self, object_name: str, modifier_type: str, **params) -> Dict[str, Any]:
        """Agrega un modificador a un objeto."""
        if not self.is_available():
            return self._error_response(EngineError.ENGINE_NOT_AVAILABLE, "Blender no disponible")
        
        try:
            obj = self._bpy.data.objects.get(object_name)
            if not obj or obj.type != 'MESH':
                return self._error_response(EngineError.OBJECT_NOT_FOUND, f"Objeto {object_name} no encontrado")
            
            # Mapear tipos comunes
            modifier_map = {
                'SUBSURF': 'SUBSURF',
                'SUBDIVISION': 'SUBSURF',
                'ARRAY': 'ARRAY',
                'BEVEL': 'BEVEL',
                'BOOLEAN': 'BOOLEAN',
                'MIRROR': 'MIRROR',
                'SOLIDIFY': 'SOLIDIFY'
            }
            
            blender_type = modifier_map.get(modifier_type.upper(), modifier_type.upper())
            modifier = obj.modifiers.new(name=modifier_type, type=blender_type)
            
            # Aplicar parámetros según tipo
            if blender_type == 'SUBSURF':
                modifier.levels = params.get('levels', params.get('levels', 2))
                modifier.render_levels = params.get('render_levels', params.get('render_levels', 3))
            elif blender_type == 'ARRAY':
                modifier.count = params.get('count', 3)
                if 'relative_offset_displace' in params:
                    modifier.use_relative_offset = params.get('use_relative_offset', True)
                    modifier.relative_offset_displace = params['relative_offset_displace']
                else:
                    offset = (params.get('offset_x', 2.0), params.get('offset_y', 0), params.get('offset_z', 0))
                    modifier.relative_offset_displace = offset
                
                if 'constant_offset_displace' in params:
                    modifier.use_constant_offset = params.get('use_constant_offset', True)
                    modifier.constant_offset_displace = params['constant_offset_displace']
                    
            elif blender_type == 'BEVEL':
                modifier.width = params.get('width', 0.1)
                modifier.segments = params.get('segments', 2)
            elif blender_type == 'MIRROR':
                if 'use_axis' in params:
                    modifier.use_axis = params['use_axis']
            elif blender_type == 'BOOLEAN':
                modifier.operation = params.get('operation', 'DIFFERENCE')
                target_name = params.get('operand_object', params.get('operand'))
                if target_name and target_name in self._bpy.data.objects:
                    modifier.object = self._bpy.data.objects[target_name]
                    # Opcionalmente ocultar el operando
                    if params.get('hide_operand', True):
                        modifier.object.hide_viewport = True
                        modifier.object.hide_render = True
                else:
                    return self._error_response(EngineError.INVALID_PARAMS, f"Objeto target para booleano no válido: {target_name}")
            
            log_debug(f"✓ Modificador {modifier_type} agregado a {object_name}")
            return self._success_response(object_name=object_name, modifier_type=modifier_type)
        except Exception as e:
            return self._error_response(EngineError.OPERATION_FAILED, str(e))
    
    # ========================================================================
    # ACTUALIZACIONES (FASE 17 CIERRE)
    # ========================================================================
    
    def update_light(self, light_name: str, **properties) -> Dict[str, Any]:
        """Actualiza propiedades de una luz existente."""
        if not self.is_available():
            return self._error_response(EngineError.ENGINE_NOT_AVAILABLE, "Blender no disponible")
        
        try:
            light_obj = self._bpy.data.objects.get(light_name)
            if not light_obj or light_obj.type != 'LIGHT':
                return self._error_response(EngineError.OBJECT_NOT_FOUND, f"Luz {light_name} no encontrada")
            
            if 'energy' in properties:
                light_obj.data.energy = properties['energy']
            if 'color' in properties:
                light_obj.data.color = tuple(properties['color'])
            
            log_debug(f"✓ Luz actualizada: {light_name}")
            return self._success_response(light_name=light_name, **properties)
        except Exception as e:
            return self._error_response(EngineError.OPERATION_FAILED, str(e))
    
    def update_material(self, material_name: str, **properties) -> Dict[str, Any]:
        """Actualiza propiedades de un material existente."""
        log_info(f"update_material called for {material_name} with properties: {properties}")
        if not self.is_available():
            return self._error_response(EngineError.ENGINE_NOT_AVAILABLE, "Blender no disponible")
        
        try:
            mat = self._bpy.data.materials.get(material_name)
            if not mat:
                return self._error_response(EngineError.OBJECT_NOT_FOUND, f"Material {material_name} no encontrado")
            
            log_info(f"Material {material_name} encontrado, use_nodes: {mat.use_nodes}")
            if not mat.use_nodes:
                mat.use_nodes = True
                log_info(f"Activados nodos para material {material_name}")
            
            # Buscar o crear Principled BSDF
            principled = mat.node_tree.nodes.get('Principled BSDF')
            if not principled:
                principled = mat.node_tree.nodes.new('ShaderNodeBsdfPrincipled')
                log_info(f"Creado Principled BSDF para material {material_name}")
            else:
                log_info(f"Principled BSDF encontrado para material {material_name}")
            
            # Actualizar propiedades
            if 'color' in properties:
                color = properties['color']
                # Asegurar que sea una lista/tupla de 4 elementos (RGBA)
                if len(color) == 3:
                    color = (*color, 1.0)
                log_info(f"Actualizando color de {material_name}: {color}")
                principled.inputs['Base Color'].default_value = tuple(color)
                log_info(f"Color actual después de actualización: {list(principled.inputs['Base Color'].default_value)}")
            
            if 'metallic' in properties:
                principled.inputs['Metallic'].default_value = properties['metallic']
            
            if 'roughness' in properties:
                principled.inputs['Roughness'].default_value = properties['roughness']
            
            log_info(f"✓ Material actualizado: {material_name}")
            return self._success_response(material_name=material_name, **properties)
        except Exception as e:
            return self._error_response(EngineError.OPERATION_FAILED, str(e))
    
    # ========================================================================
    # JERARQUÍA Y ENSAMBLAJE (FASE 19)
    # ========================================================================
    
    def set_parent(
        self,
        child_name: str,
        parent_name: Optional[str] = None,
        keep_transform: bool = True
    ) -> Dict[str, Any]:
        """Establece relación parent/child en Blender."""
        if not self.is_available():
            return self._error_response(EngineError.ENGINE_NOT_AVAILABLE, "Blender no disponible")
        
        try:
            # Verificar que el hijo existe
            if child_name not in self._bpy.data.objects:
                return self._error_response(
                    EngineError.OBJECT_NOT_FOUND,
                    f"Objeto hijo '{child_name}' no encontrado"
                )
            
            child_obj = self._bpy.data.objects[child_name]
            
            # Si hay padre, establecer relación
            if parent_name is not None:
                if parent_name not in self._bpy.data.objects:
                    return self._error_response(
                        EngineError.OBJECT_NOT_FOUND,
                        f"Objeto padre '{parent_name}' no encontrado"
                    )
                
                parent_obj = self._bpy.data.objects[parent_name]
                
                # Prevenir ciclos
                temp_parent = parent_obj.parent
                while temp_parent:
                    if temp_parent == child_obj:
                        return self._error_response(
                            EngineError.INVALID_PARAMS,
                            f"Ciclo detectado: '{child_name}' no puede ser padre de su ancestro"
                        )
                    temp_parent = temp_parent.parent
                
                # Establecer parent
                child_obj.parent = parent_obj
                
                # Mantener transformación mundial si se solicita
                if keep_transform:
                    child_obj.matrix_parent_inverse = parent_obj.matrix_world.inverted()
                
                log_debug(f"✓ Parentado: {child_name} → {parent_name}")
            else:
                # Desparentar
                child_obj.parent = None
                log_debug(f"✓ Desparentado: {child_name}")
            
            return self._success_response(
                child=child_name,
                parent=parent_name,
                keep_transform=keep_transform
            )
        
        except Exception as e:
            return self._error_response(EngineError.OPERATION_FAILED, str(e))
    
    def get_parent(self, object_name: str) -> Optional[str]:
        """Obtiene el nombre del padre en Blender."""
        if not self.is_available():
            return None
        
        try:
            if object_name not in self._bpy.data.objects:
                return None
            
            obj = self._bpy.data.objects[object_name]
            return obj.parent.name if obj.parent else None
        except Exception:
            return None
    
    def get_children(self, object_name: str) -> List[str]:
        """Obtiene la lista de hijos en Blender."""
        if not self.is_available():
            return []
        
        try:
            if object_name not in self._bpy.data.objects:
                return []
            
            obj = self._bpy.data.objects[object_name]
            return [child.name for child in obj.children]
        except Exception:
            return []
    
    def align_objects(
        self,
        target_name: str,
        reference_name: str,
        mode: Literal['center', 'top', 'bottom', 'left', 'right', 'front', 'back']
    ) -> Dict[str, Any]:
        """Alinea objetos en Blender usando dimensions."""
        if not self.is_available():
            return self._error_response(EngineError.ENGINE_NOT_AVAILABLE, "Blender no disponible")
        
        try:
            # Verificar que ambos objetos existen
            if target_name not in self._bpy.data.objects:
                return self._error_response(
                    EngineError.OBJECT_NOT_FOUND,
                    f"Objeto target '{target_name}' no encontrado"
                )
            
            if reference_name not in self._bpy.data.objects:
                return self._error_response(
                    EngineError.OBJECT_NOT_FOUND,
                    f"Objeto reference '{reference_name}' no encontrado"
                )
            
            target = self._bpy.data.objects[target_name]
            reference = self._bpy.data.objects[reference_name]
            
            # CRÍTICO: Actualizar view layer para obtener dimensions correctas
            self._bpy.context.view_layer.update()
            
            # Obtener dimensiones
            target_dims = target.dimensions
            ref_dims = reference.dimensions
            ref_loc = reference.location
            
            # Calcular nueva posición según modo
            new_location = list(target.location)
            
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
            target.location = new_location
            
            log_debug(f"✓ Alineado: {target_name} → {reference_name} ({mode})")
            
            return self._success_response(
                target=target_name,
                reference=reference_name,
                new_location=list(new_location),
                mode=mode
            )
        
        except Exception as e:
            return self._error_response(EngineError.OPERATION_FAILED, str(e))
    
    
    # ========================================================================
    # TOPOLOGÍA Y AUDITORÍA DE MALLA (RETO 6.6)
    # ========================================================================
    
    def validate_mesh_topology(self, object_name: str) -> Dict[str, Any]:
        """Audita la topología de un objeto MESH usando bmesh (Watertight, degeneración, etc)."""
        if not self.is_available():
            return self._error_response(EngineError.ENGINE_NOT_AVAILABLE, "Blender no disponible")
            
        try:
            import bmesh
            
            obj = self._bpy.data.objects.get(object_name)
            if not obj or obj.type != 'MESH':
                return self._error_response(EngineError.OBJECT_NOT_FOUND, f"Objeto {object_name} no encontrado o no es una MESH")
                
            # Forzar object mode
            if self._bpy.context.mode != 'OBJECT':
                self._bpy.ops.object.mode_set(mode='OBJECT')
                
            # Trabajar con el objeto evaluado (modificadores aplicados visualmente)
            depsgraph = self._bpy.context.evaluated_depsgraph_get()
            eval_obj = obj.evaluated_get(depsgraph)
            mesh_data = eval_obj.to_mesh()
            
            # Inicializar BMesh
            bm = bmesh.new()
            bm.from_mesh(mesh_data)
            
            # Asegurar geometría actualizada antes del análisis
            bm.verts.ensure_lookup_table()
            bm.edges.ensure_lookup_table()
            bm.faces.ensure_lookup_table()
            
            # Recálculo de normales para consistencia
            bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
            
            # Auditorías Estructurales
            non_manifold_edges = [e for e in bm.edges if not e.is_manifold]
            loose_verts = [v for v in bm.verts if not v.link_edges]
            zero_area_faces = [f for f in bm.faces if f.calc_area() < 1e-6]
            
            validation_results = {
                "is_watertight": len(non_manifold_edges) == 0,
                "non_manifold_edges_count": len(non_manifold_edges),
                "loose_vertices_count": len(loose_verts),
                "zero_area_faces_count": len(zero_area_faces),
                "total_vertices": len(bm.verts),
                "total_edges": len(bm.edges),
                "total_faces": len(bm.faces),
            }
            
            # Limpieza de memoria (En 3.6, to_mesh crea un dato nuevo que debemos liberar)
            bm.free()
            try:
                # Intentar limpiar el mesh temporal si es posible
                if hasattr(obj, "to_mesh_clear"):
                    obj.to_mesh_clear()
            except:
                pass
            
            log_info(f"✓ Auditoría de Topología de '{object_name}' completada: Watertight = {validation_results['is_watertight']}")
            
            return self._success_response(
                object_name=object_name,
                metrics=validation_results
            )
            
        except ImportError:
            return self._error_response(EngineError.OPERATION_FAILED, "El módulo bmesh no está disponible en este entorno.")
        except Exception as e:
            return self._error_response(EngineError.OPERATION_FAILED, f"Error validando topología: {e}")

    def fix_mesh(self, object_name: str, remove_doubles: bool = True, 
                 recalculate_normals: bool = True, dissolve_degenerate: bool = True) -> Dict[str, Any]:
        """
        Aplica reparaciones automáticas avanzadas a una malla.
        """
        if not self.is_available():
            return self._error_response(EngineError.ENGINE_NOT_AVAILABLE)
            
        try:
            obj = self._enter_edit_mode(object_name)
            if not obj:
                return self._error_response(EngineError.OBJECT_NOT_FOUND)
                
            self._bpy.ops.mesh.select_all(action='SELECT')
            
            if remove_doubles:
                self._bpy.ops.mesh.remove_doubles(threshold=0.0001)
            
            if dissolve_degenerate:
                self._bpy.ops.mesh.dissolve_degenerate()
                
            if recalculate_normals:
                self._bpy.ops.mesh.normals_make_consistent(inside=False)
            
            self._exit_edit_mode()
            
            log_info(f"💪 Malla '{object_name}' saneada (Doubles={remove_doubles}, Normals={recalculate_normals})")
            return self._success_response(object_name=object_name, status="fixed")
            
        except Exception as e:
            self._exit_edit_mode()
            return self._error_response(EngineError.OPERATION_FAILED, f"Error reparando malla: {e}")

    # ========================================================================
    # EDIT MODE — OPERACIONES DE ESCULTURA (FASE F)
    # ========================================================================

    def _enter_edit_mode(self, object_name: str):
        """Utilidad: Selecciona un objeto y entra en Edit Mode."""
        obj = self._find_object(object_name)
        if not obj or obj.type != 'MESH':
            return None
        # Deseleccionar todo primero
        self._bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        self._bpy.context.view_layer.objects.active = obj
        self._bpy.ops.object.mode_set(mode='EDIT')
        return obj

    def _exit_edit_mode(self):
        """Utilidad: Sale de Edit Mode."""
        try:
            self._bpy.ops.object.mode_set(mode='OBJECT')
        except:
            pass

    def _select_faces_by_direction(self, bm, face_select: str):
        """Utilidad: Selecciona caras de un bmesh según su orientación normal."""
        for f in bm.faces:
            f.select = False
        
        # Mapeo de nombre a vector normal esperado
        direction_map = {
            'TOP':    ('z', 1),
            'BOTTOM': ('z', -1),
            'FRONT':  ('y', -1),
            'BACK':   ('y', 1),
            'LEFT':   ('x', -1),
            'RIGHT':  ('x', 1),
        }
        
        if face_select == 'ALL':
            for f in bm.faces:
                f.select = True
        elif face_select in direction_map:
            axis, sign = direction_map[face_select]
            for f in bm.faces:
                val = getattr(f.normal, axis)
                if (sign > 0 and val > 0.5) or (sign < 0 and val < -0.5):
                    f.select = True

    def _get_extrude_vector(self, face_select: str, offset: float):
        """Utilidad: Calcula el vector de extrusión correcto según la dirección de la cara."""
        vectors = {
            'TOP':    (0, 0, offset),
            'BOTTOM': (0, 0, -offset),
            'FRONT':  (0, -offset, 0),
            'BACK':   (0, offset, 0),
            'LEFT':   (-offset, 0, 0),
            'RIGHT':  (offset, 0, 0),
            'ALL':    (0, 0, offset),  # Fallback: hacia arriba
        }
        return vectors.get(face_select, (0, 0, offset))

    def extrude_faces(self, object_name: str, offset: float = 1.0, 
                      face_select: str = 'ALL') -> Dict[str, Any]:
        """
        Extruye caras de un objeto para crear profundidad.
        La dirección de extrusión sigue la normal de las caras seleccionadas.
        
        Args:
            object_name: Nombre del objeto.
            offset: Distancia de extrusión (positivo = hacia afuera).
            face_select: 'ALL', 'TOP', 'BOTTOM', 'FRONT', 'BACK', 'LEFT', 'RIGHT'
        """
        if not self.is_available():
            return self._error_response(EngineError.ENGINE_NOT_AVAILABLE)
        try:
            obj = self._enter_edit_mode(object_name)
            if not obj:
                return self._error_response(EngineError.OBJECT_NOT_FOUND)
            
            import bmesh
            bm = bmesh.from_edit_mesh(obj.data)
            bm.faces.ensure_lookup_table()
            
            # Seleccionar caras según orientación
            self._select_faces_by_direction(bm, face_select)
            bmesh.update_edit_mesh(obj.data)
            
            # Calcular vector de extrusión correcto
            extrude_vec = self._get_extrude_vector(face_select, offset)
            
            # Extruir en la dirección correcta
            self._bpy.ops.mesh.extrude_region_move(
                TRANSFORM_OT_translate={"value": extrude_vec}
            )
            
            self._exit_edit_mode()
            
            # Saneamiento automático post-extrusión (Evita caras duplicadas y normales invertidas)
            self.fix_mesh(object_name)
            
            log_info(f"Extrusion aplicada a '{object_name}': offset={offset}, dir={face_select}, vec={extrude_vec}")
            return self._success_response(object_name=object_name, offset=offset, direction=face_select)
        except Exception as e:
            self._exit_edit_mode()
            return self._error_response(EngineError.OPERATION_FAILED, f"Error en extrusion: {e}")


    def inset_faces(self, object_name: str, thickness: float = 0.1, depth: float = 0.0,
                    face_select: str = 'ALL') -> Dict[str, Any]:
        """
        Inserta bordes internos en las caras seleccionadas (como un marco).
        
        Args:
            object_name: Nombre del objeto.
            thickness: Grosor del inset (distancia del borde).
            depth: Profundidad del inset (positivo = hacia adentro).
            face_select: Criterio de selección de caras.
        """
        if not self.is_available():
            return self._error_response(EngineError.ENGINE_NOT_AVAILABLE)
        try:
            obj = self._enter_edit_mode(object_name)
            if not obj:
                return self._error_response(EngineError.OBJECT_NOT_FOUND)
            
            import bmesh
            bm = bmesh.from_edit_mesh(obj.data)
            bm.faces.ensure_lookup_table()
            
            self._select_faces_by_direction(bm, face_select)
            bmesh.update_edit_mesh(obj.data)
            
            self._bpy.ops.mesh.inset(thickness=thickness, depth=depth)
            
            self._exit_edit_mode()
            log_info(f"✓ Inset aplicado a '{object_name}': thickness={thickness}, depth={depth}")
            return self._success_response(object_name=object_name, thickness=thickness, depth=depth)
        except Exception as e:
            self._exit_edit_mode()
            return self._error_response(EngineError.OPERATION_FAILED, f"Error en inset: {e}")

    def loop_cut(self, object_name: str, number_cuts: int = 1, 
                 edge_index: int = 0, factor: float = 0.0) -> Dict[str, Any]:
        """
        Añade cortes de bucle a un objeto para subdividir geometría.
        
        Args:
            object_name: Nombre del objeto.
            number_cuts: Número de cortes.
            edge_index: Índice de la arista donde empieza el corte.
            factor: Posición del corte (-1 a 1, 0 = centro).
        """
        if not self.is_available():
            return self._error_response(EngineError.ENGINE_NOT_AVAILABLE)
        try:
            obj = self._enter_edit_mode(object_name)
            if not obj:
                return self._error_response(EngineError.OBJECT_NOT_FOUND)
            
            self._bpy.ops.mesh.loopcut_slide(
                MESH_OT_loopcut={"number_cuts": number_cuts, "edge_index": edge_index},
                TRANSFORM_OT_edge_slide={"value": factor}
            )
            
            self._exit_edit_mode()
            log_info(f"✓ Loop Cut aplicado a '{object_name}': {number_cuts} corte(s)")
            return self._success_response(object_name=object_name, number_cuts=number_cuts)
        except Exception as e:
            self._exit_edit_mode()
            return self._error_response(EngineError.OPERATION_FAILED, f"Error en loop cut: {e}")

    def bevel_edges(self, object_name: str, width: float = 0.05, 
                    segments: int = 3, select_all: bool = True) -> Dict[str, Any]:
        """
        Bisela aristas para crear esquinas suavizadas.
        
        Args:
            object_name: Nombre del objeto.
            width: Ancho del biselado.
            segments: Número de segmentos del bisel.
            select_all: Si True, bisela todas las aristas.
        """
        if not self.is_available():
            return self._error_response(EngineError.ENGINE_NOT_AVAILABLE)
        try:
            obj = self._enter_edit_mode(object_name)
            if not obj:
                return self._error_response(EngineError.OBJECT_NOT_FOUND)
            
            if select_all:
                self._bpy.ops.mesh.select_all(action='SELECT')
            
            self._bpy.ops.mesh.bevel(offset=width, segments=segments, affect='EDGES')
            
            self._exit_edit_mode()
            log_info(f"✓ Bevel aplicado a '{object_name}': width={width}, segments={segments}")
            return self._success_response(object_name=object_name, width=width, segments=segments)
        except Exception as e:
            self._exit_edit_mode()
            return self._error_response(EngineError.OPERATION_FAILED, f"Error en bevel: {e}")

    def boolean_cut(self, object_name: str, cutter_name: str, 
                    operation: str = 'DIFFERENCE') -> Dict[str, Any]:
        """
        Aplica una operación booleana Y la hace permanente (apply).
        Opcionalmente elimina el objeto cortante.
        
        Args:
            object_name: Objeto a cortar.
            cutter_name: Objeto cortante (se elimina después).
            operation: 'DIFFERENCE', 'UNION', 'INTERSECT'.
        """
        if not self.is_available():
            return self._error_response(EngineError.ENGINE_NOT_AVAILABLE)
        try:
            obj = self._find_object(object_name)
            cutter = self._find_object(cutter_name)
            if not obj or not cutter:
                return self._error_response(EngineError.OBJECT_NOT_FOUND)
            
            # Asegurar que estamos en Object Mode
            self._bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)
            self._bpy.context.view_layer.objects.active = obj
            
            # Agregar modificador booleano
            mod = obj.modifiers.new(name="BoolCut", type='BOOLEAN')
            mod.operation = operation
            mod.object = cutter
            
            # Aplicar el modificador (hacerlo permanente)
            self._bpy.ops.object.modifier_apply(modifier=mod.name)
            
            # Saneamiento automático post-booleano (Crítico para evitar normales locas)
            self.fix_mesh(object_name)
            
            # Eliminar el objeto cortante
            self._bpy.ops.object.select_all(action='DESELECT')
            cutter.select_set(True)
            self._bpy.context.view_layer.objects.active = cutter
            self._bpy.ops.object.delete()
            
            log_info(f"✓ Boolean {operation} aplicado: '{cutter_name}' cortó '{object_name}' (y fue eliminado)")
            return self._success_response(object_name=object_name, operation=operation, cutter_removed=True)
        except Exception as e:
            return self._error_response(EngineError.OPERATION_FAILED, f"Error en boolean cut: {e}")

    def apply_modifier(self, object_name: str, modifier_name: str = None) -> Dict[str, Any]:
        """
        Aplica (hace permanente) un modificador existente.
        Si no se indica nombre, aplica el primero.
        """
        if not self.is_available():
            return self._error_response(EngineError.ENGINE_NOT_AVAILABLE)
        try:
            obj = self._find_object(object_name)
            if not obj:
                return self._error_response(EngineError.OBJECT_NOT_FOUND)
            
            self._bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)
            self._bpy.context.view_layer.objects.active = obj
            
            if modifier_name:
                self._bpy.ops.object.modifier_apply(modifier=modifier_name)
            elif obj.modifiers:
                self._bpy.ops.object.modifier_apply(modifier=obj.modifiers[0].name)
            else:
                return self._error_response(EngineError.INVALID_PARAMS, "No hay modificadores para aplicar")
            
            log_info(f"✓ Modificador aplicado permanentemente en '{object_name}'")
            return self._success_response(object_name=object_name)
        except Exception as e:
            return self._error_response(EngineError.OPERATION_FAILED, f"Error aplicando modificador: {e}")

    def recalculate_normals(self, object_name: str, inside: bool = False) -> Dict[str, Any]:
        """
        Corrige la orientación de las caras de forma explícita.
        """
        if not self.is_available():
            return self._error_response(EngineError.ENGINE_NOT_AVAILABLE)
        try:
            obj = self._enter_edit_mode(object_name)
            if not obj:
                return self._error_response(EngineError.OBJECT_NOT_FOUND)
            
            self._bpy.ops.mesh.select_all(action='SELECT')
            self._bpy.ops.mesh.normals_make_consistent(inside=inside)
            self._exit_edit_mode()
            
            log_info(f"✓ Normales recalculadas en '{object_name}' (inside={inside})")
            return self._success_response(object_name=object_name)
        except Exception as e:
            self._exit_edit_mode()
            return self._error_response(EngineError.OPERATION_FAILED, f"Error recalculando normales: {e}")


    def scan_scene_pattern(self, selected_only: bool = False) -> Dict[str, Any]:
        """
        Escanea la escena extrayendo el 'ADN' geométrico.
        Si selected_only es True, solo escanea los objetos seleccionados.
        """
        if not self.is_available():
            return self._error_response(EngineError.ENGINE_NOT_AVAILABLE, "Blender no disponible")
            
        try:
            pattern_data = {"objects": []}
            
            target_objects = self._bpy.context.selected_objects if selected_only else self._bpy.context.scene.objects
            
            for obj in target_objects:
                if obj.type != 'MESH':
                    continue
                
                obj_data = {
                    "name": obj.name,
                    "type": obj.type,
                    "location": list(obj.location),
                    "rotation": list(obj.rotation_euler),
                    "scale": list(obj.scale),
                    "dimensions": list(obj.dimensions),
                    "parent": obj.parent.name if obj.parent else None,
                    "modifiers": []
                }
                
                for mod in obj.modifiers:
                    mod_data = {
                        "name": mod.name,
                        "type": mod.type
                    }
                    if mod.type == 'BEVEL':
                        mod_data["width"] = getattr(mod, 'width', 0)
                        mod_data["segments"] = getattr(mod, 'segments', 0)
                    elif mod.type == 'ARRAY':
                        mod_data["count"] = getattr(mod, 'count', 0)
                        mod_data["use_relative_offset"] = getattr(mod, 'use_relative_offset', False)
                        mod_data["relative_offset_displace"] = list(getattr(mod, 'relative_offset_displace', [0, 0, 0]))
                        mod_data["use_constant_offset"] = getattr(mod, 'use_constant_offset', False)
                        mod_data["constant_offset_displace"] = list(getattr(mod, 'constant_offset_displace', [0, 0, 0]))
                    elif mod.type == 'BOOLEAN':
                        mod_data["operation"] = getattr(mod, 'operation', 'UNKNOWN')
                        mod_data["operand"] = mod.object.name if getattr(mod, 'object', None) else None
                    elif mod.type == 'SUBSURF':
                        mod_data["levels"] = getattr(mod, 'levels', 0)
                        mod_data["render_levels"] = getattr(mod, 'render_levels', 0)
                    elif mod.type == 'MIRROR':
                        mod_data["use_axis"] = [mod.use_axis[0], mod.use_axis[1], mod.use_axis[2]]
                        
                    obj_data["modifiers"].append(mod_data)
                    
                pattern_data["objects"].append(obj_data)
                
            log_info(f"✓ Escáner pasivo completado: {len(pattern_data['objects'])} mallas extraídas.")
            return self._success_response(pattern=pattern_data)
            
        except Exception as e:
            return self._error_response(EngineError.OPERATION_FAILED, f"Error escaneando patrón: {e}")

    def delete_object(self, object_name: str) -> Dict[str, Any]:
        """Borra un objeto en Blender."""
        if not self.is_available():
            return self._error_response(EngineError.ENGINE_NOT_AVAILABLE)
        try:
            obj = self._find_object(object_name)
            if not obj:
                return self._error_response(EngineError.OBJECT_NOT_FOUND)
            
            # Seleccionar solo este objeto y borrar
            self._bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)
            self._bpy.context.view_layer.objects.active = obj
            self._bpy.ops.object.delete()
            
            log_debug(f"✓ Objeto '{object_name}' eliminado")
            return self._success_response(message=f"Objeto '{object_name}' eliminado")
        except Exception as e:
            return self._error_response(EngineError.OPERATION_FAILED, f"Error eliminando objeto: {e}")

    def duplicate_object(self, object_name: str, new_name: Optional[str] = None) -> Dict[str, Any]:
        """Duplica un objeto en Blender."""
        if not self.is_available():
            return self._error_response(EngineError.ENGINE_NOT_AVAILABLE)
        try:
            obj = self._find_object(object_name)
            if not obj:
                return self._error_response(EngineError.OBJECT_NOT_FOUND)
            
            # Seleccionar y duplicar
            self._bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)
            self._bpy.context.view_layer.objects.active = obj
            self._bpy.ops.object.duplicate()
            
            new_obj = self._bpy.context.active_object
            if new_name:
                new_obj.name = new_name
            
            log_debug(f"✓ Objeto '{object_name}' duplicado como '{new_obj.name}'")
            return self._success_response(object_name=new_obj.name)
        except Exception as e:
            return self._error_response(EngineError.OPERATION_FAILED, f"Error duplicando objeto: {e}")

    def select_object(self, object_name: str) -> Dict[str, Any]:
        """Selecciona un objeto en Blender."""
        if not self.is_available():
            return self._error_response(EngineError.ENGINE_NOT_AVAILABLE)
        try:
            obj = self._find_object(object_name)
            if not obj:
                return self._error_response(EngineError.OBJECT_NOT_FOUND)
            
            obj.select_set(True)
            self._bpy.context.view_layer.objects.active = obj
            log_debug(f"✓ Objeto '{object_name}' seleccionado")
            return self._success_response(object_name=object_name)
        except Exception as e:
            return self._error_response(EngineError.OPERATION_FAILED, f"Error seleccionando objeto: {e}")

    def deselect_all(self) -> Dict[str, Any]:
        """Deselecciona todos los objetos en Blender."""
        if not self.is_available():
            return self._error_response(EngineError.ENGINE_NOT_AVAILABLE)
        try:
            self._bpy.ops.object.select_all(action='DESELECT')
            log_debug("✓ Todos los objetos deseleccionados")
            return self._success_response()
        except Exception as e:
            return self._error_response(EngineError.OPERATION_FAILED, f"Error deseleccionando: {e}")

    def select_all_by_type(self, type_name: str) -> Dict[str, Any]:
        """Selecciona todos los objetos de un tipo en Blender."""
        if not self.is_available():
            return self._error_response(EngineError.ENGINE_NOT_AVAILABLE)
        try:
            self._bpy.ops.object.select_by_type(type=type_name)
            log_debug(f"✓ Objetos de tipo '{type_name}' seleccionados")
            return self._success_response(type=type_name)
        except Exception as e:
            return self._error_response(EngineError.OPERATION_FAILED, f"Error seleccionando por tipo: {e}")

    def rename_object(self, old_name: str, new_name: str) -> Dict[str, Any]:
        """Renombra un objeto en Blender."""
        if not self.is_available():
            return self._error_response(EngineError.ENGINE_NOT_AVAILABLE)
        try:
            obj = self._find_object(old_name)
            if not obj:
                return self._error_response(EngineError.OBJECT_NOT_FOUND)
            
            obj.name = new_name
            log_debug(f"✓ Objeto '{old_name}' renombrado a '{new_name}'")
            return self._success_response(old_name=old_name, new_name=new_name)
        except Exception as e:
            return self._error_response(EngineError.OPERATION_FAILED, f"Error renombrando objeto: {e}")

    def set_parent(self, child_name: str, parent_name: Optional[str] = None, 
                   keep_transform: bool = True) -> Dict[str, Any]:
        """Establece relación parent/child en Blender."""
        if not self.is_available():
            return self._error_response(EngineError.ENGINE_NOT_AVAILABLE)
        try:
            child = self._find_object(child_name)
            if not child:
                return self._error_response(EngineError.OBJECT_NOT_FOUND, f"Hijo '{child_name}' no encontrado")
            
            if parent_name:
                parent = self._find_object(parent_name)
                if not parent:
                    return self._error_response(EngineError.OBJECT_NOT_FOUND, f"Padre '{parent_name}' no encontrado")
                
                # Guardar matriz mundial antes si se requiere mantener transform
                if keep_transform:
                    matrix_world = child.matrix_world.copy()
                    child.parent = parent
                    child.matrix_world = matrix_world
                else:
                    child.parent = parent
            else:
                # Desparentar
                if keep_transform:
                    matrix_world = child.matrix_world.copy()
                    child.parent = None
                    child.matrix_world = matrix_world
                else:
                    child.parent = None
            
            return self._success_response(child=child_name, parent=parent_name)
        except Exception as e:
            return self._error_response(EngineError.OPERATION_FAILED, f"Error en set_parent: {e}")

    def get_parent(self, object_name: str) -> Optional[str]:
        """Obtiene el nombre del padre en Blender."""
        obj = self._find_object(object_name)
        if obj and obj.parent:
            return obj.parent.name
        return None

    def get_children(self, object_name: str) -> List[str]:
        """Obtiene la lista de nombres de hijos en Blender."""
        obj = self._find_object(object_name)
        if obj:
            return [child.name for child in obj.children]
        return []

    def align_objects(self, target_name: str, reference_name: str, mode: str) -> Dict[str, Any]:
        """
        Alineación básica en Blender.
        TODO: Implementar lógica de alineación robusta.
        """
        # Implementación mínima: mover target a posición de reference
        target = self._find_object(target_name)
        reference = self._find_object(reference_name)
        if target and reference:
            target.location = reference.location
            return self._success_response(target=target_name, reference=reference_name)
        return self._error_response(EngineError.OBJECT_NOT_FOUND)

    def create_camera(self, **params) -> Dict[str, Any]:
        """Crea una cámara en Blender."""
        if not self.is_available():
            return self._error_response(EngineError.ENGINE_NOT_AVAILABLE)
        try:
            name = params.get('name', 'Camera')
            cam_data = self._bpy.data.cameras.new(name)
            cam_obj = self._bpy.data.objects.new(name, cam_data)
            self._bpy.context.collection.objects.link(cam_obj)
            
            if 'location' in params:
                cam_obj.location = params['location']
            
            return self._success_response(camera_name=name)
        except Exception as e:
            return self._error_response(EngineError.OPERATION_FAILED, f"Error creando cámara: {e}")

    def set_active_camera(self, camera_name: str) -> Dict[str, Any]:
        """Establece la cámara activa de la escena."""
        if not self.is_available():
            return self._error_response(EngineError.ENGINE_NOT_AVAILABLE)
        try:
            cam = self._find_object(camera_name)
            if cam and cam.type == 'CAMERA':
                self._bpy.context.scene.camera = cam
                return self._success_response(camera_name=camera_name)
            return self._error_response(EngineError.OBJECT_NOT_FOUND)
        except Exception as e:
            return self._error_response(EngineError.OPERATION_FAILED, f"Error activando cámara: {e}")

    def position_camera(self, camera_name: str, location: List[float], look_at: List[float]) -> Dict[str, Any]:
        """Posiciona una cámara mirando un punto (reutiliza rotate_object/look_at)."""
        # Implementación simplificada (solo mueve)
        return self.move_object(camera_name, location=location)

    def add_modifier(self, object_name: str, modifier_type: str, **params) -> Dict[str, Any]:
        """Agrega un modificador a un objeto."""
        if not self.is_available():
            return self._error_response(EngineError.ENGINE_NOT_AVAILABLE)
        try:
            obj = self._find_object(object_name)
            if not obj:
                return self._error_response(EngineError.OBJECT_NOT_FOUND)
            
            mod = obj.modifiers.new(name=params.get('name', modifier_type), type=modifier_type)
            return self._success_response(object_name=object_name, modifier_name=mod.name)
        except Exception as e:
            return self._error_response(EngineError.OPERATION_FAILED, f"Error agregando modificador: {e}")

    def update_light(self, light_name: str, **properties) -> Dict[str, Any]:
        """Actualiza propiedades de una luz."""
        if not self.is_available():
            return self._error_response(EngineError.ENGINE_NOT_AVAILABLE)
        try:
            light = self._find_object(light_name)
            if light and light.type == 'LIGHT':
                data = light.data
                if 'energy' in properties:
                    data.energy = properties['energy']
                if 'color' in properties:
                    data.color = properties['color']
                return self._success_response(light_name=light_name)
            return self._error_response(EngineError.OBJECT_NOT_FOUND)
        except Exception as e:
            return self._error_response(EngineError.OPERATION_FAILED, f"Error actualizando luz: {e}")
    
    def _get_collections_hierarchy(self) -> List[Dict]:
        """Obtiene la jerarquía de colecciones de la escena."""
        if not self.is_available():
            return []
        
        try:
            def traverse(collection):
                return {
                    'name': collection.name,
                    'objects': [obj.name for obj in collection.objects],
                    'children': [traverse(child) for child in collection.children]
                }
            
            if hasattr(self._bpy.context, 'scene') and self._bpy.context.scene:
                return [traverse(self._bpy.context.scene.collection)]
            return []
        except Exception:
            return []
