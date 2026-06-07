"""
Demo C4 - Auto-tuning Procedural

5 demostraciones de optimización automática de parámetros:
1. Optimización de parámetro único (hill climbing)
2. Convergencia a óptimo con múltiples iteraciones
3. Comparación de estrategias (hill climbing vs random)
4. Auto-tuning con evaluador C1 personalizado
5. Exportación de resultado a JSON
"""

from core.cognition.c4_auto_tuning_procedural import (
    C4AutoTuningProcedural, ParameterBound, ParameterType, OptimizationStrategy
)


def demo_1_basic_optimization():
    """DEMO 1: Optimización básica con hill climbing"""
    print("\n" + "="*70)
    print("DEMO 1: Optimización Básica de Parámetro")
    print("="*70)
    print("\nObjetivo: Optimizar parámetro 'calidad' (1-10)")
    print("Función: cuanto más cercano a 7, mejor")
    print("")
    
    # Procedimiento simple: calidad es mejor cuanto más cercano a 7
    def quality_procedure(quality_param):
        """Procedimiento que retorna calidad basada en param"""
        distance_to_optimal = abs(quality_param - 7)
        quality_score = 1.0 - (distance_to_optimal / 10.0)
        return {
            "quality_score": quality_score,
            "parameter": quality_param,
            "feedback": f"Calidad: {quality_score:.2f}"
        }
    
    # Bounds
    bounds = {
        "quality": ParameterBound(
            name="quality",
            param_type=ParameterType.INT,
            min_value=1,
            max_value=10,
            step=1
        )
    }
    
    # Optimización
    c4 = C4AutoTuningProcedural()
    result = c4.optimize(
        objective="quality_optimization",
        procedure=quality_procedure,
        param_bounds=bounds,
        strategy=OptimizationStrategy.HILL_CLIMBING,
        max_iterations=15,
        no_improvement_limit=3
    )
    
    # Mostrar resultado
    print(f"Parámetro óptimo encontrado: {result.best_parameter_value}")
    print(f"Score conseguido: {result.best_score:.4f}")
    print(f"Iteraciones totales: {result.total_iterations}")
    print(f"Convergencia: {result.converged} ({result.convergence_reason})")
    print(f"Tiempo: {result.execution_time:.3f}s")
    
    # Mostrar histórico
    print(f"\nHistórico de optimización:")
    for i, step in enumerate(result.history[:5]):  # Primeros 5
        marker = "X" if step.best_so_far else " "
        print(f"  [{marker}] Iter {step.step_number}: param={step.parameter_value}, "
              f"score={step.c1_score:.4f}")
    if len(result.history) > 5:
        print(f"  ... ({len(result.history) - 5} más)")


def demo_2_convergence():
    """DEMO 2: Convergencia a óptimo"""
    print("\n" + "="*70)
    print("DEMO 2: Convergencia a Óptimo Global")
    print("="*70)
    print("\nObjetivo: Encontrar parámetro que minimice error")
    print("Función: f(x) = (x-5)² (parábola, óptimo en x=5)")
    print("")
    
    def parabola_procedure(x):
        """Función parábola: (x-5)² normalizada a 0-1"""
        error = (x - 5) ** 2
        # Normalizar: error máximo es cuando x=0 o x=10 (error=25)
        score = 1.0 - (error / 25.0)
        return {"error": error, "score": score}
    
    bounds = {
        "x": ParameterBound(
            name="x",
            param_type=ParameterType.FLOAT,
            min_value=0.0,
            max_value=10.0,
            step=0.5
        )
    }
    
    c4 = C4AutoTuningProcedural()
    result = c4.optimize(
        objective="parabola_minimization",
        procedure=parabola_procedure,
        param_bounds=bounds,
        strategy=OptimizationStrategy.HILL_CLIMBING,
        target_score=0.99,
        max_iterations=50,
        no_improvement_limit=5
    )
    
    print(f"Parámetro óptimo: {result.best_parameter_value:.2f}")
    print(f"Score conseguido: {result.best_score:.4f}")
    print(f"Óptimo teórico: x=5.00")
    print(f"Error: {abs(result.best_parameter_value - 5.0):.2f}")
    print(f"Iteraciones: {result.total_iterations}")
    print(f"Convergió: {result.converged}")


def demo_3_strategy_comparison():
    """DEMO 3: Comparación de estrategias"""
    print("\n" + "="*70)
    print("DEMO 3: Comparación de Estrategias de Optimización")
    print("="*70)
    print("\nMismo problema, diferentes estrategias:")
    print("")
    
    def comparison_procedure(param):
        """Procedimiento para comparar"""
        distance = abs(param - 6)
        return {"score": 1.0 - (distance / 10.0)}
    
    bounds = {
        "p": ParameterBound(
            name="p",
            param_type=ParameterType.INT,
            min_value=0,
            max_value=10,
            step=1
        )
    }
    
    c4 = C4AutoTuningProcedural()
    
    # Hill Climbing
    result_hc = c4.optimize(
        objective="comparison_hc",
        procedure=comparison_procedure,
        param_bounds=bounds,
        strategy=OptimizationStrategy.HILL_CLIMBING,
        max_iterations=20
    )
    
    # Random Search
    result_rs = c4.optimize(
        objective="comparison_rs",
        procedure=comparison_procedure,
        param_bounds=bounds,
        strategy=OptimizationStrategy.RANDOM_SEARCH,
        max_iterations=20
    )
    
    print("HILL CLIMBING:")
    print(f"  Óptimo: {result_hc.best_parameter_value}, Score: {result_hc.best_score:.4f}")
    print(f"  Iteraciones: {result_hc.total_iterations}")
    
    print("\nRANDOM SEARCH:")
    print(f"  Óptimo: {result_rs.best_parameter_value}, Score: {result_rs.best_score:.4f}")
    print(f"  Iteraciones: {result_rs.total_iterations}")
    
    print("\nConclusion:")
    if result_hc.best_score > result_rs.best_score:
        print(f"  Hill Climbing fue mejor (diff: {result_hc.best_score - result_rs.best_score:.4f})")
    else:
        print(f"  Random Search fue mejor (diff: {result_rs.best_score - result_hc.best_score:.4f})")


def demo_4_with_c1_evaluator():
    """DEMO 4: Auto-tuning con evaluador C1"""
    print("\n" + "="*70)
    print("DEMO 4: Auto-tuning con Evaluador C1 Personalizado")
    print("="*70)
    print("\nScenario: Optimizar 'render_quality' (1-5)")
    print("C1 evalúa: render_quality/5 + success_bonus")
    print("")
    
    def render_procedure(render_quality):
        """Simula procedimiento de render"""
        # Calidad base
        base_quality = render_quality / 5.0
        # Agregar bonus si calidad es alta
        success_bonus = 0.2 if render_quality >= 3 else 0.0
        return {
            "success": render_quality >= 2,
            "quality": base_quality,
            "bonus": success_bonus
        }
    
    def c1_render_evaluator(exec_result):
        """Evaluador C1 para render"""
        if not exec_result["success"]:
            return 0.0
        score = exec_result["quality"] + exec_result["bonus"]
        return min(1.0, score)
    
    bounds = {
        "render_quality": ParameterBound(
            name="render_quality",
            param_type=ParameterType.INT,
            min_value=1,
            max_value=5,
            step=1
        )
    }
    
    c4 = C4AutoTuningProcedural()
    
    # Con C2 memory
    c2_memory = {}
    
    result = c4.optimize(
        objective="render_optimization",
        procedure=render_procedure,
        param_bounds=bounds,
        c1_evaluator=c1_render_evaluator,
        c2_memory=c2_memory,
        strategy=OptimizationStrategy.HILL_CLIMBING,
        max_iterations=15
    )
    
    print(f"Render quality óptima: {result.best_parameter_value}")
    print(f"Score conseguido: {result.best_score:.4f}")
    print(f"Iteraciones: {result.total_iterations}")
    
    # Mostrar lo guardado en C2
    if "render_optimization" in c2_memory:
        print(f"\nHeurísticas guardadas en C2: {len(c2_memory['render_optimization'])} registros")
        print("Últimas 3 heurísticas:")
        for h in c2_memory["render_optimization"][-3:]:
            print(f"  - param={h['param_value']}, score={h['score']:.4f}")


def demo_5_export_plan():
    """DEMO 5: Exportación de resultado"""
    print("\n" + "="*70)
    print("DEMO 5: Exportación de Resultado a JSON")
    print("="*70)
    print("\nOptimizando y exportando resultado...")
    print("")
    
    def simple_opt(p):
        return {"score": max(0.0, 1.0 - abs(p - 5) / 10)}
    
    bounds = {
        "param": ParameterBound(
            name="param",
            param_type=ParameterType.INT,
            min_value=1,
            max_value=10,
            step=1
        )
    }
    
    c4 = C4AutoTuningProcedural()
    result = c4.optimize(
        objective="export_demo",
        procedure=simple_opt,
        param_bounds=bounds,
        max_iterations=10
    )
    
    # Exportar
    export_path = "bitacora/optimization_result.json"
    success = c4.export_result(result, export_path)
    
    if success:
        print(f"[OK] Resultado exportado a: {export_path}")
        print(f"\nContenido del archivo JSON (resumen):")
        
        import json
        with open(export_path, 'r') as f:
            data = json.load(f)
            print(f"  - Objetivo: {data['objective']}")
            print(f"  - Parámetro óptimo: {data['best_parameter_value']}")
            print(f"  - Score: {data['best_score']:.4f}")
            print(f"  - Iteraciones: {data['total_iterations']}")
            print(f"  - Convergió: {data['converged']}")
            print(f"  - Razón: {data['convergence_reason']}")
            print(f"  - Tiempo: {data['execution_time']:.3f}s")
    else:
        print("[ERROR] Error al exportar resultado")


def demo_6_multi_parameter():
    """DEMO 6: Concepto de múltiples parámetros"""
    print("\n" + "="*70)
    print("DEMO 6: Arquitectura para Múltiples Parámetros (Concepto)")
    print("="*70)
    print("\nNota: C4 actual optimiza UN parámetro por iteración.")
    print("Arquitectura extensible para múltiples parámetros.")
    print("")
    
    print("Casos de uso futuros:")
    print("  1. Grid search: busca en cuadrícula de parámetros")
    print("  2. Bayesian optimization: busca inteligente")
    print("  3. Genetic algorithms: evolución de parámetros")
    print("")
    
    print("Ejemplo hipotético: renderizado con 3 parámetros")
    print("  - quality: 1-10 (actual implementado)")
    print("  - resolution: 1-4 (extensión futura)")
    print("  - samples: 1-16 (extensión futura)")
    print("")
    
    print("Flujo propuesto:")
    print("  1. Optimizar quality manteniendo resolution=2, samples=8")
    print("  2. Optimizar resolution manteniendo quality_óptima, samples=8")
    print("  3. Optimizar samples manteniendo quality_óptima, resolution_óptima")
    print("  4. Refinamiento simultáneo (genetic algorithm)")


if __name__ == "__main__":
    print("\n" + "="*70)
    print("C4 - AUTO-TUNING PROCEDURAL - DEMOSTRACIONES")
    print("="*70)
    
    # Ejecutar demostraciones
    demo_1_basic_optimization()
    demo_2_convergence()
    demo_3_strategy_comparison()
    demo_4_with_c1_evaluator()
    demo_5_export_plan()
    demo_6_multi_parameter()
    
    print("\n" + "="*70)
    print("TODAS LAS DEMOSTRACIONES COMPLETADAS")
    print("="*70)
    print("\nResumen:")
    print("  [OK] Demo 1: Optimizacion basica")
    print("  [OK] Demo 2: Convergencia a optimo")
    print("  [OK] Demo 3: Comparacion de estrategias")
    print("  [OK] Demo 4: Con evaluador C1")
    print("  [OK] Demo 5: Exportacion a JSON")
    print("  [OK] Demo 6: Concepto de multiples parametros")
    print("="*70 + "\n")
