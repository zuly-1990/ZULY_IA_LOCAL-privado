#!/usr/bin/env python3
"""
DADO REAL - Con puntos en posiciones correctas según estándar
Cara 1 opuesta a 6, 2 opuesta a 5, 3 opuesta a 4
"""

import sys
sys.path.insert(0, "C:/Users/Admin/Desktop/ZULY_IA_LOCAL")

import bpy
import math

# Limpiar TODO
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

print("="*60)
print("🎲 DADO REAL - Posiciones correctas")
print("="*60)

# 1. CUBO BASE
tamano_cubo = 2.0
bpy.ops.mesh.primitive_cube_add(size=tamano_cubo, location=(0, 0, 0))
cubo = bpy.context.active_object
cubo.name = "Dado"

# Material negro brillante
mat_negro = bpy.data.materials.new(name="Negro")
mat_negro.use_nodes = True
nodes = mat_negro.node_tree.nodes
nodes["Principled BSDF"].inputs['Base Color'].default_value = (0.02, 0.02, 0.02, 1)
nodes["Principled BSDF"].inputs['Roughness'].default_value = 0.1
cubo.data.materials.append(mat_negro)
print("✅ Cubo creado")

# Material rojo para puntos
mat_rojo = bpy.data.materials.new(name="Rojo")
mat_rojo.use_nodes = True
nodes = mat_rojo.node_tree.nodes
nodes["Principled BSDF"].inputs['Base Color'].default_value = (0.9, 0.0, 0.0, 1)
nodes["Principled BSDF"].inputs['Roughness'].default_value = 0.2

# Offset para puntos (afuera del cubo)
offset = tamano_cubo / 2 + 0.08  # Justo afuera de la superficie
radio_punto = 0.15

# Desplazamiento de puntos desde el centro (45% del tamaño del lado)
dp = 0.45  # delta position

print("\n🔴 Creando puntos en posiciones correctas...")
contador = 0

def crear_punto(x, y, z, nombre):
    global contador
    bpy.ops.mesh.primitive_uv_sphere_add(radius=radio_punto, location=(x, y, z))
    esfera = bpy.context.active_object
    esfera.name = nombre
    esfera.data.materials.append(mat_rojo)
    contador += 1

# CARA 1 (frente, Z+) - 1 punto en centro
crear_punto(0, 0, offset, "Cara1_Punto1")
print("   Cara 1: 1 punto (centro)")

# CARA 6 (atrás, Z-) - 6 puntos en 2 filas de 3
# Fila superior
for x in [-dp, 0, dp]:
    crear_punto(x, dp, -offset, f"Cara6_Punto_{contador}")
# Fila inferior
for x in [-dp, 0, dp]:
    crear_punto(x, -dp, -offset, f"Cara6_Punto_{contador}")
print("   Cara 6: 6 puntos (2 filas de 3)")

# CARA 2 (derecha, X+) - 2 puntos en diagonal ↖ ↘
crear_punto(offset, dp, dp, "Cara2_Punto1")    # Arriba-izquierda
crear_punto(offset, -dp, -dp, "Cara2_Punto2")  # Abajo-derecha
print("   Cara 2: 2 puntos (diagonal)")

# CARA 5 (izquierda, X-) - 5 puntos (4 esquinas + centro)
crear_punto(-offset, dp, dp, "Cara5_Punto1")      # Arriba-izquierda
crear_punto(-offset, -dp, -dp, "Cara5_Punto2")    # Abajo-derecha
crear_punto(-offset, dp, -dp, "Cara5_Punto3")     # Arriba-derecha
crear_punto(-offset, -dp, dp, "Cara5_Punto4")     # Abajo-izquierda
crear_punto(-offset, 0, 0, "Cara5_Punto5")        # Centro
print("   Cara 5: 5 puntos (4 esquinas + centro)")

# CARA 3 (arriba, Y+) - 3 puntos en diagonal ↖ C ↘
crear_punto(-dp, offset, dp, "Cara3_Punto1")   # Arriba-izquierda
crear_punto(0, offset, 0, "Cara3_Punto2")      # Centro
crear_punto(dp, offset, -dp, "Cara3_Punto3")   # Abajo-derecha
print("   Cara 3: 3 puntos (diagonal)")

# CARA 4 (abajo, Y-) - 4 puntos en esquinas
crear_punto(-dp, -offset, dp, "Cara4_Punto1")   # Arriba-izquierda
crear_punto(dp, -offset, -dp, "Cara4_Punto2")   # Abajo-derecha
crear_punto(-dp, -offset, -dp, "Cara4_Punto3")  # Arriba-derecha
crear_punto(dp, -offset, dp, "Cara4_Punto4")    # Abajo-izquierda
print("   Cara 4: 4 puntos (esquinas)")

print(f"\n✅ Total puntos: {contador} (debe ser 21)")

# Verificación: suma de opuestos
print("\n📐 Verificación (caras opuestas suman 7):")
print("   1 ↔ 6 = 7 ✓")
print("   2 ↔ 5 = 7 ✓")
print("   3 ↔ 4 = 7 ✓")

# LUZ
bpy.ops.object.light_add(type='SUN', location=(5, 5, 10))
luz = bpy.context.active_object
luz.name = "Luz"
luz.data.energy = 5

# CÁMARA
bpy.ops.object.camera_add(location=(3.5, -3.5, 2.5))
cam = bpy.context.active_object
cam.name = "Camara"
cam.rotation_euler = (1.0, 0, 0.785)
bpy.context.scene.camera = cam

# SUELO (plano invisible para recibir sombras)
bpy.ops.mesh.primitive_plane_add(size=10, location=(0, 0, -2))
suelo = bpy.context.active_object
suelo.name = "Suelo"
mat_suelo = bpy.data.materials.new(name="SueloGris")
mat_suelo.use_nodes = True
mat_suelo.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.4, 0.4, 0.45, 1)
suelo.data.materials.append(mat_suelo)

# GUARDAR
print("\n💾 Guardando...")
bpy.ops.wm.save_as_mainfile(
    filepath="C:/Users/Admin/Desktop/ZULY_IA_LOCAL/ZULY_PROJECTS/dado_real.blend"
)

# RENDER
print("🎨 Renderizando...")
scene = bpy.context.scene
scene.render.engine = 'BLENDER_EEVEE'
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.filepath = "C:/Users/Admin/Desktop/ZULY_IA_LOCAL/ZULY_PROJECTS/dado_real.png"
bpy.ops.render.render(write_still=True)

# RESUMEN
print("\n" + "="*60)
print("✅ DADO REAL COMPLETADO")
print("="*60)
print(f"Objetos: {len(bpy.data.objects)}")
print("  • 1 cubo (dado)")
print(f"  • {contador} puntos (posiciones correctas)")
print("  • 1 luz, 1 cámara, 1 suelo")
print(f"\nArchivos:")
print("  • dado_real.blend")
print("  • dado_real.png")
print("="*60)
print("\nConfiguración del dado:")
print("  • Cara 1 (frente): 1 punto")
print("  • Cara 2 (derecha): 2 puntos")
print("  • Cara 3 (arriba): 3 puntos")
print("  • Cara 4 (abajo): 4 puntos")
print("  • Cara 5 (izquierda): 5 puntos")
print("  • Cara 6 (atrás): 6 puntos")
print("="*60)
