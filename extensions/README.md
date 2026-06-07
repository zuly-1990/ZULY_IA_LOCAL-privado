# ZULY Extensions

**Core Version:** v1.0 (IMMUTABLE)  
**Purpose:** External extensions that use ZULY without modifying the core

---

## Structure

```
extensions/
├── README.md           # This file
├── shields/            # Protection layers
├── sandboxes/          # Isolated experimental environments
├── plugins/            # External plugins
└── tools/              # Tools and wrappers
```

---

## Rules

1. **Never modify `/core`** - The core is immutable
2. **Use public interfaces only** - CommandGate, ExecutionShell
3. **No state reading** - Core state is private
4. **Explicit commands only** - No automation

---

## Getting Started

See [`docs/architecture/EXTENSION_LAYER.md`](../docs/architecture/EXTENSION_LAYER.md) for complete architectural documentation.

---

*Extensions live outside the core*  
*Intelligence lives outside the core*  
*Everything experimental lives outside the core*
