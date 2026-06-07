"""
proyecto_animacion_cubo.py

PROYECTO: ANIMACIÓN SIMPLE CUBO (EJE Z)
=======================================

Objetivos:
- Animación de 5 segundos (120 frames)
- Movimiento simple en eje Z
- Motor EEVEE (rápido)
- Sin materiales (ahorro recursos)
"""

import sys
from pathlib import Path
import math

# Configuración básica
PROJECT_NAME = "Animacion_Cubo_Simple"
OUTPUT_DIR = Path("C:/Users/Admin/Desktop/ZULY_IA_LOCAL/export/animaciones")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

FPS = 24
DURATION_SECONDS = 5
TOTAL_FRAMES = FPS * DURATION_SECONDS

import bpy

# 1. Limpiar escena
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# 2. Configurar Render (EEVEE)
scene = bpy.context.scene
scene.render.engine = 'BLENDER_EEVEE'
scene.render.fps = FPS
scene.frame_start = 1
scene.frame_end = TOTAL_FRAMES
scene.render.resolution_x = 1280  # HD suave
scene.render.resolution_y = 720

# Salida de video
scene.render.image_settings.file_format = 'FFMPEG'
scene.render.ffmpeg.format = 'MPEG4'
scene.render.ffmpeg.codec = 'H264'
scene.render.filepath = str(OUTPUT_DIR / f"{PROJECT_NAME}.mp4")

print(f"Configurado: {TOTAL_FRAMES} frames @ {FPS} fps. EEVEE engine.")

# 3. Crear Cubo
bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
cubo = bpy.context.active_object
cubo.name = "Cubo_Animado"

# 4. Animar (Eje Z)
# Frame 1: Z = 0
cubo.location.z = 0
cubo.keyframe_insert(data_path="location", frame=1)

# Frame 60 (mitad): Z = 3
cubo.location.z = 3
cubo.keyframe_insert(data_path="location", frame=60)

# Frame 120 (final): Z = 0
cubo.location.z = 0
cubo.keyframe_insert(data_path="location", frame=120)

# Hacer la curva suave (interpolación Bezier por defecto)
# Opcional: Hacer bucle perfecto
for fcurve in cubo.animation_data.action.fcurves:
    for keyframe in fcurve.keyframe_points:
        keyframe.interpolation = 'BEZIER'

print("Animación creada: Rebote suave en Z.")

# 5. Cámara
bpy.ops.object.camera_add(location=(8, -8, 5))
cam = bpy.context.active_object
cam.rotation_euler = (math.radians(70), 0, math.radians(45))
scene.camera = cam

# 6. Luz Básica
bpy.ops.object.light_add(type='SUN', location=(5, 5, 10))
luz = bpy.context.active_object
luz.data.energy = 2.0

# 7. Guardar .blend
blend_path = OUTPUT_DIR / f"{PROJECT_NAME}.blend"
bpy.ops.wm.save_as_mainfile(filepath=str(blend_path))
print(f"Archivo guardado: {blend_path}")

# 8. Renderizar Animación
print("Iniciando render de animación...")
bpy.ops.render.render(animation=True)
print(f"Render completado: {scene.render.filepath}")
