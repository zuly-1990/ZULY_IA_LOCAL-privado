#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MOD-002: Torre Corporativa - SIMPLIFICADO
"""

import subprocess
from pathlib import Path

zuly_path = Path('c:/Users/Admin/Desktop/ZULY_IA_LOCAL')
backup = zuly_path / 'archivo_zuly/BACKUP_SEGURO/BACKUP_20260404_211121'

P001B = str(backup / 'P-001B_CuboBasico_2m/blend/P-001B_CuboBasico_2m.blend').replace('\\', '/')
MAT001 = str(backup / 'MAT-001_Material_Metal/blend/MAT-001_Material_Metal.blend').replace('\\', '/')
LUZ001 = str(backup / 'LUZ-001_Iluminacion_3Point/blend/LUZ-001_Iluminacion_3Point.blend').replace('\\', '/')

print("="*70)
print("MOD-002: Torre Corporativa (SIMPLIFICADO)")
print("="*70)

script = '''
import bpy

print("\\n" + "="*70)
print("CONSTRUYENDO TORRE")
print("="*70)

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Funcion importar
def importar(blend_path, obj_name, new_name, loc, scl):
    print("  Importando " + obj_name + "...")
    try:
        bpy.ops.wm.append(directory=blend_path + "/Object/", filename=obj_name)
        if bpy.context.selected_objects:
            obj = bpy.context.selected_objects[0]
            obj.name = new_name
            obj.location = loc
            obj.scale = scl
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.transform_apply(scale=True)
            print("    [OK] " + new_name)
            return obj
    except Exception as e:
        print("    [ERROR] " + str(e))
    return None

# NUCLEO - 3 cubos
print("Creando nucleo...")
importar("''' + P001B + '''", "Cube", "Nucleo_1", (0, 0, 1), (0.8, 0.8, 1))
importar("''' + P001B + '''", "Cube", "Nucleo_2", (0, 0, 3), (0.8, 0.8, 1))
importar("''' + P001B + '''", "Cube", "Nucleo_3", (0, 0, 5), (0.8, 0.8, 1))

# NIVELES CON VENTANAS (boolean)
print("Creando niveles...")
for nivel, z in [(1, 1.5), (2, 3.5), (3, 5.5)]:
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, z))
    piso = bpy.context.active_object
    piso.name = "Nivel_" + str(nivel)
    piso.scale = (2.5, 2.5, 0.1)
    bpy.ops.object.transform_apply(scale=True)
    # Ventanas boolean
    for x in [-1, 1]:
        bpy.ops.mesh.primitive_cube_add(size=1, location=(x, 2.6, z))
        ventana = bpy.context.active_object
        ventana.name = "Ventana_" + str(nivel) + "_" + ("L" if x < 0 else "R")
        ventana.scale = (0.3, 0.1, 0.5)
        bpy.ops.object.transform_apply(scale=True)
        bool_mod = piso.modifiers.new(name="Boolean_" + str(nivel), type='BOOLEAN')
        bool_mod.object = ventana
        bool_mod.operation = 'DIFFERENCE'
        ventana.hide_set(True)
        ventana.hide_render = True
    print("  [OK] Nivel " + str(nivel))

# MATERIAL METAL
print("Aplicando material metalico...")
with bpy.data.libraries.load("''' + MAT001 + '''") as (data_from, data_to):
    data_to.materials = data_from.materials
if data_to.materials:
    metal = data_to.materials[0]
    for obj in bpy.data.objects:
        if obj.type == 'MESH' and len(obj.data.materials) == 0:
            obj.data.materials.append(metal)
    print("  [OK] Material aplicado")

# LUZ
print("Configurando iluminacion...")
try:
    bpy.ops.wm.append(directory="''' + LUZ001 + '''" + "/Object/", filename="Light")
    print("  [OK] Luz importada")
except:
    bpy.ops.object.light_add(type='SUN', location=(5, 5, 10))
    print("  [OK] Luz basica")

# SSR
bpy.context.scene.render.engine = 'BLENDER_EEVEE'
bpy.context.scene.eevee.use_ssr = True
bpy.context.scene.eevee.ssr_thickness = 0.1

# CAMARA
bpy.ops.object.camera_add(location=(12, -8, 8))
cam = bpy.context.active_object
cam.name = "Camara_Torre"
cam.rotation_euler = (1.0, 0, 0.6)
bpy.context.scene.camera = cam

# Guardar
output = "./archivo_zuly/temp_arena/MOD-002_Torre_Corporativa.blend"
bpy.ops.wm.save_as_mainfile(filepath=output)
print("\\n[OK] Guardado: " + output)
'''

script_path = zuly_path / 'temp_mod2_simple.py'
with open(script_path, 'w', encoding='utf-8') as f:
    f.write(script)

blender_exe = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe"
result = subprocess.run(
    [str(blender_exe), '--background', '--python', str(script_path)],
    capture_output=True, text=True, encoding='utf-8', errors='ignore',
    cwd=str(zuly_path)
)

print(result.stdout[-1500:] if len(result.stdout) > 1500 else result.stdout)
script_path.unlink()
print("\n[OK] MOD-002 creado")
