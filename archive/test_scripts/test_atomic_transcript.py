# test_atomic_transcript.py
import sys
from lyzu_core import LYZUCore
from core.utils.logging import log_info, log_success, log_error, log_warning

def run_atomic_test():
    core = LYZUCore(mode='hybrid')
    
    # Transcripción de prueba (dividida en frases para el procesador)
    transcript = [
        "Crea un cubo de tamaño 2.",                          # Falta posición (Trigger Dialog)
        "Crear un cubo en la posición 0,0,0.",               # Atómico perfecto
        "Mueve el cubo un poquito hacia arriba.",            # Lenguaje relativo (Trigger Rejection/Dialog)
        "Mueve el objeto cubo a la posición 0,0,10."         # Atómico perfecto
    ]
    
    log_info("--- INICIANDO PRUEBA DE TRANSCRIPCIÓN ATÓMICA ---")
    
    for i, line in enumerate(transcript):
        print(f"\n[FRASE {i+1}]: {line}")
        result = core.process_user_input(line)
        
        if result.get('pending_clarification'):
            log_warning(f"RESULTADO: DIALOG REQUERIDO")
            log_info(f"Mensaje Zuly: {result['message']}")
            if 'missing' in result.get('details', {}):
                log_info(f"Faltan parámetros: {result['details']['missing']}")
                
        elif result.get('error') == 'Dialog Rejection':
            log_error(f"RESULTADO: RECHAZO POR AMBIGÜEDAD")
            log_info(f"Mensaje Zuly: {result['message']}")
            
        elif result.get('pending_approval'):
            log_success(f"RESULTADO: LISTO PARA EJECUCIÓN (ATÓMICO)")
            log_info(f"Comando: {result['command']['name']}")
            log_info(f"Parámetros: {result['command']['parameters']}")
            
        else:
            log_info(f"RESULTADO: {result.get('error', 'Desconocido')}")

    log_success("\n--- FIN DE LA PRUEBA ---")

if __name__ == "__main__":
    run_atomic_test()
