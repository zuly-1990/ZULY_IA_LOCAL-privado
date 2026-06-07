"""
scripts/zuly_lab_model_inspirado.py
ZULY LAB - Reto 6.8 - Modelado Inspirado por Ingeniería Inversa
Zuly genera un conjunto arquitectónico combinando las proporciones
aprendidas de casarural.blend y edificio_2.blend.
"""
import sys, json

ZULY_PATH = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL"
if ZULY_PATH not in sys.path:
    sys.path.insert(0, ZULY_PATH)

import bpy
from core.agent import Agent
from core.utils.logging import log_info, log_success, log_error

def main():
    log_info("=" * 55)
    log_info("ZULY LAB - SÍNTESIS ARQUITECTÓNICA")
    log_info("Modelado Inspirado por Ingeniería Inversa")
    log_info("=" * 55)

    agent = Agent()
    adapter = agent.engine_adapter

    # ─── Leer ADN de los modelos del usuario ───────────────────
    pattern_casa = json.load(open(
        ZULY_PATH + r"\knowledge_base\patterns\learned\pattern_casarural_v1.json",
        encoding='utf-8'))
    pattern_edif = json.load(open(
        ZULY_PATH + r"\knowledge_base\patterns\learned\pattern_edificio2_v1.json",
        encoding='utf-8'))

    # Sacar estadísticas básicas del ADN
    dims_casa = [o['dimensions'] for o in pattern_casa['objects']]
    dims_edif = [o['dimensions'] for o in pattern_edif['objects']]
    avg_h_casa  = sum(d[2] for d in dims_casa if d[2] > 0.1) / max(len(dims_casa), 1)
    avg_w_edif  = sum(d[0] for d in dims_edif if d[0] > 0.5) / max(len(dims_edif), 1)
    max_d_edif  = max((d[0] for d in dims_edif), default=10.0)

    log_info(f"ADN Casa Rural → altura promedio piezas: {avg_h_casa:.2f}m")
    log_info(f"ADN Edificio 2 → anchura promedio: {avg_w_edif:.2f}m | mayor dim: {max_d_edif:.2f}m")

    # ─── Limpiar escena ────────────────────────────────────────
    adapter.clear_scene()

    # ─── CONJUNTO ARQUITECTÓNICO "SÍNTESIS ZULY v1" ───────────
    # Concepto: Viilla compacta + Torre de referencia, proporciones derivadas del ADN.

    # ── Base de la Plaza (inspirada en la dimensión circular del Edificio 2) ──
    bpy.ops.mesh.primitive_circle_add(
        vertices=32,
        radius=max_d_edif * 0.25,   # 25% de la mayor dimensión leída
        fill_type='NGON',
        location=(0, 0, 0))
    plaza = bpy.context.active_object
    plaza.name = "ZULY_Plaza_Sintetizada"
    bpy.ops.transform.resize(value=(1, 1, 0.02))  # plato de plaza plano

    # ── Torre central (escala derivada del edificio_2) ──────────
    h_torre = avg_w_edif * 0.8 if avg_w_edif > 2 else 15.0
    adapter.create_primitive('cube',
        name='ZULY_Torre_Central',
        location=[0, 0, h_torre / 2],
        scale=[avg_w_edif * 0.15, avg_w_edif * 0.15, h_torre / 2]
    )

    # Bisel estructural (aprendido del ADN de Ciudad 7.1)
    adapter.add_modifier('ZULY_Torre_Central', type='BEVEL', width=0.08, segments=2)

    # ── Cuerpos laterales (casas rurales compactas usando proporciones del Casa Rural) ──
    posiciones = [
        ( avg_w_edif * 0.5,  0, avg_h_casa / 2),
        (-avg_w_edif * 0.5,  0, avg_h_casa / 2),
        ( 0,  avg_w_edif * 0.5, avg_h_casa / 2),
        ( 0, -avg_w_edif * 0.5, avg_h_casa / 2),
    ]
    for idx, pos in enumerate(posiciones):
        nombre = f"ZULY_CuerpoRural_{idx + 1}"
        adapter.create_primitive('cube',
            name=nombre,
            location=list(pos),
            scale=[avg_h_casa * 0.7, avg_h_casa * 0.7, avg_h_casa * 0.5]
        )
        # Cubierta tipo rural: techo inclinado simulado (cono)
        adapter.create_primitive('cone',
            name=f"ZULY_Techo_{idx + 1}",
            location=[pos[0], pos[1], avg_h_casa + (avg_h_casa * 0.5)],
            scale=[avg_h_casa * 0.8, avg_h_casa * 0.8, avg_h_casa * 0.4]
        )

    # ── Luz de Escena ────────────────────────────────────────────
    adapter.create_primitive('cube',
        name='ZULY_Placeholder_Light',
        location=[0, 0, h_torre * 1.5]
    )
    bpy.ops.object.select_all(action='DESELECT')
    obj = bpy.data.objects.get('ZULY_Placeholder_Light')
    if obj:
        bpy.context.scene.objects.unlink(obj) if hasattr(bpy.context.scene, 'objects') else None
        bpy.data.objects.remove(obj, do_unlink=True)

    bpy.ops.object.light_add(type='SUN', location=(0, 0, h_torre * 2))
    bpy.context.active_object.name = "ZULY_Sol_Sintetico"

    # ── Exportar ─────────────────────────────────────────────────
    out = ZULY_PATH + r"\ZULY_PROJECTS\ZULY_SINTESIS_LAB_V1.blend"
    bpy.ops.wm.save_as_mainfile(filepath=out)
    log_success(f"Conjunto Arquitectónico guardado: {out}")
    log_success("Zuly ha sintetizado un modelo real a partir del ADN de tus obras. RETO 6.8 COMPLETADO.")

if __name__ == "__main__":
    main()
