import unittest
from core.reasoning.intention_classifier import classify_intention
from core.reasoning.permission_gate import evaluate_permission

class TestPermissionGate(unittest.TestCase):
    def test_safe_action(self):
        intent = "borrar cubo"
        report = classify_intention(intent)
        perm = evaluate_permission(report)
        self.assertFalse(perm["requiere_permiso_humano"], "Safe action should not require permission")
        self.assertEqual(perm["estado"], "PREAPROBADA")
        self.assertFalse(perm["accion_ejecutada"])

    def test_dangerous_action(self):
        intent = "borrar colección principal"
        report = classify_intention(intent)
        perm = evaluate_permission(report)
        self.assertTrue(perm["requiere_permiso_humano"], "Dangerous action should require permission")
        self.assertEqual(perm["estado"], "BLOQUEADA")
        self.assertFalse(perm["accion_ejecutada"])

    def test_ambiguous_action(self):
        intent = "modificar objeto"
        report = classify_intention(intent)
        perm = evaluate_permission(report)
        self.assertTrue(perm["requiere_permiso_humano"], "Ambiguous action should require permission")
        self.assertEqual(perm["estado"], "BLOQUEADA")
        self.assertFalse(perm["accion_ejecutada"])

if __name__ == "__main__":
    unittest.main()
