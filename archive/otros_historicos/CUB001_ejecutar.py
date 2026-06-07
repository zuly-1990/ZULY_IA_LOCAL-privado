#!/usr/bin/env python3
"""
CUB-001_Modelado_BiselRealista
Cubo con bordes redondeados para look realista
"""

import bpy
import sys

def ejecutar_cub001():
    print("="*60)
    print("🔧 CUB-001: Cubo con Bisel Realista")
    print("="*60)
    
    # 1. RESET - Limpiar escena
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    
    # Limpiar materiales
    for material in bpy.data.materials:
        bpy.data.materials.remove(material)
    
    print("✅ Escena limpia (reset aplicado)")
    
    # 2. CREAR CUBO
    bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 1))
    cubo = bpy.context.active_object
    cubo.name = "CUB001_BiselRealista"
    
    print(f"✅ Cubo creado: {cubo.name}")
    
    # 3. APLICAR ESCALA (regla de oro)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    print("✅ Escala aplicada")
    
    # 4. AGREGAR MODIFICADOR BEVEL
    bevel = cubo.modifiers.new(name="Bevel_Edges", type='BEVEL')
    bevel.width = 0.05  # Ancho del bisel
    bevel.segments = 3  # Segmentos para suavizado
    bevel.limit_method = 'ANGLE'
    bevel.angle_limit = 0.5236  # 30 grados en radianes
    
    print(f"✅ Modificador Bevel agregado:")
    print(f"   - Width: {bevel.width}")
    print(f"   - Segments: {bevel.segments}")
    
    # 5. SOMBREADO SUAVE (Auto Smooth)
    cubo.data.use_auto_smooth = True
    cubo.data.auto_smooth_angle = 0.5236  # 30 grados
    
    print("✅ Auto Smooth activado (30°)")
    
    # 6. MATERIAL BÁSICO (gris para ver el bisel)
    material = bpy.data.materials.new(name="Material_CUB001")
    material.use_nodes = True
    
    # Configurar material
    principled = material.node_tree.nodes.get("Principled BSDF")
    if principled:
        principled.inputs['Base Color'].default_value = (0.7, 0.7, 0.7, 1.0)  # Gris
        principled.inputs['Roughness'].default_value = 0.4
        principled.inputs['Specular'].default_value = 0.5
    
    cubo.data.materials.append(material)
    print("✅ Material aplicado")
    
    # 7. ILUMINACIÓN BÁSICA (3-point lighting)
    # Key light
    bpy.ops.object.light_add(type='SUN', location=(5, 5, 10))
    key = bpy.context.active_object
    key.name = "Key_Light"
    key.data.energy = 5.0
    
    # Fill light
    bpy.ops.object.light_add(type='AREA', location=(-5, 2, 5))
    fill = bpy.context.active_object
    fill.name = "Fill_Light"
    fill.data.energy = 2.0
    
    print("✅ Iluminación configurada")
    
    # 8. CÁMARA
    bpy.ops.object.camera_add(location=(3, -3, 2.5))
    camara = bpy.context.active_object
    camara.name = "Camera_CUB001"
    
    # Apuntar al cubo
    direction = cubo.location - camara.location
    rot_quat = direction.to_track_quat('-Z', 'Y')
    camara.rotation_euler = rot_quat.to_euler()
    
    # Establecer como cámara activa
    bpy.context.scene.camera = camara
    
    print("✅ Cámara posicionada")
    
    # 9. CONFIGURAR RENDER
    bpy.context.scene.render.engine = 'BLENDER_EEVEE'
    bpy.context.scene.render.resolution_x = 1920
    bpy.context.scene.render.resolution_y = 1080
    bpy.context.scene.render.filepath = "./ZULY_PROJECTS/CUB001_render.png"
    
    print("✅ Render configurado (EEVEE)")
    
    # 10. GUARDAR ARCHIVO .blend
    output_path = "./ZULY_PROJECTS/CUB001_Modelado_BiselRealista.blend"
    bpy.ops.wm.save_as_mainfile(filepath=output_path)
    print(f"✅ Archivo guardado: {output_path}")
    
    # 11. RENDERIZAR
    print("📸 Renderizando...")
    bpy.ops.render.render(write_still=True)
    print("✅ Render completado")
    
    # 12. VALIDACIÓN
    print("\n" + "="*60)
    print("🔍 VALIDACIÓN CUB-001")
    print("="*60)
    
    # Verificar objeto existe
    if "CUB001_BiselRealista" in bpy.data.objects:
        print("✅ Objeto existe")
        obj = bpy.data.objects["CUB001_BiselRealista"]
        
        # Verificar modificadores
        if obj.modifiers:
            print(f"✅ Tiene {len(obj.modifiers)} modificador(es)")
            for mod in obj.modifiers:
                print(f"   - {mod.name} ({mod.type})")
        
        # Verificar material
        if obj.data.materials:
            print("✅ Tiene material asignado")
        
        # Verificar auto smooth
        if obj.data.use_auto_smooth:
            print("✅ Auto Smooth activado")
    else:
        print("❌ Objeto NO encontrado")
        return False
    
    print("\n" + "="*60)
    print("✅ CUB-001 COMPLETADO Y VALIDADO")
    print("="*60)
    
    return True

if __name__ == "__main__":
    try:
        resultado = ejecutar_cub001()
        sys.exit(0 if resultado else 1)
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
