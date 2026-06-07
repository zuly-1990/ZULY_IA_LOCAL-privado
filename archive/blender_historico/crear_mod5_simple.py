#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MOD-005: Estacion Espacial - SIMPLIFICADO
"""

import subprocess
from pathlib import Path

zuly_path = Path('c:/Users/Admin/Desktop/ZULY_IA_LOCAL')
backup = zuly_path / 'archivo_zuly/BACKUP_SEGURO/BACKUP_20260404_211121'

P002E = str(backup / 'P-002E_EsferaUV_05m/blend/P-002E_EsferaUV_05m.blend').replace('\\', '/')
MAT001 = str(backup / 'MAT-001_Material_Metal/blend/MAT-001_Material_Metal.blend').replace('\\', '/')
MAT003 = str(backup / 'MAT-003_Material_Emisivo/blend/MAT-003_Material_Emisivo.blend').replace('\\', '/')
LUZ002 = str(backup / 'LUZ-002_Iluminacion_HDRI/blend/LUZ-002_Iluminacion_HDRI.blend').replace('\\', '/')

print("="*70)
print("MOD-005: Estacion Espacial (SIMPLIFICADO)")
print("="*70)

script = '''
import bpy

print("\\n" + "="*70)
print("CONSTRUYENDO ESTACION ESPACIAL")
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

# MODULOS HABITABLES (Esferas)
print("Creando modulos...")
pos_modulos = [(0, 0, 0), (3, 0, 0), (-3, 0, 0), (0, 3, 0), (0, -3, 0)]
for i, (x, y, z) in enumerate(pos_modulos):
    importar("''' + P002E + '''", "Sphere", "Modulo_" + str(i+1), (x, y, z), (1.5, 1.5, 1.5))

# CONECTORES (Cilindros)
print("Creando conectores...")
conectores = [
    ((1.5, 0, 0), (0, 0, 1.57)), ((-1.5, 0, 0), (0, 0, 1.57)),
    ((0, 1.5, 0), (0, 0, 0)), ((0, -1.5, 0), (0, 0, 0)),
]
for i, (loc, rot) in enumerate(conectores):
    bpy.ops.mesh.primitive_cylinder_add(radius=0.3, depth=1.5, location=loc)
    conn = bpy.context.active_object
    conn.name = "Conector_" + str(i+1)
    conn.rotation_euler = rot
    bpy.ops.object.transform_apply(scale=True, rotation=True)
print("  [OK] Conectores")

# PANELES SOLARES
print("Creando paneles solares...")
for i, (x, y) in enumerate([(4, 0), (-4, 0), (0, 4), (0, -4)]):
    bpy.ops.mesh.primitive_plane_add(size=1, location=(x, y, 1))
    panel = bpy.context.active_object
    panel.name = "Panel_" + str(i+1)
    panel.scale = (2, 1, 1)
    panel.rotation_euler = (0, 0.5, 0)
    bpy.ops.object.transform_apply(scale=True, rotation=True)
print("  [OK] Paneles")

# MATERIAL METALICO
print("Aplicando material metalico...")
with bpy.data.libraries.load("''' + MAT001 + '''") as (data_from, data_to):
    data_to.materials = data_from.materials
if data_to.materials:
    metal = data_to.materials[0]
    for obj in bpy.data.objects:
        if obj.type == 'MESH' and len(obj.data.materials) == 0:
            obj.data.materials.append(metal)
    print("  [OK] Material metal")

# LUCES DE NAVEGACION
print("Creando luces de navegacion...")
with bpy.data.libraries.load("''' + MAT003 + '''") as (data_from, data_to):
    data_to.materials = data_from.materials
if data_to.materials:
    emisivo = data_to.materials[0]
    for i, (x, y, z) in enumerate([(2, 2, 2), (-2, -2, 2), (2, -2, -2), (-2, 2, -2)]):
        bpy.ops.mesh.primitive_ico_sphere_add(radius=0.1, location=(x, y, z))
        luz = bpy.context.active_object
        luz.name = "Luz_Nav_" + str(i+1)
        luz.data.materials.append(emisivo)
    print("  [OK] Luces de navegacion")

# LUZ HDRI
print("Configurando iluminacion espacial...")
try:
    bpy.ops.wm.append(directory="''' + LUZ002 + '''" + "/Object/", filename="Light")
    print("  [OK] HDRI importado")
except:
    bpy.ops.object.light_add(type='SUN', location=(10, 10, 10))
    bpy.context.active_object.data.energy = 5
    print("  [OK] Luz basica")

# SSR
bpy.context.scene.render.engine = 'BLENDER_EEVEE'
bpy.context.scene.eevee.use_ssr = True
bpy.context.scene.eevee.ssr_thickness = 0.1

# CAMARA
bpy.ops.object.camera_add(location=(12, -10, 8))
cam = bpy.context.active_object
cam.name = "Camara_Espacial"
cam.rotation_euler = (1.0, 0, 0.5)
bpy.context.scene.camera = cam

# Guardar
output = "./archivo_zuly/temp_arena/MOD-005_Estacion_Espacial.blend"
bpy.ops.wm.save_as_mainfile(filepath=output)
print("\\n[OK] Guardado: " + output)
'''

script_path = zuly_path / 'temp_mod5_simple.py'
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
print("\n[OK] MOD-005 creado")
