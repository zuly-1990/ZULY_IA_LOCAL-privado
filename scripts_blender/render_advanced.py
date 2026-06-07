#!/usr/bin/env python3
# scripts_blender/render_advanced.py
"""
Script avanzado de renderizado para Blender.

Este script se ejecuta DENTRO de Blender (bpy context) y realiza renders
con opciones avanzadas de calidad, formato y post-procesamiento.

Uso desde Python (sin Blender):
    subprocess.run([BLENDER_PATH, "--background", "--python", "render_advanced.py", 
                   "--config", "config.json"])

Uso desde Blender Python Console:
    exec(open("render_advanced.py").read())
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, Any, Optional


def parse_arguments():
    """Parsea argumentos de línea de comandos."""
    parser = argparse.ArgumentParser(description="Renderizado avanzado en Blender")
    
    parser.add_argument("--config", type=str, default="render_config.json",
                        help="Archivo JSON con configuración de render")
    parser.add_argument("--output", type=str, help="Ruta de salida (sobrescribe config)")
    parser.add_argument("--samples", type=int, help="Muestras (sobrescribe config)")
    parser.add_argument("--resolution", type=str, help="Resolución WIDTHxHEIGHT (sobrescribe config)")
    parser.add_argument("--engine", type=str, choices=['CYCLES', 'EEVEE'],
                        help="Motor de render (sobrescribe config)")
    parser.add_argument("--format", type=str, choices=['PNG', 'JPEG', 'TIFF', 'EXR'],
                        help="Formato de salida (sobrescribe config)")
    parser.add_argument("--denoiser", action="store_true",
                        help="Aplicar denoising (OptiX si disponible)")
    parser.add_argument("--verbose", action="store_true",
                        help="Mostrar información detallada")
    
    return parser.parse_args()


def load_config(config_path: str) -> Dict[str, Any]:
    """Carga configuración desde archivo JSON."""
    config = {
        'output_path': './render_output.png',
        'samples': 128,
        'resolution_x': 1920,
        'resolution_y': 1080,
        'engine': 'CYCLES',
        'format': 'PNG',
        'use_denoiser': False,
        'use_adaptive_sampling': True,
        'tile_size': 16,
        'use_gpu': True,
        'device': 'GPU',  # 'CPU' o 'GPU'
    }
    
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                loaded = json.load(f)
                config.update(loaded)
            print(f"✓ Configuración cargada desde {config_path}")
        except Exception as e:
            print(f"⚠ Error al cargar config: {e}. Usando valores por defecto.")
    
    return config


def apply_config(config: Dict[str, Any], verbose: bool = False):
    """Aplica configuración a Blender (requiere contexto bpy)."""
    try:
        import bpy
    except ImportError:
        print("✗ Blender Python API (bpy) no disponible.")
        print("  Este script debe ejecutarse dentro de Blender o como addon.")
        return False
    
    if verbose:
        print("\n📋 Aplicando configuración de render...")
    
    # Configurar escena
    scene = bpy.context.scene
    
    # Resolución
    scene.render.resolution_x = config['resolution_x']
    scene.render.resolution_y = config['resolution_y']
    if verbose:
        print(f"  • Resolución: {config['resolution_x']}x{config['resolution_y']}")
    
    # Motor de render
    scene.render.engine = config['engine']
    if verbose:
        print(f"  • Motor: {config['engine']}")
    
    # Formato de salida
    scene.render.image_settings.file_format = config['format']
    if verbose:
        print(f"  • Formato: {config['format']}")
    
    # Ruta de salida
    output_path = Path(config['output_path'])
    output_path.parent.mkdir(parents=True, exist_ok=True)
    scene.render.filepath = str(output_path)
    if verbose:
        print(f"  • Salida: {output_path}")
    
    # Configuración específica para CYCLES
    if config['engine'] == 'CYCLES':
        cycles = scene.cycles
        
        # Muestras
        cycles.samples = config['samples']
        cycles.preview_samples = min(config['samples'], 64)
        if verbose:
            print(f"  • Muestras: {config['samples']}")
        
        # GPU
        if config['use_gpu']:
            try:
                # Intenta usar GPU
                for scene_with_context in bpy.data.scenes:
                    scene_with_context.render.use_freestyle = False
                if hasattr(cycles, 'use_denoising'):
                    cycles.use_denoising = config['use_denoiser']
                
                # Intentar usar GPU
                cycles.use_adaptive_sampling = config['use_adaptive_sampling']
                if verbose:
                    print(f"  • Adaptive sampling: {config['use_adaptive_sampling']}")
                
                # Denoiser
                if config['use_denoiser']:
                    if hasattr(cycles, 'denoiser'):
                        cycles.denoiser = 'OPTIX'  # O 'OPENIMAGEDENOISE'
                        if verbose:
                            print(f"  • Denoiser: OPTIX")
            except Exception as e:
                if verbose:
                    print(f"  ⚠ No se pudo aplicar configuración GPU: {e}")
        
        # Tamaño de tile
        if config.get('tile_size'):
            cycles.tile_size = config['tile_size']
    
    # Configuración para EEVEE
    elif config['engine'] == 'EEVEE':
        eevee = scene.eevee
        if verbose:
            print(f"  • EEVEE configurado")
    
    if verbose:
        print("✓ Configuración aplicada correctamente.\n")
    
    return True


def render_scene(output_path: Optional[str] = None, verbose: bool = False) -> bool:
    """Renderiza la escena actual en Blender."""
    try:
        import bpy
    except ImportError:
        print("✗ Blender Python API (bpy) no disponible.")
        return False
    
    try:
        scene = bpy.context.scene
        
        if output_path:
            scene.render.filepath = output_path
        
        if verbose:
            print(f"\n🎬 Iniciando render a: {scene.render.filepath}")
            print(f"   Resolución: {scene.render.resolution_x}x{scene.render.resolution_y}")
            print(f"   Motor: {scene.render.engine}")
        
        # Renderizar
        bpy.ops.render.render(write_still=True)
        
        if verbose:
            print(f"✓ Render completado: {scene.render.filepath}")
        
        return True
    
    except Exception as e:
        print(f"✗ Error durante render: {e}")
        return False


def get_render_info(verbose: bool = False) -> Dict[str, Any]:
    """Obtiene información sobre la escena y configuración de render."""
    try:
        import bpy
    except ImportError:
        return {'error': 'bpy no disponible'}
    
    scene = bpy.context.scene
    render = scene.render
    
    info = {
        'scene_name': scene.name,
        'resolution': f"{render.resolution_x}x{render.resolution_y}",
        'engine': render.engine,
        'format': render.image_settings.file_format,
        'output_path': render.filepath,
        'frame_start': scene.frame_start,
        'frame_end': scene.frame_end,
        'fps': scene.render.fps,
    }
    
    # Información de ciclos
    if render.engine == 'CYCLES':
        cycles = scene.cycles
        info['samples'] = cycles.samples if hasattr(cycles, 'samples') else 'N/A'
        info['use_adaptive_sampling'] = cycles.use_adaptive_sampling if hasattr(cycles, 'use_adaptive_sampling') else False
    
    # Contar objetos
    info['total_objects'] = len(bpy.data.objects)
    info['total_meshes'] = len(bpy.data.meshes)
    info['total_materials'] = len(bpy.data.materials)
    info['total_lights'] = len([o for o in bpy.data.objects if o.type == 'LIGHT'])
    
    if verbose:
        print("\n📊 Información de escena:")
        for key, value in info.items():
            print(f"   {key}: {value}")
    
    return info


def main():
    """Función principal."""
    args = parse_arguments()
    verbose = args.verbose
    
    if verbose:
        print("=" * 60)
        print("RENDERIZADOR AVANZADO DE BLENDER")
        print("=" * 60)
    
    # Cargar configuración
    config = load_config(args.config)
    
    # Sobrescribir con argumentos
    if args.output:
        config['output_path'] = args.output
    if args.samples:
        config['samples'] = args.samples
    if args.engine:
        config['engine'] = args.engine
    if args.format:
        config['format'] = args.format
    if args.resolution:
        try:
            w, h = args.resolution.split('x')
            config['resolution_x'] = int(w)
            config['resolution_y'] = int(h)
        except:
            print(f"⚠ Resolución inválida: {args.resolution}")
    
    config['use_denoiser'] = args.denoiser or config.get('use_denoiser', False)
    
    # Aplicar configuración a Blender
    success = apply_config(config, verbose)
    
    if success:
        # Obtener información
        info = get_render_info(verbose)
        
        # Renderizar
        render_success = render_scene(verbose=verbose)
        
        if render_success:
            if verbose:
                print("\n✓ Proceso completado exitosamente.")
            sys.exit(0)
        else:
            if verbose:
                print("\n✗ Error durante el renderizado.")
            sys.exit(1)
    else:
        if verbose:
            print("\n✗ No se pudo aplicar la configuración.")
        sys.exit(1)


if __name__ == "__main__":
    main()
