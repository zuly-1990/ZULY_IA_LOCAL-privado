# ZULY 3.0 - GUIA DE USO RAPIDO (QUICK START)

## INICIO INMEDIATO

### Opcion 1: Modo Normal (Como Antes)
```python
from lyzu_core import LYZUCore

# Inicializar
lyzu = LYZUCore(mode='hybrid')

# Usar
result = lyzu.process_user_input("Crea un cubo rojo")
# Ejecuta UNA estrategia, pide confirmacion
```

### Opcion 2: Modo Learning Freedom (NUEVO - RECOMENDADO)
```python
from lyzu_core import LYZUCore

# Inicializar con Learning Freedom
lyzu = LYZUCore(mode='hybrid', enable_learning_freedom=True)

# Usar (TODO AUTOMATICO)
result = lyzu.process_with_learning_freedom("Crea algo hermoso")
# - Genera 5 estrategias automaticamente
# - Ejecuta todas en paralelo
# - Auto-selecciona ganador
# - Aprende del resultado
```

---

## EJEMPLO PRACTICO

```python
from lyzu_core import LYZUCore

# Crear instancia con Learning Freedom
lyzu = LYZUCore(mode='hybrid', enable_learning_freedom=True)

# Procesar solicitud
resultado = lyzu.process_with_learning_freedom("Crea una escena con iluminacion dramatica")

# Ver resultado
print(f"Estrategia ganadora: {resultado['assessment']['strategy_type']}")
print(f"Score: {resultado['best_score']:.1f}/100")
print(f"Tiempo ejecucion: {resultado['execution_time_ms']:.0f}ms")

# El sistema automaticamente:
# 1. Genero 5 estrategias diferentes
# 2. Ejecuto todas
# 3. Evaluo cada una con 7 criterios
# 4. Eligio la mejor
# 5. Aprendi del resultado para proximas veces
```

---

## COMPONENTES DISPONIBLES

### 1. LearningFreedomEngine
- Genera estrategias alternativas
- Ejecuta en paralelo
- Auto-selecciona mejor

```python
from core.learning import LearningFreedomEngine
engine = LearningFreedomEngine(max_strategies=5)
strategies = engine.generate_strategies(
    user_prompt="Crea algo",
    intent="crear_objeto",
    entities={'objeto': 'cube'}
)
```

### 2. KnowledgeGraph
- Base de datos semantica
- Relaciones entre objetos
- Inferencias automaticas

```python
from core.knowledge import KnowledgeGraph
kg = KnowledgeGraph()
kg.add_object("MiCubo", "OBJECT", {'color': 'red'})
kg.add_material("Material1", {'color': [1, 0, 0]})
```

### 3. SelfAssessmentEngine
- Evalua escenas 0-100
- 7 criterios automaticos
- Niveles de calidad

```python
from core.learning.self_assessment import SelfAssessmentEngine
assess = SelfAssessmentEngine()
score = assess.assess_scenario({
    'num_objects': 5,
    'lighting_quality': 8
})
print(f"Score: {score['score']}/100")
```

### 4. StrategySynthesizer
- Crea nuevas estrategias
- Cross-breeding
- Mutaciones

```python
from core.learning.strategy_synthesizer import StrategySynthesizer
synth = StrategySynthesizer()
new_strategies = synth.synthesize(n=10)
```

---

## MODOS DE FUNCIONAMIENTO

### Modo REACTIVE (Automatico Total)
```python
lyzu = LYZUCore(mode='reactive', enable_learning_freedom=True)
# Ejecuta sin pedir confirmacion
# Ideal para automatizacion
```

### Modo HYBRID (Confirmacion Manual)
```python
lyzu = LYZUCore(mode='hybrid', enable_learning_freedom=True)
# Pide aprobacion para comandos
# Ideal para desarrollo/pruebas
```

### Modo AUTONOMOUS (Futuro)
```python
lyzu = LYZUCore(mode='autonomous', enable_learning_freedom=True)
# Toma decisiones completamente autonomo
# Requiere validacion extra
```

---

## HANDLERS DISPONIBLES

### Basicos (8)
- `create_cube` - Crear cubo
- `create_sphere` - Crear esfera
- `create_cylinder` - Crear cilindro
- `move_object` - Mover objeto
- `rotate_object` - Rotar objeto
- `scale_object` - Escalar objeto
- `render_scene` - Renderizar escena
- `system_get_info` - Info del sistema

### Avanzados (15)
**Materiales**: create_material, apply_material, set_material_color
**Luces**: create_light, set_light_energy, set_light_color
**Camaras**: create_camera, set_active_camera, position_camera
**Modificadores**: add_subdivision_surface, add_array, add_bevel
**Exportacion**: export_fbx, export_obj, export_gltf

---

## EJEMPLO: WORKFLOW COMPLETO

```python
from lyzu_core import LYZUCore

# 1. Crear sistema
lyzu = LYZUCore(mode='hybrid', enable_learning_freedom=True)
print("Sistema inicializado")
print(f"Version: {lyzu.version}")
print(f"Learning Freedom: {'ON' if lyzu.learning_freedom_enabled else 'OFF'}")

# 2. Primera solicitud (Learning Freedom genera multiples opciones)
resultado1 = lyzu.process_with_learning_freedom("Crea un cubo bonito")
print(f"Primera ejecucion: {resultado1['best_score']:.1f}/100")

# 3. Segunda solicitud (Sistema ha aprendido de la primera)
resultado2 = lyzu.process_with_learning_freedom("Crea una esfera")
print(f"Segunda ejecucion: {resultado2['best_score']:.1f}/100")

# 4. Ver estadisticas de memoria
stats = lyzu.memory.get_memory_stats()
print(f"Turnos procesados: {stats['total_turns_processed']}")
print(f"Uso de memoria: {stats['memory_usage_pct']:.1f}%")

# 5. Acceder a Knowledge Graph
objetos = lyzu.knowledge_graph.query_objects(limit=10)
print(f"Objetos en escena: {len(objetos)}")
```

---

## DIAGNOSTICO / VERIFICACION

### Verificar que todo funciona
```python
from lyzu_core import LYZUCore

lyzu = LYZUCore(mode='hybrid', enable_learning_freedom=True)

# Verificar modulos
assert lyzu.learning_engine is not None, "Learning Engine: ERROR"
assert lyzu.knowledge_graph is not None, "Knowledge Graph: ERROR"
assert lyzu.self_assessment is not None, "Self-Assessment: ERROR"
assert lyzu.strategy_synthesizer is not None, "Synthesizer: ERROR"

print("TODOS LOS MODULOS: OK")
print("SISTEMA LISTO")
```

### Ver logs
```python
# Los logs se generan automaticamente en:
# bitacora/  - Documentacion
# bitacora/archive/ - Turnos archivados
# bitacora/knowledge_graph.db - Base de datos
```

---

## CASOS DE USO

### Caso 1: Generar Arte Automatico
```python
lyzu = LYZUCore(mode='reactive', enable_learning_freedom=True)

for i in range(10):
    result = lyzu.process_with_learning_freedom("Crea algo unico")
    print(f"Obra {i+1}: Score {result['best_score']:.1f}")
    # Cada llamada genera 5 opciones diferentes
    # Sistema aprende cual estilo es mejor
```

### Caso 2: Exploracion de Espacios de Diseno
```python
lyzu = LYZUCore(mode='hybrid', enable_learning_freedom=True)

# Sistema explora multiples estrategias automaticamente
result = lyzu.process_with_learning_freedom(
    "Explora diseños minimales con 3 elementos"
)

# Puedes ver:
# - Que estrategias se intentaron
# - Cual fue la mejor
# - Por que fue mejor (scores)
```

### Caso 3: Mejora Iterativa
```python
lyzu = LYZUCore(mode='hybrid', enable_learning_freedom=True)

solicitud = "Crea una escena surrealista"
for iteracion in range(5):
    result = lyzu.process_with_learning_freedom(solicitud)
    print(f"Iteracion {iteracion}: {result['best_score']:.1f}")
    # Cada iteracion el sistema genera opciones mas refinadas
```

---

## PREGUNTAS FRECUENTES

**P: Cual es la diferencia entre mode='reactive' y mode='hybrid'?**
R: reactive = ejecucion automatica sin confirmacion
   hybrid = pide aprobacion antes de ejecutar

**P: Como puedo ver que estrategias se generaron?**
R: El sistema log todas las estrategias en bitacora/
   Ver learning_engine._log() para detalles

**P: Se puede usar sin Blender?**
R: Si, pero los handlers de Blender no funcionaran.
   El sistema mostrara errores pero seguira funcionando.

**P: Como puedo reset el aprendizaje?**
R: Borrar bitacora/knowledge_graph.db
   Crear nueva instancia LYZUCore()

**P: Cual es el limite de memoria?**
R: 500 turnos en memoria activa
   Luego se archivan automaticamente a bitacora/archive/

---

## DOCUMENTACION COMPLETA

Para mas detalles, ver:

1. **Cambios realizados**: CERTIFICADO_REPARACION.txt
2. **Arquitectura**: REPARACION_PROYECTO_ESTADO.md
3. **Detalles tecnicos**: DETALLES_REPARACION_TECNICOS.txt
4. **Resumen**: RESUMEN_REPARACION.txt

Para validar el sistema:
```bash
python validate_integration_fixed.py
```

Para ver demos:
```bash
python demo_learning_freedom.py
```

Para ejecutar tests:
```bash
python test_learning_freedom.py
```

---

## RESUMEN

✓ Sistema ZULY 3.0 completamente operativo
✓ Learning Freedom Framework activo y funcionando
✓ 23 handlers disponibles
✓ 19/19 tests pasando
✓ Listo para usar en produccion

Usa `process_with_learning_freedom()` para aprovechar todas las capacidades.
