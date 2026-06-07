#!/usr/bin/env python3
"""
Test del NLU para dimensiones arquitectónicas.
"""

import sys
sys.path.insert(0, '.')

from core.intents.entity_extractor import EntityExtractor

def test_architectural_extraction():
    """Test de extracción de dimensiones arquitectónicas."""
    
    extractor = EntityExtractor()
    
    test_cases = [
        # (input, expected_ancho, expected_prof, expected_altura, descripcion)
        ("crea habitación 4x5", 4.0, 5.0, 2.5, "2D básico con inferencia"),
        ("habitación 4 x 5 metros", 4.0, 5.0, 2.5, "2D con espacios y unidades"),
        ("cuarto 4x5x2.5", 4.0, 5.0, 2.5, "3D completo"),
        ("room 3.5x4.2x2.8", 3.5, 4.2, 2.8, "3D con decimales"),
        ("casa ancho 6m profundidad 8m altura 3m", 6.0, 8.0, 3.0, "Dimensiones explícitas"),
        ("muro largo 5m alto 2.5m", None, 5.0, 2.5, "Muro sin ancho"),
        ("columna 0.4x0.4x3", 0.4, 0.4, 3.0, "Columna pequeña"),
        ("edificio 10 por 15", 10.0, 15.0, 2.5, "Por en lugar de x"),
    ]
    
    print("="*70)
    print("TEST: Extracción de Dimensiones Arquitectónicas")
    print("="*70)
    
    passed = 0
    failed = 0
    
    for command, exp_ancho, exp_prof, exp_alt, desc in test_cases:
        entities = extractor.extract(command)
        dims = entities.get('dimensiones')
        
        if dims:
            actual = dims.value
            ok_ancho = (exp_ancho is None and actual['ancho'] is None) or \
                       (exp_ancho is not None and actual['ancho'] == exp_ancho)
            ok_prof = (exp_prof is None and actual['profundidad'] is None) or \
                      (exp_prof is not None and actual['profundidad'] == exp_prof)
            ok_alt = actual['altura'] == exp_alt
            
            status = "✓ PASS" if (ok_ancho and ok_prof and ok_alt) else "✗ FAIL"
            
            if ok_ancho and ok_prof and ok_alt:
                passed += 1
            else:
                failed += 1
            
            print(f"\n{status} | {desc}")
            print(f"  Input: \"{command}\"")
            print(f"  Expected: ancho={exp_ancho}, prof={exp_prof}, alt={exp_alt}")
            print(f"  Actual:   ancho={actual['ancho']}, prof={actual['profundidad']}, alt={actual['altura']}")
            print(f"  Confidence: {dims.confidence:.2f}")
        else:
            if exp_ancho is None and exp_prof is None:
                print(f"\n✓ PASS | {desc} (no dims expected)")
                passed += 1
            else:
                print(f"\n✗ FAIL | {desc}")
                print(f"  Input: \"{command}\"")
                print(f"  Expected: dims, Got: None")
                failed += 1
    
    print("\n" + "="*70)
    print(f"RESULTADO: {passed} passed, {failed} failed")
    print("="*70)
    
    return failed == 0

if __name__ == "__main__":
    success = test_architectural_extraction()
    sys.exit(0 if success else 1)
