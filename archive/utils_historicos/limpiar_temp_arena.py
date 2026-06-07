#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧹 LIMPIEZA TEMP_ARENA - Borrar .blend viejos antes de regenerar CUB-001
"""

from pathlib import Path
import glob

zuly_path = Path('c:/Users/Admin/Desktop/ZULY_IA_LOCAL')
temp_arena = zuly_path / 'archivo_zuly' / 'temp_arena'

print("="*60)
print("🧹 LIMPIANDO TEMP_ARENA - Archivos .blend viejos")
print("="*60)

# Buscar todos los .blend
blend_files = list(temp_arena.glob('*.blend'))
json_files = list(temp_arena.glob('*_JUES_REPORT.json'))

print(f"\n📁 Archivos .blend encontrados: {len(blend_files)}")
for f in blend_files:
    size_kb = f.stat().st_size / 1024
    print(f"   • {f.name} ({size_kb:.1f} KB)")

print(f"\n📄 Reportes JUES a eliminar: {len(json_files)}")
for f in json_files:
    print(f"   • {f.name}")

# Eliminar
print("\n🗑️ Eliminando archivos...")
eliminados = 0
for f in blend_files + json_files:
    try:
        f.unlink()
        print(f"   ✅ Eliminado: {f.name}")
        eliminados += 1
    except Exception as e:
        print(f"   ❌ Error eliminando {f.name}: {e}")

print(f"\n✅ LIMPIEZA COMPLETADA: {eliminados} archivos eliminados")
print("="*60)
print("📁 Temp_arena ahora está limpio")
print("🆕 Listo para regenerar CUB-001 desde cero")
print("="*60)
