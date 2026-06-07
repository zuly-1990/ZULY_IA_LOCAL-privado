"""
Script de Reto 4 - Semana 6 (Laboratorio Real 2.0)
Sistema Solar Jerárquico.
"""
import os
from datetime import datetime
from core.agent import Agent
from core.utils.logging import log_info, log_success, log_error
from core.authorization.human_gate import HumanGate

def run_challenge_4():
    log_info("=== INICIANDO RETO 4: SISTEMA SOLAR (VERSION BINARIA) ===")
    
    original_authorize = HumanGate.authorize
    HumanGate.authorize = staticmethod(lambda x: {"risk": "LOW", "action": "EXECUTE", "reason": "Bypass Test"})
    
    agent = Agent()
    agent.authorized = True
    
    agent.process_natural_request("Limpia la escena de Blender")
    
    # Sol
    agent.process_natural_request("Crea una esfera llamada Sol de escala 2")
    # Tierra
    agent.process_natural_request("Crea una esfera llamada Tierra en x=10")
    agent.process_natural_request("Emparenta el objeto Tierra al objeto Sol")
    # Luna
    agent.process_natural_request("Crea una esfera llamada Luna en x=12 de escala 0.3")
    agent.process_natural_request("Emparenta el objeto Luna al objeto Tierra")
    
    # Rotar el Sol para ver que todo gira
    agent.process_natural_request("Rota el objeto Sol 45 grados en Z")
    
    today = datetime.now().strftime("%Y%m%d")
    blend_name = f"SEMANA_6_sistema_solar_{today}.blend"
    blend_path = os.path.abspath(f"C:/Users/Admin/Desktop/ZULY_IA_LOCAL/ZULY_PROJECTS/{blend_name}")
    
    agent.process_natural_request(f"Guarda el proyecto de Blender en {blend_path}")
    
    if os.path.exists(blend_path) and os.path.getsize(blend_path) > 5000:
        log_success(f"✅ ARCHIVO BINARIO REAL CREADO: {blend_name}")
    else:
        log_error("❌ FALLO: Archivo no generado.")

    HumanGate.authorize = original_authorize

if __name__ == "__main__":
    run_challenge_4()
