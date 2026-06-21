# ZULY_IA_LOCAL

Agente IA para Blender con auto-mejora multi-IA.

## ¿Qué es ZULY?
Sistema agente que recibe órdenes en lenguaje natural (español/inglés)
y las convierte en acciones 3D reales dentro de Blender.

## Arquitectura
- `core/` — Cerebro: cognition, learning, execution, environment, security
- `tools/` — Interfaces: CLI, QA runner, batch JUES, lab
- `bitacora/` — Bases de datos SQLite y logs
- `patterns/` — ADN arquitectónico aprendido
- `archive/` — Histórico de scripts de desarrollo

## Estado actual
Fase 3 — Despliegue en nube completado

**Infraestructura:**
- ✅ Git inicializado y conectado a GitHub
- ✅ Dockerfile creado
- ✅ GitHub Actions CI configurado
- ✅ VM Hetzner (ubuntu-4gb-fsn1-1) desplegada
- ✅ Blender 3.6 instalado en VM
- ✅ ZULY ejecutándose en VM con cron job (cada 6 horas)

**Resultados de pruebas (VM Hetzner):**
- Critical pass rate: 100.0% (9/9)
- High pass rate: 100.0% (4/4)
- Overall OK: True
- Archivo .blend generado: prueba_final_zuly_qa_runner.blend

## Roadmap
1. ✅ Estructura limpia y git inicializado
2. ✅ Suite de pruebas básicas pasando al 100%
3. ✅ Docker + Hetzner + GitHub Actions
4. ⬜ Gemini API como revisor automático
5. ⬜ Ciclo autónomo completo

## Author
Signature WO-002
