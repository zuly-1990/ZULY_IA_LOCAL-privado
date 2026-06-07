import bpy
import sys
import os
import json

# Rutas oficiales de ZULY
PROJECT_ROOT = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL"
SAVE_PATH = os.path.join(PROJECT_ROOT, "ZULY_PROJECTS", "pruebas", "dados_reales_zuly.blend")

sys.path.insert(0, PROJECT_ROOT)

from core.agent import Agent
from core.utils.logging import log_info, log_success, log_error, log_warning

def create_realistic_dice():
    log_info("=== INICIANDO SÍNTESIS DE DADOS REALISTAS (ANTI-LEGO) ===")
    os.makedirs(os.path.dirname(SAVE_PATH), exist_ok=True)
    agent = Agent(force_mock=False, auto_monitor=True)
    
    # 1. Limpiar escena
    agent.execute_via_router('blender.clear_scene', {})
    
    # 2. El Dado (Cuerpo Principal)
    agent.execute_via_router('blender.create_cube', {'location': [0, 0, 1], 'scale': 1.0})
    agent.execute_via_router('blender.rename_object', {'old_name': 'Cube', 'new_name': 'Die_Body'})
    
    # 3. Biselado (Crucial para eliminar el estilo Lego)
    # Aplicamos un bevel moderado para redondear las esquinas
    agent.execute_via_router('blender.add_bevel', {
        'object_name': 'Die_Body',
        'width': 0.1,
        'segments': 5
    })
    
    # 4. Los Puntos (Pips) - Coordenadas relativas al centro del dado [0,0,1]
    # Usaremos esferas pequeñas para "excavar" el dado
    pips_data = [
        # Cara 1 (Arriba, Z=2)
        {'loc': [0, 0, 2.0], 'name': 'pip_1_1'},
        
        # Cara 6 (Abajo, Z=0) - Opuesta a 1
        {'loc': [0.5, 0.5, 0], 'name': 'pip_6_1'},
        {'loc': [0.5, -0.5, 0], 'name': 'pip_6_2'},
        {'loc': [-0.5, 0.5, 0], 'name': 'pip_6_3'},
        {'loc': [-0.5, -0.5, 0], 'name': 'pip_6_4'},
        {'loc': [0.5, 0, 0], 'name': 'pip_6_5'},
        {'loc': [-0.5, 0, 0], 'name': 'pip_6_6'},
        
        # Cara 2 (Frente, Y=-1)
        {'loc': [0.4, -1.0, 1.4], 'name': 'pip_2_1'},
        {'loc': [-0.4, -1.0, 0.6], 'name': 'pip_2_2'},
        
        # Cara 5 (Atrás, Y=1) - Opuesta a 2
        {'loc': [0.5, 1.0, 1.5], 'name': 'pip_5_1'},
        {'loc': [-0.5, 1.0, 0.5], 'name': 'pip_5_2'},
        {'loc': [0.5, 1.0, 0.5], 'name': 'pip_5_3'},
        {'loc': [-0.5, 1.0, 1.5], 'name': 'pip_5_4'},
        {'loc': [0, 1.0, 1.0], 'name': 'pip_5_5'},
    ]
    
    # Crear esferas para los pips
    for pip in pips_data:
        agent.execute_via_router('blender.create_sphere', {
            'location': pip['loc'],
            'radius': 0.15
        })
        # Usar el booleano para cada uno (Sustractivo)
        agent.execute_via_router('blender.add_boolean', {
            'object_name': 'Die_Body',
            'target_name': 'Sphere', # El último creado
            'operation': 'DIFFERENCE'
        })
        # Ocultar o borrar la herramienta booleana
        agent.execute_via_router('blender.delete_object', {'object_name': 'Sphere'})

    # 5. Materiales Realistas
    agent.execute_via_router('blender.create_material', {
        'name': 'Die_Plastic',
        'color': [1, 1, 1, 1], # Blanco
        'roughness': 0.1,      # Brillante
        'metallic': 0.0
    })
    agent.execute_via_router('blender.apply_material', {
        'object_name': 'Die_Body',
        'material_name': 'Die_Plastic'
    })

    # 6. Iluminación y Cámara para el "Beauty Shot"
    agent.execute_via_router('blender.create_light', {'light_type': 'AREA', 'location': [5, 5, 10], 'energy': 1000})
    agent.execute_via_router('blender.create_camera', {'location': [4, -4, 4]})

    # 7. Guardado
    try:
        bpy.ops.wm.save_as_mainfile(filepath=SAVE_PATH)
        log_success(f"=== DADOS REALISTAS COMPLETADOS: {SAVE_PATH} ===")
    except Exception as e:
        log_error(f"Error al guardar dados: {e}")

if __name__ == "__main__":
    create_realistic_dice()
