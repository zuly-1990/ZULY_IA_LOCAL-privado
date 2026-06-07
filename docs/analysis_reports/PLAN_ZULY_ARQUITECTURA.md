# PLAN ZULY: Arquitectura Desde Cero
## Caso de Uso Real - Modelado Arquitectónico Procedural

**Fecha:** 11 Abril 2026  
**Objetivo:** ZULY aprende a crear elementos arquitectónicos básicos desde comandos naturales  
**Métrica de éxito:** 3 usuarios pueden crear una habitación completa solo con voz/texto

---

## 🎯 CASOS DE USO ARQUITECTÓNICOS (Prioridad 1)

### FASE A: Elementos Básicos (Semana 1)
- [ ] "crea una pared 3 metros de ancho, 2.5 de alto, 20cm de grosor"
- [ ] "agrega una puerta de 80cm x 2.1m en la pared"
- [ ] "crea una ventana 1.2m x 1.5m"
- [ ] "haz un piso 4x4 metros"
- [ ] "crea un techo plano"

### FASE B: Materiales Arquitectónicos (Semana 2)
- [ ] "aplica concreto a la pared"
- [ ] "madera al piso"
- [ ] "vidrio a la ventana"
- [ ] "metal a la puerta"

### FASE C: Habitación Completa (Semana 3)
- [ ] "crea habitación 4x5x3 metros con paredes, piso, techo"
- [ ] "agrega 2 ventanas y 1 puerta"
- [ ] "iluminación interior"

---

## 📦 SIMPLIFICACIÓN AGRESIVA (Hacer hoy)

### Eliminar (simplifica ZULY)
- [ ] Borrar 38 handlers, quedarse con 10 arquitectónicos
- [ ] Eliminar 3 sistemas de validación, quedarse con JUESController
- [ ] Archivar 80% de bitácoras antiguas
- [ ] Consolidar a 1 solo modo: REACTIVE (simplificar agent.py)

### Quedarse con (núcleo arquitectónico)
1. **Handlers:**
   - crear_pared
   - crear_puerta
   - crear_ventana
   - crear_piso
   - crear_techo
   - aplicar_material
   - crear_luz
   - transformar_objeto
   - renderizar
   - exportar

2. **Validación:**
   - Solo JUESController (ya integrado)
   - 3 validaciones básicas: ¿se creó? ¿medidas correctas? ¿material aplicado?

3. **Memoria:**
   - C2 solo para patrones arquitectónicos
   - Ej: "cuando digo 'habitación', crear paredes+piso+techo"

---

## 🧪 TEST REAL (Próximos 7 días)

### Usuario 1: Tú (11 Abril)
- [ ] Crear pared con medidas exactas
- [ ] Verificar que mide lo que pediste
- [ ] Validar JUES da >90pts

### Usuario 2: Conocido (12-13 Abril)
- [ ] Dar comando sin ayuda: "crea una pared"
- [ ] Observar si entiende sin explicaciones
- [ ] Feedback: ¿qué no entendió?

### Usuario 3: Desconocido (14-15 Abril)
- [ ] Mismo test
- [ ] Medir tiempo: ¿cuánto tarda en crear una habitación?

---

## 📁 ESTRUCTURA NUEVA (Limpiar hoy)

```
ZULY_IA_LOCAL/
├── zuly.py                    # Entry point simple
├── core/
│   ├── agent.py               # Simplificado (eliminar 50%)
│   ├── handlers/
│   │   └── arquitectura.py    # 10 handlers básicos
│   └── jues_controller.py     # Ya listo
├── templates/
│   ├── pared.blend            # Template base pared
│   ├── puerta.blend           # Template puerta
│   └── ventana.blend          # Template ventana
├── training/
│   └── vocabulario_arquitectonico.json
└── tests/
    └── test_arquitectura_real.py
```

---

## 🚀 PRIMER PASO (Hacer ahora, 30 min)

### 1. Crear handler `crear_pared`
```python
# core/handlers/arquitectura.py
def crear_pared(ancho: float, alto: float, grosor: float = 0.2):
    """
    Crea una pared arquitectónica con medidas exactas.
    
    Args:
        ancho: metros (e.g., 3.0)
        alto: metros (e.g., 2.5)
        grosor: metros (default 0.2m = 20cm)
    """
    # Usar BMesh para crear malla procedural
    # Validar: medidas > 0
    # Crear cubo escalado a medidas
    # Retornar objeto creado
    pass
```

### 2. Entrenar NLU con vocabulario arquitectónico
```json
{
  "pared": ["pared", "muro", "tabique", "divisorio"],
  "puerta": ["puerta", "porton", "entrada", "acceso"],
  "ventana": ["ventana", "ventanal", "lucernario"],
  "medidas": ["metros", "m", "x", "por", "de"]
}
```

### 3. Test inmediato
```bash
python zuly.py "crea una pared de 3 metros por 2.5 metros"
# → ¿Crea pared 3x2.5x0.2m?
# → ¿JUES reporta 100pts?
```

---

## ✅ CHECKLIST PARA HOY (90% → 100%)

- [ ] Simplificar agent.py (eliminar modo HYBRID, FAILSAFE, etc.)
- [ ] Crear handler `crear_pared` funcional
- [ ] Test: crear pared 3x2.5m → medir en Blender
- [ ] Documentar en bitácora: primera pared arquitectónica

---

## 💰 PROPUESTA DE VALOR (Para usuarios)

### Antes (Blender tradicional):
1. Shift+A → Mesh → Cube
2. Tab → Modo edición
3. Escalar manualmente
4. Aplicar material
5. 5 minutos, conocimiento técnico requerido

### Después (ZULY Arquitectura):
1. "crea pared 3x2.5 metros concreto"
2. Listo. 5 segundos.

**Valor:** 60x más rápido, no requiere saber Blender.

---

## 🎓 PRÓXIMOS PASOS (Después de hoy)

### Semana 1: Paredes, puertas, ventanas
### Semana 2: Materiales, iluminación
### Semana 3: Habitaciones completas, exportar a PDF/planos
### Semana 4: 3 usuarios de prueba

---

## 🏆 DEFINICIÓN DE ÉXITO

En 30 días:
- [ ] 1 arquitecto/diseñador usa ZULY semanalmente
- [ ] Puede crear habitación básica en <2 minutos sin ayuda
- [ ] 5 templates arquitectónicos funcionan 100%
- [ ] 0 fases nuevas, solo mejoras al caso de uso real

---

**Decisión:** ¿Empezamos con `crear_pared` ahora?

Si SÍ → 30 min y tienes primera pared procedural.
Si NO → Seguimos en fases infinitas.

¿Tu respuesta?
