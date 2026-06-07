import sys
import os
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

import bpy
from core.adapters.blender_adapter import BlenderAdapter

adapter = BlenderAdapter()

print("--- DEFINITIVE CUBE TEST ---")

def run_cube_case(name, **kwargs):
    """Helper manual (no es test pytest: el nombre evita recolección automática)."""
    print(f"Testing {name} with: {kwargs}")
    try:
        bpy.ops.mesh.primitive_cube_add(**kwargs)
        print("✓ SUCCESS")
        bpy.ops.object.delete()
    except Exception as e:
        print(f"✗ FAIL: {e}")

# Case 1: Minimal
run_cube_case("Minimal", size=2.0)

# Case 2: With location (tuple)
run_cube_case("Location (tuple)", size=2.0, location=(0, 0, 0))

# Case 3: With location (list)
run_cube_case("Location (list)", size=2.0, location=[0.0, 0.0, 0.0])

# Case 4: With scale (tuple)
run_cube_case("Scale (tuple)", size=2.0, scale=(1.0, 1.0, 1.0))

# Case 5: All (floats)
run_cube_case("All Floats", size=float(2.0), location=(0.0, 0.0, 0.0), scale=(1.0, 1.0, 1.0))

print("--- END ---")
