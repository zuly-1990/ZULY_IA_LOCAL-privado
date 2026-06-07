import bpy
import sys
import os
import json

# Rutas oficiales de ZULY
PROJECT_ROOT = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL"
SAVE_PATH = os.path.join(PROJECT_ROOT, "ZULY_PROJECTS", "pruebas", "dados_reales_zuly_v2.blend")

sys.path.insert(0, PROJECT_ROOT)

from core.agent import Agent
from core.utils.logging import log_info, log_success, log_error, log_warning

def create_perfect_dice():
    log_info("=== INICIANDO SÍNTESIS DE DADOS PERFECTOS (V2) ===")
    os.makedirs(os.path.dirname(SAVE_PATH), exist_ok=True)
    agent = Agent(force_mock=False, auto_monitor=True)
    
    # 1. Limpiar escena
    agent.execute_via_router('blender.clear_scene', {})
    
    # 2. El Dado (Cuerpo Principal)
    agent.execute_via_router('blender.create_cube', {'location': [0, 0, 1], 'scale': 1.0})
    agent.execute_via_router('blender.rename_object', {'old_name': 'Cube', 'new_name': 'Die_Body'})
    
    # Suavizado de sombreado (Nativo Blender vía scripting)
    agent.execute_via_router('blender.run_python_script', {
        'script_content': "import bpy; obj = bpy.data.objects.get('Die_Body'); \
                           if obj: bpy.context.view_layer.objects.active = obj; \
                           bpy.ops.object.shade_smooth()"
    })

    # 3. Biselado de Alta Calidad
    agent.execute_via_router('blender.add_bevel', {
        'object_name': 'Die_Body',
        'width': 0.15,
        'segments': 10
    })
    
    # 4. Los Puntos (Pips) - Mapa completo de 6 caras
    pips_map = [
        # Cara 1 (Top, Z=2)
        [0, 0, 2.0],
        # Cara 6 (Bottom, Z=0)
        [0.5, 0.5, 0], [0.5, -0.5, 0], [-0.5, 0.5, 0], [-0.5, -0.5, 0], [0.5, 0, 0], [-0.5, 0, 0],
        # Cara 2 (Front, Y=-1)
        [0.5, -1, 1.5], [-0.5, -1, 0.5],
        # Cara 5 (Back, Y=1)
        [0.5, 1, 1.5], [-0.5, 1, 0.5], [0.5, 1, 0.5], [-0.5, 1, 1.5], [0, 1, 1],
        # Cara 3 (Right, X=1)
        [1, 0.5, 1.5], [1, 0, 1], [1, -0.5, 0.5],
        # Cara 4 (Left, X=-1)
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

    # 5. Material Premium
    agent.execute_via_router('blender.create_material', {
        'name': 'Ivory_Plastic',
        'color': [0.95, 0.95, 0.9, 1], # Blanco marfil
        'roughness': 0.05,
        'metallic': 0.0
    })
    agent.execute_via_router('blender.apply_material', {
        'object_name': 'Die_Body',
        'material_name': 'Ivory_Plastic'
    })

    # 6. Iluminación y Cámara
    agent.execute_via_router('blender.create_light', {'light_type': 'SUN', 'energy': 5.0})
    agent.execute_via_router('blender.create_camera', {'location': [5, -5, 5]})

    # 7. Guardado
    try:
        bpy.ops.wm.save_as_mainfile(filepath=SAVE_PATH)
        log_success(f"=== DADOS PERFECTOS V2 COMPLETADOS: {SAVE_PATH} ===")
    except Exception as e:
        log_error(f"Error al guardar dados V2: {e}")

if __name__ == "__main__":
    create_perfect_dice()
