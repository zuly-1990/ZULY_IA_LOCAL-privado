"""
Renombra un objeto existente en Blender
"""

def handle(context, old_name, new_name):
    """
    Renombra un objeto
    Args:
        context: Contexto de ejecución de ZULY
        old_name (str): Nombre actual
        new_name (str): Nuevo nombre
    Returns:
        dict: Resultado
    """
    # Pseudo-código
    # import bpy
    # bpy.data.objects[old_name].name = new_name
    return {"status": "ok", "renamed": {"from": old_name, "to": new_name}}
