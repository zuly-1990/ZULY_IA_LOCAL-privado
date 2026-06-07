"""
C3 - Abstract Objectives
========================

Parte del Plan C (Cognición Base) - Fase de Descomposición

Responsabilidades:
1. Descomponer objetivos complejos en subtareas
2. Analizar dependencias entre tareas
3. Planificar orden de ejecución
4. Sugerir estrategias de ejecución

Componentes:
- TaskDecomposer: Descompone objetivos en subtareas
- DependencyAnalyzer: Analiza dependencias
- ExecutionPlanner: Planifica orden de ejecución
- C3AbstractObjectives: Orquestador
"""

import json
from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass, asdict, field
from enum import Enum
from pathlib import Path
from collections import defaultdict


class TaskPriority(Enum):
    """Prioridad de tareas"""
    CRITICAL = "critical"       # Debe ejecutarse primero
    HIGH = "high"               # Importante
    MEDIUM = "medium"           # Normal
    LOW = "low"                 # Puede esperar


class TaskType(Enum):
    """Tipos de tareas"""
    CREATE_OBJECT = "create_object"        # Crear objeto 3D
    MODIFY_OBJECT = "modify_object"        # Modificar objeto
    APPLY_MATERIAL = "apply_material"      # Aplicar material
    ADD_LIGHTING = "add_lighting"          # Agregar iluminación
    RENDER = "render"                      # Renderizar
    COMPOSITE = "composite"                # Tarea compuesta (contiene subtareas)
    CUSTOM = "custom"                      # Otra


@dataclass
class Task:
    """Una subtarea descompuesta"""
    id: str                             # Identificador único
    name: str                           # Nombre de la tarea
    description: str                    # Descripción
    task_type: TaskType                 # Tipo de tarea
    priority: TaskPriority              # Prioridad
    estimated_time: float               # Tiempo estimado en segundos
    dependencies: List[str] = field(default_factory=list)  # IDs de tareas que debe esperar
    parameters: Dict[str, Any] = field(default_factory=dict)  # Parámetros de ejecución
    subtasks: List[str] = field(default_factory=list)  # IDs de subtareas (si es compuesta)
    
    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data['task_type'] = self.task_type.value
        data['priority'] = self.priority.value
        return data


@dataclass
class ExecutionPlan:
    """Plan de ejecución con orden de tareas"""
    tasks: List[Task]                   # Todas las tareas
    execution_order: List[str]          # Orden de ejecución (IDs)
    critical_path: List[str]            # Camino crítico
    total_time_estimated: float         # Tiempo total estimado
    parallel_groups: List[List[str]] = field(default_factory=list)  # Tareas que pueden correr en paralelo


class TaskDecomposer:
    """Descompone objetivos complejos en subtareas"""
    
    # Plantillas de descomposición
    DECOMPOSITION_TEMPLATES = {
        'crear escena 3d': {
            'subtasks': [
                {'name': 'Crear objetos básicos', 'type': 'CREATE_OBJECT', 'priority': 'CRITICAL'},
                {'name': 'Aplicar materiales', 'type': 'APPLY_MATERIAL', 'priority': 'HIGH'},
                {'name': 'Agregar iluminación', 'type': 'ADD_LIGHTING', 'priority': 'HIGH'},
                {'name': 'Renderizar', 'type': 'RENDER', 'priority': 'MEDIUM'},
            ]
        },
        'renderizar escena': {
            'subtasks': [
                {'name': 'Verificar materiales', 'type': 'MODIFY_OBJECT', 'priority': 'HIGH'},
                {'name': 'Ajustar iluminación', 'type': 'ADD_LIGHTING', 'priority': 'HIGH'},
                {'name': 'Configurar cámara', 'type': 'MODIFY_OBJECT', 'priority': 'MEDIUM'},
                {'name': 'Renderizar', 'type': 'RENDER', 'priority': 'CRITICAL'},
            ]
        },
        'crear objeto texturizado': {
            'subtasks': [
                {'name': 'Crear objeto', 'type': 'CREATE_OBJECT', 'priority': 'CRITICAL'},
                {'name': 'Crear material', 'type': 'APPLY_MATERIAL', 'priority': 'HIGH'},
                {'name': 'Aplicar textura', 'type': 'APPLY_MATERIAL', 'priority': 'HIGH'},
                {'name': 'Verificar resultado', 'type': 'MODIFY_OBJECT', 'priority': 'MEDIUM'},
            ]
        },
    }
    
    @staticmethod
    def decompose(objective: str, context: Optional[Dict[str, Any]] = None) -> List[Task]:
        """
        Descompone un objetivo en subtareas.
        
        Args:
            objective: Objetivo a descomponer ("Crear escena 3D completa")
            context: Contexto adicional (parámetros, preferencias)
            
        Returns:
            Lista de tareas
        """
        objective_lower = objective.lower()
        
        # Buscar plantilla coincidente
        for template_key, template in TaskDecomposer.DECOMPOSITION_TEMPLATES.items():
            if template_key in objective_lower:
                return TaskDecomposer._create_tasks_from_template(template, context)
        
        # Si no encuentra plantilla, descomponer genéricamente
        return TaskDecomposer._decompose_generic(objective, context)
    
    @staticmethod
    def _create_tasks_from_template(template: Dict, context: Optional[Dict]) -> List[Task]:
        """Crea tareas a partir de una plantilla"""
        tasks = []
        
        for i, subtask_info in enumerate(template['subtasks']):
            task = Task(
                id=f"task_{i}",
                name=subtask_info['name'],
                description=f"Subtarea: {subtask_info['name']}",
                task_type=TaskType[subtask_info['type']],
                priority=TaskPriority[subtask_info['priority']],
                estimated_time=5.0 + (i * 2),  # 5s, 7s, 9s, etc
                dependencies=[f"task_{j}" for j in range(max(0, i-1), i)],  # Dependencia de tarea anterior
                parameters=context or {}
            )
            tasks.append(task)
        
        return tasks
    
    @staticmethod
    def _decompose_generic(objective: str, context: Optional[Dict]) -> List[Task]:
        """Descomposición genérica para objetivos desconocidos"""
        tasks = []
        
        # Tarea principal
        task = Task(
            id="task_0",
            name=objective,
            description=f"Objetivo: {objective}",
            task_type=TaskType.CUSTOM,
            priority=TaskPriority.CRITICAL,
            estimated_time=10.0,
            parameters=context or {}
        )
        tasks.append(task)
        
        return tasks


class DependencyAnalyzer:
    """Analiza dependencias entre tareas"""
    
    @staticmethod
    def analyze_dependencies(tasks: List[Task]) -> Dict[str, Set[str]]:
        """
        Analiza todas las dependencias.
        
        Returns:
            Dict: {task_id -> set(task_ids que depende)}
        """
        dependencies = defaultdict(set)
        
        for task in tasks:
            for dep in task.dependencies:
                dependencies[task.id].add(dep)
        
        return dict(dependencies)
    
    @staticmethod
    def detect_circular_dependencies(tasks: List[Task]) -> List[Tuple[str, str]]:
        """
        Detecta dependencias circulares (si las hay).
        
        Returns:
            Lista de tuplas (task_a, task_b) que forman ciclo
        """
        dependencies = DependencyAnalyzer.analyze_dependencies(tasks)
        circular = []
        
        def has_cycle(task_id: str, visited: Set[str], rec_stack: Set[str]) -> bool:
            visited.add(task_id)
            rec_stack.add(task_id)
            
            for dep in dependencies.get(task_id, set()):
                if dep not in visited:
                    if has_cycle(dep, visited, rec_stack):
                        return True
                elif dep in rec_stack:
                    circular.append((task_id, dep))
                    return True
            
            rec_stack.remove(task_id)
            return False
        
        visited = set()
        for task in tasks:
            if task.id not in visited:
                has_cycle(task.id, visited, set())
        
        return circular
    
    @staticmethod
    def calculate_critical_path(tasks: List[Task]) -> List[str]:
        """
        Calcula el camino crítico (tareas que no pueden retrasarse).
        
        Returns:
            Lista de IDs de tareas en camino crítico
        """
        if not tasks:
            return []
        
        # Crear diccionario de tareas por ID
        task_map = {t.id: t for t in tasks}
        
        # Calcular duración máxima desde cada tarea
        durations = {}
        
        def get_max_duration(task_id: str) -> float:
            if task_id in durations:
                return durations[task_id]
            
            task = task_map.get(task_id)
            if not task:
                return 0.0
            
            if not task.dependencies:
                durations[task_id] = task.estimated_time
                return task.estimated_time
            
            max_dep_duration = max(get_max_duration(dep) for dep in task.dependencies)
            durations[task_id] = task.estimated_time + max_dep_duration
            return durations[task_id]
        
        # Calcular duración para todas
        for task in tasks:
            get_max_duration(task.id)
        
        # Encontrar máximo
        max_duration = max(durations.values()) if durations else 0
        
        # Tareas en camino crítico
        critical = [task_id for task_id, duration in durations.items() 
                   if duration == max_duration]
        
        return critical


class ExecutionPlanner:
    """Planifica orden de ejecución de tareas"""
    
    @staticmethod
    def plan_execution(tasks: List[Task]) -> ExecutionPlan:
        """
        Crea plan de ejecución.
        
        Returns:
            ExecutionPlan con orden y grupos paralelos
        """
        # Verificar ciclos
        cycles = DependencyAnalyzer.detect_circular_dependencies(tasks)
        if cycles:
            raise ValueError(f"Dependencias circulares detectadas: {cycles}")
        
        # Ordenamiento topológico
        execution_order = ExecutionPlanner._topological_sort(tasks)
        
        # Camino crítico
        critical_path = DependencyAnalyzer.calculate_critical_path(tasks)
        
        # Grupos paralelos
        parallel_groups = ExecutionPlanner._identify_parallel_groups(tasks, execution_order)
        
        # Tiempo total
        total_time = max((t.estimated_time for t in tasks), default=0)
        
        return ExecutionPlan(
            tasks=tasks,
            execution_order=execution_order,
            critical_path=critical_path,
            total_time_estimated=total_time,
            parallel_groups=parallel_groups
        )
    
    @staticmethod
    def _topological_sort(tasks: List[Task]) -> List[str]:
        """Ordenamiento topológico de tareas"""
        task_map = {t.id: t for t in tasks}
        visited = set()
        order = []
        
        def visit(task_id: str):
            if task_id in visited:
                return
            visited.add(task_id)
            
            task = task_map.get(task_id)
            if task:
                for dep in task.dependencies:
                    visit(dep)
            
            order.append(task_id)
        
        for task in tasks:
            visit(task.id)
        
        return order
    
    @staticmethod
    def _identify_parallel_groups(tasks: List[Task], execution_order: List[str]) -> List[List[str]]:
        """Identifica tareas que pueden ejecutarse en paralelo"""
        groups = []
        current_group = []
        task_map = {t.id: t for t in tasks}
        
        for task_id in execution_order:
            task = task_map.get(task_id)
            if not task or not task.dependencies:
                if current_group:
                    groups.append(current_group)
                current_group = [task_id]
            else:
                # Puede ejecutarse después de dependencias
                current_group.append(task_id)
        
        if current_group:
            groups.append(current_group)
        
        return groups


class C3AbstractObjectives:
    """
    Objectives Principal (C3)
    
    Orquesta descomposición, análisis y planificación de objetivos.
    """
    
    def __init__(self):
        self.decomposer = TaskDecomposer()
        self.analyzer = DependencyAnalyzer()
        self.planner = ExecutionPlanner()
        self.plans_history: List[ExecutionPlan] = []
    
    def decompose_objective(self, objective: str, context: Optional[Dict[str, Any]] = None) -> ExecutionPlan:
        """
        Descompone un objetivo y crea plan de ejecución.
        
        Args:
            objective: Objetivo a descomponer
            context: Contexto adicional
            
        Returns:
            ExecutionPlan listo para ejecutar
        """
        # 1. Descomponer
        tasks = self.decomposer.decompose(objective, context)
        
        # 2. Analizar dependencias
        cycles = self.analyzer.detect_circular_dependencies(tasks)
        if cycles:
            raise ValueError(f"Dependencias circulares: {cycles}")
        
        # 3. Planificar
        plan = self.planner.plan_execution(tasks)
        
        # 4. Guardar en historial
        self.plans_history.append(plan)
        
        return plan
    
    def get_next_tasks(self, plan: ExecutionPlan, completed_ids: List[str]) -> List[Task]:
        """
        Obtiene siguiente(s) tarea(s) a ejecutar.
        
        Args:
            plan: Plan de ejecución
            completed_ids: IDs de tareas ya completadas
            
        Returns:
            Lista de tareas listas para ejecutar
        """
        task_map = {t.id: t for t in plan.tasks}
        ready = []
        
        for task_id in plan.execution_order:
            if task_id in completed_ids:
                continue
            
            task = task_map.get(task_id)
            if not task:
                continue
            
            # Verificar si todas las dependencias están completas
            if all(dep in completed_ids for dep in task.dependencies):
                ready.append(task)
        
        return ready
    
    def export_plan(self, plan: ExecutionPlan, filepath: Path) -> bool:
        """Exporta plan a JSON"""
        try:
            data = {
                'execution_order': plan.execution_order,
                'critical_path': plan.critical_path,
                'total_time_estimated': plan.total_time_estimated,
                'parallel_groups': plan.parallel_groups,
                'tasks': [t.to_dict() for t in plan.tasks]
            }
            
            filepath.parent.mkdir(parents=True, exist_ok=True)
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"Error exportando plan: {e}")
            return False
    
    def get_summary(self, plan: ExecutionPlan) -> Dict[str, Any]:
        """Obtiene resumen del plan"""
        return {
            'total_tasks': len(plan.tasks),
            'execution_order': plan.execution_order,
            'critical_path': plan.critical_path,
            'critical_path_length': len(plan.critical_path),
            'total_time_estimated': plan.total_time_estimated,
            'parallel_groups': plan.parallel_groups,
            'task_types': [t.task_type.value for t in plan.tasks],
            'task_priorities': [t.priority.value for t in plan.tasks]
        }
