# DESCRIPTORES PROCEDURALES: Geometry Nodes y Sistemas No Ejecutables

**Fecha de Creación:** 31 de Diciembre de 2025
**Estado:** Activo - Fase 5.9

## 1. Definición

Los **Descriptores Procedurales** son entidades reconocidas por el sistema Zuly que representan sistemas lógicos complejos (como Geometry Nodes en Blender) pero que **NO son ejecutables directamente** por el agente en su estado actual.

Se clasifican bajo el tipo: `DESCRIPTOR`
Estado de Ejecución: `BLOQUEADA`

## 2. Propósito y Filosofía

Zuly prioriza la **integridad estructural y la seguridad determinista**. Los sistemas procedurales, por su naturaleza, son:
- **Abstractos:** "Distribuir puntos" no significa nada sin una geometría base concreta.
- **Dependientes de Contexto:** Requieren flujos de datos (inputs/outputs) que no pueden inferirse de una sola frase.
- **Riesgo de Densidad:** Un mal parámetro puede generar millones de vértices y colgar el sistema.

Por tanto, Zuly adopta una postura de **Observador Informado**:
1.  **Reconoce** que se está hablando de Geometry Nodes.
2.  **Entiende** los conceptos clave (instancias, campos, nodos).
3.  **Bloquea** la ejecución para evitar "alucinaciones procedurales" o acciones destructivas.
4.  **Informa** al usuario con lenguaje neutro que se requiere una definición explícita.

## 3. Implementación Técnica

### Diccionario Atómico (`core/knowledge/atomic_dictionary.py`)
Nueva categoría `procedural_descriptors` que contiene `GEOMETRY_NODES_CONCEPTO`. Este diccionario actúa como la fuente de verdad.

### Evaluador (`core/utils/transcription_evaluator.py`)
Escanea las transcripciones en busca de keywords definidas en el diccionario. Si encuentra términos como "geometry nodes", "procedural", o "instancias", inyecta un objeto `detected_concepts` en el reporte de evaluación.

### Gestor de Diálogo (`core/dialog.py`)
Antes de aprobar cualquier ejecución, verifica si el reporte de evaluación contiene conceptos bloqueados. Si es así, rechaza la intención con el mensaje:

> "Detectado sistema procedural (Geometry Nodes). Concepto registrado como descriptivo. Se requiere definición explícita de geometría base y objetivo."

## 4. Evolución Futura

Esta estructura prepara el terreno para:
- **Fase 6 (Futura):** Generación segura de árboles de nodos básicos.
- **Validación de Inputs:** Permitir proceduralismo solo si se definen explícitamente los inputs (objeto, count, seed).
