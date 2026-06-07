# README: Organización de Scripts y Aprendizaje Inteligente

## Estructura Recomendada

- **core/**: Lógica principal, NLU, validación, ejecución de comandos.
- **scripts_blender/**: Scripts activos para Blender.
- **scripts_blender/legacy/**: Scripts antiguos, experimentales o en desuso.
- **bitacora/**: Registro de hitos y avances.
- **tests/**: Pruebas unitarias e integración.
- **docs/**: Documentación técnica y de usuario.

## Buenas Prácticas
- Centraliza la lógica de interpretación y ejecución en `core/`.
- Archiva scripts viejos en `scripts_blender/legacy/` para evitar desorden.
- Documenta cada nuevo comando o handler en los archivos `.md`.
- Usa la bitácora para registrar cada avance o aprendizaje relevante.

## Aprendizaje Inteligente
- Zuly aprende de los comandos ejecutados y los errores detectados.
- El feedback y los logs alimentan la mejora continua del parser y los handlers.
- Se recomienda implementar un módulo de retroalimentación automática para ajustar reglas y sugerencias según el historial de uso.

---

**¿Cómo seguir mejorando?**
- Automatiza el archivado de scripts obsoletos.
- Implementa un sistema de sugerencias basado en logs y feedback.
- Refuerza la modularidad para facilitar el aprendizaje incremental.
