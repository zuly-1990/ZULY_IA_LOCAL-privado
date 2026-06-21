import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("167.233.69.104", username="root", password="ZULY.server.77")

script = """
import time
from core.cognition.zuly_memory_rag import ZulyMemoryRAG
memoria = ZulyMemoryRAG(db_path="/opt/zuly/bitacora/memory.db")

tutorial = '''[TUTORIAL APRENDIDO] Archivo: Guia_DXF_Arquitectura.txt

TUTORIAL MAESTRO DE IMPORTACIÓN Y EXTRUSIÓN DXF EN BLENDER 3.6:

Si el usuario te pide modelar o levantar paredes basándote en un archivo DXF de AutoCAD (por ejemplo, desde /opt/zuly/descargas/), sigue este script EXACTO:

```python
import bpy
import bmesh

# 1. Habilitar el Addon oficial de DXF
bpy.ops.preferences.addon_enable(module="io_import_dxf")

# 2. Borrar objetos por defecto
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# 3. Importar el archivo DXF (cambia la ruta a la que indique el usuario)
ruta_dxf = "/opt/zuly/descargas/archivo.dxf" # REEMPLAZA ESTO
bpy.ops.import_scene.dxf(filepath=ruta_dxf)

# 4. Los DXF se importan como Curvas. Convertirlas todas a Malla (Mesh)
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.convert(target='MESH')

# 5. Unir todas las mallas importadas en un solo objeto para facilitar la extrusión
bpy.ops.object.join()

# 6. Entrar a Modo Edición, seleccionar todo, y extruir hacia arriba (ej. 3 metros)
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value":(0, 0, 3)})

# 7. Regresar a Modo Objeto
bpy.ops.object.mode_set(mode='OBJECT')

# 8. (Opcional) Asignar un material sólido para el renderizado
mat = bpy.data.materials.new(name="Muro_Blanco")
mat.use_nodes = True
bsdf = mat.node_tree.nodes["Principled BSDF"]
bsdf.inputs["Base Color"].default_value = (0.8, 0.8, 0.8, 1)

obj = bpy.context.active_object
if obj.data.materials:
    obj.data.materials[0] = mat
else:
    obj.data.materials.append(mat)
```
Al aplicar este código, las líneas 2D del plano se convertirán mágicamente en paredes 3D de 3 metros de altura.
'''

memoria.ingest_experience(int(time.time()), tutorial)
print("Tutorial DXF inyectado al Hipocampo exitosamente.")
"""

stdin, stdout, stderr = ssh.exec_command(f"export PYTHONPATH=/opt/zuly; python3 -c \"{script}\"")
print(stdout.read().decode())
print(stderr.read().decode())
ssh.close()
