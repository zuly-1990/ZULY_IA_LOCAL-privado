#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🆕 MAT-001/002/003 BATCH - 3 Materiales PBR
Metal Cromado, Vidrio Transparente, Emisivo Naranja
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
print("🆕 FASE 2 - MAT-001/002/003 (3 Materiales PBR)")
print("="*60)

# MAT-001: Metal Cromado
print("\\n🆕 MAT-001 - Material_Metal_Cromado...")
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(0, 0, 1), segments=32, ring_count=16)
esfera = bpy.context.active_object
esfera.name = "MAT-001_Material_Metal"

mat = bpy.data.materials.new(name="Mat_Metal_Cromado")
mat.use_nodes = True
bsdf = mat.node_tree.nodes.get("Principled BSDF")
if bsdf:
    bsdf.inputs['Base Color'].default_value = (0.95, 0.95, 0.97, 1.0)  # Plateado
    bsdf.inputs['Metallic'].default_value = 1.0  # 100% metal
    bsdf.inputs['Roughness'].default_value = 0.1  # Brillante
    bsdf.inputs['Specular'].default_value = 0.9
esfera.data.materials.append(mat)

luces = aplicar_iluminacion_profesional(esfera)
cam_pos = mathutils.Vector((3, -3, 2))
bpy.ops.object.camera_add(location=cam_pos)
cam = bpy.context.active_object
direction = esfera.location - cam.location
cam.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
bpy.context.scene.camera = cam

bpy.ops.wm.save_as_mainfile(filepath='./archivo_zuly/temp_arena/MAT-001_Material_Metal.blend')
print("   ✅ MAT-001_Material_Metal")

# MAT-002: Vidrio Transparente
print("\\n🆕 MAT-002 - Material_Vidrio...")
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(0, 0, 1), segments=32, ring_count=16)
esfera = bpy.context.active_object
esfera.name = "MAT-002_Material_Vidrio"

mat = bpy.data.materials.new(name="Mat_Vidrio_Transparente")
mat.use_nodes = True
mat.blend_method = 'BLEND'
bsdf = mat.node_tree.nodes.get("Principled BSDF")
if bsdf:
    bsdf.inputs['Base Color'].default_value = (1.0, 1.0, 1.0, 1.0)
    bsdf.inputs['Transmission'].default_value = 1.0
    bsdf.inputs['Roughness'].default_value = 0.0
    bsdf.inputs['IOR'].default_value = 1.45
    bsdf.inputs['Specular'].default_value = 0.9
esfera.data.materials.append(mat)

luces = aplicar_iluminacion_profesional(esfera)
cam_pos = mathutils.Vector((3, -3, 2))
bpy.ops.object.camera_add(location=cam_pos)
cam = bpy.context.active_object
direction = esfera.location - cam.location
cam.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
bpy.context.scene.camera = cam

bpy.ops.wm.save_as_mainfile(filepath='./archivo_zuly/temp_arena/MAT-002_Material_Vidrio.blend')
print("   ✅ MAT-002_Material_Vidrio")

# MAT-003: Emisivo Naranja
print("\\n🆕 MAT-003 - Material_Emisivo...")
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(0, 0, 1), segments=32, ring_count=16)
esfera = bpy.context.active_object
esfera.name = "MAT-003_Material_Emisivo"

mat = bpy.data.materials.new(name="Mat_Emisivo_Naranja")
mat.use_nodes = True
bsdf = mat.node_tree.nodes.get("Principled BSDF")
if bsdf:
    bsdf.inputs['Base Color'].default_value = (1.0, 0.42, 0.21, 1.0)  # Naranja
    bsdf.inputs['Emission'].default_value = (1.0, 0.42, 0.21, 1.0)
    bsdf.inputs['Emission Strength'].default_value = 5.0
    bsdf.inputs['Roughness'].default_value = 0.5
esfera.data.materials.append(mat)

luces = aplicar_iluminacion_profesional(esfera)
cam_pos = mathutils.Vector((3, -3, 2))
bpy.ops.object.camera_add(location=cam_pos)
cam = bpy.context.active_object
direction = esfera.location - cam.location
cam.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
bpy.context.scene.camera = cam

bpy.ops.wm.save_as_mainfile(filepath='./archivo_zuly/temp_arena/MAT-003_Material_Emisivo.blend')
print("   ✅ MAT-003_Material_Emisivo")

print("\\n" + "="*60)
print("✅ FASE 2 COMPLETADA - 3 materiales PBR listos")
print("="*60)
'''

script_path = zuly_path / 'temp_mat_batch.py'
with open(script_path, 'w', encoding='utf-8') as f:
    f.write(script_batch)

blender_exe = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe"

print("🆕 FASE 2 - MAT-001/002/003 (3 materiales)...")
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
print("\n✅ FASE 2 completada")
