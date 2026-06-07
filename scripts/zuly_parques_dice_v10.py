import bpy
import sys
import os

# Rutas oficiales de ZULY
PROJECT_ROOT = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL"
SAVE_PATH = os.path.join(PROJECT_ROOT, "ZULY_PROJECTS", "pruebas", "dado_parques_zuly_v10.blend")

sys.path.insert(0, PROJECT_ROOT)

from core.agent import Agent
from core.utils.logging import log_info, log_success, log_error

def create_parques_dice_v10():
    log_info("=== INICIANDO SÍNTESIS DE DADO DE PARQUÉS MULTI-COLOR (V10) ===")
    os.makedirs(os.path.dirname(SAVE_PATH), exist_ok=True)
    agent = Agent(force_mock=False, auto_monitor=True)
    
    # 1. Limpiar escena
    agent.execute_via_router('blender.clear_scene', {})
    
    # 2. Material Principal Blanco
    agent.execute_via_router('blender.create_material', {'name': 'Die_White', 'color': [0.95, 0.95, 0.95, 1], 'roughness': 0.1, 'specular': 1.0})
    
    # 3. Colores por Cara
    colors_map = {
        'F1': ('Pip_Red', [1.0, 0.0, 0.0, 1]),
        'F2': ('Pip_Blue', [0.0, 0.0, 1.0, 1]),
        'F3': ('Pip_Green', [0.0, 1.0, 0.0, 1]),
        'F4': ('Pip_Yellow', [1.0, 0.8, 0.0, 1]),
        'F5': ('Pip_Orange', [1.0, 0.4, 0.0, 1]),
        'F6': ('Pip_Purple', [0.6, 0.0, 0.8, 1])
    }
    
    for mat_name, rgba in colors_map.values():
        agent.execute_via_router('blender.create_material', {'name': mat_name, 'color': rgba, 'roughness': 0.8, 'specular': 0.5})

    # 4. El Dado (Cuerpo Principal con ALTA DENSIDAD)
    agent.execute_via_router('blender.create_cube', {'location': [0, 0, 1], 'scale': 1.0, 'name': 'Parques_Die_V10'})
    
    # PRE-CARGAR SLOTS DE MATERIAL (1 Blanco + 6 Colores)
    script_preload = """
import bpy
obj = bpy.data.objects.get('Parques_Die_V10')
mat_white = bpy.data.materials.get('Die_White')

if obj and mat_white:
    if len(obj.data.materials) == 0:
        obj.data.materials.append(mat_white)
    else:
        obj.data.materials[0] = mat_white

    # Añadir los 6 materiales de colores
    mats_to_add = ['Pip_Red', 'Pip_Blue', 'Pip_Green', 'Pip_Yellow', 'Pip_Orange', 'Pip_Purple']
    for m in mats_to_add:
        c_mat = bpy.data.materials.get(m)
        if c_mat:
            obj.data.materials.append(c_mat)
"""
    agent.execute_via_router('blender.run_python_script', {'script_content': script_preload})
    
    # INCREMENTO DE DENSIDAD BASE (Loop Cuts 4x4)
    script_subdiv = """
import bpy
obj = bpy.data.objects.get('Parques_Die_V10')
if obj:
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.subdivide(number_cuts=4)
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.shade_smooth()
    obj.data.use_auto_smooth = True
    obj.data.auto_smooth_angle = 0.523599
"""
    agent.execute_via_router('blender.run_python_script', {'script_content': script_subdiv})

    # 5. Biselado Premium (0.25m / 16 segs)
    agent.execute_via_router('blender.add_bevel', {
        'object_name': 'Parques_Die_V10',
        'width': 0.25,
        'segments': 16
    })
    
    # 6. Los Puntos (Pips) - ALTA RESOLUCIÓN Y COLOR FORZADO
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
        # Identificar material de esta cara
        face_material_name = colors_map[face][0]
        
        for loc in locs:
            pip_name = f"Pip_V10_{face}_{counter}"
            # Crear esfera DE ALTA RESOLUCIÓN via script y ponerle material
            script_create_pip = f"""
import bpy
bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=0.18, location={loc})
obj = bpy.context.active_object
obj.name = '{pip_name}'
mat = bpy.data.materials.get('{face_material_name}')
if mat:
    if len(obj.data.materials) == 0:
        obj.data.materials.append(mat)
    else:
        obj.data.materials[0] = mat
"""
            agent.execute_via_router('blender.run_python_script', {'script_content': script_create_pip})
            
            # CIRUGÍA TÉCNICA DEFINITIVA (Forzando herencia de material)
            script_boolean = f"""
import bpy
obj = bpy.data.objects.get('Parques_Die_V10')
cutter = bpy.data.objects.get('{pip_name}')
if obj and cutter:
    bpy.context.view_layer.objects.active = obj
    mod = obj.modifiers.new(name="Cut_V10_{counter}", type='BOOLEAN')
    mod.operation = 'DIFFERENCE'
    mod.object = cutter
    mod.material_mode = 'TRANSFER'  # Asigna el slot correcto de V10
    bpy.ops.object.modifier_apply(modifier=mod.name)
    bpy.data.objects.remove(cutter, do_unlink=True)
"""
            agent.execute_via_router('blender.run_python_script', {'script_content': script_boolean})
            counter += 1

    # 7. Weighted Normals (Cierre técnico final)
    script_wn = """
import bpy
obj = bpy.data.objects.get('Parques_Die_V10')
if obj:
    mod = obj.modifiers.new(name="WN", type='WEIGHTED_NORMAL')
    mod.keep_sharp = True
    bpy.ops.object.modifier_apply(modifier="WN")
"""
    agent.execute_via_router('blender.run_python_script', {'script_content': script_wn})

    # 8. Guardado Final
    try:
        bpy.ops.wm.save_as_mainfile(filepath=SAVE_PATH)
        log_success(f"=== DADO DE PARQUÉS MULTI-COLOR V10 COMPLETADO: {SAVE_PATH} ===")
    except Exception as e:
        log_error(f"Error guardando dado V10: {e}")

if __name__ == "__main__":
    create_parques_dice_v10()
