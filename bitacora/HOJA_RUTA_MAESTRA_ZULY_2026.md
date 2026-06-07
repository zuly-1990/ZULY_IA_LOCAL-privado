# 🧭 HOJA DE RUTA MAESTRA ZULY 2026

## Endurecimiento Cognitivo + Pruebas Reales + Preparación Fase 6

**Modalidad:** Trabajo fines de semana
**Estado actual:** 🚨 ULTRA EMERGENCIA (activada 2026-03-21)
**Fase activa:** U1 — Contención Inmediata (V0, HumanGate, Handlers)
**Bitácora de avances:** `bitacora/ULTRA_EMERGENCIA.md`

---

# 🎯 PROPÓSITO DEL PLAN

Consolidar a ZULY como:
* Motor determinista validado físicamente.
* Sistema de memoria no contaminable.
* Arquitectura desacoplada y coherente (Agent vs Lyzu).
* Plataforma capaz de activar Fase 6 sin riesgo estructural.

Si al finalizar este plan ZULY puede ejecutar patrones complejos bajo V0 + V1 + V2 sin errores ni contaminación durante 60 días continuos, entonces todo lo construido fue exitoso.

---

# 🧠 PRINCIPIOS RECTORES

1. MAC-0 gobierna todo.
2. No se activa Fase 6 sin memoria saneada.
3. Ningún patrón es verdad hasta demostrar estabilidad repetida.
4. Todo avance debe registrarse en bitácora.
5. Si no está documentado, no existe.
6. No agregar inteligencia sin fortalecer estructura.

---

# 📆 PLAN COMPLETO POR FINES DE SEMANA

---

## 🗓 FIN DE SEMANA 1
**ETIQUETA: SANEAMIENTO DE MEMORIA (Estructural Base)**
**ESTADO: ✅ COMPLETADO (2026-02-28)**
*Objetivo:* Eliminar riesgo de contaminación cognitiva.
*Tareas (Todas realizadas con TDD y Clean Architecture):*
* ✅ Crear: `patterns_staging.json`, `patterns_verified.json`, `patterns_quarantine.json`
* ✅ Migrar todos los patrones actuales a STAGING mediante script seguro `migrate_patterns_to_staging.py`.
* ✅ Agregar campos obligatorios de entorno: `origin`, `blender_version`, `active_mode`, `environment_hash`, `engine_adapter_version`. Implementado con algoritmo SHA256 sobre la escena base.
* ✅ Desactivar auto-memorización (Agente Central reactivo pasivo en stand-by estructural).
*Registro oficial generado:* `bitacora/SESION_2026-02-28_FIN_DE_SEMANA_1_SANEAMIENTO.md`

## 🗓 FIN DE SEMANA 2
**ETIQUETA: REESCRITURA DE EVOCACIÓN (Corrección Crítica)**
**ESTADO: ✅ COMPLETADO (2026-03-01)**
*Objetivo:* Eliminar dependencia exclusiva de similitud textual.
*Tareas (Todas realizadas con TDD y Clean Architecture):*
* ✅ Implementar `contextual_match()` en nuevo módulo `core/learning/contextual_matcher.py`
* ✅ Comparar: snapshot actual vs scene_before, active_mode, colección activa, archivo base, hash estructural
* ✅ Si falla algo → NO EVOCAR. Log detallado del rechazo. 3 vetos absolutos implementados (hash, mode, version).
*Registro oficial generado:* `bitacora/SESION_2026-03-01_FIN_DE_SEMANA_2_EVOCACION.md`
*Registro obligatorio verificado:*
* ✅ Casos donde se bloquea correctamente (5 tests de bloqueo)
* ✅ Pruebas comparativas antes/después (modo legacy vs contextual)
* ✅ Impacto en latencia: 100 ops < 50ms confirmado

## 🗓 FIN DE SEMANA 3
**ETIQUETA: VALIDACIÓN V1 (Estructural Profunda) | COMPLETADO ✅ (2026-03-01)**
*Objetivo:* Detectar diferencias estructurales no visibles en V0.
*Tareas:*
* ✅ Implementar Validador V1 (Tipos, Jerarquías, Vértices) en `core/validation/v1_validator.py`
* ✅ Actualizar `StateSnapshot` y `Adapters` para captura de datos estructurales
* ✅ Integrar V1 después de V0 en `Agent`. Bloqueo lógico si falla.
* ✅ Verificar con suite de tests: `tests/test_v1_validator_weekend3.py` (6/6 PASS)
*Registro oficial generado:* `bitacora/SESION_2026-03-01_FIN_DE_SEMANA_3_VALIDACION_V1.md`

## 🗓 FIN DE SEMANA 4
**ETIQUETA: VALIDACIÓN V2 (Contextual) | COMPLETADO ✅ (2026-03-07)**
*Objetivo:* Bloquear ejecución fuera de contexto.
*Tareas:*
* ✅ Implementar `V2Validator` (Contextual) en `core/validation/v2_validator.py`
  * ✅ `check_blender_available` — bloquea si no hay adapter activo
  * ✅ `check_execution_mode` — bloquea en EDIT/SCULPT mode (solo OBJECT válido)
  * ✅ `check_active_collection` — bloquea si no hay colecciones en escena
  * ✅ `check_base_file_path` — advierte si el archivo está fuera de rutas oficiales
* ✅ Integrar V2 en `Agent.process_natural_request()` (pre-ejecución, post-seguridad)
* ✅ Suite de tests: `tests/test_v2_validator_weekend4.py` (**21/21 PASS**)
* ✅ Convención de nombres registrada en `manuales/MANUAL_USO_ZULY_2026.md` (Sección 15)
*Registro oficial generado:* `bitacora/SESION_2026-03-07_FIN_DE_SEMANA_4_VALIDACION_V2.md`
*Registro obligatorio verificado:*
* ✅ Bloqueos correctos: sin adapter, EDIT mode, SCULPT mode, sin colecciones
* ✅ Falsos positivos: ninguno detectado
* ✅ Cadena completa: V2 (pre) → Ejecución → V0 (post) → V1 (post)


## 🗓 FIN DE SEMANA 5
**ETIQUETA: JERARQUÍA DE MEMORIA (Staging -> Verified) | COMPLETADO ✅ (2026-03-07)**
*Objetivo:* Crear sistema de promoción controlada y jerarquizada.
*Logros:*
* ✅ Patrones nacen en `STAGING` y requieren permiso (`ASK`).
* ✅ Promoción a `VERIFIED` tras 3 éxitos consecutivos.
* ✅ Degradación a `QUARANTINE` tras 2 fallos.
* ✅ Persistencia física del movimiento de archivos.
*Registro oficial:* `bitacora/SESION_2026-03-07_FIN_DE_SEMANA_5_JERARQUIA_MEMORIA.md`

---

# 🚨🔥 ULTRA EMERGENCIA — MÁXIMA PRIORIDAD 🔥🚨

> **Estado:** CRÍTICO CONTROLABLE
> **Activado:** 2026-03-21
> **Motivo:** Auditoría técnica total reveló fallos que pueden destruir la confianza del sistema
> **Bitácora:** `bitacora/ULTRA_EMERGENCIA.md`
>
> ⛔ **REGLA:** Nada de lo que está debajo (FdS 6-8) se toca hasta completar U1-U5.
> ❌ **PROHIBIDO:** Nuevos handlers grandes, Fase 6, IA más inteligente, refactors masivos.

---

## 🔴 U1 — CONTENCIÓN INMEDIATA
**ESTADO: [/] EN PROCESO**
*Objetivo:* ZULY NO MIENTE. ZULY NO EJECUTA SIN PERMISO.
*Tareas:*
* [x] Registrar 5 handlers faltantes (delete, duplicate, select, deselect, select_all_by_type) — `selection.py`
* [x] Corregir numeración duplicada en `agent.py` (pasos 6→13)
* [x] Crear formato de bitácora PRO — `bitacora/ULTRA_EMERGENCIA.md`
* [x] **Corregir V0 pasivo** — `effect=None` retorna `passive: True` + WARNING + bloqueo memorización ✅
* [x] **Corregir HumanGate** — `ASK` retorna `success: False` + `BLOCKED_AWAITING_CONFIRMATION` ✅
* [x] Verificar pipeline E2E: crear → mover → eliminar ✅
*Registro obligatorio:* Cada corrección en `bitacora/ULTRA_EMERGENCIA.md` ✅

**Estado U1: COMPLETADO 🟢**
## 🟠 U2 — SANEAR MEMORIA
**ESTADO: ✅ COMPLETADO**
*Objetivo:* ZULY APRENDE SOLO LO REAL. NO APRENDE BASURA.
*Tareas:*
* [x] Limpiar duplicados en staging (3 patrones idénticos "Crea una esfera azul") ✅
* [x] Revisar quarantine (2 patrones "cilindro roto") ✅
* [x] Reactivar auto-memorización CONTROLADA (V0 OK + confianza ≥ 0.85 + attempts == 1 + modo != HYBRID + snapshot no vacío) ✅
* [x] Implementar deduplicación (texto > 95% similar + mismo command_name → rechazar) ✅
* [x] Validar que snapshot no esté vacío → si `scene_before: {}` → NO guardar patrón ✅
*Registro obligatorio:* Cada patrón: origen, validación, resultado ✅

**Estado U2: COMPLETADO 🟢**

## 🟡 U3 — PRUEBAS REALES EN BLENDER
**ESTADO: ✅ COMPLETADO (2026-03-21)**
*Objetivo:* Validar comportamiento real.
*Tareas:*
* [x] Crear script `scripts/u3_real_test.py` automatizado ✅
* [x] Ejecutar: crear objeto → verificar V0 → mover → verificar → eliminar → verificar ✅
* [x] Probar: repetir comando → verificar que usa memoria ✅
* [x] Probar: activar evidencia física (Condition 6 - snapshots) ✅
*Registro oficial generado:* `bitacora/SESION_2026-03-21_ESTABILIZACION_U3.md`

## 🟢 U4 — ESTABILIZACIÓN / AUDITORÍA V2
**ESTADO: ✅ COMPLETADO (2026-03-21)**
*Objetivo:* Evitar degradación y sanear completamente la memoria.
*Tareas:*
* [x] Mover patrones malos/legados → quarantine ✅
* [x] Realizar Auditoría V2 completa (Mapeo total) ✅
* [x] Generar reporte final de confianza ✅
*Registro oficial:* `bitacora/AUDITORIA_V2_RESULTADOS.md`

## 🔵 U5 — LIMPIEZA ESTRUCTURAL
**ESTADO: ⏳ PENDIENTE (puede ejecutarse en paralelo)**
*Objetivo:* Reducir desorden del proyecto.
*Tareas:*
* [ ] Organizar raíz (248 archivos → mover debug, logs, scripts repetidos a carpetas)
* [ ] Separar archivos de debug vs producción
* [ ] Eliminar archivos muertos (pseudo-handlers viejos en `core/commands/`)

---

# ❄️ FASES CONGELADAS (Reanudar tras Ultra Emergencia)

---

## 🗓 FIN DE SEMANA 6
**ETIQUETA: MODELADO IMPECABLE (Arquitectura Analítica)**
**ESTADO: ❄️ CONGELADO (Era [/] EN PROCESO — Pausado por Ultra Emergencia)**
*Objetivo:* Alcanzar la perfección geométrica y la justificación física de cada malla.
*Metas Obligatorias:*
* [x] **TOPOLOGÍA ESTANCA (Watertight):** 100% de mallas cerradas, sin caras internas, listas para Impresión 3D profesional.
* [x] **BISELADO ESTRUCTURAL (Bevel Tech):** Implementación de biseles reales en todas las aristas vivas para captura de luz natural.
* [x] **MODELADO SUSTRACTIVO (Boolean Workflow):** Ventanas y vanos creados mediante sustracción real, no superposición.
* [x] **VALIDADOR V3 (Métrica & Topología):** Creación de un agente de auditoría que verifique bordes no-manifold y superposición de geometría.
* [ ] **EFICIENCIA DE INSTANCIAS:** Implementación de `Linked Data` para rascacielos y mobiliario, reduciendo el peso del archivo .blend en un 70%.
* [ ] **RETO 6.8: ZULY LAB (Ingeniería Inversa Cognitiva):** Extracción de patrones topológicos de modelos creados por el humano.
* [ ] **INFORME DE JUSTIFICACIÓN:** ZULY debe explicar la razón técnica de cada parámetro geométrico.
*Registro obligatorio:* Proyecto .blend de Ciudad 7.0 (Geometría Pura) y reporte de validación física.

## 🗓 FIN DE SEMANA 7
**ETIQUETA: AUDITORÍA CEREBRAL (ZULY vs LYZU)**
**ESTADO: ❄️ CONGELADO**
*Objetivo:* Eliminar superposición detectada.
*Tareas:*
* Mapear responsabilidades de `agent.py` y `lyzu_core.py`.
* Aplicar DRY (Don't Repeat Yourself). Refactorizar arquitectura.
*Registro obligatorio:* Diagrama actualizado, Código eliminado/refactorizado.

## 🗓 FIN DE SEMANA 8
**ETIQUETA: EVALUACIÓN FINAL Y DECISIÓN FASE 6**
**ESTADO: ❄️ CONGELADO**
*Objetivo:* Determinar si puede habilitarse autonomía controlada.
*Condiciones mínimas:* V0/V1/V2 estables, Memoria jerárquica funcionando, 0 ejecuciones fuera de contexto, 60 días sin contaminación.
*Registro obligatorio:* Informe técnico final, Riesgo, Decisión de Fase 6.

---

# 🧪 FASE FINAL — RE-AUDITORÍA Y VALIDACIÓN DE METAS

## 🗓 POST ULTRA EMERGENCIA
**ETIQUETA: AUDITORÍA TÉCNICA TOTAL v2**
**ESTADO: ⏳ PENDIENTE (Se ejecuta al completar U1-U5)**
*Objetivo:* Repetir la auditoría completa (9 fases) para validar que todas las correcciones surten efecto.
*Tareas:*
* [ ] Ejecutar auditoría técnica total (mismas 9 fases del informe 2026-03-21)
* [ ] Comparar resultados vs auditoría v1 (estado antes vs después)
* [ ] Validar que V0 ya no miente (0 falsos positivos)
* [ ] Validar que HumanGate bloquea realmente
* [ ] Validar que memoria no contiene duplicados
* [ ] Validar que auto-memorización funciona con controles
* [ ] Confirmar 42 handlers registrados y funcionales
* [ ] Pipeline E2E: crear → mover → material → eliminar → repetir patrón
* [ ] Generar informe comparativo: ANTES vs DESPUÉS
*Condición de éxito:*
> Si ZULY puede: recibir comando → ejecutar → validar V0+V1+V2 → memorizar → repetir correctamente
> → **TODO LO CONSTRUIDO FUE UN ÉXITO REAL**
*Registro obligatorio:* `bitacora/ULTRA_EMERGENCIA.md` (sección final) + informe de auditoría v2

### [PROCESO] ZULY LABORATORIO: INGENIERÍA INVERSA (2026-03-21)
- **Hito**: Primer Escaneo Pasivo (Scan & Learn) sobre modelo real `casarural.blend`.
- **Logro**: Extracción exitosa de ADN topológico (`adn_casa_rural_v1.json`).
- **Verificación**: Auditoría V3 ejecutada sobre mallas complejas; detección precisa de 71 bordes no-estancos en el objeto 'Куб'.
- **Estado**: **FUNCIONAL**. El laboratorio puede aprender de archivos externos y validar su integridad antes de la síntesis.

---

# 🚀 FASES ESTRATÉGICAS FUTURAS (A Definir)

## 🗓 FASE X — SOBERANÍA COGNITIVA (Propuesta)
**Objetivo:** Eliminar dependencia externa y error humano.
*   **Autocorrección Autónoma (Self-Correction):** Aprendizaje y corrección automática desde la `Quarantine`.
*   **AI Geometry Nodes:** Control procedural nativo avanzado.
