# 🧪 ZULY_LAB - Laboratorio de Entrenamiento

**Sistema de entrenamiento práctico para ZULY**

---

## 🎯 Filosofía del Laboratorio

ZULY aprende **HACIENDO**, no leyendo documentación.

Este laboratorio implementa:
- ✅ Entrenamiento estructurado por fases
- ✅ Ejercicios repetibles
- ✅ Dataset automático
- ✅ Validación continua

---

## 📁 Estructura

```
ZULY_LAB/
├── A_estructura/          # FASE A: Fundación Estructural
│   └── ejercicios/        # Primitivas y construcción básica
│
├── B_automatizacion/      # FASE B: Workflows completos
│   └── ejercicios/        # Rutinas automatizadas
│
├── C_render_tecnico/      # FASE C: Presentación profesional
│   └── ejercicios/        # Render e iluminación
│
├── D_integracion_real/    # FASE D: Trabajo con humano
│
├── dataset_patrones/      # Patrones aprendidos
├── logs_sesiones/         # Logs automáticos JSON
├── resultados_zuly/       # Archivos .blend generados
└── entrenamiento_youtube/ # Transcripciones (futuro)
```

---

## 🚀 Uso Rápido

### Ejecutar un ejercicio

```bash
python zuly_lab.py run A1.1
```

### Ejecutar todos los ejercicios de una fase

```bash
python zuly_lab.py run-all A
```

### Ver estadísticas

```bash
python zuly_lab.py stats
```

### Validar ejercicio

```bash
python zuly_lab.py validate A1.1
```

---

## 📚 Fases de Entrenamiento

### FASE A: Fundación Estructural (4-6 semanas)
**Objetivo**: ZULY aprende lógica de construcción repetible

**Ejercicios**:
- A1.1: Cubo básico (crear, transformar, material, guardar)
- A1.2: 5 columnas alineadas
- A1.3: Base estructural con duplicados
- A1.4: Organización de escena
- A1.5: Variaciones controladas

**Criterio de aprobación**: Ejecuta rutinas sin errores, logs completos

---

### FASE B: Automatización (4 semanas)
**Objetivo**: ZULY ejecuta workflows completos

**Próximamente**

---

### FASE C: Render Técnico (3-5 semanas)
**Objetivo**: ZULY prepara presentaciones profesionales

**Próximamente**

---

### FASE D: Integración Real (Continua)
**Objetivo**: ZULY trabaja contigo en proyectos reales

**Próximamente**

---

## 📊 Sistema de Logging

Cada ejercicio genera automáticamente:

```json
{
  "ejercicio": "A1.1",
  "timestamp": "2026-02-14T18:30:00",
  "pasos_ejecutados": 6,
  "tiempo_total_segundos": 2.3,
  "exito": true,
  "objetos_creados": ["Cube"],
  "validacion_v0": "OK",
  "errores": []
}
```

---

## ✅ Checklist Primera Sesión

**Para considerar Lab A1 operativo:**

- [ ] Estructura creada
- [ ] 5 ejercicios definidos
- [ ] CLI funcional
- [ ] Rutina A1.1 ejecutada exitosamente
- [ ] Log generado
- [ ] Archivo .blend guardado

---

## 🎯 Primer Ejercicio: A1.1

**Nombre**: "Cubo Básico"  
**Objetivo**: Primer contacto real de ZULY con Blender

**Pasos**:
1. Crear escena nueva
2. Crear cubo
3. Escalar cubo (2x)
4. Mover cubo a [2, 0, 0]
5. Aplicar material básico
6. Guardar escena
7. Registrar log

**Validación**:
- ✅ Cubo existe
- ✅ Transformación correcta
- ✅ Material aplicado
- ✅ Escena guardada en `resultados_zuly/`
- ✅ Log en `logs_sesiones/`

---

## 🔥 Reglas de Oro

1. **No saltar fases** - Cada fase construye sobre la anterior
2. **Cada ejecución = log** - Sin dataset no hay aprendizaje
3. **Validar antes de avanzar** - Estabilidad > velocidad
4. **Repetir hasta dominar** - 10 ejecuciones exitosas = aprobado

---

## 📈 Métricas de Progreso

ZULY está aprendiendo si:
- ✅ Tasa de éxito aumenta (>95%)
- ✅ Tiempo de ejecución disminuye
- ✅ Logs completos y estructurados
- ✅ Dataset crece consistentemente

---

**Creado**: 2026-02-14  
**Fase Actual**: A (Fundación Estructural)  
**Ejercicio Actual**: A1.1 (Cubo Básico)
