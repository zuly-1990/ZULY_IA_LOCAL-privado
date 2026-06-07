#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
demo_agent.py

Script de demostración del Agente Zuly con IA.
Muestra ejemplos de uso, capacidades de NLU, manejo de errores,
monitoreo de escena y modo interactivo.

Ejecución:
    python demo_agent.py

Cada función demo_X_... muestra una característica específica.
"""

import sys
from pathlib import Path

# Agregar al path
sys.path.insert(0, str(Path(__file__).parent))

from core.agent import Agent
from core.utils.logging import log


def print_header(title):
    """Imprime un encabezado formateado para la consola."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def print_section(title):
    """Imprime un título de sección para separar bloques de demo."""
    print(f"\n{'-' * 80}")
    print(f"  {title}")
    print(f"{'-' * 80}\n")


def demo_1_basic_requests():
    """Demostración 1: Peticiones básicas en lenguaje natural."""
    print_section("Demo 1: Peticiones Básicas en Lenguaje Natural")
    
    agent = Agent(auto_monitor=False)
    
    peticiones = [
        "Crea un cubo",
        "Necesito una esfera",
        "Quiero un cilindro",
    ]
    
    for peticion in peticiones:
        print(f"Petición: '{peticion}'")
        result = agent.process_natural_request(peticion)
        print(f"Resultado: {result['feedback']}")
        print()


def demo_2_complex_requests():
    """Demostración 2: Peticiones complejas con múltiples elementos."""
    print_section("Demo 2: Peticiones Complejas")
    
    agent = Agent(auto_monitor=False)
    
    peticion = "Crea una escena con un cubo de oro y una esfera plateada, iluminada con luz solar"
    print(f"Petición: '{peticion}'")
    result = agent.process_natural_request(peticion)
    print(f"Resultado: {result['feedback']}")
    
    print(f"\nDetalles de ejecución:")
    print(f"  • Comando ejecutado: {result['command_executed']}")
    print(f"  • Confianza: {result['confidence']:.0%}")
    print(f"  • Parámetros extraídos: {result['parameters']}")


def demo_3_parameter_extraction():
    """Demostración 3: Extracción de parámetros."""
    print_section("Demo 3: Extracción de Parámetros")
    
    agent = Agent(auto_monitor=False)
    
    peticiones = [
        "Coloca el cubo en la posición 5, 3, 2",
        "Crea una esfera con radio 2",
        "Aplica un material de oro a la esfera",
        "Añade una luz con energía 5",
    ]
    
    for peticion in peticiones:
        print(f"Petición: '{peticion}'")
        intents = agent.nlu.process(peticion)
        if intents:
            intent = intents[0]
            print(f"  Comando: {intent.command_name}")
            print(f"  Parámetros: {intent.parameters}")
        print()


def demo_4_nlu_capabilities():
    """Demostración 4: Capacidades del NLU."""
    print_section("Demo 4: Capacidades de Lenguaje Natural")
    
    agent = Agent(auto_monitor=False)
    
    print("Sinónimos reconocidos:\n")
    
    ejemplos = [
        ("cubo = box = cube", "Crea un cubo"),
        ("esfera = sphere = ball", "Necesito una esfera"),
        ("luz = light = iluminacion", "Añade una luz"),
        ("material = textura", "Aplica un material dorado"),
        ("posicion = location = pos", "Mueve a la posición 5,3,0"),
    ]
    
    for explanation, example in ejemplos:
        print(f"  {explanation}")
        print(f"    Ejemplo: '{example}'")
        intents = agent.nlu.process(example)
        if intents:
            print(f"    → {intents[0].command_name}")
        print()


def demo_5_scene_monitoring():
    """Demostración 5: Monitoreo de escena."""
    print_section("Demo 5: Monitoreo de Escena")
    
    agent = Agent(auto_monitor=True)
    
    print("Creando objetos y monitoreando escena:\n")
    
    peticiones = [
        "Crea un cubo",
        "Necesito una esfera",
        "Añade una luz",
    ]
    
    for peticion in peticiones:
        print(f"Ejecutando: '{peticion}'")
        result = agent.process_natural_request(peticion)
        
        if result['scene_state']:
            scene = result['scene_state']
            print(f"  → Escena: {scene['object_count']} objeto(s), " 
                  f"{scene['light_count']} luz(ces)")
        print()


def demo_6_error_handling():
    """Demostración 6: Manejo de errores y corrección automática."""
    print_section("Demo 6: Manejo de Errores y Corrección Automática")
    
    agent = Agent(auto_monitor=False)
    
    print("Intentando comandos con errores intencionales:\n")
    
    peticiones_erroneas = [
        "creaaa un cuboooo",
        "Necesito una esferaaaa",
        "cylindro por favor",
    ]
    
    for peticion in peticiones_erroneas:
        print(f"Petición (con error): '{peticion}'")
        result = agent.process_natural_request(peticion)
        
        if result.get('suggestion'):
            print(f"  ✓ Sugerencia: '{result['suggestion']}' "
                  f"(similitud: {result.get('similarity', 0):.0%})")
        
        print(f"  → {result['feedback']}")
        print()


def demo_7_command_listing():
    """Demostración 7: Listar comandos disponibles."""
    print_section("Demo 7: Comandos Disponibles")
    
    agent = Agent(auto_monitor=False)
    
    commands = agent.get_available_commands()
    
    print(f"Total de comandos disponibles: {len(commands)}\n")
    
    # Agrupar por tipo
    categories = {}
    for cmd_name in commands.keys():
        if 'primitiva' in cmd_name or 'primitva' in cmd_name:
            cat = 'Primitivas'
        elif 'transformar' in cmd_name:
            cat = 'Transformaciones'
        elif 'material' in cmd_name:
            cat = 'Materiales'
        elif 'luz' in cmd_name or 'anadir' in cmd_name:
            cat = 'Iluminación'
        elif 'camara' in cmd_name or 'camera' in cmd_name:
            cat = 'Cámara'
        elif 'render' in cmd_name or 'export' in cmd_name:
            cat = 'Rendering/Exportación'
        else:
            cat = 'Otros'
        
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(cmd_name)
    
    for category, cmds in sorted(categories.items()):
        print(f"{category}:")
        for cmd in sorted(cmds):
            desc = commands[cmd][:60] + ("..." if len(commands[cmd]) > 60 else "")
            print(f"  • {cmd}: {desc}")
        print()


def demo_8_session_tracking():
    """Demostración 8: Rastreo de sesión."""
    print_section("Demo 8: Rastreo de Sesión")
    
    agent = Agent(auto_monitor=False)
    
    print("Ejecutando múltiples comandos:\n")
    
    peticiones = [
        "Crea un cubo",
        "Crea una esfera",
        "Crea un cilindro",
        "Añade una luz",
    ]
    
    for peticion in peticiones:
        result = agent.process_natural_request(peticion)
        success_str = "✓" if result['success'] else "✗"
        print(f"{success_str} {peticion}")
    
    print("\nResumen de sesión:")
    summary = agent.get_session_summary()
    print(f"  Comandos ejecutados: {summary['commands_executed']}")
    print(f"  Exitosos: {summary['successes']}")
    print(f"  Fallidos: {summary['failures']}")
    
    print("\nExportando reporte...")
    report_path = agent.export_session_report()
    print(f"✓ Reporte guardado en: {report_path}")


def demo_9_nlu_processing():
    """Demostración 9: Procesamiento detallado de NLU."""
    print_section("Demo 9: Procesamiento Detallado de NLU")
    
    agent = Agent(auto_monitor=False)
    
    peticion = "Quiero una escena con un cubo de oro y una esfera plateada, iluminada desde arriba"
    
    print(f"Petición: '{peticion}'\n")
    print("Procesando con NLU...\n")
    
    intents = agent.nlu.process(peticion)
    
    print(f"Intenciones detectadas: {len(intents)}\n")
    
    for i, intent in enumerate(intents, 1):
        print(f"Intención {i}:")
        print(f"  Comando: {intent.command_name}")
        print(f"  Confianza: {intent.confidence:.0%}")
        print(f"  Parámetros: {intent.parameters}")
        print()


def demo_10_interactive():
    """Demostración 10: Modo interactivo."""
    print_section("Demo 10: Modo Interactivo")
    
    agent = Agent(auto_monitor=True)
    
    print("Modo interactivo del Agente Zuly")
    print("Escribe 'salir' para terminar, 'comandos' para ver disponibles\n")
    
    while True:
        try:
            peticion = input("Petición: ").strip()
            
            if not peticion:
                continue
            
            if peticion.lower() == 'salir':
                print("¡Hasta luego!")
                break
            
            if peticion.lower() == 'comandos':
                commands = agent.get_available_commands()
                print(f"\nComandos disponibles ({len(commands)}):")
                for cmd in sorted(commands.keys())[:10]:
                    print(f"  • {cmd}")
                if len(commands) > 10:
                    print(f"  ... y {len(commands) - 10} más")
                print()
                continue
            
            result = agent.process_natural_request(peticion)
            print(f"Resultado: {result['feedback']}")
            
            if result['scene_state']:
                scene = result['scene_state']
                print(f"[Escena: {scene['object_count']} objeto(s), "
                      f"{scene['light_count']} luz(ces)]")
            print()
        
        except KeyboardInterrupt:
            print("\n\n¡Hasta luego!")
            break
        except Exception as e:
            print(f"Error: {e}")


def main():
    """Función principal: menú de selección de demostraciones."""
    print_header("DEMOSTRACIÓN: AGENTE ZULY CON CAPACIDADES DE IA")
    
    demos = [
        ("1", "Peticiones Básicas", demo_1_basic_requests),
        ("2", "Peticiones Complejas", demo_2_complex_requests),
        ("3", "Extracción de Parámetros", demo_3_parameter_extraction),
        ("4", "Capacidades de Lenguaje Natural", demo_4_nlu_capabilities),
        ("5", "Monitoreo de Escena", demo_5_scene_monitoring),
        ("6", "Manejo de Errores", demo_6_error_handling),
        ("7", "Comandos Disponibles", demo_7_command_listing),
        ("8", "Rastreo de Sesión", demo_8_session_tracking),
        ("9", "Procesamiento Detallado NLU", demo_9_nlu_processing),
        ("10", "Modo Interactivo", demo_10_interactive),
    ]
    
    print("Demostraciones disponibles:\n")
    for num, title, _ in demos:
        print(f"  {num}. {title}")
    
    print("\n" + "-" * 80)
    print("Opciones:")
    print("  • Ingresa un número (1-10) para ejecutar esa demostración")
    print("  • Ingresa 'all' para ejecutar todas")
    print("  • Ingresa 'q' para salir")
    print("-" * 80 + "\n")
    
    while True:
        try:
            choice = input("Selecciona una opción: ").strip().lower()
            
            if choice == 'q':
                print("¡Hasta luego!")
                break
            
            if choice == 'all':
                for num, title, demo_func in demos:
                    try:
                        demo_func()
                    except Exception as e:
                        print(f"Error en demostración {num}: {e}")
                    input("\nPresiona Enter para continuar...")
                
                print_header("FIN DE LAS DEMOSTRACIONES")
                break
            
            try:
                demo_num = int(choice)
                if 1 <= demo_num <= len(demos):
                    _, title, demo_func = demos[demo_num - 1]
                    demo_func()
                    input("\nPresiona Enter para volver al menú...")
                else:
                    print(f"Selecciona un número entre 1 y {len(demos)}")
            except ValueError:
                print("Entrada inválida. Intenta de nuevo.")
        
        except KeyboardInterrupt:
            print("\n¡Hasta luego!")
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"\nError fatal: {e}", file=sys.stderr)
        sys.exit(1)
