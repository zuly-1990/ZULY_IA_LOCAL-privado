"""
Test Integration End-to-End
Pruebas de flujo completo: crear → modificar → renderizar.
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.adapters.mock_adapter import MockAdapter
from core.commands.blender_handlers.primitives import create_cube_handler, create_sphere_handler
from core.commands.blender_handlers.transforms import move_object_handler, scale_object_handler
from core.commands.blender_handlers.render import render_scene_handler
from core.commands.blender_handlers.advanced.materials import create_material_handler, apply_material_handler
from core.commands.blender_handlers.advanced.modifiers import add_subdivision_surface_handler
from core.commands.blender_handlers.advanced.lights import create_light_handler
from core.commands.blender_handlers.advanced.cameras import create_camera_handler


class TestIntegrationEndToEnd(unittest.TestCase):
    """Tests de integración end-to-end."""
    
    def setUp(self):
        self.adapter = MockAdapter()
    
    def test_complete_scene_workflow(self):
        """
        Flujo completo: Crear escena → Modificar → Agregar luz/cámara → Render.
        """
        # 1. Crear objetos base
        cube = create_cube_handler({'location': [0, 0, 0]}, adapter=self.adapter)
        self.assertTrue(cube['success'], "Cube creation failed")
        
        sphere = create_sphere_handler({'location': [3, 0, 0], 'radius': 0.5}, adapter=self.adapter)
        self.assertTrue(sphere['success'], "Sphere creation failed")
        
        # 2. Crear y aplicar material
        mat = create_material_handler({
            'name': 'RedMetal',
            'color': [1.0, 0.2, 0.2, 1.0],
            'metallic': 0.8,
            'roughness': 0.2
        }, adapter=self.adapter)
        self.assertTrue(mat['success'], "Material creation failed")
        
        apply_result = apply_material_handler({
            'object_name': cube['object_name'],
            'material_name': 'RedMetal'
        }, adapter=self.adapter)
        self.assertTrue(apply_result['success'], "Material application failed")
        
        # 3. Agregar modificador
        subsurf = add_subdivision_surface_handler({
            'object_name': cube['object_name'],
            'levels': 2
        }, adapter=self.adapter)
        self.assertTrue(subsurf['success'], "Modifier failed")
        
        # 4. Transformar objeto
        move = move_object_handler({
            'object_name': cube['object_name'],
            'location': [0, 0, 1]
        }, adapter=self.adapter)
        self.assertTrue(move['success'], "Move failed")
        
        scale = scale_object_handler({
            'object_name': cube['object_name'],
            'scale': 1.5
        }, adapter=self.adapter)
        self.assertTrue(scale['success'], "Scale failed")
        
        # 5. Crear iluminación
        light = create_light_handler({
            'name': 'MainLight',
            'light_type': 'SUN',
            'energy': 5.0
        }, adapter=self.adapter)
        self.assertTrue(light['success'], "Light creation failed")
        
        # 6. Crear cámara
        camera = create_camera_handler({
            'name': 'RenderCam',
            'location': [7, -7, 5],
            'focal_length': 35
        }, adapter=self.adapter)
        self.assertTrue(camera['success'], "Camera creation failed")
        
        # 7. Renderizar
        render = render_scene_handler({
            'output_path': 'temp/integration_test_render.png',
            'resolution': [1920, 1080],
            'samples': 64
        }, adapter=self.adapter)
        self.assertTrue(render['success'], "Render failed")
        
        # Verificar estado final de la escena
        scene_state = self.adapter.get_scene_state()
        self.assertGreaterEqual(scene_state['object_count'], 2)
    
    def test_multiple_objects_workflow(self):
        """
        Crear múltiples objetos y verificar que todos existen.
        """
        objects_created = []
        
        # Crear 5 cubos en diferentes posiciones
        for i in range(5):
            result = create_cube_handler({
                'location': [i * 2, 0, 0]
            }, adapter=self.adapter)
            self.assertTrue(result['success'])
            objects_created.append(result['object_name'])
        
        # Verificar que hay al menos 5 objetos
        scene = self.adapter.get_scene_state()
        self.assertGreaterEqual(scene['object_count'], 5)
    
    def test_material_workflow(self):
        """
        Crear múltiples materiales y aplicarlos a diferentes objetos.
        """
        # Crear objetos
        cube1 = create_cube_handler({'location': [0, 0, 0]}, adapter=self.adapter)
        cube2 = create_cube_handler({'location': [3, 0, 0]}, adapter=self.adapter)
        
        # Crear materiales diferentes
        mat1 = create_material_handler({
            'name': 'BlueMaterial',
            'color': [0.2, 0.2, 1.0, 1.0]
        }, adapter=self.adapter)
        
        mat2 = create_material_handler({
            'name': 'GreenMaterial', 
            'color': [0.2, 1.0, 0.2, 1.0]
        }, adapter=self.adapter)
        
        # Aplicar materiales
        apply1 = apply_material_handler({
            'object_name': cube1['object_name'],
            'material_name': 'BlueMaterial'
        }, adapter=self.adapter)
        
        apply2 = apply_material_handler({
            'object_name': cube2['object_name'],
            'material_name': 'GreenMaterial'
        }, adapter=self.adapter)
        
        self.assertTrue(apply1['success'])
        self.assertTrue(apply2['success'])


class TestEdgeCases(unittest.TestCase):
    """Tests de casos extremos."""
    
    def setUp(self):
        self.adapter = MockAdapter()
    
    def test_invalid_scale_zero(self):
        """Scale = 0 debe fallar."""
        result = create_cube_handler({'scale': 0}, adapter=self.adapter)
        self.assertFalse(result['success'])
    
    def test_invalid_scale_negative(self):
        """Scale negativo debe fallar."""
        result = create_cube_handler({'scale': -1.0}, adapter=self.adapter)
        self.assertFalse(result['success'])
    
    def test_invalid_location_format(self):
        """Location como string debe fallar."""
        result = create_cube_handler({'location': "0,0,0"}, adapter=self.adapter)
        self.assertFalse(result['success'])
    
    def test_apply_material_nonexistent_object(self):
        """Aplicar material a objeto inexistente debe fallar."""
        create_material_handler({'name': 'TestMat'}, adapter=self.adapter)
        result = apply_material_handler({
            'object_name': 'NonExistentObject999',
            'material_name': 'TestMat'
        }, adapter=self.adapter)
        self.assertFalse(result['success'])
    
    def test_modifier_on_nonexistent_object(self):
        """Modifier en objeto inexistente debe fallar."""
        result = add_subdivision_surface_handler({
            'object_name': 'NonExistent',
            'levels': 2
        }, adapter=self.adapter)
        self.assertFalse(result['success'])
    
    def test_extreme_subdivision_levels(self):
        """Subdivision > 6 debe fallar."""
        cube = create_cube_handler({}, adapter=self.adapter)
        result = add_subdivision_surface_handler({
            'object_name': cube['object_name'],
            'levels': 10  # Demasiado alto
        }, adapter=self.adapter)
        self.assertFalse(result['success'])
    
    def test_empty_render_path(self):
        """Render sin path especificado debería usar default."""
        result = render_scene_handler({}, adapter=self.adapter)
        self.assertTrue(result['success'])


if __name__ == '__main__':
    unittest.main()
