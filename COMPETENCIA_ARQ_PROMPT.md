# 🏆 COMPETENCIA: ARQ - Sistema de Reparación Pre-JUES

## 📋 DESAFÍO

Crear **ARQ** (Arquitecto de Reparación y Calidad) - un sistema que inspecciona y repara modelos 3D de Blender ANTES de pasar por validación JUES.

---

## 🎯 OBJETIVO

Flujo integrado:
```
Usuario: "crea habitación 4x5m"
    ↓
Handler crear_habitacion() → 6 objetos
    ↓
ARQ.inspect() → detecta problemas
    ↓
ARQ.repair() → corrige problemas (si hay)
    ↓
JUES.validate() → 100pts + bitácora
    ↓
Resultado al usuario
```

---

## 📦 ENTREGABLES REQUERIDOS

### 1. Estructura de archivos
```
core/repair/
├── __init__.py
├── arq_core.py          ← ORQUESTADOR (clase ARQCore)
├── mesh_analyzer.py     ← Detector de problemas
└── mesh_fixer.py        ← Corrector de problemas
```

### 2. API mínima (arq_core.py)

```python
class ARQCore:
    def inspect_mesh(self, obj_name: str) -> dict:
        """
        Retorna:
        {
            'duplicated_verts': int,      # vértices duplicados
            'inverted_normals': bool,       # normales invertidas
            'non_manifold_edges': int,      # bordes no-manifold
            'holes': int,                   # agujeros en malla
            'degenerate_faces': int,        # caras con área ~0
            'total_issues': int             # suma de todos
        }
        """
        pass
    
    def repair_mesh(self, obj_name: str) -> dict:
        """
        Ejecuta:
        - bpy.ops.mesh.remove_doubles()
        - bpy.ops.mesh.normals_make_consistent()
        - bpy.ops.mesh.fill_holes()
        
        Retorna:
        {
            'merged_verts': int,
            'fixed_normals': bool,
            'filled_holes': int,
            'success': bool
        }
        """
        pass
    
    def inspect_objects(self, obj_names: list) -> dict:
        """Inspección batch de múltiples objetos"""
        pass
    
    def repair_objects(self, obj_names: list) -> dict:
        """Reparación batch de múltiples objetos"""
        pass
    
    def generate_report(self, obj_names: list) -> dict:
        """
        Reporte final para JUES:
        {
            'arq_score': int,           # 0-100
            'issues_before': dict,
            'fixes_applied': dict,
            'issues_after': dict,
            'dictamen': 'REPARADO'|'LIMPIO'|'CRITICO',
            'timestamp': str
        }
        """
        pass
```

### 3. Integración obligatoria

Modificar `core/commands/blender_handlers/architectural.py`:

```python
def crear_habitacion_handler(parameters, adapter=None):
    # ... código existente crea 6 objetos ...
    
    # NUEVO: ARQ inspecciona y repara
    from core.repair.arq_core import ARQCore
    arq = ARQCore(adapter)
    
    # Inspección
    issues = arq.inspect_objects(created_objects)
    
    # Reparación si es necesario
    if issues['total_issues'] > 0:
        fixes = arq.repair_objects(created_objects)
        print(f"ARQ reparó: {fixes}")
    
    # Reporte para JUES
    arq_report = arq.generate_report(created_objects)
    
    # JUES valida
    jues_report = _validate_with_jues(pattern_id, v0, v1, v2)
    
    # Retorno incluye ambos reportes
    return {
        'success': True,
        'result': {
            'arq_validation': arq_report,
            'jues_validation': jues_report
        }
    }
```

---

## 🧪 TEST DE VALIDACIÓN

El código debe pasar este test:

```python
# test_arq_competencia.py
import sys; sys.path.insert(0, '.')

from core.repair.arq_core import ARQCore
from core.adapters import get_engine_adapter

adapter = get_engine_adapter(force_mock=True)
arq = ARQCore(adapter)

# Test 1: Inspección de cubo limpio
result = arq.inspect_mesh('Cube')
assert result['duplicated_verts'] == 0
assert result['inverted_normals'] == False
assert result['total_issues'] == 0
print("✓ Test 1: Cubo limpio pasa")

# Test 2: Reparación simulada
result = arq.repair_mesh('Cube_Dirty')
assert result['success'] == True
assert 'merged_verts' in result
print("✓ Test 2: Reparación ejecuta")

# Test 3: Batch de 3 objetos
objs = ['Cube_001', 'Cube_002', 'Plane_001']
issues = arq.inspect_objects(objs)
assert issues['total_objects'] == 3
print("✓ Test 3: Batch inspection funciona")

# Test 4: Reporte para JUES
report = arq.generate_report(objs)
assert report['arq_score'] >= 0
assert report['dictamen'] in ['LIMPIO', 'REPARADO', 'CRITICO']
print("✓ Test 4: Reporte generado")

print("\n🏆 TODOS LOS TESTS PASARON")
```

---

## 🔧 RESTRICCIONES TÉCNICAS

### Blender API permitida:
```python
# Mesh analysis/repair
import bpy
import bmesh

# Operaciones permitidas:
bpy.ops.mesh.remove_doubles()
bpy.ops.mesh.normals_make_consistent()
bpy.ops.mesh.fill_holes()
bpy.ops.mesh.delete_loose()
bmesh.from_mesh()
bmesh.to_mesh()
```

### NO usar (fuera de scope):
- Geometry Nodes (nodes_analyzer.py NO requerido para Opción A)
- Modifiers complejos
- Shaders/materials
- Animaciones
- Physics

---

## 📊 CRITERIOS DE EVALUACIÓN

| Criterio | Peso | Descripción |
|----------|------|-------------|
| **Funcionalidad** | 40% | Pasa todos los tests |
| **Integración** | 30% | Funciona con crear_habitacion_handler() |
| **Código limpio** | 20% | PEP8, documentación, sin duplicados |
| **Manejo de errores** | 10% | Graceful degradation si Blender no responde |

**Puntaje máximo:** 100 puntos

**Mínimo para aprobar:** 70 puntos + todos los tests pasan

---

## 🏆 PREMIOS (Simbólicos)

- **1er lugar:** Integración directa a ZULY + crédito en README
- **2do lugar:** Mención en bitácora
- **3er lugar:** Feedback detallado del código

---

## ⏱️ TIEMPO LÍMITE

**30 minutos** desde recepción del prompt hasta entrega.

---

## 📤 ENTREGA

Formato: Archivos `.py` en estructura de carpetas exacta.

Validación: `python test_arq_competencia.py` debe pasar 4/4 tests.

---

## 💡 TIPS

1. **Empezar por arq_core.py** - Es el orquestador, el resto son helpers
2. **Usar bmesh para análisis** - Más rápido que bpy.ops para inspección
3. **bpy.ops para reparación** - Ya tienen los algoritmos optimizados
4. **Logging importante** - Usa `from core.utils.logging import log_info`
5. **Mock mode compatible** - Debe funcionar con `force_mock=True`

---

## 🔥 JUEZ FINAL

El ganador se determina por:
1. Tests pasan (sí/no) - Eliminación inmediata si falla
2. Puntaje de código (calidad, limpieza)
3. Tiempo de entrega (desempate)

**Juez:** JUESController evalúa el código con su sistema de validación.

---

*"El mejor código no es el más complejo, es el que funciona y se integra sin fricción."*

**¿LISTOS PARA EL RETO?** 🚀
