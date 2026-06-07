# Intention Boundary - Cortafuegos de Intención

**Fase:** 5.16  
**Tipo:** Límite cognitivo pasivo  
**Propósito:** Asegurar que ninguna señal genere intención automáticamente

---

## ¿Qué es?

IntentionBoundary es un **cortafuegos semántico pasivo** que define explícitamente qué NO puede convertirse en intención dentro de ZULY.

**NO es:**
- ❌ Un generador de intenciones
- ❌ Un sistema de decisión
- ❌ Un disparador de acciones

**SÍ es:**
- ✅ Una definición de límites cognitivos
- ✅ Una lista de fuentes prohibidas
- ✅ Una barrera arquitectónica

---

## ¿Por qué existe?

**Problema:** ZULY puede observar estado, patrones, errores, métricas.

**Riesgo:** Esas observaciones podrían convertirse automáticamente en intenciones o acciones.

**Solución:** IntentionBoundary define explícitamente que **percibir no implica querer**.

### Principio Rector

> **"Percibir no implica querer."**

ZULY puede observar, registrar y monitorear.  
Pero no puede desear, decidir o actuar a partir de eso.

---

## ¿Qué NO permite?

### Fuentes PROHIBIDAS de Intención (10)

IntentionBoundary prohíbe que las siguientes fuentes generen intención:

1. **`state_snapshot`** - Estado observado
2. **`logs`** - Logs del sistema
3. **`metrics`** - Métricas internas
4. **`errors`** - Errores
5. **`performance_data`** - Rendimiento
6. **`pattern_memory`** - Patrones memorizados
7. **`history`** - Historial de ejecución
8. **`external_signals`** - Señales externas
9. **`time_elapsed`** - Paso del tiempo
10. **`self_reflection`** - Autorreferencia

**Ninguna de estas puede generar intención automáticamente.**

### Fuentes PERMITIDAS de Intención (3)

Solo 3 fuentes explícitas están permitidas:

1. **`explicit_command`** - Comando explícito del usuario
2. **`manual_trigger`** - Disparo manual autorizado
3. **`controlled_test`** - Tests controlados

**Solo lo explícito puede generar intención.**

---

## Uso

```python
from core.intention.intention_boundary import IntentionBoundary

# Verificar si una fuente está prohibida
if IntentionBoundary.is_forbidden('state_snapshot'):
    # NO generar intención a partir del estado
    pass

# Obtener lista de fuentes prohibidas
forbidden = IntentionBoundary.get_forbidden_sources()
```

**CRÍTICO:** IntentionBoundary NO ejecuta lógica, solo define límites.

---

## Garantías

✅ **IntentionBoundary NO depende de Agent**  
✅ **IntentionBoundary NO importa StateAwareness**  
✅ **IntentionBoundary NO importa PatternMemory**  
✅ **IntentionBoundary NO ejecuta lógica**  
✅ **IntentionBoundary solo define límites**

---

## Resultado

Después de Fase 5.16:

- ✅ Estado observable (5.14)
- ✅ Estado aislado (5.15)
- ✅ Intención bloqueada (5.16)

**ZULY aún no quiere nada. Y eso es exactamente lo correcto.**

---

## Mensaje Final

> **"Conocer no implica actuar.  
> Percibir no implica desear."**

IntentionBoundary asegura que ZULY:
- Puede observar
- No puede querer
- No puede decidir por sí misma

**Esto es seguridad cognitiva, no funcionalidad.**

---

*Fase 5.16 - Intention Boundary*  
*Cortafuegos de intención*  
*"Percibir no implica querer"*
