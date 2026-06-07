# SESIÓN: 2026-03-01 - FIN DE SEMANA 3: VALIDACIÓN V1 PROFUNDA

## OBJETIVOS
- Implementar Validador V1 para chequeos estructurales profundos.
- Capturar jerarquías y métricas geométricas (vértices) en snapshots.
- Integrar cadena de validación V0 -> V1 en el Agente ZULY.

## IMPLEMENTACIÓN

### Componentes Actualizados
- **`BlenderAdapter` / `MockAdapter`**: Ahora retornan `parent` y `vertex_count` en `get_scene_state()`.
- **`StateSnapshot`**: Captura los nuevos campos estructurales.
- **`V1Validator`**: Nuevo módulo que compara tipos de objetos, jerarquías y conteo de vértices.
- **`Agent`**: Encadena V0 y V1. Reporta errores estructurales incluso si el comando fue exitoso en el motor.

### Pipeline de Validación
1. **Ejecución**: El comando se envía al motor (Blender).
2. **Nivel V0**: Verifica existencia física (¿hay algo nuevo?).
3. **Nivel V1**: Verifica integridad estructural (¿es lo que pedimos?).

---

## VERIFICACIÓN EXITOSA ✅
- Suite de tests: `tests/test_v1_validator_weekend3.py`.
- **Tests Unitarios**: Confirmado que detecta mismatches de tipo y de jerarquía.
- **Tests de Integridad**: Confirmado que detecta cambios anómalos en geometría (vértices).
- **Tests de Integración**: Confirmado que el Agente ZULY procesa la cadena completa V0 -> V1.
- **Resultado final**: 6/6 tests pasados.

## DECISIONES CLAVE
- **V1 no es mortal, pero sí bloqueante**: Si V1 falla, la ejecución se marca como fallida en la respuesta final de ZULY, permitiendo al usuario decidir si hace rollback.
- **Rutas Estandarizadas**: Se alineó el sistema para usar `ZULY_PROJECTS/` como ruta por defecto para archivos `.blend`, cumpliendo con el estándar del manual.
- **Snapshot compartido**: Se optimizó la captura de snapshots para que V1 use los mismos datos que V0, minimizando la latencia.

## PRÓXIMOS PASOS
1. Usuario verificará manualmente los archivos `.blend` resultantes.
2. Preparar para el Fin de Semana 4: Validación V2 (Semántica/Lógica).
