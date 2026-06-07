#!/usr/bin/env python3
"""
APROBAR LOS 23 PATRONES PENDIENTES
Mover de PENDING a STAGING para que ZULY pueda usarlos
"""

import json
import os

def aprobar_todos_los_patrones():
    print("="*60)
    print("✅ APROBANDO PATRONES PENDIENTES")
    print("="*60)
    
    # Cargar patrones pendientes
    with open('memory/patterns_pending.json', 'r') as f:
        patrones = json.load(f)
    
    print(f"\n📋 Total patrones a aprobar: {len(patrones)}")
    
    # Cargar staging existente (vacío)
    try:
        with open('memory/patterns_staging.json', 'r') as f:
            staging = json.load(f)
    except:
        staging = []
    
    # Aprobar cada patrón
    aprobados = 0
    for p in patrones:
        # Cambiar status
        p['metadata']['status'] = 'STAGING'
        p['metadata']['aprobado_por'] = 'admin'
        p['metadata']['timestamp_aprobacion'] = '2026-04-03T12:59:00'
        staging.append(p)
        aprobados += 1
        print(f"  ✅ {p['user_request'][:40]}... (ID: {p['pattern_id'][:8]})")
    
    # Guardar staging
    with open('memory/patterns_staging.json', 'w') as f:
        json.dump(staging, f, indent=2)
    
    # Limpiar pending
    with open('memory/patterns_pending.json', 'w') as f:
        json.dump([], f, indent=2)
    
    print(f"\n📊 Resultado:")
    print(f"  • Aprobados: {aprobados}")
    print(f"  • En STAGING: {len(staging)}")
    print(f"  • En PENDING: 0")
    
    print("\n" + "="*60)
    print("✅ TODOS LOS PATRONES APROBADOS")
    print("="*60)
    print("\nZULY ahora puede:")
    print("  • Usar estos patrones para evocación")
    print("  • Aprender de ellos")
    print("  • Reutilizar en comandos similares")
    print("="*60)

if __name__ == "__main__":
    aprobar_todos_los_patrones()
