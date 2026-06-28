import json
import math
import os

def create_circle(cx, cy, cz, radius, segments, color_idx):
    nodes = []
    edges = []
    for i in range(segments):
        angle = 2 * math.pi * i / segments
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)
        nodes.append([round(x,2), round(y,2), round(cz,2)])
        
    for i in range(segments):
        nxt = (i + 1) % segments
        edges.append([i, nxt, color_idx])
    return nodes, edges

def create_extruded_polygon(cx, cy, radius, segments, height, color_wall, color_roof):
    # Base
    b_nodes, b_edges = create_circle(cx, cy, 0, radius, segments, color_wall)
    # Roof
    t_nodes, t_edges = create_circle(cx, cy, height, radius, segments, color_roof)
    
    nodes = b_nodes + t_nodes
    edges = b_edges
    
    offset = len(b_nodes)
    for e in t_edges:
        edges.append([e[0] + offset, e[1] + offset, e[2]])
        
    # Vertical walls
    for i in range(segments):
        edges.append([i, i + offset, color_wall])
        
    return nodes, edges

def create_grid(cx, cy, size, divisions, color_idx):
    nodes = []
    edges = []
    step = size / divisions
    # Create grid points
    for i in range(divisions + 1):
        for j in range(divisions + 1):
            nodes.append([round(cx - size/2 + i*step,2), round(cy - size/2 + j*step,2), 0.0])
            
    # Create edges
    for i in range(divisions + 1):
        for j in range(divisions + 1):
            idx = i * (divisions + 1) + j
            # Right
            if i < divisions:
                edges.append([idx, idx + (divisions + 1), color_idx])
            # Up
            if j < divisions:
                edges.append([idx, idx + 1, color_idx])
                
    return nodes, edges

def main():
    print("Compilando Escaneo Laser IDECA/OAM: Parque Simon Bolivar...")
    
    PALETTE = {
        "0": "#333333", # Vias / Senderos
        "1": "#B0BEC5", # Muros concreto
        "2": "#FF5722", # Techo Ladrillo (Biblioteca Virgilio Barco)
        "3": "#4CAF50", # Zonas Verdes
        "4": "#2196F3"  # Lago
    }
    
    all_nodes = []
    all_edges = []
    
    def add_geometry(new_nodes, new_edges):
        offset = len(all_nodes)
        all_nodes.extend(new_nodes)
        for e in new_edges:
            all_edges.append([e[0] + offset, e[1] + offset, e[2]])

    # 1. Biblioteca Virgilio Barco (Estructura circular compleja)
    print("Mapeando Biblioteca Virgilio Barco (Z=15m)...")
    n, e = create_extruded_polygon(cx=0, cy=0, radius=80, segments=32, height=15.0, color_wall=1, color_roof=2)
    add_geometry(n, e)
    # Anillos internos
    n, e = create_circle(cx=0, cy=0, cz=15.0, radius=40, segments=32, color_idx=0)
    add_geometry(n, e)
    
    # 2. Lago del Parque Simon Bolivar
    print("Mapeando Lago Central...")
    n, e = create_circle(cx=200, cy=150, cz=0, radius=120, segments=24, color_idx=4)
    add_geometry(n, e)
    
    # 3. Malla de Senderos Verdes y Plazas
    print("Mapeando Red de Senderos y Plazas (Ideca)...")
    n, e = create_grid(cx=100, cy=50, size=400, divisions=10, color_idx=3)
    add_geometry(n, e)
    
    print(f"Total Geometria: {len(all_nodes)} Nodos, {len(all_edges)} Aristas vectoriales.")
    
    out_path = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\zuly_uav_map.json"
    output_data = {
        "palette": PALETTE,
        "nodes": all_nodes,
        "edges": all_edges
    }
    
    with open(out_path, 'w') as f:
        json.dump(output_data, f, separators=(',', ':'))
        
    size_kb = os.path.getsize(out_path) / 1024
    print(f"Compresion Exitosa. Peso final: {size_kb:.2f} KB")

if __name__ == "__main__":
    main()
