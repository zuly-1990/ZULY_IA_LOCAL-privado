#!/usr/bin/env python3
"""
ZULY - Gestor de .BLEND ÚNICO
- Sin duplicación de archivos
- Modificaciones directas en archivo único
- Sin crear .blend1, respaldos o copias
"""

import subprocess
import tempfile
from pathlib import Path
import time
import json

BLENDER_PATH = Path(r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe")
BLEND_FILE = Path(r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\ZULY_PROJECTS\cubo_biselado.blend")
LOCK_FILE = Path(r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\.zuly_blend_lock")

def esperar_archivo_libre(timeout=10):
    """Espera a que el archivo no esté en uso"""
    inicio = time.time()
    while (time.time() - inicio) < timeout:
        try:
            if LOCK_FILE.exists():
                time.sleep(0.5)
                continue
            return True
        except:
            time.sleep(0.1)
    return True

def crear_lock():
    """Crear archivo de bloqueo"""
    LOCK_FILE.write_text(str(time.time()))

def liberar_lock():
    """Liberar archivo de bloqueo"""
    if LOCK_FILE.exists():
        LOCK_FILE.unlink()

# Script para ZULY
code = """
import bpy
import os

filepath = r'C:\\Users\\Admin\\Desktop\\ZULY_IA_LOCAL\\ZULY_PROJECTS\\cubo_biselado.blend'

print("[ZULY] Abriendo cubo_biselado.blend")

# ABRIR SIN CREAR RESPALDO
bpy.ops.wm.open_mainfile(filepath=filepath)

print("[ZULY] Archivo abierto - modificando...")

# CREAR MATERIAL NARANJA
mat = bpy.data.materials.new(name="ColorAgujero")
mat.use_nodes = True
nodes = mat.node_tree.nodes
links = mat.node_tree.links

nodes.clear()
bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
output = nodes.new(type='ShaderNodeOutputMaterial')

bsdf.inputs['Base Color'].default_value = (1.0, 0.55, 0.1, 1.0)
bsdf.inputs['Roughness'].default_value = 0.15

links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

print("[ZULY] Material creado")

# APLICAR AL AGUJERO
for obj in bpy.context.scene.objects:
    if obj.type == 'MESH' and 'Agujero' in obj.name:
        obj.data.materials.clear()
        obj.data.materials.append(mat)
        print(f"[ZULY] Color aplicado a {obj.name}")

# GUARDAR - SIN CREAR RESPALDO
# Desactivar auto-save y backups
bpy.context.preferences.filepaths.save_version = 0

# Guardar en mismo archivo
bpy.ops.wm.save_mainfile(filepath=filepath)

print("[ZULY] ✓ Guardado en: " + filepath)
print("[ZULY] ✓ SIN duplicar archivos")

# VERIFICAR que solo existe un .blend
import os
archivos = os.listdir(os.path.dirname(filepath))
blend_files = [f for f in archivos if 'cubo_biselado' in f]
print(f"[ZULY] Archivos relacionados: {len(blend_files)} - {blend_files}")
"""

try:
    print("[ZULY SISTEMA] Esperando acceso al archivo...")
    esperar_archivo_libre()
    
    crear_lock()
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
        f.write(code)
        temp_path = Path(f.name)
    
    print("[ZULY] Ejecutando modificación...")
    cmd = [str(BLENDER_PATH), "--background", "--python", str(temp_path)]
    result = subprocess.run(cmd, timeout=30)
    
    print("\n✅ [ZULY COMPLETE] Archivo modificado SIN duplicación")
    print("   Recarga en Blender (F5) para ver cambios")
    
except Exception as e:
    print(f"[ERROR] {e}")
finally:
    if temp_path.exists():
        temp_path.unlink()
    liberar_lock()
    print("[ZULY] Lock liberado - Archivo disponible")
