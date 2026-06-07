import bpy
import sys
import os
import json

# Agregar el directorio del proyecto al path para importar core
sys.path.insert(0, r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL")

from core.agent import Agent
from core.utils.logging import log_info, log_success, log_error

def run_lab_test():
    log_info("=== INICIANDO PRUEBA REAL: ZULY LAB - INGENIERÍA INVERSA ===")
    
    # Limpiar escena actual por seguridad
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    # Cargar modelo de ejemplo
    blend_path = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\ZULY_PROJECTS\ejemplos\casarural.blend"
    if not os.path.exists(blend_path):
        log_error(f"Fallo: El archivo {blend_path} no existe.")
        return

    try:
        bpy.ops.wm.open_mainfile(filepath=blend_path)
        log_success(f"Modelo cargado correctamente: {blend_path}")
    except Exception as e:
        log_error(f"Error cargando archivo .blend: {e}")
        return

    # Inicializar Agente con motor real
    # force_mock=False asegura que use BlenderAdapter
    agent = Agent(force_mock=False)

    # Identificar objetos para escanear
    objetos = [obj.name for obj in bpy.data.objects if obj.type == 'MESH']
    log_info(f"Objetos detectados para escaneo: {objetos}")

    # Ejecutar Escaneo y Aprendizaje
    log_info("Invocando 'blender.scan_and_learn'...")
    output_name = "adn_casa_rural_v1"
    
    # Ejecutar vía router para validar el flujo completo
    result = agent.execute_via_router('blender.scan_and_learn', {
        'output_name': output_name
    })

    if result.get('success'):
        saved_path = result.get('saved_path')
        log_success(f"¡ÉXITO! Ingeniería Inversa completada.")
        log_info(f"ADN extraído y guardado en: {saved_path}")
        
        # Verificar contenido básico
        if os.path.exists(saved_path):
            with open(saved_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                num_obj = len(data.get('objects', []))
                log_info(f"Verificación de ADN: Se extrajeron {num_obj} definiciones de mallas.")
                
                # Listar algunos nombres extraídos
                nombres = [o['name'] for o in data['objects']]
                log_info(f"Mallas en el ADN: {nombres}")
    else:
        log_error(f"FALLO en ZULY LAB: {result.get('error')}")

    log_info("=== FIN DE PRUEBA REAL ===")

if __name__ == "__main__":
    run_lab_test()
