import bpy

print("--- CUBE TEST ---")
try:
    print("Trying size=2.0 (float)...")
    try:
        bpy.ops.mesh.primitive_cube_add(size=2.0)
        print("Success with float size")
        bpy.ops.object.delete()
    except Exception as e:
        print(f"Failed with float: {e}")
        
    print("Trying size=(2.0, 2.0, 2.0) (sequence)...")
    try:
        bpy.ops.mesh.primitive_cube_add(size=(2.0, 2.0, 2.0))
        print("Success with sequence size")
        bpy.ops.object.delete()
    except Exception as e:
        print(f"Failed with sequence: {e}")

except Exception as e:
    print(f"Global error: {e}")
print("--- END ---")
