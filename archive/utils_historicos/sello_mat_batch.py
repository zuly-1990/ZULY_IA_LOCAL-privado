#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔧 SELLO BATCH - FASE 2 (3 materiales)
"""

import subprocess
from pathlib import Path

zuly_path = Path('c:/Users/Admin/Desktop/ZULY_IA_LOCAL')

patrones = [
    ("MAT-001_Material_Metal", "#F2F2F7"),  # Plateado
    ("MAT-002_Material_Vidrio", "#FFFFFF"),  # Blanco transparente
    ("MAT-003_Material_Emisivo", "#FF6B35"), # Naranja
]

print("🔧 Sello automático FASE 2 (3 materiales)...")

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

print("\n✅ FASE 2 sellada (3 materiales)")
