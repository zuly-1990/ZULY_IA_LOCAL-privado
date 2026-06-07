"""
scripts/zuly_perfect_modeling_v11.py
(Ciudad 7.1 - Geometría de Precisión)

Genera un edificio impecable utilizando sustracciones booleanas reales
para las ventanas y biselado estructural en todas las aristas vivas,
cumpliendo el reto 6.5 del Modelado Perfecto.
"""

import sys
ZULY_PATH = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL"
if ZULY_PATH not in sys.path:
    sys.path.insert(0, ZULY_PATH)

from core.agent import Agent

def run():
    print("Iniciando ZULY Ciudad 7.1: Geometría de Precisión...")
    
    agent = Agent()
    
    # Limpiamos escena
    agent.engine_adapter.clear_scene()
    
    # 1. Base del Edificio (Masa Principal)
    result = agent.engine_adapter.create_primitive(
        'cube',
        name='Edificio_Principal',
        location=[0, 0, 5],
        scale=[3, 3, 5]
    )
    
    if result.get('status') == 'failed':
        print("Error creador masa principal")
        return
    
    # 2. Agregar Modificador Bevel a la masa principal para capturar luz
    agent.engine_adapter.add_modifier(
        'Edificio_Principal',
        'BEVEL',
        width=0.1,
        segments=3
    )
    
    # 3. Modelado Sustractivo: Crear "Cúteres" para las ventanas
    print("Generando huecos de ventanas mediante sustracción booleana...")
    
    for floor in range(1, 4):
        z_pos = floor * 2.5
        for side in [-1, 1]:
            # Cortadores en el eje X
            cutter_name_x = f'Cutter_Win_X_F{floor}_S{side}'
            agent.engine_adapter.create_primitive(
                'cube',
                name=cutter_name_x,
                location=[side * 3, 0, z_pos],
                scale=[0.5, 2, 0.8]
            )
            
            # Aplicar Booleano
            agent.engine_adapter.add_modifier(
                'Edificio_Principal',
                'BOOLEAN',
                operation='DIFFERENCE',
                operand_object=cutter_name_x,
                hide_operand=True
            )
            
            # Cortadores en el eje Y
            cutter_name_y = f'Cutter_Win_Y_F{floor}_S{side}'
            agent.engine_adapter.create_primitive(
                'cube',
                name=cutter_name_y,
                location=[0, side * 3, z_pos],
                scale=[2, 0.5, 0.8]
            )
            
            # Aplicar Booleano
            agent.engine_adapter.add_modifier(
                'Edificio_Principal',
                'BOOLEAN',
                operation='DIFFERENCE',
                operand_object=cutter_name_y,
                hide_operand=True
            )

    # Guardamos el archivo .blend resultante para validación del FS6
    agent.engine_adapter.export_scene(
        'BLEND',
        'C:/Users/Admin/Desktop/ZULY_IA_LOCAL/ZULY_PROJECTS/ZULY_CIUDAD_7_1_PRECISION.blend'
    )
    
    print("Éxito: Geometría de Precisión generada y guardada exitosamente.")

if __name__ == '__main__':
    run()
