"""
Tests de Comportamiento: Modelo de Acción Fundacional (MAC-0)
Basado en ORDEN_ARCA_04
"""

import unittest
import sys
import os

# Asegurar que podemos importar desde la raíz del proyecto
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from extensions.shields.action_model_v1 import ActionModelV1

class TestActionModelV1(unittest.TestCase):

    def test_1_no_actuar_por_defecto(self):
        """Ante ambigüedad o cualquier contexto, NO ACTÚA."""
        print("\n[TEST MAC-0] Verificando inacción por defecto")
        self.assertFalse(ActionModelV1.should_act({"any": "context"}))
        self.assertFalse(ActionModelV1.should_act(None))

    def test_2_detenerse_ante_conflicto(self):
        """Ante conflicto técnico o ético, SE DETIENE."""
        print("[TEST MAC-0] Verificando detención ante conflicto")
        self.assertEqual(ActionModelV1.on_conflict(), "halt")

    def test_3_solo_registrar_ante_desconocido(self):
        """Ante input desconocido, SOLO REGISTRA (no reacciona)."""
        print("[TEST MAC-0] Verificando registro de input desconocido")
        self.assertEqual(ActionModelV1.on_unknown_input("unknown garbage"), "store_only")

    def test_4_bloquear_ante_violacion_noe(self):
        """Ante violación detectada de la Tabla de NOÉ, BLOQUEA."""
        print("[TEST MAC-0] Verificando bloqueo ante violación de NOÉ")
        self.assertEqual(ActionModelV1.on_principle_violation(), "deny")

    def test_5_principio_de_detencion(self):
        """El comportamiento de detenerse es fundamental."""
        print("[TEST MAC-0] Verificando que 'detenerse' es la respuesta correcta")
        # Este test valida la filosofía: Detenerse > Avanzar a ciegas
        response = ActionModelV1.on_conflict()
        self.assertIn(response, ["halt", "deny"])

if __name__ == '__main__':
    unittest.main()
