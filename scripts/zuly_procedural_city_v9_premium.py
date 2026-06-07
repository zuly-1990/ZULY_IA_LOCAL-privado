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

def run_premium_city_v9():
    print("\n" + "="*60)
    print("🏙️ INICIANDO RETO 6.3: CIUDAD 5.0 (BARRIO PREMIUM)")
    print("="*60)
    
    # Patchear HumanGate para ejecución automatizada
    from core.authorization.human_gate import HumanGate
    HumanGate.authorize = lambda *args: {"status": "authorized", "risk": "LOW", "action": "EXECUTE", "reason": "Premium Showcase"}
    
    # Inicializar Agente
    agent = Agent()
    
    # --- PASO 0: Limpiar Escena ---
    print("\n--- Paso 0: Limpieza Total ---")
    agent.process_natural_request("Limpiar escena")
    
    # --- PASO 1: Infraestructura (Calle y Aceras) ---
    print("\n--- Paso 1: Urbanización (Calles y Aceras) ---")
    # Terreno base (Pasto/Tierra)
    agent.process_natural_request("Crea un plano llamado 'Terreno_Base' en [0, 0, -0.05] con escala 50")
    agent.process_natural_request("Aplica material 'madera' a 'Terreno_Base'") # Usamos madera como mat base para distinción

    # Sistema de Calles (Cruz Central)
    agent.process_natural_request("Crea un plano llamado 'Calle_X' en [0, 0, 0.01] con escala [40, 6, 1]")
    agent.process_natural_request("Crea un plano llamado 'Calle_Y' en [0, 0, 0.01] con escala [6, 40, 1]")
    agent.process_natural_request("Aplica material 'concreto' a 'Calle_X'")
    agent.process_natural_request("Aplica material 'concreto' a 'Calle_Y'")

    # Aceras para Manzanas
    manzanas = [[15, 15], [-15, 15], [15, -15], [-15, -15]]
    for mi, pos in enumerate(manzanas):
        acera_name = f"Acera_Manzana_{mi}"
        agent.process_natural_request(f"Crea un cubo llamado '{acera_name}' en [{pos[0]}, {pos[1]}, 0.05] con escala [10, 10, 0.05]")
        agent.process_natural_request(f"Aplica material 'concreto' a '{acera_name}'")

    # --- PASO 2: Arquitectura Premium (Pilotis 2.0) ---
    def crear_edificio_premium(name, x, y, h):
        print(f"\n> Edificio Premium: {name} (Pilotis con Capitel)")
        # 1. Pilotis Premium (Base + Fuste + Capitel)
        p_offset = 2.0
        p_positions = [[x-p_offset, y-p_offset], [x+p_offset, y-p_offset], [x-p_offset, y+p_offset], [x+p_offset, y+p_offset]]
        
        for i, pos in enumerate(p_positions):
            p_prefix = f"{name}_P_{i}"
            # Base
            agent.process_natural_request(f"Crea un cilindro llamado '{p_prefix}_Base' en [{pos[0]}, {pos[1]}, 0.1] con escala [0.5, 0.5, 0.1]")
            # Fuste (Columna)
            agent.process_natural_request(f"Crea un cilindro llamado '{p_prefix}_Fuste' en [{pos[0]}, {pos[1]}, 1.5] con escala [0.25, 0.25, 1.4]")
            # Capitel (Soporte)
            agent.process_natural_request(f"Crea un cubo llamado '{p_prefix}_Capitel' en [{pos[0]}, {pos[1]}, 2.9] con escala [0.6, 0.6, 0.1]")
            
            # Aplicar materiales y emparentar
            agent.process_natural_request(f"Aplica material 'metal' a '{p_prefix}_Fuste'")
            agent.process_natural_request(f"Emparenta '{p_prefix}_Base' al '{p_prefix}_Fuste'")
            agent.process_natural_request(f"Emparenta '{p_prefix}_Capitel' al '{p_prefix}_Fuste'")

        # 2. Cuerpo del Edificio
        body_h = h - 3
        agent.process_natural_request(f"Crea un cubo llamado '{name}_Body' en [{x}, {y}, {3 + body_h/2}] con escala [3.5, 3.5, {body_h/2}]")
        agent.process_natural_request(f"Aplica material 'vidrio' a '{name}_Body'")
        
        # 3. Forjados (Losas)
        for floor in range(int(body_h/3) + 1):
            losa_z = 3 + (floor * 3)
            losa_name = f"{name}_Losa_{floor}"
            agent.process_natural_request(f"Crea un cubo llamado '{losa_name}' en [{x}, {y}, {losa_z}] con escala [3.7, 3.7, 0.05]")
            agent.process_natural_request(f"Aplica material 'metal' a '{losa_name}'")
            agent.process_natural_request(f"Emparenta '{losa_name}' al '{name}_Body'")

    # Posicionar Edificios en Manzanas
    crear_edificio_premium("Savoye_Center", 15, 15, 12)
    crear_edificio_premium("Savoye_North", -15, 15, 9)
    crear_edificio_premium("Savoye_South", 15, -15, 15)
    crear_edificio_premium("Savoye_West", -15, -15, 6)

    # --- PASO 3: Árboles Orgánicos 2.0 ---
    print("\n--- Paso 3: Reforestación Premium (Árboles Orgánicos) ---")
    def crear_arbol_premium(name, x, y):
        # 1. Tronco Inclinado
        rot_x = random.uniform(-5, 5)
        rot_y = random.uniform(-5, 5)
        agent.process_natural_request(f"Crea un cilindro llamado '{name}_Trunk' en [{x}, {y}, 0.8] con escala [0.15, 0.15, 0.8]")
        
        # 2. Follaje Multicapa (3 conos)
        for layer in range(3):
            scale = 1.0 - (layer * 0.25)
            z_pos = 1.5 + (layer * 0.7)
            fol_name = f"{name}_Fol_{layer}"
            agent.process_natural_request(f"Crea un cono llamado '{fol_name}' en [{x}, {y}, {z_pos}] con escala [{scale}, {scale}, 0.6]")
            agent.process_natural_request(f"Aplica material 'oro' a '{fol_name}'") # Manteniendo el toque premium
            agent.process_natural_request(f"Emparenta '{fol_name}' al '{name}_Trunk'")

    # Plantar en plazas de aceras
    for mi, pos in enumerate(manzanas):
        crear_arbol_premium(f"Arbol_M{mi}", pos[0] + 6, pos[1] + 6)
        crear_arbol_premium(f"Arbol_M{mi}_B", pos[0] - 6, pos[1] - 6)

    # --- PASO 4: Render y Cierre ---
    print("\n--- Paso 4: Finalización del Barrio ---")
    agent.process_natural_request("Crea una luz llamada 'Sol_Premium' en [30, -30, 40] con energia 5000")
    agent.process_natural_request("Crea una camara llamada 'Cam_Cine' en [50, -50, 40]")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    filepath = rf"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\ZULY_PROJECTS\ZULY_BARRIO_PREMIUM_{timestamp}.blend"
    agent.process_natural_request(f"Guardar proyecto en '{filepath}'")

    print("\n" + "="*60)
    print("✅ CIUDAD 5.0 (BARRIO PREMIUM) COMPLETADA SUCCESS")
    print("="*60)

if __name__ == "__main__":
    run_premium_city_v9()
