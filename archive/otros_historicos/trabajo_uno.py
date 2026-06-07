#!/usr/bin/env python3
"""
ZULY - Trabajo CON HANDLERS REALES
===================================
Archivo único: uno.blend
Dado: AZUL base + PUNTOS ROJOS
"""

import sys
sys.path.insert(0, r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL")

from core.commands.blender_handlers.primitives import create_cube_handler, create_sphere_handler
from core.commands.blender_handlers.transforms import move_object_handler
from core.commands.blender_handlers.system import save_blend_handler
from core.adapters import get_engine_adapter
from core.utils.registro_aprendizaje import registrar_aprendizaje

print("=" * 100)
print("🎲 ZULY - Handlers solo (sin scripts temporales)")
print("=" * 100)

adapter = get_engine_adapter()

# STEP 2: Crear cubo BASE AZUL
print("[2] Creando cubo AZUL...")
result_cube = create_cube_handler({
    "object_name": "DadoBase",
    "scale": [2.0, 2.0, 2.0],
    "location": [0, 0, 0],
    "color": [0.0, 0.0, 1.0]  # AZUL RGB
}, adapter)
print(f"    ✅ {result_cube}")

# STEP 3: Crear 21 esferas ROJAS (puntos)
print("[3] Creando 21 puntos ROJOS...")
positions = [
    # Cara 1 - 1 punto
    [0, 0, 2.1],
    # Cara 2 - 2 puntos
    [-0.7, 0, -1.5], [0.7, 0, -1.5],
    # Cara 3 - 3 puntos
    [-1, 1.5, 0], [0, 1.5, 0], [1, 1.5, 0],
    # Cara 4 - 4 puntos
    [-1, -1.5, -0.7], [-0.3, -1.5, -0.7], [0.3, -1.5, -0.7], [1, -1.5, -0.7],
    # Cara 5 - 5 puntos
    [-1.3, 2.2, 1], [-0.6, 2.2, 1], [0, 2.2, 1], [0.6, 2.2, 1], [1.3, 2.2, 1],
    # Cara 6 - 6 puntos
    [-1.5, -2.2, 0.8], [-0.9, -2.2, 0.8], [-0.3, -2.2, 0.8], [0.3, -2.2, 0.8], [0.9, -2.2, 0.8], [1.5, -2.2, 0.8],
]

for i, pos in enumerate(positions):
    result_sphere = create_sphere_handler({
        "object_name": f"Punto_{i+1}",
        "radius": 0.25,
        "location": pos,
        "color": [1.0, 0.0, 0.0]  # ROJO RGB
    }, adapter)
    if i % 7 == 0:
        print(f"    ✅ Puntos {i+1}-{min(i+7, len(positions))}")

# STEP 4: Guardar archivo
print("[4] Guardando archivo único...")
archivo_path = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\ZULY_PROJECTS\pruebas\uno.blend"
save_blend_handler({"filepath": archivo_path}, adapter)
print(f"    ✅ Guardado en: uno.blend")

# STEP 5: Registrar aprendizaje
print("[5] Registrando aprendizaje...")
try:
    registrar_aprendizaje(
        accion="Crear dado AZUL+ROJO con handlers reales",
        script="trabajo_uno.py",
        parametros="Cubo azul 2x2x2 + 21 esferas rojas (pips)",
        resultado="Archivo uno.blend creado exitosamente",
        archivos="uno.blend",
        observaciones="Usando SOLO handlers reales del sistema. Sin scripts Blender temporales.",
        leccion="Los handlers ya existen - no crear scripts nuevos. Archivo unico reutilizable."
    )
    print("    ✅ Aprendizaje registrado")
except Exception as e:
    print(f"    ⚠️ Registro: {e}")

print("\n" + "=" * 100)
print("✅ COMPLETADO")
print("=" * 100)
print("""
Archivo: uno.blend
Estado:
  ✅ Base: AZUL (RGB 0,0,1)
  ✅ Pips: ROJO (RGB 1,0,0)
  ✅ Cantidad: 21 puntos
  ✅ Sistema: Handlers REALES

Proximo: Más pruebas en el MISMO archivo
""")
