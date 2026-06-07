"""
ZULY Lab - CLI Principal
Interfaz de línea de comandos para el laboratorio
"""
import sys
import argparse
from pathlib import Path

# Agregar core al path
sys.path.insert(0, str(Path(__file__).parent))

from core.agent import Agent
from core.lab.exercise_runner import ExerciseRunner


def main():
    # Si se ejecuta desde Blender, filtrar argumentos
    if "--" in sys.argv:
        idx = sys.argv.index("--")
        # Mantener script name + argumentos después de --
        sys.argv = [sys.argv[0]] + sys.argv[idx+1:]

    parser = argparse.ArgumentParser(
        description='ZULY Laboratorio - Sistema de entrenamiento práctico'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Comandos disponibles')
    
    # Comando: run
    run_parser = subparsers.add_parser('run', help='Ejecutar un ejercicio')
    run_parser.add_argument('exercise', help='Código del ejercicio (ej: A1.1)')
    run_parser.add_argument('--mock', action='store_true', help='Usar MockAdapter')
    
    # Comando: run-all
    runall_parser = subparsers.add_parser('run-all', help='Ejecutar todos los ejercicios de una fase')
    runall_parser.add_argument('phase', help='Fase (A, B, C, D)')
    runall_parser.add_argument('--mock', action='store_true', help='Usar MockAdapter')
    
    # Comando: list
    list_parser = subparsers.add_parser('list', help='Listar ejercicios disponibles')
    list_parser.add_argument('--phase', help='Filtrar por fase (A, B, C, D)')
    
    # Comando: stats
    stats_parser = subparsers.add_parser('stats', help='Ver estadísticas')
    
    # Comando: validate
    validate_parser = subparsers.add_parser('validate', help='Validar un ejercicio')
    validate_parser.add_argument('exercise', help='Código del ejercicio')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Ejecutar comando
    if args.command == 'run':
        run_exercise(args.exercise, args.mock)
    
    elif args.command == 'run-all':
        run_all_phase(args.phase, args.mock)
    
    elif args.command == 'list':
        list_exercises(args.phase)
    
    elif args.command == 'stats':
        show_stats()
    
    elif args.command == 'validate':
        validate_exercise(args.exercise)


def run_exercise(exercise_code: str, use_mock: bool = False):
    """Ejecutar un ejercicio"""
    print("="*70)
    print("🧪 ZULY LABORATORIO")
    print("="*70)
    
    # Inicializar agent
    print(f"\n📦 Inicializando ZULY...")
    print(f"   Modo: {'MockAdapter (Simulación)' if use_mock else 'BlenderAdapter (Real)'}")
    
    agent = Agent(force_mock=use_mock)
    
    # Crear runner
    runner = ExerciseRunner(agent)
    
    # Ejecutar
    try:
        result = runner.execute_exercise(exercise_code)
        
        # Exit code según resultado
        sys.exit(0 if result['exito'] else 1)
    
    except Exception as e:
        print(f"\n❌ Error fatal: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def run_all_phase(phase: str, use_mock: bool = False):
    """Ejecutar todos los ejercicios de una fase"""
    print("="*70)
    print(f"🚀 ZULY LABORATORIO - Fase {phase}")
    print("="*70)
    
    agent = Agent(force_mock=use_mock)
    runner = ExerciseRunner(agent)
    
    try:
        results = runner.run_all_phase(phase)
        
        # Exit code según resultados
        all_success = all(r['exito'] for r in results)
        sys.exit(0 if all_success else 1)
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


def list_exercises(phase_filter: str = None):
    """Listar ejercicios disponibles"""
    lab_root = Path("ZULY_LAB")
    
    print("="*70)
    print("📋 EJERCICIOS DISPONIBLES")
    print("="*70)
    
    phases = {
        'A': 'A_estructura',
        'B': 'B_automatizacion',
        'C': 'C_render_tecnico',
        'D': 'D_integracion_real'
    }
    
    for phase_code, phase_dir in phases.items():
        if phase_filter and phase_filter != phase_code:
            continue
        
        print(f"\n📁 Fase {phase_code}: {phase_dir}")
        
        ejercicios_dir = lab_root / phase_dir / 'ejercicios'
        if not ejercicios_dir.exists():
            print("   (No hay ejercicios)")
            continue
        
        ejercicios = sorted(ejercicios_dir.glob("*.yaml"))
        
        if not ejercicios:
            print("   (No hay ejercicios)")
        
        for ex_file in ejercicios:
            code = ex_file.stem.split('_')[0]
            name = ' '.join(ex_file.stem.split('_')[1:]).title()
            print(f"   • {code}: {name}")


def show_stats():
    """Mostrar estadísticas de ejecución"""
    import json
    from collections import defaultdict
    
    logs_dir = Path("ZULY_LAB/logs_sesiones")
    
    if not logs_dir.exists() or not list(logs_dir.glob("*.json")):
        print("No hay logs de ejecución todavía.")
        print("Ejecuta algunos ejercicios primero con: python zuly_lab.py run A1.1")
        return
    
    print("="*70)
    print("📊 ESTADÍSTICAS DEL LABORATORIO")
    print("="*70)
    
    stats = defaultdict(lambda: {'total': 0, 'exitosos': 0, 'tiempo_promedio': 0})
    
    for log_file in logs_dir.glob("*.json"):
        with open(log_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        ejercicio = data['ejercicio']
        stats[ejercicio]['total'] += 1
        
        if data['exito']:
            stats[ejercicio]['exitosos'] += 1
        
        stats[ejercicio]['tiempo_promedio'] += data['tiempo_total_segundos']
    
    # Calcular promedios
    for ejercicio, data in stats.items():
        if data['total'] > 0:
            data['tiempo_promedio'] /= data['total']
    
    # Mostrar
    print(f"\nTotal de ejecuciones: {sum(s['total'] for s in stats.values())}")
    print(f"\nPor ejercicio:")
    
    for ejercicio in sorted(stats.keys()):
        data = stats[ejercicio]
        tasa = (data['exitosos'] / data['total']) * 100 if data['total'] > 0 else 0
        print(f"\n   {ejercicio}:")
        print(f"      Ejecuciones: {data['total']}")
        print(f"      Exitosas: {data['exitosos']} ({tasa:.1f}%)")
        print(f"      Tiempo promedio: {data['tiempo_promedio']:.2f}s")


def validate_exercise(exercise_code: str):
    """Validar un ejercicio"""
    print(f"🔍 Validando ejercicio {exercise_code}...")
    print("(Función en desarrollo)")


if __name__ == '__main__':
    main()
