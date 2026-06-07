import unittest
from core.reasoning.decision_chain_simulator import simulate_decision_chain

class TestDecisionChainSimulator(unittest.TestCase):
    def test_safe_action(self):
        result = simulate_decision_chain("borrar cubo", {})
        # Should not require permission and be acceptable
        self.assertFalse(result["requiere_permiso_humano"], "Safe action should not need permission")
        self.assertEqual(result["evaluacion_global"], "ACEPTABLE")
        # Chain should have at least one step
        self.assertGreaterEqual(len(result["cadena_simulada"]), 1)
        self.assertFalse(result["accion_ejecutada"])

    def test_dangerous_action(self):
        result = simulate_decision_chain("borrar colección principal", {})
        self.assertTrue(result["requiere_permiso_humano"], "Dangerous action should need permission")
        self.assertEqual(result["evaluacion_global"], "BLOQUEADA")
        # Chain should be empty because blocked
        self.assertEqual(len(result["cadena_simulada"]), 0)
        self.assertFalse(result["accion_ejecutada"])

    def test_ambiguous_action(self):
        result = simulate_decision_chain("modificar objeto", {})
        self.assertTrue(result["requiere_permiso_humano"], "Ambiguous action should need permission")
        # According to logic, ambiguous leads to RIESGOSA global evaluation
        self.assertEqual(result["evaluacion_global"], "RIESGOSA")
        self.assertEqual(len(result["cadena_simulada"]), 0)
        self.assertFalse(result["accion_ejecutada"])

if __name__ == "__main__":
    unittest.main()
