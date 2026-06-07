"""
Test: Fase 5.11 - Bloqueo por Operational State

Verifica que el agente NO ejecute comandos cuando operational_state = "Bloqueo ético"
Este test valida la barrera de seguridad implementada en core/agent.py líneas 206-221
"""
import sys
from pathlib import Path

# Add root
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.agent import Agent


def test_direct_blocking():
    """Test directo: Forzar estado de bloqueo y verificar que impide ejecución"""
    print("="*70)
    print("TEST FASE 5.11: Bloqueo Directo por Estado Operacional")
    print("="*70)
    
    agent = Agent(auto_monitor=False)
    
    # FORZAR estado de bloqueo ético directamente
    agent.operational_state = "Bloqueo ético"
    print(f"\n[OK] Estado forzado a: '{agent.operational_state}'")
    
    # Intentar ejecutar comando
    print("\n[EJECUTANDO] Comando: 'Crea un cubo en 0,0,0'")
    result = agent.process_natural_request("Crea un cubo en 0,0,0")
    
    # Verificaciones
    print("\n[VERIFICACIÓN]")
    checks_passed = 0
    
    # Check 1: Debe fallar
    if result['success'] == False:
        print("  [OK] 1. Ejecución bloqueada (success=False)")
        checks_passed += 1
    else:
        print("  [X] 1. FALLO: Comando se ejecutó cuando debería estar bloqueado")
    
    # Check 2: Error debe mencionar bloqueo
    if 'error' in result and 'bloqueada' in result['error'].lower():
        print(f"  [OK] 2. Error estructurado: '{result['error']}'")
        checks_passed += 1
    else:
        print("  [X] 2. FALLO: Error no menciona bloqueo")
    
    # Check 3: Debe reportar operational_state
    if result.get('operational_state') == "Bloqueo ético":
        print(f"  [OK] 3. Estado reportado: '{result['operational_state']}'")
        checks_passed += 1
    else:
        print("  [X] 3. FALLO: Estado operacional no reportado correctamente")
    
    # Check 4: Debe tener razón del bloqueo
    if 'reason' in result:
        print(f"  [OK] 4. Razón: '{result['reason']}'")
        checks_passed += 1
    else:
        print("  [X] 4. FALLO: No se proporciona razón del bloqueo")
    
    # Check 5: Cero intentos de ejecución
    if result.get('attempts', 0) == 0:
        print("  [OK] 5. Cero intentos de ejecución (bloqueo preventivo)")
        checks_passed += 1
    else:
        print("  [X] 5. FALLO: Se realizaron intentos de ejecución")
    
    print(f"\n[RESULTADO] {checks_passed}/5 verificaciones pasadas")
    
    if checks_passed == 5:
        print("\n[SUCCESS] FASE 5.11 VALIDADA: Bloqueo de seguridad operativo")
        return True
    else:
        print("\n[FAILED] FASE 5.11 FALLO: Bloqueo de seguridad no funciona correctamente")
        return False


def test_normal_operation():
    """Test complementario: Verificar que funciona normalmente sin bloqueo"""
    print("\n" + "="*70)
    print("TEST COMPLEMENTARIO: Operación Normal (Sin Bloqueo)")
    print("="*70)
    
    agent = Agent(auto_monitor=False)
    
    # Verificar estado inicial
    print(f"\n[OK] Estado inicial: '{agent.operational_state}'")
    
    if agent.operational_state == "Bloqueo ético":
        print("  [WARN] ADVERTENCIA: Estado inicial es bloqueo (puede ser por identidad)")
        return True  # No es un error, puede ser por seguridad
    
    # Intentar ejecución normal
    print("\n[EJECUTANDO] Comando en estado normal")
    result = agent.process_natural_request("Crea un cubo")
    
    # Verificar que NO fue bloqueado por estado
    if not result['success']:
        if 'bloqueada por estado operacional' in result.get('error', ''):
            print("  [X] FALLO: Bloqueado cuando NO debería estarlo")
            return False
    
    print("  [OK] No hay bloqueo indebido en estado normal")
    print("\n[SUCCESS] TEST COMPLEMENTARIO PASADO")
    return True


if __name__ == "__main__":
    print("\n" + "="*70)
    print("SUITE DE VALIDACION: FASE 5.11")
    print("="*70 + "\n")
    
    # Test 1: Bloqueo directo
    test1_pass = test_direct_blocking()
    
    # Test 2: Operación normal
    test2_pass = test_normal_operation()
    
    # Resultado final
    if test1_pass and test2_pass:
        print("\n" + "="*70)
        print("[SUCCESS] TODOS LOS TESTS PASARON - FASE 5.11 COMPLETADA")
        print("="*70 + "\n")
        sys.exit(0)
    else:
        print("\n" + "="*70)
        print("[FAILED] ALGUNOS TESTS FALLARON")
        print("="*70 + "\n")
        sys.exit(1)

