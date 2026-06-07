"""
core/diagnostics/run_diagnostics.py

Script principal para ejecutar diagnóstico completo de ZULY.
FASE 22: Auto-Diagnóstico Controlado.

Uso:
    python -m core.diagnostics.run_diagnostics
    python core/diagnostics/run_diagnostics.py --save export/diagnostics/
"""

import argparse
from pathlib import Path
from datetime import datetime

from .system_health_checker import SystemHealthChecker
from .module_validator import ModuleValidator
from .diagnostic_reporter import DiagnosticReporter, IssueSeverity


def run_full_diagnostics(project_root: Path, save_path: Path = None) -> DiagnosticReporter:
    """
    Ejecuta diagnóstico completo del sistema.
    
    Args:
        project_root: Raíz del proyecto
        save_path: Directorio donde guardar reporte (opcional)
        
    Returns:
        DiagnosticReporter con resultados
    """
    print("[*] Iniciando diagnostico completo de ZULY...")
    print(f"   Proyecto: {project_root}")
    print()
    
    # 1. Health Checks
    print("[>] Ejecutando health checks...")
    health_checker = SystemHealthChecker(project_root)
    health_report = health_checker.run_all_checks()
    
    # 2. Module Validation
    print("[>] Validando modulos...")
    module_validator = ModuleValidator(project_root)
    module_checks = module_validator.run_all_validations()
    
    # Agregar module checks al health report
    for check in module_checks:
        health_report.add_check(check)
    
    # 3. Generar reporte
    print("[>] Generando reporte...")
    reporter = DiagnosticReporter.from_health_report(health_report)
    
    # 4. Mostrar resultados
    print()
    print("=" * 60)
    print("RESULTADOS DEL DIAGNÓSTICO")
    print("=" * 60)
    print(f"Estado general: {reporter.determine_overall_health()}")
    print(f"Total issues: {len(reporter.issues)}")
    print(f"  - CRITICAL: {sum(1 for i in reporter.issues if i.severity == IssueSeverity.CRITICAL)}")
    print(f"  - SERIOUS: {sum(1 for i in reporter.issues if i.severity == IssueSeverity.SERIOUS)}")
    print(f"  - MINOR: {sum(1 for i in reporter.issues if i.severity == IssueSeverity.MINOR)}")
    print()
    
    # Mostrar issues
    if reporter.issues:
        print("Issues detectados:")
        for issue in reporter.issues:
            icon = "[!]" if issue.severity == IssueSeverity.CRITICAL else "[*]" if issue.severity == IssueSeverity.SERIOUS else "[i]"
            print(f"  {icon} [{issue.severity.value}] {issue.component}: {issue.message}")
        print()
    
    # Mostrar recomendaciones
    recommendations = reporter.generate_recommendations()
    if recommendations:
        print("Recomendaciones:")
        for rec in recommendations:
            print(f"  -> {rec}")
        print()
    
    # 5. Guardar si se especificó
    if save_path:
        save_dir = Path(save_path)
        save_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = save_dir / f"diagnostic_report_{timestamp}.json"
        
        reporter.save_to_file(report_file)
        print(f"✅ Reporte guardado: {report_file}")
        print()
    
    print("=" * 60)
    print()
    
    return reporter


def main():
    """Punto de entrada principal."""
    parser = argparse.ArgumentParser(description="Ejecutar diagnóstico completo de ZULY")
    parser.add_argument(
        '--save',
        type=str,
        help="Directorio donde guardar reporte JSON"
    )
    parser.add_argument(
        '--root',
        type=str,
        help="Raíz del proyecto (auto-detecta si no se especifica)"
    )
    
    args = parser.parse_args()
    
    # Determinar project root
    if args.root:
        project_root = Path(args.root)
    else:
        # Auto-detectar (asume que estamos en core/diagnostics/)
        project_root = Path(__file__).parent.parent.parent
    
    # Determinar save path
    save_path = Path(args.save) if args.save else None
    
    # Ejecutar diagnóstico
    reporter = run_full_diagnostics(project_root, save_path)
    
    # Exit code según salud
    health = reporter.determine_overall_health()
    if health == "CRITICAL":
        exit(2)
    elif health == "WARNING":
        exit(1)
    else:
        exit(0)


if __name__ == "__main__":
    main()
