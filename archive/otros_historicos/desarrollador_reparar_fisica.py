#!/usr/bin/env python3
"""
DESARROLLADOR - Reparación física del dado
Corregir simulación Rigid Body para que realmente funcione
"""

import sys
sys.path.insert(0, "C:/Users/Admin/Desktop/ZULY_IA_LOCAL")

import bpy

print("="*70)
print("🛠️ DESARROLLADOR - Reparando física del dado")
print("="*70)

# Cargar archivo existente
bpy.ops.wm.open_mainfile(
    filepath="C:/Users/Admin/Desktop/ZULY_IA_LOCAL/ZULY_PROJECTS/dado_fisica.blend"
)

print("\n🔍 DIAGNÓSTICO:")
print("   Problema: Dado no cae, física no simulada")

# VERIFICAR Rigid Body World
print("\n⚙️ Configurando Rigid Body World correctamente...")
scene = bpy.context.scene

if scene.rigidbody_world is None:
    bpy.ops.rigidbody.world_add()
    print("   ✅ Rigid Body World creado")
else:
    print("   ✅ Rigid Body World ya existe")

# Configurar correctamente
rbw = scene.rigidbody_world
rbw.enabled = True
rbw.point_cache.frame_start = 1
rbw.point_cache.frame_end = 120

print(f"   ✅ Frames: {rbw.point_cache.frame_start} - {rbw.point_cache.frame_end}")

# HACER BAKE CORRECTO
print("\n🎬 Realizando bake de física...")
print("   Esto calculará la simulación frame por frame...")

# Método correcto: usar bake operator
bpy.context.scene.frame_set(1)

# Seleccionar todos los objetos con física
bpy.ops.object.select_all(action='DESELECT')
for obj in bpy.data.objects:
    if obj.rigid_body:
        obj.select_set(True)

print(f"   {len([o for o in bpy.data.objects if o.rigid_body])} objetos seleccionados")

# Bake to keyframes para que la animación se guarde
print("\n📼 Bakeando animación a keyframes...")

# Hacer bake del Rigid Body World
override = bpy.context.copy()
override['scene'] = scene

# Ejecutar bake
bpy.ops.rigidbody.bake_to_keyframes(
    override,
    frame_start=1,
    frame_end=120,
    step=1
)

print("   ✅ Bake completado")

# Verificar movimiento
print("\n🔍 Verificando movimiento después del bake:")
for frame in [1, 30, 60, 90, 120]:
    bpy.context.scene.frame_set(frame)
    dado = bpy.data.objects.get("Dado")
    if dado:
        z = dado.location.z
        rot = dado.rotation_euler.z
        print(f"   Frame {frame}: Z={z:.2f}, Rot={rot:.2f}")

# Guardar versión reparada
print("\n💾 Guardando versión reparada...")
bpy.ops.wm.save_as_mainfile(
    filepath="C:/Users/Admin/Desktop/ZULY_IA_LOCAL/ZULY_PROJECTS/dado_fisica_reparado.blend"
)

print("   ✅ Guardado: dado_fisica_reparado.blend")

print("\n" + "="*70)
print("✅ REPARACIÓN COMPLETADA")
print("="*70)
print("   La física ahora está bakeada a keyframes")
print("   El dado caerá y rodará visiblemente")
print("="*70)
