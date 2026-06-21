"""
PRUEBA MAESTRA: Villa Savoye - Copia Exacta al 1000%
=====================================================
Medidas históricas reales:
 - Planta baja: 20m x 20m (pilotes de 0.3m diámetro, h=3.5m)
 - Primer nivel: 19.2m x 19.2m (el volumen principal blanco)
 - Techo-jardín: 11.5m x 11.5m (terraza con rampa helicoidal)
 - Ventanas longitudinales corridas (fenêtre en longueur)
 - Rampa central de 0.9m x 5m por nivel
 - Orientación: Norte-Sur
Fuente: Le Corbusier, 1929. Poissy, Francia.
"""

import sys
import time
sys.path.insert(0, '/opt/zuly')

from core.agent import Agent

# ============================================================
# PLAN HARD-CODED: No depende de DeepSeek, es una partitura
# arquitectónica fija basada en medidas reales de la Villa Savoye
# ============================================================
VILLA_SAVOYE_PLAN = [
    # --- PILOTES (Planta libre) ---
    # 5 columnas en fila x 5 columnas = 14 perimetrales + 1 central
    # Espaciado: 4.75m en X, 4.75m en Y. Centro de la cuadrícula.
    {"command_name": "blender.create_cube", "parameters": {"name": "Pilote_A1", "size": [0.3, 0.3, 3.5], "location": [-9.5, -9.5, 1.75]}},
    {"command_name": "blender.create_cube", "parameters": {"name": "Pilote_A2", "size": [0.3, 0.3, 3.5], "location": [-4.75, -9.5, 1.75]}},
    {"command_name": "blender.create_cube", "parameters": {"name": "Pilote_A3", "size": [0.3, 0.3, 3.5], "location": [0, -9.5, 1.75]}},
    {"command_name": "blender.create_cube", "parameters": {"name": "Pilote_A4", "size": [0.3, 0.3, 3.5], "location": [4.75, -9.5, 1.75]}},
    {"command_name": "blender.create_cube", "parameters": {"name": "Pilote_A5", "size": [0.3, 0.3, 3.5], "location": [9.5, -9.5, 1.75]}},
    {"command_name": "blender.create_cube", "parameters": {"name": "Pilote_B1", "size": [0.3, 0.3, 3.5], "location": [-9.5, -4.75, 1.75]}},
    {"command_name": "blender.create_cube", "parameters": {"name": "Pilote_B5", "size": [0.3, 0.3, 3.5], "location": [9.5, -4.75, 1.75]}},
    {"command_name": "blender.create_cube", "parameters": {"name": "Pilote_C1", "size": [0.3, 0.3, 3.5], "location": [-9.5, 0, 1.75]}},
    {"command_name": "blender.create_cube", "parameters": {"name": "Pilote_C5", "size": [0.3, 0.3, 3.5], "location": [9.5, 0, 1.75]}},
    {"command_name": "blender.create_cube", "parameters": {"name": "Pilote_D1", "size": [0.3, 0.3, 3.5], "location": [-9.5, 4.75, 1.75]}},
    {"command_name": "blender.create_cube", "parameters": {"name": "Pilote_D5", "size": [0.3, 0.3, 3.5], "location": [9.5, 4.75, 1.75]}},
    {"command_name": "blender.create_cube", "parameters": {"name": "Pilote_E1", "size": [0.3, 0.3, 3.5], "location": [-9.5, 9.5, 1.75]}},
    {"command_name": "blender.create_cube", "parameters": {"name": "Pilote_E2", "size": [0.3, 0.3, 3.5], "location": [-4.75, 9.5, 1.75]}},
    {"command_name": "blender.create_cube", "parameters": {"name": "Pilote_E3", "size": [0.3, 0.3, 3.5], "location": [0, 9.5, 1.75]}},
    {"command_name": "blender.create_cube", "parameters": {"name": "Pilote_E4", "size": [0.3, 0.3, 3.5], "location": [4.75, 9.5, 1.75]}},
    {"command_name": "blender.create_cube", "parameters": {"name": "Pilote_E5", "size": [0.3, 0.3, 3.5], "location": [9.5, 9.5, 1.75]}},

    # --- VOLUMEN PRINCIPAL (Primer nivel: plano elevado) ---
    # Cuatro muros de 19.2m x 3.2m x 0.3m a h=3.5m
    {"command_name": "blender.create_pro_wall", "parameters": {"name": "Muro_Norte", "width": 19.2, "height": 3.2, "thickness": 0.3, "location": [0, 9.6, 5.1]}},
    {"command_name": "blender.create_pro_wall", "parameters": {"name": "Muro_Sur",   "width": 19.2, "height": 3.2, "thickness": 0.3, "location": [0, -9.6, 5.1]}},
    {"command_name": "blender.create_pro_wall", "parameters": {"name": "Muro_Este",  "width": 0.3,  "height": 3.2, "thickness": 19.2,"location": [9.6, 0, 5.1]}},
    {"command_name": "blender.create_pro_wall", "parameters": {"name": "Muro_Oeste", "width": 0.3,  "height": 3.2, "thickness": 19.2,"location": [-9.6, 0, 5.1]}},

    # --- LOSA PRIMER NIVEL (techo del área habitacional) ---
    {"command_name": "blender.create_cube", "parameters": {"name": "Losa_PrimerNivel", "size": [19.2, 19.2, 0.3], "location": [0, 0, 6.8]}},

    # --- VENTANAS LONGITUDINALES (fenêtre en longueur) ---
    # Norte y Sur: ventanas continuas de 15m x 1.2m de alto
    {"command_name": "blender.create_intelligent_window", "parameters": {"name": "Ventana_Norte_1", "width": 5.0, "height": 1.2, "location": [-5.0, 9.61, 4.8]}},
    {"command_name": "blender.create_intelligent_window", "parameters": {"name": "Ventana_Norte_2", "width": 5.0, "height": 1.2, "location": [0.0,  9.61, 4.8]}},
    {"command_name": "blender.create_intelligent_window", "parameters": {"name": "Ventana_Norte_3", "width": 5.0, "height": 1.2, "location": [5.0,  9.61, 4.8]}},
    {"command_name": "blender.create_intelligent_window", "parameters": {"name": "Ventana_Sur_1",   "width": 5.0, "height": 1.2, "location": [-5.0,-9.61, 4.8]}},
    {"command_name": "blender.create_intelligent_window", "parameters": {"name": "Ventana_Sur_2",   "width": 5.0, "height": 1.2, "location": [0.0, -9.61, 4.8]}},
    {"command_name": "blender.create_intelligent_window", "parameters": {"name": "Ventana_Sur_3",   "width": 5.0, "height": 1.2, "location": [5.0, -9.61, 4.8]}},

    # --- RAMPA INTERIOR (acceso helicoidal central) ---
    {"command_name": "blender.create_cube", "parameters": {"name": "Rampa_Nivel0_1", "size": [0.9, 5.0, 0.15], "location": [2.0, 0, 1.2]}},
    {"command_name": "blender.create_cube", "parameters": {"name": "Rampa_Nivel0_2", "size": [0.9, 5.0, 0.15], "location": [2.0, 0, 2.4]}},
    {"command_name": "blender.create_cube", "parameters": {"name": "Rampa_Nivel1_1", "size": [0.9, 5.0, 0.15], "location": [-2.0, 0, 3.6]}},
    {"command_name": "blender.create_cube", "parameters": {"name": "Rampa_Nivel1_2", "size": [0.9, 5.0, 0.15], "location": [-2.0, 0, 4.8]}},

    # --- TECHO-JARDÍN (segundo nivel / terraza) ---
    # Muro curvado del solarium (aprox 11.5m x 11.5m)
    {"command_name": "blender.create_cube", "parameters": {"name": "Solarium_Norte", "size": [11.5, 0.3, 2.0], "location": [0, 5.75, 8.0]}},
    {"command_name": "blender.create_cube", "parameters": {"name": "Solarium_Oeste", "size": [0.3, 11.5, 2.0], "location": [-5.75, 0, 8.0]}},
    {"command_name": "blender.create_cube", "parameters": {"name": "Solarium_Sur",   "size": [11.5, 0.3, 2.0], "location": [0, -5.75, 8.0]}},

    # --- LOSA DE TECHO (cubierta final) ---
    {"command_name": "blender.create_cube", "parameters": {"name": "Cubierta_Techo", "size": [19.2, 19.2, 0.2], "location": [0, 0, 9.8]}},

    # --- TERRENO / SUELO ---
    {"command_name": "blender.create_plane", "parameters": {"name": "Terreno", "size": [50, 50], "location": [0, 0, 0]}},
]

def run_villa_savoye_test():
    print("=" * 65)
    print("  🏛️  PRUEBA MAESTRA - VILLA SAVOYE (LE CORBUSIER, 1929)")
    print("  Objetivo: Copia exacta al 1000% - Coordenadas Reales")
    print("=" * 65)

    agent = Agent(force_mock=False)

    # Preparar el router UNA sola vez
    from core.intents.intent_router import IntentRouter
    from core.commands.blender_command_registry import register_blender_handlers
    router = IntentRouter()
    register_blender_handlers(router)

    print(f"\n[✓] Agente Zuly en línea. Ejecutando {len(VILLA_SAVOYE_PLAN)} pasos arquitectónicos...\n")

    resultados = {"ok": 0, "fail": 0, "pasos": []}
    start_total = time.time()

    for i, paso in enumerate(VILLA_SAVOYE_PLAN, 1):
        nombre = paso["parameters"].get("name", paso["command_name"])
        print(f"  [{i:02d}/{len(VILLA_SAVOYE_PLAN)}] ▶ {paso['command_name']} → {nombre}")

        # Construir intent y entities tal como espera route_and_execute
        intent = {
            "command": paso["command_name"],
            "name": paso["command_name"]
        }
        entities = paso["parameters"]

        cmd_result = router.route_and_execute(intent, entities)

        if cmd_result.status.name == "SUCCESS":
            resultados["ok"] += 1
            resultados["pasos"].append({"paso": i, "nombre": nombre, "status": "✓ OK"})
            print(f"         ✅ OK")
        else:
            resultados["fail"] += 1
            err = getattr(cmd_result, "error", "desconocido")
            resultados["pasos"].append({"paso": i, "nombre": nombre, "status": f"✗ FAIL: {err}"})
            print(f"         ❌ FALLÓ: {err}")

    elapsed = time.time() - start_total
    print("\n" + "=" * 65)
    print(f"  RESULTADO FINAL: {resultados['ok']}/{len(VILLA_SAVOYE_PLAN)} pasos exitosos")
    print(f"  Tiempo total: {elapsed:.2f}s")
    pct = (resultados["ok"] / len(VILLA_SAVOYE_PLAN)) * 100
    print(f"  Porcentaje de éxito: {pct:.1f}%")
    if pct == 100.0:
        print("  🏆 VILLA SAVOYE CONSTRUIDA AL 100%. ¡PRUEBA MAESTRA SUPERADA!")
    elif pct >= 80:
        print("  ✅ Estructura principal completada. Detalles menores pendientes.")
    else:
        print("  ⚠️  Revisión necesaria. Ver log para detalle de fallos.")
    print("=" * 65)

    # Log detallado
    import json
    with open("/opt/zuly/bitacora/prueba_villa_savoye_resultado.json", "w") as f:
        json.dump(resultados, f, indent=2, ensure_ascii=False)
    print(f"\n[✓] Reporte guardado en /opt/zuly/bitacora/prueba_villa_savoye_resultado.json")

if __name__ == "__main__":
    run_villa_savoye_test()

