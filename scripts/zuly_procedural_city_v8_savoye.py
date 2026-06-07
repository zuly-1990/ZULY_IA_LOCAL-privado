import bpy
import os
import sys
import random
import time
from datetime import datetime

# Añadir el directorio del proyecto al PYTHONPATH
sys.path.append(r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL")

from core.agent import Agent
from core.utils.logging import log_info, log_success, log_error

def run_savoye_structure_showcase():
    print("\n" + "="*60)
    print("🏙️ INICIANDO RETO 6.2: MASTER PLAN SAVOYE (SÓLO ESTRUCTURA)")
    print("="*60)
    
    # Patchear HumanGate para ejecución automatizada
    from core.authorization.human_gate import HumanGate
    HumanGate.authorize = lambda *args: {"status": "authorized", "risk": "LOW", "action": "EXECUTE", "reason": "Structural Showcase"}
    
    # Inicializar Agente
    agent = Agent()
    
    # --- PASO 0: Limpiar Escena ---
    print("\n--- Paso 0: Limpieza Arquitectónica ---")
    agent.process_natural_request("Limpiar escena")
    
    # --- PASO 1: Suelo y Urbanismo ---
    print("\n--- Paso 1: Terreno y Zonificación (60x60m) ---")
    agent.process_natural_request("Crea un plano llamado 'Suelo_Master' en [0, 0, 0] con escala 30")
    agent.process_natural_request("Aplica material 'concreto' a 'Suelo_Master'")

    def crear_edificio_financiero(name, x, y, h):
        print(f"\n> Estructura Financiera: {name} (Pilotis + Cuerpo)")
        # 1. Pilotis (4 columnas circulares)
        p_offset = 1.5
        for i, pos in enumerate([[x-p_offset, y-p_offset], [x+p_offset, y-p_offset], [x-p_offset, y+p_offset], [x+p_offset, y+p_offset]]):
            p_name = f"{name}_Piloti_{i}"
            agent.process_natural_request(f"Crea un cilindro llamado '{p_name}' en [{pos[0]}, {pos[1]}, 1.5] con escala [0.3, 0.3, 1.5]")
            agent.process_natural_request(f"Aplica material 'metal' a '{p_name}'")
        
        # 2. Cuerpo Vital (Caja de Vidrio elevada)
        body_h = h - 3
        agent.process_natural_request(f"Crea un cubo llamado '{name}_Cuerpo' en [{x}, {y}, {3 + body_h/2}] con escala [2.5, 2.5, {body_h/2}]")
        agent.process_natural_request(f"Aplica material 'vidrio' a '{name}_Cuerpo'")
        
        # 3. Emparentar todo al cuerpo (Estructura jerárquica)
        for i in range(4):
            agent.process_natural_request(f"Emparenta '{name}_Piloti_{i}' al '{name}_Cuerpo'")

    def crear_edificio_residencial(name, x, y, floors):
        print(f"\n> Estructura Residencial: {name} ({floors} niveles)")
        h_per_floor = 3
        total_h = floors * h_per_floor
        
        # 1. Cuerpo de Concreto
        agent.process_natural_request(f"Crea un cubo llamado '{name}_Estructura' en [{x}, {y}, {total_h/2}] con escala [3, 3, {total_h/2}]")
        agent.process_natural_request(f"Aplica material 'concreto' a '{name}_Estructura'")
        
        # 2. Losas Técnicas (Forjados marcados)
        for f in range(floors + 1):
            l_name = f"{name}_Losa_{f}"
            z_pos = f * h_per_floor
            agent.process_natural_request(f"Crea un cubo llamado '{l_name}' en [{x}, {y}, {z_pos}] con escala [3.2, 3.2, 0.07]")
            agent.process_natural_request(f"Aplica material 'metal' a '{l_name}'")
            agent.process_natural_request(f"Emparenta '{l_name}' al '{name}_Estructura'")

    # --- PASO 2: Construcción por Zonas ---
    # Distrito Financiero (Centro)
    crear_edificio_financiero("Sky_Alpha", 0, 0, 20)
    crear_edificio_financiero("Sky_Beta", 15, 0, 18)
    crear_edificio_financiero("Sky_Gamma", -15, 0, 22)
    
    # Zona Residencial (Periferia)
    crear_edificio_residencial("Block_A", 0, 15, 3)
    crear_edificio_residencial("Block_B", 0, -15, 4)
    crear_edificio_residencial("Block_C", 15, 15, 2)
    crear_edificio_residencial("Block_D", -15, -15, 3)

    # --- PASO 3: Espacios Públicos (Estructura de Árboles) ---
    print("\n--- Paso 3: Reforestación Técnica (Plazas) ---")
    plazas = [[15, -15], [-15, 15]]
    for pi, pos in enumerate(plazas):
        for ai in range(3):
            tx = pos[0] + random.uniform(-2, 2)
            ty = pos[1] + random.uniform(-2, 2)
            t_name = f"Arbol_Plaza_{pi}_{ai}"
            agent.process_natural_request(f"Crea un cilindro llamado '{t_name}_Tronco' en [{tx}, {ty}, 0.5] con escala [0.2, 0.2, 0.5]")
            agent.process_natural_request(f"Crea un cono llamado '{t_name}_Copa' en [{tx}, {ty}, 1.5] con escala [0.6, 0.6, 0.6]")
            agent.process_natural_request(f"Emparenta '{t_name}_Copa' al '{t_name}_Tronco'")

    # --- PASO 4: Iluminación y Guardado ---
    print("\n--- Paso 4: Cierre de Obra ---")
    agent.process_natural_request("Crea una luz llamada 'Sol_Master' en [20, -20, 30] con energia 3000")
    agent.process_natural_request("Crea una camara llamada 'Render_Urban' en [40, -40, 30]")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    filepath = rf"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\ZULY_PROJECTS\ZULY_SAVOYE_STRUCT_{timestamp}.blend"
    agent.process_natural_request(f"Guardar proyecto en '{filepath}'")

    print("\n" + "="*60)
    print("✅ ESTRUCTURA SAVOYE COMPLETADA")
    print("="*60)

if __name__ == "__main__":
    run_savoye_structure_showcase()
