import bpy
import bmesh
import math
import re
from mathutils import Vector, Euler
from typing import Optional, List, Dict, Tuple

# ---------------------------------------------------------------------------
# CONFIGURACIÓN INICIAL
# ---------------------------------------------------------------------------
SCALE = 1.0  # 1 Blender unit = 1 meter
LAT_CENTER = 41.3870
LON_CENTER = 2.1700
HEIGHT = 1.5  # Cámara a 1.5m del suelo

# Limpiar escena
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Eliminar todos los materiales (opcional, por seguridad)
for material in bpy.data.materials:
    bpy.data.materials.remove(material)

# ---------------------------------------------------------------------------
# FUNCIONES AUXILIARES
# ---------------------------------------------------------------------------
def geo_to_xy(lat: float, lon: float,
              lat_center: float, lon_center: float) -> Tuple[float, float]:
    """Convierte coordenadas geográficas (lat, lon) a (x, y) en metros (proyección equidistante simple)"""
    R = 6371000  # Radio de la Tierra en metros
    dlat = math.radians(lat - lat_center)
    dlon = math.radians(lon - lon_center)
    midlat = math.radians((lat + lat_center) / 2.0)
    x = R * dlon * math.cos(midlat)
    y = R * dlat
    return x, y

def parse_osm_xml(filepath: str) -> Dict:
    """Parseador simple de OSM XML a diccionario con nodos y ways"""
    import xml.etree.ElementTree as ET
    tree = ET.parse(filepath)
    root = tree.getroot()
    nodes = {}
    ways = []
    for child in root:
        if child.tag == 'node':
            lat = float(child.attrib['lat'])
            lon = float(child.attrib['lon'])
            uid = int(child.attrib['id'])
            x, y = geo_to_xy(lat, lon, LAT_CENTER, LON_CENTER)
            nodes[uid] = (x, y)
        elif child.tag == 'way':
            way = {'id': int(child.attrib['id']), 'nodes': [], 'tags': {}}
            for sub in child:
                if sub.tag == 'nd':
                    way['nodes'].append(int(sub.attrib['ref']))
                elif sub.tag == 'tag':
                    way['tags'][sub.attrib['k']] = sub.attrib['v']
            ways.append(way)
    return {'nodes': nodes, 'ways': ways}

def get_building_height(tags: Dict) -> float:
    """Obtiene altura de un edificio desde las tags OSM, por defecto 10m"""
    height = tags.get('height', '10')
    levels = tags.get('building:levels', None)
    # Intentar parsear height
    match = re.search(r'(\d+\.?\d*)', height)
    if match:
        return float(match.group(1))
    # Si no, usar levels * 3m
    if levels:
        try:
            return float(levels) * 3.0
        except ValueError:
            return 10.0
    return 10.0

def is_building_way(tags: Dict) -> bool:
    """Determina si un way representa un edificio"""
    building = tags.get('building', None)
    if building and building not in ('no', 'construction', 'ruins'):
        return True
    if 'building:part' in tags:
        return True
    return False

def create_building(way_data: Dict, nodes_dict: Dict):
    """Crea un edificio 3D a partir de un way OSM"""
    node_ids = way_data['nodes']
    tags = way_data['tags']
    if len(node_ids) < 3:
        return

    coords = [nodes_dict.get(uid) for uid in node_ids]
    if None in coords:
        return

    # Cerrar polígono si no está cerrado
    if coords[0] != coords[-1]:
        coords.append(coords[0])

    # Crear malla bidimensional (suelo)
    vertices_2d = [(x, y, 0) for x, y in coords]
    edges = [(i, i+1) for i in range(len(vertices_2d)-1)]
    faces = [list(range(len(vertices_2d)-1))]
    # Asegurar que la cara esté bien orientada (sentido antihorario)
    # Calculamos el área 2D para determinar orientación
    area_2d = 0
    n = len(vertices_2d)-1  # ignoramos el último (duplicado)
    for i in range(n):
        x1, y1, _ = vertices_2d[i]
        x2, y2, _ = vertices_2d[(i+1)%n]
        area_2d += x1*y2 - x2*y1
    if area_2d < 0:
        faces[0] = list(reversed(faces[0]))

    # Crear mesh del suelo
    mesh_ground = bpy.data.meshes.new(name="GroundTemp")
    mesh_ground.from_pydata(vertices_2d, edges, faces)
    mesh_ground.update()

    # Crear objeto suelo
    obj_ground = bpy.data.objects.new("GroundTemp", mesh_ground)
    bpy.context.collection.objects.link(obj_ground)

    # Extruir verticalmente con el modificador Solidify
    height = get_building_height(tags)
    # Si la altura es 0, no creamos edificio
    if height <= 0:
        bpy.data.objects.remove(obj_ground, do_unlink=True)
        return

    solidify = obj_ground.modifiers.new(name="Solidify", type='SOLIDIFY')
    solidify.thickness = height
    solidify.offset = 1.0  # Hacia arriba (positivo Z)
    solidify.use_even_offset = True

    # Aplicar el modificador para tener geometría real
    bpy.context.view_layer.objects.active = obj_ground
    bpy.ops.object.modifier_apply(modifier="Solidify")

    # Renombrar
    building_name = f"Building_{way_data['id']}"
    obj_ground.name = building_name
    mesh_ground.name = building_name

    # Material base (gris claro)
    mat = bpy.data.materials.new(name=f"Mat_{building_name}")
    mat.use_nodes = True
    nodes_mat = mat.node_tree.nodes
    bsdf = nodes_mat.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (0.7, 0.7, 0.7, 1.0)
        bsdf.inputs['Roughness'].default_value = 0.8
    obj_ground.data.materials.append(mat)

    return obj_ground

def create_ground_plane(x_min, x_max, y_min, y_max):
    """Crea un plano base para el terreno"""
    bpy.ops.mesh.primitive_plane_add(size=max(x_max-x_min, y_max-y_min),
                                      location=((x_min+x_max)/2, (y_min+y_max)/2, 0))
    plane = bpy.context.active_object
    plane.name = "Terrain"
    # Material color tierra
    mat = bpy.data.materials.new(name="GroundMat")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (0.3, 0.6, 0.2, 1.0)
    plane.data.materials.append(mat)
    return plane

def setup_camera(bbox):
    """Configura cámara cenital a 50m de altura, orientada hacia abajo"""
    cx = (bbox[0] + bbox[2]) / 2
    cy = (bbox[1] + bbox[3]) / 2
    bpy.ops.object.camera_add(location=(cx, cy, 50))
    cam = bpy.context.active_object
    cam.name = "CamTop"
    cam.rotation_euler = (0, 0, 0)  # Apunta hacia -Z por defecto
    # Forzar rotación para que mire hacia abajo (local -Z)
    cam.rotation_euler = (0, 0, 0)
    # Apuntar exactamente hacia abajo
    # Usamos constraint para fijar
    constraint = cam.constraints.new(type='TRACK_TO')
    constraint.target = None
    constraint.track_axis = 'TRACK_NEGATIVE_Z'
    constraint.up_axis = 'UP_Y'
    # Crear Empty como objetivo
    bpy.ops.object.empty_add(location=(cx, cy, 0))
    target = bpy.context.active_object
    target.name = "CamTarget"
    constraint.target = target
    # Ajustar cámara
    cam.data.type = 'PERSP'
    cam.data.lens = 35  # Gran angular para captar más
    cam.data.clip_end = 200
    return cam

def add_sun_light():
    """Añade iluminación solar"""
    bpy.ops.object.light_add(type='SUN', location=(50, 50, 100))
    sun = bpy.context.active_object
    sun.name = "SunLight"
    sun.data.energy = 3
    sun.rotation_euler = (math.radians(45), 0, math.radians(45))
    return sun

# ---------------------------------------------------------------------------
# CARGA DE DATOS OSM
# ---------------------------------------------------------------------------
# Nota: el archivo OSM debe existir. Si no, se genera un escenario de demostración.
import os
osm_file = "barcelona.osm"
if os.path.exists(osm_file):
    data = parse_osm_xml(osm_file)
    nodes = data['nodes']
    ways = data['ways']
else:
    # Crear datos de demostración (un cuadrado y un rectángulo)
    print("OSM no encontrado, generando datos demo.")
    nodes = {
        1: (0, 0), 2: (20, 0), 3: (20, 20), 4: (0, 20),
        5: (30, 0), 6: (50, 0), 7: (50, 15), 8: (30, 15),
    }
    ways = [
        {'id': 100, 'nodes': [1,2,3,4,1], 'tags': {'building':'yes', 'height':'12'}},
        {'id': 101, 'nodes': [5,6,7,8,5], 'tags': {'building':'yes', 'levels':'5'}},
    ]

# ---------------------------------------------------------------------------
# CREACIÓN DE EDIFICIOS
# ---------------------------------------------------------------------------
all_x = []
all_y = []
buildings_objects = []

for way in ways:
    if is_building_way(way['tags']):
        obj = create_building(way, nodes)
        if obj:
            build_verts = obj.data.vertices
            for v in build_verts:
                all_x.append(v.co.x)
                all_y.append(v.co.y)
            buildings_objects.append(obj)

# Si no hay edificios, crear un plano de demostración
if not buildings_objects:
    # Crear un cubo de demostración
    bpy.ops.mesh.primitive_cube_add(size=10, location=(0,0,5))
    cube = bpy.context.active_object
    cube.name = "DemoBuilding"
    mat = bpy.data.materials.new(name="DemoMat")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (0.6, 0.4, 0.2, 1.0)
    cube.data.materials.append(mat)
    all_x = [-5, 5]
    all_y = [-5, 5]

# ---------------------------------------------------------------------------
# TERRENO Y CÁMARA
# ---------------------------------------------------------------------------
# Calcular bounding box
x_min = min(all_x) - 10
x_max = max(all_x) + 10
y_min = min(all_y) - 10
y_max = max(all_y) + 10

ground = create_ground_plane(x_min, x_max, y_min, y_max)
camera = setup_camera((x_min, x_max, y_min, y_max))
sun = add_sun_light()

# ---------------------------------------------------------------------------
# CONFIGURACIÓN FINAL
# ---------------------------------------------------------------------------
# Ajustar resolución de render (para visibilidad)
bpy.context.scene.render.resolution_x = 1920
bpy.context.scene.render.resolution_y = 1080
bpy.context.scene.render.engine = 'EEVEE'
bpy.context.scene.eevee.taa_render_samples = 64

# Forzar evaluación visual: reemplazar error de Gemini por configuración correcta
print("Render configurado. Cámara cenital a 50m, luz solar, edificios creados.")
print("Puedes renderizar con F12 o establecer animación si lo deseas.")