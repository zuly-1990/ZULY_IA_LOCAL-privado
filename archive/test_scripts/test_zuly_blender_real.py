"""
ZULY → Blender Real - Test de Integración
==========================================

Este script ejecuta ZULY con Blender REAL (no simulado).
Prueba comandos básicos para verificar la integración.
"""
import bpy
import sys
from pathlib import Path

# Agregar ZULY al path
zuly_path = Path(__file__).parent
sys.path.insert(0, str(zuly_path))

print("=" * 70)
print("ZULY → BLENDER REAL - TEST DE INTEGRACIÓN")
print("=" * 70)

# Limpiar escena inicial
print("\n[1/5] Limpiando escena...")
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Importar ZULY
print("[2/5] Inicializando ZULY con BlenderAdapter...")
from core.agent import Agent

# force_mock=False → Usa BlenderAdapter REAL
agent = Agent(force_mock=False)

print(f"[3/5] Handlers disponibles: {len(agent.intent_router.command_handlers)}")

# Test 0: Limpieza vía Handler
print("\n[4/5] TEST 0: Limpiar escena vía ZULY")
result0 = agent.execute_via_router('blender.clear_scene', {})
print(f"  → Success: {result0.get('success')}")

# Test 1: Crear cubo
print("\n[4/5] TEST 1: Crear cubo azul")
result1 = agent.execute_via_router('blender.create_cube', {
    'location': [0, 0, 0],
    'scale': 2.0,
    'name': 'CuboZULY'
})
print(f"  → Success: {result1.get('success')}")
print(f"  → Object: {result1.get('object_name', 'N/A')}")

# Test 2: Crear luz
print("\n[4/5] TEST 2: Crear luz solar")
result2 = agent.execute_via_router('blender.create_light', {
    'light_type': 'SUN',
    'energy': 5.0,
    'name': 'LuzZULY'
})
print(f"  → Success: {result2.get('success')}")
print(f"  → Light: {result2.get('object_name', 'N/A')}")

# Test 3: Crear cámara
print("\n[4/5] TEST 3: Crear cámara")
result3 = agent.execute_via_router('blender.create_camera', {
    'location': [7, -7, 5],
    'name': 'CamaraZULY'
})
print(f"  → Success: {result3.get('success')}")
print(f"  → Camera: {result3.get('object_name', 'N/A')}")

# Test 4: Render (VINCULACIÓN CRÍTICA)
print("\n[4/5] TEST 4: Renderizado de prueba")
render_path = "ZULY_LAB/resultados_zuly/test_render_integracion.png"
result4 = agent.execute_via_router('blender.render_scene', {
    'output_path': render_path,
    'resolution': [400, 300],
    'samples': 8
})
print(f"  → Success: {result4.get('success')}")
print(f"  → Path: {result4.get('output_path')}")

# Verificar objetos creados
print("\n[5/5] Verificación de objetos en escena:")
for obj in bpy.data.objects:
    print(f"  → {obj.name} ({obj.type})")

# Resultado final
print("\n" + "=" * 70)
tester_results = [result0, result1, result2, result3, result4]
if all(r.get('success') for r in tester_results):
    print("✅ ZULY FUNCIONA CON BLENDER REAL Y RENDERIZADO")
else:
    print("⚠️  Algunos comandos fallaron - revisar logs")
print("=" * 70)

# Guardar .blend de prueba en ZULY_PROJECTS
output_path = zuly_path / "ZULY_PROJECTS" / "test_zuly_real.blend"
bpy.ops.wm.save_as_mainfile(filepath=str(output_path))
print(f"\n💾 Escena guardada en: {output_path}")
