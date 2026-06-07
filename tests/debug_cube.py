import bpy
import sys

print("--- DIAGNOSTIC CUBE ---")
try:
    print("Attempting to create cube...")
    res = bpy.ops.mesh.primitive_cube_add(size=2.0, location=(0,0,0), scale=(1,1,1))
    print(f"Result: {res}")
    print(f"Active object: {bpy.context.active_object.name}")
except Exception as e:
    import traceback
    print(f"ERROR: {e}")
    traceback.print_exc()
print("--- END DIAGNOSTIC ---")
