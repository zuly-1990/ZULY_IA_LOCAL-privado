import bpy
import sys
import os

# Rutas oficiales de ZULY
PROJECT_ROOT = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL"
SAVE_PATH = os.path.join(PROJECT_ROOT, "ZULY_PROJECTS", "pruebas", "dado_parques_zuly_v7.blend")

sys.path.insert(0, PROJECT_ROOT)

from core.agent import Agent
from core.utils.logging import log_info, log_success, log_error

def create_parques_dice_v7():
    log_info("=== INICIANDO SÍNTESIS DE DADO DE PARQUÉS REAL (V7 - HUECOS FÍSICOS) ===")
    os.makedirs(os.path.dirname(SAVE_PATH), exist_ok=True)
    agent = Agent(force_mock=False, auto_monitor=True)
    
    # 1. Limpiar escena
    agent.execute_via_router('blender.clear_scene', {})
    
    # 2. Materiales de Contraste
    agent.execute_via_router('blender.create_material', {'name': 'Die_White', 'color': [0.95, 0.95, 0.95, 1], 'roughness': 0.1, 'specular': 1.0})
    agent.execute_via_router('blender.create_material', {'name': 'Pip_Black', 'color': [0.0, 0.0, 0.0, 1], 'roughness': 0.9, 'specular': 0.0})
    
    # 3. El Dado (Cuerpo Principal)
    agent.execute_via_router('blender.create_cube', {'location': [0, 0, 1], 'scale': 1.0, 'name': 'Parques_Die_Real'})
    agent.execute_via_router('blender.apply_material', {'object_name': 'Parques_Die_Real', 'material_name': 'Die_White'})
    
    # SUAVIZADO INDUSTRIAL V7
    agent.execute_via_router('blender.run_python_script', {
        'script_content': """
import bpy
obj = bpy.data.objects.get('Parques_Die_Real')
if obj:
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.shade_smooth()
    obj.data.use_auto_smooth = True
    obj.data.auto_smooth_angle = 0.523599
"""
    })

    # 4. Biselado Premium (0.25m / 16 segs)
    agent.execute_via_router('blender.add_bevel', {
        'object_name': 'Parques_Die_Real',
        'width': 0.25,
        'segments': 16
    })
    
    # 5. Los Puntos (Pips) - Mapa de 21 puntos con APLICACIÓN DEFINITIVA
    # Ajustamos profundidad (locs slightly center-ward)
    pips_map = {
        'F1': [[0, 0, 1.95]],
        'F2': [[0.5, -0.95, 1.5], [-0.5, -0.95, 0.5]],
        'F3': [[0.95, 0.5, 1.5], [0.95, 0, 1], [0.95, -0.5, 0.5]],
        'F4': [[-0.95, 0.5, 1.5], [-0.95, 0.5, 0.5], [-0.95, -0.5, 1.5], [-0.95, -0.5, 0.5]],
        'F5': [[0.5, 0.95, 1.5], [-0.5, 0.95, 0.5], [0.5, 0.95, 0.5], [-0.5, 0.95, 1.5], [0, 0.95, 1]],
        'F6': [[0.5, 0.5, 0.05], [0.5, -0.5, 0.05], [-0.5, 0.5, 0.05], [-0.5, -0.5, 0.05], [0.5, 0, 0.05], [-0.5, 0, 0.05]]
    }
    
    counter = 0
    for face, locs in pips_map.items():
        for loc in locs:
            pip_name = f"Pip_Temp_{face}_{counter}"
            # Crear esfera operando
            agent.execute_via_router('blender.create_sphere', {
                'location': loc,
                'radius': 0.18,
                'name': pip_name
            })
            
            # ASIGNAR MATERIAL NEGRO
            agent.execute_via_router('blender.apply_material', {
                'object_name': pip_name,
                'material_name': 'Pip_Black'
            })
            
            # CIRUGÍA TÉCNICA: Booleano -> Aplicar -> Borrar
            # Usamos script para asegurar la aplicación
            agent.execute_via_router('blender.run_python_script', {
                'script_content': f"""
import bpy
obj = bpy.data.objects.get('Parques_Die_Real')
cutter = bpy.data.objects.get('{pip_name}')
if obj and cutter:
    bpy.context.view_layer.objects.active = obj
    mod = obj.modifiers.new(name="Cut_{counter}", type='BOOLEAN')
    mod.operation = 'DIFFERENCE'
    mod.object = cutter
    bpy.ops.object.modifier_apply(modifier=mod.name)
    # Borrar el cortador
    bpy.data.objects.remove(cutter, do_unlink=True)
"""
            })
            counter += 1

    # 6. Weighted Normals (Cierre técnico final)
    agent.execute_via_router('blender.run_python_script', {
        'script_content': """
import bpy
obj = bpy.data.objects.get('Parques_Die_Real')
if obj:
    mod = obj.modifiers.new(name="WN", type='WEIGHTED_NORMAL')
    mod.keep_sharp = True
    bpy.ops.object.modifier_apply(modifier="WN")
"""
    })

    # 7. Guardado Final
    try:
        bpy.ops.wm.save_as_mainfile(filepath=SAVE_PATH)
        log_success(f"=== DADO DE PARQUÉS REAL V7 COMPLETADO: {SAVE_PATH} ===")
    except Exception as e:
        log_error(f"Error guardando dado V7: {e}")

if __name__ == "__main__":
    create_parques_dice_v7()
