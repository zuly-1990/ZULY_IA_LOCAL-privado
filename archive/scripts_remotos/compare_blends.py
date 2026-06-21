import subprocess, json, tempfile, os

BLENDER = '/usr/local/bin/blender'
BLEND_V05 = '/opt/zuly/planos_temp/Planos y premodelado/Villa Saboye v05 Pre Modelado.blend'
BLEND_V09 = '/opt/zuly/resultados_masivos_v9/Villa_Savoye_V9_Modelado3D_intento_4.blend'

inspect_script = '''
import bpy, json

data = {
    "objects": [],
    "node_groups": []
}

for obj in bpy.data.objects:
    obj_data = {
        "name": obj.name,
        "type": obj.type,
        "location": [round(v, 4) for v in obj.location],
        "scale": [round(v, 4) for v in obj.scale],
        "dimensions": [round(v, 4) for v in obj.dimensions] if hasattr(obj, 'dimensions') else None,
        "modifiers": [m.type for m in obj.modifiers] if obj.type == 'MESH' else [],
        "vertices": len(obj.data.vertices) if obj.type == 'MESH' and obj.data else 0,
        "polygons": len(obj.data.polygons) if obj.type == 'MESH' and obj.data else 0
    }
    data["objects"].append(obj_data)

for ng in bpy.data.node_groups:
    data["node_groups"].append({
        "name": ng.name,
        "type": ng.type,
        "nodes": [n.type for n in ng.nodes]
    })

print("ZULY_INSPECT:" + json.dumps(data))
'''

def inspect_blend(blend_path):
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(inspect_script)
        tmp = f.name
    
    result = subprocess.run([BLENDER, blend_path, '--background', '--python', tmp], capture_output=True, text=True)
    os.unlink(tmp)
    
    for line in result.stdout.splitlines():
        if line.startswith("ZULY_INSPECT:"):
            return json.loads(line[13:])
    return {"error": "No data found", "stdout": result.stdout[-500:]}

print("Inspeccionando V05...")
v05_data = inspect_blend(BLEND_V05)
print("Inspeccionando V09...")
v09_data = inspect_blend(BLEND_V09)

report = {
    "v05_pre_modelado": {
        "total_objects": len(v05_data.get("objects", [])),
        "node_groups": len(v05_data.get("node_groups", [])),
        "objects": v05_data.get("objects", [])
    },
    "v09_intento_4": {
        "total_objects": len(v09_data.get("objects", [])),
        "node_groups": len(v09_data.get("node_groups", [])),
        "objects": v09_data.get("objects", []),
        "geometry_nodes": v09_data.get("node_groups", [])
    }
}

with open('/opt/zuly/comparativa_v05_v09.json', 'w') as f:
    json.dump(report, f, indent=2)

print("Comparativa guardada en /opt/zuly/comparativa_v05_v09.json")
