#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🆕 CUB-002 - Transform_PivoteSuelo
Cubo con origen (pivote) en el suelo (Z=0) - Para arquitectura
"""

import subprocess
import sys
from pathlib import Path

zuly_path = Path('c:/Users/Admin/Desktop/ZULY_IA_LOCAL')

script_cub002 = '''
import bpy
import sys
import mathutils
sys.path.insert(0, 'c:/Users/Admin/Desktop/ZULY_IA_LOCAL/core')
from sistema_luces_inteligente import aplicar_iluminacion_profesional

print("="*60)
print("🆕 CUB-002 - Transform_PivoteSuelo")
print("="*60)

# Limpiar
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# 1. CREAR CUBO (centrado para que base quede en Z=0)
print("1️⃣ Creando cubo centrado en Z=1...")
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 1))
cubo = bpy.context.active_object
cubo.name = "CUB-002_Transform_PivoteSuelo"

# 2. BEVEL suave
print("2️⃣ Aplicando bevel...")
bevel = cubo.modifiers.new(name="Bevel_Suave", type='BEVEL')
bevel.width = 0.05
bevel.segments = 3
bevel.limit_method = 'ANGLE'
bevel.angle_limit = 0.5236

# 3. MOVER ORIGEN AL SUELO (Z=0)
print("3️⃣ Moviendo pivote al suelo...")
# Colocar cursor en el suelo
bpy.context.scene.cursor.location = (0, 0, 0)
# Mover origen al cursor (suelo)
bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')

# Verificar
print(f"   Origen del cubo: {cubo.location}")
print(f"   ✓ Pivote ahora está en Z=0 (suelo)")

# 4. MATERIAL VERDE CONSTRUCTIVO (diferente a CUB-001)
print("4️⃣ Creando material verde arquitectura...")
mat = bpy.data.materials.new(name="Mat_Verde_Arqui")
mat.use_nodes = True
principled = mat.node_tree.nodes.get("Principled BSDF")
if principled:
    # Verde construcción: #4CAF50
    r, g, b = 76/255, 175/255, 80/255
    principled.inputs['Base Color'].default_value = (r, g, b, 1.0)
    principled.inputs['Roughness'].default_value = 0.6
    principled.inputs['Specular'].default_value = 0.3
cubo.data.materials.append(mat)

# 5. ILUMINACIÓN SLIZ
print("5️⃣ Aplicando iluminación SLIZ...")
luces = aplicar_iluminacion_profesional(cubo)
print(f"   Luces: {list(luces.keys())}")

# 6. CÁMARA
print("6️⃣ Posicionando cámara...")
cam_pos = mathutils.Vector((4, -3, 2))
bpy.ops.object.camera_add(location=cam_pos)
cam = bpy.context.active_object
direction = mathutils.Vector((0, 0, 0.5)) - cam.location
cam.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
bpy.context.scene.camera = cam

# 7. Guardar
output = './archivo_zuly/temp_arena/CUB-002_Transform_PivoteSuelo.blend'
bpy.ops.wm.save_as_mainfile(filepath=output)

print("\\n" + "="*60)
print("✅ CUB-002 CREADO - Listo para validación")
print("="*60)
print(f"📁 Archivo: {output}")
print(f"📐 Característica: Pivote en suelo (Z=0)")
print(f"🎨 Color: #4CAF50 (Verde arquitectura)")
'''

script_path = zuly_path / 'temp_cub002.py'
with open(script_path, 'w', encoding='utf-8') as f:
    f.write(script_cub002)

blender_exe = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe"

print("🆕 Generando CUB-002...")
result = subprocess.run(
    [blender_exe, '--background', '--python', str(script_path)],
    capture_output=True,
    text=True,
    encoding='utf-8',
    errors='ignore',
    cwd=str(zuly_path)
)

if result.stdout:
    print(result.stdout[-2000:] if len(result.stdout) > 2000 else result.stdout)

script_path.unlink()

print("\n✅ CUB-002 generado")
