"""
fractal_tree.py
Generador recursivo de árboles 3D.
Demuestra: Recursividad, Transformaciones Locales, Complejidad Exponencial.
"""

import math
import random

# Intentar importar mathutils si está disponible (Blender)
try:
    import mathutils
except ImportError:
    mathutils = None

# Parámetros
depth = locals().get('depth', 4)
length = locals().get('branch_len', 2.0)
angle_deg = locals().get('angle', 25.0)
angle_rad = math.radians(angle_deg)

# Materiales (Globales)
adapter.create_material(name="MatTronco", color=[0.4, 0.25, 0.1, 1.0], roughness=1.0)
adapter.create_material(name="MatHoja", color=[0.1, 0.8, 0.2, 1.0], roughness=0.5)

def create_branch(start_vec, direction_vec, length, current_depth, adapter, angle_rad, recursive_func):
    import math
    import random
    import mathutils # Asumimos contexto Blender

    if current_depth <= 0:
        # Hoja terminal
        name = f"Hoja_{random.randint(0,999999)}"
        adapter.create_primitive(
            'sphere', 
            location=[start_vec.x, start_vec.y, start_vec.z], 
            radius=length/2, 
            name=name
        )
        adapter.apply_material(name, "MatHoja")
        return

    # Calcular vector final
    end_vec = start_vec + (direction_vec * length)
    
    # Crear geometría (Cubo estirado entre start y end)
    mid_vec = (start_vec + end_vec) / 2
    
    branch_name = f"Rama_D{current_depth}_{random.randint(0,999999)}"
    
    # Usar cubos delgados como ramas
    adapter.create_primitive(
        'cube',
        location=[mid_vec.x, mid_vec.y, mid_vec.z],
        scale=[length/10, length/10, length/2], # Scale Z is half-length for cube primitive (radius mechanism)
        name=branch_name
    )
    
    # Rotar para alinear con direccion
    # direction_vec es el vector unitario
    rot_quat = direction_vec.to_track_quat('Z', 'Y')
    rot_euler = rot_quat.to_euler()
    adapter.rotate_object(branch_name, [rot_euler.x, rot_euler.y, rot_euler.z])
    
    adapter.apply_material(branch_name, "MatTronco")
    
    # Recursión
    new_len = length * 0.75
    
    # Generar nuevas direcciones rotando el vector actual
    # Rama 1
    rot_mat1 = mathutils.Matrix.Rotation(angle_rad + random.uniform(-0.1, 0.1), 4, 'X')
    rot_mat2 = mathutils.Matrix.Rotation(random.uniform(0, 6.28), 4, 'Z') # Rotacion aleatoria alrededor del eje Z global (simplificacion)
    
    # Para hacerlo bien: rotar ALREDEDOR de un eje perpendicular local.
    # Simplificacion fractal: Perturbar el vector actual.
    
    # Metodo simple: Randomizar vector y mezclar
    noise = mathutils.Vector((random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5)))
    dir1 = (direction_vec + (noise * 0.5)).normalized()
    dir2 = (direction_vec - (noise * 0.5)).normalized()

    recursive_func(end_vec, dir1, new_len, current_depth - 1, adapter, angle_rad, recursive_func)
    recursive_func(end_vec, dir2, new_len, current_depth - 1, adapter, angle_rad, recursive_func)
    
    if random.random() > 0.7:
        dir3 = (direction_vec + mathutils.Vector((0,0,1))).normalized()
        recursive_func(end_vec, dir3, new_len, current_depth - 1, adapter, angle_rad, recursive_func)


# Iniciar
start = mathutils.Vector((0, 0, 0))
direction = mathutils.Vector((0, 0, 1)) # Hacia arriba (Z)

create_branch(start, direction, length, depth, adapter, angle_rad, create_branch)

print("Árbol Fractal Matemático Generado")
