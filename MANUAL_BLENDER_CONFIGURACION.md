# 🔧 MANUAL: Configuración de Blender para ZULY

**Última actualización:** 2 de abril de 2026  
**Estado:** ✅ Configurado y Conectado

---

## 📋 ÍNDICE RÁPIDO

1. [Ruta de Blender](#ruta-de-blender-registrada)
2. [Configuración Automática](#configuración-automática)
3. [Cómo Funciona](#cómo-funciona)
4. [Usar ZULY con Blender Real](#usar-zuly-con-blender-real)
5. [Solución de Problemas](#solución-de-problemas)

---

## 🎯 Ruta de Blender Registrada

```
Ubicación: C:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe
Versión: Blender 3.6.0
Estado: ✅ DETECTADO Y DISPONIBLE
Tipo: Instalación Local ZULY
```

### Archivos de Configuración

| Archivo | Propósito | Ubicación |
|---------|-----------|-----------|
| `.env.blender` | Configuración en variables de entorno | Raíz del proyecto |
| `core/config/blender_config.py` | Módulo de carga de configuración | `core/config/` |
| `core/adapters/blender_adapter.py` | Adapter para conectar con Blender | `core/adapters/` |

---

## ⚙️ Configuración Automática

Cada vez que inicies ZULY, el sistema:

1. **Carga el archivo `.env.blender`** con la ruta pre-configurada
2. **Detecta automáticamente** la ruta de Blender desde:
   - Variables de entorno (`.env.blender`)
   - Sistema PATH
   - Ruta local predeterminada
3. **Conecta el BlenderAdapter** con la ruta encontrada
4. **Registra el estado** en los logs

### Variables de Configuración (`.env.blender`)

```env
# Ruta al ejecutable de Blender
BLENDER_PATH=C:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe

# Versión de Blender
BLENDER_VERSION=3.6.0

# Modo de conexión
BLENDER_CONNECTION_MODE=python_subprocess

# Modo de operación (background = sin GUI)
BLENDER_OPERATION_MODE=background

# Timeout para operaciones
BLENDER_TIMEOUT=300

# Directorio de salida
BLENDER_OUTPUT_DIR=./export/
```

---

## 🔄 Cómo Funciona

### Diagrama de Inicialización

```
Inicio de ZULY
    ↓
Carga .env.blender
    ↓
BlenderConfig.get_blender_path()
    ├→ Intenta desde variables de entorno
    ├→ Busca en PATH del sistema
    └→ Fallback a ruta local predeterminada
    ↓
BlenderAdapter inicializado
    ├→ Intenta cargar bpy desde ruta configurada
    ├→ Auto-detección en caliente
    └→ Fallback a MockAdapter si falla
    ↓
✅ Sistema listo para modelar
```

### Flujo de Detección de Blender

El sistema usa este orden de prioridad:

1. **Configuración desde `.env.blender`** (máxima prioridad)
2. **Detección desde PATH** del sistema
3. **Ruta predeterminada local** (fallback automático)
4. **MockAdapter** si nada funciona (simulación)

---

## 🚀 Usar ZULY con Blender Real

### Opción 1: Línea de Comandos (Una ejecución)

```bash
# Crear un cubo
python zuly_cli_v2.py --real --command "crear un cubo"

# Crear escena completa (descompone automáticamente)
python zuly_cli_v2.py --real --command "crea una escena con iluminación profesional"

# Ver estado del sistema
python zuly_cli_v2.py --real --command "estado"
```

### Opción 2: Modo Interactivo (Sesión completa)

```bash
# Inicia CLI interactivo con Blender real
python zuly_cli_v2.py --real

# Luego escribes comandos:
zuly> crear un cubo
zuly> mover objeto
zuly> renderizar
zuly> salir
```

### Opción 3: Desde Python

```python
from core.agent import Agent

# Crear agente con Blender real (NO force_mock)
agent = Agent(force_mock=False)

# Procesar petición
result = agent.process_natural_request("crear un cubo azul")

# Ver resultado
print(result)
```

---

## ✅ Verificación de Configuración

Ejecuta el script de prueba para verificar que todo está conectado:

```bash
python test_blender_config.py
```

Debería mostrar:

```
✅ EXCELENTE: Blender encontrado en la ruta configurada
Ruta de Blender: C:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe
Archivo existe: True
```

---

## 🆘 Solución de Problemas

### Problema 1: "BlenderAdapter: bpy no disponible"

**Causa:** Blender no se detectó correctamente  
**Solución:**
1. Verifica que `.env.blender` exista en la raíz del proyecto
2. Ejecuta: `python test_blender_config.py`
3. Verifica la ruta en `.env.blender`

### Problema 2: "Usando MockAdapter (fallback)"

**Causa:** ZULY no logró conectar con Blender  
**Solución:**
1. Verifica que la ruta en `.env.blender` existe: 
   ```bash
   Test-Path "C:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe"
   ```
2. Si devuelve `False`, actualiza `.env.blender`
3. Reinicia ZULY

### Problema 3: "Script ejecutado pero no ve cambios en Blender"

**Causa:** Blender se ejecuta en background  
**Solución:**
1. Abre Blender manualmente
2. O usa modo interactivo con `--real` flag

---

## 📝 Notas Importantes

- **Persistencia:** La configuración se guarda en `.env.blender` y persiste automáticamente
- **Seguridad:** NO modificar manualmente `.env.blender` a menos que cambies la ruta de Blender
- **Actualización:** Si actualizas Blender, edita `.env.blender` con la nueva ruta
- **Testing:** Usa `--real` flag para conectar con Blender real

---

## 📞 Referencias

- [Ruta de archivo de configuración](.env.blender)
- [Módulo de configuración](core/config/blender_config.py)
- [Script de prueba](test_blender_config.py)
- [Manual del Sistema Completo](MANUAL_ZULY_SISTEMA_COMPLETO.md)

---

**Estado del Sistema:** ✅ OPERACIONAL  
**Última verificación:** 2 de abril de 2026, 15:12  
**Próxima acción:** Comenzar a modelar con `python zuly_cli_v2.py --real`
