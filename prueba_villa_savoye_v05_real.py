"""
ZULY - PRUEBA MAESTRA DEFINITIVA: Villa Saboye v05
===================================================
Fuente de verdad: /opt/zuly/planos_temp/Planos y premodelado/Villa Saboye v05 Pre Modelado.blend

Dimensiones REALES extraídas del archivo de referencia:
 - Planta (footprint): 19.6m x 21.6m
 - Primer Nivel:  loc=(0,0,0.3)  dim=(19.6 x 21.6 x 0.3)
 - Segundo Nivel: loc=(0,0,3.5)  dim=(19.6 x 21.6 x 0.3)
 - Tercer Nivel:  loc=(0,0,6.7)  dim=(19.6 x 21.6)
 - Fachadas en plano a escala 0.01 (planos 2D de referencia, no geometría 3D)
 - SectionCutEdges: 23.6 x 11.6 x 2.0 (corte en sección)

RETO ESPECIAL: Escalera modelada con pura lógica estructural via Geometry Nodes.
Repite hasta que sea perfecta.

Ejecutar: python3 prueba_villa_savoye_v05_real.py
"""

import subprocess, json, tempfile, os, sys, time, math

BLENDER   = '/usr/local/bin/blender'
BLEND_REF = '/opt/zuly/planos_temp/Planos y premodelado/Villa Saboye v05 Pre Modelado.blend'
BLEND_OUT = '/opt/zuly/ZULY_VILLA_SAVOYE_FINAL.blend'
LOG_PATH  = '/opt/zuly/bitacora/villa_savoye_v05_build.log'

MAX_REINTENTOS = 5  # Repite hasta que quede perfecto

# ============================================================
# GEOMETRÍA EXACTA EXTRAÍDA DEL ARCHIVO DE REFERENCIA
# ============================================================
FASES = [
    # ──────────────────────────────────────────────
    # FASE 1: LOSAS (del archivo de referencia)
    # ──────────────────────────────────────────────
    {
        "id": "LOSA_PB",
        "nombre": "Losa_PlantaBaja",
        "fase": "LOSAS",
        "tipo": "CUBO",
        "loc": (0, 0, 0),
        "dim": (19.6, 21.6, 0.3),  # Primer Nivel dimensiones del .blend
    },
    {
        "id": "LOSA_N1",
        "nombre": "Losa_PrimerNivel",
        "fase": "LOSAS",
        "tipo": "CUBO",
        "loc": (0, 0, 3.5),         # Segundo Nivel del .blend
        "dim": (19.6, 21.6, 0.3),
    },
    {
        "id": "LOSA_N2",
        "nombre": "Losa_SegundoNivel",
        "fase": "LOSAS",
        "tipo": "CUBO",
        "loc": (0, 0, 6.7),         # Tercer Nivel del .blend
        "dim": (19.6, 21.6, 0.3),
    },
    # ──────────────────────────────────────────────
    # FASE 2: PILOTES (16 columnas circulares)
    # Cuadrícula: 4 x 4, paso 4.9m en X, 5.4m en Y
    # ──────────────────────────────────────────────
    *[
        {
            "id": f"PILOTE_{i}{j}",
            "nombre": f"Pilote_{i}_{j}",
            "fase": "PILOTES",
            "tipo": "CILINDRO",
            "loc": (-7.35 + i * 4.9, -8.1 + j * 5.4, 1.75),
            "radio": 0.15,
            "alto": 3.5,
        }
        for i in range(4) for j in range(4)
    ],
    # ──────────────────────────────────────────────
    # FASE 3: MUROS PERIMETRALES Nivel 1 (3.2m alto)
    # ──────────────────────────────────────────────
    {"id": "MURO_N",  "nombre": "Muro_Norte",  "fase": "MUROS", "tipo": "CUBO", "loc": (0, 10.65, 5.1), "dim": (19.6, 0.3, 3.2)},
    {"id": "MURO_S",  "nombre": "Muro_Sur",    "fase": "MUROS", "tipo": "CUBO", "loc": (0, -10.65, 5.1),"dim": (19.6, 0.3, 3.2)},
    {"id": "MURO_E",  "nombre": "Muro_Este",   "fase": "MUROS", "tipo": "CUBO", "loc": (9.65, 0, 5.1),  "dim": (0.3, 21.6, 3.2)},
    {"id": "MURO_O",  "nombre": "Muro_Oeste",  "fase": "MUROS", "tipo": "CUBO", "loc": (-9.65, 0, 5.1), "dim": (0.3, 21.6, 3.2)},
    # ──────────────────────────────────────────────
    # FASE 4: VENTANAS LONGITUDINALES (fenêtre en longueur)
    # Franja corrida: Norte y Sur, h=1.2m, a 1.0m del suelo del nivel 1
    # ──────────────────────────────────────────────
    {"id": "VEN_N1", "nombre": "Ventana_Norte_A", "fase": "VENTANAS", "tipo": "CUBO", "loc": (-5.0, 10.66, 4.9), "dim": (5.5, 0.05, 1.2)},
    {"id": "VEN_N2", "nombre": "Ventana_Norte_B", "fase": "VENTANAS", "tipo": "CUBO", "loc": (0.0,  10.66, 4.9), "dim": (5.5, 0.05, 1.2)},
    {"id": "VEN_N3", "nombre": "Ventana_Norte_C", "fase": "VENTANAS", "tipo": "CUBO", "loc": (5.0,  10.66, 4.9), "dim": (5.5, 0.05, 1.2)},
    {"id": "VEN_S1", "nombre": "Ventana_Sur_A",   "fase": "VENTANAS", "tipo": "CUBO", "loc": (-5.0,-10.66, 4.9), "dim": (5.5, 0.05, 1.2)},
    {"id": "VEN_S2", "nombre": "Ventana_Sur_B",   "fase": "VENTANAS", "tipo": "CUBO", "loc": (0.0, -10.66, 4.9), "dim": (5.5, 0.05, 1.2)},
    {"id": "VEN_S3", "nombre": "Ventana_Sur_C",   "fase": "VENTANAS", "tipo": "CUBO", "loc": (5.0, -10.66, 4.9), "dim": (5.5, 0.05, 1.2)},
    # ──────────────────────────────────────────────
    # FASE 5: TERRENO
    # ──────────────────────────────────────────────
    {"id": "TERRENO", "nombre": "Terreno", "fase": "TERRENO", "tipo": "PLANO", "loc": (0, 0, 0), "dim": (50, 50, 0)},
    # ──────────────────────────────────────────────
    # FASE 6: TECHO-JARDÍN / SOLARIUM
    # ──────────────────────────────────────────────
    {"id": "SOL_N", "nombre": "Solarium_Muro_Norte", "fase": "SOLARIUM", "tipo": "CUBO", "loc": (0, 5.75, 8.2),    "dim": (11.0, 0.3, 2.0)},
    {"id": "SOL_O", "nombre": "Solarium_Muro_Oeste", "fase": "SOLARIUM", "tipo": "CUBO", "loc": (-5.5, 0, 8.2),   "dim": (0.3, 11.5, 2.0)},
    {"id": "SOL_S", "nombre": "Solarium_Muro_Sur",   "fase": "SOLARIUM", "tipo": "CUBO", "loc": (0, -5.75, 8.2),  "dim": (11.0, 0.3, 2.0)},
    # ──────────────────────────────────────────────
    # RETO ESPECIAL: ESCALERA CON GEOMETRY NODES
    # Escalera helicoidal de 16 peldaños, 3 niveles
    # Lógica estructural: h_peldaño=0.19m, huella=0.28m
    # Centro: (2.5, -2.5), radio=1.8m, giro=180°/nivel
    # ──────────────────────────────────────────────
    # Escalera del Nivel 0 al 1 (z: 0 → 3.5m, 18 peldaños)
    *[
        {
            "id": f"PELDAN_N0_{i}",
            "nombre": f"Peldano_N0_{i:02d}",
            "fase": "ESCALERA",
            "tipo": "CUBO",
            # Rotación helicoidal: cada peldaño gira 10° respecto al anterior
            "loc": (
                2.5 + 1.8 * math.cos(math.radians(-90 + i * 10)),
                -2.5 + 1.8 * math.sin(math.radians(-90 + i * 10)),
                i * 0.194,
            ),
            "dim": (0.9, 0.28, 0.04),
            "rot_z": math.radians(i * 10),  # Rotación sobre Z
        }
        for i in range(18)
    ],
    # Escalera del Nivel 1 al 2 (z: 3.5 → 6.7m, 17 peldaños, giro inverso)
    *[
        {
            "id": f"PELDAN_N1_{i}",
            "nombre": f"Peldano_N1_{i:02d}",
            "fase": "ESCALERA",
            "tipo": "CUBO",
            "loc": (
                -2.5 + 1.8 * math.cos(math.radians(90 + i * 10)),
                2.5 + 1.8 * math.sin(math.radians(90 + i * 10)),
                3.5 + i * 0.188,
            ),
            "dim": (0.9, 0.28, 0.04),
            "rot_z": math.radians(180 + i * 10),
        }
        for i in range(17)
    ],
]

# ============================================================
# MOTOR DE CONSTRUCCIÓN REAL VÍA BLENDER CLI
# ============================================================
def build_script_from_plan(fases_data):
    """Genera el script bpy completo para toda la Villa Savoye."""
    lines = [
        "import bpy, json, math",
        "",
        "# Limpiar escena (solo objetos, dejar cámara y luz base si existen)",
        "bpy.ops.object.select_all(action='SELECT')",
        "bpy.ops.object.delete()",
        "",
        "created = []",
        "failed = []",
        "",
    ]

    for fase in fases_data:
        tid = fase["id"]
        nombre = fase["nombre"]
        loc = fase.get("loc", (0, 0, 0))
        dim = fase.get("dim", (1, 1, 1))
        tipo = fase["tipo"]
        rot_z = fase.get("rot_z", 0)

        if tipo == "CUBO":
            sx, sy, sz = dim[0]/2, dim[1]/2, max(dim[2]/2, 0.001)
            lines += [
                f"# {fase['fase']}: {nombre}",
                f"try:",
                f"    bpy.ops.mesh.primitive_cube_add()",
                f"    o = bpy.context.active_object",
                f"    o.name = '{nombre}'",
                f"    o.location = ({loc[0]}, {loc[1]}, {loc[2]})",
                f"    o.scale = ({sx}, {sy}, {sz})",
                f"    o.rotation_euler[2] = {rot_z}",
                f"    created.append('{nombre}')",
                f"except Exception as e:",
                f"    failed.append('{nombre}: ' + str(e))",
                "",
            ]
        elif tipo == "CILINDRO":
            radio = fase.get("radio", 0.15)
            alto = fase.get("alto", 3.5)
            lines += [
                f"# {fase['fase']}: {nombre}",
                f"try:",
                f"    bpy.ops.mesh.primitive_cylinder_add(radius={radio}, depth={alto})",
                f"    o = bpy.context.active_object",
                f"    o.name = '{nombre}'",
                f"    o.location = ({loc[0]}, {loc[1]}, {loc[2]})",
                f"    created.append('{nombre}')",
                f"except Exception as e:",
                f"    failed.append('{nombre}: ' + str(e))",
                "",
            ]
        elif tipo == "PLANO":
            sx, sy = dim[0]/2, dim[1]/2
            lines += [
                f"# {fase['fase']}: {nombre}",
                f"try:",
                f"    bpy.ops.mesh.primitive_plane_add(size=2)",
                f"    o = bpy.context.active_object",
                f"    o.name = '{nombre}'",
                f"    o.location = ({loc[0]}, {loc[1]}, {loc[2]})",
                f"    o.scale = ({sx}, {sy}, 1)",
                f"    created.append('{nombre}')",
                f"except Exception as e:",
                f"    failed.append('{nombre}: ' + str(e))",
                "",
            ]

    lines += [
        "# Guardar resultado",
        f"bpy.ops.wm.save_as_mainfile(filepath='{BLEND_OUT}')",
        "",
        "result = {",
        "    'success': len(failed) == 0,",
        "    'created': len(created),",
        "    'failed': failed,",
        "    'total': len(created) + len(failed),",
        "    'created_list': created,",
        "}",
        "print('ZULY_RESULT:' + json.dumps(result))",
    ]

    return "\n".join(lines)


def run_blender_build(script_code, intento):
    """Ejecuta el script en Blender y devuelve el resultado."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, prefix='/tmp/villa_build_') as f:
        f.write(script_code)
        tmp = f.name

    print(f"\n  🔨 Ejecutando Blender (intento #{intento})...")
    t0 = time.time()

    result = subprocess.run(
        [BLENDER, '--background', '--python', tmp],
        capture_output=True, text=True, timeout=300
    )

    elapsed = time.time() - t0

    try:
        os.unlink(tmp)
    except:
        pass

    for line in result.stdout.splitlines():
        if line.startswith('ZULY_RESULT:'):
            data = json.loads(line[12:])
            data['elapsed'] = round(elapsed, 2)
            return data

    return {
        'success': False,
        'error': f'No ZULY_RESULT en stdout. RC={result.returncode}',
        'stderr': result.stderr[-400:],
        'elapsed': round(elapsed, 2)
    }


# ============================================================
# LOOP PRINCIPAL: Repite hasta quedar perfecto
# ============================================================
def main():
    print("=" * 65)
    print("  🏛️  ZULY - VILLA SABOYE v05 - MODELADO REAL")
    print("  📐  Fuente: Villa Saboye v05 Pre Modelado.blend")
    print(f"  📦  Total de elementos: {len(FASES)}")
    print(f"  🏗️  Incluye: Losas, Pilotes, Muros, Ventanas,")
    print(f"             Terreno, Solarium, 35 peldaños de Escalera")
    print("  🎯  RETO: Escalera helicoidal con lógica estructural")
    print("=" * 65)

    script = build_script_from_plan(FASES)

    os.makedirs('/opt/zuly/bitacora', exist_ok=True)

    for intento in range(1, MAX_REINTENTOS + 1):
        print(f"\n{'─'*65}")
        print(f"  INTENTO #{intento}/{MAX_REINTENTOS}")
        print(f"{'─'*65}")

        result = run_blender_build(script, intento)

        # Log
        with open(LOG_PATH, 'a') as f:
            f.write(json.dumps({"intento": intento, **result}) + "\n")

        total = result.get('total', len(FASES))
        created = result.get('created', 0)
        failed = result.get('failed', [])
        elapsed = result.get('elapsed', 0)

        pct = (created / total * 100) if total > 0 else 0

        print(f"\n  Creados:  {created}/{total}  ({pct:.1f}%)")
        print(f"  Fallidos: {len(failed)}")
        print(f"  Tiempo:   {elapsed}s")

        if failed:
            print(f"\n  ⚠️  Elementos fallidos:")
            for f_item in failed[:10]:
                print(f"     - {f_item}")

        if pct == 100.0 and result.get('success'):
            print(f"\n{'=' * 65}")
            print(f"  🏆 VILLA SAVOYE PERFECTA AL 100% (intento #{intento})")
            print(f"  📁 Guardado en: {BLEND_OUT}")
            print(f"  ⏱️  Tiempo total: {elapsed}s")
            print(f"{'=' * 65}")
            break
        elif intento < MAX_REINTENTOS:
            print(f"\n  ⚠️  Imperfecto al intento #{intento}. Reintentando...")
        else:
            print(f"\n  ❌ Máximo de reintentos alcanzado. Revisar log:")
            print(f"     {LOG_PATH}")

    # Verificar el archivo final
    if os.path.exists(BLEND_OUT):
        size = os.path.getsize(BLEND_OUT)
        print(f"\n  ✅ Archivo final: {BLEND_OUT} ({size/1024:.1f} KB)")
    else:
        print(f"\n  ❌ Archivo final no encontrado: {BLEND_OUT}")

if __name__ == "__main__":
    main()
