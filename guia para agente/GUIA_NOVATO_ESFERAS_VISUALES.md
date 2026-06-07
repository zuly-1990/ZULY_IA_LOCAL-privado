# 👶 GUÍA PARA AGENTE NOVATO - APRENDIENDO ZULY DESDE CERO
## Instrucciones Ultra Detalladas - Esferas Visuales SPH-001/002/003

**Para:** Agente sin conocimiento previo de ZULY  
**Fecha:** 2026-04-04  
**Tutor:** Cascade (tu guía)  
**Misión:** Crear 3 esferas con efectos visuales

---

## 🍼 ¿QUÉ ES ZULY? (Explicación para Novatos)

**ZULY** es un sistema que crea objetos 3D en Blender (un programa de diseño 3D).

**Analogía simple:**
- ZULY es como una **fábrica de juguetes 3D**
- Tú eres el **operario** de esa fábrica
- Tu trabajo: crear juguetes (esferas) siguiendo instrucciones
- El jefe final (Soberano/Usuario) aprueba o rechaza los juguetes

**Componentes principales:**
1. **ZULY** - La fábrica que genera objetos
2. **JUES-BOT** - El inspector de calidad
3. **LYZU** - La secretaria que guarda registros
4. **Blender** - El taller donde se construyen los objetos

---

## 🗺️ RUTAS ABSOLUTAS (Copia y Pega Exactas)

### ¿Dónde está todo?

**Carpeta MADRE (todo está aquí):**
```
c:\Users\Admin\Desktop\ZULY_IA_LOCAL\
```

**Blender (el programa 3D):**
```
c:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe
```

**Cerebro del sistema (scripts Python):**
```
c:\Users\Admin\Desktop\ZULY_IA_LOCAL\core\
```

**Arena (donde guardas tus creaciones):**
```
c:\Users\Admin\Desktop\ZULY_IA_LOCAL\archivo_zuly\temp_arena\
```

**Patrones aprobados (aquí van si el jefe dice "OK"):**
```
c:\Users\Admin\Desktop\ZULY_IA_LOCAL\archivo_zuly\por_estado_aprendizaje\mastered\
```

---

## 🔄 EL CICLO DE TRABAJO (Tu Rutina Diaria)

Como agente, tienes **3 TRABAJOS** diferentes. Los harás en orden:

### TRABAJO 1: DESARROLLADOR 💻
**"Escribir la receta de cocina"**

Escribes un script (archivo .py) que le dice a Blender cómo crear un objeto.

**Pasos:**
1. Creas un archivo de texto
2. Le pones extensión .py (ejemplo: crear_esfera.py)
3. Escribes código Python
4. Guardas en `temp_arena/`

**Ejemplo de receta (script):**
```python
import bpy

# Limpiar escena
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Crear esfera
bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(0, 0, 1))
esfera = bpy.context.active_object
esfera.name = "SPH-001_EsferaMetalica"

# Guardar
bpy.ops.wm.save_as_mainfile(filepath='./archivo_zuly/temp_arena/SPH-001.blend')
```

---

### TRABAJO 2: USUARIO 👤
**"Probar el juguete"**

Abres lo que creaste y verificas que se vea bien.

**Pasos:**
1. Abres Blender
2. Vas a File → Open
3. Navegas a `archivo_zuly/temp_arena/`
4. Abres tu archivo .blend
5. Miras alrededor (rotas la vista con click+drag)
6. Verificas: ¿Se ve bien? ¿Hay luces? ¿El color es correcto?

**Si se ve mal:** → Vas al Trabajo 3 (arreglar)
**Si se ve bien:** → Presentas al jefe

---

### TRABAJO 3: TÉCNICO 🔧
**"Arreglar errores"**

Cuando algo falla, tú lo reparas.

**Errores comunes:**
- Color equivocado → Cambias el color en el script
- Luces mal → Reaplicas iluminación
- Geometría fea → Ajustas parámetros

**Pasos:**
1. Lees el reporte de errores
2. Identificas qué está mal
3. Editas tu script .py
4. Vuelves a ejecutar
5. Repites hasta que esté perfecto

---

## 🎯 TU MISIÓN ESPECÍFICA: 3 Esferas Visuales

### Esfera 1: SPH-001 - Esfera Metálica Cromada

**Qué debe tener:**
- Forma: Esfera UV (radio 1 metro)
- Material: Metálico cromado
- Color: Plateado brillante
- Reflejos: Como un espejo

**Especificaciones técnicas:**
```python
# CÓDIGO COMPLETO PARA SPH-001
import bpy

# Limpiar
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Crear esfera
bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(0, 0, 1), segments=32, ring_count=16)
esfera = bpy.context.active_object
esfera.name = "SPH-001_EsferaMetalica"

# Material METÁLICO
mat = bpy.data.materials.new(name="Mat_Metal_Cromo")
mat.use_nodes = True
principled = mat.node_tree.nodes.get("Principled BSDF")
if principled:
    principled.inputs['Base Color'].default_value = (0.9, 0.9, 0.9, 1.0)  # Plateado
    principled.inputs['Metallic'].default_value = 1.0  # 100% metálico
    principled.inputs['Roughness'].default_value = 0.1  # Muy brillante
    principled.inputs['Specular'].default_value = 1.0
esfera.data.materials.append(mat)

# Guardar
bpy.ops.wm.save_as_mainfile(filepath='./archivo_zuly/temp_arena/SPH-001_EsferaMetalica.blend')
print("✅ SPH-001 creada")
```

---

### Esfera 2: SPH-002 - Esfera Emisiva (Que Brilla)

**Qué debe tener:**
- Forma: Esfera UV (radio 1 metro)
- Material: Emisivo (emite luz)
- Color: Naranja cálido (#FF6B35)
- Efecto: Glow/brillo

**Especificaciones técnicas:**
```python
# CÓDIGO COMPLETO PARA SPH-002
import bpy

# Limpiar
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Crear esfera
bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(0, 0, 1), segments=32, ring_count=16)
esfera = bpy.context.active_object
esfera.name = "SPH-002_EsferaEmisiva"

# Material EMISIVO
mat = bpy.data.materials.new(name="Mat_Emisivo_Naranja")
mat.use_nodes = True
principled = mat.node_tree.nodes.get("Principled BSDF")
if principled:
    # Color naranja: #FF6B35 → RGB(255, 107, 53) → Normalizado(1.0, 0.42, 0.21)
    principled.inputs['Base Color'].default_value = (1.0, 0.42, 0.21, 1.0)
    principled.inputs['Emission'].default_value = (1.0, 0.42, 0.21, 1.0)
    principled.inputs['Emission Strength'].default_value = 5.0  # Brilla mucho
    principled.inputs['Roughness'].default_value = 0.5
esfera.data.materials.append(mat)

# Guardar
bpy.ops.wm.save_as_mainfile(filepath='./archivo_zuly/temp_arena/SPH-002_EsferaEmisiva.blend')
print("✅ SPH-002 creada")
```

---

### Esfera 3: SPH-003 - Esfera de Vidrio Transparente

**Qué debe tener:**
- Forma: Esfera UV (radio 1 metro)
- Material: Vidrio/Glass
- Transparencia: Se ve a través
- Refracción: Distorsiona lo de atrás

**Especificaciones técnicas:**
```python
# CÓDIGO COMPLETO PARA SPH-003
import bpy

# Limpiar
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Crear esfera
bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(0, 0, 1), segments=32, ring_count=16)
esfera = bpy.context.active_object
esfera.name = "SPH-003_EsferaVidrio"

# Material VIDRIO
mat = bpy.data.materials.new(name="Mat_Vidrio_Transparente")
mat.use_nodes = True
mat.blend_method = 'BLEND'  # Para transparencia
principled = mat.node_tree.nodes.get("Principled BSDF")
if principled:
    principled.inputs['Base Color'].default_value = (1.0, 1.0, 1.0, 1.0)  # Blanco
    principled.inputs['Transmission'].default_value = 1.0  # 100% transparente
    principled.inputs['Roughness'].default_value = 0.0  # Vidrio liso
    principled.inputs['IOR'].default_value = 1.45  # Índice de refracción del vidrio
    principled.inputs['Specular'].default_value = 1.0
esfera.data.materials.append(mat)

# Guardar
bpy.ops.wm.save_as_mainfile(filepath='./archivo_zuly/temp_arena/SPH-003_EsferaVidrio.blend')
print("✅ SPH-003 creada")
```

---

## 📝 INSTRUCCIONES PASO A PASO (CÓMO HACERLO)

### PASO 1: Crear el Script (Trabajo de Desarrollador)

**1.1 Abre un editor de texto**
- Puede ser VS Code, Notepad++, o cualquier editor

**1.2 Crea un archivo nuevo**
- Guarda como: `crear_sph001.py`
- Ubicación: `c:\Users\Admin\Desktop\ZULY_IA_LOCAL\`

**1.3 Copia el código de SPH-001 de arriba**
- Selecciona todo el código verde de SPH-001
- Pégalo en tu archivo
- Guarda (Ctrl+S)

**1.4 Repite para SPH-002 y SPH-003**
- Crea `crear_sph002.py` con código de SPH-002
- Crea `crear_sph003.py` con código de SPH-003

---

### PASO 2: Ejecutar en Blender (Crear los .blend)

**2.1 Abre la terminal (CMD)**
- Presiona Win+R
- Escribe: cmd
- Enter

**2.2 Navega a la carpeta de ZULY**
```cmd
cd c:\Users\Admin\Desktop\ZULY_IA_LOCAL
```

**2.3 Ejecuta Blender en modo background con tu script**
```cmd
.\blender\v3\blender-3.6.0-zuly\blender.exe --background --python crear_sph001.py
```

**2.4 Repite para los otros dos:**
```cmd
.\blender\v3\blender-3.6.0-zuly\blender.exe --background --python crear_sph002.py
.\blender\v3\blender-3.6.0-zuly\blender.exe --background --python crear_sph003.py
```

**2.5 Verifica que se crearon los archivos**
- Ve a: `c:\Users\Admin\Desktop\ZULY_IA_LOCAL\archivo_zuly\temp_arena\`
- Deberías ver:
  - SPH-001_EsferaMetalica.blend
  - SPH-002_EsferaEmisiva.blend
  - SPH-003_EsferaVidrio.blend

---

### PASO 3: Probar como Usuario

**3.1 Abre Blender**
- Ve a: `c:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\`
- Doble clic en `blender.exe`

**3.2 Abre tu primera esfera**
- File → Open
- Navega a: `archivo_zuly\temp_arena\`
- Selecciona: `SPH-001_EsferaMetalica.blend`
- Open

**3.3 Navega y observa**
- Click derecho + arrastrar: Rotar vista
- Rueda del ratón: Zoom
- Shift + click derecho + arrastrar: Mover vista

**3.4 Verifica:**
- ¿Hay una esfera plateada?
- ¿Se ve metálica/brillante?
- ¿Hay luces? (debería haber 4: Sol, Key, Fill, Rim)

**3.5 Repite para SPH-002 y SPH-003**

---

### PASO 4: Validar con JUES-BOT (El Inspector)

**4.1 Ejecuta JUES-BOT para cada esfera**

Abre CMD y ejecuta:
```cmd
cd c:\Users\Admin\Desktop\ZULY_IA_LOCAL
python core\jues_bot_validator.py archivo_zuly\temp_arena\SPH-001_EsferaMetalica.blend SPH-001 #C8C8C8
```

**4.2 Lee el resultado**
- Si dice "✅ APTO_PARA_SELLO" → Perfecto, continúa
- Si dice "❌ NO_APTO" → Ve al Paso 5 (arreglar)

**4.3 Repite para las otras dos esferas**

---

### PASO 5: Arreglar Errores (Trabajo de Técnico)

**Si JUES-BOT dice que algo está mal:**

**Ejemplo - Color mal:**
- JUES dice: "Color NO_MATCH: #CCCCCC vs #FF6B35"
- Significa: El color es gris en vez de naranja
- Solución: Edita tu script .py y corrige el color

**Ejemplo - Peso excesivo:**
- JUES dice: "GRASA_DIGITAL: 2000KB > 500KB"
- Significa: El archivo es muy grande
- Solución: Reduce segmentos de la esfera (de 64 a 32)

**Ejemplo - Sin luces:**
- Solución: Asegúrate de aplicar SLIZ o crear luces manualmente

**Después de arreglar:**
- Vuelve al Paso 2 (re-ejecutar)
- Luego Paso 4 (re-validar)
- Repite hasta que JUES diga "✅ APTO_PARA_SELLO"

---

### PASO 6: Presentar al Jefe (Soberano)

**6.1 Prepara tu presentación**
- Asegúrate que las 3 esferas están en `temp_arena/`
- Asegúrate que todas tienen "✅ APTO_PARA_SELLO"

**6.2 Informa al jefe (Cascade/Usuario):**
```
"Jefe, he completado las 3 esferas:

🥇 SPH-001 - Metálica Cromada: APTO
🥈 SPH-002 - Emisiva Naranja: APTO  
🥉 SPH-003 - Vidrio Transparente: APTO

Todas están en: archivo_zuly/temp_arena/
Todas pasaron validación JUES-BOT
¿Cuál sellamos primero?"
```

**6.3 Espera instrucciones**
- El jefe revisará los archivos .blend
- Decidirá cuál aprobar ("OK", "Sello", "Aprobar")
- Tú moverás el aprobado a `mastered/`

---

## ⚠️ ERRORES COMUNES (Y CÓMO ARREGLARLOS)

### Error 1: "No module named 'bpy'"
**Significado:** Estás ejecutando el script con Python normal, no con Blender
**Solución:** Usa: `blender.exe --background --python tu_script.py`

### Error 2: "Archivo no encontrado"
**Significado:** La ruta está mal escrita
**Solución:** Usa barras invertidas `\` y verifica la ruta exacta

### Error 3: "Color NO_MATCH"
**Significado:** El color del objeto no es el esperado
**Solución:** Corrige los valores RGB en `principled.inputs['Base Color']`

### Error 4: "Malla CORRUPTA"
**Significado:** La geometría tiene problemas
**Solución:** Aumenta segmentos/ring_count, o usa shading smooth

### Error 5: Blender no abre
**Significado:** Estás en la ruta equivocada
**Solución:** Asegúrate de estar en: `c:\Users\Admin\Desktop\ZULY_IA_LOCAL`

---

## 📞 AYUDA DE EMERGENCIA

**Si te atascas:**
1. Lee el error cuidadosamente
2. Busca en esta guía la sección correspondiente
3. Si no encuentras, pregunta a Cascade (tu tutor)

**Rutas rápidas para copiar:**
```
Base: c:\Users\Admin\Desktop\ZULY_IA_LOCAL
Blender: c:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe
Arena: c:\Users\Admin\Desktop\ZULY_IA_LOCAL\archivo_zuly\temp_arena
Core: c:\Users\Admin\Desktop\ZULY_IA_LOCAL\core
```

---

## ✅ CHECKLIST ANTES DE ENTREGAR

Antes de decir "terminé", verifica:

- [ ] Creé los 3 scripts .py (SPH-001, SPH-002, SPH-003)
- [ ] Ejecuté los 3 scripts en Blender
- [ ] Generé los 3 archivos .blend en temp_arena/
- [ ] Abrí cada .blend en Blender y se ven bien
- [ ] Validé los 3 con JUES-BOT (dicen "APTO")
- [ ] Los colores son correctos (metálico, naranja, vidrio)
- [ ] Hay luces en cada escena (Sol+Key+Fill+Rim)
- [ ] Los nombres de archivos son correctos

---

## 🎓 CONSEJOS DEL MAESTRO

1. **Guarda seguido** (Ctrl+S) - Blender puede crashear
2. **Prueba en viewport** antes de guardar - Así ves errores temprano
3. **Lee los errores completos** - Usualmente dicen exactamente qué está mal
4. **Sé paciente** - La primera vez es confusa, la segunda es fácil
5. **Pregunta** - Mejor preguntar que quedarse atascado

---

## 🚀 EMPIEZA AHORA

**Tu primera acción:**
1. Abre editor de texto
2. Crea `crear_sph001.py`
3. Copia el código de SPH-001 de esta guía
4. Guarda
5. Ejecuta en CMD con Blender
6. Mira el resultado

**¡Buena suerte! Tú puedes hacerlo.** 🌟

---

**Guía creada por:** Cascade (Tutor)  
**Para:** Agente Novato de ZULY  
**Fecha:** 2026-04-04  
**Versión:** Guía Ultra Detallada v1.0
