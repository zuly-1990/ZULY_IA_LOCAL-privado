# PLAN DE TRABAJO – ZULY (FASE ACTIVA)

## 🎯 OBJETIVO DE ESTA FASE
Construir el núcleo de diálogo generalizado de Zuly, capaz de:
- Interpretar órdenes simples en lenguaje natural
- Extraer intención + parámetros
- Ejecutar primitivas básicas en Blender
- Registrar todo en bitácora

## 🧩 FASE 1 – Diálogo Generalizado (ACTIVA)
### Alcance
Zuly debe entender órdenes como:
- "crea un cubo"
- "crea un cubo rojo"
- "crea una esfera grande"
- "crea un plano como piso"
- "agrega un mono de prueba"
- "crea 3 cubos"
(No materiales complejos, no escenas cinematográficas aún)

### Archivos a trabajar (en este orden)
1. core/dialog.py
2. core/commands/blender_commands.py
3. core/diagnostics/diagnostics.py
4. bitacora/resúmenes/dialogo_fase_1.md

### Principios
- Validar todo
- Nada automático sin validación
- Todo explicable y reversible
- Todo registrado

### Criterios de parada
- Zuly ejecuta órdenes simples correctamente
- Responde con advertencia si algo no se entiende
- Todo queda registrado

---

Cada vez que alcancemos un hito, lo documentamos en la bitácora.
