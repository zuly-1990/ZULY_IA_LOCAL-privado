"""
core/observability/session_registry.py

Registro de sesiones para mantener la persistencia de configuración
de Blender entre inicios de ZULY.
"""

import json
from pathlib import Path
from datetime import datetime
from core.utils.logging import log_info, log_debug


class SessionRegistry:
    """
    Mantiene un registro de sesiones exitosas de ZULY.
    Asegura que la configuración de Blender persista entre inicios.
    """
    
    REGISTRY_FILE = Path(__file__).parent.parent.parent / "ZULY_SESSION_REGISTRY.json"
    
    @classmethod
    def register_session(cls, blender_path: str = None, status: str = "success"):
        """
        Registra una nueva sesión en el archivo de persistencia.
        
        Args:
            blender_path: Ruta de Blender detectada
            status: Estado de la sesión (success, warning, error)
        """
        try:
            # Cargar registro existente
            registry_data = cls._load_registry()
            
            # Crear entrada de sesión
            session_entry = {
                "timestamp": datetime.now().isoformat(),
                "status": status,
                "blender_path": blender_path,
                "agent_version": "2.0",
                "notes": "Configuración de Blender persistida"
            }
            
            # Agregar a registro
            if "sessions" not in registry_data:
                registry_data["sessions"] = []
            
            registry_data["sessions"].append(session_entry)
            
            # Mantener solo últimas 100 sesiones
            if len(registry_data["sessions"]) > 100:
                registry_data["sessions"] = registry_data["sessions"][-100:]
            
            # Actualizar último estado conocido
            registry_data["last_session"] = session_entry
            registry_data["blender_configured"] = blender_path is not None
            registry_data["last_blender_path"] = blender_path
            
            # Guardar
            cls._save_registry(registry_data)
            
            log_info(f"✓ Sesión registrada en: {cls.REGISTRY_FILE}")
            
        except Exception as e:
            log_debug(f"Advertencia al registrar sesión: {e}")
    
    @classmethod
    def get_last_session_info(cls) -> dict:
        """Retorna información de la última sesión registrada."""
        try:
            data = cls._load_registry()
            return data.get("last_session", {})
        except Exception as e:
            log_debug(f"Error cargando última sesión: {e}")
            return {}
    
    @classmethod
    def is_blender_configured(cls) -> bool:
        """Verifica si Blender fue configurado en sesiones anteriores."""
        try:
            data = cls._load_registry()
            return data.get("blender_configured", False)
        except Exception as e:
            log_debug(f"Error verificando configuración: {e}")
            return False
    
    @classmethod
    def get_last_blender_path(cls) -> str:
        """Retorna la última ruta de Blender conocida."""
        try:
            data = cls._load_registry()
            return data.get("last_blender_path", None)
        except Exception as e:
            log_debug(f"Error cargando ruta anterior: {e}")
            return None
    
    @classmethod
    def get_session_count(cls) -> int:
        """Retorna el número total de sesiones registradas."""
        try:
            data = cls._load_registry()
            return len(data.get("sessions", []))
        except Exception as e:
            log_debug(f"Error contando sesiones: {e}")
            return 0
    
    @classmethod
    def print_session_summary(cls):
        """Imprime resumen de sesiones para debugging."""
        try:
            data = cls._load_registry()
            total = len(data.get("sessions", []))
            last = data.get("last_session", {})
            
            log_info(f"\n📊 REGISTRO DE SESIONES ZULY")
            log_info(f"   • Total sesiones: {total}")
            log_info(f"   • Última sesión: {last.get('timestamp', 'N/A')}")
            log_info(f"   • Estado: {last.get('status', 'N/A')}")
            log_info(f"   • Blender configurado: {'SÍ' if data.get('blender_configured') else 'NO'}\n")
        except Exception as e:
            log_debug(f"Error imprimiendo resumen: {e}")
    
    @classmethod
    def _load_registry(cls) -> dict:
        """Carga el archivo de registro."""
        if cls.REGISTRY_FILE.exists():
            try:
                with open(cls.REGISTRY_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                log_debug(f"Error cargando registry: {e}")
                return cls._default_registry()
        return cls._default_registry()
    
    @classmethod
    def _save_registry(cls, data: dict):
        """Guarda el archivo de registro."""
        try:
            with open(cls.REGISTRY_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            log_debug(f"Error guardando registry: {e}")
    
    @classmethod
    def _default_registry(cls) -> dict:
        """Retorna estructura de registro por defecto."""
        return {
            "version": "1.0",
            "created": datetime.now().isoformat(),
            "sessions": [],
            "blender_configured": False,
            "last_blender_path": None,
            "last_session": {}
        }
