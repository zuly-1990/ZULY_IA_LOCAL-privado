# test_secure_flow.py
"""
Script de verificación para el flujo seguro de ZULY.
Valida: NLU -> DialogManager -> SafeGuard -> Execution
"""

import sys
import os
from lyzu_core import LYZUCore
from core.utils.logging import log_info, log_success, log_error, log_warning

def test_flow():
    log_info("Iniciando prueba de Flujo Seguro ZULY...")
    
    # Inicializar Core en modo híbrido (para ver confirmaciones)
    core = LYZUCore(mode='hybrid')
    
    cases = [
        {
            'name': 'CASO 1: AMBIGÜEDAD (Baja confianza)',
            'input': 'haz algo raro con cosas',
            'expected': 'Dialog Rejection / Ambigüedad'
        },
        {
            'name': 'CASO 2: PARÁMETROS FALTANTES (Fase 1)',
            'input': 'crear cubo',
            'expected': 'Pending Clarification (falta posicion)'
        },
        {
            'name': 'CASO 3: ACCIÓN CRÍTICA (Fase 4)',
            'input': 'borrar toda la escena',
            'expected': 'Pending Confirmation (SafeGuard)'
        },
        {
            'name': 'CASO 4: FLUJO EXITOSO (Aprobación total)',
            'input': 'crear cubo en posicion 1, 2, 3',
            'expected': 'Success / Pending Approval (Hybrid mode)'
        }
    ]
    
    for case in cases:
        print(f"\n" + "="*50)
        print(f"TEST: {case['name']}")
        print(f"INPUT: {case['input']}")
        print(f"EXPECTED: {case['expected']}")
        print("-"*50)
        
        try:
            result = core.process_user_input(case['input'])
            
            if result.get('pending_clarification'):
                log_warning(f"[DIALOG] STATUS: CLARIFY")
                log_info(f"Mensaje: {result['message']}")
                log_info(f"Detalles: {result.get('details', {})}")
                
            elif result.get('pending_confirmation'):
                log_warning(f"[SAFEGUARD] STATUS: CONFIRM")
                log_info(f"Mensaje: {result['message']}")
                log_info(f"Riesgo: {result.get('details', {}).get('risk')}")
                
            elif result.get('error'):
                log_error(f"[REJECTED] STATUS: ERROR")
                log_error(f"Error: {result['error']}")
                log_info(f"Mensaje: {result.get('message', '')}")
                
            elif result.get('pending_approval'):
                log_success(f"[APPROVED] STATUS: SUCCESS (WAITING FOR OP)")
                log_info(f"Comando listo: {result['command']['name']}")
                log_debug(f"Parámetros: {result['command']['parameters']}")
                
            else:
                log_success(f"[SUCCESS] Resultado directo: {result}")
        
        except Exception as e:
            log_error(f"Fallo crítico en el test: {e}")
            import traceback
            traceback.print_exc()

    print("\n" + "="*50)
    log_success("Pruebas finalizadas.")

if __name__ == "__main__":
    test_flow()
