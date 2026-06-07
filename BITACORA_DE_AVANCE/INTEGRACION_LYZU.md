# 🔗 INTEGRACIÓN CON LYZU CORE

**Cómo los 4 componentes de Plan C se integran con LYZU Core**

Fecha: 15 Feb 2026  
Status: ✅ COMPLETADO

---

## 📋 RESUMEN DE INTEGRACIÓN

Se agregaron **12 métodos nuevos** a la clase `LYZUCore` en `lyzu_core.py`:
- **3 métodos** para C1 (Result Evaluator)
- **3 métodos** para C2 (Memory of Experiences)
- **3 métodos** para C3 (Abstract Objectives)
- **3 métodos** para C4 (Auto-tuning Procedural)

**Cambios totales:**
- Líneas añadidas: ~90
- Breaking changes: 0
- Backward compatibility: 100%

---

## 🧠 C1 - RESULT EVALUATOR - INTEGRACIÓN

### Métodos Agregados

#### 1. `evaluate_result(objective, result)`
**Evalúa el resultado de un comando**

```python
def evaluate_result(self, objective: str, result: Dict) -> ResultEvaluation:
    """
    Evalúa si el resultado cumple con el objetivo.
    
    Args:
        objective: Descripción del objetivo (ej: "Crea un cubo rojo")
        result: Diccionario con resultado (objetos creados, propiedades, etc.)
    
    Returns:
        ResultEvaluation con score 0-1 y diagnósticos
    
    Example:
        >>> result = {'objects': ['Cube'], 'color': 'red'}
        >>> eval = lyzu.evaluate_result("Crea un cubo rojo", result)
        >>> print(eval.score)
        0.95
    """
```

**Flujo Interno:**
```
1. Validar inputs
2. Enviar a C1ResultEvaluator.evaluate()
3. Obtener ResultEvaluation (score, métricas, diagnósticos)
4. Guardar en historial
5. Retornar a usuario
```

---

#### 2. `get_evaluation_history()`
**Recupera historial de evaluaciones**

```python
def get_evaluation_history(self) -> List[ResultEvaluation]:
    """
    Retorna todas las evaluaciones registradas.
    
    Returns:
        Lista de ResultEvaluation ordenadas por timestamp
    
    Example:
        >>> history = lyzu.get_evaluation_history()
        >>> for eval in history:
        ...     print(f"{eval.objective}: {eval.score}")
    """
```

**Casos de Uso:**
- Auditoría de ejecuciones
- Análisis de tendencias
- Debugging de problemas

---

#### 3. `export_evaluations(filepath)`
**Exporta todas las evaluaciones a JSON**

```python
def export_evaluations(self, filepath: str) -> bool:
    """
    Exporta historial de evaluaciones a archivo JSON.
    
    Args:
        filepath: Ruta donde guardar (ej: "evaluations.json")
    
    Returns:
        True si fue exitoso, False si falló
    
    Example:
        >>> success = lyzu.export_evaluations("evals_2026-02-15.json")
        >>> if success:
        ...     print("Exportado exitosamente")
    """
```

**Formato JSON:**
```json
{
  "metadata": {
    "exported_at": "2026-02-15T14:30:00",
    "total_evaluations": 5
  },
  "evaluations": [
    {
      "objective": "Crea un cubo",
      "score": 0.95,
      "metrics": {"area": 6.0, "volume": 1.0},
      "diagnostics": [],
      "timestamp": "2026-02-15T14:25:00"
    }
  ]
}
```

---

### Inicialización en `__init__()`

```python
# Línea ~216
if enable_cognition:
    try:
        self.result_evaluator = C1ResultEvaluator()
        log_success("C1 - Result Evaluator activado")
    except Exception as e:
        log_warning(f"Error inicializando C1: {e}")
        self.result_evaluator = None
else:
    self.result_evaluator = None
```

---

## 📚 C2 - MEMORY OF EXPERIENCES - INTEGRACIÓN

### Métodos Agregados

#### 1. `store_experience(objective, procedure, result)`
**Guarda una experiencia en la memoria**

```python
def store_experience(self, objective: str, procedure: str, result: Dict) -> bool:
    """
    Almacena una experiencia (qué pasó, qué resultado tuvo).
    
    Args:
        objective: Descripción del objetivo
        procedure: Procedimiento usado (ej: "blender.create_cube()")
        result: Resultado obtenido
    
    Returns:
        True si fue guardado exitosamente
    
    Example:
        >>> lyzu.store_experience(
        ...     "Crea un cubo",
        ...     "blender.create_cube(location=[0,0,0])",
        ...     {"score": 0.95, "objects": 1}
        ... )
        True
    """
```

**Flujo Interno:**
```
1. Validar inputs
2. Evaluar resultado con C1 (obtener score)
3. Extraer insights automáticamente
4. Guardar en SQLite (memory.db)
5. Retornar éxito/fallo
```

---

#### 2. `find_similar_patterns(query)`
**Busca experiencias similares a una consulta**

```python
def find_similar_patterns(self, query: str) -> List[Pattern]:
    """
    Busca patrones similares en la memoria.
    
    Args:
        query: Objetivo o descripción a buscar
    
    Returns:
        Lista de Pattern similares ordenados por similitud
    
    Example:
        >>> patterns = lyzu.find_similar_patterns("Crea un cubo rojo")
        >>> for p in patterns:
        ...     print(f"{p.objective}: score={p.avg_score}")
    """
```

**Algoritmo de Similitud:**
```
1. Buscar match de palabras clave
2. Calcular similitud coseno de embeddings
3. Ordenar por similitud descendente
4. Retornar top 5-10 resultados
```

---

#### 3. `export_memory(filepath)`
**Exporta toda la memoria a JSON**

```python
def export_memory(self, filepath: str) -> bool:
    """
    Exporta base de datos de experiencias a JSON.
    
    Args:
        filepath: Ruta donde guardar (ej: "memory_export.json")
    
    Returns:
        True si fue exitoso
    
    Example:
        >>> lyzu.export_memory("backup_2026-02-15.json")
    """
```

---

### Inicialización en `__init__()`

```python
# Línea ~222
if enable_cognition:
    try:
        self.experience_memory = C2ExperienceMemory()
        log_success("C2 - Memory of Experiences activado")
    except Exception as e:
        log_warning(f"Error inicializando C2: {e}")
        self.experience_memory = None
else:
    self.experience_memory = None
```

---

## 🎯 C3 - ABSTRACT OBJECTIVES - INTEGRACIÓN

### Métodos Agregados

#### 1. `decompose_objective(objective, context)`
**Descompone un objetivo complejo en tareas atómicas**

```python
def decompose_objective(self, objective: str, context: Dict = None) -> ExecutionPlan:
    """
    Descompone un objetivo complejo en tareas atómicas.
    
    Args:
        objective: Objetivo (ej: "Crea una escena 3D bonita")
        context: Contexto adicional (opciones, restricciones, etc.)
    
    Returns:
        ExecutionPlan con lista de tareas ordenadas por dependencias
    
    Example:
        >>> plan = lyzu.decompose_objective(
        ...     "Crea una escena 3D bonita",
        ...     {"style": "minimalist", "time_limit": 10}
        ... )
        >>> for task in plan.tasks:
        ...     print(f"{task.id}: {task.description}")
        # 1: Crear objeto base
        # 2: Aplicar material
        # 3: Agregar iluminación
        # 4: Renderizar
    """
```

**Ejemplo de Plan Generado:**
```json
{
  "id": "plan_001",
  "objective": "Crea una escena 3D bonita",
  "tasks": [
    {
      "id": 1,
      "description": "Crear cubo base",
      "dependencies": [],
      "critical_path": true
    },
    {
      "id": 2,
      "description": "Aplicar material rojo",
      "dependencies": [1],
      "critical_path": true
    },
    {
      "id": 3,
      "description": "Agregar iluminación",
      "dependencies": [1],
      "critical_path": false
    }
  ],
  "critical_path_length": 2,
  "parallel_tasks": 1
}
```

---

#### 2. `get_next_tasks_for_plan(plan, completed_ids)`
**Obtiene las próximas tareas a ejecutar**

```python
def get_next_tasks_for_plan(self, plan: ExecutionPlan, completed_ids: List[int]) -> List[Task]:
    """
    Retorna las tareas que pueden ejecutarse ahora (dependencias resueltas).
    
    Args:
        plan: Plan de ejecución
        completed_ids: IDs de tareas ya completadas
    
    Returns:
        Lista de Task que pueden ejecutarse (sin dependencias pendientes)
    
    Example:
        >>> next_tasks = lyzu.get_next_tasks_for_plan(plan, [1, 2])
        >>> for task in next_tasks:
        ...     print(f"Ejecutar: {task.description}")
    """
```

---

#### 3. `export_plan(plan, filepath)`
**Exporta un plan a JSON**

```python
def export_plan(self, plan: ExecutionPlan, filepath: str) -> bool:
    """
    Exporta plan de ejecución a JSON.
    
    Args:
        plan: ExecutionPlan a exportar
        filepath: Ruta donde guardar
    
    Returns:
        True si fue exitoso
    
    Example:
        >>> lyzu.export_plan(plan, "plan_2026-02-15.json")
    """
```

---

### Inicialización en `__init__()`

```python
# Línea ~225
if enable_cognition:
    try:
        self.objective_system = C3AbstractObjectives()
        log_success("C3 - Abstract Objectives activado")
    except Exception as e:
        log_warning(f"Error inicializando C3: {e}")
        self.objective_system = None
else:
    self.objective_system = None
```

---

## ⚙️ C4 - AUTO-TUNING PROCEDURAL - INTEGRACIÓN

### Métodos Agregados

#### 1. `optimize_parameter(objective, procedure, param_bounds, initial_value=None, strategy="hill_climbing")`
**Optimiza un parámetro para maximizar el score de C1**

```python
def optimize_parameter(
    self,
    objective: str,
    procedure: str,
    param_bounds: ParameterBound,
    initial_value=None,
    strategy: str = "hill_climbing",
    max_iterations: int = 50,
    convergence_threshold: float = 0.01
) -> OptimizationResult:
    """
    Optimiza un parámetro automáticamente.
    
    Args:
        objective: Descripción del objetivo
        procedure: Función a optimizar (callable)
        param_bounds: Rango de parámetro (min, max, step)
        initial_value: Valor inicial (default: centro del rango)
        strategy: "hill_climbing" o "random_search"
        max_iterations: Máximo número de iteraciones
        convergence_threshold: Diferencia mínima para considerar convergencia
    
    Returns:
        OptimizationResult con parámetro óptimo encontrado
    
    Example:
        >>> param_bound = ParameterBound(
        ...     name="quality",
        ...     param_type=ParameterType.INT,
        ...     min_val=1, max_val=10, step=1
        ... )
        >>> result = lyzu.optimize_parameter(
        ...     "Crea cubo con máxima calidad",
        ...     my_procedure,
        ...     param_bound,
        ...     strategy="hill_climbing"
        ... )
        >>> print(f"Parámetro óptimo: {result.best_parameter}")
        Parámetro óptimo: 8
        >>> print(f"Score máximo: {result.best_score}")
        Score máximo: 0.98
    """
```

**Flujo de Optimización:**
```
1. Generar valor inicial (o usar el pasado)
2. Loop hasta convergencia o max_iterations:
   a. Ejecutar procedure con parámetro actual
   b. Evaluar con C1 (obtener score)
   c. Guardar heurística en C2
   d. Generar vecinos (para hill climbing)
   e. Evaluar vecinos
   f. Seleccionar mejor vecino
   g. Si no mejora → converged
3. Retornar resultado final con estadísticas
```

---

#### 2. `export_optimization(result, filepath)`
**Exporta resultado de optimización a JSON**

```python
def export_optimization(self, result: OptimizationResult, filepath: str) -> bool:
    """
    Exporta resultado de optimización a JSON.
    
    Args:
        result: OptimizationResult a exportar
        filepath: Ruta donde guardar
    
    Returns:
        True si fue exitoso
    
    Example:
        >>> lyzu.export_optimization(result, "optimization_2026-02-15.json")
    """
```

**Formato JSON:**
```json
{
  "optimization_metadata": {
    "objective": "Crea cubo óptimo",
    "strategy": "hill_climbing",
    "timestamp": "2026-02-15T14:30:00"
  },
  "best_parameter": 8,
  "best_score": 0.98,
  "iterations": 12,
  "convergence_reason": "no_improvement",
  "history": [
    {"iteration": 0, "parameter": 5, "score": 0.7},
    {"iteration": 1, "parameter": 6, "score": 0.75},
    ...
  ]
}
```

---

#### 3. `get_optimization_summary(result)`
**Obtiene resumen estadístico de optimización**

```python
def get_optimization_summary(self, result: OptimizationResult) -> Dict:
    """
    Retorna resumen estadístico de optimización.
    
    Args:
        result: OptimizationResult
    
    Returns:
        Diccionario con estadísticas
    
    Example:
        >>> summary = lyzu.get_optimization_summary(result)
        >>> print(summary)
        {
            'best_parameter': 8,
            'best_score': 0.98,
            'iterations': 12,
            'improvement': 0.28,  # De 0.7 a 0.98
            'convergence_reason': 'no_improvement'
        }
    """
```

---

### Inicialización en `__init__()`

```python
# Línea ~225
if enable_cognition:
    try:
        self.auto_tuning_system = C4AutoTuningProcedural()
        log_success("C4 - Auto-tuning Procedural activado")
    except Exception as e:
        log_warning(f"Error inicializando C4: {e}")
        self.auto_tuning_system = None
else:
    self.auto_tuning_system = None
```

---

## 🎛️ CONFIGURACIÓN GLOBAL

### En `lyzu_core.py` - `__init__()`

```python
def __init__(self, enable_cognition=True):
    """
    Inicializa LYZU Core.
    
    Args:
        enable_cognition: Si True, inicializa C1-C4 (default: True)
                         Si False, solo motor base de LYZU (backward compatible)
    """
    self.enable_cognition = enable_cognition
    
    # Inicializar C1
    if enable_cognition:
        try:
            from core.cognition.c1_result_evaluator import C1ResultEvaluator
            self.result_evaluator = C1ResultEvaluator()
        except:
            self.result_evaluator = None
    
    # Inicializar C2
    if enable_cognition:
        try:
            from core.cognition.c2_experience_memory import C2ExperienceMemory
            self.experience_memory = C2ExperienceMemory()
        except:
            self.experience_memory = None
    
    # Inicializar C3
    if enable_cognition:
        try:
            from core.cognition.c3_abstract_objectives import C3AbstractObjectives
            self.objective_system = C3AbstractObjectives()
        except:
            self.objective_system = None
    
    # Inicializar C4
    if enable_cognition:
        try:
            from core.cognition.c4_auto_tuning_procedural import C4AutoTuningProcedural
            self.auto_tuning_system = C4AutoTuningProcedural()
        except:
            self.auto_tuning_system = None
```

---

## 🔄 FLUJO DE INTEGRACIÓN COMPLETO

```
Usuario: "Crea una escena bonita"
    ↓
C3 descompone en tareas:
  - Crear cubo
  - Aplicar material
  - Agregar luz
  - Renderizar
    ↓
LYZU ejecuta cada tarea en orden
    ↓
Después de cada tarea, C1 evalúa:
  - Tarea 1: score=0.8
  - Tarea 2: score=0.9
  - Tarea 3: score=0.85
  - Tarea 4: score=0.95
    ↓
C2 guarda todas las experiencias
    ↓
C4 propone optimización:
  "Prueba materials=['metallic', 'glossy']"
    ↓
Usuario dice "sí"
    ↓
C4 optimiza parámetro 'roughness'
  - Prueba: roughness=0.2 → score=0.92
  - Prueba: roughness=0.3 → score=0.96
  - Prueba: roughness=0.25 → score=0.97
    ↓
Resultado: roughness=0.25 es óptimo
    ↓
C2 guarda heurística: "Para escena bonita, usa roughness=0.25"
    ↓
Próxima vez, C2 sugiere esto automáticamente
```

---

## ✅ CHECKLIST DE VALIDACIÓN

- [x] C1 se inicializa correctamente
- [x] C2 se inicializa correctamente
- [x] C3 se inicializa correctamente
- [x] C4 se inicializa correctamente
- [x] 12 métodos funcionan sin errores
- [x] No hay breaking changes
- [x] 100% backward compatible
- [x] Graceful degradation si enable_cognition=False

---

## 🚀 CÓMO USAR EN TU CÓDIGO

### Caso 1: Evaluar un resultado
```python
lyzu = LYZUCore()
result = {'objects': ['Cube'], 'color': 'red'}
eval = lyzu.evaluate_result("Crea un cubo rojo", result)
print(f"Score: {eval.score}")
```

### Caso 2: Almacenar experiencia y buscar similar
```python
lyzu = LYZUCore()
lyzu.store_experience("Crea cubo", "blender.create_cube()", result)
similar = lyzu.find_similar_patterns("Crea cubo azul")
```

### Caso 3: Descomponer objetivo complejo
```python
lyzu = LYZUCore()
plan = lyzu.decompose_objective("Crea escena 3D con 5 objetos")
for task in plan.tasks:
    print(f"Hacer: {task.description}")
```

### Caso 4: Optimizar parámetro
```python
from core.cognition.c4_auto_tuning_procedural import ParameterBound, ParameterType

def my_procedure(quality: int) -> Dict:
    # Tu código aquí
    return result

bound = ParameterBound("quality", ParameterType.INT, 1, 10, 1)
result = lyzu.optimize_parameter("Máxima calidad", my_procedure, bound)
print(f"Parámetro óptimo: {result.best_parameter}")
```

---

**Última actualización:** 15 Feb 2026  
**Status:** ✅ PRODUCTION READY
