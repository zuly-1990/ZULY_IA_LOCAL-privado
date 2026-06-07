#!/usr/bin/env python3
"""
ZULY abre cubo_biselado y aplica COLOR al agujero
"""

import subprocess
import tempfile
from pathlib import Path

BLENDER_PATH = Path(r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe")
BLEND_FILE = Path(r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\ZULY_PROJECTS\cubo_biselado.blend")

code = """
import bpy

print("[ZULY] Abriendo cubo_biselado.blend...")

# ABRIR ARCHIVO
filepath = r'C:\\Users\\Admin\\Desktop\\ZULY_IA_LOCAL\\ZULY_PROJECTS\\cubo_biselado.blend'
bpy.ops.wm.open_mainfile(filepath=filepath)

print("[ZULY] Archivo abierto")

# CREAR MATERIAL NARANJA PARA EL AGUJERO
mat_naranja = bpy.data.materials.new(name="ColorAgujero")
mat_naranja.use_nodes = True
nodes = mat_naranja.node_tree.nodes
links = mat_naranja.node_tree.links

# Limpiar nodos
nodes.clear()

# Crear nodos
bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
output = nodes.new(type='ShaderNodeOutputMaterial')

# Color naranja brillante
bsdf.inputs['Base Color'].default_value = (1.0, 0.55, 0.1, 1.0)
bsdf.inputs['Roughness'].default_value = 0.15

links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

print("[ZULY] Material naranja creado")

# BUSCAR EL CILINDRO (AGUJERO) Y APLICAR MATERIAL
encontrado = False
for obj in bpy.context.scene.objects:
    if obj.type == 'MESH' and 'Agujero' in obj.name:
        obj.data.materials.clear()
        obj.data.materials.append(mat_naranja)
        print(f"[ZULY] Color aplicado a: {obj.name}")
        encontrado = True
        break

if not encontrado:
    print("[ZULY] No se encontro el agujero, buscando cilindro...")
    for obj in bpy.context.scene.objects:
        if obj.type == 'MESH' and obj.name != 'CuboBiselado':
            obj.data.materials.clear()
            obj.data.materials.append(mat_naranja)
            print(f"[ZULY] Color aplicado a: {obj.name}")
            break

# GUARDAR
bpy.ops.wm.save_mainfile(filepath=filepath)

print("[ZULY] Archivo guardado - Recarga en Blender para ver color")
"""

with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
    f.write(code)
    temp_path = Path(f.name)

try:
    print("[ZULY TRABAJANDO] Abriendo y aplicando color...")
    cmd = [str(BLENDER_PATH), "--background", "--python", str(temp_path)]
    result = subprocess.run(cmd, timeout=30)
    print("✅ [ZULY OK] Color al agujero aplicado - Recarga en Blender (F5)")
    
except Exception as e:
    print(f"[ERROR] {e}")
finally:
    if temp_path.exists():
        temp_path.unlink()
