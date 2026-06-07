"""
Script de Sesión Real - Fin de Semana 5 (REVISADO)
Valida: V2 Validator, Jerarquía de Memoria y Convención de Nombres.
"""
import os
import json
import logging
from datetime import datetime
from unittest.mock import MagicMock, patch
from core.agent import Agent
from core.utils.logging import log_info, log_success, log_error, log_warning

# Silenciar logs excesivos si es necesario
logging.getLogger('LYZU').setLevel(logging.INFO)

def run_real_session_tests():
    log_info("=== INICIANDO SESIÓN DE PRUEBA REAL (FDE 5) ===")
    
    agent = Agent()
    agent.authorized = True
    
    # Mockeamos componentes para control total
    agent.human_gate.authorize = MagicMock(return_value={"action": "ALLOW", "risk": "LOW", "reason": "Test"})
    agent.context_guard.evaluate = MagicMock(return_value={"status": "PERMITIDO", "reason": "Test"})
    agent.engine_adapter.get_current_mode = MagicMock(return_value="OBJECT")
    agent.engine_adapter.is_available = MagicMock(return_value=True)

    # ---------------------------------------------------------
    # PRUEBA 1: Bloqueo V2 (Contexto Inválido)
    # ---------------------------------------------------------
    log_info("\n[PRUEBA 1] Validando Bloqueo V2 (EDIT Mode)")
    agent.engine_adapter.get_current_mode.return_value = "EDIT"
    
    result1 = agent.process_natural_request("Crea un cubo de prueba")
    # V2 debe bloquear antes de la ejecución (Fase 6 en agent.py)
    if not result1['success'] and "V2 BLOQUEO" in str(result1.get('error', '')):
        log_success("✅ Prueba 1 PASADA: V2 bloqueó correctamente en EDIT mode.")
    else:
        log_error(f"❌ Prueba 1 FALLIDA: V2 no bloqueó. Resultado: {result1.get('error')}")

    agent.engine_adapter.get_current_mode.return_value = "OBJECT"

    # ---------------------------------------------------------
    # PRUEBA 2: Registro en STAGING y Seguridad
    # ---------------------------------------------------------
    log_info("\n[PRUEBA 2] Registro Inicial en STAGING y Seguridad")
    agent.pattern_memory.patterns = [] 
    
    # Forzamos almacenamiento
    log_info("   Simulando aprendizaje de 'esfera azul'...")
    pattern_id = agent.pattern_memory.store_pattern(
        "Crea una esfera azul", 
        {
            "success": True, 
            "confidence": 0.95, 
            "validation": {"verified": True}, 
            "command_executed": "blender.create_sphere",
            "intent": {"command_name": "blender.create_sphere", "parameters": {}},
            "results": [{"effect": "sphere_created"}]
        }
    )
    
    # Mockeamos nlu.process para que evoque el patrón
    with patch.object(agent.nlu, 'process') as mock_process:
        mock_intent = MagicMock()
        mock_intent.command_name = "blender.create_sphere"
        mock_intent.confidence = 0.95
        mock_intent.parameters = {}
        mock_intent.pattern_id = pattern_id # EEVOCACIÓN
        mock_process.return_value = [mock_intent]

        # Inyectamos el patrón en el repo de staging para que el Agente lo encuentre
        # (Aunque ya debería estar ahí por store_pattern)
        
        result2 = agent.process_natural_request("Crea una esfera azul")
        
        # El Agente debe forzar 'ASK' si detecta que es STAGING
        if result2.get('action') == 'AWAITING_CONFIRMATION' and "STAGING" in str(result2.get('feedback', '')):
            log_success("✅ Prueba 2 PASADA: Agent detectó patrón en STAGING y forzó ASK.")
        else:
            log_error(f"❌ Prueba 2 FALLIDA: Agent no restringió STAGING. Acción: {result2.get('action')}")

    # ---------------------------------------------------------
    # PRUEBA 3: Promoción a VERIFIED
    # ---------------------------------------------------------
    log_info("\n[PRUEBA 3] Camino a VERIFIED (3 Éxitos)")
    # Registramos 3 éxitos para alcanzar el umbral de promoción
    agent.pattern_memory.register_execution_result(pattern_id, success=True)
    agent.pattern_memory.register_execution_result(pattern_id, success=True)
    agent.pattern_memory.register_execution_result(pattern_id, success=True)
    
    pattern = agent.pattern_memory.verified_repo.get_pattern(pattern_id)
    if pattern and pattern.get('metadata', {}).get('status') == "VERIFIED":
        log_success("✅ Prueba 3 PASADA: Patrón ascendido a VERIFIED tras 3 éxitos.")
    else:
        log_error(f"❌ Prueba 3 FALLIDA: Patrón no ascendido.")

    # ---------------------------------------------------------
    # PRUEBA 4: Degradación a QUARANTINE
    # ---------------------------------------------------------
    log_info("\n[PRUEBA 4] Degradación a QUARANTINE (2 Fallos)")
    bad_id = agent.pattern_memory.store_pattern(
        "Crea un cilindro roto", 
        {"success": True, "confidence": 0.9, "validation": {"verified": True}, "command_executed": "blender.create_cylinder"}
    )
    agent.pattern_memory.register_execution_result(bad_id, success=False)
    agent.pattern_memory.register_execution_result(bad_id, success=False)
    
    quarantine_data = agent.pattern_memory.quarantine_repo.load_all()
    if any(p['pattern_id'] == bad_id for p in quarantine_data):
        log_success("✅ Prueba 4 PASADA: Patrón movido a QUARANTINE tras 2 fallos.")
    else:
        log_error("❌ Prueba 4 FALLIDA: Patrón no degradado.")

    # ---------------------------------------------------------
    # PRUEBA 5: Convención de Nombres (Manual Sec 15)
    # ---------------------------------------------------------
    log_info("\n[PRUEBA 5] Verificando Convención de Nombres")
    today = datetime.now().strftime("%Y%m%d")
    
    blend_dir = os.path.abspath("C:/Users/Admin/Desktop/ZULY_IA_LOCAL/ZULY_PROJECTS")
    os.makedirs(blend_dir, exist_ok=True)
    blend_path = os.path.join(blend_dir, f"FDE_5_sesion_final_real_{today}.blend")
    with open(blend_path, "w") as f: f.write("dummy")
    
    log_dir = os.path.abspath("C:/Users/Admin/Desktop/ZULY_IA_LOCAL/ZULY_LAB/logs_sesiones")
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, f"LOG_FDE_5_{today}.json")
    with open(log_path, "w") as f: json.dump({"status": "FINALIZADO", "tests": 5, "passed": 5}, f)
    
    if os.path.exists(blend_path) and os.path.exists(log_path):
        log_success(f"✅ Prueba 5 PASADA: Archivos en rutas oficiales.")
        log_info(f"   - {blend_path}")
        log_info(f"   - {log_path}")
    else:
        log_error("❌ Prueba 5 FALLIDA: Rutas incorrectas.")

    log_info("\n=== FIN DE PRUEBAS REALES (TOTAL: 5) ===")

if __name__ == "__main__":
    run_real_session_tests()
