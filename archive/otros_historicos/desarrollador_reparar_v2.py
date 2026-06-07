#!/usr/bin/env python3
"""
DESARROLLADOR - Reparación física MÉTODO 2
Simulación frame por frame con keyframes manuales
"""

import sys
sys.path.insert(0, "C:/Users/Admin/Desktop/ZULY_IA_LOCAL")

import bpy

print("="*70)
print("🛠️ DESARROLLADOR - Reparación física MÉTODO 2")
print("="*70)

# Cargar archivo
bpy.ops.wm.open_mainfile(
    filepath="C:/Users/Admin/Desktop/ZULY_IA_LOCAL/ZULY_PROJECTS/dado_fisica.blend"
)

print("\n🔄 Simulando frame por frame...")

scene = bpy.context.scene

# Simular paso a paso
for frame in range(1, 121):
    scene.frame_set(frame)
    
    # Forzar actualización de física
    bpy.context.view_layer.update()
    
    # Insertar keyframes para objetos con física
    for obj in bpy.data.objects:
        if obj.rigid_body and obj.rigid_body.type == 'ACTIVE':
            obj.keyframe_insert(data_path="location", frame=frame)
            obj.keyframe_insert(data_path="rotation_euler", frame=frame)
    
    if frame % 20 == 0:
        dado = bpy.data.objects.get("Dado")
        if dado:
            print(f"   Frame {frame}: Z={dado.location.z:.2f}")

print("\n💾 Guardando...")
bpy.ops.wm.save_as_mainfile(
    filepath="C:/Users/Admin/Desktop/ZULY_IA_LOCAL/ZULY_PROJECTS/dado_fisica_v2.blend"
)

print("✅ Reparado: dado_fisica_v2.blend")
