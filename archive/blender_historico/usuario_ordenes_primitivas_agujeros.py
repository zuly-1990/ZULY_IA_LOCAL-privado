#!/usr/bin/env python3
"""
USUARIO FINAL - Script de comandos para ZULY
Modela todas las primitivas y crea agujeros en ejes X, Y, Z
"""

import sys
sys.path.insert(0, 'c:/Users/Admin/Desktop/ZULY_IA_LOCAL')

from core.agent import Agent

def main():
    print("="*70)
    print("👤 USUARIO FINAL - Dando órdenes a ZULY")
    print("="*70)
    
    # Inicializar agente
    agent = Agent()
    
    # ========== ÓRDENES DE PRIMITIVAS ==========
    print("\n🗣️  Órdenes de primitivas:")
    
    comandos_primitivas = [
        "Crea un cubo rojo en posición 0,0,0",
        "Crea una esfera azul en posición 3,0,0", 
        "Crea un cilindro verde en posición 6,0,0",
        "Crea un plano amarillo en posición 9,0,0",
        "Crea un cono naranja en posición 12,0,0",
    ]
    
    for comando in comandos_primitivas:
        print(f"\n👤 Usuario: '{comando}'")
        resultado = agent.process_natural_request(comando)
        if resultado.get('success'):
            print(f"✅ ZULY: {resultado.get('feedback', 'Hecho')}")
        else:
            print(f"❌ ZULY Error: {resultado.get('feedback', 'Falló')}")
    
    # ========== ÓRDENES DE AGUJEROS ==========
    print("\n" + "="*70)
    print("🗣️  Órdenes de agujeros:")
    print("="*70)
    
    comandos_agujeros = [
        "Crea un cubo grande blanco en posición 0,3,0",
        "Haz un agujero en el eje X del cubo",
        "Haz un agujero en el eje Y del cubo", 
        "Haz un agujero en el eje Z del cubo",
    ]
    
    for comando in comandos_agujeros:
        print(f"\n👤 Usuario: '{comando}'")
        resultado = agent.process_natural_request(comando)
        if resultado.get('success'):
            print(f"✅ ZULY: {resultado.get('feedback', 'Hecho')}")
        else:
            print(f"❌ ZULY Error: {resultado.get('feedback', 'Falló')}")
    
    print("\n" + "="*70)
    print("👤 USUARIO: Comandos completados")
    print("="*70)

if __name__ == "__main__":
    main()
