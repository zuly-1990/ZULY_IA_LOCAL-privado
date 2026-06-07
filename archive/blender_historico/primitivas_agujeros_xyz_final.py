#!/usr/bin/env python3
"""
SCRIPT FINAL - PRIMITIVAS CON AGUJEROS EN EJES X, Y, Z
Usuario: Modela todas las primitivas y agujeros en los 3 ejes
Desarrollador: Vocabulario expandido implementado
"""

import sys
sys.path.insert(0, 'c:/Users/Admin/Desktop/ZULY_IA_LOCAL')

from core.agent import Agent

def modelo_completo_primitivas_agujeros():
    print("="*70)
    print("🎨 PRIMITIVAS + AGUJEROS EN X, Y, Z")
    print("="*70)
    
    agent = Agent()
    
    # Limpiar escena primero
    print("\n🧹 Limpiando escena...")
    agent.process_natural_request("limpiar escena")
    
    # ========== PRIMITIVAS CON AGUJERO EN EJE X ==========
    print("\n" + "="*70)
    print("📦 PRIMITIVAS CON AGUJERO EN EJE X (horizontal)")
    print("="*70)
    
    primitivas_x = [
        "Crea una caja roja grande en 0,0,0 y haz un agujero en eje x",
        "Crea una bola azul en 4,0,0 y perfora en eje x",
        "Crea un tubo verde en 8,0,0 y talla un hueco horizontal",
        "Crea una dona amarilla en 12,0,0 y cava en eje x",
    ]
    
    for cmd in primitivas_x:
        print(f"\n👤 Usuario: '{cmd}'")
        result = agent.process_natural_request(cmd)
        print(f"🤖 ZULY: {'✅ OK' if result.get('success') else '❌ Falló'}")
    
    # ========== PRIMITIVAS CON AGUJERO EN EJE Y ==========
    print("\n" + "="*70)
    print("📦 PRIMITIVAS CON AGUJERO EN EJE Y (vertical)")
    print("="*70)
    
    primitivas_y = [
        "Crea una piramide naranja en 0,4,0 y haz agujero en eje y",
        "Crea un cilindro morado en 4,4,0 y perfora vertical",
        "Crea una esfera rosada en 8,4,0 y talla en eje y",
        "Crea un cono café en 12,4,0 y cava vertical",
    ]
    
    for cmd in primitivas_y:
        print(f"\n👤 Usuario: '{cmd}'")
        result = agent.process_natural_request(cmd)
        print(f"🤖 ZULY: {'✅ OK' if result.get('success') else '❌ Falló'}")
    
    # ========== PRIMITIVAS CON AGUJERO EN EJE Z ==========
    print("\n" + "="*70)
    print("📦 PRIMITIVAS CON AGUJERO EN EJE Z (profundidad)")
    print("="*70)
    
    primitivas_z = [
        "Crea un cubo dorado en 0,8,0 y haz agujero en eje z",
        "Crea una caja plateada en 4,8,0 y perfora en profundidad",
        "Crea un tubo cian en 8,8,0 y talla hueco en eje z",
        "Crea una dona verde en 12,8,0 y cava en profundidad",
    ]
    
    for cmd in primitivas_z:
        print(f"\n👤 Usuario: '{cmd}'")
        result = agent.process_natural_request(cmd)
        print(f"🤖 ZULY: {'✅ OK' if result.get('success') else '❌ Falló'}")
    
    # ========== RENDER FINAL ==========
    print("\n" + "="*70)
    print("🎨 Renderizando resultado final...")
    print("="*70)
    
    agent.process_natural_request("renderizar escena")
    
    print("\n" + "="*70)
    print("✅ MODELO COMPLETADO")
    print("="*70)
    print("\nPrimitivas creadas:")
    print("  • 4 con agujeros en eje X (horizontal)")
    print("  • 4 con agujeros en eje Y (vertical)")
    print("  • 4 con agujeros en eje Z (profundidad)")
    print("\nVocabulario utilizado:")
    print("  • caja, bola, tubo, dona, piramide")
    print("  • perforar, tallar, cava, agujero")
    print("  • horizontal, vertical, profundidad (x, y, z)")
    print("  • rojo, azul, verde, amarillo, naranja, morado, café, dorado, plateado, cian")
    print("="*70)

if __name__ == "__main__":
    modelo_completo_primitivas_agujeros()
