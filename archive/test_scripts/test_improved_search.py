#!/usr/bin/env python3
"""
test_improved_search.py

Valida que la búsqueda mejorada de patrones funciona bien.
"""

import sys
sys.path.insert(0, 'c:\\Users\\Admin\\Desktop\\ZULY_IA_LOCAL')

from decision_engine import get_decision_engine

print("\n" + "="*80)
print("🔍 TEST: Búsqueda Mejorada de Patrones")
print("="*80 + "\n")

engine = get_decision_engine()

test_cases = [
    # (query, expected_pattern_name, esperado_tipo)
    ("crear un cubo", "crear_cubo", "usar_patron"),
    ("crea un cubo", "crear_cubo", "usar_patron"),
    ("crea cubo", "crear_cubo", "usar_patron"),
    ("haz un cubo", "crear_cubo", "usar_patron"),
    ("quiero un cubo", "crear_cubo", "usar_patron"),
    
    ("crear esfera", "crear_esfera", "usar_patron"),
    ("crea una esfera", "crear_esfera", "usar_patron"),
    
    ("mover mi objeto", "mover_objeto", "usar_patron"),
    ("mover un objeto", "mover_objeto", "usar_patron"),
    
    ("renderizar la escena", "renderizar", "usar_patron"),
    ("render", "renderizar", "usar_patron"),
    
    ("algo completamente raro", None, "usar_agente"),
]

passed = 0
failed = 0

for query, expected_pattern, expected_type in test_cases:
    decision = engine.decidir(query)
    
    matches = (decision["tipo"] == expected_type and 
               (expected_pattern is None or decision.get("patron") == expected_pattern))
    
    status = "✅" if matches else "❌"
    actual_pattern = decision.get("patron", "NINGUNO")
    confianza = decision.get("confianza", 0)
    
    print(f"{status} Query: '{query}'")
    print(f"   └─ Esperado: {expected_pattern or 'AGENTE'} | Recibido: {actual_pattern}")
    print(f"   └─ Tipo: {decision['tipo']} | Confianza: {confianza:.0%}")
    
    if matches:
        passed += 1
    else:
        failed += 1
    
    print()

print("="*80)
print(f"📊 RESULTADOS: {passed} pasados, {failed} fallidos")
print("="*80 + "\n")

if failed == 0:
    print("✅ TODOS LOS TESTS PASARON\n")
else:
    print(f"⚠️  {failed} tests fallaron\n")
