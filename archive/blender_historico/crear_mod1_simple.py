#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MOD-001: Pabellon Minimalista - SIMPLIFICADO
"""

import subprocess
from pathlib import Path

zuly_path = Path('c:/Users/Admin/Desktop/ZULY_IA_LOCAL')
backup = zuly_path / 'archivo_zuly/BACKUP_SEGURO/BACKUP_20260404_211121'

# Patrones
CUB003 = str(backup / 'CUB-003_Modelado_MuroPro/blend/CUB-003_Modelado_MuroPro.blend').replace('\\', '/')
MAT002 = str(backup / 'MAT-002_Material_Vidrio/blend/MAT-002_Material_Vidrio.blend').replace('\\', '/')
P004A = str(backup / 'P-004A_CilindroAlto/blend/P-004A_CilindroAlto.blend').replace('\\', '/')
LUZ001 = str(backup / 'LUZ-001_Iluminacion_3Point/blend/LUZ-001_Iluminacion_3Point.blend').replace('\\', '/')

print("="*70)
print("MOD-001: Pabellon Minimalista (SIMPLIFICADO)")
print("="*70)

# Script Blender usando concatenacion simple (sin f-strings anidados)
script = '''
import bpy
from math import radians

print("\\n" + "="*70)
print("CONSTRUYENDO PABELLON")
print("="*70)

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Funcion importar con aplicacion de escala
def importar_objeto(blend_path, obj_name, new_name, loc, scl):
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

# MUROS
print("Creando muros...")
importar_objeto("''' + CUB003 + '''", "Cube", "Muro_1", (-2.5, 0, 1.35), (0.075, 3, 1.35))
importar_objeto("''' + CUB003 + '''", "Cube", "Muro_2", (0, 0, 1.35), (0.075, 3, 1.35))
importar_objeto("''' + CUB003 + '''", "Cube", "Muro_3", (2.5, 0, 1.35), (0.075, 3, 1.35))

# COLUMNA
print("Creando columna...")
importar_objeto("''' + P004A + '''", "Cylinder", "Columna_Central", (0, 0, 1.5), (0.3, 0.3, 3))

# FACHADA VIDRIO - Cubo delgado (no plano) para evitar non-manifold
print("Creando fachada...")
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 3, 1.35))
bpy.ops.transform.rotate(value=radians(90), orient_axis='X')
vidrio = bpy.context.active_object
vidrio.name = "Fachada_Vidrio"
vidrio.scale = (3, 1.35, 0.02)  # Espesor 0.02m
bpy.ops.object.transform_apply(scale=True)

# Material de vidrio
with bpy.data.libraries.load("''' + MAT002 + '''") as (data_from, data_to):
    data_to.materials = data_from.materials
if data_to.materials:
    vidrio.data.materials.append(data_to.materials[0])
    print("  [OK] Material vidrio")

# TECHO
print("Creando techo...")
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 2.85))
techo = bpy.context.active_object
techo.name = "Techo"
techo.scale = (3.5, 3.5, 0.05)
bpy.context.view_layer.objects.active = techo
bpy.ops.object.transform_apply(scale=True)
bevel = techo.modifiers.new(name="Bevel", type='BEVEL')
bevel.width = 0.02
bevel.segments = 2
print("  [OK] Techo")

# LUZ Y RENDER
print("Configurando iluminacion...")
try:
    bpy.ops.wm.append(directory="''' + LUZ001 + '''" + "/Object/", filename="Light")
    print("  [OK] Luz importada")
except:
    bpy.ops.object.light_add(type='SUN', location=(5, 5, 10))
    print("  [OK] Luz basica")

# Configurar SSR
bpy.context.scene.render.engine = 'BLENDER_EEVEE'
bpy.context.scene.eevee.use_ssr = True
bpy.context.scene.eevee.ssr_thickness = 0.1
print("  [OK] SSR activado")

# CAMARA
bpy.ops.object.camera_add(location=(8, -6, 3))
cam = bpy.context.active_object
cam.name = "Camara_Pabellon"
cam.rotation_euler = (1.1, 0, 0.8)
bpy.context.scene.camera = cam

# Guardar
output = "./archivo_zuly/temp_arena/MOD-001_Pabellon_Minimalista.blend"
bpy.ops.wm.save_as_mainfile(filepath=output)
print("\\n[OK] Guardado: " + output)
print("[OK] MOD-001 COMPLETADO")
'''

script_path = zuly_path / 'temp_mod1_simple.py'
with open(script_path, 'w', encoding='utf-8') as f:
    f.write(script)

blender_exe = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe"
result = subprocess.run(
    [str(blender_exe), '--background', '--python', str(script_path)],
    capture_output=True, text=True, encoding='utf-8', errors='ignore',
    cwd=str(zuly_path)
)

print(result.stdout[-1500:] if len(result.stdout) > 1500 else result.stdout)
if result.stderr:
    print("ERR:", result.stderr[-300:])

script_path.unlink()
print("\n[OK] MOD-001 creado")
