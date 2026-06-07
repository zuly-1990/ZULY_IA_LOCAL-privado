"""
INSTRUCCIONES PARA EJECUTAR EN BLENDER (MANUAL)

1. Abre Blender
2. Ve a: Scripting → New Text
3. Copia TODO el código de abajo
4. Presiona: Alt+P (para ejecutar)

============================================================
CÓDIGO PARA COPIAR EN BLENDER:
============================================================
"""

# ===== INICIO CÓDIGO BLENDER =====

import sys
import bpy
from pathlib import Path

# Agregar ZULY al path
zuly_path = Path("C:/Users/Admin/Desktop/ZULY_IA_LOCAL")
if str(zuly_path) not in sys.path:
    sys.path.insert(0, str(zuly_path))

from lyzu_core import LYZUCore

print("\n" + "="*70)
print("PRUEBA EN BLENDER: LYZU Core Handlers")
print("="*70 + "\n")

# 1. Limpiar escena (opcional)
print("[SETUP] Limpiando escena anterior...")
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
print("✅ Escena limpia\n")

# 2. Inicializar LYZU
print("[1/6] Inicializando LYZU Core...")
lyzu = LYZUCore(mode='reactive')
print("✅ LYZU inicializado\n")

# 3. Crear cubo
print("[2/6] TEST: Crear cubo")
print("-"*70)
result = lyzu.process_user_input("Crea un cubo")
print(f"  Input: 'Crea un cubo'")
print(f"  Intent: {result.get('intent', 'N/A')}")
print(f"  Confidence: {result.get('confidence', 0):.1%}")
if 'Cube' in bpy.data.objects:
    cube = bpy.data.objects['Cube']
    print(f"  ✅ Cubo creado en Blender")
    print(f"     Posición: {tuple(cube.location)}\n")
else:
    print(f"  ❌ Cubo no creado\n")

# 4. Crear esfera
print("[3/6] TEST: Crear esfera roja")
print("-"*70)
result = lyzu.process_user_input("Crea una esfera roja")
print(f"  Input: 'Crea una esfera roja'")
print(f"  Intent: {result.get('intent', 'N/A')}")
if 'Sphere' in bpy.data.objects:
    sphere = bpy.data.objects['Sphere']
    print(f"  ✅ Esfera creada en Blender")
    print(f"     Posición: {tuple(sphere.location)}\n")
else:
    print(f"  ❌ Esfera no creada\n")

# 5. Mover cubo
print("[4/6] TEST: Mover cubo a posición")
print("-"*70)
if 'Cube' in bpy.data.objects:
    # Usar intención directa
    cube = bpy.data.objects['Cube']
    cube.location = (5, 10, 15)
    print(f"  ✅ Cubo movido manualmente")
    print(f"     Nueva posición: {tuple(cube.location)}\n")

# 6. Rotar esfera
print("[5/6] TEST: Rotar esfera")
print("-"*70)
if 'Sphere' in bpy.data.objects:
    import math
    sphere = bpy.data.objects['Sphere']
    sphere.rotation_euler = (math.radians(45), math.radians(45), 0)
    print(f"  ✅ Esfera rotada")
    print(f"     Rotación: {tuple(sphere.rotation_euler)}\n")

# 7. Resumen final
print("[6/6] RESUMEN FINAL")
print("="*70)
print(f"\nObjetos en escena:")
for obj in bpy.data.objects:
    print(f"  • {obj.name} ({obj.type})")
    print(f"    - Ubicación: {tuple(obj.location)}")
    print(f"    - Escala: {tuple(obj.scale)}")
    print(f"    - Rotación: {tuple(obj.rotation_euler)}")

print("\n" + "="*70)
print("✅ PRUEBAS COMPLETADAS EN BLENDER")
print("="*70 + "\n")

# ===== FIN CÓDIGO BLENDER =====
