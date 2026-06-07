import bpy
import sys
import os

# Rutas oficiales de ZULY
PROJECT_ROOT = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL"
SAVE_PATH = os.path.join(PROJECT_ROOT, "ZULY_PROJECTS", "pruebas", "dado_parques_zuly_v9.blend")

sys.path.insert(0, PROJECT_ROOT)

from core.agent import Agent
from core.utils.logging import log_info, log_success, log_error

def create_parques_dice_v9():
    log_info("=== INICIANDO SÍNTESIS DE DADO DE PARQUÉS ULTRA-CONTRASTE (V9 - COLOR ROJO) ===")
    os.makedirs(os.path.dirname(SAVE_PATH), exist_ok=True)
    agent = Agent(force_mock=False, auto_monitor=True)
    
    # 1. Limpiar escena
    agent.execute_via_router('blender.clear_scene', {})
    
    # 2. Materiales de Contraste (Blanco y Rojo Vibrante)
    agent.execute_via_router('blender.create_material', {'name': 'Die_White', 'color': [0.95, 0.95, 0.95, 1], 'roughness': 0.1, 'specular': 1.0})
    agent.execute_via_router('blender.create_material', {'name': 'Pip_Color', 'color': [1.0, 0.0, 0.0, 1], 'roughness': 0.8, 'specular': 0.5})
    
    # 3. El Dado (Cuerpo Principal con ALTA DENSIDAD)
    agent.execute_via_router('blender.create_cube', {'location': [0, 0, 1], 'scale': 1.0, 'name': 'Parques_Die_Ultra_Color'})
    
    # PRE-CARGAR SLOTS DE MATERIAL
    agent.execute_via_router('blender.run_python_script', {
        'script_content': """
import bpy
obj = bpy.data.objects.get('Parques_Die_Ultra_Color')
mat_white = bpy.data.materials.get('Die_White')
mat_color = bpy.data.materials.get('Pip_Color')
if obj and mat_white and mat_color:
    if len(obj.data.materials) == 0:
        obj.data.materials.append(mat_white)
    else:
        obj.data.materials[0] = mat_white
    # Añadir segundo slot para el color de los puntos
    obj.data.materials.append(mat_color)
"""
    })
    
    # INCREMENTO DE DENSIDAD BASE (Loop Cuts 4x4)
    agent.execute_via_router('blender.run_python_script', {
        'script_content': """
import bpy
obj = bpy.data.objects.get('Parques_Die_Ultra_Color')
if obj:
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.subdivide(number_cuts=4)
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.shade_smooth()
    obj.data.use_auto_smooth = True
    obj.data.auto_smooth_angle = 0.523599
"""
    })

    # 4. Biselado Premium (0.25m / 16 segs)
    agent.execute_via_router('blender.add_bevel', {
        'object_name': 'Parques_Die_Ultra_Color',
        'width': 0.25,
        'segments': 16
    })
    
    # 5. Los Puntos (Pips) - ALTA RESOLUCIÓN Y COLOR FORZADO
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
            pip_name = f"Pip_V9_{face}_{counter}"
            # Crear esfera DE ALTA RESOLUCIÓN via script
            agent.execute_via_router('blender.run_python_script', {
                'script_content': f"""
import bpy
bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=0.18, location={loc})
obj = bpy.context.active_object
obj.name = '{pip_name}'
mat = bpy.data.materials.get('Pip_Color')
if mat:
    if len(obj.data.materials) == 0:
        obj.data.materials.append(mat)
    else:
        obj.data.materials[0] = mat
"""
            })
            
            # CIRUGÍA TÉCNICA DEFINITIVA (Forzando herencia de material)
            agent.execute_via_router('blender.run_python_script', {
                'script_content': f"""
import bpy
obj = bpy.data.objects.get('Parques_Die_Ultra_Color')
cutter = bpy.data.objects.get('{pip_name}')
if obj and cutter:
    bpy.context.view_layer.objects.active = obj
    mod = obj.modifiers.new(name="Cut_V9_{counter}", type='BOOLEAN')
    mod.operation = 'DIFFERENCE'
    mod.object = cutter
    # Forzar uso de materiales del cutter
    mod.material_mode = 'TRANSFER' # Blender lo hace por defecto en 3.6+ si cutter tiene mat
    bpy.ops.object.modifier_apply(modifier=mod.name)
    bpy.data.objects.remove(cutter, do_unlink=True)
"""
            })
            counter += 1

    # 6. Weighted Normals (Cierre técnico final)
    agent.execute_via_router('blender.run_python_script', {
        'script_content': """
import bpy
obj = bpy.data.objects.get('Parques_Die_Ultra_Color')
if obj:
    mod = obj.modifiers.new(name="WN", type='WEIGHTED_NORMAL')
    mod.keep_sharp = True
    bpy.ops.object.modifier_apply(modifier="WN")
"""
    })

    # 7. Guardado Final
    try:
        bpy.ops.wm.save_as_mainfile(filepath=SAVE_PATH)
        log_success(f"=== DADO DE PARQUÉS ULTRA-CONTRASTE V9 COMPLETADO: {SAVE_PATH} ===")
    except Exception as e:
        log_error(f"Error guardando dado V9: {e}")

if __name__ == "__main__":
    create_parques_dice_v9()
