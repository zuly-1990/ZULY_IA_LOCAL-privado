"""
test_v2_validator_weekend4.py
==============================

Suite de tests para el Validador V2 (Contextual).
FIN DE SEMANA 4 — Plan Maestro ZULY 2026.

Objetivo: Verificar que V2 bloquea correctamente ejecuciones fuera de
contexto y permite las que sí son válidas.

Estructura (siguiendo el mismo patrón de test_v1_validator_weekend3.py):
  - TestV2ChecksIndividuales   : Tests de cada check por separado
  - TestV2ValidateCompleto     : Tests del método validate() completo
  - TestAgentV2Integracion     : Test de integración con Agent

Convención de logs de salida (Manual Sección 15):
  ZULY_LAB/logs_sesiones/LOG_FDE_4_YYYYMMDD.json

Ejecutar con:
    .venv\\Scripts\\python.exe -m pytest tests/test_v2_validator_weekend4.py -v
"""

import unittest
from unittest.mock import MagicMock, patch
from core.validation.v2_validator import V2Validator


class TestV2ChecksIndividuales(unittest.TestCase):
    """Tests de cada check individual del V2Validator."""

    def setUp(self):
        self.validator = V2Validator()

    # ─── CHECK 1: blender_available ───────────────────────

    def test_v2_bloquea_sin_adapter(self):
        """Sin adapter, V2 debe bloquear completamente."""
        result = self.validator.check_blender_available(adapter=None)
        self.assertFalse(result["passed"])
        self.assertIn("No hay adapter activo", result["detail"])

    def test_v2_bloquea_adapter_no_disponible(self):
        """Adapter que reporta is_available=False debe ser bloqueado."""
        mock_adapter = MagicMock()
        mock_adapter.is_available.return_value = False
        result = self.validator.check_blender_available(adapter=mock_adapter)
        self.assertFalse(result["passed"])
        self.assertIn("NO está disponible", result["detail"])

    def test_v2_pasa_adapter_disponible(self):
        """Adapter disponible debe pasar el check."""
        mock_adapter = MagicMock()
        mock_adapter.is_available.return_value = True
        result = self.validator.check_blender_available(adapter=mock_adapter)
        self.assertTrue(result["passed"])

    # ─── CHECK 2: execution_mode ──────────────────────────

    def test_v2_bloquea_edit_mode(self):
        """EDIT mode debe ser bloqueado."""
        ctx = {"mode": "EDIT"}
        result = self.validator.check_execution_mode(ctx)
        self.assertFalse(result["passed"])
        self.assertIn("EDIT", result["detail"])
        self.assertIn("OBJECT", result["detail"])

    def test_v2_bloquea_sculpt_mode(self):
        """SCULPT mode debe ser bloqueado."""
        ctx = {"mode": "SCULPT"}
        result = self.validator.check_execution_mode(ctx)
        self.assertFalse(result["passed"])

    def test_v2_pasa_object_mode(self):
        """OBJECT mode es el modo válido para ejecutar comandos."""
        ctx = {"mode": "OBJECT"}
        result = self.validator.check_execution_mode(ctx)
        self.assertTrue(result["passed"])

    def test_v2_pasa_contexto_vacio(self):
        """Sin contexto (MockAdapter) el check de modo es pasivo."""
        result = self.validator.check_execution_mode({})
        self.assertTrue(result["passed"])
        self.assertIn("pasivo", result["detail"])

    # ─── CHECK 3: active_collection ───────────────────────

    def test_v2_bloquea_sin_colecciones(self):
        """Sin colecciones y fuente válida de Blender debe bloquear."""
        ctx = {"collections": [], "collection_count": 0, "source": "blender"}
        result = self.validator.check_active_collection(ctx)
        self.assertFalse(result["passed"])
        self.assertIn("colecciones", result["detail"])

    def test_v2_pasa_con_coleccion(self):
        """Con al menos una colección debe pasar."""
        ctx = {"collections": ["Collection"], "collection_count": 1, "source": "blender"}
        result = self.validator.check_active_collection(ctx)
        self.assertTrue(result["passed"])

    def test_v2_pasa_fuente_mock(self):
        """Fuente 'mock' (sin Blender real) hace el check pasivo."""
        ctx = {"collections": [], "collection_count": 0, "source": "mock"}
        result = self.validator.check_active_collection(ctx)
        self.assertTrue(result["passed"])
        self.assertIn("pasivo", result["detail"])

    # ─── CHECK 4: base_file_path ──────────────────────────

    def test_v2_advierte_ruta_incorrecta(self):
        """Archivo fuera de rutas oficiales genera advertencia (no bloqueo)."""
        ctx = {"filepath": "C:/Users/Admin/Desktop/mi_archivo.blend"}
        result = self.validator.check_base_file_path(ctx)
        self.assertFalse(result["passed"])
        self.assertIn("ADVERTENCIA", result["detail"])
        self.assertIn("ZULY_PROJECTS", result["detail"])

    def test_v2_pasa_ruta_zuly_projects(self):
        """Archivo en ZULY_PROJECTS es válido."""
        ctx = {"filepath": "C:/Users/Admin/Desktop/ZULY_IA_LOCAL/ZULY_PROJECTS/test.blend"}
        result = self.validator.check_base_file_path(ctx)
        self.assertTrue(result["passed"])

    def test_v2_pasa_ruta_resultados_zuly(self):
        """Archivo en ZULY_LAB/resultados_zuly es válido."""
        ctx = {"filepath": "ZULY_LAB/resultados_zuly/A1.1_cubo_basico.blend"}
        result = self.validator.check_base_file_path(ctx)
        self.assertTrue(result["passed"])

    def test_v2_pasa_archivo_nuevo(self):
        """Archivo nuevo (ruta vacía) siempre es válido."""
        ctx = {"filepath": ""}
        result = self.validator.check_base_file_path(ctx)
        self.assertTrue(result["passed"])
        self.assertIn("nuevo", result["detail"])


class TestV2ValidateCompleto(unittest.TestCase):
    """Tests del método validate() completo — cadena de checks."""

    def setUp(self):
        self.validator = V2Validator()
        self.mock_adapter = MagicMock()
        self.mock_adapter.is_available.return_value = True

    def test_v2_bloquea_sin_adapter(self):
        """validate() sin adapter retorna bloqueo."""
        result = self.validator.validate(adapter=None, blender_context={})
        self.assertFalse(result["verified"])
        self.assertTrue(result["blocked"])
        self.assertEqual(result["failed_check"], "blender_available")

    def test_v2_bloquea_edit_mode_completo(self):
        """validate() en EDIT mode retorna bloqueo con cadena de checks."""
        ctx = {"mode": "EDIT", "source": "blender"}
        result = self.validator.validate(adapter=self.mock_adapter, blender_context=ctx)
        self.assertFalse(result["verified"])
        self.assertTrue(result["blocked"])
        self.assertEqual(result["failed_check"], "execution_mode")
        # Check 1 pasó, Check 2 bloqueó
        self.assertEqual(len(result["checks"]), 2)
        self.assertTrue(result["checks"][0]["passed"])   # blender_available OK
        self.assertFalse(result["checks"][1]["passed"])  # execution_mode FAIL

    def test_v2_pasa_contexto_valido_completo(self):
        """validate() con contexto completamente válido retorna verificado."""
        ctx = {
            "mode": "OBJECT",
            "source": "blender",
            "collections": ["Scene Collection"],
            "collection_count": 1,
            "filepath": "ZULY_PROJECTS/FDE_4_test_20260307.blend"
        }
        result = self.validator.validate(
            adapter=self.mock_adapter,
            blender_context=ctx
        )
        self.assertTrue(result["verified"])
        self.assertFalse(result["blocked"])
        self.assertIn("verificado", result["reason"])

    def test_v2_pasa_mock_adapter(self):
        """validate() con MockAdapter (sin contexto real) es permisivo."""
        ctx = {}  # Sin contexto — todos los checks son pasivos
        result = self.validator.validate(
            adapter=self.mock_adapter,
            blender_context=ctx
        )
        self.assertTrue(result["verified"])
        self.assertFalse(result["blocked"])

    def test_v2_registra_checks_ejecutados(self):
        """validate() registra todos los checks en el resultado."""
        ctx = {"mode": "OBJECT", "source": "blender",
               "collections": ["Col"], "collection_count": 1}
        self.validator.validate(adapter=self.mock_adapter, blender_context=ctx)
        checks = self.validator.get_last_checks()
        # Por lo menos 3 checks deben ejecutarse
        self.assertGreaterEqual(len(checks), 3)
        check_names = [c["check"] for c in checks]
        self.assertIn("blender_available", check_names)
        self.assertIn("execution_mode", check_names)
        self.assertIn("active_collection", check_names)


class TestAgentV2Integracion(unittest.TestCase):
    """
    Test de integración: V2 se llama ANTES de la ejecución en Agent.

    Verifica que la cadena completa V2 → Ejecución → V0 → V1 funciona.
    """

    @patch('core.agent.V2Validator')
    @patch('core.agent.V0Validator')
    @patch('core.agent.V1Validator')
    @patch('core.agent.NaturalLanguageProcessor')
    @patch('core.agent.get_failsafe_executor')
    @patch('core.agent.HumanGate')
    @patch('core.agent.ContextGuard')
    def test_agent_llama_v2_antes_de_ejecucion(
            self, mock_guard_cls, mock_gate_cls, mock_failsafe,
            mock_nlu, mock_v1_cls, mock_v0_cls, mock_v2_cls):
        """
        Verifica que process_natural_request() llama a V2.validate()
        antes de ejecutar el comando.
        """
        from core.agent import Agent

        # Configurar mocks de seguridad
        mock_gate = mock_gate_cls.return_value
        mock_gate.authorize.return_value = {"action": "ALLOW", "risk": "LOW", "reason": "Test"}

        mock_guard = mock_guard_cls.return_value
        mock_guard.evaluate.return_value = {"status": "PERMITIDO", "reason": "Test"}

        # V2: pasa sin bloqueo
        mock_v2 = mock_v2_cls.return_value
        mock_v2.validate.return_value = {
            "verified": True, "blocked": False,
            "checks": [], "reason": "OK"
        }

        # V0 y V1: pasan
        mock_v0 = mock_v0_cls.return_value
        mock_v0.validate.return_value = {"verified": True, "details": "V0 OK"}
        mock_v0.pre_snapshot = {}

        mock_v1 = mock_v1_cls.return_value
        mock_v1.validate.return_value = {"verified": True, "details": "V1 OK"}

        # Simular intent
        intent = MagicMock()
        intent.command_name = "crear_cubo"
        intent.confidence = 0.95
        intent.parameters = {"location": [0, 0, 0], "primitive_type": "cube"}

        mock_nlu.return_value.process.return_value = [intent]

        # Simular executor
        mock_executor = mock_failsafe.return_value
        mock_executor.execute_single.return_value = MagicMock(
            success=True, result={}, error=None
        )

        agent = Agent(force_mock=True, auto_monitor=False)

        with patch('core.validation.state_snapshot.StateSnapshot.capture') as mock_snap:
            mock_snap.return_value = {}
            response = agent.process_natural_request("Crea un cubo")

        # V2 fue llamado antes de la ejecución
        mock_v2.validate.assert_called()

    @patch('core.agent.V2Validator')
    @patch('core.agent.NaturalLanguageProcessor')
    @patch('core.agent.get_failsafe_executor')
    @patch('core.agent.HumanGate')
    @patch('core.agent.ContextGuard')
    def test_agent_bloquea_si_v2_falla(
            self, mock_guard_cls, mock_gate_cls, mock_failsafe,
            mock_nlu, mock_v2_cls):
        """
        Verifica que si V2 falla (contexto inválido), el Agent NO ejecuta
        el comando y retorna el error de V2.
        """
        from core.agent import Agent

        mock_gate = mock_gate_cls.return_value
        mock_gate.authorize.return_value = {"action": "ALLOW", "risk": "LOW", "reason": "Test"}

        mock_guard = mock_guard_cls.return_value
        mock_guard.evaluate.return_value = {"status": "PERMITIDO", "reason": "Test"}

        # V2: FALLA (contexto fuera de Blender)
        mock_v2 = mock_v2_cls.return_value
        mock_v2.validate.return_value = {
            "verified": False,
            "blocked": True,
            "failed_check": "blender_available",
            "checks": [],
            "reason": "V2 BLOQUEO: No hay adapter activo."
        }

        intent = MagicMock()
        intent.command_name = "crear_cubo"
        intent.confidence = 0.95
        intent.parameters = {}
        mock_nlu.return_value.process.return_value = [intent]

        mock_executor = mock_failsafe.return_value

        agent = Agent(force_mock=True, auto_monitor=False)
        response = agent.process_natural_request("Crea un cubo")

        # La respuesta debe ser fallo con error de V2
        self.assertFalse(response["success"])
        self.assertIn("V2", response.get("error", ""))

        # El executor NO fue llamado (V2 bloqueó antes)
        mock_executor.execute_single.assert_not_called()


if __name__ == "__main__":
    unittest.main()
