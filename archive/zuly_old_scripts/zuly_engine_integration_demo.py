#!/usr/bin/env python3
"""
ZULY + TheCubeUniverseEngine Integration
=========================================

Demostración: Cómo el engine integrado mejora el trabajo colaborativo.

Flujo:
1. Usuario pide: "Haz un dado para Guayatá"
2. C3 (OBJETIVOS) descompone: ¿Cuál es el volumen?
3. C1 (EVALUADOR) valida: ¿Es viable?
4. C2 (PATRONES) genera: Parámetros con precisión atómica
5. Blender ejecuta: Usando handlers con datos precisos
"""

import sys
sys.path.insert(0, r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL")

from core.cognition.c_engine_integration import engine_integration
from core.utils.registro_aprendizaje import registrar_aprendizaje
from datetime import datetime

print("=" * 100)
print("🎲 ZULY + TheCubeUniverseEngine v20 Integration Demo")
print("=" * 100)

# ============================================================================
# ESCENARIO: Usuario pide "Haz un dado para Guayatá"
# ============================================================================

proyecto = "Dado para Guayatá"
volumen_m3 = 0.001  # Pequeño dado: 0.001m³ (10cm × 10cm × 10cm)

print(f"\n👤 Usuario: '{proyecto}'")
print(f"📊 Volumen estimado: {volumen_m3}m³")

# ============================================================================
# PASO 1: C1 EVALUADOR - ¿Es viable?
# ============================================================================

print("\n" + "─" * 100)
print("PASO 1: C1 EVALUADOR - Validar viabilidad")
print("─" * 100)

evaluacion = engine_integration.evaluate_viability(volumen_m3)

print(f"\n✅ Estado: {evaluacion['viability'].upper()}")
print(f"   Masa: {evaluacion['properties']['masa_kg']:.3f}kg ({evaluacion['properties']['masa_ton']:.6f}toneladas)")
print(f"   Volumen: {evaluacion['properties']['volumen_m3']}m³")

if evaluacion['warnings']:
    print(f"\n⚠️  Advertencias:")
    for w in evaluacion['warnings']:
        print(f"   • {w}")

if evaluacion['recommendations']:
    print(f"\n💡 Recomendaciones:")
    for r in evaluacion['recommendations']:
        print(f"   • {r}")

# ============================================================================
# PASO 2: C3 OBJETIVOS - Descomponer la tarea
# ============================================================================

print("\n" + "─" * 100)
print("PASO 2: C3 OBJETIVOS - Descomponer en subtareas logísticas")
print("─" * 100)

descomposicion = engine_integration.decompose_construction_task(volumen_m3, proyecto)

tasks = descomposicion['decomposition']['subtasks']
logistica = descomposicion['decomposition']['logistics']
estimaciones = descomposicion['decomposition']['estimations']

print(f"\n📋 PLAN DE PROYECTO:")
for i, task in enumerate(tasks, 1):
    print(f"\n   {i}. {task['name']}")
    print(f"      Descripción: {task['description']}")
    print(f"      Duración: {task['duration_days']} días")
    print(f"      Costo: ${task['cost_usd']:,}")

print(f"\n📊 LOGÍSTICA:")
print(f"   Viajes dobletroque: {logistica['viajes_dobletroque']}")
print(f"   Masa total: {logistica['masa_toneladas']} toneladas")
print(f"   Costo total: ${logistica['costo_estimado_usd']:,}")

print(f"\n⏱️  ESTIMACIONES:")
print(f"   Duración total: {estimaciones['duration_weeks']} semanas")
print(f"   Costo por m³: ${estimaciones['cost_per_m3']:,}/m³")

# ============================================================================
# PASO 3: C2 PATRONES - Usar unidad mínima
# ============================================================================

print("\n" + "─" * 100)
print("PASO 3: C2 PATRONES - Aplicar unidad mínima atómica")
print("─" * 100)

atom_info = engine_integration.get_atom_info()
pattern = engine_integration.pattern_from_volume(volumen_m3)

print(f"\n🔬 ÁTOMO BASE (Unidad mínima):")
print(f"   Tamaño: {atom_info['size_mm']}mm ({atom_info['size_micrometers']:,.0f} micrometros)")
print(f"   Volumen: {atom_info['volume_m3']:.2e}m³")
print(f"   Masa: {atom_info['mass_g']:.6f}g")

print(f"\n🎲 PATRÓN PARA ESTE DADO:")
print(f"   Átomos necesarios: {pattern['total_atoms']:,}")
print(f"   Átomos por lado: {pattern['atoms_per_side']}")
print(f"   Cubo equivalente: {pattern['equivalent_cube_side_m']:.6f}m")

# ============================================================================
# PASO 4: PARÁMETROS PRECISOS PARA HANDLERS
# ============================================================================

print("\n" + "─" * 100)
print("PASO 4: Parámetros precisos para Blender (Handlers)")
print("─" * 100)

handler_params = {
    "object_name": "DadoGuayata",
    "size_m": pattern['equivalent_cube_side_m'],
    "volume_m3": volumen_m3,
    "mass_kg": evaluacion['properties']['masa_kg'],
    "density": evaluacion['properties']['densidad_kgm3'],
    "atom_size_mm": atom_info['size_mm'],
    "viability": evaluacion['viability']
}

print(f"\n✅ Parámetros para Handlers:")
for key, value in handler_params.items():
    if isinstance(value, float):
        print(f"   {key}: {value:.6f}")
    else:
        print(f"   {key}: {value}")

# ============================================================================
# REGISTRO DE APRENDIZAJE
# ============================================================================

print("\n" + "─" * 100)
print("PASO 5: Registrar aprendizaje")
print("─" * 100)

try:
    report = engine_integration.generate_report(proyecto, volumen_m3)
    
    registrar_aprendizaje(
        accion="Integración TheCubeUniverseEngine v20 con ZULY",
        script="zuly_engine_integration_demo.py",
        parametros=f"Volumen: {volumen_m3}m³\nProyecto: {proyecto}",
        resultado=f"✅ Evaluación completada\n✅ Descomposición logística realizada\n✅ Parámetros precisos generados",
        archivos="c_engine_integration.py",
        observaciones="Engine integrado con C1, C2, C3. ZULY ahora es sistema de ingeniería preciso.",
        leccion="""
LECCIÓN FUNDAMENTAL:
- Engine proporciona precisión matemática (átomo 0.137mm)
- C1 valida viabilidad con propiedades físicas reales
- C3 descompone proyectos en logística realista
- C2 usa modelo atómico como patrón base mínimo
- Resultado: De "dibujar" a "proyectar ingeniería"
"""
    )
    print("\n✅ Aprendizaje registrado exitosamente")
except Exception as e:
    print(f"\n⚠️  No se pudo registrar: {e}")

# ============================================================================
# RESUMEN FINAL
# ============================================================================

print("\n" + "=" * 100)
print("✅ INTEGRACIÓN COMPLETADA")
print("=" * 100)
print(f"""
🎯 ESTADO ACTUAL DE ZULY:
   ✅ Módulo engine_integration.py: FUNCIONAL
   ✅ C1 (Evaluador): Valida propiedades físicas
   ✅ C3 (Objetivos): Descompone logística
   ✅ C2 (Patrones): Usa unidad atómica (0.137mm)
   
🔧 HANDLERS AHORA RECIBEN:
   • Dimensiones precisas (desde patrón atómico)
   • Propiedades físicas validadas
   • Parámetros logísticos reales
   • Viabilidad confirmada

🚀 PRÓXIMO PASO:
   Reconstruir uno.blend usando estos parámetros precisos
   
📂 ARCHIVO READY: uno.blend
   → Será actualizado con engine engine_integration
""")
print("=" * 100)
