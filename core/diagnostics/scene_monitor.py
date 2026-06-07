# core/diagnostics/scene_monitor.py
"""
Monitor de escena para capturar y analizar el estado de Blender.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
from core.utils.logging import log_info, log_warning, log_error

class SceneState:
    """Representa el estado de una escena en un momento dado."""
    
    def __init__(self, timestamp: str = None):
        """
        Inicializa un estado de escena.
        
        :param timestamp: Marca de tiempo del estado
        """
        self.timestamp = timestamp or datetime.now().isoformat()
        self.objects = []
        self.lights = []
        self.cameras = []
        self.materials = []
        self.metadata = {}
    
    def add_object(self, obj_data: Dict):
        """Añade un objeto al estado."""
        self.objects.append(obj_data)
    
    def add_light(self, light_data: Dict):
        """Añade una luz al estado."""
        self.lights.append(light_data)
    
    def add_camera(self, camera_data: Dict):
        """Añade una cámara al estado."""
        self.cameras.append(camera_data)
    
    def to_dict(self) -> Dict:
        """Convierte el estado a diccionario."""
        return {
            'timestamp': self.timestamp,
            'objects': self.objects,
            'lights': self.lights,
            'cameras': self.cameras,
            'materials': self.materials,
            'metadata': self.metadata,
        }


class SceneMonitor:
    """Monitor de escena que captura el estado de Blender.
    
    FASE 17: Refactorizado para usar EngineAdapter.
    """
    
    def __init__(self, adapter=None, max_history: int = 50):
        """
        Inicializa el monitor de escena.
        
        Args:
            adapter: EngineAdapter instance (si es None, se obtiene automáticamente)
            max_history: Número máximo de estados a mantener en memoria
        """
        self.scene_history = []
        self.current_state = None
        self.max_history = max_history
        self.adapter = adapter
        if self.adapter is None:
            from core.adapters import get_engine_adapter
            self.adapter = get_engine_adapter()
        log_info("SceneMonitor inicializado")
    
    def capture_scene_state(self) -> SceneState:
        """
        Captura el estado actual de la escena usando EngineAdapter.
        
        FASE 17: Ahora usa EngineAdapter en lugar de bpy directo.
        
        :return: Estado de la escena capturado
        """
        state = SceneState()
        
        if not self.adapter or not self.adapter.is_available():
            log_warning("Adapter no disponible - usando estado simulado")
            state.metadata['simulated'] = True
            self.current_state = state
            self.scene_history.append(state)
            return state
        
        try:
            # Obtener estado de la escena a través del adapter
            scene_state = self.adapter.get_scene_state()
            
            if not scene_state.get('success', False):
                log_error(f"Error obteniendo estado de escena: {scene_state.get('error', 'Unknown')}")
                state.metadata['error'] = scene_state.get('error', 'Unknown')
                self.current_state = state
                self.scene_history.append(state)
                return state
            
            # Procesar objetos
            for obj in scene_state.get('objects', []):
                obj_data = {
                    'name': obj['name'],
                    'type': obj['type'],
                    'location': obj.get('location', [0, 0, 0]),
                    'rotation': obj.get('rotation', [0, 0, 0]),
                    'scale': obj.get('scale', [1, 1, 1]),
                }
                
                # Clasificar por tipo
                if obj['type'] == 'MESH':
                    state.add_object(obj_data)
                elif obj['type'] == 'LIGHT':
                    # Nota: información detallada de luz no disponible en adapter estándar
                    obj_data['light_type'] = 'POINT'  # Fallback
                    obj_data['energy'] = 1.0  # Fallback
                    state.add_light(obj_data)
                elif obj['type'] == 'CAMERA':
                    state.add_camera(obj_data)
            
            # Materiales (no disponibles en adapter estándar)
            state.materials = []
            
            log_info(f"Estado capturado: {len(state.objects)} objetos, {len(state.lights)} luces")
        
        except Exception as e:
            log_error(f"Error capturando estado de escena: {e}")
            state.metadata['error'] = str(e)
        
        self.current_state = state
        self.scene_history.append(state)
        
        # Gestión de memoria: Rotación de historial
        if len(self.scene_history) > self.max_history:
            self.scene_history.pop(0)
        
        return state
    
    def get_scene_summary(self) -> Dict:
        """
        Obtiene un resumen del estado actual de la escena.
        
        :return: Diccionario con resumen de la escena
        """
        if self.current_state is None:
            # Capturar estado si no existe
            self.capture_scene_state()
        
        state = self.current_state
        
        summary = {
            'timestamp': state.timestamp,
            'object_count': len(state.objects),
            'light_count': len(state.lights),
            'camera_count': len(state.cameras),
            'material_count': len(state.materials),
            'objects': [obj.get('name', 'Unknown') for obj in state.objects],
            'lights': [light.get('name', 'Unknown') for light in state.lights],
            'simulated': state.metadata.get('simulated', False),
        }
        
        return summary
    
    def validate_scene_requirements(self, requirements: Dict) -> Dict:
        """
        Valida si la escena cumple con ciertos requisitos.
        
        :param requirements: Diccionario de requisitos
        :return: Diccionario con resultados de validación
        """
        if self.current_state is None:
            self.capture_scene_state()
        
        state = self.current_state
        results = {
            'valid': True,
            'missing': [],
            'satisfied': [],
        }
        
        # Validar número mínimo de objetos
        if 'min_objects' in requirements:
            if len(state.objects) < requirements['min_objects']:
                results['valid'] = False
                results['missing'].append(f"Se requieren al menos {requirements['min_objects']} objetos")
            else:
                results['satisfied'].append('Número mínimo de objetos')
        
        # Validar presencia de luces
        if requirements.get('requires_light', False):
            if len(state.lights) == 0:
                results['valid'] = False
                results['missing'].append('Se requiere al menos una luz')
            else:
                results['satisfied'].append('Iluminación presente')
        
        # Validar presencia de cámara
        if requirements.get('requires_camera', False):
            if len(state.cameras) == 0:
                results['valid'] = False
                results['missing'].append('Se requiere al menos una cámara')
            else:
                results['satisfied'].append('Cámara presente')
        
        return results
    
    def get_scene_history(self) -> List[SceneState]:
        """Retorna el historial de estados de escena."""
        return self.scene_history
    
    def export_scene_state(self, filepath: str = None) -> str:
        """
        Exporta el estado actual de la escena a JSON.
        
        :param filepath: Ruta del archivo de salida
        :return: Ruta del archivo exportado
        """
        import json
        from pathlib import Path
        
        if filepath is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = f"scene_state_{timestamp}.json"
        
        if self.current_state is None:
            self.capture_scene_state()
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.current_state.to_dict(), f, indent=2, ensure_ascii=False)
        
        log_info(f"Estado de escena exportado a: {filepath}")
        return filepath
