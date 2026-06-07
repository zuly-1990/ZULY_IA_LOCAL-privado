import sys
import os
import importlib.util

def check_module(module_name, file_path):
    print(f"🔍 Verificando integridad de: {module_name}...")
    if not os.path.exists(file_path):
        print(f"❌ ARCHIVO NO ENCONTRADO: {file_path}")
        return None
    
    try:
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        print(f"✅ SINTAXIS CORRECTA: {module_name} se cargó bien.")
        return module
    except SyntaxError as e:
        print(f"🚨 ERROR CRÍTICO DE SINTAXIS en {file_path}:")
        print(f"   Línea {e.lineno}: {e.text.strip() if e.text else '?'}")
        print(f"   Error: {e.msg}")
        print("   -> (Probable corte por caída de red)")
        return None
    except Exception as e:
        print(f"⚠️ Error general importando {module_name}: {e}")
        return None

print("╔════════════════════════════════════════════╗")
print("║   DIAGNÓSTICO DE RECUPERACIÓN - ZULY       ║")
print("╚════════════════════════════════════════════╝")
print("")

# 1. Verificar Core Handlers
lyzu = check_module("lyzu_core", "lyzu_core.py")
if lyzu:
    expected_handlers = ["create_cube", "create_sphere", "move_object", "rotate_object", "scale_object"]
    print("   🛠️  Comprobando conectores de funciones:")
    for h in expected_handlers:
        if hasattr(lyzu, h):
            print(f"      OK: {h} existe.")
        else:
            print(f"      ⚠️ ALERTA: La función '{h}' no se encuentra (¿archivo incompleto?).")

# 2. Verificar CLI Parser
cli = check_module("zuly_cli_interactive", "zuly_cli_interactive.py")
if cli:
    print("   🔌 Comprobando Mapas de Acción (ACTION_MAP):")
    if hasattr(cli, 'ACTION_MAP'):
        print(f"      ✅ ACTION_MAP detectado con {len(cli.ACTION_MAP)} comandos mapeados.")
    else:
        print("      ⚠️ ALERTA: No se encuentra 'ACTION_MAP'. El CLI no funcionará.")

print("\n🏁 Diagnóstico finalizado.")