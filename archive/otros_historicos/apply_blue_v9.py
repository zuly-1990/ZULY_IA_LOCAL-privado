import sys
from pathlib import Path

# Agregar path de ZULY al sys.path
zuly_path = Path("C:/Users/Admin/Desktop/ZULY_IA_LOCAL")
if str(zuly_path) not in sys.path:
    sys.path.insert(0, str(zuly_path))

import bpy
from core.agent import Agent

print("\nAplicando material azul al objeto principal del dado v9\n")

# Inicializar Agent con Blender real
agent = Agent(force_mock=False)

# Paso 1: Abrir el archivo guardado
print("Paso 1: Abriendo archivo guardado...")
bpy.ops.wm.open_mainfile(filepath="C:/Users/Admin/Desktop/ZULY_IA_LOCAL/ZULY_PROJECTS/zuly_save_20260322_080236.blend")
print("Archivo abierto.")

# Paso 2: Crear material azul (por si no existe)
print("Paso 2: Creando material azul...")
result_mat = agent.execute_via_router('blender.create_material', {'name': 'BlueDot'})
result_color = agent.execute_via_router('blender.set_material_color', {'material_name': 'BlueDot', 'color': [0.0, 0.0, 1.0, 1.0]})
print(f"Material azul: {result_mat}, color: {result_color}")

# Paso 3: Aplicar material azul al objeto principal
print("Paso 3: Aplicando material azul...")
obj_name = "Parques_Die_Ultra_Color"
result_apply = agent.execute_via_router('blender.apply_material', {'object_name': obj_name, 'material_name': 'BlueDot'})
print(f"Material aplicado a {obj_name}: {result_apply}")

# Paso 4: Guardar cambios
print("Paso 4: Guardando cambios...")
result_save = agent.execute_via_router('blender.save_scene', {})
print(f"Escena guardada: {result_save}")

print("Aplicación completada.")