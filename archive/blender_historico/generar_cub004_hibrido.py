#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 CUB-004-HIBRIDO - Combinación de CUB-001 + CUB-002 + CUB-003
Bevel profesional + Pivote en suelo + Proporciones muro
"""

import subprocess
import sys
from pathlib import Path

zuly_path = Path('c:/Users/Admin/Desktop/ZULY_IA_LOCAL')

script_hibrido = '''
import bpy
import sys
import mathutils
sys.path.insert(0, 'c:/Users/Admin/Desktop/ZULY_IA_LOCAL/core')
from sistema_luces_inteligente import aplicar_iluminacion_profesional

print("="*60)
print("🧪 CUB-004-HIBRIDO - Prueba Combinada")
print("="*60)
print("Combina: Bevel(CUB-001) + PivoteSuelo(CUB-002) + MuroPro(CUB-003)")
print("="*60)

# Limpiar
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# 1. CREAR CUBO BASE (proporciones muro CUB-003)
print("1️⃣ Creando base tipo muro (6x0.25x3)...")
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 1.5))
cubo = bpy.context.active_object
cubo.name = "CUB-004-HIBRIDO_Prueba"

# Escalar a proporciones muro (CUB-003)
cubo.scale = (6, 0.25, 3)
bpy.ops.object.transform_apply(scale=True)

# 2. BEVEL PROFESIONAL (CUB-001 - bisel realista)
print("2️⃣ Aplicando bevel profesional (CUB-001 style)...")
bevel = cubo.modifiers.new(name="Bevel_Pro", type='BEVEL')
bevel.width = 0.08  # Bevel más marcado como CUB-001
bevel.segments = 4  # Más segmentos = más suave
bevel.limit_method = 'ANGLE'
bevel.angle_limit = 0.5236  # 30 grados
bevel.miter_outer = 'MITER_ARC'  # Esquinas redondeadas

# 3. PIVOTE EN SUELO (CUB-002)
print("3️⃣ Moviendo pivote al suelo (CUB-002 style)...")
bpy.context.scene.cursor.location = (0, 0, 0)
bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
print(f"   ✓ Pivote en Z=0 (suelo): {cubo.location}")

# 4. MATERIAL HÍBRIDO - Gris con toque azulado (mezcla CUB-001 + CUB-003)
print("4️⃣ Creando material híbrido...")
mat = bpy.data.materials.new(name="Mat_Hibrido_ZULY")
mat.use_nodes = True
principled = mat.node_tree.nodes.get("Principled BSDF")
if principled:
    # Color híbrido: #607D8B (Blue Grey - entre azul CUB-001 y gris CUB-003)
    r, g, b = 96/255, 125/255, 139/255
    principled.inputs['Base Color'].default_value = (r, g, b, 1.0)
    principled.inputs['Roughness'].default_value = 0.5  # Intermedio
    principled.inputs['Specular'].default_value = 0.5
    principled.inputs['Metallic'].default_value = 0.1  # Ligeramente metálico
cubo.data.materials.append(mat)

# 5. ILUMINACIÓN SLIZ
print("5️⃣ Aplicando iluminación SLIZ v2.0...")
luces = aplicar_iluminacion_profesional(cubo)
print(f"   Luces: {list(luces.keys())}")

# 6. CÁMARA
print("6️⃣ Posicionando cámara...")
cam_pos = mathutils.Vector((5, -5, 2))
bpy.ops.object.camera_add(location=cam_pos)
cam = bpy.context.active_object
direction = cubo.location - cam.location
cam.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
bpy.context.scene.camera = cam

# 7. Render settings
bpy.context.scene.render.engine = 'BLENDER_EEVEE'
bpy.context.scene.render.resolution_x = 1920
bpy.context.scene.render.resolution_y = 1080
bpy.context.scene.eevee.use_bloom = True
bpy.context.scene.eevee.bloom_intensity = 0.05

# 8. Guardar
output = './archivo_zuly/temp_arena/CUB-004-HIBRIDO_Prueba.blend'
bpy.ops.wm.save_as_mainfile(filepath=output)

print("\\n" + "="*60)
print("✅ CUB-004-HIBRIDO CREADO")
print("="*60)
print(f"📁 Archivo: {output}")
print(f"📐 Características:")
print(f"   • Forma: Muro (6x0.25x3) - CUB-003")
print(f"   • Bevel: Profesional 4 segmentos - CUB-001")
print(f"   • Pivote: En suelo Z=0 - CUB-002")
print(f"   • Color: #607D8B Blue Grey (híbrido)")
print("="*60)
'''

script_path = zuly_path / 'temp_hibrido.py'
with open(script_path, 'w', encoding='utf-8') as f:
    f.write(script_hibrido)

blender_exe = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe"

print("🧪 Generando CUB-004-HIBRIDO (combinación de 3 patrones)...")
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

print("\n✅ CUB-004-HIBRIDO generado")
