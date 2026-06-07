# Paradigmas Evolutivos de Blender

**Implementación:** Fase 5.12
**Objetivo:** Abstracción conceptual de la versión de software.

## ¿Por qué Paradigmas y no Versiones?
Blender evoluciona rápidamente. Un script escrito para Blender 2.8 puede no funcionar en 4.0 debido a cambios en la API, pero el **concepto** sigue siendo el mismo. Zuly se diseñó para aprender conceptos, no sintaxis efímera.

Al clasificar instrucciones por **Paradigma**, Zuly se desvincula de la "versión" y se enfoca en el "modo de operación".

## Clasificación de Paradigmas

### 1. PARADIGM_IMPERATIVE (Legacy)
*   **Descripción:** Acciones directas y destructivas. "Mover cubo", "Escalar", "Aplicar rotación".
*   **Compatibilidad:** Total (Legacy).
*   **Uso:** Instrucciones básicas y manipulación de viewport.

### 2. PARADIGM_MODULAR (Supported)
*   **Descripción:** Uso de modificadores no destructivos en stack.
*   **Compatibilidad:** Soportada.
*   **Uso:** Modelado procedural clásico (Mirror, Array, Subdivision).

### 3. PARADIGM_DECLARATIVE (Requiere Adaptación)
*   **Descripción:** Definición de *qué* se quiere lograr mediante flujos de datos, sin especificar el paso a paso imperativo.
*   **Ejemplos:** Geometry Nodes (Fields), Shader Nodes.
*   **Estado:** **BLOQUEADO POR DEFECTO**. Requiere que Zuly interprete la intención y construya el grafo nodal internamente, en lugar de intentar ejecutar comandos paso a paso.

### 4. PARADIGM_PROCEDURAL_EVALUATED (No Ejecutable)
*   **Descripción:** Sistemas de simulación en tiempo real, GPU driven, Physics Nodes.
*   **Estado:** Observación pura. Zuly puede narrar lo que sucede pero no tiene permiso de intervención.

## Estrategia de Supervivencia
Si Blender 5.0 cambia toda la API de Python:
1.  Los paradigmas conceptuales (Imperativo, Declarativo) se mantienen.
2.  Solo se necesita actualizar el *adaptador* de ejecución del paradigma.
3.  La lógica de razonamiento de Zuly permanece intacta.
