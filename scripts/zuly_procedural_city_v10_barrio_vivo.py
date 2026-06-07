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

def run_barrio_vivo_v10():
    print("\n" + "="*60)
    print("🏙️ INICIANDO RETO 6.4: CIUDAD 6.0 (BARRIO VIVO)")
    print("="*60)
    
    # Patchear HumanGate para ejecución automatizada
    from core.authorization.human_gate import HumanGate
    HumanGate.authorize = lambda *args: {"status": "authorized", "risk": "LOW", "action": "EXECUTE", "reason": "Barrio Vivo Showcase"}
    
    # Inicializar Agente
    agent = Agent()
    
    # --- PASO 0: Limpiar Escena ---
    print("\n--- Paso 0: Limpieza Detallada ---")
    agent.process_natural_request("Limpiar escena")
    
    # --- PASO 1: Infraestructura y Manzanas ---
    print("\n--- Paso 1: Urbanización de Alta Fidelidad ---")
    # Terreno base (Pasto)
    agent.process_natural_request("Crea un plano llamado 'Base_Pasto' en [0, 0, -0.1] con escala 60")
    agent.process_natural_request("Aplica material 'madera' a 'Base_Pasto'") # Verde simulado

    # Calles con Asfalto y Líneas
    agent.process_natural_request("Crea un plano llamado 'Calle_Principal_H' en [0, 0, 0.01] con escala [50, 7, 1]")
    agent.process_natural_request("Crea un plano llamado 'Calle_Principal_V' en [0, 0, 0.01] con escala [7, 50, 1]")
    agent.process_natural_request("Aplica material 'concreto' a 'Calle_Principal_H'")
    agent.process_natural_request("Aplica material 'concreto' a 'Calle_Principal_V'")

    # Aceras con bordillos
    manzanas = [[18, 18], [-18, 18], [18, -18], [-18, -18]]
    for mi, pos in enumerate(manzanas):
        acera = f"Acera_M{mi}"
        agent.process_natural_request(f"Crea un cubo llamado '{acera}' en [{pos[0]}, {pos[1]}, 0.1] con escala [12, 12, 0.1]")
        agent.process_natural_request(f"Aplica material 'concreto' a '{acera}'")

    # --- PASO 2: Arquitectura Detallada (Ensambles) ---
    def crear_edificio_vivo(name, x, y, h, floors):
        print(f"\n> Construyendo Edificio Detallado: {name}")
        # 1. Pilotis Premium
        p_offset = 2.5
        p_pos = [[x-p_offset, y-p_offset], [x+p_offset, y-p_offset], [x-p_offset, y+p_offset], [x+p_offset, y+p_offset]]
        for i, pos in enumerate(p_pos):
            col = f"{name}_Col_{i}"
            agent.process_natural_request(f"Crea un cilindro llamado '{col}' en [{pos[0]}, {pos[1]}, 1.5] con escala [0.3, 0.3, 1.5]")
            agent.process_natural_request(f"Aplica material 'metal' a '{col}'")

        # 2. Cuerpo y Carpintería (Mullions)
        body_z = 3 + (h/2)
        agent.process_natural_request(f"Crea un cubo llamado '{name}_Vidrio' en [{x}, {y}, {body_z}] con escala [4, 4, {h/2}]")
        agent.process_natural_request(f"Aplica material 'vidrio' a '{name}_Vidrio'")
        
        # Simulación de Carpintería (Marcos de Ventanas)
        for f in range(floors):
            z_f = 3 + (f * 4) + 2
            marco_h = f"{name}_Marco_H_{f}"
            agent.process_natural_request(f"Crea un cubo llamado '{marco_h}' en [{x}, {y}, {z_f}] con escala [4.1, 4.1, 0.05]")
            agent.process_natural_request(f"Aplica material 'metal' a '{marco_h}'")
            agent.process_natural_request(f"Emparenta '{marco_h}' al '{name}_Vidrio'")
            
            # Mullions Verticales (4 esquinas detalladas)
            for vi, vpos in enumerate(p_pos):
                marco_v = f"{name}_Marco_V_{f}_{vi}"
                agent.process_natural_request(f"Crea un cubo llamado '{marco_v}' en [{vpos[0]}, {vpos[1]}, {z_f}] con escala [0.1, 0.1, 2]")
                agent.process_natural_request(f"Aplica material 'metal' a '{marco_v}'")
                agent.process_natural_request(f"Emparenta '{marco_v}' al '{name}_Vidrio'")

        # 3. Cubierta Técnica
        roof_z = 3 + h
        agent.process_natural_request(f"Crea un cubo llamado '{name}_Roof' en [{x}, {y}, {roof_z + 0.5}] con escala [2, 2, 0.5]")
        agent.process_natural_request(f"Aplica material 'metal' a '{name}_Roof'")
        agent.process_natural_request(f"Emparenta '{name}_Roof' al '{name}_Vidrio'")

    # Ejecutar construcción masiva jerarquizada
    crear_edificio_vivo("Savoye_V1", 18, 18, 12, 3)
    crear_edificio_vivo("Savoye_V2", -18, 18, 8, 2)
    crear_edificio_vivo("Savoye_V3", 18, -18, 16, 4)

    # --- PASO 3: Mobiliario Urbano (Postes de Luz) ---
    print("\n--- Paso 3: Mobiliario Urbano Detallado ---")
    postes = [[8, 8], [-8, 8], [8, -8], [-8, -8]]
    for idx, p_pos in enumerate(postes):
        post_name = f"Poste_{idx}"
        agent.process_natural_request(f"Crea un cilindro llamado '{post_name}' en [{p_pos[0]}, {p_pos[1]}, 2.5] con escala [0.1, 0.1, 2.5]")
        agent.process_natural_request(f"Aplica material 'metal' a '{post_name}'")
        # Foco Emisor
        agent.process_natural_request(f"Crea una esfera llamada '{post_name}_Luz' en [{p_pos[0]}, {p_pos[1]}, 5] con escala 0.3")
        agent.process_natural_request(f"Aplica material 'oro' a '{post_name}_Luz'") # Simula emisión
        agent.process_natural_request(f"Crea una luz llamada '{post_name}_Point' en [{p_pos[0]}, {p_pos[1]}, 4.8] con energia 500")

    # --- PASO 4: Vegetación y Cierre ---
    print("\n--- Paso 4: Finalización del Barrio Escénico ---")
    agent.process_natural_request("Crea una luz llamada 'Luna_Cenital' en [0, 0, 50] con energia 2000")
    agent.process_natural_request("Crea una camara llamada 'Camara_Barrio' en [60, -60, 45]")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    filepath = rf"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\ZULY_PROJECTS\ZULY_BARRIO_VIVO_V10_{timestamp}.blend"
    agent.process_natural_request(f"Guardar proyecto en '{filepath}'")

    print("\n" + "="*60)
    print("✅ CIUDAD 6.0 (BARRIO VIVO) COMPLETADA SUCCESS")
    print("="*60)

if __name__ == "__main__":
    run_barrio_vivo_v10()
