#!/usr/bin/env python3
"""
ZULY TRABAJA CON UN SOLO .BLEND
- Sin crear nuevos archivos
- Solo modifica el mismo
- Hasta nueva orden
"""

import subprocess
import tempfile
from pathlib import Path

BLENDER_PATH = Path(r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe")
BLEND_FILE = Path(r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\ZULY_PROJECTS\cubo_biselado.blend")

code = """
import bpy

# CARGAR archivo UNO SOLO
filepath = r'C:\\Users\\Admin\\Desktop\\ZULY_IA_LOCAL\\ZULY_PROJECTS\\cubo_biselado.blend'
bpy.ops.wm.open_mainfile(filepath=filepath)

print("[ZULY] Trabajando con: cubo_biselado.blend")

# LIMPIAR MATERIALS PREVIOS
for mat in bpy.data.materials:
    if "Color" in mat.name or "Agujero" in mat.name:
        bpy.data.materials.remove(mat)

print("[ZULY] Limpiados materiales previos")

# CREAR MATERIAL BLANCO (cubo)
mat_blanco = bpy.data.materials.new(name="MaterialBlanco")
mat_blanco.use_nodes = True
nodes = mat_blanco.node_tree.nodes
links = mat_blanco.node_tree.links

# Limpiar nodos default
nodes.clear()

# Crear nodos
bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
output = nodes.new(type='ShaderNodeOutputMaterial')

# Configurar color blanco
bsdf.inputs['Base Color'].default_value = (1.0, 1.0, 1.0, 1.0)
bsdf.inputs['Roughness'].default_value = 0.5

# Conectar
links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

print("[ZULY] Material blanco creado")

# CREAR MATERIAL NARANJA (agujero)
mat_naranja = bpy.data.materials.new(name="MaterialNaranja")
mat_naranja.use_nodes = True
nodes = mat_naranja.node_tree.nodes
links = mat_naranja.node_tree.links

nodes.clear()

bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
output = nodes.new(type='ShaderNodeOutputMaterial')

bsdf.inputs['Base Color'].default_value = (1.0, 0.5, 0.0, 1.0)  # Naranja
bsdf.inputs['Roughness'].default_value = 0.15  # Brillante

links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

print("[ZULY] Material naranja creado")

# APLICAR MATERIALES A OBJETOS
for obj in bpy.context.scene.objects:
    if obj.type == 'MESH':
        obj.data.materials.clear()
        
        if "CuboBiselado" in obj.name:
            obj.data.materials.append(mat_blanco)
            print(f"[ZULY] Material blanco -> {obj.name}")
        
        if "Agujero" in obj.name:
            obj.data.materials.append(mat_naranja)
            print(f"[ZULY] Material naranja -> {obj.name}")

# GUARDAR EN MISMO ARCHIVO (no crear nuevo)
bpy.ops.wm.save_mainfile(filepath=filepath)

print("[ZULY OK] Materiales aplicados al cubo_biselado.blend")
print("[ZULY OK] Recarga en Blender (F5 o File > Reload)")
"""

with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
    f.write(code)
    temp_path = Path(f.name)

try:
    print("[ZULY] Modificando UN SOLO archivo: cubo_biselado.blend")
    cmd = [str(BLENDER_PATH), "--background", "--python", str(temp_path)]
    result = subprocess.run(cmd, timeout=30)
    
    if result.returncode == 0:
        print("✅ [ZULY LISTO] Materiales aplicados correctamente")
        print("   Recarga en Blender para ver cambios (F5)")
    
except Exception as e:
    print(f"[ERROR] {e}")
finally:
    if temp_path.exists():
        temp_path.unlink()
