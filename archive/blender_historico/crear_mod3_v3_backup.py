#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🏠 MODELO 3: Casa Contenedor Industrial (V3 - BACKUP)
Patrones: CUB-004 + P-005A + MAT-003 + P-006A
"""

import subprocess
from pathlib import Path

zuly_path = Path('c:/Users/Admin/Desktop/ZULY_IA_LOCAL')
backup = zuly_path / 'archivo_zuly/BACKUP_SEGURO/BACKUP_20260404_211121'

patrones = {
    'CUB-004': str(backup / 'CUB-004-HIBRIDO_Prueba/blend/CUB-004-HIBRIDO_Prueba.blend').replace('\\', '/'),
    'P-005A': str(backup / 'P-005A_ConoAlto/blend/P-005A_ConoAlto.blend').replace('\\', '/'),
    'MAT-003': str(backup / 'MAT-003_Material_Emisivo/blend/MAT-003_Material_Emisivo.blend').replace('\\', '/'),
    'P-006A': str(backup / 'P-006A_PlanoBase/blend/P-006A_PlanoBase.blend').replace('\\', '/'),
    'LUZ-002': str(backup / 'LUZ-002_Iluminacion_HDRI/blend/LUZ-002_Iluminacion_HDRI.blend').replace('\\', '/'),
}

print("="*70)
print("🏠 RECREANDO MOD-003: Casa Contenedor (V3 - BACKUP)")
print("="*70)

script = f'''
import bpy
from math import radians

print("\\n🏠 CONSTRUYENDO CASA CONTENEDOR")
print("="*70)

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# BASE DE HORMIGÓN - Desde P-006A (PlanoBase)
print("📦 Creando base de hormigón...")
bpy.ops.wm.append(directory="{patrones['P-006A']}" + "/Object/", filename="Plane")
if bpy.context.selected_objects:
    base = bpy.context.selected_objects[0]
    base.name = "Base_Hormigon"
    base.location = (0, 0, 0.05)
    base.scale = (4, 3, 1)
    # Darle volumen
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={{"value":(0, 0, 0.1)}})
    bpy.ops.object.mode_set(mode='OBJECT')
    print("  ✅ Base creada")

# CONTENEDORES - 2 cubos desde CUB-004 (Híbrido)
print("📦 Creando contenedores...")
for i, x in enumerate([-1.5, 1.5]):
    bpy.ops.wm.append(directory="{patrones['CUB-004']}" + "/Object/", filename="Cube")
    if bpy.context.selected_objects:
        cont = bpy.context.selected_objects[0]
        cont.name = f"Contenedor_{{i+1}}"
        cont.location = (x, 0, 1.3)
        cont.scale = (1.2, 2.5, 1.3)
        print(f"  ✅ Contenedor_{{i+1}}")

# TECHO CÓNICO - Desde P-005A
print("📦 Creando techo cónico...")
bpy.ops.wm.append(directory="{patrones['P-005A']}" + "/Object/", filename="Cone")
if bpy.context.selected_objects:
    techo = bpy.context.selected_objects[0]
    techo.name = "Techo_Conico"
    techo.location = (0, 0, 3.5)
    techo.scale = (2.5, 2.5, 1)
    print("  ✅ Techo cónico")

# LUCES EMISIVAS - Desde MAT-003
print("💡 Creando luces emisivas...")
with bpy.data.libraries.load("{patrones['MAT-003']}") as (data_from, data_to):
    data_to.materials = data_from.materials

if data_to.materials:
    emisivo = data_to.materials[0]
    # Crear luces decorativas
    for i, x in enumerate([-1.5, 0, 1.5]):
        bpy.ops.mesh.primitive_cube_add(size=0.2, location=(x, 2.6, 2.5))
        luz = bpy.context.active_object
        luz.name = f"Luz_Emisiva_{{i+1}}"
        luz.data.materials.append(emisivo)
    print("  ✅ Luces emisivas creadas")

# ILUMINACIÓN HDRI
print("💡 Configurando iluminación HDRI...")
try:
    bpy.ops.wm.append(directory="{patrones['LUZ-002']}" + "/Object/", filename="Light")
    print("  ✅ HDRI importado")
except:
    bpy.ops.object.light_add(type='SUN', location=(5, 5, 10))
    bpy.context.active_object.data.energy = 5
    print("  ⚠️ Luz básica creada")

# CÁMARA
bpy.ops.object.camera_add(location=(10, -7, 5))
cam = bpy.context.active_object
cam.name = "Camara_Casa"
cam.rotation_euler = (1.0, 0, 0.6)
bpy.context.scene.camera = cam

# Guardar
output = "./archivo_zuly/temp_arena/MOD-003_Casa_Contenedor.blend"
bpy.ops.wm.save_as_mainfile(filepath=output)
print(f"\\n💾 Guardado: {{output}}")
print("\\n✅ MOD-003 COMPLETADO - Casa Contenedor")
'''

script_path = zuly_path / 'temp_mod3_v3.py'
with open(script_path, 'w') as f:
    f.write(script)

blender_exe = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe"
result = subprocess.run(
    [str(blender_exe), '--background', '--python', str(script_path)],
    capture_output=True, text=True, encoding='utf-8', errors='ignore',
    cwd=str(zuly_path)
)

for line in result.stdout.split('\n'):
    if any(x in line for x in ['✅', '📦', '💡', '💾', 'MOD-003']):
        print(line)

script_path.unlink()
print("\n🏠 MOD-003 recreado con patrones del backup")
