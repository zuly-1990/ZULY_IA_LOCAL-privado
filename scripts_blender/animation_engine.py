"""
Sistema de Animaciones para ZULY
Genera keyframes y exporta videos automáticamente
"""

import bpy
import os
from pathlib import Path
from dataclasses import dataclass
from typing import List, Optional, Tuple
import json
from datetime import datetime


@dataclass
class KeyframeConfig:
    """Configuración de un keyframe"""
    frame: int
    location: Optional[Tuple[float, float, float]] = None
    rotation: Optional[Tuple[float, float, float]] = None
    scale: Optional[Tuple[float, float, float]] = None
    properties: Optional[dict] = None


@dataclass
class AnimationConfig:
    """Configuración de animación completa"""
    name: str
    start_frame: int = 1
    end_frame: int = 250
    fps: int = 30
    format: str = "MP4"  # MP4, WEBM, PNG
    resolution: Tuple[int, int] = (1920, 1080)
    engine: str = "CYCLES"
    samples: int = 128
    output_path: str = "output.mp4"


class AnimationBuilder:
    """Construtor de animaciones en Blender"""
    
    def __init__(self):
        self.scene = bpy.context.scene
        self.keyframes: List[KeyframeConfig] = []
        self.config = None
        
    def set_config(self, config: AnimationConfig):
        """Establece la configuración de la animación"""
        self.config = config
        self.scene.frame_start = config.start_frame
        self.scene.frame_end = config.end_frame
        self.scene.render.fps = config.fps
        self.scene.render.resolution_x = config.resolution[0]
        self.scene.render.resolution_y = config.resolution[1]
        
    def add_keyframe(self, obj_name: str, config: KeyframeConfig):
        """Añade un keyframe a un objeto"""
        try:
            obj = bpy.data.objects[obj_name]
            self.scene.frame_set(config.frame)
            
            # Localización
            if config.location:
                obj.location = config.location
                obj.keyframe_insert(data_path="location")
            
            # Rotación
            if config.rotation:
                obj.rotation_euler = config.rotation
                obj.keyframe_insert(data_path="rotation_euler")
            
            # Escala
            if config.scale:
                obj.scale = config.scale
                obj.keyframe_insert(data_path="scale")
            
            # Propiedades personalizadas
            if config.properties:
                for prop_name, value in config.properties.items():
                    try:
                        setattr(obj, prop_name, value)
                        obj.keyframe_insert(data_path=prop_name)
                    except:
                        pass
            
            print(f"✅ Keyframe añadido: {obj_name} en frame {config.frame}")
            return True
        except KeyError:
            print(f"❌ Objeto no encontrado: {obj_name}")
            return False
    
    def add_camera_path(self, camera_name: str, positions: List[Tuple[float, float, float]],
                       frames: List[int], look_at: Optional[Tuple[float, float, float]] = None):
        """Crea una ruta de cámara suave"""
        try:
            camera = bpy.data.objects[camera_name]
            
            # Crear Bezier curve para la ruta
            curve_data = bpy.data.curves.new(
                name=f"{camera_name}_path",
                type='CURVE'
            )
            curve_obj = bpy.data.objects.new(
                f"{camera_name}_path",
                curve_data
            )
            bpy.context.collection.objects.link(curve_obj)
            
            # Configurar spline
            curve_data.splines.new('BEZIER')
            bezier_spline = curve_data.splines[0]
            
            # Añadir puntos
            bezier_spline.points.add(len(positions) - 1)
            for idx, pos in enumerate(positions):
                point = bezier_spline.points[idx]
                point.co = (*pos, 1)
                point.handle_left_type = 'AUTO'
                point.handle_right_type = 'AUTO'
            
            # Suavizar curva
            curve_data.resolution_u = 12
            
            # Configurar follow path constraint
            follow_path = camera.constraints.new(type='FOLLOW_PATH')
            follow_path.target = curve_obj
            follow_path.offset = -90
            
            # Añadir keyframes de progreso
            for frame_idx, frame in enumerate(frames):
                self.scene.frame_set(frame)
                progress = frame_idx / (len(frames) - 1) if len(frames) > 1 else 0
                follow_path.offset_factor = progress
                follow_path.keyframe_insert(data_path="offset_factor")
            
            print(f"✅ Ruta de cámara creada: {len(positions)} puntos")
            return True
        except Exception as e:
            print(f"❌ Error creando ruta de cámara: {e}")
            return False
    
    def rotate_object(self, obj_name: str, axis: str = 'Z', 
                     start_angle: float = 0, end_angle: float = 360,
                     start_frame: int = 1, end_frame: int = 250):
        """Rota un objeto de forma continua"""
        try:
            obj = bpy.data.objects[obj_name]
            
            # Frame inicial
            self.scene.frame_set(start_frame)
            if axis == 'X':
                obj.rotation_euler.x = start_angle * (3.14159 / 180)
            elif axis == 'Y':
                obj.rotation_euler.y = start_angle * (3.14159 / 180)
            elif axis == 'Z':
                obj.rotation_euler.z = start_angle * (3.14159 / 180)
            obj.keyframe_insert(data_path="rotation_euler")
            
            # Frame final
            self.scene.frame_set(end_frame)
            if axis == 'X':
                obj.rotation_euler.x = end_angle * (3.14159 / 180)
            elif axis == 'Y':
                obj.rotation_euler.y = end_angle * (3.14159 / 180)
            elif axis == 'Z':
                obj.rotation_euler.z = end_angle * (3.14159 / 180)
            obj.keyframe_insert(data_path="rotation_euler")
            
            print(f"✅ Rotación añadida: {obj_name} ({axis})")
            return True
        except KeyError:
            print(f"❌ Objeto no encontrado: {obj_name}")
            return False
    
    def zoom_camera(self, camera_name: str, start_focal: float = 50,
                   end_focal: float = 35, start_frame: int = 1,
                   end_frame: int = 250):
        """Crea un efecto de zoom con la cámara"""
        try:
            camera = bpy.data.objects[camera_name]
            camera_data = camera.data
            
            # Frame inicial
            self.scene.frame_set(start_frame)
            camera_data.lens = start_focal
            camera_data.keyframe_insert(data_path="lens")
            
            # Frame final
            self.scene.frame_set(end_frame)
            camera_data.lens = end_focal
            camera_data.keyframe_insert(data_path="lens")
            
            print(f"✅ Zoom añadido: {start_focal}mm → {end_focal}mm")
            return True
        except Exception as e:
            print(f"❌ Error en zoom: {e}")
            return False
    
    def add_lighting_animation(self, light_name: str,
                              start_energy: float = 1.0,
                              end_energy: float = 2.0,
                              start_frame: int = 1,
                              end_frame: int = 250):
        """Anima la intensidad de una luz"""
        try:
            light = bpy.data.objects[light_name]
            light_data = light.data
            
            # Frame inicial
            self.scene.frame_set(start_frame)
            light_data.energy = start_energy
            light_data.keyframe_insert(data_path="energy")
            
            # Frame final
            self.scene.frame_set(end_frame)
            light_data.energy = end_energy
            light_data.keyframe_insert(data_path="energy")
            
            print(f"✅ Animación de luz: {light_name}")
            return True
        except Exception as e:
            print(f"❌ Error en animación de luz: {e}")
            return False
    
    def set_render_settings(self, engine: str = "CYCLES", 
                           samples: int = 128, gpu: bool = True):
        """Configura los parámetros de render"""
        self.scene.render.engine = engine
        
        if engine == "CYCLES":
            self.scene.cycles.samples = samples
            if gpu:
                self.scene.cycles.use_denoising = True
                try:
                    self.scene.cycles.device = "GPU"
                except:
                    print("⚠️ GPU no disponible, usando CPU")
        
        print(f"✅ Render configurado: {engine}, {samples} muestras")
    
    def render_animation(self, output_path: str, format: str = "MP4"):
        """Renderiza la animación completa"""
        try:
            output_path = str(Path(output_path).with_suffix(''))
            
            # Configurar opciones de render de vídeo
            if format == "MP4":
                self.scene.render.image_settings.file_format = 'FFMPEG'
                self.scene.render.ffmpeg.codec = 'H264'
                self.scene.render.ffmpeg.format = 'MPEG4'
                self.scene.render.ffmpeg.use_lossless_output = False
                output_path += ".mp4"
            elif format == "WEBM":
                self.scene.render.image_settings.file_format = 'FFMPEG'
                self.scene.render.ffmpeg.codec = 'WEBM'
                output_path += ".webm"
            elif format == "PNG":
                self.scene.render.image_settings.file_format = 'PNG'
                output_path += "_####.png"
            
            # Establecer ruta de salida
            self.scene.render.filepath = output_path
            
            print(f"🎬 Renderizando animación: {output_path}")
            print(f"   Frames: {self.scene.frame_start}-{self.scene.frame_end}")
            print(f"   FPS: {self.scene.render.fps}")
            
            # Iniciar render
            bpy.ops.render.render(animation=True, write_still=True)
            
            print(f"✅ Animación renderizada: {output_path}")
            return True
        except Exception as e:
            print(f"❌ Error en render: {e}")
            return False
    
    def export_animation_config(self, filepath: str):
        """Exporta la configuración de animación como JSON"""
        config_data = {
            'name': self.config.name if self.config else 'animation',
            'frames': {
                'start': self.scene.frame_start,
                'end': self.scene.frame_end
            },
            'fps': self.scene.render.fps,
            'resolution': {
                'width': self.scene.render.resolution_x,
                'height': self.scene.render.resolution_y
            },
            'render_engine': self.scene.render.engine,
            'timestamp': datetime.now().isoformat()
        }
        
        with open(filepath, 'w') as f:
            json.dump(config_data, f, indent=2)
        
        print(f"✅ Configuración exportada: {filepath}")


class AnimationCommandGenerator:
    """Genera comandos de animación automáticamente"""
    
    @staticmethod
    def create_spinning_object(object_name: str, 
                               rotations: int = 2,
                               duration_frames: int = 250) -> str:
        """Crea comando para rotar un objeto"""
        end_angle = 360 * rotations
        return f"""
        animation = AnimationBuilder()
        animation.rotate_object('{object_name}', 'Z', 0, {end_angle}, 1, {duration_frames})
        animation.render_animation('spinning_{object_name}.mp4', 'MP4')
        """
    
    @staticmethod
    def create_camera_pan(start_pos: Tuple[float, float, float],
                         end_pos: Tuple[float, float, float],
                         duration_frames: int = 250) -> str:
        """Crea comando para hacer pan de cámara"""
        return f"""
        animation = AnimationBuilder()
        positions = [{start_pos}, {end_pos}]
        frames = [1, {duration_frames}]
        animation.add_camera_path('Camera', positions, frames)
        animation.render_animation('camera_pan.mp4', 'MP4')
        """
    
    @staticmethod
    def create_zoom_animation(focal_start: float = 50,
                             focal_end: float = 35,
                             duration_frames: int = 250) -> str:
        """Crea comando para efecto zoom"""
        return f"""
        animation = AnimationBuilder()
        animation.zoom_camera('Camera', {focal_start}, {focal_end}, 1, {duration_frames})
        animation.render_animation('zoom_animation.mp4', 'MP4')
        """


# Script de entrada para Blender
if __name__ == "__main__":
    print("=" * 50)
    print("ZULY Animation Engine v1.0")
    print("=" * 50)
    
    # Ejemplo de uso
    anim = AnimationBuilder()
    config = AnimationConfig(
        name="demo",
        end_frame=250,
        fps=30,
        format="MP4"
    )
    anim.set_config(config)
    
    print("✅ Sistema de animaciones cargado correctamente")
