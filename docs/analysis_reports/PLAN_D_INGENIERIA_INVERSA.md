# 🔗 INGENIERÍA INVERSA: Plan D + ZULY_LAB

**Integración de Plan C (Cognición) con ZULY_LAB (Entrenamiento)**

Fecha: 15 Febrero 2026

---

## 🎯 DESCUBRIMIENTO

ZULY_LAB ya tiene estructura perfecta para Plan D:

```
ZULY_LAB/
├─ A_estructura/ (FASE A - Fundación)
├─ B_automatizacion/ (FASE B - Workflows)
├─ C_render_tecnico/ (FASE C - Presentación)
├─ D_integracion_real/ (FASE D - Datos reales) ← AQUÍ va Plan C
├─ dataset_patrones/ (← C2 guardará aquí)
├─ logs_sesiones/ (← C1 guardará logs aquí)
└─ resultados_zuly/ (← Archivos .blend)
```

---

## 📊 MAPEO: Plan C → ZULY_LAB

### C1 - Result Evaluator
**Donde:** `ZULY_LAB/logs_sesiones/`  
**Qué:** Guardar evaluación de cada ejercicio  
**Formato:** JSON con score, métricas, timestamp

```json
{
  "ejercicio": "A1.1_cubo_basico",
  "timestamp": "2026-02-15T14:30:00",
  "c1_evaluation": {
    "objective": "Crear cubo con material rojo",
    "score": 0.95,
    "metrics": {
      "geometry": 0.98,
      "material": 0.92,
      "structure": 0.95
    },
    "diagnostics": []
  }
}
```

### C2 - Experience Memory
**Donde:** `ZULY_LAB/dataset_patrones/`  
**Qué:** Guardar patrón exitoso después de cada ejercicio  
**Formato:** YAML con procedimiento + heurísticas

```yaml
objetivo: "Crear cubo con material rojo"
procedimiento: "create_cube → scale → move → material → apply"
score: 0.95
heuristics:
  - "Para color rojo, usar RGB=(0.8, 0.2, 0.2)"
  - "Scale 2.0 + move [2, 0, 0] = buen spacing"
frecuencia: 1
confianza: 0.95
```

### C3 - Abstract Objectives
**Donde:** `ZULY_LAB/ejercicios/`  
**Qué:** Cada .yaml ES una descomposición  
**Estructura:** Ya tiene steps = descomposición automática

**Ejemplo:** A1.1_cubo_basico.yaml es:
- Objetivo: "Cubo Básico"
- Tareas: [create_cube, scale, move, material, apply, save]
- Dependencias: [create_cube] → [scale, move, material] → [apply] → [save]

### C4 - Auto-tuning
**Donde:** `ZULY_LAB/D_integracion_real/`  
**Qué:** Optimizar parámetros de ejercicios  
**Ejemplo:** Encontrar escala óptima para A1.2 (columnas)

```yaml
# A1.2_columnas_OPTIMIZADO.yaml
ejercicio_base: "A1.2_columnas_alineadas"
parametro_optimizado: "column_height"
rango: [1.0, 10.0]
paso: 0.5
estrategia: "hill_climbing"
resultado_optimo: 4.2
score_maximo: 0.96
```

---

## 🚀 PLAN D REDEFINIDO

**NO crear nueva infraestructura**  
**USAR ZULY_LAB como laboratorio de Plan C**

### FASE D1: Ejecutar Ejercicios A con C1
```
Para cada ejercicio en A_estructura/ejercicios/:
  1. Ejecutar .yaml
  2. C1 evalúa resultado
  3. Log guardado en logs_sesiones/
  4. Si score > 0.8 → Patrón guardado en dataset_patrones/
```

**Resultado esperado:** 4+ ejercicios × score > 0.8 = 4 patrones

### FASE D2: Ejecutar Ejercicios B con C3
```
Para cada ejercicio en B_automatizacion/ejercicios/:
  1. C3 descompone objetivo
  2. Ejecutar pasos en orden
  3. C1 evalúa cada tarea
  4. C2 guarda patrones complejos
```

**Resultado esperado:** Workflows complejos aprenden dependencias

### FASE D3: Ejecutar Ejercicios C con C4
```
Para cada parámetro en C_render_tecnico/:
  1. C4 optimiza parámetro (luz, sombras, etc.)
  2. C1 evalúa calidad render
  3. Heurística óptima guardada en dataset_patrones/
```

**Resultado esperado:** Parámetros óptimos para rendering

### FASE D4: Análisis & Generación de Insights
```
1. Analizar logs_sesiones/*.json
2. Extraer patrones más frecuentes
3. Generar recomendaciones automáticas
4. Crear PLAN_D_RESULTADOS.md
```

---

## 🔧 IMPLEMENTACIÓN

### Script Principal: `zuly_lab.py`

Extiende el script existente con cognición:

```python
#!/usr/bin/env python3
"""
ZULY_LAB - Laboratorio con Plan C integrado
"""

from pathlib import Path
import json
import yaml
from datetime import datetime
from core.cognition import C1ResultEvaluator, C2ExperienceMemory, C3AbstractObjectives, C4AutoTuningProcedural

class ZulyLabWithCognition:
    def __init__(self):
        self.lab_root = Path("ZULY_LAB")
        self.c1 = C1ResultEvaluator()
        self.c2 = C2ExperienceMemory()
        self.c3 = C3AbstractObjectives()
        self.c4 = C4AutoTuningProcedural()
    
    def run_exercise(self, exercise_id: str):
        """
        Ejecuta ejercicio + captura con Plan C
        Ej: "A1.1"
        """
        # Cargar YAML
        yaml_path = self.lab_root / f"A_estructura/ejercicios/{exercise_id}_*.yaml"
        exercise = self.load_yaml(yaml_path)
        
        # Ejecutar pasos
        result = self.execute_steps(exercise["steps"])
        
        # C1: Evaluar
        objective = exercise["descripcion"]
        evaluation = self.c1.evaluate(objective, result)
        
        # Guardar log C1
        log_path = self.lab_root / f"logs_sesiones/{exercise_id}_{datetime.now().isoformat()}.json"
        self.save_log(log_path, evaluation)
        
        # C2: Si score bueno, guardar patrón
        if evaluation.score > 0.8:
            self.c2.store_experience(
                objective=objective,
                procedure=" → ".join([s["action"] for s in exercise["steps"]]),
                result=result
            )
            
            # Guardar patrón en YAML
            pattern_path = self.lab_root / f"dataset_patrones/{exercise_id}_pattern.yaml"
            self.save_pattern(pattern_path, exercise, evaluation)
        
        return evaluation
    
    def run_phase(self, phase: str):
        """Ejecuta todos los ejercicios de una fase: A, B, C, D"""
        fase_dir = self.lab_root / f"{phase}_*"
        ejercicios = sorted(Path.glob(fase_dir))
        
        resultados = []
        for ej in ejercicios:
            resultado = self.run_exercise(ej.stem)
            resultados.append(resultado)
        
        # Generar reporte
        self.generate_phase_report(phase, resultados)
        return resultados

# Uso:
# lab = ZulyLabWithCognition()
# lab.run_phase("A")  # Ejecuta A1.1, A1.2, A1.3, A1.4
```

---

## 📊 SALIDA ESPERADA

### Después de Fase D1 (A_estructura):
```
ZULY_LAB/
├─ logs_sesiones/
│  ├─ A1.1_2026-02-15T14:30:00.json (score: 0.95)
│  ├─ A1.2_2026-02-15T14:35:00.json (score: 0.92)
│  ├─ A1.3_2026-02-15T14:40:00.json (score: 0.88)
│  └─ A1.4_2026-02-15T14:45:00.json (score: 0.90)
└─ dataset_patrones/
   ├─ A1.1_pattern.yaml (guardar cubo + material)
   ├─ A1.2_pattern.yaml (crear columnas duplicadas)
   ├─ A1.3_pattern.yaml (base estructural)
   └─ A1.4_pattern.yaml (organizar escena)
```

### Reporte Generado:
```markdown
# PLAN_D_FASE_A_RESULTADOS.md

## Estadísticas

- Ejercicios ejecutados: 4/4
- Score promedio: 0.91
- Patrones aprendidos: 4
- Confianza promedio: 0.91

## Heurísticas Descubiertas

1. "Para crear columnas bien alineadas, usar spacing = 2.0"
2. "Material rojo óptimo: RGB=(0.8, 0.2, 0.2)"
3. "Scale 2.0 + rotation 45° = estructura equilibrada"
4. ...
```

---

## ✅ DEFINICIÓN DE ÉXITO

- [x] Plan C carga correctamente
- [ ] Ejecuta ejercicio A1.1 sin errores
- [ ] C1 evalúa con score > 0.8
- [ ] C2 guarda patrón en dataset_patrones/
- [ ] C3 descompone objetivo
- [ ] C4 optimiza parámetro
- [ ] Reporte final generado

---

## 🔄 CICLO CONTINUO

```
Usuario: "Enséñale a ZULY a hacer X"
    ↓
Crear ejercicio X.yaml en ZULY_LAB/D_integracion_real/
    ↓
zuly_lab.py run X
    ↓
[Plan C ejecuta]
    ├─ C1: Evalúa resultado
    ├─ C2: Guarda si score > 0.8
    ├─ C3: Descompone en el futuro
    └─ C4: Optimiza parámetros
    ↓
Reporte automático generado
    ↓
Usuario aprueba/rechaza
    ↓
ZULY aprende
```

---

## 🎯 PRÓXIMOS PASOS

1. ✅ Entender ZULY_LAB (HECHO)
2. ⏳ Crear `zuly_lab_with_cognition.py`
3. ⏳ Ejecutar Fase A con C1, C2
4. ⏳ Ejecutar Fase B con C3
5. ⏳ Ejecutar Fase C con C4
6. ⏳ Generar reporte final

---

**Status:** 🚀 LISTO PARA IMPLEMENTAR  
**Enfoque:** Usar infraestructura existente, NO crear nueva
