import bpy
import os
path = r'C:\Users\Admin\Desktop\ZULY_IA_LOCAL\ZULY_PROJECTS\test_real_binario.blend'
bpy.ops.mesh.primitive_cube_add()
bpy.ops.wm.save_as_mainfile(filepath=path)
print(f'ARCHIVO CREADO: {os.path.exists(path)}')
print(f'TAMANO: {os.path.getsize(path)}')
