#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 MODELO 5: Estación Espacial Orbital
Patrones: P-002E + CUB-005 + MAT-001 + MAT-003 + LUZ-002
"""

import subprocess
from pathlib import Path

zuly_path = Path('c:/Users/Admin/Desktop/ZULY_IA_LOCAL')

script = '''
import bpy
import mathutils
from math import radians

print("="*70)
print("🚀 MODELO 5: Estacion Espacial Orbital")
print("="*70)

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# MÓDULOS HABITABLES (P-002E style) - Esferas UV conectadas
print("🚀 Creando modulos habitables...")
modulos = [
    ("Modulo_A", (0, 0, 0), 1.5, (0.85, 0.9, 0.95)),
    ("Modulo_B", (4, 0, 0), 1.2, (0.75, 0.85, 0.9)),
    ("Modulo_C", (-3.5, 2, 0), 1.0, (0.9, 0.85, 0.8)),
]

for nombre, loc, radio, color in modulos:
    bpy.ops.mesh.primitive_uv_sphere_add(radius=radio, location=loc, segments=24, ring_count=12)
    mod = bpy.context.active_object
    mod.name = nombre
    
    # Material metal exterior (MAT-001 style)
    mat = bpy.data.materials.new(name=f"Metal_{nombre}")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs['Base Color'].default_value = (*color, 1.0)
    bsdf.inputs['Metallic'].default_value = 0.95
    bsdf.inputs['Roughness'].default_value = 0.25
    mod.data.materials.append(mat)

# UNIONES ENTRE MÓDULOS (CUB-005 style) - Boolean simulation conectores
print("🚀 Creando conectores entre modulos...")
conectores = [
    ((0, 0, 0), (4, 0, 0)),
    ((0, 0, 0), (-3.5, 2, 0)),
]

for start, end in conectores:
    mid_x = (start[0] + end[0]) / 2
    mid_y = (start[1] + end[1]) / 2
    mid_z = (start[2] + end[2]) / 2
    
    bpy.ops.mesh.primitive_cylinder_add(radius=0.4, depth=2.5, location=(mid_x, mid_y, mid_z))
    conn = bpy.context.active_object
    conn.name = f"Conector_{start}_{end}"
    
    # Rotar para conectar
    direction = mathutils.Vector(end) - mathutils.Vector(start)
    conn.rotation_euler = direction.to_track_quat('Z', 'Y').to_euler()
    
    mat_conn = bpy.data.materials.new(name=f"Mat_{conn.name}")
    mat_conn.use_nodes = True
    bsdf = mat_conn.node_tree.nodes["Principled BSDF"]
    bsdf.inputs['Base Color'].default_value = (0.6, 0.6, 0.62, 1.0)
    bsdf.inputs['Metallic'].default_value = 0.8
    bsdf.inputs['Roughness'].default_value = 0.4
    conn.data.materials.append(mat_conn)

# PANELES SOLARES
print("🚀 Creando paneles solares...")
for i, (x, y) in enumerate([(2, -2), (-2, -2)]):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, 0))
    panel = bpy.context.active_object
    panel.name = f"Panel_Solar_{i+1}"
    panel.scale = (0.05, 3, 1.5)
    panel.rotation_euler = (0, radians(15), 0)
    
    mat_panel = bpy.data.materials.new(name=f"Solar_{i+1}")
    mat_panel.use_nodes = True
    bsdf = mat_panel.node_tree.nodes["Principled BSDF"]
    bsdf.inputs['Base Color'].default_value = (0.1, 0.15, 0.4, 1.0)  # Azul oscuro
    bsdf.inputs['Roughness'].default_value = 0.1
    panel.data.materials.append(mat_panel)

# LUCES DE NAVEGACIÓN (MAT-003 style) - Emisivas rojas/verdes
print("💡 Creando luces de navegacion...")
luces = [
    ("Luz_Roja_1", (1.5, 0, 1.5), (1.0, 0.0, 0.0)),
    ("Luz_Roja_2", (-3.5, 2, 1.0), (1.0, 0.0, 0.0)),
    ("Luz_Verde", (4, 0, 1.2), (0.0, 1.0, 0.0)),
]

for nombre, loc, color in luces:
    bpy.ops.mesh.primitive_ico_sphere_add(radius=0.15, location=loc, subdivisions=1)
    luz = bpy.context.active_object
    luz.name = nombre
    
    mat_l = bpy.data.materials.new(name=f"Emisivo_{nombre}")
    mat_l.use_nodes = True
    bsdf = mat_l.node_tree.nodes["Principled BSDF"]
    bsdf.inputs['Base Color'].default_value = (*color, 1.0)
    bsdf.inputs['Emission'].default_value = (*color, 1.0)
    bsdf.inputs['Emission Strength'].default_value = 5.0
    luz.data.materials.append(mat_l)

# ILUMINACIÓN HDRI (LUZ-002 style) - Ambiente espacial
print("💡 Configurando iluminacion espacial...")

# World con color espacio
world = bpy.context.scene.world
world.use_nodes = True
bg = world.node_tree.nodes['Background']
bg.inputs['Color'].default_value = (0.02, 0.02, 0.05, 1.0)  # Azul oscuro espacio
bg.inputs['Strength'].default_value = 0.5

# Sol (estrella lejana)
bpy.ops.object.light_add(type='SUN', location=(10, 10, 10))
sun = bpy.context.active_object
sun.name = "Sol_Lejanos"
sun.data.energy = 2
sun.data.angle = radians(0.5)

# Luces de relleno azuladas
bpy.ops.object.light_add(type='AREA', location=(-5, -5, 5))
fill = bpy.context.active_object
fill.name = "Fill_Espacial"
fill.data.energy = 50
fill.data.color = (0.7, 0.8, 1.0)

# Cámara
bpy.ops.object.camera_add(location=(8, -8, 4))
cam = bpy.context.active_object
cam.rotation_euler = (1.1, 0, 0.7)
bpy.context.scene.camera = cam

# Guardar
output = './archivo_zuly/temp_arena/MOD-005_Estacion_Espacial.blend'
print(f"\\n💾 Guardando...")
bpy.ops.wm.save_as_mainfile(filepath=output)

print("\\n" + "="*70)
print("✅ MODELO 5 COMPLETADO: Estacion Espacial Orbital")
print("="*70)
'''

script_path = zuly_path / 'temp_mod5.py'
with open(script_path, 'w', encoding='utf-8') as f:
    f.write(script)

blender_exe = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe"

print("🚀 Creando MODELO 5: Estación Espacial...")
result = subprocess.run(
    [str(blender_exe), '--background', '--python', str(script_path)],
    capture_output=True, text=True, encoding='utf-8', errors='ignore',
    cwd=str(zuly_path)
)

if result.stdout:
    print(result.stdout[-1000:] if len(result.stdout) > 1000 else result.stdout)

script_path.unlink()
print("\n✅ MOD-005 creado")
