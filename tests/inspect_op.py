import bpy
import inspect

print("--- OPERATOR SIGNATURE ---")
try:
    # Obtener el operador
    op = bpy.ops.mesh.primitive_cube_add
    print(f"Operator: {op}")
    # En Blender, los operadores no son funciones normales, pero podemos ver sus propiedades
    # Una forma de ver los argumentos es via help()
    import io
    from contextlib import redirect_stdout
    f = io.StringIO()
    with redirect_stdout(f):
        help(op)
    print(f.getvalue())
except Exception as e:
    print(f"Error: {e}")
print("--- END SIGNATURE ---")
