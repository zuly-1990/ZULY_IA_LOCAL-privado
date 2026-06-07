# PLAN DE CONSOLIDACIÓN ZULY - 2026
## "De la Parálisis a la Producción"

**Fecha inicio:** 11 Abril 2026  
**Duración estimada:** 3 semanas  
**Estado:** 0% completado

---

## 🎯 OBJETIVO FINAL

Tener **UN** sistema JUES funcional, **UN** controlador, **UNA** bitácora clara, y **CERO** TODOs críticos pendientes.

**Métrica de éxito:** `zuly "crea un cubo azul"` funciona en 1 comando sin errores.

---

## 📋 FASES DETALLADAS

---

## FASE 1: Deprecación JUES (Días 1-2)

### 1.1 Crear directorio de archivos obsoletos
```bash
mkdir core/deprecated/
mkdir scripts_deprecated/
```

### 1.2 Mover versiones antiguas de JUES
| Archivo | Destino | Estado |
|---------|---------|--------|
| `core/jues_bot.py` | `core/deprecated/jues_bot_v1.py` | 🔴 MOVER |
| `core/jues_bot_v2.py` | `core/deprecated/jues_bot_v2.py` | 🔴 MOVER |
| `core/jues_bot_validator.py` | `core/deprecated/jues_bot_validator.py` | 🔴 MOVER |
| `core/controlador_zuly_jues.py` | `core/deprecated/controlador_zuly_jues_v1.py` | 🔴 MOVER |

### 1.3 Verificar que JUESAggregator funciona
```bash
python -c "from core.cognition.jues_logic import JUESAggregator; j = JUESAggregator(); print('OK')"
```

### 1.4 Actualizar imports en archivos activos
- `core/cognition/cognition_core.py` ← YA TIENE JUESAggregator ✅
- `core/soberano_seal_system.py` ← VERIFICAR import

### Checklist Fase 1
- [ ] Directorio deprecated creado
- [ ] 4 archivos movidos
- [ ] JUESAggregator testeado
- [ ] 0 referencias a jues_bot.py en código activo

---

## FASE 2: Consolidar Controladores (Días 3-5)

### 2.1 Crear `core/jues_controller.py` (NUEVO ÚNICO)

Este archivo unifica:
- `controlador_zuly_jues.py`
- `soberano_seal_system.py` 
- `JUESAggregator`

```python
# core/jues_controller.py
"""
JUES Controller - Sistema Único de Validación y Sellado
"""
from core.cognition.jues_logic import JUESAggregator
from pathlib import Path
import json

class JUESController:
    """
    Controlador único que combina:
    - Validación JUES con ponderación
    - Sellado de patrones
    - Bitácora persistente
    """
    
    def __init__(self):
        self.aggregator = JUESAggregator()
        self.sellos_dir = Path("archivo_zuly/sellos")
        self.sellos_dir.mkdir(parents=True, exist_ok=True)
    
    def validar_y_sellar(self, blend_path, candidato_id, target_color, 
                         resultados_validacion, auto_aprobar=False):
        """
        Flujo completo: validar → evaluar JUES → sellar (si aplica)
        """
        # 1. Evaluar con JUESAggregator
        reporte = self.aggregator.generate_jues_report(
            pattern_id=candidato_id,
            save_to_bitacora=True,
            **resultados_validacion
        )
        
        # 2. Decidir acción
        if reporte['dictamen'] == 'APTO_PARA_SELLO' or auto_aprobar:
            return self._ejecutar_sello(blend_path, candidato_id, reporte)
        elif reporte['dictamen'].startswith('FALLO_CRITICO'):
            return self._rechazar(candidato_id, reporte)
        else:
            return self._pendiente_revision(candidato_id, reporte)
    
    def _ejecutar_sello(self, blend_path, candidato_id, reporte):
        """Ejecuta sellado físico del archivo"""
        sello_path = self.sellos_dir / f"{candidato_id}_SELLADO.blend"
        # Lógica de sellado...
        return {
            'status': 'SELLADO',
            'candidato_id': candidato_id,
            'ubicacion': str(sello_path),
            'puntuacion_jues': reporte['puntuacion_jues'],
            'dictamen': reporte['dictamen']
        }
    
    def _rechazar(self, candidato_id, reporte):
        """Rechaza patrón con fallos críticos"""
        return {
            'status': 'RECHAZADO',
            'candidato_id': candidato_id,
            'razon': reporte['dictamen'],
            'errores': reporte['errors']
        }
    
    def _pendiente_revision(self, candidato_id, reporte):
        """Pone en cola de revisión manual"""
        return {
            'status': 'PENDIENTE_REVISION',
            'candidato_id': candidato_id,
            'puntuacion_jues': reporte['puntuacion_jues'],
            'advertencias': reporte['warnings']
        }
    
    def get_estadisticas(self, dias=7):
        """Obtiene resumen de bitácora JUES"""
        return self.aggregator.get_bitacora_summary(days=dias)

# Singleton global
_jues_controller = None

def get_jues_controller():
    global _jues_controller
    if _jues_controller is None:
        _jues_controller = JUESController()
    return _jues_controller
```

### 2.2 Actualizar `core/agent.py`
```python
# Reemplazar imports de JUES antiguos
from core.jues_controller import get_jues_controller  # NUEVO

class Agent:
    def __init__(self):
        # ...
        self.jues = get_jues_controller()  # UNIFICADO
```

### 2.3 Actualizar `core/cognition/cognition_core.py`
```python
# Ya está integrado con JUESAggregator ✅
# Solo verificar que usa el mismo formato de reporte
```

### Checklist Fase 2
- [ ] `jues_controller.py` creado
- [ ] `agent.py` actualizado
- [ ] Tests pasan con nuevo controlador
- [ ] 0 referencias a archivos deprecated

---

## FASE 3: Resolver TODOs Críticos (Días 6-10)

### 3.1 TODO #1: Mode real en `core/agent.py:555`

**Ubicación:** Buscar línea con `final_response['mode'] = 'REACTIVE'`

**Solución:**
```python
def _detect_current_mode(self):
    """Detecta modo actual del agente basado en estado"""
    if hasattr(self, 'black_protocol') and self.black_protocol.is_active():
        return "SECURITY_LOCK"
    if hasattr(self, 'failsafe_executor') and self.failsafe_executor.is_running():
        return "FAILSAFE"
    if hasattr(self, 'context_guard') and self.context_guard.is_active():
        return "PROTECTED"
    if hasattr(self, 'learning_allowed') and not self.learning_allowed:
        return "RESTRICTED"
    return "REACTIVE"  # default

# En el código donde estaba el TODO:
final_response['mode'] = self._detect_current_mode()
```

### 3.2 TODO #2: Rollback detection en `core/state/state_awareness.py:211`

**Solución básica (sin listener de Blender):**
```python
def detect_rollback(self, current_scene_hash, previous_scene_hash):
    """
    Detecta si hubo rollback comparando hashes de escena.
    Implementación simple sin bpy.ops.undo (que es inestable)
    """
    if current_scene_hash != previous_scene_hash:
        # Verificar si el hash actual es igual a uno anterior (rollback)
        for i, old_hash in enumerate(reversed(self.scene_history[:-1])):
            if current_scene_hash == old_hash:
                return True, len(self.scene_history) - i - 1
    return False, None
```

### 3.3 TODO #3: Rollback triggered en `core/learning/pattern_memory.py:95`

**Solución:**
```python
# En PatternMemory.store_experience()
experience = {
    'timestamp': datetime.now().isoformat(),
    'command': command,
    'parameters': parameters,
    'score': score,
    'diagnosis': diagnosis,
    'rollback_triggered': diagnosis.get('rollback_detected', False),  # NUEVO
    'finalized': True
}
```

### 3.4 TODO #4: Validación de tipos en `core/utils/validators.py:360`

**Solución:**
```python
import typing
from typing import get_type_hints

def validate_types_strict(obj, expected_type):
    """Validación estricta usando type hints"""
    hints = get_type_hints(expected_type)
    for attr, attr_type in hints.items():
        if hasattr(obj, attr):
            value = getattr(obj, attr)
            if not isinstance(value, attr_type):
                raise TypeError(f"{attr}: esperado {attr_type}, got {type(value)}")
```

### Checklist Fase 3
- [ ] Mode real implementado
- [ ] Rollback detection básico
- [ ] Campo rollback_triggered agregado
- [ ] Validación de tipos mejorada
- [ ] DEUDA_TECNICA.md actualizado (0 críticos)

---

## FASE 4: Limpieza Documentación (Día 11)

### 4.1 Archivos a MOVER a `docs/archive/`:

**Resúmenes redundantes:**
- RESUMEN_FINAL.txt
- RESUMEN_FINAL_DIA.md
- RESUMEN_ETAPA5.md
- RESUMEN_SESION_ACTUAL.md
- RESUMEN_JUES_IMPLEMENTACION.txt
- DASHBOARD_ZULY_ESTADO_COMPLETO.txt
- DASHBOARD_FINAL.md
- COMPARACION_ARQUITECTURAS.txt
- RESUMEN_EJECUTIVO_*.md (mantener solo el más reciente)

**Análisis obsoletos:**
- ANALISIS_TIEMPO_ZULY.md
- ANALISIS_ZULY_MAESTRO.md (si hay versión más nueva)

### 4.2 Archivos a MANTENER (raíz):

| Archivo | Razón |
|---------|-------|
| 0_COMIENZA_AQUI.txt | Entry point |
| README_INDICE.md | Mapa del proyecto |
| BITACORA_DE_AVANCE/README.md | Plan C documentado |
| INFORME_CICLO_ZULY_2026-04-04.md | Informe más reciente |
| ARCHITECTURE_RULES.md | Reglas activas |

### 4.3 Estructura de bitácora limpia:
```
bitacora/
├── SESION_YYYY-MM-DD_*.md  # Solo sesiones de los últimos 2 meses
├── REGISTRO_APRENDIZAJE_*.md  # Aprendizajes validados
├── archive/  # Sesiones antiguas (>2 meses)
└── jues_reports/  # JSONs automáticos (ya existe)
```

### Checklist Fase 4
- [ ] docs/archive/ creado
- [ ] 15+ archivos movidos
- [ ] README_INDICE.md actualizado con rutas correctas
- [ ] Solo 5-7 archivos de resumen en raíz

---

## FASE 5: Prueba de Producción Real (Días 12-15)

### 5.1 Script de prueba único

Crear `test_produccion_real.py`:

```python
#!/usr/bin/env python3
"""
Test de producción real - El único test que importa
"""
import subprocess
import sys
from pathlib import Path

def test_comando_simple():
    """Test: zuly 'crea un cubo azul'"""
    print("="*60)
    print("TEST 1: Comando simple")
    result = subprocess.run(
        [sys.executable, "zuly_cli.py", "crea un cubo azul"],
        capture_output=True,
        text=True,
        cwd="c:/Users/Admin/Desktop/ZULY_IA_LOCAL"
    )
    success = result.returncode == 0 and "cubo" in result.stdout.lower()
    print(f"  {'✓' if success else '✗'} {'OK' if success else 'FALLÓ'}")
    return success

def test_validacion_jues():
    """Test: Validación JUES de resultado"""
    print("\n" + "="*60)
    print("TEST 2: Validación JUES")
    from core.jues_controller import get_jues_controller
    
    jues = get_jues_controller()
    resultados = {
        'v0_result': {'verified': True, 'details': 'OK'},
        'v1_result': {'verified': True, 'details': 'OK'},
        'v2_result': {'verified': True, 'details': 'OK'},
        'v3_result': {'verified': True, 'metrics': {'is_watertight': True}},
        'chromatic_sync_result': {'match': True, 'details': 'OK'},
        'optimization_instinct_result': {'optimized': True, 'details': 'OK'},
        'immutability_seal_result': {'verified': True, 'hash_short': 'abc'}
    }
    
    reporte = jues.aggregator.generate_jues_report(
        pattern_id="TEST_PROD",
        save_to_bitacora=False,
        **resultados
    )
    
    success = reporte['puntuacion_jues'] >= 90
    print(f"  {'✓' if success else '✗'} Puntuación: {reporte['puntuacion_jues']}")
    return success

def test_bitacora():
    """Test: Bitácora JUES funciona"""
    print("\n" + "="*60)
    print("TEST 3: Bitácora JUES")
    from core.jues_controller import get_jues_controller
    
    jues = get_jues_controller()
    stats = jues.get_estadisticas(dias=7)
    
    success = 'total_reportes' in stats
    print(f"  {'✓' if success else '✗'} Estadísticas disponibles")
    return success

def main():
    print("="*60)
    print("PRUEBA DE PRODUCCIÓN REAL - ZULY")
    print("="*60)
    
    tests = [
        test_comando_simple(),
        test_validacion_jues(),
        test_bitacora()
    ]
    
    print("\n" + "="*60)
    print(f"RESULTADO: {sum(tests)}/{len(tests)} tests pasaron")
    print("="*60)
    
    if all(tests):
        print("✅ SISTEMA LISTO PARA PRODUCCIÓN")
        return 0
    else:
        print("❌ SISTEMA NO LISTO - Revisar fallos")
        return 1

if __name__ == "__main__":
    sys.exit(main())
```

### 5.2 Criterios de aceptación

- [ ] `test_produccion_real.py` pasa 3/3 tests
- [ ] No hay errores de import
- [ ] Bitácora JUES genera archivos JSON
- [ ] Comando `zuly "crea un cubo azul"` funciona

---

## 📊 TRACKING DEL PLAN

Crear archivo de progreso:

```bash
echo "# Progreso Consolidación

## FASE 1: Deprecación JUES
- [ ] 1.1 Directorio deprecated creado
- [ ] 1.2 Archivos movidos
- [ ] 1.3 JUESAggregator testeado
- [ ] 1.4 Imports actualizados

## FASE 2: Controlador Unificado
- [ ] 2.1 jues_controller.py creado
- [ ] 2.2 agent.py actualizado
- [ ] 2.3 Tests pasan

## FASE 3: TODOs Resueltos
- [ ] 3.1 Mode real implementado
- [ ] 3.2 Rollback detection
- [ ] 3.3 rollback_triggered agregado
- [ ] 3.4 Validación tipos

## FASE 4: Documentación
- [ ] 4.1 Archivos movidos
- [ ] 4.2 README actualizado

## FASE 5: Prueba Real
- [ ] 5.1 test_produccion_real.py creado
- [ ] 5.2 3/3 tests pasan

**Progreso total: 0%**
" > PROGRESO_CONSOLIDACION.md
```

---

## 🚀 DECISIONES QUE TOMAR AHORA

### 1. ¿Empezamos hoy?
- [ ] SÍ → Crear `core/deprecated/` y mover primer archivo
- [ ] NO → Seguir documentando la parálisis

### 2. ¿Qué priorizas?
- **Opción A:** Deprecación primero (limpieza visible)
- **Opción B:** TODOs primero (funcionalidad crítica)
- **Opción C:** Documentación primero (orden mental)

### 3. ¿Límite de tiempo?
- **Realista:** 3 semanas (1 fase por semana)
- **Agresivo:** 1 semana (todo a la vez)
- **Eterno:** "Cuando tenga tiempo" (nunca)

---

## 💀 QUÉ PASA SI NO HACES ESTO

En 3 meses (julio 2026):
- Tendrás `jues_bot_v4.py` y `JUESAggregator_v2.py`
- 8 TODOs críticos en vez de 4
- 25 archivos de resumen en vez de 15
- Seguirás sin saber qué versión usar
- El proyecto será imposible de mantener

**O lo consolidas ahora, o lo abandonas en julio.**

---

## ✅ PRIMER PASO (hazlo ahora, 5 minutos)

```bash
cd c:/Users/Admin/Desktop/ZULY_IA_LOCAL
mkdir -p core/deprecated
mv core/jues_bot.py core/deprecated/
echo "jues_bot.py deprecado - usar JUESAggregator" > core/deprecated/README.txt
git add core/deprecated/
git commit -m "FASE 1.1: Inicio consolidacion - jues_bot.py deprecado"
```

**¿Lo haces?**
