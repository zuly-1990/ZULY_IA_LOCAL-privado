#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🆕 P-004/005/006 BATCH - Cilindros, Conos, Plano
Final del batch legacy
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
print("🆕 P-004/005/006 BATCH - Cilindros, Conos, Plano")
print("="*60)

# P-004: 2 Cilindros
print("\\n🆕 P-004 - Cilindros...")
cilindros = [
    ("P-004A_CilindroAlto", 0.5, 3.0, 32, "#795548"),    # Radio 0.5, alto 3m
    ("P-004B_CilindroAncho", 1.0, 1.5, 64, "#607D8B"),   # Radio 1.0, alto 1.5m
]

for nombre, radius, depth, verts, color in cilindros:
    print(f"🆕 {nombre}...")
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    
    bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=depth, vertices=verts, location=(0, 0, depth/2))
    obj = bpy.context.active_object
    obj.name = nombre
    
    mat = bpy.data.materials.new(name=f"Mat_{nombre}")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        r = int(color[1:3], 16)/255
        g = int(color[3:5], 16)/255
        b = int(color[5:7], 16)/255
        bsdf.inputs['Base Color'].default_value = (r, g, b, 1.0)
        bsdf.inputs['Roughness'].default_value = 0.4
    obj.data.materials.append(mat)
    
    luces = aplicar_iluminacion_profesional(obj)
    
    dist = max(radius, depth) * 2.5
    cam_pos = mathutils.Vector((dist, -dist, depth/2))
    bpy.ops.object.camera_add(location=cam_pos)
    cam = bpy.context.active_object
    direction = obj.location - cam.location
    cam.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
    bpy.context.scene.camera = cam
    
    output = f'./archivo_zuly/temp_arena/{nombre}.blend'
    bpy.ops.wm.save_as_mainfile(filepath=output)
    print(f"   ✅ {nombre}")

# P-005: 2 Conos
print("\\n🆕 P-005 - Conos...")
conos = [
    ("P-005A_ConoAlto", 0.8, 2.5, 32, "#FF9800"),      # Radio 0.8, alto 2.5m
    ("P-005B_ConoChato", 1.2, 1.0, 64, "#9C27B0"),      # Radio 1.2, alto 1m
]

for nombre, radius, depth, verts, color in conos:
    print(f"🆕 {nombre}...")
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    
    bpy.ops.mesh.primitive_cone_add(radius1=radius, depth=depth, vertices=verts, location=(0, 0, depth/2))
    obj = bpy.context.active_object
    obj.name = nombre
    
    mat = bpy.data.materials.new(name=f"Mat_{nombre}")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        r = int(color[1:3], 16)/255
        g = int(color[3:5], 16)/255
        b = int(color[5:7], 16)/255
        bsdf.inputs['Base Color'].default_value = (r, g, b, 1.0)
        bsdf.inputs['Roughness'].default_value = 0.5
    obj.data.materials.append(mat)
    
    luces = aplicar_iluminacion_profesional(obj)
    
    dist = max(radius, depth) * 2.5
    cam_pos = mathutils.Vector((dist, -dist, depth/2))
    bpy.ops.object.camera_add(location=cam_pos)
    cam = bpy.context.active_object
    direction = obj.location - cam.location
    cam.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
    bpy.context.scene.camera = cam
    
    output = f'./archivo_zuly/temp_arena/{nombre}.blend'
    bpy.ops.wm.save_as_mainfile(filepath=output)
    print(f"   ✅ {nombre}")

# P-006: 1 Plano
print("\\n🆕 P-006 - Plano...")
print("🆕 P-006A_PlanoBase...")
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

bpy.ops.mesh.primitive_plane_add(size=4, location=(0, 0, 0))
plano = bpy.context.active_object
plano.name = "P-006A_PlanoBase"

mat = bpy.data.materials.new(name="Mat_P-006A")
mat.use_nodes = True
bsdf = mat.node_tree.nodes.get("Principled BSDF")
if bsdf:
    bsdf.inputs['Base Color'].default_value = (0.9, 0.9, 0.9, 1.0)  # Blanco gris
    bsdf.inputs['Roughness'].default_value = 0.8
plano.data.materials.append(mat)

luces = aplicar_iluminacion_profesional(plano)

cam_pos = mathutils.Vector((5, -5, 3))
bpy.ops.object.camera_add(location=cam_pos)
cam = bpy.context.active_object
direction = mathutils.Vector((0, 0, 0)) - cam.location
cam.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
bpy.context.scene.camera = cam

output = './archivo_zuly/temp_arena/P-006A_PlanoBase.blend'
bpy.ops.wm.save_as_mainfile(filepath=output)
print("   ✅ P-006A_PlanoBase")

print("\\n" + "="*60)
print("✅ P-004/005/006 BATCH - 5 objetos listos (2+2+1)")
print("="*60)
'''

script_path = zuly_path / 'temp_p004_005_006_batch.py'
with open(script_path, 'w', encoding='utf-8') as f:
    f.write(script_batch)

blender_exe = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe"

print("🆕 P-004/005/006 BATCH (5 objetos)...")
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
print("\n✅ P-004/005/006 BATCH completado")
