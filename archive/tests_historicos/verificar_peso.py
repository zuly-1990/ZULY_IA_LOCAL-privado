#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📊 VERIFICADOR DE PESO - Archivos ZULY
Herramienta simple para revisar peso de patrones
"""

import os
from pathlib import Path
from datetime import datetime

ZULY_BASE = Path("c:/Users/Admin/Desktop/ZULY_IA_LOCAL")

def verificar_peso(archivo_path):
    """Verifica peso de un archivo y da formato legible"""
    if not os.path.exists(archivo_path):
        return None, "Archivo no existe"
    
    size_bytes = os.path.getsize(archivo_path)
    size_kb = size_bytes / 1024
    size_mb = size_kb / 1024
    
    # Formato legible
    if size_mb >= 1:
        size_str = f"{size_mb:.2f} MB ({size_kb:.1f} KB)"
    else:
        size_str = f"{size_kb:.2f} KB"
    
    # Evaluación
    if size_kb < 500:
        status = "✅ ÓPTIMO"
        icon = "🟢"
    elif size_kb < 2000:
        status = "✅ ACEPTABLE"
        icon = "🟡"
    elif size_kb < 5000:
        status = "⚠️ PESADO"
        icon = "🟠"
    else:
        status = "❌ GRASA DIGITAL"
        icon = "🔴"
    
    return {
        "bytes": size_bytes,
        "kb": size_kb,
        "mb": size_mb,
        "texto": size_str,
        "status": status,
        "icon": icon
    }

def verificar_temp_arena():
    """Verifica todos los archivos en temp_arena"""
    print("="*70)
    print("📊 VERIFICADOR DE PESO - Archivos en temp_arena/")
    print("="*70)
    
    temp_arena = ZULY_BASE / "archivo_zuly" / "temp_arena"
    
    if not temp_arena.exists():
        print("❌ Carpeta temp_arena no existe")
        return
    
    blend_files = list(temp_arena.glob("*.blend"))
    
    if not blend_files:
        print("📭 No hay archivos .blend en temp_arena/")
        return
    
    print(f"\n📁 Total archivos: {len(blend_files)}\n")
    
    total_kb = 0
    for blend_file in sorted(blend_files):
        resultado = verificar_peso(blend_file)
        total_kb += resultado["kb"]
        
        print(f"{resultado['icon']} {blend_file.name}")
        print(f"   📊 Peso: {resultado['texto']}")
        print(f"   🏷️  Estado: {resultado['status']}")
        print()
    
    print("="*70)
    print(f"📦 TOTAL: {total_kb:.2f} KB ({total_kb/1024:.2f} MB)")
    print("="*70)

def verificar_mastered():
    """Verifica todos los patrones sellados"""
    print("\n" + "="*70)
    print("🏆 PATRONES SELLADOS - Pesos en mastered/")
    print("="*70)
    
    mastered = ZULY_BASE / "archivo_zuly" / "por_estado_aprendizaje" / "mastered"
    
    if not mastered.exists():
        print("❌ Carpeta mastered no existe")
        return
    
    pattern_folders = [f for f in mastered.iterdir() if f.is_dir()]
    
    if not pattern_folders:
        print("📭 No hay patrones sellados")
        return
    
    print(f"\n📚 Total patrones: {len(pattern_folders)}\n")
    
    for folder in sorted(pattern_folders):
        blend_file = folder / "blend" / f"{folder.name}.blend"
        if blend_file.exists():
            resultado = verificar_peso(blend_file)
            print(f"{resultado['icon']} {folder.name}")
            print(f"   📊 {resultado['texto']} - {resultado['status']}")
    
    print("="*70)

def comparar_pesos():
    """Compara pesos entre temp_arena y mastered"""
    print("\n" + "="*70)
    print("⚖️  COMPARACIÓN DE PESOS")
    print("="*70)
    
    temp_arena = ZULY_BASE / "archivo_zuly" / "temp_arena"
    mastered = ZULY_BASE / "archivo_zuly" / "por_estado_aprendizaje" / "mastered"
    
    temp_files = {f.stem: f for f in temp_arena.glob("*.blend")}
    mastered_patterns = [f.name for f in mastered.iterdir() if f.is_dir()]
    
    for pattern in mastered_patterns:
        temp_file = temp_files.get(pattern)
        mastered_file = mastered / pattern / "blend" / f"{pattern}.blend"
        
        if temp_file and mastered_file.exists():
            temp_size = verificar_peso(temp_file)
            master_size = verificar_peso(mastered_file)
            
            diff = temp_size["kb"] - master_size["kb"]
            
            print(f"\n📦 {pattern}")
            print(f"   📂 temp_arena:  {temp_size['texto']}")
            print(f"   🏆 mastered:    {master_size['texto']}")
            if abs(diff) > 0.1:
                print(f"   📊 Diferencia:  {diff:+.2f} KB")
    
    print("="*70)

if __name__ == "__main__":
    # Menú simple
    print("\n📊 VERIFICADOR DE PESO ZULY")
    print("="*70)
    print("\nOpciones:")
    print("  1 - Ver pesos en temp_arena/ (patrones candidatos)")
    print("  2 - Ver pesos en mastered/ (patrones sellados)")
    print("  3 - Comparar temp_arena vs mastered")
    print("  4 - Todo (completo)")
    print("  5 - Salir")
    
    opcion = input("\nSelección (1-5): ").strip()
    
    if opcion == "1":
        verificar_temp_arena()
    elif opcion == "2":
        verificar_mastered()
    elif opcion == "3":
        comparar_pesos()
    elif opcion == "4":
        verificar_temp_arena()
        verificar_mastered()
        comparar_pesos()
    elif opcion == "5":
        print("👋 Saliendo...")
    else:
        print("❌ Opción inválida. Mostrando todo por defecto:")
        verificar_temp_arena()
        verificar_mastered()
