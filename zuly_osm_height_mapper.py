import urllib.request
import urllib.parse
import json
import math
import os

# Configuracion
# Bounding Box: Manhattan Financial District (Wall St)
LAT_MIN, LON_MIN = 40.706, -74.012
LAT_MAX, LON_MAX = 40.710, -74.005

# Calculo de centro para proyeccion local
CENTER_LAT = (LAT_MIN + LAT_MAX) / 2
CENTER_LON = (LON_MIN + LON_MAX) / 2
EARTH_RADIUS = 6378137.0 # metros

# Paleta de colores para el Drone Map
PALETTE = {
    "0": "#333333", # Calles (Gris Oscuro)
    "1": "#B0BEC5", # Muros de Edificios (Gris Claro)
    "2": "#FFFFFF", # Techos (Blanco)
    "3": "#4CAF50"  # Parques/Zonas Verdes
}

def latlon_to_xy(lat, lon):
    # Proyeccion simple (Equirectangular approximation) a metros desde el centro
    dx = (lon - CENTER_LON) * (math.pi / 180) * EARTH_RADIUS * math.cos(CENTER_LAT * math.pi / 180)
    dy = (lat - CENTER_LAT) * (math.pi / 180) * EARTH_RADIUS
    return dx, dy

def build_overpass_query():
    # Buscamos edificios y calles (highways)
    query = f"""
    [out:json][timeout:25];
    (
      way["building"]({LAT_MIN},{LON_MIN},{LAT_MAX},{LON_MAX});
      way["highway"]({LAT_MIN},{LON_MIN},{LAT_MAX},{LON_MAX});
      way["leisure"="park"]({LAT_MIN},{LON_MIN},{LAT_MAX},{LON_MAX});
    );
    out body;
    >;
    out skel qt;
    """
    return query

def parse_osm_data(data):
    # Mapas intermedios
    osm_nodes = {} # node_id -> (lat, lon)
    ways = [] # list of ways dict
    
    for element in data['elements']:
        if element['type'] == 'node':
            osm_nodes[element['id']] = (element['lat'], element['lon'])
        elif element['type'] == 'way':
            ways.append(element)
            
    # Zuly Map Struct
    zuly_nodes = [] # [x, y, z]
    zuly_edges = [] # [id1, id2, color_idx]
    
    # Para evitar nodos duplicados en la misma coordenada exacta (compresion)
    coord_to_idx = {}
    
    def get_or_create_node(x, y, z):
        # Redondear a 2 decimales (centimetros) para evitar flotantes largos en el JSON
        x = round(x, 2)
        y = round(y, 2)
        z = round(z, 2)
        key = f"{x}_{y}_{z}"
        if key not in coord_to_idx:
            coord_to_idx[key] = len(zuly_nodes)
            zuly_nodes.append([x, y, z])
        return coord_to_idx[key]

    for way in ways:
        nodes_in_way = way.get('nodes', [])
        if len(nodes_in_way) < 2: continue
        
        tags = way.get('tags', {})
        
        if 'highway' in tags:
            # Calle (Z = 0)
            color = "0"
            for i in range(len(nodes_in_way) - 1):
                n1 = osm_nodes.get(nodes_in_way[i])
                n2 = osm_nodes.get(nodes_in_way[i+1])
                if not n1 or not n2: continue
                
                x1, y1 = latlon_to_xy(n1[0], n1[1])
                x2, y2 = latlon_to_xy(n2[0], n2[1])
                
                idx1 = get_or_create_node(x1, y1, 0)
                idx2 = get_or_create_node(x2, y2, 0)
                zuly_edges.append([idx1, idx2, int(color)])
                
        elif 'building' in tags:
            # Edificio (Z base = 0, Z techo = height)
            # Calcular altura
            height = 10.0 # Altura por defecto si no hay datos
            if 'height' in tags:
                try:
                    h_str = tags['height'].replace('m', '').strip()
                    height = float(h_str)
                except:
                    pass
            elif 'building:levels' in tags:
                try:
                    height = float(tags['building:levels']) * 3.0 # Asumir 3m por piso
                except:
                    pass
            
            # Crear huella en el piso, huella en el techo, y muros verticales
            for i in range(len(nodes_in_way) - 1):
                n1 = osm_nodes.get(nodes_in_way[i])
                n2 = osm_nodes.get(nodes_in_way[i+1])
                if not n1 or not n2: continue
                
                x1, y1 = latlon_to_xy(n1[0], n1[1])
                x2, y2 = latlon_to_xy(n2[0], n2[1])
                
                # Nodos base
                b1 = get_or_create_node(x1, y1, 0)
                b2 = get_or_create_node(x2, y2, 0)
                # Arista base (Muro)
                zuly_edges.append([b1, b2, 1])
                
                # Nodos techo
                t1 = get_or_create_node(x1, y1, height)
                t2 = get_or_create_node(x2, y2, height)
                # Arista techo
                zuly_edges.append([t1, t2, 2])
                
                # Arista vertical (conecta base con techo)
                zuly_edges.append([b1, t1, 1])
                
        elif 'leisure' in tags and tags['leisure'] == 'park':
            # Parques (Z = 0)
            color = "3"
            for i in range(len(nodes_in_way) - 1):
                n1 = osm_nodes.get(nodes_in_way[i])
                n2 = osm_nodes.get(nodes_in_way[i+1])
                if not n1 or not n2: continue
                
                x1, y1 = latlon_to_xy(n1[0], n1[1])
                x2, y2 = latlon_to_xy(n2[0], n2[1])
                
                idx1 = get_or_create_node(x1, y1, 0)
                idx2 = get_or_create_node(x2, y2, 0)
                zuly_edges.append([idx1, idx2, int(color)])

    return zuly_nodes, zuly_edges

def main():
    print("Iniciando Mapeo Topografico Real via Overpass API (OpenStreetMap)...")
    query = build_overpass_query()
    
    url = "https://overpass-api.de/api/interpreter"
    data = urllib.parse.urlencode({'data': query}).encode('utf-8')
    
    print("Descargando geometria de satelite (Manhattan Financial District)...")
    try:
        headers = {'User-Agent': 'ZulyDroneMapper/1.0'}
        req = urllib.request.Request(url, data=data, headers=headers)
        with urllib.request.urlopen(req) as response:
            osm_json = json.loads(response.read().decode('utf-8'))
    except Exception as e:
        print(f"Error conectando a OSM: {e}")
        return
        
    print(f"Datos descargados. Parseando {len(osm_json.get('elements', []))} elementos...")
    nodes, edges = parse_osm_data(osm_json)
    
    print(f"Geometria 3D generada: {len(nodes)} Nodos espaciales, {len(edges)} Aristas vectoriales.")
    
    out_path = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\zuly_uav_map.json"
    
    # Exportar
    output_data = {
        "palette": PALETTE,
        "nodes": nodes,
        "edges": edges
    }
    
    with open(out_path, 'w') as f:
        # Usamos compresion maxima en JSON
        json.dump(output_data, f, separators=(',', ':'))
        
    size_kb = os.path.getsize(out_path) / 1024
    print(f"¡Mapa compilado exitosamente en {out_path}!")
    print(f"PESO DEL MAPA 3D (Z-AXIS COMPLETO): {size_kb:.2f} KB")

if __name__ == "__main__":
    main()
