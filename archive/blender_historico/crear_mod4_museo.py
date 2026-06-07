#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎨 MODELO 4: Museo de Arte Abstracto
Patrones: P-002 + P-003A + CUB-001 + LUZ-001
"""

import subprocess
from pathlib import Path

zuly_path = Path('c:/Users/Admin/Desktop/ZULY_IA_LOCAL')

script = '''
import bpy
import mathutils
from math import radians

print("="*70)
print("🎨 MODELO 4: Museo de Arte Abstracto")
print("="*70)

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# SUELO MUSEO
print("📦 Creando suelo museo...")
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0.05))
suelo = bpy.context.active_object
suelo.name = "Suelo_Museo"
suelo.scale = (8, 8, 0.05)

mat_suelo = bpy.data.materials.new(name="Suelo_Blanco")
mat_suelo.use_nodes = True
bsdf = mat_suelo.node_tree.nodes["Principled BSDF"]
bsdf.inputs['Base Color'].default_value = (0.98, 0.98, 0.98, 1.0)
bsdf.inputs['Roughness'].default_value = 0.1
suelo.data.materials.append(mat_suelo)

# ESCULTURA CENTRAL (P-003A style) - Sphere alta resolucion
print("🎨 Creando escultura central...")
bpy.ops.mesh.primitive_uv_sphere_add(radius=1.2, location=(0, 0, 1.8), segments=64, ring_count=32)
esfera_central = bpy.context.active_object
esfera_central.name = "Escultura_Central"

mat_central = bpy.data.materials.new(name="Escultura_Cromada")
mat_central.use_nodes = True
bsdf = mat_central.node_tree.nodes["Principled BSDF"]
bsdf.inputs['Base Color'].default_value = (0.9, 0.1, 0.3, 1.0)  # Rojo brillante
bsdf.inputs['Metallic'].default_value = 1.0
bsdf.inputs['Roughness'].default_value = 0.1
esfera_central.data.materials.append(mat_central)

# PEDESTAL CENTRAL (CUB-001 style) - Con bevel
print("📦 Creando pedestal central...")
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0.6))
pedestal_c = bpy.context.active_object
pedestal_c.name = "Pedestal_Central"
pedestal_c.scale = (0.8, 0.8, 0.6)

bevel = pedestal_c.modifiers.new(name="Bevel", type='BEVEL')
bevel.width = 0.02
bevel.segments = 3

mat_ped = bpy.data.materials.new(name="Pedestal_Marmol")
mat_ped.use_nodes = True
bsdf = mat_ped.node_tree.nodes["Principled BSDF"]
bsdf.inputs['Base Color'].default_value = (0.95, 0.95, 0.93, 1.0)
bsdf.inputs['Roughness'].default_value = 0.2
pedestal_c.data.materials.append(mat_ped)

# ESCULTURAS LATERALES (P-002 style) - Esferas variadas
print("🎨 Creando esculturas laterales...")
esculturas = [
    ("Escultura_Oro", (-3, 0, 1.2), 0.8, (1.0, 0.8, 0.0), 'UV'),
    ("Escultura_Azul", (3, 0, 1.0), 0.6, (0.0, 0.3, 0.9), 'ICO'),
    ("Escultura_Verde", (0, 3, 1.4), 0.9, (0.0, 0.7, 0.4), 'UV'),
]

for nombre, loc, radio, color, tipo in esculturas:
    if tipo == 'UV':
        bpy.ops.mesh.primitive_uv_sphere_add(radius=radio, location=loc, segments=32, ring_count=16)
    else:
        bpy.ops.mesh.primitive_ico_sphere_add(radius=radio, location=loc, subdivisions=2)
    
    esf = bpy.context.active_object
    esf.name = nombre
    
    mat = bpy.data.materials.new(name=f"Mat_{nombre}")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs['Base Color'].default_value = (*color, 1.0)
    bsdf.inputs['Metallic'].default_value = 0.8
    bsdf.inputs['Roughness'].default_value = 0.2
    esf.data.materials.append(mat)
    
    # Pedestal para cada escultura
    bpy.ops.mesh.primitive_cube_add(size=1, location=(loc[0], loc[1], 0.5))
    ped = bpy.context.active_object
    ped.name = f"Pedestal_{nombre}"
    ped.scale = (0.5, 0.5, 0.5)
    
    bevel_p = ped.modifiers.new(name="Bevel", type='BEVEL')
    bevel_p.width = 0.01
    bevel_p.segments = 2
    ped.data.materials.append(mat_ped)

# ILUMINACION 3-POINT (LUZ-001 style) - Profesional
print("💡 Configurando iluminacion 3-Point...")

# Key light
bpy.ops.object.light_add(type='AREA', location=(-4, -4, 4))
key = bpy.context.active_object
key.name = "Key_Light"
key.data.energy = 200
key.data.size = 2

# Fill light
bpy.ops.object.light_add(type='AREA', location=(4, -2, 3))
fill = bpy.context.active_object
fill.name = "Fill_Light"
fill.data.energy = 100
fill.data.size = 3

# Rim light
bpy.ops.object.light_add(type='SPOT', location=(0, 5, 5))
rim = bpy.context.active_object
rim.name = "Rim_Light"
rim.data.energy = 150
rim.data.spot_size = radians(60)
rim.rotation_euler = (radians(45), 0, radians(180))

# Cámara
bpy.ops.object.camera_add(location=(6, -6, 3))
cam = bpy.context.active_object
cam.rotation_euler = (1.15, 0, 0.8)
bpy.context.scene.camera = cam

# Guardar
output = './archivo_zuly/temp_arena/MOD-004_Museo_Arte.blend'
print(f"\\n💾 Guardando...")
bpy.ops.wm.save_as_mainfile(filepath=output)

print("\\n" + "="*70)
print("✅ MODELO 4 COMPLETADO: Museo de Arte Abstracto")
print("="*70)
'''

script_path = zuly_path / 'temp_mod4.py'
with open(script_path, 'w', encoding='utf-8') as f:
    f.write(script)

blender_exe = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe"

print("🎨 Creando MODELO 4: Museo de Arte...")
result = subprocess.run(
    [str(blender_exe), '--background', '--python', str(script_path)],
    capture_output=True, text=True, encoding='utf-8', errors='ignore',
    cwd=str(zuly_path)
)

if result.stdout:
    print(result.stdout[-1000:] if len(result.stdout) > 1000 else result.stdout)

script_path.unlink()
print("\n✅ MOD-004 creado")
