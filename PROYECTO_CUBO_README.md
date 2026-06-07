# 🎲 PROYECTO: EXPLORACIÓN COMPLETA DEL CUBO

**Fecha:** 14 de Diciembre de 2025  
**Objetivo:** Explorar TODAS las variaciones posibles del cubo primitivo en Blender

---

## 📋 Resumen del Proyecto

Este proyecto crea **25+ variaciones del cubo** explorando:
- ✅ Diferentes escalas (0.5x a 2.5x)
- ✅ Rotaciones simples (0° a 180°)
- ✅ Rotaciones complejas (combinaciones de ejes)
- ✅ Escalas no uniformes (barras, placas, discos)
- ✅ 10 materiales diferentes (metales, plásticos, emisivos)
- ✅ Iluminación profesional (3-point lighting)
- ✅ Renders de alta calidad (1920x1080, 128 samples)

---

## 🚀 Cómo Ejecutar

### Método 1: En Blender GUI (Recomendado)

1. **Abrir Blender 3.6**

2. **Ir a Scripting** (pestaña superior)

3. **Abrir el script:**
   - Click en **📁 Open** (o **Ctrl+O**)
   - Navegar a: `C:\Users\Admin\Desktop\ZULY_IA_LOCAL\`
   - Seleccionar: `proyecto_cubo_completo.py`

4. **Ejecutar:**
   - Presionar **Alt + P**
   - O click en **▶ Run Script**

5. **Esperar:** El proceso toma 2-5 minutos dependiendo de tu hardware

---

### Método 2: Línea de Comandos

```powershell
cd C:\Users\Admin\Desktop\ZULY_IA_LOCAL

# Ejecutar en Blender
.\blender\v3\blender-3.6.0-zuly\blender.exe --background --python proyecto_cubo_completo.py
```

---

## 📊 Variaciones Creadas

### 1. Variaciones de Escala (5 cubos)
```
Cubo_Escala_0.5  → Escala: 0.5x  | Material: Oro
Cubo_Escala_1.0  → Escala: 1.0x  | Material: Oro
Cubo_Escala_1.5  → Escala: 1.5x  | Material: Oro
Cubo_Escala_2.0  → Escala: 2.0x  | Material: Oro
Cubo_Escala_2.5  → Escala: 2.5x  | Material: Oro
```

### 2. Variaciones de Rotación (5 cubos)
```
Cubo_Rotacion_0   → Rotación: 0°   | Material: Plata
Cubo_Rotacion_45  → Rotación: 45°  | Material: Plata
Cubo_Rotacion_90  → Rotación: 90°  | Material: Plata
Cubo_Rotacion_135 → Rotación: 135° | Material: Plata
Cubo_Rotacion_180 → Rotación: 180° | Material: Plata
```

### 3. Variaciones de Material (5 cubos)
```
Cubo_Material_oro            → Material: Oro (metálico)
Cubo_Material_plata          → Material: Plata (metálico)
Cubo_Material_cobre          → Material: Cobre (metálico)
Cubo_Material_plastico_rojo  → Material: Plástico Rojo
Cubo_Material_plastico_azul  → Material: Plástico Azul
```

### 4. Escalas No Uniformes (5 cubos)
```
Cubo_NoUniforme_1 → Barra horizontal (2.0, 0.5, 0.5)
Cubo_NoUniforme_2 → Barra vertical   (0.5, 2.0, 0.5)
Cubo_NoUniforme_3 → Barra profunda   (0.5, 0.5, 2.0)
Cubo_NoUniforme_4 → Placa            (2.0, 1.0, 0.5)
Cubo_NoUniforme_5 → Disco            (1.5, 1.5, 0.3)
```

### 5. Rotaciones Complejas (5 cubos)
```
Cubo_RotCompleja_1 → Rotación: (45°, 0°, 0°)
Cubo_RotCompleja_2 → Rotación: (0°, 45°, 0°)
Cubo_RotCompleja_3 → Rotación: (0°, 0°, 45°)
Cubo_RotCompleja_4 → Rotación: (45°, 45°, 0°)
Cubo_RotCompleja_5 → Rotación: (45°, 45°, 45°)
```

**Total:** 25 variaciones de cubo

---

## 🎨 Materiales Disponibles

| Material | Tipo | Color | Metallic | Roughness |
|----------|------|-------|----------|-----------|
| Oro | Metal | Dorado | 1.0 | 0.2 |
| Plata | Metal | Plateado | 1.0 | 0.1 |
| Cobre | Metal | Cobrizo | 1.0 | 0.3 |
| Vidrio | Transparente | Azul claro | 0.0 | 0.0 |
| Plástico Rojo | Plástico | Rojo | 0.0 | 0.3 |
| Plástico Azul | Plástico | Azul | 0.0 | 0.3 |
| Plástico Verde | Plástico | Verde | 0.0 | 0.3 |
| Mate Negro | Mate | Negro | 0.0 | 0.9 |
| Mate Blanco | Mate | Blanco | 0.0 | 0.8 |
| Emisión Azul | Emisivo | Azul brillante | 0.0 | 0.5 |

---

## 💡 Iluminación Profesional

El proyecto usa **3-Point Lighting** (técnica cinematográfica):

### Key Light (Luz Principal)
- **Tipo:** Area Light
- **Posición:** (5, -5, 8)
- **Energía:** 500W
- **Función:** Iluminación principal del objeto

### Fill Light (Luz de Relleno)
- **Tipo:** Area Light
- **Posición:** (-5, -3, 5)
- **Energía:** 200W
- **Función:** Suavizar sombras

### Back Light (Luz Trasera)
- **Tipo:** Spot Light
- **Posición:** (0, 5, 6)
- **Energía:** 300W
- **Función:** Separar objeto del fondo (rim light)

---

## 📸 Configuración de Render

```
Motor:       Cycles
Resolución:  1920 x 1080 (Full HD)
Samples:     128
Formato:     PNG
Fondo:       Gris oscuro (0.05, 0.05, 0.05)
Cámara:      50mm lens, posición (8, -8, 6)
```

---

## 📁 Archivos Generados

Después de ejecutar el script, encontrarás:

```
C:\Users\Admin\Desktop\ZULY_IA_LOCAL\export\cubos\
├── Cubo_Exploracion_Completa.blend          # Archivo Blender
└── Cubo_Exploracion_Completa_Vista_General.png  # Render
```

---

## 🎯 Personalización

### Activar Renders Individuales

Por defecto, el script solo genera 1 render de vista general. Para renderizar cada cubo individualmente:

1. Abrir `proyecto_cubo_completo.py`
2. Buscar la línea:
   ```python
   RENDER_INDIVIDUAL = False
   ```
3. Cambiar a:
   ```python
   RENDER_INDIVIDUAL = True
   ```
4. Ejecutar de nuevo

Esto generará **25 renders adicionales** (uno por cada cubo).

---

### Modificar Resolución

Para cambiar la resolución del render:

```python
# Buscar esta línea:
RENDER_RESOLUTION = (1920, 1080)

# Cambiar a:
RENDER_RESOLUTION = (3840, 2160)  # 4K
# o
RENDER_RESOLUTION = (1280, 720)   # HD
```

---

### Modificar Samples (Calidad)

Para cambiar la calidad del render:

```python
# Buscar:
RENDER_SAMPLES = 128

# Cambiar a:
RENDER_SAMPLES = 256  # Mayor calidad (más lento)
# o
RENDER_SAMPLES = 64   # Menor calidad (más rápido)
```

---

## 🔧 Agregar Nuevas Variaciones

Para agregar tus propias variaciones, edita la sección de variaciones:

```python
# Agregar después de las variaciones existentes:
variaciones.append({
    'nombre': 'Mi_Cubo_Personalizado',
    'location': (0, 15, 0),  # Posición X, Y, Z
    'scale': (2.0, 2.0, 2.0),  # Escala X, Y, Z
    'rotation': (math.radians(30), math.radians(45), 0),  # Rotación en radianes
    'material': 'emision_azul'  # Material a aplicar
})
```

---

## 📊 Estadísticas del Proyecto

```
✅ Cubos creados:        25
✅ Materiales únicos:    10
✅ Luces configuradas:   3 (3-point lighting)
✅ Renders generados:    1 (vista general)
✅ Tiempo estimado:      2-5 minutos
✅ Tamaño archivo .blend: ~5 MB
✅ Tamaño render PNG:    ~2-3 MB
```

---

## 🎨 Próximas Mejoras Sugeridas

### Corto Plazo
- [ ] Agregar animación de rotación
- [ ] Crear composición de galería automática
- [ ] Exportar a formatos 3D (GLB, FBX)

### Mediano Plazo
- [ ] Agregar texturas procedurales
- [ ] Implementar diferentes esquemas de iluminación
- [ ] Crear variaciones con modificadores (bevel, subdivision)

### Largo Plazo
- [ ] Generar video 360° de cada cubo
- [ ] Crear comparación lado a lado
- [ ] Implementar sistema de votación de renders

---

## 🐛 Troubleshooting

### Error: "ModuleNotFoundError: No module named 'lyzu_core'"

**Solución:** Verifica que la ruta en la línea 18 sea correcta:
```python
sys.path.insert(0, "C:/Users/Admin/Desktop/ZULY_IA_LOCAL")
```

---

### Render toma mucho tiempo

**Solución:** Reduce los samples:
```python
RENDER_SAMPLES = 64  # En lugar de 128
```

---

### No se ven los cubos en el viewport

**Solución:** 
1. Presiona **Numpad 0** para ver desde la cámara
2. Presiona **Z** → **Rendered** para ver con materiales

---

## 📚 Recursos Adicionales

- **Guía de Integración:** `GUIA_INTEGRACION_BLENDER_COMPLETA.md`
- **Inicio Rápido:** `INICIO_BLENDER.md`
- **Dashboard del Proyecto:** `DASHBOARD_FINAL.md`

---

## ✅ Checklist de Ejecución

```
Antes de ejecutar:
[✅] Blender 3.6 instalado
[✅] ZULY_IA_LOCAL descargado
[✅] Script proyecto_cubo_completo.py creado

Durante la ejecución:
[ ] Abrir Blender
[ ] Cargar script
[ ] Ejecutar con Alt+P
[ ] Esperar 2-5 minutos

Después de ejecutar:
[ ] Verificar archivo .blend creado
[ ] Verificar render PNG generado
[ ] Explorar escena en Blender
[ ] (Opcional) Activar renders individuales
```

---

**Proyecto creado:** 14 de Diciembre de 2025  
**Versión:** 1.0  
**Estado:** ✅ Listo para Ejecutar

**¡Explora todas las posibilidades del cubo! 🎲🚀**
