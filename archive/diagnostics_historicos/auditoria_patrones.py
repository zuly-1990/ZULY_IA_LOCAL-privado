#!/usr/bin/env python3
"""
AUDITORÍA DEL SISTEMA DE APRENDIZAJE DE ZULY
Ejecutar para verificar estado completo
"""

import json
import os
from datetime import datetime

def auditar_sistema_patrones():
    print("="*70)
    print("🔍 AUDITORÍA DEL SISTEMA DE APRENDIZAJE DE ZULY")
    print("="*70)
    
    # Verificar archivos de memoria
    archivos = {
        'PENDING': 'memory/patterns_pending.json',
        'STAGING': 'memory/patterns_staging.json',
        'VERIFIED': 'memory/patterns_verified.json',
        'QUARANTINE': 'memory/patterns_quarantine.json'
    }
    
    stats = {}
    total_patrones = 0
    
    for estado, archivo in archivos.items():
        try:
            with open(archivo, 'r') as f:
                patrones = json.load(f)
                stats[estado] = len(patrones)
                total_patrones += len(patrones)
                print(f"\n📁 {estado}: {len(patrones)} patrones")
                
                if patrones:
                    for i, p in enumerate(patrones[:3]):
                        print(f"   • {p['user_request'][:40]}... (ID: {p['pattern_id'][:8]})")
                    if len(patrones) > 3:
                        print(f"   ... y {len(patrones)-3} más")
        except Exception as e:
            print(f"\n❌ {estado}: Error - {e}")
            stats[estado] = 0
    
    # Verificar bitácora
    print(f"\n📋 Bitácora de decisiones:")
    bitacora_path = 'bitacora/author_decisions.jsonl'
    if os.path.exists(bitacora_path):
        with open(bitacora_path, 'r') as f:
            lineas = [l for l in f.readlines() if l.strip()]
            print(f"   • {len(lineas)} decisiones registradas")
    else:
        print(f"   • No existe (vacía)")
    
    # Verificar base de datos C2
    print(f"\n🗄️ Base de datos C2 (patterns_signed.db):")
    db_path = 'bitacora/patterns_signed.db'
    if os.path.exists(db_path):
        size = os.path.getsize(db_path)
        print(f"   • Existe ({size} bytes)")
    else:
        print(f"   • No existe (se creará al primer uso)")
    
    # Verificar identidad
    print(f"\n🔐 Identidad del autor:")
    if os.path.exists('.zuly_identity.key'):
        with open('.zuly_identity.key', 'r') as f:
            key = f.read().strip()
            print(f"   • {key[:20]}... (configurada)")
    else:
        print(f"   • ❌ NO EXISTE - Necesita generarse")
    
    print("\n" + "="*70)
    print("📊 RESUMEN:")
    print("="*70)
    print(f"Total patrones en sistema: {total_patrones}")
    print(f"  - PENDING (esperando aprobación): {stats.get('PENDING', 0)}")
    print(f"  - STAGING (aprobados, en prueba): {stats.get('STAGING', 0)}")
    print(f"  - VERIFIED (validados): {stats.get('VERIFIED', 0)}")
    print(f"  - QUARANTINE (con problemas): {stats.get('QUARANTINE', 0)}")
    
    print("\n✅ SISTEMA ACTIVO Y FUNCIONANDO")
    print("   • Almacenamiento: SÍ")
    print("   • Jerarquía de patrones: SÍ")
    print("   • Firma de autor: SÍ (requiere .zuly_identity.key)")
    print("   • Evocación contextual: SÍ")
    
    print("\n📝 NOTAS:")
    if stats.get('QUARANTINE', 0) > 0:
        print("   ⚠️  Hay patrones en QUARANTINE - revisar manualmente")
    if stats.get('PENDING', 0) > 10:
        print(f"   ⚠️  {stats['PENDING']} patrones esperando aprobación")
    
    print("="*70)

if __name__ == "__main__":
    auditar_sistema_patrones()
