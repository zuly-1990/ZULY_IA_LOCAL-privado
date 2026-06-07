"""
core/diagnostics/diagnostic_reporter.py

Generación de reportes de diagnóstico.
FASE 22: Auto-Diagnóstico Controlado.

Genera reportes JSON estructurados con:
- Clasificación de severidad
- Timestamps
- Recomendaciones
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum
from datetime import datetime
import json
from pathlib import Path


class IssueSeverity(str, Enum):
    """Niveles de severidad de issues."""
    MINOR = "MINOR"          # Reportar, continuar
    SERIOUS = "SERIOUS"      # Reportar, escalar
    CRITICAL = "CRITICAL"    # Activar Protocolo Negro si configurado


@dataclass
class Issue:
    """Un issue detectado."""
    severity: IssueSeverity
    component: str
    message: str
    details: Optional[Dict[str, Any]] = None
    recommendation: Optional[str] = None


class DiagnosticReporter:
    """Generador de reportes de diagnóstico."""
    
    def __init__(self):
        """Inicializa reporter."""
        self.issues: List[Issue] = []
        self.timestamp = datetime.now().isoformat()
    
    def add_issue(
        self,
        severity: IssueSeverity,
        component: str,
        message: str,
        details: Optional[Dict[str, Any]] = None,
        recommendation: Optional[str] = None
    ):
        """
        Agrega un issue al reporte.
        
        Args:
            severity: Nivel de severidad
            component: Componente afectado
            message: Mensaje descriptivo
            details: Detalles adicionales
            recommendation: Recomendación de acción
        """
        self.issues.append(Issue(
            severity=severity,
            component=component,
            message=message,
            details=details,
            recommendation=recommendation
        ))
    
    def determine_overall_health(self) -> str:
        """
        Determina salud general del sistema.
        
        Returns:
            "OK", "WARNING", o "CRITICAL"
        """
        if not self.issues:
            return "OK"
        
        # Si hay algún CRITICAL
        if any(i.severity == IssueSeverity.CRITICAL for i in self.issues):
            return "CRITICAL"
        
        # Si hay algún SERIOUS
        if any(i.severity == IssueSeverity.SERIOUS for i in self.issues):
            return "WARNING"
        
        # Solo MINOR
        return "OK"
    
    def generate_recommendations(self) -> List[str]:
        """
        Genera lista de recomendaciones basadas en issues.
        
        Returns:
            Lista de recomendaciones
        """
        recommendations = []
        
        for issue in self.issues:
            if issue.recommendation:
                recommendations.append(issue.recommendation)
            else:
                # Generar recomendación genérica basada en severidad
                if issue.severity == IssueSeverity.CRITICAL:
                    recommendations.append(f"URGENTE: Resolver '{issue.component}' antes de continuar")
                elif issue.severity == IssueSeverity.SERIOUS:
                    recommendations.append(f"Revisar '{issue.component}' pronto")
        
        return list(set(recommendations))  # Remove duplicates
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convierte reporte a diccionario.
        
        Returns:
            Diccionario con reporte completo
        """
        return {
            'timestamp': self.timestamp,
            'system_health': self.determine_overall_health(),
            'total_issues': len(self.issues),
            'issues_by_severity': {
                'CRITICAL': sum(1 for i in self.issues if i.severity == IssueSeverity.CRITICAL),
                'SERIOUS': sum(1 for i in self.issues if i.severity == IssueSeverity.SERIOUS),
                'MINOR': sum(1 for i in self.issues if i.severity == IssueSeverity.MINOR),
            },
            'issues': [
                {
                    'severity': i.severity.value,
                    'component': i.component,
                    'message': i.message,
                    'details': i.details or {},
                    'recommendation': i.recommendation
                }
                for i in self.issues
            ],
            'recommendations': self.generate_recommendations()
        }
    
    def to_json(self, indent: int = 2) -> str:
        """
        Convierte reporte a JSON string.
        
        Args:
            indent: Indentación para JSON
            
        Returns:
            JSON string
        """
        return json.dumps(self.to_dict(), indent=indent)
    
    def save_to_file(self, filepath: Path):
        """
        Guarda reporte a archivo JSON.
        
        Args:
            filepath: Ruta donde guardar
        """
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(self.to_json())
    
    @classmethod
    def from_health_report(cls, health_report) -> 'DiagnosticReporter':
        """
        Crea DiagnosticReporter desde HealthReport.
        
        Args:
            health_report: Instancia de HealthReport
            
        Returns:
            DiagnosticReporter con issues extraídos
        """
        reporter = cls()
        reporter.timestamp = health_report.timestamp
        
        for check in health_report.checks:
            if not check.passed:
                severity = IssueSeverity[check.severity]
                reporter.add_issue(
                    severity=severity,
                    component=check.name,
                    message=check.message,
                    details=check.details
                )
        
        return reporter
