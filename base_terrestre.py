import tkinter as tk
import socket
import threading
import json
import time

HOST = '127.0.0.1'
PORT = 9999

class ZulyGroundStation:
    def __init__(self, root):
        self.root = root
        self.root.title("Zuly UAV Ground Station - Recibiendo Telemetría...")
        self.canvas = tk.Canvas(root, width=800, height=600, bg='black')
        self.canvas.pack()
        
        self.nodes = []
        self.palette = {}
        
        self.scale = 1.0
        self.offset_x = 400
        self.offset_y = 300
        
        # Iniciar hilo de servidor TCP
        self.server_thread = threading.Thread(target=self.start_server, daemon=True)
        self.server_thread.start()

    def start_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            print(f"Base terrestre escuchando en {HOST}:{PORT}")
            conn, addr = s.accept()
            with conn:
                print(f"Enlace establecido con el dron: {addr}")
                buffer = ""
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    buffer += data.decode('utf-8')
                    while '\n' in buffer:
                        line, buffer = buffer.split('\n', 1)
                        self.process_packet(line)

    def process_packet(self, packet_str):
        try:
            packet = json.loads(packet_str)
            p_type = packet.get("type")
            
            if p_type == "palette":
                self.palette = packet.get("data")
            elif p_type == "nodes":
                self.nodes = packet.get("data")
            elif p_type == "edge":
                # Schedule drawing on main thread
                edge = packet.get("data")
                self.root.after(0, self.draw_edge, edge)
        except Exception as e:
            print("Error procesando paquete:", e)

    def draw_edge(self, edge):
        if not self.nodes or not self.palette: return
        n1_idx, n2_idx, color_idx = edge
        x1, y1, z1 = self.nodes[n1_idx]
        x2, y2, z2 = self.nodes[n2_idx]
        
        hex_color = self.palette.get(str(color_idx), "#FFFFFF")
        
        # Proyeccion ortografica 2D simple para Tkinter
        cx1 = x1 * self.scale + self.offset_x
        cy1 = y1 * self.scale + self.offset_y
        cx2 = x2 * self.scale + self.offset_x
        cy2 = y2 * self.scale + self.offset_y
        
        self.canvas.create_line(cx1, cy1, cx2, cy2, fill=hex_color, width=2)
        # Update is handled by Tkinter mainloop

def main():
    root = tk.Tk()
    app = ZulyGroundStation(root)
    root.mainloop()

if __name__ == "__main__":
    main()
