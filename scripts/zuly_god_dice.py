import bpy
import sys
import os
import json

# Rutas oficiales de ZULY
PROJECT_ROOT = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL"
SAVE_PATH = os.path.join(PROJECT_ROOT, "ZULY_PROJECTS", "pruebas", "dados_reales_zuly_v3.blend")

sys.path.insert(0, PROJECT_ROOT)

from core.agent import Agent
from core.utils.logging import log_info, log_success, log_error, log_warning

def create_god_dice():
    log_info("=== INICIANDO SÍNTESIS DE DADOS NIVEL DIOS (V3) ===")
    os.makedirs(os.path.dirname(SAVE_PATH), exist_ok=True)
    agent = Agent(force_mock=False, auto_monitor=True)
    
    # 1. Limpiar escena
    agent.execute_via_router('blender.clear_scene', {})
    
    # 2. El Dado (Cuerpo Principal)
    agent.execute_via_router('blender.create_cube', {'location': [0, 0, 1], 'scale': 1.0})
    agent.execute_via_router('blender.rename_object', {'old_name': 'Cube', 'new_name': 'Die_Body'})
    
    # ACTIVAR AUTO-SMOOTH (El secreto de la suavidad industrial)
    agent.execute_via_router('blender.run_python_script', {
        'script_content': """
import bpy
obj = bpy.data.objects.get('Die_Body')
if obj:
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.shade_smooth()
    obj.data.use_auto_smooth = True
    obj.data.auto_smooth_angle = 0.523599 # 30 grados
"""
    })

    # 3. Biselado profundo (0.2m para curvas más orgánicas)
    agent.execute_via_router('blender.add_bevel', {
        'object_name': 'Die_Body',
        'width': 0.2,
        'segments': 12
    })
    
    # 4. Los Puntos (Pips) - Mapa completo de 6 caras
    pips_map = [
        # Cara 1 (Top)
        [0, 0, 2.0],
        # Cara 6 (Bottom)
        [0.5, 0.5, 0], [0.5, -0.5, 0], [-0.5, 0.5, 0], [-0.5, -0.5, 0], [0.5, 0, 0], [-0.5, 0, 0],
        # Cara 2 (Front)
        [0.5, -1, 1.5], [-0.5, -1, 0.5],
        # Cara 5 (Back)
        [0.5, 1, 1.5], [-0.5, 1, 0.5], [0.5, 1, 0.5], [-0.5, 1, 1.5], [0, 1, 1],
        # Cara 3 (Right)
        [1, 0.5, 1.5], [1, 0, 1], [1, -0.5, 0.5],
        # Cara 4 (Left)
        [-1, 0.5, 1.5], [-1, 0.5, 0.5], [-1, -0.5, 1.5], [-1, -0.5, 0.5]
    ]
    
    for i, loc in enumerate(pips_map):
        agent.execute_via_router('blender.create_sphere', {
            'location': loc,
            'radius': 0.18
        })
        # Booleano Sustractivo
        agent.execute_via_router('blender.add_boolean', {
            'object_name': 'Die_Body',
            'target_name': 'Sphere',
            'operation': 'DIFFERENCE'
        })
        agent.execute_via_router('blender.delete_object', {'object_name': 'Sphere'})

    # 5. Modificador Weighted Normal (Cura final para sombras sueltas)
    agent.execute_via_router('blender.run_python_script', {
        'script_content': """
import bpy
obj = bpy.data.objects.get('Die_Body')
if obj:
    mod = obj.modifiers.new(name="WeightedNormal", type='WEIGHTED_NORMAL')
    mod.keep_sharp = True
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.modifier_apply(modifier="WeightedNormal") # Opcional, pero mejor dejarlo activo
"""
    })

    # 6. Material y Luces
    agent.execute_via_router('blender.create_material', {
        'name': 'Premium_Plastic',
        'color': [1, 1, 1, 1],
        'roughness': 0.02,
        'specular': 1.0
    })
    agent.execute_via_router('blender.apply_material', {
        'object_name': 'Die_Body',
        'material_name': 'Premium_Plastic'
    })
    
    agent.execute_via_router('blender.create_light', {'light_type': 'POINT', 'location': [3, -3, 5], 'energy': 500})
    agent.execute_via_router('blender.create_camera', {'location': [4, -4, 4]})

    # 7. Guardado
    try:
        bpy.ops.wm.save_as_mainfile(filepath=SAVE_PATH)
        log_success(f"=== DADOS NIVEL DIOS V3 COMPLETADOS: {SAVE_PATH} ===")
    except Exception as e:
        log_error(f"Error al guardar dados V3: {e}")

if __name__ == "__main__":
    create_god_dice()
