# SESIÓN: 2026-03-07 - FIN DE SEMANA 4: VALIDACIÓN V2 CONTEXTUAL

## OBJETIVOS
- Implementar Validador V2 (contextual) para bloquear ejecuciones fuera de contexto.
- Integrar V2 en la cadena de validación del Agent (antes de la ejecución).
- Crear suite de tests unitarios y de integración.
- Documentar la convención oficial de nombres de archivos.

---

## IMPLEMENTACIÓN

### Componentes Creados

#### `core/validation/v2_validator.py` (NUEVO)
Validador contextual con 4 checks independientes ejecutados en cadena:

| Check | Qué verifica | Acción si falla |
|-------|-------------|-----------------|
| `check_blender_available` | Adapter activo y `is_available() == True` | **BLOQUEO** |
| `check_execution_mode` | Blender en `OBJECT` mode (no EDIT, SCULPT) | **BLOQUEO** |
| `check_active_collection` | Al menos una colección activa en escena | **BLOQUEO** |
| `check_base_file_path` | Archivo en `ZULY_PROJECTS/` o `ZULY_LAB/resultados_zuly/` | **ADVERTENCIA** (no bloqueo) |

**Principio central**: V2 nunca modifica el estado de la escena. Solo observa y bloquea.

**Comportamiento con MockAdapter**: Los checks son pasivos (sin contexto real, todo pasa).
Esto es correcto: MockAdapter es para simulación y no tiene un Blender real que validar.

#### `core/agent.py` (MODIFICADO)
- **Import** agregado: `from core.validation.v2_validator import V2Validator`
- **Instancia** agregada en `__init__`: `self.validator_v2 = V2Validator()`
- **Llamada pre-ejecución** en `process_natural_request()`:
  - V2 se ejecuta DESPUÉS de las verificaciones de seguridad (Protocolo Negro, Context Guard, Human Gate)
  - V2 se ejecuta ANTES del bucle de intentos de ejecución
  - Si V2 falla: retorno inmediato con error detallado + traza registrada en TraceCore

### Cadena de Validación Completa (Post-Semana 4)

```
Petición del usuario
    ↓
Protocolo Negro (bloqueo global)
    ↓
ContextGuard + HumanGate (seguridad de intención)
    ↓
V2Validator (contexto de ejecución) ← NUEVO SEMANA 4
    ↓
Ejecución del comando en Blender
    ↓
V0Validator (validación existencial - ¿apareció algo?)
    ↓
V1Validator (validación estructural - ¿es lo correcto?)
    ↓
Respuesta final al usuario
```

---

## VERIFICACIÓN EXITOSA ✅

- **Suite de tests**: `tests/test_v2_validator_weekend4.py`
- **Total tests**: 21
- **Resultado**: **21/21 PASADOS** ✅
- **Tiempo**: 0.581s

### Detalle de Tests

| Clase | Tests | Resultado |
|-------|-------|-----------|
| `TestV2ChecksIndividuales` | 15 | ✅ 15/15 |
| `TestV2ValidateCompleto` | 4 | ✅ 4/4 |
| `TestAgentV2Integracion` | 2 | ✅ 2/2 |

### Bloqueos Verificados (Casos Fuera de Contexto)
- ✅ Sin adapter → V2 bloquea con: `"No hay adapter activo"`
- ✅ Adapter no disponible → V2 bloquea con: `"Blender NO está disponible"`
- ✅ EDIT mode → V2 bloquea con: `"Modo de ejecución inválido 'EDIT'"`
- ✅ SCULPT mode → V2 bloquea con: `"Modo de ejecución inválido 'SCULPT'"`
- ✅ Sin colecciones (fuente Blender) → V2 bloquea con: `"No se detectaron colecciones"`

### Casos Válidos Verificados (Contexto Correcto)
- ✅ Adapter disponible + OBJECT mode + colección activa → V2 pasa
- ✅ MockAdapter (simulación) → V2 pasivo (permisivo)
- ✅ Archivo nuevo sin guardar → ruta no requerida, V2 pasa

---

## CONVENCIÓN DE NOMBRES (Registrada en Manual Sección 15)
Se documentó la convención oficial de nombres en `manuales/MANUAL_USO_ZULY_2026.md` (Sección 15):
- `.blend` de prueba de semana → `ZULY_PROJECTS/FDE_N_<etiqueta>_YYYYMMDD.blend`
- Log de sesión → `ZULY_LAB/logs_sesiones/LOG_FDE_N_YYYYMMDD.json`
- Log de test individual → `ZULY_LAB/logs_sesiones/LOG_TEST_<nombre>_YYYYMMDD_HHMMSS.json`

---

## FALSOS POSITIVOS DETECTADOS
- Ninguno. Los checks pasivos (MockAdapter, contexto vacío) funcionan correctamente.
- El check de ruta de archivo genera ADVERTENCIA (no bloqueo) cuando el archivo está fuera de las rutas oficiales. Decisión correcta: no bloquear proyectos nuevos.

---

## ARCHIVOS GENERADOS EN ESTA SESIÓN
| Archivo | Tipo | Ruta oficial |
|---------|------|-------------|
| `test` resultado 1 | txt temporal | Raíz (limpiar) |
| `test` resultado 2 | txt temporal | Raíz (limpiar) |

> **Nota**: Los archivos `v2_test_result.txt` y `v2_test_result2.txt` en la raíz del proyecto
> son temporales de debugging y deben eliminarse (no siguen la convención FDE_N).

---

## DECISIONES CLAVE
1. **V2 es pasivo con MockAdapter**: Correcto en diseño. Los tests unitarios necesitan MockAdapter.
   V2 en Blender real sí aplica todos los checks.
2. **Check de ruta es ADVERTENCIA, no BLOQUEO**: Un proyecto nuevo no tiene ruta hasta que se guarda.
   Bloquear aquí impediría el primer guardado.
3. **V2 corre después de seguridad pero antes de ejecución**: El orden correcto. Seguridad → Contexto → Ejecución.

---

## PRÓXIMOS PASOS (Semana 5)
- Pruebas reales en Blender headless con la cadena V0→V1→V2 completa
- Jerarquía de Memoria: Staging → Verified (3 ejecuciones perfectas = VERIFIED)
- Crear sistema de promoción controlada de patrones
