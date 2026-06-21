import sys
import time
import pprint
from core.agent import Agent

# ASCII Art
ZULY_BANNER = """
===================================================================
  ______   _   _   _      __   __       ____   _       ___ 
 |__  / | | | | | | |     \\ \\ / /      / ___| | |     |_ _|
   / /| | | | | | | |      \\ V /      | |     | |      | | 
  / /_| |_| | | |___|       | |       | |___  | |___   | | 
 /____|\\___/  |_____|       |_|        \\____| |_____| |___|
                                                           
 ZULY INTERACTIVE CLI v1.1 - Sistema Arquitectónico Experto
 Escribe 'exit' para salir, 'status' para ver memoria, 'help' comandos.
===================================================================
"""

def main():
    print(ZULY_BANNER)
    print("[*] Iniciando entorno cognitivo Zuly...")
    
    # Inicializar el Agente
    # Cambiar force_mock a False cuando se use en producción con Blender
    force_mock = '--mock' in sys.argv
    agent = Agent(force_mock=force_mock)
    
    print("[✓] Zuly está en línea y lista para recibir órdenes.")
    print("-" * 65)
    
    while True:
        try:
            # Leer orden
            user_input = input("\n> ZULY: ").strip()
            
            if not user_input:
                continue
                
            command_lower = user_input.lower()
            
            if command_lower in ['exit', 'quit', 'salir']:
                print("\n[!] Cerrando sesión de Zuly... ¡Hasta luego!")
                break
                
            elif command_lower == 'status':
                summary = agent.context.get_summary()
                print("\n[ESTADO DE MEMORIA Y SESIÓN]")
                pprint.pprint(summary)
                continue
                
            elif command_lower == 'history':
                print("\n[HISTORIAL DE COMANDOS]")
                if not agent.context.execution_history:
                    print("  No hay historial en esta sesión.")
                for i, record in enumerate(agent.context.execution_history, 1):
                    print(f"  {i}. {record['command']} -> {'Éxito' if record['success'] else 'Fallido'}")
                continue
                
            elif command_lower == 'help':
                print("\n[AYUDA]")
                print("  - Puedes escribir órdenes naturales: 'crea un cubo y muevelo a la derecha'")
                print("  - Tareas complejas: 'descomponer: crea una sala con piso, techo y pilares'")
                print("  - Comandos del sistema: status, history, exit")
                continue
                
            # Enrutamiento al Agente
            print("\n[Procesando...]")
            start_time = time.time()
            result = agent.process_natural_request(user_input)
            elapsed = time.time() - start_time
            
            if result.get('success'):
                print(f"✅ ÉXITO ({elapsed:.2f}s)")
                print(f"   Feedback: {result.get('feedback', 'Comando ejecutado correctamente.')}")
                if 'output' in result:
                    print(f"   Resultado: {result['output']}")
            elif result.get('status') == 'requires_confirmation':
                print(f"⚠️  ALERTA DE SEGURIDAD ({elapsed:.2f}s)")
                print(f"   {result.get('feedback', 'Comando riesgoso.')}")
                confirm = input("   ¿Continuar de todos modos? (s/n): ").strip().lower()
                if confirm == 's':
                    print("\n[Ejecución Forzada...]")
                    # Agregamos un modificador oculto al final
                    forced_input = user_input + " --force-execute"
                    result2 = agent.process_natural_request(forced_input)
                    if result2.get('success'):
                        print(f"✅ ÉXITO FORZADO")
                        print(f"   Feedback: {result2.get('feedback', 'Comando ejecutado correctamente.')}")
                    else:
                        print(f"❌ FALLÓ")
                        print(f"   Motivo: {result2.get('error', 'Error desconocido')}")
                else:
                    print("🚫 Operación cancelada por el usuario.")
            else:
                print(f"❌ FALLÓ ({elapsed:.2f}s)")
                print(f"   Motivo: {result.get('error', 'Error desconocido')}")
                if 'feedback' in result:
                    print(f"   Zuly dice: {result['feedback']}")
                if 'suggestion' in result:
                    print(f"   Sugerencia: {result['suggestion']}")
                    
        except KeyboardInterrupt:
            print("\n[!] Operación cancelada. Escribe 'exit' para salir completamente.")
        except Exception as e:
            print(f"\n[ERROR CRÍTICO] {str(e)}")

if __name__ == "__main__":
    main()
