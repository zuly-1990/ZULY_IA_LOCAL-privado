import bpy
import os
path = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\ZULY_LAB\resultados_zuly\zuly_cli_resultado_primitivas.blend"
if os.path.exists(path):
    bpy.ops.wm.open_mainfile(filepath=path)
    # Buscar cualquier objeto que empiece por ZULY
    zuly_objs = [o for o in bpy.data.objects if "ZULY" in o.name]
    if zuly_objs:
        for obj in zuly_objs:
            print(f"VERIFY: {obj.name} | Verts: {len(obj.data.vertices)} | Faces: {len(obj.data.polygons)}")
    else:
        print("VERIFY: No ZULY objects found.")
else:
    print(f"VERIFY: File not found at {path}")
