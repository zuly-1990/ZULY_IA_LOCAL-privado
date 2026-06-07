"""
Tests unitarios para C4 - Auto-tuning Procedural

22 tests cubriendo:
- ParameterOptimizer (5 tests)
- IterativeExecutor (3 tests)
- FeedbackLoop (4 tests)
- ConvergenceChecker (3 tests)
- C4AutoTuningProcedural (7 tests)
"""

import unittest
from datetime import datetime

from core.cognition.c4_auto_tuning_procedural import (
    ParameterOptimizer, IterativeExecutor, FeedbackLoop, ConvergenceChecker,
    C4AutoTuningProcedural, ParameterBound, ParameterType, OptimizationStrategy,
    OptimizationStep, OptimizationResult
)


class TestParameterOptimizer(unittest.TestCase):
    """Tests para ParameterOptimizer"""
    
    def setUp(self):
        """Configuración inicial"""
        self.bounds = {
            "quality": ParameterBound(
                name="quality",
                param_type=ParameterType.INT,
                min_value=1,
                max_value=10,
                step=1
            ),
            "speed": ParameterBound(
                name="speed",
                param_type=ParameterType.FLOAT,
                min_value=0.1,
                max_value=1.0,
                step=0.1
            )
        }
        self.optimizer = ParameterOptimizer(self.bounds)
    
    def test_validate_bounds(self):
        """Valida que bounds se validen correctamente"""
        # Debe no lanzar excepción
        optimizer = ParameterOptimizer(self.bounds)
        self.assertIsNotNone(optimizer)
    
    def test_invalid_bounds_raise_error(self):
        """Bounds inválidos deben lanzar error"""
        invalid_bounds = {
            "bad": ParameterBound(
                name="bad",
                param_type=ParameterType.INT
                # Falta min_value y max_value
            )
        }
        with self.assertRaises(ValueError):
            ParameterOptimizer(invalid_bounds)
    
    def test_generate_initial_value_int(self):
        """Genera valor inicial para INT"""
        value = self.optimizer.generate_initial_value("quality")
        self.assertIsInstance(value, int)
        self.assertGreaterEqual(value, 1)
        self.assertLessEqual(value, 10)
    
    def test_generate_initial_value_float(self):
        """Genera valor inicial para FLOAT"""
        value = self.optimizer.generate_initial_value("speed")
        self.assertIsInstance(value, float)
        self.assertGreaterEqual(value, 0.1)
        self.assertLessEqual(value, 1.0)
    
    def test_get_neighbors_int(self):
        """Obtiene vecinos para INT"""
        neighbors = self.optimizer.get_neighbors("quality", 5)
        self.assertIn(4, neighbors)
        self.assertIn(6, neighbors)
        self.assertEqual(len(neighbors), 2)
    
    def test_is_valid_within_bounds(self):
        """Valida que valor esté dentro de bounds"""
        self.assertTrue(self.optimizer.is_valid("quality", 5))
        self.assertFalse(self.optimizer.is_valid("quality", 15))
        self.assertFalse(self.optimizer.is_valid("quality", -1))


class TestIterativeExecutor(unittest.TestCase):
    """Tests para IterativeExecutor"""
    
    def setUp(self):
        """Configuración inicial"""
        self.call_count = 0
        
        def simple_procedure(param_value):
            """Procedimiento simple que retorna param * 2"""
            return {"result": param_value * 2, "input": param_value}
        
        self.procedure = simple_procedure
        self.executor = IterativeExecutor(self.procedure, max_iterations=10)
    
    def test_execute_successful(self):
        """Ejecución exitosa retorna success=True"""
        result = self.executor.execute_with_parameter(5)
        self.assertTrue(result["success"])
        self.assertEqual(result["result"]["result"], 10)
    
    def test_execute_captures_param(self):
        """Captura el parámetro usado"""
        result = self.executor.execute_with_parameter(42)
        self.assertEqual(result["param_used"], 42)
    
    def test_execute_failed_procedure(self):
        """Procedimiento fallido retorna success=False"""
        def failing_procedure(param):
            raise ValueError("Error simulado")
        
        executor = IterativeExecutor(failing_procedure)
        result = executor.execute_with_parameter(5)
        self.assertFalse(result["success"])
        self.assertIn("error", result)


class TestFeedbackLoop(unittest.TestCase):
    """Tests para FeedbackLoop"""
    
    def setUp(self):
        """Configuración inicial"""
        self.feedback = FeedbackLoop()
    
    def test_evaluate_successful_execution(self):
        """Evalúa ejecución exitosa"""
        exec_result = {
            "success": True,
            "result": {"value": 10}
        }
        score = self.feedback.evaluate_execution(exec_result)
        self.assertEqual(score, 0.8)
    
    def test_evaluate_failed_execution(self):
        """Evalúa ejecución fallida"""
        exec_result = {
            "success": False,
            "error": "Error simulado"
        }
        score = self.feedback.evaluate_execution(exec_result)
        self.assertEqual(score, 0.0)
    
    def test_evaluate_with_custom_evaluator(self):
        """Usa evaluador C1 personalizado"""
        def custom_evaluator(exec_result):
            return 0.95  # Siempre retorna 0.95
        
        feedback = FeedbackLoop(evaluator_c1=custom_evaluator)
        exec_result = {"success": True}
        score = feedback.evaluate_execution(exec_result)
        self.assertEqual(score, 0.95)
    
    def test_save_heuristic(self):
        """Guarda heurística en C2"""
        c2_memory = {}
        feedback = FeedbackLoop(memory_c2=c2_memory)
        
        feedback.save_heuristic("crear_cubo", param_value=0.8, score=0.95)
        
        self.assertIn("crear_cubo", c2_memory)
        self.assertEqual(len(c2_memory["crear_cubo"]), 1)
        self.assertEqual(c2_memory["crear_cubo"][0]["param_value"], 0.8)


class TestConvergenceChecker(unittest.TestCase):
    """Tests para ConvergenceChecker"""
    
    def setUp(self):
        """Configuración inicial"""
        self.checker = ConvergenceChecker(
            target_score=0.9,
            max_iterations=50,
            no_improvement_limit=5
        )
    
    def test_target_reached(self):
        """Detiene si se alcanza score objetivo"""
        should_continue, reason = self.checker.should_continue(
            iteration=10,
            best_score=0.95,  # >= target_score
            no_improvement_count=0
        )
        self.assertFalse(should_continue)
        self.assertEqual(reason, "target_reached")
    
    def test_max_iterations_reached(self):
        """Detiene si se alcanza máximo de iteraciones"""
        should_continue, reason = self.checker.should_continue(
            iteration=50,  # >= max_iterations
            best_score=0.5,
            no_improvement_count=0
        )
        self.assertFalse(should_continue)
        self.assertEqual(reason, "max_iterations")
    
    def test_no_improvement_limit_reached(self):
        """Detiene si no hay mejora después de límite"""
        should_continue, reason = self.checker.should_continue(
            iteration=20,
            best_score=0.5,
            no_improvement_count=5  # >= no_improvement_limit
        )
        self.assertFalse(should_continue)
        self.assertEqual(reason, "no_improvement")
    
    def test_should_continue(self):
        """Continúa si no se cumple ninguna condición"""
        should_continue, reason = self.checker.should_continue(
            iteration=10,
            best_score=0.5,
            no_improvement_count=2
        )
        self.assertTrue(should_continue)
        self.assertEqual(reason, "continue")


class TestC4AutoTuningProcedural(unittest.TestCase):
    """Tests para C4AutoTuningProcedural"""
    
    def setUp(self):
        """Configuración inicial"""
        self.c4 = C4AutoTuningProcedural()
        
        # Procedimiento simple: cuanto más cercano a 5, mejor
        def simple_procedure(param_value):
            distance = abs(param_value - 5)
            quality_score = 1.0 - (distance / 10.0)  # Normalizado 0-1
            return {"quality": quality_score, "param": param_value}
        
        self.procedure = simple_procedure
        
        # Bounds simples
        self.bounds = {
            "param": ParameterBound(
                name="param",
                param_type=ParameterType.INT,
                min_value=1,
                max_value=10,
                step=1
            )
        }
    
    def test_optimize_hill_climbing(self):
        """Ejecuta optimización con hill climbing"""
        result = self.c4.optimize(
            objective="test_optimization",
            procedure=self.procedure,
            param_bounds=self.bounds,
            strategy=OptimizationStrategy.HILL_CLIMBING,
            max_iterations=20,
            no_improvement_limit=3
        )
        
        self.assertIsNotNone(result)
        self.assertEqual(result.objective, "test_optimization")
        self.assertGreater(result.best_score, 0.5)
        self.assertGreater(result.total_iterations, 0)
    
    def test_optimize_converges_to_optimum(self):
        """Converge hacia el óptimo"""
        result = self.c4.optimize(
            objective="converge_test",
            procedure=self.procedure,
            param_bounds=self.bounds,
            strategy=OptimizationStrategy.HILL_CLIMBING,
            target_score=0.9,
            max_iterations=30
        )
        
        # Debería encontrar valor cercano a 5
        self.assertIn(result.best_parameter_value, [4, 5, 6])
    
    def test_optimization_saved_to_history(self):
        """Guarda resultado en historial"""
        self.c4.optimize(
            objective="history_test",
            procedure=self.procedure,
            param_bounds=self.bounds,
            max_iterations=10
        )
        
        self.assertIn("history_test", self.c4.optimization_history)
    
    def test_export_result(self):
        """Exporta resultado a JSON"""
        result = self.c4.optimize(
            objective="export_test",
            procedure=self.procedure,
            param_bounds=self.bounds,
            max_iterations=5
        )
        
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_file = f.name
        
        success = self.c4.export_result(result, temp_file)
        self.assertTrue(success)
        
        # Verificar que archivo existe y contiene JSON válido
        import json
        with open(temp_file, 'r') as f:
            data = json.load(f)
            self.assertEqual(data["objective"], "export_test")
        
        # Limpiar
        import os
        os.unlink(temp_file)
    
    def test_get_summary(self):
        """Genera resumen de resultado"""
        result = self.c4.optimize(
            objective="summary_test",
            procedure=self.procedure,
            param_bounds=self.bounds,
            max_iterations=10
        )
        
        summary = self.c4.get_summary(result)
        
        self.assertIn("objective", summary)
        self.assertIn("best_parameter", summary)
        self.assertIn("best_score", summary)
        self.assertIn("iterations", summary)
        self.assertIn("converged", summary)


class TestOptimizationDataclasses(unittest.TestCase):
    """Tests para dataclasses de optimización"""
    
    def test_optimization_step_to_dict(self):
        """OptimizationStep se serializa a dict"""
        step = OptimizationStep(
            step_number=1,
            parameter_value=5,
            c1_score=0.8,
            is_improvement=True
        )
        
        step_dict = step.to_dict()
        self.assertEqual(step_dict["step_number"], 1)
        self.assertEqual(step_dict["c1_score"], 0.8)
        self.assertTrue(step_dict["is_improvement"])
    
    def test_optimization_result_to_dict(self):
        """OptimizationResult se serializa a dict"""
        result = OptimizationResult(
            objective="test",
            best_parameter_value=5,
            best_score=0.9,
            total_iterations=10,
            converged=True,
            convergence_reason="target_reached"
        )
        
        result_dict = result.to_dict()
        self.assertEqual(result_dict["objective"], "test")
        self.assertEqual(result_dict["best_score"], 0.9)
        self.assertTrue(result_dict["converged"])


if __name__ == "__main__":
    unittest.main()
