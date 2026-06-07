#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🤖 JUES-BOT VALIDACIÓN - CUB-001 CORREGIDO
Validación técnica post-corrección de color
"""

import subprocess
import sys
from pathlib import Path

zuly_path = Path('c:/Users/Admin/Desktop/ZULY_IA_LOCAL')

script_jues = '''
import sys
sys.path.insert(0, 'c:/Users/Admin/Desktop/ZULY_IA_LOCAL/core')
from jues_bot_validator import JuesBotValidator

print("="*60)
print("🤖 JUES-BOT: Validando CUB-001 CORREGIDO")
print("="*60)

blend_path = './archivo_zuly/temp_arena/CUB-001_Modelado_BiselRealista.blend'
candidato_id = 'CUB-001_Modelado_BiselRealista'
target_color = '#1A4DCC'

# Ejecutar validación completa
jues = JuesBotValidator(blend_path, candidato_id, target_color)
resultado = jues.ejecutar_inspeccion_completa()

# Guardar reporte
report_path = jues.guardar_reporte()
print(f"📄 Reporte guardado: {report_path}")

# Resumen para decisión
print("\\n" + "="*60)
print("🎯 RESUMEN PARA DECISIÓN DEL SOBERANO")
print("="*60)
print(f"Patrón: {candidato_id}")
print(f"Dictamen: {resultado['dictamen']}")
print(f"Errores: {resultado.get('errores', 0)}")
print(f"Advertencias: {resultado.get('advertencias', 0)}")

if resultado['dictamen'] == '✅ APTO_PARA_SELLO':
    print("\\n✅ LISTO PARA SELLO DEL SOBERANO")
    print("   Acción recomendada: [S] SELLO → Mover a mastered/")
else:
    print("\\n⚠️  REQUIERE ATENCIÓN")
    print("   Revisar dashboard arriba para detalles")

print("="*60)
'''

script_path = zuly_path / 'temp_validar_cub001_jues.py'
with open(script_path, 'w', encoding='utf-8') as f:
    f.write(script_jues)

blender_exe = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe"

print("🤖 Ejecutando JUES-BOT validación...")
result = subprocess.run(
    [blender_exe, '--background', '--python', str(script_path)],
    capture_output=True,
    text=True,
    encoding='utf-8',
    errors='ignore',
    cwd=str(zuly_path)
)

if result.stdout:
    print(result.stdout[-2500:] if len(result.stdout) > 2500 else result.stdout)
if result.stderr and "Error" in result.stderr:
    print(f"⚠️  Errores: {result.stderr[-300:]}")

script_path.unlink()

print("\n✅ Validación JUES-BOT completada")
