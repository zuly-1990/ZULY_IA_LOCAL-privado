"""
Test de Conciencia de Contexto Blender (Fase D) - Standalone
Verifica que Zuly pueda "verse a sí misma" en el entorno Blender.
"""

import sys
import unittest
from unittest.mock import MagicMock, patch

# Añadir root al path para importar core
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.agent import Agent
from core.environment.blender_context import get_blender_context

class TestBlenderContextAwareness(unittest.TestCase):

    def setUp(self):
        # Limpiar bpy de sys.modules antes de cada test para evitar contaminación
        if 'bpy' in sys.modules:
            del sys.modules['bpy']

    def tearDown(self):
        if 'bpy' in sys.modules:
            del sys.modules['bpy']

    def test_blender_context_external(self):
        """Verifica el comportamiento cuando NO hay Blender (entorno externo)."""
        # Asegurarse de que no existe bpy
        if 'bpy' in sys.modules:
            del sys.modules['bpy']

        context = get_blender_context()
        
        self.assertFalse(context["is_blender"])
        self.assertEqual(context["mode"], "external_script")
        self.assertIn("executable", context)

    def test_blender_context_internal(self):
        """Verifica el comportamiento DENTRO de Blender (simulado)."""
        # Simular bpy
        mock_bpy = MagicMock()
        mock_bpy.app.version_string = "4.2.0"
        mock_bpy.app.background = True
        mock_bpy.data.filepath = "/path/to/test_project.blend"
        mock_bpy.context.scene.name = "Scene_Master"
        
        # Inyectar
        with patch.dict(sys.modules, {"bpy": mock_bpy}):
            context = get_blender_context()
            
            self.assertTrue(context["is_blender"])
            self.assertEqual(context["mode"], "background")
            self.assertEqual(context["active_scene"], "Scene_Master")
            self.assertEqual(context["version"], "4.2.0")

    def test_agent_analyze_scene_integration(self):
        """Verifica que el Agente integre todo en analyze_scene()."""
        # Simular bpy para que el agente crea que está en Blender
        mock_bpy = MagicMock()
        mock_bpy.app.version_string = "4.2.0"
        mock_bpy.app.background = True
        mock_bpy.data.filepath = "/path/to/test_project.blend"
        mock_bpy.context.scene.name = "Scene_Master"
        
        # Simular colecciones para el Observer
        main_col = MagicMock()
        main_col.name = "Collection"
        main_col.objects = []
        main_col.children = []
        mock_bpy.context.scene.collection = main_col
        # Simular lista de objetos vacía para iteración
        mock_bpy.data.objects = []

        with patch.dict(sys.modules, {"bpy": mock_bpy}):
            # Importar Agent DENTRO del patch para que coja el bpy simulado si lo importa
            # (Aunque Agent lo importa en top-level, get_blender_context lo hace dentro de la función)
            # BlenderObserver sí importa bpy dentro de su método snapshot o top-level?
            # En mi código blender_observer hace import bpy dentro de try pero la clase es top level.
            # Veamos blender_observer.py: "try: import bpy ... except ImportError".
            # Si inyecto bpy en sys.modules, el import funcionará.
            
            agent = Agent(auto_monitor=False)
            
            # Ejecutar análisis
            analysis = agent.analyze_scene()
            
            # Verificar estructura básica
            self.assertIn("context", analysis)
            self.assertIn("visual_snapshot", analysis)
            self.assertIn("semantic_interpretation", analysis)
            self.assertIn("collections_hierarchy", analysis)
            
            # Verificar datos del contexto
            self.assertTrue(analysis["context"]["is_blender"])
            self.assertEqual(analysis["context"]["active_scene"], "Scene_Master")
            
            # Verificar datos semánticos
            self.assertEqual(analysis["semantic_interpretation"]["scene_type"], "EMPTY_SCENE")

if __name__ == '__main__':
    unittest.main()
