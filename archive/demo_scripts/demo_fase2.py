#!/usr/bin/env python3
"""Demo: LYZU Core con Handlers y Límite de Memoria"""

from lyzu_core import LYZUCore
import time

print("\n" + "=" * 70)
print("DEMO: LYZU Core 1.0 - Handlers + Memory Limit")
print("=" * 70 + "\n")

# 1. Inicializar
print("1. Inicializando LYZU Core...")
lyzu = LYZUCore(mode='reactive')
print()

# 2. Procesar comandos
commands = [
    "Crea un cubo",
    "Crea una esfera roja",
    "Renderiza",
    "Mueve el objeto",
    "Info del sistema",
]

print("2. Procesando comandos...")
print("-" * 70)

for i, cmd in enumerate(commands, 1):
    result = lyzu.process_user_input(cmd)
    print(f"\n{i}. Input: '{cmd}'")
    print(f"   Intent: {result.get('intent', 'N/A')}")
    print(f"   Confidence: {result.get('confidence', 0):.1%}")
    print(f"   Time: {result.get('execution_time_ms', 0):.1f}ms")

# 3. Mostrar estadísticas de memoria
print("\n" + "=" * 70)
print("3. MEMORY STATISTICS")
print("=" * 70)

stats = lyzu.memory.get_memory_stats()
print(f"\n  Turnos en memoria: {stats['turns_in_memory']}/{stats['max_turns']}")
print(f"  Archivados: {stats['archived_turns']}")
print(f"  Total procesados: {stats['total_turns_processed']}")
print(f"  Uso de memoria: {stats['memory_usage_pct']:.1f}%")

# 4. Mostrar handlers registrados
print("\n" + "=" * 70)
print("4. HANDLERS REGISTRADOS")
print("=" * 70)

handlers = lyzu.intent_router.get_handler_list()
print(f"\nTotal handlers: {len(handlers)}\n")

handler_list = list(handlers.items())
for i, (name, _) in enumerate(handler_list[:8], 1):
    print(f"  {i:2d}. {name}")

if len(handler_list) > 8:
    print(f"\n  ... ({len(handler_list) - 8} más)")

# 5. Guardar sesión
print("\n" + "=" * 70)
print("5. GUARDANDO SESIÓN")
print("=" * 70)

session_path = lyzu.save_session()
print(f"\n  ✓ Sesión guardada en: {session_path}")

# 6. Contexto final
context = lyzu.get_context_summary()
print("\n" + "=" * 70)
print("6. CONTEXTO FINAL")
print("=" * 70)

print(f"\n  Session ID: {context['session_id']}")
print(f"  Turnos: {context['turns_count']}")
print(f"  Modo: {context['mode']}")

print("\n" + "=" * 70)
print("✅ DEMO COMPLETADO - FASE 2 LISTA")
print("=" * 70 + "\n")
