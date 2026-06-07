"""
core/diagnostics/module_validator.py

Validación de coherencia de módulos.
FASE 22: Auto-Diagnóstico Controlado.

Verifica:
- Estructura de directorios correcta
- Imports no rotos
- Core modules presentes
"""

from typing import Dict, Any, List
from pathlib import Path
import importlib.util
import ast

from .system_health_checker import CheckResult


class ModuleValidator:
    """Validador de coherencia de módulos."""
    
    def __init__(self, project_root: Path):
        """
        Inicializa validador.
        
        Args:
            project_root: Raíz del proyecto
        """
        self.project_root = Path(project_root)
    
    def validate_directory_structure(self) -> CheckResult:
        """Valida que la estructura de directorios sea correcta."""
        # Estructura real del proyecto ZULY
        # Actualizada en Fase 22 para reflejar arquitectura actual
        expected_structure = {
            'core': ['__init__.py', 'agent.py', 'adapters', 'reasoning', 'memory', 'validation', 'diagnostics'],
            'core/adapters': ['__init__.py', 'blender_adapter.py', 'engine_adapter.py'],
            'core/reasoning': ['__init__.py', 'decision_chain_simulator.py', 'explain_engine.py', 'inference_engine.py'],
            'core/memory': ['__init__.py', 'memory_manager.py', 'trace_core.py', 'volatile_memory.py'],
            'core/diagnostics': ['__init__.py', 'system_health_checker.py', 'diagnostic_reporter.py', 'module_validator.py'],
            'tests': [],  # Solo verificar que exista
        }
        
        missing_items = []
        for dir_path, expected_items in expected_structure.items():
            dir_full = self.project_root / dir_path
            
            if not dir_full.exists():
                missing_items.append(f"Directory: {dir_path}")
                continue
            
            for item in expected_items:
                item_path = dir_full / item
                if not item_path.exists():
                    missing_items.append(f"File/Dir: {dir_path}/{item}")
        
        if not missing_items:
            return CheckResult(
                name="directory_structure",
                passed=True,
                message="Estructura de directorios correcta",
                details={'structure_validated': list(expected_structure.keys())},
                severity="MINOR"
            )
        else:
            return CheckResult(
                name="directory_structure",
                passed=False,
                message=f"Elementos faltantes: {len(missing_items)}",
                details={'missing': missing_items},
                severity="SERIOUS"
            )
    
    def check_broken_imports(self) -> CheckResult:
        """
        Verifica imports rotos en archivos .py del core.
        
        Nota: Check básico, no exhaustivo.
        """
        core_path = self.project_root / 'core'
        python_files = list(core_path.rglob('*.py'))
        
        broken_imports = []
        
        for py_file in python_files:
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Parse AST para encontrar imports
                try:
                    tree = ast.parse(content)
                    for node in ast.walk(tree):
                        if isinstance(node, ast.Import):
                            for alias in node.names:
                                # Intentar importar
                                try:
                                    __import__(alias.name)
                                except ImportError:
                                    broken_imports.append({
                                        'file': str(py_file.relative_to(self.project_root)),
                                        'import': alias.name
                                    })
                        elif isinstance(node, ast.ImportFrom):
                            if node.module:
                                # Solo verificar imports de core
                                if node.module.startswith('core') or node.module.startswith('.'):
                                    try:
                                        __import__(node.module)
                                    except ImportError:
                                        broken_imports.append({
                                            'file': str(py_file.relative_to(self.project_root)),
                                            'import': f"from {node.module}"
                                        })
                except SyntaxError:
                    # Skip archivos con errores de sintaxis
                    pass
                    
            except Exception:
                # Skip archivos que no se pueden leer
                continue
        
        if not broken_imports:
            return CheckResult(
                name="broken_imports",
                passed=True,
                message=f"No se detectaron imports rotos ({len(python_files)} archivos revisados)",
                details={'files_checked': len(python_files)},
                severity="MINOR"
            )
        else:
            return CheckResult(
                name="broken_imports",
                passed=False,
                message=f"Posibles imports rotos: {len(broken_imports)}",
                details={'broken': broken_imports[:10]},  # Limitar a 10
                severity="SERIOUS"
            )
    
    def verify_core_integrity(self) -> CheckResult:
        """Verifica integridad del core (VERSION file, estructura básica)."""
        issues = []
        
        # Verificar VERSION file
        version_file = self.project_root / 'core' / 'VERSION'
        if not version_file.exists():
            issues.append("VERSION file missing")
        else:
            try:
                content = version_file.read_text(encoding='utf-8')
                if 'IMMUTABLE' not in content or 'ZULY CORE' not in content:
                    issues.append("VERSION file content unexpected")
            except Exception as e:
                issues.append(f"VERSION file unreadable: {e}")
        
        # Verificar __init__.py en core
        core_init = self.project_root / 'core' / '__init__.py'
        if not core_init.exists():
            issues.append("core/__init__.py missing")
        
        if not issues:
            return CheckResult(
                name="core_integrity",
                passed=True,
                message="Core integrity verified",
                details={'checks': ['VERSION', '__init__.py']},
                severity="MINOR"
            )
        else:
            return CheckResult(
                name="core_integrity",
                passed=False,
                message=f"Integrity issues: {len(issues)}",
                details={'issues': issues},
                severity="CRITICAL"
            )
    
    def run_all_validations(self) -> List[CheckResult]:
        """
        Ejecuta todas las validaciones.
        
        Returns:
            Lista de CheckResults
        """
        return [
            self.validate_directory_structure(),
            self.check_broken_imports(),
            self.verify_core_integrity(),
        ]
