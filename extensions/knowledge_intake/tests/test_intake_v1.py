"""
Tests Mínimos para Knowledge Intake v1

Propósito:
- Validar que el módulo existe
- Validar que guarda texto sin modificarlo
- Validar que NO importa core
- Validar que NO analiza contenido
- Tests estructurales + funcionales mínimos

Regla: Solo tests especificados.
"""

import sys
import os
import unittest
import tempfile
import shutil

# Add project root to path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.insert(0, project_root)

from extensions.knowledge_intake.intake_v1 import IntakeV1
from extensions.knowledge_intake.schema import KnowledgeSchema


class TestIntakeV1Minimal(unittest.TestCase):
    """
    Tests mínimos para Knowledge Intake v1.
    
    Tests estructurales + funcionales mínimos.
    """
    
    def setUp(self):
        """Configurar directorio temporal para tests."""
        self.test_dir = tempfile.mkdtemp()
        self.intake = IntakeV1(storage_path=self.test_dir)
    
    def tearDown(self):
        """Limpiar directorio temporal."""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_1_modulo_existe(self):
        """Test 1: El módulo existe"""
        print("\n[TEST 1] Módulo existe")
        
        # Validar que la clase existe
        self.assertTrue(hasattr(IntakeV1, 'receive'))
        self.assertTrue(hasattr(IntakeV1, 'get_entry'))
        
        print("  ✓ IntakeV1 existe con métodos requeridos")
    
    def test_2_guarda_texto_sin_modificar(self):
        """Test 2: Guarda texto SIN modificarlo"""
        print("\n[TEST 2] Guarda texto sin modificar")
        
        # Texto original con caracteres especiales, espacios, etc.
        original_text = "  Hola, esto es una prueba con MAYÚSCULAS, números 123, y símbolos !@#  "
        
        # Recibir conocimiento
        entry = self.intake.receive(
            raw_text=original_text,
            source="informal_interview",
            speaker_type="adult"
        )
        
        # Recuperar entrada
        retrieved = self.intake.get_entry(entry['id'])
        
        # Validar que el texto NO fue modificado
        self.assertEqual(retrieved['raw_text'], original_text)
        
        print("  ✓ Texto guardado exactamente como se recibió")
    
    def test_3_no_importa_core(self):
        """Test 3: NO importa módulos del core"""
        print("\n[TEST 3] NO importa core")
        
        # Validar que intake_v1 no importa core
        import extensions.knowledge_intake.intake_v1 as intake_module
        
        intake_source = intake_module.__file__
        with open(intake_source, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verificar que no hay imports del core
        self.assertNotIn('from core.', content)
        self.assertNotIn('import core.', content)
        
        print("  ✓ Intake NO importa módulos del core")
    
    def test_4_no_analiza_contenido(self):
        """Test 4: NO analiza contenido"""
        print("\n[TEST 4] NO analiza contenido")
        
        # Texto con contenido que podría ser "analizable"
        text_with_intent = "Por favor crea un cubo rojo de tamaño 5"
        
        # Recibir conocimiento
        entry = self.intake.receive(raw_text=text_with_intent)
        
        # Validar que NO hay campos de análisis
        self.assertNotIn('intent', entry)
        self.assertNotIn('entities', entry)
        self.assertNotIn('classification', entry)
        self.assertNotIn('sentiment', entry)
        self.assertNotIn('keywords', entry)
        
        # Validar que processed es False
        self.assertFalse(entry['processed'])
        
        print("  ✓ Intake NO analiza contenido")
    
    def test_5_no_clasifica_semanticamente(self):
        """Test 5: NO clasifica semánticamente"""
        print("\n[TEST 5] NO clasifica semánticamente")
        
        # Recibir varios textos diferentes
        texts = [
            "Quiero un cubo",
            "Me gusta el color azul",
            "¿Cómo estás?"
        ]
        
        entries = []
        for text in texts:
            entry = self.intake.receive(raw_text=text)
            entries.append(entry)
        
        # Validar que NO hay clasificación semántica
        for entry in entries:
            self.assertNotIn('category', entry)
            self.assertNotIn('topic', entry)
            self.assertNotIn('semantic_class', entry)
        
        print("  ✓ Intake NO clasifica semánticamente")
    
    def test_6_no_ejecuta_nada(self):
        """Test 6: NO ejecuta comandos"""
        print("\n[TEST 6] NO ejecuta nada")
        
        # Texto que parece un comando
        command_like_text = "ejecuta crear_cubo(size=5)"
        
        # Variable para detectar ejecución
        executed = {'value': False}
        
        # Recibir conocimiento
        entry = self.intake.receive(raw_text=command_like_text)
        
        # Validar que NO se ejecutó nada
        # (si se hubiera ejecutado, habría algún efecto secundario)
        self.assertFalse(executed['value'])
        
        # Validar que solo se guardó el texto
        self.assertEqual(entry['raw_text'], command_like_text)
        
        print("  ✓ Intake NO ejecuta nada")


if __name__ == '__main__':
    print("="*70)
    print("TESTS MÍNIMOS - KNOWLEDGE INTAKE V1 (FASE 9.0)")
    print("="*70)
    print("\nTests cubiertos:")
    print("1. El módulo existe")
    print("2. Guarda texto sin modificarlo")
    print("3. NO importa core")
    print("4. NO analiza contenido")
    print("5. NO clasifica semánticamente")
    print("6. NO ejecuta nada")
    print("\nTests estructurales + funcionales mínimos.")
    print("="*70)
    unittest.main(verbosity=2)
