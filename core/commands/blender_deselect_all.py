"""
Deselecciona todos los objetos en Blender
"""

def handle(context):
    """
    Deselecciona todos los objetos
    Args:
        context: Contexto de ejecución de ZULY
    Returns:
        dict: Resultado
    """
    # Pseudo-código
    # import bpy
    # bpy.ops.object.select_all(action='DESELECT')
    return {"status": "ok", "action": "deselected_all"}
