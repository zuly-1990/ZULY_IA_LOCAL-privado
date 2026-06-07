# Manuales ZULY

Documentación y guías de uso del sistema ZULY.

## 📚 Manual Actual

### [MANUAL_USO_ZULY_2026.md](MANUAL_USO_ZULY_2026.md)
**Versión**: 2.0 - Febrero 2026  
**Estado**: ✅ Activo y actualizado

**Contenido**:
- Ubicación del Blender local (`blender/v3/blender-3.6.0-zuly/`)
- 29 comandos disponibles con ejemplos
- Guías de uso paso a paso
- Arquitectura del sistema
- Solución de problemas
- Scripts de verificación

**Úsalo si**: Estás empezando con ZULY o necesitas referencia de comandos

---

## 🗂️ Manuales Anteriores

### [MANUAL_VIEJO_AGENTE_IA.md](MANUAL_VIEJO_AGENTE_IA.md)
**Versión**: 1.0 - 2025/2026  
**Estado**: ⚠️ Archivado - contenido desactualizado

**Nota**: Este manual describe el sistema antiguo con comandos en formato de clases. El sistema actual usa IntentRouter con handlers funcionales.

**Úsalo si**: Necesitas entender la evolución del sistema o migrar código antiguo

---

## 🚀 Inicio Rápido

Para empezar inmediatamente:

1. **Ejecutar prueba rápida**:
   ```powershell
   cd C:\Users\Admin\Desktop\ZULY_IA_LOCAL
   .\run_zuly_blender_real.ps1
   ```

2. **Manual completo**:
   Abre [`MANUAL_USO_ZULY_2026.md`](MANUAL_USO_ZULY_2026.md)

3. **Verificar sistema**:
   ```python
   from core.agent import Agent
   agent = Agent(force_mock=True)
   print(f"Handlers: {len(agent.intent_router.command_handlers)}")
   ```

---

## 📂 Estructura de Carpeta

```
manuales/
├── README.md                      # Este archivo
├── MANUAL_USO_ZULY_2026.md       # ✅ Manual actual
└── MANUAL_VIEJO_AGENTE_IA.md     # ⚠️  Archivado
```

---

## 📞 ¿Necesitas ayuda?

- **Manual principal**: [`MANUAL_USO_ZULY_2026.md`](MANUAL_USO_ZULY_2026.md)
- **Walkthrough técnico**: `../brain/.../walkthrough.md`
- **Bitácora**: `../bitacora/`
- **Logs**: `../bitacora/zuly_agent.log`

---

**Última actualización**: 2026-02-14
