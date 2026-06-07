#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔧 SELLO AUTOMÁTICO CUB-003
"""

import subprocess
import sys
from pathlib import Path

zuly_path = Path('c:/Users/Admin/Desktop/ZULY_IA_LOCAL')

script_sello = '''
import sys
sys.path.insert(0, 'c:/Users/Admin/Desktop/ZULY_IA_LOCAL/core')
from jues_bot_v2 import jues_bot_validar_y_sellar

print("="*70)
print("🎮 SELLO AUTOMÁTICO - CUB-003 (MuroPro)")
print("="*70)

resultado = jues_bot_validar_y_sellar(
    "./archivo_zuly/temp_arena/CUB-003_Modelado_MuroPro.blend",
    "CUB-003_Modelado_MuroPro",
    "#8C8C8C",
    aprobar=True
)

print("\\n" + "="*70)
print("📊 RESULTADO")
print("="*70)
print(f"🎯 CUB-003_Modelado_MuroPro")
print(f"🏛️ Dictamen: {resultado.get('dictamen', 'N/A')}")
print(f"⚠️ Errores: {resultado.get('errores', 0)}")

if resultado.get('sellado'):
    print(f"🏆 SELLO: {resultado['sellado'].get('status', 'N/A')}")
    print(f"📁 Ubicación: {resultado['sellado'].get('ubicacion', 'N/A')}")
    print("\\n✅ CUB-003 SELLADO AUTOMÁTICAMENTE")
else:
    print("\\n❌ No se aplicó sello")

print("="*70)
'''

script_path = zuly_path / 'temp_sello_cub003.py'
with open(script_path, 'w', encoding='utf-8') as f:
    f.write(script_sello)

blender_exe = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe"

print("🔧 Sello automático CUB-003...")
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

print("\n✅ CUB-003 completado")
