#!/usr/bin/env python3
"""
Test del flujo completo: NLU → Dimensiones → Handler Arquitectónico
"""

import sys
sys.path.insert(0, '.')

from core.utils.nlu import NaturalLanguageProcessor
from core.intents.intent_router import IntentRouter
from core.commands.blender_command_registry import register_blender_handlers

def test_nlu_architecture_flow():
    """Test del flujo completo con dimensiones arquitectónicas."""
    
    print("="*70)
    print("TEST: Flujo NLU → Dimensiones → Handler Arquitectónico")
    print("="*70)
    
    # Setup
    router = IntentRouter()
    register_blender_handlers(router)
    nlu = NaturalLanguageProcessor(router.command_handlers)
    
    test_cases = [
        ("crea habitación 4x5", 4.0, 5.0, 2.5, "2D básico"),
        ("crea habitación 3x4x2.8", 3.0, 4.0, 2.8, "3D completo"),
        ("crea cuarto 6 por 8 metros", 6.0, 8.0, 2.5, "Por + metros"),
        ("nueva habitación ancho 5m profundidad 6m alto 3m", 5.0, 6.0, 3.0, "Dimensiones explícitas"),
    ]
    
    passed = 0
    failed = 0
    
    for command, exp_ancho, exp_prof, exp_alt, desc in test_cases:
        print(f"\n📝 Input: \"{command}\"")
        print(f"   Desc: {desc}")
        
        # Procesar con NLU
        intents = nlu.process(command)
        
        if not intents:
            print(f"   ✗ FAIL: No se detectaron intenciones")
            failed += 1
            continue
        
        best_intent = intents[0]
        params = best_intent.parameters
        
        # Verificar dimensiones
        ancho = params.get('ancho')
        prof = params.get('profundidad')
        alt = params.get('altura')
        
        print(f"   Detectado: {best_intent.command_name}")
        print(f"   Params: ancho={ancho}, prof={prof}, alt={alt}")
        
        # Validar
        ok_ancho = ancho == exp_ancho
        ok_prof = prof == exp_prof
        ok_alt = alt == exp_alt
        
        if ok_ancho and ok_prof and ok_alt:
            print(f"   ✓ PASS")
            passed += 1
        else:
            print(f"   ✗ FAIL - Expected: ancho={exp_ancho}, prof={exp_prof}, alt={exp_alt}")
            failed += 1
    
    print("\n" + "="*70)
    print(f"RESULTADO: {passed}/{passed+failed} tests pasaron")
    print("="*70)
    
    return failed == 0

if __name__ == "__main__":
    success = test_nlu_architecture_flow()
    sys.exit(0 if success else 1)
