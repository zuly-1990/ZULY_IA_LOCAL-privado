import bpy
import json
import os

JSON_PATH = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\zuly_uav_map.json"
GROSOR_LINEA = 0.5 # Metros (Ajustar segun la escala del dron)

def limpiar_escena():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

def hex_to_rgba(hex_code):
    hex_code = hex_code.lstrip('#')
    return tuple(int(hex_code[i:i+2], 16)/255.0 for i in (0, 2, 4)) + (1.0,)

def main():
    if not os.path.exists(JSON_PATH):
        print(f"ERROR: No se encontro {JSON_PATH}")
        return
        
    print("Limpiando escena...")
    limpiar_escena()
    
    with open(JSON_PATH, 'r') as f:
        data = json.load(f)
        
    palette = data.get("palette", {})
    nodes = data.get("nodes", [])
    edges = data.get("edges", [])
    
    print(f"Construyendo Topografia: {len(nodes)} Nodos, {len(edges)} Lineas Estructurales")
    
    # Crear Objeto Curva
    curve_data = bpy.data.curves.new('Zuly_UAV_Map_Curve', type='CURVE')
    curve_data.dimensions = '3D'
    curve_data.bevel_depth = GROSOR_LINEA
    
    curve_obj = bpy.data.objects.new('Zuly_UAV_Map', curve_data)
    bpy.context.collection.objects.link(curve_obj)
    
    # Crear y asignar Materiales
    mat_indices = {} # Mapea "0" (str) al indice del slot de material en Blender
    
    for color_id_str, hex_code in palette.items():
        mat = bpy.data.materials.new(name=f"Material_Color_{color_id_str}")
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            # Blender Emission para que brille un poco como wireframe
            bsdf.inputs['Base Color'].default_value = hex_to_rgba(hex_code)
            bsdf.inputs['Emission'].default_value = hex_to_rgba(hex_code)
            bsdf.inputs['Emission Strength'].default_value = 2.0
            
        curve_obj.data.materials.append(mat)
        mat_indices[color_id_str] = len(curve_obj.data.materials) - 1
        
    # Crear lineas
    # En Blender, una Curva puede tener muchos "Splines". Cada Spline sera una arista.
    for edge in edges:
        n1_idx, n2_idx, color_idx = edge
        
        # En el JSON, color_idx puede guardarse como int o str dependiendo de json.dump
        color_idx_str = str(color_idx)
        
        x1, y1, z1 = nodes[n1_idx]
        x2, y2, z2 = nodes[n2_idx]
        
        spline = curve_data.splines.new(type='POLY')
        spline.points.add(1) # Un POLY spline nuevo ya trae 1 punto, sumamos 1 mas para tener 2
        
        spline.points[0].co = (x1, y1, z1, 1.0)
        spline.points[1].co = (x2, y2, z2, 1.0)
        
        if color_idx_str in mat_indices:
            spline.material_index = mat_indices[color_idx_str]
            
    print("Reconstruccion espacial finalizada!")

if __name__ == "__main__":
    main()
