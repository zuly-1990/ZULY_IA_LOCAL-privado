"""
Tests para WO-002: Firma del Autor en C2

Valida que:
1. save() lanza excepción si falta firma
2. save() lanza excepción si autor_id no coincide
3. Rechazo del autor se persiste en DISCO (no en C2)
4. score_final y confianza se calculan correctamente
5. No existe camino que llame __persist() sin validación
"""

import unittest
import tempfile
import json
import os
from pathlib import Path
from unittest.mock import patch, MagicMock

# Importar el módulo a testear
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.cognition.c2_pattern_storage import (
    PatternStorageV2, 
    AuthorSignature, 
    PatternRecord
)


class TestWO002AuthorSignature(unittest.TestCase):
    """Test para AuthorSignature"""
    
    def test_valid_signature(self):
        """Firma válida debe pasar validación"""
        sig = AuthorSignature(
            autor_id="17a08a21-8eef-41b5-ac6b-bbd620a45fa4",
            autor_aprueba=True,
            autor_nota="Patrón aprobado"
        )
        self.assertTrue(sig.is_valid())
    
    def test_invalid_signature_empty_nota(self):
        """Firma con nota vacía debe fallar"""
        sig = AuthorSignature(
            autor_id="17a08a21-8eef-41b5-ac6b-bbd620a45fa4",
            autor_aprueba=True,
            autor_nota=""  # ← Vacío = inválido
        )
        self.assertFalse(sig.is_valid())
    
    def test_invalid_signature_empty_id(self):
        """Firma con ID vacío debe fallar"""
        sig = AuthorSignature(
            autor_id="",  # ← Vacío = inválido
            autor_aprueba=True,
            autor_nota="Válido"
        )
        self.assertFalse(sig.is_valid())


class TestWO002PatternSave(unittest.TestCase):
    """Tests para el método save()"""
    
    def setUp(self):
        """Setup: crear storage temporal para cada test"""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.temp_dir.name, 'test.db')
        self.diag_path = os.path.join(self.temp_dir.name, 'diagnósticos.jsonl')
        
        # Crear .zuly_identity.key temporal
        self.identity_file = os.path.join(self.temp_dir.name, '.zuly_identity.key')
        self.test_author_id = "17a08a21-8eef-41b5-ac6b-bbd620a45fa4"
        with open(self.identity_file, 'w') as f:
            f.write(self.test_author_id)
        
        # Parchear la ruta del archivo de identidad
        self.orig_cwd = os.getcwd()
        os.chdir(self.temp_dir.name)
    
    def tearDown(self):
        """Limpieza después de cada test"""
        os.chdir(self.orig_cwd)
        self.temp_dir.cleanup()
    
    def test_save_sin_firma_falta_autor_id(self):
        """❌ save() sin autor_id debe lanzar excepción"""
        storage = PatternStorageV2(db_path=self.db_path, diagnostics_log_path=self.diag_path)
        
        pattern = {
            "pattern_name": "test_pattern",
            "pattern_type": "primitive",
            "origin": "real_execution",
            "intent": "test",
            "handlers": [],
            "scene_before": {},
            "scene_after": {},
            "validation_v0": "OK",
            "score_c1": 80.0,
            # Falta: autor_id, autor_aprueba, autor_nota
        }
        
        with self.assertRaises(ValueError) as cm:
            storage.save(pattern)
        
        self.assertIn("autor_id", str(cm.exception))
        self.assertIn("BLOCKED", str(cm.exception))
    
    def test_save_sin_firma_falta_autor_aprueba(self):
        """❌ save() sin autor_aprueba debe lanzar excepción"""
        storage = PatternStorageV2(db_path=self.db_path, diagnostics_log_path=self.diag_path)
        
        pattern = {
            "pattern_name": "test_pattern",
            "pattern_type": "primitive",
            "origin": "real_execution",
            "intent": "test",
            "handlers": [],
            "scene_before": {},
            "scene_after": {},
            "validation_v0": "OK",
            "score_c1": 80.0,
            "autor_id": self.test_author_id,
            # Falta: autor_aprueba, autor_nota
        }
        
        with self.assertRaises(ValueError) as cm:
            storage.save(pattern)
        
        self.assertIn("autor_aprueba", str(cm.exception))
    
    def test_save_sin_firma_falta_autor_nota(self):
        """❌ save() sin autor_nota debe lanzar excepción"""
        storage = PatternStorageV2(db_path=self.db_path, diagnostics_log_path=self.diag_path)
        
        pattern = {
            "pattern_name": "test_pattern",
            "pattern_type": "primitive",
            "origin": "real_execution",
            "intent": "test",
            "handlers": [],
            "scene_before": {},
            "scene_after": {},
            "validation_v0": "OK",
            "score_c1": 80.0,
            "autor_id": self.test_author_id,
            "autor_aprueba": True,
            # Falta: autor_nota
        }
        
        with self.assertRaises(ValueError) as cm:
            storage.save(pattern)
        
        self.assertIn("autor_nota", str(cm.exception))
    
    def test_save_autor_id_no_coincide(self):
        """❌ save() con autor_id incorrecto debe lanzar SECURITY exception"""
        storage = PatternStorageV2(db_path=self.db_path, diagnostics_log_path=self.diag_path)
        
        pattern = {
            "pattern_name": "test_pattern",
            "pattern_type": "primitive",
            "origin": "real_execution",
            "intent": "test",
            "handlers": [],
            "scene_before": {},
            "scene_after": {},
            "validation_v0": "OK",
            "score_c1": 80.0,
            "autor_id": "WRONG_ID_COMO_SI_FUERA_DE_OTRA_MAQUINA",
            "autor_aprueba": True,
            "autor_nota": "Test"
        }
        
        with self.assertRaises(ValueError) as cm:
            storage.save(pattern)
        
        self.assertIn("SECURITY", str(cm.exception))
        self.assertIn("coincide", str(cm.exception))
    
    def test_save_autor_rechaza_patrones_no_entra_a_c2(self):
        """✓ save() con autor_aprueba=False → rechazo persistido, NO en C2"""
        storage = PatternStorageV2(db_path=self.db_path, diagnostics_log_path=self.diag_path)
        
        pattern = {
            "pattern_name": "test_pattern_rechazado",
            "pattern_type": "primitive",
            "origin": "real_execution",
            "intent": "test",
            "handlers": [],
            "scene_before": {},
            "scene_after": {},
            "validation_v0": "OK",
            "score_c1": 80.0,
            "autor_id": self.test_author_id,
            "autor_aprueba": False,
            "autor_nota": "Cubo inclinado, rechazado"
        }
        
        ok, message = storage.save(pattern)
        
        # Debe retornar False (no guardado)
        self.assertFalse(ok)
        self.assertIn("rechazado", message.lower())
        
        # Patrón NO debe estar en C2
        retrieved = storage.get_pattern_by_name("test_pattern_rechazado")
        self.assertIsNone(retrieved)
        
        # Pero DEBE estar en diagnósticos (DISCO)
        self.assertTrue(self.diag_path.exists() or Path(self.diag_path).exists())
        with open(self.diag_path, 'r') as f:
            content = f.read()
            if content.strip():
                event = json.loads(content.strip().split('\n')[0])
                self.assertEqual(event['pattern_name'], "test_pattern_rechazado")
                self.assertIn("rechazado", event['event_type'])
    
    def test_save_con_firma_valida_entra_a_c2(self):
        """✓ save() con firma válida → persiste en C2 con confianza alta"""
        storage = PatternStorageV2(db_path=self.db_path, diagnostics_log_path=self.diag_path)
        
        pattern = {
            "pattern_name": "test_pattern_aprobado",
            "pattern_type": "primitive",
            "origin": "real_execution",
            "intent": "create a cube",
            "handlers": ["create_cube"],
            "scene_before": {"objects": 0},
            "scene_after": {"objects": 1},
            "validation_v0": "OK",
            "score_c1": 87.0,
            "autor_id": self.test_author_id,
            "autor_aprueba": True,
            "autor_nota": "Perfecto, listo para reusar"
        }
        
        ok, message = storage.save(pattern)
        
        # Debe retornar True (guardado)
        self.assertTrue(ok)
        self.assertIn("✓", message)
        
        # Patrón DEBE estar en C2
        retrieved = storage.get_pattern_by_name("test_pattern_aprobado")
        self.assertIsNotNone(retrieved)
        
        # Verificar score_final y confianza
        self.assertEqual(retrieved['confianza'], 95)  # Máxima confianza
        expected_score = min(87.0 * 1.15, 100.0)  # 87 * 1.15 = 100.05 → capped at 100
        self.assertEqual(retrieved['score_final'], expected_score)


class TestWO002ScoreCalculation(unittest.TestCase):
    """Tests para cálculo de score_final y confianza"""
    
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.temp_dir.name, 'test.db')
        self.diag_path = os.path.join(self.temp_dir.name, 'diag.jsonl')
        
        self.identity_file = os.path.join(self.temp_dir.name, '.zuly_identity.key')
        self.test_author_id = "17a08a21-8eef-41b5-ac6b-bbd620a45fa4"
        with open(self.identity_file, 'w') as f:
            f.write(self.test_author_id)
        
        self.orig_cwd = os.getcwd()
        os.chdir(self.temp_dir.name)
    
    def tearDown(self):
        os.chdir(self.orig_cwd)
        self.temp_dir.cleanup()
    
    def test_score_final_con_boost(self):
        """score_final = C1_score * 1.15 (boost por autor)"""
        storage = PatternStorageV2(db_path=self.db_path, diagnostics_log_path=self.diag_path)
        
        pattern = {
            "pattern_name": "test_boost",
            "pattern_type": "primitive",
            "origin": "real_execution",
            "intent": "test",
            "handlers": [],
            "scene_before": {},
            "scene_after": {},
            "validation_v0": "OK",
            "score_c1": 80.0,  # Score de C1
            "autor_id": self.test_author_id,
            "autor_aprueba": True,
            "autor_nota": "Aprobado"
        }
        
        storage.save(pattern)
        retrieved = storage.get_pattern_by_name("test_boost")
        
        # Debe ser 80 * 1.15 = 92.0
        self.assertEqual(retrieved['score_final'], 92.0)
        self.assertEqual(retrieved['confianza'], 95)
    
    def test_score_final_capped_at_100(self):
        """score_final debe estar caped en 100.0"""
        storage = PatternStorageV2(db_path=self.db_path, diagnostics_log_path=self.diag_path)
        
        pattern = {
            "pattern_name": "test_cap",
            "pattern_type": "primitive",
            "origin": "real_execution",
            "intent": "test",
            "handlers": [],
            "scene_before": {},
            "scene_after": {},
            "validation_v0": "OK",
            "score_c1": 95.0,  # 95 * 1.15 = 109.25 → debe capar a 100
            "autor_id": self.test_author_id,
            "autor_aprueba": True,
            "autor_nota": "Excelente"
        }
        
        storage.save(pattern)
        retrieved = storage.get_pattern_by_name("test_cap")
        
        # Debe estar capeado en 100.0
        self.assertEqual(retrieved['score_final'], 100.0)


class TestWO002PrivatePersist(unittest.TestCase):
    """Tests para verificar que __persist() es privado y no accesible directamente"""
    
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.temp_dir.name, 'test.db')
        self.diag_path = os.path.join(self.temp_dir.name, 'diag.jsonl')
        
        self.identity_file = os.path.join(self.temp_dir.name, '.zuly_identity.key')
        self.test_author_id = "17a08a21-8eef-41b5-ac6b-bbd620a45fa4"
        with open(self.identity_file, 'w') as f:
            f.write(self.test_author_id)
        
        self.orig_cwd = os.getcwd()
        os.chdir(self.temp_dir.name)
    
    def tearDown(self):
        os.chdir(self.orig_cwd)
        self.temp_dir.cleanup()
    
    def test_persist_is_private(self):
        """__persist() debe ser inaccesible directamente (name mangling)"""
        storage = PatternStorageV2(db_path=self.db_path, diagnostics_log_path=self.diag_path)
        
        # Intentar acceder a __persist() debe fallar
        self.assertFalse(hasattr(storage, '__persist'))
        self.assertFalse(callable(getattr(storage, '__persist', None)))
        
        # Pero sí existe el método mangled
        self.assertTrue(hasattr(storage, f'_PatternStorageV2__persist'))


if __name__ == '__main__':
    unittest.main(verbosity=2)
