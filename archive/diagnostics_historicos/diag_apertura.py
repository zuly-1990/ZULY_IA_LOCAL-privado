#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 DIAGNÓSTICO - Qué pasa al abrir el archivo con JUES-BOT
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
print("🔍 DIAGNÓSTICO APERTURA ARCHIVO")
print("="*60)

# Abrir como hace JUES-BOT
blend_path = './archivo_zuly/temp_arena/CUB-001_Modelado_BiselRealista.blend'
print(f"Abriendo: {blend_path}")
bpy.ops.wm.open_mainfile(filepath=blend_path)

print(f"\\n📦 Objetos tras abrir: {len(bpy.context.scene.objects)}")
for obj in bpy.context.scene.objects:
    print(f"   - {obj.name} (tipo: {obj.type})")
    if obj.type == 'MESH':
        print(f"     Materiales: {len(obj.data.materials)}")
        for i, mat in enumerate(obj.data.materials):
            if mat:
                print(f"       [{i}] {mat.name}")

# Buscar primer MESH como hace JUES
print("\\n🔍 Buscando primer MESH...")
obj = None
for o in bpy.context.scene.objects:
    if o.type == 'MESH':
        obj = o
        break

print(f"   Primer MESH encontrado: {obj.name if obj else 'None'}")

if obj and obj.data.materials:
    mat = obj.data.materials[0]
    print(f"   Material: {mat.name}")
    if mat.use_nodes:
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            c = bsdf.inputs['Base Color'].default_value
            hex_color = f"#{int(c[0]*255):02X}{int(c[1]*255):02X}{int(c[2]*255):02X}"
            print(f"   Color: {hex_color}")

print("="*60)
'''

script_path = zuly_path / 'temp_diag_apertura.py'
with open(script_path, 'w', encoding='utf-8') as f:
    f.write(script_diag)

blender_exe = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe"

print("🔍 Ejecutando diagnóstico de apertura...")
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
