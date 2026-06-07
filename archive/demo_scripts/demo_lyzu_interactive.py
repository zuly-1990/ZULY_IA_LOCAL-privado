#!/usr/bin/env python3
"""Demo interactivo mejorado de LYZU Core"""

from lyzu_core import LYZUCore

def main():
    print("\n" + "=" * 70)
    print("🤖 LYZU Core 1.0 - Demostración Interactiva")
    print("=" * 70)
    print("\nModo: HYBRID (Humano-en-Loop)")
    print("\nEjemplos de órdenes:")
    print("  • 'Crea un cubo'")
    print("  • 'Crea una esfera roja'")
    print("  • 'Mueve el cubo a 5,10,15'")
    print("  • 'Renderiza'")
    print("  • 'Salir' para terminar\n")
    print("-" * 70 + "\n")
    
    lyzu = LYZUCore(mode='hybrid')
    
    while True:
        try:
            user_input = input("👤 You: ").strip()
            
            if user_input.lower() in ['exit', 'salir', 'quit']:
                print("\n✅ Sesión guardada. ¡Adiós!")
                lyzu.save_session()
                break
            
            if not user_input:
                continue
            
            # Procesar entrada
            result = lyzu.process_user_input(user_input)
            
            if result.get('pending_approval'):
                print(f"\n🤖 LYZU (Pending Approval):")
                print(f"   Intent: {result['intent']}")
                print(f"   Confidence: {result['confidence']:.1%}")
                print(f"   Description: {result.get('description', 'N/A')}")
                print(f"   Command: {result['command']['command']}")
                
                approval = input("\n   ¿Aprobar? (s/n): ").strip().lower()
                if approval in ['s', 'y', 'yes']:
                    exec_result = lyzu.approve_and_execute(
                        result['command'],
                        result['command'].get('parameters', {})
                    )
                    print(f"   ✓ Ejecutado: {exec_result.get('success', False)}")
                else:
                    print("   ✗ Cancelado por usuario")
            else:
                success = result.get('success')
                if success:
                    print(f"🤖 LYZU: ✓ Exitoso")
                    print(f"   Output: {result.get('output', 'N/A')}")
                elif success is False:
                    print(f"🤖 LYZU: ❌ Error")
                    print(f"   Error: {result.get('error', 'Unknown error')}")
                else:
                    print(f"🤖 LYZU: ⏳ Pendiente")
            
            print(f"   ⏱️  {result.get('execution_time_ms', 0):.1f}ms\n")
            
        except KeyboardInterrupt:
            print("\n\n✅ Sesión guardada. ¡Adiós!")
            lyzu.save_session()
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")

if __name__ == '__main__':
    main()
