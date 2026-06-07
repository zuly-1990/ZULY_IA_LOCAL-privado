# ZULY - Código Único: Ejemplo demostrativo

## SIN código único (actual)

```
[AUDIT] ZULY System Status
  Patrones: 0
  Handlers: 25
  Engine: v20_STABLE
  Status: Operational
```

Problema: ¿Cuál ZULY es este? ¿El de hoy? ¿El de ayer?

---

## CON código único - Opción 1: UUID

```
[ZULY-ID] 550e8400-e29b-41d4-a716-446655440000
[AUDIT] ZULY System Status
  Patrones: 0
  Handlers: 25
  Engine: v20_STABLE
  Status: Operational
```

✅ Ventaja: Universal, nunca se repite
❌ Desventaja: Poco legible, sin semántica

---

## CON código único - Opción 2: Firma de Versión (RECOMENDADO)

```
[ZULY-ID] ZULY-v20-25h-20260329
  • v20 = Engine version
  • 25h = 25 handlers
  • 20260329 = Fecha creación

[AUDIT] ZULY System Status
  ID: ZULY-v20-25h-20260329
  Patrones: 0
  Handlers: 25
  Engine: v20_STABLE
  Status: Operational
```

✅ Ventajas: 
- Legible
- Contiene info semántica
- Log automático de configuración
- Fácil de rastrear cambios

---

## Uso en archivos .blend

### SIN ID
```json
{
  "engine_version": "v20_STABLE",
  "atom_size_mm": 0.137,
  "mass_kg": 2.4
}
```

### CON ID
```json
{
  "zuly_id": "ZULY-v20-25h-20260329",
  "engine_version": "v20_STABLE",
  "atom_size_mm": 0.137,
  "mass_kg": 2.4,
  "created_by": "ZULY-v20-25h-20260329"
}
```

---

## Uso en bitácora

### SIN ID
```
2026-03-29 14:30:45 | Created uno.blend
2026-03-29 14:31:12 | Created pattern variant
2026-03-29 14:31:55 | Audit completed
```

### CON ID
```
2026-03-29 14:30:45 | [ZULY-v20-25h-20260329] Created uno.blend
2026-03-29 14:31:12 | [ZULY-v20-25h-20260329] Created pattern variant
2026-03-29 14:31:55 | [ZULY-v20-25h-20260329] Audit completed
```

Beneficio: Cambios futuros → ZULY-v20-26h (agregó 1 handler)

---

## ¿Es mejor? Análisis

| Aspecto | SIN ID | CON ID |
|---------|--------|--------|
| Rastreabilidad | ❌ Difícil | ✅ Fácil |
| Auditoría | ⚠️ Parcial | ✅ Completa |
| Debugging | ❌ Confuso | ✅ Claro |
| Reproducibilidad | ❌ No | ✅ Sí |
| Overhead | ✅ Bajo | ✅ Muy bajo |
| Mantenimiento | ✅ Bajo | ⚠️ Mínimo |

---

## Conclusión

**RECOMENDACIÓN: SÍ implementar**

Razón: Permite rastrear exactamente qué versión de ZULY creó cada artefacto (uno.blend, registros, etc.). Facilita debugging cuando cambia la arquitectura.

Formato sugerido: `ZULY-v{engine}-{handlers}h-{YYYYMMDD}`

Ejemplo: `ZULY-v20-25h-20260329`
