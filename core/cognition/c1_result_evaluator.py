"""
C1 - Evaluador de Resultados
=============================

Parte del Plan C (Cognición Base) - Fase de Evaluación

Responsabilidades:
1. Analizar escenas generadas vs objetivos
2. Calcular métricas: Geometría, Render, Procedural
3. Generar diagnósticos estructurados (éxito/fallo/mejorable)
4. Proporcionar retroalimentación para aprendizaje

Componentes:
- SceneAnalyzer: Inspecciona escena en Blender
- MetricsCalculator: Calcula métricas relevantes
- DiagnosticGenerator: Genera diagnósticos
- EvaluationResult: Estructura de resultados
"""

import json
import time
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, asdict, field
from enum import Enum
from pathlib import Path


class EvaluationStatus(Enum):
    """Estados posibles de una evaluación"""
    SUCCESS = "success"          # Objetivo alcanzado completamente
    PARTIAL = "partial"          # Objetivo alcanzado parcialmente
    FAILED = "failed"            # Objetivo no alcanzado
    UNKNOWN = "unknown"          # No se pudo evaluar


class MetricType(Enum):
    """Tipos de métricas que se pueden evaluar"""
    GEOMETRY = "geometry"        # Formas, dimensiones, proporciones
    RENDER = "render"            # Texturas, materiales, iluminación
    PROCEDURAL = "procedural"    # Algoritmos, patrones, lógica
    STRUCTURAL = "structural"    # Jerarquía, relaciones, ensamblaje
    TEMPORAL = "temporal"        # Animación, timing, secuencias


@dataclass
class MetricResult:
    """Resultado de una métrica individual"""
    type: MetricType
    name: str
    expected: Any
    actual: Any
    score: float  # 0.0 a 1.0
    details: Dict[str, Any] = field(default_factory=dict)
    passed: bool = False
    
    def __post_init__(self):
        self.passed = self.score >= 0.7  # Umbral de aprobación
    
    def to_dict(self):
        return {
            "type": self.type.value,
            "name": self.name,
            "expected": str(self.expected),
            "actual": str(self.actual),
            "score": round(self.score, 3),
            "passed": self.passed,
            "details": self.details
        }


@dataclass
class Diagnostic:
    """Diagnóstico estructurado de un resultado"""
    status: EvaluationStatus
    summary: str
    score_overall: float  # 0.0 a 1.0
    metrics_passed: int
    metrics_total: int
    recommendations: List[str] = field(default_factory=list)
    issues: List[str] = field(default_factory=list)
    strengths: List[str] = field(default_factory=list)
    
    def to_dict(self):
        return {
            "status": self.status.value,
            "summary": self.summary,
            "score_overall": round(self.score_overall, 3),
            "metrics": f"{self.metrics_passed}/{self.metrics_total}",
            "recommendations": self.recommendations,
            "issues": self.issues,
            "strengths": self.strengths
        }


@dataclass
class EvaluationResult:
    """Resultado completo de una evaluación"""
    objective: str
    timestamp: datetime
    status: EvaluationStatus
    diagnostic: Diagnostic
    metrics: List[MetricResult]
    scene_data: Dict[str, Any] = field(default_factory=dict)
    duration_seconds: float = 0.0
    
    def to_dict(self):
        return {
            "objective": self.objective,
            "timestamp": self.timestamp.isoformat(),
            "status": self.status.value,
            "diagnostic": self.diagnostic.to_dict(),
            "metrics": [m.to_dict() for m in self.metrics],
            "scene_data": self.scene_data,
            "duration_seconds": round(self.duration_seconds, 2)
        }
    
    def to_json(self):
        return json.dumps(self.to_dict(), indent=2, ensure_ascii=False)


class SceneAnalyzer:
    """Analiza escenas de Blender y extrae información relevante"""
    
    def __init__(self):
        self.last_analysis = None
        self.scene_history = []
    
    def analyze_mock_scene(self, objects: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analiza una escena simulada (para testing sin Blender).
        
        Formato esperado de objects:
        {
            "Cube": {
                "type": "MESH",
                "location": [0, 0, 0],
                "rotation": [0, 0, 0],
                "scale": [1, 1, 1],
                "dimensions": [2, 2, 2],
                "material": "Blue"
            }
        }
        """
        analysis = {
            "timestamp": datetime.now().isoformat(),
            "object_count": len(objects),
            "objects": {},
            "total_volume": 0.0,
            "mesh_objects": 0,
            "materials": set()
        }
        
        for obj_name, obj_data in objects.items():
            analysis["objects"][obj_name] = {
                "type": obj_data.get("type", "UNKNOWN"),
                "location": obj_data.get("location", [0, 0, 0]),
                "dimensions": obj_data.get("dimensions", [0, 0, 0]),
                "scale": obj_data.get("scale", [1, 1, 1])
            }
            
            # Calcular volumen aproximado
            if "dimensions" in obj_data:
                dims = obj_data["dimensions"]
                volume = dims[0] * dims[1] * dims[2]
                analysis["total_volume"] += volume
            
            if obj_data.get("type") == "MESH":
                analysis["mesh_objects"] += 1
            
            if "material" in obj_data:
                analysis["materials"].add(obj_data["material"])
        
        analysis["materials"] = list(analysis["materials"])
        self.last_analysis = analysis
        self.scene_history.append(analysis)
        
        return analysis
    
    def analyze_blender_scene(self, adapter) -> Dict[str, Any]:
        """
        Analiza una escena real de Blender usando un adapter.
        (Implementación real cuando se integre con BlenderAdapter)
        """
        try:
            # Aquí iría la integración real con BlenderAdapter
            # Por ahora retornamos estructura
            return {
                "timestamp": datetime.now().isoformat(),
                "adapter_available": adapter is not None,
                "note": "Implementar con BlenderAdapter real"
            }
        except Exception as e:
            return {
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def get_object_count(self, scene_data: Dict[str, Any]) -> int:
        """Obtiene el número de objetos en la escena"""
        return scene_data.get("object_count", 0)
    
    def get_materials(self, scene_data: Dict[str, Any]) -> List[str]:
        """Obtiene lista de materiales en la escena"""
        return scene_data.get("materials", [])
    
    def get_total_volume(self, scene_data: Dict[str, Any]) -> float:
        """Obtiene volumen total aproximado"""
        return scene_data.get("total_volume", 0.0)


class MetricsCalculator:
    """Calcula métricas de evaluación"""
    
    def __init__(self, analyzer: SceneAnalyzer):
        self.analyzer = analyzer
        self.metrics = []
    
    def calculate_geometry_metrics(self, scene_data: Dict[str, Any], 
                                   expected: Dict[str, Any]) -> List[MetricResult]:
        """Calcula métricas geométricas"""
        results = []
        
        # Métrica 1: Número de objetos
        actual_count = self.analyzer.get_object_count(scene_data)
        expected_count = expected.get("object_count", actual_count)
        
        score = 1.0 if actual_count == expected_count else 0.7 if abs(actual_count - expected_count) <= 1 else 0.3
        
        results.append(MetricResult(
            type=MetricType.GEOMETRY,
            name="object_count",
            expected=expected_count,
            actual=actual_count,
            score=score,
            details={
                "difference": abs(actual_count - expected_count),
                "tolerance": 1
            }
        ))
        
        # Métrica 2: Dimensiones totales
        actual_volume = self.analyzer.get_total_volume(scene_data)
        expected_volume = expected.get("estimated_volume", actual_volume)
        
        if expected_volume > 0:
            volume_score = max(0.0, 1.0 - abs(actual_volume - expected_volume) / expected_volume)
        else:
            volume_score = 1.0 if actual_volume == 0 else 0.0
        
        results.append(MetricResult(
            type=MetricType.GEOMETRY,
            name="total_volume",
            expected=round(expected_volume, 2),
            actual=round(actual_volume, 2),
            score=volume_score,
            details={"unit": "cubic_units"}
        ))
        
        return results
    
    def calculate_render_metrics(self, scene_data: Dict[str, Any],
                                expected: Dict[str, Any]) -> List[MetricResult]:
        """Calcula métricas de render (texturas, materiales, etc)"""
        results = []
        
        # Métrica 1: Presencia de materiales
        actual_materials = set(self.analyzer.get_materials(scene_data))
        expected_materials = set(expected.get("materials", []))
        
        if expected_materials:
            materials_found = len(actual_materials & expected_materials)
            score = materials_found / len(expected_materials)
        else:
            score = 1.0 if not actual_materials else 0.8
        
        results.append(MetricResult(
            type=MetricType.RENDER,
            name="materials_match",
            expected=list(expected_materials),
            actual=list(actual_materials),
            score=score,
            details={
                "found": materials_found if expected_materials else 0,
                "expected": len(expected_materials)
            }
        ))
        
        return results
    
    def calculate_procedural_metrics(self, scene_data: Dict[str, Any],
                                    expected: Dict[str, Any]) -> List[MetricResult]:
        """Calcula métricas de procedimientos (lógica, patrones)"""
        results = []
        
        # Métrica 1: Verificación de procedimiento documentado
        procedure = expected.get("procedure", "")
        results.append(MetricResult(
            type=MetricType.PROCEDURAL,
            name="procedure_documented",
            expected=True,
            actual=bool(procedure),
            score=1.0 if procedure else 0.5,
            details={
                "procedure_length": len(procedure),
                "has_steps": "steps" in expected or "commands" in expected
            }
        ))
        
        return results
    
    def calculate_all_metrics(self, scene_data: Dict[str, Any],
                            objective: Dict[str, Any]) -> List[MetricResult]:
        """Calcula todas las métricas relevantes"""
        all_metrics = []
        
        all_metrics.extend(self.calculate_geometry_metrics(scene_data, objective))
        all_metrics.extend(self.calculate_render_metrics(scene_data, objective))
        all_metrics.extend(self.calculate_procedural_metrics(scene_data, objective))
        
        self.metrics = all_metrics
        return all_metrics


class DiagnosticGenerator:
    """Genera diagnósticos estructurados basados en métricas"""
    
    @staticmethod
    def generate_diagnostic(metrics: List[MetricResult], 
                          objective: str) -> Diagnostic:
        """Genera un diagnóstico a partir de métricas"""
        
        if not metrics:
            return Diagnostic(
                status=EvaluationStatus.UNKNOWN,
                summary="No hay métricas para evaluar",
                score_overall=0.0,
                metrics_passed=0,
                metrics_total=0,
                issues=["Sin datos de evaluación"]
            )
        
        # Calcular scores
        passed = sum(1 for m in metrics if m.passed)
        total = len(metrics)
        overall_score = sum(m.score for m in metrics) / total if total > 0 else 0.0
        
        # Determinar estado
        if overall_score >= 0.9:
            status = EvaluationStatus.SUCCESS
            summary = f"[SUCCESS] Objetivo alcanzado exitosamente ({overall_score:.1%})"
        elif overall_score >= 0.7:
            status = EvaluationStatus.PARTIAL
            summary = f"[PARTIAL] Objetivo alcanzado parcialmente ({overall_score:.1%})"
        elif overall_score > 0.3:
            status = EvaluationStatus.FAILED
            summary = f"[FAILED] Objetivo no alcanzado ({overall_score:.1%})"
        else:
            status = EvaluationStatus.FAILED
            summary = f"[FAILED] Evaluacion critica ({overall_score:.1%})"
        
        # Analizar detalles
        issues = []
        strengths = []
        recommendations = []
        
        for metric in metrics:
            if metric.passed:
                strengths.append(f"OK {metric.name}: {metric.score:.1%}")
            else:
                issues.append(f"FAIL {metric.name}: {metric.score:.1%} (esperado: {metric.expected})")
                recommendations.append(f"Revisar {metric.name}: actual={metric.actual} vs esperado={metric.expected}")
        
        return Diagnostic(
            status=status,
            summary=summary,
            score_overall=overall_score,
            metrics_passed=passed,
            metrics_total=total,
            issues=issues,
            strengths=strengths,
            recommendations=recommendations
        )


class C1ResultEvaluator:
    """
    Evaluador Principal (C1)
    
    Orquesta análisis de escena, cálculo de métricas y generación de diagnósticos.
    """
    
    def __init__(self):
        self.analyzer = SceneAnalyzer()
        self.metrics_calculator = MetricsCalculator(self.analyzer)
        self.diagnostic_generator = DiagnosticGenerator()
        self.evaluation_history = []
    
    def evaluate(self, objective: str, scene_data: Dict[str, Any],
                expected_result: Optional[Dict[str, Any]] = None) -> EvaluationResult:
        """
        Evalúa una escena contra un objetivo.
        
        Args:
            objective: Descripción del objetivo (ej: "Crear un cubo azul")
            scene_data: Datos de la escena a evaluar
            expected_result: Datos esperados (si no se pasan, se estiman)
        
        Returns:
            EvaluationResult con diagnóstico completo
        """
        start_time = time.time()
        
        # Si no hay expected_result, crear uno por defecto
        if expected_result is None:
            expected_result = {
                "object_count": scene_data.get("object_count", 1),
                "materials": scene_data.get("materials", []),
                "procedure": objective
            }
        
        # Calcular métricas
        metrics = self.metrics_calculator.calculate_all_metrics(scene_data, expected_result)
        
        # Generar diagnóstico
        diagnostic = self.diagnostic_generator.generate_diagnostic(metrics, objective)
        
        # Crear resultado
        duration = time.time() - start_time
        result = EvaluationResult(
            objective=objective,
            timestamp=datetime.now(),
            status=diagnostic.status,
            diagnostic=diagnostic,
            metrics=metrics,
            scene_data=scene_data,
            duration_seconds=duration
        )
        
        # Guardar en historial
        self.evaluation_history.append(result)
        
        return result
    
    def evaluate_with_feedback(self, objective: str, scene_data: Dict[str, Any],
                              human_feedback: Optional[str] = None) -> EvaluationResult:
        """
        Evalúa incluyendo feedback humano (para ajustar métricas).
        """
        result = self.evaluate(objective, scene_data)
        
        if human_feedback:
            result.diagnostic.recommendations.insert(0, f"Feedback humano: {human_feedback}")
        
        return result
    
    def export_evaluation(self, result: EvaluationResult, filepath: Path) -> bool:
        """Exporta evaluación a JSON"""
        try:
            filepath.parent.mkdir(parents=True, exist_ok=True)
            with open(filepath, 'w') as f:
                f.write(result.to_json())
            return True
        except Exception as e:
            print(f"Error exportando evaluación: {e}")
            return False
    
    def get_history_summary(self) -> Dict[str, Any]:
        """Resumen del historial de evaluaciones"""
        if not self.evaluation_history:
            return {"total": 0}
        
        successes = sum(1 for e in self.evaluation_history if e.status == EvaluationStatus.SUCCESS)
        partials = sum(1 for e in self.evaluation_history if e.status == EvaluationStatus.PARTIAL)
        failures = sum(1 for e in self.evaluation_history if e.status == EvaluationStatus.FAILED)
        avg_score = sum(e.diagnostic.score_overall for e in self.evaluation_history) / len(self.evaluation_history)
        
        return {
            "total": len(self.evaluation_history),
            "successes": successes,
            "partials": partials,
            "failures": failures,
            "average_score": round(avg_score, 3),
            "success_rate": round(successes / len(self.evaluation_history), 3)
        }
