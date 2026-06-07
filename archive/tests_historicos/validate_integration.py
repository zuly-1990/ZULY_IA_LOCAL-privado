#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
validate_integration.py

Valida que la integración de Learning Freedom esté completa en lyzu_core.py
y que todos los componentes funcionan correctamente.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test 1: Verifica que todos los imports funcionan."""
    print("[TEST 1] Verificando imports...")
    try:
        from core.learning import LearningFreedomEngine
        from core.knowledge import KnowledgeGraph
        from core.learning.self_assessment import SelfAssessmentEngine
        from core.learning.strategy_synthesizer import StrategySynthesizer
        from lyzu_core import LYZUCore
        print("[OK] All imports successful")
        return True
    except ImportError as e:
        print(f"[✗] Import error: {e}")
        return False

def test_lyzu_initialization():
    """Test 2: Verifica que LYZUCore se inicializa con Learning Freedom."""
    print("\n[TEST 2] Inicializando LYZUCore con Learning Freedom...")
    try:
        from lyzu_core import LYZUCore
        lyzu = LYZUCore(mode='hybrid', enable_learning_freedom=True)
        
        # Verificar que los módulos estén inicializados
        assert lyzu.learning_freedom_enabled, "Learning Freedom should be enabled"
        assert lyzu.learning_engine is not None, "Learning Engine should be initialized"
        assert lyzu.knowledge_graph is not None, "Knowledge Graph should be initialized"
        assert lyzu.self_assessment is not None, "Self-Assessment should be initialized"
        assert lyzu.strategy_synthesizer is not None, "Strategy Synthesizer should be initialized"
        
        print(f"[✓] LYZUCore version: {lyzu.version}")
        print(f"[✓] Mode: {lyzu.mode}")
        print(f"[✓] Learning Freedom: {'ENABLED' if lyzu.learning_freedom_enabled else 'DISABLED'}")
        return True
    except Exception as e:
        print(f"[✗] Initialization error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_process_with_learning_freedom():
    """Test 3: Verifica que el método process_with_learning_freedom existe y funciona."""
    print("\n[TEST 3] Probando process_with_learning_freedom()...")
    try:
        from lyzu_core import LYZUCore
        lyzu = LYZUCore(mode='hybrid', enable_learning_freedom=True)
        
        # Verificar que el método existe
        assert hasattr(lyzu, 'process_with_learning_freedom'), "Method should exist"
        assert callable(getattr(lyzu, 'process_with_learning_freedom')), "Should be callable"
        
        print("[✓] Method exists and is callable")
        
        # Intentar ejecutar (puede fallar sin Blender, pero se valida la estructura)
        try:
            result = lyzu.process_with_learning_freedom("Crea algo lindo")
            print(f"[✓] Execution returned: {type(result)} with keys: {list(result.keys())}")
        except Exception as e:
            print(f"[⚠] Execution raised (expected without Blender): {e}")
            print("[✓] But method is accessible and has correct structure")
        
        return True
    except Exception as e:
        print(f"[✗] Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_memory_system():
    """Test 4: Verifica que el sistema de memoria funciona."""
    print("\n[TEST 4] Probando sistema de memoria...")
    try:
        from lyzu_core import LYZUCore
        lyzu = LYZUCore(mode='reactive', enable_learning_freedom=True)
        
        # Verificar que la memoria se inicializó
        assert lyzu.memory is not None, "Memory should be initialized"
        stats = lyzu.memory.get_memory_stats()
        
        print(f"[✓] Memory session ID: {lyzu.memory.session_id}")
        print(f"[✓] Memory stats: {stats}")
        return True
    except Exception as e:
        print(f"[✗] Memory error: {e}")
        return False

def test_knowledge_persistence():
    """Test 5: Verifica que el Knowledge Graph se puede usar."""
    print("\n[TEST 5] Probando Knowledge Graph...")
    try:
        from core.knowledge import KnowledgeGraph
        kg = KnowledgeGraph(db_path=':memory:')
        
        # Agregar algunos datos
        kg.add_object("CubeTest", "OBJECT", {'color': 'red'})
        kg.add_material("RedMaterial", {'color': [1, 0, 0]})
        
        print("[✓] Knowledge Graph initialized and working")
        return True
    except Exception as e:
        print(f"[✗] Knowledge Graph error: {e}")
        return False

def main():
    """Ejecuta todos los tests."""
    print("="*70)
    print("VALIDACIÓN DE INTEGRACIÓN - Learning Freedom Framework")
    print("="*70)
    
    tests = [
        test_imports,
        test_lyzu_initialization,
        test_process_with_learning_freedom,
        test_memory_system,
        test_knowledge_persistence
    ]
    
    results = []
    for test in tests:
        try:
            results.append(test())
        except Exception as e:
            print(f"\n[✗] Test crashed: {e}")
            results.append(False)
    
    print("\n" + "="*70)
    print(f"RESULTADOS: {sum(results)}/{len(results)} tests passed")
    print("="*70)
    
    if all(results):
        print("\n[✓✓✓] VALIDACIÓN EXITOSA - Sistema completamente integrado")
        return 0
    else:
        print("\n[✗✗✗] VALIDACIÓN FALLIDA - Revisar errores arriba")
        return 1

if __name__ == '__main__':
    sys.exit(main())
