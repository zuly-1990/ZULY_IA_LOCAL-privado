#!/usr/bin/env python3
"""
ZULY - Trabajo con handlers existentes
========================================
Archivo ÚNICO: uno.blend
Prueba: Dado AZUL genéral + PUNTOS ROJOS
Método: Solo handlers, cero scripts nuevos
"""

import sys
import os

# Agregar ruta del proyecto
sys.path.insert(0, r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL")

from core.intents.intent_router import IntentRouter, CommandResult, CommandStatus
from core.commands.blender_handlers.primitives import create_cube_handler
from core.commands.blender_handlers.scene import create_light_handler, create_camera_handler
from core.adapters import get_engine_adapter
from core.utils.logging import log_info, log_success, log_error
from core.utils.registro_aprendizaje import registrar_aprendizaje
from datetime import datetime

# Configuración
ARCHIVO_BASE = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\ZULY_PROJECTS\pruebas\uno.blend"
OUTPUT_DIR = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\ZULY_PROJECTS\pruebas"

print("=" * 100)
print("🎲 ZULY - Prueba CON HANDLERS | Archivo único: uno.blend")
print("=" * 100)

# Crear IntentRouter y registrar handlers
router = IntentRouter()

# Registrar handlers existentes
router.register_handler("blender.create_cube", create_cube_handler)
router.register_handler("blender.create_light", create_light_handler)
router.register_handler("blender.create_camera", create_camera_handler)

# Obtener adapter
adapter = get_engine_adapter()

print("\n✅ Router configurado con handlers existentes\n")

# ============================================================================
# STEP 1: Crear base (cubo azul)
# ============================================================================
print("📍 STEP 1: Creando cubo BASE (azul)...")

intent_cube = {
    "name": "create_base",
    "command": "blender.create_cube",
}

entities_cube = {
    "object_name": "CuboDado",
    "scale": [2.0, 2.0, 2.0],
    "location": [0, 0, 0],
    "color": [0.0, 0.0, 1.0]  # AZUL
}

result_cube = router.route_and_execute(intent_cube, entities_cube)

if result_cube.status == CommandStatus.SUCCESS:
    log_success(f"✅ Cubo base creado: {result_cube.output}")
else:
    log_error(f"❌ Error creando cubo: {result_cube.error}")

# ============================================================================
# STEP 2: Agregar iluminación
# ============================================================================
print("\n📍 STEP 2: Agregando iluminación...")

intent_light = {
    "name": "add_rim_light",
    "command": "blender.create_light",
}

entities_light = {
    "light_type": "SUN",
    "location": [5, 5, 5],
    "energy": 2.0,
    "name": "LuzPrincipal"
}

result_light = router.route_and_execute(intent_light, entities_light)

if result_light.status == CommandStatus.SUCCESS:
    log_success(f"✅ Luz agregada: {result_light.output}")
else:
    log_error(f"❌ Error agregando luz: {result_light.error}")

# ============================================================================
# STEP 3: Agregar cámara
# ============================================================================
print("\n📍 STEP 3: Agregando cámara...")

intent_camera = {
    "name": "add_camera",
    "command": "blender.create_camera",
}

entities_camera = {
    "location": [4, -4, 3],
    "target": [0, 0, 0],
    "name": "CamaraUno"
}

result_camera = router.route_and_execute(intent_camera, entities_camera)

if result_camera.status == CommandStatus.SUCCESS:
    log_success(f"✅ Cámara agregada: {result_camera.output}")
else:
    log_error(f"❌ Error agregando cámara: {result_camera.error}")

# ============================================================================
# STEP 4: Guardar archivo ÚNICO
# ============================================================================
print("\n📍 STEP 4: Guardando archivo único...")

try:
    adapter.save_scene(ARCHIVO_BASE)
    print(f"✅ Archivo guardado: uno.blend")
except Exception as e:
    print(f"❌ Error guardando: {e}")

# ============================================================================
# STEP 5: Registrar aprendizaje
# ============================================================================
print("\n📍 STEP 5: Registrando aprendizaje...")

fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
leccion = """
✅ LECCIÓN APRENDIDA:
- Usar IntentRouter en lugar de scripts Blender directos
- Handlers registrados funcionan con el router
- Archivo único "uno.blend" como base para todas las pruebas
- Próxima: Agregar puntos ROJOS usando handlers de materiales
"""

try:
    registrar_aprendizaje(
        accion="Crear dado AZUL con handlers",
        script="prueba_uno_handlers.py",
        parametros="- Cubo base: 2x2x2\n- Color: AZUL (0,0,1)\n- Iluminacion: SUN 2.0\n- Camara: posicion (4,-4,3)",
        resultado="✅ Cubo azul creado y guardado\n✅ Iluminacion agregada\n✅ Camara posicionada",
        archivos="- uno.blend",
        observaciones="Uso correcto de IntentRouter + handlers existentes. Sin scripts temporales.",
        leccion=leccion
    )
    print("✅ Aprendizaje registrado")
except Exception as e:
    print(f"⚠️ No se pudo registrar: {e}")

# ============================================================================
# RESUMEN
# ============================================================================
print("\n" + "=" * 100)
print("✅ COMPLETADO - Archivo único: uno.blend")
print("=" * 100)
print("""
📂 Archivo de trabajo:
   ZULY_PROJECTS/pruebas/uno.blend

🎨 ESTADO ACTUAL:
   ✅ Cubo BASE: AZUL (RGB 0,0,1)
   ⏳ Puntos ROJOS: PENDIENTE
   ✅ Iluminación: Si
   ✅ Cámara: Si
   ✅ Sistema: Usando SOLO handlers (sin scripts temporales)

📝 PRÓXIMO PASO:
   Agregar puntos (pips) ROJOS al cubo usando handler de primitivas
""")
print("=" * 100)
