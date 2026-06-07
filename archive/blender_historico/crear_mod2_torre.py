#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🏢 MODELO 2: Torre Corporativa (3 niveles)
Patrones: CUB-002 + CUB-005 + MAT-001 + P-001B
"""

import subprocess
from pathlib import Path

zuly_path = Path('c:/Users/Admin/Desktop/ZULY_IA_LOCAL')

script = '''
import bpy
import mathutils
from math import radians

print("="*70)
print("🏢 MODELO 2: Torre Corporativa")
print("="*70)

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# NÚCLEO CENTRAL (P-001B style) - Cubo 2m x 6m alto
print("📦 Creando nucleo central...")
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 3))
nucleo = bpy.context.active_object
nucleo.name = "Nucleo_Central"
nucleo.scale = (1, 1, 6)  # 2m x 2m x 12m

# Pivote en suelo (CUB-002 style)
nucleo.location.z = 6  # Centrado en altura

mat_nucleo = bpy.data.materials.new(name="Nucleo_Hormigon")
mat_nucleo.use_nodes = True
bsdf = mat_nucleo.node_tree.nodes["Principled BSDF"]
bsdf.inputs['Base Color'].default_value = (0.4, 0.4, 0.42, 1.0)
bsdf.inputs['Roughness'].default_value = 0.9
nucleo.data.materials.append(mat_nucleo)

# NIVELES con Boolean (CUB-005 style)
print("📦 Creando niveles con ventanas (boolean)...")
for nivel in range(3):
    z = nivel * 4
    
    # Plataforma del nivel
    bpy.ops.mesh.primitive_cube_add(size=1, location=(2.5, 0, z + 2))
    plataforma = bpy.context.active_object
    plataforma.name = f"Nivel_{nivel+1}"
    plataforma.scale = (2, 3, 0.2)
    
    # Material metal (MAT-001 style)
    mat_metal = bpy.data.materials.new(name=f"Metal_{nivel+1}")
    mat_metal.use_nodes = True
    bsdf = mat_metal.node_tree.nodes["Principled BSDF"]
    bsdf.inputs['Base Color'].default_value = (0.72, 0.73, 0.75, 1.0)
    bsdf.inputs['Metallic'].default_value = 0.9
    bsdf.inputs['Roughness'].default_value = 0.2
    plataforma.data.materials.append(mat_metal)
    
    # Ventanas (boolean simulation - cubos negros)
    for x in [1.5, 3.5]:
        bpy.ops.mesh.primitive_cube_add(size=1, location=(x, 2.5, z + 2.5))
        ventana = bpy.context.active_object
        ventana.name = f"Ventana_{nivel+1}_{x}"
        ventana.scale = (0.5, 0.1, 0.8)
        
        mat_vidrio = bpy.data.materials.new(name=f"Vidrio_{nivel+1}_{x}")
        mat_vidrio.use_nodes = True
        bsdf = mat_vidrio.node_tree.nodes["Principled BSDF"]
        bsdf.inputs['Base Color'].default_value = (0.2, 0.3, 0.5, 1.0)
        bsdf.inputs['Roughness'].default_value = 0.0
        bsdf.inputs['Transmission'].default_value = 0.8
        ventana.data.materials.append(mat_vidrio)

# Estructura exterior metálica
print("📦 Creando estructura exterior...")
for z in [0, 4, 8, 12]:
    for x in [-3, 6]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.15, depth=4, location=(x, 0, z + 2))
        columna = bpy.context.active_object
        columna.name = f"Columna_{x}_{z}"
        
        mat_col = bpy.data.materials.new(name=f"Columna_{x}_{z}")
        mat_col.use_nodes = True
        bsdf = mat_col.node_tree.nodes["Principled BSDF"]
        bsdf.inputs['Base Color'].default_value = (0.6, 0.6, 0.62, 1.0)
        bsdf.inputs['Metallic'].default_value = 0.7
        bsdf.inputs['Roughness'].default_value = 0.3
        columna.data.materials.append(mat_col)

# Iluminación
bpy.ops.object.light_add(type='AREA', location=(5, -5, 6))
key = bpy.context.active_object
key.data.energy = 200

bpy.ops.object.light_add(type='SUN', location=(10, 10, 15))
sun = bpy.context.active_object
sun.data.energy = 2

# Cámara
bpy.ops.object.camera_add(location=(12, -10, 8))
cam = bpy.context.active_object
cam.rotation_euler = (1.0, 0, 0.6)
bpy.context.scene.camera = cam

# Guardar
output = './archivo_zuly/temp_arena/MOD-002_Torre_Corporativa.blend'
print(f"\\n💾 Guardando...")
bpy.ops.wm.save_as_mainfile(filepath=output)

print("\\n" + "="*70)
print("✅ MODELO 2 COMPLETADO: Torre Corporativa (3 niveles)")
print("="*70)
'''

script_path = zuly_path / 'temp_mod2.py'
with open(script_path, 'w', encoding='utf-8') as f:
    f.write(script)

blender_exe = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe"

print("🏢 Creando MODELO 2: Torre Corporativa...")
result = subprocess.run(
    [str(blender_exe), '--background', '--python', str(script_path)],
    capture_output=True, text=True, encoding='utf-8', errors='ignore',
    cwd=str(zuly_path)
)

if result.stdout:
    print(result.stdout[-1000:] if len(result.stdout) > 1000 else result.stdout)

script_path.unlink()
print("\n✅ MOD-002 creado")
