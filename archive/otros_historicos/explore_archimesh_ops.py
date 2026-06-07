import bpy
import json

print("--- EXPLORANDO OPERADORES DE ARCHIMESH ---")

# Listar todos los operadores disponibles que contengan 'archi'
arch_ops = [op for op in dir(bpy.ops) if 'archi' in op.lower()]
print(f"Módulos de operadores encontrados: {arch_ops}")

# Si 'archimesh' existe en bpy.ops, listar sus operadores
if hasattr(bpy.ops, 'archimesh'):
    print("Operadores dentro de bpy.ops.archimesh:")
    print(dir(bpy.ops.archimesh))
else:
    print("Módulo bpy.ops.archimesh NO encontrado directamente.")

# Intentar listar vía blender operators registry
all_ops = []
for module_name in dir(bpy.ops):
    module = getattr(bpy.ops, module_name)
    for op_name in dir(module):
        full_name = f"bpy.ops.{module_name}.{op_name}"
        if 'archi' in full_name.lower():
            all_ops.append(full_name)

print("\nOperadores 'archi' en todo el registro:")
for op in all_ops:
    print(f"  - {op}")
