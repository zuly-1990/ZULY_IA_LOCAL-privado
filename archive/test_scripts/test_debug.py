#!/usr/bin/env python3
"""Debug script para LYZU Core"""

from lyzu_core import LYZUCore
import traceback

print("=" * 60)
print("TEST 1: Inicializar LYZU")
print("=" * 60)
try:
    lyzu = LYZUCore(mode='hybrid')
    print("✓ LYZU inicializado correctamente")
except Exception as e:
    print(f"✗ Error: {e}")
    traceback.print_exc()
    exit(1)

print("\n" + "=" * 60)
print("TEST 2: Procesar entrada simple")
print("=" * 60)
try:
    user_input = "Crea un cubo"
    print(f"Input: '{user_input}'")
    result = lyzu.process_user_input(user_input)
    print(f"✓ Procesado exitosamente")
    print(f"  Resultado: {result}")
except Exception as e:
    print(f"✗ Error: {e}")
    traceback.print_exc()
    exit(1)

print("\n" + "=" * 60)
print("TEST 3: Procesar entrada con typo")
print("=" * 60)
try:
    user_input = "crear cuvo"
    print(f"Input: '{user_input}'")
    result = lyzu.process_user_input(user_input)
    print(f"✓ Procesado exitosamente")
    print(f"  Resultado: {result}")
except Exception as e:
    print(f"✗ Error: {e}")
    traceback.print_exc()
    exit(1)

print("\n" + "=" * 60)
print("✅ TODOS LOS TESTS PASARON")
print("=" * 60)
