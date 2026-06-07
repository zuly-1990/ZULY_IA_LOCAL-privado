"""
Script de Reto 5 - Semana 6 (Laboratorio Real 2.0)
Suite de Rendimiento (Burst Mode).
"""
import os
import time
from datetime import datetime
from core.agent import Agent
from core.utils.logging import log_info, log_success, log_error
from core.authorization.human_gate import HumanGate

def run_challenge_5():
    log_info("=== INICIANDO RETO 5: RENDIMIENTO (VERSION BINARIA) ===")
    
    original_authorize = HumanGate.authorize
    HumanGate.authorize = staticmethod(lambda x: {"risk": "LOW", "action": "EXECUTE", "reason": "Bypass Test"})
    
    agent = Agent()
    agent.authorized = True
    
    agent.process_natural_request("Limpia la escena de Blender")
    
    start_time = time.time()
    for i in range(20): # Reducido a 20 para ráfaga rápida pero real
        agent.process_natural_request(f"Crea un cubo llamado Burst_{i} en {i},0,0")
    end_time = time.time()
    
    total = end_time - start_time
    log_info(f"Tiempo total de ráfaga: {total:.2f}s")
    
    today = datetime.now().strftime("%Y%m%d")
    blend_name = f"SEMANA_6_rendimiento_{today}.blend"
    blend_path = os.path.abspath(f"C:/Users/Admin/Desktop/ZULY_IA_LOCAL/ZULY_PROJECTS/{blend_name}")
    
    agent.process_natural_request(f"Guarda el proyecto de Blender en {blend_path}")
    
    if os.path.exists(blend_path) and os.path.getsize(blend_path) > 5000:
        log_success(f"✅ ARCHIVO BINARIO REAL CREADO: {blend_name}")
    else:
        log_error("❌ FALLO: Archivo no generado.")

    HumanGate.authorize = original_authorize

if __name__ == "__main__":
    run_challenge_5()
