import bpy
import json
import os
import math

BLEND_OUT = '/opt/zuly/ZULY_VILLA_SAVOYE_FINAL.blend'

def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

def create_geometry_nodes_tree(name="Zuly_Savoye_Nodes"):
    tree = bpy.data.node_groups.new(name=name, type='GeometryNodeTree')
    
    # Input/Output nodes
    # For Blender 4.x compatibility we use standard interface
    out_node = tree.nodes.new('NodeGroupOutput')
    out_node.location = (800, 0)
    tree.outputs.new('NodeSocketGeometry', 'Geometry')
    
    join_node = tree.nodes.new('GeometryNodeJoinGeometry')
    join_node.location = (600, 0)
    tree.links.new(join_node.outputs[0], out_node.inputs[0])
    
    # -------------------------------------------------------------
    # 1. LOSAS (Slabs)
    # -------------------------------------------------------------
    slabs_locs = [(0, 0, 0.3), (0, 0, 3.5), (0, 0, 6.7)]
    dim_slab = (19.6, 21.6, 0.3)
    
    for i, loc in enumerate(slabs_locs):
        cube = tree.nodes.new('GeometryNodeMeshCube')
        cube.inputs['Size'].default_value = dim_slab
        cube.location = (-400, 400 - i*150)
        
        transform = tree.nodes.new('GeometryNodeTransform')
        transform.inputs['Translation'].default_value = loc
        transform.location = (-200, 400 - i*150)
        
        tree.links.new(cube.outputs['Mesh'], transform.inputs['Geometry'])
        tree.links.new(transform.outputs['Geometry'], join_node.inputs[0])

    # -------------------------------------------------------------
    # 2. PILOTES (Geometry Nodes Instance on Grid)
    # -------------------------------------------------------------
    grid = tree.nodes.new('GeometryNodeMeshGrid')
    grid.inputs['Size X'].default_value = 14.7  # 3 * 4.9m
    grid.inputs['Size Y'].default_value = 16.2  # 3 * 5.4m
    grid.inputs['Vertices X'].default_value = 4
    grid.inputs['Vertices Y'].default_value = 4
    grid.location = (-600, -200)

    cylinder = tree.nodes.new('GeometryNodeMeshCylinder')
    cylinder.inputs['Radius'].default_value = 0.15
    cylinder.inputs['Depth'].default_value = 3.5
    cylinder.location = (-600, -400)

    iop = tree.nodes.new('GeometryNodeInstanceOnPoints')
    iop.location = (-400, -200)

    tree.links.new(grid.outputs['Mesh'], iop.inputs['Points'])
    tree.links.new(cylinder.outputs['Mesh'], iop.inputs['Instance'])

    trans_pilotes = tree.nodes.new('GeometryNodeTransform')
    trans_pilotes.inputs['Translation'].default_value = (0, 0, 1.75)
    trans_pilotes.location = (-200, -200)

    tree.links.new(iop.outputs['Instances'], trans_pilotes.inputs['Geometry'])
    tree.links.new(trans_pilotes.outputs['Geometry'], join_node.inputs[0])

    # -------------------------------------------------------------
    # 3. ESCALERA HELICOIDAL PARAMÉTRICA (El Reto)
    # -------------------------------------------------------------
    # Instead of complex math nodes in python which break across Blender versions,
    # we use a Mesh Line with 35 points, and Instance On Points.
    # We create a spiral using a curve line and resample, or mathematically instance it.
    
    # Base step
    step_cube = tree.nodes.new('GeometryNodeMeshCube')
    step_cube.inputs['Size'].default_value = (0.9, 0.28, 0.04)
    step_cube.location = (-800, -800)
    
    # Offset step so center of rotation is at the edge
    step_offset = tree.nodes.new('GeometryNodeTransform')
    step_offset.inputs['Translation'].default_value = (1.8, 0, 0) # Radio 1.8m
    step_offset.location = (-600, -800)
    tree.links.new(step_cube.outputs['Mesh'], step_offset.inputs['Geometry'])

    # Line for points
    line = tree.nodes.new('GeometryNodeMeshLine')
    line.inputs['Count'].default_value = 35
    line.inputs['Offset'].default_value = (0, 0, 0.1914) # 6.7m / 35 steps
    line.location = (-800, -600)
    
    # Math for rotation (Index * 10 degrees)
    index_node = tree.nodes.new('GeometryNodeInputIndex')
    index_node.location = (-800, -1000)
    
    math_mul = tree.nodes.new('ShaderNodeMath')
    math_mul.operation = 'MULTIPLY'
    math_mul.inputs[1].default_value = math.radians(10)
    math_mul.location = (-600, -1000)
    tree.links.new(index_node.outputs['Index'], math_mul.inputs[0])
    
    combine_rot = tree.nodes.new('ShaderNodeCombineXYZ')
    combine_rot.location = (-400, -1000)
    tree.links.new(math_mul.outputs['Value'], combine_rot.inputs['Z'])
    
    # Instance
    iop_stairs = tree.nodes.new('GeometryNodeInstanceOnPoints')
    iop_stairs.location = (-200, -700)
    tree.links.new(line.outputs['Mesh'], iop_stairs.inputs['Points'])
    tree.links.new(step_offset.outputs['Geometry'], iop_stairs.inputs['Instance'])
    tree.links.new(combine_rot.outputs['Vector'], iop_stairs.inputs['Rotation'])
    
    # Move stairs to position (2.5, -2.5, 0)
    trans_stairs = tree.nodes.new('GeometryNodeTransform')
    trans_stairs.inputs['Translation'].default_value = (2.5, -2.5, 0)
    trans_stairs.location = (0, -700)
    tree.links.new(iop_stairs.outputs['Instances'], trans_stairs.inputs['Geometry'])
    
    tree.links.new(trans_stairs.outputs['Geometry'], join_node.inputs[0])

    return tree

def build_villa():
    clear_scene()
    
    mesh = bpy.data.meshes.new("Villa_Geo")
    obj = bpy.data.objects.new("Villa_Savoye_Parametrica", mesh)
    bpy.context.scene.collection.objects.link(obj)
    
    mod = obj.modifiers.new(name="Zuly_GeometryNodes", type='NODES')
    mod.node_group = create_geometry_nodes_tree()
    
    bpy.ops.wm.save_as_mainfile(filepath=BLEND_OUT)
    
    result = {
        "success": True,
        "mode": "Geometry Nodes",
        "objects_count": len(bpy.data.objects),
        "node_groups_count": len(bpy.data.node_groups)
    }
    print("ZULY_RESULT:" + json.dumps(result))

if __name__ == "__main__":
    try:
        build_villa()
    except Exception as e:
        print("ZULY_RESULT:" + json.dumps({"success": False, "error": str(e)}))
