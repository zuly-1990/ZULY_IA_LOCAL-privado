import os
import subprocess
import sys
import re

# Asegurar que se puede importar desde la raiz del proyecto
sys.path.append('/opt/zuly')

from core.external.multi_api_orchestrator import MultiAPIOrchestrator

# Metricas heurísticas para la Fase V9 (Modelado Volumétrico 3D Real)
TARGET_METRICS_V9 = {
    "01 Primer Nivel v08.dxf":              {"Z_TARGET": 3.50, "F_MIN": 100, "3D": True},
    "02 Segundo Nivel v02.dxf":             {"Z_TARGET": 3.20, "F_MIN": 100, "3D": True},
    "03 Tercer Nivel v02.dxf":              {"Z_TARGET": 3.00, "F_MIN": 50,  "3D": True},
    "04 Fachada Principal v01.dxf":         {"Z_TARGET": 0.00, "F_MIN": 0,   "3D": False},
    "05 Fachada Lateral Derecho v01.dxf":   {"Z_TARGET": 0.00, "F_MIN": 0,   "3D": False},
    "06 Fachada Lateral Izquierdo v01.dxf": {"Z_TARGET": 0.00, "F_MIN": 0,   "3D": False},
    "07 Fachada Posterior v01.dxf":         {"Z_TARGET": 0.00, "F_MIN": 0,   "3D": False},
    "08 Corte 01.dxf":                      {"Z_TARGET": 0.00, "F_MIN": 0,   "3D": False},
    "08 Corte 02.dxf":                      {"Z_TARGET": 0.00, "F_MIN": 0,   "3D": False},
    "08 Corte 03.dxf":                      {"Z_TARGET": 0.00, "F_MIN": 0,   "3D": False},
}

def extract_python_code(response: str) -> str:
    if not response or len(response) < 20:
        return ""
    if response.startswith("ERROR_") or "quota" in response.lower() or "rate limit" in response.lower():
        return ""
    if "```python" in response:
        return response.split("```python")[1].split("```")[0].strip()
    if response.strip().startswith("import bpy"):
        return response.strip()
    return ""

def extract_metrics(output: str):
    """Busca la linea METRICAS_ZULY: V=100, F=10, Z=0.3 en el stdout de Blender"""
    match = re.search(r"METRICAS_ZULY:\s*V=(\d+),\s*F=(\d+),\s*Z=([0-9.]+)", output)
    if match:
        return {
            "V": int(match.group(1)),
            "F": int(match.group(2)),
            "Z": round(float(match.group(3)), 3)
        }
    return None

def process_dxf_v9(dxf_path: str, output_dir: str, orchestrator: MultiAPIOrchestrator):
    basename = os.path.basename(dxf_path)
    blend_name = basename.replace('.dxf', '_v9_3d.blend')
    output_path = os.path.join(output_dir, blend_name)

    target = TARGET_METRICS_V9.get(basename)
    if not target:
        print("[SKIP] " + basename + " no tiene metricas V9 definidas.")
        return False

    # Detectar prefijo de piso para nombramiento de objetos separados
    if "Primer" in basename or basename.startswith("01"):
        floor_prefix = "N1"
    elif "Segundo" in basename or basename.startswith("02"):
        floor_prefix = "N2"
    elif "Tercer" in basename or basename.startswith("03"):
        floor_prefix = "N3"
    else:
        floor_prefix = "N0"

    print("")
    print("=" * 60)
    print("[ZULY V9] Procesando volumetricamente: " + basename)
    print("=" * 60)

    if target['3D']:
        instruccion_geometria = (
            f"Este plano requiere EXTRUSION VOLUMETRICA 3D REAL.\n"
            f"CRITICO: NO unir todos los elementos en un solo objeto al final.\n"
            f"Cada tipo de elemento debe quedar como OBJETO SEPARADO con prefijo '{floor_prefix}_'.\n"
            f"\n"
            f"=== PASO 1: CREAR LOSA BASE Y LOSA DE TECHO ===\n"
            f"El footprint estandar de la Villa Savoye es:\n"
            f"   min_x, max_x = -0.1, 19.7\n"
            f"   min_y, max_y = -0.1, 21.7\n"
            f"   losa_width_x = max_x - min_x  # 19.8m\n"
            f"   losa_length_y = max_y - min_y  # 21.8m\n"
            f"   losa_center_x = (min_x + max_x) / 2.0  # 9.8m\n"
            f"   losa_center_y = (min_y + max_y) / 2.0  # 10.8m\n"
            f"   # LOSA BASE: Z de 0.0 a 0.30m\n"
            f"   bpy.ops.mesh.primitive_cube_add(size=1.0, enter_editmode=False, location=(losa_center_x, losa_center_y, 0.15))\n"
            f"   losa_base = bpy.context.active_object\n"
            f"   losa_base.name = '{floor_prefix}_Losa_Base'\n"
            f"   losa_base.dimensions = (19.8, 21.8, 0.30)\n"
            f"   # LOSA DE TECHO: cima del nivel, Z de ({target['Z_TARGET']}-0.30) a {target['Z_TARGET']}m\n"
            f"   bpy.ops.mesh.primitive_cube_add(size=1.0, enter_editmode=False, location=(losa_center_x, losa_center_y, {target['Z_TARGET']} - 0.15))\n"
            f"   losa_techo = bpy.context.active_object\n"
            f"   losa_techo.name = '{floor_prefix}_Losa_Techo'\n"
            f"   losa_techo.dimensions = (19.8, 21.8, 0.30)\n"
            f"\n"
            f"=== PASO 2: PROCESAR, EXTRUIR Y NOMBRAR CADA CAPA ===\n"
            f"Para cada capa: une sus objetos, procesa geometria, extruye y RENOMBRA el resultado con prefijo '{floor_prefix}_'.\n"
            f"\n"
            f"   MUROS (objetos cuyo nombre empieza con 'ZMUROS_curve_'):\n"
            f"   - spline.use_cyclic_u=True -> join -> Edit Mode -> remove_doubles(0.01) -> fill_holes(sides=0)\n"
            f"   - extrude_region_move Z={target['Z_TARGET']-0.30:.2f}m -> normals_make_consistent(inside=False) -> Object Mode\n"
            f"   - location.z = 0.30\n"
            f"   - RENOMBRAR: bpy.context.active_object.name = '{floor_prefix}_Muros'\n"
            f"\n"
            f"   MURETES (objetos cuyo nombre empieza con 'ZMURETES_curve_'):\n"
            f"   - Mismo proceso. extrude 0.80m. location.z=0.30\n"
            f"   - RENOMBRAR: '{floor_prefix}_Muretes'\n"
            f"\n"
            f"   COLUMNAS (objetos cuyo nombre empieza con 'ZCOLUMNAS_curve_'):\n"
            f"   - spline.use_cyclic_u=True -> join -> Edit Mode -> remove_doubles(0.001) -> fill_holes(sides=0)\n"
            f"   - extrude_region_move Z={target['Z_TARGET']-0.30:.2f}m -> normals_make_consistent(inside=False) -> Object Mode\n"
            f"   - location.z = 0.30\n"
            f"   - RENOMBRAR: '{floor_prefix}_Columnas'\n"
            f"\n"
            f"   VENTANAS ('ZCRISTAL_curve_' o 'ZVENTANAL_curve_'):\n"
            f"   - join -> fill_holes(sides=0) -> extrude 1.90m -> location.z=0.30\n"
            f"   - RENOMBRAR: '{floor_prefix}_Ventanas'\n"
            f"\n"
            f"   PUERTAS ('BL|puertita ver_curve_'):\n"
            f"   - join -> fill_holes(sides=0) -> extrude 1.80m -> location.z=0.30\n"
            f"   - RENOMBRAR: '{floor_prefix}_Puertas'\n"
            f"\n"
            f"   ESCALERAS (nombre contiene 'ESCALERA' o empieza con 'BL|ESCALERA'):\n"
            f"   esc_objs = [o for o in bpy.context.scene.objects if 'ESCALERA' in o.name.upper()]\n"
            f"   SI hay objetos de escalera en el DXF (esc_objs no esta vacio):\n"
            f"     * Para cada objeto CURVE: spline.use_cyclic_u = True\n"
            f"     * join -> Edit Mode -> select all -> remove_doubles(0.01) -> fill_holes(sides=0)\n"
            f"     * extrude_region_move Z=0.25m -> normals_make_consistent(inside=False) -> Object Mode\n"
            f"     * location.z = 0.30\n"
            f"     * RENOMBRAR: '{floor_prefix}_Escalera'\n"
            f"   SI NO hay escaleras en el DXF (esc_objs esta vacio), GENERAR escalera parametrica:\n"
            f"     num_steps=16; step_d=0.28; step_h=0.18; step_w=2.4; sx=7.5; sy=9.0\n"
            f"     for i in range(num_steps):\n"
            f"         bpy.ops.mesh.primitive_cube_add(location=(sx+i*step_d+step_d/2, sy+step_w/2, 0.30+i*step_h+step_h/2))\n"
            f"         p=bpy.context.active_object; p.dimensions=(step_d, step_w, step_h); p.name='esc_p_'+str(i)\n"
            f"     peldanos=[o for o in bpy.context.scene.objects if o.name.startswith('esc_p_')]\n"
            f"     for p in peldanos: p.select_set(True)\n"
            f"     bpy.context.view_layer.objects.active=peldanos[0]\n"
            f"     bpy.ops.object.join()\n"
            f"     bpy.context.active_object.name='{floor_prefix}_Escalera'\n"
            f"\n"
            f"   CURVOS ('BL|Curvo 001_curve_'):\n"
            f"   - join -> fill_holes(sides=0) -> extrude {target['Z_TARGET']-0.30:.2f}m -> location.z=0.30\n"
            f"   - RENOMBRAR: '{floor_prefix}_Curvos'\n"
            f"\n"
            f"   PROYECCIONES ('ZPROYECCIONES' o 'BL|flecha'):\n"
            f"   - join -> extrude 0.08m -> location.z=0.30\n"
            f"   - RENOMBRAR: '{floor_prefix}_Proyecciones'\n"
            f"\n"
            f"=== PASO 3: REGLAS GLOBALES DE GEOMETRIA SOLIDA ===\n"
            f"   a. En TODO objeto tipo CURVE, antes de convert(target='MESH'), itera sus splines y establece spline.use_cyclic_u = True.\n"
            f"   b. Tras join() de cada capa: Edit Mode -> remove_doubles(0.01) -> fill_holes(sides=0).\n"
            f"   c. Tras extrude_region_move: normals_make_consistent(inside=False).\n"
            f"   d. select_non_manifold() -> fill() para tapar huecos restantes.\n"
            f"\n"
            f"=== PASO 4: NO UNIR — MANTENER OBJETOS SEPARADOS ===\n"
            f"IMPORTANTE: NO llames a bpy.ops.object.join() para unir TODOS los elementos al final.\n"
            f"Cada elemento ({floor_prefix}_Muros, {floor_prefix}_Columnas, {floor_prefix}_Losa_Base, {floor_prefix}_Losa_Techo, {floor_prefix}_Escalera, etc.)\n"
            f"debe quedar como objeto INDEPENDIENTE en la escena con su nombre correcto.\n"
            f"El compilador los organizara en colecciones por piso automaticamente."
        )
    else:
        instruccion_geometria = (
            "NO extruir. Este es un plano de Fachada o Corte y debe permanecer plano (Z=0).\n"
            "Solo convertir las curvas del DXF a MESH y unirlas. NO aplicar extrusiones."
        )

    prompt = (
        "Eres Zuly, IA Arquitecta de Codigo para Blender 3.6.\n"
        "Genera un script Python COMPLETO y AUTONOMO para Blender 3.6.\n"
        "El script debe ser 100% autosuficiente, sin imports externos al propio Blender.\n\n"
        "ARCHIVO DXF ORIGEN: " + dxf_path + "\n"
        "ARCHIVO BLEND DESTINO: " + output_path + "\n\n"
        "PASOS OBLIGATORIOS EN ORDEN:\n"
        "1. import bpy\n"
        "2. bpy.ops.object.select_all(action='SELECT') y bpy.ops.object.delete(use_global=False)\n"
        "3. bpy.ops.preferences.addon_enable(module='io_import_dxf')\n"
        "4. bpy.ops.import_scene.dxf(filepath='" + dxf_path + "')\n"
        "5. Seleccionar todos los objetos importados (de tipo CURVE o MESH) usando loop de seleccion segura try/except.\n"
        "6. Asegurarse de que al menos uno de los objetos seleccionados sea el objeto activo: si hay bpy.context.selected_objects, establecer el primero como activo (bpy.context.view_layer.objects.active = bpy.context.selected_objects[0]).\n"
        "7. Convertir todo a MESH: bpy.ops.object.convert(target='MESH')\n"
        "8. " + instruccion_geometria + "\n"
        "9. Medir el bounding box TOTAL de todos los objetos 3D y hacer print EXACTAMENTE asi:\n"
        "   all_3d = [o for o in bpy.context.scene.objects if o.type == 'MESH' and o.dimensions.z > 0.05]\n"
        "   if all_3d:\n"
        "       max_z_top = max(o.location.z + o.dimensions.z for o in all_3d)\n"
        "       min_z_bot = min(o.location.z for o in all_3d)\n"
        "       total_z = round(max_z_top - min_z_bot, 3)\n"
        "       total_v = sum(len(o.data.vertices) for o in all_3d)\n"
        "       total_f = sum(len(o.data.polygons) for o in all_3d)\n"
        "   else:\n"
        "       total_z, total_v, total_f = 0.0, 0, 0\n"
        "   print('METRICAS_ZULY: V=' + str(total_v) + ', F=' + str(total_f) + ', Z=' + str(total_z))\n"
        "10. bpy.ops.wm.save_as_mainfile(filepath='" + output_path + "')\n\n"
        "IMPORTANTE: Devuelve UNICAMENTE el bloque de codigo Python entre ```python ... ```. Sin explicaciones.\n\n"
        "TIP DE SELECCION SEGURA:\n"
        "for obj in list(bpy.context.scene.objects):\n"
        "    if obj.type in ['CURVE', 'MESH']:\n"
        "        try: obj.select_set(True)\n"
        "        except: pass\n\n"
        "TIP DE EXTRUSION Y UNION POR CAPAS (MÁXIMA EFICIENCIA):\n"
        "Para evitar lentitud o que Blender sea terminado por falta de memoria (Out of Memory), NO hagas bucles individuales sobre miles de objetos para extruirlos por separado.\n"
        "Es mucho mejor buscar todos los objetos de la misma capa (por ejemplo, los que empiezan con 'ZMUROS_curve_'), seleccionarlos todos, hacer uno de ellos el activo, y unirlos en un solo objeto usando `bpy.ops.object.join()` ANTES de extruir.\n"
        "Ejemplo para muros:\n"
        "   bpy.ops.object.select_all(action='DESELECT')\n"
        "   muros = [o for o in bpy.context.scene.objects if o.name.startswith('ZMUROS_curve_')]\n"
        "   if muros:\n"
        "       for m in muros: m.select_set(True)\n"
        "       bpy.context.view_layer.objects.active = muros[0]\n"
        "       bpy.ops.object.join()\n"
        "       muro_unificado = bpy.context.active_object\n"
        "       # Ahora extruye el muro_unificado una sola vez!\n\n"
        "TIP DE EXTRUSION PARA BLENDER 3.6:\n"
        "Para extruir un objeto en modo edicion:\n"
        "   bpy.ops.object.select_all(action='DESELECT')\n"
        "   obj_muro.select_set(True)\n"
        "   bpy.context.view_layer.objects.active = obj_muro\n"
        "   bpy.ops.object.mode_set(mode='EDIT')\n"
        "   bpy.ops.mesh.select_all(action='SELECT')\n"
        "   bpy.ops.mesh.extrude_region_move(\n"
        "       MESH_OT_extrude_region={},\n"
        "       TRANSFORM_OT_translate={'value': (0, 0, altura_z), 'orient_type': 'GLOBAL'}\n"
        "   )\n"
        "   bpy.ops.object.mode_set(mode='OBJECT')\n\n"
        "EVITAR ERRORES DE BLENDER 3.6:\n"
        "1. NO uses `center='BOUNDS_MIN'` en `bpy.ops.object.origin_set`. Usa `center='BOUNDS'` o `center='MEDIAN'`.\n"
        "2. NO uses `obj.data.total_edge_count` ni `obj.data.total_face_count`. Usa `len(obj.data.edges)` y `len(obj.data.polygons)`."
    )

    max_retries = 3
    current_prompt = prompt

    for attempt in range(1, max_retries + 1):
        print("[Intento " + str(attempt) + "/" + str(max_retries) + "] Pidiendo codigo a Gemini...")

        response = orchestrator.call_advanced_model(current_prompt)
        code = extract_python_code(response)

        if not code or len(code) < 50:
            print("[ERROR] Gemini devolvio una respuesta vacia o muy corta. Reintentando...")
            continue

        safe_name = basename.replace(' ', '_').replace('.dxf', '')
        temp_script = "/opt/zuly/temp_v9_" + safe_name + ".py"
        with open(temp_script, "w", encoding="utf-8") as f:
            f.write(code)

        print("[Ejecutando] blender -b -P " + temp_script)
        cmd = ["blender", "-b", "-P", temp_script]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)

        combined_output = result.stdout + "\n" + result.stderr
        metrics = extract_metrics(combined_output)

        if result.returncode != 0 and not metrics:
            print("[ERROR] Blender fallo con codigo " + str(result.returncode))
            last_stderr = result.stderr[-1500:] if result.stderr else "Sin STDERR"
            feedback = (
                "El script fallo al ejecutarse en Blender con codigo de salida " +
                str(result.returncode) + ".\n\n"
                "ULTIMAS LINEAS DE ERROR:\n" + last_stderr + "\n\n"
                "Corrige el error y devuelve el codigo Python completo y corregido."
            )
        elif not metrics:
            print("[ERROR] Blender termino pero no se encontraron METRICAS_ZULY en la salida.")
            print("[STDOUT RECORTADO]:", result.stdout[-500:])
            feedback = (
                "El script se ejecuto pero no imprimio la linea METRICAS_ZULY correctamente.\n"
                "Asegurate de que la linea print sea EXACTAMENTE:\n"
                "print('METRICAS_ZULY: V=' + str(len(obj.data.vertices)) + ', F=' + str(len(obj.data.polygons)) + ', Z=' + str(round(obj.dimensions.z, 3)))\n"
                "Devuelve el codigo completo corregido."
            )
        else:
            v_obtenidos = metrics['V']
            f_obtenidos = metrics['F']
            z_obtenidos = metrics['Z']

            print("[RESULTADO] V: " + str(v_obtenidos) +
                  " | F: " + str(f_obtenidos) +
                  " | Z: " + str(z_obtenidos))

            # Validacion heuristica V9
            z_diff = abs(z_obtenidos - target['Z_TARGET'])
            z_ok = z_diff < 0.10  # Tolerancia de 10 cm en altura Z
            f_ok = (target['F_MIN'] == 0 and f_obtenidos == 0) or (target['F_MIN'] > 0 and f_obtenidos >= target['F_MIN'])

            is_perfect = z_ok and f_ok

            if is_perfect:
                print("[EXITO V9] Modelado 3D correcto! Guardado en: " + output_path)
                knowledge_file = "/opt/zuly/bitacora/aprendizaje_v9.log"
                with open(knowledge_file, "a", encoding="utf-8") as kf:
                    kf.write(
                        "EXITO V9 | Plano: " + basename +
                        " | V:" + str(v_obtenidos) +
                        " | F:" + str(f_obtenidos) +
                        " | Z:" + str(z_obtenidos) + "\n"
                    )
                return True
            else:
                print("[DIFERENCIA V9] Altura Z o Caras no coinciden con los objetivos 3D.")
                feedback = (
                    "El modelo 3D se genero pero no tiene la altura o cantidad de caras adecuadas.\n\n"
                    "TU RESULTADO => Caras: " + str(f_obtenidos) + ", Altura Z: " + str(z_obtenidos) + "m\n"
                    "OBJETIVO     => Caras Min: " + str(target['F_MIN']) + ", Altura Z: " + str(target['Z_TARGET']) + "m\n\n"
                    "Corrige el codigo para extruir correctamente las capas (ZMUROS, ZCOLUMNAS, ZMURETES) en 3D."
                )

        current_prompt = (
            prompt + "\n\n"
            "============================================================\n"
            "ERROR O DISCREPANCIA EN EL INTENTO ANTERIOR:\n"
            "============================================================\n"
            "Tu codigo anterior fue:\n"
            "```python\n" + code + "\n```\n\n"
            "Resultado/Error obtenido:\n" + feedback + "\n"
            "Por favor, analiza el error/resultado, corrige los fallos, y genera de nuevo el script completo."
        )

    print("[AGOTADO] " + str(max_retries) + " intentos usados. No se pudo modelar en 3D: " + basename)
    return False

def main():
    print("=" * 60)
    print("ZULY V9: PIPELINE DE MODELADO VOLUMÉTRICO 3D AUTÓNOMO")
    print("=" * 60)

    orchestrator = MultiAPIOrchestrator()
    if not orchestrator.gemini_keys:
        print("CRITICO: No se encontraron llaves de Gemini. Abortando.")
        return

    print("APIs listas: Gemini con " + str(len(orchestrator.gemini_keys)) + " llave(s).")

    dxf_folder = "/opt/zuly/planos_temp/Planos y premodelado/"
    output_folder = "/opt/zuly/resultados_masivos_v9/"
    os.makedirs(output_folder, exist_ok=True)

    exitosos = 0
    fallidos = 0
    total = len(TARGET_METRICS_V9)

    for basename, target in TARGET_METRICS_V9.items():
        dxf_path = os.path.join(dxf_folder, basename)
        if os.path.exists(dxf_path):
            ok = process_dxf_v9(dxf_path, output_folder, orchestrator)
            if ok:
                exitosos += 1
            else:
                fallidos += 1
        else:
            print("[NO ENCONTRADO] " + dxf_path)
            fallidos += 1

    print("")
    print("=" * 60)
    print("REPORTE FINAL ZULY V9:")
    print("  Exitosos : " + str(exitosos) + "/" + str(total))
    print("  Fallidos : " + str(fallidos) + "/" + str(total))
    print("  Resultados en: " + output_folder)
    print("=" * 60)

if __name__ == "__main__":
    main()
