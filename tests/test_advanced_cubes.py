"""
test_advanced_cubes.py

Script de prueba avanzada para generación de cubos en Blender.
Genera escenas complejas con fractales, física y modificadores.
"""

import sys
import os
import math
import random
from pathlib import Path

# Configuración de rutas
CURRENT_DIR = Path(os.getcwd())
OUTPUT_DIR = CURRENT_DIR / "export" / "pruebas_cubo"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

import bpy

def limpiar_escena():
    """Limpia la escena completamente."""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    
    # Limpiar orphan data
    for block in bpy.data.meshes:
        if block.users == 0:
            bpy.data.meshes.remove(block)
    for block in bpy.data.materials:
        if block.users == 0:
            bpy.data.materials.remove(block)

def crear_material(nombre, color, metalico=0.0, rugosidad=0.5):
    """Crea un material PBR simple."""
    mat = bpy.data.materials.new(name=nombre)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")
    
    bsdf.inputs['Base Color'].default_value = (*color, 1.0)
    bsdf.inputs['Metallic'].default_value = metalico
    bsdf.inputs['Roughness'].default_value = rugosidad
    
    return mat

def crear_cubo_fractal(nivel, posicion, tamaño):
    """
    Crea una estructura fractal simple de cubos (Esponja de Menger simplificada).
    """
    if nivel == 0:
        bpy.ops.mesh.primitive_cube_add(
            size=tamaño, 
            location=posicion
        )
        return

    sub_tamaño = tamaño / 3.0
    for x in range(-1, 2):
        for y in range(-1, 2):
            for z in range(-1, 2):
                # Omitir el centro y los centros de las caras (tipo Menger)
                suma_abs = abs(x) + abs(y) + abs(z)
                if suma_abs > 1: # Simplificación para no generar tantos cubos
                    nueva_pos = (
                        posicion[0] + x * sub_tamaño,
                        posicion[1] + y * sub_tamaño,
                        posicion[2] + z * sub_tamaño
                    )
                    
                    # Solo recursión si es necesaria, optimización
                    if nivel > 1 and random.random() > 0.7: # Aleatoriedad para variedad
                         crear_cubo_fractal(nivel - 1, nueva_pos, sub_tamaño)
                    else:
                        bpy.ops.mesh.primitive_cube_add(
                            size=sub_tamaño,
                            location=nueva_pos
                        )

def prueba_fisica_cubos():
    """Crea una simulación de física con cubos cayendo."""
    print("Generando simulación de física...")
    
    # Suelo
    bpy.ops.mesh.primitive_plane_add(size=20, location=(0, 0, 0))
    suelo = bpy.context.active_object
    suelo.name = "Suelo_Fisica"
    bpy.ops.rigidbody.object_add()
    suelo.rigid_body.type = 'PASSIVE'
    
    mat_suelo = crear_material("SueloMat", (0.1, 0.1, 0.1), 0.0, 1.0)
    suelo.data.materials.append(mat_suelo)

    # Torre de cubos
    mat_cubo = crear_material("CuboFisica", (0.2, 0.5, 0.8), 0.5, 0.2)
    
    for i in range(10):
        x = random.uniform(-1, 1)
        y = random.uniform(-1, 1)
        z = 2 + i * 2.2 # Altura incremental
        
        bpy.ops.mesh.primitive_cube_add(size=2, location=(x, y, z))
        cubo = bpy.context.active_object
        cubo.name = f"Cubo_Fisica_{i}"
        
        bpy.ops.rigidbody.object_add()
        cubo.rigid_body.type = 'ACTIVE'
        cubo.rigid_body.mass = 1.0
        
        cubo.data.materials.append(mat_cubo)
        
        # Rotación aleatoria inicial para caos
        cubo.rotation_euler = (
            random.uniform(0, 0.5),
            random.uniform(0, 0.5),
            random.uniform(0, 0.5)
        )

def prueba_modificadores():
    """Prueba modificadores en cubos."""
    print("Generando prueba de modificadores...")
    
    # Array de cubos
    bpy.ops.mesh.primitive_cube_add(size=1, location=(10, 0, 2))
    cubo = bpy.context.active_object
    cubo.name = "Cubo_Array"
    
    mod = cubo.modifiers.new(name="Array", type='ARRAY')
    mod.count = 5
    mod.use_relative_offset = True
    mod.relative_offset_displace = (1.5, 0, 0)
    
    mod2 = cubo.modifiers.new(name="Bevel", type='BEVEL')
    mod2.width = 0.1
    
    mat = crear_material("ArrayMat", (0.8, 0.2, 0.5), 0.8, 0.2)
    cubo.data.materials.append(mat)

def configurar_camara_luz():
    """Configura cámara y luz básica."""
    # Cámara
    bpy.ops.object.camera_add(location=(15, -15, 12))
    cam = bpy.context.active_object
    cam.rotation_euler = (math.radians(55), 0, math.radians(45))
    bpy.context.scene.camera = cam
    
    # Sol
    bpy.ops.object.light_add(type='SUN', location=(0, 0, 20))
    sun = bpy.context.active_object
    sun.data.energy = 5
    sun.rotation_euler = (math.radians(30), math.radians(30), 0)

def main():
    print("="*60)
    print("INICIANDO PRUEBAS AVANZADAS DE CUBOS")
    print("="*60)
    
    limpiar_escena()
    
    # 1. Escena de Física (Centro)
    prueba_fisica_cubos()
    
    # 2. Escena de Modificadores (Derecha)
    prueba_modificadores()
    
    # 3. Escena Fractal (Izquierda - Simplificada)
    print("Generando fractal...")
    crear_cubo_fractal(2, (-10, 0, 3), 4.0)
    
    configurar_camara_luz()
    
    # Guardar .blend
    blend_path = OUTPUT_DIR / "test_avanzado_cubos.blend"
    bpy.ops.wm.save_as_mainfile(filepath=str(blend_path))
    print(f"✅ Archivo .blend guardado en: {blend_path}")
    
    # Render rápido (Workbench para velocidad)
    bpy.context.scene.render.engine = 'BLENDER_WORKBENCH'
    bpy.context.scene.render.resolution_x = 1280
    bpy.context.scene.render.resolution_y = 720
    
    render_path = OUTPUT_DIR / "render_prueba_cubos.png"
    bpy.context.scene.render.filepath = str(render_path)
    bpy.ops.render.render(write_still=True)
    print(f"✅ Render guardado en: {render_path}")
    
    print("="*60)
    print("PRUEBA COMPLETADA EXITOSAMENTE")
    print("="*60)

if __name__ == "__main__":
    main()
