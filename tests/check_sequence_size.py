import bpy

print("--- CUBE SEQUENCE SIZE TEST ---")
try:
    print("Trying size=(2.0, 2.0, 2.0)...")
    try:
        bpy.ops.mesh.primitive_cube_add(size=(2.0, 2.0, 2.0))
        print("Success with sequence size!")
        bpy.ops.object.delete()
    except Exception as e:
        print(f"Failed with sequence size: {e}")
except Exception as e:
    print(f"Global error: {e}")
print("--- END ---")
