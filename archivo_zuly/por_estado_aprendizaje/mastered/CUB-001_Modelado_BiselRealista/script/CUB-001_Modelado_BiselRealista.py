#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🆕 CUB-001_Modelado_BiselRealista
CUB - Cubo con bordes suaves (Bevel) y color azul corporativo #1A4DCC
Generado: 2026-04-04T16:11:10.922719
"""

import bpy
import sys
sys.path.insert(0, 'c:/Users/Admin/Desktop/ZULY_IA_LOCAL/core')
from sistema_luces_inteligente import aplicar_iluminacion_profesional

# Limpiar
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Crear cubo
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 1))
cubo = bpy.context.active_object
cubo.name = "CUB-001_Modelado_BiselRealista"

# Bevel
bevel = cubo.modifiers.new(name="Bevel_Pro", type='BEVEL')
bevel.width = 0.08
bevel.segments = 4
bevel.limit_method = 'ANGLE'
bevel.angle_limit = 0.5236

# Material Azul #1A4DCC
mat = bpy.data.materials.new(name="Mat_Azul_Pro")
mat.use_nodes = True
principled = mat.node_tree.nodes.get("Principled BSDF")
if principled:
    r, g, b = 26/255, 77/255, 204/255  # #1A4DCC
    principled.inputs['Base Color'].default_value = (r, g, b, 1.0)
    principled.inputs['Roughness'].default_value = 0.3
    principled.inputs['Specular'].default_value = 0.7
cubo.data.materials.append(mat)

# Iluminación SLIZ
luces = aplicar_iluminacion_profesional(cubo)

# Cámara
import mathutils
cam_pos = mathutils.Vector((4, -4, 3))
bpy.ops.object.camera_add(location=cam_pos)
cam = bpy.context.active_object
direction = cubo.location - cam.location
cam.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
bpy.context.scene.camera = cam

# Render settings
bpy.context.scene.render.engine = 'BLENDER_EEVEE'
bpy.context.scene.render.resolution_x = 1920
bpy.context.scene.render.resolution_y = 1080

# Guardar
bpy.ops.wm.save_as_mainfile(filepath='./CUB-001_Modelado_BiselRealista.blend')
