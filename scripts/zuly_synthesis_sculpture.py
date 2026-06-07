import bpy
import sys
import os
import json
import random

# Rutas oficiales de ZULY
PROJECT_ROOT = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL"
SAVE_PATH = os.path.join(PROJECT_ROOT, "ZULY_PROJECTS", "pruebas", "escultura_zuly_v1.blend")

sys.path.insert(0, PROJECT_ROOT)

from core.agent import Agent
from core.utils.logging import log_info, log_success, log_error

def create_sculpture():
    log_info("=== INICIANDO SÍNTESIS URBANA VALIDADA: ESCULTURA V1 ===")
    os.makedirs(os.path.dirname(SAVE_PATH), exist_ok=True)
    agent = Agent(force_mock=False, auto_monitor=True)
    
    # 1. Limpiar escena
    agent.execute_via_router('blender.clear_scene', {})
    
    # 2. Crear composición abstracta
    for i in range(5):
        # Esferas de base
        agent.execute_via_router('blender.create_sphere', {
            'location': [random.uniform(-3, 3), random.uniform(-3, 3), random.uniform(1, 5)],
            'radius': random.uniform(0.5, 2.0)
        })
        # Conos intersecados
        agent.execute_via_router('blender.create_cone', {
            'location': [random.uniform(-4, 4), random.uniform(-4, 4), random.uniform(1, 6)],
            'radius1': random.uniform(0.8, 1.5),
            'depth': random.uniform(2, 5)
        })

    # 3. Añadir un "Sol" para sombras dramáticas
    agent.execute_via_router('blender.create_light', {'light_type': 'SUN', 'energy': 5.0})
    
    # 4. VALIDACIÓN V3 (Muestreo de un objeto al azar)
    all_meshes = [obj.name for obj in bpy.data.objects if obj.type == 'MESH']
    if all_meshes:
        log_info(f"Validando integridad de la pieza: {all_meshes[0]}")
        agent.execute_via_router('blender.validate_topology', {'object_name': all_meshes[0]})

    # 5. Guardado Final
    try:
        bpy.ops.wm.save_as_mainfile(filepath=SAVE_PATH)
        log_success(f"=== ESCULTURA COMPLETADA: {SAVE_PATH} ===")
    except Exception as e:
        log_error(f"Error al guardar escultura: {e}")

if __name__ == "__main__":
    # Seed fija para "repetibilidad" en esta prueba
    random.seed(42)
    create_sculpture()
