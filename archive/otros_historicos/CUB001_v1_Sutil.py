#!/usr/bin/env python3
"""
CUB-001_v1 - VARIACIÓN "SUTIL" (Mínima)
Bisel casi imperceptible, material blanco mate
"""

import bpy
import sys

def ejecutar():
    print("="*60)
    print("🔧 CUB-001_v1: Bisel Sutil (Mínimo)")
    print("="*60)
    
    # RESET
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for mat in bpy.data.materials:
        bpy.data.materials.remove(mat)
    
    # Crear cubo
    bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 1))
    cubo = bpy.context.active_object
    cubo.name = "CUB001_v1_Sutil"
    
    # Aplicar escala
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
    # BEVEL SUTIL: width 0.01, segments 2
    bevel = cubo.modifiers.new(name="Bevel_Sutil", type='BEVEL')
    bevel.width = 0.01
    bevel.segments = 2
    bevel.limit_method = 'ANGLE'
    bevel.angle_limit = 0.5236
    
    # AUTO SMOOTH 30°
    cubo.data.use_auto_smooth = True
    cubo.data.auto_smooth_angle = 0.5236
    
    # MATERIAL BLANCO MATE (roughness 0.8)
    mat = bpy.data.materials.new(name="Mat_v1_BlancoMate")
    mat.use_nodes = True
    principled = mat.node_tree.nodes.get("Principled BSDF")
    if principled:
        principled.inputs['Base Color'].default_value = (0.95, 0.95, 0.95, 1.0)
        principled.inputs['Roughness'].default_value = 0.8
        principled.inputs['Specular'].default_value = 0.2
    cubo.data.materials.append(mat)
    
    # ILUMINACIÓN
    bpy.ops.object.light_add(type='SUN', location=(5, 5, 10))
    key = bpy.context.active_object
    key.name = "Key_Light_v1"
    key.data.energy = 4.0
    
    bpy.ops.object.light_add(type='AREA', location=(-5, 2, 5))
    fill = bpy.context.active_object
    fill.name = "Fill_Light_v1"
    fill.data.energy = 1.5
    
    # CÁMARA
    bpy.ops.object.camera_add(location=(3, -3, 2.5))
    cam = bpy.context.active_object
    cam.name = "Camera_v1"
    direction = cubo.location - cam.location
    cam.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
    bpy.context.scene.camera = cam
    
    # RENDER
    bpy.context.scene.render.engine = 'BLENDER_EEVEE'
    bpy.context.scene.render.resolution_x = 1920
    bpy.context.scene.render.resolution_y = 1080
    bpy.context.scene.render.filepath = "./ZULY_PROJECTS/CUB001_v1_preview.png"
    
    # GUARDAR
    bpy.ops.wm.save_as_mainfile(filepath="./ZULY_PROJECTS/CUB001_v1_Sutil.blend")
    
    # RENDERIZAR
    bpy.ops.render.render(write_still=True)
    
    print("✅ CUB-001_v1 completado")
    return True

if __name__ == "__main__":
    try:
        ejecutar()
    except Exception as e:
        print(f"❌ ERROR: {e}")
        sys.exit(1)
