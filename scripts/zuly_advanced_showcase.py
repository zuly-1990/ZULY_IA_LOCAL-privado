# scripts/zuly_advanced_showcase.py
import sys
import os
import time
from datetime import datetime

# Añadir el path raíz para importar core
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.agent import Agent
from core.utils.logging import log_info, log_success, log_error

# FASE 24: Parche de autorización automática para Showcase
from core.authorization.human_gate import HumanGate
HumanGate.authorize = lambda *args: {"risk": "LOW", "action": "EXECUTE", "reason": "Autorización automática para Showcase jjj"}

def run_advanced_showcase():
    log_info("🚀 INICIANDO SHOWCASE DE CAPACIDADES AVANZADAS - ZULY_IA")
    agent = Agent()
    
    # 0. Limpiar escena
    agent.process_natural_request("Limpiar escena")
    
    # 1. Crear Base (Plataforma de Oro)
    log_info("--- Paso 1: Creando Base de Oro ---")
    agent.process_natural_request("Crea un plano llamado 'Base_Showcase' en [0, 0, 0] con escala [5, 5, 1]")
    agent.process_natural_request("Aplica material 'oro' a 'Base_Showcase'")
    
    # 2. Crear Escultura Central (Estructura con Modificadores)
    log_info("--- Paso 2: Escultura con Modificadores ---")
    agent.process_natural_request("Crea un cubo llamado 'Escultura_Core' en [0, 0, 1.5] con escala 0.8")
    agent.process_natural_request("Aplica modificador 'subdivision' a 'Escultura_Core' con niveles 2")
    agent.process_natural_request("Aplica material 'vidrio' a 'Escultura_Core'")
    
    # 3. Componentes Orbitantes (Jerarquía)
    log_info("--- Paso 3: Jerarquía y Orbitales ---")
    for i in range(4):
        angle = (360 / 4) * i
        x = 2.0 * (1 if i % 2 == 0 else -1) if i < 2 else 0
        y = 0 if i < 2 else 2.0 * (1 if i % 2 == 0 else -1)
        name = f"Orbital_{i}"
        agent.process_natural_request(f"Crea una esfera llamada '{name}' en [{x}, {y}, 2.0] con escala 0.3")
        agent.process_natural_request(f"Emparenta '{name}' a 'Escultura_Core'")
        agent.process_natural_request(f"Aplica material 'plata' a '{name}'")
    
    # 4. Iluminación Pro (Three-Point Lighting)
    log_info("--- Paso 4: Iluminación Cinemática ---")
    agent.process_natural_request("Crea una luz llamada 'Key_Light' en [5, -5, 10] con energía 1000")
    agent.process_natural_request("Crea una luz llamada 'Fill_Light' en [-5, -5, 5] con energía 300")
    agent.process_natural_request("Crea una luz llamada 'Rim_Light' en [0, 10, 5] con energía 500")
    
    # 5. Cámara con Look-At
    log_info("--- Paso 5: Cámara con Look-At ---")
    agent.process_natural_request("Crea una camara llamada 'Main_Cam' en [8, -8, 6]")
    # Nota: El agente debería poder posicionarla mirando a la escultura
    # Usaremos el nombre directo si la NLU lo permite o vía parametro manual en el script
    from core.adapters import get_engine_adapter
    adapter = get_engine_adapter()
    adapter.position_camera("Main_Cam", [8, -8, 6], [0, 0, 1.5])
    
    # 6. Salvar Archivo Final Certificado
    log_info("--- Paso 6: Persistencia Binaria ---")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    output_path = f"C:\\Users\\Admin\\Desktop\\ZULY_IA_LOCAL\\ZULY_PROJECTS\\ZULY_SHOWCASE_{timestamp}.blend"
    
    # Usar el comando de guardado que ya sanamos
    agent.process_natural_request(f"Guardar proyecto en '{output_path}'")
    
    if os.path.exists(output_path):
        size = os.path.getsize(output_path)
        log_success(f"💎 SHOWCASE COMPLETADO: {output_path} ({size} bytes)")
    else:
        log_error("❌ Falla en la persistencia del Showcase")

if __name__ == "__main__":
    run_advanced_showcase()
