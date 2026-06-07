# 📋 HOJA DE RUTA - PRIORIDAD ALTA
**Fecha:** 2026-04-03  
**Proyecto:** ZULY Pattern System  
**Estado:** En progreso  

---

## 🎯 OBJETIVO PRINCIPAL

Establecer sistema de aprobación de patrones donde:
1. **ZULY** genera y propone patrones
2. **Usuario** da visto bueno ("OK")
3. **ZULY** guarda automáticamente en `VERIFIED`

---

## 📊 PATRONES EXISTENTES (23 pendientes de aprobación)

### Primitivas Básicas

| ID | Comando | Cantidad | Estado |
|-----|---------|----------|--------|
| P-001 | crear_cubo | 4 | ⏳ PENDING |
| P-002 | crear_esfera | 5 | ⏳ PENDING |
| P-003 | blender.create_sphere | 3 | ⏳ PENDING |
| P-004 | blender.create_cylinder | 2 | ⏳ PENDING |
| P-005 | blender.create_cone | 2 | ⏳ PENDING |
| P-006 | blender.create_plane | 1 | ⏳ PENDING |

**Total:** 23 patrones en PENDING  
**Acción requerida:** Aprobación usuario para mover a VERIFIED

---

## 🆕 NUEVOS PATRONES EN DESARROLLO

### FASE 1 - Cubos Avanzados (Prioridad ALTA)

| ID | Nombre | Descripción | Estado |
|-----|--------|-------------|--------|
| CUB-001 | Modelado_BiselRealista | Cubo con bordes suaves (Bevel) | 🔄 CORRECCIÓN |
| CUB-002 | Transform_PivoteSuelo | Cubo con origen en suelo | ⏳ PENDIENTE |
| CUB-003 | Modelado_MuroPro | Muro arquitectónico | ⏳ PENDIENTE |
| CUB-004 | Modificador_ArrayModular | Repetición de módulos | ⏳ PENDIENTE |
| CUB-005 | Modificador_BooleanExacto | Operaciones booleanas | ⏳ PENDIENTE |

### FASE 2 - Materiales Avanzados (Prioridad MEDIA)

| ID | Nombre | Descripción | Estado |
|-----|--------|-------------|--------|
| MAT-001 | Material_Metal | Shader metálico | ⏳ PENDIENTE |
| MAT-002 | Material_Vidrio | Shader transparente | ⏳ PENDIENTE |
| MAT-003 | Material_Emisivo | Shader emisivo | ⏳ PENDIENTE |

### FASE 3 - Iluminación Profesional (Prioridad MEDIA)

| ID | Nombre | Descripción | Estado |
|-----|--------|-------------|--------|
| LUZ-001 | Iluminacion_3Point | Setup key+fill+rim | ⏳ PENDIENTE |
| LUZ-002 | Iluminacion_HDRI | Ambiente HDRI | ⏳ PENDIENTE |

---

## 🏗️ ESTRUCTURA DE ALMACENAMIENTO

### Jerarquía de Repositorios

```
memory/
├── patterns_pending.json     ← ZULY propone aquí
├── patterns_staging.json     ← Validación técnica
├── patterns_verified.json    ← ✅ TU APROBACIÓN
└── patterns_quarantine.json  ← Rechazados
```

### Flujo de Aprobación

```
┌────────────────┐
│  ZULY genera   │
│    patrón      │
└───────┬────────┘
        ▼
┌────────────────┐
│   PENDING      │
│  (temporal)    │
└───────┬────────┘
        ▼
┌────────────────┐
│   STAGING      │
│  (prueba real  │
│   en Blender)  │
└───────┬────────┘
        ▼
┌────────────────┐
│   Esperando    │
│   tu "OK"      │
└───────┬────────┘
        ▼
┌────────────────┐     ┌────────────────┐
│  TU DICES:     │     │  TU DICES:     │
│     "OK"       │     │   "ERROR"      │
└───────┬────────┘     └───────┬────────┘
        ▼                      ▼
┌────────────────┐     ┌────────────────┐
│   VERIFIED     │     │  QUARANTINE    │
│   (guardado    │     │  (revisar      │
│    permanente) │     │   después)     │
└────────────────┘     └────────────────┘
```

---

## 📝 PROTOCOLO DE APROBACIÓN

### Para el Agente ZULY:

1. **Generar patrón** siguiendo estructura JSON completa
2. **Ejecutar en Blender** background
3. **Validar técnica**:
   - Sin errores
   - Escala aplicada
   - Nombres técnicos
   - Archivos generados (.blend + render)
4. **Guardar en STAGING** temporalmente
5. **Presentar a usuario** con resumen
6. **Esperar aprobación**: "OK" o "ERROR"
7. **Si OK**: Mover a VERIFIED
8. **Si ERROR**: Corregir o mover a QUARANTINE

### Para el Usuario:

Solo necesitas decir:
- **"OK"** → Aprobado, ZULY guarda
- **"ERROR"** → Rechazado, ZULY corrige o descarta

---

## 🔧 ESTRUCTURA JSON ESTÁNDAR

```json
{
  "id": "CUB-001",
  "nombre_tecnico": "CUB-001_Modelado_BiselRealista",
  "nombre_simple": "Cubo con bordes suaves",
  
  "descripcion_simple": "Crea un cubo con bordes redondeados.",
  "descripcion_tecnica": "Aplica modificador Bevel con 3 segmentos.",
  "uso": "Arquitectura, hard surface",
  
  "tags": ["cubo", "modelado", "modificador", "bevel"],
  
  "propiedades": {
    "parametros_editables": {
      "bevel_width": "Ancho del bisel"
    },
    "valores_default": {
      "bevel_width": 0.05
    },
    "limites": {
      "bevel_width": [0.001, 0.2]
    },
    "dependencias": []
  },
  
  "reglas_aplicadas": {
    "reset": true,
    "escala": true,
    "nombres_tecnicos": true,
    "sin_errores": true
  },
  
  "archivos_generados": {
    "blend": "./ZULY_PROJECTS/CUB001_Modelado_BiselRealista.blend",
    "render": "./ZULY_PROJECTS/CUB001_render.png"
  },
  
  "validacion": {
    "ejecutado": "2026-04-03T14:00:00",
    "status": "PENDIENTE_APROBACION",
    "aprobado_por": null,
    "timestamp_aprobacion": null
  }
}
```

---

## 📂 ARCHIVOS DE PATRONES APROBADOS

Cada patrón aprobado se guarda en:

```
patrones/
├── CUB001.json    ← Patrón CUB-001 aprobado
├── CUB002.json    ← Patrón CUB-002 aprobado
├── MAT001.json    ← Patrón MAT-001 aprobado
└── ...
```

Y también en:
```
memory/patterns_verified.json    ← Lista completa
```

---

## ✅ CHECKLIST HOY (2026-04-03)

### Completado:
- [x] Análisis de 23 patrones existentes
- [x] CUB-001 generado (en corrección)
- [x] Estructura de hoja de ruta creada

### Pendiente:
- [ ] Corregir CUB-001 (color + auto smooth)
- [ ] Re-ejecutar CUB-001
- [ ] Aprobación CUB-001
- [ ] Generar CUB-002 a CUB-005
- [ ] Aprobar/descartar 23 patrones antiguos
- [ ] Implementar guardado automático en VERIFIED

---

## 🎯 PRÓXIMOS PASOS

1. **Corregir CUB-001**
   - Definir color correcto
   - Ajustar auto smooth
   - Re-ejecutar

2. **Aprobar CUB-001**
   - Usuario dice "OK"
   - ZULY guarda en VERIFIED
   - Documenta estructura

3. **Continuar con CUB-002 a CUB-005**
   - Seguir mismo protocolo
   - Uno por uno

---

## 📌 NOTAS IMPORTANTES

- **ZULY nunca aprueba solo** - siempre espera tu "OK"
- **Patrones rechazados** van a QUARANTINE, no se pierden
- **Estructura JSON** es obligatoria para todos los patrones
- **Prueba real en Blender** requerida antes de presentar
- **Fecha de aprobación** se registra automáticamente

---

**Documento generado:** 2026-04-03  
**Próxima revisión:** Después de aprobación CUB-001  
**Responsable:** Agente ZULY + Usuario (aprobadores)
