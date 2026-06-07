"""
core/environment/blender_config.py

Configuración de Blender para ZULY.
Lee la ruta de Blender desde .env.blender y la proporciona al sistema.
"""

from pathlib import Path
import os
from core.utils.logging import log_info, log_warning

# Intentar cargar archivo .env.blender
try:
    from dotenv import load_dotenv
    env_file = Path(__file__).parent.parent.parent / ".env.blender"
    if env_file.exists():
        load_dotenv(str(env_file), override=True)
        log_info(f"✓ Configuración de Blender cargada desde: {env_file}")
    else:
        log_warning(f"⚠️ Archivo .env.blender no encontrado en {env_file}")
except ImportError:
    log_warning("⚠️ python-dotenv no instalado, omitiendo carga de .env.blender")
except Exception as e:
    log_warning(f"⚠️ Error cargando .env.blender: {e}")

# Configuración de Blender
class BlenderConfig:
    """Configuración centralizada de Blender para ZULY."""
    
    @staticmethod
    def get_blender_path() -> str:
        """Retorna la ruta al ejecutable de Blender."""
        # 1. Intentar desde variable de entorno
        blender_path = os.getenv("BLENDER_PATH")
        if blender_path and Path(blender_path).exists():
            log_info(f"✓ Usando ruta de Blender desde .env.blender: {blender_path}")
            return blender_path
        
        # 2. Intenta detección automática en PATH
        import shutil
        blender_exe = shutil.which("blender")
        if blender_exe:
            log_info(f"✓ Blender encontrado en PATH: {blender_exe}")
            return blender_exe
        
        # 3. Fallback a ruta local predeterminada
        default_path = r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL\blender\v3\blender-3.6.0-zuly\blender.exe"
        if Path(default_path).exists():
            log_info(f"✓ Usando ruta local predeterminada: {default_path}")
            return default_path
        
        log_warning("⚠️ No se encontró ruta de Blender disponible")
        return None
    
    @staticmethod
    def get_blender_version() -> str:
        """Retorna la versión de Blender configurada."""
        return os.getenv("BLENDER_VERSION", "3.6.0")
    
    @staticmethod
    def get_connection_mode() -> str:
        """Retorna el modo de conexión a Blender."""
        return os.getenv("BLENDER_CONNECTION_MODE", "python_subprocess")
    
    @staticmethod
    def get_operation_mode() -> str:
        """Retorna el modo de operación (background vs interactive)."""
        return os.getenv("BLENDER_OPERATION_MODE", "background")
    
    @staticmethod
    def get_timeout() -> int:
        """Retorna el timeout en segundos."""
        return int(os.getenv("BLENDER_TIMEOUT", "300"))
    
    @staticmethod
    def is_test_mode() -> bool:
        """Retorna si está en modo de prueba."""
        return os.getenv("BLENDER_TEST_MODE", "false").lower() == "true"
    
    @staticmethod
    def get_output_dir() -> str:
        """Retorna el directorio de salida."""
        return os.getenv("BLENDER_OUTPUT_DIR", "./export/")


# Verificar configuración al importar
blender_path = BlenderConfig.get_blender_path()
if blender_path:
    log_info(f"✅ Blender conectado: {blender_path}")
else:
    log_warning("⚠️ Blender no disponible - usando modo MOCK")
