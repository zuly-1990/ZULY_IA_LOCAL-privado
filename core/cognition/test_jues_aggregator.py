#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de prueba para JUESAggregator con bitácora.
Verifica que la generación de reportes y el almacenamiento en bitácora funcionen correctamente.
"""

import sys
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from core.cognition.jues_logic import JUESAggregator
from datetime import datetime

def create_mock_results():
    """Crea resultados mock para prueba."""
    return {
        "v0_result": {
            "verified": True,
            "details": "Objeto creado correctamente en Blender."
        },
        "v1_result": {
            "verified": True,
            "details": "Estructura del archivo Blender es válida."
        },
        "v2_result": {
            "verified": True,
            "details": "Contexto de escena es apropiado."
        },
        "v3_result": {
            "verified": True,
            "metrics": {
                "is_watertight": True,
                "non_manifold_edges_count": 0
            }
        },
        "chromatic_sync_result": {
            "match": True,
            "details": "Color exacto según especificaciones."
        },
        "optimization_instinct_result": {
            "optimized": True,
            "details": "Patrón optimizado y eficiente.",
            "final_size_kb": 245.5
        },
        "immutability_seal_result": {
            "verified": True,
            "hash_short": "a3f5e2b9"
        }
    }

def test_jues_aggregator():
    """Prueba el agregador JUES."""
    print("=" * 60)
    print("🧪 PRUEBA: JUESAggregator con Bitácora")
    print("=" * 60)
    
    # Crear instancia del agregador
    aggregator = JUESAggregator()
    print(f"✅ JUESAggregator inicializado.")
    print(f"   Directorio de bitácora: {aggregator.bitacora_dir}\n")
    
    # Crear resultados mock
    results = create_mock_results()
    
    # Generar reporte JUES
    print("📋 Generando reporte JUES...")
    report = aggregator.generate_jues_report(
        pattern_id="TEST_CUB001_V1",
        save_to_bitacora=True,
        **results
    )
    
    print(f"\n✅ Reporte JUES generado:")
    print(f"   Pattern ID: {report['pattern_id']}")
    print(f"   Puntuación: {report['puntuacion_jues']}/100")
    print(f"   Dictamen: {report['dictamen']}")
    print(f"   Hallazgos ({len(report['findings'])}): {', '.join(report['findings'][:2])}...")
    print(f"   Errores: {len(report['errors'])}")
    print(f"   Advertencias: {len(report['warnings'])}")
    
    # Obtener resumen de bitácora
    print("\n📊 Obteniendo resumen de bitácora...")
    summary = aggregator.get_bitacora_summary(days=7)
    print(f"   Total de reportes (últimos 7 días): {summary['total_reportes']}")
    print(f"   Puntuación promedio: {summary['promedio_puntuacion']}")
    if summary['por_dictamen']:
        print(f"   Distribución por dictamen: {summary['por_dictamen']}")
    
    print("\n" + "=" * 60)
    print("✓ PRUEBA COMPLETADA EXITOSAMENTE")
    print("=" * 60)

if __name__ == "__main__":
    try:
        test_jues_aggregator()
    except Exception as e:
        print(f"\n❌ ERROR durante la prueba: {e}")
        import traceback
        traceback.print_exc()
