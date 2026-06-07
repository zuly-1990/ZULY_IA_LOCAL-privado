
import bpy
import sys
import json
from pathlib import Path

args = sys.argv[sys.argv.index("--") + 1:]
blend_path = args[0]
out_json = args[1]

bpy.ops.wm.read_factory_settings()
bpy.ops.wm.open_mainfile(filepath=blend_path)

meshes = [o for o in bpy.context.scene.objects if o.type == "MESH"]
cameras = [o for o in bpy.context.scene.objects if o.type == "CAMERA"]
lights = [o for o in bpy.context.scene.objects if o.type == "LIGHT"]
materials = list(bpy.data.materials)

# Bounding box world
coords = []
for obj in meshes:
    for v in obj.bound_box:
        world_v = obj.matrix_world @ (obj.scale * obj.location)
        coords.append((v[0], v[1], v[2]))

if coords:
    xs = [c[0] for c in coords]
    ys = [c[1] for c in coords]
    zs = [c[2] for c in coords]
    dims = (round(max(xs)-min(xs), 3), round(max(ys)-min(ys), 3), round(max(zs)-min(zs), 3))
else:
    dims = (0, 0, 0)

verts = sum(len(o.data.vertices) for o in meshes)
edges = sum(len(o.data.edges) for o in meshes)
faces = sum(len(o.data.polygons) for o in meshes)

mats_info = []
for mat in materials:
    col = "#N/A"
    if mat.use_nodes:
        for node in mat.node_tree.nodes:
            if node.type == "BSDF_PRINCIPLED":
                c = node.inputs["Base Color"].default_value
                col = "#" + "{:02x}{:02x}{:02x}".format(int(c[0]*255), int(c[1]*255), int(c[2]*255))
                break
    mats_info.append({"name": mat.name, "color": col})

data = {
    "mesh_objects": len(meshes),
    "cameras": len(cameras),
    "lights": len(lights),
    "materials": len(materials),
    "vertices": verts,
    "edges": edges,
    "faces": faces,
    "dimensions": dims,
    "materials_detail": mats_info,
    "file_size_kb": round(Path(blend_path).stat().st_size / 1024, 1)
}

with open(out_json, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print("[METRICS] Guardado en " + out_json)
