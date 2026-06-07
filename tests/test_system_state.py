"""
tests/test_system_state.py

Tests para SystemStateSnapshot (Fase 18.1)
"""

import unittest
import sys
import os

# Agregar path del proyecto
project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_path not in sys.path:
    sys.path.insert(0, project_path)

from core.agent import Agent
from core.observability.system_state import SystemStateSnapshot
import json


class TestSystemStateSnapshot(unittest.TestCase):
    """Tests para el snapshot de estado del sistema."""
    
    def setUp(self):
        """Inicializar Agent para tests."""
        self.agent = Agent(force_mock=True)
    
    def test_capture_returns_self(self):
        """Test: capture() retorna self para encadenamiento."""
        snapshot = SystemStateSnapshot(self.agent)
        result = snapshot.capture()
        
        self.assertIs(result, snapshot, "capture() debe retornar self")
        self.assertIsNotNone(snapshot.state, "state debe estar poblado")
    
    def test_snapshot_has_required_sections(self):
        """Test: snapshot contiene todas las secciones requeridas."""
        snapshot = SystemStateSnapshot(self.agent).capture()
        
        required_sections = ["timestamp", "agent", "adapter", "black_protocol", "modules", "last_action"]
        
        for section in required_sections:
            self.assertIn(section, snapshot.state, f"Falta sección: {section}")
    
    def test_to_json_is_valid(self):
        """Test: to_json() genera JSON válido."""
        snapshot = SystemStateSnapshot(self.agent).capture()
        json_str = snapshot.to_json()
        
        # Debe ser parseable
        try:
            parsed = json.loads(json_str)
            self.assertIsInstance(parsed, dict)
        except json.JSONDecodeError as e:
            self.fail(f"JSON inválido: {e}")
    
    def test_to_human_readable_is_string(self):
        """Test: to_human_readable() retorna string legible."""
        snapshot = SystemStateSnapshot(self.agent).capture()
        human = snapshot.to_human_readable()
        
        self.assertIsInstance(human, str)
        self.assertGreater(len(human), 100, "Formato humano muy corto")
        
        # Debe contener elementos clave
        self.assertIn("ZULY", human)
        self.assertIn("AGENT", human)
        self.assertIn("ADAPTER", human)
    
    def test_save_to_file(self):
        """Test: save() guarda snapshot a archivo."""
        import tempfile
        
        snapshot = SystemStateSnapshot(self.agent).capture()
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            filepath = f.name
        
        try:
            snapshot.save(filepath, format="human")
            
            # Verificar que existe
            self.assertTrue(os.path.exists(filepath))
            
            # Verificar contenido
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                self.assertIn("ZULY", content)
        finally:
            if os.path.exists(filepath):
                os.remove(filepath)
    
    def test_fail_safe_with_broken_agent(self):
        """Test: snapshot no falla incluso con Agent roto."""
        # Crear snapshot con agent "roto" (sin atributos)
        class BrokenAgent:
            pass
        
        broken = BrokenAgent()
        snapshot = SystemStateSnapshot(broken).capture()
        
        # Debe capturar algo, no fallar
        self.assertIsNotNone(snapshot.state)
        self.assertIn("agent", snapshot.state)
        
        # Agent debe tener valores por defecto (fail-safe funciona)
        agent_state = snapshot.state["agent"]
        self.assertIn("operational_state", agent_state)
        self.assertEqual(agent_state["operational_state"], "unknown")
    
    def test_agent_get_system_state(self):
        """Test: Agent.get_system_state() funciona."""
        snapshot = self.agent.get_system_state()
        
        self.assertIsInstance(snapshot, SystemStateSnapshot)
        self.assertIsNotNone(snapshot.state)
    
    def test_chaining(self):
        """Test: encadenamiento funciona."""
        import tempfile
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            filepath = f.name
        
        try:
            # Encadenar: capture() -> save()
            self.agent.get_system_state().save(filepath)
            
            self.assertTrue(os.path.exists(filepath))
        finally:
            if os.path.exists(filepath):
                os.remove(filepath)


if __name__ == "__main__":
    unittest.main()
