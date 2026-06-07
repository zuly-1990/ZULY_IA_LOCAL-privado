#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🏛️ MODELO 1: Pabellón Moderno Minimalista (V2)
Usa patrones sellados del BACKUP_SEGURO
Patrones: CUB-003 + CUB-001 + MAT-002 + P-004A
"""

import subprocess
import sys
from pathlib import Path

zuly_path = Path('c:/Users/Admin/Desktop/ZULY_IA_LOCAL')
backup_path = zuly_path / 'archivo_zuly/BACKUP_SEGURO/BACKUP_20260404_211121'

# Patrones base sellados
patrones = {
    'CUB-003': backup_path / 'CUB-003_Modelado_MuroPro/blend/CUB-003_Modelado_MuroPro.blend',
    'CUB-001': backup_path / 'CUB-001_Modelado_BiselRealista/blend/CUB-001_Modelado_BiselRealista.blend',
    'MAT-002': backup_path / 'MAT-002_Material_Vidrio/blend/MAT-002_Material_Vidrio.blend',
    'P-004A': backup_path / 'P-004A_CilindroAlto/blend/P-004A_CilindroAlto.blend',
    'LUZ-001': backup_path / 'LUZ-001_Iluminacion_3Point/blend/LUZ-001_Iluminacion_3Point.blend',
}

print("="*70)
print("🏛️ RECREANDO MOD-001: Pabellon Moderno Minimalista (V2)")
print("Usando patrones sellados del BACKUP_SEGURO")
print("="*70)

# Verificar patrones existen
for nombre, ruta in patrones.items():
    if ruta.exists():
        print(f"✅ {nombre}: {ruta.name}")
    else:
        print(f"❌ {nombre}: NO ENCONTRADO")
        sys.exit(1)

script = f'''
import bpy
import mathutils
from math import radians

print("\\n" + "="*70)
print("🏛️ CONSTRUYENDO PABELLÓN CON PATRONES SELLADOS")
print("="*70)

# Limpiar
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Importar CUB-003 (Muro Pro) para muros
print("📦 Importando CUB-003 para muros...")
bpy.ops.wm.open_mainfile(filepath="{str(patrones['CUB-003']).replace('\\', '/')}")
# Duplicar y posicionar 3 muros
for i, x in enumerate([-2.5, 0, 2.5]):
    bpy.ops.object.select_all(action='DESELECT')
    # El objeto principal de CUB-003
    obj = [o for o in bpy.data.objects if o.type == 'MESH'][0]
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.duplicate()
    muro = bpy.context.active_object
    muro.name = f"Muro_{{i+1}}"
    muro.location = (x, 0, 1.35)
    muro.scale = (0.075, 3, 1.35)

# Importar P-004A (Cilindro) para columna
print("📦 Importando P-004A para columna...")
bpy.ops.wm.append(
    directory="{str(patrones['P-004A']).replace('\\', '/')}/Object/",
    filename="Cylinder"
)
columna = bpy.context.selected_objects[0]
columna.name = "Columna_Central"
columna.location = (0, 0, 1.5)
columna.scale = (0.3, 0.3, 3)

# Crear fachada de vidrio
print("📦 Creando fachada de vidrio...")
bpy.ops.mesh.primitive_plane_add(size=2, location=(0, 3, 1.35))
bpy.ops.transform.rotate(value=radians(90), orient_axis='X')
vidrio = bpy.context.active_object
vidrio.name = "Fachada_Vidrio"
vidrio.scale = (3, 1.35, 1)

# Importar material de vidrio del patrón MAT-002
with bpy.data.libraries.load("{str(patrones['MAT-002']).replace('\\', '/')}") as (data_from, data_to):
    data_to.materials = [m for m in data_from.materials if "Vidrio" in m or "Glass" in m]
if data_to.materials:
    vidrio.data.materials.append(data_to.materials[0])

# Crear techo
print("📦 Creando techo...")
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 2.85))
techo = bpy.context.active_object
techo.name = "Techo"
techo.scale = (3.5, 3.5, 0.05)

# Aplicar bevel
bevel = techo.modifiers.new(name="Bevel", type='BEVEL')
bevel.width = 0.02
bevel.segments = 2

# Importar iluminación LUZ-001
print("💡 Configurando iluminación profesional...")
bpy.ops.wm.append(
    directory="{str(patrones['LUZ-001']).replace('\\', '/')}/Object/",
    filename="Light"
)

# Cámara
bpy.ops.object.camera_add(location=(8, -6, 3))
cam = bpy.context.active_object
cam.name = "Camara_Pabellon"
cam.rotation_euler = (1.1, 0, 0.8)
bpy.context.scene.camera = cam

# Guardar
output = "./archivo_zuly/temp_arena/MOD-001_Pabellon_Minimalista.blend"
print(f"\\n💾 Guardando {{output}}...")
bpy.ops.wm.save_as_mainfile(filepath=output)

print("\\n" + "="*70)
print("✅ MOD-001 RECREADO CON PATRONES SELLADOS")
print("="*70)
'''

script_path = zuly_path / 'temp_mod1_v2.py'
with open(script_path, 'w', encoding='utf-8') as f:
    f.write(script)

blender_exe = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe"

print("\n🏛️ Ejecutando Blender...")
result = subprocess.run(
    [str(blender_exe), '--background', '--python', str(script_path)],
    capture_output=True, text=True, encoding='utf-8', errors='ignore',
    cwd=str(zuly_path)
)

if result.stdout:
    print(result.stdout[-1500:] if len(result.stdout) > 1500 else result.stdout)

script_path.unlink()
print("\n✅ MOD-001 Pabellón recreado con patrones sellados")
