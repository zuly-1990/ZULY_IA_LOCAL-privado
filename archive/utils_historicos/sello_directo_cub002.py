#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔧 FLUJO DIRECTO - Validar + Sellar CUB-002 automáticamente
Sin intermediarios, JUES V2 directo
"""

import subprocess
import sys
from pathlib import Path

zuly_path = Path('c:/Users/Admin/Desktop/ZULY_IA_LOCAL')

script_directo = '''
import sys
sys.path.insert(0, 'c:/Users/Admin/Desktop/ZULY_IA_LOCAL/core')
from jues_bot_v2 import jues_bot_validar_y_sellar

print("="*70)
print("🎮 DEMOSTRACIÓN - SELLO AUTOMÁTICO CUB-002 (V2 DIRECTO)")
print("="*70)

# Ejecutar JUES-BOT V2 con aprobación automática
resultado = jues_bot_validar_y_sellar(
    "./archivo_zuly/temp_arena/CUB-002_Transform_PivoteSuelo.blend",
    "CUB-002_Transform_PivoteSuelo",
    "#4CAF50",
    aprobar=True
)

print("\\n" + "="*70)
print("📊 RESULTADO FINAL")
print("="*70)
print(f"🎯 Patrón: CUB-002_Transform_PivoteSuelo")
print(f"🏛️ Dictamen: {resultado.get('dictamen', 'N/A')}")
print(f"⚠️ Errores: {resultado.get('errores', 0)}")
print(f"⚠️ Advertencias: {resultado.get('advertencias', 0)}")

if resultado.get('sellado'):
    print(f"🏆 SELLO: {resultado['sellado'].get('status', 'N/A')}")
    print(f"📁 Ubicación: {resultado['sellado'].get('ubicacion', 'N/A')}")
    print("\\n✅ SELLO APLICADO AUTOMÁTICAMENTE")
else:
    print("\\n❌ No se aplicó sello - Revisar dictamen")

print("="*70)
'''

script_path = zuly_path / 'temp_sello_directo.py'
with open(script_path, 'w', encoding='utf-8') as f:
    f.write(script_directo)

blender_exe = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe"

print("🔧 Ejecutando sello directo CUB-002...")
result = subprocess.run(
    [str(blender_exe), '--background', '--python', str(script_path)],
    capture_output=True,
    text=True,
    encoding='utf-8',
    errors='ignore',
    cwd=str(zuly_path)
)

if result.stdout:
    print(result.stdout[-2500:] if len(result.stdout) > 2500 else result.stdout)
if result.stderr:
    print(f"Stderr: {result.stderr[-500:]}")

script_path.unlink()

print("\n✅ Proceso completado")
