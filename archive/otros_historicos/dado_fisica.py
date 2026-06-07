#!/usr/bin/env python3
"""
DADO CON FÍSICA - Rigid Body para que ruede
"""

import sys
sys.path.insert(0, "C:/Users/Admin/Desktop/ZULY_IA_LOCAL")

import bpy
import math

# Cargar el dado limpio existente
print("="*60)
print("🎲 CARGANDO DADO Y AGREGANDO FÍSICA...")
print("="*60)

# Abrir el archivo existente
bpy.ops.wm.open_mainfile(
    filepath="C:/Users/Admin/Desktop/ZULY_IA_LOCAL/ZULY_PROJECTS/dado_limpio.blend"
)

# Configurar física
print("\n⚙️ Configurando motor de física...")

# Habilitar Rigid Body World
if bpy.context.scene.rigidbody_world is None:
    bpy.ops.rigidbody.world_add()

# Configurar gravedad
bpy.context.scene.rigidbody_world.enabled = True
bpy.context.scene.gravity = (0, 0, -9.8)

# Configurar frames de animación
bpy.context.scene.frame_start = 1
bpy.context.scene.frame_end = 120

print("   ✅ Motor de física listo")

# Agregar física al cubo (Dado)
print("\n📦 Física al dado...")
dado = bpy.data.objects.get("Dado")
if dado:
    bpy.context.view_layer.objects.active = dado
    bpy.ops.rigidbody.object_add(type='ACTIVE')
    dado.rigid_body.mass = 1.0
    dado.rigid_body.friction = 0.5
    dado.rigid_body.restitution = 0.3
    dado.rigid_body.linear_damping = 0.1
    dado.rigid_body.angular_damping = 0.1
    
    # Posicionar en altura para que caiga
    dado.location = (0, 0, 5)
    dado.rotation_euler = (math.radians(15), math.radians(25), math.radians(10))
    print("   ✅ Dado con física activa")

# Agregar física a las esferas (puntos)
print("\n🔴 Física a los puntos...")
puntos_fisica = 0
for obj in bpy.data.objects:
    if obj.name.startswith("Punto_"):
        bpy.context.view_layer.objects.active = obj
        bpy.ops.rigidbody.object_add(type='ACTIVE')
        obj.rigid_body.mass = 0.05  # Muy ligeros
        obj.rigid_body.friction = 0.8
        obj.rigid_body.restitution = 0.5
        obj.rigid_body.linear_damping = 0.5
        obj.rigid_body.angular_damping = 0.5
        puntos_fisica += 1

print(f"   ✅ {puntos_fisica} puntos con física")

# Crear suelo
print("\n🟫 Creando suelo...")
bpy.ops.mesh.primitive_plane_add(size=20, location=(0, 0, -2))
suelo = bpy.context.active_object
suelo.name = "Suelo"

# Material del suelo
mat_suelo = bpy.data.materials.new(name="Suelo_Material")
mat_suelo.use_nodes = True
mat_suelo.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.3, 0.3, 0.35, 1)
suelo.data.materials.append(mat_suelo)

# Física del suelo (pasivo)
bpy.ops.rigidbody.object_add(type='PASSIVE')
suelo.rigid_body.friction = 0.8
suelo.rigid_body.restitution = 0.1
print("   ✅ Suelo creado")

# Hacer bake de la física (simular)
print("\n🎬 Simulando física (bake)...")
print("   Esto puede tomar un momento...")

# Ir al frame inicial y bake
bpy.context.scene.frame_set(1)

# Simular hasta frame 120
for frame in range(1, 121):
    bpy.context.scene.frame_set(frame)
    if frame % 20 == 0:
        print(f"   Frame {frame}/120...")

print("   ✅ Simulación completa")

# Guardar con física
print("\n💾 Guardando con física...")
bpy.ops.wm.save_as_mainfile(
    filepath="C:/Users/Admin/Desktop/ZULY_IA_LOCAL/ZULY_PROJECTS/dado_fisica.blend"
)
print("   ✅ Guardado: dado_fisica.blend")

# Renderizar frame 60 (en medio de la caída)
print("\n🎨 Renderizando frame 60...")
bpy.context.scene.frame_set(60)
scene = bpy.context.scene
scene.render.engine = 'BLENDER_EEVEE'
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.filepath = "C:/Users/Admin/Desktop/ZULY_IA_LOCAL/ZULY_PROJECTS/dado_rodando.png"
bpy.ops.render.render(write_still=True)
print("   ✅ Render guardado")

# Guardar también como video (secuencia de imágenes)
print("\n📹 Guardando secuencia de animación...")
scene.render.image_settings.file_format = 'PNG'
scene.render.filepath = "C:/Users/Admin/Desktop/ZULY_IA_LOCAL/ZULY_PROJECTS/animacion/frame_"

# Renderizar algunos frames clave
key_frames = [1, 30, 60, 90, 120]
for frame in key_frames:
    bpy.context.scene.frame_set(frame)
    scene.render.filepath = f"C:/Users/Admin/Desktop/ZULY_IA_LOCAL/ZULY_PROJECTS/animacion/frame_{frame:03d}.png"
    bpy.ops.render.render(write_still=True)
    print(f"   Frame {frame} renderizado")

# RESUMEN
print("\n" + "="*60)
print("✅ DADO CON FÍSICA COMPLETADO")
print("="*60)
print(f"\n📊 Simulación:")
print("  • Dado cae desde 5 unidades de altura")
print("  • 21 puntos con física individual")
print("  • Suelo con fricción realista")
print("  • 120 frames de animación")
print(f"\n📁 Archivos:")
print("  • dado_fisica.blend (con física)")
print("  • dado_rodando.png (frame 60)")
print("  • animacion/frame_*.png (secuencia)")
print("="*60)

print("\n💡 Para ver la animación:")
print("1. Abre dado_fisica.blend")
print("2. Presiona SPACE para reproducir")
print("3. O presiona SHIFT + ← (ir a inicio) y luego ▶")
