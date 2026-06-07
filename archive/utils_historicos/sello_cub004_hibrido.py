#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔧 SELLO AUTOMÁTICO CUB-004-HIBRIDO
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
print("🧪 SELLO AUTOMÁTICO - CUB-004-HIBRIDO")
print("="*70)

resultado = jues_bot_validar_y_sellar(
    "./archivo_zuly/temp_arena/CUB-004-HIBRIDO_Prueba.blend",
    "CUB-004-HIBRIDO_Prueba",
    "#607D8B",
    aprobar=True
)

print("\\n" + "="*70)
print("📊 RESULTADO")
print("="*70)
print(f"🎯 CUB-004-HIBRIDO_Prueba")
print(f"🏛️ Dictamen: {resultado.get('dictamen', 'N/A')}")

if resultado.get('sellado'):
    print(f"🏆 SELLO: {resultado['sellado'].get('status', 'N/A')}")
    print("\\n✅ PATRÓN HÍBRIDO SELLADO")
else:
    print("\\n❌ No se aplicó sello")

print("="*70)
'''

script_path = zuly_path / 'temp_sello_hibrido.py'
with open(script_path, 'w', encoding='utf-8') as f:
    f.write(script_sello)

blender_exe = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe"

print("🔧 Sello automático CUB-004-HIBRIDO...")
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

print("\n✅ CUB-004-HIBRIDO completado")
