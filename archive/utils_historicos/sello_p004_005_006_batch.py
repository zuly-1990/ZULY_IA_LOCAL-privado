#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔧 SELLO BATCH - P-004/005/006 (5 objetos)
"""

import subprocess
from pathlib import Path

zuly_path = Path('c:/Users/Admin/Desktop/ZULY_IA_LOCAL')

patrones = [
    ("P-004A_CilindroAlto", "#795548"),
    ("P-004B_CilindroAncho", "#607D8B"),
    ("P-005A_ConoAlto", "#FF9800"),
    ("P-005B_ConoChato", "#9C27B0"),
    ("P-006A_PlanoBase", "#E5E5E5"),  # Gris claro
]

print("🔧 Sello automático P-004/005/006 BATCH (5 objetos)...")

for nombre, color in patrones:
    script_sello = f'''
import sys
sys.path.insert(0, 'c:/Users/Admin/Desktop/ZULY_IA_LOCAL/core')
from jues_bot_v2 import jues_bot_validar_y_sellar

resultado = jues_bot_validar_y_sellar(
    "./archivo_zuly/temp_arena/{nombre}.blend",
    "{nombre}",
    "{color}",
    aprobar=True
)

print(f"🎯 {nombre}")
print(f"Dictamen: {{resultado.get('dictamen', 'N/A')}}")
if resultado.get('sellado'):
    print(f"🏆 SELLO: {{resultado['sellado'].get('status', 'N/A')}}")
'''
    
    script_path = zuly_path / 'temp_sello.py'
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(script_sello)
    
    blender_exe = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe"
    
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

print("\n✅ P-004/005/006 BATCH sellado (5 objetos)")
