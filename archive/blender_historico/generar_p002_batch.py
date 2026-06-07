#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🆕 P-002 BATCH - 5 Esferas Variantes
UV Sphere, ICO Sphere, y variantes de tamaño
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
print("🆕 P-002 BATCH - 5 Esferas Variantes")
print("="*60)

variantes = [
    ("P-002A_EsferaUV_1m", 1.0, 32, 16, "#E91E63"),      # UV Sphere 1m
    ("P-002B_EsferaUV_2m", 2.0, 64, 32, "#673AB7"),      # UV Sphere 2m alta res
    ("P-002C_EsferaICO_1m", 1.0, 2, 0, "#00BCD4"),       # ICO Sphere 1m
    ("P-002D_EsferaICO_05m", 0.5, 1, 0, "#8BC34A"),      # ICO Sphere 0.5m baja res
    ("P-002E_EsferaUV_05m", 0.5, 16, 8, "#FFC107"),      # UV Sphere 0.5m
]

for nombre, radius, seg, rings, color in variantes:
    print(f"\\n🆕 {nombre}...")
    
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    
    # Crear esfera (UV o ICO según rings)
    if rings == 0:  # ICO Sphere
        bpy.ops.mesh.primitive_ico_sphere_add(radius=radius, subdivisions=seg, location=(0, 0, radius))
    else:  # UV Sphere
        bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, segments=seg, ring_count=rings, location=(0, 0, radius))
    
    esfera = bpy.context.active_object
    esfera.name = nombre
    
    # Material
    mat = bpy.data.materials.new(name=f"Mat_{nombre}")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        r = int(color[1:3], 16)/255
        g = int(color[3:5], 16)/255
        b = int(color[5:7], 16)/255
        bsdf.inputs['Base Color'].default_value = (r, g, b, 1.0)
        bsdf.inputs['Roughness'].default_value = 0.3
    esfera.data.materials.append(mat)
    
    # Iluminación
    luces = aplicar_iluminacion_profesional(esfera)
    
    # Cámara
    dist = radius * 3
    cam_pos = mathutils.Vector((dist, -dist, radius))
    bpy.ops.object.camera_add(location=cam_pos)
    cam = bpy.context.active_object
    direction = esfera.location - cam.location
    cam.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
    bpy.context.scene.camera = cam
    
    # Guardar
    output = f'./archivo_zuly/temp_arena/{nombre}.blend'
    bpy.ops.wm.save_as_mainfile(filepath=output)
    print(f"   ✅ {nombre}")

print("\\n" + "="*60)
print("✅ P-002 BATCH - 5 esferas listas")
print("="*60)
'''

script_path = zuly_path / 'temp_p002_batch.py'
with open(script_path, 'w', encoding='utf-8') as f:
    f.write(script_batch)

blender_exe = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe"

print("🆕 P-002 BATCH (5 esferas)...")
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
print("\n✅ P-002 BATCH completado")
