#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MUSEO DE ARTE - V3 BACKUP
Patrones: P-002 + P-003A + CUB-001 + LUZ-001
"""

import subprocess
from pathlib import Path

zuly_path = Path('c:/Users/Admin/Desktop/ZULY_IA_LOCAL')
backup = zuly_path / 'archivo_zuly/BACKUP_SEGURO/BACKUP_20260404_211121'

patrones = {
    'P-002A': str(backup / 'P-002A_EsferaUV_1m/blend/P-002A_EsferaUV_1m.blend').replace('\\', '/'),
    'P-003A': str(backup / 'P-003A_SphereAltaRes/blend/P-003A_SphereAltaRes.blend').replace('\\', '/'),
    'CUB-001': str(backup / 'CUB-001_Modelado_BiselRealista/blend/CUB-001_Modelado_BiselRealista.blend').replace('\\', '/'),
    'LUZ-001': str(backup / 'LUZ-001_Iluminacion_3Point/blend/LUZ-001_Iluminacion_3Point.blend').replace('\\', '/'),
}

print("="*70)
print("RECREANDO MOD-004: Museo de Arte (V3 - BACKUP)")
print("="*70)

script = f'''
import bpy
from math import radians

print("\\nCONSTRUYENDO MUSEO DE ARTE")
print("="*70)

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# SUELO MUSEO
print("Creando suelo...")
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, 0))
suelo = bpy.context.active_object
suelo.name = "Suelo_Museo"
suelo.scale = (8, 8, 1)

# ESCULTURA CENTRAL - P-003A (Sphere Alta Res)
print("Creando escultura central (P-003A)...")
bpy.ops.wm.append(directory="{patrones['P-003A']}" + "/Object/", filename="Sphere")
if bpy.context.selected_objects:
    esc = bpy.context.selected_objects[0]
    esc.name = "Escultura_Central"
    esc.location = (0, 0, 2)
    esc.scale = (1.5, 1.5, 1.5)
    print("  [OK] Escultura central")

# PEDESTAL CENTRAL - CUB-001 con bevel
print("Creando pedestal central...")
bpy.ops.wm.append(directory="{patrones['CUB-001']}" + "/Object/", filename="Cube")
if bpy.context.selected_objects:
    ped = bpy.context.selected_objects[0]
    ped.name = "Pedestal_Central"
    ped.location = (0, 0, 0.5)
    ped.scale = (1, 1, 0.5)
    print("  [OK] Pedestal central")

# ESCULTURAS LATERALES - P-002A (Esferas UV)
print("Creando esculturas laterales (P-002A)...")
for i, (x, y) in enumerate([(-4, 3), (4, 3), (-4, -3), (4, -3)]):
    bpy.ops.wm.append(directory="{patrones['P-002A']}" + "/Object/", filename="Sphere")
    if bpy.context.selected_objects:
        esc = bpy.context.selected_objects[0]
        esc.name = "Escultura_" + str(i+1)
        esc.location = (x, y, 1.5)
        esc.scale = (0.8, 0.8, 0.8)
        print("  [OK] Escultura_" + str(i+1))

# PEDESTALES LATERALES
print("Creando pedestales laterales...")
for i, (x, y) in enumerate([(-4, 3), (4, 3), (-4, -3), (4, -3)]):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, 0.25))
    ped = bpy.context.active_object
    ped.name = "Pedestal_" + str(i+1)
    ped.scale = (0.6, 0.6, 0.25)

# ILUMINACIÓN 3-POINT
print("Configurando iluminación 3-Point...")
try:
    bpy.ops.wm.append(directory="{patrones['LUZ-001']}" + "/Object/", filename="Light")
    print("  [OK] Iluminacion 3-Point")
except:
    # Key light
    bpy.ops.object.light_add(type='AREA', location=(0, -5, 4))
    bpy.context.active_object.data.energy = 200
    # Fill light
    bpy.ops.object.light_add(type='AREA', location=(5, 0, 3))
    bpy.context.active_object.data.energy = 100
    # Back light
    bpy.ops.object.light_add(type='SUN', location=(-3, 3, 5))
    print("  [!] Luces basicas creadas")

# CÁMARA
bpy.ops.object.camera_add(location=(10, -8, 4))
cam = bpy.context.active_object
cam.name = "Camara_Museo"
cam.rotation_euler = (1.1, 0, 0.7)
bpy.context.scene.camera = cam

# Guardar
output = "./archivo_zuly/temp_arena/MOD-004_Museo_Arte.blend"
bpy.ops.wm.save_as_mainfile(filepath=output)
print(f"\\nGuardado: {{output}}")
print("\\n[OK] MOD-004 COMPLETADO - Museo de Arte")
'''

script_path = zuly_path / 'temp_mod4_v3.py'
with open(script_path, 'w') as f:
    f.write(script)

blender_exe = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe"
result = subprocess.run(
    [str(blender_exe), '--background', '--python', str(script_path)],
    capture_output=True, text=True, encoding='utf-8', errors='ignore',
    cwd=str(zuly_path)
)

for line in result.stdout.split('\n'):
    if any(x in line for x in ['[OK]', '[!]', 'MOD-004', 'Guardado']):
        print(line)

script_path.unlink()
print("\n[OK] MOD-004 recreado con patrones del backup")
