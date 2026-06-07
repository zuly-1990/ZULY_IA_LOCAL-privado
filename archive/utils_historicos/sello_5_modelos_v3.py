#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔧 SELLO BATCH - 5 Modelos Combinados con JUES V3
"""

import subprocess
from pathlib import Path

zuly_path = Path('c:/Users/Admin/Desktop/ZULY_IA_LOCAL')

# 5 modelos con colores neutros representativos
modelos = [
    ("MOD-001_Pabellon_Minimalista", "#C0C0C0"),  # Gris claro
    ("MOD-002_Torre_Corporativa", "#A0A0A0"),     # Gris medio
    ("MOD-003_Casa_Contenedor", "#B8B0A0"),       # Beige industrial
    ("MOD-004_Museo_Arte", "#E8E8E8"),            # Blanco museo
    ("MOD-005_Estacion_Espacial", "#9090A0"),     # Gris azulado metal
]

print("🔧 Sello automático JUES V3 (5 modelos complejos)...")
print("="*70)

for nombre, color in modelos:
    print(f"\n🎯 {nombre}")
    
    script_sello = f'''
import sys
sys.path.insert(0, 'c:/Users/Admin/Desktop/ZULY_IA_LOCAL/core')
from jues_bot_v3 import jues_bot_v3_validar_y_sellar

resultado = jues_bot_v3_validar_y_sellar(
    "./archivo_zuly/temp_arena/{nombre}.blend",
    "{nombre}",
    "{color}",
    aprobar=True
)

print(f"📊 Puntuacion: {{resultado.get('puntuacion', 0)}}/100")
print(f"Dictamen: {{resultado.get('dictamen', 'N/A')}}")
if resultado.get('sellado'):
    print(f"🏆 SELLO: {{resultado['sellado'].get('status', 'N/A')}}")
'''
    
    script_path = zuly_path / 'temp_sello_v3.py'
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(script_sello)
    
    blender_exe = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe"
    
    result = subprocess.run(
        [str(blender_exe), '--background', '--python', str(script_path)],
        capture_output=True, text=True, encoding='utf-8', errors='ignore',
        cwd=str(zuly_path)
    )
    
    if result.stdout:
        # Filtrar solo líneas importantes
        for line in result.stdout.split('\n'):
            if any(x in line for x in ['Puntuacion', 'Dictamen', '🏆', '📊', 'SELLO', 'APTO', 'NO_APTO']):
                print(f"   {line}")
    
    script_path.unlink()

print("\n" + "="*70)
print("✅ VALIDACIÓN V3 COMPLETADA (5 modelos)")
print("="*70)
