import sys
import os
import unittest
from unittest.mock import MagicMock, patch

# Añadir el path raíz para importar core
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

# Mocking modules before importing core.agent to avoid side effects
sys.modules['bpy'] = MagicMock()

from core.agent import Agent
from core.utils.nlu import CommandIntent

class TestControlIntegration(unittest.TestCase):
    def setUp(self):
        # Parchear todas las dependencias externas para una inicialización limpia
        patches = [
            patch('core.agent.is_author_verified', return_value=True),
            patch('core.agent.BlackProtocol.is_active', return_value=False),
            patch('core.agent.BlackProtocol.detect_ai_influence', return_value=None),
            patch('core.agent.BlackProtocol.activate_lock', MagicMock()),
            patch('core.agent.CommandLoader'),
            patch('core.agent.NaturalLanguageProcessor'),
            patch('core.agent.SceneMonitor'),
            patch('core.agent.V0Validator'),
            patch('core.agent.PatternMemory'),
            patch('core.agent.StateAwareness'),
            patch('core.agent.BlenderObserver'),
            patch('core.agent.BlenderSemanticObserver'),
            patch('core.agent.IntentionSimulator'),
            patch('core.agent.get_blender_context', return_value={}),
            patch('core.agent.log_info'),
            patch('core.agent.log_warning'),
            patch('core.agent.log_error'),
            patch('core.agent.log_success')
        ]
        for p in patches:
            p.start()
            self.addCleanup(p.stop)
            
        self.agent = Agent()
        # Mock manual de analyze_scene para controlar el contexto
        self.agent.analyze_scene = MagicMock()

    def test_context_guard_blocks_render_when_dirty(self):
        """Prueba que ContextGuard bloquea el render si hay cambios sin guardar."""
        self.agent.analyze_scene.return_value = {"context": {"is_dirty": True, "mode": "OBJECT"}}
        self.agent.nlu.process.return_value = [CommandIntent("RENDER", 0.95, {})]
        
        result = self.agent.process_natural_request("render")
        
        self.assertFalse(result["success"])
        self.assertEqual(result["error"], "Contexto Inválido")
        self.assertEqual(result["explanation"]["technical_log"]["guard_status"], "BLOQUEADO")

    def test_human_gate_medium_risk_delete_flow(self):
        """HumanGate clasifica borrado como riesgo MEDIO (ASK); el agente auto-autoriza y ejecuta (saneamiento)."""
        self.agent.analyze_scene.return_value = {
            "context": {"selected_objects_count": 1, "mode": "OBJECT", "is_dirty": False}
        }
        self.agent.nlu.process.return_value = [
            CommandIntent("blender.delete_object", 0.95, {"object_name": "Cube"})
        ]
        self.agent._execute_intent = MagicMock(
            return_value={"success": True, "effect": "delete", "result": {"name": "Cube"}}
        )

        result = self.agent.process_natural_request("borra")

        self.assertTrue(result["success"])
        self.agent._execute_intent.assert_called()

    def test_explainability_on_success(self):
        """Prueba que DecisionExplainer genera una explicación en caso de éxito."""
        self.agent.analyze_scene.return_value = {"context": {"mode": "OBJECT", "is_dirty": False}}
        self.agent.nlu.process.return_value = [CommandIntent("LIST_OBJECTS", 0.95, {})]
        self.agent._execute_intent = MagicMock(return_value={"success": True, "result": "OK"})
        self.agent.validator_v0.validate = MagicMock(return_value={"verified": True, "details": "OK"})
        
        result = self.agent.process_natural_request("lista")
        
        self.assertTrue(result["success"])
        self.assertIn("explanation", result)
        self.assertIn("fue realizada con éxito", result["explanation"]["human_summary"])

if __name__ == '__main__':
    unittest.main()
