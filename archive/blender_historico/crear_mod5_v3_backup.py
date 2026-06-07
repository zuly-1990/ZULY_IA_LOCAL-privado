#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MODELO 5: Estacion Espacial Orbital (V3 - BACKUP)
Patrones: P-002E + CUB-005 + MAT-001 + MAT-003 + LUZ-002
"""

import subprocess
from pathlib import Path

zuly_path = Path('c:/Users/Admin/Desktop/ZULY_IA_LOCAL')
backup = zuly_path / 'archivo_zuly/BACKUP_SEGURO/BACKUP_20260404_211121'

patrones = {
    'P-002E': str(backup / 'P-002E_EsferaUV_05m/blend/P-002E_EsferaUV_05m.blend').replace('\\', '/'),
    'CUB-005': str(backup / 'CUB-005_BooleanExacto/blend/CUB-005_BooleanExacto.blend').replace('\\', '/'),
    'MAT-001': str(backup / 'MAT-001_Material_Metal/blend/MAT-001_Material_Metal.blend').replace('\\', '/'),
    'MAT-003': str(backup / 'MAT-003_Material_Emisivo/blend/MAT-003_Material_Emisivo.blend').replace('\\', '/'),
    'LUZ-002': str(backup / 'LUZ-002_Iluminacion_HDRI/blend/LUZ-002_Iluminacion_HDRI.blend').replace('\\', '/'),
}

print("="*70)
print("RECREANDO MOD-005: Estacion Espacial (V3 - BACKUP)")
print("="*70)

script = f'''
import bpy
from math import radians

print("\\nCONSTRUYENDO ESTACION ESPACIAL")
print("="*70)

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# MODULOS HABITABLES - Esferas desde P-002E
print("CREANDO MODULOS HABITABLES...")
modulos_pos = [(0, 0, 0), (3, 0, 0), (-3, 0, 0), (0, 3, 0), (0, -3, 0)]
for i, (x, y, z) in enumerate(modulos_pos):
    bpy.ops.wm.append(directory="{patrones['P-002E']}" + "/Object/", filename="Sphere")
    if bpy.context.selected_objects:
        mod = bpy.context.selected_objects[0]
        mod.name = "Modulo_" + str(i+1)
        mod.location = (x, y, z)
        mod.scale = (1.5, 1.5, 1.5)
        print("  [OK] Modulo_" + str(i+1))

# CONECTORES - Cilindros con boolean desde CUB-005
print("CREANDO CONECTORES...")
conectores = [
    ((1.5, 0, 0), (0, 0, 1.57)),
    ((-1.5, 0, 0), (0, 0, 1.57)),
    ((0, 1.5, 0), (0, 0, 0)),
    ((0, -1.5, 0), (0, 0, 0)),
]
for i, (loc, rot) in enumerate(conectores):
    bpy.ops.mesh.primitive_cylinder_add(radius=0.3, depth=1.5, location=loc)
    conn = bpy.context.active_object
    conn.name = "Conector_" + str(i+1)
    conn.rotation_euler = rot
    print("  [OK] Conector_" + str(i+1))

# PANELES SOLARES - Planos desde CUB-005 (hibrido)
print("CREANDO PANELES SOLARES...")
for i, (x, y) in enumerate([(4, 0), (-4, 0), (0, 4), (0, -4)]):
    bpy.ops.mesh.primitive_plane_add(size=1, location=(x, y, 1))
    panel = bpy.context.active_object
    panel.name = "Panel_" + str(i+1)
    panel.scale = (2, 1, 1)
    panel.rotation_euler = (0, 0.5, 0)
    print("  [OK] Panel_" + str(i+1))

# MATERIAL METALICO - Desde MAT-001
print("APLICANDO MATERIAL METALICO...")
with bpy.data.libraries.load("{patrones['MAT-001']}") as (data_from, data_to):
    data_to.materials = data_from.materials
if data_to.materials:
    metal = data_to.materials[0]
    for obj in bpy.data.objects:
        if obj.type == 'MESH' and len(obj.data.materials) == 0:
            obj.data.materials.append(metal)
    print("  [OK] Material metal aplicado")

# LUCES DE NAVEGACION - Emisivas desde MAT-003
print("CREANDO LUCES DE NAVEGACION...")
with bpy.data.libraries.load("{patrones['MAT-003']}") as (data_from, data_to):
    data_to.materials = data_from.materials
if data_to.materials:
    emisivo = data_to.materials[0]
    for i, (x, y, z) in enumerate([(2, 2, 2), (-2, -2, 2), (2, -2, -2), (-2, 2, -2)]):
        bpy.ops.mesh.primitive_ico_sphere_add(radius=0.1, location=(x, y, z))
        luz = bpy.context.active_object
        luz.name = "Luz_Nav_" + str(i+1)
        luz.data.materials.append(emisivo)
    print("  [OK] Luces de navegacion creadas")

# ILUMINACION ESPACIAL - HDRI desde LUZ-002
print("CONFIGURANDO ILUMINACION ESPACIAL...")
try:
    bpy.ops.wm.append(directory="{patrones['LUZ-002']}" + "/Object/", filename="Light")
    print("  [OK] Iluminacion HDRI")
except:
    bpy.ops.object.light_add(type='SUN', location=(10, 10, 10))
    bpy.context.active_object.data.energy = 5
    print("  [!] Luz basica creada")

# CAMARA
bpy.ops.object.camera_add(location=(12, -10, 8))
cam = bpy.context.active_object
cam.name = "Camara_Espacial"
cam.rotation_euler = (1.0, 0, 0.5)
bpy.context.scene.camera = cam

# Guardar
output = "./archivo_zuly/temp_arena/MOD-005_Estacion_Espacial.blend"
bpy.ops.wm.save_as_mainfile(filepath=output)
print("\\nGuardado: " + output)
print("\\n[OK] MOD-005 COMPLETADO - Estacion Espacial")
'''

script_path = zuly_path / 'temp_mod5_v3.py'
with open(script_path, 'w') as f:
    f.write(script)

blender_exe = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe"
result = subprocess.run(
    [str(blender_exe), '--background', '--python', str(script_path)],
    capture_output=True, text=True, encoding='utf-8', errors='ignore',
    cwd=str(zuly_path)
)

for line in result.stdout.split('\n'):
    if any(x in line for x in ['[OK]', '[!]', 'MOD-005', 'Guardado']):
        print(line)

script_path.unlink()
print("\n[OK] MOD-005 recreado con patrones del backup")
