import bpy
import sys
import os

# Rutas oficiales de ZULY
PROJECT_ROOT = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL"
SAVE_PATH = os.path.join(PROJECT_ROOT, "ZULY_PROJECTS", "pruebas", "dado_parques_zuly_v5.blend")

sys.path.insert(0, PROJECT_ROOT)

from core.agent import Agent
from core.utils.logging import log_info, log_success, log_error

def create_parques_dice_v5():
    log_info("=== INICIANDO SÍNTESIS DE DADO DE PARQUÉS (V5 - CORRECCIÓN CRÍTICA) ===")
    os.makedirs(os.path.dirname(SAVE_PATH), exist_ok=True)
    agent = Agent(force_mock=False, auto_monitor=True)
    
    # 1. Limpiar escena
    agent.execute_via_router('blender.clear_scene', {})
    
    # 2. El Dado (Cuerpo Principal)
    agent.execute_via_router('blender.create_cube', {'location': [0, 0, 1], 'scale': 1.0, 'name': 'Parques_Die'})
    
    # SUAVIZADO INDUSTRIAL V5
    agent.execute_via_router('blender.run_python_script', {
        'script_content': """
import bpy
obj = bpy.data.objects.get('Parques_Die')
if obj:
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.shade_smooth()
    obj.data.use_auto_smooth = True
    obj.data.auto_smooth_angle = 0.523599
"""
    })

    # 3. Biselado Premium (0.25m / 16 segs)
    agent.execute_via_router('blender.add_bevel', {
        'object_name': 'Parques_Die',
        'width': 0.25,
        'segments': 16
    })
    
    # 4. Los Puntos (Pips) - Mapa de 21 puntos
    pips_map = {
        'F1': [[0, 0, 2.0]],
        'F2': [[0.5, -1, 1.5], [-0.5, -1, 0.5]],
        'F3': [[1, 0.5, 1.5], [1, 0, 1], [1, -0.5, 0.5]],
        'F4': [[-1, 0.5, 1.5], [-1, 0.5, 0.5], [-1, -0.5, 1.5], [-1, -0.5, 0.5]],
        'F5': [[0.5, 1, 1.5], [-0.5, 1, 0.5], [0.5, 1, 0.5], [-0.5, 1, 1.5], [0, 1, 1]],
        'F6': [[0.5, 0.5, 0], [0.5, -0.5, 0], [-0.5, 0.5, 0], [-0.5, -0.5, 0], [0.5, 0, 0], [-0.5, 0, 0]]
    }
    
    # Materiales
    agent.execute_via_router('blender.create_material', {'name': 'Die_White', 'color': [1, 1, 1, 1], 'roughness': 0.1})
    agent.execute_via_router('blender.apply_material', {'object_name': 'Parques_Die', 'material_name': 'Die_White'})

    # Procesar Pips individualmente
    counter = 0
    for face, locs in pips_map.items():
        for loc in locs:
            pip_name = f"Pip_{face}_{counter}"
            agent.execute_via_router('blender.create_sphere', {
                'location': loc,
                'radius': 0.18,
                'name': pip_name
            })
            
            # BOOLEAN CORREGIDO: Usando 'operand_object' y NO borrando el objeto
            agent.execute_via_router('blender.add_boolean', {
                'object_name': 'Parques_Die',
                'operand_object': pip_name,
                'operation': 'DIFFERENCE',
                'hide_operand': True
            })
            counter += 1

    # 5. Weighted Normals (Cierre técnico)
    agent.execute_via_router('blender.run_python_script', {
        'script_content': """
import bpy
obj = bpy.data.objects.get('Parques_Die')
if obj:
    mod = obj.modifiers.new(name="WN", type='WEIGHTED_NORMAL')
    mod.keep_sharp = True
"""
    })

    # 6. Guardado Final
    try:
        bpy.ops.wm.save_as_mainfile(filepath=SAVE_PATH)
        log_success(f"=== DADO DE PARQUÉS V5 COMPLETADO: {SAVE_PATH} ===")
    except Exception as e:
        log_error(f"Error guardando dado V5: {e}")

if __name__ == "__main__":
    create_parques_dice_v5()
