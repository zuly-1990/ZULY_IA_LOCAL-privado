#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎮 DEMOSTRACIÓN - Sellar CUB-002 automáticamente con OK
"""

import subprocess
import sys
from pathlib import Path

zuly_path = Path('c:/Users/Admin/Desktop/ZULY_IA_LOCAL')

# Ejecutar controlador con orden OK
blender_exe = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe"

script_ejecucion = '''
import sys
sys.path.insert(0, 'c:/Users/Admin/Desktop/ZULY_IA_LOCAL/core')
from controlador_zuly_jues import ControladorZulyJues

print("="*70)
print("🎮 DEMOSTRACIÓN - SELLO AUTOMÁTICO CUB-002")
print("="*70)
print("👤 Soberano ordena: OK (Sellar automáticamente)")
print("="*70)

ctrl = ControladorZulyJues()
resultado = ctrl.procesar_orden_soberano(
    "CUB-002_Transform_PivoteSuelo.blend",
    "CUB-002_Transform_PivoteSuelo",
    "#4CAF50",
    "OK"
)

print("\\n" + "="*70)
print("✅ RESULTADO FINAL")
print("="*70)
print(f"🎯 Patrón: {resultado.get('candidato_id', 'N/A')}")
print(f"🏛️ Orden: {resultado.get('orden', 'N/A')}")
print(f"📊 Dictamen: {resultado.get('dictamen', 'N/A')}")
print(f"⚠️ Errores: {resultado.get('errores', 'N/A')}")
print(f"🏆 Sello: {resultado.get('sello', 'N/A')}")
print(f"📁 Ubicación: {resultado.get('ubicacion', 'N/A')}")
'''

script_path = zuly_path / 'temp_demo_sello.py'
with open(script_path, 'w', encoding='utf-8') as f:
    f.write(script_ejecucion)

print("🎮 Ejecutando demostración de sello automático...")
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

script_path.unlink()

print("\n✅ Demostración completada")
