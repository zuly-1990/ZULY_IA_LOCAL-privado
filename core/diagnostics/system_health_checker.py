"""
core/diagnostics/system_health_checker.py

Verificación de salud del sistema.
FASE 22: Auto-Diagnóstico Controlado.

Verifica:
- Blender disponible y versión correcta
- Rutas críticas existen
- Permisos de escritura
- Versiones de dependencias
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from pathlib import Path
import sys
from datetime import datetime


@dataclass
class CheckResult:
    """Resultado de una verificación individual."""
    name: str
    passed: bool
    message: str
    details: Optional[Dict[str, Any]] = None
    severity: str = "MINOR"  # MINOR, SERIOUS, CRITICAL


class HealthReport:
    """Reporte consolidado de salud del sistema."""
    
    def __init__(self):
        self.timestamp = datetime.now().isoformat()
        self.checks: List[CheckResult] = []
        self.overall_status = "OK"  # OK, WARNING, CRITICAL
    
    def add_check(self, check: CheckResult):
        """Agrega resultado de check."""
        self.checks.append(check)
        
        # Actualizar estado general
        if not check.passed:
            if check.severity == "CRITICAL" and self.overall_status != "CRITICAL":
                self.overall_status = "CRITICAL"
            elif check.severity == "SERIOUS" and self.overall_status == "OK":
                self.overall_status = "WARNING"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte a diccionario."""
        return {
            'timestamp': self.timestamp,
            'system_health': self.overall_status,
            'checks_performed': len(self.checks),
            'checks_passed': sum(1 for c in self.checks if c.passed),
            'checks_failed': sum(1 for c in self.checks if not c.passed),
            'checks': [
                {
                    'name': c.name,
                    'passed': c.passed,
                    'message': c.message,
                    'severity': c.severity,
                    'details': c.details or {}
                }
                for c in self.checks
            ]
        }


class SystemHealthChecker:
    """Verificador de salud del sistema."""
    
    def __init__(self, project_root: Optional[Path] = None):
        """
        Inicializa el verificador.
        
        Args:
            project_root: Raíz del proyecto (auto-detecta si None)
        """
        if project_root is None:
            # Auto-detectar raíz (asume que __file__ está en core/diagnostics/)
            self.project_root = Path(__file__).parent.parent.parent
        else:
            self.project_root = Path(project_root)
    
    def check_blender_availability(self) -> CheckResult:
        """Verifica si Blender está disponible."""
        try:
            from core.adapters.blender_adapter import BlenderAdapter
            
            adapter = BlenderAdapter()
            is_available = adapter.is_available()
            
            if is_available:
                info = adapter.get_engine_info()
                version = info.get('version', 'unknown')
                
                return CheckResult(
                    name="blender_availability",
                    passed=True,
                    message=f"Blender disponible (versión {version})",
                    details={'version': version, 'info': info},
                    severity="MINOR"
                )
            else:
                return CheckResult(
                    name="blender_availability",
                    passed=False,
                    message="Blender no disponible (modo simulación)",
                    details={'mock_mode': True},
                    severity="MINOR"  # No crítico, puede usar mock
                )
        
        except Exception as e:
            return CheckResult(
                name="blender_availability",
                passed=False,
                message=f"Error verificando Blender: {e}",
                details={'error': str(e)},
                severity="SERIOUS"
            )
    
    def check_critical_paths(self) -> CheckResult:
        """Verifica que existan rutas críticas."""
        critical_paths = [
            'core',
            'tests',
            'export',
            'bitacora',
            'core/adapters',
            'core/reasoning',
            'core/memory',
        ]
        
        missing_paths = []
        for path_str in critical_paths:
            path = self.project_root / path_str
            if not path.exists():
                missing_paths.append(path_str)
        
        if not missing_paths:
            return CheckResult(
                name="critical_paths",
                passed=True,
                message=f"Todas las rutas críticas existen ({len(critical_paths)} verificadas)",
                details={'paths_checked': critical_paths},
                severity="MINOR"
            )
        else:
            return CheckResult(
                name="critical_paths",
                passed=False,
                message=f"Rutas faltantes: {', '.join(missing_paths)}",
                details={'missing': missing_paths, 'checked': critical_paths},
                severity="CRITICAL"
            )
    
    def check_write_permissions(self) -> CheckResult:
        """Verifica permisos de escritura en directorios importantes."""
        write_paths = [
            'export',
            'bitacora',
        ]
        
        permission_issues = []
        for path_str in write_paths:
            path = self.project_root / path_str
            if path.exists():
                # Intentar crear archivo temporal
                try:
                    test_file = path / '.zuly_write_test'
                    test_file.touch()
                    test_file.unlink()  # Eliminar inmediatamente
                except Exception as e:
                    permission_issues.append({'path': path_str, 'error': str(e)})
            else:
                permission_issues.append({'path': path_str, 'error': 'Path does not exist'})
        
        if not permission_issues:
            return CheckResult(
                name="write_permissions",
                passed=True,
                message=f"Permisos de escritura OK ({len(write_paths)} paths)",
                details={'paths_checked': write_paths},
                severity="MINOR"
            )
        else:
            return CheckResult(
                name="write_permissions",
                passed=False,
                message=f"Problemas de permisos en {len(permission_issues)} paths",
                details={'issues': permission_issues},
                severity="SERIOUS"
            )
    
    def check_python_version(self) -> CheckResult:
        """Verifica versión de Python."""
        version = sys.version_info
        version_str = f"{version.major}.{version.minor}.{version.micro}"
        
        # ZULY requiere Python 3.10+
        if version.major == 3 and version.minor >= 10:
            return CheckResult(
                name="python_version",
                passed=True,
                message=f"Python {version_str} (compatible)",
                details={'version': version_str, 'required': '3.10+'},
                severity="MINOR"
            )
        else:
            return CheckResult(
                name="python_version",
                passed=False,
                message=f"Python {version_str} (requiere 3.10+)",
                details={'version': version_str, 'required': '3.10+'},
                severity="CRITICAL"
            )
    
    def check_core_modules(self) -> CheckResult:
        """Verifica que módulos core estén importables."""
        # Módulos actualizados para reflejar arquitectura real de ZULY
        # FASE 22: Lista actualizada con módulos existentes
        core_modules = [
            'core.agent',
            'core.adapters.engine_adapter',
            'core.reasoning.intention_classifier',
            'core.memory.memory_manager',
            'core.diagnostics.diagnostic_reporter',
        ]
        
        import_issues = []
        for module_name in core_modules:
            try:
                __import__(module_name)
            except Exception as e:
                import_issues.append({'module': module_name, 'error': str(e)})
        
        if not import_issues:
            return CheckResult(
                name="core_modules",
                passed=True,
                message=f"Core modules importables ({len(core_modules)} verificados)",
                details={'modules_checked': core_modules},
                severity="MINOR"
            )
        else:
            return CheckResult(
                name="core_modules",
                passed=False,
                message=f"Problemas importando {len(import_issues)} módulos",
                details={'issues': import_issues},
                severity="CRITICAL"
            )
    
    def run_all_checks(self) -> HealthReport:
        """
        Ejecuta todos los checks y genera reporte consolidado.
        
        Returns:
            HealthReport con todos los resultados
        """
        report = HealthReport()
        
        # Ejecutar todos los checks
        report.add_check(self.check_python_version())
        report.add_check(self.check_critical_paths())
        report.add_check(self.check_write_permissions())
        report.add_check(self.check_core_modules())
        report.add_check(self.check_blender_availability())
        
        return report


# CLI para testing
if __name__ == "__main__":
    import json
    
    checker = SystemHealthChecker()
    report = checker.run_all_checks()
    
    print(json.dumps(report.to_dict(), indent=2))
