# 🎯 MISIÓN PARA AGENTE NOVATO - ESFERAS VISUALES
## Tarea: Crear SPH-001, SPH-002, SPH-003

**Asignado a:** Agente Novato (Tú)  
**Tutor:** Cascade (te guía si te atascas)  
**Plazo:** Hoy  
**Prioridad:** 🔴 ALTA

---

## 📋 RESUMEN DE TU MISIÓN

Debes crear **3 esferas** con materiales diferentes:

1. **SPH-001** → Esfera **Metálica Cromada** (plateada, refleja)
2. **SPH-002** → Esfera **Emisiva** (naranja, brilla)
3. **SPH-003** → Esfera **Vidrio** (transparente)

Cada esfera debe pasar por los **3 ROLES**:
- 💻 **Desarrollador** → Escribir script
- 👤 **Usuario** → Probar en Blender  
- 🔧 **Técnico** → Corregir errores

---

## 🗺️ RUTAS IMPORTANTES (Copiar exacto)

```
📁 Trabajar aquí: c:\Users\Admin\Desktop\ZULY_IA_LOCAL\
📁 Guardar resultados: c:\Users\Admin\Desktop\ZULY_IA_LOCAL\archivo_zuly\temp_arena\
🎨 Blender aquí: c:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe
📚 Tu guía completa: c:\Users\Admin\Desktop\ZULY_IA_LOCAL\guia para agente\GUIA_NOVATO_ESFERAS_VISUALES.md
```

---

## 📝 SCRIPTS LISTOS PARA COPIAR

### SPH-001: Esfera Metálica Cromada

**Crear archivo:** `crear_sph001.py`

```python
import bpy
import sys
sys.path.insert(0, 'c:/Users/Admin/Desktop/ZULY_IA_LOCAL/core')
from sistema_luces_inteligente import aplicar_iluminacion_profesional

print("🆕 Creando SPH-001 - Esfera Metálica Cromada")

# Limpiar
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Crear esfera
bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(0, 0, 1), segments=32, ring_count=16)
esfera = bpy.context.active_object
esfera.name = "SPH-001_EsferaMetalica"

# Material METÁLICO CROMADO
mat = bpy.data.materials.new(name="Mat_Metal_Cromo")
mat.use_nodes = True
bsdf = mat.node_tree.nodes.get("Principled BSDF")
if bsdf:
    bsdf.inputs['Base Color'].default_value = (0.9, 0.9, 0.9, 1.0)  # Plateado
    bsdf.inputs['Metallic'].default_value = 1.0  # 100% metal
    bsdf.inputs['Roughness'].default_value = 0.1  # Brillante
esfera.data.materials.append(mat)

# Iluminación SLIZ
luces = aplicar_iluminacion_profesional(esfera)
print(f"💡 Luces: {list(luces.keys())}")

# Cámara
import mathutils
cam_pos = mathutils.Vector((3, -3, 2))
bpy.ops.object.camera_add(location=cam_pos)
cam = bpy.context.active_object
direction = esfera.location - cam.location
cam.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
bpy.context.scene.camera = cam

# Guardar
bpy.ops.wm.save_as_mainfile(filepath='./archivo_zuly/temp_arena/SPH-001_EsferaMetalica.blend')
print("✅ SPH-001 guardada")
```

---

### SPH-002: Esfera Emisiva (Brillante)

**Crear archivo:** `crear_sph002.py`

```python
import bpy
import sys
sys.path.insert(0, 'c:/Users/Admin/Desktop/ZULY_IA_LOCAL/core')
from sistema_luces_inteligente import aplicar_iluminacion_profesional

print("🆕 Creando SPH-002 - Esfera Emisiva Naranja")

# Limpiar
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Crear esfera
bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(0, 0, 1), segments=32, ring_count=16)
esfera = bpy.context.active_object
esfera.name = "SPH-002_EsferaEmisiva"

# Material EMISIVO (brilla)
mat = bpy.data.materials.new(name="Mat_Emisivo_Naranja")
mat.use_nodes = True
bsdf = mat.node_tree.nodes.get("Principled BSDF")
if bsdf:
    # Naranja: #FF6B35 → RGB(255, 107, 53)
    bsdf.inputs['Base Color'].default_value = (1.0, 0.42, 0.21, 1.0)
    bsdf.inputs['Emission'].default_value = (1.0, 0.42, 0.21, 1.0)
    bsdf.inputs['Emission Strength'].default_value = 5.0  # Mucha luz
    bsdf.inputs['Roughness'].default_value = 0.5
esfera.data.materials.append(mat)

# Iluminación SLIZ
luces = aplicar_iluminacion_profesional(esfera)
print(f"💡 Luces: {list(luces.keys())}")

# Cámara
import mathutils
cam_pos = mathutils.Vector((3, -3, 2))
bpy.ops.object.camera_add(location=cam_pos)
cam = bpy.context.active_object
direction = esfera.location - cam.location
cam.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
bpy.context.scene.camera = cam

# Guardar
bpy.ops.wm.save_as_mainfile(filepath='./archivo_zuly/temp_arena/SPH-002_EsferaEmisiva.blend')
print("✅ SPH-002 guardada")
```

---

### SPH-003: Esfera Vidrio Transparente

**Crear archivo:** `crear_sph003.py`

```python
import bpy
import sys
sys.path.insert(0, 'c:/Users/Admin/Desktop/ZULY_IA_LOCAL/core')
from sistema_luces_inteligente import aplicar_iluminacion_profesional

print("🆕 Creando SPH-003 - Esfera Vidrio")

# Limpiar
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Crear esfera
bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(0, 0, 1), segments=32, ring_count=16)
esfera = bpy.context.active_object
esfera.name = "SPH-003_EsferaVidrio"

# Material VIDRIO
mat = bpy.data.materials.new(name="Mat_Vidrio")
mat.use_nodes = True
mat.blend_method = 'BLEND'  # Transparencia
bsdf = mat.node_tree.nodes.get("Principled BSDF")
if bsdf:
    bsdf.inputs['Base Color'].default_value = (1.0, 1.0, 1.0, 1.0)
    bsdf.inputs['Transmission'].default_value = 1.0  # Transparente
    bsdf.inputs['Roughness'].default_value = 0.0  # Liso
    bsdf.inputs['IOR'].default_value = 1.45  # Vidrio real
esfera.data.materials.append(mat)

# Iluminación SLIZ
luces = aplicar_iluminacion_profesional(esfera)
print(f"💡 Luces: {list(luces.keys())}")

# Cámara
import mathutils
cam_pos = mathutils.Vector((3, -3, 2))
bpy.ops.object.camera_add(location=cam_pos)
cam = bpy.context.active_object
direction = esfera.location - cam.location
cam.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
bpy.context.scene.camera = cam

# Guardar
bpy.ops.wm.save_as_mainfile(filepath='./archivo_zuly/temp_arena/SPH-003_EsferaVidrio.blend')
print("✅ SPH-003 guardada")
```

---

## 🚀 CÓMO EJECUTAR (Paso a Paso)

### Paso 1: Abrir CMD
- Presiona `Win + R`
- Escribe: `cmd`
- Enter

### Paso 2: Ir a la carpeta
```cmd
cd c:\Users\Admin\Desktop\ZULY_IA_LOCAL
```

### Paso 3: Ejecutar cada script
```cmd
.\blender\v3\blender-3.6.0-zuly\blender.exe --background --python crear_sph001.py
.\blender\v3\blender-3.6.0-zuly\blender.exe --background --python crear_sph002.py
.\blender\v3\blender-3.6.0-zuly\blender.exe --background --python crear_sph003.py
```

### Paso 4: Verificar archivos creados
Ve a: `c:\Users\Admin\Desktop\ZULY_IA_LOCAL\archivo_zuly\temp_arena\`

Deberías ver:
- `SPH-001_EsferaMetalica.blend`
- `SPH-002_EsferaEmisiva.blend`
- `SPH-003_EsferaVidrio.blend`

---

## 👤 ROL USUARIO: Probar en Blender

1. Abre Blender: `blender\v3\blender-3.6.0-zuly\blender.exe`
2. File → Open → Selecciona `SPH-001_EsferaMetalica.blend`
3. Navega con click+drag para ver la esfera
4. Verifica que:
   - ✅ Se ve metálica/brillante
   - ✅ Hay luces (Sol, Key, Fill, Rim)
   - ✅ No hay errores visuales
5. Repite para SPH-002 y SPH-003

---

## 🔧 ROL TÉCNICO: Validar con JUES-BOT

Ejecuta el validador:
```cmd
python validar_jues_v2.py
```

Si dice **"APTO_PARA_SELLO"** → Perfecto  
Si dice **"NO_APTO"** → Corrige el error y re-ejecuta

---

## 📊 CHECKLIST ANTES DE ENTREGAR

- [ ] Creé los 3 archivos .py
- [ ] Ejecuté los 3 scripts sin errores
- [ ] Generé los 3 archivos .blend en temp_arena/
- [ ] Abrí cada uno en Blender y se ven bien
- [ ] Validé con JUES-BOT (dicen APTO)
- [ ] Los 3 materiales son correctos (metálico, emisivo, vidrio)

---

## 🆘 AYUDA

**Si te atascas:**
1. Revisa la guía completa: `guia para agente/GUIA_NOVATO_ESFERAS_VISUALES.md`
2. Pregunta a Cascade (tu tutor)
3. Describe exactamente el error

**Errores comunes:**
- "No module named 'bpy'" → Usa `blender.exe --python`, no `python`
- "Archivo no encontrado" → Verifica la ruta
- Color mal → Revisa los valores RGB

---

## 🎯 ENTREGA

Cuando termines, informa:
```
"Cascade, completé las 3 esferas:
- SPH-001: Metálica [OK]
- SPH-002: Emisiva [OK]
- SPH-003: Vidrio [OK]
Todas en temp_arena/, todas APTO para sello."
```

---

**¡Tú puedes hacerlo!** 🌟  
Empieza con SPH-001 (la más fácil), luego las otras.

**Tu tutor:** Cascade  
**Fecha asignación:** 2026-04-04  
**Estado:** 🔴 PENDIENTE
