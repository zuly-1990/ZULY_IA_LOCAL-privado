"""
Demo Completo de C2 - Memoria de Experiencias
==============================================

Demuestra toda la funcionalidad de C2:
1. Registrar experiencias
2. Analizar insights
3. Buscar patrones similares
4. Obtener sugerencias
5. Exportar memoria

Integración con C1 y LYZU Core.
"""

from core.cognition.c2_experience_memory import (
    C2ExperienceMemory, ExperienceType, PatternMatcher, 
    ExperienceExtractor, HeuristicBuilder
)
from pathlib import Path
import json
from datetime import datetime


def print_section(title: str):
    """Imprime un título de sección"""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}")


def print_subsection(title: str):
    """Imprime un subtítulo"""
    print(f"\n{'-'*70}")
    print(f"  {title}")
    print(f"{'-'*70}")


def demo_basic_storage():
    """Demuestra almacenamiento básico"""
    print_section("DEMO 1: Almacenamiento de Experiencias")
    
    memory = C2ExperienceMemory()
    
    # Simular varias experiencias
    experiences_data = [
        ('Crear cubo 3D', 'success', 0.95, 4, 4, [], ['Excelente geometría']),
        ('Crear esfera', 'success', 0.88, 3, 4, ['Baja resolución'], ['Aumentar resolución']),
        ('Crear pirámide', 'failed', 0.3, 1, 4, ['Error de geometría'], ['Usar parámetros correctos']),
        ('Crear cilindro', 'success', 0.92, 4, 4, [], ['Perfecto']),
        ('Crear cono', 'partial', 0.65, 2, 4, ['Material incompleto'], ['Agregar textura']),
    ]
    
    print("\n[*] Registrando experiencias...")
    for obj, status, score, passed, total, issues, recs in experiences_data:
        exp_id = memory.record_experience(
            objective=obj,
            evaluation={
                'status': status,
                'score': score,
                'metrics_passed': passed,
                'metrics_total': total,
                'issues': issues,
                'recommendations': recs,
                'parameters': {'size': 10}
            }
        )
        print(f"  [OK] ID {exp_id}: {obj} ({status})")
    
    print("\n[*] Experiencias almacenadas exitosamente!")


def demo_insights_analysis():
    """Demuestra análisis de insights"""
    print_section("DEMO 2: Análisis de Insights")
    
    memory = C2ExperienceMemory()
    
    # Registrar experiencias previas
    for i in range(8):
        status = 'success' if i % 2 == 0 else 'failed'
        score = 0.9 if status == 'success' else 0.3
        
        memory.record_experience(
            objective=f'Crear objeto {i}',
            evaluation={
                'status': status,
                'score': score,
                'metrics_passed': 4 if status == 'success' else 1,
                'metrics_total': 4,
                'issues': [] if status == 'success' else ['Error genérico'],
                'recommendations': ['Bien'] if status == 'success' else ['Revisar'],
                'parameters': {}
            }
        )
    
    # Obtener insights
    insights = memory.get_insights()
    
    print("\n[*] Analizando historial...")
    print(f"\n  Total de Experiencias: {insights['total_experiences']}")
    print(f"  Tasa de Éxito: {insights['success_rate']:.1%}")
    print(f"  Score Promedio: {insights['average_score']:.2f}")
    print(f"  Éxitos: {insights['successes']}")
    print(f"  Fallos: {insights['failures']}")
    
    if insights['common_issues']:
        print(f"\n[*] Problemas más comunes:")
        for issue, count in list(insights['common_issues'].items())[:3]:
            print(f"  - {issue} ({count} veces)")
    
    if insights['failure_reasons']:
        print(f"\n[*] Razones principales de fracaso:")
        for reason, count in list(insights['failure_reasons'].items())[:3]:
            print(f"  - {reason} ({count} veces)")


def demo_pattern_matching():
    """Demuestra búsqueda de patrones"""
    print_section("DEMO 3: Búsqueda de Patrones Similares")
    
    memory = C2ExperienceMemory()
    
    # Registrar experiencias con objetivos similares
    objetivos = [
        'Crear cubo 3D rojo',
        'Crear cubo 3D azul',
        'Crear cubo grande',
        'Crear esfera de metal',
        'Renderizar escena',
    ]
    
    for objetivo in objetivos:
        memory.record_experience(
            objective=objetivo,
            evaluation={
                'status': 'success' if 'cubo' in objetivo.lower() else 'partial',
                'score': 0.9 if 'cubo' in objetivo.lower() else 0.7,
                'metrics_passed': 4 if 'cubo' in objetivo.lower() else 3,
                'metrics_total': 4,
                'issues': [],
                'recommendations': ['OK'],
                'parameters': {}
            }
        )
    
    # Buscar similares
    print("\n[*] Buscando experiencias similares a 'Crear cubo'...")
    suggestions = memory.get_suggestions_for('Crear cubo')
    
    print(f"\n  Experiencias similares: {suggestions['similar_experiences']}")
    print(f"  Intentos fallidos: {suggestions['failed_attempts']}")
    
    if suggestions['improvement_suggestions']:
        print(f"\n[*] Sugerencias de mejora:")
        for sugg in suggestions['improvement_suggestions'][:3]:
            print(f"  - {sugg}")


def demo_heuristics():
    """Demuestra construcción de heurísticas"""
    print_section("DEMO 4: Construcción de Heurísticas")
    
    memory = C2ExperienceMemory()
    
    # Registrar experiencias con parámetros similares exitosos
    print("\n[*] Registrando experiencias con parámetros variados...")
    
    for i in range(6):
        memory.record_experience(
            objective='Crear cubo',
            evaluation={
                'status': 'success',
                'score': 0.95 - (i * 0.02),
                'metrics_passed': 4,
                'metrics_total': 4,
                'issues': [],
                'recommendations': ['Excelente'],
                'parameters': {
                    'size': 10,
                    'color': ['red', 'blue', 'green', 'red', 'blue', 'green'][i],
                    'position': [0, 5, 10, 0, 5, 10][i]
                }
            }
        )
    
    # Obtener sugerencias
    suggestions = memory.get_suggestions_for('Crear cubo nuevo')
    
    print(f"\n[*] Parámetros recomendados (basados en éxitos):")
    for param, value in suggestions['suggested_parameters'].items():
        print(f"  - {param}: {value}")


def demo_learnings():
    """Demuestra extracción de lecciones"""
    print_section("DEMO 5: Extracción de Lecciones Aprendidas")
    
    memory = C2ExperienceMemory()
    
    # Registrar muchas experiencias exitosas
    print("\n[*] Registrando 10 experiencias exitosas...")
    for i in range(10):
        memory.record_experience(
            objective=f'Tarea {i}',
            evaluation={
                'status': 'success',
                'score': 0.85 + (i * 0.01),
                'metrics_passed': 4,
                'metrics_total': 4,
                'issues': [],
                'recommendations': [],
                'parameters': {}
            }
        )
    
    # Obtener lecciones
    learnings = memory.get_all_learnings()
    
    print(f"\n[*] Lecciones Aprendidas ({len(learnings)} total):")
    for i, learning in enumerate(learnings, 1):
        print(f"\n  Lección {i}:")
        print(f"    Tipo: {learning['type']}")
        print(f"    Contenido: {learning['learning']}")
        print(f"    Confianza: {learning['confidence']:.1%}")


def demo_full_workflow():
    """Demuestra flujo completo: registro → análisis → sugerencias"""
    print_section("DEMO 6: Flujo Completo de C2")
    
    memory = C2ExperienceMemory()
    
    print("\n[1/3] Fase de Aprendizaje: Registrando 15 experiencias...")
    
    tareas = [
        ('Crear cubo', 'success', 0.95),
        ('Crear esfera', 'success', 0.88),
        ('Crear pirámide', 'failed', 0.2),
        ('Mover objeto', 'success', 0.92),
        ('Rotar objeto', 'partial', 0.65),
        ('Escalar objeto', 'success', 0.90),
        ('Renderizar', 'success', 0.94),
        ('Animar', 'partial', 0.60),
        ('Duplicar', 'success', 0.93),
        ('Agrupar', 'success', 0.89),
        ('Desagrupar', 'partial', 0.70),
        ('Hacer material', 'partial', 0.62),
        ('Agregar textura', 'failed', 0.25),
        ('Agregar luz', 'success', 0.91),
        ('Agregar cámara', 'success', 0.88),
    ]
    
    for tarea, status, score in tareas:
        memory.record_experience(
            objective=tarea,
            evaluation={
                'status': status,
                'score': score,
                'metrics_passed': int(score * 4),
                'metrics_total': 4,
                'issues': [] if status == 'success' else ['Necesita revisión'],
                'recommendations': ['OK'],
                'parameters': {}
            }
        )
    
    print("[OK] 15 experiencias registradas")
    
    print("\n[2/3] Fase de Análisis: Procesando datos...")
    insights = memory.get_insights()
    
    print(f"\n  Estadísticas:")
    print(f"    - Total: {insights['total_experiences']}")
    print(f"    - Éxito: {insights['success_rate']:.1%}")
    print(f"    - Score: {insights['average_score']:.2f}/1.0")
    
    print("\n[3/3] Fase de Sugerencias: Para nueva tarea 'Crear cubo texturizado'...")
    
    suggestions = memory.get_suggestions_for('Crear cubo texturizado')
    
    print(f"\n  Análisis:")
    print(f"    - Casos similares: {suggestions['similar_experiences']}")
    print(f"    - Mejoras sugeridas: {len(suggestions['improvement_suggestions'])}")
    
    # Exportar
    print("\n[BONUS] Exportando memoria a JSON...")
    export_path = Path('bitacora/c2_demo_export.json')
    success = memory.export_memory(export_path)
    
    if success:
        print(f"[OK] Exportado a {export_path}")
        
        # Mostrar preview del JSON
        with open(export_path) as f:
            data = json.load(f)
        print(f"\n[*] Preview del JSON:")
        print(f"    - Total experiencias: {data['total_experiences']}")
        print(f"    - Lecciones aprendidas: {len(data['learnings'])}")
    else:
        print("[ERROR] No se pudo exportar")


def main():
    """Ejecuta todas las demostraciones"""
    print("\n")
    print("  " + "="*68)
    print("  " + " "*15 + "C2 - MEMORIA DE EXPERIENCIAS")
    print("  " + " "*18 + "DEMOSTRACIÓN COMPLETA")
    print("  " + "="*68)
    
    try:
        demo_basic_storage()
        demo_insights_analysis()
        demo_pattern_matching()
        demo_heuristics()
        demo_learnings()
        demo_full_workflow()
        
        print_section("CONCLUSIÓN")
        print("\n[OK] Todas las demostraciones completadas exitosamente!")
        print("\nC2 demuestra capacidades de:")
        print("  - Almacenamiento persistente de experiencias")
        print("  - Análisis estadístico de patrones")
        print("  - Búsqueda de casos similares")
        print("  - Extracción de heurísticas")
        print("  - Aprendizaje de experiencias pasadas")
        print("  - Generación de sugerencias inteligentes")
        
        print("\n[+] Próximo paso: C3 - Objetivos Abstractos")
        print("    C3 aprenderá a descomponer objetivos complejos en subtareas\n")
        
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
