import unittest
import os
import json
import shutil
from unittest.mock import MagicMock, patch
from core.learning.pattern_memory import PatternMemory
from core.agent import Agent

class TestMemoryHierarchy(unittest.TestCase):
    def setUp(self):
        # Setup carpetas temporales para tests
        self.test_dir = "test_memory_weekend5"
        os.makedirs(self.test_dir, exist_ok=True)
        
        # Patch de los repositorios para usar carpeta de test
        with patch('core.learning.repositories.pattern_repository.PatternRepository._ensure_file_exists'):
            self.memory = PatternMemory()
            self.memory.staging_repo.file_path = os.path.join(self.test_dir, "staging.json")
            self.memory.verified_repo.file_path = os.path.join(self.test_dir, "verified.json")
            self.memory.quarantine_repo.file_path = os.path.join(self.test_dir, "quarantine.json")
            
            # Limpiar archivos si existen
            for p in [self.memory.staging_repo.file_path, 
                     self.memory.verified_repo.file_path, 
                     self.memory.quarantine_repo.file_path]:
                with open(p, 'w', encoding='utf-8') as f:
                    json.dump([], f)
            
            self.memory.patterns = []

    def tearDown(self):
        # Limpiar carpeta de test
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_patron_nace_en_staging(self):
        """Un patrón nuevo siempre debe guardarse en STAGING."""
        req = "Crea un cubo rojo"
        res = {
            "success": True,
            "command_executed": "blender.create_cube",
            "confidence": 0.95,
            "mode": "REACTIVE",
            "validation": {"verified": True},
            "results": [{"effect": "cube_created"}]
        }
        
        pattern_id = self.memory.store_pattern(req, res)
        self.assertIsNotNone(pattern_id)
        
        # Verificar en lista interna
        pattern = self.memory.patterns[0]
        self.assertEqual(pattern['metadata']['status'], "STAGING")
        
        # Verificar en repo físico
        staging_data = self.memory.staging_repo.load_all()
        self.assertEqual(len(staging_data), 1)
        self.assertEqual(staging_data[0]['pattern_id'], pattern_id)

    def test_promocion_a_verified_tras_3_exitos(self):
        """3 éxitos consecutivos deben mover el patrón a VERIFIED."""
        req = "Crea un cubo rojo"
        res = {
            "success": True,
            "command_executed": "blender.create_cube",
            "confidence": 0.95,
            "mode": "REACTIVE",
            "validation": {"verified": True},
            "results": [{"effect": "cube_created"}]
        }
        
        pattern_id = self.memory.store_pattern(req, res)
        
        # 1er Éxito (ya se contó uno al crear? no, register_execution_result debe llamarse)
        self.memory.register_execution_result(pattern_id, success=True)
        self.assertEqual(self.memory.patterns[0]['metadata']['consecutive_successes'], 1)
        self.assertEqual(self.memory.patterns[0]['metadata']['status'], "STAGING")
        
        # 2do Éxito
        self.memory.register_execution_result(pattern_id, success=True)
        self.assertEqual(self.memory.patterns[0]['metadata']['consecutive_successes'], 2)
        
        # 3er Éxito -> PROMOCIÓN
        self.memory.register_execution_result(pattern_id, success=True)
        self.assertEqual(self.memory.patterns[0]['metadata']['status'], "VERIFIED")
        
        # Verificar movimiento físico
        self.assertEqual(len(self.memory.staging_repo.load_all()), 0)
        self.assertEqual(len(self.memory.verified_repo.load_all()), 1)

    def test_degradacion_a_quarantine_tras_2_fallos(self):
        """2 fallos deben mover el patrón a QUARANTINE."""
        req = "Crea un cubo rojo"
        res = {
            "success": True,
            "command_executed": "blender.create_cube",
            "confidence": 0.95,
            "mode": "REACTIVE",
            "validation": {"verified": True},
            "results": [{"effect": "cube_created"}]
        }
        
        pattern_id = self.memory.store_pattern(req, res)
        
        # 1er Fallo
        self.memory.register_execution_result(pattern_id, success=False)
        self.assertEqual(self.memory.patterns[0]['metadata']['fails'], 1)
        self.assertEqual(self.memory.patterns[0]['metadata']['status'], "STAGING")
        
        # 2do Fallo -> DEGRADACIÓN
        self.memory.register_execution_result(pattern_id, success=False)
        self.assertEqual(self.memory.patterns[0]['metadata']['status'], "QUARANTINE")
        
        # Verificar movimiento físico
        self.assertEqual(len(self.memory.staging_repo.load_all()), 0)
        self.assertEqual(len(self.memory.quarantine_repo.load_all()), 1)

    @patch('core.agent.HumanGate')
    def test_agent_pide_permiso_en_staging(self, mock_gate):
        """El Agent debe forzar ASK si el patrón está en STAGING."""
        # Setup Agent con nuestra memoria de test
        agent = Agent()
        agent.pattern_memory = self.memory
        
        # Crear patrón en STAGING
        pattern = {
            "pattern_id": "test_staging_123",
            "user_request": "ejecuta test",
            "intent": {"command_name": "blender.test", "confidence": 0.9, "parameters": {}},
            "metadata": {"status": "STAGING"}
        }
        self.memory.patterns = [pattern]
        self.memory.staging_repo.add_pattern(pattern)
        
        # Simular evocación (inyectar el pattern_id en la intención)
        with patch('core.agent.IntentRouter') as mock_router_class:
            mock_router_instance = mock_router_class.return_value
            mock_best = MagicMock()
            mock_best.command_name = "blender.test"
            mock_best.confidence = 0.95
            mock_best.parameters = {}
            mock_best.pattern_id = "test_staging_123" # Simular que se encontró este patrón
            mock_router_instance.detect_intent.return_value = ([mock_best], "explicación")
            
            # Forzar autoría verificada
            agent.authorized = True
            
            # Procesar petición
            result = agent.process_natural_request("ejecuta test")
            
            # Verificar que el resultado indica espera de confirmación
            self.assertEqual(result.get('action'), 'AWAITING_CONFIRMATION')
            self.assertIn("STAGING", result.get('feedback'))

if __name__ == "__main__":
    unittest.main()
