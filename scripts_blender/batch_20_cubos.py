"""
Script para crear 20 archivos .blend con cubos usando Zuly y registrar feedback inteligente.
"""
import sys
import os
import subprocess
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.dialog import parse_user_input
from core.diagnostics.diagnostics import validate_params
from core.commands.blender_commands import execute_blender_action
from core.learning_feedback import FeedbackLogger

logger = FeedbackLogger()
blender_path = "blender/v3/blender-3.6.0-zuly/blender.exe"
export_dir = "export/cubos_batch/"
os.makedirs(export_dir, exist_ok=True)

for i in range(1, 21):
    orden = f"crea un cubo rojo"
    params = parse_user_input(orden)
    params['count'] = 1
    valido, advertencias = validate_params(params)
    params['advertencias'] = advertencias
    resultado = "ok" if valido else "error"
    sugerencia = advertencias[0] if advertencias else None
    logger.log(orden, params.get('intent'), params, resultado, sugerencia)
    # Ejecutar Blender para cada cubo
    blend_path = os.path.join(export_dir, f"cubo_zuly_{i}.blend")
    cmd = [
        blender_path,
        "--background",
        "--python-expr",
        f"import bpy; bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False); bpy.ops.mesh.primitive_cube_add(location=(0,0,0), size=2); bpy.ops.wm.save_as_mainfile(filepath='{blend_path}')"
    ]
    try:
        subprocess.run(cmd, check=True)
        print(f"✅ Cubo {i} creado y guardado en {blend_path}")
    except Exception as e:
        print(f"❌ Error en cubo {i}: {e}")
