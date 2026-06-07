
import os
import json
import sys
import time

# Agregar el path del proyecto para importar core
sys.path.append('C:\\Users\\Admin\\Desktop\\ZULY_IA_LOCAL')

from lyzu_core import LYZUCore
from core.adapters.blender_adapter import BlenderAdapter
from core.utils.logging import log_info, log_success, log_error

def run_synthesis():
    log_info("--- Iniciando S\u00edntesis Arquitect\u00f3nica Urbana (v1) ---")
    
    # Cargar ADN
    pattern_path = "C:\\Users\\Admin\\Desktop\\ZULY_IA_LOCAL\\knowledge_base\\patterns\\learned\\pattern_edificio_2.json"
    if not os.path.exists(pattern_path):
        log_error(f"Falta el archivo de ADN: {pattern_path}")
        return
        
    with open(pattern_path, 'r') as f:
        adn = json.load(f)
    
    # Inicializar componentes
    adapter = BlenderAdapter()
    if not adapter.is_available():
        log_error("Blender no disponible en el script")
        return
        
    # Limpiar escena
    adapter.clear_scene()
    
    # 1. Crear Materiales Premium
    adapter.create_material("Cristal_Fachada", color=(0.1, 0.2, 0.5), metallic=0.9, roughness=0.1)
    adapter.create_material("Hormigon_Estructura", color=(0.4, 0.4, 0.4), roughness=0.8)
    
    # 2. Reconstrucci\u00f3n selectiva del ADN (Mapeo de objetos clave)
    # Filtramos para evitar saturar la escena con los 175 objetos si son repetitivos
    # pero para esta demo, intentaremos una reconstrucci\u00f3n estructurada.
    
    created_map = {} # Original Name -> New Name
    
    # Ordenar objetos por jerarqu\u00eda (padres primero)
    objects = adn.get('objects', [])
    # (En una versi\u00f3n robusta har\u00edamos un grafo, aqu\u00ed asumimos orden razonable o lo resolvemos)
    
    for obj_data in objects:
        name = obj_data['name']
        type = obj_data['type']
        loc = obj_data['location']
        rot = obj_data['rotation']
        scale = obj_data['scale']
        
        # Mapeo de tipos (ZULY interpreta MESH de Blender)
        # Para esta demo usaremos primitivas equivalentes o crearemos mallas si es necesario
        prim_type = 'cube'
        if 'Circle' in name:
            prim_type = 'cylinder'
        elif 'Plane' in name:
            prim_type = 'plane'
            
        # Crear objeto
        res = adapter.create_primitive(
            prim_type,
            name=f"Synthesized_{name}",
            location=loc,
            scale=scale
        )
        
        if res.get('success'):
            new_name = res.get('object_name')
            created_map[name] = new_name
            
            # Aplicar rotaci\u00f3n
            adapter.rotate_object(new_name, rot)
            
            # Aplicar Modificadores
            for mod in obj_data.get('modifiers', []):
                mod_type = mod['type']
                params = {}
                if mod_type == 'ARRAY':
                    params['count'] = mod.get('count', 2)
                    # Inferimos offset vertical si es un edificio alto
                    params['offset_z'] = 1.1 
                elif mod_type == 'SUBSURF':
                    params['levels'] = mod.get('levels', 1)
                elif mod_type == 'MIRROR':
                    pass # Mirror b\u00e1sico
                
                adapter.add_modifier(new_name, mod_type, **params)
            
            # Aplicar materiales seg\u00fan nombre
            if 'Circle' in name:
                adapter.apply_material(new_name, "Cristal_Fachada")
            else:
                adapter.apply_material(new_name, "Hormigon_Estructura")
    
    # 3. Guardar Prototipo
    output_path = "C:\\Users\\Admin\\Desktop\\ZULY_IA_LOCAL\\ZULY_PROJECTS\\laboratorio\\urban_synthesis_alpha.blend"
    adapter.export_scene(format='BLEND', output_path=output_path)
    
    log_success(f"--- S\u00edntesis Completada: {output_path} ---")

if __name__ == "__main__":
    run_synthesis()
