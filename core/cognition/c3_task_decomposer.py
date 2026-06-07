"""
C3 - Task Decomposition Engine
===============================

Descompone objetivos complejos en subtareas ejecutables automáticamente.

ARQUITECTURA:
    Objetivo complejo → Análisis de intención → Árbol de tareas → Plan ejecutable

Ejemplo:
    Input:  "Crea una escena arquitectónica completa"
    Output: 
        1. Crear plano base
        2. Importar referencia 2D
        3. Trazar muros
        4. Agregar puertas/ventanas
        5. Aplicar materiales
        6. Iluminación
        7. Renderizar

RESPONSABILIDADES:
    - Analizar objetivo en lenguaje natural
    - Identificar dependencias entre subtareas
    - Generar plan secuencial con paralelización donde sea posible
    - Estimar complejidad y tiempo
    - Integración con C2 (almacenar patrones de descomposición aprendidos)
"""

import json
from enum import Enum
from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass, asdict, field
from datetime import datetime
import hashlib


class TaskPriority(Enum):
    """Prioridad de ejecución"""
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4


class TaskType(Enum):
    """Tipos de tareas"""
    CREATE = "create"              # Crear objeto
    TRANSFORM = "transform"        # Mover, rotar, escalar
    MATERIAL = "material"          # Aplicar materiales/texturas
    LIGHTING = "lighting"          # Iluminación
    CAMERA = "camera"              # Posicionar cámara
    RENDER = "render"              # Renderizar
    IMPORT = "import"              # Importar archivo
    EXPORT = "export"              # Exportar archivo
    MODIFIER = "modifier"          # Aplicar modificadores
    COMPOUND = "compound"          # Tarea compuesta (contiene subtareas)


@dataclass
class SubTask:
    """Subtarea individual"""
    id: str
    name: str
    description: str
    task_type: TaskType
    priority: TaskPriority = TaskPriority.MEDIUM
    depends_on: List[str] = field(default_factory=list)  # IDs de tareas previas
    estimated_time_sec: float = 10.0
    parameters: Dict[str, Any] = field(default_factory=dict)
    is_completed: bool = False
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'task_type': self.task_type.value,
            'priority': self.priority.value,
            'depends_on': self.depends_on,
            'estimated_time_sec': self.estimated_time_sec,
            'parameters': self.parameters,
            'is_completed': self.is_completed,
            'result': self.result,
            'error': self.error
        }


@dataclass
class DecompositionPlan:
    """Plan de descomposición de un objetivo"""
    objective: str
    plan_id: str = field(default_factory=lambda: hashlib.md5(str(datetime.now()).encode()).hexdigest()[:8])
    tasks: List[SubTask] = field(default_factory=list)
    total_estimated_time_sec: float = 0.0
    complexity_score: float = 0.0  # 0-1, 1 = muy complejo
    parallelizable_groups: List[List[str]] = field(default_factory=list)  # Grupos de tareas parallelizables
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    status: str = "pending"  # pending, executing, completed, failed
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'objective': self.objective,
            'plan_id': self.plan_id,
            'tasks': [t.to_dict() for t in self.tasks],
            'total_estimated_time_sec': self.total_estimated_time_sec,
            'complexity_score': self.complexity_score,
            'parallelizable_groups': self.parallelizable_groups,
            'created_at': self.created_at,
            'status': self.status
        }


class TaskDecomposer:
    """Motor de descomposición de tareas."""
    
    def __init__(self):
        """Inicializa descompositor."""
        self.decomposition_patterns = self._init_patterns()
        self.task_counter = 0
        
    def _init_patterns(self) -> Dict[str, List[Dict[str, Any]]]:
        """Inicializa patrones conocidos de descomposición."""
        return {
            'architectural_scene': [
                {'name': 'Crear plano base', 'type': TaskType.CREATE, 'priority': TaskPriority.CRITICAL},
                {'name': 'Importar referencia 2D', 'type': TaskType.IMPORT, 'priority': TaskPriority.HIGH},
                {'name': 'Trazar muros', 'type': TaskType.CREATE, 'priority': TaskPriority.HIGH, 'depends_on': [0]},
                {'name': 'Agregar puertas/ventanas', 'type': TaskType.CREATE, 'priority': TaskPriority.MEDIUM, 'depends_on': [2]},
                {'name': 'Aplicar materiales', 'type': TaskType.MATERIAL, 'priority': TaskPriority.MEDIUM, 'depends_on': [3]},
                {'name': 'Iluminación', 'type': TaskType.LIGHTING, 'priority': TaskPriority.MEDIUM, 'depends_on': [4]},
                {'name': 'Posicionar cámara', 'type': TaskType.CAMERA, 'priority': TaskPriority.LOW, 'depends_on': [5]},
                {'name': 'Renderizar', 'type': TaskType.RENDER, 'priority': TaskPriority.LOW, 'depends_on': [6]},
            ],
            'product_visualization': [
                {'name': 'Importar modelo 3D', 'type': TaskType.IMPORT, 'priority': TaskPriority.CRITICAL},
                {'name': 'Aplicar materiales PBR', 'type': TaskType.MATERIAL, 'priority': TaskPriority.HIGH, 'depends_on': [0]},
                {'name': 'Configurar iluminación HDR', 'type': TaskType.LIGHTING, 'priority': TaskPriority.HIGH, 'depends_on': [1]},
                {'name': 'Posicionar cámara turntable', 'type': TaskType.CAMERA, 'priority': TaskPriority.MEDIUM, 'depends_on': [2]},
                {'name': 'Renderizar múltiples vistas', 'type': TaskType.RENDER, 'priority': TaskPriority.MEDIUM, 'depends_on': [3]},
            ],
            'character_model': [
                {'name': 'Crear armadura (rigging)', 'type': TaskType.CREATE, 'priority': TaskPriority.CRITICAL},
                {'name': 'Aplicar texturas', 'type': TaskType.MATERIAL, 'priority': TaskPriority.HIGH, 'depends_on': [0]},
                {'name': 'Crear pose', 'type': TaskType.TRANSFORM, 'priority': TaskPriority.MEDIUM, 'depends_on': [0]},
                {'name': 'Iluminación para personaje', 'type': TaskType.LIGHTING, 'priority': TaskPriority.MEDIUM, 'depends_on': [2]},
                {'name': 'Renderizar', 'type': TaskType.RENDER, 'priority': TaskPriority.LOW, 'depends_on': [3]},
            ],
        }
    
    def decompose(self, objective: str) -> DecompositionPlan:
        """
        Descompone un objetivo en subtareas.
        
        Args:
            objective: Descripción del objetivo en lenguaje natural
            
        Returns:
            DecompositionPlan con subtareas ordenadas
        """
        # Detectar tipo de objetivo
        objective_lower = objective.lower()
        
        # Clasificar objetivo
        pattern_key = self._classify_objective(objective_lower)
        
        # Obtener patrón
        if pattern_key not in self.decomposition_patterns:
            # Fallback: patrón genérico
            pattern_key = 'generic'
            pattern_tasks = self._generate_generic_decomposition(objective)
        else:
            pattern_tasks = self.decomposition_patterns[pattern_key]
        
        # Crear plan
        plan = DecompositionPlan(objective=objective)
        
        # Convertir patrón a SubTasks
        task_id_map = {}  # map: índice en patrón → id generado
        for idx, task_data in enumerate(pattern_tasks):
            task_id = self._generate_task_id()
            task_id_map[idx] = task_id
            
            # Resolver dependencias
            depends_on_indices = task_data.get('depends_on', [])
            depends_on_ids = [task_id_map[i] for i in depends_on_indices if i in task_id_map]
            
            # Estimar tiempo según tipo
            estimated_time = self._estimate_task_time(task_data['type'])
            
            subtask = SubTask(
                id=task_id,
                name=task_data.get('name', f"Tarea {idx}"),
                description=task_data.get('description', ''),
                task_type=task_data['type'],
                priority=task_data.get('priority', TaskPriority.MEDIUM),
                depends_on=depends_on_ids,
                estimated_time_sec=estimated_time,
                parameters=task_data.get('parameters', {})
            )
            plan.tasks.append(subtask)
        
        # Calcular métricas del plan
        plan.total_estimated_time_sec = sum(t.estimated_time_sec for t in plan.tasks)
        plan.complexity_score = self._calculate_complexity(plan.tasks)
        plan.parallelizable_groups = self._find_parallelizable_groups(plan.tasks)
        
        return plan
    
    def _classify_objective(self, objective: str) -> str:
        """Clasifica objetivo en tipo conocido."""
        keywords = {
            'architectural_scene': ['arquitectonico', 'edificio', 'casa', 'construcción', 'muros', 'interior'],
            'product_visualization': ['producto', 'visualizacion', 'render', 'objeto', 'modelo 3d'],
            'character_model': ['personaje', 'personaje', 'cara', 'cuerpo', 'rigging'],
        }
        
        for pattern_key, kws in keywords.items():
            if any(kw in objective for kw in kws):
                return pattern_key
        
        return 'generic'
    
    def _generate_generic_decomposition(self, objective: str) -> List[Dict[str, Any]]:
        """Genera descomposición genérica para objetivo desconocido."""
        return [
            {'name': 'Preparar escena', 'type': TaskType.CREATE, 'priority': TaskPriority.CRITICAL},
            {'name': 'Crear elementos principales', 'type': TaskType.CREATE, 'priority': TaskPriority.HIGH, 'depends_on': [0]},
            {'name': 'Aplicar detalles', 'type': TaskType.MODIFIER, 'priority': TaskPriority.MEDIUM, 'depends_on': [1]},
            {'name': 'Aplicar materiales', 'type': TaskType.MATERIAL, 'priority': TaskPriority.MEDIUM, 'depends_on': [2]},
            {'name': 'Iluminación', 'type': TaskType.LIGHTING, 'priority': TaskPriority.MEDIUM, 'depends_on': [3]},
            {'name': 'Renderizar', 'type': TaskType.RENDER, 'priority': TaskPriority.LOW, 'depends_on': [4]},
        ]
    
    def _generate_task_id(self) -> str:
        """Genera ID único para tarea."""
        self.task_counter += 1
        return f"task_{self.task_counter:04d}"
    
    def _estimate_task_time(self, task_type: TaskType) -> float:
        """Estima tiempo de ejecución según tipo."""
        time_estimates = {
            TaskType.CREATE: 15.0,
            TaskType.TRANSFORM: 5.0,
            TaskType.MATERIAL: 20.0,
            TaskType.LIGHTING: 25.0,
            TaskType.CAMERA: 8.0,
            TaskType.RENDER: 120.0,
            TaskType.IMPORT: 10.0,
            TaskType.EXPORT: 10.0,
            TaskType.MODIFIER: 10.0,
            TaskType.COMPOUND: 60.0,
        }
        return time_estimates.get(task_type, 10.0)
    
    def _calculate_complexity(self, tasks: List[SubTask]) -> float:
        """Calcula complejidad del plan (0-1)."""
        num_tasks = len(tasks)
        max_depth = self._calculate_max_dependency_depth(tasks)
        
        # Fórmula: complejidad = (tareas + profundidad*2) / 20
        complexity = min(1.0, (num_tasks + max_depth * 2) / 20.0)
        return complexity
    
    def _calculate_max_dependency_depth(self, tasks: List[SubTask]) -> int:
        """Calcula profundidad máxima de dependencias."""
        task_map = {t.id: t for t in tasks}
        depths = {}
        
        def get_depth(task_id: str) -> int:
            if task_id in depths:
                return depths[task_id]
            
            task = task_map.get(task_id)
            if not task or not task.depends_on:
                depths[task_id] = 0
                return 0
            
            max_dep_depth = max(get_depth(dep_id) for dep_id in task.depends_on)
            depths[task_id] = max_dep_depth + 1
            return depths[task_id]
        
        return max((get_depth(t.id) for t in tasks), default=0)
    
    def _find_parallelizable_groups(self, tasks: List[SubTask]) -> List[List[str]]:
        """Encuentra grupos de tareas que pueden ejecutarse en paralelo."""
        groups = []
        executed = set()
        
        while len(executed) < len(tasks):
            # Encontrar tareas cuyas dependencias están todas ejecutadas
            ready = [t.id for t in tasks 
                    if t.id not in executed and all(d in executed for d in t.depends_on)]
            
            if ready:
                groups.append(ready)
                executed.update(ready)
            else:
                break  # Debe haber ciclo (no debería pasar)
        
        return groups
    
    def save_plan(self, plan: DecompositionPlan, filepath: str):
        """Guarda plan en archivo JSON."""
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(plan.to_dict(), f, indent=2, ensure_ascii=False)
    
    def load_plan(self, filepath: str) -> DecompositionPlan:
        """Carga plan desde archivo JSON."""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Reconstruir plan
        tasks = []
        for task_data in data['tasks']:
            task = SubTask(
                id=task_data['id'],
                name=task_data['name'],
                description=task_data['description'],
                task_type=TaskType(task_data['task_type']),
                priority=TaskPriority(task_data['priority']),
                depends_on=task_data['depends_on'],
                estimated_time_sec=task_data['estimated_time_sec'],
                parameters=task_data['parameters'],
                is_completed=task_data['is_completed'],
                result=task_data['result'],
                error=task_data['error']
            )
            tasks.append(task)
        
        plan = DecompositionPlan(
            objective=data['objective'],
            plan_id=data['plan_id'],
            tasks=tasks,
            total_estimated_time_sec=data['total_estimated_time_sec'],
            complexity_score=data['complexity_score'],
            parallelizable_groups=data['parallelizable_groups'],
            created_at=data['created_at'],
            status=data['status']
        )
        
        return plan
