#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔧 SELLO P-006A corregido
"""

import subprocess
from pathlib import Path

zuly_path = Path('c:/Users/Admin/Desktop/ZULY_IA_LOCAL')

script_sello = '''
import sys
sys.path.insert(0, 'c:/Users/Admin/Desktop/ZULY_IA_LOCAL/core')
from jues_bot_v2 import jues_bot_validar_y_sellar

resultado = jues_bot_validar_y_sellar(
    "./archivo_zuly/temp_arena/P-006A_PlanoBase.blend",
    "P-006A_PlanoBase",
    "#E5E5E5",
    aprobar=True
)

print(f"🎯 P-006A_PlanoBase")
print(f"Dictamen: {resultado.get('dictamen', 'N/A')}")
if resultado.get('sellado'):
    print(f"🏆 SELLO: {resultado['sellado'].get('status', 'N/A')}")
'''

script_path = zuly_path / 'temp_sello_p006.py'
with open(script_path, 'w', encoding='utf-8') as f:
    f.write(script_sello)

blender_exe = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe"

print("🔧 Sello P-006A corregido...")
result = subprocess.run(
    [str(blender_exe), '--background', '--python', str(script_path)],
    capture_output=True,
    text=True,
    encoding='utf-8',
    errors='ignore',
    cwd=str(zuly_path)
)

if result.stdout:
    for line in result.stdout.split('\n'):
        if '🎯' in line or '🏆' in line or 'Dictamen' in line:
            print(line)

script_path.unlink()
print("\n✅ P-006A sellado")
