import sys
import os
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.adapters.blender_adapter import BlenderAdapter
import bpy

print("--- DIRECT ADAPTER TEST ---")
adapter = BlenderAdapter()
if not adapter.is_available():
    print("Adapter NOT available")
    exit(1)

# Limpiar
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

print("Calling create_primitive('cube', name='Cubo_Test')...")
result = adapter.create_primitive('cube', name='Cubo_Test')
print(f"Result: {result}")

if not result['success']:
    print(f"Error Message: {result.get('error')}")

print("--- END ---")
