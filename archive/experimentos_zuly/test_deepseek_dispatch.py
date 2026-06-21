import sys, json, os
sys.path.insert(0, '/opt/zuly')

from core.navigation.zuly_nav import ZulyNav

print("=" * 60)
print("  📡 ZULY NAV - DESPACHO A DEEPSEEK")
print("=" * 60)

nav = ZulyNav()

# Verificamos si la key está en el entorno
api_key = os.environ.get("DEEPSEEK_API_KEY")
if not api_key:
    print("⚠️ ADVERTENCIA: DEEPSEEK_API_KEY no encontrada en las variables de entorno.")
    print("Se intentará hacer la petición de todos modos por si está configurada en otro lado...")

print("Enviando contexto espacial de la Villa Savoye a DeepSeek...")
print("Analizando escalera helicoidal y centro de masa...")

resultado = nav.nav_dispatch(
    agente="deepseek",
    contexto="villa_savoye",
    modo="completo"
)

print("\n--- RESPUESTA DE DEEPSEEK ---")
if resultado.get("success"):
    resp = resultado.get("respuesta", {})
    if isinstance(resp, dict):
        print(json.dumps(resp, indent=2, ensure_ascii=False))
    else:
        print(resp)
else:
    print("❌ ERROR en el despacho:")
    print(resultado)

print("=" * 60)
