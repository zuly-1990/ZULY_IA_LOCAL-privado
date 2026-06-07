#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🏠 MODELO 3: Casa Contenedor Industrial
Patrones: CUB-004 + P-005A + MAT-003 + P-006A
"""

import subprocess
from pathlib import Path

zuly_path = Path('c:/Users/Admin/Desktop/ZULY_IA_LOCAL')

script = '''
import bpy
import mathutils
from math import radians

print("="*70)
print("🏠 MODELO 3: Casa Contenedor Industrial")
print("="*70)

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# BASE/SUELO (P-006A style) - Plano con grosor
print("📦 Creando base de hormigon...")
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0.1))
base = bpy.context.active_object
base.name = "Base_Hormigon"
base.scale = (6, 4, 0.1)

mat_base = bpy.data.materials.new(name="Hormigon_Base")
mat_base.use_nodes = True
bsdf = mat_base.node_tree.nodes["Principled BSDF"]
bsdf.inputs['Base Color'].default_value = (0.5, 0.5, 0.52, 1.0)
bsdf.inputs['Roughness'].default_value = 1.0
base.data.materials.append(mat_base)

# CONTENEDORES (CUB-004 style) - Hibrido combinacion
print("📦 Creando contenedores...")
for i, x in enumerate([-2, 2]):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x, 0, 1.4))
    cont = bpy.context.active_object
    cont.name = f"Contenedor_{i+1}"
    cont.scale = (1.8, 3, 1.3)  # 3.6m x 6m x 2.6m (standard contenedor)
    
    # Material metal oxidado
    mat = bpy.data.materials.new(name=f"Metal_Cont_{i+1}")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    color = (0.45, 0.25, 0.15, 1.0) if i == 0 else (0.35, 0.45, 0.25, 1.0)  # Oxido / Verde
    bsdf.inputs['Base Color'].default_value = color
    bsdf.inputs['Metallic'].default_value = 0.6
    bsdf.inputs['Roughness'].default_value = 0.7
    cont.data.materials.append(mat)
    
    # Ventanas contenedor
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x + 0.9, 0, 1.8))
    vent = bpy.context.active_object
    vent.name = f"Ventana_Cont_{i+1}"
    vent.scale = (0.05, 0.8, 0.6)
    
    mat_v = bpy.data.materials.new(name=f"Vidrio_Cont_{i+1}")
    mat_v.use_nodes = True
    bsdf = mat_v.node_tree.nodes["Principled BSDF"]
    bsdf.inputs['Base Color'].default_value = (0.1, 0.15, 0.2, 1.0)
    bsdf.inputs['Transmission'].default_value = 0.7
    vent.data.materials.append(mat_v)

# TECHO CONICO (P-005A style) - Cono como techo inclinado
print("📦 Creando techo conico...")
bpy.ops.mesh.primitive_cone_add(radius1=2.5, radius2=0.2, depth=1.5, location=(0, 0, 3.5))
techo = bpy.context.active_object
techo.name = "Techo_Cono"
techo.rotation_euler = (0, radians(15), 0)  # Inclinado

mat_techo = bpy.data.materials.new(name="Techo_Lamina")
mat_techo.use_nodes = True
bsdf = mat_techo.node_tree.nodes["Principled BSDF"]
bsdf.inputs['Base Color'].default_value = (0.7, 0.3, 0.2, 1.0)  # Teja rojiza
bsdf.inputs['Roughness'].default_value = 0.6
techo.data.materials.append(mat_techo)

# LUCES EMISIVAS (MAT-003 style) - Luces interior/exterior
print("💡 Creando luces emisivas...")
for x in [-2, 2]:
    bpy.ops.mesh.primitive_plane_add(size=1, location=(x + 0.9, 1, 1.4))
    luz = bpy.context.active_object
    luz.name = f"Luz_Emisiva_{x}"
    luz.scale = (0.1, 0.3, 1)
    
    mat_em = bpy.data.materials.new(name=f"Emisivo_{x}")
    mat_em.use_nodes = True
    bsdf = mat_em.node_tree.nodes["Principled BSDF"]
    bsdf.inputs['Base Color'].default_value = (1.0, 0.4, 0.1, 1.0)  # Naranja calido
    bsdf.inputs['Emission'].default_value = (1.0, 0.5, 0.2, 1.0)
    bsdf.inputs['Emission Strength'].default_value = 2.0
    luz.data.materials.append(mat_em)

# Iluminación ambiental
bpy.ops.object.light_add(type='AREA', location=(0, -5, 4))
key = bpy.context.active_object
key.data.energy = 100
key.data.size = 5

bpy.ops.object.light_add(type='POINT', location=(0, 0, 2))
interior = bpy.context.active_object
interior.data.energy = 50
interior.data.color = (1.0, 0.9, 0.8)

# Cámara
bpy.ops.object.camera_add(location=(8, -8, 3))
cam = bpy.context.active_object
cam.rotation_euler = (1.1, 0, 0.7)
bpy.context.scene.camera = cam

# Guardar
output = './archivo_zuly/temp_arena/MOD-003_Casa_Contenedor.blend'
print(f"\\n💾 Guardando...")
bpy.ops.wm.save_as_mainfile(filepath=output)

print("\\n" + "="*70)
print("✅ MODELO 3 COMPLETADO: Casa Contenedor Industrial")
print("="*70)
'''

script_path = zuly_path / 'temp_mod3.py'
with open(script_path, 'w', encoding='utf-8') as f:
    f.write(script)

blender_exe = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe"

print("🏠 Creando MODELO 3: Casa Contenedor...")
result = subprocess.run(
    [str(blender_exe), '--background', '--python', str(script_path)],
    capture_output=True, text=True, encoding='utf-8', errors='ignore',
    cwd=str(zuly_path)
)

if result.stdout:
    print(result.stdout[-1000:] if len(result.stdout) > 1000 else result.stdout)

script_path.unlink()
print("\n✅ MOD-003 creado")
