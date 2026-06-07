#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔧 CORREGIR LUZ-001/002 - Colores exactos
"""

import subprocess
import sys
from pathlib import Path

zuly_path = Path('c:/Users/Admin/Desktop/ZULY_IA_LOCAL')

# Primero verifico qué color tiene actualmente
script_diag = '''
import bpy

# Abrir LUZ-001
bpy.ops.wm.open_mainfile(filepath='./archivo_zuly/temp_arena/LUZ-001_Iluminacion_3Point.blend')

# Buscar objeto y color
obj = None
for o in bpy.context.scene.objects:
    if o.type == 'MESH':
        obj = o
        break

if obj and obj.data.materials:
    mat = obj.data.materials[0]
    if mat.use_nodes:
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            c = bsdf.inputs['Base Color'].default_value
            hex_color = f"#{int(c[0]*255):02X}{int(c[1]*255):02X}{int(c[2]*255):02X}"
            print(f"LUZ-001 Color: {hex_color}")

# Abrir LUZ-002
bpy.ops.wm.open_mainfile(filepath='./archivo_zuly/temp_arena/LUZ-002_Iluminacion_HDRI.blend')

obj = None
for o in bpy.context.scene.objects:
    if o.type == 'MESH':
        obj = o
        break

if obj and obj.data.materials:
    mat = obj.data.materials[0]
    if mat.use_nodes:
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            c = bsdf.inputs['Base Color'].default_value
            hex_color = f"#{int(c[0]*255):02X}{int(c[1]*255):02X}{int(c[2]*255):02X}"
            print(f"LUZ-002 Color: {hex_color}")
'''

script_path = zuly_path / 'temp_diag_luz.py'
with open(script_path, 'w', encoding='utf-8') as f:
    f.write(script_diag)

blender_exe = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe"

print("🔍 Diagnosticando colores LUZ-001/002...")
result = subprocess.run(
    [str(blender_exe), '--background', '--python', str(script_path)],
    capture_output=True,
    text=True,
    encoding='utf-8',
    errors='ignore',
    cwd=str(zuly_path)
)

if result.stdout:
    print(result.stdout[-1000:] if len(result.stdout) > 1000 else result.stdout)

script_path.unlink()

# Ahora corrijo con colores exactos
script_fix = '''
import bpy

# Corregir LUZ-001 con color exacto #B0B0B0
print("🔧 Corrigiendo LUZ-001...")
bpy.ops.wm.open_mainfile(filepath='./archivo_zuly/temp_arena/LUZ-001_Iluminacion_3Point.blend')

obj = None
for o in bpy.context.scene.objects:
    if o.type == 'MESH':
        obj = o
        break

if obj and obj.data.materials:
    mat = obj.data.materials[0]
    if mat.use_nodes:
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            # #B0B0B0 exacto
            r = 176/255
            g = 176/255  
            b = 176/255
            bsdf.inputs['Base Color'].default_value = (r, g, b, 1.0)
            print(f"   Color ajustado a #B0B0B0")

bpy.ops.wm.save_as_mainfile(filepath='./archivo_zuly/temp_arena/LUZ-001_Iluminacion_3Point.blend')
print("   ✅ LUZ-001 corregido")

# Corregir LUZ-002 con color exacto #99AACC
print("\\n🔧 Corrigiendo LUZ-002...")
bpy.ops.wm.open_mainfile(filepath='./archivo_zuly/temp_arena/LUZ-002_Iluminacion_HDRI.blend')

obj = None
for o in bpy.context.scene.objects:
    if o.type == 'MESH':
        obj = o
        break

if obj and obj.data.materials:
    mat = obj.data.materials[0]
    if mat.use_nodes:
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            # #99AACC exacto
            r = 153/255
            g = 170/255
            b = 204/255
            bsdf.inputs['Base Color'].default_value = (r, g, b, 1.0)
            print(f"   Color ajustado a #99AACC")

bpy.ops.wm.save_as_mainfile(filepath='./archivo_zuly/temp_arena/LUZ-002_Iluminacion_HDRI.blend')
print("   ✅ LUZ-002 corregido")

print("\\n🔧 Corrección completada")
'''

script_path = zuly_path / 'temp_fix_luz.py'
with open(script_path, 'w', encoding='utf-8') as f:
    f.write(script_fix)

print("\n🔧 Corrigiendo colores...")
result = subprocess.run(
    [str(blender_exe), '--background', '--python', str(script_path)],
    capture_output=True,
    text=True,
    encoding='utf-8',
    errors='ignore',
    cwd=str(zuly_path)
)

if result.stdout:
    print(result.stdout[-1000:] if len(result.stdout) > 1000 else result.stdout)

script_path.unlink()

print("\n✅ LUZ-001/002 corregidos")
