# Estructura del Ecosistema ZULY (Fase 5.15)

## 🧠 ZULY CORE (`/core`)
*El cerebro inmutable y seguro.*
```text
core/
├── agent.py                 # Cerebro central (Identidad, NLU, Ejecución)
├── version                  # Estado inmutable (v1.0 Frozen)
├── environment/             # [NUEVO] Sentidos Pasivos
│   └── blender_observer.py  # Ojos de Zuly (Fase 5.15)
├── state/                   # Conciencia
│   └── state_awareness.py   # Autoconciencia pasiva (Fase 5.14)
├── security/                # Sistema Inmune
│   └── identity.py          # Verificación de Autor
├── learning/                # Memoria
│   └── pattern_memory.py    # Memoria de Patrones de Éxito
├── validation/              # Juez de Realidad
│   └── v0_validator.py      # Verificación Estructural V0
├── intention/               # Intenciones
├── diagnostics/             # Monitor de Salud
└── utils/                   # Herramientas base
```

## 🦾 EXTENSIONES (`/extensions`)
*El cuerpo y las herramientas (Sandbox).*
```text
extensions/
├── shields/                 # Escudos de protección externa
│   └── action_model_v1.py   # MAC-0 (Modelo de Acción)
├── sandboxes/               # Áreas de juego seguro
└── knowledge_intake/        # Ingesta de conocimiento
```

## 🧪 PRUEBAS (`/tests`)
*La garantía de estabilidad.*
```text
tests/
├── test_blender_observer_minimal.py  # [NUEVO] Test de observación pasiva
├── test_state_awareness_minimal.py   # Test de conciencia
├── test_full_pipeline.py             # Pruebas de integración
└── ...
```

## 📚 DOCUMENTACIÓN (`/docs`)
*La sabiduría acumulada.*
```text
docs/
├── philosophy/              # Principios (MODELO_DE_ACCION.md)
├── architecture/            # Planos
└── ...
```

## 📝 BITÁCORA (`/bitacora`)
*La historia viva.*
- Registros de sesión, decisiones aprendidas y evolución.
