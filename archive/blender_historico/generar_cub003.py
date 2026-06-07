#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🆕 CUB-003 - Modelado_MuroPro
Muro arquitectónico con proporciones reales (3x6x0.25m)
"""

import subprocess
import sys
from pathlib import Path

zuly_path = Path('c:/Users/Admin/Desktop/ZULY_IA_LOCAL')

script_cub003 = '''
import bpy
import sys
import mathutils
sys.path.insert(0, 'c:/Users/Admin/Desktop/ZULY_IA_LOCAL/core')
from sistema_luces_inteligente import aplicar_iluminacion_profesional

print("="*60)
print("🆕 CUB-003 - Modelado_MuroPro")
print("="*60)

# Limpiar
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# 1. CREAR CUBO BASE
print("1️⃣ Creando cubo base...")
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 1.5))  # Altura 3m → centro en 1.5
cubo = bpy.context.active_object
cubo.name = "CUB-003_Modelado_MuroPro"

# 2. ESCALAR A PROPORCIONES DE MURO
print("2️⃣ Escalando a proporciones muro (6x0.25x3)...")
# Dimensiones: Largo=6, Grosor=0.25, Alto=3
cubo.scale = (6, 0.25, 3)  # X=6m (largo), Y=0.25m (grosor), Z=3m (alto)
bpy.ops.object.transform_apply(scale=True)  # Aplicar escala

# 3. BEVEL (bordes suaves de construcción)
print("3️⃣ Aplicando bevel de construcción...")
bevel = cubo.modifiers.new(name="Bevel_Construccion", type='BEVEL')
bevel.width = 0.01  # 1cm de redondeo
bevel.segments = 2
bevel.limit_method = 'ANGLE'
bevel.angle_limit = 0.7854  # 45 grados

# 4. MATERIAL CONCRETO GRIS
print("4️⃣ Creando material concreto...")
mat = bpy.data.materials.new(name="Mat_Concreto_Muro")
mat.use_nodes = True
principled = mat.node_tree.nodes.get("Principled BSDF")
if principled:
    # Gris concreto: #8C8C8C
    r, g, b = 140/255, 140/255, 140/255
    principled.inputs['Base Color'].default_value = (r, g, b, 1.0)
    principled.inputs['Roughness'].default_value = 0.8  # Muy rugoso
    principled.inputs['Specular'].default_value = 0.2
cubo.data.materials.append(mat)

# 5. ILUMINACIÓN SLIZ
print("5️⃣ Aplicando iluminación SLIZ...")
luces = aplicar_iluminacion_profesional(cubo)
print(f"   Luces: {list(luces.keys())}")

# 6. CÁMARA (vista frontal del muro)
print("6️⃣ Posicionando cámara...")
cam_pos = mathutils.Vector((0, -8, 1.5))  # Frente al muro, altura media
bpy.ops.object.camera_add(location=cam_pos)
cam = bpy.context.active_object
direction = mathutils.Vector((0, 0, 1.5)) - cam.location
cam.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
bpy.context.scene.camera = cam

# 7. Guardar
output = './archivo_zuly/temp_arena/CUB-003_Modelado_MuroPro.blend'
bpy.ops.wm.save_as_mainfile(filepath=output)

print("\\n" + "="*60)
print("✅ CUB-003 CREADO - Muro arquitectónico listo")
print("="*60)
print(f"📁 Archivo: {output}")
print(f"📐 Dimensiones: 6m (largo) x 0.25m (grosor) x 3m (alto)")
print(f"🎨 Color: #8C8C8C (Concreto gris)")
print(f"🏗️ Uso: Arquitectura, muros, construcción")
'''

script_path = zuly_path / 'temp_cub003.py'
with open(script_path, 'w', encoding='utf-8') as f:
    f.write(script_cub003)

blender_exe = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe"

print("🆕 Generando CUB-003 (Muro Arquitectónico)...")
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

print("\n✅ CUB-003 generado")
