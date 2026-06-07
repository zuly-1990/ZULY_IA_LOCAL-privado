#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 AUDITORÍA BATCH FINAL - 5 MODELOS
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

for blend_file, color in modelos:
    blend_path = arena_path / blend_file
    model_id = blend_file.replace('.blend', '')
    
    print(f"\n{'─'*70}")
    print(f"🔍 {model_id}")
    print(f"{'─'*70}")
    
    if not blend_path.exists():
        print(f"❌ No encontrado")
        continue
    
    cmd = [
        str(blender_exe), '--background', '--python',
        str(zuly_path / 'jues_audit_batch.py'),
        '--', str(blend_path), color
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore')
    
    # Extraer score y dictamen de la salida
    score = "N/A"
    dictamen = "N/A"
    for line in result.stdout.split('\n'):
        if 'Score:' in line:
            score = line.split('Score:')[1].strip().split()[0]
        if 'Dictamen:' in line:
            dictamen = line.split('Dictamen:')[1].strip()
    
    icon = "✅" if str(score) != "N/A" and int(score.split('/')[0]) >= 80 else "⚠️" if str(score) != "N/A" and int(score.split('/')[0]) >= 60 else "❌"
    print(f"{icon} Score: {score} | Dictamen: {dictamen}")

print("\n" + "=" * 70)
print("📊 RESUMEN FINAL")
print("=" * 70)

# Leer todos los JSON generados
scores = []
for blend_file, _ in modelos:
    model_id = blend_file.replace('.blend', '')
    json_path = arena_path / f"{model_id}_AUDIT.json"
    
    if json_path.exists():
        with open(json_path) as f:
            data = json.load(f)
            score = data.get('score', 0)
            scores.append((model_id, score, data.get('dictamen', 'N/A')))

for model_id, score, dictamen in scores:
    icon = "✅" if score >= 80 else "⚠️" if score >= 60 else "❌"
    print(f"{icon} {model_id}: {score}/100 - {dictamen}")

if scores:
    avg = sum(s[1] for s in scores) / len(scores)
    aptos = sum(1 for s in scores if s[1] >= 80)
    print(f"\n📈 Promedio: {avg:.1f}/100")
    print(f"✅ APTOS: {aptos}/{len(scores)}")

print("\n" + "=" * 70)
print("🎉 AUDITORÍA COMPLETA")
print("=" * 70)
