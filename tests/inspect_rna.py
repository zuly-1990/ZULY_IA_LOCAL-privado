import bpy
import sys

def inspect_operator(op_name):
    print(f"\n--- {op_name} ---")
    try:
        # Una forma de ver los argumentos de un operador es via bpy.ops.get_rna_type()
        # Pero es mas directo intentar llamarlo con help()
        op = eval(f"bpy.ops.{op_name}")
        
        # Obtener parametros del RNA
        rna = op.get_rna_type()
        for prop in rna.properties:
            if prop.identifier != "rna_type":
                print(f"  - {prop.identifier}: {prop.type} {prop.array_length if prop.is_array else ''}")
    except Exception as e:
        print(f"Error inspecting {op_name}: {e}")

inspect_operator("mesh.primitive_cube_add")
inspect_operator("mesh.primitive_uv_sphere_add")
inspect_operator("mesh.primitive_cylinder_add")
print("\n--- END ---")
