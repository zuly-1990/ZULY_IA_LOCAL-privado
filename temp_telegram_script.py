import bpy
import mathutils
import os

# --- Limpieza inicial de la escena ---
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# --- 1. Importar el archivo DXF ---
dxf_path = "/opt/zuly/Planos y premodelado_extraido/Planos y premodelado/01 Primer Nivel v08.dxf"

# Verificar que el archivo exista
if not os.path.exists(dxf_path):
    print(f"ERROR: El archivo DXF no se encontró en la ruta: {dxf_path}")
else:
    print(f"Importando DXF desde: {dxf_path}")
    bpy.ops.import_scene.dxf(filepath=dxf_path)
    print("Importación completada.")

# --- 2. Seleccionar todas las curvas importadas y convertirlas a malla ---
bpy.ops.object.select_all(action='DESELECT')

# Seleccionar todos los objetos que sean de tipo 'CURVE'
curves_to_convert = [obj for obj in bpy.data.objects if obj.type == 'CURVE']

if not curves_to_convert:
    print("No se encontraron curvas para convertir.")
else:
    print(f"Encontradas {len(curves_to_convert)} curvas. Convirtiendo a malla...")
    # Activar y seleccionar cada curva, convertirla a malla
    for curve in curves_to_convert:
        curve.select_set(True)
        bpy.context.view_layer.objects.active = curve
        bpy.ops.object.convert(target='MESH')
        curve.select_set(False)
    print("Conversión a malla completada.")

# --- 3. Unir todas las mallas en un solo objeto ---
# Seleccionar todos los objetos que ahora son de tipo 'MESH'
bpy.ops.object.select_all(action='DESELECT')
mesh_objects = [obj for obj in bpy.data.objects if obj.type == 'MESH']

if not mesh_objects:
    print("No se encontraron mallas para unir.")
else:
    print(f"Uniendo {len(mesh_objects)} mallas...")
    # Hacer que la primera malla sea el objeto activo y seleccionar todas
    bpy.context.view_layer.objects.active = mesh_objects[0]
    for obj in mesh_objects:
        obj.select_set(True)
    
    # Unir (Join)
    bpy.ops.object.join()
    print("Unión completada.")

    # Renombrar el objeto resultante para claridad
    bpy.context.active_object.name = "Primer_Nivel_Planta"

# --- 4. Entrar en Modo Edición y extruir todo hacia arriba (Z) ---
# Asegurarse de que el objeto activo sea la malla unida
if bpy.context.active_object and bpy.context.active_object.type == 'MESH':
    obj = bpy.context.active_object
    
    # Ir a modo edición y seleccionar todas las caras
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    
    # Extruir a lo largo del eje Z local (que es el global si no hay rotación)
    # La extrusión por defecto sigue el promedio de las normales.
    # Para extruir 3 metros en Z global, usamos el operador 'extrude_region_move'
    print("Extruyendo 3 metros en el eje Z...")
    bpy.ops.mesh.extrude_region_move(
        MESH_OT_extrude_region={
            "use_normal_flip": False,
            "use_dissolve_ortho_edges": False,
            "mirror": False
        },
        TRANSFORM_OT_translate={
            "value": (0, 0, 3.0),  # 3 metros en Z
            "orient_type": 'GLOBAL',
            "orient_matrix": ((1, 0, 0), (0, 1, 0), (0, 0, 1)),
            "orient_matrix_type": 'GLOBAL',
            "constraint_axis": (False, False, True)
        }
    )
    
    # (Opcional) Recalcular normales para que apunten hacia afuera
    bpy.ops.mesh.normals_make_consistent(inside=False)
    
    # Volver al modo objeto
    bpy.ops.object.mode_set(mode='OBJECT')
    print("Extrusión completada.")
else:
    print("No hay un objeto malla activo para extruir.")

# --- 5. ¡GUARDAR EL ARCHIVO! ---
output_path = "/opt/zuly/Primer_Nivel_Extruido.blend"
print(f"Guardando archivo en: {output_path}")
bpy.ops.wm.save_as_mainfile(filepath=output_path)
print("¡Archivo guardado exitosamente! 🎉")