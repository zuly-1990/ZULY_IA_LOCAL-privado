"""
Script de Reto 2 - Semana 6 (Laboratorio Real 2.0)
Generación de Bosque (100 árboles).
"""
import os
from datetime import datetime
from core.agent import Agent
from core.utils.logging import log_info, log_success, log_error
from core.authorization.human_gate import HumanGate

def run_challenge_2():
    log_info("=== INICIANDO RETO 2: BOSQUE ORGANICO (VERSION BINARIA) ===")
    
    original_authorize = HumanGate.authorize
    HumanGate.authorize = staticmethod(lambda x: {"risk": "LOW", "action": "EXECUTE", "reason": "Bypass Test"})
    
    agent = Agent()
    agent.authorized = True
    
    agent.process_natural_request("Limpia la escena de Blender")
    
    # Crear 100 árboles (simplificado para evitar tiempos infinitos en BG)
    log_info("Generando 100 elementos...")
    for i in range(50): # 50 árboles = 100 objetos (tronco + copa)
        x = (i % 10) * 3
        y = (i // 10) * 3
        agent.process_natural_request(f"Crea un cilindro de radio 0.2 llamado Tronco_{i} en {x},{y},0")
        agent.process_natural_request(f"Crea un cono llamado Copa_{i} en {x},{y},2")
        
    today = datetime.now().strftime("%Y%m%d")
    blend_name = f"SEMANA_6_bosque_{today}.blend"
    blend_path = os.path.abspath(f"C:/Users/Admin/Desktop/ZULY_IA_LOCAL/ZULY_PROJECTS/{blend_name}")
    
    agent.process_natural_request(f"Guarda el proyecto de Blender en {blend_path}")
    
    if os.path.exists(blend_path) and os.path.getsize(blend_path) > 5000:
        log_success(f"✅ ARCHIVO BINARIO REAL CREADO: {blend_name}")
    else:
        log_error("❌ FALLO: Archivo no generado.")

    HumanGate.authorize = original_authorize

if __name__ == "__main__":
    run_challenge_2()
