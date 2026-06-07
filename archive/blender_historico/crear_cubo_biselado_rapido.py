#!/usr/bin/env python3
"""
Cubo Biselado - ULTRA RAPIDO
Solo: bevel + smooth shading
"""

import subprocess
import tempfile
from pathlib import Path

BLENDER_PATH = Path(r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe")
OUTPUT = Path(r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\ZULY_PROJECTS\cubo_biselado.blend")

code = """
import bpy

# LIMPIAR
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# CREAR CUBO
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))
cubo = bpy.context.active_object
cubo.name = "CuboBiselado"

# SUAVIZAR (SMOOTH SHADING)
bpy.context.view_layer.objects.active = cubo
cubo.select_set(True)
bpy.ops.object.shade_smooth()

# BEVEL MODIFIER (aristas y vertices)
bevel = cubo.modifiers.new(name="Bevel", type='BEVEL')
bevel.width = 0.2
bevel.segments = 2
bevel.affect = 'EDGES'

print("[OK] Cubo creado con bevel + smooth")

# GUARDAR
output_path = r'C:\\Users\\Admin\\Desktop\\ZULY_IA_LOCAL\\ZULY_PROJECTS\\cubo_biselado.blend'
bpy.ops.wm.save_as_mainfile(filepath=output_path)

print("[OK] Guardado")
"""

with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
    f.write(code)
    temp_path = Path(f.name)

try:
    print("Creando cubo biselado... ")
    cmd = [str(BLENDER_PATH), "--background", "--python", str(temp_path)]
    result = subprocess.run(cmd, timeout=30)
    
    if OUTPUT.exists():
        size = OUTPUT.stat().st_size / 1024
        print(f"✅ Archivo: {OUTPUT.name}")
        print(f"   Tamanio: {size:.1f} KB")
    else:
        print("[ERROR] Archivo no creado")
    
except Exception as e:
    print(f"[ERROR] {e}")
finally:
    if temp_path.exists():
        temp_path.unlink()
