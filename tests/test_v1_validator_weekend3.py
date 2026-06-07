import unittest
from unittest.mock import MagicMock, patch
from core.validation.v1_validator import V1Validator
from core.validation.v0_validator import V0Validator
from core.adapters.mock_adapter import MockAdapter
from core.validation.state_snapshot import StateSnapshot
from core.agent import Agent

class TestV1Validator(unittest.TestCase):
    def setUp(self):
        self.validator = V1Validator()
        self.adapter = MockAdapter()
        # Inyectar adapter en StateSnapshot para los tests
        # (StateSnapshot usa el adapter global a través de SceneMonitor o similar, 
        # pero aquí lo mockearemos o usaremos el real si está bien desacoplado)
        
    @patch('core.validation.state_snapshot.StateSnapshot.capture')
    def test_v1_creation_success(self, mock_capture):
        # Escenario: Se crea un cubo 'Cube_001'
        pre_snap = {}
        post_snap = {
            'Cube_001': {
                'name': 'Cube_001',
                'type': 'MESH',
                'vertex_count': 8,
                'parent': None
            }
        }
        
        command_result = {
            'success': True,
            'effect': 'create',
            'command_executed': 'crear_cubo',
            'parameters': {'primitive_type': 'cube'},
            'result': {'object_name': 'Cube_001'}
        }
        
        result = self.validator.validate(command_result, pre_snap, post_snap)
        self.assertTrue(result['verified'])
        self.assertIn("Estructura", result['details'])
        self.assertIn("'Cube_001'", result['details'])

    def test_v1_creation_type_mismatch(self):
        pre_snap = {}
        post_snap = {
            'Light_001': {
                'name': 'Light_001',
                'type': 'LIGHT',
                'vertex_count': 0,
                'parent': None
            }
        }
        
        command_result = {
            'success': True,
            'effect': 'create',
            'command_executed': 'crear_cubo',
            'parameters': {'primitive_type': 'cube'},
            'result': {'object_name': 'Light_001'}
        }
        
        result = self.validator.validate(command_result, pre_snap, post_snap)
        self.assertFalse(result['verified'])
        self.assertIn("se obtuvo LIGHT", result['details'])

    def test_v1_hierarchy_success(self):
        pre_snap = {
            'ParentObj': {'name': 'ParentObj', 'type': 'MESH', 'parent': None},
            'ChildObj': {'name': 'ChildObj', 'type': 'MESH', 'parent': None}
        }
        post_snap = {
            'ParentObj': {'name': 'ParentObj', 'type': 'MESH', 'parent': None},
            'ChildObj': {'name': 'ChildObj', 'type': 'MESH', 'parent': 'ParentObj'}
        }
        
        command_result = {
            'success': True,
            'effect': 'hierarchy',
            'command_executed': 'parent_object',
            'parameters': {'child_name': 'ChildObj', 'parent_name': 'ParentObj'}
        }
        
        result = self.validator.validate(command_result, pre_snap, post_snap)
        self.assertTrue(result['verified'])
        self.assertIn("Parenting", result['details'])
        self.assertIn("correcto", result['details'])

    def test_v1_hierarchy_mismatch(self):
        pre_snap = {
            'ParentA': {'name': 'ParentA', 'type': 'MESH'},
            'Child': {'name': 'Child', 'type': 'MESH'}
        }
        post_snap = {
            'ParentA': {'name': 'ParentA', 'type': 'MESH'},
            'ParentB': {'name': 'ParentB', 'type': 'MESH'},
            'Child': {'name': 'Child', 'type': 'MESH', 'parent': 'ParentB'} # Error: should be ParentA
        }
        
        command_result = {
            'success': True,
            'effect': 'hierarchy',
            'command_executed': 'parent_object',
            'parameters': {'child_name': 'Child', 'parent_name': 'ParentA'}
        }
        
        result = self.validator.validate(command_result, pre_snap, post_snap)
        self.assertFalse(result['verified'])
        self.assertIn("se esperaba 'ParentA'", result['details'])

    def test_v1_geometric_integrity_broken(self):
        pre_snap = {
            'MyCube': {'name': 'MyCube', 'type': 'MESH', 'vertex_count': 8}
        }
        post_snap = {
            'MyCube': {'name': 'MyCube', 'type': 'MESH', 'vertex_count': 12} # Anomalía!
        }
        
        command_result = {
            'success': True,
            'effect': 'transform',
            'command_executed': 'mover_objeto',
            'result': {'name': 'MyCube'}
        }
        
        result = self.validator.validate(command_result, pre_snap, post_snap)
        self.assertFalse(result['verified'])
        self.assertIn("Integridad geométrica comprometida", result['details'])

class TestAgentV1Integration(unittest.TestCase):
    @patch('core.agent.V0Validator')
    @patch('core.agent.V1Validator')
    @patch('core.agent.NaturalLanguageProcessor')
    @patch('core.agent.get_failsafe_executor')
    @patch('core.agent.HumanGate')
    @patch('core.agent.ContextGuard')
    def test_agent_calls_v0_and_v1(self, mock_guard_class, mock_gate_class, mock_failsafe, mock_nlu, mock_v1_class, mock_v0_class):
        # Setup mocks
        mock_v0 = mock_v0_class.return_value
        mock_v1 = mock_v1_class.return_value
        
        # Mocks para seguridad (permitir ejecución)
        mock_gate = mock_gate_class.return_value
        mock_gate.authorize.return_value = {"action": "ALLOW", "risk": "LOW", "reason": "Test"}
        
        mock_guard = mock_guard_class.return_value
        mock_guard.evaluate.return_value = {"status": "PERMITIDO", "reason": "Test"}
        
        mock_v0.validate.return_value = {'verified': True, 'details': 'V0 OK'}
        mock_v1.validate.return_value = {'verified': True, 'details': 'V1 OK'}
        
        # Simular éxito de ejecución
        mock_executor = mock_failsafe.return_value
        mock_executor.execute_single.return_value = MagicMock(success=True, result={}, error=None)
        
        # Simular intención
        intent = MagicMock()
        intent.command_name = 'crear_cubo'
        intent.confidence = 0.95
        intent.parameters = {'location': [0, 0, 0], 'primitive_type': 'cube', 'name': 'Cube_001'}
        
        mock_nlu_inst = mock_nlu.return_value
        mock_nlu_inst.process.return_value = [intent]
        
        # Agent con adapters mockeados
        agent = Agent(force_mock=True, auto_monitor=False)
        
        # Mocking StateSnapshot para evitar bpy
        with patch('core.validation.state_snapshot.StateSnapshot.capture') as mock_snap:
            mock_snap.return_value = {}
            
            response = agent.process_natural_request("crear un cubo")
            
            # Verificar secuencia
            mock_v0.validate.assert_called()
            mock_v1.validate.assert_called()
            self.assertTrue(response['success'])

if __name__ == '__main__':
    unittest.main()
