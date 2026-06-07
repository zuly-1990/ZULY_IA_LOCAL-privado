#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🗑️ Script de limpieza - Elimina ZULY_PROJECTS si existe
"""

import shutil
from pathlib import Path

zuly_path = Path('c:/Users/Admin/Desktop/ZULY_IA_LOCAL')
zuly_projects = zuly_path / 'ZULY_PROJECTS'

print("="*60)
print("🧹 LIMPIEZA - Eliminando ZULY_PROJECTS")
print("="*60)

if zuly_projects.exists():
    try:
        shutil.rmtree(zuly_projects)
        print(f"✅ ZULY_PROJECTS eliminado completamente")
    except Exception as e:
        print(f"⚠️  Error: {e}")
else:
    print(f"ℹ️  ZULY_PROJECTS no existe (ya fue eliminado)")

print("="*60)
