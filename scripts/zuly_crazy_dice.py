import bpy
import sys
import os
import math

# Rutas oficiales de ZULY
PROJECT_ROOT = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL"
SAVE_PATH = os.path.join(PROJECT_ROOT, "ZULY_PROJECTS", "pruebas", "dado_parques_crazy_cut.blend")

sys.path.insert(0, PROJECT_ROOT)

from core.agent import Agent
from core.utils.logging import log_info, log_success, log_error

def create_crazy_dice_scene():
    log_info("=== INICIANDO EXPERIMENTO LOCO: EL GRAN CORTE TRANSVERSAL ===")
    os.makedirs(os.path.dirname(SAVE_PATH), exist_ok=True)
    agent = Agent(force_mock=False, auto_monitor=True)
    
    # 1. Limpiar escena
    agent.execute_via_router('blender.clear_scene', {})
    
    # 2. Materiales Base de Dados
    mat_white = {'name': 'Body_White', 'color': [0.95, 0.95, 0.95, 1], 'roughness': 0.1, 'specular': 1.0}
    mat_black = {'name': 'Body_Black', 'color': [0.02, 0.02, 0.02, 1], 'roughness': 0.1, 'specular': 1.0}
    mat_gold  = {'name': 'Body_Gold',  'color': [0.8, 0.5, 0.1, 1], 'roughness': 0.2, 'specular': 1.0}
    
    # Crear oro usando script para metallic
    agent.execute_via_router('blender.create_material', mat_white)
    agent.execute_via_router('blender.create_material', mat_black)
    agent.execute_via_router('blender.run_python_script', {'script_content': """
import bpy
mat = bpy.data.materials.new(name="Body_Gold")
mat.use_nodes = True
bsdf = mat.node_tree.nodes.get('Principled BSDF')
if bsdf:
    bsdf.inputs['Base Color'].default_value = (1.0, 0.766, 0.336, 1.0)
    bsdf.inputs['Metallic'].default_value = 1.0
    bsdf.inputs['Roughness'].default_value = 0.2
"""})

    # 3. Material Neon Slicer
    agent.execute_via_router('blender.run_python_script', {'script_content': """
import bpy
mat = bpy.data.materials.new(name="Cut_Neon")
mat.use_nodes = True
bsdf = mat.node_tree.nodes.get('Principled BSDF')
if bsdf:
    bsdf.inputs['Emission'].default_value = (0.0, 0.8, 1.0, 1.0)  # Cyan Neon
    bsdf.inputs['Emission Strength'].default_value = 5.0
"""})

    # 4. Colores de Pips por Cara (V10)
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

    # FUNCIÓN PARA CREAR UN DADO
    pips_map = {
        'F1': [[0, 0, 1.95]],
        'F2': [[0.5, -0.95, 1.5], [-0.5, -0.95, 0.5]],
        'F3': [[0.95, 0.5, 1.5], [0.95, 0, 1], [0.95, -0.5, 0.5]],
        'F4': [[-0.95, 0.5, 1.5], [-0.95, 0.5, 0.5], [-0.95, -0.5, 1.5], [-0.95, -0.5, 0.5]],
        'F5': [[0.5, 0.95, 1.5], [-0.5, 0.95, 0.5], [0.5, 0.95, 0.5], [-0.5, 0.95, 1.5], [0, 0.95, 1]],
        'F6': [[0.5, 0.5, 0.05], [0.5, -0.5, 0.05], [-0.5, 0.5, 0.05], [-0.5, -0.5, 0.05], [0.5, 0, 0.05], [-0.5, 0, 0.05]]
    }

    def build_dice(name, body_mat, loc, rot):
        # 4.1 Cubo Base en origen
        agent.execute_via_router('blender.create_cube', {'location': [0, 0, 1], 'scale': 1.0, 'name': name})
        
        # 4.2 Materiales y Subdivisión
        script_setup = f"""
import bpy
obj = bpy.data.objects.get('{name}')
mat_body = bpy.data.materials.get('{body_mat}')
if obj and mat_body:
    obj.data.materials.append(mat_body)
    mats_to_add = ['Pip_Red', 'Pip_Blue', 'Pip_Green', 'Pip_Yellow', 'Pip_Orange', 'Pip_Purple']
    for m in mats_to_add:
        c_mat = bpy.data.materials.get(m)
        if c_mat:
            obj.data.materials.append(c_mat)
            
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.subdivide(number_cuts=4)
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.shade_smooth()
    obj.data.use_auto_smooth = True
    obj.data.auto_smooth_angle = 0.523599
"""
        agent.execute_via_router('blender.run_python_script', {'script_content': script_setup})
        
        # 4.3 Bevel
        agent.execute_via_router('blender.add_bevel', {'object_name': name, 'width': 0.25, 'segments': 16})
        
        # 4.4 Cortar Pips V10
        counter = 0
        for face, locs in pips_map.items():
            face_material_name = colors_map[face][0]
            for p_loc in locs:
                pip_name = f"Pip_{name}_{counter}"
                script_pip = f"""
import bpy
bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=0.18, location={p_loc})
cutter = bpy.context.active_object
cutter.name = '{pip_name}'
mat = bpy.data.materials.get('{face_material_name}')
if mat:
    cutter.data.materials.append(mat)
    
obj = bpy.data.objects.get('{name}')
if obj:
    bpy.context.view_layer.objects.active = obj
    mod = obj.modifiers.new(name="Cut_{counter}", type='BOOLEAN')
    mod.operation = 'DIFFERENCE'
    mod.object = cutter
    mod.material_mode = 'TRANSFER'
    bpy.ops.object.modifier_apply(modifier=mod.name)
    bpy.data.objects.remove(cutter, do_unlink=True)
"""
                agent.execute_via_router('blender.run_python_script', {'script_content': script_pip})
                counter += 1

        # 4.5 Weighted Normals
        agent.execute_via_router('blender.run_python_script', {'script_content': f"""
import bpy
obj = bpy.data.objects.get('{name}')
if obj:
    mod = obj.modifiers.new(name="WN", type='WEIGHTED_NORMAL')
    mod.keep_sharp = True
    bpy.ops.object.modifier_apply(modifier="WN")
"""})
        
        # 4.6 Mover y Rotar (a su posición final)
        agent.execute_via_router('blender.move_object', {'object_name': name, 'location': loc})
        agent.execute_via_router('blender.rotate_object', {'object_name': name, 'rotation': rot})

    # 5. CONSTRUCCIÓN DE LOS 3 DADOS
    build_dice('Die_1_White', 'Body_White', [-3, 0, 1], [0, 0, math.radians(45)])
    build_dice('Die_2_Black', 'Body_Black', [0, 0, 1], [math.radians(90), 0, math.radians(15)])
    build_dice('Die_3_Gold', 'Body_Gold', [3, 0, 1], [math.radians(180), 0, math.radians(-30)])

    # 6. EL GRAN CORTE TRANSVERSAL (La Navaja Neón)
    script_slicer = """
import bpy
# Crear cubo gigante en Y negativo
bpy.ops.mesh.primitive_cube_add(location=[0, -5.5, 1], scale=[10, 5, 5])
slicer = bpy.context.active_object
slicer.name = 'Giant_Slicer'

# Material Neón
mat_neon = bpy.data.materials.get('Cut_Neon')
if mat_neon:
    slicer.data.materials.append(mat_neon)

dice_names = ['Die_1_White', 'Die_2_Black', 'Die_3_Gold']
for die_name in dice_names:
    die = bpy.data.objects.get(die_name)
    if die:
        # Añadir material neon al dado antes de cortar
        if mat_neon.name not in [m.name for m in die.data.materials if m]:
            die.data.materials.append(mat_neon)
            
        bpy.context.view_layer.objects.active = die
        mod = die.modifiers.new(name="TRANSVERSAL_CUT", type='BOOLEAN')
        mod.operation = 'DIFFERENCE'
        mod.object = slicer
        mod.material_mode = 'TRANSFER'
        bpy.ops.object.modifier_apply(modifier=mod.name)

# Remover Navaja
bpy.data.objects.remove(slicer, do_unlink=True)
"""
    agent.execute_via_router('blender.run_python_script', {'script_content': script_slicer})

    # 7. Add ground and lighting to appreciate
    agent.execute_via_router('blender.run_python_script', {'script_content': """
import bpy
bpy.ops.mesh.primitive_plane_add(size=20, location=(0,0,0))
bpy.context.active_object.name = 'Studio_Floor'
mat_floor = bpy.data.materials.new(name="Dark_Floor")
mat_floor.use_nodes = True
mat_floor.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = (0.05, 0.05, 0.05, 1)
mat_floor.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value = 0.2
bpy.context.active_object.data.materials.append(mat_floor)

# Lights
bpy.ops.object.light_add(type='AREA', location=(0, -3, 5), rotation=(0.5, 0, 0))
bpy.context.active_object.data.energy = 500
bpy.context.active_object.data.size = 10
bpy.ops.object.light_add(type='AREA', location=(0, 3, 5), rotation=(-0.5, 0, 0))
bpy.context.active_object.data.energy = 200
bpy.context.active_object.data.size = 10
"""})

    # 8. Guardar
    try:
        bpy.ops.wm.save_as_mainfile(filepath=SAVE_PATH)
        log_success(f"=== EXPERIMENTO COMPLETADO: {SAVE_PATH} ===")
    except Exception as e:
        log_error(f"Error guardando scene: {e}")

if __name__ == "__main__":
    create_crazy_dice_scene()
