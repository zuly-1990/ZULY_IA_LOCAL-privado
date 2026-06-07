# 🚀 INICIO RÁPIDO: INTEGRACIÓN CON BLENDER

**¿Primera vez usando ZULY con Blender?** Esta guía te llevará de 0 a crear tu primera escena 3D en **5 minutos**.

---

## ⚡ Método Más Rápido (PowerShell)

```powershell
# 1. Abre PowerShell en el directorio del proyecto
cd C:\Users\Admin\Desktop\ZULY_IA_LOCAL

# 2. Ejecuta el script automático
.\blender_run_test.ps1
```

**¡Eso es todo!** El script:
- ✅ Encuentra Blender automáticamente
- ✅ Ejecuta pruebas completas
- ✅ Muestra resultados

---

## 🎨 Método Manual (Control Visual)

### Paso 1: Abre Blender 3.6

### Paso 2: Ve a la pestaña **Scripting**

### Paso 3: Crea nuevo script (botón **+ New**)

### Paso 4: Copia y pega este código:

```python
import sys
from pathlib import Path

# Agregar ZULY al path
sys.path.insert(0, "C:/Users/Admin/Desktop/ZULY_IA_LOCAL")

import bpy
from lyzu_core import LYZUCore

# Inicializar LYZU
lyzu = LYZUCore(mode='reactive')

# Limpiar escena
lyzu.process_user_input("Limpia la escena")

# Crear objetos
lyzu.process_user_input("Crea un cubo dorado en 0,0,0")
lyzu.process_user_input("Crea una esfera plateada en 3,0,0")
lyzu.process_user_input("Añade una luz solar")

# Verificar
print(f"\n✅ Objetos creados: {len(bpy.data.objects)}")
for obj in bpy.data.objects:
    print(f"  • {obj.name} en {tuple(obj.location)}")
```

### Paso 5: Ejecuta con **Alt + P**

**Resultado:** Verás los objetos creados en el viewport 3D de Blender.

---

## 💡 Ejemplos de Comandos

Una vez que LYZU esté inicializado, puedes usar estos comandos:

```python
# Crear primitivas
lyzu.process_user_input("Crea un cubo")
lyzu.process_user_input("Crea una esfera")
lyzu.process_user_input("Crea un cilindro")

# Con posición
lyzu.process_user_input("Crea un cubo en 5,10,15")

# Con material
lyzu.process_user_input("Crea una esfera dorada")
lyzu.process_user_input("Crea un cilindro plateado")

# Transformaciones
lyzu.process_user_input("Mueve el cubo a 10,0,0")
lyzu.process_user_input("Rota la esfera 45 grados")
lyzu.process_user_input("Escala el objeto a 2")

# Iluminación
lyzu.process_user_input("Añade una luz solar")
lyzu.process_user_input("Añade una luz puntual")

# Sistema
lyzu.process_user_input("Limpia la escena")
lyzu.process_user_input("Guarda el archivo como ./ZULY_PROJECTS/mi_escena.blend")
```

---

## 🎯 Crear y Renderizar Cubo Dorado

**Script completo para crear y renderizar:**

```python
import sys
sys.path.insert(0, "C:/Users/Admin/Desktop/ZULY_IA_LOCAL")

import bpy
from lyzu_core import LYZUCore

# Inicializar
lyzu = LYZUCore(mode='reactive')

# Crear escena
lyzu.process_user_input("Limpia la escena")
lyzu.process_user_input("Crea un cubo dorado en 0,0,0")
lyzu.process_user_input("Escala el cubo a 2")
lyzu.process_user_input("Añade una luz solar en 5,5,5")

# Configurar cámara (manual)
bpy.ops.object.camera_add(location=(7, -7, 5))
camera = bpy.context.active_object
camera.rotation_euler = (1.1, 0, 0.785)
bpy.context.scene.camera = camera

# Configurar render
scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.cycles.samples = 64
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080

# Renderizar
scene.render.filepath = "C:/Users/Admin/Desktop/ZULY_IA_LOCAL/ZULY_PROJECTS/cubo.png"
bpy.ops.render.render(write_still=True)

print("✅ Render completado: ZULY_PROJECTS/cubo.png")
```

---

## ❓ Problemas Comunes

### "ModuleNotFoundError: No module named 'lyzu_core'"

**Solución:** Verifica la ruta en `sys.path.insert(0, "...")`:
```python
# Debe apuntar a tu carpeta ZULY_IA_LOCAL
sys.path.insert(0, "C:/Users/Admin/Desktop/ZULY_IA_LOCAL")
```

### "Blender not found" (PowerShell)

**Solución:** Edita `blender_run_test.ps1` línea 6:
```powershell
$blender_paths = @(
    "TU_RUTA_AQUI\blender.exe",  # ← Agregar tu ruta
    ...
)
```

### Los objetos no aparecen

**Solución:** Asegúrate de estar en modo `reactive`:
```python
lyzu = LYZUCore(mode='reactive')  # ← Importante
```

---

## 📚 Documentación Completa

Para más detalles, consulta:

- **Guía Completa:** `guia_integracion_blender.md` (en artifacts)
- **Guía de Pruebas:** `GUIA_PRUEBAS_BLENDER.md`
- **Arquitectura:** `ARQUITECTURA_MEJORADA.md`
- **Dashboard:** `DASHBOARD_FINAL.md`

---

## ✅ Verificación Rápida

**Ejecuta esto en Python (fuera de Blender):**
```python
from lyzu_core import LYZUCore

lyzu = LYZUCore()
print(f"✅ LYZU versión: {lyzu.version}")
print(f"✅ Handlers: {len(lyzu.intent_router.handlers)}")
```

**Resultado esperado:**
```
✅ LYZU versión: 3.0
✅ Handlers: 23
```

---

## 🎉 ¡Listo!

Ya tienes todo configurado. Ahora puedes:

1. ✅ Crear objetos 3D con lenguaje natural
2. ✅ Transformar objetos (mover, rotar, escalar)
3. ✅ Aplicar materiales (oro, plata, vidrio)
4. ✅ Configurar iluminación
5. ✅ Renderizar escenas

**¡Diviértete creando arte 3D con IA! 🎨🚀**

---

**Creado:** 14 de Diciembre de 2025  
**Para:** Inicio rápido con Blender  
**Estado:** ✅ Listo para usar
