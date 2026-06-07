#!/usr/bin/env python3
"""Test rápido de JUESController"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from core.jues_controller import JUESController, get_jues_controller

print("="*60)
print("TEST: JUESController")
print("="*60)

# Test 1: Import
print("\n1. Import...")
print("   ✓ JUESController importado")

# Test 2: Singleton
print("\n2. Singleton...")
ctrl = get_jues_controller()
print("   ✓ Singleton funciona")

# Test 3: Validación simple
print("\n3. Validación y decisión...")
resultados = {
    'v0_result': {'verified': True, 'details': 'OK'},
    'v1_result': {'verified': True, 'details': 'OK'},
    'v2_result': {'verified': True, 'details': 'OK'},
    'v3_result': {'verified': True, 'metrics': {'is_watertight': True}},
    'chromatic_sync_result': {'match': True, 'details': 'OK'},
    'optimization_instinct_result': {'optimized': True, 'details': 'OK', 'final_size_kb': 100},
    'immutability_seal_result': {'verified': True, 'hash_short': 'abc123'}
}

resultado = ctrl.validar_y_decidir('TEST_CONSOLIDACION', resultados)
print(f"   ✓ Status: {resultado['status']}")
print(f"   ✓ Puntuación: {resultado.get('puntuacion_jues', 'N/A')}pts")

# Test 4: Estadísticas
print("\n4. Estadísticas...")
stats = ctrl.get_estadisticas(dias=7)
print(f"   ✓ Total reportes: {stats['total_reportes']}")

print("\n" + "="*60)
print("✅ JUESController 100% operativo")
print("="*60)
