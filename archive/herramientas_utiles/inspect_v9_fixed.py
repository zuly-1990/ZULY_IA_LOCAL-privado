import bpy
import mathutils

bpy.ops.wm.open_mainfile(filepath='/opt/zuly/Villa_Savoye_V9_Modelado3D.blend')

for name in ["Primer Nivel", "Segundo Nivel", "Tercer Nivel"]:
    obj = bpy.data.objects.get(name)
    if obj:
        bbox = [obj.matrix_world @ mathutils.Vector(v) for v in obj.bound_box]
        min_z = min(v.z for v in bbox)
        max_z = max(v.z for v in bbox)
        print(f"[{name}] Z Min: {min_z:.4f}, Z Max: {max_z:.4f}")
