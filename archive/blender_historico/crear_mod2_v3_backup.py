#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🏢 MODELO 2: Torre Corporativa (V3 - BACKUP)
Patrones: CUB-002 + CUB-005 + MAT-001 + P-001B
"""

import subprocess
from pathlib import Path

zuly_path = Path('c:/Users/Admin/Desktop/ZULY_IA_LOCAL')
backup = zuly_path / 'archivo_zuly/BACKUP_SEGURO/BACKUP_20260404_211121'

patrones = {
    'CUB-002': str(backup / 'CUB-002_Transform_PivoteSuelo/blend/CUB-002_Transform_PivoteSuelo.blend').replace('\\', '/'),
    'CUB-005': str(backup / 'CUB-005_BooleanExacto/blend/CUB-005_BooleanExacto.blend').replace('\\', '/'),
    'MAT-001': str(backup / 'MAT-001_Material_Metal/blend/MAT-001_Material_Metal.blend').replace('\\', '/'),
    'P-001B': str(backup / 'P-001B_CuboBasico_2m/blend/P-001B_CuboBasico_2m.blend').replace('\\', '/'),
    'LUZ-001': str(backup / 'LUZ-001_Iluminacion_3Point/blend/LUZ-001_Iluminacion_3Point.blend').replace('\\', '/'),
}

print("="*70)
print("🏢 RECREANDO MOD-002: Torre Corporativa (V3 - BACKUP)")
print("="*70)

script = f'''
import bpy
from math import radians

print("\\n🏢 CONSTRUYENDO TORRE CORPORATIVA")
print("="*70)

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# NÚCLEO CENTRAL - 3 cubos apilados desde P-001B
print("📦 Creando núcleo central...")
for i, z in enumerate([1, 3, 5]):
    bpy.ops.wm.append(directory="{patrones['P-001B']}" + "/Object/", filename="Cube")
    if bpy.context.selected_objects:
        cubo = bpy.context.selected_objects[0]
        cubo.name = f"Nucleo_{{i+1}}"
        cubo.location = (0, 0, z)
        cubo.scale = (0.8, 0.8, 1)
        print(f"  ✅ Nucleo_{{i+1}}")

# NIVELES CON VENTANAS - Boolean desde CUB-005
print("📦 Creando niveles con boolean...")
for nivel, z in enumerate([1.5, 3.5, 5.5], 1):
    # Piso principal
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, z))
    piso = bpy.context.active_object
    piso.name = f"Nivel_{{nivel}}"
    piso.scale = (2.5, 2.5, 0.1)
    
    # Ventanas (cubos pequeños para boolean difference)
    for x in [-1, 1]:
        bpy.ops.mesh.primitive_cube_add(size=1, location=(x, 2.6, z))
        ventana = bpy.context.active_object
        ventana.name = f"Ventana_{{nivel}}_{{'L' if x<0 else 'R'}}"
        ventana.scale = (0.3, 0.1, 0.5)
        
        # Aplicar boolean
        bool_mod = piso.modifiers.new(name=f"Boolean_{{nivel}}", type='BOOLEAN')
        bool_mod.object = ventana
        bool_mod.operation = 'DIFFERENCE'
        
        # Ocultar ventana (solo usada para boolean)
        ventana.hide_set(True)
        ventana.hide_render = True

# ESTRUCTURA EXTERIOR - Desde CUB-002 con transformaciones
print("📦 Creando estructura exterior...")
bpy.ops.wm.append(directory="{patrones['CUB-002']}" + "/Object/", filename="Cube")
if bpy.context.selected_objects:
    base = bpy.context.selected_objects[0]
    base.name = "Base_Estructura"
    base.location = (0, 0, 0.1)
    base.scale = (3, 3, 0.2)
    print("  ✅ Base estructura")

# Aplicar material metálico a todo
print("🎨 Aplicando material metálico...")
with bpy.data.libraries.load("{patrones['MAT-001']}") as (data_from, data_to):
    data_to.materials = data_from.materials

if data_to.materials:
    metal = data_to.materials[0]
    for obj in bpy.data.objects:
        if obj.type == 'MESH' and len(obj.data.materials) == 0:
            obj.data.materials.append(metal)
    print("  ✅ Material metal aplicado")

# ILUMINACIÓN
print("💡 Configurando iluminación...")
bpy.ops.wm.append(directory="{patrones['LUZ-001']}" + "/Object/", filename="Light")
print("  ✅ Luz importada")

# CÁMARA
bpy.ops.object.camera_add(location=(12, -8, 8))
cam = bpy.context.active_object
cam.name = "Camara_Torre"
cam.rotation_euler = (1.0, 0, 0.6)
bpy.context.scene.camera = cam

# Guardar
output = "./archivo_zuly/temp_arena/MOD-002_Torre_Corporativa.blend"
bpy.ops.wm.save_as_mainfile(filepath=output)
print(f"\\n💾 Guardado: {{output}}")
print("\\n✅ MOD-002 COMPLETADO - Torre Corporativa")
'''

script_path = zuly_path / 'temp_mod2_v3.py'
with open(script_path, 'w') as f:
    f.write(script)

blender_exe = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe"
result = subprocess.run(
    [str(blender_exe), '--background', '--python', str(script_path)],
    capture_output=True, text=True, encoding='utf-8', errors='ignore',
    cwd=str(zuly_path)
)

for line in result.stdout.split('\n'):
    if any(x in line for x in ['✅', '📦', '🎨', '💡', '💾', 'MOD-002']):
        print(line)

script_path.unlink()
print("\n🏢 MOD-002 recreado con patrones del backup")
