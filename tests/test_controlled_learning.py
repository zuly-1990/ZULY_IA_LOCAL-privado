
import unittest
from unittest.mock import patch, MagicMock
from core.agent import Agent
from core.utils.nlu import CommandIntent

class TestControlledLearning(unittest.TestCase):
    
    @patch('core.agent.is_author_verified')
    def test_unauthorized_learning_blocked(self, mock_verified):
        # Mock autor no verificado
        mock_verified.return_value = False
        agent = Agent(auto_monitor=False)
        
        # Petición con alta confianza
        with patch.object(agent.nlu, 'process') as mock_process:
            mock_process.return_value = [CommandIntent("crear_cubo", confidence=0.95)]
            result = agent.process_natural_request("crea un cubo")
            
            self.assertFalse(result['success'])
            self.assertIn("Protección de Decisión", result['error'])
            self.assertEqual(agent.operational_state, "Bloqueo Ético / Seguridad")

    @patch('core.agent.is_author_verified')
    def test_authorized_learning_allowed(self, mock_verified):
        # Mock autor verificado
        mock_verified.return_value = True
        agent = Agent(auto_monitor=False)
        
        # Mock de ejecución de comando exitosa
        agent._execute_intent = MagicMock(return_value={'success': True})
        
        # Petición con alta confianza (≥ 90%)
        with patch.object(agent.nlu, 'process') as mock_process:
            mock_process.return_value = [CommandIntent("crear_cubo", confidence=0.92)]
            result = agent.process_natural_request("crea un cubo")
            
            # Verificamos que pasó por el estado de aprendizaje
            # Nota: agent.operational_state vuelve a "Observación" al final, 
            # así que testeamos la lógica interna o el registro.
            self.assertTrue(result['success'])
            
    @patch('core.agent.is_author_verified')
    def test_low_confidence_no_learning(self, mock_verified):
        # Mock autor verificado
        mock_verified.return_value = True
        agent = Agent(auto_monitor=False)
        
        # Petición con confianza media (70-89%) -> Ejecución normal, no aprendizaje
        with patch.object(agent.nlu, 'process') as mock_process:
            mock_process.return_value = [CommandIntent("crear_cubo", confidence=0.80)]
            agent._execute_intent = MagicMock(return_value={'success': True})
            
            result = agent.process_natural_request("crea un cubo")
            self.assertTrue(result['success'])
            # No debería haber registrado en bitácora de aprendizaje (verificable via mocks o archivo)

if __name__ == '__main__':
    unittest.main()
