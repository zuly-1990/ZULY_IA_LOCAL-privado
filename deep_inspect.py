import bpy
import json

def deep_inspect():
    data = {"collections": [], "objects": [], "node_groups": []}
    
    # Inspeccionar colecciones
    for coll in bpy.data.collections:
        data["collections"].append(coll.name)
        
    # Inspeccionar todos los objetos (incluyendo los ocultos o no en escena)
    for obj in bpy.data.objects:
        obj_data = {
            "name": obj.name,
            "type": obj.type,
            "modifiers": [m.type for m in obj.modifiers],
            "location": list(obj.location),
            "dimensions": list(obj.dimensions) if hasattr(obj, 'dimensions') else []
        }
        if obj.type == 'MESH' and obj.data:
            obj_data["vertices"] = len(obj.data.vertices)
        data["objects"].append(obj_data)
        
    # Inspeccionar grupos de nodos
    for ng in bpy.data.node_groups:
        data["node_groups"].append({
            "name": ng.name,
            "type": ng.type,
            "nodes_count": len(ng.nodes)
        })
        
    print("ZULY_DEEP_INSPECT:" + json.dumps(data))

deep_inspect()
