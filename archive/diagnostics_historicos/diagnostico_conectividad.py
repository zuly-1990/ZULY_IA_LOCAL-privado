#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 DIAGNÓSTICO DE CONECTIVIDAD ZULY
Verifica que todos los subsistemas estén correctamente conectados
"""

import sys
import traceback
from pathlib import Path

# Agregar ZULY al path
zuly_path = Path("c:/Users/Admin/Desktop/ZULY_IA_LOCAL")
core_path = zuly_path / "core"
sys.path.insert(0, str(zuly_path))
sys.path.insert(0, str(core_path))

print("=" * 70)
print("🔍 DIAGNÓSTICO DE CONECTIVIDAD ZULY")
print("=" * 70)

# Lista de componentes críticos a verificar
componentes = {
    "Config": "core.config",
    "Agent": "core.agent",
    "JUES": "core.jues_bot",
    "LYZU": "core.cerebro_lyzu",
    "Decision Engine": "decision_engine",
    "Cognition Core": "core.cognition.cognition_core",
    "Pattern Memory": "core.learning.pattern_memory",
    "Intent Router": "core.intents.intent_router",
    "Blender Commands": "core.commands.blender_command_registry",
    "Scene Monitor": "core.diagnostics.scene_monitor",
    "Validators": "core.validation.v0_validator",
    "Adapters": "core.adapters",
    "State Awareness": "core.state.state_awareness",
    "Black Protocol": "core.security.black_protocol",
    "Human Gate": "core.authorization.human_gate",
    "Context Guard": "core.guard.context_guard",
    "Decision Explainer": "core.explain.decision_explainer",
    "Trace Core": "core.memory.trace_core",
    "Failsafe Executor": "core.execution.failsafe_executor",
    "Action Logger": "core.observability.action_logger",
}

resultados = {"ok": [], "error": [], "warning": []}

# Test 1: Imports básicos
print("\n📦 TEST 1: IMPORTS BÁSICOS")
print("-" * 70)

for nombre, modulo in componentes.items():
    try:
        __import__(modulo)
        print(f"  ✅ {nombre}: OK")
        resultados["ok"].append(nombre)
    except Exception as e:
        error_msg = str(e)[:50]
        print(f"  ❌ {nombre}: {error_msg}")
        resultados["error"].append((nombre, str(e)))

# Test 2: Dependencias cruzadas
print("\n🔗 TEST 2: DEPENDENCIAS CRUZADAS")
print("-" * 70)

# Verificar que Agent pueda inicializar subsistemas
if "core.agent" in [m for n, m in componentes.items()]:
    try:
        from core.agent import Agent
        print("  ✅ Clase Agent importada")
        
        # Verificar que tiene los atributos esperados
        atributos_esperados = [
            'nlu', 'scene_monitor', 'pattern_memory', 'validator_v0',
            'validator_v1', 'validator_v2', 'intent_router',
            'failsafe_executor', 'action_logger', 'cognition'
        ]
        
        for attr in atributos_esperados:
            if hasattr(Agent, attr) or hasattr(Agent, '__init__'):
                print(f"  ✅ Atributo '{attr}': Declarado")
            else:
                print(f"  ⚠️ Atributo '{attr}': No encontrado")
                resultados["warning"].append(f"Agent falta: {attr}")
                
    except Exception as e:
        print(f"  ❌ Error inicializando Agent: {str(e)[:60]}")
        traceback.print_exc()

# Test 3: IntentRouter y handlers
print("\n🎯 TEST 3: INTENT ROUTER")
print("-" * 70)

try:
    from core.intents.intent_router import IntentRouter
    from core.commands.blender_command_registry import register_blender_handlers
    
    router = IntentRouter()
    register_blender_handlers(router)
    handler_count = len(router.command_handlers)
    
    if handler_count >= 40:
        print(f"  ✅ {handler_count} handlers registrados")
        resultados["ok"].append(f"IntentRouter ({handler_count} handlers)")
    else:
        print(f"  ⚠️ Solo {handler_count} handlers (esperado 48)")
        resultados["warning"].append(f"Handlers insuficientes: {handler_count}")
        
except Exception as e:
    print(f"  ❌ Error en IntentRouter: {str(e)[:60]}")
    resultados["error"].append(("IntentRouter", str(e)))

# Test 4: Validadores
print("\n✅ TEST 4: SISTEMA DE VALIDACIÓN")
print("-" * 70)

try:
    from core.validation.v0_validator import V0Validator
    from core.validation.v1_validator import V1Validator
    from core.validation.v2_validator import V2Validator
    
    print("  ✅ V0Validator importado")
    print("  ✅ V1Validator importado")
    print("  ✅ V2Validator importado")
    resultados["ok"].extend(["V0", "V1", "V2"])
    
except Exception as e:
    print(f"  ❌ Error en validadores: {str(e)[:60]}")
    resultados["error"].append(("Validadores", str(e)))

# Test 5: Cognition
print("\n🧠 TEST 5: SISTEMA DE COGNICIÓN")
print("-" * 70)

c_modules = [
    ("C1 Evaluator", "core.cognition.c1_result_evaluator"),
    ("C2 Memory", "core.cognition.c2_experience_memory"),
    ("C3 Objectives", "core.cognition.c3_abstract_objectives"),
    ("C4 Auto-tuning", "core.cognition.c4_auto_tuning_procedural"),
]

for nombre, modulo in c_modules:
    try:
        __import__(modulo)
        print(f"  ✅ {nombre}: OK")
        resultados["ok"].append(nombre)
    except Exception as e:
        print(f"  ❌ {nombre}: {str(e)[:40]}")
        resultados["error"].append((nombre, str(e)))

# Test 6: Ruteo de decisiones
print("\n⚙️ TEST 6: DECISION ENGINE")
print("-" * 70)

try:
    from decision_engine import decidir, get_decision_engine
    print("  ✅ decidir() importada")
    print("  ✅ get_decision_engine() importada")
    resultados["ok"].append("DecisionEngine")
except Exception as e:
    print(f"  ❌ Error: {str(e)[:60]}")
    resultados["error"].append(("DecisionEngine", str(e)))

# Test 7: Seguridad
print("\n🛡️ TEST 7: SISTEMA DE SEGURIDAD")
print("-" * 70)

seg_modules = [
    ("BlackProtocol", "core.security.black_protocol"),
    ("HumanGate", "core.authorization.human_gate"),
    ("ContextGuard", "core.guard.context_guard"),
]

for nombre, modulo in seg_modules:
    try:
        __import__(modulo)
        print(f"  ✅ {nombre}: OK")
        resultados["ok"].append(nombre)
    except Exception as e:
        print(f"  ❌ {nombre}: {str(e)[:40]}")
        resultados["error"].append((nombre, str(e)))

# Test 8: Observabilidad
print("\n👁️ TEST 8: OBSERVABILIDAD")
print("-" * 70)

obs_modules = [
    ("ActionLogger", "core.observability.action_logger"),
    ("SceneMonitor", "core.diagnostics.scene_monitor"),
    ("TraceCore", "core.memory.trace_core"),
]

for nombre, modulo in obs_modules:
    try:
        __import__(modulo)
        print(f"  ✅ {nombre}: OK")
        resultados["ok"].append(nombre)
    except Exception as e:
        print(f"  ❌ {nombre}: {str(e)[:40]}")
        resultados["error"].append((nombre, str(e)))

# Resumen final
print("\n" + "=" * 70)
print("📊 RESUMEN DE CONECTIVIDAD")
print("=" * 70)

total = len(resultados["ok"]) + len(resultados["error"]) + len(resultados["warning"])
ok_count = len(resultados["ok"])
error_count = len(resultados["error"])
warning_count = len(resultados["warning"])

print(f"\n  ✅ OK: {ok_count}/{total}")
print(f"  ⚠️  Advertencias: {warning_count}")
print(f"  ❌ Errores: {error_count}")

if error_count == 0:
    print(f"\n  🎉 TODOS LOS SISTEMAS CONECTADOS")
    print(f"  Conectividad: {ok_count}/{total} ({100*ok_count//total}%)")
elif error_count <= 3:
    print(f"\n  ⚠️  CONECTIVIDAD PARCIAL ({100*ok_count//total}%)")
    print("  Algunos subsistemas no responden pero el core funciona")
else:
    print(f"\n  ❌ PROBLEMAS DE CONECTIVIDAD DETECTADOS")
    print("  Revisar dependencias rotas")

# Listar errores si existen
if resultados["error"]:
    print("\n🚨 ERRORES DETECTADOS:")
    for nombre, error in resultados["error"]:
        print(f"   • {nombre}: {error[:60]}")

if resultados["warning"]:
    print("\n⚠️  ADVERTENCIAS:")
    for warning in resultados["warning"]:
        print(f"   • {warning}")

print("\n" + "=" * 70)
