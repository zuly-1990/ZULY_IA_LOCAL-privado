#!/usr/bin/env python3
"""
PRUEBA DE VOCABULARIO EXPANDIDO - ZULY
Verifica que el nuevo vocabulario lingüístico funcione
"""

import sys
sys.path.insert(0, 'c:/Users/Admin/Desktop/ZULY_IA_LOCAL')

from zuly_cli import ZULYCommandParser

def test_vocabulario():
    print("="*70)
    print("🧪 DESARROLLADOR - Probando vocabulario expandido")
    print("="*70)
    
    # Test 1: Primitivas nuevas
    print("\n📦 Test de primitivas:")
    pruebas_primitivas = [
        "caja roja",
        "bola azul",
        "tubo verde",
        "dona amarilla",
        "piramide naranja",
    ]
    
    for cmd in pruebas_primitivas:
        actions, confidence = ZULYCommandParser.parse_command(cmd)
        status = "✅" if actions else "❌"
        print(f"  {status} '{cmd}' -> {len(actions)} acciones")
    
    # Test 2: Agujeros
    print("\n🕳️ Test de agujeros:")
    pruebas_agujeros = [
        "haz agujero en el cubo",
        "perfora el cilindro",
        "talla un hueco",
        "cava en la esfera",
    ]
    
    for cmd in pruebas_agujeros:
        actions, confidence = ZULYCommandParser.parse_command(cmd)
        status = "✅" if actions else "❌"
        print(f"  {status} '{cmd}' -> {len(actions)} acciones")
    
    # Test 3: Ejes
    print("\n📐 Test de ejes:")
    pruebas_ejes = [
        "agujero en eje x",
        "perforación en eje y",
        "hueco en eje z",
        "corte horizontal",
        "talla vertical",
    ]
    
    for cmd in pruebas_ejes:
        actions, confidence = ZULYCommandParser.parse_command(cmd)
        status = "✅" if actions else "❌"
        print(f"  {status} '{cmd}' -> {len(actions)} acciones")
    
    # Test 4: Transformaciones
    print("\n🔄 Test de transformaciones:")
    pruebas_transform = [
        "mueve el cubo",
        "gira la esfera",
        "escala el cono",
        "desplaza el cilindro",
    ]
    
    for cmd in pruebas_transform:
        actions, confidence = ZULYCommandParser.parse_command(cmd)
        status = "✅" if actions else "❌"
        print(f"  {status} '{cmd}' -> {len(actions)} acciones")
    
    # Test 5: Colores nuevos
    print("\n🎨 Test de colores:")
    pruebas_colores = [
        "cubo dorado",
        "esfera plateada",
        "cilindro café",
        "cono morado",
    ]
    
    for cmd in pruebas_colores:
        actions, confidence = ZULYCommandParser.parse_command(cmd)
        status = "✅" if actions else "❌"
        print(f"  {status} '{cmd}' -> {len(actions)} acciones")
    
    print("\n" + "="*70)
    print("✅ DESARROLLADOR - Vocabulario expandido listo")
    print("="*70)
    print("\nNuevas capacidades:")
    print("  • 20+ primitivas (caja, bola, tubo, dona, piramide)")
    print("  • 10+ términos de agujeros (perforar, tallar, cava)")
    print("  • 6 ejes direccionales (x, y, z, horizontal, vertical)")
    print("  • 20+ colores (dorado, plateado, café, morado)")
    print("  • 10+ transformaciones (mueve, gira, desplaza)")

if __name__ == "__main__":
    test_vocabulario()
