#!/usr/bin/env python3
"""
🚀 ORDEN DE EJECUCIÓN - PRUEBA DE IAs CON VARIACIONES MÚLTIPLES
Sistema ZULY - Benchmark de IAs para generación de patrones 3D
"""

# ============================================================================
# 📋 PROMPT DE EJECUCIÓN PARA AGENTES IA
# ============================================================================

EJECUCION_PROMPT = """
╔═══════════════════════════════════════════════════════════════════════════╗
║                    🧠 ORDEN DE EJECUCIÓN ZULY - BENCHMARK IA              ║
╚═══════════════════════════════════════════════════════════════════════════╝

📅 FECHA: 2026-04-03
🎯 OBJETIVO: Evaluar capacidad de IAs para generar patrones 3D con variaciones
🏆 META: Encontrar la IA más efectiva para el sistema ZULY

═══════════════════════════════════════════════════════════════════════════
📝 TAREA A REALIZAR
═══════════════════════════════════════════════════════════════════════════

Generar el patrón base "CUB-001_Modelado_BiselRealista" con MÚLTIPLES 
VARIACIONES automáticas según parámetros editables.

═══════════════════════════════════════════════════════════════════════════
📐 ESPECIFICACIÓN DEL PATRÓN BASE
═══════════════════════════════════════════════════════════════════════════

ID: CUB-001
Nombre: CUB-001_Modelado_BiselRealista
Descripción: Cubo con bordes redondeados usando modificador Bevel

PROPIEDADES EDITABLES:
┌─────────────────────┬─────────────┬────────────────┐
│ Parámetro           │ Default     │ Rango          │
├─────────────────────┼─────────────┼────────────────┤
│ bevel_width         │ 0.05        │ 0.001 - 0.2    │
│ bevel_segments      │ 3           │ 1 - 6          │
│ auto_smooth_angle   │ 30°         │ 10° - 90°      │
│ cube_size           │ 2.0         │ 0.1 - 10.0     │
│ material_roughness  │ 0.4         │ 0.0 - 1.0      │
└─────────────────────┴─────────────┴────────────────┘

═══════════════════════════════════════════════════════════════════════════
🎲 VARIACIONES REQUERIDAS (Generar TODAS)
═══════════════════════════════════════════════════════════════════════════

Debes generar 5 VARIACIONES del patrón base:

VARIACIÓN 1: "Sutil" (Mínima)
  - bevel_width: 0.01
  - bevel_segments: 2
  - cube_size: 2.0
  - material: Blanco mate (roughness: 0.8)

VARIACIÓN 2: "Estándar" (Default)
  - bevel_width: 0.05
  - bevel_segments: 3
  - cube_size: 2.0
  - material: Gris técnico (roughness: 0.4)

VARIACIÓN 3: "Pronunciado" (Máxima dentro de rango seguro)
  - bevel_width: 0.15
  - bevel_segments: 5
  - cube_size: 3.0
  - material: Metal plateado (metallic: 0.9, roughness: 0.2)

VARIACIÓN 4: "Arquitectónico" (Proporción diferente)
  - bevel_width: 0.03
  - bevel_segments: 4
  - cube_size: Ancho: 4.0, Alto: 2.0, Profundo: 0.5 (muro)
  - material: Concreto (roughness: 0.9, color: gris oscuro)

VARIACIÓN 5: "Orgánico" (Forma suavizada)
  - bevel_width: 0.08
  - bevel_segments: 6
  - cube_size: 2.5
  - Subsurf modificador: 2 niveles
  - material: Plástico brillante (roughness: 0.1, color: azul)

═══════════════════════════════════════════════════════════════════════════
✅ CRITERIOS DE EVALUACIÓN (Cada variación debe cumplir)
═══════════════════════════════════════════════════════════════════════════

[ ] CÓDIGO FUNCIONAL
    - Script Python ejecutable en Blender 3.6
    - Sin errores de sintaxis
    - Sin imports innecesarios

[ ] ESTRUCTURA ZULY CORRECTA
    - Nombres técnicos: CUB-001_v1, CUB-001_v2, etc.
    - Tags ordenados alfabéticamente
    - JSON completo con todas las propiedades

[ ] RESULTADO VISUAL
    - Archivo .blend generado
    - Render PNG de preview
    - Objeto visible y correctamente iluminado

[ ] REGLAS DE ORO APLICADAS
    - Reset de escena al inicio
    - Escala aplicada (1,1,1)
    - Modificadores en orden correcto
    - Sin objetos duplicados

[ ] DOCUMENTACIÓN
    - Descripción simple clara
    - Descripción técnica detallada
    - Uso específico identificado

═══════════════════════════════════════════════════════════════════════════
📤 FORMATO DE ENTREGA
═══════════════════════════════════════════════════════════════════════════

Para cada variación entregar:

1. 📄 SCRIPT: CUB001_v{N}.py
2. 📦 BLEND: ZULY_PROJECTS/CUB001_v{N}.blend  
3. 🖼️ RENDER: ZULY_PROJECTS/CUB001_v{N}_preview.png
4. 📋 JSON: patrones/CUB001_v{N}.json

═══════════════════════════════════════════════════════════════════════════
🏆 CRITERIOS DE PUNTUACIÓN (0-100 puntos)
═══════════════════════════════════════════════════════════════════════════

FUNCIONALIDAD:     /30  (¿Funciona en Blender?)
ESTRUCTURA:        /25  (¿JSON completo y correcto?)
VISUAL:            /25  (¿Render de calidad?)
DOCUMENTACIÓN:     /10  (¿Descripciones claras?)
VELOCIDAD:         /10  (¿Tiempo de generación?)
────────────────────────────────────────
TOTAL:            /100

═══════════════════════════════════════════════════════════════════════════
⚔️ IAs A EVALUAR
═══════════════════════════════════════════════════════════════════════════

1. Claude (Anthropic)    - [ ] Pendiente
2. GPT-4 (OpenAI)        - [ ] Pendiente  
3. DeepSeek-V3           - [ ] Pendiente
4. Gemini Pro            - [ ] Pendiente
5. Llama 3.1 (Local)     - [ ] Pendiente

═══════════════════════════════════════════════════════════════════════════
📊 TABLA DE RESULTADOS
═══════════════════════════════════════════════════════════════════════════

IA              │ v1   │ v2   │ v3   │ v4   │ v5   │ TOTAL │ RANK
────────────────┼──────┼──────┼──────┼──────┼──────┼───────┼──────
Claude          │  /30 │  /30 │  /30 │  /30 │  /30 │  /150 │  ?
GPT-4           │  /30 │  /30 │  /30 │  /30 │  /30 │  /150 │  ?
DeepSeek        │  /30 │  /30 │  /30 │  /30 │  /30 │  /150 │  ?
Gemini          │  /30 │  /30 │  /30 │  /30 │  /30 │  /150 │  ?
Llama 3.1       │  /30 │  /30 │  /30 │  /30 │  /30 │  /150 │  ?

═══════════════════════════════════════════════════════════════════════════
✍️ INSTRUCCIÓN FINAL
═══════════════════════════════════════════════════════════════════════════

Eres un agente IA participante en el benchmark ZULY.
Tu misión: Generar las 5 variaciones del patrón CUB-001.
Tu objetivo: Obtener la puntuación más alta posible.

REGLAS:
• NO generes explicaciones extensas, solo código funcional
• SÍ documenta el código con comentarios claros
• SI tienes dudas, toma la decisión más conservadora
• PRIORIDAD: Que funcione en Blender 3.6 sin errores

╔═══════════════════════════════════════════════════════════════════════════╗
║                    🚀 COMIENZA LA GENERACIÓN AHORA                         ║
╚═══════════════════════════════════════════════════════════════════════════╝
"""

# ============================================================================
# 🎯 FUNCIÓN DE EJECUCIÓN
# ============================================================================

def ejecutar_benchmark():
    """Ejecuta el benchmark completo"""
    print(EJECUCION_PROMPT)
    
    print("\n" + "="*80)
    print("INSTRUCCIONES PARA USUARIO:")
    print("="*80)
    print("""
1. Copia el prompt de arriba
2. Pégalo en cada IA que quieras probar
3. Cada IA generará 5 variaciones
4. Ejecuta los scripts en Blender uno por uno
5. Evalúa según los criterios y llena la tabla
6. La IA con mayor puntuación se integra a ZULY

ARCHIVOS QUE DEBES TENER LISTOS:
- CUB001_v1.py hasta CUB001_v5.py (por cada IA)
- CUB001_v1.blend hasta CUB001_v5.blend
- CUB001_v1_preview.png hasta CUB001_v5_preview.png
- CUB001_v1.json hasta CUB001_v5.json

TIEMPO ESTIMADO:
- Generación por IA: 10-15 minutos
- Prueba en Blender: 5 minutos por variación
- Evaluación: 2 minutos por variación
- TOTAL por IA: ~30 minutos

¿Listo para comenzar el benchmark?
    """)
    print("="*80)

if __name__ == "__main__":
    ejecutar_benchmark()
