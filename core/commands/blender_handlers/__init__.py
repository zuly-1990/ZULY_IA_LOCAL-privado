"""
blender_handlers/__init__.py

Handlers funcionales para comandos Blender.
Estos handlers se registran en IntentRouter y ejecutan acciones reales.
"""

from .primitives import (
    create_cube_handler,
    create_sphere_handler,
    create_cylinder_handler,
    create_plane_handler,
    create_cone_handler,
)
from .transforms import (
    move_object_handler,
    rotate_object_handler,
    scale_object_handler,
)
from .render import render_scene_handler
from .system import get_system_info_handler, save_blend_handler
from .selection import (
    delete_object_handler,
    duplicate_object_handler,
    select_object_handler,
    deselect_all_handler,
    select_all_by_type_handler,
)

__all__ = [
    'create_cube_handler',
    'create_sphere_handler',
    'create_cylinder_handler',
    'create_plane_handler',
    'create_cone_handler',
    'move_object_handler',
    'rotate_object_handler',
    'scale_object_handler',
    'render_scene_handler',
    'get_system_info_handler',
    'save_blend_handler',
    'delete_object_handler',
    'duplicate_object_handler',
    'select_object_handler',
    'deselect_all_handler',
    'select_all_by_type_handler',
]

