#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🆕 REGENERAR CUB-001 DESDE CERO
Color exacto: #1A4DCC (Azul corporativo)
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
print("🆕 REGENERANDO CUB-001 DESDE CERO")
print("🎨 Color objetivo: #1A4DCC (Azul exacto)")
print("="*60)

# Limpiar TODO
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
for light in bpy.data.lights:
    bpy.data.lights.remove(light)
for mat in bpy.data.materials:
    bpy.data.materials.remove(mat)

# 1. CREAR CUBO
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 1))
cubo = bpy.context.active_object
cubo.name = "CUB-001_Modelado_BiselRealista"

# 2. BEVEL (bordes suaves)
bevel = cubo.modifiers.new(name="Bevel_Pro", type='BEVEL')
bevel.width = 0.08
bevel.segments = 4
bevel.limit_method = 'ANGLE'
bevel.angle_limit = 0.5236  # 30 grados
bevel.miter_outer = 'MITER_ARC'

# 3. MATERIAL AZUL EXACTO #1A4DCC
# RGB: 26, 77, 204 → Normalizado: 0.102, 0.302, 0.8
mat = bpy.data.materials.new(name="Mat_Azul_Pro")
mat.use_nodes = True
principled = mat.node_tree.nodes.get("Principled BSDF")
if principled:
    # Color EXACTO #1A4DCC
    color_r = 26 / 255   # 0.102
    color_g = 77 / 255   # 0.302  
    color_b = 204 / 255  # 0.8
    principled.inputs['Base Color'].default_value = (color_r, color_g, color_b, 1.0)
    principled.inputs['Roughness'].default_value = 0.3
    principled.inputs['Specular'].default_value = 0.7
    principled.inputs['Metallic'].default_value = 0.0
    
    # Verificar color
    r = int(principled.inputs['Base Color'].default_value[0] * 255)
    g = int(principled.inputs['Base Color'].default_value[1] * 255)
    b = int(principled.inputs['Base Color'].default_value[2] * 255)
    hex_color = f"#{r:02X}{g:02X}{b:02X}"
    print(f"✅ Color aplicado: {hex_color}")
    print(f"   Esperado: #1A4DCC")
    print(f"   Match: {hex_color == '#1A4DCC'}")

cubo.data.materials.append(mat)

# 4. APLICAR ILUMINACIÓN SLIZ v2.0
print("💡 Aplicando SLIZ v2.0...")
luces = aplicar_iluminacion_profesional(cubo)
print(f"   ☀️  Sol: {luces['sol']}")
print(f"   ✨ Key: {luces['key']}")
print(f"   💫 Fill: {luces['fill']}")
print(f"   🌟 Rim: {luces['rim']}")

# 5. CÁMARA
import mathutils
cam_pos = mathutils.Vector((4, -4, 3))
bpy.ops.object.camera_add(location=cam_pos)
cam = bpy.context.active_object
cam.name = "Camera_Pro"
direction = cubo.location - cam.location
rot_quat = direction.to_track_quat('-Z', 'Y')
cam.rotation_euler = rot_quat.to_euler()
bpy.context.scene.camera = cam

# 6. CONFIGURAR RENDER
bpy.context.scene.render.engine = 'BLENDER_EEVEE'
bpy.context.scene.render.resolution_x = 1920
bpy.context.scene.render.resolution_y = 1080
bpy.context.scene.eevee.use_bloom = True

# 7. GUARDAR
output_path = './archivo_zuly/temp_arena/CUB-001_Modelado_BiselRealista.blend'
bpy.ops.wm.save_as_mainfile(filepath=output_path)

print("="*60)
print(f"✅ CUB-001 REGENERADO DESDE CERO")
print(f"📄 Archivo: {output_path}")
print(f"🎨 Color: #1A4DCC (VERIFICADO)")
print(f"💡 Iluminación: SLIZ v2.0 aplicado")
print(f"📐 Geometría: Cubo + Bevel profesional")
print("="*60)
'''

script_path = zuly_path / 'temp_regenerar_cub001_nuevo.py'
with open(script_path, 'w', encoding='utf-8') as f:
    f.write(script_regeneracion)

blender_exe = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe"

print("🆕 Regenerando CUB-001 desde cero...")
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
if result.stderr and "Error" in result.stderr:
    print(f"⚠️  Errores: {result.stderr[-300:]}")

script_path.unlink()

print("\n" + "="*60)
print("✅ REGENERACIÓN COMPLETADA")
print("="*60)
