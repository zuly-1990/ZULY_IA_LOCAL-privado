# ORDEN DE TRABAJO: FASE 5.16 — PRUEBAS DE CONFIANZA Y ESTABILIDAD

**Origen:** Instrucción directa del Arquitecto (Sesión anterior)
**Objetivo:** Confirmar que la Conciencia Contextual de ZULY no miente, no se rompe y no asume cosas incorrectas.

## 🚫 Restricciones
- No avanzar a Fase 6 todavía.
- No ejecutar operadores de Blender aún.
- No modificar escenas.

## 🧪 Batería de Pruebas Requerida

### 🔹 PRUEBA 1 — Escena Vacía
- **Condición:** Blender abierto, archivo nuevo, sin objetos.
- **Esperado:**
    - `object_count = 0`
    - Colección raíz existe.
    - `semantic.scene_type = "EMPTY_SCENE"`
    - Confianza alta.

### 🔹 PRUEBA 2 — Escena Simple Controlada
- **Condición:** Añadir 1 Cubo, 1 Luz, crear 2 colecciones manualmente.
- **Esperado:**
    - Jerarquía de colecciones correcta (padres/hijos).
    - Objeto en colección correcta.
    - Semántica coherente.

### 🔹 PRUEBA 3 — Cambio en Vivo
- **Condición:** Ejecutar `analyze_scene()`, mover objeto de colección, ejecutar de nuevo.
- **Esperado:**
    - Snapshot refleja el cambio.
    - Estructura actualizada.
    - Sin "fantasmas" de memoria vieja.

### 🔹 PRUEBA 4 — Contexto Incorrecto
- **Condición:** Ejecutar fuera de Blender.
- **Esperado:**
    - `source = "no_blender"` (o `is_blender = False`)
    - Semántica bloqueada o vacía.
    - Agente no propone acciones.

## ✅ Criterio de Éxito
Si las 4 pruebas pasan, se habilita **Fase 6 – Observación Activa**.
