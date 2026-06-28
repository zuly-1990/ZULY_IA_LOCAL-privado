import socket
import json
import time
import os

HOST = '127.0.0.1'
PORT = 9999
JSON_PATH = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\zuly_uav_map.json"

def main():
    if not os.path.exists(JSON_PATH):
        print(f"Error: No existe el mapa {JSON_PATH}")
        return

    with open(JSON_PATH, 'r') as f:
        map_data = json.load(f)
        
    print("Iniciando Transmisor de Telemetria del Dron Zuly...")
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORT))
            print("Conectado a la Base Terrestre.")
        except ConnectionRefusedError:
            print("Error: La base terrestre no esta encendida. Ejecuta base_terrestre.py primero.")
            return

        # 1. Enviar Paleta (Header)
        palette_packet = {"type": "palette", "data": map_data["palette"]}
        s.sendall((json.dumps(palette_packet) + '\n').encode('utf-8'))
        time.sleep(0.5)
        
        # 2. Enviar Nodos (Coordenadas maestras)
        print(f"Enviando matriz de {len(map_data['nodes'])} Nodos...")
        nodes_packet = {"type": "nodes", "data": map_data["nodes"]}
        s.sendall((json.dumps(nodes_packet) + '\n').encode('utf-8'))
        time.sleep(1.0)
        
        # 3. Transmitir Lineas (Aristas) una por una simulando bajo ancho de banda
        edges = map_data["edges"]
        print(f"Transmitiendo {len(edges)} lineas topograficas a 20Hz...")
        
        for i, edge in enumerate(edges):
            edge_packet = {"type": "edge", "data": edge}
            s.sendall((json.dumps(edge_packet) + '\n').encode('utf-8'))
            
            # Imprimir progreso en consola
            if i % 20 == 0:
                print(f"Progreso: {i}/{len(edges)} lineas enviadas...")
                
            time.sleep(0.005) # 200 lineas por segundo para grandes ciudades
            
        print("Mision Completada. Telemetria enviada al 100%.")

if __name__ == "__main__":
    main()
