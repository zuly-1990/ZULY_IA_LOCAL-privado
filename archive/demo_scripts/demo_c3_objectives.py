"""
Demo de C3 - Abstract Objectives
Demuestra descomposición automática de objetivos complejos
"""

from core.cognition.c3_abstract_objectives import C3AbstractObjectives


def print_section(title: str):
    """Imprime sección"""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}")


def demo_basic_decomposition():
    """Demo 1: Descomposición básica"""
    print_section("DEMO 1: Descomposición Basica")
    
    c3 = C3AbstractObjectives()
    
    print("\n[*] Objetivo: Crear una escena 3D")
    plan = c3.decompose_objective('crear escena 3d')
    
    print(f"\n[+] Plan generado:")
    print(f"  - Total de tareas: {len(plan.tasks)}")
    print(f"  - Tiempo estimado: {plan.total_time_estimated:.1f}s")
    
    print(f"\n[*] Tareas:")
    for i, task in enumerate(plan.tasks, 1):
        print(f"  {i}. {task.name} ({task.priority.value})")
        print(f"     Tipo: {task.task_type.value}, Tiempo: {task.estimated_time}s")


def demo_execution_order():
    """Demo 2: Orden de ejecución"""
    print_section("DEMO 2: Orden de Ejecucion")
    
    c3 = C3AbstractObjectives()
    
    print("\n[*] Generando plan para: Renderizar escena")
    plan = c3.decompose_objective('renderizar escena')
    
    print(f"\n[+] Orden de ejecución:")
    for i, task_id in enumerate(plan.execution_order, 1):
        task = next(t for t in plan.tasks if t.id == task_id)
        deps_str = f" (deps: {task.dependencies})" if task.dependencies else ""
        print(f"  {i}. [{task_id}] {task.name}{deps_str}")
    
    print(f"\n[+] Camino crítico:")
    for task_id in plan.critical_path:
        task = next(t for t in plan.tasks if t.id == task_id)
        print(f"  - {task.name}")


def demo_parallel_execution():
    """Demo 3: Tareas paralelas"""
    print_section("DEMO 3: Tareas Paralelas (Pueden ejecutarse juntas)")
    
    c3 = C3AbstractObjectives()
    plan = c3.decompose_objective('crear objeto texturizado')
    
    print(f"\n[+] Grupos de tareas paralelas:")
    for group_num, group in enumerate(plan.parallel_groups, 1):
        print(f"\n  Grupo {group_num}:")
        for task_id in group:
            task = next(t for t in plan.tasks if t.id == task_id)
            print(f"    - {task.name}")


def demo_sequential_task_allocation():
    """Demo 4: Asignación secuencial de tareas"""
    print_section("DEMO 4: Asignacion Secuencial")
    
    c3 = C3AbstractObjectives()
    plan = c3.decompose_objective('crear escena 3d')
    
    print("\n[*] Simulando ejecución secuencial de tareas...")
    completed = []
    
    for step in range(len(plan.tasks)):
        next_tasks = c3.get_next_tasks(plan, completed)
        
        if not next_tasks:
            break
        
        print(f"\n[Paso {step+1}] Tareas disponibles:")
        for task in next_tasks:
            print(f"  - {task.name} ({task.task_type.value})")
        
        # Simular completar la primera tarea disponible
        first_task = next_tasks[0]
        completed.append(first_task.id)
        print(f"  [+] Completado: {first_task.name}")
    
    print(f"\n[*] Ejecución completa. Tareas finalizadas: {len(completed)}/{len(plan.tasks)}")


def demo_plan_summary():
    """Demo 5: Resumen del plan"""
    print_section("DEMO 5: Resumen del Plan")
    
    c3 = C3AbstractObjectives()
    plan = c3.decompose_objective('crear escena 3d completa')
    summary = c3.get_summary(plan)
    
    print(f"\n[+] Resumen del plan:")
    print(f"  - Total de tareas: {summary['total_tasks']}")
    print(f"  - Tareas en camino crítico: {summary['critical_path_length']}")
    print(f"  - Tiempo total estimado: {summary['total_time_estimated']:.1f}s")
    print(f"  - Grupos paralelos: {len(summary['parallel_groups'])}")
    
    print(f"\n[+] Tipos de tareas:")
    task_types = {}
    for task_type in summary['task_types']:
        task_types[task_type] = task_types.get(task_type, 0) + 1
    
    for task_type, count in task_types.items():
        print(f"  - {task_type}: {count}")
    
    print(f"\n[+] Distribución de prioridades:")
    priorities = {}
    for priority in summary['task_priorities']:
        priorities[priority] = priorities.get(priority, 0) + 1
    
    for priority in ['critical', 'high', 'medium', 'low']:
        count = priorities.get(priority, 0)
        if count > 0:
            print(f"  - {priority.upper()}: {count}")


def demo_multiple_objectives():
    """Demo 6: Múltiples objetivos"""
    print_section("DEMO 6: Multiples Objetivos")
    
    c3 = C3AbstractObjectives()
    
    objectives = [
        'crear escena 3d',
        'renderizar escena',
        'crear objeto texturizado'
    ]
    
    print(f"\n[*] Procesando {len(objectives)} objetivos diferentes...")
    
    for obj in objectives:
        print(f"\n[+] Objetivo: {obj}")
        plan = c3.decompose_objective(obj)
        print(f"    Tareas: {len(plan.tasks)}, Tiempo: {plan.total_time_estimated:.1f}s")
    
    print(f"\n[+] Historial de planes: {len(c3.plans_history)}")


def main():
    """Ejecuta todas las demostraciones"""
    print("\n")
    print("  " + "="*68)
    print("  " + " "*15 + "C3 - OBJETIVOS ABSTRACTOS")
    print("  " + " "*18 + "DEMOSTRACIÓN COMPLETA")
    print("  " + "="*68)
    
    try:
        demo_basic_decomposition()
        demo_execution_order()
        demo_parallel_execution()
        demo_sequential_task_allocation()
        demo_plan_summary()
        demo_multiple_objectives()
        
        print_section("CONCLUSION")
        print("\n[OK] Todas las demostraciones completadas exitosamente!")
        print("\nC3 demuestra capacidades de:")
        print("  - Descomponer objetivos complejos automáticamente")
        print("  - Analizar dependencias entre tareas")
        print("  - Identificar camino crítico")
        print("  - Detectar tareas paralelas")
        print("  - Planificar orden de ejecución")
        print("  - Generar resúmenes de planes")
        
        print("\n[+] Próximo paso: C4 - Auto-tuning Procedural")
        print("    C4 optimizará parámetros automáticamente\n")
        
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
