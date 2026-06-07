import bpy
print("--- CUBE SCALE TEST ---")
try:
    print("Trying scale=(1.0, 1.0, 1.0)...")
    try:
        bpy.ops.mesh.primitive_cube_add(size=2.0, scale=(1.0, 1.0, 1.0))
        print("Success with tuple scale")
        bpy.ops.object.delete()
    except Exception as e:
        print(f"Failed with tuple scale: {e}")
        
    print("Trying scale=1.0 (float)...")
    try:
        bpy.ops.mesh.primitive_cube_add(size=2.0, scale=1.0)
        print("Success with float scale")
        bpy.ops.object.delete()
    except Exception as e:
        print(f"Failed with float scale: {e}")
except Exception as e:
    print(f"Global error: {e}")
print("--- END ---")
