# GUÍA DE USO - AGENTE ZULY CON IA

## Inicio Rápido

### 1. Iniciación Básica

```python
from core.agent import Agent

# Crear agente
agent = Agent(auto_monitor=True)

# Procesar petición en lenguaje natural
result = agent.process_natural_request("Crea un cubo dorado")

# Obtener resultado
print(result['feedback'])
```

### 2. Peticiones en Lenguaje Natural

El agente entiende múltiples formas de expresar lo mismo:

```python
# Todos estos funcionan:
agent.process_natural_request("Crea un cubo")
agent.process_natural_request("Necesito un cubo")
agent.process_natural_request("Quiero un cubo en la escena")
agent.process_natural_request("Box creation por favor")  # Mezcla de idiomas
```

### 3. Resultados Complejos

```python
result = agent.process_natural_request("Crea una escena bonita")

# Acceder a información:
print(result['success'])           # ¿Fue exitoso?
print(result['command_executed'])  # ¿Qué comando se ejecutó?
print(result['confidence'])        # Confianza de interpretación (0-1)
print(result['feedback'])          # Mensaje legible para el usuario
print(result['scene_state'])       # Estado actual de la escena
print(result['parameters'])        # Parámetros extraídos
```

---

## Ejemplos Prácticos

### Ejemplo 1: Crear Objetos Simples

```python
from core.agent import Agent

agent = Agent()

# Crear cubo
result = agent.process_natural_request("Crea un cubo")
print(result['feedback'])
# ✓ Cubo creado exitosamente. Escena actualizada: 1 objeto

# Crear esfera
result = agent.process_natural_request("Necesito una esfera")
print(result['feedback'])
```

### Ejemplo 2: Transformaciones

```python
# Mover objeto
result = agent.process_natural_request("Mueve el cubo a la posición 5, 3, 0")

# Rotar objeto
result = agent.process_natural_request("Gira el cubo 45 grados")

# Escalar objeto
result = agent.process_natural_request("Haz el cubo el doble de grande")
```

### Ejemplo 3: Materiales

```python
# Aplicar material
result = agent.process_natural_request("Dale al cubo un aspecto dorado")

# Otros materiales disponibles:
agent.process_natural_request("Aplica un material de vidrio")
agent.process_natural_request("Hazlo plateado y brillante")
agent.process_natural_request("Negro mate por favor")
```

### Ejemplo 4: Iluminación

```python
# Agregar luz
result = agent.process_natural_request("Añade una luz solar brillante")

# Luz puntual
result = agent.process_natural_request("Crea una lámpara de punto focal")

# Luz de área
result = agent.process_natural_request("Ilumina la escena con luz de área")
```

### Ejemplo 5: Escena Completa

```python
peticion = """
Necesito una escena con:
- Un cubo de oro en el centro
- Una esfera plateada a la derecha
- Iluminación solar desde arriba
- Una cámara bien posicionada
"""

result = agent.process_natural_request(peticion)
print(result['feedback'])
```

---

## Comandos Disponibles

El agente puede ejecutar estos comandos:

### Primitivas
- `CrearPrimitivaCubo` - Crea un cubo
- `CrearPrimitvaEsfera` - Crea una esfera
- `CrearPrimitivaCilindro` - Crea un cilindro
- `CrearPrimitivaCono` - Crea un cono
- `CrearPrimitivaPlano` - Crea un plano

### Transformaciones
- `TransformarObjeto` - Modifica posición, rotación o escala

### Materiales
- `AplicarMaterial` - Aplica material predefinido

### Iluminación
- `AnadirLuz` - Agrega luz a la escena

### Cámara
- `ConfigurarCamara` - Posiciona y configura la cámara

### Rendering
- `RenderizarEscena` - Genera imagen final
- `ExportarEscena` - Exporta en varios formatos

### Para ver comandos disponibles:
```python
commands = agent.get_available_commands()
for cmd_name, description in commands.items():
    print(f"{cmd_name}: {description}")
```

---

## Parámetros Comunes

### Ubicación (Posición)
Acepta: `ubicacion`, `posicion`, `position`, `pos`

```python
result = agent.process_natural_request("Coloca el cubo en 10, 5, 0")
```

### Rotación
Acepta: `rotacion`, `rotation`, `giro`, `angulo`

```python
result = agent.process_natural_request("Rota el objeto 45 grados")
```

### Escala (Tamaño)
Acepta: `escala`, `scale`, `tamaño`, `size`

```python
result = agent.process_natural_request("Aumenta el tamaño 2 veces")
```

### Nombre
Acepta: `nombre`, `name`, `object_name`, `objeto`

```python
result = agent.process_natural_request("Llama al cubo MiCubo")
```

---

## Monitoreo de Escena

### Ver Estado Actual

```python
summary = agent.scene_monitor.get_scene_summary()

print(f"Objetos: {summary['object_count']}")
print(f"Luces: {summary['light_count']}")
print(f"Cámaras: {summary['camera_count']}")
print(f"Objetos: {summary['objects']}")  # Nombres
```

### Exportar Datos

```python
# Exportar captura de escena
file_path = agent.scene_monitor.export_scene_snapshot()
print(f"Escena guardada en: {file_path}")

# Exportar historial de comandos
file_path = agent.scene_monitor.export_command_history()
print(f"Historial guardado en: {file_path}")
```

### Validar Requisitos

```python
satisfied, problems = agent.scene_monitor.has_required_elements({
    'object': 3,
    'light': 1,
    'camera': 1
})

if not satisfied:
    print("Problemas detectados:")
    for problem in problems:
        print(f"  - {problem}")
```

---

## Gestión de Sesiones

### Ver Estadísticas

```python
summary = agent.get_session_summary()

print(f"Comandos ejecutados: {summary['commands_executed']}")
print(f"Exitosos: {summary['successes']}")
print(f"Fallidos: {summary['failures']}")
print(f"Duración: {summary['session_start']}")
```

### Exportar Reporte Completo

```python
report_path = agent.export_session_report()
print(f"Reporte guardado en: {report_path}")

# El reporte contiene:
# - Resumen de sesión
# - Historial de ejecuciones
# - Estadísticas de comandos
# - Comandos disponibles
# - Estado final de escena
```

---

## Manejo de Errores

### Peticiones Inválidas

```python
result = agent.process_natural_request("")

if not result['success']:
    print(f"Error: {result['error']}")
    print(f"Sugerencia: {result.get('suggestions', [])}")
```

### Comandos No Reconocidos

```python
result = agent.process_natural_request("creaaa un cuboooo")

if not result['success'] and 'suggestion' in result:
    print(f"¿Quisiste decir '{result['suggestion']}'?")
    print(f"Similitud: {result['similarity']:.0%}")
```

### Parámetros Inválidos

```python
result = agent.process_natural_request("Mueve a una posición inválida")

if not result['success']:
    print(f"Información de error: {result}")
```

---

## API Avanzada

### Ejecución Directa de Comandos

```python
# API anterior (sigue funcionando)
result = agent.execute_command(
    'crearprimitivacubo',
    name='MiCubo',
    location=(0, 0, 0)
)
```

### Acceso a NLU Directo

```python
intents = agent.nlu.process("Crea un cubo")

for intent in intents:
    print(f"Comando: {intent.command_name}")
    print(f"Confianza: {intent.confidence}")
    print(f"Parámetros: {intent.parameters}")
```

### Corrección de Comandos

```python
similar = agent.nlu.find_similar_command("creerprimitivacubo")

if similar:
    cmd, ratio = similar
    print(f"¿Quisiste decir '{cmd}'? (similitud: {ratio:.0%})")
```

---

## Pruebas

### Ejecutar Suite de Pruebas

```bash
# Desde el directorio raíz del proyecto
python -m core.tests.test_nlu_and_agent
```

### Pruebas Específicas

```bash
# Solo NLU
python -m unittest core.tests.test_nlu_and_agent.TestNLU -v

# Solo Agent
python -m unittest core.tests.test_nlu_and_agent.TestAgent -v

# Solo Scene Monitor
python -m unittest core.tests.test_nlu_and_agent.TestSceneMonitor -v
```

---

## Mejores Prácticas

### 1. Usar Peticiones Claras y Naturales
```python
# ✓ Bien
agent.process_natural_request("Crea un cubo de oro en el centro")

# ✗ Evitar
agent.execute_command('crearprimitivacubo', location=(0,0,0), material='oro')
```

### 2. Verificar Resultados
```python
result = agent.process_natural_request(...)

if result['success']:
    print("Éxito!")
else:
    print(f"Error: {result['error']}")
    print(f"Feedback: {result['feedback']}")
```

### 3. Monitorear la Escena
```python
agent = Agent(auto_monitor=True)  # Captura automáticamente

result = agent.process_natural_request(...)
print(f"Escena: {result['scene_state']}")
```

### 4. Guardar Reportes
```python
# Al final de la sesión
report_path = agent.export_session_report()
print(f"Session guardada en {report_path}")
```

---

## Solución de Problemas

### El comando no se reconoce
- Intenta usar sinónimos: "esfera" = "sphere", "bola"
- Verifica la ortografía
- El sistema buscará comandos similares automáticamente

### Parámetros incorrecto
- El agente intenta corregir automáticamente
- Verifica que uses números válidos: `5, 3, 0` para posición
- Usa nombres simples para objetos sin caracteres especiales

### La escena no se actualiza
- Asegúrate de que `auto_monitor=True`
- Verifica que Blender esté disponible (bpy importable)
- Revisa los logs en `bitacora/zuly_agent.log`

### Bajo rendimiento
- Reduce la cantidad de comandos por sesión
- Desactiva `auto_monitor=False` si no lo necesitas
- Usa `export_session_report()` solo cuando sea necesario

---

## Recursos

- **Documentación detallada**: `ARQUITECTURA_MEJORADA.md`
- **Código fuente**: `core/agent.py`, `core/utils/nlu.py`, `core/commands/extended_commands.py`
- **Pruebas**: `core/tests/test_nlu_and_agent.py`
- **Configuración**: `config.json`, `core/config.py`

---

## Soporte

Para reportar problemas o sugerir mejoras:
1. Revisa los logs en `bitacora/zuly_agent.log`
2. Ejecuta las pruebas: `python -m core.tests.test_nlu_and_agent`
3. Consulta la documentación en `ARQUITECTURA_MEJORADA.md`
