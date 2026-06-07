# 🔧 GUÍA: Cómo ZULY se Conecta con Blender

**Documento:** Explicación paso a paso de la arquitectura  
**Fecha:** 30 Marzo 2026  
**Versión:** 1.0

---

## 📊 Diagrama General

```
┌─────────────────────────────────────────────────────────────┐
│                   TÚ (Usuario)                              │
│        Escribes lenguaje natural en español                 │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              ZULY Agent (agent.py)                           │
│  • Procesa lo que escribiste en español (NLU)               │
│  • Convierte a comandos estructurados                       │
│  • Orquesta la ejecución                                    │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│        BlenderAdapter (core/adapters/)                       │
│  • ÚNICO que importa bpy (la API de Blender)                │
│  • Traduce comandos de ZULY a código Blender               │
│  • Envía órdenes al ejecutable de Blender                  │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│         Blender Executable (blender.exe)                    │
│  • Recibe comandos Python (bpy)                             │
│  • Crea objetos 3D, materiales, luces                       │
│  • Renderiza si es necesario                               │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│           SceneMonitor (Observador)                         │
│  • Captura el estado de la escena                           │
│  • Lee qué objetos se crearon                               │
│  • Devuelve feedback al usuario                             │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│             TÚ (Usuario)                                     │
│        Ves el resultado en español claro                    │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎯 Los 4 Componentes Clave

### 1️⃣ **Agent (agent.py)**

**¿Qué hace?**  
Es tu asistente que entiende lo que dices en español

**Ejemplo:**
```python
from core.agent import Agent

agent = Agent()
result = agent.process_natural_request(
    "Crea un cubo dorado en la posición 0, 0, 0"
)
```

**Internamente:**
- Lee: `"Crea un cubo dorado en la posición 0, 0, 0"`
- Interpreta: `→ comando_cubo + material_oro + posicion_(0,0,0)`
- Ordena: `→ BlenderAdapter.create_primitive(...)`

---

### 2️⃣ **BlenderAdapter (core/adapters/blender_adapter.py)**

**¿Qué hace?**  
Es el ÚNICO traductor entre ZULY y Blender

**Cómo funciona:**
```python
class BlenderAdapter(EngineAdapter):
    def __init__(self):
        # INTENTA importar bpy (la API de Blender)
        try:
            import bpy
            self._bpy = bpy  # ✅ Blender disponible
        except:
            self._available = False  # ❌ Blender no está
    
    def create_primitive(self, type='cube', **params):
        # Usa bpy para crear objeto en Blender
        bpy.ops.mesh.primitive_cube_add(...)
        # Lee el objeto creado
        obj = bpy.context.active_object
        # Devuelve info
        return {'success': True, 'object_name': obj.name}
```

**Métodos principales:**
- `create_primitive(cube, sphere, cylinder, etc.)`
- `move_object(nombre, posición)`
- `apply_material(objeto, material)`
- `render_scene()`
- `export_scene(formato)`

---

### 3️⃣ **Blender Executable (blender.exe)**

**Ubicación típica en tu PC:**
```
C:\Program Files\Blender Foundation\Blender 3.6\
└── blender.exe (♦ El ejecutable real)
```

**¿Qué contiene bpy?**  
Blender viene con une Python integrado que expone la API `bpy`:
```
C:\Program Files\Blender Foundation\Blender 3.6\
└── 3.6\
    └── python\
        └── lib\
            └── site-packages\
                └── bpy.py (♦ La API)
```

---

### 4️⃣ **SceneMonitor (core/diagnostics/scene_monitor.py)**

**¿Qué hace?**  
Observa qué pasó después de ejecutar un comando

**Ejemplo:**
```python
monitor = SceneMonitor()
state = monitor.capture_scene_state()
# Retorna:
# {
#   'objects': [{'name': 'Cube', 'type': 'MESH'}, ...],
#   'lights': [...],
#   'materials': [...],
#   'cameras': [...]
# }
```

---

## 🔄 Flujo Completo de Ejecución

### Paso 1: TÚ escribes
```
"Crea un cubo rojo, una esfera azul y una luz"
```

### Paso 2: Agent procesa (NLU)
```python
agent.process_natural_request("Crea un cubo rojo...")
    ↓
NaturalLanguageProcessor.process()
    ↓
Detecta:
  • Intención 1: crear_cubo (confianza: 95%)
  • Intención 2: crear_esfera (confianza: 94%)
  • Intención 3: crear_luz (confianza: 92%)
```

### Paso 3: BlenderAdapter ejecuta
```python
# COMANDO 1: Cubo rojo
adapter.create_primitive(
    type='cube',
    location=[0, 0, 0],
    material='red'
)
    ↓
import bpy
bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
obj = bpy.context.active_object
obj.name = "Cube_Red"
# Aplicar material rojo
    ↓
✅ ÉXITO: "Cube_Red" creado

# COMANDO 2: Esfera azul
adapter.create_primitive(
    type='sphere',
    location=[2, 0, 0],
    material='blue'
)
    ↓
bpy.ops.mesh.primitive_uv_sphere_add(location=(2, 0, 0))
...
    ↓
✅ ÉXITO: "Sphere_Blue" creado

# COMANDO 3: Luz
adapter.add_light(
    type='SUN',
    location=[5, 5, 5]
)
    ↓
bpy.ops.object.light_add(type='SUN', location=(5, 5, 5))
    ↓
✅ ÉXITO: "Sun" creado
```

### Paso 4: SceneMonitor captura estado
```python
monitor.capture_scene_state()
    ↓
bpy.data.objects  # Lee todos los objetos
bpy.data.lights   # Lee todas las luces
bpy.data.materials  # Lee todos los materiales
    ↓
Retorna:
{
  'objects': 3,
  'list': ['Cube_Red', 'Sphere_Blue', 'Sun'],
  'summary': 'Escena actualizada con 3 elementos'
}
```

### Paso 5: TÚ ves resultado
```
✅ ÉXITO - Escena actualizada:
  • Cubo rojo en (0, 0, 0)
  • Esfera azul en (2, 0, 0)
  • Luz solar en (5, 5, 5)
  
Escena total: 3 objetos nuevos
```

---

## ⚙️ Configuración de ZULY

### Archivo: `config.json`

```json
{
  "entorno": {
    "modo": "blender",
    "version_blender": "3.6",
    "motor_render": "cycles",
    "muestras_render": 32,
    "escena": "default",
    "directorio_salida": "./export/"
  }
}
```

### Archivo: `core/adapters/blender_adapter.py`

```python
# Las 3 formas en que BlenderAdapter puede obtener bpy:

# 1. Auto-detección (Recomendado)
adapter = BlenderAdapter()
# Automáticamente intenta: import bpy

# 2. Inyección directa
import bpy
adapter = BlenderAdapter(bpy_module=bpy)

# 3. Modo test (sin Blender real)
adapter = BlenderAdapter(force_mock=True)
# Usa MockAdapter en lugar de BlenderAdapter
```

---

## 🛠️ Rutas Importantes

### Estructura del Proyecto
```
c:\Users\Admin\Desktop\ZULY_IA_LOCAL\
│
├── core/
│   ├── adapters/
│   │   ├── engine_adapter.py       (♦ Interfaz)
│   │   ├── blender_adapter.py      (♦ Conector real)
│   │   └── mock_adapter.py         (♦ Para pruebas)
│   │
│   ├── diagnostics/
│   │   └── scene_monitor.py        (♦ Observador)
│   │
│   └── commands/
│       └── extended_commands.py    (♦ Comandos)
│
├── agent.py                         (♦ Orquestador)
├── config.json                      (♦ Configuración)
│
└── export/                          (♦ Salida)
    ├── renders/
    ├── models/
    └── logs/
```

### Ruta de Blender Executable
```
# Estándar en Windows:
C:\Program Files\Blender Foundation\Blender 3.6\blender.exe

# O en tu PC puede estar en:
c:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe
```

---

## 🧪 Cómo Verificar la Conexión

### Test 1: ¿Está Blender disponible?
```python
from core.adapters.blender_adapter import BlenderAdapter

adapter = BlenderAdapter()
if adapter.is_available():
    print("✅ Blender conectado")
    info = adapter.get_engine_info()
    print(f"Version: {info['version']}")
else:
    print("❌ Blender no disponible")
```

### Test 2: ¿Puedo crear objetos?
```python
result = adapter.create_primitive(
    'cube',
    location=[0, 0, 0],
    scale=1.0
)
if result['success']:
    print(f"✅ Objeto creado: {result['object_name']}")
else:
    print(f"❌ Error: {result['error']}")
```

### Test 3: ¿Puedo monitorear escena?
```python
from core.diagnostics.scene_monitor import SceneMonitor

monitor = SceneMonitor()
state = monitor.capture_scene_state()
print(f"Objetos en escena: {len(state.objects)}")
```

---

## 🎓 Resumen de Capas

| Capa | Archivo | Responsabilidad | Idioma |
|------|---------|-----------------|--------|
| **Usuario** | Tú | Escribir en español | Español |
| **Agent** | `agent.py` | Interpretar español | Python + Lógica IA |
| **Adapter** | `blender_adapter.py` | Traducir a bpy | Python puro |
| **Blender** | `blender.exe` | Ejecutar 3D | bpy (Python Blender) |
| **Monitor** | `scene_monitor.py` | Observar cambios | Python + bpy |

---

## ❓ Preguntas Frecuentes

**P: ¿Necesito instalar nada extra?**  
R: No. Blender ya viene con bpy integrado. ZULY lo detecta automáticamente.

**P: ¿Dónde guarda los archivos?**  
R: En `./export/` según config.json. Puedes cambiar en el archivo.

**P: ¿Qué pasa si Blender no está instalado?**  
R: ZULY automáticamente usa `MockAdapter` (simulación). Funciona igual pero sin 3D real.

**P: ¿Cómo agrego nuevos comandos?**  
R: En `extended_commands.py` creas una clase que herede de `BaseCommand`.

**P: ¿Puedo trabajar sin interfaz gráfica de Blender?**  
R: Sí. Blender puede correr en modo headless (sin ventana). ZULY lo maneja automáticamente.

---

## 🚀 Próximos Pasos

1. **Ejecutar demo:** `python demo_zuly_cli.py`
2. **Usar CLI interactivo:** `python zuly_cli_interactive.py`
3. **Entrenar con Blender real:** `python train_c2_from_blender_real.py`
4. **Ver estado del sistema:** Revisar `system_report()` en Agent

¡Listo! ZULY está conectado y listo para crear 3D con lenguaje natural 🎨
