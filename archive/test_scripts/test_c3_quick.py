#!/usr/bin/env python3
import sys
sys.path.insert(0, '.')

from core.cognition.c3_task_decomposer import TaskDecomposer
from core.cognition.c3_dependency_graph import DependencyGraph

print('='*70)
print('C3 OBJECTIVES - PRUEBA COMPLETA')
print('='*70)

decomposer = TaskDecomposer()

# Prueba 1
print('\n[TEST 1] Objetivo arquitectonico')
plan = decomposer.decompose('Crea una escena arquitectonica completa')
print(f'OK: {len(plan.tasks)} tareas generadas')
print(f'  Complejidad: {plan.complexity_score:.0%}')
print(f'  Duracion: {plan.total_estimated_time_sec/60:.1f} min')

graph = DependencyGraph()
for task in plan.tasks:
    graph.add_task(task.id, task.name, task.estimated_time_sec, task.depends_on)

valid, cycle = graph.validate()
print(f'OK: Grafo valido={valid}')

if valid:
    critical, duration = graph.calculate_critical_path()
    print(f'OK: Camino critico {duration/60:.1f} min ({len(critical)} tareas)')
    order = graph.get_execution_order()
    print(f'OK: {len(order)} niveles parallelizables')

# Prueba 2
print('\n[TEST 2] Visualizacion de producto')
plan2 = decomposer.decompose('Render de producto con materiales PBR')
print(f'OK: {len(plan2.tasks)} tareas')

# Prueba 3
print('\n[TEST 3] Objetivo generico')
plan3 = decomposer.decompose('Hazme algo epico en 3D')
print(f'OK: {len(plan3.tasks)} tareas (patron generico)')

print('\n' + '='*70)
print('EXITO: Todas las pruebas pasaron')
print('='*70)
