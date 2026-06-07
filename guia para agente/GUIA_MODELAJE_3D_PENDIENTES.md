# 📋 GUÍA PARA AGENTE ZULY - TAREAS DE MODELAJE 3D PENDIENTES
## Instrucciones Específicas para Generación de Patrones Blender

**Fecha:** 2026-04-04  
**Prioridad:** 🔴 ALTA  
**Enfoque:** Modelado 3D y Geometría

---

## 🎯 TAREAS DE MODELAJE PENDIENTES (FASE 1 - PRIORIDAD ALTA)

### 🔴 CUB-001: Modelado_BiselRealista
**Estado:** 🔄 EN CORRECCIÓN  
**Ubicación:** `archivo_zuly/temp_arena/CUB-001_Modelado_BiselRealista.blend`

**Descripción:**  
Cubo con bordes redondeados profesionales usando modificador Bevel.

**Especificaciones Técnicas:**
```python
# GEOMETRÍA
- Tipo: Cube primitivo
- Dimensiones: 2x2x2 metros (default)
- Modificador Bevel:
  * Width: 0.05 - 0.1 (ajustable)
  * Segments: 3-4
  * Limit Method: ANGLE
  * Angle Limit: 30° (0.5236 rad)
  * Miter Outer: MITER_ARC

# MATERIAL
- Nombre: Mat_Azul_Pro
- Tipo: Principled BSDF
- Base Color: #1A4DCC (Azul corporativo - CORREGIR)
- Roughness: 0.3
- Specular: 0.7

# ILUMINACIÓN
- Aplicar SLIZ v2.0 automáticamente
- Key + Fill + Rim + Sol
- Todas apuntan al centro del cubo
```

**Error Actual a Corregir:**
- ❌ Color actual: #194CCC
- ✅ Color objetivo: #1A4DCC
- Diferencia: ~3% en canal azul

**Próximo Paso:**  
1. Ajustar color a #1A4DCC exacto
2. Revalidar con JUES-BOT
3. Presentar a Usuario para SELLO

---

### 🔴 CUB-002: Transform_PivoteSuelo
**Estado:** ⏳ PENDIENTE - GENERAR  
**Prioridad:** ALTA

**Descripción:**  
Cubo con punto de pivote (origin) ubicado en la base/suelo, no en el centro.

**Especificaciones Técnicas:**
```python
# GEOMETRÍA
- Tipo: Cube primitivo
- Dimensiones: 2x2x2 metros
- PIVOTE CRÍTICO:
  * Centro geométrico: (0, 0, 1)  # Centro del cubo
  * Origen (pivote): (0, 0, 0)     # EN EL SUELO
  * Aplicar: Object → Set Origin → Origin to 3D Cursor
  * Cursor en Z=0 antes de operar

# CASOS DE USO
- Arquitectura (muros, pilares)
- Props de suelo (cajas, barriles)
- Estructuras que se apilan desde base

# VALIDACIÓN JUES
- Check: origin.z == 0 (tolerancia 0.001)
- Geometría: malla limpia
- Peso: < 500KB para primitiva simple
```

**Script de Generación Esqueleto:**
```python
import bpy

# Limpiar
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Crear cubo centrado en Z=1 (para que base esté en Z=0)
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 1))
cubo = bpy.context.active_object
cubo.name = "CUB-002_PivoteSuelo"

# Mover cursor al suelo (Z=0)
bpy.context.scene.cursor.location = (0, 0, 0)

# Mover origen al cursor (ahora pivote está en suelo)
bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')

# Verificar
print(f"Origen: {cubo.location}")
print(f"Pivote Z: {cubo.location.z} (debe ser 0)")
```

---

### 🔴 CUB-003: Modelado_MuroPro
**Estado:** ⏳ PENDIENTE - GENERAR  
**Prioridad:** ALTA

**Descripción:**  
Muro arquitectónico con proporciones reales, biselado y detalles constructivos.

**Especificaciones Técnicas:**
```python
# GEOMETRÍA
- Tipo: Cube modificado (escalado)
- Dimensiones (proporción muro real):
  * Alto: 3.0 metros
  * Largo: 6.0 metros  
  * Grosor: 0.25 metros (25cm)
- Escala aplicada: SÍ (Ctrl+A → Scale)

# MODIFICADORES
1. Bevel (bordes):
   - Width: 0.01 (1cm)
   - Segments: 2
   - Limit: ANGLE 45°

2. Solidify (opcional, para doble cara):
   - Thickness: 0.02
   - Solo si se necesita interior

# MATERIAL
- Nombre: Mat_Concreto_Muro
- Tipo: Principled BSDF
- Base Color: #8C8C8C (gris concreto)
- Roughness: 0.8
- Normal map: textura concreto (opcional)

# USOS
- Arquitectura exterior
- Interiores (muros divisorios)
- Escenarios urbanos
```

**Proporciones Arquitectónicas:**
```
Muro estándar:
┌────────────────────────────┐ ← Altura: 3m
│                            │
│         FACHADA            │
│                            │
│     Grosor: 25cm           │
└────────────────────────────┘
        ↕
    Largo: 6m
```

---

### 🔴 CUB-004: Modificador_ArrayModular
**Estado:** ⏳ PENDIENTE - GENERAR  
**Prioridad:** ALTA

**Descripción:**  
Sistema de repetición modular usando modificador Array para crear estructuras escalables.

**Especificaciones Técnicas:**
```python
# GEOMETRÍA BASE
- Tipo: Módulo base (cubo, viga, panel, etc.)
- Dimensiones módulo: 1x1x1 metro (unitario)
- Eje de repetición: X (default, configurable)

# MODIFICADOR ARRAY
- Count: 5 (default, configurable 1-50)
- Relative Offset: 1.0 en eje X
- Constant Offset: 0.0 (o pequeño gap si se desea)
- Merge: SÍ (para mantener malla limpia)

# MATERIAL
- Nombre: Mat_Modular_Base
- Base Color: #4A90D9 (azul técnico)
- Roughness: 0.4

# PARÁMETROS EXPUESTOS (para usuario)
{
  "modulo_count": {
    "descripcion": "Cantidad de repeticiones",
    "default": 5,
    "rango": [1, 50],
    "tipo": "int"
  },
  "modulo_separacion": {
    "descripcion": "Espacio entre módulos",
    "default": 0.0,
    "rango": [0.0, 1.0],
    "tipo": "float"
  },
  "eje_repeticion": {
    "descripcion": "Eje de repetición",
    "default": "X",
    "opciones": ["X", "Y", "Z"],
    "tipo": "enum"
  }
}

# CASOS DE USO
- Barandas
- Muros de contención
- Rejas
- Estructuras repetitivas
- Pisos técnicos
```

**Ejemplo Visual:**
```
Módulo base: [■] × 5 repeticiones = [■][■][■][■][■]
```

---

### 🔴 CUB-005: Modificador_BooleanExacto
**Estado:** ⏳ PENDIENTE - GENERAR  
**Prioridad:** ALTA

**Descripción:**  
Operaciones booleanas precisas para crear geometrías complejas por sustracción/adición.

**Especificaciones Técnicas:**
```python
# GEOMETRÍA
- Objeto A (base): Cubo principal
- Objeto B (operador): Cubo, esfera o cilindro de operación
- Operación: BOOLEAN (modificador)

# MODIFICADOR BOOLEAN
- Operation: DIFFERENCE (default, también UNION e INTERSECT)
- Solver: EXACT (precisión máxima)
- Operand Type: OBJECT
- Object: [referencia a objeto B]
- Solver: FAST si hay problemas de rendimiento

# ESCENARIO TÍPICO
1. Cubo base: 2x2x2 metros
2. Cilindro sustractor: radio 0.5, altura 3
3. Resultado: Cubo con agujero cilíndrico

# MATERIAL
- Nombre: Mat_Boolean_Demo
- Base Color: #D9534F (rojo alarma/diferencia)
- Roughness: 0.5

# PARÁMETROS EXPUESTOS
{
  "boolean_operation": {
    "descripcion": "Tipo de operación booleana",
    "default": "DIFFERENCE",
    "opciones": ["DIFFERENCE", "UNION", "INTERSECT"],
    "tipo": "enum"
  },
  "objeto_sustractor_tipo": {
    "descripcion": "Forma del objeto que opera",
    "default": "CUBE",
    "opciones": ["CUBE", "SPHERE", "CYLINDER"],
    "tipo": "enum"
  },
  "posicion_sustractor": {
    "descripcion": "Posición XYZ del operador",
    "default": [0, 0, 0],
    "tipo": "vector"
  }
}

# CASOS DE USO
- Ventanas en muros
- Puertas en paneles
- Agujeros para tuberías
- Uniones mecánicas
- Formas complejas por sustracción

# VALIDACIÓN ESPECIAL
- JUES debe verificar: malla resultante es manifold
- Si no es manifold → advertencia "Revisar geometría booleana"
```

**Diagrama Booleano:**
```
  ┌─────────┐       ┌─────────┐       ┌─────────┐
  │  BASE   │   -   │ CILINDRO │   =   │ RESULT │
  │  ████   │       │   ██    │       │  █  █   │
  │  ████   │       │   ██    │       │  █  █   │
  └─────────┘       └─────────┘       └─────────┘
```

---

## 📐 PRINCIPIOS DE MODELAJE PARA AGENTE ZULY

### ✅ REGLAS DE ORO (Siempre aplicar)

1. **Escala Aplicada**  
   Después de cualquier escalado: `Ctrl+A → Scale`  
   Validación: JUES verifica escala == (1,1,1)

2. **Malla Limpia**  
   - 0 vértices no-manifold  
   - 0 bordes sueltos  
   - Caras planas (no Ngons raros)

3. **Origen Estratégico**  
   - Por defecto: Centro geométrico  
   - Casos especiales: Suelo, centro de masa, etc.

4. **Nomenclatura Estricta**  
   - Objeto: `{ID}_{DescripcionBreve}`  
   - Material: `Mat_{Tipo}_{Color}`  
   - Modificadores: `{Tipo}_{Descripcion}`

5. **Optimización**  
   - Mínimo vértices necesarios  
   - Modificadores no destructivos cuando sea posible  
   - Peso: < 2000KB por patrón

---

## 🔧 CHECKLIST PRE-VALIDACIÓN (Auto-verificar antes de JUES)

```python
✅ Checklist antes de guardar .blend:

□ Geometría:
  □ Escala aplicada (Ctrl+A)
  □ Origen en posición correcta
  □ Malla manifold (Ctrl+Shift+Alt+M para check visual)
  □ Normales correctas (azul hacia afuera)

□ Materiales:
  □ Color exacto al especificado (hex)
  □ Principled BSDF configurado
  □ Nombre descriptivo

□ Iluminación:
  □ SLIZ aplicado (automático en generación)
  □ 4 luces creadas (Sol+Key+Fill+Rim)
  □ Luces apuntan al centro

□ Escena:
  □ Cámara posicionada
  □ Resolución 1920x1080
  □ Motor: Eevee (rápido) o Cycles (calidad)
  □ Sin objetos basura
```

---

## 📁 ESTRUCTURA DE ENTREGA POR PATRÓN

Cuando generes un patrón, entregar:

```
temp_arena/
├── {ID}_{Nombre}.blend          ← Geometría 3D lista
├── {ID}_{Nombre}.py             ← Script de generación
├── {ID}_{Nombre}.json           ← Metadatos y parámetros
└── {ID}_{Nombre}_preview.png    ← Render preview (opcional)
```

### JSON de Metadatos (Obligatorio):
```json
{
  "pattern_id": "CUB-002",
  "nombre_tecnico": "CUB-002_Transform_PivoteSuelo",
  "version": "1.0",
  "descripcion": "Cubo con origen en suelo para arquitectura",
  "tags": ["cubo", "pivote", "arquitectura", "transform"],
  "parametros_exposed": {
    "size": {"default": 2.0, "min": 0.1, "max": 10.0},
    "pivote_z": {"default": 0.0, "valor_fijo": true}
  },
  "geometria": {
    "vertices": 8,
    "caras": 6,
    "tipo": "primitiva_cubo"
  },
  "validacion_jues": {
    "malla": "LIMPIA",
    "peso_kb": 245,
    "color_match": true,
    "hash": "abc123..."
  }
}
```

---

## 🚀 FLUJO DE TRABAJO RECOMENDADO

### Para cada patrón nuevo:

1. **Leer especificación** (esta guía)
2. **Escribir script** de generación (.py)
3. **Ejecutar en Blender** (background)
4. **Auto-validar** con checklist
5. **JUES-BOT valida** técnicamente
6. **LYZU registra** evento
7. **Presentar** a Usuario para decisión
8. **Iterar** si necesita correcciones

---

## 🔄 CICLO DE TRABAJO COMPLETO - AGENTE ZULY (3 ROLES)

El Agente ZULY debe ejecutar el **CICLO COMPLETO** siempre, actuando en **3 ROLES** diferentes:

### 👤 ROL 1: USUARIO NORMAL (Tester/Reviewer)
**Función:** Probar, revisar y validar como un usuario real

**Responsabilidades:**
- Abrir el .blend generado en Blender
- Verificar visualmente la calidad
- Comprobar que el modelo se ve profesional
- Validar que las luces iluminan correctamente
- Revisar que los materiales son correctos
- Verificar dimensiones y proporciones

**Acciones:**
```python
# Como Usuario:
1. Abrir blend en Blender (File → Open)
2. Navegar viewport (rotate, zoom, pan)
3. Verificar iluminación (render preview)
4. Chequear materiales (viewport shading)
5. Validar geometría (wireframe mode)
6. Decisión interna: ¿Pasa o no pasa?
```

**Criterios de Aprobación (Usuario):**
- ✅ Se ve profesional
- ✅ Iluminación correcta
- ✅ No hay errores visuales
- ✅ Proporciones adecuadas
- ❌ Descartar si hay fallos visibles

---

### 🔧 ROL 2: TÉCNICO REPARADOR (Fixer/Debugger)
**Función:** Arreglar errores detectados por JUES-BOT o el Usuario

**Responsabilidades:**
- Interpretar reportes de JUES-BOT
- Corregir errores técnicos
- Ajustar colores exactos (hex codes)
- Limpiar geometría (manifold issues)
- Optimizar peso del archivo
- Ajustar iluminación si es necesario

**Acciones:**
```python
# Como Técnico:
1. Leer reporte JUES: "Color NO_MATCH: #194CCC vs #1A4DCC"
2. Identificar problema: Diferencia de 3% en canal azul
3. Corregir: Ajustar material Base Color a #1A4DCC exacto
4. Revalidar: Ejecutar JUES-BOT de nuevo
5. Verificar: Confirmar "Color MATCH"
6. Documentar: LYZU registra corrección
```

**Reparaciones Comunes:**
| Error | Reparación |
|-------|------------|
| Color NO_MATCH | Ajustar hex exacto en material |
| Malla CORRUPTA | Limpiar vértices dobles, bordes |
| Peso GRASA | Eliminar datos ocultos, optimizar |
| Luces desordenadas | Reaplicar SLIZ v2.0 |
| Origen incorrecto | Object → Set Origin → to Geometry |

---

### 💻 ROL 3: DESARROLLADOR (Creator/Coder)
**Función:** Crear scripts, mejorar código, implementar nuevas features

**Responsabilidades:**
- Escribir scripts de generación (.py)
- Implementar lógica de creación
- Crear funciones reutilizables
- Optimizar algoritmos
- Documentar código
- Crear nuevos sistemas (ej: SLIZ v2.0)

**Acciones:**
```python
# Como Desarrollador:
1. Analizar requerimiento: "Cubo con pivote en suelo"
2. Diseñar solución: origin_set al cursor en Z=0
3. Escribir script: crear_cubo_pivote_suelo.py
4. Implementar: bpy.ops.object.origin_set(...)
5. Probar: Ejecutar en Blender
6. Documentar: Comentarios + JSON metadatos
```

**Entregables de Desarrollador:**
- Script .py funcional
- Código comentado
- JSON de metadatos
- Guía de uso
- Ejemplos de implementación

---

### 🔄 CICLO COMPLETO - EJECUCIÓN PASO A PASO

El Agente ZULY SIEMPRE ejecuta este ciclo completo:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    CICLO COMPLETO ZULY (3 ROLES)                            │
└─────────────────────────────────────────────────────────────────────────────┘

PASO 1: DESARROLLADOR 💻
┌─────────────────────────────────────────────────────────────────────────────┐
│ • Analiza requerimiento de patrón                                          │
│ • Escribe script de generación (.py)                                         │
│ • Implementa lógica de creación en Blender                                   │
│ • Crea funciones auxiliares si es necesario                                  │
│ • Guarda script en core/ o temp/                                              │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
PASO 2: DESARROLLADOR 💻 (continuación)
┌─────────────────────────────────────────────────────────────────────────────┐
│ • Ejecuta script en Blender (background)                                     │
│ • Genera .blend en temp_arena/                                              │
│ • Crea JSON de metadatos                                                     │
│ • Verifica que no hay errores de sintaxis                                    │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
PASO 3: USUARIO 👤
┌─────────────────────────────────────────────────────────────────────────────┐
│ • Abre .blend generado en Blender                                            │
│ • Navega escena (viewport)                                                   │
│ • Verifica visualmente:                                                      │
│   - ¿Se ve bien?                                                             │
│   - ¿Luces correctas?                                                        │
│   - ¿Materiales bien?                                                        │
│   - ¿Proporciones correctas?                                                 │
│ • Decisión: ¿Pasa visual? ✅ / ❌                                             │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
PASO 4: JUES-BOT 🤖 (automático)
┌─────────────────────────────────────────────────────────────────────────────┐
│ • Valida técnicamente el patrón                                              │
│ • Aplica 4 superpoderes:                                                     │
│   - Visión Rayos X (manifold)                                                │
│   - Instinto Optimización (peso)                                             │
│   - Sincronía Cromática (color)                                              │
│   - Sello Inmutabilidad (hash)                                               │
│ • Aplica SLIZ v2.0 (iluminación)                                             │
│ • Genera reporte JSON                                                        │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
PASO 5: TÉCNICO 🔧 (si hay errores)
┌─────────────────────────────────────────────────────────────────────────────┐
│ • Lee reporte JUES                                                           │
│ • Si hay errores:                                                            │
│   - Color NO_MATCH → Ajustar hex exacto                                      │
│   - Malla CORRUPTA → Limpiar geometría                                       │
│   - Peso GRASA → Optimizar                                                   │
│   - Luces mal → Reaplicar SLIZ                                               │
│ • Re-ejecuta script corregido                                                │
│ • Revalida con JUES                                                          │
│ • Repite hasta "APTO_PARA_SELLO"                                              │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
PASO 6: USUARIO 👤 (final)
┌─────────────────────────────────────────────────────────────────────────────┐
│ • Revisa patrón corregido                                                    │
│ • Valida visualmente                                                         │
│ • Decide:                                                                    │
│   [S] SELLO → Presentar a Soberano para aprobación                           │
│   [R] RECHAZO → Bitacora y regenerar                                         │
│   [C] CORREGIR → Devolver a Técnico                                         │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
PASO 7: PRESENTACIÓN AL SOBERANO 👑
┌─────────────────────────────────────────────────────────────────────────────┐
│ • ZULY presenta al Usuario real:                                             │
│   - Dashboard JUES-BOT                                                       │
│   - Ranking de candidatos                                                    │
│   - Archivo .blend para revisión                                             │
│ • Espera decisión final del Soberano                                         │
│ • Si SELLO: Ejecuta archivado en mastered/                                     │
│ • LYZU registra toda la transacción                                          │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

### 📋 CHECKLIST POR ROL

**DESARROLLADOR 💻 debe verificar:**
- [ ] Script ejecuta sin errores
- [ ] Código está comentado
- [ ] JSON de metadatos creado
- [ ] Funciones son reutilizables
- [ ] Especifícaciones técnicas cumplidas

**USUARIO 👤 debe verificar:**
- [ ] Modelo se ve profesional
- [ ] Iluminación es correcta
- [ ] Materiales se ven bien
- [ ] No hay errores visuales
- [ ] Proporciones son adecuadas

**TÉCNICO 🔧 debe verificar:**
- [ ] JUES-BOT reporta "LIMPIA"
- [ ] Color es MATCH exacto
- [ ] Peso es OPTIMO (< 2000KB)
- [ ] Hash generado correctamente
- [ ] Luces SLIZ apuntan al centro

---

### 🎯 REGLA DE ORO

> **"El Agente ZULY nunca genera y abandona. Siempre completa el ciclo: Desarrollar → Usar → Reparar → Presentar."**

**Prohibido:**
- ❌ Generar patrón sin revisarlo visualmente
- ❌ Dejar errores JUES sin corregir
- ❌ Saltarse el paso de prueba de usuario
- ❌ Entregar sin documentación

**Obligatorio:**
- ✅ Siempre probar como Usuario
- ✅ Siempre corregir como Técnico
- ✅ Siempre documentar como Desarrollador
- ✅ Siempre completar el ciclo hasta presentación

---

## 🎯 PRIORIDADES ACTUALES (Hoy - 2026-04-04)

### Orden de Trabajo:

**1. URGENTE - Terminar CUB-001:**
   - Ajustar color a #1A4DCC exacto
   - Revalidar JUES
   - Conseguir primer SELLO del sistema

**2. ALTA - Generar CUB-002:**
   - Crear cubo con pivote en suelo
   - Script con origin_set
   - Validar y presentar

**3. ALTA - Generar CUB-003:**
   - Muro arquitectónico 3x6x0.25m
   - Proporciones reales
   - Material concreto

**4. ALTA - Generar CUB-004:**
   - Sistema modular con Array
   - Parámetros expuestos configurables
   - Ejemplo con 5 repeticiones

**5. ALTA - Generar CUB-005:**
   - Booleano difference con cilindro
   - Verificar manifold resultante
   - Material de demostración

---

## 📚 REFERENCIAS RÁPIDAS

### Rutas Importantes:
```
Guía completa: c:\Users\Admin\Desktop\ZULY_IA_LOCAL\guia para agente\ (esta carpeta)
Core sistema:  c:\Users\Admin\Desktop\ZULY_IA_LOCAL\core\
Arena:         c:\Users\Admin\Desktop\ZULY_IA_LOCAL\archivo_zuly\temp_arena\
Mastered:      c:\Users\Admin\Desktop\ZULY_IA_LOCAL\archivo_zuly\por_estado_aprendizaje\mastered\
Hoja de ruta:  c:\Users\Admin\Desktop\ZULY_IA_LOCAL\HOJA_DE_RUTA_PRIORIDAD_ALTA.md
```

### Archivos de Soporte:
- `core/sistema_luces_inteligente.py` → SLIZ v2.0
- `core/jues_bot_validator.py` → Validación técnica
- `core/cerebro_lyzu.py` → Registro de eventos

---

**Agente ZULY - Modelador 3D**  
**Misión:** Generar geometrías perfectas, validadas técnicamente, listas para aprobación del Soberano.

**Recuerda:** "Escala aplicada, malla limpia, iluminación profesional, SELLO garantizado."
