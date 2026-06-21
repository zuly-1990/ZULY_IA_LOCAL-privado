def wrap_prompt_with_geometry_nodes_constraint(user_prompt: str) -> str:
    """
    Pilar 1: Transición a Geometry Nodes
    Envuelve la petición del usuario con un meta-prompt estricto para obligar
    a DeepSeek a generar árboles de nodos geométricos en lugar de geometría destructiva.
    """
    system_constraint = """
[CRITICAL SYSTEM CONSTRAINT - ZULY V2 ARCHITECTURE]
You are writing a Blender Python script (`bpy`) for Blender 3.6.
YOU ARE STRICTLY FORBIDDEN FROM USING DESTRUCTIVE MODELING (e.g. bpy.ops.mesh.primitive_cube_add, bmesh, etc).
ALL GEOMETRY MUST BE GENERATED PROCEDURALLY USING GEOMETRY NODES.

Rules:
1. Create a base object (e.g. a simple plane or cube) and add a 'GeometryNodes' modifier to it.
2. Build a node tree programmatically using `modifier.node_group.nodes.new()`.
3. Use nodes like 'GeometryNodeMeshGrid', 'GeometryNodeExtrudeMesh', 'GeometryNodeInstanceOnPoints', etc.
4. Link the nodes correctly from the Group Input to the Group Output.
5. The result must be a fully procedural and parametric object.
6. Provide ONLY valid python code, no markdown or explanations.

USER REQUEST:
"""
    return f"{system_constraint}\n{user_prompt}"
