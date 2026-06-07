#!/usr/bin/env python3
"""
ZULY: Desactivar backups .blend1
Ejecutar UNA VEZ para configurar Blender
"""

import subprocess
import tempfile
from pathlib import Path

BLENDER_PATH = Path(r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe")

disable_backups = """
import bpy

# Desactivar creación de .blend1
bpy.context.preferences.filepaths.save_version = 0

# Guardar preferencias
bpy.ops.wm.save_userpref()

print("\\n✅ Backups .blend1 DESACTIVADOS")
print("   save_version = 0")
"""

print("\n" + "="*60)
print("🔧 Configurando Blender: DESACTIVAR .blend1")
print("="*60)

with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
    f.write(disable_backups)
    script_file = Path(f.name)

try:
    cmd = [str(BLENDER_PATH), "--background", "--python", str(script_file)]
    subprocess.run(cmd, timeout=30)
    print("\n✓ Preferencias actualizadas")
finally:
    if script_file.exists():
        script_file.unlink()

print("\n" + "="*60)
print("✨ LISTO: Ya no habrá .blend1 duplicados")
print("="*60)
