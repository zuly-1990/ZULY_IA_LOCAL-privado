import sys
from pathlib import Path

# Agregar path de ZULY al sys.path
zuly_path = Path("C:/Users/Admin/Desktop/ZULY_IA_LOCAL")
if str(zuly_path) not in sys.path:
    sys.path.insert(0, str(zuly_path))

import bpy
from core.agent import Agent

print("\nAjustando color azul del dado para mejor distinción\n")

# Inicializar Agent con Blender real
agent = Agent(force_mock=False)

# Paso 1: Abrir el archivo modificado
print("Paso 1: Abriendo archivo modificado...")
bpy.ops.wm.open_mainfile(filepath="C:/Users/Admin/Desktop/ZULY_IA_LOCAL/ZULY_PROJECTS/pruebas/zuly_save_20260322_080414.blend")
print("Archivo abierto.")

# Paso 2: Ajustar color azul a uno más vibrante/distinguible
print("Paso 2: Ajustando color azul...")
# Azul más vibrante: RGB [0.0, 0.2, 1.0] o similar
result_color = agent.execute_via_router('blender.set_material_color', {'material_name': 'BlueDot', 'color': [0.0, 0.3, 1.0, 1.0]})  # Azul brillante
print(f"Color ajustado: {result_color}")

# Paso 3: Guardar cambios
print("Paso 3: Guardando cambios...")
result_save = agent.execute_via_router('blender.save_scene', {})
print(f"Escena guardada: {result_save}")

print("Ajuste completado.")