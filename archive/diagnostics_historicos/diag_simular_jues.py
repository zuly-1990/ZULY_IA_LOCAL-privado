#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 DIAGNÓSTICO - Ejecutar pasos exactos de JUES-BOT
"""

import subprocess
import sys
from pathlib import Path

zuly_path = Path('c:/Users/Admin/Desktop/ZULY_IA_LOCAL')

script_diag = '''
import bpy
import sys
sys.path.insert(0, 'c:/Users/Admin/Desktop/ZULY_IA_LOCAL/core')

print("="*60)
print("🔍 SIMULANDO JUES-BOT PASO A PASO")
print("="*60)

# PASO 1: Abrir archivo
blend_path = './archivo_zuly/temp_arena/CUB-001_Modelado_BiselRealista.blend'
print(f"\\n1️⃣ Abriendo archivo...")
bpy.ops.wm.open_mainfile(filepath=blend_path)

print(f"   Objetos: {len(bpy.context.scene.objects)}")
mesh_objects = [o for o in bpy.context.scene.objects if o.type == 'MESH']
print(f"   MESH objects: {[o.name for o in mesh_objects]}")

# PASO 2: Obtener primer mesh
print(f"\\n2️⃣ Buscando primer MESH...")
obj = None
for o in bpy.context.scene.objects:
    if o.type == 'MESH':
        obj = o
        break
print(f"   Encontrado: {obj.name if obj else 'None'}")
objeto_original = obj

# PASO 3: Importar SLIZ
print(f"\\n3️⃣ Importando SLIZ...")
from sistema_luces_inteligente import aplicar_iluminacion_profesional

# PASO 4: Aplicar SLIZ
print(f"\\n4️⃣ Aplicando SLIZ...")
if objeto_original:
    luces = aplicar_iluminacion_profesional(objeto_original)
    print(f"   Luces creadas: {list(luces.keys())}")

# PASO 5: Verificar objetos tras SLIZ
print(f"\\n5️⃣ Tras aplicar SLIZ:")
print(f"   Objetos: {len(bpy.context.scene.objects)}")
mesh_objects = [o for o in bpy.context.scene.objects if o.type == 'MESH']
print(f"   MESH objects: {[o.name for o in mesh_objects]}")

# PASO 6: Validar color del objeto_original
print(f"\\n6️⃣ Validando objeto_original ({objeto_original.name}):")
if objeto_original.data.materials:
    mat = objeto_original.data.materials[0]
    print(f"   Material: {mat.name}")
    if mat.use_nodes:
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            c = bsdf.inputs['Base Color'].default_value
            hex_color = f"#{int(c[0]*255):02X}{int(c[1]*255):02X}{int(c[2]*255):02X}"
            print(f"   Color: {hex_color}")

print("="*60)
'''

script_path = zuly_path / 'temp_diag_jues.py'
with open(script_path, 'w', encoding='utf-8') as f:
    f.write(script_diag)

blender_exe = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe"

print("🔍 Ejecutando simulación JUES-BOT...")
result = subprocess.run(
    [blender_exe, '--background', '--python', str(script_path)],
    capture_output=True,
    text=True,
    encoding='utf-8',
    errors='ignore',
    cwd=str(zuly_path)
)

if result.stdout:
    print(result.stdout)

script_path.unlink()
