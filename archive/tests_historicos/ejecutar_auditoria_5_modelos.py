#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 AUDITORÍA BATCH - 5 MODELOS COMBINADOS
Ejecuta JUES-BOT en cada modelo y muestra resultados
"""

import subprocess
import json
from pathlib import Path

zuly_path = Path('c:/Users/Admin/Desktop/ZULY_IA_LOCAL')
arena_path = zuly_path / 'archivo_zuly/temp_arena'

modelos = [
    ("MOD-001_Pabellon_Minimalista.blend", "#B0B0B0"),
    ("MOD-002_Torre_Corporativa.blend", "#B0B0B0"),
    ("MOD-003_Casa_Contenedor.blend", "#B0B0B0"),
    ("MOD-004_Museo_Arte.blend", "#99AACC"),
    ("MOD-005_Estacion_Espacial.blend", "#99AACC"),
]

blender_exe = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe"

print("=" * 70)
print("🚀 AUDITORÍA JUES-BOT - 5 MODELOS COMBINADOS")
print("=" * 70)

resultados = []

for blend_file, color in modelos:
    blend_path = arena_path / blend_file
    model_id = blend_file.replace('.blend', '')
    
    print(f"\n{'='*70}")
    print(f"🔍 {model_id}")
    print(f"{'='*70}")
    
    if not blend_path.exists():
        print(f"❌ No encontrado: {blend_path}")
        continue
    
    # Ejecutar auditoría en Blender
    cmd = [
        str(blender_exe), '--background', '--python',
        str(zuly_path / 'jues_audit_batch.py'),
        '--', str(blend_path), color
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore')
    
    # Mostrar salida
    if result.stdout:
        # Buscar líneas relevantes
        for line in result.stdout.split('\n'):
            if any(k in line for k in ['Score', 'Dictamen', 'Objetos', 'icon', 'JUES', 'AUDITOR', 'Reporte']):
                print(line)
    
    # Buscar JSON generado
    json_path = arena_path / f"{model_id}_AUDIT.json"
    if json_path.exists():
        with open(json_path) as f:
            data = json.load(f)
            resultados.append({
                'modelo': model_id,
                'score': data.get('score', 0),
                'dictamen': data.get('dictamen', 'ERROR'),
                'objetos': data.get('total_objetos', 0)
            })
            print(f"✅ Auditado: {data.get('score', 0)}/100 - {data.get('dictamen', 'N/A')}")

# Resumen final
print("\n" + "=" * 70)
print("📊 RESUMEN AUDITORÍA")
print("=" * 70)

for r in resultados:
    icon = "✅" if r['score'] >= 80 else "⚠️" if r['score'] >= 60 else "❌"
    print(f"{icon} {r['modelo']}: {r['score']}/100 - {r['dictamen']} ({r['objetos']} objs)")

if resultados:
    avg = sum(r['score'] for r in resultados) / len(resultados)
    aptos = sum(1 for r in resultados if r['score'] >= 80)
    print(f"\n📈 Promedio: {avg:.1f}/100")
    print(f"✅ APTOS: {aptos}/{len(resultados)}")

print("\n" + "=" * 70)
print("🎉 AUDITORÍA COMPLETA - JUES-BOT UNIFICADO")
print("=" * 70)
