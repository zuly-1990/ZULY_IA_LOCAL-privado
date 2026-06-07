import bpy
import sys
import os
import json

# Agregar el directorio del proyecto al path
sys.path.insert(0, r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL")

from core.agent import Agent
from core.utils.logging import log_info, log_success, log_error, log_warning

def run_topology_test():
    log_info("=== INICIANDO AUDITORÍA V3: ZULY LAB ===")
    
    # Cargar modelo de ejemplo
    blend_path = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\ZULY_PROJECTS\ejemplos\casarural.blend"
    if not os.path.exists(blend_path):
        log_error(f"Fallo: El archivo {blend_path} no existe.")
        return

    try:
        bpy.ops.wm.open_mainfile(filepath=blend_path)
        log_success(f"Modelo cargado para auditoría: {blend_path}")
    except Exception as e:
        log_error(f"Error cargando archivo .blend: {e}")
        return

    # Inicializar Agente con motor real
    agent = Agent(force_mock=False)

    # Identificar un objeto para auditar
    meshes = [obj.name for obj in bpy.data.objects if obj.type == 'MESH']
    if not meshes:
        log_error("No se encontraron mallas en la escena para auditar.")
        return
        
    # Usar el primer objeto encontrado
    object_name = meshes[0]
    log_info(f"Objeto seleccionado para Auditoría V3: {object_name}")

    # Ejecutar Auditoría vía Router
    result = agent.execute_via_router('blender.validate_topology', {
        'object_name': object_name
    })

    if result.get('success'):
        metrics = result.get('metrics', {})
        log_success(f"V3 Audit exitosa para '{object_name}'")
        
        # Imprimir resultados formateados para el log
        print(f"METRIC_WATERTIGHT: {metrics.get('is_watertight')}")
        print(f"METRIC_NON_MANIFOLD: {metrics.get('non_manifold_edges_count')}")
        print(f"METRIC_VERTS: {metrics.get('total_vertices')}")
        print(f"METRIC_FACES: {metrics.get('total_faces')}")
        
        if metrics.get('is_watertight'):
            log_success("Resultado: Malla técnica perfecta (Watertight).")
        else:
            log_warning(f"Resultado: Malla con problemas topológicos ({metrics.get('non_manifold_edges_count')} bordes abiertos).")
            
        # GUARDAR RESULTADOS EN JSON PARA AGENTE
        with open(r'scripts\topology_result.json', 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=4)
            log_info("Resultados exportados a scripts/topology_result.json")
    else:
        log_error(f"Error en el handler de auditoría: {result.get('error')}")

    log_info("=== FIN DE AUDITORÍA V3 ===")

if __name__ == "__main__":
    run_topology_test()
