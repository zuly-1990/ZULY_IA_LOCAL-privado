"""
ZULY Web UI - Flask Backend
Interfaz web moderna para controlar el agente ZULY
"""

from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
from flask_socketio import SocketIO, emit, join_room, leave_room
import json
import os
import sys
from datetime import datetime
from pathlib import Path
import threading
import uuid
from io import BytesIO

# Importar el agente ZULY
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.agent import Agent
from core.diagnostics.scene_monitor import SceneMonitor
from core.external.vision_analyzer import VisualAnalyzer

# Configuración de Flask
app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Configuración
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
RENDERS_FOLDER = os.path.join(os.path.dirname(__file__), 'renders')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RENDERS_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RENDERS_FOLDER'] = RENDERS_FOLDER

# Instancias globales
agent = None
scene_monitor = None
vision_analyzer = None
active_sessions = {}

# ==================== INICIALIZACIÓN ====================

def initialize_zuly():
    """Inicializa el agente ZULY"""
    global agent, scene_monitor, vision_analyzer
    try:
        config_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), 
            'config.json'
        )
        agent = Agent(config_path=config_path)
        scene_monitor = SceneMonitor()
        
        # Inicializar vision analyzer (puede fallar si no tiene API key)
        try:
            vision_analyzer = VisualAnalyzer()
        except Exception as e:
            print(f"Advertencia: VisualAnalyzer no inicializado: {e}")
            vision_analyzer = None
            
        return True
    except Exception as e:
        print(f"Error inicializando ZULY: {e}")
        return False

# ==================== RUTAS PRINCIPALES ====================

@app.route('/')
def index():
    """Página principal del dashboard"""
    return render_template('index.html')

@app.route('/api/status')
def get_status():
    """Obtiene el estado del sistema"""
    return jsonify({
        'status': 'ready' if agent else 'not_initialized',
        'agent_initialized': agent is not None,
        'vision_analyzer': vision_analyzer is not None,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/initialize', methods=['POST'])
def api_initialize():
    """Inicializa el sistema ZULY"""
    success = initialize_zuly()
    return jsonify({
        'success': success,
        'message': 'ZULY inicializado correctamente' if success else 'Error al inicializar ZULY'
    })

# ==================== API DE COMANDOS ====================

@app.route('/api/command', methods=['POST'])
def execute_command():
    """Ejecuta un comando ZULY"""
    if not agent:
        return jsonify({'error': 'ZULY no inicializado'}), 400
    
    try:
        data = request.json
        natural_request = data.get('request', '')
        
        if not natural_request:
            return jsonify({'error': 'Solicitud vacía'}), 400
        
        # Ejecutar comando en hilo separado para no bloquear
        session_id = str(uuid.uuid4())
        
        def execute():
            try:
                resultado = agent.process_natural_request(natural_request)
                active_sessions[session_id] = {
                    'status': 'completed',
                    'resultado': {
                        'exito': resultado.get('status') == 'exitoso',
                        'mensaje': resultado.get('mensaje', ''),
                        'detalles': resultado.get('detalles', {}),
                        'timestamp': datetime.now().isoformat()
                    }
                }
                # Emitir evento WebSocket
                socketio.emit('command_completed', {
                    'session_id': session_id,
                    'resultado': active_sessions[session_id]['resultado']
                }, broadcast=True)
            except Exception as e:
                active_sessions[session_id] = {
                    'status': 'error',
                    'error': str(e)
                }
                socketio.emit('command_error', {
                    'session_id': session_id,
                    'error': str(e)
                }, broadcast=True)
        
        thread = threading.Thread(target=execute)
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'session_id': session_id,
            'status': 'processing'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/command/<session_id>', methods=['GET'])
def get_command_status(session_id):
    """Obtiene el estado de un comando"""
    if session_id in active_sessions:
        return jsonify(active_sessions[session_id])
    return jsonify({'error': 'Sesión no encontrada'}), 404

# ==================== API DE ESCENA ====================

@app.route('/api/scene/info', methods=['GET'])
def get_scene_info():
    """Obtiene información de la escena actual"""
    if not agent:
        return jsonify({'error': 'ZULY no inicializado'}), 400
    
    try:
        # Aquí se podría obtener información de la escena actual
        return jsonify({
            'objects': [],
            'camera': 'Camera',
            'lights': [],
            'materials': [],
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/scene/reset', methods=['POST'])
def reset_scene():
    """Limpia la escena actual"""
    if not agent:
        return jsonify({'error': 'ZULY no inicializado'}), 400
    
    try:
        resultado = agent.process_natural_request("Limpia la escena")
        return jsonify({'success': True, 'resultado': resultado})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== API DE RENDER ====================

@app.route('/api/render', methods=['POST'])
def start_render():
    """Inicia un render"""
    if not agent:
        return jsonify({'error': 'ZULY no inicializado'}), 400
    
    try:
        data = request.json
        config = data.get('config', {})
        
        # Construir solicitud de render
        motor = config.get('engine', 'CYCLES')
        muestras = config.get('samples', 128)
        resolucion = config.get('resolution', '1920x1080')
        
        solicitud = f"Renderiza con {motor}, {muestras} muestras, resolución {resolucion}"
        
        session_id = str(uuid.uuid4())
        
        def render():
            try:
                resultado = agent.process_natural_request(solicitud)
                active_sessions[session_id] = {
                    'status': 'completed',
                    'resultado': resultado
                }
                socketio.emit('render_completed', {
                    'session_id': session_id,
                    'resultado': resultado
                }, broadcast=True)
            except Exception as e:
                active_sessions[session_id] = {
                    'status': 'error',
                    'error': str(e)
                }
        
        thread = threading.Thread(target=render)
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'session_id': session_id,
            'status': 'rendering'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/renders', methods=['GET'])
def list_renders():
    """Lista todos los renders generados"""
    try:
        renders = []
        if os.path.exists(RENDERS_FOLDER):
            for file in os.listdir(RENDERS_FOLDER):
                if file.endswith(('.png', '.jpg', '.tiff', '.exr')):
                    filepath = os.path.join(RENDERS_FOLDER, file)
                    renders.append({
                        'filename': file,
                        'size': os.path.getsize(filepath),
                        'timestamp': datetime.fromtimestamp(
                            os.path.getmtime(filepath)
                        ).isoformat()
                    })
        
        return jsonify({'renders': sorted(renders, 
                                         key=lambda x: x['timestamp'], 
                                         reverse=True)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== API DE ANÁLISIS ====================

@app.route('/api/analyze/<render_id>', methods=['POST'])
def analyze_render(render_id):
    """Analiza un render con VisualAnalyzer"""
    if not vision_analyzer:
        return jsonify({
            'error': 'VisualAnalyzer no disponible',
            'message': 'Configure la API key de Gemini en config.json'
        }), 400
    
    try:
        render_path = os.path.join(RENDERS_FOLDER, render_id)
        if not os.path.exists(render_path):
            return jsonify({'error': 'Render no encontrado'}), 404
        
        session_id = str(uuid.uuid4())
        
        def analyze():
            try:
                analisis = vision_analyzer.analyze_render(
                    render_path,
                    analysis_type='describe'
                )
                active_sessions[session_id] = {
                    'status': 'completed',
                    'resultado': {
                        'success': analisis.success,
                        'description': analisis.description,
                        'quality_score': analisis.quality_score,
                        'objects_detected': analisis.objects_detected,
                        'lighting_description': analisis.lighting_description,
                        'suggestions': analisis.suggestions,
                        'timestamp': datetime.now().isoformat()
                    }
                }
                socketio.emit('analysis_completed', {
                    'session_id': session_id,
                    'resultado': active_sessions[session_id]['resultado']
                }, broadcast=True)
            except Exception as e:
                active_sessions[session_id] = {
                    'status': 'error',
                    'error': str(e)
                }
        
        thread = threading.Thread(target=analyze)
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'session_id': session_id,
            'status': 'analyzing'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== WEBSOCKET EVENTS ====================

@socketio.on('connect')
def handle_connect():
    """Cliente se conecta"""
    print(f'Cliente conectado: {request.sid}')
    emit('connected', {'message': 'Conectado a ZULY WebUI'})

@socketio.on('disconnect')
def handle_disconnect():
    """Cliente se desconecta"""
    print(f'Cliente desconectado: {request.sid}')

@socketio.on('command')
def handle_command(data):
    """Recibe comando vía WebSocket"""
    solicitud = data.get('request', '')
    if solicitud and agent:
        session_id = str(uuid.uuid4())
        
        def execute():
            try:
                resultado = agent.process_natural_request(solicitud)
                emit('command_result', {
                    'session_id': session_id,
                    'resultado': resultado,
                    'timestamp': datetime.now().isoformat()
                }, broadcast=True)
            except Exception as e:
                emit('command_error', {
                    'session_id': session_id,
                    'error': str(e)
                }, broadcast=True)
        
        thread = threading.Thread(target=execute)
        thread.daemon = True
        thread.start()

# ==================== UTILIDADES ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check del servidor"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'zuly_ready': agent is not None
    })

@app.errorhandler(404)
def not_found(error):
    """Manejo de ruta no encontrada"""
    return jsonify({'error': 'Ruta no encontrada'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Manejo de error interno"""
    return jsonify({'error': 'Error interno del servidor'}), 500

# ==================== INICIO ====================

if __name__ == '__main__':
    # Inicializar ZULY
    print("🚀 Inicializando ZULY...")
    initialize_zuly()
    
    # Iniciar servidor
    print("🌐 Iniciando servidor Web UI en http://localhost:5000")
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
