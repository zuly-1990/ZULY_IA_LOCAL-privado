#!/usr/bin/env python3
"""
Script para crear un dado negro con puntos rojos usando Blender con ZULY
Este script está diseñado para ejecutarse dentro de Blender
"""

import sys
from pathlib import Path

# Agregar ZULY al path
sys.path.insert(0, "C:/Users/Admin/Desktop/ZULY_IA_LOCAL")

import bpy
from lyzu_core import LYZUCore

def crear_dado_con_puntos_rojos():
    """Crear dado negro con puntos rojos usando LYZU"""
    
    print("\n" + "="*60)
    print("🎲 CREANDO DADO NEGRO CON PUNTOS ROJOS")
    print("="*60 + "\n")
    
    # Inicializar LYZU
    lyzu = LYZUCore(mode='reactive')
    
    # Limpiar escena
    print("🧹 Limpiando escena...")
    lyzu.process_user_input("Limpia la escena")
    
    # Crear cubo base negro
    print("🎲 Creando cubo base negro...")
    lyzu.process_user_input("Crea un cubo negro de tamaño 2 en posición 0,0,0")
    
    # Coordenadas de los puntos para cada cara del dado
    # Cara 1 (frente): 1 punto
    # Cara 2 (derecha): 2 puntos  
    # Cara 3 (arriba): 3 puntos
    # Cara 4 (abajo): 4 puntos
    # Cara 5 (atrás): 5 puntos
    # Cara 6 (izquierda): 6 puntos
    
    puntos_caras = {
        'cara_1': [(0, 0, 1.05)],  # 1 punto frente
        'cara_2': [(1.05, -0.3, 0.3), (1.05, 0.3, -0.3)],  # 2 puntos derecha
        'cara_3': [(0, 1.05, 0), (-0.3, 1.05, -0.3), (0.3, 1.05, 0.3)],  # 3 puntos arriba
        'cara_4': [(-0.3, -1.05, 0.3), (0.3, -1.05, -0.3), 
                   (-0.3, -1.05, -0.3), (0.3, -1.05, 0.3)],  # 4 puntos abajo
        'cara_5': [(-1.05, 0.3, 0.3), (-1.05, -0.3, -0.3),
                   (-1.05, 0, 0), (-1.05, 0.3, -0.3), (-1.05, -0.3, 0.3)],  # 5 puntos atrás
        'cara_6': [(-0.2, 0, -1.05), (0.2, 0.2, -1.05), (0.2, -0.2, -1.05),
                   (0, 0.3, -1.05), (0, -0.3, -1.05), (-0.2, -0.2, -1.05)]  # 6 puntos izq
    }
    
    # Crear puntos rojos
    print("🔴 Creando puntos rojos...")
    total_puntos = 0
    
    for cara, posiciones in puntos_caras.items():
        print(f"   Creando puntos para {cara}...")
        for i, pos in enumerate(posiciones):
            comando = f"Crea una esfera roja pequeña de radio 0.15 en posición {pos[0]},{pos[1]},{pos[2]}"
            lyzu.process_user_input(comando)
            total_puntos += 1
    
    print(f"✅ Total de puntos creados: {total_puntos}")
    
    # Añadir iluminación
    print("💡 Añadiendo iluminación...")
    lyzu.process_user_input("Añade una luz solar en posición 5,5,5")
    
    # Configurar cámara
    print("📷 Configurando cámara...")
    bpy.ops.object.camera_add(location=(7, -7, 5))
    camera = bpy.context.active_object
    camera.rotation_euler = (1.1, 0, 0.785)
    bpy.context.scene.camera = camera
    
    # Guardar archivo .blend
    print("💾 Guardando archivo .blend...")
    blend_path = "C:/Users/Admin/Desktop/ZULY_IA_LOCAL/ZULY_PROJECTS/dado_con_puntos_rojos.blend"
    bpy.ops.wm.save_as_mainfile(filepath=blend_path)
    print(f"   ✅ Guardado: {blend_path}")
    
    # Renderizar
    print("🖼️ Renderizando...")
    scene = bpy.context.scene
    scene.render.engine = 'BLENDER_EEVEE'
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.render.filepath = "C:/Users/Admin/Desktop/ZULY_IA_LOCAL/ZULY_PROJECTS/dado_eevee.png"
    bpy.ops.render.render(write_still=True)
    
    print("\n" + "="*60)
    print("🎉 DADO COMPLETADO")
    print("="*60)
    print(f"✅ Cubo negro creado")
    print(f"✅ {total_puntos} puntos rojos agregados")
    print(f"✅ Render guardado en: ZULY_PROJECTS/dado_eevee.png")
    print("="*60)
    
    # Mostrar objetos creados
    print(f"\n📋 Objetos en la escena: {len(bpy.data.objects)}")
    for obj in bpy.data.objects:
        print(f"  • {obj.name} ({obj.type})")

if __name__ == "__main__":
    crear_dado_con_puntos_rojos()
    
