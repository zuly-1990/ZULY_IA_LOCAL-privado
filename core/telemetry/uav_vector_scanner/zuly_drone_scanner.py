import cv2
import numpy as np
import json
import os
from scipy.spatial import Delaunay
import math

def hex_to_rgb(hex_code):
    hex_code = hex_code.lstrip('#')
    return tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))

def color_distance(c1, c2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(c1, c2)))

def main():
    imagen_path = r"C:\Users\Admin\.gemini\antigravity\brain\c39cd392-d7db-4d2c-875e-6664c3cb2a95\drone_aerial_neighborhood_1782649114337.png"
    
    if not os.path.exists(imagen_path):
        print(f"ERROR: No se encontró la imagen en {imagen_path}")
        return

    print("Inicializando Escáner Vectorial UAV...")
    
    # Paleta Semántica
    palette = {
        "0": "#333333", # Calles / Asfalto
        "1": "#FFFFFF", # Techos / Estructuras
        "2": "#4CAF50", # Vegetación
        "3": "#2196F3", # Agua
        "4": "#FF9800"  # Limites
    }
    
    # Pre-calcular colores RGB para la paleta (B, G, R por OpenCV)
    palette_bgr = {}
    for k, v in palette.items():
        r, g, b = hex_to_rgb(v)
        palette_bgr[k] = (b, g, r)

    # 1. Cargar Imagen
    img_color = cv2.imread(imagen_path)
    # Reducimos resolución si es muy grande para simular eficiencia de dron
    if max(img_color.shape) > 1024:
        scale = 1024 / max(img_color.shape)
        img_color = cv2.resize(img_color, (0,0), fx=scale, fy=scale)
    
    img_gray = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)
    
    print("Detectando Esquinas Arquitectónicas (Nodos)...")
    # 2. Detectar Esquinas (Nodos) con Shi-Tomasi
    # maxCorners, qualityLevel, minDistance
    corners = cv2.goodFeaturesToTrack(img_gray, maxCorners=500, qualityLevel=0.01, minDistance=15)
    corners = np.int32(corners)
    
    nodes = []
    points_2d = []
    for i, pt in enumerate(corners):
        x, y = pt.ravel()
        # Elevacion simulada en Z = 0 por ahora
        nodes.append([int(x), int(y), 0.0])
        points_2d.append([x, y])
        
    print(f"Se encontraron {len(nodes)} nodos críticos.")

    # 3. Extraer contornos reales
    print("Analizando topología estructural...")
    edges_canny = cv2.Canny(img_gray, 50, 150, apertureSize=3)
    
    # 4. Triangulación para encontrar conexiones candidatas
    points_np = np.array(points_2d)
    tri = Delaunay(points_np)
    
    # Extraer aristas únicas de la triangulación
    candidate_edges = set()
    for t in tri.simplices:
        candidate_edges.add(tuple(sorted((t[0], t[1]))))
        candidate_edges.add(tuple(sorted((t[1], t[2]))))
        candidate_edges.add(tuple(sorted((t[2], t[0]))))
        
    print(f"Validando {len(candidate_edges)} conexiones candidatas contra la geometría real...")
    
    valid_edges = []
    
    for edge in candidate_edges:
        pt1 = points_2d[edge[0]]
        pt2 = points_2d[edge[1]]
        
        # Crear máscara temporal para esta línea
        mask = np.zeros(img_gray.shape, dtype=np.uint8)
        cv2.line(mask, (int(pt1[0]), int(pt1[1])), (int(pt2[0]), int(pt2[1])), 255, 2)
        
        # Validar si esta línea cruza un borde estructural real (usando Canny)
        overlap = cv2.bitwise_and(edges_canny, mask)
        pixels_in_line = np.count_nonzero(mask)
        pixels_overlap = np.count_nonzero(overlap)
        
        # Si al menos un 15% de la línea coincide con un borde real, la aceptamos
        if pixels_in_line > 0 and (pixels_overlap / pixels_in_line) > 0.15:
            # 5. Mapear Color Semántico
            # Promedio de color bajo la línea
            mean_color = cv2.mean(img_color, mask=mask)[:3] # B, G, R
            
            best_color_index = "0"
            min_dist = float('inf')
            
            for k, color_val in palette_bgr.items():
                dist = color_distance(mean_color, color_val)
                if dist < min_dist:
                    min_dist = dist
                    best_color_index = k
                    
            valid_edges.append([int(edge[0]), int(edge[1]), int(best_color_index)])

    print(f"Geometría confirmada: {len(valid_edges)} conexiones estructurales.")
    
    # 6. Exportar JSON de peso pluma
    output_data = {
        "palette": palette,
        "nodes": nodes,
        "edges": valid_edges
    }
    
    out_path = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\zuly_uav_map.json"
    with open(out_path, 'w') as f:
        json.dump(output_data, f, separators=(',', ':'))
        
    size_kb = os.path.getsize(out_path) / 1024
    print(f"Compresión exitosa! Mapa guardado en {out_path}")
    print(f"PESO TOTAL DEL ARCHIVO: {size_kb:.2f} KB")

if __name__ == "__main__":
    main()
