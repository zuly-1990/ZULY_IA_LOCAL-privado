"""
Tests para C1 - Evaluador de Resultados
"""

import pytest
from pathlib import Path
from datetime import datetime
from core.cognition.c1_result_evaluator import (
    C1ResultEvaluator, SceneAnalyzer, MetricsCalculator, DiagnosticGenerator,
    EvaluationStatus, MetricType
)


class TestSceneAnalyzer:
    """Tests para SceneAnalyzer"""
    
    def test_analyze_mock_scene_basic(self):
        analyzer = SceneAnalyzer()
        scene = {
            "Cube": {
                "type": "MESH",
                "location": [0, 0, 0],
                "dimensions": [2, 2, 2],
                "scale": [1, 1, 1],
                "material": "Blue"
            }
        }
        
        result = analyzer.analyze_mock_scene(scene)
        
        assert result["object_count"] == 1
        assert result["mesh_objects"] == 1
        assert "Blue" in result["materials"]
        assert result["total_volume"] == 8.0  # 2*2*2
    
    def test_analyze_mock_scene_multiple_objects(self):
        analyzer = SceneAnalyzer()
        scene = {
            "Cube": {
                "type": "MESH",
                "dimensions": [2, 2, 2],
                "material": "Red"
            },
            "Sphere": {
                "type": "MESH",
                "dimensions": [3, 3, 3],
                "material": "Blue"
            }
        }
        
        result = analyzer.analyze_mock_scene(scene)
        
        assert result["object_count"] == 2
        assert result["mesh_objects"] == 2
        assert len(result["materials"]) == 2
        assert result["total_volume"] == pytest.approx(8.0 + 27.0)  # 2³ + 3³
    
    def test_get_object_count(self):
        analyzer = SceneAnalyzer()
        assert analyzer.get_object_count({"object_count": 5}) == 5
    
    def test_get_materials(self):
        analyzer = SceneAnalyzer()
        materials = analyzer.get_materials({"materials": ["Red", "Blue"]})
        assert "Red" in materials
        assert "Blue" in materials


class TestMetricsCalculator:
    """Tests para MetricsCalculator"""
    
    def test_geometry_metrics_perfect_match(self):
        analyzer = SceneAnalyzer()
        calculator = MetricsCalculator(analyzer)
        
        scene_data = {
            "object_count": 3,
            "total_volume": 12.0,
            "materials": []
        }
        expected = {
            "object_count": 3,
            "estimated_volume": 12.0
        }
        
        metrics = calculator.calculate_geometry_metrics(scene_data, expected)
        
        assert len(metrics) == 2
        assert metrics[0].score == 1.0  # Cuenta perfecta
        assert metrics[0].passed
    
    def test_geometry_metrics_partial_match(self):
        analyzer = SceneAnalyzer()
        calculator = MetricsCalculator(analyzer)
        
        scene_data = {
            "object_count": 2,
            "total_volume": 10.0,
            "materials": []
        }
        expected = {
            "object_count": 3,
            "estimated_volume": 12.0
        }
        
        metrics = calculator.calculate_geometry_metrics(scene_data, expected)
        
        assert metrics[0].score < 1.0  # No coincide perfectamente
        assert not metrics[0].passed or metrics[0].score >= 0.7
    
    def test_render_metrics_with_materials(self):
        analyzer = SceneAnalyzer()
        calculator = MetricsCalculator(analyzer)
        
        scene_data = {
            "materials": ["Red", "Blue", "Green"]
        }
        expected = {
            "materials": ["Red", "Blue"]
        }
        
        metrics = calculator.calculate_render_metrics(scene_data, expected)
        
        assert len(metrics) == 1
        assert metrics[0].type == MetricType.RENDER
        assert metrics[0].score > 0.5  # Algunos materiales coinciden
    
    def test_calculate_all_metrics(self):
        analyzer = SceneAnalyzer()
        calculator = MetricsCalculator(analyzer)
        
        scene_data = {
            "object_count": 1,
            "total_volume": 8.0,
            "materials": ["Blue"]
        }
        objective = {
            "object_count": 1,
            "estimated_volume": 8.0,
            "materials": ["Blue"],
            "procedure": "Crear cubo"
        }
        
        metrics = calculator.calculate_all_metrics(scene_data, objective)
        
        assert len(metrics) >= 3  # Al menos geometría, render, procedural
        assert all(m.score >= 0.0 and m.score <= 1.0 for m in metrics)


class TestDiagnosticGenerator:
    """Tests para DiagnosticGenerator"""
    
    def test_generate_diagnostic_all_pass(self):
        analyzer = SceneAnalyzer()
        calculator = MetricsCalculator(analyzer)
        
        scene_data = {
            "object_count": 1,
            "total_volume": 8.0,
            "materials": ["Blue"]
        }
        objective = {
            "object_count": 1,
            "estimated_volume": 8.0,
            "materials": ["Blue"],
            "procedure": "Crear cubo azul"
        }
        
        metrics = calculator.calculate_all_metrics(scene_data, objective)
        diagnostic = DiagnosticGenerator.generate_diagnostic(metrics, "Crear cubo azul")
        
        assert diagnostic.status in [EvaluationStatus.SUCCESS, EvaluationStatus.PARTIAL]
        assert diagnostic.score_overall >= 0.7
        assert diagnostic.metrics_passed > 0
    
    def test_generate_diagnostic_all_fail(self):
        from core.cognition.c1_result_evaluator import MetricResult
        
        # Crear métricas que fallen
        metrics = [
            MetricResult(
                type=MetricType.GEOMETRY,
                name="count",
                expected=5,
                actual=1,
                score=0.2
            ),
            MetricResult(
                type=MetricType.GEOMETRY,
                name="volume",
                expected=50.0,
                actual=2.0,
                score=0.1
            )
        ]
        
        diagnostic = DiagnosticGenerator.generate_diagnostic(metrics, "Objetivo")
        
        assert diagnostic.status == EvaluationStatus.FAILED
        assert diagnostic.metrics_passed == 0
        assert len(diagnostic.issues) > 0


class TestC1ResultEvaluator:
    """Tests para C1ResultEvaluator (orquestador principal)"""
    
    def test_evaluate_basic(self):
        evaluator = C1ResultEvaluator()
        
        scene_data = {
            "object_count": 1,
            "total_volume": 8.0,
            "materials": ["Blue"]
        }
        
        result = evaluator.evaluate("Crear cubo azul", scene_data)
        
        assert result.objective == "Crear cubo azul"
        assert result.status in [EvaluationStatus.SUCCESS, EvaluationStatus.PARTIAL, EvaluationStatus.FAILED]
        assert result.diagnostic.score_overall >= 0.0
        assert len(result.metrics) > 0
        assert result.duration_seconds > 0.0
    
    def test_evaluate_stores_in_history(self):
        evaluator = C1ResultEvaluator()
        
        evaluator.evaluate("Objetivo 1", {"object_count": 1})
        evaluator.evaluate("Objetivo 2", {"object_count": 2})
        
        assert len(evaluator.evaluation_history) == 2
    
    def test_export_evaluation(self, tmp_path):
        evaluator = C1ResultEvaluator()
        
        result = evaluator.evaluate("Test", {"object_count": 1})
        filepath = tmp_path / "evaluation.json"
        
        success = evaluator.export_evaluation(result, filepath)
        
        assert success
        assert filepath.exists()
        
        # Verificar contenido JSON válido
        import json
        with open(filepath) as f:
            data = json.load(f)
            assert data["objective"] == "Test"
            assert "status" in data
    
    def test_get_history_summary(self):
        evaluator = C1ResultEvaluator()
        
        # Crear varias evaluaciones
        for i in range(3):
            evaluator.evaluate(f"Objetivo {i}", {"object_count": i + 1})
        
        summary = evaluator.get_history_summary()
        
        assert summary["total"] == 3
        assert "average_score" in summary
        assert "success_rate" in summary
        assert 0 <= summary["success_rate"] <= 1
    
    def test_evaluate_with_feedback(self):
        evaluator = C1ResultEvaluator()
        
        result = evaluator.evaluate_with_feedback(
            "Crear cubo",
            {"object_count": 1},
            human_feedback="Se vería mejor con más detalles"
        )
        
        assert any("Feedback humano" in rec for rec in result.diagnostic.recommendations)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
