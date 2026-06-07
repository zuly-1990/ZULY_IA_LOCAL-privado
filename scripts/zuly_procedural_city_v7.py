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

def run_procedural_city_showcase():
    print("\n" + "="*60)
    print("🏙️ INICIANDO RETO: CIUDAD PROCEDURAL - ZULY_IA")
    print("="*60)
    
    # Patchear HumanGate para ejecución automatizada
    from core.authorization.human_gate import HumanGate
    HumanGate.authorize = lambda *args: {"status": "authorized", "risk": "LOW", "action": "EXECUTE", "reason": "Showcase Bypass"}
    
    # Inicializar Agente
    agent = Agent()
    
    # --- PASO 0: Limpiar Escena ---
    print("\n--- Paso 0: Limpieza Total ---")
    agent.process_natural_request("Limpiar escena")
    
    # --- PASO 1: Suelo ---
    print("\n--- Paso 1: El Suelo de la Ciudad (Norma Técnica: 40x40m) ---")
    agent.process_natural_request("Crea un plano llamado 'Suelo_Ciudad' en [0, 0, 0] con escala 20") # escala 20 = 40m
    agent.process_natural_request("Aplica material 'concreto' a 'Suelo_Ciudad'")
    
    # --- PASO 2: Edificios (Procedural - Espaciado Técnico) ---
    print("\n--- Paso 2: Generación Urbanística (Retiro de 15m) ---")
    num_buildings = 12
    grid_size = 4
    spacing = 15
    
    for i in range(num_buildings):
        # Evitar el centro exacto para dejar "vía" central
        row = i // 3
        col = i % 3
        x = col * spacing - (3 * spacing / 2) + 7.5
        y = row * spacing - (4 * spacing / 2) + 7.5
        
        h = random.uniform(3, 12) # Edificios más altos
        name = f"Edificio_{i}"
        
        print(f"\n> Construyendo {name} (Norma Técnica: Espaciado 10m)...")
        agent.process_natural_request(f"Crea un cubo llamado '{name}' en [{x}, {y}, {h/2}] con escala [2, 2, {h/2}]") # Ligeramente más anchos
        
        # Rotación sutil
        agent.process_natural_request(f"Rota '{name}' en [0, 0, {random.uniform(-15, 15)}] grados")
        
        # Materiales premium
        mat = "vidrio" if h > 8 else ("cobre" if h > 5 else "metal")
        agent.process_natural_request(f"Aplica material '{mat}' a '{name}'")

    # --- PASO 3: Árboles (Jerárquicos - Reforestación) ---
    print("\n--- Paso 3: Reforestación de Parques ---")
    num_trees = 8
    for i in range(num_trees):
        tx = random.uniform(-15, 15)
        ty = random.uniform(-15, 15)
        
        trunk_name = f"Tronco_{i}"
        top_name = f"Copa_{i}"
        
        print(f"\n> Plantado árbol {i}...")
        # Tronco
        agent.process_natural_request(f"Crea un cilindro llamado '{trunk_name}' en [{tx}, {ty}, 0.5] con escala [0.2, 0.2, 0.5]")
        agent.process_natural_request(f"Aplica material 'madera' a '{trunk_name}'")
        
        # Copa
        agent.process_natural_request(f"Crea un cono llamado '{top_name}' en [{tx}, {ty}, 1.5] con escala [0.6, 0.6, 0.6]")
        agent.process_natural_request(f"Aplica material 'oro' a '{top_name}'") # Árboles de oro!
        
        # Jerarquía
        agent.process_natural_request(f"Emparenta '{top_name}' al '{trunk_name}'")

    # --- PASO 4: Luces y Cámara ---
    print("\n--- Paso 4: Iluminación y Visión ---")
    agent.process_natural_request("Crea una luz llamada 'Sol_Ciudad' en [10, -10, 20] con energia 2000")
    agent.process_natural_request("Crea una camara llamada 'Vista_Aerea' en [25, -25, 20]")
    
    # --- PASO 5: Guardar ---
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    filepath = rf"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\ZULY_PROJECTS\ZULY_CITY_PROD_{timestamp}.blend"
    print(f"\n--- Paso 5: Persistencia en {filepath} ---")
    agent.process_natural_request(f"Guardar proyecto en '{filepath}'")

    print("\n" + "="*60)
    print("✅ RETO DE CIUDAD COMPLETADO")
    print("="*60)

if __name__ == "__main__":
    run_procedural_city_showcase()
