#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 DIAGNÓSTICO - Verificar qué material tiene CUB-001
"""

import subprocess
import sys
from pathlib import Path

zuly_path = Path('c:/Users/Admin/Desktop/ZULY_IA_LOCAL')

script_diag = '''
import bpy

print("="*60)
print("🔍 DIAGNÓSTICO DE MATERIAL")
print("="*60)

# Abrir archivo
blend_path = './archivo_zuly/temp_arena/CUB-001_Modelado_BiselRealista.blend'
bpy.ops.wm.open_mainfile(filepath=blend_path)

print(f"\\n📦 Objetos en escena: {len(bpy.context.scene.objects)}")

for obj in bpy.context.scene.objects:
    print(f"\\n   Objeto: {obj.name} | Tipo: {obj.type}")
    if obj.type == 'MESH':
        print(f"   Materiales: {len(obj.data.materials)}")
        for i, mat in enumerate(obj.data.materials):
            if mat:
                print(f"      [{i}] {mat.name}")
                if mat.use_nodes:
                    bsdf = mat.node_tree.nodes.get("Principled BSDF")
                    if bsdf:
                        c = bsdf.inputs['Base Color'].default_value
                        hex_color = f"#{int(c[0]*255):02X}{int(c[1]*255):02X}{int(c[2]*255):02X}"
                        print(f"          Color: {hex_color}")
                        print(f"          RGB: ({c[0]:.3f}, {c[1]:.3f}, {c[2]:.3f})")

print("\\n" + "="*60)
'''

script_path = zuly_path / 'temp_diagnostico.py'
with open(script_path, 'w', encoding='utf-8') as f:
    f.write(script_diag)

blender_exe = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe"

print("🔍 Ejecutando diagnóstico...")
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
