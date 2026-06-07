#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🏛️ MODELO 1: Pabellón Moderno Minimalista
Patrones: CUB-003 + CUB-001 + MAT-002 + P-004
"""

import subprocess
import sys
from pathlib import Path

zuly_path = Path('c:/Users/Admin/Desktop/ZULY_IA_LOCAL')

script = '''
import bpy
import bmesh
import mathutils
from math import radians

print("="*70)
print("🏛️ MODELO 1: Pabellon Moderno Minimalista")
print("="*70)

# Limpiar
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# 1. MUROS (CUB-003 style) - Estructura principal 6m x 0.15m x 2.7m
print("📦 Creando muros arquitectonicos...")
for i, x in enumerate([-2.5, 0, 2.5]):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x, 0, 1.35))
    muro = bpy.context.active_object
    muro.name = f"Muro_{i+1}"
    muro.scale = (0.075, 3, 1.35)  # 0.15m x 6m x 2.7m
    
    # Bevel (CUB-001 style)
    bevel = muro.modifiers.new(name="Bevel", type='BEVEL')
    bevel.width = 0.005
    bevel.segments = 2
    bevel.limit_method = 'ANGLE'
    
    # Material hormigon
    mat = bpy.data.materials.new(name=f"Hormigon_{i+1}")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs['Base Color'].default_value = (0.75, 0.73, 0.7, 1.0)  # Gris claro
    bsdf.inputs['Roughness'].default_value = 0.9
    muro.data.materials.append(mat)

# 2. COLUMNA CENTRAL (P-004 style) - Cilindro 3m alto
print("📦 Creando columna central...")
bpy.ops.mesh.primitive_cylinder_add(radius=0.3, depth=3, location=(0, 0, 1.5))
columna = bpy.context.active_object
columna.name = "Columna_Central"

mat_col = bpy.data.materials.new(name="Columna_Metal")
mat_col.use_nodes = True
bsdf = mat_col.node_tree.nodes["Principled BSDF"]
bsdf.inputs['Base Color'].default_value = (0.25, 0.25, 0.27, 1.0)  # Metal oscuro
bsdf.inputs['Metallic'].default_value = 0.8
bsdf.inputs['Roughness'].default_value = 0.3
columna.data.materials.append(mat_col)

# 3. FACHADA VIDRIO (MAT-002 style) - Paneles de vidrio
print("📦 Creando fachada de vidrio...")
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 3, 1.35))
vidrio = bpy.context.active_object
vidrio.name = "Fachada_Vidrio"
vidrio.scale = (3, 1, 1.35)
bpy.ops.transform.rotate(value=radians(90), orient_axis='X')

mat_vidrio = bpy.data.materials.new(name="Vidrio_Fachada")
mat_vidrio.use_nodes = True
bsdf = mat_vidrio.node_tree.nodes["Principled BSDF"]
bsdf.inputs['Base Color'].default_value = (0.9, 0.95, 1.0, 1.0)
bsdf.inputs['Roughness'].default_value = 0.0
bsdf.inputs['Transmission'].default_value = 0.9
bsdf.inputs['IOR'].default_value = 1.45
vidrio.data.materials.append(mat_vidrio)

# 4. TECHO (CUB-003 style)
print("📦 Creando techo...")
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 2.85))
techo = bpy.context.active_object
techo.name = "Techo"
techo.scale = (3.5, 3.5, 0.05)

mat_techo = bpy.data.materials.new(name="Techo_Blanco")
mat_techo.use_nodes = True
bsdf = mat_techo.node_tree.nodes["Principled BSDF"]
bsdf.inputs['Base Color'].default_value = (1.0, 1.0, 1.0, 1.0)
bsdf.inputs['Roughness'].default_value = 0.8
techo.data.materials.append(mat_techo)

# 5. Iluminación
print("💡 Configurando iluminacion...")
bpy.ops.object.light_add(type='AREA', location=(0, -2, 2.5))
key = bpy.context.active_object
key.name = "Key_Light"
key.data.energy = 150
key.data.size = 3

bpy.ops.object.light_add(type='SUN', location=(5, 5, 10))
sun = bpy.context.active_object
sun.name = "Sun"
sun.data.energy = 3

# 6. Cámara
bpy.ops.object.camera_add(location=(8, -6, 3))
cam = bpy.context.active_object
cam.name = "Camara_Pabellon"
cam.rotation_euler = (mathutils.Vector((1.1, 0, 0.8))).to_tuple()
bpy.context.scene.camera = cam

# Guardar
output = './archivo_zuly/temp_arena/MOD-001_Pabellon_Minimalista.blend'
print(f"\\n💾 Guardando {output}...")
bpy.ops.wm.save_as_mainfile(filepath=output)

print("\\n" + "="*70)
print("✅ MODELO 1 COMPLETADO: Pabellon Moderno Minimalista")
print("📊 Elementos: 3 muros + 1 columna + vidrio + techo")
print("="*70)
'''

script_path = zuly_path / 'temp_mod1.py'
with open(script_path, 'w', encoding='utf-8') as f:
    f.write(script)

blender_exe = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe"

print("🏛️ Creando MODELO 1: Pabellon Moderno Minimalista...")
result = subprocess.run(
    [str(blender_exe), '--background', '--python', str(script_path)],
    capture_output=True, text=True, encoding='utf-8', errors='ignore',
    cwd=str(zuly_path)
)

if result.stdout:
    print(result.stdout[-1500:] if len(result.stdout) > 1500 else result.stdout)

script_path.unlink()
print("\n✅ MOD-001 creado")
