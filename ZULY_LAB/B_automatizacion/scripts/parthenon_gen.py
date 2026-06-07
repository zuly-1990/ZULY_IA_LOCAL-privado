"""
parthenon_gen.py
Generador procedural de un templo griego (Partenón simplificado).
Demuestra precisión matemática, bucles anidados y jerarquía estructural.
"""
import math

# Asegurar acceso al adapter (inyectado por run_python_script_handler)
if 'adapter' not in locals() and 'adapter' not in globals():
    raise NameError("El objeto 'adapter' no fue inyectado correctamente en el script.")

# Parámetros (inyectados o defaults)
# Intentamos obtener del scope global o local inyectado
def get_var(name, default):
    return globals().get(name, locals().get(name, default))

cols_x = get_var('cols_x', 8)  # Columnas en el frente/atrás (Octástilo)
cols_y = get_var('cols_y', 17) # Columnas en los laterales
col_spacing = get_var('spacing', 2.5)
col_height = get_var('col_height', 8.0)
col_radius = get_var('col_radius', 0.4)

# Materiales
adapter.create_material(name="MatMarmol", color=[0.95, 0.95, 0.9, 1.0], roughness=0.1, metallic=0.0)
adapter.create_material(name="MatTecho", color=[0.6, 0.3, 0.2, 1.0], roughness=0.8)

def create_column(x, y, z_base):
    name = f"Columna_{x}_{y}"
    adapter.create_primitive(
        'cylinder',
        location=[x, y, z_base + col_height/2],
        scale=[col_radius, col_radius, col_height/2],
        name=name
    )
    adapter.apply_material(name, "MatMarmol")
    return name

# 1. Crear el Estilóbato (Base de 3 niveles)
for i in range(3):
    base_w = (cols_x * col_spacing) + 2.0 - (i * 0.5)
    base_d = (cols_y * col_spacing) + 2.0 - (i * 0.5)
    name = f"Estilobato_{i}"
    adapter.create_primitive(
        'cube',
        location=[(cols_x-1)*col_spacing/2, (cols_y-1)*col_spacing/2, i*0.2],
        scale=[base_w/2, base_d/2, 0.1],
        name=name
    )
    adapter.apply_material(name, "MatMarmol")

z_floor = 0.6

# 2. Crear las Columnas (Peristilo)
for ix in range(cols_x):
    for iy in range(cols_y):
        # Solo en el perímetro
        if ix == 0 or ix == cols_x-1 or iy == 0 or iy == cols_y-1:
            create_column(ix * col_spacing, iy * col_spacing, z_floor)

# 3. Arquitrabe (Dintel perimetral)
arch_w = (cols_x - 1) * col_spacing + col_radius * 4
arch_d = (cols_y - 1) * col_spacing + col_radius * 4
z_arch = z_floor + col_height + 0.3

adapter.create_primitive(
    'cube',
    location=[(cols_x-1)*col_spacing/2, (cols_y-1)*col_spacing/2, z_arch],
    scale=[arch_w/2, arch_d/2, 0.3],
    name="Arquitrabe"
)
adapter.apply_material("Arquitrabe", "MatMarmol")

# 4. Techo a dos aguas (Frontón)
roof_height = 2.0
adapter.create_primitive(
    'cube',
    location=[(cols_x-1)*col_spacing/2, (cols_y-1)*col_spacing/2, z_arch + 0.6 + roof_height/4],
    scale=[arch_w/2, arch_d/2, 0.1], # Base del techo
    name="TechoBase"
)
adapter.apply_material("TechoBase", "MatTecho")

# Frontón (simplificado con un prisma o cubo rotado)
# En una versión real usaríamos geometría de malla, aquí simulamos con la estructura base.

print(f"Partenón Generado: {cols_x}x{cols_y} columnas.")
result = "Parthenon Generation Complete"
