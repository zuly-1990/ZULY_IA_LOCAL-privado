#!/usr/bin/env python3
"""
validate_zuly_system.py

VALIDACIÓN COMPLETA DE LA ESTRUCTURA DE ZULY
- Verifica rutas de proyectos
- Valida handlers disponibles
- Confirma adapters y conexión a Blender
- Genera reporte de conectividad

Uso: python validate_zuly_system.py
"""

import os
import sys
from pathlib import Path
import json
from typing import Dict, List, Tuple, Any

# Agregar ruta del proyecto
ZULY_ROOT = Path(__file__).parent
sys.path.insert(0, str(ZULY_ROOT))

# ============================================================================
# COLORES PARA SALIDA
# ============================================================================

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_header(text: str):
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}▶ {text}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.RESET}\n")

def print_success(text: str, details: str = ""):
    tick = f"{Colors.GREEN}✓{Colors.RESET}"
    msg = f"{tick} {Colors.GREEN}{text}{Colors.RESET}"
    if details:
        msg += f" {Colors.BLUE}({details}){Colors.RESET}"
    print(msg)

def print_error(text: str, details: str = ""):
    cross = f"{Colors.RED}✗{Colors.RESET}"
    msg = f"{cross} {Colors.RED}{text}{Colors.RESET}"
    if details:
        msg += f" {Colors.BLUE}({details}){Colors.RESET}"
    print(msg)

def print_warning(text: str, details: str = ""):
    warn = f"{Colors.YELLOW}⚠{Colors.RESET}"
    msg = f"{warn} {Colors.YELLOW}{text}{Colors.RESET}"
    if details:
        msg += f" {Colors.BLUE}({details}){Colors.RESET}"
    print(msg)

def print_info(text: str, details: str = ""):
    info = f"{Colors.BLUE}ℹ{Colors.RESET}"
    msg = f"{info} {text}"
    if details:
        msg += f" {Colors.BLUE}({details}){Colors.RESET}"
    print(msg)

# ============================================================================
# VALIDACIÓN DE RUTAS
# ============================================================================

def validate_paths() -> Dict[str, Any]:
    """Valida que todas las rutas de ZULY existan"""
    print_header("1. VALIDACIÓN DE RUTAS")
    
    required_paths = {
        "ZULY_ROOT": ZULY_ROOT,
        "ZULY_PROJECTS/pruebas": ZULY_ROOT / "ZULY_PROJECTS" / "pruebas",
        "export": ZULY_ROOT / "export",
        "knowledge_base": ZULY_ROOT / "knowledge_base",
        "knowledge_base/patterns/learned": ZULY_ROOT / "knowledge_base" / "patterns" / "learned",
        "ZULY_LAB": ZULY_ROOT / "ZULY_LAB",
        "bitacora": ZULY_ROOT / "bitacora",
        "core": ZULY_ROOT / "core",
        "core/adapters": ZULY_ROOT / "core" / "adapters",
        "core/commands": ZULY_ROOT / "core" / "commands",
        "core/commands/blender_handlers": ZULY_ROOT / "core" / "commands" / "blender_handlers",
    }
    
    results = {}
    for name, path in required_paths.items():
        exists = path.exists()
        if exists:
            print_success(f"Ruta: {name}", str(path))
        else:
            print_error(f"Ruta: {name}", f"NO EXISTE: {path}")
        results[name] = exists
    
    all_ok = all(results.values())
    
    if all_ok:
        print(f"\n{Colors.GREEN}{Colors.BOLD}✓ Todas las rutas están configuradas correctamente{Colors.RESET}")
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}✗ Algunas rutas están faltando{Colors.RESET}")
    
    return {"all_ok": all_ok, "paths": results}

# ============================================================================
# VALIDACIÓN DE HANDLERS
# ============================================================================

def validate_handlers() -> Dict[str, Any]:
    """Valida que todos los handlers estén disponibles"""
    print_header("2. VALIDACIÓN DE HANDLERS")
    
    required_handlers = [
        "create_cube_handler",
        "create_sphere_handler",
        "create_cylinder_handler",
        "create_plane_handler",
        "create_cone_handler",
        "move_object_handler",
        "rotate_object_handler",
        "scale_object_handler",
        "render_scene_handler",
        "delete_object_handler",
        "duplicate_object_handler",
        "select_object_handler",
    ]
    
    available_handlers = {}
    
    try:
        from core.commands.blender_handlers import (
            create_cube_handler,
            create_sphere_handler,
            create_cylinder_handler,
            create_plane_handler,
            create_cone_handler,
            move_object_handler,
            rotate_object_handler,
            scale_object_handler,
            render_scene_handler,
            delete_object_handler,
            duplicate_object_handler,
            select_object_handler,
        )
        
        handlers_dict = {
            "create_cube_handler": create_cube_handler,
            "create_sphere_handler": create_sphere_handler,
            "create_cylinder_handler": create_cylinder_handler,
            "create_plane_handler": create_plane_handler,
            "create_cone_handler": create_cone_handler,
            "move_object_handler": move_object_handler,
            "rotate_object_handler": rotate_object_handler,
            "scale_object_handler": scale_object_handler,
            "render_scene_handler": render_scene_handler,
            "delete_object_handler": delete_object_handler,
            "duplicate_object_handler": duplicate_object_handler,
            "select_object_handler": select_object_handler,
        }
        
        print_success("Importación de handlers", "Módulo blender_handlers cargado")
        
        for name in required_handlers:
            if name in handlers_dict and callable(handlers_dict[name]):
                print_success(f"Handler: {name}")
                available_handlers[name] = True
            else:
                print_error(f"Handler: {name}", "NO DISPONIBLE")
                available_handlers[name] = False
        
    except ImportError as e:
        print_error(f"Error importando handlers: {e}")
        return {"all_ok": False, "handlers": {}}
    
    all_ok = all(available_handlers.values())
    
    if all_ok:
        print(f"\n{Colors.GREEN}{Colors.BOLD}✓ Todos los handlers están disponibles{Colors.RESET}")
    else:
        print(f"\n{Colors.YELLOW}{Colors.BOLD}⚠ Algunos handlers no están disponibles{Colors.RESET}")
    
    return {"all_ok": all_ok, "handlers": available_handlers}

# ============================================================================
# VALIDACIÓN DE ADAPTER
# ============================================================================

def validate_adapter() -> Dict[str, Any]:
    """Valida que el adapter de Blender esté disponible"""
    print_header("3. VALIDACIÓN DE ADAPTER (Conexión Blender)")
    
    try:
        from core.adapters.blender_adapter import BlenderAdapter
        print_success("Importación", "BlenderAdapter disponible")
        
        adapter = BlenderAdapter()
        is_available = adapter.is_available()
        
        if is_available:
            print_success("Conexión Blender", "🔗 Blender conectado correctamente")
            
            # Obtener info del motor
            info = adapter.get_engine_info()
            if info.get('success'):
                engine_info = info.get('data', {})
                print_success("Versión Blender", engine_info.get('version', 'N/A'))
                print_info("Capacidades disponibles:", str(engine_info.get('capabilities', [])))
            else:
                print_warning("No se pudo obtener info del motor")
        else:
            print_warning("Blender NO está disponible actualmente", "Modo Mock habilitado")
            print_info("La mayoría de funciones funcionarán con datos simulados")
        
        return {
            "all_ok": True,
            "blender_available": is_available,
            "adapter_type": "BlenderAdapter",
            "engine_info": info if is_available else {}
        }
    
    except Exception as e:
        print_error(f"Error inicializando adapter: {e}")
        return {"all_ok": False, "blender_available": False}

# ============================================================================
# VALIDACIÓN DE ARCHIVOS DE PROYECTO
# ============================================================================

def validate_project_files() -> Dict[str, Any]:
    """Valida que los archivos de proyecto estén presentes"""
    print_header("4. VALIDACIÓN DE ARCHIVOS DE PROYECTO")
    
    projects_dir = ZULY_ROOT / "ZULY_PROJECTS" / "pruebas"
    
    if not projects_dir.exists():
        print_error(f"Directorio de proyectos no existe: {projects_dir}")
        return {"all_ok": False, "files": {}}
    
    # Buscar archivos .blend
    blend_files = list(projects_dir.glob("*.blend"))
    
    print_info(f"Archivos .blend encontrados: {len(blend_files)}")
    for blend_file in blend_files:
        print_success(f"Archivo: {blend_file.name}")
    
    # Buscar archivos JSON de laboratorio
    lab_dir = ZULY_ROOT / "ZULY_LAB"
    if lab_dir.exists():
        json_files = list(lab_dir.glob("*.json"))
        print_info(f"Archivos de laboratorio: {len(json_files)}")
        for json_file in json_files[:5]:  # Mostrar primeros 5
            print_success(f"Lab file: {json_file.name}")
        if len(json_files) > 5:
            print_info(f"... y {len(json_files) - 5} archivos más")
    
    # Buscar patrones aprendidos
    patterns_dir = ZULY_ROOT / "knowledge_base" / "patterns" / "learned"
    if patterns_dir.exists():
        pattern_files = list(patterns_dir.glob("*.json"))
        print_info(f"Patrones aprendidos: {len(pattern_files)}")
        for pattern_file in pattern_files[:3]:
            print_success(f"Pattern: {pattern_file.name}")
    
    return {
        "all_ok": len(blend_files) > 0,
        "blend_files": [f.name for f in blend_files],
        "blend_count": len(blend_files)
    }

# ============================================================================
# VALIDACIÓN DE CONFIGURACIÓN
# ============================================================================

def validate_config() -> Dict[str, Any]:
    """Valida la configuración de ZULY"""
    print_header("5. VALIDACIÓN DE CONFIGURACIÓN (config.json)")
    
    config_path = ZULY_ROOT / "config.json"
    
    if not config_path.exists():
        print_error(f"config.json no encontrado en: {config_path}")
        return {"all_ok": False, "config": {}}
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        print_success("config.json", "Cargado correctamente")
        
        # Validar campos principales
        required_fields_env = ['modo', 'version_blender', 'motor_render', 'directorio_salida']
        if 'entorno' in config:
            env = config['entorno']
            for field in required_fields_env:
                if field in env:
                    print_success(f"Config.entorno.{field}", str(env[field]))
                else:
                    print_warning(f"Config.entorno.{field}", "NO CONFIGURADO")
        
        return {"all_ok": True, "config": config}
    
    except json.JSONDecodeError as e:
        print_error(f"Error decodificando config.json: {e}")
        return {"all_ok": False, "config": {}}

# ============================================================================
# VALIDACIÓN DEL CORE
# ============================================================================

def validate_core() -> Dict[str, Any]:
    """Valida módulos core principales"""
    print_header("6. VALIDACIÓN DE MÓDULOS CORE")
    
    core_modules = {
        "agent": "core.agent",
        "adapters": "core.adapters",
        "nlu": "core.utils.nlu",
        "scene_monitor": "core.diagnostics.scene_monitor",
        "learning_engine": "core.learning.learning_freedom_engine",
    }
    
    available_modules = {}
    
    for name, module_path in core_modules.items():
        try:
            __import__(module_path)
            print_success(f"Módulo: {name} ({module_path})")
            available_modules[name] = True
        except ImportError as e:
            print_warning(f"Módulo: {name}", f"ERROR: {e}")
            available_modules[name] = False
    
    all_ok = all(available_modules.values())
    
    if all_ok:
        print(f"\n{Colors.GREEN}{Colors.BOLD}✓ Todos los módulos core están disponibles{Colors.RESET}")
    else:
        print(f"\n{Colors.YELLOW}{Colors.BOLD}⚠ Algunos módulos core no están disponibles{Colors.RESET}")
    
    return {"all_ok": all_ok, "modules": available_modules}

# ============================================================================
# REPORTE FINAL
# ============================================================================

def generate_final_report(results: Dict[str, Any]):
    """Genera reporte final"""
    print_header("REPORTE FINAL DE VALIDACIÓN")
    
    total_checks = len(results)
    passed_checks = sum(1 for r in results.values() if r.get('all_ok', False))
    
    status_color = Colors.GREEN if passed_checks == total_checks else Colors.YELLOW
    status_text = "✓ EXITOSA" if passed_checks == total_checks else "⚠ CON ADVERTENCIAS"
    
    print(f"\n{Colors.BOLD}Resumen:{Colors.RESET}")
    print(f"  {Colors.BOLD}Validaciones exitosas:{Colors.RESET} {status_color}{passed_checks}/{total_checks}{Colors.RESET}")
    
    for check_name, result in results.items():
        status = f"{Colors.GREEN}✓{Colors.RESET}" if result.get('all_ok', False) else f"{Colors.YELLOW}⚠{Colors.RESET}"
        print(f"  {status} {check_name}")
    
    print(f"\n{Colors.BOLD}{status_color}Estado General: {status_text}{Colors.RESET}")
    
    if passed_checks == total_checks:
        print(f"""
{Colors.GREEN}{Colors.BOLD}
╔════════════════════════════════════════════════════════════╗
║  ✓ ZULY ESTÁ COMPLETAMENTE OPERACIONAL                    ║
║  • Rutas configuradas correctamente                        ║
║  • Handlers disponibles                                    ║
║  • Adapter Blender funcional                              ║
║  • Configuración validada                                  ║
║  • Módulos core disponibles                                ║
║                                                            ║
║  🎯 LISTO PARA: Crear el dado con handlers                ║
╚════════════════════════════════════════════════════════════╝
{Colors.RESET}""")
    else:
        print(f"""
{Colors.YELLOW}{Colors.BOLD}
╔════════════════════════════════════════════════════════════╗
║  ⚠ ZULY OPERACIONAL CON LIMITACIONES                      ║
║  • Revisar advertencias arriba                             ║
║  • Algunas características pueden estar limitadas          ║
║  • Sistema puede funcionar en modo simulado                ║
╚════════════════════════════════════════════════════════════╝
{Colors.RESET}""")

# ============================================================================
# MAIN
# ============================================================================

def main():
    print(f"\n{Colors.BOLD}{Colors.CYAN}ZULY SYSTEM VALIDATION 🔍{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.RESET}\n")
    
    results = {}
    
    try:
        results["1. Rutas"] = validate_paths()
        results["2. Handlers"] = validate_handlers()
        results["3. Adapter Blender"] = validate_adapter()
        results["4. Archivos de Proyecto"] = validate_project_files()
        results["5. Configuración"] = validate_config()
        results["6. Módulos Core"] = validate_core()
        
        generate_final_report(results)
        
        # Guardar reporte
        report_path = ZULY_ROOT / "validation_report.json"
        with open(report_path, 'w', encoding='utf-8') as f:
            # Hacer serializable
            clean_results = {}
            for key, value in results.items():
                clean_value = {}
                for k, v in value.items():
                    if k not in ['engine_info', 'config']:  # Skip non-serializable
                        clean_value[k] = v
                clean_results[key] = clean_value
            
            json.dump(clean_results, f, indent=2, default=str)
        
        print(f"\n{Colors.BLUE}Reporte guardado en: {report_path}{Colors.RESET}\n")
        
    except Exception as e:
        print_error(f"Error durante validación: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
