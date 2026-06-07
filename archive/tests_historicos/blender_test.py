"""
blender_test.py

Script para ejecutar dentro de Blender.
Prueba todos los handlers en ambiente real.

Uso en Blender:
1. Abrir Blender
2. Scripting → New
3. Copiar este código
4. Run Script
"""

import sys
from pathlib import Path

# Agregar path de ZULY al sys.path
zuly_path = Path("C:/Users/Admin/Desktop/ZULY_IA_LOCAL")
if str(zuly_path) not in sys.path:
    sys.path.insert(0, str(zuly_path))

import bpy
from lyzu_core import LYZUCore

print("\n" + "=" * 70)
print("BLENDER TEST: LYZU Core Handlers en Ambiente Real")
print("=" * 70 + "\n")

# Inicializar LYZU
print("[1/5] Inicializando LYZU Core...")
lyzu = LYZUCore(mode='reactive')
print("✅ LYZU inicializado\n")

# Test 1: Crear cubo
print("[2/5] TEST: Crear cubo")
print("-" * 70)
result = lyzu.process_user_input("Crea un cubo")
print(f"Input: 'Crea un cubo'")
print(f"Intent: {result.get('intent', 'N/A')}")
print(f"Confidence: {result.get('confidence', 0):.1%}")
print(f"Success: {result.get('success', 'N/A')}")
print()

# Verificar que cubo se creó en Blender (puede llamarse Cube, Cube.001, etc.)
cube_found = any(obj.name.startswith('Cube') for obj in bpy.data.objects)
if cube_found:
    # Obtener el objeto más reciente que empiece por Cube
    cubes = [obj for obj in bpy.data.objects if obj.name.startswith('Cube')]
    cube = cubes[-1]
    print(f"✅ Cubo encontrado en Blender: {cube.name}")
    print(f"   Ubicación: {tuple(cube.location)}")
    print(f"   Escala: {tuple(cube.scale)}")
else:
    print("❌ Cubo no encontrado en Blender")
print()

# Test 2: Crear esfera
print("[3/5] TEST: Crear esfera")
print("-" * 70)
result = lyzu.process_user_input("Crea una esfera")
print(f"Input: 'Crea una esfera'")
print(f"Intent: {result.get('intent', 'N/A')}")
print(f"Confidence: {result.get('confidence', 0):.1%}")
print(f"Success: {result.get('success', 'N/A')}")

sphere_found = any(obj.name.startswith('Sphere') for obj in bpy.data.objects)
if sphere_found:
    print("✅ Esfera encontrada en Blender!")
else:
    print("❌ Esfera no encontrada")
print()

# Test 3: Mover objeto
print("[4/5] TEST: Mover objeto")
print("-" * 70)
if cube_found:
    # Preparar para mover
    result = lyzu.process_user_input("Mueve el cubo a 5 10 15")
    # Recargar referencia al cubo por si cambió de nombre (no debería, pero para ser seguros)
    cubes = [obj for obj in bpy.data.objects if obj.name.startswith('Cube')]
    cube = cubes[-1]
    print(f"✅ Intento de mover completado")
    print(f"   Intent: {result.get('intent', 'N/A')}")
    print(f"   Nueva posición: {tuple(cube.location)}")
else:
    print("❌ Cubo no disponible para mover")
print()

# Test 4: Rotar objeto
print("[5/5] TEST: Rotar objeto")
print("-" * 70)
if cube_found:
    result = lyzu.process_user_input("Rota el cubo")
    cube = cubes[-1]
    print(f"✅ Intento de rotar completado")
    print(f"   Intent: {result.get('intent', 'N/A')}")
    print(f"   Nueva rotación: {tuple(cube.rotation_euler)}")
else:
    print("❌ Cubo no disponible")
print()

# Resumen
print("=" * 70)
print("RESUMEN DE OBJETOS EN ESCENA")
print("=" * 70)
for obj in bpy.data.objects:
    print(f"  • {obj.name} ({obj.type})")
    print(f"    - Ubicación: {tuple(obj.location)}")
    print(f"    - Escala: {tuple(obj.scale)}")

print("\n" + "=" * 70)
print("✅ PRUEBAS EN BLENDER COMPLETADAS")
print("=" * 70 + "\n")
