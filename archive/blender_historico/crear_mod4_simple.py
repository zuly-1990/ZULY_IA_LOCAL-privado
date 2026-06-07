#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MOD-004: Museo de Arte - SIMPLIFICADO
"""

import subprocess
from pathlib import Path

zuly_path = Path('c:/Users/Admin/Desktop/ZULY_IA_LOCAL')
backup = zuly_path / 'archivo_zuly/BACKUP_SEGURO/BACKUP_20260404_211121'

P002A = str(backup / 'P-002A_EsferaUV_1m/blend/P-002A_EsferaUV_1m.blend').replace('\\', '/')
P003A = str(backup / 'P-003A_SphereAltaRes/blend/P-003A_SphereAltaRes.blend').replace('\\', '/')
CUB001 = str(backup / 'CUB-001_Modelado_BiselRealista/blend/CUB-001_Modelado_BiselRealista.blend').replace('\\', '/')
LUZ001 = str(backup / 'LUZ-001_Iluminacion_3Point/blend/LUZ-001_Iluminacion_3Point.blend').replace('\\', '/')

print("="*70)
print("MOD-004: Museo de Arte (SIMPLIFICADO)")
print("="*70)

script = '''
import bpy

print("\\n" + "="*70)
print("CONSTRUYENDO MUSEO")
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

# SUELO
print("Creando suelo...")
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, 0))
suelo = bpy.context.active_object
suelo.name = "Suelo"
suelo.scale = (8, 8, 1)
bpy.ops.object.transform_apply(scale=True)
print("  [OK] Suelo")

# ESCULTURA CENTRAL (Alta res)
print("Creando escultura central...")
importar("''' + P003A + '''", "Sphere", "Escultura_Central", (0, 0, 2), (1.5, 1.5, 1.5))

# PEDESTAL CENTRAL
print("Creando pedestal central...")
importar("''' + CUB001 + '''", "Cube", "Pedestal_Central", (0, 0, 0.5), (1, 1, 0.5))

# ESCULTURAS LATERALES
print("Creando esculturas laterales...")
posiciones = [(-4, 3), (4, 3), (-4, -3), (4, -3)]
for i, (x, y) in enumerate(posiciones):
    importar("''' + P002A + '''", "Sphere", "Escultura_" + str(i+1), (x, y, 1.5), (0.8, 0.8, 0.8))
    # Pedestal
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x, y, 0.25))
    ped = bpy.context.active_object
    ped.name = "Pedestal_" + str(i+1)
    ped.scale = (0.6, 0.6, 0.25)
    bpy.ops.object.transform_apply(scale=True)
print("  [OK] Esculturas y pedestales")

# LUZ 3-POINT
print("Configurando iluminacion...")
try:
    bpy.ops.wm.append(directory="''' + LUZ001 + '''" + "/Object/", filename="Light")
    print("  [OK] Luz 3-Point")
except:
    bpy.ops.object.light_add(type='AREA', location=(0, -5, 4))
    bpy.context.active_object.data.energy = 200
    print("  [OK] Luz basica")

# SSR
bpy.context.scene.render.engine = 'BLENDER_EEVEE'
bpy.context.scene.eevee.use_ssr = True
bpy.context.scene.eevee.ssr_thickness = 0.1

# CAMARA
bpy.ops.object.camera_add(location=(10, -8, 4))
cam = bpy.context.active_object
cam.name = "Camara_Museo"
cam.rotation_euler = (1.1, 0, 0.7)
bpy.context.scene.camera = cam

# Guardar
output = "./archivo_zuly/temp_arena/MOD-004_Museo_Arte.blend"
bpy.ops.wm.save_as_mainfile(filepath=output)
print("\\n[OK] Guardado: " + output)
'''

script_path = zuly_path / 'temp_mod4_simple.py'
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
print("\n[OK] MOD-004 creado")
