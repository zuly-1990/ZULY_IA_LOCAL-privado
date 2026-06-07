#!/usr/bin/env python3
"""
ANÁLISIS PROFUNDO DE PATRONES ZULY
Investigación para evolución del sistema
"""

import json
from collections import defaultdict
from datetime import datetime

def analisis_profundo():
    print("="*80)
    print("🔬 ANÁLISIS PROFUNDO DEL SISTEMA DE PATRONES ZULY")
    print("="*80)
    
    # Cargar patrones
    with open('memory/patterns_pending.json', 'r') as f:
        patrones = json.load(f)
    
    # ANÁLISIS 1: Dimensionalidad
    print("\n📊 ANÁLISIS DIMENSIONAL:\n")
    
    tipos_primitivas = defaultdict(int)
    tiene_color = 0
    tiene_posicion = 0
    tiene_transformacion = 0
    tiene_agujero = 0
    complejidad = {'simple': 0, 'media': 0, 'alta': 0}
    
    for p in patrones:
        req = p['user_request'].lower()
        
        # Detectar primitiva
        if 'cubo' in req or 'cube' in req:
            tipos_primitivas['cubo'] += 1
        elif 'esfera' in req or 'bola' in req or 'sphere' in req:
            tipos_primitivas['esfera'] += 1
        elif 'cilindro' in req or 'cylinder' in req:
            tipos_primitivas['cilindro'] += 1
        elif 'cono' in req or 'cone' in req:
            tipos_primitivas['cono'] += 1
        elif 'plano' in req or 'plane' in req:
            tipos_primitivas['plano'] += 1
        
        # Detectar atributos
        colores = ['rojo', 'azul', 'verde', 'amarillo', 'naranja', 'morado', 'café', 'negro', 'blanco']
        if any(c in req for c in colores):
            tiene_color += 1
        
        if 'posición' in req or 'posicion' in req:
            tiene_posicion += 1
        
        if any(t in req for t in ['mueve', 'mover', 'rota', 'rotar', 'escala', 'escalar', 'perfora', 'cava']):
            tiene_transformacion += 1
        
        if any(h in req for h in ['perfora', 'cava', 'agujero', 'hoyo']):
            tiene_agujero += 1
        
        # Clasificar complejidad
        atributos = sum([req.count('y') + 1, 1 if tiene_color else 0, 
                        1 if tiene_posicion else 0, 1 if tiene_transformacion else 0])
        if atributos <= 2:
            complejidad['simple'] += 1
        elif atributos <= 4:
            complejidad['media'] += 1
        else:
            complejidad['alta'] += 1
    
    print("PRIMITIVAS APRENDIDAS:")
    for tipo, count in sorted(tipos_primitivas.items(), key=lambda x: -x[1]):
        barra = '█' * count
        print(f"  {tipo:12} {count:2} {barra}")
    
    print(f"\nATRIBUTOS:")
    print(f"  Con color:      {tiene_color}/{len(patrones)} ({tiene_color/len(patrones)*100:.0f}%)")
    print(f"  Con posición:   {tiene_posicion}/{len(patrones)} ({tiene_posicion/len(patrones)*100:.0f}%)")
    print(f"  Con transform:  {tiene_transformacion}/{len(patrones)} ({tiene_transformacion/len(patrones)*100:.0f}%)")
    print(f"  Con agujeros:   {tiene_agujero}/{len(patrones)} ({tiene_agujero/len(patrones)*100:.0f}%)")
    
    print(f"\nCOMPLEJIDAD:")
    for nivel, count in complejidad.items():
        print(f"  {nivel:10}: {count}")
    
    # ANÁLISIS 2: Cobertura de handlers
    print("\n" + "="*80)
    print("🔍 ANÁLISIS DE COBERTURA:\n")
    
    handlers_unicos = set()
    for p in patrones:
        handlers_unicos.add(p['intent']['command_name'])
    
    print(f"Handlers únicos: {len(handlers_unicos)}")
    for h in sorted(handlers_unicos):
        print(f"  • {h}")
    
    # ANÁLISIS 3: GAPS identificados
    print("\n" + "="*80)
    print("⚠️ GAPS IDENTIFICADOS (Lo que FALTA):\n")
    
    gaps = []
    
    # Primitivas faltantes
    primitivas_faltantes = [
        'torus'           # Dona - no está
    ]
    gaps.append(("PRIMITIVAS", primitivas_faltantes))
    
    # Materiales avanzados
    materiales_faltantes = [
        'texturas'        # UV mapping, imágenes
        'metallic'        # Materiales metálicos
        'glass'           # Vidrio
        'emission'        # Emisivo
    ]
    gaps.append(("MATERIALES", materiales_faltantes))
    
    # Transformaciones
    transform_faltantes = [
        'escala_proporcional',    # Escalar manteniendo proporciones
        'rotacion_precisa',       # Rotación exacta en grados
        'posicion_relativa',      # Mover respecto a otro objeto
    ]
    gaps.append(("TRANSFORMACIONES", transform_faltantes))
    
    # Operaciones booleanas
    booleanas_faltantes = [
        'union',           # Unir objetos
        'diferencia',      # Restar (ya tenemos agujeros parcialmente)
        'interseccion',    # Intersección
    ]
    gaps.append(("BOOLEANAS", booleanas_faltantes))
    
    # Modificadores
    modificadores_faltantes = [
        'bevel',           # Biselado de bordes
        'subdivision',     # Subsurf
        'array',           # Array de objetos
        'mirror',          # Espejo
        'solidify',        # Dar grosor
    ]
    gaps.append(("MODIFICADORES", modificadores_faltantes))
    
    # Iluminación
    iluminacion_faltantes = [
        'luz_puntual',     # Point light
        'luz_area',        # Area light
        'luz_spot',        # Spot light
        'hdri',            # Ambiente HDRI
        'sombras_config',  # Configurar sombras
    ]
    gaps.append(("ILUMINACIÓN", iluminacion_faltantes))
    
    # Cámara y render
    camara_faltantes = [
        'animacion_camara',       # Movimiento de cámara
        'focal_length',           # Distancia focal
        'depth_of_field',         # Profundidad de campo
        'render_animacion',       # Video, no solo frames
    ]
    gaps.append(("CÁMARA/RENDER", camara_faltantes))
    
    # Procedurales complejos
    procedurales_faltantes = [
        'arrays_complejos',       # Patrones repetitivos
        'displacement',           # Desplazamiento de geometría
        'curvas_bezier',          # Curvas y superficies
        'particulas',             # Sistemas de partículas
    ]
    gaps.append(("PROCEDURALES", procedurales_faltantes))
    
    # Composición
    composicion_faltantes = [
        'colecciones',            # Organizar en colecciones
        'parenting',              # Jerarquía padre-hijo
        'constraints',            # Constraints
        'drivers',                # Drivers para animación
    ]
    gaps.append(("COMPOSICIÓN", composicion_faltantes))
    
    for categoria, items in gaps:
        print(f"{categoria}:")
        for item in items:
            print(f"  ❌ {item}")
        print()
    
    # ANÁLISIS 4: Recomendaciones
    print("="*80)
    print("🎯 RECOMENDACIONES DE EVOLUCIÓN:\n")
    
    recomendaciones = [
        ("ALTA", "Materiales avanzados", "Permitir crear materiales metálicos, vidrio, emisivos"),
        ("ALTA", "Modificador Bevel", "Biselado automático para bordes suaves en todas las primitivas"),
        ("MEDIA", "Operaciones booleanas completas", "Unión, diferencia e intersección estructuradas"),
        ("MEDIA", "Iluminación profesional", "Setup de 3 luces básico (key, fill, rim)"),
        ("MEDIA", "Arrays y repeticiones", "Crear filas, grilles y patrones repetitivos"),
        ("BAJA", "Animación básica", "Keyframes simples para movimiento de objetos"),
        ("BAJA", "Curvas Bezier", "Path creation para flujos complejos"),
        ("INVESTIGAR", "Evolución autónoma", "Sistema para que ZULY proponga nuevos patrones"),
    ]
    
    for prio, tema, desc in recomendaciones:
        icono = "🔴" if prio == "ALTA" else "🟡" if prio == "MEDIA" else "🟢" if prio == "BAJA" else "🔵"
        print(f"{icono} [{prio}] {tema}")
        print(f"      {desc}\n")
    
    print("="*80)
    print("📈 PRIORIDAD ESTRATÉGICA:\n")
    print("""
FASE 1 (Inmediata - Semana 1):
  1. Materiales avanzados (metal, vidrio, emisivo)
  2. Modificador Bevel para todas las primitivas
  3. Aprobar los 23 patrones existentes

FASE 2 (Corto plazo - Semana 2-3):
  4. Iluminación profesional (3-point lighting)
  5. Operaciones booleanas (union, diferencia, intersección)
  6. Arrays y repeticiones

FASE 3 (Mediano plazo - Mes 2):
  7. Animación básica con keyframes
  8. Sistema de propuesta autónoma de patrones
  9. Integración con Gemini para sugerencias

El cuello de botella actual NO es cantidad de patrones,
es COMPLEJIDAD DE PATRONES (solo simples y medios).
""")
    
    print("="*80)
    print(f"✅ ANÁLISIS COMPLETADO")
    print("="*80)

if __name__ == "__main__":
    analisis_profundo()
