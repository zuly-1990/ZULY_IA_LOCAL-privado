"""
Suite de Pruebas Fase 5.16 - Verificación de Estabilidad y Confianza
Objetivo: Probar que la percepción de Zuly es robusta, veraz y resiliente.

Batería:
1. Escena Vacía (Mock Empty)
2. Escena Simple Controlada (Mock Hierarchy)
3. Cambio en Vivo (Mock State Change)
4. Contexto Incorrecto (Real External)
"""

import sys
import unittest
from unittest.mock import MagicMock, patch
import os

# Asegurar path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.agent import Agent
from core.environment.blender_context import get_blender_context

class TestPhase516Verification(unittest.TestCase):
    
    def setUp(self):
        # Limpieza básica
        if 'bpy' in sys.modules:
            del sys.modules['bpy']

    def tearDown(self):
        if 'bpy' in sys.modules:
            del sys.modules['bpy']

    # 🔹 PRUEBA 1 — Escena Vacía
    def test_1_empty_scene_truth(self):
        """Valida que Zuly reconoce el vacío perfecto sin alucinaciones."""
        mock_bpy = MagicMock()
        mock_bpy.app.background = True
        mock_bpy.data.objects = []
        mock_bpy.data.filepath = "untitled.blend"
        mock_bpy.context.scene.name = "Scene"
        
        # Colección raíz vacía de hijos
        root_col = MagicMock()
        root_col.name = "Scene Collection"
        root_col.objects = []
        root_col.children = []
        mock_bpy.context.scene.collection = root_col
        
        with patch.dict(sys.modules, {"bpy": mock_bpy}):
            agent = Agent(auto_monitor=False)
            analysis = agent.analyze_scene()
            
            # Validaciones estrictas
            visual = analysis['visual_snapshot']
            semantic = analysis['semantic_interpretation']
            
            self.assertEqual(visual['object_count'], 0, "Debe contar 0 objetos")
            self.assertEqual(semantic['scene_type'], "EMPTY_SCENE", "Debe clasificar como EMPTY_SCENE")
            self.assertGreaterEqual(semantic['confidence'], 1.0, "Confianza debe ser máxima en vacío")
            
            # Validar jerarquía
            hierarchy = analysis['collections_hierarchy']
            self.assertEqual(len(hierarchy), 1)
            self.assertEqual(hierarchy[0]['name'], "Scene Collection")
            self.assertEqual(len(hierarchy[0]['children']), 0)

    # 🔹 PRUEBA 2 — Escena Simple Controlada
    def test_2_controlled_simple_structure(self):
        """Valida compresión estructural (Objetos, Tipos, Colecciones)."""
        mock_bpy = MagicMock()
        mock_bpy.app.background = True
        
        # Objetos simulados
        obj_cube = MagicMock()
        obj_cube.name = "Cube"
        obj_cube.type = "MESH"
        
        obj_light = MagicMock()
        obj_light.name = "Light"
        obj_light.type = "LIGHT"
        
        # Colecciones
        # Scene Collection -> [Env (Cube), Lgt (Light)]
        
        col_env = MagicMock()
        col_env.name = "Environment"
        col_env.objects = [obj_cube]
        col_env.children = []
        
        col_lgt = MagicMock()
        col_lgt.name = "Lighting"
        col_lgt.objects = [obj_light]
        col_lgt.children = []
        
        root_col = MagicMock()
        root_col.name = "Master"
        # Objetos directos en raíz: ninguno
        root_col.objects = [] 
        root_col.children = [col_env, col_lgt]
        
        # Configurar bpy
        mock_bpy.data.objects = [obj_cube, obj_light]
        # Necesario para observer plano:
        obj_cube.users_collection = [col_env]
        obj_light.users_collection = [col_lgt]
        
        mock_bpy.context.scene.collection = root_col
        
        with patch.dict(sys.modules, {"bpy": mock_bpy}):
            agent = Agent(auto_monitor=False)
            analysis = agent.analyze_scene()
            
            # Semántica
            sem = analysis['semantic_interpretation']
            self.assertIn("MESH", sem['object_summary'])
            self.assertIn("LIGHT", sem['object_summary'])
            
            # Estructura Jerárquica
            h = analysis['collections_hierarchy'][0] # Master
            self.assertEqual(h['name'], "Master")
            self.assertEqual(len(h['children']), 2)
            
            child_names = [c['name'] for c in h['children']]
            self.assertIn("Environment", child_names)
            self.assertIn("Lighting", child_names)
            
            # Verificar contenido profundo
            env_node = next(c for c in h['children'] if c['name'] == "Environment")
            self.assertIn("Cube", env_node['objects'])

    # 🔹 PRUEBA 3 — Cambio en Vivo
    def test_3_live_state_change(self):
        """Prueba que Zuly no tenga memoria cacheada incorrecta (fantasmas)."""
        mock_bpy = MagicMock()
        mock_bpy.app.background = True
        
        # ESTADO A: 1 Cubo
        cube = MagicMock()
        cube.name = "Cube"
        cube.type = "MESH"
        cube.users_collection = [MagicMock(name="Col")]
        
        root = MagicMock()
        root.name = "Root"
        root.objects = [cube]
        root.children = []
        
        mock_bpy.data.objects = [cube]
        mock_bpy.context.scene.collection = root
        
        with patch.dict(sys.modules, {"bpy": mock_bpy}):
            agent = Agent(auto_monitor=False)
            
            # Lectura 1
            res1 = agent.analyze_scene()
            self.assertEqual(res1['visual_snapshot']['object_count'], 1)
            
            # CAMBIO DE ESTADO (Simulando movimiento/borrado en Blender)
            # Borramos el cubo
            mock_bpy.data.objects = []
            root.objects = []
            
            # Lectura 2
            res2 = agent.analyze_scene()
            
            self.assertEqual(res2['visual_snapshot']['object_count'], 0, "Fallo: Zuly sigue viendo el cubo fantasma")
            self.assertNotEqual(res1['timestamp'], res2['timestamp'])

    # 🔹 PRUEBA 4 — Contexto Incorrecto
    def test_4_incorrect_context_external(self):
        """Valida comportamiento fuera de Blender (Realidad actual del test runner)."""
        # Asegurar limpieza
        if 'bpy' in sys.modules:
            del sys.modules['bpy']
            
        agent = Agent(auto_monitor=False)
        analysis = agent.analyze_scene()
        
        ctx = analysis['context']
        self.assertFalse(ctx['is_blender'], "Debe detectar que NO está en Blender")
        
        # Agente no debe proponer locuras
        sem = analysis['semantic_interpretation']
        self.assertEqual(sem['scene_type'], "EMPTY_SCENE", "Fuera de Blender debe asumir vacío/seguro")
        
        # Verificación extra de seguridad
        snapshot = analysis['visual_snapshot']
        self.assertEqual(snapshot['source'], "no_blender")

if __name__ == '__main__':
    unittest.main()
