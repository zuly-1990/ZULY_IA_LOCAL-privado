
import sys
from unittest.mock import MagicMock

# This module is automatically imported by pytest.
# We check if 'bpy' is available; if not, we mock it globally.
# This ensures that tests can run in environments without Blender.

try:
    import bpy
except ImportError:
    # bpy is not available, so we create a comprehensive mock.
    bpy = MagicMock()
    
    # Mock bpy.data.objects
    bpy.data.objects = []
    
    # Mock bpy.context for typical access patterns if needed
    bpy.context = MagicMock()
    
    # Inject the mock into sys.modules so subsequent imports of 'import bpy' work.
    sys.modules['bpy'] = bpy
    
    # Also ensure that 'bpy.types' and other common submodules are accessible via the mock
    # (MagicMock handles attribute access automatically, but explicit injection helps some linters/importers)
