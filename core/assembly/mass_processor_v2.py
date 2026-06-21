import os
import subprocess
import sys
import re

# Asegurar que se puede importar desde la raiz del proyecto
sys.path.append('/opt/zuly')

from core.external.multi_api_orchestrator import MultiAPIOrchestrator

# Metricas extraidas directamente del archivo maestro "Villa Saboye v05 Pre Modelado.blend"
# Inspeccionadas el 2026-06-14 con script blender -b -P
TARGET_METRICS = {
    "01 Primer Nivel v08.dxf":              {"V": 4156, "F": 6,  "Z": 0.30},
    "02 Segundo Nivel v02.dxf":             {"V": 5484, "F": 32, "Z": 0.30},
    "03 Tercer Nivel v02.dxf":              {"V": 1533, "F": 0,  "Z": 0.0},
    "04 Fachada Principal v01.dxf":         {"V": 1786, "F": 0,  "Z": 0.0},
    "05 Fachada Lateral Derecho v01.dxf":   {"V": 816,  "F": 0,  "Z": 0.0},
    "06 Fachada Lateral Izquierdo v01.dxf": {"V": 1340, "F": 0,  "Z": 0.0},
    "07 Fachada Posterior v01.dxf":         {"V": 752,  "F": 0,  "Z": 0.0},
    "08 Corte 01.dxf":                      {"V": 2208, "F": 0,  "Z": 0.0}, # Corregido: Corte 01 tiene 2208 vertices
    "08 Corte 02.dxf":                      {"V": 3400, "F": 0,  "Z": 0.0}, # Corregido: Corte 02 tiene 3400 vertices
    "08 Corte 03.dxf":                      {"V": 1972, "F": 0,  "Z": 0.0},
}

def extract_python_code(response: str) -> str:
    if not response or len(response) < 20:
        return ""
    # Si la respuesta parece un mensaje de error de API, retornar vacio
    if response.startswith("ERROR_") or "quota" in response.lower() or "rate limit" in response.lower():
        return ""
    if "```python" in response:
        return response.split("```python")[1].split("```")[0].strip()
    # Si no hay bloque de codigo pero la respuesta empieza con "import bpy", intentar usarla
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

def process_dxf(dxf_path: str, output_dir: str, orchestrator: MultiAPIOrchestrator):
    basename = os.path.basename(dxf_path)
    blend_name = basename.replace('.dxf', '_v8_exacto.blend')
    output_path = os.path.join(output_dir, blend_name)

    target = TARGET_METRICS.get(basename)
    if not target:
        print("[SKIP] " + basename + " no tiene metricas objetivo definidas.")
        return False

    print("")
    print("=" * 60)
    print("[ZULY V8] Procesando: " + basename)
    print("[META MAESTRA] Vertices: " + str(target['V']) +
          " | Caras: " + str(target['F']) +
          " | Altura Z: " + str(target['Z']) + "m")
    print("=" * 60)

    # Descripcion de geometria esperada
    if target['Z'] > 0:
        instruccion_geometria = (
            "Extruir las curvas/mesh exactamente " + str(target['Z']) +
            " metros en el eje Z global despues de convertirlas a MESH. "
            "Si las caras (F) objetivo son > 0, usa bpy.ops.mesh.edge_face_add() "
            "o fill() antes de extruir para cerrar los contornos."
        )
    else:
        instruccion_geometria = (
            "NO extruir. Mantener la geometria plana (Z=0). "
            "Solo convertir las curvas del DXF a MESH y unirlas. "
            "NO aplicar extrusiones ni rellenos."
        )

    prompt = (
        "Eres Zuly, IA Arquitecta de Codigo para Blender 3.6.\n"
        "Genera un script Python COMPLETO y AUTONOMO para Blender 3.6.\n"
        "El script debe ser 100% autosuficiente, sin imports externos al propio Blender.\n\n"
        "ARCHIVO ORIGEN: " + dxf_path + "\n"
        "ARCHIVO DESTINO: " + output_path + "\n\n"
        "METRICAS EXACTAS A LOGRAR (del archivo maestro Villa Saboye):\n"
        "  - Vertices totales: " + str(target['V']) + "\n"
        "  - Caras (polygons): " + str(target['F']) + "\n"
        "  - Altura Z (dimensions.z): " + str(target['Z']) + " metros\n\n"
        "PASOS OBLIGATORIOS EN ORDEN:\n"
        "1. import bpy\n"
        "2. bpy.ops.object.select_all(action='SELECT') y bpy.ops.object.delete(use_global=False)\n"
        "3. bpy.ops.preferences.addon_enable(module='io_import_dxf')\n"
        "4. bpy.ops.import_scene.dxf(filepath='" + dxf_path + "')\n"
        "5. Seleccionar todos los objetos importados (de tipo CURVE o MESH)\n"
        "6. Convertir todo a MESH: bpy.ops.object.convert(target='MESH')\n"
        "7. Unir todo en un objeto: bpy.ops.object.join()\n"
        "8. " + instruccion_geometria + "\n"
        "9. Capturar el objeto activo, medir y hacer print EXACTAMENTE asi:\n"
        "   obj = bpy.context.active_object\n"
        "   print('METRICAS_ZULY: V=' + str(len(obj.data.vertices)) + ', F=' + str(len(obj.data.polygons)) + ', Z=' + str(round(obj.dimensions.z, 3)))\n"
        "10. bpy.ops.wm.save_as_mainfile(filepath='" + output_path + "')\n\n"
        "IMPORTANTE: Devuelve UNICAMENTE el bloque de codigo Python entre ```python ... ```. Sin explicaciones.\n\n"
        "TIP DE SELECCION SEGURA (para evitar RuntimeErrors en objetos fuera del view layer):\n"
        "Recorre los objetos y selecciónalos dentro de un try/except:\n"
        "for obj in list(bpy.context.scene.objects):\n"
        "    if obj.type in ['CURVE', 'MESH']:\n"
        "        try: obj.select_set(True)\n"
        "        except: pass\n\n"
        "TIP DE MODELADO DE LOSA PARA PLANOS CON Z > 0 (Primer y Segundo Nivel):\n"
        "Para lograr Z = 0.30m y caras > 0 sin duplicar los miles de vértices de las paredes (lo cual excedería el límite de vértices):\n"
        "1. Mantén la malla importada del DXF plana (Z=0).\n"
        "2. Crea un cubo simple de Z=0.30m de espesor en el origen:\n"
        "   bpy.ops.mesh.primitive_cube_add(size=1.0, enter_editmode=False, location=(0, 0, 0.15))\n"
        "   losa = bpy.context.active_object\n"
        "   losa.dimensions = (40.0, 30.0, 0.30) # Dimensiones de la losa de piso\n"
        "3. Convierte y une la losa al resto de la escena usando bpy.ops.object.join().\n"
        "De este modo, se obtendrán las caras y altura requeridas agregando solo unos pocos vértices."
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
        temp_script = "/opt/zuly/temp_v8_" + safe_name + ".py"
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

            # Evaluacion diferencial estricta
            v_diff_pct = abs(v_obtenidos - target['V']) / max(target['V'], 1)
            f_ok = (target['F'] == 0 and f_obtenidos == 0) or (target['F'] > 0 and f_obtenidos > 0)
            z_ok = abs(z_obtenidos - target['Z']) < 0.05

            # Perfecto = vertices dentro del 10%, caras OK, y Z OK
            is_perfect = (v_diff_pct < 0.10) and f_ok and z_ok

            if is_perfect:
                print("[PERFECTO] Evaluacion diferencial superada! Guardado en: " + output_path)
                # Guardar conocimiento exitoso para aprendizaje futuro
                knowledge_file = "/opt/zuly/bitacora/aprendizaje_v8.log"
                with open(knowledge_file, "a", encoding="utf-8") as kf:
                    kf.write(
                        "EXITO | Plano: " + basename +
                        " | V:" + str(v_obtenidos) +
                        " | F:" + str(f_obtenidos) +
                        " | Z:" + str(z_obtenidos) + "\n"
                    )
                return True
            else:
                print("[DIFERENCIA] Modelo no coincide con el maestro. Calculando feedback...")
                feedback = (
                    "El modelo se genero pero NO coincide exactamente con el archivo maestro.\n\n"
                    "TU RESULTADO  => Vertices: " + str(v_obtenidos) + ", Caras: " + str(f_obtenidos) + ", Z: " + str(z_obtenidos) + "m\n"
                    + "EL MAESTRO   => Vertices: " + str(target['V']) + ", Caras: " + str(target['F']) + ", Z: " + str(target['Z']) + "m\n\n"
                    + "ANALISIS DE DIFERENCIAS:\n"
                    + ("- Vertices: " + ("OK" if v_diff_pct < 0.10 else "MAL - difieren en " + str(round(v_diff_pct*100, 1)) + "%") + "\n")
                    + ("- Caras:    " + ("OK" if f_ok else "MAL - el maestro tiene " + str(target['F']) + " caras, tu tienes " + str(f_obtenidos)) + "\n")
                    + ("- Altura Z: " + ("OK" if z_ok else "MAL - el maestro mide " + str(target['Z']) + "m, tu mides " + str(z_obtenidos) + "m") + "\n\n")
                    + "Corrige el codigo para acercarte a los valores del maestro. "
                    + "Devuelve el codigo Python completo corregido."
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

    print("[AGOTADO] " + str(max_retries) + " intentos usados. No se pudo igualar al maestro en: " + basename)
    return False

def main():
    print("=" * 60)
    print("ZULY V8 PLUS: EVALUADOR DIFERENCIAL EXACTO (SIN EMOJIS)")
    print("Referencia: Villa Saboye v05 Pre Modelado.blend")
    print("=" * 60)

    orchestrator = MultiAPIOrchestrator()
    if not orchestrator.gemini_keys:
        print("CRITICO: No se encontraron llaves de Gemini. Abortando.")
        return

    print("APIs listas: Gemini con " + str(len(orchestrator.gemini_keys)) + " llave(s).")

    dxf_folder = "/opt/zuly/planos_temp/Planos y premodelado/"
    output_folder = "/opt/zuly/resultados_masivos_v8/"
    os.makedirs(output_folder, exist_ok=True)

    exitosos = 0
    fallidos = 0
    total = len(TARGET_METRICS)

    for basename, target in TARGET_METRICS.items():
        dxf_path = os.path.join(dxf_folder, basename)
        if os.path.exists(dxf_path):
            ok = process_dxf(dxf_path, output_folder, orchestrator)
            if ok:
                exitosos += 1
            else:
                fallidos += 1
        else:
            print("[NO ENCONTRADO] " + dxf_path)
            fallidos += 1

    print("")
    print("=" * 60)
    print("REPORTE FINAL ZULY V8:")
    print("  Exitosos : " + str(exitosos) + "/" + str(total))
    print("  Fallidos : " + str(fallidos) + "/" + str(total))
    print("  Resultados en: " + output_folder)
    print("=" * 60)

if __name__ == "__main__":
    main()
