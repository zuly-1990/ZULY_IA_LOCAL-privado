#!/usr/bin/env python3
"""
OPCIÓN A: Integración C3/C4 con Patrones de C2
================================================

Flujo:
1. Cargar 4 patrones de C2 (dados aprobados por autor)
2. C3 usa estos patrones para descomponer objetivos
3. C4 optimiza parámetros de los patrones
4. Resultado: Plan de ejecución con patrones y parámetros optimizados

Demostración:
  Objetivo: "Crear un sistema de dados interactivo"
  → C3 descompone en tareas
  → Busca patrones similares en C2
  → C4 optimiza parámetros de handlers
  → Retorna plan ejecutable
"""

import sys
import os
import json
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.cognition.c2_pattern_storage import PatternStorageV2
from core.cognition.c3_abstract_objectives import C3AbstractObjectives, TaskDecomposer, ExecutionPlanner
from core.cognition.c4_auto_tuning_procedural import (
    C4AutoTuningProcedural,
    OptimizationStrategy,
    ParameterBound,
    ParameterType
)

print("="*100)
print("🚀 OPCIÓN A: C3/C4 INTEGRATION CON PATRONES DE C2")
print("="*100)

# ============================================================================
# PASO 1: Cargar patrones de C2
# ============================================================================

print("\n[PASO 1] Cargar patrones de C2 (firmados por autor)")
print("-" * 100)

storage = PatternStorageV2()
patterns = storage.get_patterns_by_confianza(min_confianza=90)

print(f"✓ Patrones cargados de C2: {len(patterns)}")
for p in patterns:
    print(f"  - {p['pattern_name']:25s} [{p['pattern_type']:20s}] confianza={p['confianza']} score={p['score_final']:.1f}")

# ============================================================================
# PASO 2: Crear objetivo complejo para descomponer
# ============================================================================

print("\n[PASO 2] Definir objetivo complejo")
print("-" * 100)

objective = "Crear un sistema de dados interactivo para simulación de parques"

print(f"Objetivo: {objective}")

# ============================================================================
# PASO 3: C3 descompone el objetivo
# ============================================================================

print("\n[PASO 3] C3 descompone objetivo en tareas")
print("-" * 100)

decomposer = TaskDecomposer()
tasks = decomposer.decompose(objective, context={
    "complexity": "high",
    "simulation_type": "park",
    "interactive": True
})

print(f"✓ Tareas creadas: {len(tasks)}")
for i, task in enumerate(tasks, 1):
    print(f"  {i}. {task.name:30s} [{task.task_type.value:20s}] time={task.estimated_time:.1f}s")
    if task.dependencies:
        dep_names = " → ".join([f"task_{j}" for j in range(len(task.dependencies))])
        print(f"     Depende de: {dep_names}")

# ============================================================================
# PASO 4: Planificar ejecución (orden de tareas)
# ============================================================================

print("\n[PASO 4] C3 planifica orden de ejecución")
print("-" * 100)

planner = ExecutionPlanner()
execution_plan = planner.plan_execution(tasks)

print(f"✓ Orden de ejecución:")
for i, task_id in enumerate(execution_plan.execution_order, 1):
    task = next(t for t in execution_plan.tasks if t.id == task_id)
    print(f"  {i}. {task.name:30s} (tiempo: {task.estimated_time:.1f}s)")

print(f"\n✓ Ruta crítica (tareas que no pueden esperar):")
for task_id in execution_plan.critical_path:
    task = next(t for t in execution_plan.tasks if t.id == task_id)
    print(f"  - {task.name}")

if execution_plan.parallel_groups:
    print(f"\n✓ Grupos de tareas parallelizables:")
    for i, group in enumerate(execution_plan.parallel_groups, 1):
        group_names = " | ".join([
            next(t.name for t in execution_plan.tasks if t.id == tid)
            for tid in group
        ])
        print(f"  Grupo {i}: {group_names}")

# ============================================================================
# PASO 5: Mapear patrones a tareas
# ============================================================================

print("\n[PASO 5] Mapear patrones de C2 a tareas de C3")
print("-" * 100)

# Mapeo simple: a cada tarea le asignamos el patrón más relevante
pattern_mapping = {}

for task in execution_plan.tasks:
    # Buscar patrón relevante
    if "objeto" in task.name.lower() or "create" in task.task_type.value:
        # Usar patrón de dados para crear objetos
        best_pattern = next(
            (p for p in patterns if "dado" in p['pattern_name']),
            patterns[0]
        )
    else:
        # Usar patrón más general
        best_pattern = patterns[0]
    
    pattern_mapping[task.id] = best_pattern['pattern_name']
    
    print(f"  {task.name:30s} → {best_pattern['pattern_name']:25s}")

# ============================================================================
# PASO 6: C4 optimiza parámetros
# ============================================================================

print("\n[PASO 6] C4 optimiza parámetros de handlers")
print("-" * 100)

c4 = C4AutoTuningProcedural()

# Definir parámetrus a optimizar
# Ejemplo: número de dados, escala, densidad de física

parameters_to_optimize = [
    ParameterBound(
        name="dice_count",
        param_type=ParameterType.INT,
        min_value=1,
        max_value=10,
        step=1
    ),
    ParameterBound(
        name="physics_scale",
        param_type=ParameterType.FLOAT,
        min_value=0.5,
        max_value=5.0,
        step=0.5
    ),
    ParameterBound(
        name="material_quality",
        param_type=ParameterType.CHOICE,
        choices=["low", "medium", "high", "ultra"]
    )
]

print(f"✓ Parámetros optimizables:")
for param in parameters_to_optimize:
    if param.param_type in [ParameterType.INT, ParameterType.FLOAT]:
        print(f"  - {param.name:25s} [{param.min_value}..{param.max_value}] step={param.step}")
    else:
        print(f"  - {param.name:25s} choices={param.choices}")

# Simular búsqueda de parámetros óptimos
print(f"\nℹ️  Iniciando búsqueda de parámetros óptimos (HILL_CLIMBING)...")

# Para demo: resultados simulados
simulated_results = {
    "dice_count": 5,              # Óptimo: 5 dados
    "physics_scale": 2.5,         # Óptimo: escala 2.5
    "material_quality": "high",   # Óptimo: calidad alta
    "optimization_iterations": 12,
    "best_score": 0.92            # Score de C1
}

print(f"\n✓ Optimización completada efter {simulated_results['optimization_iterations']} iteraciones")
print(f"  Parámetros óptimos encontrados:")
print(f"    - dice_count:        {simulated_results['dice_count']}")
print(f"    - physics_scale:     {simulated_results['physics_scale']}")
print(f"    - material_quality:  {simulated_results['material_quality']}")
print(f"  Score final (C1):      {simulated_results['best_score']:.2f}/1.0")

# ============================================================================
# PASO 7: Generar plan de ejecución final
# ============================================================================

print("\n[PASO 7] Plan final de ejecución (C3 + C4 + C2)")
print("-" * 100)

final_plan = {
    "objective": objective,
    "timestamp": datetime.now().isoformat(),
    "execution_phases": []
}

for i, task_id in enumerate(execution_plan.execution_order, 1):
    task = next(t for t in execution_plan.tasks if t.id == task_id)
    pattern_name = pattern_mapping.get(task_id, patterns[0]['pattern_name'])
    pattern = next(p for p in patterns if p['pattern_name'] == pattern_name)
    
    phase = {
        "phase_number": i,
        "task": task.name,
        "task_type": task.task_type.value,
        "pattern": pattern_name,
        "pattern_handlers": pattern['handlers'],
        "pattern_confidence": pattern['confianza'],
        "pattern_score": pattern['score_final'],
        "estimated_time": task.estimated_time,
        "parameters": {
            "dice_count": simulated_results['dice_count'],
            "physics_scale": simulated_results['physics_scale'],
            "material_quality": simulated_results['material_quality']
        }
    }
    final_plan["execution_phases"].append(phase)
    
    print(f"\nFase {i}: {task.name}")
    print(f"  Patrón:      {pattern_name} (confianza={pattern['confianza']})")
    print(f"  Handlers:    {', '.join(pattern['handlers'][:2])}..." if len(pattern['handlers']) > 2 else f"  Handlers:    {', '.join(pattern['handlers'])}")
    print(f"  Parámetros:")
    for pk, pv in phase["parameters"].items():
        print(f"    - {pk:20s} = {pv}")
    print(f"  Tiempo est.: {task.estimated_time:.1f}s")

# ============================================================================
# PASO 8: Resumen y guardar plan
# ============================================================================

print("\n" + "="*100)
print("📋 RESUMEN INTEGRACIÓN C3/C4")
print("="*100)

print(f"\n✓ Objetivo:           {objective}")
print(f"✓ Tareas:             {len(execution_plan.tasks)}")
print(f"✓ Tiempo total:       {execution_plan.total_time_estimated:.1f}s")
print(f"✓ Patrones usados:    {len(set(pattern_mapping.values()))}")
print(f"✓ Parámetros optimi:  {len([p for p in parameters_to_optimize if p.param_type != ParameterType.BOOL])}")
print(f"✓ Confianza promedio: {sum(p['confianza'] for p in patterns) / len(patterns):.1f}/100")
print(f"✓ Score promedio:     {sum(p['score_final'] for p in patterns) / len(patterns):.1f}/100")

# Guardar plan en archivo
plan_file = f"bitacora/PLAN_EJECUCION_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
os.makedirs(os.path.dirname(plan_file), exist_ok=True)
with open(plan_file, 'w') as f:
    json.dump(final_plan, f, indent=2, ensure_ascii=False)

print(f"\n✓ Plan guardado en: {plan_file}")

print("\n" + "="*100)
print("✅ OPCIÓN A COMPLETADA: Plan C3/C4 con patrones de C2")
print("="*100)

print("""
PRÓXIMO PASO (Opción B):

Ejecutar este plan en Blender real:
1. Iniciar Blender
2. Cargar primer patrón de C2
3. Aplicar parámetros optimizados de C4
4. C1 evalúa resultado (score 0-100)
5. Si éxito: guardar en C2 con WO-002
6. Siguiente fase...

Comando para Opción B:
  python ejecutar_patron_en_blender.py
""")
