"""
STRESS TEST ZULY 20 - VALIDAION V1 (WEEKEND 3)
==============================================
Suite de 20 pruebas reales para llevar a ZULY al límite.
Valida: V0, V1, NLU, Jerarquías y Rendimiento.
"""
import bpy
import sys
import os
from pathlib import Path
from datetime import datetime

# Agregar ZULY al path
zuly_path = Path(__file__).parent.parent
sys.path.insert(0, str(zuly_path))

from core.agent import Agent
from core.utils.logging import log_info, log_success, log_error

def run_stress_test():
    log_info("=" * 80)
    log_info("INICIANDO SUITE DE ESTRÉS: 20 PRUEBAS REALES (V1 VALIDATION)")
    log_info("=" * 80)

    # Inicializar Agente con Blender Real
    agent = Agent(force_mock=False)
    
    # BYPASS SEGURIDAD PARA STRESS TEST
    agent.authorized = True
    agent.operational_state = "Ejecución Directa" # Evitar bloqueos de estado
    
    from unittest.mock import MagicMock
    agent.human_gate.authorize = MagicMock(return_value={"action": "ALLOW", "risk": "LOW", "reason": "STRESS_TEST_BYPASS"})
    agent.context_guard.evaluate = MagicMock(return_value={"status": "PERMITIDO", "reason": "STRESS_TEST_BYPASS"})
    
    # Limpiar escena
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    tests = [
        # 1-3: Creación y Tipos (V1 Type Check)
        ("Crea un cubo llamado 'Cubo_Test'", "create"),
        ("Crea una esfera", "create"),
        ("Crea un cilindro", "create"),
        
        # 4-6: Jerarquías (V1 Hierarchy Check)
        ("Crea un cubo y llámalo 'Padre'", "create"),
        ("Crea una esfera y emparenta al 'Padre'", "hierarchy"), 
        ("Crea un cilindro y emparenta a la 'Esfera'", "hierarchy"),
        
        # 7-9: Transformaciones Genéricas (Nuevo NLU)
        ("Mueve el 'Padre' a 10 0 0", "transform"),
        ("Escala el 'Padre' a 2 2 2", "transform"),
        ("Rota el 'Padre' 90 0 0", "transform"),
        
        # 10-12: Iluminación y Cámaras
        ("Crea una luz solar", "create"),
        ("Crea una camara", "create"),
        ("Mueve la 'Camera' a 15 -15 10", "transform"),
        
        # 13-15: Materiales y Propiedades
        ("Dale al 'Cilindro' un material de 'oro'", "property"),
        ("Haz que la 'Esfera' sea invisible", "property"),
        ("Rename 'Cubo_Test' to 'Cubo_Final'", "property"),
        
        # 16-18: Estructuras y NLU
        ("Crea un plano", "create"),
        ("Mueve el 'Plano' a 0 0 -5", "transform"),
        ("Renderiza la escena", "render"),
        
        # 19-20: Persistencia
        ("Guardar el proyecto", "system"),
        ("Obtener informacion del sistema", "system")
    ]

    results = []
    
    for i, (request, expected_effect) in enumerate(tests, 1):
        log_info(f"\n[TEST {i}/20] Petición: '{request}'")
        try:
            # Diagnóstico de escena PRE
            objs_pre = [obj.name for obj in bpy.data.objects]
            log_info(f"  Diagnóstico Escena (PRE): {len(objs_pre)} objetos -> {objs_pre}")
            
            result = agent.process_natural_request(request)
            
            # Diagnóstico de escena POST
            objs_post = [obj.name for obj in bpy.data.objects]
            log_info(f"  Diagnóstico Escena (POST): {len(objs_post)} objetos -> {objs_post}")
            
            # Verificar validaciones (Extraer del último intento en results)
            results_list = result.get('results', [])
            last_attempt = results_list[-1] if results_list else {}
            
            v1_data = last_attempt.get('validation_v1', {})
            v1 = v1_data.get('verified', False) if isinstance(v1_data, dict) else False
            
            v0_data = last_attempt.get('validation_v0', {})
            v0 = v0_data.get('verified', False) if isinstance(v0_data, dict) else False
            
            status = "✅ PASS" if result.get('success') and v0 and v1 else "❌ FAIL"
            if not v1 and v0:
                status = "⚠️ V1 FAIL (Estructural)"
            
            if not result.get('success'):
                status = f"❌ FAIL ({result.get('error', 'Unknown Error')})"
            
            log_info(f"  Resultado: {status}")
            log_info(f"  V0: {'OK' if v0 else 'FAIL'} | V1: {'OK' if v1 else 'FAIL'}")
            
            results.append({
                'num': i,
                'request': request,
                'success': result.get('success', False),
                'v0': v0,
                'v1': v1,
                'details': result.get('feedback', '')
            })
        except Exception as e:
            log_error(f"  Error crítico en test {i}: {e}")
            results.append({'num': i, 'request': request, 'success': False, 'error': str(e)})

    # Reporte Final
    log_info("\n" + "=" * 80)
    log_info("RESUMEN DE PRUEBAS DE ESTRÉS")
    log_info("=" * 80)
    
    passed_v0 = sum(1 for r in results if r.get('v0'))
    passed_v1 = sum(1 for r in results if r.get('v1'))
    
    log_info(f"Total Tests: {len(tests)}")
    log_info(f"V0 (Existencial) Pasados: {passed_v0}/{len(tests)}")
    log_info(f"V1 (Estructural) Pasados: {passed_v1}/{len(tests)}")
    log_info("=" * 80)
    
    # Guardar reporte en bitácora
    report_path = zuly_path / "bitacora" / f"REPORTE_ESTRES_V1_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(f"# Reporte de Estrés ZULY V1 - {datetime.now()}\n\n")
        f.write("| # | Petición | Éxito | V0 | V1 | Detalle |\n")
        f.write("|---|-----------|-------|----|----|---------|\n")
        for r in results:
            f.write(f"| {r['num']} | {r['request']} | {'✅' if r['success'] else '❌'} | {'✅' if r.get('v0') else '❌'} | {'✅' if r.get('v1') else '❌'} | {r.get('details', r.get('error', ''))} |\n")

    log_success(f"Reporte detallado guardado en: {report_path}")

if __name__ == "__main__":
    run_stress_test()
