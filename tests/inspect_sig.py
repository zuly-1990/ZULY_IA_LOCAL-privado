import bpy
import inspect

print("--- OPERATOR SIGNATURE INSPECTION ---")
try:
    op = bpy.ops.mesh.primitive_cube_add
    print(f"Type: {type(op)}")
    # Blender operators are weird, sometimes they don't support inspect
    try:
        sig = inspect.signature(op)
        print(f"Signature: {sig}")
    except Exception as e:
        print(f"Inspect Signature failed: {e}")
        
    # Standard Blender way: rna_type
    print("RNA Properties:")
    for prop in op.get_rna_type().properties:
        if prop.identifier != "rna_type":
            print(f"  - {prop.identifier}: {prop.type} ({prop.subtype})")
            
except Exception as e:
    print(f"Global error: {e}")
print("--- END ---")
