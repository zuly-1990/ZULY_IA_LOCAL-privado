"""
Selecciona todos los objetos de un tipo (MESH, LIGHT, etc.) en Blender
"""

def handle(context, type_name):
    """
    Selecciona todos los objetos de un tipo
    Args:
        context: Contexto de ejecución de ZULY
        type_name (str): Tipo de objeto ("MESH", "LIGHT", etc.)
    Returns:
        dict: Resultado
    """
    # Pseudo-código para integración con bpy
    # import bpy
    # bpy.ops.object.select_all(action='DESELECT')
    # for obj in bpy.data.objects:
    #     if obj.type == type_name:
    #         obj.select_set(True)
    return {"status": "ok", "selected_type": type_name}
