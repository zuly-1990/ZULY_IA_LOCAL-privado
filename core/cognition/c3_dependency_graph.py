"""
C3 - Dependency Graph
=====================

Maneja el grafo dirigido de dependencias entre tareas.
Permite análisis topológico, detección de ciclos, y visualización.

OPERACIONES:
  - Validar acyclicity (sin ciclos)
  - Ordenamiento topológico
  - Encontrar tareas críticas (camino crítico)
  - Calcular slack/holgura
  - Visualizar como DOT (Graphviz)
"""

from typing import Dict, List, Set, Tuple, Optional
from dataclasses import dataclass, field
import json
from pathlib import Path


@dataclass
class TaskNode:
    """Nodo en el grafo de dependencias."""
    task_id: str
    task_name: str
    duration_sec: float
    dependencies: List[str] = field(default_factory=list)
    dependents: List[str] = field(default_factory=list)  # tareas que dependen de esta
    
    # Calculados durante análisis
    earliest_start: float = 0.0
    earliest_finish: float = 0.0
    latest_start: float = 0.0
    latest_finish: float = 0.0
    slack: float = 0.0  # holgura = latest_start - earliest_start
    is_critical: bool = False  # parte del camino crítico


class DependencyGraph:
    """Grafo de dependencias entre tareas."""
    
    def __init__(self):
        """Inicializa grafo vacío."""
        self.nodes: Dict[str, TaskNode] = {}
        self.is_valid = True
        self.cycle_detected = False
    
    def add_task(self, task_id: str, task_name: str, duration: float, dependencies: List[str] = None):
        """Agrega tarea al grafo."""
        dependencies = dependencies or []
        
        node = TaskNode(
            task_id=task_id,
            task_name=task_name,
            duration_sec=duration,
            dependencies=dependencies,
            dependents=[]
        )
        
        self.nodes[task_id] = node
        
        # Actualizar dependents de las dependencias
        for dep_id in dependencies:
            if dep_id in self.nodes:
                self.nodes[dep_id].dependents.append(task_id)
    
    def validate(self) -> Tuple[bool, Optional[List[str]]]:
        """
        Valida el grafo.
        
        Returns:
            (es_válido, ciclo_encontrado)
        """
        # Detectar ciclos usando DFS
        visited = set()
        rec_stack = set()
        cycle = []
        
        def has_cycle_util(node_id: str, path: List[str]) -> bool:
            visited.add(node_id)
            rec_stack.add(node_id)
            path.append(node_id)
            
            node = self.nodes.get(node_id)
            if not node:
                return False
            
            for dep_id in node.dependencies:
                if dep_id not in visited:
                    if has_cycle_util(dep_id, path):
                        return True
                elif dep_id in rec_stack:
                    # Ciclo encontrado
                    cycle_start = path.index(dep_id)
                    nonlocal cycle
                    cycle = path[cycle_start:] + [dep_id]
                    return True
            
            path.pop()
            rec_stack.remove(node_id)
            return False
        
        for node_id in self.nodes:
            if node_id not in visited:
                if has_cycle_util(node_id, []):
                    self.cycle_detected = True
                    self.is_valid = False
                    return False, cycle
        
        self.is_valid = True
        return True, None
    
    def topological_sort(self) -> List[str]:
        """
        Retorna orden topológico de tareas (ejecución correcta).
        
        Returns:
            Lista de task_ids en orden topológico
        """
        if not self.is_valid:
            raise ValueError("Grafo contiene ciclos, no se puede ordenar topológicamente")
        
        visited = set()
        order = []
        
        def dfs(node_id: str):
            visited.add(node_id)
            node = self.nodes[node_id]
            
            for dep_id in node.dependencies:
                if dep_id not in visited:
                    dfs(dep_id)
            
            order.append(node_id)
        
        for node_id in self.nodes:
            if node_id not in visited:
                dfs(node_id)
        
        return order
    
    def calculate_critical_path(self) -> Tuple[List[str], float]:
        """
        Calcula camino crítico (tareas que no pueden atrasarse).
        
        Returns:
            (lista_de_task_ids, duración_total)
        """
        # Forward pass: calcular earliest start/finish
        self._forward_pass()
        
        # Backward pass: calcular latest start/finish
        self._backward_pass()
        
        # Encontrar tareas críticas (slack = 0)
        critical_tasks = [
            node_id for node_id, node in self.nodes.items()
            if abs(node.slack) < 0.001  # floating point tolerance
        ]
        
        # Calcular duración total (finish time del nodo final)
        project_duration = max(
            (node.earliest_finish for node in self.nodes.values()),
            default=0.0
        )
        
        return critical_tasks, project_duration
    
    def _forward_pass(self):
        """Calcula Early Start/Finish para cada tarea."""
        # Ordenar topológicamente
        order = self.topological_sort()
        
        for task_id in order:
            node = self.nodes[task_id]
            
            if not node.dependencies:
                # Sin dependencias: comienza en 0
                node.earliest_start = 0.0
            else:
                # Comienza cuando terminan sus dependencias
                node.earliest_start = max(
                    self.nodes[dep_id].earliest_finish
                    for dep_id in node.dependencies
                )
            
            node.earliest_finish = node.earliest_start + node.duration_sec
    
    def _backward_pass(self):
        """Calcula Late Start/Finish para cada tarea."""
        # Orden inverso topológico
        order = self.topological_sort()[::-1]
        
        # Duración total del proyecto
        project_duration = max(
            (node.earliest_finish for node in self.nodes.values()),
            default=0.0
        )
        
        for task_id in order:
            node = self.nodes[task_id]
            
            if not node.dependents:
                # Sin dependientes: termina en duración total
                node.latest_finish = project_duration
            else:
                # Debe terminar antes de que comiencen sus dependientes
                node.latest_finish = min(
                    self.nodes[dep_id].latest_start
                    for dep_id in node.dependents
                )
            
            node.latest_start = node.latest_finish - node.duration_sec
            
            # Calcular slack (holgura)
            node.slack = node.latest_start - node.earliest_start
            
            # Marcar como crítica si slack ≈ 0
            node.is_critical = abs(node.slack) < 0.001
    
    def get_critical_path_tasks(self) -> List[Dict]:
        """Retorna tareas en el camino crítico con detalles."""
        critical_path, total_duration = self.calculate_critical_path()
        
        return [
            {
                'task_id': node_id,
                'task_name': self.nodes[node_id].task_name,
                'duration': self.nodes[node_id].duration_sec,
                'slack': self.nodes[node_id].slack,
                'earliest_start': self.nodes[node_id].earliest_start,
                'earliest_finish': self.nodes[node_id].earliest_finish,
            }
            for node_id in critical_path
        ]
    
    def to_dot(self, filepath: str = None) -> str:
        """
        Exporta grafo como Graphviz DOT.
        
        Args:
            filepath: Si se proporciona, guarda en archivo
            
        Returns:
            String DOT
        """
        dot_lines = ['digraph TaskDependencies {']
        dot_lines.append('  rankdir=LR;')
        dot_lines.append('  node [shape=box];')
        
        # Nodos
        for node_id, node in self.nodes.items():
            label = f"{node.task_name}\\n({node.duration_sec}s)"
            color = "red" if node.is_critical else "lightblue"
            dot_lines.append(
                f'  "{node_id}" [label="{label}", style=filled, fillcolor={color}];'
            )
        
        # Aristas (dependencias)
        for node_id, node in self.nodes.items():
            for dep_id in node.dependencies:
                dot_lines.append(f'  "{dep_id}" -> "{node_id}";')
        
        dot_lines.append('}')
        
        dot_content = '\n'.join(dot_lines)
        
        if filepath:
            Path(filepath).write_text(dot_content, encoding='utf-8')
        
        return dot_content
    
    def to_json(self) -> Dict:
        """Exporta grafo como JSON."""
        return {
            'nodes': {
                node_id: {
                    'task_name': node.task_name,
                    'duration_sec': node.duration_sec,
                    'dependencies': node.dependencies,
                    'dependents': node.dependents,
                    'earliest_start': node.earliest_start,
                    'earliest_finish': node.earliest_finish,
                    'latest_start': node.latest_start,
                    'latest_finish': node.latest_finish,
                    'slack': node.slack,
                    'is_critical': node.is_critical,
                }
                for node_id, node in self.nodes.items()
            },
            'is_valid': self.is_valid,
            'cycle_detected': self.cycle_detected,
        }
    
    def get_execution_order(self) -> List[Tuple[int, List[str]]]:
        """
        Retorna orden de ejecución considerando paralelización.
        
        Returns:
            Lista de (nivel, [task_ids]) para ejecutar en paralelo
        """
        levels = []
        executed = set()
        current_level = 0
        
        while len(executed) < len(self.nodes):
            # Tareas cuyas dependencias están ejecutadas
            ready = [
                task_id for task_id in self.nodes
                if task_id not in executed
                and all(dep in executed for dep in self.nodes[task_id].dependencies)
            ]
            
            if not ready:
                break  # Ciclo
            
            levels.append((current_level, ready))
            executed.update(ready)
            current_level += 1
        
        return levels
    
    def get_bottleneck_tasks(self) -> List[Dict]:
        """Identifica tareas que son cuello de botella (muchos dependientes)."""
        bottlenecks = []
        
        for node_id, node in self.nodes.items():
            num_dependents = len(node.dependents)
            if num_dependents >= 2:  # Al menos 2 tareas dependen de esta
                bottlenecks.append({
                    'task_id': node_id,
                    'task_name': node.task_name,
                    'num_dependents': num_dependents,
                    'depended_by': node.dependents,
                })
        
        return sorted(bottlenecks, key=lambda x: x['num_dependents'], reverse=True)
