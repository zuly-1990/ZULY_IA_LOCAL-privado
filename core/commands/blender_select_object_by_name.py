"""
Selecciona uno o más objetos por su nombre en Blender
"""

def handle(context, name):
    """
    Selecciona objetos por nombre
    Args:
        context: Contexto de ejecución de ZULY
        name (str or list): Nombre(s) de objeto(s) a seleccionar
    Returns:
        dict: Resultado
    """
    # Ejemplo de integración con bpy (pseudo-código)
    # import bpy
    # if isinstance(name, str):
    #     bpy.ops.object.select_all(action='DESELECT')
    #     bpy.data.objects[name].select_set(True)
    # elif isinstance(name, list):
    #     bpy.ops.object.select_all(action='DESELECT')
    #     for n in name:
    #         bpy.data.objects[n].select_set(True)
    return {"status": "ok", "selected": name}
