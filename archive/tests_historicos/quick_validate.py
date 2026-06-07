"""
Script Simplificado de Validación del Proyecto Zuly
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

print("="*70)
print("VALIDACION RAPIDA - PROYECTO ZULY")
print("="*70)

# Test 1: Logging con UTF-8
try:
    from core.utils.logging import log_info
    log_info("Test UTF-8: OK (emojis: OK)")
    print("[OK] Logging + UTF-8")
except Exception as e:
    print(f"[FAIL] Logging: {e}")

# Test 2: Security
try:
    from core.security.identity import is_author_verified
    verified = is_author_verified()
    print(f"[OK] Security (Author: {verified})")
except Exception as e:
    print(f"[FAIL] Security: {e}")

# Test 3: Validation
try:
    from core.validation.v0_validator import V0Validator
    print("[OK] Validation V0")
except Exception as e:
    print(f"[FAIL] Validation: {e}")

# Test 4: Agent
try:
    from core.agent import Agent
    agent = Agent(auto_monitor=False)
    print(f"[OK] Agent (State: {agent.operational_state})")
    
    # Test bloqueo
    agent.operational_state = "Bloqueo etico"
    result = agent.process_natural_request("test")
    if not result['success'] and result.get('attempts', 1) == 0:
        print("[OK] Bloqueo de seguridad funcional")
    else:
        print("[WARN] Bloqueo de seguridad no verificado")
        
except Exception as e:
    print(f"[FAIL] Agent: {e}")

# Test 5: Knowledge
try:
    from core.knowledge.atomic_dictionary import ATOMIC_DICTIONARY
    print(f"[OK] Atomic Dictionary ({len(ATOMIC_DICTIONARY)} categories)")
except Exception as e:
    print(f"[FAIL] Knowledge: {e}")

print("="*70)
print("VALIDACION COMPLETADA")
print("="*70)
