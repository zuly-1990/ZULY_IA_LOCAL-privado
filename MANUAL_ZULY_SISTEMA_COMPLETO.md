# 📖 MANUAL ZULY - SISTEMA COMPLETO
**Versión:** 2.0  
**Fecha:** 31 de Marzo de 2026  
**Fase:** 18.5 - Control de Complejidad  
**Estado:** ✅ OPERACIONAL

---

## 📋 TABLA DE CONTENIDOS

1. [Rutas Críticas](#rutas-críticas)
2. [Estructura de Directorios](#estructura-de-directorios)
3. [Ejecución de ZULY CLI](#ejecución-de-zuly-cli)
4. [Ciclo de Guardado de .BLEND](#ciclo-de-guardado-de-blend)
5. [Handlers Disponibles](#handlers-disponibles)
6. [Troubleshooting](#troubleshooting)

---

## 🗺️ RUTAS CRÍTICAS

### 1. BLENDER EJECUTABLE
```
RUTA COMPLETA:
c:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe

VERSIÓN:     Blender 3.6.0
MOTOR:       Cycles (por defecto)
ESTADO:      ✅ Instalado y listo
```

### 2. ZULY CLI (Interfaz Principal)
```
RUTA COMPLETA:
c:\Users\Admin\Desktop\ZULY_IA_LOCAL\zuly_cli_v2.py

EJECUCIÓN:
  Modo MOCK (simulado):
    python zuly_cli_v2.py

  Modo BLENDER REAL:
    python zuly_cli_v2.py --real

  Un solo comando:
    python zuly_cli_v2.py --real -c "crear un cubo"
```

### 3. ARCHIVOS .BLEND PROYECTOS
```
DIRECTORIO PRINCIPAL:
c:\Users\Admin\Desktop\ZULY_IA_LOCAL\ZULY_PROJECTS\

SUBDIRECTORIOS:
  ├─ /pruebas/                      ← Pruebas unitarias
  ├─ /laboratorio/                  ← Experimentos
  ├─ /demo_blender/                 ← Demostraciones
  ├─ /ejemplos/                     ← Ejemplos de uso
  ├─ /proyecto_casa_tutorial/       ← Tutorial casas
  └─ /proyecto_prueba_estandar/     ← Tests estándar

ARCHIVOS PRINCIPALES:
  • dado_2.blend                    (Proyecto activo)
  • dado_perfecto_final.blend       (Finalizado)
  • prueba_usuario_20260330.blend   (Último test)
```

### 4. EXPORTACIÓN Y RENDERS
```
DIRECTORIO SALIDA:
c:\Users\Admin\Desktop\ZULY_IA_LOCAL\export\

CONTENIDO:
  ├─ *.blend                        ← Proyectos exportados
  ├─ *.png                          ← Renders generados
  ├─ *.obj                          ← Modelos OBJ
  ├─ *.fbx                          ← Modelos FBX
  └─ *.gltf                         ← Modelos GLTF
```

### 5. CONFIGURACIÓN GLOBAL
```
ARCHIVO CONFIG:
c:\Users\Admin\Desktop\ZULY_IA_LOCAL\config.json

PARÁMETROS PRINCIPALES:
  {
    "entorno": {
      "directorio_salida": "./export/",
      "motor_render": "cycles",
      "muestras_render": 32,
      "escena": "default"
    },
    "logs": {
      "nivel": "INFO",
      "archivo": "./logs/proceso.log"
    }
  }
```

### 6. REGISTROS Y LOGS
```
DIRECTORIO LOGS:
c:\Users\Admin\Desktop\ZULY_IA_LOCAL\logs\

ARCHIVOS PRINCIPALES:
  • proceso.log                     ← Log del sistema
  • trace.txt                       ← Traza de ejecución
  • debug_*.txt                     ← Debug específicos
```

### 7. CORE DEL AGENTE
```
DIRECTORIO CORE:
c:\Users\Admin\Desktop\ZULY_IA_LOCAL\core\

MÓDULOS:
  ├─ agent.py                       ← Agente principal (Agent class)
  ├─ adapters/
  │   ├─ blender_adapter.py         ← Conexión real a Blender
  │   └─ mock_adapter.py            ← Simulación fallback
  ├─ commands/
  │   ├─ blender_handlers/          ← 48 handlers de Blender
  │   └─ blender_commands.py        ← Comandos registrados
  ├─ intents/
  │   └─ intent_router.py           ← Router de intenciones
  ├─ utils/
  │   ├─ nlu.py                     ← Procesador de lenguaje natural
  │   └─ logging.py                 ← Sistema de logging
  ├─ cognition/
  │   └─ cognition_core.py          ← Motor de cognición
  ├─ learning/
  │   └─ learning_freedom_engine.py ← Motor de aprendizaje
  └─ execution/
      ├─ failsafe_executor.py       ← Ejecución segura
      └─ safe_executor.py           ← Executor base
```

---

## 📂 ESTRUCTURA DE DIRECTORIOS COMPLETA

```
c:\Users\Admin\Desktop\ZULY_IA_LOCAL\
│
├─ 🐍 SCRIPTS PRINCIPALES
│  ├─ zuly_cli_v2.py               ← ⭐ CLI PRINCIPAL
│  ├─ zuly_cli.py                  ← CLI alternativo
│  ├─ lanzar_blender_zuly.py       ← Lanzador Blender real
│  └─ lyzu_core.py                 ← Core LYZU
│
├─ 📁 CORE (Sistema de IA)
│  └─ core/
│     ├─ agent.py                  ← Agente central
│     ├─ adapters/                 ← Adaptadores
│     ├─ commands/                 ← Handlers (48 total)
│     ├─ intents/                  ← Intent routing
│     ├─ utils/                    ← Utilidades (NLU, logging)
│     ├─ cognition/                ← Motor de cognición
│     ├─ learning/                 ← Motor de aprendizaje
│     ├─ execution/                ← Ejecutores seguros
│     ├─ diagnostics/              ← Monitoreo de escena
│     └─ tests/                    ← Tests unitarios
│
├─ 📁 BLENDER (Instalación local)
│  └─ blender/
│     └─ v3/
│        └─ blender-3.6.0-zuly/
│           ├─ blender.exe         ← ⭐ EJECUTABLE
│           ├─ 3.6/
│           └─ [recursos Blender]
│
├─ 📁 PROYECTOS Y ARCHIVOS .BLEND
│  └─ ZULY_PROJECTS/               ← ⭐ ALMACÉN .BLEND
│     ├─ dado_2.blend
│     ├─ dado_perfecto_final.blend
│     ├─ prueba_usuario_20260330.blend
│     ├─ pruebas/
│     ├─ laboratorio/
│     ├─ demo_blender/
│     ├─ ejemplos/
│     ├─ proyecto_casa_tutorial/
│     └─ proyecto_prueba_estandar/
│
├─ 📁 EXPORTACIÓN Y RENDERS
│  ├─ export/                      ← ⭐ SALIDA .PNG, .OBJ, .FBX
│  └─ exports/                     ← Alternativo
│
├─ 📁 ALMACENAMIENTO Y MEMORIA
│  ├─ memory/                      ← Memoria de patrones
│  ├─ patterns/                    ← Patrones aprendidos
│  ├─ knowledge_base/              ← Base de conocimiento
│  └─ ZULY_LAB/                    ← Laboratorio experimental
│
├─ 📁 DOCUMENTACIÓN Y MANUALES
│  ├─ manuales/                    ← Guías (si existen)
│  ├─ docs/                        ← Documentación técnica
│  ├─ MANUAL_ZULY_SISTEMA_COMPLETO.md  ← ⭐ ESTE ARCHIVO
│  ├─ ARCHITECTURE_RULES.md        ← Reglas de arquitectura
│  ├─ ARQUITECTURA_MEJORADA.md     ← Diseño del sistema
│  ├─ MAPEO_COMPONENTES.txt        ← Mapeo de componentes
│  ├─ COMPARACION_ARQUITECTURAS.txt
│  └─ RESOLUTION_TECNICA_COMPLETA_ZULY.txt
│
├─ 📁 LOGS Y REGISTROS
│  ├─ logs/                        ← Logs del sistema
│  ├─ bitacora/                    ← Bitácora de avance
│  └─ BITACORA_DE_AVANCE/          ← Histórico
│
├─ 🎬 RECURSOS Y DATOS
│  ├─ assets_3d/                   ← Modelos 3D
│  ├─ blender_support/             ← Soporte Blender
│  ├─ blender_training_data.json   ← Datos entrenamiento
│  └─ laboratorio_metadata.json    ← Metadata laboratorio
│
├─ ⚙️ CONFIGURACIÓN
│  ├─ config.json                  ← ⭐ CONFIG GLOBAL
│  ├─ .zuly_identity.key           ← Identidad ZULY
│  └─ requirements.txt             ← Dependencias Python
│
├─ 🧪 TESTS Y VALIDACIÓN
│  ├─ tests/                       ← Suite de tests
│  ├─ core/tests/                  ← Tests core
│  └─ test_*.py                    ← Tests individuales
│
└─ 🐍 ENTORNO VIRTUAL
   └─ .venv/                       ← Virtual environment Python
```

---

## ▶️ EJECUCIÓN DE ZULY CLI

### Opción 1: Inicialiación Normal (Terminal Interactiva)

```bash
cd c:\Users\Admin\Desktop\ZULY_IA_LOCAL

# Activar virtual environment (si aún no está activado)
.venv\Scripts\Activate.ps1

# Ejecutar en BLENDER REAL
python zuly_cli_v2.py --real
```

**Resultado:**
```
🤖 ZULY CLI - Sistema de Agente Inteligente para Blender
======================================================================

⏳ Inicializando agente...

✓ Agente listo | Modo: BLENDER REAL

🤖 zuly> 
```

### Opción 2: Comando Único Directo

```bash
python zuly_cli_v2.py --real -c "crear un cubo"
```

**Salida:** 
- Ejecuta el comando
- Guarda automáticamente en `ZULY_PROJECTS/`
- Render en `export/`
- Exit automático

### Opción 3: Prueba en MOCK MODE (Simulado)

```bash
python zuly_cli_v2.py
```

No requiere Blender instalado. Simula todas las acciones.

---

## 💾 CICLO DE GUARDADO DE .BLEND

### Flujo Automático Completo

```
┌─────────────────────────────────────────────────────────────────┐
│ 1. USER INPUT (CLI)                                             │
│    zuly> crear un cubo de 2 metros                              │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ 2. NLU PROCESSING                                               │
│    • Procesamiento de lenguaje natural                          │
│    • Extracción de intención y parámetros                       │
│    └─→ CommandIntent(command="create_cube", params={...})      │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ 3. INTENT ROUTING                                               │
│    • 48 handlers disponibles                                    │
│    • Búsqueda fuzzy matching si es necesario                   │
│    └─→ blender.create_cube handler                             │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ 4. HANDLER EXECUTION                                            │
│    • BlenderAdapter conecta a Blender real                      │
│    • Si falla → MockAdapter ejecuta fallback                    │
│    └─→ Cubo creado en escena                                   │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ 5. AUTOMATIC SAVE                                               │
│    ✅ Archivo .blend guardado en:                               │
│       ZULY_PROJECTS/cubo_TIMESTAMP.blend                        │
│                                                                 │
│    ✅ Render PNG guardado en:                                   │
│       export/cubo_TIMESTAMP.png                                 │
│                                                                 │
│    ✅ Trace guardado en:                                        │
│       logs/proceso.log                                          │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ 6. USER FEEDBACK                                                │
│    ✅ ÉXITO                                                     │
│    └─ Comando: blender.create_cube                              │
│    └─ Confianza: 95%                                            │
│    └─ Estado: Cubo creado y guardado                            │
└─────────────────────────────────────────────────────────────────┘
```

### Ubicaciones de Guardado por Tipo

| Tipo | Ubicación | Patrón |
|------|-----------|--------|
| **Proyecto .blend** | `ZULY_PROJECTS/` | `{nombre}_{YYYYMMDD_HHMMSS}.blend` |
| **Render PNG** | `export/` | `{nombre}_{YYYYMMDD_HHMMSS}.png` |
| **Modelos OBJ** | `export/` | `{nombre}.obj` |
| **Modelos FBX** | `export/` | `{nombre}.fbx` |
| **Modelos GLTF** | `export/` | `{nombre}.gltf` |
| **Log detallado** | `logs/` | `proceso.log` |
| **Traza ejecución** | App | `trace_core.traces` |

---

## 🎮 HANDLERS DISPONIBLES (48 TOTALES)

### PRIMIIVAS (5)
```
• crear_cubo / create_cube
• crear_esfera / create_sphere
• crear_cilindro / create_cylinder
• crear_plano / create_plane
• crear_cono / create_cone
```

### TRANSFORMACIÓN (3)
```
• mover_objeto / move_object
• rotar_objeto / rotate_object
• escalar_objeto / scale_object
```

### SELECCIÓN (5)
```
• seleccionar_objeto / select_object
• deseleccionar_todo / deselect_all
• seleccionar_por_tipo / select_all_by_type
• eliminar_objeto / delete_object
• duplicar_objeto / duplicate_object
```

### ESCENA (4)
```
• limpiar_escena / clear_scene
• renombrar_objeto / rename_object
• visibilidad_objeto / set_object_visibility
• establecer_padre / set_parent
```

### MATERIALES (4)
```
• crear_material / create_material
• crear_material_textura / create_texture_material
• aplicar_material / apply_material
• establecer_color_material / set_material_color
```

### ILUMINACIÓN (3)
```
• crear_luz / create_light
• establecer_energia_luz / set_light_energy
• establecer_color_luz / set_light_color
```

### CÁMARAS (3)
```
• crear_camara / create_camera
• establecer_camara_activa / set_active_camera
• posicionar_camara / position_camera
```

### MODIFICADORES (5)
```
• agregar_subdivision_surface / add_subdivision_surface
• agregar_array / add_array
• agregar_bisel / add_bevel
• agregar_booleano / add_boolean
• aplicar_modificador / apply_modifier
```

### EXPORTACIÓN (3)
```
• exportar_fbx / export_fbx
• exportar_obj / export_obj
• exportar_gltf / export_gltf
```

### RENDER (1)
```
• renderizar / render_scene
```

### PATRONES (3)
```
• guardar_patron / save_pattern
• cargar_patron / load_pattern
• listar_patrones / list_patterns
```

### DIAGNÓSTICO (1)
```
• escanear_y_aprender / scan_and_learn
```

### SISTEMA (8)
```
• info_sistema / get_system_info
• guardar_blend / save_blend
• guardar_escena / save_scene
• ejecutar_script / run_python_script
• validar_topologia / validate_topology
• construir_estructura / build_structure
• crear_dados / create_parques_dice
• (otros)
```

---

## ⚙️ CONFIGURACIÓN DETALLADA

### config.json - Parámetros

```json
{
  "objeto_3d": {
    "tipo": "cubo",
    "opciones_validas": [
      "cubo", "plano", "esfera", "cilindro", "torus", 
      "mono", "circulo", "cono", "ico_esfera", "uv_esfera"
    ]
  },
  
  "transformacion": {
    "posicion": [0, 0, 0],
    "rotacion_grados": [0, 0, 0],
    "escala": [1, 1, 1]
  },
  
  "material": {
    "nombre": "oro",
    "opciones_validas": [
      "oro", "plata", "negro_mate", "blanco_brillante", 
      "vidrio", "emision_azul", null
    ]
  },
  
  "entorno": {
    "modo": "blender",
    "version_blender": "3.6",
    "motor_render": "cycles",
    "muestras_render": 32,
    "escena": "default",
    "directorio_salida": "./export/"
  },
  
  "logs": {
    "nivel": "INFO",
    "archivo": "./logs/proceso.log",
    "guardar_tiempos": true,
    "guardar_errores": true
  }
}
```

---

## 🔄 SISTEMA DE MONITOREO

### SceneMonitor - Variables de Estado

El `SceneMonitor` captura automáticamente:

```python
{
  "objects": [lista de objetos en escena],
  "lights": [fuentes de luz],
  "cameras": [cámaras disponibles],
  "materials": [materiales aplicados],
  "modifiers": [modificadores activos],
  "render_settings": {
    "engine": "cycles",
    "samples": 32,
    "resolution": [1920, 1080]
  }
}
```

Acceso:
```bash
zuly> estado
# Imprime reporte completo del sistema
```

---

## 🐛 TROUBLESHOOTING

### Problema 1: "BlenderAdapter: bpy no disponible"

**Síntoma:**
```
WARNING  [LYZU] ⚠️ BlenderAdapter: bpy no disponible (Blender no detectado)
WARNING  [LYZU] ⚠️ BlenderAdapter no disponible (bpy no encontrado)
INFO     [LYZU] 🔧 Usando MockAdapter (fallback)
```

**Solución:**
Blender se está ejecutando en fallback (MockAdapter). Puedes:
- Continuar en MOCK MODE (simulación)
- Lanzar Blender por separado: `lanzar_blender_zuly.py`
- O verificar la ruta: `c:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe`

---

### Problema 2: "Archivo .blend no se guarda"

**Verificar:**
1. ¿Existe `ZULY_PROJECTS/`?
   ```bash
   Test-Path c:\Users\Admin\Desktop\ZULY_IA_LOCAL\ZULY_PROJECTS
   ```

2. ¿Permisos de escritura?
   ```bash
   Get-Acl c:\Users\Admin\Desktop\ZULY_IA_LOCAL\ZULY_PROJECTS
   ```

3. ¿Espacio en disco?
   ```bash
   Get-Volume c:
   ```

---

### Problema 3: "Handler no encontrado"

**Comando:**
```bash
zuly> patrones
# Lista todos los 48 handlers disponibles

zuly> estado
# Verifica estado de handlers
```

---

### Problema 4: "Error en render"

**Verificar config.json:**
```json
"motor_render": "cycles",
"muestras_render": 32,
"directorio_salida": "./export/"
```

**Logs detallados:**
```bash
cat c:\Users\Admin\Desktop\ZULY_IA_LOCAL\logs\proceso.log
```

---

## 📞 CONTACTO Y SOPORTE

**Para reportar problemas o sugerencias:**

1. Revisar logs: `logs/proceso.log`
2. Ejecutar diagnóstico: `python diagnostico_zuly.py`
3. Verificar sistema: `python validate_zuly_system.py`
4. Consultar bitácora: `bitacora/` (histórico de cambios)

---

**✅ Manual actualizado: 31 de Marzo de 2026**
