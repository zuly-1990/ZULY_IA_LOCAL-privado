#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 AUDITORÍA DETALLADA - 5 MODELOS CON JUES-BOT UNIFICADO
"""

import subprocess
import sys
import json
from pathlib import Path

zuly_path = Path('c:/Users/Admin/Desktop/ZULY_IA_LOCAL')
arena_path = zuly_path / 'archivo_zuly/temp_arena'

# 5 modelos a auditar
modelos = [
    ("MOD-001_Pabellon_Minimalista.blend", "#B0B0B0"),
    ("MOD-002_Torre_Corporativa.blend", "#B0B0B0"),
    ("MOD-003_Casa_Contenedor.blend", "#B0B0B0"),
    ("MOD-004_Museo_Arte.blend", "#99AACC"),
    ("MOD-005_Estacion_Espacial.blend", "#99AACC"),
]

print("=" * 70)
print("🚀 AUDITORÍA DETALLADA - JUES-BOT UNIFICADO")
print("=" * 70)

resultados_finales = []

for blend_file, color in modelos:
    blend_path = arena_path / blend_file
    model_id = blend_file.replace('.blend', '')
    
    print(f"\n{'='*70}")
    print(f"🔍 {model_id}")
    print(f"{'='*70}")
    
    if not blend_path.exists():
        print(f"❌ Archivo no encontrado")
        continue
    
    # Script que retorna JSON - usar forward slashes para evitar escape errors
    blend_path_str = str(blend_path).replace('\\', '/')
    zuly_path_str = str(zuly_path).replace('\\', '/')
    
    script = f'''
import sys
import json
sys.path.insert(0, "{zuly_path_str}")
sys.path.insert(0, "{zuly_path_str}/core")

from core.jues_bot import jues_bot_validar_y_sellar

resultado = jues_bot_validar_y_sellar(
    blend_path="{blend_path_str}",
    candidato_id="{model_id}",
    target_color="{color}",
    aprobar=False
)

# Imprimir como JSON para parsing
print("JSON_RESULT_START")
print(json.dumps(resultado))
print("JSON_RESULT_END")
'''
    
    temp_script = zuly_path / f'audit_json_{model_id}.py'
    with open(temp_script, 'w', encoding='utf-8') as f:
        f.write(script)
    
    blender_exe = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe"
    
    result = subprocess.run(
        [str(blender_exe), '--background', '--python', str(temp_script)],
        capture_output=True, text=True, encoding='utf-8', errors='ignore',
        cwd=str(zuly_path)
    )
    
    temp_script.unlink()
    
    # Parsear resultado JSON
    try:
        stdout = result.stdout
        start_idx = stdout.find('JSON_RESULT_START')
        end_idx = stdout.find('JSON_RESULT_END')
        
        if start_idx != -1 and end_idx != -1:
            json_str = stdout[start_idx + len('JSON_RESULT_START'):end_idx].strip()
            data = json.loads(json_str)
            
            score = data.get('score', 0)
            dictamen = data.get('dictamen', 'N/A')
            sellado = data.get('sellado', False)
            
            # Mostrar resultado
            icon = "✅" if score >= 80 else "⚠️" if score >= 60 else "❌"
            print(f"{icon} Score: {score}/100 | Dictamen: {dictamen}")
            
            if 'superpoderes' in data:
                for sp_name, sp_data in data['superpoderes'].items():
                    status = sp_data.get('status', 'N/A')
                    sp_icon = sp_data.get('icon', '')
                    print(f"   {sp_icon} {sp_name}: {status}")
            
            resultados_finales.append({
                'modelo': model_id,
                'score': score,
                'dictamen': dictamen,
                'sellado': sellado
            })
        else:
            print(f"⚠️ No se pudo parsear resultado JSON")
            print(f"Salida: {stdout[-500:]}")
            
    except Exception as e:
        print(f"❌ Error parseando resultado: {e}")

# Resumen final
print("\n" + "=" * 70)
print("📊 RESUMEN FINAL AUDITORÍA")
print("=" * 70)

for r in resultados_finales:
    icon = "✅" if r['score'] >= 80 else "⚠️" if r['score'] >= 60 else "❌"
    print(f"{icon} {r['modelo']}: {r['score']}/100 - {r['dictamen']}")

avg_score = sum(r['score'] for r in resultados_finales) / len(resultados_finales) if resultados_finales else 0
print(f"\n📈 Score Promedio: {avg_score:.1f}/100")

aptos = sum(1 for r in resultados_finales if 'APTO' in r['dictamen'])
print(f"✅ Modelos APTOS: {aptos}/{len(resultados_finales)}")

print("\n" + "=" * 70)
print("🎉 AUDITORÍA COMPLETA")
print("=" * 70)
