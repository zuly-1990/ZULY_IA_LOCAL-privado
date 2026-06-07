# MANUAL DE USO - ZULY 2026
## Agente IA para Blender (ACTUALIZADO)

**Versión**: 2.0 - Febrero 2026  
**Estado**: ✅ Sistema 100% Operacional  
**Última Actualización**: 2026-03-15 (Fase F - Edit Mode y Escultura Arquitectónica)
**Hitos**: ✅ Plan D Completado | ✅ Plan E (Maestría) Completado | ✅ Fase F (Edit Mode) Completado

---

## 📦 Configuración del Sistema

### Ubicación de Blender

ZULY incluye Blender 3.6.0 integrado en:

```
C:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe
```

**No necesitas instalar Blender por separado** - todo está incluido en ZULY.

### Estructura de Carpetas

```
ZULY_IA_LOCAL/
├── blender/              # Blender 3.6.0 incluido
├── core/                 # Motor ZULY y LYZU
├── manuales/             # Documentación oficial
├── ZULY_PROJECTS/        # Gestión de Activos 3D
│   ├── ejemplos/         # Modelos de referencia (ej. edificio_2, casarural)
│   └── pruebas/          # Resultados de síntesis y tests (ej. urban_synthesis)
└── knowledge_base/       # ADN y patrones aprendidos
```

---

## 🚀 Inicio Rápido

### Método 1: Script de Prueba (Recomendado)

```powershell
# Desde ZULY_IA_LOCAL
.\run_zuly_blender_real.ps1
```

Este script:
- ✅ Inicia Blender automáticamente
- ✅ Carga ZULY
- ✅ Ejecuta 3 comandos de ejemplo
- ✅ Guarda `.blend` en `ZULY_PROJECTS/`

### Método 2: Python Directo

```python
import bpy
import sys
sys.path.insert(0, r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL")

from core.agent import Agent

# Inicializar con Blender REAL
agent = Agent(force_mock=False)

# Crear cubo
result = agent.execute_via_router('blender.create_cube', {
    'location': [0, 0, 0],
    'scale': 2.0
})

print(f"Éxito: {result['success']}")
```

### Método 3: Simulación (Sin Blender)

```python
from core.agent import Agent

# MockAdapter - para testing sin Blender
agent = Agent(force_mock=True)

# Mismo código, solo simula
result = agent.execute_via_router('blender.create_cube', {...})
```

---

## 🗣️ Lenguaje Natural (Recomendado)

### Uso Básico

ZULY entiende lenguaje natural en español e inglés:

```python
from core.agent import Agent

agent = Agent(force_mock=False)  # o True para simulación

# Interfaz de lenguaje natural
result = agent.process_natural_request("Crea un cubo dorado")

print(result['feedback'])
# → "✓ Cubo creado exitosamente"
```

### Variaciones Aceptadas

El agente entiende múltiples formas de expresar lo mismo:

```python
# Todas estas funcionan:
agent.process_natural_request("Crea un cubo")
agent.process_natural_request("Necesito un cubo")
agent.process_natural_request("Quiero un cubo en la escena")
agent.process_natural_request("Box creation por favor")  # Mezcla idiomas

# Transformaciones naturales:
agent.process_natural_request("Mueve el cubo a la posición 5, 3, 0")
agent.process_natural_request("Gira el cubo 45 grados")
agent.process_natural_request("Haz el cubo el doble de grande")

# Materiales descriptivos:
agent.process_natural_request("Dale al cubo un aspecto dorado")
agent.process_natural_request("Hazlo plateado y brillante")
```

### Respuesta Estructurada

```python
result = agent.process_natural_request("Crea una escena bonita")

# Información disponible:
print(result['success'])           # ¿Exitoso?
print(result['command_executed'])  # Comando ejecutado
print(result['confidence'])        # Confianza NLU (0-1)
print(result['feedback'])          # Mensaje al usuario
print(result['scene_state'])       # Estado de escena
print(result['parameters'])        # Parámetros extraídos
```

---

## 📊 Monitoreo de Escena (SceneMonitor)

### Estado Actual de la Escena

```python
# Ver resumen
summary = agent.scene_monitor.get_scene_summary()

print(f"Objetos: {summary['object_count']}")
print(f"Luces: {summary['light_count']}")
print(f"Cámaras: {summary['camera_count']}")
print(f"Lista: {summary['objects']}")  # Nombres de objetos
```

### Exportar Instantáneas

```python
# Exportar estado de escena completo
snapshot_path = agent.scene_monitor.export_scene_snapshot()
print(f"Instantánea guardada en: {snapshot_path}")

# Exportar historial de comandos
history_path = agent.scene_monitor.export_command_history()
print(f"Historial guardado en: {history_path}")
```

### Validar Requisitos

```python
# Verificar que la escena tenga elementos requeridos
requisitos = {
    'object': 3,   # Al menos 3 objetos
    'light': 1,    # Al menos 1 luz
    'camera': 1    # Al menos 1 cámara
}

satisfied, problems = agent.scene_monitor.has_required_elements(requisitos)

if not satisfied:
    print("Elementos faltantes:")
    for problem in problems:
        print(f"  - {problem}")
else:
    print("✓ Escena cumple requisitos")
```

---

## 📈 Estadísticas y Reportes de Sesión

### Ver Estadísticas

```python
summary = agent.get_session_summary()

print(f"Comandos ejecutados: {summary['commands_executed']}")
print(f"Exitosos: {summary['successes']}")
print(f"Fallidos: {summary['failures']}")
print(f"Inicio sesión: {summary['session_start']}")
print(f"Tasa éxito: {summary['successes']/summary['commands_executed']*100:.1f}%")
```

### Exportar Reporte Completo

```python
# Al final de tu sesión
report_path = agent.export_session_report()
print(f"Reporte completo guardado en: {report_path}")

# El reporte incluye:
# - Resumen de sesión
# - Historial completo de comandos
# - Estadísticas detalladas
# - Lista de comandos disponibles
# - Estado final de la escena
```

---

## 🧠 Acceso Directo al NLU

### Procesar Intents Manualmente

```python
# Analizar qué entiende ZULY de una frase
intents = agent.nlu.process("Crea un cubo")

for intent in intents:
    print(f"Comando: {intent.command_name}")
    print(f"Confianza: {intent.confidence:.0%}")
    print(f"Parámetros: {intent.parameters}")
```

### Buscar Comandos Similares

```python
# Si escribiste mal un comando
similar = agent.nlu.find_similar_command("creerprimitivacubo")

if similar:
    cmd, ratio = similar
    print(f"¿Quisiste decir '{cmd}'?")
    print(f"Similitud: {ratio:.0%}")
```

---

## ⚠️ Manejo de Errores Avanzado

### Peticiones Inválidas

```python
result = agent.process_natural_request("")

if not result['success']:
    print(f"Error: {result['error']}")
    if 'suggestions' in result:
        print(f"Sugerencias: {result['suggestions']}")
```

### Comandos No Reconocidos

```python
result = agent.process_natural_request("creaaa un cuboooo")

if not result['success'] and 'suggestion' in result:
    print(f"¿Quisiste decir '{result['suggestion']}'?")
    print(f"Similitud: {result['similarity']:.0%}")
```

### Parámetros Incorrectos

```python
result = agent.process_natural_request("Mueve a una posición inválida")

if not result['success']:
    print(f"Error en parámetros: {result['error']}")
    if 'missing_params' in result:
        print(f"Faltantes: {result['missing_params']}")
```

---

## 📋 Comandos Disponibles (29 Total)

### 🧊 Primitivas (3)

| Comando Usuario | Handler | Descripción |
|-----------------|---------|-------------|
| `crear_cubo` | `blender.create_cube` | Crea cubo 3D |
| `crear_esfera` | `blender.create_sphere` | Crea esfera 3D |
| `crear_cilindro` | `blender.create_cylinder` | Crea cilindro 3D |
| `crear_plano` | `blender.create_plane` | Crea plano 3D |

**Ejemplo:**
```python
agent.execute_via_router('blender.create_cube', {
    'location': [0, 0, 0],
    'scale': 1.5,
    'name': 'MiCubo'
})
```

### 🔄 Transformaciones (3)

| Comando | Handler | Parámetros |
|---------|---------|------------|
| `mover_objeto` | `blender.move_object` | `object_name`, `location` [x,y,z] |
| `rotar_objeto` | `blender.rotate_object` | `object_name`, `rotation` [x,y,z] |
| `escalar_objeto` | `blender.scale_object` | `object_name`, `scale` |

**Ejemplo:**
```python
agent.execute_via_router('blender.move_object', {
    'object_name': 'Cube',
    'location': [5, 0, 2]
})
```

### 🎨 Materiales (3)

| Comando | Handler | Uso |
|---------|---------|-----|
| `crear_material` | `blender.create_material` | Nuevo material básico |
| `crear_material_textura` | `blender.create_texture_material` | Material con imagen PNG |
| `aplicar_material` | `blender.apply_material` | Aplicar a objeto |
| `color_material` | `blender.set_material_color` | Cambiar color |

### 💡 Iluminación (3)

| Comando | Handler | Tipos de Luz |
|---------|---------|--------------|
| `crear_luz` | `blender.create_light` | SUN, POINT, SPOT, AREA |
| `energia_luz` | `blender.set_light_energy` | Ajustar intensidad |
| `color_luz` | `blender.set_light_color` | Color RGB |

**Ejemplo:**
```python
agent.execute_via_router('blender.create_light', {
    'light_type': 'SUN',
    'energy': 5.0,
    'name': 'LuzSolar'
})
```

### 📷 Cámaras (3)

| Comando | Handler |
|---------|---------|
| `crear_camara` | `blender.create_camera` |
| `camara_activa` | `blender.set_active_camera` |
| `posicionar_camara` | `blender.position_camera` |

### ⚙️ Modificadores (3)

| Comando | Handler | Efecto |
|---------|---------|--------|
| `subdivision` | `blender.add_subdivision_surface` | Suavizar geometría |
| `array` | `blender.add_array` | Duplicar en patrón |
| `bevel` | `blender.add_bevel` | Redondear bordes |

### 📤 Exportación (3)

| Comando | Handler | Formato |
|---------|---------|---------|
| `exportar_fbx` | `blender.export_fbx` | Autodesk FBX |
| `exportar_obj` | `blender.export_obj` | Wavefront OBJ |
| `exportar_gltf` | `blender.export_gltf` | glTF 2.0 |

### 🏗️ Assembly - Fase 20 (4)

| Comando | Handler | Descripción |
|---------|---------|-------------|
| `construir_estructura` | `blender.build_structure` | Edificios complejos |
| `guardar_patron` | `blender.save_pattern` | Guardar para reusar |
| `cargar_patron` | `blender.load_pattern` | Cargar patrón guardado |
| `listar_patrones` | `blender.list_patterns` | Ver disponibles |

### 💾 Sistema (3)

| Comando | Handler |
|---------|---------|
| `renderizar` | `blender.render_scene` |
| `obtener_info_sistema` | `system.get_info` |
| `guardar_proyecto` | `blender.save_project` |

---

## 🧪 ZULY LAB: Ingeniería Inversa y Síntesis

ZULY cuenta con un laboratorio avanzado para "aprender" de modelos existentes y crear versiones mejoradas.

### 1. Extracción de ADN (Scan & Learn)
Permite a ZULY analizar un `.blend` y extraer su topología, modificadores y materiales de forma atómica.
- **Uso**: `ZULY, analiza este edificio y aprende sus patrones`.
- **Destino**: El ADN se guarda en `knowledge_base/patterns/learned/`.

### 2. Síntesis Urbana Validada
Reconstruye estructuras complejas basándose en el ADN extraído anteriormente.
- **Alta Fidelidad**: Utiliza dimensiones exactas y parámetros de modificadores reales (Array, Mirror, Bevel).
- **Validación V3**: El sistema realiza una auditoría geométrica automática (Watertightness, Non-manifold edges) antes de dar por finalizado el modelo.
- **Salida**: Los archivos resultantes se alojan en `ZULY_PROJECTS/pruebas/`.

### 3. Organización de Activos
Para evitar confusiones, los archivos se clasifican en:
- **Ejemplos**: Archivos de origen para ingeniería inversa.
- **Pruebas**: Modelos generados procedimentalmente por ZULY.

---

## 📝 Ejemplos Completos

### Ejemplo 1: Lenguaje Natural - Escena Completa

```python
from core.agent import Agent

agent = Agent(force_mock=False, auto_monitor=True)

# Usar lenguaje natural para crear toda una escena
peticion = """
Necesito una escena con:
- Un cubo de oro en el centro
- Una esfera plateada a la derecha  
- Iluminación solar desde arriba
- Una cámara bien posicionada
"""

result = agent.process_natural_request(peticion)
print(result['feedback'])

# Verificar resultados
if result['success']:
    summary = agent.scene_monitor.get_scene_summary()
    print(f"\n✓ Escena creada:")
    print(f"  Objetos: {summary['object_count']}")
    print(f"  Luces: {summary['light_count']}")
    print(f"  Cámaras: {summary['camera_count']}")
```

### Ejemplo 2: Comandos Directos - Escena Básica

```python
from core.agent import Agent

# Inicializar
agent = Agent(force_mock=False)

# Crear objetos
agent.execute_via_router('blender.create_cube', {'location': [0,0,0]})
agent.execute_via_router('blender.create_light', {'light_type': 'SUN'})
agent.execute_via_router('blender.create_camera', {'location': [7,-7,5]})

# Guardar
import bpy
bpy.ops.wm.save_as_mainfile(filepath=r'C:\Users\Admin\Desktop\ZULY_IA_LOCAL\ZULY_PROJECTS\mi_escena.blend')
```

### Ejemplo 3: Material y Transformación (Híbrido)

```python
# Lenguaje natural para crear
agent.process_natural_request("Crea un cubo rojo")

# Comandos directos para transformar
agent.execute_via_router('blender.move_object', {
    'object_name': 'Cube',
    'location': [2, 0, 0]
})

agent.execute_via_router('blender.scale_object', {
    'object_name': 'Cube',
    'scale': 2.0
})
```

### Ejemplo 4: Validación y Exportación

```python
# Crear escena via lenguaje natural
agent.process_natural_request("Crea un cubo")
agent.process_natural_request("Añade una luz solar")
agent.process_natural_request("Crea una cámara")

# Validar requisitos
requisitos = {'object': 1, 'light': 1, 'camera': 1}
satisfied, problems = agent.scene_monitor.has_required_elements(requisitos)

if satisfied:
    # Exportar
    agent.execute_via_router('blender.export_fbx', {
        'filepath': r'C:\Users\Admin\Desktop\ZULY_IA_LOCAL\export\escena.fbx'
    })
    
    # Reporte de sesión
    report_path = agent.export_session_report()
    print(f"Reporte guardado en: {report_path}")
else:
    print(f"Faltan elementos: {problems}")
```

### Ejemplo 5: Debugging con NLU

```python
# Ver qué entiende ZULY de tu petición
texto = "Crea un cubo grande y rojo"
intents = agent.nlu.process(texto)

for intent in intents:
    print(f"\nComando: {intent.command_name}")
    print(f"Confianza: {intent.confidence:.0%}")
    print(f"Parámetros extraídos: {intent.parameters}")

# Luego ejecutar si estás conforme
result = agent.process_natural_request(texto)
```

---

## 💡 Mejores Prácticas

### 1. Preferir Lenguaje Natural para Simplicidad

```python
# ✓ BIEN - Claro y natural
agent.process_natural_request("Crea un cubo dorado en el centro")

# ✗ EVITAR - Innecesariamente técnico para casos simples  
agent.execute_via_router('blender.create_cube', {
    'location': [0,0,0],
    'material': 'gold'
})
```

### 2. Usar Comandos Directos para Precisión

```python
# ✓ BIEN - Cuando necesitas control exacto
agent.execute_via_router('blender.move_object', {
    'object_name': 'Cube',
    'location': [5.234, -2.891, 1.567]
})

# ✗ EVITAR - Lenguaje natural no es preciso aquí
agent.process_natural_request("Mueve el cubo a 5.234, -2.891, 1.567")
```

### 3. Monitorear Escena con auto_monitor=True

```python
# ✓ BIEN - Seguimiento automático
agent = Agent(auto_monitor=True)

result = agent.process_natural_request("Crea un cubo")
print(f"Escena actualizada: {result['scene_state']}")
```

### 4. Validar Resultados Siempre

```python
result = agent.process_natural_request("...")

if result['success']:
    print(f"✓ {result['feedback']}")
else:
    print(f"✗ Error: {result['error']}")
    if 'suggestion' in result:
        print(f"  Sugerencia: {result['suggestion']}")
```

### 5. Exportar Reportes al Final

```python
# Al terminar tu sesión de trabajo
report = agent.export_session_report()
print(f"Sesión documentada en: {report}")

# El reporte sirve para:
# - Auditoría de cambios
# - Debugging de problemas
# - Aprendizaje del sistema
```

---

## 🔧 Arquitectura del Sistema

### Flujo de Ejecución

```
Usuario/Script
    ↓
Agent.execute_via_router()
    ↓
IntentRouter.command_handlers['blender.create_cube']
    ↓
create_cube_handler(params, BlenderAdapter)
    ↓
BlenderAdapter.create_primitive()
    ↓
bpy.ops.mesh.primitive_cube_add()  ← Blender API
    ↓
✓ Cubo creado
```

### Componentes Principales

1. **Agent** (`core/agent.py`)
   - Cerebro principal
   - Gestiona IntentRouter
   - Logging y observabilidad

2. **IntentRouter** (`core/intents/intent_router.py`)
   - Enruta comandos a handlers
   - 29 handlers registrados

3. **BlenderAdapter** (`core/adapters/blender_adapter.py`)
   - Interfaz con Blender API
   - Desacoplamiento (Fase 17)

4. **Handlers** (`core/commands/blender_handlers/`)
   - Funciones específicas
   - Primitivas, transformaciones, etc.

---

## 🔐 Llave de Identidad y Portabilidad

### ¿Qué es `.zuly_identity.key`?

**La llave de identidad es el UUID único que identifica tu instalación de ZULY.**

**Ubicación**: `C:\Users\Admin\Desktop\ZULY_IA_LOCAL\.zuly_identity.key`  
**Contenido**: `17a08a21-8eef-41b5-ac6b-bbd620a45fa4`

**Importante**:
- ✅ Esta llave vincula todas las acciones de ZULY a tu identidad
- ✅ Sin ella, ZULY entra en "bloqueo ético" y no funciona
- ⚠️ **NUNCA la subas a Git ni la compartas públicamente**

---

### 🗝️ Protocolo de Bóveda USB (Portabilidad)

**¿Por qué necesitas esto?**  
Si quieres usar ZULY en otro equipo (portátil, USB, otra PC), **necesitas copiar esta llave** para mantener la continuidad de identidad.

#### Opción A: Respaldo en USB (Recomendado)

**Paso 1: Crear carpeta en USB**
```
F:\ZULY_VAULT\
```

**Paso 2: Copiar la llave**
```powershell
# Desde ZULY_IA_LOCAL
Copy-Item ".zuly_identity.key" "F:\ZULY_VAULT\.zuly_identity.key"
```

**Paso 3: Usar en otro equipo**
Cuando copies ZULY a otro equipo:
1. Copia toda la carpeta `ZULY_IA_LOCAL`
2. Copia `.zuly_identity.key` desde tu USB a la raíz del proyecto
3. ZULY funcionará con la misma identidad en el nuevo equipo

#### Opción B: Respaldo en Teléfono

```
1. Conecta tu teléfono a la PC
2. Copia .zuly_identity.key a una carpeta segura en el móvil
3. Úsalo como backup si pierdes el archivo
```

#### Opción C: Máxima Seguridad (USB como Llave Física)

Para que ZULY **SOLO funcione con tu USB conectado**:

```powershell
# 1. Copiar llave a USB
Copy-Item ".zuly_identity.key" "F:\ZULY_VAULT\.zuly_identity.key"

# 2. Borrar del proyecto (¡SOLO SI TIENES EL BACKUP!)
Remove-Item ".zuly_identity.key"
```

Ahora ZULY buscará la llave en:
1. Raíz del proyecto (no la encontrará)
2. **Unidades USB en `X:\ZULY_VAULT\`** ← La encontrará aquí

**Sin el USB = ZULY no funciona** = Máxima seguridad 🔒

---

### 📋 Checklist de Portabilidad

**Cuando muevas ZULY a otro equipo:**

- [ ] Copiar carpeta completa `ZULY_IA_LOCAL`
- [ ] Copiar `.zuly_identity.key` (desde USB o backup)
- [ ] Instalar Python 3.10+ en nuevo equipo
- [ ] Crear virtualenv: `python -m venv .venv`
- [ ] Activar: `.venv\Scripts\activate` (Windows)
- [ ] Instalar dependencias: `pip install -r requirements.txt`
- [ ] Verificar identidad: ZULY debe arrancar normalmente

**Resultado**: ZULY funciona igual en el nuevo equipo, manteniendo toda su historia y configuración.

---

### ⚠️ Recuperación de Emergencia

**Si perdiste `.zuly_identity.key`:**

1. **Busca en tus backups**: USB, teléfono, copias viejas
2. **Si no la encuentras**: ZULY generará una nueva identidad
   - ⚠️ Perderás la continuidad histórica
   - Necesitarás reconfigurarlo
3. **Prevención**: Siempre ten 2+ copias de la llave

**Script de backup automático**:
```powershell
# Ejecutar al final de cada sesión
.\herramientas\backup_zuly.ps1
```

---

## 🛠️ Solución de Problemas

### Error: "IntentRouter no inicializado"

**Causa**: Agent no fue inicializado correctamente

**Solución**:
```python
agent = Agent(force_mock=False)  # Para Blender real
# o
agent = Agent(force_mock=True)   # Para simulación
```

### Error: "Handler no encontrado"

**Causa**: Nombre de handler incorrecto

**Solución**:
```python
# Ver handlers disponibles
print(list(agent.intent_router.command_handlers.keys()))

# Usar nombre correcto
agent.execute_via_router('blender.create_cube', {...})  # ✓
agent.execute_via_router('crear_cubo', {...})           # ✗
```

### Blender no responde

**Verificar ruta**:
```python
import os
path = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe"
print(f"Existe: {os.path.exists(path)}")
```

---

## 📚 Recursos

### Scripts Útiles

- `run_zuly_blender_real.ps1` - Ejecutar con Blender
- `test_zuly_blender_real.py` - Test de integración
- `verify_mappings.py` - Verificar comandos

### Documentación

- `manuales/README.md` - Índice de manuales
- `bitacora/` - Historial de sesiones
- `walkthrough.md` - Guía técnica detallada

### Carpetas Importantes

- `ZULY_PROJECTS/` - Tus archivos `.blend`
- `ZULY_PROJECTS/pruebas/` - **Resultados de pruebas reales** (incluye escenas de dado y otras síntesis)
- `ZULY_PROJECTS/ejemplos/` - Modelos de referencia (p. ej. `casarural.blend`, `edificio_2.blend`)
- `export/` - Exportaciones (FBX, OBJ, etc.)
- `core/` - Código fuente ZULY
- `tests/` - Tests automatizados

---

## Dados de prueba: dónde están y cómo ejecutarlos

### Carpeta fija de resultados

Todas las escenas `.blend` generadas por los scripts de **dado** del proyecto se guardan en:

```
ZULY_IA_LOCAL/ZULY_PROJECTS/pruebas/
```

Ruta absoluta típica en este equipo:

```
C:\Users\Admin\Desktop\ZULY_IA_LOCAL\ZULY_PROJECTS\pruebas\
```

**Nota:** Los scripts bajo `scripts/` declaran `PROJECT_ROOT = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL"`. Si moviste el proyecto a otra carpeta, debes actualizar esa constante al inicio de cada script que ejecutes.

### Archivos `.blend` de dado (referencia rápida)

| Salida `.blend` | Script que la genera (desde la raíz del repo) |
|-----------------|-----------------------------------------------|
| `dados_reales_zuly.blend` | `scripts/zuly_realistic_dice.py` |
| `dados_reales_zuly_v2.blend` | `scripts/zuly_perfect_dice.py` |
| `dados_reales_zuly_v3.blend` | `scripts/zuly_god_dice.py` |
| `dado_parques_zuly.blend` | `scripts/zuly_parques_dice.py` (línea de trabajo “Parqués” V4 en logs) |
| `dado_parques_zuly_v5.blend` | `scripts/zuly_parques_dice_v5.py` |
| `dado_parques_zuly_v6.blend` | `scripts/zuly_parques_dice_v6.py` |
| `dado_parques_zuly_v7.blend` | `scripts/zuly_parques_dice_v7.py` |
| `dado_parques_zuly_v8.blend` | `scripts/zuly_parques_dice_v8.py` |
| `dado_parques_zuly_v9.blend` | `scripts/zuly_parques_dice_v9.py` |
| `dado_blanco_pips_multicolor.blend` | `scripts/zuly_parques_dice_multicolor.py` (cuerpo blanco, puntos de color distinto por cara) |

**Patrón / receta:** `knowledge_base/patterns/learned/dado_blanco_pips_multicolor_recipe.json` (`handler_recipe`). Incluye `blender.apply_modifier` (`apply_last` o `modifier_name`), `blender.add_boolean` con `material_mode` (p. ej. `TRANSFER`), `blender.add_weighted_normal` y `blender.delete_object`, además de primitivas y materiales.

Otros `.blend` en `pruebas/` (escultura, torre, urban_synthesis, etc.) suelen provenir de `scripts/zuly_synthesis_*.py`, `urban_synthesis_*.py` o sesiones guardadas; este apartado se centra en los **dados**.

### Cómo ejecutar estas pruebas (Blender real)

Los scripts importan `bpy` y `Agent(force_mock=False)`: **no** se ejecutan con el Python del sistema aislado; hay que lanzarlos **con el Blender del proyecto**.

1. Abre PowerShell y sitúate en la raíz del repo:
   ```powershell
   cd C:\Users\Admin\Desktop\ZULY_IA_LOCAL
   ```
2. Define la ruta al ejecutable (misma que en el resto del manual):
   ```powershell
   $BLENDER = "C:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe"
   ```
3. Ejecuta el script deseado en segundo plano (ejemplo: dado Parqués V9):
   ```powershell
   & $BLENDER --background --python "scripts\zuly_parques_dice_v9.py"
   ```
4. Comprueba el archivo generado:
   ```powershell
   Get-Item "ZULY_PROJECTS\pruebas\dado_parques_zuly_v9.blend"
   ```

**Requisitos:** `.zuly_identity.key` en la raíz del proyecto (protocolo de identidad) y dependencias del proyecto accesibles desde el `sys.path` que inserta cada script (`PROJECT_ROOT`).

**Alternativa:** Abrir Blender en modo gráfico, cargar el `.blend` que quieras revisar desde `ZULY_PROJECTS\pruebas\`, o ejecutar el mismo `.py` desde *Scripting* si ajustas rutas; el flujo recomendado para reproducir la prueba es el comando `--background --python` anterior.

---

## ✅ Verificación del Sistema

Ejecuta este script para verificar que todo funciona:

```python
from core.agent import Agent

print("Iniciando verificación...")

agent = Agent(force_mock=True)  # Simulación

tests = [
    ('blender.create_cube', {'location': [0,0,0]}),
    ('blender.create_light', {'light_type': 'SUN'}),
    ('blender.create_camera', {}),
]

for handler, params in tests:
    result = agent.execute_via_router(handler, params)
    status = "✓" if result['success'] else "✗"
    print(f"{status} {handler}")

print(f"\nHandlers disponibles: {len(agent.intent_router.command_handlers)}")
print("Sistema verificado correctamente")
```

---

## 📞 Soporte

### Logs del Sistema

```
bitacora/zuly_agent.log
```

---

## 🧪 ZULY Lab: Entrenamiento y Validación

ZULY Lab es el sistema de entrenamiento práctico y validación técnica. Permite ejecutar ejercicios predefinidos para asegurar que el motor de ZULY funciona correctamente.

### Estructura de ZULY Lab
```
ZULY_LAB/
├── A_estructura/       # Fase A: Primitivas y layouts básicos
├── B_automatizacion/   # Fase B: Scripts procedurales y loops
├── C_render_tecnico/   # Fase C: Texturizado y Render Avanzado ✅
├── resultados_zuly/    # ✅ Aquí se guardan tus .blend y .png
└── logs_sesiones/      # Reportes de éxito/fallo JSON
```

### Cómo Ejecutar Ejercicios

Puedes ejecutar ejercicios desde la consola (PowerShell/CMD):

```bash
# 1. Ejecutar un ejercicio específico
python zuly_lab.py run A1.1

# 2. Ejecutar toda una Fase (Recomendado para validación)
python zuly_lab.py run-all A

# 3. Modo Simulación (Rápido, sin abrir Blender)
python zuly_lab.py run B1.1 --mock
```

### Procedimiento de Validación (Clausura de Fase)

Para garantizar que ZULY está en óptimo estado, se ha validado lo siguiente:

1.  **Limpieza de Escena (`clear_scene`)**: Cada ejercicio inicia con una escena 100% limpia. Esto evita errores de nombres duplicados y acumulación de memoria.
2.  **Generación Procedural (Fase B)**:
    - **ADN Spiral (B1.1)**: Crea una doble hélice matemática.
    - **Ciudad (B1.2)**: Genera edificios aleatorios.
    - **Árbol Fractal (B1.3)**: Geometría recursiva orgánica.
    - **Partenón (B1.4)**: Arquitectura clásica precisa.

### Resultados de Fase A y B (2026-02-22)

| Fase | Ejercicios | Estado | Resultados en |
|------|------------|--------|---------------|
| A | 4/4 | ✅ 100% | `ZULY_LAB/resultados_zuly/A1.*` |
| B | 4/4 | ✅ 100% | `ZULY_LAB/resultados_zuly/B1.*` |
| C | 1/1 | ✅ 100% | `ZULY_LAB/resultados_zuly/C1.1*` |

> [!NOTE]
> Todos los renders finales de la Fase B se generan en resolución **Full HD (1920x1080)** y se almacenan en la carpeta de resultados.

---

### Reportar Problemas

1. Revisa logs en `bitacora/`
2. Ejecuta tests: `pytest tests/`
3. Consulta `walkthrough.md` para detalles técnicos

---

## 📜 Historial de Versiones

**v2.0 - 2026-02-14**
- ✅ Fase 23 completada
- ✅ 29 handlers funcionales
- ✅ IntentRouter integrado
- ✅ Blender 3.6.0 incluido
- ✅ Sistema 100% operacional

**v1.0 - 2026-01-03**
- Core v1.0 STABLE congelado
- Sistema de comandos básico
- NLU inicial

---

**Fecha de creación**: 2026-02-14  
**Última actualización**: 2026-02-22  
**Estado**: Activo y mantenido

---

## ⚠️ Notas Importantes de Laboratorio (ZULY_LAB)

### Rutas Exactas en Ejercicios

Cuando edites o crees nuevos ejercicios `.yaml` en `ZULY_LAB`, ten en cuenta cómo Blender maneja las rutas de archivos:

1.  **Raíz de Ejecución**: Blender se ejecuta desde la carpeta raíz del proyecto (`ZULY_IA_LOCAL`).
2.  **Rutas Relativas**: Todas las rutas de salida (`filepath` en `save_project` o exportaciones) deben ser relativas a esta raíz.

**Ejemplo Correcto:**
```yaml
  - action: "save_project"
    params:
      # CORRECTO: Incluye la carpeta ZULY_LAB
      filepath: "ZULY_LAB/resultados_zuly/mi_ejercicio.blend"
```

**Ejemplo Incorrecto:**
```yaml
  - action: "save_project"
    params:
      # INCORRECTO: Blender intentará guardar en la raíz del proyecto
      filepath: "resultados_zuly/mi_ejercicio.blend"
```

### Argumentos de Línea de Comandos

El sistema `zuly_lab.py` está diseñado para filtrar automáticamente los argumentos de Blender. Si ejecutas manualmente, recuerda usar el separador `--` para pasar argumentos al script de Python:

```powershell
# Sintaxis: blender [opciones_blender] -- [opciones_script]
& "...\blender.exe" --background --python zuly_lab.py -- run A1.1
```

---

## 🧪 12. Pruebas Unitarias de ZULY_LAB

> **Implementadas**: 2026-02-22 · **Estado**: ✅ 80/80 pasando

Las pruebas unitarias del ZULY_LAB corren **sin Blender real** usando el `MockAdapter`.
Se encuentran en `tests/` junto al resto del sistema de tests de ZULY.

### Archivos de Prueba

| Archivo | Tests | Qué cubre |
|---------|-------|-----------|
| `tests/test_exercise_runner.py` | 65 | ExerciseRunner completo |
| `tests/test_zuly_lab_cli.py` | 16 | Funciones del CLI |
| **Total** | **80** | **100% sin Blender** |

### Ejecutar las Pruebas

```powershell
# Desde la raíz del proyecto:

# Solo las pruebas de ZULY_LAB
& ".venv\Scripts\python.exe" -m pytest tests/test_exercise_runner.py tests/test_zuly_lab_cli.py -v

# Con resumen corto (más rápido)
& ".venv\Scripts\python.exe" -m pytest tests/test_exercise_runner.py tests/test_zuly_lab_cli.py --tb=short

# Todas las pruebas del proyecto
& ".venv\Scripts\python.exe" -m pytest tests/ -v
```

### Qué Cubre Cada Suite

#### `test_exercise_runner.py`

```
TestExerciseRunnerInit       — Init: crea logs_sesiones/, resultados_zuly/
TestLoadExercise             — Carga de A1.1 a A1.4, B1.1 (YAMLs reales)
TestExecuteStep              — create_cube, sphere, cylinder, plane, move, material, light, camera
TestExecuteExercise          — Ejecución completa de A1.1/A1.2/A1.3, estructura de resultados, logs JSON
TestValidation               — object_exists, object_count, object_at_location, object_scale, material_applied
TestRunAllPhase              — run_all Fase A (4 ejercicios), run_all Fase B
```

#### `test_zuly_lab_cli.py`

```
TestListExercises            — list --phase A/B, sin filtro, conteo de ejercicios
TestShowStats                — stats sin logs, stats con logs existentes
TestValidateExercise         — validate acepta cualquier código, produce output
TestIntegracionCLI           — Estructura física: carpetas A/B/C/D, YAMLs accesibles, A1.1 y B1.1
```

### Requisitos

```powershell
# PyYAML es necesario en el venv (instalado 2026-02-22)
& ".venv\Scripts\python.exe" -m pip install pyyaml
```

### Diseño de las Fixtures

```python
# Todas las pruebas usan MockAdapter (sin Blender)
@pytest.fixture
def agent_mock():
    return Agent(force_mock=True)

# Los YAMLs reales del proyecto se copian a un directorio temporal
# para que los logs no contaminen el proyecto
@pytest.fixture
def tmp_lab_root(tmp_path):
    for fase in ["A_estructura", "B_automatizacion", ...]:
        shutil.copytree(ZULY_LAB_REAL / fase / "ejercicios", tmp_path / fase / "ejercicios")
    return tmp_path
```

### Resultado Esperado

```
platform win32 -- Python 3.13.1, pytest-9.0.2
collected 80 items

tests/test_exercise_runner.py   65 passed
tests/test_zuly_lab_cli.py      16 passed

80 passed in 4.86s
```

---

## 🦾 13. Ejecución con Blender Real (ZULY_LAB)

Para ejecutar los ejercicios de ZULY_LAB con Blender real (generando archivos `.blend`
y renders), usa el Blender integrado en el proyecto:

### Ruta de Blender

```
C:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe
```

### Comandos con Blender Real

```powershell
# Variable de conveniencia
$BLENDER = "C:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe"

# Ejecutar un ejercicio específico
& $BLENDER --background --python zuly_lab.py -- run A1.1

# Ejecutar todos los ejercicios de Fase A
& $BLENDER --background --python zuly_lab.py -- run-all A

# Ejecutar todos los ejercicios de Fase B
& $BLENDER --background --python zuly_lab.py -- run-all B

# Ver lista de ejercicios disponibles
& $BLENDER --background --python zuly_lab.py -- list

# Ver estadísticas de ejecuciones previas
& $BLENDER --background --python zuly_lab.py -- stats
```

### Diferencias: MockAdapter vs BlenderAdapter

| Aspecto | MockAdapter (tests) | BlenderAdapter (real) |
|---------|---------------------|-----------------------|
| Blender | No necesario | Blender 3.6.0 requerido |
| Archivo `.blend` | No se crea | ✅ Se crea en `resultados_zuly/` |
| Archivo PNG (render) | No se crea | ✅ Se crea (ejercicio A1.4) |
| Velocidad | ~5s para 80 tests | Varios minutos por ejercicio |
| Uso | Desarrollo y CI | Validación final y producción |

### Resultados Generados

Después de ejecutar con Blender real, encontrarás los archivos en:

```
ZULY_LAB/
├── resultados_zuly/
│   ├── A1.1_cubo_basico.blend
│   ├── A1.2_columnas.blend
│   ├── A1.3_base_estructura.blend
│   ├── A1.4_altar_completo.blend
│   ├── A1.4_render_altar.png     ← Render render real
│   └── ...
└── logs_sesiones/
    ├── A1.1_20260222_110000.json
    └── ...
```

### Verificar Instalación de PyYAML en Blender

PyYAML debe estar instalado en el Python embebido de Blender:

```powershell
$BLENDER = "C:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe"

# Verificar
& $BLENDER --background --python-expr "import yaml; print('PyYAML OK:', yaml.__version__)"

# Instalar si no está
# (usa el Python de Blender, no el del venv)
$BLENDER_PYTHON = "C:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\3.6\python\bin\python.exe"
& $BLENDER_PYTHON -m pip install pyyaml
```

---

## 🧠 14. Cognición y Memoria (Fase C)

ZULY incluye ahora un sistema de autoevaluación técnica que le permite auditar la calidad de sus resultados.

### Sistema de Cognición (C1)
Cada vez que ZULY realiza un render, el **CognitionCore** analiza el archivo generado.
- **Auditoría**: Verifica que el archivo exista, no esté vacío y tenga un tamaño coherente.
- **Diagnóstico**: En los logs (`ZULY_LAB/logs_sesiones/`), verás la sección `cognition_diagnosis` con el estatus del resultado.

### Memoria Heurística (C2)
ZULY almacena automáticamente las configuraciones que resultan en alta calidad técnica.
- **Ubicación**: `core/cognition/memory/experiences.json`
- **Funcionamiento**: Si un render obtiene una puntuación alta, ZULY guarda los parámetros (motor, resolución, muestras) para sugerirlos en el futuro.

> **Hito del Fuego**: La Fase C1/C2 fue validada con el renderizado de fuego procedural (`EXPERIMENTO_FUEGO_FINAL.png`), logrando una puntuación cognitiva de 0.9 (Éxito Total).

---

## 📁 15. Convención Oficial de Nombres de Archivos

> **Actualizado**: 2026-03-07 — Semana 4 del Plan Maestro  
> **Prioridad**: 🔴 OBLIGATORIO — Todo nuevo archivo de salida debe seguir este estándar.

Esta convención existe para que cualquier archivo generado por ZULY sea **identificable de inmediato**: a qué semana pertenece, qué tipo de prueba representa, y cuándo fue creado. **Sin esto, los resultados se vuelven inútiles a largo plazo.**

---

### 🗂️ Tabla Maestra de Rutas y Patrones

| Tipo de archivo | Carpeta oficial | Patrón de nombre | Quién lo genera |
|-----------------|-----------------|------------------|-----------------|
| Archivo Blender auto-guardado | `ZULY_PROJECTS/` | `zuly_save_YYYYMMDD_HHMMSS.blend` | `save_blend_handler` automático |
| Archivo Blender de prueba de Semana | `ZULY_PROJECTS/` | `FDE_N_<etiqueta>_YYYYMMDD.blend` | Script de prueba de Semana N |
| Archivo Blender de ejercicio Lab | `ZULY_LAB/resultados_zuly/` | `<FASE><NUMERO>_<nombre>.blend` | `ExerciseRunner` (zuly_lab.py) |
| Render PNG de ejercicio Lab | `ZULY_LAB/resultados_zuly/` | `<FASE><NUMERO>_render_<nombre>.png` | `ExerciseRunner` (zuly_lab.py) |
| Log de sesión de Semana | `ZULY_LAB/logs_sesiones/` | `LOG_FDE_N_YYYYMMDD.json` | Script de prueba de Semana N |
| Log de prueba individual | `ZULY_LAB/logs_sesiones/` | `LOG_TEST_<nombre>_YYYYMMDD_HHMMSS.json` | Cualquier script de test |
| Bitácora de sesión | `bitacora/` | `SESION_YYYY-MM-DD_FIN_DE_SEMANA_N_<ETIQUETA>.md` | Manual (redacción) |
| Reporte de estrés | `bitacora/` | `REPORTE_ESTRES_<VERSION>_YYYYMMDD_HHMMSS.md` | Script de estrés |

---

### 🔑 Clave de Abreviaturas

| Abreviatura | Significado | Ejemplo |
|-------------|-------------|---------|
| `FDE_N` | "Fin De semana" número N | `FDE_4` = Semana 4 del Plan Maestro |
| `YYYYMMDD` | Año-Mes-Día compacto | `20260307` = 7 de marzo 2026 |
| `HHMMSS` | Hora-Minuto-Segundo | `173500` = 17:35:00 |
| `<etiqueta>` | Nombre corto descriptivo (sin espacios, usar `_`) | `v2_validator_test` |
| `<FASE><NUMERO>` | Fase y número de ejercicio del Lab | `A1.1`, `B1.3`, `C3.6` |

---

### 📋 Ejemplos Completos por Tipo

#### Archivos `.blend` en `ZULY_PROJECTS/`

```
# Auto-guardado estándar (generado por save_blend_handler):
ZULY_PROJECTS/zuly_save_20260307_173500.blend

# Resultado de la prueba real de la Semana 4:
ZULY_PROJECTS/FDE_4_v2_validator_test_20260307.blend

# Resultado de la prueba real de la Semana 6 (Laboratorio 2.0):
ZULY_PROJECTS/FDE_6_laboratorio_real_20260321.blend
```

#### Logs JSON en `ZULY_LAB/logs_sesiones/`

```
# Log consolidado de toda la sesión de Semana 4:
ZULY_LAB/logs_sesiones/LOG_FDE_4_20260307.json

# Log de un test puntual (V2 bloqueando contexto fuera de Blender):
ZULY_LAB/logs_sesiones/LOG_TEST_v2_block_fuera_contexto_20260307_175000.json

# Log de un test puntual (V2 bloqueo en Edit Mode):
ZULY_LAB/logs_sesiones/LOG_TEST_v2_block_edit_mode_20260307_175500.json
```

#### Archivos generados por `zuly_lab.py`

```
# .blend de ejercicio A1.1:
ZULY_LAB/resultados_zuly/A1.1_cubo_basico.blend

# Render PNG del ejercicio A1.4:
ZULY_LAB/resultados_zuly/A1.4_render_altar.png

# .blend del pabellón C3.6:
ZULY_LAB/resultados_zuly/C3.6_pabellon_modernista.blend
```

#### Bitácoras en `bitacora/`

```
# Bitácora oficial de sessión (siempre este formato):
bitacora/SESION_2026-03-07_FIN_DE_SEMANA_4_VALIDACION_V2.md

# Reporte de estrés:
bitacora/REPORTE_ESTRES_V1_20260301_162912.md
```

---

### ⚠️ Reglas de Oro — Nunca Romper

1. **NUNCA guardar `.blend` fuera de `ZULY_PROJECTS/` o `ZULY_LAB/resultados_zuly/`.**  
   Si un script guarda en la raíz del proyecto o en otro lugar, es un error que debe corregirse.

2. **NUNCA usar espacios en los nombres.** Siempre usar `_` (guión bajo).  
   ❌ `prueba final semana 4.blend`  
   ✅ `FDE_4_prueba_final_20260307.blend`

3. **NUNCA omitir la fecha.** Sin fecha, el archivo es imposible de ordenar y rastrear.

4. **Los logs de Semana (`LOG_FDE_N`) son consolidados:** Un solo archivo JSON por sesión de trabajo, no uno por comando.

5. **Los logs de test individual (`LOG_TEST_`) son granulares:** Uno por cada caso de prueba específico que quieras documentar.

6. **`zuly_lab.py` gestiona sus propias rutas automáticamente.** No cambies las rutas dentro de los archivos YAML de ejercicios a menos que sepas exactamente lo que haces.

---

### 🔍 Cómo Verificar que un Archivo Está en el Lugar Correcto

Antes de dar una prueba por terminada, comprueba que:

```powershell
# ¿El .blend está en ZULY_PROJECTS?
Get-ChildItem "C:\Users\Admin\Desktop\ZULY_IA_LOCAL\ZULY_PROJECTS\" -Filter "*.blend"

# ¿El log JSON de la semana está en logs_sesiones?
Get-ChildItem "C:\Users\Admin\Desktop\ZULY_IA_LOCAL\ZULY_LAB\logs_sesiones\" -Filter "LOG_FDE_*.json"

# ¿El .blend del lab está en resultados_zuly?
Get-ChildItem "C:\Users\Admin\Desktop\ZULY_IA_LOCAL\ZULY_LAB\resultados_zuly\" -Filter "*.blend"
```

Si algún archivo faltante, hay que buscarlo en la raíz del proyecto y moverlo a su lugar correcto.

---

## 🧠 Razonamiento Híbrido y Paradigmas (NUEVO 2026-03-15)

ZULY 2026 ya no solo ejecuta comandos, sino que ajusta su comportamiento según el **paradigma** detectado en tu voz o texto.

### Declarativo vs Procedural
- **Modo Procedural** ("Añade un cubo, luego muévelo a 2,0,0"): ZULY entiende que hay una orden directa y la ejecuta paso a paso.
- **Modo Declarativo** ("Quiero una escena arquitectónica inspirada en el modernismo"): ZULY detecta un "deseo" y activa el componente **C3 (Objetivos Abstractos)**. Este componente descompone tu visión en un plan técnico de varios pasos sin que tú tengas que dictarlos.

### Ajuste Reactivo (Bypass)
En tareas complejas y automatizadas (ZULY LAB), el sistema activa un modo de **Bypass de Diálogo**. Esto permite que ZULY tome decisiones técnicas rápidas (vía **C1/C4**) sin detenerse a pedir aclaraciones por cada parámetro, logrando una fluidez profesional.

---

## 🏗️ Ingeniería Inversa (ZULY LAB - ADN de Blender)

Ahora ZULY puede "aprender" de modelos existentes mediante el análisis de su estructura topológica.

### El Escáner Pasivo (`scan_and_learn`)
Cuando ZULY analiza un archivo, extrae un **Patrón de ADN** que contiene jerarquías, relaciones espaciales y materiales.

**Ubicación de Ejemplos**: 
Los modelos de referencia para ingeniería inversa se alojan en:
`C:\Users\Admin\Desktop\ZULY_IA_LOCAL\ZULY_PROJECTS\laboratorio\`

**Modelos Disponibles**:
1.  **`casarural.blend`**: Estilo arquitectónico campestre (ADN ya extraído).
2.  **`edificio_2.blend`**: Estructura urbana compleja (Listo para escaneo).
3.  **`demo.blend`**: Escena de referencia técnica.

### Cómo usar el ADN aprendido
Una vez que ZULY ha aprendido un patrón, puedes invocarlo para inspirar nuevas creaciones o replicar estilos:

```python
# Ejemplo: Crear algo usando la base de la casa rural
agent.process_natural_request("Crea una estructura usando el patrón aprendido de la casa rural")
```

Los patrones se guardan automáticamente en:
`knowledge_base\patterns\learned\`

---

## ✅ Resumen de Capacidades Cognitivas (Plan C)

| Componente | Función Real | Impacto |
|------------|--------------|---------|
| **C1** | Evaluador de Resultados | ZULY sabe si el comando "quedó bien" en Blender. |
| **C2** | Memoria de Experiencia | ZULY recuerda qué comandos funcionaron antes. |
| **C3** | Objetivos Abstractos | ZULY crea planes complejos desde ideas simples. |
| **C4** | Auto-tuning Procedural | ZULY ajusta parámetros (escala, luz) hasta el éxito. |

---

## 🛠️ Solución de Problemas de Cognición

### ZULY pide aclaración constante
Si ZULY se detiene mucho, asegúrate de estar en una tarea de laboratorio o usa palabras clave decididas como "ejecuta" o "crea". El `IntentManager` ha sido reforzado para ser más proactivo.

### Error en Ingeniería Inversa
El escáner topológico requiere archivos `.blend` compatibles con la versión 3.6. Modelos de versiones mucho más nuevas podrían requerir una actualización del `BlenderAdapter`.

---
**ZULY 2026 - Evolución Cognitiva Completada**
