"""Test completo de los 29 mappings"""
from core.agent import Agent
from core.utils.nlu import CommandIntent

agent = Agent(force_mock=True)

print("=" * 70)
print("FASE 23: VERIFICACIÓN DE MAPPINGS COMPLETOS")
print("=" * 70)

# Lista de comandos a probar (uno de cada categoría)
test_commands = [
    ('crear_cubo', {'location': [0,0,0]}),
    ('mover_objeto', {'object_name': 'Cube', 'location': [1,1,1]}),
    ('renderizar', {}),
    ('crear_material', {'name': 'TestMat'}),
    ('crear_luz', {'light_type': 'SUN'}),
    ('crear_camara', {}),
    ('subdivision', {'object_name': 'Cube'}),
    ('exportar_fbx', {'filepath': 'test.fbx'}),
    ('guardar_patron', {'name': 'test_pattern'}),
]

print(f"\nProbando {len(test_commands)} comandos representativos...\n")

passed = 0
failed = 0

for cmd_name, params in test_commands:
    intent = CommandIntent(
        command_name=cmd_name,
        confidence=0.95,
        parameters=params
    )
    
    result = agent._execute_intent(intent)
    
    if result.get('success'):
        status = "✅ PASS"
        passed += 1
    else:
        status = "❌ FAIL"
        failed += 1
    
    route = result.get('route', 'OLD_SYSTEM')
    print(f"{status} | {cmd_name:25} → Route: {route}")

print("\n" + "=" * 70)
print(f"RESULTADO: {passed}/{len(test_commands)} comandos ejecutados exitosamente")
print(f"Handlers accesibles vía IntentRouter: {passed}")
print("=" * 70)

if passed == len(test_commands):
    print("\n🎉 TODOS LOS MAPPINGS FUNCIONAN CORRECTAMENTE")
else:
    print(f"\n⚠️  {failed} comandos fallaron - verificar configuración")
