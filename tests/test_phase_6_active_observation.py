"""
Test Fase 6 - Observación Activa (Simulada)
Valida que ZULY piensa antes de actuar y detecta contradicciones.
"""

import sys
import unittest
from unittest.mock import MagicMock, patch
import os

# Asegurar path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.agent import Agent

class TestPhase6ActiveObservation(unittest.TestCase):
    
    def setUp(self):
        if 'bpy' in sys.modules:
            del sys.modules['bpy']

    def tearDown(self):
        if 'bpy' in sys.modules:
            del sys.modules['bpy']

    def test_1_delete_cube_on_empty_scene_contradiction(self):
        """
        ESCENARIO OBLIGATORIO:
        Escena vacía + Intención "borrar cubo"
        Esperado: Contradicción TRUE, Acción Ejecutada FALSE
        """
        # 1. Configurar Escena Vacía
        mock_bpy = MagicMock()
        mock_bpy.app.background = True
        mock_bpy.data.objects = []
        mock_bpy.context.scene.collection.children = []
        
        # Mock Intent
        mock_intent = MagicMock()
        mock_intent.command_name = "borrar_objeto"
        mock_intent.parameters = {"name": "cubo"}
        mock_intent.confidence = 0.95
        
        with patch.dict(sys.modules, {"bpy": mock_bpy}):
            agent = Agent(auto_monitor=False)
            
            # Mockear NLU para aislar la prueba del simulador
            agent.nlu.process = MagicMock(return_value=[mock_intent])
            
            # 2. Simular intención
            result = agent.simulate_intention("borrar cubo")
            
            # 3. Validaciones de FASE 6
            print(f"\nResultado Simulación (Vacío): {result}")
            
            self.assertTrue(result['contradiccion'], "Debe haber contradicción (cubo no existe)")
            self.assertFalse(result['accion_ejecutada'], "NUNCA debe ejecutar acción")
            self.assertIn("no existe", result['razon'].lower())
            
            # Validar sugerencias inteligentes
            sugerencias = " ".join(result['opciones_sugeridas']).lower()
            self.assertTrue("crear" in sugerencias or "listar" in sugerencias, 
                           "Debe sugerir crear o listar")

    def test_2_delete_cube_on_valid_scene(self):
        """
        ESCENARIO:
        Escena con Cubo + Intención "borrar cubo"
        Esperado: Contradicción FALSE, Acción Ejecutada FALSE (Simulación viable)
        """
        # 1. Configurar Escena con Cubo
        mock_bpy = MagicMock()
        mock_bpy.app.background = True
        
        cube = MagicMock()
        cube.name = "Cube"
        cube.type = "MESH"
        
        mock_bpy.data.objects = [cube]
        mock_bpy.context.scene.collection.objects = [cube]
        
        # Mock Intent
        mock_intent = MagicMock()
        mock_intent.command_name = "borrar_objeto"
        mock_intent.parameters = {"name": "Cube"}
        mock_intent.confidence = 0.95

        with patch.dict(sys.modules, {"bpy": mock_bpy}):
            agent = Agent(auto_monitor=False)
            agent.nlu.process = MagicMock(return_value=[mock_intent])
            
            # 2. Simular intención
            result = agent.simulate_intention("borrar el objeto Cube")
            
            # 3. Validaciones
            print(f"\nResultado Simulación (Con Cubo): {result}")
            
            self.assertFalse(result['contradiccion'], "No debe haber contradicción (cubo existe)")
            self.assertFalse(result['accion_ejecutada'], "Aun siendo viable, NUNCA ejecuta en simulación")
            self.assertIn("existe y está listo", result['estado_detectado'])

    def test_3_safety_guarantee(self):
        """Valida que simulate_intention NUNCA llama a execute_command."""
        with patch.object(Agent, '_execute_intent') as mock_exec:
             agent = Agent(auto_monitor=False)
             # Mockear scene analysis para no depender de bpy
             with patch.object(agent, 'analyze_scene', return_value={'visual_snapshot': {'objects': []}}):
                 agent.simulate_intention("crear esfera")
                 
             mock_exec.assert_not_called()

if __name__ == '__main__':
    unittest.main()
