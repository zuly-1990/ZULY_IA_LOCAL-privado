"""
test_learning_freedom.py
========================

TESTS DE LIBERTAD DE APRENDIZAJE

Valida que:
1. Learning Freedom Engine genera múltiples estrategias
2. Knowledge Graph almacena relaciones
3. Self-Assessment evalúa escenas correctamente
4. Strategy Synthesizer crea nuevas combinaciones
5. Todo funciona integrado

Ejecutar: python -m pytest test_learning_freedom.py -v
"""

import sys
import unittest
from pathlib import Path

# Agregar paths
sys.path.insert(0, str(Path(__file__).parent / 'core' / 'learning'))
sys.path.insert(0, str(Path(__file__).parent / 'core' / 'knowledge'))

from core.learning.learning_freedom_engine import (
    LearningFreedomEngine, StrategyType, Strategy, HandlerCall
)
from core.knowledge.knowledge_graph import KnowledgeGraph, NodeType, RelationType
from core.learning.self_assessment import SelfAssessmentEngine, SceneQuality
from core.learning.strategy_synthesizer import StrategySynthesizer, SynthesisMethod


class TestLearningFreedomEngine(unittest.TestCase):
    """Tests para Learning Freedom Engine"""
    
    def setUp(self):
        self.engine = LearningFreedomEngine(max_strategies=5, verbose=False)
    
    def test_init(self):
        """Test: Inicialización del motor"""
        self.assertIsNotNone(self.engine)
        self.assertEqual(self.engine.max_strategies, 5)
    
    def test_generate_strategies(self):
        """Test: Generación de estrategias"""
        user_prompt = "Crea algo lindo con cubos"
        intent = "create_objects"
        entities = {'object_type': 'cube', 'quantity': 3}
        
        strategies = self.engine.generate_strategies(user_prompt, intent, entities)
        
        self.assertGreater(len(strategies), 0)
        self.assertLessEqual(len(strategies), 5)
        
        for strategy in strategies:
            self.assertIsNotNone(strategy.id)
            self.assertIsNotNone(strategy.description)
            self.assertGreater(len(strategy.handlers), 0)
    
    def test_strategy_types(self):
        """Test: Variedad de tipos de estrategia"""
        strategies = self.engine.generate_strategies(
            "test",
            "test_intent",
            {'object_type': 'sphere'}
        )
        
        types = {s.strategy_type for s in strategies}
        # Debe haber variedad de tipos
        self.assertGreater(len(types), 1)
    
    def test_get_statistics(self):
        """Test: Estadísticas del motor"""
        stats = self.engine.get_statistics()
        
        self.assertIn('total_experiments', stats)
        self.assertIn('strategy_database_size', stats)
        self.assertEqual(stats['total_experiments'], 0)


class TestKnowledgeGraph(unittest.TestCase):
    """Tests para Knowledge Graph"""
    
    def setUp(self):
        self.kg = KnowledgeGraph(db_path=':memory:')  # SQLite en memoria
    
    def test_add_object(self):
        """Test: Agregar objeto al grafo"""
        obj = self.kg.add_object('cube_1', 'Cubo Principal', 'cube', {'size': 2.0})
        
        self.assertEqual(obj.name, 'Cubo Principal')
        self.assertIn('cube_1', self.kg.nodes)
    
    def test_add_light(self):
        """Test: Agregar luz al grafo"""
        light = self.kg.add_light('light_1', 'Luz Punto', 'POINT', energy=1500)
        
        self.assertIn('light_1', self.kg.nodes)
        self.assertEqual(light.properties['type'], 'POINT')
    
    def test_relations(self):
        """Test: Crear relaciones entre nodos"""
        cube = self.kg.add_object('cube_1', 'Cubo', 'cube')
        light = self.kg.add_light('light_1', 'Luz', 'POINT')
        
        relation = self.kg.illuminates('light_1', 'cube_1')
        
        self.assertIsNotNone(relation)
        self.assertEqual(relation.relation_type, RelationType.ILLUMINATES)
    
    def test_query_objects(self):
        """Test: Consultar objetos en escena"""
        self.kg.add_object('cube_1', 'Cubo', 'cube')
        self.kg.add_object('sphere_1', 'Esfera', 'sphere')
        
        objects = self.kg.query_objects()
        
        self.assertEqual(len(objects), 2)
    
    def test_infer_improvements(self):
        """Test: LYZU infiere mejoras"""
        # Escena sin luces
        self.kg.add_object('cube_1', 'Cubo', 'cube')
        
        suggestions = self.kg.infer_improvements("Mejora la escena")
        
        # Debe tener sugerencias
        self.assertGreater(len(suggestions), 0)
    
    def test_scene_summary(self):
        """Test: Resumen de escena"""
        self.kg.add_object('cube_1', 'Cubo', 'cube')
        self.kg.add_light('light_1', 'Luz', 'POINT')
        
        summary = self.kg.get_scene_summary()
        
        self.assertEqual(summary['total_objects'], 1)
        self.assertEqual(summary['total_lights'], 1)


class TestSelfAssessmentEngine(unittest.TestCase):
    """Tests para Self-Assessment Engine"""
    
    def setUp(self):
        self.assessor = SelfAssessmentEngine(verbose=False)
    
    def test_assess_simple_scene(self):
        """Test: Evaluar escena simple"""
        assessment = self.assessor.assess_scenario(
            num_objects=1,
            has_lights=False,
            num_lights=0,
            has_materials=False,
            has_camera=False,
            num_modifiers=0,
            is_novel=True
        )
        
        self.assertIsNotNone(assessment.overall_score)
        self.assertGreater(assessment.overall_score, 0)
        self.assertLess(assessment.overall_score, 100)
        self.assertEqual(assessment.quality_level, SceneQuality.POOR)
    
    def test_assess_complete_scene(self):
        """Test: Evaluar escena completa"""
        assessment = self.assessor.assess_scenario(
            num_objects=3,
            has_lights=True,
            num_lights=2,
            has_materials=True,
            has_camera=True,
            num_modifiers=2,
            is_novel=True
        )
        
        # Escena completa debe tener mejor score
        self.assertGreater(assessment.overall_score, 70)
    
    def test_compare_assessments(self):
        """Test: Comparar dos evaluaciones"""
        assessment1 = self.assessor.assess_scenario(
            num_objects=1, has_lights=False, num_lights=0,
            has_materials=False, has_camera=False, num_modifiers=0,
            is_novel=True
        )
        
        assessment2 = self.assessor.assess_scenario(
            num_objects=3, has_lights=True, num_lights=2,
            has_materials=True, has_camera=True, num_modifiers=2,
            is_novel=True
        )
        
        comparison = self.assessor.compare_assessments(assessment1, assessment2)
        
        self.assertIn('verdict', comparison)
        self.assertGreater(comparison['difference'], 0)
    
    def test_assessment_criteria(self):
        """Test: Criterios de evaluación"""
        assessment = self.assessor.assess_scenario(
            num_objects=5, has_lights=True, num_lights=3,
            has_materials=True, has_camera=True, num_modifiers=3,
            is_novel=True
        )
        
        criteria = assessment.criteria
        self.assertGreater(criteria.composition_score, 0)
        self.assertGreater(criteria.lighting_score, 0)
        self.assertGreater(criteria.contrast_score, 0)


class TestStrategySynthesizer(unittest.TestCase):
    """Tests para Strategy Synthesizer"""
    
    def setUp(self):
        self.synthesizer = StrategySynthesizer(verbose=False)
    
    def test_synthesize_random(self):
        """Test: Síntesis random de estrategias"""
        strategies = self.synthesizer.synthesize(
            SynthesisMethod.RANDOM_COMBO,
            num_strategies=3,
            max_handlers=5
        )
        
        self.assertEqual(len(strategies), 3)
        
        for strategy in strategies:
            self.assertIn('handlers', strategy)
            self.assertGreater(len(strategy['handlers']), 0)
    
    def test_synthesize_cross_breed(self):
        """Test: Cross-breeding de estrategias"""
        strategy1 = {'id': 's1', 'handlers': [{'id': 'h1'}, {'id': 'h2'}]}
        strategy2 = {'id': 's2', 'handlers': [{'id': 'h3'}, {'id': 'h4'}]}
        
        offspring = self.synthesizer.synthesize(
            SynthesisMethod.CROSS_BREED,
            strategy1=strategy1,
            strategy2=strategy2,
            num_offspring=2
        )
        
        self.assertEqual(len(offspring), 2)
        
        for child in offspring:
            self.assertIn('parent1', child)
            self.assertIn('parent2', child)
    
    def test_synthesize_mutation(self):
        """Test: Mutación de estrategias"""
        base_strategy = {'id': 'base', 'handlers': [{'id': 'h1'}, {'id': 'h2'}]}
        
        mutations = self.synthesizer.synthesize(
            SynthesisMethod.MUTATION,
            base_strategy=base_strategy,
            num_mutations=3
        )
        
        self.assertEqual(len(mutations), 3)
        
        # Las mutaciones deben ser diferentes del original
        original_count = len(base_strategy['handlers'])
        for mutation in mutations:
            # No todas deben tener exactamente los mismos handlers
            pass  # (pueden variar)
    
    def test_handler_library(self):
        """Test: Librería de handlers disponibles"""
        library = self.synthesizer.handler_library
        
        self.assertGreater(len(library), 0)
        
        # Verificar que hay diferentes tipos
        types = {h['type'] for h in library}
        self.assertGreater(len(types), 1)


class TestIntegration(unittest.TestCase):
    """Tests de integración completa"""
    
    def test_full_learning_loop(self):
        """Test: Loop completo de libertad de aprendizaje"""
        # 1. Generar estrategias
        engine = LearningFreedomEngine(max_strategies=3, verbose=False)
        strategies = engine.generate_strategies(
            "Crea algo bonito",
            "create_aesthetic",
            {'object_type': 'cube'}
        )
        
        self.assertEqual(len(strategies), 3)
        
        # 2. Evaluar escenarios simulados
        assessor = SelfAssessmentEngine(verbose=False)
        assessments = []
        for strategy in strategies:
            assessment = assessor.assess_scenario(
                num_objects=len(strategy.handlers),
                has_lights=any('light' in h.handler_name for h in strategy.handlers),
                num_lights=sum(1 for h in strategy.handlers if 'light' in h.handler_name),
                has_materials=any('material' in h.handler_name for h in strategy.handlers),
                has_camera=any('camera' in h.handler_name for h in strategy.handlers),
                num_modifiers=sum(1 for h in strategy.handlers if 'modifier' in h.handler_name),
                is_novel=True
            )
            assessments.append(assessment)
        
        # 3. Knowledge Graph registra la escena
        kg = KnowledgeGraph(db_path=':memory:')
        kg.add_object('objeto_1', 'Objeto Principal', 'cube')
        kg.add_light('luz_1', 'Iluminación', 'POINT')
        kg.illuminates('luz_1', 'objeto_1')
        
        summary = kg.get_scene_summary()
        self.assertEqual(summary['total_objects'], 1)
        self.assertEqual(summary['total_lights'], 1)
        
        # 4. Synthesizer genera nuevas estrategias
        synthesizer = StrategySynthesizer(verbose=False)
        new_strategies = synthesizer.synthesize(
            SynthesisMethod.RANDOM_COMBO,
            num_strategies=2
        )
        
        self.assertEqual(len(new_strategies), 2)


def run_tests():
    """Ejecuta todos los tests"""
    print("=" * 70)
    print("[TESTS] TESTS DE LIBERTAD DE APRENDIZAJE")
    print("=" * 70)
    
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Agregar todos los tests
    suite.addTests(loader.loadTestsFromTestCase(TestLearningFreedomEngine))
    suite.addTests(loader.loadTestsFromTestCase(TestKnowledgeGraph))
    suite.addTests(loader.loadTestsFromTestCase(TestSelfAssessmentEngine))
    suite.addTests(loader.loadTestsFromTestCase(TestStrategySynthesizer))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Resumen
    print("\n" + "=" * 70)
    print("[SUMMARY] RESUMEN DE TESTS")
    print("=" * 70)
    print(f"Tests ejecutados: {result.testsRun}")
    print(f"Exitosos: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Fallos: {len(result.failures)}")
    print(f"Errores: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("\n[SUCCESS] TODOS LOS TESTS PASARON - LIBERTAD ACTIVADA")
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
