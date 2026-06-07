import sys; sys.path.insert(0, '.')
from core.commands.blender_handlers.architectural import crear_muro_handler, crear_habitacion_handler, listar_patrones_handler
from core.adapters import get_engine_adapter

a = get_engine_adapter(force_mock=True)

r = crear_muro_handler({'ancho': 3.0, 'alto': 2.5, 'grosor': 0.2}, a)
print(f"Muro: {r['success']} - {r['message']}")

r2 = crear_habitacion_handler({'ancho': 4.0, 'profundidad': 5.0, 'altura': 2.5}, a)
print(f"Habitacion: {r2['success']} - {r2['message']}")

r3 = listar_patrones_handler({})
print(f"Patrones: {r3['message']}")
