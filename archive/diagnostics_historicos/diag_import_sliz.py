#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 DIAGNÓSTICO - Qué pasa al importar SLIZ
"""

import subprocess
import sys
from pathlib import Path

zuly_path = Path('c:/Users/Admin/Desktop/ZULY_IA_LOCAL')

script_diag = '''
import bpy

print("="*60)
print("🔍 DIAGNÓSTICO IMPORTACIÓN SLIZ")
print("="*60)

# Abrir archivo
blend_path = './archivo_zuly/temp_arena/CUB-001_Modelado_BiselRealista.blend'
bpy.ops.wm.open_mainfile(filepath=blend_path)

print(f"\\n1️⃣ Tras abrir archivo:")
print(f"   Objetos: {len(bpy.context.scene.objects)}")
for obj in bpy.context.scene.objects:
    if obj.type == 'MESH':
        print(f"   MESH: {obj.name}")

# Buscar primer mesh
obj = None
for o in bpy.context.scene.objects:
    if o.type == 'MESH':
        obj = o
        break
print(f"\\n   Primer MESH: {obj.name if obj else 'None'}")

# AHORA importar SLIZ (como hace JUES-BOT)
print(f"\\n2️⃣ Importando SLIZ...")
import sys
sys.path.insert(0, 'c:/Users/Admin/Desktop/ZULY_IA_LOCAL/core')
from sistema_luces_inteligente import aplicar_iluminacion_profesional

print(f"\\n3️⃣ Tras importar SLIZ:")
print(f"   Objetos: {len(bpy.context.scene.objects)}")
for obj in bpy.context.scene.objects:
    if obj.type == 'MESH':
        print(f"   MESH: {obj.name}")

# Buscar primer mesh de nuevo
obj = None
for o in bpy.context.scene.objects:
    if o.type == 'MESH':
        obj = o
        break
print(f"\\n   Primer MESH: {obj.name if obj else 'None'}")

print("="*60)
'''

script_path = zuly_path / 'temp_diag_import.py'
with open(script_path, 'w', encoding='utf-8') as f:
    f.write(script_diag)

blender_exe = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe"

print("🔍 Ejecutando diagnóstico de importación...")
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
