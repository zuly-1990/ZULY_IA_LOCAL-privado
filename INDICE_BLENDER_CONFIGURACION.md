# 📚 INDICE DE DOCUMENTACIÓN - BLENDER CONFIGURADO EN ZULY

**Fecha de configuración:** 2 de abril de 2026  
**Status:** ✅ OPERACIONAL  
**Última revisión:** 2026-04-02 15:12

---

## 🎯 GUÍAS RÁPIDAS

### Si es tu PRIMER USO de ZULY con Blender:

1. **Lee primero:** [MANUAL_BLENDER_CONFIGURACION.md](MANUAL_BLENDER_CONFIGURACION.md) (5 min)
   - Explica dónde está Blender
   - Cómo funciona la detección automática
   - Cómo ejecutar ZULY

2. **Luego prueba:** 
   ```bash
   python test_blender_config.py
   python zuly_cli_v2.py --real --command "crear un cubo"
   ```

3. **Después lee:** [INICIO_RAPIDO.md](INICIO_RAPIDO.md) (10 min)
   - Ejemplos prácticos
   - Cómo usar API de Agent

---

## 📖 DOCUMENTACIÓN COMPLETA

### Configuración de Blender

| Documento | Propósito | Para quién | Tiempo |
|-----------|---------|-----------|--------|
| **[MANUAL_BLENDER_CONFIGURACION.md](MANUAL_BLENDER_CONFIGURACION.md)** | Guía completa de Blender conectado | Todos | 15 min |
| **[BLENDER_CONFIG_REGISTRY.ini](BLENDER_CONFIG_REGISTRY.ini)** | Registro de persistencia | Técnico | - |
| **[.env.blender](.env.blender)** | Configuración de variables de entorno | Técnico | - |

### Sistema ZULY

| Documento | Propósito | Para quién | Tiempo |
|-----------|---------|-----------|--------|
| **[INICIO_RAPIDO.md](INICIO_RAPIDO.md)** | Cómo empezar en 5 min | Todos | 5 min |
| **[GUIA_USO_AGENTE_IA.md](GUIA_USO_AGENTE_IA.md)** | Ejemplos de uso | Desarrolladores | 30 min |
| **[ARQUITECTURA_MEJORADA.md](ARQUITECTURA_MEJORADA.md)** | Cómo funciona internamente | Arquitectos | 60 min |
| **[MANUAL_ZULY_SISTEMA_COMPLETO.md](MANUAL_ZULY_SISTEMA_COMPLETO.md)** | Manual exhaustivo | Todos | 120 min |

---

## 🔧 ARCHIVOS TÉCNICOS

### Sistema de Configuración

```
core/config/
├── blender_config.py          ← Carga ruta de Blender
├── __init__.py                ← Package init
└── healthy_state.json         ← Estado actual
```

### Sistema de Persistencia

```
Raíz del proyecto/
├── .env.blender               ← Variables de entorno
├── BLENDER_CONFIG_REGISTRY.ini ← Registro de sesiones
└── ZULY_SESSION_REGISTRY.json ← Historial de inicios (auto-generado)
```

### Adapter de Blender

```
core/adapters/
├── blender_adapter.py         ← Conecta con Blender
├── engine_adapter.py          ← Interfaz abstracta
├── mock_adapter.py            ← Fallback simulación
└── __init__.py                ← Factory singleton
```

### Registry de Sesiones

```
core/observability/
└── session_registry.py        ← Registra cada inicio (auto-generado)
```

---

## ✅ CHECKLIST DE CONFIGURACIÓN

- [x] Blender 3.6.0 detectado
- [x] Ruta local configurada
- [x] `.env.blender` creado
- [x] `core/config/blender_config.py` creado
- [x] `core/adapters/blender_adapter.py` actualizado
- [x] `test_blender_config.py` créado y validado
- [x] `ZULY_SESSION_REGISTRY.json` auto-creado en primer inicio
- [x] Persistencia de sesiones implementada
- [x] Manual completo creado

---

## 🚀 COMANDOS RÁPIDOS

```bash
# Verificar que Blender está detectado
python test_blender_config.py

# Usar ZULY con Blender real (una orden)
python zuly_cli_v2.py --real --command "crear un cubo"

# Modo interactivo con Blender real
python zuly_cli_v2.py --real

# Ver historial de sesiones
Python -c "from core.observability.session_registry import SessionRegistry; SessionRegistry.print_session_summary()"
```

---

## 📊 INFORMACIÓN DEL SISTEMA

### Blender Instalado

```
Ubicación:   C:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe
Versión:     3.6.0
Tipo:        Instalación local ZULY
Estado:      ✅ DETECTADO
Conexión:    python_subprocess
Operación:   background (sin GUI)
```

### Persistencia

**La configuración de Blender NO se pierde entre sesiones porque:**

1. Ruta se guarda en `.env.blender` (no se borra)
2. Cada inicio registra sesión en `ZULY_SESSION_REGISTRY.json`
3. Module `SessionRegistry` mantiene historial completo
4. Agent carga configuración automáticamente al iniciar

---

## 🔍 DEBUGGING

### Si Blender no se detecta:

```bash
# 1. Verificar configuración
python test_blender_config.py

# 2. Ver logs detallados
python -c "
from core.config.blender_config import BlenderConfig
print(f'Path: {BlenderConfig.get_blender_path()}')
print(f'Versión: {BlenderConfig.get_blender_version()}')
"

# 3. Verificar archivo .env.blender
cat .env.blender
```

### Si sesiones no se registran:

```bash
# 1. Ver si archivo existe
ls -la ZULY_SESSION_REGISTRY.json

# 2. Ver contenido
python -c "
from core.observability.session_registry import SessionRegistry
print(f'Total sesiones: {SessionRegistry.get_session_count()}')
SessionRegistry.print_session_summary()
"
```

---

## 📞 REFERENCIAS RÁPIDAS

- **¿Dónde está Blender?** → [MANUAL_BLENDER_CONFIGURACION.md](MANUAL_BLENDER_CONFIGURACION.md#ruta-de-blender-registrada)
- **¿Cómo uso ZULY?** → [INICIO_RAPIDO.md](INICIO_RAPIDO.md#-en-5-minutos)
- **¿Cómo funciona por dentro?** → [ARQUITECTURA_MEJORADA.md](ARQUITECTURA_MEJORADA.md)
- **¿Dónde se guarda la configuración?** → Ver sección [Archivos Técnicos](#archivos-técnicos)
- **¿Cómo verifico que funciona?** → Ejecuta: `python test_blender_config.py`

---

## 📝 NOTAS

- **Persistencia:** Automática via `.env.blender` y `SessionRegistry`
- **Seguridad:** Configuración solo lectura una vez cargada
- **Rendimiento:** Detección en caché (singleton pattern)
- **Compatibilidad:** Funciona en Windows, fácil adaptar a Mac/Linux

---

**Estado:** 🟢 OPERACIONAL  
**Próximo paso:** Comienza a usar ZULY → `python zuly_cli_v2.py --real`
