import sys
import os
import json
from datetime import datetime

# Agregar root al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.agent import Agent
from core.utils.logging import log_info, log_success, log_warning

def run_u3_stabilization():
    print("\n" + "="*80)
    print("🚀 ZULY ULTRA EMERGENCIA — U3: PRUEBAS REALES (ESTABILIZACIÓN)")
    print("="*80 + "\n")

    # 1. Inicializar Agente en modo simulación (Mock) para validar lógica
    log_info("[1/8] Inicializando Agente (force_mock=True)...")
    agent = Agent(force_mock=True)
    log_success("Agente listo.")

    # Secuencia del Manual de Blender
    test_sequence = [
        ("Limpia la escena", "Setup inicial"),
        ("Crea un cubo dorado en 0,0,0", "Creación con aprendizaje (Nuevo)"),
        ("Crea un cubo dorado en 0,0,0", "Prueba de Deduplicación (Debe usar memoria)"),
        ("Crea una esfera plateada en 3,0,0", "Creación 2 (Evidencia física)"),
        ("Mueve el cubo a 10,0,0", "Transformación (Registro de cambio)"),
        ("Escala el cubo a 2", "Escalado"),
        ("Dime la hora", "Saneamiento V0 (No debe memorizar - No 3D)")
    ]

    results_log = []

    for i, (cmd, desc) in enumerate(test_sequence, 1):
        print(f"\n[{i}/{len(test_sequence)}] TEST: {desc}")
        print(f"  > Input: '{cmd}'")
        
        # Procesar
        result = agent.process_natural_request(cmd)
        
        # Verificar éxito
        success = result.get('success', False)
        status = "✅ PASÓ" if success else "❌ FALLÓ"
        
        # Verificar si memorizó
        # NOTA: En MockAdapter, store_pattern se llama pero depende de los resultados simulados.
        # can_memorize retornará True si hay snapshots (que MockAdapter provee).
        
        print(f"  Resultado: {status}")
        if not success:
            print(f"  Error: {result.get('error', 'Desconocido')}")
        
        results_log.append({
            'step': i,
            'command': cmd,
            'description': desc,
            'success': success,
            'pattern_status': "N/A" # Se verificará en el resumen final de la memoria
        })

    # 2. Resumen de Memoria (Verificar que no hay duplicados basura)
    print("\n" + "="*80)
    print("📊 RESUMEN DE MEMORIA (AUDITORÍA TRAS U3)")
    print("="*80)
    
    stats = agent.pattern_memory.get_stats()
    print(f"Total patrones en Staging: {stats['total_patterns']}")
    print(f"Total usos registrados: {stats['total_uses']}")
    
    # Listar patrones para asegurar que no hay duplicados de "cubo dorado"
    patterns = agent.pattern_memory.patterns
    found_cubes = [p for p in patterns if "cubo dorado" in p['user_request'].lower()]
    
    if len(found_cubes) > 1:
        log_warning(f"⚠️ FALLO DE DEDUPLICACIÓN: Se encontraron {len(found_cubes)} patrones para el mismo comando.")
    else:
        log_success("✅ DEDUPLICACIÓN CONFIRMADA: Solo un patrón único para 'cubo dorado'.")

    # Verificar si "Dime la hora" se memorizó (NO debería)
    time_patterns = [p for p in patterns if "dime la hora" in p['user_request'].lower()]
    if len(time_patterns) > 0:
        log_warning("⚠️ FALLO DE SANEAMIENTO: Se memorizó un comando no-3D ('dime la hora').")
    else:
        log_success("✅ SANEAMIENTO CONFIRMADO: El comando 'dime la hora' fue ignorado por la memoria.")

    print("\n" + "="*80)
    print("🏁 PRUEBAS U3 COMPLETADAS")
    print("="*80 + "\n")

if __name__ == "__main__":
    run_u3_stabilization()
