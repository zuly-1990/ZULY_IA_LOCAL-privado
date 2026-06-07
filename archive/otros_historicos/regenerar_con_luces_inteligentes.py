#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔄 REGENERAR CUBO CON ILUMINACIÓN INTELIGENTE
Corrige las luces desordenadas del patrón CUB001_v2
"""

import subprocess
import sys
from pathlib import Path

zuly_path = Path('c:/Users/Admin/Desktop/ZULY_IA_LOCAL')

script_regeneracion = '''
import bpy
import sys
sys.path.insert(0, 'c:/Users/Admin/Desktop/ZULY_IA_LOCAL/core')
from sistema_luces_inteligente import aplicar_iluminacion_profesional

print("="*60)
print("🤖 ZULY: Regenerando CUB-001 con Iluminación Inteligente")
print("="*60)

# Limpiar
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
for light in bpy.data.lights:
    bpy.data.lights.remove(light)

# Crear cubo con bisel profesional
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 1))
cubo = bpy.context.active_object
cubo.name = "CUB001_v2_IluminacionCorregida"

# BEVEL profesional
bevel = cubo.modifiers.new(name="Bevel_Pro", type='BEVEL')
bevel.width = 0.08
bevel.segments = 4
bevel.limit_method = 'ANGLE'
bevel.angle_limit = 0.5236
bevel.miter_outer = 'MITER_ARC'

# Material azul profesional
mat = bpy.data.materials.new(name="Mat_Azul_Pro")
mat.use_nodes = True
principled = mat.node_tree.nodes.get("Principled BSDF")
if principled:
    principled.inputs['Base Color'].default_value = (0.1, 0.3, 0.8, 1.0)
    principled.inputs['Roughness'].default_value = 0.3
    principled.inputs['Specular'].default_value = 0.7
cubo.data.materials.append(mat)

# APLICAR SISTEMA DE LUCES INTELIGENTE
luces = aplicar_iluminacion_profesional(cubo)
print(f"💡 Sistema de Iluminación Inteligente aplicado:")
print(f"   Key:   {luces['key']}   (Luz principal 45° frontal)")
print(f"   Fill:  {luces['fill']}  (Luz de relleno suave)")
print(f"   Rim:   {luces['rim']}    (Luz de contorno trasera)")

# Cámara profesional posicionada correctamente
import mathutils
dims = cubo.dimensions
radio = max(dims) * 1.8
cam_pos = mathutils.Vector((radio * 0.7, -radio * 0.7, dims.z * 0.8))

bpy.ops.object.camera_add(location=cam_pos)
cam = bpy.context.active_object
cam.name = "Camera_Profesional"

# Apuntar cámara al centro del objeto
direction = cubo.location - cam.location
rot_quat = direction.to_track_quat('-Z', 'Y')
cam.rotation_euler = rot_quat.to_euler()

bpy.context.scene.camera = cam

# Render settings profesionales
bpy.context.scene.render.engine = 'BLENDER_EEVEE'
bpy.context.scene.render.resolution_x = 1920
bpy.context.scene.render.resolution_y = 1080
bpy.context.scene.render.resolution_percentage = 100
bpy.context.scene.eevee.use_bloom = True
bpy.context.scene.eevee.bloom_intensity = 0.05

# Guardar
blend_path = './archivo_zuly/temp_arena/CUB001_v2_IluminacionCorregida.blend'
bpy.ops.wm.save_as_mainfile(filepath=blend_path)

print(f"✅ Guardado: {blend_path}")
print(f"   Vértices: {len(cubo.data.vertices)}")
print(f"   Modificadores: {len(cubo.modifiers)}")
print(f"   Iluminación: 3-Point Professional (SLIZ)")
'''

script_path = zuly_path / 'temp_regenerar_luces.py'
with open(script_path, 'w', encoding='utf-8') as f:
    f.write(script_regeneracion)

blender_exe = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe"

print("🔄 Ejecutando regeneración con iluminación inteligente...")
result = subprocess.run(
    [blender_exe, '--background', '--python', str(script_path)],
    capture_output=True,
    text=True,
    cwd=str(zuly_path)
)

print(result.stdout[-1500:] if len(result.stdout) > 1500 else result.stdout)
if result.stderr and "Error" in result.stderr:
    print(f"⚠️  Errores: {result.stderr[-500:]}")

script_path.unlink()

print("\n" + "="*60)
print("✅ REGENERACIÓN COMPLETADA")
print("="*60)
print("📄 Nuevo archivo: CUB001_v2_IluminacionCorregida.blend")
print("💡 Iluminación: Sistema 3-Point Inteligente (SLIZ)")
print("📍 Ubicación: archivo_zuly/temp_arena/")
print("="*60)
