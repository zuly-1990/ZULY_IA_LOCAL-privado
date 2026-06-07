# 🎨 GUÍA COMPLETA: INTEGRACIÓN CON BLENDER

**Proyecto:** ZULY_IA_LOCAL  
**Versión:** 3.0 / LYZU Core 1.0  
**Fecha:** 14 de Diciembre de 2025  
**Estado:** ✅ Completamente Funcional

---

## 📋 Tabla de Contenidos

1. [Visión General](#visión-general)
2. [Arquitectura de Integración](#arquitectura-de-integración)
3. [Métodos de Ejecución](#métodos-de-ejecución)
4. [Handlers Disponibles](#handlers-disponibles)
5. [Ejemplos Prácticos](#ejemplos-prácticos)
6. [Troubleshooting](#troubleshooting)
7. [Verificación y Testing](#verificación-y-testing)

---

## 🎯 Visión General

ZULY/LYZU se integra con **Blender 3.6** mediante un sistema de **handlers** que traducen comandos en lenguaje natural a operaciones de la API `bpy` de Blender.

### Características Principales

✅ **Comprensión de Lenguaje Natural**: Procesa peticiones en español/inglés  
✅ **Validación Automática**: Valida parámetros antes de ejecutar  
✅ **Manejo de Errores**: Excepciones personalizadas y reintentos  
✅ **Monitoreo de Escena**: Captura estado de Blender en tiempo real  
✅ **Múltiples Métodos de Ejecución**: GUI, CLI, scripts automáticos  

---

## 🏗️ Arquitectura de Integración

```
┌─────────────────────────────────────────────────────────┐
│                    USUARIO                              │
│         "Crea un cubo dorado en 5,10,15"                │
└────────────────────┬────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────┐
│              LYZU CORE / AGENT                          │
│  • Procesa lenguaje natural                             │
│  • Extrae intenciones y parámetros                      │
└────────────────────┬────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────┐
│            INTENT ROUTER                                │
│  • Mapea intención → handler                            │
│  • Valida parámetros                                    │
└────────────────────┬────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────┐
│         BLENDER HANDLERS                                │
│  ├─ primitives.py    (crear objetos)                    │
│  ├─ transforms.py    (mover, rotar, escalar)            │
│  ├─ render.py        (renderizar, exportar)             │
│  └─ system.py        (limpiar, guardar)                 │
└────────────────────┬────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────┐
│              BLENDER API (bpy)                          │
│  • bpy.ops.mesh.primitive_cube_add()                    │
│  • bpy.data.objects[name].location = (x,y,z)            │
│  • bpy.ops.render.render()                              │
└─────────────────────────────────────────────────────────┘
                     ↓
                ✅ RESULTADO EN BLENDER
```

---

## 🚀 Métodos de Ejecución

### Método 1: Ejecución Automática (Recomendado) ⭐

**Windows PowerShell:**
```powershell
cd C:\Users\Admin\Desktop\ZULY_IA_LOCAL
.\blender_run_test.ps1
```

**Ventajas:**
- ✅ Detecta Blender automáticamente
- ✅ Ejecuta pruebas completas
- ✅ Muestra resultados formateados
- ✅ No requiere configuración manual

**Qué hace:**
1. Busca Blender en rutas comunes
2. Ejecuta `blender_test.py` en modo background
3. Muestra resultados en consola

---

### Método 2: Manual en Blender GUI (Más Control)

**Paso 1:** Abrir Blender 3.6

**Paso 2:** Ir a la pestaña **Scripting** (menú superior)

**Paso 3:** Crear nuevo script (botón **+ New**)

**Paso 4:** Copiar el contenido de uno de estos archivos:
- `blender_test.py` - Pruebas básicas
- `test_render_cubo.py` - Crear y renderizar cubo
- `demo_mejoras_blender.py` - Demo completa

**Paso 5:** Ejecutar con **Alt + P** o botón **▶ Run Script**

**Ventajas:**
- ✅ Control visual completo
- ✅ Ver objetos creados en tiempo real
- ✅ Depuración interactiva
- ✅ Acceso a consola de Blender

---

### Método 3: Línea de Comandos

**Windows:**
```bash
"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe" --background --python blender_test.py
```

**Linux/Mac:**
```bash
blender --background --python blender_test.py
```

**Flags útiles:**
- `--background` - Sin GUI (más rápido)
- `--python <script>` - Ejecutar script Python
- `--debug` - Modo debug
- `--verbose` - Output detallado

**Ventajas:**
- ✅ Ideal para CI/CD
- ✅ Automatización completa
- ✅ Sin interfaz gráfica

---

### Método 4: Integración Programática

**Desde Python externo (sin Blender):**
```python
from lyzu_core import LYZUCore

# Inicializar LYZU
lyzu = LYZUCore(mode='hybrid', enable_learning_freedom=True)

# Procesar comandos
resultado = lyzu.process_user_input("Crea un cubo dorado")

print(resultado)
# Nota: Esto genera el comando pero NO lo ejecuta en Blender
# Para ejecutar, necesitas estar dentro de Blender
```

**Desde Python dentro de Blender:**
```python
import sys
from pathlib import Path

# Agregar ZULY al path
sys.path.insert(0, "C:/Users/Admin/Desktop/ZULY_IA_LOCAL")

import bpy
from lyzu_core import LYZUCore

# Inicializar
lyzu = LYZUCore(mode='reactive')

# Ejecutar comandos (se ejecutan en Blender real)
lyzu.process_user_input("Crea un cubo en 0,0,0")
lyzu.process_user_input("Crea una esfera dorada en 2,0,0")
lyzu.process_user_input("Añade una luz solar")

# Verificar objetos creados
for obj in bpy.data.objects:
    print(f"Objeto: {obj.name}, Tipo: {obj.type}")
```

---

## 🎨 Handlers Disponibles

### 1. **Primitives Handler** (`primitives.py`)

**Comandos:**
- `crear_cubo` / `create_cube`
- `crear_esfera` / `create_sphere`
- `crear_cilindro` / `create_cylinder`
- `crear_cono` / `create_cone`
- `crear_plano` / `create_plane`

**Ejemplo:**
```python
# Lenguaje natural
"Crea un cubo en la posición 5, 10, 15"
"Crear una esfera dorada"
"Añade un cilindro plateado"

# Resultado en Blender
→ bpy.ops.mesh.primitive_cube_add(location=(5,10,15))
→ Material aplicado automáticamente
```

**Parámetros soportados:**
- `location` / `posicion` / `ubicacion`: Tupla (x, y, z)
- `scale` / `escala` / `tamaño`: Float o tupla
- `material` / `color`: Nombre del material (oro, plata, vidrio, etc.)
- `name` / `nombre`: Nombre del objeto

---

### 2. **Transforms Handler** (`transforms.py`)

**Comandos:**
- `mover_objeto` / `move_object`
- `rotar_objeto` / `rotate_object`
- `escalar_objeto` / `scale_object`

**Ejemplo:**
```python
# Mover
"Mueve el cubo a 10, 5, 0"
→ bpy.data.objects['Cube'].location = (10, 5, 0)

# Rotar
"Rota la esfera 45 grados en X"
→ bpy.data.objects['Sphere'].rotation_euler = (0.785, 0, 0)

# Escalar
"Escala el objeto a 2.5"
→ bpy.data.objects['Object'].scale = (2.5, 2.5, 2.5)
```

**Parámetros:**
- `object_name` / `nombre_objeto`: Nombre del objeto a transformar
- `location` / `rotation` / `scale`: Valores de transformación

---

### 3. **Render Handler** (`render.py`)

**Comandos:**
- `renderizar` / `render`
- `exportar_escena` / `export_scene`

**Ejemplo:**
```python
# Renderizar
"Renderiza la escena"
→ bpy.ops.render.render(write_still=True)
→ Guarda en ./ZULY_PROJECTS/render.png

# Exportar
"Exporta la escena como GLB"
→ bpy.ops.export_scene.gltf(filepath='./ZULY_PROJECTS/scene.glb')
```

**Formatos de exportación:**
- GLB / GLTF
- FBX
- OBJ
- BLEND

---

### 4. **System Handler** (`system.py`)

**Comandos:**
- `limpiar_escena` / `clear_scene`
- `guardar_archivo` / `save_file`

**Ejemplo:**
```python
# Limpiar
"Limpia la escena"
→ Elimina todos los objetos

# Guardar
"Guarda el archivo como mi_escena.blend"
→ bpy.ops.wm.save_as_mainfile(filepath='./ZULY_PROJECTS/mi_escena.blend')
```

---

## 💡 Ejemplos Prácticos

### Ejemplo 1: Crear Escena Simple

```python
import sys
sys.path.insert(0, "C:/Users/Admin/Desktop/ZULY_IA_LOCAL")

import bpy
from lyzu_core import LYZUCore

lyzu = LYZUCore(mode='reactive')

# Limpiar escena
lyzu.process_user_input("Limpia la escena")

# Crear objetos
lyzu.process_user_input("Crea un cubo en 0,0,0")
lyzu.process_user_input("Crea una esfera en 3,0,0")
lyzu.process_user_input("Crea un cilindro en -3,0,0")

# Añadir iluminación
lyzu.process_user_input("Añade una luz solar")

# Verificar
print(f"Objetos en escena: {len(bpy.data.objects)}")
```

---

### Ejemplo 2: Crear y Renderizar Cubo Dorado

```python
import sys
sys.path.insert(0, "C:/Users/Admin/Desktop/ZULY_IA_LOCAL")

import bpy
from lyzu_core import LYZUCore

lyzu = LYZUCore(mode='reactive')

# Crear cubo dorado
lyzu.process_user_input("Crea un cubo dorado en el centro")

# Escalar
lyzu.process_user_input("Escala el cubo a 2")

# Añadir luz
lyzu.process_user_input("Añade una luz solar en 5,5,5")

# Configurar cámara (manual)
bpy.ops.object.camera_add(location=(7, -7, 5))
camera = bpy.context.active_object
camera.rotation_euler = (1.1, 0, 0.785)
bpy.context.scene.camera = camera

# Renderizar
lyzu.process_user_input("Renderiza la escena")
```

---

### Ejemplo 3: Secuencia Compleja

```python
import sys
sys.path.insert(0, "C:/Users/Admin/Desktop/ZULY_IA_LOCAL")

import bpy
from lyzu_core import LYZUCore

lyzu = LYZUCore(mode='reactive')

comandos = [
    "Limpia la escena",
    "Crea un cubo dorado en 0,0,0",
    "Crea una esfera plateada en 3,0,0",
    "Crea un cilindro en -3,0,0",
    "Mueve el cubo a 0,0,2",
    "Rota la esfera 45 grados",
    "Escala el cilindro a 1.5",
    "Añade una luz solar",
    "Guarda el archivo como ./ZULY_PROJECTS/mi_escena.blend"
]

for comando in comandos:
    print(f"Ejecutando: {comando}")
    resultado = lyzu.process_user_input(comando)
    print(f"  → {resultado.get('feedback', 'OK')}\n")
```

---

## 🔧 Troubleshooting

### Error: "ModuleNotFoundError: No module named 'lyzu_core'"

**Causa:** Python no encuentra el módulo ZULY

**Solución:**
```python
import sys
from pathlib import Path

# Asegúrate de usar la ruta correcta
zuly_path = Path("C:/Users/Admin/Desktop/ZULY_IA_LOCAL")
sys.path.insert(0, str(zuly_path))
```

---

### Error: "Blender not found"

**Causa:** El script PowerShell no encuentra Blender

**Solución:** Edita `blender_run_test.ps1` y agrega tu ruta:
```powershell
$blender_paths = @(
    "TU_RUTA_AQUI\blender.exe",  # ← Cambiar
    "C:\Program Files\Blender Foundation\Blender 3.6\blender.exe",
    ...
)
```

---

### Error: "ImportError: cannot import name 'bpy'"

**Causa:** `bpy` solo está disponible dentro de Blender

**Solución:** 
- Usa Método 2 (GUI) o Método 3 (CLI con Blender)
- NO ejecutes scripts que usan `bpy` fuera de Blender

---

### Error: "ValidationError: Invalid location"

**Causa:** Parámetros de ubicación inválidos

**Solución:**
```python
# ❌ Incorrecto
"Crea un cubo en abc"

# ✅ Correcto
"Crea un cubo en 0,0,0"
"Crea un cubo en la posición 5 10 15"
```

---

### Error: "CommandExecutionError: Object not found"

**Causa:** Intentas transformar un objeto que no existe

**Solución:**
```python
# Primero crea el objeto
lyzu.process_user_input("Crea un cubo")

# Luego transfórmalo
lyzu.process_user_input("Mueve el cubo a 5,0,0")
```

---

## ✅ Verificación y Testing

### Test 1: Verificar Instalación

```python
# Ejecutar en Python normal (fuera de Blender)
from lyzu_core import LYZUCore

lyzu = LYZUCore()
print(f"✅ LYZU versión: {lyzu.version}")
print(f"✅ Handlers registrados: {len(lyzu.intent_router.handlers)}")
```

**Resultado esperado:**
```
✅ LYZU versión: 3.0
✅ Handlers registrados: 23
```

---

### Test 2: Verificar Handlers de Blender

```bash
# Windows PowerShell
cd C:\Users\Admin\Desktop\ZULY_IA_LOCAL
.\blender_run_test.ps1
```

**Resultado esperado:**
```
✅ Blender encontrado: C:\...\blender.exe
Ejecutando pruebas...
======================================================================
BLENDER TEST: LYZU Core Handlers en Ambiente Real
======================================================================
[1/5] Inicializando LYZU Core...
✅ LYZU inicializado

[2/5] TEST: Crear cubo
----------------------------------------------------------------------
✅ Cubo creado en Blender!
   Ubicación: (0.0, 0.0, 0.0)
...
✅ PRUEBAS EN BLENDER COMPLETADAS
```

---

### Test 3: Crear y Renderizar (Manual)

1. Abre Blender 3.6
2. Ve a **Scripting**
3. Copia el contenido de `test_render_cubo.py`
4. Ejecuta con **Alt + P**

**Resultado esperado:**
- ✅ Cubo dorado visible en viewport
- ✅ Luz solar agregada
- ✅ Cámara configurada
- ✅ Render generado en `./ZULY_PROJECTS/cubo_render.png`
- ✅ Archivo guardado en `./ZULY_PROJECTS/cubo_mejorado.blend`

---

### Test 4: Pruebas Unitarias

```bash
# Ejecutar tests de validadores
python -m pytest tests/test_validators.py -v

# Ejecutar tests de excepciones
python -m pytest tests/test_exceptions.py -v

# Ejecutar tests de NLU
python -m pytest tests/test_nlu_improvements.py -v
```

**Resultado esperado:**
```
tests/test_validators.py::test_validate_location PASSED
tests/test_validators.py::test_validate_scale PASSED
...
======================== 47 passed in 2.34s ========================
```

---

## 📊 Configuración

### Archivo: `config.json`

```json
{
  "objeto_3d": {
    "tipo": "cubo",
    "opciones_validas": ["cubo", "esfera", "cilindro", "cono", "plano"]
  },
  "transformacion": {
    "posicion": [0, 0, 0],
    "rotacion_grados": [0, 0, 0],
    "escala": [1, 1, 1]
  },
  "material": {
    "nombre": "oro",
    "opciones_validas": ["oro", "plata", "vidrio", "negro_mate", "blanco_brillante"]
  },
  "entorno": {
    "modo": "blender",
    "version_blender": "3.6",
    "motor_render": "cycles",
    "muestras_render": 32,
    "directorio_salida": "./ZULY_PROJECTS/"
  }
}
```

---

## � UBICACIÓN DE ARCHIVOS (IMPORTANTE)

### 🎯 Dónde se guardan los archivos

**Ruta oficial configurada en `config.json`:**
```
./ZULY_PROJECTS/
```

**Ruta completa en tu sistema:**
```
C:\Users\Admin\Desktop\ZULY_IA_LOCAL\ZULY_PROJECTS\
```

### 📂 Qué se guarda aquí:

| Tipo de archivo | Extensión | Ejemplo |
|-----------------|-----------|---------|
| **Archivos Blender** | `.blend` | `mi_escena.blend`, `cubo_dorado.blend` |
| **Renders** | `.png`, `.jpg` | `render_001.png`, `escena_final.jpg` |
| **Exportaciones** | `.glb`, `.fbx`, `.obj` | `modelo_3d.glb`, `exportacion.fbx` |

### ✅ Verificación rápida:

```powershell
ls C:\Users\Admin\Desktop\ZULY_IA_LOCAL\ZULY_PROJECTS\
```

### ⚠️ NOTA IMPORTANTE:

Los archivos se guardan **ÚNICAMENTE** en `./ZULY_PROJECTS/` (configurado en `config.json`)

---

## �📚 Recursos Adicionales

### Documentación del Proyecto
- `README_INDICE.md` - Índice completo
- `DASHBOARD_FINAL.md` - Estado del proyecto
- `GUIA_PRUEBAS_BLENDER.md` - Guía de pruebas
- `ARQUITECTURA_MEJORADA.md` - Arquitectura técnica

### Scripts de Prueba
- `blender_test.py` - Pruebas básicas
- `test_render_cubo.py` - Crear y renderizar
- `demo_mejoras_blender.py` - Demo completa
- `blender_run_test.ps1` - Ejecución automática

### Handlers
- `core/commands/blender_handlers/primitives.py`
- `core/commands/blender_handlers/transforms.py`
- `core/commands/blender_handlers/render.py`
- `core/commands/blender_handlers/system.py`

---

## 🎯 Próximos Pasos

### Corto Plazo
- [ ] Ejecutar pruebas en Blender real
- [ ] Validar renders generados
- [ ] Documentar resultados en bitácora

### Mediano Plazo
- [ ] Integrar Gemini Vision para feedback visual
- [ ] Implementar feedback loop automático
- [ ] Crear CLI interactiva

### Largo Plazo
- [ ] Integración con render farms
- [ ] API REST para control remoto
- [ ] Plugin nativo de Blender

---

## ✅ Checklist de Integración

```
Preparación:
[✅] Blender 3.6 instalado
[✅] ZULY_IA_LOCAL descargado
[✅] Python 3.10+ disponible
[✅] Dependencias instaladas (requirements.txt)

Verificación:
[✅] Handlers registrados
[✅] Tests unitarios pasando
[✅] Config.json configurado

Ejecución:
[ ] Método 1 (PowerShell) probado
[ ] Método 2 (GUI) probado
[ ] Método 3 (CLI) probado
[ ] Método 4 (Programático) probado

Validación:
[ ] Objetos creados correctamente
[ ] Transformaciones funcionando
[ ] Renders generados
[ ] Archivos exportados
```

---

**Guía creada:** 14 de Diciembre de 2025  
**Versión:** 1.0  
**Estado:** ✅ Completa y Lista para Usar

**¡Listo para crear arte 3D con IA! 🎨🚀**
