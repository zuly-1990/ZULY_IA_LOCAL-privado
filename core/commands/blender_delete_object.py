"""
Borra el objeto seleccionado o por nombre en Blender
"""

def handle(context, name=None):
    """
    Borra objeto(s) por nombre o selección
    Args:
        context: Contexto de ejecución de ZULY
        name (str or list, optional): Nombre(s) de objeto(s) a borrar
    Returns:
        dict: Resultado
    """
    # Pseudo-código
    # import bpy
    # if name:
    #     for n in ([name] if isinstance(name, str) else name):
    #         bpy.data.objects.remove(bpy.data.objects[n], do_unlink=True)
    # else:
    #     bpy.ops.object.delete()
    return {"status": "ok", "deleted": name or "selected"}
