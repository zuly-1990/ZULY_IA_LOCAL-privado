#!/usr/bin/env python3
"""
Cambiar color del agujero a NARANJA BRILLANTE
ZULY ejecuta esta operacion
"""

import subprocess
import tempfile
from pathlib import Path

BLENDER_PATH = Path(r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe")
BLEND_FILE = Path(r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\ZULY_PROJECTS\cubo_biselado.blend")

code = """
import bpy

# CARGAR BLEND
bpy.ops.wm.open_mainfile(filepath=r'C:\\Users\\Admin\\Desktop\\ZULY_IA_LOCAL\\ZULY_PROJECTS\\cubo_biselado.blend')

print("[ZULY] Modificando color del agujero...")

# BUSCAR MATERIAL "ColorAgujero"
mat = bpy.data.materials.get("ColorAgujero")
if mat:
    mat.use_nodes = True
    # CAMBIAR A NARANJA BRILLANTE
    mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (1.0, 0.5, 0.0, 1.0)  # Naranja
    mat.node_tree.nodes["Principled BSDF"].inputs[9].default_value = 0.1  # Menos rough (mas brillante)
    print("[ZULY] ✓ Material naranja aplicado")
else:
    print("[ZULY] Material no encontrado, creando nuevo...")
    mat_nuevo = bpy.data.materials.new(name="ColorAgujero")
    mat_nuevo.use_nodes = True
    mat_nuevo.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (1.0, 0.5, 0.0, 1.0)
    mat_nuevo.node_tree.nodes["Principled BSDF"].inputs[9].default_value = 0.1
    
    # APLICAR AL CILINDRO AGUJERO
    for obj in bpy.context.scene.objects:
        if "Agujero" in obj.name:
            obj.data.materials.append(mat_nuevo)
    print("[ZULY] ✓ Material naranja creado y aplicado")

# GUARDAR
bpy.ops.wm.save_mainfile()
print("[ZULY] ✓ Cambios guardados")
print("[LISTO] Recarga en Blender para ver el agujero NARANJA BRILLANTE")
"""

with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
    f.write(code)
    temp_path = Path(f.name)

try:
    print("[ZULY EJECUTANDO] Cambiar color del agujero a naranja brillante...")
    cmd = [str(BLENDER_PATH), "--background", "--python", str(temp_path)]
    result = subprocess.run(cmd, timeout=30)
    print("✅ ZULY completo - Recarga en Blender (File > Reload)")
    
except Exception as e:
    print(f"[ERROR] {e}")
finally:
    if temp_path.exists():
        temp_path.unlink()
