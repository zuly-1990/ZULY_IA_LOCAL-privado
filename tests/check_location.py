import bpy

print("--- CUBE LOCATION TEST ---")
try:
    print("Trying location=(0.0, 0.0, 0.0) (tuple)...")
    try:
        bpy.ops.mesh.primitive_cube_add(size=2.0, location=(0.0, 0.0, 0.0))
        print("Success with tuple location")
        bpy.ops.object.delete()
    except Exception as e:
        print(f"Failed with tuple: {e}")
        
    print("Trying location=[0.0, 0.0, 0.0] (list)...")
    try:
        bpy.ops.mesh.primitive_cube_add(size=2.0, location=[0.0, 0.0, 0.0])
        print("Success with list location")
        bpy.ops.object.delete()
    except Exception as e:
        print(f"Failed with list: {e}")
except Exception as e:
    print(f"Global error: {e}")
print("--- END ---")
