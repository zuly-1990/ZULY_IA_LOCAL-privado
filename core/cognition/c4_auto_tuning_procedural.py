"""
C4 - Auto-tuning Procedural (Plan C Phase 4)

Módulo de autoajuste procedural que optimiza automáticamente parámetros
mediante un ciclo iterativo: variar → ejecutar → evaluar (C1) → guardar (C2) → converger.

Arquitectura:
  - ParameterOptimizer: Gestiona espacio de parámetros y variaciones
  - IterativeExecutor: Ejecuta procedimientos con diferentes parámetros
  - FeedbackLoop: Integra evaluación C1 y aprendizaje C2
  - ConvergenceChecker: Verifica convergencia y termina loop
  - C4AutoTuningProcedural: Orquestador principal

Flujo:
  1. Usuario define objetivo, parámetros iniciales, bounds
  2. C4 varía parámetro dentro de bounds
  3. Ejecuta procedimiento
  4. C1 evalúa resultado (obtiene score 0-1)
  5. C2 almacena heurística: (param_value, score)
  6. Si mejor → guardar nuevo valor
  7. Iterar hasta convergencia
  8. Retornar parámetro óptimo y heurística
"""

from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Dict, List, Tuple, Optional, Callable, Any
from datetime import datetime
import json
from pathlib import Path


class OptimizationStrategy(Enum):
    """Estrategias de optimización disponibles"""
    GRID_SEARCH = "grid_search"              # Búsqueda en cuadrícula (exhaustiva)
    RANDOM_SEARCH = "random_search"          # Búsqueda aleatoria
    HILL_CLIMBING = "hill_climbing"          # Ascenso de colina (greedy local)
    SIMULATED_ANNEALING = "simulated_annealing"  # Recocido simulado
    GENETIC = "genetic"                      # Algoritmo genético


class ParameterType(Enum):
    """Tipos de parámetros"""
    INT = "int"
    FLOAT = "float"
    BOOL = "bool"
    CHOICE = "choice"


@dataclass
class ParameterBound:
    """Define rango y tipo de un parámetro"""
    name: str
    param_type: ParameterType
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    choices: Optional[List[Any]] = None
    step: float = 1.0
    
    def validate(self) -> bool:
        """Valida que los bounds sean consistentes"""
        if self.param_type in [ParameterType.INT, ParameterType.FLOAT]:
            return self.min_value is not None and self.max_value is not None
        elif self.param_type == ParameterType.CHOICE:
            return self.choices is not None and len(self.choices) > 0
        elif self.param_type == ParameterType.BOOL:
            return True
        return False


@dataclass
class OptimizationStep:
    """Representa un paso en la optimización"""
    step_number: int
    parameter_value: Any
    execution_result: Optional[Dict] = None
    c1_score: Optional[float] = None
    is_improvement: bool = False
    best_so_far: bool = False
    timestamp: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict:
        """Serializa a diccionario"""
        return {
            "step_number": self.step_number,
            "parameter_value": str(self.parameter_value),
            "c1_score": self.c1_score,
            "is_improvement": self.is_improvement,
            "best_so_far": self.best_so_far,
            "timestamp": self.timestamp.isoformat()
        }


@dataclass
class OptimizationResult:
    """Resultado final de la optimización"""
    objective: str
    best_parameter_value: Any
    best_score: float
    total_iterations: int
    converged: bool
    convergence_reason: str  # "max_iterations", "target_reached", "no_improvement"
    history: List[OptimizationStep] = field(default_factory=list)
    strategy: OptimizationStrategy = OptimizationStrategy.HILL_CLIMBING
    execution_time: float = 0.0
    
    def to_dict(self) -> Dict:
        """Serializa a diccionario"""
        return {
            "objective": self.objective,
            "best_parameter_value": str(self.best_parameter_value),
            "best_score": self.best_score,
            "total_iterations": self.total_iterations,
            "converged": self.converged,
            "convergence_reason": self.convergence_reason,
            "strategy": self.strategy.value,
            "execution_time": self.execution_time,
            "history": [step.to_dict() for step in self.history]
        }


class ParameterOptimizer:
    """Gestiona el espacio de parámetros y variaciones"""
    
    def __init__(self, bounds: Dict[str, ParameterBound]):
        """
        Inicializa optimizador con bounds de parámetros
        
        Args:
            bounds: Dict {param_name: ParameterBound}
        """
        self.bounds = bounds
        self._validate_bounds()
    
    def _validate_bounds(self):
        """Valida que todos los bounds sean válidos"""
        for name, bound in self.bounds.items():
            if not bound.validate():
                raise ValueError(f"Bound inválido para {name}: {bound}")
    
    def generate_initial_value(self, param_name: str) -> Any:
        """Genera valor inicial (centro del rango)"""
        bound = self.bounds[param_name]
        
        if bound.param_type == ParameterType.INT:
            return int((bound.min_value + bound.max_value) / 2)
        elif bound.param_type == ParameterType.FLOAT:
            return (bound.min_value + bound.max_value) / 2.0
        elif bound.param_type == ParameterType.BOOL:
            return True
        elif bound.param_type == ParameterType.CHOICE:
            return bound.choices[0]
        return None
    
    def get_neighbors(self, param_name: str, current_value: Any) -> List[Any]:
        """Obtiene valores vecinos (para hill climbing)"""
        bound = self.bounds[param_name]
        neighbors = []
        
        if bound.param_type == ParameterType.INT:
            current = int(current_value)
            # Vecinos: valor - step, valor + step
            lower = max(int(bound.min_value), current - int(bound.step))
            upper = min(int(bound.max_value), current + int(bound.step))
            if lower != current:
                neighbors.append(lower)
            if upper != current:
                neighbors.append(upper)
        
        elif bound.param_type == ParameterType.FLOAT:
            current = float(current_value)
            lower = max(bound.min_value, current - bound.step)
            upper = min(bound.max_value, current + bound.step)
            if lower != current:
                neighbors.append(lower)
            if upper != current:
                neighbors.append(upper)
        
        elif bound.param_type == ParameterType.BOOL:
            other = not current_value
            neighbors.append(other)
        
        elif bound.param_type == ParameterType.CHOICE:
            # Todos los choices son vecinos
            for choice in bound.choices:
                if choice != current_value:
                    neighbors.append(choice)
        
        return neighbors
    
    def is_valid(self, param_name: str, value: Any) -> bool:
        """Verifica que el valor esté dentro de bounds"""
        bound = self.bounds[param_name]
        
        if bound.param_type in [ParameterType.INT, ParameterType.FLOAT]:
            return bound.min_value <= value <= bound.max_value
        elif bound.param_type == ParameterType.CHOICE:
            return value in bound.choices
        elif bound.param_type == ParameterType.BOOL:
            return isinstance(value, bool)
        
        return False


class IterativeExecutor:
    """Ejecuta procedimientos con diferentes parámetros"""
    
    def __init__(self, procedure: Callable, max_iterations: int = 50):
        """
        Inicializa ejecutor
        
        Args:
            procedure: Función a ejecutar (toma param_value, retorna dict)
            max_iterations: Máximo de iteraciones permitidas
        """
        self.procedure = procedure
        self.max_iterations = max_iterations
    
    def execute_with_parameter(self, param_value: Any) -> Dict:
        """
        Ejecuta procedimiento con parámetro específico
        
        Args:
            param_value: Valor del parámetro a usar
            
        Returns:
            Dict con resultado de ejecución
        """
        try:
            result = self.procedure(param_value)
            return {
                "success": True,
                "result": result,
                "param_used": param_value
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "param_used": param_value
            }


class FeedbackLoop:
    """Integra evaluación C1 y aprendizaje C2"""
    
    def __init__(self, evaluator_c1: Optional[Callable] = None,
                 memory_c2: Optional[Dict] = None):
        """
        Inicializa feedback loop
        
        Args:
            evaluator_c1: Función que evalúa resultados (retorna score 0-1)
            memory_c2: Referencia a memoria C2 para guardar heurísticas
        """
        self.evaluator_c1 = evaluator_c1
        self.memory_c2 = memory_c2 if memory_c2 is not None else {}
    
    def evaluate_execution(self, exec_result: Dict) -> float:
        """
        Evalúa resultado de ejecución
        
        Args:
            exec_result: Resultado de IterativeExecutor.execute_with_parameter()
            
        Returns:
            Score 0-1 (0=peor, 1=mejor)
        """
        if not exec_result["success"]:
            return 0.0
        
        if self.evaluator_c1:
            # Usa evaluador C1 si está disponible
            try:
                score = self.evaluator_c1(exec_result)
                return max(0.0, min(1.0, score))  # Clamp a [0, 1]
            except Exception:
                return 0.5  # Valor neutral si falla
        
        # Fallback: considera éxito como 0.8, fallo como 0.0
        return 0.8 if exec_result.get("success") else 0.0
    
    def save_heuristic(self, objective: str, param_value: Any, score: float):
        """
        Guarda heurística en C2
        
        Args:
            objective: Nombre del objetivo
            param_value: Valor del parámetro
            score: Score obtenido (0-1)
        """
        if objective not in self.memory_c2:
            self.memory_c2[objective] = []
        
        self.memory_c2[objective].append({
            "param_value": param_value,
            "score": score,
            "timestamp": datetime.now().isoformat()
        })


class ConvergenceChecker:
    """Verifica convergencia y condiciones de parada"""
    
    def __init__(self, target_score: float = 0.95,
                 max_iterations: int = 50,
                 no_improvement_limit: int = 5):
        """
        Inicializa checker
        
        Args:
            target_score: Score objetivo (0-1)
            max_iterations: Máximo de iteraciones
            no_improvement_limit: Iteraciones sin mejora antes de parar
        """
        self.target_score = target_score
        self.max_iterations = max_iterations
        self.no_improvement_limit = no_improvement_limit
    
    def should_continue(self, iteration: int, best_score: float,
                       no_improvement_count: int) -> Tuple[bool, str]:
        """
        Determina si debe continuar optimizando
        
        Returns:
            (should_continue, reason)
        """
        if best_score >= self.target_score:
            return False, "target_reached"
        
        if iteration >= self.max_iterations:
            return False, "max_iterations"
        
        if no_improvement_count >= self.no_improvement_limit:
            return False, "no_improvement"
        
        return True, "continue"


class C4AutoTuningProcedural:
    """Orquestador principal de auto-tuning procedural"""
    
    def __init__(self, silent_mode: bool = True):
        """Inicializa C4 en modo silencioso por defecto (Fase 4)"""
        self.optimization_history: Dict[str, OptimizationResult] = {}
        self.heuristics_cache: Dict[str, Any] = {}
        self.silent_mode = silent_mode
    
    def optimize(self,
                objective: str,
                procedure: Callable,
                param_bounds: Dict[str, ParameterBound],
                initial_value: Optional[Any] = None,
                c1_evaluator: Optional[Callable] = None,
                c2_memory: Optional[Dict] = None,
                strategy: OptimizationStrategy = OptimizationStrategy.HILL_CLIMBING,
                target_score: float = 0.95,
                max_iterations: int = 50,
                no_improvement_limit: int = 5) -> OptimizationResult:
        """
        Ejecuta ciclo de optimización
        
        Args:
            objective: Nombre del objetivo a optimizar
            procedure: Función a ejecutar (param_value) -> result
            param_bounds: Bounds de parámetros
            initial_value: Valor inicial (si None, usa centro del rango)
            c1_evaluator: Evaluador C1 opcional
            c2_memory: Memoria C2 opcional
            strategy: Estrategia de optimización
            target_score: Score objetivo
            max_iterations: Máximo de iteraciones
            no_improvement_limit: Paradas sin mejora
            
        Returns:
            OptimizationResult con resultado final
        """
        import time
        start_time = time.time()
        
        # Inicializar componentes
        optimizer = ParameterOptimizer(param_bounds)
        executor = IterativeExecutor(procedure, max_iterations)
        feedback = FeedbackLoop(c1_evaluator, c2_memory)
        checker = ConvergenceChecker(target_score, max_iterations,
                                    no_improvement_limit)
        
        # Obtener parámetro inicial
        if initial_value is None:
            param_name = list(param_bounds.keys())[0]
            current_value = optimizer.generate_initial_value(param_name)
        else:
            current_value = initial_value
        
        # Variables de seguimiento
        best_value = current_value
        best_score = 0.0
        no_improvement_count = 0
        history: List[OptimizationStep] = []
        iteration = 0
        param_name = list(param_bounds.keys())[0]
        convergence_reason = "completed"  # Default reason
        
        # Ciclo principal
        while iteration < max_iterations:
            iteration += 1
            
            # Ejecutar con parámetro actual
            exec_result = executor.execute_with_parameter(current_value)
            
            # Evaluar resultado
            score = feedback.evaluate_execution(exec_result)
            
            # Guardar heurística en C2
            feedback.save_heuristic(objective, current_value, score)
            
            # Determinar si es mejora
            is_improvement = score > best_score
            
            if is_improvement:
                best_value = current_value
                best_score = score
                no_improvement_count = 0
            else:
                no_improvement_count += 1
            
            # Guardar en historial
            step = OptimizationStep(
                step_number=iteration,
                parameter_value=current_value,
                execution_result=exec_result,
                c1_score=score,
                is_improvement=is_improvement,
                best_so_far=(current_value == best_value)
            )
            history.append(step)
            
            # FASE 4: Notificación Silenciosa (ZULY PRO)
            if not self.silent_mode:
                log_info(f"   [C4] Iteración {iteration}: Score {score:.2f} (Mejor: {best_score:.2f})")
            
            # Verificar convergencia
            should_continue, reason = checker.should_continue(
                iteration, best_score, no_improvement_count)
            
            if not should_continue:
                convergence_reason = reason
                break
            
            # Siguiente parámetro (según estrategia)
            if strategy == OptimizationStrategy.HILL_CLIMBING:
                neighbors = optimizer.get_neighbors(param_name, current_value)
                if neighbors:
                    # Evaluación greedy: elige mejor vecino
                    best_neighbor_score = score
                    best_neighbor_value = current_value
                    
                    for neighbor in neighbors:
                        neighbor_exec = executor.execute_with_parameter(neighbor)
                        neighbor_score = feedback.evaluate_execution(neighbor_exec)
                        
                        if neighbor_score > best_neighbor_score:
                            best_neighbor_score = neighbor_score
                            best_neighbor_value = neighbor
                    
                    current_value = best_neighbor_value
                else:
                    convergence_reason = "no_neighbors"
                    break
            
            elif strategy == OptimizationStrategy.RANDOM_SEARCH:
                import random
                bound = param_bounds[param_name]
                if bound.param_type == ParameterType.INT:
                    current_value = random.randint(
                        int(bound.min_value), int(bound.max_value))
                elif bound.param_type == ParameterType.FLOAT:
                    current_value = random.uniform(
                        bound.min_value, bound.max_value)
                elif bound.param_type == ParameterType.CHOICE:
                    current_value = random.choice(bound.choices)
        
        # Construir resultado
        execution_time = time.time() - start_time
        result = OptimizationResult(
            objective=objective,
            best_parameter_value=best_value,
            best_score=best_score,
            total_iterations=iteration,
            converged=(convergence_reason in ["target_reached", "no_improvement"]),
            convergence_reason=convergence_reason,
            history=history,
            strategy=strategy,
            execution_time=execution_time
        )
        
        # Guardar en historial
        self.optimization_history[objective] = result
        
        return result
    
    def export_result(self, result: OptimizationResult, filepath: str) -> bool:
        """
        Exporta resultado de optimización a JSON
        
        Args:
            result: OptimizationResult a exportar
            filepath: Ruta del archivo
            
        Returns:
            bool: True si éxito
        """
        try:
            path = Path(filepath)
            path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(result.to_dict(), f, indent=2, ensure_ascii=False)
            
            return True
        except Exception:
            return False
    
    def get_summary(self, result: OptimizationResult) -> Dict:
        """
        Genera resumen de resultado
        
        Args:
            result: OptimizationResult
            
        Returns:
            Dict con estadísticas
        """
        improvements = sum(1 for step in result.history if step.is_improvement)
        avg_score = sum(step.c1_score for step in result.history) / len(result.history)
        
        return {
            "objective": result.objective,
            "best_parameter": result.best_parameter_value,
            "best_score": result.best_score,
            "iterations": result.total_iterations,
            "converged": result.converged,
            "reason": result.convergence_reason,
            "strategy": result.strategy.value,
            "total_improvements": improvements,
            "average_score": avg_score,
            "execution_time": f"{result.execution_time:.2f}s"
        }
