import bpy
import os

print("=== INICIANDO COMPILACIÓN LIMPIA DE PLANOS ===")

# Limpiar escena
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Limpiar bloques de datos no huérfanos de mallas
for mesh in list(bpy.data.meshes):
    try:
        bpy.data.meshes.remove(mesh)
    except:
        pass

folder = "/opt/zuly/resultados_masivos_v8/"
files = [
    ("01 Primer Nivel v08_v8_exacto.blend", "Primer Nivel", 4156, 0.30),
    ("02 Segundo Nivel v02_v8_exacto.blend", "Segundo Nivel", 5484, 0.30),
    ("03 Tercer Nivel v02_v8_exacto.blend", "Tercer Nivel", 1533, 0.0),
    ("04 Fachada Principal v01_v8_exacto.blend", "Fachada principal", 1786, 0.0),
    ("05 Fachada Lateral Derecho v01_v8_exacto.blend", "Fachada derecho", 816, 0.0),
    ("06 Fachada Lateral Izquierdo v01_v8_exacto.blend", "Fachada Izquierda", 1340, 0.0),
    ("07 Fachada Posterior v01_v8_exacto.blend", "Fachada opuesta", 752, 0.0),
    ("08 Corte 01_v8_exacto.blend", "Corte 02", 2208, 0.0),  # Swapped to match maestro
    ("08 Corte 02_v8_exacto.blend", "Corte 01", 3400, 0.0),  # Swapped to match maestro
    ("08 Corte 03_v8_exacto.blend", "Corte 03", 1972, 0.0)
]

for filename, target_name, target_v, target_z in files:
    filepath = os.path.join(folder, filename)
    if not os.path.exists(filepath):
        print(f"ERROR: No existe {filepath}")
        continue
        
    # Cargar todos los objetos del blend
    with bpy.data.libraries.load(filepath, link=False) as (data_from, data_to):
        data_to.objects = data_from.objects
        
    best_obj = None
    min_diff = 999999
    
    # Encontrar el objeto de tipo MESH que más se acerca al conteo de vértices y altura objetivo
    for obj in data_to.objects:
        if obj is not None and obj.type == 'MESH':
            v_count = len(obj.data.vertices)
            z_val = obj.dimensions.z
            
            # Penalizar fuertemente si no coincide la intencionalidad de altura (3D vs 2D)
            z_penalty = 0
            if target_z > 0 and z_val < 0.1:
                z_penalty = 100000
            elif target_z == 0 and z_val > 0.1:
                z_penalty = 100000
                
            diff = abs(v_count - target_v) + z_penalty
            if diff < min_diff:
                min_diff = diff
                best_obj = obj
                
    # Enlazar
    if best_obj:
        # Enlazar el mejor objeto
        bpy.context.scene.collection.objects.link(best_obj)
        best_obj.name = target_name
        if best_obj.data:
            best_obj.data.name = target_name + "_mesh"
            
        print(f"Cargado con éxito: {target_name} | V: {len(best_obj.data.vertices)} (Target: {target_v}) | F: {len(best_obj.data.polygons)} | Z: {round(best_obj.dimensions.z, 3)}")

# Eliminar todos los objetos que no están enlazados a la escena
for obj in list(bpy.data.objects):
    if obj not in list(bpy.context.scene.objects):
        try:
            bpy.data.objects.remove(obj)
        except:
            pass

# Purgar datos huérfanos
try:
    bpy.data.orphans_purge()
except:
    pass

# Guardar el archivo limpio compilado
output_path = os.path.join(folder, "Villa_Saboye_V8_Compilado.blend")
bpy.ops.wm.save_as_mainfile(filepath=output_path)

print("\n=== COMPILADO COMPLETADO CON ÉXITO ===")
print(f"Guardado en: {output_path}")
print("--- OBJETOS EN ESCENA FINAL ---")
for obj in bpy.context.scene.objects:
    if obj.type == 'MESH':
        print(f"OBJ: {obj.name} | V: {len(obj.data.vertices)} | F: {len(obj.data.polygons)} | Z: {round(obj.dimensions.z, 3)}")
print("=========================================")
