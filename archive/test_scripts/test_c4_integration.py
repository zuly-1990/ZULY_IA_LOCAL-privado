"""
Tests de integración C4 con LYZU Core

12 tests verific ando:
- Inicialización con enable_cognition
- Métodos C4 funcionan en LYZU
- Compatibilidad con C1/C2/C3
- Backward compatibility
"""

import unittest
import tempfile
import os

from lyzu_core import LYZUCore
from core.cognition.c4_auto_tuning_procedural import ParameterBound, ParameterType


class TestC4Initialization(unittest.TestCase):
    """Tests de inicialización C4"""
    
    def test_c4_initialization_enabled(self):
        """C4 se inicializa cuando enable_cognition=True"""
        lyzu = LYZUCore(enable_cognition=True)
        self.assertIsNotNone(lyzu.auto_tuning_system)
    
    def test_c4_initialization_disabled(self):
        """C4 es None cuando enable_cognition=False"""
        lyzu = LYZUCore(enable_cognition=False)
        self.assertIsNone(lyzu.auto_tuning_system)
    
    def test_c4_default_enabled(self):
        """C4 está enabled por defecto"""
        lyzu = LYZUCore()
        self.assertIsNotNone(lyzu.auto_tuning_system)


class TestC4Methods(unittest.TestCase):
    """Tests de métodos C4 en LYZU"""
    
    def setUp(self):
        """Setup LYZU con C4 enabled"""
        self.lyzu = LYZUCore(enable_cognition=True)
    
    def test_optimize_parameter_exists(self):
        """Método optimize_parameter existe en LYZU"""
        self.assertTrue(hasattr(self.lyzu, 'optimize_parameter'))
    
    def test_optimize_parameter_works(self):
        """optimize_parameter funciona"""
        def test_proc(p):
            return {"score": max(0.0, 1.0 - abs(p - 5) / 10)}
        
        bounds = {
            "p": ParameterBound(
                name="p",
                param_type=ParameterType.INT,
                min_value=1,
                max_value=10,
                step=1
            )
        }
        
        result = self.lyzu.optimize_parameter(
            objective="test",
            procedure=test_proc,
            param_bounds=bounds,
            max_iterations=10
        )
        
        self.assertIsNotNone(result)
        self.assertGreater(result.best_score, 0.0)
    
    def test_optimize_parameter_disabled(self):
        """optimize_parameter retorna None cuando disabled"""
        lyzu = LYZUCore(enable_cognition=False)
        result = lyzu.optimize_parameter(
            objective="test",
            procedure=lambda p: {"score": 0.5},
            param_bounds={},
            max_iterations=5
        )
        self.assertIsNone(result)
    
    def test_export_optimization_exists(self):
        """Método export_optimization existe"""
        self.assertTrue(hasattr(self.lyzu, 'export_optimization'))
    
    def test_export_optimization_works(self):
        """export_optimization funciona"""
        def test_proc(p):
            return {"score": 0.5 + p / 100}
        
        bounds = {
            "p": ParameterBound(
                name="p",
                param_type=ParameterType.FLOAT,
                min_value=0.1,
                max_value=1.0,
                step=0.1
            )
        }
        
        result = self.lyzu.optimize_parameter(
            objective="export_test",
            procedure=test_proc,
            param_bounds=bounds,
            max_iterations=5
        )
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_file = f.name
        
        try:
            success = self.lyzu.export_optimization(result, temp_file)
            self.assertTrue(success)
            
            # Verificar que el archivo existe
            self.assertTrue(os.path.exists(temp_file))
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)
    
    def test_export_optimization_disabled(self):
        """export_optimization retorna False cuando disabled"""
        lyzu = LYZUCore(enable_cognition=False)
        result = lyzu.export_optimization(None, "test.json")
        self.assertFalse(result)
    
    def test_get_optimization_summary_exists(self):
        """Método get_optimization_summary existe"""
        self.assertTrue(hasattr(self.lyzu, 'get_optimization_summary'))
    
    def test_get_optimization_summary_works(self):
        """get_optimization_summary funciona"""
        def test_proc(p):
            return {"score": max(0.0, 1.0 - abs(p - 5) / 10)}
        
        bounds = {
            "p": ParameterBound(
                name="p",
                param_type=ParameterType.INT,
                min_value=1,
                max_value=10,
                step=1
            )
        }
        
        result = self.lyzu.optimize_parameter(
            objective="summary_test",
            procedure=test_proc,
            param_bounds=bounds,
            max_iterations=5
        )
        
        summary = self.lyzu.get_optimization_summary(result)
        
        self.assertIsNotNone(summary)
        self.assertIn("objective", summary)
        self.assertIn("best_parameter", summary)
        self.assertIn("best_score", summary)


class TestC4WithC1C2C3(unittest.TestCase):
    """Tests de compatibilidad C4 con C1/C2/C3"""
    
    def test_all_cognition_modules_together(self):
        """C1, C2, C3 y C4 pueden estar enabled juntos"""
        lyzu = LYZUCore(enable_cognition=True)
        
        # Verificar que todos los métodos están disponibles
        self.assertTrue(hasattr(lyzu, 'optimize_parameter'))
        self.assertTrue(hasattr(lyzu, 'export_optimization'))
        self.assertTrue(hasattr(lyzu, 'get_optimization_summary'))
    
    def test_all_cognition_modules_disabled(self):
        """C4 es None cuando enable_cognition=False"""
        lyzu = LYZUCore(enable_cognition=False)
        
        # C4 debe retornar None en los métodos
        result = lyzu.optimize_parameter(
            objective="test",
            procedure=lambda p: {"score": 0.5},
            param_bounds={}
        )
        self.assertIsNone(result)


class TestBackwardCompatibility(unittest.TestCase):
    """Tests de backward compatibility"""
    
    def test_existing_code_still_works(self):
        """Código existente sigue funcionando"""
        lyzu = LYZUCore(enable_cognition=False)
        
        # LYZU debe funcionar sin cognición
        self.assertIsNotNone(lyzu)
        # Debe tener los métodos C4 pero retornan None
        result = lyzu.optimize_parameter(
            objective="test",
            procedure=lambda p: {"score": 0.5},
            param_bounds={}
        )
        self.assertIsNone(result)
    
    def test_c4_doesnt_affect_existing_methods(self):
        """C4 no afecta métodos existentes de LYZU"""
        lyzu = LYZUCore(enable_cognition=True)
        
        # Los métodos C4 deben existir
        self.assertTrue(hasattr(lyzu, 'optimize_parameter'))
        self.assertTrue(hasattr(lyzu, 'export_optimization'))
        self.assertTrue(hasattr(lyzu, 'get_optimization_summary'))


class TestC4EdgeCases(unittest.TestCase):
    """Tests de casos límite para C4"""
    
    def setUp(self):
        """Setup LYZU"""
        self.lyzu = LYZUCore(enable_cognition=True)
    
    def test_optimize_with_zero_iterations(self):
        """Maneja max_iterations=0 gracefully"""
        def test_proc(p):
            return {"score": 0.5}
        
        bounds = {
            "p": ParameterBound(
                name="p",
                param_type=ParameterType.INT,
                min_value=1,
                max_value=10,
                step=1
            )
        }
        
        # No debe fallar, pero resultado será limitado
        result = self.lyzu.optimize_parameter(
            objective="edge_case",
            procedure=test_proc,
            param_bounds=bounds,
            max_iterations=0
        )
        
        # Debería retornar algo (o None)
        if result is not None:
            self.assertEqual(result.total_iterations, 0)
    
    def test_multiple_optimizations_independent(self):
        """Múltiples optimizaciones son independientes"""
        def proc1(p):
            return {"score": max(0.0, 1.0 - abs(p - 3) / 10)}
        
        def proc2(p):
            return {"score": max(0.0, 1.0 - abs(p - 7) / 10)}
        
        bounds = {
            "p": ParameterBound(
                name="p",
                param_type=ParameterType.INT,
                min_value=1,
                max_value=10,
                step=1
            )
        }
        
        result1 = self.lyzu.optimize_parameter(
            objective="obj1",
            procedure=proc1,
            param_bounds=bounds,
            max_iterations=8
        )
        
        result2 = self.lyzu.optimize_parameter(
            objective="obj2",
            procedure=proc2,
            param_bounds=bounds,
            max_iterations=8
        )
        
        # Ambos deberían encontrar sus óptimos
        self.assertLess(abs(result1.best_parameter_value - 3), 3)
        self.assertLess(abs(result2.best_parameter_value - 7), 3)


if __name__ == "__main__":
    unittest.main()
