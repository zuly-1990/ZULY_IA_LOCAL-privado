"""
city_generator_v1.py
Script procedural para generar una ciudad simple usando cubos.
Se ejecuta dentro del contexto de Blender vía ZULY.
"""

import random

# Variables inyectadas desde YAML o defaults
grid_size = locals().get('grid_size', 5)
block_size = locals().get('block_size', 2.0)
max_height = locals().get('max_height', 5.0)

# Asegurar materiales
adapter.create_material(name="MatEdificio", color=[0.3, 0.3, 0.35, 1.0], roughness=0.2)
adapter.create_material(name="MatVentanas", color=[0.9, 0.9, 0.5, 1.0], emission_strength=5.0)
adapter.create_material(name="MatSueloCiudad", color=[0.1, 0.1, 0.1, 1.0])

# Crear suelo base
suelo_scale = grid_size * block_size
adapter.create_primitive(
    'plane',
    location=[(suelo_scale/2)-block_size/2, (suelo_scale/2)-block_size/2, 0], 
    scale=suelo_scale/2, 
    name="SueloBase"
)
adapter.apply_material("SueloBase", "MatSueloCiudad")

# Generar edificios
for x in range(grid_size):
    for y in range(grid_size):
        # Probabilidad de parque (hueco)
        if random.random() < 0.2:
            continue
            
        height = random.uniform(1.0, max_height)
        
        # Posición
        pos_x = x * block_size
        pos_y = y * block_size
        pos_z = height / 2.0
        
        name = f"Edificio_{x}_{y}"
        
        # Crear estructura
        adapter.create_primitive(
            'cube',
            location=[pos_x, pos_y, pos_z],
            scale=[block_size * 0.4, block_size * 0.4, height/2], # Scale en Z es half-size
            name=name
        )
        adapter.apply_material(name, "MatEdificio")
        
        # Detalles simples (antena o caja arriba)
        if random.random() > 0.7:
             adapter.create_primitive(
                'cube',
                location=[pos_x, pos_y, height + 0.25],
                scale=[0.2, 0.2, 0.25],
                name=f"Detalle_{x}_{y}"
            )

print(f"Ciudad generada: {grid_size}x{grid_size}")
result = "City Generation Complete"
