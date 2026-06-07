"""
C3 - Task Scheduler & Executor
===============================

Ejecuta planes de descomposición de tareas siguiendo dependencias.

FLUJO:
  1. Recibe DecompositionPlan desde TaskDecomposer
  2. Construye DependencyGraph
  3. Valida acyclicity
  4. Calcula camino crítico
  5. Ejecuta tareas en paralelo siguiendo dependencias
  6. Integra con IntentRouter para ejecutar cada subtarea
  7. Almacena resultados y aprende (C2)

RESPONSABILIDADES:
  - Ejecución secuencial/paralela
  - Manejo de errores y reintentos
  - Reporte de progreso
  - Integración C1 (evaluación)
  - Integración C2 (almacenamiento)
"""

import asyncio
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field, asdict
from datetime import datetime
import json
from pathlib import Path
from enum import Enum
import time
import sys
from pathlib import Path

# Agregar directorio de cognición al path
sys.path.insert(0, str(Path(__file__).parent))

from c3_task_decomposer import DecompositionPlan, SubTask, TaskType
from c3_dependency_graph import DependencyGraph


class ExecutionStatus(Enum):
    """Estados de ejecución"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class TaskExecutionRecord:
    """Registro de ejecución de una tarea."""
    task_id: str
    task_name: str
    status: ExecutionStatus
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    duration_sec: float = 0.0
    result: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None
    retries: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'task_id': self.task_id,
            'task_name': self.task_name,
            'status': self.status.value,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'duration_sec': self.duration_sec,
            'result': self.result,
            'error': self.error,
            'retries': self.retries,
        }


@dataclass
class ExecutionReport:
    """Reporte de ejecución de un plan completo."""
    plan_id: str
    objective: str
    start_time: str
    end_time: Optional[str] = None
    total_duration_sec: float = 0.0
    overall_status: ExecutionStatus = ExecutionStatus.PENDING
    task_records: List[TaskExecutionRecord] = field(default_factory=list)
    tasks_completed: int = 0
    tasks_failed: int = 0
    tasks_skipped: int = 0
    critical_path: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'plan_id': self.plan_id,
            'objective': self.objective,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'total_duration_sec': self.total_duration_sec,
            'overall_status': self.overall_status.value,
            'task_records': [r.to_dict() for r in self.task_records],
            'tasks_completed': self.tasks_completed,
            'tasks_failed': self.tasks_failed,
            'tasks_skipped': self.tasks_skipped,
            'critical_path': self.critical_path,
        }


class TaskScheduler:
    """Ejecuta planes de tareas."""
    
    def __init__(self, intent_router: Optional[Any] = None, max_retries: int = 2):
        """
        Inicializa scheduler.
        
        Args:
            intent_router: Router que ejecuta intenciones (handler de comandos)
            max_retries: Máximo reintentos por tarea
        """
        self.intent_router = intent_router
        self.max_retries = max_retries
        self.execution_reports: Dict[str, ExecutionReport] = {}
    
    def execute_plan(self, plan: DecompositionPlan, dry_run: bool = False) -> ExecutionReport:
        """
        Ejecuta plan completo.
        
        Args:
            plan: DecompositionPlan a ejecutar
            dry_run: Si True, solo valida sin ejecutar
            
        Returns:
            ExecutionReport con resultados
        """
        report = ExecutionReport(
            plan_id=plan.plan_id,
            objective=plan.objective,
            start_time=datetime.now().isoformat()
        )
        
        # Construir grafo
        graph = DependencyGraph()
        for task in plan.tasks:
            graph.add_task(
                task_id=task.id,
                task_name=task.name,
                duration=task.estimated_time_sec,
                dependencies=task.depends_on
            )
        
        # Validar
        is_valid, cycle = graph.validate()
        if not is_valid:
            report.overall_status = ExecutionStatus.FAILED
            report.end_time = datetime.now().isoformat()
            report.task_records.append(TaskExecutionRecord(
                task_id="validation",
                task_name="Graph Validation",
                status=ExecutionStatus.FAILED,
                error=f"Ciclo detectado: {' -> '.join(cycle)}"
            ))
            return report
        
        # Calcular camino crítico
        critical_path, total_duration = graph.calculate_critical_path()
        report.critical_path = critical_path
        
        if dry_run:
            report.overall_status = ExecutionStatus.COMPLETED
            report.end_time = datetime.now().isoformat()
            return report
        
        # Ejecutar en orden topológico
        task_map = {t.id: t for t in plan.tasks}
        execution_results = {}
        
        # Obtener orden de ejecución con paralelización
        execution_levels = graph.get_execution_order()
        
        for level, task_ids in execution_levels:
            # Ejecutar tareas en paralelo (si el router lo soporta)
            level_results = {}
            
            for task_id in task_ids:
                task = task_map.get(task_id)
                if not task:
                    continue
                
                record = self._execute_task(task, execution_results)
                level_results[task_id] = record
                report.task_records.append(record)
                
                if record.status == ExecutionStatus.COMPLETED:
                    report.tasks_completed += 1
                elif record.status == ExecutionStatus.FAILED:
                    report.tasks_failed += 1
                else:
                    report.tasks_skipped += 1
            
            execution_results.update(level_results)
        
        # Finalizar reporte
        report.end_time = datetime.now().isoformat()
        report.total_duration_sec = time.time() - time.time() + sum(
            r.duration_sec for r in report.task_records
        )
        
        # Determinar estado general
        if report.tasks_failed > 0:
            report.overall_status = ExecutionStatus.FAILED
        elif report.tasks_completed > 0:
            report.overall_status = ExecutionStatus.COMPLETED
        else:
            report.overall_status = ExecutionStatus.SKIPPED
        
        self.execution_reports[plan.plan_id] = report
        return report
    
    def _execute_task(
        self, 
        task: SubTask, 
        execution_results: Dict[str, TaskExecutionRecord]
    ) -> TaskExecutionRecord:
        """
        Ejecuta una tarea individual.
        
        Args:
            task: SubTask a ejecutar
            execution_results: Resultados de tareas previas
            
        Returns:
            TaskExecutionRecord con resultado
        """
        record = TaskExecutionRecord(
            task_id=task.id,
            task_name=task.name,
            status=ExecutionStatus.PENDING,
            start_time=datetime.now().isoformat()
        )
        
        # Verificar dependencias
        failed_dependencies = [
            dep_id for dep_id in task.depends_on
            if dep_id in execution_results
            and execution_results[dep_id].status != ExecutionStatus.COMPLETED
        ]
        
        if failed_dependencies:
            record.status = ExecutionStatus.SKIPPED
            record.error = f"Dependencias fallidas: {failed_dependencies}"
            record.end_time = datetime.now().isoformat()
            return record
        
        # Intentar ejecución con reintentos
        last_error = None
        
        for attempt in range(self.max_retries + 1):
            try:
                # Ejecutar tarea vía intent_router si disponible
                if self.intent_router:
                    result = self.intent_router.route_intent(
                        command=task.name.lower(),
                        parameters=task.parameters
                    )
                    record.result = result
                    record.status = ExecutionStatus.COMPLETED
                    break
                else:
                    # Modo simulación (mock)
                    record.result = {
                        'simulated': True,
                        'task_type': task.task_type.value,
                        'parameters': task.parameters
                    }
                    record.status = ExecutionStatus.COMPLETED
                    break
            
            except Exception as e:
                last_error = str(e)
                record.retries = attempt + 1
                
                if attempt < self.max_retries:
                    time.sleep(0.5 * (attempt + 1))  # Backoff exponencial
                else:
                    record.status = ExecutionStatus.FAILED
                    record.error = f"Error en intento {attempt + 1}: {last_error}"
        
        record.end_time = datetime.now().isoformat()
        record.duration_sec = self._calculate_duration(record.start_time, record.end_time)
        
        return record
    
    def _calculate_duration(self, start_iso: str, end_iso: str) -> float:
        """Calcula duración en segundos entre dos timestamps ISO."""
        try:
            start = datetime.fromisoformat(start_iso)
            end = datetime.fromisoformat(end_iso)
            return (end - start).total_seconds()
        except:
            return 0.0
    
    def save_report(self, report: ExecutionReport, filepath: str):
        """Guarda reporte en archivo."""
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(report.to_dict(), f, indent=2, ensure_ascii=False)
    
    def get_report_summary(self, plan_id: str) -> Dict[str, Any]:
        """Retorna resumen de reporte."""
        report = self.execution_reports.get(plan_id)
        if not report:
            return {}
        
        return {
            'objective': report.objective,
            'status': report.overall_status.value,
            'tasks_completed': report.tasks_completed,
            'tasks_failed': report.tasks_failed,
            'tasks_skipped': report.tasks_skipped,
            'total_tasks': len(report.task_records),
            'total_duration_sec': report.total_duration_sec,
            'success_rate': (
                report.tasks_completed / len(report.task_records)
                if report.task_records else 0
            ),
        }


# ============================================================================
# Integración con C2 (almacenamiento de aprendizajes)
# ============================================================================

def save_decomposition_pattern(
    objective: str,
    plan: DecompositionPlan,
    success: bool,
    c2_memory = None
):
    """
    Guarda patrón de descomposición aprendido en C2.
    
    Args:
        objective: Objetivo original
        plan: Plan que se ejecutó
        success: Si la ejecución fue exitosa
        c2_memory: Referencia a C2 ExperienceMemory (opcional)
    """
    pattern = {
        'objective_template': objective,
        'tasks': [t.to_dict() for t in plan.tasks],
        'parallelizable_groups': plan.parallelizable_groups,
        'complexity_score': plan.complexity_score,
        'success': success,
        'timestamp': datetime.now().isoformat(),
    }
    
    if c2_memory:
        try:
            c2_memory.record_experience(
                objective=f"decompose_task: {objective}",
                evaluation={'success': success, 'complexity': plan.complexity_score},
                metadata=pattern
            )
        except Exception as e:
            print(f"[C3] Warning: No se guardó patrón en C2: {e}")
