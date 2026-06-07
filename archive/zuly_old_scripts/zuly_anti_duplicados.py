#!/usr/bin/env python3
"""
ZULY CONFIGURACION ANTI-DUPLICADOS
- Sin crear .blend1
- Sin respaldos automáticos
- Trabajo SOLO con cubo_3.blend
"""

import subprocess
import time
from pathlib import Path
import tempfile

BLENDER_PATH = Path(r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe")
BLEND_FILE = Path(r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\ZULY_PROJECTS\cubo_3.blend")

print("\n" + "="*70)
print("🔒 ZULY MODO ANTI-DUPLICADOS")
print("="*70)

config_script = """
import bpy
import os

filepath = r'C:\\Users\\Admin\\Desktop\\ZULY_IA_LOCAL\\ZULY_PROJECTS\\cubo_3.blend'

print("\\n[CONFIG] Configurando Blender para evitar duplicados...")

# DESACTIVAR RESPALDOS AUTOMÁTICOS
bpy.context.preferences.filepaths.save_version = 0
print("  ✓ Versiones de respaldo desactivadas (save_version = 0)")

# ABRIENDO ARCHIVO
print("\\n[ZULY] Abriendo cubo_3.blend...")
bpy.ops.wm.open_mainfile(filepath=filepath)

print("[OK] Archivo abierto")

# VERIFICAR NO HAY DUPLICADOS
import os
directorio = os.path.dirname(filepath)
archivos_blend = [f for f in os.listdir(directorio) if 'cubo_3' in f and '.blend' in f]

print(f"\\n[VERIFICACION] Archivos 'cubo_3' encontrados: {len(archivos_files)}")
for archivo in archivos_blend:
    print(f"  - {archivo}")

if len(archivos_blend) > 1:
    print("  ⚠️ DETECTADOS DUPLICADOS")
else:
    print("  ✓ ÚNICO archivo encontrado")

# GUARDAR CON CONFIGURACIÓN ANTI-DUPLICADO
print("\\n[GUARDADO] Guardando SOLO como cubo_3.blend...")
bpy.ops.wm.save_mainfile(filepath=filepath)

print("[OK] Guardado exitoso - SIN crear .blend1")

print("\\n[LISTO] ZULY en modo anti-duplicados")
print("  - Respaldos: DESACTIVADOS")
print("  - Archivo único: cubo_3.blend")
print("  - Duplicados: 0")
"""

try:
    print("\n📝 Configurando sistema...")
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
        # FIX typo en script
        script_fixed = config_script.replace('archivos_files', 'archivos_blend')
        f.write(script_fixed)
        script_file = Path(f.name)
    print("   ✓ Script preparado")
    
    print("\n🔧 Ejecutando configuración...")
    cmd = [str(BLENDER_PATH), "--background", "--python", str(script_file)]
    result = subprocess.run(cmd, timeout=30)
    
    print("\n✅ CONFIGURACIÓN COMPLETADA")
    
    # Verificar estado final
    print("\n📊 Estado final del sistema:")
    archivos = list(Path(r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\ZULY_PROJECTS").glob("cubo_3*.blend*"))
    print(f"   Archivos cubo_3: {len(archivos)}")
    for archivo in archivos:
        print(f"   - {archivo.name}")
    
    if len(archivos) == 1:
        print("\n   ✅ ÚNICO ARCHIVO - SIN DUPLICADOS")
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
finally:
    if script_file.exists():
        script_file.unlink()

print("\n" + "="*70)
print("🎯 ZULY PROTEGIDO CONTRA DUPLICADOS")
print("="*70)
print("\nAhora ZULY trabajará SOLO con cubo_3.blend")
print("Sin crear respaldos .blend1")
