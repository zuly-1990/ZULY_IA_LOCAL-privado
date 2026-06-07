# Command Gate - Puerta de Comandos Explícitos

**Fase:** 5.17  
**Tipo:** Puerta pasiva de validación  
**Propósito:** Definir la única vía legítima para recibir órdenes externas

---

## ¿Qué es?

CommandGate es una **puerta pasiva de validación** que define la única vía legítima por la cual ZULY puede recibir una orden externa.

**NO es:**
- ❌ Un intérprete de lenguaje natural
- ❌ Un generador de comandos
- ❌ Un sistema de ejecución

**SÍ es:**
- ✅ Una definición de tipos de comandos permitidos
- ✅ Una lista de tipos prohibidos
- ✅ Una barrera de entrada

---

## ¿Por qué existe?

**Problema:** ZULY podría recibir comandos de múltiples fuentes (estado, patrones, tiempo, errores).

**Riesgo:** Comandos automáticos o implícitos podrían ejecutarse sin autorización humana explícita.

**Solución:** CommandGate define que **solo comandos explícitos y humanos pueden pasar**.

### Principio Rector

> **"Obedecer no implica comprender."**

ZULY puede ejecutar un comando sin entenderlo, sin evaluarlo y sin desear nada.

---

## ¿Qué NO permite?

### Tipos de Comandos PROHIBIDOS (9)

CommandGate prohíbe los siguientes tipos de comandos:

1. **`implicit`** - Comandos implícitos
2. **`derived`** - Comandos inferidos
3. **`automatic`** - Generados por el sistema
4. **`state_based`** - Basados en estado observado
5. **`pattern_based`** - Basados en patrones memorizados
6. **`self_generated`** - Generados por ZULY
7. **`timed`** - Disparados por paso del tiempo
8. **`conditional`** - Comandos condicionales
9. **`heuristic`** - Comandos heurísticos

**Ninguno de estos puede ejecutarse.**

### Tipos de Comandos PERMITIDOS (2)

Solo 2 tipos explícitos están permitidos:

1. **`explicit_human`** - Comando humano explícito
2. **`manual_test`** - Tests controlados manualmente

**Solo lo explícito y humano puede pasar.**

---

## Uso

```python
from core.command.command_gate import CommandGate

# Verificar si un tipo de comando está prohibido
if CommandGate.is_forbidden('automatic'):
    # NO ejecutar comando automático
    pass

# Solo permitir comandos explícitos
if CommandGate.is_allowed('explicit_human'):
    # OK: comando humano explícito
    execute_command(user_command)
```

**CRÍTICO:** CommandGate NO ejecuta comandos, solo define límites.

---

## Garantías

✅ **CommandGate NO depende de Agent**  
✅ **CommandGate NO importa StateAwareness**  
✅ **CommandGate NO importa IntentionBoundary**  
✅ **CommandGate NO importa PatternMemory**  
✅ **CommandGate NO ejecuta lógica**  
✅ **CommandGate solo define límites**

---

## Resultado

Después de Fase 5.17:

- ✅ Estado observable (5.14)
- ✅ Estado aislado (5.15)
- ✅ Intención bloqueada (5.16)
- ✅ Comandos filtrados (5.17)

**Nada ocurre sin que un humano lo ordene explícitamente.**

---

## Mensaje Final

> **"Mandar no implica pensar.  
> Obedecer no implica decidir."**

CommandGate asegura que ZULY:
- Puede recibir órdenes
- Solo de humanos
- Solo explícitas
- Sin interpretación

**Esto es control de entrada, no funcionalidad.**

---

*Fase 5.17 - Command Gate*  
*Puerta de comandos explícitos*  
*"Obedecer no implica comprender"*
