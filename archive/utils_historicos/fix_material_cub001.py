#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔧 CORRECCIÓN DIRECTA - Aplicar material azul #1A4DCC a CUB-001 existente
"""

import subprocess
import sys
from pathlib import Path

zuly_path = Path('c:/Users/Admin/Desktop/ZULY_IA_LOCAL')

script_fix = '''
import bpy

print("="*60)
print("🔧 CORRECCIÓN DIRECTA DE MATERIAL")
print("🎨 Objetivo: #1A4DCC")
print("="*60)

# Abrir CUB-001
blend_path = './archivo_zuly/temp_arena/CUB-001_Modelado_BiselRealista.blend'
bpy.ops.wm.open_mainfile(filepath=blend_path)

# Obtener objeto cubo
obj = None
for o in bpy.context.scene.objects:
    if o.type == 'MESH' and 'CUB' in o.name:
        obj = o
        break

if not obj:
    print("❌ No se encontró objeto CUB")
    sys.exit(1)

print(f"📦 Objeto: {obj.name}")

# ELIMINAR TODOS LOS MATERIALES PREVIOS
print("🗑️ Eliminando materiales previos...")
obj.data.materials.clear()  # Limpiar slots de materiales
for mat in bpy.data.materials:
    if mat:
        bpy.data.materials.remove(mat)

# CREAR MATERIAL AZUL EXACTO #1A4DCC
print("🎨 Creando material azul #1A4DCC...")
mat = bpy.data.materials.new(name="Mat_Azul_Exacto")
mat.use_nodes = True

# Configurar Principled BSDF
principled = mat.node_tree.nodes.get("Principled BSDF")
if principled:
    # #1A4DCC = RGB(26, 77, 204)
    r, g, b = 26/255, 77/255, 204/255
    principled.inputs['Base Color'].default_value = (r, g, b, 1.0)
    principled.inputs['Roughness'].default_value = 0.3
    principled.inputs['Specular'].default_value = 0.7
    
    print(f"   Base Color: ({r:.3f}, {g:.3f}, {b:.3f})")
    
    # Verificar
    actual_r = int(principled.inputs['Base Color'].default_value[0] * 255)
    actual_g = int(principled.inputs['Base Color'].default_value[1] * 255)
    actual_b = int(principled.inputs['Base Color'].default_value[2] * 255)
    hex_actual = f"#{actual_r:02X}{actual_g:02X}{actual_b:02X}"
    print(f"   Hex result: {hex_actual}")

# ASIGNAR MATERIAL AL OBJETO (slot 0)
print("🔗 Asignando material al objeto...")
obj.data.materials.append(mat)

# Verificar asignación
if len(obj.data.materials) > 0:
    mat_asignado = obj.data.materials[0]
    print(f"✅ Material asignado: {mat_asignado.name}")
    
    # Forzar actualización
    obj.data.update()
    
    # Verificar color final
    if mat_asignado.use_nodes:
        principled_final = mat_asignado.node_tree.nodes.get("Principled BSDF")
        if principled_final:
            r = int(principled_final.inputs['Base Color'].default_value[0] * 255)
            g = int(principled_final.inputs['Base Color'].default_value[1] * 255)
            b = int(principled_final.inputs['Base Color'].default_value[2] * 255)
            hex_final = f"#{r:02X}{g:02X}{b:02X}"
            print(f"🎨 Color final en objeto: {hex_final}")

# Guardar
print("💾 Guardando...")
bpy.ops.wm.save_as_mainfile(filepath=blend_path)

print("="*60)
print("✅ CORRECCIÓN COMPLETADA")
print("="*60)
'''

script_path = zuly_path / 'temp_fix_material.py'
with open(script_path, 'w', encoding='utf-8') as f:
    f.write(script_fix)

blender_exe = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe"

print("🔧 Aplicando corrección de material...")
result = subprocess.run(
    [blender_exe, '--background', '--python', str(script_path)],
    capture_output=True,
    text=True,
    encoding='utf-8',
    errors='ignore',
    cwd=str(zuly_path)
)

if result.stdout:
    print(result.stdout[-1500:] if len(result.stdout) > 1500 else result.stdout)

script_path.unlink()

print("\n✅ Material corregido - Revalidando...")
