"""
Script de Validación Completa del Proyecto Zuly
Verifica que todos los módulos principales se importen y funcionen correctamente.
"""

import sys
from pathlib import Path

# Agregar root al path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Prueba que todos los módulos críticos se importen correctamente."""
    print("=" * 70)
    print("VALIDACIÓN DE IMPORTS - PROYECTO ZULY")
    print("=" * 70)
    
    tests_passed = 0
    tests_failed = 0
    
    # Test 1: Logging
    try:
        from core.utils.logging import log_info, log_warning, log_error
        print("✓ [OK] core.utils.logging")
        tests_passed += 1
    except Exception as e:
        print(f"✗ [FAIL] core.utils.logging: {e}")
        tests_failed += 1
    
    # Test 2: Security/Identity
    try:
        from core.security.identity import is_author_verified, generate_local_key
        verified = is_author_verified()
        print(f"✓ [OK] core.security.identity (Author verified: {verified})")
        tests_passed += 1
    except Exception as e:
        print(f"✗ [FAIL] core.security.identity: {e}")
        tests_failed += 1
    
    # Test 3: Validation
    try:
        from core.validation.state_snapshot import StateSnapshot
        from core.validation.v0_validator import V0Validator
        print("✓ [OK] core.validation (StateSnapshot + V0Validator)")
        tests_passed += 1
    except Exception as e:
        print(f"✗ [FAIL] core.validation: {e}")
        tests_failed += 1
    
    # Test 4: Knowledge
    try:
        from core.knowledge.atomic_dictionary import ATOMIC_DICTIONARY
        categories = len(ATOMIC_DICTIONARY)
        print(f"✓ [OK] core.knowledge.atomic_dictionary ({categories} categories)")
        tests_passed += 1
    except Exception as e:
        print(f"✗ [FAIL] core.knowledge.atomic_dictionary: {e}")
        tests_failed += 1
    
    # Test 5: Agent
    try:
        from core.agent import Agent
        agent = Agent(auto_monitor=False)
        print(f"✓ [OK] core.agent.Agent (State: {agent.operational_state})")
        tests_passed += 1
    except Exception as e:
        print(f"✗ [FAIL] core.agent.Agent: {e}")
        tests_failed += 1
    
    # Test 6: Command Loader
    try:
        from core.command_loader import CommandLoader
        loader = CommandLoader()
        commands = loader.load_commands()
        print(f"✓ [OK] core.command_loader ({len(commands)} commands)")
        tests_passed += 1
    except Exception as e:
        print(f"✗ [FAIL] core.command_loader: {e}")
        tests_failed += 1
    
    # Test 7: NLU
    try:
        from core.utils.nlu import NaturalLanguageProcessor
        print("✓ [OK] core.utils.nlu.NaturalLanguageProcessor")
        tests_passed += 1
    except Exception as e:
        print(f"✗ [FAIL] core.utils.nlu: {e}")
        tests_failed += 1
    
    # Test 8: Intents
    try:
        from core.intents.intent_manager import IntentManager
        from core.intents.entity_extractor import EntityExtractor
        from core.intents.intent_router import IntentRouter
        print("✓ [OK] core.intents (Manager + Extractor + Router)")
        tests_passed += 1
    except Exception as e:
        print(f"✗ [FAIL] core.intents: {e}")
        tests_failed += 1
    
    print("\n" + "=" * 70)
    print(f"RESULTADOS: {tests_passed} PASSED, {tests_failed} FAILED")
    print("=" * 70)
    
    return tests_failed == 0

def test_agent_functionality():
    """Prueba funcionalidad básica del agente."""
    print("\n" + "=" * 70)
    print("VALIDACIÓN DE FUNCIONALIDAD - AGENTE")
    print("=" * 70)
    
    try:
        from core.agent import Agent
        
        agent = Agent(auto_monitor=False)
        
        # Test 1: Estado inicial
        assert agent.operational_state == "Observación", f"Estado inicial incorrecto: {agent.operational_state}"
        print("✓ [OK] Estado inicial: Observación")
        
        # Test 2: Comandos disponibles
        commands = agent.get_available_commands()
        assert len(commands) > 0, "No hay comandos disponibles"
        print(f"✓ [OK] Comandos disponibles: {len(commands)}")
        
        # Test 3: Bloqueo de seguridad
        agent.operational_state = "Bloqueo ético"
        result = agent.process_natural_request("Crea un cubo")
        assert result['success'] == False, "Bloqueo de seguridad no funcionó"
        assert 'Bloqueo' in result.get('error', ''), "Error no menciona bloqueo"
        assert result.get('attempts', 1) == 0, "Se realizaron intentos cuando debería estar bloqueado"
        print("✓ [OK] Bloqueo de seguridad funcional")
        
        # Test 4: Restaurar estado
        agent.operational_state = "Observación"
        print("✓ [OK] Estado restaurado a Observación")
        
        print("\n✓ [SUCCESS] Todas las pruebas de funcionalidad pasaron")
        return True
        
    except Exception as e:
        print(f"\n✗ [FAIL] Error en pruebas de funcionalidad: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_encoding():
    """Prueba que el encoding UTF-8 funciona con emojis."""
    print("\n" + "=" * 70)
    print("VALIDACIÓN DE ENCODING UTF-8")
    print("=" * 70)
    
    try:
        from core.utils.logging import log_info, log_warning, log_success
        
        # Test con emojis
        log_info("Test con emoji: ✓ ✗ ⚠️ 🔒")
        log_warning("Test warning: ⛔ Bloqueado")
        log_success("Test success: ✨ Completado")
        
        print("✓ [OK] Encoding UTF-8 funcional con emojis")
        return True
        
    except UnicodeEncodeError as e:
        print(f"✗ [FAIL] Error de encoding: {e}")
        return False
    except Exception as e:
        print(f"✗ [FAIL] Error inesperado: {e}")
        return False

if __name__ == "__main__":
    print("\n" + "[*] INICIANDO VALIDACION COMPLETA DEL PROYECTO ZULY" + "\n")
    
    # Ejecutar todas las pruebas
    imports_ok = test_imports()
    encoding_ok = test_encoding()
    functionality_ok = test_agent_functionality()
    
    # Resultado final
    print("\n" + "=" * 70)
    print("RESUMEN FINAL")
    print("=" * 70)
    print(f"Imports:        {'✓ PASS' if imports_ok else '✗ FAIL'}")
    print(f"Encoding UTF-8: {'✓ PASS' if encoding_ok else '✗ FAIL'}")
    print(f"Funcionalidad:  {'✓ PASS' if functionality_ok else '✗ FAIL'}")
    print("=" * 70)
    
    if imports_ok and encoding_ok and functionality_ok:
        print("\n✅ PROYECTO VALIDADO EXITOSAMENTE")
        print("Todos los módulos principales funcionan correctamente.\n")
        sys.exit(0)
    else:
        print("\n⚠️ PROYECTO CON ERRORES")
        print("Revise los fallos reportados arriba.\n")
        sys.exit(1)
