#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🏛️ MODELO 1: Pabellón Moderno Minimalista (V3 - BACKUP)
Usa patrones sellados del BACKUP_SEGURO - Estrategia APPEND
"""

import subprocess
import sys
from pathlib import Path

zuly_path = Path('c:/Users/Admin/Desktop/ZULY_IA_LOCAL')
backup_path = zuly_path / 'archivo_zuly/BACKUP_SEGURO/BACKUP_20260404_211121'

# Rutas con forward slashes para Blender
patrones = {
    'CUB-003': str(backup_path / 'CUB-003_Modelado_MuroPro/blend/CUB-003_Modelado_MuroPro.blend').replace('\\', '/'),
    'MAT-002': str(backup_path / 'MAT-002_Material_Vidrio/blend/MAT-002_Material_Vidrio.blend').replace('\\', '/'),
    'P-004A': str(backup_path / 'P-004A_CilindroAlto/blend/P-004A_CilindroAlto.blend').replace('\\', '/'),
    'LUZ-001': str(backup_path / 'LUZ-001_Iluminacion_3Point/blend/LUZ-001_Iluminacion_3Point.blend').replace('\\', '/'),
}

print("="*70)
print("🏛️ RECREANDO MOD-001 CON PATRONES SELLADOS (V3 - BACKUP)")
print("="*70)

for nombre, ruta in patrones.items():
    existe = "✅" if Path(ruta.replace('/', '\\')).exists() else "❌"
    print(f"{existe} {nombre}")

script = f'''
import bpy
from math import radians

print("\\n" + "="*70)
print("🏛️ CONSTRUYENDO PABELLÓN CON PATRONES SELLADOS")
print("="*70)

# Limpiar escena
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Función para importar objeto con aplicación de escala
def importar_objeto(blend_path, obj_name, new_name, location, scale):
    print(f"  [INFO] Importando {obj_name}...")
    try:
        bpy.ops.wm.append(directory=blend_path + "/Object/", filename=obj_name)
        if bpy.context.selected_objects:
            obj = bpy.context.selected_objects[0]
            obj.name = new_name
            obj.location = location
            obj.scale = scale
            # Aplicar escala
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.transform_apply(scale=True)
            print(f"    [OK] {new_name}")
            return obj
    except Exception as e:
        print(f"    [!] Error: {e}")
    return None

# 1. MUROS - 3 veces desde CUB-003
print("📦 Creando muros...")
for i, x in enumerate([-2.5, 0, 2.5]):
    importar_objeto("{patrones['CUB-003']}", "Cube", f"Muro_{{i+1}}", (x, 0, 1.35), (0.075, 3, 1.35))

# 2. COLUMNA
print("📦 Creando columna...")
importar_objeto("{patrones['P-004A']}", "Cylinder", "Columna_Central", (0, 0, 1.5), (0.3, 0.3, 3))

# 3. FACHADA VIDRIO - Cubo delgado en lugar de plano (evita non-manifold)
print("[INFO] Creando fachada de vidrio...")
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 3, 1.35))
bpy.ops.transform.rotate(value=radians(90), orient_axis='X')
vidrio = bpy.context.active_object
vidrio.name = "Fachada_Vidrio"
vidrio.scale = (3, 1.35, 0.02)  # Espesor 0.02m
# Aplicar escala
bpy.ops.object.transform_apply(scale=True)

print("[INFO] Importando material...")
with bpy.data.libraries.load("{patrones['MAT-002']}") as (data_from, data_to):
    data_to.materials = data_from.materials
if data_to.materials:
    vidrio.data.materials.append(data_to.materials[0])
    print("  [OK] Material vidrio aplicado")

# 4. TECHO con aplicacion de escala
print("[INFO] Creando techo...")
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 2.85))
techo = bpy.context.active_object
techo.name = "Techo"
techo.scale = (3.5, 3.5, 0.05)
# Aplicar escala
bpy.context.view_layer.objects.active = techo
bpy.ops.object.transform_apply(scale=True)
bevel = techo.modifiers.new(name="Bevel", type='BEVEL')
bevel.width = 0.02
bevel.segments = 2

# 5. LUZ y RENDER SETTINGS
print("[INFO] Configurando iluminacion...")
try:
    bpy.ops.wm.append(directory="{patrones['LUZ-001']}" + "/Object/", filename="Light")
    print("  [OK] Luz importada")
except:
    bpy.ops.object.light_add(type='SUN', location=(5, 5, 10))
    print("  [!] Luz basica creada")

# Configurar SSR en Eevee
print("[INFO] Configurando render...")
bpy.context.scene.render.engine = 'BLENDER_EEVEE'
bpy.context.scene.eevee.use_ssr = True
bpy.context.scene.eevee.ssr_thickness = 0.1

# 6. CÁMARA
bpy.ops.object.camera_add(location=(8, -6, 3))
cam = bpy.context.active_object
cam.name = "Camara_Pabellon"
cam.rotation_euler = (1.1, 0, 0.8)
bpy.context.scene.camera = cam

# Guardar
output = "./archivo_zuly/temp_arena/MOD-001_Pabellon_Minimalista.blend"
bpy.ops.wm.save_as_mainfile(filepath=output)
print(f"\\n💾 Guardado: {{output}}")
print("\\n✅ MOD-001 COMPLETADO")
'''

script_path = zuly_path / 'temp_mod1_v3.py'
with open(script_path, 'w', encoding='utf-8') as f:
    f.write(script)

blender_exe = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe"

result = subprocess.run(
    [str(blender_exe), '--background', '--python', str(script_path)],
    capture_output=True, text=True, encoding='utf-8', errors='ignore',
    cwd=str(zuly_path)
)

if result.stdout:
    lines = result.stdout.split('\n')
    for line in lines:
        if any(x in line for x in ['✅', '⚠️', '❌', '📦', '🎨', '💡', '💾', 'MOD-001']):
            print(line)

script_path.unlink()
print("\n🏛️ MOD-001 recreado con patrones del backup")
