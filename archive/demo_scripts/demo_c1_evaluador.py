#!/usr/bin/env python3
"""
Demo C1 - Evaluador de Resultados

Este script demuestra cómo funciona C1 con ejemplos prácticos.
Ejecutar: python demo_c1_evaluator.py
"""

import json
import sys
from pathlib import Path
from core.cognition.c1_result_evaluator import C1ResultEvaluator, EvaluationStatus

# Configurar encoding para Windows
if sys.platform == 'win32':
    import os
    os.environ['PYTHONIOENCODING'] = 'utf-8'


def print_section(title):
    """Imprime un título de sección"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def print_result(result):
    """Imprime un resultado de evaluación de forma legible"""
    print(f"\nObjetivo: {result.objective}")
    print(f"Timestamp: {result.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Duracion: {result.duration_seconds:.3f}s")
    print(f"\nDiagnostico:")
    print(f"   Estado: {result.diagnostic.status.value.upper()}")
    print(f"   Resumen: {result.diagnostic.summary}")
    print(f"   Score: {result.diagnostic.score_overall:.1%}")
    print(f"   Metricas: {result.diagnostic.metrics_passed}/{result.diagnostic.metrics_total}")
    
    if result.diagnostic.strengths:
        print(f"\nFortalezas:")
        for s in result.diagnostic.strengths:
            print(f"   {s}")
    
    if result.diagnostic.issues:
        print(f"\nProblemas:")
        for i in result.diagnostic.issues:
            print(f"   {i}")
    
    if result.diagnostic.recommendations:
        print(f"\nRecomendaciones:")
        for r in result.diagnostic.recommendations[:3]:  # Mostrar top 3
            print(f"   - {r}")


def demo_1_basic_evaluation():
    """Demo 1: Evaluación básica de un cubo"""
    print_section("DEMO 1: Evaluación Básica - Cubo Azul")
    
    evaluator = C1ResultEvaluator()
    
    # Scenario: Se ejecutó el comando "crear cubo azul"
    # y generó una escena con estos datos
    scene_data = {
        "object_count": 1,
        "total_volume": 8.0,    # Cubo 2x2x2 = 8 unidades cúbicas
        "materials": ["Blue"],
        "objects": {
            "Cube": {
                "type": "MESH",
                "location": [0, 0, 0],
                "dimensions": [2, 2, 2],
                "scale": [1, 1, 1]
            }
        }
    }
    
    # Evaluación
    result = evaluator.evaluate(
        objective="Crear un cubo azul de 2x2x2",
        scene_data=scene_data
    )
    
    print_result(result)
    return evaluator, result


def demo_2_partial_success():
    """Demo 2: Evaluación parcial (casi correcto)"""
    print_section("DEMO 2: Éxito Parcial - Cubo pero sin material")
    
    evaluator = C1ResultEvaluator()
    
    # Scenario: Se creó el cubo pero sin el material azul
    scene_data = {
        "object_count": 1,
        "total_volume": 8.0,    # Correcto
        "materials": [],         # ⚠️ Falta material
        "objects": {
            "Cube": {
                "type": "MESH",
                "dimensions": [2, 2, 2]
            }
        }
    }
    
    result = evaluator.evaluate(
        objective="Crear un cubo azul de 2x2x2",
        scene_data=scene_data
    )
    
    print_result(result)
    return evaluator, result


def demo_3_failure():
    """Demo 3: Evaluación fallida (equivocación completa)"""
    print_section("DEMO 3: Fallo - Se creó esfera en lugar de cubo")
    
    evaluator = C1ResultEvaluator()
    
    # Scenario: Se creó una esfera en lugar de un cubo
    scene_data = {
        "object_count": 1,
        "total_volume": 4.19,   # Aproximadamente una esfera de radio 1
        "materials": ["Red"],    # Color equivocado también
        "objects": {
            "Sphere": {
                "type": "MESH",
                "dimensions": [2, 2, 2]
            }
        }
    }
    
    result = evaluator.evaluate(
        objective="Crear un cubo azul de 2x2x2",
        scene_data=scene_data
    )
    
    print_result(result)
    return evaluator, result


def demo_4_complex_scene():
    """Demo 4: Evaluación compleja - múltiples objetos"""
    print_section("DEMO 4: Escena Compleja - Estructura con Soporte")
    
    evaluator = C1ResultEvaluator()
    
    # Scenario: Se creó una estructura de soporte
    scene_data = {
        "object_count": 3,
        "total_volume": 35.0,    # Múltiples objetos
        "materials": ["Steel", "Rubber"],
        "objects": {
            "Base": {
                "type": "MESH",
                "dimensions": [10, 10, 1],
                "material": "Steel"
            },
            "Support1": {
                "type": "MESH",
                "dimensions": [1, 1, 5],
                "material": "Steel"
            },
            "Support2": {
                "type": "MESH",
                "dimensions": [1, 1, 5],
                "material": "Steel"
            }
        }
    }
    
    expected = {
        "object_count": 3,
        "estimated_volume": 35.0,
        "materials": ["Steel", "Rubber"],
        "procedure": "Crear base y soportes estructurales"
    }
    
    result = evaluator.evaluate(
        objective="Crear estructura de soporte con base y 2 pilares",
        scene_data=scene_data,
        expected_result=expected
    )
    
    print_result(result)
    return evaluator, result


def demo_5_with_feedback():
    """Demo 5: Evaluación con feedback humano"""
    print_section("DEMO 5: Evaluación con Feedback Humano")
    
    evaluator = C1ResultEvaluator()
    
    scene_data = {
        "object_count": 1,
        "total_volume": 8.0,
        "materials": ["Blue"],
        "objects": {
            "Cube": {
                "type": "MESH",
                "dimensions": [2, 2, 2]
            }
        }
    }
    
    result = evaluator.evaluate_with_feedback(
        objective="Crear cubo con textura rugosa",
        scene_data=scene_data,
        human_feedback="El cubo necesita una textura más rugosa para simular hormigón"
    )
    
    print_result(result)
    return evaluator, result


def demo_6_history_and_export():
    """Demo 6: Historial y exportación"""
    print_section("DEMO 6: Historial y Exportacion a JSON")
    
    evaluator = C1ResultEvaluator()
    
    # Ejecutar varias evaluaciones
    evaluations = [
        ("Cubo simple", {"object_count": 1, "total_volume": 8.0, "materials": ["Blue"]}),
        ("Dos cubos", {"object_count": 2, "total_volume": 16.0, "materials": ["Blue", "Red"]}),
        ("Estructura", {"object_count": 3, "total_volume": 24.0, "materials": ["Steel"]}),
        ("Objeto incompleto", {"object_count": 1, "total_volume": 0.0, "materials": []}),
    ]
    
    print("\nEjecutando multiples evaluaciones...")
    for objective, scene in evaluations:
        result = evaluator.evaluate(objective, scene)
        print(f"   OK {objective}: {result.diagnostic.score_overall:.1%}")
    
    # Ver historial
    print("\nResumen del Historial:")
    summary = evaluator.get_history_summary()
    print(f"   Total evaluaciones: {summary['total']}")
    print(f"   Exitos: {summary['successes']}")
    print(f"   Parciales: {summary['partials']}")
    print(f"   Fallos: {summary['failures']}")
    print(f"   Score promedio: {summary['average_score']:.1%}")
    print(f"   Tasa de exito: {summary['success_rate']:.1%}")
    
    # Exportar última evaluación
    print("\nExportando evaluacion a JSON...")
    export_path = Path("exports/demo_c1_evaluation.json")
    evaluator.export_evaluation(
        evaluator.evaluation_history[-1],
        export_path
    )
    print(f"   Guardado en: {export_path}")
    
    # Mostrar contenido
    print("\nContenido exportado:")
    if export_path.exists():
        with open(export_path) as f:
            data = json.load(f)
            print(json.dumps(data, indent=2, ensure_ascii=False)[:500] + "...")
    
    return evaluator


def main():
    """Ejecuta todos los demos"""
    print("\n")
    print("=" * 70)
    print(" " * 15 + "DEMO C1 - EVALUADOR DE RESULTADOS")
    print(" " * 18 + "Plan C: Cognicion Base")
    print("=" * 70)
    
    # Ejecutar demos
    try:
        print("\nEjecutando demostraciones...\n")
        
        demo_1_basic_evaluation()
        demo_2_partial_success()
        demo_3_failure()
        demo_4_complex_scene()
        demo_5_with_feedback()
        demo_6_history_and_export()
        
        # Resumen final
        print_section("RESUMEN FINAL")
        print("""
COMPLETADO: Demostraciones exitosas.

C1 - Evaluador de Resultados:
  * Analiza escenas generadas
  * Calcula multiples tipos de metricas
  * Genera diagnosticos estructurados
  * Almacena historial de evaluaciones
  * Exporta a JSON para persistencia

Proximos pasos:
  1. C2 - Memoria de Experiencias (guardar lo aprendido)
  2. C3 - Objetivos Abstractos (traducir intenciones)
  3. C4 - Autoajuste Procedural (optimizar automaticamente)

Ver: bitacora/C1_EVALUADOR.md
        """)
        
    except Exception as e:
        print(f"\nError durante las demostraciones: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
