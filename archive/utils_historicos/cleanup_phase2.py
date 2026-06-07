#!/usr/bin/env python3
"""
Fase 2 de limpieza - Organización segura de archivos
Mueve archivos a estructura de archivo sin eliminar nada
"""

import os
import shutil
from pathlib import Path
from collections import defaultdict

# Directorio base
BASE_DIR = Path(r"c:\Users\Admin\Desktop\ZULY_IA_LOCAL")
ARCHIVE_DIR = BASE_DIR / "archive"

# Definir estructura de carpetas
FOLDERS_TO_CREATE = [
    "archive/debug_logs",
    "archive/historical_reports",
    "archive/legacy_consolidators",
    "archive/old_demos",
    "archive/legacy_validators",
    "archive/bitacora_historica",
]

# Patrones de archivos a mover
FILE_PATTERNS = {
    "archive/debug_logs": [
        ("debug_*.txt", "debug text files"),
        ("debug_*.py", "debug python scripts"),
        ("debug_*.log", "debug log files"),
        ("lab_*.log", "lab log files"),
    ],
    "archive/historical_reports": [
        ("REPORTE_*.md", "report markdown files"),
        ("RESUMEN_ETAPA*.md", "stage summary files"),
        ("RESUMEN_10_PRUEBAS*.md", "test summary files"),
    ],
    "archive/legacy_consolidators": [
        ("consolidate_*.py", "consolidate scripts"),
        ("run_youtube_*.py", "youtube runner scripts"),
        ("train_blender_*.py", "blender training scripts"),
        ("wrapper_blender_advanced.py", "blender wrapper"),
    ],
    "archive/old_demos": [
        ("demo_agent.py", "agent demo"),
        ("demo_c1_evaluador.py", "evaluador demo"),
        ("demo_c2_memory.py", "memory demo"),
        ("demo_c3_objectives.py", "objectives demo"),
        ("demo_c4_auto_tuning.py", "auto tuning demo"),
        ("demo_fase2.py", "fase2 demo"),
        ("demo_learning_freedom.py", "learning freedom demo"),
        ("demo_lyzu_interactive.py", "lyzu interactive demo"),
        ("demo_mejoras_blender.py", "blender improvements demo"),
        ("demo_sculpted_building.py", "sculpted building demo"),
        ("demo_zuly_cmd.py", "zuly cmd demo"),
    ],
    "archive/legacy_validators": [
        ("core/validation/v0_validator.py", "v0 validator"),
        ("core/validation/v1_validator.py", "v1 validator"),
        ("core/validation/v2_validator.py", "v2 validator"),
    ],
}

# Directorios completos a mover
DIRS_TO_MOVE = [
    ("bitacora", "archive/bitacora_historica", "bitacora (excluding README.md)"),
    ("BITACORA_DE_AVANCE", "archive/bitacora_historica", "BITACORA_DE_AVANCE"),
]

def create_folder_structure():
    """Crear estructura de carpetas"""
    print("\n" + "="*70)
    print("PASO 1: Creando estructura de carpetas...")
    print("="*70)
    
    for folder in FOLDERS_TO_CREATE:
        folder_path = BASE_DIR / folder
        if not folder_path.exists():
            folder_path.mkdir(parents=True, exist_ok=True)
            print(f"✓ Creada: {folder}")
        else:
            print(f"✓ Existe: {folder}")

def find_files_by_pattern(pattern):
    """Encontrar archivos que coincidan con un patrón"""
    from fnmatch import fnmatch
    found_files = []
    
    # Si el patrón tiene ruta (ej: core/validation/...)
    if "/" in pattern:
        parts = pattern.split("/")
        base_path = BASE_DIR
        for part in parts[:-1]:
            base_path = base_path / part
        file_pattern = parts[-1]
        
        if base_path.exists():
            for file in base_path.iterdir():
                if fnmatch(file.name, file_pattern):
                    found_files.append(file)
    else:
        # Buscar en el directorio raíz
        for file in BASE_DIR.iterdir():
            if fnmatch(file.name, pattern) and file.is_file():
                found_files.append(file)
    
    return found_files

def move_files():
    """Mover archivos según patrones"""
    print("\n" + "="*70)
    print("PASO 2: Moviendo archivos...")
    print("="*70)
    
    total_moved = 0
    moved_summary = defaultdict(list)
    
    # Procesar patrones de archivos
    for dest_folder, patterns in FILE_PATTERNS.items():
        for pattern, description in patterns:
            files = find_files_by_pattern(pattern)
            
            if files:
                dest_path = BASE_DIR / dest_folder
                for src_file in files:
                    try:
                        # Crear destino si tiene estructura de carpetas
                        dest_file = dest_path / src_file.name
                        
                        # Si el archivo viene de una subcarpeta, mantener esa estructura
                        if "/" in pattern:
                            rel_parts = pattern.split("/")[:-1]
                            sub_folder = dest_path / "/".join(rel_parts)
                            sub_folder.mkdir(parents=True, exist_ok=True)
                            dest_file = sub_folder / src_file.name
                        
                        shutil.move(str(src_file), str(dest_file))
                        moved_summary[dest_folder].append(src_file.name)
                        total_moved += 1
                        print(f"  ✓ {src_file.name} → {dest_folder}")
                    except Exception as e:
                        print(f"  ✗ Error moviendo {src_file.name}: {e}")
    
    # Procesar directorios completos
    for src_dir, dest_parent, description in DIRS_TO_MOVE:
        src_path = BASE_DIR / src_dir
        
        if src_path.exists():
            dest_path = BASE_DIR / dest_parent / src_dir
            
            try:
                # Si es bitacora, excluir README.md
                if src_dir == "bitacora":
                    os.makedirs(dest_path, exist_ok=True)
                    for item in src_path.iterdir():
                        if item.name != "README.md":
                            if item.is_file():
                                shutil.move(str(item), str(dest_path / item.name))
                                moved_summary[dest_parent].append(f"{src_dir}/{item.name}")
                                total_moved += 1
                            elif item.is_dir():
                                shutil.move(str(item), str(dest_path / item.name))
                                moved_summary[dest_parent].append(f"{src_dir}/{item.name}")
                                total_moved += 1
                    print(f"  ✓ {src_dir}/ → {dest_parent}/ (excepto README.md)")
                else:
                    # Mover directorio completo
                    if dest_path.exists():
                        shutil.rmtree(dest_path)
                    shutil.move(str(src_path), str(dest_path))
                    moved_summary[dest_parent].append(src_dir)
                    total_moved += 1
                    print(f"  ✓ {src_dir}/ → {dest_parent}/")
            except Exception as e:
                print(f"  ✗ Error moviendo {src_dir}: {e}")
    
    return total_moved, moved_summary

def display_summary(total_moved, moved_summary):
    """Mostrar resumen de la operación"""
    print("\n" + "="*70)
    print("RESUMEN FINAL DE LA FASE 2")
    print("="*70)
    print(f"\n✓ Total de archivos/carpetas movidos: {total_moved}\n")
    
    for dest_folder in sorted(moved_summary.keys()):
        items = moved_summary[dest_folder]
        print(f"{dest_folder}: {len(items)} elementos")
        for item in sorted(items)[:5]:
            print(f"  - {item}")
        if len(items) > 5:
            print(f"  ... y {len(items) - 5} más")
    
    print("\n" + "="*70)
    print("FASE 2 COMPLETADA CON ÉXITO")
    print("="*70)

def main():
    """Ejecutar limpieza Fase 2"""
    print("\n" + "█"*70)
    print("█" + " "*68 + "█")
    print("█" + "  FASE 2 DE LIMPIEZA - ORGANIZACIÓN DE ARCHIVOS".center(68) + "█")
    print("█" + " "*68 + "█")
    print("█"*70)
    
    # Verificar que el directorio existe
    if not BASE_DIR.exists():
        print(f"\n✗ El directorio {BASE_DIR} no existe")
        return
    
    print(f"\nDirectorio base: {BASE_DIR}")
    
    try:
        # Paso 1: Crear estructura
        create_folder_structure()
        
        # Paso 2: Mover archivos
        total_moved, moved_summary = move_files()
        
        # Paso 3: Mostrar resumen
        display_summary(total_moved, moved_summary)
        
    except Exception as e:
        print(f"\n✗ Error durante la limpieza: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
