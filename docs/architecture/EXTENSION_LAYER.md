# ZULY Extension Layer - Arquitectura Externa

**Versión Core:** v1.0 (INMUTABLE)  
**Fecha:** 3 de Enero de 2026  
**Propósito:** Definir cómo se extiende ZULY sin tocar el núcleo

---

## Principio Rector

> **"La inteligencia vive fuera del núcleo."**

El core garantiza seguridad.  
Las capas externas experimentan.

---

## Regla Absoluta

**Si algo requiere tocar `/core` → queda automáticamente prohibido.**

El núcleo es INMUTABLE. Todo lo que venga después debe ser externo.

---

## Estructura de Extensiones

### Ubicación

```
ZULY_IA_LOCAL/
├── core/                    # INMUTABLE - NO TOCAR
│   ├── VERSION
│   ├── state/
│   ├── intention/
│   ├── command/
│   ├── execution/
│   └── learning/
│
└── extensions/              # MUTABLE - Experimentación permitida
    ├── README.md
    ├── shields/             # Escudos y protecciones
    ├── sandboxes/           # Entornos aislados
    ├── plugins/             # Plugins externos
    └── tools/               # Herramientas y wrappers
```

---

## Cómo Interactúa una Extensión con el Core

### 1. Envío de Comandos Explícitos

**Regla:** Solo a través de interfaces públicas del core.

```python
# ✅ CORRECTO - Uso de interfaz pública
from core.command.command_gate import CommandGate
from core.execution.execution_shell import ExecutionShell

# Verificar que el comando es permitido
if CommandGate.is_allowed('explicit_human'):
    # Ejecutar a través del shell
    result = ExecutionShell.execute(validated_function, args)
```

```python
# ❌ PROHIBIDO - Acceso directo al núcleo
from core.agent import Agent
agent = Agent()
agent.process_natural_request("comando")  # NO - Bypasea gates
```

### 2. Recepción de Resultados

**Regla:** Solo recibir lo que el core expone explícitamente.

```python
# ✅ CORRECTO - Recibir resultado de ejecución
result = ExecutionShell.execute(function)
# Procesar resultado sin modificar core
process_result(result)
```

```python
# ❌ PROHIBIDO - Leer estado interno
from core.state.state_awareness import StateAwareness
snapshot = StateAwareness.snapshot()  # NO - Estado es privado
```

### 3. Estado Prohibido

**NO se puede leer:**
- Estado interno del agent
- Snapshots de StateAwareness
- Memoria de PatternMemory
- Validaciones de V0Validator

**El estado del core es PRIVADO.**

---

## Qué es un Sandbox

Un **sandbox** es un entorno aislado donde una extensión puede:

- ✅ Experimentar con lógica propia
- ✅ Usar IA/ML localmente
- ✅ Tomar decisiones internas
- ✅ Aprender de sus propios datos

**Pero:**
- ❌ NO puede modificar el core
- ❌ NO puede leer estado prohibido
- ❌ NO puede generar comandos automáticos

**Ejemplo de sandbox:**
```
extensions/sandboxes/experimental_ai/
├── model.py          # IA local
├── data/             # Datos propios
└── interface.py      # Interfaz con core (solo comandos explícitos)
```

---

## Dónde Viven los "Escudos"

Los **escudos** son capas de protección que:

- Validan comandos antes de enviarlos al core
- Filtran resultados antes de exponerlos
- Añaden capas de seguridad adicionales
- Monitorizan uso del sistema

**Ubicación:** `extensions/shields/`

**Ejemplo de escudo:**
```python
# extensions/shields/command_validator.py

class CommandValidator:
    """
    Escudo que valida comandos antes de enviarlos al core.
    """
    
    @staticmethod
    def validate_command(command_text):
        # Validación adicional
        if is_safe(command_text):
            return True
        return False
```

**Los escudos NO modifican el core, lo protegen desde fuera.**

---

## Qué NO Puede Hacer Jamás una Extensión

### Prohibido Absolutamente

1. ❌ **Modificar archivos en `/core`**
2. ❌ **Importar y modificar clases del core**
3. ❌ **Leer estado interno prohibido**
4. ❌ **Generar comandos automáticos**
5. ❌ **Bypasear CommandGate**
6. ❌ **Acceder directamente a ExecutionShell sin validación**
7. ❌ **Modificar PatternMemory**
8. ❌ **Alterar StateGuard o IntentionBoundary**
9. ❌ **Conectarse directamente con Agent**
10. ❌ **Romper límites del núcleo**

### Regla de Oro

> **"Si una extensión necesita modificar el core para funcionar, entonces NO debe existir."**

---

## Reglas de Interacción con el Core

### 1. Solo Interfaces Públicas

Las extensiones SOLO pueden usar:
- `CommandGate` - Para verificar tipos de comandos
- `ExecutionShell.execute()` - Para ejecutar callables validados

**Nada más.**

### 2. Comandos Explícitos

Toda interacción debe ser a través de comandos explícitos:
- Tipo: `explicit_human` o `manual_test`
- Validados externamente
- Sin automatización

### 3. Sin Lectura de Estado

Las extensiones NO pueden:
- Leer snapshots de StateAwareness
- Consultar PatternMemory
- Acceder a validaciones V0
- Leer estado del Agent

**El estado es PRIVADO del core.**

### 4. Sin Modificación

Las extensiones NO pueden:
- Modificar archivos del core
- Alterar comportamiento del núcleo
- Añadir métodos a clases del core
- Romper límites establecidos

---

## Ejemplo de Extensión Mínima

```python
# extensions/plugins/simple_wrapper.py

"""
Ejemplo de extensión mínima que respeta el core.
"""

from core.execution.execution_shell import ExecutionShell
from core.command.command_gate import CommandGate


class SimpleWrapper:
    """
    Wrapper simple que usa el core sin modificarlo.
    """
    
    def execute_safe_command(self, validated_callable, *args, **kwargs):
        """
        Ejecuta un comando ya validado.
        
        Esta extensión NO valida, solo envuelve.
        La validación ocurre ANTES de llegar aquí.
        """
        # Verificar que es un comando permitido (redundante pero seguro)
        if not CommandGate.is_allowed('explicit_human'):
            raise ValueError("Tipo de comando no permitido")
        
        # Ejecutar a través del shell
        result = ExecutionShell.execute(validated_callable, *args, **kwargs)
        
        # Procesar resultado (sin modificar core)
        return self._process_result(result)
    
    def _process_result(self, result):
        """
        Procesa resultado sin tocar el core.
        """
        # Lógica de la extensión
        return {"processed": True, "result": result}
```

**Características:**
- ✅ Usa interfaces públicas
- ✅ No modifica el core
- ✅ No lee estado prohibido
- ✅ Respeta límites

---

## Declaración Explícita

**EL CORE NO SE TOCA.**

A partir de ZULY CORE v1.0:

- El núcleo es INMUTABLE
- Las extensiones son MUTABLES
- El core garantiza seguridad
- Las extensiones experimentan

**Toda la inteligencia, aprendizaje y autonomía vive FUERA del core.**

---

## Próximos Pasos (Fuera de Fase 7.0)

Después de establecer la arquitectura:

1. **Shields** - Capas de protección
2. **Sandboxes** - Entornos experimentales
3. **Plugins** - Funcionalidad extendida
4. **Tools** - Herramientas y wrappers

**Todo externo. Todo respetuoso del núcleo.**

---

*Arquitectura Externa - ZULY Extension Layer*  
*Core v1.0 (INMUTABLE)*  
*"La inteligencia vive fuera del núcleo"*
