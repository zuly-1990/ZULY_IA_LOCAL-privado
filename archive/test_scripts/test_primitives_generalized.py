# test_primitives_generalized.py
import sys
from lyzu_core import LYZUCore
from core.utils.logging import log_info, log_success, log_error, log_warning

def run_generalized_test():
    core = LYZUCore(mode='hybrid')
    
    primitives = {
        'cube': {
            'A': "Crea un cubo de tamaño 2.",
            'B': "Crear un cubo en la posición 1,1,1.",
            'C': "Mueve el cubo un poquito."
        },
        'sphere': {
            'A': "Haz una esfera de radio 5.",
            'B': "Crear una esfera en la posición 2,2,2.",
            'C': "Sube la esfera un pelín."
        },
        'cylinder': {
            'A': "Añadir un cilindro de radio 1.",
            'B': "Crear un cilindro en la posición 0,0,5.",
            'C': "Rota el cilindro un poco a la izquierda."
        },
        'plane': {
            'A': "Pon un plano de tamaño 10.",
            'B': "Crear un plano en la posición -1,-1,0.",
            'C': "Escala el plano un poquito más."
        }
    }
    
    results = {}

    log_info("=== INICIANDO MATRIZ DE PRUEBAS ATÓMICAS MULTI-PRIMITIVA ===")
    
    for name, cases in primitives.items():
        print(f"\n" + "#"*40)
        print(f" TESTING PRIMITIVE: {name.upper()} ")
        print("#"*40)
        results[name] = {}
        
        for case_id, text in cases.items():
            print(f"\n[CASO {case_id}] Input: {text}")
            try:
                res = core.process_user_input(text)
                
                status = "UNKNOWN"
                if res.get('pending_clarification'):
                    status = "DIALOG_TRIGGERED"
                    msg = res['message']
                    details = res.get('details', {})
                elif res.get('pending_approval'):
                    status = "EXECUTION_READY"
                    msg = "Validado y aprobado"
                    details = res.get('command', {})
                elif res.get('error') == 'Dialog Rejection' or res.get('pending_clarification') is False:
                    # Si no hay pendiente_clarification pero hay respuesta de diálogo, puede ser rechazo
                    status = "REJECTED_AMBIGUOUS"
                    msg = res.get('message', "Rechazo por ambigüedad")
                    details = {}
                else:
                    status = "ERROR_OR_REJECT"
                    msg = res.get('message', "Desconocido")
                    details = res.get('error', 'N/A')

                results[name][case_id] = {
                    'input': text,
                    'status': status,
                    'msg': msg
                }
                
                # Reporte visual
                if case_id == 'A':
                    if status == "DIALOG_TRIGGERED":
                        log_success(f" - OK: Detectó falta de datos.")
                    else:
                        log_error(f" - FAIL: Debería haber pedido posición.")
                
                elif case_id == 'B':
                    if status == "EXECUTION_READY":
                        log_success(f" - OK: Orden atómica aceptada.")
                    else:
                        log_error(f" - FAIL: Debería haber sido aprobada.")
                
                elif case_id == 'C':
                    if status in ["DIALOG_TRIGGERED", "REJECTED_AMBIGUOUS"]:
                        log_success(f" - OK: Rechazó lenguaje relativo.")
                    else:
                        log_error(f" - FAIL: No debería haber procesado lenguaje vago.")

            except Exception as e:
                log_error(f"FALLO CRÍTICO en {name}/{case_id}: {e}")
                results[name][case_id] = {'status': 'CRASH', 'error': str(e)}

    log_success("\n=== MATRIZ FINALIZADA ===")
    return results

if __name__ == "__main__":
    run_generalized_test()
