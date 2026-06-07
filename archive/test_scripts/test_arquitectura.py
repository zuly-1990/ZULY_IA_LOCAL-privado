#!/usr/bin/env python3
"""
Test: Handlers arquitectónicos conectados a Assembly Patterns
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

print("="*60)
print("TEST: Handlers Arquitectónicos + Assembly Patterns")
print("="*60)

# Test 1: IntentManager reconoce "columna"
print("\n1. IntentManager reconoce 'crea una columna'...")
try:
    from core.intents.intent_manager import IntentManager
    im = IntentManager()
    intent = im.classify("crea una columna")
    print(f"   ✓ Intent: {intent.name}")
    print(f"   ✓ Command: {intent.command}")
    print(f"   ✓ Confidence: {intent.confidence:.2f}")
    assert intent.command == 'blender.create_column', f"Esperaba blender.create_column, got {intent.command}"
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 2: IntentManager reconoce "muro"
print("\n2. IntentManager reconoce 'crea un muro'...")
try:
    intent = im.classify("crea un muro")
    print(f"   ✓ Intent: {intent.name}")
    print(f"   ✓ Command: {intent.command}")
    assert intent.command == 'blender.create_wall', f"Esperaba blender.create_wall, got {intent.command}"
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 3: IntentManager reconoce "habitación"
print("\n3. IntentManager reconoce 'crea una habitación'...")
try:
    intent = im.classify("crea una habitación")
    print(f"   ✓ Intent: {intent.name}")
    print(f"   ✓ Command: {intent.command}")
    assert intent.command == 'blender.create_room', f"Esperaba blender.create_room, got {intent.command}"
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 4: Handler crear_columna funciona
print("\n4. Handler crear_columna...")
try:
    from core.commands.blender_handlers.architectural import crear_columna_handler
    from core.adapters import get_engine_adapter
    
    adapter = get_engine_adapter(force_mock=True)
    result = crear_columna_handler({}, adapter)
    
    if result.get('success'):
        print(f"   ✓ Columna creada: {result.get('message')}")
        print(f"   ✓ Objetos: {result['result'].get('created_objects', [])}")
        print(f"   ✓ Patrón: {result['result'].get('pattern')}")
    else:
        print(f"   ✗ Falló: {result.get('message')}")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 5: Handler crear_muro funciona
print("\n5. Handler crear_muro (3m x 2.5m x 0.2m)...")
try:
    from core.commands.blender_handlers.architectural import crear_muro_handler
    
    result = crear_muro_handler({'ancho': 3.0, 'alto': 2.5, 'grosor': 0.2}, adapter)
    
    if result.get('success'):
        dims = result['result']['dimensions']
        print(f"   ✓ Muro creado: {dims['ancho_m']}m x {dims['alto_m']}m x {dims['grosor_m']}m")
    else:
        print(f"   ✗ Falló: {result.get('message')}")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 6: Handler crear_habitacion funciona
print("\n6. Handler crear_habitacion (4m x 5m x 2.5m)...")
try:
    from core.commands.blender_handlers.architectural import crear_habitacion_handler
    
    result = crear_habitacion_handler({'ancho': 4.0, 'profundidad': 5.0, 'altura': 2.5}, adapter)
    
    if result.get('success'):
        stats = result['result']['stats']
        dims = result['result']['dimensions']
        print(f"   ✓ Habitación: {dims['ancho_m']}m x {dims['profundidad_m']}m x {dims['altura_m']}m")
        print(f"   ✓ Objetos: {stats['total_objects']} ({stats['paredes']} paredes + piso + techo)")
    else:
        print(f"   ✗ Falló: {result.get('message')}")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 7: Handler listar_patrones
print("\n7. Handler listar_patrones...")
try:
    from core.commands.blender_handlers.architectural import listar_patrones_handler
    
    result = listar_patrones_handler({})
    
    if result.get('success'):
        patterns = result['result']['patterns']
        print(f"   ✓ {result['result']['total']} patrones disponibles:")
        for p in patterns:
            print(f"     - {p['name']}: {p['description'][:50]}...")
    else:
        print(f"   ✗ Falló: {result.get('message')}")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 8: Agent procesa "crea una columna"
print("\n8. Agent procesa 'crea una columna'...")
try:
    from core.agent import Agent
    
    agent = Agent(auto_monitor=False, force_mock=True)
    result = agent.process_natural_request("crea una columna")
    
    if result.get('success'):
        print(f"   ✓ Agente ejecutó: {result.get('feedback', '')[:60]}...")
    else:
        print(f"   ✗ Falló: {result.get('error', 'unknown')}")
except Exception as e:
    print(f"   ✗ Error: {e}")

print("\n" + "="*60)
print("✅ Test Arquitectónico Completado")
print("="*60)
