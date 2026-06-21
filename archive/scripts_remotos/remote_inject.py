import time
import os
from core.cognition.zuly_memory_rag import ZulyMemoryRAG

print("Ingestando tutorial DXF...")
memoria = ZulyMemoryRAG(db_path="/opt/zuly/bitacora/memory.db")

tutorial = """[TUTORIAL APRENDIDO] Archivo: Guia_DXF_Arquitectura.txt

TUTORIAL MAESTRO DE IMPORTACIÓN Y EXTRUSIÓN DXF EN BLENDER:

Si te piden modelar o levantar paredes basándote en un archivo DXF (ej. desde /opt/zuly/Planos y premodelado_extraido/), usa EXACTAMENTE este código:

```python
import bpy

# 1. Habilitar el Addon oficial de DXF
bpy.ops.preferences.addon_enable(module="io_import_dxf")

# 2. Borrar objetos por defecto
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# 3. Importar el archivo DXF 
ruta_dxf = "/opt/zuly/Planos y premodelado_extraido/Planos y premodelado/01 Primer Nivel v08.dxf"
try:
    bpy.ops.import_scene.dxf(filepath=ruta_dxf)
except Exception as e:
    print(f"Error importando DXF: {e}")

# 4. Los DXF se importan como Curvas. Convertirlas todas a Malla (Mesh)
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.convert(target='MESH')

# 5. Unir todas las mallas en un solo objeto para facilitar la extrusión
bpy.ops.object.join()

# 6. Entrar a Modo Edición, seleccionar todo, y extruir hacia arriba (ej. 3 metros)
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value":(0, 0, 3)})

# 7. Regresar a Modo Objeto
bpy.ops.object.mode_set(mode='OBJECT')

# 8. Guardar
bpy.ops.wm.save_as_mainfile(filepath="/opt/zuly/planos_extruidos.blend")
```
"""

memoria.ingest_experience(int(time.time()), tutorial)
print("¡Tutorial inyectado con éxito!")
