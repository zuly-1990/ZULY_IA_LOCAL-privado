#!/usr/bin/env python3
"""
Renderizar Cubo Biselado - RAPIDO
64 samples, 1920x1080
"""

import subprocess
import tempfile
from pathlib import Path

BLENDER_PATH = Path(r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe")
BLEND_INPUT = Path(r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\ZULY_PROJECTS\cubo_biselado.blend")
OUTPUT_PNG = Path(r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\export\cubo_biselado_render.png")

code = """
import bpy

# CARGAR ESCENA
bpy.ops.wm.open_mainfile(filepath=r'C:\\Users\\Admin\\Desktop\\ZULY_IA_LOCAL\\ZULY_PROJECTS\\cubo_biselado.blend')

# CONFIGURAR RENDER
scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.render.samples = 64
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.filepath = r'C:\\Users\\Admin\\Desktop\\ZULY_IA_LOCAL\\export\\cubo_biselado_render.png'

# CREAR LUZ (key light)
bpy.ops.object.light_add(type='SUN', location=(5, 5, 10))
luz = bpy.context.active_object
luz.data.energy = 2.0
luz.data.angle = 0.5

# CREAR CAMARA
bpy.ops.object.camera_add(location=(5, -5, 3))
camara = bpy.context.active_object
camara.rotation_euler = (1.1, 0, 0.785)
scene.camera = camara

print("[OK] Configuracion lista")
print("[RENDER] Iniciando render 64 samples...")

# RENDER
bpy.ops.render.render(write_still=True)

print("[OK] Render completado")
print("[OK] Imagen: C:\\\\Users\\\\Admin\\\\Desktop\\\\ZULY_IA_LOCAL\\\\export\\\\cubo_biselado_render.png")
"""

with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
    f.write(code)
    temp_path = Path(f.name)

try:
    print("Renderizando cubo biselado (64 samples)...")
    cmd = [str(BLENDER_PATH), "--background", "--python", str(temp_path)]
    result = subprocess.run(cmd, timeout=600)
    
    if OUTPUT_PNG.exists():
        size = OUTPUT_PNG.stat().st_size / 1024 / 1024
        print(f"✅ Render completado: {OUTPUT_PNG.name}")
        print(f"   Tamanio: {size:.2f} MB")
    else:
        print("[ERROR] PNG no creado")
    
except subprocess.TimeoutExpired:
    print("[ERROR] Timeout en render")
except Exception as e:
    print(f"[ERROR] {e}")
finally:
    if temp_path.exists():
        temp_path.unlink()
