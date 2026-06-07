# 📑 ÍNDICE DE DOCUMENTACIÓN ZULY
**Sistema de IA para Blender - Fase 18.5**

---

## 📖 MANUALES Y GUÍAS

### 🟢 DOCUMENTOS PRINCIPALES (ACTUALIZADO 31-MAR-2026)

| Documento | Ubicación | Uso |
|-----------|-----------|-----|
| **MANUAL_ZULY_SISTEMA_COMPLETO.md** | Root | Manual exhaustivo con todas las rutas y configuraciones |
| **REFERENCIA_RAPIDA_RUTAS.md** | Root | Cheat sheet con 5 rutas esenciales y comandos directos |
| **ARCHITECTURE_RULES.md** | Root | Reglas fundamentales de arquitectura (NO negociables) |
| **ARQUITECTURA_MEJORADA.md** | Root | Diseño completo del sistema ZULY v2 |

---

## 📍 RUTAS CRÍTICAS (COPIAR Y PEGAR)

### Blender
```
c:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe
```

### CLI Principal
```
c:\Users\Admin\Desktop\ZULY_IA_LOCAL\zuly_cli_v2.py
```

### Proyectos .BLEND
```
c:\Users\Admin\Desktop\ZULY_IA_LOCAL\ZULY_PROJECTS\
```

### Exportación (Renders + Modelos)
```
c:\Users\Admin\Desktop\ZULY_IA_LOCAL\export\
```

### Configuración
```
c:\Users\Admin\Desktop\ZULY_IA_LOCAL\config.json
```

### Logs
```
c:\Users\Admin\Desktop\ZULY_IA_LOCAL\logs\proceso.log
```

---

## 🚀 INICIO RÁPIDO

### 1. Abrir Terminal
```powershell
cd c:\Users\Admin\Desktop\ZULY_IA_LOCAL
```

### 2. Activar Virtual Environment
```powershell
.venv\Scripts\Activate.ps1
```

### 3. Ejecutar ZULY REAL
```powershell
python zuly_cli_v2.py --real
```

### 4. Dar una orden
```
zuly> crear un cubo
```

### 5. Verificar resultado
- ✅ .blend guardado en: `ZULY_PROJECTS/`
- ✅ Render guardado en: `export/`
- ✅ Log guardado en: `logs/proceso.log`

---

## 🎮 HANDLERS DISPONIBLES (48 TOTAL)

### Crear Primitivas
```
zuly> crear un cubo
zuly> crear una esfera
zuly> crear cilindro / plano / cono
```

### Transformar
```
zuly> mover objeto a 5, 3, 0
zuly> rotar objeto 90 grados
zuly> escalar objeto 2 veces
```

### Materiales
```
zuly> crear material dorado
zuly> aplicar material al cubo
zuly> establecer color rojo
```

### Render
```
zuly> renderizar escena
```

### Sistema
```
zuly> estado          # Estado completo
zuly> patrones        # Lista handlers
zuly> ayuda          # Ayuda
```

---

## 🔍 TROUBLESHOOTING RÁPIDO

| Problema | Solución |
|----------|----------|
| "bpy no disponible" | Blender en fallback (OK). Continúa en MOCK o lanza Blender por separado. |
| ".blend no se guarda" | Verifica permisos en `ZULY_PROJECTS/`. ¿Existe el directorio? |
| "Handler no encontrado" | Ejecuta `zuly> patrones` para ver lista de 48 handlers. |
| "Error en render" | Revisa `logs/proceso.log` para detalles específicos. |

---

## 📊 ESTRUCTURA DIRECTORIO RAÍZ

```
c:\Users\Admin\Desktop\ZULY_IA_LOCAL\

🟢 DOCUMENTOS ACTUALIZADOS:
├─ MANUAL_ZULY_SISTEMA_COMPLETO.md      ⭐ NUEVO
├─ REFERENCIA_RAPIDA_RUTAS.md           ⭐ NUEVO
├─ INDICE_DOCUMENTACION_ZULY.md         ⭐ NUEVO (este archivo)
├─ ARCHITECTURE_RULES.md
├─ ARQUITECTURA_MEJORADA.md
└─ [otros documentos de arquitectura]

🐍 EJECUTABLES:
├─ zuly_cli_v2.py                       ⭐ CLI PRINCIPAL
├─ zuly_cli.py
├─ lanzar_blender_zuly.py
└─ lyzu_core.py

🔧 DIRECTORIOS CLAVE:
├─ blender/v3/blender-3.6.0-zuly/       ⭐ BLENDER INSTALADO
├─ ZULY_PROJECTS/                       ⭐ ALMACÉN .BLEND
├─ export/                              ⭐ RENDERS Y MODELOS
├─ core/                                ⭐ SISTEMA DE IA (48 handlers)
├─ logs/                                ⭐ REGISTROS
├─ patterns/
├─ memory/
└─ .venv/                               ⭐ PYTHON VIRTUAL ENV
```

---

## 📋 CONFIGURACIÓN (config.json)

```json
{
  "entorno": {
    "directorio_salida": "./export/",
    "motor_render": "cycles",
    "muestras_render": 32
  },
  "logs": {
    "nivel": "INFO",
    "archivo": "./logs/proceso.log"
  }
}
```

---

## 🔄 CICLO AUTOMÁTICO COMPLETO

```
┌─ CLI Input ─────────────────────────────────┐
│ zuly> crear un cubo de 2 metros             │
└─────────────────────────────────────────────┘
           ↓
┌─ NLU Processing ────────────────────────────┐
│ • Extrae: comando=create_cube, size=2       │
│ • Confianza: 95%                            │
└─────────────────────────────────────────────┘
           ↓
┌─ Intent Router ─────────────────────────────┐
│ • Busca en 48 handlers disponibles          │
│ • Selecciona: blender.create_cube           │
└─────────────────────────────────────────────┘
           ↓
┌─ Handler Execution ─────────────────────────┐
│ • BlenderAdapter ejecuta en Blender real    │
│ • Si falla → MockAdapter fallback           │
└─────────────────────────────────────────────┘
           ↓
┌─ Automatic Save ────────────────────────────┐
│ ✅ .blend → ZULY_PROJECTS/                  │
│ ✅ .png   → export/                         │
│ ✅ .log   → logs/                           │
└─────────────────────────────────────────────┘
           ↓
┌─ User Feedback ─────────────────────────────┐
│ ✅ ÉXITO                                    │
│ └─ Cubo creado y guardado                   │
└─────────────────────────────────────────────┘
```

---

## 🧪 VALIDACIÓN DEL SISTEMA

### Verificar Blender
```powershell
Test-Path c:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe
# Resultado: True
```

### Verificar ZULY_PROJECTS
```powershell
Test-Path c:\Users\Admin\Desktop\ZULY_IA_LOCAL\ZULY_PROJECTS
# Resultado: True
```

### Ver Archivos .BLEND
```powershell
Get-ChildItem c:\Users\Admin\Desktop\ZULY_IA_LOCAL\ZULY_PROJECTS -Filter *.blend
```

### Ver Renders
```powershell
Get-ChildItem c:\Users\Admin\Desktop\ZULY_IA_LOCAL\export -Filter *.png
```

---

## 💡 TIPS Y TRICKS

1. **Autocomplete:** Escribe `zuly> cre` y presiona TAB para autocompletar
2. **Historial:** Las órdenes anteriores se guardan en trace.txt
3. **Diagróstico:** `python diagnostico_zuly.py` ejecuta verificación completa
4. **Múltiples comandos:** Usa `;` para separar comandos en CLI
5. **Batch execution:** `python zuly_cli_v2.py --real -c "crear un cubo; mover objeto"`

---

## 📞 SOPORTE Y DEBUG

### Archivo de log principal
```
c:\Users\Admin\Desktop\ZULY_IA_LOCAL\logs\proceso.log
```

### Ejecutar diagnóstico completo
```bash
python c:\Users\Admin\Desktop\ZULY_IA_LOCAL\diagnostico_zuly.py
```

### Validar sistema
```bash
python c:\Users\Admin\Desktop\ZULY_IA_LOCAL\validate_zuly_system.py
```

---

## 📅 HISTORIAL DE ACTUALIZACIONES

| Fecha | Versión | Cambios |
|-------|---------|---------|
| 31-MAR-2026 | 2.0 | ✅ Manual completo con rutas específicas |
| 31-MAR-2026 | 2.0 | ✅ Referencia rápida creada |
| 31-MAR-2026 | 2.0 | ✅ Ciclo de guardado documentado |
| 31-MAR-2026 | 2.0 | ✅ 48 handlers categorizados |

---

## ✅ ESTADO DEL SISTEMA

```
🟢 BLENDER:        Instalado v3.6.0 (listo)
🟢 ZULY CLI:       Operacional v2.0 (listo)
🟢 HANDLERS:       48/48 registrados (listo)
🟢 PROYECTOS:      ZULY_PROJECTS/ (listo)
🟢 EXPORTACIÓN:    export/ (listo)
🟢 CONFIGURACIÓN:  config.json (listo)
🟢 LOGS:           Sistema activo (listo)
```

---

**📌 Documentación actualizada: 31 de Marzo de 2026**

*Para acceso rápido, consulta:*
- ⭐ [REFERENCIA_RAPIDA_RUTAS.md](REFERENCIA_RAPIDA_RUTAS.md) - Cheat sheet
- 📖 [MANUAL_ZULY_SISTEMA_COMPLETO.md](MANUAL_ZULY_SISTEMA_COMPLETO.md) - Manual detallado
