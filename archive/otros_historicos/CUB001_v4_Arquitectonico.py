#!/usr/bin/env python3
"""
CUB-001_v4 - VARIACIÓN "ARQUITECTÓNICO" (Muro)
Proporción de muro: ancho 4, alto 2, profundo 0.5
Material concreto gris oscuro
"""

import bpy
import sys

def ejecutar():
    print("="*60)
    print("🔧 CUB-001_v4: Muro Arquitectónico")
    print("="*60)
    
    # RESET
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for mat in bpy.data.materials:
        bpy.data.materials.remove(mat)
    
    # Crear cubo con ESCALA DE MURO (no size uniforme)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 1))
    cubo = bpy.context.active_object
    cubo.name = "CUB001_v4_Muro"
    
    # Aplicar escala DE MURO: ancho 4, alto 2, profundo 0.5
    cubo.scale = (4.0, 0.5, 2.0)  # X=ancho, Y=profundo, Z=alto
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
    # BEVEL ARQUITECTÓNICO: width 0.03 (sutil), segments 4 (suave)
    bevel = cubo.modifiers.new(name="Bevel_Muro", type='BEVEL')
    bevel.width = 0.03
    bevel.segments = 4
    bevel.limit_method = 'ANGLE'
    bevel.angle_limit = 0.5236
    
    # AUTO SMOOTH 30°
    cubo.data.use_auto_smooth = True
    cubo.data.auto_smooth_angle = 0.5236
    
    # MATERIAL CONCRETO GRIS OSCURO (roughness 0.9)
    mat = bpy.data.materials.new(name="Mat_v4_Concreto")
    mat.use_nodes = True
    principled = mat.node_tree.nodes.get("Principled BSDF")
    if principled:
        principled.inputs['Base Color'].default_value = (0.25, 0.25, 0.27, 1.0)
        principled.inputs['Roughness'].default_value = 0.9
        principled.inputs['Specular'].default_value = 0.1
    cubo.data.materials.append(mat)
    
    # SUELO (plano) para contexto arquitectónico
    bpy.ops.mesh.primitive_plane_add(size=20, location=(0, 0, 0))
    suelo = bpy.context.active_object
    suelo.name = "Suelo_Contexto"
    
    mat_suelo = bpy.data.materials.new(name="Mat_Suelo")
    mat_suelo.use_nodes = True
    principled_suelo = mat_suelo.node_tree.nodes.get("Principled BSDF")
    if principled_suelo:
        principled_suelo.inputs['Base Color'].default_value = (0.15, 0.15, 0.15, 1.0)
        principled_suelo.inputs['Roughness'].default_value = 1.0
    suelo.data.materials.append(mat_suelo)
    
    # ILUMINACIÓN ARQUITECTÓNICA
    bpy.ops.object.light_add(type='SUN', location=(8, 8, 15))
    key = bpy.context.active_object
    key.name = "Key_Light_v4"
    key.data.energy = 4.5
    
    bpy.ops.object.light_add(type='AREA', location=(-8, 4, 8))
    fill = bpy.context.active_object
    fill.name = "Fill_Light_v4"
    fill.data.energy = 2.0
    
    # CÁMARA (vista frontal del muro)
    bpy.ops.object.camera_add(location=(0, -8, 2))
    cam = bpy.context.active_object
    cam.name = "Camera_v4"
    direction = cubo.location - cam.location
    cam.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
    bpy.context.scene.camera = cam
    
    # RENDER
    bpy.context.scene.render.engine = 'BLENDER_EEVEE'
    bpy.context.scene.render.resolution_x = 1920
    bpy.context.scene.render.resolution_y = 1080
    bpy.context.scene.render.filepath = "./ZULY_PROJECTS/CUB001_v4_preview.png"
    
    # GUARDAR
    bpy.ops.wm.save_as_mainfile(filepath="./ZULY_PROJECTS/CUB001_v4_Arquitectonico.blend")
    
    # RENDERIZAR
    bpy.ops.render.render(write_still=True)
    
    print("✅ CUB-001_v4 completado")
    return True

if __name__ == "__main__":
    try:
        ejecutar()
    except Exception as e:
        print(f"❌ ERROR: {e}")
        sys.exit(1)
