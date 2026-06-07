# blender_commands.py
"""
Recibe diccionario del diálogo y traduce a acciones Blender.
"""

def execute_blender_action(params):
    """Ejecuta acción en Blender según parámetros."""
    print(f"Acción: Crear {params['object']} | Color: {params['color']} | Tamaño: {params['size']} | Cantidad: {params['count']}")
    # Simulación de advertencias
    if hasattr(params, 'advertencias') and params['advertencias']:
        for adv in params['advertencias']:
            print(f"Advertencia: {adv}")
