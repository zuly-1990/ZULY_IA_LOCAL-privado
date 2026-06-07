import os
import sys
import json
import hashlib

# Script de migración de patrones de Memoria V0 a STAGING (Clean Architecture)
# Fin de Semana 1 - ZULY_LAB Master Roadmap 2026

def legacy_hash_scene(scene_data):
    """Genera un hash SHA256 simulado para legacy patterns"""
    if not scene_data:
        return hashlib.sha256(b"legacy_unknown_scene").hexdigest()
    return hashlib.sha256(str(scene_data.get('objects', [])).encode('utf-8')).hexdigest()

def migrate():
    source_file = "memory/patterns.json"
    target_file = "memory/patterns_staging.json"
    backup_file = "memory/patterns.json.bak"
    
    # 1. Verificar si hay archivo legacy
    if not os.path.exists(source_file):
        print(f"No source memory file found at {source_file}. Nothing to migrate.")
        return
    
    print(f"Leyendo patrones legacy de {source_file}...")
    try:
        with open(source_file, 'r', encoding='utf-8') as f:
            legacy_patterns = json.load(f)
    except json.JSONDecodeError:
         print("Error crítico: patterns.json está corrupto o vacío.")
         return
         
    num_patterns = len(legacy_patterns)
    print(f"Encontrados {num_patterns} patrones para migrar.")
    
    migrated_patterns = []
    
    # 2. Inyectar metadatos obligatorios a cada patrón
    for p in legacy_patterns:
        context = p.get('context', {})
        
        # Inyectar campos de entorno si no existen
        context['origin'] = context.get('origin', 'legacy_migration')
        context['blender_version'] = context.get('blender_version', 'unknown_legacy')
        context['active_mode'] = context.get('active_mode', 'UNKNOWN')
        context['engine_adapter_version'] = context.get('engine_adapter_version', 'v0_legacy')
        
        # Inyectar Hash Estructural (Regla de Saneamiento)
        if 'scene_before' in context:
             context['environment_hash'] = legacy_hash_scene(context['scene_before'])
        else:
             context['environment_hash'] = legacy_hash_scene({})
             
        p['context'] = context
        
        # Actualizar metadata
        metadata = p.get('metadata', {})
        metadata['status'] = 'STAGING'
        p['metadata'] = metadata
        
        migrated_patterns.append(p)
        
    # 3. Guardar en STAGING
    print(f"Guardando en repositorio tipo STAGING ({target_file})...")
    os.makedirs(os.path.dirname(target_file), exist_ok=True)
    with open(target_file, 'w', encoding='utf-8') as f:
        json.dump(migrated_patterns, f, indent=2)
        
    # 4. Crear el backup safe
    print(f"Respaldando archivo original a {backup_file}...")
    os.rename(source_file, backup_file)
    
    print("Migración de memoria exitosa. ✅")

if __name__ == "__main__":
    migrate()
