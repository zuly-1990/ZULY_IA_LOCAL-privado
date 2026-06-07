#!/usr/bin/env python3
"""
DADO LIMPIO - Solo cubo + esferas como puntos
"""

import sys
sys.path.insert(0, "C:/Users/Admin/Desktop/ZULY_IA_LOCAL")

import bpy

# Limpiar TODO
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

print("="*60)
print("🎲 DADO LIMPIO - Creando...")
print("="*60)

# 1. CUBO BASE (el dado)
print("\n📦 Creando cubo base...")
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))
cubo = bpy.context.active_object
cubo.name = "Dado"

# Material negro
mat_negro = bpy.data.materials.new(name="Negro")
mat_negro.use_nodes = True
nodes = mat_negro.node_tree.nodes
nodes["Principled BSDF"].inputs['Base Color'].default_value = (0.05, 0.05, 0.05, 1)
nodes["Principled BSDF"].inputs['Roughness'].default_value = 0.3
cubo.data.materials.append(mat_negro)
print("   ✅ Cubo creado")

# 2. PUNTOS (esferas rojas)
print("\n🔴 Creando puntos...")

# Material rojo
mat_rojo = bpy.data.materials.new(name="Rojo")
mat_rojo.use_nodes = True
nodes = mat_rojo.node_tree.nodes
nodes["Principled BSDF"].inputs['Base Color'].default_value = (0.9, 0.05, 0.05, 1)
nodes["Principled BSDF"].inputs['Roughness'].default_value = 0.2

# Posiciones de puntos para cada cara (más afuera para que se vean)
desplazamiento = 1.15  # Un poco afuera del cubo

puntos = [
    # Cara 1 (frente, Z+) - 1 punto
    [(0, 0, desplazamiento)],
    # Cara 2 (derecha, X+) - 2 puntos
    [(desplazamiento, -0.4, 0.4), (desplazamiento, 0.4, -0.4)],
    # Cara 3 (arriba, Y+) - 3 puntos
    [(0, desplazamiento, 0), (-0.4, desplazamiento, -0.4), (0.4, desplazamiento, 0.4)],
    # Cara 4 (abajo, Y-) - 4 puntos
    [(-0.4, -desplazamiento, 0.4), (0.4, -desplazamiento, -0.4),
     (-0.4, -desplazamiento, -0.4), (0.4, -desplazamiento, 0.4)],
    # Cara 5 (atrás, X-) - 5 puntos
    [(-desplazamiento, 0, 0), (-desplazamiento, 0.4, 0.4), (-desplazamiento, -0.4, -0.4),
     (-desplazamiento, 0.4, -0.4), (-desplazamiento, -0.4, 0.4)],
    # Cara 6 (atrás, Z-) - 6 puntos
    [(0, -0.3, -desplazamiento), (0, 0.3, -desplazamiento),
     (-0.4, -0.3, -desplazamiento), (0.4, 0.3, -desplazamiento),
     (-0.4, 0.3, -desplazamiento), (0.4, -0.3, -desplazamiento)]
]

contador = 0
cara_num = 1
for cara_puntos in puntos:
    for pos in cara_puntos:
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.18, location=pos)
        esfera = bpy.context.active_object
        esfera.name = f"Punto_{cara_num}_{contador+1}"
        esfera.data.materials.append(mat_rojo)
        contador += 1
    cara_num += 1

print(f"   ✅ {contador} puntos creados")

# 3. LUZ
print("\n💡 Añadiendo luz...")
bpy.ops.object.light_add(type='SUN', location=(5, 5, 8))
luz = bpy.context.active_object
luz.name = "Luz"
luz.data.energy = 4
print("   ✅ Luz creada")

# 4. CÁMARA
print("\n📷 Cámara...")
bpy.ops.object.camera_add(location=(4, -4, 3))
cam = bpy.context.active_object
cam.name = "Camara"
cam.rotation_euler = (1.1, 0, 0.785)
bpy.context.scene.camera = cam
print("   ✅ Cámara creada")

# 5. GUARDAR .blend
print("\n💾 Guardando...")
bpy.ops.wm.save_as_mainfile(
    filepath="C:/Users/Admin/Desktop/ZULY_IA_LOCAL/ZULY_PROJECTS/dado_limpio.blend"
)
print("   ✅ Guardado: dado_limpio.blend")

# 6. RENDER
print("\n🎨 Renderizando...")
scene = bpy.context.scene
scene.render.engine = 'BLENDER_EEVEE'
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.filepath = "C:/Users/Admin/Desktop/ZULY_IA_LOCAL/ZULY_PROJECTS/dado_limpio.png"
bpy.ops.render.render(write_still=True)
print("   ✅ Render guardado")

# RESUMEN
print("\n" + "="*60)
print("✅ DADO LIMPIO COMPLETADO")
print("="*60)
print(f"Objetos: {len(bpy.data.objects)}")
print("  • 1 cubo (dado)")
print(f"  • {contador} esferas (puntos)")
print("  • 1 luz")
print("  • 1 cámara")
print(f"\nArchivos:")
print("  • dado_limpio.blend")
print("  • dado_limpio.png")
print("="*60)
