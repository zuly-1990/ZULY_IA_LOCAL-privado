import sys
import os
import unittest
from unittest.mock import MagicMock, patch

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.agent import Agent
from core.validation.v0_validator import V0Validator
from core.validation.state_snapshot import StateSnapshot

class TestPhase512Validation(unittest.TestCase):
    
    def setUp(self):
        # Mock StateSnapshot to avoid Blender dependency
        self.original_capture = StateSnapshot.capture
    
    def tearDown(self):
        StateSnapshot.capture = self.original_capture

    def test_validation_success_cycle(self):
        """Test que verifica que el ciclo de validación V0 funciona en el Agente."""
        print("\n======================================================================")
        print("TEST FASE 5.12: Validación Estructural V0")
        print("======================================================================")
        
        # 1. Setup Mock Snapshots
        # PRE: Empty
        pre_snapshot = {}
        # POST: One cube
        post_snapshot = {
            'Cube': {'type': 'MESH', 'location': (0,0,0), 'collection': 'Collection'}
        }
        
        # Mocking StateSnapshot.capture to return pre then post
        StateSnapshot.capture = MagicMock(side_effect=[pre_snapshot, post_snapshot])
        
        # 2. Initialize Agent
        agent = Agent(auto_monitor=False)
        
        # 3. Mock NLU to return a create intent
        mock_intent = MagicMock()
        mock_intent.command_name = 'blender.create_cube'
        mock_intent.confidence = 0.99
        mock_intent.parameters = {'name': 'Cube'}
        
        agent.nlu.process = MagicMock(return_value=[mock_intent])
        
        # 4. Mock Command Execution to return Success
        # We need to mock _execute_intent because we don't have real commands loaded that work without Blender
        agent._execute_intent = MagicMock(return_value={
            'success': True,
            'command': 'blender.create_cube',
            'effect': 'create',  # NUEVO: campo effect requerido por V0
            'result': {'name': 'Cube'},
            'attempt': 1
        })
        
        # 5. Execute Request
        print("Ejecutando petición: 'Crea un cubo'")
        response = agent.process_natural_request("Crea un cubo")
        
        # 6. Verify Results
        print(f"Resultado Agente: {response['success']}")
        
        # Check if validation was performed
        self.assertIn('validation', response['results'][0], "El resultado debe contener datos de validación")
        validation = response['results'][0]['validation']
        
        print(f"Datos Validación: {validation}")
        
        self.assertTrue(validation['verified'], "La validación debería ser exitosa")
        self.assertIn("Objeto 'Cube' existe físicamente", validation['details'])
        
        print("[SUCCESS] Ciclo de validación V0 completado correctamente.")

if __name__ == '__main__':
    unittest.main()
