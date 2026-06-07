#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🆕 CUB-001 V3 - CREACIÓN COMPLETA DESDE CERO
Todo en un solo script, paso a paso verificado
"""

import subprocess
import sys
from pathlib import Path

zuly_path = Path('c:/Users/Admin/Desktop/ZULY_IA_LOCAL')

script_completo = '''
import bpy
import sys
import mathutils

print("="*60)
print("🆕 CUB-001 V3 - CREACIÓN COMPLETA")
print("="*60)

# 1. LIMPIAR TODO ABSOLUTAMENTE
print("\\n1️⃣ Limpiando escena...")
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Eliminar TODOS los datos previos
for mesh in bpy.data.meshes:
    bpy.data.meshes.remove(mesh)
for mat in bpy.data.materials:
    bpy.data.materials.remove(mat)
for light in bpy.data.lights:
    bpy.data.lights.remove(light)

# 2. CREAR CUBO
print("2️⃣ Creando cubo...")
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 1))
cubo = bpy.context.active_object
cubo.name = "CUB-001"

# 3. APLICAR BEVEL
print("3️⃣ Aplicando bevel...")
bevel = cubo.modifiers.new(name="Bevel", type='BEVEL')
bevel.width = 0.08
bevel.segments = 4
bevel.limit_method = 'ANGLE'
bevel.angle_limit = 0.5236

# 4. CREAR MATERIAL AZUL #1A4DCC
print("4️⃣ Creando material azul #1A4DCC...")

# Borrar materiales del objeto si tiene
if cubo.data.materials:
    cubo.data.materials.clear()

# Crear material nuevo
mat = bpy.data.materials.new(name="Azul_CUB001")
mat.use_nodes = True

# Configurar nodos
nodes = mat.node_tree.nodes
links = mat.node_tree.links

# Limpiar nodos default
for node in list(nodes):
    if node.type != 'OUTPUT_MATERIAL':
        nodes.remove(node)

# Crear Principled BSDF
bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
bsdf.location = (0, 0)

# Color EXACTO #1A4DCC
# 26/255=0.102, 77/255=0.302, 204/255=0.8
r, g, b = 0.102, 0.302, 0.8
bsdf.inputs['Base Color'].default_value = (r, g, b, 1.0)
bsdf.inputs['Roughness'].default_value = 0.3

# Conectar a output
output = nodes.get('Material Output')
links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

# Asignar al objeto
mat.use_fake_user = False
cubo.data.materials.append(mat)

# Verificar
print(f"   Material: {mat.name}")
print(f"   Color RGB: ({r}, {g}, {b})")
c = bsdf.inputs['Base Color'].default_value
print(f"   Verificado: ({c[0]:.3f}, {c[1]:.3f}, {c[2]:.3f})")
print(f"   Hex: #{int(c[0]*255):02X}{int(c[1]*255):02X}{int(c[2]*255):02X}")

# 5. CREAR LUCES MANUALMENTE (SLIZ style)
print("\\n5️⃣ Creando iluminación...")

# Sol
bpy.ops.object.light_add(type='SUN', location=(5, -5, 10))
sol = bpy.context.active_object
sol.name = "Sol"
sol.data.energy = 5
direction = mathutils.Vector((0, 0, 0)) - sol.location
sol.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()

# Key
bpy.ops.object.light_add(type='AREA', location=(4, -3, 3))
key = bpy.context.active_object
key.name = "Key"
key.data.energy = 150
key.data.size = 3
direction = mathutils.Vector((0, 0, 1)) - key.location
key.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()

# Fill
bpy.ops.object.light_add(type='AREA', location=(-3, 2, 2))
fill = bpy.context.active_object
fill.name = "Fill"
fill.data.energy = 60
fill.data.size = 2
direction = mathutils.Vector((0, 0, 1)) - fill.location
fill.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()

# Rim
bpy.ops.object.light_add(type='SPOT', location=(0, -5, 3))
rim = bpy.context.active_object
rim.name = "Rim"
rim.data.energy = 180
rim.data.spot_size = 1.0
direction = mathutils.Vector((0, 0, 1)) - rim.location
rim.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()

print("   ✅ Sol, Key, Fill, Rim creadas")

# 6. CÁMARA
print("6️⃣ Creando cámara...")
bpy.ops.object.camera_add(location=(3, -4, 2.5))
cam = bpy.context.active_object
cam.name = "Camera"
direction = mathutils.Vector((0, 0, 1)) - cam.location
cam.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
bpy.context.scene.camera = cam

# 7. CONFIGURAR RENDER
bpy.context.scene.render.engine = 'BLENDER_EEVEE'
bpy.context.scene.render.resolution_x = 1920
bpy.context.scene.render.resolution_y = 1080

# 8. VERIFICACIÓN FINAL
print("\\n8️⃣ Verificación final...")
print(f"   Objeto: {cubo.name}")
print(f"   Material: {cubo.data.materials[0].name if cubo.data.materials else 'NINGUNO'}")
if cubo.data.materials:
    mat = cubo.data.materials[0]
    if mat.use_nodes:
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            c = bsdf.inputs['Base Color'].default_value
            print(f"   Color: #{int(c[0]*255):02X}{int(c[1]*255):02X}{int(c[2]*255):02X}")

# 9. GUARDAR
output = './archivo_zuly/temp_arena/CUB-001_Modelado_BiselRealista.blend'
print(f"\\n💾 Guardando en: {output}")
bpy.ops.wm.save_as_mainfile(filepath=output)

print("\\n" + "="*60)
print("✅ CUB-001 V3 COMPLETADO")
print("="*60)
'''

script_path = zuly_path / 'temp_cub001_v3.py'
with open(script_path, 'w', encoding='utf-8') as f:
    f.write(script_completo)

blender_exe = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe"

print("🆕 Creando CUB-001 V3 desde cero...")
result = subprocess.run(
    [blender_exe, '--background', '--python', str(script_path)],
    capture_output=True,
    text=True,
    encoding='utf-8',
    errors='ignore',
    cwd=str(zuly_path)
)

if result.stdout:
    print(result.stdout[-2500:] if len(result.stdout) > 2500 else result.stdout)

script_path.unlink()

print("\n" + "="*60)
print("🤖 Validando con JUES-BOT...")
print("="*60)
