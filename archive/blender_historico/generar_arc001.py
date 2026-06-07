#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🆕 ARC-001 - MuroLadrillo_Carga
Muro de carga estructural con proporciones reales (Perú/Latam)
Dimensiones: 6m largo x 0.15m grosor x 2.7m alto (estándar local)
"""

import subprocess
import sys
from pathlib import Path

zuly_path = Path('c:/Users/Admin/Desktop/ZULY_IA_LOCAL')

script_arc001 = '''
import bpy
import sys
import mathutils
sys.path.insert(0, 'c:/Users/Admin/Desktop/ZULY_IA_LOCAL/core')
from sistema_luces_inteligente import aplicar_iluminacion_profesional

print("="*60)
print("🆕 ARC-001 - MuroLadrillo_Carga")
print("="*60)
print("Muro estructural real - Dimensiones Perú/Latam estándar")
print("="*60)

# Limpiar
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# 1. CREAR CUBO BASE
print("1️⃣ Creando muro de carga...")
# Centro en altura/2 para que base quede en Z=0
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 1.35))
muro = bpy.context.active_object
muro.name = "ARC-001_MuroLadrillo_Carga"

# 2. ESCALAR A DIMENSIONES REALES (Perú/Latam estándar)
print("2️⃣ Aplicando dimensiones reales 6x0.15x2.7m...")
# Largo: 6m, Grosor: 0.15m (ladrillo), Alto: 2.7m (techo estándar)
muro.scale = (6, 0.15, 2.7)
bpy.ops.object.transform_apply(scale=True)
print(f"   📐 Dimensiones: 6.0m x 0.15m x 2.7m")

# 3. BEVEL SUAVE (bordes de construcción real)
print("3️⃣ Aplicando bevel de construcción...")
bevel = muro.modifiers.new(name="Bevel_Construccion", type='BEVEL')
bevel.width = 0.005  # 5mm - junta de construcción
bevel.segments = 2
bevel.limit_method = 'ANGLE'
bevel.angle_limit = 0.7854

# 4. PIVOTE EN SUELO (CUB-002 style)
print("4️⃣ Ajustando pivote al suelo...")
bpy.context.scene.cursor.location = (0, 0, 0)
bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
print(f"   ✓ Pivote en Z=0 (suelo)")

# 5. MATERIAL LADRILLO REALISTA
print("5️⃣ Creando material ladrillo...")
mat = bpy.data.materials.new(name="Mat_Ladrillo_Carga")
mat.use_nodes = True
bsdf = mat.node_tree.nodes.get("Principled BSDF")
if bsdf:
    # Color ladrillo quemado: #B95C45
    r, g, b = 185/255, 92/255, 69/255
    bsdf.inputs['Base Color'].default_value = (r, g, b, 1.0)
    bsdf.inputs['Roughness'].default_value = 0.9  # Muy rugoso
    bsdf.inputs['Specular'].default_value = 0.1
    bsdf.inputs['Subsurface'].default_value = 0.02
    bsdf.inputs['Subsurface Color'].default_value = (0.5, 0.25, 0.15, 1.0)
muro.data.materials.append(mat)

# 6. ILUMINACIÓN SLIZ
print("6️⃣ Aplicando iluminación SLIZ v2.0...")
luces = aplicar_iluminacion_profesional(muro)
print(f"   💡 Luces: {list(luces.keys())}")

# 7. CÁMARA (vista lateral del muro)
print("7️⃣ Posicionando cámara...")
cam_pos = mathutils.Vector((8, -6, 1.5))
bpy.ops.object.camera_add(location=cam_pos)
cam = bpy.context.active_object
direction = mathutils.Vector((0, 0, 1.35)) - cam.location
cam.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
bpy.context.scene.camera = cam

# 8. Render settings
bpy.context.scene.render.engine = 'BLENDER_EEVEE'
bpy.context.scene.render.resolution_x = 1920
bpy.context.scene.render.resolution_y = 1080
bpy.context.scene.eevee.use_bloom = True
bpy.context.scene.eevee.bloom_intensity = 0.03

# 9. Guardar
output = './archivo_zuly/temp_arena/ARC-001_MuroLadrillo_Carga.blend'
bpy.ops.wm.save_as_mainfile(filepath=output)

print("\\n" + "="*60)
print("✅ ARC-001 MURO LADRILLO CREADO")
print("="*60)
print(f"📁 Archivo: {output}")
print(f"📐 Dimensiones reales: 6.0m x 0.15m x 2.7m")
print(f"🏗️  Tipo: Muro de carga estructural")
print(f"🧱 Material: Ladrillo quemado #B95C45")
print(f"🎯 Pivote: En suelo (Z=0)")
print(f"⚖️  Uso: Construcción civil - muros de albañilería")
print("="*60)
'''

script_path = zuly_path / 'temp_arc001.py'
with open(script_path, 'w', encoding='utf-8') as f:
    f.write(script_arc001)

blender_exe = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe"

print("🆕 Generando ARC-001 MuroLadrillo_Carga...")
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

print("\n✅ ARC-001 generado")
