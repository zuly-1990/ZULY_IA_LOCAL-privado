"""
Test Sagrado de Principios (ORDEN_ARCA_03)

Propósito:
Verificar que la memoria ética del sistema (Tabla de NOÉ)
permanece intacta e invulnerable.

Este test debe fallar si:
- El archivo TABLA_DE_NOE.md es modificado.
- El hash no coincide.
- El sistema intenta arrancar con principios corruptos.
"""

import sys
import os
import unittest
from unittest.mock import patch, mock_open

# Asegurar que podemos importar desde core
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.guards.noe_guard import NoeGuard

class TestSacredPrinciples(unittest.TestCase):
    
    def test_1_integridad_actual(self):
        """Test 1: La Tabla de NOÉ está intacta en disco."""
        print("\n[TEST 1] Verificación de Integridad Actual")
        
        # Verificar que el archivo existe
        self.assertTrue(os.path.exists(NoeGuard.SACRED_FILE_PATH), 
                       "El archivo sagrado TABLA_DE_NOE.md debe existir.")
        
        # Verificar integridad real
        is_intact = NoeGuard.verify_integrity()
        
        if is_intact:
            print("  ✓ Integridad VERIFICADA (Hash coincide)")
        else:
            self.fail("INTEGRIDAD COMPROMETIDA: El hash de TABLA_DE_NOE.md no coincide con NoeGuard.")

    def test_2_deteccion_de_manipulacion(self):
        """Test 2: El sistema detecta cualquier alteración (Simulada con archivo temporal)."""
        print("\n[TEST 2] Detección de Manipulación (Simulada)")
        
        # Crear un archivo temporal con contenido corrupto
        import tempfile
        
        with tempfile.NamedTemporaryFile(mode='wb', delete=False) as tmp:
            tmp.write(b"# HACKED CONTENT")
            tmp_path = tmp.name
            
        try:
            # Uso de _override_path para pruebas deterministas
            is_intact = NoeGuard.verify_integrity(_override_path=tmp_path)
            
            if not is_intact:
                print("  ✓ Sistema RECHAZÓ contenido alterado correctamente.")
            else:
                self.fail("FALLO DE SEGURIDAD: NoeGuard aceptó contenido alterado.")
        finally:
            # Limpieza
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

if __name__ == '__main__':
    unittest.main(verbosity=2)
