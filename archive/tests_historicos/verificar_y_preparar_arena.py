import sys
import os
from core.agent import Agent
from core.jues_controller import get_jues_controller

def ejecutar_orden_maestra():
    print("🚀 INICIANDO ORDEN MAESTRA DE VERIFICACIÓN (ARENA)")
    print("---------------------------------------------------")
    
    # Inicializar Agente en modo REAL
    agent = Agent(force_mock=False)
    jues = get_jues_controller()
    
    # Lista de objetivos basada en la Hoja de Ruta de Prioridad Alta
    objetivos = [
        {"id": "P-001", "cmd": "crear un cubo", "desc": "Primitiva Cubo"},
        {"id": "P-002", "cmd": "crear una esfera", "desc": "Primitiva Esfera"},
        {"id": "P-004", "cmd": "crear un cilindro", "desc": "Primitiva Cilindro"},
        {"id": "P-006", "cmd": "crear un plano", "desc": "Primitiva Plano"},
        {"id": "CUB-001", "cmd": "crear un cubo con bisel realista", "desc": "Cubo Biselado (Bevel)"},
        {"id": "ARC-003", "cmd": "crear una ventana rectangular segun ADN casarural", "desc": "Ventana Arq"},
        {"id": "ARC-004", "cmd": "crear una puerta de entrada segun ADN casarural", "desc": "Puerta Arq"},
    ]

    resultados = []

    for obj in objetivos:
        print(f"\n[PROCESANDO {obj['id']}] -> {obj['desc']}")
        
        # 1. Ejecución en la Arena
        result = agent.process_natural_request(obj['cmd'])
        
        if result['success']:
            # 2. Validación automática JUES
            # Intentamos localizar el archivo .blend generado en temp_arena o ZULY_PROJECTS
            path_blend = result.get('scene_state', {}).get('last_save', "")
            
            if os.path.exists(path_blend):
                print(f"✅ Archivo generado: {os.path.basename(path_blend)}")
                calificacion = jues.validar_y_decidir(path_blend, obj['id'])
                
                print(f"📊 JUES Score: {calificacion.get('score', 0)}/100")
                print(f"📋 Dictamen: {calificacion.get('status', 'ERROR')}")
                
                resultados.append({
                    "id": obj['id'],
                    "status": calificacion.get('status'),
                    "score": calificacion.get('score')
                })
            else:
                print(f"⚠️ Error: No se encontró el archivo .blend para {obj['id']}")
        else:
            print(f"❌ Error al ejecutar el comando: {result.get('error')}")

    print("\n---------------------------------------------------")
    print("🏁 RESUMEN DE LA ORDEN")
    for res in resultados:
        icon = "✅" if res['score'] >= 85 else "⚠️"
        print(f"{icon} {res['id']}: {res['score']} pts - {res['status']}")
    
    print("\n💡 INSTRUCCIÓN PARA EL SOBERANO:")
    print("Revisa la carpeta 'archivo_zuly/temp_arena/'. Si estás conforme, di: 'zuly approve <ID>'")

if __name__ == "__main__":
    ejecutar_orden_maestra()