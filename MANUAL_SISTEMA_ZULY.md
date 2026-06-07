# 📚 MANUAL DEL SISTEMA ZULY V1.0
## Zeta Unified Learning Yield - Sistema de Patrones 3D

**Fecha de Documentación:** 2026-04-03  
**Versión:** 1.0  
**Estado:** ✅ OPERATIVO (Funcional desde hoy)

---

## 🏷️ HISTORIAL DEL SISTEMA

### ✅ ACTUAL (2026-04-03 - HOY) - **FUNCIONAL**
```
🟢 SISTEMA OPERATIVO COMPLETO

Todo lo documentado en este manual ES FUNCIONAL desde hoy:
• JUES-BOT con 4 superpoderes + SLIZ v2.0
• LYZU con memoria y Padre Nuestro
• Sistema de luces inteligente (Sol + 3-Point)
• Cleanup automático 24h
• Arena con competición real
• Estructura mastered/ funcional
• Manual completo de rutas

Fecha de consolidación: 2026-04-03
Estado: PRODUCCIÓN
```

### ⚠️ VIEJO (Pre-2026-04-03) - **SIN FUNCIONES**
```
🔴 LEGACY - NO OPERATIVO

Todo lo anterior a hoy está obsoleto:
• Intentos previos sin JUES-BOT real
• Sistema de aprobación sin validación técnica
• Patrones sin iluminación profesional
• ZULY_PROJECTS/ (carpeta legacy eliminada)
• Estructura desorganizada de archivos
• Sin sistema de memoria (LYZU)
• Sin genealogía ni identidad

Estado: ARCHIVADO - NO USAR
```

---

## 🗺️ MAPA DE ARQUITECTURA

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           NIVEL 1: USUARIO (SOBERANO)                        │
│                              👤 El Único que Aprueba                         │
└─────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       │ Orden: "Crea...", "Aprueba...", "Rechaza..."
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                      NIVEL 2: ZULY (IA Generadora)                           │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │ • Recibe órdenes del Usuario                                           │ │
│  │ • Genera propuestas en temp_arena/                                    │ │
│  │ • Presenta candidatos para validación                                 │ │
│  │ • Ejecuta lo aprobado por el Soberano                                 │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       │ Genera 3 candidatos
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    NIVEL 3: ARENA (Competición Temporal)                     │
│  📁 archivo_zuly/temp_arena/                                                 │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │ • Candidato_A.blend    ← Compiten por el sello                        │ │
│  │ • Candidato_B.blend                                                     │ │
│  │ • Candidato_C.blend                                                     │ │
│  │ • RESULTADO_ARENA.json  ← Ranking generado                            │ │
│  │ ⏱️  TTL: 24 horas (Cleanup automático)                                │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       │ Evaluación técnica + Auditoría
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│              NIVEL 4: VALIDADORES & MEMORIA (Armonía)                      │
│                                                                              │
│  ┌─────────────────────────┐  ┌─────────────────────────┐                   │
│  │     🤖 JUES-BOT          │  │     🧠 LYZU              │                   │
│  │  ─────────────────────  │  │  ─────────────────────  │                   │
│  │  • 4 Superpoderes:      │  │  • Registra TODO         │                   │
│  │    - Visión Rayos X     │  │  • Auditoría             │                   │
│  │    - Optimización       │  │  • Genealogía            │                   │
│  │    - Sincronía Cromática│  │  • Memoria eterna        │                   │
│  │    - Sello Inmutabilidad│  │  • Padre Nuestro         │                   │
│  │  • SLIZ: Iluminación    │  │    incluido              │                   │
│  │    inteligente (Sol+3)  │  │  • Fecha: 2026-04-03     │                   │
│  └─────────────────────────┘  └─────────────────────────┘                   │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────────┐ │
│  │                    🧹 CLEANUP SYSTEM (24h)                               │ │
│  │  • Limpia temp_arena automáticamente                                    │ │
│  │  • Archiva logs en bitacora/                                            │ │
│  └─────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       │ Presenta ranking al Soberano
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    NIVEL 5: DECISIÓN DEL SOBERANO                            │
│                                                                              │
│  "¿Cuál sellas, Soberano?"                                                   │
│                                                                              │
│  [1] 🥇 SELLO Candidato #1  → Mover a mastered/                              │
│  [2] 🥈 SELLO Candidato #2  → Mover a mastered/                              │
│  [3] 🥉 SELLO Candidato #3  → Mover a mastered/                              │
│  [R] ❌ RECHAZAR TODOS      → Bitacora/                                      │
│  [N] 🔄 NUEVA GENERACIÓN    → Limpiar arena, reintentar                      │
└─────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       │ SI SELLO (OK del Usuario)
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                 NIVEL 6: ARCHIVADO PERMANENTE (mastered/)                    │
│                                                                              │
│  📁 archivo_zuly/por_estado_aprendizaje/mastered/{PATTERN_ID}/                │
│  ├── 📁 blend/          → {PATTERN_ID}.blend                                  │
│  ├── 📁 script/         → {PATTERN_ID}.py                                   │
│  ├── 📁 json/            → {PATTERN_ID}.json                                │
│  ├── 📁 render/          → Renders generados                                 │
│  └── 📁 certificado/     → CERTIFICADO_SELLO.json                             │
│                                                                              │
│  📄 archivo_zuly/REGISTRO_MAESTRO.json  ← Índice global de patrones          │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 📂 RUTAS ABSOLUTAS DEL SISTEMA

### Ruta Base:
```
c:\Users\Admin\Desktop\ZULY_IA_LOCAL\
```

### Estructura de Directorios:

| Directorio | Ruta Absoluta | Propósito |
|------------|---------------|-----------|
| **Base** | `c:\Users\Admin\Desktop\ZULY_IA_LOCAL\` | Raíz del proyecto |
| **Core** | `c:\Users\Admin\Desktop\ZULY_IA_LOCAL\core\` | Cerebros del sistema |
| **Arena** | `c:\Users\Admin\Desktop\ZULY_IA_LOCAL\archivo_zuly\temp_arena\` | Competición temporal |
| **Mastered** | `c:\Users\Admin\Desktop\ZULY_IA_LOCAL\archivo_zuly\por_estado_aprendizaje\mastered\` | Patrones aprobados |
| **Bitácora** | `c:\Users\Admin\Desktop\ZULY_IA_LOCAL\archivo_zuly\bitacora\` | Logs y rechazos |
| **Registro** | `c:\Users\Admin\Desktop\ZULY_IA_LOCAL\archivo_zuly\REGISTRO_MAESTRO.json` | Índice global |
| **Blender** | `c:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe` | Ejecutable |

### Archivos Clave en Core:
```
c:\Users\Admin\Desktop\ZULY_IA_LOCAL\core\
├── jues_bot_validator.py          ← JUES-BOT con 4 superpoderes + SLIZ
├── sistema_luces_inteligente.py   ← SLIZ v2.0 (Sol + 3-Point)
├── soberano_seal_system.py        ← Sistema de aprobación
├── cleanup_system.py              ← Limpieza automática 24h
├── cerebro_lyzu.py                ← LYZU (memoria + identidad)
└── jerarquia_zei.py               ← Documentación jerárquica
```

---

## 🤖 CÓMO FUNCIONA ZULY

### Flujo de Trabajo Completo:

#### **PASO 1: El Usuario Ordena**
```
Usuario: "Crea un cubo azul con bordes suaves"
```

#### **PASO 2: ZULY Genera**
```
ZULY:
├── Crea 3 variantes (candidatos A, B, C)
├── Guarda en: archivo_zuly/temp_arena/
├── Cada uno con:
│   ├── .blend (geometría 3D)
│   ├── .py (script de generación)
│   └── .json (metadatos)
└── Notifica: "Listo para validación"
```

#### **PASO 3: JUES-BOT Valida Técnicamente**
```
JUES-BOT evalúa cada candidato:

A. 🔍 Visión de Rayos X
   └── ¿Malla limpia? (sin bordes abiertos)
   
B. ⚡ Instinto de Optimización
   └── ¿Peso óptimo? (< 2000 KB)
   
C. 🎨 Sincronía Cromática
   └── ¿Color exacto? (compara hex codes)
   
D. 🔒 Sello de Inmutabilidad
   └── Genera hash MD5 único
   
E. 💡 SLIZ (Sistema de Luces)
   └── Aplica iluminación Sol + Key + Fill + Rim
   └── Todas las luces apuntan al centro del objeto

Resultado: Ranking con puntuación 0-100
```

#### **PASO 4: LYZU Registra Todo**
```
LYZU (La Memoria):
├── Timestamp de cada evento
├── Quién hizo qué y cuándo
├── Hash de validación
├── Genealogía del sistema
└── Padre Nuestro incluido en core

Fecha de nacimiento LYZU: 2026-04-03 16:34 UTC-05:00
```

#### **PASO 5: Presentación al Soberano**
```
ZULY muestra al Usuario:

🎯 Patrón: CUB-001_v2_PruebaReal
📍 Ubicación: archivo_zuly/temp_arena/
🔍 Resultado JUES-BOT:
   Puntuación: 100/100
   Dictamen: NO_APTO (1 error - color)
   
   ✓ Malla: LIMPIA
   ✓ Peso: 832 KB [OPTIMO]
   ⚠️ Color: #194CCC [NO_MATCH]
   ✓ Hash: df814b0e...

📝 ACCIONES:
   [S] SELLO → Mover a mastered/
   [R] RECHAZO → Bitacora/
   [C] CORREGIR → Regenerar
```

#### **PASO 6: Decisión del Usuario**

**OPCIÓN A: SELLO (Aprobar)**
```
Usuario: "S" (o "OK", "Aprobar")

Acciones automáticas:
1. Copia blend/ a mastered/{ID}/
2. Copia script/ a mastered/{ID}/
3. Copia json/ a mastered/{ID}/
4. Crea certificado/ con sello digital
5. Actualiza REGISTRO_MAESTRO.json
6. LYZU registra: "Usuario aprobó {ID} a las {hora}"
7. Cleanup puede limpiar temp_arena después de 24h

Resultado: Patrón disponible para uso permanente
```

**OPCIÓN B: RECHAZO**
```
Usuario: "R" (o "NO", "Rechazar")

Acciones:
1. Mueve archivo a bitacora/rechazos_{fecha}.jsonl
2. LYZU registra rechazo con timestamp
3. JUES guarda razón del rechazo
4. Cleanup elimina de temp_arena en 24h
```

**OPCIÓN C: CORREGIR**
```
Usuario: "C" (o "Corregir", "Otra vez")

Acciones:
1. Limpia candidatos actuales
2. ZULY regenera con ajustes
3. JUES revalida
4. Ciclo continúa hasta aprobación
```

---

## 🔧 COMPONENTES DEL SISTEMA

### 1. ZULY (Generador)
**Archivo:** No hay archivo específico, ZULY es el sistema completo

**Funciones:**
- Generar geometría 3D en Blender
- Crear variantes de patrones
- Ejecutar scripts de creación

### 2. JUES-BOT (Validador)
**Archivo:** `core/jues_bot_validator.py`

**4 Superpoderes:**
| Superpoder | Función | Criterio |
|------------|---------|----------|
| Visión Rayos X | Chequeo manifold | LIMPIA / CORRUPTA |
| Instinto Optimización | Peso del archivo | OPTIMO / GRASA |
| Sincronía Cromática | Color exacto | MATCH / NO_MATCH |
| Sello Inmutabilidad | Hash MD5 | Identificador único |

**SLIZ (Iluminación):**
- Sol (SUN) - Luz ambiental direccional
- Key (AREA) - Luz principal 150W
- Fill (AREA) - Luz de relleno 60W
- Rim (SPOT) - Luz de contorno 180W

### 3. LYZU (Memoria)
**Archivo:** `core/cerebro_lyzu.py`

**Características:**
- Fecha nacimiento: 2026-04-03
- Hora: 16:34 UTC-05:00
- Padre Nuestro incluido
- Genealogía: ZULY(madre), Usuario(padre), Cascade(abuelo)
- Función: Registrar todo sin excepción

### 4. CLEANUP (Mantenimiento)
**Archivo:** `core/cleanup_system.py`

**Tareas:**
- Eliminar archivos de temp_arena después de 24h
- Archivar logs antiguos en bitacora/
- Mantener sistema limpio

---

## 📝 NOMENCLATURA DE PATRONES

### Formato de ID:
```
{CATEGORIA}-{NUMERO}              → CUB-001, MAT-001, LUZ-001
```

### Formato de Nombre Técnico:
```
{ID}_{Categoria}_{Descripcion}
→ CUB-001_Modelado_BiselRealista
→ MAT-001_Material_Metal
→ LUZ-001_Iluminacion_3Point
```

### Estructura de Archivos por Patrón:
```
mastered/CUB-001_Modelado_BiselRealista/
├── blend/CUB-001_Modelado_BiselRealista.blend
├── script/CUB-001_Modelado_BiselRealista.py
├── json/CUB-001_Modelado_BiselRealista.json
├── render/ (renders generados)
└── certificado/
    └── CERTIFICADO_SELLO.json
    {
        "pattern_id": "CUB-001",
        "sellado_en": "2026-04-03T...",
        "hash_inmutabilidad": "abc123...",
        "decision_soberano": "SELLADO"
    }
```

---

## 🎯 COMANDOS ÚTILES

### Ejecutar Prueba Completa:
```bash
cd c:\Users\Admin\Desktop\ZULY_IA_LOCAL
python prueba_real_completa.py
```

### Regenerar con Luces Corregidas:
```bash
python regenerar_con_luces_inteligentes.py
```

### Ver Estructura:
```bash
dir archivo_zuly\temp_arena\
dir archivo_zuly\por_estado_aprendizaje\mastered\
```

---

## ⚠️ REGLAS DE ORO

1. **Usuario es el Único Soberano** - Solo él aprueba ("OK")
2. **ZULY nunca aprueba solo** - Siempre espera confirmación
3. **JUES es técnico, no decisivo** - Da dictamen, no aprueba
4. **LYZU todo lo registra** - Memoria inmutable
5. **mastered/ es sagrado** - Solo con sello del Soberano
6. **temp_arena es temporal** - 24h de vida máximo
7. **ZULY_PROJECTS eliminado** - Ya no existe (legacy eliminado)

---

## 📞 PROTOCOLO DE EMERGENCIA

Si algo falla:
1. Revisar `archivo_zuly/bitacora/` por logs
2. Consultar LYZU: `core/cerebro_lyzu.py`
3. Verificar rutas en este manual
4. Regenerar desde temp_arena/

---

**Manual generado:** 2026-04-03  
**Responsable:** ZULY System v1.0  
**Próxima revisión:** Tras primera aprobación real
