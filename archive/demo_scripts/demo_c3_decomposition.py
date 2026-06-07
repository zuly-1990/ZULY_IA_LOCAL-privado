#!/usr/bin/env python3
"""
Demo ejecutable: C3 Objectives - Task Decomposition

Ejecutar con: python demo_c3_decomposition.py
"""

import sys
sys.path.insert(0, '.')

try:
    from core.cognition.c3_task_decomposer import TaskDecomposer
    from core.cognition.c3_dependency_graph import DependencyGraph
    from core.cognition.c3_scheduler import TaskScheduler
except ImportError:
    print("Error: Módulos C3 no encontrados. Asegúrate de ejecutar desde ZULY_IA_LOCAL")
    sys.exit(1)


def main():
    """Ejecución demo."""
    print("\n" + "="*70)
    print("🎯 C3 OBJECTIVES - DEMO DESCOMPOSICIÓN")
    print("="*70)
    
    decomposer = TaskDecomposer()
    
    # Test objetivo complejo
    objective = "Crea una escena arquitectónica completa"
    print(f"\nObjetivo: {objective}")
    print("-" * 70)
    
    plan = decomposer.decompose(objective)
    
    print(f"\n✓ Plan generado:")
    print(f"  Tareas: {len(plan.tasks)}")
    print(f"  Complejidad: {plan.complexity_score:.0%}")
    print(f"  Duración: {plan.total_estimated_time_sec/60:.1f} min")
    
    print(f"\n📋 Tareas:")
    for i, task in enumerate(plan.tasks, 1):
        print(f"  {i}. {task.name} ({task.task_type.value})")
    
    # Grafo
    graph = DependencyGraph()
    for task in plan.tasks:
        graph.add_task(task.id, task.name, task.estimated_time_sec, task.depends_on)
    
    if graph.validate()[0]:
        critical_path, duration = graph.calculate_critical_path()
        print(f"\n✓ Camino crítico: {duration/60:.1f} min")
    
    print("\n✅ Demo completada")


if __name__ == '__main__':
    main()
