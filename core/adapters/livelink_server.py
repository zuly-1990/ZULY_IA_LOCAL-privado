import bpy
import socket
import json
import threading

# Puerto de comunicación Zuly
HOST = 'localhost'
PORT = 9999

class ZulyLiveServer:
    _instance = None
    
    def __init__(self):
        self.sock = None
        self.running = False
        self.queue = []
        self.lock = threading.Lock()
        
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = ZulyLiveServer()
        return cls._instance

    def start(self):
        if self.running:
            print("🚀 El servidor Zuly Live ya está corriendo.")
            return
            
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self.sock.bind((HOST, PORT))
        except socket.error as e:
            print(f"❌ Error bindeando el puerto: {e}")
            return
            
        self.sock.listen(1)
        self.running = True
        print(f"📡 Zuly Live-Link escuchando en {HOST}:{PORT}")
        
        # Hilo de escucha para no bloquear la UI de Blender
        threading.Thread(target=self._listen, daemon=True).start()
        
        # Registrar el procesador de colas en el timer de Blender
        if not bpy.app.timers.is_registered(self._process_queue):
            bpy.app.timers.register(self._process_queue, first_interval=0.1)

    def _listen(self):
        while self.running:
            try:
                self.sock.settimeout(1.0)
                conn, addr = self.sock.accept()
                with conn:
                    data = conn.recv(1024 * 10) # 10KB max
                    if data:
                        decoded = data.decode('utf-8')
                        try:
                            msg = json.loads(decoded)
                            with self.lock:
                                self.queue.append(msg)
                            conn.sendall(b"OK_RECEIVED")
                        except json.JSONDecodeError:
                            conn.sendall(b"ERROR_JSON")
            except socket.timeout:
                continue
            except Exception as e:
                print(f"❌ Error en listener: {e}")
                break

    def _process_queue(self):
        with self.lock:
            if not self.queue:
                return 0.05 # Re-chequear en 50ms
            
            while self.queue:
                cmd = self.queue.pop(0)
                self._execute_command(cmd)
        
        return 0.05

    def _execute_command(self, cmd):
        """
        Traductor Universal de Comandos Zuly -> Blender BPY
        """
        action = cmd.get('action')
        params = cmd.get('params', {})
        print(f"⚙️ Procesando: {action}")
        
        try:
            if action == "create_cube":
                size = params.get('size', 2.0)
                loc = params.get('location', (0,0,0))
                bpy.ops.mesh.primitive_cube_add(size=size, location=loc)
            elif action == "create_sphere":
                radius = params.get('radius', 1.0)
                loc = params.get('location', (0,0,0))
                bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, location=loc)
            elif action == "create_hollow_primitive":
                # Motor V3 Ultra-Estable para Live-Link
                import math
                p_type = params.get('type', 'cube')
                loc = params.get('location', (0,0,0))
                
                # 1. Crear Base
                if p_type == 'cube': bpy.ops.mesh.primitive_cube_add(size=2, location=loc)
                elif p_type == 'sphere': bpy.ops.mesh.primitive_uv_sphere_add(radius=1.0, location=loc)
                elif p_type == 'monkey': bpy.ops.mesh.primitive_monkey_add(size=2, location=loc)
                else: bpy.ops.mesh.primitive_cube_add(size=2, location=loc)
                
                obj = bpy.context.active_object
                
                # 2. Crear Taladros
                cutters = []
                # X
                bpy.ops.mesh.primitive_cylinder_add(radius=0.25, depth=10, location=loc, rotation=(0, math.pi/2, 0))
                cutters.append(bpy.context.active_object)
                # Y
                bpy.ops.mesh.primitive_cylinder_add(radius=0.25, depth=10, location=loc, rotation=(math.pi/2, 0, 0))
                cutters.append(bpy.context.active_object)
                # Z
                bpy.ops.mesh.primitive_cylinder_add(radius=0.25, depth=10, location=loc)
                cutters.append(bpy.context.active_object)
                
                # 3. Aplicar Booleanos con gestión de contexto forzada
                for i, cut in enumerate(cutters):
                    bpy.ops.object.select_all(action='DESELECT')
                    obj.select_set(True)
                    bpy.context.view_layer.objects.active = obj
                    
                    mod = obj.modifiers.new(name=f"LiveHole_{i}", type='BOOLEAN')
                    mod.operation = 'DIFFERENCE'
                    mod.object = cut
                    mod.solver = 'EXACT'
                    bpy.ops.object.modifier_apply(modifier=mod.name)
                    bpy.data.objects.remove(cut, do_unlink=True)
                
            elif action == "move_object":
                target = params.get('name')
                loc = params.get('location', (0,0,0))
                if target in bpy.data.objects:
                    bpy.data.objects[target].location = loc
            elif action == "delete_all":
                bpy.ops.object.select_all(action='SELECT')
                bpy.ops.object.delete()
            # Expandir según sea necesario
        except Exception as e:
            print(f"❌ Error ejecutando comando: {e}")

    def stop(self):
        self.running = False
        if self.sock:
            self.sock.close()
        print("🛑 Servidor Zuly Live detenido.")

# Ejecución
server = ZulyLiveServer.get_instance()
server.start()
