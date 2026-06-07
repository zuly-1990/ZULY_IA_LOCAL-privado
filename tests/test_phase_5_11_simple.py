# -*- coding: utf-8 -*-
"""
Test Simple: Validacion Fase 5.11 - Bloqueo por Estado Operacional
Sin caracteres Unicode para evitar problemas de encoding
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.agent import Agent


def main():
    print("="*70)
    print("TEST FASE 5.11: Bloqueo por Estado Operacional")
    print("="*70)
    
    # Crear agente
    agent = Agent(auto_monitor=False)
    
    # Forzar estado de bloqueo
    agent.operational_state = "Bloqueo etico"
    print(f"\nEstado forzado a: {agent.operational_state}")
    
    # Intentar ejecutar comando
    print("\nIntentando ejecutar comando...")
    result = agent.process_natural_request("Crea un cubo")
    
    # Verificar resultado
    print("\n[VERIFICACION]")
    passed = 0
    total = 5
    
    if result['success'] == False:
        print("  [OK] 1. Ejecucion bloqueada")
        passed += 1
    else:
        print("  [FAIL] 1. Comando se ejecuto")
    
    if 'error' in result:
        print("  [OK] 2. Error presente")
        passed += 1
    else:
        print("  [FAIL] 2. Sin error")
    
    if 'operational_state' in result:
        print("  [OK] 3. Estado reportado")
        passed += 1
    else:
        print("  [FAIL] 3. Estado no reportado")
    
    if 'reason' in result:
        print("  [OK] 4. Razon presente")
        passed += 1
    else:
        print("  [FAIL] 4. Sin razon")
    
    if result.get('attempts', 0) == 0:
        print("  [OK] 5. Cero intentos")
        passed += 1
    else:
        print("  [FAIL] 5. Hubo intentos")
    
    print(f"\n[RESULTADO] {passed}/{total} checks pasados")
    
    if passed == total:
        print("\n[SUCCESS] FASE 5.11 VALIDADA")
        return 0
    else:
        print("\n[FAILED] FASE 5.11 FALLO")
        return 1


if __name__ == "__main__":
    sys.exit(main())
