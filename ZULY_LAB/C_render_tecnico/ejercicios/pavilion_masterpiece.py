# pavilion_masterpiece.py
import bpy
import bmesh
import math

def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

def create_modernist_column(location, height=3.0, radius=0.2):
    # Basado en el patrón 'columna_circular_tecnica'
    bpy.ops.mesh.primitive_circle_add(radius=radius, location=location)
    col = bpy.context.object
    col.name = f"Columna_{int(location[0])}_{int(location[1])}"
    
    bpy.ops.object.mode_set(mode='EDIT')
    bm = bmesh.from_edit_mesh(col.data)
    
    # Fill (F) y Extrude (E)
    bmesh.ops.contextual_create(bm, geom=bm.verts)
    # Extruir en Z
    result = bmesh.ops.extrude_face_region(bm, geom=[f for f in bm.faces])
    verts = result['geom']
    for v in verts:
        if isinstance(v, bmesh.types.BMVert):
            v.co.z += height
            
    bmesh.update_edit_mesh(col.data)
    bpy.ops.object.mode_set(mode='OBJECT')
    return col

def create_floor_slab(name, z_location, size=10):
    # Basado en el patrón 'suelo_techo_perimetral' (simulado con vertices)
    bpy.ops.mesh.primitive_plane_add(size=size, location=(0, 0, z_location))
    slab = bpy.context.object
    slab.name = name
    
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value":(0, 0, 0.2)})
    bpy.ops.object.mode_set(mode='OBJECT')
    return slab

def apply_bisect_section():
    # Basado en el patrón 'corte_seccion_tecnico'
    # Seleccionamos todo para el corte global
    bpy.ops.object.select_all(action='SELECT')
    # Protegemos el suelo (no seleccionable en teoría, aquí simplemente lo deseleccionamos)
    if "Suelo_Base" in bpy.data.objects:
        bpy.data.objects["Suelo_Base"].select_set(False)
        
    bpy.ops.object.mode_set(mode='EDIT')
    # Corte transversal a 1.5m de altura para ver el interior
    bpy.ops.mesh.bisect(
        plane_co=(0, 0, 1.5), 
        plane_no=(0, 0, 1), 
        clear_outer=True, 
        clear_inner=False, 
        use_fill=True
    )
    bpy.ops.object.mode_set(mode='OBJECT')

def run_masterpiece():
    clear_scene()
    
    # 1. Suelo Base
    create_floor_slab("Suelo_Base", 0, size=12)
    
    # 2. Retícula de Columnas (Pilotis - Villa Savoye style)
    column_positions = [
        (-4, -4), (0, -4), (4, -4),
        (-4,  0), (0,  0), (4,  0),
        (-4,  4), (0,  4), (4,  4)
    ]
    for pos in column_positions:
        create_modernist_column((pos[0], pos[1], 0.2))
        
    # 3. Losa de Segundo Nivel (Stacking)
    create_floor_slab("Losa_N2", 3.2, size=10)
    
    # 4. Muros del Segundo Nivel (Modernist walls)
    bpy.ops.mesh.primitive_cube_add(scale=(4.8, 0.1, 1.5), location=(0, 4.9, 4.7))
    bpy.ops.mesh.primitive_cube_add(scale=(4.8, 0.1, 1.5), location=(0, -4.9, 4.7))
    bpy.ops.mesh.primitive_cube_add(scale=(0.1, 4.8, 1.5), location=(4.9, 0, 4.7))
    
    # 5. Aplicar Bisección (El "Efecto Wow" para mostrar arquitectura)
    apply_bisect_section()
    
    # Configuración de Cámara para el render
    bpy.ops.object.camera_add(location=(15, -15, 10), rotation=(math.radians(60), 0, math.radians(45)))
    bpy.context.scene.camera = bpy.context.object
    
    # Luz
    bpy.ops.object.light_add(type='SUN', location=(10, 10, 20))
    
    # Render
    output_path = "c:/Users/Admin/Desktop/ZULY_IA_LOCAL/ZULY_LAB/resultados_zuly/pabellon_modernista.png"
    bpy.context.scene.render.filepath = output_path
    bpy.ops.render.render(write_still=True)
    
    print(f"MASTERPIECE_COMPLETE: {output_path}")

# Ejecución Incondicional para ZULY
run_masterpiece()
