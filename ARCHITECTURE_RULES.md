# REGLAS DE ARQUITECTURA DE ZULY

**Fecha:** 24 de Enero de 2026  
**Fase:** 18.5 - Control de Complejidad  
**Estado:** ACTIVAS Y NO NEGOCIABLES

---

## 🎯 Propósito

Estas reglas NO son decoración.  
Son **ley técnica** que protege a ZULY del colapso.

Toda capacidad nueva debe ser:
- ✅ **Observable** (visible en system_report)
- ✅ **Testeable** (tiene tests)
- ✅ **Reversible** (se puede desactivar)

**Si no cumple las 3 → NO entra.**

---

## 📜 Reglas Fundamentales

### 1. Ningún módulo core importa `bpy` directamente

**Razón:** Desacoplamiento estratégico (Fase 17)

**Excepción:** Solo `BlenderAdapter` puede importar `bpy`

**Verificación:**
```bash
grep -r "import bpy" core/ --exclude-dir=adapters
# Debe retornar: 0 resultados
```

---

### 2. Todo adapter tiene fallback

**Razón:** ZULY debe funcionar sin Blender instalado

**Implementación:**
- `BlenderAdapter` → `MockAdapter` (automático)
- Nunca fallar silenciosamente

**Verificación:**
```python
agent = Agent(force_mock=True)
assert agent.engine_adapter.is_available() == True
```

---

### 3. Toda acción deja trace

**Razón:** Observabilidad total para el humano

**Implementación:**
- Usar `trace_core.append_trace()` en cada acción
- Formato: `{intention, execution_success, ...}`

**Verificación:**
```python
agent.execute("create_cube")
assert len(agent.trace_core.traces) > 0
```

---

### 4. Todo estado es observable

**Razón:** El humano manda porque ve todo

**Implementación:**
- `agent.system_report()` debe mostrar estado completo
- Incluir: Agent, Adapter, Módulos, Trace

**Verificación:**
```python
report = agent.system_report()
assert "ESTADO DEL SISTEMA" in report
assert "TRAZA" in report
```

---

### 5. Nada se ejecuta sin pasar por Agent

**Razón:** Punto único de control y observabilidad

**Implementación:**
- Toda acción va por `agent.process_natural_request()` o similar
- No llamar handlers directamente desde fuera

**Verificación:**
- Code review manual
- Arquitectura de capas respetada

---

## 🛑 Límites Técnicos

### Límite de Acciones por Sesión

```python
MAX_ACTIONS_PER_SESSION = 50
```

**Razón:** Evitar loops infinitos y uso descontrolado

**Implementación:** En `agent.execute()` verificar límite

---

### Registro de Módulos

**Razón:** Saber qué está vivo en ZULY

**Implementación:**
```python
from core.governance import registry
registry.register("ModuleName")
```

**Verificación:**
```python
snapshot = registry.snapshot()
assert "SceneMonitor" in snapshot
```

---

## ⚖️ Proceso de Cambio

### Para agregar nueva capacidad:

1. **Diseñar** con reglas en mente
2. **Implementar** con observabilidad
3. **Testear** end-to-end
4. **Documentar** en bitácora
5. **Registrar** módulo si aplica

### Para modificar regla existente:

1. **Justificación** técnica documentada
2. **Aprobación** explícita (humano raíz)
3. **Actualizar** este archivo
4. **Comunicar** cambio en bitácora

---

## 🚨 Violaciones

**Si se viola una regla:**

1. El sistema debe **fallar ruidosamente** (no silencioso)
2. El error debe ser **claro y específico**
3. La solución debe ser **obvia**

**Ejemplo:**
```python
if len(execution_history) >= MAX_ACTIONS_PER_SESSION:
    raise RuntimeError(
        "Límite de acciones por sesión alcanzado (50). "
        "Reinicia el Agent para continuar."
    )
```

---

## ✅ Verificación de Cumplimiento

### Checklist antes de commit:

- [ ] No hay `import bpy` fuera de adapters
- [ ] Nuevos módulos están registrados
- [ ] Acciones dejan trace
- [ ] Estado es observable en `system_report()`
- [ ] Tests E2E pasan
- [ ] Límites respetados

---

## 🧠 Filosofía

> **"ZULY no depende de tu memoria. ZULY depende de sus reglas."**

Estas reglas son el **freno** que permite que ZULY crezca sin colapsar.

Sin ellas, ZULY sería otro proyecto brillante que muere por complejidad.

Con ellas, ZULY es **ingeniería sostenible**.

---

**Firmado:**  
Gemini 2.0 Flash Thinking  
Fase 18.5 - Control de Complejidad  
24 de Enero de 2026
