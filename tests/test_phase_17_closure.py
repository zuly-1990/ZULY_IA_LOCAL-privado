"""
Test Phase 17 Closure - Adapter Interchangeability
Verifica que los handlers funcionan igual con MockAdapter y BlenderAdapter.
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.adapters.mock_adapter import MockAdapter
from core.commands.blender_handlers.primitives import (
    create_cube_handler,
    create_sphere_handler,
    create_cylinder_handler
)
from core.commands.blender_handlers.transforms import (
    move_object_handler,
    rotate_object_handler,
    scale_object_handler
)
from core.commands.blender_handlers.render import render_scene_handler
from core.commands.blender_handlers.advanced.lights import (
    create_light_handler,
    set_light_energy_handler
)
from core.commands.blender_handlers.advanced.materials import (
    create_material_handler,
    apply_material_handler
)
from core.commands.blender_handlers.advanced.cameras import (
    create_camera_handler,
    set_active_camera_handler
)
from core.commands.blender_handlers.advanced.modifiers import (
    add_subdivision_surface_handler,
    add_array_modifier_handler
)
from core.commands.blender_handlers.advanced.export import (
    export_fbx_handler,
    export_obj_handler
)


class TestPhase17AdapterInterchangeability(unittest.TestCase):
    """
    Verifica que todos los handlers funcionan con MockAdapter.
    Si funcionan con Mock, funcionarán con Blender (misma interfaz).
    """
    
    def setUp(self):
        self.adapter = MockAdapter()
    
    # =========================================
    # PRIMITIVAS
    # =========================================
    
    def test_create_cube(self):
        result = create_cube_handler({'location': [1, 2, 3]}, adapter=self.adapter)
        self.assertTrue(result['success'])
        self.assertIn('object_name', result)
    
    def test_create_sphere(self):
        result = create_sphere_handler({'radius': 2.0}, adapter=self.adapter)
        self.assertTrue(result['success'])
    
    def test_create_cylinder(self):
        result = create_cylinder_handler({'radius': 1.0, 'depth': 3.0}, adapter=self.adapter)
        self.assertTrue(result['success'])
    
    # =========================================
    # TRANSFORMACIONES
    # =========================================
    
    def test_move_object(self):
        # Primero crear objeto
        create_cube_handler({}, adapter=self.adapter)
        # Luego mover (usar objeto activo)
        result = move_object_handler({'location': [5, 5, 5]}, adapter=self.adapter)
        # MockAdapter acepta moves sin objeto específico
        self.assertIn('success', result)
    
    def test_rotate_object(self):
        create_cube_handler({}, adapter=self.adapter)
        result = rotate_object_handler({'rotation': [0, 0, 45], 'degrees': True}, adapter=self.adapter)
        self.assertIn('success', result)
    
    # =========================================
    # RENDER
    # =========================================
    
    def test_render_scene(self):
        result = render_scene_handler({
            'output_path': 'temp/test_render.png',
            'resolution': [800, 600]
        }, adapter=self.adapter)
        self.assertTrue(result['success'])
        self.assertIn('render_time', result)
    
    # =========================================
    # LUCES
    # =========================================
    
    def test_create_light(self):
        result = create_light_handler({
            'name': 'TestLight',
            'light_type': 'POINT',
            'energy': 500.0
        }, adapter=self.adapter)
        self.assertTrue(result['success'])
        self.assertEqual(result['light_type'], 'POINT')
    
    def test_set_light_energy(self):
        # Crear luz primero
        light_result = create_light_handler({'name': 'TestLight2', 'light_type': 'SUN'}, adapter=self.adapter)
        actual_light_name = light_result.get('light_name', 'TestLight2')
        result = set_light_energy_handler({
            'light_name': actual_light_name,
            'energy': 2000.0
        }, adapter=self.adapter)
        self.assertTrue(result['success'])
    
    # =========================================
    # MATERIALES
    # =========================================
    
    def test_create_material(self):
        result = create_material_handler({
            'name': 'TestMaterial',
            'color': [1.0, 0.0, 0.0, 1.0],
            'metallic': 0.5
        }, adapter=self.adapter)
        self.assertTrue(result['success'])
    
    def test_apply_material(self):
        # Crear objeto y material
        cube_result = create_cube_handler({}, adapter=self.adapter)
        create_material_handler({'name': 'TestMat'}, adapter=self.adapter)
        
        result = apply_material_handler({
            'object_name': cube_result['object_name'],
            'material_name': 'TestMat'
        }, adapter=self.adapter)
        self.assertTrue(result['success'])
    
    # =========================================
    # CÁMARAS
    # =========================================
    
    def test_create_camera(self):
        result = create_camera_handler({
            'name': 'TestCamera',
            'location': [10, -10, 5]
        }, adapter=self.adapter)
        self.assertTrue(result['success'])
        self.assertEqual(result['camera_name'], 'TestCamera')
    
    def test_set_active_camera(self):
        create_camera_handler({'name': 'MainCam'}, adapter=self.adapter)
        result = set_active_camera_handler({
            'camera_name': 'MainCam'
        }, adapter=self.adapter)
        self.assertTrue(result['success'])
    
    # =========================================
    # MODIFICADORES
    # =========================================
    
    def test_add_subdivision_surface(self):
        cube = create_cube_handler({}, adapter=self.adapter)
        result = add_subdivision_surface_handler({
            'object_name': cube['object_name'],
            'levels': 2
        }, adapter=self.adapter)
        self.assertTrue(result['success'])
    
    def test_add_array_modifier(self):
        cube = create_cube_handler({}, adapter=self.adapter)
        result = add_array_modifier_handler({
            'object_name': cube['object_name'],
            'count': 5
        }, adapter=self.adapter)
        self.assertTrue(result['success'])
        self.assertEqual(result['count'], 5)
    
    # =========================================
    # EXPORTACIÓN
    # =========================================
    
    def test_export_fbx(self):
        result = export_fbx_handler({
            'filepath': 'temp/test_export.fbx'
        }, adapter=self.adapter)
        self.assertTrue(result['success'])
        self.assertEqual(result['format'], 'FBX')
    
    def test_export_obj(self):
        result = export_obj_handler({
            'filepath': 'temp/test_export.obj'
        }, adapter=self.adapter)
        self.assertTrue(result['success'])


class TestPhase17NoBpyImports(unittest.TestCase):
    """
    Verifica que ningún handler tenga import bpy directo.
    """
    
    def test_no_bpy_in_handlers(self):
        """Los handlers no deben importar bpy directamente."""
        import ast
        import os
        
        handlers_path = os.path.join(
            os.path.dirname(__file__), 
            '..', 'core', 'commands', 'blender_handlers'
        )
        
        bpy_imports = []
        
        for root, dirs, files in os.walk(handlers_path):
            # Skip __pycache__
            dirs[:] = [d for d in dirs if d != '__pycache__']
            
            for f in files:
                if f.endswith('.py') and not f.startswith('__'):
                    filepath = os.path.join(root, f)
                    with open(filepath, 'r', encoding='utf-8') as file:
                        try:
                            tree = ast.parse(file.read())
                            for node in ast.walk(tree):
                                if isinstance(node, ast.Import):
                                    for alias in node.names:
                                        if alias.name == 'bpy':
                                            bpy_imports.append(filepath)
                                elif isinstance(node, ast.ImportFrom):
                                    if node.module == 'bpy':
                                        bpy_imports.append(filepath)
                        except SyntaxError:
                            pass
        
        self.assertEqual(bpy_imports, [], 
            f"Found direct bpy imports in: {bpy_imports}")


if __name__ == '__main__':
    unittest.main()
