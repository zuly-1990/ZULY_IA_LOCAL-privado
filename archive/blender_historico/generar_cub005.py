#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🆕 CUB-005 - Modificador_BooleanExacto
Operaciones booleanas precisas (unión, diferencia, intersección)
"""

import subprocess
import sys
from pathlib import Path

zuly_path = Path('c:/Users/Admin/Desktop/ZULY_IA_LOCAL')

script_cub005 = '''
import bpy
import sys
import mathutils
sys.path.insert(0, 'c:/Users/Admin/Desktop/ZULY_IA_LOCAL/core')
from sistema_luces_inteligente import aplicar_iluminacion_profesional

print("="*60)
print("🆕 CUB-005 - Modificador_BooleanExacto")
print("="*60)

# Limpiar
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# 1. CREAR CUBO BASE (objeto A)
print("1️⃣ Creando cubo base...")
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 1))
cubo_base = bpy.context.active_object
cubo_base.name = "CUB-005_Base"

# 2. CREAR CILINDRO (objeto B - para cortar)
print("2️⃣ Creando cilindro booleano...")
bpy.ops.mesh.primitive_cylinder_add(radius=0.6, depth=3, location=(0, 0, 1), vertices=32)
cilindro = bpy.context.active_object
cilindro.name = "CUB-005_Cortador"

# 3. APLICAR BOOLEAN DIFFERENCE
print("3️⃣ Aplicando Boolean Difference...")
bool_mod = cubo_base.modifiers.new(name="Boolean_Corte", type='BOOLEAN')
bool_mod.operation = 'DIFFERENCE'
bool_mod.object = cilindro

# Aplicar el modificador
bpy.context.view_layer.objects.active = cubo_base
bpy.ops.object.modifier_apply(modifier="Boolean_Corte")

# Eliminar cilindro (ya no necesario)
bpy.data.objects.remove(cilindro, do_unlink=True)

# 4. BEVEL EN BORDES DEL CORTE
print("4️⃣ Suavizando bordes del corte...")
bevel = cubo_base.modifiers.new(name="Bevel_Corte", type='BEVEL')
bevel.width = 0.03
bevel.segments = 2
bevel.limit_method = 'ANGLE'
bevel.angle_limit = 0.7854

# Renombrar objeto final
cubo_base.name = "CUB-005_BooleanExacto"

# 5. MATERIAL ROJO BOOLEAN
print("5️⃣ Creando material...")
mat = bpy.data.materials.new(name="Mat_Boolean_Rojo")
mat.use_nodes = True
bsdf = mat.node_tree.nodes.get("Principled BSDF")
if bsdf:
    # Rojo #D32F2F
    r, g, b = 211/255, 47/255, 47/255
    bsdf.inputs['Base Color'].default_value = (r, g, b, 1.0)
    bsdf.inputs['Roughness'].default_value = 0.4
    bsdf.inputs['Specular'].default_value = 0.6
cubo_base.data.materials.append(mat)

# 6. ILUMINACIÓN SLIZ
print("6️⃣ Aplicando SLIZ...")
luces = aplicar_iluminacion_profesional(cubo_base)

# 7. CÁMARA
cam_pos = mathutils.Vector((4, -4, 2))
bpy.ops.object.camera_add(location=cam_pos)
cam = bpy.context.active_object
direction = cubo_base.location - cam.location
cam.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
bpy.context.scene.camera = cam

# 8. Guardar
output = './archivo_zuly/temp_arena/CUB-005_BooleanExacto.blend'
bpy.ops.wm.save_as_mainfile(filepath=output)

print("\\n" + "="*60)
print("✅ CUB-005 BOOLEAN EXACTO CREADO")
print("="*60)
print(f"📁 {output}")
print(f"🔧 Operación: Cubo - Cilindro = Boolean Difference")
print(f"🎨 Color: #D32F2F (Rojo boolean)")
'''

script_path = zuly_path / 'temp_cub005.py'
with open(script_path, 'w', encoding='utf-8') as f:
    f.write(script_cub005)

blender_exe = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe"

print("🆕 Generando CUB-005 BooleanExacto...")
result = subprocess.run(
    [str(blender_exe), '--background', '--python', str(script_path)],
    capture_output=True,
    text=True,
    encoding='utf-8',
    errors='ignore',
    cwd=str(zuly_path)
)

if result.stdout:
    print(result.stdout[-2000:] if len(result.stdout) > 2000 else result.stdout)

script_path.unlink()

print("\n✅ CUB-005 generado")
