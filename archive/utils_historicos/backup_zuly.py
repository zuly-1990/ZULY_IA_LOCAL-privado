#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔒 SISTEMA DE BACKUP ZULY - Protección de Patrones Sellados
Previene borrado accidental y guarda copias de seguridad
"""

import json
import shutil
import hashlib
from pathlib import Path
from datetime import datetime

ZULY_BASE = Path("c:/Users/Admin/Desktop/ZULY_IA_LOCAL")
MASTERED = ZULY_BASE / "archivo_zuly" / "por_estado_aprendizaje" / "mastered"
BACKUP_DIR = ZULY_BASE / "archivo_zuly" / "BACKUP_SEGURO"
PROTECCION_FILE = ZULY_BASE / "archivo_zuly" / "PROTECCION_PATRONES.json"

def crear_backup():
    """Crea copia de seguridad de todos los patrones sellados"""
    print("="*60)
    print("🔒 CREANDO BACKUP DE SEGURIDAD")
    print("="*60)
    
    # Crear directorio backup
    backup_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_folder = BACKUP_DIR / f"BACKUP_{backup_timestamp}"
    backup_folder.mkdir(parents=True, exist_ok=True)
    
    # Contar patrones
    if not MASTERED.exists():
        print("❌ No hay patrones para respaldar")
        return None
    
    pattern_folders = [f for f in MASTERED.iterdir() if f.is_dir()]
    
    if not pattern_folders:
        print("📭 No hay patrones en mastered/")
        return None
    
    print(f"\n📦 Encontrados {len(pattern_folders)} patrones")
    print(f"📁 Destino: {backup_folder}\n")
    
    # Copiar cada patrón
    for pattern in sorted(pattern_folders):
        src = pattern
        dst = backup_folder / pattern.name
        
        try:
            shutil.copytree(src, dst)
            print(f"   ✅ {pattern.name}")
        except Exception as e:
            print(f"   ❌ {pattern.name}: {e}")
    
    # Crear registro del backup
    registro = {
        "fecha": datetime.now().isoformat(),
        "timestamp": backup_timestamp,
        "patrones_respaldados": len(pattern_folders),
        "ubicacion": str(backup_folder),
        "lista_patrones": [p.name for p in pattern_folders]
    }
    
    registro_path = backup_folder / "BACKUP_REGISTRO.json"
    with open(registro_path, 'w', encoding='utf-8') as f:
        json.dump(registro, f, indent=2, ensure_ascii=False)
    
    print(f"\n📄 Registro: {registro_path}")
    print(f"✅ Backup completado: {len(pattern_folders)} patrones seguros")
    
    return backup_folder

def verificar_integridad():
    """Verifica que los patrones no hayan sido alterados"""
    print("\n" + "="*60)
    print("🔍 VERIFICANDO INTEGRIDAD DE PATRONES")
    print("="*60)
    
    if not MASTERED.exists():
        print("❌ No hay patrones para verificar")
        return
    
    pattern_folders = [f for f in MASTERED.iterdir() if f.is_dir()]
    
    if not pattern_folders:
        print("📭 Sin patrones")
        return
    
    print(f"\n📦 Verificando {len(pattern_folders)} patrones:\n")
    
    todo_ok = True
    for pattern in sorted(pattern_folders):
        blend_file = pattern / "blend" / f"{pattern.name}.blend"
        json_file = pattern / "json" / f"{pattern.name}.json"
        cert_file = pattern / "certificado" / "CERTIFICADO_SELLO.json"
        
        status = "✅" if blend_file.exists() and json_file.exists() and cert_file.exists() else "❌"
        if status == "❌":
            todo_ok = False
        
        print(f"   {status} {pattern.name}")
        
        if not blend_file.exists():
            print(f"      ❌ Falta archivo .blend")
        if not json_file.exists():
            print(f"      ❌ Falta archivo JSON")
        if not cert_file.exists():
            print(f"      ❌ Falta certificado")
    
    print("\n" + "="*60)
    if todo_ok:
        print("✅ TODOS LOS PATRONES ESTÁN COMPLETOS E INTACTOS")
    else:
        print("⚠️  ALGUNOS PATRONES TIENEN PROBLEMAS - RESTAURAR DESDE BACKUP")
    print("="*60)
    
    return todo_ok

def listar_backups():
    """Lista todos los backups disponibles"""
    print("\n" + "="*60)
    print("📂 BACKUPS DISPONIBLES")
    print("="*60)
    
    if not BACKUP_DIR.exists():
        print("📭 No hay backups creados aún")
        return []
    
    backups = [d for d in BACKUP_DIR.iterdir() if d.is_dir() and d.name.startswith("BACKUP_")]
    backups.sort(reverse=True)  # Más reciente primero
    
    if not backups:
        print("📭 Sin backups")
        return []
    
    print(f"\n📦 Total backups: {len(backups)}\n")
    
    for i, backup in enumerate(backups, 1):
        registro_file = backup / "BACKUP_REGISTRO.json"
        if registro_file.exists():
            with open(registro_file, 'r', encoding='utf-8') as f:
                registro = json.load(f)
            fecha = registro.get("fecha", "Desconocida")
            patrones = registro.get("patrones_respaldados", 0)
            print(f"   {i}. {backup.name}")
            print(f"      📅 {fecha}")
            print(f"      📦 {patrones} patrones")
        else:
            print(f"   {i}. {backup.name} (sin registro)")
    
    return backups

def proteger_contra_borrado():
    """Crea archivo de protección contra borrado accidental"""
    print("\n" + "="*60)
    print("🛡️  ACTIVANDO PROTECCIÓN CONTRA BORRADO")
    print("="*60)
    
    proteccion = {
        "sistema": "ZULY Protección de Patrones",
        "version": "1.0",
        "fecha_activacion": datetime.now().isoformat(),
        "advertencia": "⚠️  ESTOS ARCHIVOS SON PATRONES SELLADOS OFICIALES",
        "instrucciones": {
            "no_borrar": "No borrar carpetas en mastered/ sin backup previo",
            "no_mover": "No mover archivos de mastered/ a otras ubicaciones",
            "no_renombrar": "No renombrar carpetas ni archivos en mastered/",
            "backup": "Hacer backup antes de cualquier modificación"
        },
        "recuperacion": "Si borraste accidentalmente, restaurar desde archivo_zuly/BACKUP_SEGURO/",
        "contacto": "Cascade - ZULY Lead Developer"
    }
    
    with open(PROTECCION_FILE, 'w', encoding='utf-8') as f:
        json.dump(proteccion, f, indent=2, ensure_ascii=False)
    
    # Crear archivo README visible
    readme_path = MASTERED / "⚠️_NO_BORRAR_PATRONES_SELLADOS.txt"
    readme_content = """
╔═══════════════════════════════════════════════════════════╗
║  ⚠️  ADVERTENCIA - PATRONES SELLADOS OFICIALES           ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║  Estas carpetas contienen los patrones oficiales de ZULY   ║
║  que han sido validados y sellados por JUES-BOT.          ║
║                                                           ║
║  ⚠️  NO BORRAR                                            ║
║  ⚠️  NO MOVER                                             ║
║  ⚠️  NO RENOMBRAR                                         ║
║                                                           ║
║  Si necesitas espacio, haz backup primero:                ║
║  → Ejecutar: python backup_zuly.py                        ║
║                                                           ║
║  Si borraste accidentalmente:                             ║
║  → Restaurar desde: archivo_zuly/BACKUP_SEGURO/           ║
║                                                           ║
║  Último backup: VERIFICAR FECHA EN BACKUP_SEGURO/         ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
"""
    
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print(f"✅ Protección activada:")
    print(f"   📄 {PROTECCION_FILE}")
    print(f"   📄 {readme_path}")
    print(f"\n🛡️  Los patrones están protegidos contra borrado accidental")

def main():
    """Menú principal"""
    print("\n" + "="*70)
    print("🔒 SISTEMA DE PROTECCIÓN ZULY")
    print("="*70)
    
    while True:
        print("\nOpciones:")
        print("  1 - Crear backup de seguridad AHORA")
        print("  2 - Verificar integridad de patrones")
        print("  3 - Listar backups disponibles")
        print("  4 - Activar protección contra borrado")
        print("  5 - Todo (backup + verificar + proteger)")
        print("  6 - Salir")
        
        opcion = input("\nSelección (1-6): ").strip()
        
        if opcion == "1":
            crear_backup()
        elif opcion == "2":
            verificar_integridad()
        elif opcion == "3":
            listar_backups()
        elif opcion == "4":
            proteger_contra_borrado()
        elif opcion == "5":
            crear_backup()
            verificar_integridad()
            proteger_contra_borrado()
            print("\n🛡️  PROTECCIÓN COMPLETA ACTIVADA")
        elif opcion == "6":
            print("👋 Saliendo...")
            break
        else:
            print("❌ Opción inválida")

if __name__ == "__main__":
    main()
