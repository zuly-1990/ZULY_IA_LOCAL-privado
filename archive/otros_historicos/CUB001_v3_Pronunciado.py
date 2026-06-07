#!/usr/bin/env python3
"""
CUB-001_v3 - VARIACIÓN "PRONUNCIADO" (Máximo seguro)
Bisel grande, cubo más grande, material metal plateado
"""

import bpy
import sys

def ejecutar():
    print("="*60)
    print("🔧 CUB-001_v3: Bisel Pronunciado + Metal")
    print("="*60)
    
    # RESET
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for mat in bpy.data.materials:
        bpy.data.materials.remove(mat)
    
    # Crear cubo MÁS GRANDE (size 3)
    bpy.ops.mesh.primitive_cube_add(size=3, location=(0, 0, 1.5))
    cubo = bpy.context.active_object
    cubo.name = "CUB001_v3_Pronunciado"
    
    # Aplicar escala
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
    # BEVEL PRONUNCIADO: width 0.15, segments 5
    bevel = cubo.modifiers.new(name="Bevel_Pronunciado", type='BEVEL')
    bevel.width = 0.15
    bevel.segments = 5
    bevel.limit_method = 'ANGLE'
    bevel.angle_limit = 0.5236
    
    # AUTO SMOOTH 45° (más suave)
    cubo.data.use_auto_smooth = True
    cubo.data.auto_smooth_angle = 0.7854  # 45 grados
    
    # MATERIAL METAL PLATEADO (metallic 0.9, roughness 0.2)
    mat = bpy.data.materials.new(name="Mat_v3_MetalPlateado")
    mat.use_nodes = True
    principled = mat.node_tree.nodes.get("Principled BSDF")
    if principled:
        principled.inputs['Base Color'].default_value = (0.8, 0.85, 0.9, 1.0)
        principled.inputs['Metallic'].default_value = 0.9
        principled.inputs['Roughness'].default_value = 0.2
        principled.inputs['Specular'].default_value = 0.8
    cubo.data.materials.append(mat)
    
    # ILUMINACIÓN (más fuerte para metal)
    bpy.ops.object.light_add(type='SUN', location=(5, 5, 10))
    key = bpy.context.active_object
    key.name = "Key_Light_v3"
    key.data.energy = 6.0
    
    bpy.ops.object.light_add(type='AREA', location=(-5, 2, 5))
    fill = bpy.context.active_object
    fill.name = "Fill_Light_v3"
    fill.data.energy = 2.5
    
    # CÁMARA
    bpy.ops.object.camera_add(location=(4, -4, 3))
    cam = bpy.context.active_object
    cam.name = "Camera_v3"
    direction = cubo.location - cam.location
    cam.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
    bpy.context.scene.camera = cam
    
    # RENDER
    bpy.context.scene.render.engine = 'BLENDER_EEVEE'
    bpy.context.scene.render.resolution_x = 1920
    bpy.context.scene.render.resolution_y = 1080
    bpy.context.scene.render.filepath = "./ZULY_PROJECTS/CUB001_v3_preview.png"
    
    # GUARDAR
    bpy.ops.wm.save_as_mainfile(filepath="./ZULY_PROJECTS/CUB001_v3_Pronunciado.blend")
    
    # RENDERIZAR
    bpy.ops.render.render(write_still=True)
    
    print("✅ CUB-001_v3 completado")
    return True

if __name__ == "__main__":
    try:
        ejecutar()
    except Exception as e:
        print(f"❌ ERROR: {e}")
        sys.exit(1)
