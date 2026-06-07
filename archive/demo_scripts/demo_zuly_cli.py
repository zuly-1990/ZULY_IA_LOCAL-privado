#!/usr/bin/env python3
"""
Demo: ZULY CLI Interactivo - Opción 2
Demuestra parsing y ejecución de comandos en lenguaje natural
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from zuly_cli_interactive import ZULYNLParser, ZULYExecutor


def demo_parser():
    """Demuestra el parser"""
    print("\n" + "=" * 70)
    print("  DEMO 1: PARSER DE LENGUAJE NATURAL")
    print("=" * 70)
    
    test_cases = [
        "crear un cubo",
        "crear una esfera",
        "crear esfera y rotar 45 grados",
        "crear cubo, mover y escalar 2.0",
        "crear arquitectura villa savoye",
        "rotar 90 grados",
        "escalar objeto 3 veces",
    ]
    
    parser = ZULYNLParser()
    
    for instruction in test_cases:
        print(f"\n📝 Instrucción: '{instruction}'")
        actions, confidence = parser.parse(instruction)
        
        print(f"   Confianza: {confidence:.1%}")
        print(f"   Acciones detectadas: {len(actions)}")
        
        for i, action in enumerate(actions, 1):
            print(f"     {i}. {action['action']}")
            if action.get('parameters'):
                for k, v in action['parameters'].items():
                    print(f"        - {k}: {v}")


def demo_script_generation():
    """Demuestra generación de scripts"""
    print("\n" + "=" * 70)
    print("  DEMO 2: GENERACIÓN DE SCRIPTS BLENDER")
    print("=" * 70)
    
    parser = ZULYNLParser()
    executor = ZULYExecutor()
    
    # Ejemplo: crear cubo y rotar
    instruction = "crear cubo y rotar 45 grados"
    print(f"\n📝 Instrucción: '{instruction}'")
    
    actions, confidence = parser.parse(instruction)
    print(f"✓ Parseado: {len(actions)} acciones")
    
    script = executor._generate_script(actions)
    print(f"\n🐍 Script Blender generado:\n")
    print("-" * 70)
    for i, line in enumerate(script.split("\n"), 1):
        print(f"{i:2d}. {line}")
    print("-" * 70)


def demo_complex_commands():
    """Demuestra comandos complejos"""
    print("\n" + "=" * 70)
    print("  DEMO 3: COMANDOS COMPLEJOS")
    print("=" * 70)
    
    parser = ZULYNLParser()
    
    complex_commands = [
        "crear un cubo luego una esfera y rotar 90 grados",
        "crear arquitectura y renderizar",
        "crear dos cubos, escalar 2 y rotar 45",
        "crear villa savoye con decoración",
    ]
    
    for cmd in complex_commands:
        print(f"\n📝 '{cmd}'")
        actions, conf = parser.parse(cmd)
        print(f"   ✓ {len(actions)} acciones, confianza {conf:.0%}")


def demo_statistics():
    """Demuestra estadísticas"""
    print("\n" + "=" * 70)
    print("  DEMO 4: ESTADÍSTICAS DE PARSER")
    print("=" * 70)
    
    parser = ZULYNLParser()
    executor = ZULYExecutor()
    
    # Géneros de prueba
    test_commands = [
        "crear cubo",
        "crear esfera",
        "rotar 45",
        "escalar 2",
        "crear arquitectura",
        "mover objeto",
        "create cube",  # Comando erróneo
        "xyz random",   # Comando inválido
    ]
    
    total = len(test_commands)
    recognized = 0
    avg_confidence = 0
    
    print(f"\nProbando {total} comandos...\n")
    
    for cmd in test_commands:
        actions, conf = parser.parse(cmd)
        avg_confidence += conf
        
        if actions:
            recognized += 1
            status = "✅"
        else:
            status = "❌"
        
        print(f"{status} '{cmd}' → {len(actions)} acciones, {conf:.0%} confianza")
    
    print(f"\n📊 RESULTADOS:")
    print(f"   • Comandos reconocidos: {recognized}/{total} ({recognized*100//total}%)")
    print(f"   • Confianza promedio: {avg_confidence/total:.1%}")
    print(f"   • Tasa de éxito del parser: {recognized*100//total}%")


if __name__ == "__main__":
    print("\n" + "🚀 " * 35)
    print("     DEMOSTRACIONES: ZULY CLI INTERACTIVO")
    print("🚀 " * 35)
    
    demo_parser()
    demo_script_generation()
    demo_complex_commands()
    demo_statistics()
    
    print("\n" + "=" * 70)
    print("✅ DEMOSTRACIONES COMPLETADAS")
    print("=" * 70)
    print("\nPara usar modo interactivo:")
    print("  python zuly_cli_interactive.py")
    print("\n" + "=" * 70 + "\n")
