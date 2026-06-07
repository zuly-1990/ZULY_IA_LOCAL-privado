#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔧 CORREGIR P-006A - Plano con volumen mínimo
"""

import subprocess
import sys
from pathlib import Path

zuly_path = Path('c:/Users/Admin/Desktop/ZULY_IA_LOCAL')

script_fix = '''
import bpy
import sys
sys.path.insert(0, 'c:/Users/Admin/Desktop/ZULY_IA_LOCAL/core')
from sistema_luces_inteligente import aplicar_iluminacion_profesional
import mathutils

print("🔧 CORREGIR P-006A_PlanoBase...")

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Crear plano con extrusión (darle volumen mínimo)
print("1️⃣ Creando plano base 4x4m...")
bpy.ops.mesh.primitive_plane_add(size=4, location=(0, 0, 0))
plano = bpy.context.active_object
plano.name = "P-006A_PlanoBase"

# Modo edit y extruir para darle volumen
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.transform.translate(value=(0, 0, 0.01))  # Mover 1cm arriba
bpy.ops.object.mode_set(mode='OBJECT')

# Añadir Solidify modifier para grosor
solidify = plano.modifiers.new(name="Solidify_Grosor", type='SOLIDIFY')
solidify.thickness = 0.02  # 2cm de grosor

# Aplicar
bpy.context.view_layer.objects.active = plano
bpy.ops.object.modifier_apply(modifier="Solidify_Grosor")

# Material
mat = bpy.data.materials.new(name="Mat_P-006A")
mat.use_nodes = True
bsdf = mat.node_tree.nodes.get("Principled BSDF")
if bsdf:
    bsdf.inputs['Base Color'].default_value = (0.9, 0.9, 0.9, 1.0)
    bsdf.inputs['Roughness'].default_value = 0.8
plano.data.materials.append(mat)

# Iluminación
luces = aplicar_iluminacion_profesional(plano)

# Cámara
cam_pos = mathutils.Vector((5, -5, 3))
bpy.ops.object.camera_add(location=cam_pos)
cam = bpy.context.active_object
direction = mathutils.Vector((0, 0, 0.01)) - cam.location
cam.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
bpy.context.scene.camera = cam

# Guardar
output = './archivo_zuly/temp_arena/P-006A_PlanoBase.blend'
bpy.ops.wm.save_as_mainfile(filepath=output)

print(f"✅ P-006A corregido: plano con grosor 2cm")
'''

script_path = zuly_path / 'temp_fix_p006.py'
with open(script_path, 'w', encoding='utf-8') as f:
    f.write(script_fix)

blender_exe = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe"

print("🔧 Corrigiendo P-006A...")
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
print("\n✅ P-006A corregido")
