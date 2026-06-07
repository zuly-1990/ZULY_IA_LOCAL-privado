import sys
import os

# Rutas oficiales de ZULY
PROJECT_ROOT = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL"
SAVE_PATH = os.path.join(PROJECT_ROOT, "ZULY_PROJECTS", "pruebas", "dado_parques_handler_test.blend")

sys.path.insert(0, PROJECT_ROOT)

from core.agent import Agent
from core.utils.logging import log_info, log_success, log_error
import bpy

def test_dice_handler():
    log_info("=== INICIANDO PRUEBA DE HANDLER: DADO DE PARQUÉS V9 ===")
    os.makedirs(os.path.dirname(SAVE_PATH), exist_ok=True)
    agent = Agent(force_mock=False, auto_monitor=True)
    
    agent.execute_via_router('blender.clear_scene', {})
    
    # Ejecutamos el handler nativo:
    result = agent.execute_via_router('blender.create_parques_dice', {})
    
    if result and result.get('success'):
        log_success("Handler ejecutado con éxito.")
    else:
        log_error(f"Fallo en execution del handler: {result}")
        
    try:
        bpy.ops.wm.save_as_mainfile(filepath=SAVE_PATH)
        log_success(f"=== PRUEBA DE HANDLER COMPLETADA: {SAVE_PATH} ===")
    except Exception as e:
        log_error(f"Error guardando scene: {e}")

if __name__ == "__main__":
    test_dice_handler()
    
