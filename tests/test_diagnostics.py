"""
tests/test_diagnostics.py

Tests para el módulo de diagnósticos de ZULY.
FASE 22: Auto-Diagnóstico Controlado.
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

# Agregar project root al path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from core.diagnostics import (
    SystemHealthChecker,
    CheckResult,
    HealthReport,
    ModuleValidator,
    DiagnosticReporter,
    IssueSeverity
)


class TestCheckResult:
    """Tests para CheckResult dataclass."""
    
    def test_check_result_creation_passed(self):
        """Test crear CheckResult exitoso."""
        result = CheckResult(
            name="test_check",
            passed=True,
            message="Todo bien",
            severity="MINOR"
        )
        assert result.name == "test_check"
        assert result.passed is True
        assert result.message == "Todo bien"
        assert result.severity == "MINOR"
    
    def test_check_result_creation_failed(self):
        """Test crear CheckResult fallido."""
        result = CheckResult(
            name="critical_check",
            passed=False,
            message="Error crítico",
            details={"issue": "missing_file"},
            severity="CRITICAL"
        )
        assert result.passed is False
        assert result.severity == "CRITICAL"
        assert result.details == {"issue": "missing_file"}


class TestHealthReport:
    """Tests para HealthReport."""
    
    def test_health_report_empty(self):
        """Test reporte vacío tiene estado OK."""
        report = HealthReport()
        assert report.overall_status == "OK"
        assert len(report.checks) == 0
    
    def test_health_report_add_passing_check(self):
        """Test agregar check exitoso mantiene OK."""
        report = HealthReport()
        check = CheckResult(
            name="test",
            passed=True,
            message="OK",
            severity="MINOR"
        )
        report.add_check(check)
        assert report.overall_status == "OK"
        assert len(report.checks) == 1
    
    def test_health_report_escalates_to_warning(self):
        """Test que SERIOUS escala a WARNING."""
        report = HealthReport()
        check = CheckResult(
            name="test",
            passed=False,
            message="Issue",
            severity="SERIOUS"
        )
        report.add_check(check)
        assert report.overall_status == "WARNING"
    
    def test_health_report_escalates_to_critical(self):
        """Test que CRITICAL escala a CRITICAL."""
        report = HealthReport()
        check = CheckResult(
            name="test",
            passed=False,
            message="Critical",
            severity="CRITICAL"
        )
        report.add_check(check)
        assert report.overall_status == "CRITICAL"
    
    def test_health_report_to_dict(self):
        """Test conversión a diccionario."""
        report = HealthReport()
        check = CheckResult(
            name="test_check",
            passed=True,
            message="OK",
            severity="MINOR"
        )
        report.add_check(check)
        
        data = report.to_dict()
        
        assert 'timestamp' in data
        assert data['system_health'] == "OK"
        assert 'checks' in data
        assert len(data['checks']) == 1


class TestSystemHealthChecker:
    """Tests para SystemHealthChecker."""
    
    def test_checker_initialization(self):
        """Test inicialización del checker."""
        checker = SystemHealthChecker(project_root)
        assert checker.project_root == project_root
    
    def test_check_python_version(self):
        """Test verificación de versión de Python."""
        checker = SystemHealthChecker(project_root)
        result = checker.check_python_version()
        
        assert result.name == "python_version"
        # Python 3.8+ debería pasar
        assert result.passed is True
    
    def test_check_critical_paths(self):
        """Test verificación de rutas críticas."""
        checker = SystemHealthChecker(project_root)
        result = checker.check_critical_paths()
        
        assert result.name == "critical_paths"
        # core/ debe existir
        assert result.passed is True
    
    def test_run_all_checks(self):
        """Test ejecución de todos los checks."""
        checker = SystemHealthChecker(project_root)
        report = checker.run_all_checks()
        
        assert isinstance(report, HealthReport)
        assert len(report.checks) > 0


class TestModuleValidator:
    """Tests para ModuleValidator."""
    
    def test_validator_initialization(self):
        """Test inicialización del validador."""
        validator = ModuleValidator(project_root)
        assert validator.project_root == project_root
    
    def test_validate_directory_structure(self):
        """Test validación de estructura de directorios."""
        validator = ModuleValidator(project_root)
        result = validator.validate_directory_structure()
        
        assert result.name == "directory_structure"
        assert isinstance(result.passed, bool)
    
    def test_verify_core_integrity(self):
        """Test verificación de integridad del core."""
        validator = ModuleValidator(project_root)
        result = validator.verify_core_integrity()
        
        assert result.name == "core_integrity"
        # Ahora que existe __init__.py, debería pasar
        assert result.passed is True
    
    def test_run_all_validations(self):
        """Test ejecución de todas las validaciones."""
        validator = ModuleValidator(project_root)
        results = validator.run_all_validations()
        
        assert isinstance(results, list)
        assert len(results) == 3
        assert all(isinstance(r, CheckResult) for r in results)


class TestDiagnosticReporter:
    """Tests para DiagnosticReporter."""
    
    def test_reporter_initialization(self):
        """Test inicialización del reporter."""
        reporter = DiagnosticReporter()
        assert len(reporter.issues) == 0
        assert reporter.timestamp is not None
    
    def test_add_issue(self):
        """Test agregar issue."""
        reporter = DiagnosticReporter()
        reporter.add_issue(
            severity=IssueSeverity.MINOR,
            component="test_component",
            message="Test issue"
        )
        
        assert len(reporter.issues) == 1
        assert reporter.issues[0].severity == IssueSeverity.MINOR
    
    def test_determine_overall_health_ok(self):
        """Test salud OK sin issues."""
        reporter = DiagnosticReporter()
        assert reporter.determine_overall_health() == "OK"
    
    def test_determine_overall_health_warning(self):
        """Test salud WARNING con issue SERIOUS."""
        reporter = DiagnosticReporter()
        reporter.add_issue(
            severity=IssueSeverity.SERIOUS,
            component="test",
            message="Serious issue"
        )
        assert reporter.determine_overall_health() == "WARNING"
    
    def test_determine_overall_health_critical(self):
        """Test salud CRITICAL con issue CRITICAL."""
        reporter = DiagnosticReporter()
        reporter.add_issue(
            severity=IssueSeverity.CRITICAL,
            component="test",
            message="Critical issue"
        )
        assert reporter.determine_overall_health() == "CRITICAL"
    
    def test_generate_recommendations(self):
        """Test generación de recomendaciones."""
        reporter = DiagnosticReporter()
        reporter.add_issue(
            severity=IssueSeverity.CRITICAL,
            component="test_component",
            message="Critical issue"
        )
        
        recommendations = reporter.generate_recommendations()
        
        assert len(recommendations) > 0
        assert any("test_component" in r for r in recommendations)
    
    def test_to_dict(self):
        """Test conversión a diccionario."""
        reporter = DiagnosticReporter()
        reporter.add_issue(
            severity=IssueSeverity.MINOR,
            component="test",
            message="Test"
        )
        
        data = reporter.to_dict()
        
        assert 'timestamp' in data
        assert 'system_health' in data
        assert 'total_issues' in data
        assert data['total_issues'] == 1
        assert 'issues' in data
        assert 'recommendations' in data
    
    def test_to_json(self):
        """Test conversión a JSON."""
        reporter = DiagnosticReporter()
        json_str = reporter.to_json()
        
        assert isinstance(json_str, str)
        assert 'timestamp' in json_str
    
    def test_from_health_report(self):
        """Test crear reporter desde HealthReport."""
        health_report = HealthReport()
        health_report.add_check(CheckResult(
            name="test_check",
            passed=False,
            message="Failed",
            severity="SERIOUS"
        ))
        
        reporter = DiagnosticReporter.from_health_report(health_report)
        
        assert len(reporter.issues) == 1
        assert reporter.issues[0].severity == IssueSeverity.SERIOUS


class TestIntegration:
    """Tests de integración del sistema de diagnóstico."""
    
    def test_full_diagnostic_flow(self):
        """Test flujo completo de diagnóstico."""
        # 1. Health checks
        checker = SystemHealthChecker(project_root)
        health_report = checker.run_all_checks()
        
        # 2. Module validation
        validator = ModuleValidator(project_root)
        for check in validator.run_all_validations():
            health_report.add_check(check)
        
        # 3. Generate report
        reporter = DiagnosticReporter.from_health_report(health_report)
        
        # Verificar que el flujo funciona
        data = reporter.to_dict()
        assert 'system_health' in data
        assert 'issues' in data
        assert 'recommendations' in data
    
    def test_diagnostic_output_format(self):
        """Test que el formato de salida es correcto."""
        checker = SystemHealthChecker(project_root)
        health_report = checker.run_all_checks()
        reporter = DiagnosticReporter.from_health_report(health_report)
        
        data = reporter.to_dict()
        
        # Verificar estructura
        required_keys = ['timestamp', 'system_health', 'total_issues', 
                        'issues_by_severity', 'issues', 'recommendations']
        for key in required_keys:
            assert key in data, f"Missing key: {key}"
        
        # Verificar issues_by_severity
        assert 'CRITICAL' in data['issues_by_severity']
        assert 'SERIOUS' in data['issues_by_severity']
        assert 'MINOR' in data['issues_by_severity']


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
