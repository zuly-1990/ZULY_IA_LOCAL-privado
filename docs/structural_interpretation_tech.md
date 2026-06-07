# Documentación Técnica: Interpretación Estructural Zuly

## Flujo de Trabajo (Pipeline)
Zuly procesa la información en capas para garantizar robustez y evitar ejecuciones accidentales:

1.  **Texto Plano**: Entrada del usuario (tutorial, transcripción, descripción).
2.  **Fase de Interpretación (StructuralInterpreter)**:
    *   **Determinista**: Identificación de primitivas y roles basados en el `Atomic Dictionary`.
    *   **Heurística**: Extracción de parámetros y relaciones espaciales mediante Regex (aislado para futura sustitución por IA).
3.  **Mapa Estructural (JSON)**: Generación del esquema v1.1.1 que contiene elementos, parámetros y relaciones lógicas.
4.  **Validación Estructural (StructuralValidator)**:
    *   Detección de inconsistencias (objetos inexistentes en relaciones).
    *   Detección de incoherencias (objetos con roles sin propósito claro).
5.  **Capa Dialog (Futuro)**: Notificación de parámetros faltantes o advertencias.
6.  **Capa Blender (Fase 6)**: Ejecución final solo si `executable` es True (actualmente bloqueado en Fase 5).

## Estado Actual (Qué hace Zuly hoy)
*   ✅ Identifica 6 primitivas geométricas básicas.
*   ✅ Detecta roles explícitos (base, soporte, etc.).
*   ✅ Extrae coordenadas y medidas numéricas.
*   ✅ Detecta relaciones lógicas (encima de, debajo de, alineado con).
*   ✅ Valida la integridad de la estructura sin tocar Blender.

## Lo que Zuly NO hace todavía
*   ❌ No infiere valores que no están en el texto.
*   ❌ No resuelve ambigüedades sin preguntar (vía `missing_parameters`).
*   ❌ No valida colisiones físicas o gravedad.
*   ❌ No ejecuta código `bpy` durante la interpretación.

## Diseño para el Futuro: Interfaz Semántica
Se ha implementado `parser_interface.py` para que, cuando se integren modelos de lenguaje avanzados, solo sea necesario implementar una nueva clase que herede de `BaseSemanticParser`, manteniendo el resto de la arquitectura intacta.
