#!/usr/bin/env python3
"""
Limpieza controlada de archivos en raíz de ZULY.
Mueve archivos a directorios organizados.
"""

import os
import shutil
from pathlib import Path
from datetime import datetime

BASE_DIR = Path("c:/Users/Admin/Desktop/ZULY_IA_LOCAL")

# Directorios destino
DIRS = {
    'archive_zuly': BASE_DIR / "archive" / "zuly_old_scripts",
    'archive_test': BASE_DIR / "archive" / "test_scripts",
    'archive_demo': BASE_DIR / "archive" / "demo_scripts",
    'docs_analysis': BASE_DIR / "docs" / "analysis_reports",
    'docs_sessions': BASE_DIR / "docs" / "session_logs",
    'temp': BASE_DIR / "temp",
}

# Archivos a preservar (no mover)
KEEP_FILES = {
    'README_INDICE.md', 'PROGRESO_CONSOLIDACION.md', 'DEUDA_TECNICA.md',
    'requirements.txt', '.env.blender', 'config.json',
    'zuly_cli.py', 'zuly_lab.py', 'zuly_trabajo_continuo.py',
    'cleanup_root_files.py',  # este script
}

# Patrones de archivos a mover
PATTERNS = {
    'archive_zuly': ['zuly_*.py'],
    'archive_test': ['test_*.py'],
    'archive_demo': ['demo_*.py'],
    'docs_analysis': [
        'ANALISIS_*.txt', 'ANALISIS_*.md',
        'DASHBOARD_*.md', 'DASHBOARD_*.txt',
        'RESUMEN_*.txt', 'RESUMEN_*.md',
        'COMPARATIVA_*.md', 'INFORME_*.md',
        'PLAN_*.md', 'PLAN_*.txt',
        'OPINION_*.txt', 'OPINION_*.md',
        'AUDITORIA_*.md',
    ],
    'docs_sessions': [
        'lab_output*.txt', 'lab_*.txt', 'lab_*.log',
        'debug_*.txt', 'debug_*.log',
        'reto_*_output.txt', 'reto_*_real.log',
        'test_output*.log', 'test_output*.txt',
    ],
}

def ensure_dirs():
    """Crea directorios si no existen."""
    for dir_path in DIRS.values():
        try:
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"✓ Directorio listo: {dir_path.relative_to(BASE_DIR)}")
        except FileExistsError:
            # El directorio ya existe como archivo (no debería pasar, pero lo manejamos)
            print(f"✓ Directorio ya existe: {dir_path.relative_to(BASE_DIR)}")

def should_keep(filename):
    """Determina si un archivo debe preservarse."""
    if filename in KEEP_FILES:
        return True
    # Preservar archivos core del sistema
    if filename.startswith('core'):
        return True
    if filename in ['agent.py', 'intent_manager.py', 'blender_adapter.py']:
        return True
    return False

def move_files():
    """Mueve archivos según patrones."""
    moved = 0
    errors = []
    
    for dest_key, patterns in PATTERNS.items():
        dest_dir = DIRS[dest_key]
        for pattern in patterns:
            # Buscar archivos matching el patrón
            for file_path in BASE_DIR.glob(pattern):
                if file_path.is_file() and not should_keep(file_path.name):
                    try:
                        dest = dest_dir / file_path.name
                        # Si ya existe, agregar timestamp
                        if dest.exists():
                            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                            dest = dest_dir / f"{file_path.stem}_{timestamp}{file_path.suffix}"
                        
                        shutil.move(str(file_path), str(dest))
                        print(f"  → {file_path.name} → {dest_dir.relative_to(BASE_DIR)}/")
                        moved += 1
                    except Exception as e:
                        errors.append(f"Error moviendo {file_path.name}: {e}")
    
    return moved, errors

def count_remaining():
    """Cuenta archivos restantes en raíz."""
    extensions = {'.py', '.md', '.txt', '.json', '.log'}
    files = [f for f in BASE_DIR.iterdir() if f.is_file() and f.suffix in extensions]
    return len(files), files

def main():
    print("="*60)
    print("LIMPIEZA DE ARCHIVOS EN RAÍZ ZULY")
    print("="*60)
    
    # Contar inicial
    initial_count, _ = count_remaining()
    print(f"\nArchivos iniciales en raíz: {initial_count}")
    
    # Crear directorios
    print("\n1. Creando directorios...")
    ensure_dirs()
    
    # Mover archivos
    print("\n2. Moviendo archivos...")
    moved, errors = move_files()
    
    # Resultado
    final_count, remaining = count_remaining()
    
    print(f"\n3. Resultado:")
    print(f"   Archivos movidos: {moved}")
    print(f"   Archivos restantes en raíz: {final_count}")
    print(f"   Reducción: {initial_count - final_count} archivos")
    
    if errors:
        print(f"\n   Errores ({len(errors)}):")
        for e in errors[:5]:
            print(f"     - {e}")
    
    print("\n" + "="*60)
    print("LIMPIEZA COMPLETADA")
    print("="*60)
    
    # Listar algunos archivos que quedaron
    print("\nArchivos que permanecen en raíz (primeros 20):")
    for f in sorted(remaining)[:20]:
        print(f"  - {f.name}")
    if len(remaining) > 20:
        print(f"  ... y {len(remaining) - 20} más")

if __name__ == "__main__":
    main()
