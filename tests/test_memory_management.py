"""
test_memory_management.py

Tests para Fase 19: Gestión de Memoria y Trazas
"""

import sys
import os
import unittest
import tempfile
import json
import gzip
from datetime import datetime, timedelta
from pathlib import Path

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.memory.retention_policy import RetentionPolicy, RetentionConfig
from core.memory.archiver import SessionArchiver
from core.memory.memory_manager import MemoryManager
from core.memory.trace_core import TraceCore
from core.observability.action_logger import ActionLogger


class TestRetentionPolicy(unittest.TestCase):
    """Tests para RetentionPolicy."""
    
    def test_default_policies_exist(self):
        """Test que políticas por defecto existen."""
        policy = RetentionPolicy()
        
        self.assertIn('trace_core', policy.get_all_policies())
        self.assertIn('action_logger', policy.get_all_policies())
    
    def test_get_policy(self):
        """Test obtener política para componente."""
        policy = RetentionPolicy()
        
        config = policy.get_policy('trace_core')
        
        self.assertIsInstance(config, RetentionConfig)
        self.assertEqual(config.max_live_items, 1000)
    
    def test_should_archive(self):
        """Test determinar si debe archivar."""
        policy = RetentionPolicy()
        
        # Trace_core archiva después de 30 días
        self.assertFalse(policy.should_archive('trace_core', 10))
        self.assertTrue(policy.should_archive('trace_core', 40))
    
    def test_should_cleanup(self):
        """Test determinar si debe hacer cleanup."""
        policy = RetentionPolicy()
        
        # Trace_core max 1000 items
        self.assertFalse(policy.should_cleanup('trace_core', 500))
        self.assertTrue(policy.should_cleanup('trace_core', 1500))
    
    def test_custom_policy(self):
        """Test política personalizada."""
        custom_config = RetentionConfig(
            max_live_items=100,
            archive_after_days=5,
            compress_archives=False
        )
        
        policy = RetentionPolicy({'custom_component': custom_config})
        
        config = policy.get_policy('custom_component')
        self.assertEqual(config.max_live_items, 100)
        self.assertEqual(config.archive_after_days, 5)
        self.assertFalse(config.compress_archives)


class TestSessionArchiver(unittest.TestCase):
    """Tests para SessionArchiver."""
    
    def setUp(self):
        """Setup temporal directory."""
        self.temp_dir = tempfile.mkdtemp()
        self.archiver = SessionArchiver(self.temp_dir)
    
    def tearDown(self):
        """Cleanup temporal directory."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_archive_file_compressed(self):
        """Test archivar archivo con compresión."""
        # Crear archivo temporal
        test_file = Path(self.temp_dir) / 'test_session.json'
        test_data = {'test': 'data', 'value': 123}
        
        with open(test_file, 'w') as f:
            json.dump(test_data, f)
        
        # Archivar
        archived_path = self.archiver.archive_file(str(test_file), compress=True)
        
        # Verificar
        self.assertIsNotNone(archived_path)
        self.assertTrue(archived_path.endswith('.gz'))
        self.assertFalse(test_file.exists())  # Original eliminado
        
        # Verificar que está comprimido y tiene contenido correcto
        with gzip.open(archived_path, 'rt', encoding='utf-8') as f:
            loaded_data = json.load(f)
        
        self.assertEqual(loaded_data, test_data)
    
    def test_archive_old_files(self):
        """Test archivar archivos antiguos."""
        # Crear archivos de diferentes edades
        old_file = Path(self.temp_dir) / 'old_session.json'
        recent_file = Path(self.temp_dir) / 'recent_session.json'
        
        # Crear archivos
        for filepath in [old_file, recent_file]:
            with open(filepath, 'w') as f:
                json.dump({'data': 'test'}, f)
        
        # Modificar mtime del archivo antiguo
        old_time = (datetime.now() - timedelta(days=10)).timestamp()
        os.utime(old_file, (old_time, old_time))
        
        # Archivar archivos > 5 días
        archived = self.archiver.archive_old_files(age_days=5)
        
        # Verificar que solo se archivó el antiguo
        self.assertEqual(len(archived), 1)
        self.assertFalse(old_file.exists())
        self.assertTrue(recent_file.exists())
    
    def test_restore_file(self):
        """Test restaurar archivo archivado."""
        # Crear y archivar archivo
        test_file = Path(self.temp_dir) / 'session.json'
        test_data = {'restored': True}
        
        with open(test_file, 'w') as f:
            json.dump(test_data, f)
        
        archived_path = self.archiver.archive_file(str(test_file), compress=True)
        
        # Restaurar
        restore_dir = Path(self.temp_dir) / 'restored'
        restore_dir.mkdir()
        
        restored_path = self.archiver.restore_file(archived_path, str(restore_dir))
        
        # Verificar
        self.assertIsNotNone(restored_path)
        self.assertTrue(Path(restored_path).exists())
        
        with open(restored_path, 'r') as f:
            loaded_data = json.load(f)
        
        self.assertEqual(loaded_data, test_data)
    
    def test_get_archive_stats(self):
        """Test obtener estadísticas de archives."""
        # Crear y archivar algunos archivos
        for i in range(3):
            test_file = Path(self.temp_dir) / f'session_{i}.json'
            with open(test_file, 'w') as f:
                json.dump({'index': i}, f)
            
            self.archiver.archive_file(str(test_file), compress=True)
        
        # Obtener stats
        stats = self.archiver.get_archive_stats()
        
        # Verificar
        self.assertEqual(stats['total_archived_files'], 3)
        self.assertGreater(stats['total_size_bytes'], 0)


class TestMemoryManager(unittest.TestCase):
    """Tests para MemoryManager."""
    
    def setUp(self):
        """Setup temporal directories."""
        self.temp_base = tempfile.mkdtemp()
        self.logs_dir = Path(self.temp_base) / 'logs' / 'actions'
        self.logs_dir.mkdir(parents=True)
        
        self.memory_dir = Path(self.temp_base) / 'memory'
        self.memory_dir.mkdir(parents=True)
    
    def tearDown(self):
        """Cleanup."""
        import shutil
        shutil.rmtree(self.temp_base, ignore_errors=True)
    
    def test_get_memory_report(self):
        """Test generar reporte de memoria."""
        manager = MemoryManager()
        
        report = manager.get_memory_report()
        
        # Verificar estructura
        self.assertIn('timestamp', report)
        self.assertIn('policies', report)
        self.assertIn('components', report)
        self.assertIn('summary', report)
        
        # Verificar summary
        self.assertIn('total_active_items', report['summary'])
        self.assertIn('total_archived_items', report['summary'])


class TestTraceCoreLimits(unittest.TestCase):
    """Tests para límites de TraceCore."""
    
    def setUp(self):
        """Setup temporal trace file."""
        self.temp_dir = tempfile.mkdtemp()
        self.trace_file = os.path.join(self.temp_dir, 'traces.json')
    
    def tearDown(self):
        """Cleanup."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_trace_limit_enforced(self):
        """Test que límite de trazas se respeta."""
        trace_core = TraceCore(storage_path=self.trace_file)
        
        # Agregar más trazas que el límite
        for i in range(TraceCore.MAX_TRACES + 100):
            trace_core.append_trace({
                'intention': f'test_{i}',
                'execution_success': True
            })
        
        # Verificar que no excede el límite
        self.assertLessEqual(len(trace_core.traces), TraceCore.MAX_TRACES)


class TestActionLoggerRotation(unittest.TestCase):
    """Tests para rotación de ActionLogger."""
    
    def setUp(self):
        """Setup temporal log directory."""
        self.temp_dir = tempfile.mkdtemp()
        self.logger = ActionLogger(log_dir=self.temp_dir)
    
    def tearDown(self):
        """Cleanup."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_logger_max_records(self):
        """Test que ActionLogger respeta MAX_RECORDS."""
        # Agregar más registros que el límite
        for i in range(ActionLogger.MAX_RECORDS + 50):
            self.logger.log_ok('test_action', f'target_{i}')
        
        # Verificar que no excede el límite
        self.assertLessEqual(len(self.logger._records), ActionLogger.MAX_RECORDS)
    
    def test_session_auto_saved(self):
        """Test que sesión se guarda automáticamente en límite."""
        # Agregar registros hasta exceder límite
        for i in range(ActionLogger.MAX_RECORDS + 1):
            self.logger.log_ok('test', f'target_{i}')
        
        # Verificar que existe archivo de sesión
        session_files = list(Path(self.temp_dir).glob('session_*.json'))
        
        self.assertGreater(len(session_files), 0)


if __name__ == '__main__':
    unittest.main()
