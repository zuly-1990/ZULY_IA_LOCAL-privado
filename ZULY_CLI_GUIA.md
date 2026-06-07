# ZULY CLI INTERACTIVO - GUÍA DE USO

**Estado:** ✅ OPERACIONAL (Opción 2 Completada)

## Descripción

ZULY CLI es una interfaz de línea de comandos que permite controlar LYZU usando **lenguaje natural en español**. No requiere código ni configuración compleja.

## Instalación

```bash
# Ya incluido en ZULY_IA_LOCAL
# Solo ejecutar:
python zuly_cli_interactive.py
```

## Uso Básico

### Modo Interactivo

```bash
$ python zuly_cli_interactive.py

======================================================================
  ZULY CLI INTERACTIVO v2.0
======================================================================

zuly> crear un cubo
📋 Acciones: 1 | Confianza: 95%
   • create_cube
⚙️  Ejecutando...
✅ Completado: 1 objeto creado

zuly> crear esfera y rotar 45 grados
📋 Acciones: 2 | Confianza: 90%
   • create_sphere
   • rotate_object

zuly> exit
👋 Hasta luego!
```

## Comandos Soportados

| Comando | Acción | Ejemplo |
|---------|--------|---------|
| `crear cubo` | Crea un cubo 3D | `crear un cubo` |
| `crear esfera` | Crea una esfera | `crear una esfera` |
| `crear cilindro` | Crea un cilindro | `crear cilindro` |
| `crear cono` | Crea un cono | `crear un cono` |
| `rotar X grados` | Rota el objeto | `rotar 45 grados` |
| `escalar N` | Aumenta tamaño | `escalar 2.0` |
| `mover X` | Mueve objeto | `mover 5 unidades` |
| `arquitectura` | Crea escena Villa Savoye | `crear arquitectura` |
| `renderizar` | Renderiza la escena | `renderizar` |
| `review` | Revisa patrones pendientes | `review` |
| `approve <id>` | Aprueba un patrón | `approve d4f1` |
| `reject <id>` | Rechaza un patrón | `reject d4f1` |

## Ejemplos de Uso

### Ejemplo 1: Crear geometría simple
```
zuly> crear cubo
✅ Completado: 1 objeto creado

zuly> crear esfera
✅ Completado: 1 objeto creado
```

### Ejemplo 2: Transformaciones
```
zuly> crear cubo y rotar 45 grados
✅ Completado: 1 objeto creado

zuly> escalar 2.0
✅ Completado
```

### Ejemplo 3: Comandos complejos
```
zuly> crear esfera y rotar 90 grados luego escalar 1.5
📋 Acciones: 3 | Confianza: 85%
   • create_sphere
   • rotate_object
   • scale_object
✅ Completado
```

### Ejemplo 4: Arquitectura
```
zuly> crear arquitectura villa savoye
📋 Acciones: 1 | Confianza: 80%
   • create_scene_villa_savoye
✅ Completado: 2 objetos creados
```

## Características

✅ **Lenguaje Natural:** Entiende español directo
✅ **Parsing Inteligente:** Extrae parámetros a partir del texto
✅ **Confianza Dinámica:** Indica qué tan seguro está de la interpretación
✅ **Ejecución Real:** Comunicación directa con Blender 3.6
✅ **Feedback Inmediato:** Resultados en tiempo real
✅ **Historial:** Opcional almacenar comandos ejecutados

## Cómo Funciona

```
Entrada en Lenguaje Natural
         ↓
    [PARSER]
         ↓
Lista de Acciones + Confianza
         ↓
   [VALIDAR]
         ↓
  [GENERAR SCRIPT PYTHON PARA BLENDER]
         ↓
   [EJECUTAR EN BLENDER]
         ↓
   [PROCESAR RESULTADO]
         ↓
   Feedback al Usuario
```

### Parser

El parser transforma texto en acciones usando:
- **Mapa de palabras clave:** "cubo" → `create_cube`
- **Extracción de parámetros:** "45 grados" → `rotation: 45`
- **Conectores:** "y", "luego", "después" separan acciones
- **Scoring de confianza:** Penaliza comandos no reconocidos

### Generador de Scripts

Convierte acciones a código Python que Blender entiende:

```python
import bpy
try:
    bpy.ops.mesh.primitive_cube_add(size=2)
    results['objects'] += 1
except Exception as e:
    results['commands'].append({'status': 'error'})
```

## Estadísticas

**Última ejecución:**
- Comandos reconocidos: 6/8 (75% en español)
- Confianza promedio: 81.9%
- Velocidad: <5 segundos por comando

## Limitaciones Actuales

⚠️ **Español solo:** Por ahora no soporta inglés
⚠️ **Geometría básica:** No soporta mallas complejas
⚠️ **Sin booleans:** No puede hacer operaciones CSG aún
⚠️ **Parámetros simples:** Ángulos en grados, distancias en unidades BU

## Próximas Mejoras

🔄 Integración con C3 Objectives (descomponer tareas complejas)
🔄 Soporte para booleans y operaciones CSG
🔄 Historial persistente
🔄 Auto-complete y sugerencias
🔄 Integración con C2 Memory (aprender de experiencias previas) ✅ (Fase 25)
🔄 Modo batch (ejecutar lista de comandos)
🔄 Control de Calidad Humano (Comandos `review`, `approve`, `reject`) ✅ (Fase 25)

## Debugging

### El parser no reconoce mi comando
- Intenta usar palabras más simples
- Usa presente: "crear" no "crearemos"
- Especifica ángulos: "45 grados" no solo "45"

### Blender no ejecuta
- Verifica que Blender 3.6 esté instalado en `blender/v3/blender-3.6.0-zuly/`
- Revisa que no haya otra instancia ejecutándose
- Intenta reinicar el ambiente

### Script no genera resultado
- Revisa `zuly_result.json` en el directorio de trabajo
- Verifica mensajes de error en terminal

## Integración con ZULY

El CLI se integra con:
- **LYZU Core:** Handlers de Blender
- **C2 Memory:** Experiencias de acciones previas (próximo)
- **C3 Objectives:** Descomposición de tareas (próximo)
- **Evaluador C1:** Evaluación de resultados (próximo)

## Futura Arquitectura

```
┌─────────────────────┐
│   CLI Interactivo   │  ← Lenguaje Natural
└──────────┬──────────┘
           │
    ┌──────▼──────┐
    │ NLParser    │  95% español, 81.9% confianza
    └──────┬──────┘
           │
    ┌──────▼──────┐
    │ Validador   │  Chequea confianza ≥ 0.3
    └──────┬──────┘
           │
    ┌──────▼───────────┐
    │ ScriptGenerator  │  Crea code Blender puro
    └──────┬───────────┘
           │
    ┌──────▼──────┐
    │  Blender    │  Ejecuta 3.6.2
    └──────┬──────┘
           │
    ┌──────▼──────┐
    │  C1 Result  │  Evalúa calidad resultado
    │  Evaluator  │  (próximo)
    └──────┬──────┘
           │
    ┌──────▼──────┐
    │ C2 Memory   │  Guarda experiencia
    │             │  (próximo)
    └─────────────┘
```

## Versión

- **Versión CLI:** 2.0
- **LYZU Core:** 1.0
- **Blender Target:** 3.6.2
- **Python:** 3.10+

---

**Creado como Opción 2 del Plan de Trabajo ZULY**
Hecha: 2024-02-22
Estado: ✅ FUNCIONAL
