"""
Handlers avanzados para LYZU
"""

from .materials import (
    create_material_handler,
    create_texture_material_handler,
    apply_material_handler,
    set_material_color_handler
)

from .lights import (
    create_light_handler,
    set_light_energy_handler,
    set_light_color_handler
)

from .cameras import (
    create_camera_handler,
    set_active_camera_handler,
    position_camera_handler
)

from .modifiers import (
    add_subdivision_surface_handler,
    add_array_modifier_handler,
    add_bevel_modifier_handler,
    add_boolean_modifier_handler,
    apply_modifier_handler,
    add_weighted_normal_handler,
)

from .export import (
    export_fbx_handler,
    export_obj_handler,
    export_gltf_handler
)

from .validation_handlers import validate_topology_handler
from .lab_handlers import scan_and_learn_handler

__all__ = [
    'create_material_handler',
    'create_texture_material_handler',
    'apply_material_handler',
    'set_material_color_handler',
    'create_light_handler',
    'set_light_energy_handler',
    'set_light_color_handler',
    'create_camera_handler',
    'set_active_camera_handler',
    'position_camera_handler',
    'add_subdivision_surface_handler',
    'add_array_modifier_handler',
    'add_bevel_modifier_handler',
    'add_boolean_modifier_handler',
    'apply_modifier_handler',
    'add_weighted_normal_handler',
    'export_fbx_handler',
    'export_obj_handler',
    'export_gltf_handler',
    'validate_topology_handler',
    'scan_and_learn_handler',
]
