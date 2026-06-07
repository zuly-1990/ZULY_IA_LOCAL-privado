#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 AUDITORÍA COMPLETA - 5 MODELOS COMBINADOS CON JUES-BOT UNIFICADO
Fecha: 2026-04-05
"""

import subprocess
import sys
from pathlib import Path

zuly_path = Path('c:/Users/Admin/Desktop/ZULY_IA_LOCAL')
arena_path = zuly_path / 'archivo_zuly/temp_arena'

# 5 modelos a auditar
modelos = [
    ("MOD-001_Pabellon_Minimalista.blend", "#B0B0B0"),  # Gris claro
    ("MOD-002_Torre_Corporativa.blend", "#B0B0B0"),     # Metal
    ("MOD-003_Casa_Contenedor.blend", "#B0B0B0"),      # Industrial
    ("MOD-004_Museo_Arte.blend", "#99AACC"),           # Azul grisáceo
    ("MOD-005_Estacion_Espacial.blend", "#99AACC"),    # Espacial
]

print("=" * 70)
print("🚀 AUDITORÍA JUES-BOT - 5 MODELOS COMBINADOS")
print("=" * 70)

resultados = []

for blend_file, color in modelos:
    blend_path = arena_path / blend_file
    model_id = blend_file.replace('.blend', '')
    
    print(f"\n{'='*70}")
    print(f"🔍 Auditando: {model_id}")
    print(f"{'='*70}")
    
    if not blend_path.exists():
        print(f"❌ Archivo no encontrado: {blend_path}")
        continue
    
    # Script para Blender que ejecuta JUES-BOT
    script = f'''
import sys
sys.path.insert(0, "c:/Users/Admin/Desktop/ZULY_IA_LOCAL")
sys.path.insert(0, "c:/Users/Admin/Desktop/ZULY_IA_LOCAL/core")

from core.jues_bot import jues_bot_validar_y_sellar

resultado = jues_bot_validar_y_sellar(
    blend_path="{blend_path}",
    candidato_id="{model_id}",
    target_color="{color}",
    aprobar=False
)

print("\\n" + "="*70)
print("📊 RESULTADO AUDITORÍA")
print("="*70)
print(f"Modelo: {{resultado.get('candidato_id', 'N/A')}}")
print(f"Score: {{resultado.get('score', 0)}}/100")
print(f"Dictamen: {{resultado.get('dictamen', 'N/A')}}")
print(f"Sellado: {{resultado.get('sellado', False)}}")

if 'superpoderes' in resultado:
    print("\\n🔍 Superpoderes:")
    for sp_name, sp_data in resultado['superpoderes'].items():
        status = sp_data.get('status', 'N/A')
        icon = sp_data.get('icon', '')
        print(f"  {{icon}} {{sp_name}}: {{status}}")
        
print("\\n" + "="*70)
'''
    
    # Guardar y ejecutar
    temp_script = zuly_path / f'audit_{model_id}.py'
    with open(temp_script, 'w', encoding='utf-8') as f:
        f.write(script)
    
    blender_exe = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe"
    
    result = subprocess.run(
        [str(blender_exe), '--background', '--python', str(temp_script)],
        capture_output=True, text=True, encoding='utf-8', errors='ignore',
        cwd=str(zuly_path)
    )
    
    # Mostrar salida
    if result.stdout:
        lines = result.stdout.split('\n')
        for line in lines:
            if 'RESULTADO' in line or 'Score' in line or 'Dictamen' in line or '✓' in line or '✅' in line or '🚨' in line:
                print(line)
    
    temp_script.unlink()
    
    print(f"\n✅ Auditoría {model_id} completada")

print("\n" + "=" * 70)
print("🎉 AUDITORÍA COMPLETA FINALIZADA")
print("=" * 70)
print("\n5 modelos auditados con JUES-BOT unificado")
print("Revisa los reportes JSON generados para detalles completos")
