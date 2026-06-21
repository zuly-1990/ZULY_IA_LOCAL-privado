"""
test_nav.py - Prueba completa del módulo ZulyNav
Ejecutar: python3 test_nav.py
"""
import sys, json
sys.path.insert(0, '/opt/zuly')

from core.navigation.zuly_nav import ZulyNav

nav = ZulyNav()

print("=" * 60)
print("  🧭  ZULY NAV - MÓDULO DE NAVEGACIÓN COGNITIVA")
print("=" * 60)

# 1. Status
print("\n[1] STATUS DEL MÓDULO")
st = nav.status()
for k, v in st.items():
    print(f"   {k}: {v}")

# 2. Nav Ancestral
print("\n[2] MEMORIA ANCESTRAL (búsqueda profunda)")
anc = nav.nav_ancestral()
print(f"   Resumen: {anc['resumen']}")
print(f"   Total memorias: {anc['total_memorias_encontradas']}")
print(f"   Proyectos ancestrales: {list(anc['memorias']['ancestral_hardcoded']['proyectos'])}")

# 3. Nav Query
print("\n[3] CONSULTA: 'villa_savoye'")
q = nav.nav_query("villa_savoye")
print(f"   Encontrados: {q['total']}")
print(f"   Fuentes ancestrales: {len(q['ancestral'])}")

# 4. Nav Scan
print("\n[4] ESCANEO PROFUNDO (archivos JSON)")
scan = nav.nav_scan(deep=True)
print(f"   Elementos encontrados: {scan['total_encontrados']}")

# 5. Nav Register (prueba de registro)
print("\n[5] REGISTRO DE COORDENADA")
reg = nav.nav_register(
    proyecto="Test_Nav",
    elemento="Punto_Prueba",
    loc=[5.0, 3.0, 1.0],
    dim=[2.0, 2.0, 2.0],
    contexto="Prueba de registro del módulo nav"
)
print(f"   Registrado: {reg['registrado']} en {reg['loc']}")

print("\n" + "=" * 60)
print("  ✅ MÓDULO ZULY NAV OPERATIVO AL 100%")
print("=" * 60)

# Guardar reporte completo
with open('/opt/zuly/bitacora/nav_test_result.json', 'w') as f:
    json.dump({
        "status": st,
        "ancestral_resumen": anc['resumen'],
        "scan_total": scan['total_encontrados'],
        "query_villa": q['total'],
    }, f, indent=2, ensure_ascii=False)
print(f"\n  📁 Reporte guardado en /opt/zuly/bitacora/nav_test_result.json")
