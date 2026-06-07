# C2 - MEMORY OF EXPERIENCES - CORE

**¿Qué es?**  
Sistema que almacena experiencias (objetivo → procedimiento → resultado) y aprende patrones para sugerir mejoras futuras.

**¿Para qué?**
- No repetir el mismo error
- Sugerir procedimientos que funcionaron antes
- Llenar base de datos de heurísticas
- Entrenar C4 con pesos iniciales

---

## 🏗️ ARQUITECTURA

```
C2ExperienceMemory
├─ ExperienceStorage (SQLite)
│  ├─ Tabla: experiences (objetivo, procedure, result, score)
│  └─ Tabla: heuristics (parámetro óptimo guardado)
├─ ExperienceExtractor
│  ├─ Extrae insights automáticamente
│  └─ Detecta patrones
└─ PatternMatcher
   ├─ Búsqueda por similitud
   └─ Retorna opciones
```

---

## 📊 BASE DE DATOS

### Tabla: experiences
```sql
CREATE TABLE experiences (
    id INTEGER PRIMARY KEY,
    objective TEXT,
    procedure TEXT,
    result JSON,
    score FLOAT,
    timestamp DATETIME,
    insights TEXT
);
```

### Tabla: heuristics
```sql
CREATE TABLE heuristics (
    id INTEGER PRIMARY KEY,
    procedure TEXT,
    parameter_name TEXT,
    optimal_value FLOAT,
    confidence FLOAT,
    timestamp DATETIME
);
```

---

## 💻 EJEMPLO DE USO

```python
from core.cognition.c2_experience_memory import C2ExperienceMemory

# Crear memoria
memory = C2ExperienceMemory()

# Guardar experiencia
memory.store_experience(
    objective="Crea un cubo rojo",
    procedure="blender.create_cube(color='red')",
    result={"score": 0.95, "objects": 1},
    insights="El color rojo debe ser RGB=(1,0,0)"
)

# Buscar similar
patterns = memory.find_similar_patterns("Crea un cubo")
for p in patterns:
    print(f"{p.objective}: score={p.avg_score}")

# Exportar
memory.export_to_json("memory_backup.json")
```

---

## 🔄 FLUJO DE ALMACENAMIENTO

```
1. USUARIO EJECUTA: "Crea un cubo rojo"
   ├─ Procedimiento: blender.create_cube(color='red')
   └─ Resultado: score=0.95

2. C2 EXTRAE INSIGHTS:
   ├─ "Para rojo brillante, usa RGB=(1,0,0)"
   └─ "Procedimiento tarda 0.5 segundos"

3. C2 GUARDA EN SQLite:
   ├─ experiences table: (objetivo, proc, resultado, insights)
   └─ heuristics table: (procedimiento, parámetro_óptimo, confianza)

4. C2 CREA ÍNDICES:
   ├─ Por objetivo (búsqueda rápida)
   └─ Por palabras clave (similitud)

5. PRÓXIMA VEZ USUARIO PIDE SIMILAR:
   ├─ C2 busca: "Crea un cubo azul"
   └─ Retorna: "Usa RGB=(0,0,1), tarda 0.5s"
```

---

## 📝 ESTRUCTURA DE DATOS

### Experience (dataclass)
```python
@dataclass
class Experience:
    objective: str
    procedure: str
    result: Dict
    score: float
    timestamp: str
    insights: List[str]
```

### Pattern (dataclass)
```python
@dataclass
class Pattern:
    objective: str
    avg_score: float
    frequency: int
    similar_objectives: List[str]
    recommended_procedure: str
    confidence: float
```

---

## 🧪 TESTS PRINCIPALES

| Test | Descripción | Status |
|------|------------|--------|
| test_store_experience | Guarda en SQLite | ✅ |
| test_retrieve_experience | Lee de SQLite | ✅ |
| test_find_similar_patterns | Búsqueda por similitud | ✅ |
| test_extract_insights | Extrae heurísticas | ✅ |
| test_export_json | Exporta correctamente | ✅ |

---

## 🔗 INTEGRACIÓN CON OTROS COMPONENTES

### Con C1 (Evaluator)
```
C1 Genera score = 0.95
   ↓
C2 Guarda: (objetivo, proc, score=0.95)
```

### Con C4 (Auto-tuning)
```
C4 Busca heurística: "¿Cuál es el roughness óptimo?"
   ↓
C2 Retorna: roughness=0.25 (confianza=0.8)
   ↓
C4 Usa como valor inicial para optimización
```

---

## 📚 REFERENCIAS

- Tests: [test_c2_experience_memory.py](../../tests/test_c2_experience_memory.py)
- DB Schema: memory.db en bitacora/
- Demo: [demo_c2_memory.py](../../demo_c2_memory.py)

---

**Status:** ✅ PRODUCCIÓN READY
