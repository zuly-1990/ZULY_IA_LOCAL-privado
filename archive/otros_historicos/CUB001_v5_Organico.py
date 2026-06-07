#!/usr/bin/env python3
"""
CUB-001_v5 - VARIACIÓN "ORGÁNICO" (Suavizado)
Subsurf para forma orgánica, material plástico brillante azul
"""

import bpy
import sys

def ejecutar():
    print("="*60)
    print("🔧 CUB-001_v5: Orgánico Suavizado + Plástico Brillante")
    print("="*60)
    
    # RESET
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for mat in bpy.data.materials:
        bpy.data.materials.remove(mat)
    
    # Crear cubo MÁS GRANDE (size 2.5)
    bpy.ops.mesh.primitive_cube_add(size=2.5, location=(0, 0, 1.25))
    cubo = bpy.context.active_object
    cubo.name = "CUB001_v5_Organico"
    
    # Aplicar escala
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
    # BEVEL: width 0.08, segments 6 (muy suave)
    bevel = cubo.modifiers.new(name="Bevel_Organico", type='BEVEL')
    bevel.width = 0.08
    bevel.segments = 6
    bevel.limit_method = 'ANGLE'
    bevel.angle_limit = 0.5236
    
    # SUBSURF (Subdivision Surface) - 2 niveles
    subsurf = cubo.modifiers.new(name="Subsurf_Suavizado", type='SUBSURF')
    subsurf.levels = 2
    subsurf.render_levels = 2
    subsurf.subdivision_type = 'CATMULL_CLARK'
    
    # AUTO SMOOTH 60° (más permisivo para orgánico)
    cubo.data.use_auto_smooth = True
    cubo.data.auto_smooth_angle = 1.0472  # 60 grados
    
    # MATERIAL PLÁSTICO BRILLANTE AZUL (roughness 0.1)
    mat = bpy.data.materials.new(name="Mat_v5_PlasticoAzul")
    mat.use_nodes = True
    principled = mat.node_tree.nodes.get("Principled BSDF")
    if principled:
        principled.inputs['Base Color'].default_value = (0.1, 0.4, 0.9, 1.0)  # Azul
        principled.inputs['Roughness'].default_value = 0.1  # Brillante
        principled.inputs['Specular'].default_value = 0.7
        principled.inputs['Clearcoat'].default_value = 0.5  # Efecto barniz
    cubo.data.materials.append(mat)
    
    # ILUMINACIÓN SUAVE (para plástico brillante)
    bpy.ops.object.light_add(type='AREA', location=(4, 4, 6))
    key = bpy.context.active_object
    key.name = "Key_Light_v5"
    key.data.energy = 3.5
    key.data.color = (1.0, 0.95, 0.9)  # Cálida
    key.scale = (4, 4, 4)  # Tamaño de la luz área
    
    bpy.ops.object.light_add(type='AREA', location=(-4, 3, 4))
    fill = bpy.context.active_object
    fill.name = "Fill_Light_v5"
    fill.data.energy = 2.0
    fill.scale = (3, 3, 3)
    
    bpy.ops.object.light_add(type='AREA', location=(0, -4, 3))
    rim = bpy.context.active_object
    rim.name = "Rim_Light_v5"
    rim.data.energy = 1.5
    rim.scale = (2, 2, 2)
    
    # CÁMARA
    bpy.ops.object.camera_add(location=(3.5, -3.5, 2.5))
    cam = bpy.context.active_object
    cam.name = "Camera_v5"
    direction = cubo.location - cam.location
    cam.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
    bpy.context.scene.camera = cam
    
    # RENDER
    bpy.context.scene.render.engine = 'BLENDER_EEVEE'
    bpy.context.scene.render.resolution_x = 1920
    bpy.context.scene.render.resolution_y = 1080
    bpy.context.scene.render.filepath = "./ZULY_PROJECTS/CUB001_v5_preview.png"
    
    # GUARDAR
    bpy.ops.wm.save_as_mainfile(filepath="./ZULY_PROJECTS/CUB001_v5_Organico.blend")
    
    # RENDERIZAR
    bpy.ops.render.render(write_still=True)
    
    print("✅ CUB-001_v5 completado")
    return True

if __name__ == "__main__":
    try:
        ejecutar()
    except Exception as e:
        print(f"❌ ERROR: {e}")
        sys.exit(1)
