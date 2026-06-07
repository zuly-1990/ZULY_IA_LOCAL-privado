#!/usr/bin/env python3
"""
Test: Verificar primitivas base funcionan 100%
Base sólida antes de pivotear a arquitectura.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

print("="*60)
print("TEST: Primitivas Base ZULY")
print("="*60)

# Test 1: Crear cubo
print("\n1. Crear cubo...")
try:
    from core.adapters import get_engine_adapter
    from core.commands.blender_handlers.primitives import create_cube_handler
    
    adapter = get_engine_adapter(force_mock=True)
    result = create_cube_handler({'size': 2.0, 'color': 'azul'}, adapter)
    
    if result['success']:
        print(f"   ✓ Cubo creado: {result.get('object_name')}")
        print(f"   ✓ Tamaño: {result.get('parameters', {}).get('size')}m")
    else:
        print(f"   ✗ Falló: {result.get('error')}")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 2: Crear esfera
print("\n2. Crear esfera...")
try:
    from core.commands.blender_handlers.primitives import create_sphere_handler
    
    result = create_sphere_handler({'radius': 1.0, 'color': 'rojo'}, adapter)
    
    if result['success']:
        print(f"   ✓ Esfera creada: {result.get('object_name')}")
        print(f"   ✓ Radio: {result.get('parameters', {}).get('radius')}m")
    else:
        print(f"   ✗ Falló: {result.get('error')}")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 3: Crear cilindro
print("\n3. Crear cilindro...")
try:
    from core.commands.blender_handlers.primitives import create_cylinder_handler
    
    result = create_cylinder_handler({'radius': 0.5, 'depth': 2.0}, adapter)
    
    if result['success']:
        print(f"   ✓ Cilindro creado: {result.get('object_name')}")
        print(f"   ✓ Dimensiones: {result.get('parameters', {})}")
    else:
        print(f"   ✗ Falló: {result.get('error')}")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 4: Agente ejecuta comando natural
print("\n4. Agente ejecuta 'crea un cubo azul'...")
try:
    from core.agent import Agent
    
    agent = Agent(auto_monitor=False, force_mock=True)
    result = agent.process_natural_request("crea un cubo azul")
    
    if result['success']:
        print(f"   ✓ Comando exitoso")
        print(f"   ✓ Feedback: {result['feedback'][:50]}...")
    else:
        print(f"   ✗ Falló: {result.get('error')}")
except Exception as e:
    print(f"   ✗ Error: {e}")

print("\n" + "="*60)
print("✅ Base primitivas verificada")
print("="*60)
print("\nPRÓXIMO PASO: Derivar arquitectura de estas primitivas")
print("  - Pared = Cubo escalado (largo x alto x grosor)")
print("  - Piso = Plano escalado")
print("  - Ventana = Cubo + operación booleana")
