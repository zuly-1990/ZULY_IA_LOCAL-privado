"""Test simple de integración IntentRouter"""
from core.agent import Agent

print("=" * 60)
print("FASE 23: TEST DE INTEGRACIÓN")
print("=" * 60)

# Inicializar Agent con MockAdapter
agent = Agent(force_mock=True)

print(f"\n>>> Handlers disponibles: {len(agent.intent_router.command_handlers)}")

# Test 1: Llamada directa al router
print("\n>>> Test 1: execute_via_router() directo")
result1 = agent.execute_via_router('blender.create_cube', {'location': [0,0,0], 'scale': 2.0})
print(f"Success: {result1.get('success')}")
print(f"Route: {result1.get('route')}")
print(f"Object: {result1.get('object_name', 'N/A')}")

# Test 2: Via process_natural_request (si el NLU lo soporta)
# Este test puede fallar si el NLU no tiene templates, pero no es crítico
print("\n>>> Test 2: process_natural_request() (puede fallar, no es crítico)")
try:
    from core.utils.nlu import CommandIntent
    # Crear intent sintético
    intent = CommandIntent(
        command_name='crear_cubo',
        confidence=0.95,
        parameters={'location': [1, 1, 1], 'scale': 1.5}
    )
    result2 = agent._execute_intent(intent)
    print(f"Success: {result2.get('success')}")
    print(f"Route: {result2.get('route', 'OLD_SYSTEM')}")
except Exception as e:
    print(f"Error (esperado): {e}")

print("\n" + "=" * 60)
print("TEST COMPLETADO")
print("=" * 60)
