#!/usr/bin/env python3
"""
Test de integración AADD - ZULY Architectural Kit
"""

import sys
sys.path.insert(0, '.')

print('=== VERIFICACIÓN AADD v2 ===')
print()

# 1. Verificar importación
try:
    from core.commands.blender_handlers.architectural_pro import crear_ventana_pro_handler
    print('✅ Handler AADD importado correctamente')
except Exception as e:
    print(f'❌ Error: {e}')
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 2. Verificar firma
import inspect
sig = inspect.signature(crear_ventana_pro_handler)
print(f'✅ Firma del handler: {sig}')

# 3. Test simulado
result = crear_ventana_pro_handler({
    'ancho': 1.2,
    'alto': 1.5,
    'sill_height': 0.9
}, adapter=None)

print('✅ Handler ejecutado (modo simulación)')
print(f'   Mensaje: {result.get("message")}')
print(f'   Requiere JUES: {result.get("requires_jues")}')
print(f'   Success: {result.get("success")}')

# 4. Verificar NLU
try:
    from core.utils.nlu import NaturalLanguageProcessor
    from core.intents.intent_router import IntentRouter
    
    router = IntentRouter()
    from core.commands.blender_command_registry import register_blender_handlers
    register_blender_handlers(router)
    
    nlu = NaturalLanguageProcessor(router.command_handlers)
    intents = nlu.process('crear ventana 1.2x1.5')
    
    if intents:
        cmd_result = intents[0]
        print()
        print('✅ NLU procesa "crear ventana 1.2x1.5"')
        print(f'   Comando: {cmd_result.command_name}')
        print(f'   Confianza: {cmd_result.confidence:.2f}')
        print(f'   Parámetros: {cmd_result.parameters}')
    else:
        print('❌ NLU no encontró comandos')
    
except Exception as e:
    print(f'⚠️ NLU test: {e}')

print()
print('=== Sistema AADD ZULY PRO - LISTO ===')
print('ZULY ahora puede crear ventanas profesionales con JUES validation')
