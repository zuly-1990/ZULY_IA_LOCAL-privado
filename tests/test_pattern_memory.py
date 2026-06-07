"""
Tests Comprehensivos para PatternMemory - Fase 5.13

Valida las 5 condiciones obligatorias:
1. validation.verified == True
2. confidence >= 0.85
3. success == True
4. mode != HYBRID
5. attempts == 1
"""

import sys
import os
import unittest
import json
import tempfile

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.learning.pattern_memory import PatternMemory


class TestPatternMemory(unittest.TestCase):
    
    def setUp(self):
        """Setup para cada test - usa carpeta temporal"""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.memory = PatternMemory(storage_dir=self.temp_dir.name)
    
    def tearDown(self):
        """Cleanup después de cada test"""
        self.temp_dir.cleanup()
    
    def test_memorization_success_all_conditions_met(self):
        """Test: Memorización exitosa cuando se cumplen las 5 condiciones"""
        print("\n[TEST] Memorización exitosa - Todas las condiciones")
        
        result = {
            'success': True,
            'confidence': 0.95,
            'validation': {'verified': True, 'details': 'Objeto creado'},
            'mode': 'REACTIVE',
            'operational_state': 'Ejecución con Aprendizaje',
            'attempts': 1,
            'scene_state_pre': {'objects': ['Cube']}, # Snapshot no vacío
            'scene_state': {'objects': ['Cube']}, # Snapshot no vacío
            'command_executed': 'create_cube',
            'effect': 'create',
            'results': [{'effect': 'create', 'result': {'name': 'Cube'}}]
        }
        
        pattern_id = self.memory.store_pattern("Crea un cubo", result)
        
        self.assertIsNotNone(pattern_id)
        self.assertEqual(len(self.memory.patterns), 1)
        print(f"  ✓ Patrón memorizado: {pattern_id[:8]}...")

    def test_deduplication(self):
        """Test: No memoriza patrones duplicados (Condición 1c)"""
        print("\n[TEST] Deduplicación - No repetir aprendizaje")
        
        result = {
            'success': True,
            'confidence': 0.95,
            'validation': {'verified': True, 'details': 'Objeto creado'},
            'mode': 'REACTIVE',
            'attempts': 1,
            'scene_state_pre': {'objects': ['Cube']}, # Snapshot no vacío
            'scene_state': {'objects': ['Cube', 'Sphere']}, # Snapshot no vacío
            'results': [{'effect': 'create'}]
        }
        
        # Guardar primer patrón
        id1 = self.memory.store_pattern("Crea un cubo", result)
        self.assertIsNotNone(id1)
        self.assertEqual(len(self.memory.patterns), 1)
        
        # Intentar guardar duplicado idéntico
        id2 = self.memory.store_pattern("Crea un cubo", result)
        self.assertEqual(id1, id2, "Debe retornar el ID del patrón existente")
        self.assertEqual(len(self.memory.patterns), 1, "No debe haber agregado un nuevo patrón")
        
        # Intentar guardar duplicado muy similar
        id3 = self.memory.store_pattern("crea un CubO", result)
        self.assertEqual(id1, id3, "Debe detectar similitud textual (insensible a caja)")
        self.assertEqual(len(self.memory.patterns), 1)
        
        print("  ✓ Deduplicación funcional (evitados 2 duplicados)")
    
    def test_rejection_v0_failed(self):
        """Test: Rechazo cuando V0 falla (Condición 1)"""
        print("\n[TEST] Rechazo - V0 falló")
        
        result = {
            'success': True,
            'confidence': 0.95,
            'validation': {'verified': False},  # ← V0 FALLÓ
            'mode': 'REACTIVE',
            'attempts': 1,
            'scene_state_pre': {'objects': ['Cube']},
            'scene_state': {'objects': ['Cube']}
        }
        
        pattern_id = self.memory.store_pattern("Crea un cubo", result)
        
        self.assertIsNone(pattern_id)
        self.assertEqual(len(self.memory.patterns), 0)
        print("  ✓ Patrón rechazado correctamente (V0 no pasó)")
    
    def test_rejection_low_confidence(self):
        """Test: Rechazo cuando confianza < 0.85 (Condición 2)"""
        print("\n[TEST] Rechazo - Baja confianza")
        
        result = {
            'success': True,
            'confidence': 0.70,  # ← BAJA CONFIANZA
            'validation': {'verified': True},
            'mode': 'REACTIVE',
            'attempts': 1,
            'scene_state_pre': {'objects': ['Cube']},
            'scene_state': {'objects': ['Cube']}
        }
        
        pattern_id = self.memory.store_pattern("Crea un cubo", result)
        
        self.assertIsNone(pattern_id)
        self.assertEqual(len(self.memory.patterns), 0)
        print("  ✓ Patrón rechazado correctamente (confianza < 0.85)")
    
    def test_rejection_execution_failed(self):
        """Test: Rechazo cuando ejecución falla (Condición 3)"""
        print("\n[TEST] Rechazo - Ejecución fallida")
        
        result = {
            'success': False,  # ← EJECUCIÓN FALLÓ
            'confidence': 0.95,
            'validation': {'verified': True},
            'mode': 'REACTIVE',
            'attempts': 1,
            'scene_state_pre': {'objects': ['Cube']},
            'scene_state': {'objects': ['Cube']}
        }
        
        pattern_id = self.memory.store_pattern("Crea un cubo", result)
        
        self.assertIsNone(pattern_id)
        self.assertEqual(len(self.memory.patterns), 0)
        print("  ✓ Patrón rechazado correctamente (ejecución fallida)")
    
    def test_rejection_hybrid_mode(self):
        """Test: Rechazo cuando mode == HYBRID (Condición 4)"""
        print("\n[TEST] Rechazo - Modo HYBRID")
        
        result = {
            'success': True,
            'confidence': 0.95,
            'validation': {'verified': True},
            'mode': 'HYBRID',  # ← INTERVENCIÓN HUMANA
            'attempts': 1,
            'scene_state_pre': {'objects': ['Cube']}, # Snapshot no vacío
            'scene_state': {'objects': ['Cube']}, # Snapshot no vacío
        }
        
        pattern_id = self.memory.store_pattern("Crea un cubo", result)
        
        self.assertIsNone(pattern_id)
        self.assertEqual(len(self.memory.patterns), 0)
        print("  ✓ Patrón rechazado correctamente (modo HYBRID)")
    
    def test_rejection_multiple_attempts(self):
        """Test: Rechazo cuando attempts > 1 (Condición 5)"""
        print("\n[TEST] Rechazo - Múltiples intentos")
        
        result = {
            'success': True,
            'confidence': 0.95,
            'validation': {'verified': True},
            'mode': 'REACTIVE',
            'attempts': 3, # ← HUBO REINTENTOS
            'scene_state_pre': {'objects': ['Cube']}, # Snapshot no vacío
            'scene_state': {'objects': ['Cube']}, # Snapshot no vacío
        }
        
        pattern_id = self.memory.store_pattern("Crea un cubo", result)
        
        self.assertIsNone(pattern_id)
        self.assertEqual(len(self.memory.patterns), 0)
        print("  ✓ Patrón rechazado correctamente (reintentos detectados)")
    
    def test_can_memorize_method(self):
        """Test: Método can_memorize retorna razón correcta"""
        print("\n[TEST] can_memorize() - Razones de rechazo")
        
        # Test V0 fallo
        result = {
            'success': True, 
            'confidence': 0.95, 
            'validation': {'verified': False}, 
            'attempts': 1,
            'scene_state_pre': {'objects': ['Cube']},
            'scene_state': {'objects': ['Cube']}
        }
        can, reason = self.memory.can_memorize(result)
        self.assertFalse(can)
        self.assertIn("Validación V0", reason)
        print(f"  ✓ V0 fallo: {reason}")
        
        # Test baja confianza
        result = {
            'success': True, 
            'confidence': 0.70, 
            'validation': {'verified': True}, 
            'attempts': 1,
            'scene_state_pre': {'objects': ['Cube']},
            'scene_state': {'objects': ['Cube']}
        }
        can, reason = self.memory.can_memorize(result)
        self.assertFalse(can)
        self.assertIn("Confianza insuficiente", reason)
        print(f"  ✓ Baja confianza: {reason}")
        
        # Test éxito
        result = {
            'success': True, 
            'confidence': 0.95, 
            'validation': {'verified': True}, 
            'mode': 'REACTIVE',
            'attempts': 1,
            'scene_state_pre': {'objects': ['Cube']},
            'scene_state': {'objects': ['Cube']}
        }
        can, reason = self.memory.can_memorize(result)
        self.assertTrue(can)
        self.assertIn("Cumple todas", reason)
        print(f"  ✓ Éxito: {reason}")
    
    def test_find_similar_pattern(self):
        """Test: Búsqueda de patrones similares"""
        print("\n[TEST] Búsqueda de patrones similares")
        
        # Memorizar patrón
        result = {
            'success': True,
            'confidence': 0.95,
            'validation': {'verified': True},
            'mode': 'REACTIVE',
            'attempts': 1,
            'scene_state_pre': {'objects': ['Cube']}, # Snapshot no vacío
            'scene_state': {'objects': ['Cube', 'Sphere']}, # Snapshot no vacío
            'results': [{'effect': 'create', 'result': {'name': 'Cube'}}]
        }
        self.memory.store_pattern("Crea un cubo rojo", result)
        
        # Buscar similar
        pattern = self.memory.find_similar_pattern("Crea un cubo azul")
        
        self.assertIsNotNone(pattern)
        self.assertIn("cubo", pattern['user_request'].lower())
        self.assertEqual(pattern['metadata']['uses'], 1)  # Se incrementó el uso
        print(f"  ✓ Patrón similar encontrado: '{pattern['user_request']}'")
    
    def test_find_similar_no_match(self):
        """Test: No encuentra patrón si similitud es baja"""
        print("\n[TEST] Búsqueda sin coincidencias")
        
        # Memorizar patrón
        result = {
            'success': True,
            'confidence': 0.95,
            'validation': {'verified': True},
            'mode': 'REACTIVE',
            'attempts': 1,
            'scene_state_pre': {'objects': ['Cube']}, # Snapshot no vacío
            'scene_state': {'objects': ['Cube', 'Sphere']}, # Snapshot no vacío
            'results': [{}]
        }
        self.memory.store_pattern("Crea un cubo", result)
        
        # Buscar algo muy diferente
        pattern = self.memory.find_similar_pattern("Elimina la esfera gigante")
        
        self.assertIsNone(pattern)
        print("  ✓ No se encontró patrón (similitud baja)")
    
    def test_persistence(self):
        """Test: Persistencia en disco (JSON)"""
        print("\n[TEST] Persistencia JSON")
        
        # Memorizar patrón
        result = {
            'success': True,
            'confidence': 0.95,
            'validation': {'verified': True},
            'mode': 'REACTIVE',
            'attempts': 1,
            'scene_state_pre': {'objects': ['Cube']}, # Snapshot no vacío
            'scene_state': {'objects': ['Cube', 'Sphere']}, # Snapshot no vacío
            'results': [{}]
        }
        pattern_id = self.memory.store_pattern("Crea un cubo", result)
        
        # Verificar que se guardó en disco
        staging_file = os.path.join(self.temp_dir.name, "patterns_staging.json")
        self.assertTrue(os.path.exists(staging_file))
        
        # Cargar en nueva instancia
        memory2 = PatternMemory(storage_dir=self.temp_dir.name)
        
        self.assertEqual(len(memory2.patterns), 1)
        self.assertEqual(memory2.patterns[0]['pattern_id'], pattern_id)
        print("  ✓ Patrón persistido y cargado correctamente")
    
    def test_get_stats(self):
        """Test: Estadísticas de memoria"""
        print("\n[TEST] Estadísticas de memoria")
        
        # Memoria vacía
        stats = self.memory.get_stats()
        self.assertEqual(stats['total_patterns'], 0)
        self.assertEqual(stats['total_uses'], 0)
        print(f"  ✓ Stats vacío: {stats}")
        
        # Memorizar patrón
        result = {
            'success': True,
            'confidence': 0.95,
            'validation': {'verified': True},
            'mode': 'REACTIVE',
            'attempts': 1,
            'scene_state_pre': {'objects': ['Cube']},
            'scene_state': {'objects': ['Cube']},
            'results': [{}]
        }
        self.memory.store_pattern("Crea un cubo", result)
        
        # Usar patrón
        self.memory.find_similar_pattern("Crea un cubo rojo")
        
        stats = self.memory.get_stats()
        self.assertEqual(stats['total_patterns'], 1)
        self.assertEqual(stats['total_uses'], 1)
        self.assertIsNotNone(stats['most_used'])
        print(f"  ✓ Stats con datos: {stats}")


if __name__ == '__main__':
    print("="*70)
    print("TESTS COMPREHENSIVOS - PATTERN MEMORY (FASE 5.13)")
    print("="*70)
    unittest.main(verbosity=2)
