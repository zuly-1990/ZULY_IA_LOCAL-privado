# core/config.py
"""
Configuración global del sistema Zuly.
"""

import os
import json
from pathlib import Path

class Config:
    """Clase de configuración del sistema Zuly."""
    
    def __init__(self):
        # Directorio base del proyecto
        self.BASE_DIR = Path(__file__).parent.parent
        
        # Cargar configuración desde config.json si existe
        config_path = self.BASE_DIR / "config.json"
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                self._config_data = json.load(f)
        else:
            self._config_data = {}
        
        # Configuración de Blender
        self.BLENDER_VERSION = self._config_data.get('entorno', {}).get('version_blender', '3.6')
        self.RENDER_ENGINE = self._config_data.get('entorno', {}).get('motor_render', 'cycles')
        self.RENDER_SAMPLES = self._config_data.get('entorno', {}).get('muestras_render', 32)
        
        # Directorios
        self.OUTPUT_DIR = self.BASE_DIR / self._config_data.get('entorno', {}).get('directorio_salida', './export/')
        self.LOGS_DIR = self.BASE_DIR / "bitacora"
        self.REPORTS_DIR = self.BASE_DIR / "reports"
        
        # Crear directorios si no existen
        self.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        self.LOGS_DIR.mkdir(parents=True, exist_ok=True)
        self.REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        
        # Configuración de logs
        self.LOG_LEVEL = self._config_data.get('logs', {}).get('nivel', 'INFO')
        self.LOG_FILE = self.LOGS_DIR / "zuly_agent.log"
        
        # Configuración de objetos 3D
        self.VALID_OBJECTS = self._config_data.get('objeto_3d', {}).get('opciones_validas', [
            'cubo', 'esfera', 'cilindro', 'cono', 'plano'
        ])
        
        # Configuración de materiales
        self.VALID_MATERIALS = self._config_data.get('material', {}).get('opciones_validas', [
            'oro', 'plata', 'negro_mate', 'blanco_brillante', 'vidrio'
        ])
        
        # Configuración de pruebas
        self.TESTS_ENABLED = self._config_data.get('pruebas', {})

        # ==============================================================================
        # SEGURIDAD Y PRESUPUESTO (SAFETY NET) - ZULY v4.0
        # ==============================================================================
        # Límite de gasto diario en USD
        self.MAX_DAILY_BUDGET_USD = self._config_data.get('seguridad', {}).get('presupuesto_diario', 1.00)
        # Costo estimado por llamada a API Vision
        self.COST_PER_VISION_CALL = 0.01
        # Límite de iteraciones autónomas (Circuit Breaker)
        self.MAX_AUTONOMOUS_ITERATIONS = 5
        # Archivo de registro de gastos
        self.BUDGET_TRACKER_FILE = self.LOGS_DIR / "budget_tracker.json"
    
    def get(self, key, default=None):
        """Obtiene un valor de configuración."""
        return self._config_data.get(key, default)
    
    def __repr__(self):
        return f"<Config: Blender {self.BLENDER_VERSION}, Engine: {self.RENDER_ENGINE}>"

# Instancia global de configuración
config = Config()
