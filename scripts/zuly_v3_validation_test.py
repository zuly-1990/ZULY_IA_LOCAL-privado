"""
scripts/zuly_v3_validation_test.py
ZULY QA - Reto 6.6
Prueba del Certificador Topológico (Validador V3)
"""

import sys
ZULY_PATH = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL"
if ZULY_PATH not in sys.path:
    sys.path.insert(0, ZULY_PATH)

from core.agent import Agent
from core.utils.logging import log_info

def run_test():
    log_info("=" * 50)
    log_info("INICIANDO TEST: VALIDADOR V3 (BMESH TOPOLOGY)")
    log_info("=" * 50)
    
    agent = Agent()
    agent.engine_adapter.clear_scene()
    
    # ----------------------------------------------------
    # TEST 1: Prisma Impecable (Watertight)
    # ----------------------------------------------------
    log_info("\n>> TEST 1: Prisma Perfecto")
    agent.engine_adapter.create_primitive('cube', name='Prisma_Perfecto', scale=[2,2,2])
    
    result_1 = agent.execute_via_router('blender.validate_topology', {
        'object_name': 'Prisma_Perfecto'
    })
    
    print("\n--- Resultado TEST 1 ---")
    print(f"Status: {result_1.get('status')}")
    print(f"Datos Validador: {result_1.get('result')}")
    
    # ----------------------------------------------------
    # TEST 2: Ciudad 7.1 (Booleans Estructurales)
    # ----------------------------------------------------
    log_info("\n>> TEST 2: Boolean Architecture")
    agent.engine_adapter.create_primitive('cube', name='Edificio_V3', scale=[3, 3, 5])
    agent.engine_adapter.create_primitive('cube', name='Cutter_V3', location=[3, 0, 0], scale=[1, 1, 1])
    agent.engine_adapter.add_modifier('Edificio_V3', 'BOOLEAN', operation='DIFFERENCE', operand_object='Cutter_V3')
    
    result_2 = agent.execute_via_router('blender.validate_topology', {
        'object_name': 'Edificio_V3'
    })
    
    print("\n--- Resultado TEST 2 ---")
    print(f"Status: {result_2.get('status')}")
    print(f"Datos Validador: {result_2.get('result')}")

    # ----------------------------------------------------
    # TEST 3: Superficie Abierta (Bordes Non-Manifold Intencionales)
    # ----------------------------------------------------
    log_info("\n>> TEST 3: Malla Corrupta (Plane)")
    # Un "plane" simple tiene 4 bordes libres por definición (no es cerrado), así que es Non-Manifold.
    agent.engine_adapter.create_primitive('plane', name='Plano_Corrupto', scale=[5,5,1])
    
    result_3 = agent.execute_via_router('blender.validate_topology', {
        'object_name': 'Plano_Corrupto'
    })
    
    print("\n--- Resultado TEST 3 ---")
    print(f"Status: {result_3.get('status')}")
    print(f"Datos Validador: {result_3.get('result')}")

if __name__ == "__main__":
    run_test()
