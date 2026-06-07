#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
demo_learning_freedom.py

Demostracion del Learning Freedom Framework en LYZU Core 3.0
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

def demo_basic_system():
    """Demo 1: Sistema basico sin Learning Freedom"""
    print("\n" + "="*70)
    print("DEMO 1: Sistema Basico (modo reactive)")
    print("="*70)
    
    try:
        from lyzu_core import LYZUCore
        
        lyzu = LYZUCore(mode='reactive', enable_learning_freedom=False)
        print("[OK] LYZU inicializado en modo reactive")
        print("     Version: " + lyzu.version)
        print("     Learning Freedom: DISABLED")
        
    except Exception as e:
        print("[FAIL] Error:", e)

def demo_learning_freedom():
    """Demo 2: Sistema con Learning Freedom Framework"""
    print("\n" + "="*70)
    print("DEMO 2: Learning Freedom Framework (automatico)")
    print("="*70)
    
    try:
        from lyzu_core import LYZUCore
        
        lyzu = LYZUCore(mode='hybrid', enable_learning_freedom=True)
        print("[OK] LYZU inicializado con Learning Freedom")
        print("     Version: " + lyzu.version)
        print("     Mode: hybrid")
        print("     Learning Freedom: ENABLED")
        
        # Información de módulos cargados
        print("\n[OK] Modulos cargados:")
        print("     - LearningFreedomEngine (max_strategies=5)")
        print("     - KnowledgeGraph (SQLite backend)")
        print("     - SelfAssessmentEngine (7 criterios)")
        print("     - StrategySynthesizer (multi-method)")
        
    except Exception as e:
        print("[FAIL] Error:", e)
        import traceback
        traceback.print_exc()

def demo_memory_system():
    """Demo 3: Sistema de memoria"""
    print("\n" + "="*70)
    print("DEMO 3: Sistema de Memoria (500 turns + archival)")
    print("="*70)
    
    try:
        from lyzu_core import LYZUCore
        
        lyzu = LYZUCore(mode='reactive', enable_learning_freedom=True)
        stats = lyzu.memory.get_memory_stats()
        
        print("[OK] Memoria inicializada")
        print("     Session ID: " + str(lyzu.memory.session_id))
        print("     Max turns: " + str(stats['max_turns']))
        print("     Current turns: " + str(stats['turns_in_memory']))
        print("     Memory usage: " + str(stats['memory_usage_pct']) + "%")
        
    except Exception as e:
        print("[FAIL] Error:", e)

def demo_knowledge_graph():
    """Demo 4: Knowledge Graph"""
    print("\n" + "="*70)
    print("DEMO 4: Knowledge Graph (semantic DB)")
    print("="*70)
    
    try:
        from core.knowledge import KnowledgeGraph
        
        kg = KnowledgeGraph(db_path=':memory:')
        print("[OK] Knowledge Graph inicializado")
        
        # Agregar objetos
        kg.add_object("MainCube", "OBJECT", {'color': 'red', 'size': 2.0})
        kg.add_material("RedMaterial", {'color': [1, 0, 0], 'metallic': 0.5})
        kg.add_light("SunLight", {'type': 'SUN', 'energy': 2.0})
        
        print("[OK] Objetos agregados:")
        print("     - MainCube (OBJECT)")
        print("     - RedMaterial (MATERIAL)")
        print("     - SunLight (LIGHT)")
        
    except Exception as e:
        print("[FAIL] Error:", e)

def demo_self_assessment():
    """Demo 5: Self Assessment Engine"""
    print("\n" + "="*70)
    print("DEMO 5: Self Assessment Engine (7 criterios)")
    print("="*70)
    
    try:
        from core.learning.self_assessment import SelfAssessmentEngine
        
        engine = SelfAssessmentEngine(verbose=False)
        
        scene_data = {
            'num_objects': 5,
            'lighting_quality': 8,
            'color_variety': 6,
            'symmetry': 7,
            'novelty': 4,
            'completeness': 9,
            'harmony': 7
        }
        
        result = engine.assess_scenario(scene_data)
        
        print("[OK] Escena evaluada")
        print("     Score: " + str(result['score']) + "/100")
        print("     Quality Level: " + result['quality_level'])
        print("     Composition: " + str(result.get('criteria', {}).get('composition', 0)))
        print("     Lighting: " + str(result.get('criteria', {}).get('lighting', 0)))
        print("     Contrast: " + str(result.get('criteria', {}).get('contrast', 0)))
        
    except Exception as e:
        print("[FAIL] Error:", e)

def main():
    print("\n" + "="*70)
    print("LYZU CORE 3.0 - Learning Freedom Framework Demonstrations")
    print("="*70)
    
    demos = [
        demo_basic_system,
        demo_learning_freedom,
        demo_memory_system,
        demo_knowledge_graph,
        demo_self_assessment
    ]
    
    for demo in demos:
        try:
            demo()
        except Exception as e:
            print("[FAIL] Demo crashed:", e)
    
    print("\n" + "="*70)
    print("DEMOSTRACIONES COMPLETADAS")
    print("="*70)
    print("\nSistema LYZU 3.0 listo para usar.")
    print("Ver REPARACION_PROYECTO_ESTADO.md para detalles completos.")
    print()

if __name__ == '__main__':
    main()
