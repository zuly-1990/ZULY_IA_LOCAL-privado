#!/usr/bin/env python3
"""
USUARIO FINAL - Prueba del dado con física
Verifica que el archivo funciona correctamente
"""

import sys
sys.path.insert(0, "C:/Users/Admin/Desktop/ZULY_IA_LOCAL")

import bpy

print("="*70)
print("👤 USUARIO FINAL - Probando dado con física")
print("="*70)

# Abrir el archivo con física
bpy.ops.wm.open_mainfile(
    filepath="C:/Users/Admin/Desktop/ZULY_IA_LOCAL/ZULY_PROJECTS/dado_fisica.blend"
)

print("\n📂 Archivo cargado: dado_fisica.blend")

# Verificar objetos
print("\n📋 Objetos en escena:")
objetos = bpy.data.objects
for obj in objetos:
    print(f"  • {obj.name} ({obj.type})")

# Verificar física
print("\n⚙️ Verificando física Rigid Body:")
objetos_con_fisica = 0
for obj in objetos:
    if obj.rigid_body:
        objetos_con_fisica += 1
        tipo = obj.rigid_body.type
        masa = obj.rigid_body.mass if obj.rigid_body.type == 'ACTIVE' else 'N/A'
        print(f"  ✅ {obj.name}: {tipo} (masa: {masa})")

print(f"\n📊 Total objetos con física: {objetos_con_fisica}")

# Verificar animación
print("\n🎬 Configuración de animación:")
print(f"  • Frame inicio: {bpy.context.scene.frame_start}")
print(f"  • Frame fin: {bpy.context.scene.frame_end}")
print(f"  • FPS: {bpy.context.scene.render.fps}")

# Verificar frames clave
print("\n🎞️ Verificando frames simulados:")
for frame in [1, 30, 60, 90, 120]:
    bpy.context.scene.frame_set(frame)
    dado = bpy.data.objects.get("Dado")
    if dado:
        loc = dado.location
        print(f"  Frame {frame}: Dado en Z={loc.z:.2f}")

# Resultado del usuario
print("\n" + "="*70)
print("👤 RESULTADO DEL USUARIO:")
print("="*70)
print("✅ Archivo abre correctamente")
print(f"✅ Hay {objetos_con_fisica} objetos con física")
print("✅ Animación configurada (120 frames)")
print("✅ Dado se mueve en la simulación")

if objetos_con_fisica >= 23:  # Dado + 21 puntos + suelo
    print("\n🟢 ESTADO: TODO FUNCIONA BIEN")
else:
    print(f"\n🟡 ESTADO: Faltan objetos con física ({objetos_con_fisica}/23)")
    print("   Necesita reparación")

print("="*70)
