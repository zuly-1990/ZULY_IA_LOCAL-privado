#!/usr/bin/env python3
"""
Script para lanzar Blender REAL y dejar archivo .blend para revisión
"""

import subprocess
import sys
import tempfile
from pathlib import Path

BLENDER_PATH = Path(r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe")
ZULY_ROOT = Path(r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL")
OUTPUT_BLEND = ZULY_ROOT / "ZULY_PROJECTS" / "prueba_usuario_20260330.blend"

# Script Python a ejecutar en Blender
blender_script = """
import sys
sys.path.insert(0, r'C:\\Users\\Admin\\Desktop\\ZULY_IA_LOCAL')

print("\\n" + "="*70)
print("👤 SCRIPT BLENDER REAL - Crear archivo para revisión")
print("="*70)

from core.agent import Agent

# Inicializar con BLENDER REAL
print("\\n⏳ Inicializando ZULY con Blender Real...")
agent = Agent(force_mock=False)

print("\\n📢 Petición: Crear un cubo")
result = agent.process_natural_request("Crear un cubo")
print(f"✓ Resultado: {result.get('success')}")

# Guardar archivo
print("\\n💾 Guardando archivo...")
import bpy
output_file = r'C:\\Users\\Admin\\Desktop\\ZULY_IA_LOCAL\\ZULY_PROJECTS\\prueba_usuario_20260330.blend'
bpy.ops.wm.save_as_mainfile(filepath=output_file)
print(f"✅ Guardado: {output_file}")

print("\\nArchivo listo para revisión en:")
print(f"  {output_file}")
print("\\n" + "="*70)
"""

# Crear archivo temporal
with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
    f.write(blender_script)
    temp_script = Path(f.name)

try:
    print("\n" + "="*70)
    print("🚀 Lanzando Blender REAL para generar archivo .blend")
    print("="*70)
    print(f"\nEjectable: {BLENDER_PATH}")
    print(f"Output: {OUTPUT_BLEND}\n")
    
    # Lanzar Blender
    cmd = [
        str(BLENDER_PATH),
        "--background",
        "--python", str(temp_script)
    ]
    
    result = subprocess.run(cmd, capture_output=False, text=True)
    
    if OUTPUT_BLEND.exists():
        size_mb = OUTPUT_BLEND.stat().st_size / (1024*1024)
        print(f"\n✅ ARCHIVO CREADO:")
        print(f"   Ruta: {OUTPUT_BLEND}")
        print(f"   Tamaño: {size_mb:.2f} MB")
        print(f"\n👉 Abre el archivo y da tu 'Visto Bueno'")
    else:
        print(f"\n⚠️  Archivo no encontrado: {OUTPUT_BLEND}")
    
finally:
    # Limpiar
    if temp_script.exists():
        temp_script.unlink()
