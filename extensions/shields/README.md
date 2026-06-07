# Shield v1 - Escudo Externo de Comandos

**Versión:** 1.0  
**Tipo:** Validación estática  
**Ubicación:** `extensions/shields/`

---

## Qué Hace

Shield v1 valida comandos ANTES de que lleguen al core según reglas estáticas.

**Funciones:**
- ✅ Valida tipo de comando
- ✅ Valida estructura mínima
- ✅ Bloquea comandos no permitidos
- ✅ Devuelve ALLOW / DENY + razón

---

## Qué NO Hace

**Prohibido absolutamente:**

❌ **NO ejecuta comandos** - Solo valida  
❌ **NO decide "inteligentemente"** - Solo reglas estáticas  
❌ **NO lee estado del core** - Estado es privado  
❌ **NO importa módulos del core** - Solo interfaces públicas si es necesario  
❌ **NO tiene heurísticas** - Solo reglas explícitas  
❌ **NO tiene timers o retries** - Un comando = un intento  
❌ **NO modifica comandos** - Solo ALLOW o DENY

---

## Regla de Oro

> **"El shield solo autoriza o bloquea, nunca ejecuta."**

---

## Uso

```python
from extensions.shields.shield_v1 import ShieldV1

# Comando a validar
command = {
    'type': 'explicit_human',
    'callable': my_function
}

# Validar
result = ShieldV1.validate_command(command)

if result['allowed']:
    # Comando permitido, proceder
    execute_command(command['callable'])
else:
    # Comando bloqueado
    print(f"Bloqueado: {result['reason']}")
```

---

## Reglas Estáticas

### Tipos Permitidos
- `explicit_human` - Comando humano explícito
- `manual_test` - Test manual controlado

### Tipos Bloqueados
- `implicit` - Comandos implícitos
- `derived` - Inferidos
- `automatic` - Generados por el sistema
- `state_based` - Basados en estado
- `pattern_based` - Basados en patrones
- `self_generated` - Generados por ZULY
- `timed` - Disparados por tiempo
- `conditional` - Condicionales
- `heuristic` - Heurísticos

### Campos Obligatorios
- `type` - Tipo de comando
- `callable` - Función a ejecutar

---

## Arquitectura

```
extensions/shields/
├── shield_v1.py        # Lógica de validación
├── rules.py            # Reglas estáticas
├── README.md           # Este archivo
└── tests/
    └── test_shield_v1_minimal.py
```

---

## Tests

**6 tests mínimos:**
1. El shield existe
2. Permite comando válido
3. Bloquea comando inválido
4. Bloquea campo faltante
5. Shield NO ejecuta
6. Shield NO importa core

**Ejecutar:**
```bash
python extensions\shields\tests\test_shield_v1_minimal.py
```

---

## Garantías

✅ **NO toca `/core`** - El core es inmutable  
✅ **NO ejecuta** - Solo valida  
✅ **NO decide** - Solo reglas estáticas  
✅ **NO lee estado** - Estado es privado

---

*Shield v1 - Escudo Externo*  
*"Solo autoriza o bloquea, nunca ejecuta"*
