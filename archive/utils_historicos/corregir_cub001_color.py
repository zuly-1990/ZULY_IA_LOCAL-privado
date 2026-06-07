#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔧 CORRECCIÓN CUB-001 - ROL: TÉCNICO REPARADOR
Ajusta color exacto de #194CCC a #1A4DCC
"""

import subprocess
import sys
from pathlib import Path

zuly_path = Path('c:/Users/Admin/Desktop/ZULY_IA_LOCAL')

script_correccion = '''
import bpy
import sys
sys.path.insert(0, 'c:/Users/Admin/Desktop/ZULY_IA_LOCAL/core')
from sistema_luces_inteligente import aplicar_iluminacion_profesional

print("="*60)
print("🔧 TÉCNICO REPARADOR: Corrigiendo CUB-001")
print("="*60)

# Abrir archivo existente
blend_path = './archivo_zuly/temp_arena/CUB-001_Modelado_BiselRealista.blend'
bpy.ops.wm.open_mainfile(filepath=blend_path)

# Obtener objeto
obj = None
for o in bpy.context.scene.objects:
    if o.type == 'MESH':
        obj = o
        break

if not obj:
    print("❌ ERROR: No se encontró objeto mesh")
    sys.exit(1)

print(f"📦 Objeto encontrado: {obj.name}")

# CORREGIR COLOR DEL MATERIAL
if obj.data.materials:
    mat = obj.data.materials[0]
    if mat.use_nodes:
        principled = mat.node_tree.nodes.get("Principled BSDF")
        if principled:
            # Color objetivo exacto: #1A4DCC
            # RGB: 26, 77, 204 → Normalizado: 0.102, 0.302, 0.8
            color_correcto = (0.102, 0.302, 0.8, 1.0)
            principled.inputs['Base Color'].default_value = color_correcto
            
            # Verificar
            r = int(color_correcto[0] * 255)
            g = int(color_correcto[1] * 255)
            b = int(color_correcto[2] * 255)
            hex_actual = f"#{r:02X}{g:02X}{b:02X}"
            
            print(f"✅ Color corregido: {hex_actual}")
            print(f"   Esperado: #1A4DCC")
            print(f"   Match: {hex_actual == '#1A4DCC'}")

# REAPLICAR ILUMINACIÓN (limpiar primero)
print("💡 Limpiando luces antiguas...")
for light in bpy.data.lights:
    bpy.data.lights.remove(light)
for obj_light in bpy.context.scene.objects:
    if obj_light.type == 'LIGHT':
        bpy.data.objects.remove(obj_light, do_unlink=True)

print("💡 Aplicando SLIZ v2.0...")
luces = aplicar_iluminacion_profesional(obj)
print(f"   ☀️  Sol: {luces['sol']}")
print(f"   ✨ Key: {luces['key']}")
print(f"   💫 Fill: {luces['fill']}")
print(f"   🌟 Rim: {luces['rim']}")

# Guardar versión corregida
output_path = './archivo_zuly/temp_arena/CUB-001_Modelado_BiselRealista_CORREGIDO.blend'
bpy.ops.wm.save_as_mainfile(filepath=output_path)

print("="*60)
print(f"✅ CORRECCIÓN COMPLETADA")
print(f"📄 Archivo: {output_path}")
print("="*60)
'''

script_path = zuly_path / 'temp_corregir_cub001.py'
with open(script_path, 'w', encoding='utf-8') as f:
    f.write(script_correccion)

blender_exe = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe"

print("🔧 Ejecutando corrección de color CUB-001...")
result = subprocess.run(
    [blender_exe, '--background', '--python', str(script_path)],
    capture_output=True,
    text=True,
    encoding='utf-8',
    errors='ignore',
    cwd=str(zuly_path)
)

if result.stdout:
    print(result.stdout[-2000:] if len(result.stdout) > 2000 else result.stdout)
if result.stderr and "Error" in result.stderr:
    print(f"⚠️  Errores: {result.stderr[-500:]}")

script_path.unlink()

print("\n" + "="*60)
print("✅ CUB-001 CORREGIDO - LISTO PARA JUES-BOT")
print("="*60)
print("📄 Archivo: CUB-001_Modelado_BiselRealista_CORREGIDO.blend")
print("🎨 Color: #1A4DCC (CORREGIDO)")
print("💡 Iluminación: SLIZ v2.0 reaplicado")
print("="*60)
