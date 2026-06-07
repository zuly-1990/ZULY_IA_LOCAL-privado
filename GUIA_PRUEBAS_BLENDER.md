# 🔬 GUÍA: PRUEBAS EN BLENDER

**Fecha:** 8 de Diciembre de 2025  
**Objetivo:** Probar handlers de LYZU en Blender real

---

## ✅ OPCIÓN 1: Ejecución Automática (Recomendado)

### Windows PowerShell

```powershell
cd C:\Users\Admin\Desktop\ZULY_IA_LOCAL
.\blender_run_test.ps1
```

Esto automáticamente:
- 🔍 Detecta Blender instalado
- 🚀 Ejecuta pruebas
- 📊 Muestra resultados

### Linux / Mac

```bash
cd ~/ZULY_IA_LOCAL
bash blender_run_test.sh
```

---

## ✅ OPCIÓN 2: Manual en Blender GUI (Más Control)

### Paso 1: Abrir Blender
```
Abre Blender normalmente
```

### Paso 2: Ir a Scripting
```
Top menu → Scripting
```

### Paso 3: Crear nuevo script
```
+ New (esquina superior)
```

### Paso 4: Copiar código
Copia TODO el contenido de:
```
MANUAL_BLENDER_TEST.py
```

### Paso 5: Ejecutar
```
Alt+P (en la ventana de texto)
```

Verás los resultados en la consola.

---

## ✅ OPCIÓN 3: Línea de Comandos Blender

```bash
# Windows
"C:\Program Files\Blender Foundation\Blender 3.6\blender.exe" --background --python blender_test.py

# Linux
blender --background --python blender_test.py
```

**Flags útiles:**
- `--background`: Sin GUI (más rápido)
- `--python`: Ejecutar script Python
- `--debug`: Ver más detalles
- `--verbose`: Output completo

---

## 🧪 QUÉ SE PRUEBA

### Test 1: Crear Cubo
```
Input: "Crea un cubo"
Esperado: ✅ Cubo en escena en (0,0,0)
```

### Test 2: Crear Esfera
```
Input: "Crea una esfera roja"
Esperado: ✅ Esfera en escena
```

### Test 3: Mover Objeto
```
Acción: cube.location = (5,10,15)
Esperado: ✅ Cubo en posición correcta
```

### Test 4: Rotar Objeto
```
Acción: sphere.rotation_euler = (45°, 45°, 0°)
Esperado: ✅ Esfera rotada
```

### Test 5: Renderizar (Opcional)
```
Input: "Renderiza"
Esperado: ⏳ Render comienza (necesita Blender GUI)
```

---

## 📊 ESPERADO VER

Si todo funciona:

```
======================================================================
PRUEBA EN BLENDER: LYZU Core Handlers
======================================================================

[SETUP] Limpiando escena anterior...
✅ Escena limpia

[1/6] Inicializando LYZU Core...
✅ LYZU inicializado

[2/6] TEST: Crear cubo
----------------------------------------------------------------------
  Input: 'Crea un cubo'
  Intent: crear_cubo
  Confidence: 92%
  ✅ Cubo creado en Blender
     Posición: (0.0, 0.0, 0.0)

[3/6] TEST: Crear esfera roja
----------------------------------------------------------------------
  Input: 'Crea una esfera roja'
  Intent: crear_esfera
  ✅ Esfera creada en Blender
     Posición: (0.0, 0.0, 0.0)

... (más tests) ...

[6/6] RESUMEN FINAL
======================================================================

Objetos en escena:
  • Cube (MESH)
    - Ubicación: (5.0, 10.0, 15.0)
    - Escala: (1.0, 1.0, 1.0)
    - Rotación: (0.0, 0.0, 0.0)
  
  • Sphere (MESH)
    - Ubicación: (0.0, 0.0, 0.0)
    - Escala: (1.0, 1.0, 1.0)
    - Rotación: (0.785, 0.785, 0.0)

======================================================================
✅ PRUEBAS COMPLETADAS EN BLENDER
======================================================================
```

---

## ❌ TROUBLESHOOTING

### Error: "ModuleNotFoundError: No module named 'lyzu_core'"

**Solución:**
Asegúrate que en `blender_test.py`:
```python
zuly_path = Path("C:/Users/Admin/Desktop/ZULY_IA_LOCAL")
```
Apunta a tu carpeta correcta.

### Error: "Blender not found"

**Solución:**
Edita la ruta en `blender_run_test.ps1`:
```powershell
$blender_paths = @(
    "Tu/Ruta/A/Blender/blender.exe",  # ← Cambiar aquí
    ...
)
```

### Error: "ImportError: bpy"

**Posibles causas:**
- Blender no tiene módulo `bpy` (solo en Blender Python)
- Script no está siendo ejecutado dentro de Blender

**Solución:**
Usa Opción 2 (Manual GUI) que garantiza que está en Blender.

---

## 🔍 VERIFICACIÓN MANUAL

Si prefieres verificar sin ejecutar:

### 1. Ver archivos creados
```bash
ls -la core/commands/blender_handlers/
```

Debe mostrar:
```
__init__.py
primitives.py
transforms.py
render.py
system.py
```

### 2. Ver handlers registrados
```python
from lyzu_core import LYZUCore
lyzu = LYZUCore()
handlers = lyzu.intent_router.get_handler_list()
print(handlers)
# Output: {'blender.create_cube': <function>, ...}
```

### 3. Ver intenciones
```python
intents = lyzu.intent_manager.list_intents()
print(intents)
# Output: {'crear_cubo': '...', 'crear_esfera': '...', ...}
```

---

## 📈 SIGUIENTES PASOS

Si todo funciona ✅:
1. [ ] Crear CLI funcional
2. [ ] Integrar Gemini Vision
3. [ ] Implementar feedback loop

Si hay errores ❌:
1. [ ] Revisar logs
2. [ ] Debuggear en Blender console
3. [ ] Reportar issue

---

## 📝 REPORTE DE RESULTADOS

Después de ejecutar, crea reporte en bitácora:
```
bitacora/REPORTE_PRUEBAS_BLENDER_REAL.md
```

Incluye:
- Fecha/hora
- Qué tests pasaron
- Qué tests fallaron
- Objetos creados
- Observaciones

---

**Guía creada:** 8 de Diciembre de 2025  
**Para:** Pruebas de LYZU Core en Blender  
**Estado:** Ready to test
