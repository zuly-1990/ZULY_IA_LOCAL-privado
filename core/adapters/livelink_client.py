import socket
import json
from typing import Dict, Any, Optional

HOST = 'localhost'
PORT = 9999

class ZulyLiveClient:
    """
    Cliente para comunicarse con Blender en tiempo real vía Sockets.
    """
    def __init__(self, host: str = HOST, port: int = PORT):
        self.host = host
        self.port = port

    def is_alive(self) -> bool:
        """ Verifica si el puente con Blender está abierto. """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.5)
                s.connect((self.host, self.port))
                return True
        except:
            return False

    def send_command(self, action: str, params: Dict[str, Any]) -> bool:
        """ Envía un comando a Blender. """
        msg = {
            "action": action,
            "params": params
        }
        data = json.dumps(msg).encode('utf-8')
        
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1.0)
                s.connect((self.host, self.port))
                s.sendall(data)
                response = s.recv(1024)
                return response == b"OK_RECEIVED"
        except Exception as e:
            print(f"⚠️ Error enviando comando Live-Link: {e}")
            return False

if __name__ == "__main__":
    # Prueba rápida
    client = ZulyLiveClient()
    if client.is_alive():
        print("✅ Puente detectado! Enviando cubo de prueba...")
        client.send_command("create_cube", {"size": 3.0, "location": (5, 0, 0)})
    else:
        print("❌ Puente no detectado. Abre Blender y corre livelink_server.py")
