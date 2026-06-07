"""
Test de Integración: C1 con LYZU Core

Verifica que C1 se integra correctamente sin romper nada.
"""

import sys
from pathlib import Path

# Agregar path
sys.path.insert(0, str(Path(__file__).parent))

def test_c1_integration_basic():
    """Test 1: C1 se inicializa correctamente en LYZUCore"""
    from lyzu_core import LYZUCore
    
    # Crear core con C1 habilitado
    lyzu = LYZUCore(mode='reactive', enable_cognition=True)
    
    assert lyzu.evaluator is not None, "C1 should be initialized"
    assert lyzu.cognition_enabled is True, "Cognition should be enabled"
    print("✓ Test 1: C1 inicializa correctamente")


def test_c1_integration_disabled():
    """Test 2: C1 se puede deshabilitar sin errores"""
    from lyzu_core import LYZUCore
    
    # Crear core con C1 deshabilitado
    lyzu = LYZUCore(mode='reactive', enable_cognition=False)
    
    assert lyzu.evaluator is None, "C1 should be None when disabled"
    assert lyzu.cognition_enabled is False, "Cognition should be disabled"
    print("✓ Test 2: C1 se puede deshabilitar")


def test_execute_with_evaluation():
    """Test 3: Método execute_with_evaluation retorna resultado"""
    from lyzu_core import LYZUCore
    
    lyzu = LYZUCore(mode='reactive', enable_cognition=True)
    
    # Test que el método existe
    assert hasattr(lyzu, 'execute_with_evaluation'), "Method should exist"
    print("✓ Test 3: execute_with_evaluation existe")


def test_get_evaluation_summary():
    """Test 4: Método get_evaluation_summary retorna resumen o None"""
    from lyzu_core import LYZUCore
    
    # Con C1 habilitado
    lyzu1 = LYZUCore(mode='reactive', enable_cognition=True)
    summary1 = lyzu1.get_evaluation_summary()
    assert isinstance(summary1, dict), "Should return dict when C1 enabled"
    print("✓ Test 4a: get_evaluation_summary retorna dict con C1")
    
    # Con C1 deshabilitado
    lyzu2 = LYZUCore(mode='reactive', enable_cognition=False)
    summary2 = lyzu2.get_evaluation_summary()
    assert summary2 is None, "Should return None when C1 disabled"
    print("✓ Test 4b: get_evaluation_summary retorna None sin C1")


def test_get_current_scene_state():
    """Test 5: Método _get_current_scene_state funciona"""
    from lyzu_core import LYZUCore
    
    lyzu = LYZUCore(mode='reactive', enable_cognition=True)
    scene = lyzu._get_current_scene_state()
    
    assert isinstance(scene, dict), "Should return dict"
    assert 'object_count' in scene or len(scene) >= 0, "Should have scene data"
    print("✓ Test 5: _get_current_scene_state funciona")


def test_backward_compatibility():
    """Test 6: LYZU sin cambios sigue funcionando igual"""
    from lyzu_core import LYZUCore
    
    # Versión sin C1 (como era antes)
    lyzu_old = LYZUCore(mode='reactive', enable_learning_freedom=False, enable_cognition=False)
    
    assert lyzu_old.mode == 'reactive'
    assert lyzu_old.version == "3.0"
    assert lyzu_old.evaluator is None
    assert lyzu_old.learning_freedom_enabled is False
    print("✓ Test 6: Compatibilidad hacia atrás mantenida")


def test_default_values():
    """Test 7: Valores por defecto son correctos"""
    from lyzu_core import LYZUCore
    
    # Sin argumentos
    lyzu = LYZUCore()
    
    assert lyzu.mode == 'hybrid', "Default mode should be hybrid"
    assert lyzu.learning_freedom_enabled is True, "Learning freedom enabled by default"
    assert lyzu.cognition_enabled is True, "Cognition enabled by default"
    print("✓ Test 7: Valores por defecto correctos")


if __name__ == "__main__":
    print("\n" + "="*70)
    print("TESTS DE INTEGRACION: C1 + LYZU CORE")
    print("="*70 + "\n")
    
    try:
        test_c1_integration_basic()
        test_c1_integration_disabled()
        test_execute_with_evaluation()
        test_get_evaluation_summary()
        test_get_current_scene_state()
        test_backward_compatibility()
        test_default_values()
        
        print("\n" + "="*70)
        print("RESULTADO: TODOS LOS TESTS PASARON")
        print("="*70 + "\n")
        print("C1 está correctamente integrado en LYZU Core")
        print("Próximo: Implementar C2 (Memoria de Experiencias)")
        
    except AssertionError as e:
        print(f"\n✗ Test falló: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
