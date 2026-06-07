"""
tests/test_system_report.py

Tests para system_report (Fase 18.3)
"""

import unittest
import sys
import os

# Agregar path del proyecto
project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_path not in sys.path:
    sys.path.insert(0, project_path)

from core.agent import Agent


class TestSystemReport(unittest.TestCase):
    """Tests para el reporte del sistema."""
    
    def setUp(self):
        """Inicializar Agent para tests."""
        self.agent = Agent(force_mock=True)
    
    def test_system_report_no_crash(self):
        """Test: system_report() no crashea."""
        try:
            report = self.agent.system_report()
            self.assertIsNotNone(report)
        except Exception as e:
            self.fail(f"system_report() crashed: {e}")
    
    def test_includes_estado_del_sistema(self):
        """Test: incluye 'ESTADO DEL SISTEMA'."""
        report = self.agent.system_report()
        self.assertIn("ESTADO DEL SISTEMA", report)
    
    def test_includes_trace_section_if_events(self):
        """Test: incluye sección 'TRAZA' si hay eventos."""
        # Agregar un evento
        self.agent.trace_core.append_trace({
            "intention": "test_action",
            "execution_success": True
        })
        
        report = self.agent.system_report()
        self.assertIn("TRAZA", report)
        self.assertIn("Eventos registrados", report)


if __name__ == "__main__":
    unittest.main()
