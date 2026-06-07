#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔧 SELLO JUES V3 - Ejecutar a través de Blender
"""

import subprocess
from pathlib import Path

zuly_path = Path('c:/Users/Admin/Desktop/ZULY_IA_LOCAL')

# Script que se ejecutará dentro de Blender
script_blender = '''
import sys
sys.path.insert(0, 'c:/Users/Admin/Desktop/ZULY_IA_LOCAL/core')
from jues_bot_v3 import jues_bot_v3_validar_y_sellar

modelos = [
    ("MOD-001_Pabellon_Minimalista", "#C0C0C0"),
    ("MOD-002_Torre_Corporativa", "#A0A0A0"),
    ("MOD-003_Casa_Contenedor", "#B8B0A0"),
    ("MOD-004_Museo_Arte", "#E8E8E8"),
    ("MOD-005_Estacion_Espacial", "#9090A0"),
]

print("\\n" + "="*70)
print("🔧 JUES V3 - Validando 5 modelos complejos")
print("="*70)

for nombre, color in modelos:
    print(f"\\n🎯 {nombre}")
    print("-" * 50)
    
    resultado = jues_bot_v3_validar_y_sellar(
        f"./archivo_zuly/temp_arena/{nombre}.blend",
        nombre,
        color,
        aprobar=True
    )
    
    print(f"⭐ Puntuacion: {resultado.get('puntuacion', 0)}/100")
    print(f"📋 Dictamen: {resultado.get('dictamen', 'N/A')}")
    
    if resultado.get('sellado'):
        print(f"🏆 SELLO: {resultado['sellado'].get('status', 'N/A')}")
    else:
        print("⚠️ Sin sello - Puntuacion insuficiente")

print("\\n" + "="*70)
print("✅ VALIDACION COMPLETADA")
print("="*70)
'''

# Guardar script temporal
script_path = zuly_path / 'temp_jues_v3_sello.py'
with open(script_path, 'w', encoding='utf-8') as f:
    f.write(script_blender)

# Ejecutar a través de Blender
blender_exe = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe"

print("🔧 Ejecutando JUES V3 a través de Blender...")
print("⏱️ Esto tomará 3-4 minutos para 5 modelos...")
result = subprocess.run(
    [str(blender_exe), '--background', '--python', str(script_path)],
    capture_output=True, text=True, encoding='utf-8', errors='ignore',
    cwd=str(zuly_path)
)

# Mostrar salida
if result.stdout:
    print(result.stdout[-4000:] if len(result.stdout) > 4000 else result.stdout)

if result.stderr:
    errores = [line for line in result.stderr.split('\n') if 'Error' in line or 'Traceback' in line]
    if errores:
        print("\n⚠️ Errores detectados:")
        for e in errores[:5]:
            print(f"   {e}")

# Limpiar
script_path.unlink()
print("\n✅ Proceso JUES V3 completado")
