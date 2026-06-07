"""
scripts/zuly_lab_scanner_test.py
ZULY QA - Reto 6.8 - ZULY LAB
Entorno de prueba donde Zuly audita un modelo externo para ingeniería inversa.
"""

import sys
ZULY_PATH = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL"
if ZULY_PATH not in sys.path:
    sys.path.insert(0, ZULY_PATH)

from core.agent import Agent
from core.utils.logging import log_info, log_success

def test_inverse_engineering():
    log_info("=" * 50)
    log_info("BIENVENIDOS A ZULY LAB - INGENIERÍA INVERSA")
    log_info("=" * 50)
    
    agent = Agent()
    
    # Asumimos que el modelo ya está cargado por línea de comandos.
    # Procedemos a "mirarlo" cognitivamente.
    log_info("Iniciando escáner en escena cargada...")
    
    import sys
    output_name = sys.argv[-1] if len(sys.argv) > 1 and not sys.argv[-1].endswith('.py') else 'learned_pattern_v1'
    
    result = agent.execute_via_router('blender.scan_and_learn', {
        'output_name': output_name
    })
    
    if result.get('status') == 'success' or result.get('success') == True or result.get('result', {}).get('success') == True:
        log_success("¡ADN extraído con éxito!")
        print(f"Patrón extraído en: {result.get('result', {}).get('saved_path')}")
        
        # Opcional: imprimir el JSON extraído
        import json
        pattern_data = result.get('result', {}).get('pattern_data', {})
        print("\n=== RESUMEN DE COMPRENSIÓN ZULY ===")
        print(f"Mallas leídas: {len(pattern_data.get('objects', []))}")
        if pattern_data.get('objects'):
            first_obj = pattern_data['objects'][0]
            print(f"Primer objeto base detectado: {first_obj['name']} ({first_obj['type']})")
            print(f"Dimensiones: {first_obj['dimensions']}")
            print(f"Nro. modificadores encontrados: {len(first_obj['modifiers'])}")
            
    else:
        print("El escaneo ha fallado.")

if __name__ == "__main__":
    test_inverse_engineering()
