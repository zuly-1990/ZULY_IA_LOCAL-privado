#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🆕 FASE 3 - LUZ-001/002 (2 Sistemas Iluminación)
3-Point Professional + HDRI Ambiente
"""

import subprocess
import sys
from pathlib import Path

zuly_path = Path('c:/Users/Admin/Desktop/ZULY_IA_LOCAL')

script_batch = '''
import bpy
import sys
sys.path.insert(0, 'c:/Users/Admin/Desktop/ZULY_IA_LOCAL/core')
from sistema_luces_inteligente import aplicar_iluminacion_profesional
import mathutils

print("="*60)
print("🆕 FASE 3 - LUZ-001/002 (2 Iluminaciones)")
print("="*60)

# LUZ-001: Iluminación 3-Point (ya la tenemos, documentar)
print("\\n🆕 LUZ-001 - Iluminacion_3Point...")
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

bpy.ops.mesh.primitive_cube_add(size=1.5, location=(0, 0, 0.75))
cubo = bpy.context.active_object
cubo.name = "LUZ-001_Demo_3Point"

# Material neutro
mat = bpy.data.materials.new(name="Mat_Neutro")
mat.use_nodes = True
bsdf = mat.node_tree.nodes.get("Principled BSDF")
if bsdf:
    bsdf.inputs['Base Color'].default_value = (0.7, 0.7, 0.7, 1.0)
    bsdf.inputs['Roughness'].default_value = 0.5
cubo.data.materials.append(mat)

# SLIZ v2.0 ya es 3-Point
luces = aplicar_iluminacion_profesional(cubo)
print(f"   💡 Luces 3-Point: {list(luces.keys())}")

cam_pos = mathutils.Vector((4, -3, 2))
bpy.ops.object.camera_add(location=cam_pos)
cam = bpy.context.active_object
direction = cubo.location - cam.location
cam.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
bpy.context.scene.camera = cam

bpy.ops.wm.save_as_mainfile(filepath='./archivo_zuly/temp_arena/LUZ-001_Iluminacion_3Point.blend')
print("   ✅ LUZ-001_Iluminacion_3Point")

# LUZ-002: Iluminación HDRI (simulada con world)
print("\\n🆕 LUZ-002 - Iluminacion_HDRI...")
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

bpy.ops.mesh.primitive_cube_add(size=1.5, location=(0, 0, 0.75))
cubo = bpy.context.active_object
cubo.name = "LUZ-002_Demo_HDRI"

mat = bpy.data.materials.new(name="Mat_Neutro_HDRI")
mat.use_nodes = True
bsdf = mat.node_tree.nodes.get("Principled BSDF")
if bsdf:
    bsdf.inputs['Base Color'].default_value = (0.6, 0.6, 0.6, 1.0)
    bsdf.inputs['Roughness'].default_value = 0.5
cubo.data.materials.append(mat)

# Configurar World con HDRI-like (gradiente simple)
world = bpy.context.scene.world
world.use_nodes = True
bg = world.node_tree.nodes.get('Background')
if bg:
    # Simular HDRI con color cielo
    bg.inputs['Color'].default_value = (0.3, 0.5, 0.8, 1.0)  # Azul cielo
    bg.inputs['Strength'].default_value = 1.5

# Añadir SLIZ también
luces = aplicar_iluminacion_profesional(cubo)
print(f"   💡 HDRI + Luces: {list(luces.keys())}")

cam_pos = mathutils.Vector((4, -3, 2))
bpy.ops.object.camera_add(location=cam_pos)
cam = bpy.context.active_object
direction = cubo.location - cam.location
cam.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
bpy.context.scene.camera = cam

bpy.ops.wm.save_as_mainfile(filepath='./archivo_zuly/temp_arena/LUZ-002_Iluminacion_HDRI.blend')
print("   ✅ LUZ-002_Iluminacion_HDRI")

print("\\n" + "="*60)
print("✅ FASE 3 COMPLETADA - 2 iluminaciones listas")
print("="*60)
'''

script_path = zuly_path / 'temp_luz_batch.py'
with open(script_path, 'w', encoding='utf-8') as f:
    f.write(script_batch)

blender_exe = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe"

print("🆕 FASE 3 - LUZ-001/002 (2 iluminaciones)...")
result = subprocess.run(
    [str(blender_exe), '--background', '--python', str(script_path)],
    capture_output=True,
    text=True,
    encoding='utf-8',
    errors='ignore',
    cwd=str(zuly_path)
)

if result.stdout:
    print(result.stdout[-2000:] if len(result.stdout) > 2000 else result.stdout)

script_path.unlink()
print("\n✅ FASE 3 completada")
