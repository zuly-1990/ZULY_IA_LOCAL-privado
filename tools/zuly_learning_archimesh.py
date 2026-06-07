import bpy
import json
import time
import os

def learn_from_archimesh():
    print("--- ZULY APRENDIENDO DE ARCHIMESH ---")
    
    # 1. Crear una ventana profesional usando Archimesh
    # La API de Archimesh suele estar bajo bpy.ops.archimesh
    try:
        # Crear ventana tipo Rail
        bpy.ops.archimesh.window_panel_add()
        window = bpy.context.active_object
        print(f"Objeto creado por Archimesh: {window.name}")
        
        # 2. Analizar Geometría (Data-Driven)
        # ZULY extrae los datos que hacen que esta ventana sea 'perfecta'
        mesh_data = {
            "vertices_count": len(window.data.vertices),
            "edges_count": len(window.data.edges),
            "polygons_count": len(window.data.polygons),
            "dimensions": list(window.dimensions),
            "location": list(window.location)
        }
        
        # 3. Analizar Estructura de Colecciones
        # Archimesh suele agrupar elementos (marco, cristal, etc)
        hierarchy = []
        if window.type == 'MESH':
            for modifier in window.modifiers:
                hierarchy.append({"modifier_type": modifier.type, "name": modifier.name})
        
        learning_result = {
            "source": "archimesh",
            "feature": "window_panel",
            "timestamp": time.time(),
            "geometric_rules": mesh_data,
            "modifiers_found": hierarchy,
            "jues_compatible": True
        }
        
        print("LEARNING_START")
        print(json.dumps(learning_result))
        print("LEARNING_END")
        
    except Exception as e:
        print(f"ERROR DURANTE EL APRENDIZAJE: {str(e)}")

if __name__ == "__main__":
    learn_from_archimesh()
