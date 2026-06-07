#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MOD-003: Casa Contenedor - SIMPLIFICADO
"""

import subprocess
from pathlib import Path

zuly_path = Path('c:/Users/Admin/Desktop/ZULY_IA_LOCAL')
backup = zuly_path / 'archivo_zuly/BACKUP_SEGURO/BACKUP_20260404_211121'

CUB004 = str(backup / 'CUB-004-HIBRIDO_Prueba/blend/CUB-004-HIBRIDO_Prueba.blend').replace('\\', '/')
P005A = str(backup / 'P-005A_ConoAlto/blend/P-005A_ConoAlto.blend').replace('\\', '/')
MAT003 = str(backup / 'MAT-003_Material_Emisivo/blend/MAT-003_Material_Emisivo.blend').replace('\\', '/')
LUZ002 = str(backup / 'LUZ-002_Iluminacion_HDRI/blend/LUZ-002_Iluminacion_HDRI.blend').replace('\\', '/')

print("="*70)
print("MOD-003: Casa Contenedor (SIMPLIFICADO)")
print("="*70)

script = '''
import bpy

print("\\n" + "="*70)
print("CONSTRUYENDO CASA CONTENEDOR")
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

# BASE
print("Creando base...")
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0.1))
base = bpy.context.active_object
base.name = "Base"
base.scale = (4, 3, 0.2)
bpy.ops.object.transform_apply(scale=True)
print("  [OK] Base")

# CONTENEDORES
print("Creando contenedores...")
importar("''' + CUB004 + '''", "Cube", "Contenedor_1", (-1.5, 0, 1.3), (1.2, 2.5, 1.3))
importar("''' + CUB004 + '''", "Cube", "Contenedor_2", (1.5, 0, 1.3), (1.2, 2.5, 1.3))

# TECHO CONICO
print("Creando techo...")
importar("''' + P005A + '''", "Cone", "Techo_Conico", (0, 0, 3.5), (2.5, 2.5, 1))

# LUCES EMISIVAS
print("Creando luces...")
with bpy.data.libraries.load("''' + MAT003 + '''") as (data_from, data_to):
    data_to.materials = data_from.materials
if data_to.materials:
    emisivo = data_to.materials[0]
    for i, x in enumerate([-1.5, 0, 1.5]):
        bpy.ops.mesh.primitive_cube_add(size=0.2, location=(x, 2.6, 2.5))
        luz = bpy.context.active_object
        luz.name = "Luz_" + str(i+1)
        luz.data.materials.append(emisivo)
    print("  [OK] Luces emisivas")

# LUZ HDRI
print("Configurando iluminacion...")
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
bpy.ops.object.camera_add(location=(10, -7, 5))
cam = bpy.context.active_object
cam.name = "Camara_Casa"
cam.rotation_euler = (1.0, 0, 0.6)
bpy.context.scene.camera = cam

# Guardar
output = "./archivo_zuly/temp_arena/MOD-003_Casa_Contenedor.blend"
bpy.ops.wm.save_as_mainfile(filepath=output)
print("\\n[OK] Guardado: " + output)
'''

script_path = zuly_path / 'temp_mod3_simple.py'
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
print("\n[OK] MOD-003 creado")
