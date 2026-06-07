# ⚡ REFERENCIA RÁPIDA ZULY - RUTAS ESENCIALES
**Última actualización:** 12 de Abril 2026 (Post-Consolidación Fases 1-4)

---

## 🎯 5 RUTAS MÁS IMPORTANTES

### 1️⃣ EJECUTABLE BLENDER
```
c:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe
```

### 2️⃣ CLI PRINCIPAL ZULY
```
c:\Users\Admin\Desktop\ZULY_IA_LOCAL\zuly_cli.py

EJECUCIÓN:
  python zuly_cli.py --real
```

### 3️⃣ ALMACÉN .BLEND PROYECTOS
```
c:\Users\Admin\Desktop\ZULY_IA_LOCAL\ZULY_PROJECTS\

ARCHIVOS PRINCIPALES:
  • ZULY_MAESTRO.blend (modelo maestro del sistema)
  • cubo_azul_render.png (render de referencia)
```

### 4️⃣ EXPORTACIÓN (RENDERS + MODELOS)
```
c:\Users\Admin\Desktop\ZULY_IA_LOCAL\export\

CONTIENE:
  *.png     - Renders
  *.obj     - Modelos OBJ
  *.fbx     - Modelos FBX
  *.gltf    - Modelos GLTF
```

### 5️⃣ CONFIGURACIÓN GLOBAL
```
c:\Users\Admin\Desktop\ZULY_IA_LOCAL\config.json

PARÁMETROS:
  - directorio_salida: "./export/"
  - motor_render: "cycles"
  - muestras_render: 32
```

---

## 🔥 COMANDOS RÁPIDOS

### Inicio ZULY REAL
```bash
cd c:\Users\Admin\Desktop\ZULY_IA_LOCAL
python zuly_cli.py --real
```

### Un comando directo
```bash
python zuly_cli.py --real -c "crear un cubo"
```

### Test de sistema
```bash
python test_fase3_refactor.py
```

### Ver estado
```bash
zuly> estado
```

### Listar handlers
```bash
zuly> patrones
```

### Salir
```bash
zuly> salir
```

---

## 📂 DIRECTORIOS CLAVE (ACTUALIZADO FASE 3-4)

```
core/                       ← Sistema de IA refactorizado
├── session/                ← ExecutionContext, SessionManager (NUEVO FASE 3)
├── execution/              ← ExecutionEngine (NUEVO FASE 3)
├── commands/blender_handlers/  ← 12 handlers (primitivas + arquitectura)
├── intents/                ← NLU con dimensiones arquitectónicas (FASE 2)
├── adapters/               ← BlenderAdapter
└── deprecated/             ← Archivos JUES viejos (FASE 1)

memory/                     ← Patrones assembly (FUNCIONAL)
├── assembly_patterns.json  ← 10 patrones JUES-validados
└── traces.json             ← Trazas del sistema

export/                     ← .png renders + .obj/.fbx (SALIDA)
bitacora/                   ← Logs, decisiones aprendidas, reportes JUES
blender/v3/                 ← Blender 3.6 instalado
archive/                    ← Backups y archivos históricos (FASE 1)
```

---

## ✅ CICLO AUTOMÁTICO (FASE 2-4)

```
1. Usuario: "crear habitación 4x5"
   ↓
2. NLU extrae dimensiones (ancho=4, prof=5, alt=2.5)
   ↓
3. ExecutionEngine enruta a crear_habitacion_handler
   ↓
4. BlenderAdapter ejecuta en Blender real
   ↓
5. JUES valida automáticamente (100pts = APTO_PARA_SELLO)
   ↓
6. ✅ Estructura creada en Blender
   ✅ Reporte JUES en bitacora/jues_reports/
   ✅ Traza en memory/traces.json
```

## 🗑️ SISTEMAS ELIMINADOS (FASE 4)
- ❌ C2 Memory (pattern_memory.py) - 0 patrones aprendidos, sistema roto
- ❌ LearningFreedomEngine - No conectado
- ❌ Repositorios de patrones (staging/verified/quarantine) - Vacíos

**Reemplazado por:** `assembly_patterns.json` (10 patrones hardcoded, funcionales)

---

## 🎮 HANDLERS ACTUALES (12 Total - FASE 3-4)

### Primitivas (5)
- `blender.create_cube` - Crear cubo
- `blender.create_sphere` - Crear esfera  
- `blender.create_cylinder` - Crear cilindro
- `blender.create_plane` - Crear plano
- `blender.create_cone` - Crear cono

### Arquitectura (6) - NUEVO FASE 2
- `blender.crear_columna` - Columna desde assembly pattern
- `blender.crear_muro` - Muro con medidas arquitectónicas
- `blender.crear_piso` - Piso/suelo
- `blender.crear_techo` - Techo elevado
- `blender.crear_habitacion` - Habitación completa (4 paredes + piso + techo)
- `blender.listar_patrones` - Listar patrones assembly

### Render/Sistema (1)
- `blender.renderizar` - Renderizar escena

### Comandos NLU con Dimensiones (NUEVO FASE 2)
```
"crea habitación 4x5"           → ancho=4m, prof=5m, alt=2.5m
"habitación 3x4x2.8"            → ancho=3m, prof=4m, alt=2.8m
"cuarto 6 por 8 metros"         → ancho=6m, prof=8m, alt=2.5m
"ancho 5m profundidad 6m alto 3m" → medidas explícitas
```

---

## 🆘 SI ALGO FALLA

1. **Revisar bitácora:**
   ```
   c:\Users\Admin\Desktop\ZULY_IA_LOCAL\bitacora\jues_reports\
   c:\Users\Admin\Desktop\ZULY_IA_LOCAL\bitacora\DECISIONES_APRENDIDAS.md
   ```

2. **Verificar ruta Blender:**
   ```powershell
   Test-Path c:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe
   ```

3. **Validar sistema:**
   ```bash
   python test_fase3_refactor.py
   ```

4. **Ejecutar diagnóstico:**
   ```
   python diagnostico_zuly.py
   ```

## 📊 ARCHIVOS DE REFERENCIA

- `PROGRESO_CONSOLIDACION.md` - Estado Fases 1-6
- `bitacora/FASE4_ELIMINACION_C2_MEMORY.md` - Detalles FASE 4
- `bitacora/SESION_2026-04-12_REFACTOR_FASE3_COMPLETADA.md` - FASE 3
- `memory/assembly_patterns.json` - Patrones disponibles

---

**🟢 SISTEMA LISTO - 12 de Abril 2026**
**✅ CONSOLIDACIÓN ZULY 100% COMPLETADA**
- FASE 1: Limpieza raíz (40% archivos eliminados)
- FASE 2: NLU Arquitectónico (dimensiones 4x5m, 2.5m alto)
- FASE 3: Refactor agent.py (God Object → Facade, 74% reducción)
- FASE 4: Eliminación C2 Memory (~2000 líneas código muerto)
